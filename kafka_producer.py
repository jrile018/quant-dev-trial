# kafka_producer.py

import json
import time
from kafka import KafkaProducer
import pandas as pd

# Load and filter the dataset
df = pd.read_csv('l1_day.csv')
df['ts_event'] = pd.to_datetime(df['ts_event'], errors='coerce')
df = df[df['ts_event'].dt.time.between(pd.to_datetime("13:36:32").time(),
                                       pd.to_datetime("13:45:14").time())]

# Sort by event timestamp
df = df.sort_values('ts_event')

# Create snapshots grouped by ts_event
snapshots = df.groupby('ts_event')

# Setup Kafka producer
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Stream snapshots
prev_time = None
for ts, group in snapshots:
    snapshot = []
    for _, row in group.iterrows():
        snapshot.append({
            'ts_event': str(ts),
            'publisher_id': int(row['publisher_id']),
            'ask_px_00': float(row['ask_px_00']),
            'ask_sz_00': int(row['ask_sz_00']),
            'fee': 0.0,
            'rebate': 0.0
        })

    producer.send('mock_l1_stream', value=snapshot)
    print(f"Sent snapshot @ {ts} with {len(snapshot)} records")

    if prev_time is not None:
        delta = (ts - prev_time).total_seconds()
        time.sleep(min(delta, 0.5))
    prev_time = ts

producer.flush()
producer.close()

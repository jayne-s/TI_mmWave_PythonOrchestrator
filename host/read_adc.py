from scapy.all import sniff, UDP
from dotenv import load_dotenv
from datetime import datetime 
from minio import Minio
import numpy as np
import threading
import os
import time
import json

load_dotenv()

DEVICE_ID = os.getenv("DEVICE_ID")
INTERFACE = os.getenv("INTERFACE")
UDP_PORT = 4098
TIMEOUT = 2.0
TEMP_DIR = "C:\\RadarTemp"
os.makedirs(TEMP_DIR, exist_ok=True)
client = Minio(
  os.getenv("IP") + ":9000",
  access_key=os.getenv("MINIO_ROOT_USER"),
  secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
  secure=False
) 

print(f"Checking Connection: {client.bucket_exists("radar-data")}")

recording = False
capture_file = None
capture_filename = None
metadata_filename = None
recording_timestamp = None
recording_start = None
bytes_received = 0
timer = None
lock = threading.Lock()

stop_event = threading.Event()

def start_recording():
  global recording, capture_file, capture_filename, metadata_filename,recording_timestamp, recording_start, bytes_received

  recording = True
  recording_start = time.time()
  recording_timestamp = datetime.now()
  folder_name = recording_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
  capture_filename = os.path.join(
    TEMP_DIR,
    f"{DEVICE_ID}_{folder_name}_capture.bin"
  )
  metadata_filename = os.path.join(
    TEMP_DIR,
    f"{DEVICE_ID}_{folder_name}_metadata.json"
  )
  capture_file = open(capture_filename, "wb")
  bytes_received = 0
  print(f"\nStarted Recording: {capture_filename}")

def finish_recording():
  global recording, capture_file, timer
  with lock:
    if not recording:
      return
    print("Recording Finished")
    capture_file.close()

    folder = recording_timestamp.strftime("%Y-%m-%d_%H-%M-%S")

    duration = time.time() - recording_start
    metadata = {
      "device_id": DEVICE_ID,
      "timestamp": recording_timestamp.isoformat(),
      "duration_seconds": duration,
      "bytes_received": bytes_received
    }
    with open(metadata_filename, "w") as f:
      json.dump(metadata, f, indent=4)

    print(f"Ready to Upload: {capture_filename} || {metadata_filename}")
    try:
      client.fput_object(
        bucket_name="radar-data",
        object_name=f"{DEVICE_ID}/{folder}/capture.bin",
        file_path=capture_filename
      )
      client.fput_object(
        bucket_name="radar-data",
        object_name=f"{DEVICE_ID}/{folder}/metadata.json",
        file_path=metadata_filename
      )
      os.remove(capture_filename)
      os.remove(metadata_filename)
      print("Upload Completed Successfully!")
      stop_event.set()
    except Exception as e:
      print(f"Error Occurred While Uploading: {e}")
      print("Keeping Local Files --- stored in RadarTemp directory")

    recording = False
    timer = None

def reset_timer():
  global timer
  if timer is not None:
    timer.cancel()
  timer = threading.Timer(TIMEOUT, finish_recording)
  timer.daemon = True
  timer.start()

def process_packet(pkt):
  global bytes_received
  if not pkt.haslayer(UDP):
    return
  if pkt[UDP].dport != UDP_PORT:
    return
  data = bytes(pkt[UDP].payload)
  with lock:
    if not recording:
      start_recording()
    capture_file.write(data)
    bytes_received+=len(data)
    reset_timer()

print("Listening...")

print("READY", flush=True)

while not stop_event.is_set():
  sniff(
    iface=INTERFACE,
    store=False,
    prn=process_packet,
    timeout=1
  )
  
print("Program Exiting...")

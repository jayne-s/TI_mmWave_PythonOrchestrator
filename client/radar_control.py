import subprocess
import paramiko
from dotenv import load_dotenv

load_dotenv()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    hostname=os.getenv("HOSTNAME"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD")
)

subprocess.run([
    "dotnet", "run", "--project", "RadarRemote"
])

print("Capture Complete!")

stdin, stdout, stderr = ssh.exec_command(
    'python C:\\path\\to\\upload_adc.py' # change to host's path to upload_adc.py
)

print("DONE!")


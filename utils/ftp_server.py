from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import utils.constants
import subprocess

# Define the directory where you want to store files
FTP_WORKING_DIRECTORY = utils.constants.LLM_WORKING_FOLDER + "/ftp_server"
subprocess.run(f"mkdir -p {FTP_WORKING_DIRECTORY}", shell=True)

# Instantiate a dummy authorizer for managing 'virtual' users
authorizer = DummyAuthorizer()

# Add a user with full r/w permissions (username: 'user', password: '12345')
authorizer.add_user("user", "12345", FTP_WORKING_DIRECTORY, perm="elradfmw")

# Instantiate FTP handler class
handler = FTPHandler
handler.authorizer = authorizer

# Define a custom banner (optional)
handler.banner = "Welcome to my FTP server."

# Specify the address and port for the server to listen on
address = ("", 2100)  # Listen on all interfaces

# Create FTP server instance and start serving
server = FTPServer(address, handler)

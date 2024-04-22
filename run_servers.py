from utils.ftp_server import server
from utils.web_server import web_server_thread

# Start WEB server
web_server_thread.start()

# Start FTP server
server.serve_forever()

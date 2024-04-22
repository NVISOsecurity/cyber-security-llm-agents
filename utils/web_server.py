from http import server
import socketserver
import threading
from . import constants
import os
import utils.constants

WORKING_DIRECTORY = utils.constants.LLM_WORKING_FOLDER + "/http_server"


class Handler(server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WORKING_DIRECTORY, **kwargs)


def run_server():
    # Create the directory if it doesn't exist
    if not os.path.exists(WORKING_DIRECTORY):
        os.makedirs(WORKING_DIRECTORY)

    with socketserver.TCPServer(("", constants.WEB_SERVER_PORT), Handler) as httpd:
        print(
            f"Serving HTTP on 0.0.0.0 port {constants.WEB_SERVER_PORT} (http://0.0.0.0:{constants.WEB_SERVER_PORT}/)..."
        )
        httpd.serve_forever()


# Start the server in a new thread
web_server_thread = threading.Thread(target=run_server)
web_server_thread.daemon = (
    True  # This ensures the thread will be killed when the main program exits
)

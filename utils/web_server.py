from http import server
import socketserver
import threading
from . import constants
import os
import cgi
import utils.constants

WORKING_DIRECTORY = utils.constants.LLM_WORKING_FOLDER + "/http_server"


class Handler(server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WORKING_DIRECTORY, **kwargs)

    def do_POST(self):
        if self.path == "/upload":
            # The enctype should be multipart/form-data
            ctype, pdict = cgi.parse_header(self.headers.get("content-type"))
            if ctype == "multipart/form-data":
                # Parse the form data
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={
                        "REQUEST_METHOD": "POST",
                        "CONTENT_TYPE": self.headers["Content-Type"],
                    },
                )
                # Check if the file was uploaded
                if "file" in form:
                    file_item = form["file"]
                    # Check if the file has contents
                    if file_item.file:
                        # Read the file contents
                        file_data = file_item.file.read()
                        file_name = os.path.join(WORKING_DIRECTORY, file_item.filename)
                        # Save the file
                        with open(file_name, "wb") as f:
                            f.write(file_data)
                        # Respond with a success message
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b"File uploaded successfully.")
                    else:
                        # Respond with an error message
                        self.send_error(400, "File is empty.")
                else:
                    # Respond with an error message
                    self.send_error(400, "File not found in the request.")
            else:
                # Respond with an error message
                self.send_error(400, "Unsupported Media Type: {}".format(ctype))
        else:
            # For any other POST request, respond with a 404
            self.send_error(404, "Can only POST to /upload")


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

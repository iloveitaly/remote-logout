#!/usr/bin/env python3

import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import logging

# Set up logging
logger = logging.getLogger("LogoutService")
logger.setLevel(logging.INFO)


def get_whitelist_ips():
    # Fetch and process the whitelist IPs from the environment variable
    whitelist_env = os.getenv("LOGOUT_WHITELIST_IPS", "")
    return [ip.strip() for ip in whitelist_env.split(",")] if whitelist_env else []


class RequestHandler(BaseHTTPRequestHandler):
    whitelist_ips = get_whitelist_ips()

    def do_GET(self):
        client_ip = self.client_address[0]

        # IP Whitelisting
        if self.whitelist_ips and client_ip not in self.whitelist_ips:
            logger.warning(f"Unauthorized access attempt from {client_ip}")
            self.send_response(403)  # Forbidden
            self.end_headers()
            self.wfile.write(b"Access denied.")
            return

        if self.path == "/logout":
            logger.info(f"Request from {client_ip} to /logout")

            # Redirect to /logout-success
            self.send_response(302)
            self.send_header("Location", "/logout-success")
            self.end_headers()
        elif self.path == "/logout-success":
            user_id = (
                subprocess.check_output("id -u assistant", shell=True).decode().strip()
            )
            command = f"launchctl bootout gui/{user_id}"

            logger.info(f"Executing command for user {user_id}: {command}")
            subprocess.run(command, shell=True)

            # Display the success message
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Logout command executed successfully.")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")


def run(server_class=HTTPServer, handler_class=RequestHandler, port=51789):
    # Determine log file path based on argument provided or use default
    log_file_path = (
        sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != "-" else "./logout.log"
    )

    if log_file_path != "-":
        # Set up file logging
        handler = logging.FileHandler(log_file_path, mode="a")
        logger.addHandler(handler)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
    else:
        # Log to stdout
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    ip = "0.0.0.0"  # Bind to all available interfaces
    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    try:
        logger.info(f"Starting http server on {ip}:{port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logger.info("Server stopped.")


if __name__ == "__main__":
    run()

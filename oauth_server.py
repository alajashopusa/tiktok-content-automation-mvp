#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if '/callback' in self.path:
            code = self.path.split('code=')[1].split('&')[0] if 'code=' in self.path else 'None'
            print(f"\n{'='*50}")
            print(f"AUTH CODE: {code}")
            print(f"{'='*50}\n")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
            <h1>Success!</h1>
            <p>Authorization code captured. Check your terminal.</p>
            """)
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

print("Starting OAuth server...")
print("1. Open this URL in your browser:")
print("https://www.tiktok.com/v2/oauth/authorize/?client_key=aw7sa05ggaws7lhg&response_type=code&redirect_uri=http://localhost:8080/callback&scope=product.read,order.read")
print("\n2. Authorize the app")
print("3. Come back here - the code will appear above")
print("\nServer running on http://localhost:8080")

server = HTTPServer(('localhost', 8080), OAuthHandler)
server.serve_forever()
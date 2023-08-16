# (based on: https://youtu.be/dgvLegLW6ek)

import cgi
import json
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler


class Guitar():
    def __init__(self, gId, mfr, mdl, gtype, puc, color):
        self.gId = gId  # this auto-increments db-side
        self.mfr = mfr  # manufacturer
        self.mdl = mdl  # model
        self.gtype = gtype  # guitar type i.e. 'acoustic'
        self.puc = puc  # pickup configuration: 'HH'
        self.color = color # i.e. '3 color fireburst'




class GittyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        #if self.path == '/':
        #    print("MY SERVER: The GET request is for the root URL.")
        #    self.path = 'my_webpage.html'
        #return self.do_GET()

        if self.path.endswith("/all"):
            print('all')
            self.send_response(200)
            self.send_header('content_type', 'application/json')
            self.end_headers()
            conn = sqlite3.connect('gitty.db')
            cursor = conn.cursor()
            query = "SELECT * FROM guitars"
            print(query)
            result = cursor.execute(query)
            rows = result.fetchall()
            items = []
            for row in rows:
                lr = list(row)
                gitty = Guitar(*lr)
                items.append({"gId": gitty.gId, "mfr": gitty.mfr,
                              "mdl": gitty.mdl, "gtype": gitty.gtype,
                              "puc": gitty.puc, "color": gitty.color})
            for item in items:
                print(item)
                self.wfile.write(json.dumps(item).encode())
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
            self.wfile.write(bytes("<form method = 'POST' action='all'>", "utf-8"))
            self.wfile.write(bytes("<label for='fname''>First name:</label><br>", "utf-8"))
            self.wfile.write(bytes("<input type='text' id='fname' name='fname' placeholder='Enter your name'><br>", "utf-8"))
            self.wfile.write(bytes("<label for='age'>Last name:</label><br>", "utf-8"))
            self.wfile.write(bytes("<input type='text' id='age' name='age' placeholder='Enter your age here'><br><br>", "utf-8"))
            self.wfile.write(bytes("<input type='submit' value='Submit''>", "utf-8"))
            self.wfile.write(bytes("</form>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))


    def do_POST(self):
        if self.path.endswith("/add_new"):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'application/json':
                payload = json.loads(self.rfile.read(content_len))
                gitty = Guitar(*payload.values())
                try:
                    conn = sqlite3.connect('gitty.db')
                    cursor = conn.cursor()    
                    query = "INSERT INTO guitars (mfr, mdl, gtype, puc, color) VALUES (?, ?, ?, ?, ?)"
                    cursor.execute(query, (gitty.mfr, gitty.mdl, gitty.gtype,     
                                       gitty.puc, gitty.color))
                    conn.commit()
                    self.send_response(201)
                    self.send_header('content-type', 'application/json')
                    self.send_header('Location', '/add_new')
                    self.end_headers()
                except sqlite3.Error as er:
                    print("SQLite Error: {}".format(er))
                    self.send_response(500)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("Your G string broke...".encode())




def main():
    PORT = 8080
    server = HTTPServer(('127.0.0.1', PORT), GittyHandler)
    print('SERVER RUNNING ON PORT:{}'.format(PORT))
    server.serve_forever()

if __name__ == "__main__":
    main()
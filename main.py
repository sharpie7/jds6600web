from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import time
import json
import sys
import os
# Hack to keep the jds6600 library in its original directory
sys.path.append(os.path.join(os.path.dirname(__file__),"jds6600_python-master"))
from jds6600 import jds6600

defaultHostName = "localhost"
defaultServerPort = 8080
defaultSerialPort = "COM10"

class MyJds6600(jds6600):
    def __del__(self):
        if self.ser:
            self.ser.close()
            
            
class MyServer(SimpleHTTPRequestHandler):

    def mySendResponse(self, code, mime, data):
        self.send_response(code)
        self.send_header("Content-type", mime)
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsedPath = urlparse(self.path)
        queryParams = parse_qs(parsedPath.query)
        if parsedPath.path == "/control":
            try:
                j = MyJds6600(serialPort)
            except:
                self.mySendResponse(503,"text/plain","503: Unable to open serial connection to {}.".format(serialPort).encode('utf-8'))
                return
            if "mode" in queryParams:
                j.setmode(queryParams["mode"][0])
            if "chan" in queryParams:
                ch = int(queryParams["chan"][0])
            else:
                ch = 1
            if "wave" in queryParams:
                j.setwaveform(ch,queryParams["wave"][0])
            if "freq" in queryParams:
                if "freqm" in queryParams:
                    j.setfrequency(ch,float(queryParams["freq"][0]),int(queryParams["freqm"][0]))
                else:
                    j.setfrequency(ch,float(queryParams["freq"][0]))
            if "ampl" in queryParams:
                j.setamplitude(ch,float(queryParams["ampl"][0]))
            if "offs" in queryParams:
                j.setoffset(ch,float(queryParams["offs"][0]))
            if "duty" in queryParams:
                j.setdutycycle(ch,int(queryParams["duty"][0]))
            wave = j.getwaveform(1)[1]
            (freq, freqm) = j.getfrequency_m(1)
            ampl = j.getamplitude(1)
            offs = j.getoffset(1)
            duty = j.getdutycycle(1)
            del j
            data = dict(zip(('wave','freq','freqm', 'ampl','offs','duty'),(wave, freq, freqm, ampl, offs, duty)))
#           print(data)
            json_data = json.dumps(data).encode('utf-8')
            self.mySendResponse(200, "application/json", json_data)
        elif parsedPath.path == "/" or parsedPath.path == "/favicon.ico" :
            super().do_GET()
        else:
            ftext="403: forbidden".encode('utf-8')
            self.mySendResponse(403, "text/plain", ftext)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        hostName = sys.argv[1]
    else:
        hostName = defaultHostName
    if len(sys.argv) >= 3:
        serverPort = int(sys.argv[2])
    else:
        serverPort = defaultServerPort
    if len(sys.argv) >=4:
        serialPort = sys.argv[3]
    else:
        serialPort = defaultSerialPort
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    
    webServer.serve_forever()


    webServer.server_close()
    print("Server stopped.")
# Copyright (C)
# 2021-01-30
#  Reinhold Autengruber, OE5RNL
#  Manfred Autengruber,  OE5NVL
#
#
#  Flask app for NPR
#
#  V0.1b 2021-02-05
#
#
import os
import os.path
import platform
from flask import Flask
from npr_control import Npr #, version
import time

#tty = "/dev/ttydummy"
tty = "/dev/ttyACM0"

app = Flask(__name__)

npr = Npr(tty)

# npr commands

@app.route("/npr_version")
def version():
    return "<pre>"+npr.version()+"</pre>"

@app.route("/npr_who")
def who():
  return "<pre>"+npr.who()+"</pre>"

@app.route("/npr_status")
def status():
  return "<pre>"+npr.status()+"</pre>"

@app.route("/npr_display_config")
def display_config():
  return "<pre>"+npr.display_config()+"</pre>"

@app.route("/")
def Index():
    return "<h1>OE5XBR NPR-Info</h1>"

# usb switch commands

@app.route("/npr_usb_status")
def npr_status():
  p = os.popen("/usr/local/bin/npr-status")
  out = p.read()
  p.close()
  return out

@app.route("/npr_usb_on")
def npr_on():
  p = os.popen("/usr/local/bin/npr-on")
  out = p.read()
  p.close()
  return out

@app.route("/npr_usb_off")
def npr_off():
  p = os.popen("/usr/local/bin/npr-off")
  out = p.read()
  p.close()
  return out


@app.route("/node")
def node():
  return platform.node()

@app.route("/cmd")
def cmd():
  s =  "npr_version<br>"
  s += "npr_display_config<br>"
  s += "npr_status<br>"
  s += "npr_who<br>"
  s += "npr_usb_status<br>"
  s += "npr_usb_on<br>"
  s += "npr_usb_off<br>"

  return s

if __name__ == "__name__":
  app.run(host="0.0.0.0")


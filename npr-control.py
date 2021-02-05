Copyright (C)
# 2021-01-30 
#  Reinhold Autengruber, OE5RNL
#  Manfred Autengruber,  OE5NVL
#
# A very simple Python control interface for New Packet radio (NPR).
# 
# V0.1b 2021-01-30
# - more testing needed
# - ugly time.sleep
# V0.1c 2021-02-05
# - like above
# - ser open changed

import serial
import time
import os

# sudo interceptty /dev/ttyACM0 /dev/ttydummy

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
      return False
    for x in a:
      if not x.isdigit():
          return False
      i = int(x)
      if i < 0 or i > 255:
        return False
    return True

def validate_qrg(qrg):
  a = qrg.split('.')
  if len(a) != 2:
    return False
  if ((a[0][0] != "4") or (a[0][1] != "3")):
    return False
  for x in a:
    if not x.isdigit():
      return False
  return True


class Npr():

  connected = False
  _com =""
  retErrComText = "npr: com not available! USB Power down ?"

  def __init__(self, com):
    self._com = com
    print(self._com)

    
  def ser_open(self):
    #print("COM: "+self._com)
    if os.path.exists(self._com):
      self.ser = serial.Serial(self._com)
      self.ser.close()
      self.ser.port = self._com; 
      self.ser.baudrate = 921600 
      self.ser.open()
      #print("ser filno "+str(self.ser.fileno()))
      self.connected = True
    else:
      print("ser seropen false")
      self.connected = False
    return self.connected


  def ser_close():
     self.close()


  def isConnected():
    self.connected = False
    if os.path.exists(com):
      if self.ser.fileno():
        self.connected = True
    return self.connected


  def sendCommand(self,cmd):    
    for element in cmd:
      self.ser.write(element.encode("utf-8"))
      time.sleep(0.01)
    self.ser.write(chr(13).encode("utf-8"))
    
  def getResponse(self):
    s =''
    time.sleep(0.1)
    while self.ser.inWaiting() > 0:
       s += self.ser.read(1).decode("utf-8")  
       #time.sleep(0.01)
    self.ser.close()
    return s



  def version(self):
    if self.ser_open():
      self.sendCommand("version")
      time.sleep(0.5)
      return self.getResponse()
    return self.retErrComText

  def radio(self,on_off):
    if self.ser_open():
      if on_off=="on":
        self.sendCommand("radio on")
      if on_off=="off":
        self.sendCommand("radio off")
      time.sleep(1)
      return self.getResponse()
    return self.retErrComText

  def status(self):
    if self.ser_open():
      self.sendCommand("status")
      time.sleep(0.5)
      self.ser.write(chr(3).encode("utf-8"))
      r = self.getResponse()
      return r
    return self.retErrComText

  def who(self):
    if self.ser_open():
      self.sendCommand("who")
      time.sleep(0.5)
      self.ser.write(chr(3).encode("utf-8"))
      return self.getResponse()
    return self.retErrComText

  def display_config(self):
    if self.ser_open():
      self.sendCommand("display config")
      time.sleep(0)
      return self.getResponse()
    return self.retErrComText

  def display_DHCP_ARP(self):
    if self.ser_open():
      self.sendCommand("display DHCP_ARP")
      time.sleep(0.5)
      return self.getResponse()
    return self.retErrComText

  def TX_test(self,t):
    if self.ser_open():
      self.sendCommand("TX_test "+str(t))
      time.sleep(int(t))
      return self.getResponse()
    return self.retErrComText

  def set_callsign(self,call):
    if self.ser_open():
      self.sendCommand("set callsign "+call)
      time.sleep(0.5)
      return self.getResponse()
    return self.retErrComText
  
  # testen
  def set_is_master(self,yn):
    if self.ser_open():
      if ((yn=="yes") or (yn=="no")):
        self.sendCommand("set is_master "+ yn)
        time.sleep(0.5)
        return self.getResponse()
      else:
        return "ERROR: set is_master: "+yn
      return self.retErrComText

  # offen
  def set_master_FDD(self,m):
    if self.ser_open():
      return "not defined"
    return self.retErrComText

  # TESTEN !!!
  def set_Eth_mode(self,v):
    if self.ser_open():
      if ((v>=0) and (v<=7)):
        self.sendCommand("set Eth_mode" + str(v))
        return self.getResponse()
      else:
        return "Error set_Eth_mode: "+str(v)
    return self.retErrComText

  def set_modem_IP(self, ip):
    if self.ser_open():
      if validate_ip(ip):
        self.sendCommand("set modem_IP "+ ip)
        time.sleep(0.5)
        self.getResponse()
      else:
        return "ERROR ip Adress: "+ ip
    return self.retErrComText

  def set_netmask(self,mask):
    if self.ser_open():
      if validate_ip(mask):
        self.sendCommand("set netmask "+ mask)
        time.sleep(0.5)
        self.getResponse()
      else:
        return "ERROR Netmask: "+ mask
    return self.retErrComText

  def set_telnet_active(self,yn):
    if self.ser_open():
      if ((yn=="yes") or (yn=="no")):
        self.sendCommand("set telnet_active "+yn)
        time.sleep(0.5)
        return self.getResponse()
      else:
        return "ERROR set_telnet_active "+yn
    return self.retErrComText

  def set_DNS_acitive(self,yn):
    if self.ser_open():
      if ((yn=="yes") or (yn=="no")):
        self.sendCommand("set DNS_active "+ yn)
        time.sleep(1)
        return self.getResponse()
      else:
        return "ERROR: set DNS_active: "+yn
    return self.retErrComText

  def set_DNS_value(self, ip):
    if self.ser_open():
      if validate_ip(ip):
        self.sendCommand("set DNS_value "+ ip)
        time.sleep(0.5)
        self.getResponse()
      else:
        return "ERROR ip Adress: "+ ip
    return self.retErrComText

  def set_def_route_active(self, yn):
    if self.ser_open():
      if ((yn=="yes") or (yn=="no")):
        self.sendCommand("set def_route_active "+ yn)
        time.sleep(1)
        return self.getResponse()
      else:
        return "ERROR: yn: "+yn
    return self.retErrComText

  def set_def_route_val(self,ip):
    if self.ser_open():
      if validate_ip(ip):
        self.sendCommand("set def_route_val "+ ip)
        time.sleep(0.5)
        self.getResponse()
      else:
        return "ERROR ip Adress: "+ ip
    return self.retErrComText

  def set_IP_begin(self, ip):
    if self.ser_open():
      if validate_ip(ip):
        self.sendCommand("set IP_begin "+ ip)
        time.sleep(0.5)
        self.getResponse()
      else:
        return "ERROR ip Adress: "+ ip
    return self.retErrComText

  def set_master_IP_size(self,num):
    if self.ser_open():
      if ((num>0) and (num<=32)):
        self.sendCommand("set master_IP_size "+ str(num))
        time.sleep(0.5)
      else:
        return "ERROR ip num: " + str(num)
    return self.retErrComText

  def set_client_req_size(self,num):
    if self.ser_open():
      if ((num>0) and (num<=5)):
        self.sendCommand("set client_req_size "+ str(num))
        time.sleep(0.5)
      else:
        return "ERROR set_client_req_size num: " + str(num)
    return self.retErrComText

  def set_master_IP_down(self, ip):
    if self.ser_open():
      if validate_ip(ip):
        self.sendCommand("set master_IP_down "+ ip)
        time.sleep(0.5)
        self.getResponse()
      else:
        return "ERROR ip Adress: "+ ip
    return self.retErrComText

  def set_DHCP_active(self, yn):
    if self.ser_open():
      if ((yn=="yes") or (yn=="no")):
        self.sendCommand("set DHCP_active "+ yn)
        time.sleep(1)
        return self.getResponse()
      else:
        return "ERROR: set_DHCP_active: "+yn
    return self.retErrComText

  def set_radio_on_at_start(self, yn):
    if self.ser_open():
      if ((yn=="yes") or (yn=="no")):
        self.sendCommand("set radio_on_at_start "+ yn)
        time.sleep(1)
        return self.getResponse()
      else:
        return "ERROR: set_radio_on_at_start: "+yn
    return self.retErrComText

  def set_frequency(self, qrg):
    if self.ser_open():
      if validate_qrg(qrg):
        self.sendCommand("set frequency "+ qrg)
        time.sleep(3.0)
        return self.getResponse()
      else:
        return "ERROR set frequency: "+ qrg
    return self.retErrComText

  def set_RF_power(self, p):
    if self.ser_open():
      if ((p>=0) and (p<=127)):
        self.sendCommand("set RF_power "+ str(p))
        time.sleep(1)
        return self.getResponse()
      else:
        return "ERROR: set_RF_power: "+str(p)
    return self.retErrComText

  def set_modulation(self, m):
    if self.ser_open():
      ml = ["11","12","13","14","20","21","22","23","24"]
      if (m in ml):
        self.sendCommand("set modulation "+ m)
        time.sleep(2)
        return self.getResponse()
      else:
        return "ERROR: set_modulation: " + m
    return self.retErrComText

  def set_radio_netw_id(self,v):
    if self.ser_open():
      r =""
      if ((v>=0) and (v<=15)):
        self.sendCommand("set radio_netw_ID "+ str(v))
        time.sleep(2)
        r = self.getResponse()
        time.sleep(2)
        return r + self.getResponse() 
      else:
        return "ERROR: set_radio_netw_id: "+str(v)
    return self.retErrComText

  def save(self):
    if self.ser_open():
      self.sendCommand("save")
      time.sleep(1)
      return self.getResponse() 
    return self.retErrComText

  def reboot(self):
    if self.ser_open():
      self.sendCommand("reboot")
    return self.retErrComText

  def reset_to_default(self):
    if self.ser_open():
      self.sendCommand("reset_to_default")
      time.sleep(2)
      return 
    return self.retErrComText


  def exit(sef):
    if self.ser_open():
      pass
    return self.retErrComText


def main():

  npr = Npr("/dev/ttyACM0")
  #npr = Npr("/dev/ttydummy")

  #print(npr.version())
  #print(npr.radio("off"))
  #print(npr.status())
  #print(npr.who())
  #print(npr.display_config())
  #print(npr.display_DHCP_ARP())
  #print(npr.TX_test(5))
  #print(npr.set_callsign("OE5RNL"))
  #print(npr.set_is_master("no"))
  #print(npr.set_master_FDD(m))
  #print(npr.set_Eth_mode(5))
  #print(npr.set_modem_IP("192.168.8.54"))
  #print(npr.set_netmask("255.255.255.0"))
  #print(npr.set_telnet_active("yes"))
  #print(npr.set_DNS_acitive("yes"))
  #print(npr.set_DNS_value("44.143.97.254"))
  #print(npr.set_def_route_active("yes"))
  #print(npr.set_def_route_val("192.168.8.254"))
  #print(npr.set_IP_begin("192.168.8.90"))
  #print(npr.set_master_IP_size(6))
  #print(npr.set_client_req_size(5))
  #print(npr.set_master_IP_down("192.168.8.252"))
  #print(npr.set_DHCP_active("yes"))
  #print(npr.set_radio_on_at_start("no"))
  #print(npr.set_frequency("435.500"))
  #print(npr.set_RF_power(127))
  #print(npr.set_modulation("24"))
  #print(npr.set_radio_netw_id(0))
  #print(npr.save())

  #print(npr.reset_to_default())

  #print(npr.display_config())

if __name__ == "__main__":
  # execute only if run as a script
  main()


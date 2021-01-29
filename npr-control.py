import serial
import time

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

  def init(self,com):
    print(com)
    self.ser = serial.Serial(com)
    self.ser.close()
    self.ser.port = com; 
    self.ser.baudrate = 921600 
    self.ser.open()


  def sendCommand(self,cmd):    
    for element in cmd:
      self.ser.write(element.encode("utf-8"))
      time.sleep(0.05)
    self.ser.write(chr(13).encode("utf-8"))
    
  def getResponse(self):
    s =''
    #print (self.ser.inWaiting())
    while self.ser.inWaiting() > 0:
       #print(s)
       s += self.ser.read(1).decode("utf-8")  
       #time.sleep(0.01)
    return s

  def version(self):
    self.sendCommand("version")
    time.sleep(0.5)
    return self.getResponse()

  def radio(self,on_off):
    if on_off=="on":
      self.sendCommand("radio on")
    if on_off=="off":
      self.sendCommand("radio off")
    time.sleep(1)
    return self.getResponse()

  def status(self):
    self.sendCommand("status")
    time.sleep(0.5)
    self.ser.write(chr(3).encode("utf-8"))
    r = self.getResponse()
    return r

  def who(self):
    self.sendCommand("who")
    time.sleep(0.5)
    self.ser.write(chr(3).encode("utf-8"))
    return self.getResponse()

  def display_config(self):
    self.sendCommand("display config")
    time.sleep(0.3)
    return self.getResponse()


  def display_DHCP_ARP(self):
    self.sendCommand("display DHCP_ARP")
    time.sleep(0.5)
    return self.getResponse()

  def TX_test(self,t):
    self.sendCommand("TX_test "+str(t))
    time.sleep(int(t))
    return self.getResponse()
    pass

  def set_callsign(self,call):
    self.sendCommand("set callsign "+call)
    time.sleep(0.5)
    return self.getResponse()
  
  # testen
  def set_is_master(self,yn):
    if ((yn=="yes") or (yn=="no")):
      self.sendCommand("set is_master "+ yn)
      time.sleep(0.5)
      return self.getResponse()
    else:
      return "ERROR: set is_master: "+yn


  # offen
  def set_master_FDD(self,m):
    pass

  # TESTEN !!!
  def set_Eth_mode(self,v):
    if ((v>=0) and (v<=7)):
      self.sendCommand("set Eth_mode" + str(v))
      return self.getResponse()
    else:
      return "Error set_Eth_mode: "+str(v)

  def set_modem_IP(self, ip):
    if validate_ip(ip):
      self.sendCommand("set modem_IP "+ ip)
      time.sleep(0.5)
      self.getResponse()
    else:
      return "ERROR ip Adress: "+ ip

  def set_netmask(self,mask):
    if validate_ip(mask):
      self.sendCommand("set netmask "+ mask)
      time.sleep(0.5)
      self.getResponse()
    else:
      return "ERROR Netmask: "+ mask

  def set_telnet_active(self,yn):
    if ((yn=="yes") or (yn=="no")):
      self.sendCommand("set telnet_active "+yn)
      time.sleep(0.5)
      return self.getResponse()
    else:
      return "ERROR set_telnet_active "+yn

  def set_DNS_acitive(self,yn):
    if ((yn=="yes") or (yn=="no")):
      self.sendCommand("set DNS_active "+ yn)
      time.sleep(1)
      return self.getResponse()
    else:
      return "ERROR: set DNS_acitive: "+yn

  def set_DNS_value(self, ip):
    if validate_ip(ip):
      self.sendCommand("set DNS_value "+ ip)
      time.sleep(0.5)
      self.getResponse()
    else:
      return "ERROR ip Adress: "+ ip

  def set_def_route_active(self, yn):
    if ((yn=="yes") or (yn=="no")):
      self.sendCommand("set def_route_active "+ yn)
      time.sleep(1)
      return self.getResponse()
    else:
      return "ERROR: yn: "+yn

  def set_def_route_val(self,ip):
    if validate_ip(ip):
      self.sendCommand("set def_route_val "+ ip)
      time.sleep(0.5)
      self.getResponse()
    else:
      return "ERROR ip Adress: "+ ip

  def set_IP_begin(self, ip):
    if validate_ip(ip):
      self.sendCommand("set IP_begin "+ ip)
      time.sleep(0.5)
      self.getResponse()
    else:
      return "ERROR ip Adress: "+ ip

  # 32  ???
  def set_master_IP_size(self,num):
    if ((num>0) and (num<=32)):
      self.sendCommand("set master_IP_size "+ str(num))
      time.sleep(0.5)
    else:
      return "ERROR ip num: " + str(num)

  # 5 ????
  def set_client_req_size(self,num):
    if ((num>0) and (num<=5)):
      self.sendCommand("set client_req_size "+ str(num))
      time.sleep(0.5)
    else:
      return "ERROR set_client_req_size num: " + str(num)


  # testen
  def set_master_IP_down(self, ip):
    if validate_ip(ip):
      self.sendCommand("set master_IP_down "+ ip)
      time.sleep(0.5)
      self.getResponse()
    else:
      return "ERROR ip Adress: "+ ip


  def set_DHCP_active(self, yn):
    if ((yn=="yes") or (yn=="no")):
      self.sendCommand("set DHCP_active "+ yn)
      time.sleep(1)
      return self.getResponse()
    else:
      return "ERROR: set_DHCP_active: "+yn

  def set_radio_on_at_start(self, yn):
    if ((yn=="yes") or (yn=="no")):
      self.sendCommand("set radio_on_at_start "+ yn)
      time.sleep(1)
      return self.getResponse()
    else:
      return "ERROR: set_radio_on_at_start: "+yn

  def set_frequency(self, qrg):
    if validate_qrg(qrg):
      self.sendCommand("set frequency "+ qrg)
      time.sleep(3.0)
      return self.getResponse()
    else:
      return "ERROR set frequency: "+ qrg

  def set_RF_power(self, p):
    if ((p>=0) and (p<=127)):
      self.sendCommand("set RF_power "+ str(p))
      time.sleep(1)
      return self.getResponse()
    else:
      return "ERROR: set_RF_power: "+str(p)

  def set_modulation(self, m):
    ml = ["11","12","13","14","20","21","22","23","24"]
    if (m in ml):
      self.sendCommand("set modulation "+ m)
      time.sleep(2)
      return self.getResponse()
    else:
      return "ERROR: set_modulation: " + m

  def set_radio_netw_id(self,v):
    r =""
    if ((v>=0) and (v<=15)):
      self.sendCommand("set radio_netw_ID "+ str(v))
      time.sleep(2)
      r = self.getResponse()
      time.sleep(2)
      return r + self.getResponse() 
    else:
      return "ERROR: set_radio_netw_id: "+str(v)


  # testen
  def save(self):
    self.sendCommand("save")
    time.sleep(1)
    return self.getResponse() 

  #testen
  def reboot(self):
    self.sendCommand("reboot")

  #testen
  def reset_to_default(self):
    self.sendCommand("reset_to_default")
    time.sleep(2)
    return 


  def exit(sef):
    pass


def main():

  npr = Npr()
  npr.init("/dev/ttydummy")
  #npr.init("/dev/ttyACM0")

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
  print(npr.save())

  #print(npr.reset_to_default())

  print(npr.display_config())

if __name__ == "__main__":
  # execute only if run as a script
  main()


# ser = serial.Serial()
# #ser.close()
# ser.port = "/dev/ttyACM0"
# #ser.port = "/dev/ttydummy"
# ser.baudrate = 921600 
# ser.open()
# print(ser)


# def _delay():
#   time.sleep(0.01)


# def sendCommand(cmd):

#   for element in cmd:
#     #print(element, end='') 
#     #print(element.encode("utf-8"))
#     ser.write(element.encode("utf-8"))
#     _delay()

#   ser.write(chr(13).encode("utf-8"))
#   #print("\n") 
  
 
# sendCommand("set modulation 11") 
# time.sleep(10)
# sendCommand("display config") 
# #sendCommand("status") 
# #ser.write(chr(3).encode("utf-8"))


# time.sleep(0.5)

# s =''
# while ser.inWaiting() > 0:
#    s += ser.read(1).decode("utf-8")

# print("|"+s+"|")



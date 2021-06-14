# import pyserial
import sys
import glob
import serial
import time

def showAviableSerialPorts():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            # print(s.baudrate)
            # result.append(port)
            # result.append(s.baudrate)
            result.append({"name":port,"speed":s.baudrate})

        except (OSError, serial.SerialException):
            pass
    return result

def connectAndSend(name,baundRate,text):
    s = serial.Serial(name,baundRate)
    s.write(str.encode(text))
        # if(s.read_all().decode().strip()!="\n"):
            # print(s.read_all().decode())
    tdata = s.read()
    time.sleep(1)  
    data_left = s.inWaiting()  
    tdata += s.read(data_left)
    print(tdata,"<-here")
    # print(s.readall())

def repeatCommand(name,baundRate,text,waitTime,reapeatTime,step):
    for n in range(reapeatTime,0,-1):
        timeInSeconds = waitTime*60
        connectAndSend(name,baundRate,text)
        for m in range(timeInSeconds, 0, -step):
            if(step>m):
                print("Remaining time: ", int(m/60),"minutes",m-(int(m/60)*60),"seconds")
                print("remeining time is smaller step size: ",step," waitTime: ",m)
                time.sleep(m)
            else:
                print("Remaining time: ", int(m/60),"minutes",m-(int(m/60)*60),"seconds")
                time.sleep(step)

def main():
    print("Essa")
    print(showAviableSerialPorts())
    _port = input("Specify destination port ")
    _baundrate = input("Specify port baundrate ")
    _cmd = input("Put command to use ")
    print(_port,_baundrate,_cmd)
    # connectAndSend("COM14",_baundrate,"essa")
    repeatCommand("COM14",_baundrate,"essa",3,5,65)

if __name__ == "__main__":
    main()
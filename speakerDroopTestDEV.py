
#Eliseo Izazaga
# the purpose of this test is to drive the speaker and IRLEDS
# while recording GG voltage and current, and the same through 
# and agilent scope
# primary interface is UART and GPIB. 

#header should look like

#Time,GGvolt,GGcurrent,Vsysmin, Vsysavg, IspkrmaX, IspkrAVG, Delay

#IRLEDS Date,IRLEDS Time,IRLEDS GGvolt,IRLEDS GGcurrent,IRLEDS Vsysmin,IRLEDS  Vsysavg,IRLEDS  IspkrmaX,IRLEDS  IspkrAVG,IRLEDS Delay

#IRLEDS SOUND 6 Date,IRLEDS SOUND 6 Time,IRLEDS SOUND 6 GGvolt,IRLEDS SOUND 6 GGcurrent,IRLEDS SOUND 6 Vsysmin,IRLEDS SOUND 6  Vsysavg,IRLEDS SOUND 6  IspkrmaX,IRLEDS SOUND 6 IspkrAVG,IRLEDS SOUND 6 Delay

#IRLEDS SOUND 1 Date,IRLEDS SOUND 1 Time,IRLEDS SOUND 1 GGvolt,IRLEDS SOUND 1 GGcurrent,IRLEDS SOUND 1 Vsysmin,IRLEDS SOUND 1  Vsysavg,IRLEDS SOUND 1  IspkrmaX,IRLEDS SOUND 1 IspkrAVG,IRLEDS SOUND 1 Delay

######################Application#####################

#configure scope, 
# 
# print header to log
# 
# configure UART. 
# 
# make function that records and returns GG information, returns voltage and current DONE
# make ISP login, no return DONE
# make function that will send command to ISP, no return DONE

# make function that will returns vsys min and avg from scope, returns vsysMin, VsysAvg DONE
# make function that will returns ISPKr max and avg from scope, returns ISPKR nax, ISPKR avg. DONE


# make function that will configure scope capture time and set to trigger on spkrAmp current, input in seconds. DONE
# 
#  
 
import pyvisa
import serial
import time
import datetime
import re

ispLoginName = '_Y&?"])4~2pxGk4cBtC-o'
ispLoginPassword = '%zeW(96eE-3)y~n["J-3pz9_2Bf`Q:&+]J!@it?'
rm = ""
dsoScope = ""
UARTcmdDelay = 1
scopeDelay = 11
EFRport = r'COM17'
OVport = r'COM16'
header1 = "Time,GGvolt,GGcurrent,Vsysmin, Vsysavg, IspkrmaX, IspkrAVG, \n"
header2 = "IRLEDS Time,IRLEDS GGvolt,IRLEDS GGcurrent,IRLEDS Vsysmin,IRLEDS Vsysavg,IRLEDS IspkrmaX,IRLEDS IspkrAVG,\n"
header3 = "IRLEDS SIREN Time,IRLEDS SIREN GGvolt,IRLEDS SIREN GGcurrent,IRLEDS SIREN Vsysmin,IRLEDS SIREN Vsysavg,IRLEDS SIREN IspkrmaX,IRLEDS SIREN IspkrAVG, \n"
header4 = "IRLEDS HARVARD Time,IRLEDS HARVARD GGvolt,IRLEDS HARVARD GGcurrent,IRLEDS HARVARD Vsysmin,IRLEDS HARVARD Vsysavg,IRLEDS HARVARD IspkrmaX,IRLEDS HARVARD IspkrAVG \n"
VsysMinGlobal = 5
VsysAvgGlobal = 5

EFR = serial.Serial(port=EFRport, baudrate=9600, parity="N", stopbits=1, bytesize=8, timeout=None)
OV = serial.Serial(port=OVport, baudrate=115200, parity="N", stopbits=1, bytesize=8, timeout=None)

#EFR.setRTS(True)

LOG1 = r'C:\Users\TESTER\Desktop\DSO AQUILA SPEAKERDROOP\TestLogs\LOG1.txt'
LOG2 = r'C:\Users\TESTER\Desktop\DSO AQUILA SPEAKERDROOP\TestLogs\LOG2.txt'
LOG3 = r'C:\Users\TESTER\Desktop\DSO AQUILA SPEAKERDROOP\TestLogs\LOG3.txt'
LOG4 = r'C:\Users\TESTER\Desktop\DSO AQUILA SPEAKERDROOP\TestLogs\LOG4.txt'

def getGGinfo():
    EFR.reset_input_buffer()
    EFR.reset_output_buffer()
    #time.sleep(UARTcmdDelay)
    #voltageByteCommand = bytes(':bq27z561:voltage;'.encode('ascii'))
    #EFR.reset_input_buffer()
    #EFR.write(bytes(':bq27z561'.encode('ascii')))
    #EFR.write(bytes(':voltage'.encode('ascii')))
    #print(EFR.read_all())
    EFR.write(b'b')
    EFR.write(b'q')
    EFR.write(b'2')
    EFR.write(b'7')
    EFR.write(b'z')
    EFR.write(b'5')
    EFR.write(b'6')
    EFR.write(b'1')
    EFR.write(b':')
    EFR.write(b'v')
    EFR.write(b'o')
    EFR.write(b'l')
    EFR.write(b't')
    EFR.write(b'a')
    EFR.write(b'g')
    EFR.write(b'e')
    EFR.write(b';')
    #EFR.write(bytes(';'.encode('ascii')))
    #EFR.write(bytes(';'.encode('ascii')))
    time.sleep(UARTcmdDelay)
    #time.sleep(1)
    voltage = EFR.read_all()
    voltage = str(voltage)

    print("Length of voltage: " + str(len(voltage)))

    print("GG volt function reading: "+voltage+"\n")
    if(len(voltage) >= 31  and 'ERR' not in voltage):
        voltage = re.search("\s\d\d\d\d", voltage).group(0)
    else:
        voltage = " GGERROR"
    voltage = str(voltage)
    voltage = voltage.split(" ")
    voltage = str(voltage[1])
    #print("GG volt read: "+voltage)
    EFR.reset_input_buffer()
    EFR.reset_output_buffer()

    #time.sleep(UARTcmdDelay)
    #currentByteCommand = bytes(':bq27z561:current;'.encode('ascii'))
    #print(EFR.read_all())
    EFR.reset_input_buffer()
    #EFR.write(currentByteCommand)
    EFR.write(b'b')
    EFR.write(b'q')
    EFR.write(b'2')
    EFR.write(b'7')
    EFR.write(b'z')
    EFR.write(b'5')
    EFR.write(b'6')
    EFR.write(b'1')
    EFR.write(b':')
    EFR.write(b'c')
    EFR.write(b'u')
    EFR.write(b'r')
    EFR.write(b'r')
    EFR.write(b'e')
    EFR.write(b'n')
    EFR.write(b't')
    EFR.write(b';')
    time.sleep(UARTcmdDelay)
    #time.sleep(1)
    current = EFR.read_all()
    current = str(current)

    print("Length of current: " + str(len(current)))
    print("GG curr function reading: "+current+"\n")
    print(current)
    if(len(current) >= 28 and 'ERR' not in current):
        current = re.search("\s-\d+|\s\d+", current).group(0)
    else:
        current = " GGERROR"

    current = str(current)
    current = current.split(" ")
    current = str(current[1])
    #print("GG volt read: "+voltage)
    #print(current)
    EFR.reset_input_buffer()
    EFR.reset_output_buffer()
    return voltage, current

def sendISP(inCommand):
    command = inCommand.encode('utf-8')
    OV.write(bytes(command))
    time.sleep(UARTcmdDelay)
    print(OV.read_all())
    OV.reset_input_buffer()
    OV.reset_output_buffer()
    

def loginISP():
    print("Logging into ISP: ")
    sendEFR("isp:power:on;")
    sendISP("\r")
    sendISP("\r")
    sendISP("\r")
    sendISP("\r")

    sendISP(ispLoginName)
    sendISP("\r")
    time.sleep(3)
    sendISP(ispLoginPassword)
    sendISP("\r")
    sendISP("\r")
    time.sleep(3)
    print("ISP Log in done: ")


def sendEFR(inCommand):
    EFR.reset_input_buffer()
    EFR.reset_output_buffer()
    command = inCommand.encode('utf-8')
    print("Command Sent to EFR; " + str(command))
    EFR.write(bytes(command))
    time.sleep(UARTcmdDelay)
    print(EFR.read_all())
    EFR.reset_input_buffer()
    EFR.reset_output_buffer()


def initScope():
    dsoScope.write(":TIMebase:SCALe 1000 MS")
    time.sleep(1)
    dsoScope.write("TIMebase:POSition 0 US")
    time.sleep(1)
    dsoScope.write("CHANnel1:Display 1")
    time.sleep(1)
    dsoScope.write("CHANnel2:Display 1")
    time.sleep(1)
    dsoScope.write("CHANnel1:SCAle 2.0")
    time.sleep(1)
    dsoScope.write("CHANnel2:SCAle 1.0")
    time.sleep(1)
    dsoScope.write("CHANnel2:OFFSet 3.0")

def setScopeTime(seconds):
    #seconds = seconds / 10
    sendScope = ":TIMebase:SCALe "+str(seconds) + " MS"
    dsoScope.write(sendScope)


def playConstantSound():
    while True: 
     sendEFR(":isp:audio:playsound:6:100;")   


def triggerScope():
    #dsoScope.write("TRIGger:EDGE:SOURce 2")
    #dsoScope.write("TRIGger:EDGE:LEVel NONE, CHANNEL2")
    #dsoScope.write("TRIGger:SWEep AUTO")
    #dsoScope.write("TRIGger:EDGE:SOURce 2")
    dsoScope.write(":RUN")
    #dsoScope.write(":SINGle")
    #dsoScope.write(":SINGle")
    #time.sleep(2)
    print(dsoScope.query(r'*OPC?'))

def measureScope():
    VsysMin = dsoScope.query(":MEASure:VMIN? CHAN1")
    print(dsoScope.query(r'*OPC?'))
    VsysAve = dsoScope.query(":MEASure:VAVerage? CHAN1")
    print(dsoScope.query(r'*OPC?'))
    IspkrMax = dsoScope.query(":MEASure:VMAX? CHAN2")
    print(dsoScope.query(r'*OPC?'))
    IspkrAvg = dsoScope.query(":MEASure:VAVerage? CHAN2")
    print(dsoScope.query(r'*OPC?'))
    #print("Vsys min: " + str(VsysMin))
    #print("Vsys Avg: " + str(VsysAve))
    #print("Ispkr Max: " + str(IspkrMax))
    #print("Ispkr Avg: " + str(IspkrAvg))
    #vsysMin = VsysMin.split('\n')
    VsysMin = str(VsysMin)
    VsysAve = str(VsysAve)
    IspkrAvg = str(IspkrAvg)
    IspkrMax = str(IspkrMax)

    VsysMin = VsysMin.strip()
    VsysAve = VsysAve.strip()
    IspkrAvg = IspkrAvg.strip()
    IspkrMax = IspkrMax.strip()

    global VsysAvgGlobal
    global VsysMinGlobal

    VsysAvgGlobal = float(VsysAve)
    VsysMinGlobal = float(VsysMin)

    return VsysMin, VsysAve, IspkrMax, IspkrAvg,

def writeToLog(inLog , inGGvolt, inGGCurr):

    f = open(inLog, "a")
    timeStamp = time.time()
    timeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
    #GGvolt, GGcur = getGGinfo()
    #time.sleep(scopeDelay)
    #dsoScope.write(":STOP")
    time.sleep(2)
    scopeVsysMin, scopeVsysAve, scopeIspkrMax, scopeIspkrAvg = measureScope()

    data = timeStamp + "," + inGGvolt + "," + inGGCurr + "," + scopeVsysMin + "," + scopeVsysAve + "," + scopeIspkrMax + "," + scopeIspkrAvg

    f.write(data + "\n")

    f.close()

   
    
    


if __name__=="__main__":
    rm = pyvisa.ResourceManager()
    dsoScope = rm.open_resource('GPIB0::7::INSTR')
    print(dsoScope.query('*IDN?'))
    initScope()
    #define location for log results,
    # open and write headers to logs 
    l1 = open(LOG1, "a")
    l1.write(header1 + "\n")
    l1.close()

    l2 = open(LOG2, "a")
    l2.write(header2 + "\n")
    l2.close()

    l3 = open(LOG3, "a")
    l3.write(header3 + "\n")
    l3.close()

    l4 = open(LOG4, "a")
    l4.write(header4 + "\n")
    l4.close()

    #loginISP()

    #triggerScope()
    #sendEFR(":isp:audio:playsound:6:100;")
    #time.sleep(scopeDelay)
    #measureScope()


    #^^ how to take scope measurement

    while(VsysMinGlobal > 2.8 and VsysAvgGlobal > 3.0 ):
        #sendEFR("reset;")
        print("Vsys Min is: " + str(VsysMinGlobal))
        print("Vsys Avg is: " + str(VsysAvgGlobal))
        #time.sleep(30)
        #loginISP()
        #GG to log1
        #scope cap to log1
        ###First Part#######

        setScopeTime(100)
       #play sound 6
        print("in part 3")
        triggerScope()
        time.sleep(0.1)
        time.sleep(0.1)
        time.sleep(0.1)
        time.sleep(0.1)
        #time.sleep(0.3)
        sendEFR(":isp:audio:playsound:6:100;")
        time.sleep(0.1)
        time.sleep(0.1)
        time.sleep(0.1)
        time.sleep(0.1)
        #time.sleep(0.3)
        dsoScope.write(":STOP")
        GGvolt, GGcur = getGGinfo()
        #dsoScope.write(":STOP")
        #time.sleep(0.2)
        #dsoScope.write(":STOP")
        #GGvolt, GGcur = getGGinfo()
        writeToLog(LOG3, GGvolt, GGcur)
        #time.sleep(10)
        #triggerScope()
        #writeToLog(LOG3)
        #GG to log3
        #scopeCap to log3

        #play sound 1
        #GG to log4
        #scope cap to log4
        print("in part 4")
        setScopeTime(1000)
        triggerScope()
        time.sleep(1)
        sendEFR(":isp:audio:playsound:1:100;")
        #triggerScope()
        #GGvolt, GGcur = getGGinfo()
        #writeToLog(LOG1, GGvolt, GGcur)
        time.sleep(3)
        GGvolt, GGcur = getGGinfo()
        time.sleep(5)
        #triggerScope()
        dsoScope.write(":STOP")
        writeToLog(LOG4, GGvolt, GGcur)
        #time.sleep(10)
        #update globals 
        sendISP('pwm_on 0 0')
        time.sleep(2)
        sendISP("\r")
        sendISP('pwm_on 0 0')
        time.sleep(2)
        sendISP("\r")
        time.sleep(2)
        #IRLEDS OFF
    
    print("Test Complete")


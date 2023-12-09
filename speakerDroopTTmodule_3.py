#This is the third version of this test. 

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


'''
UPDATE 20231011 V3, adjust speaker clipping with a start of 
'''
 
import pyvisa
import serial
import time
import datetime
import re
import pyautogui

ispLoginName = ''
ispLoginPassword = ''
rm = ""
dsoScope = ""
UARTcmdDelay = 1
scopeDelay = 11
EFRport = r'COM7'
#OVport = r'COM16'
header0 = "Time,GGvolt (NoLoad),GGcurrent (NoLoad) ,Vsysmin (NoLoad),VsysAvg (NoLoad),IspkrMax (NoLoad),IspkrAvg (NoLoad), Time,GGvolt (MAX CLP LVL 0),GGcurrent (MAX CLP LVL 0) ,Vsysmin (MAX CLP LVL 0),VsysAvg (MAX CLP LVL 0),IspkrMax (MAX CLP LVL 0),IspkrAvg (MAX CLP LVL 0),Time,GGvolt (MAX CLP LVL -3),GGcurrent (MAX CLP LVL -3) ,Vsysmin (MAX CLP LVL -3),VsysAvg (MAX CLP LVL -3),IspkrMax (MAX CLP LVL -3),IspkrAvg (MAX CLP LVL -3),Time,GGvolt (MAX CLP LVL -9),GGcurrent (MAX CLP LVL -9) ,Vsysmin (MAX CLP LVL -9),VsysAvg (MAX CLP LVL -9),IspkrMax (MAX CLP LVL -9),IspkrAvg (MAX CLP LVL -9),Time,GGvolt (MAX CLP LVL -9),GGcurrent (MAX CLP LVL -9) ,Vsysmin (MAX CLP LVL -9),VsysAvg (MAX CLP LVL -9),IspkrMax (MAX CLP LVL -9),IspkrAvg (MAX CLP LVL -9),Time,GGvolt (MAX CLP LVL -12),GGcurrent (MAX CLP LVL -12) ,Vsysmin (MAX CLP LVL -12),VsysAvg (MAX CLP LVL -12),IspkrMax (MAX CLP LVL -12),IspkrAvg (MAX CLP LVL -12),Time,GGvolt (MAX CLP LVL -15),GGcurrent (MAX CLP LVL -15) ,Vsysmin (MAX CLP LVL -15),VsysAvg (MAX CLP LVL -15),IspkrMax (MAX CLP LVL -15),IspkrAvg (MAX CLP LVL -15),Time,GGvolt (MAX CLP LVL -18),GGcurrent (MAX CLP LVL -18) ,Vsysmin (MAX CLP LVL -18),VsysAvg (MAX CLP LVL -18),IspkrMax (MAX CLP LVL -18),IspkrAvg (MAX CLP LVL -18),Time,GGvolt (MAX CLP LVL -21),GGcurrent (MAX CLP LVL -21) ,Vsysmin (MAX CLP LVL -21),VsysAvg (MAX CLP LVL -21),IspkrMax (MAX CLP LVL -21),IspkrAvg (MAX CLP LVL -21),Time,GGvolt (MAX CLP LVL -24),GGcurrent (MAX CLP LVL -24) ,Vsysmin (MAX CLP LVL -24),VsysAvg (MAX CLP LVL -24),IspkrMax (MAX CLP LVL -24),IspkrAvg (MAX CLP LVL -24),Time,GGvolt (MAX CLP LVL -27),GGcurrent (MAX CLP LVL -27) ,Vsysmin (MAX CLP LVL -27),VsysAvg (MAX CLP LVL -27),IspkrMax (MAX CLP LVL -27),IspkrAvg (MAX CLP LVL -27), \n"
#header1 = "OV ON Time,OV ON GGvolt,OV ON GGcurrent,Vsysmin,OV ON Vsysavg, OV ON IspkrmaX, OV ON IspkrAVG, \n"
#header2 = "IRLEDS Time,IRLEDS GGvolt,IRLEDS GGcurrent,IRLEDS Vsysmin,IRLEDS Vsysavg,IRLEDS IspkrmaX,IRLEDS IspkrAVG,\n"
#header3 = "IRLEDS SIREN Time,IRLEDS SIREN GGvolt,IRLEDS SIREN GGcurrent,IRLEDS SIREN Vsysmin,IRLEDS SIREN Vsysavg,IRLEDS SIREN IspkrmaX,IRLEDS SIREN IspkrAVG, \n"
#header4 = "IRLEDS HARVARD Time,IRLEDS HARVARD GGvolt,IRLEDS HARVARD GGcurrent,IRLEDS HARVARD Vsysmin,IRLEDS HARVARD Vsysavg,IRLEDS HARVARD IspkrmaX,IRLEDS HARVARD IspkrAVG \n"
VsysMinGlobal = 5
VsysAvgGlobal = 5

#global CLP_LVL
#global MAX_CLP  
#global END_CLP  

EFR = serial.Serial(port=EFRport, baudrate=9600, parity="N", stopbits=1, bytesize=8, timeout=None)
#OV = serial.Serial(port=OVport, baudrate=115200, parity="N", stopbits=1, bytesize=8, timeout=None)

#EFR.setRTS(True)
LOG0 = r'C:\Users\EIzazaga\OneDrive - Arlo Technologies, Inc\Desktop\Aquila Stuff\SpeakerDroopTest\SpeakerDroop_testCode\TestLogs\20231129_test_3_rechargeable_dry_run_lower_Params.txt'
#LOG1 = r'C:\Users\EIzazaga\OneDrive - Arlo Technologies, Inc\Desktop\Aquila Stuff\SpeakerDroopTest\SpeakerDroop_testCode\TestLogs\DRY_RUN_LOG1.txt'
#LOG2 = r'C:\Users\EIzazaga\OneDrive - Arlo Technologies, Inc\Desktop\Aquila Stuff\SpeakerDroopTest\SpeakerDroop_testCode\TestLogs\DRY_RUN_LOG2.txt'
#LOG3 = r'C:\Users\EIzazaga\OneDrive - Arlo Technologies, Inc\Desktop\Aquila Stuff\SpeakerDroopTest\SpeakerDroop_testCode\TestLogs\DRY_RUN_LOG3.txt'
#LOG4 = r'C:\Users\EIzazaga\OneDrive - Arlo Technologies, Inc\Desktop\Aquila Stuff\SpeakerDroopTest\SpeakerDroop_testCode\TestLogs\DRY_RUN_LOG4.txt'

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

    #print("Length of voltage: " + str(len(voltage)))

    #print("GG volt function reading: "+voltage+"\n")
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

    #print("Length of current: " + str(len(current)))
    #print("GG curr function reading: "+current+"\n")
    #print(current)
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

    data = timeStamp + "," + inGGvolt + "," + inGGCurr + "," + scopeVsysMin + "," + scopeVsysAve + "," + scopeIspkrMax + "," + scopeIspkrAvg + ","

    f.write(data)
    #f.write(data + ", CLIPPING_LVL " + str(CLP_LVL) + ", MAX_CLP_LVL " + str(MAX_CLP) + ", END_CLP_LVL " + str(END_CLP) + "\n")

    #data

    f.close()

   


def ttModuleLogInISP():
    print("loggin into TT module: ")
    sendEFR("isp:power:on;")
    time.sleep(1)
    pyautogui.moveTo(237, 384)
    pyautogui.click()
    time.sleep(3)
    pyautogui.write("\n")
    time.sleep(3)
    pyautogui.write("\n")
    pyautogui.write(ispLoginName)
    pyautogui.write("\n")
    time.sleep(3)
    pyautogui.write(ispLoginPassword)
    pyautogui.write("\n")
    time.sleep(3)
    #sendEFR("isp:power:on;")
def ttModuleSendISP(inCommand):
    print("Command sent to TT terminal: " +inCommand)
    pyautogui.moveTo(237, 384)
    pyautogui.click()
    pyautogui.write("\n")
    time.sleep(3)
    pyautogui.write(inCommand)
    pyautogui.write("\n")
    time.sleep(3)


def write_zero_for_scope_cap(inLog, inGGvolt, inGGCurr):
    print("Writing 0 in the log ")
    global CLP_LVL
    global MAX_CLP  
    global END_CLP 

    f = open(inLog, "a")
    timeStamp = time.time()
    timeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
    #GGvolt, GGcur = getGGinfo()
    #time.sleep(scopeDelay)
    #dsoScope.write(":STOP")
    time.sleep(2)
    #scopeVsysMin, scopeVsysAve, scopeIspkrMax, scopeIspkrAvg = measureScope()

    data = timeStamp + "," + inGGvolt + "," + inGGCurr + "," + "0" + "," + "0" + "," + "0" + "," + "0" + ","

    f.write(data)
    #f.write(data + ", CLIPPING_LVL " + str(CLP_LVL) + ", MAX_CLP_LVL " + str(MAX_CLP) + ", END_CLP_LVL " + str(END_CLP) + "\n")

    f.close()

def write_new_line_in_log(inLog):
    print("Writing /n to log ")
    f = open(inLog, "a")
    f.write(", \n")


if __name__=="__main__":
    global CLP_LVL
    global MAX_CLP
    global END_CLP

    CLP_LVL = -27
    MAX_CLP = 0
    END_CLP = 0
    rm = pyvisa.ResourceManager()
    dsoScope = rm.open_resource('GPIB0::7::INSTR')
    print(dsoScope.query('*IDN?'))
    initScope()
    #define location for log results,
    # open and write headers to logs
    l0 = open(LOG0, "a")
    l0.write(header0 + "\n")
    l0.close()

    #l1 = open(LOG1, "a")
    #l1.write(header1 + "\n")
    #l1.close()

    

    ISPCounterForLogin = 0
    #while True:
#        global CLP_LVL
#        global MAX_CLP
#        global END_CLP
    
    setScopeTime(100)
    triggerScope()
    #measureScope()
    GGvolt, GGcur = getGGinfo()
    writeToLog(LOG0, GGvolt, GGcur)
    time.sleep(2)

    ########IRLEDS on##########
    ttModuleLogInISP()
    time.sleep(5)
    ttModuleSendISP('pwm_on 85016 0')
    #time.sleep(2)
    #sendISP("\r")
    ttModuleSendISP('pwm_on 85016 0')
    #time.sleep(2)
    while(MAX_CLP != -27):
            print(MAX_CLP)
            sendEFR(":isp:power:on;")
            sendEFR(":isp:power:on;")
            sendEFR(":isp:power:on;")
            ttModuleLogInISP()
            #ttModuleSendISP('pwm_on 85016 0')
            time.sleep(2)
            #sendISP("\r")
            #ttModuleSendISP('pwm_on 85016 0')
            time.sleep(2)    
            print("Going into first IF statement")
            print("Vsys Avg: Vsys Min is= " + str(VsysMinGlobal) + " Vsys Avg is= " + str(VsysAvgGlobal))
            if(CLP_LVL > END_CLP):
                print("in first comparison ")
                print("CLP_LVL = " + str(CLP_LVL) + " " + "END_CLP = " + str(END_CLP) )
                time.sleep(2)
                #time.sleep(10)
                #update globals 
                ttModuleSendISP('pwm_on 0 0')
                time.sleep(2)
                #sendISP("\r")
                ttModuleSendISP('pwm_on 0 0')
                time.sleep(2)
                #sendISP("\r")
                time.sleep(2)
                #IRLEDS OFF
                #Turn Off ISP here
                #sendEFR(":isp:power:off;")
                #sendEFR(":isp:power:off;")
                sendEFR("reset;")
                while(MAX_CLP < -27):
                    print("STOP")
                time.sleep(20)
                CLP_LVL = -27
                setScopeTime(100)
                triggerScope()
                #measureScope()
                GGvolt, GGcur = getGGinfo()
                writeToLog(LOG0, GGvolt, GGcur)
                time.sleep(2)
            elif(CLP_LVL > MAX_CLP):
                print("in second comparison")
                #print("")
                print("CLP_LVL = " + str(CLP_LVL) + " " + "MAX_CLP = " + str(MAX_CLP) )
                GGvolt, GGcur = getGGinfo()
                write_zero_for_scope_cap(LOG0, GGvolt, GGcur)
                CLP_LVL = CLP_LVL + 3
                print("CLP_LVL: " + str(CLP_LVL - 3) + " is now: " + str(CLP_LVL))
                #break 
            else:
                print("Writing 0 and increasing CLP_LVL")
                print("CLP_LVL = " + str(CLP_LVL) + " " + "MAX_CLP = " + str(MAX_CLP) ) 
                ttModuleSendISP("spkr_limit " + str(CLP_LVL))
                triggerScope()
                time.sleep(0.1)
                time.sleep(0.1)
                time.sleep(0.1)
                time.sleep(0.1)        
                sendEFR(":isp:audio:playsound:6:100;")
                #time.sleep(0.1)
                #time.sleep(0.1)
                time.sleep(0.1)
                time.sleep(0.1)      
                dsoScope.write(":STOP")
                GGvolt, GGcur = getGGinfo()
                writeToLog(LOG0, GGvolt, GGcur)
                time.sleep(2)
                #l0 = open(LOG0, "a")
                #l0.write("\n")
                #l0.close()
                print("Comparing Vsys Min, Vsys Avg: Vsys Min is= " + str(VsysMinGlobal) + " Vsys Avg is= " + str(VsysAvgGlobal))
                if(VsysMinGlobal < 2.8 or VsysAvgGlobal < 3.0):
                    print("Vsys Min is: " + str(VsysMinGlobal))
                    print("Vsys Avg is: " + str(VsysAvgGlobal))
                    MAX_CLP = CLP_LVL - 3
                    print("MAX_CLP: " + str(MAX_CLP - 3) +  " is now: " + str(MAX_CLP))
                    time.sleep(2)
                    #time.sleep(10)
                    #update globals 
                    ttModuleSendISP('pwm_on 0 0')
                    time.sleep(2)
                    #sendISP("\r")
                    ttModuleSendISP('pwm_on 0 0')
                    time.sleep(2)
                    #sendISP("\r")
                    time.sleep(2)
                    #IRLEDS OFF
                    #Turn Off ISP here
                    #sendEFR(":isp:power:off;")
                    #sendEFR(":isp:power:off;")
                    #sendEFR(":isp:power:off;")
                    sendEFR("reset;")
                    while(MAX_CLP < -27):
                        print("STOP")
                        exit()
                    time.sleep(20)
                    CLP_LVL = -27
                    #write_new_line_in_log(LOG0)
                    l0 = open(LOG0, "a")
                    l0.write(header0 + "\n")
                    l0.close()
                    setScopeTime(100)
                    triggerScope()
                    #measureScope()
                    GGvolt, GGcur = getGGinfo()
                    writeToLog(LOG0, GGvolt, GGcur)
                    time.sleep(2)
                else:
                    CLP_LVL = CLP_LVL + 3
                    print("CLP_LVL: " + str(CLP_LVL - 3) +  " is now: " + str(CLP_LVL)) 
            
            



    


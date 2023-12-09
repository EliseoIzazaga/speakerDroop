#by Eliseo Izazaga, 
#This will be similar to the speaker droop test except we will use a state machine to drive the test

'''
UPDATE 20231011 V2, adjust speaker clipping with a start of 

HEllo This is new code
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
header0 = "OV OFF Time,OV OFF GGvolt,OV OFF GGcurrent,Vsysmin,OV OFF Vsysavg, OV OFF IspkrmaX, OV OFF IspkrAVG,IRLEDS SIREN GGvolt,IRLEDS SIREN GGcurrent,IRLEDS SIREN Vsysmin,IRLEDS SIREN Vsysavg,IRLEDS SIREN IspkrmaX,IRLEDS SIREN IspkrAVG, \n"
#header1 = "OV ON Time,OV ON GGvolt,OV ON GGcurrent,Vsysmin,OV ON Vsysavg, OV ON IspkrmaX, OV ON IspkrAVG, \n"
#header2 = "IRLEDS Time,IRLEDS GGvolt,IRLEDS GGcurrent,IRLEDS Vsysmin,IRLEDS Vsysavg,IRLEDS IspkrmaX,IRLEDS IspkrAVG,\n"
#header3 = "IRLEDS SIREN Time,IRLEDS SIREN GGvolt,IRLEDS SIREN GGcurrent,IRLEDS SIREN Vsysmin,IRLEDS SIREN Vsysavg,IRLEDS SIREN IspkrmaX,IRLEDS SIREN IspkrAVG, \n"
#header4 = "IRLEDS HARVARD Time,IRLEDS HARVARD GGvolt,IRLEDS HARVARD GGcurrent,IRLEDS HARVARD Vsysmin,IRLEDS HARVARD Vsysavg,IRLEDS HARVARD IspkrmaX,IRLEDS HARVARD IspkrAVG \n"
VsysMinGlobal = 5
VsysAvgGlobal = 5

global CLP_LVL
global MIN_CLP  
global END_CLP  

#CLP_LVL = -27
#MIN_CLP = 0
END_CLP = 0

EFR = serial.Serial(port=EFRport, baudrate=9600, parity="N", stopbits=1, bytesize=8, timeout=None)
#OV = serial.Serial(port=OVport, baudrate=115200, parity="N", stopbits=1, bytesize=8, timeout=None)

#EFR.setRTS(True)
LOG0 = r'C:\Users\EIzazaga\OneDrive - Arlo Technologies, Inc\Desktop\Aquila Stuff\SpeakerDroopTest\SpeakerDroop_testCode\TestLogs\DRY_RUN_ALKALINE_25C.txt'
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
    global CLP_LVL
    f = open(inLog, "a")
    timeStamp = time.time()
    timeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
    #GGvolt, GGcur = getGGinfo()
    #time.sleep(scopeDelay)
    #dsoScope.write(":STOP")
    time.sleep(2)
    scopeVsysMin, scopeVsysAve, scopeIspkrMax, scopeIspkrAvg = measureScope()

    data = timeStamp + "," + inGGvolt + "," + inGGCurr + "," + scopeVsysMin + "," + scopeVsysAve + "," + scopeIspkrMax + "," + scopeIspkrAvg

    f.write(data + ", CLIPPING_LVL " + str(CLP_LVL) + ", MIN_CLP_LVL " + str(MIN_CLP) + ", END_CLP_LVL " + str(END_CLP) + "\n")

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

#will need to make similar func for new log caps that take in CLP_LVL MIN_CLP and END_CLP
def write_zero_for_scope_cap(inLog, inGGvolt, inGGCurr):
    #global CLP_LVL
    global CLP_LVL
    global MIN_CLP  
    global END_CLP 
    f = open(inLog, "a")
    timeStamp = time.time()
    timeStamp = datetime.datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d %H:%M:%S')
    #GGvolt, GGcur = getGGinfo()
    #time.sleep(scopeDelay)
    #dsoScope.write(":STOP")
    time.sleep(2)
    #scopeVsysMin, scopeVsysAve, scopeIspkrMax, scopeIspkrAvg = measureScope()

    data = timeStamp + "," + inGGvolt + "," + inGGCurr + "," + "0" + "," + "0" + "," + "0" + "," + "0"

    f.write(data + ", CLIPPING_LVL " + str(CLP_LVL) + ", MIN_CLP_LVL " + str(MIN_CLP) + ", END_CLP_LVL " + str(END_CLP) + "\n")

    f.close()
    clp_lvl_increase()

def turnOnIRLEDS():
    time.sleep(5)
    ttModuleSendISP('pwm_on 85016 0')
    time.sleep(2)
    #sendISP("\r")
    ttModuleSendISP('pwm_on 85016 0')
    time.sleep(2)


def init_state():
    print("init state")
    #global CLP_LVL
    #global MIN_CLP  
    #global END_CLP  

    #CLP_LVL = -27
    #MIN_CLP = 0
    #END_CLP = 0
    setScopeTime(100)
    triggerScope()
    GGvolt, GGcur = getGGinfo()
    ttModuleLogInISP()
    turnOnIRLEDS()
    return "GOTO_MAIN_CONDITION_STATE"

def param_set_state():
    global MIN_CLP
    print("param set state")
    print(MIN_CLP)
    ttModuleSendISP('pwm_on 0 0')
    time.sleep(2)
    ttModuleSendISP('pwm_on 0 0')
    time.sleep(2)
    if(MIN_CLP < -27):
        while True:
            print("Test End")
    else:
        time.sleep(20)
        print("setting CLP_LVL to -27")
        global CLP_LVL
        CLP_LVL = -27
        return "GOTO_INIT_STATE"


def clp_lvl_increase():
    global CLP_LVL
    print("clp_level increase: clp_lvl is: " + str(CLP_LVL))
    #global CLP_LVL
    CLP_LVL = CLP_LVL + 3
    print("clp_lvl is now: " + str(CLP_LVL))
    return "GOTO_MAIN_CONDITION_STATE"

def min_clp_decrease():
    print("min_clp_decrease")
    global CLP_LVL
    global MIN_CLP
    MIN_CLP = CLP_LVL - 3
    #CALL PARAM SET STATE
    return param_set_state()

def log_0_state(inLOG):
    print("log 0 state")
    GGvolt, GGcur = getGGinfo()
    write_zero_for_scope_cap(inLOG, GGvolt, GGcur)
    clp_lvl_increase()

def siren_state(inLOG):
    global CLP_LVL
    print("siren state")
    ttModuleSendISP("spkr_limit " + str(CLP_LVL))
    triggerScope()
    #time.sleep(0.1)
    #time.sleep(0.1)
    #time.sleep(0.1)
    time.sleep(0.1)
    sendEFR(":isp:audio:playsound:6:100;")
    #sendEFR(":isp:audio:playsound:6:100;")
    #time.sleep(0.1)
    #time.sleep(0.1)
    #time.sleep(0.1)
    #time.sleep(0.1)
    dsoScope.write(":STOP")      
    GGvolt, GGcur = getGGinfo()
    writeToLog(inLOG, GGvolt, GGcur)
    l0 = open(inLOG, "a")
    l0.write(" Clipping =  " + str(CLP_LVL))
    l0.write("\n")
    l0.close()
    time.sleep(2)

def vSys_condition_state():
    global VsysMinGlobal
    global VsysAvgGlobal
    print("IN VYSYS_CONDITION_STATE")
    print("VsysMin =: " + str(VsysMinGlobal))
    print("VsysAvg =: " + str(VsysAvgGlobal))
    if(VsysMinGlobal < 3.5 or VsysAvgGlobal < 4.1):
        print("GOING TO MIN_CLP_DECREASE_STATE")
        return "GOTO MIN_CLP_DECREASE_STATE"
    else:
        print("GOING TO CLP_LVL_INCREASE_STATE")
        return "GOTO CLP_LVL_INCREASE_STATE"
    
    

def condition_state_CLP():
    print("IN MAIN CONDITION STATE")
    global CLP_LVL
    global END_CLP
    global MIN_CLP
    if(CLP_LVL > END_CLP):
        print("COMPARING CLP_LVL AND END_CLP "+ " CLP_LVL :" + str(CLP_LVL) + " END_CLP :" +str(END_CLP))
        print("GOING TO PARAM_SET_STATE")
        return "GOTO PARAM_SET_STATE"
    else:
        if(CLP_LVL < MIN_CLP):
            print("COMPARING CLP_LVL AND MIN_CLP "+ " CLP_LVL :" + str(CLP_LVL) + " END_CLP :" +str(MIN_CLP))
            print("GOING TO LOG_0_STATE")
            return "GOTO LOG_0_STATE"
        else:
            print("GOING TO SIREN STATE")
            return "GOTO SIREN_STATE"
            

if __name__=="__main__":
    CLP_LVL = -27
    MIN_CLP = 0
    END_CLP = 0
    rm = pyvisa.ResourceManager()
    dsoScope = rm.open_resource('GPIB0::7::INSTR')
    print(dsoScope.query('*IDN?'))
    initScope()
    #define location of test results
    l0 = open(LOG0, "a")
    l0.write(header0 + "\n")
    l0.close()
    stateToGoTo = init_state()
    #stateToGoTo = condition_state_CLP()
    while True:
        if(stateToGoTo == "GOTO_INIT_STATE"): 
            stateToGoTo = init_state()
        if(stateToGoTo == "GOTO_MAIN_CONDITION_STATE"):
            stateToGoTo = condition_state_CLP()
        if(stateToGoTo == "GOTO PARAM_SET_STATE"):
            param_set_state()
        else:
            if(stateToGoTo == "GOTO LOG_0_STATE"):
                GGvolt, GGcur = getGGinfo()
                write_zero_for_scope_cap(LOG0, GGvolt, GGcur)
            else:
                if(stateToGoTo == "GOTO SIREN_STATE"):
                    siren_state(LOG0)
                    stateToGoTo = vSys_condition_state()
            if(stateToGoTo == "GOTO CLP_LVL_DECREASE_STATE"):
                stateToGoTo = min_clp_decrease()
            else:
                if(stateToGoTo == "GOTO CLP_LVL_INCREASE_STATE"):
                   stateToGoTo = clp_lvl_increase()





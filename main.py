from machine import ADC,Pin,UART
from utime import sleep
 
MQ2= ADC(28)
LED=Pin(16,Pin.OUT)#LED pin
Buzzer=Pin(15,Pin.OUT)#Buzzer Pin
BatID=Pin(25,Pin.OUT)#Battery Indicator, it is the onboard LED.


gsm_module = UART(0, baudrate=9600, tx=Pin(12), rx=Pin(13), timeout=2000)#You can replace the Rx and Tx pin if have changed them in the circuit. Also change 0 to 1 if you have used UART1
gsm_buffer = ''
destination_phone = 'Destination Phone number with country code'

#----GSM Functions----#
def convert_to_string(buf):
    tt =  buf.decode('utf-8').strip()
    return tt
def send_command(cmdstr, lines=1, msgtext=None):
    global gsm_buffer
    print(cmdstr)
    cmdstr = cmdstr+'\r\n'
    while gsm_module.any():
        gsm_module.read()
    gsm_module.write(cmdstr)
    if msgtext:
        print(msgtext)
        gsm_module.write(msgtext)
    buf=gsm_module.readline() #discard linefeed etc
    #print('discard linefeed:{}'.format(buf))
    buf=gsm_module.readline()
    #print('next linefeed:{}'.format(buf))
    if not buf:
        return None
    result = convert_to_string(buf)
    if lines>1:
        gsm_buffer = ''
        for i in range(lines-1):
            buf=gsm_module.readline()
            if not buf:
                return result
            #print(buf)
            buf = convert_to_string(buf)
            if not buf == '' and not buf == 'OK':
                gsm_buffer += buf+'\n'
    return result
def send_sms(msgtext):
    global gsm_buffer
    result = send_command('AT+CMGS="{}"\n'.format(destination_phone),99,msgtext+'\x1A')
    if result and result=='>' and gsm_buffer:
        params = gsm_buffer.split(':')
        if params[0]=='+CUSD' or params[0] == '+CMGS':
            print('OK')
            return 'OK'
#----0----#

print(send_command('AT'))#check connection between pico and sim800l
print(send_command('AT+CMEE=1'))#if you get an error, this will make sure you get the error code. Search on the internet to find solution
print(send_command('AT+CPIN?'))#make sure the sim is inserted properly
print(send_command('AT+CSQ'))#checks the network strength
print(send_command('AT+CMGF=1'))#enables text mode
print(send_command('AT+CNMI=1'))

while True:
    reading=MQ2.read_u16()     
    print(reading)
    if reading>20000:
        Buzzer.value(1)
        LED.value(1)
        send_sms('SMS text that you want to send')
        #--~--#
        char=send_command('AT+CBC')
        charg=char[:-5]
        charge=int(charg.replace('+CBC: 0,',''))
        print(charge)
        if charge<=15:
            BatID.value(1)
            sleep(0.5)
            BatID.value(0)
        else:
            BatID.value(0)
    else:
        Buzzer.value(0)
        LED.value(0)
    sleep(2)#change the refresh rate if you want to. For faster rate, reduce the time and vice-versa


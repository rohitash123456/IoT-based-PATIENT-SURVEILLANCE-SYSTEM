import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import serial

pnconf = PNConfiguration()
pnconf.subscribe_key = "sub-c-49b1aafe-19f4-11e7-894d-0619f8945a4f"
pnconf.publish_key = "pub-c-860897e3-bc4e-4d19-9e11-dfaeee7284b3"
pubnub = PubNub(pnconf)
channel = "pidemo"


ser = serial.Serial('/dev/ttyS0', 9600, timeout=5)
###reading raw data from 8051###
while True:
    
    ser.write("t")
    tl= ser.read()
    th = ser.read()
    
    time.sleep(0.1)
    ser.write("h")
    hl = ser.read()
    hh = ser.read()
    
    ser.flush();
    time.sleep(0.5)
    ser.write("a")
    time.sleep(0.1)
    a = ser.read()
    a1=ser.read()
    a2=ser.read()
    
###end of reding raw data####

    ####starting conversion#####
    
    ##acc conversion first####
    x=ord(a)&0x3f
    y=ord(a1)&0x3f
    z=ord(a2)&0x3f
    if((x&(1<<5))):
        x=x|0xc0
        x=(256-x)*-1
    if((y&(1<<5))):
        y=y|0xc0
        y=(256-y)*-1
    if((z&(1<<5))):
        z=z|0xc0
        z=(256-z)*-1
     
     ####acc converstion is over here###
     ##heart beat decode###
    
    hb=ord(hl)
    print "heart beat"
    print hb
    time.sleep(2)
    
    ###heart beat decoded ###
    
    ###temperature####
    th=ord(th)
    tl=ord(tl)
    th=th & 0x7f
    th=th<<4
    t=th | (tl)>>4
    
    i=1
    while(i<5):
        if(tl&(1<<(4-i))):
		    t=t+(0.5**i)
        i=i+1
    print "tempe"
    print t
    
    print "acc"
    print x
    print y
    print z
    
    ###end of temperature###
    
    #print 'connected'
    
    pubnub.publish().channel(channel).message({'TEMP':str(t),'HB':str(hb),'X':str(x),'Y':str(y),'Z':str(z)}).sync()
    



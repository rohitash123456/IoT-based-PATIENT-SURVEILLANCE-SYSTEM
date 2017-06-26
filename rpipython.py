import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
#import serial

#ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=5)
while True:
 """   time.sleep(2)
    ser.write("t")
    t1 = ser.read()
    t2 = ser.read()

    time.sleep(1)
    ser.write("h")
    time.sleep(11)
    h = ser.read(4)

    time.sleep(1)
    ser.write("a")
    a = ser.read(4)
"""
   # print s
    pnconf = PNConfiguration()
    pnconf.subscribe_key = "pub-c-077eca30-340d-11e7-81b3-02ee2ddab7fe"
    pnconf.publish_key = "pub-c-df8834de-1092-41eb-bff8-29f753a7184b"
    pubnub = PubNub(pnconf)
    channel = "Channel1"
    print "dainth"
    print 'connected'
    pubnub.publish().channel(channel).message({'TEMP': t[:3], 'HB': h[:3], 'ACC':a[:3]}).sync()
    #result = my_listener.wait_for_message_on(channel)
    #print(result.message)

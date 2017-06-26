import datetime
import time
import os
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from Tkinter import *
import signal
from matplotlib.figure import Figure
matplotlib.use('TkAgg')
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
 
pnconfig = PNConfiguration()
 
pnconfig.publish_key = 'pub-c-860897e3-bc4e-4d19-9e11-dfaeee7284b3'
pnconfig.subscribe_key = 'sub-c-49b1aafe-19f4-11e7-894d-0619f8945a4f'
 
pubnub = PubNub(pnconfig)
 
my_listener = SubscribeListener()
pubnub.add_listener(my_listener)
 
pubnub.subscribe().channels('pidemo').execute()
my_listener.wait_for_connect()
print('connected')

def handler(signum, frame):
    raise KeyboardInterrupt
    #print 'Ctrl+Z pressed, but ignored'

root = Tk()
root.title("project")
#root.attributes('-fullscreen', True)
left=Frame(root)
left.pack(side=TOP,fill=BOTH, expand=1)
right=Frame(root)
right.pack(side=BOTTOM, anchor=NE, fill=BOTH, expand=1)

west=Frame(root)
west.pack(side=BOTTOM,anchor=NE,fill=BOTH, expand=0)#rangeeee
east=Frame(root)
east.pack(side=BOTTOM,anchor=NE,fill=BOTH, expand=0)

a=Label(east,font=('times',40 , 'bold'), bg='red') #for differernt axes
b=Label(west,font=('times',40 , 'bold'),bg='blue')  # color range 
v=Label(right,font=('times',40 , 'bold'), bg='yellow')



#f = Figure(figsize=(5, 4), dpi=100)     
# 
# 
#   
fi, ax = plt.subplots()
lines, = ax.plot([],[])       
ax.grid(True)
ax.set_xlabel('Time')
ax.set_ylabel('temperature')
ax.set_title("Monitering system")

#ax.set_xlim(0,200)
#ax.set_ylim(0,110)#setting y limit 0-110
c = FigureCanvasTkAgg(fi, master=left)
c.show()
c.get_tk_widget().pack(fill=BOTH, expand=1)



def show(xdata, ydata):

        lines.set_xdata(xdata)
        lines.set_ydata(ydata)
        
        ax.set_xlim(auto=True)
        ax.set_ylim(0,200)
        
        #Need both of these in order to rescale
        ax.relim()
        ax.autoscale_view()
        #We need to draw *and* flush
        fi.canvas.flush_events()
        c.show()

volumelist=[]  #y axis
potlist=[]#x axis
volumelist1=[]
volumel=[]  #y axis
potl = []
reading = 0



try:

        while 1:
                result = my_listener.wait_for_message_on('pidemo')
                #print(result.message[u'ACC'])
                #print type(result.message)
                volumelist.append(result.message[u'HB'])
                potlist.append(reading)
                reading=reading+1
                show(potlist,volumelist)
               # v.config(text=str("Heart beat:"+result.message[u'HB'])+"BPM")
                #v.pack(fill=X,expand=1)
                a.config(text=str("TEMP:"+result.message[u'TEMP'])+"c")
                a.pack(fill=X,expand=1)
                b.config(text=str("ACC:"+result.message[u'HB'])+"k")
                b.pack(fill=X,expand=1)
                time.sleep(0.01)
            
except KeyboardInterrupt:   
   # exits when you press CTRL+C  
    print "\nPlotting Graph is closed Bye\n" 
    plt.close('all')
    pubnub.unsubscribe().channels('pidemo').execute()
    my_listener.wait_for_disconnect()
    print('unsubscribed')
except:  
 #   print "\nOther error or exception occurred!\n good bye\n"  
    plt.close('all')
    pubnub.unsubscribe().channels('pidemo').execute()
    my_listener.wait_for_disconnect()
    print('unsubscribed')
finally: 
    print("bye")
    os.kill(os.getpid(), 9)
     
         

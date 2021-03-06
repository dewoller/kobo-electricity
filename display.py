from tkinter import *
import MQTT
import queue
import logging, logging.handlers, logging.config
logging.config.fileConfig('log.conf' )
logger=logging.getLogger( "kobo" )

eventQueue = queue.Queue()
mqtt = MQTT.MQTT(  "192.168.1.38", eventQueue, clientID="kobo", inTopic="/home/electricity/ac", outTopic="kobo" )
nzones=10

values= [0] * nzones


root = Tk()

root.geometry('800x600+0+0')
root.overrideredirect(True)
root.overrideredirect(False)
root.attributes('-fullscreen',True)

labelText = StringVar()
depositLabel = Label(root, text = "hello",textvariable=labelText, font=("Helvetica", 200))
depositLabel.pack(side=RIGHT)
labelText.set('start')
#root.mainloop()

while True:
    root.update()
    try:
        payload = eventQueue.get(True, 300)
        eventQueue.task_done()
    except queue.Empty as e:
            continue
        
    zone=int(payload[0])
    if zone<0 or zone >= nzones:
        continue
    values[ zone ] = int(payload[1])
    if zone==9:
        labelText.set(sum( values))
        




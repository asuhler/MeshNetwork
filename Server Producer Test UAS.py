import pika
import sys
import time
from Tkinter import *


class vars():
    switch = True
    rabbit = object
    username = 'UAS'
    password = 'UAS'
    host = '10.128.4.222'
    vhost = 'UASHost'
    exchange = 'UAS'

Vars = vars()

creds = pika.PlainCredentials(username=Vars.username, password=Vars.password)
connection = pika.BlockingConnection(pika.ConnectionParameters(\
        host = Vars.host,\
        virtual_host = Vars.vhost,\
        credentials = creds))

channel = connection.channel()

channel.exchange_declare(exchange = Vars.exchange, \
                         type = 'topic')

def publishSomething():
    channel.basic_publish(exchange=Vars.exchange, \
    routing_key='Autopilot.commands',\
    body="Land")
    #"Loiter,2,2,10"
def keypress(event):

    print "Key pressesd: " + str(event.char)
    if vars.switch == True:
        frame.configure(background= 'black')
        vars.switch = False
    else:
        frame.configure(background= 'white')
        vars.switch = True
    publishSomething()

def callback(event):
    frame.focus_set()
    frame.configure(background= 'white')


root = Tk()
print "Press a key (Escape key to exit):"
frame = Frame(root, width=100, height=100)
frame.configure(background= 'white')
frame.bind('<Key>', keypress)
frame.bind("<Button-1>", callback)
frame.pack()
frame.focus_set()
root.mainloop()


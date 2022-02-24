#!/usr/bin/env python3

import client
from random import randint

client.connect_npc( 'http://dragon.foi.hr:5000', 'markus', 'stef' )


state = 0

def next_action():
    global state
    if state == 0:
        return { 'action':'right', 'params':3 }
    elif state == 1:
        return { 'action':'up', 'params':3 }
    elif state == 2:
        return { 'action':'left', 'params':3 }
    elif state == 3:
        return { 'action':'down', 'params':3 }

def adjust( status ):
    global state
    print( status.data )
    if state == 3:
        state = 0
    elif state == 0:
        state = 1
    elif state == 1:
        state = 2
    elif state == 2:
        state = 3
    
client.sio.next_action = next_action
client.sio.status_callback = adjust

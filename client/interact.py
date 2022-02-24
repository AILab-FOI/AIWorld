#!/usr/bin/env python3

import client
from random import randint

client.connect_npc( 'http://dragon.foi.hr:5000', 'markus', 'ivek' )

state = 0

def next_action():
    global state
    if state == 0:
        return { 'action':'msg', 'params':'Hello!' }
    elif state == 1:
        return { 'action':'msg', 'params':'Go away!' }

def adjust( status ):
    global state
    print( status.data )
    if state == 1:
        state = 0
    else:
        state = 1
        
client.sio.next_action = next_action
client.sio.status_callback = adjust


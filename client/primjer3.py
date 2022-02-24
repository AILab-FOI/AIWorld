#!/usr/bin/env python3

import client
from random import choice

client.connect_npc( 'http://dragon.foi.hr:5000', 'markus', 'ivek' )

state = 0

def next_action():
    global state, mychoice
    if state == 0:
        return { 'action':'choice', 'params':{ 'msg':'Škare, papir ili kamen?', 'choices':[ 'škare', 'papir', 'kamen' ] } }
    elif state == 1:
        return { 'action':'msg', 'params':'I ja sam odabrao %s. Neodlučeno!' % mychoice }
    elif state == 2:
        return { 'action':'msg', 'params':'Ja sam odabrao %s. Ti pobjeđuješ!' % mychoice}
    elif state == 3:
        return { 'action':'msg', 'params':'Ja sam odabrao %s. Moja pobjeda!' % mychoice }

def adjust( status ):
    global state, mychoice
    print( status.data )
    mychoice = choice( [ 'škare', 'papir', 'kamen' ] )
    if state == 0:
        if status.answer == mychoice:
            state = 1
        elif status.answer == 'škare' and mychoice == 'kamen':
            state = 3
        elif status.answer == 'papir' and mychoice == 'škare':
            state = 3
        elif status.answer == 'kamen' and mychoice == 'papir':
            state = 3
        else:
            state = 2
    else:
        state = 0
        
client.sio.next_action = next_action
client.sio.status_callback = adjust


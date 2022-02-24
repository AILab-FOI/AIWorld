#!/usr/bin/env python3

import client
from random import randint

client.connect_npc( 'http://dragon.foi.hr:5000', 'markus', 'barica' )

'''
Moguće akcije
img - promjena slike + index
msg - poruka (igraču) + text
chat - poruka (na chat) + text
choice - odabir + text + izbori (callback?)
left - pomak lijevo + broj koraka
right - pomak desno + broj koraka
up - pomak gore + broj koraka
down - pomak dolje + broj koraka
gold - daj novce + količina

{ 
 'action':<akcija>
 'params':<parametri>
}

{ 
 'action':'img'
 'params':1
}

{ 
 'action':'msg'
 'params':'Bok, kako si?'
}

{ 
 'action':'chat'
 'params':'Bok, kako si?'
}

{ 
 'action':'choice'
 'params':{ 'msg':'Škare, papir ili kamen?', 'choices':[ 'škare', 'papir', 'kamen' ] }
}

{ 
 'action':'left' // ili right, up, down
 'params':3
}

{ 
 'action':'gold'
 'params':100
}

'''

state = 0

def next_action():
    global state
    if state == 0:
        return { 'action':'left', 'params':3 }
    elif state == 1:
        return { 'action':'right', 'params':3 }
    elif state == 2:
        return { 'action':'up', 'params':3 }
    elif state == 3:
        return { 'action':'down', 'params':3 }

def adjust( status ):
    global state
    print( status.data )
    if status.playerx > status.x:
        state = 0
    elif status.playerx < status.x:
        state = 1
    elif status.playery > status.y:
        state = 2
    elif status.playery < status.y:
        state = 3
    else:
        state = randint( 0, 3 )
    
client.sio.next_action = next_action
client.sio.status_callback = adjust

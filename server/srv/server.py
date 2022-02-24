#!/usr/bin/env python3

import argparse
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit, join_room
import eventlet
eventlet.monkey_patch()

from random import choice
import json
import sys
from time import sleep

from threading import Event

app = Flask(__name__)
CORS( app )
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO( app, logger=True, engineio_logger=True )


LIK = 'Ivek'

LIKOVI = { 'Ivek':0, 'Joža':1, 'Štefica':2, 'Marica':3, 'Štef':4, 'Barica':5 }
PORUKA = "Bok ja sam Ivek"

NPCS = {}
CLIENTS = []

def log( *arg ):
    print( '%s:' % request.sid, *arg )

def get_user( sid ):
    global NPCS
    try:
        user = [ i[ 'user' ] for i in NPCS.values() if i[ 'id' ] == sid  ][ 0 ]
    except Exception as e:
        user = 'not connected to any NPC'
    return user

def get_npc( sid ):
    global NPCS
    try:
        npc = [ i for i,j in NPCS.items() if j[ 'id' ] == sid  ][ 0 ]
    except Exception as e:
        npc = None
    return npc

@socketio.on( 'connect' )
def connect():
    global CLIENTS
    CLIENTS.append( request.sid )
    log( 'Client %s connected' % request.sid )
    
@socketio.on( 'disconnect' )
def disconnect():
    global CLIENTS
    log( 'Client %s (%s) disconnected' % ( get_user( request.sid ), request.sid ) )
    CLIENTS.remove( request.sid )
    npc = get_npc( request.sid )
    if npc:
        del NPCS[ npc ]

@socketio.on( 'connect_npc' )
def handle_connect_npc( data ):
    global NPCS
    if not data[ 'npc' ] in NPCS:
        log( 'Connecting', data[ 'username' ], 'to', data[ 'npc' ] )
        NPCS[ data[ 'npc' ] ] = { 'user':data[ 'username' ], 'id':request.sid, 'buffer':[] }
        send( { 'status':'ok' } )
    else:
        log( 'Error connecting', data[ 'username' ], 'to', data[ 'npc' ] )
        send( { 'status':'Error, the NPC has already been assigned!' } )

@socketio.on( 'next_action' )
def handle_next_action( data ):
    global NPCS
    user = get_user( request.sid )
    npc = get_npc( request.sid )
    if npc:
        log( 'Next action for NPC', npc, 'is', data[ 'action' ] )
        NPCS[ npc ][ 'buffer' ].append( data )
        #send( { 'actionstatus':'ok' } )
    else:
        log( 'Error issuing next action for NPC', npc )
        #send( { 'actionstatus':'Error, the NPC is not assigned!' } )



@app.route( '/query/poruka' )
def query():
    socketio.emit( 'bla', { 'hello':'bla' }, room=CLIENTS[ 0 ] )
    return json.dumps( { 'msg':PORUKA, 'lik':LIK, 'slika':LIKOVI[ LIK ] } )

@app.route( '/next/<npc>' )
def next( npc ):
    global NPCS
    try:
        sid = NPCS[ npc ][ 'id' ] 
        user = NPCS[ npc ][ 'user' ]
    except:
        return json.dumps( { 'action':None, 'params':None } )


    ev = Event()
    result = None

    def ack():
        nonlocal result
        nonlocal ev

        result = NPCS[ npc ][ 'buffer' ].pop()
        
        ev.set()

    socketio.emit( 'next', { 'next':user }, room=sid, callback=ack )
    ev.wait() 
    
    return json.dumps( { 'action':result[ 'action' ], 'params':result[ 'params' ] } )

@app.route( '/feedback/<npc>/<status>' )
def feedback( npc, status ):
    status = json.loads( status )
    print( 'Got status', npc, status )
    global NPCS
    try:
        sid = NPCS[ npc ][ 'id' ]
    except:
        return json.dumps( { 'status':'fail' } )
    socketio.emit( 'status', status, room=sid )
    return json.dumps( { 'status':'ok' } )

'''
Moguće akcije
img - promjena slike + index
msg - poruka + text
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument( "--rest", const=True, nargs='?', type=bool, help="Specify if the agent shoud be start as a RESTful server." )
    args = parser.parse_args()

    REST = bool( args.rest )

    if REST:
        socketio.run( app )
        sys.exit()

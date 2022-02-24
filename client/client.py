#!/usr/bin/env python3

import socketio

class status:
    def __init__( self, data ):
        self.data = data
        for k, v in data.items():
            self.__dict__[ k ] = v

sio = socketio.Client()


@sio.event
def connect():
    sio.connectcallback()

@sio.event
def connect_error( data ):
    print("The connection failed!")

@sio.event
def disconnect():
    print("Server disconnected!")

@sio.event
def message( data ):
    sio.npccallback( data )


@sio.on( 'bla' )
def handle_message( data ):
    print( data )

@sio.on( 'status' )
def handle_status( data ):
    sio.statuscallback( data )
    
@sio.on( 'next' )
def next_action( data ):
    def status_cb( data ):
        sio.status_callback( status( data ) )
    sio.statuscallback = lambda x:status_cb( x )
    sio.emit( 'next_action', sio.next_action() )

def connect_npc( url, username, npc ):
    def handle_msg( data ):
        if data[ 'status' ] == 'ok':
            print( 'User', username, 'connected to NPC', npc )
        else:
            msg = 'Error connecting user ' +  username + ' to NPC ' + npc
            msg += '. Status: ' + data[ 'status' ]
            sio.disconnect()
            raise IOError( msg )
    
    def send_msg( username, npc ):
        sio.npccallback = lambda x: handle_msg( x )
        sio.emit('connect_npc', {'username': username, 'npc':npc } )
        
    sio.connectcallback = lambda: send_msg( username, npc )
    sio.connect( url )
    


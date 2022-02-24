#!/usr/bin/env python3

import client

agent = 'stef'
server = 'http://dragon.foi.hr:5000'
user = 'babaroga'


from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import argparse

def train( bot ):
    chatbot = ListTrainer( bot )
	
    bot.set_trainer( ListTrainer )
    chatbot = bot

    chatbot.train([
	    "Hej",
	    "Hej! Tko si ti?"
        ])

    chatbot.train([
	    "Bok",
	    "Hej! Tko si ti?"
        ])

    chatbot.train([
	    "Pozdrav",
	    "Hej! A tko si ti?"
        ])

    chatbot.train([
	    "Kako se zoveš?",
	    "Štefek!!"
        ])

    chatbot.train([
	    "A ti?",
	    "Ja sam Štefek!!"
        ])



'''
0 - listening
1 - mention detected, answer
'''
state = 0
last_seen = -1
msgs = []

def next_action():
    global state, bot, msgs, last_seen
    if state == 0:
        return { 'action':'none', 'params':'nil' }
    elif state == 1:
        res = msgs[ last_seen ]
        res = res.replace( '@%s' % agent, '' )
        msg = str( bot.get_response( res ) )
        print( res, msg )
        return { 'action':'chat', 'params':msg }

def adjust( status ):
    global state, msgs, last_seen
    #print( status.data )
    msgs = status.data[ 'chat' ]
    if state == 0:
        ln = len( msgs ) - 1
        if last_seen < ln:
            last_seen = ln
            if '@%s' % agent in msgs[ last_seen ]:
                state = 1
    elif state == 1:
        state = 0
    
client.sio.next_action = next_action
client.sio.status_callback = adjust

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument( "--train", const=True, nargs='?', type=bool, help="Specify if the agent shoud be trained. If not specified the next argument will be considered." )
    
    args = parser.parse_args()
    
    TRAIN = bool( args.train )

    bot = ChatBot( 'Talker', logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'threshold': 0.85,
            'default_response': 'O čemu ti pričaš?'
        }], read_only=not TRAIN, database_uri='sqlite:///talker.sqlite3' )
    
    if TRAIN:
        train( bot )
    else:
        client.connect_npc( server, user, agent )



#!/usr/bin/env bash
echo "Killing all existing instances and more >:)"

killall python3
killall node
killall rethinkdb

echo "Starting database ..."

cd server

screen -d -m rethinkdb

sleep 3

echo "Done!"

echo "Starting MMO server ..."

screen -d -m node mmo.js

sleep 3

echo "Done!"

echo "Starting AIWorld server ..."

cd ../srv

screen -d -m ./server.py --rest

cd ..

sleep 3

echo "Done!"

echo "Everything up and ready, you can now start the game!"

# AI World

## Installation Before Running the Project

Before running the project, [RethinkDB](https://rethinkdb.com) must be installed:

```bash
source /etc/lsb-release && echo "deb https://download.rethinkdb.com/repository/ubuntu-$DISTRIB_CODENAME $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb
```

Then, add the following lines into the RPG Maker's `index.html` file, before `pixi.js` is included:

```html
<script type="text/javascript" src="js/libs/socket.io.js"></script>
<script type="text/javascript" src="js/libs/jquery.js"></script>
```

Make sure the referenced files (`socket.io.js` and `jquery.js`) are present at the defined paths. If they are not, use the following commands within this folder:

```bash
wget -O js/libs/socket.io.js https://raw.githubusercontent.com/socketio/socket.io/main/client-dist/socket.io.min.js
wget -O js/libs/jquery.js https://code.jquery.com/jquery-3.6.4.min.js
```

## Running the Project

First, in the folder `server` run:

```bash
rethinkdb
```

Then, in the same folder, run the following to install all the necessary modules.

```bash
npm install
```

Next, in the same folder, run the following command to start the MMO server.

```bash
node mmo.js
```

Lastly, in the folder `srv` run:

```bash
./server.py --rest
```

If all of the above are running, and produced no errors, the game can be run from RPG Maker or similar.

### Alternately

You can try running the `start_servers.sh` script.

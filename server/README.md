# AI World

## Installation Before Running the Project

Before running the project, [RethinkDB](https://rethinkdb.com) must be installed:

```bash
source /etc/lsb-release && echo "deb https://download.rethinkdb.com/repository/ubuntu-$DISTRIB_CODENAME $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/repository/raw/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb
```

Then, add the following lines into the RPG Maker's `index.html` file, before `pixi.js` is included (make sure the referenced files are present at the defined paths):

```html
<script type="text/javascript" src="js/libs/socket.io.js"></script>
<script type="text/javascript" src="js/libs/jquery.js"></script>
```

## Running the Project

First, in the folder `server` run:

```bash
rethinkdb
```

Then, in the same folder, run:

```bash
node mmo.js
```

Lastly, in the folder `srv` run:

```bash
./server.py --rest
```

The game can be run from RPG Maker or similar.

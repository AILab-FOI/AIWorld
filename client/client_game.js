var eventno = 3;
var eventname = 'ivek';
let xhr = new XMLHttpRequest();
xhr.open('GET', getLocation() + 'next/' + eventname, false);
xhr.send();
var ans = JSON.parse( xhr.response )

var action = 0;
switch( ans[ 'action' ] ){
case 'img':
    action = 2;
    break;
case 'msg':
    action = 3;
    break;
case 'choice':
    action = 4;
    break;
case 'left':
    action = 5;
    break;
case 'right':
    action = 6;
    break;
case 'up':
    action = 7;
    break;
case 'down':
    action = 8;
    break;
case 'gold':
    action = 9;
    break;
case 'chat':
    MMO_Core.sendMessage( eventname + ' says: ' + ans[ 'params' ]);
    break;
}
$gameVariables.setValue( eventno + 7, action )
$gameVariables.setValue( eventno + 17, ans[ 'params' ] );
//-------------------

var eventno = 3;
var eventname = 'ivek';
var x = $gameMap.event( eventno ).x;
var y = $gameMap.event( eventno ).y;
var px = $gamePlayer.x;
var py = $gamePlayer.y;
var chat = document.querySelector("#chatbox_box").innerText.split( '\n' );
var status = { x:x, y:y, playerx:px, playery:y, chat:chat };
let xhr = new XMLHttpRequest();
xhr.open('GET', getLocation() + 'feedback/' + eventname + '/' + encodeURIComponent( JSON.stringify( status ) ), false);
xhr.send();
var ans = JSON.parse( xhr.response )
//--------------------

var eventno = 3;
var eventname = 'ivek';
var choices = $gameVariables.value( eventno + 17 )[ 'choices' ];
$gameMessage.setBackground( 1 );
$gameMessage.setPositionType( 2 );
$gameMessage.add( $gameVariables.value( eventno + 17 )[ 'msg' ] )
$gameMessage.setChoices( choices, 0, -1 );
$gameMessage.setChoiceCallback(function(responseIndex) {
    var x = $gameMap.event( eventno ).x;
    var y = $gameMap.event( eventno ).y;
    var px = $gamePlayer.x;
    var py = $gamePlayer.y;
    var chat = document.querySelector("#chatbox_box").innerText.split( '\n' );
    var status = { x:x, y:y, playerx:px, playery:y, chat:chat };
    status[ 'answer' ] = $gameVariables.value( eventno + 17 )[ 'choices' ][ responseIndex ]
    let xhr = new XMLHttpRequest();
    xhr.open('GET', getLocation() + 'feedback/' + eventname + '/' + encodeURIComponent( JSON.stringify( status ) ), false);
    xhr.send();
    var ans = JSON.parse( xhr.response )
} );
this.setWaitMode( 'Choose:' );

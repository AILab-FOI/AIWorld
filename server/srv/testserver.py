from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send, emit, Namespace
import argparse
import sys
import datetime

from planner import Planner

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


def log_content(data, msg_type=None, author=None):
    """Log data.

    Parameters
    ----------
    data : type
        Data to be logged.
    msg_type : type
        Type of the logged data, n/a yet.
    author : type
        Author of the logged data.

    """
    print(f'Log by {author} T{msg_type}: {data}')


def decode_action_name(action):
    if action == 'get_gold':
        return '$gameParty.gainGold({})'


def decode_plan(plan):
    decoded_plan = []
    for name, parameters in plan:
        action = decode_action_name(name)
        decoded_plan.append(action.format(parameters))

    return decoded_plan


# @socketio.on('message')
# def handle_message(data):
#     print(f'received message: {data}')
#
#
# @socketio.event
# def connect():
#     print('Client connected!')
#
#
# @socketio.event
# def disconnect():
#     print('Client DISconnected!')
#
#
# @socketio.on('json')
# def handle_json(json):
#     print('received json: ' + str(json))
#
#


@socketio.on('newevent')
def log_event(data):
    print(f'Client ran the event! {data}')
    emit('newresponse',
         {'data': f'Response message is {datetime.datetime.now()}'})
    emit('disconnect')


class PDDLPlanning(Namespace):
    """Namespace for all things PDDL."""

    def on_connect(self):
        self.engine = Planner()
        print('Client connected.')

    def on_disconnect(self):
        print('Client disconnected.')

    def on_makeplan(self, domain: str, problem: str):
        """Make a plan based on `domain` that solves `problem`.

        Parameters
        ----------
        domain : str
            Domain of the problem. Can be listed in a string, or a file path.
        problem : str
            Domain of the problem. Can be listed in a string, or a file path.
        """
        log_content(f'Domain: {domain}\nProblem: {problem}')
        try:
            solution = self.engine.solve(domain, problem)
            log_content(solution)
            plan = [f'{action.name}{action.parameters}' for action in solution]
            plan = decode_plan(solution)
            emit('deliverplan',
                 {
                    'plan': plan
                 })
            emit('disconnect')
        except Exception as ex:
            emit('disconnect')
            raise ex

    def on_decode_plan(self, plan):
        """Receive a plan and store it."""
        log_content(plan)
        actions = []


socketio.on_namespace(PDDLPlanning('/plan'))

# emit('connect', {'data': 'Connected'})
#
#
# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')
#
#
# @socketio.event
# def newevent(data):
#     print(f'Received data: {data}')
#     emit('newresponse', data)
#     return {'response': True}
#
#
# class TestNamespace(Namespace):
#     def on_connect(self):
#         print('Client connected.')
#
#     def on_disconnect(self):
#         print('Client DISconnected.')
#
#     def on_newevent(self, data):
#         print(data)
#         emit('newresponse', data)
#
#
# socketio.on_namespace(TestNamespace('/test'))
#
#


@app.route('/')
def index():
    return render_template('jedan.html')


@app.route('/planner')
def planiranje():
    return render_template('dva.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rest",
        const=True,
        nargs='?',
        type=bool,
        help="Specify if the agent shoud be start as a RESTful server.")
    parser.add_argument(
        "--debug",
        const=True,
        nargs='?',
        type=bool,
        help="Specify if the agent shoud be start in debug mode.")
    args = parser.parse_args()

    REST = bool(args.rest)

    if REST:
        socketio.run(app, host="0.0.0.0", debug=args.debug)
        sys.exit()
    # socketio.run(app, host="localhost", debug=args.debug, port="5005")
    # sys.exit()

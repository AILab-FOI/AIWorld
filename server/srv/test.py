aString = "jedan ({})"
aString.format('dva')

# %%


class Action():
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters


solution = [
    Action(
        'get_gold',
        [100]
    ),
    Action(
        'receive',
        ['gold', 200]
    ),
    Action(
        'receive',
        [
            'item',  # object type
            12,  # object ID
            1  # quantity
        ]
    ),
    Action(
        'receive',
        ['weapon', 1, 2]
    ),
    Action(
        'lose',
        ['gold', 100]
    ),
    Action(
        'lose',
        ['item', 12, 1]
    ),
    Action(
        'move',
        [
            14,  # x coordinate
            73  # y coordinate
        ]
    ),
    Action(
        'say',
        [
            'Actor1',  # name of the faceset to use
            0,  # index of face
            2,  # position on screen
            "You shall\nnot pass!",  # text to be shown
        ]
    ),
]

action_dictionary = {
    'get_gold': '$gameParty.gainGold({});',
    'receive_gold': '$gameParty.gainGold({});',
    'receive_item': '$gameParty.gainItem($dataItems[{}], {});',
    'receive_weapon': '$gameParty.gainItem($dataWeapons[{}], {});',
    'lose_gold': '$gameParty.loseGold({});',
    'lose_item': '$gameParty.loseItem($dataItems[{}], {});',
    'say': '$gameMessage.setFaceImage("{}", {}); $gameMessage.setBackground(0); $gameMessage.setPositionType({}); $gameMessage.add("{}"); this.setWaitMode("message");',
    'move': '',
}


def build_command(action):
    """Build action template waiting to be filled with parameter values."""
    command = action_dictionary.get(action.name)
    decoded_action = command.format(*action.parameters)

    return decoded_action


def rebuild_action_name(action):
    """Remake action name to be more specific, based on the first parameter."""
    action.name = '_'.join([action.name, action.parameters.pop(0)])

    return action


def decode_action(action):
    """Replace a single plan action name with applicable RPGMaker command."""
    if action.name == 'get_gold':
        action = build_command(action)

    elif action.name == 'say':
        action = build_command(action)

    elif action.name == 'receive':
        action = rebuild_action_name(action)
        action = build_command(action)

    elif action.name == 'lose':
        action = rebuild_action_name(action)
        action = build_command(action)

    return action


def decode_plan(plan):
    """Convert a PDDL plan into a list of RPGMaker commands."""
    decoded_plan = []
    for action in plan:
        action = decode_action(action)
        decoded_plan.append(action)

    return decoded_plan


decode_plan(solution)

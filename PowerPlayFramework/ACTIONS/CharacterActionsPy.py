# # Minimal Action System
# - Given a Character and a context, it must be possible to list possible Actions for that Character.
# - Given a Character, an Action and a context, it must be possible to find if the Action can be taken.
# - Given a Character, an Action and a context, it must be possible to take it and have it affect the game (e.g. changing player stats; advancing the time; changing an NPCs state).
# - Given a Character and an Action it must be possible to retrieve the Description of the Action or a Description of its result.

## DEPENDENCIES: Character

def default_get_possible_actions(context, character):
    return Character_Action.index_of_actions_ids

def default_execute_action(character_action, character, context):
    if character_action.execution_description is not None:
        if character_action.execution_description.action_description_kind is Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__FUNCTION:
            action_description = character_action.execution_description.action_description(character_action, character, context)
        else:
            action_description = character_action.execution_description.action_description
    else:
        action_description = None
    character_action.execute(character, context)
    if character_action.result_description is not None:
        if character_action.result_description.action_description_kind is Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__FUNCTION:
            result_description = character_action.result_description.action_description(character_action, character, context)
        else:
            result_description = character_action.result_description.action_description
    else:
        result_description = None
    if action_description is not None:
        print(action_description)
    if result_description is not None:
        print(result_description)

def register_in_database(character_action):
    Character_Action.index_of_actions_ids[character_action.id] = character_action

class Character_Action_Description(object):
    ENUM__ACTION_DESCRIPTION_KINDS__TEXT = "TEXT"
    ENUM__ACTION_DESCRIPTION_KINDS__FUNCTION = "FUNCTION"
    ENUM__ACTION_DESCRIPTION_KINDS__LABEL = "LABEL"
    def __init__(self, action_description, action_description_kind = ENUM__ACTION_DESCRIPTION_KINDS__TEXT):
        self.action_description_kind = action_description_kind
        self.action_description = action_description # if it is a function: action_description(action, character, context)

class Character_Action(object):
    index_of_actions_ids = {}
    get_possible_actions_default_function = default_get_possible_actions
    execute_action_default_function = default_execute_action
    def __init__(self, id):
        self.id = id
        self.check_action_is_possible_function = None # check_action_is_possible_function(action, character, context)
        self.execution_function = None # execution_function(action, character, context)
        self.player_menu_description = None
        self.execution_description = None
        self.result_description = None
    
    def check_action_is_possible(self, character, context):
        if self.check_action_is_possible_function is None:
            return True
        else:
            return self.check_action_is_possible_function(self, character, context)

    def execute(self, character, context):
        if self.execution_function is not None:
            return self.execution_function(self, character, context)

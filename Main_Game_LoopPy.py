# - Examine Self
# - Go to a location
# - Look for a Known Character
# - Start an Activity
# - Start an Interaction
# - Take an Action
# 
# # Examine Self
# - SELF EXPLANATORY
# 
# # Go to a Location
# - Change POV Location
# - List Characters at Location
# - List Actions at Location
# - List Activities at Location
# - List Locations accessible from this Location
# - List Locations discovered from this Location
# 
# # Look for a Known Character
# - Get Character's current Location
# - Get Character's current Activity
# - List possible Interactions with Character
# 
# # Start an Activity
# - Describe Activity execution
# - Get Duration
# - Start Interruption, if any
# - Describe Consequence of Activity
# - Update Characters involved in Activity
# 
# # Start an Interaction
# - Select Targets
# - List Actions for this Interaction
# - Start Interruption, if any
# - Finish Interaction
# - Produce Interaction Report
# - Update all Characters involved in the Interaction
# 
# # Take an Action
# - Select Targets, if any
# - Describe Action execution
# - Describe Consequence of Activity
# - Describe Targets' Reactions
# - Update all Characters involved in the Action

import PowerPlayFramework.CHARACTERS_BASE.CharactersPy as Characters
import PowerPlayFramework.NAMES.NamesPy as Names
import PowerPlayFramework.ACTIONS.CharacterActionsPy as Actions
import PowerPlayFramework.LOCATIONS.LocationsPy as Locations
import PowerPlayFramework.GAME_SCENES.Game_ScenesPy as Game_Scenes

GLOBAL_DEBUG_FLAG = True

class Game_System(object):
    def __init__(self):
        self.protagonist = None
        self.characters_database = None
        self.locations_database = None
    
    def initialize(self):
        pass

class Game_Base(object):
    registered_scenes = {}
    def __init__(self, default_scene):
        self.default_scene = default_scene
        self.stop_game = False
    
    def initialize(self):
        pass

    def register_scene(self, scene_object):
        Game_Base.registered_scenes[scene_object.scene_id] = scene_object
    
    def game_loop_start(self):
        self._loop_start_updates()
        game_scene = self.select_next_scene()
        if game_scene is not None:
            self._start_scene(game_scene)
            return
        else:
            self._start_scene(self.default_scene)
        return

    def game_loop_handle_input(self):
        pass

    def game_loop_end(self):
        self._loop_end_updates()
        pass

    def _loop_start_updates(self):
        pass

    def select_next_scene(self):
        for scene_key in Game_Base.registered_scenes.keys():
            return Game_Base.registered_scenes[scene_key]

    def _loop_end_updates(self):
        pass

    def _start_scene(self, scene_object):
        scene_object.status = Game_Scenes.ABSTRACT_Game_Scene.READY_TO_START
        while scene_object.status is not Game_Scenes.ABSTRACT_Game_Scene.FINISHED:
            scene_object.run()

## SCENES

class PurePython_Game_Scene(Game_Scenes.ABSTRACT_Game_Scene):
    def __init__(self):
        super(PurePython_Game_Scene, self).__init__()
    
    def _present(self, presentation_function):
        presentation_function(self)
    
    def _get_player_input(self, input_function):
        input_function(self)

def DEFAULT_SECENE_before(context):
    context.loop_count = 0

def DEFAULT_SECENE_update(context):
    context.loop_count += 1
    if context.loop_count > 1:
        context.interrupt_scene()

player_action_options = dict()

def DEFAULT_SECENE_presentation(context):
    # Present current location
    if system.protagonist.location is None:
        print("[@] You are NOWHERE!!!")
    else:
        print("[@] You are " + system.protagonist.location.in_or_at + " " + system.protagonist.location.short_name)
    # List local characters perceived
    print("[@] There is no one else here.")
    # print("[@] These are the people here: ...")
    # Ask for Action
    global player_action_options
    player_action_options = dict()
    possible_actions = Actions.Character_Action.get_possible_actions_default_function(None, system.protagonist)
    actions_count = 0
    print("[@] These are your options: ...")
    sorted_keys = list(possible_actions.keys())
    sorted_keys.sort()
    for possible_action_key in sorted_keys:
        description_object = possible_actions[possible_action_key].player_menu_description
        if description_object.action_description_kind is Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__FUNCTION:
            text = description_object.action_description(possible_actions[possible_action_key], system.protagonist, context)
        else:
            text = description_object.action_description
        input_number = -1
        if possible_action_key is not quit_game.id:
            input_number = actions_count
            actions_count += 1
        else:
            input_number = 999
        print("[{0}] - {1}".format(input_number, text))
        player_action_options[str(input_number)] = possible_action_key


def DEFAULT_SECENE_input_processing(context):
    print("What do you want to do?")
    player_input = input("> ")
    if player_input in player_action_options.keys():
        character_action = Actions.Character_Action.index_of_actions_ids[player_action_options[player_input]]
        Actions.Character_Action.execute_action_default_function(character_action, system.protagonist, context)
    return player_input

DEFAULT_SECENE = PurePython_Game_Scene()
DEFAULT_SECENE.should_run_function = lambda: True
DEFAULT_SECENE.before_run_function = DEFAULT_SECENE_before
DEFAULT_SECENE.scene_start_presentation = DEFAULT_SECENE_presentation
DEFAULT_SECENE.scene_update_function = DEFAULT_SECENE_update
DEFAULT_SECENE.scene_player_input_processing_function = DEFAULT_SECENE_input_processing
DEFAULT_SECENE.scene_update_presentation = None
DEFAULT_SECENE.after_run_function = None
DEFAULT_SECENE.scene_end_presentation = None

def should_run_introduction(introduction_scene):
    if "ran_once" not in introduction_scene.__dir__() or introduction_scene.ran_once is None or introduction_scene.ran_once is False:
        return True
    else:
        return False

def after_run_introduction(introduction_scene):
    introduction_scene.ran_once = True
    Game_Base.registered_scenes.pop(introduction_scene.scene_id)

def introduction_scene_presentation(context = None):
    print("\tThis is what a presentation could look like.")
    print("\tAnd here is a second line as an example.")

def introduction_scene_update(context):
    context.interrupt_scene()

introduction = PurePython_Game_Scene()
introduction.should_run_function = should_run_introduction
introduction.before_run_function = None
introduction.scene_start_presentation = introduction_scene_presentation
introduction.scene_update_function = introduction_scene_update
introduction.scene_player_input_processing_function = None
introduction.scene_update_presentation = None
introduction.after_run_function = after_run_introduction
introduction.scene_end_presentation = None

## CHARACTERS
prot_name = Names.Character_Names()
prot_name.individual_name = "Blake"
prot_name.family_name = "Dancer"
prot_name.standard = "Bly"
protagonist = Characters.Character("PROTAGONIST", prot_name, "MALE", 25)

## ACTIONS

def examine_self_action(character_action, character, context):
    return Characters.Character.examine_character_default_function(system.protagonist)

examine_self = Actions.Character_Action("SIMPLER_TESTER__Examine_Self")
examine_self.player_menu_description = Actions.Character_Action_Description(action_description = "Examine self", action_description_kind = Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__TEXT)
examine_self.execution_description = Actions.Character_Action_Description(action_description = "You look at yourself.", action_description_kind = Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__TEXT)
examine_self.result_description = Actions.Character_Action_Description(action_description = examine_self_action, action_description_kind = Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__FUNCTION)
Actions.register_in_database(examine_self)

def quit_game_action(character_action, character, context):
    game.stop_game = True

quit_game = Actions.Character_Action("SIMPLER_TESTER__Quit_Game")
quit_game.player_menu_description = Actions.Character_Action_Description(action_description = "QUIT the GAME", action_description_kind = Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__TEXT)
quit_game.execution_function = quit_game_action
Actions.register_in_database(quit_game)

## LOCATIONS

unending_void = Locations.Location("SIMPLER_TESTER__Unending_Void", in_or_at = "in an", short_name = "Unending Void")
unending_void.short_descriptor = "Emptiness infinite."

protagonist.location = unending_void

def powerPlayFramework_initialize():
    global system
    system = Game_System()
    system.initialize()
    system.protagonist = protagonist
    game_initialize()

def game_initialize():
    global game
    game = Game_Base(DEFAULT_SECENE)
    game.initialize()
    game.register_scene(introduction)

print("[+] Initializing game...")
powerPlayFramework_initialize()
print("[+] Game initialized...")
#print(Characters.Character.examine_character_default_function(system.protagonist))
while not game.stop_game:
    game.game_loop_start()
    game.game_loop_handle_input()
    game.game_loop_end()

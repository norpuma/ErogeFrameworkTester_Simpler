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

class Object(object):
    pass

class Game_System(object):
    def __init__(self):
        self.protagonist = None
        self.characters_database = None
        self.locations_database = None
    
    def initialize(self):
        pass

class Game_Base(object):
    registered_scenes = {}
    def __init__(self, active_scene_creator_function, default_scene = None):
        self.active_scene_creator_function = active_scene_creator_function
        self.default_scene = default_scene
        self.stop_game = False
        self.active_scenes_stack = []
        self.active_scene = None
    
    def initialize(self):
        pass

    def register_scene(self, scene_object):
        Game_Base.registered_scenes[scene_object.scene_id] = scene_object
    
    def game_loop(self):
        if self.stop_game == True:
            return
        if self._check_for_scene_interruption() == True:
            self._interrupt_scene_with_another(self._select_next_active_scene())
        if self.active_scene is None:
            self.active_scene = self._select_next_active_scene()
            return
        if self.active_scene.status == Game_Scenes.ABSTRACT_Active_Scene_Reference.FINISHED:
            self._finish_scene(self.active_scene)
            self.active_scene = self._select_next_active_scene()
            return
        elif self.active_scene.status == Game_Scenes.ABSTRACT_Active_Scene_Reference.WAITING_FOR_NEXT_SCENE:
            self.inject_scene(self.active_scene.next_scene_id, self.active_scene.scene_context)
            return
        else: # All other active scene statuses
            self.active_scene.run()

    def _check_for_scene_interruption(self):
        if len(self.active_scenes_stack) < 1:
            return False
        candidate_scene = self.active_scenes_stack[-1]
        if self.active_scene is not candidate_scene:
            return True
        else:
            return False

    def _interrupt_scene_with_another(self, candidate_scene):
        if self.active_scene is not None and self.active_scene.status != Game_Scenes.ABSTRACT_Active_Scene_Reference.FINISHED:
            self.active_scene.set_scene_switch(candidate_scene.referred_scene.scene_id)
        self.active_scene = candidate_scene

    def _get_previous_context(self):
        if len(self.active_scenes_stack) >= 2:
            previous_context = self.active_scenes_stack[-2].scene_context
        else: 
            previous_context = None
        return previous_context
    
    def _finish_scene(self, active_scene):
        self.active_scenes_stack.remove(active_scene)
    
    def inject_scene(self, next_scene_id, previous_context):
        next_scene = Game_Base.registered_scenes[next_scene_id]
        new_active_scene = self.active_scene_creator_function(next_scene, previous_context)
        self.active_scenes_stack.append(new_active_scene)

    def _select_next_active_scene(self):
        if len(self.active_scenes_stack) < 1:
            if self.default_scene is None:
                self.stop_game = True
                return None
            else:
                previous_context = None
                if self.active_scene is not None:
                    previous_context = self.active_scene.scene_context
                self.inject_scene(self.default_scene.scene_id, previous_context)
        return self.active_scenes_stack[-1]

## SCENES

class PurePython_Game_Scene(Game_Scenes.ABSTRACT_Active_Scene_Reference):
    def __init__(self, referred_scene, scene_context):
        super(PurePython_Game_Scene, self).__init__(referred_scene, scene_context)
    
    def _present(self, presentation_function):
        presentation_function(self, self.scene_context)
    
    def _get_player_input(self, input_function):
        input_function(self, self.scene_context)

def active_scene_creator(new_scene, previous_context):
    reference_scene = Game_Base.registered_scenes[new_scene.scene_id]
    return PurePython_Game_Scene(reference_scene, previous_context)

player_action_options = dict()

def DEFAULT_SCENE_prepare_scene_and_create_context(game_scene, previous_context):
    new_context = Object()
    new_context.scene_changed = False
    return new_context

def DEFAULT_SCENE_presentation(game_scene, context):
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


def DEFAULT_SCENE_input_processing(game_scene, context):
    print("What do you want to do?")
    player_input = input("> ")
    if player_input in player_action_options.keys():
        character_action = Actions.Character_Action.index_of_actions_ids[player_action_options[player_input]]
        Actions.Character_Action.execute_action_default_function(character_action, system.protagonist, context)
    return player_input

def DEFAULT_SCENE_update_presentation(game_scene, context):
    if context.scene_changed:
        DEFAULT_SCENE_presentation(context)

DEFAULT_SCENE = Game_Scenes.Game_Scene("SIMPLER_TESTER__Default_Scene")
DEFAULT_SCENE.should_run_function = lambda: True
DEFAULT_SCENE.prepare_scene_and_create_context_function = DEFAULT_SCENE_prepare_scene_and_create_context
DEFAULT_SCENE.scene_start_presentation = DEFAULT_SCENE_presentation
DEFAULT_SCENE.scene_update_function = None
DEFAULT_SCENE.scene_player_input_processing_function = DEFAULT_SCENE_input_processing
DEFAULT_SCENE.scene_update_presentation = DEFAULT_SCENE_update_presentation
DEFAULT_SCENE.after_run_function = None
DEFAULT_SCENE.scene_end_presentation = None

def should_run_introduction(introduction_scene):
    if "ran_once" not in introduction_scene.__dir__() or introduction_scene.ran_once is None or introduction_scene.ran_once is False:
        return True
    else:
        return False

def introduction_scene_presentation(game_scene, context):
    print("\tThis is what a presentation could look like.")
    print("\tAnd here is a second line as an example.")

def introduction_scene_update(game_scene, context):
    game_scene.interrupt_scene()

introduction = Game_Scenes.Game_Scene("SIMPLER_TESTER__Introduction")
introduction.should_run_function = should_run_introduction
introduction.scene_start_presentation = introduction_scene_presentation
introduction.scene_update_function = introduction_scene_update
introduction.scene_player_input_processing_function = None
introduction.scene_update_presentation = None
introduction.after_run_function = None
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
    game = Game_Base(active_scene_creator, DEFAULT_SCENE)
    game.initialize()
    game.register_scene(DEFAULT_SCENE)
    game.register_scene(introduction)
    game.inject_scene(introduction.scene_id, None)

print("[+] Initializing game...")
powerPlayFramework_initialize()
print("[+] Game initialized...")
#print(Characters.Character.examine_character_default_function(system.protagonist))
while not game.stop_game:
    game.game_loop()

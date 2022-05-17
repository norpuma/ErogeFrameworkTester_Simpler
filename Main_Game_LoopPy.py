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
from PowerPlayFramework.CHARACTERS_BASE.FundamentalsPy import Age_Group
import PowerPlayFramework.NAMES.NamesPy as Names
import PowerPlayFramework.ACTIONS.CharacterActionsPy as Actions
import PowerPlayFramework.LOCATIONS.LocationsPy as Locations
import PowerPlayFramework.GAME_SCENES.Game_ScenesPy as Game_Scenes

import random

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
        if self.active_scene is not None and self.active_scene.status != Game_Scenes.ABSTRACT_Active_Scene_Reference.FINISHED and self.active_scene.status != Game_Scenes.ABSTRACT_Active_Scene_Reference.WAITING_FOR_NEXT_SCENE:
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
        next_active_scene = self._select_next_active_scene()
        if next_active_scene is not None and next_active_scene.status == Game_Scenes.ABSTRACT_Active_Scene_Reference.WAITING_FOR_NEXT_SCENE:
            next_active_scene.resume_after_scene_switch(active_scene.scene_context)
    
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

def DEFAULT_SCENE_prepare_scene_and_create_context(game_scene, previous_context):
    new_context = Object()
    new_context.scene_changed = False
    new_context.switch_scene_new_scene_id = None
    new_context.player_action_options = dict()
    return new_context

def DEFAULT_SCENE_possible_player_options_presentation(context):
    context.player_action_options = dict()
    possible_actions = Actions.Character_Action.get_possible_actions_default_function(None, system.protagonist)
    actions_count = 0
    print("[@] These are your options:")
    for possible_action_key in possible_actions.keys():
        if possible_action_key is quit_game.id:
            continue
        description_object = possible_actions[possible_action_key].player_menu_description
        if description_object.action_description_kind is Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__FUNCTION:
            text = description_object.action_description(possible_actions[possible_action_key], system.protagonist, context)
        else:
            text = description_object.action_description
        print("  [{0}] - {1}".format(actions_count, text))
        context.player_action_options[str(actions_count)] = possible_action_key
        actions_count += 1

    if quit_game.id in possible_actions.keys():
        possible_action_key = quit_game.id
        description_object = possible_actions[possible_action_key].player_menu_description
        if description_object.action_description_kind is Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__FUNCTION:
            text = description_object.action_description(possible_actions[possible_action_key], system.protagonist, context)
        else:
            text = description_object.action_description
        actions_count = 999
        print("  [{0}] - {1}".format(actions_count, text))
        context.player_action_options[str(actions_count)] = quit_game.id

def DEFAULT_SCENE_presentation(game_scene, context):
    if system.protagonist.location is None:
        print("[@] You are NOWHERE!!!")
    else:
        print("[@] You are " + system.protagonist.location.in_or_at + " " + system.protagonist.location.short_name)
    # List local characters perceived
    print("[@] There is no one else here.")
    # print("[@] These are the people here: ...")
    DEFAULT_SCENE_possible_player_options_presentation(context)


def DEFAULT_SCENE_input_processing(game_scene, context):
    print("What do you want to do?")
    player_input = input("> ")
    if player_input in context.player_action_options.keys():
        character_action = Actions.Character_Action.index_of_actions_ids[context.player_action_options[player_input]]
        Actions.Character_Action.execute_action_default_function(character_action, system.protagonist, context)
    else:
        print("ERROR: Unknown option. Please select a valid option.")
    return player_input

def DEFAULT_SCENE_update(game_scene, context):
    if context.switch_scene_new_scene_id is not None:
        context.actor = system.protagonist
        game_scene.set_scene_switch(context.switch_scene_new_scene_id)

def DEFAULT_SCENE_update_presentation(game_scene, context):
    if context.scene_changed:
        DEFAULT_SCENE_presentation(game_scene, context)

def DEFAULT_SCENE_resume_after_scene_switch(current_context, game_scene_id, context):
    if game_scene_id == "SIMPLER_TESTER__Travel_to_Location" and context.location_changed:
        current_context.scene_changed = True
    else:
        DEFAULT_SCENE_possible_player_options_presentation(context)

DEFAULT_SCENE = Game_Scenes.Game_Scene("SIMPLER_TESTER__Default_Scene")
DEFAULT_SCENE.prepare_scene_and_create_context_function = DEFAULT_SCENE_prepare_scene_and_create_context
DEFAULT_SCENE.scene_start_presentation = DEFAULT_SCENE_presentation
DEFAULT_SCENE.scene_update_function = DEFAULT_SCENE_update
DEFAULT_SCENE.scene_player_input_processing_function = DEFAULT_SCENE_input_processing
DEFAULT_SCENE.scene_update_presentation = DEFAULT_SCENE_update_presentation
DEFAULT_SCENE.resume_after_scene_switch_function = DEFAULT_SCENE_resume_after_scene_switch
DEFAULT_SCENE.after_run_function = None
DEFAULT_SCENE.scene_end_presentation = None

def introduction_scene_presentation(game_scene, context):
    print("\tThis is what a presentation could look like.")
    print("\tAnd here is a second line as an example.")

def introduction_scene_update(game_scene, context):
    game_scene.interrupt_scene()

introduction = Game_Scenes.Game_Scene("SIMPLER_TESTER__Introduction")
introduction.scene_start_presentation = introduction_scene_presentation
introduction.scene_update_function = introduction_scene_update
introduction.scene_player_input_processing_function = None
introduction.scene_update_presentation = None
introduction.after_run_function = None
introduction.scene_end_presentation = None

def travel_to_location_prepare_scene_and_create_context(game_scene, previous_context):
    new_context = Object()
    new_context.player_action_options = dict()
    new_context.actor = previous_context.actor
    new_context.possible_destination_ids = Locations.Location.reachable_locations_default_function(new_context.actor, new_context)
    new_context.location_changed = False
    return new_context

def travel_to_location_scene_presentation(game_scene, context):
    options_count = 0
    for possible_destination_id in context.possible_destination_ids:
        if context.actor.location.id != possible_destination_id:
            location = Locations.Location.locations_database[possible_destination_id]
            text = location.short_name
            print("  [{0}] - {1}".format(options_count, text))
            context.player_action_options[str(options_count)] = possible_destination_id
            options_count += 1
    options_count = 999
    print("  [{0}] - {1}".format(options_count, "Give up traveling and stay at current location."))
    context.player_action_options[str(options_count)] = None

def travel_to_location_scene_input_processing(game_scene, context):
    print("What is your destination?")
    player_input = input("> ")
    if player_input == str(999):
        game_scene.interrupt_scene()
        return None
    if player_input in context.player_action_options.keys():
        destination_id = context.player_action_options[player_input]
        context.actor.location = Locations.Location.locations_database[destination_id]
        context.location_changed = True
    else:
        print("ERROR: Unknown option. Please select a valid option.")
    game_scene.interrupt_scene()
    return player_input

travel_to_location_scene = Game_Scenes.Game_Scene("SIMPLER_TESTER__Travel_to_Location")
travel_to_location_scene.prepare_scene_and_create_context_function = travel_to_location_prepare_scene_and_create_context
travel_to_location_scene.scene_start_presentation = travel_to_location_scene_presentation
travel_to_location_scene.scene_player_input_processing_function = travel_to_location_scene_input_processing

def spawn_character_prepare_scene_and_create_context(game_scene, previous_context):
    new_context = Object()
    new_context.player_action_options = dict()
    new_context.new_character_names = None
    new_context.new_character_age = None
    new_context.new_character_age_group = None
    new_context.new_character_gender = None
    new_context.choice_context = "GENERAL"
    return new_context

def spawn_character_scene_presentation(game_scene, context):
    print("--------Character Creation--------")

def spawn_character_scene_update(game_scene, context):
    print("--------Character Update--------")

def spawn_character_scene_generate_display_name(names_object):
    if names_object is None:
        return "RANDOM 'RANDOM' McRANDOM"
    if names_object.first is None:
        first_name = "RANDOM"
    else:
        first_name = names_object.first
    if names_object.last is None:
        last_name = "RANDOM"
    else:
        last_name = names_object.last

    if names_object.standard is not None and names_object.first != names_object.standard:
        display_full_name = "{0} '{1}' {2}".format(first_name, names_object.standard, last_name)
    else:
        display_full_name = "{0} {1}".format(first_name, last_name)
    return display_full_name

def spawn_character_scene_character_details(game_scene, context):
    if context.new_character_gender is None:
        display_gender = "???"
    else:
        if context.new_character_gender == Characters.Gender.FEMALE:
            display_gender = "Female"
        else: # context.new_character_gender == Characters.Gender.MALE:
            display_gender = "Male"
    if context.new_character_age is None:
        display_age = "???"
    else:
        display_age = "{0} years old - {1}".format(context.new_character_age, context.new_character_age_group)

    display_full_name = spawn_character_scene_generate_display_name(context.new_character_names)

    print("  [0] Character Names: ", display_full_name)
    context.player_action_options[str(0)] = "CHANGE_NAMES"
    print("  [1] Character Age: ", display_age)
    context.player_action_options[str(1)] = "CHANGE_AGE"
    print("  [2] Character Gender: ", display_gender)
    context.player_action_options[str(2)] = "CHANGE_GENDER"
    print("  [99] Interrupt without spawning a character.")
    context.player_action_options[str(99)] = "CANCEL"
    print("  [00] Spawn character.")
    context.player_action_options["00"] = "SPAWN"

def spawn_character_scene_input_processing_for_general(game_scene, context, player_choice):
    if player_choice == "GENERAL":
        context.choice_context = "GENERAL"
    elif player_choice == "CHANGE_NAMES":
        context.choice_context = "CHANGE_NAMES"
    elif player_choice == "CHANGE_AGE":
        context.choice_context = "CHANGE_AGE"
    elif player_choice == "CHANGE_GENDER":
        context.choice_context = "CHANGE_GENDER"
    elif player_choice == "CANCEL":
        context.new_character = None
        game_scene.interrupt_scene()
    elif player_choice == "SPAWN":
        context.new_character = Characters.generate_random_character(id = None, gender = context.new_character_gender, age = context.new_character_age, names = context.new_character_names)
        game_scene.interrupt_scene()

def spawn_character_scene_names_options(game_scene, context):
    display_full_name =  spawn_character_scene_generate_display_name(context.new_character_names)
    print("    [@] ", display_full_name)
    display_individual_name = "RANDOM"
    if context.new_character_names is not None and context.new_character_names.individual_name is not None:
        display_individual_name = context.new_character_names.individual_name + " - leave blank for RANDOM"
    print("    [0] Change individual name ({0}).".format(display_individual_name))
    context.player_action_options[str(0)] = "CHANGE_INDIVIDUAL_NAME"
    display_family_name = "RANDOM"
    if context.new_character_names is not None and context.new_character_names.family_name is not None:
        display_family_name = context.new_character_names.family_name + " - leave blank for RANDOM"
    print("    [1] Change family name ({0}).".format(display_family_name))
    context.player_action_options[str(1)] = "CHANGE_FAMILY_NAME"

    display_standard_name = "RANDOM"
    if context.new_character_names is not None and context.new_character_names.standard is not None:
        display_standard_name = context.new_character_names.standard + " - leave blank for RANDOM"
    print("    [2] Change the name by which the character prefers to be called ({0}).".format(display_standard_name))
    context.player_action_options[str(2)] = "CHANGE_STANDARD_NAME"
    print("    [99] Back.")
    context.player_action_options[str(99)] = "BACK"
    print("    [00] Reset all to random names.")
    context.player_action_options["00"] = "RESET_NAMES"

def spawn_character_scene_input_processing_for_names__get_name():
    player_input = input("> ")
    name = player_input.strip()
    if len(name) < 1:
        name = None
    return name

def spawn_character_scene_input_processing_for_names(game_scene, context, player_choice):
    if context.new_character_names is None:
        context.new_character_names = Characters.Character_Names()
    if player_choice == "CHANGE_INDIVIDUAL_NAME":
        name = spawn_character_scene_input_processing_for_names__get_name()
        context.new_character_names.individual_name = name
    elif player_choice == "CHANGE_FAMILY_NAME":
        name = spawn_character_scene_input_processing_for_names__get_name()
        context.new_character_names.family_name = name
    elif player_choice == "CHANGE_STANDARD_NAME":
        name = spawn_character_scene_input_processing_for_names__get_name()
        context.new_character_names.standard = name
    elif player_choice == "BACK":
        context.choice_context = "GENERAL"
    elif player_choice == "RESET_NAMES":
        context.new_character_names = None
    
def spawn_character_scene_age_options(game_scene, context):
    if context.new_character_age is None:
        display_age = "???"
    else:
        display_age = "{0} years old - {1}".format(context.new_character_age, Characters.Age_Group.get_age_group_from_age(context.new_character_age))
    print("    [@] ", display_age)
    print("    [0] Set to a specific number (between {0} and {1}).".format(Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__TEEN], Characters.Age_Group.MAX_AGE))
    context.player_action_options[str(0)] = "CHANGE_AGE_TO_NUMBER"
    print("    [1] Set to a random value for a 'teenager' (between {0} and {1})".format(Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__TEEN], Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__YOUNG_ADULT]-1))
    context.player_action_options[str(1)] = "CHANGE_AGE_TO_TEENAGER_AGE_GROUP"
    print("    [2] Set to a random value for a 'young adult' (between {0} and {1})".format(Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__YOUNG_ADULT], Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__ADULT]-1))
    context.player_action_options[str(2)] = "CHANGE_AGE_TO_YOUNG_ADULT_AGE_GROUP"
    print("    [3] Set to a random value for a 'adult' (between {0} and {1})".format(Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__ADULT], Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__MATURE_ADULT]-1))
    context.player_action_options[str(3)] = "CHANGE_AGE_TO_ADULT_AGE_GROUP"
    print("    [4] Set to a random value for a 'mature adult' (between {0} and {1})".format(Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__MATURE_ADULT], Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__ELDER]-1))
    context.player_action_options[str(4)] = "CHANGE_AGE_TO_MATURE_ADULT_AGE_GROUP"
    print("    [5] Set to a random value for a 'elder' (between {0} and {1})".format(Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__ELDER], Characters.Age_Group.MAX_AGE))
    context.player_action_options[str(5)] = "CHANGE_AGE_TO_ELDER_AGE_GROUP"
    print("    [99] Back.")
    context.player_action_options[str(99)] = "BACK"
    print("    [00] Reset to a random number within accepted values.")
    context.player_action_options["00"] = "RESET_AGE"

def spawn_character_scene_input_processing_for_age_set_age_and_reset_input_context(context):
    context.new_character_age = Characters.Age_Group.generate_random_age(context.new_character_age_group)
    context.choice_context = "GENERAL"

def spawn_character_scene_input_processing_for_age(game_scene, context, player_choice):
    if player_choice == "CHANGE_AGE_TO_NUMBER":
        player_input = input("> ")
        try:
            age = int(player_input)
            if age < Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__TEEN]:
                print("ERROR: Valid ages are between {0} and {1}.".format(Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__TEEN], Characters.Age_Group.MAX_AGE))
            else:
                context.new_character_age = age
                context.new_character_age_group = Characters.Age_Group.get_age_group_from_age(context.new_character_age)
                context.choice_context = "GENERAL"
        except ValueError:
            print("ERROR: Unable to convert the value to an age between {0} and {1}.".format(Characters.Age_Group.min_age_by_age_group[Characters.Age_Group.ENUM__AGE_GROUP__TEEN], Characters.Age_Group.MAX_AGE))
    elif player_choice == "CHANGE_AGE_TO_TEENAGER_AGE_GROUP":
        context.new_character_age_group = Characters.Age_Group.ENUM__AGE_GROUP__TEEN
        spawn_character_scene_input_processing_for_age_set_age_and_reset_input_context(context)
    elif player_choice == "CHANGE_AGE_TO_YOUNG_ADULT_AGE_GROUP":
        context.new_character_age_group = Characters.Age_Group.ENUM__AGE_GROUP__YOUNG_ADULT
        spawn_character_scene_input_processing_for_age_set_age_and_reset_input_context(context)
    elif player_choice == "CHANGE_AGE_TO_ADULT_AGE_GROUP":
        context.new_character_age_group = Characters.Age_Group.ENUM__AGE_GROUP__ADULT
        spawn_character_scene_input_processing_for_age_set_age_and_reset_input_context(context)
    elif player_choice == "CHANGE_AGE_TO_MATURE_ADULT_AGE_GROUP":
        context.new_character_age_group = Characters.Age_Group.ENUM__AGE_GROUP__MATURE_ADULT
        spawn_character_scene_input_processing_for_age_set_age_and_reset_input_context(context)
    elif player_choice == "CHANGE_AGE_TO_ELDER_AGE_GROUP":
        context.new_character_age_group = Characters.Age_Group.ENUM__AGE_GROUP__ELDER
        spawn_character_scene_input_processing_for_age_set_age_and_reset_input_context(context)
    elif player_choice == "BACK":
        context.choice_context = "GENERAL"
    elif player_choice == "RESET_AGE":
        context.new_character_age = None
        context.new_character_age_group = None
        context.choice_context = "GENERAL"

def spawn_character_scene_gender_options(game_scene, context):
    if context.new_character_gender is None:
        display_gender = "???"
    else:
        if context.new_character_gender == Characters.Gender.FEMALE:
            display_gender = "Female"
        else: # context.new_character_gender == Characters.Gender.MALE:
            display_gender = "Male"
    print("    [@] ", display_gender)
    print("    [0] Set to FEMALE.")
    context.player_action_options[str(0)] = "CHANGE_GENDER_TO_FEMALE"
    print("    [1] Set to MALE.")
    context.player_action_options[str(1)] = "CHANGE_GENDER_TO_MALE"
    print("    [99] Back.")
    context.player_action_options[str(99)] = "BACK"
    print("    [00] Reset gender to random.")
    context.player_action_options["00"] = "RESET_GENDER"

def spawn_character_scene_input_processing_for_gender(game_scene, context, player_choice):
    if player_choice == "CHANGE_GENDER_TO_FEMALE":
        context.new_character_gender = Characters.Gender.FEMALE
    elif player_choice == "CHANGE_GENDER_TO_MALE":
        context.new_character_gender = Characters.Gender.MALE
    elif player_choice == "BACK":
        pass
    elif player_choice == "RESET_GENDER":
        context.new_character_gender = None

    context.choice_context = "GENERAL"

def spawn_character_scene_input_processing(game_scene, context):
    context.player_action_options = dict()
    if context.choice_context == "GENERAL":
        spawn_character_scene_character_details(game_scene, context)
    elif context.choice_context == "CHANGE_NAMES":
        spawn_character_scene_names_options(game_scene, context)
    elif context.choice_context == "CHANGE_GENDER":
        spawn_character_scene_gender_options(game_scene, context)
    elif context.choice_context == "CHANGE_AGE":
        spawn_character_scene_age_options(game_scene, context)
    else:
        raise ValueError("spawn_character_scene_input_processing(): Unrecognized context '{0}'".format(context.choice_context))

    print("What is your choice?")
    player_input = input("> ")
    if player_input not in context.player_action_options.keys():
        print("ERROR: Unknown option. Please select a valid option.")
        return

    player_choice = context.player_action_options[player_input]
    if context.choice_context == "GENERAL":
        spawn_character_scene_input_processing_for_general(game_scene, context, player_choice)
    elif context.choice_context == "CHANGE_NAMES":
        spawn_character_scene_input_processing_for_names(game_scene, context, player_choice)
    elif context.choice_context == "CHANGE_GENDER":
        spawn_character_scene_input_processing_for_gender(game_scene, context, player_choice)
    elif context.choice_context == "CHANGE_AGE":
        spawn_character_scene_input_processing_for_age(game_scene, context, player_choice)
    else:
        raise ValueError("spawn_character_scene_input_processing(): Unrecognized context '{0}' (after processing player input)".format(context.choice_context))

spawn_character_scene = Game_Scenes.Game_Scene("SIMPLER_TESTER__Spawn_Character")
spawn_character_scene.prepare_scene_and_create_context_function = spawn_character_prepare_scene_and_create_context
spawn_character_scene.scene_start_presentation = spawn_character_scene_presentation
spawn_character_scene.scene_player_input_processing_function = spawn_character_scene_input_processing

## NAMES
standar_names_resource_raw = {
    "Alexa": {
        "name_possessive": "Alexa's",
        "gender_of_characters_using_this_name_in_game": Characters.Gender.FEMALE,
        "can_be_individual_name_in_game": True,
        "can_be_nickname_in_game": True,
        "linked_nicknames_in_game": ["Al", "Allie", "Lexa", "Lexi", "Alex"],
        "individual_names_for_this_name_as_a_nickname_in_game": ["Alexandra"],
    },
    "Paul": {
        "name_possessive": "Paul's",
        "gender_of_characters_using_this_name_in_game": Characters.Gender.MALE,
        "can_be_individual_name_in_game": True,
        "can_be_nickname_in_game": False,
        "linked_nicknames_in_game": ["Paulie"],
        "individual_names_for_this_name_as_a_nickname_in_game": [],
    },
    "Alexandra": {
        "name_possessive": "Alexandra's",
        "gender_of_characters_using_this_name_in_game": Characters.Gender.FEMALE,
        "can_be_individual_name_in_game": True,
        "linked_nicknames_in_game": ["Al", "Allie", "Lexa", "Lexi", "Alex", "Alexa"],
        "individual_names_for_this_name_as_a_nickname_in_game": [],
    },

    "Alessa": {
        "name_possessive": "Alessa's",
        "gender_of_characters_using_this_name_in_game": Characters.Gender.FEMALE,
        "can_be_individual_name_in_game": True,
        "can_be_nickname_in_game": True,
        "linked_nicknames_in_game": ["Al", "Allie", "Lessa"],
        "individual_names_for_this_name_as_a_nickname_in_game": ["Alessandra"],
    },
    "Alessandra": {
        "name_possessive": "Alessandra's",
        "gender_of_characters_using_this_name_in_game": Characters.Gender.FEMALE,
        "can_be_individual_name_in_game": True,
        "can_be_nickname_in_game": False,
        "linked_nicknames_in_game": ["Al", "Allie", "Lessa", "Alessa"],
        "individual_names_for_this_name_as_a_nickname_in_game": [],
    },
    "John": {
        "name_possessive": "John's",
        "gender_of_characters_using_this_name_in_game": Characters.Gender.MALE,
        "can_be_individual_name_in_game": True,
        "can_be_nickname_in_game": False,
        "linked_nicknames_in_game": ["Johny"],
        "individual_names_for_this_name_as_a_nickname_in_game": [],
    },
    "Johny": {
        "name_possessive": "Johny's",
        "gender_of_characters_using_this_name_in_game": Characters.Gender.MALE,
        "can_be_individual_name_in_game": False,
        "can_be_nickname_in_game": True,
        "linked_nicknames_in_game": [],
        "individual_names_for_this_name_as_a_nickname_in_game": ["John", "Johnatan"],
    },
}

family_names_resource_raw = {
    "Briger": {
        "name_possessive": "Brdger's",
    },

    "Grimm": {
        "name_possessive": "Grimm's",
    },

    "Foster": {
        "name_possessive": "Foster's",
    },
}

## CHARACTERS
prot_name = Names.Character_Names()
prot_name.individual_name = "Otherworldy Being"
prot_name.family_name = ""
protagonist = Characters.Character("PROTAGONIST", prot_name, "MALE", 9000000)

## ACTIONS

def quit_game_action(character_action, character, context):
    game.stop_game = True

quit_game = Actions.Character_Action("SIMPLER_TESTER__Quit_Game")
quit_game.player_menu_description = Actions.Character_Action_Description(action_description = "QUIT the GAME", action_description_kind = Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__TEXT)
quit_game.execution_function = quit_game_action
Actions.register_in_database(quit_game)

def examine_self_action(character_action, character, context):
    return Characters.Character.examine_character_default_function(system.protagonist)

examine_self = Actions.Character_Action("SIMPLER_TESTER__Examine_Self")
examine_self.player_menu_description = Actions.Character_Action_Description(action_description = "Examine self", action_description_kind = Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__TEXT)
examine_self.execution_description = Actions.Character_Action_Description(action_description = "You look at yourself.", action_description_kind = Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__TEXT)
examine_self.result_description = Actions.Character_Action_Description(action_description = examine_self_action, action_description_kind = Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__FUNCTION)
Actions.register_in_database(examine_self)

def travel_to_new_location_possibility_check(character_action, character, context):
    reachable_locations = Locations.Location.reachable_locations_default_function(character, context)
    if character.location.id not in reachable_locations:
        if len(reachable_locations) > 0:
            return True
    elif len(reachable_locations) > 1:
        return True
    return False

def travel_to_location_action_scene_starter(character_action, character, context):
    context.switch_scene_new_scene_id = "SIMPLER_TESTER__Travel_to_Location"

travel_to_location_action = Actions.Character_Action("SIMPLER_TESTER__Travel_to_Location")
travel_to_location_action.check_action_is_possible_function = travel_to_new_location_possibility_check
travel_to_location_action.player_menu_description = Actions.Character_Action_Description(action_description = "Go somewhere else...", action_description_kind = Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__TEXT)
travel_to_location_action.execution_function = travel_to_location_action_scene_starter
Actions.register_in_database(travel_to_location_action)

def spawn_character_check_action_is_possible(character_action, character, context):
    if game.debug_mode == True:
        return True
    else:
        return False

def spawn_character_action_scene_starter(character_action, character, context):
    context.switch_scene_new_scene_id = "SIMPLER_TESTER__Spawn_Character"

spawn_character_action = Actions.Character_Action("SIMPLER_TESTER__Spawn_Character")
spawn_character_action.check_action_is_possible_function = spawn_character_check_action_is_possible
spawn_character_action.player_menu_description = Actions.Character_Action_Description(action_description = "Spawn character...", action_description_kind = Actions.Character_Action_Description.ENUM__ACTION_DESCRIPTION_KINDS__TEXT)
spawn_character_action.execution_function = spawn_character_action_scene_starter
Actions.register_in_database(spawn_character_action)

## LOCATIONS

unending_void = Locations.Location("SIMPLER_TESTER__Unending_Void", in_or_at = "in an", short_name = "Unending Void")
unending_void.short_descriptor = "Emptiness infinite."
unending_void.register_in_database()

protagonist.location = unending_void

strangely_tight_location = Locations.Location("SIMPLER_TESTER__Strangely_Tight_Location", in_or_at = "in a", short_name = "strangely tight location")
strangely_tight_location.short_descriptor = "Confining, yet featureless."
strangely_tight_location.register_in_database()

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
    game.register_scene(travel_to_location_scene)
    game.register_scene(spawn_character_scene)
    game.inject_scene(introduction.scene_id, None)

    standard_names_database = Names.Standard_Name_Entry.build_collection_from_dict(standar_names_resource_raw)
    family_names_database = Names.Family_Name_Entry().build_collection_from_dict(family_names_resource_raw)
    Names.Character_Names.names_databases.reset_databases(standard_names_database = standard_names_database, family_names_database = family_names_database)

    new_character = Characters.generate_random_character(id = None, gender = None, age = None, names = None)
    new_character = Characters.generate_random_character(id = None, gender = None, age = None, names = None)

    game.debug_mode = True

print("[+] Initializing game...")
powerPlayFramework_initialize()
print("[+] Game initialized...")
#print(Characters.Character.examine_character_default_function(system.protagonist))
while not game.stop_game:
    game.game_loop()

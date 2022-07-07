# # Minimal Mind System
# - Given a Topic and a Context, how much does the Character Like that Topic.
# - Given a Topic and a character, how much does the Character Believe that Topic.

ENUM__ACCEPTANCE__INDIFFERENT = "INDIFFERENT" # = 0

ENUM__ACCEPTANCE__APPRECIATE = "APPRECIATE" # = 1 /Enjoy/Enjoyable
ENUM__ACCEPTANCE__LIKE = "LIKE" # = 2 /Delight/Want/Delightful
ENUM__ACCEPTANCE__LOVE = "LOVE" # = 3 /Cherish/Loveable
ENUM__ACCEPTANCE__NEED = "NEED" # = 4 /Needed
ENUM__ACCEPTANCE__REQUIRE = "REQUIRE" # = 5 /Required

ENUM__ACCEPTANCE__TOLERATE = "TOLERATE" # = -1 /Accept/Annoying
ENUM__ACCEPTANCE__DESPISE = "DESPISE" # = -2 /Uncomfortable
ENUM__ACCEPTANCE__DISLIKE = "DISLIKE" # = -3 /Unpalatable
ENUM__ACCEPTANCE__SCORN = "SCORN" # = -4 /Distressing
ENUM__ACCEPTANCE__HATE = "HATE" # = -5 /Traumatizing
ENUM__ACCEPTANCE__EXECRATE = "EXECRATE" # = -6 /Terrifying/Unforgivable


def get_satisfaction(context, character, topic):
    satisfaction = character.mind.get_satisfaction(context, character, topic)
    return satisfaction

def get_conviction(character, topic):
    belief_value = Belief_Value()
    return belief_value

def initalize_mind_system(character_class_to_have_mind):
    character_class_to_have_mind.dynamic_initialization_functions.append(initialize_mind_on_character)

def initialize_mind_on_character(character):
    character.mind = Character_Mind()

class Character_Mind(object):
    def __init__(self):
        self.preferences = {}
    
    def get_satisfaction(self, context, perspective_owner, topic):
        if topic in self.preferences.keys():
            return self.preferences[topic].get_satisfaction(context, perspective_owner)
        else:
            return None

class Satisfaction(object):
    def __init__(self, value, components = {}):
        self.value = value
        self.components = components

class Belief_Value(object):
    def __init__(self, value, components = {}):
        self.value = value
        self.components = components

class Character_Preference(object):
    def __init__(self, id):
        self.id = id
        self.value = None
        self.evaluation_function = None
    
    def set_value(self, value):
        self.value = value
    
    def get_satisfaction(self, context, perspective_owner):
        if self.evaluation_function is not None:
            return self.evaluation_function(context, perspective_owner, self.value)
        else:
            return self.value


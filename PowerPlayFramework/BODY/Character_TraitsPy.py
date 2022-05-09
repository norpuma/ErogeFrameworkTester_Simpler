def get_trait_value(character, trait_id):
    value = Character_Trait_Value(Character_Trait_Value.ENUM__CHARACTER_TRAIT_VALUE_TYPES__TEXT, "DEBUG__INVALID_VALUE")
    return value

def initialize_traits_on_character(character):
    character.traits = {}

def initialize_traits_on_character_member(character_member):
    character_member.traits = {}

class Character_Trait_Value(object):
    ENUM__CHARACTER_TRAIT_VALUE_TYPES__TEXT = "TEXT"
    ENUM__CHARACTER_TRAIT_VALUE_TYPES__INTEGER = "INTEGER"
    ENUM__CHARACTER_TRAIT_VALUE_TYPES__FLOAT = "FLOAT"
    ENUM__CHARACTER_TRAIT_VALUE_TYPES__INTENSITY = "INTENSITY"
    def __init__(self, value_type, value):
        self.value_type = value_type
        self.value = value

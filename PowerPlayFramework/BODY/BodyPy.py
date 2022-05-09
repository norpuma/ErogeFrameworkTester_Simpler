# # Minimal Body System
# - Given a Character and a Trait, what is the value of this Trait.

import Character_TraitsPy

def get_trait_value(character, trait_id):
    value = character.body.traits[trait_id].value
    return value

def initalize_body_system(character_class_to_have_body):
    character_class_to_have_body.dynamic_initialization_functions.append(initialize_body_on_character)

def initialize_body_on_character(character):
    character.body = Character_Body(character.gender, character.age)

class Character_Body(object):
    def __init__(self, gender, age):
        Character_TraitsPy.initialize_traits_on_character_member(self)

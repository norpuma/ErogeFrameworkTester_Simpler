from .FundamentalsPy import Gender
from .FundamentalsPy import Age_Group
from ..NAMES.NamesPy import Character_Names
import uuid

def initialize_system():
    pass

def generate_random_character(id = None, gender = None, age_group = None, age = None, names = None):
    if id is None:
        id = uuid.uuid4()
    if gender is None:
        gender = Gender.generate_random()
    if age is None and age_group is None:
        age_group = Age_Group.generate_random_age_group()
        age = Age_Group.generate_random_age(age_group)
    elif age is None:
        age = Age_Group.generate_random_age(age_group)

    names = Character_Names.generate_random_from_name_object(gender, names)

    result = Character(id, names, gender, age)
    return result

def default_examine_character(character):
    _msg = "{0} is a {1} years old {2}.".format(character.names.full, character.age, character.gender)
    return _msg

class Character(object):
    dynamic_initialization_functions = []
    examine_character_default_function = default_examine_character
    def __init__(self, id, names, gender, age):
        self.id = id
        self.names = names
        self.gender = gender
        self.age = age
        for function in Character.dynamic_initialization_functions:
            function(self)


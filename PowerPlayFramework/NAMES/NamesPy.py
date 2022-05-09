# # Minimal Character Names System
# - Characters have standard names (the default name displayed).
# - Characters have first and last names.
# - Characters share names with their families (unless family members are married or the character themself is married).
# - It must be possible to generate random names.
# - Random names come from a database of names.
# - It must be possible to prevent repeating random names.

import random
from ..CHARACTERS_BASE.FundamentalsPy import Gender

individual_names_database = {
    Gender.FEMALE: {
        # Individual names have: "Name": ["Individual", "Name", "Variants"]; e.g. "Patricia": ["Pattie", "Trish", "Trisha"]
    },
    Gender.MALE: {
        # Individual names have: "Name": ["Individual", "Name", "Variants"]; e.g. "Michael": ["Mick", "Mickey"]
    },
}

family_names_database = []

available_standard_names = {
    Gender.FEMALE: {
        # Available standard names have: "Name": Individual_name_attached_to_this_standard_name; e.g. "Trish": "Patricia"
        # ATTENTION no two characters should use the same standard name
    },
    Gender.MALE: {
        # Available standard names have: "Name": Individual_name_attached_to_this_standard_name; e.g. "Mickey": "Michael"
        # ATTENTION no two characters should use the same standard name
    },
}

used_individual_names = {
    # Used first names have: "Name": [Character, Object, Using, The, Name]; e.g. "Patricia": [important_lawyer, rebel_student]
}

used_family_names = {
    # Used first names have: "Name": [Character, Object, Using, The, Name]; e.g. "Gladson": [important_lawyer, important_lawyers_daughter]
}

used_standard_names = {
    # Used first names have: "Name": Character_Object_Using_The_Name; e.g. "Trish": important_lawyer
    # ATTENTION no two characters should use the same standard name
}

available_family_names = []

def reset_databases():
    global individual_names_database
    individual_names_database = {
        Gender.FEMALE: {
            # Individual names have: "Name": ["Individual", "Name", "Variants"]; e.g. "Patricia": ["Pattie", "Trish", "Trisha"]
        },
        Gender.MALE: {
            # Individual names have: "Name": ["Individual", "Name", "Variants"]; e.g. "Michael": ["Mick", "Mickey"]
        },
    }

    global family_names_database
    family_names_database = []

    global available_standard_names
    available_standard_names = {
        Gender.FEMALE: {
            # Available standard names have: "Name": Individual_name_attached_to_this_standard_name; e.g. "Trish": "Patricia"
            # ATTENTION no two characters should use the same standard name
        },
        Gender.MALE: {
            # Available standard names have: "Name": Individual_name_attached_to_this_standard_name; e.g. "Mickey": "Michael"
            # ATTENTION no two characters should use the same standard name
        },
    }

    global used_individual_names
    used_individual_names = {
        # Used first names have: "Name": [Character, Object, Using, The, Name]; e.g. "Patricia": [important_lawyer, rebel_student]
    }

    global used_family_names
    used_family_names = {
        # Used first names have: "Name": [Character, Object, Using, The, Name]; e.g. "Gladson": [important_lawyer, important_lawyers_daughter]
    }

    global used_standard_names
    used_standard_names = {
        # Used first names have: "Name": Character_Object_Using_The_Name; e.g. "Trish": important_lawyer
        # ATTENTION no two characters should use the same standard name
    }

    global available_family_names
    available_family_names = []



def initialize_names_databases(female_individual_names__to_insert, male_individual_names__to_insert, family_names__to_insert, should_reset_databases = True):
    if should_reset_databases:
        reset_databases()

    global individual_names_database
    global available_standard_names
    global used_individual_names
    global used_standard_names
    used_individual_names_keys = used_individual_names.keys()
    used_standard_names_keys = used_standard_names.keys()

    individual_names_to_insert_keys = female_individual_names__to_insert.keys()
    individual_names_database_keys = individual_names_database[Gender.FEMALE].keys()
    for name in individual_names_to_insert_keys:
        if name not in individual_names_database_keys:
            individual_names_database[Gender.FEMALE][name] = []
        if should_reset_databases or (name not in used_individual_names_keys):
            available_standard_names[Gender.FEMALE][name] = name
        for nickname in female_individual_names__to_insert[name]:
            if nickname not in individual_names_database[Gender.FEMALE][name]:
                individual_names_database[Gender.FEMALE][name].append(nickname)
            if should_reset_databases or (nickname not in used_standard_names_keys):
                available_standard_names[Gender.FEMALE][nickname] = name

    individual_names_to_insert_keys = male_individual_names__to_insert.keys()
    individual_names_database_keys = individual_names_database[Gender.MALE].keys()
    for name in individual_names_to_insert_keys:
        if name not in individual_names_database_keys:
            individual_names_database[Gender.MALE][name] = []
        if should_reset_databases or (name not in used_individual_names_keys):
            available_standard_names[Gender.MALE][name] = name
        for nickname in male_individual_names__to_insert[name]:
            if nickname not in individual_names_database[Gender.MALE][name]:
                individual_names_database[Gender.MALE][name].append(nickname)
            if should_reset_databases or (nickname not in used_standard_names_keys):
                available_standard_names[Gender.MALE][nickname] = name
    
    global family_names_database
    global used_family_names
    global available_family_names
    family_names_database_keys = family_names_database.keys()
    used_family_names_keys = used_family_names.keys()
    for name in family_names__to_insert:
        if name not in family_names_database_keys:
            family_names_database.append(name)
        if should_reset_databases or (name not in used_family_names_keys):
            available_family_names.append(name)
        

def consume_standard_name(gender, name, character, should_throw_exception_on_name_not_available = True):
    gendered_available_standard_names = available_standard_names[gender]
    if name in gendered_available_standard_names.keys():
        used_standard_names[name] = character
        attached_individual_name = gendered_available_standard_names.pop(name)
        if attached_individual_name not in used_individual_names.keys():
            used_individual_names[attached_individual_name] = []
        used_individual_names[attached_individual_name].append(character)
    elif should_throw_exception_on_name_not_available:
        raise ValueError("ERROR: consume_standard_name(): Name '{0}' could not be found in datababase '{1}' and could not be consumed for character '{2}'.".format(name, "gendered_available_standard_names", character.id))

def consume_family_name(name, character, should_throw_exception_on_name_not_available = True):
    if name in available_family_names.keys():
        used_family_names[name] = character
        available_family_names.pop(name)
    elif should_throw_exception_on_name_not_available:
        raise ValueError("ERROR: consume_family_name(): Name '{0}' could not be found in datababase '{1}' and could not be consumed for character '{2}'.".format(name, "available_family_names", character.id))

def release_standard_name(gender, character, standard_name, attached_individual_name):
    gendered_available_standard_names = available_standard_names[gender]
    gendered_available_standard_names[standard_name] = attached_individual_name
    if attached_individual_name not in individual_names_database[gender]:
        individual_names_database[gender] = attached_individual_name
    if attached_individual_name in used_individual_names and character in used_individual_names[attached_individual_name]:
        used_individual_names[attached_individual_name].pop(character)
    if standard_name in used_standard_names.keys():
        used_standard_names.pop(standard_name)

def release_family_name():
    pass

def default_full_name(names_object):
    if names_object.standard is not None and names_object.standard != names_object.first:
        return names_object.first + " '" + names_object.standard + "' " + names_object.last
    return names_object.first + " " + names_object.last

class Character_Names(object):
    full_name_default_function = default_full_name
    def __init__(self):
        self.standard = None
        self.individual_name = None
        self.family_name = None
        self.custom_full_name = None
    
    @property
    def first(self):
        return self.individual_name
    
    @property
    def last(self):
        return self.family_name
    
    @property
    def full(self):
        if self.custom_full_name is not None:
            return self.custom_full_name(self)
        else:
            return Character_Names.full_name_default_function(self)
    
    @classmethod
    def random(cls, gender, character, individual_name = None, family_name = None, standard = None, should_consume_name = True, should_throw_exception_on_standard_name_clash = True):
        result = cls()
        if standard != None:
            result.standard = standard
        else:
            result.standard = cls._random_standard(result.individual_name, should_throw_exception_on_standard_name_clash)
        if should_consume_name:
            consume_standard_name(gender, result.standard, character, should_throw_exception_on_standard_name_clash)
    
        if individual_name != None:
            cls._check_individual_name_uniqueness(individual_name, family_name, should_throw_exception_on_standard_name_clash)
            # if should_throw_exception_on_standard_name_clash:
            # if individual_name in used_individual_names.keys():
            #     raise ValueError("ERROR: Character_Names.random(): Name {0} is already in used by character {1}.".format(individual_name, used_individual_names[individual_name]))
            result.individual_name = individual_name
        else:
            result.first = cls._random_individual_name(gender, should_throw_exception_on_standard_name_clash)
        
        if family_name != None:
            result.family_name = family_name
        else:
            result.family_name = cls._random_family_name()
        
    @classmethod
    def _random_individual_name(cls, gender, should_consume_name, should_throw_exception_on_standard_name_clash):
        if gender is None:
            gender = Gender.generate_random()

        if gender == Gender.FEMALE:
            return cls._random_individual_name_female(should_consume_name, should_throw_exception_on_standard_name_clash)
        else: # if gender == Gender.MALE:
            return cls._random_individual_name_male(should_consume_name, should_throw_exception_on_standard_name_clash)

    @classmethod
    def _random_individual_name_female(cls, should_consume_name, should_throw_exception_on_standard_name_clash):
        individual_names_database = female_individual_names_database
        # Individual names have: "Name": ["Individual", "Name", "Variants"]; e.g. "Patricia": ["Pattie", "Trish", "Trisha"]

        return "Mary"
    
    @classmethod
    def _random_individual_name_male(cls, should_consume_name, should_throw_exception_on_standard_name_clash):
        return "John"

    @classmethod
    def _check_individual_name_uniqueness(cls, individual_name, family_name, should_consume_name, should_throw_exception_on_standard_name_clash):
        # TODO: Implement this.
        return

    @classmethod
    def _random_family_name(cls):
        return "Smith"

    @classmethod
    def _random_standard(cls, base_name, should_consume_name, should_throw_exception_on_standard_name_clash):
        if base_name == "John":
            return random.choice("John", "Johnny")
        else:
            return "Shortie"

    @classmethod
    def _check_standard_name_uniqueness(cls, individual_name, family_name, standard, should_consume_name, should_throw_exception_on_standard_name_clash):
        # TODO: Implement this.
        return

    @classmethod
    def build_from_dict(cls, pre_defined_attributes, should_throw_exception_on_standard_name_clash = True):
        gender = None
        individual_name = None
        family_name = None
        standard_name = None
        pre_defined_attributes_keys = pre_defined_attributes.keys()
        if "gender" in pre_defined_attributes_keys:
            gender = pre_defined_attributes["gender"]
        if "individual_name" in pre_defined_attributes_keys:
            individual_name = pre_defined_attributes["individual_name"]
        if "family_name" in pre_defined_attributes_keys:
            family_name = pre_defined_attributes["family_name"]
        if "standard_name" in pre_defined_attributes_keys:
            standard_name = pre_defined_attributes["standard_name"]

        result = cls.random(gender, individual_name, family_name, standard_name, should_throw_exception_on_standard_name_clash)
        return result

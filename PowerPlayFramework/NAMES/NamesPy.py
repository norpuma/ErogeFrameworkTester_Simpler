# # Minimal Character Names System
# - Characters have standard names (the default name displayed).
# - Characters have first and last names.
# - Characters share names with their families (unless family members are married or the character themself is married).
# - It must be possible to generate random names.
# - Random names come from a database of names.
# - It must be possible to prevent repeating random names.

import random
from ..CHARACTERS_BASE.FundamentalsPy import Gender

def default_full_name_builder(names_object):
    if names_object.standard is not None and names_object.standard != names_object.first:
        return names_object.first + " '" + names_object.standard + "' " + names_object.last
    return names_object.first + " " + names_object.last

class Names_Databases(object):
    def __init__(self):
        self._reset()
    
    def _reset(self):
        self.standard_names_database = dict()
        self.family_names_database = dict()
        self.available_standard_female_names_keys = []
        self.available_standard_male_names_keys = []
        self.available_family_names_keys = []
        self.used_individual_names = {}
        self.used_standard_names = {}
        self.used_family_names = {}

    def reset_databases(self, standard_names_database, family_names_database):
        self._reset()
        self.standard_names_database.update(standard_names_database)
        standard_keys = self.standard_names_database.keys()
        entries_discovered_during_processing = dict()
        for standard_name in standard_keys:
            standard_name_entry = self.standard_names_database[standard_name]
            self.add_standard_name(standard_name_entry, entries_discovered_during_processing)
        self.standard_names_database.update(entries_discovered_during_processing)

        self.family_names_database.update(family_names_database)
        for family_name_entry in family_names_database.values():
            self.available_family_names_keys.append(family_name_entry.name)

    def add_standard_name(self, standard_name_entry, entries_discovered_during_processing):
        standard_name = standard_name_entry.name
        if standard_name in self.standard_names_database.keys():
            existing_entry = self.standard_names_database[standard_name]
            if existing_entry.name_possessive is None:
                existing_entry.name_possessive = standard_name_entry.name_possessive
        else:
            entries_discovered_during_processing[standard_name] = standard_name_entry
        if standard_name_entry.gender_of_characters_using_this_name_in_game == Gender.FEMALE:
            available_list = self.available_standard_female_names_keys
        else:
            available_list = self.available_standard_male_names_keys
        available_list.append(standard_name)
        for individual_name in standard_name_entry.individual_names_for_this_name_as_a_nickname_in_game:
            if individual_name not in self.standard_names_database.keys():
                new_standard_entry = Standard_Name_Entry()
                new_standard_entry.gender_of_characters_using_this_name_in_game = standard_name_entry.gender_of_characters_using_this_name_in_game
                new_standard_entry.name = individual_name
                new_standard_entry.can_be_individual_name_in_game = True
                new_standard_entry.linked_nicknames_in_game.append(standard_name)
                self.add_standard_name(new_standard_entry, entries_discovered_during_processing)
                if individual_name not in available_list:
                    available_list.append(individual_name)
            else:
                existing_individual_entry = self.standard_names_database[individual_name]
                if standard_name not in existing_individual_entry.linked_nicknames_in_game:
                    existing_individual_entry.linked_nicknames_in_game.append(standard_name)
        for nickname in standard_name_entry.linked_nicknames_in_game:
            if nickname not in self.standard_names_database.keys():
                new_standard_entry = Standard_Name_Entry()
                new_standard_entry.gender_of_characters_using_this_name_in_game = standard_name_entry.gender_of_characters_using_this_name_in_game
                new_standard_entry.name = nickname
                new_standard_entry.individual_names_for_this_name_as_a_nickname_in_game.append(standard_name)
                self.add_standard_name(new_standard_entry, entries_discovered_during_processing)
                if nickname not in available_list:
                    available_list.append(nickname)
            else:
                existing_nickname_entry = self.standard_names_database[nickname]
                if standard_name not in existing_nickname_entry.individual_names_for_this_name_as_a_nickname_in_game:
                    existing_nickname_entry.individual_names_for_this_name_as_a_nickname_in_game.append(standard_name)

    def check_standard_is_in_use(self, name):
        if name in self.used_standard_names.keys():
            return True
        return False

    def check_family_name_is_in_use(self, name):
        if name in self.used_family_names.keys():
            return True
        return False

    def check_individual_and_family_name_combination_is_in_use(self, individual_name, family_name):
        if family_name not in self.used_family_names.keys():
            return False
        family_members = self.used_family_names[family_name]
        for family_member in family_members:
            if family_member.names.individual_name == individual_name:
                return True
        return False

    def consume_standard_name(self, gender, standard_name, individual_name, character):
        if standard_name not in self.used_standard_names.keys():
            self.used_standard_names[standard_name] = Used_Standard_Name_Entry()
        if individual_name == standard_name:
            self.used_standard_names[standard_name].used_as_nickname_by.append(character)
        else:
            self.used_standard_names[standard_name].used_as_individual_name_by.append(character)
        
        if gender == Gender.FEMALE:
            available_standar_names_keys = self.available_standard_female_names_keys
        else:
            available_standar_names_keys = self.available_standard_male_names_keys

        if standard_name in available_standar_names_keys:
            index_of_name = available_standar_names_keys.index(standard_name)
            del available_standar_names_keys[index_of_name]

    def consume_family_name(self, name, character):
        if name not in self.used_family_names.keys():
            self.used_family_names[name] = []
        
        self.used_family_names[name].append(character)

    def pick_random_standard_and_individual_names(self, gender, standard = None, individual = None):
        if standard is not None and individual is not None:
            return (standard, individual)
        names_resource = Character_Names.names_databases.standard_names_database

        if (gender == Gender.FEMALE):
            available_names_keys = Character_Names.names_databases.available_standard_female_names_keys
        else:
            available_names_keys = Character_Names.names_databases.available_standard_male_names_keys

        if individual is not None:
            if individual in names_resource.keys():
                current_index = random.randint(0, len(names_resource[individual].linked_nicknames_in_game)+1)
                attempts_count = 0
                while attempts_count < len(names_resource[individual].linked_nicknames_in_game)+1:
                    if attempts_count == len(names_resource[individual].linked_nicknames_in_game):
                        candidate_standard_name = individual
                    else:
                        candidate_standard_name = names_resource[individual].linked_nicknames_in_game[current_index]
                    if candidate_standard_name in Character_Names.names_databases.available_names_keys:
                        return (candidate_standard_name, individual)
                    attempts_count += 1
                    if attempts_count + current_index >= len(names_resource[individual].linked_nicknames_in_game)+1:
                        current_index = -1 * attempts_count
                # At this point, no linked nickname is available for the individual name
                raise Exception("ERROR: No available standard names for individual name '{0}'. The name isn't available either as a standard name.")
            else:
                standard = individual
            return (standard, individual)

        # At this point, both standard and individual are None
        standard = random.choice(available_names_keys)
        if len(names_resource[standard].individual_names_for_this_name_as_a_nickname_in_game) > 0:
            individual = random.choice(names_resource[standard].individual_names_for_this_name_as_a_nickname_in_game)
        else:
            individual = standard

        return (standard, individual)

    def pick_random_between_provided_name_and_linked_name_from_available(self, provided_name, linked_names, available_names_list):
        candidate_names = []
        for possible_candidate in linked_names:
            if possible_candidate in available_names_list:
                candidate_names.append(possible_candidate)
        choice = random.randint(0, len(candidate_names))
        if choice == len(candidate_names):
            return provided_name
        else:
            return candidate_names[choice]
    
    def pick_random_family_name(self):
        return random.choice(self.available_family_names_keys)

    def add_standard_name_entry(self, gender, standard_name_entry):
        if standard_name_entry.name in self.standard_names_database.keys():
            return
        
        if gender == Gender.FEMALE:
            available_individual_names_keys = self.available_standard_female_names_keys
        else:
            available_individual_names_keys = self.available_standard_male_names_keys

        self.standard_names_database[standard_name_entry.name] = standard_name_entry
        available_individual_names_keys.append(standard_name_entry.name)

    def add_family_name_entry(self, family_name_entry):
        if family_name_entry.name in self.family_names_database.keys():
            return
        self.family_names_database[family_name_entry.name] = family_name_entry
        self.available_family_names_keys.append(family_name_entry.name)
    
class Character_Names(object):
    full_name_default_function = default_full_name_builder
    FIRST_NAME_REFERENCE = "individual_name"
    LAST_NAME_REFERENCE = "family_name"
    STANDARD_NAME_KEY = "standard"
    INDIVIDUAL_NAME_KEY = "individual_name"
    FAMILY_NAME_KEY = "family_name"
    names_databases = Names_Databases()
    def __init__(self):
        self._reset()
    
    def _reset(self):
        self.standard = None
        self.standard_possessive = None
        self.individual_name = None
        self.individual_name_possessive = None
        self.family_name = None
        self.family_name_possessive = None
        self.custom_full_name_function = None

    @property
    def first(self):
        return self.individual_name

    @property
    def first_possessive(self):
        return self.individual_name_possessive

    @property
    def last(self):
        return self.family_name

    @property
    def last_possessive(self):
        return self.family_name

    def set_name(self, kind, new_name, new_name_possessive = None):
        if kind == "first" and self.standard is None:
            self.set_name("standard", new_name, new_name_possessive)
        if kind == "first":
            kind = Character_Names.FIRST_NAME_REFERENCE
        elif kind == "last":
            kind = Character_Names.LAST_NAME_REFERENCE

        setattr(self, kind, new_name)
        if (new_name_possessive != None):
            setattr(self, kind + "_possessive", new_name_possessive)
        else:
            setattr(self, kind + "_possessive", new_name + "'s")

    @property
    def full(self):
        if self.custom_full_name_function is not None:
            return self.custom_full_name_function(self)
        else:
            return Character_Names.full_name_default_function(self)

    @classmethod
    def generate_random_from_name_object(cls, gender, names, should_throw_exception_on_standard_name_clash = True):
        if names != None:
            standard = names.standard
            standard_possessive = names.standard_possessive
            individual = names.individual_name
            individual_possessive = names.individual_name_possessive
            family = names.family_name
            family_possessive = names.family_name_possessive
        else:
            standard = None
            standard_possessive = None
            individual = None
            individual_possessive = None
            family = None
            family_possessive = None
        return cls.generate_random(gender, standard, standard_possessive, individual, individual_possessive, family, family_possessive, should_throw_exception_on_standard_name_clash)

    @classmethod
    def generate_random(cls, gender, standard = None, standard_possessive = None, individual = None, individual_possessive = None, family = None, family_possessive = None, should_throw_exception_on_standard_name_clash = True, iteration_count = 0):
        if iteration_count > 200:
            raise Exception("FATAL: Character_Names.generate_random(): Too many iterations! Can't find a suitable name for given constraints ({0}, {1}, {2}, {3}, {4}). There are not enough names in the datbase. Aborting.".format(gender, standard, individual, family, should_throw_exception_on_standard_name_clash))
        received_standard = standard
        received_individual = individual
        received_family = family
        result = Character_Names()

        standard, individual = Character_Names.names_databases.pick_random_standard_and_individual_names(gender, standard, individual)
        result.set_name(Character_Names.STANDARD_NAME_KEY, standard, standard_possessive)
        result.set_name(Character_Names.INDIVIDUAL_NAME_KEY, individual, individual_possessive)

        if family is not None:
            if Character_Names.names_databases.check_family_name_is_in_use(family) == True:
                family_members = Character_Names.names_databases.used_family_names[family]
                for family_member in family_members:
                    if family_member.names.individual_name == individual:
                        return Character_Names.generate_random(gender, received_standard, standard_possessive, received_individual, individual_possessive, received_family, family_possessive, should_throw_exception_on_standard_name_clash, iteration_count +1)
                    if family_member.names.standard == standard:
                        return Character_Names.generate_random(gender, received_standard, standard_possessive, received_individual, individual_possessive, received_family, family_possessive, should_throw_exception_on_standard_name_clash, iteration_count +1)
        else:
            family = Character_Names.names_databases.pick_random_family_name()
        
        result.set_name(Character_Names.FAMILY_NAME_KEY, family, Character_Names.names_databases.family_names_database[family].name_possessive)

        return result

class Standard_Name_Entry(object):
    def __init__(self):
        self.name = None
        self.name_possessive = None
        self.gender_of_characters_using_this_name_in_game = None
        self.can_be_individual_name_in_game = False
        self.linked_nicknames_in_game = []
        self.individual_names_for_this_name_as_a_nickname_in_game = []
    
    @classmethod
    def build_from_dict(cls, name, dict_object):
        result = cls()
        if name is None:
            raise Exception("ERROR: Standard_Name_Entry.build_from_dict(): Can't process Standard_Name_Entry without a 'name' member.")
        result.name = name
        if "gender_of_characters_using_this_name_in_game" not in dict_object.keys():
            raise Exception("ERROR: Standard_Name_Entry.build_from_dict(): Can't process Standard_Name_Entry without a 'gender_of_characters_using_this_name_in_game' member.")
        for member in result.__dir__():
            if member in dict_object.keys():
                result.__setattr__(member, dict_object[member])
        if not result.can_be_individual_name_in_game and len(result.linked_nicknames_in_game) < 1 and len(result.individual_names_for_this_name_as_a_nickname_in_game) < 1:
            raise Exception("ERROR: Standard_Name_Entry.build_from_dict(): Name {0} is not defined as either an individual nor a nickname.".format(result.name))

        return result
    
    @classmethod
    def build_collection_from_dict(cls, dict_object):
        result = dict()
        name_keys = dict_object.keys()
        for name_entry_key in name_keys:
            name_entry = cls.build_from_dict(name_entry_key, dict_object[name_entry_key])
            result[name_entry.name] = name_entry
        
        return result

class Family_Name_Entry(object):
    def __init__(self):
        self.name = None
        self.name_possessive = None

    @classmethod
    def build_from_dict(cls, name, dict_object):
        result = cls()
        if name is None:
            raise Exception("ERROR: Standard_Name_Entry.build_from_dict(): Can't process Standard_Name_Entry without a 'name' member.")
        result.name = name
        for member in result.__dir__():
            if member in dict_object.keys():
                result.__setattr__(member, dict_object[member])

        return result
    
    @classmethod
    def build_collection_from_dict(cls, dict_object):
        result = dict()
        name_keys = dict_object.keys()
        for name_entry_key in name_keys:
            name_entry = cls.build_from_dict(name_entry_key, dict_object[name_entry_key])
            result[name_entry.name] = name_entry
        
        return result

class Used_Standard_Name_Entry(object):
    def __init__(self):
        self.used_as_nickname_by = []
        self.used_as_individual_name_by = []

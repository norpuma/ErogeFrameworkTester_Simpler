# # Minimal Location System
# - Set a Character's Location.
# - Get a Character's Location.

## DEPENDENCIES: Characters

def initalize_system(character_class_to_have_location):
    character_class_to_have_location.dynamic_initialization_functions.append(initialize_location_on_character)

def initialize_location_on_character(character):
    character.location = Location()

def default_reachable_locations(character, context):
    return list(Location.locations_database.keys())

class Location(object):
    locations_database = {}
    reachable_locations_default_function = default_reachable_locations
    def __init__(self, id, in_or_at, short_name):
        self.id = id
        self.in_or_at = in_or_at
        self.short_name = short_name
        self.short_descriptor = None
    
    def register_in_database(self):
        Location.locations_database[self.id] = self

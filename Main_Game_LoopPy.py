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
import PowerPlayFramework.LOCATIONS.LocationsPy as Locastions

class Game_System(object):
    def __init__(self):
        self.protagonist = None
        self.characters_database = None
        self.locations_database = None

system = Game_System()
system.protagonist = Characters.Character("PROTAGONIST", "Some name", "MALE", 25)

print("[+] Game initialized...")
print("[+] Protagonist is named '{0}'".format(system.protagonist.names))

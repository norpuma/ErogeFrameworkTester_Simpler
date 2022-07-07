# ## Story-Relevant Actions/Events
# - Protagonist is noticed by home mate.
# - Protagonist flirts with home mate.
# - Protagonist offers crude compliment to home mate.
# - Protagonist offers massage to home mate.
# - Protagonist passionately kisses home mate.
# - Protagonist starts an unasked for massage on home mate.
# - Protagonist starts unasked for groping on home mate.
# - Protagonist enters bedroom of home mate.
# - Protagonist pimps home mate.
# 
# ## Story-Relevant home mate Traits
# - Is nice
# - Is timid
# - Is liberated
# - Is uptight
# - Is dominant
# - Is lesbian
# - Hates protagonist
# - Loves (wants happy) protagonist
# - Has sexual history with protagonist
# - Has romantic relationship with protagonist
# - Has dominant relationship with protagonist
# - Has submissive relationship with protagonist
# - Has friendzoned relationship with protagonist
# - Has romantic relationship with another character
# - Has submissive relationship with another character
# - Feels intimacy with protagonist
# - Feels trust with protagonist
# - Feels safe with protagonist
# - Feels attraction to protagonist
# - Feels romantically-attracted to protagonist
# - Is currently bored
# - Is currently busy
# - Is currently changing
# - Is currently masturbating
# - Is currently sexually entertaining partner
# - Is currently camming
# ## Story-Relevant protagonist Traits
# - Has sexual history with home mate
# - Has romantic relationship with home mate
# - Has dominant relationship with home mate
# - Has submissive relationship with home mate
# - Has known romantic relationship with another character
# - Has known submissive relationship with another character
# - Has big penis
# - Has small penis
# - Is currently locked in chastity
# - Is currently unable to have erections
# - Is castrated
# - Is dominant
# - Is submissive

class Object(object):
    pass

class SUPER_SIMPLE_Character_Action(object):
    def __init__(self):
        self.check_action_is_possible_function = None

class SUPER_SIMPLE_Presentation_Elements(object):
    def __init__(self):
        pass
    
    def add_statement(self, character, *statement_elements):
        pass

ENUM__INTENSITIES__NOT = "NOT"
ENUM__INTENSITIES__SLIGHT = "SLIGHT"
ENUM__INTENSITIES__MODERATE = "MODERATE"
ENUM__INTENSITIES__INTENSE = "INTENSE"
ENUM__INTENSITIES__EXCESSIVE = "EXCESSIVE"

ENUM__COMPARATORS__EQUAL = "EQUAL"
ENUM__COMPARATORS__DIFFERENT = "DIFFERENT"
ENUM__COMPARATORS__GREATER_THAN = "GREATER_THAN"
ENUM__COMPARATORS__GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
ENUM__COMPARATORS__LESS_THAN = "LESS_THAN"
ENUM__COMPARATORS__LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"

def compare_intensities(intensity_1, comparator, intensity_2):
    intensity_1 = get_numeric_intensity(intensity_1)
    intensity_2 = get_numeric_intensity(intensity_2)
    if comparator == ENUM__COMPARATORS__EQUAL:
        return intensity_1 == intensity_2
    elif comparator == ENUM__COMPARATORS__DIFFERENT:
        return intensity_1 != intensity_2
    elif comparator == ENUM__COMPARATORS__GREATER_THAN:
        return intensity_1 > intensity_2
    elif comparator == ENUM__COMPARATORS__GREATER_THAN_OR_EQUAL:
        return intensity_1 >= intensity_2
    elif comparator == ENUM__COMPARATORS__LESS_THAN:
        return intensity_1 < intensity_2
    elif comparator == ENUM__COMPARATORS__LESS_THAN_OR_EQUAL:
        return intensity_1 <= intensity_2

def get_numeric_intensity(intensity, use_zero_based = False, use_exponential = False, multiplier = 0):
    value = 0
    if intensity == ENUM__INTENSITIES__NOT:
        value = 1
    elif intensity == ENUM__INTENSITIES__MODERATE:
        value = 2
    elif intensity == ENUM__INTENSITIES__INTENSE:
        value = 3
    else: # elif intensity == ENUM__INTENSITIES__EXCESSIVE:
        value = 4
    if use_zero_based:
        value -= 1
    if use_exponential:
        value = 10 ** value
    if multiplier != 0:
        value *= multiplier
    return value

def get_trait(perspective_owner, perspective_target, trait_key, trait_target = None, use_perspecitve_owners_model_for_target = True):
    pass

def register_trait_check_function(trait_key, check_function):
    pass

protagonist = Object()
home_mate = Object()
possible_actions = {}
possible_actions["NOTICED"] = SUPER_SIMPLE_Character_Action()
possible_actions["FLIRT"] = SUPER_SIMPLE_Character_Action()
possible_actions["OFFER_CRUDE_COMPLIMENT"] = SUPER_SIMPLE_Character_Action()
possible_actions["OFFER_MASSAGE"] = SUPER_SIMPLE_Character_Action()
possible_actions["PASSIONATELY_KISS"] = SUPER_SIMPLE_Character_Action()
possible_actions["START_UNASKED_FOR_MASSAGE"] = SUPER_SIMPLE_Character_Action()
possible_actions["START_UNASKED_FOR_GROPING"] = SUPER_SIMPLE_Character_Action()
possible_actions["ENTER_BEDROOM"] = SUPER_SIMPLE_Character_Action()
possible_actions["PIMP"] = SUPER_SIMPLE_Character_Action()

presentation_elements = SUPER_SIMPLE_Presentation_Elements()

def flirt__buid_presentation(actor, target, presentation_elements):
    presentation_elements.add_statement(protagonist, "Hi, there, gorgeous!", "You say, with a loaded smile.")
    flirt_build_presentation__reaction(protagonist, home_mate, presentation_elements)

def flirt_build_presentation__reaction(actor, target, presentation_elements):
    is_nice = compare_intensities(get_trait(None, target, "NICENESS"), ENUM__COMPARATORS__GREATER_THAN_OR_EQUAL, ENUM__INTENSITIES__MODERATE)
    is_timid = compare_intensities(get_trait(None, target, "TIMIDITY"), ENUM__COMPARATORS__GREATER_THAN_OR_EQUAL, ENUM__INTENSITIES__MODERATE)
    liberated_level = get_trait(None, target, "LIBERATED")
    dominant_level_towards_protagonist = get_trait(None, target, "DOMINANT", trait_target = protagonist)
    attracted_to_males_level = get_trait(None, target, "ATTRACTED_TO_MALES")
    romantic_relationship_level_with_protagonist = get_trait(None, target, "ROMANTIC_RELATIONSHIP", )
    if is_nice:
        if romantic_relationship_level_with_protagonist >= get_numeric_intensity(ENUM__INTENSITIES__MODERATE):
        # Check if protagonist has romantic relationship with target
        # Check if protagonist has sexual relationship with target
        # Check if home mate is attracted to protagonist
        # Check if home mate hates protagonist
        # Check if home mate loves protagonist
        # Check if home mate is romantically attracted to protagonist
        # Check if home mate has a dominant relationship with protagonist
        # Check if protagonist has a known romantic relationship with another character
        # Check if protagonist has a known sexual relationship with another character
        # Check if home mate is liberated or uptight
        # Check if home mate is lesbian
        # Check if home mate has friendzoned relationship with protagonist
            pass
    elif is_timid:
        pass
    elif liberated_level >= get_numeric_intensity(ENUM__INTENSITIES__MODERATE):
        pass
    elif liberated_level <= -1 * get_numeric_intensity(ENUM__INTENSITIES__MODERATE): # CHECKING FOR UPTIGHT
        pass
    elif dominant_level_towards_protagonist >= get_numeric_intensity(ENUM__INTENSITIES__MODERATE):
        pass
    elif dominant_level_towards_protagonist <= -1 * get_numeric_intensity(ENUM__INTENSITIES__MODERATE): # CHECKING FOR SUBMISSIVE
        pass
    elif attracted_to_males_level <= -1 * get_numeric_intensity(ENUM__INTENSITIES__MODERATE): # CHECKING FOR LESBIAN (or asexual)
        pass


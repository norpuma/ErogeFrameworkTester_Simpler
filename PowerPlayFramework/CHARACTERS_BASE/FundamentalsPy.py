import random

ENUM__FUNDAMENTALS__TRAITS__GENDER = "GENDER"
ENUM__FUNDAMENTALS__TRAITS__IS_FEMALE = "IS_FEMALE"
ENUM__FUNDAMENTALS__TRAITS__IS_MALE = "IS_MALE"
ENUM__FUNDAMENTALS__TRAITS__AGE = "AGE"
ENUM__FUNDAMENTALS__TRAITS__AGE_GROUP = "AGE_GROUP"
ENUM__FUNDAMENTALS__TRAITS__IS_OLDER = "IS_OLDER"
ENUM__FUNDAMENTALS__TRAITS__IS_OLD = "IS_OLD"
ENUM__FUNDAMENTALS__TRAITS__IS_YOUNGER = "IS_YOUNGER"
ENUM__FUNDAMENTALS__TRAITS__IS_YOUNG = "IS_YOUNG"

ENUM__CONTEXT__CHARACTER_CREATION = "CONTEXT__CHARACTER_CREATION"

ENUM__INTENSITIES__NONE = 0
ENUM__INTENSITIES__SLIGHT = 1
ENUM__INTENSITIES__MODERATE = 2
ENUM__INTENSITIES__INTENSE = 3
ENUM__INTENSITIES__EXCESSIVE = 4
INTENSITIES = [
    ENUM__INTENSITIES__NONE,
    ENUM__INTENSITIES__SLIGHT,
    ENUM__INTENSITIES__MODERATE,
    ENUM__INTENSITIES__INTENSE,
    ENUM__INTENSITIES__EXCESSIVE,
]

class Gender(object):
    FEMALE = "FEMALE"
    MALE = "MALE"
    def __init__(self):
        pass

    @classmethod
    def generate_random(cls):
        return random.choice([Gender.FEMALE, Gender.MALE])

class Pronouns(object):
    def __init__(self, subject, subject_capitalized, object, object_capitalized, possessive, possessive_capitalized, possessive_pronouns, possessive_pronouns_capitalized, reflexive, reflexive_capitalized):
        self.subject = subject
        self.subject_capitalized = subject_capitalized
        self.object = object
        self.object_capitalized = object_capitalized
        self.possessive = possessive
        self.possessive_capitalized = possessive_capitalized
        self.possessive_pronouns = possessive_pronouns
        self.possessive_pronouns_capitalized = possessive_pronouns_capitalized
        self.reflexive = reflexive
        self.reflexive_capitalized = reflexive_capitalized

female_pronouns = Pronouns(
    subject = "she",
    subject_capitalized = "She",
    object = "her",
    object_capitalized = "Her",
    possessive = "her",
    possessive_capitalized = "Her",
    possessive_pronouns = "hers",
    possessive_pronouns_capitalized = "Hers",
    reflexive = "herself",
    reflexive_capitalized = "Herself"
)

male_pronouns = Pronouns(
    subject = "he",
    subject_capitalized = "He",
    object = "him",
    object_capitalized = "Him",
    possessive = "his",
    possessive_capitalized = "His",
    possessive_pronouns = "his",
    possessive_pronouns_capitalized = "His",
    reflexive = "himself",
    reflexive_capitalized = "Himself"
)

class Age_Group(object):
    ENUM__AGE_GROUP__CHILD = "ENUM__AGE_GROUP__CHILD"
    ENUM__AGE_GROUP__TEEN = "ENUM__AGE_GROUP__TEEN"
    ENUM__AGE_GROUP__YOUNG_ADULT = "ENUM__AGE_GROUP__YOUNG_ADULT"
    ENUM__AGE_GROUP__ADULT = "ENUM__AGE_GROUP__ADULT"
    ENUM__AGE_GROUP__MATURE_ADULT = "ENUM__AGE_GROUP__MATURE_ADULT"
    ENUM__AGE_GROUP__ELDER = "ENUM__AGE_GROUP__ELDER"
    ordered_available_age_groups = [
        ENUM__AGE_GROUP__CHILD,
        ENUM__AGE_GROUP__TEEN,
        ENUM__AGE_GROUP__YOUNG_ADULT,
        ENUM__AGE_GROUP__ADULT,
        ENUM__AGE_GROUP__MATURE_ADULT,
        ENUM__AGE_GROUP__ELDER,
    ]
    min_age_by_age_group = {
        ENUM__AGE_GROUP__CHILD: 10,
        ENUM__AGE_GROUP__TEEN: 18,
        ENUM__AGE_GROUP__YOUNG_ADULT: 21,
        ENUM__AGE_GROUP__ADULT: 26,
        ENUM__AGE_GROUP__MATURE_ADULT: 35,
        ENUM__AGE_GROUP__ELDER: 50,
    }
    MAX_AGE = 70
    def __init__(self, id):
        if id not in Age_Group.ordered_available_age_groups:
            raise ValueError("ERROR: Age_Group:__init__(): Age group '{0}' is not a valid age group.".format(id))
        self.id = id
        min = Age_Group.min_age_by_age_group[self.id]

    @classmethod
    def next_age_group(cls, age_group):
        if age_group not in Age_Group.ordered_available_age_groups:
            raise ValueError("ERROR: Age_Group:next_age_group(): Age group '{0}' is not a valid age group.".format(age_group))
        index = Age_Group.ordered_available_age_groups.index(age_group)
        if index < len(Age_Group.ordered_available_age_groups)-1:
            return Age_Group.ordered_available_age_groups[index+1]
        else:
            return None
    
    @classmethod
    def get_age_group_min_and_max(cls, age_group):
        if age_group not in Age_Group.ordered_available_age_groups:
            raise ValueError("ERROR: Age_Group:next_age_group(): Age group '{0}' is not a valid age group.".format(age_group))
        index = Age_Group.ordered_available_age_groups.index(age_group)
        lower = Age_Group.ordered_available_age_groups[index]
        min = Age_Group.min_age_by_age_group[lower]
        if index < len(Age_Group.ordered_available_age_groups)-1:
            upper = Age_Group.ordered_available_age_groups[index+1]
            max = Age_Group.min_age_by_age_group[upper]-1
        else:
            max = Age_Group.MAX_AGE
        return (min, max)

    @classmethod
    def get_age_group_from_age(cls, age):
        if age < Age_Group.min_age_by_age_group[Age_Group.ENUM__AGE_GROUP__CHILD]:
            return Age_Group.ENUM__AGE_GROUP__CHILD
        elif age < Age_Group.min_age_by_age_group[Age_Group.ENUM__AGE_GROUP__TEEN]:
            return Age_Group.ENUM__AGE_GROUP__TEEN
        elif age < Age_Group.min_age_by_age_group[Age_Group.ENUM__AGE_GROUP__YOUNG_ADULT]:
            return Age_Group.ENUM__AGE_GROUP__YOUNG_ADULT
        elif age < Age_Group.min_age_by_age_group[Age_Group.ENUM__AGE_GROUP__ADULT]:
            return Age_Group.ENUM__AGE_GROUP__ADULT
        elif age < Age_Group.min_age_by_age_group[Age_Group.ENUM__AGE_GROUP__MATURE_ADULT]:
            return Age_Group.ENUM__AGE_GROUP__MATURE_ADULT
        else: # elif age < Age_Group.min_age_by_age_group[Age_Group.ENUM__AGE_GROUP__ELDER]:
            return Age_Group.ENUM__AGE_GROUP__ELDER

characters_database = {}

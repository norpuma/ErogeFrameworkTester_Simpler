# - Given an Actor, a Target, a Context and an Action, determine a character's Update and Reaction to the Action.
# -- Perspective owner can check Traits on Actor and Target, Status, History, Reputation

# Dependencies: MIND, ACTION, TRAITS, STATUS

from ..MIND.MindPy import ENUM__ACCEPTANCE__INDIFFERENT


def evaluate_acceptance_to_action(perspective_owner, action, actor, target, context):
    return ENUM__ACCEPTANCE__INDIFFERENT

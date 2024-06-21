from enum import Enum


class DataComponentTypes(Enum): #TODO - this enum isn't pulling its weight... should be lumped in with the relevant tracked point data classes somehow
    BODY = "body"
    FACE = "face"
    RIGHT_HAND = "right_hand"
    LEFT_HAND = "left_hand"

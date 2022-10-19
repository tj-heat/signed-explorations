from typing import Dict, List, Tuple
import arcade

# Asset constants
CAT_HEAD_ICON = "assets/ui/Cat_Face.png"
DOG_HEAD_ICON = "assets/ui/Dog_Face.png"

CAT_SPEAKER = arcade.Sprite(texture=arcade.load_texture(CAT_HEAD_ICON))
DOG_SPEAKER = arcade.Sprite(texture=arcade.load_texture(DOG_HEAD_ICON))

# Access constants
MSGS = "msgs"
SPEAKER = "speaker"

# All dialogue
DIALOGUE_INTRODUCTION_P1 = {
    MSGS: [
        "Before you stands a dog.",
        "He is happy to see you.",
        "In his hands is a keyboard. (Where did he get that from?)",
        "He uses it to give you a demonstration."
    ],
    SPEAKER: None,
}

DIALOGUE_INTRODUCTION_P2 = {
    MSGS: [
        "You can use <W> <A> <S> <D> to move about.",
        "<E> is used to interact with the world around you.",
        "<I> opens your spell(ing) book.",
        "<Q> can also call me to your side.",
    ],
    SPEAKER: DOG_SPEAKER,
}

DIALOGUE_INTRODUCTION_P3 = {
    MSGS: [
        "I think my body is just up ahead!",
    ],
    SPEAKER: CAT_SPEAKER,
}

KEY_FIRST = {
    MSGS: [
        "I left my keys in my other body.",
    ],
    SPEAKER: CAT_SPEAKER
}

BRIDGE_MIDDLE = {
    MSGS: [
        "L'appel du vide...",
    ],
    SPEAKER: CAT_SPEAKER,
}

PUZZLE_INTERACT = {
    MSGS: [
        "Your paw passes straight through.",
    ],
    SPEAKER: None,
}

MARBLE_FLOOR = {
    MSGS: [
        "This marble feels cold... I think?",
    ],
    SPEAKER: CAT_SPEAKER,
}

def get_msgs(topic: Dict) -> List[str]:
    """ Get the message for a given topic. 
    
    Params:
        topic (str): the name of the topic to get the message for

    Returns:
        (List) The messages for the given topic
    """
    return topic.get(MSGS)

def get_dialogue(topic: Dict) -> Tuple[List[str], arcade.Sprite]:
    """ Get the message and speaker for a given topic. 
    
    Params:
        topic (str): the name of the topic to get the message for

    Returns:
        (Typle) The messages for the given topic and the associated speaker
    """
    return (get_msgs(topic), topic.get(SPEAKER))
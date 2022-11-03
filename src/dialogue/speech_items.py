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
        "He starts barking at you, but you don't understand Dog.",
        "You meow back, but he looks confused.",
        "He turns around and suddenly and there's...",
        "a keyboard in his mouth?",
        "Where did he get that from?",
        "He uses it to give you a demonstration."
    ],
    SPEAKER: None,
}

DIALOGUE_INTRODUCTION_P2 = {
    MSGS: [
        "You can use <W> <A> <S> <D> to move about.",
        "<E> is used to interact with the world around you.",
    ],
    SPEAKER: DOG_SPEAKER,
}


#remove
DIALOGUE_INTRODUCTION_P3 = {
    MSGS: [
        "I think my body is just up ahead!",
    ],
    SPEAKER: CAT_SPEAKER,
}

PICK_UP_SPELLBOOK = {
    MSGS: [
        "You've found a spell(ing) book!",
        "as you hover above it, the spell[ing] book disappears.",
        "Use <I> to open the spell(ing) book.",
    ],
    SPEAKER: CAT_SPEAKER,
}

OPEN_SPELLBOOK = {
    MSGS: [
        "This is where you stored your fingerspelling spells!",
        "Each of these signs correlates to a letter.",
        "If you fingerspell out multiple letters to form a word"
        "you can cast powerful magic.",
        "It doesn't look like any of the spells are active.",
        "You should look around more.",
        "Maybe you can use it to talk."
    ],
    SPEAKER: CAT_SPEAKER,
}

KEY_FIRST = {
    MSGS: [
        "You think you might need this key later.",
    ],
    SPEAKER: CAT_SPEAKER
}

GOT_FIRST_KEY = {
    MSGS: [
        "You think that could open the door!",
        "You might have to push the dog through, however."
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
        "Your ghostly paw passes straight through.",
    ],
    SPEAKER: None,
}

MARBLE_FLOOR = {
    MSGS: [
        "You wonder if the merble feels cold",
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
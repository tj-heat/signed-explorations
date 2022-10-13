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
DIALOGUE_INTRODUCTION = {
    MSGS: [
        "Before you stands a dog.",
        "He is happy to see you.",
        "In his hands is a keyboard. (Where did he get that from?)",
        "You can use <W> <A> <S> <D> to move your character.",
        "<E> is used to interact with the world around you.",
        "<Q> can also call the dog to your side.",
    ],
    SPEAKER: None,
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
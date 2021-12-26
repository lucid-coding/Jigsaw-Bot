# pylint: disable=too-few-public-methods
"""
A file where most the constants are stored
"""
BOTNAME = "909028270517932064"


class Emojis:
    """
    A Emoji class
    ---
    Lists -> Trash_Emojis,Pepe_sad_Emojis
    Strings -> pensive, mod_button, fun_button ,info_button, sus_emoji
    Methods -> None
    """

    pensive = "😔"
    pepe_sad_emojis = [
        "<a:CH_PepeSadCry:918905686178553867>",
        "<:CH_PepeSadLove:918905725542080522> ",
        "<:Pepe:918905546604691556>",
        "<:k_pepesadhug:918905636522176512>",
        "<a:pepesadrain:918905666423390218>",
    ]
    trash_emojis = [
        "<:OH_peepoTrash:743662557226598460>",
        "<a:LS_PepeTrash:919229878971273236>",
        "<:trash:701267250006458508>",
    ]
    info_button = "<:info_button:919628823446839436>"
    fun_button = "<a:DanceLightSaber:793880620782190592>"
    mod_button = "<:moderator:857241458889195571>"
    sus_emoji = "<:suspeepo:920001743536926782>"


class Colors:
    """
    A class to store all the used Colors.
    HexCode -> Colors
    Methods -> None
    """

    blue = 0x0000FF
    red = 0x992D22
    green = 0x1F8B4C
    yellow = 0xFFFF00
    pink = 0xFFC0CB
    gray = 0x808080


class Replies:
    """
    A Class that stores Replies
    ---
    List -> postive_replies,negative_replies
    Methods -> None
    """

    positive_replies = [
        "Yep.",
        "Absolutely!",
        "Can do!",
        "Affirmative!",
        "Yeah okay.",
        "Sure.",
        "Sure thing!",
        "You're the boss!",
        "Okay.",
        "No problem.",
        "I got you.",
        "Alright.",
        "You got it!",
        "ROGER THAT",
        "Of course!",
        "Aye aye, cap'n!",
        "I'll allow it.",
    ]

    error_replies = [
        "Please don't do that.",
        "You have to stop.",
        "Do you mind?",
        "In the future, don't do that.",
        "That was a mistake.",
        "You blew it.",
        "You're bad at computers.",
        "Are you trying to kill me?",
        "Noooooo!!",
        "I can't believe you've done this",
    ]

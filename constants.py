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

    ZeroTwoHug = "<:02hug:838664910128021514>"
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
    economy_button = '<:economy_button:941016748109488130>'
    welcome_button = '<:welcome_button:941016748109488130>'
    sus_emoji = "<:suspeepo:920001743536926782>"
    currency_emoji = "<:currency:939966655134588938>"


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
    List -> welcome_back_replies, error_replies, postive_replies,
    Methods -> None
    """

    welcome_back_replies = [
        "great to see you again",
        "hey you've gone for some time. we've missed you",
        "some time has passed.",
        "oh look, its you again ",
        "No matter how far we may wander from the Lord’s perfect will for our lives, we are always welcome back!",
    ]
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
    begging_responds = [
        "be gone",
        "coin.exe has stopped working",
        "I only give money to my mommy",
        "go ask someone else",
        "Well, let's ask another person ",
        "I share money with no-one",
        "the atm is out of order, sorry",
        "bye jerk, no coins for you ",
        "ew no",
        "Back in my day we worked for a living",
        "I would not share with the likes of you (based on your race)",
        "honestly why are you even begging, get a job",
        "ew get away",
        "can you not",
        "nah, would rather not feed your gambling addiction",
        "I need my money to buy airpods",
        "ur too stanky",
        "ur not stanky enough ",
        "Oh hell/BAD-WORD nah",
        "stop begging",
        "Sure take this nonexistent coin",
        "no coins for you",
        "there. is. no. coins. for. you.",
        "You get nothing",
        "no u",
        "Get a job you hippy",
        "No way, you'll just use it to buy pink phallics",
        "I give people nothing ",
        "get the heck/censored out of here, you demon!",
        "I would sooner spend money on taxes than giving you anything",
        "get lost u simp ",
        "get out of here, moron, get clapped on!",
        "I don't share with the n-words ",
        "pull urself up by your bootstraps scrub ",
        "HeRe In AmErIcA wE dOnT dO cOmMuNiSm",
        "Imagine begging in 2022, gofundme is where it is at",
    ]

class ImageUrls:
    """
    A class to taht stores ImageUrls that are constants
    """
    win_url = 'https://cdn.discordapp.com/attachments/939956056795262978/939958253759111228/unknown.png'
    lose_url = 'https://cdn.discordapp.com/attachments/939956056795262978/939958253759111228/unknown.png'
    treasure_url = 'https://cdn.discordapp.com/attachments/939956056795262978/939957865010053160/unknown.png'
    bank_url = 'https://cdn.discordapp.com/attachments/918891402224611379/939944596664881182/unknown.png'
    bag_url = 'https://cdn.discordapp.com/attachments/939956056795262978/939958931239878656/unknown.png'
    error_url = 'https://cdn.discordapp.com/emojis/601404540444737536.png'
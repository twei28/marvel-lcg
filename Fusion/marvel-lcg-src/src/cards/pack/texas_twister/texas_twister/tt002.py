from . import *

# * Shooting Star (Victoria Star) — ALLIE, cout 3, PV 3, CTR 1* / ATQ 2*.
#   RANGER. [physical].
# Response: After Shooting Star enters play, ready Texas Twister.
#
# CARTES DE REFERENCE
#  - `bk016` Tallus : `AfterCardEnterPlay` en Reponse, meme montage.
#  - `14001a` Quicksilver : `Faces.ReadyAll` sur l'identite.
#
# TEXTE CONTRE CODE
#  « ready TEXAS TWISTER » -> l'IDENTITE HEROS, pas l'alliee : jouer Shooting
#    Star rend un pouvoir de base au heros, ce qui relance toute la chaine du
#    pack. Elle ne se redresse pas elle-meme.
#  ⚠ Le heros peut etre en forme CIVILE au moment ou elle arrive : `HerosDuJoueur`
#    rend alors None et la Reponse ne fait rien, ce qui est le comportement
#    juste (« Texas Twister » n'est pas en jeu).


def GetAbilities() -> Sequence['Ability']:

    def etoile_filante(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        heros = HerosDuJoueur(effect)
        if heros is not None:
            Faces.ReadyAll([heros], effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            etoile_filante,
        ),
    ]

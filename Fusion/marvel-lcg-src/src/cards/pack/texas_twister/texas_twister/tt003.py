from . import *

# Accelerated Rotation — EVENEMENT, cout 0, [mental]. SUPERPOWER.
# Hero Action: Texas Twister gets +1 THW, +1 ATK, and +1 DEF until the end of
#   the round.
#
# CARTE DE REFERENCE
#  - `12016` Moxie : `GainUntilRoundEnd(effect, attack=1, thwart=1, defense=1)`.
#
# TEXTE CONTRE CODE
#  LES TROIS POUVOIRS D'UN COUP, contrairement a tt001a qui n'en donne qu'un,
#    celui qui vient de servir. C'est le contraste imprime du pack.
#  ⚠ AUCUN libelle `(attack)` ni `(thwart)` sur cette carte : c'est une Hero
#    Action seche, elle ne consomme pas l'attaque du tour. `SetLabel` serait
#    une invention.
#  « until the end of the ROUND » -> le bonus survit a la phase du vilain.


def GetAbilities() -> Sequence['Ability']:

    def rotation_acceleree(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        heros = HerosDuJoueur(effect)
        if heros is not None:
            heros.GainUntilRoundEnd(effect, attack=1, thwart=1, defense=1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            rotation_acceleree,
        ).SetPlay(),
    ]

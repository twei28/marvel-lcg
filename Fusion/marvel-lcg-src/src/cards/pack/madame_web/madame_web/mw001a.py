from . import *

# * Madame Web — custom « Kajislav »
# A Bond with the Allies — Madame Web gains the traits of each ally you control.
# X is equal to the number of allies you control (to a maximum of 3).
#
# ATK/THW/DEF sont imprimes « X » sur la carte : cards.json les declare a 0 et
# les deux fabriques ci-dessous les remontent a min(nb_allies, 3).

def GetAbilities() -> Sequence['Ability']:

    def nombre_allies(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Hero)

        player = this.GetControlByPlayer()
        allies = player.GetControlAllies()
        for ally in allies[:3]:
            ui.append(ally)
        return min(3, len(allies))

    return [
        AbilityFactory.ThisGainKeyword(
            nombre_allies,
            attack=1,
            thwart=1,
            defense=1,
            change_on_event=OnEvent.CardInPlay(Ally),
        ).SetName("X"),
        AbilityFactory.ThisGainTraitsOfEachCardInPlay(
            Ally,
        ).SetName("A Bond with the Allies"),
    ]

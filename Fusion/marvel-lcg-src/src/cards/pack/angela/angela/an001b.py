from . import *

# * Aldrif Odinsdottir (face alter-ego)
# ASGARD.  REC 4* — HS 6 / PV 13
# Setup: Search your deck and discard pile for a WEAPON card and add it to
#   your hand. Shuffle your deck.
# [star] Of Heven and Hel — Aldrif Odinsdottir gets +1 REC for each WEAPON
#   you control.
#
# Cartes de reference :
#  - Setup : ok001b * Okoye (pack okoye), jumeau exact — meme
#    `WhenCardSetup` + `Search.PlayerCard(include_player_deck=True,
#    include_discard_pile=True, trait=...)` + `GainCard`. T'Challa 01040b est
#    le modele d'origine, mais il ne fouille QUE le deck.
#  - +1 REC par arme : dt133 * Orka / 12011 Ant-Man, motif
#    `ThisGainKeyword(<compteur>, recover=1, change_on_event=...)`.
#
# `OnEvent.CardInPlay(Unit2)` ne suffirait pas : une arme est une AMELIORATION,
# pas une unite. On surveille donc l'entree en jeu de n'importe quelle carte.

def GetAbilities() -> Sequence['Ability']:

    def setup_arme(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            trait="WEAPON",
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            setup_arme,
        ),
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: ArmesControlees(effect),
            recover=1,
            change_on_event=OnEvent.CardInPlay(CardFace),
        ),
    ]

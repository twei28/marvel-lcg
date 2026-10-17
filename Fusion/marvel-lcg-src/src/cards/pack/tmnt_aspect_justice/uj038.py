from . import *

# * Wingnut — ALLIE 3 [mental], aspect Justice (TMNT Reskins, Inkwire). AERIAL. BAT. DIMENSION X.
# Bandeau « ✦ Cloak » (unique_also, decision Q-R1).
# PV 2, THW 2, ATK 1 (aucun degat consecutif). [acceleration] (desc.Acceleration = 1).
# Action: Exhaust Wingnut and spend [energy][energy] resources → find Screwloose and put him into play.
#
# MODIFIEE par rapport a `60020` Cloak (Tyrone Johnson) : « Dagger »/« her » -> « Screwloose »/« him ». Le
# module de 60020 cherche le NOM « Dagger » en dur : pas d'`ability_link` possible (RECETTES §11 point 3),
# script propre, copie de 60020 au nom pres.
#
# MOT-CLE (fiche lue) : ACCELERATION — acceleration.md : icone lue dans `desc.Acceleration`, aucun code.
#
# CARTES DE REFERENCE
#  - `60020` Cloak : `WhenInYourPlayTurn(Action, op).SetCostFunc(Exhaust("This")).SetCostFunc(Spend(Cost('YY')))`
#    + `Search.PlayerCard(..., include_player_deck, include_discard_pile, include_player_hand_cards, name=...)`
#    puis `PutIntoPlay`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « Exhaust Wingnut AND spend [energy][energy] → » : deux couts, tous les deux.
#  ⚠ « find Screwloose » : deck, defausse et main (« find » = chercher partout ou le joueur a ses cartes,
#    lecture de 60020 reprise telle quelle) ; mis en jeu SANS payer.


def GetAbilities() -> Sequence['Ability']:

    def wingnut(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(effect, initiator, include_player_deck=True, include_discard_pile=True,
                                 include_player_hand_cards=True, name='Screwloose')
        if face:
            face.CastTo(Ally).PutIntoPlay(initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, wingnut)
        .SetCostFunc(CostFunc.Exhaust('This'))
        .SetCostFunc(CostFunc.Spend(Cost('YY'))),
    ]

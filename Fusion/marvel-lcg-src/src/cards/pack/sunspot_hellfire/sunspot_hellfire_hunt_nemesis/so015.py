from . import *

# Cybernetic Assault — TRAITRISE de l'ennemi juré, boost 1, x2.
# When Revealed: Donald Pierce attacks you. If he is not in play, search the encounter deck and discard pile for Donald
#   Pierce and put him into play engaged with you.
#
# CARTES DE REFERENCE
#  - `01164` Titania's Fury : `Worlds.FindCardOnField(effect, name=.., card_type=Minion)` puis `minion.DoAttackYou(player, effect)`.
#  - `11051` Ancient Grudge : `Search.EncounterCard(effect, player, include_discard_pile=True, name=..)` puis `PutIntoPlay(player, effect)`.
#
# ⚠ ARBITRAGE PROVISOIRE (voir le gabarit) : le texte ne dit pas si Pierce, tout juste mis en jeu, attaque aussi. Lecture retenue :
#   en jeu -> il attaque ; absent -> on le met en jeu engage avec le joueur (son Quickstrike le fait alors attaquer en forme heros).


def GetAbilities() -> Sequence['Ability']:

    def cybernetic_assault(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        joueur = message.GetToPlayer()
        pierce = Worlds.FindCardOnField(effect, name="Donald Pierce", card_type=Minion)
        if pierce:
            pierce.DoAttackYou(joueur, effect)
            return
        pierce = Search.EncounterCard(effect, joueur, include_discard_pile=True, name="Donald Pierce")
        if pierce:
            pierce.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            cybernetic_assault,
        ),
    ]

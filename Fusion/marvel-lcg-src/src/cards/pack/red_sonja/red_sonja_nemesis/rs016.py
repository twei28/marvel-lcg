from . import *

# * Ice Queen — MINION, RED SONJA NEMESIS (2/5). SCH 2, ATK 2, HP 5. ELITE.
# MYSTIC. Boost 5.
# When Defeated: The defeating player discards cards from the top of the
# encounter deck and reveals the first minion discarded this way.
# (Red Sonja's nemesis minion.)
# [star] Boost: Put this minion into play engaged with you.
#
# CARTES DE REFERENCE
#  - `01182` Hydra Soldier (officiel) : `AbilityFactory.WhenUnitBeDefeated
#    (AbilityType.WhenDefeated, "This", operation)`.
#  - `ar001a` Bring the War : `Worlds.DiscardEncounterCardsUntil(effect,
#    card_type=Minion)` pour « discard from the top ... until [a minion] »
#    (le mot-cle maison `seek`, defini dans l'insert de spider_man_2099).
#  - `56109` S.H.I.E.L.D. Soldier (officiel) :
#    `AbilityFactory.WhenCardBecomeBoost("This", PutThisIntoPlay)`.
#
# TEXTE CONTRE CODE : « THE DEFEATING PLAYER », pas « the engaged player » :
# `message.GetKillerPlayer()` (l'auteur de la defaite), pas
# `this.GetEngagedPlayer()`.
#
# ⚠⚠ `effect.GetInitiator()` PLANTE (ASSERTIONERROR), IL NE REND PAS None
# (23/09/2026, bug trouve par le cas de test de cette carte). `Effect.
# GetInitiator()` (effect.py:417) fait `assert isinstance(self.initiator,
# Player)` -- si l'initiateur n'est PAS un joueur (ici, un `Puzzle.Damage`
# sans source explicite attribue la defaite au VILAIN lui-meme), l'appel leve
# AVANT que la garde `isinstance(joueur, Player)` du code appelant n'ait la
# moindre chance de s'executer. `message.GetKillerPlayer()`
# (sender_unit.py:94, ou `message.defeating_player`) est le pendant SANS
# assertion : il rend `None` proprement quand le tueur n'a pas de
# controleur-joueur, exactement le cas que ce code veut ecarter.

def GetAbilities() -> Sequence['Ability']:

    def ice_queen(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        joueur = message.GetKillerPlayer()
        if isinstance(joueur, Player):
            Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            ice_queen,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            PutThisIntoPlay,
        ),
    ]

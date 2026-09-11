from . import *
# Battle for a Soul — MANIGANCE ANNEXE nemesis, 2 menaces, boost 2.
# Blackheart gets +X SCH and Daimon Hellstrom gets +X ATK, where X is the
#   number of cards attached to Hellcat.
# Forced Interrupt: When Blackheart or Daimon Hellstrom activate, they also
#   activate against the player the other is engaged with.
#
# Modeles : `GiveKeywordToInPlayWhenApplyThis(finder, scheme=1,
# get_new_value=fn)` (environment.py:66 ; `get_new_value` REMPLACE la valeur,
# environment_helper.py:184), `WhenEnemyWouldActivate` (activate.py:6),
# `Enemy.DoActivate(against_player, effect)` (enemy.py:208).
# ⚠ `GiveKeywordToInPlayWhenApplyThis` rend une LISTE : deballage `*` obligatoire
#   (meme piege que `GiveKeywordToAttached`, ma006). Sans lui : « 'list' object
#   has no attribute 'paper' » au setup, vu le 11/09/2026.
# ⚠ X se lit sur la CARTE identite de Hellcat (zone des cartes glissees),
#   quelle que soit sa face.

def GetAbilities() -> Sequence['Ability']:

    def x_accrochees(effect: 'Effect', face: 'CardFace') -> int:
        Unused(face)
        for joueur in Worlds.GetPlayers(effect):
            identite = joueur.GetIdentity()
            if identite.IsName(HELLCAT) or identite.IsName(PATSY):
                return len(CartesAttacheesA(identite))
        return 0

    def battle_for_a_soul(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        demon = message.trigger.CastTo(Minion)
        autre = AutreDemon(effect, DAIMON if demon.IsName(BLACKHEART) else BLACKHEART)
        if autre is None:
            return
        cible = autre.GetEngagedPlayer()
        if cible is None or cible is message.player:
            return
        demon.DoActivate(cible, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name=BLACKHEART, card_type=Minion),
            scheme=1,
            get_new_value=x_accrochees,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name=DAIMON, card_type=Minion),
            attack=1,
            get_new_value=x_accrochees,
        ),
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.ForcedInterrupt,
            CardFinder(name=BLACKHEART, card_type=Minion) | CardFinder(name=DAIMON, card_type=Minion),
            battle_for_a_soul,
        ),
    ]

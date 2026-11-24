from . import *

# * Hellbride — SBIRE. DEMON. HAND. SCH 1 / ATQ 3 / PV 7, Boost 3.
# When Defeated : The defeating player places 2 corruption counters on their Creeping Corruption, then heals 6 damage from their identity.
# Hero Action : If Hellbride has 2 or fewer remaining hit points, exhaust your hero → discard Hellbride. Remove 1 corruption counter from your Creeping Corruption.
#
# Cartes de reference : sl006 (`WhenUnitBeDefeated(WhenDefeated, "This")`, joueur qui vainc), 01153 Concussion Blasters (`CostFunc.Exhaust("YourHero")` d'une Hero Action ennemie),
# 27016 / drs 09016 (soin d'identite : `HealHealth`).
# ⚠ Mots-pieges : « THE DEFEATING player » : le joueur qui controle ce qui a vaincu Hellbride (`message.defeating_player`), pas forcement celui engage ; sans joueur vainqueur (degats sans source
#  joueur) rien n'est fait ; « places 2 counters, THEN heals 6 » : dans cet ordre (le seuil de 5 peut tomber avant le soin) ; « heals 6 damage FROM THEIR IDENTITY » : au plus 6 ; « IF Hellbride has 2 or
#  fewer REMAINING hit points » : condition d'OFFRE de l'action (PV restants <= 2, pas les degats subis) ; « exhaust YOUR hero » : le cout ; « DISCARD Hellbride » : defausse, PAS une defaite (pas de
#  When Defeated) ; « Remove 1 corruption counter » est un effet, apres la defausse.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        joueur = getattr(message, 'defeating_player', None)
        if joueur is None:
            return
        PlacerCorruption(effect, joueur, 2)
        joueur.GetIdentity().HealHealth(6, effect)

    def en_fin_de_vie(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return effect.this.CastTo(Minion).health <= 2

    def congedier(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.DiscardAll([effect.this], effect)
        joueur = effect.GetInitiator()
        if joueur is not None:
            RetirerCorruption(effect, joueur)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, congedier, conditions=[en_fin_de_vie])
            .SetCostFunc(CostFunc.Exhaust("YourHero")),
    ]

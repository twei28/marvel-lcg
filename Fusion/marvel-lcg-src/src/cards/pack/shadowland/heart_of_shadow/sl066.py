from . import *

# * Fist — SBIRE. HAND. UNDEAD. SCH 2 / ATQ 2 / PV 6, Boost 2.
# Patrol. Retaliate 2.
# Hero Action : Place 1 corruption counter on your Creeping Corruption → deal 4 damage to Fist.
#
# Cartes de reference : 01153 Concussion Blasters et 27150 Neocarbon Scales (Hero Action d'une carte ENNEMIE qui paie par `SetCostFunc`), iron_man_model_42 `CoutDuReacteur` (jeton pose PAR LE COUT, impayable
# sans cible), 01152 / 01102 pour Patrol et Retaliate (lus dans `desc`, fiches patrol.md et retaliate.md : rien a coder).
# ⚠ Mots-pieges : « deal 4 damage TO FIST » : a Fist lui-meme, pas a un autre ennemi ; ce ne sont PAS des degats d'attaque (pas de riposte, Toughness absorbe) ; le jeton est un COUT : sans
#  Creeping Corruption l'action n'est pas offerte ; « Hero » Action : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def frapper(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Minion)
        this.DealDamage([this], 4, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, frapper, conditions=[PeutPayerCorruption])
            .SetCostFunc(CoutPlacerCorruption(1)),
    ]

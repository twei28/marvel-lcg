from . import *

# Intruder Alert! — ATTACHEMENT (Security Protocol 5/7, x3). 1 boost + etoile. Icone Crisis.
# Attach to your identity.
# Action: Take 2 damage or exhaust your identity -> discard this card.
# [star] Boost: Reveal this card.
#
# Cartes de reference : `ma017` Edges Syndrome (`PlayerActionToDiscardThis(AbilityType.Action)` +
# `CostFunc.TakeDamage(2, "YourIdentity")`, « Action » nu = les DEUX formes) ; `aa018` pour « X or Y » en
# deux actions (`CostFunc.Exhaust`) ; `wd111` pour « Attach to your identity » ; `RevealThisCard` pour le Boost
# (modele 04092). Crisis : base automatique (`desc.Crisis`), fiche mots-cles/crisis.md.
#
# Mots-pieges : « Take 2 damage » = cout paye par l'IDENTITE ; « exhaust your IDENTITY » (heros ou alter-ego,
# a la difference de « your hero ») ; « Action » (pas Hero Action) ; deux couts alternatifs = deux capacites.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.Action,
        ).SetCostFunc(CostFunc.TakeDamage(2, "YourIdentity")),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.Action,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]

from . import *

# Elite Guard (x2) — SBIRE. FOOT CLAN. NINJA. MNG 1 / ATQ 2 / PV 3, 1 icone de boost + etoile.
# Guard. Patrol.
# When Revealed: Cloak Shredder.
# [star] Boost: Give Shredder a tough status card.
#
# Cartes de reference : `01101` Hydra Mercenary (Guard, lu dans `desc`) ; Patrol
# idem (fiche patrol.md) ; `ts004b` pour « Cloak Shredder » ; `fne 60149`
# (boost « give ... a tough status card » : `Faces.GiveStatus([...], "Tough")`).
#
# Mots-pieges : « Cloak SHREDDER » (le vilain, pas la garde) ; boost : « Give
# SHREDDER a tough » (pas « the activating enemy »).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Cloak(effect, TrouverShredder(effect))

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        shredder = TrouverShredder(effect)
        if shredder:
            Faces.GiveStatus([shredder], "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]

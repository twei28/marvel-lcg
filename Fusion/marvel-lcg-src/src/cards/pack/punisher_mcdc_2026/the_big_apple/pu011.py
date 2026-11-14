from . import *

# * Bellona — SBIRE UNIQUE. CLONE. CRIMINAL. MUTANT. SCH 1, ATQ 1★, 5 PV, Boost 3.
# Toughness. Villainous.
# ★ Bellona's attacks gain piercing.
# When Defeated : Shuffle Bellona into the encounter deck. The defeating player may take 2 damage to discard her instead.
#
# Cartes de reference : aos/batrocs_brigade/50098.py (Machete : piercing + `Faces.ShuffleAllTo([this], "EncounterDeck", effect)` a la defaite),
# `joueur.MayChooseOneAbility(effect, ForChoiceAbility(...))` (RECETTES-MOTEUR : « you may »), `message.defeating_player`.
# ⚠ Toughness / Villainous : desc (natifs) ; « may take 2 damage » : le refus est « Cancel » ; le joueur qui a VAINCU (pas celui contre qui elle
# etait engagee) ; pas de joueur vainqueur (degats d'un effet) : elle est melangee d'office.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.defeating_player
        prix_paye = False

        def payer(cibles: Sequence['CardFace']) -> None:
            nonlocal prix_paye
            prix_paye = True
            this.DealDamage([joueur.GetIdentity()], 2, effect)

        if joueur is not None:
            joueur.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility("Take 2 damage to discard Bellona instead", payer).SetHasNoTargetEffect())
        if not prix_paye:
            Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]

from . import *

# * Gunarm : AMELIORATION (TECH. WEAPON.), cout 3, [energy]. Restricted. Uses (3 ammo counters). Unique.
# Hero Action (attack): Exhaust Gunarm and remove 1 ammo counter from it → deal 3 damage to an enemy and choose: • Stun that enemy. • Confuse that enemy. • Deal 3 damage to another enemy.
#
# CARTES DE REFERENCE
#  - `61033a` Suggestion (fiche `mots-cles/uses.md`) : `CostFunc.Counter("This", 1, 'ammo')` pour « remove 1 counter » ; `Uses` : `desc.Uses = "3,ammo"` (le compteur `ammo` existe deja
#    dans l'enum). ⚠ `Uses` POSE les 3 jetons et DEFAUSSE la carte au dernier jeton retire, sans script : `ThisEnterPlayWithCounters` en plus en posait 6 (mesure du 01/11/2026).
#  - `01012` Crisis Interdiction : choix apres l'effet par `ChooseAbilities` + `ForChoiceAbility(..).SetTarget(..)` ; `Faces.GiveStatus(.., "Stunned"/"Confused", effect)`.
#
# TEXTE CONTRE CODE
#  « Exhaust Gunarm AND remove 1 ammo counter » : deux couts, sans jeton la carte n'est pas jouable. « deal 3 damage to AN enemy AND choose » : les 3 degats d'abord, PUIS UN
#  seul des trois choix. « Stun/Confuse THAT enemy » -> la cible des 3 premiers degats (rien si elle est vaincue). « 3 damage to ANOTHER enemy » -> un ennemi different.
#  « Uses (3 ammo counters) » : 3 utilisations, puis Gunarm quitte le jeu (regle du mot-cle). Chiffres : cout 3, 3 jetons, 3 degats, 3 degats.


def GetAbilities() -> Sequence['Ability']:

    def gunarm(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = effect.GetInitiator()
        hero = joueur.GetHero()
        cibles = list(effect.targets)
        hero.DealDamage(cibles, 3, effect)
        restantes = [c for c in cibles if c.card.IsOnField()]
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun that enemy",
                lambda _: Faces.GiveStatus(restantes, "Stunned", effect) if restantes else None,
            ),
            AbilityFactory.ForChoiceAbility(
                "Confuse that enemy",
                lambda _: Faces.GiveStatus(restantes, "Confused", effect) if restantes else None,
            ),
            AbilityFactory.ForChoiceAbility(
                "Deal 3 damage to another enemy",
                lambda autres:
                    this.DealDamage(autres, 3, effect),
            ).SetTarget(Enemy, exclude=cibles),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            gunarm,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'ammo'))
        .SetTarget(Enemy),
    ]

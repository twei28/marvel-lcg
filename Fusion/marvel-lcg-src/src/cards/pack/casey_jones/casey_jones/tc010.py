from . import *

# Driving Iron — AMELIORATION, cout 1, [mental]. WEAPON. Restricted.
# Hero Action: Exhaust Driving Iron → deal 1 damage to an enemy, or remove 1
#   threat from a scheme.
#
# MOT-CLE : RESTRICTED — fiche `restricted.md` (`desc.Restricted = "1"`, AUCUN
# SCRIPT pour la limite).
#
# CARTES DE REFERENCE
#  - `ho010` : amelioration a Hero Action = `CanPlayThisUpgradeCard()` +
#    `WhenInYourPlayTurn(HeroAction, op).SetCostFunc(Exhaust("This"))`.
#  - `raphael/tr010` Gekido : « choose: A / B » = `joueur.ChooseAbilities(effect,
#    ForChoiceAbility(...), ForChoiceAbility(...))`.
#  - `raphael/tr003` : `this.RemoveThreatFromSchemes(cibles, n, effect)`,
#    cible `Scheme2` ; `heros.DealDamage(cibles, n, effect)` (tr004).
#
# TEXTE CONTRE CODE
#  ⚠ « deal 1 damage to AN ENEMY, OR remove 1 threat from A SCHEME » : UN CHOIX
#    du joueur (pas les deux), chaque branche avec sa propre cible ; les deux
#    nombres sont 1.
#  ⚠ « Exhaust Driving Iron » est devant la fleche : un COUT.
#  ⚠ Action, pas un contre (aucun libelle `thwart`) : la Crise n'est donc pas
#    contournee ni verrouillee au ciblage (RECETTES §2, mots-cles/crisis.md).
#  ⚠ « Hero Action » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def driving_iron(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        heros = joueur.GetHero()

        def blesser(cibles: Sequence['CardFace']) -> None:
            auteur = heros if heros is not None else this
            auteur.DealDamage(list(cibles), 1, effect)

        def retirer(cibles: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(list(cibles), 1, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an enemy",
                blesser,
            ).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Remove 1 threat from a scheme",
                retirer,
            ).SetTarget(Scheme2),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            driving_iron,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]

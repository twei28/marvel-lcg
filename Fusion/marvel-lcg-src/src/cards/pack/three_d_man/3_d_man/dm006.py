from . import *

# 3-D Men Combined — EVENEMENT. SUPERPOWER. Cout 3, [wild].
# Hero Action: Ready up to 3 cards you control. If you reduced this card's
#   cost, for each card readied this way, deal 3 damage to an enemy.
#
# CARTES DE REFERENCE
#  - « Ready up to N <cards> you control » : **`lj029`** Inhuman's Best
#    Friend (`.SetTarget(Support, range=(0, 4), canbe_ready=True)` +
#    `Faces.ReadyAll(effect.targets, effect)`), generalise a n'importe quel
#    type de carte via `CardFinder()` + `from_where=["YouControlCards"]`
#    (modele **`ar003`** pour `from_where`).
#  - « If you reduced this card's cost, for each card readied this way, deal
#    3 damage to an enemy » : `CoutReduit` (helper du pack) + une resolution
#    de degats PAR carte redressee (pas une seule fois) : `this.DealDamage`
#    appele en boucle, cible choisie a chaque fois (modele d'un choix repete
#    via `joueur.AskChooseFace` sur les ennemis en jeu, comme dm005).
#
# TEXTE CONTRE CODE
#  « up to 3 CARDS you control » : tout type (identite comprise ? NON — une
#  identite n'est pas « une carte qu'on controle » au sens incliner/redresser
#  habituel pour ce genre d'effet ; lecture retenue : les cartes en jeu sous
#  son controle hors identite, comme `lj029`/`ar003`) ; 0 a 3, le joueur
#  choisit lesquelles. « FOR EACH card readied THIS WAY » : le compte REEL de
#  cartes redressees par CETTE resolution (pas 3 fixes, pas les cartes deja
#  pretes qu'on aurait choisies en trop — le moteur ne propose que des cartes
#  inclinees via `canbe_ready=True`).


def GetAbilities() -> Sequence['Ability']:

    def trois_d_men_combined(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        redressees = list(effect.targets)
        Faces.ReadyAll(redressees, effect)

        if not CoutReduit(effect) or not redressees:
            return

        for _ in redressees:
            ennemis = Worlds.GetOnFieldEnemies(effect)
            if not ennemis:
                return
            cible = joueur.AskChooseFace(ennemis, effect, prompt="Deal 3 damage to an enemy")
            if cible is None:
                return
            this.DealDamage([cible], 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            trois_d_men_combined,
        ).SetPlay()
        .SetTarget(CardFinder(), from_where=["YouControlCards"], range=(0, 3), canbe_ready=True),
    ]

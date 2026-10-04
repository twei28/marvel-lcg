from cards.pack.conan.conan import *

# The Coils of Doom — obligation. Give to the Conan player.
# Uses (3 serpent counters). Victory 0. Hazard x1, Boost x2.
# Hero Action: Spend 1 resource of any type or remove 1 Crom counter from The
#   Cimmerian -> remove 1 serpent counter from here.
#
# CARTES DE REFERENCE
#  - 53029 Harlem's Protector (Falcon, officiel) : MEME forme exacte (Uses 3,
#    Hazard, Boost 2, Victory 0), `WhenInYourPlayTurn(..., op).SetCost(Cost("1"))`
#    et `Faces.RemoveCountersOn([this], 1, '<pion>', effect)`. Uses, Hazard,
#    Victory, GiveTo : lus dans `desc`. Au dernier pion retire, la carte part
#    en vitrine (Victory 0) ; tant qu'elle est en jeu, son icone Hazard ajoute
#    une carte de rencontre a chaque phase du vilain.
#  - l'autre cout : `CostFunc.Counter(<selecteur>, 1, 'crom')` sur The Cimmerian.
#
# TEXTE CONTRE CODE
#  « Hero Action » : en forme heros seulement (53029 est une Alter-Ego Action).
#  « Spend 1 resource ... OR remove 1 Crom counter » : deux capacites, une par cout.


def GetAbilities() -> Sequence['Ability']:

    def retirer_un_serpent(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this.CastTo(Obligation)
        Faces.RemoveCountersOn([this], 1, 'serpent', effect)

    def cimmerian_a_un_crom(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        joueur = JoueurDe(effect)
        return joueur is not None and CromSur(joueur, effect) > 0

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            retirer_un_serpent,
        ).SetName("Spend 1 resource").SetCost(Cost("1")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            retirer_un_serpent,
            conditions=[cimmerian_a_un_crom],
        ).SetName("Remove 1 Crom counter")
        .SetCostFunc(CostFunc.Counter(
            Select.From(CardFinder(name=NOM_CIMMERIAN, card_type=Upgrade)), 1, 'crom')),
    ]

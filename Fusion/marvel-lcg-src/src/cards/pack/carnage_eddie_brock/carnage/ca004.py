from . import *

# * Lethal Restraint : AMELIORATION (CONDITION.), cout 1, [physical]. Classe Hero.
# Carnage gains retaliate 1.
# Hero Action: Return this card to your hand (from play) -> reduce the cost of the next Carnage event you play this phase by 1.
#
# CARTES DE REFERENCE
#  - « NOM gains retaliate 1 » : `nt011` (Prewind Stance) : `GiveKeywordToInPlayWhenApplyThis(CardFinder(name=..), control_by="You", retaliate=1)` + `CanPlayThisUpgradeCard()`.
#    Riposte est une BASE du moteur (fiche mots-cles/retaliate.md) : on la DONNE, on ne la recode pas.
#  - « reduce the cost of the next <X> card you play this phase by N » : `us009` (Solid Gear) : `Worlds.UpdateNextCardPlayCost(joueur, -N, effect, finder=.., in_this="Phase")`.
#  - « Return this card to your hand → » en COUT : `47028` (Jubilee) : `CostFunc.ReturnToHand(.., to_who="Owner")`.
#
# TEXTE CONTRE CODE
#  « CARNAGE gains retaliate 1 » : nom propre = la face heros, jamais l'alter-ego. « Hero Action » : `HeroAction` (forme heros seulement). « Return this card to your hand → » : le retour en main est le COUT.
#  « the NEXT Carnage EVENT » : UNE seule carte, de TYPE evenement et du set « Carnage » (ca010-ca013), jamais une amelioration ni une carte d'un autre set. « THIS PHASE » : `in_this="Phase"`.
#  « by 1 » : valeur negative (-1), la fabrique ne descend pas sous 0. Chiffres : cout 1, retaliate 1, -1.


def GetAbilities() -> Sequence['Ability']:

    def lethal_restraint(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        Worlds.UpdateNextCardPlayCost(
            joueur, -1, effect,
            finder=CardFinder(set_name=NOM_CARNAGE, card_type=Event),  # type: ignore
            in_this="Phase",
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name=NOM_CARNAGE),
            control_by="You",
            retaliate=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lethal_restraint,
        ).SetCostFunc(CostFunc.ReturnToHand("This", to_who="Owner")),
    ]

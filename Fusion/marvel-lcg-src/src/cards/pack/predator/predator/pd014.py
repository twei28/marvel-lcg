from . import *

# * Bio-Helmet — AMELIORATION, cout 2, [mental]. ARMOR. TECH.
# Hero Action: Exhaust Bio-Helmet → look at the top card of the encounter deck. For each icon (★ and Y) in that card's boost
#   area, remove 1 threat from a scheme.
#
# Cartes de reference :
#  - `CostFunc.LookAtDeck("EncounterDeck", 1)` (cost_func.py) / `player.LookAtDeck(deck, n, effect)` : « look at the top card » ;
#  - `FacesCounter.CountTotalBoostIcons` + `CountTotalBoostStar` (15004, ho014) : les icones du cadre de boost ;
#  - `RetirerMenaceDUneManigance` (alligator_loki, web_of_deceit) : « remove N threat from a scheme », choix du joueur.
#
# ⚠ Mots-pieges :
#  - « FOR EACH icon (★ and Y) ... remove 1 threat from A scheme » : DECISION UTILISATEUR (25/10/2026) = UNE manigance AU CHOIX
#    PAR ICONE (repartition libre entre complot principal et annexes).
#  - « look at the top card » : la carte reste sur le deck (aucun mouvement), meme sans icone.
#  - « Exhaust Bio-Helmet → » : l'inclinaison est le COUT ; deck de rencontre vide : rien a regarder, rien ne part.


def GetAbilities() -> Sequence['Ability']:

    def casque(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        dessus = joueur.LookAtDeck(Worlds.GetEncounterDeck(effect), 1, effect)
        if not dessus:
            return
        for _ in range(IconesDeBoost(dessus[0])):
            RetirerMenaceDUneManigance(effect, joueur, 1)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            casque,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]

from . import *

# * Book of the Iron Fist — AMELIORATION, cout 2, [physical]. ITEM. K'UN-LUN. x1 (Iron Fist 10/15).
# Hero Action: Exhaust this card -> if the top card of your discard pile is a Technique, put it
#   into play.
#
# CARTES DE REFERENCE
#  - « the top card of your discard pile » : `texas_twister/tt005` Pine Ridge Reservation
#    (`joueur.discard_pile.GetTop()`, deck.py:398 = `cards[-1]`, le dessus).
#  - Hero Action a cout d'inclinaison sur une amelioration : `human_torch/ht006` Spark
#    (`WhenInYourPlayTurn(HeroAction, op).SetCostFunc(CostFunc.Exhaust("This"))`).
#  - mise en jeu sans paiement : `bp/51025` (`face.PutIntoPlay(joueur, effect)`).
#
# TEXTE CONTRE CODE
#  ⚠ La condition « if the top card ... is a Technique » est lue A LA RESOLUTION, apres le cout :
#    l'action peut etre lancee sans Technique au sommet (elle incline le Livre et ne fait rien).
#  ⚠ « the TOP card » seulement : une Technique plus bas dans la defausse ne compte pas.
#  ⚠ « a Technique » = le trait TECHNIQUE (pas le type).
#  ⚠ « put IT into play » : sans paiement ; s'attache a l'identite (selecteur par defaut des
#    ameliorations, decision utilisateur n°1).
#  ⚠ Unique (✦ imprime) : « * » devant le nom.


def GetAbilities() -> Sequence['Ability']:

    def livre(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        dessus = joueur.discard_pile.GetTop()
        if dessus is not None and dessus.HasTrait(TRAIT_TECHNIQUE):
            dessus.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            livre,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]

from . import *

# * Purposeful Disparity : AMELIORATION (CONDITION.), cout 2, [wild]. Classe Hero. (PAS de trait SPLIT : aucun Special.)
# While Sentry is in hero form, reduce the amount of damage he takes from each attack by 1.
# Action: Exhaust this card → choose a SPLIT card in your discard pile. Place it on top of your discard pile.
#
# CARTES DE REFERENCE
#  - « reduce the damage he takes by 1 » : `WhenUnitWouldTakeDamage(.., is_from_attack=True)` + `message.ReduceDamage(1, effect)` (sender_damage.py:830).
#  - « Exhaust this card → » : `CostFunc.Exhaust("This")` ; deplacer une carte : `Faces.MoveAllTo([carte], joueur.discard_pile, effect)` (le dernier arrive est le DESSUS).
#
# TEXTE CONTRE CODE
#  « While Sentry is in HERO FORM » : seulement quand l'identite du joueur est la face heros (l'alter-ego ne beneficie pas de la reduction). « from EACH attack » : chaque attaque, d'au plus 1 ; jamais sous 0.
#  « Place it ON TOP of your discard pile » : devient la carte du dessus (celle que le Void resout en premier). Chiffres : cout 2, -1.


def GetAbilities() -> Sequence['Ability']:

    def reduire(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        if message.will_take_damage > 0:
            message.ReduceDamage(1, effect)

    def sentry_en_forme_heros(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        joueur = JoueurDeCetteCarte(effect)
        return joueur is not None and message.trigger is joueur.GetIdentity() and Hero.IsType(message.trigger)

    def remonter(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        cartes = CartesSplitDansLaDefausse(joueur)
        if not cartes:
            return
        choisie = joueur.AskChooseFace(cartes, effect, not_move=True)
        if choisie is not None:
            Faces.MoveAllTo([choisie], joueur.discard_pile, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.NonKeyword,
            None,
            reduire,
            is_from_attack=True,
            conditions=[sentry_en_forme_heros],
        ),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, remonter).SetCostFunc(CostFunc.Exhaust("This")),
    ]

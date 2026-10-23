from . import *

# Seized Tech Crates — AMELIORATION de campagne (recompense du combat 1, p264). Permanent.
# Setup : Place 1 counter here, plus 1 more for each player who did not play the last game together.
# Action : Remove 1 counter -> choose (any player may trigger this ability, limit once per player per round):
#   • Reduce the cost of the next card you play this phase by 1.
#   • Find a support or upgrade with a cost of 2 or less and add it to your hand.
#
# Cartes de reference : fne/typhoid_mary/60112 (`AfterGameSetup`, le Setup d'une carte hors scenario), mister_fantastic/mf007
# (`CostFunc.Counter("This", 1, ...)`), skrull_menace/skrull_menace_campaign/sk281 (`AnyPlayerCanDoThis`) et skrull_empire
# (`LimitOncePerRoundPerPlayer`), dazzler/dz003 (`Worlds.UpdateNextCardPlayCost`), angela/an001b (`Search.PlayerCard` + `GainCard`).
# ⚠ Mots-pieges :
#  - « each player who did not play the last game together » : decision P6 (cadrage 14-15-19) : un HEROS qui n'etait pas dans la partie
#    precedente (le carnet garde `Player N Identity` de la derniere partie) ; sans carnet de la partie precedente, aucun joueur en plus.
#  - « the next card you play THIS PHASE » : `in_this="Phase"` (pas "Round") ; « by 1 » : -1, et le cout ne descend pas sous 0.
#  - « Find a support or upgrade » : TOUTES les zones ou la carte peut etre (`Find.Find` : deck, defausse, zone de jeu, mises de cote ; decision
#    de l'utilisateur du 23/10/2026, texte de la Rules Reference dans `game/operate/find.py`), sauf une carte deja en main et Seized Tech Crates elle-meme ; cout imprime <= 2 ;
#    la carte va en MAIN. « cost of 2 or less » = cout imprime.
#  - « limit once per player per round » : `LimitOncePerRoundPerPlayer`, jamais `LimitOncePerRound` (une limite globale).
#  - « Remove 1 counter -> » : le retrait est le COUT, il est paye avant le choix ; sans compteur l'Action n'est pas offerte.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        Unused(message)
        Faces.PlaceCountersOn([effect.this], JetonsDeDepart(effect), 'counter', effect)

    def reduire_le_cout(targets: Sequence['CardFace'], effect: 'Effect') -> None:
        Unused(targets)
        joueur = effect.GetInitiator()
        if joueur is not None:
            Worlds.UpdateNextCardPlayCost(joueur, -1, effect, in_this="Phase")

    def chercher(effect: 'Effect') -> None:
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        # « Find » = TOUTES les zones ou la carte peut se trouver (`Find.Find`, regle du 23/10/2026), sauf une carte deja en main.
        face = Find.Find(
            effect, who_perform=joueur,
            finder=CardFinder(card_type=Support | Upgrade,
                              check_face_fn=lambda f: f.printed_cost.val <= 2 and not f.card.IsInHand() and f is not effect.this),
        )
        if face is not None:
            joueur.GainCard([face], effect)

    def action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Reduce the cost of the next card you play this phase by 1",
                                            lambda cibles: reduire_le_cout(cibles, effect)),
            AbilityFactory.ForChoiceAbility("Find a support or upgrade with a cost of 2 or less and add it to your hand",
                                            lambda cibles: chercher(effect)),
        )

    return [
        AbilityFactory.AfterGameSetup(mise_en_place),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, action)
        .SetCostFunc(CostFunc.Counter("This", 1, 'counter'))
        .AnyPlayerCanDoThis()
        .LimitOncePerRoundPerPlayer(),
    ]

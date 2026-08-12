from . import *

# Briefing Room — custom « Rainy »
# Hero Response: After a minion or side scheme is revealed, exhaust Briefing
# Room → each player in hero form draws 1 card.
#
# Modele pour l'exhaustion + pioche en Response : Mission Leader (40023,
# next_evol), « Apres qu'une manigance annexe est vaincue, epuise -> chaque
# joueur pioche 1 carte », et Winter Mask (54010) pour la meme mecanique sans
# `SetTarget` explicite (aucune cible n'est choisie, l'effet est automatique).
# Modele pour le filtre « en forme heros » : Green Goblin (I) (02001b), via
# le helper `WhenRevealDealDamangeToPlayers` qui teste `player.IsHero()`
# dans une boucle `Players.ForEachPlayer`.
#
# « Minion ou manigance annexe » n'a pas de type unique dans le moteur : on
# le rend par un `CardFinder(check_face_fn=...)` qui accepte les deux types,
# plutot que deux abilites separees qui partageraient mal le cout
# d'epuisement (l'une resolue empecherait l'autre de se declencher a tort si
# elles etaient distinctes cost-wise, alors qu'ici le cout est unique).

def GetAbilities() -> Sequence['Ability']:

    def briefing_room(effect: 'Effect', message: 'Message.AfterCardRevealedEnd') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        def action(player: 'Player') -> None:
            if player.IsHero():
                player.DrawUp(1, effect)

        Players.ForEachPlayer(effect, action)

    return [
        AbilityFactory.AfterPlayerRevealCard(
            AbilityType.HeroResponse,
            "AnyPlayer",
            CardFinder(check_face_fn=lambda face: Minion.IsType(face) or SchemeSide2.IsType(face)),
            briefing_room,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]

from . import *

# Now It's Personal

def GetAbilities() -> Sequence['Ability']:

    def now_its_personal(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)

        # « Action: Remove this card from the game -> each player on your team
        # chooses 2 of your leader's set-aside player cards and adds them to
        # their hand. » Le retrait de la partie est le COUT, deja porte par
        # SetCostFunc ; il ne reste ici que le gain.
        #
        # Les 4 cartes viennent de l'etape 3 de la mise en place competitive
        # (mc56 p.14), et sont celles du leader de VOTRE camp, celui qui est
        # sur la table d'en face. Elles appartiennent a l'equipe : en 2v2 les
        # deux joueurs en prennent 2 chacun, en 1v1 le joueur seul en prend 2
        # et les deux autres restent de cote.
        world = effect.world
        camp = Worlds.GetTeamOfEffect(effect)
        reserve = world.GetTeamSetAside(camp)

        for player in world.GetTeamPlayers(camp):
            disponibles = reserve.Get()
            if not disponibles:
                break
            combien = min(2, len(disponibles))
            choisies = player.AskChooseFaces(
                disponibles,
                (combien, combien),
                effect,
                prompt="Take 2 of your leader's cards",
                not_move=True,
                not_shuffle=True,
            )
            if not choisies:
                choisies = disponibles[:combien]
            for face in choisies:
                # « Those cards become part of that player's deck for the rest
                # of the game » : la carte change de proprietaire, sans quoi
                # elle repartirait a la defausse du scenario.
                face.card.SetOwner(player)
            Faces.AddToHand(list(choisies), player, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            now_its_personal
        ).SetCostFunc(CostFunc.RemoveFromGame("This")),
    ]

from . import *

# Switching Sides

def GetAbilities() -> Sequence['Ability']:

    def switching_sides_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        player = message.GetToPlayer()

        defaussees = player.AskDiscardFaces(player.GetControlAllies(), (1, 1), effect)

        if defaussees and Worlds.IsCompetitiveMode(effect):
            # « Any player on the enemy team may spend resources equal to that
            # ally's cost to put it into play under their control. »
            #
            # L'equipe adverse est a une AUTRE table : on ouvre la fenetre de
            # paiement a chacun de ses joueurs, dans l'ordre des sieges, et le
            # premier qui paie emporte l'allie. Rien n'oblige a payer.
            allie = defaussees[0]
            monde = effect.world
            camp_adverse = monde.GetOtherTeam(Worlds.GetTeamOfEffect(effect))
            for acheteur in monde.GetTeamPlayers(camp_adverse):
                if acheteur.is_eliminated:
                    continue
                if acheteur.AskSpendResources(allie.printed_cost, effect):
                    # L'allie change de camp : il entre en jeu sous le controle
                    # de l'acheteur, donc sur SA table.
                    allie.PutIntoPlay(
                        acheteur, effect,
                        under_control=True,
                        target_game_area=acheteur.GetGameArea())
                    break

        if not defaussees:
            # « If no ally left play this way, this card gains surge. » C'est
            # l'idiome habituel du jeu (« If you cannot, this card gains
            # surge », mw020) : le deferlement paie l'effet qui n'a PAS eu
            # lieu, pas le rachat qui n'a pas ete offert. Un joueur sans allie
            # subit donc une carte de plus, qu'on soit en competitif ou non —
            # avant ce lot, la carte deferlait a chaque revelation en
            # competitif, et jamais en cooperatif.
            this.GainSurge(+1, effect)


    return [
        AbilityFactory.WhenThisRevealed(
            None,
            switching_sides_revealed
        ),
    ]

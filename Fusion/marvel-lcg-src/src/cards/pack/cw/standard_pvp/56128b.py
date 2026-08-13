from . import *

# Now It's Personal

def GetAbilities() -> Sequence['Ability']:

    def now_its_personal(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)

        # ECART ASSUME, ecrit plutot que silencieux.
        #
        # Texte : « Action: Remove this card from the game -> each player on
        # your team chooses 2 of your leader's set-aside player cards and adds
        # them to their hand. »
        #
        # Ces cartes joueur mises de cote viennent de l'etape 3 de la mise en
        # place competitive (mc56 p.14) : « Each team finds their chosen
        # leader's basic player cards and sets them aside. » Cette etape n'est
        # pas encore montee par le moteur — c'est la meme reserve que pour la
        # manigance Choosing Sides, qui les fait gagner (p.16).
        #
        # Tant qu'elle n'existe pas, l'obligation se resout par son SEUL cout,
        # deja porte par SetCostFunc : elle est retiree de la partie et rien
        # n'est ajoute en main. Le joueur perd donc un gain, il ne subit pas
        # une regle inventee.
        Unused(this)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            now_its_personal
        ).SetCostFunc(CostFunc.RemoveFromGame("This")),
    ]

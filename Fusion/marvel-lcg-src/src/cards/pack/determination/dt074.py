from . import *

# In the Wings

def GetAbilities() -> Sequence['Ability']:

    def check_aerial(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        if player is None:
            return False
        return player.GetIdentity().HasTrait("AERIAL")

    def in_the_wings(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)

        player = this.GetControlByPlayer()
        if player is None:
            return

        allies = player.discard_pile.FindCards(card_type=Ally)
        if allies:
            # « le PREMIER allie de votre pile de defausse » : le dessus de la
            # pile, c'est-a-dire le dernier defausse.
            allie = allies[-1].CastTo(Ally)
            allie.PutIntoPlay(player, effect)
            # APPROXIMATION ECRITE : « declarez-le defenseur pour cette
            # attaque ». Le moteur choisit son defenseur dans sa propre
            # fenetre, plus tard, et n'expose pas de moyen de le fixer d'ici.
            # L'allie arrive donc en jeu, pret a defendre, mais le joueur doit
            # le declarer lui-meme au moment de la defense.

        villain = message.trigger
        Faces.GiveStatus([villain], "Confused", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Villain,
            in_the_wings,
            conditions=[check_aerial],
        ).SetCostFunc(CostFunc.Discard("This")),
    ]

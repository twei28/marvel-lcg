from . import *


def GetAbilities() -> Sequence['Ability']:
    def allies_du_joueur(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> List['CardFace']:
        joueur = message.against_player
        if joueur is None:
            return []
        return [a for a in joueur.GetControlCards() if Ally.IsType(a)]

    def a_un_allie(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        # Garde anti-boucle : l'attaque REDIRIGEE vers un allie est aussi « contre le joueur » (RR 1.8 p.10) ; elle ne
        # doit pas se rediriger a son tour (RecursionError vu au journal). Seule une attaque visant l'IDENTITE se redirige.
        vise_l_identite = any(Hero.IsType(t) or AlterEgo.IsType(t) for t in message.attacked_targets)
        return vise_l_identite and bool(allies_du_joueur(effect, message))

    def green_goblin(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        allies = allies_du_joueur(effect, message)
        if not allies:
            return                                   # « (if able) »
        joueur = message.against_player
        # Plusieurs allies admissibles pour une carte de rencontre : c'est le PREMIER joueur qui choisit (RR First Player, arbitrage du
        # 26/10/2026), pas le joueur attaque. En solo c'est le meme joueur.
        premier = this.card.world.GetFirstPlayer()
        cible = allies[0] if len(allies) == 1 else (premier or joueur).AskChooseFace(allies, effect, prompt="Green Goblin attacks an ally")
        message.SetBeInstead(effect)
        this.AttackCharacter(cible, effect)

    return [
        AbilityFactory.WhenUnitInitiatesAttackAgainst(
            AbilityType.ForcedInterrupt,
            "This",
            "AnyPlayer",
            green_goblin,
            conditions=[a_un_allie],
        ),
    ]

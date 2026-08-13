from . import *

# "Get 'Em, Boom-Boom!"

def GetAbilities() -> Sequence['Ability']:

    # Cette carte n'a PAS de mise en jeu ordinaire : sa seule facon d'arriver
    # est la Response, qui l'attache a un ennemi. Lui donner en plus un
    # `CanPlayThisUpgradeCard` faisait DEUX capacites Play, et la generation
    # tombait (factory.py). « Fleeting » est lu par le moteur dans le texte.
    def attacher_a_un_ennemi(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        for cible in effect.targets:
            this.AttachTo2(cible, effect)

    def boom_boom(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        this = effect.this.CastTo(Upgrade)

        ennemis = [x for x in Worlds.FindCardsOnField(effect, card_type=Enemy)
                   if not x.IsDefeated()]
        if ennemis:
            this.DealDamage(ennemis, 1, effect)

    def check_votre_identite(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        initiator = effect.GetInitiator()
        return initiator is not None and message.trigger == initiator.GetIdentity()

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            None,
            attacher_a_un_ennemi,
            conditions=[check_votre_identite],
        ).SetPlay()
        .SetTarget(Enemy),
        AbilityFactory.WhenCardWouldDiscard(
            AbilityType.Interrupt,
            "This",
            boom_boom
        ),
    ]

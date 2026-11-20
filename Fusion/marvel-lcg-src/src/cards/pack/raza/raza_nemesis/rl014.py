from . import *
def GetAbilities() -> Sequence['Ability']:
    def joueur_engage_avec_zzzxx(effect: 'Effect', joueur: 'Player|None') -> bool:
        zzzxx = TrouverZzzxx(effect)
        return joueur is not None and zzzxx is not None and zzzxx.CastTo(Minion).GetEngagedPlayer() is joueur
    def attaquant_engage(effect: 'Effect', message: 'Message.CheckIfUnitCanBeAttackBy') -> bool:
        return joueur_engage_avec_zzzxx(effect, message.attacker.GetControlByPlayer())
    def contreur_engage_autre_complot(effect: 'Effect', message: 'Message.CheckIfSchemeCanBeThwartBy') -> bool:
        # « thwart schemes OTHER THAN THIS ONE » : la fabrique `can_only_thwart="This"` est LOCALE a la carte (elle n'ecoute que les
        # messages de cette manigance) ; on interdit donc TOUTE manigance et la condition ecarte celle-ci.
        return message.scheme is not effect.this and joueur_engage_avec_zzzxx(effect, message.who_thwart.GetControlByPlayer())
    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        MettreZzzxxEnJeu(effect, message.GetToPlayer())
    return [
        AbilityFactory.WhenThisRevealed(None, reveler),
        AbilityFactory.UnitCannotBeAttacked(
            CardFinder(name=NOM_ZZZXX, card_type=Minion),
            conditions=[attaquant_engage],
        ),
        *AbilityFactory.UnitCannotThwartTarget(
            Hero,
            cannot_thwart=Scheme2,
            conditions=[contreur_engage_autre_complot],
        ),
        *AbilityFactory.UnitCannotThwartTarget(
            Ally,
            cannot_thwart=Scheme2,
            conditions=[contreur_engage_autre_complot],
        ),
    ]

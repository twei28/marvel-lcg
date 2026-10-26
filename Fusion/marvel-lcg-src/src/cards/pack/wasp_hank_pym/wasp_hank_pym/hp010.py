from . import *
# Huge Surprise — amelioration. Hero Action : attache cette carte a un ENNEMI ; jusqu'a la fin du round cet ennemi
# perd Steady et Stalwart et subit 4 degats APRES avoir ete etourdi ou desoriente ; la carte gagne Temporary
# (defaussee en fin de round). Modeles : 50144 (statut sur l'hote, Stalwart retire), 27171 (AttachTo2).
def GetAbilities() -> Sequence['Ability']:
    def surprise(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        for cible in effect.targets:
            this.AttachTo2(cible, effect)
        this.GainTemporary(1, effect)
    def quatre_degats(effect: 'Effect', message: 'Message.AfterCardPlaceStatusOn') -> None:
        this = effect.this.CastTo(Upgrade)
        hote = this.bind_face
        if hote is not None:
            this.DealDamage([hote], 4, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            surprise,
            # Deja attachee a un ennemi : l'Action ne se rejoue pas (l'autoplay la rejouait a l'infini, 2 parties « bloquees » sur 8).
            conditions=[lambda effect, message: not (effect.this.bind_face is not None and Enemy.IsType(effect.this.bind_face))],
        ).SetTarget(Enemy),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            stalwart=-1,
            steady=-1,
        ),
        AbilityFactory.AfterStatusCardPlaceOn(
            AbilityType.ForcedResponse,
            "AttachedEnemy",
            ["Stunned", "Confused"],
            quatre_degats,
        ),
    ]

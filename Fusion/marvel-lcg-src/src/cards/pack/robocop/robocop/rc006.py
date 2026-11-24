from . import *

# Internal Reload System : AMELIORATION (ITEM. TECH.), cout 2, [wild].
# Hero Resource: Generate a [wild] resource for Auto-9's ability. That attack gains piercing.
# Interrupt: When you use one of RoboCop's basic powers, ready Auto-9.
#
# CARTES DE REFERENCE
#  - `33003` Ruby Quartz Visor : TEXTE QUASI IDENTIQUE (`CanGenerateResources(HeroResource, Resources(..), for_ability="<nom de l'Action>", ex_operation=..)` ; l'operation
#    enregistre une regle temporaire `WhenUnitWouldAttack(Temp0, .., by_effect=message.for_effect)` qui donne piercing a l'attaque PAYEE par cette ressource). Difference : le
#    Visor s'incline, l'Internal Reload System NON (aucun cout imprime).
#  - `WhenUnitUseBasicPower(Interrupt, "You", ..)` (`friend.py`) pour « When you use one of RoboCop's basic powers ».
#
# TEXTE CONTRE CODE
#  « Hero RESOURCE » : forme heros seulement. « for AUTO-9'S ability » : n'est utilisable que pour payer l'Action nommee « Auto-9 » (rc005), pas pour une autre carte.
#  « THAT attack gains piercing » : seulement l'attaque payee avec cette ressource. « When you use ONE OF RoboCop's basic powers » : ATQ, CTR, DEF ou REC du heros ;
#  « ready Auto-9 » : l'arme nommee Auto-9 que ce joueur controle, si elle est inclinee. Interruption nue.
#  Chiffres : cout 2, une ressource [wild].


def GetAbilities() -> Sequence['Ability']:

    def piercing_pour_cette_attaque(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Upgrade)

        def action(effect: 'Effect', message: 'Message.WhenUnitWouldAttack'):
            message.GainPiercing(effect)

        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldAttack(
                AbilityType.Temp0,
                None,
                action,
                by_effect=message.for_effect,
            ),
            unregister_after_exec=True,
        )

    def ready_auto_9(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = effect.GetInitiator()
        armes = [f for f in joueur.GetControlUpgrade(CardFinder(name=NOM_AUTO_9))]
        if armes:
            Faces.ReadyAll(armes, effect)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            for_ability=NOM_AUTO_9,
            ex_operation=piercing_pour_cette_attaque,
        ),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "You",
            ready_auto_9,
        ),
    ]

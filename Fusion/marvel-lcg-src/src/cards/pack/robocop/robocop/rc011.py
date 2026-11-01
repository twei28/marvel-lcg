from . import *

# * Officer Lewis : SOUTIEN (OFFICER. PERSONA.), cout 1, [wild]. Unique.
# Alter-Ego Action: Exhaust Officer Lewis → heal 2 damage from Alex Murphy.
# Hero Response: After you resolve an "Action" ability on a WEAPON upgrade you control, exhaust Officer Lewis → deal 2 additional damage to that enemy. Any player may trigger this ability.
#
# CARTES DE REFERENCE
#  - `27009` Web-Bracelet / `36007` Storm's Cape : `AfterPlayerResolveAbility(HeroResponse, "You", <carte>, op, which_abilities=[..], control_by_you=True)` ;
#    `which_abilities="Action"` couvre Action ET Hero Action (`ability_type.py`). `40197` Safehouse : `AnyPlayerCanDoThis()`.
#
# TEXTE CONTRE CODE
#  « After YOU resolve an Action ability on a WEAPON upgrade YOU control » -> le joueur qui declenche, sur SA propre arme (`control_by_you`). « that enemy » -> l'ennemi
#    vise par cette Action (premiere cible ennemie de l'effet resolu) ; rien si l'Action n'avait pas d'ennemi pour cible. « ADDITIONAL damage » : 2 de plus, apres.
#  « Any player may trigger » -> `AnyPlayerCanDoThis`. Alter-Ego Action : soigne l'identite (Alex Murphy) du joueur qui agit.
#  Chiffres : cout 1, soin 2, 2 degats.


def GetAbilities() -> Sequence['Ability']:

    def officer_lewis_soin(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        joueur = effect.GetInitiator()
        this.HealthUnits([joueur.GetIdentity()], 2, effect)

    def officer_lewis_degats(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        this = effect.this.CastTo(Support)
        ennemis = [c for c in message.effect.targets if Enemy.IsType(c) and c.card.IsOnField()]
        if ennemis:
            this.DealDamage(ennemis[:1], 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            officer_lewis_soin,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.HeroResponse,
            "You",
            Upgrade,
            officer_lewis_degats,
            which_abilities="Action",
            conditions=[
                lambda effect, message:
                    ArmeDuJoueur(message.trigger, effect.GetInitiator()),
            ],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .AnyPlayerCanDoThis(),
    ]

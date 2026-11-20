from . import *

# * Wolverine's Claws — PERMANENT. WEAPON. Pas de cout, ressource [wild] imprimee.
# Resource: Exhaust Wolverine's Claws -> generate a [wild] resource for an [[Attack]] event. That event deals 1 additional
# damage (to a maximum of 3) for each card you discarded from your hand at random this round.
#
# Carte de reference : `54002` * Cybernetic Arm (Winter Soldier officiel) : le meme texte a « that event deals 1
# additional damage » — `CanGenerateResources(Resource, Resources("G"), for_card=CardFinder2("ATTACK", Event),
# ex_operation=...)` + `RegisterTemp(WhenUnitWouldAttack(Temp0, "You", DealAdditionalDamage), until_resolve_effect=
# message.for_effect)`. Ici le bonus n'est pas 1 mais le NOMBRE DE CARTES DEFAUSSEES AU HASARD CE ROUND, plafonne a 3,
# lu au moment de l'attaque (`world.stat.CountRandomDiscards`) : la defausse qui PAIE l'evenement compte donc aussi.
# Permanent : natif (`desc.Permanent`), aucun script (fiche mots-cles/permanent.md).
#
# Mots-pieges : « each card you discarded ... at random » (pas une defausse choisie : Winter Mask, Phoenix et les cartes
# du pack passent par `DiscardRandomHandCards`) ; « THIS round » (remis a zero en fin de round) ; « to a maximum of 3 » ;
# « THAT event » : chaque attaque de l'evenement recoit le bonus (Wild Slash en fait plusieurs, comme Slice and Dice
# avec Cybernetic Arm).


def GetAbilities() -> Sequence['Ability']:

    def wolverines_claws(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = effect.GetInitiator()

        def bonus(atk_effect: 'Effect', atk_message: 'Message.WhenUnitWouldAttack') -> None:
            n = min(3, atk_effect.world.stat.CountRandomDiscards(joueur))
            if n > 0:
                atk_message.DealAdditionalDamage(n, atk_effect)

        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldAttack(
                AbilityType.Temp0,
                "You",
                bonus,
                by_effect=message.for_effect,
            ),
            unregister_after_exec=False,
            until_resolve_effect=message.for_effect,
        )

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            for_card=CardFinder2("ATTACK", Event),
            ex_operation=wolverines_claws,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]

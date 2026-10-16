from . import *

# Improvised Club — AMELIORATION 1 [energy], aspect Basic (MC Custom Content, Inkwire). WEAPON.
# Attach to an ally. Max 1 per ally.
# Response: After attached ally attacks and damages a minion, discard Improvised Club → stun that minion.
#
# NOUVELLE. Cartes de reference :
#  - « Attach to an ally. Max 1 per ally » : 01074 Inspired, `CanPlayThisUpgradeCard(Ally)` ; le « Max 1 per
#    ally » est `MaxPerUnit` dans `desc` (lu par le moteur).
#  - « After attached ally attacks ... » : 12017 Power Gloves, porteur designe par "AttachedAlly".
#  - « attacks AND damages a <type>, stun that character » : 01118 Sonic Converter,
#    `AfterUnitAttackAndDamageUnit(<attaquant>, <cible>, ...)`, la cible etant `message.attacked`.
# TEXTE CONTRE CODE : « attached ally » (le porteur) ; « attacks AND damages » (degats reellement infliges) ;
#   « a MINION » (pas le vilain) ; « discard Improvised Club » = COUT ; « stun THAT minion ».


def GetAbilities() -> Sequence['Ability']:

    def club(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.GiveStatus([message.attacked], "Stunned", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Ally),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.Response,
            "AttachedAlly",
            Minion,
            club,
            target_in_play=True,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]

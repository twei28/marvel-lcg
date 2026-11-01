from . import *

# Fortified Mind (x2) : AMELIORATION (CONDITION. PSIONIC.), cout 1, [mental]. Hero Class. Max 1 par allie.
# Hero form only. Attach to an ally. Limit 1 per ally.
# Forced Interrupt: When attached ally would take consequential damage, discard Fortified Mind instead. Then, confuse that ally.
#
# CARTES DE REFERENCE
#  - `bt017` Automated Life-Support : `CanPlayThisUpgradeCard(CardFinder(card_type=Ally))` (cible « Attach to an ally ») ; « Max 1 per ally » lu NATIVEMENT dans `desc.MaxPerUnit`.
#  - `32036` Phased and Confused : `.SetPlay(hero_form_only=True)` + « discard this card instead. Then, confuse ... ».
#  - `dt009` Savior Complex / `pt001a` Patriot : `Ability(.., Message.WhenAllyWouldTakeConsequentialDamage, [cond], op)` + `message.SetBeInstead(effect)` : le degat consecutif PART, il n'est pas dupliqué.
#
# TEXTE CONTRE CODE
#  « Hero form only » : la carte ne se joue qu'en forme heros. « would take CONSEQUENTIAL damage » : le seul message `WhenAllyWouldTakeConsequentialDamage` (les degats d'attaque subis par un
#    allie ne la declenchent PAS). « attached ally » : l'allie qui porte la carte, pas un autre allie. « discard Fortified Mind INSTEAD » : le degat n'a pas lieu. « Then, confuse that ally » :
#    le meme allie, apres la defausse. Forced Interrupt : obligatoire, sans cout.
#  Chiffres : cout 1, 1 par allie.


def GetAbilities() -> Sequence['Ability']:

    def allie_porteur(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> bool:
        this = effect.this.CastTo(Upgrade)
        return message.trigger == this.GetBindFace()

    def fortified_mind(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        allie = message.trigger
        message.SetBeInstead(effect)
        Faces.DiscardAll([this], effect)
        Faces.GiveStatus([allie], "Confused", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Ally),
        ).SetPlay(hero_form_only=True),
        Ability(
            AbilityType.ForcedInterrupt,
            Message.WhenAllyWouldTakeConsequentialDamage,
            [allie_porteur],
            fortified_mind,
        ),
    ]

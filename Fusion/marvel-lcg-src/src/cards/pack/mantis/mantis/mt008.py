from . import *

# Fortified Mind (x2) : AMELIORATION (CONDITION. PSIONIC.), cout 1, [mental]. Hero Class. Max 1 par allie.
# Attach to an ally. Limit 1 per ally.
# Interrupt: When attached ally attacks or thwarts, discard Fortified Mind → that ally gets +1 THW and +1 ATK and takes no consequential damage for this activation. Then, confuse that ally.
# (Version du 04/03/2024 de l'auteur, relevee sur son Drive le 24/11/2026 : l'ancienne « Forced Interrupt : quand l'allie subirait des degats consecutifs, defaussez-la a la place » a disparu,
#  « Hero form only » aussi.)
#
# CARTES DE REFERENCE
#  - `bt017` Automated Life-Support : `CanPlayThisUpgradeCard(CardFinder(card_type=Ally))` (cible « Attach to an ally ») ; « Max 1 per ally » lu NATIVEMENT dans `desc.MaxPerUnit`.
#  - `sk283` 3-D Man's Goggles (amelioration attachee a un allie, `Interrupt` sur `WhenUnitWouldAttack`, `message.DoesNotTakeConsequentialDamage`) et `sd002` Quicksilver (`WhenUnitWouldAttackOrThwart`,
#    meme message pour « he suffers no consequential damage for that use »).
#  - `36014` Havok / `63038` Moondragon : `unite.GainForThisActive(effect, message, attack=.., thwart=..)` = « +N ATK / +N THW for this attack / this thwart ».
#  - `lj026` Ms. Marvel : « Interrupt: When she attacks, she gets +1 ATK ... When she thwarts, she gets +1 THW ».
#
# TEXTE CONTRE CODE
#  « Attach to an ALLY » : un allie, pas un autre personnage. « When ATTACHED ally attacks OR thwarts » : l'allie qui porte la carte, a chaque attaque ET a chaque contre (message `WhenUnitWouldAttackOrThwart`),
#    jamais un autre allie. « Interrupt » : sans « Hero » ni « Forced » : facultatif (le cout « discard » se paie en connaissance de cause), jouable dans les DEUX formes. « discard Fortified Mind → » = COUT.
#    « that ally gets +1 THW AND +1 ATK » : +1 a la puissance QUI SERT (ATQ pour une attaque, CTR pour un contre : l'autre n'a pas d'objet) pour CETTE activation seulement. « takes NO consequential damage for
#    this activation » : `DoesNotTakeConsequentialDamage`. « Then, confuse that ally » : apres ces effets, MEME allie. L'activation est deja declaree : la confusion (qui retire sa cible a un contre) ne
#    l'annule pas, elle pese sur la SUIVANTE.
#  Chiffres : cout 1, +1, +1, 1 par allie.


def GetAbilities() -> Sequence['Ability']:

    def allie_porteur(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart') -> bool:
        this = effect.this.CastTo(Upgrade)
        allie = this.GetBindFace()
        return allie is not None and message.trigger == allie

    def fortified_mind(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart') -> None:
        allie = message.trigger.CastTo(Ally)
        if isinstance(message, Message.WhenUnitWouldAttack):
            allie.GainForThisActive(effect, message, attack=1)
        else:
            allie.GainForThisActive(effect, message, thwart=1)
        message.DoesNotTakeConsequentialDamage(effect)
        Faces.GiveStatus([allie], "Confused", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Ally),
        ).SetPlay(),
        AbilityFactory.WhenUnitWouldAttackOrThwart(
            AbilityType.Interrupt,
            Ally,
            fortified_mind,
            conditions=[allie_porteur],
        ).SetCostFunc(CostFunc.Discard("This")),
    ]

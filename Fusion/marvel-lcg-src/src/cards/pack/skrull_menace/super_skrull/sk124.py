from . import *

# Pyrokinesis — ATTACHEMENT (paquet SUPERPOWER). SUPERPOWER. +1 ATK (★).
# Attach to Super-Skrull.
# Forced Response: After a friendly character thwarts the main scheme, deal 1
#   damage to it.
# ★ Super-Skrull's attacks gain piercing.
#
# Cartes de reference :
#  - **`27176`** Back Alley Burglary / **`vv003`** : `AfterUnitThwartScheme(
#    ForcedResponse, ...)` + condition ; `message.trigger` = le personnage qui
#    contre. Les degats : `unit.TakeDamage(this, 1, effect)` (46031 Life Drain).
#  - **`ho016`** Bullseye / `50107b` : « ★ X's attacks gain piercing » =
#    `UnitAttackGainKeyword(..., piercing=True)` (fiche piercing.md).
#  - `ATK+` : cle desc (HasModify, base automatique). Le ★ en exposant du badge
#    renvoie au texte (convention validee le 15/10/2026), sans valeur de plus.
#
# ⚠ Mots-pieges : « FRIENDLY character » (heros ou allie d'un joueur, pas un
# ennemi) ; « thwarts the MAIN scheme » (pas un complot annexe) ; « deal 1 damage
# to IT » = au personnage qui a contre ; Reponse obligatoire (pas d'option) ;
# les degats sont normaux (Toughness/Tough les absorbent), pas indirects.


def GetAbilities() -> Sequence['Ability']:
    mechant = CardFinder(name=NOM_MECHANT, card_type=Villain)

    def ami(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> bool:
        return Hero.IsType(message.trigger) or Ally.IsType(message.trigger)

    def bruler(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        this = effect.this.CastTo(Attachment)
        message.trigger.CastTo(Unit2).TakeDamage(this, 1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(mechant),
        AbilityFactory.AfterUnitThwartScheme(AbilityType.ForcedResponse, None, MainScheme, bruler, conditions=[ami]),
        AbilityFactory.UnitAttackGainKeyword(mechant, piercing=True),
    ]

from . import *

# Uru Armor Plating — ATTACHEMENT (ensemble Destroyer). ARMOR.
# CONDITION.
# Attach to Destroyer. Otherwise, attach to the enemy with the least remaining hit points.
# Uses (3 plate counters).
# Forced Interrupt: When attached enemy would take any amount of damage, prevent 2 of that damage and
#   remove 1 plate counter from here.
#
# Cartes de reference :
#  - « Attach to Destroyer. Otherwise, attach to the enemy with the least remaining hit points » :
#    `AttachToFaceWhenPutIntoPlay(CardFinder(name="Destroyer"), otherwise_attach_to=
#    CardFinder(card_type=Enemy, fewest_remaining_hp=True))` (modele gs163 Main Concern pour le
#    "most/fewest_remaining_hp", modele gs172 pour `otherwise_attach_to`).
#  - « Uses (3 plate counters) » : `desc.Uses = "3,plate"` (natif), compteur 'plate' ajoute a
#    `CardFace.COUNTER`.
#  - « prevent 2 of that damage and remove 1 plate counter » : `message.PreventDamage(2, effect)` +
#    `Faces.RemoveCountersOn([this], 1, 'plate', effect)` (modele `WhenFaceWouldDealDamage` +
#    `ReduceDamage`/`PreventDamage`, `damage.py`).
#
# ⚠ Mots-pieges : « ANY amount of damage » (meme 0 ou 1, l'interruption part quand meme) ; le plafond des
# 3 compteurs n'est pas une limite de declenchement imprimee ("Limit"), juste un decompte de charges — a 0
# compteur, la carte reste attachee mais la prevention ne dit rien d'un retrait automatique (texte muet,
# lecture litterale : elle continue de prevenir sans jamais aller sous 0, `RemoveCountersOn` plafonne deja
# a 0 en interne).


def GetAbilities() -> Sequence['Ability']:

    def prevenir(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> None:
        this = effect.this.CastTo(Attachment)
        message.PreventDamage(2, effect)
        Faces.RemoveCountersOn([this], 1, 'plate', effect)

    def sur_lhote(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> bool:
        return message.target is getattr(effect.this, 'bind_face', None)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Destroyer", card_type=Villain),
            otherwise_attach_to=Select.From(CardFinder(card_type=Enemy), fewest_remaining_hp=True),
        ),
        AbilityFactory.WhenDamageWouldBeDealtTo(
            AbilityType.ForcedInterrupt,
            Enemy,
            prevenir,
            conditions=[sur_lhote],
            allow_zero_damage=True,
        ),
    ]

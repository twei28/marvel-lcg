from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout


def AUnVehicule(face: 'CardFace') -> bool:
    """« a character with a VEHICLE attachment » : un attachement VEHICLE dans
    sa zone d'ameliorations."""
    try:
        return any(a.HasTrait("VEHICLE") for a in face.GetInventoryDeck().Get())
    except Exception:
        return False


def CapacitesDUnVehicule(seuil: int, **choix) -> Sequence['Ability']:
    """Sports Car / Motorcycle / Utility Van : « Attach to the enemy with the
    <critere> without a VEHICLE attachment. Otherwise, this card gains surge.
    Forced Interrupt: When attached character would take any amount of damage,
    place it here instead. If there is <seuil> or more damage here, discard this
    card. »  Le critere passe par AttachToFaceWhenPutIntoPlay (highest_atk,
    highest_sch, fewest_remaining_hp) ; la pose des degats copie 60117
    Assembled Armor (PreventDamage("All") + compteurs 'damage')."""

    def encaisse(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        total = message.will_take_damage
        if total <= 0:
            return
        message.PreventDamage("All", effect)
        Faces.PlaceCountersOn([this], total, 'damage', effect)
        if this.GetCounters('damage') >= seuil:
            Faces.DiscardAll([this], effect)

    def le_porteur(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.trigger is this.GetBindFace()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Enemy, not_with_attach=CardFinder(trait="VEHICLE")),
            if_cannot_gain_surge=True,
            **choix,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt, Enemy, encaisse, conditions=[le_porteur]),
    ]

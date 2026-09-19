from . import *

# * Adamantium-Laced Spine (TECH) — Permanent.
# Forced Interrupt: When Bullseye would take damage, prevent all but 3 of that
#   damage. Place the prevented damage here. Then, if there is 6 or more damage
#   here, flip this card.
# Le « damage here » est un compteur nomme 'damage' sur l'attachement ; le
# recto-verso passe par RetournerLaColonne (card.Flip + raccrochage, voir __init__).
# Attache a Bullseye a l'entree en jeu (stade II le « Find and attach »).

def GetAbilities() -> Sequence['Ability']:

    def colonne(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        total = message.will_take_damage
        evite = max(0, total - 3)
        if evite > 0:
            message.PreventDamage(evite, effect)
            Faces.PlaceCountersOn([this], evite, 'damage', effect)
        if this.GetCounters('damage') >= 6:
            RetournerLaColonne(this, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Bullseye")),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            CardFinder(name="Bullseye"),
            colonne,
        ),
    ]

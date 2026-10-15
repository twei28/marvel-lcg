from . import *

# Invisible Forcefield — ATTACHEMENT x2 (Skrull Elite - Xavin). Aucune icone de boost, aucun trait.
# Attach to the enemy with the highest printed hit points and without another Invisible Forcefield attached.
#   If you cannot, this card gains surge.
# Forced Interrupt: When any amount of damage would be dealt to attached character, place it here instead.
#   Then, if there is at least 5 damage here, discard this card.
#
# Cartes de reference :
#  - Attache : `AttachToFaceWhenPutIntoPlay(finder, highest_printed_hp=True, if_cannot_gain_surge=True)`
#    (attachment.py) ; « without another X attached » : `not_with_attach=CardFinder(name=...)` (modele sk098).
#  - Interruption qui detourne les degats : **`sk086`** Skrull Empire (`WhenUnitWouldTakeDamage(ForcedInterrupt,
#    ..., op)` + `message.SetBeInstead(effect)` + `Faces.PlaceCountersOn([this], montant, 'damage', effect)`) ;
#    **`39031`** Undercover Mojo ; `message.will_take_damage` = le montant reel apres preventions.
#  - « discard this card » : `Faces.DiscardAll([this], effect)`.
#
# ⚠ Mots-pieges : « highest PRINTED hit points » (PV imprimes, pas restants ; PV par joueur multiplies) ;
# « enemy » (sbire OU mechant) ; « WITHOUT ANOTHER Invisible Forcefield » (une seule par ennemi) ; « If you cannot,
# SURGE » (aucun ennemi eligible : la carte reste en jeu non attachee ? non : elle est defaussee par le moteur et
# la surge joue) ; « ANY AMOUNT » (au moins 1 degat) ; « place IT here » (les degats, en compteurs 'damage' sur
# cette carte, ne sont pas infliges) ; « AT LEAST 5 damage here » : seuil sur le total de la carte (un coup de 8
# met 8 et la carte part) ; les degats deja poses ne sont jamais rendus.


def GetAbilities() -> Sequence['Ability']:

    def detourne(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this
        montant = message.will_take_damage
        if montant <= 0:
            return
        message.SetBeInstead(effect)
        Faces.PlaceCountersOn([this], montant, 'damage', effect)
        if this.GetCounters('damage') >= 5:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Enemy, not_with_attach=CardFinder(name=NOM_CHAMP)),
            highest_printed_hp=True,
            if_cannot_gain_surge=True,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "AttachedCharacter", detourne),
    ]

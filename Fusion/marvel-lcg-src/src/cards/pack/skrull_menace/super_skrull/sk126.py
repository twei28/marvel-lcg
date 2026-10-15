from . import *

# Invisible Forcefield — ATTACHEMENT x3 (Super-Skrull). Aucune icone de boost.
# Attach to the enemy with the highest printed hit points and without another
#   Invisible Forcefield attached. If you cannot, this card gains surge.
# Forced Interrupt: When any amount of damage would be dealt to attached
#   character, place it here instead. Then, if there is at least 5 damage here,
#   discard this card.
#
# Cartes de reference :
#  - **`drive` CapacitesDUnVehicule** (Sports Car, pack fne) : TEXTE QUASI
#    IDENTIQUE — « Attach to the enemy with the <critere> without a VEHICLE
#    attachment. Otherwise, this card gains surge. Forced Interrupt: When attached
#    character would take any amount of damage, place it here instead. If there is
#    <seuil> or more damage here, discard this card » : `AttachToFaceWhenPutIntoPlay(
#    CardFinder(card_type=Enemy, not_with_attach=...), highest_printed_hp=True,
#    if_cannot_gain_surge=True)` + `WhenUnitWouldTakeDamage(ForcedInterrupt, Enemy, ...)`
#    + `PreventDamage("All")` puis compteurs 'damage' sur la carte.
#  - **`60117`** Assembled Armor / **`60167`** Mountain of Muscle : meme geste.
#
# ⚠ Mots-pieges : « ENEMY » (mechant OU sbire) ; « highest PRINTED hit points »
# (PV imprimes, pas restants) ; « WITHOUT ANOTHER Invisible Forcefield » (on saute
# les ennemis qui en portent deja une) ; « ANY AMOUNT of damage » (on ne
# declenche pas sur 0) ; « place it HERE » (les degats vont sur la carte, ils ne
# sont pas subis) ; « AT LEAST 5 » (>= 5, pas 5 exactement ; le seuil n'est pas
# double en expert, il n'est pas imprime ainsi) ; les degats TOUS places ici,
# meme ceux qui depassent le seuil.


def GetAbilities() -> Sequence['Ability']:

    def encaisse(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        total = message.will_take_damage
        if total <= 0:
            return
        message.PreventDamage("All", effect)
        Faces.PlaceCountersOn([this], total, 'damage', effect)
        if this.GetCounters('damage') >= 5:
            Faces.DiscardAll([this], effect)

    def le_porteur(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.trigger is this.GetBindFace()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Enemy, not_with_attach=CardFinder(name="Invisible Forcefield")),
            highest_printed_hp=True,
            if_cannot_gain_surge=True,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt, Enemy, encaisse, conditions=[le_porteur]),
    ]

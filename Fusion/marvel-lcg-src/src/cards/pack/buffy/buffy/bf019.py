from . import *

# Prophecy Girl — AMELIORATION (CONDITION), sans cout. Linked (Harvest).
# Interrupt: When Buffy's hit points are 3 or less, find Kendra and put her into play under your control and remove this card from the game.
#
# CARTES DE REFERENCE
#  - `WhenUnitWouldTakeDamage(Interrupt, <cible>, op, conditions=[..])` (sender_damage.py : `trigger.health`, `will_take_damage`).
#  - `mv012` / `Search.PlayerCard` + `PutIntoPlay(joueur, effect, under_control=True)` pour « find X and put it into play under your control » ;
#    `Faces.RemoveAllFromGame` pour « remove from the game ».
#
# ⚠ LECTURE PROVISOIRE (question posee a l'utilisateur) : « When Buffy's hit points are 3 or less » n'est pas un evenement du moteur. Lu comme :
#   quand Buffy s'apprete a subir des degats qui la laisseraient a 3 PV ou moins (ou qu'elle y est deja). `desc.Linked = "bf027"` (le complot Harvest, par card_id : « Harvest » est
#   aussi le nom de la traitrise officielle 05029).


def GetAbilities() -> Sequence['Ability']:

    def pas_plus_de_3_pv(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        Unused(effect)
        return message.trigger.health - message.will_take_damage <= 3

    def prophecy_girl(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = effect.GetInitiator()
        kendra = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            include_player_hand_cards=True,
            name=NOM_KENDRA,
        )
        if kendra:
            kendra.PutIntoPlay(joueur, effect, under_control=True)
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            CardFinder(name=NOM_BUFFY),
            prophecy_girl,
            conditions=[pas_plus_de_3_pv],
        ),
    ]

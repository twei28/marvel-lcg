from . import *

# * Shackled Wrath — pacte BARGAIN. Peril (natif). Capacites communes : `AbilitesDuPacte`.
# « Your identity's attacks gain overkill. Double the ATK value of your identity. »
#
# Cartes de reference : sm/symbiotic_strength/27169 et ares/ar008 (`message.GainOverKill(effect)` sur `WhenUnitWouldAttack`), mp012
# (doublement : `get_new_value` + `GiveKeywordToAttached`).
# ⚠ Mots-pieges : « identity's ATTACKS » : toutes les attaques de l'identite porteuse (de base ou par carte), pas celles des allies ni des autres
# joueurs ; « DOUBLE the ATK value » : +ATK imprime (donc x2).


def GetAbilities() -> Sequence['Ability']:
    def l_identite_porteuse(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return message.attacker is effect.this.CastTo(Attachment).GetBindFace()

    def overkill(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainOverKill(effect)

    def valeur_imprimee(effect: 'Effect', face: Any, ui: List['CardFace']) -> int:
        return getattr(face, "printed_attack", 0)

    return [
        *AbilitesDuPacte(),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, Identity, overkill, conditions=[l_identite_porteuse]),
        *AbilityFactory.GiveKeywordToAttached(Identity, get_new_value=valeur_imprimee, attack=1),
    ]

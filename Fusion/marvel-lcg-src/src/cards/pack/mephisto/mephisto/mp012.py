from . import *

# * Prideful Ambitions — pacte BARGAIN. Peril (natif). Capacites communes : `AbilitesDuPacte`.
# « Your identity ignores the patrol keyword and any crisis icons in play. Double the THW value of your identity. »
#
# Cartes de reference : nebu/nebula/22005 (`UnitIgnoreKeywordIcons(.., patrol=True, crisis=True)`), brawn/bw016 (`get_new_value` = multiplicateur du
# gain de `GiveKeywordToAttached`), mp009 (hand_size, meme fabrique sur `Identity`).
# ⚠ Mots-pieges : « YOUR identity » : seul le porteur ignore Patrol et Crise (pas les autres joueurs) ; « DOUBLE the THW value » : +THW imprime
# (le gain vaut la valeur imprimee, donc x2) ; alter-ego sans THW : 0 + 0.


def GetAbilities() -> Sequence['Ability']:
    def le_porteur(effect: 'Effect', message: 'Message.CheckIfEffectIsIgnoreKeyWord') -> bool:
        return message.effect.this is effect.this.CastTo(Attachment).GetBindFace()

    def valeur_imprimee(effect: 'Effect', face: Any, ui: List['CardFace']) -> int:
        return getattr(face, "printed_thwart", 0)

    return [
        *AbilitesDuPacte(),
        AbilityFactory.UnitIgnoreKeywordIcons(Identity, patrol=True, crisis=True, conditions=[le_porteur]),
        *AbilityFactory.GiveKeywordToAttached(Identity, get_new_value=valeur_imprimee, thwart=1),
    ]

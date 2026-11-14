from . import *
# Pirate's Rapier (Basic, amelioration 1 [physical]). WEAPON.
# Attach to a STARJAMMER ally. Max 1 per ally.
# Attached ally gets +1 ATK and its attacks gain piercing.
#
# Cartes de reference : 01074 Inspired (`CanPlayThisUpgradeCard(Ally)` + `*GiveKeywordToAttached(Ally, thwart=1)`) ;
# `UnitAttackGainKeyword(attacker, piercing=True, conditions=[..])` (do_attack.py:828) pour « its attacks gain piercing ».
# ⚠ « its attacks » : les attaques de l'allie PORTEUR (pas de toutes les allies) : condition `message.attacker is porteur`.
def GetAbilities() -> Sequence['Ability']:
    def attaque_du_porteur(effect: 'Effect', message: 'Message.CheckIfAttackMessageHasKeyword') -> bool:
        porteur = effect.this.GetBindFace()
        return porteur is not None and message.attacker is porteur
    return [
        AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Ally, trait="STARJAMMER")),
        *AbilityFactory.GiveKeywordToAttached(Ally, attack=1),
        AbilityFactory.UnitAttackGainKeyword(Ally, piercing=True, conditions=[attaque_du_porteur]),
    ]

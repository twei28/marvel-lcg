from . import *
# Tactical Teleporter (Justice, amelioration 1 [energy]). TECH.
# Attach to a STARJAMMER ally. Max 1 per ally.
# Attached ally gets +1 THW and ignores the guard keyword, the patrol keyword, and the crisis icon ([crisis]).
#
# Cartes de reference : 01074 Inspired (`CanPlayThisUpgradeCard(..)` + `*GiveKeywordToAttached(Ally, thwart=1)`) ; 22005 Evasive Maneuvering /
# 32002 Shadowcat (`UnitIgnoreKeywordIcons(finder, guard=True, patrol=True, crisis=True)`, play.py:517).
# ⚠ « Attached ally ignores... » : seulement le PORTEUR (condition `message.effect.this is porteur`) ; `UnitIgnoreKeywordIcons` appelle la
# condition avec le message `CheckIfEffectIsIgnoreKeyWord` dont `message.effect.this` est la carte qui agit (l'allie lui-meme pour un pouvoir
# de base ; l'heros d'un evenement n'est PAS le porteur).
def GetAbilities() -> Sequence['Ability']:
    def le_porteur(effect: 'Effect', message: 'Message.CheckIfEffectIsIgnoreKeyWord') -> bool:
        porteur = effect.this.GetBindFace()
        return porteur is not None and message.effect.this is porteur
    return [
        AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Ally, trait="STARJAMMER")),
        *AbilityFactory.GiveKeywordToAttached(Ally, thwart=1),
        AbilityFactory.UnitIgnoreKeywordIcons(
            Ally,
            guard=True,
            patrol=True,
            crisis=True,
            conditions=[le_porteur],
        ),
    ]

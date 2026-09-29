from cards.pack import *

################################################################################
# Pack Agent Anti-Venom — custom « DesignHacker ».
#
# Deux notions maison, absentes du moteur, sont centralisees ici.
#
# 1. « exactly 10 hit points remaining ». Cinq cartes du pack en dependent
#    (l'identite elle-meme, Dig Deep, Extricate...). 10 est aussi le total
#    imprime : la condition vaut donc « intact », mais on compare bien les PV
#    COURANTS a 10, pas health a max_health — un bonus de PV ne doit pas
#    satisfaire la condition.
#
# 2. « drain X from an enemy » : mot-cle du pack, jamais defini sur les cartes
#    fournies. Lecture retenue avec l'utilisateur le 4/8/2026 : X degats a
#    l'ennemi, puis X soins sur Agent Anti-Venom (et sur lui seul).
################################################################################

TEN = 10


def GetAgentAntiVenom(effect: 'Effect') -> Any:
    """L'identite du joueur qui resout l'effet, quelle que soit sa face."""
    initiator = effect.GetInitiator()
    if initiator is None:
        return None
    return initiator.GetIdentity()


def HasExactlyTen(effect: 'Effect', message: Any=None) -> bool:
    identity = GetAgentAntiVenom(effect)
    return identity is not None and identity.health == TEN


def Drain(source: 'CardFace', targets: Sequence['CardFace'], value: int, effect: 'Effect') -> None:
    """X degats a l'ennemi, puis X soins sur Agent Anti-Venom SI l'ennemi les a subis.

    ⚠ ALIGNE SUR LE GLOSSAIRE MC4DB LE 29/09/2026 (ce pack n'imprime aucune
    definition) : « deal X damage to that character's target. Then, IF THE
    TARGET TOOK THAT DAMAGE, heal X damage from the character who triggered
    drain ». Un ennemi Tough absorbe les degats : aucun soin. Le pack
    `venompool`, lui, imprime sa propre definition (soin inconditionnel) et la
    garde, fiche `docs/reference/mots-cles/drain-x.md`.
    ⚠ « A SUBI » SE LIT SUR LES POINTS DE VIE, PAS SUR LE RETOUR DE
    `DealDamage` : celui-ci compte les degats INFLIGES (`deal_damage`,
    avant prevention), et rendait 1 face a un vilain Tough (cas
    « av009 ... vilain TOUGH », rouge le 29/09/2026). Un ennemi vaincu par
    ces degats les a subis, meme si sa carte a quitte le terrain.
    """
    if not targets:
        return
    avant = {cible: cible.health for cible in targets if hasattr(cible, "health")}
    source.DealDamage(targets, value, effect)
    subis = any(cible.health < sante or cible.IsDefeated() or not cible.IsInPlay()
                for cible, sante in avant.items())
    if not subis:
        return
    identity = GetAgentAntiVenom(effect)
    if identity is not None:
        source.HealthUnits([identity], value, effect)


################################################################################
# « ranged » et « piercing » : tout passe par le moteur.
#
# Ten Out of Ten! (piercing a 10 PV) et Bear Arms (ranged sur la prochaine
# attaque) accordent leurs mots-cles par la fabrique standard
# `UnitAttackGainKeyword`. "I've Got This!" ne les devine donc PAS : elle porte
# `SetLabel('attack')`, ce qui fait passer ses degats par une vraie attaque, et
# lit le resultat sur `WhenRecalculateAttackDamage`.
#
# Consequence voulue : une carte d'aspect exterieure au pack qui accorde ranged
# ou piercing aux attaques du heros compte elle aussi pour le bonus, sans que le
# pack ait a la connaitre.
################################################################################

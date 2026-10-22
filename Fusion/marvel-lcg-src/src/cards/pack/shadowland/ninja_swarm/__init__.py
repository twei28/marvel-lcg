from cards.pack.shadowland import *
from cards.pack.fne import PeutCouvrirLeCout

# ===========================================================================
# Helpers du set NINJA SWARM (Shadowland, sl028 a sl036) : sbires du Clan de la Main, set modulaire des TROIS scenarios.
# Le mot-cle Teamwork (NINJA) est NATIF (`desc.Teamwork`, voir docs/reference/mots-cles/teamwork.md) : aucun script ne le recode.
# ===========================================================================


def UnAllieDefend(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> bool:
    """« If an ally is defending against this attack » (boost de sl028 et sl029) : le DEFENSEUR de l'attaque pour laquelle la carte est revelee en boost est un ALLIE
    (la defense d'un heros ou d'une identite ne compte pas). Faux hors attaque (boost reveles pour une manigance)."""
    attaque = getattr(message, 'would_atk_message', None)
    defenseur = attaque.GetDefender() if attaque is not None else None
    return defenseur is not None and Ally.IsType(defenseur)


def JoueurQuiVainc(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> 'Player|None':
    """« The defeating player » : le joueur qui a vaincu le sbire, a defaut (vaincu par un effet sans joueur) celui avec qui il etait engage."""
    return getattr(message, 'defeating_player', None) or effect.this.CastTo(Minion).GetEngagedPlayer()


def DefausserDeuxEtReveler(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
    """« When Defeated : The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way »
    (sl030 a sl034). « the first » = la plus haute des deux, dans l'ORDRE de defausse ; « with the teamwork keyword » = mot-cle IMPRIME (`printed_teamwork`) : une carte
    defaussee n'a plus de mots-cles courants. Les deux cartes restent defaussees ; seul le sbire trouve est revele (engage avec le joueur qui a vaincu)."""
    joueur = JoueurQuiVainc(effect, message)
    if joueur is None:
        return
    for face in Worlds.DiscardEncounterCards(2, effect):
        if Minion.IsType(face) and face.printed_teamwork:
            face.Reveal(joueur, effect)
            return

from . import *

# Unrelenting Hate (treachery) — boost [star]+1.
# When Revealed: Your nemesis minion activates against you. If your nemesis
#   minion is not in play, find it and reveal it. If you cannot find it, find an
#   UNDERLING minion that is not in play and reveal it.
# [star] Boost: If this activation is an attack, it gains overkill.
# Modeles : 60074 (DoActivate), Find.FindAndReveal (fouille deck, defausse,
# mise de cote, jamais la zone retiree), an013 (GainOverKill en boost).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        sbire = SbireNemesisEnJeu(joueur, effect)
        if sbire is not None:
            sbire.DoActivate(joueur, effect)
            return
        trouve = Find.FindAndReveal(effect, joueur, finder=CardFinder(card_type=Minion, is_nemesis=joueur))
        if trouve is None:
            TrouverEtRevelerUnderling(effect, joueur)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        attaque = getattr(message, 'would_atk_message', None)
        if attaque is not None:
            attaque.GainOverKill(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]

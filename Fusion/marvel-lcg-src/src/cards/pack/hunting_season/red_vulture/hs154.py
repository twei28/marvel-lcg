from . import *

# hs154 Acid Expulsion
# When Revealed : defaussez 5 cartes de rencontre ; par icone de boost, defaussez 1 carte du dessus de votre deck.
# Boost : apres cette attaque, defaussez 1 carte du deck par degat subi.

def GetAbilities() -> Sequence['Ability']:

    def expulser(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        avant = list(Worlds.GetEncounterDiscardPileCards(effect))
        Worlds.DiscardEncounterCards(5, effect)
        nouvelles = [c for c in Worlds.GetEncounterDiscardPileCards(effect) if c not in avant]
        icones = sum(c.boost_const for c in nouvelles)
        if icones > 0:
            message.GetToPlayer().DiscardDeckTopCards(icones, effect)

    def en_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        avant = identite.health

        def apres() -> None:
            subi = avant - identite.health
            if subi > 0:
                joueur.DiscardDeckTopCards(subi, effect)

        message.AfterThisActivation(effect, apres)

    return [
        AbilityFactory.WhenThisRevealed(None, expulser),
        AbilityFactory.WhenCardBecomeBoost("This", en_boost),
    ]

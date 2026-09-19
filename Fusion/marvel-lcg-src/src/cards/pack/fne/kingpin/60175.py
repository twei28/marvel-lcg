from . import *

# Bag of Tricks (treachery) — boost [star] seule.
# When Revealed: Reveal a random card from your set-aside nemesis set. If no
#   card is revealed this way, this card gains surge.
# [star] Boost: Give this character a random card from your set-aside nemesis
#   set as an additional boost card.
# Modeles : 01190 Shadow of the Past (player.set_aside_nemesis_sets),
# Rand.RandomChoice (60112), CanBoost.GiveBoostCard (60094 : la carte rejoint la
# pile de boost, la boucle de ResolveBoostCards la retourne dans la foulee).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        cartes = CartesNemesisMisesDeCote(joueur)
        if not cartes:
            ThisCardGainSurge(effect)
            return
        carte = Rand.RandomChoice(cartes, effect)
        if carte.Reveal(joueur, effect) is None:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        ennemi = message.activating_enemy
        cartes = CartesNemesisMisesDeCote(joueur)
        if not cartes or ennemi is None or not CanBoost.IsType(ennemi):
            return
        carte = Rand.RandomChoice(cartes, effect)
        ennemi.GiveBoostCard(carte, effect, getattr(message, 'would_atk_message', None))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]

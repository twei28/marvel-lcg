from . import *

# * DJ: Mark Sheppard
# MUTANT. X-MEN.
# Forced Response: After DJ enters play, perform the following for each SONG
#   card used to pay for him:
#   - remove 2 threat from a scheme.
#   - give him a tough status card.
#   - deal 1 damage to an enemy.
#
# « for each SONG card USED TO PAY for him » : le moteur garde la trace des
# ressources depensees dans le message de jeu (`paid_res_effects`), chaque
# effet-ressource portant la carte qui l'a produite. On compte donc les cartes
# payantes qui avaient le trait [[SONG]].
#
# On passe par `AfterPlayerPlayedCard` et non `AfterCardEnterPlay` : seule la
# premiere connait le paiement.


def GetAbilities() -> Sequence['Ability']:

    def dj(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        chansons = 0
        for res_effect in (message.paid_res_effects or []):
            face = getattr(res_effect, "this", None)
            if face is not None and face.HasTrait(TRAIT_SONG):
                chansons += 1
        if chansons <= 0:
            return

        schemes = [s for s in Worlds.FindCardsOnField(effect, card_type=Scheme2)
                   if s.threat > 0]
        ennemis = list(Worlds.FindCardsOnField(effect, card_type=Enemy))

        # « perform the following FOR EACH » : les trois lignes, autant de fois
        # qu'il y a eu de chansons depensees.
        for _ in range(chansons):
            if schemes:
                this.RemoveThreatFromSchemes([schemes[0]], 2, effect)
            Faces.GiveStatus([this], "Tough", effect)
            if ennemis:
                this.DealDamage([ennemis[0]], 1, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.ForcedResponse,
            "You",
            "This",
            dj,
        ),
    ]

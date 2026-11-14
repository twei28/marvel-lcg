from . import *

# Chinatown (9) — LIEU (environnement LOCATION).
# Interrupt: When you would be dealt an encounter card, instead discard from the encounter deck until a minion is discarded.
# Reveal that minion. (Limit once per round.)
#
# Cartes de reference : 53009 (Aerial Recon : Interrupt `WhenPlayerWouldBeDealtEncounterCard` + `message.SetBeInstead(effect)`),
# 16057 (Planetary Invasion : `Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)` puis `minion.Reveal(joueur, effect)`),
# pu031 (limite globale + `Ville.AuLieu`).
# ⚠ « When YOU would be dealt » : le joueur qui occupe Chinatown (`Ville.AuLieu` lit `message.GetToPlayer()`), pas n'importe quel joueur
# (53009 dit « a player »). « INSTEAD » : la carte n'est PAS distribuee, `SetBeInstead` ; le sbire est revele POUR ce joueur
# (il s'engage avec lui). Interrupt = au choix du joueur.

def GetAbilities() -> Sequence['Ability']:

    def a_la_place(effect: 'Effect', message: 'Message.WhenPlayerWouldBeDealtEncounterCard') -> None:
        message.SetBeInstead(effect)
        joueur = message.GetToPlayer()
        sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if sbire:
            sbire.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenPlayerWouldBeDealtEncounterCard(AbilityType.Interrupt, a_la_place, conditions=[Ville.AuLieu])
        .LimitOncePerRound(),
    ]

from . import *

# Public Support (LOW) — environnement recto-verso (60163a,60163b), mis en jeu
# par le When Revealed de The King's Gambit 1B.
# Forced Response: After a minion is defeated, place 1 support counter here.
# Forced Interrupt: When the villain phase begins, if there are at least
#   2[per_hero]+2 support counters here, flip Kingpin and advance the main
#   scheme to stage 2A. Then, flip this card.
# Modeles : 60094 (AfterUnitBeDefeated Minion), 60112 Disturbed Psyche
# (card.Flip du vilain), WhenVillainPhaseBegin (nt011), MainScheme.Advance("2A")
# (scheme_main.py:175 -> world.AdvanceMainScheme). Le retournement de
# l'environnement lui-meme : card.Flip (il n'est pas attache, pas de
# RetournerLAttachement) ; les compteurs restent sur la carte (60068a/b).

def GetAbilities() -> Sequence['Ability']:

    def seuil_atteint(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> bool:
        return effect.this.GetCounters('support') >= 2 * Worlds.GetPlayerNumIcon(effect) + 2

    def bascule(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this
        kingpin = TrouverKingpin(effect)
        if kingpin is not None:
            kingpin.card.Flip(effect)
        complot = Worlds.FindMainScheme(effect)
        if complot is not None and complot.printed_stage == 1:
            complot.Advance("2A", effect)
        this.card.Flip(effect, call_reveal=False)

    return [
        ReponseForceeSoutien(),
        AbilityFactory.WhenVillainPhaseBegin(AbilityType.ForcedInterrupt, bascule, conditions=[seuil_atteint]),
    ]

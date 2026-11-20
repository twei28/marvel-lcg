from . import *

# Diplomatic Sabotage (1B), stade 1. Menace 7[per_hero], escalade +1[per_hero], menace de depart 1[per_hero].
# « Forced Response : After your turn ends, if there is Cassandra Controls counter on your identity, you must choose to either place 1 threat here
# or take 2 damage. Hero Action : Discard 5 cards from the top of the encounter deck -> remove a Cassandra Controls counter from your identity.
# (Limit once per round per player.) »
# Cartes de reference : sk193b (complot B : `AfterPlayerTurnEnd(ForcedResponse, "AnyPlayer")`), gb006b (Hero Action de complot a cout
# `DiscardDeckTopCards`), 27065 (`LimitOncePerRoundPerPlayer`).
# ⚠ « take 2 damage » : degats DIRECTS a l'identite (pas indirects) ; « your turn » : le joueur dont le tour finit, pour SES compteurs.


def GetAbilities() -> Sequence['Ability']:
    def expert(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        """Texte du Setup de 1A : « In expert mode, advance to stage 2A. » (voir hf604a : la face B est seule en jeu a la fin de la mise en place)."""
        this = effect.this.CastTo(MainScheme)
        if Worlds.IsExpert(effect) and this.IsInPlay():
            this.Advance("2A", effect)

    return [
        AbilityFactory.AfterGameSetup(expert),
        ReponseFinDeTour(1, "Take 2 damage", PenaliteDegats),
        ActionRetirerControle(5),
    ]

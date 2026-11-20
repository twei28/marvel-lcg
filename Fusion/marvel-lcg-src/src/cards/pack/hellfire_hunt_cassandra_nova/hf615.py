from . import *

# Shatter Your Mind (TREACHERY PSIONIC TACTIC, x3 : hf613-hf615). Boost 2. « When Revealed : Discard X cards from the encounter deck, where X is
# equal to double the villain's stage number. Each time a Cassandra Nova card is discarded this way, place 1 Cassandra Controls counter on your
# identity. »
# Cartes de reference : `Worlds.DiscardEncounterCards` (hf104a / WQ `DefausserEtCompterIcones`), sp006b (`set_name` d'une carte) ; stade = `printed_stage`.
# ⚠ « Cassandra Nova card » : une carte de l'ensemble Cassandra Nova (le `set_name`) ; un compteur PAR carte, pose un a un (chaque pose peut
# declencher Cassandra Domination) ; « the villain's stage number » : 1, 2 ou 3 (le chiffre romain, en expert aussi).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        villain = VilainCN(effect)
        if villain is None:
            return
        faces = Worlds.DiscardEncounterCards(2 * villain.printed_stage, effect)
        nova = [f for f in faces if getattr(f.paper, "set_name", None) == ENSEMBLE_CN or f.IsName(NOM_CN)]
        for _ in nova:
            PoserControle(effect, joueur, 1)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]

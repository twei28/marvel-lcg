from . import *

# Asteroid M B
#
# ERRATA RRG 1.8 (Annexe V, Mutant Genesis #141B / #142B / #143B) : « Forced Response: After you place a magnet counter on this scheme, if there are at least 3 magnet
#   counters here, REMOVE 3 OF THEM and discard cards from the encounter deck until a [[Magnetic]] card is discarded. Reveal that card. » (les 3 compteurs sont retires
#   AVANT la revelation ; l'ancien texte disait « ... Reveal that card, then remove 3 magnet counters from this scheme »).
#   Le script de 32141b suit DEJA le nouvel ordre (retrait puis defausse puis revelation).
#   ⚠ CE MODULE SERT AUX TROIS STADES : `32142b` (Factory Online) et `32143b` (The Rule of Magnus) portent `ability_link: 32141b` dans cards.json et chargent donc CE script
#   (verifie le 03/11/2026 par substitution : un module 32142b.py cree par erreur etait ignore et a ete retire). Cas `32141b`/`32142b`/`32143b` de `tools/cas/errata_rrg.py`.

def GetAbilities() -> Sequence['Ability']:

    def asteroid_m(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        if this.GetCounters('magnet') >= 3:

            Faces.RemoveCountersOn([this], 3, 'magnet', effect)

            face = Worlds.DiscardEncounterCardsUntil(
                effect,
                trait="MAGNETIC",
            )
            if face:
                face.Reveal(None, effect)

    return [
        AbilityFactory.AfterCounterPlacedOn(
            AbilityType.ForcedResponse,
            "This",
            'magnet',
            asteroid_m,
            at_least=3
        ),
    ]


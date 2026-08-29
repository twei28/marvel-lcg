from . import *

# Massive Attack
#
# Hinder 2 = desc.Hinder="2*" (lu nativement, voir mots-cles/hinder.md).
# Boost qui met la carte en jeu : modele Goblin Nation (gob/02027.py),
# `WhenCardBecomeBoost("This", PutThisIntoPlay)`. Degats au joueur qui revele :
# `message.GetToPlayer()` (et non `effect.GetInitiator()`, qui leve une
# assertion quand l'initiateur est le vilain -- modele Dazzler Concert()).
# Simplification assumee : le texte dit "the Tony Stark player", rendu par
# "you" (le joueur qui affronte ce set nemesis) -- fonctionnellement identique
# puisqu'un set nemesis n'est jamais affronte par un autre heros.
#
# CORRECTIF (bug trouve en test) : la classe s'appelle `EncounterSideScheme`
# (game/card/face/card_type/scheme_side.py), PAS "SideScheme" -- ce nom
# n'existe nulle part dans le moteur. `test_cards.py` ne l'a jamais vu : le
# `CastTo` est a l'INTERIEUR de la fonction, seulement evalue quand la carte
# est vraiment revelee (le moteur avale l'exception, voir mots-cles/README).

def GetAbilities() -> Sequence['Ability']:

    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        player = message.GetToPlayer()
        this.DealDamage([player.GetIdentity()], 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            when_revealed,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            PutThisIntoPlay,
        ),
    ]

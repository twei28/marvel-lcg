from . import *

# Back from Hel — traitrise nemesis. Boost 1.
# When Revealed: Search the encounter discard pile for the bottom most minion
#   and reveal it.
# [star] Boost: If you are engaged with a minion, this attack gains 1
#   additional boost icon ([boost]).
#
# Cartes de reference : ss019 * Bella Donna (pack scarlet_spider) pour
# `Search.EncounterCard(include_discard_pile=True, card_type=Minion)` puis
# `face.Reveal(None, effect)`, et 02030 (pack gob) pour un [star] Boost qui
# ajoute une icone de boost.
#
# ⚠ « the BOTTOM MOST minion » : pas n'importe lequel, le plus profond de la
# defausse de rencontre. Le moteur ne propose pas ce filtre : on lit la pile
# nous-memes et on prend le dernier sbire trouve.

def GetAbilities() -> Sequence['Ability']:

    def back_from_hel(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this, message)

        pile = list(Worlds.GetEncounterDiscardPile(effect).Get(True))
        sbires = [f for f in pile if Minion.IsType(f)]
        if not sbires:
            return
        sbires[-1].Reveal(None, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        if joueur.engaged_minions.GetSize() > 0:
            message.AddBoostIcon(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            back_from_hel,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]

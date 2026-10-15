from . import *

# Power Multiplying — TRAITRISE x4 (Super-Skrull). Icone ★ de boost seule.
# When Revealed: Reveal the top card of the SUPERPOWER deck. If you cannot, this
#   card gains surge.
# ★ Boost: This card gets +1 boost icon for each SUPERPOWER attachment attached
#   to Super-Skrull.
#
# Cartes de reference :
#  - **`sk106`** Wrath of the Empire (scenario 1) : `message.GainBoostIcon(n,
#    effect)` dans un `WhenCardBecomeBoost("This", ...)` (modele 46028 Burn).
#  - **`sk120b`** (ce set) : reveler la carte du dessus du paquet SUPERPOWER ;
#    `ThisCardGainSurge` (surge natif) si le paquet est vide (« If you cannot »,
#    modele `fne/60084` Energy Overload).
#
# ⚠ Mots-pieges : « If YOU CANNOT » = paquet vide (rien a reveler), pas « si le
# pouvoir n'a pas pu s'attacher » ; « each SUPERPOWER attachment ATTACHED TO
# SUPER-SKRULL » (comptes a la resolution du boost, pas ceux du paquet) ; l'icone
# Y est une icone de boost ordinaire ; la carte n'a PAS d'icone Y imprimee (desc
# sans `Boost`, seulement l'etoile).


def GetAbilities() -> Sequence['Ability']:

    def multiplier(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        if not RevelerSuperpouvoir(effect):
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        n = len(SuperpouvoirsAttaches(effect))
        if n:
            message.GainBoostIcon(n, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, multiplier),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]

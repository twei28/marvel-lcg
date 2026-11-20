from . import *

# Kree Secret Laboratory — MANIGANCE ANNEXE (ensemble Doctor Minerva). Hinder 1.
# [star] Boost: If this activation is a scheme, reveal this card.
#
# Cartes de reference :
#  - « If this activation is a scheme, reveal this card » : `WhenCardBecomeBoost` + `message.would_sch_message`
#    (present seulement si l'activation boostee est une manigance, modele sk196 pour `this.Reveal`).
#
# ⚠ Mots-pieges : « reveal this card » depuis la pile de boost (face cachee) : une simple revelation,
# PAS un retour dans le deck de rencontre (elle reste dans la pile de boost du mechant, visible).


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if getattr(message, 'would_sch_message', None) is None:
            return
        this = effect.this
        joueur = message.GetToPlayer()
        this.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]

from . import *

# Backstab — TRAITRISE, aspect Justice (Elektra Natchios 35). Linked (Double-Cross).
# When Revealed: Deal 4 damage to the villain. This card gains surge.
# [star] Boost: If an enemy is activating, deal 2 damage to it. Otherwise, this card gains [boost][boost].
#
# CARTES DE REFERENCE
#  - `01168` Sweeping Swoop : « This card gains surge » = `this.GainSurge(1, effect)` dans `WhenThisRevealed`.
#  - `56150` : `this.GainBoostIcons(2, effect)` dans un Boost ; `ar011`/`sk039` : `message.activating_enemy` (None si c'est une manigance).
#  - `pu020` : `this.DealDamage([vilain], N, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « the villain » : le vilain, pas un sbire ; « This card gains SURGE » : la carte suivante est revelee.
#  ⚠ `activating_enemy` peut etre un ALLIE Villainous (Black Cat 63016) : `Enemy.IsType` le distingue d'un vrai ennemi (vilain, sbire).
#  ⚠ Boost « IF AN ENEMY is activating » : un ennemi (vilain OU sbire) qui active ; sinon (activation de complot) : DEUX icones boost de plus.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(message)
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            this.DealDamage([vilain], 4, effect)
        this.GainSurge(1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        ennemi = message.activating_enemy
        if ennemi is not None and Enemy.IsType(ennemi):
            this.DealDamage([ennemi], 2, effect)
        else:
            this.GainBoostIcons(2, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]

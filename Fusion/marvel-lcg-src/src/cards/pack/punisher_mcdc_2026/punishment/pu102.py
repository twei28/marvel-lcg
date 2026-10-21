from . import *

# Bullet Spray — TRAITRISE x2. Boost ★.
# When Revealed : Deal 1 damage to each character you control. Deal 1 damage to the TARGETED villain and each minion engaged
#   with you.
# ★ Boost : Deal 1 damage to the TARGETED villain.
#
# Cartes de reference : `DealDamage` (pu059/pu099), `joueur.GetControlCharacters()`, `joueur.engaged_minions`.
# ⚠ « each character YOU control » : identite et allies ; « each minion engaged with YOU » : seulement ceux engages avec le joueur
# qui revele ; le vilain cible (pas Punisher). Degats de la carte, pas d'une attaque.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        persos = list(joueur.GetControlCharacters())
        if persos:
            this.DealDamage(persos, 1, effect)
        cibles = list(joueur.engaged_minions.Get())
        if cibles:
            this.DealDamage(cibles, 1, effect)
        cible = VilainCible(effect)
        if cible is not None:
            this.DealDamage([cible], 1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        cible = VilainCible(effect)
        if cible is not None:
            effect.this.DealDamage([cible], 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]

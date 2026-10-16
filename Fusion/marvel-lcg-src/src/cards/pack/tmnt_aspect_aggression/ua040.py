from . import *

# * Ujigami (Splinter) — ALLIE 4 [physical], ATK 2 (1), THW 2 (1), PV 3. NINJA. MARTIAL ARTIST. RAT.
# Bandeau « ✦ Shang-Chi » sous le titre : unicite jugee sur les deux titres (Q-R1, `unique_also`).
# Ujigami enters play with 10 dagger counters on him.
# Action: Remove 1 dagger counter from here → deal 1 damage to an enemy. (Limit twice per round.)
#
# CARTES DE REFERENCE
#  - `38003` * Gambit : `ThisEnterPlayWithCounters(N, '<compteur>')` + `CostFunc.Counter("This", 1, ...)`
#    (compteur 'dagger' ajoute a `CardFace.COUNTER`, 16/10/2026).
#  - `hc001a` * Hellcat : « (Limit twice per round.) » = DEUX capacites identiques, chacune
#    `.LimitOncePerRound()` (le moteur n'a que la limite « une fois »).
# TEXTE CONTRE CODE
#  ⚠ « Action » (pas Hero Action) : jouable dans les deux formes, pendant votre tour.
#  ⚠ « Limit TWICE per round » : la 3e utilisation dans le round est refusee (temoin d'epuisement).
#  ⚠ « from HERE » = d'Ujigami.


def GetAbilities() -> Sequence['Ability']:

    def dague(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.DealDamage(effect.targets, 1, effect)

    def action() -> 'Ability':
        return AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            dague,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'dagger')).SetTarget(Enemy).LimitOncePerRound()

    return [
        AbilityFactory.ThisEnterPlayWithCounters(10, 'dagger'),
        action(),
        action(),
    ]

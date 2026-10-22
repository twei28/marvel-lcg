from . import *

# * Shang-Chi (Zheng Shang-Chi) — ALLIE 4 [physical], aspect Aggression (Elektra Natchios 15). HERO FOR HIRE. MARTIAL ARTIST.
#   PV 3, THW 2*, ATK 2*.
# Shang-Chi enters play with 10 ring counters on him.
# Action: Remove 1 ring counter from here → deal 1 damage to an enemy. (Limit twice per round.)
#
# CARTES DE REFERENCE
#  - `ua040` Ujigami (aspect TMNT d'Inkwire, MEME texte avec « dagger ») : `ThisEnterPlayWithCounters(10, ...)` +
#    `CostFunc.Counter("This", 1, ...)` ; « (Limit twice per round) » = DEUX capacites identiques, chacune
#    `.LimitOncePerRound()` (le moteur n'a que la limite « une fois ») ; modele `hc001a` Hellcat.
#  - `09014` Iron Fist (Danny Rand) : `ThisEnterPlayWithCounters(2, 'mystic')`.
#
# TEXTE CONTRE CODE
#  ⚠ « Action » (pas Hero Action) : jouable dans les deux formes, pendant votre tour.
#  ⚠ « Limit TWICE per round » : la 3e utilisation dans le round est refusee (temoin d'epuisement).
#  ⚠ « from HERE » = de Shang-Chi ; « deal 1 damage » : 1 degat, pas une attaque (aucune etiquette (attack)).
#  ⚠ Unique (✦ imprime) : « * » devant le nom.


def GetAbilities() -> Sequence['Ability']:

    def anneau(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.DealDamage(effect.targets, 1, effect)

    def action() -> 'Ability':
        return AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            anneau,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'ring')).SetTarget(Enemy).LimitOncePerRound()

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.ThisEnterPlayWithCounters(10, 'ring'),
        action(),
        action(),
    ]

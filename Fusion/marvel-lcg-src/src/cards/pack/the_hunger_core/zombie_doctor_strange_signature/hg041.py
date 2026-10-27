from . import *

# Crimson Bands of Cyttorak — ATTACHEMENT (set signature Zombie Doctor Strange, carte 2/3). Traits SPELL, MYSTIC.
# Attach to your hero.
# Your hero cannot attack.
# Hero Action: Spend 2 resources of different types and exhaust your hero -> discard this card.
#
# Cartes de reference :
#  - Attache a « your hero » (pas « your identity ») : `hg027` Rotten Web (meme pack, deck signature Zombie
#    Spider-Man, carte 1/3) : `AbilityFactory.AttachToFaceWhenPutIntoPlay("YourHero")`, retenu au mot pres parce
#    que le texte imprime de hg041 dit bien « your hero », jamais « your identity ». `09030` Counterspell
#    (Doctor Strange Nemesis) confirme le meme choix de fabrique pour « your hero ».
#  - « Attached identity/hero cannot attack » : `32150` Wrapped in Metal (Magneto, Attachment officiel,
#    « Attached identity cannot thwart, attack, defend, or recover ») : `*AbilityFactory.UnitCannotAttackTarget(
#    "AttachedIdentity", cannot_attack=True, cannot_trigger_attack_ability=True)` -- repris ici en ne gardant que
#    la restriction D'ATTAQUE (hg041 n'imprime ni « cannot thwart » ni « cannot defend » ni « cannot recover »,
#    contrairement a 32150). Meme fabrique vue sur `32055` Permanently Phased (mut_gen/shadowcat) pour le meme
#    schema « AttachedIdentity + cannot_attack=True ».
#  - Cout de defausse compose « Spend 2 resources of different types AND exhaust your hero -> discard this
#    card » : meme schema que `32150` (`.SetCost(Cost("R")).SetCostFunc(CostFunc.Exhaust("YourIdentity"))`), ici
#    avec `Cost("2", different_type=True)` (meme cout de ressources que `hg027`, qui utilise
#    `Cost("3", different_type=True)` pour « Spend 3 resources of different types ») et
#    `CostFunc.Exhaust("YourHero")` (plus de 40 cartes du depot, ex. `04102` Taskmaster, `01153` Under Attack,
#    pour « and exhaust your hero », coherent avec l'attache sur « YourHero » plutot que « YourIdentity »).
#
# [!] Mots-pieges verifies :
#  - « Attach to YOUR HERO » : vise la forme HEROS precisement (comme `hg027`/`09030`), pas « your identity »
#    (qui suivrait l'identite quelle que soit sa face courante, cf. `32150`/`32055`) -- rien a coder en plus,
#    c'est la fabrique `AttachToFaceWhenPutIntoPlay("YourHero")` elle-meme qui porte cette restriction.
#  - « Your hero CANNOT ATTACK » : restriction totale, non qualifiee (pas « cannot attack <cible>, » ni
#    « unless »/« otherwise »/« without ») -- `cannot_attack=True` (pas un `CardFinder` de cible), comme `32150`.
#    Pas de « cannot thwart/defend/recover » imprime sur cette carte (contrairement a `32150`) : ne pas copier
#    ces trois fabriques en plus.
#  - `cannot_trigger_attack_ability=True` : convention retenue sur toutes les cartes « cannot attack » attachees
#    a une identite deja vues dans le depot (`32150`, `32055`) -- une capacite declenchee par une tentative
#    d'attaque (ex. "Whenever this attacks") ne doit pas non plus pouvoir partir.
#  - « Hero Action » SANS « (Any player can do this.) » imprime : contrairement a `hg027` (« Hero Action
#    (any player) », `.AnyPlayerCanDoThis()`), ce texte ne porte aucune mention equivalente -- ne pas ajouter
#    `.AnyPlayerCanDoThis()` : seul le joueur controlant le heros attache (donc le heros a exhaust lui-meme)
#    peut activer l'action.
#  - « Spend 2 resources OF DIFFERENT TYPES » : `Cost("2", different_type=True)` -- deux ressources dont les
#    deux types different (different de "2 resources of any type", qui n'imposerait aucune contrainte de type).
#  - « AND exhaust your hero » : cout COMPOSE, deux parties a payer ensemble (pas une alternative "or") --
#    `.SetCost(...)` pour la partie ressources et `.SetCostFunc(CostFunc.Exhaust("YourHero"))` pour la partie
#    exhaustion, comme `32150` qui combine les deux de la meme facon.
#  - Traits imprimes SPELL, MYSTIC : traits DE SAVEUR (comme ARTIFACT/MYSTIC sur `hg040`, meme deck signature,
#    et ATTACK sur `hg016`) -- absents de `docs/reference/mots-cles/README.md`, rien a coder pour eux.
#  - "Hero Action" (simple) : type d'habilite natif du moteur (`AbilityType.HeroAction`), pas un mot-cle avec
#    fiche a part (meme constat que `hg027`).
#  - Pas de surge, pas de choix de cible, pas de limite imprimee ("Limit once per round/phase") sur cette
#    carte : rien d'autre a coder.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourHero",
        ),
        *AbilityFactory.UnitCannotAttackTarget(
            "AttachedIdentity",
            cannot_attack=True,
            cannot_trigger_attack_ability=True,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("2", different_type=True))
        .SetCostFunc(CostFunc.Exhaust("YourHero")),
    ]

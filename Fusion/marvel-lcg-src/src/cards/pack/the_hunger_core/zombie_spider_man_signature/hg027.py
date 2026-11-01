from . import *

# Rotten Web — ATTACHEMENT (deck signature de Zombie Spider-Man, carte 1/3). Trait CONDITION.
# Attach to your hero.
# Your hero gets -1 ATK and -1 THW.
# Hero Action (any player): Spend 3 resources of different types -> discard this card.
#
# Cartes de reference :
#  - Attache a « your hero » (pas « your identity ») : `09030` Counterspell (Doctor Strange Nemesis), seule
#    CONDITION du depot qui ecrit `AttachToFaceWhenPutIntoPlay("YourHero")` au lieu de "YourIdentity" --
#    modele retenu au mot pres parce que le texte imprime de hg027 dit bien « your hero », jamais
#    « your identity » (porte sur la forme HEROS precisement, pas sur l'identite quelle que soit sa forme).
#  - Malus de stats sur le porteur attache : `16123` Obedience Potion (Galactic Artifacts) :
#    `AbilityFactory.GiveKeywordToAttached("Character", thwart=-1, attack=-1, defense=-1)` -- repris ici avec
#    seulement `thwart=-1, attack=-1` (aucun malus DEF imprime sur Rotten Web).
#  - Cout de defausse « Spend 3 resources of different types -> discard this card. (Any player can do this.) » :
#    texte IDENTIQUE a `16125` The Poison (Galactic Artifacts) :
#    `AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("3", different_type=True))
#    .AnyPlayerCanDoThis()`.
#
# ⚠ Mots-pieges verifies :
#  - « Attach to YOUR HERO » : vise la forme HEROS precisement (comme `09030`), distinct de « your identity »
#    (ex. `16123`/`16125`) qui suit l'identite quelle que soit sa face courante -- rien a coder en plus, c'est
#    la fabrique `AttachToFaceWhenPutIntoPlay("YourHero")` elle-meme qui porte cette restriction.
#  - « gets -1 ATK and -1 THW » : exactement deux stats modifiees, aucun malus DEF -- ne pas copier le
#    `defense=-1` du modele `16123`.
#  - « Hero Action (ANY PLAYER) » : `.AnyPlayerCanDoThis()`, comme `16125` -- n'importe quel joueur peut payer
#    le cout et defausser la carte, pas seulement celui dont le heros la porte.
#  - « Spend 3 resources OF DIFFERENT TYPES » : `Cost("3", different_type=True)` -- trois ressources dont
#    aucune paire n'est du meme type (different de "3 resources of any type", vu sur `sf014`/Sunfire Nemesis,
#    qui n'impose aucune contrainte de type).
#  - Trait imprime CONDITION : trait DE SAVEUR (statut nefaste), sans module moteur associe -- meme
#    constat que le trait ATTACK sur `hg016` (absent de `docs/reference/mots-cles/README.md`).
#  - "Hero Action" (simple ou "any player") : type d'habilite natif du moteur (`AbilityType.HeroAction` +
#    `.AnyPlayerCanDoThis()`), pas un mot-cle avec texte de rappel a ficher a part (comme Response/Interrupt,
#    absents eux aussi de `mots-cles/`).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourHero",
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            thwart=-1,
            attack=-1,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("3", different_type=True))
        .AnyPlayerCanDoThis(),
    ]

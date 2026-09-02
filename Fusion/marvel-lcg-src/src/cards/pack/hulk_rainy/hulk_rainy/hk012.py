from . import *

# Limitless Strength — amelioration signature, x1 (n/15 = 15).
# CONDITION. GAMMA. SUPERPOWER. Cout 3, ressource [physical].
# Hulk gets +1 ATK.
# Hero Resource: Exhaust Limitless Strength -> generate a [physical] resource.
#
# Cartes de reference :
#  - `an002` * Sera pour le bonus nomme : « HULK gets +1 ATK » cite un nom
#    PROPRE, et « Hulk » est le nom de la seule face HEROS (l'alter-ego
#    s'appelle « Bruce Banner »). Le bonus ne vaut donc qu'en forme de heros,
#    d'ou `GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You")` et PAS
#    `GiveKeywordToAttached("You")`, qui servirait les deux faces ;
#  - `an007` Asgard's Assassin pour la ressource :
#    `CanGenerateResources(HeroResource, ...)` + `CostFunc.Exhaust("This")`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - `control_by="You"` n'est pas decoratif : « Hulk » est un nom TRES
#    partage (l'allie officiel 01050, le sbire th014, l'allie 62020, le heros
#    officiel 10001a). Passer par le TYPE de face plus le controle evite tout
#    ciblage d'homonyme, alors qu'un `CardFinder(name="Hulk")` nu servirait
#    aussi un allie du meme nom pose par un autre joueur.
#  - « Hero Resource » : la ressource ne peut PAS etre generee en forme
#    civile. C'est ce qui distingue cette carte de hk008 Unnatural Strength,
#    qui est une ressource de main.
#  - « Exhaust -> » : cout, donc une generation par round tant que
#    l'amelioration n'est pas redressee.
#  - ⚠ HOMONYME : `10007` Limitless Strength est une carte signature du HULK
#    OFFICIEL, et c'est une RESSOURCE la-bas, une amelioration ici. Deux
#    cartes distinctes de meme nom (voir le `collision_note` du deck).


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            attack=1,
        ),
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("R"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]

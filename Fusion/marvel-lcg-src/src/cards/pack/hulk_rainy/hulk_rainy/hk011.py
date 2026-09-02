from . import *

# Limitless Endurance — amelioration signature, x1 (n/15 = 14).
# CONDITION. GAMMA. SUPERPOWER. Cout 3, ressource [energy].
# You get +3 hit points and Bruce Banner gets +1 REC.
# Hero Action: Exhaust Limitless Endurance -> heal 1 damage from Hulk.
#
# Cartes de reference :
#  - `05023` Endurance, MEME phrase imprimee pour les PV :
#    `GiveKeywordToAttached("You", health=3)` ;
#  - `aa003` * Ebony et `al011` pour le +1 REC nomme :
#    `GiveKeywordToInPlayWhenApplyThis(CardFinder(name=..., card_type=
#    AlterEgo), control_by="You", recover=1)` ;
#  - `38007` Energy Transfer pour `HealthUnits`.
#
# ⚠ LES DEUX BONUS N'ONT PAS LA MEME PORTEE, ET C'EST IMPRIME (piege §3 de
# RECETTES-MOTEUR, trouve en partie reelle sur an002) :
#  - « YOU get +3 hit points » : « you », c'est l'identite, donc les DEUX
#    faces. PV 15 -> 18 en heros comme en civil ;
#  - « BRUCE BANNER gets +1 REC » : un nom PROPRE, celui de la seule face
#    CIVILE (la face heros s'appelle « Hulk »). REC 4 -> 5, et seulement la.
# Ecrire le second comme le premier donnerait un REC a la face heros, qui
# n'en a pas — silencieusement.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « heal 1 damage from HULK » : la face heros, pas un allie du meme nom,
#    d'ou `initiator.GetHero()` et non un selecteur de cible.
#  - « Hero Action » : injouable en forme civile, alors meme que le +1 REC
#    qu'elle donne ne sert QUE la-bas.
#  - « Exhaust -> » : cout, donc un soin par round.
#  - `card_type=AlterEgo` et `control_by="You"` : « Bruce Banner » est aussi
#    le nom de l'alter-ego OFFICIEL `10001b`. On vise notre face, pas un
#    homonyme.


def GetAbilities() -> Sequence['Ability']:

    def limitless_endurance(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        this.HealthUnits([initiator.GetHero()], 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Bruce Banner", card_type=AlterEgo),
            control_by="You",
            recover=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            limitless_endurance,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]

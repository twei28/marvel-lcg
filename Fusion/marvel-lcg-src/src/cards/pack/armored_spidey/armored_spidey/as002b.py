from . import *

# Spider Armor — FACE [[DESTROYED]] de l'amelioration PERMANENTE a deux faces.
# ARMOR. Classe Hero.
# Permanent.
# Armored Spidey gets -1 ATK and -1 DEF.
# Alter-Ego Action: Spend 3 resources of any type -> flip this card.
#
# Cartes de reference :
#  - **`34002b`** Phoenix Force (face UNLEASHED) : « Phoenix gets -2 THW and
#    +2 ATK », rendu par `GiveKeywordToAttached(CardFinder(name="Phoenix"),
#    thwart=-2, attack=+2)`. Meme montage, meme piege de nom propre.
#  - **`32179`** Ferocious Attack et `40122a` * Juggernaut's Helmet pour
#    `SetCost(Cost("3"))` : « Spend 3 resources of any type » sur une capacite
#    deja en jeu (`Cost("3", same_type=True)` serait « of the same type »).
#  - `40122a` pour `this.card.Flip(effect)` declenche par une Action.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Armored Spidey** gets -1 ATK and -1 DEF » : un NOM PROPRE, celui de
#    la seule face HEROS. L'alter-ego s'appelle Peter Parker et n'a ni ATQ ni
#    DEF. `CardFinder(name="Armored Spidey")` et surtout PAS `"You"`, qui
#    viserait les deux faces (piege an002, trouve en partie reelle le
#    1/9/2026).
#  - « Spend 3 resources of **any** type » : `Cost("3")` tout court. Le
#    `same_type=True` de Juggernaut rendrait « of the same type », ce qui
#    n'est pas ce qui est imprime.
#  - « **Alter-Ego** Action » : rien en forme heros, alors meme que c'est la
#    forme heros qui subit le malus. C'est le prix a payer, et c'est ce qui
#    rend `as003` Spider-Bot precieux : lui repare SANS changer de forme.
#  - « flip **this** card » : l'amelioration, pas l'identite.
#  - Cette face n'a AUCUN Forced Response de retournement : c'est as002a qui
#    porte « After you flip to this side, place 3 metal counters here », donc
#    le rechargement se fait automatiquement a l'arrivee sur l'autre face.
#  - « Permanent. » : base automatique lue dans `desc.Permanent`, aucun
#    script (fiche mots-cles/permanent.md).


def GetAbilities() -> Sequence['Ability']:

    def reparation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        this.card.Flip(effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Armored Spidey"),
            attack=-1,
            defense=-1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            reparation,
        ).SetCost(Cost("3")),
    ]

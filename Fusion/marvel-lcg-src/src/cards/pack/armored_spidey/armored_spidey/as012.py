from . import *

# Night Vision — amelioration signature, x1. ITEM. TECH. Cout 1,
# ressource [energy].
# While Spider Armor has the [[OPERATIONAL]] trait, Armored Spidey gets +1 THW
#   and he ignores guard and patrol keyword.
#
# Cartes de reference :
#  - **`50093`** Embassy Guard / `50094` Embassy Patrol (set Batroc) : le
#    montage « tant que TELLE carte recto-verso est sur TELLE face » se rend
#    par un `condition=` + `change_on_event=OnEvent.Trait(CardFinder(
#    name=...))`. Alert Level est exactement une carte a deux faces dont le
#    seul marqueur lisible est un trait, comme la Spider Armor.
#    Le helper `IfAlertLevelIsHighSide` du set Batroc est le jumeau de
#    `ArmureOperationnelle`.
#  - **`32002`** * Shadowcat: Kitty Pryde et `29034` * Wasp pour
#    `UnitIgnoreKeywordIcons(..., guard=True, patrol=True)`.
#  - `ok014` / `im007` pour `GiveKeywordToInPlayWhenApplyThis(..., thwart=1)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Armored Spidey** gets +1 THW » : un NOM PROPRE, celui de la seule
#    face HEROS. L'alter-ego s'appelle Peter Parker. `CardFinder(name=
#    "Armored Spidey")` et surtout PAS `"You"`, qui donnerait le bonus aussi
#    en forme civile (piege an002, trouve en partie reelle le 1/9/2026).
#    → un contre-cas en forme CIVILE est donc du.
#  - « **While** Spider Armor has the [[OPERATIONAL]] trait » : condition
#    CONTINUE, relue a chaque retournement de l'armure. Sans le
#    `change_on_event`, le bonus resterait fige a sa valeur du moment ou il a
#    ete calcule.
#  - « ignores **guard and patrol** keyword » : les deux, et RIEN d'autre.
#    Pas de `crisis=True`, alors meme que les trois vont ensemble sur
#    Shadowcat et sur Wasp. Ne pas copier le modele au-dela du texte.
#  - Guard et Patrol sont des bases automatiques du moteur (fiches
#    mots-cles/guard.md et patrol.md) : rien a recoder, seulement a IGNORER,
#    ce que fait `UnitIgnoreKeywordIcons` par
#    `effect.IsIgnoreKeyword('Guard'|'Patrol', effect)`.
#  - ⚠ `which_unit` VAUT `CardFinder(name="Armored Spidey")`, PAS `"You"`.
#    `"You"` est converti en `"This"` par le moteur (play.py:471) puis compare
#    a `effect.this` — qui est CETTE amelioration, jamais le heros qui attaque.
#    La comparaison echoue donc toujours pour une amelioration porteuse, et
#    l'exemption ne s'applique jamais. Mesure : le cas « le heros frappe le
#    vilain malgre un sbire GARDE » rendait 0 degat sur Rhino (03/09/2026).
#    Le montage `"You"` de `im013` ne marche que parce qu'il enregistre
#    l'abilite EN TEMPORAIRE depuis l'interruption, et son cas de test ne
#    verifie d'ailleurs pas l'exemption elle-meme.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Armored Spidey"),
            control_by="You",
            thwart=1,
            condition=ArmureOperationnelle,
            change_on_event=OnEvent.Trait(CardFinder(name=NOM_ARMURE)),
        ),
        AbilityFactory.UnitIgnoreKeywordIcons(
            CardFinder(name="Armored Spidey"),
            guard=True,
            patrol=True,
            conditions=[lambda effect, message: ArmureOperationnelle(effect)],
        ),
    ]

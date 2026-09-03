from . import *

# Swing It! — evenement signature, x2. THWART. Cout 2, ressource [physical].
# Hero Action (thwart): Remove 3 threat from a scheme. You may remove 1 metal
#   counter from Spider Armor to confuse an enemy.
#
# Cartes de reference :
#  - `ls004` / `an004` / `vp001a` pour `this.RemoveThreatFromSchemes(cibles,
#    3, effect)` et le libelle `('thwart')`.
#  - **`08013`** Stealth Strike pour le SECOND ciblage a l'interieur de
#    l'operation : `initiator.ChooseAbilities(effect,
#    ForChoiceAbility(...).SetTarget(...))`. C'est le montage impose quand
#    deux types de cibles differents cohabitent dans une meme carte.
#  - `im002` pour le « you may » paye en compteur (`MayChooseOneAbility`).
#  - `05015` / `01083` pour `Faces.GiveStatus(cibles, "Confused", effect)` et
#    le filtre `canbe_confused=True`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « confuse **an** enemy » : UN ennemi quelconque, DEUXIEME choix, sans
#    aucun lien avec le complot vise plus haut. C'est la difference exacte
#    avec as006 Kick It!, qui ecrit « that enemy » et reutilise la premiere
#    cible.
#  - « Remove 3 threat from **a scheme** » : un complot au choix, principal ou
#    annexe. `Scheme2` couvre les deux ; aucune mention de Crise, donc pas
#    d'`ignore_crisis`.
#  - « **You may** remove 1 metal counter » : facultatif, et la menee retiree
#    tombe de toute facon. Le retrait passe donc par `RetirerUnMetal`
#    (corps), pas par un `CostFunc` : la carte ne peut pas resoudre en ne
#    faisant rien.
#  - « **(thwart)** » : le libelle alimente Desoriente. Un seul `SetLabel`.


def GetAbilities() -> Sequence['Ability']:

    def swing_it(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        if CompteursMetal(effect) < 1:
            return

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        choix = initiator.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 1 metal counter to confuse an enemy",
                lambda targets:
                    Faces.GiveStatus(targets, "Confused", effect)
                    if RetirerUnMetal(effect) else None,
            ).SetTarget(Enemy, canbe_confused=True),
        )
        Unused(choix)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            swing_it,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]

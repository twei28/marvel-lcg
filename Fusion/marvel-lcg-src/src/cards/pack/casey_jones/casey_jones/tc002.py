from . import *

# Clap Back — EVENEMENT, cout 3, [mental]. THWART. x2.
# Hero Action (thwart): Remove 5 threat from a scheme. If a Casey Jones WEAPON
#   upgrade was discarded to pay for this card, confuse an enemy.
#
# CARTES DE REFERENCE
#  - `raphael/tr003` Disarm : `SetPlay().SetLabel('thwart').SetTarget(Scheme2)`
#    + `this.RemoveThreatFromSchemes(effect.targets, N, effect)`.
#  - `ma015` Break Through / `raphael/tr004` : second choix (un ENNEMI quelconque)
#    par `joueur.ChooseAbilities(effect, ForChoiceAbility(...).SetTarget(
#    Enemy, canbe_confused=True))`.
#  - la condition « discarded to pay for this card » : `tc001a` Overswing, qui
#    consigne l'arme defaussee sur l'effet de la carte payee
#    (`ConsignerArmeDefausseePourPayer`, `__init__.py` du set).
#
# TEXTE CONTRE CODE
#  ⚠ « Remove 5 threat from A scheme » : inconditionnel, AVANT le reste ; une
#    Crise bloque le complot principal (label `thwart`, `CanBeThwartBy`).
#  ⚠ « a CASEY JONES WEAPON upgrade » : arme du SET Casey Jones (voir Q1). Une
#    arme d'un autre heros defaussee par Overswing ne confond PAS.
#  ⚠ « discarded TO PAY FOR THIS CARD » : une arme defaussee a un autre moment
#    (Sac, Clap Back d'avant) ne compte pas : la marque vit sur l'effet de CETTE
#    carte seulement.
#  ⚠ « confuse AN enemy » : choix du joueur parmi les ennemis confondables
#    (vilain ou sbire) ; rien ne se passe sans cible (un Stalwart ne l'est pas).


def GetAbilities() -> Sequence['Ability']:

    def clap_back(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 5, effect)

        if not ArmeDeCaseyDefausseePourPayer(effect):
            return
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Clap Back: confuse an enemy",
                lambda cibles: Faces.GiveStatus(list(cibles), "Confused", effect),
            ).SetTarget(Enemy, canbe_confused=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            clap_back,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]

from . import *

# Energy Manipulation — Amelioration, cout 0, ressource [energy]. COSMIC. SUPERPOWER.
# Action: Spend X [energy] resources -> put X energy counters here.
# Hero Action: Discard Energy Manipulation -> draw 1 card (to a maximum of 5) for each energy counter here.
#
# Cartes de reference :
#  - `01018` Energy Channel (core) : MEME schema, « Spend X [energy] resources -> put X energy counters here »
#    avec `SetCost(Cost("Y"))` (cout variable) + `Faces.PlaceCountersOn(... 'energy')`, puis Hero Action
#    `CostFunc.Discard("This")` qui lit `this.GetCounters('energy')` apres la defausse.
#  - `06006` Lightning Strike : lecture du paiement variable.
#
# ⚠ Mots-pieges :
#  - « Action » nue (civile ET heroique) pour poser les compteurs ; « Hero Action » pour piocher.
#  - « (to a maximum of 5) » : plafond sur le NOMBRE de cartes piochees, pas sur les compteurs.
#  - le compteur `energy` existe deja dans l'enum COUNTER.
#  - « Discard Energy Manipulation -> » : la defausse est un COUT, la carte part meme si 0 compteur.


def GetAbilities() -> Sequence['Ability']:

    def poser_les_compteurs(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        valeur = effect.GetPaidResources().GetColor("Y")
        Faces.PlaceCountersOn([this], valeur, 'energy', effect)

    def piocher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        nombre = min(this.GetCounters('energy'), 5)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None and nombre > 0:
            joueur.DrawUp(nombre, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            poser_les_compteurs,
        ).SetCost(Cost("Y")),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            piocher,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]

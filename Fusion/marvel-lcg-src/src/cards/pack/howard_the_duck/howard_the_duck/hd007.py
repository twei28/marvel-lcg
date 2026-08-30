from . import *

# Fowl Play (1/2) — THWART — evenement, cout 2
# Hero Action (thwart): Remove 3 threat from a scheme. If you defeat a side
#   scheme in this way, you may ready your hero or remove 1 threat from a
#   scheme for each side scheme in the victory display.
#
# Exemplaire physique 1 de 2 (hd007 RES mental, hd008 RES physique : meme
# texte, deux card_id distincts — modele ok004/ok005).
#
# « If you defeat a side scheme IN THIS WAY » : crochet dedie du moteur,
# `RemoveThreatFromSchemes(..., if_this_remove_last_threat=<fn>)` — modele
# exact cw/tigra/56009.py (Feline Senses) et ironheart/29005.py (Fly Over),
# les deux memes « retire N, et si la derniere menace part, bonus ». La
# restriction « SIDE scheme » (pas le complot principal) est verifiee a la
# main sur la cible : le crochet ne filtre pas le type de manigance.
#
# « you may ready your hero OR remove ... » : choix OPTIONNEL a 2 branches ->
# `initiator.MayChooseOneAbility` (player_action.py:230, qui ajoute une option
# « Cancel »), la ou une obligation forcee utiliserait `ChooseAbilities`
# (ok019). « ready your HERO » = l'identite en forme heros
# (`initiator.GetHero()`, modele ok014 Royal Protector), pas la carte jouee.
# Le montant du second choix compte TOUTES les manigances annexes en zone de
# victoire, celles du vilain comprises (portee large, voir le __init__.py du
# set) -> `NombreDeManigancesEnVictoire`.


def GetAbilities() -> Sequence['Ability']:

    def fowl_play(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        cibles = list(effect.targets)
        vise_une_manigance_annexe = any(SchemeSide2.IsType(c) for c in cibles)

        def bonus() -> None:
            if not vise_une_manigance_annexe:
                return

            def redresser(targets: Sequence['CardFace']) -> None:
                Unused(targets)
                Faces.ReadyAll([initiator.GetHero()], effect)

            def nettoyer(targets: Sequence['CardFace']) -> None:
                valeur = NombreDeManigancesEnVictoire(effect)
                if targets and valeur > 0:
                    this.RemoveThreatFromSchemes(targets, valeur, effect)

            initiator.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Ready your hero",
                    redresser,
                ),
                AbilityFactory.ForChoiceAbility(
                    "Remove 1 threat from a scheme for each side scheme in the victory display",
                    nettoyer,
                ).SetLabel('thwart').SetTarget(Scheme2),
            )

        this.RemoveThreatFromSchemes(cibles, 3, effect, if_this_remove_last_threat=bonus)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            fowl_play,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]

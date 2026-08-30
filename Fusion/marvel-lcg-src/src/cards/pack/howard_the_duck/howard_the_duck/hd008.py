from . import *

# Fowl Play (2/2)
# Exemplaire physique 2 de 2 (RES physique), contenu identique a hd007 (voir
# ce fichier pour le detail du modele repris).


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

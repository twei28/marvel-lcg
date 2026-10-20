from . import *

# Threat on the Horizon — TRAITRISE (Earth Under Siege), x2 exemplaires.
# When Revealed: Choose to either spend 2 resources of any type or remove 1 safety counter from the main
#   scheme.
#
# Cartes de reference :
#  - « Choose to either A or B » : `joueur.ChooseAbilities(effect, *options)` (modele gs240q Distant
#    Manipulation / OFFICIEL hs052 Restraining Pincers), options construites SEULEMENT si realisables.
#  - « spend 2 resources of any type » : `joueur.AskSpendResources(Cost("2"), effect)` (modele gs089
#    Caught in Its Sights) ; offerte seulement si couvrable (modele `PeutDepenserDeuxRessources`, kree_sentry).
#  - « remove 1 safety counter from the main scheme » : `Faces.RemoveCountersOn` (modele gs161b), offerte
#    seulement si Earthfall porte au moins 1 jeton.
#
# ⚠ Mots-pieges : AUCUNE clause « If you cannot, gains surge » imprimee sur cette carte (contrairement a
# gs240q/hs052) : si aucune des deux options n'est realisable, rien ne se passe, pas de Renfort ; « the
# main scheme » = la manigance principale UNIQUE de ce scenario (Earthfall), trouvee par
# `Worlds.FindMainScheme`.


def GetAbilities() -> Sequence['Ability']:

    def peut_depenser_deux(joueur: 'Player') -> bool:
        faces = list(joueur.hand_cards.Get()) + list(joueur.reserve.Get())
        return FacesCounter.GetPrintedResources(faces).val >= 2

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        complot = Worlds.FindMainScheme(effect)

        options = []
        if peut_depenser_deux(joueur):
            options.append(AbilityFactory.ForChoiceAbility(
                "Spend 2 resources of any type",
                lambda cibles: joueur.AskSpendResources(Cost("2"), effect),
            ))
        if complot is not None and complot.GetCounters('safety') > 0:
            options.append(AbilityFactory.ForChoiceAbility(
                "Remove 1 safety counter from the main scheme",
                lambda cibles: Faces.RemoveCountersOn([complot], 1, 'safety', effect),
            ))
        if options:
            joueur.ChooseAbilities(effect, *options)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]

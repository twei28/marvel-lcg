from . import *

# Love Song
# SONG.
# Hero Action: Choose:
#   - Remove 1+X threat from the main scheme.
#   - Heal 1+X damage from a friendly character.
#   Where X is the number of enemies in play with a status card on them.
#
# X se calcule au moment de la resolution, pas au moment du choix : on le lit
# donc dans chaque branche.
#
# « the MAIN scheme » : pas de selection, la machination principale.
#
# CORRECTIF DU 20/10/2026 (backlog 12) : « Choose: » est un choix OBLIGATOIRE
# (`ChooseAbilities`, sans option Cancel). Le module passait par
# `MayChooseOneAbility`, qui offrait « Cancel » : la carte pouvait etre jouee
# pour rien.
# « a FRIENDLY character » : `Friend` (tout personnage du cote des joueurs),
# au lieu de « YouControlUnit » qui excluait les personnages des autres joueurs.


def GetAbilities() -> Sequence['Ability']:

    def compter_statuts(effect: 'Effect') -> int:
        total = 0
        for ennemi in Worlds.FindCardsOnField(effect, card_type=Enemy):
            if ennemi.HasStatus("Any"):
                total += 1
        return total

    def chanson_d_amour(effect: 'Effect',
                        message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def menace(targets: Sequence['CardFace']) -> None:
            principales = Worlds.GetAllMainSchemes(effect)
            if principales:
                this.RemoveThreatFromSchemes(
                    [principales[0]], 1 + compter_statuts(effect), effect)

        def soigner(targets: Sequence['CardFace']) -> None:
            this.HealthUnits(targets, 1 + compter_statuts(effect), effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Remove threat from the main scheme",
                                            menace),
            AbilityFactory.ForChoiceAbility("Heal a friendly character", soigner)
            .SetTarget(Friend, canbe_heal=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chanson_d_amour,
        ).SetPlay().SetLabel(),
    ]

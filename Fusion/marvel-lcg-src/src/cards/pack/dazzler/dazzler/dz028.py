from . import *

# "Doom and Gloom"
# SONG.
# Hero Action: Choose:
#   - Ready a friendly character.
#   - Remove a status card from up to 2 friendly characters.
#
# Carte BASIQUE : trait [[SONG]], donc rattrapee par la Setlist, mais pas de
# « Showtime! ».
#
# « UP TO 2 » : la fourchette part de zero, d'ou `range=(1, 2)` avec un
# minimum a 1 puisque choisir cette option implique d'en viser au moins un.
#
# CORRECTIF DU 20/10/2026 (backlog 12) : « Choose: » est un choix OBLIGATOIRE
# (`ChooseAbilities`, sans option Cancel). Le module passait par
# `MayChooseOneAbility`, qui offrait « Cancel » : la carte pouvait etre jouee
# pour rien.
# « a FRIENDLY character » : `Friend` (tout personnage du cote des joueurs),
# au lieu de « YouControlUnit » qui excluait les personnages des autres joueurs.


def GetAbilities() -> Sequence['Ability']:

    def morose(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def redresser(targets: Sequence['CardFace']) -> None:
            Faces.ReadyAll(targets, effect)

        def nettoyer(targets: Sequence['CardFace']) -> None:
            for cible in targets:
                RetirerUnStatut(cible, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Ready a friendly character",
                                            redresser)
            .SetTarget(Friend, canbe_ready=True),
            AbilityFactory.ForChoiceAbility("Remove a status card", nettoyer)
            .SetTarget(Friend, has_status="Any", range=(1, 2)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            morose,
        ).SetPlay().SetLabel(),
    ]

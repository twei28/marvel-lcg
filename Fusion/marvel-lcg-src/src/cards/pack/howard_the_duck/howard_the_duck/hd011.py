from . import *

# In a World — manigance annexe JOUEUR, cout 1, menace de depart 3*, Victory 0
# Victory 0.
# While In a World is in the victory display, Howard the Duck gets +1 DEF.
# When Defeated: Give each player a tough status card. The player who defeated
#   this scheme, may heal 2 damage from their identity.
#
# Meme montage que hd010 (Trapped) : `BonusDepuisLaZoneDeVictoire` pour le
# bonus permanent (modele 40006 Technovirus Purge) et
# `WhenSchemeBeDefeated(..., has_defeating_player=True)` pour le When
# Defeated (modele jubilee/47003.py Shopping Spree).
#
# « Give EACH PLAYER a tough status card » : le statut Tenace se pose sur
# l'IDENTITE du joueur (`player.GetIdentity()`), seule carte qui puisse le
# porter — modele trors/04017.py (Ready for Action) et ok006, tous deux via
# `Faces.GiveStatus(<faces>, "Tough", effect)`. Boucle sur les joueurs :
# `Players.ForEachPlayer`.
# « THE PLAYER WHO DEFEATED this scheme, MAY heal 2 » : portee restreinte au
# seul vainqueur, et optionnelle (`MayChooseOneAbility`). Le soin passe par
# `this.HealthUnits([identite], 2, effect)` (modele il002 Stature).


def GetAbilities() -> Sequence['Ability']:

    def in_a_world_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)

        def donner_tenace(player: 'Player') -> None:
            Faces.GiveStatus([player.GetIdentity()], "Tough", effect)

        Players.ForEachPlayer(effect, donner_tenace)

        vainqueur = message.GetDefeatingPlayer()
        vainqueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Heal 2 damage from your identity",
                lambda targets: this.HealthUnits([vainqueur.GetIdentity()], 2, effect),
            ),
        )

    return [
        *BonusDepuisLaZoneDeVictoire(defense=1),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            in_a_world_defeated,
            has_defeating_player=True,
        ),
    ]

from . import *

# Trapped — manigance annexe JOUEUR, cout 1, menace de depart 3*, Victory 0
# Victory 0.
# While Trapped is in the victory display, Howard the Duck gets +1 ATK.
# When Defeated: Each player may search their deck and discard pile for an
#   ally and add it to their hand. The player who defeated this scheme, may
#   put that ally into play.
#
# « Victory 0 » est lu par le moteur dans `desc.Victory` (has_victory.py:25 :
# la carte part d'elle-meme en zone de victoire a sa defaite) : aucun code.
#
# Bonus permanent depuis la zone de victoire : modele exact
# next_evol/cable/40006.py (Technovirus Purge), via l'aide
# `BonusDepuisLaZoneDeVictoire` du set (`works_in_the_victory_display=True`,
# garde-fou dans environment_helper.py:85).
#
# When Defeated : modele exact jubilee/47003.py (Shopping Spree), meme
# `AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", ...,
# has_defeating_player=True)` + `Search.PlayerCard`. Deux portees distinctes
# et volontairement differentes dans le texte imprime :
#   - « EACH PLAYER may search ... and add it to their HAND » : boucle
#     `Players.ForEachPlayer` (modele next_evol/cable/40002.py Bodyslide),
#     recherche OPTIONNELLE (`may=True`) puis `GainCard`.
#   - « THE PLAYER WHO DEFEATED this scheme, may put THAT ally into play » :
#     seulement `message.GetDefeatingPlayer()`, et « that ally » est bien LA
#     MEME carte que celle qu'il vient d'ajouter en main (piege `that <nom>`
#     du tableau) — on conserve la face trouvee pour ce joueur-la.


def GetAbilities() -> Sequence['Ability']:

    def trapped_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)

        vainqueur = message.GetDefeatingPlayer()
        trouvees: Dict[Any, Any] = {}

        def chercher(player: 'Player') -> None:
            face = Search.PlayerCard(
                effect,
                player,
                include_player_deck=True,
                include_discard_pile=True,
                may=True,
                card_type=Ally,
            )
            if face:
                player.GainCard(face, effect)
                trouvees[player] = face

        Players.ForEachPlayer(effect, chercher)

        allie = trouvees.get(vainqueur)
        if allie is None:
            return

        vainqueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Put that ally into play",
                lambda targets: allie.PutIntoPlay(vainqueur, effect),
            ),
        )

    return [
        *BonusDepuisLaZoneDeVictoire(attack=1),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            trapped_defeated,
            has_defeating_player=True,
        ),
    ]

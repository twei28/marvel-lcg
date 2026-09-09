from . import *

# Containment Breach — COMPLOT ANNEXE (nemesis). Boost 3. Amplify 1.
# Menace de depart 1 par joueur.
# When Revealed: Each player discards the top 4 cards of their deck and places
#   threat here equal to the number of [energy] resources discarded this way.
#
# CARTES DE REFERENCE
#  - `an011`, `ho014` : « When Revealed » sur un complot annexe =
#    `WhenThisRevealed(None, op)`.
#  - `bc010` / `sn003` : compter les RESSOURCES IMPRIMEES d'un paquet de
#    cartes se fait par `FacesCounter.GetPrintedResources([...])`, jamais en
#    relisant `desc` a la main. Ici par l'helper commun du set,
#    `IconesEnergie`, qui porte le `convert_green_res=False` — sans lui une
#    ressource wild compterait comme une energie.
#  - `50134`, `ho015` : `this.PlaceThreatOnSchemes(cibles, n, effect)`.
#  - `Player.DiscardDeckTopCards(n, effect)` (`player_action.py:1009`), qui
#    rend la liste des cartes reellement defaussees.
#
# TEXTE CONTRE CODE
#  ⚠ « EACH PLAYER discards » : tous les joueurs, pas seulement celui qui
#    revele. En solo la difference ne se voit pas — c'est exactement le genre
#    d'ecart que seule une position a deux joueurs montre (`heros2` dans le
#    harnais).
#  ⚠ « places threat HERE » : sur CE complot annexe, pas sur le principal.
#  ⚠ « equal to the number of [energy] resources DISCARDED THIS WAY » : on
#    compte les icones ENERGIE sur les cartes que CETTE capacite a defaussees,
#    toutes zones et tous joueurs confondus, et une carte a deux icones
#    energie en vaut DEUX. `GetPrintedResources` compte les icones, pas les
#    cartes.
#    ⚠ Et c'est bien la ressource IMPRIMEE : une carte dont la ressource
#    serait modifiee en jeu n'a de toute facon pas d'existence dans un deck.
#  ⚠ Un deck de moins de 4 cartes ne bloque rien : `DiscardDeckTopCards` rend
#    ce qu'il a pu defausser, et le compte porte sur ce qui est sorti.
#  ⚠ `Amplify 1` et `Boost 3` sont des BASES AUTOMATIQUES lues dans `desc`
#    (RECETTES §3) : aucun script. L'icone Amplify a ete identifiee par
#    comparaison d'image contre `16069` Spatial Positioning le 08/09/2026 —
#    jamais a vue (lecon Lockjaw).
#  ⚠ La menace de depart « 1 [per_hero] » s'ecrit `StartingThreat: "1*"` dans
#    `desc` (modele `bl012`), et non dans le script.
#  ⚠ Aucune limite imprimee : etape 7 bis sans objet.


def GetAbilities() -> Sequence['Ability']:

    def breche(effect: 'Effect', message: 'Message.WhenThisRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)

        defaussees: List['CardFace'] = []

        def defausser(joueur: 'Player') -> None:
            defaussees.extend(joueur.DiscardDeckTopCards(4, effect))

        # ⚠ `World()` N'EST PAS dans le namespace d'un pack : un `World().
        # GetPlayers(effect)` leve `NameError` que le moteur AVALE, et la carte
        # ne fait plus rien — verte a la construction, muette en partie. Le bon
        # chemin pour « each player » est `Players.ForEachPlayer` (modele
        # `16026` Blazing Inferno). Paye ici le 08/09/2026 : ni
        # `verifier_appels_modules` ni `verifier_noms_modules` ne l'ont vu, seul
        # le cas de test l'a montre.
        Players.ForEachPlayer(effect, defausser)

        if not defaussees:
            return

        energie = IconesEnergie(defaussees)
        if energie > 0:
            this.PlaceThreatOnSchemes([this], energie, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            breche,
        ),
    ]

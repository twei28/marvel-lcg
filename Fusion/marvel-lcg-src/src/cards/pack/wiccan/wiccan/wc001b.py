from . import *

# * Billy Kaplan (face alter-ego) — custom « CptScorp »
# Clairvoyance — During the player phase, play with the top card of the
#   encounter deck face up.
# Action: Look at the top 2 cards of the encounter deck, you may discard one
#   of them. (Limit once per round.)
#
# Clairvoyance -> meme fabrique et meme modele que wc001a (Falcon 53001a) :
# la capacite est imprimee sur LES DEUX faces, elle est donc dupliquee, pas
# heritee. Sans elle sur cette face, retourner en identite civile eteindrait
# la carte visible, ce que le texte ne dit pas.
#
# « Action: » nu (et non « Alter-Ego Action: ») sur une FACE alter-ego ->
# `AbilityType.Action` + `.LimitOncePerRound()`, comme Bruce Banner (10001b),
# Tony Stark (01029b), Sharon Carter (ag001b) et Remy LeBeau (37001b).
# `AlterEgoAction` designe un autre type d'abilite, reserve aux cartes JOUEUR
# qui doivent declarer ce mode puisqu'elles ne sont pas elles-memes la face
# alter-ego.
#
# « Look at the top 2 cards, you may discard one of them » -> le couple
# `player.LookAtDeck("EncounterDeck", 2, effect)` puis `player.AskDiscardFaces
# (faces, (0, 1), effect, not_shuffle=True)`. Modele de la mecanique :
# Remy LeBeau (37001b), qui fait exactement « look at the top 2 cards of the
# encounter deck, discard 1 of those cards » via `CostFunc.LookAtDeck(
# "EncounterDeck", 2, discard=1)`. Cette fabrique-la n'est PAS reutilisable
# telle quelle ici : elle impose une defausse de (1, 1), donc FORCEE, alors
# que Billy Kaplan imprime « you MAY discard one of them ». La plage (0, 1)
# rend l'optionnalite, exactement comme le fait `Faces`/`AskDiscardFaces`
# ailleurs. Le pilote de test choisit le minimum par defaut : le cas dedie
# emploie `accepter_choix: True` pour exercer vraiment la defausse.
#
# Cas limite : deck de rencontre vide -> `faces` vide, aucune question posee,
# aucune erreur.

def GetAbilities() -> Sequence['Ability']:

    def regarder_le_dessus(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        faces = joueur.LookAtDeck("EncounterDeck", 2, effect)
        if not faces:
            return

        joueur.AskDiscardFaces(faces, (0, 1), effect, not_shuffle=True)

    return [
        *AbilityFactory.PlayWithTopCardOfDeckFaceup(
            lambda effect:
                Worlds.GetEncounterDecks(effect),
            only_during_player_phase=True,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            regarder_le_dessus,
        ).LimitOncePerRound(),
    ]

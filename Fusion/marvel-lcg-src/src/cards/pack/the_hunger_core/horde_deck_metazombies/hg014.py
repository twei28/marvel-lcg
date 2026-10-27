from . import *

# Zombie Doctor Strange — METAZOMBIE (Horde deck). MYSTIC. SCH 2. ATK 1. PV 10[per_hero].
# Hex — Forced Response: After Zombie Doctor Strange activates against you, deal yourself 1 facedown
# encounter card.
#
# Cartes de reference :
#  - « After Zombie Doctor Strange ACTIVATES against you » : `AbilityFactory.AfterEnemyActivatesAgainstYou(
#    ForcedResponse, "This", op)` (activate.py:93), MEME fabrique que `hg012` Zombie Thor (« activates against
#    a player ») : le moteur resout « against you » et « against a player » de la meme facon, via
#    `message.GetAgainstPlayer()` (sender_enemy.py:186), qui rend le joueur REELLEMENT vise par CETTE
#    activation precise -- la difference de pronom dans le texte imprime (« you » gineriquement adresse a la
#    table, vs « a player » sur Thor) ne change rien au code, deja documente sur hg012.
#  - « deal yourself 1 facedown encounter card » : `joueur.DealEncounterCards(1, effect)` (player_action.py:471),
#    modele `sk065` Untrustworthiness (« deal yourself 1 facedown encounter card » -> meme appel, meme sens de
#    « yourself » = le joueur VISE par le declencheur, pas un joueur fixe par le code) et brique maison
#    `Just a Core X` (`hg001`-`hg003`, fiche mots-cles/just-a-core-x.md) qui pose le MEME appel pour un texte
#    proche (« deals themself X facedown encounter cards »). Le joueur qui recoit la carte est celui resolu
#    par `message.GetAgainstPlayer()`, pas `Worlds.GetFirstPlayer()` ni un joueur en dur -- important en
#    multijoueur.
#
# ⚠ Mots-pieges :
#  - « Hex » est un NOM D'AMBIANCE propre a cette carte, pas un mot-cle officiel ni une mecanique a coder --
#    MEME statut, DEJA ARBITRE par l'utilisateur le 27/10/2026, que « Storm » (hg012), « Devour » (hg009),
#    « Web » (hg010), « Absorption » (hg011) et « Ambush » (hg013) : aucune fiche `mots-cles/hex.md` a creer,
#    rien a ouvrir avant de coder, seule la phrase qui suit (« Forced Response: ... ») porte une regle. Ce
#    n'est donc PAS un cas ambigu nouveau : c'est le 6e exemplaire identique d'un motif deja tranche 5 fois
#    dans ce meme pack, pas de "A CONFIRMER" ici.
#  - « ACTIVATES », pas « attacks » : couvre AUSSI la manigance (forme alter-ego), exactement comme `hg012`
#    (meme commentaire deja laisse sur nt013/27158/hg012) -- `AfterEnemyActivatesAgainstYou`, jamais
#    `AfterUnitAttackUnit` seul, sous peine de rater la moitie des declenchements.
#  - « against YOU » : contrairement a `Just a Core X` (hg001-hg003, qui REMPLACE l'attaque par la
#    distribution), Zombie Doctor Strange N'A AUCUNE clause « instead of » -- son attaque (ou sa manigance)
#    se resout NORMALEMENT, et la carte de rencontre est distribuee EN PLUS, pas a la place. Aucune
#    `SetBeInstead` ici, a la difference de `hg001`/`hg002`/`hg003`.
#  - « deal YOURSELF » : le joueur qui recoit la carte est la VICTIME de l'activation (`GetAgainstPlayer()`),
#    jamais Zombie Doctor Strange ni `effect.this` -- la carte n'a pas de case "joueur" a elle, c'est un
#    Villain comme les autres Metazombies.
#  - « 1 facedown encounter card », SANS condition sur le nombre de joueurs ni sur le mode de jeu : un seul
#    appel `DealEncounterCards(1, effect)`, pas un par joueur (contrairement a `hg002`/`hg003` « each player »,
#    qui n'est pas le texte imprime ici -- seul LE joueur vise par l'activation est concerne).


def GetAbilities() -> Sequence['Ability']:

    def hex_(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        joueur = message.GetAgainstPlayer()
        joueur.DealEncounterCards(1, effect)

    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            "This",
            hex_,
        ),
    ]

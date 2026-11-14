from . import *

# * Silver Surfer (face ALTER-EGO) — POWER COSMIC. COSMIC. AERIAL. HP 12,
# REC 3, main 6.
#
# Texte imprime :
#  « Characters at a PLANET cannot attack or scheme and lose guard and
#    patrol. » — IDENTIQUE a la face Heros (pc001a), voir pc001a.py pour le
#    texte contre code complet (partage via `AbilitésBlocagePlanet`).
#  « Action: Exhaust Cosmic Surfboard → put the top card of the planet deck
#    into play. (Limit once per phase.) »
#
# Regle de l'auteur (hors carte, QUESTIONS-AUTEUR.md) : « During setup, start
# with Zenn-La and your Cosmic Surfboard in play. Shuffle the planet deck and
# set it aside facedown. » Pas de texte imprime pour cette phrase : elle vit
# ici, sur l'Alter-Ego (modele bt001b/al001b, PROCESSUS-HEROS etape 3).
#
# CARTES DE REFERENCE
#  - `CostFunc.Exhaust(name="Cosmic Surfboard")` (cost_func.py:261) : incliner
#    une carte NOMMEE plutot que « This » — cible la carte pc002 par son nom
#    imprime, pas la carte qui porte l'action.
#  - `SetupPutIntoPlay`/`face.PutIntoPlay(joueur, effect, under_control=True)`
#    (factory/setup.py) : mettre une carte en jeu sous le controle du joueur.
#  - helper `PlanetDeck(joueur)` (__init__.py du pack) : deck personnel
#    mele/mis de cote au Setup, modele `HordeDeck` (the_hunger_core).
#  - `as001b`/`cd001b` : `AbilityFactory.SetupPutIntoPlay([...], operation=...)`,
#    modele retenu pour Zenn-La — PAS son propre `desc.Setup` (carte pc003) :
#    Zenn-La ne vit jamais dans `player.player_deck` (contrairement a Cosmic
#    Surfboard, carte du deck de heros, donc deja melee au deck du joueur au
#    moment ou le moteur scanne les cartes Setup, `world.py:596-607`), donc le
#    scan natif ne la trouverait jamais — elle doit etre posee EXPLICITEMENT.
#
# CORRIGE (05/11/2026, matin) : les 4 cartes existent desormais (pc005
# Sakaar, pc006 Newhaven, pc007 Xandar, pc017 Ego) -- `construire_le_planet_
# deck` les fabrique et les mele dans `PlanetDeck(joueur)` au Setup, modele
# `ConstruireLeHordeDeck` (the_hunger_core/commun.py :
# `CardFactory.GenerateCard` + `deck.Shuffle`). Avant ce correctif, le deck
# restait TOUJOURS VIDE (`PlanetDeck(joueur)` ne fait QUE creer un `Deck2`
# vide, rien ne le remplissait jamais) : l'Action « put the top card of the
# planet deck into play » ne faisait donc jamais rien en vraie partie,
# invisible aux cas de test qui posent Sakaar/Newhaven/Xandar directement
# via `Puzzle.PutIntoPlay` (contournant le deck entierement).
#
# TEXTE CONTRE CODE
#  « the top card » : UNE seule carte, `PlanetDeck(joueur).GetTop()`.
#  « (Limit once per phase.) » : `.LimitOncePerPhase()` — le texte imprime ne
#    dit pas « per player », donc pas `LimitOncePerPhasePerPlayer`.
#  « Exhaust Cosmic Surfboard » : si Cosmic Surfboard n'est pas en jeu (pas
#    encore posee, ou retiree), le cout echoue et l'action n'est pas
#    proposee — comportement natif de `CostFunc.Exhaust`, rien a coder.


def GetAbilities() -> Sequence['Ability']:

    def jouer_planete(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        carte = PlanetDeck(joueur).GetTop()
        if carte is None:
            return
        carte.PutIntoPlay(joueur, effect, under_control=True)

    def construire_le_planet_deck(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        from game.card.factory import CardFactory
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        deck = PlanetDeck(joueur)
        for card_id in ("pc005", "pc006", "pc007", "pc017"):
            CardFactory.GenerateCard(card_id, deck, effect.world)
        deck.Shuffle(effect)

    return AbilitésBlocagePlanet() + [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            jouer_planete,
        ).SetCostFunc(CostFunc.Exhaust(name="Cosmic Surfboard"))
        .LimitOncePerPhase()
        .SetName("Jouer une planète"),
        AbilityFactory.SetupPutIntoPlay(["pc003"]),
        AbilityFactory.WhenCardSetup("This", construire_le_planet_deck),
    ]

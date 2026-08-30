from . import *

# * Howard Duckson (face alter-ego) — DUCK. GENIUS
# Deducktive Reasoning — Action: Look at the top 3 cards of the encounter
#   deck. Put 1 on the bottom of the deck and the others back in any order.
#   (Limit once per round.)
#
# Modele exact : next_evol/cable/40004.py (Precognition), meme triplet
# `initiator.LookAtDeck("EncounterDeck", n, effect)` +
# `initiator.MayChooseFace(faces, effect, not_move=True)` +
# `initiator.PlaceOnTopInAnyOrder(reste, effect)`. Seule difference imprimee :
# Precognition DEFAUSSE la carte choisie, Howard la met SOUS le deck ->
# `Faces.MoveAllToDeck([choisie], deck, "Bottom", effect)` (modele
# msm/ms_marvel/05006.py et sm/mysterio/__init__.py, les deux seuls usages du
# mode "Bottom" du depot).
#
# Le nombre regarde est FIXE (3), contrairement a Precognition dont le nombre
# depend de la zone de victoire.
#
# MISE EN PLACE DU PACK : c'est l'IDENTITE qui met en jeu hd017 (Nexus of all
# Realities, Setup. Permanent.), via `AbilityFactory.SetupPutIntoPlay
# (["hd017"])` (setup.py:6-31, qui genere la carte depuis son card_id sans
# qu'elle ait besoin d'etre dans un deck). C'est la voie idiomatique du depot,
# partagee par les 20 heros a `set_aside` non vide : Wolverine (35001b ->
# "35002"), Vision (26001b -> "26002a,26002b"), Spider-Man Rainy (sr001b ->
# "sr012"), Storm, Doctor Strange... La cle `set_aside` d'un deck de depart est
# PUREMENT DOCUMENTAIRE : `SceneLoader.NewScene` ne la lit pas (loader.py:98-108
# ne construit le HeroDescriptor qu'avec hero / hero_deck / obligations /
# nemesis_set / player_deck), seul le chemin « puzzle » s'en sert
# (server_new_game.py:109/122). Sans cette ability, hd017 n'entrerait JAMAIS en
# jeu, en silence — c'est exactement ce que le cas test_capacites de hd017 a
# revele le 30/08/2026.


def GetAbilities() -> Sequence['Ability']:

    def deducktive_reasoning(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        faces = initiator.LookAtDeck("EncounterDeck", 3, effect)
        if not faces:
            return

        choisie = initiator.MayChooseFace(faces, effect, not_move=True)
        if choisie is not None:
            faces = [f for f in faces if f is not choisie]
            Faces.MoveAllToDeck([choisie], Worlds.GetEncounterDeck(effect), "Bottom", effect)

        if faces:
            initiator.PlaceOnTopInAnyOrder(faces, effect)

    return [
        AbilityFactory.SetupPutIntoPlay(
            ["hd017"],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            deducktive_reasoning,
        ).SetName("Deducktive Reasoning")
        .LimitOncePerRound(),
    ]

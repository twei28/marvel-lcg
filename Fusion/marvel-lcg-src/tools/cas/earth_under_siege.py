# Cas test_capacites du scenario 4 EARTH UNDER SIEGE de Galactic Storm (gs161-gs194), lot GS-7
# (20/10/2026). Noms prefixes `[eus]` (filtre : `[eus]`).
#
# Ce premier lot de cas couvre le SOCLE NEUF du scenario : la brique "plusieurs mechants en jeu"
# (src/game/operate/villains.py, jamais cablee avant ce lot), Earthfall (gs161a/b) et Enemies at Large
# (gs162a/b). Les cartes des 6 mechants eux-memes (stades + ensembles) ont chacune leur propre gabarit et
# leurs propres cas, a venir carte par carte.
#
# [eus-setup] utilise la VRAIE mise en place du scenario ("scenario": SC) : le mechant revele est
# ALEATOIRE (BuildVillainDeck melange), donc ces cas ne verifient que des MESURES INDEPENDANTES DE L'IDENTITE
# du mechant (nombre en jeu, taille du deck de mechants, compteurs de securite, presence d'Enemies at
# Large). [eus-mec] monte sa propre position DETERMINISTE (scenario "rhino", villains construits a la main
# via Puzzle.BuildVillainDeck) pour les cas qui ont besoin de savoir EXACTEMENT quel mechant est en jeu.

SC = "gs_earth_under_siege"

MEC_SOCLE = [
    "Puzzle.RemoveVillain('01094')",  # le Rhino du scenario "rhino" n'est pas un mechant du lot : l'otter
    "Puzzle.PutIntoPlay('gs161b')",
    "Puzzle.PlaceCounters('gs161b', 'safety', 6)",
    "Puzzle.SetVillainRule('Leftmost', 'PlayerChooses')",
]


def _c(nom, pourquoi, scenario, mise, declencher, attendu, **cle):
    cas = {"nom": "[eus] " + nom, "pourquoi": pourquoi, "scenario": scenario,
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "briques_le_mechant"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    # ============================================================== gs161a : mise en place reelle
    _c("gs161a mise en place : 1 mechant en jeu (le plus a gauche), 5 dans le deck de mechants, "
       "Enemies at Large en jeu, 6 compteurs de securite sur Earthfall",
       "« Create the villain deck ... Reveal the top card ... Reveal the Enemies at Large side scheme. "
       "Place 6 safety counters here. » : Villains.BuildVillainDeck + RevealNextVillain + "
       "SetupCards.PutIntoPlay + Faces.PlaceCountersOn (gs161a)",
       SC, [], [],
       {"tous": 1, "deck_de_mechants": 5}),
    _c("gs161a mise en place : Enemies at Large (standard, gs162a) est en jeu",
       "« Reveal the Enemies at Large side scheme » : SetupCards.PutIntoPlay(name=\"Enemies at Large\")",
       SC, [], [],
       {"en_jeu": ["gs162a"]}, verifier="etat_attendu"),
    _c("gs161a mise en place : Earthfall porte 6 compteurs de securite",
       "« Place 6 safety counters here » : Faces.PlaceCountersOn([this], 6, 'safety', effect)",
       SC, [], [],
       {"compteurs": [["gs161b", "safety", 6]]}, verifier="etat_attendu"),

    # ============================================================== gs161b : tic de securite
    _c("gs161b apres la phase du mechant : securite 6 -> 5, PAS de second mechant revele (5 n'est pas < 5)",
       "« remove 1 safety counter... If there are less safety counters here than the number of cards in "
       "the villain deck, reveal... » : 5 compteurs restants, 5 cartes au deck de mechants (apres la "
       "revelation initiale) -> comparaison stricte, aucune revelation",
       SC, [], ["Puzzle.EndVillainPhase()"],
       {"tous": 1, "deck_de_mechants": 5, "compteurs": [["gs161b", "safety", 5]]}),
    _c("gs161b 2e tic : securite 5 -> 4, 4 < 5 (deck de mechants) -> un 2e mechant est revele",
       "meme Reponse forcee, un tour plus tard : le seuil mord des que la securite passe SOUS la taille du "
       "deck de mechants",
       SC, [], ["Puzzle.EndVillainPhase()", "Puzzle.EndVillainPhase()"],
       {"tous": 2, "deck_de_mechants": 4, "compteurs": [["gs161b", "safety", 4]]}),
    # ============================================================== gs161b : retrait du mechant vaincu
    # ⚠ Villains.BuildVillainDeck MELANGE (Faces.ShuffleAllTo) : avec les 6 memes cartes et le meme seed
    # de test, l'ordre reel est gs170 (Attuma) PUIS gs190 (Veranke) PUIS... (confirme par mesure directe,
    # 20/10/2026) -- PAS gs166. Les deux cas ci-dessous visent donc gs170/gs190, pas les card_id cites
    # dans leur titre.
    _c("gs161b mechant vaincu NON DERNIER (2 en jeu, gs170 puis gs190 reveles) : gs170 est retire, gs190 "
       "reste, PAS de 3e revelation",
       "« If a villain is defeated, remove that villain from the game » (regle generale p.16), applique "
       "SEULEMENT quand Enemies at Large n'a pas deja revele un remplacant (il ne le fait que pour le "
       "DERNIER mechant) : le deck de mechants ne bouge pas",
       "rhino", MEC_SOCLE + [
           "Puzzle.BuildVillainDeck('gs166','gs170','gs176','gs181','gs186','gs190')",
           "Puzzle.RevealNextVillain()", "Puzzle.RevealNextVillain()",
           "Puzzle.PutIntoPlay('gs162a')",
       ], ["Puzzle.Damage('gs170', 6)"],
       {"tous": 1, "deck_de_mechants": 4, "en_jeu": ["gs190"], "hors_jeu": ["gs170"]}),
    _c("gs161b+gs162a mechant vaincu DERNIER (1 seul en jeu, gs170) : Enemies at Large revele le "
       "remplacant (gs190) AVANT le retrait, le deck de mechants descend a 4, gs170 est bien retire",
       "« Forced Interrupt: When the last villain is defeated, reveal the top card of the villain deck... » "
       "(gs162a) JOUE AVANT la Reponse de retrait (gs161b) : un mechant reste en jeu (le nouveau), pas 0",
       "rhino", MEC_SOCLE + [
           "Puzzle.BuildVillainDeck('gs166','gs170','gs176','gs181','gs186','gs190')",
           "Puzzle.RevealNextVillain()",
           "Puzzle.PutIntoPlay('gs162a')",
       ], ["Puzzle.Damage('gs170', 6)"],
       {"tous": 1, "deck_de_mechants": 4, "en_jeu": ["gs190"], "hors_jeu": ["gs170"]}),
    _c("gs161b+gs162a dernier mechant vaincu, deck de mechants VIDE : les joueurs gagnent la partie",
       "« Otherwise, the players win the game » : un seul mechant construit dans le deck de mechants "
       "(gs166), revele puis vaincu -> plus personne a reveler",
       "rhino", MEC_SOCLE + [
           "Puzzle.BuildVillainDeck('gs166')",
           "Puzzle.RevealNextVillain()",
           "Puzzle.PutIntoPlay('gs162a')",
       ], ["Puzzle.Damage('gs166', 6)"],
       {}, verifier="eus_victoire"),
]

VERIFICATIONS = r'''
def eus_victoire(monde, aides):
    """gs162a/b, branche « Otherwise, the players win the game » : deck de mechants vide, dernier
    mechant vaincu -> partie terminee, victoire."""
    if not monde.is_game_over:
        return False, "la partie n'est pas terminee"
    if not monde.game_over.players_won:
        return False, f"les joueurs ont PERDU (attendu : victoire), raison={monde.game_over.reason}"
    return True, "victoire"
'''

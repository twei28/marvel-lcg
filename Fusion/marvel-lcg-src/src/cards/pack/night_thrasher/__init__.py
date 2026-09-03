from cards.pack import *

# ===========================================================================
# Pack NIGHT THRASHER — contenu custom de « DESIGNHACKER », format
# « MC4 SEALED ». Set 153, prefixe `nt`.
#
# DEUX sets dans ce pack :
#   - `Night Thrasher`         (nt001a-nt011, dossier night_thrasher/night_thrasher/)
#   - `Night Thrasher Nemesis` (nt012-nt016, dossier night_thrasher/night_thrasher_nemesis/)
# 18 card_id : 2 faces d'identite, 2 faces d'amelioration PERMANENTE,
# 9 cartes signature distinctes (15 exemplaires), 1 obligation, 4 cartes
# nemesis distinctes (5 exemplaires).
#
# ⚠ `FileManager.CleanName` rend `night_thrasher` et `night_thrasher_nemesis` :
# ce sont bien les noms des deux dossiers de modules (leçon bt019, dont le
# module n'etait jamais charge, en silence).
# ⚠ `set_name` = « Night Thrasher », verifie LIBRE le 03/09/2026. L'homonyme
# `dt125` * Night Thrasher est un ALLIE du pack determination, pas un set.
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : UNE PLANCHE A DEUX FACES, ET NEUF CARTES QUI LA LISENT
#
# `nt003a/nt003b` Battle Board est une amelioration PERMANENTE RECTO-VERSO,
# posee au Setup (`desc.Setup`), qui bascule entre deux traits :
#
#   VEHICLE (nt003a)   +1 CTR au heros, `agile 1`, et 1 menace retiree a
#                      chaque retour sur cette face
#   WEAPON  (nt003b)   +1 ATQ et +1 DEF, et 1 degat a chaque retour
#
# NEUF des quinze cartes du deck la retournent ou testent sa face :
#   RETOURNENT   nt001a (Varial Heelflip), nt002 Disaster, nt005 Kickflip,
#                nt011 Prewind Stance
#   TESTENT      nt002, nt004 Drop In, nt006 Melon Grab, nt007 Tailblock,
#                nt009 Escrima Sticks
#   PUNIT        nt012 Practice (l'obligation interdit de la retourner) et
#                nt014 Cemented (le complot annexe aussi)
#
# Le heros a des statistiques de base MINUSCULES — CTR 1, ATQ 1, DEF 1 — et
# c'est deliberé : la planche vaut la moitie de sa fiche, et la retourner au
# bon moment EST le jeu.
#
# ---------------------------------------------------------------------------
# ⚠ MOT-CLE MAISON `agile 1`, porte par la seule face VEHICLE :
# « reduce damage from attacks with boost cards by 1 ». DEFINI PAR L'AUTEUR
# entre parentheses sur la carte : aucun arbitrage, mais aucune primitive
# moteur non plus. Fiche complete et montage retenu :
# `docs/reference/mots-cles/agile.md`.
#
# ---------------------------------------------------------------------------
# ⚠ LE PACK EST BATI SUR LE TRAIT `SKILL`, et quatre cartes en vivent :
# nt001a (Varial Heelflip se declenche dessus), nt001b (4 cartes SKILL hors
# aspect en construction de deck, et le Manual les recycle), nt008 The Mancave
# (reduit le cout de la prochaine), nt010 Multi-Skilled (une ressource qui ne
# paie QUE ca). Aspect JUSTICE retenu par l'utilisateur le 03/09/2026 : c'est
# le plus gros vivier de cartes SKILL du jeu (12), et il compense la CTR 1.
#
# ---------------------------------------------------------------------------
# ⚠ PIEGES DU MATERIEL, releves a la lecture des 26 scans :
#  - LES NOMS DE FICHIERS NE SONT PAS LES NOMS DE CARTES.
#    `UPGRADE - Night Thrasher_s Suit.png` contient « Prewind Stance » (nt011),
#    `SUPPORT - The Man Cave.png` contient « The Mancave » (nt008, en un mot).
#    Ne jamais nommer une carte d'apres son fichier dans ce pack.
#  - LE ZIP CONTIENT UNE CARTE ETRANGERE : « Fired Up », bandeau
#    « MAGMA NEMESIS (2/5) », art et texte de Selene. ECARTEE sur decision de
#    l'utilisateur (03/09/2026) : le set nemesis de Night Thrasher est complet
#    sans elle (Terrax 1/5, Cemented 2/5, Cosmic Connection 3/5 et 4/5,
#    Cosmic Ax 5/5). A reprendre le jour ou Magma sera portee.
#  - Les exemplaires multiples ont ete compares AU PIXEL sur leur zone de
#    regles : Disaster x2, Drop In x2, Kickflip x4, Tailblock x2 et Cosmic
#    Connection x2 ne different que par leur numero de collection.
#
# ---------------------------------------------------------------------------
# ⚠ HOMONYMES, verifies dans data/cards.json le 03/09/2026 :
#  - « * Night Thrasher » : `dt125`, ALLIE du pack determination. Notre face
#    heros porte le meme nom, c'est le set_name qui differe.
#  - « Battle Board », « Prewind Stance », « The Mancave », « Escrima Sticks »,
#    « Multi-Skilled », « Kickflip », « Melon Grab », « Tailblock »,
#    « Drop In », « Disaster », « Practice », « Terrax the Tamer »,
#    « Cemented », « Cosmic Connection », « Cosmic Ax » : verifies LIBRES.
# ===========================================================================

# ⚠ Les helpers partages du set vivent dans le `__init__.py` DU SET, pas ici :
# les modules font `from . import *`, qui importe le `__init__` du dossier du
# set. Un helper defini ici leve un NameError avale par le moteur (paye sur
# hk005 le 02/09/2026).

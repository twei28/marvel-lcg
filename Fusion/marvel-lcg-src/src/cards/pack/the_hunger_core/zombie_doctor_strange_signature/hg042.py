from . import *

# Hunger Hex — MANIGANCE ANNEXE (SideScheme, deck signature de Zombie Doctor Strange, carte 3/3). Sans trait imprime.
# StartingThreat 3* (3 x nombre de joueurs, lu NATIVEMENT par le moteur depuis `desc.StartingThreat` via
# `HasAttribute.FormatPlayerNumValue` : aucun script requis pour cette valeur, comme pour toute menace de
# depart imprimee avec une etoile).
# While this scheme is in play, each player's hand size is reduced by 2.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - Aucun mot-cle (gras ou non) imprime sur cette carte hors le "*" de StartingThreat (base native, voir
#   ci-dessus, hors perimetre d'une fiche mots-cles). « hand size » n'est pas un mot-cle a fiche dediee dans
#   `docs/reference/mots-cles/` (absent du README) : c'est un attribut de regle de base (`desc`/
#   `HasHandSize`), modifie ici par un malus continu, exactement comme `bp/extreme_risk/51041.py`
#   (« Each identity gets +1 hand size ») ou `skrull_menace/skrull_empire/sk090.py` (« Each identity gets
#   -1 REC »). Rien a creer.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « each player's hand size is reduced by 2 » (effet continu sur TOUS les joueurs, tant que cette carte de
#   rencontre est en jeu) : carte modele `bp/extreme_risk/51041.py` Playing for Keeps (EncounterSideScheme,
#   « Each identity gets +1 hand size » -> `AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Identity,
#   hand_size=+1)`), ici en negatif (-2). `Identity` (pas "You" ni "EngagedIdentity"/"EngagedPlayer") cible
#   TOUTES les identites de la partie, pas seulement un joueur engage avec un ennemi : conforme a
#   « each player's », comme sur `sk090` (« Each identity gets -1 REC » -> `CardFinder(card_type=Identity)`)
#   et CONTRAIREMENT a `trors/spider_woman_nemesis/04054.py` (« While the Viper is engaged with you, YOUR
#   hand size... » -> `control_by="EngagedPlayer"`), inapplicable ici car le texte imprime ne conditionne rien
#   a un engagement : c'est une carte de scheme (le symbole de menace, pas d'ennemi engage) et le texte dit
#   bien « each player's », pas « your ».
# - Le malus est pose/retire automatiquement par la fabrique selon la presence en jeu de LA CIBLE (Identity,
#   toujours vraie tant qu'un joueur a une identite) : `GiveKeywordToInPlayWhenApplyThisInternal` cale son
#   `change_on_event` sur `OnEvent.EnterPlayWhen(card_finder)`, et le moteur retire le gain a la sortie de jeu
#   de CETTE carte (`hg042`) comme sur `51041`/`sk090` : aucune carte de ce paquet n'a besoin de recoder la
#   pose/sortie a la main pour ce genre d'effet (environment_helper.py, meme fabrique).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « WHILE this scheme is IN PLAY » -> effet CONTINU tant que `hg042` est en jeu (pas un When Revealed
#   ponctuel declenche une seule fois) : `GiveKeywordToInPlayWhenApplyThis`, pas `WhenThisRevealed`.
# « EACH player's hand size » -> cible `Identity` (toutes les identites de la partie en cours), pas "You" ni
#   "EngagedIdentity"/"EngagedPlayer" (qui limiteraient le malus a un seul joueur).
# « is reduced BY 2 » -> `hand_size=-2` (malus de 2, pas +2 ; signe verifie contre `04054` qui code
#   « reduced by 1 » en `hand_size=-1`).
#
# BLOC NOMBRES (etape 6) : une seule valeur numerique sur cette carte hors StartingThreat : « 2 » (reduction
#   de main) -> `hand_size=-2` dans le script. StartingThreat "3*" est dans `data/cards_custom.json` (desc),
#   lu nativement, aucune valeur dupliquee dans ce fichier.
#
# A CONFIRMER : aucun doute de regle releve sur cette carte (texte simple, un seul effet continu, aucune
#   limite imprimee, aucun compteur du scenario (infection) ni trait de scenario implique). Ne bloque pas.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            hand_size=-2,
        ),
    ]

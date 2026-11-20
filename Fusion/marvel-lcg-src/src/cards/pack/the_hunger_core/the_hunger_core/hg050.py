from . import *

# The Hive Calls — SIDE SCHEME (set partage « The Hunger Core », carte 5/5 et DERNIERE de hg046-hg050). Trait
# imprime HIVE. StartingThreat 4* (donc 4[per_hero]), Acceleration 1, Boost 1. `data/cards_custom.json` porte
# `"text": ""` pour cette carte : AUCUN texte de capacite n'a ete recupere lors du portage TTS (contrairement a
# hg046-hg049, qui ont chacun un texte complet). Voir le bloc A CONFIRMER plus bas : ce n'est pas suppose a la
# legere, c'est verifie contre le reste du depot.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[acceleration]] (mots-cles/acceleration.md) : « Acceleration Icon: Place +1 threat on the main scheme at
#   the start of the villain phase. » Fiche EXPLICITE : « Aucun script requis pour ce mot-cle : c'est une des
#   bases automatiques du guide. » `desc.Acceleration` est lu nativement par `HasAccelerationIcon`
#   (`SchemeSide2(HasAccelerationIcon, Scheme2)`, `src/game/card/face/base/scheme_side.py`) ; aucun code ici.
#   Carte modele citee par la fiche : `01109` Bomb Scare, qui porte EN PLUS un When Revealed propre (son script
#   ne code QUE ce surplus, jamais l'icone elle-meme).
# - Keyword « Boost » (icone de boost sur une carte Rencontre) : lu nativement par le moteur depuis `desc.Boost`
#   au tirage d'une carte de boost ; aucun mot-cle maison, aucun script necessaire (base automatique du guide,
#   au meme titre que Toughness/Restricted).
# - « StartingThreat »: `Scheme2.RegisterAttribute("StartingThreat", "start_threat")`
#   (`src/game/card/face/base/scheme.py`) lit la valeur directement depuis `desc`. Le suffixe `*` est deja
#   interprete NATIVEMENT par le moteur : `HasAttribute.FormatPlayerNumValue`
#   (`src/game/card/face/attribute/has_attribute.py:17-21`) remplace `*` par `*<nombre de joueurs>` puis evalue
#   la chaine (`"4*"` -> `4*2` = 8 a deux joueurs). Donc `"StartingThreat": "4*"` est deja un 4[per_hero]
#   complet SANS AUCUN CODE, exactement comme toute autre carte Rencontre a seuil per_hero (menace de depart,
#   PV de vilain, etc. — meme mecanisme que `hg001`-`hg003` « PV 12[per_hero] »). Pas une fiche mots-cles dediee
#   (mecanisme generique du moteur sur TOUTE carte avec `desc` chiffre, pas un mot imprime specifique a cette
#   carte), mais verifie au code pour ne pas confondre ce `*` avec celui, DIFFERENT, de `hg049` Hunger Pulse
#   (« Place 1* threat », qui est un `*` dans un APPEL `PlaceThreatOnSchemes`, pas dans un `desc`).
#
# ---------------------------------------------------------------------------
# LIEN AVEC LE TRAIT HIVE (demande explicitement dans la tache)
#
# Le trait HIVE est deja pose sur hg001/hg002/hg003 (Le Coeur, les 3 stades) et sur hg049 Hunger Pulse. Grep
# exhaustif de `src/cards/pack/the_hunger_core/` : AUCUN script du pack ne filtre jamais sur
# `CardFinder(traits=["HIVE"])` ou equivalent — contrairement a METAZOMBIE (filtre par `commun.py` a plusieurs
# endroits : `Metazombies`, `NbMetazombiesEnJeu`, `CapacitesDuCoeur.rupture`). Le lien avec le trait moteur
# n'est donc PAS mecanique ici : HIVE est un trait purement THEMATIQUE sur ce scenario (le Coeur = la Ruche, sa
# manigance de fin de partie « The Hive Calls » = l'appel de la Ruche), sans CardFinder ni capacite d'aucune
# carte du pack qui en depende a ce jour. Si une carte future du scenario devait un jour compter/filtrer les
# cartes HIVE, ce serait une nouveaute, pas un mecanisme deja branche ici.
#
# ---------------------------------------------------------------------------
# CARTE(S) DE REFERENCE (Etape 2) ET A CONFIRMER SUR LE TEXTE MANQUANT
#
# Precedent direct, dans LE MEME DEPOT (`data/cards.json`, cartes officielles deja scriptees) : plusieurs
# SideScheme ont un `desc.text == ""` STRICTEMENT identique a hg050, et AUCUN fichier `.py` n'existe pour elles
# dans `src/cards/pack` (verifie par `find`, zero resultat) :
#   - `01156` Usurp The Throne (Black Panther Nemesis) : `{"Boost":"3","Hazard":"1","StartingThreat":"3*"}`,
#     text="".
#   - `16054` Vendetta (Rocket Raccoon Nemesis) : `{"Boost":"2","Amplify":"1","StartingThreat":"2*"}`, text="".
# Ces deux cartes prouvent qu'une SideScheme purement a base de `desc` (StartingThreat/Boost + une icone
# Hazard/Amplify/Acceleration), sans aucune ligne de texte imprimee, existe deja dans le moteur ET n'a besoin
# d'AUCUN script : le moteur gere tout nativement depuis `desc`. `hg050` a exactement ce profil de `desc`
# (StartingThreat + Boost + Acceleration, rien d'autre) et le meme `text=""`.
# Carte de reference la plus proche AVEC capacite annexe pour comparaison (contre-exemple, montre a quoi
# ressemblerait hg050 SI elle avait une capacite) : `01109` Bomb Scare, `39008` Pump Up the Crowd — les deux
# ont `StartingThreat` avec `*` ET une capacite annexe (When Revealed / When Defeated), toujours DOCUMENTEE par
# un texte imprime non vide dans leur `desc`. hg050 n'a pas ce texte.
#
# ⚠ A CONFIRMER (Etape 3, « Contenu absent du materiel fourni ») : aucune trace du texte imprime de « The Hive
# Calls » n'existe nulle part dans le depot — `data/cards_custom.json` porte `text: ""`, le scan genere
# (`navigateur/.cache/scans-resolution/generes/image/hg050.jpg` et son equivalent FR) est un PLACEHOLDER gris
# uni (nom + type seulement, aucune ligne de regle visible), et aucune autre source (dossier `medias/`,
# fichiers scenario `the_hunger_core(_expert).json`, `tools/cas/the_hunger_core.py`) ne cite de texte pour
# cette carte. Decision retenue ICI, par analogie directe avec `01156`/`16054` (meme profil `desc`, meme
# `text=""`, memes cartes reellement en jeu sans script) : traiter hg050 comme une SideScheme SANS capacite
# annexe, seulement StartingThreat 4[per_hero] + Acceleration 1 + Boost 1 (tous geres nativement). A CONFIRMER
# cependant si le mod TTS source portait bien une ligne de texte perdue lors du portage (hg046-hg049, memes
# auteurs/memes agents, ont TOUS un texte complet) : si une ligne apparait un jour (scan haute resolution,
# reference BGG/TTS), rouvrir ce fichier pour l'ajouter avant de considerer la carte vraiment terminee.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (Etape 5) ET NOMBRES (Etape 6)
#
# Aucune ligne de texte a verifier (texte imprime vide, cf. bloc A CONFIRMER ci-dessus) : rien a coder en
# `GetAbilities`.
# Valeurs numeriques imprimees, toutes dans `desc` (verifiees contre `data/cards_custom.json`, aucune n'est
# dupliquee dans ce script) :
#   - `StartingThreat: "4*"` -> 4[per_hero], lu nativement (cf. bloc mots-cles ci-dessus).
#   - `Acceleration: "1"` -> une icone Acceleration, lue nativement.
#   - `Boost: "1"` -> icone de boost valeur 1, lue nativement.


def GetAbilities() -> Sequence['Ability']:
    return []

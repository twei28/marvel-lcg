# KIT-HEROS-IA — à lire d'abord

Ce zip permet à **une autre IA** (ChatGPT, Gemini, un autre Claude…) de **refaire les fichiers d'un héros** pour le
jeu Marvel Champions du projet « Narwhal Champions » : les cartes (identité à deux faces, cartes signature,
obligation, set némésis, cartes d'aspect), le deck de départ, les scripts, les textes français, la biographie, la
réplique de recrutement, la liste des images et les preuves de test. **Claude** (l'assistant qui a le dépôt du jeu)
**compare, teste et intègre** ensuite ce que l'autre IA a produit.

Version du 20/10/2026. Construit par `outils/construire-kit-heros.py` depuis le dépôt (chaque exemple est la copie
exacte d'un fichier réel).

## Ce que contient le zip

| Fichier / dossier | Contenu |
|---|---|
| **`KIT-HEROS-COMPLET.md`** | **le manuel** (douze chapitres) : à lire en entier avant de commencer |
| `LISTE-DES-FICHIERS.md` | la **liste maîtresse** : chaque fichier d'un héros, son chemin, son rôle, qui le produit |
| `verifier-livraison-heros.py` + `verifier-livraison-campagne.py` + `reference/` | le **vérificateur de livraison** (Python 3, sans dépendance ; il charge celui des campagnes placé à côté) et les listes du jeu qu'il utilise (ids, traits, compteurs, préfixes, **152 decks existants**, **cartes signature**) |
| `modeles/A-officiel-ant-man/` | un héros **officiel à trois formes**, complet, au format d'une livraison |
| `modeles/B-maison-lockjaw/` | un héros **maison** complet (decklist de l'auteur, obligation à choix, set némésis, cartes d'aspect) |
| `modeles/C-maison-harry-osborn/` | un héros maison **sans decklist d'auteur** (`player_deck` vide), règle de deck-building propre |
| `modeles/D-officiel-recent-iron-fist/` | un héros officiel **partiellement publié**, avec **57 cas de test** et ses gabarits |
| `modeles/E-questions-iron-fist/` | les **questions et les décisions réelles** de l'utilisateur (forme de `QUESTIONS.md`) |
| `commun/` | les fichiers **génériques** du moteur, du lanceur et des outils qui font marcher un héros (mise en place du joueur, chargement des decks, catalogue des héros, règles de deck-building, gates) |
| `annexes/` | le kit de cartes (A), les recettes du moteur (B), les mots-clés (C), les processus carte et héros (D), le guide (E), **l'index de l'API du moteur (I)**, l'architecture (J), le manuel de campagne (L : chapitres généraux de cartes et de scripts), les gabarits d'Iron Fist (M) |

## Comment l'utiliser

### 1. Donner le zip à l'IA, avec ce message

> Tu vas produire les fichiers d'un héros pour un jeu Marvel Champions dont le moteur est open source (Python).
> Lis d'abord `LISEZ-MOI.md`, puis `KIT-HEROS-COMPLET.md` **en entier** (chapitres 1 à 12), puis ouvre les modèles du
> dossier `modeles/` avant d'écrire ta première carte. Les règles absolues du chapitre 1 s'appliquent **à chaque
> réponse** : fidélité à 100 % au texte imprimé (le scan fait foi) ; n'invente jamais une fonction, une clé ou une
> chaîne de ciblage ; ce que tu ne sais pas faire s'écrit `A_FAIRE_CLAUDE` ; **une question à la fois, en choix
> multiple, image à l'appui** ; ne touche jamais au moteur ; ne livre que des fragments pour les fichiers partagés ;
> `player_deck` reste vide pour un héros maison sauf decklist fournie par son auteur ; jamais la carte signature d'un
> autre héros dans un deck ; ne prétends jamais qu'un test est vert si tu ne l'as pas exécuté.
> Le héros à produire : **<nom, auteur ou éditeur, dossier des images, decklist de l'auteur s'il y en a une>**.
> Commence par la phase 0 (lecture) et la phase 1 (cadrage) du §9.1 : propose l'identifiant de deck, la clé de pack et
> **deux préfixes libres** en une question à choix multiple, puis attends ma réponse.
> Livre **par lots**, dans le dossier `livraison/` décrit au chapitre 9, et lance
> `python3 verifier-livraison-heros.py livraison/` (avec `--officiel` pour un héros d'éditeur) avant chaque livraison.

### 2. Ce que vous lui fournissez en plus

* **Toutes les images de cartes du héros** (une image par face : héros, alter ego, chaque carte signature,
  l'obligation, les cartes némésis, les cartes d'aspect s'il y en a) ;
* la **decklist de l'auteur** si elle existe (sinon `player_deck` restera vide), le nom de l'auteur, ses liens ;
* **vos réponses** à ses questions (une à la fois : le §1.3 du manuel dit lesquelles).

### 3. Ce que vous me rapportez

Le dossier **`livraison/`** de l'IA, tel quel (avec `MANIFESTE.md`, `QUESTIONS.md`, `BESOINS-MOTEUR.md`,
`A_FAIRE_CLAUDE.md`, `GABARITS.md`, `AUTO-VERIFICATION.md`, `integration/…`). Claude :

1. relance `verifier-livraison-heros.py --moteur …` **contre le jeu réel** ;
2. **compare** chaque carte à son image, le deck à la decklist, chaque script à son texte imprimé ; si le héros existe
   déjà dans le jeu (test du kit), `outils/comparer-livraison-heros-au-depot.py` donne, élément par élément, ce qui
   est identique, différent, manquant ou en trop ;
3. fusionne les fragments, recalcule les checksums, pose les images, **exécute** les gates : cas de test, preuve par
   substitution, `verifier_tous_les_decks`, autoplay ;
4. vous rend la liste de **ce qui est juste, ce qui est faux et ce qui reste à décider**.

## Ce que le vérificateur dit des modèles eux-mêmes (calibrage)

Les quatre modèles passent avec **0 erreur** (`python3 verifier-livraison-heros.py modeles/A-officiel-ant-man/livraison --officiel`,
etc.). Les avertissements qui restent sont de vrais doutes que le jeu porte déjà : traits absents de la liste typée
du moteur, aucun cas de test dédié pour les héros anciens (leurs cas vivent dans le gros harnais), un `deck/starter`
qui existe déjà dans le jeu (ces modèles *sont* des héros déjà intégrés), `metadata.author` absent d'un héros maison,
héros officiel dont l'éditeur n'a pas tout publié. Un avertissement n'est jamais « sans importance » : il s'explique.

## Ce que ce kit ne fait pas

Il ne produit ni images, ni scans, ni vignettes, ni checksums ; il ne modifie pas le moteur ; il ne lance aucun test
(l'IA n'a pas le moteur) ; il ne remplace pas une partie jouée par un humain.

## Avertissement sur ce que le vérificateur sait et ne sait pas

`verifier-livraison-heros.py` contrôle la **forme** et les **références croisées** (45 casses volontaires, toutes
détectées : `outils/test_verifier_livraison_heros.py`). Un script peut le passer **et ne rien faire en partie** : c'est
pourquoi les règles « n'invente rien » et « `A_FAIRE_CLAUDE` honnête » comptent plus que tout le reste, et pourquoi
Claude exécute ensuite les cas de test et `verifier_tous_les_decks`.

# KIT-CAMPAGNE-IA — à lire d'abord

Ce zip permet à **une autre IA** (ChatGPT, Gemini, un autre Claude…) de **refaire les fichiers d'une campagne** pour
le jeu Marvel Champions du projet « Narwhal Champions » : les cartes, les scénarios, les sets de rencontre, les
scripts, la logique de carnet, la description de la campagne, les textes français, les listes d'images et les preuves
de test. **Claude** (l'assistant qui a le dépôt du jeu) **compare, teste et intègre** ensuite ce que l'autre IA a
produit.

Version du 20/10/2026. Construit par `outils/construire-kit-campagne.py` depuis le dépôt (chaque exemple est la
copie exacte d'un fichier réel).

## Ce que contient le zip

| Fichier / dossier | Contenu |
|---|---|
| **`KIT-CAMPAGNE-COMPLET.md`** | **le manuel** (plus de 6 000 lignes) : à lire en entier avant de commencer |
| `LISTE-DES-FICHIERS.md` | la **liste maîtresse** : chaque fichier d'une campagne, son chemin, son rôle, qui le produit |
| `verifier-livraison-campagne.py` + `reference/` | le **vérificateur de livraison** (Python 3, sans dépendance) et les listes du jeu qu'il utilise |
| `modeles/A-officielle-the-mad-titans-shadow/` | une campagne **officielle** complète, au format d'une livraison |
| `modeles/B-maison-web-of-deceit/` | une campagne **maison** (fan-made) complète, au format d'une livraison |
| `modeles/C-livraison-exemple-hunting-season/` | la **vraie livraison** d'une autre IA (ce que Claude a reçu) |
| `modeles/D-patrons-de-campaign-py/` | les **douze** `campaign.py` du jeu, un motif par mécanique |
| `commun/` | les fichiers **génériques** du moteur, du serveur, de l'écran et du plateau qui font marcher une campagne |
| `annexes/` | le kit de cartes (A), les recettes du moteur (B), les mots-clés (C), les processus (D), le guide (E), l'état des lieux des campagnes (F), le journal de Web of Deceit (G), la boucle de campagne (H), **l'index de l'API du moteur (I)**, l'**architecture (J)**, les modèles Skrull Menace (K) |

## Comment l'utiliser

### 1. Donner le zip à l'IA, avec ce message

> Tu vas produire les fichiers d'une campagne pour un jeu Marvel Champions dont le moteur est open source (Python).
> Lis d'abord `LISEZ-MOI.md`, puis `KIT-CAMPAGNE-COMPLET.md` **en entier** (chapitres 1 à 15), puis ouvre les modèles
> du dossier `modeles/` avant d'écrire ta première carte. Les règles absolues du chapitre 1 s'appliquent **à chaque
> réponse** : fidélité à 100 % au texte imprimé ; n'invente jamais une fonction, une clé ou une chaîne de ciblage ;
> ce que tu ne sais pas faire s'écrit `A_FAIRE_CLAUDE` ; **une question à la fois, en choix multiple** ; ne touche
> jamais au moteur ; ne livre que des fragments pour les fichiers partagés ; ne prétends jamais qu'un test est vert
> si tu ne l'as pas exécuté.
> La campagne à produire : **<nom, auteur, nombre de scénarios, livret, dossier des cartes>**.
> Commence par la phase 0 (lecture) et la phase 1 (cadrage) du §12.1 : propose le code de campagne, le nom de pack et
> **deux préfixes libres** en une question à choix multiple, puis attends ma réponse.
> Livre **scénario par scénario**, dans le dossier `livraison/` décrit au §12, et lance
> `python3 verifier-livraison-campagne.py livraison/` avant chaque livraison.

### 2. Ce que vous lui fournissez en plus

* **Le livret** de la campagne (PDF) et **toutes les images de cartes** (une image par face) ;
* les noms des auteurs et de l'équipe (crédits) ;
* **vos réponses** à ses questions (une à la fois : le §1.3 du manuel dit lesquelles).

### 3. Ce que vous me rapportez

Le dossier **`livraison/`** de l'IA, tel quel (avec `MANIFESTE.md`, `QUESTIONS.md`, `BESOINS-MOTEUR.md`,
`A_FAIRE_CLAUDE.md`, `CARNET-CLES.md`, `AUTO-VERIFICATION.md`, `integration/…`). Claude :

1. relance `verifier-livraison-campagne.py --moteur …` **contre le jeu réel** ;
2. **compare** chaque carte à son image et à son texte, chaque scénario au livret, chaque clé du carnet à sa lecture ; si la campagne existe déjà dans le jeu (test du kit), `outils/comparer-livraison-au-depot.py` donne, élément par élément, ce qui est identique, différent, manquant ou en trop ;
3. fusionne les fragments, recalcule les checksums, **exécute** les vérificateurs, les cas de test, les épreuves de
   boucle de campagne, l'autoplay ;
4. vous rend la liste de **ce qui est juste, ce qui est faux et ce qui reste à décider**.

## Ce que le vérificateur dit des modèles eux-mêmes (calibrage)

`python3 verifier-livraison-campagne.py modeles/A-officielle-the-mad-titans-shadow/livraison --officiel` → **0 erreur**.
`python3 verifier-livraison-campagne.py modeles/B-maison-web-of-deceit/livraison` → **0 erreur**.
Les avertissements des deux modèles sont de vrais doutes (liste vide justifiée par un commentaire, `name` de set en
minuscules, épreuves sans test de l'estampille…) : un avertissement n'est jamais « sans importance », il s'explique.

## Ce que ce kit ne fait pas

Il ne produit ni images, ni scans, ni vignettes, ni checksums ; il ne modifie pas le moteur ; il ne lance aucun test
(l'IA n'a pas le moteur) ; il ne remplace pas une partie jouée par un humain.

## Avertissement sur ce que le vérificateur sait et ne sait pas

`verifier-livraison-campagne.py` contrôle la **forme** et les **références croisées** (16 familles de défauts
vérifiées par mutation : `outils/test_verifier_livraison.py`). Un script peut le passer **et ne rien faire en partie** :
c'est pourquoi les règles « n'invente rien » et « `A_FAIRE_CLAUDE` honnête » comptent plus que tout le reste, et pourquoi
Claude exécute ensuite les cas de test et les épreuves.

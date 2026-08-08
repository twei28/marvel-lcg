# Rangement du dossier — état, cible, et ce qui a été fait

Écrit le 08/08/2026. Le dossier `Marvel LCG last try` avait accumulé trois ans
de copies, d'essais et d'archives sans logique apparente. Ce document dit ce
qu'était chaque chose, où elle est allée, et pourquoi.

Il se lit seul, sans autre contexte.

---

## 1. Ce qu'il y avait, et ce que c'était vraiment

Le dossier parent contenait 4,2 Go répartis en neuf entrées, dont plusieurs
doublons partiels d'un même travail.

| Entrée | Taille | Ce que c'était |
|---|---|---|
| `Jeu Marvel Champions/` | 2,5 Go | **la copie vivante**, celle que lancent les `.bat` |
| `Jeu Marvel Champions Arnaud/` | 909 Mo | **installation complète** du 6/8, mais sans les scans FR ni Agent 13 |
| `Jeux original/` | 486 Mo | le jeu distribué d'origine, référence de la reconstruction |
| `Fusion/` | 294 Mo | doublon partiel : 9846 fichiers contre 22125 dans la copie vivante |
| `ui-app/` | 68 Mo | 13 fichiers contre 1221 dans la copie vivante |
| `ui-check/` | 37 Mo | 73 fichiers contre 108 |
| `Chatgpt/`, `Claude/` | 44 Mo | archives de la reconstruction du source, été 2026 |
| `cartes-multiple-man/` | 352 Ko | essai de carte, jamais intégré |

**Le piège** : rien dans les noms ne disait laquelle des copies était vivante.
Seul `JOUER-SOLO.bat` le révélait, en pointant sur
`Jeu Marvel Champions/Fusion/marvel-lcg-src`.

### Les dépôts git

Une recherche naïve en trouve quatre. **Il n'y en a que deux** :
`Fusion/.git` et `Jeu Marvel Champions/Fusion/.git` sont des dossiers **vides**,
et git remonte alors au parent, ce qui donne l'illusion de dépôts distincts.

| Dépôt réel | Commits | Fichiers suivis | Contenu |
|---|---|---|---|
| racine | 47 | 100 | le projet de refonte design, `.planning/` |
| `Jeu Marvel Champions/` | 171 | 322 | tout le travail réel |

### À l'intérieur de la copie vivante

Sa racine mélangeait sept documents markdown, quatre archives zip de packs de
cartes (161 Mo), un mp3 d'ambiance de 83 Mo, un APK de 175 Mo, et les dossiers
de travail du moteur.

**Vérifié avant de bouger quoi que ce soit** : ni le mp3, ni l'APK, ni les zips,
ni les sept documents ne sont référencés par une seule ligne de code. Les
déplacer ne casse rien.

---

## 2. L'arborescence cible

```
Marvel LCG last try/
├── Jeu Marvel Champions/          la seule copie vivante
│   ├── docs/                      les documents, dont celui-ci
│   ├── paquets-cartes/            les zips de packs fournis par les auteurs
│   ├── medias/                    mp3, APK, badges
│   ├── Fusion/marvel-lcg-src/     le moteur et ses données
│   ├── ui-app/                    le plateau React
│   ├── ui-check/                  les captures de contrôle
│   ├── outils/                    les scripts d'entretien
│   └── JOUER-*.bat, JOUER-*.command
├── Jeux original/                 la référence, intouchée
├── _archive-2026-08-08/           tout le périmé, rien de supprimé
│   ├── copie-Arnaud/
│   ├── racine-Fusion/
│   ├── reconstruction-source/     Chatgpt, Claude, cartes-multiple-man
│   └── depot-racine/              .planning, ui-app, ui-check et leur .git
└── JOUER-EN-MULTI.bat
```

**Principe** : une seule copie vivante, une seule référence, et tout le reste
dans une archive datée qu'on peut supprimer plus tard en connaissance de cause.

---

## 3. Les règles à tenir

**Une seule copie fait foi.** `Jeu Marvel Champions/` est la seule qui compte.
Toute autre copie qui réapparaît est un doublon jusqu'à preuve du contraire.

**La copie WSL n'est pas dans cet arbre.** `~/marvel-work/fusion/marvel-lcg-src`
existe en parallèle et sert de source à `ui-app/deployer.sh`. Elle a déjà écrasé
du travail deux fois. Toute modification de `src/` ou de `public/` doit y être
poussée après coup. Voir le paragraphe 8 de `CAMPAGNES.md`.

**Un seul dépôt git.** `Jeu Marvel Champions/` et rien d'autre. Un `.git` qui
réapparaît ailleurs est une erreur.

**La racine de la copie vivante n'accueille que les lanceurs.** Un document va
dans `docs/`, un pack fourni dans `paquets-cartes/`, un binaire lourd dans
`medias/`. Rien d'autre ne se pose à la racine.

---

## 4. Ce qui a été fait le 08/08/2026

Tout a été exécuté et vérifié, **sauf un dossier**. Rien n'a été supprimé.

**Archivé** : la copie Arnaud, les dossiers `Chatgpt`, `Claude` et
`cartes-multiple-man`, et le dépôt de la racine avec son `.git`, son
`.gitignore`, son `.planning`, ses `ui-app` et `ui-check`. Le dépôt archivé a
été contrôlé après coup : ses 47 commits et ses 100 fichiers suivis sont
intacts.

**Rangé dans la copie vivante** : sept documents dans `docs/`, quatre archives
de packs dans `paquets-cartes/`, le mp3, l'APK et la sauvegarde dans `medias/`.
`medias/` et `paquets-cartes/` ont été ajoutés au `.gitignore` : ce sont des
binaires lourds qui n'ont rien à faire dans l'historique.

**Vérifié** : une partie complète d'Agent 13 jouée après le rangement, sept
rounds, fin normale. Le jeu n'a pas bougé.

### Deux écarts à connaître

**`Fusion/` à la racine : contenu déplacé, coquille vide restante.** Le dossier
lui-même est verrouillé par un processus Windows, probablement une fenêtre de
l'explorateur restée ouverte dessus. Établi par élimination : le renommer sur
place échoue, mais renommer chacun de ses sous-dossiers réussit, aucun processus
WSL n'y a de fichier ouvert, et `mv`, `cmd /c move` et PowerShell `Move-Item`
échouent tous les trois de la même façon.

Contournement appliqué : ses 14 entrées, 9846 fichiers et 294 Mo, ont été
déplacées une par une dans `_archive-2026-08-08/racine-Fusion/`. Il ne reste
qu'un dossier vide. Pour le faire disparaître, fermer les fenêtres de
l'explorateur puis :

```bash
rmdir "/mnt/c/Users/arnau/Desktop/Marvel LCG last try/Fusion"
```

**La copie Arnaud avait été mal jugée.** Un premier examen l'avait déclarée vide
de ses données ; c'était un chemin de test erroné. Elle est complète. Ce qui
justifie son archivage est qu'elle date du 6 août et qu'il lui manque les 4271
scans FR et les seize cartes d'Agent 13, pas qu'elle serait creuse. Si tu t'en
sers, remets-la en place plutôt que de la reconstruire.

---

## 5. Refaire ou défaire

### Refaire, si l'arbre se salit à nouveau

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try"

# 1. L'archive
mkdir -p _archive-2026-08-08/{reconstruction-source,depot-racine}
mv "Jeu Marvel Champions Arnaud" _archive-2026-08-08/copie-Arnaud
mv Fusion                        _archive-2026-08-08/racine-Fusion
mv Chatgpt Claude cartes-multiple-man _archive-2026-08-08/reconstruction-source/
mv .git .gitignore .planning ui-app ui-check _archive-2026-08-08/depot-racine/

# 2. Le faux depot git, un dossier vide
rmdir "Jeu Marvel Champions/Fusion/.git"

# Note : le dossier `Fusion/` lui-meme peut etre verrouille par Windows.
# Dans ce cas, deplacer son CONTENU plutot que le dossier :
#   mkdir -p _archive-2026-08-08/racine-Fusion
#   for e in $(ls -1a Fusion | grep -v '^\.$\|^\.\.$'); do
#       mv "Fusion/$e" _archive-2026-08-08/racine-Fusion/
#   done
#   rmdir Fusion   # une fois le verrou leve

# 3. L'interieur de la copie vivante
cd "Jeu Marvel Champions"
mkdir -p docs paquets-cartes medias
git mv CAMPAGNES.md RAPPORT-SCANS-FR.md docs/
mv BRIEF-REFONTE-PLATEAU.md GUIDE-*.md MULTIJOUEUR.md RAPPORT-AUDIT-CARTES.md \
   squirrel_girl_*.md docs/
mv *.zip paquets-cartes/
mv *.mp3 MarvelChampions.apk sauvegarde-packs-supprimes-*.tar.gz medias/
```

### Défaire

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG last try"
mv _archive-2026-08-08/copie-Arnaud "Jeu Marvel Champions Arnaud"
mv _archive-2026-08-08/racine-Fusion Fusion
mv _archive-2026-08-08/reconstruction-source/* .
mv _archive-2026-08-08/depot-racine/{.git,.gitignore,.planning,ui-app,ui-check} .
rmdir _archive-2026-08-08/{reconstruction-source,depot-racine} _archive-2026-08-08
```

---

## 6. Ce qu'on n'a pas touché, et pourquoi

**`Jeux original/`** est la référence de la reconstruction du source. Elle ne
bouge pas et ne se supprime pas.

**L'intérieur de `Fusion/marvel-lcg-src/`** est le moteur. Son organisation
répond à ses propres contraintes, décrites au paragraphe 1 de
`GUIDE-CREATION-CONTENU.md`. On n'y touche pas depuis ce document.

**Le dépôt de la copie vivante** garde ses branches en l'état. `src/cards/`
n'est toujours pas suivi dans son ensemble, ce qui a coûté douze cartes
périmées le 7/8. C'est un chantier à part, pas du rangement.

**Rien n'a été supprimé.** L'archive pèse environ 1,3 Go. Elle se supprime le
jour où tu es sûr, et pas avant.

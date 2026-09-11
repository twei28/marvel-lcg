# Ce que fait play.marvelsimulator.com, et ce qui vaut la peine d'être copié

**Relevé le 11/09/2026** à la demande de l'utilisateur, sur les pages
publiques (la page `/stats` répondait 500). Projet fan-made, « not
affiliated with FFG or Marvel », v0.0.26, Discord et Ko-fi.

## Ce qu'ils ont

- **Simulation en masse** : « run hundreds of games in seconds against any
  villain », 60+ vilains, 100+ modules, tier lists et taux de victoire tirés
  de « thousands of games ». C'est leur cœur.
- **Challenges** : héros imposé (ex. Spider-Woman), vilain + modules imposés
  (« Magog Standard, Legions of Hydra, Longshot, Ship Command »), on soumet un
  **Deck ID marvelcdb**, classement « Win % / Score / Avg Turns », 82 inscrits.
- **Play Online** : jouer soi-même dans le navigateur, « free, no install, no
  signup ». Bandeau « Install for a faster, full-screen experience » (PWA) et
  message hors-ligne.
- Import marvelcdb par ID ou URL, difficulté Standard/Expert et variantes,
  jusqu'à 4 modules.

## Ce qu'on a déjà

Import marvelcdb (+ tri par popularité depuis le 11/09), vilains, modules,
difficultés, journal de partie, comptes, campagne, multijoueur. Et
`tools/autoplay.py`, mais c'est une **gate interne** dont le pilote tient
~7 rounds : ses taux de victoire ne signifieraient rien pour un joueur.

## À copier, par ordre de rendement

1. **PWA installable** : manifeste, icône, bouton « Installer », plein écran
   sur tablette. Une demi-journée, gain immédiat.
2. **Défi de la semaine, en solo** : héros + vilain + modules tirés d'une
   graine hebdomadaire, deck libre (import marvelcdb), meilleur score personnel
   en rounds/victoire. Tout le socle existe (moteur, comptes, import).
3. **Simulation en masse pour le joueur** : NON tant que le pilote ne gagne
   pas. Prérequis : un pilote qui tient une partie entière.

## Ajout du 11/09/2026 : Thwart (Hasyame, GitHub, MIT)

Appli Android compagnon, pas un moteur : deckbuilder, suivi de campagne (8
extensions), randomiseur de scénario filtré par contenu possédé, journal de
parties avec stats, référence de règles bilingue FR/EN, cartes via MarvelCDB
(comme nous). À reprendre éventuellement :

- **Référence de règles bilingue** : dérivée de `deejimy/mc-reference` (CC0).
  Source possible pour les tooltips de mots-clés du plateau, aujourd'hui
  écrits à la main dans `docs/reference/mots-cles/`.
- **Randomiseur de scénario** (vilain + sets modulaires, filtré par
  collection) : petit, adapté au wizard.
- **Suivi de campagne** : structure d'état par extension, si un mode campagne
  arrive.

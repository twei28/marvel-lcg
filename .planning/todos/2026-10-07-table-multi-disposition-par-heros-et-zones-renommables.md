> **MISE À JOUR 23/10/2026 : FAIT, l'en-tête ci-dessous est périmé** (ancien état : « « Rien n'est commencé » puis « en cours de codage » »). Preuve : `EditeurTable.tsx:227` (double-clic pour renommer), `cote-ameliorations.ts:9`, `FenetreReglages.tsx:356` (tri : `docs/rapports/etat-du-backlog-2026-10-19.md` §3, n°11).

# Table personnalisable : aussi en multijoueur, par héros, et zones renommables (07/10/2026)

**Statut : BACKLOG, demande de l'utilisateur. Rien n'est commencé.** Suite de la fiche
`2026-10-05-table-par-briques-decisions.md` (la table faite de briques), à lire avant.

## La demande (ses mots)
« Pour le truc où on peut changer la disposition de la table, on doit avoir un bouton pour le faire aussi pour le multi, genre
choisir où vont les sbires et alliés de chaque héros, et aussi peut-être pouvoir renommer les zones. »

## Trois demandes distinctes
1. **Un bouton pour modifier la disposition AUSSI en multijoueur.** À vérifier d'abord pourquoi / où il manque aujourd'hui : l'éditeur
   (`ui-app/src/board/EditeurTable.tsx`, monté dans `board.tsx` ~l. 4299 avec `enregistrerDisposition(nombreDeJoueurs, ...)`) est
   réservé au plateau PC, et la disposition est enregistrée PAR NOMBRE DE JOUEURS.
2. **Choisir où vont les sbires et les alliés DE CHAQUE HÉROS.** Chaque joueur (ou l'hôte ?) place les zones de ses propres sbires
   engagés et de ses alliés.
3. **Peut-être renommer les zones.** (« peut-être » : à confirmer.)

## ⚠ Contradiction avec une décision déjà prise (05/10/2026)
La fiche des briques dit : « Multijoueur : UNE brique par type, rangée par joueur à l'intérieur (pas de brique par joueur) » et
« titre AUTOMATIQUE » d'après les briques de la zone. La demande d'aujourd'hui va dans l'autre sens :
- placer les sbires/alliés **héros par héros** suppose une brique (ou une zone) PAR JOUEUR ;
- renommer une zone remplace le titre automatique (« Héros et soutiens », « X et Y »).
À arbitrer avant de coder : soit on assouplit la règle « une brique par type » en multi, soit on garde l'organisation par type et on
ajoute seulement un choix de rangée par joueur à l'intérieur de la zone.

## Questions à trancher le jour où on le fait (à poser une à une)
- **Qui décide en multi** : chaque joueur règle SA table (vue personnelle, chez lui seulement), ou l'hôte règle pour tout le monde ?
- Les zones d'un autre héros (alliés, sbires engagés avec lui) : on les voit où ? Les déplacer change-t-il la vue des autres joueurs ?
- **Renommer** : un nom libre par zone ? Retenu par zone, par joueur ou par nombre de joueurs ? Un bouton « remettre le titre automatique » ?
- La disposition enregistrée par nombre de joueurs suffit-elle, ou faut-il l'enregistrer par COMPOSITION (2 héros, mais lesquels) ?
- Téléphone : l'éditeur reste-t-il réservé au PC ?

## Décidé le 07/10/2026 (questions une à une), EN COURS de codage

- **Renommer une zone** : double-clic sur le titre de la zone, seulement en mode « Modifier la table ». Entrée valide, Échap annule. Vider le champ remet le titre automatique. Le nom vaut pour ce joueur, toutes ses parties, sur ce navigateur (gardé avec sa disposition) ; les autres joueurs gardent les leurs. Constat de l'utilisateur : « je n'arrive pas à cliquer à un endroit pour changer le nom de la zone » (rien n'était codé).
- **Améliorations à gauche ou à droite de la carte** (demande nouvelle : « il y a des gens qui aiment avoir les améliorations du côté gauche de la carte du héros ou de l'allié ») : réglage dans Réglages, onglet Jeu ; s'applique à TOUTES les cartes qui portent des améliorations (héros, alliés, méchant, sbires) ; droite par défaut, comme aujourd'hui.

## CLOS le 21/10/2026 : les 5 questions tranchées, et c'était déjà fait

Questions posées une à une, réponses de l'utilisateur :
1. **Qui décide en multi** : chaque joueur règle sa propre vue (pas l'hôte pour tous).
2. **Zones d'un autre héros** : on garde toujours SA PROPRE disposition, quel que soit le héros regardé (pas celle du héros consulté).
3. **Mémorisation** : par nombre de joueurs (pas par composition exacte de héros).
4. **Granularité alliés/sbires** : la brique commune actuelle (une zone « Alliés, sbires et environnement » pour toute la table, rangée par joueur à l'intérieur) suffit — PAS de zone séparée par héros. Lève la contradiction du 05/10 : plus besoin d'assouplir la règle « une brique par type ».
5. **Téléphone** : éditeur réservé au PC (inchangé).

**Vérifié en vrai** (serveur local, partie 2 joueurs Adam Warlock + Angel) : ces 5 réponses correspondent EXACTEMENT à ce que le code fait déjà (`EditeurTable.tsx`, `table-briques.ts`, `enregistrerDisposition(nombreDeJoueurs, ...)`, garde `modePlateau !== 'mobile'`). L'éditeur « Modifier la table » s'ouvre dans les Réglages en vraie partie multijoueur, affiche la zone commune « Alliés, sbires et environnement », un glisser-déposer fonctionne sans erreur. **Rien à coder : item 6 du backlog clos.**

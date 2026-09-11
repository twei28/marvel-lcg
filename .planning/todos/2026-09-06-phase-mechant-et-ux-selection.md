# Pour le 06/09/2026 — la phase du méchant, et l'UX de la préparation

Demandé le 05/09/2026 en fin de session, après le lot « connexion, historique,
tchat, vue par joueur, deckthèque ».

## 1. Revoir TOUTE la phase du méchant

Périmètre à cadrer au début : ce qui se passe entre la fin du tour des joueurs
et le retour à leur tour — activation du méchant, activation des sbires,
manigance, révélation de la carte rencontre, et tout ce que le plateau en
montre (ou ne montre pas).

Existant à relire avant de proposer quoi que ce soit :

- `ui-app/src/board/RecapPhaseMechant.tsx` — le récapitulatif de phase
  existe déjà, avec son mode « phase rapide ».
- `ui-app/src/board/CouchePasAPas.tsx` — le pas-à-pas, sa pause, son
  « tout passer ».
- `ui-app/src/board/causalite.ts` et `historique-brut.ts` — ce qui est
  narré et comment.

## 2. UI/UX de la sélection : héros, méchants, decks

L'écran `prepare.html` (le wizard en 5 étapes : ÉQUIPE, DECKS, MÉCHANT,
MENACE, FINAL), servi par `Fusion/marvel-lcg-src/public/js/prepare/`.

À reprendre : le choix des héros, celui des méchants, et l'assignation des
decks — c'est là qu'on passe le plus de temps avant de jouer.

Point de départ utile : la deckthèque vient d'être élaguée (05/09), il ne
reste par héros que le deck de départ et les préconstruits d'origine. La
maquette de l'étape DECKS doit en tenir compte.

## Méthode

Passer par `superpowers:brainstorming` avant de toucher au code : les deux
sujets sont des refontes, pas des correctifs, et le périmètre est à fixer avec
l'utilisateur avant d'écrire quoi que ce soit.

## Où en est le chantier 1, au soir du 06/09

**Spec validée** (54 décisions, une par question) :
`docs/superpowers/specs/2026-09-06-phase-mechant-deroule-detaille-design.md`.

**Livraison 1, le squelette : faite.** Le mode « Détaillé » existe, le cartouche
découpe la phase en étapes, chacune avec son titre, sa règle du jeu, ses
conséquences, et un bouton « Suivant ». Les étapes de narration technique du
moteur défilent seules, sans clic.

**Livraison 2, la mise en scène : faite.** Un bandeau rouge traverse l'écran
avec un éclair à l'ouverture de la phase (deux secondes, une seule à partir du
round 4), la carte qui agit grandit sur un plateau assombri, un trait fléché
part vers sa cible, les cartes de boost se retournent une par une. Tout se
débraye quand on coupe les animations. 662 tests.

**Contrôle en partie réelle : six points sur huit sont bons.** Rapport complet
dans `.superpowers/sdd/2026-09-06-deroule-phase-mechant-mise-en-scene/task-7-report.md`.

**Le défaut qui commande la livraison 3 : le moteur n'attend pas le cartouche.**
Mesuré en jeu : cinquante-deux entrées de journal en sept cent cinquante
millisecondes pendant que le cartouche en est encore à sa première étape. La
phase entière est jouée avant qu'on ait lu une ligne, et le cartouche raconte
ensuite un passé révolu. On a vu le moteur poser sa question sur l'ordre des
sbires avant que le cartouche ait annoncé la moindre activation, et le cartouche
commenter une manigance déjà vaincue et remplacée.

Cause exacte : `ui-app/src/board.tsx:2209` passe `onTerminer={() => undefined}`,
et le cartouche n'a aucun rappel « Suivant ». Le moteur SAIT attendre
(`decisionAccuse` rend `attendre-clic` pour le mode détaillé,
`moteur.ts:200-202`) et la méthode qui le relâche existe déjà
(`moteur.avancerMaintenant()`, exposée en `board.tsx:815`). La porte est là,
personne ne tient la clé : seul le filet anti-blocage à six secondes la rouvre.

Ce n'est pas un branchement d'une ligne. Le cartouche construit ses étapes
depuis le journal, le moteur retient ses trames sur un autre critère : la
correspondance entre une étape lue et une trame retenue est à concevoir. C'est
la première chose à trancher avec l'utilisateur pour la livraison 3.

**Reste aussi pour la livraison 3** (déjà cadré dans la spec, jamais commencé) :
les cas particuliers (ennemi étourdi, étape vide, héros vaincu, défaite en
pleine phase, sbire qui arrive en cours de phase), le récap raccourci et sa
réintroduction en mode détaillé, le menu Options avec ses quatre choix
expliqués, la version mobile, les étapes de distribution et de premier joueur,
et le déroulé des effets pendant le tour du joueur.

## Reste ouvert de la session du 05/09

- **Trois decks custom gardés par prudence** : `Doctor_Doom_custom.json`,
  `Okoye_custom.json`, `Wolverine_custom.json`. Ils n'avaient pas la
  `metadata.aspect_note` des decks générés, donc rien ne disait qu'ils étaient
  de moi. À trancher.
- **`deployer.ps1` n'efface jamais** : il extrait une archive par-dessus
  l'existant. Toute suppression de fichier doit être répercutée à la main sur
  le serveur (fait pour les 145 decks). Un `--delete` global est exclu : il
  emporterait les dossiers de travail volontairement exclus (sauvegardes,
  campagnes, decks des joueurs).
- **Sièges et `hot_seat`** : correctif posé le 05/09 (guetteur de silence dans
  `moteur.ts`, voir `sieges-hot-seat.ts`), à confirmer en partie réelle à
  plusieurs héros sur le serveur.

## Point du 11/09/2026 au soir (relecture de la fiche)

- **« Le moteur n'attend pas le cartouche »** : corrigé le 06/09 à 17:48
  (`68381f96`, « le cartouche du déroulé détaillé relâche enfin le moteur ») ;
  `board.tsx` passe `onTerminer={avancerPasAPas}`. Le paragraphe ci-dessus
  est donc dépassé sur ce point.
- La phase du méchant a ensuite changé de forme : **scène centrale** (spec
  `2026-09-07-scene-phase-mechant-design.md`, commits `44e2c4db`,
  `402d1d11`, `8c1f3583`), puis ancrée en bas en portrait (`3e96ad44`), et
  les cartes de statut y entrent (`d4ff2c9e`).
- **La partie 2 (UX de la sélection)** est couverte par la modale du héros
  (11/09) et les écrans téléphone (`40400f0f`, `fee77023`).
- **Reste à re-cadrer avec l'utilisateur**, jamais commencé ni vérifié : les
  cas particuliers de la livraison 3 (ennemi étourdi, étape vide, héros
  vaincu, défaite en pleine phase, sbire arrivé en cours de phase), le récap
  raccourci, le menu Options à quatre choix, les étapes de distribution et de
  premier joueur, le déroulé des effets pendant le tour du joueur. Passer par
  `superpowers:brainstorming`, une question à la fois.

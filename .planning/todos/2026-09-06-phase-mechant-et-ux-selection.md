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

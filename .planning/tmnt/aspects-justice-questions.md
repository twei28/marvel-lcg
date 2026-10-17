# Aspect TMNT Justice (`uj`) : questions ouvertes

16/10/2026. Une question par carte, multichoix, option recommandée en premier. Scans :
`scratchpad/zip-aspect/TMNT Aspect/Justice/<fichier>` (dossier du zip fourni). Chaque carte concernée est
codée selon l'option recommandée en attendant, et marquée « NON terminée » dans
`.planning/tmnt/aspects-justice-gabarits.md` jusqu'à la réponse.

Questions déjà tranchées appliquées : Q-R1 (bandeau « ✦ <titre d'origine> » : unicité sur les deux titres,
`unique_also` posé sur uj023, uj026, uj028, uj036, uj038, uj039) ; Rampage avec deck court (jouable).
Q-R2 (deck-builder qui masque les homonymes) reste ouverte côté coordinateur : 18 cartes uj portent le nom
exact d'une officielle (uj001, 002, 003, 007, 010, 011, 013, 014, 015, 017, 019, 022, 024, 025, 029, 030, 031,
032, 035, 040).

---

## Q-uj002 : Chance Encounter (`uj002`), « Attach to a scheme »

Scan : `Justice/Chance Encounter.png`. L'officielle (26034 / 60025) dit « Attach to a **side** scheme ».
Le scan dit « Attach to a scheme. Max 1 per scheme. » mais son Interruption parle toujours de « attached
**side** scheme ». Coquille de l'auteur, ou changement voulu ?

1. **(recommandé, codé)** Suivre le scan : jouable sur n'importe quelle manigance, principale comprise. En
   jeu : rien ne change sur une manigance annexe ; posée sur la principale, la carte ne fait jamais rien
   (son Interruption ne vise que la manigance annexe attachée).
2. Coquille : seulement sur une manigance annexe, comme l'officielle (`ability_link` vers 26034 possible).
   En jeu : identique à l'officielle.
3. Autre (précise).

## Q-uj036 : Venus (Bonnie) (`uj036`), « their deck and a discard pile »

Scan : `Justice/Venus.png`. Reskin de Manifold (51014) : « searches their deck and discard pile ». Le scan
imprime « their deck and **a** discard pile ».

1. **(recommandé, codé : `ability_link` 51014)** Coquille : le joueur choisi fouille SON deck et SA défausse,
   comme Manifold. En jeu : identique à Manifold.
2. Voulu : le joueur choisi fouille son deck et UNE pile de défausse au choix (la sienne ou celle d'un autre
   joueur). En jeu : en multijoueur, on peut récupérer la manigance joueur d'un partenaire. Script propre.
3. Autre (précise).

## Q-uj040 : Zone of Silence (`uj040`), « 4 card cards »

Scan : `Justice/Zone of Silence.png`. Le scan imprime « discard up to 4 card cards » ; l'officielle 21050
dit « 4 cards ». Aucun effet de jeu, seulement le texte affiché.

1. **(recommandé, fait)** Afficher « 4 cards » (texte corrigé dans `cards.json`, carte liée à 21050).
2. Reproduire la coquille à l'affichage.
3. Autre (précise).

# T13 et T14 : mobile portrait et éventail des améliorations (19/10/2026)

Branche `table-eventail` (départ `e5a844f8`).

## T13 (mobile portrait) : ABANDONNÉE
Décision de l'utilisateur en cours de travail : « téléphone et tablette, on oublie pour le moment ». Un premier jet (défilement automatique jusqu'à la bande « Ton héros », cibles fixes sur les cartes, bande mise à plat) avait été commité puis RETIRÉ dans le commit suivant. Il avait été vu fonctionner à 390×844 (héros seul et héros + 3 alliés : cartes entièrement visibles, centre = la carte, retour du défilement), mais n'est pas livré. Cause trouvée : en portrait il n'y a pas de `.plateau-cadre`, donc les cartes sont « absentes » et les choix de défense retombent en boutons du bandeau.

Téléphone/tablette : non traité, à reprendre plus tard. Points à regarder : défilement vers la bande des défenseurs, cartes touchables ≥ 44 px, bandeau étroit (195 px au lieu de la largeur d'écran : `left: 50%` + translate), améliorations à toucher dans la bande « Améliorations », tablette 1180×820.

## T14 (éventail des améliorations) : faite, PC seulement
Ce qui change (`ui-app/src/board/TableSansModale.tsx`, `table-sans-modale.css`, `DemandeCentrale.tsx`, `dico-en.ts`) :
- Les choix d'amélioration (interruption/réponse) portent leur carte. Pendant la question, elles s'étalent en rangée de VRAIES cartes (112 px de large, nom + capacité dessous) à côté de la pile du porteur, et disparaissent au choix.
- Placement (`placerEventail`, testé) : à droite de la pile, sinon à gauche, au-dessus, en dessous, puis un trou entre les cartes. Évite le bandeau, le porteur, la zone de l'aperçu (à droite) et les autres cartes de la table quand c'est possible.
- Le bouton nommé du bandeau reste. Survol d'une carte de la rangée : aperçu habituel + halo vert sur la carte de la pile. Max N : rien touché à la règle.

Preuves (serveur 2496/2497, Playwright, Barrière énergétique 05017 + Clairvoyance mw004 + Bottes Propulsées 16052) :
- 1280×720, 3 améliorations sous le héros : rangée à x=433..785, y=419..614, 3 cartes de 112×158 + libellé, aucune ne recouvre le bandeau (6,82,200×342), le héros ni l'aperçu au survol (x=924..1269). Clic sur une carte : rangée retirée, choix pris.
- 1280×720, 3 sous un allié (Hulk) : rangée à y=377..., sans recouvrir bandeau, héros ni aperçu.
- 1280×720, 1 amélioration sous le héros : idem. 1920×1080, 2 sous un allié : idem.
- `npx tsc --noEmit` propre ; `npx vitest run src/board/` : 3858/3859 avant ajout de la clé anglaise « Améliorations à jouer », corrigée ensuite (dico-en, DemandeCentrale, eventail-ameliorations repassés : 42/42). Le dossier `src/board/` complet n'a pas été relancé après cette dernière correction.
- Captures : `corrections-2026-10-19/captures/T14-AVANT-*` et `T14-APRES-*` ; script `corrections-2026-10-19/outils/t14-eventail.mjs`.

Non vérifié : 2 améliorations sous le héros (1 et 3 vues, pas 2), 1 amélioration sous un allié, les cas où la place manque vraiment (le repli « trou entre les cartes » n'est testé qu'en unité), tablette, mobile, paysage (hors périmètre). Le style de l'éventail (halo vert, libellé) reste à valider par l'utilisateur : voir `.planning/tmnt/table-eventail-questions.md`.

## Fichiers touchés
`ui-app/src/board/TableSansModale.tsx`, `ui-app/src/board/table-sans-modale.css`, `ui-app/src/board/DemandeCentrale.tsx`, `ui-app/src/board/dico-en.ts`, `ui-app/src/board/eventail-ameliorations.test.ts`, `docs/rapports/phase-mechant-sur-la-table/corrections-eventail-mobile-2026-10-19.md`, `docs/rapports/phase-mechant-sur-la-table/corrections-2026-10-19/` (captures T14, `outils/t14-eventail.mjs`), `.planning/tmnt/table-eventail-questions.md`.

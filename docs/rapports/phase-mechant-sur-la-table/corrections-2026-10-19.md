# Corrections de la phase du méchant « Sur la table » — 19 octobre 2026

Branche `table-corrections` (issue de `sauvegarde-cle-usb-2026-10-14`, départ `036a3b31`). Rien n'est poussé ni déployé.
Captures et mesures : `corrections-2026-10-19/` (captures/, outils/). Tests : `ui-check/tests/phase-sur-table-*.spec.ts`, `ui-app/src/board/*.test.ts`.
Preuves générales : `npx tsc --noEmit` propre ; `npx vitest run src/board` : 332 fichiers, 3862 tests passent ; specs Playwright lancées sur le
projet `pc` seulement (1280×720), sur un moteur d'essai à moi (port 2494, historique redirigé vers /tmp).

**Périmètre final décidé en cours de route** : je ne fais PAS T13 (mobile portrait), T14 (éventail des améliorations), T15 (toast),
T16 (sbire Rapide), T17 (vaincus) — repris par d'autres agents ; T18 est ANNULÉE (aucune ligne n'en a été commencée, rien à défaire).
« Téléphone / tablette : non traité, à reprendre plus tard » (voir la liste en fin de rapport).

## Défaut prioritaire — attaque déclenchée par une carte révélée (Assaut 01187, Se Liguer 01189)
- **Cause : le plateau, pas le moteur.** Le moteur distribue et résout bien les boosts (faits : `attaque / resolu / Klaw / boosts=2 / subi=2`,
  PV réels 10 → 5). `rangerLesConsequences` (deroule-phase.ts) rangeait l'attaque SOUS la carte révélée : plus d'annonce, de lecture des
  boosts ni de résultat, et le bilan comptait mal.
- Correction : l'attaque ou la manigance déclenchée reste une étape à part, juste APRÈS sa carte ; les entrées de sbire et les statuts restent rangés dessous.
- Chiffres (dégâts réels / dégâts du bilan, avant → après) : Assaut + Klaw 5 / 3 → 5 / 5 ; Se Liguer + 1 sbire 8 / 4 → 8 / 8 ; Se Liguer sans sbire 6 / 3 → 6 / 6 ;
  Assaut + Rhino 6 / 3 → 6 / 6 ; lectures de boosts : 2/1/3 → 4/3/6. (Se Liguer avec 2 sbires : le héros meurt, comme attendu.)
- Mode « Détaillé » ancien et version en ligne (3c199bca) : même fonction `rangerLesConsequences` à l'identique, donc même rangement ; le moteur y est tout aussi juste,
  les dégâts sont portés ; la différence : l'attaque est résumée en une ligne sous la carte (pas de cartes boost lues). Je n'ai pas relancé le mode ancien dans un navigateur : à confirmer si besoin.
- Autres déclencheurs hors activation : le sbire Rapide est le cas T16 (non traité, voir « Observé en passant »). Captures : `captures/bug-assaut/`. Cas de test : `deroule-phase.test.ts` (3 cas) + script `outils/bug-assaut.mjs`.

## T1 — Étiquettes « Défendre avec … »
- Avant : 112 px fixes pour des cartes de 78 à 95 px ; chevauchement 19 px (PC), 27 px (tablette), 8 px (paysage) entre voisines à 2 et 3 alliés ; PV cachés.
- Après : largeur = celle de la carte (mesure : 84,7/84,7 ; 78/78 ; 95,3/95,3 px), aucun recouvrement, posée sous la barre de PV (aussi pour une carte inclinée), verbe en petit + nom sur 2 lignes puis « … ».
- Test : `phase-sur-table-etiquettes.spec.ts` (4 écrans × 1/2/3 alliés ; passe sur PC aux deux extrêmes après la dernière modification ; les 4 formats avaient été mesurés par script avant le dernier retouchage de style).
- Captures : `t1-avant-*`, `t1-apres-*`.

## T2 — Bandeau de question (+ précision : colonne sur le côté)
- Par défaut : colonne de 200 px contre le bord GAUCHE (l'aperçu agrandi est ancré à droite). Recouvrement bandeau/aperçu mesuré avant : 593 px² (héros), 69 px² (allié, sbire) à 1280, 4619 px² en paysage 1050 ; après : 0 (PC et tablette). Les cartes gardent leur taille.
- Poignée visible (44 px au toucher), glisser souris ET doigt (émulation tactile Chromium par CDP), reste entier dans la table (jamais sur la barre du haut, testé aux 3 coins), place retenue (localStorage + try/catch, retrouvée après rechargement), double-clic ou bouton ⟲ pour la remise, flèches du clavier. Le fond du bandeau laisse passer les clics : la carte dorée dessous reste cliquable ; les boutons restent cliquables.
- Mobile portrait (< 641 px) : le bandeau reste une ligne en haut à la largeur de l'écran ; **non capturé** (instruction « téléphone/tablette : on oublie »).
- Test : `phase-sur-table-bandeau.spec.ts` (souris 1280 et doigt 1180, passent). Captures : `t2-*`.

## T3 — Ordre d'activation des sbires
- Le moteur reçoit l'ordre par `ChooseOrder` (cibles dans l'ordre du clic, `range="All"`) ; aucune règle changée.
- Bouton « Garder l'ordre de la table (Espace) » : 7 clics (6 sbires + Valider) → 1. L'ancien mode (cliquer chaque sbire) reste. Le bandeau s'affiche à chaque tour (le moteur pose la question à chaque fois). Même bouton pour l'ordre des joueurs. Bebop/Rocksteady : question à choix unique, déjà un clic.
- ⚠ Le moteur liste les sbires du plus récent au plus ancien (droite → gauche à l'écran) ; j'ai pris « gauche → droite » : vérifié, le premier sbire de la rangée active en premier. **Question ouverte Q1.** Script `outils/t3-ordre.mjs`, captures `t3-*`.

## T4 — Petit écran
- Avant (844×390) : la barre (40 px fixes) passait sur deux lignes ; le centre de « Fin du tour » était touché par `zone-complots-secondaires` ; boutons de 30 px au toucher.
- Après : une ligne (Menu/Annuler/Sauver en pictogrammes, ligne de phase masquée quand la place manque), barre au-dessus de la table (z-index), 52 px et boutons ≥ 44 px (hauteur de « Fin du tour » 44 px dès que le pointeur est tactile ; souris inchangée 30 px). Le doublon flottant du bas : min-height 44 px au toucher.
- Test `phase-sur-table-entete.spec.ts` (PC, tablette 1180, 1050×480, 844×390, 390×844 : `elementFromPoint` au centre, ≥ 44 px, aucun bouton hors barre) : 5 passent. Captures `t4-avant-*`, `t4-apres-*`.

## T5 — Boost qui met une carte en jeu (Weapons Runner 01121)
- Ordre ACTUEL avant correction (capture image par image, `outils/t5-boost-image-par-image.mjs`) : « Klaw va attaquer » → question de défense → clic → directement « Weapons Runner entre en jeu » avec la carte sur la table ; **le boost n'était jamais lu et le résultat de l'attaque jamais montré** (le moteur inscrit l'entrée AVANT que l'attaque passe à « boosts » puis « résolu » ; le clic sautait à l'entrée).
- Après : lecture du boost en grand → « Klaw attaque Spider-Man 1 dégât (ATQ 0 + Boost 1 = 1) » → « Weapons Runner entre en jeu » → la carte n'est visible qu'à ce moment (retenue aussi pendant le vol de jeton). Test de séquence `phase-sur-table-boost-entree.spec.ts` (passe). Pas de changement du moteur. Non testés séparément : attachement ou Rapide (même mécanique d'étape « entrée »).

## T6 — Défendre sans s'incliner (héros ET allié inclinés)
- Usagi up041 : proposé dans « Qui défend ? » (le héros incliné non), désigne Usagi. Témoin : un allié ordinaire incliné ne défend pas, aucune question ni message.
- « Je peux faire ça toute la journée » 56047 : proposé à l'annonce ; joué, Spider-Man incliné défend (« ATQ 0 + Boost 1 − DÉF 3 = 0 »). Bodyguard se011 : proposé, DÉF 2 retranchée. Test `phase-sur-table-defendre-sans-incliner.spec.ts` (4 cas passent).
- **Draw Their Fire 53011 : non proposé** dans ma reproduction (aucune fenêtre de réponse ouverte par le moteur au début de la phase) — pas un défaut du plateau, cause non trouvée : Q4. Le bouton de Bodyguard s'appelle « Interruption de héros » : Q3.

## T7 — « Tout le monde valide »
- Reproduit (Klaw, Spider-Man + She-Hulk, graines 4321 et 777). Cause : la révélation lue dans le journal (clé `carte:…`) est remplacée par celle du moteur ; sa clé disparaît, l'index retombe sur la dernière étape validée hors attente ; seul un clic en sortait, or en « tous » le clic est refusé et « Prêt » déjà marqué → « Prêt · 2 / 2 » éternel.
- Correction : une étape déjà validée qui n'est pas la dernière passe à la suivante (garde : clé identique, pas une annonce, pas le bilan, pas une relecture). Spec multi : concerne, tous, quiconque passent sur PC. Le bouton « détaché du DOM » de « quiconque » ne s'est pas reproduit. `outils/t7-tous-valident.mjs`.

## T8 — Textes
- « Klaw passe au stade 2 » (au lieu de `stade-revele`) ; écran de fin : « DÉFAITE ! / VICTOIRE ! » en français (les images n'ont que l'anglais : elles ne servent plus qu'en anglais) ; fenêtre « LIMITE D'ALLIÉS » ; calcul « − 1 Barrière énergétique » ; options d'Ultron et de Lay the Beatdown traduites (textes français existants : `textes-fr-complets` « 01134 », `textes-fr-fanmade` « tk022 ») ; dico anglais à jour (test passe).
- ⚠ Moteur touché (champ additif) : `world_stat.py` ajoute `source_id` aux réductions. Le toast « gagne 1 menace » pour un statut : c'est T15, non traité.

## T9 — Renfort
Pastille rouge « RENFORT » contre la carte lue, phrase en petit dessous (« une autre carte va être révélée », ou « Renfort de X » pour la carte révélée par un Renfort) ; plus de surtitre ni de « Renfort : … » dans le bandeau (en colonne, hauteur ≤ 166 px au lieu d'environ 250 px) ; carte lue entière, y compris pour deux Renforts d'affilée. Test `phase-sur-table-renfort.spec.ts`. Captures `t9-*`.

## T10 — Calcul par source
Moteur (champs additifs : `message_type.py`, `face_action.py`, `can_attack.py`) : le fait d'attaque porte `bonus` = (source, id, valeur) pour les bonus d'EFFETS (pas les icônes de boost). Plateau : un terme par source au nom français de la carte, reste « Bonus » si inconnu. Preuve : avant « ATQ 0 + 1 Bonus + Boost 1 ★ = 2 », après « ATQ 0 + 1 Altéré Berserk + Boost 1 ★ = 2 » (Berserk Mutate 04116 en boost de Klaw). Limite : les bonus permanents (attachements déjà comptés dans l'ATQ annoncée) n'ont pas de source (Crossbones affiche déjà « + 1 Fusil Laser » dans la question).

## T11 — Règles cachées
Une ligne discrète dans le bandeau, qui disparaît avec lui : « Accélération : +1 menace » (icônes des manigances en jeu tant que le fait du moteur n'est pas arrivé), « ★ Nom : effet de la carte », « Désorienté : n'empêche pas d'attaquer » (moteur : `desoriente` additif), « Perforant : le Tenace est retiré », et en plus « Tenace : défaussé à la place des dégâts » (Q5). Texte français + dico anglais. `outils/t11-regles.mjs`, captures `t11/`.

## T12 — « Continuer (Espace) » toujours présent
Bouton à chaque étape (désactivé pendant un trajet de cartes) ; phrase « Clique la carte dorée, ou Espace » supprimée ; la carte dorée avance toujours. Test `phase-sur-table-continuer.spec.ts` (étapes vues, phase menée au bout en alternant carte et bouton).

## Observé en passant (non corrigé, T16)
Avec un sbire Rapide qui attaque pendant le tour du joueur (Le Vautour 01167, Rhino, Fin du tour avec le sbire en jeu), la partie reste en « En attente de Spider-Man » sans aucune fenêtre ni bandeau dans le mode « Sur la table » (écran sans bouton). À reprendre avec T16.

## Ce que je n'ai pas pu vérifier
Tablette et téléphone sur appareil réel (émulation seulement) ; aucun test tactile pour T9 à T12 ; T7 seulement sur PC ; T2 portrait ; mode « Détaillé » ancien relancé dans un navigateur ; Draw Their Fire.

## Téléphone / tablette : non traité, à reprendre plus tard
À revérifier au toucher : poignée du bandeau (44 px) et glisser au doigt sur appareil ; bandeau en colonne sur tablette portrait ; étiquettes « Défendre avec » en 844×390 après les derniers changements de style ; barre du haut (52 px, pictogrammes) à 844×390 et 390×844 ; « Fin du tour » ≥ 44 px ; pastille Renfort et ligne de règles à petit écran ; « Continuer » ≥ 44 px (déjà posé par la règle `.tsm-bouton` au toucher).

## T18 (annulée) — notes pour plus tard
Fichiers qu'elle toucherait : `ui-app/src/board/moteur.ts` (interrupteur `ETAPE_PAR_ETAPE_SUR_TABLE`, `lireModePhaseMechant`, `MODE_SUR_TABLE_OUVERT`), `board/phase-presentation.ts`, `board/essais.ts`, `board/FenetreReglages.tsx` (liste des choix), `board.tsx` (présentation `table` selon le mode), `board/DeroulePhase.tsx` (`presentation`/`essai`), tests `moteur.test.ts`, `phase-presentation.test.ts`, `FenetreReglages.test.tsx`, `Board…test`, `public/js/prepare/nouveautes.js` (une ligne fr + en). Conception : repli des valeurs rangées `sur-table` et `detaille-bis` vers `detaille` comme `lireModePhaseMechant` ; ne pas supprimer l'ancien cartouche ; la clé `mc_phase_presentation` ne doit plus rien changer ; un seul clic par étape, pas d'avance automatique.

## Questions ouvertes
`.planning/tmnt/table-corrections-questions.md` (Q1 ordre des sbires, Q2 côté du bandeau, Q3 nom du bouton Bodyguard, Q4 Draw Their Fire, Q5 ligne « Tenace »).

## Fichiers du moteur modifiés (champs additifs seulement)
`src/game/world/world_stat.py` (source_id des réductions), `src/game/message/message_type.py`, `src/game/card/face/model/face_action.py`, `src/game/card/face/attribute/can_attack.py` (bonus, desoriente). Aucune règle de jeu changée.

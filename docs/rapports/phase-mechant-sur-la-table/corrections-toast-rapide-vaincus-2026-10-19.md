# Toast d'effet, sbire Rapide, alliés vaincus : 19 octobre 2026

Branche `table-reste` (départ `e5a844f8`). Tout est testé sur PC 1280 x 720 uniquement.
**Téléphone/tablette : non traité, à reprendre plus tard** (décision de l'utilisateur du 19/10/2026).
Captures dans `corrections-2026-10-19/captures/` (préfixes `T15-`, `T16-`, `T17-`), scripts dans `corrections-2026-10-19/outils/`.

## T15 : le toast dit ce qui arrive vraiment

**Cause.** `board.tsx` (`effetCentrale`) tenait pour de la menace tout effet qui n'était ni des dégâts ni des soins : un
statut posé donnait « Klaw gagne 1 menace ». Le texte venait de là, sous l'intitulé « Événement de jeu » de
`EvenementCentrale`, pas des messages d'événement du moteur.

**Changé.**
- Nouveau `phrases-effets.ts` (source unique des phrases) : « Klaw reçoit un statut Sonné », « Klaw perd le statut Sonné »,
  « Hulk reçoit les statuts Sonné et Désorienté », « Peter Parker gagne 1 jeton Rage », « Trafic Clandestin gagne 3 menaces »,
  « Hulk subit 1 dégât » (accord du pluriel).
- Détection des **jetons nommés** (`c_*`, jeton d'accélération) dans `useEffetsCartes`, nouveau genre `token`.
- `deltasStatuts` garde tous les statuts changés d'un rendu (`aussi`) ; les 7 statuts ont leur nom français
  (`libelleDeStatut` n'en connaissait que 3).
- Nouveau `ToastEffetCarte.tsx` : le toast est posé AU-DESSUS de la carte concernée (jamais sur son bas), à gauche si la
  carte est tout en haut (à droite si pas de place), jamais sur la barre du haut ; 1,25 s ; plus d'intitulé.
- `dico-en.ts` mis à jour (test `dico-en.test.ts` vert).

**Inventaire des libellés « gagne / perd »** (objet vérifié) :
| Lieu | Avant | Après |
|---|---|---|
| toast (`board.tsx`) | « X gagne N menace » pour TOUT (statut, jeton) | statut reçu/perdu, jeton nommé, menace seulement pour une vraie menace |
| cartouche, étape statut (`deroule-textes.ts`) | « Klaw gagne Sonné » | « Klaw reçoit un statut Sonné » |
| bilan de phase, ligne statuts | « Klaw gagne Sonné x2 » | « Klaw reçoit un statut Sonné x2 » |
| récap `RecapPhaseMechant.tsx` | « X gagne Sonné » | « X reçoit un statut Sonné » |
| journal `HistoriquePartie.tsx` | « gagne 2 menace » (sans pluriel) | « gagne 2 menaces » |
| cartouche menace / effets de révélation / bilan menaces | « gagne N menaces » (cible = manigance) | inchangé, objet correct |

**Preuve.** Captures `T15-avant-*` (« Klaw gagne 1 menace » au centre, sur les cartes) et `T15-apres-*` : Klaw Sonné, Hulk
(Sonné puis Désorienté, deux commandes), Luke Cage qui entre Tenace, Peter Parker + jeton Rage, menace de la manigance.
`outils/t15-toast.mjs`. Tests : `phrases-effets.test.ts` (13).

## T16 : le sbire Rapide passe par le bandeau de la table

**Changé.** « Sur la table », hors phase du méchant :
- la question « Qui défend ? » est portée par le bandeau latéral (`DemandeCentrale` en mode `surLaTable`, rendue dans le cadre
  du plateau) ; plus de fenêtre au centre ni d'aperçu plein écran du héros (il ne reste que l'agrandissement au survol,
  comme pendant la phase) ;
- le résultat passe par `TableSansModale` (`CoupHorsPhaseSurTable`) : phrase, nombre, calcul (« ATQ 1 + 2 Bonus − DÉF 3 =
  0 dégâts »), carte dorée / bouton Continuer / Espace ; l'ancien cartouche du bas « Hors de la phase du méchant » disparaît
  dans ce mode (il reste dans les autres) ;
- **Espace** ferme le coup sans finir le tour : (constaté, existait avant) Espace au repos finit le tour du joueur en mode
  sur-table ; ce correctif l'en empêche pendant ce coup et pendant la question.
Les règles du moteur ne changent pas.

**Preuve.** `T16-avant-question-fenetre-centrale.png`, `T16-avant-resultat-cartouche-bas.png` ; `T16-apres-question-bandeau.png`,
`T16-apres-resultat-bandeau.png`, `T16-apres-continuer.png`. Parcours réel complet (`outils/t16-rapide.mjs`, Assassin Badoon
puis Vautour 01167) : question, défense, résultat, Espace, retour au tour (`ASSERT parcours complet: OK`, Fin du tour actif,
aucune fenêtre). Tests : `ou-va-la-question.test.ts`, `cartouche-hors-phase-plateau.test.tsx` (attendu mis à jour).

**Non fait / limites.** Pas de flèche attaquant → cible ni de lecture des cartes de boost hors phase (Q3). Une demande
qui n'est QUE une réponse (sans option « Défendre ») garde la fenêtre centrale.
**Corrigé ensuite (voir Q1)** : « Ne pas défendre » contre le Badoon figeait la partie (question imbriquée dans un geste manuel, doublon dans `asking_players`).

## T17 : l'allié vaincu a son étape

**Changé.** `etapesDeroule` ajoute une étape `vaincu` juste après le coup qui met un allié à 0 PV (liste des alliés fournie
par `board.tsx`, hors héros) : ligne « Hulk est vaincu », la carte est **lue au centre** (1,3 s), puis **part en défausse**
(0,65 s) ; le clic ou Espace reste le seul qui avance. Elle précède le bilan. Le héros vaincu garde sa fenêtre
(« Spider-Man est vaincu · La phase s'arrête ici »), vérifiée en parcours. Nouveau `AllieVaincuSurTable.tsx`.

**Preuve.** `T17-avant-allie-vaincu-bilan-sans-ligne.png` (catalogue d'origine : Hulk n'apparaît qu'au bilan, « Hulk a pris
1 dégât 0/5 ») ; Hulk à 1 PV attaqué par Klaw : `T17-apres-hulk-klaw-1-coup/2-vol/3-defausse.png` ; Garde Blindé (Klaw
Sonné) : `T17-apres-garde-2-vol/3-defausse.png` ; `T17-apres-heros-vaincu-inchange.png`. `outils/t17-parcours.mjs`.
Tests : 4 cas dans `deroule-phase.test.ts`.
**Limite** : pas de capture « avant » propre pour le Garde Blindé (le comportement d'avant était identique, sans étape).

## Vérifications
- `npx tsc --noEmit` propre ; `npx vitest run src/board/` en entier : 332 fichiers, 3875 tests, tous verts après la mise à jour
  de `cartouche-hors-phase-plateau.test.tsx` (seul échec, attendu, du changement T16).
- Questions ouvertes : `.planning/tmnt/table-reste-questions.md`.

## Fichiers touchés
Nouveaux : `ui-app/src/board/phrases-effets.ts`, `phrases-effets.test.ts`, `ToastEffetCarte.tsx`, `ToastEffetCarte.css`,
`AllieVaincuSurTable.tsx`, `allie-vaincu.css`.
Modifiés : `ui-app/src/board.tsx`, `board/CoupHorsPhase.tsx`, `board/DeroulePhase.tsx`, `board/deroule-phase.ts`,
`board/deroule-phase.test.ts`, `board/deroule-textes.ts`, `board/deroule-textes.test.ts`, `board/effets-statuts.ts`,
`board/HistoriquePartie.tsx`, `board/RecapPhaseMechant.tsx`, `board/PhaseDynamique.tsx`, `board/dico-en.ts`,
`board/ou-va-la-question.ts`, `board/ou-va-la-question.test.ts`, `board/cartouche-hors-phase-plateau.test.tsx`,
`components/ScanCard.tsx`, `components/ScanCard.css`.
Documentation : ce rapport, `corrections-2026-10-19/captures/*`, `corrections-2026-10-19/outils/*`, `.planning/tmnt/table-reste-questions.md`.

# Roadmap : v1.1 Tablette et téléphone

Jalon ouvert le 13/10/2026. La roadmap v1.0 (phases 1 à 7, refonte UI) est archivée dans
`.planning/milestones/v1.0-ROADMAP.md`. Exigences : `.planning/REQUIREMENTS.md`.
Recherche : `.planning/research/v1.1/` (SUMMARY, ARCHITECTURE, PITFALLS).

## Vue d'ensemble

La tablette n'est pas une troisième mise en page : c'est le plateau PC existant, plus un axe
de saisie (doigt ou souris) détecté sur le dernier geste. On pose d'abord ce détecteur et un
filet Playwright qui touche vraiment (phase 8, bloquante), puis on rend le plateau PC
jouable au doigt en deux lots (phases 9 et 10). Les menus du téléphone touchent des fichiers
disjoints du plateau et avancent en parallèle de la tablette (phase 11). Le plateau du
téléphone est refait ensuite, dans la structure tranchée le 13/10 (paysage en deux colonnes
dérivées des bandes du portrait), en deux lots (phases 12 et 13). Le mode manuel au doigt
vient en dernier, une fois l'aperçu et les cibles tactiles posés (phase 14).

La « décision d'orientation » que la recherche plaçait en phase propre est déjà prise
(décisions de cadrage du 13/10 dans REQUIREMENTS.md) : elle n'a donc pas de phase.

## Règles communes à toutes les phases

- **Aucune dépendance ajoutée** (décision de cadrage, recherche STACK).
- **Aucune modification des règles du moteur.**
- **Déploiement seulement sur « déploie » explicite de l'utilisateur.** Une phase terminée
  n'est pas une phase déployée. Avant tout déploiement : entrées fr + en des nouveautés,
  `bash ui-app/deployer.sh`, contrôle du hash du bundle et du HEAD.
- **Base des suites mesurée le 13/10 (recherche phase 8) : tout est vert**, `boutons-bd.test.ts`
  compris (Vitest 290 fichiers / 3315 tests, `tsc`, `node --test` 187/187). Toute suite rouge
  est donc une régression jusqu'à preuve du contraire. Relever la base à nouveau au début de
  chaque phase : l'arbre est partagé avec d'autres sessions.
- **Avant de toucher `Board.tsx` ou `board.css`** (phases 9, 10, 12, 13, 14) : lire
  `git stash list` (deux sessions ont déjà travaillé sur le même arbre) et vérifier que la
  refonte de la phase du méchant est close, ses fichiers étant les mêmes.

## Phases

- [ ] **Phase 8 : Fondations tactiles et filet de tests** (BLOQUANTE) : le jeu sait si on joue au doigt ou à la souris, quel plateau afficher, et un filet de tests touche vraiment
- [ ] **Phase 9 : Tablette T1, aperçu refermable** : sur tablette, toucher une carte ne laisse plus jamais un aperçu collé ni de toucher fantôme
- [ ] **Phase 10 : Tablette T2, cibles et infobulles** : tout ce qui se touche sur la tablette est assez grand, s'explique, et se feuillette
- [ ] **Phase 11 : Menus du téléphone** : toutes les pages hors partie se naviguent au pouce par une barre en bas (parallélisable avec 9 et 10)
- [ ] **Phase 12 : Plateau du téléphone, paysage et rotations** : téléphone couché en deux colonnes, rien ne se recouvre après des rotations
- [ ] **Phase 13 : Plateau du téléphone, repères et réglages** : le joueur voit ce que le moteur attend hors champ, comprend les mots-clés, et n'a que des réglages qui marchent
- [ ] **Phase 14 : Mode manuel au doigt** : le mode manuel se joue au doigt par une barre d'outils

## Détail des phases

### Phase 8 : Fondations tactiles et filet de tests
**Objectif** : Le jeu distingue doigt et souris d'après le dernier geste, sait quel plateau afficher (y compris sur les écrans limites), et un filet Playwright tactile existe avant le premier changement visible.
**Dépend de** : Rien (première phase du jalon, bloquante pour toutes les autres)
**Exigences** : SAISIE-01, SAISIE-02, SAISIE-03, SAISIE-04, TEST-01, TEST-03
**Critères de succès** (ce qui doit être VRAI) :
  1. Sur un iPad (y compris un iPad qui se déclare Mac), toucher l'écran met le jeu en mode doigt, et utiliser ensuite le trackpad le remet en mode souris, sans que la mise en page saute sous le doigt.
  2. Le joueur règle « Écran tactile : automatique / toujours / jamais » et « Plateau : automatique / téléphone / tablette » ; le choix est respecté à la fois sur le plateau et sur les pages de menus, et survit au rechargement.
  3. Sur un écran limite (iPad mini en portrait, écran partagé), le joueur se voit demander une seule fois à l'arrivée s'il veut le plateau téléphone ou tablette ; il ne la revoit plus ensuite et peut changer d'avis dans les réglages.
  4. Une commande lance les tests Playwright sur un gabarit tablette tactile (Chromium) et un gabarit iPad WebKit, avec de vrais touchers.
  5. Un signalement envoyé depuis la partie contient la taille de l'écran, les zones sûres, le mode de saisie et le plateau choisi.
**Points de vigilance** : relever l'état des suites AVANT tout changement (tout vert au 13/10, `boutons-bd.test.ts` compris) pour que le filet distingue l'existant d'une régression. Un seul propriétaire de l'attribut de saisie, partagé entre le plateau React et les pages JS non compilées ; la disposition par largeur (`useModeMobile.ts`) reste un axe séparé.
**Plans** : 11 plans en 7 vagues
- [ ] 08-01-PLAN.md : base des suites relevée avant tout changement, moteur d'essai p8 (vague 1)
- [ ] 08-02-PLAN.md : saisie.js en TDD, détection doigt/souris, réglages par appareil, mesures (vague 2)
- [ ] 08-03-PLAN.md : filet Playwright tactile (tablette Chromium, iPad et iPad mini WebKit) sur le jeu d'avant (vague 2)
- [ ] 08-04-PLAN.md : saisie.ts et useModeMobile, forme du plateau selon réglage et écran limite (vague 3)
- [ ] 08-05-PLAN.md : saisie.js dans les pages, module « Écran et plateau », empreintes deployer.sh (vague 3)
- [ ] 08-06-PLAN.md : réglages Écran tactile et Plateau dans les Réglages du plateau (vague 4)
- [ ] 08-07-PLAN.md : mesures d'écran jointes à chaque signalement (vague 4)
- [ ] 08-08-PLAN.md : bouton dans les menus, question d'écran limite à l'accueil (vague 4)
- [ ] 08-09-PLAN.md : question d'écran limite à l'entrée du plateau (vague 5)
- [ ] 08-10-PLAN.md : filet tactile complet (bascule, réglages, question, signalement) (vague 6)
- [ ] 08-11-PLAN.md : non-régression contre la base, planche validée, nettoyage (vague 7, checkpoint)

### Phase 9 : Tablette T1, aperçu refermable
**Objectif** : Sur tablette au doigt, lire une carte ne la joue jamais et l'aperçu se referme toujours ; le PC reste strictement inchangé.
**Dépend de** : Phase 8
**Exigences** : TAB-01, TAB-02, TAB-09
**Critères de succès** (ce qui doit être VRAI) :
  1. Sur tablette, toucher une carte ouvre l'aperçu et le menu ensemble ; toucher ailleurs ou la croix les referme, sans déclencher la carte qui se trouve dessous.
  2. Un appui long sur une carte n'ouvre ni la loupe ni le menu d'iOS, et un double toucher ne zoome pas la page.
  3. Avec « Écran tactile : jamais », le plateau PC est identique au pixel à son état d'avant le jalon (comparaison de captures sur les gabarits PC).
  4. Les cas ci-dessus passent dans le filet tactile de la phase 8 (Chromium tactile et WebKit iPad).
**Points de vigilance** : `git stash list` et clôture de la refonte de la phase du méchant vérifiées avant la première ligne dans `Board.tsx`.
**Definition of done** : TAB-09 (PC identique au pixel avec « jamais ») vérifié par captures.
**Plans** : à définir

### Phase 10 : Tablette T2, cibles et infobulles
**Objectif** : Tout ce que le joueur touche sur la tablette est assez grand, s'explique sans survol, et la main se feuillette au doigt.
**Dépend de** : Phase 9 (réutilise l'aperçu posé par T1)
**Exigences** : TAB-03, TAB-04, TAB-05, TAB-06, TAB-07
**Critères de succès** (ce qui doit être VRAI) :
  1. Les boutons de la barre du haut, les compteurs et la croix mesurent au moins 44 px à l'écran, même quand le plateau est réduit.
  2. Un appui long sur une icône affiche son libellé ; un simple toucher l'active.
  3. Toucher une carte injouable affiche la raison pour laquelle elle ne peut pas être jouée.
  4. Une carte de la main agrandie se feuillette en glissant à gauche ou à droite vers les autres cartes de la main.
  5. L'agrandissement de l'identité propose « voir l'autre face » sans changer la forme du héros en jeu.
**Points de vigilance** : mêmes vérifications que la phase 9 avant de toucher `Board.tsx`.
**Definition of done** : TAB-09 (rattachée à la phase 9) revérifiée par captures : avec « Écran tactile : jamais », le plateau PC reste identique au pixel.
**Plans** : à définir

### Phase 11 : Menus du téléphone
**Objectif** : Sur téléphone, toutes les pages hors partie se parcourent au pouce par une barre de navigation en bas, et le jeu installé s'ouvre toujours sur l'accueil.
**Dépend de** : Phase 8 (balise du détecteur de saisie). Fichiers disjoints du plateau : peut avancer en parallèle des phases 9 et 10.
**Exigences** : TELM-01, TELM-02, TELM-03, TELM-04
**Critères de succès** (ce qui doit être VRAI) :
  1. Depuis n'importe quelle page, une barre en bas mène aux 4 ou 5 destinations principales ; le burger ne contient plus que la langue, le compte et les mises à jour.
  2. L'assistant de préparation (Héros, Équipe, Decks, Méchant) se déroule jusqu'au lancement sans que la barre du bas ne masque un bouton ni l'inverse.
  3. Accueil, galerie, éditeur, campagne et connexion utilisent la même barre du bas, et le livre de campagne se feuillette en glissant.
  4. Ouvrir le jeu depuis l'icône de l'écran d'accueil arrive sur l'accueil, jamais sur une ancienne partie.
**Points de vigilance** : le salon invité reste hors périmètre (en pause depuis le 10/10). La recherche signale que l'arbitrage barre du bas ne repose que sur des études génériques : le revérifier à l'œil sur captures avant de l'étendre à toutes les pages.
**Plans** : à définir

### Phase 12 : Plateau du téléphone, paysage et rotations
**Objectif** : Le téléphone couché affiche les bandes du portrait sur deux colonnes, et la partie reste jouable quel que soit le nombre de rotations.
**Dépend de** : Phase 8
**Exigences** : TELP-01, TELP-02, SAISIE-05, TEST-02
**Critères de succès** (ce qui doit être VRAI) :
  1. Téléphone couché, le joueur voit la rencontre à gauche, son héros à droite et sa main en languette, au lieu du plateau PC réduit.
  2. Après n'importe quel nombre de rotations, aucun bouton (Fin du tour compris) ne recouvre la main, et une carte agrandie s'affiche en entier.
  3. Sur iPhone et iPad, aucun bouton ni aucune carte ne passe sous l'encoche ou dans un coin arrondi, en portrait comme en paysage.
  4. Un test enchaîne 6 rotations et vérifie que la main et chaque bouton restent touchables.
**Points de vigilance** : `git stash list` et clôture de la refonte de la phase du méchant vérifiées avant de toucher `Board.tsx` et l'aiguillage du plateau. `viewport-fit=cover` ne s'ajoute qu'avec l'audit complet des marges qui va avec. La recherche n'a pas maquetté la mise en page à deux colonnes : maquettes bâties sur le portrait existant avant le code.
**Plans** : à définir

### Phase 13 : Plateau du téléphone, repères et réglages
**Objectif** : Sur téléphone, le joueur ne rate jamais une demande du moteur hors de l'écran, comprend les mots-clés d'une carte, et ne voit que des réglages qui fonctionnent sur son appareil.
**Dépend de** : Phase 12 (les repères se posent sur les bandes et onglets des deux orientations)
**Exigences** : TELP-03, TELP-04, TELP-05, TELP-06
**Critères de succès** (ce qui doit être VRAI) :
  1. Quand le moteur demande une cible ou une réponse hors de l'écran, une pastille apparaît sur la bande ou l'onglet concerné, et disparaît une fois la demande traitée.
  2. La carte agrandie explique ses mots-clés (Retaliate, Guard…) sous le scan.
  3. Le bandeau Annuler, la taille du texte, l'écran allumé, les vibrations et l'installation fonctionnent en portrait et en paysage.
  4. Sur iPhone, les réglages vibrations, verrou portrait et plein écran n'apparaissent pas ; sur Android et PC ils sont inchangés.
**Points de vigilance** : mêmes vérifications que la phase 12 avant de toucher `Board.tsx`.
**Plans** : à définir

### Phase 14 : Mode manuel au doigt
**Objectif** : Le mode manuel se joue au doigt : on choisit un outil, puis on touche les cartes visées.
**Dépend de** : Phases 9 et 10 (aperçu refermable et cibles tactiles)
**Exigences** : TAB-08
**Critères de succès** (ce qui doit être VRAI) :
  1. Le joueur choisit un outil dans une barre (par exemple « jeton +1 ») et chaque carte qu'il touche ensuite reçoit l'effet, sans ouvrir l'aperçu à la place.
  2. Le joueur voit à tout moment quel outil est actif et peut le relâcher pour revenir au toucher normal.
  3. À la souris, le mode manuel se comporte comme avant le jalon.
**Points de vigilance** : la branche courante s'appelle `mode-manuel` et un stash `WIP on mode-manuel` existe : le lire avant d'écrire quoi que ce soit. Mêmes vérifications avant `Board.tsx`.
**Definition of done** : TAB-09 revérifiée par captures (PC identique au pixel avec « Écran tactile : jamais »).
**Plans** : à définir

## Couverture des exigences

| Exigence | Phase |
|----------|-------|
| SAISIE-01 | 8 |
| SAISIE-02 | 8 |
| SAISIE-03 | 8 |
| SAISIE-04 | 8 |
| SAISIE-05 | 12 |
| TAB-01 | 9 |
| TAB-02 | 9 |
| TAB-03 | 10 |
| TAB-04 | 10 |
| TAB-05 | 10 |
| TAB-06 | 10 |
| TAB-07 | 10 |
| TAB-08 | 14 |
| TAB-09 | 9 (DoD des phases 10 et 14) |
| TELP-01 | 12 |
| TELP-02 | 12 |
| TELP-03 | 13 |
| TELP-04 | 13 |
| TELP-05 | 13 |
| TELP-06 | 13 |
| TELM-01 | 11 |
| TELM-02 | 11 |
| TELM-03 | 11 |
| TELM-04 | 11 |
| TEST-01 | 8 |
| TEST-02 | 12 |
| TEST-03 | 8 |

**Couverture : 27/27, aucune exigence orpheline, aucune en double.**

## Ordre d'exécution

8 (bloquante), puis 9 et 11 en parallèle, 10 après 9, 12 après 8 (de préférence après 10 pour
ne pas croiser deux chantiers dans `Board.tsx`), 13 après 12, 14 après 10.

## Progression

| Phase | Plans terminés | Statut | Terminée |
|-------|----------------|--------|----------|
| 8. Fondations tactiles et filet de tests | 0/11 | Planifiée | - |
| 9. Tablette T1, aperçu refermable | 0/? | Pas commencée | - |
| 10. Tablette T2, cibles et infobulles | 0/? | Pas commencée | - |
| 11. Menus du téléphone | 0/? | Pas commencée | - |
| 12. Plateau du téléphone, paysage et rotations | 0/? | Pas commencée | - |
| 13. Plateau du téléphone, repères et réglages | 0/? | Pas commencée | - |
| 14. Mode manuel au doigt | 0/? | Pas commencée | - |

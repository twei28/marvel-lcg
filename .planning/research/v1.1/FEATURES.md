# Feature Research : jalon v1.1 « Tablette et téléphone »

**Domain :** jeu de cartes coopératif (LCG) au doigt, téléphone et tablette, dans un navigateur
**Researched :** 13/10/2026
**Confidence :** MEDIUM (bonne sur les patterns et les contraintes navigateur, moyenne sur le détail de chaque jeu : plusieurs revues inaccessibles, captures non consultées directement)

Ne répète pas `.planning/research/FEATURES.md` (v1.0, section E « Mobile et tablette »). Point de départ : la refonte
d'octobre (`.planning/todos/2026-10-09-mode-telephone-refonte.md`) et les retours de Raven
(`.planning/todos/2026-10-12-mode-tablette.md`), déjà codés dans `ui-app/src/board/mobile/`.

## Synthèse en 10 lignes

1. Tous les jeux de cartes **portés depuis un PC** sont en paysage sur téléphone (Hearthstone, Magic Arena, Runeterra, Slay the Spire, Balatro, Spirit Island ; Gwent probablement). Le seul grand jeu **conçu pour le téléphone**, Marvel Snap, est en portrait, et ses règles ont été taillées pour l'écran (3 lieux, 4 cartes par côté).
2. Le paysage de ces portages a un prix connu et documenté : main repliée dans un coin, cartes réduites à l'illustration et aux chiffres, texte illisible sans zoom, piles qui recouvrent le plateau (Magic Arena), mauvais toucher (Slay the Spire).
3. Marvel Champions ne peut pas changer ses règles comme Snap : une vingtaine de zones, jusqu'à 4 héros. Aucun jeu étudié n'affiche ça d'un bloc sur un téléphone. Tous **découpent** : main à part, détail à la demande, un joueur à la fois.
4. Le motif le plus universel : **toucher = lire, glisser ou bouton = agir**. Lecture à l'appui long (Hearthstone, Arena, Gwent) ou au toucher (Arena, Snap). Le conflit lire / jouer est la plainte n°1 (Slay the Spire, DragnCards #54).
5. Le retour arrière est rare chez les concurrents (Snap seulement, dans le tour). Le bandeau « Annuler » 5 s déjà construit est **au-dessus** de l'état de l'art.
6. Le navigateur impose sa loi : **iOS Safari ne verrouille pas l'orientation** (ni `screen.orientation.lock()`, ni le manifeste), **pas de plein écran sur iPhone**, **pas de vibration** ; écran maintenu allumé seulement depuis iOS 18.4. Un iPhone tourné doit donc rester jouable ou être poliment invité à revenir.
7. Les surfaces du plateau téléphone existant (4 bandes, une ligne par famille, onglets par héros, main en feuille, encoches, agrandissement avec voisines, Annuler) recoupent déjà les patterns de l'état de l'art. Le jalon doit **consolider**, pas réinventer.
8. Le paysage téléphone actuel (plateau PC réduit) est la source des retours 6 et 7 de Raven. C'est lui qu'il faut repenser.
9. Pour les menus, l'état de l'art mobile (Snap, Arena, Material 3) met les 3 à 5 destinations principales **en barre basse visible** ; NN/g mesure que le menu burger réduit fortement la découverte. Ça remet en question le burger décidé le 09/10 : à arbitrer.
10. **Recommandation d'orientation** : portrait comme seule mise en page conçue et validée ; paysage **dérivé des mêmes bandes** (deux colonnes), plus le plateau PC réduit ; tablette (dès 768 px) = plateau PC tactile. Détail et mesures de confirmation en fin de fiche.

## Panorama : comment les jeux étudiés tiennent au doigt

Légende de confiance : H = source officielle ou plusieurs sources concordantes ; M = une revue ou un article de designer ; B = résumé de recherche ou connaissance non vérifiée cette session.

| Jeu | Orientation et pourquoi | Plateau dense | Inspection | Cible | Jouer une carte | Main | Retour arrière | Conf. |
|---|---|---|---|---|---|---|---|---|
| **Marvel Snap** | Portrait. Ben Brode : « Portrait mode is the way to go. Don't force players to turn their device », parties de 3 min, jeu pensé d'abord pour le mobile | Le plateau a été taillé pour l'écran : 3 lieux × 4 emplacements par côté, jamais plus | Toucher une carte = carte en grand avec son texte (B) | Peu de ciblage manuel par conception | Glisser de la main vers un lieu | Rangée en bas, cartes grandes, toujours visibles | Une carte posée se reprend tant que le tour n'est pas fini (B) | H (orientation), M (ergonomie), B (gestes) |
| **Hearthstone** (téléphone) | Paysage, portage du PC. L'interface téléphone a été refaite écran par écran (2015) | Plateau unique de 7 serviteurs par côté, pas de débordement par règle | Appui long = carte agrandie | Glisser une flèche depuis la carte ou le héros | Toucher la main pour la déplier, puis glisser | **Repliée dans le coin bas droit**, un toucher la déploie | Aucun. Ping à deux doigts | H |
| **Magic Arena** (mobile) | Paysage, portage du PC ; bords latéraux laissés libres pour l'encoche | Terrains à gauche, artefacts à droite, créatures au milieu ; **défilement latéral** du champ de bataille quand il déborde | Appui long, ou toucher = texte complet avec mots-clés expliqués à droite | Toucher la cible | Main déployée puis glisser | **À moitié cachée en bas**, un toucher l'étale et masque le plateau ; bascule main / plateau dans un coin | Annuler le paiement de mana en cours | M |
| **Legends of Runeterra** | Paysage, portage du PC | Banc + zone de combat, 6 unités max par règle | Toucher ou glisser = carte en grand | Glisser vers la cible | Glisser de la main au banc | En éventail, **coin bas droit**, se déploie au toucher ; plainte : cartes qui se chevauchent et texte illisible même zoomé | Un sort se reprend avant validation (B) | M |
| **Slay the Spire** (iOS) | Paysage, portage du PC | Peu de zones | Toucher une carte la lève ; appui long : le doigt **cache** le texte | Glisser vers l'ennemi OU toucher carte puis ennemi | Idem | Rangée en bas | Aucun | M. Contre-exemple : cibles trop petites en haut, lire et jouer confondus, cartes jouées par erreur |
| **Balatro** (mobile) | Paysage, portrait demandé mais **absent** (mods seulement) | Peu de zones | Toucher | Sans objet | Sélection par toucher puis bouton ; acheter, vendre, utiliser = **glisser vers une zone de l'écran** parce que « les boutons du PC seraient trop petits sur téléphone » | Rangée en bas | Désélection libre avant de valider | M |
| **Gwent** (mobile) | Paysage d'après deux résumés, **non confirmé** sur source primaire | 2 rangées par côté, plateau jugé « à l'étroit » sur téléphone | Appui long (B) | Toucher / glisser | Glisser, double-toucher | Rangée en bas | Non documenté | B |
| **Spirit Island** (Handelabra) | Paysage, mise en page adaptée par appareil | Plateau très dense ; mode 2D proposé à la place de la 3D | Cartes agrandissables | Glisser-déposer + quelques touchers | Glisser | Non documenté | Non documenté | M. Le plus proche d'un coop dense : réussi selon les revues |
| **Sentinels of the Multiverse** (Handelabra) | Un résumé parle de vertical sur téléphone, **non vérifié** | Jusqu'à 5 héros + vilain + environnement. Plateau simplifié sur téléphone | Toucher = bulle « ce que fait cette carte » | Toucher | Main ouverte puis glisser | **Rangée sur le côté**, un toucher l'ouvre | Non documenté | B. Revue : « l'iPhone n'est pas la façon idéale de jouer » |
| **Arkham Horror LCG** | Aucune version jouable sur téléphone. Ce qui en tient lieu : **Arkham Cards** (compagnon : decks, carnet de campagne, sac du chaos) pour jouer avec de vraies cartes, et des moteurs PC (OCTGN, TTS, DragnCards) | Sans objet | Recherche de cartes avancée dans le compagnon | Sans objet | Sans objet | Sans objet | Sans objet | H |
| **LotR Adventure Card Game** (FFG Interactive) | **Pas de version mobile sortie** (PC et consoles ; les joueurs la réclamaient sur Steam) | Sans objet | | | | | | M |
| **DragnCards** (LotR, Marvel Champions) | Navigateur, plateau PC. **Mode tactile** depuis fin 2023 | Plateau PC complet | Premier toucher = grande image ; le menu de carte est **difficile à ouvrir** au doigt (issue #54, 2024) | Mode « outil » : on choisit un bouton dans une **barre tactile du bas** (jeton +1, défausser, épuiser), puis on touche les cartes ; second appui sur un bouton de jeton = mode retrait | Glisser (bogues de dépôt sur iPad, #53) | Rangée PC | Annuler du moteur | H (code source et issues lus). Un fork tablette Android pour Marvel Champions a été proposé en 10/2026 puis retiré (#95, #162) |

### Ce qui revient partout (patterns transverses)

1. **Détail à la demande** : on n'essaie jamais de rendre une carte lisible à sa taille de plateau. Illustration + chiffres sur le plateau, texte au toucher ou à l'appui long (Arena l'assume : « on ne lit pas les noms des créatures, mais force et endurance sont nettes »).
2. **Main repliée, divulgation progressive** : Hearthstone, Arena, Runeterra, Sentinels la cachent dans un coin ou un bord, un toucher la déploie. Snap est l'exception parce que son plateau est minuscule.
3. **Défilement d'une zone qui déborde** plutôt que réduction (Arena défile latéralement). C'est exactement le principe des bandes existantes.
4. **Séparer lire et agir** : quand un même geste lit et joue, les joueurs jouent par erreur (Slay the Spire, revue de The Sixth Axis). Les bons portages font lire au toucher et jouer au glisser ou au bouton.
5. **Actions déplacées vers des zones de dépôt** quand les boutons deviendraient trop petits (Balatro).
6. **Mode outil** pour les manipulations répétitives (DragnCards) : choisir l'action, puis toucher les cartes une à une.
7. **Interactifs dans la moitié basse** (designer UI de Snap : « moving a lot more interactable elements closer to the bottom half of the screen »).
8. Ce que **personne ne fait bien** : 4 joueurs sur un téléphone. Sentinels le tente avec une revue mitigée, Spirit Island réussit grâce à une mise en page dédiée par appareil.

## Contraintes de la plateforme (navigateur, pas application native)

| Fait | Source | Conséquence |
|---|---|---|
| `screen.orientation.lock()` absent de Safari (iOS compris) ; Chrome Android seulement en plein écran | MDN browser-compat-data (H) | Sur iPhone, **impossible de forcer le portrait**. Le verrou existant (`EcranTourne.tsx`) ne peut que couvrir l'écran. |
| `orientation` du manifeste ignorée par Safari | MDN browser-compat-data (H) | Même installée sur l'écran d'accueil, l'app iPhone tourne. |
| `requestFullscreen` : iPad seulement, jamais iPhone, avec un bouton imposé et sortie au glissement | MDN browser-compat-data (H) | Sur iPhone, la barre de Safari reste : compter ~60 à 90 px de moins en hauteur portrait, proportionnellement **pire en paysage**. |
| Wake Lock complet depuis iOS 18.4 (avant : pas en app installée) | MDN browser-compat-data (H) | « Écran maintenu allumé » marche sur les iPhone à jour seulement. |
| `navigator.vibrate` absent de Safari | MDN browser-compat-data (H) | Les vibrations décidées le 09/10 ne concernent qu'Android : ne pas les compter comme un retour iPhone. |
| Cibles 44 × 44 pt minimum | Apple HIG (H) | Déjà la règle du projet. |
| Prise en main : 49 % à une main, 75 % des touchers au pouce, les prises changent souvent | Hoober 2013, A List Apart (M) | Le portrait à une main est le cas majoritaire ; les actions fréquentes vont en bas. |
| Accessibilité : permettre les deux orientations (appareil fixé sur fauteuil ou lit) | Game Accessibility Guidelines, niveau avancé (M) | Argument contre un verrou portrait **dur** par défaut. |

## Feature Landscape

Complexité : LOW (quelques heures), MEDIUM (quelques jours), HIGH (un lot entier ou plus). « Dépend de » renvoie aux fichiers existants.

### Table Stakes (Users Expect These)

#### A. Plateau téléphone (portrait)

| Feature | Why Expected | Complexity | Notes et dépendance à l'existant |
|---|---|---|---|
| Lire une carte sans la jouer, partout (plateau, main, piles, vilain, manigances) | Patron universel (Hearthstone, Arena, Gwent) | LOW | **Fait** : `CarteOuverte.tsx` + `useAppuiLong.ts`. À vérifier : aucun écran où le toucher joue directement (piège Slay the Spire). |
| Carte agrandie **entière** à l'écran, quelle que soit l'orientation, avec ses attachements | Retour Raven 7 ; Arena et Runeterra critiqués pour du texte coupé ou illisible | LOW | Fait en portrait et corrigé en paysage (959f1402). Ajouter un test de non-débordement par orientation. |
| Agrandissement prioritaire sur toute fenêtre (mulligan, question du moteur) | Retour Raven 1 | LOW | Fait (959f1402). Généraliser la règle : l'agrandissement est toujours au-dessus. |
| Feuilleter la main en grand d'un glissement | Retour Raven 2 ; c'est le « déployer la main » de Hearthstone et Arena | LOW | Fait (`voisines` dans `CarteOuverte.tsx`). |
| Voir l'autre face (héros / alter ego) sans changer de forme | Retour Raven 3 ; lire un passif est une lecture, pas une action | LOW | Fait. |
| Jamais deux cartes superposées au point de capter le doigt d'une autre | Retour Raven 4 ; plainte Runeterra (cartes qui se chevauchent) | MEDIUM | Fait par « une ligne par famille » (`bandes-portrait.ts`). Reste à garantir par un test de géométrie : aucune intersection de boîtes tactiles. |
| Jouer = toucher puis bouton (ou glisser), jamais un seul toucher | Séparer lire et agir | LOW | Fait (`MainPortrait.tsx`). |
| Sélection de cible : cibles valides mises en évidence, le reste éteint, la cible hors écran est amenée à l'écran | Arena, Hearthstone : cibles surlignées ; sur un plateau qui défile, une cible hors vue est invisible | MEDIUM | `defiler-vers-la-cible.ts` existe. À compléter : indicateur « N cibles ailleurs » sur les bandes et les onglets d'autres héros. |
| Bouton d'action principal (Fin de tour, Valider) au pouce, jamais sur la main ni sur une carte | Retour Raven 6 ; designer Snap : interactifs dans la moitié basse | MEDIUM | Corrigé en paysage (959f1402). En faire une **zone réservée** dans la mise en page plutôt qu'un bouton flottant. |
| Annuler la dernière action en un toucher | Personne ne le fait aussi bien ; indispensable avec un doigt imprécis | LOW | **Fait** : `BandeauAnnuler.tsx`. Avantage concurrentiel à garder. |
| Un héros à la fois, bascule rapide vers les autres | Aucun jeu n'affiche 4 aires sur un téléphone | LOW | **Fait** : `OngletsJoueurs.tsx`. Ajouter un badge « ce héros attend ta décision » sur l'onglet. |
| Main et piles à portée sans masquer le plateau en permanence | Main repliée de Hearthstone, Arena, Sentinels | LOW | **Fait** : `Encoche.tsx`, `MainPortrait.tsx`, `TiroirPiles.tsx`. |
| Compteurs et états lisibles à taille de plateau (PV, menace, jetons, états) | Arena : « les chiffres restent nets même quand le nom ne se lit plus » | MEDIUM | `etats.ts` (pastilles lettrées). Vérifier taille minimale des chiffres à 320 px et au niveau de texte le plus petit. |
| Zones sûres (encoche, îlot, barre d'accueil) dans les deux orientations | Arena laisse les bords latéraux libres en paysage | LOW | `env(safe-area-inset-*)` : contrôler le paysage, où l'encoche passe sur le côté. |
| Rotation sans perte d'état ni mise en page cassée | Retour Raven 6 (bouton déplacé après plusieurs rotations) ; HIG Apple | MEDIUM | Test automatisé : 5 rotations d'affilée puis contrôle des positions. |

#### B. Menus téléphone

| Feature | Why Expected | Complexity | Notes et dépendance à l'existant |
|---|---|---|---|
| Une seule colonne, rien qui déborde, cibles 44 px, de 320 à 430 px | Base | LOW | **Fait** pour accueil, galerie, campagne, éditeur, site (`ui-check/tests/pages-telephone.spec.ts`). Le **salon invité** reste à faire. |
| Assistant de préparation par étapes avec barre d'étapes et bouton Continuer en bas | Standard des parcours mobiles ; Snap, Arena gardent l'action principale en bas | MEDIUM | Décidé le 09/10, à vérifier fait ou non dans `prepare/`. |
| Feuilles basses fermables au glissement pour les détails (fiche héros, filtres, import) | Material 3, HIG : feuilles pour les tâches ponctuelles | LOW | Décidé le 09/10, `menus-mobile.css`. |
| Recherche + filtres en pastilles, grille de cartes à 3 colonnes, détail au toucher | Galeries d'Arena, Snap | LOW | Fait (zone 2). |
| Éditeur de deck utilisable d'une main : grille plein écran, deck en feuille, compteur visible | Arena et Gwent : le deckbuilder est la partie **la plus critiquée** sur téléphone (« hard to navigate », « extremely cluttered ») | MEDIUM | Décision du 09/10 gardée. C'est là qu'il faut le plus de tests réels. |
| Retour Android = étape précédente partout | Attente Android | LOW | **Fait** (`retour-android.ts`). |
| Clavier qui ne cache pas le bouton d'envoi (connexion, recherche) | Base iOS / Android | LOW | `visualViewport` ; décidé le 09/10. |

#### C. Tablette (dès 768 px)

| Feature | Why Expected | Complexity | Notes et dépendance à l'existant |
|---|---|---|---|
| Aucun survol nécessaire : aperçu au toucher, fermeture en touchant ailleurs ou par une croix | Retour iPad ; DragnCards #54 décrit le même blocage | MEDIUM | Lot T1 (`Board.tsx:1133`). |
| Aperçu et menu ensemble au premier toucher | Option a) réclamée dans DragnCards #54, décision 1 de la fiche tablette | LOW | Lot T1. |
| Détection tactile au dernier geste (iPad qui se déclare Mac) + réglage auto / toujours / jamais | iPad avec clavier-trackpad | MEDIUM | Lot T1, `useModeMobile.ts`. |
| Barre du haut et compteurs à 44 px | HIG | LOW | Lot T2. |
| Infobulles à l'appui long, raison « injouable » au toucher | Pas de survol | LOW | Lot T2. |
| `touch-action: manipulation`, pas de menu contextuel iOS sur appui long | Sinon le double-toucher zoome et l'appui long ouvre « Copier l'image » | LOW | Lot T1. |

### Differentiators (Competitive Advantage)

| Feature | Value Proposition | Complexity | Notes et dépendance à l'existant |
|---|---|---|---|
| **Paysage téléphone dérivé des bandes** (deux colonnes : rencontre à gauche, mon héros à droite) à la place du plateau PC réduit | Supprime la source des retours 6 et 7 ; respecte la règle d'accessibilité « les deux orientations » ; aucun concurrent porté n'a de portrait, aucun natif n'a de paysage | MEDIUM | `bandes-portrait.ts` est une fonction pure : la donnée est déjà là, seule la disposition change (`portrait.css`, `PlateauPortrait.tsx`). Voir la recommandation. |
| **Indicateurs de hors-champ** : pastille sur une bande ou un onglet quand une cible, une menace ou une question s'y trouve | Résout le vrai problème du découpage (ce qu'on ne voit pas) ; personne ne le fait bien | MEDIUM | `defiler-vers-la-cible.ts`, `OngletsJoueurs.tsx`. |
| **Vue d'ensemble d'une table à 4** : une bande compacte « tous les héros » (PV, état, menace engagée, nombre de cartes) au-dessus des onglets | Le coop exige de voir les partenaires ; Sentinels échoue faute de vue d'ensemble | MEDIUM | Nouveau composant, dépend d'`OngletsJoueurs`. |
| **Mots-clés expliqués dans l'agrandissement** (Riposte, Garde, Percée…) | Arena l'a, Runeterra est critiqué pour ne pas l'avoir ; règle maison : fiches dans `docs/reference/mots-cles/` | MEDIUM | `CarteOuverte.tsx` ; source des textes à décider (fiches existantes ou dictionnaire de traduction). |
| **Mode outil au doigt** pour le mode manuel (choisir « +1 dégât », toucher les cartes) | Le seul geste qui rend une manipulation libre rapide au doigt (DragnCards) | HIGH | T3 « plus tard ». Branche `mode-manuel`. |
| **Glisser vers une zone de dépôt** pour les actions fréquentes (défausser, épuiser) | Balatro : remplace des boutons trop petits | MEDIUM | Optionnel, en complément du bouton, jamais à sa place (geste caché, HIG). |
| **Barre basse de navigation** (Jouer, Campagne, Galerie, Decks, Profil) à la place du burger sur l'accueil | NN/g : la navigation cachée réduit nettement la découverte et allonge les tâches ; Material 3 : 3 à 5 destinations = barre basse | MEDIUM | **Remet en cause la décision du 09/10 (burger)** : à arbitrer avant de coder. |
| **Taille du texte à 3 niveaux** qui agit aussi sur les chiffres du plateau | Aucun concurrent ne l'offre en partie | LOW | Fait (`html[data-taille-texte]`). Vérifier les 3 niveaux × 4 largeurs × 2 orientations. |
| **Annuler 5 s** | Au-dessus de Hearthstone, Runeterra, Slay the Spire | LOW | Fait. Le mettre en avant dans les nouveautés. |

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---|---|---|---|
| Tout le plateau visible d'un coup, réduit | « Je veux tout voir » | Personne n'y arrive : cartes illisibles, cibles sous 44 px, chevauchements (constat 09/10 en paysage, retour Raven 4) | Bandes qui défilent + vue d'ensemble compacte + indicateurs de hors-champ |
| Plateau PC réduit pour le téléphone couché | Pas de seconde mise en page à écrire | Source directe des retours Raven 6 et 7 ; une troisième mise en page à tester sans la concevoir | Bandes en deux colonnes |
| Verrou portrait **dur** par défaut | Une seule orientation à tester | Impossible sur iOS sans couvrir l'écran ; exclut les appareils fixés (accessibilité) ; Raven joue couché | Verrou en option (existant), paysage dérivé par défaut |
| Lire et jouer sur le même geste (un toucher = jouer) | Plus rapide | Plainte n°1 de Slay the Spire mobile ; cartes jouées par erreur | Toucher = lire et lever, bouton ou glisser = jouer |
| Appui long comme **seul** accès à une fonction | Geste gratuit | Geste caché (HIG), et sur iOS l'appui long déclenche le menu système | Toujours un équivalent visible ; l'appui long reste un raccourci |
| Glisser-déposer obligatoire | Sensation « carte physique » | Imprécis, bogues de dépôt (DragnCards #53), inaccessible | Toucher-cible-valider, le glisser en bonus |
| Une 3e mise en page « tablette » dédiée | Écran intermédiaire | Coût de test triplé ; décision de la fiche tablette : non | Plateau PC rendu tactile |
| Vibrations comme seul retour d'un moment clé | Décidé le 09/10 | Rien sur iPhone (pas de `vibrate` dans Safari) | Retour visuel toujours, vibration en plus sur Android |
| Tchat sur téléphone | Coop en ligne | Hors périmètre décidé ; le clavier mange la moitié de l'écran | Pings ou émotes plus tard si besoin |
| Animations longues à chaque carte | « Ça fait jeu mobile » | Ralentit un tour déjà long (coop 4 héros), coûte de la batterie | Animations courtes, coupées en sobre (décidé) |

## Feature Dependencies

```
Décision d'orientation (portrait seul / dérivé / les deux)
    └──conditionne──> Paysage téléphone en deux colonnes
    └──conditionne──> Zone réservée du bouton d'action (une par orientation)
    └──conditionne──> Tests de rotation

bandes-portrait.ts (fonction pure, une ligne par famille)
    └──alimente──> Plateau portrait (existant)
    └──alimente──> Paysage en deux colonnes (nouveau)
    └──alimente──> Indicateurs de hors-champ

OngletsJoueurs.tsx ──enrichi par──> Vue d'ensemble des héros ──enrichie par──> badges « attend ta décision »

CarteOuverte.tsx ──enrichi par──> Mots-clés expliqués
                 ──réutilisé par──> Tablette (voisines, autre face) après T1

Lot T1 tablette (détection, fermeture d'aperçu) ──requis par──> Lot T2 (44 px, infobulles)
                                                ──requis par──> Mode outil au doigt (T3)

Barre basse de navigation ──conflit──> En-tête burger du 09/10 (choisir l'un)
Verrou portrait dur par défaut ──conflit──> Paysage dérivé
```

### Dependency Notes

- **L'orientation se décide avant de toucher au plateau** : elle fixe où vit le bouton d'action et si `PlateauMobile.tsx` garde son aiguillage vers le plateau PC réduit pour un téléphone couché (commentaire d'en-tête : « un telephone couche plus large prend le plateau PC reduit »).
- **Le paysage dérivé dépend de `bandes-portrait.ts`** : la répartition par famille (retour Raven 4) est déjà faite côté données ; seule la disposition change. C'est pourquoi le coût est MEDIUM et pas HIGH.
- **La tablette réutilise les gestes du téléphone** (décision 12/10) : feuilleter la main et voir l'autre face doivent être sortis de `board/mobile/` vers un module partagé avant d'être branchés sur `Board.tsx`.
- **Le mode outil dépend de T1** : sans détection tactile fiable, on ne sait pas quand proposer la barre d'outils.
- **Menus et plateau sont indépendants** : la refonte des menus peut avancer en parallèle, sauf le salon invité qui partage l'assistant.

## MVP Definition

### Launch With (v1.1)

- [ ] Décision d'orientation écrite dans PROJECT.md, avec les mesures ci-dessous faites avant de coder le plateau
- [ ] Tablette T1 + T2 (aperçu sans survol, 44 px, détection au dernier geste)
- [ ] Plateau portrait consolidé : test de non-chevauchement des boîtes tactiles, zone réservée du bouton d'action, test de rotation répétée
- [ ] Paysage téléphone sur les bandes (deux colonnes) en remplacement du plateau PC réduit, verrou portrait gardé en option
- [ ] Indicateurs de hors-champ pour les cibles et les questions (bandes et onglets)
- [ ] Salon invité au format de l'assistant (seule page de menus non faite)
- [ ] Éditeur de deck testé à 320 px par un vrai joueur (point faible connu de tous les concurrents)

### Add After Validation (v1.x)

- [ ] Vue d'ensemble des héros en coop à 3 ou 4 : dès qu'une partie à 4 sur téléphone est signalée difficile
- [ ] Mots-clés expliqués dans l'agrandissement : dès qu'un joueur demande ce que fait un mot-clé
- [ ] Barre basse de navigation : si l'arbitrage burger / barre la retient
- [ ] Glisser vers zone de dépôt : si les mesures montrent beaucoup de touchers pour défausser ou épuiser

### Future Consideration (v2+)

- [ ] Mode outil au doigt (T3, mode manuel) : attend la branche `mode-manuel`
- [ ] Pings ou émotes coop : seulement si le tchat reste exclu et que les joueurs en ligne en ont besoin

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---|---|---|---|
| Tablette T1 (sans survol, fermeture d'aperçu, détection) | HIGH | MEDIUM | P1 |
| Tablette T2 (44 px, infobulles, raison injouable) | HIGH | LOW | P1 |
| Non-chevauchement garanti par test (portrait) | HIGH | LOW | P1 |
| Zone réservée du bouton d'action | HIGH | MEDIUM | P1 |
| Paysage en deux colonnes (bandes) | HIGH | MEDIUM | P1 |
| Indicateurs de hors-champ | HIGH | MEDIUM | P1 |
| Salon invité | MEDIUM | MEDIUM | P1 |
| Test de rotation répétée | MEDIUM | LOW | P1 |
| Vue d'ensemble des héros | MEDIUM | MEDIUM | P2 |
| Mots-clés dans l'agrandissement | MEDIUM | MEDIUM | P2 |
| Barre basse de navigation | MEDIUM | MEDIUM | P2 (à arbitrer) |
| Glisser vers zone de dépôt | LOW | MEDIUM | P3 |
| Mode outil au doigt | MEDIUM | HIGH | P3 |

## Competitor Feature Analysis

| Feature | Marvel Snap | Hearthstone / Arena / Runeterra | DragnCards | Notre approche |
|---|---|---|---|---|
| Orientation | Portrait, règles taillées pour l'écran | Paysage, portage du PC | Paysage navigateur | Portrait conçu, paysage dérivé des mêmes bandes |
| Plateau dense | Petit par règle | Défilement latéral (Arena), limites de règles | Plateau PC entier | Bandes qui défilent, une ligne par famille, un héros par onglet |
| Inspection | Toucher | Appui long / toucher | Toucher = grande image | Toucher = carte en grand, voisines, autre face |
| Cible | Peu de ciblage | Flèche glissée, cibles surlignées | Outil puis carte | Cibles surlignées + défilement vers la cible + indicateurs hors-champ |
| Jouer | Glisser | Déployer la main puis glisser | Glisser | Toucher puis bouton Jouer |
| Main | Toujours visible | Repliée dans un coin | Rangée PC | Feuille derrière l'encoche |
| Retour arrière | Dans le tour | Aucun ou presque | Annuler du moteur | Bandeau Annuler 5 s |
| Menus | Barre basse | Hub central / barre | Pages web | En-tête burger (09/10), barre basse à arbitrer |

## Recommandation : l'orientation de la partie sur téléphone

**Verdict : portrait d'abord, paysage dérivé. Concrètement :**

1. **Le portrait est la seule mise en page conçue, testée et validée** pour le plateau téléphone (moins de 768 px de large). Toute fonctionnalité naît en portrait.
2. **En paysage, un téléphone ne reçoit plus le plateau PC réduit** mais les **mêmes bandes en deux colonnes** : à gauche le côté rencontre (vilain, manigances, engagés), à droite mon côté (héros et alliés, soutiens, améliorations), chaque colonne défilant verticalement ; main et piles restent derrière leurs encoches ; le bouton d'action a sa zone réservée en bas à droite, hors des colonnes.
3. **Le verrou portrait reste une option** (`EcranTourne.tsx`), jamais le défaut.
4. **Tablette (768 px et plus) : plateau PC tactile**, dans les deux orientations, comme décidé le 12/10.

**Pourquoi :**

- **La densité utile est la même dans les deux sens.** Calcul indicatif, à mesurer : iPhone de 393 × 852 px CSS. En portrait avec la barre Safari, environ 393 × 660 utiles : 3 cartes de ~115 × 160 px par rangée, ~4 bandes visibles, soit ~12 cartes. En paysage, environ 760 × 340 utiles (encoche et barre déduites) : 2 rangées de cartes de ~100 × 140, 7 par rangée, soit ~14 cartes, mais **sans place pour la main, le bouton ni les onglets** sans recouvrir une rangée. Le paysage ne gagne rien de décisif et perd la bande basse où vivent les actions.
- **Les règles de Marvel Champions sont des rangées qui débordent.** Une rangée qui défile horizontalement dans une bande (le principe des bandes, et le défilement latéral d'Arena) se lit mieux qu'un plateau PC réduit dont tout rapetisse.
- **Le jeu à une main est le cas majoritaire** (49 % de prise à une main, 75 % des touchers au pouce, Hoober) ; c'est l'argument explicite de Snap.
- **Les jeux en paysage le sont parce qu'ils sont des portages** d'un plateau PC figé dans un moteur natif. Ici, le moteur d'affichage est déjà séparé en données pures (`bandes-portrait.ts`) : on peut avoir les deux sans écrire deux plateaux.
- **On ne peut pas interdire le paysage sur iPhone** (pas de verrou ni de manifeste dans Safari), et Raven joue couché : il faut donc que le paysage soit jouable. Le plateau PC réduit a prouvé qu'il ne l'est pas (retours 6 et 7, constat du 09/10 « une seule bande à la fois, la main ouverte couvre presque tout »).
- **La base existante est validée** par un vrai joueur : « C'est excellent pour le moment sur téléphone » (Raven, en portrait).

**Ce qu'il faut mesurer pour confirmer (avant le lot plateau) :**

| Mesure | Comment | Seuil qui confirme |
|---|---|---|
| Cartes visibles à taille lisible (chiffres ≥ 12 px, carte ≥ 96 px de large) | Playwright sur une partie de référence à 4 héros, en 360 × 640, 390 × 664 (iPhone avec Safari), 430 × 740, et leurs paysages réels (barre déduite) | Portrait ≥ paysage à ±2 cartes : la densité ne tranche pas, l'ergonomie décide |
| Touchers pour un tour type (jouer un allié, attaquer un sbire, défendre, fin de tour) | Script Playwright qui compte les gestes, dans chaque orientation | Paysage dérivé ≤ portrait + 1 toucher, sinon le garder au rang de secours |
| Défilements et changements d'onglet par tour à 4 héros | Même script | Moins de 3 par tour en portrait avec indicateurs hors-champ |
| Part réelle des parties jouées couché | Compteur anonyme de l'orientation au début et toutes les 5 min d'une partie téléphone (journal serveur, sans donnée personnelle) | Si moins de 10 %, le paysage dérivé descend en P2 ; si plus de 30 %, il mérite les mêmes tests que le portrait |
| Recours au bandeau Annuler dans les 5 s | Même compteur | Un taux qui baisse après la refonte = moins de touchers ratés |
| Retour qualitatif | Raven + 2 joueurs, une partie dans chaque orientation, une question : « laquelle reprendrais-tu ? » | Choix concordant |

## Confidence & Gaps

| Point | Confiance | Raison |
|---|---|---|
| Contraintes navigateur iOS / Android | HIGH | Données de compatibilité MDN lues directement |
| Orientation de Snap et ses raisons | HIGH | Déclaration de Ben Brode rapportée par Out of Games |
| Orientation des portages (Hearthstone, Arena, Runeterra, Slay the Spire, Balatro) | HIGH à MEDIUM | Plusieurs revues concordantes |
| Gwent et Sentinels sur téléphone | LOW | Résumés de recherche contradictoires, revues inaccessibles (403) |
| Gestes précis de Snap (reprise d'une carte, toucher pour lire) | LOW | Connaissance non vérifiée sur source cette session |
| DragnCards (mode tactile, barre d'outils) | HIGH | Code source et issues GitHub lus |
| Chiffres de densité portrait / paysage | LOW | Calcul indicatif, à remplacer par la mesure ci-dessus |

**Gaps :**
- Aucune capture de jeu n'a été ouverte directement : les descriptions viennent de revues. Une passe visuelle sur les captures App Store de Snap, Arena et Sentinels lèverait les doutes LOW.
- L'état réel de l'assistant de préparation et du salon invité sur téléphone n'a pas été vérifié dans le code pour cette fiche.
- Le point d'arbitrage burger contre barre basse n'est appuyé que par des études génériques (NN/g), pas par un jeu de cartes.

## Sources

- Out of Games, conseils de Ben Brode et de l'équipe Snap (portrait, 3 min) : https://outof.games/news/6233-ben-brode-marvel-snap-devs-provide-game-design-tips-for-mobile-gaming/ (H)
- Tiffany Smart, UI de Marvel Snap (interactifs dans la moitié basse, cartes d'abord) : https://www.tiffanysmart.com/work/marvel-snap (M)
- Hearthstone sur téléphone, main dans le coin, appui long : https://illgaming.net/hearthstone-for-mobile-phones-how-does-it-hold-up/ et https://www.kitguru.net/gaming/apps-software/matthew-wilson/hearthstone-has-finally-arrived-for-smartphones/ (M) ; problème de détection téléphone / tablette : https://us.forums.blizzard.com/en/hearthstone/t/mobile-ui-on-a-large-phone/1729 (M)
- Magic Arena mobile : https://draftsim.com/mtg-arena-mobile/ (défilement latéral, pile envahissante, illustration plutôt que nom), https://www.cbr.com/magic-arena-ios-review/ (texte au toucher, mots-clés, deckbuilder difficile), synthèse https://github.com/iftheshoefritz/webula/issues/191 (M)
- Legends of Runeterra mobile, main en coin et lisibilité : https://noisypixel.net/legends-of-runeterra-review-ios-android/ (M, via résumé)
- Slay the Spire mobile : https://www.thesixthaxis.com/2021/03/03/slay-the-spire-mobile-review/ (M)
- Balatro mobile, zones de dépôt, paysage : https://www.shacknews.com/article/141549/balatro-mobile-impressions (M) ; portrait absent : https://github.com/beiklive/balatro-portrait-mobile (M)
- Gwent mobile, plateau à l'étroit : https://www.thegamer.com/gwent-best-worst-things-mobile-version/ (M) ; orientation non confirmée (LOW)
- Spirit Island digital : https://www.pixelatedcardboard.com/spirit-island-review/ et https://8bitmeeple.com/review/spirit-island/ (M, via résumé)
- Sentinels of the Multiverse digital : https://boardgamegeek.com/blogpost/41189/review-roundup-sentinels-multiverse-rook-city-and (LOW, page 403, résumé seulement)
- Arkham Cards (compagnon Arkham Horror LCG) : https://arkhamcards.com/ (H)
- LotR Adventure Card Game sans version mobile : https://steamcommunity.com/app/509580/discussions/0/1732090362039717022/ (M)
- DragnCards : code `frontend/src/features/engine/TouchBarBottom.js`, `hooks/useHandleTouchAction.js`, `TouchModePrompt.js` de https://github.com/seastan/dragncards ; issues #53, #54, #55, #159, #161, #162 ; https://github.com/hone/dragncards-mc-plugin/issues/95 (H)
- MDN browser-compat-data (`ScreenOrientation.lock`, manifeste `orientation`, `Element.requestFullscreen`, `WakeLock`, `Navigator.vibrate`) : https://github.com/mdn/browser-compat-data (H)
- Apple, Designing for games / HIG (44 pt, deux orientations, gestes cachés) : https://developer.apple.com/design/human-interface-guidelines/designing-for-games (M, page lue via résumé)
- Steven Hoober, prise en main : https://alistapart.com/article/how-we-hold-our-gadgets/ (M)
- Game Accessibility Guidelines, les deux orientations : https://gameaccessibilityguidelines.com/allow-play-in-both-landscape-and-portrait/ (M)
- NN/g, navigation cachée : https://www.nngroup.com/articles/hamburger-menus/ (M) ; Material 3 barre de navigation : https://m3.material.io/components/navigation-bar/guidelines (M)

---
*Feature research for : Marvel Champions LCG, jalon v1.1 Tablette et téléphone*
*Researched : 13/10/2026*

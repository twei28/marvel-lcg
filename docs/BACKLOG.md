# Backlog

Les chantiers décidés ou envisagés, pas encore faits. Une entrée par sujet : ce qu'on veut, ce qu'on a mesuré,
les options, et ce qui reste à trancher. Quand un sujet est fait, on le raye ici et on renvoie vers son commit ou
sa documentation.

---

## Outil de traduction autonome dans MC Creator (mis en pause le 04/11/2026)

**Le besoin.** Des traducteurs externes (FR ou toute autre langue) veulent produire leurs propres images de cartes
traduites, à partir d'un scan anglais, SANS dépendre des traductions déjà faites dans le jeu ni du catalogue
(pas de `card_id`, pas de `textes-fr-fanmade.ts`). Deux exigences fermes posées par l'utilisateur en cours de
route : (1) l'effacement du texte anglais doit être RÉEL (le vrai algorithme `effacer-texte.ts`, pas une boîte
grise plaquée — une première tentative en artefact Claude autonome a été jugée « dégueulasse » et abandonnée),
(2) l'outil doit pouvoir s'ouvrir en un seul fichier HTML, en double-cliquant dessus (`file://`), sans serveur.

**Ce qui existe, non commité** (`git status` : rien n'est indexé) :
- `Fusion/marvel-lcg-src/public/createur-cartes/traduction.html` + `.js` — la page, servie dans MC Creator.
  Fonctionne avec un serveur statique (`python3 -m http.server` depuis `public/`).
- `Fusion/marvel-lcg-src/public/createur-cartes/effacer-texte.js` — port JS vanilla fidèle de
  `ui-app/src/board/effacer-texte.ts` (logique inchangée, juste les types retirés).
- `Fusion/marvel-lcg-src/public/createur-cartes/detecter-zone.js` — port JS vanilla fidèle de la détection de
  zone de `ui-app/src/board/traduction-posee.ts`.
- `Fusion/marvel-lcg-src/public/createur-cartes/stockage-traduction.js` — persistance IndexedDB dédiée
  (base séparée des projets de cartes normaux).
- `Fusion/marvel-lcg-src/public/createur-cartes/traduction-autonome.html` — version à fichier unique (polices en
  base64, tout le JS inliné), **OBSOLÈTE** : date du 04/11 16:43, alors que le dernier correctif de
  `traduction.js` (option `gommes`, voir plus bas) a été écrit à 16:51 et n'a jamais été regénéré dedans.
  **Relancer `node Fusion/marvel-lcg-src/tools/createur-cartes/construire-traduction-autonome.mjs` avant
  toute reprise.**
- `Fusion/marvel-lcg-src/tools/createur-cartes/construire-traduction-autonome.mjs` — le script qui regénère le
  fichier ci-dessus (concatène le JS, encode les polices utilisées par `polices.js` en base64, inline
  `donnees/types.json`).
- `Fusion/marvel-lcg-src/public/createur-cartes.html` — modifié (1 ligne : lien « Traduction » ajouté au bandeau
  d'accueil).

**Zones gérées** (chacune : détection automatique + rectangle ajustable à la main + effacement réel +
saisie libre multilingue, pré-remplie en FR officiel modifiable) : texte de règles (fiable, vérifié sur tous
les types de carte testés), titre de la carte, libellé du type imprimé, badges de stats (THW→CTR, ATK→ATQ,
DEF, REC, selon ce que le type a réellement), bande « Taille de main / Points de vie » (identité/alter-ego
seulement). Export PNG individuel + zip global ; sauvegarde locale persistante (IndexedDB) entre deux visites.

**Ce qui restait FAUX au moment de l'arrêt**, cause trouvée mais correctif non entièrement revérifié :
- Le titre pouvait doubler avec l'anglais dessous sur certains scans (ex. `01001a.jpg` Spider-Man) : l'algorithme
  de regroupement en lignes de `effacer-texte.ts` coupait au trait d'union de « SPIDER-MAN », n'effaçant que
  « SPIDER ». Les badges THW/ATK/DEF pouvaient ne rien effacer du tout sur ce même scan (échec de reconnaissance
  sur des mini-rectangles, pas une limite de résolution). **Correctif écrit** : pour les zones étroites
  (titre/type/badges/main), passer tout le rectangle en `gommes` à `effacerTexte` (efface toute encre dans le
  rectangle, sans dépendre de la reconnaissance en lignes) au lieu de la détection fine. Un seul test après ce
  correctif (Spider-Man) montrait les 7 zones « effacé » et un zoom propre sur titre+ATQ — **pas revérifié sur
  les 6 autres combinaisons zone/scan avant l'arrêt**, ni régénéré dans le fichier autonome.

**À faire pour reprendre proprement** :
1. Régénérer `traduction-autonome.html` avec le script (dernier correctif `gommes` non inclus dedans).
2. Revérifier par EXPORT PNG (pas par l'aperçu en cours d'édition — c'est ce qui a fait annoncer un correctif
   qui ne marchait pas, deux fois de suite) : titre, type, les 3-4 badges, bande main/PV, sur au moins 3 scans
   `identity`/`alter-ego` réels, zoomés, en comparant au scan officiel d'origine.
3. Vérifier la cohérence centrage/alignement par TYPE (mesuré sur de vrais scans officiels, jamais sur la
   métadonnée `types.json` qui s'est révélée fausse pour la police/couleur de ces mêmes éléments) : `ally` =
   aligné à gauche (confirmé sur 3 scans), `identity`/`alter-ego` = centré (confirmé sur la référence FR
   Cyclope) — probablement vrai aussi pour les autres types, à vérifier au cas par cas avant d'étendre.
4. Repasser un œil sur les libellés de type et d'abréviations de stats : dérivés des MOTS RÉELLEMENT IMPRIMÉS
   sur de vrais scans (HÉROS, ALTER EGO sans trait d'union, CTR, ATQ...), pas du nom de menu de MC Creator
   (`app.js`, table `NOMS`) qui a été utilisé par erreur une première fois.

---

## 3. Une « barre d'avantage » sur le plateau, comme aux échecs (ajouté le 22/10/2026)

> **FAIT le 22/10/2026 (version 1, formule simple)** : l'utilisateur a donné son go après la maquette. Code : `ui-app/src/board/barre-avantage.ts` (formule pure, 6 tests),
> `BarreAvantage.tsx` + `barre-avantage.css` (barre de 7 px au bord gauche, détail au survol), `barre-avantage-reglage.ts` et `LigneBarreAvantage` dans `FenetreReglages.tsx`
> (option **désactivée par défaut**, clé `mc_barre_avantage`). **Pas encore fait** : les fiches réglage par scénario atypique ; la calibration des poids sur de vraies parties
> (seuils 0,4 et 0,6, 12 tours « confortables »). Vérifié sur Rhino en navigateur : absente par défaut, présente une fois activée, repart quand on la désactive.

**L'idée de l'utilisateur.** Dans les programmes d'échecs, une barre verticale sur le côté monte ou descend selon qui a l'avantage. Il voudrait
l'équivalent pour Marvel Champions : une barre qui dit, au fil de la partie, si **les héros** ou **le méchant** ont l'avantage.

**Ce que ce n'est pas.** Aux échecs, un moteur calcule les coups à l'avance, information complète. Ici : jeu coopératif, decks cachés et mélangés, hasard
(cartes de rencontre, boosts), choix très nombreux. **On ne peut pas calculer « qui gagne » : on ne peut que l'ESTIMER.** La barre doit s'appeler
« estimation » et ne jamais prétendre être une probabilité exacte.

**Ce que la barre montre.** Héros contre méchant (pas blanc contre noir). Haut = les héros dominent ; bas = le méchant va gagner. En Normal (ex-Épuré),
une barre verticale sur un côté du plateau, à l'allure du reste (panneau bleu, coins coupés de 6 px). **Au survol : le détail**, par exemple
« 2 tours avant la défaite · méchant à 40 % ». **Une option dans les Réglages pour la cacher.** Pas sur téléphone (le projet ne travaille que sur PC).

### Les trois approches, de la moins chère à la plus chère

1. **Indicateur par formule (recommandé si on s'y met).** Une fonction pure qui lit l'état du jeu (`/get_world`, le même que le plateau lit déjà) et rend un
   nombre de -1 à +1 plus ses raisons. Entrées utiles : menace sur la manigance par rapport à son seuil et accélération (= tours avant la défaite) ; PV restants du
   méchant, stade ; PV des héros (identités) ; sbires engagés et leur menace ; taille de la main, alliés en jeu ; phase du tour. Instantané, expliquable, testable avec
   les parties du bac à sable. Ne donne PAS une probabilité de victoire : dit si la partie « tourne mal ».
2. **Simulation (Monte-Carlo).** Copier l'état du moteur, rejouer des centaines de fins de partie avec des pioches tirées au hasard, compter les victoires. Plus juste,
   mais : coût de calcul, copie d'état du moteur à vérifier (est-elle possible et rapide ?), et il faut un **pilote** qui joue correctement pour simuler (il existe un
   pilote de test dans `ui-check/pilote-*.ts`, à évaluer, pas fait pour ça).
3. **Modèle appris** sur des parties jouées (historique des parties, statistiques). Le plus précis, mais exige beaucoup de données et de travail : à écarter sauf
   si 1 et 2 ne suffisent pas.

### Valable pour tous les scénarios ?

**Oui pour une version générale, non pour une version exacte partout.** Presque tous les scénarios ont une manigance principale avec seuil de menace, un méchant avec des
PV, des héros avec des PV : le **cœur de la formule est universel** (course « tours avant la défaite » contre « dégâts avant la victoire »).

**Ce qui casse la formule générale** (cas atypiques) : conditions de victoire ou de défaite inhabituelles (ex. *La ville ne dort jamais* : deux pistes pour passer le stade 1,
méchants qui remettent leurs PV à zéro quand on les « bat », victoire en battant le Gunrunner ; scénarios officiels où l'on gagne autrement qu'en battant le méchant) ;
mécaniques propres (Punisher qui attaque le sous-méchant, pods multi-groupes de Kingsfall) ; mode campagne et multijoueur.

### Architecture envisagée (décision de l'utilisateur, 22/10/2026)

- **Une formule de base générale** qui marche partout (approche 1).
- **Une « fiche réglage » par scénario atypique, seulement pour eux** : quelques lignes qui REMPLACENT la partie qui ne convient pas (« ici le danger, c'est le nombre
  de pistes qui manquent » ; « on gagne en battant le Gunrunner, pas le CAPO »). Elle ne refait pas toute la formule. Comme pour les cartes : la plupart suivent les
  règles du jeu, seules celles à effet inhabituel ont un traitement à part.
- **Un repli honnête** : si le scénario n'est pas connu et ne ressemble pas au cas général, afficher « **estimation indisponible** » plutôt qu'un chiffre faux. C'est aussi
  le repli des scénarios sur mesure ajoutés plus tard, tant qu'on n'a pas écrit leur fiche.

### Estimation du travail (à confirmer)

Approche 1 : une fonction pure + son test + un petit composant de barre + une option dans `FenetreReglages.tsx` + une maquette HTML sur le vrai plateau avant de coder
(comme celle de `docs/packs/mcdc-2026-punisher/maquette-ville.html`). Les fiches des scénarios atypiques viennent après, au cas par cas.

### Décisions de l'utilisateur (22/10/2026), questions une à une

1. **Approche : formule simple** (l'approche 1), avec fiches réglage pour les scénarios atypiques.
2. **Affichage : la barre seule, le détail au survol** (pas de nombre permanent, pour ne pas la faire passer pour une probabilité).
3. **Modes : solo et coop.** Pas de barre en Bataille 1v1 (deux camps, autre logique) ni en mode manuel.
4. **Place : le bord gauche**, fine barre verticale, sans gêner le journal ni la mini-carte de La Ville à droite.

**Reste à faire le jour où on s'y met :** une maquette HTML sur le vrai plateau (comme celle de La Ville) pour juger l'effet, puis la fonction pure + test,
le composant de barre, l'option « cacher » dans les Réglages. Détail de ce que fait le bac à sable pour tester : parties de la section « bac à sable » de
`docs/README.md`. Rien n'est commencé.

### Vérification des données disponibles (22/10/2026, lecture seule, rien codé)

Lu dans `ui-app/src/board/world.ts` (le type `World`, ce que le moteur envoie au plateau) et dans les usages du plateau. **Les chiffres dont la formule a besoin existent déjà** :
- **Menace de la manigance** : `info.k_threat` (menace posée), `info.target_threat` (seuil), `info.k_acceleration_token` (jetons d'accélération), `info.acceleration_icon`,
  `info.crisis` ; les faits de phase du méchant portent aussi `restant`, `plafond`, `escalade`, `acceleration`, `joueurs` (type `FaitMenace`).
- **PV** : `info.health` et `info.max_health` sur chaque carte (méchant, sbires, identités) ; `info.is_infinite_health` pour les PV infinis.
- **Autour** : `hand_size` du joueur, `allies`, `supports`, `area_hero`, `dealt_encounter_cards`, `bind_object_id` (cartes attachées), `info.victory`.
- **Limites** : le moteur local n'était pas lancé ce jour-là, donc **non testé sur une partie vivante** ; à confirmer au premier essai (sur Rhino, puis sur un scénario atypique). Les compteurs propres à un
  scénario (pistes, jetons « recherché », etc.) sont dans `info` sous des clés variables : c'est là que les fiches réglage devront aller les lire.

### Maquette (faite le 22/10/2026)

`docs/maquettes/barre-avantage.html` : une barre fine au bord gauche sur une capture réelle du plateau en Normal ; le survol donne le détail ; quatre états (équilibrée, les héros
dominent, la partie tourne mal, scénario inconnu) et trois curseurs pour essayer à la main (formule fictive : moyenne de trois valeurs, juste pour juger l'allure).
**Constat de la maquette** : à 22 px de large la barre frôlait la **pile de cartes de gauche** ; l'utilisateur l'a voulue **beaucoup plus fine** (7 px sur un plateau de 1440 px) : elle ne touche plus la pile, pas de marge à ajouter.

---

## 4. La barre d'adresse dans l'appli installée, sur la page d'une table (ajouté le 22/10/2026)

> **RETIRÉ le 23/10/2026, décision de l'utilisateur : déjà traité.** Ce n'était pas un défaut du plateau (voir la cause ci-dessous) ; rien n'a été changé dans le code.

**Le signalement (Yarro, 22/10/2026).** Dans l'appli installée (Chrome « Installer l'application »), une fine barre apparaît en haut du plateau : une croix, l'adresse
`https://p9.narwhalchampions.com` et le titre « Board - Marvel Champions ». Les autres applis (Dragn Cards…) n'ont pas ça. Contournement connu : passer en mode web puis plein écran (F11).

**La cause (vérifiée dans le code et le manifeste servi en ligne).** `site/orchestrateur.py` (`MANIFESTE_APPLI`) déclare l'appli pour `narwhalchampions.com` : `scope: "/"`,
`start_url: "/entrer"`. La table, elle, est servie sur `p<N>.narwhalchampions.com`, un AUTRE site pour le navigateur : hors du périmètre de l'appli, Chrome affiche sa barre de
sécurité. **Le code le dit déjà** (commentaire « Contrepartie assumée : une fois sur la table, le navigateur garde une fine barre d'adresse »). La barre n'est donc pas un défaut du plateau.

**Pourquoi un sous-domaine par table (docstring en tête de `orchestrateur.py`).** Le client du jeu utilise des chemins ABSOLUS (`/ws`, `/save_deck`, `/app/board.html`...) : environ
**164 routes** côté moteur. Les servir sous `narwhalchampions.com/partie3/` les ferait partir à la racine du site. Le routage est statique dans Caddy (`p1..p30` → ports 2351..2380).

### Les voies examinées

1. **Table sous un chemin du même domaine** (`narwhalchampions.com/p9/...`) : la « vraie » solution, mais il faut réécrire les ~164 appels absolus du client (JS de `public/`, plateau React
   `ui-app/`, WebSocket) ou les réécrire en Caddy. **Gros chantier, risque élevé** (invitations, spectateurs, activité Discord, clés de siège dans les URL).
2. **Même domaine, table choisie par cookie dans Caddy** (les chemins restent à la racine ; un cookie `table=N`, posé par l'orchestrateur, envoie les routes du moteur vers le bon port).
   Contre : collisions avec les routes du site (`/`, `/admin`, `/entrer`...), **une seule table par navigateur** (l'admin ne pourrait plus en regarder une autre en jouant), invités et
   spectateurs à revoir. **Chantier moyen à gros, risque moyen.**
3. **Appli installée sur la table, pas sur le site** (un manifeste servi par chaque `p<N>`, `start_url` sur sa propre adresse). Contre : l'appli est liée à UNE adresse ; la table est
   éteinte quand personne ne joue (l'appli afficherait une erreur au lieu d'allumer la table : à contourner côté Caddy en renvoyant vers `/entrer`, qui fait sortir du périmètre une
   seconde), et le cookie de site ne voyage pas jusqu'à `p<N>` (connexion à repenser). **Chantier moyen, plusieurs inconnues.**
4. **`scope_extensions`** (le périmètre de l'appli étendu aux sous-domaines, `"origin": "https://*.narwhalchampions.com"` + fichier `/.well-known/web-app-origin-association`) : la voie
   propre sans toucher au routage, MAIS d'après la documentation Chrome (page de décembre 2023) c'était un essai (« origin trial ») **sans Android** et seulement sur ordinateur ;
   son état actuel est inconnu. À revérifier avant de s'y fier. **Petit chantier si ça marche, à tester sur un vrai Chrome installé.**
5. **Ne rien changer, et le dire** : garder le contournement (mode web + plein écran) et l'expliquer dans la FAQ / les nouveautés.

### À décider avant de coder

- Quelle voie (recommandation provisoire : tester 4 d'abord, c'est le seul test peu coûteux ; sinon 5, puis 2 si l'utilisateur veut vraiment supprimer la barre).
- Sur ordinateur seulement, ou aussi sur téléphone ? (4 ne couvre pas le téléphone.)
- Rien n'a été codé.

---

## 7. ~~Cartes manquantes de Wasp (Hank Pym) : Shadow of the Past et Pursued by the Past~~ (RÉSOLU le 26/10/2026)

> **Résolu le 26/10/2026 : cette entrée reposait sur une erreur.** Ces deux cartes ne manquaient pas : ce sont des cartes officielles
> déjà présentes dans le moteur, Shadow of the Past `01190` (set Standard) et Pursued by the Past `45075a/b` (Standard III).
> `hp013` est maintenant branché dessus (5 compteurs : recherche de `01190` dans le deck rencontre et sa défausse, sinon 7 compteurs
> `pursuit` sur `45075a` s'il est en jeu), avec 8 cas verts : voir `docs/packs/wasp-hank-pym/GABARITS.md` (« Corrections du 26/10/2026 »)
> et `docs/reference/mots-cles/find.md`. **Rien à faire ici.** Le texte ci-dessous est conservé pour mémoire seulement.

**Décision de l'utilisateur (26/10/2026) : coder pour l'instant sans ces deux cartes, et noter ici qu'il faut les trouver pour finir.**
L'obligation `hp013` Identity Crisis (pack `wasp_hank_pym`, préfixe `hp`, auteur JackHKP) dit : à 5 compteurs crise,
« find Shadow of the Past and reveal it. If you cannot, place 7 pursuit counters on Pursued by the Past ». Ces deux cartes ne sont
pas dans le zip `Wasp-20261025T195548Z-1-001.zip`. Aujourd'hui : on compte les compteurs crise et rien ne se révèle à 5 ;
l'obligation reste jouable. À faire : retrouver les deux cartes auprès de l'auteur (scans ou texte), les ajouter au pack
(`docs/reference/PROCESSUS-CARTE.md`) et brancher `hp013` dessus (gabarit `docs/packs/wasp-hank-pym/GABARITS.md`).

---

## 8. Problèmes trouvés le 26/10/2026

Liste vivante, à cocher au fur et à mesure : `docs/rapports/2026-10-26-problemes-a-corriger.md`.

---

## 9. Campagnes fan-made EN PAUSE (mise au backlog le 26/10/2026, à la demande de l'utilisateur : « on reprendra ça une autre fois »)

**Décisions prises**
- Seules les campagnes COMPLÈTES (livret + carnet) sont faites : **Hellfire Hunt** (Dipsome) d'abord, puis **Hydra Unleashed** (Lord Havok).
- **Schemes of the Shi'ar** (équipe Starjammers, WIP dans le zip Starjammers) : **abandonnée** (ni livret ni carnet).
- **Mockingbird** (héros d'Hydra) : cartes absentes du zip ; à chercher si le temps le permet, **non bloquant** (Hydra se joue avec U.S. Agent seul).
- **Dé à 6 faces d'Hydra God** (scénario 5) : un randomizer cliquable avec un petit D6 animé qui montre le résultat ; tirage enregistré côté moteur (rejouable et partagé en multijoueur).
- **FAQ vide d'Hydra** : ignorée, les doutes se tranchent par les règles et le livret.
- **Squirrel Girl** : homebrew de l'utilisateur, hors périmètre de test.

**Où est le travail**
- Branche git **`campagnes-fanmade`**, dans un dossier séparé (git worktree) : `/home/oem/Desktop/Marvel-LCG-campagnes`. Dernier commit : `3f4b215e` (« wip(campagne) »). ⚠ **Ne pas supprimer ce dossier** : il contient aussi 90 images `hf*.jpg` (réelles, non versionnées) et des liens vers les images, le venv et node_modules du dossier principal.
- Le dossier principal (`gs7-earth-under-siege`) ne contient AUCUNE ligne de campagne.
- Pour recréer le dossier : `git worktree add ../Marvel-LCG-campagnes campagnes-fanmade`, puis relier `assets/pics*` (`cp -as`), `assets/cache`, `assets/docs`, `data/marvelcdb`, `public/stories`, `.venv-linux`, `ui-app/node_modules`, `ui-check/node_modules`, et recréer `.game-src` (liens vers src, data, deck, assets, public + build.py, game_entry.py, launch.json, main.py, winsound.py). Les images `hf*` se régénèrent depuis le zip avec `tools/importer_images_hellfire_hunt.py` ; les cartes avec `tools/importer_cartes_hellfire_hunt.py`.
- Avant de reprendre : `git -C ../Marvel-LCG-campagnes merge gs7-earth-under-siege` (la branche de campagne est en retard sur le principal).

**Ce qui est fait**
- Lecture complète du livret Hellfire Hunt : `docs/rapports/2026-10-26-hellfire-hunt-lecture-livret.md` ; audit des trois campagnes : `docs/rapports/2026-10-26-audit-campagnes-fanmade.md`.
- **États nets** écrits par les agents au moment de la pause : `docs/rapports/campagnes-en-pause/hellfire-hunt-fondations-GABARITS.md` et `.../hellfire-hunt-white-queen-GABARITS.md` (copies des gabarits de la branche de campagne : à lire en premier pour reprendre).
- **Fondations** (hf001-hf099) : fichier de campagne `data/campagnes/hellfire_hunt.json`, 16 alliés recrutés, 12 side schemes Potential Ally, 7 side schemes de campagne, Xavier's Institute, cartes d'aspect de Marvel Girl, reskins ; extensions moteur du deck « Recruited Mutants » ; **92 cas `[hfc]` verts** ; decks de départ Marvel Girl (22 cartes) et Sunspot (15 cartes, incomplet : Finishing Blow, Cecilia Reyes, For What's Right et X-Force Strike manquent du zip et du jeu).
- **White Queen** (hf100-hf199) et ses modules (hf300-hf399) : scénarios `data/scenarios`, `data/encounter_sets`, cartes et scripts ; **94 cas `[hf]` verts** ; changement de forme du vilain sans remise à zéro des PV natif dans le moteur (seul ajout : trait `DIAMOND`) ; « incite 1 » au retour en PSIONIC codé dans le script de hf103a.
- Toutes les cartes restent « Carte terminée : NON (provisoire) ».

**Ce qui reste**
- Preuves par substitution (pour toutes les cartes de campagne et de White Queen) ; cas manquants (Rally the Survivors, limite once-per-phase de hf048, hf043, retournement de White Queen) ; `test_cards`, vérificateurs de préfixes et d'API ; recalcul des checksums ; `RECETTES-MOTEUR.md` ; textes français de White Queen (42 cartes) et voiles des 48 + scans ; autoplay (8 parties Sunspot + témoin) ; `QUESTIONS.md`.
- Perte de campagne au scénario 5 en expert et jeton d'accélération : déclarés, **non testés** (ni vitest ni jeu).
- **Scénarios 2 à 5 non commencés** : Black King, Cassandra Nova, Black Queen, Torn (ordre recommandé : Black King, Cassandra Nova, Black Queen, Torn ; Torn en dernier, Emma Frost a quatre faces dont deux à PV infinis). Onze extensions moteur au total d'après le dossier de lecture (jour/nuit, decks de table partagés, formes de vilain…).
- **Questions ouvertes** : X-Gene ×2 contre « Max 1 per player » ; texte de hf044 Psychic Minefield ; Rally the Survivors « reste en jeu » ; permission de jouer Blink depuis la défausse Recruited ; moment où la 1B de White Queen avance après la fin du round et report du jeton d'accélération ; hf304 en multijoueur ; incite du stade 3 à la première révélation ; **règle jour/nuit de Black Queen** (portée par ses deux cartes d'environnement, absente du livret).
- **Hydra Unleashed** : 385 cartes, 8 scénarios, 5 mots-clés absents du moteur (Civilians X, Heroic, Sniper X, Zealot, Mercenary), au moins 4 extensions moteur (six vilains simultanés avec jeton d'activation, vilain issu du deck de rencontre, deck de Lieutenants, vilain à six cartes avec dé) ; héros Mockingbird sans cartes.
- **Une seule passe complète des cas de test à la fin des campagnes** (décision de l'utilisateur) : en mode parallèle `PARALLELES=6` (environ une heure ; la séquentielle dépasse six heures).

## 10. Retours du créateur TMNT et rapports de bug (ajouté le 12/11/2026)

Reste à faire après la session du 12/11 (commits `2f7c51d6`, `e16fc138`, `a3ddb219` non poussés sur `gs7-earth-under-siege`).

**Cartes du créateur à publier** (fichiers ou textes à demander au créateur) : Odyn (set Taijutsu), Nobody (set Alopex), Onmitsu (Path shinobi, recto et verso), Shuriken renommée Throwing Stars (FFG a déjà une carte Suriken). Chaque carte passe par `docs/reference/PROCESSUS-CARTE.md`.

**Kuji-Kiri, Ring of Protection (sj007)** : le créateur signale qu'elle ne propose jamais d'annuler une traitrise pendant une partie avec Baxter. Non reproduit : les 7 cas `[sj] sj007` passent. Il faut le nom de la traitrise et le moment exact de la partie.

**Dazed et Cloaked sur les trahisons** : même correction appliquée aux deux (`2f7c51d6`, `a3ddb219`). Le créateur n'a demandé que Cloaked : à confirmer.

**Voie Shinobi dans l'éditeur de deck** (`e16fc138`) : panneau de choix du Path, filtrage de la grille, Voie propre de Jennika. Logique testée (node), rendu jamais vérifié à l'écran : le créateur doit le tester. Il dit neuf Paths ; les données en contiennent onze.

**Bug 128 : Odorat Amélioré (Enhanced Olfaction, 60003) ne se déclenche jamais.** Confirmé : aucun script pour 60002 à 60006 dans `src/cards/pack/fne/daredevil/` (seul 60012 existe, et il ne fait que lister ces cartes comme cibles d'attachement). Les interruptions de la série Sense (attacher, réduire le coût de la prochaine carte) ne sont donc jamais jouées. Carte à implémenter, pas un misplay. Cinq cartes à faire : 60002, 60003, 60004, 60005, 60006.

**Bug 129 : Nick Fury (art alternatif) ne propose pas « retirer 2 menaces ».** Probablement pas un bug : le complot The Crimson Cowl avait 0 menace au moment du choix (journal), donc l'option n'a pas de cible. Capture et journal lus. À confirmer avec le joueur ; si la règle veut qu'elle soit proposée à 0 menace, c'est un correctif moteur.

**Poussée** : les commits de cette session et les quatre précédents restent locaux (sept commits au total sur la branche).

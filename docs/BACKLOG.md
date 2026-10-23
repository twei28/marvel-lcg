# Backlog

Les chantiers décidés ou envisagés, pas encore faits. Une entrée par sujet : ce qu'on veut, ce qu'on a mesuré,
les options, et ce qui reste à trancher. Quand un sujet est fait, on le raye ici et on renvoie vers son commit ou
sa documentation.

---

## 1. Un jeu « installable » sans installer 2,5 Go de cartes (ajouté le 18/10/2026)

> **Décision du 20/10/2026 : le jeu installable reste au backlog, on ne le fait pas maintenant.** Le cadrage est fait
> (`docs/rapports/cadrage-14-15-19-2026-10-20.md`, §3) : voie recommandée = application installable de `play.` avec cache hors
> ligne, WebP et paquets par héros/scénario. Sept décisions (I1 à I7) restent à poser le moment venu. Constat utile : la
> phrase « pas de hors-ligne » ci-dessous est périmée (le mode navigateur `play.` fait déjà tourner le moteur chez le joueur).

**Le besoin.** Que les joueurs installent le jeu sans attendre le téléchargement de toutes les cartes.

**Le critère de choix, donné par l'utilisateur.** La solution qui est la plus facile pour les joueurs ET la plus
facile à mettre à jour de notre côté. C'est ce critère qui tranche, pas la puissance de la technique.

**Ce qu'on a mesuré (18/10/2026, `Fusion/marvel-lcg-src/assets/`).**

| Dossier | Poids | Fichiers |
|---|---|---|
| `pics` (scans anglais) | 981 Mo | 7 876, 125 Ko en moyenne |
| `pics-fr` (scans français) | 915 Mo | |
| `pics-hd` | 225 Mo | |
| `vignettes` (images de la table) | 433 Mo | 10 871, 39 Ko en moyenne |
| sons, textures | environ 25 Mo | |

Environ 2,5 Go d'images, le reste du jeu est léger. **Une partie n'en utilise qu'une petite part** : environ
120 cartes (deck du joueur, scénario, méchant), soit environ 5 Mo de vignettes. Les grands scans ne servent
qu'au zoom.

**Ce qui existe déjà.** Une installation « application » sur téléphone (`ui-app/src/board/mobile/installation.ts`,
manifeste et `sw-plateau.js` servis par `web_server.py`). Son service worker **ne garde rien en cache** et il ne
s'active que sur téléphone.

**Les options.**

1. **Application installable + cache des cartes à la demande.** Installation de quelques dizaines de Mo. Chaque carte
   vue est gardée, et les ~120 cartes de la partie sont préchargées au lancement (quelques secondes). Mise à jour :
   uniquement côté serveur, rien à redistribuer.
2. **Alléger les images.** JPG et PNG en WebP (souvent 30 à 50 % de moins), français seulement avec l'anglais en
   secours, haute définition à la demande. De 2,5 Go à environ 1 Go, sans perte à l'usage.
3. **Paquets à télécharger** (un héros, un scénario, une extension, ~8 Mo chacun) pour jouer hors ligne. Les archives
   actuelles de `paquets-cartes/` (3 Go, par héros) ne sont pas faites pour ça.
4. **Application de bureau complète** (moteur Python + interface), images téléchargées en arrière-plan. C'est la
   seule voie pour jouer **sans internet**. Mises à jour plus lourdes : installateur, versions, signature.

**Limite à connaître.** Le moteur de règles est en Python, côté serveur : une application installable depuis le
navigateur ne peut pas jouer hors ligne. Le lancement local (`JOUER-SOLO`) a, lui, toutes les images sur le disque.

**Réponses de l'utilisateur (18/10/2026).**
- Jouer **sans connexion** : oui, c'est un besoin.
- Le cache doit servir **aussi sur PC**, pas seulement sur téléphone : oui.
- Règle de nettoyage du cache : **pas décidée** (« je ne sais pas »). Proposition par défaut, à confirmer plus tard :
  garder les cartes des decks et scénarios déjà joués, effacer d'abord les moins récemment vues au-delà d'une taille
  maximale réglable (par exemple 1 Go).

**Conséquence : la recommandation change.** Le hors-ligne est un besoin, or le moteur de règles est en Python côté
serveur : les options 1 et 2 seules (navigateur + cache) ne suffisent plus. Il faut une **application de bureau**
(option 4) qui embarque le moteur et l'interface, avec les images en téléchargement à la demande. Les options 1 et 2
y restent utiles, comme briques :
- **Allègement des images (option 2)** : à faire quoi qu'il arrive, il réduit le téléchargement de chaque joueur.
- **Cache et préchargement à la demande (option 1)** : la même logique, dans l'application de bureau, avec un dossier de
  cartes sur le disque du joueur à la place du cache du navigateur.
- **Paquets (option 3)** : « télécharger ce héros et ce scénario pour jouer hors ligne », en plus du téléchargement
  automatique des cartes de la partie.

**Pour tenir ton critère (facile pour les joueurs, facile à mettre à jour).**
- Joueur : un seul installateur léger (le moteur et l'interface, sans les cartes), puis les cartes arrivent au fil des
  parties ; un bouton « tout télécharger » est facultatif.
- Mises à jour : une mise à jour automatique de l'application au lancement, et des images adressées par leur
  **empreinte** (nom de fichier = hash), de sorte que seules les cartes nouvelles ou modifiées se retéléchargent.

**À trancher ensuite.**
- La technique d'emballage du moteur Python avec une interface web (par exemple une fenêtre qui embarque le navigateur)
  et le programme de mise à jour : à comparer sur la taille de l'installateur, la signature et les antivirus sous
  Windows, et la facilité des mises à jour.
- Garder aussi l'accès par navigateur pour ceux qui ne veulent rien installer (le jeu en ligne actuel).
- Les systèmes visés : Windows seulement, ou aussi Mac et Linux (les lanceurs `.command` et `.sh` existent déjà).

**Pistes de départ.** Mesurer le gain d'un passage en WebP sur 100 cartes ; prototyper le téléchargement à la demande
des cartes d'une partie ; étendre `sw-plateau.js` pour la version en ligne ; évaluer l'emballage du moteur.

---

## 2. Ajouter des langues au jeu (ajouté le 18/10/2026)

> **Décision du 20/10/2026 : l'espagnol est la langue choisie en premier, mais le chantier est laissé au backlog, on ne le fait pas maintenant.**
> Un cadrage a été lancé puis arrêté avant tout résultat (aucun fichier du jeu touché). Au moment de reprendre : mesurer la couverture espagnole de MC4DB et MarvelCDB,
> cartographier le branchement de fr/en (interface, cartes, noms, scans, site, préférence de langue), puis poser les décisions une par une (traduction machine ou relecture,
> scans espagnols ou texte seulement, repli sur l'anglais, noms de héros officiels).

**Le besoin.** Le jeu est en français et en anglais. Savoir quelles langues ajouter ensuite, et où trouver leurs
cartes (textes et images).

**Quelles langues.** Les ventes par langue **ne sont pas publiques** (ni Fantasy Flight Games ni Asmodee ne les
publient). Éditions officielles confirmées : anglais, français, allemand, italien, coréen ; espagnol, chinois et
tchèque cités par un site de fans non officiel. Estimation, **non sourcée**, des cinq langues les plus
vendues : anglais, puis français, allemand, espagnol, italien (ordre incertain après le français). L'allemand et
l'espagnol seraient les suivantes à ajouter.

**Où trouver les cartes (mesuré le 18/10/2026).**

*Textes et noms : MarvelCDB* (`<langue>.marvelcdb.com`, même interface publique que pour `fr.`, déjà utilisée par le
projet). Sur ses 2 155 cartes officielles, part dont le nom ou le texte est traduit :

| Langue | Adresse | Couverture |
|---|---|---|
| Espagnol | `es.marvelcdb.com` | 99 % |
| Allemand | `de.marvelcdb.com` | 86 % |
| Français | `fr.marvelcdb.com` | 82 % (déjà utilisé) |
| Italien | `it.marvelcdb.com` | 82 % |
| Coréen | `ko.marvelcdb.com` | 35 % |
| Polonais, russe | `pl.`, `ru.marvelcdb.com` | 0 % (le site existe, tout est en anglais) |
| Chinois, japonais, portugais, tchèque | | aucun site de langue |

*Images :*
- Un **pack d'images chinoises** (54 Mo, 24/05/2024) pour le moteur d'`irefrixs`, annoncé dans son
  [journal de développement](https://irefrixs.itch.io/marvel-lcg/devlog/737085/post) ; même mécanisme que les scans
  français (dossier d'images ajouté à `image_folders`).
- **Coréen** : communauté [Boardlife](https://boardlife.co.kr/game/14799/board/talk), traductions de fans incomplètes.
- **OCTGN** et **DragnCards** : à ma connaissance ils ont des cartes et images en plusieurs langues, mais **non vérifié**,
  les recherches n'ont rien donné ; à aller voir directement dans leurs dépôts.

**Ce que ça ne couvre pas.** Les extensions fan-made et TMNT/Shinobi n'existent pas sur MarvelCDB : leurs traductions
resteraient à faire à la main. Les conditions d'usage de MarvelCDB pour une réutilisation à grande échelle n'ont pas
été vérifiées.

**Ce qui existe déjà dans le projet.** L'import français (`fr.marvelcdb.com`, textes FR du plateau, scans dans
`assets/pics-fr`, 915 Mo ; rapport `docs/rapports/RAPPORT-SCANS-FR.md`). Le travail pour une nouvelle langue suit
le même chemin : textes de cartes, textes de l'interface (`dico-en`-like), scans, noms de cartes.

**À trancher.**
- Quelle langue en premier (l'espagnol a le meilleur rapport couverture/effort pour le texte) ?
- Les scans : où les trouver pour cette langue (pack OCTGN ? DragnCards ?) et leur poids (voir le chantier 1 : ~1 Go
  par langue de scans, à alléger avant d'en multiplier).
- Faut-il demander l'accord de MarvelCDB ?

**Pistes de départ.** Chiffrer le travail pour l'espagnol (textes MarvelCDB + interface) ; regarder les modules
OCTGN et DragnCards pour les scans ; mesurer le poids d'une langue en WebP.

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

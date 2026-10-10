# Éditeur de deck : refonte (décidée le 09/10/2026, PAS ENCORE CODÉE)

Constat (capture 1920x1080, `deck-builder.html?hero=spider_man`) : quatre lignes de decks « Partir de » (~30 pastilles) puis
cinq lignes de filtres occupent la moitié haute ; la grille commence à mi-hauteur (deux rangées visibles) ; à droite,
l'aperçu de la carte survolée prend toute la hauteur et pousse la liste du deck hors de vue.

Décisions de l'utilisateur :
- **Trois colonnes** : filtres à gauche en colonne étroite et repliable (aspects, types, coûts, ressources, mots-clés) ;
  grille au centre ; deck en cours à droite, toujours visible. « Partir de » devient un menu déroulant. Recherche en haut
  de la grille.
- **Vignettes** : scan entier, TAILLE ACTUELLE, sans le nom répété dessous ; nombre d'exemplaires en badge sur la carte,
  + / − au survol.
- **Mon deck** : liste groupée par type (Alliés, Événements, Améliorations, Soutiens, Ressources) avec le nombre par
  groupe ; chaque ligne : coût, nom, pastille d'aspect, ×N ; survol = aperçu, clic = retire un exemplaire. En haut :
  total / 40, courbe de coûts, validité.
- **Aperçu** : en haut de la colonne deck, plus petit qu'aujourd'hui, au-dessus de la liste.
- **Fan-made** : un simple interrupteur « Afficher le fan-made » dans la colonne des filtres, sans mémoire d'une visite
  à l'autre (les cartes fan-made déjà dans le deck restent dans la liste du deck).
- **Style** : celui de la préparation (police Marvel pour les titres, pastilles biseautées, couleurs d'aspect franches,
  en-tête fin).

- **Repris de MarvelCDB / MC4DB (choix du 09/10/2026)** :
  - simulateur de pioche : main de départ tirée au hasard, probabilité de piocher une carte donnée ;
  - graphiques du deck (coûts, ressources générées, aspects) et tri du deck au choix (type, coût, aspect, nom, pack) ;
  - filtres avancés : traits, pack, unique, ATK / THW / DEF / PV, et une syntaxe courte dans la recherche.
  NON retenus : historique des versions, notes et étiquettes, bouton Chaos, filtre « mes extensions », export texte.

À garder : recherche FR (recherche.js), arts des rééditions (arts-reeditions.js, bouton « Arts » en anglais), traduction
posée sur l'aperçu, mode Legacy (cartes verrouillées), Stan Lee (signatures empruntables), cartes imposées par aspect,
sauvegarde / brouillon / export, mobile.

## Décisions détaillées (40 questions, 09/10/2026 au soir) : elles PRIMENT sur ce qui précède

Mise en page
- 1920 px : filtres 15 %, grille 60 %, deck 25 %. Sous 1600 px : filtres repliés en icônes (panneau au clic).
- Mobile : grille plein écran + barre en bas « Filtres · Deck (40) » qui ouvre des panneaux glissants.
- Colonne des filtres ouverte au chargement, état mémorisé (localStorage).

Filtres
- Sections Aspects, Types, Coûts dépliées ; Ressources, Mots-clés, Traits, Pack, Stats repliées.
- Aspects : pastilles colorées, multi-sélection ; défaut = aspect(s) du deck + Basique. Hors aspect cachés par défaut.
- Aspects multiples : selon les règles du héros (Spider-Woman, Adam Warlock...). Héros à un aspect : ajout d'une
  carte d'un autre aspect autorisé, deck marqué invalide avec la raison.
- Types : pastilles icône + nom, multi ; aucune = tous. Coût : pastilles 0 1 2 3 4 5+ X, multi.
- ATK / THW / DEF / PV : pastilles 0 1 2 3 4+ par stat.
- Traits : champ avec suggestions, étiquettes, bouton ET / OU. Pack : liste groupée par vague, cases, recherche, fan-made
  en dernier groupe.
- Syntaxe courte (t: c: a: p: atk>= ...) FR et EN, aide « ? ». Recherche simple : nom FR et EN d'abord, puis texte.
- Tri de la grille : menu, défaut aspect puis coût (aussi nom, coût, type, pack).

Grille
- Clic gauche = +1, clic droit = −1, + / − au survol. Au maximum : badge « 3/3 » plein, + grisé, carte un peu assombrie.
- Legacy (cadenas) et Stan Lee (badge) comme aujourd'hui.

Colonne du deck (de haut en bas)
- Nom du deck modifiable, icônes Enregistrer / Exporter / Importer, menu « Partir de » (confirmation « Remplacer ton
  deck actuel ? » si non vide).
- Aperçu ~1/3 de la hauteur ; vide = carte d'identité du héros ; arts alternatifs en petites vignettes sous l'aperçu.
- Total « 25 + 15 = 40 / 40–50 », histogramme des coûts 0 à 5+, pastille validité verte « Valide » / rouge « N problèmes »
  (clic = liste, cartes fautives soulignées).
- Onglets Liste / Statistiques / Pioche.
  - Liste : tri au choix (type par défaut, coût, aspect, nom, pack), groupes avec nombre ; ligne teintée par l'aspect
    (normal et sobre) ; + / − sur la ligne, clic sur le nom = aperçu fixé. Kit du héros caché : compteur
    « +15 cartes du héros », clic = liste en lecture seule.
  - Statistiques : ressources générées, répartition par aspect.
  - Pioche : main de départ (bouton alter ego / héros pour la taille), « Piocher 1 », « Nouvelle main », chances pour une
    carte survolée (main de départ, tours 2 et 3).
- Deck invalide : ni enregistrable ni jouable ; brouillon automatique conservé quand même.
- Clavier : / recherche, Échap vide, Ctrl+S enregistre.

Validation : maquette image d'abord (validée par l'utilisateur), puis code, puis captures réelles.

## Comparaison MarvelCDB / MC4DB (09/10/2026)

Sources : pages publiques de marvelcdb.com (recherche, vue de deck), guide « The Champion's Guide to MarvelCDB »
(Alter Ego Chronicle), accueil et listes de mc4db.merlindumesnil.net. MC4DB est une refonte de ThronesDB, même famille que
MarvelCDB, avec le contenu fan-made en plus.

**À reprendre (du plus utile au moins utile)**
1. Simulateur de pioche et calcul de probabilités (main de départ, chances de tirer telle carte au tour N).
2. Graphiques du deck : coûts, icônes de ressources générées, répartition par aspect.
3. Tri du deck au choix (type, coût, aspect, nom, pack), pas seulement par type.
4. Filtres de recherche avancés : traits, pack, unique, valeurs ATK/THW/DEF/PV, ressources ; idéalement une syntaxe courte
   tapée dans la barre (ex. trait, coût).
5. Historique des versions du deck avec retour en arrière.
6. Notes et étiquettes sur le deck.
7. Bouton « Chaos » : remplissage aléatoire légal du deck.
8. Filtre « mes extensions possédées » (collection).
9. Export texte en plus du JSON.

**Ce que nous faisons mieux**
- Le deck se sauvegarde et se joue directement dans le jeu, sans copier de lien.
- Recherche par nom français officiel, sans accents ; traduction posée sur les cartes anglaises.
- Règles du jeu appliquées en direct : Legacy, cartes imposées par aspect, Stan Lee, cartes Multiverse.
- Choix de l'illustration des rééditions.
- Aperçu de la carte au survol, sans changer de page.

**Non vérifié**
- L'éditeur de MC4DB lui-même (connexion requise) et ses éventuels ajouts propres.
- La syntaxe exacte du « filtre personnalisé » de MarvelCDB (page d'aide introuvable en 404).
- Le rendu mobile des deux sites.

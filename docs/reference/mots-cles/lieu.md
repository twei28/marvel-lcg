# Lieu (LOCATION), déplacement en grille

**Texte imprimé / définition** :
- Punisher MC×DC 2026, p009 *The City* (environnement, Setup/Permanent) : « Players mark their location in the city
  with a token, starting in Midtown. Players can only interact with locations (abilities & cards attached) they
  occupy. **Action**: Exhaust a character you control or spend 1 resource of any type → move to an adjacent (↔ or ↕)
  location. »
- 9 cartes type *Lieu* (p059-p075, set « Locations — The Big Apple », ID 6030-6038), chacune numérotée 1 à 9 et
  associée à une case fixe de la grille 3×3 : Hell's Kitchen (1), Theater District (2), Upper East Side (3), West
  Village (4), Midtown (5, lieu de départ), Lower East Side (6), Soho (7), Financial District (8), Chinatown (9).
  Chacune porte une capacité **Action** ou un effet passif propre à son emplacement (ex. p059 Hell's Kitchen :
  « Allies and minions in Hell's Kitchen cannot thwart or scheme and gain toughness » ; p069 Lower East Side :
  « Each character in Lower East Side gains retaliate 1 »).
- 3 cartes Uptown en plus (p045-p049, U1-U3 : Upper West Side, Harlem, The Bronx), 4e rangée optionnelle (décision
  P2 de `.planning/todos/2026-10-20-punisher-questions.md`).
- `regles-fr.md` ligne 60 (règle imprimée confirmée par l'utilisateur) : une capacité de lieu « limite une fois par
  round » l'est **au total**, pas par joueur.

**Mécanisme moteur** : **à créer**, aucun équivalent exact dans le dépôt au 20/10/2026. Ce qu'il faut :
- Un état de position PAR JOUEUR (pas par carte, pas par partie) : quel lieu (1 à 9, ou U1-U3) occupe chaque joueur,
  initialisé à Midtown (case 5) à la mise en place. Candidat le plus proche repéré par le cadrage (§1.2, M1) :
  l'état du monde (`World`) plutôt qu'un compteur de carte, car neuf lieux sont en jeu simultanément et chaque
  joueur n'en occupe qu'un.
- La grille 3×3 (4×3 avec Uptown) et l'adjacence orthogonale (↔ ↕, jamais en diagonale) pour l'action de déplacement
  de *The City* : coût = épuiser un personnage **ou** dépenser 1 ressource de n'importe quel type.
- La restriction « un joueur ne peut interagir qu'avec le lieu qu'il occupe » (capacités ET attachements posés sur
  ce lieu) : à vérifier contre chaque capacité de lieu lors du portage carte par carte (PROCESSUS-CARTE.md).
- Modèle de TEXTE le plus proche dans le dépôt (pas de modèle de MÉCANISME de position) : les environnements à
  trait LOCATION/PLANET de Skrull Empire (Galactic Storm, `skrull_menace/skrull_empire/sk086.py`…`sk097.py`) pour
  la forme des capacités d'un lieu, mais ils ne portent pas de déplacement de joueur ni de grille.

**Carte exemple** : aucune carte portée à ce jour (lot PU-5 du cadrage, « fort » recommandé pour la spécification).

**Pièges connus** :
- Ne pas confondre la **capacité de lieu** (un *Action* imprimé sur la carte lieu elle-même, utilisable par
  n'importe quel joueur occupant le lieu, limité au total) avec une capacité de **personnage** qui mentionne un
  lieu (ex. p073 Financial District : « The villain attacks you » est une **Hero Action**, donc par joueur, pas par
  lieu — la limite « une fois par round » de cette carte-là s'applique à ELLE, pas au lieu).
- Des attachements de lieu existent (Burning Building p013, Citizens in Danger! p015, Hunted by the Past p017,
  "It's a Trap!" p019) : « Attach to your current location » lit la position du joueur qui révèle la carte, pas un
  lieu fixe. Voir `territoire.md` pour les sbires qui s'attachent à un lieu inoccupé.
- La piste (LEAD) liée à un lieu (même numéro) lit elle aussi « while in <lieu> » : la condition de position est
  donc partagée entre les capacités de lieu et les pistes, voir `piste-lead.md`.
- Le lieu de départ (Midtown, case 5) doit être mémorisé en mode campagne (combat 2 : « record the location where
  the final LEAD card was added to the victory display », p003).

**Variantes maison** : aucune à ce jour ; brique neuve du lot Punisher MC×DC 2026 (cadrage §1.2, mécanique M1).

# Shadowland : decisions de l'agent D (Ninja Swarm sl028-sl036, Black Flower sl072-sl078)

Format : decision, raisonnement. Aucune question n'a pu etre posee a l'utilisateur (pas de livret officiel).

1. **Creeping Corruption (sl072a/b) : le joueur « est vaincu » = son identite est vaincue.** Selon la Rules Reference, un joueur est elimine quand son identite est vaincue ;
   le moteur fait deja `Identity.OnBeDefeated -> Player.Eliminate`. On passe donc par `Faces.DefeatUnits([identite])` (les interruptions de defaite restent valables) et non par
   `Player.Eliminate` direct. Dans une partie a un joueur la partie est perdue ; a plusieurs, la regle d'elimination habituelle s'applique.
2. **« When Defeated » d'un sbire : la carte vaincue est encore en jeu pendant la resolution** (comportement du moteur, conforme a la RR : une carte vaincue quitte le jeu
   APRES ses capacites « When Defeated »). Consequence pour Bo Staff / Fukiya / Katana / Kusarigama / Shuriken : le sbire Teamwork qu'ils revelent trouve le sbire
   vaincu comme « autre sbire NINJA en jeu » et s'active. Mesure par le cas `sl034 ... SEUL NINJA en jeu`.
3. **Teamwork (NINJA)** est lu dans `desc` (natif, `Teamwork: NINJA`, ajoute sur sl029-sl034, absent de la transcription automatique). Regle de jeu reelle : `v16_all`
   (seul le sbire qui arrive s'active) ; les cas posent `regles: [v16_all, v18_all]`. Sous la regle par defaut du moteur (pre-1.6) tous les sbires Teamwork de meme trait s'activeraient.
4. **« the first minion with the teamwork keyword »** : premier dans l'ordre de defausse (la carte du dessus d'abord) ; « with the teamwork keyword » = mot-cle IMPRIME
   (`printed_teamwork`), car une carte defaussee n'a plus de mots-cles courants.
5. **« The defeating player »** : le joueur qui a vaincu le sbire ; a defaut (vaincu par un effet sans joueur : retaliate...) le joueur avec qui il etait engage.
6. **Kirigi, « either spends 2 resources of any type or shuffles Kirigi »** : choix du joueur ; la branche « depenser » n'est offerte que si elle est payable (sinon le moteur
   la reduirait au plus gros morceau payable). S'il choisit de depenser, Kirigi reste defausse.
7. **Corrections de `data/cards.json`** apres relecture des scans : Teamwork NINJA (sl029-sl034), Toughness (sl030), Boost 1 (sl036), StartingThreat 1 par joueur (sl075),
   StartingThreat 1 et Acceleration 2 (sl076), Permanent/Setup/MaxPerUnit (sl072a) et Permanent/MaxPerUnit (sl072b). L'ATQ « 1★ / 3★ » est celle du texte : la valeur reste 1 / 3.
8. **Aka (sl073), boost « discard 1 random card from your hand »** : la branche est masquee quand la main est vide (elle n'aurait aucun effet et deviendrait une echappatoire
   a la corruption). Meme principe pour toute branche « Choose: either A or B » : une branche IMPOSSIBLE n'est pas choisissable (Creeping Corruption absente -> pas de branche compteur).
9. **Invasive Thoughts (sl078) sans Creeping Corruption** : aucun compteur n'est pose, « it » n'existe pas, le test « If it has OVERPOWERING » echoue donc et « otherwise, take 1 damage » s'applique.
   Avec une Creeping Corruption, le test est fait APRES la pose (la pose du 5e compteur retourne la carte, qui devient OVERPOWERING : 1 menace, pas de degat).
10. **Setup de la Creeping Corruption (sl072a)** : `desc.Setup` ne met la carte en jeu QUE si l'exemplaire est dans un deck JOUEUR (il a un proprietaire). Un exemplaire du deck de rencontre
    ou de la reserve du scenario est « mis en jeu » par `ProcessSetup` sans effet visible (`PutIntoPlay` sans `under_control` n'attache rien) : le scenario 3 doit donc donner SA Creeping Corruption
    a chaque joueur par code (`face.PutIntoPlay(joueur, effect, under_control=True)`, voir `skrull_menace_campaign/__init__.py`), un exemplaire par joueur (Max 1 per player). Mesure en autoplay :
    un exemplaire ajoute au `hero_deck` est bien mis en jeu au Setup (16 parties sur 16). Les sets `ninja_swarm` et `black_flower` ne contiennent donc PAS sl072a/b.
11. **Interruption de Aka (sl073)** : la fenetre d'Interruption est elle-meme le « you may » (le joueur l'accepte ou la passe) ; on ne repose pas une seconde question. La capacite n'est offerte
    que si le joueur a une Creeping Corruption. L'annulation ne vise que l'attaque : l'activation (Quickstrike, boost de Villainous) a bien eu lieu.
12. **Elimination par Creeping Corruption face B** : voir n°1. Un test a un joueur mesure `partie_finie` (la defaite du seul joueur termine la partie).
13. **Une carte PERMANENTE n'est jamais une cible de defausse** (correctif sur le scenario 1, fichiers de l'agent A) : `Faces.DiscardAll` sur une carte Permanent attachee leve
    `assert controller.is_eliminated` (`card_face.py:861`), exception AVALEE par le moteur (invisible hors journal d'autoplay). `sl004b` (« discard an ally or upgrade you control ») pouvait
    cibler la Creeping Corruption ; `CartesControlees` (sl006, « discard 1 card you control ») la proposait aussi. Correctif : `CardFinder(canbe_discard=True)` dans les deux. A reporter dans
    toute carte du pack qui defausse « une carte que vous controlez ».
14. **Compteur dans le deck de rencontre** : les 9 cartes de Ninja Swarm sont x1 chacune ; Black Flower : sl073 x1, sl074 x1, sl075 x2, sl076 x1, sl077 x2, sl078 x2 (quantites du recensement
    `cartes.md`, a confirmer par le livret : Q10).

## Gabarits PROCESSUS-CARTE.md (resumes)

Pour toutes les cartes : etape 2 (references) en tete de chaque script (`src/cards/pack/shadowland/ninja_swarm/*.py`, `black_flower/*.py`) ; etape 5 (mots-pieges) et etape 6 (nombres texte/code)
verifies sur le scan lu image par image (corrections de `cards.json` au n°7) ; etape 7 : cas `[sld]` dans `Fusion/marvel-lcg-src/tools/cas/shadowland_d.py`, preuve par substitution (module remplace
par `GetAbilities -> []`, cas rouges ; seuls restent verts les temoins d'absence et les mots-cles natifs lus dans `desc`) ; etape 7 bis : aucune limite imprimee sur ces cartes ; etape 8 : autoplay
8 parties (`sl_essai_ninja_black_flower`, perdues au round 1 dans le scenario 1 comme le temoin : complot du scenario A) puis 16 parties `rhino` + `--modulaires ninja_swarm,black_flower`
(deck Spider-Man + sl072a au Setup) : 0 traceback, toutes les cartes vues en jeu, temoin Spider-Man seul : 0 victoire sur 16 contre 3 ; etape 8 bis : voir le rapport (non faite).

| Carte | Cas `[sld]` | Mutations (module vide) |
|---|---|---|
| sl072a/b Creeping Corruption | 10 | 072a : 3 rouges sur 6 ; 072b : 3 rouges sur 4 |
| sl028 Black Mountain | 7 | 2 rouges sur 7 (les 5 autres sont des temoins d'absence) |
| sl029 Kirigi | 5 | 4 rouges sur 5 |
| sl030-sl034 ninjas Teamwork | 6 / 2 / 5 / 3 / 3 | rouges sur tout ce que le module porte (When Defeated, ranged, piercing) ; Teamwork, Guard, Patrol, Toughness sont natifs (desc) |
| sl035 Dancing Shadows | 7 | 3 rouges sur 7 (PV, menace non retirable, boost) |
| sl036 Countless Numbers | 4 | 2 rouges sur 4 (revelation, boost ; Surge natif) |
| sl073 Aka | 8 | 7 rouges sur 8 |
| sl074 Tongue of the Beast | 6 | 5 rouges sur 6 |
| sl075 Binding Ritual | 6 | 5 rouges sur 6 (Crisis natif) |
| sl076 Roots of a Black Flower | 6 | 4 rouges sur 6 |
| sl077 Malediction | 10 | 9 rouges sur 10 (boost natif) |
| sl078 Invasive Thoughts | 6 | 6 rouges sur 6 |

Carte terminee : OUI pour les 24 faces, sous les reserves du rapport (aucune partie jouee par un humain ; plateau 8 bis non ecrit).

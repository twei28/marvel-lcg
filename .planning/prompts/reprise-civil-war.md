Projet Marvel LCG, dossier "Jeu Marvel Champions" (git, branche master).
Lis d'abord .twei/SESSION.md puis .planning/todos/2026-07-30-mode-bataille-civil-war.md
(surtout ses §6 et §7, qui sont le resultat d'une investigation mesuree).

ETAT : Civil War en mode COOPERATIF est TERMINE et valide en jeu le 13/08/2026.
Rien n'a eu a etre ecrit : 227 cartes, 184 modules, les 4 leaders (iron_man,
captain_marvel, captain_america, spider_woman) et les 2 heros (tigra, hulkling)
se jouent, et la boite "56. Civil War" est deja proposee dans l'ecran de
preparation. L'autoplay mene une partie complete contre chacun des 4 leaders.

IL RESTE DEUX CHOSES, et elles sont de tailles tres differentes.

--- 1. LE CHOIX DU CAMP (petit, a evaluer d'abord) ---

La carte parle de deux camps : registration (pro-recensement, camp Iron Man) et
resistance (anti-recensement, camp Cap). En cooperatif, le camp est aujourd'hui
IMPLICITE : c'est l'oppose du leader choisi, et les sets d'equipe sont deja dans
les modular_sets du scenario (ex. iron_man tire mighty_avengers + the_initiative).

A FAIRE : jouer une partie et regarder si le camp est lisible pour le joueur, et
si quelque chose manque a la preparation. Si rien ne cloche, clore ce point.
Ne rien construire avant d'avoir joue.

--- 2. LE MODE COMPETITIF (gros, et bloque) ---

Deux equipes de joueurs humains s'affrontent. AUJOURD'HUI C'EST DESACTIVE EN DUR,
et pas seulement par un drapeau : toute la famille "equipe" est bouchonnee dans
src/game/operate/worlds.py.

  worlds.py:884  IsCompetitiveMode  -> return False        (annote Literal[False])
  worlds.py:888  IsCooperativeMode  -> return True
  worlds.py:876  GetYourTeamLeader  -> return None
  worlds.py:860  GetEnemyTeam       -> GetFirstPlayer      (pas une equipe)
  worlds.py:872  GetYourTeam        -> GetFirstPlayer      (le meme !)
  worlds.py:864  GetEnemyLeader     -> cherche une carte de type Leader sur le terrain

Donc le travail n'est pas "lever un booleen" : il faut donner un sens a
GetYourTeam / GetEnemyTeam / GetYourTeamLeader, et decider comment les sieges se
repartissent entre deux camps. 6 cartes du pack cw lisent ces fonctions
(src/cards/pack/cw/, dont registration/56063a.py qui fait
`assert not Worlds.IsCompetitiveMode(effect)`).

⚠ PREREQUIS ABANDONNE : le competitif dependait du serveur permanent multijoueur,
dont la fiche a ete RETIREE de la todo le 13/08 (chantier abandonne). Avant de
coder quoi que ce soit, il faut trancher avec moi : rouvre-t-on ce chantier, ou
vise-t-on seulement du hot-seat local a deux equipes sur une meme machine ?
NE PAS commencer le competitif sans cette decision.

--- COMMENT TRAVAILLER SUR CE DEPOT (pieges deja payes) ---

* git status MENT (cache stat WSL). Seul `git diff --stat` prouve qu'un arbre est
  propre, et il est lent (~2 min) : le lancer en tache de fond AU DEBUT et A LA
  FIN. Six lots non commites ont ete trouves comme ca.
* Deux arborescences : le depot est la source pour src/, data/, tools/ ;
  ~/marvel-work/fusion/marvel-lcg-src est la REFERENCE pour public/js et
  public/css. Toute modif doit finir dans les DEUX. Apres modif de src/, data/
  ou tools/ : copier vers ~/marvel-work puis `launcher_fast.py --build-only`.
* public/ est en CRLF. Lire ET ecrire avec newline='' sinon le diff explose.
* NE JAMAIS ECRIRE UN APPEL "PLAUSIBLE". `GainKeywordPermanently`,
  `Worlds.GetPhase`, `ReduceCostToPlayCard` n'existent pas et sont passes entre
  les mailles. Verifier chaque appel par `grep -rn "def <Nom>" src/game`, puis
  passer `tools/verifier_appels_modules.py`.
* Le port 2345 est celui de la partie de l'utilisateur : NE PAS Y TOUCHER.
  Prendre un port libre (2346+), et `launcher_fast.py` recopie launch.json donc
  il ne peut pas servir un second serveur — demarrer le moteur en respectant le
  .game/launch.json deja pose (voir SESSION.md).

--- LES OUTILS DE VERIFICATION (tous dans tools/) ---

  autoplay.py                 joue des parties entieres sans navigateur
  test_cards.py               les capacites se construisent
  test_generate_cards.py      la carte se construit
  verifier_appels_modules.py  les METHODES appelees existent
  verifier_noms_modules.py    les NOMS utilises existent
  verifier_desc_mots_cles.py  le desc dit ce que le texte annonce
  verifier_cartes_en_jeu.py   la carte PORTE ce qu'elle annonce

AUCUN ne dit qu'une capacite fait la BONNE chose : c'est une partie reelle qui
l'a dit pour Merc Squad. Mesurer avant de conclure, et ecrire ce qui est mesure.

Commence par le point 1 (le camp) : c'est peu couteux et il decide du reste.
Enchaine ce qui est le plus logique, commite au fur et a mesure, et tiens
.twei/SESSION.md a jour.

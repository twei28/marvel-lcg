# Preuves PROCESSUS-CARTE : Jigsaw (pu056a, pu056b, pu057a, pu057b)

Une seule capacité commune (`jigsaw_commun.py`), quatre faces. Le scan a été envoyé à l'utilisateur ; aucune ambiguïté de règle.

### pu056a / pu056b / pu057a / pu057b : Jigsaw

- [x] Étape 2 : cartes de référence : `sm/sinister_six/27099.py` (déclencheur), `angela/angela_nemesis/an015.py` (lecture de la défausse de rencontre), `sm/sinister_six/27100a.py` (`PutIntoPlay`, `PlaceThreatOnSchemes`).
- [x] Étape 5 : texte-contre-code. Mots-pièges : « attaque » seul (PAS « attaque et blesse » : corrigé), « le dessus » (seul le dessus compte), « mettre en jeu » (ne déclenche pas « When Revealed »), « vous » (le joueur attaqué).
      Résultat : conforme. ⚠ La carte Boost de l'attaque est défaussée AVANT la Réponse forcée : c'est elle qui est « le dessus ». À confirmer par l'utilisateur si une autre lecture est voulue.
- [x] Étape 6 : nombres : 1 menace (pu056a/b, pu057a), 2 menaces (pu057b). Résultat : conforme (cas 3).
- [x] Étape 7 : `tools/cas/jigsaw.py`, 3 cas `[jig]` : sbire en dessus → en jeu, pas de menace ; traitrise en dessus (sbire dessous) → 1 menace, aucun sbire ; pu057b → 2 menaces.
      Témoin rouge par substitution (condition sbire forcée à faux, menace forcée à 1) : 2 cas sur 3 rouges, le 3e (témoin 1 menace) reste vert comme prévu. Restauré, 3/3 verts.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay 8 parties Jigsaw (normal) contre 8 parties Hammerhead témoin, Spider-Man : 0 incident des deux côtés, 0% de victoire des deux côtés (deck de départ seul, sans amélioration), rounds 4,0 contre 4,2. Journal détaillé non relu ligne à ligne.
- [x] Étape 8 bis : la carte change ce qu'on voit ? NON (un sbire entre en jeu et de la menace monte : zones et jauges déjà couvertes).

Autres corrections de la passe : les 5 scénarios expert Jigsaw n'avaient pas l'ensemble de rencontre « expert » (le complot n'était alors pas posé ; corrigé, script de construction aussi).

Carte terminée : OUI pour le script. Restent hors de cette preuve : les 4 doutes de `jigsaw-doutes.md` (stades, étoile `N**`, tuiles d'accueil, scan tourné).

### pu058 : Jigsaw's Knife

- [x] Étape 2 : références `skrull_menace/paibok/sk148.py` (attache + Riposte + action de défausse à coût), `ts201` (piercing). `ATK+ 1**` natif.
- [x] Question à l'utilisateur (21/10) : « exhaust a character you control » = au choix parmi ses personnages prêts. Réponse : oui, recommandé.
- [x] Étape 7 : 5 cas `[jig] pu058` verts (attache + Riposte 1, témoin sans couteau, piercing, témoin Tenace, action de héros avec héros épuisé). Rouge par substitution (piercing retiré, Riposte à 0, épuisement retiré) : 3 cas rouges sur 5 (les deux témoins restent verts). Restauré, 8/8 `[jig]` verts.
- [x] Limite imprimée : NON. Autoplay : couvert par les 16 parties précédentes (la carte est dans le deck Jigsaw). Plateau : NON (attachement standard).
Carte terminée : OUI (script). Boost ATK+ « 1** » dépend du doute n°2 (étoile).

### pu059 : Bushwhacker

- [x] Étape 2 : références sk099/sk185 (`WhenUnitWouldAttack` + `SetBeInstead`), 27176 (`ChooseAbilities` + coût), 60133 (indirect sur l'identité).
- [x] Question à l'utilisateur (21/10) : qui encaisse et paie ? Réponse : le joueur visé (engagé avec Bushwhacker).
- [x] Étape 7 : 2 cas `[jig] pu059` verts (3 indirects sur le héros ; paiement de [mental] → 3 dégâts sur Jigsaw, héros indemne). Rouge par substitution : le cas « payer » passe au rouge. ⚠ Le cas 1 reste vert quand on retire `SetBeInstead` (ATQ 0★ : l'attaque ne ferait aucun dégât de toute façon) : l'effet « à la place » n'est donc prouvé que par l'ATQ 0. Les « 3 dégâts indirects sur un ennemi » passent par `DamageProperty(is_indirect_damage=True)` (`TakeIndirectDamage` n'agit que sur le camp d'un joueur).
- [x] « ★ » de l'ATQ (`0**`) : doute n°2. Limite imprimée : NON. Plateau : NON.
Carte terminée : OUI (script).

### pu063 : Man Mountain Marko

- [x] Étape 2 : 60133 (Pedestrians). Teamwork et Toughness natifs (fiche `teamwork.md`).
- [x] Étape 5/6 : **`desc.Teamwork = "MAGGIA"` manquait à l'échafaudage** (le texte l'imprimait, pas le `desc`) : ajouté dans `cards.json` (checksum recalculé) et dans `defs/punisher_cards.py`. Tout autre mot-clé natif des cartes à venir est à vérifier de même dans `desc`.
- [x] Étape 7 : 4 cas `[jig] pu063` verts (épuisement ; témoin ; Teamwork avec un autre MAGGIA en jeu → 3 dégâts ; témoin sans MAGGIA → aucun). Rouge par substitution : l'épuisement retiré rend le cas 1 rouge. Restauré, 14/14 `[jig]` verts.
- [x] Pas de question à l'utilisateur : « un personnage que vous contrôlez » = personnage prêt du joueur (RR).
Carte terminée : OUI (script).

### pu064 Eel, pu065 Putting the Pieces Together, pu068 Friends of Ours (21/10, sans question : la RR tranche)

- pu064 : `AfterUnitAttackUnit` ForcedResponse ; blessé → épuisé, sinon le défenseur est étourdi. 2 cas verts (héros blessé par le Quickstrike ; allié Tenace défenseur → étourdi), les deux rouges sans le script.
- pu065 : « 2 menaces par personnage MAGGIA en jeu » (sbires + vilain + alliés) ; « When Defeated » = `WhenSchemeBeDefeated(WhenDefeated, "This")` (modèle 27068), chaque joueur `Find.FindAndReveal(trait MAGGIA)`. 3 cas verts (3 menaces avec Jigsaw seul, 5 avec le Thug, défaite → Thug révélé), rouges sans le script. Crisis natif.
- pu068 : trouver/révéler un MAGGIA hors jeu puis `Worlds.Enemies.AllMinionActivateAgainstEngagedPlayer(trait=MAGGIA)`. 2 cas (Thug trouvé puis il attaque : 2 dégâts ; témoin sans MAGGIA), le premier rouge sans le script.
- ⚠ Piège de harnais : une commande qui contient la chaîne `tools/test_capacites.py` peut faire refuser le démarrage (« un autre harnais tourne ») ; passer par un script (`/tmp/jigrun.sh`).

### pu066 Cut to Pieces, pu070 A Made Man (21/10, sans question)

- pu066 : `villain.DoActivate(joueur, effect, op)`, +1 ATQ par `GainForThisActive(effect, would_message, attack=1)` (⚠ `would_message`, pas l'`activation` ni `IncreaseDamage`, qui ne changeaient rien) ; boost : 1 menace sur le complot principal + `HealHealth(1)` sur Jigsaw. 2 cas verts, rouges sans le script.
- ⚠ **Artefact de harnais** : `Puzzle.Boost(<n'importe quelle carte>)` fait attaquer Jigsaw (1 dégât mesuré sur lui) et pose 2 menaces (alter ego) ; les attendus du cas Boost en tiennent compte (témoin sans soin = 5).
- pu070 : alter ego = défausser un allié EN JEU (choisi par le joueur qui révèle ; aucun → 1 menace par joueur sur chaque complot) ; héros = 1 carte de boost face cachée à Jigsaw, +1 si un sbire MAGGIA est en jeu ; ★ boost = `RunAt.AfterEnemyActivationEnd`. 6 cas verts (dont un témoin), 4 rouges sans le script.
- Vérificateur maison `jigsaw_etat` (clé `boosts_jigsaw`) dans `tools/cas/jigsaw.py`.
- Batterie `[jig]` : 29/29.

## Bilan du set Jigsaw (21/10/2026)

13 cartes scriptées ou vérifiées (pu056a/b, 057a/b, 058, 059, 060, 063, 064, 065, 066, 068, 070), 30 cas `[jig]` verts. Autoplay 48 parties (4 scénarios dont 3 Jigsaw, normal et expert, Hammerhead en témoin) : 0 incident, 0 traceback.

# Set Hobgoblin (21/10/2026, sans question : la RR tranche)

14 cartes scriptées : Hobgoblin (pu071a/b, pu072a/b), Glider pu073, Flaming Sword pu074, Prowler pu075, Rabble pu076, The Enforcers pu077, Torn to Pieces pu078 (Obligation), Designs on Crimes pu079, Guise to Terrorize pu080, Smashing Pumpkins pu082, Wrath of the Hobgoblin pu084. « Pumpkin Bomb » = UNE fonction (`hobgoblin/__init__.py`, `ResoudrePumpkinBomb`).

- 27 cas `[hob]` (`tools/cas/hobgoblin.py`) verts. Rouge par substitution (tous les modules vidés) : 24 cas rouges sur 27 ; les 3 restants sont des témoins sans module.
- Compteur `drone` ajouté (`CardFace.COUNTER`, `compteurs-fr.ts`).
- ⚠ Pièges rencontrés : `SideScheme` n'existe pas comme nom (utiliser `EncounterSideScheme`) et une `NameError` dans un script est avalée par le moteur sans message ; pour qu'un pouvoir de base du héros se résolve, le cas doit fournir `cibles` ; `effect.GetInitiator()` peut être vide dans une Réponse forcée d'obligation (utiliser `message.trigger.GetControlByPlayer()`) ; Protection Racket (60134b) pose déjà 1 menace quand le vilain attaque ; `Puzzle.Boost` tire sa carte en tête de liste alors que `DiscardEncounterCards` la prend en fin : les cas utilisent des decks homogènes.
- Non vérifié en détail : pu075 (soutien/amélioration défaussés, branche amélioration), pu078 Alter-Ego Action sans identité épuisée possible.

Autoplay Hobgoblin (60 parties, 5 scénarios dont Hammerhead témoin) : 0 incident, 0 traceback. Les « victoires » de l'option `expert` d'autoplay sont de vraies fins de partie du dernier stade du scénario standard (II, 17 PV) : l'outil rejoue le scénario standard avec le drapeau expert, il ne charge pas les fichiers `*_expert`. 3 cas `[hob]` couvrent l'enchaînement des stades (standard et expert, par dégâts et par attaque).

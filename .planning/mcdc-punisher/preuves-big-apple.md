# Preuves PROCESSUS-CARTE : scénario 1 « The Big Apple » (environnements + 9 lieux), PU-5 fin / PU-7

Harnais : `tools/cas/big_apple.py`, préfixe `[big]`. Ville RÉELLE : `Puzzle.InstallerVille(grille, depart, en_jeu=True)` met les 9 lieux
en jeu, chacun dans la zone de SA rangée ; The City / Never Sleeps vont dans la zone commune (indice 1). Lancer :
`bash <script>` avec le filtre `[big]` (le filtre est une sous-chaîne, pas une regex ; une commande contenant le nom du harnais est refusée).
Méthode de substitution : copie du script, `sed` qui casse UNE chose (limite, condition de lieu, effet), relancer, constater rouge, restaurer.

⚠ Pièges trouvés en route (à reporter dans RECETTES-MOTEUR) :
- `Puzzle.CreateEncounterDeck(a, b, c)` : le DESSUS du deck est le DERNIER argument.
- `SetTarget(check_fn=...)` est IGNORÉ pour une cible `from_where=["YourHandCards"]` (jamais appelé) ; `traits=[...]` (OU) marche. Pour une cible `Identity`, `check_fn` est bien appelé.
- Un témoin « pas au lieu » placé dans une AUTRE rangée reste vert sans `Ville.AuLieu` (la zone suffit à bloquer) : le placer dans la MÊME rangée.
- Un ennemi hors de la zone du joueur n'est pas ciblable (R5) : monter un sbire AVANT `InstallerVille` pour qu'il suive le joueur.

### pu005 : The City
- [x] Étape 2 : mu004 (Action d'environnement, coût `Exhaust("YouControlUnit")`), pu121 (`Spend(Cost("1"))`), gmw/16073b (`SetTarget(lambda effect: ...)`).
- [x] Étape 5 : « or » du coût = DEUX Actions jumelles (une par coût) ; aucune limite par round ; les deux puces de règle sont portées par `Ville.Installer` / `Ville.AuLieu`.
- [x] Étape 7 : 3 cas `[big] pu005` (épuiser → Theater District, zone change ; 1 ressource → Lower East Side, même zone, perso pas épuisé ; deux déplacements dans le même round). Script retiré : 3 rouges. Restauré : 3 verts.
- [x] Limite imprimée : NON (témoin d'absence de limite = le 3e cas). Plateau : OUI (jeton de position : PU-8, interface).
Carte terminée : script OUI ; interface (jeton) à faire en PU-8.

### pu031 Theater District
- [x] Réf. mu004 + pu066. 3 cas : soin 4→2 ; témoin d'épuisement (2e Action avec un allié blessé : refusée) ; témoin pas-au-lieu (Hell's Kitchen, même rangée).
- [x] Substitution : sans limite → épuisement rouge ; sans AuLieu → témoin rouge ; soin à 0 → 2 rouges.
Carte terminée : OUI.

### pu036 Soho
- [x] Réf. ar010 (coût +1), 28020 (DrawUp/DiscardHandCards), pu031. 6 cas : Haymaker (2) refusé avec 2 icônes à Soho ; témoin Midtown ; témoin Financial District (même rangée) ; pioche 2/défausse 2 (main 3, deck 31→29) ; épuisement ; pas-au-lieu.
- [x] Substitution : coût +0, coût sans AuLieu, sans limite, Action sans AuLieu, sans pioche : chacune fait rougir au moins un cas.
Carte terminée : OUI.

### pu034 Midtown
- [x] Réf. 12024 (`PlayCardsLikeInTurn(..., update_resources_cost=-1)`), 28020 (« a player » = cible Identity), pu031. 5 cas : Black Widow (3) jouée avec 2 icônes ; témoin sans l'Action ; témoin de trait (Jessica Jones DEFENDER non éligible) ; épuisement (Hellcat reste en main) ; pas-au-lieu (West Village).
- [x] Substitution : sans réduction, sans limite, sans AuLieu, sans traits, sans script : tous rouges.
- ⚠ NON PROUVÉ : le filtre « joueur dans ce territoire » (`check_fn` sur Identity) à DEUX joueurs : le harnais ne sait pas donner une main au joueur 2. Appelé (vérifié par trace), non mesuré.
Carte terminée : OUI, sauf ce point (à vérifier en partie réelle à deux joueurs dans des rangées différentes).

### pu032 Upper East Side
- [x] Réf. jj008, 24030. `EncounterSideScheme` (pas la principale). 3 cas : annexe révélée après 1 traitrise défaussée ; épuisement (la 2e annexe reste dans le deck) ; pas-au-lieu.
- [x] Substitution : sans limite, sans AuLieu, sans reveal, type Minion : tous rouges.
Carte terminée : OUI.

### pu038 Chinatown
- [x] Réf. 53009 (`WhenPlayerWouldBeDealtEncounterCard` + `SetBeInstead`), 16057. « When YOU would be dealt » = le joueur au lieu. 3 cas : traitrise non distribuée, Shocker révélé (1 dégât) ; épuisement ; pas-au-lieu.
- [x] Substitution : sans limite, sans AuLieu, sans instead, sans reveal : tous rouges.
Carte terminée : OUI.

### pu037 Financial District
- [x] Réf. 15030 (`Worlds.FindVillain(effect).DoAttackYou`), 27151, 53003 (`FacesCounter.CountTotalBoostStarAndBoost`). 5 cas : Tough + boost 2 icônes → pioche 2 ; boost pu131 (1 icône + ★) → pioche 2 ; 3 dégâts → aucune pioche ; épuisement ; pas-au-lieu. Le CAPO de la rangée est mis dans la zone du joueur.
- ⚠ Spider-Man pioche 1 (Spider-Sense) quand le vilain l'attaque : la main compte ce +1.
- [x] Substitution : la 1re passe était FAUSSE-VERTE (`atk.attacked` n'est pas une liste → exception avalée → aucune pioche, cas « 3 dégâts » vert par accident). Corrigé ; sans limite / sans AuLieu / sans attaque / seuil 4 / seuil 0 / sans étoile : tous rouges.
Carte terminée : OUI. « You take » = l'identité (allié défenseur = 0 pour vous) : lecture à confirmer en partie réelle.

### pu035 Lower East Side
- [x] Réf. up039 (`TemporaryGain(effect, would_atk_message, retaliate=+1)` sur `WhenCalculatingAttackDamage`), `GiveKeywordToInPlayWhenApplyThis(..., get_new_value, change_on_event)`. Message ajouté : `Message.AfterPlayerMovedInCity` (envoyé par `Ville.Installer` et `Ville.Deplacer`).
- [x] 8 cas : riposte du héros, du sbire engagé, du vilain (par attaque) ; témoins Midtown ; arrivée/départ. Substitutions : sans continu, sans lieu, sans message, sans riposte du vilain, vilain partout : tous rouges.
Carte terminée : OUI.

### pu033 West Village
- [x] Réf. an002/06007 (+1 hand size, Identity = les deux formes), 39026b (`WhenVillainPhaseStepStart(ForcedInterrupt, 3, ...)`). 7 cas dont l'alter ego, arrivée/départ, phase du vilain (Rhino déplacé dans la zone ; Jigsaw évité car il met un sbire en jeu depuis le dessus du deck).
- [x] Substitution : sans carte, sans taille, sans lieu, sans message : rouges.
Carte terminée : OUI.

### pu030 Hell's Kitchen
- [x] Réf. ip018 (`CheckIfUnitCanThwart` + `SetCannotThwart`), `Search.EncounterCard`, 27150 (`CostFunc.Custom`), sk024. « cannot scheme » des sbires = `WhenUnitWouldScheme` + `SetBeInstead` (rien n'arrive, pas de boost) : décision, la RR ne prévoit que « si on ne peut pas, rien ».
- ⚠ `CardFinder(...) & CardFinder(...)` plante (`issubclass`) dans `Select.From(finder=...)` : la 2e condition de coût passe par `conditions=[peut_payer]`.
- [x] 12 cas (toughness sbire/allié/arrivée, allié ne contre pas, sbire ne manigance pas, Action + 2 témoins de coût + pas-au-lieu). Substitutions : 9 variantes, toutes rouges (`peut_payer` demandait un cas dédié : identité déjà Tough).
Carte terminée : OUI.

### pu006 Never Sleeps
- Aucun script : les trois puces sont la structure même de la ville (une zone par rangée, vilain par zone, manigances communes), prouvées par les cas `[ville]` (R5, R6, R7) ; pas de capacité propre à scripter. Carte terminée : OUI (à relier au Setup du scénario).

### pu048a/b ... pu055a/b : les 8 CAPO (16 faces, p095-p110) : `[capo]`, 30 cas
Harnais : `tools/cas/capos.py`, scenario `rhino`, le CAPO mis en jeu a cote, `Puzzle.EnemyAttacks`. Scripts : `capos/__init__.py` (une fabrique par CAPO, la face B ne change qu'un nombre ou un mot).
Mots-cles ouverts avant d'ecrire : overkill, ranged (fiches), boost. PV non par joueur (pied de carte « HIT POINTS 13 »), pas de stade imprime.
- [x] Etape 2 : refs. Kang I (toafk/kang/__init__.py : Forced Interrupt + deux branches + `GainForThisActive`) pour The Rose / Mister Negative ; Jigsaw (`AfterUnitAttackUnit(ForcedResponse, "This", "You")`) pour Ringmaster / Yulan / Nightshade ; M.O.D.O.K. 50107b (`UnitAttackGainKeyword("This", overkill, ranged)`) pour Nefaria ; sk100 (`GiveAdditionalBoostCardForThisActivation`) ; fne 60132 (`PeutCouvrirLeCout`, branche payante offerte seulement si payable) ; pu077 (`TakeIndirectDamage`) ; spot sp014 (`dealt_more_than_damage`) pour Diamondback.
- [x] Etape 5 : mots-pieges. « you » = le joueur attaque ; « each minion engaged WITH YOU » (pas tous les sbires) ; « to a maximum of +2 » (cas a 3 sbires) ; « After X attacks » (Reponse) vs « When X attacks » (Interruption) respectes ; « After this attack, stun » = `RunAt.AfterEnemyActivationEnd`, pas tout de suite ; « 1 indirect damage for each ally » = un bloc de N (allies seulement, pas l'identite) ; « takes at least 3 damage from an attack » = `dealt_more_than_damage=3` sur UNE attaque ; « Spend a [mental] resource » = `Cost("B")` (le joker paie) ; face B Mister Negative : « and this attack gains overkill » dans la 1re branche seulement.
- [x] Etape 6 : nombres. ATQ/SCH/PV des 16 faces relus sur les scans (p095 p097 p104 p109 vus ; le reste conforme a cartes.md) ; heal 2/3 et defausse 6/10 (Yulan), +2 ATQ / 2 menaces (Rose), plafond +2 (Crime-Master), seuil 3 (Diamondback).
- [x] Etape 7 : preuve par substitution (module vide, 8 passes) : Nefaria 3 rouges ; Crime-Master 3 rouges (le cas « aucun sbire » reste vert : base) ; Ringmaster 4 rouges ; Yulan 3 rouges ; Mister Negative 3 rouges (le temoin face A reste vert : il prouve l'ABSENCE d'overkill) ; Rose 3 rouges ; Nightshade 3 rouges (« aucun allie » vert) ; Diamondback 2 rouges (le cas « 2 degats < 3 » reste vert : temoin du seuil). Temoins : pu055a (sans overkill ni ranged) pour Nefaria, pu052a pour pu052b.
- ⚠ Pieges : Spider-Sense pioche une carte apres l'attaque (« 01062 » en main) : un test « aucune ressource mentale en main » doit remplir le deck (`Puzzle.CreatePlayerDeck`) ; `Puzzle.CreatePlayerDeck` AJOUTE au deck ; `defausse_joueur` est un compteur, pas une liste ; `dans_deck_rencontre` / `defausse_rencontre` sont des tests de PRESENCE : pour compter les cartes de boost, utiliser deux cartes DIFFERENTES (la 2e a des icones : Shocker 2) ; une attaque ENNEMI contre un vilain/allie ne pose pas la question « Defense » (pas de `passer_sur_option`).
- Limite imprimee : NON. Etape 8 (autoplay) : reportee au scenario jouable. Etape 8 bis (plateau) : NON (les CAPO sont des vilains ordinaires ; la rangee / jeton de position : PU-8).
Carte terminee : OUI (script) pour les 16 faces ; mise en place (3 au hasard, un par rangee) = Gang War.

### pu039 ... pu047 : les 9 PISTES (LEAD, p077-p093) : `[pist]`, 29 cas
Harnais : `tools/cas/pistes.py` (ville reelle, piste dans l'aire du joueur, paquet LEADS cree par `Puzzle.CreateLeadsDeck`, nouveau). Scripts : `leads_the_big_apple/` (`__init__.py` : `Joueur`, `EnLieu`, `CreerPaquetPistes`, `RevelerPiste`, `PisteTerminee`, `CompteurPuisFin`).
Engine : paquet `LeadsDeck` ajoute a `Worlds.ASIDE_DECK_NAME` (modele PlanetDeck) ; compteurs `bouncer culture curse rent stock takeout dojo hustle quell` ajoutes a `CardFace.COUNTER`.
- [x] Etape 2 : refs. vz035 (`Ability(Response, Message.AfterUnitHealHealth ...)`), skrull_empire `CreerPaquetPlanete/RevelerPlanete` (deck commun), fne typhoid_mary (jetons `damage`, `SetBeInstead`), tuck.md (`TuckCardUnderHere`), fabriques `AfterUnitDefeatedScheme/AfterPlayerRevealCard/AfterPlayerPlayedCard/AfterUnitDefendAgainstAttack/AfterUnitDefeatedUnit`.
- [x] Etape 5 : mots-pieges. « While in X » lu AU DECLENCHEMENT (`EnLieu`) ; « you » = le joueur dans l'aire duquel est la piste ; seuils 3/3/—/4/3/8/3/3/2 (pu042 : 4, pu047 : 2, pu044 : 8 degats) ; « Then, if there are N or more » apres le compteur ; fin commune = victoire + piste du dessus + 1 carte ; pu044 « instead » = le vilain ne subit rien.
- ⚠ DECISIONS SANS TEXTE DE RR (a confirmer en partie reelle) : pu039 « a minion or ally you control » = tout sbire defait dans son territoire OU un allie que je controle ; « you defend / you thwart » = l'IDENTITE (pas un allie) ; « you defeat » (pu047/pu041) = la fabrique « You ».
- [x] Etape 6 : nombres relus (texte ↔ code). Etape 7 : substitution (module vide) : pu039 4 rouges, pu040 2, pu041 1, pu042 3, pu043 2, pu044 2, pu045 2, pu046 2, pu047 2 ; le temoin « pas au lieu » reste vert (absence d'effet).
- ⚠ Pieges : `GetControlByOrOwner()` d'une obligation rend le VILAIN : le joueur = `Obligation.GetGaveToPlayer()` ; `AbilityFactory.AfterUnitThwartScheme(..., "You")` ne lit PAS « You » (chaine passee a `CheckWhichCard`) : `Ability` a la main ; `AfterUnitDefendAgainstAttack("You")` = identite seulement ; `Puzzle.Attack('<ennemi>')` fait attaquer l'ennemi : pour que le HEROS attaque, `Puzzle.Attack('01001a')` + `cibles=[...]` ; `Puzzle.PlaceCounters` sur la piste avant qu'elle soit en jeu : mal ordonne (le harnais range ces lignes APRES la piste).
- Limite imprimee : NON. Etape 8 : au scenario jouable. Etape 8 bis : la piste glisse une carte (pu043) et pose des compteurs : a montrer en PU-8 (interface).
Carte terminee : OUI (script) pour les 9 ; Uptown (3 pistes) a faire avec l'extension.

### pu001a/b, pu002a/b, pu003a/b, pu004 : les 3 complots et Gunrunner (p001-p007) : `[gang]`, 20 cas
Harnais : `tools/cas/gang_war.py`. VRAIE mise en place (`data/scenarios/the_big_apple*.json`, `villain: []`, 3 CAPO tires au hasard : mesures independantes de leur identite) + montage deterministe (`rhino` + Diamondback pu055a). Scripts : `the_big_apple/` (`MettreEnPlaceLaVille` dans `__init__.py`).
Engine ajoute : `World.AdvanceMainScheme` met le NOUVEAU stade dans la zone commune quand elle existe (sinon ses When Revealed ne repondent pas) ; `Puzzle.CreateLeadsDeck / AddToVictoryDisplay / PlaceCountersOnVillains / DamageAllVillains`.
- [x] Etape 2 : refs. earth_under_siege gs161a (`WhenCardSetup`, `villain: []`, `Villains.BuildVillainDeck/RevealNextVillain/SetRule`), fne typhoid_mary (`WhenUnitWouldBeDefeated` + `SetBeInstead` + `ResetHealth`), gmw 16073b (`AfterCardsMoved`), pu092 (`GiveKeywordToAttached` + `WhenUnitBeDefeated`), pu109 (`AttachTo2`), `Faces.SetAside`, `RemoveThreatFromSchemes`.
- [x] Etape 5 : mots-pieges. « a villain » (1B/2B) = n'importe quel CAPO ; « 2[per hero] LEAD » = 2 x joueurs (`ConvertPerPlayerIconToInt("2*")`) ; « each villain has at least 1 quell » = TOUS les CAPO en jeu (`GetAllVillains`, pas la zone) ; « each player » (2A) = tous les joueurs (`Worlds.GetPlayers` filtre par la ZONE de la carte : un complot de la zone commune n'y voit personne, d'ou `TousLesJoueurs`) ; « reveal a random CAPO from the set-aside area » = un CAPO PAS en jeu (les 5 restants) ; « set all other CAPOS aside » ; « each player is considered to be in their turf » (3B) = tous les joueurs rejoignent la zone du CAPO Gunrunner et la grille disparait (`world.ville = None`) ; Gunrunner « +7 par joueur » ; la 1re vague de degats sur le CAPO porteur est absorbee par sa carte Tough.
- [x] Etape 6 : nombres. 1B : 9/1/+1 par joueur, retrait de 5 ; 2B : 8/2/+1 ; 3B : 9/0/+1 ; seuil de 2 pistes par joueur ; Gunrunner +7, SCH +1, ATQ +1 (relus sur p001-p007 vus et cartes.md).
- [x] Etape 7 : substitution (module vide, 6 passes) : pu001a 5 rouges sur 5 ; pu001b 3 rouges (les 2 temoins verts) ; pu002a 2/2 ; pu002b 2 rouges (le temoin vert) ; pu003a 1/1 ; pu004 3 rouges (le temoin « avant 3A » vert).
- ⚠ Pieges : Great Responsibility (01061, Spider-Man) est jouee par le pilote et annule `Puzzle.SetThreat` : `main_exclusive` ; la face A d'un complot se retourne SEULE sur B (2A -> 2B, 3A -> 3B) : tester `pu002b` / `pu003b` ; `Player.game_area` n'existe pas : `GetIdentity().card.GetGameArea()` ; `zone.AddCard` plante si la carte y est deja (exception avalee) ; attendre `AdvanceMainScheme(1)` une fois par etape.
- A faire plus tard : « deal any cards attached to locations as facedown encounter cards » (3A) : code ecrit, NON PROUVE tant que les attachements de lieu (pu007, pu008, pu010) n'existent pas ; la parenthese de campagne de 2A (noter le lieu de la derniere piste) : PU-9.
Carte terminee : OUI (script) sauf le point ci-dessus (3A, cartes attachees aux lieux).

### Cartes de rencontre, lot 1 : pu009 Hunted by the Past, pu011 Bellona, pu012 Black Tarantula, pu016 Busted!, pu017 Conflicting Evidence, pu018 Red Herring, pu020 Shootout, pu021 Bank Robbery : `[renc]`, 22 cas
Harnais : `tools/cas/big_apple_rencontre.py`. Engine : `Ville.Placer` (deplacement sans adjacence, Red Herring).
- Refs : Machete 50098 (Bellona), 01166 Highway Robbery (Bank Robbery), 27153 / valk 25028 (Busted!), pu110 (`do_not_give_boost`), gs204 (`OnEvent.Victory`), pu109 (Hunted), `CardFinder(is_nemesis=joueur)`.
- Substitution (module vide) : toutes rouges sauf les temoins ; pu017 verifie en plus en retournant `do_not_give_boost` (2 rouges).
- DECISIONS SANS TEXTE DE RR : Busted! « you cannot attack the villain » = identite ET allies ; Red Herring exclut aussi le lieu actuel et laisse le joueur choisir ; Shootout « character in this turf » = identites, allies et sbires de la zone + le CAPO.
- ⚠ Pieges : `EnemyAttacks` ne distribue PAS de carte de boost (utiliser `Puzzle.Attack('<ennemi>')` ou `Puzzle.Boost`) ; `Puzzle.Action(card, 'AlterEgoAction')` ; une carte Tough absorbe la 1re vague de degats ; `Puzzle.Boost` pour tester un Boost.
- Non prouve : Red Herring et Shootout en mode EXPERT (incite 1, epuisement) : pas de cas expert.
Cartes terminees : OUI (hors point expert).

## Bilan (22/10/2026)
11 cartes de lieu/environnement faites : 55 cas `[big]` verts, 15 `[ville]` verts, `test_cards` : 7103 ok, 0 erreur. Non fait : autoplay ciblé (étape 8, il faut le scénario jouable) et plateau (étape 8 bis, PU-8).

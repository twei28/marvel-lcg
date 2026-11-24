# Smasher (Starjammers) : gabarits PROCESSUS-CARTE, 26/10/2026

Pack `smasher` (prefixe `sz`, set 228, auteur Phenexian). Scripts : `src/cards/pack/smasher/{smasher,smasher_nemesis}/` et `sz015.py` a la racine (Team-Up Basic).
Cas : `tools/cas/smasher.py` (cas `[sz]`, 67) ; plateau : `ui-app/src/board/smasher-plateau.test.ts` (3 cas) ; deck `smasher` ; recettes `RECETTES-MOTEUR.md` §33.

**Aucune carte n'est « terminee »** : il manque la partie reelle jouee par un humain (voir la fin), et plusieurs cartes portent une question de regle en suspens (choix provisoire code, consigne utilisateur du 25/10/2026 : les questions sont gardees pour la fin).

**Sources** : zip `Starjammers-...zip`, dossier `Smasher (Hero)/` uniquement (21 PNG de cartes, `Hero Pack` = visuel de boite sans texte, compteur de PV, 3 reskins de ressources, Team-Up `Power Couple`). Pas de decklist imprimee : `player_deck` vide. Pas de regle de deckbuilder imprimee : aucune entree dans `regles.js`.

**Modification du MOTEUR** (une seule, marquee `# CORRECTIF`) : `src/game/card/face/card_face.py`, ajout du trait `EXOSPEX` a la liste `TRAITS` (sans lui la partie ne se monte pas).

**Autoplay** (`tools/autoplay.py`, Rhino normal, profil equilibre, 8 parties) : Smasher 8 parties TERMINEES (0 victoire, 5 « manigance accomplie », 3 « tous elimines », 4,6 rounds), 0 exception, 0 blocage ; temoin Spider-Man : 8 parties terminees (0 victoire, 6,9 rounds), 0 blocage. Aucune victoire de Smasher : le deck de joueur est vide (pilote seul, comme les autres decks fan-made sans liste). **Preuve par substitution** : `tools/substituer_pack.py` sur les 16 modules a script, le pack est IDENTIQUE avant et apres (md5 b50bfc54…), chaque carte a au moins un cas rouge sans son module (detail a chaque carte). **Verifications finales** : 67/67 cas [sz], test_cards 7 664 modules 0 erreur, verifier_tous_les_decks 171/171 (deck smasher monte une partie), verifier_prefixes / verifier_cibles / verifier_desc_mots_cles OK, verifier_appels_modules OK (calibre : `Faces.MethodeInventee` est vu), tests de vocabulaire FR (19) et plateau (3) verts.

**Defaut de MESURE trouve par la substitution** : les premiers cas de `sz001a` (Forced Response) restaient VERTS 5/5 module vide. Cause : `defausse: ["sz005"]` lit la defausse ENTIERE, or le harnais y jette la main de depart (`main_exclusive`), qui contient d'autres exemplaires de la meme amelioration. Remplace par `hors_jeu: [..]` (la carte EN JEU est partie) : `sz001a` rougit 2/5, les cinq cas d'Accessing aussi corriges. Voir RECETTES §33.

---


### sz001a : * Smasher (face heros)

- [x] Etape 2 : carte(s) de reference : 56029b Teddy Altman (meme famille « une seule amelioration [[Shapeshift]] ») et hz001a (`AfterPlayerPlayedCard(.., "You", <filtre>, op)`).
- [x] Etape 5 : mots-pieges verifies : « all OTHER » (la carte jouee reste : `message.played_face`) ; « you control » (toutes les EXOSPEX que le joueur controle, `GetControlCardsByType(upgrade=True)`) ; **Forced** Response (se resout avant les Responses des ameliorations).
- [x] Etape 6 : nombres texte <-> code : PV 12, ATK 1, THW 1, DEF 1, HS 5 (scan) = `desc` = cas de valeurs imprimees. Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : valeurs imprimees ; Hyper-Speed jouee avec Penta-Vision en jeu -> Penta-Vision `hors_jeu`, Hyper-Speed reste ; TROIS EXOSPEX -> les deux autres partent ; CONTRE-CAS soutien (Home on Chandilar) ; CONTRE-CAS amelioration sans le trait (01027). Substitution : **rouges 2/5** (les deux cas nominaux ; les 3 verts sont les valeurs imprimees et les 2 contre-cas d'absence, assumes).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q1 : la Forced Response vise-t-elle aussi les EXOSPEX attachees a un AUTRE personnage que Smasher (choix code : toutes celles qu'on controle, quel que soit l'hote) ?.

### sz001b : * Izzy Kane (face alter ego)

- [x] Etape 2 : carte(s) de reference : 56029b Teddy Altman (restriction `PlayersCannotPlayCardWhile` + Action `Search.PlayerCard(.., include_player_deck=True, include_discard_pile=True, trait=..)` + `Faces.AddToHand`).
- [x] Etape 5 : mots-pieges verifies : « cannot have MORE THAN 1 » (la 2e ne se pose pas, au lieu d'une defausse) ; « deck AND discard pile » (les deux sont fouilles) ; « once per TURN » (voir limite).
- [x] Etape 6 : nombres texte <-> code : PV 12, REC 3, HS 6 (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : valeurs imprimees ; 2e EXOSPEX non jouable en alter ego (reste en main) ; CONTRE-CAS sans EXOSPEX en jeu elle se joue ; Battle Ready trouve une EXOSPEX dans le DECK (`sz_main`) et dans la DEFAUSSE (`cibles` obligatoire : le deck de heros contient d'autres EXOSPEX). Substitution : **rouges 4/6** (les verts : valeurs imprimees et contre-cas).
- [x] Etape 7 bis : limite imprimee ? OUI : « once per TURN ». **CORRIGE le 26/10/2026 (RR « Action »)** : la limite est maintenant PAR TOUR (`PlayerStat.this_turn_limited_abilities`, videe a chaque tour, ajout moteur additif ; condition locale du module), plus `LimitOncePerRound` : un tour de plus dans le meme round (rm007) rouvre l'Action. Temoin d'epuisement : « TEMOIN D'EPUISEMENT » (2 declenchements dans le meme tour, le 2e dans `declencher_tolerant`) : taille de main 2 (la Strength de depart + UNE seule EXOSPEX), alors que deux sont dans le deck ; **nouveau cas « tour suivant »** (`Puzzle.NewPlayerTurnStat`, ajout au banc) : 1re Action, fin du tour, 2e Action : DEUX EXOSPEX en main (3 cartes), vu ROUGE avant le correctif (« n'offre aucune action disponible »), vert apres. Substitution (module vide) : rouges 5/7.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine non faite (le tour de plus de rm007 n'est pas exercable par un cas : seul l'autoplay le montre).

### sz002 : * Cannonball (Sam Guthrie), allie

- [x] Etape 2 : carte(s) de reference : 49035 Bling! (« gains toughness » conditionnel : `ThisGainKeyword(.., toughness=1, change_on_event=OnEvent.Trait("YourIdentity"))`) ; 01017 Cosmic Flight (trait AERIAL donne a l'identite).
- [x] Etape 5 : mots-pieges verifies : « an AERIAL card » = TOUT type de carte (evenement, amelioration, allie), filtre par trait seul ; « has toughness IF your identity has AERIAL » (conditionnel, recalcule quand l'identite change de trait).
- [x] Etape 6 : nombres texte <-> code : cout 3, PV 3, ATQ 2 THW 2 avec **deux icones de degats consequents chacun** (`"2**"`, scan), [wild] (icone verte etoile, comparee a `01020` Hellcat RES G). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : valeurs imprimees (PV, traits) ; identite AERIAL (Exo-Flight en jeu) -> entre en jeu avec Tough ; CONTRE-CAS identite non aerienne, mis en jeu sans etre JOUE -> pas de Tough ; Response : Power Couple jouee -> Tough ; CONTRE-CAS Home on Chandilar jouee -> pas de Tough ; jouer Cannonball LUI-MEME (carte AERIAL) lui donne Tough (comportement du moteur). Substitution : **rouges 3/6** (verts : valeurs, contre-cas, jeu de Cannonball lui-même : voir Q3).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (statut Tough : affichage standard).
Carte terminee : NON (provisoire) : partie reelle humaine ; Q3 : « After you play an AERIAL card » inclut-il Cannonball LUI-MEME quand on le joue (choix code = le comportement du moteur : oui, il se donne une carte Tough) ?.

### sz003 : * Home on Chandilar (soutien)

- [x] Etape 2 : carte(s) de reference : 01045 The Golden City (texte identique : `AlterEgoAction` + `Exhaust("This")` + `DrawUp(2)`).
- [x] Etape 5 : mots-pieges verifies : « Alter-Ego Action » (pas Hero Action) ; « draw 2 cards » (`DrawUp(2)` pioche DEUX cartes, pas jusqu'a la taille de main).
- [x] Etape 6 : nombres texte <-> code : cout 2, [physical] (icone poing, comparee a `01023` RES R), LOCATION SHI'AR. Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : Action en alter ego : s'incline et pioche 2 (main videe avant : 2 cartes) ; valeurs imprimees. Substitution : **rouges 1/2** (le vert : valeurs imprimees).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine.

### sz004 : Accessing (evenement)

- [x] Etape 2 : carte(s) de reference : 01043a Wakanda Forever! (`SetTarget(Upgrade, trait=.., from_where=["YouControlCards"])`, choix d'une amelioration controlee par son trait) ; `ResolveSpecialAbility` n'existe que pour « Special » : on rejoue donc les fonctions des cinq Hero Responses (set `__init__.py`, `ResoudreLaReponseDe`).
- [x] Etape 5 : mots-pieges verifies : « Resolve the Hero Response ability » (la capacite est rejouee SANS son declencheur « after you play ») ; « Then discard » (la defausse suit TOUJOURS) ; « an EXOSPEX upgrade you control » (sans cible legale la carte n'est pas jouable).
- [x] Etape 6 : nombres texte <-> code : cout 0, [mental] (icone bleue, comparee a `01022` RES B), SUPERPOWER. Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : un cas par amelioration : Penta-Vision (3 degats a Rhino), Hyper-Strength (Rhino sonne), Hyper-Speed (heros incline se redresse), Super-Resistance (Tough sur le heros), Exo-Flight (menace 5 -> 2), chacun avec `hors_jeu` de l'amelioration ; CONTRE-CAS aucune EXOSPEX en jeu -> carte non jouable. Substitution : **rouges 5/6** (le vert : le contre-cas d'absence).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
**Q4 TRANCHEE le 26/10/2026 (RR « Labeled Ability »)** : resoudre une capacite etiquetee « (attack) » = une attaque de l'identite. `ReponsePentaVision` (set `__init__.py`) appelle maintenant `AttackDamage` (attack_in_event), qui sert aussi la Response jouee de la main. Cas ajoutes : Accessing -> Penta-Vision avec Smasher SONNEE : le Sonne part et Rhino ne prend rien (vu ROUGE avant : 3 degats et le Sonne reste ; ROUGE aussi quand on remet `DealDamage` a la place d'`AttackDamage`), TEMOIN sans Sonne (3 degats), TEMOIN de l'etiquette (Penta-Vision jouee de la main, Sonne : meme resultat que par Accessing).
Carte terminee : NON (provisoire) : partie reelle humaine non faite.

### sz005 : Penta-Vision (amelioration EXOSPEX)

- [x] Etape 2 : carte(s) de reference : 01017 Cosmic Flight (bonus attache) ; fiche ranged.md (`UnitAttackGainKeyword("You", ranged=True)`, permanent) ; 62009 (`AfterYouPlayThisFromHand`) ; 08010 Widow's Bite (Hero Response (attack) : `.SetLabel('attack')` + cible).
- [x] Etape 5 : mots-pieges verifies : « Smasher's attacks gain ranged » (permanent, pas ponctuel) ; « Hero Response » (sous-type dedie `AbilityType.HeroResponse`) ; « after you play Penta-Vision » (`AfterYouPlayThisFromHand`, depuis la main seulement).
- [x] Etape 6 : nombres texte <-> code : cout 1, [mental] ; +1 ATK, +1 THW ; 3 degats (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : bonus (ATK 2, THW 2) ; Hero Response : 3 degats a Rhino ; ranged : attaque d'un sbire a Riposte 1 (Whiplash) -> 0 degat au heros, TEMOIN Hyper-Speed (sans ranged) -> 1 degat de riposte ; valeurs imprimees. Substitution : **rouges 3/5** (verts : valeurs et temoin de riposte).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine.

### sz006 : Hyper-Strength (amelioration EXOSPEX)

- [x] Etape 2 : carte(s) de reference : 01017 ; fiche overkill.md (`UnitAttackGainKeyword("You", overkill=True)`) ; 62009.
- [x] Etape 5 : mots-pieges verifies : « +2 ATK » ; « overkill » (l'exces va au vilain) ; « stun an enemy » (cible a choisir).
- [x] Etape 6 : nombres texte <-> code : cout 1, [physical] ; +2 ATK (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : bonus (ATK 3) ; Hero Response : Rhino sonne ; overkill : sbire a 1 PV restant, ATK 3 -> 2 degats d'exces a Rhino ; TEMOIN Hyper-Speed (ATK 2, sans overkill) -> 0. Substitution : **rouges 3/4** (le vert : le temoin d'overkill, qui vaut avec ou sans module puisqu'il utilise Hyper-Speed).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine.

### sz007 : Hyper-Speed (amelioration EXOSPEX)

- [x] Etape 2 : carte(s) de reference : 01017 ; 01082 Indomitable (`ReadyAll([hero])`).
- [x] Etape 5 : mots-pieges verifies : « +1 ATK, +1 THW and +1 DEF » (trois bonus) ; « ready Smasher » (un heros deja pret n'est pas un echec).
- [x] Etape 6 : nombres texte <-> code : cout 1, [energy] (icone jaune, comparee a `01025` RES Y). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : bonus (2, 2, 2) ; Hero Response : le heros incline se redresse. Substitution : **rouges 2/2**.
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine.

### sz008 : Super-Resistance (amelioration EXOSPEX)

- [x] Etape 2 : carte(s) de reference : 01017 ; fiche stalwart.md (`GiveKeywordToAttached(.., stalwart=1)`) ; 01105 (`Faces.GiveStatus([..], "Tough", effect)`).
- [x] Etape 5 : mots-pieges verifies : « +2 DEF and gains Stalwart » (Stalwart = Robuste en francais) ; « tough status card » (Tenace).
- [x] Etape 6 : nombres texte <-> code : cout 1, [physical] ; +2 DEF (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : bonus (DEF 3, Stalwart 1) ; Hero Response : Tough sur le heros ; Stalwart : `Puzzle.Stun` ne pose aucune carte Sonne. Substitution : **rouges 3/3**.
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine.

### sz009 : Exo-Flight (amelioration EXOSPEX AERIAL)

- [x] Etape 2 : carte(s) de reference : 01017 Cosmic Flight (`GiveKeywordToAttached(.., trait="AERIAL")`) ; 47004 Jubilee's Coat (Hero Response (thwart) : `.SetLabel('thwart')` + `.SetTarget(Scheme2)`).
- [x] Etape 5 : mots-pieges verifies : « gains the AERIAL trait » (le trait va a l'IDENTITE, pas a l'amelioration) ; « remove 3 threat » (menace posee avant : le cas mesure un chiffre).
- [x] Etape 6 : nombres texte <-> code : cout 1, [energy] ; +1 THW, +1 DEF ; 3 menaces (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : bonus (THW 2, DEF 2) + trait AERIAL sur l'identite ; Hero Response : menace 5 -> 2 ; valeurs imprimees. Substitution : **rouges 2/3** (le vert : valeurs imprimees).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine.

### sz010 : Family Matters (obligation)

- [x] Etape 2 : carte(s) de reference : gs031 Forgotten Life (obligation qui RESTE en jeu, `GiveKeywordToInPlayWhenApplyThis(.., hand_size=-1)`) ; ar010 Ire of Athena (« Exhaust A or B -> discard this » = DEUX `PlayerActionToDiscardThis(AlterEgoAction)`).
- [x] Etape 5 : mots-pieges verifies : « Give to the Izzy Kane player » (`desc.GiveTo`, aucun script) ; « hand size reduced by 3 » (toute forme) ; « DISCARD » (retourne a la defausse rencontre) ; « Exhaust Izzy Kane OR Cannonball » (deux capacites, un cout chacune).
- [x] Etape 6 : nombres texte <-> code : boost 2 icones (scan) ; -3 de taille de main. Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : taille de main 6 -> 3 en alter ego ; Action : Izzy Kane s'incline -> defaussee ; Action : Cannonball s'incline -> defaussee, Izzy Kane reste prete. Substitution : **rouges 3/3**.
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q5 : « Your hand size is reduced by 3 » vaut-il aussi en forme HEROS (choix code : oui, toute forme) ?.

### sz011 : * Scientist Supreme (Andrew Forson), sbire nemesis

- [x] Etape 2 : carte(s) de reference : ho016 Bullseye (`UnitAttackGainKeyword("This", piercing=True, ..)`, capacite etoilee permanente) ; 56176 Pheromones (`WhenThisRevealed(None, op)` + `GiveStatus` x2) ; fiche villainous.md (`desc.Villainous`).
- [x] Etape 5 : mots-pieges verifies : « Villainous » (base automatique, pas de script) ; « [star] attacks gain piercing and ranged » ; « stunned AND confused » (deux statuts) ; « Smasher's nemesis minion » (`desc.Nemesis`).
- [x] Etape 6 : nombres texte <-> code : PV 4, SCH 2, ATQ **1★** (lu 1 : l'etoile marque la capacite etoilee), boost 3 icones (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : valeurs imprimees ; When Revealed : sonne ET desoriente ; Villainous : une carte de boost par attaque (deck rencontre 8 -> 7) ; TEMOIN sbire ordinaire (8) ; perforant : Tough consommee et 1 degat passe ; TEMOIN sbire ordinaire contre Tough : 0 degat. **« ranged » non mesure** (le heros n'a aucune Riposte : meme fabrique que « piercing », une seule ligne). Substitution : **rouges 2/6** (verts : valeurs, Villainous et temoins, qui ne dependent pas du script).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q6 : l'ATQ « 1★ » est lue 1 (voir aussi Hepzibah, Q11)..

### sz012 : Entropic Subversion (manigance annexe nemesis)

- [x] Etape 2 : carte(s) de reference : 32004 Iron Will (`AfterStatusDiscardFrom(.., <qui>, "Tough", op)`) ; sk277 / ra001b (« a friendly character » = `SetTarget(Friend)`) ; 01182 (`PlaceThreatOnSchemes("MainScheme", n, effect)`).
- [x] Etape 5 : mots-pieges verifies : DEUX Forced Responses (une par statut : le filtre est un parametre de la fabrique) ; « friendly character » (un ennemi sonne ne declenche rien) ; « deal 2 damage to a friendly character » (cible a choisir).
- [x] Etape 6 : nombres texte <-> code : menace de depart 3 par heros, boost 2 icones (scan, carte en paysage). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : menace 3 ; carte SONNE defaussee d'un ami -> 2 degats ; carte DESORIENTE defaussee -> 2 menaces sur le complot principal ; CONTRE-CAS statut d'un ennemi ; CONTRE-CAS statut Tough. `Puzzle.Stun` / `Puzzle.Confuse` basculent : le 2e appel DEFAUSSE la carte et declenche la Response. Substitution : **rouges 2/5** (verts : menace de depart et contre-cas).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine.

### sz013 : Biosynthetic Sting (traitrise nemesis, x2)

- [x] Etape 2 : carte(s) de reference : 56176 Pheromones (When Revealed qui pose un statut au joueur) ; 04092 / 16140 (« [star] Boost: Reveal this card » = `WhenCardBecomeBoost("This", RevealThisCard)`).
- [x] Etape 5 : mots-pieges verifies : « Take 1 damage » (`DealDamage([identite], 1, ..)`) ; « You are stunned » ; boost ★ SANS icone imprimee (`desc.Boost = "0"`).
- [x] Etape 6 : nombres texte <-> code : boost : etoile seule (aucune icone, scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : When Revealed : 1 degat et sonne ; Boost : revelee pendant l'attaque de Rhino (2 + 1 = 3 degats, sonne) ; TEMOIN carte sans effet de boost (2 degats, pas sonne). Substitution : **rouges 2/3** (le vert : le temoin).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine.

### sz014 : Corrupting Revelation (traitrise nemesis)

- [x] Etape 2 : carte(s) de reference : 45028 Bantam (« If X is in play, place threat on it. Otherwise find X and reveal it » : `Worlds.FindCardOnField` + `Find.FindAndReveal`).
- [x] Etape 5 : mots-pieges verifies : ordre imprime respecte (desorienter d'abord) ; « already in play » (3 menaces dessus, personne n'est cherche).
- [x] Etape 6 : nombres texte <-> code : boost 2 icones ; menace 3 (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : Entropic Subversion dans le deck rencontre -> trouvee et revelee (menace 3), joueur desoriente ; deja en jeu -> 3 + 3 = 6 menaces. Substitution : **rouges 2/2**.
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine.

### sz015 : Power Couple (evenement Basic, Team-Up Cannonball / Smasher)

- [x] Etape 2 : carte(s) de reference : hc020 Green Hell (Team-Up : le chargeur EXIGE `.SetTarget("TeamUp")`) ; 29025 « Go for Champions! » (`RegisterTemp(UnitCannotTakeDamageWhile(Temp0, ..), unregister_after_exec=False, until_round_end=True)`).
- [x] Etape 5 : mots-pieges verifies : « Max 1 per deck » (`desc.MaxPerDeck`) ; Team-Up par `desc.TeamUp = "Cannonball;Smasher"` ; « They cannot take damage » : SEULEMENT les deux cibles du Team-Up (`m.trigger in cibles`) ; le nom « Power Couple » existe deja (jj022) : distinguees par card_id.
- [x] Etape 6 : nombres texte <-> code : cout 2, [energy], AERIAL (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : Smasher et Cannonball inclines se redressent ; Smasher puis Cannonball ne prennent aucun degat apres la carte (`declencher_apres`) ; CONTRE-CAS Black Cat prend son degat ; TEMOIN sans la carte (3 degats) ; CONTRE-CAS sans Cannonball en jeu : carte non jouable. Substitution : **rouges 3/6** (verts : contre-cas et temoin).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (statuts et immunite : affichage standard).
Carte terminee : NON (provisoire) : partie reelle humaine ; Q7 : le Team-Up est rempli par TOUT personnage ami nomme « Smasher » ou « Cannonball », y compris l'allie officiel Smasher (gs108) ou un Cannonball officiel (comportement du chargeur, par nom). Acceptable ?.

### sz016 : Energy (ressource Basic, reskin d'art)

- [x] Etape 2 : carte(s) de reference : rl018 (meme gabarit de ressource Basic, reskin d'art, decision Hellcat).
- [x] Etape 5 : mots-pieges verifies : « Max 1 per deck ».
- [x] Etape 6 : nombres texte <-> code : RES YY (scan).
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : aucun script, aucun cas.
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q8 : cartes a part (code, precedent Hellcat) ou arts alternatifs des ressources officielles ?.
- [x] **26/10/2026, arbitrage reskins** (RR « A copy of a card is defined by title » + GUIDE §12 bis) : ces trois ressources ne changent que l'image de `01088` / `01089` / `01090` : ART ALTERNATIF des ressources doubles. Traitement, comme Gwenpool / Beast / Binary : collection `smasher` dans `COLLECTIONS` (`ui-app/src/board/variantes.ts`) ET dans `COLLECTIONS_RESSOURCES` (`public/js/prepare/app.js`, proposée par défaut au héros « Smasher » : `collectionDuHeros`). Les cartes restent dans `cards.json` (précédent TMNT / Gwenpool).
      « Max 1 per deck » par TITRE : `validerDeck` (`public/js/deckbuilder/regles.js`, `cleCopie` = titre|sous-titre) compte déjà `01088` + le reskin comme un même titre ; **aucun correctif nécessaire**, preuve : `tools/tests-lanceur/regles-ressources-doubles-par-titre.test.mjs` (4 verts : chaque reskin du dépôt + son officielle = « Trop d’exemplaires de « Energy » : 2/1 », deux mêmes reskins idem, un seul légal, trois titres différents sans gêne). Le moteur n'applique pas MaxPerDeck (seul le constructeur le juge).
      Collection : `ui-app/src/board/resources-art-packs-fanmade-2026-10.test.ts` (45 verts : ordre Energy/Genius/Strength, wizard aligné, images présentes ; ROUGE vu avant le câblage : 18 échecs sur 27, puis rouge à nouveau en retirant l'entrée du wizard).
      Carte terminée : NON (provisoire) : partie réelle humaine (voir la collection « Smasher » dans la modale du héros et les trois ressources à l'écran).

### sz017 : Genius (ressource Basic, reskin d'art)

- [x] Etape 2 : carte(s) de reference : rl019.
- [x] Etape 5 : mots-pieges verifies : « Max 1 per deck ».
- [x] Etape 6 : nombres texte <-> code : RES BB (scan).
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : aucun script, aucun cas.
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine.

### sz018 : Strength (ressource Basic, reskin d'art)

- [x] Etape 2 : carte(s) de reference : rl020.
- [x] Etape 5 : mots-pieges verifies : « Max 1 per deck ».
- [x] Etape 6 : nombres texte <-> code : RES RR (scan).
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : aucun script, aucun cas.
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `spider_man`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine.

---

## A verifier en partie reelle (aucun outil du projet ne le voit)

- une partie complete avec Smasher choisie dans la liste Fan-made (alter ego au depart, bascule en heros) ;
- le choix de la cible des Hero Responses jouees de la main (Penta-Vision, Hyper-Strength, Exo-Flight) et la fenetre d'Accessing (amelioration puis cible) ;
- le Team-Up Power Couple depuis le deckbuilder (Basic, Max 1 par deck) avec un vrai Cannonball en jeu ;
- les 19 images a l'ecran (Entropic Subversion est en paysage) ;
- la biographie au survol du heros dans l'assistant (le module `heros-info.js` est syntaxiquement valide, non vu dans un navigateur) ;
- les icones de ressource, lues a l'oeil et comparees a des cartes officielles de meme glyphe (01020 G, 01022 B, 01023 R, 01025 Y), pas decoupees pixel par pixel.

## Autoplay du 26/10/2026 (corrections de verdicts : sz001b, sz004, sz005)

`tools/autoplay.py .game-src-sz --deck smasher --vilains klaw --profils equilibre --parties 8` : 8 parties, 0 victoire / 8 défaites (4,2 rounds : 5 « tous les joueurs éliminés »,
3 « manigance accomplie »), 0 bloquée, **0 traceback** sur les 8 journaux. Témoin `she_hulk` (même vilain, mêmes graines) : 8 parties, 0 victoire, 1 bloquée. Le pilote ne
joue pas Battle Ready ni Accessing dans ces parties (aucune ligne « Battle Ready ») : ces deux capacités ne sont prouvées que par leurs cas. Deck `smasher` seul : OK
« identité sz001b, main 6, deck 9 ». Modification moteur de ce passage (additive) : `PlayerStat.this_turn_limited_abilities` (+ `RecordLimitedAbility`,
`HasUsedLimitedAbilityThisTurn`, vidé à chaque tour) et la commande de banc `Puzzle.NewPlayerTurnStat`.

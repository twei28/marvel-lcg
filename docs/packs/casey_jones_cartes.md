# Casey Jones v3 (TMNT, Inkwire, prefixe `tc`) : gabarits PROCESSUS-CARTE

Preuves du 16/10/2026, worktree `tmnt-casey`. Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_casey.py`
(prefixe `[casey]`, 101 cas, 101/101 verts en batterie complete `test_capacites.py .game-src <port> rapport "[casey] "`). Substitution : `tools/substituer_pack.py .game-src 45000 tc`
(17/17 modules avec au moins un cas ROUGE sans leur module ; tc015 n'a pas de module (bases automatiques `desc`), empreinte md5 du pack identique avant/apres, aucun stub reste). Autoplay : `tools/autoplay.py --deck casey_jones` (8 parties (rhino + klaw, normal, equilibre, graines 1-4) : 0 incident, 0 traceback sur les 8 journaux (grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback) ; temoin raphael, memes 8 parties ; 0 % de victoire des deux (player_deck vide par regle, 16 cartes seulement), rounds moyens casey 3,2 (klaw) / 7,0 (rhino) contre raphael 4,0 / 6,5 ; les journaux montrent Overswing (« Pay_cost_Discard » x9), « Clap_Back:_confuse_an_enemy », Driving Iron (« Deal_1_damage_to_an_enemy » x11), Hero Interrupt x19).
Gates : `verifier_tous_les_decks` (DECK_NOM=casey_jones : « identite tc001a, main 6, deck 9 »), `verifier_appels_modules`
(OK), `verifier_noms_modules` (OK), `verifier_desc_mots_cles casey_jones` (« les 18 cartes ont un desc conforme a leur
texte »), `verifier_cibles` (OK), `test_cards` (6432 ok / 0 erreur, relance apres les derniers scripts). Chaque gate a ete VUE ECHOUER une fois (calibrage) :
`verifier_appels_modules` sur un `this.PlaceThreatOn` ajoute a tc008 (« n'existe pas »), `verifier_tous_les_decks` sur un
card_id `tc999` dans le deck (« AssertionError »), `casey_desc` sur un Requirement faux, la limite d'Overswing en retirant
`LimitOncePerPhase()` (11 degats au lieu de 8, tc010 defaussee), les gates plateau en CASSANT le rendu (voir 8 bis).

Decisions utilisateur appliquees (`.planning/tmnt/decisions-phase-b.md`) : fidelite 100 % (rien d'approche) ; `player_deck`
VIDE ; inserts de regles : il n'y en a pas dans ce zip. Questions en attente : `.planning/tmnt/casey-questions.md` (Q1 « Casey
Jones WEAPON », Q2 Setup du Sac en main de depart, Q3 Reponse du Willow sans cible).

Icones de ressource verifiees PAR DECOUPE contre les cartes officielles du jeu de base (`.planning/tmnt/pics-casey-icones/icons.png`) :
01088 Energy (jaune, eclair = energie, Y), 01089 Genius (bleu, noeuds = mental, B), 01090 Strength (rouge, poing = physique, R).
Cartes du pack : tc002 B, tc003 Y, tc004 R, tc005 R, tc006 R, tc007 Y, tc008 B, tc009 Y, tc010 B, tc011 Y, tc012 R, tc013 B :
TOUTES conformes a `cards.json`. L'etoile de « Requirement (*) » (tc005) et de « generate *** » (tc001a) est la glyphe wild
(`04010`, `04033`, `wild.png`). Le glyphe central de tc015 est la Crise (`01108`, `crisis.png`).

Homonyme : « Casey Jones » est aussi l'allie de Raphael (`tr002`, classe Hero, unique, meme nom). Aucun module du pack ne cherche
par le nom : card_id, type (Hero/AlterEgo/identite) ou ensemble « Casey Jones ». `deck/starter/casey_jones.json` porte une
`collision_note` ; le moteur interdit d'avoir les deux en jeu (regle d'unicite).

Etape 8 bis (plateau) : `ui-app/src/board/tmnt-casey-plateau.test.ts`, 28 cas verts (`cd ui-app && npx vitest run
src/board/tmnt-casey-plateau.test.ts`). Aucun correctif plateau n'a ete necessaire (le rendu savait deja dessiner une carte
glissee sous une amelioration, td012) : il n'y a donc pas de « rouge avant correctif » a montrer. Sensibilite prouvee en CASSANT
temporairement puis restaurant 4 lignes de rendu : (B) `attachees` de `zones.ts` -> 21 cas rouges ; (C) `exhausted` de
`card-model.ts` -> 3 rouges ; (D) zone `retirees` de `zones.ts` -> 1 rouge ; (E)/(F) roles `porteur` / `cible` de `interaction.ts`
-> 1 rouge chacun. Un orphelin (`bind_object_id` inexistant) est dessine a la racine : `toBeDefined()` seul ne suffit PAS, les cas
affirment aussi `portePar`, `peeking` et `zone`. Pas de panorama des paires jumelles (aucune paire a illustration continue reperee
dans ce zip).

Moteur partage touche : AUCUN. Fichiers partages ajoutes (lignes de Casey seulement) : `data/cards.json` (+ checksum),
`data/sets_info.json` (« 184. Custom (Casey Jones) »), `tools/prefixes_fanmade.json`, `public/js/prepare/heros-info.js`,
`ui-app/src/board/textes-fr-fanmade.ts` + copie `public/js/traduction/textes-fr-fanmade.js` regeneree.

### tc001a : Casey Jones (face heros, Overswing)
- [x] Étape 2 : `34001a` Phoenix (« Psionic Bond », Resource a cout + `LimitOncePerPhase`), `32031a` Shadowcat (`for_card` a traits ATTACK/DEFENSE), `50177` (`CostFunc.Discard("YouControlCards", ...)`), `32180` Brawler (`ex_operation`).
- [x] Étape 5 : « you control » (`YouControlCards`), « WEAPON upgrade » (type Upgrade + trait), « with the restricted keyword » (`face.restricted > 0`), « [wild][wild][wild] » (`Resources("GGG")`), « ATTACK, THWART, or DEFENSE event » (type Event ET trait, `traits=` est un OU), « Limit once per phase ». Résultat : OK.
- [x] Étape 6 : PV 10, ATQ 2, CTR 2, DEF 2, main 5, 3 icones wild : cas `etape 6` (table relue sur le scan). Résultat : OK.
- [x] Étape 7 : substitution `rouges 5/9` (4 verts = contre-cas d'absence (arme sans Restricted, non-arme Restricted, amelioration, evenement hors traits : la carte reste en main, comme sans module)) ; cas : arme Casey, arme d'un autre heros (Sai), arme sans Restricted (refus), Restricted non-arme (refus), amelioration et evenement hors traits (refus), Face-Off cout 2 (paye), contre-cas limite.
- [x] Étape 7 bis : limite OUI ; temoin d'epuisement : deux armes Restricted en jeu, Grand Slam puis Face-Off dans la meme phase, 2e Overswing refuse -> Face-Off reste en main, tc010 intacte, **8 degats et non 11** ; verifie en RETIRANT `LimitOncePerPhase()` : le cas tombe (11 degats, tc010 defaussee, Face-Off jouee). Resultat : OK.
- [x] Étape 8 : autoplay 8 parties, temoin raphael, grep tracebacks : 0 sur 8 journaux, 0 incident ; journal : Cross Block paye `B G G G` (Overswing + 1 mental), « Pay_cost_Discard » apparait au journal de round.
- [x] Étape 8 bis : OUI (arme defaussee : changement de zone). Cas « tc001a Overswing » du plateau (attachee a l'identite avant, `piles-joueur` apres), vu ROUGE en cassant `attachees` (B).
Carte terminée : OUI

### tc001b : Casey Jones (face alter-ego)
- [x] Étape 2 : `michelangelo/tm001b` et `aa001b` (Setup + fouille deck/defausse), `01019a`/`bt001b` (`AfterUnitChangeForm(..., to_this_form=True)`), `hd013` (`Faces.ReturnToHand`).
- [x] Étape 5 : « deck AND discard pile » (pas la main : **Q2**), « the Casey's Bag » (card_id tc013), « return A WEAPON » (n'importe quelle arme), « to THIS form ». Résultat : OK, une lecture marquee `TODO-QUESTION` (Q2).
- [x] Étape 6 : REC 4, PV 10, main 6. Résultat : OK.
- [x] Étape 7 : substitution `rouges 6/9` (3 verts = contre-cas d'absence (non-arme, forme HEROS, defausse sans arme)) ; cas : vraie mise en place (Sac en jeu, attache, deck 9), Sac dans la defausse / le deck / la main (reste en main : Q2), Response : une arme revient (choix libre : Bat ou Sai), non-arme (Shell) reste, vers la forme HEROS rien ne revient, defausse sans arme sans plantage.
- [x] Étape 7 bis : NON. Étape 8 : OK (voir le pack).
- [x] Étape 8 bis : OUI (Sac attache a l'identite en civil, absent de la pile du deck). Cas « tc001b Setup », vu rouge en cassant `attachees` (B).
Carte terminée : OUI (avec la question Q2 en attente : la lecture litterale est implementee)

### tc002 : Clap Back (x2)
- [x] Étape 2 : `raphael/tr003` Disarm (`SetPlay().SetLabel('thwart').SetTarget(Scheme2)`), `ma015` (second choix `ForChoiceAbility.SetTarget(Enemy, canbe_confused=True)`), `tc001a` Overswing (marque l'effet de la carte payee).
- [x] Étape 5 : « a scheme », « CASEY JONES WEAPON » (**Q1**), « discarded TO PAY FOR THIS CARD », « confuse AN enemy » (choix). Résultat : OK.
- [x] Étape 6 : cout 3, 5 menaces, [mental]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 5/5` (5/5, aucun vert) ; cas : sans arme (menace 6 -> 1, pas de confusion), arme de Casey par Overswing (confus), arme d'un autre heros (pas confus), arme defaussee AVANT (pas confus), sous Crise (annexe seulement).
- [x] Étape 7 bis : NON. Étape 8 : OK (« Clap_Back:_confuse_an_enemy » au journal).
- [x] Étape 8 bis : OUI (carte d'etat Desoriente sur l'ennemi) : cas plateau « tc002 Clap Back ».
Carte terminée : OUI

### tc003 : Cross Block (x2)
- [x] Étape 2 : `14014` Never Back Down (`WhenUnitDefendAgainstAttack(HeroInterrupt, "You", op, is_basic_defense=True).SetPlay().SetLabel('defense')`).
- [x] Étape 5 : « +3 DEF FOR THAT ATTACK », « THEN ready Casey Jones AND give him a tough status card » (deux effets dans l'ordre, sur l'identite), « When YOU defend » (pas un allie). Résultat : OK.
- [x] Étape 6 : cout 2, +3, [energy]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 2/4` (2 verts = temoin sans la carte et allie defenseur (absence)) ; cas : +3 DEF (1 degat -> 0), Casey redresse et Tough, temoin sans la carte (1 degat, incline, sans Tough), paye par Overswing, allie defenseur : non jouee.
- [x] Étape 7 bis : NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI (carte d'etat Tenace sur l'identite) : cas plateau « Cross Block ».
Carte terminée : OUI

### tc004 : Face-Off (x2)
- [x] Étape 2 : `10015` Toe to Toe (`cible.DoAttackYou(joueur, effect)`), `raphael/tr004` (degats par le heros).
- [x] Étape 5 : ordre imprime (ready, 3 degats, attaque ; Toe to Toe fait l'inverse), « THAT enemy attacks YOU ». Résultat : OK.
- [x] Étape 6 : cout 2, 3 degats, [physical]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 3/4` (1 vert = temoin sans la carte (absence)) ; cas : Casey incline -> redresse, 3 degats, Rhino attaque et Casey defend (0 degat) ; temoin sans la carte (2 degats) ; ennemi vaincu : pas d'attaque et Casey reste PRET ; paye par Overswing.
- [x] Étape 7 bis : NON. Étape 8 : OK. Étape 8 bis : NON (degats, inclinaison).
Carte terminée : OUI

### tc005 : Grand Slam (x2)
- [x] Étape 2 : `raphael/tr004` (montage), `dt084` Off the Cuff (`"Requirement": "G"`).
- [x] Étape 5 : « Requirement ([wild]) » (au moins une wild dans le paiement : mots-cles/requirement.md), « Deal 8 damage ». Résultat : OK.
- [x] Étape 6 : cout 3, Requirement wild, 8 degats, [physical]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 2/3` (1 vert = Requirement non satisfait : base automatique `desc.Requirement`, refus du moteur sans module (assume) ; mesure 2/4 avant le renommage d'un cas `etape 6`) ; cas : vraie carte wild (16019) + Strength, refus sans wild (RR + YY), 8 degats sur le MINION choisi ; + cas Overswing (tc001a) qui paie Grand Slam.
- [x] Étape 7 bis : NON. Étape 8 : OK. Étape 8 bis : NON.
Carte terminée : OUI

### tc006 : Anything Goes
- [x] Étape 2 : `td012` / `60030` (`TuckCardUnderHere`, `GetPlacedCardArea`), `tr003` (choix secondaire), `ho010` (amelioration a Hero Action).
- [x] Étape 5 : « SWAP » (echange : l'arme en jeu est RANGEE sous le Sac, pas defaussee), « Casey Jones WEAPON ... you control / tucked » (**Q1**), « Exhaust » est un cout, Restricted : on range avant d'entrer. Résultat : OK.
- [x] Étape 6 : cout 1, [physical]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 4/7` (3 verts = les trois refus « l'Action n'est pas offerte » (absence)) ; cas : echange nominal (attachee a Casey, batte rangee, Anything Goes inclinee), limite Restricted respectee (2 Restricted en jeu), choix parmi deux armes rangees ; refus : rien range, aucune arme de Casey en jeu (Sai), arme rangee non-Casey ; temoin positif (1 action offerte).
- [x] Étape 7 bis : NON. Étape 8 : OK (« Hero_Action » au journal).
- [x] Étape 8 bis : OUI (l'arme sortante est dessinee SOUS le Sac, l'entrante attachee) : cas plateau « tc006 Anything Goes » + choix cliquable.
Carte terminée : OUI

### tc007 : Baseball Bat
- [x] Étape 2 : `tg009` Frogjolnir et `20010` Venom's Pistol (meme texte : `WhenUnitUseBasicPower(HeroInterrupt, ...)` + `message.GainValue(+1, effect)`).
- [x] Étape 5 : « When YOU use » (identite seulement), « +1 to THAT power FOR THIS USE », « exhaust » = cout, Restricted (base `desc`). Résultat : OK.
- [x] Étape 6 : cout 1, +1, Restricted 1, [energy]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 3/4` (1 vert = l'attaque d'un allie (absence)) ; cas : attaque (+1), contre (+1), defense (+1), allie : pas de bonus.
- [x] Étape 7 bis : NON. Étape 8 : OK. Étape 8 bis : NON (inclinaison couverte par `exhausted`, sensibilite C).
Carte terminée : OUI

### tc008 : Casey's Mask
- [x] Étape 2 : `ho010`, `Faces.ReadyAll` (an001a, 31009).
- [x] Étape 5 : « ready CASEY JONES » = l'identite (jamais le nom : homonyme tr002), Hero Action, unique. Résultat : OK.
- [x] Étape 6 : cout 3, [mental]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 1/3` (2 verts = Hero Action absente en civil (absence) et unicite (regle moteur, `desc`)) ; cas : redresse l'identite, absente en alter-ego, 2e Mask refusee (unique).
- [x] Étape 7 bis : NON. Étape 8 : OK. Étape 8 bis : NON.
Carte terminée : OUI

### tc009 : Cricket Willow
- [x] Étape 2 : `04159a` (+N a un pouvoir par `GiveKeywordToAttached(Hero, ...)`), `iw001a`/`ho001a` (`AfterUnitAttackEnd(..., against_who=Enemy)`), `22014` (`CostFunc.Discard("This")`).
- [x] Étape 5 : « YOUR HERO gets +1 ATK », « After you attack AN enemy », « THAT enemy » (cibles de cette attaque), cout de defausse devant la fleche. Résultat : OK, une lecture marquee `TODO-QUESTION` (Q3 : Reponse non offerte sans cible).
- [x] Étape 6 : cout 2, +1 ATQ, Restricted 1, [energy]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 4/5` (1 vert = retour en civil sans erreur (absence)) ; cas : +1 ATQ en heros, suit la forme (pose en civil puis heros), retour en civil sans erreur, attaque -> 3 degats + Sonne + Willow defausse, ennemi vaincu : Reponse non offerte, Willow en jeu.
- [x] Étape 7 bis : NON. Étape 8 : OK. Étape 8 bis : OUI (Willow defausse, carte d'etat Sonne) : cas plateau.
Carte terminée : OUI

### tc010 : Driving Iron
- [x] Étape 2 : `ho010`, `raphael/tr010` Gekido (choix `ChooseAbilities`), `tr003` (`RemoveThreatFromSchemes`).
- [x] Étape 5 : « deal 1 damage to AN enemy OR remove 1 threat from A scheme » (un choix, deux nombres a 1), Action (pas un contre : la Crise ne verrouille pas le ciblage), Hero Action. Résultat : OK.
- [x] Étape 6 : cout 1, 1 / 1, Restricted 1, [mental]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 2/3` (1 vert = Hero Action absente en civil (absence)) ; cas : branche degats, branche menace, absente en alter-ego.
- [x] Étape 7 bis : NON. Étape 8 : OK (« Deal_1_damage_to_an_enemy » au journal). Étape 8 bis : NON.
Carte terminée : OUI

### tc011 : Hockey Stick
- [x] Étape 2 : `tg009` / tc007 (meme montage + `powers=["ATK", "DEF"]`).
- [x] Étape 5 : « basic attack OR DEFENSE » (le contre n'est pas cite), « +2 ». Résultat : OK.
- [x] Étape 6 : cout 2, +2, Restricted 1, [energy]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 2/3` (1 vert = le contre ne declenche rien (absence)) ; cas : attaque (+2), defense (+2), CONTRE-CAS : le contre ne declenche rien (baton reste pret).
- [x] Étape 7 bis : NON. Étape 8 : OK. Étape 8 bis : NON.
Carte terminée : OUI

### tc012 : Persuader
- [x] Étape 2 : `ar004` / `ho016` (`GainPiercing`), `tc009` (+1 ATQ continu).
- [x] Étape 5 : « basic ATTACK » seulement (`is_basic_attack=True` sur `WhenUnitWouldAttack`), « +1 ATK for THAT attack » en plus du +1 continu, « THIS attack gains piercing ». Résultat : OK.
- [x] Étape 6 : cout 2, +1 / +1, Restricted 1, [physical]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 4/8` (4 verts = temoin sans piercing, defense, contre, retour en civil (absence)) ; cas : ATQ 4 (2+1+1), piercing sur Rhino Tough (4 degats et plus de Tough) contre le temoin sans piercing (0 degat), defense et contre : rien, bonus continu suit la forme, retour en civil sans erreur.
- [x] Étape 7 bis : NON. Étape 8 : OK. Étape 8 bis : NON.
Carte terminée : OUI

### tc013 : Casey's Bag
- [x] Étape 2 : `td012` (tuck, jouer comme en main), `hd013` (la plus basse de la defausse), `ho010`.
- [x] Étape 5 : « play cards tucked here » (play seulement, tout type, sans plafond), « the BOTTOMMOST WEAPON upgrade » (la plus basse des armes, une non-arme au fond est sautee), « Exhaust » = cout (action non offerte sans arme), Permanent (desc). Résultat : OK.
- [x] Étape 6 : AUCUN cout imprime, Permanent 1, [mental]. Résultat : OK.
- [x] Étape 7 : substitution `rouges 5/9` (4 verts = temoin « autre carte », action non offerte x2 (absence) et Permanent (base automatique `desc`, assume) ; mesure 5/10 avant le renommage d'un cas `etape 6`) ; cas : jouer une amelioration rangee (VRAI chemin : le moteur l'offre), un evenement rangé, temoin sous une autre carte (non offerte), Action (range la plus basse, saute la non-arme, n'importe quelle arme), refus sans arme / en civil, Permanent.
- [x] Étape 7 bis : NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI (cartes glissees dessinees, plusieurs, face cachee, jouables). Cas plateau « tc013 Sac » (9 cas), sensibilite B, E, F.
Carte terminée : OUI

### tc014 : Daddy Issues (obligation)
- [x] Étape 2 : `raphael/tr013` (squelette), `donatello/td013` (`PlayerActionToRemoveThisFromGame`, `ChangeToOtherIdentityForm`).
- [x] Étape 5 : « Flip to alter-ego » obligatoire, « cannot change forms » (les deux sens), « Action » (pas Hero), « Exhaust Casey Jones » = l'identite (cout), « remove ... from the game ». Module dans `casey_jones/` (bandeau CASEY JONES). Résultat : OK.
- [x] Étape 6 : 2 icones de boost, GiveTo « Casey Jones ». Résultat : OK.
- [x] Étape 7 : substitution `rouges 4/6` (2 verts = recue en civil (rien a retourner) et identite inclinee (absence)) ; cas : recue en heros (retourne en civil, non incline), en civil, bon joueur (2 joueurs), changement de forme refuse, Action (incline et retire du jeu), identite inclinee : Action non offerte.
- [x] Étape 7 bis : NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI (obligation dessinee, retiree du jeu -> `annexes`) : cas plateau « tc014 », sensibilite D.
Carte terminée : OUI

### tc015 : The Purple Dragons (manigance annexe nemesis)
- [x] Étape 2 : `04056` / `sk073` (Incite), `01108` Crowd Control (Crisis), `tm014` Sewer Problems. Aucun module (bases automatiques `desc`).
- [x] Étape 5 : « Incite 1 [per_hero] » (`1*`), menace de depart 3 (sans glyphe joueur), Crise 1 (glyphe central = 01108, decoupe), boost 2. Résultat : OK.
- [x] Étape 6 : menace 3, boost 2, Incite 1*, Crise 1 : cas `etape 6` + cas Incite (1 joueur +1, 2 joueurs +2), menace 3 meme a 2 joueurs, Crise. Résultat : OK.
- [x] Étape 7 : cas sujets tc015 (4), vert sans module (bases `desc`, assume : pas de substitution possible, voir tc016/tc017 pour les modules).
- [x] Étape 7 bis : NON. Étape 8 : OK. Étape 8 bis : NON (la pastille de Crise est couverte par la gate des manigances a Crise).
Carte terminée : OUI

### tc016 : Hun (sbire nemesis)
- [x] Étape 2 : `21156` Laufey (TEXTE IDENTIQUE : Ténacité + `AfterUnitAttackAndDamageUnit(ForcedResponse, "This", None, op, target_in_play=True)`).
- [x] Étape 5 : « attacks AND DAMAGES », « a CHARACTER » (allie compris), « stun THAT character », sans [star]. Résultat : OK.
- [x] Étape 6 : PV 4, ATQ 2, CTR 1, boost 3, Tenacite 1, Nemesis « Casey Jones ». Résultat : OK.
- [x] Étape 7 : substitution `rouges 2/5` (3 verts = Tenacite (base `desc`, assume) et deux contre-cas « attacks AND DAMAGES » (absence)) ; cas : Tenacite (Tough a l'entree), 2 degats + Sonne (Casey incline), defense a 0 degat : pas de statut, Tough absorbe : pas de statut, allie blesse : Sonne.
- [x] Étape 7 bis : NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI (carte d'etat Sonne sur un personnage ami) : cas plateau « Hun ».
Carte terminée : OUI

### tc017 : Purple Dragon Goons (x3)
- [x] Étape 2 : `tl016` / `td015` (`WhenThisRevealed`), `Worlds.FindVillain`.
- [x] Étape 5 : « the VILLAIN » (pas un sbire), vilain deja Tough : pas de 2e, Guard / Patrol (bases `desc`). Résultat : OK.
- [x] Étape 6 : PV 3, ATQ 2, CTR 1, boost 2, Guard 1, Patrol 1, trois exemplaires pour un card_id. Résultat : OK.
- [x] Étape 7 : substitution `rouges 1/6` (5 verts = plafond Tough (absence), Guard et Patrol avec leurs temoins (bases automatiques `desc`, assume) ; mesure 1/7 avant le renommage d'un cas `etape 6`) ; cas : Tough sur le vilain, pas de 2nd Tough, Guard (seul le sbire attaquable) + temoin, Patrol (menace inchangee) + temoin.
- [x] Étape 7 bis : NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI (Tenace sur le vilain) : cas plateau « Goons ».
Carte terminée : OUI


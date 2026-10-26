# Pack Wasp (Hank Pym) (JackHKP, prefixe `hp`) : gabarits PROCESSUS-CARTE (26/10/2026)

Set 222. 20 identifiants : hp001a/b/c (identite a TROIS formes), hp002-hp012 (11 cartes signature, 15 exemplaires), hp013 (obligation),
hp014-hp018 (set nemesis, hp016 MIS DE COTE au setup). Cas : `Fusion/marvel-lcg-src/tools/cas/wasp_hank_pym.py` (filtre `[hp]`).
Plateau : `ui-app/src/board/wasp-hank-pym-plateau.test.ts` (etape 8 bis).

**Etat : aucune carte n'est terminee.** Toutes restent `NON (provisoire)` pour UNE seule raison : aucune partie reelle n'a ete jouee par un humain.
**Plus aucune question de regle n'est en attente** : le 26/10/2026, Q1 a Q5 ont recu la reponse A de l'utilisateur et Q6 a Q18 ont ete tranchees par le
Rules Reference v1.8 et les scans (`VERDICTS-REGLES-2026-10-26.md`, dans ce dossier), puis les corrections ont ete appliquees (hp007, hp009, hp012,
hp013, hp017 ; hp015 / hp016 verifies ; voir « Corrections du 26/10/2026 » plus bas). Synthese transversale : `docs/rapports/2026-10-26-arbitrages-heros-fanmade.md`.

> Toutes les icones de ressource ont ete lues contre les glyphes d'autres packs (She-Hulk, Ant-Man) a l'ecran, **sans decoupe pixel par pixel** :
> a reverifier si un doute apparait en partie (Jocasta, Resize at Will : mental ; Mansion, Gigantification, Huge Surprise : physique ; Wings, Size Manipulation, Stinger : energie ; Ant-Man, Pym Particles : wild).

### hp001a : * Wasp (forme minuscule)

- [x] Etape 2 : carte(s) de reference : 13001a (Wasp officielle : Response sur forme) ; 12001a (`AfterUnitChangeForm(..., to_this_form=True)`) ; 90117 (`ForChoiceAbilityWithCost`)
- [x] Etape 5 : texte-contre-code, mots-pieges : « confuse a minion » / « instead » : branches EXCLUSIVES dans un `ChooseAbilities` ; « you MAY spend » : branche payante offerte seulement si couvrable (`PeutCouvrirLeCout`)
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : PV 12, THW 2, ATK 1, DEF 2, main 5 ; cout BB
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp001a Bumble Bee (sbire / vilain paye) + valeurs imprimees
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp001b : * Hank Pym (alter ego)

- [x] Etape 2 : carte(s) de reference : 13001b (`WhenInYourPlayTurn(Action)`) ; 27040 (`Search.PlayerCard` + `PutIntoPlay`) ; bt001b (`BeginGameWithSetAside`)
- [x] Etape 5 : texte-contre-code, mots-pieges : « Spend 1 [mental] » = `SetCost(Cost("B"))` ; « If you cannot » : repli sur la recherche ; « You can only change form by card abilities » : CORRECTIF player_setup.py
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : PV 12, REC 3, main 6
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp001b Scientist Supreme (2 branches) + valeurs + temoin « pas de changement libre »
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp001c : * Wasp (forme geante)

- [x] Etape 2 : carte(s) de reference : 13001c, 12001c (Response sur forme), 90117
- [x] Etape 5 : texte-contre-code, mots-pieges : idem hp001a : « stun » (Stunned) et cout RR
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : PV 12, THW 1, ATK 3, DEF 3, main 4 ; cout RR
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp001c Man-Mountain (sbire / vilain paye) + valeurs imprimees
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp002 : * Ant-Man (Eric O'Grady)

- [x] Etape 2 : carte(s) de reference : 13012 (`ThisGainKeyword` + `OnEvent.Counter`, compteurs pym) ; 12007 (Action avec cout) ; 12005
- [x] Etape 5 : texte-contre-code, mots-pieges : « for each pym counter on HIM (max +3) » ; « Exhaust a Size Manipulation -> move 1 » (le cout incline, le compteur est deplace par l'effet) ; « Discard this card -> change form »
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : cout 3, PV 3, ATK 2*, THW 2*, +1/+1 par compteur, max +3
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp002 : deplacement, temoin sans compteur, plafond +3, defausse -> forme
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp003 : Gigantification

- [x] Etape 2 : carte(s) de reference : 12003 (condition de forme + Hero Action) ; 01003 Backflip (Interrupt defense) ; 61023 (`SetIgnoreKeyword`)
- [x] Etape 5 : texte-contre-code, mots-pieges : « Play only if TINY » ; « ignoring any guard keyword » : `.SetIgnoreKeyword('Guard')` ; deux capacites Play sur un evenement
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : cout 1, 4 degats
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp003 : attaque (Guard ignore), temoin forme geante, interruption de defense (GIANT + Tough)
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp004 : Resize at Will (x3)

- [x] Etape 2 : carte(s) de reference : 12005 Resize (changement de forme + pioche) ; ls004 / bw024 (`BasicAttack` sans incliner)
- [x] Etape 5 : texte-contre-code, mots-pieges : « Change form » a TROIS faces : le joueur choisit (`changer_de_forme`, traits) ; « without exhausting » : `BasicAttack`/`BasicThwart` sans rien incliner
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : cout 2, pioche 2
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp004 : alter ego -> geant -> attaque de base
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp005 : Self-Shrinking

- [x] Etape 2 : carte(s) de reference : 12003 ; 01003 Backflip ; bt015 (`CancelThisAttack`) ; 61023 (`SetIgnoreKeyword('Patrol')`)
- [x] Etape 5 : texte-contre-code, mots-pieges : « Play only if GIANT » ; « initiates an attack against YOU » : `against_player="You"` ; « ignoring any patrol keyword » sur l'effet de la carte elle-meme
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : cout 1, 3 menaces
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp005 : menee (GIANT -> TINY, -3), temoin forme minuscule, defense (annule l'attaque)
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp006 : Pym Particles (x2)

- [x] Etape 2 : carte(s) de reference : 12006 (`AfterYouSpendThisCard`) ; mf007 (compteurs)
- [x] Etape 5 : texte-contre-code, mots-pieges : « a TOTAL of 2 pym counters on THEM » : un compteur a la fois, au choix si plusieurs Size Manipulation ; « If none were placed » : compte le retour de `PlaceCountersOn`
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : 2 compteurs au total
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp006 : redresse + 2 compteurs
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp007 : * Infinite Avengers Mansion

- [x] Etape 2 : carte(s) de reference : 12007 (support Action) ; 27040 ; hc014
- [x] Etape 5 : texte-contre-code, mots-pieges : « AlterEgo Action » ; « identity-specific » = classe Hero du set de l'identite (RR IDENTITY-SPECIFIC CARD) ; **« a card you control » : TOUTE carte en jeu qu'on controle, l'IDENTITE et le Mansion lui-meme compris** (RR OWNERSHIP AND CONTROL : « Identity cards are owned and controlled by the player playing as that identity »)
      **CORRECTIF 26/10/2026** : le script excluait l'identite et le Mansion, sans appui dans le texte (verdict Q8). Filtre retire.
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : cout 2, 1 compteur
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp007 : compteur + remelange d'une carte de la defausse ; **3 cas** : le compteur pym est pose quand le Mansion et l'identite sont les SEULES cartes en jeu ; le joueur designe l'IDENTITE (`compteurs_identite`)
      Resultat : **VUS ROUGES avec l'ancien filtre** (« total des compteurs pym en jeu = 0 », « identite.pym=0 »), verts avec le correctif ; sans module : rouges 3/3 (`tools/cas/wasp_hank_pym.py`, 26/10/2026).
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas (le pilote joue la carte comme ressource, jamais son Action : non exercee en autoplay).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (un compteur pym peut maintenant porter sur l'identite). Cas plateau : `wasp-hank-pym-plateau.test.ts` « hp007 ... compteur pym sur l'identite » : VERT du premier coup, **pas vu rouge** (le rendu generique des compteurs d'identite suffisait : garde-fou de non-regression, pas preuve d'un correctif de plateau).

Carte terminee : NON (provisoire) : partie reelle humaine non faite.

### hp008 : * Jocasta

- [x] Etape 2 : carte(s) de reference : an002 Sera (`GiveKeywordToInPlayWhenApplyThis(Hero, ...)`) ; 12008 (`AfterUnitChangeForm`)
- [x] Etape 5 : texte-contre-code, mots-pieges : « WASP gets +1 THW » : cible `Hero` (le NOM Wasp = formes heros, pas l'alter ego, lecon an002) ; `AlterEgoResponse` + cout incliner
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : cout 3, +1 THW
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp008 : +1 THW (geant), temoin alter ego, redressement apres retour en alter ego
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp009 : * Bio-Synthetic Wings

- [x] Etape 2 : carte(s) de reference : 13010 (`GiveKeywordToAttached` par forme) ; **17029 Agile Flight et 36010 Torrential Rain** (`RemoveThreatFromSchemesTotal` + `SetTarget(Scheme2, range=..., repeat_rules="Threat")`) ; ex-modele Iron Man im003
- [x] Etape 5 : texte-contre-code, mots-pieges : « remove X threat **from among schemes** » = menace REPARTIE entre les manigances, une designation = 1 menace (formule officielle de 17029) ; X = formes changees ce tour (lu a la resolution) ; « While Wasp is in TINY hero form » : trait AERIAL par forme
      **CORRECTIF 26/10/2026** : le script retirait X menaces d'UNE seule manigance (`RemoveThreatFromSchemes`, cible unique) ; verdict Q9. Plage de cibles `(min(1, X), X)` calculee a la resolution (callable) : X = 0 (forme prise un tour precedent) ne bloque rien.
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : cout 1 ; X = nombre de changements de forme CE tour
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : 5 cas : AERIAL en minuscule ; temoin geante (pas d'AERIAL) ; thwart X = formes changees ; **X = 2 avec DEUX manigances a 1 menace -> 1 retiree a chacune** ; **temoin X = 0** (`Puzzle.NewTurnWorldStat`, l'Action se resout sans erreur)
      Resultat : le cas « deux manigances » **VU ROUGE avec l'ancien code** (« menace sur 01109 = 1 (attendu 0) »), vert avec le correctif ; sans module : rouges 4/5 (reste vert : temoin forme GEANTE, absence de trait, a assumer).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas (Action non exercee par le pilote).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (menace retiree : jauge deja couverte)

Carte terminee : NON (provisoire) : partie reelle humaine non faite.

### hp010 : Huge Surprise

- [x] Etape 2 : carte(s) de reference : 50144 (statut sur l'hote, perd Stalwart) ; 27171 (`AttachTo2`) ; temporary.md
- [x] Etape 5 : texte-contre-code, mots-pieges : « Attach this card to an enemy » (le heros l'a posee sur lui d'abord) ; « loses steady and stalwart » : `GiveKeywordToAttached("Character", stalwart=-1, steady=-1)` ; « after it is stunned OR confused » ; « gains temporary »
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : cout 2, 4 degats
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp010 : attache au vilain, etourdi -> 4 degats
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `wasp-hank-pym-plateau.test.ts`

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp011 : Size Manipulation (x2)

- [x] Etape 2 : carte(s) de reference : 13012 (entree en jeu avec compteurs) ; ab007 (`CanGenerateResources`) ; mf007 (`CostFunc.Counter`)
- [x] Etape 5 : texte-contre-code, mots-pieges : « Enters play with 2 pym counters » ; Resource ET Action qui retirent 1 compteur : `CostFunc.Counter("This", 1, 'pym')` verifie qu'il en reste
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : cout 1, 2 compteurs
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp011 : 2 compteurs, Action change de forme, Resource paie
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp012 : * The Stinger

- [x] Etape 2 : carte(s) de reference : 13006 Wasp Sting (un degat par designation, `repeat_rules="Health"`) ; 12013
- [x] Etape 5 : texte-contre-code, mots-pieges : « deal **X** damage divided among enemies you choose » : l'Action oblige a repartir les X degats, pas a en perdre (X = formes changees ce tour, lu a la resolution)
      **CORRECTIF 26/10/2026** : la plage de cibles etait `(1, 6)` puis tronquee a X : le joueur pouvait designer MOINS de X ennemis et perdre des degats (verdict Q11). Plage = exactement X (callable `formes_changees_ce_tour`).
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : cout 1 ; X = nombre de changements de forme CE tour
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : 3 cas : X = 1 -> 1 degat ; **X = 2, le pilote ne designe que le MINIMUM exige -> 2 degats infliges** ; **temoin X = 0**
      Resultat : le cas X = 2 **VU ROUGE avec l'ancien code** (« 1 degat(s) au total ... attendu 2 »), vert avec le correctif ; sans module : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas (Action non exercee par le pilote).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (degats : jauge deja couverte)

Carte terminee : NON (provisoire) : partie reelle humaine non faite.

### hp013 : Identity Crisis (obligation)

- [x] Etape 2 : carte(s) de reference : hc013 (obligation, `GiveTo`) ; 13026 ; **40160 Manufactured Drama** (cout `Exhaust("YourIdentity")` + effet = defausser l'obligation) ; `hp018` / `sk193a` (`Search.EncounterCard` + `Reveal`) ; `45075a` (reaction aux compteurs `pursuit`)
- [x] Etape 5 : texte-contre-code, mots-pieges : « find Shadow of the Past and reveal it » (RR FIND) : **cartes OFFICIELLES du moteur** : `01190` Shadow of the Past (traitrise du set Standard) cherchee dans le deck rencontre ET sa defausse ; « If you cannot, place 7 pursuit counters on Pursued by the Past » : `45075a/b` (environnement permanent du set Standard III), cherche EN JEU ; « **exhaust Hank Pym -> discard** » : TOUT ce qui precede la fleche est le COUT (RR COST ARROW ICON) : le choix degats / menace ET l'inclinaison de Hank Pym ; l'effet = la defausse
      **CORRECTIFS 26/10/2026** : (1) la branche « 5 compteurs ou plus » n'etait pas codee, sur la foi d'une note FAUSSE (« cartes absentes du zip ») ; (2) l'Action etait offerte meme Hank Pym incline, et laissait subir degats / menace avant l'echec de l'inclinaison (verdicts Q12 et Q13). Cout = `Exhaust("YourIdentity")` + `CostFunc.Custom` (choix degats / menace ; degats pris EN ENTIER, RR COST), effet = defausse. Les 7 compteurs sont poses avec `GameRule(identite)` : `45075a` ne reagit qu'a un compteur pose PAR UN JOUEUR (`place_player`), l'effet d'une obligation a le vilain pour initiateur (voir `mots-cles/find.md`).
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : boost 2, seuil 5 compteurs, 7 compteurs pursuit
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : 8 cas : compteur crisis ; sortie par les degats ; **sortie par la menace** ; **temoin Hank deja incline -> Action non offerte** ; **5e compteur + Shadow of the Past -> Ultron en jeu** ; **temoin 4 compteurs -> pas de recherche** ; **5e compteur sans Shadow, Pursued by the Past en jeu -> 7 compteurs, 45075a se retourne et revele Ultron** (carte a deux faces `45075a,45075b`) ; **ni l'une ni l'autre -> rien, aucune erreur**
      Resultat : **VUS ROUGES avec l'ancien code** : temoin incline (« degats sur l'identite = 2 (attendu 0) »), 5e compteur / Shadow (« hp015 n'est pas en jeu »), Pursued by the Past ; verts avec le correctif ; sans module : rouges 7/8 (reste vert : le temoin Hank incline, un contre-cas d'ABSENCE d'effet, a assumer).
- [x] Etape 7 bis : limite imprimee ? NON (le seuil « 5 ou plus » n'est pas une limite)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas : l'obligation est revelee et pose ses compteurs crisis en vraie partie ; ni l'Action ni la branche a 5 compteurs ne sont jouees par le pilote.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (compteurs sur l'obligation / sur Pursued by the Past) : rendu generique des compteurs, deja couvert par `wasp-hank-pym-plateau.test.ts` (pas de correctif de plateau).

Carte terminee : NON (provisoire) : partie reelle humaine non faite.

### hp014 : Return of the Prodigal Son

- [x] Etape 2 : carte(s) de reference : tuck.md ; 13027 (complot annexe)
- [x] Etape 5 : texte-contre-code, mots-pieges : « After the player phase ends » : `AfterPhaseEnd(ForcedResponse, "Player")` ; « highest cost » : `Filter.One(..., highest_cost=True)` ; boost etoile « Reveal this card »
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : menace 2 par heros, 2 compteurs seize
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp014 : compteur, glissement au 2e compteur
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `wasp-hank-pym-plateau.test.ts`

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp015 : * Ultron

- [x] Etape 2 : carte(s) de reference : 13028 (sbire nemesis) ; seek.md (`DiscardEncounterCardsUntil`)
- [x] Etape 5 : texte-contre-code, mots-pieges : « set-aside Seized Control » : `joueur.set_aside_deck` (Hank Pym le met de cote : `BeginGameWithSetAside`) ; Stalwart / Villainous dans desc
      **Justification corrigee le 26/10/2026 (verdict Q15)** : aucune carte n'ordonne de mettre Seized Control « a part » : dans les regles, il est mis de cote AVEC tout le set nemesis (RR NEMESIS ENCOUNTER SET). Ultron est revele AVANT le melange du reste du set (`01190` Shadow of the Past : sbire revele, puis « shuffle the rest »), donc son When Revealed trouve Seized Control encore de cote ; la branche « seek un [[Hacked]] » ne joue que si Ultron est revele une 2e fois. Le `BeginGameWithSetAside(["hp016"])` + `nemesis_set` SANS hp016 (deck JSON) produit le meme effet.
      **Doublon verifie** : cas `hp016 ... une seule copie existe dans la partie au demarrage` (cle `hp_exemplaires` : 1 x hp016 et 1 x hp015 parmi tous les objets de la partie) : VERT.
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : PV 5, ATK 2, SCH 2, boost 1 + etoile
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp015 : revele -> Seized Control s'attache
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp016 : Seized Control

- [x] Etape 2 : carte(s) de reference : 13029 (`AttachToFaceWhenPutIntoPlay(CardFinder(name="Ultron"), if_cannot_attach_to=Villain)`) ; tuck.md
- [x] Etape 5 : texte-contre-code, mots-pieges : « lowest cost » ; « place it here instead » : compteurs `damage` sur la carte ; X = cout imprime de la carte glissee
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : boost 2
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp016 : les degats d'Ultron vont sur la carte ; **une seule copie dans la partie** (cle `hp_exemplaires`, 26/10/2026 : pas de doublon entre le set nemesis et `BeginGameWithSetAside`)
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas. Cout X = cout IMPRIME de la carte glissee (RR TUCK : une carte glissee n'est pas en jeu) : verdict Q16, aucun changement.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `wasp-hank-pym-plateau.test.ts`

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

### hp017 : Take Over Signal

- [x] Etape 2 : carte(s) de reference : 27171 Manipulated Mind (`TreatAttachedCardAsMinion`) ; `st016` (trait HACKED : `GainTraits`) ; skrull sk098
- [x] Etape 5 : texte-contre-code, mots-pieges : « Treat attached ally as a **HACKED** minion » : le sbire garde les traits de l'allie ET porte HACKED ; « seek an ally from your deck » : `DiscardDeckUntil(card_type=Ally)` puis mise en jeu (voir `mots-cles/seek.md`) ; « blank text box » / « no consequential damage » : seulement ce que fait `TreatAttachedCardAsMinion` ; **aucun surge imprime**
      **CORRECTIFS 26/10/2026** : (1) le trait HACKED n'etait pas donne au sbire ; (2) le script ajoutait un « surge » qui n'est PAS imprime (27171 en a un, pas cette carte) : sans allie a prendre, la carte est defaussee (RR ATTACH TO) (verdict Q17).
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : boost 2
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : 4 cas : s'attache a l'allie au cout le plus eleve ; **l'hote porte HACKED** ; **aucun allie nulle part -> pas de surge, carte defaussee** ; **aucun allie en jeu, un allie dans le deck -> il entre en jeu avec la carte, HACKED**
      Resultat : **VUS ROUGES avec l'ancien code** (3 sur 4 : « n'a pas le trait HACKED », « 01103 absent du deck Rencontre » = le surge avait pioche) ; sans module : rouges 3/4 (reste vert : le cas « aucun allie », un contre-cas d'ABSENCE d'effet, a assumer).
- [x] Etape 7 bis : limite imprimee ? NON
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (trait ajoute : le plateau ne l'affiche pas)

Carte terminee : NON (provisoire) : partie reelle humaine non faite.

### hp018 : Submit or Perish

- [x] Etape 2 : carte(s) de reference : 13030 (traitrise) ; 60020 (`Search.EncounterCard`)
- [x] Etape 5 : texte-contre-code, mots-pieges : « exhaust each upgrade » : retour de `ExhaustAll` compte ; « fewer than 2 » : strictement moins ; « Ultron minion » : deck rencontre ET defausse
      Resultat : script relu phrase par phrase contre le scan.
- [x] Etape 6 : nombres texte <-> code : boost 2
      Resultat : conforme a `data/cards.json` (desc) et au script.
- [x] Etape 7 : cas test_capacites : hp018 : 1 amelioration -> Ultron ; 2 -> surge
      Resultat : verts avec le module ; preuve par substitution : voir le bloc « Preuves » en bas.
- [x] Etape 7 bis : limite imprimee ? NON (aucune limite imprimee sur cette carte)
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » en bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (compteur / statut / forme : rendu generique)

Carte terminee : NON (provisoire) : partie reelle humaine non faite ; questions de regle en attente.

---

## Preuves (26/10/2026)

- **Cas** : 43 cas `[hp]` au 26/10 matin ; **59 cas** apres les corrections du 26/10 apres-midi (16 cas ajoutes), tous verts sur le code final (59/59, relances par groupes de 10 a 13 cas ; voir « Corrections du 26/10/2026 »).
- **Preuve par substitution** (`tools/substituer_pack.py`, sources restaurees : empreintes md5 IDENTIQUES avant/apres) : les 20 identifiants ont au moins un cas
  rouge sans leur module. `rouges N/M` avec M > N (hp001a 2/3, hp001c 2/3, hp002 3/4, hp003 2/3, hp005 2/3, hp008 2/3, hp009 2/3) : le cas qui reste vert est a chaque fois
  un TEMOIN d'absence ou une valeur imprimee (valeurs de la face, temoin sans compteur, temoin « injouable dans l'autre forme », temoin alter ego), a assumer.
  hp001a 2/3 : « valeurs imprimees » vert sans module (la face est imprimee, pas scriptee).
- **Statique** : `test_cards.py` 0 erreur ; `verifier_prefixes.py` OK ; `verifier_cibles.py` OK (il a refuse `SetTarget('AttachedEnemy')`, corrige) ;
  `verifier_traductions_fr.py` et `textes-fr-fanmade.test.ts` verts ; `wasp-hank-pym-plateau.test.ts` vert (3 cas, etape 8 bis, rendu generique sans correctif).
- **Defauts trouves PAR les cas ou les logs** (et corriges) : `ForChoiceAbilityWithCost` appelle l'operation avec `(cibles, res)` (un `TypeError` avale laissait Bumble Bee et Man-Mountain
  muets) ; la branche payante est offerte meme impayable et son echec ANNULE tout le changement de forme (`UndoRequest`) : `PeutCouvrirLeCout` ; `face.card_id` n'existe pas
  (`hp007`) ; `SetTarget("AttachedEnemy")` n'existe pas (`hp010`) ; `Search.EncounterCard` prend `include_discard_pile` (`hp018`).

## Modifications du MOTEUR (toutes marquees `# CORRECTIF`)

1. `src/game/player/element/player_setup.py` : l'option « Change To … » (changement de forme LIBRE) n'est pas offerte quand la face imprime « can only change form by card abilities ».
2. `src/game/world/world_stat.py` + `src/game/card/face/model/form.py` : compteur « formes changees CE TOUR » (`AddFormChange` / `CountFormChanges`, remis a zero a `OnTurnBegin` / `OnTurnEnd`).
3. `src/game/card/face/card_face.py` : compteurs imprimes `crisis` et `seize` ajoutes a `COUNTER`.
4. `tools/test_capacites.py` : cle de cas `noms_tour` (outillage de test, additif).
5. (26/10/2026, apres-midi) `src/game/puzzle/puzzle.py` : `Puzzle.NewTurnWorldStat()` (remet a zero les compteurs « ce tour » du monde, `WorldStat.OnTurnEnd`), pour monter X = 0 (hp009 / hp012). Additif.
   Aucun autre fichier du moteur touche pour ces corrections.

## A verifier en partie reelle (aucun outil ne le remplace)

- Une partie complete avec « Wasp (Hank Pym) » dans Fan-made : demarrage en alter ego, **aucun bouton « Change To »**, Scientist Supreme -> Size Manipulation -> passage en forme heros (choix de la forme).
- Le choix de la forme cible quand deux formes sont possibles (invites `AskChooseOneText` : « AVENGER TINY » / « AVENGER GIANT » / « GENIUS ») : lisibilite de l'invite.
- Bumble Bee / Man-Mountain : l'ecran de choix a deux branches (la branche payante n'apparait que si le cout est couvrable).
- Gigantification / Self-Shrinking : les Interruptions de defense au vrai moment d'une attaque ennemie (fenetre d'Interruption).
- Huge Surprise attachee a un ennemi : affichage, perte de Steady/Stalwart, 4 degats apres Sonne/Desoriente, defausse de fin de round (Temporary).
- Obligation Identity Crisis : ses actions en forme d'alter ego depuis la zone d'obligations.
- Seized Control mis de cote au setup puis revele par Ultron ; Take Over Signal sur un allie reel ; Return of the Prodigal Son (glissement face cachee, boost « reveal this card »).
- Non teste par un cas : « Patrol » ignore par Self-Shrinking, « Guard » absent du plafond d'Ant-Man, Boost de hp014 et hp015, branche « 5 compteurs » de hp013.

## Questions : TOUTES TRANCHEES le 26/10/2026 (historique de la liste d'origine plus bas)

Ordre suivi : (1) Rules Reference v1.8 (`assets/docs/mc01_rules_reference_v18.pdf`), (2) scan de la carte, (3) l'utilisateur seulement en cas de doute reel apres 1 et 2
(consigne du 26/10/2026 : ne pas poser de question que les regles tranchent). Detail, texte imprime et regle citee : `VERDICTS-REGLES-2026-10-26.md`.

| Q | Carte | Decision | Code |
|---|---|---|---|
| 1 a 5 | hp001a/b/c, hp002, hp003 | **A**, reponse de l'utilisateur | inchange |
| 6 | hp004 | A : obligatoire (RR MAY : pas de « may ») | inchange |
| 7 | hp006 | A : un compteur a la fois couvre toutes les repartitions | inchange |
| 8 | hp007 | « a card you control » inclut identite et Mansion (RR OWNERSHIP AND CONTROL) | **corrige** |
| 9 | hp009 | menace repartie « from among schemes » (17029) | **corrige** |
| 10 | hp010 | A : COUT = s'attacher a un ennemi (RR COST ARROW ICON) | inchange |
| 11 | hp012 | A + exactement X designations | **corrige** |
| 12 | hp013 | Shadow of the Past `01190` / Pursued by the Past `45075` EXISTENT : brancher | **corrige** |
| 13 | hp013 | cout = choix + inclinaison de Hank, effet = defausse (RR COST ARROW ICON) | **corrige** |
| 14 | hp014 | A | inchange |
| 15 | hp015 | A (justification corrigee : set nemesis avant melange) ; pas de doublon de hp016 verifie | inchange + cas |
| 16 | hp016 | A : cout IMPRIME de la carte glissee (RR TUCK) | inchange |
| 17 | hp017 | A + trait HACKED + aucun surge imprime | **corrige** |
| 18 | icones de ressource | A : relues sur chaque scan contre `RES` de `cards.json` | inchange |

### Historique : la liste d'origine (option A = celle qui etait CODEE)

1. **« Change form » avec trois formes** (Resize at Will, Size Manipulation, Ant-Man, Pym Particles, Self-Shrinking exclu) : A) on choisit n'importe quelle AUTRE forme (alter ego, minuscule, geant) ; B) depuis une forme heros on ne va qu'a l'alter ego, depuis l'alter ego on choisit la forme heros.
2. **hp001a / hp001c « confuse / stun a minion ... You may spend ... instead »** : A) choix exclusif : sbire OU (en payant) le vilain ; B) deux Reponses separees (on pourrait cumuler).
3. **hp001b Scientist Supreme « If you cannot »** : A) s'il y a un Size Manipulation en jeu on y pose le compteur (au choix si plusieurs), sinon on cherche dans le deck ; B) on cherche aussi quand le compteur ne peut pas etre pose pour une autre raison.
4. **hp002 Ant-Man « Exhaust a Size Manipulation -> move 1 pym counter »** : A) le cout (incliner) est paye meme si la carte n'a plus de compteur (rien n'est deplace) ; B) l'action n'est offerte que si la carte porte un compteur.
5. **hp003 Gigantification (defense) « When an enemy attacks »** : A) toute attaque ennemie (meme contre un allie ou un autre joueur) ; B) seulement contre vous.
6. **hp004 Resize at Will « make a basic attack / thwart without exhausting »** : A) obligatoire si une cible existe (branche unique du choix) ; B) facultative.
7. **hp006 Pym Particles « a total of 2 pym counters on them »** : A) un compteur a la fois, au choix entre les Size Manipulation ; B) repartition libre en un seul choix (2 + 0 possible deja couvert par A).
8. **hp007 Infinite Avengers Mansion** : A) « a card you control » = toute carte sauf l'identite et le Mansion lui-meme ; « identity-specific » = classe Hero du set de l'identite ; B) seulement les cartes pouvant porter un compteur pym (ameliorations, allies, soutiens).
9. **hp009 Bio-Synthetic Wings « remove X threat from among schemes »** : A) une seule manigance cible, X menaces ; B) X reparti entre plusieurs manigances.
10. **hp010 Huge Surprise** : A) Hero Action depuis la carte posee sur le heros, qui s'attache a l'ennemi (« attach this card to an enemy -> ... ») ; « loses steady and stalwart » = -1 chacun ; « takes 4 damage after it is stunned or confused » = une Reponse forcee a chaque carte Sonne/Desoriente posee ; B) la carte se joue directement sur l'ennemi.
11. **hp012 The Stinger « X damage divided among enemies you choose »** : A) un degat par cible choisie (jusqu'a 6), tronque a X, comme Wasp Sting ; B) repartition libre des X points.
12. **hp013 Identity Crisis « Shadow of the Past » / « Pursued by the Past »** : ces deux cartes ne sont PAS dans le zip. A) a 5 compteurs rien ne se passe de plus (seul le comptage est code) ; B) vous les fournissez / les creons (sbire ? complot ?) ; C) a 5 compteurs on revele une carte du deck rencontre.
13. **hp013 « exhaust Hank Pym -> discard this obligation »** : A) l'inclinaison est le cout de la defausse (si Hank est deja incline, l'obligation reste) ; B) l'inclinaison est le cout de l'Action.
14. **hp014 Return of the Prodigal Son** : A) « the upgrade or support in play with the highest cost » = parmi TOUS les joueurs, une seule carte ; le boost « Reveal this card » met la carte en jeu comme une revelation ; B) seulement parmi les cartes du joueur actif.
15. **hp015 Ultron « Find the set-aside Seized Control »** : A) Seized Control est mis de cote au Setup par Hank Pym ; sans lui (autre heros), on cherche une carte HACKED du deck rencontre ; B) Seized Control reste dans le set nemesis melange.
16. **hp016 Seized Control « place it here instead » / « X = cost of the tucked card »** : A) les degats deviennent des compteurs `damage` sur la carte ; X = cout IMPRIME de la/les cartes glissees ; B) X = cout actuel.
17. **hp017 Take Over Signal** : A) on reutilise `TreatAttachedCardAsMinion` (l'allie devient un sbire generique avec SCH = THW imprime) ; « blank text box » et « no consequential damage » : seulement ce que fait ce mecanisme ; B) coder explicitement l'absence de degats consecutifs.
18. **Icones de ressource** (voir l'avertissement en tete) : lues a l'ecran, sans decoupe pixel par pixel contre une carte du meme pack.

## Autoplay et decks (26/10/2026)

- **Autoplay** (`tools/autoplay.py .game-src-hp --deck wasp_hank_pym --vilains rhino --difficultes normal --profils equilibre --parties 8`) : 8 parties, **0 traceback**
  (grep exhaustif NameError / AttributeError / TypeError / KeyError / AssertionError : 0 sur les 8 journaux), 0 partie bloquee, 0 victoire / 8 defaites (5 manigance accomplie, 3 heros eliminé).
  **Temoin** `wasp` (Wasp officielle), meme vilain et memes graines : 0 victoire / 8 defaites, memes causes, 0 bloquee. Le pilote joue un `player_deck` de ressources neutres (deck vide,
  decision du 06/09/2026) : le 0 % ne mesure pas le heros.
  Premiere passe : 2 parties « bloquees » sur 8, toutes deux dues a **hp010 Huge Surprise** : son Hero Action restait offerte une fois la carte attachee au vilain, le pilote la rejouait
  a l'infini. Corrige (condition « pas deja attachee a un ennemi »), puis cas hp010 revert + preuve par substitution hp010 1/1 + autoplay relance.
- **Deck** `wasp_hank_pym` (`verifier_tous_les_decks`, ce deck seul) : **OK** « identite hp001b, main 6, deck 9 ». Deux defauts trouves par cet outil et PAS par les 43 cas :
  1. `game/card/factory.py` : un evenement a DEUX capacites de jeu doit etre declare dans la liste blanche (lecon ls005) : `hp003` et `hp005` ajoutes, sinon AssertionError au setup ;
  2. le pilote du verificateur ne reconnaissait pas le debut de tour d'un heros sans « Change Form » ni « Recover » : option « Play » hors mulligan acceptee (`tools/verifier_tous_les_decks.py`, additif).
- **Passe complete des decks du jeu** : lancee (sous verrou), 55 decks verifies au moment de ce rapport, tous OK sauf `batgirl` (`bg004`, pack d'une autre session) ; elle se poursuit en arriere-plan
  (sortie : scratchpad de la session, `hp_post.out`). **A relire avant tout commit** : le deck wasp_hank_pym y apparaitra ECHEC (passe lancee AVANT les deux corrections ci-dessus) mais reussit
  seul apres elles. La batterie complete `test_capacites` (~2 h) n'a PAS ete relancee : les changements moteur sont additifs (aucun deck existant ne porte la phrase « only by card abilities »).

## Corrections du 26/10/2026 (apres-midi) : arbitrages relus contre le RR v1.8 et les scans

Cartes touchees : **hp007, hp009, hp012, hp013, hp017** (gabarits ci-dessus) ; hp015 / hp016 verifies (justification corrigee, pas de doublon de Seized Control).
Fichiers : `src/cards/pack/wasp_hank_pym/wasp_hank_pym/{hp007,hp009,hp012,hp013}.py`, `.../wasp_hank_pym_nemesis/hp017.py`, `src/game/puzzle/puzzle.py` (`NewTurnWorldStat`, additif),
`tools/cas/wasp_hank_pym.py` (16 cas et 3 cles de verification : `hp_hote_trait`, `hp_exemplaires`, `hp_degats_somme`, `hp_menace_nulle_ou_absente`), `ui-app/src/board/wasp-hank-pym-plateau.test.ts` (1 cas),
`docs/reference/mots-cles/find.md` (fiche creee : « find » n'en avait pas ; elle aurait du preceder le script de hp013).

- **Rouge avant, vert apres** : chaque nouveau cas de correction a ete lance sur l'ANCIEN code et vu rouge (hp007 x2, hp009 x1, hp012 x1, hp013 x3, hp017 x3), sauf :
  le cas hp013 « Pursued by the Past » dans sa version finale (carte a deux faces `45075a,45075b`) : vu rouge sur sa premiere version (une seule face), pas relance sur l'ancien code (qui ne faisait que compter) ;
  les temoins d'absence (X = 0, 4 compteurs seulement, ni l'une ni l'autre carte, branche menace de hp013), verts avant comme apres par construction.
- **Substitution** (module remplace par `GetAbilities -> []`, puis restaure, empreintes verifiees) : hp007 rouges 3/3, hp009 4/5, hp012 3/3, hp013 7/8, hp017 3/4. Les cas qui restent verts sont des temoins d'ABSENCE d'effet (assume).
- **Pack complet** : 59/59 cas `[hp]` verts. `verifier_appels_modules` OK (calibre : un appel inexistant ajoute a la main le fait tomber), `verifier_cibles` OK, `verifier_prefixes` OK,
  deck `wasp_hank_pym` monte une partie (« identite hp001b, main 6, deck 9 »), plateau 4/4.
- **Autoplay** : `wasp_hank_pym` contre Rhino, 8 parties, **0 traceback** (grep NameError / AttributeError / TypeError / KeyError / AssertionError : 0 sur les 8 journaux), 0 bloquee, 0 victoire / 8 defaites (5 manigance, 3 heros elimine) ;
  temoin `wasp` memes graines : 0 / 8, memes causes, 0 traceback. Le journal montre l'obligation hp013 revelee et ses compteurs crisis poses en vraie partie ; **le pilote ne joue jamais les Actions de hp007, hp009, hp012, hp013 (il les joue en ressource)
  ni la branche a 5 compteurs** : ces chemins ne sont prouves que par les cas.
- **Non lance** : la batterie complete `test_capacites` (~2 h) et la passe `verifier_tous_les_decks` complete (le moteur n'a recu qu'une methode `Puzzle` additive) ; `test_cards.py` (ecrit `/tmp/cards_stdout.log`, fichier partage avec les autres sessions).
- **Piege rencontre** : `place_player` de `45075a` (compteur « pursuit ») : voir `mots-cles/find.md`. Autre piege d'outillage : sans `CAS_PREFIX=<prefixe>`, deux sessions qui lancent `test_capacites` en meme temps se partagent `/tmp/capacites_<index>.json` et les rapports se melangent (constate : cas decales).

### A verifier en partie reelle (aucun outil ne le remplace)

- hp007 : poser le compteur pym sur Hank Pym lui-meme (invite de choix : identite, Mansion, autres cartes) ; lisibilite de l'invite.
- hp009 / hp012 : repartition des X menaces / X degats en plusieurs designations (UI de choix repete), avec 2 manigances / 2 ennemis ; X = 0 : l'Action ne propose-t-elle aucune cible sans bloquer ?
- hp013 : le cout a deux temps (choix degats / menace PUIS inclinaison) ; l'Action absente quand Hank est incline ; la branche a 5 compteurs dans une vraie partie avec Standard III (Pursued by the Past en jeu) et sans.
- hp017 : le sbire « Hacked » issu d'un allie du deck (entre en jeu engage) ; la carte defaussee quand il n'y a aucun allie.

## Preuves complémentaires du 26/10/2026

- **hp013** : le cas « 5e compteur, AUCUNE Shadow of the Past, Pursued by the Past (45075a) en jeu → 7 compteurs pursuit » est ROUGE quand l'ancien défaut est réintroduit (branche `Pursued by the Past` neutralisée : `hp015 n'est pas en jeu`), vert avec le script réel (fichier restauré, empreinte identique).
- **hp007** : le test plateau « compteur pym sur l'identité » (`ui-app/src/board/wasp-hank-pym-plateau.test.ts`) est ROUGE quand `compteursAffiches` ignore les identités (mutant temporaire de `card-model.ts`, restauré à l'identique), vert sinon.

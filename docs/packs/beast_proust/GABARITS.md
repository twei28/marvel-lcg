# Beast (Proust) : gabarits PROCESSUS-CARTE, 02/11/2026

Pack `beast_proust` (prefixe `bs`, set 247, auteur Proust). Scripts : `src/cards/pack/beast_proust/{beast_proust,beast_proust_nemesis}/` (18 cartes). Cas : `tools/cas/beast_proust.py` (75). Deck : `deck/starter/beast_proust.json` (`player_deck` VIDE : aucun Extras). Textes FR : `ui-app/src/board/textes-fr-fanmade.ts` (+ copie `public/js/traduction/textes-fr-fanmade.js` regeneree). Biographie : `heros-info.js` (`bs001a`). Plateau : `ui-app/src/board/beast-proust-plateau.test.ts`. Ecran : `ui-check/tests/beast-proust-ecrans.spec.ts`.

## Source et decisions

- ⚠ Un AUTRE Beast existe (D0natello, `bt`, set 134, deck `beast`) : celui-ci est « Beast (Proust) » (nom de la carte heros, nom du deck). Le set nemesis `Beast Proust Nemesis` evite toute collision de set.
- Matiere : 24 scans FR seuls (pas d'EN, pas de dos) : **le texte EN de `cards.json` est TRADUIT du FR** par l'assistant ; le texte canonique est donc le scan FR (relu carte par carte contre `cards.json` le 02/11/2026). Les scans vont dans `assets/pics-fr/fr_bs*.jpg` ET dans `assets/pics/bs*.jpg` (la meme image : aucun scan EN n'existe, sans cela le mode anglais n'aurait aucune image), et `SCANS_FR_FANMADE` (`scans-fr.ts`) les declare « deja francais » : aucun voile FR.
- Icones verifiees contre le pack : l'icone « noeuds relies » de Spider-Tracers (bs005) est la ressource [mental] (meme icone que la pastille de bs008, `RES = B`). ATQ de Black Beast = `0*` (l'etoile du scan), pas `0`.
- Compteurs `tracer` (bs005) et `psy` (bs008) ajoutes a l'enum `COUNTER` de `card_face.py` : sans eux la carte tombe a la construction.
- Hero deck = les 16 numeros « n/16 » ; obligation bs013 ; nemesis bs014 + bs015 + bs016 x2 + bs017.
- Particularites de test : le Lab est en jeu des la mise en place (Setup natif) ; `PlaceUnder('<carte>', 'bs002')` pose une carte sous le Lab ; Sandman `01102` est Tenace (utiliser Hydra Mercenary `01101` pour un sbire vaincu) ; `CreatePlayerDeck` : la derniere carte citee est au dessus ; le pilote accepte par defaut une option « you may » (refus : `choisir_option=["Cancel"]`). Cle de harnais ajoutee : `jouer_sous_tolerant`.

### bs001a

- [x] Etape 2 : carte(s) de reference : `td012`/`gs099q` (glisser une carte en jeu), `12016` (`GainUntilRoundEnd`), `14001a` (`Faces.ReadyAll`, limite par phase), `CostFunc.Custom` (RECETTES §5).
- [x] Etape 5 : mots-pieges : « Tuck a TECH upgrade YOU CONTROL » = COUT (avant la fleche) vers le Lab ; « ready YOUR HERO » ; « choose THW, ATK or DEF » : un seul ; « X = PRINTED cost » (`printed_cost.val`, pas le paye) ; « until the end of the ROUND » ; « Limit once per PHASE ». Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : PV 14, main 4, ATQ 1, CTR 1, DEF 2. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (8) : Repurposing — Belt (TECH, cout 3) glissee sous le Lab, heros REDRESSE, +3 ATQ jusqu'a la fin du round (ATQ 1 -> 4) ; Repurposing — meme position, on choisit CTR : +3 CTR (1 -> 4), ATQ et DEF inchangees ; Repurposing — Xavier's Cerebro (cout IMPRIME 5, meme reduit a 4 au jeu) : +5 DEF (2 -> 7) ; Repurposing — TEMOIN : une amelioration NON TECH (Ultimate Mutation) n'est pas glissable : rien sous le Lab, elle reste en jeu ; Repurposing — LIMITE une fois par phase : deux ameliorations TECH en jeu, un seul emploi (1 carte glissee, la 2e reste en jeu) ; Repurposing — TEMOIN : en forme alter-ego la capacite de la face heros n'existe pas (rien glisse) ; Repurposing — sans Beast's Lab en jeu l'Action n'est pas offerte (la Belt reste en jeu) ; Repurposing — plafond du Lab : 3 cartes deja glissees, une 4e par l'Action : le joueur defausse jusqu'a n'en garder que 3. Substitution : **rouges 4/8** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d'epuisement : voir les cas LIMITE / plafond ci-dessus, chiffre mesure au second emploi.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs001b

- [x] Etape 2 : carte(s) de reference : `dy001b` / `01040b` (`WhenCardSetup` + `Search.PlayerCard`), `PutIntoPlay(under_control=True)` (face_on_event.py:170), `ma005` (Action + limite par phase).
- [x] Etape 5 : mots-pieges : Setup d'identite ET Setup natif du Lab : le Lab est deja en jeu, la recherche ne trouve rien (pas de double entree) ; « a RESOURCE card » : type Resource, deck OU defausse, ajoutee a la main ; limite par phase. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : PV 14, REC 4, main 5. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (5) : Setup — si Beast's Lab etait RESTE dans le deck, la capacite de mise en place le met en jeu sous le controle du joueur ; Resourceful — Action : une carte RESSOURCE du deck (Genius, pas Beast's Lab ni une amelioration) est ajoutee a la main ; Resourceful — la recherche couvre aussi la DEFAUSSE : une ressource de la defausse est ajoutee a la main ; Resourceful — LIMITE une fois par phase : au 2e emploi rien n'est offert (1 seule ressource ajoutee : 2 cartes en main, et non 3) ; Resourceful — TEMOIN : en forme HEROS la capacite de l'alter-ego n'existe pas, rien n'est ajoute. Substitution : **rouges 4/5** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d'epuisement : voir les cas LIMITE / plafond ci-dessus, chiffre mesure au second emploi.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs002

- [x] Etape 2 : carte(s) de reference : `tc013` / `td012` (`AttachedCardCanPlayLikeInHand`), `sf010` (`AfterCardsMoved` pour une regle de plafond), `permanent.md` / `setup.md` (natifs).
- [x] Etape 5 : mots-pieges : « UPGRADES tucked » : le type filtre (un evenement glisse n'est pas jouable) ; « MAY be played as if in hand » : jouer seulement (ni depenser ni defausser) ; « MORE THAN 3 » : plafond a 3, le joueur choisit. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : plafond 3, aucun cout imprime (Setup + Permanent natifs). Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (5) : Setup — Beast's Lab est en jeu et PRET des la mise en place (Permanent + Setup) ; Lab — une amelioration glissee dessous est JOUABLE comme en main (Bobby's Belt, cout 3 paye par deux Energy) : elle entre en jeu ; Lab — TEMOIN : une carte qui n'est PAS une amelioration (Beastly Charge, evenement) glissee dessous N'est PAS jouable comme en main ; Lab — plafond : 3 cartes glissees + une 4e (Tech Support, recherche) : le joueur defausse jusqu'a n'en garder que 3 ; Lab — TEMOIN du plafond : 2 cartes glissees + une 3e : aucune defausse, 3 restent. Substitution : **rouges 2/5** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d'epuisement : voir les cas LIMITE / plafond ci-dessus, chiffre mesure au second emploi.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : cas plateau `beast-proust-plateau.test.ts` (cartes glissees dessinees derriere leur hote, lisibles par leur proprietaire) ; pas vu ROUGE sur le code (le dessin des cartes glissees est generique, `zones.ts`), mais le meme test devient rouge quand le lien `bind_object_id` est casse (mutation verifiee le 02/11/2026).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs003

- [x] Etape 2 : carte(s) de reference : `04159a` (`GiveKeywordToAttached(Hero, ..)`), `nt009` / `22032` (`UnitAttackGainKeyword("AttachedHero", piercing=True)`), `piercing.md`.
- [x] Etape 5 : mots-pieges : « BEAST gets » = forme heros seulement (`Hero`) ; « +4 hit points » (branche ignore_flip) ; « his BASIC attacks gain piercing » : `is_basic_attack=True`. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 3, DEF +1, PV +4. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (4) : Ultimate Mutation — jouee (cout 3, deux Strength) : DEF +1 (2 -> 3) et PV max +4 (14 -> 18) ; Ultimate Mutation — TEMOIN : sans la carte, DEF 2 et PV max 14 ; Ultimate Mutation — les attaques de base PERCENT : Rhino Tough, ATQ 1 : le Tough est defausse ET le degat passe (1) ; Ultimate Mutation — TEMOIN : sans la carte, l'attaque de base est ABSORBEE par le Tough (0 degat, Tough defausse). Substitution : **rouges 2/4** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs004

- [x] Etape 2 : carte(s) de reference : `nt005` (`ReduceCostToPlayThis`), `14001a` / `20010` (`WhenUnitUseBasicPower`), `mantis/__init__.py RetirerUneMenace` (choix + cible), `hz006` (`this.DealDamage`).
- [x] Etape 5 : mots-pieges : reduction TECH (la carte ne se compte pas) ; « BASIC power » : ATQ/CTR/DEF, pas la recuperation ; « CHOOSE » : une branche, offerte si une cible existe. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 3, reduction 1, 1 degat, 1 menace. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (5) : Gloves — REDUCTION : avec une amelioration TECH en jeu (Belt) le cout 3 devient 2 : un seul Energy (YY) la paie ; Gloves — TEMOIN : sans amelioration TECH en jeu le cout reste 3 : un seul Energy (2 icones) ne suffit pas, la carte reste en main ; Gloves — Interruption (branche degat) : quand Beast utilise un pouvoir de base (attaque ATQ 1), 1 degat a un ennemi s'ajoute : Rhino subit 1 + 1 = 2 ; Gloves — Interruption (branche menace) : un pouvoir de CONTRE (CTR 1) retire 1 menace en plus (5 - 1 - 1 = 3) ; Gloves — TEMOIN : en forme alter-ego (recuperation de base, pas un pouvoir ATQ/CTR/DEF) rien n'est inflige. Substitution : **rouges 3/5** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs005

- [x] Etape 2 : carte(s) de reference : `53006` (`CanGenerateResources(.., CardFinder2(trait))` + `CostFunc.Counter`), `16036` (`ThisEnterPlayWithCounters`, PAS `Uses`), `nt005`.
- [x] Etape 5 : mots-pieges : 4 pions `tracer` (nouveau dans l'enum) ; « Resource » (pas Hero Resource) ; « for a TECH CARD » ; ICONE [mental] verifiee contre bs008 et lj005 ; « Limit once per CARD » : au plus un tracer par carte payee. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 3, 4 pions, 1 ressource [mental]. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (4) : Spider-Tracers — entre en jeu avec 4 compteurs tracer (jouee, cout 3, deux Strength) ; Spider-Tracers — Ressource : 1 compteur retire, 1 ressource [mental] pour une carte TECH : Gloves (TECH, cout 3 - 1 = 2) payee par le tracer + un Strength ; Spider-Tracers — TEMOIN : pour une carte NON TECH (Ultimate Mutation) le tracer ne paie PAS : 4 compteurs, la carte reste en main (un Strength ne suffit pas) ; Spider-Tracers — « Limit once per card » : pour une carte TECH de cout 2 (Reactor reduit), un seul tracer par carte : le tracer SEUL (1) ne paie pas, la carte reste en main. Substitution : **rouges 3/4** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d'epuisement : voir les cas LIMITE / plafond ci-dessus, chiffre mesure au second emploi.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : cas plateau `beast-proust-plateau.test.ts` (cartes glissees dessinees derriere leur hote, lisibles par leur proprietaire) ; pas vu ROUGE sur le code (le dessin des cartes glissees est generique, `zones.ts`), mais le meme test devient rouge quand le lien `bind_object_id` est casse (mutation verifiee le 02/11/2026).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs006

- [x] Etape 2 : carte(s) de reference : `28027` (`WhenUnitWouldTakeDamage(NonKeyword, "You")` + `ReduceDamage`), `nt005`.
- [x] Etape 5 : mots-pieges : « Reduce the damage Beast takes by 1 » : tous les degats (attaque ou non), par instance ; « BEAST takes » : forme heros seulement (contre-cas alter-ego). Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 3, reduction 1, degats -1. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (3) : Belt — 2 degats d'attaque de Rhino (heros incline, pas de defense) : la Belt les reduit de 1 (1 subi) ; Belt — TEMOIN : sans la Belt Rhino inflige ses 2 degats ; Belt — TEMOIN : en forme ALTER-EGO la Belt ne reduit rien (« Beast takes ») : 2 degats. Substitution : **rouges 1/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs007

- [x] Etape 2 : carte(s) de reference : `04159a` (`GiveKeywordToAttached(Hero, hand_size=..)`), `nt005`.
- [x] Etape 5 : mots-pieges : « while you are in hero form » : bonus sur la face heros seulement (contre-cas alter-ego, lecon an002). Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 3, main +1. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (2) : Reactor — taille de main +1 en forme heros (4 -> 5) ; Reactor — TEMOIN : en forme ALTER-EGO aucun bonus (main 5). Substitution : **rouges 1/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs008

- [x] Etape 2 : carte(s) de reference : `hz006` (Exhaust + Counter + `SetTarget(Enemy, range="All")`), `16036`, `nt005`.
- [x] Etape 5 : mots-pieges : 2 pions `psy` ; « Remove 1 psy counter AND exhaust it » : deux couts ; « EACH enemy IN PLAY » : villain + sbires ; icone [mental] de la pastille = reference de bs005. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 5, 2 pions, 3 degats. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (4) : Cerebro — entre en jeu avec 2 compteurs psy ; AVEC une amelioration TECH (Belt) en jeu son cout 5 devient 4 : deux Energy (4 icones) la paient ; Cerebro — TEMOIN : sans amelioration TECH le cout reste 5 : deux Energy (4) ne suffisent pas ; Cerebro — Action : 1 compteur psy retire, Cerebro inclinee, 3 degats a CHAQUE ennemi (Rhino ET Hydra Mercenary, 3 PV : vaincu) ; Cerebro — 2 compteurs seulement : le 3e emploi est refuse (6 degats a Rhino, et non 9) et 0 compteur. Substitution : **rouges 3/4** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : cas plateau `beast-proust-plateau.test.ts` (cartes glissees dessinees derriere leur hote, lisibles par leur proprietaire) ; pas vu ROUGE sur le code (le dessin des cartes glissees est generique, `zones.ts`), mais le meme test devient rouge quand le lien `bind_object_id` est casse (mutation verifiee le 02/11/2026).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs009

- [x] Etape 2 : carte(s) de reference : `nt005` (`SetPlay` + cout d'inclinaison), `dy013` (`ForChoiceAbility(.., condition=..)`), `Search.PlayerCard(include_player_deck, include_discard_pile)`.
- [x] Etape 5 : mots-pieges : « Exhaust the Lab, THEN choose » : cout commun aux deux branches ; UNE seule capacite `Play` (RECETTES §5) ; « deck OR discard pile » ; « TECH upgrade ». Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 0. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (5) : Tech Support — branche RECHERCHE : une amelioration TECH du deck (Belt) est glissee sous le Lab, le Lab est incline ; Tech Support — la recherche couvre la DEFAUSSE : un Reactor de la defausse est glisse sous le Lab ; Tech Support — TEMOIN : une amelioration NON TECH (Ultimate Mutation) n'est pas trouvee : rien sous le Lab ; Tech Support — branche DEFAUSSE : la carte glissee (Belt) est defaussee, le heros incline est REDRESSE, le Lab est incline ; Tech Support — TEMOIN : Lab deja INCLINE (cout impayable) : l'evenement n'est pas joue, il reste en main. Substitution : **rouges 4/5** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : cas plateau `beast-proust-plateau.test.ts` (cartes glissees dessinees derriere leur hote, lisibles par leur proprietaire) ; pas vu ROUGE sur le code (le dessin des cartes glissees est generique, `zones.ts`), mais le meme test devient rouge quand le lien `bind_object_id` est casse (mutation verifiee le 02/11/2026).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs010

- [x] Etape 2 : carte(s) de reference : `01053` (`hero.DealDamage(.., property=AttackProperty(overkill=..))`), `ra011` / `nt014` (`MayChooseOneAbility`), `overkill.md`.
- [x] Etape 5 : mots-pieges : « YOU MAY exhaust AND discard » : option refusable a deux couts ; « THIS ATTACK gains overkill AND deals X additional » : 6 + X avec overkill ; X = cout IMPRIME de la carte defaussee. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 3, 6 degats, X additionnels. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (5) : Beastly Charge — sans l'option : 6 degats a Rhino, le Lab reste PRET, rien n'est defausse ; Beastly Charge — AVEC l'option : le Lab est incline, Cerebro (cout imprime 5) defausse : 6 + 5 = 11 degats a Rhino ; Beastly Charge — OVERKILL : sbire Hydra Mercenary (3 PV), Gloves (cout 3) defausse : 6 + 3 = 9, 6 exces vont au vilain ; Beastly Charge — TEMOIN : sans l'option, la meme attaque sur Hydra Mercenary (3 PV, 6 degats) ne deborde PAS : Rhino intact ; Beastly Charge — TEMOIN : Lab incline : l'option n'est pas offerte (6 degats, la carte glissee reste). Substitution : **rouges 5/5** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs011

- [x] Etape 2 : carte(s) de reference : `mf009` (`RemoveThreatFromSchemes`), `YouMayFlipToYourAlterEgoForm` (`ChangeToForm(AlterEgo)`), `bs010` (option a cout).
- [x] Etape 5 : mots-pieges : « Remove 3 threat from A scheme » ; « YOU MAY exhaust AND discard TO change to alter-ego form » : option refusable, apres le retrait. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 2, 3 menaces. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (3) : Civil Genius — 3 menaces retirees d'une manigance (5 -> 2) ; sans carte glissee rien d'autre n'est offert (forme heros conservee) ; Civil Genius — AVEC l'option : le Lab s'incline, la carte glissee (Belt) est defaussee, Beast passe en forme ALTER-EGO ; Civil Genius — TEMOIN : l'option est REFUSEE (« you may ») : Beast reste en forme heros, le Lab pret, la carte glissee conservee. Substitution : **rouges 3/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs012

- [x] Etape 2 : carte(s) de reference : `dz018` (`AfterYouSpendThisCard`), `bs009` (`ChercherTechEtGlisser`).
- [x] Etape 5 : mots-pieges : « Hero RESPONSE » : sous-type dedie ; « After you SPEND this card » ; « deck OR discard pile » ; « tuck under the Lab ». Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : aucun cout imprime (ressource wild). Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (2) : Tech Genius — apres l'avoir DEPENSEE (avec un Energy pour Ultimate Mutation, cout 3) : une amelioration TECH du deck est glissee sous le Lab ; Tech Genius — TEMOIN : en forme ALTER-EGO la Reponse de HEROS ne part pas : rien sous le Lab. Substitution : **rouges 1/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : cas plateau `beast-proust-plateau.test.ts` (cartes glissees dessinees derriere leur hote, lisibles par leur proprietaire) ; pas vu ROUGE sur le code (le dessin des cartes glissees est generique, `zones.ts`), mais le meme test devient rouge quand le lien `bind_object_id` est casse (mutation verifiee le 02/11/2026).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs013

- [x] Etape 2 : carte(s) de reference : `dy013` / `mt011` (`WhenThisObligationGiveToYou`), `mf017` / `sl029` (`ShuffleAllTo(.., "EncounterDeck")`), `ar012` (`DealEncounterCards`).
- [x] Etape 5 : mots-pieges : « ALL cards tucked » ; « THEN discard Overworked » ; « NO TECH upgrade discarded THIS WAY » : seules les cartes glissees comptent ; « deal yourself 1 FACEDOWN card THEN shuffle Overworked » : la carte distribuee d'abord. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : boost 3, 1 carte distribuee. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (4) : Overworked — une amelioration TECH (Belt) et une autre (Mutation) glissees : TOUTES defaussees, l'obligation est defaussee, AUCUNE carte distribuee ; Overworked — AUCUNE amelioration TECH defaussee (seule Mutation, non TECH, etait glissee) : une carte Rencontre est distribuee face cachee, puis l'obligation est melangee dans le deck rencontre ; Overworked — Lab vide : rien n'est defausse, donc la carte est distribuee ET l'obligation melangee dans le deck ; Overworked — TEMOIN : une amelioration TECH EN JEU (pas glissee) ne compte pas : la carte est distribuee. Substitution : **rouges 4/4** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs014

- [x] Etape 2 : carte(s) de reference : `27156` / `mf015` (`PlaceThreatOnSchemes([this], n)`), `acceleration.md`.
- [x] Etape 5 : mots-pieges : « 1 threat for EACH upgrade IN PLAY » : tous les joueurs, les cartes glissees ne comptent pas ; « on THIS card ». Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : menace de depart 5, boost 2, acceleration 1. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (2) : Technical Difficulties — a la revelation : 1 menace par amelioration EN JEU (Belt + Mutation = 2) en plus des 5 de depart (7) ; une carte glissee sous le Lab ne compte pas ; Technical Difficulties — TEMOIN : aucune amelioration en jeu : 5 menaces de depart seulement. Substitution : **rouges 1/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs015

- [x] Etape 2 : carte(s) de reference : `dy001a` (`ThisGainKeyword(.., change_on_event=[OnEvent.PlacedCard(..)])`), `gs099q` (glisser une amelioration EN JEU), `ra031` (cout le plus eleve).
- [x] Etape 5 : mots-pieges : [star] = l'etoile de l'ATQ (`ATK = "0*"`), pas un boost ; « PRINTED resource cost » ; « highest-cost TECH upgrade YOU CONTROL » (egalite : le joueur choisit) ; « If you cannot » : dessus du deck. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : PV 6, SCH 2, ATQ 0*, boost 4. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (6) : Black Beast — a la revelation : l'amelioration TECH de cout le plus ELEVE (Cerebro 5, devant Gloves 3) QUITTE le jeu pour aller sous lui ; son ATQ vaut 0 + 5 ; Black Beast — egalite de cout (Gloves, Belt : 3) : le joueur choisit ; l'ATQ vaut 3 ; Black Beast — SANS amelioration TECH : la carte du DESSUS du deck (Beastly Charge, cout 3) est glissee sous lui : ATQ 3 ; Black Beast — une amelioration NON TECH (Mutation) en jeu ne compte pas : la carte du dessus du deck est glissee, la Mutation reste en jeu ; Black Beast — TEMOIN : rien sous lui, ATQ 0 (imprimee) ; Black Beast — une carte sans cout imprime (Energy, ressource) glissee sous lui : X = 0. Substitution : **rouges 5/6** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : cas plateau `beast-proust-plateau.test.ts` (cartes glissees dessinees derriere leur hote, lisibles par leur proprietaire) ; pas vu ROUGE sur le code (le dessin des cartes glissees est generique, `zones.ts`), mais le meme test devient rouge quand le lien `bind_object_id` est casse (mutation verifiee le 02/11/2026).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs016

- [x] Etape 2 : carte(s) de reference : `nt015` (`DealIndirectDamage`), `dy013` (`GainSurge`).
- [x] Etape 5 : mots-pieges : « A TECH upgrade YOU CONTROL » : une carte glissee n'est pas controlee ; X = cout IMPRIME ; « If NO upgrade is discarded BY THIS EFFECT » : surge. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : boost 2, X = cout imprime. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (4) : Evil Genius — Cerebro (TECH, cout imprime 5) est defausse : 5 degats indirects a l'identite ; Evil Genius — deux ameliorations TECH (Belt 3, Cerebro 5) : le JOUEUR choisit celle qui est defaussee (Belt : 3 degats) ; Evil Genius — AUCUNE amelioration TECH (Mutation seulement) : rien n'est defausse, 0 degat, la carte gagne SURGE (la carte suivante est distribuee) ; Evil Genius — TEMOIN : une amelioration TECH seulement GLISSEE sous le Lab n'est pas « controlee » : surge, la carte glissee reste. Substitution : **rouges 4/4** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

### bs017

- [x] Etape 2 : carte(s) de reference : `ar013` (`AttachToFaceWhenPutIntoPlay(.., if_cannot_attach_to=Villain)`), `01099` / `01141` (`ATK+` / `SCH+` natifs), `01100` (defausse de l'attachement), `tc001a` (`CostFunc.Discard("YouControlCards", card_type=Upgrade)`).
- [x] Etape 5 : mots-pieges : « Attach to BLACK BEAST. If you cannot, the VILLAIN » ; « Discard AN upgrade YOU CONTROL » = cout ; bonus natifs. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : boost 3, ATQ +1, SCH +1. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (4) : Glasses — mise en jeu avec Black Beast : elle s'attache a LUI (ATQ 0 + 1, SCH 2 + 1) ; Glasses — SANS Black Beast : elle s'attache au VILAIN (Rhino) ; Glasses — Action : une amelioration du joueur (Mutation) est defaussee en cout, l'attachement est defausse ; Glasses — TEMOIN : sans amelioration a defausser l'Action n'est pas offerte, l'attachement reste. Substitution : **rouges 4/4** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 (3 profils x 8, 0 bloquee) parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : cas plateau `beast-proust-plateau.test.ts` (cartes glissees dessinees derriere leur hote, lisibles par leur proprietaire) ; pas vu ROUGE sur le code (le dessin des cartes glissees est generique, `zones.ts`), mais le meme test devient rouge quand le lien `bind_object_id` est casse (mutation verifiee le 02/11/2026).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 181/181 decks montent).

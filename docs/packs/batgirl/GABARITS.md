# Pack Batgirl (ES, « Sealed 11.26.2025 », prefixe `bg`) : gabarits PROCESSUS-CARTE

Etat du 26/10/2026 (apres la consigne du coordinateur). **Aucune carte n'est « terminee »** : il manque la partie reelle jouee par un humain
et plusieurs questions de regle restent en attente. Les trois defauts du premier rapport sont CORRIGES :

- **bg003 Nightwing** : la conversion en wild n'agissait pas parce que l'effet temporaire se detruisait au PREMIER calcul des moyens de
  paiement (le moteur calcule un apercu puis relit au paiement). Il dure maintenant jusqu'a la fin du tour et ne convertit que la PREMIERE
  ressource generee (`ConvertirEnWild`, `__init__.py`). Cas vert : Batarangs payee RR devient wild + physique, 4 degats.
- **bg006 Master Plan, option 1** : le cas etait mal monte (le `declencher` du harnais part AVANT `jouer`) ; la carte donne maintenant +2 au
  pouvoir tout de suite (`GainThwart`...) et le retire apres la prochaine utilisation (`AfterUnitUseBasicPower`, qui part, contrairement a
  `WhenUnitUseBasicPower` pose en temp). Cas vert (THW 2 -> 4, temoin 2).
- **bg012 Utility Belt** (CORRIGE le 26/10/2026, voir son gabarit) : Hero Action FACULTATIVE `exhaust -> l'evenement suivant coute 1 de moins`
  (`Worlds.UpdateNextCardPlayCost`), forme heros seulement ; l'ancienne reduction automatique est retiree. +1 main = `WhenPlayerEndPhase` (la fenetre
  « juste avant la pioche de fin de tour », celle de `WhenPhaseEnd` arrive APRES la pioche), retire en `AfterPhaseEnd`, conditionne a « prete ».
  Ajout de test : `Puzzle.PlayersEndPhaseDraw` (`puzzle.py`, marque CORRECTIF).

Cas ajoutes : temoin d'epuisement de la limite de The Oracle (2 cartes, 4 degats au lieu de 8), Black Mask a SCH 0 (carte rencontre donnee) et SCH 1
(temoin), Psychological Torture a deck epuise (le vilain manigance), Master Plan temoin, Utility Belt (3 cas de plus). Cas plateau :
`ui-app/src/board/batgirl-plateau.test.ts` (compteur recon dessine apres l'attachement, sbire engage et manigance d'annexe dessines) ; la carte
rencontre donnee face cachee par Black Mask n'a pas de dessin propre.

**bg001c (face hero_alts)** : le harnais ne sait PAS l'exercer, noir sur blanc : `Puzzle.ChangeToFace` echange les deux faces d'UNE MEME carte
(bg001a/bg001b) ; bg001c est une troisieme face declaree seulement dans `metadata.hero_alts` du deck, que le lanceur injecte dans le deck envoye
au moteur. Aucun cas ne peut la monter. Preuves de remplacement : son script est identique a celui de bg001a (diff), `test_cards` le construit,
ses valeurs imprimees sont celles de `cards.json` (PV 10, ATK 1, THW 2, DEF 2, main 5, trait BAT FAMILY), et `verifier_tous_les_decks` monte le
deck de base. A confirmer en partie reelle : le choix « Batgirl (Bat Family) » dans le selecteur d'identite.

### bg001a : * Batgirl (Birds of Prey)

- [x] Etape 2 : cartes de reference : The Oracle : aucune carte officielle ne change l'icone d'un texte ; modele du MECANISME : `rz018` (WhenCardWouldResolveAbility), `ho006` (WhenPlayerPlayCard)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : interruption ; « resolve the effect of a card » ; « once per round ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : PV 10, ATK 1, THW 2, DEF 2, main 5.
- [x] Etape 7 : cas test_capacites : cas `[bg] bg001a` : valeurs, Oracle sur Applying Pressure (VERT), temoin sans changement ; substitution : rouge 1/3 sans module (valeurs imprimees + temoin d'absence restent verts, assume).
- [x] Etape 7 bis : limite imprimee ? OUI (une fois par round, par fenetre) : cas `The Oracle : limite UNE fois par round` VERT (Applying Pressure change, Batarangs non : 4 degats et pas 8).
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : Oracle limite aux cartes du PACK (registre `ICONES_DU_TEXTE`) : les cartes OFFICIELLES ne sont pas modifiables

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg001b : * Barbara Gordon

- [x] Etape 2 : cartes de reference : `40044` Pip the Pug (carte remise sur le deck), `01027` (DrawUp)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « bottommost », « printed resource », « this round », « once per round ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : PV 10, REC 3, main 6.
- [x] Etape 7 : cas test_capacites : 4 cas VERTS : carte la plus ANCIENNE remontee, temoin sans exploit, exploit (ennemi vaincu) = pioche, limite 1/round (2 Actions, une seule carte deplacee) ; substitution : rouge 4/5.
- [ ] Etape 7 bis : limite imprimee ? limite : cas d'epuisement VERT (2e Action sans effet).
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : `bottommost` = premiere carte ENTREE dans la defausse (indice 0) : lecture a confirmer

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg001c : * Batgirl (Bat Family)

- [x] Etape 2 : cartes de reference : copie EXACTE de bg001a (script identique, verifie par diff)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : —. Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : memes valeurs que bg001a, trait BAT FAMILY.
- [x] Etape 7 : cas test_capacites : AUCUN cas : le harnais ne sait pas monter une face alternative declaree par `hero_alts` (`ChangeToFace` exige les deux faces d'une meme carte) ; substitution : AUCUN CAS (gate non tenue, assumee).
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : False), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : a verifier en partie reelle : choix « Batgirl (Bat Family) » dans le selecteur d'identite

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg002 : * Black Canary

- [x] Etape 2 : cartes de reference : `06012` Valkyrie (paiement lu a l'entree en jeu), `01083` (Stunned)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « for each [mental] resource used to pay », « enters play ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : cout 3, ATK 2*, THW 2**, PV 3.
- [x] Etape 7 : cas test_capacites : 2 cas : payee BBBB -> sonne (VERT), temoin sans [mental] (VERT) ; substitution : rouge 1/2.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : `message.paid_cost` de `WhenCardEnterPlay` ; le wild compte comme [mental] (`GetColor` converti)

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg003 : * Nightwing

- [x] Etape 2 : cartes de reference : `ah001a` Hypermind (CheckEffectGeneratedResources)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « next resource you generate », « basic power ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : cout 3, ATK 1, THW 2*, PV 3.
- [ ] Etape 7 : cas test_capacites : 2 cas VERTS (conversion visible : Batarangs RR -> 4 degats ; temoin 6) ; substitution : rouge 1/2.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : False), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? peut-etre. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : CORRIGE : l'effet temporaire doit rester actif jusqu'au paiement (voir en-tete). Ecart : dure jusqu'a la fin du tour, premiere ressource de CHAQUE generation

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg004 : Applying Pressure

- [x] Etape 2 : cartes de reference : `18020` Hit and Run (attack/thwart), `10004` Sub-Orbital Leap
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « only [physical] », « this attack defeats an enemy », « attack/thwart ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : cout 2, menace 4, degats 2.
- [x] Etape 7 : cas test_capacites : 3 cas VERTS (RR : 4 menace + 2 degats ; YY : pas de degats ; ennemi vaincu -> pioche) ; substitution : rouge 3/3.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : carte injouable sans menace sur un complot (cible exigee)

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg005 : Batarangs

- [x] Etape 2 : cartes de reference : `23006` Missile Launcher (ranged), `01083`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « for each resource », « gains ranged ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : cout 2, 2 degats, 2 degats/ligne.
- [x] Etape 7 : cas test_capacites : 3 cas VERTS (RR : 6 ; YY : 2 + 2 sonnes ; BB : 2 + 2 desorientes) ; substitution : rouge 3/3.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : wild imprime ne compte pour aucune ligne (question en attente)

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.
- [x] **26/10/2026, arbitrage Wild** (RR « Wild Resource », fiche `mots-cles/wild-resource.md`) : un wild dépensé pour Batarangs compte pour la ligne du type déclaré. Avant : `GetPaidResources()` + `convert_green_res=False` ne comptait le wild dans AUCUNE ligne. Maintenant : `GetPaidResources(not SansType(effect))` (demande le type ; rien demandé sous Recalled Trauma, aucune ligne).
      Cas ajoutés : deux Hellcat déclarés [mental]+[energy] (`preferer_option="BY"` : 2 dégâts, Sonné ET Désorienté) ; deux Hellcat déclarés [physical] (`"RR"` : 6 dégâts). Cas RÉÉCRITS (ils encodaient « le wild ne vaut aucune ligne ») : `bg003` Nightwing (Strength RR → G + R, wild déclaré [mental] : 4 dégâts + Désorienté) et `bg006` option 2 (Strength RR convertie en GG, déclarée [energy] ×2 : 2 dégâts + Sonné, aucune ligne physique). ROUGES vus en rétablissant l'ancien code (4 rouges), VERTS après ; substitution du module : **rouges 5/5**.
      Autoplay ciblé (26/10/2026, `--deck batgirl --vilains rhino --difficultes normal --profils equilibre --parties 8`) : 8 parties, 0 / 8, 0 bloquée, 0 erreur sur les 8 journaux ; témoin `spider_man` : 0 / 8, 0 bloquée, 0 erreur. Batarangs jouée dans les 8 parties (journal lu : « jouer … avec BY », « avec YY »). Aucun wild dans ce deck : le cas unitaire est la preuve du wild.

### bg006 : Master Plan

- [x] Etape 2 : cartes de reference : `ma009` America's Anger, `ah001a`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « choose one », « considered wild », « draw a card ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : cout 0, +2.
- [ ] Etape 7 : cas test_capacites : 4 cas VERTS (option 1 : THW 2 -> 4 + temoin ; option 2 : degats 2 seulement ; pioche) ; substitution : rouge 2/3.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : CORRIGE (voir en-tete). « Draw a card » lu comme appartenant a la 2e puce (question en attente)

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg007 : Calculated Counter

- [x] Etape 2 : cartes de reference : `01075` Black Widow (annuler une carte revelee), `03005` (interruption d'evenement)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « using only [energy] », « X = icones de boost ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : cout 2, X = 2 (Shadow of the Past).
- [x] Etape 7 : cas test_capacites : 2 cas VERTS (annulation + X degats ; temoin sans [energy]) ; substitution : rouge 1/2.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : —

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg008 : * The Clocktower

- [x] Etape 2 : cartes de reference : `01026`, `ho006`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « alter-ego action », « using only [mental] », « up to 2 ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : cout 1.
- [x] Etape 7 : cas test_capacites : 3 cas VERTS ; substitution : rouge 2/3.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : —

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg009 : * James Gordon

- [x] Etape 2 : cartes de reference : `ho006`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : deux interruptions « using only [physical/energy] ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : cout 2.
- [x] Etape 7 : cas test_capacites : 2 cas VERTS ; substitution : rouge 2/2.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : —

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg010 : Armored Suit

- [x] Etape 2 : cartes de reference : `01081`, `03005`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « +3 hit points », « prevent 1 ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : cout 2, +3 PV, prevent 1.
- [x] Etape 7 : cas test_capacites : 2 cas VERTS (PV 13 ; 2 degats -> 1 + incline) ; substitution : rouge 2/2.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : —

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg011 : Grapple Line

- [x] Etape 2 : cartes de reference : `53009` Aerial Recon (compteur recon), `06012`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « paid ... using a [physical] resource », « recon counter », « ready a friendly character ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : cout 1.
- [x] Etape 7 : cas test_capacites : 4 cas VERTS (compteur / temoin / Action avec recon / sans) ; substitution : rouge 3/4.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (compteur recon). Cas plateau : `batgirl-plateau.test.ts`.
- Notes : compteur pose APRES l'attachement (perdu sinon) ; paiement lu a la fenetre du JEU (`WhenPlayerPlayCard`) car l'entree en jeu d'une amelioration rend un paiement vide ; cible par fonction (`verifier_cibles` : `Identity|Ally` inconnu du moteur)

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg012 : Utility Belt

**CORRIGÉ le 26/10/2026 (verdict RR « Action » / « Triggered Abilities », `VERDICTS-REGLES-2026-10-26.md`).** Avant : réduction de coût AUTOMATIQUE
(`ReduceCostToPlayFaceWhen`) + inclinaison forcée à chaque événement, dans toutes les formes. Maintenant : une vraie **Hero Action** facultative
(`WhenInYourPlayTurn(HeroAction)` + coût `Exhaust("This")`) qui arme `Worlds.UpdateNextCardPlayCost(joueur, -1, finder=Event, in_this="Turn")` :
l'événement joué ensuite coûte 1 de moins. Le joueur peut refuser (ceinture prête pour le +1 de main) et l'action n'existe qu'en forme héros.
Écart restant, assumé : la capacité imprimée dit « quand vous allez jouer un événement » ; `WhenPlayerWouldPlayCard` part APRÈS le paiement (impossible d'y
réduire le coût), donc l'activation se fait AVANT de jouer l'événement (comme Solid Gear `us009`).

- [x] Étape 2 : cartes de référence : `us009` Solid Gear (`Worlds.UpdateNextCardPlayCost`, coût d'inclinaison), `hz003` / `14022` (Hero Action d'amélioration), `01029a` Iron Man / `04054` (taille de main).
- [x] Étape 5 : texte-contre-code : mots-pièges : « Hero Action » (facultative, forme héros seulement), « reduce the cost of THAT event by 1 » (un seul événement), « exhaust → » (coût), « if this card is ready ». Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 3, −1 coût, +1 main. Résultat : conforme.
- [x] Étape 7 : cas `[bg] bg012` : (1) +1 main prête = 6 cartes ; (2) témoin inclinée = 5 ; (3) Action → Applying Pressure (coût 2) payée par UNE ressource, ceinture inclinée, menace 5 → 1 ; (4) **REFUS** : l'action n'est pas activée, l'événement est payé plein (2 ressources), la ceinture reste PRÊTE ; (5) alter ego : l'action n'est pas offerte, ceinture prête ; (6) témoin sans ceinture (coût plein, non payable avec une ressource).
      Vus ROUGES avant le correctif (cas 3 : « n'offre aucune action », cas 4 : ceinture inclinée alors qu'elle devait rester prête), verts après. Substitution (module vidé) : rouges 2/6 (les quatre autres sont des cas d'absence ou des témoins, verts sans module : assumé).
- [x] Étape 7 bis : limite imprimée ? NON (le coût d'inclinaison borne l'Action à une fois par redressement).
- [x] Étape 8 : autoplay ciblé : voir « Autoplay du 26/10/2026 » en bas de ce fichier.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (une carte s'incline, rien d'attaché ni de compteur).
- Notes : le FAQ de l'insert décrit un autre texte (Drop Kick) : texte IMPRIMÉ suivi.

**Carte terminée : NON (provisoire)** : partie réelle humaine non faite (notamment : l'Action se lit-elle bien dans le menu du plateau avant de jouer l'événement ?).

### bg013 : Recalled Trauma

- [x] Etape 2 : cartes de reference : `us012`, `th011`, `ah001a`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « you may flip », « no resource type », « until the end of the next round ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : boost 2.
- [x] Etape 7 : cas test_capacites : 2 cas VERTS (branche 1 : Barbara s'incline + obligation retiree ; branche 2 : Applying Pressure payee RR n'inflige plus de degats) ; substitution : rouge 2/2.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : True), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : « sans type » ne vaut que pour les cartes DU PACK (drapeau `bg_sans_type` lu par les helpers) ; la convertir en ressource `L` rend les cartes impayables (essaye)

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg014 : Return of the Mask

- [x] Etape 2 : cartes de reference : `uw014` (FindAndReveal), `02042` (TakeIndirectDamage)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Find ... Reveal him », « each player takes 1 indirect damage ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : menace 3, boost 2.
- [x] Etape 7 : cas test_capacites : 1 cas VERT ; substitution : rouge 1/1.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : False), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? peut-etre. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : icone de la manigance (boite) non identifiee : laissee sans Crisis/Acceleration

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg015 : * Black Mask

- [x] Etape 2 : cartes de reference : `27154`, `rz020`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : SCH variable, Incite 1. Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : PV 4, ATQ 2, boost 1.
- [x] Etape 7 : cas test_capacites : 1 cas VERT (SCH = 2 avec deux cartes mental) ; substitution : rouge 1/2.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : False), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (valeur SCH). Cas plateau : `batgirl-plateau.test.ts`.
- Notes : cas SCH 0 (carte rencontre donnee) et SCH 1 (temoin) VERTS

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg016 : * The Reaper

- [x] Etape 2 : cartes de reference : `uw010`, `uw014`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « piercing », « forced response after villain phase ends ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : PV 4, SCH 1, ATQ 2.
- [x] Etape 7 : cas test_capacites : 2 cas VERTS ; substitution : rouge 2/2.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : False), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : —

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg017 : * Mr. Zsasz

- [x] Etape 2 : cartes de reference : bg016
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « overkill », « when the villain phase begins ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : PV 3, SCH 1, ATQ 3.
- [x] Etape 7 : cas test_capacites : 2 cas VERTS ; substitution : rouge 2/2.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : False), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : —

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg018 : Psychological Torture

- [x] Etape 2 : cartes de reference : `02044` Lightning Bolt
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « until you have discarded 3 cards with the same printed resource type ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : boost 2.
- [x] Etape 7 : cas test_capacites : 1 cas VERT ; substitution : rouge 1/1.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : False), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : branche « deck epuise -> le vilain manigance » : cas VERT (le moteur remelange la defausse apres coup : on detecte la DERNIERE carte)

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg019 : Birds of a Feather

- [x] Etape 2 : cartes de reference : `hc022` Divas (Team-Up « any 2 of »)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Team-Up (any combination) », « X = BIRD OF PREY in play ». Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : cout 2, X options, 3 degats.
- [x] Etape 7 : cas test_capacites : 2 cas VERTS (Batgirl + Black Canary -> 2 x 3 degats ; temoin Batgirl seule) ; substitution : rouge 1/2.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : False), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : Huntress n'existe pas dans le jeu : la condition accepte deux des trois noms

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg020 : Energy (reskin Basic)

- [x] Etape 2 : cartes de reference : —
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : RES YY, max 1. Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : —.
- [x] Etape 7 : cas test_capacites : aucun module (ressource Basic) ; substitution : —.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : False), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : reskin d'une carte officielle : carte a part (precedent Hellcat)

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.
- [x] **26/10/2026, arbitrage reskins** (RR « A copy of a card is defined by title » + GUIDE §12 bis) : ces trois ressources ne changent que l'image de `01088` / `01089` / `01090` : ART ALTERNATIF des ressources doubles. Traitement, comme Gwenpool / Beast / Binary : collection `batgirl` dans `COLLECTIONS` (`ui-app/src/board/variantes.ts`) ET dans `COLLECTIONS_RESSOURCES` (`public/js/prepare/app.js`, proposée par défaut au héros « Batgirl » : `collectionDuHeros`). Les cartes restent dans `cards.json` (précédent TMNT / Gwenpool).
      « Max 1 per deck » par TITRE : `validerDeck` (`public/js/deckbuilder/regles.js`, `cleCopie` = titre|sous-titre) compte déjà `01088` + le reskin comme un même titre ; **aucun correctif nécessaire**, preuve : `tools/tests-lanceur/regles-ressources-doubles-par-titre.test.mjs` (4 verts : chaque reskin du dépôt + son officielle = « Trop d’exemplaires de « Energy » : 2/1 », deux mêmes reskins idem, un seul légal, trois titres différents sans gêne). Le moteur n'applique pas MaxPerDeck (seul le constructeur le juge).
      Collection : `ui-app/src/board/resources-art-packs-fanmade-2026-10.test.ts` (45 verts : ordre Energy/Genius/Strength, wizard aligné, images présentes ; ROUGE vu avant le câblage : 18 échecs sur 27, puis rouge à nouveau en retirant l'entrée du wizard).
      Carte terminée : NON (provisoire) : partie réelle humaine (voir la collection « Batgirl » dans la modale du héros et les trois ressources à l'écran).

### bg021 : Genius (reskin Basic)

- [x] Etape 2 : cartes de reference : —
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : RES BB, max 1. Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : —.
- [x] Etape 7 : cas test_capacites : aucun module ; substitution : —.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : False), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : idem

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

### bg022 : Strength (reskin Basic)

- [x] Etape 2 : cartes de reference : —
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : RES RR, max 1. Resultat : lu sur le scan (icones de ressource comparees aux icones du bas de carte du MEME pack).
- [x] Etape 6 : nombres texte <-> code : —.
- [x] Etape 7 : cas test_capacites : aucun module ; substitution : —.
- [ ] Etape 7 bis : limite imprimee ? —.
- [x] Etape 8 : autoplay ciblé : 8 parties Batgirl, 0 exception (la carte apparait dans les journaux : False), temoin She-Hulk : 0 exception.
- [ ] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `batgirl-plateau.test.ts`.
- Notes : idem

**Carte terminee : NON (provisoire)** : partie reelle humaine non faite.

## Autoplay du 26/10/2026 (corrections de verdicts : bg012)

`tools/autoplay.py .game-src-bg --deck batgirl --vilains klaw --profils equilibre --parties 8` : 8 parties, 0 victoire / 8 défaites (4,8 rounds), 0 partie bloquée,
**0 traceback** (grep NameError / AttributeError / TypeError / KeyError / AssertionError sur les 8 journaux). Témoin `she_hulk`, même vilain : 8 parties, 0 victoire,
1 bloquée. ⚠ Le pilote ne prend JAMAIS la nouvelle Hero Action de Utility Belt (il ne s'en sert que comme ressource) : l'autoplay ne prouve donc que l'absence de plantage ;
l'Action n'est prouvée que par les cas `[bg] bg012`. Deck `batgirl` seul (`verifier_tous_les_decks`, DECK_NOM) : OK « identité bg001a, main 6, deck 9 ».
Hors périmètre de ce passage : le wild de bg005 (agent transversal).

## Mesure de l'ordre de bg012 Utility Belt (26/10/2026)

`declencher` tourne AVANT `jouer` dans le banc : les cas existants prouvent « Action de la ceinture, PUIS événement payé 1 ressource ». Cas ajouté `ORDRE` (`declencher_apres`) : l'Action jouée APRÈS l'événement ne le réduit pas (menace 5, événement non joué avec une seule ressource, ceinture inclinée). L'Action « arme » donc le PROCHAIN événement, comme Solid Gear. À regarder en partie réelle : que l'Action se lise bien dans le menu avant de jouer l'événement.

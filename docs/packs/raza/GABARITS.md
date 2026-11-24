# Raza Longknife (Starjammers) : gabarits PROCESSUS-CARTE, 26/10/2026

Pack `raza` (prefixe `rl`, set 226, auteurs Phenexian et Mysteltainn). Scripts : `src/cards/pack/raza/{raza,raza_nemesis}/`.
Cas : `tools/cas/raza.py` (cas `[rl]`) ; plateau : `ui-app/src/board/raza-plateau.test.ts` (3 cas) ; deck `raza` ; recettes `RECETTES-MOTEUR.md` §31.

**Aucune carte n'est « terminee »** : il manque la partie reelle jouee par un humain (voir la fin), et plusieurs cartes portent une question de regle en suspens (choix provisoire code, consigne utilisateur du 25/10/2026 : les questions sont gardees pour la fin).

## Arbitrages du 26/10/2026 (RR 1.8 + scans)
Questions en attente tranchees par le Rules Reference et les scans (`VERDICTS-REGLES-2026-10-26.md`, `docs/rapports/2026-10-26-arbitrages-heros-fanmade.md`). Changent : **rl001a/b** (« unattached »), **rl017** (le premier joueur choisit) ; **rl008** : moteur deja conforme, cas ajoute ; **rl016 New Host** : decision utilisateur du 26/10/2026, le sbire defausse est revele (engage avec le joueur) et New Host s'y attache, deja code. **rl018-rl020** (copies par titre) : traites par l'agent transversal, hors de ce lot.

**Autoplay** (`tools/autoplay.py`, Rhino normal, profil equilibre, 8 parties) : Raza 8 parties TERMINEES (0 victoire, 5 « manigance accomplie », 3 « tous elimines »), 0 exception, 0 blocage, 0 ligne « failed » ; toutes les cartes du pack (rl002 a rl017) apparaissent dans les journaux. Temoin She-Hulk officielle : 8 parties, 7 terminees, 1 bloquee (non liee a Raza), 0 exception. Aucune victoire de Raza : le deck de joueur est vide (pilote seul, comme les autres decks fan-made sans liste). Defaut trouve par l'autoplay puis corrige : Implanted Tools (voir rl006). Pack identique avant et apres substitution (md5 29245384…, puis re-prouve pour rl006 et rl012 apres leur correctif). Verifications finales : 64/64 cas [rl], test_cards 7 648 modules 0 erreur, verifier_tous_les_decks 169/169 (deck raza « identite rl001a, main 6, deck 9 »), verifier_prefixes / verifier_cibles / verifier_appels_modules (calibre : un appel invente est vu) / verifier_desc_mots_cles OK, tests de vocabulaire FR (19) verts.

---

### rl001a : Raza Longknife (face heros)
- [x] Etape 2 : carte(s) de reference : `01029a` Iron Man (`ThisGainKeyword(..., change_on_event=OnEvent.AttachedMove(Upgrade))`) et `12011` Ant-Man (`health=1`).
- [x] Etape 5 : mots-pieges verifies : « unattached » : **ARBITRAGE DU 26/10/2026 (RR Upgrade)** : une amelioration ordinaire entre en jeu PRES de l'identite ; seules celles qui s'attachent (« attach to ») a une AUTRE carte (allie, sbire) sont exclues. Dans le moteur, `bind_face` d'une amelioration ordinaire est l'identite : filtre `PresDeLIdentite` (`raza/__init__.py`) ; « each » compte des CARTES (Blaster TECH ET WEAPON = 1) ; « you control ».
- [x] Etape 6 : nombres texte <-> code : PV 9, ATK 2, THW 2, DEF 2, HS 5 (scan) = `desc` = cas de valeurs imprimees. Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : valeurs imprimees ; 1 arme TECH+WEAPON = +1 ; 3 ameliorations = +3 ; contre-cas CONDITION ; l'amelioration part -> PV redescendent ; NOUVEAU : une amelioration TECH ATTACHEE a un allie (rl011 sur Mockingbird) ne compte pas (10 PV et non 11, vu ROUGE avec l'ancien code). Substitution : rouges 3/6 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau `raza-plateau.test.ts` (3 cas verts ; fixture ecrite sur le modele `attachement-en-chaine`, aucun correctif d'affichage necessaire : pas de « vu rouge »).
Carte terminee : NON (provisoire) : partie reelle humaine ; question de regle TRANCHEE le 26/10/2026 (« unattached » = pas attachee a une autre carte).

### rl001b : Raza Longknife (face alter ego)
- [x] Etape 2 : carte(s) de reference : `rl001a` (meme phrase imprimee sur l'alter ego).
- [x] Etape 5 : mots-pieges verifies : memes mots-pieges que `rl001a` (« unattached » : voir son arbitrage du 26/10/2026).
- [x] Etape 6 : nombres texte <-> code : PV 9, REC 4, HS 6 (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : valeurs imprimees ; le meme calcul de PV en alter ego (Blaster en jeu : 10). Substitution : rouges 1/2 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; « unattached » tranche le 26/10/2026 (voir rl001a).

### rl002 : Tolo Hawk
- [x] Etape 2 : carte(s) de reference : `40024` Deadpool (`WhenUnitWouldBeDefeated(..., by_consequential_damage=True)` + `message.SetBeInstead` + `HealHealth`).
- [x] Etape 5 : mots-pieges verifies : « would be defeated by CONSEQUENTIAL damage » (pas tout degat) ; « instead » (la defaite n'a pas lieu) ; « deal 1 damage to Raza Longknife » (l'identite) ; « remove ALL damage from Tolo Hawk ». Resultat : Interruption (non forcee, comme imprime).
- [x] Etape 6 : nombres texte <-> code : cout 2, PV 2, ATK 1*, THW 1*, ressource [wild] (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : valeurs imprimees ; defait par degats consequents (il avait 1 degat avant d'attaquer Rhino) -> reste en jeu, 0 degat, Raza 1 ; contre-cas : degat direct de 2 -> defait normalement. Substitution : rouges 1/3 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q2 Interruption facultative ou forcee.

### rl003 : Breach Their Defenses!
- [x] Etape 2 : carte(s) de reference : `15004` / evenements d'attaque a decompte ; `rl004` (meme decompte).
- [x] Etape 5 : mots-pieges verifies : « for EACH WEAPON you control » : toute carte controlee portant le trait (allies, ameliorations, soutiens) ; « 1 additional damage ».
- [x] Etape 6 : nombres texte <-> code : cout 2, ressource [physical], trait ATTACK (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : sans arme 3 ; deux armes 5 ; contre-cas TECH sans WEAPON 3 ; valeurs imprimees. Substitution : rouges 3/4 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q3 « each WEAPON / TECH you control » : quelles cartes.

### rl004 : Boarding Action
- [x] Etape 2 : carte(s) de reference : `rl003` (meme decompte, avec TECH et l'effet « contre »).
- [x] Etape 5 : mots-pieges verifies : « each TECH you control » ; « 1 additional threat ».
- [x] Etape 6 : nombres texte <-> code : cout 2, ressource [energy], trait THWART (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : sans TECH 2 ; deux TECH 4 ; contre-cas WEAPON sans TECH 2. Substitution : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q3 « each WEAPON / TECH you control » : quelles cartes.

### rl005 : Warrior Apotheosis
- [x] Etape 2 : carte(s) de reference : `tg003` Great Courage (engager n'importe quel nombre de sbires) ; `ts015` Disarming Assault (le meneur attaque sans boost) ; `ok023` (attaque d'un sbire).
- [x] Etape 5 : mots-pieges verifies : « Engage ANY NUMBER of minions » (choix 0 a n) ; « the villain AND EACH minion engaged with you attacks YOU » ; « do not deal the VILLAIN a boost card » (pas les sbires) ; « damage equal to RAZA'S ATK » (ATK courante, Sabre compris) ; « each enemy that attacked you THIS WAY ».
- [x] Etape 6 : nombres texte <-> code : cout 0, ressource [physical] (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : Rhino attaque sans carte de boost (deck de 01101 : le deck ne diminue pas, 0 degat au lieu de 1) puis 2 degats ; un sbire NON engage s'engage, attaque et subit l'ATK ; le Sabre porte l'ATK a 3 ; valeurs imprimees. Substitution : rouges 3/4 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q4 Apotheosis : ordre des attaques et attaques remplacees.

### rl006 : Implanted Tools
- [x] Etape 2 : carte(s) de reference : `27043` (`CostFunc.Exhaust(trait=..., from_where=["YouControlCards"])`) ; ressource = `CanGenerateResources(Resource, Resources("G"))`.
- [x] Etape 5 : mots-pieges verifies : « Exhaust Implanted Tools AND ANOTHER TECH upgrade you control » : deux incliner, la seconde est une AUTRE amelioration ; « Resource » (pas « Hero Resource »).
- [x] Etape 6 : nombres texte <-> code : cout 1, ressource [mental], traits SKILL TECH (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : paie un Sabre (cout 1) en s'inclinant avec Raza's Cybernetic Eye ; contre-cas : sans autre TECH ; contre-cas : l'autre amelioration n'est pas TECH. DEFAUT TROUVE PAR L'AUTOPLAY ET CORRIGE : avec Implanted Tools SEULE amelioration TECH en jeu, « another TECH » comptait la carte elle-meme (la verification des couts l'acceptait), le paiement echouait (`GameSignal_UndoRequest`) et le pilote rebouclait sur la meme question (graines 7 et 8 bloquees au round 1). Correctif : selecteur du 2e cout exclu de `effect.this` (`Select.From(...).selector_filter.AddParameter(check_effect_fn=...)`). Le banc de cas ne reproduit pas ce chemin (il ne passe pas par le paiement choisi par le pilote) : le temoin de regression est l'autoplay (8 parties terminees apres correctif). Substitution : rouges 1/3 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; aucune question de regle.

### rl007 : Warrior Pride
- [x] Etape 2 : carte(s) de reference : `36012` Flash Freeze (`WhenUnitAttackYou(HeroInterrupt, Villain, op)`).
- [x] Etape 5 : mots-pieges verifies : « When the VILLAIN attacks you » (pas un sbire) ; « draw 1 card » PUIS « if you have sustained 5 or more damage, heal 1 » ; « from your identity ».
- [x] Etape 6 : nombres texte <-> code : cout 3, ressource [mental], trait CONDITION (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : pioche 1 sous 5 degats (le heros defend : degats inchanges) ; a 5 degats pioche ET soigne 1 (5 -> 4) ; contre-cas : un sbire qui attaque ne la declenche pas. Substitution : rouges 2/3 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q5 Warrior Pride : ordre pioche / soin.

### rl008 : Raza's Cybernetic Arm
- [x] Etape 2 : carte(s) de reference : `hz004` Hepzibah's Spacesuit (`control_additional_restricted=CardFinder(card_type=Upgrade)`) ; `brawn/bw016` (retaliate conditionnelle, `get_new_value` + `ex_change_on_event`).
- [x] Etape 5 : mots-pieges verifies : « 1 ADDITIONAL upgrade that has the restricted keyword » ; « WHILE your identity has sustained 5 or more damage, you gain Retaliate 1 » (se recalcule quand les degats changent) ; la parenthese « (Retaliate will trigger for attacks that cause Raza to gain Retaliate) » n'est PAS ambigue (arbitrage du 26/10/2026, RR 1.8 : Retaliate est une Reponse forcee APRES l'attaque) : une attaque qui fait passer Raza a 5 degats ou plus declenche la riposte.
- [x] Etape 6 : nombres texte <-> code : cout 1, ressource [energy], traits TECH WEAPON (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : avec le Bras, une 3e Restricted (Bouclier 03009) reste en jeu avec les deux autres ; contre-cas : sans le Bras la 3e force a defausser (2 restent) ; a 5 degats Rhino subit la riposte (1) ; contre-cas : a 4 degats rien (Raza DEFEND : degats reduits a 0, il ne teste pas la parenthese) ; NOUVEAU : Raza a 4 degats et EPUISE, l'attaque non defendue de Rhino le porte a 6 -> riposte 1 (le moteur etait DEJA conforme, le cas manquait) ; temoin 2 + 2 = 4, aucune riposte ; valeurs imprimees. Substitution : rouges 3/7 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; question tranchee le 26/10/2026 (la parenthese signifie bien que l'attaque qui fait gagner Retaliate declenche la riposte ; moteur deja conforme, cas ajoute).

### rl009 : Raza's Cybernetic Eye
- [x] Etape 2 : carte(s) de reference : `cr008` Riposte (`AfterUnitAttackYou(HeroResponse, ...)`).
- [x] Etape 5 : mots-pieges verifies : « After the VILLAIN attacks you » (pas un sbire) ; « 1 threat (2 threat if you have sustained 5 or more damage) » : seuil lu a la resolution.
- [x] Etape 6 : nombres texte <-> code : cout 1, ressource [mental], trait TECH (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : 1 menace sous 5 degats ; 2 a 5 degats ; contre-cas : l'attaque d'un sbire. Substitution : rouges 2/3 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; aucune question de regle.

### rl010 : Raza's Blaster
- [x] Etape 2 : carte(s) de reference : `pulse blaster` / actions d'amelioration inclinant `CostFunc.Exhaust("This")` (`cr004`).
- [x] Etape 5 : mots-pieges verifies : « Restricted » (limite par le moteur) ; « exhaust Raza's Blaster -> deal 1 damage (or 2 if you have sustained 5 or more damage) ».
- [x] Etape 6 : nombres texte <-> code : cout 2, ressource [energy], Restricted, traits TECH WEAPON (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : 1 degat ; 2 a 5 degats ; valeurs imprimees. Substitution : rouges 2/3 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; aucune question de regle.

### rl011 : Raza's Sabre
- [x] Etape 2 : carte(s) de reference : `brawn/bw016` (`GiveKeywordToAttached("You", get_new_value=..., attack=1, ex_change_on_event=OnEvent.Health(...))`).
- [x] Etape 5 : mots-pieges verifies : « Raza gets +1 ATK (+2 ATK INSTEAD if you have sustained 5 or more damage) » : +2 au lieu de +1, pas +3 ; « Restricted ».
- [x] Etape 6 : nombres texte <-> code : cout 1, ressource [physical], Restricted, trait WEAPON (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : +1 ATK sous 5 degats ; +2 a 5 degats ; le bonus suit les degats (soin de 5 -> retour a +1). Substitution : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; aucune question de regle.

### rl012 : Honour-Bound Warrior
- [x] Etape 2 : carte(s) de reference : `vision/26028` Corrupted Programming (`GiveKeywordToInPlayWhenApplyThis(..., treat_as_blank=True)` + Alter-Ego Action qui se retire).
- [x] Etape 5 : mots-pieges verifies : « textbox on each of YOUR upgrades as blank (except for TRAITS) » : les traits comptent encore ; « Alter-Ego Action: exhaust Raza Longknife -> remove this card from the game ».
- [x] Etape 6 : nombres texte <-> code : Boost 2 (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : le Sabre ne donne plus +1 ATK ; les traits restent (PV 10 avec le Blaster) ; Alter-Ego Action : l'alter ego s'incline et l'obligation quitte la partie ; contre-cas : l'obligation partie, le Sabre redonne +1. Substitution : rouges 2/4 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q7 Honour-Bound Warrior : portee multijoueur.

### rl013 : Zzzxx
- [x] Etape 2 : carte(s) de reference : `rz020` / `16119` Badoon Lieutenant (`WhenCardBecomeBoost` + `message.GainBoostIcon`) ; Villainous = fiche `villainous.md`.
- [x] Etape 5 : mots-pieges verifies : « activates AGAINST A CHARACTER who has sustained 5 or more damage » (une attaque, pas une manigance) ; « gains Villainous FOR THAT ACTIVATION » = une carte de boost de plus pour cette attaque ; « Boost: boost icons EQUAL TO THE VILLAIN'S STAGE NUMBER » (Boost imprime 0).
- [x] Etape 6 : nombres texte <-> code : PV 5, ATQ 2, SCH 1, ELITE SYMBIOTE, Boost 0 + ★ (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : valeurs imprimees ; attaque contre 5 degats : une carte de boost donnee (deck 8 -> 7) ; contre-cas a 4 degats (8) ; Boost : stade 1 -> +1 icone (Rhino 3 contre DEF 2 = 1 degat). Substitution : rouges 2/4 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q8 Zzzxx : Vilenie pour l'activation et icones de boost.

### rl014 : Symbiote Possession
- [x] Etape 2 : carte(s) de reference : `60060` Raised by the Kingpin (find et mise en jeu engagee) ; `03028` Baron Zemo (`UnitCannotThwartTarget`) ; `cr015` (`UnitCannotBeAttacked`).
- [x] Etape 5 : mots-pieges verifies : « Players ENGAGED WITH Zzzxx » (conditions sur l'engagement) ; « cannot attack Zzzxx » ; « cannot thwart schemes OTHER THAN THIS ONE » ; « Find Zzzxx and put him into play engaged with YOU » (deja en jeu : il t'engage). ⚠ `can_only_thwart="This"` est LOCAL : ne marche pas (RECETTES §31).
- [x] Etape 6 : nombres texte <-> code : menace 2 par joueur, 1 icone Acceleration (meme icone que Slave Pits of Chandilar, `cr014`), 1 icone de boost (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : revelee : Zzzxx en jeu, engage, menace 2 ; le heros engage ne peut pas attaquer Zzzxx ; ne peut pas contrer le complot principal ; PEUT contrer cette manigance (menace 2 -> 0, elle est defaite). Substitution : rouges 3/4 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q9 Symbiote Possession : portee de l'interdiction.

### rl015 : Shi'ar Host
- [x] Etape 2 : carte(s) de reference : `45124` Cruel Experiment / `Worlds.GetEncounterDiscardPileCards` ; surge : `ThisCardGainSurge`.
- [x] Etape 5 : mots-pieges verifies : « Search the DISCARD pile » (la defausse rencontre seulement) ; « an attachment that CAN BE ATTACHED to Shi'Ar Host » (lecture du texte « Attach to a minion / the minion / a character ») ; « If no attachment was revealed this way, this card gains surge ».
- [x] Etape 6 : nombres texte <-> code : PV 3, ATQ 1, SCH 1, Boost 2, SHI'AR (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : valeurs imprimees ; revelee avec Genetically Enhanced en defausse -> attache a lui ; sans attachement -> surge (la carte suivante du deck est revelee). Substitution : rouges 2/3 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attache une carte a un sbire / pose un compteur. Cas plateau `raza-plateau.test.ts` (3 cas verts ; fixture ecrite sur le modele `attachement-en-chaine`, aucun correctif d'affichage necessaire : pas de « vu rouge »).
Carte terminee : NON (provisoire) : partie reelle humaine ; Q10 Shi'ar Host : quel attachement convient.

### rl016 : New Host
- [x] Etape 2 : carte(s) de reference : `45124` Cruel Experiment (`Worlds.DiscardEncounterCardsUntil`, `AttachTo2`) ; `uw011` (`WhenUnitBeDefeated(..., "AttachedMinion", ...)`).
- [x] Etape 5 : mots-pieges verifies : « Discard cards UNTIL you discard a minion. ATTACH New Host to it » (sbire defausse : revele puis attache) ; « Forced Response: WHEN attached minion IS DEFEATED » : `AfterUnitBeDefeated` ne part jamais pour un attachement (RECETTES §31) ; « search the encounter deck AND discard pile for Zzzxx » ; « +1 ATK » imprime = cle `ATK+` du `desc`.
- [x] Etape 6 : nombres texte <-> code : Boost 2, +1 ATK, CONDITION SYMBIOTE (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : revelee : s'attache au sbire (ATQ 1 -> 2) ; sbire vaincu -> Zzzxx en jeu, engage ; contre-cas : sans sbire, la carte est defaussee. Substitution : rouges 2/3 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attache une carte a un sbire / pose un compteur. Cas plateau `raza-plateau.test.ts` (3 cas verts ; fixture ecrite sur le modele `attachement-en-chaine`, aucun correctif d'affichage necessaire : pas de « vu rouge »).
Carte terminee : NON (provisoire) : partie reelle humaine ; Q11 New Host : le sbire defausse.

### rl017 : Devour
- [x] Etape 2 : carte(s) de reference : `06003` / `45124` (defausser jusqu'a un sbire) ; `an013` Hel-Wolf (boost qui donne Deferlement : `message.would_atk_message.GainOverKill`).
- [x] Etape 5 : mots-pieges verifies : « Discard AN ALLY you control. IF YOU CANNOT, discard cards ... until you discard a minion AND PUT IT INTO PLAY engaged with you » ; « Boost: IF THIS ACTIVATION IS AN ATTACK, this attack gains overkill ».
- [x] Etape 6 : nombres texte <-> code : Boost 2 + ★, SYMBIOTE (scan). Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite : allie defausse (Mockingbird) ; sans allie : le sbire du deck est mis en jeu engage ; Boost : Rhino 2 + 2 icones attaque Black Cat (2 PV) : 2 degats d'exces au heros ; TEMOIN : meme montage avec New Host (sans overkill) : 0 ; valeurs imprimees ; NOUVEAU : a deux joueurs, Devour revelee par le joueur 2 qui controle deux allies : c'est le PREMIER joueur qui est interroge (RR First Player, vu ROUGE avec l'ancien code : joueur 1 interroge). Substitution : rouges 4/6 (les verts : valeurs imprimees, contre-cas d'absence ou temoins, assumes).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (8 parties, temoin `she_hulk`).
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
Carte terminee : NON (provisoire) : partie reelle humaine ; question tranchee le 26/10/2026 (RR First Player : plusieurs allies admissibles pour une carte de rencontre -> le premier joueur choisit ; en solo c'est le meme joueur). `rl017.py` : `world.GetFirstPlayer()`.

### rl018, rl019, rl020 : Energy, Genius, Strength (reskins de ressources)
- Aucun module (ressources Basic, `desc.RES`), valeurs lues sur le scan : YY, BB, RR, 1 max par deck. Question Q13.
Carte terminee : NON (provisoire) : partie reelle humaine ; Q13.
- [x] **26/10/2026, arbitrage reskins** (RR « A copy of a card is defined by title » + GUIDE §12 bis) : ces trois ressources ne changent que l'image de `01088` / `01089` / `01090` : ART ALTERNATIF des ressources doubles. Traitement, comme Gwenpool / Beast / Binary : collection `raza` dans `COLLECTIONS` (`ui-app/src/board/variantes.ts`) ET dans `COLLECTIONS_RESSOURCES` (`public/js/prepare/app.js`, proposée par défaut au héros « Raza Longknife » : `collectionDuHeros`). Les cartes restent dans `cards.json` (précédent TMNT / Gwenpool).
      « Max 1 per deck » par TITRE : `validerDeck` (`public/js/deckbuilder/regles.js`, `cleCopie` = titre|sous-titre) compte déjà `01088` + le reskin comme un même titre ; **aucun correctif nécessaire**, preuve : `tools/tests-lanceur/regles-ressources-doubles-par-titre.test.mjs` (4 verts : chaque reskin du dépôt + son officielle = « Trop d’exemplaires de « Energy » : 2/1 », deux mêmes reskins idem, un seul légal, trois titres différents sans gêne). Le moteur n'applique pas MaxPerDeck (seul le constructeur le juge).
      Collection : `ui-app/src/board/resources-art-packs-fanmade-2026-10.test.ts` (45 verts : ordre Energy/Genius/Strength, wizard aligné, images présentes ; ROUGE vu avant le câblage : 18 échecs sur 27, puis rouge à nouveau en retirant l'entrée du wizard).
      Carte terminée : NON (provisoire) : partie réelle humaine (voir la collection « Raza Longknife » dans la modale du héros et les trois ressources à l'écran).

---

## Questions de regle en attente (une par carte, option recommandee en premier = celle codee)

**Q1** : Alien Augmentations, « unattached » : le texte imprime dit « unattached TECH or WEAPON upgrade » alors qu'une amelioration en jeu est toujours attachee a une carte.
- A (code) : compter toute amelioration TECH ou WEAPON que vous controlez
- B : ne compter que les ameliorations attachees a Raza lui-meme (pas celles attachees a un allie ou autre)
- C : compter litteralement celles qui ne sont attachees a RIEN (aucune amelioration ordinaire : le bonus serait toujours nul)

**Q2** : Tolo Hawk : l'Interruption est « Interrupt » (non forcee).
- A (code) : facultative, le joueur peut la refuser (Tolo Hawk est alors vaincu)
- B : forcee

**Q3** : Breach Their Defenses! / Boarding Action : « for each WEAPON / TECH you control ».
- A (code) : toute carte que vous controlez portant le trait (allies, ameliorations, soutiens, identite)
- B : seulement les ameliorations

**Q4** : Warrior Apotheosis : ordre des attaques et attaques remplacees.
- A (code) : le vilain attaque d'abord, puis chaque sbire engage ; seuls les ennemis dont l'attaque a REELLEMENT eu lieu subissent les degats (un sbire sonne n'attaque pas, donc n'en subit pas)
- B : tous les ennemis qui devaient attaquer subissent les degats, meme si leur attaque a ete remplacee

**Q5** : Warrior Pride : ordre de resolution.
- A (code) : piocher 1 carte, PUIS verifier les 5 degats et soigner
- B : verifier les 5 degats avant de piocher

**Q6** : Raza's Cybernetic Arm : la parenthese « (Retaliate will trigger for attacks that cause Raza to gain Retaliate) » est ambigue.
- A (code) : Retaliate 1 ordinaire a 5 degats ou plus (riposte a toute attaque contre Raza)
- B : a demander a l'auteur (lecture de la parenthese)

**Q7** : Honour-Bound Warrior : portee du texte vide.
- A (code) : seules les ameliorations du joueur qui detient l'obligation (`control_by="You"`), celles de Raza comprises
- B : toutes les ameliorations en jeu, tous joueurs confondus

**Q8** : Zzzxx : « gains Villainous for that activation » et icones de boost.
- A (code) : Vilenie = UNE carte de boost de plus pour cette attaque ; en carte de boost, +autant d'icones que le numero de stade du vilain
- B : meme Vilenie, mais icones de boost fixes a l'imprime (pas de calcul de stade)

**Q9** : Symbiote Possession : « Players engaged with Zzzxx cannot attack Zzzxx or thwart schemes other than this one ».
- A (code) : s'applique aux heros ET aux allies des joueurs engages avec Zzzxx ; Zzzxx hors jeu : plus aucune interdiction
- B : seulement aux heros

**Q10** : Shi'ar Host : « an attachment that can be attached to Shi'Ar Host » (la defausse rencontre).
- A (code) : tout attachement dont le texte commence par « Attach to a minion / the minion / a character / an enemy »
- B : seulement ceux imprimes « Attach to a minion »
- C : tout attachement de la defausse

**Q11** : New Host : « Discard cards ... until you discard a minion. Attach New Host to it. » (le sbire est dans la defausse).
- A (code) : le sbire defausse est REVELE (mis en jeu, engage) puis New Host s'y attache (comme Cruel Experiment)
- B : New Host s'attache au sbire reste dans la defausse (aucun effet en jeu)

**Q12** : Devour : « Discard an ally you control ».
- A (code) : le joueur choisit l'allie a defausser s'il en a plusieurs
- B : le moteur choisit (premier allie)

**Q13** : Reskins de ressources (rl018-rl020, « Alt Art Energy / Genius / Strength » du zip).
- A (code) : cartes a part, 1 max par deck (precedent Hellcat / Corsair)
- B : arts alternatifs des ressources officielles

## A verifier en partie reelle
- Une partie complete avec Raza choisi dans la liste Fan-made.
- Alien Augmentations (PV de Raza) quand on joue / defausse des ameliorations a l'ecran.
- Le choix des sbires a engager de Warrior Apotheosis dans l'interface (liste de cases a cocher).
- Le jeu de Symbiote Possession : interdiction d'attaquer Zzzxx / de contrer d'autres manigances, a l'ecran.
- La biographie de Raza au survol du heros dans l'assistant (le module se charge et la cle est la bonne, la fiche n'a pas ete vue dans un navigateur).
- Les icones de ressource ont ete lues a l'oeil sur les scans et comparees a des cartes du meme pack (Corsair) ; pas de decoupe pixel par pixel.
- Le Boost de Shi'ar Host / New Host sans cas de test propre.

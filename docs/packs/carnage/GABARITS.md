# Carnage (Eddie Brock) : gabarits PROCESSUS-CARTE, 03/11/2026

Pack `carnage_eddie_brock` (prefixe `ca`, set 249, auteur Neptune). Scripts : `src/cards/pack/carnage_eddie_brock/{carnage,carnage_nemesis,twisted_killers}/`. Cas : `tools/cas/carnage.py` (111). Decks : `deck/starter/carnage_eddie_brock.json` (decklist Aggression de l'auteur) et `carnage_eddie_brock_protection.json`. Textes FR : `ui-app/src/board/textes-fr-fanmade.ts` (+ copie generee `public/js/traduction/textes-fr-fanmade.js`). Biographie : `heros-info.js` (`ca001a`). Ecran : `ui-check/tests/carnage-ecrans.spec.ts` (captures `captures/carnage`, `captures/carnage-en`).

## Source et decisions

- Matiere : carnage.zip (PNG 1500x2150 ; **les PNG priment sur le PDF d'impression**, plus ancien : textes nemesis anciens). Scans EN seuls, aucun scan FR : textes FR ecrits a la main (noms de cartes et de capacites laisses en anglais, precedent `bt`).
- Pacifying Presence (n°6 de la liste imprimee) : carte OUBLIEE par l'auteur, ligne laissee vide dans les decklists (decision utilisateur du 03/11).
- Decisions utilisateur du 03/11 : ca005 « heal 1 damage » = CARNAGE seulement ; ca009 = ressource WILD reservee a un evenement Carnage ; ca014 « your ATK » = ATK COURANTE de l'identite (0 en alter ego) ; ca021 et boost de ca023 : exces de degats d'un sbire KILLER = CONVERTI en menace (lecture B, en remplacement) ; ca018 : l'identite compte comme classification identity-specific ; ca019 : « the character » = personnage ami ; PV de ca002 = 4 (scan).
- ★ devant une capacite = `NonKeywordStar` / ★ devant « Boost » = `AbilityType.Boost` (fiche `special.md`, `boost.md`) ; ★ devant une Interruption forcee = l'Interruption forcee elle-meme.
- **Defauts trouves par les portes finales** : `factory.py` (liste blanche des evenements a deux capacites de jeu : ca011) ; ca002 (`by_effect` sans `ability` : AttributeError avale) ; ca022 (overkill perdu apres `ChangeTarget` : engine) ; temporaire de boost de ca023 (pose sur la carte de boost, pas sur l'ennemi).
- Limites du harnais/moteur (ecrites dans les scripts) : ca022 ne redirige pas vers un AUTRE ennemi ; `ranged` d'un evenement non observable (ca011) ; plafond RRR de ca013 non prouve ; branche 2 de ca014 en forme heros inatteignable par le pilote ; ca017 : meme texte d'Interruption que Torment (preuve par attache, surge et Action).

### ca001a : Carnage

- [x] Etape 2 : carte(s) de reference : - Death-Dealer : `ar005` (Ares' Battle Helm) : `AfterUnitDefeatedUnit(.., "You", Enemy, op, is_from_attack=True, has_excess_damage=True)` + `message.excess_damage` ; soin : `HealthUnits([cible], n, effect)` (`my001b`). - Need to Kill : `61040` (pack jj) `AfterRoundEnd(ForcedResponse)` pour « at the end of the round » ; `jj` `RecordSideSchemeDefeat` pour le marqueur « ce round » ; `rz016` (Weighed Down) `this.DealDamage([joueur.GetIdentity()], n, effect)` pour « take N damage ».
- [x] Etape 5 : texte-contre-code : « After YOU attack AND defeat an enemy » : `"You"` + `is_from_attack=True` (une defaite par un allie ou par un effet sans attaque ne declenche pas). « an ENEMY » : le vilain compte. « for each point of EXCESS damage » : `message.excess_damage` (avec `has_excess_damage=True` la Reponse n'est meme pas proposee quand l'exces vaut 0). « heal ... FROM CARNAGE » : l'identite. « if YOU did not defeat an enemy THIS ROUND » : tout ennemi vaincu par le joueur (attaque ou effet) ce round annule la Reponse forcee. « damage equal to YOUR ATK » : l'ATK COURANTE de l'identite (+1 de Frenzied Violence compris), lue au moment de la resolution. Chiffres : PV 12, main 5, ATQ 2, CTR 1, DEF 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (6) : Carnage abat Hydra Mercenary avec 1 degat d'exces : il soigne 1 degat (4 -> 3) ; TEMOIN : le sbire est abattu EXACTEMENT (0 exces) : aucun soin (4 degats restent) ; TEMOIN : le sbire survit (pas de defaite) : aucun soin (4 degats restent) ; fin de round SANS ennemi vaincu : Carnage subit des degats egaux a son ATQ (2) ; TEMOIN : un ennemi a ete vaincu ce round : aucun degat ; TEMOIN : en forme ALTER-EGO la Reponse forcee de la face heros n'existe pas (0 degat). Preuve par substitution : rouges 2/6 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca001b : Eddie Brock

- [x] Etape 2 : carte(s) de reference : - `01116b` Underground Distribution : `Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)` + `face.PutIntoPlay(joueur, effect)` (mise en jeu, SANS When Revealed). - `mystique/my001b` : `WhenInYourPlayTurn(AbilityType.Action, op).SetName(..).LimitOncePerRound()` pour une « Action » imprimee sur l'identite.
- [x] Etape 5 : texte-contre-code : « Action » : jouable uniquement en forme alter-ego (face visible). « discard ... UNTIL you discard a minion » : `DiscardEncounterCardsUntil` (remelange la defausse si le deck s'epuise, regle native). « engaged WITH YOU » : mis en jeu pour CE joueur. « Limit once per round » : `LimitOncePerRound`. Chiffres : PV 12, main 6, REC 4.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (3) : Action : on defausse jusqu'au premier sbire (Hydra Mercenary) ; il entre en jeu ENGAGE avec le joueur, le complot annexe saute est defausse ; LIMITE une fois par round : la 2e Action est refusee, le second sbire reste dans le deck ; TEMOIN : en forme HEROS la capacite de l'alter-ego n'existe pas (aucun sbire n'entre en jeu). Preuve par substitution : rouges 2/3 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? OUI : Dark Urges, une fois par round ; temoin d'epuisement : cas LIMITE (2e sbire reste dans le deck).
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca002 : Spider-Man

- [x] Etape 2 : carte(s) de reference : - « When X would take damage -> prevent all » : `im012` (Hulkbuster) : `WhenUnitWouldTakeDamage(Interrupt, "You", op)` + `message.PreventDamage("All", effect)`. - Declencheur lie a UNE capacite nommee : `ma002` / `mt001a` : `effect.ability.name` compare a la chaine posee par `.SetName()` (ici « Need to Kill », ca001a), lue sur `message.by_effect`. - « exhaust X and deal 1 damage to him → » : les deux dans le COUT : `22012` (`CostFunc.DealDamage(1, "This")`) + `CostFunc.Exhaust("This")`.
- [x] Etape 5 : texte-contre-code : « Interrupt » NU : jouable dans les deux formes. « When YOU would take any amount of damage FROM RESOLVING Need to Kill » : seuls les degats de CETTE capacite (nom lu sur l'effet source), jamais une attaque ou un autre effet ; « you » = l'identite du joueur. « exhaust Spider-Man AND deal 1 damage to him → » : deux couts ; ni l'un ni l'autre possible (deja epuise) = pas d'Interruption. « prevent ALL of that damage » : `PreventDamage("All")`. Chiffres : cout 4, PV 4, un degat paye par Spider-Man. ⚠ A RELIRE SUR LE SCAN : les notes de lecture marquent le PV de Spider-Man « non imprime lisible » ; `data/cards.json` porte 4.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (4) : TEMOIN (autoplay) : les degats d'une ATTAQUE (source = regle de jeu, sans `ability`) ne plantent pas la condition et ne sont pas previenus ; l'Interruption previent les degats de Need to Kill : Carnage ne subit rien, Spider-Man s'incline et prend 1 degat ; TEMOIN : Spider-Man deja epuise (cout impayable) : Need to Kill frappe Carnage (2 degats), Spider-Man intact ; TEMOIN : des degats d'une AUTRE source (1 degat pose par le harnais sur Carnage) ne sont pas previenus : Spider-Man reste pret. Preuve par substitution : rouges 1/4 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca003 : Symbiote Hive-Mind

- [x] Etape 2 : carte(s) de reference : - +1 REC en continu : `ho005` (Gwen Stacy Osborn, « Harry Osborn gets +1 REC ») : `GiveKeywordToInPlayWhenApplyThis(.., control_by="You", recover=1)` (un SOUTIEN, pas un attachement) ; mais le TYPE vise ICI `AlterEgo` et non `Identity` : « Eddie Brock » est un NOM PROPRE, il ne designe que la face alter-ego (RECETTES §3, lecon an002 Sera ; contre-cas en forme heros). - Action alter-ego qui remelange une carte du set depuis la defausse : `bw012` (Cho's Lab, « shuffle a Brawn card from your discard pile into your deck ») : `CardFinder(set_name=..).Checks(joueur.discard_pile.Get())` + `AskChooseFace(.., not_move=True)` + `Faces.ShuffleAllTo`.
- [x] Etape 5 : texte-contre-code : « EDDIE BROCK gets +1 REC » : nom propre = la face alter-ego du joueur qui controle la carte, jamais la face heros (Carnage). « Alter-Ego Action » : `AlterEgoAction` (jouable en forme alter-ego seulement). « Exhaust this card → » : l'epuisement est le COUT (`CostFunc.Exhaust("This")`). « 1 Carnage card » : une carte du SET « Carnage » (ca002-ca013), PAS du set nemesis ; UNE carte, choisie par le joueur. « from YOUR discard pile into YOUR deck » : defausse et deck du joueur, deck remelange (`ShuffleAllTo`). Chiffres : cout 1, +1 REC, 1 carte.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (5) : Eddie Brock (alter-ego) gagne +1 REC en continu ; TEMOIN DE BASE : sans la carte en jeu, la REC d'Eddie Brock reste a sa valeur imprimee (le +1 vient bien d'elle) ; Alter-Ego Action : une carte du set Carnage (ca004) remonte de la defausse dans le deck, la carte etrangere (Energy) y reste ; ca003 s'incline ; TEMOIN : la defausse ne contient qu'une carte ETRANGERE au set : rien ne remonte (deck vide, defausse intacte) ; TEMOIN : en forme HEROS l'Action d'alter-ego n'existe pas (rien ne remonte). Preuve par substitution : rouges 3/5 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca004 : Lethal Restraint

- [x] Etape 2 : carte(s) de reference : - « NOM gains retaliate 1 » : `nt011` (Prewind Stance) : `GiveKeywordToInPlayWhenApplyThis(CardFinder(name=..), control_by="You", retaliate=1)` + `CanPlayThisUpgradeCard()`. Riposte est une BASE du moteur (fiche mots-cles/retaliate.md) : on la DONNE, on ne la recode pas. - « reduce the cost of the next <X> card you play this phase by N » : `us009` (Solid Gear) : `Worlds.UpdateNextCardPlayCost(joueur, -N, effect, finder=.., in_this="Phase")`. - « Return this card to your hand → » en COUT : `47028` (Jubilee) : `CostFunc.ReturnToHand(.., to_who="Owner")`.
- [x] Etape 5 : texte-contre-code : « CARNAGE gains retaliate 1 » : nom propre = la face heros, jamais l'alter-ego. « Hero Action » : `HeroAction` (forme heros seulement). « Return this card to your hand → » : le retour en main est le COUT. « the NEXT Carnage EVENT » : UNE seule carte, de TYPE evenement et du set « Carnage » (ca010-ca013), jamais une amelioration ni une carte d'un autre set. « THIS PHASE » : `in_this="Phase"`. « by 1 » : valeur negative (-1), la fabrique ne descend pas sous 0. Chiffres : cout 1, retaliate 1, -1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (5) : Carnage (forme heros) gagne retaliate 1 ; TEMOIN DE BASE : sans la carte, Carnage n'a pas de retaliate ; Hero Action : la carte revient en MAIN (cout) et sort du jeu ; la Hero Action reduit de 1 la prochaine Carnage EVENT : ca010 (cout 1) se joue SANS depenser ca004 (restee en main) ; TEMOIN : SANS l'Action, ca010 est payee avec ca004 (defaussee de la main) : la reduction vient bien de la carte. Preuve par substitution : rouges 3/6 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca005 : Probing Minds

- [x] Etape 2 : carte(s) de reference : - « When you reveal a non-ELITE minion » : `50101` (Batroc's Brigade) : `WhenPlayerRevealCard(HeroInterrupt, "You", NonEliteMinion, "All", op)` (CardFinder.NonEliteMinion du pack commun). - Statuts : `nt004` / `01083` : `Faces.GiveStatus(cibles, "Confused"|"Stunned", effect)` ; soin `my001b` : `HealthUnits([cible], n, effect)` ; retrait de menace d'un complot CHOISI : `RemoveThreatFromSchemes`.
- [x] Etape 5 : texte-contre-code : « Hero Interrupt: When YOU reveal a NON-ELITE MINION » : revelation par le joueur (jamais une mise en jeu directe comme Dark Urges), type sbire, trait ELITE exclu. « exhaust this card → » : COUT. « boost icons equal to » : ICONES DE BOOST IMPRIMEES du sbire (`printed_boost` ; 0 si aucune) : 0 = soin, 1 = confus, 2 = etourdi, 3 ou plus = menace. Les quatre cas sont EXCLUSIFS. « heal 1 damage » : DECISION UTILISATEUR du 03/11 (lecture A) : soigne CARNAGE (l'identite du joueur, forme heros puisque Hero Interrupt), sans choix de cible. « remove 1 threat FROM A SCHEME » : un complot au choix, principal ou annexe. Chiffres : cout 1, 1 soin / 1 menace.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (5) : sbire a 0 icone de boost (Weapons Runner 01121) revele : Carnage (4 degats avant) se soigne de 1 ; ca005 s'incline ; sbire a 1 icone (Hydra Mercenary 01101) : le sbire est CONFUS ; sbire a 2 icones (Shocker 01103) : le sbire est ETOURDI ; sbire a 3 icones (Tyrannosaurus Rex 11032) : 1 menace retiree du complot principal (5 -> 4) ; TEMOIN : un sbire ELITE (Sandman 01102, 2 icones) revele : aucun effet, ca005 reste prete. Preuve par substitution : rouges 4/5 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca006 : Frenzied Violence

- [x] Etape 2 : carte(s) de reference : - « NOM gets +1 ATK and his basic attacks gain overkill » : `im012` (Hulkbuster Armor) : `GiveKeywordToAttached(Hero, attack=1)` + `UnitAttackGainKeyword("You", overkill=True, is_basic_attack=True)` (fiche mots-cles/overkill.md). - « After you attack and defeat an enemy » : `an004` (Murderous Glare) / ar005 : `AfterUnitDefeatedUnit(HeroResponse, "You", Enemy, op, is_from_attack=True)` ; « ready Carnage » : `Faces.ReadyAll` (`an001a`).
- [x] Etape 5 : texte-contre-code : « CARNAGE gets +1 ATK » : nom propre, face heros (`Hero`). « his BASIC attacks gain overkill » : `is_basic_attack=True` (Chomp, Vicious Lashing et Rend n'en profitent pas par cette ligne). « Hero Response: After YOU attack AND defeat AN enemy » : `HeroResponse` + `"You"` + `Enemy` (vilain compris) + `is_from_attack=True`. « exhaust this card → » : COUT (`CostFunc.Exhaust("This")`). « ready CARNAGE » : l'identite, pas la carte. Chiffres : cout 2, +1 ATK.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (5) : Carnage gagne +1 ATK ; TEMOIN DE BASE : sans la carte, ATK = valeur imprimee ; l'attaque de BASE a OVERKILL : 2 degats d'exces d'un sbire a 1 PV restant (ATK 3) passent au vilain ; Hero Response : apres avoir abattu un ennemi, la carte s'incline et Carnage est REDRESSE ; TEMOIN : l'ennemi SURVIT : pas de Reponse, Carnage reste epuise, ca006 reste prete. Preuve par substitution : rouges 3/5 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca007 : Hunting Hosts

- [x] Etape 2 : carte(s) de reference : - « After you attack and defeat a MINION » : `an001a` (Frenzy) : `AfterUnitDefeatedUnit(Response, "You", Minion, op)` + `LimitOncePerRound` (absente ici) ; `is_from_attack=True` pour « attack AND defeat » (`an004`). Condition ELITE : `message.target.HasTrait("ELITE")` (`ua003`). - « search the encounter deck and discard pile for a minion and put it into play engaged with you » : `ar014` (Lead the Charge) : `Search.EncounterCard(effect, joueur, include_discard_pile=True, card_type=Minion)` + `PutIntoPlay(joueur, ..)` ; mise en jeu engagee : `ca001b` (Dark Urges, meme carte modele 01116b).
- [x] Etape 5 : texte-contre-code : « Response » NU (pas Hero Response) : jouable dans les deux formes. « After YOU attack AND defeat an ELITE MINION » : `"You"` + `is_from_attack=True` + type `Minion` (le vilain ne compte pas) + condition ELITE. « ready THIS card » : l'amelioration, pas Carnage. « Exhaust this card → » : COUT. « encounter deck AND discard pile » : `include_discard_pile=True`. « a minion » : un seul, au choix du joueur. « engaged WITH YOU » : mis en jeu pour ce joueur. « (Shuffle.) » : le deck de rencontre est remelange par la recherche (comportement par defaut). Chiffres : cout 2, un sbire.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (5) : Action : cherche un sbire DANS LE DECK de rencontre (Hydra Mercenary) : il entre en jeu ENGAGE avec le joueur ; Action : cherche aussi DANS LA DEFAUSSE de rencontre (deck sans sbire, Sandman en defausse) ; ca007 s'incline (cout) ; TEMOIN : ni sbire dans le deck ni dans la defausse : rien n'entre en jeu ; Response : apres avoir abattu un sbire ELITE (Time-Displaced Soldier 11048, 3 PV), ca007 (epuisee avant) est redressee ; TEMOIN : un sbire NON elite (Hydra Mercenary) est abattu : ca007 reste epuisee. Preuve par substitution : rouges 3/5 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca008 : Amorphous Arsenal

- [x] Etape 2 : carte(s) de reference : - « when you make an attack WITH <keyword> → +N damage » : `bl008` (Blade's Sword) : `WhenUnitMakeKeyWordAttack(.., "You", op)` + `message.DealAdditionalDamage(n, effect)` ; ce message part APRES `WhenUnitWouldAttack`, donc apres les mots-cles donnes par d'autres cartes (ca006 overkill, ca011 ranged, ca012 piercing) ET par l'Interruption de cette carte. Le compte lit `message.would_atk_unit_message.IsOverKill()/IsPiercing()/IsRanged()` (`av005`). - « choose a keyword → the attack gains it » : `ForChoiceAbility` + `joueur.ChooseAbilities` (`60017`) ; `WhenUnitWouldAttack(HeroInterrupt, "You", op)` + `message.GainOverKill/GainPiercing/GainRanged(effect)`.
- [x] Etape 5 : texte-contre-code : Premiere phrase SANS type imprime = effet CONTINU, obligatoire : `ForcedInterrupt` (et non Hero Interrupt, qui serait refusable comme bl008). « an attack that HAS a keyword » : `has_keyword="Any"` ; « 1 additional damage for EACH keyword it has » : 1, 2 ou 3 selon les mots-cles presents (overkill, piercing, ranged ; pas les autres mots-cles). « When YOU make an attack » : toute attaque de l'identite, evenement d'attaque compris (libelle `attack`). « Hero Interrupt: When you attack, exhaust this card AND choose a keyword → » : l'inclinaison est le COUT ; le mot-cle est choisi a la resolution ; « THAT attack gains » : l'attaque en cours (`WhenUnitWouldAttack`). Le mot-cle donne compte pour la premiere phrase (+1) : la premiere s'evalue apres. Chiffres : cout 3, +1 par mot-cle.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (6) : attaque avec UN mot-cle (Chomp : piercing) : 8 + 1 = 9 degats sur le vilain ; DEUX attaques de Vicious Lashing (ranged chacune, 2 degats) : +1 par attaque = 3 + 3 = 6 sur le vilain ; UN mot-cle OVERKILL (Rend, ca008 inclinee) sur Hydra Mercenary a 1 PV : 6 + 1 = 7 degats d'attaque, exces 6 au vilain ; DEUX mots-cles : Chomp (piercing) + l'Interruption (ca008 prete) donne overkill : 8 + 2 = 10 degats, ca008 s'incline ; TEMOIN : attaque de base SANS mot-cle, ca008 inclinee : 2 degats, pas de bonus ; Hero Interrupt : en attaquant (base, ca008 prete), un mot-cle est choisi puis donne, ca008 s'incline : 2 + 1 = 3 degats. Preuve par substitution : rouges 5/6 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca009 : Klyntar Bond

- [x] Etape 2 : carte(s) de reference : - « When X uses a basic power » : `32177` (Swagger) : `WhenUnitUseBasicPower(HeroInterrupt, 'YourHero', op)` ; carte de boost donnee a un HEROS : `Faces.GiveFacedownBoostCards([identite], 1, effect)` (`sf011`, `dd001a`). - « Resource: Exhaust → generate a [wild] resource » : `im005` (Stark Tower) : `CanGenerateResources(AbilityType.Resource, Resources("G"))` + `CostFunc.Exhaust("This")` ; restriction « for a Carnage event » : parametre `for_card=CardFinder(..)` de la fabrique (resources.py:341).
- [x] Etape 5 : texte-contre-code : « Hero Interrupt: When CARNAGE uses a basic power » : `YourHero` (face heros seule), pouvoirs de base ATK / THW / DEF ; « you MAY give him a boost card » : Interruption facultative (le joueur la prend ou non) ; UNE carte de boost, face cachee, au heros. « Resource » NU : se genere dans les deux formes. « generate a [WILD] resource » : DECISION UTILISATEUR du 03/11 : ressource WILD (comme ecrit dans `cards.json`), PAS une ressource maison ★. « FOR A CARNAGE EVENT » : ne paie qu'un EVENEMENT du set « Carnage » (ca010 a ca013), jamais une amelioration ni une carte d'un autre set. Chiffres : cout 3, 1 carte de boost, 1 ressource wild.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (4) : Hero Interrupt : a l'attaque de base, Carnage recoit UNE carte de boost (Hydra Mercenary, 1 icone) : 2 + 1 = 3 degats sur le vilain ; TEMOIN DE BASE : sans la carte, la meme attaque fait 2 degats et Carnage ne recoit aucune carte de boost ; Resource : paie seule un evenement Carnage (ca010, cout 1, main = ca010 seule) ; ca009 s'incline ; TEMOIN : ca009 NE PAIE PAS une amelioration Carnage (ca004, cout 1, main = ca004 seule) : elle reste en main, ca009 reste prete. Preuve par substitution : rouges 2/4 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca010 : Sinister Flight

- [x] Etape 2 : carte(s) de reference : - Evenement de menee qui ignore Patrouille : `42006` (Natural Flight) : `RemoveThreatFromSchemes(effect.targets, N, effect)` + `.SetPlay().SetLabel('thwart').SetTarget(Scheme2).SetIgnoreKeyword(..)`. ICI seul Patrol est ignore (pas Crisis : le texte ne le dit pas). - Trait gagne jusqu'a la fin de la phase : `GainUntilPhaseEnd(effect, trait=..)` (`face_action.py:513`) ; modele de forme `60017` (`GainUntilRoundEnd(effect, trait=['AERIAL'])`).
- [x] Etape 5 : texte-contre-code : « Hero Action (thwart) » : `HeroAction` + `SetLabel('thwart')` (les cartes qui reagissent a « thwart » le voient). « Remove 2 threat from A scheme » : UN complot, principal ou annexe (`Scheme2`), 2 menaces. « ignoring the PATROL keyword » : `SetIgnoreKeyword('Patrol')` seulement. « CARNAGE gains the AERIAL trait » : l'identite du joueur (face heros, seule face ou l'evenement se joue). « UNTIL THE END OF THE PHASE » : `GainUntilPhaseEnd`, pas le round. Chiffres : cout 1, 2 menaces. Deux exemplaires dans le deck (cas : `ca010`).
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (3) : retire 2 menaces du complot principal MALGRE un sbire Patrol engage (Badoon Lieutenant 16119) et Carnage gagne AERIAL ; TEMOIN DE BASE : sans la carte jouee, Carnage n'a pas AERIAL ; AERIAL tombe a la FIN DE LA PHASE (pas le round) : absent apres la fin de la phase des joueurs. Preuve par substitution : rouges 5/6 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca011 : Vicious Lashing

- [x] Etape 2 : carte(s) de reference : - Interruption d'evenement « when an enemy attacks you → deal N damage to that enemy » : `05012` (Nova) : `WhenUnitInitiatesAttackAgainst(Interrupt, Enemy, "You", op).SetTarget("Attacker")` ; evenement a libelle `bw005` (`.SetPlay().SetLabel('defense')`) ; mot-cle ranged : fiche mots-cles/ranged.md, `AttackProperty(ranged=True)`. - Action « Deal 2 damage to an enemy. Deal 2 damage to an enemy. » : `bm003` (Violent Means) : deux choix de cible INDEPENDANTS (`Worlds.GetOnFieldEnemies` + `AskChooseFace`), cas `bm003` (`cibles=[VILAIN, VILAIN]`).
- [x] Etape 5 : texte-contre-code : « Hero Interrupt (attack/defense) » : `HeroInterrupt` + `SetLabel('attack', 'defense')`. « When an enemy attacks YOU » : l'attaque vise l'identite du joueur (`"You"`), pas un allie. « deal 4 damage to THAT enemy » : l'attaquant (`SetTarget("Attacker")`). « This attack gains RANGED » : `AttackProperty(ranged=True)` sur les degats (pas de Retaliate en retour). « Deal 2 damage to AN enemy. Deal 2 damage to AN enemy » : DEUX cibles choisies separement, la meme possible. Deux capacites distinctes sur la meme carte : l'Interruption n'est proposee que pendant une attaque ennemie, l'Action pendant le tour du joueur. Chiffres : cout 2, 4 degats / 2 + 2 degats.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (3) : Hero Action : deux fois 2 degats, les deux sur le vilain (Rhino) = 4 ; TEMOIN (limite du harnais) : 4 degats en deux coups tuent Whiplash (Retaliate 1) ; Carnage ne subit rien ; Hero Interrupt : un ennemi (Hydra Mercenary, 3 PV) attaque Carnage ; 4 degats a l'attaquant, il tombe et Carnage ne subit rien. Preuve par substitution : rouges 3/3 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca012 : Chomp

- [x] Etape 2 : carte(s) de reference : - Evenement d'attaque a libelle, degats fixes + mot-cle d'attaque : `uw004` (Deranged Burst) : `this.DealDamage(effect.targets, N, effect, property=AttackProperty(piercing=True))` + `.SetPlay().SetLabel('attack').SetTarget(Enemy)`. - « If this attack defeats that enemy → » : `th009` (Sock 'Em) / `sn002` : `if_this_attack_defeats=fn`, appelee PAR UNITE VAINCUE par CETTE attaque ; redressement : `Faces.ReadyAll` (`an001a`).
- [x] Etape 5 : texte-contre-code : « Hero Action (attack) » : `HeroAction` + `SetLabel('attack')`. « Deal 8 damage to AN enemy » : une cible, vilain ou sbire (`Enemy`). « This attack GAINS PIERCING » : `AttackProperty(piercing=True)` (fiche mots-cles/piercing.md : defausse un statut tough au lieu d'etre absorbe). « IF THIS ATTACK defeats THAT enemy » : defaite par CETTE attaque seulement (`if_this_attack_defeats`). « ready CARNAGE » : l'identite du joueur (face heros, seule forme ou l'evenement se joue). Chiffres : cout 3, 8 degats.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (4) : inflige 8 degats au vilain (Rhino) ; PIERCING : un sbire robuste (statut tough, 3 PV) est abattu malgre la robustesse ; si l'attaque VAINC l'ennemi, Carnage (epuise avant) est redresse ; TEMOIN : l'ennemi SURVIT (Rhino, 14 PV) : Carnage reste epuise. Preuve par substitution : rouges 4/4 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca013 : Rend

- [x] Etape 2 : carte(s) de reference : - Evenement d'attaque a libelle + mot-cle : `uw004` (`this.DealDamage(.., property=AttackProperty(..))`, `.SetPlay().SetLabel('attack').SetTarget(Enemy)`) ; fiche mots-cles/overkill.md. - Surpaiement d'un EVENEMENT : `sk008` / `yd006` : `effect.GetCostX()` = ressources payees - cout (effect.py:519) ; `effect.GetPaidResources().GetColor("R")` pour le nombre de ressources [physical] payees (le wild compte).
- [x] Etape 5 : texte-contre-code : « Deal 6 damage ... This attack gains OVERKILL » : UNE attaque de 6 avec `AttackProperty(overkill=True)`. « 2 ADDITIONAL damage for EACH [physical] you OVERPAID » : seules les ressources [physical] AU-DELA du cout comptent ; lecture du joueur (FAQ du jeu : le joueur choisit lesquelles de ses ressources sont le surplus) = min(surpaiement total, ressources [physical] payees). « to a MAXIMUM of three » : plafond 3 (soit +6). Les ressources d'une autre couleur surpayees ne rapportent rien. Chiffres : cout 3, 6 degats, +2 par [physical], plafond 3.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (4) : paye avec Energy + Genius (YYBB, AUCUN [physical]) : 6 degats, le surpaiement ne rapporte rien ; paye avec Strength x2 (RRRR) : 1 [physical] surpaye = 6 + 2 = 8 degats ; surplus de 3 [physical] (6 ressources [physical] payees avec quatre cartes) : bonus maximal, 6 + 6 = 12 degats ; OVERKILL : Hydra Mercenary a 1 PV restant (6 degats, exces 5) : l'exces passe au vilain. Preuve par substitution : rouges 4/4 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca014 : Essential Bloodlust

- [x] Etape 2 : carte(s) de reference : - `dy013` (Seizure) / `my015` (My Love) / `mt011` : meme gabarit (`WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` + `ChooseAbilities`, branche 1 `condition=joueur.IsAlterEgo()` + `Exhaust("YourIdentity")`). - Degats indirects : `ch021` : `this.DealIndirectDamage(identite, N, effect)` (le joueur repartit entre son identite et ses allies).
- [x] Etape 5 : texte-contre-code : « You may flip to alter-ego form » : bascule facultative avant le choix. « Exhaust EDDIE BROCK → remove from the game » : l'alter-ego (donc seulement en forme alter-ego, apres l'eventuelle bascule) doit etre PRET ; la carte quitte la partie. « Take indirect damage equal to YOUR ATK. Discard this obligation » : DECISION UTILISATEUR du 03/11 (lecture B) : l'ATK COURANTE de l'identite (bonus de cartes compris : Frenzied Violence +1...). En forme ALTER-EGO l'identite n'a PAS d'ATK : 0 degat indirect (basculer en alter-ego avant de choisir la seconde branche l'annule donc). « Discard this obligation » appartient a la SECONDE branche (la premiere la retire de la partie). Aucun surge (le texte n'en parle pas). Chiffres : boost 2, degats = ATK.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (2) : branche 1 : en alter-ego, Eddie Brock s'incline et l'obligation est RETIREE de la partie ; branche 2 en ALTER-EGO : l'identite n'a pas d'ATK, 0 degat indirect, l'obligation est tout de meme defaussee. Preuve par substitution : rouges 2/2 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca015 : Torment

- [x] Etape 2 : carte(s) de reference : - Quickstrike / Villainous : mots-cles natifs lus dans `desc` (fiches mots-cles/quickstrike.md, villainous.md), AUCUN code. - « Search the encounter deck, discard pile and set-aside area for X and reveal it » : `49022` (Face the Past : meme balayage deck + defausse + zone de cote) + `find.md` (`Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)` puis `face.Reveal(joueur, effect)`) ; `bw021` (Imperius Rex) pour la recherche d'une carte du set nemesis. - Interruption forcee « when X attacks a friendly character → cancel » : `sk242` (`WhenUnitWouldAttack(ForcedInterrupt, .., op)`) + `hf120` (`message.CancelThisAttack`) ; helpers `EchangerContreUnSacrifice` / `CibleAmie` (carnage_nemesis/__init__.py), partages avec Death Spiral (ca017).
- [x] Etape 5 : texte-contre-code : « When Revealed: SEARCH the encounter deck, discard pile AND set-aside area for Death Spiral AND REVEAL it » : une carte, trois zones, revelee (son attache a Torment resout alors). Absente (deja en jeu ou introuvable) : rien d'autre. « [star] Forced Interrupt: When TORMENT attacks a FRIENDLY character » : l'attaquant est Torment lui-meme (`"This"`) ; cible = identite ou allie du joueur. « an ALLY OR PERSONA SUPPORT with the SAME CLASSIFICATION as THAT CHARACTER, under your control OR IN YOUR HAND » : classe imprimee (identite = `Hero`). « cancel this attack AND discard THAT CARD instead » : annulation + defausse de la carte choisie. Sans carte sacrifiable l'attaque a lieu. Chiffres : PV 6, ATK 1, SCH 2, boost 3.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (4) : When Revealed : cherche Death Spiral (set nemesis mis de cote) et la REVELE : elle s'attache a Torment ; TEMOIN : Death Spiral INTROUVABLE (set nemesis retire de la zone de cote) : rien n'est revele, aucun attachement ; Forced Interrupt : deux Spider-Man (classe Hero) en MAIN, deux attaques de Torment (Quickstrike a l'entree puis `Puzzle.Attack`) : chacune est annulee ; TEMOIN : aucune carte sacrifiable (main = Energy seule) : l'attaque a lieu, Carnage subit des degats. Preuve par substitution : rouges 2/4 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca016 : Meticulous Targeting

- [x] Etape 2 : carte(s) de reference : - « Find X and reveal it ; if already in play, it engages you » : `find.md` (`Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)` + `face.Reveal(joueur, effect)`), `Worlds.FindCardOnField` pour « deja en jeu » ; engagement : `ar014` (`Minion.EngagePlayer(joueur, effect)`). - « X activates against you » : `bw021` (Imperius Rex) / `11051` : `ennemi.DoActivate(joueur, effect)` ; rend `None` quand l'ennemi n'a pas pu s'activer (`enemy.py:303`). - « If no enemy activated this way, this card gains surge » : `this.GainSurge(1, effect)` (my015). - Menace de depart par joueur (`StartingThreat 2*`) et Amplify 1 : lus nativement dans `desc` (fiche mots-cles/amplify.md), aucun code.
- [x] Etape 5 : texte-contre-code : « FIND Torment and REVEAL him » : en jeu -> il s'engage avec le joueur ; sinon recherche dans le deck, la defausse et la zone de cote, puis revelation (son When Revealed resout, son Quickstrike frappe). « Torment ACTIVATES against YOU » : une activation (attaque ou manigance selon l'etat du joueur) contre le joueur qui revele. « If NO enemy activated this way » : Torment introuvable OU activation impossible -> surge. Chiffres : menace de depart 2 par joueur, Amplify 1, boost 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (4) : Torment dans le set de cote : il est TROUVE et REVELE (en jeu, engage avec le joueur) ; Torment trouve : il s'active CONTRE le joueur EN PLUS de son Quickstrike (deux Spider-Man en main, deux attaques annulees : main videe) ; Torment DEJA EN JEU : une seule activation contre le joueur (deux Spider-Man en main, un seul annule, il en reste un) ; Torment INTROUVABLE (set nemesis retire) : aucun ennemi ne s'active, la carte gagne SURGE (Hydra Mercenary distribuee). Preuve par substitution : rouges 4/4 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca017 : Death Spiral

- [x] Etape 2 : carte(s) de reference : - « Attach to X. Otherwise, gains surge » : `AttachToFaceWhenPutIntoPlay(CardFinder(..), if_cannot_gain_surge=True)` (attachment.py:47) ; modele de forme `sk242` (attache a un sbire d'un trait). - « When the attached enemy attacks → cancel » : `sk242` : `WhenUnitWouldAttack(ForcedInterrupt, "AttachedEnemy", op)` + `message.CancelThisAttack(effect)` (`hf120`). - « Hero Action: Spend [mental][physical] → discard this card » : `sk147` (Distracted) : `PlayerActionToDiscardThis(HeroAction).SetCost(Cost("BB"))` ; ici `Cost("BR")` ([mental]=B, [physical]=R, verifie contre une carte du pack : ca003 RES B, ca004 RES R).
- [x] Etape 5 : texte-contre-code : « Attach to TORMENT. Otherwise → surge » : seul Torment (le sbire du set) convient ; absent, la carte gagne surge. « [star] » : capacite propre a la carte (`NonKeywordStar` dans la fiche special.md : le moteur n'en fait rien de plus ; l'Interruption forcee est bien portee par la carte). « When TORMENT attacks a FRIENDLY character » : l'attache (`"AttachedEnemy"`) attaque une identite ou un allie du joueur. « an ALLY OR PERSONA SUPPORT with the SAME CLASSIFICATION as THAT CHARACTER, under your control OR IN YOUR HAND » : helper `CartesSacrifiables` (classe imprimee ; identite = `Hero`) ; « cancel this attack AND discard THAT CARD INSTEAD » : l'attaque est annulee et la carte choisie par le joueur est defaussee. Sans carte sacrifiable, l'attaque a lieu. Meme texte que Torment : si les deux sont en jeu, la premiere annule l'attaque et la seconde n'a plus rien a annuler (une seule carte defaussee). « Hero Action » : forme heros seulement ; cout [mental][physical] (B + R). Chiffres : boost 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (5) : revelee avec Torment en jeu : elle s'attache A TORMENT ; Torment ABSENT : « Otherwise, this card gains surge » : la carte suivante du deck (Hydra Mercenary) est distribuee ; Forced Interrupt (avec celle de Torment, meme texte) : deux Spider-Man (classe Hero) en MAIN, deux attaques de Torment (Quickstrike a l'entree puis `P ; TEMOIN : aucun allie ni soutien PERSONA de meme classification (main = Energy seule) : l'attaque a lieu, Carnage subit des degats ; Hero Action : on depense [mental][physical] (une carte RBY : Cosmic Cube Fragment sk230d) et la carte est defaussee ; Torment reste en jeu. Preuve par substitution : rouges 3/5 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca018 : Closing the Loops

- [x] Etape 2 : carte(s) de reference : - « X attacks you (even in alter-ego) ; if no attack... surge » : `ld013` (Lash Out) : `ennemi.DoAttackYou(joueur, effect, ..)` (attaque dans les deux formes) ; `if_no_attack_was_made=` (enemy.py:110) pour le surge. - Boost etoile « +1 boost icon » : `sk116` (Skrull Assault) : `WhenCardBecomeBoost("This", op)` + `message.GainBoostIcon(n, effect)`.
- [x] Etape 5 : texte-contre-code : « TORMENT attacks you » : Torment en JEU (introuvable ou pas en jeu : aucune attaque -> surge) ; « even in alter-ego form » : `DoAttackYou` attaque aussi l'alter-ego. « If NO attack was made this way » : `if_no_attack_was_made` (aussi quand Torment est absent). « [star] Boost: +1 boost icon IF you have MORE THAN 2 classifications IN PLAY » : plus de 2 classifications DISTINCTES parmi les cartes sous le controle du joueur (identite comprise : IdentitySpecific ; un aspect compte par aspect ; Basic). Meme `ClassificationDe` que Torment. ⚠ LECTURE A CONFIRMER : l'identite elle-meme compte comme « identity-specific in play » (lecture litterale : elle est une carte en jeu). Sans elle, il faudrait trois classifications parmi les seules cartes du deck. Chiffres : boost 1 (+1), seuil > 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (5) : When Revealed : Torment (en jeu) ATTAQUE le joueur : un Spider-Man en main est defausse (attaque annulee par Torment), Carnage ne subit rien de plus ; ALTER-EGO (« even in alter-ego form ») : l'attaque a lieu aussi (Spider-Man defausse a la place) ; Torment ABSENT (set nemesis retire) : aucune attaque, la carte gagne SURGE (Hydra Mercenary distribuee) ; Boost avec TROIS classifications en jeu (identite, Aggression 01057, Basic 05033) : 1 + 1 = 2 icones de boost, l'attaque d'Hydra Mercenary (ATK 1) fai ; TEMOIN : seulement DEUX classifications en jeu (identite + Aggression) : 1 icone de boost, l'attaque fait 2. Preuve par substitution : rouges 4/5 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca019 : Muse

- [x] Etape 2 : carte(s) de reference : - Steady / Villainous : natifs (`desc`, fiches steady.md / villainous.md), aucun code. - « attacks X instead » : `41028` (Psionic Illusion) / `ca022` : `WhenUnitWouldAttackUnit(ForcedInterrupt, .., op)` + `message.ChangeTarget(unit, effect)` ; « gains piercing » : `message.GainPiercing(effect)` (sender_damage.py:395, fiche piercing.md). - Soin de l'exces : `AfterUnitDefeatedUnit(.., is_from_attack=True, has_excess_damage=True)` + `message.excess_damage` (ca001a Death-Dealer, ar005) ; `HealthUnits([muse], n, effect)` (my001b).
- [x] Etape 5 : texte-contre-code : « the CHARACTER with the FEWEST REMAINING hit points » : personnage AMI (identite, allies) du joueur attaque, PV RESTANTS (`health`) ; ex aequo : le joueur choisit. LECTURE : « character » = ami (contraste avec Murderous Nature, qui nomme expressement « or other enemy »). « This attack gains PIERCING » : tous ses attaques via cette Interruption. « If this attack DEFEATS a character, heal 1 damage FROM MUSE for EACH point of EXCESS damage » : soin de Muse = exces de CETTE attaque ; aucun exces = aucun soin. Chiffres : PV 6, ATK 1, SCH 2, boost 3. ⚠ Meme limite que ca022 : aucune redirection vers un ennemi (il n'y en a pas ici : ami seulement).
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (3) : Forced Interrupt : elle attaque l'ALLIE aux PV restants les plus bas (Spider-Man, 4) et non Carnage (12) ; PIERCING : Spider-Man porte un statut TOUGH (4 PV) ; l'attaque le defausse au lieu d'etre absorbee : Spider-Man est blesse ; si l'attaque VAINC un personnage (Spider-Man a 1 PV restant), Muse (endommagee avant) se soigne d'1 par point d'EXCES. Preuve par substitution : rouges 2/3 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca020 : Bushwacker

- [x] Etape 2 : carte(s) de reference : - Toughness / Villainous : natifs (`desc`, fiches toughness.md / villainous.md), aucun code. - « X's attacks gain piercing and overkill » : `UnitAttackGainKeyword("This", piercing=True, overkill=True)` (do_attack.py:828, modele ca006 / im012 ; fiches piercing.md, overkill.md). - Boost etoile « give this enemy another boost card » : `27141` / `sender_card.py` : `message.GiveActivatingEnemyAdditionalBoostCard(1, effect)` ; test « attache a cet ennemi » sur les attachements de l'ennemi qui s'active.
- [x] Etape 5 : texte-contre-code : « Bushwacker's ATTACKS gain piercing AND overkill » : toutes ses attaques, les deux mots-cles. « [star] Boost: IF Murderous Nature is attached TO THIS ENEMY » : lecon du boost : « this enemy » = l'ennemi qui s'active et recoit cette carte de boost (pas Bushwacker, qui n'est qu'une carte retournee) ; une seule carte de boost supplementaire, seulement si Murderous Nature est attachee a cet ennemi. Chiffres : PV 8, ATK 2, SCH 1, boost 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (5) : OVERKILL : il attaque Spider-Man (3 degats deja, 1 PV restant) : l'exces est inflige a Carnage ; PIERCING : Spider-Man porte un statut TOUGH ; l'attaque le defausse au lieu d'etre absorbee : Spider-Man est blesse ; Boost AVEC Murderous Nature attachee a l'ennemi qui s'active : UNE carte de boost supplementaire (Hydra Mercenary, 1 icone) s'ajoute ; TEMOIN : sans Murderous Nature sur l'ennemi qui s'active, pas de carte de boost supplementaire ; TEMOIN DE BASE : Murderous Nature seule (Villainous gagne : +1 carte de boost de rencontre), SANS Bushwacker : ATK 2 + 1 icone = 3. Preuve par substitution : rouges 3/5 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca021 : Recognizing Evil

- [x] Etape 2 : carte(s) de reference : - « Find a copy of X and reveal it » : `find.md` / ca015 : `Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)` + `face.Reveal(joueur, effect)`. - Exces d'une attaque : `AfterUnitDefeatedUnit(.., is_from_attack=True, has_excess_damage=True)` + `message.excess_damage` (ca001a, ar005) ; menace posee sur ce complot : `this.PlaceThreatOnSchemes([this], n, effect)`. - Interdire l'exces : le transfert d'overkill est un `WhenUnitWouldTakeDamage` dont `property.is_from_overkill` est vrai (damage_property.py:7, can_health.py:243) : `message.PreventDamage("All", effect)`. - Acceleration 1 et menace de depart par joueur : natifs (`desc`, fiche mots-cles/acceleration.md), aucun code.
- [x] Etape 5 : texte-contre-code : « EXCESS damage dealt BY KILLER MINIONS is placed AS THREAT here » : DECISION UTILISATEUR du 03/11 (lecture B, EN REMPLACEMENT) : l'exces d'un sbire KILLER qui abat un personnage est CONVERTI en menace sur ce complot annexe et N'EST PLUS INFLIGE (le transfert d'overkill vers l'identite est empeche). Seuls les sbires portant le trait KILLER (Torment, Muse, Bushwacker, tout sbire sous Murderous Nature) ; l'exces mesure ce qui depasse les PV restants du personnage abattu (attaque seulement). Sans exces, rien. « When Revealed: FIND A COPY of Murderous Nature and REVEAL it » : recherche dans le deck, la defausse et la zone de cote ; aucune copie : rien. Chiffres : menace de depart 2 par joueur, Acceleration 1, boost 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (3) : When Revealed : cherche UNE copie de Murderous Nature (dans le deck) et la REVELE : elle s'attache a Hydra Mercenary ; EXCES EN MENACE (lecture B, remplacement) : Bushwacker (KILLER, overkill) abat Spider-Man (1 PV restant) ; l'exces devient menace sur ca021, Carnage n ; TEMOIN DE BASE : sans ca021, le meme exces est INFLIGE a Carnage (overkill de Bushwacker). Preuve par substitution : rouges 2/3 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca022 : Murderous Nature

- [x] Etape 2 : carte(s) de reference : - « Attach to a minion ... Otherwise surge » : `AttachToFaceWhenPutIntoPlay(CardFinder(..), without_another_copy=True, if_cannot_gain_surge=True)` (attachment.py:47, comme ca017) ; « gains trait / villainous » : `GiveKeywordToAttached(Minion, trait=.., villainous=1)` (asset.py:6). - « it attacks X instead » : `41028` (Psionic Illusion) : `WhenUnitWouldAttackUnit(ForcedInterrupt, .., op)` + `message.ChangeTarget(unit, effect)` ; mot-cle : `message.GainOverKill(effect)` (sender_damage.py:388).
- [x] Etape 5 : texte-contre-code : « non-ELITE MINION WITHOUT A COPY of Murderous Nature » : `CardFinder(non_trait="ELITE", card_type=Minion)` + `without_another_copy=True` ; aucun sbire valable -> surge. « gains KILLER AND villainous » : les deux, par l'attache. « [star] Forced Interrupt: When ATTACHED enemy attacks » : l'ennemi porteur (`"AttachedEnemy"`). « the FRIENDLY character OR OTHER ENEMY with the FEWEST REMAINING hit points » : PV RESTANTS (`health`), parmi les personnages amis (identite, allies) ET les AUTRES ennemis en jeu (jamais lui-meme) ; ex aequo : le joueur choisit. « That attack gains OVERKILL ». Chiffres : boost 3. ⚠ LIMITE DU MOTEUR (03/11) : la branche « OR OTHER ENEMY » est codee (les autres ennemis sont candidats, `ChangeTarget`) mais le moteur ne redirige pas une attaque d'ennemi vers un AUTRE ennemi : `ChangeTarget(<ennemi>)` laisse l'attaque frapper l'identite (cas ecrit puis retire le 03/11 : Carnage prenait 2 degats, Hydra Bomber 0). A verifier en partie reelle. Le test « sans copie deja attachee » n'est pas montable non plus : `Puzzle.Reveal('ca022')` retrouve la copie DEJA en jeu (meme card_id).
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (3) : revelee avec un sbire NON elite en jeu (Hydra Mercenary) : elle s'attache a lui et il gagne le trait KILLER ; TEMOIN : seul sbire en jeu ELITE (Sandman 01102) : pas de cible valable, la carte gagne SURGE (Hydra Mercenary distribuee) ; Forced Interrupt : le sbire porteur attaque, mais frappe l'ALLIE aux PV restants les plus bas (Spider-Man, 4) et non Carnage (12). Preuve par substitution : rouges 2/3 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca023 : Hunting Victims

- [x] Etape 2 : carte(s) de reference : - « Each X minion engaged with a player activates against that player ; if none, surge » : `ar014` (Lead the Charge) / `bw021` : `enemy.DoActivate(joueur, effect)` (rend `None` si l'ennemi ne s'est pas active, enemy.py:303), `this.GainSurge(1, effect)` (ca016, my015). - Boost etoile qui concerne l'ACTIVATION en cours : `sk116` (`WhenCardBecomeBoost("This", op)`), `GiveBoostCardForThisActivation` / `message.would_message` (sender_card.py:776) ; capacite temporaire de l'ennemi qui s'active : `RegisterTemp` (`GainBoostIcon`, sender_card.py:748). - Exces en menace, EN REMPLACEMENT : meme mecanique que ca021 (`AfterUnitDefeatedUnit(.., has_excess_damage=True)` + `message.excess_damage` ; transfert d'overkill `property.is_from_overkill` empeche par `PreventDamage("All")`).
- [x] Etape 5 : texte-contre-code : « EACH KILLER minion ENGAGED WITH A PLAYER activates AGAINST THAT PLAYER » : chaque sbire KILLER engage avec un joueur s'active contre CE joueur (attaque en forme heros, manigance en alter-ego, selon `DoActivate`) ; un sbire non KILLER ou non engage n'agit pas. « If NO minion activates this way » : aucun sbire KILLER engage -> surge. « [star] Boost: If THIS ACTIVATION is an attack that DEFEATS A CHARACTER, EXCESS damage dealt BY THIS ATTACK is placed as threat ON THE MAIN SCHEME » : DECISION UTILISATEUR du 03/11 (lecture B, coherente avec ca021) : l'exces est CONVERTI en menace sur le complot PRINCIPAL et N'EST PLUS INFLIGE. Seule l'attaque de CETTE activation (les autres attaques du tour ne sont pas touchees) ; pas de defaite, pas d'exces : rien. Chiffres : boost 1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (4) : When Revealed : le sbire KILLER engage (Bushwacker) s'ACTIVE contre le joueur : Carnage (epuise) subit des degats ; TEMOIN : aucun sbire KILLER engage (seulement Hydra Mercenary) : personne ne s'active, la carte gagne SURGE (la carte suivante, Hydra Mercenary, est d ; Boost (lecture B, remplacement) : Bushwacker (KILLER, overkill) abat Spider-Man (1 PV restant) avec ca023 en boost : l'exces devient menace sur le com ; TEMOIN DE BASE : meme montage SANS ca023 en boost : l'exces est INFLIGE a Carnage, aucune menace posee. Preuve par substitution : rouges 3/4 (les cas verts sans le module sont des temoins d'absence).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca024 : Face the Past

- [x] Etape 2 : carte(s) de reference : reskin d'une carte OFFICIELLE par `ability_link` (data/cards.json) : meme script que l'officielle, aucun script ici.
- [x] Etape 5 : texte-contre-code : texte identique a l'officielle liee (verifie sur `textes-fr.ts` : memes phrases) ; aucun mot-piege propre.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (1) : Hero Action : revele Torment (nemesis), redresse le heros epuise et pioche 3 cartes ; ca024 quitte la partie. Reskin sans module : preuve par les cas verts (la reskin joue le script de l'officielle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca025 : Energy

- [x] Etape 2 : carte(s) de reference : reskin d'une carte OFFICIELLE par `ability_link` (data/cards.json) : meme script que l'officielle, aucun script ici.
- [x] Etape 5 : texte-contre-code : texte identique a l'officielle liee (verifie sur `textes-fr.ts` : memes phrases) ; aucun mot-piege propre.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (1) : paie le cout 1 de Sinister Flight (ca010) : la menace du complot principal baisse de 2. Reskin sans module : preuve par les cas verts (la reskin joue le script de l'officielle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca026 : Genius

- [x] Etape 2 : carte(s) de reference : reskin d'une carte OFFICIELLE par `ability_link` (data/cards.json) : meme script que l'officielle, aucun script ici.
- [x] Etape 5 : texte-contre-code : texte identique a l'officielle liee (verifie sur `textes-fr.ts` : memes phrases) ; aucun mot-piege propre.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (1) : paie le cout 1 de Sinister Flight (ca010). Reskin sans module : preuve par les cas verts (la reskin joue le script de l'officielle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca027 : Strength

- [x] Etape 2 : carte(s) de reference : reskin d'une carte OFFICIELLE par `ability_link` (data/cards.json) : meme script que l'officielle, aucun script ici.
- [x] Etape 5 : texte-contre-code : texte identique a l'officielle liee (verifie sur `textes-fr.ts` : memes phrases) ; aucun mot-piege propre.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (1) : paie le cout 1 de Sinister Flight (ca010). Reskin sans module : preuve par les cas verts (la reskin joue le script de l'officielle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca028 : Down Time

- [x] Etape 2 : carte(s) de reference : reskin d'une carte OFFICIELLE par `ability_link` (data/cards.json) : meme script que l'officielle, aucun script ici.
- [x] Etape 5 : texte-contre-code : texte identique a l'officielle liee (verifie sur `textes-fr.ts` : memes phrases) ; aucun mot-piege propre.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (1) : l'alter ego gagne +2 REC. Reskin sans module : preuve par les cas verts (la reskin joue le script de l'officielle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca029 : Endurance

- [x] Etape 2 : carte(s) de reference : reskin d'une carte OFFICIELLE par `ability_link` (data/cards.json) : meme script que l'officielle, aucun script ici.
- [x] Etape 5 : texte-contre-code : texte identique a l'officielle liee (verifie sur `textes-fr.ts` : memes phrases) ; aucun mot-piege propre.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (1) : +3 points de vie. Reskin sans module : preuve par les cas verts (la reskin joue le script de l'officielle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca030 : Enhanced Awareness

- [x] Etape 2 : carte(s) de reference : reskin d'une carte OFFICIELLE par `ability_link` (data/cards.json) : meme script que l'officielle, aucun script ici.
- [x] Etape 5 : texte-contre-code : texte identique a l'officielle liee (verifie sur `textes-fr.ts` : memes phrases) ; aucun mot-piege propre.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (1) : Hero Resource : genere [mental] et paie Sinister Flight (ca010) ; ca030 s'incline. Reskin sans module : preuve par les cas verts (la reskin joue le script de l'officielle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca031 : Enhanced Physique

- [x] Etape 2 : carte(s) de reference : reskin d'une carte OFFICIELLE par `ability_link` (data/cards.json) : meme script que l'officielle, aucun script ici.
- [x] Etape 5 : texte-contre-code : texte identique a l'officielle liee (verifie sur `textes-fr.ts` : memes phrases) ; aucun mot-piege propre.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (1) : Hero Resource : genere [physical] et paie Sinister Flight (ca010) ; ca031 s'incline. Reskin sans module : preuve par les cas verts (la reskin joue le script de l'officielle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca032 : Enhanced Reflexes

- [x] Etape 2 : carte(s) de reference : reskin d'une carte OFFICIELLE par `ability_link` (data/cards.json) : meme script que l'officielle, aucun script ici.
- [x] Etape 5 : texte-contre-code : texte identique a l'officielle liee (verifie sur `textes-fr.ts` : memes phrases) ; aucun mot-piege propre.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (1) : Hero Resource : genere [energy] et paie Sinister Flight (ca010) ; ca032 s'incline. Reskin sans module : preuve par les cas verts (la reskin joue le script de l'officielle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca033 : Ready to Rumble

- [x] Etape 2 : carte(s) de reference : reskin d'une carte OFFICIELLE par `ability_link` (data/cards.json) : meme script que l'officielle, aucun script ici.
- [x] Etape 5 : texte-contre-code : texte identique a l'officielle liee (verifie sur `textes-fr.ts` : memes phrases) ; aucun mot-piege propre.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (1) : Hero Response : apres un changement de forme, la carte est defaussee et le heros est redresse. Reskin sans module : preuve par les cas verts (la reskin joue le script de l'officielle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).

### ca034 : Symbiote Suit

- [x] Etape 2 : carte(s) de reference : reskin d'une carte OFFICIELLE par `ability_link` (data/cards.json) : meme script que l'officielle, aucun script ici.
- [x] Etape 5 : texte-contre-code : texte identique a l'officielle liee (verifie sur `textes-fr.ts` : memes phrases) ; aucun mot-piege propre.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (chiffres de la ligne « Chiffres » de l'entete du script).
- [x] Etape 7 : cas (1) : +1 a chaque pouvoir de base et +10 points de vie. Reskin sans module : preuve par les cas verts (la reskin joue le script de l'officielle).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 8 parties (rhino, normal, equilibre), 0 bloquee, grep tracebacks : 0 sur les 8 journaux (apres correction de ca002) ; temoin spider_man : 8 parties, 0 bloquee.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, cartes en jeu, attachements (Death Spiral sur Torment), complots annexes ; cas Vitest `carnage-plateau.test.ts` + captures Chromium FR et EN (captures/carnage, captures/carnage-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 8 parties autoplay menees au bout, tous les decks montent).


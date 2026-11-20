# Major Victory (Vance Astro) : gabarits PROCESSUS-CARTE, 30/10/2026

Pack `major_victory` (prefixe `mv`, set 236). Scripts : `src/cards/pack/major_victory/{major_victory,major_victory_nemesis}/`.
Cas : `tools/cas/major_victory.py` (42 cas, noms commencant par le card_id) ; plateau : `ui-app/src/board/major-victory-plateau.test.ts` (4 cas) ; deck `major_victory` ; textes FR : `ui-app/src/board/textes-fr-fanmade.ts` ; biographie : `public/js/prepare/heros-info.js` (`mv001a`).

**Aucune carte n'est « terminee »** : il manque UNE chose que je ne peux pas faire, la partie reelle jouee par un humain dans le navigateur (voir « Manques »). Les 17 cartes du pack sont scriptees, testees et prouvees par substitution.

**Source** : Drive partage « Major Victory » (dossiers `Hero Deck`, `Not so good stuff`, `hero.png`, `alter-ego.png`), telecharge par `curl -sL "https://drive.google.com/uc?export=download&id=<id>"` dans `~/Desktop/Major-Victory-source/` (hors depot). 23 PNG 1500x2150 (Korvac's Future en 2150x1500 ; l'obligation `obligation.png` est dans « Not so good stuff », elle avait ete ratee a la premiere lecture du dossier a cause de la pagination du connecteur Drive : 5 fichiers par page, et la 2e page se lit avec le jeton de la 1re), passes par `outils/uniformiser-scans.py --sauvegarde` puis `--appliquer` (615x882, originaux dans `sauvegardes-serveur/scans-originaux`). Auteur inconnu : le champ `custom` est volontairement absent.

**Numerotation** : mv001a/b identite ; mv002-mv011 deck de heros (15 cartes : mv005 x2, mv006 x3, mv008 x2, mv009 x2) ; **mv012 = l'obligation Damaged Containment Suit** ; mv013-mv016 nemesis (5 cartes : mv015 x2). Les numeros « n/15 » du Drive sont par EXEMPLAIRE ; une seule image par carte distincte a ete retenue (la « 4/15 » pour Shield Block, la « 6/15 » pour Psychokinetic Blast, etc.).

**Modification du MOTEUR** : AUCUNE. Seuls fichiers partages touches : `data/cards.json`, `data/sets_info.json` (checksums recalcules avec le venv du projet), `tools/prefixes_fanmade.json`, `deck/starter/major_victory.json`.

**Decisions utilisateur (30/10/2026)** :
- `mv007` : « deal 4 damage to an enemy and deal 4 damage to an enemy » = DEUX choix independants (le meme ennemi peut etre vise deux fois).
- `mv015` : le « gains surge » ne s'applique QU'AU choix « menace » (pas aux degats indirects).

**Autoplay** (`tools/autoplay.py`, rhino et klaw, normal, profils prudent/equilibre/agressif, 24 parties par ligne = 144 parties, 30/10/2026) : toutes TERMINEES (1 victoire, rhino/agressif ; 94 « tous elimines », 49 « manigance accomplie » ; 3,5 a 4,6 rounds), 0 exception sur les 144 journaux (grep `NameError|AttributeError|TypeError|KeyError|AssertionError`), colonne « ! » a 0 ; l'obligation `mv012` et le costume glisse dessous apparaissent dans les 144. Un premier lot de 8 parties (rhino, equilibre) avait donne le meme resultat sans l'obligation, temoin `spider_man` : 0 victoire, 0 exception. ⚠ Le faible taux de victoire du heros ne dit rien de l'equilibrage : le deck de depart n'a PAS de moitie d'aspect (`player_deck` vide, regle du projet) et le pilote joue un deck de cartes signature + ressources inertes. La lecture ligne a ligne des journaux n'a PAS ete faite carte par carte.

**Preuve par substitution** (`tools/substituer_pack.py <game_dir> <port> mv0`, 30/10/2026) : **17/17 cartes** avec au moins un cas rouge sans leur module (mv012 6/6, mv015 6/6, mv009 3/3, mv001a 3/3...). Cas qui restent VERTS sans module, et c'est voulu (contre-cas d'ABSENCE d'effet, a assumer) : `mv010` en alter-ego (le vaisseau ne produit rien), `mv013` sans Korvac en jeu (la menace PEUT etre retiree), `mv014` sous 4 menaces (pas de malus) et a 13 menaces (pas de defaite).

**Defaut de MESURE de mes propres cas (corriges, pas contournes)** :
- `mv008` : 8 menaces posees depassaient le seuil du complot principal, qui s'ACCOMPLIT et termine la partie avant que la carte soit jouee. Pose ramenee a 6.
- `mv001a` limite : la seconde activation refusee faisait echouer la MISE EN PLACE du harnais ; `declencher_tolerant`.
- `mv004` steady : j'avais mesure l'absence d'un statut Stunned, or le premier statut RESTE sur la carte (c'est son effet qui demande deux cartes). Mesure de l'ATTRIBUT `steady`.
- `mv011` : une attaque REPARTIE fait 1 degat PAR CHOIX de cible (`damage = 1`, can_attack.py:398) ; le pilote ne choisit qu'une fois. `cibles` liste la cible autant de fois que de points d'ATQ.
- `mv003` ally : `attributs_carte` prend l'ECART par rapport au PV imprime (+1), pas la valeur absolue (ma premiere version attendait 4 et lisait « attendu 7 »).
- `mv015` : (a) le surge de la branche menace revele une autre carte (1 degat) : deck rencontre vide ; (b) le boost se mesure par les DEGATS d'une vraie activation (`Puzzle.Boost` ACTIVE le vilain), pas par `icones_boost` (la carte boost n'est pas « en jeu »).

**Vrais DEFAUTS de carte trouves par les cas** :
- `mv012` : le degat en plus ne partait JAMAIS (3 au lieu de 4). Le filtre « identite du porteur » utilisait `GetControlByPlayer()` ; une obligation est DONNEE a un joueur, pas controlee comme une amelioration : `GetGaveToPlayer()` (modele `60060`).
- `mv014` (malus de main) ne se recalculait pas quand la menace baissait sous 4 (le temoin « 3 menaces » voyait encore -1). Corrige par `change_on_event=OnEvent.Threat("This")` (modele `sk138`).

**Ecarts assumes**
- `mv010` The Captain America : la condition « un joueur qui controle un personnage GUARDIAN » est lue sur le joueur qui PAIE (`ControleUnGardien` : identite ou allie), avec `AnyPlayerCanDoThis()` pour offrir la ressource a un autre joueur. **Non teste a plusieurs joueurs.**
- `mv013` : « Threat cannot be removed from Korvac's Future » est imprime sur KORVAC : l'interdiction dure tant que Korvac est en jeu (temoin sans Korvac, cas vert).
- `mv005` Shield Block / `mv009` Victory's Command exhaustent le bouclier **par son NOM** « Captain America's Shield ». Le Set de base a une carte officielle `03009` de MEME nom : un deck qui melangerait les deux serait indistinct (l'exhaust cible celui qu'on controle).
- `mv011` Nikki : la ★ imprimee juste apres l'ATQ « 2 » est lue comme l'etoile du texte `[star]` (et non comme un second modificateur de valeur) ; les pastilles sous THW/ATQ comme les degats consequents (`"2**"`, `"2*"`), comme les autres allies.
- **Icones de ressource lues A VUE** (en infraction avec PROCESSUS-CARTE etape 3) : etoile verte = wild `G` (mv002, mv011), noeuds relies lilas = mental `B` (mv003, mv005-mv008 ; meme glyphe que `lj005` qui porte RES=B), eclair jaune = energie `Y` (mv004, mv010), poing orange = physique `R` (mv009). Aucune carte du MEME pack ne porte une ressource certaine : a verifier par un humain contre une carte imprimee.

**Manques (a dire noir sur blanc)**
1. **Aucune partie reelle jouee par un humain** dans le navigateur ; l'autoplay ne remplace pas ce juge. A regarder en priorite : Nikki (le choix de cible est-il bien repete deux fois ?), le vaisseau, le Boost de Judgment, et l'obligation (le costume range sous elle, l'Action d'alter-ego).
2. Pas de lecture ligne a ligne des journaux d'autoplay carte par carte.
3. **Multijoueur** non teste : le vaisseau (`mv010`, ressource offerte a un autre joueur), Shield Block (identite d'un AUTRE joueur), Psychic Link (joueur sans Guardian qui ne pioche pas), Tactical Foresight (« choose a player » = soi dans les cas).
4. `mv007` : seule la lecture « meme ennemi vise deux fois » est mesuree ; « deux ennemis differents » n'a pas de cas.
5. (Fait, pas un manque) Controle de l'etape 10 de PROCESSUS-HEROS, lance le 30/10/2026 : 176 decks de depart, 0 carte signature d'un autre heros ; les 17 cartes distinctes du deck `major_victory` existent toutes dans `cards.json` et appartiennent au set `Major Victory` (heros) ou `Major Victory Nemesis`.
6. (Fait) Passe `verifier_tous_les_decks` sur les **176 decks** apres l'ajout de l'obligation : 176/176 montent une partie, dont `major_victory`.
8. `tools/verifier_coherence_cartes.py` affiche « 0 % » de couverture pour `major_victory` (et pour `smasher`, qui a 67 cas) : l'outil ne lit pas `tools/cas/*.py`, seulement `test_capacites.py`. C'est une limite de l'outil, pas un trou : 42 cas existent et tournent (`test_capacites.py ... mv0`). Il signale aussi des « capacites annoncees sans module » pour les cartes dont les capacites sont portees par `desc` (Peril, Villainous, Retaliate, Restricted, Permanent) : voulu.
7. (Fait) Cas plateau (etape 8 bis) : `ui-app/src/board/major-victory-plateau.test.ts`, 4 cas verts (costume glisse face cachee sous l'obligation, Korvac et la Future, bouclier sur Major Victory). ⚠ Ils sont passes au vert DIRECTEMENT : le correctif generique de `zones.ts` (lecon Contingency Plan) existait deja ; la regle « voir rouge avant le correctif » ne s'applique donc pas. Ils ont ete vus rouges une fois pour une autre raison (mauvaise zone de test), preuve qu'ils peuvent echouer.

---

### mv001a : * Major Victory (face heros)

- [x] Etape 2 : carte(s) de reference : `04001b` Clint Barton / `rg001b` (`SetCost(Cost("1"))` + `Search.PlayerCard` + `GainCard`) ; `Faces.ReturnToHand` pour une carte EN JEU.
- [x] Etape 5 : mots-pieges verifies : « find » (deck + defausse + JEU : `include_player_area`) ; « if it leaves play this way » (`IsInPlay()` lu AVANT le retour en main) ; « deal 4 damage to AN enemy » (cible choisie) ; « Limit once per round ». Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 10, ATK 1, THW 2, DEF 2, HS 5 (scan) = `desc` ; 1 ressource ; 4 degats. Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : bouclier du deck -> en main sans degats ; bouclier EN JEU -> en main + 4 degats ; rouges 3/3 sans module.
- [x] Etape 7 bis : limite imprimee ? OUI (once per round). Temoin d'epuisement : `mv001a Shield Toss — TEMOIN D'EPUISEMENT` : deux activations dans le meme round, le bouclier reste en jeu et Rhino ne prend que 4. Vert ; rouge sans module.
- [x] Etape 8 : autoplay cible : voir l'en-tete.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (carte du jeu vers la main) ; cas plateau `major-victory-plateau.test.ts` (bouclier sur Major Victory), vert.
Carte terminee : NON : partie reelle humaine.

### mv001b : * Vance Astro (face alter-ego)

- [x] Etape 2 : `lj009` Fast Travel (`SetTarget("Players")`, cible = identite, `GetControlByPlayer()`) ; `bw001b` (`Faces.MoveAllToDeck([carte], deck, "Top", effect)`).
- [x] Etape 5 : « THAT player draws 2, THEN places 1 card from THEIR hand » (le joueur choisi choisit sa carte) ; main vide : rien a replacer ; « once per round ». Resultat : conforme.
- [x] Etape 6 : PV 10, REC 3, HS 6 (scan). 2 cartes, 1 carte. Resultat : vert.
- [x] Etape 7 : cas : main 1 + 2 - 1 = 2 ; rouges 2/2 sans module.
- [x] Etape 7 bis : limite OUI. Temoin : `mv001b Tactical Foresight — TEMOIN D'EPUISEMENT` : seconde Action refusee, la main reste a 2 (et non 3). Vert ; rouge sans module.
- [x] Etape 8 : autoplay : voir l'en-tete.
- [x] Etape 8 bis : NON (pioche et replacement sur le deck).
Carte terminee : NON : partie reelle humaine. Cas **monojoueur** seulement (« choose a player » = soi).

### mv002 : Captain America's Shield (amelioration)

- [x] Etape 2 : `03009` * Captain America's Shield (officiel), meme fabrique `GiveKeywordToAttached(CardFinder(name=..), defense=1, retaliate=1)`.
- [x] Etape 5 : « Restricted » lu par le moteur dans `desc` (aucun module) ; « Major Victory gets +1 DEF and gains retaliate 1 » : porteur nomme (face HEROS). Resultat : conforme.
- [x] Etape 6 : cout 1, +1 DEF, retaliate 1, RES G. Resultat : vert.
- [x] Etape 7 : `mv002` : les DEUX ecarts (defense, retaliate) mesures ; rouge 1/1 sans module.
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : NON (attachement standard).
Carte terminee : NON : partie reelle humaine. Pas de `MaxPerUnit` imprime : aucun plafond de restreintes pose.

### mv003 : * Founder of the Guardians (titre)

- [x] Etape 2 : `56120` (`GiveKeywordToInPlayWhenApplyThis(Identity, trait=..)`) ; `sk113` (`CardFinder2(trait, Friend)`).
- [x] Etape 5 : « each identity » (deux faces, tous joueurs) ; « each friendly GUARDIAN character » (identite ET allies). Resultat : conforme.
- [x] Etape 6 : cout 2, +1 PV, RES B. Resultat : vert.
- [x] Etape 7 : alter-ego : devient GUARDIAN (`traits_de`) ET gagne +1 PV ; rouge 1/1 sans module.
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine. (+1 PV d'un ALLIE GUARDIAN : cas `mv003 ... Nikki gagne aussi +1 PV`, vert, rouge sans module ; rouges 2/2.)

### mv004 : Containment Suit (amelioration)

- [x] Etape 2 : `01036` Mark V Armor (`GiveKeywordToAttached("You", health=..)`).
- [x] Etape 5 : « You » et « your identity » = meme cible. Resultat : conforme.
- [x] Etape 6 : cout 1, +2 PV, steady 1, RES Y. Resultat : vert.
- [x] Etape 7 : `+2 PV` et attribut `steady` : rouges 2/2 sans module.
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine.

### mv005 : Shield Block (evenement, x2)

- [x] Etape 2 : `03005` Shield Block (cout exhaust par nom) + `sr006` (`Identity`).
- [x] Etape 5 : « AN identity » (pas « you ») ; « ANY amount » (pas `is_from_attack`) ; « Hero Interrupt » ; bouclier que TU controles. Resultat : conforme.
- [x] Etape 6 : cout 0, RES B. Resultat : vert.
- [x] Etape 7 : bouclier en jeu, 3 degats INDIRECTS (mv015, Future absente) : 0 degat et bouclier incline ; rouge 1/1 sans module. ⚠ Sandman ne traverse plus depuis que mv002 donne +1 DEF.
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine ; protection d'une identite D'UN AUTRE JOUEUR non testee (multijoueur).

### mv006 : Psychokinetic Blast (evenement, x3)

- [x] Etape 2 : `30007` Swinging Web Pig (texte identique).
- [x] Etape 5 : « that enemy » = meme cible pour degats et statut. Resultat : conforme.
- [x] Etape 6 : cout 3, 6 degats, RES B. Resultat : vert.
- [x] Etape 7 : 6 degats + Confused ; rouge 1/1 sans module.
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine.

### mv007 : Telekinetic Throw (evenement)

- [x] Etape 2 : `sf006` (filtre sur la SOURCE `message.by_effect`) + `mv001a` (nom « Shield Toss »).
- [x] Etape 5 : « when YOU deal damage » (meme initiateur) ; « from your "Shield Toss" ability » (nom de la capacite) ; « exhaust Major Victory » (`Exhaust("YourIdentity")`). Decision utilisateur : deux choix independants. Resultat : conforme.
- [x] Etape 6 : cout 1, 4 + 4 degats, RES B. Resultat : vert.
- [x] Etape 7 : Shield Toss 4 + 4 + 4 = 12 sur Rhino, Major Victory incline ; rouge 1/1 sans module.
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine ; la branche « deux ennemis differents » n'est pas testee (le cas vise le meme ennemi).

### mv008 : Psychic Link (evenement, x2)

- [x] Etape 2 : `04049` Clear the Area.
- [x] Etape 5 : « each player who controls a GUARDIAN character » (`ControleUnGardien`, tous les joueurs). Resultat : conforme.
- [x] Etape 6 : cout 3, 5 menaces, 1 carte, RES B. Resultat : vert.
- [x] Etape 7 : menace 6 -> 1, une carte piochee ; rouge 1/1 sans module.
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine ; le cas d'un joueur SANS Guardian (qui ne pioche pas) n'existe pas (multijoueur).

### mv009 : Victory's Command (evenement, x2)

- [x] Etape 2 : `49019` You Got This! (`WhenUnitUseBasicPower`, `powers=["THW","ATK"]`) + `GainValue` (sender_unit.py).
- [x] Etape 5 : « a friendly character » (`Friend`) ; « basic thwart or attack » (ni DEF ni REC) ; « +2 to that basic power » ; « Ready that character ». Resultat : conforme.
- [x] Etape 6 : cout 1, +2, RES R. Resultat : vert.
- [x] Etape 7 : attaque de base ATQ 1 + 2 = 3 degats, heros redresse, bouclier incline ; contre de base du heros 2 + 2 = 4 ; contre de l'alliee Nikki 2 + 2 = 4, redressee, 2 degats consequents ; rouges 3/3 sans module.
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine. (Les branches THWART et ALLIEE ont maintenant leur cas : contre du heros 2 + 2 = 4 ; Nikki 2 + 2 = 4 et redressee ; rouges 3/3 sans module.)

### mv010 : * The Captain America (soutien)

- [x] Etape 2 : `32020` The X-Jet + `16142` Milano (`AnyPlayerCanDoThis`).
- [x] Etape 5 : « a player who controls a GUARDIAN character » ; « Resource » nu (deux formes) ; « [wild] ». Resultat : conforme, avec l'ecart note en tete.
- [x] Etape 6 : cout 2, 1 ressource wild, RES Y. Resultat : vert.
- [x] Etape 7 : Founder (cout 2) payee grace au vaisseau seul ; temoin alter-ego : Founder reste en main et le vaisseau pret ; rouge 1/2 sans module (le temoin reste vert, voulu).
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine ; multijoueur non teste.

### mv011 : * Nikki (Nicholette Gold), alliee

- [x] Etape 2 : `17013` Yondu (`UnitAttackGainKeyword("This", ranged=True)`) ; `cd002a` (`ThisCanAttack(canbe_divided=True)`). Un module qui declare `ATK` REMPLACE l'attaque par defaut de l'allie (ally.py:33).
- [x] Etape 5 : « ranged » (ignore la riposte) ; « divided among enemies as you choose ». Resultat : conforme.
- [x] Etape 6 : cout 3, PV 3, ATK 2*, THW 2**, RES G (`desc`). Resultat : vert.
- [x] Etape 7 : Whiplash (Retaliate 1) : Nikki ne subit que 1 degat consequent ; repartition 1 + 1 sur deux ennemis ; rouges 2/2 sans module.
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine ; ATQ 2 = 2 choix de cible : verifier a la main que l'interface propose bien le choix repete.

### mv012 : Damaged Containment Suit (obligation de Vance Astro)

- [x] Etape 2 : carte(s) de reference : `rg012` Caged Bird (chercher une carte nommee OU QU'ELLE SOIT, la glisser sous l'obligation, Alter-Ego Action qui la sort) ; `dt094` Diversion Skill (`WhenUnitWouldTakeDamage` + `IncreaseDamage`) ; `03008` Captain America's Helmet (`SetHealth(1)`) ; `60060` (`GetGaveToPlayer()` pour une obligation).
- [x] Etape 5 : mots-pieges verifies : « Forced Interrupt » (avant les degats) ; « when YOU would take ANY amount of damage » (toute source, identite du porteur, PAS `is_from_attack`) ; « 1 ADDITIONAL » (on ajoute) ; « Find » (main, deck, defausse, zone du joueur ET jeu : le costume peut etre porte) ; « tuck it HERE » (face cachee) ; « reduced to 0 or less THIS WAY » (seulement le depart du costume : cadran pose a 3 avant, 3 - 2 = 1) ; « Alter-Ego Action ... exhaust Vance Astro » ; le costume part en MAIN AVANT que l'obligation quitte le jeu (lecon rg012). Resultat : conforme apres la correction du filtre `GetGaveToPlayer`.
- [x] Etape 6 : nombres texte <-> code : boost 2 (deux icones, scan), +1 degat, +2 PV du costume (`BONUS_PV_COSTUME`), PV remis a 1. Resultat : vert.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : degat en plus (3 indirects -> 4) ; costume du DECK glisse sous l'obligation ; costume PORTE glisse (identite a 10 sur 10 sans degat) ; PV restants a 1 avec costume (11 degats sur 12) -> reste en vie a 1 PV (9 degats sur 10) ; TEMOIN 5 degats -> 5 sur 10, pas remis a 1 ; Action d'alter-ego : costume en main, obligation hors jeu, identite inclinee. Rouges 6/6 sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : l'obligation est en jeu dans les 144 journaux, 0 exception.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (le costume glisse face cachee) ; cas plateau `major-victory-plateau.test.ts`, vert.
Carte terminee : NON : partie reelle humaine. Obligation donnee a UN joueur : le cas multijoueur (« give to the Vance Astro player ») n'est pas teste.

### mv013 : * Michael Korvac (sbire nemesis)

- [x] Etape 2 : `21177` Enchantress (`Search.EncounterCard(.., include_set_aside=True)`) ; `10027` Total Destruction (`ThreatCannotBeRemovedFromWhile`).
- [x] Etape 5 : Villainous/Retaliate dans `desc` ; « threat cannot be removed » imprime sur Korvac (dure tant qu'il est en jeu) ; « find and reveal ». Resultat : conforme.
- [x] Etape 6 : PV 8, ATK 2, SCH 2, boost 4, retaliate 1. Resultat : vert.
- [x] Etape 7 : revelation -> Future EN JEU ; menace de la Future inchangee (4) avec Korvac ; temoin sans Korvac : 0 ; rouges 2/3 sans module (temoin voulu).
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : OUI (la Future entre en jeu) ; cas plateau `major-victory-plateau.test.ts`, vert.
Carte terminee : NON : partie reelle humaine, plateau.

### mv014 : Korvac's Future (complot annexe)

- [x] Etape 2 : `st005b`/`04165` + `sk138` (`change_on_event=OnEvent.Threat("This")`) ; `ra029`/`wt018` (`AfterSchemePlaceThreat(.., has_at_least_threat=N)`, `Worlds.SetGameOver(False, ..)`).
- [x] Etape 5 : « 4 OR MORE » (seuil atteint) ; « each hero identity » ; « at least 14 » ; « AFTER threat is placed here ». Resultat : conforme apres correction du recalcul.
- [x] Etape 6 : menace initiale 4, boost 3, -1, 14. Resultat : vert.
- [x] Etape 7 : 4 menaces -> -1 ; temoin 3 menaces -> 0 ; 14 -> defaite ; temoin 13 -> la partie continue ; rouges 2/4 sans module (temoins voulus).
- [x] Etape 7 bis : NON. Etape 8 : autoplay. Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine ; defaite a 14 verifiee par le moteur, pas par un humain. « Permanent » lu dans `desc` sans cas dedie.

### mv015 : Judgment of Korvac (trahison, x2)

- [x] Etape 2 : `mw013` (`ChooseAbilities`, `TakeIndirectDamage`) ; `mf017` (`ThisCardGainSurge`) ; `sk113` (`message.GainBoostIcon`).
- [x] Etape 5 : « OR » (le joueur choisit ; si la Future n'est pas en jeu, seule la branche degats est possible) ; surge UNIQUEMENT avec la menace (decision utilisateur) ; Boost : defenseur = `message.against_player`. Resultat : conforme.
- [x] Etape 6 : boost 1 + [star] ; 3 degats ; 2 menaces ; +2 icones. Resultat : vert.
- [x] Etape 7 : sans Future : 3 degats indirects ; avec Future, branche menace : 6 menaces, 0 degat (deck vide) ; boost sans Future : 3 degats ; boost avec Future, branche menace : menace 6 et 1 degat ; surge mesure directement (sbire revele / reste dans le deck) ; rouges 6/6 sans module.
- [x] Etape 7 bis : NON. Etape 8 : autoplay (apparait 1 fois). Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine. (Le surge est maintenant mesure DIRECTEMENT : deck rencontre a un seul sbire connu, revele avec la branche menace, qui reste dans le deck avec la branche degats ; rouges 6/6.)

### mv016 : Accept Perfection (trahison)

- [x] Etape 2 : `21177` (recherche + `Reveal`) ; `07042` Oversized Hands (`DiscardControlCards(.., highest_cost=True)`) ; `mw013` (`ChooseAbilities`).
- [x] Etape 5 : « Peril » dans `desc` ; « Choose: » deux puces ; Korvac revele PUIS 4 menaces ; « highest cost card you control ». Resultat : conforme.
- [x] Etape 6 : boost 2, peril, 4 menaces. Resultat : vert.
- [x] Etape 7 : 1re puce : Korvac et Future en jeu, menace 4 + 4 = 8 ; 2e puce : Nikki (cout 3) defaussee, bouclier (cout 1) reste ; rouges 2/2 sans module.
- [x] Etape 7 bis : NON. Etape 8 : autoplay (apparait 1 fois). Etape 8 bis : NON.
Carte terminee : NON : partie reelle humaine ; egalite de cout non testee.

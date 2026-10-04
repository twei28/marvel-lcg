# PROCESSUS-CARTE.md : les 22 gabarits du pack Conan (cn001a-cn017)

Gate de `CLAUDE.md` : rien n'est terminé sans le gabarit rempli, preuve à
l'appui. Rédigés le 25/09/2026, à la suite du portage complet du héros
(demande du 25/09/2026 : zip « Conan (09-26) », auteur RyCoRan). Journal de
recherche et de décisions : `.planning/todos/2026-09-25-portage-conan.md`.

**Portée.** 22 scripts (`src/cards/pack/conan/{conan,conan_nemesis}/`) :
l'identité à 5 faces (cn001a-e), 11 cartes signature uniques (16
exemplaires, The Cimmerian recto/verso compris), l'obligation, 4 cartes
némésis (5 exemplaires).

## Preuves communes, citées une fois

- **Étape 1** : 22 entrées dans `data/cards.json`, clé `conan`, tranche
  `cn001a`-`cn017` vérifiée libre ; pack déclaré dans `data/sets_info.json`
  (« 177. Custom (Conan) ») et préfixe `cn` dans `tools/prefixes_fanmade.json`
  (`verifier_prefixes.py` : OK pour cn). Empreintes recalculées.
- **Étape 3, deck** : `deck/starter/conan.json` monte (`verifier_tous_les_decks`
  avec `DECK_NOM=conan` : identité cn001b, main 6, deck 9, The Cimmerian en
  jeu). `player_deck` vide, comme tout homebrew sans decklist d'aspect.
- **Étape 4, images** : 22/22 posées (`assets/pics/cn0XX.jpg`, 615 px sur le
  petit côté, qualité 88). Icônes Hazard/Amplify/Boost lues sur les glyphes
  de ChampionsIcons.ttf, pas devinées.
- **Étape 7, cas** : `tools/test_capacites.py`, filtre `"cn0"` sur
  `.game-src-par9` : **49/49 verts** (relance du 25/09/2026 au soir).
  **Substitution formelle** (`tools/substituer_pack.py ... cn0`) : **21/22
  cartes avec au moins un cas rouge sans leur module**. cn009 (module vide
  par construction) est prouvée par substitution MANUELLE du helper
  `CitadelleEnVitrine` : 3/4 rouges, le témoin restant vert comme il se
  doit ; fichier restauré à l'identique (md5). Les verts résiduels de cn013
  (Uses lus dans `desc`) et cn014 (témoin d'absence) sont attendus.
- **Outils statiques** : `test_cards.py` construit les 22 modules conan sans
  erreur (vérifié par une copie instrumentée, 22 lignes `CONAN_OK`) ;
  `verifier_api_cartes.py` parcourt tout `src/cards` (0 faute conan) ;
  `verifier_appels_modules.py` OK, calibré par un appel inexistant injecté ;
  `audit_cartes.py` ne signale que cn007 (« Action » imprimée, Réponse
  codée), écart voulu par l'arbitrage utilisateur.
- **Étape 8, autoplay** : `tools/autoplay.py .game-src-par9 --deck conan
  --vilains rhino --parties 8` : 0 V / 8 D, **0 bloquée, 0 traceback, 0
  erreur moteur** ; témoin Red Sonja même série : 0 V / 8 D, 0 bloquée.
  Les 17 cartes du pack apparaissent dans les journaux, compteurs Crom
  posés. Le couronnement n'est jamais atteint (parties de 4,9 rounds) : il
  reste couvert par le harnais seul. Un premier passage avait donné 1
  partie bloquée (graine 2) : défaut du PILOTE, pas du pack (voir plus bas).
- **Étape 8 bis, plateau** : portée volontairement limitée. Les compteurs
  `crom` et `serpent` passent par le mécanisme générique des compteurs,
  déjà rendu en production. Ce qui est neuf et testé : leurs noms français
  (`ui-app/src/board/compteurs-fr.ts`, « Crom », « serpent »,
  `compteurs-fr.test.ts` 6/6), les 22 textes FR (`textes-fr-fanmade.ts`) et
  la bio (`heros-info.js`). **Hors de portée** : aucune capture d'écran, et
  le retournement de l'identité vers King Conan n'a pas été regardé dans un
  navigateur.
- **Moteur, ajouts génériques** (additifs, sans effet sur les autres packs) :
  drapeau de face `hors_pile_identite` respecté par `player_setup.py`,
  `GetAllIdentityFace` et `identity.py` (ChangeToOtherHeroForm,
  ChangeToOtherForm) ; compteurs `crom`, `serpent` et traits ADVENTURER,
  CIMMERIA, PIRATE, BARBARIAN déclarés dans `card_face.py`.
- **Défaut de pilote trouvé et corrigé** (`tools/autoplay.py`) : un « Play »
  impayable à cible obligatoire (plage [1, 1]) était rejoué « par prudence »
  au lieu d'être décliné. Main réduite à cn003, coût 1, `payment` vide : la
  même question revenait et la partie finissait « bloquée ». Une carte
  n'est jamais imposée : le pilote passe désormais. Le moteur, lui, refuse
  bien le jeu (cas `cn003 ... sans KING ni ressource ... la carte reste en
  main`, vert).
- **Arbitrages utilisateur du 25/09/2026**, cités une fois : (1) seuils
  « in a phase » cumulés PAR cible ; (2) cn007 jouée en Hero Response après
  une défense, une carte « (defense) » comptant comme défendre (Rules
  Reference v1.8) ; (3) le couronnement garde le côté (héros ou alter-ego)
  et n'est pas un changement de forme.

---

## cn001a : * Conan the Thief (face héros)

- [x] **Étape 2 : références** : `AfterSchemeRemoveThreat`, helper
      `FranchitLeSeuil` (cumul par manigance et par phase).
- [x] **Étape 5 : mots-pièges** : « you remove » exclut Bêlit ; « in a
      phase » cumulatif par cible (arbitrage 1).
- [x] **Étape 6 : nombres** : THW 2 / ATK 1 / DEF 2, 11 PV, main 5, seuil 4.
- [x] **Étape 7 : cas** : `cn001a Rogue's Intuition` (2+2 menaces, 1 Crom).
      Substitution 1/1 rouge.
- [ ] **Étape 7 bis : limite imprimée ?** NON (une fois par manigance et
      par phase, porté par le seuil).
- [x] **Étape 8 : autoplay** : FAIT.
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn001b : * Conan (alter-ego de départ)

- [x] **Étape 2 : références** : 26001b Vision (`SetupPutIntoPlay` recto
      verso), 04001b Clint Barton (`SetCost(Cost("1"))`).
- [x] **Étape 5 : mots-pièges** : « Set King Conan aside » : drapeau
      `hors_pile_identite` ; « Limit once per round ».
- [x] **Étape 6 : nombres** : REC 3, main 6, coût 1 ressource, 1 Crom.
- [x] **Étape 7 : cas** : Setup, Action, témoin d'épuisement. Substitution
      3/3 rouges.
- [x] **Étape 7 bis : limite imprimée ?** OUI, témoin `TEMOIN D'EPUISEMENT`.
- [x] **Étape 8 : autoplay** : FAIT (« Savage_Vitality » dans les journaux).
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn001c : * Conan the Barbarian (face héros)

- [x] **Étape 2 : références** : `AfterUnitTookDamage` (`took_damage`, la
      Toughness n'est pas « dealt »), `FranchitLeSeuil`.
- [x] **Étape 5 : mots-pièges** : « you deal » exclut Bêlit ; cumul par
      ennemi (arbitrage 1).
- [x] **Étape 6 : nombres** : THW 1 / ATK 2 / DEF 2, seuil 5.
- [x] **Étape 7 : cas** : 2+2+2 dégâts, et témoin « 10 dégâts ne donnent
      qu'1 compteur ». Substitution 2/2 rouges.
- [ ] **Étape 7 bis : limite imprimée ?** NON (témoin de plafond fait quand
      même).
- [x] **Étape 8 : autoplay** : FAIT (« Born_of_Battle »).
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn001d : * King Conan (face héros)

- [x] **Étape 2 : références** : `AfterUnitUseBasicPower(..., powers="Hero")`.
- [x] **Étape 5 : mots-pièges** : « a basic power » : ATK, THW, DEF.
- [x] **Étape 6 : nombres** : 2 / 2 / 3, 2 Crom.
- [x] **Étape 7 : cas** : `cn001d Crown of Aquilonia`. Substitution 1/1.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT (face jamais atteinte en partie,
      couverte par le harnais).
- [ ] **Étape 8 bis : plateau** : non regardé dans un navigateur (réserve
      commune).

**Carte terminée : OUI**

---

## cn001e : * Conan (alter-ego roi)

- [x] **Étape 2 : références** : 12001b Scott Lang (`to_this_form=True`),
      44043 Bob (`ChooseAbilities`).
- [x] **Étape 5 : mots-pièges** : le couronnement n'est pas « change to this
      form » (arbitrage 3) ; « heal King Conan » soigne l'identité.
- [x] **Étape 6 : nombres** : REC 3, main 6.
- [x] **Étape 7 : cas** : option soin, option Tough. Substitution 2/2.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT (harnais seul pour la face).
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn002 : Bêlit (alliée signature)

- [x] **Étape 2 : références** : 26001b Vision (`ThisGainKeyword` avec
      `change_on_event`), 44043 Bob (`AfterCardEnterPlay`).
- [x] **Étape 5 : mots-pièges** : « you have the trait » : trait de
      l'identité ; `OnEvent.Faceup` pour le couronnement sans changement de
      forme.
- [x] **Étape 6 : nombres** : coût 3, THW 1* / ATK 1*, 3 PV.
- [x] **Étape 7 : cas** : Voleur, Barbare, Roi. Substitution 3/3.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT (« Play:Ally »).
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn003 : Crush Your Enemies (événement, x2)

- [x] **Étape 2 : références** : 60023 Know Your Enemy (`DiscountAbility`),
      rs006 Hyrkanian Fury (attaque ciblée).
- [x] **Étape 5 : mots-pièges** : « if you are King Conan » : face cn001d.
- [x] **Étape 6 : nombres** : coût 1*, 3 dégâts, 4 en roi.
- [x] **Étape 7 : cas** : Barbare 3, Roi 4 gratuite, témoin Discount, état
      de la graine 2. Substitution 2/2.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT, après correction du pilote.
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn004 : Reaper's Cleave (événement, x2)

- [x] **Étape 2 : références** : 60023 (`DiscountAbility`, contre ciblé).
- [x] **Étape 5 : mots-pièges** : comme cn003.
- [x] **Étape 6 : nombres** : coût 1*, 2 menaces, 3 en roi.
- [x] **Étape 7 : cas** : Voleur 2, Roi 3 gratuite. Substitution 2/2.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT.
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn005 : Destroyer's Defiance (événement, x2)

- [x] **Étape 2 : références** : rs005 Devil's Defiance.
- [x] **Étape 5 : mots-pièges** : « any amount of damage » : pas seulement
      une attaque ; « (defense) » fait de l'identité le défenseur.
- [x] **Étape 6 : nombres** : coût 1*, 1 Crom, 2 en roi.
- [x] **Étape 7 : cas** : Rhino attaque 1 Crom, Roi 2 Crom. Substitution 2/2.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT.
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn006 : Hyborian Havoc (événement, x2)

- [x] **Étape 2 : références** : 44043 Bob (`ChoisirDegatsOuMenace`), bk004
      (`SetLabel('attack', 'thwart')`).
- [x] **Étape 5 : mots-pièges** : « an enemy » : un ennemi choisi, pas
      forcément la cible.
- [x] **Étape 6 : nombres** : coût 3, 5 dégâts ou 4 menaces.
- [x] **Étape 7 : cas** : Voleur, Barbare, Roi. Substitution 3/3.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT.
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn007 : Cimmerian Counter (événement, x2)

- [x] **Étape 2 : références** : `AfterUnitDefendAgainstAttack`, pt005
      Covered Fire.
- [x] **Étape 5 : mots-pièges** : texte contradictoire, arbitrage 2.
- [x] **Étape 6 : nombres** : coût 1*, valeurs courantes ATK/THW.
- [x] **Étape 7 : cas** : défense de base, défense par carte (cn005).
      Substitution 2/2.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT (« Hero_Response »).
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI** (signalement `audit_cartes` voulu)

---

## cn008 : Savage Sword (événement)

- [x] **Étape 2 : références** : `CostFunc.Exhaust("YourIdentity")`
      (60122-60125), `ChoisirDegatsOuMenace`.
- [x] **Étape 5 : mots-pièges** : total THW+ATK+DEF courant.
- [x] **Étape 6 : nombres** : coût 4*.
- [x] **Étape 7 : cas** : Barbare incliné, 5 dégâts. Substitution 1/1.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT.
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn009 : * The Scarlet Citadel (manigance annexe joueur)

- [x] **Étape 2 : références** : recette §3bis (leçon rs009, carte en
      vitrine inerte) ; bonus portés par les faces héros
      (`CapacitesCitadelle`).
- [x] **Étape 5 : mots-pièges** : « ignore the patrol / guard keyword ».
- [x] **Étape 6 : nombres** : coût 0, menace 5, Victory 0.
- [x] **Étape 7 : cas** : Voleur +1 THW, Barbare +1 ATK, témoin hors
      vitrine, Garde ignorée. Substitution automatique 0/4 attendue (module
      vide) ; manuelle 3/4, témoin vert.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT (« Play:PlayerSideScheme »).
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn010 : Savage Tales (ressource)

- [x] **Étape 2 : références** : rs010 She Devil with a Sword.
- [x] **Étape 5 : mots-pièges** : « After you spend this card ».
- [x] **Étape 6 : nombres** : RES physique + énergie, 1 Crom, 2 en roi.
- [x] **Étape 7 : cas** : payer 1 Crom, Roi 2 Crom. Substitution 2/2.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT.
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn011 : * Atlantean Sword (amélioration)

- [x] **Étape 2 : références** : rs012 Bloodmoon Battleaxe, 42001c
      Archangel (`FacesCounter.GetPrintedCost`).
- [x] **Étape 5 : mots-pièges** : « printed cost » : 1 pour un « 1* ».
- [x] **Étape 6 : nombres** : coût 2, Restricted.
- [x] **Étape 7 : cas** : après cn003, 1 dégât de plus, épée inclinée.
      Substitution 1/1.
- [ ] **Étape 7 bis : limite imprimée ?** NON (le coût d'inclinaison en
      tient lieu).
- [x] **Étape 8 : autoplay** : FAIT (« Play:Upgrade »).
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn012a : * The Cimmerian (recto TITLE)

- [x] **Étape 2 : références** : `AfterCounterPlacedOn(..., at_least=8)`,
      helper `Couronner`.
- [x] **Étape 5 : mots-pièges** : « Response » optionnelle ; « Remove your
      other identities » : faces marquées hors pile ; compteurs conservés.
- [x] **Étape 6 : nombres** : 8 Crom.
- [x] **Étape 7 : cas** : alter-ego, héros incliné, anciennes formes hors
      partie, verso attaché. Substitution 3/3 (le 4e cas est postérieur).
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT (Crom posés, seuil jamais atteint).
- [x] **Étape 8 bis : plateau** : nom FR du compteur `crom` testé ; rendu
      du retournement non regardé.

**Carte terminée : OUI**

---

## cn012b : * The Cimmerian (verso KING)

- [x] **Étape 2 : références** : rs002 Conan (`WhenUnitUseBasicPower`,
      `GainValue`), `CostFunc.Counter("This", (1, N), 'crom')`.
- [x] **Étape 5 : mots-pièges** : pouvoirs de base de cn001d seulement ;
      deux coûts payés.
- [x] **Étape 6 : nombres** : X choisi.
- [x] **Étape 7 : cas** : retirer 3 Crom, +3 ATK. Substitution 1/1.
- [ ] **Étape 7 bis : limite imprimée ?** NON (l'inclinaison en tient lieu).
- [x] **Étape 8 : autoplay** : FAIT (harnais seul pour le verso).
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn013 : The Coils of Doom (obligation)

- [x] **Étape 2 : références** : 53029 Harlem's Protector (même forme).
- [x] **Étape 5 : mots-pièges** : « Hero Action » ; « OR » : deux
      capacités, une par coût.
- [x] **Étape 6 : nombres** : Uses 3 serpent, Hazard 1, Boost 2, Victory 0.
- [x] **Étape 7 : cas** : révélée 3 serpents, ressource, Crom.
      Substitution 2/3 (le vert restant lit `desc`, attendu).
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT.
- [x] **Étape 8 bis : plateau** : nom FR du compteur `serpent` testé.

**Carte terminée : OUI**

---

## cn014 : Frozen Ambush (manigance annexe némésis)

- [x] **Étape 2 : références** : `AfterUnitChangeForm(ForcedResponse,
      Identity)`.
- [x] **Étape 5 : mots-pièges** : « an identity » : tous les joueurs ; le
      couronnement ne pose rien (arbitrage 3).
- [x] **Étape 6 : nombres** : menace 4, Amplify 1, Boost 3, +2 menaces.
- [x] **Étape 7 : cas** : changement de forme, témoin couronnement.
      Substitution 1/2 (témoin d'absence vert, attendu).
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT.
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn015 : * Hrothgar (sbire némésis)

- [x] **Étape 2 : références** : 32147 Magneto's Helmet
      (`AfterUnitMakeBasicAttack`), 11030 Ancient Warrior (Boost).
- [x] **Étape 5 : mots-pièges** : attaque de BASE d'un héros ; la Toughness
      de Hymdul absorbe.
- [x] **Étape 6 : nombres** : SCH 1 / ATK 3 / 5 PV, Toughness, Boost 0.
- [x] **Étape 7 : cas** : dégât à Hymdul, Boost sonné. Substitution 2/2.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT.
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn016 : * Hymdul (sbire némésis)

- [x] **Étape 2 : références** : comme cn015.
- [x] **Étape 5 : mots-pièges** : symétrique de cn015.
- [x] **Étape 6 : nombres** : identiques à Hrothgar.
- [x] **Étape 7 : cas** : dégât à Hrothgar, Boost désorienté. Substitution
      2/2.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT.
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

---

## cn017 : Grapple on the Glacier (traîtrise némésis, x2)

- [x] **Étape 2 : références** : 01114 Klaw (`Search.EncounterCard(...,
      include_discard_pile=True)`), `PutIntoPlay(joueur)`.
- [x] **Étape 5 : mots-pièges** : « Otherwise » : aucun géant trouvé.
- [x] **Étape 6 : nombres** : Boost 2, 4 dégâts.
- [x] **Étape 7 : cas** : géant en défausse, aucun géant. Substitution 2/2.
- [ ] **Étape 7 bis : limite imprimée ?** NON.
- [x] **Étape 8 : autoplay** : FAIT.
- [ ] **Étape 8 bis : plateau** : sans objet.

**Carte terminée : OUI**

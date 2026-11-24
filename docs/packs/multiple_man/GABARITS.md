# Multiple Man (Jamie Madrox) : gabarits PROCESSUS-CARTE, 04/11/2026

Pack `multiple_man` (prefixe `mm`, set 251, auteur Neptune). Scripts : `src/cards/pack/multiple_man/{multiple_man}/` + helpers `multiple_man_commun.py`. Cas : `tools/cas/multiple_man.py` (45). Deck : `deck/starter/multiple_man.json`. Textes FR : `ui-app/src/board/textes-fr-fanmade.ts` (+ copie generee `public/js/traduction/textes-fr-fanmade.js`). Biographie : `heros-info.js` (`mm001a`). Plateau : `ui-app/src/board/multiple-man-plateau.test.ts`. Ecran : `ui-check/tests/multiple-man-ecrans.spec.ts` (`MM_ECRANS=1`, captures `captures/multiple-man`, `captures/multiple-man-en`). Recettes moteur : `RECETTES-MOTEUR.md` §46.

## Source et decisions

- Matiere : zip d'images (PNG 1500x2150) + inserts auteur. Scans EN seuls, aucun scan FR : textes FR ecrits a la main (noms de cartes et de capacites laisses en anglais, precedent `ca`/`rr`).
- Les basiques (`mm025-mm027` Energy/Genius/Strength) et les ressources sont des reskins de cartes reelles ; le set nemesis est Emperor Madrox + Dupes Gone Bad.
- Decisions utilisateur du 04/11 :
  - complots annexes joueur `mm012-mm014` : le glyphe de cout est un **2** (pas un « N ») — cout 2 confirme par l'utilisateur.
  - mm006/mm007 « for each Dupe ally » : les complots annexes « Only a Dupe ally » (mm012-mm014) ne perdent AUCUNE menace par ces evenements (la source est l'evenement, pas un Dupe) — TEMOIN DUPE-SEULEMENT ecrit.
  - mm001b 3e branche (« +1 to all basic powers until the end of the round ») : le bonus RESTE apres un retournement en forme heros dans le meme round.
  - Prepare For Future Tragedy (mm014) : un Dupe qui entre en jeu APRES coup recoit bien Tenace (RRG « Toughness » : accorde a l'entree en jeu).
- Mot-cle maison : trait **DUPLICATE** (porte par les Dupe) ajoute a `CardFace.TRAITS` dans `card_face.py` (SEUL fichier moteur touche). Fiches : `docs/reference/mots-cles/{duplicate,dupe,x-factor}.md`.
- Regle RRG appliquee sans question (consigne « regles a 100 % ») : limite d'allies = 3 (un 4e Dupe en ejecte un) ; « Search » melange le deck ; « Then » exige la resolution de la 1re partie avant la 2e.

### mm001a : Multiple Man (face HEROS)

- [x] Etape 2 : carte(s) de reference : redirection de cible d'attaque : `41028`, `ca022`, `gmw16019` (`WhenUnitWouldAttackUnit` + `ChangeTarget`) ; redirection de degats d'effet : `nt007` (`WhenUnitWouldTakeDamage(HeroInterrupt, "You", ..)` + `PreventDamage("All")`) ; Makin' Dupes : `ar010` (`CostFunc.Discard("YourHandCards")`), `27150` (`CostFunc.Custom`), `Search.PlayerCard(include_player_hand_cards, include_player_discard_cards)` ; bonus en zone de victoire : RECETTES §3bis + `conan/CapacitesCitadelle` (`ThisGainKeyword(.., change_on_event=OnEvent.Victory(..))`).
- [x] Etape 5 : texte-contre-code : « you MAY have it target a Dupe instead » : remplacement FACULTATIF ; l'attaque contre l'identite part sur un Dupe via `ChangeTarget`, mais la cible du Dupe est un `SetTarget(range=(0, 1))` DECLINABLE (sans cible : rien n'est redirige, ce qui laisse `He's Got This` se declencher). Les DEGATS d'effet (hors attaque) sur l'identite sont prevenus puis infliges au Dupe. Les effets SANS degats (soins, statuts) ne sont pas portes. « Your Hero/Identity » : la face heros porte la capacite (forme heros seulement). Makin' Dupes : UNE capacite (`LimitOncePerRound` natif), couts = defausser 1 carte (toujours) + epuiser Multiple Man via `CostFunc.Custom` SAUF si Madrox Prime est en zone de victoire. Bonus continus (+1 ATQ/THW/DEF, trait S.H.I.E.L.D.) lus dans la zone de victoire (`OnEvent.Victory`). Chiffres : PV 9, main 5, THW/ATQ/DEF 1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script.
- [x] Etape 7 : cas (16, incluant les complots annexes mm012-mm014 pour les bonus) : Madrox Prime en zone de victoire → +1 ATQ (+ TEMOIN sans la carte) ; Madrox Agent → +1 THW + trait S.H.I.E.L.D. (+ TEMOIN) ; Prepare For Future Tragedy → +1 DEF ; Dupe entrant apres coup recoit Tenace ; Makin' Dupes met un Dupe du deck en jeu et incline l'identite (+ LIMITE une fois par round + variante « ne s'incline pas » avec Prime en vitrine) ; Dupe a la place : Rhino frappe l'identite, un Dupe encaisse (+ TEMOIN sans Dupe l'identite subit).
- [x] Etape 7 bis : limite imprimee ? OUI (Makin' Dupes, une fois par round) ; temoin : la 2e Action ne met pas de 2e Dupe. Preuve par substitution : rouges 8/11 (les cas verts sans module sont des temoins d'absence).
- [x] Etape 8 : autoplay cible : passe de TOUS les decks (`card_face.py` touche) verte, `multiple_man` monte (deck 34, main 6) ; aucun deck en echec.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : face heros / alter ego, Dupe en jeu, bonus de zone de victoire ; cas Vitest `multiple-man-plateau.test.ts` + captures Chromium FR et EN.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### mm001b : Jamie Madrox (face ALTER-EGO)

- [x] Etape 2 : carte(s) de reference : `mystique/my001b` (`WhenInYourPlayTurn(AbilityType.Action, op).LimitOncePerRound()` sur l'identite) ; choix multi-branches : `AskChoose`/`preferer_option` ; retrait de menace : `RemoveThreat` ; bonus temporaire : `GainUntilRoundEnd(effect, attack=1, thwart=1, defense=1)`.
- [x] Etape 5 : texte-contre-code : « Action » (forme alter-ego) « Limit once per round ». « Discard a Dupe Ally from play, THEN choose 1 » : la defausse d'un Dupe est un prerequis (RRG « Then ») — sans Dupe l'Action n'est pas offerte. Branches : soin 2 sur Jamie ; retire 2 menaces d'une manigance (source = Jamie, donc une manigance « Only a Dupe ally » n'est PAS affectee) ; +1 a tous les pouvoirs de base de Multiple Man et de chaque Dupe jusqu'a la fin du round (survit au retournement en heros). Chiffres : PV 9, REC 3, main 6.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script.
- [x] Etape 7 : cas (5) : branche 1 soigne 2 degats ; branche 2 retire 2 menaces d'une manigance ordinaire (+ TEMOIN DUPE-SEULEMENT : rien sur Prepare For Future Tragedy) ; SANS Dupe l'Action n'est pas offerte (aucun soin) ; branche 3 +1 pouvoirs de base et reste apres retournement.
- [x] Etape 7 bis : limite imprimee ? OUI (Reabsorb Dupe, une fois par round). Preuve par substitution : rouges 3/5 (les verts sont des temoins d'absence).
- [x] Etape 8 : autoplay cible : passe de TOUS les decks verte (voir mm001a).
- [x] Etape 8 bis : OUI (voir mm001a).

Carte terminee : OUI : sous reserve de la gate de heros.

### mm002 à mm005 : Dupe (quatre allie·e·s, trait DUPLICATE, meme texte, ressource imprimee differente)

- [x] Etape 2 : carte(s) de reference : `21006` (`CanGenerateResources(.., resources_fn=..)` + `GetPrintedResources`) ; `card_class="IdentitySpecific"` pour la restriction « identity-specific card ».
- [x] Etape 5 : texte-contre-code : « Separate Lives — Action : Exhaust this card → generate its PRINTED resource to pay for an IDENTITY-SPECIFIC card. » La ressource generee est la ressource imprimee (mm002 = mental, mm003 = physical, mm004 = energy, mm005 = wild/selon le PNG) et ne paie QUE les cartes propres a l'identite (pas une carte d'aspect). Chiffres : cout 2, PV 3, ATQ 1*, THW 1*.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script.
- [x] Etape 7 : cas (2, portes par mm002) : le Dupe paie Kinetic Absorption Suit (carte propre a l'identite, cout 1) → elle entre en jeu, le Dupe s'incline ; TEMOIN : la meme ressource ne paie PAS Noble Sacrifice (49018, carte d'aspect) → elle reste en main.
- [x] Etape 7 bis : limite imprimee ? NON. Preuve par substitution : mm002 rouges 1/2 (le TEMOIN reste vert par construction) ; mm003-mm005 identiques (pas de cas propre : reskins verifies par la passe de decks et l'audit).
- [x] Etape 8 : autoplay cible : passe de TOUS les decks verte.
- [x] Etape 8 bis : OUI (allies en jeu) ; captures Chromium FR et EN.

Carte terminee : OUI.

### mm006 / mm007 : Someone's Got This (evenement thwart, meme texte)

- [x] Etape 2 : carte(s) de reference : `ca010`, `lj019` (retrait de menace + « for each … in play »).
- [x] Etape 5 : texte-contre-code : « Remove 2 threat from a scheme. Then, remove 1 threat from EACH scheme in play FOR EACH Dupe ally in play. » 2 menaces sur la manigance ciblee, puis 1 par Dupe sur CHAQUE manigance. Une manigance « Only a Dupe ally » n'est pas retiree par cet evenement (source = l'evenement). Chiffres : cout 2.
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : cas (3, portes par mm006) : 2 Dupe → 6 → 2 sur le complot principal ; TEMOIN sans Dupe → 6 → 4 ; TEMOIN DUPE-SEULEMENT → Prepare For Future Tragedy (4) ne perd rien.
- [x] Etape 7 bis : limite imprimee ? NON. Preuve par substitution : mm006 rouges 3/3.
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm008 / mm009 : We've Got This (evenement attack, meme texte)

- [x] Etape 2 : carte(s) de reference : `ca012` (degats + « for each … in play »).
- [x] Etape 5 : texte-contre-code : « Deal 4 damage to an enemy. Then, choose a player and deal 1 damage to the villain AND each enemy engaged with that player FOR EACH Dupe ally in play. » Chiffres : cout 3.
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : cas (2, portes par mm008) : 2 Dupe → 4 degats a Rhino puis +2 au vilain (6) et +2 au sbire engage (Tiger Shark, sans Garde) ; TEMOIN sans Dupe → seulement 4 degats.
- [x] Etape 7 bis : limite imprimee ? NON. Preuve par substitution : mm008 rouges 2/2.
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm010 / mm011 : He's Got This (interruption defense, meme texte)

- [x] Etape 2 : carte(s) de reference : `nt007`, `47028` (prevention d'attaque + mise en jeu depuis deck/main/defausse).
- [x] Etape 5 : texte-contre-code : « Hero Interrupt (defense) : When you take damage from an attack, discard 1 Dupe ally from play → prevent all damage from that attack. Search your deck, hand, and discard pile for a DIFFERENT Dupe ally and put it into play EXHAUSTED. » Depend de la redirection declinable de mm001a (sinon l'attaque part sur le Dupe avant). Chiffres : cout 1.
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : cas (1, porte par mm010) : Rhino frappe l'identite, on defausse mm002 en cout, TOUS les degats prevenus, mm003 (du deck) entre en jeu EPUISE. (cas avec `cibles=['mm002']` pour forcer la redirection a decliner.)
- [x] Etape 7 bis : limite imprimee ? NON. Preuve par substitution : mm010 rouges 1/1.
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm012 / mm013 / mm014 : complots annexes joueur (Madrox Prime / Agent of S.H.I.E.L.D. / Prepare For Future Tragedy)

- [x] Etape 2 : carte(s) de reference : `ThreatCannotBeRemovedFromWhile(by_character=…)` (verrou « Only a Dupe ally ») ; Reponse « After this side scheme is defeated » : `AfterUnitDefeatedScheme`/`WhenSchemeBeDefeated` ; bonus en zone de victoire : voir mm001a.
- [x] Etape 5 : texte-contre-code : « Victory 0. Only a Dupe ally can remove threat from this scheme. » (verrou : ni l'identite ni un effet ne retire de menace). Cout imprime = **2** (glyphe confirme par l'utilisateur). Reponse heros apres defaite : renvoie en main le Dupe qui a vaincu la manigance → soin 2 (mm012) / 2 degats a un ennemi (mm013) / retire 2 menaces d'une AUTRE manigance (mm014). Bonus en zone de victoire : +1 ATQ + Makin' Dupes sans epuiser (mm012) ; +1 THW + trait S.H.I.E.L.D. + limite d'allies +1 (mm013) ; +1 DEF + Tenace pour les Dupe (mm014).
- [x] Etape 6 : nombres : relus (menace initiale 4, victoire 0, cout 2).
- [x] Etape 7 : cas (2 + 1 + 1) : mm012 : TROIS Dupe (limite 3) retirent les 4 menaces, le 1er se redresse pour la 4e, la Reponse renvoie le dernier Dupe en main et soigne 2 ; VERROU : l'identite ne retire aucune menace. mm013 : idem, Reponse → 2 degats a Rhino. mm014 : idem, Reponse → retire 2 menaces d'une autre manigance. (Les bonus de zone de victoire sont couverts par les cas mm001a.)
- [x] Etape 7 bis : limite imprimee ? NON (Victory 0). Preuve par substitution : mm012 rouges 2/2, mm013 1/1, mm014 1/1.
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm015 : Kinetic Absorption Suit (amelioration)

- [x] Etape 2 : carte(s) de reference : `im012` (`WhenUnitWouldTakeDamage` + reduction) ; `Search.PlayerCard` pour la 2e branche.
- [x] Etape 5 : texte-contre-code : « Hero Interrupt : When Multiple Man is dealt damage from an attack, exhaust this card → choose 1 : • Reduce the amount of damage taken by 1. • Search your hand, deck, and discard pile for a Dupe ally and put it into play. (Shuffle.) » Chiffres : cout 1.
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : cas (2) : branche 1 → l'attaque de Rhino inflige 1 degat de moins (le costume s'incline) ; branche 2 → un Dupe du deck entre en jeu.
- [x] Etape 7 bis : limite imprimee ? NON. Preuve par substitution : mm015 rouges 2/2.
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm016 : X-Factor Investigations (soutien)

- [x] Etape 2 : carte(s) de reference : « Alter Ego Response : After … defeats a side scheme » : `AfterUnitDefeatedScheme(ForcedResponse / Response, "You", ..)` + `RemoveThreat` sur le complot principal ; epuisement du soutien.
- [x] Etape 5 : texte-contre-code : « Alter Ego Response : After Jamie Madrox defeats a side scheme, exhaust X-Factor Investigations → remove 3 threat from the main scheme. » Reponse en forme ALTER-EGO seulement. Chiffres : cout 1.
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : cas (2) : Jamie (alter-ego) vainc un complot annexe par Reabsorb Dupe → 3 menaces retirees du complot principal (5 → 2), le soutien s'incline ; TEMOIN : en forme HEROS la Reponse n'existe pas.
- [x] Etape 7 bis : limite imprimee ? NON (epuisement). Preuve par substitution : mm016 rouges 1/2 (le TEMOIN reste vert).
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm017 : Got Duped! (obligation)

- [x] Etape 2 : carte(s) de reference : obligation « Give to … player » + flip alter-ego + recherche dans le deck de rencontre (`Worlds`/`Search` encounter) + mise en jeu d'un sbire.
- [x] Etape 5 : texte-contre-code : « Give to the Jamie Madrox player. You may flip to alter-ego form. Choose : • Exhaust Jamie Madrox → remove Got Duped! from the game. • Discard 1 Dupe ally you control. If no ally was discarded this way, search the encounter deck, encounter discard pile, and set-aside area for a Dupes Gone Bad minion and put it into play. Discard this obligation. » Chiffres : boost 2.
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : cas (3) : branche 1 → Jamie s'incline, l'obligation est RETIREE de la partie ; branche 2 avec Dupe → le Dupe est defausse, aucun sbire, l'obligation defaussee ; branche 2 SANS Dupe → un Dupes Gone Bad est cherche dans le deck de rencontre et entre en jeu engage.
- [x] Etape 7 bis : limite imprimee ? NON. Preuve par substitution : mm017 rouges 3/3.
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm018 : Who's Killing Dupes? (complot annexe nemesis)

- [x] Etape 2 : carte(s) de reference : verrou « Only a Dupe ally » (voir mm012) ; « When Revealed : discard a Dupe ally » : `WhenRevealed` + `Discard`.
- [x] Etape 5 : texte-contre-code : « Only a Dupe ally can remove threat from this scheme. When Revealed : Discard a Dupe ally from play. » Chiffres : menace initiale 3, boost 2, amplify 1.
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : cas (2) : Revelee → un Dupe en jeu est defausse ; VERROU → l'identite ne retire aucune menace (reste a 3).
- [x] Etape 7 bis : limite imprimee ? NON. Preuve par substitution : mm018 rouges 2/2.
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm019 : Emperor Madrox (sbire nemesis)

- [x] Etape 2 : carte(s) de reference : « his attack targets an ally » : `WhenUnitWouldAttackUnit(ForcedInterrupt, Unit2, Unit2, op)` + `ChangeTarget(allie)` ; « Dupe allies may not attack » : `UnitCannotBeAttacked` conditionne au trait DUPLICATE.
- [x] Etape 5 : texte-contre-code : « [star] When Emperor Madrox attacks you, his attack targets an ally you control. Dupe allies may not attack Emperor Madrox. » Chiffres : PV 4, ATQ 3*, SCH 1, boost 2, hazard 1.
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : cas (3) : son attaque contre l'identite cible un ALLIE (Hulk NON-Dupe, pour que la redirection de l'identite ne masque pas celle d'Emperor : Hulk encaisse 3, l'identite rien) ; TEMOIN sans allie → l'attaque frappe l'identite ; un Dupe NE PEUT PAS l'attaquer (reste intact).
- [x] Etape 7 bis : limite imprimee ? NON. Preuve par substitution : mm019 rouges 2/3 (apres isolation par allie NON-Dupe ; le TEMOIN reste vert).
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm020 / mm021 / mm022 : Dupes Gone Bad (sbires nemesis, meme texte)

- [x] Etape 2 : carte(s) de reference : « When Revealed : add 1 threat to each side scheme » + « Boost : add 1 threat to each side scheme » : `WhenRevealed`/`AbilityType.Boost` + `AddThreat` sur chaque complot annexe.
- [x] Etape 5 : texte-contre-code : « When Revealed : Add 1 threat to each side scheme in play. [star] Boost : Add 1 threat to each side scheme in play. » Chiffres : PV 3, ATQ 2, SCH 1, boost 1.
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : cas (1, porte par mm020) : Revelee → 1 menace sur CHAQUE manigance annexe (Bomb Scare 2 → 3). mm021/mm022 identiques (reskins).
- [x] Etape 7 bis : limite imprimee ? NON. Preuve par substitution : mm020 rouges 1/1.
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm023 : Got Your Back (evenement Leadership)

- [x] Etape 2 : carte(s) de reference : « cannot take damage until the end of the round » : `UnitCannotTakeDamageWhile` sur chaque personnage controle ; condition de jeu « control an ally while 3 or fewer HP » : `CanPlayThisCard`.
- [x] Etape 5 : texte-contre-code : « Play only if you control an ally while you have 3 or fewer remaining hit points. Hero Action : Each character you control cannot take damage until the end of the round. » C'est une Action qui pose la prevention AVANT l'attaque. Chiffres : cout 2.
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : cas (2) : avec un allie NON-Dupe (Hulk, pour que la redirection de l'identite ne masque pas l'effet) et 3 PV restants → chaque personnage controle ne subit plus de degats (l'attaque de Rhino ne fait rien, l'allie epuise ne defend pas) ; TEMOIN : avec plus de 3 PV la carte n'est PAS jouable (reste en main).
- [x] Etape 7 bis : limite imprimee ? NON (condition de jeu). Preuve par substitution : mm023 rouges 1/2 (apres correction : jouer la carte puis attaquer via `declencher_apres`, allie NON-Dupe epuise ; le TEMOIN reste vert).
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm024 : Ultimate Teamwork (evenement Leadership)

- [x] Etape 2 : carte(s) de reference : « choose a team trait … they each get +2 ATK » : `GainUntilPhaseEnd`/bonus conditionne au trait choisi + comptage des personnages.
- [x] Etape 5 : texte-contre-code : « Hero Action : Choose a team trait. If you control at least 4 characters that share the chosen team trait, they each get +2 ATK until the end of the phase. » Chiffres : cout 2.
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : cas (2) : 4 personnages partagent un trait (Multiple Man + 3 Dupe : X-FACTOR) → chacun +2 ATQ ; TEMOIN : seulement 3 personnages → aucun bonus.
- [x] Etape 7 bis : limite imprimee ? NON. Preuve par substitution : mm024 rouges 1/2 (le TEMOIN reste vert).
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

### mm025 / mm026 / mm027 : Energy / Genius / Strength (ressources basiques, reskins)

- [x] Etape 2 : carte(s) de reference : ressources basiques reelles « Max 1 per deck » (reskins d'images, pas de script).
- [x] Etape 5 : texte-contre-code : « Max 1 per deck. » Double icone de ressource imprimee (Energy = YY, Genius = BB, Strength = RR).
- [x] Etape 6 : nombres : relus.
- [x] Etape 7 : pas de cas (reskins sans capacite) ; verifies par la passe de decks et `audit_cartes` (0 module en erreur).
- [x] Etape 7 bis : limite imprimee ? OUI imprimee « Max 1 per deck » (regle de deck, pas de capacite). Pas de substitution (pas de module).
- [x] Etape 8 / 8 bis : passe de decks verte ; captures FR/EN.

Carte terminee : OUI.

---

**Portes finales (04/11/2026)** : 45/45 cas verts ; `test_cards` (8233, 0 err) ; `verifier_api_cartes` (9280, 0 faute) ; `audit_cartes` (0 module en erreur) ; passe de TOUS les decks verte (`card_face.py` touche) ; Vitest `multiple-man-plateau.test.ts` (2/2) ; portes FR `traduction-public` + `textes-fr-fanmade` (23/23) + `vocabulaire-statuts` (2/2) ; captures Chromium FR+EN. Preuve par substitution : 16/25 modules a cas tombent au rouge sans eux ; les verts restants sont des temoins d'absence (TEMOIN) verts par construction.

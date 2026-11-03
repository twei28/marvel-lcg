# Mystique (Raven Darkhölme) : gabarits PROCESSUS-CARTE, 02/11/2026

Pack `mystique` (prefixe `my`, set 248, auteur Merlin). Scripts : `src/cards/pack/mystique/{mystique,mystique_nemesis}/` (23 faces). Cas : `tools/cas/mystique.py` (77). Deck : `deck/starter/mystique.json` (`player_deck` VIDE : aucun Extras). Textes FR : `ui-app/src/board/textes-fr-fanmade.ts` (+ copie `public/js/traduction/textes-fr-fanmade.js` regeneree). Biographie : `heros-info.js` (`my001a`). Plateau : `ui-app/src/board/mystique-plateau.test.ts`. Ecran : `ui-check/tests/mystique-ecrans.spec.ts`.

## Source et decisions

- Matiere : EN beta 4.2 + FR Release 1.1.1 (zip de Merlin). **Le FR, plus recent, PRIME quand ils different** (comme pour Destiny) : my005 Friend (« un heros autre que Mystique ou un allie », l'EN disait « a character other than Mystique »), my012 Really? (« redressez Mystique », l'EN disait « draw 1 card »), my013 Unnoticed (la Crise n'est ignoree QUE si Civilian est visible), my007 Infiltration (Garde et Patrouille seulement, plus la Crise), my018 (Incitation 1). my019 Mother and Son! n'existe qu'en FR.
- Scans : `assets/pics/my*.jpg` = scan EN beta, SAUF les 7 faces ci-dessus (my005a/b, my007, my012, my013, my018, my019) dont le scan EN est perime ou absent : leur `pics/` est le scan FR, declare `SCANS_FR_SEULS` (voile anglais, `textes-en-scan-fr.ts`). `assets/pics-fr/fr_my*.jpg` = les 23 scans FR (`SCANS_FR_FANMADE`, aucun voile FR).
- Formes (my003-my005) : amelioration a DEUX faces, `a` = face VISIBLE (capacites), `b` = face CACHEE (meme texte grise, aucune capacite). Mises de cote (`BeginGameWithSetAside(["my003b,my003a",...])`) puis posees face cachee par le Setup de my001b. my002 Shapeshifter : `Permanent` + `Setup` natifs.
- Nemesis : meme trio que Destiny (Mister Sinister, Destiny's Warning, So, What's the Plan? x3) recopie sous my016-my018. **Decouverte** : la branche « deja en jeu » de Sinister ne partait jamais (carte UNIQUE : le moteur defaussait la 2e copie avant son When Revealed) ; corrigee dans my016 ET dy014 par `UniqueRuleNotApplyTo(name=..)`, cas `dy014 ... DEJA en jeu` ajoute.
- « Any player may help pay the cost » (my015) : le cout n'est que d'inclinaisons, aucune ressource a aider ; `cout_en_groupe` pose par fidelite, sans effet visible.
- Un allie * Mystique de Destiny (dy003) ne peut pas entrer en jeu avec le heros * Mystique (carte UNIQUE de meme nom) : voulu ; cas Friend/Mother and Son avec Nightcrawler `32011`.
- Particularites de test : le pilote joue les cartes de la main pendant une interruption : `Puzzle.EmptyHand()` AVANT un `Puzzle.Damage` en forme heros ; `Puzzle.Action` retombe sur le pouvoir de base quand l'Action n'est plus offerte (limite de Fast Heal mesuree par l'inclinaison de l'alter-ego) ; `SetThreat` du harnais est refuse sur Infiltration (source != Mystique) : trois `Puzzle.Thwart` de Mystique la vident ; un deck rencontre de 2 cartes est remelange avec sa defausse (decks de test de 5+ cartes) ; `targets2` ne se lit qu'UNE fois.

### my001a

- [x] Etape 2 : carte(s) de reference : - `hf041` / `hf110` : `Ability(Response, Message.AfterCardFlip, [conditions], op)` pour « after you flip <une AUTRE carte> » (`AfterCardFlipToThisSide` ne vise que la carte elle-meme). - `bm010` Grapple Gun : `UnitIgnoreKeywordIcons(CardFinder(name=..), guard=True, patrol=True)` ; `pd001a` `ActionHonorHuntEnVitrine` : une capacite « en vitrine de victoire » vit sur l'IDENTITE (la carte en vitrine ne declenche jamais ses propres capacites ; RECETTES §3bis), condition = la carte est dans `Worlds.VictoryDisplay`.
- [x] Etape 5 : texte-contre-code : « After YOU flip » : le retournement d'une forme de CE joueur (l'identite de Mystique ne retourne que ses formes). « all shapeshift form upgrades are facedown » : les TROIS formes sont face `b` (apres le retournement). « ready your IDENTITY » : l'identite, pas seulement le heros (forme heros ici de toute facon). « Response » : optionnel (« you may »), jouable en forme heros seulement. Chiffres : PV 10, main 5, ATQ/CTR/DEF 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (8) : la derniere forme visible est retournee cachee : TOUTES cachees, l'identite est REDRESSEE ; TEMOIN : une forme reste VISIBLE (Enemy retournee face visible) : l'identite reste inclinee ; TEMOIN : en forme ALTER-EGO la Reponse de la face heros n'existe pas (l'alter-ego reste incline) ; Mystique ignore GARDE : un sbire Garde (Hydra Mercenary) ne protege plus le vilain ; TEMOIN : sans Infiltration en vitrine, le meme sbire Garde protege le vilain (0 degat) ; Mystique ignore PATROUILLE : un sbire Patrouille (Kree Commando) n'empeche plus de contrer le complot principal ; TEMOIN : sans la carte en vitrine, la Patrouille interdit de contrer le complot principal (menace inchangee) ; la CRISE n'est PAS ignoree (FR 1.1.1) : sous une icone de crise le complot principal reste intouchable. Substitution : **rouges 3/8** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my001b

- [x] Etape 2 : carte(s) de reference : - `36001b` Ororo Munroe (storm) : `BeginGameWithSetAside([...])` + `WhenCardSetup("This", op)` + `face.CastTo(..).PutIntoPlay(joueur, effect)` pour mettre en jeu des cartes mises de cote. - `my002` : Shapeshifter est PERMANENT + `Setup` dans `desc` : le moteur la met en jeu a la mise en place (RECETTES §3 ; `60113a`), sans script ici. - `25024` Godlike Stamina : `HealthUnits` + `components.status.GetDeck()` pour « heal ... or remove a status card from <identite> ».
- [x] Etape 5 : texte-contre-code : « Put all 3 shapeshift form upgrades into play, FACEDOWN » : chaque forme est creee face `b` en premiere face (id « my00Nb,my00Na »), posee en jeu sous le controle du joueur ; AUCUN declenchement « turned faceup ». « Fast Heal » : Action d'alter-ego (pas d'exigence d'exhaustion), « heal 1 damage OR remove a status card » : UN des deux, a la volonte, jamais les deux ; le moteur n'offre une branche que si elle est possible. « from RAVEN DARKHOLME » : l'identite. « Limit once per round » : `LimitOncePerRound`. Chiffres : PV 10, main 6, REC 4, soin 1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (6) : les trois formes sont en jeu FACE CACHEE (b), aucune face visible ; Action : l'alter-ego soigne 1 degat ; Action : retire une carte d'etat (Sonne) de l'alter-ego, sans soigner ; les DEUX branches possibles : on choisit le retrait d'etat, le soin n'a PAS lieu (3 degats restent) ; LIMITE une fois par round : la 2e Action est refusee, le pilote bascule sur le Recover de base (alter-ego INCLINE, 8 - 1 - 4 = 3 degats, et non 6) ; TEMOIN : en forme HEROS la capacite de l'alter-ego n'existe pas (3 degats restent). Substitution : **rouges 5/6** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d epuisement : cas LIMITE / Max 1 ci-dessus, chiffre mesure au second emploi.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : formes a deux faces / carte en vitrine ; cas plateau `mystique-plateau.test.ts` + captures Chromium FR et EN (captures/mystique, captures/mystique-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my002

- [x] Etape 2 : carte(s) de reference : - `21187a` Norn Stone : `WhenInYourPlayTurn(HeroAction, op)` + `this.card.Flip(effect)` ; ici le retournement vise une AUTRE carte (une forme). - `bs002` / `dy002` : amelioration Permanent + Setup, sans script pour l'entree en jeu.
- [x] Etape 5 : texte-contre-code : « Action » nue : jouable aussi en alter-ego (comme les formes). « Exhaust Shapeshifter » : cout. « choose a shapeshift form upgrade » : l'une des trois formes en jeu, visible OU cachee ; « flip that card » : elle change de face (cachee -> visible, mais aussi visible -> cachee). Le declenchement « turned faceup » des formes (retourner les autres) est SUR LES FORMES (my003-my005). Chiffres : aucun cout imprime.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (4) : Shapeshifter est en jeu des la mise en place (Permanent + Setup natifs) ; Action : une forme CACHEE (Civilian) passe face VISIBLE ; Shapeshifter s'incline ; « flip that card » : une forme VISIBLE (Enemy) est retournee face CACHEE ; LIMITE d'inclinaison : Shapeshifter deja inclinee, l'Action n'est pas offerte (la forme reste cachee). Substitution : **rouges 2/4** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : formes a deux faces / carte en vitrine ; cas plateau `mystique-plateau.test.ts` + captures Chromium FR et EN (captures/mystique, captures/mystique-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my003a

- [x] Etape 2 : carte(s) de reference : - `26002b` Dense (vision) : amelioration a deux faces qui reagit au changement de forme ; `hf041` / `state.py` : `AfterCardFlipToThisSide` pour « when THIS card is turned faceup ». - `01037` Mark V Helmet : `this.RemoveThreatFromSchemes(effect.targets, n, effect)` + `.SetTarget(Scheme2)` (cible de manigance). `Faces.ReadyAll` / `CostFunc.Exhaust("This")` (`my002`).
- [x] Etape 5 : texte-contre-code : « Exhaust Civilian » : cout de l'Action (inclinaison de CETTE carte). « WHEN THIS CARD IS TURNED FACEUP » : le retournement de b vers a, pas la mise en jeu (la forme entre en jeu face cachee). « flip EACH OTHER form FACEDOWN » : les deux autres formes visibles passent face cachee (celles deja cachees ne bougent pas) ; la forme qui vient d'etre retournee reste visible. Face cachee (`b`) : aucune capacite. Chiffres : aucun cout, aucun nombre hors « 1 threat, 1 scheme ».
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (2) : Action : retire 1 menace d'une manigance (3 -> 2) ; Civilian s'incline ; Reponse forcee : retournee face VISIBLE, elle retourne la forme Enemy (visible) face CACHEE. Substitution : **rouges 2/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : formes a deux faces / carte en vitrine ; cas plateau `mystique-plateau.test.ts` + captures Chromium FR et EN (captures/mystique, captures/mystique-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my003b

- [x] Etape 2 : carte(s) de reference : face cachee : aucune capacite ; meme gabarit que la face visible (voir my003a)
- [x] Etape 5 : texte-contre-code : face cachee : aucun texte actif
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (1) : AUCUNE capacite : l'Action ne retire rien (menace inchangee). Substitution : **rouges 0/1** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : formes a deux faces / carte en vitrine ; cas plateau `mystique-plateau.test.ts` + captures Chromium FR et EN (captures/mystique, captures/mystique-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my004a

- [x] Etape 2 : carte(s) de reference : - `26002b` Dense (vision) : amelioration a deux faces qui reagit au changement de forme ; `hf041` / `state.py` : `AfterCardFlipToThisSide` pour « when THIS card is turned faceup ». - `27182a` Compact Darts : `this.DealDamage(effect.targets, 1, effect)` + `.SetTarget(Enemy)`.
- [x] Etape 5 : texte-contre-code : « Exhaust Enemy » : cout de l'Action (inclinaison de CETTE carte). « WHEN THIS CARD IS TURNED FACEUP » : le retournement de b vers a, pas la mise en jeu (la forme entre en jeu face cachee). « flip EACH OTHER form FACEDOWN » : les deux autres formes visibles passent face cachee (celles deja cachees ne bougent pas) ; la forme qui vient d'etre retournee reste visible. Face cachee (`b`) : aucune capacite. Chiffres : aucun cout, aucun nombre hors « 1 damage, 1 enemy ».
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (2) : Action : 1 degat a un ennemi (Rhino) ; Enemy s'incline ; Reponse forcee : retournee face VISIBLE, elle retourne la forme Friend (visible) face CACHEE. Substitution : **rouges 2/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : formes a deux faces / carte en vitrine ; cas plateau `mystique-plateau.test.ts` + captures Chromium FR et EN (captures/mystique, captures/mystique-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my004b

- [x] Etape 2 : carte(s) de reference : face cachee : aucune capacite ; meme gabarit que la face visible (voir my003a)
- [x] Etape 5 : texte-contre-code : face cachee : aucun texte actif
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (1) : AUCUNE capacite : l'Action n'inflige rien (Rhino intact). Substitution : **rouges 0/1** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : formes a deux faces / carte en vitrine ; cas plateau `mystique-plateau.test.ts` + captures Chromium FR et EN (captures/mystique, captures/mystique-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my005a

- [x] Etape 2 : carte(s) de reference : - `23016` Command Team : `Action` + `CostFunc.Exhaust("This")` + `Faces.ReadyAll(cibles, effect)` pour « ready an ally » ; la cible « hero OU ally » ne s'exprime pas par un seul `SetTarget` : choix dynamique par `joueur.AskChooseFace` (modele `my002`). - `26002b` Dense (vision) / `state.py` : `AfterCardFlipToThisSide` pour « when THIS card is turned faceup ».
- [x] Etape 5 : texte-contre-code : « ready a HERO OTHER THAN MYSTIQUE or an ALLY » : un heros (identite en forme heros) de n'importe quel joueur autre que Mystique, ou un allie de n'importe quel joueur ; jamais l'alter-ego, jamais Mystique. Seules les cartes INCLINEES sont proposees (redresser une carte prete n'est pas un effet). « Exhaust Friend » : cout. « WHEN THIS CARD IS TURNED FACEUP » : le retournement de b vers a, pas la mise en jeu. Chiffres : aucun.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (4) : Action : redresse un ALLIE incline ; Friend s'incline ; Action : redresse le HEROS d'un AUTRE joueur (Spider-Man) ; TEMOIN : Mystique elle-meme n'est pas redressable (seule candidate : l'Action n'est pas offerte, Friend reste prete) ; Reponse forcee : retournee face VISIBLE, elle retourne la forme Civilian (visible) face CACHEE. Substitution : **rouges 3/4** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : formes a deux faces / carte en vitrine ; cas plateau `mystique-plateau.test.ts` + captures Chromium FR et EN (captures/mystique, captures/mystique-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my005b

- [x] Etape 2 : carte(s) de reference : face cachee : aucune capacite ; meme gabarit que la face visible (voir my003a)
- [x] Etape 5 : texte-contre-code : face cachee : aucun texte actif
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (1) : AUCUNE capacite : l'Action ne redresse rien (Nightcrawler reste incline). Substitution : **rouges 0/1** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : formes a deux faces / carte en vitrine ; cas plateau `mystique-plateau.test.ts` + captures Chromium FR et EN (captures/mystique, captures/mystique-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my006

- [x] Etape 2 : carte(s) de reference : - `dy001a` Destiny (hero) : `WhenBoostCardTurnedFaceUp(Interrupt, None, op, ..)` + `LimitOncePerPhase` ; `sender_card.py` (`WhenBoostCardTurnedFaceUp.boost_icons`, `CancelBoostIcons`) pour remplacer le compte d'icones de la carte retournee. - `53004` Bird's Eye View : `Worlds.GetEncounterDeck(effect).GetTop()` + `Faces.DiscardAll` pour « discard the top card of the encounter deck ».
- [x] Etape 5 : texte-contre-code : « during a SCHEME activation » : `while_scheme=True` (jamais une attaque). « discard the top card of the encounter deck » : TOUJOURS, meme si le joueur ne compte pas ses icones (il n'y a pas de « may » sur la defausse). « You MAY count the number of boost ICONS on THAT card INSTEAD » : option ; le compte d'icones de la carte retournee est REMPLACE par celui de la carte defaussee (icones numeriques seulement, pas l'effet [star]), qui reste applique. « Limit once per phase » : `LimitOncePerPhase`. Deck Rencontre vide : rien n'est defausse, la capacite n'a pas d'effet. Chiffres : cout 3, PV 2, CTR 1, ATQ 1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (5) : manigance de Rhino, boost 0 icone, la carte du dessus (Shocker, 2 icones) est defaussee ET ses icones comptent : menace 1 + SCH 1 + 2 = 4 ; TEMOIN sans Destiny : la meme manigance ne rapporte que SCH 1 + 0 icone (menace 1 + 1 = 2) et Shocker reste dans le deck ; « You MAY count » refuse : la carte du dessus est defaussee quand meme, mais ses icones ne comptent pas (menace 1 + 1 = 2) ; « during a SCHEME activation » : pendant une ATTAQUE de Rhino elle ne se declenche pas (le dessus du deck reste dans le deck) ; LIMITE une fois par phase : deux manigances dans la meme phase, la 2e ne declenche plus rien (Shocker ET la carte de boost 01107 en defausse ; Sandman, 4e carte, reste dans le deck). Substitution : **rouges 3/5** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d epuisement : cas LIMITE / Max 1 ci-dessus, chiffre mesure au second emploi.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my007

- [x] Etape 2 : carte(s) de reference : - `40006` Technovirus Purge (cable) : `ThreatCannotBeRemovedFromWhile("This", by_character=CardFinder(non_name=..))` pour « characters other than X cannot remove threat from this card ». - `42017` Render Medical Aid : `WhenSchemeBeDefeated(WhenDefeated, "This", op)` sur une manigance annexe de joueur. - la capacite « en vitrine de victoire » est posee sur l'IDENTITE (`my001a`, RECETTES §3bis) : le script de cette carte ne la porte pas.
- [x] Etape 5 : texte-contre-code : « Characters OTHER THAN MYSTIQUE cannot remove threat » : seuls les effets dont la source est Mystique retirent de la menace (Unnoticed, Civilian de Mystique...) ; un allie, un autre heros, ne peuvent pas. « Victory 0 » : lu dans `desc`. « CHOOSE to deal 5 damage to an enemy OR remove 3 threat from a scheme » : UNE branche, au choix du joueur qui la vainc. « While in the victory display » : sur my001a. Chiffres : cout 0, menace 6, 5 degats, 3 menaces.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (5) : jouee depuis la main (cout 0, Hero Action) : entre en jeu avec 6 de menace FIXE ; Mystique contre : retire son THW (2) de menace (6 -> 4) ; TEMOIN : un ALLIE (Nightcrawler) ne peut PAS retirer de menace d'Infiltration (6 restent) ; Une fois dejouee, branche 1 : 5 degats a un ennemi (Rhino) ; la carte part dans la pile de victoire ; Une fois dejouee, branche 2 : 3 menaces retirees d'une manigance (complot principal 5 -> 2). Substitution : **rouges 3/5** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : formes a deux faces / carte en vitrine ; cas plateau `mystique-plateau.test.ts` + captures Chromium FR et EN (captures/mystique, captures/mystique-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my008

- [x] Etape 2 : carte(s) de reference : - `ra012` : `CanGenerateResources(AbilityType.HeroResource, resources_fn=..).SetCostFunc(CostFunc.Exhaust("This"))` pour une ressource de HEROS payee par inclinaison de la carte. - `bs005` : `CanGenerateResources(.., Resources(..), CardFinder2("TECH"))` pour « for a <TRAIT> card » ; ici `SHAPESHIFTER` (trait des evenements du deck).
- [x] Etape 5 : texte-contre-code : « HERO resource » : seulement en forme heros. « generate a [WILD] resource » : `Resources("G")` (une ressource, joker). « for a SHAPESHIFTER card » : uniquement pour jouer/payer une carte portant le trait SHAPESHIFTER. « Exhaust » : cout, la carte doit etre redressee. Chiffres : cout 1, une ressource.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (3) : Ressource de heros [wild] pour une carte SHAPESHIFTER : elle paie Deception (cout 1), Focus s'incline ; TEMOIN : elle NE paie PAS une carte non SHAPESHIFTER (Unconditional Love reste en main, Focus reste prete) ; TEMOIN : en forme alter-ego, ressource de HEROS indisponible (Deception reste en main). Substitution : **rouges 1/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my009

- [x] Etape 2 : carte(s) de reference : - `03015` Avengers Assemble! : `.SetPlay().MaxOnePerRound()` (« Max 1 per round » vaut deja pour toute la table, limit-max.md) + `Faces.ReadyAll`. - `21187a` : `card.Flip(effect)` ; `my002` : choix d'une forme par `AskChooseFace`.
- [x] Etape 5 : texte-contre-code : « Flip ALL form upgrades FACEDOWN and READY THEM » : les trois formes passent cachees (celles qui le sont deja ne bougent pas), puis les trois sont redressees (meme celles qui n'ont pas change). « Draw 1 card » : une carte. « CHOOSE a form and flip THAT card FACEUP » : apres la pioche, une forme au choix passe visible (toutes sont alors cachees ; elle retourne les AUTRES facedown par sa Reponse forcee, sans objet ici). « Max 1 per round » : `MaxOnePerRound`, partage entre les trois exemplaires. « Action » nue : jouable aussi en alter-ego. Chiffres : cout 1, pioche 1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (3) : les 3 formes passent cachees (Civilian visible -> cachee), sont REDRESSEES, 1 carte piochee, puis la forme choisie (Friend) passe VISIBLE ; « ready THEM » : une forme INCLINEE (Enemy) est redressee, meme si aucune n'avait besoin de changer de face ; « Max 1 per round » : un second exemplaire, meme round, n'est pas jouable (une seule pioche : main 4 - 2 + 1 = 3, et non 2 ; Civilian visible). Substitution : **rouges 3/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d epuisement : cas LIMITE / Max 1 ci-dessus, chiffre mesure au second emploi.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : formes a deux faces / carte en vitrine ; cas plateau `mystique-plateau.test.ts` + captures Chromium FR et EN (captures/mystique, captures/mystique-en).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my010

- [x] Etape 2 : carte(s) de reference : - `bs010` Beastly Charge / `01053` Relentless Assault : `hero.DealDamage(cibles, n, effect, property=AttackProperty(overkill=..))` + `.SetPlay().SetLabel('attack').SetTarget(Enemy)` (fiche `overkill.md`).
- [x] Etape 5 : texte-contre-code : « Deal 4 damage » : 4 (une ATTAQUE du heros, donc Defense/Tenace/Perce s'appliquent). « If the ENEMY form is FACEUP » : la forme my004 face `a` ; sinon 4 degats sans overkill. « 2 ADDITIONAL damage AND gains overkill » : 6 degats ET overkill, ensemble ou pas du tout. Chiffres : cout 2, 4 degats, +2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (4) : forme Enemy CACHEE : 4 degats a Rhino, sans overkill ; forme Enemy VISIBLE : 4 + 2 = 6 degats a Rhino ; forme Enemy VISIBLE, cible Hydra Mercenary (3 PV) : 6 degats, l'overkill reporte 3 sur Rhino ; TEMOIN forme Enemy CACHEE, meme cible : 4 degats, 1 de trop, PAS d'overkill (Rhino intact). Substitution : **rouges 4/4** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my011

- [x] Etape 2 : carte(s) de reference : - `dy011` Unconditional Love (destiny) : meme carte vue du cote de Destiny (`Faces.ReadyAll` + `Search.PlayerCard(include_player_deck, include_discard_pile)` + `GainCard`).
- [x] Etape 5 : texte-contre-code : « Destiny/Irene Adler » : toute carte en jeu nommee Destiny (l'allie my006, ou l'identite du heros Destiny) ou Irene Adler (son alter-ego) ; « Mystique/Raven Darkhölme » : Mystique ou Raven Darkhölme (l'identite du joueur, ou l'allie dy003). « ready ... AND ... » : les deux ensembles se redressent. « Otherwise, search YOUR DECK AND DISCARD PILE for DESTINY » : l'allie Destiny (my006), les deux zones, une carte, deck melange. Chiffres : cout 1.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (3) : Destiny (allie) en jeu : Destiny ET Mystique sont redressees ; Destiny absente, dans le DECK : elle est ajoutee a la main ; Destiny absente, dans la DEFAUSSE : elle est ajoutee a la main. Substitution : **rouges 3/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my012

- [x] Etape 2 : carte(s) de reference : - `05005` Wiggle Room / `14015` Side Step : `WhenUnitWouldTakeDamage(HeroInterrupt, "You", op).SetPlay().SetLabel('defense')` + `message.PreventDamage(3, effect)`.
- [x] Etape 5 : texte-contre-code : « prevent 3 of THAT damage » : 3 points de CE paquet de degats (moins s'il y en a moins). « If the FRIEND form is FACEUP » : my005 face `a`. « ready MYSTIQUE » : l'identite du joueur (le heros). Interruption de HEROS. Chiffres : cout 1, prevenir 3.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (3) : Rhino frappe pour 4 (ATQ 2 + boost 2) : 3 sont prevenus, 1 passe ; Friend CACHEE : Mystique reste inclinee ; Friend VISIBLE : en plus, Mystique est REDRESSEE ; TEMOIN sans la carte, Rhino frappe pour 4. Substitution : **rouges 2/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my013

- [x] Etape 2 : carte(s) de reference : - `90119` Search and Rescue (rescue_rainy) : le seul contre du depot qui ignore la Crise ; `.SetIgnoreKeyword('Crisis', condition=..)` declare l'ignorance pour le CIBLAGE (crisis.md) et `ignore_crisis=True` pour la resolution. - `01037` Mark V Helmet : « remove 1 threat from each scheme » = `RemoveThreatFromSchemes("EachScheme", n, effect)` (retire AUSSI des manigances annexes, `hf501a`).
- [x] Etape 5 : texte-contre-code : « Remove 3 threat from a scheme » : 3 sur UNE manigance choisie. « If the Civilian form is faceup » : my003 face `a` ; alors la Crise est ignoree pour CE contre (ciblage ET resolution) ET 1 menace est retiree de CHAQUE manigance (principale et annexes, aussi sous Crise puisque la Crise est ignoree pour ce contre). Forme cachee : contre normal, la Crise s'applique. Chiffres : cout 2, 3 menaces, 1 par manigance.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (4) : Civilian CACHEE : 3 menaces retirees du complot principal (5 -> 2) ; Civilian VISIBLE : 3 sur le complot principal ET 1 sur CHAQUE manigance (principal 5 -> 1, annexe 4 -> 3) ; Civilian VISIBLE : la CRISE est ignoree pour ce contre (complot principal 5 -> 2 malgre Defense Network) ; Civilian CACHEE sous une Crise : le complot principal n'est PAS ciblable (le pilote doit viser la manigance annexe : 5 menaces restent sur le principal). Substitution : **rouges 4/4** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my014

- [x] Etape 2 : carte(s) de reference : - `th011` / `01025` : `identite.ChangeToOtherIdentityForm(effect)` pour passer en alter-ego ; `42017` : `joueur.AssignHeal(personnages, N, effect)` pour « heal N damage among ... » (le joueur repartit).
- [x] Etape 5 : texte-contre-code : « If you are in HERO form, flip to alter-ego » : sans « may » (obligatoire) ; deja en alter-ego : on ne retourne pas. « Heal 4 damage AMONG Raven Darkhölme, Destiny/Irene Adler, Rogue/Anna Marie » : 4 points au TOTAL repartis par le joueur entre les personnages EN JEU qui portent l'un de ces noms (apres le retournement : l'identite est alors Raven Darkhölme) ; un personnage absent n'est pas une cible. Chiffres : cout 2, soin 4.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (3) : en forme HEROS : retournement obligatoire en alter-ego, puis 4 degats soignes (identite 3 + Destiny 1) ; 4 degats SEULEMENT soignes : identite a 6 degats -> 2 ; Rogue (allie) fait partie des personnages soignables : 4 degats repartis sur Rogue (2) et l'identite (2). Substitution : **rouges 3/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my015

- [x] Etape 2 : carte(s) de reference : - `dy013` Seizure / `mt011` Psychic Tremor : meme gabarit (`WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` + `ChooseAbilities`, branche 1 `condition=joueur.IsAlterEgo()` + `Exhaust("YourIdentity")`). - `sk280` / `cr016` : `ability.cout_en_groupe = True` pour « any player may help pay the cost » (lu par `CheckAnyPlayerMayHelpPay`).
- [x] Etape 5 : texte-contre-code : « Exhaust RAVEN DARKHOLME AND DESTINY » : DEUX inclinaisons dans le cout, l'alter-ego (donc seulement en forme alter-ego, apres l'eventuelle bascule) ET l'allie Destiny (ready, sous le controle du joueur) ; sinon la branche n'est pas offerte. « remove My Love FROM THE GAME » : la carte quitte la partie. « Any player may help pay » : le cout ne comporte aucune ressource (que des inclinaisons), le marquage `cout_en_groupe` est pose par fidelite au texte, sans effet visible. « Discard DESTINY » : l'allie ; sans allie, la branche reste offerte, aucune carte n'est defaussee et la carte gagne le surge. « If NO card was discarded this way, this card gains surge. Discard this obligation » appartient a la SECONDE branche. Chiffres : boost 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (5) : branche 1 : en alter-ego, Raven ET Destiny s'inclinent, l'obligation est retiree de la partie ; branche 1 NON offerte quand Destiny est deja inclinee : l'obligation defausse Destiny (seconde branche) ; branche 2 choisie : Destiny est defaussee, l'obligation aussi (Raven reste prete) ; sans Destiny : rien n'est defausse et la carte gagne SURGE (la carte rencontre suivante, Hydra Mercenary, est distribuee) ; en forme HEROS le joueur peut passer en alter-ego (« you may flip ») : il y passe. Substitution : **rouges 5/5** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my016

- [x] Etape 2 : carte(s) de reference : - `49007` Wrapped in Metal / `60113b` : `EnemyCannotActivate(NonKeyword, "This", conditions=[..])` pour « does not activate » (annule l'activation par `SetBeInstead`). - `sn014` : `ennemi.DoActivate(joueur, effect)` pour « activates against you ». - `incite.md`, `villainous.md` : `Incite 2` et `Villainous 1` lus NATIVEMENT dans `desc`, aucun script.
- [x] Etape 5 : texte-contre-code : « WHILE Destiny's Warning is in play » : l'interdiction n'existe que si une Destiny's Warning est en jeu (et elle disparait avec elle). « does not ACTIVATE » : ni attaque ni manigance. « If Mister Sinister is ALREADY in play » : un AUTRE exemplaire (celui-ci vient d'etre revele). « discard THIS card THEN Sinister activates against YOU even if Warning is in play » : la carte revelee part, puis celui deja en jeu active contre le joueur qui revele, en ignorant l'interdiction (`ActiverSinister` leve le drapeau `my_forcer`). Chiffres : PV 5, ATQ 3, SCH 3, boost 2, Incite 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (3) : tant que Destiny's Warning est en jeu, il ne s'active PAS (0 degat) ; TEMOIN : sans Destiny's Warning il s'active (ATQ 3 : 3 degats) ; Une fois revele, DEJA en jeu : la 2e copie est defaussee et le sbire en jeu s'active MEME avec Destiny's Warning (3 degats). Substitution : **rouges 2/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my017

- [x] Etape 2 : carte(s) de reference : - `02027` Goblin Nation : `WhenCardBecomeBoost("This", PutThisIntoPlay)` pour « [star] Boost: Put X into play » ; fiche `boost.md` (l'etoile n'existe que par la capacite). - `mt` / `hf` : `RemoveThreatFromSchemes("MainScheme", "1*", effect)` pour « 1[per_hero] threat from the main scheme ». - `incite.md` : `Incite 2` lu NATIVEMENT dans `desc`.
- [x] Etape 5 : texte-contre-code : « Remove 1[per_hero] threat FROM THE MAIN SCHEME » : le complot principal, 1 par joueur (`"1*"`). « [star] Boost: PUT INTO PLAY » : comme carte de boost, le complot entre en jeu SANS « When Revealed » ni Incite. Chiffres : menace 3*, boost 0, Incite 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (2) : a la revelation : Incite 2 pose 2 menaces PUIS Une fois revelee en retire 1 par joueur (1 + 2 - 1 = 2) ; ★ Boost : retournee comme carte de boost d'une manigance de Rhino, elle entre en jeu. Substitution : **rouges 2/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my018

- [x] Etape 2 : carte(s) de reference : - `my015` / `my014` : `RemoveThreatFromSchemes(.., "1*", effect)`, `ActiverSinister` (helper du set). - `rl015` Shi'ar Host / `surge.md` : `ThisCardGainSurge(effect, message)` pour « if you cannot, this card gains surge ».
- [x] Etape 5 : texte-contre-code : « Remove 1[per_hero] threat FROM DESTINY'S WARNING » : ce complot annexe precise, 1 par joueur. « If you CANNOT » : Warning absente du jeu. « Sinister activates against YOU » : le joueur qui revele ; « If you cannot » (Sinister absent) : la carte gagne surge. Trois branches exclusives, la premiere possible l'emporte. Incite 1 lu dans `desc`. Chiffres : boost 2, Incite 1, 1 menace par joueur.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (3) : Destiny's Warning en jeu : 1 menace par joueur retiree de la manigance annexe (4 -> 3) ; pas de Warning, Mister Sinister en jeu : il s'active contre vous (ATQ 3 : 3 degats) ; ni Warning ni Sinister : la carte gagne SURGE (la carte suivante, Hydra Mercenary, est distribuee). Substitution : **rouges 3/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).

### my019

- [x] Etape 2 : carte(s) de reference : - `47022` Jubilee / `12020` Swarm Tactics : `desc.TeamUp` + `.SetTarget("TeamUp")` (RECETTES : le chargeur l'exige) puis `.SetTarget2(Enemy, ..)` pour la cible suivante. - `01083` : `Faces.GiveStatus(cibles, "Stunned", effect)` ; meme appel pour "Confused".
- [x] Etape 5 : texte-contre-code : « Team-Up (Nightcrawler and Mystique) » : les DEUX personnages (identite ou allie) en jeu ; `desc.TeamUp = "Nightcrawler;Mystique"`. « STUN AND CONFUSE an enemy » : le MEME ennemi recoit les deux cartes d'etat (sonne ET desoriente). « Max 1 per deck » : `desc.MaxPerDeck` (constructeur de deck). Chiffres : cout 2.
- [x] Etape 6 : nombres : relus texte <-> `cards.json` <-> script (voir la ligne Chiffres ci-dessus quand elle existe).
- [x] Etape 7 : cas (2) : Team-Up Nightcrawler + Mystique : Rhino est SONNE ET DESORIENTE ; TEMOIN : sans Nightcrawler en jeu la carte n'est pas jouable (elle reste en main, Rhino sans statut). Substitution : **rouges 1/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 24 parties (rhino, normal, 3 profils x 8, 0 bloquee), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 24 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee ; 24 parties autoplay menees au bout, 182/182 decks montent).


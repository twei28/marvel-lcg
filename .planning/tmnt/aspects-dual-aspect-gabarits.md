# Aspects TMNT « Dual-Aspect » (`ud`, pack `tmnt_aspect_dual`) : gabarits PROCESSUS-CARTE

16/10/2026, branche `aspects-ud`. Six scans, six allies NOUVELLES (aucun équivalent officiel ;
classement du TSV re-vérifié : 12013 Ronin et 60053 Ronin n'ont ni le texte ni le type). Cas :
`Fusion/marvel-lcg-src/tools/cas/tmnt_aspect_dual.py` (filtre `[ud]`, 28 cas, 28/28 verts).
Questions : `.planning/tmnt/aspects-dual-aspect-questions.md` (Q-UD1 transversale, Q-UD2 à Q-UD4).

## Socle commun aux six cartes

- **Double aspect** (`desc.Class = "A;B"`, ordre du bandeau imprimé). Aucune règle de construction
  imprimée sur les scans (ni limite, ni mention « both aspects ») : lecture = la carte entre dans un
  deck de l'un OU de l'autre aspect.
  - Moteur : rien à changer (`ClassCard` découpe sur « ; », `IsClass` vrai pour chacun). Preuve :
    `[ud] ud001 ... The Power of Justice ET The Power of Aggression (2+2 = 4)` et `ud003 ... Protection
    + Aggression`, témoin `... The Power of LEADERSHIP ne double pas`. **Mutation** (Class réduite à
    « Aggression » / « Protection ») : les deux cas ROUGES, le témoin et les 4 cas officiels « The Power
    of » restent verts.
  - Deck-builder : `regles.js` (`estDoubleAspect`, `aspectsDeClasse`, pool, légalité), `filtres.js`
    (filtre d'aspect), `app.js` (libellé « Agressivité / Justice », couleur du 1er aspect). Preuve :
    `tools/tests-lanceur/regles-double-aspect.test.mjs` (10 tests, dont 4 vus ROUGES avant le correctif : pool
    vide, deck Justice + Rōnin refusé, doubles d'aspect commun second refusés, filtre) ; les 22 autres
    fichiers `tests-lanceur` restent verts. Vrais decks + vrai catalogue (`scratchpad/ud/legal.mjs`) :
    Spider-Man Justice + ud001/ud004/ud005, Captain Marvel Leadership + ud002/ud006, Black Panther
    Protection + ud003 : LÉGAUX, un seul aspect chacun ; les six cartes ont une tuile.
  - Préparation (`catalog.js` `aspectsOfDeck`) : corrigé, NON prouvé (module lié au DOM, aucun banc).
  - Plateau : liseré du 1er aspect (`aspectDeClasse`), cas `ui-app/src/board/tmnt-aspect-dual-plateau.test.ts`.
- **Ressources** (étape 3, jamais à vue) : coin inférieur gauche découpé et comparé
  (`scratchpad/ud/icons.png`) : étoile verte = tm007 Optimism / tl002 Splinter (`RES G`) → ud001 ;
  éclair = tm004 Impulsive (`Y`) → ud002, ud003, ud006 ; poing = ua009 Clobber (`R`, même série
  d'aspects) → ud004 ; « nœuds reliés » bleus = ua006 Bo-Wing (`B`) → ud005. L'icône du coût de Rōnin
  (« spend a ✶ resource ») est la même étoile, en noir : [wild].
- **PV** : le rond orange « 2 » est la vie (Bo-Wing imprime « 3 » au même endroit = PV 3 de 53035) ;
  le TSV disait « PV non imprimés » : faux.
- **Dégât consécutif** : icône sous THW ET sous ATK, sans chiffre = 1 : `"ATK": "N*"`, `"THW": "N*"`.
- **Unicité** : ✦ imprimé sur les six → `"* "`. Aucun bandeau ✦ de titre d'origine (Q-R1) → pas
  d'`unique_also`. Sous-titres = titres d'alter ego des tortues : Q-UD1.

### ud001 : Rōnin (Mikey), Aggression/Justice, NOUVELLE

- [x] Étape 2 : cartes de référence : Cloak → `tl016` / fiche `cloak.md` ; « After X enters play »
      → `AfterCardEnterPlay(Response, "This")` (fabrique de 01066) ; « When X is defeated by
      consequential damage » → `30021` SP//dr (`WhenUnitBeDefeated(..., by_consequential=True)`) ;
      « spend a [wild] resource → draw » → `04097` Moon Knight (`Cost("G")`).
- [x] Étape 5 : mots-pièges : « cloak HIM » (lui-même) ; « defeated » ≠ damaged ; « by
      CONSEQUENTIAL damage » ; coût = ressource WILD (pas « any ») ; deux capacités, deux modules.
      Résultat : conforme.
- [x] Étape 6 : coût 4, PV 2, THW 2* / ATK 2*, RES G, 3 cartes piochées, 1 ressource wild.
      Résultat : conforme (`desc` et `DrawUp(3)`).
- [x] Étape 7 : Response → `... Response, apres son entree en jeu il est cloake` ; Interrupt →
      `... vaincu par degat consecutif + depense d'une ressource [wild] -> pioche 3` ; témoins : sans
      ressource wild (Strength) rien, vaincu par dégâts NON consécutifs rien. Substitution : 4/6 rouges
      (les 2 verts sont les cas de CLASSE, prouvés par mutation de `desc.Class`). ⚠ Sous le stub, les
      deux témoins rougissent pour une raison de montage (la bascule `Puzzle.Cloak` POSE un Cloaked
      que le stub n'a pas donné, il absorbe les dégâts) : assumé.
      Résultat : 6/6 verts.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir « Autoplay » plus bas (0 traceback ; jouée 12 fois, Cloaked vu).
- [x] Étape 8 bis : change ce qu'on VOIT ? OUI, une carte d'état Cloaked : carte d'état déjà
      dessinée par le plateau (cas des packs TMNT `cloaked`), rien de neuf.
      Résultat : sans nouveau cas.

Carte terminée : OUI, sous réserve de Q-UD1 (unicité par sous-titre).

### ud002 : Doomsayer (Donnie), Aggression/Leadership, NOUVELLE

- [x] Étape 2 : « draw X (max 3), X = villain's stage number » → `21013` White Tiger
      (`Worlds.GetVillainStage`, `Math.MinMax`) SANS sa clause « no stage → draw 1 » (non imprimée ici :
      minimum 0) ; « draw 1 for each minion engaged with you » → `19030` "Bring It!" ; défaite par dégât
      consécutif → `30021`.
- [x] Étape 5 : « enters play » (et non « play from hand ») ; « to a MAXIMUM of 3 » ; « engaged with
      YOU ». Résultat : conforme.
- [x] Étape 6 : coût 4, PV 2, THW 1* / ATK 2*, RES Y, max 3. Résultat : conforme.
- [x] Étape 7 : Response → stade I : 1 carte, stade II : 2 cartes ; Interrupt → 2 sbires engagés :
      2 cartes ; témoins 0 sbire → 0, dégâts non consécutifs → 0. Substitution 3/5 rouges (les deux
      verts sont des témoins d'ABSENCE d'effet). ⚠ Le plafond « 3 » n'est pas mordu : aucun vilain du
      harnais n'a de stade 4 (le stade III de Rhino n'existe pas en standard). Le code borne à 3.
      Résultat : 5/5 verts.
- [x] Étape 7 bis : limite imprimée ? NON (le maximum de 3 est un plafond de valeur, voir ci-dessus).
- [x] Étape 8 : voir « Autoplay » (0 traceback).
- [x] Étape 8 bis : NON (pioche).

Carte terminée : OUI, sous réserve de Q-UD1 ; le plafond « 3 » est codé mais pas mesuré (aucun
vilain à stade 4 dans le harnais).

### ud003 : Heavy Metal (Jenny), Aggression/Protection, NOUVELLE

- [x] Étape 2 : « enters play with 2 amp counters » → `01066` Hawkeye (`ThisEnterPlayWithCounters`) ;
      compteur « amp » AJOUTÉ à `CardFace.COUNTER` (extension moteur) ; « After X takes consequential
      damage » → `19012` Martyr / `tl009` ; « remove 1 counter from her → » → 01066 (`CostFunc.Counter`) ;
      « place a status card on a character » → `dt084` Off the Cuff, `50020` The Pericles.
- [x] Étape 5 : « TAKES » (Tough empêche) ; « remove ... FROM HER » = coût ; « a CHARACTER » = ami ou
      ennemi ; « a status card » : **Q-UD2** (quelles cartes d'état), codé sur l'option recommandée.
      Résultat : conforme à la lecture provisoire.
- [x] Étape 6 : coût 4, PV 2, THW 1* / ATK 2*, RES Y, 2 compteurs, 1 retiré. Résultat : conforme.
- [x] Étape 7 : `... entre en jeu avec 2 compteurs amp` ; `... Response ..., 1 amp retire, un etat
      sur Rhino` (amp 2 → 1, Rhino Stunned) ; témoins : 0 amp → rien ; Tough → pas de dégât, pas de
      Réponse. Substitution 3/5 rouges (le témoin « 0 amp » reste vert : absence d'effet ; le cas de
      classe est prouvé par mutation).
      Résultat : 5/5 verts.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : voir « Autoplay » (0 traceback).
- [x] Étape 8 bis : OUI (compteur). Cas `ui-app/src/board/tmnt-aspect-dual-plateau.test.ts` : la carte
      est dessinée avec `compteurs['amp'] = 2`, libellé « ampli » ; vu ROUGE sans l'entrée
      `amp: 'ampli'` de `compteurs-fr.ts`.
      Résultat : 4/4 verts.

Carte terminée : NON : Q-UD2 en attente (et Q-UD1).

### ud004 : Stealth Fighter (Raph), Justice/Leadership, NOUVELLE

- [x] Étape 2 : Cloak → fiche `cloak.md` ; « enters play » → `AfterCardEnterPlay` ; « takes
      consequential damage » → `19012` ; défaite par dégât consécutif → `30021` ; « cloak a friendly
      character » → `td005` (`Worlds.GetOnFieldFriendlyCharacters`, `AskChooseFaces`).
- [x] Étape 5 : « enters play OR takes consequential damage » (deux déclencheurs, deux montages) ;
      « cloak HIM » ; « a FRIENDLY character » (pas lui-même, il quitte le jeu) ; **« Interrupt: After »
      : Q-UD3**, codé sur l'option recommandée (Interruption « When ... is defeated »).
      Résultat : conforme à la lecture provisoire.
- [x] Étape 6 : coût 4, PV 2, THW 1* / ATK 1*, RES R. Résultat : conforme.
- [x] Étape 7 : entrée en jeu → Cloaked ; dégât consécutif subi (il survit) → Cloaked ; vaincu par
      dégât consécutif → Spider-Man Cloaked ; témoin dégâts non consécutifs → personne. Substitution
      4/4 rouges (le témoin rougit par le montage, comme ud001).
      Résultat : 4/4 verts.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : voir « Autoplay » (0 traceback).
- [x] Étape 8 bis : OUI (Cloaked), carte d'état déjà dessinée : sans nouveau cas.

Carte terminée : NON : Q-UD3 en attente (et Q-UD1).

### ud005 : Sōhei (Leo), Justice/Protection, NOUVELLE

- [x] Étape 2 : Toughness → `desc.Toughness` (fiche `toughness.md`, aucun code) ; défaite par dégât
      consécutif → `30021` ; « +N hand size until the end of the … » → `12033` / `wd122`
      (`GainUntilPhaseEnd(hand_size=)`), ici `GainUntilRoundEnd`.
- [x] Étape 5 : « until the end of the ROUND » (pas de la phase) ; « YOUR HERO » en alter ego :
      **Q-UD4**, codé sur l'option recommandée (rien en alter ego). Résultat : conforme à la lecture
      provisoire.
- [x] Étape 6 : coût 4, PV 2, THW 1* / ATK 1*, RES B, Toughness 1, +2. Résultat : conforme.
- [x] Étape 7 : Toughness à l'entrée ; vaincu par dégât consécutif → taille de main +2 ; toujours +2
      après `EndPlayerPhase` (round, pas phase) ; témoins : dégâts non consécutifs → +0 ; alter ego →
      +0. Substitution 2/5 rouges (Toughness = donnée ; les deux témoins d'absence restent verts).
      Résultat : 5/5 verts.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : voir « Autoplay » (0 traceback).
- [x] Étape 8 bis : NON (Tough déjà dessinée ; taille de main = chiffre).

Carte terminée : NON : Q-UD4 en attente (et Q-UD1). Non mesuré : la fin du bonus au round suivant.

### ud006 : Nightwatcher (Jenny), Leadership/Protection, NOUVELLE

- [x] Étape 2 : Toughness → `desc` ; « After X takes consequential damage, give her a tough status
      card » → `19012` Martyr, SANS ses filtres (attaque + ennemi vaincu) que Nightwatcher n'imprime pas.
- [x] Étape 5 : « TAKES » (une Tough qui empêche le dégât ne déclenche rien) ; « give HER ».
      Résultat : conforme.
- [x] Étape 6 : coût 4, PV 2, THW 1* / ATK 2*, RES Y, Toughness 1. Résultat : conforme.
- [x] Étape 7 : Toughness à l'entrée ; dégât consécutif subi → Tough ; témoin avec Tough : dégât
      empêché, pas de nouvelle Tough. Substitution 1/3 rouge (Toughness = donnée, témoin d'absence).
      Résultat : 3/3 verts.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : voir « Autoplay » (0 traceback).
- [x] Étape 8 bis : NON (Tough déjà dessinée).

Carte terminée : OUI, sous réserve de Q-UD1.

## Autoplay (étape 8, commune)

Rhino normal, profil équilibre. Decks de départ officiels, cartes basiques non-ressource remplacées
(decks LÉGAUX au verdict de `regles.js`, un seul aspect chacun) : `scratchpad/ud/deck-ud-*.json`.

| Deck | Parties | Blocages | Tracebacks (6 motifs, grep exhaustif) | Ce que le journal montre |
|---|---|---|---|---|
| Spider-Man Justice + ud001, ud004, ud005 | 8 | 1 (graine 2) | 0 | Rōnin joué 12 fois, cloaké à l'entrée, vaincu par son dégât consécutif 5 fois ; Stealth Fighter cloaké à l'entrée, son Interruption a cloaké Spider-Man ; Sōhei entré avec Tough, vaincu par dégât consécutif 3 fois |
| Captain Marvel Leadership + ud002, ud006 | 8 | 0 | 0 | Doomsayer : « pioche 1 carte (Doomsayer) » au stade I (2 fois) ; Nightwatcher entrée avec Tough |
| Black Panther Protection + ud003 | 8 + 24 | 2 (graines 29, 30) | 0 | Heavy Metal en jeu 16 fois, « perd 1 compteur amp » 8 fois, suivi chaque fois de « Rhino gagne Stunned (Heavy Metal) » |
| TÉMOIN Spider-Man (deck de départ) | 8 | 0 | 0 | — |

Les 3 blocages : `<E> (..) [01093 Tenacity] (Hero Action) WhenPlayerInTurn failed` (carte du CORE,
présente aussi dans le deck témoin, qui l'a jouée sans bloquer dans cette fournée) : aucun lien avec
le pack `ud`. Non vu en autoplay : l'Interruption de Rōnin (pas de ressource wild en main au bon
moment), celle de Doomsayer avec des sbires engagés, celle de Sōhei (la taille de main n'est pas
journalisée). Elles sont prouvées par les cas.

Étape 8 : [x] pour les six cartes (0 traceback, blocages étrangers au pack).

## Gates statiques (extension moteur : compteur `amp`)

- `test_cards` : 6587 cartes construites, 0 erreur.
- `verifier_appels_modules ... tmnt_aspect_dual` : « OK : tous les appels existent » (outil déjà
  calibré le 04/09/2026, §9 de PROCESSUS-CARTE).
- `verifier_api_cartes` : 13 fichiers en faute, tous antérieurs, aucun du pack `ud`.
- `verifier_prefixes` : OK.
- Témoins : `[reskin]` 11/11, `[rampage]` 6/6 (après fusion de `sauvegarde-cle-usb-2026-10-14`) ;
  les 4 cas officiels « The Power of » restent verts.
- `tools/tests-lanceur/*.test.mjs` : 23 fichiers verts. `ui-app` : `aspect.test.ts` +
  `tmnt-aspect-dual-plateau.test.ts` verts.

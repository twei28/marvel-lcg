# Iron Fist (Hero Pack officiel MC64EN, FFG, novembre 2026) : gabarits PROCESSUS-CARTE

Preuves du 20/10/2026, branche `iron-fist-officiel`. Pack `iron_fist`, set « Iron Fist », 13 card_id :
`64001a` Iron Fist, `64001b` Danny Rand, `64002`-`64012` (11 cartes signature, 15 exemplaires). Numérotation
officielle (série 64 libre dans `data/cards.json` : Jessica Jones 61, Luke Cage 62, Wave fan-made 65) ;
numéro de carte = numéro de collection imprimé (1A/1B, 2 à 12).
Périmètre (décision du 20/10/2026) : héros + cartes signature. PAS les cartes d'aspect du pack ni les cartes
de rencontre (obligation, némésis : non publiées).

Sources : `.planning/iron-fist-officiel/` (relevé Hall of Heroes, lecture, cinq décisions de l'utilisateur
`lecture-reponses.md`, question ouverte `creation-questions.md`). Chaque carte relue sur son image avant le
code (`hoh-iron-fist/c1`-`c11-1`, `s1`, `s2`) : aucun écart avec le relevé.

**Cas** : `Fusion/marvel-lcg-src/tools/cas/iron_fist.py`, préfixe `[iron_fist]`, **57 cas, 57 verts**
(`CAS_PREFIX=ironfist_ PARALLELES=4 test_capacites.py .game-src 31000 <rapport> "[iron_fist]"`).
**Substitution** : `tools/substituer_pack.py .game-src 32000 640`, **13/13** cartes rouges sans leur module,
empreinte md5 du pack identique avant/après (`6d6a74b3…`). Les cas restés verts sous substitution sont tous
des témoins d'ABSENCE (coût impayable, autre forme, « pas jouée ») ou des valeurs imprimées (`desc`), listés
carte par carte.

**Autres gates** : `test_cards` 6810 ok / 0 erreur ; `verifier_prefixes` OK ; `verifier_appels_modules
iron_fist` OK (calibré : une sonde `Faces.MethodeInexistanteIronFist` le fait tomber, puis retirée) ;
`verifier_api_cartes` : aucun problème dans `iron_fist` (13 problèmes préexistants ailleurs) ;
`DECK_NOM=iron_fist verifier_tous_les_decks` : « identite 64001b, main 6, deck 9 » (témoin spider_man OK) ;
légalité des decks : 0 carte signature étrangère, exemplaires = `MaxPerDeck`. Plateau (étape 8 bis) :
`ui-app/src/board/iron-fist-plateau.test.ts`, 10 cas verts ; sensibilité prouvée (sonde `c_chi` renommé :
3 rouges). Aucun correctif de plateau nécessaire : le rendu générique des compteurs dessine déjà le chi.

**Autoplay** (étape 8) : `autoplay.py --deck iron_fist --vilains rhino --profils equilibre --parties 8` :
0 victoire / 8 (4,0 rounds), 0 blocage, **0 traceback** (grep NameError|AttributeError|TypeError|KeyError|
AssertionError|Traceback sur les 8 journaux) ; témoin `spider_man` même fournée : 0 / 8 (6,9 rounds),
0 blocage. Iron Fist n'a que ses 15 cartes signature (`player_deck` vide, PROCESSUS-HEROS étape 3) : la
défaite rapide est attendue. Seconde fournée `--vilains rhino,klaw --profils prudent,agressif --parties 4` : 0 / 16, 0 blocage, 0 traceback.
Cartes que le pilote n'exerce JAMAIS sur 24 parties : Deep Breathing (jouée), l'Action du Livre, la Ressource
de Redirect Chi ; la Forced Response de 64001a et la riposte d'Embody ne se sont pas présentées non plus
(couvertes par les cas).

Icônes de ressource : découpées et comparées à Luke Cage (MC62, même maquette 2026, `desc.RES` déclaré) :
62004 R (poing rouge), 62005 B (bleu), 62006 Y (éclair jaune), 62002 G (étoile verte). Aucune carte du pack
Iron Fist n'a de `RES` déjà déclaré : comparaison « même pack » impossible, à refaire au scan HD. Le glyphe
« ✱ ✱ » du texte de Redirect Chi est le glyphe [wild] (identique à 60043 American Sign Language, FNE 2026).

Décisions de l'utilisateur appliquées : (1) Technique mise en jeu par Danny Rand / le Livre attachée à
l'identité ; (2) au retournement en héros, les Techniques redeviennent Temporary et partent en fin de round ;
(3) The Way of Things : deux « a scheme » indépendants ; (4) Deep Breathing sans carte Iron Fist : tout le
deck défaussé, rien ajouté ; (5) les chi restent sur l'identité au retournement.
Aucune partie humaine n'a été jouée dans le navigateur.

### 64001a : * Iron Fist (face héros)

- [x] Étape 2 : carte(s) de référence : Response « After you play a card » → `fne/60027` Move in Shadow
      (`AfterPlayerPlayedCard(Response, "You", None, op)`) ; compteur sur l'identité → `venus/tv001a` ;
      « After the player phase ends » → `aos/50029`, `michelangelo/tm009` (`AfterPhaseEnd(ForcedResponse,
      "Player", op)`) ; soin de soi → `jubilee/47012`.
- [x] Étape 5 : texte-contre-code : « Response » nu imprimé sur la face héros (absent en Danny, cas) ; « play a
      card » ≠ « put into play » (cas) ; « here » = la carte d'identité ; « all BUT 4 » (surplus seulement,
      cas 3 chi) ; « heal 1 for EACH removed THIS WAY » (cas 7 → 4, 5 → 2 dégâts) ; Forced Response sans
      question. Résultat : OK.
- [x] Étape 6 : nombres : PV 10, ATQ 2, CTR 1, DEF 2, main 5 (cas « valeurs imprimées », scan 1A) ; 1 chi
      par carte ; seuil 4. Résultat : OK.
- [x] Étape 7 : 9 cas, 3 rouges sans module (Response 1 carte → 1 ; 2 cartes → 2 ; fin de phase 7 → 4 et
      soin 3) ; verts assumés : Response absente en alter ego, carte mise en jeu, 3 chi inchangés, fin de phase
      en alter ego, chi gardés au retournement (comportement du composant `Counter`, décision n°5), valeurs.
      Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : 8 parties + témoin spider_man, 0 traceback ; journal lu : « Iron Fist reçoit 1 compteur(s)
      chi » après chaque carte jouée en forme héros, jamais en Danny ; la Forced Response ne s'est pas
      déclenchée (le pilote dépense le chi avant d'en avoir 5), couverte par les cas. Résultat : OK.
- [x] Étape 8 bis : OUI (compteur). `iron-fist-plateau.test.ts` « 3 chi visibles sur Iron Fist », « tous les
      chi dépensés » ; rouge prouvé par la sonde `c_chi`. Résultat : OK.

Carte terminée : OUI

### 64001b : * Danny Rand (face alter ego)

- [x] Étape 2 : « lose temporary » → `cyclops/33004` Field Commander (`temporary=-1`) ; « Search your deck and
      discard pile … Put that card into play » → `bp/51025`, `kate_bishop/kb001b` ; « Limit once per phase »
      → `phoenix/34001a` (`LimitOncePerPhase`).
- [x] Étape 5 : « YOUR Technique cards » (`control_by="You"`, trait ; 60027 Temporary sans le trait part,
      cas) ; capacité continue de la face Danny seulement (retournement → défaussée, décision n°2, cas) ;
      « deck AND discard pile » (deux cas) ; « a Technique » (le Livre ITEM n'est pas trouvé, cas) ; « Put
      into play » = attachée à l'identité (décision n°1, `accroche_a`) ; « Action » nue sur la face alter
      ego. Écart de code SANS effet de jeu : le filtre porte `card_type=Upgrade` (exigé par le moteur pour un
      filtre à trait) ; les cinq Techniques imprimées sont toutes des améliorations. Résultat : OK.
- [x] Étape 6 : PV 10, REC 4, main 6 (cas « valeurs imprimées », scan 1B). Résultat : OK.
- [x] Étape 7 : 11 cas, 7 rouges sans module (Technique gardée en fin de round ; Move in Shadow part mais pas
      Feel the Flow ; cinq Techniques gardées ; Meditation deck ; Meditation défausse ; Livre non trouvé —
      l'Action n'existe plus ; limite) ; verts assumés : Technique défaussée en forme héros, défaussée après
      retournement, Meditation absente en héros, valeurs. Résultat : OK.
- [x] Étape 7 bis : OUI. Témoin : « limite 1 par phase » : deux Techniques disponibles, deux Actions, 1 seule
      Technique en jeu (chiffre mesuré : `techniques_en_jeu` = 1, 2 sans la limite). Résultat : OK.
- [x] Étape 8 : 13 Meditation jouées dans les 8 parties (« Danny Rand s'active », fouille du deck, la
      Technique s'équipe sur Danny) ; « n'appliquent plus [Danny Rand] » au retournement puis défausse en fin
      de round, conforme à la décision n°2 ; 0 traceback. Résultat : OK.
- [x] Étape 8 bis : OUI (attache). Plateau « la Technique est dessinée sous l'identité », « le stock reste
      visible sur Danny Rand ». Résultat : OK.

Carte terminée : OUI

### 64002 : Deep Breathing (événement, ×3)

- [x] Étape 2 : « Discard … until you discard X » → `Player.DiscardDeckUntil` (fiche `seek.md`, `venus/tv001b`) ;
      « an Iron Fist card » → `cyclops/33004` (« Cyclops upgrade » = `set_name`) ; Hero Action sans libellé →
      `luke_cage/62003`.
- [x] Étape 5 : « an IRON FIST card » = `set_name` « Iron Fist » (une carte signature d'un autre héros, 62004,
      ne l'arrête pas : cas) ; « add IT to your hand » (main exacte, cas) ; aucune carte Iron Fist → rien
      (décision n°4, cas) ; trouvée en dernière position → rendue malgré le remélange (cas). Résultat : OK.
- [x] Étape 6 : coût 0, [mental], ×3 (`MaxPerDeck` 3, deck de départ 3). Résultat : OK.
- [x] Étape 7 : 5 cas, 4 rouges sans module ; vert assumé : « injouable en alter ego » (absence). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : 24 parties (8 équilibre + 16 prudent/agressif, rhino et klaw), 0 traceback, mais le pilote n'a
      JAMAIS joué Deep Breathing (il la dépense comme ressource : 17 défausses dans la 1re fournée). Le code
      n'a tourné que dans les 5 cas du harnais (vrai moteur, vraie partie montée).
- [x] Étape 8 bis : OUI (main / défausse). Plateau « la carte trouvée est dans la main ». Résultat : OK.

Carte terminée : NON — étape 8 non exercée : aucune partie (pilote ni humain) n'a joué la carte.

### 64003 : Dragon Punch (événement)

- [x] Étape 2 : X choisi puis retiré → `venus/tv003` Arc Nova (`DeclareNumber`) ; attaque à cible →
      `cw/56008` ; étourdir → `Faces.GiveStatus(..., "Stunned")`.
- [x] Étape 5 : « MAY remove UP TO 5 » (0 légal, plafond 5 avec 7 chi : cas) ; « from your IDENTITY » ;
      « 2 ADDITIONAL for EACH » (une attaque 2 + 2X) ; « AT LEAST 3 » (3 sonne, 2 non : cas) ; « that enemy ».
      Résultat : OK.
- [x] Étape 6 : coût 2, [energy], 2 dégâts, +2 par chi, plafond 5, seuil 3 (cas X = 0/2/3/5 → 2/6/8/12).
      Résultat : OK.
- [x] Étape 7 : 5 cas, 5 rouges sans module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : jouée dans les parties (« Dragon Punch s'active », dégâts, Réponse de chi ensuite) ; 0 traceback.
      Résultat : OK.
- [x] Étape 8 bis : NON pour le décompte (dégâts) ; le Sonné est le rendu standard (tv004). Résultat : OK.

Carte terminée : OUI

### 64004 : Fists of Fury (événement, ×2)

- [x] Étape 2 : même texte « Deal N damage to an enemy. Deal N damage to an enemy. » → `cw/56008` Tooth and
      Claw, `gambit/37007` Royal Flush.
- [x] Étape 5 : trois choix indépendants (cas Tiger Shark à 1 PV vaincu au 1er coup, Rhino prend les deux
      autres) ; 1 dégât chacun (3, jamais 3 d'un coup). Résultat : OK.
- [x] Étape 6 : coût 1, [physical], ×2, 1 + 1 + 1. Résultat : OK.
- [x] Étape 7 : 2 cas, 2 rouges sans module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : jouée (journal : trois « va attaquer », Hydra Mercenary vaincu puis Rhino) ; 0 traceback.
      Résultat : OK.
- [x] Étape 8 bis : NON (dégâts seulement).

Carte terminée : OUI (l'interaction avec Channel the Iron Fist est la question Q1 de 64008, pas un défaut de
cette carte).

### 64005 : The Way of Things (événement, ×2)

- [x] Étape 2 : contre d'événement → `luke_cage/62005` ; « You may remove N counters from <identité> to … » →
      `venus/__init__.py` `ProposerRetraitDragage` (modèle `01165`).
- [x] Étape 5 : « You MAY » (refus : cas) ; « from IRON FIST » = identité ; deux « a scheme » indépendants,
      même manigance permise (décision n°3 : 6 → 2 sur la même, cas) ; 2 chi = prix (branche absente à 1 chi,
      cas). Résultat : OK.
- [x] Étape 6 : coût 1, [mental], ×2, 2 + 2 menaces, 2 chi. Résultat : OK.
- [x] Étape 7 : 3 cas, 3 rouges sans module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : jouée 5 fois ; journal : « Iron Fist perd 2 compteur(s) chi » puis seconde menace ; 0 traceback.
      Résultat : OK.
- [x] Étape 8 bis : NON (menace).

Carte terminée : OUI

### 64006 : * Lei Kung (soutien)

- [x] Étape 2 : coût double « exhaust and remove 1 counter » → `tmnt_shinobi_taijutsu/sh010`, `ua033` ;
      compteur sur l'identité → `venus/tv001b`.
- [x] Étape 5 : coût à DEUX parties (incliné ET 1 chi, cas) ; « your IDENTITY » (aussi en Danny, cas) ;
      unique (« * »). Résultat : OK.
- [x] Étape 6 : coût 1, [energy], 1 chi, 1 carte. Résultat : OK.
- [x] Étape 7 : 3 cas, 2 rouges sans module ; vert assumé : refus sans chi. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (l'inclinaison borne l'usage).
- [x] Étape 8 : 20 activations (« Lei Kung inclinée, Iron Fist perd 1 compteur chi, pioche 1 ») ; 0 traceback.
      Résultat : OK.
- [x] Étape 8 bis : OUI (inclinaison). Plateau « Lei Kung incliné ». Résultat : OK.

Carte terminée : OUI

### 64007 : * Book of the Iron Fist (amélioration)

- [x] Étape 2 : dessus de la défausse → `texas_twister/tt005` (`discard_pile.GetTop()`) ; Hero Action à
      inclinaison sur une amélioration → `human_torch/ht006` ; mise en jeu → `bp/51025`.
- [x] Étape 5 : condition lue à la résolution (Livre incliné même sans Technique, cas) ; « the TOP card »
      seulement (Technique sous une autre carte : rien, cas) ; « a Technique » = trait ; « put IT into play » =
      attachée à l'identité (décision n°1) ; unique. Résultat : OK.
- [x] Étape 6 : coût 2, [physical]. Résultat : OK.
- [x] Étape 7 : 3 cas, 2 rouges sans module ; vert assumé : absente en alter ego. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : 24 parties, 0 traceback ; le Livre a été JOUÉ (3 fois dans la 1re fournée) mais son Action
      n'a JAMAIS été activée par le pilote. Le code n'a tourné que dans les 3 cas du harnais.
- [x] Étape 8 bis : OUI (attache, inclinaison). Plateau « Livre couché », « Technique sous l'identité ».

Carte terminée : NON — étape 8 non exercée : l'Action du Livre n'a été activée dans aucune partie.

### 64008 : Channel the Iron Fist (Technique)

- [x] Étape 2 : « When you attack … increase the amount of damage that attack deals by 1 » → `winter/54002`,
      `32047`, `blade/bl008` (`DealAdditionalDamage`) ; attaque de base → `IsBasicAttack()`.
- [x] Étape 5 : « by 2 INSTEAD if basic » (cas base +2, événement +1) ; coût 1 chi (absent sans chi) ;
      Temporary natif. « that attack » sur un événement à plusieurs « Deal N damage » : chaque coup est une
      attaque distincte, Channel peut partir à chacun (Q1 TRANCHÉE par l'utilisateur le 20/10/2026, ruling
      des cartes à phrases répétées type Dance of Death ; cas Fists of Fury + 3 chi = 6 dégâts). Résultat : OK.
- [x] Étape 6 : coût 0, [energy], 1 chi, +1 / +2. Résultat : OK.
- [x] Étape 7 : 4 cas, 3 rouges sans module (substitution relancée le 20/10/2026 : 3/4) ; vert assumé : sans
      chi, 2 dégâts. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : 6 activations sur 24 parties (attaque de base : 4 dégâts ; Fists of Fury : 3 déclenchements,
      2 + 2 + 2, conforme à Q1) ; 0 traceback. Résultat : OK.
- [x] Étape 8 bis : OUI (attache). Plateau « cinq Techniques sous l'identité ».

Carte terminée : OUI

### 64009 : Embody the Dragon (Technique)

- [x] Étape 2 : mot-clé dynamique sur une autre carte → `hc014` (`get_new_value`), rafraîchi par
      `OnEvent.Counter` → `sm/27067` ; retaliate accordé → `hood/24038`, `next_evol/40090`.
- [x] Étape 5 : « IRON FIST gains » = la face héros (`Hero`), pas Danny (contre-cas : riposte 0 en alter
      ego) ; « X = chi ON THIS CARD » (cas 2 → riposte 2) ; « MOVE » = part de l'identité ET arrive ici (cas
      2/0 → 1/1) ; la riposte mord (Rhino subit 2, cas) ; Temporary natif. Résultat : OK.
- [x] Étape 6 : coût 0, [physical], 1 chi déplacé, X dynamique. Résultat : OK.
- [x] Étape 7 : 5 cas, 3 rouges sans module ; verts assumés : pas de riposte en alter ego, Action non offerte
      sans chi. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : 10 activations (« Iron Fist perd 1 chi, Embody reçoit 1 chi, appliquent Embody ») ; 27 sur les deux fournées ; la
      riposte ne s'est présentée dans aucune partie (pas de ligne de riposte au journal), elle est prouvée
      par le cas « Rhino attaque Iron Fist -> Rhino subit 2 » ; 0 traceback. Résultat : OK.
- [x] Étape 8 bis : OUI (compteur sur la carte). Plateau « 1 chi sur la carte, 1 sur Iron Fist ».

Carte terminée : OUI

### 64010 : Feel the Flow (Technique)

- [x] Étape 2 : Hero Action (thwart) sur carte en jeu → `michelangelo/tm009`, `fne/60027` ; coût en chi →
      `venus/tv001b`.
- [x] Étape 5 : coût 1 chi (refus sans chi, cas) ; « (thwart) » ; « a scheme » ; Temporary natif (perdu sous
      Danny, cas 64001b). Résultat : OK.
- [x] Étape 6 : coût 0, [mental], 1 chi, 1 menace. Résultat : OK.
- [x] Étape 7 : 2 cas, 1 rouge sans module ; vert assumé : refus sans chi. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : 11 activations ; 0 traceback. Résultat : OK.
- [x] Étape 8 bis : OUI (attache). Plateau « cinq Techniques sous l'identité ».

Carte terminée : OUI

### 64011 : Keep 'Em Coming (Technique)

- [x] Étape 2 : redresser → `Faces.ReadyAll` (RECETTES §2) ; coût en chi → `venus/tv001b`.
- [x] Étape 5 : coût 2 chi (refus à 1, cas) ; « ready HIM » = Iron Fist (cas incliné → prêt). Résultat : OK.
- [x] Étape 6 : coût 0, [physical], 2 chi. Résultat : OK.
- [x] Étape 7 : 2 cas, 1 rouge sans module ; vert assumé : refus à 1 chi. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : 3 activations ; 0 traceback. Résultat : OK.
- [x] Étape 8 bis : OUI (attache). Plateau « cinq Techniques sous l'identité ».

Carte terminée : OUI

### 64012 : Redirect Chi (Technique)

- [x] Étape 2 : Hero Resource payée en compteurs d'une autre carte → `phoenix/34001a` ; coût sur l'identité →
      `venus/tv001b` ; RECETTES §4 (une seule CanGenerateResources, condition obligatoire).
- [x] Étape 5 : icône wild vérifiée (voir l'en-tête) ; coût 2 chi (impayable à 1 : le Livre reste en main,
      cas) ; deux wild (`GG` : paie seul un coût 2, cas) ; Hero Resource absente en alter ego (cas).
      Résultat : OK.
- [x] Étape 6 : coût 0, [wild], 2 chi, 2 ressources. Résultat : OK.
- [x] Étape 7 : 3 cas, 1 rouge sans module ; verts assumés : 1 chi, alter ego. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : 24 parties, 0 traceback ; la carte est jouée (10 fois dans la 1re fournée) mais sa Ressource de
      héros n'a JAMAIS servi à payer (le pilote ne dépense pas le chi ainsi). Le code n'a tourné que dans les 3
      cas du harnais (dont le paiement réel du Livre par 2 wild).
- [x] Étape 8 bis : OUI (attache). Plateau « cinq Techniques sous l'identité ».

Carte terminée : NON — étape 8 non exercée : la Ressource de héros n'a payé aucune carte en partie.

## Gate héros (PROCESSUS-HEROS)

- Étapes 1-8 : cartes, scripts, deck de départ, `sets_info.json` (« 64. Iron Fist »), images PROVISOIRES
  (`assets/pics/<id>.png`, non versionnées), biographie `heros-info.js` (`64001a`, syntaxe vérifiée par
  `node --check` ; survol dans le wizard NON vérifié), texte FR provisoire `textes-fr-fanmade.ts`. Pas de
  `data/nemesis/` (rien de publié).
- « Carte terminée : OUI » : 64001a, 64001b, 64003, 64004, 64005, 64006, 64008, 64009, 64010, 64011.
  NON : 64002, 64007, 64012 (étape 8 non exercée par le pilote, voir ci-dessous).
- `verifier_tous_les_decks` (DECK_NOM=iron_fist) : vert.
- Partie complète : 24 parties d'autoplay ; aucune partie humaine.

**Héros terminé : NON** (trois cartes NON ci-dessus ; obligation et set némésis non publiés).

### Essai de partie dirigée pour 64002, 64007, 64012 (20/10/2026)

Deck de test `deck-dirige.json` (scratchpad de session, non versionné : identité + 15 signature + 10
ressources basiques), `autoplay.py --vilains rhino --profils equilibre --parties 4 --trace 2000`, graines
1-4 : 0 traceback, mais AUCUNE des trois capacités jouée. Pourquoi, d'après le pilote (`tools/autoplay.py`) :
- Deep Breathing : `scorer` note « Play » d'après des mots-clés du texte (`MOTS_TAGS`) ; « Discard cards …
  add it to your hand » n'en contient aucun, la carte vaut 0, sous « End Phase » (0,5) : le pilote ne la jouera
  JAMAIS, quel que soit le montage, sans modifier son barème ;
- Book of the Iron Fist : le Livre n'est entré en jeu dans aucune des 4 parties dirigées (3 fois dans les 24
  autres, sans que son Action soit prise) ;
- Redirect Chi : `payer()` compte UNE ressource par carte et dépense d'abord les cartes les plus chères ; la
  Technique (coût 0) n'est jamais choisie pour payer.
Le pilote ne peut donc pas fournir la preuve demandée sans toucher à son barème (outil partagé, non modifié).
Ces trois capacités restent prouvées par les cas du harnais seulement (vrai moteur, partie montée, coût
réellement payé pour Redirect Chi) ; à jouer à la main dans le navigateur.

# Shang-Chi (DesignHacker, SEALED) : gabarits PROCESSUS-CARTE, 22 card_id

Pack `shang_chi`, préfixe `ch` (deux lettres : `verifier_prefixes` ignore les ids à trois lettres), set 212. Source : zip
« SHANG-CHI (SEALED) » déposé le 24/10/2026. Cas : `Fusion/marvel-lcg-src/tools/cas/shang_chi.py` et `shang_chi_b.py` (filtre `[ch]`).
Plateau : `ui-app/src/board/shang-chi-plateau.test.ts`. Constructeur de deck : `tools/tests-lanceur/regles-shang-chi.test.mjs`.
Mot-clé maison : `docs/reference/mots-cles/flow.md`.

## Arbitrages utilisateur du 24/10/2026 (questions posées une à une, scan à l'appui)

1. **Meditate (`ch001b`)** : « shuffle a card from State of Flow » = une carte **au choix** de la pile (pas celle du dessus, pas toute la pile).
2. **Multiple Forms (`ch001b`)** : « chaque aspect autre que le vôtre » = Aggression, Justice, Leadership, Protection **plus** Determination,
   Venomized, 'Pool ; les voies TMNT (Taijutsu...) n'en sont pas. 1 titre ATTACK par autre aspect, 3 exemplaires.
3. **Flow** : correspondance **stricte** des icônes imprimées (un wild ne vaut que wild). L'icône étoile noire du Flow de Throat Punch a été
   découpée et comparée à l'étoile verte du coin de Dragon Strike 7/15 : même forme = wild.
4. **Special Delivery (`ch007`/`ch008`)** : « play the next ATTACK event from your hand at no cost » = **coût différé** (le prochain ATTACK
   que le joueur joue ce tour coûte 0).
5. **The Life Stealer (`ch020`)** : « 3 indirect damage to each hero and ally » = **3 dégâts directs** à chaque héros et allié.
6. **Downtown Attack (`ch021`)** : le joueur qui révèle choisit parmi **ses** alliés et **ses** cartes PERSONA.
7. **Augmented Blow (`ch013`/`ch014`)** : « additional counter » = un compteur du **même type** que ceux déjà présents (au choix s'il y en a
   plusieurs), sur toute amélioration en jeu qui porte au moins un compteur.
8. Pas de decklist d'aspect fournie : `player_deck` reste vide (PROCESSUS-HEROS étape 3).

## Points d'identification des cartes (pas des arbitrages)

- **Les « copy » du zip ne sont pas des doublons** : même dessin, icône de ressource imprimée différente (numéros 1/15 à 15/15 du bas de
  carte). Flow lit cette icône, donc 6 titres × 2 impressions = 12 card_id (`ch003`-`ch014`). Correspondance impression → icône(s) :
  Throat Punch 1/15 poing+mental, 2/15 mental ; Roundhouse 3/15 énergie, 4/15 poing+énergie ; Special Delivery 5/15 wild, 6/15 mental ;
  Dragon Strike 7/15 wild, 8/15 énergie ; Chi Jabs 9/15 wild, 10/15 poing ; Augmented Blow 11/15 énergie+mental, 12/15 poing.
- Le fichier du zip « UPGRADE - Golden Bracers » est la carte **Metal Bracers** (`ch016`) ; « Special Delivery copy » et consorts : voir ci-dessus.
- Homonymes de NOM au dépôt : `* Shang-Chi` (allié 63015/04098/dt025/56113), « Special Delivery » (16148), « The Life Stealer » (`sv014`).
  Aucun module du pack ne cherche par ces noms (tout passe par card_id).
- **Préfixe** : `sc` est pris (tmnt_shinobi_dual), 63015 est l'allié d'Iron Fist ; `shc` a été essayé puis abandonné (gate
  `verifier_prefixes` : deux lettres seulement). `ch` est libre.

## Gates du héros

- [x] Étapes 1 à 8 de PROCESSUS-HEROS : cartes (`cards.json`), scripts, deck de départ (`deck/starter/shang_chi.json`, `set_aside` = State of Flow,
      `metadata.deckbuilding` = Multiple Forms), `sets_info.json`, images (`assets/pics/ch*.jpg`, non versionnées ; la manigance annexe, couchée
      dans un fichier portrait, est tournée de 90°), biographie (`heros-info.js`, clé `ch001a`), textes FR (`textes-fr-fanmade.ts` + généré).
- [x] Étape 10 (aucune signature d'un autre héros) : les 15 cartes de `hero_deck` sont de classe `Hero`, set `Shang-Chi` ; `player_deck` vide.
- [x] `tools/verifier_tous_les_decks.py` : **155/155 decks montent une partie** (dont `shang_chi` : « identite ch001a, main 6, deck 9 »).
- [x] `tools/test_cards.py` : 7328 modules OK, 0 erreur ; `verifier_prefixes.py` OK ; `verifier_traductions_fr.py` OK.
- [x] Cas : **86 cas `[ch]` verts sur 86** ; preuve par substitution : **22/22 cartes** avec au moins un cas rouge sans leur module.
      Les cas qui restent verts sans module sont des contre-cas d'absence d'effet (refus du Flow, pas de Flow sans pile, forme alter-ego...) ou des
      valeurs imprimées, assumés dans chaque gabarit.
- [x] Constructeur de deck (Multiple Forms) : `tools/tests-lanceur/regles-shang-chi.test.mjs` 8/8, et les 112 tests des autres règles de
      `regles.js` toujours verts.
- [x] Plateau : `ui-app/src/board/shang-chi-plateau.test.ts` 8/8 (calibré ROUGE en mutant deux assertions) : la pile State of Flow, les compteurs
      charge / reflet / chi / mystique sont dessinés par le rendu générique, aucun correctif n'a été nécessaire.
- [x] Autoplay : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines) + témoin spider_man (16 parties), **0 traceback** sur les 32 journaux
      (`grep NameError|AttributeError|TypeError|KeyError|AssertionError` = 0). Les parties durent 3 rounds (témoin 6) : sans deck d'aspect (`player_deck`
      complété par des ressources inertes) le héros est fragile et le pilote ne prépare pas ses Flow.
- [ ] **Biographie au survol dans le wizard : NON VÉRIFIÉE dans le navigateur.** Le serveur du port 2345 appartient à une autre session et n'a pas été
      redémarré (la liste des héros vient des decks de départ lus au démarrage). La clé `ch001a` est présente dans `HEROS_INFO` et `app.js` lit
      `HEROS_INFO[h.heroCardId]` avec `heroCardId = deck.hero[0].split(',')[0] = "ch001a"` : à confirmer au prochain lancement.
- [ ] **Une partie complète jouée par un humain avec le héros : NON FAITE.** Aucun outil du projet ne la remplace (agrément du Flow, lisibilité de la
      pile, choix de Meditate / Augmented Blow). À faire avant de déclarer le héros terminé.
- Rappels « à vérifier en partie réelle » : la mise en place de State of Flow par le Setup de `ch001b` (vue au journal d'autoplay et par un cas, pas
  par un humain) ; l'ordre « remélange de la pile / remélange de la défausse avec pénalité » quand le deck se vide (le résultat est identique dans
  les deux ordres, mesuré au cas `ch002`).



### ch001a : Shang-Chi (Hero)

```
* Shang-Chi (face HEROS) — AVENGER. MARTIAL ARTIST. PV 9, THW 1, ATK 1, DEF 1, main 5.
Chi Mastery — Response: After you resolve a "Flow" ability, ready Shang-Chi.

Cartes de reference :
 - `01019a` * She-Hulk / `tg001a` * Throg : Response imprimee sur la face HEROS, « ready <le heros> » par
   `Faces.ReadyAll([this], effect)`.
 - message maison `AfterPlayerResolveFlow` (sender_player.py) + fabrique du meme nom (factory/setup.py), sur le
   modele de `AfterPlayerResolveMulligans` (bt001b) : le moteur n'avait aucun message pour un mot-cle maison.

⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
 - « Response » nu : optionnel (le moteur propose), pas « Hero Response » ; imprimee sur la face HEROS, donc muette
   en alter-ego (le Flow se resout de toute facon surtout en forme heros).
 - « After YOU resolve » : le Flow d'un autre joueur ne declenche rien (filtre de la fabrique).
 - « a Flow ability » : n'importe lequel des six Flow ; le message n'est envoye que si le joueur ACCEPTE de le resoudre
   (« you MAY also resolve its effects »), jamais pour un Flow refuse ou non correspondant.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ch001a Chi Mastery : apres un Flow resolu, Shang-Chi se redresse (Roundhouse Kick, dessus = Chi Jabs physique)
      - ch001a Chi Mastery : AUCUN Flow resolu (pile vide) -> Shang-Chi reste incline
      - ch001a Chi Mastery : le Flow est REFUSE (le joueur ne veut pas le resoudre) -> Shang-Chi reste incline, pas de 2 degats
      - ch001a Shang-Chi : valeurs imprimees PV 9, THW/ATK/DEF 1, AVENGER MARTIAL ARTIST
      Preuve par substitution : **rouges 1/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch001b : Shang-Chi (AlterEgo)

```
* Shang-Chi (face ALTER-EGO) — MARTIAL ARTIST. PV 9, REC 4, main 6.
Multiple Forms — You may include up to 3 copies of 1 ATTACK event from each aspect other than your chosen aspect.
Meditate — Response: After you change to this form, shuffle a card from State of Flow into your deck.
(+ mise en place : State of Flow, Permanent. Setup., entre en jeu.)

Cartes de reference :
 - Setup d'une carte mise de cote : `36001b` * Ororo Munroe (storm) : `BeginGameWithSetAside([...])` +
   `WhenCardSetup("This", op)` puis `PutIntoPlay`. State of Flow est « Permanent. Setup. » et n'est PAS une des 15 cartes
   du deck de heros (les impressions sont numerotees 1/15 a 15/15 sans elle) : elle part de cote.
 - Response au changement de forme : `tc001b` * Casey Jones : `AfterUnitChangeForm(Response, "You", op, to_this_form=True)`.
 - choix dans une liste donnee : `tc001b` (`ForChoiceAbility(...).SetTarget(liste, range=(1, 1), not_move=True)`).
 - Multiple Forms (CONSTRUCTION de deck, pas une capacite de jeu) : `metadata.deckbuilding.hors_aspect` du deck de
   depart, lu par `public/js/deckbuilder/regles.js` (`quotaHorsAspect`, etendu au quota PAR ASPECT).

⚠ Mots-pieges :
 - « shuffle A CARD from State of Flow » : DECISION UTILISATEUR (24/10/2026) = une carte AU CHOIX de la pile (pas celle
   du dessus, pas toute la pile). Pile vide : rien.
 - « After you change TO THIS FORM » : `to_this_form=True` ; au Setup la partie commence en alter-ego sans changement.
 - la pile garde ses autres cartes ; la carte choisie est melangee dans LE DECK DU JOUEUR (pas la defausse).
 - « Multiple Forms » n'a aucun code de jeu : il se prouve cote constructeur (cas Node regles-deck).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - ch001b Meditate : apres le changement de forme vers l'alter-ego, une carte AU CHOIX de la pile retourne dans le deck
      - ch001b Meditate : la pile perd la carte choisie et garde l'autre
      - ch001b Meditate : pile vide -> rien ne se passe, le deck ne grossit pas
      - ch001b Meditate : absente quand on passe a la forme HEROS (la Response est imprimee sur l'alter-ego)
      - ch001b Shang-Chi : valeurs imprimees PV 9, MARTIAL ARTIST
      - ch001b State of Flow : EN JEU des la mise en place (Setup, carte mise de cote par ch001b), aucune pile
      Preuve par substitution : **rouges 3/6** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : Meditate sort une carte de la pile State of Flow vers le deck (la pile se lit sur le plateau). Cas plateau : ui-app/src/board/shang-chi-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch002 : State of Flow (Support)

```
State of Flow — SOUTIEN. Permanent. Setup. (card_id ch002, pas dans les 15 cartes du deck de heros)
Forced Response: After you play an ATTACK event, place it faceup on top here, forming a pile. After the player deck
  runs out, shuffle each card placed here back into the player deck.
Keyword - Flow: Look at the top card here. If a printed resource on that card matches the resource required by the
  "Flow" ability, you may also resolve its effects.

Cartes de reference :
 - `gs117a` / `gs119` (Galactic Storm) : « tuck » face VISIBLE = `hote.PlaceCardHere(faces, True, effect)` ; les
   cartes posees vivent dans `hote.GetPlacedCardArea()`.
 - `sk288` Sy-Torak Gem / `aa012` Regained Youth : « after your deck runs out » = `AfterDeckRunOut(type, deck_du_joueur, op)`.
 - `28002` Ms. Marvel : `AfterPlayerPlayedCard(type, "You", CardFinder(...), op)`.
 - le mot-cle Flow lui-meme : helpers `AccepterFlow` / `FlowResolu` du set (fiche mots-cles/flow.md).

⚠ Mots-pieges :
 - « Permanent » et « Setup » : bases automatiques du moteur (`desc.Permanent`/`desc.Setup`) ; l'entree en jeu se fait par
   ch001b (mise de cote, comme Storm) : aucun code ici.
 - « After YOU play an ATTACK event » : un evenement ATTACK du joueur seulement (trait ATTACK, type Event), jamais un
   evenement d'un autre joueur ni une carte sans ce trait.
 - le Forced Response passe APRES la defausse de l'evenement (Event.OnAfterPlay defausse avant d'envoyer
   AfterPlayerPlayedCard) : on le RETIRE donc de la defausse pour le poser sur la pile ; si une autre carte l'a deja
   deplace (retour en main...), on n'y touche pas.
 - « place it faceup on TOP here » : la derniere jouee est le dessus ; le Flow suivant regarde celle-la.
 - « After the player deck runs out » : `AfterDeckRunOut` part quand le DERNIER tirage vide le deck ; chaque carte de la
   pile retourne dans LE DECK DU JOUEUR (melange). Le moteur remelange ensuite la defausse avec penalite comme d'habitude.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ch002 State of Flow : une attaque jouee (Chi Jabs) se pose face visible sur la pile et quitte la defausse
      - ch002 State of Flow : deux attaques de suite, la DERNIERE est le dessus (le Flow de la 3e lit celle-la)
      - ch002 State of Flow : un evenement qui n'est PAS une attaque (For Justice!) reste a la defausse
      - ch002 State of Flow : deck vide apres une pioche -> toute la pile retourne dans le deck du joueur
      Preuve par substitution : **rouges 3/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : la pile d'attaques glissees FACE VISIBLE sous le soutien. Cas plateau : ui-app/src/board/shang-chi-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch003 : Throat Punch (Event)

```
Throat Punch — EVENEMENT, cout 0, impression 1/15 : ressource(s) imprimee(s) physique + mental. ATTACK. (card_id ch003)
Hero Action (attack): Deal 1 damage to the villain. Draw a card.
Flow: [wild] → draw 2 additional cards.

⚠ IMPRESSIONS : Throat Punch existe en DEUX cartes (ch004) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `01087` Haymaker (`SetPlay().SetLabel('attack').SetTarget(...)`) ; cible VILAIN : `27015` / `sm/27017` (`SetTarget(Villain)`).
 - pioche : `joueur.DrawUp(n, effect)` (`nt005`).

⚠ Mots-pieges :
 - « the VILLAIN » : cible unique (le vilain), pas « an enemy ».
 - Flow [wild] : une icone WILD (etoile) exigee, donc la carte du dessus doit IMPRIMER un wild (correspondance stricte).
 - « 2 ADDITIONAL cards » : 1 + 2 = 3 cartes au total ; le Flow s'ajoute a la pioche, ne la remplace pas.
 - le Flow est facultatif (« you MAY also resolve »).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ch003 Throat Punch : 1 degat au vilain et pioche 1 carte (pile vide, pas de Flow), puis se pose sur State of Flow
      - ch003 Throat Punch : Flow [wild], le dessus (Special Delivery, wild imprime) -> 2 cartes de plus (1 + 2 = 3) ; Shang-Chi se redresse
      - ch003 Throat Punch : le dessus n'imprime PAS de wild (Dragon Strike energie) -> pas de Flow, 1 carte seulement, Shang-Chi reste incline
      - ch003 Throat Punch : le dessus imprime poing + energie (Roundhouse 4/15), aucun wild -> pas de Flow
      Preuve par substitution : **rouges 2/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch004 : Throat Punch (Event)

```
Throat Punch — EVENEMENT, cout 0, impression 2/15 : ressource(s) imprimee(s) mental. ATTACK. (card_id ch004)
Hero Action (attack): Deal 1 damage to the villain. Draw a card.
Flow: [wild] → draw 2 additional cards.

⚠ IMPRESSIONS : Throat Punch existe en DEUX cartes (ch003) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `01087` Haymaker (`SetPlay().SetLabel('attack').SetTarget(...)`) ; cible VILAIN : `27015` / `sm/27017` (`SetTarget(Villain)`).
 - pioche : `joueur.DrawUp(n, effect)` (`nt005`).

⚠ Mots-pieges :
 - « the VILLAIN » : cible unique (le vilain), pas « an enemy ».
 - Flow [wild] : une icone WILD (etoile) exigee, donc la carte du dessus doit IMPRIMER un wild (correspondance stricte).
 - « 2 ADDITIONAL cards » : 1 + 2 = 3 cartes au total ; le Flow s'ajoute a la pioche, ne la remplace pas.
 - le Flow est facultatif (« you MAY also resolve »).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ch004 Throat Punch (mental seul) : seule la carte du DESSUS compte (un wild plus bas dans la pile ne sert a rien)
      - ch004 Throat Punch (mental seul) : Flow [wild] avec un dessus wild -> 3 cartes au total
      Preuve par substitution : **rouges 1/2** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch005 : Roundhouse Kick (Event)

```
Roundhouse Kick — EVENEMENT, cout 0, impression 3/15 : ressource(s) imprimee(s) energie. ATTACK. (card_id ch005)
Hero Action (attack): Deal 1 damage to an enemy.
Flow (attack): [physical] → deal 2 damage to an enemy.

⚠ IMPRESSIONS : Roundhouse Kick existe en DEUX cartes (ch006) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `64004` Fists of Fury : deux phrases « Deal N damage to an enemy » = deux choix de cible INDEPENDANTS
   (`SetTarget(Enemy)` pour le premier, `ChooseAbilities(ForChoiceAbility(...).SetTarget(Enemy))` pour le suivant).

⚠ Mots-pieges :
 - « an enemy » deux fois : la 2e cible se choisit a part (peut etre la meme si elle survit).
 - Flow [physical] : la carte du dessus doit IMPRIMER un poing ; « (attack) » : ses 2 degats sont une attaque (`DealDamage`
   depuis l'evenement, label deja pose sur le Hero Action).
 - les 2 degats s'AJOUTENT au 1 : jamais 2 a la place de 1.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ch005 Roundhouse Kick : 1 degat a un ennemi (pile vide, pas de Flow)
      - ch005 Roundhouse Kick : Flow [physical], dessus = Chi Jabs poing -> 2 degats de plus a un AUTRE ennemi choisi a part (le sbire a 1 PV meurt du 1er coup, le 2e frappe le vilain)
      - ch005 Roundhouse Kick : le dessus n'imprime pas de poing (Dragon Strike energie) -> 1 degat seulement
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch006 : Roundhouse Kick (Event)

```
Roundhouse Kick — EVENEMENT, cout 0, impression 4/15 : ressource(s) imprimee(s) physique + energie. ATTACK. (card_id ch006)
Hero Action (attack): Deal 1 damage to an enemy.
Flow (attack): [physical] → deal 2 damage to an enemy.

⚠ IMPRESSIONS : Roundhouse Kick existe en DEUX cartes (ch005) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `64004` Fists of Fury : deux phrases « Deal N damage to an enemy » = deux choix de cible INDEPENDANTS
   (`SetTarget(Enemy)` pour le premier, `ChooseAbilities(ForChoiceAbility(...).SetTarget(Enemy))` pour le suivant).

⚠ Mots-pieges :
 - « an enemy » deux fois : la 2e cible se choisit a part (peut etre la meme si elle survit).
 - Flow [physical] : la carte du dessus doit IMPRIMER un poing ; « (attack) » : ses 2 degats sont une attaque (`DealDamage`
   depuis l'evenement, label deja pose sur le Hero Action).
 - les 2 degats s'AJOUTENT au 1 : jamais 2 a la place de 1.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ch006 Roundhouse Kick (poing + energie) : Flow resolu grace a un dessus qui imprime DEUX icones dont un poing (Roundhouse 4/15)
      - ch006 Roundhouse Kick : Flow REFUSE -> seulement 1 degat (pas de 2e coup)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch007 : Special Delivery (Event)

```
Special Delivery — EVENEMENT, cout 2, impression 5/15 : ressource(s) imprimee(s) wild. ATTACK. (card_id ch007)
Hero Action (attack): Deal 3 damage to an enemy. If this is the first event you have played this phase, confuse an enemy.
Flow: [mental] → if this attack defeats an enemy, play the next ATTACK event from your hand at no cost.

⚠ IMPRESSIONS : Special Delivery existe en DEUX cartes (ch008) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `nt005` Kickflip : « la carte jouee est DEJA dans `stat.this_*_played_cards` quand son effet se resout » (a exclure).
 - `mf012` / `05015` : `Faces.GiveStatus(cibles, "Confused", effect)`.
 - cout differe : `Worlds.UpdateNextCardPlayCost(joueur, 0, effect, update_to=True, finder=..., in_this="Turn")`
   (`dz003`, `01092`), recette RECETTES-MOTEUR §0 ligne « la prochaine carte que tu joues ».

⚠ Mots-pieges :
 - « the FIRST event you have played this phase » : les evenements deja joues cette phase par CE joueur, hors cette carte.
 - « confuse AN enemy » : un ennemi au choix (autre cible que l'attaque possible), seulement si c'est le premier evenement.
 - Flow [mental] : exige un mental imprime sur la carte du dessus ; « if this attack DEFEATS an enemy » : la cible de l'attaque
   doit avoir ete VAINCUE (plus en jeu) apres les 3 degats ; sinon rien (le Flow est tout de meme resolu : Chi Mastery).
 - DECISION UTILISATEUR (24/10/2026) : « play the next ATTACK event » = COUT DIFFERE : le prochain evenement ATTACK que le
   joueur JOUE ce tour coute 0 ; il garde le choix et l'ordre. Fenetre « ce tour ».
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - ch007 Special Delivery : 3 degats a un ennemi ; PREMIER evenement de la phase -> desoriente un ennemi
      - ch007 Special Delivery : PAS le premier evenement de la phase (Throat Punch avant) -> aucun ennemi desoriente
      - ch007 Special Delivery : Flow [mental], dessus = Throat Punch (mental), l'attaque ACHEVE le sbire -> la prochaine attaque est gratuite
      - ch007 Special Delivery : le sbire SURVIT (4 PV Sandman, 3 degats) -> pas de gratuite : la 2e attaque (cout 1) reste dans la main
      - ch007 Special Delivery : le dessus n'imprime pas de mental (Dragon Strike energie) -> pas de Flow, meme si le sbire meurt
      Preuve par substitution : **rouges 5/5** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch008 : Special Delivery (Event)

```
Special Delivery — EVENEMENT, cout 2, impression 6/15 : ressource(s) imprimee(s) mental. ATTACK. (card_id ch008)
Hero Action (attack): Deal 3 damage to an enemy. If this is the first event you have played this phase, confuse an enemy.
Flow: [mental] → if this attack defeats an enemy, play the next ATTACK event from your hand at no cost.

⚠ IMPRESSIONS : Special Delivery existe en DEUX cartes (ch007) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `nt005` Kickflip : « la carte jouee est DEJA dans `stat.this_*_played_cards` quand son effet se resout » (a exclure).
 - `mf012` / `05015` : `Faces.GiveStatus(cibles, "Confused", effect)`.
 - cout differe : `Worlds.UpdateNextCardPlayCost(joueur, 0, effect, update_to=True, finder=..., in_this="Turn")`
   (`dz003`, `01092`), recette RECETTES-MOTEUR §0 ligne « la prochaine carte que tu joues ».

⚠ Mots-pieges :
 - « the FIRST event you have played this phase » : les evenements deja joues cette phase par CE joueur, hors cette carte.
 - « confuse AN enemy » : un ennemi au choix (autre cible que l'attaque possible), seulement si c'est le premier evenement.
 - Flow [mental] : exige un mental imprime sur la carte du dessus ; « if this attack DEFEATS an enemy » : la cible de l'attaque
   doit avoir ete VAINCUE (plus en jeu) apres les 3 degats ; sinon rien (le Flow est tout de meme resolu : Chi Mastery).
 - DECISION UTILISATEUR (24/10/2026) : « play the next ATTACK event » = COUT DIFFERE : le prochain evenement ATTACK que le
   joueur JOUE ce tour coute 0 ; il garde le choix et l'ordre. Fenetre « ce tour ».
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - ch008 Special Delivery (mental) : meme effet de base, 3 degats et ennemi desoriente en premier evenement
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch009 : Dragon Strike (Event)

```
Dragon Strike — EVENEMENT, cout 2, impression 7/15 : ressource(s) imprimee(s) wild. ATTACK. (card_id ch009)
Hero Action (attack): Deal 5 damage to an enemy.
Flow: [energy] → this attack gains piercing, ranged, and overkill.

⚠ IMPRESSIONS : Dragon Strike existe en DEUX cartes (ch010) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `nt006` Melon Grab : `DealDamage(cibles, N, effect, property=AttackProperty(piercing=True, overkill=True))` ;
   `ra007` : `AttackProperty(ranged=True)`.

⚠ Mots-pieges :
 - le Flow modifie l'ATTAQUE : il est resolu AVANT les degats (sinon rien a modifier) ; Flow [energy] exige un eclair imprime.
 - piercing + ranged + overkill ensemble : les trois proprietes ou aucune.
 - 5 degats dans les deux cas : le Flow ne change pas le nombre.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - ch009 Dragon Strike : 5 degats a un sbire de 3 PV SANS Flow -> pas d'overkill, le vilain ne prend rien
      - ch009 Dragon Strike : Flow [energy], dessus = Dragon Strike energie -> overkill : 5 - 3 = 2 degats d'exces au vilain
      - ch009 Dragon Strike : Flow [energy] + sbire ROBUSTE (tough) -> piercing : le sbire prend les 5 degats malgre le statut
      - ch009 Dragon Strike : SANS Flow contre un sbire robuste -> la robustesse absorbe l'attaque (aucun degat)
      - ch009 Dragon Strike : Flow [energy] contre M.O.D.O.K. (riposte 2, 8 PV) -> ranged : Shang-Chi ne prend pas la riposte
      - ch009 Dragon Strike : SANS Flow contre M.O.D.O.K. -> la riposte 2 touche Shang-Chi
      Preuve par substitution : **rouges 6/6** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch010 : Dragon Strike (Event)

```
Dragon Strike — EVENEMENT, cout 2, impression 8/15 : ressource(s) imprimee(s) energie. ATTACK. (card_id ch010)
Hero Action (attack): Deal 5 damage to an enemy.
Flow: [energy] → this attack gains piercing, ranged, and overkill.

⚠ IMPRESSIONS : Dragon Strike existe en DEUX cartes (ch009) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `nt006` Melon Grab : `DealDamage(cibles, N, effect, property=AttackProperty(piercing=True, overkill=True))` ;
   `ra007` : `AttackProperty(ranged=True)`.

⚠ Mots-pieges :
 - le Flow modifie l'ATTAQUE : il est resolu AVANT les degats (sinon rien a modifier) ; Flow [energy] exige un eclair imprime.
 - piercing + ranged + overkill ensemble : les trois proprietes ou aucune.
 - 5 degats dans les deux cas : le Flow ne change pas le nombre.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ch010 Dragon Strike (energie) : le dessus ne porte que du wild (Chi Jabs wild) -> pas de Flow [energy]
      - ch010 Dragon Strike (energie) : Flow resolu, overkill 5 - 3 = 2 sur le vilain
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch011 : Chi Jabs (Event)

```
Chi Jabs — EVENEMENT, cout 1, impression 9/15 : ressource(s) imprimee(s) wild. ATTACK. (card_id ch011)
Hero Action (attack): Choose up to 3 different enemies. Deal 1 damage to each of them.
Flow (attack): [physical] → deal 2 damage to the villain.

⚠ IMPRESSIONS : Chi Jabs existe en DEUX cartes (ch012) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `10005` Thunderclap : « Choose up to 3 different enemies. Deal N damage to each » = `SetTarget(Enemy, range=(1, 3))`.
 - cible VILAIN : `27015` (`Villain`, `SetTarget`).

⚠ Mots-pieges :
 - « up to 3 DIFFERENT enemies » : le ciblage standard interdit les doublons.
 - Flow [physical] : un poing imprime exige sur la carte du dessus ; « the VILLAIN » : degats au vilain (pas a un ennemi au choix).
 - 2 degats s'ajoutent au 1 deja inflige au vilain s'il etait une des cibles.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ch011 Chi Jabs : jusqu'a 3 ennemis DIFFERENTS, 1 degat a chacun (vilain, Shocker, Weapons Runner)
      - ch011 Chi Jabs (wild) : le dessus est un wild (Dragon Strike wild) mais le Flow exige un POING -> pas de Flow
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch012 : Chi Jabs (Event)

```
Chi Jabs — EVENEMENT, cout 1, impression 10/15 : ressource(s) imprimee(s) physique. ATTACK. (card_id ch012)
Hero Action (attack): Choose up to 3 different enemies. Deal 1 damage to each of them.
Flow (attack): [physical] → deal 2 damage to the villain.

⚠ IMPRESSIONS : Chi Jabs existe en DEUX cartes (ch011) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `10005` Thunderclap : « Choose up to 3 different enemies. Deal N damage to each » = `SetTarget(Enemy, range=(1, 3))`.
 - cible VILAIN : `27015` (`Villain`, `SetTarget`).

⚠ Mots-pieges :
 - « up to 3 DIFFERENT enemies » : le ciblage standard interdit les doublons.
 - Flow [physical] : un poing imprime exige sur la carte du dessus ; « the VILLAIN » : degats au vilain (pas a un ennemi au choix).
 - 2 degats s'ajoutent au 1 deja inflige au vilain s'il etait une des cibles.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ch012 Chi Jabs : Flow [physical], dessus = Roundhouse poing+energie -> 2 degats de plus AU VILAIN (1 + 2 = 3)
      - ch012 Chi Jabs : le Flow vise le VILAIN meme si le sbire etait la seule cible des jabs
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch013 : Augmented Blow (Event)

```
Augmented Blow — EVENEMENT, cout 1, impression 11/15 : ressource(s) imprimee(s) energie + mental. ATTACK. (card_id ch013)
Hero Action (attack): Deal 1 damage to a minion. Place 1 additional counter on an upgrade with any type of counters on it.
Flow: [energy] → choose up to 2 upgrades with any type of counter on them. Place 2 additional counters on each of them.

⚠ IMPRESSIONS : Augmented Blow existe en DEUX cartes (ch014) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `64004`/`10005` pour le Hero Action (attack) ; cible sbire : `bw002` (`SetTarget(Minion)`).
 - compteurs : `Faces.PlaceCountersOn([amelioration], n, nom, effect)` (`dz002`) ; lecture `face.components.counter.counters`.
 - liste de cibles fournie : `tc001b` (`SetTarget(liste, range=..., not_move=True)`).

⚠ Mots-pieges :
 - DECISION UTILISATEUR (24/10/2026) : « ADDITIONAL counter » = un compteur du MEME TYPE que ceux deja presents (au choix s'il y a
   plusieurs types) ; toute amelioration EN JEU avec au moins un compteur est cible (pas seulement celles de Shang-Chi).
 - « an upgrade WITH counters » : une amelioration sans compteur n'est PAS ciblable.
 - Flow : « up to 2 » ameliorations, 2 compteurs sur CHACUNE ; Flow [energy] exige un eclair imprime.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - ch013 Augmented Blow : 1 degat a un sbire et 1 compteur de plus sur une amelioration qui en porte (Stark Nunchaku : charge 3 -> 4)
      - ch013 Augmented Blow : une amelioration SANS compteur n'est pas ciblable -> aucun compteur pose
      - ch013 Augmented Blow : Flow [energy] (dessus = Dragon Strike energie) -> 2 ameliorations, 2 compteurs de plus chacune
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : pose des compteurs sur les ameliorations. Cas plateau : ui-app/src/board/shang-chi-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch014 : Augmented Blow (Event)

```
Augmented Blow — EVENEMENT, cout 1, impression 12/15 : ressource(s) imprimee(s) physique. ATTACK. (card_id ch014)
Hero Action (attack): Deal 1 damage to a minion. Place 1 additional counter on an upgrade with any type of counters on it.
Flow: [energy] → choose up to 2 upgrades with any type of counter on them. Place 2 additional counters on each of them.

⚠ IMPRESSIONS : Augmented Blow existe en DEUX cartes (ch013) qui ne different que par l'ICONE DE RESSOURCE du coin ;
  `ch` les separe parce que le Flow de la carte SUIVANTE lit cette icone (correspondance stricte, decision du 24/10).

Cartes de reference :
 - `64004`/`10005` pour le Hero Action (attack) ; cible sbire : `bw002` (`SetTarget(Minion)`).
 - compteurs : `Faces.PlaceCountersOn([amelioration], n, nom, effect)` (`dz002`) ; lecture `face.components.counter.counters`.
 - liste de cibles fournie : `tc001b` (`SetTarget(liste, range=..., not_move=True)`).

⚠ Mots-pieges :
 - DECISION UTILISATEUR (24/10/2026) : « ADDITIONAL counter » = un compteur du MEME TYPE que ceux deja presents (au choix s'il y a
   plusieurs types) ; toute amelioration EN JEU avec au moins un compteur est cible (pas seulement celles de Shang-Chi).
 - « an upgrade WITH counters » : une amelioration sans compteur n'est PAS ciblable.
 - Flow : « up to 2 » ameliorations, 2 compteurs sur CHACUNE ; Flow [energy] exige un eclair imprime.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - ch014 Augmented Blow (poing) : un compteur du MEME TYPE que ceux presents (chi sur Martial Mastery, pas charge)
      - ch014 Augmented Blow : Flow refuse -> un seul compteur de plus (le Hero Action) et pas les 2 du Flow
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : pose des compteurs sur les ameliorations. Cas plateau : ui-app/src/board/shang-chi-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch015 : Stark Nunchaku (Upgrade)

```
Stark Nunchaku — AMELIORATION, cout 3, [energy]. WEAPON. (card_id ch015, 13/15)
Restricted. Enters play with 3 charge counters on it.
Hero Action: Exhaust Stark Nunchaku and remove 2 charge counters from it → stun an enemy.

Cartes de reference :
 - `dz002` : `AbilityFactory.ThisEnterPlayWithCounters(N, 'nom')` (« enters play with N counters »).
 - `sh010` Martial Skill / `ua033` Pete : cout double `SetCostFunc(CostFunc.Exhaust("This"))` + `SetCostFunc(CostFunc.Counter("This", N, 'nom'))`.
 - `01083` / `05015` : `Faces.GiveStatus(cibles, "Stunned", effect)` avec `SetTarget(Enemy, canbe_stunned=True)`.

⚠ Mots-pieges :
 - « Restricted » : base automatique (`desc.Restricted`), aucun code.
 - « remove 2 charge counters » : DEUX, pas un ; `CostFunc.Counter` seul est offert meme impayable (RECETTES §5) : une condition
   verifie les 2 compteurs. 3 compteurs au depart = UN seul usage complet (3 - 2 = 1 < 2).
 - « Hero Action » : en forme heros seulement ; « stun AN enemy » : cible obligatoire (un STALWART n'est pas ciblable).
 - Pas de limite imprimee (le cout le borne).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - ch015 Stark Nunchaku : entre en jeu avec 3 compteurs charge
      - ch015 Stark Nunchaku : Hero Action, incline la carte, retire 2 charges et ETOURDIT un ennemi (3 -> 1)
      - ch015 Stark Nunchaku : avec 1 seule charge, l'action n'est pas offerte (les 2 compteurs sont un COUT)
      - ch015 Stark Nunchaku : deja inclinee -> l'action n'est pas offerte
      - ch015 Stark Nunchaku : absente en ALTER-EGO (Hero Action inutilisable)
      - ch015 Stark Nunchaku : trait WEAPON imprime
      Preuve par substitution : **rouges 5/6** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : compteurs charge. Cas plateau : ui-app/src/board/shang-chi-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch016 : Metal Bracers (Upgrade)

```
Metal Bracers — AMELIORATION, cout 3, [physical]. ARMOR. (card_id ch016, 14/15)
Shang-Chi gets +1 DEF. Enters play with 2 reflection counters on it.
Hero Action: Exhaust Metal Bracers and remove 2 reflection counters from it → give Shang-Chi a tough status card.
(Le fichier du zip s'appelle « Golden Bracers » : la carte imprimee est Metal Bracers.)

Cartes de reference :
 - `60038` : `*AbilityFactory.GiveKeywordToAttached(Hero, defense=1)` (+1 DEF au heros porteur).
 - `dz002` : `ThisEnterPlayWithCounters` ; `ch015` (meme pack) : cout double incline + compteurs.
 - `ra006` / `90123` : `Faces.GiveStatus([identite], "Tough", effect)`.

⚠ Mots-pieges :
 - « Shang-Chi gets +1 DEF » : la face HEROS (l'alter-ego n'a pas de DEF) : `Hero`, pas l'identite quelle qu'elle soit.
 - « remove 2 reflection counters » : DEUX ; condition de paiement posee a la main (RECETTES §5).
 - « give SHANG-CHI a tough status card » : la carte de statut va au HEROS du joueur (pas a un allie) ; un heros deja
   robuste n'en recoit pas une seconde (le moteur refuse un 2e statut identique).
 - « Hero Action » : forme heros seulement.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - ch016 Metal Bracers : entre en jeu avec 2 compteurs reflection
      - ch016 Metal Bracers : Hero Action, incline, retire 2 compteurs et donne un statut Tough a Shang-Chi
      - ch016 Metal Bracers : sans les 2 compteurs, l'action n'est pas offerte
      - ch016 Metal Bracers : +1 DEF : Shocker (ATK 2) attaque, Shang-Chi defend avec DEF 1 + 1 = 2 et ne prend aucun degat
      - ch016 Metal Bracers : SANS les bracelets, la meme defense (DEF 1) laisse passer 1 degat
      - ch016 Metal Bracers : en ALTER-EGO, Hero Action absente
      Preuve par substitution : **rouges 5/6** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : compteurs reflet. Cas plateau : ui-app/src/board/shang-chi-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch017 : Martial Mastery (Upgrade)

```
Martial Mastery — AMELIORATION, cout 2, [wild]. SKILL. (card_id ch017, 15/15)
Uses (3 chi counters).
Hero Interrupt: When you use one of your hero's basic powers (THW, ATK, or DEF), exhaust Martial Mastery and remove
  1 chi counter from it → your hero gets +1 to that power for this use.

Cartes de reference :
 - `20010` Venom's Pistol / `tg009` Frogjolnir : `WhenUnitUseBasicPower(HeroInterrupt, ..., op)` + `message.GainValue(+1, effect)`
   (« +1 to that power for this use » : `GainValue` route vers ATK/THW/DEF selon le pouvoir).
 - `sh010` Martial Skill : `desc.Uses = "N,chi"` + double cout `Exhaust("This")` + `Counter("This", 1, 'chi')`.

⚠ Mots-pieges :
 - « Uses (3 chi counters) » : natif (`desc.Uses`) ; la carte quitte le jeu au DERNIER compteur retire : ne PAS coder la sortie.
 - « basic powers (THW, ATK, or DEF) » : PAS la recuperation (REC de l'alter-ego) : `powers=["THW", "ATK", "DEF"]`.
 - « YOUR hero » : le heros que contrôle le porteur de l'amelioration (`control_by="You"`), pas le heros d'un autre joueur.
 - « +1 for THIS USE » : pour cet usage seulement (pas pour le round).
 - le cout est le double (incliner ET retirer 1 compteur) ; avec 0 compteur la carte a deja quitte le jeu.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - ch017 Martial Mastery : entre en jeu avec 3 compteurs chi (Uses)
      - ch017 Martial Mastery : attaque de base, +1 ATK (1 -> 2 degats), incline + 1 chi retire
      - ch017 Martial Mastery : pouvoir THW, +1 (1 -> 2 menaces retirees)
      - ch017 Martial Mastery : deja inclinee -> aucun bonus (attaque a 1)
      - ch017 Martial Mastery : dernier compteur chi retire -> la carte quitte le jeu (Uses)
      Preuve par substitution : **rouges 3/5** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : compteurs chi. Cas plateau : ui-app/src/board/shang-chi-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch018 : Family Ties (Obligation)

```
Family Ties — Obligation (set « Shang-Chi »), Boost 2, « Give to the Shang-Chi player ».
You may flip to alter-ego form. Choose:
 • Deal 2 damage to Shang-Chi → remove Family Ties from the game.
 • Deal 2 damage to each ally. Discard this obligation.

Cartes de reference :
 - `sv011` Silver Down (silver_surfer) : MEME squelette — `WhenThisObligationGiveToYou`, `YouMayFlipToYourAlterEgoForm`,
   puis `joueur.ChooseAbilities` avec `condition=` par branche.
 - `45113` / `aoa` : `this.DealDamage(unites, N, effect)` ; allies en jeu : `Worlds.FindCardsOnField(effect, card_type=Ally)`.

⚠ Mots-pieges :
 - 1re branche : « → remove FROM THE GAME » (jamais defausse) ; 2e branche : « DISCARD this obligation » : les deux sorties
   DIFFERENTES de la meme carte (hc013 : une obligation reste en jeu tant qu'on ne la deplace pas).
 - « Deal 2 damage to SHANG-CHI » est devant la fleche : un COUT (paye en degats a l'identite, forme comprise).
 - « each ALLY » : tous les allies en jeu (le texte ne dit pas « you control »), 2 degats chacun ; sans allie la branche
   reste jouable (elle ne fait que defausser l'obligation).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - ch018 Family Ties : branche 1 -> 2 degats a Shang-Chi et l'obligation est RETIREE de la partie
      - ch018 Family Ties : branche 2 -> 2 degats a CHAQUE allie (Mockingbird, Nick Fury) et l'obligation est DEFAUSSEE, Shang-Chi indemne
      - ch018 Family Ties : branche 2 SANS allie -> reste jouable : l'obligation part quand meme
      - ch018 Family Ties : branche 1 avec un allie -> l'allie n'est PAS blesse (les 2 degats vont a Shang-Chi seul)
      - ch018 Family Ties : en forme HEROS au moment de la revelation, l'obligation propose le retournement en alter-ego
      Preuve par substitution : **rouges 5/5** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch019 : Zheng Zu (Minion)

```
* Zheng Zu (sbire NEMESIS de Shang-Chi) — PV 6, SCH 2, ATK 1★, boost 2. ELITE. MYSTIC.
Forced Response: After Zheng Zu schemes, place 1 mystic counter here.
[star] Zheng Zu gets +1 ATK for each mystic counter here.

Cartes de reference :
 - `nt013` (night_thrasher_nemesis) / `08012` : `AfterUnitSchemeEnd(ForcedResponse, "This", op)` (« after X schemes »).
 - `64009` Embody the Dragon : valeur dynamique par compteur, `GiveKeywordToInPlayWhenApplyThis(finder, get_new_value=fn,
   change_on_event=OnEvent.Counter("This", 'nom'))` ; `64001a` pour le compteur pose.
 - `mystic` est deja un compteur connu du moteur (`CardFace.COUNTER`).

⚠ Mots-pieges :
 - « After Zheng Zu SCHEMES » : sa propre activation de manigance (ATTAQUE exclue) ; le compteur se pose APRES (Forced Response).
 - « +1 ATK FOR EACH mystic counter here » : ATK de base 1 + N compteurs ; la valeur imprimee « 1★ » vaut 1 de base.
   Sans compteur : ATK 1.
 - les compteurs restent sur LUI (« here »), pas sur la manigance annexe (ch020 compte les siens a part).
 - « Shang-Chi's nemesis minion » : `desc.Nemesis`, rien a coder.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - ch019 Zheng Zu : valeurs imprimees PV 6, ATK 1 (sans compteur), ELITE MYSTIC
      - ch019 Zheng Zu : apres une MANIGANCE, 1 compteur mystic ici et ATK 2
      - ch019 Zheng Zu : deux manigances -> 2 compteurs, ATK 3 (le bonus suit le nombre de compteurs)
      - ch019 Zheng Zu : une ATTAQUE (pas une manigance) ne pose aucun compteur
      Preuve par substitution : **rouges 2/4** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou de valeurs imprimées, assumés). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : compteurs mystiques sur le sbire nemesis. Cas plateau : ui-app/src/board/shang-chi-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch020 : The Life Stealer (SideScheme)

```
The Life Stealer — MANIGANCE ANNEXE NEMESIS (4 par heros, Victory 1). (card_id ch020, 2/5)
Victory 1.
Forced Response: After resolving step one of the villain phase, place 1 mystic counter here. After a third mystic counter is
  placed here, deal 3 indirect damage to each hero and ally in play and remove The Life Stealer from the game.

Cartes de reference :
 - `01107` Breakin' & Takin' : menace PAR HERO posee a la revelation, `this.PlaceThreatOnSchemes([this], "1*", effect)`
   (la valeur « N* » = N par joueur ; ici « 4* »).
 - `pu033` / `39026b` : `AbilityFactory.AfterResolveVillainPhaseStep(type, 1, op)` (etape 1 de la phase du vilain).
 - `45113` / `27071` : `this.DealDamage(Worlds.GetOnFieldFriendlyCharacters(effect), N, effect)`.
 - `Victory` : base automatique (`desc.Victory`).

⚠ Mots-pieges :
 - « 4 [per hero] » : menace de depart 4 PAR HERO (le scan imprime 4 + icone joueur) : posee par un « When Revealed » de la
   carte (`desc.StartingThreat = 0`), comme les manigances annexes officielles a menace par joueur.
 - « After a THIRD mystic counter is placed » : au 3e, pas au 1er ni au 2e ; la carte part ENSUITE.
 - DECISION UTILISATEUR (24/10/2026) : « deal 3 indirect damage to each hero and ally » = 3 degats DIRECTS a CHAQUE heros et
   allie en jeu (aucune repartition).
 - « remove The Life Stealer FROM THE GAME » : jamais defausse, jamais victoire (Victory 1 ne se paie que si on la vainc).
 - « step ONE of the villain phase » : l'etape 1 (placement de la menace de la manigance principale).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - ch020 The Life Stealer : revelee, 4 menaces par heros (1 heros -> 4)
      - ch020 The Life Stealer : revelee a DEUX heros -> 8 menaces (4 par heros)
      - ch020 The Life Stealer : fin de l'etape 1 de la phase du mechant -> 1 compteur mystic, rien d'autre
      - ch020 The Life Stealer : DEUX etapes -> 2 compteurs, toujours en jeu, aucun degat
      - ch020 The Life Stealer : TROISIEME compteur -> 3 degats a Shang-Chi ET a chaque allie, puis la carte est retiree de la partie
      - ch020 The Life Stealer : retiree de la partie, PAS defaussee (aucune carte dans la defausse de rencontre)
      Preuve par substitution : **rouges 6/6** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe a compteurs mystiques. Cas plateau : ui-app/src/board/shang-chi-plateau.test.ts (8 cas verts ; calibre ROUGE le 24/10 en mutant deux assertions ; aucun correctif de plateau necessaire, le rendu generique suffit). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

### ch021 : Downtown Attack (Treachery)

```
Downtown Attack — traitrise NEMESIS, x3 (3/5, 4/5 et 5/5). Boost 1.
When Revealed: Remove an ally or PERSONA card in play from the game. If no card was removed from the game this way, take
  3 indirect damage or discard 3 cards from your hand. Then, remove this card from the game.

Cartes de reference :
 - `nt015` Cosmic Connection : `WhenThisRevealed(None, op)`, `message.GetToPlayer()`, `joueur.GetControlCardsByType(CardFinder(...),
   ally=True, upgrade=True, support=True, ...)`, `this.DealIndirectDamage(identite, N, effect)` (degats INDIRECTS repartis par le joueur).
 - `27099` / `27189b` : `joueur.DiscardHandCards(range, effect)` (le joueur CHOISIT les cartes defaussees).
 - `sv011`/`sv012` : `Faces.RemoveAllFromGame([carte], effect)`.
 - choix a deux branches : `joueur.ChooseAbilities(effect, ForChoiceAbility(...), ForChoiceAbility(...))`.

⚠ Mots-pieges :
 - DECISION UTILISATEUR (24/10/2026) : le joueur qui revele choisit parmi SES alliés et SES cartes PERSONA (pas celles d'un autre joueur).
 - « an ally OR PERSONA card » : un allie quelconque ou n'importe quelle carte portant le trait PERSONA (amelioration, soutien...) ;
   l'identite n'est pas ciblee. « IN PLAY » : une carte glissee ou en main n'est pas en jeu.
 - « If NO card was removed this way » : le repli (indirect OU defausse) n'a lieu QUE si rien n'a ete retire.
 - « 3 INDIRECT damage » : repartis, non prevenus par une defense. « discard 3 cards from your HAND » : le joueur choisit lesquelles ;
   sans 3 cartes, il defausse toute sa main.
 - « Then, remove THIS card from the game » : la traitrise ne va JAMAIS a la defausse rencontre (3 exemplaires, aucun ne revient).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (coût, PV, stats, boost, ressource imprimée) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (6 cas sujets) :
      - ch021 Downtown Attack : un allie en jeu -> il est RETIRE de la partie, aucun degat ; la traitrise est retiree aussi
      - ch021 Downtown Attack : une carte PERSONA (Aunt May) en jeu, aucun allie -> elle est retiree de la partie
      - ch021 Downtown Attack : un allie ET une PERSONA -> le joueur CHOISIT (Aunt May retiree, l'allie reste)
      - ch021 Downtown Attack : rien a retirer -> 3 degats indirects a Shang-Chi (premiere option)
      - ch021 Downtown Attack : rien a retirer -> defausse de 3 cartes de la main (4 -> 1), aucun degat
      - ch021 Downtown Attack : un allie en jeu -> le repli (degats ou defausse) n'est PAS propose
      Preuve par substitution : **rouges 6/6** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack ; les coûts incliner/compteurs sont des COÛTS, testés « déjà incliné » / « sans compteur »). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 16 parties (shang_chi × rhino × équilibré/agressif × 8 graines), témoin spider_man (16 parties, mêmes réglages), grep tracebacks : 0 sur les 32 journaux. Journal lu : State of Flow se remplit à chaque attaque jouée, Meditate part au changement de forme. Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou pose un statut ; son passage sur la pile State of Flow est couvert par `ch002`. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, gate du héros, voir « Gates du héros »).

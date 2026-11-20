# Binary (Galactic Storm, Kajislav) : gabarits PROCESSUS-CARTE, lot GS-1

Preuves du 20/10/2026, branche `gs1-binary`. Pack `galactic_storm`, sets « Binary » et « Binary Nemesis »,
**17 card_id** : `gs001a` Binary, `gs001b` Carol Danvers, `gs002`-`gs011` (10 cartes signature distinctes,
15 exemplaires), `gs031` Forgotten Life (obligation), `gs032` Rogue, `gs237` Touched, `gs239` Goin' Rogue,
`gs240` Energy Transfer x2 (némésis, 5 cartes). Numérotation : décision de l'utilisateur du 20/10/2026
(`gs` + numéro imprimé), Forgotten Life en `gs031` (question Q1 de `.planning/todos/2026-10-20-gs1-questions.md`).
Plus 19 reskins d'officielles branchés en arts alternatifs `binary` (+ 3 ressources), section finale.

Sources : `docs/packs/galactic-storm/transcriptions/binary.md`, `binary-reskins.md` ; scans extraits des zips
Kajislav (z1, z2, z3, `Hero Packs/Binary (Galactic Storm expansion content)`). **Chaque carte relue contre son
image avant le code** (lecture du 20/10/2026, planches 750 px) : texte, coût, stats et traits conformes à la
transcription ; ajouts : Rogue porte 2 icônes de boost, Goin' Rogue porte une menace « 2 [par joueur] » et l'icône
Hazard (croix sur carte penchée, comparée par découpe à `sk067` Punish the Defector, même auteur, `Hazard` déclaré).

**Icônes de ressource** (jamais nommées à vue) : coin bas-gauche de chaque scan découpé et comparé aux reskins du
MÊME pack dont la ressource est connue par l'officielle : Energy 01088 `YY` = éclair brun sur fond jaune ; Genius
01089 `BB` = nœuds bleus ; Strength 01090 `RR` = poing sur fond rouge ; Combat/Defense/Front Line/Surveillance
Specialist 43034-43037 `G` = étoile verte. Résultat : Cosmic Influx R, Fuel the Fire B, Pursued by the Flame Y,
Solar Flare Y, Energy Torrent YY, Prophet-Singer R, White Hole R, Body in Flames R, Energy Conversion B, Light,
Radiation, Heat B. Contrôle croisé : la règle de Carol Danvers est tenue par les signatures (5 Y / 5 B / 5 R
cartes) et par le deck de l'auteur (9 / 9 / 9), ce qui confirme la lecture.

**Cas** : `Fusion/marvel-lcg-src/tools/cas/binary.py`, préfixe `[binary]`, **68 cas, 68 verts**
(`CAS_PREFIX=binary_ PARALLELES=2 test_capacites.py .game-src 22000 <rapport> "[binary]"`).
**Substitution** (sur les 65 cas de capacité, avant l'ajout des 3 cas de fixture plateau) : `tools/substituer_pack.py .game-src 23000 gs` : **17/17 cartes rouges sans leur module**,
empreinte md5 du pack identique avant/après (`7238354a…`). Les cas restés verts sous substitution sont des témoins
d'ABSENCE, des contre-cas dans l'autre forme ou des valeurs imprimées (`desc`), listés carte par carte.

**Autres gates** : `test_cards` 6827 ok / 0 erreur ; `verifier_prefixes` OK ; `verifier_appels_modules
galactic_storm` OK (calibré : une sonde `Faces.MethodeInexistanteBinary` posée dans gs009 le fait tomber, retirée) ;
`verifier_api_cartes` : aucun problème dans `galactic_storm` ; légalité des decks : 0 carte signature étrangère,
42 cartes de deck toutes présentes ; `DECK_NOM=binary verifier_tous_les_decks` : « identite gs001b, main 5,
deck 37 » ; passe complète des decks : voir le rapport de fin de lot. Deck-builder : `node --test
tools/tests-lanceur/regles-ressources-egales.test.mjs` 7/7 (vu ROUGE 2/7 sans la règle) ; batterie
`tools/tests-lanceur/*.test.mjs` 321/321 avant ajout. Arts : `tools/test_arts_binary.py` OK (calibré : une image
masquée le fait tomber).

**Plateau (étape 8 bis)** : `ui-app/src/board/binary-plateau.test.ts`, fixtures PRODUITES PAR LE MOTEUR
(`ToDescriptor.World`, cas `[binary] gs237 ... etape 8 bis`, `BINARY_FIXTURE_DIR`) : 5/5 verts ; vu ROUGE (1 échec)
en détachant Touched dans la fixture héros (`bind_object_id = 0`), puis restaurée. `tsc --noEmit` propre (une
annotation `as never` ajoutée à `arts-cartes.test.ts`, que la série `binary` rendait mal typée).

Aucune partie humaine n'a été jouée dans le navigateur.

---

### gs001a : * Binary (face héros)

- [x] Étape 2 : carte(s) de référence : ATQ « X » → `mw001a` Madame Web (desc 0 + `ThisGainKeyword`) ; statistique tirée
      de la MAIN → `sm/27154` Evil Doppelganger (`OnEvent.HandCards`) ; « After your turn ends » → `wolv/35030`
      (`AfterPlayerTurnEnd(ForcedResponse, "You")`).
- [x] Étape 5 : texte-contre-code : « [energy] RESOURCES » = icônes (Energy YY = 2, cas) ; wild exclu (cas, Q3) ;
      « to a MAXIMUM of 5 » (cas 6 → 5) ; « YOUR turn » ; « discard EACH [energy] resource » = chaque carte portant une
      icône [energy] (cas, Strength reste) ; Energy Conversion active : tout part (cas) ; face HÉROS seulement
      (contre-cas Burnout en alter ego). Résultat : OK.
- [x] Étape 6 : nombres : PV 12, CTR 2, DEF 2, main 5, ATQ X max 5 (cas « valeurs imprimées », scan 1A). Résultat : OK.
- [x] Étape 7 : ATQ X : 3 cas rouges sans module (3, 5, 0 → 2) ; Burnout : 2 cas rouges (main triée, sous Energy
      Conversion). Verts sans module, assumés : ATQ 0 avec R/B/G (absence), valeurs imprimées (desc), Burnout en alter
      ego (absence). 5/8. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bloc « Autoplay » en fin de fichier.
- [x] Étape 8 bis : la carte change ce qu'on VOIT ? NON (une statistique : la jauge d'ATQ est déjà couverte).

Carte terminée : OUI (la lecture du [wild], Q3, est codée sur la recommandation et se change dans une seule fonction).

### gs001b : * Carol Danvers (face alter ego)

- [x] Étape 2 : Action limitée d'alter ego → `sk001b`, `64001b` (`WhenInYourPlayTurn(Action).LimitOncePerRound()`) ;
      règle de construction → déclarative, comme Fatalis/Ares (GUIDE §5.4), nouvelle clé `ressources_egales`.
- [x] Étape 5 : « Action » nue sur la face alter ego (contre-cas en héros) ; « (Limit once per ROUND.) » ;
      « equal number of CARDS with a printed ... » = cartes, wild exclu, campagne exclue (FAQ p.22), signatures
      comprises (test deck-builder). Résultat : OK.
- [x] Étape 6 : PV 12, REC 4, main 5 (cas « valeurs imprimées », scan 1B) ; pioche 1. Résultat : OK.
- [x] Étape 7 : Exploring Space rouge sans module ; limite : rouge sans module (aucune pioche) ; contre-cas en héros
      et valeurs : verts (absence / desc). 2/4. Règle de deck : `regles-ressources-egales.test.mjs` 7/7, rouge 2/7
      sans la règle. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? OUI. Témoin : cas « limite 1 par round », deux Actions, main = 2 et non 3.
- [x] Étape 8 : autoplay : voir fin de fichier.
- [x] Étape 8 bis : NON (pioche).

Carte terminée : OUI

### gs002 : Cosmic Influx (x2)

- [x] Étape 2 : « Max 1 per round » → `cap/03015` (`.MaxOnePerRound()`) ; pioche → `player.DrawUp` rend les cartes
      piochées ; « take N damage » → `jubilee/47031`.
- [x] Étape 5 : « for EACH non-[energy] RESOURCE drawn THIS WAY » : icônes des seules cartes piochées (Genius BB +
      Strength RR = 4, Energy YY = 0) ; lues EN MAIN (FAQ p.22 : sous Energy Conversion, 0 dégât, cas) ; « TAKE » =
      l'identité. Résultat : OK.
- [x] Étape 6 : coût 1 [physical], pioche 3, 1 dégât par icône. Résultat : OK.
- [x] Étape 7 : 3/3 rouges sans module (pioche + 4 dégâts ; FAQ ; limite).
- [x] Étape 7 bis : limite imprimée ? OUI (« Max 1 per round »). Témoin : deux copies jouées, main 5 (la 2e reste) et
      non 6.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : NON.

Carte terminée : OUI

### gs003 : Fuel the Fire (x2)

- [x] Étape 2 : `sk021` Deflect the Blow (même auteur, même déclencheur) ; `message.PreventDamage(n)` ; soin
      `HealthUnits`.
- [x] Étape 5 : « When YOU would take damage FROM AN ATTACK » (`is_from_attack=True`) ; « for each ... prevent 1 AND
      heal 1 » : N et N (lecture littérale, Q4) ; « heal ... from BINARY » = l'identité ; sans [energy] la carte ne
      change rien et n'est pas proposée (cas). Résultat : OK.
- [x] Étape 6 : coût 0 [mental] ; 1 par icône. Cas : 2 [energy] → 3 dégâts deviennent 1 ; 1 [energy] → 3 restent 3.
      Résultat : OK.
- [x] Étape 7 : 2/3 rouges sans module ; vert sans module : « sans [energy], non jouée » (absence). Résultat : OK.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : NON.

Carte terminée : OUI (Q4 confirme la lecture littérale codée)

### gs004 : Pursued by the Flame (x2)

- [x] Étape 2 : `core/01052` (événement de contre `SetLabel('thwart').SetTarget(Scheme2)`) ; « ready » → `ReadyAll`.
- [x] Étape 5 : « a scheme » ; « at least [energy][energy] » = 2 icônes lues à la résolution, après paiement ;
      « ready BINARY ». Résultat : OK.
- [x] Étape 6 : coût 1 [energy] ; 2 menaces ; seuil 2. Cas : menace 5 → 3, Binary redressée ; seuil non atteint →
      reste inclinée. Résultat : OK.
- [x] Étape 7 : 2/2 rouges sans module.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : NON.

Carte terminée : OUI

### gs005 : Solar Flare (x2)

- [x] Étape 2 : `wsp/13013`, `core/05015` (événement d'attaque) ; « additional damage » = la même attaque.
- [x] Étape 5 : « an ENEMY » ; seuil lu à la résolution (Genius payé, Energy restée) ; « THAT enemy ». Résultat : OK.
- [x] Étape 6 : coût 2 [energy] ; 4 + 2. Cas : 6 dégâts / 4 dégâts. Résultat : OK.
- [x] Étape 7 : 2/2 rouges.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : NON.

Carte terminée : OUI

### gs006 : Energy Torrent

- [x] Étape 2 : `gmw/16033` Salvage (`AfterYouSpendThisCard(Response)`) ; `Faces.ShuffleAllTo`.
- [x] Étape 5 : « Response » facultative ; « after you SPEND » (défaussée par Burnout : reste en défausse, contre-cas) ;
      « shuffle IT into your deck ». Résultat : OK.
- [x] Étape 6 : `RES = YY` (découpe). Résultat : OK.
- [x] Étape 7 : 1/2 rouge (dépensée → dans le deck) ; vert sans module : Burnout (absence). Résultat : OK.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : la carte change de zone (défausse → deck) : dessin générique du deck, sans affirmation propre.

Carte terminée : OUI

### gs007 : * Prophet-Singer

- [x] Étape 2 : `next_evol/40037a` Domino (`Faces.SwapWithDeckTop`) ; `core/01091` (« Exhaust X → » sur un soutien).
- [x] Étape 5 : regarder D'ABORD (`LookAtDeck`), puis choisir la carte de la main ; échange obligatoire ; deck ou main
      vide : non proposée ; « Action » nue. Résultat : OK.
- [x] Étape 6 : coût 0 [physical], unique, AERIAL CREATURE. Résultat : OK.
- [x] Étape 7 : 1/2 rouge (échange : main = Genius, dessus = Energy, incliné) ; vert : valeurs (desc). Résultat : OK.
- [x] Étape 7 bis : NON (pas de limite imprimée ; l'inclinaison borne).
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : OUI (soutien en jeu) : `binary-plateau.test.ts`, « gs007 est dessinée ».

Carte terminée : OUI

### gs008 : White Hole

- [x] Étape 2 : `iron_fist/64002` (`DiscardDeckUntil` + `AddToHand`) ; `has_printed_res="Y"`.
- [x] Étape 5 : « HERO Action » (contre-cas alter ego) ; « PRINTED [energy] » lu dans le deck (Energy Conversion n'y
      touche pas, cas) ; wild non retenu (cas : Combat Specialist défaussé) ; carte trouvée en DERNIER : ajoutée quand
      même (défaut `Deck.DiscardUntil` contourné, cas). Résultat : OK.
- [x] Étape 6 : coût 2 [physical]. Résultat : OK.
- [x] Étape 7 : 3/4 rouges ; vert : alter ego (absence). Résultat : OK.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : déplacements deck → défausse → main : rendus génériques, pas d'affirmation propre.

Carte terminée : OUI

### gs009 : Body in Flames

- [x] Étape 2 : `iron_fist/64009` (riposte variable, `GiveKeywordToInPlayWhenApplyThis(Hero, ..., get_new_value)`) ;
      fiche `mots-cles/retaliate.md`.
- [x] Étape 5 : « BINARY gains » = face héros (contre-cas alter ego) ; paliers 0 / 1-2 / 3-4 / 5+ non cumulés.
      Résultat : OK.
- [x] Étape 6 : coût 2 [physical] ; 1 / 2 / 3. Cas : 2 → 1, 3 → 2, 6 → 3, 0 → 0. Résultat : OK.
- [x] Étape 7 : 3/5 rouges ; verts : 0 [energy] et alter ego (absence). Résultat : OK.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : OUI (amélioration en jeu) : `binary-plateau.test.ts`, « gs009 est dessinée ».

Carte terminée : OUI

### gs010 : Energy Conversion (x2)

- [x] Étape 2 : `ironheart/29038` Haywire (`WhenCountingResourcesOnCards`), `40037a` Domino (nombre gardé) ;
      Temporary : desc (fiche `mots-cles/temporary.md`).
- [x] Étape 5 : NOMBRE d'icônes gardé (Strength RR → 2, cas) ; « YOUR hand » seulement (White Hole lit le deck sans
      conversion, cas) ; vaut pour Burnout, Cosmic Influx (FAQ), Energy Transfer (cas). Résultat : OK.
- [x] Étape 6 : coût 0 [mental] ; Temporary. Résultat : OK.
- [x] Étape 7 : 1/3 rouge (ATQ 2 avec Strength) ; verts : Temporary (desc) et retour à 0 en fin de round (absence).
      Les cas FAQ / Burnout / White Hole / Energy Transfer, nommés sur leur carte, en dépendent aussi.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : NON (la jauge d'ATQ couvre le seul effet visible).

Carte terminée : OUI

### gs011 : Light, Radiation, Heat

- [x] Étape 2 : `ho016`, `27078` (`UnitAttackGainKeyword`, `is_basic_attack=True`) ; fiches ranged/piercing/overkill.
- [x] Étape 5 : « YOUR BASIC attacks » ; paliers CUMULATIFS « at least » ; compte lu pendant l'attaque. Résultat : OK.
- [x] Étape 6 : coût 1 [mental] ; seuils 1 / 2 / 3. Résultat : OK.
- [x] Étape 7 : 3/6 rouges (Distance contre Whiplash, Perçant contre Rhino Tenace, Déferlement sur sbire à 1 PV) ;
      verts : témoin sans la carte, « 1 seule, pas perçant », « 2, pas de déferlement » (absence). Résultat : OK.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : NON.

Carte terminée : OUI

### gs031 : Forgotten Life (obligation)

- [x] Étape 2 : `sunfire/sf010` Shame (obligation qui reste, « remove from the game »), `trors/04165`.
- [x] Étape 5 : « WHILE IN HERO FORM » → `"YourHero"` (contre-cas alter ego) ; « REMOVE from the game » (cas :
      zone des cartes retirées) ; deux coûts (incliner Carol ET défausser une carte SIGNATURE ; contre-cas avec une
      basique : non payable). Résultat : OK.
- [x] Étape 6 : -1 main ; 2 icônes de boost (desc). Résultat : OK.
- [x] Étape 7 : 2/4 rouges ; verts : alter ego, Action impayable (absence). Résultat : OK.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : obligation en jeu : zone `obligations_area`, rendu générique.

Carte terminée : OUI

### gs032 : * Rogue (sbire némésis)

- [x] Étape 2 : `rogue/38001a` (« After the player phase begins, find Touched ») ; `sk163` (`WhenDefeated`).
- [x] Étape 5 : à chaque phase des joueurs ; « FIND » partout, y compris en jeu (déplacement, cas) ; « other than
      Rogue » ; « IF FRIENDLY, exhaust THAT character » (Binary inclinée ; Rhino non, cas) ; « Discard Touched » =
      celle en jeu (cas). Résultat : OK.
- [x] Étape 6 : MNG 2, ATQ 2, PV 5, boost 2 (cas valeurs). Résultat : OK.
- [x] Étape 7 : 4/5 rouges ; vert : valeurs (desc). Résultat : OK.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : OUI (elle ATTACHE Touched) : `binary-plateau.test.ts`.

Carte terminée : OUI

### gs237 : Touched (attachement némésis)

- [x] Étape 2 : `tt/55062` Love Triangle (`if_cannot_gain_surge`), `mts/21083` Restrained (personnage ami),
      `gmw/16098` (réduction par attaque), `64009` (mot-clé variable sur une autre carte).
- [x] Étape 5 : « IF Rogue is in play ... OTHERWISE surge » (cas) ; quatre types de porteur, un seul bonus à la fois
      (cas sbire / vilain / allié / identité, chacun vérifie aussi l'absence des autres bonus). Résultat : OK.
- [x] Étape 6 : riposte 2, -2 dégâts par attaque (Binary ATQ 3 → 1 subi), +2 ATQ (2 → 4), Vilenie 1. Résultat : OK.
- [x] Étape 7 : 5/6 rouges ; vert : « sans Rogue → Renfort » (le moteur donne aussi Renfort à un attachement sans
      cible quand le module manque : la branche « otherwise » ne se distingue pas ; la condition « Rogue en jeu » est,
      elle, prouvée par le cas Hope Summers). Résultat : OK.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : OUI : `binary-plateau.test.ts` (Touched sur Binary, sur Hope Summers, sur Rhino ; fixtures du
      moteur).

Carte terminée : OUI

### gs239 : Goin' Rogue (manigance annexe némésis)

- [x] Étape 2 : `64009` / `hc014` (bonus variable sur une autre carte) ; `sk067` (Hazard, menace « par joueur »).
- [x] Étape 5 : FRIENDLY = identité/allié, ENEMY = vilain/sbire ; « GETS » = statistique. Résultat : OK.
- [x] Étape 6 : menace de départ 2 [par joueur] (`2*`), Hazard 1, boost 2 (cas valeurs : menace 2 en solo, 1 icône
      Hazard) ; +1 MNG / +1 ATQ. Résultat : OK.
- [x] Étape 7 : 2/3 rouges ; vert : valeurs (desc). Résultat : OK.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : manigance annexe en jeu, rendu générique ; présente dans la fixture `binary-touched-heros.json`.

Carte terminée : OUI

### gs240 : Energy Transfer (x2)

- [x] Étape 2 : `sk036` (traîtrise némésis même auteur, `WhenThisRevealed`) ; Burnout (gs001a) pour « each [energy]
      resource ».
- [x] Étape 5 : « YOUR hand » ; « IF NO CARD was discarded THIS WAY » (une seule suffit, cas) ; sous Energy Conversion
      Strength est défaussée (cas). Résultat : OK.
- [x] Étape 6 : 3 dégâts ; boost 1. Résultat : OK.
- [x] Étape 7 : 3/3 rouges.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : voir fin de fichier.
- [x] Étape 8 bis : NON.

Carte terminée : OUI

---

## Reskins de cartes officielles (deck de départ de l'auteur) : arts alternatifs `binary`

Décision appliquée : GUIDE §12 bis, « si SEULE l'image change, c'est un art alternatif » (règle de l'utilisateur du
17/10/2026, appliquée à TMNT et à MC/DC 2026). Chaque scan comparé à l'officielle sur planche (coût, ressource par
découpe, traits, texte, stats, unicité) :

| N° | Reskin | Officielle | Écart | Branché |
|---|---|---|---|---|
| 12 | Into the Fray | 13013 | aucun | oui |
| 13 | Moment of Triumph | 12030 | aucun | oui |
| 14 | Spoiling for a Fight | 54016 | aucun | oui |
| 15 | Keep Them Busy | 43018 | aucun (coût 1, imprimé tourné, lu « L » par la transcription) | oui (882×615) |
| 16 | Hall of Heroes | 06017 | aucun | oui |
| 17 | Aggressive Conditioning | 56013 | aucun | oui |
| 18 | Follow Through | 16045 | aucun | oui |
| 19 | Marked | 33032 | aucun | oui |
| 20 | Directed Force | 41019 | aucun | oui |
| 21 | Face the Past | 49022 | aucun | oui |
| 22 | Hope Summers | 40204 | aucun (PV 3, `2*`) | oui |
| 23 | Nick Fury | 01084 | aucun (PV 3, `2*`) | oui |
| 24 | Specialized Training | 43021 | aucun (coût 1, menace 5 [par joueur]) | oui (882×615) |
| 25 | Energy | 01088 | aucun | collection de ressources `binary` |
| 26 | Genius | 01089 | aucun | collection de ressources `binary` |
| 27 | Strength | 01090 | aucun | collection de ressources `binary` |
| 28 | Avengers Mansion | 01091 | trait « AVENGERS. » (coquille de l auteur) | oui (Q2 tranchée le 20/10/2026) |
| 29 | Deft Focus | 16024 | aucun | oui |
| 30 | Soaring Acrobatics | 42023 | aucun | oui |
| 36 | Combat Specialist | 43034 | aucun | oui |
| 37 | Defense Specialist | 43035 | aucun | oui |
| 38 | Front Line Specialist | 43036 | aucun | oui |
| 39 | Surveillance Specialist | 43037 | aucun | oui |

Série `binary` : art par défaut pour le héros Binary (`heros_cartes: ["gs001"]`), proposé à tous les autres.
Aucune capacité ni carte nouvelle : les cas existants des officielles restent la preuve (aucun reskin n'est une
carte). Preuve des données : `tools/test_arts_binary.py` (19 + 3, dimensions, tables alignées, présence dans les deux
tables de ressources).

## Autoplay (étape 8, commun aux 17 cartes)

`autoplay.py .game-src --deck binary --vilains rhino --profils equilibre --parties 8 --paralleles 2` : 0 victoire / 8
(5,5 rounds), **0 blocage**, **0 traceback** (grep NameError|AttributeError|TypeError|KeyError|AssertionError|Traceback
sur les 8 journaux `/tmp/autoplay_binary_rhino_normal_equilibre_*.log`). Témoin `spider_man`, même fournée : 0 / 8
(6,9 rounds), 0 blocage. Le deck est celui de l'auteur (27 cartes officielles + 15 signatures).
Lecture des journaux : toutes les cartes du pack y passent (Prophet-Singer 94 lignes, Energy Torrent et Energy
Conversion 70, Solar Flare 67, White Hole 57, Body in Flames 53, Cosmic Influx 47, Fuel the Fire 47, Forgotten Life 45,
Pursued by the Flame 44, Light, Radiation, Heat 33). La némésis sort par Shadow of the Past : Goin' Rogue entre en jeu,
Touched est révélée et s'équipe sur Rhino (« Rhino s'équipe de Touched (Rogue) »), la réduction joue (« Ces dégâts
sont ajustés de -2 (Touched) »), puis la Réponse forcée de Rogue la redéplace à chaque phase des joueurs (acte
« Attach Touched to a character other than Rogue » aux rounds 3, 4 et 5 de la partie 4).

Passe complète des decks (fichiers partagés touchés : `card_face.py`, `regles.js`, `app.js`) :
`verifier_tous_les_decks.py` **151/151** (Binary : « identite gs001b, main 5, deck 37 »).

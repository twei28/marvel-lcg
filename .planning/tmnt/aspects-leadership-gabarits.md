# Aspect TMNT Leadership (`ul`, pack `tmnt_aspect_leadership`) : gabarits PROCESSUS-CARTE

16/10/2026, agent Leadership, branche `aspects-ul`. 46 scans `ul001`–`ul046` (table figée
`tools/tmnt_aspects_numerotation.tsv`). Questions : `aspects-leadership-questions.md` (Q-UL-1 à Q-UL-8).

## Preuves transversales (valent pour toutes les cartes ci-dessous)

- **Construction** : `tools/test_cards.py` : 6605 ok / 0 err (toutes les cartes du dépôt, après ajout du pack).
- **Cas** : `tools/cas/tmnt_aspect_leadership.py`, filtre `[ul]` : **98/98 verts** (rapport
  `scratchpad/ul-r4.json`). Port 34000–34999, `CAS_PREFIX=ul_`.
- **Substitution des scripts** (`tools/substituer_pack.py .game-src 34200 ul0`) : 24/24 modules ont au moins
  un cas qui rougit sans eux ; les cas restés verts sont tous des CONTRE-CAS d'absence d'effet ou des cas de
  données, listés carte par carte. `git status` propre après l'outil.
- **Substitution des reskins** : `ability_link` retiré des 22 reskins (script `scratchpad/ul_cartes.py <ids>`),
  `[ul] ul0` relancé : les **21 cas de capacité des reskins ROUGISSENT tous**, leurs 21 TÉMOINS sur
  l'officielle restent verts, les 7 cas de données (bandeaux `unique_also`, traits) restent verts (attendu :
  ce sont des données). `cards.json` restauré (`git checkout`).
- **Ressources** vérifiées contre des cartes du MÊME pack dont l'officielle déclare la ressource : poing =
  R (`ul012` Inspired ↔ 01074 R, `ul015` ↔ 40023 R), nœuds = B (`ul013` ↔ 01071 B, `ul004` ↔ 31029 B), éclair
  = Y (`ul034` ↔ 06032 Y, `ul022` ↔ 62019 Y), étoile verte = G (`ul027` ↔ 45015 G).
- **Bandeau ✦ (décision Q-R1)** : `unique_also` sur ul017 (Squirrel Girl), ul019 (White Wolf), ul020 (Maria
  Hill), ul021 (Iron Fist), ul037 (Misty Knight), ul046 (White Tiger) ; un cas chacun (« pas jouable quand
  l'officielle est en jeu »), verts. Splinter Dojo Training porte un sous-titre vertical « Danger Room
  Training » sans ✦ et n'est pas unique : pas d'`unique_also`.
- **Autoplay** (étape 8) : deux decks Spider-Man + 25 cartes `ul` chacun (`scratchpad/deck-ul-A.json`,
  `deck-ul-B.json`), 8 parties contre Rhino, profil équilibré, témoin `spider_man` dans la même fournée.
  Fournée 1 (deck A) : 0 bloquée / 8, mais **3 parties sur 8 avec AssertionError** : `58031` Cameo (officielle,
  lue par `ul003`) fabriquait l'allié choisi avec le SCÉNARIO pour propriétaire ; dépensé comme ressource,
  `GetControlByPlayer` plantait. CORRECTIF dans `wonder_man/58031.py` (copie neuve dans le deck du joueur).
  Fournée 2 (après correctif) : voir la section « Autoplay final » en fin de fichier.
- **Plateau** (étape 8 bis) : `ui-app/src/board/tmnt-aspect-leadership.test.ts` (Venus : carte glissée face
  cachée sous un allié ; Naginata sur un allié ; Sense of Dread sur un sbire engagé) : 3/3 verts ; calibré
  ROUGE (2/3) en faisant pointer les attaches vers une carte absente. Aucun correctif plateau n'a été
  nécessaire : les chemins (attache d'allié, glissée sous allié, attache sur ennemi) existaient.
- **Images** : `tools/importer_images_tmnt_aspects.py … ul` : 46 images (assets/pics est gitignoré : à
  relancer sur la machine de jeu).
- **Texte FR** : bloc « TMNT Leadership (ul) » de `textes-fr-fanmade.ts` (46 entrées) + génération publique.

Lecture « Interrupt / Response » du pilote : les cas facultatifs passent `accepter_choix=True`.

---

### ul001 : Alopex (NOUVELLE)
- [x] Étape 2 : `03013` (Réponse d'entrée en jeu), `ta002` (« cloak her »), Retaliate en `desc` (fiche lue).
- [x] Étape 5 : « cloak HER » (elle-même), Response facultative, « Retaliate 1 » = desc. Conforme.
- [x] Étape 6 : coût 3, PV 3, ATQ 2*, CTR 2*, RES B, Retaliate 1. Conforme.
- [x] Étape 7 : `ul001 … camouflee` rouge sans module / vert ; `… Retaliate 1` vert sans module (donnée, attendu).
- [x] Étape 7 bis : limite ? NON.
- [x] Étape 8 : jouée 3 fois (fournée A), Réponse partie (« s'active, cible Alopex »), 0 erreur imputable.
- [x] Étape 8 bis : Cloaked = chemin des états déjà dessiné. NON concernée au-delà.
Carte terminée : NON — Q-UL-1 (unicité avec l'identité Alopex `ta001`).

### ul002 Band Together, ul004 Clarity of Purpose, ul009 Go All Out, ul011 Innate Inspiration, ul012 Inspired, ul013 Make the Call, ul015 Mission Leader, ul017 Napoleon, ul018 Noble Sacrifice, ul020 Rasputin, ul021 Red Shell, ul022 Righteous Purpose, ul026 Side-by-Side, ul027 Sidekick, ul032 Summoning Spell, ul034 Teamwork, ul037 Turtle-At-Arms, ul046 Zetian (IDENTIQUES, reskins par `ability_link`)
Un gabarit commun, les différences sont listées.
- [x] Étape 2 : l'officielle par `ability_link` (21018, 31029, 29017, 61037, 01074, 01071, 40023, 03013, 49018,
      01067, 62012, 62019, 45016, 45015, 21055, 06032, 62013, 21013). Modules relus : aucun nom ni card_id en dur ;
      `grep '"<id>"' src/game src/engine` : seulement deux COMMENTAIRES (31029 dans player_ask.py, 21013 dans
      has_stage.py).
- [x] Étape 5 : textes relus mot à mot contre l'officielle. Écarts SANS effet de règle, assumés :
      ul021 « defends against an attack » (officielle « an enemy attack ») — le module 62012 ne filtre pas
      l'ennemi (`WhenUnitDefendAgainstAttack`), il code déjà exactement le texte du scan ;
      ul034 « your hero power » (officielle « your hero's power ») ; ul011 : `MaxPerDeck 1` gardé de
      l'officielle (aucun des deux textes ne l'imprime). Traits du SCAN, jamais ceux de l'officielle.
- [x] Étape 6 : coûts, PV, ATQ/CTR (avec `*` de dégâts consécutifs), RES, `Uses`/`MaxPerUnit`/`MaxPerDeck`/
      `Requirement`/`Toughness`/`Setup` recopiés et vérifiés sur chaque scan. Conforme.
- [x] Étape 7 : un cas par reskin + TÉMOIN sur l'officielle, même chiffre ; tous ROUGES sans `ability_link`,
      témoins verts (voir preuves transversales). Bandeaux `unique_also` : 6 cas verts.
- [x] Étape 7 bis : limites imprimées ? NON pour toutes (Mission Leader : l'inclinaison est un coût).
- [x] Étape 8 : fournées A/B (B contient la plupart d'entre elles), 0 erreur imputable.
- [x] Étape 8 bis : NON (chiffres, statuts, attaches déjà couvertes).
Carte terminée : OUI pour chacune (Q-R2 deck-builder en attente chez l'utilisateur, non bloquante).

### ul003 : Cameo (IDENTIQUE, reskin de 58031)
- [x] Étapes 2/5/6 : comme ci-dessus (Setup, Max 1 per deck, aucun coût).
- [ ] Étape 7 : AUCUN cas : la capacité est une Mise en place (`AfterGameSetup`), hors de portée du harnais
      (le deck de départ du cas n'est pas modifiable avant la mise en place). Substitution impossible.
- [x] Étape 8 : PROUVÉE PAR AUTOPLAY : la Mise en place part (« Cameo s'active », Spider-Woman mélangée dans le
      deck) ; elle a révélé le défaut de 58031 corrigé ici (voir preuves transversales).
Carte terminée : NON — pas de cas `test_capacites` (outil manquant : un cas qui monte un deck AVANT la mise
en place). Comportement observé correct en autoplay après correctif.

### ul019 : Old Hob (IDENTIQUE, reskin de 51037)
Gabarit commun ci-dessus (cas + témoin, rouge sans lien ; trait « MUTANIMALS » vérifié par cas).
Carte terminée : NON — Q-UL-4 (MUTANIMALS / MUTANIMAL).

### ul033 : Take a Stand (IDENTIQUE, reskin de 62015)
Gabarit commun (cas + témoin, rouge sans lien). Traits : aucun (scan).
Carte terminée : NON — Q-UL-5 (trait TACTIC absent du scan).

### ul044 : "You Got This!" (texte IDENTIQUE à 49019, ressource différente)
Gabarit commun (cas + témoin, rouge sans lien). `RES R` (poing du scan) : seule différence, donnée.
Carte terminée : NON — Q-UL-8 ([physical] du scan contre [energy] de l'officielle).

### ul005 : Dask (MODIFIÉE, de 03011 Falcon)
- [x] Étape 2 : 03011 (regard + compte des traîtrises), 06020 Heimdall (« put back in any order »).
- [x] Étape 5 : « for each treachery » un dégât chacun, ennemi choisi à chaque fois ; « put THEM back »
      `PlaceOnTopInAnyOrder`. Conforme.
- [x] Étape 6 : coût 3, PV 3, 2*/2*, RES Y (éclair), 3 cartes, 1 dégât. Conforme.
- [x] Étape 7 : `2 traitrises -> 2 degats` rouge sans module ; contre-cas `aucune traitrise -> 0` vert sans
      module (absence d'effet, assumé).
- [x] 7 bis : NON. [x] 8 : jouée 3 fois (A), 0 erreur. [x] 8 bis : NON.
Carte terminée : OUI.

### ul006 : Defensive Formation (MODIFIÉE, de 62018)
- [x] Étape 2 : 62018. Étape 5 : « TURTLE ally » (DEFENDER remplacé), deux coûts, pas de SetPlay. Étape 6 :
      coût 2, Y, Uses 3 block, MaxPerDeck 3 (officielle).
- [x] Étape 7 : `Tenace a un allie TURTLE (3 -> 2 jetons)` rouge sans module ; contre-cas non TURTLE vert
      sans module (assumé).
- [x] 7 bis : NON (Uses = ressource épuisable, pas une limite). [x] 8 : 9 activations (A). [x] 8 bis : compteurs
      d'utilisation : chemin existant.
Carte terminée : OUI.

### ul007 : Down the Drain (NOUVELLE, Rampage 2)
- [x] Étape 2 : ua015 (Rampage), 49018 (« discard an ally you control → »), 61027 (seconde cible manigance).
      Fiche `rampage.md` lue.
- [x] Étape 5 : deux coûts (Rampage + allié), trois effets tous mesurés, pas d'étiquette attaque/contre.
- [x] Étape 6 : coût 1*, RES B, Rampage 2, 2 dégâts / 2 menaces / 2 cartes. Conforme.
- [x] Étape 7 : cas complet (2 dégâts subis, deck 6 → 2, Rhino 2, menace 5 → 3, main 2) rouge sans module ;
      contre-cas « sans allié : rien payé » vert sans module (assumé).
- [x] 7 bis : NON. [x] 8 : jouée 6 fois (A). [x] 8 bis : NON.
Carte terminée : OUI.

### ul008 : Gennosuke (MODIFIÉE, de 21019 Blade)
- [x] Étape 2 : 21019 ; 12025 (option « discard 1 card from your hand »).
- [x] Étape 5 : « thwarts OR attacks », « either … or », Forced. Stats : les ★ du scan sont l'icône de rappel
      (Blade : ATK 2 / THW 1 sans `*`), aucune icône de dégât consécutif : `"2"` / `"2"`.
- [x] Étape 6 : coût 2, PV 2, ATQ 2, CTR 2, RES R. Conforme.
- [x] Étape 7 : attaque main vide → défaussé ; contre → carte de main défaussée, reste en jeu : 2/2 rouges sans
      module.
- [x] 7 bis : NON. [x] 8 : 7 activations (A). [x] 8 bis : NON.
Carte terminée : OUI.

### ul010 : Heroes in a Half Shell (MODIFIÉE, de 36018)
- [x] Étape 2 : 36018 ; limite TEAM générique. Étape 5/6 : TURTLE ×3, +1 PV, −1 coût si tous TURTLE ; coût 3, B.
- [x] Étape 7 : +1 PV TURTLE (rouge sans module) ; Leonardo seul → Red Shell à 2 (rouge) ; contre-cas Maria
      Hill → pas de réduction (vert sans module, assumé).
- [x] 7 bis : NON. [x] 8 : en jeu dans la fournée A. [x] 8 bis : NON.
Carte terminée : OUI.

### ul014 : Midnight Veil (NOUVELLE)
- [x] Étape 2 : td005 (cloak de personnages choisis), ua015 (soutien NYC). Fiches cloak/cloaked lues.
- [x] Étape 5 : « up to », « you control », « 3 INSTEAD ». Étape 6 : coût 3, Y, 2/3.
- [x] Étape 7 : 3 personnages sans NYC → 2 camouflés ; avec Shell Cycle → 3 : 2/2 rouges sans module.
- [x] 7 bis : NON. [x] 8 : présente en A. [x] 8 bis : états, chemin existant.
Carte terminée : OUI.

### ul016 : Naginata (NOUVELLE)
- [x] Étape 2 : 01074 (attache + MaxPerUnit), al012 Gator Aid (même phrase), status/cloaked.py (GainValue).
- [x] Étape 5 : Interrupt facultative, coût = inclinaison, « +2 to THAT power ». Étape 6 : coût 1, B, +2, Max 1.
- [x] Étape 7 : attaque 1 + 2 = 3 et contre 2 + 2 = 4 : rouges sans module ; témoin « déjà inclinée → 1 »
      vert sans module (assumé, absence d'effet).
- [x] 7 bis : NON. [x] 8 : présente en A. [x] 8 bis : OUI, attachée à un allié : cas plateau vert, calibré.
Carte terminée : OUI.

### ul023 : Rubble Rouser (NOUVELLE, Rampage 3)
- [x] Étape 2 : bk014 (Réponse à un allié vaincu, jouée de la main), td001b (recherche + « exhausted »), ua015.
- [x] Étape 5 : HERO Response, « an ally » quelconque, « YOUR deck », incliné, mélange. Étape 6 : 1*, R, 3.
- [x] Étape 7 : allié vaincu → 3 dégâts payés, 1 allié du deck en jeu incliné : rouge sans module.
- [x] 7 bis : NON. [x] 8 : jouée 5 fois (A). [x] 8 bis : NON.
Carte terminée : OUI.

### ul024 : Sense of Dread (NOUVELLE)
- [x] Étape 2 : 43012 (« attacked this turn »), sk093/st016 (`apply`), sk213a (`WhenCardWouldLeavePlay`).
      Fiche vulnerable.md lue.
- [x] Étape 5 : MINION seulement, « your HERO », « non-ELITE », « leaves play » (toute sortie), Interrupt.
      Défaut trouvé par le cas : `WhenCardLeavePlay` arrive APRÈS le détachement, l'Interruption ne partait
      pas → `WhenCardWouldLeavePlay`.
- [x] Étape 6 : coût 1, B, pioche 1.
- [x] Étape 7 : vulnérable (rouge), ELITE non vulnérable (rouge : la carte n'est pas jouable sans module),
      non attaqué → pas jouable, défaussé → pioche, vaincu → pioche : 5/5 rouges sans module.
- [x] 7 bis : NON. [x] 8 : présente en A. [x] 8 bis : OUI, attachée à un sbire : cas plateau vert, calibré.
Carte terminée : OUI.

### ul025 : Shōgun « Leo » (NOUVELLE)
- [x] Étape 2 : 03013, td001b/ar010 (`Discard("YourHandCards", card_type=Ally)`), 49018 (Tenace).
- [x] Étape 5 : coût « discard an ALLY from YOUR HAND », « an ally » quelconque ; « Shugun » = coquille sans
      effet (cosmétique, notée). Étape 6 : coût 2, PV 2, 1*/1*, R.
- [x] Étape 7 : Tenace après défausse d'un allié (rouge sans module) ; contre-cas sans allié en main (vert,
      assumé).
- [x] 7 bis : NON. [x] 8 : jouée en A. [x] 8 bis : NON.
Carte terminée : OUI (coquille « Shugun » : question cosmétique non bloquante).

### ul028 : Splinter Dojo Training (MODIFIÉE, de 33015)
- [x] Étape 2 : 33015 ; limite TRAINING générique (`ability.py`). Étape 5 : « NINJA OR MUTANIMAL ».
      Étape 6 : coût 1, RES R (poing, comparé à ul012), +1/+1/+1.
- [x] Étape 7 : sur Red Shell (NINJA) +1/+1/+1 ; Maria Hill → pas jouable : 2/2 rouges sans module.
- [x] 7 bis : NON. [x] 8 : présente en B. [x] 8 bis : attache d'allié, couverte.
Carte terminée : OUI (l'effet sur Old Hob dépend de Q-UL-4, qui est une question sur Old Hob).

### ul029 : Splinter (NOUVELLE)
- [x] Étape 2 : 15007 Agatha Harkness (même phrase, N = 5).
- [x] Étape 5/6 : « YOUR deck », 1 carte, le reste DESSOUS ; coût 2, PV 2, 1*/1*, B.
- [x] Étape 7 : deck 6 → 5, main 0 → 1 : rouge sans module.
- [x] 7 bis : NON. [x] 8 : 6 activations (A). [x] 8 bis : NON.
Carte terminée : NON — Q-UL-2 (unicité avec `tl002` Splinter).

### ul030 : Street Vendor (NOUVELLE)
- [x] Étape 2 : 40023/al012 (amélioration sans attache), sk062 (réduction conditionnelle), 43006 (soin total).
- [x] Étape 5/6 : coût Discard, « a total of 3 », « you control » ; coût 2, Y, −1, 3.
- [x] Étape 7 : soin 2 + 1 (rouge) ; NYC → coûte 1 (rouge) ; contre-cas sans NYC (vert, assumé).
- [x] 7 bis : NON. [x] 8 : présente en A. [x] 8 bis : NON.
Carte terminée : OUI.

### ul031 : Suit Up (MODIFIÉE, de 45017)
- [x] Étapes 2/5/6 : copie de 45017 ; lecture A (attachable à CET allié) en attendant Q-UL-6. Coût 2, R.
- [x] Étape 7 : Black Cat + Sidekick en main : rouge sans module.
- [x] 7 bis : NON. [x] 8 : présente en B. [x] 8 bis : NON.
Carte terminée : NON — Q-UL-6.

### ul035 : "Turtle Power!" (MODIFIÉE, de 36020)
- [x] Étapes 2/5/6 : copie de 36020, X-MEN → TURTLE ×2 ; coût 1, Y, 5 cartes.
- [x] Étape 7 : Leonardo : Red Shell mis en jeu puis en main en fin de phase (rouge sans module) ; Spider-Man :
      pas jouable (vert sans module : sans module la carte n'est jamais jouable — assumé).
- [x] 7 bis : NON. [x] 8 : présente en B (non jouable avec Spider-Man, sert de ressource). [x] 8 bis : NON.
Carte terminée : OUI.

### ul036 : Turtle Titan « Mikey » (NOUVELLE)
- [x] Étape 2 : ta002 (`AfterUnitThwartEnd`), 45015 (soin). Étape 5 : « him » = lui-même, facultative.
- [x] Étape 6 : coût 4, PV 3, ATQ 2*, CTR 1* (★ = rappel), R, soin 2.
- [x] Étape 7 : 2 dégâts + 1 consécutif − 2 = 1 : rouge sans module.
- [x] 7 bis : NON. [x] 8 : 2 activations (A). [x] 8 bis : NON.
Carte terminée : OUI.

### ul038 : Unified Stike (MODIFIÉE, de 58020)
- [x] Étapes 2/5/6 : copie de 58020 (Interruption de héros, lecture A de Q-UL-7) ; coût 0, Y.
- [x] Étape 7 : Maria Hill 1 + 2 = 3, aucun dégât consécutif : rouge sans module.
- [x] 7 bis : NON. [x] 8 : présente en B. [x] 8 bis : NON.
Carte terminée : NON — Q-UL-7 (« Hero Response: When », titre « Stike »).

### ul039 : Venus « Bonnie » (MODIFIÉE, de 26013 Jocasta)
- [x] Étape 2 : 26013 ; vz001 (`ShareTrait(this)`).
- [x] Étape 5 : « the CARD attached » (tout type), « shares a TRAIT with Venus », face cachée.
- [x] Étape 6 : coût 3, PV 3, 2**/2**, B.
- [x] Étape 7 : carte partageant un trait glissée (rouge) ; carte jouable depuis Venus (rouge, vérificateur
      `ul_jouable_hors_main` = même filtre moteur que `jouer_glissee`) ; contre-cas sans trait commun et témoin
      « sous Maria Hill → pas jouable » (verts sans module, assumés).
- [x] 7 bis : NON. [x] 8 : présente en B. [x] 8 bis : OUI : cas plateau (glissée face cachée sous un allié),
      calibré rouge.
Carte terminée : NON — Q-UL-3 (unicité avec l'identité Venus `tv001`).

### ul040 : Weasel In + ul041 Mushroom, ul042 Zanna, ul043 Zink (NOUVELLES)
Mécanique : manigance JOUEUR + trois alliés « Linked (Weasel In) » à DOS DE RENCONTRE.
- [x] Étape 2 : Linked = mécanisme moteur EXISTANT (`desc.Linked`, `create_linked_faces` : les liées naissent
      dans `world.aside_deck`) — fiche `linked.md` lue ; 49020 New Recruits (manigance joueur, When Defeated) ;
      bk013 Morph (allié mélangé au deck rencontre) ; **39071 Longshot** (allié de rencontre : « does not
      count against your ally limit. When Revealed: Put X into play under your control. This card gains surge.
      This effect cannot be canceled. », mot pour mot) ; 60139 (« your » = le joueur qui révèle). AUCUNE
      extension moteur nécessaire. Montage commun : `AbilitiesBelette` (`__init__.py` du pack).
- [x] Étape 5 : « THE set-aside WEASEL allies » (toutes) ; « shuffle into the ENCOUNTER deck » ; « a FRIENDLY
      character » (tous joueurs) ; ordre imprimé (effet puis mise en jeu) ; « under YOUR control » ; surge ;
      « cannot be canceled » (`SetCannotBeCancel`) ; hors limite d'alliés. Propriétaire des belettes : le
      scénario (aside_deck) — cohérent avec leur DOS DE RENCONTRE (elles repartent à la défausse de rencontre).
      « Musroom » : coquille cosmétique notée.
- [x] Étape 6 : Weasel In coût 0, G, menace 2 par joueur (`2*`), Victoire 0 ; Mushroom PV 2 1*/1* R ; Zanna PV 1
      CTR 2* ATQ 0* Y ; Zink PV 1 CTR 0* ATQ 2* B ; soin 2 / menace 2 / dégâts 2.
- [x] Étape 7 : Weasel In jouée → 2 menaces + 3 belettes mises de côté (donnée Linked : vert sans module,
      attendu) ; déjouée → belettes dans le deck rencontre (rouge sans module) ; Mushroom soin 2 + en jeu ;
      Zanna −2 menaces + en jeu ; Zink 2 dégâts + en jeu ; Zink hors limite (4 alliés) : tous rouges sans module.
- [x] 7 bis : NON. [x] 8 : Weasel In présente en A et B (le pilote la dépense en ressource, ne la joue pas : la
      révélation des belettes n'est donc PAS vue en autoplay). [x] 8 bis : manigance joueur et mise de côté :
      zones existantes.
Carte terminée : OUI pour les quatre. Reste « en partie réelle » : la révélation d'une belette au milieu d'une
vraie phase du méchant (surge enchaîné) n'a été vue qu'en cas isolé (`Puzzle.Reveal`), pas en autoplay.
Deck-builder : les belettes portent la classe Leadership (scan) ; comme les liées officielles, rien ne les
masque du deck-builder (à signaler, même nature que Q-R2).

### ul045 : Zato-Ino (NOUVELLE)
- [x] Étape 2 : 01118 (`AfterUnitAttackAndDamageUnit`), ta002 (daze). Fiche daze.md lue.
- [x] Étape 5 : « attacks AND DAMAGES », « an enemy », « THAT enemy », facultative.
- [x] Étape 6 : coût 3, PV 2, 1*/1★*, Y.
- [x] Étape 7 : Rhino blessé → Dazed (rouge sans module) ; Rhino Tenace → pas de Dazed (vert, assumé).
- [x] 7 bis : NON. [x] 8 : présente en A. [x] 8 bis : statut Dazed, chemin existant.
Carte terminée : OUI.

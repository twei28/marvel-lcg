# Ch'od (Starjammers) : gabarits PROCESSUS-CARTE, 26/10/2026

Pack `chod` (préfixe `co`, set 227, auteurs Phenexian et Mysteltainn). Scripts : `src/cards/pack/chod/{chod,chod_nemesis}/`.
Cas : `tools/cas/chod.py` (50 cas `[co]`) ; plateau : `ui-app/src/board/chod-plateau.test.ts` ; deck `chod` ; recettes `RECETTES-MOTEUR.md` (§ Ch'od).

**Aucune carte n'est « terminée »** : il manque la partie réelle jouée par un humain (voir la fin), et plusieurs cartes portent une question de règle en suspens (choix provisoire codé, consigne utilisateur du 25/10/2026 : les questions sont gardées pour la fin).

Lecture de la substitution (`substituer_pack.py`, `rouges N/M`) : les cas qui restent verts sans module sont des **valeurs imprimées**, des **contre-cas d'absence** ou des **témoins** (assumés ci-dessous). Bilan : **17/17 modules ont au moins un cas rouge sans eux**, pack identique avant/après (md5 `2d3cdb11…`). Passe finale du 26/10/2026 : 50/50 cas `[co]`, `test_cards` 7 648 modules / 0 erreur, `verifier_tous_les_decks` 169/169 decks montent une partie (le deck `chod` : « identite co001a, main 5, deck 10 »), `verifier_prefixes`, `verifier_appels_modules` (calibré : un appel `Faces.` inventé est vu), `verifier_cibles`, `verifier_noms_modules`, `verifier_traductions_fr` verts. Autoplay : 8 parties Ch'od contre Rhino (0 victoire, 6 « tous éliminés », 2 « manigance accomplie », 3,9 rounds), témoin `spider_man` 8 parties (0 victoire, 6,9 rounds), 0 exception, 0 blocage ; cartes jouées par le pilote : Raw Physicality 20, Polymath 19, Cr'reee 11, Teacher 7, Engineer 6 ; ennemis révélés : Mentor, Duel of Wits, Utter Contempt, Strike and Phase, Plutonia. Non vus dans les journaux : Raw Intellect, Saurian Physique, Philosopher Scientist, Warrior (le pilote ne les joue pas ; leurs cas test_capacites sont verts).

---

### co001a : Ch'od (face héros)

- [x] Étape 2 : références : `bg001a`/`rz001a`-style : `AbilityFactory.WhenPlayerPlayCard(Interrupt, "You", None, op, conditions=[...])` (fenêtre de JEU, modèle Batgirl `bg008`) ; `GainUntilPhaseEnd(effect, hand_size=1, end_phase="Player")` (modèle `27185b`).
- [x] Étape 5 : mots-pièges : « a card with the requirement keyword » = `face.requirement.val > 0` (Requirement imprimé : événements ET améliorations) ; « Interrupt » : l'effet part AVANT la résolution de la carte (Raw Physicality lit la taille de main augmentée) ; « Limit once per phase » : `LimitOncePerPhase()`.
- [x] Étape 6 : nombres texte ↔ code : PV 14, ATQ 3, THW 2, DEF 3, HS 4 (scan) = `desc` = cas de valeurs imprimées.
- [x] Étape 7 : Cas : valeurs ; Master (Raw Physicality : 4 + 1 = 5 dégâts) ; contre-cas Polymath sans Requirement (HS reste 4) ; témoin d'épuisement (deux cartes à Requirement dans la phase : menace 6 - 5 = 1, et non 0). Substitution : rouges 2/4 (les 2 verts : valeurs imprimées, contre-cas).
- [x] Étape 7 bis : limite imprimée ? OUI : témoin d'épuisement fait (`jouer=[co003, co004]` dans la même phase : un seul +1).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q1.

### co001b : Ch'od (face alter ego)

- [x] Étape 2 : références : `rz001b` (`Search.PlayerCard(include_player_deck=True, include_discard_pile=True)` + `GainCard`) ; coût `CostFunc.Discard("YourHandCards", range=(1, 1))`.
- [x] Étape 5 : mots-pièges : « search your deck and discard pile for Cr'reee » : deck ET défausse (précédent Roz « Find ») ; la défausse est un COÛT (avant la flèche) : payée même si Cr'reee est introuvable ; « Limit once per phase » : `LimitOncePerPhase()`.
- [x] Étape 6 : nombres texte ↔ code : PV 14, REC 4, HS 5, GENIUS OUTLAW (scan).
- [x] Étape 7 : Cas : valeurs ; Cr'reee trouvée dans le deck ; trouvée dans la défausse ; témoin d'épuisement (deux Actions, la seconde refusée : une seule Cr'reee en main). Substitution : rouges 3/4 (le vert : valeurs imprimées).
- [x] Étape 7 bis : limite imprimée ? OUI : témoin fait (`declencher_tolerant` : le moteur refuse la 2e Action, c'est exactement quand la limite mord).
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q2.

### co002 : Cr'reee (allié)

- [x] Étape 2 : références : `br007` : `GiveKeywordToInPlayWhenApplyThis(Identity, control_by="You", hand_size=1, condition=...)`.
- [x] Étape 5 : mots-pièges : « While Cr'reee is exhausted » : l'état n'a AUCUN `OnEvent` : un `OnEvent.TemplateTrigger` est construit sur `Message.AfterCardExhausted` / `AfterCardReady` pour que la taille de main suive (sans lui, `hand_size` restait à 4 après `Puzzle.Exhaust`).
- [x] Étape 6 : nombres texte ↔ code : Coût 2, PV 3, ATQ 1*, THW 1*, RES mental + énergie (`BY`, deux icônes lues sur le scan puis comparées à `01022` / `01025`).
- [x] Étape 7 : Cas : valeurs ; inclinée -> HS 5 ; contre-cas prête -> HS 4. Substitution : rouges 1/3 (valeurs et contre-cas restent verts).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q3.

### co003 : Raw Physicality (x3)

- [x] Étape 2 : références : `01021` Gamma Slam (`SetPlay().SetLabel()`, `this.DealDamage`), valeur lue sur l'identité (`hand_size`).
- [x] Étape 5 : mots-pièges : « equal to your hand size » = le STAT taille de main (pas le nombre de cartes en main) ; `Requirement ([physical][physical])` est lu NATIVEMENT (`desc.Requirement = "RR"`), aucun script ; « Attack » est un TRAIT : le texte n'imprime pas « (attack) », donc `SetLabel()` sans label.
- [x] Étape 6 : nombres texte ↔ code : Coût 2, RES énergie (`Y`), Requirement `RR`.
- [x] Étape 7 : Cas : dégâts = taille de main (Cr'reee inclinée : 5 + Master = 6) ; contre-cas Requirement non satisfait (payée en mental) : injouable, reste en main. Substitution : rouges 1/2 (contre-cas).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q4.

### co004 : Raw Intellect (x3)

- [x] Étape 2 : références : `01026` Superhuman Law Division (`RemoveThreatFromSchemes(effect.targets, n, effect)`, `SetTarget(Scheme2)`).
- [x] Étape 5 : mots-pièges : « equal to your hand size » comme Raw Physicality ; `Requirement ([mental][mental])` natif (`BB`). ⚠ `Puzzle.SetThreat(01097b, 8)` ACCOMPLIT la manigance principale du harnais (partie finie avant tout jeu) : 6 au plus.
- [x] Étape 6 : nombres texte ↔ code : Coût 2, RES physique (`R`), Requirement `BB`.
- [x] Étape 7 : Cas : retire 5 menaces (6 -> 1) ; contre-cas Requirement non satisfait (payée en physique). Substitution : rouges 1/2 (contre-cas).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q4.

### co005 : Polymath (x3)

- [x] Étape 2 : références : Batgirl `bg004` (`effect.GetPaidResources()` + `GetColor`) ; `Faces.GiveStatus(.., "Tough")`, `Faces.ReadyAll`, `joueur.DrawUp(1)`.
- [x] Étape 5 : mots-pièges : « If you paid for this card with a [x] » = condition sur le PAIEMENT ; ⚠ **CORRIGÉ le 26/10/2026** : `GetPaidResources()` garde le wild en `G` (mesuré) ; `GetPaidResources(True)` demande au joueur le type du wild (`PayeEnWild` supprimé). 01083 Mockingbird n'est PAS wild (physique) : le wild des cas est 01020 Hellcat.
- [x] Étape 6 : nombres texte ↔ code : Coût 1, RES mental (`B`).
- [x] Étape 7 : Cas : payée en physique (Tenace) ; en énergie (se redresse) ; en mental (pioche + HS 5) ; avec une ressource wild : **REMPLACÉ le 26/10/2026** par trois cas (wild déclaré énergie / physique / mental), voir le bloc « arbitrage Wild » plus bas. Substitution : rouges 6/6.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q5.
- [x] **26/10/2026, arbitrage Wild** (RR « Wild Resource », fiche `mots-cles/wild-resource.md`) : un wild dépensé compte pour UN type, celui que le joueur déclare. Avant : `wild or ...` comptait les TROIS lignes. Maintenant : `effect.GetPaidResources(True)` (le moteur demande le type du wild, modèle `gs301`) puis une ligne par couleur ; `PayeEnWild` supprimé.
      Cas (3 remplacent l'ancien « les TROIS lignes ») : wild déclaré [energy] (se redresse, ni Robuste ni pioche, main 0, HS 4), [physical] (Robuste seule), [mental] (pioche + HS 5 seuls) via `preferer_option="Y"/"R"/"B"`. preuve : cas ROUGES vus AVANT le correctif (11 rouges sur 28 cas Ch'od filtrés), VERTS après ; substitution du module (`GetAbilities -> []`) : **rouges 6/6** sans le module.
      Autoplay ciblé (26/10/2026, `tools/autoplay.py --deck chod --vilains rhino --difficultes normal --profils equilibre --parties 8`) : 8 parties, 0 victoire / 8 défaites (4 manigance accomplie, 4 héros éliminé), 0 bloquée, grep exhaustif NameError / AttributeError / TypeError / KeyError / AssertionError : 0 sur les 8 journaux ; témoin `spider_man`, mêmes graines et même vilain : 0 / 8, 0 bloquée, 0 erreur. Polymath jouée dans les 8 parties (journal lu : « jouer … avec B » / « avec Y »). Aucun wild dans ce deck : le cas unitaire est la preuve du wild.

### co006 : Saurian Physique

- [x] Étape 2 : références : `im012` (`UnitAttackGainKeyword("You", overkill=True)`, `"You"` = l'IDENTITÉ seulement) ; `AfterUnitDefeatedUnit(HeroResponse, "You", Minion, ...)`.
- [x] Étape 5 : mots-pièges : « Ch'od's attacks » = attaques de l'identité (pas des alliés) ; « After you defeat a minion » = vaincu par le héros ; `Requirement ([physical][physical])` natif ; « until the end of the phase » = `end_phase="Player"`.
- [x] Étape 6 : nombres texte ↔ code : Coût 3, RES physique (`R`), Requirement `RR`, trait CONDITION.
- [x] Étape 7 : Cas : excès d'un sbire à 1 PV (2 dégâts au vilain) ; contre-cas sans la carte (0) ; Réponse (s'incline, HS 5) ; contre-cas vilain abattu (pas un sbire). Substitution : rouges 2/4 (contre-cas).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q6.

### co007 : Philosopher Scientist

- [x] Étape 2 : références : `mf005` (`GiveKeywordToAttached(CardFinder(name=...), hand_size=1)`).
- [x] Étape 5 : mots-pièges : Titre : amélioration attachée à Ch'od ; `Requirement ([mental][mental])` natif.
- [x] Étape 6 : nombres texte ↔ code : Coût 2, RES mental, Requirement `BB`, trait TITLE.
- [x] Étape 7 : Cas : +1 taille de main (5). Substitution : rouges 1/1.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine.

### co008 : Engineer

- [x] Étape 2 : références : `doctor_druid/__init__.py` `BonusSelonLaMain` (`change_on_event=OnEvent.HandCards`) ; `Types()` du pack.
- [x] Étape 5 : mots-pièges : « printed [energy] resource in your hand » = ressource IMPRIMÉE (`printed_resource`), évaluée sur la main ; une ressource wild imprimée compte pour les trois couleurs (règle du wild).
- [x] Étape 6 : nombres texte ↔ code : Coût 1, RES énergie, trait SKILL.
- [x] Étape 7 : Cas : énergie en main (+1) ; contre-cas mental (0) ; wild imprimé (Hellcat, +1). Substitution : rouges 2/3.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q8.
- [x] **26/10/2026, arbitrage Wild** (RR « Wild Resource », fiche `mots-cles/wild-resource.md`) : hors paiement un wild imprimé n'est que « wild » : il ne vaut PAS [energy]. `Types(face)` (helper du set) rend maintenant `{R, B, Y, G}` (`GetColor(c, convert_green_res=False)`). Contre-cas ajouté : une Hellcat (wild) seule en main ne donne aucun bonus de main (4). ROUGE vu avant le correctif (5 au lieu de 4), vert après. Substitution : le cas nominal tombe (rouges 1/3, les 2 contre-cas d'ABSENCE restent verts, assumé).

### co009 : Teacher

- [x] Étape 2 : références : comme co008.
- [x] Étape 5 : mots-pièges : « printed [mental] resource ».
- [x] Étape 6 : nombres texte ↔ code : Coût 1, RES mental.
- [x] Étape 7 : Cas : mental en main (+1) ; contre-cas physique (0). Substitution : rouges 1/2.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q8.
- [x] **26/10/2026, arbitrage Wild** (RR « Wild Resource », fiche `mots-cles/wild-resource.md`) : hors paiement un wild imprimé n'est que « wild » : il ne vaut PAS [mental]. `Types(face)` (helper du set) rend maintenant `{R, B, Y, G}` (`GetColor(c, convert_green_res=False)`). Contre-cas ajouté : une Hellcat (wild) seule en main ne donne aucun bonus de main (4). ROUGE vu avant le correctif (5 au lieu de 4), vert après. Substitution : le cas nominal tombe (rouges 1/3, les 2 contre-cas d'ABSENCE restent verts, assumé).

### co010 : Warrior

- [x] Étape 2 : références : comme co008.
- [x] Étape 5 : mots-pièges : « printed [physical] resource ».
- [x] Étape 6 : nombres texte ↔ code : Coût 1, RES physique.
- [x] Étape 7 : Cas : physique en main (+1) ; contre-cas énergie (0). Substitution : rouges 1/2.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q8.
- [x] **26/10/2026, arbitrage Wild** (RR « Wild Resource », fiche `mots-cles/wild-resource.md`) : hors paiement un wild imprimé n'est que « wild » : il ne vaut PAS [physical]. `Types(face)` (helper du set) rend maintenant `{R, B, Y, G}` (`GetColor(c, convert_green_res=False)`). Contre-cas ajouté : une Hellcat (wild) seule en main ne donne aucun bonus de main (4). ROUGE vu avant le correctif (5 au lieu de 4), vert après. Substitution : le cas nominal tombe (rouges 1/3, les 2 contre-cas d'ABSENCE restent verts, assumé).

### co011 : Cr'reee Captured (obligation)

- [x] Étape 2 : références : `sunfire/sf010` (obligation qui RESTE en jeu, avec une Action d'alter ego) ; `corsair/cr012` (`WhenThisObligationGiveToYou`, `message.GetGaveToPlayer()`) ; `cr014` (`TuckCardUnderHere`).
- [x] Étape 5 : mots-pièges : « Find Cr'reee » : deck ET défausse ; « tuck them under this card » : `this.TuckCardUnderHere` fonctionne sous une obligation en jeu ; compteur `search` (accepté par le moteur) ; ⚠ retirer un compteur en effet = `RemoveCountersInternal(1, 'search', effect)` (le `RemoveCounters` à trois arguments n'est pas l'API des effets) ; l'obligation retirée de la partie emporte Cr'reee à la DÉFAUSSE du joueur (mesuré, cas « MESURE »).
- [x] Étape 6 : nombres texte ↔ code : Boost 2, GiveTo « Ch'od ».
- [x] Étape 7 : Cas : révélée (Cr'reee dessous, 2 compteurs) ; contre-cas Cr'reee introuvable (2 compteurs, rien dessous) ; Action (1 compteur, Ch'od incliné) ; dernier compteur (retirée de la partie) ; mesure : Cr'reee en défausse. Substitution : rouges 4/4.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : la carte change ce qu'on VOIT (glisse sous une carte) : OUI, cas plateau `chod-plateau.test.ts` (fixture à la main, aucun correctif d'affichage nécessaire : pas de « vu rouge »).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q9.

### co012 : Mentor (sbire némésis)

- [x] Étape 2 : références : `04054` The Viper (`GiveKeywordToInPlayWhenApplyThis(Identity, control_by="EngagedPlayer", hand_size=-1)`) ; `WhenUnitBeDefeated(WhenDefeated, "This", ...)`.
- [x] Étape 5 : mots-pièges : « engaged with you » : joueur engagé ; « different printed resources » : ENSEMBLE des couleurs (un wild compte pour les trois) ; `DiscardDeckTopCards(2)`, menace sur la manigance principale `PlaceThreatOnSchemes("MainScheme", n)`. ⚠ `main_exclusive=[01090]` RETIRE 01090 du deck de test (`Puzzle.Gain` prend dans le deck) : main en 01083 pour garder le deck intact.
- [x] Étape 6 : nombres texte ↔ code : PV 5, ATQ 1, SCH 3, Boost 2, ELITE, IMPERIAL GUARD, némésis de Ch'od.
- [x] Étape 7 : Cas : taille de main 3 quand il est engagé ; valeurs ; vaincu avec deux couleurs (2 menaces) ; contre-cas même couleur (1). Substitution : rouges 3/4 (valeurs).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q10.
- [x] **26/10/2026, arbitrage Wild** (RR « Wild Resource », fiche `mots-cles/wild-resource.md`) (partie « different printed resources ») : le wild est un type à part (le 4e), pas trois couleurs. Cas ajoutés : deck wild + [physical] = 2 menaces ; deux Hellcat = 1 menace. ROUGES avant (3 menaces dans les deux cas), VERTS après (changement porté par `Types`). La question « your deck » du When Defeated (joueur qui a vaincu Mentor) est traitée par la fiche Ch'od, pas ici.
- [x] **26/10/2026, arbitrage utilisateur (Q10a)** : « Discard the top 2 cards of YOUR deck » = le deck du joueur qui a VAINCU Mentor (précédent FFG : errata de Mystique's Manipulations « the defeating player »), pas du joueur engagé ; sans vainqueur (dégâts directs), repli sur le joueur engagé. Code : `message.defeating_player` (`WhenUnitBeDefeated`). Cas ajoutés (2 joueurs, `heros2`, `Puzzle.Engage('co012', 1)`) : engagé avec le joueur 2 et vaincu par Ch'od, c'est le deck de Ch'od (R + B) qui part : 2 menaces (**ROUGE avant** : 1 menace, c'était le deck R + R du joueur engagé), vert après ; contre-cas sans vainqueur : deck du joueur engagé (1 menace). Substitution co012 : rouges 7/8 (le cas « valeurs imprimées » reste vert sans module, assumé). Passe complète `[co]` : 61/61. Autoplay (`--deck chod --vilains rhino --parties 8`) : 8 parties terminées, 0 victoire / 8 défaites, 0 incident, 0 erreur dans les 8 journaux (non lus ligne à ligne) ; témoin spider_man : 0 / 8. Vérificateur de deck `chod` : OK. Carte terminée : NON (provisoire) : partie réelle humaine à plusieurs joueurs non faite.

### co013 : Duel of Wits (manigance annexe)

- [x] Étape 2 : références : `PlayersCannotRemoveThreatFrom("AnyPlayer", "This", conditions=[...])` ; `cr014` (`TuckCardUnderHere` d'une carte de la main).
- [x] Étape 5 : mots-pièges : « cards with a printed resource that matches the printed resource on the card tucked » : intersection des couleurs imprimées de la carte source de l'effet et de la carte glissée ; l'identité et le pouvoir de base du héros n'ont pas de ressource imprimée : non concernés ; menace de départ `3*` (par joueur).
- [x] Étape 6 : nombres texte ↔ code : Menace 3 par joueur, Boost 3.
- [x] Étape 7 : Cas : révélée (carte glissée, menace 3) ; même ressource : la menace ne baisse pas ; contre-cas ressource différente : retirée, la manigance quitte le jeu. Substitution : rouges 2/3 (contre-cas).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : la carte change ce qu'on VOIT (glisse sous une carte) : OUI, cas plateau `chod-plateau.test.ts` (fixture à la main, aucun correctif d'affichage nécessaire : pas de « vu rouge »).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q11.
- [x] **26/10/2026, arbitrage Wild** (RR « Wild Resource », fiche `mots-cles/wild-resource.md`) : une carte WILD glissée dessous ne correspond qu'à un autre wild. Cas ajouté : wild glissé + Raw Intellect [physical] = la menace est retirée (manigance hors jeu). ROUGE avant (menace restait à 3, correspondance par `Types` convertissant le wild), VERT après.

### co014 : Plutonia (sbire)

- [x] Étape 2 : références : `UnitAttackGainKeyword("This", piercing=True)` (modèle `hz014`) ; Teamwork lu NATIVEMENT (`desc.Teamwork`, `can_teamwork.py`) ; `DiscardRandomHandCards`.
- [x] Étape 5 : mots-pièges : [star] : permanent, pas expert seulement ; « discard an upgrade you control. If you cannot, discard 1 random card » ; `Puzzle.EnemyAttacks(<ennemi>, <cible>)` demande la cible.
- [x] Étape 6 : nombres texte ↔ code : PV 4, ATQ 2*, SCH 1, Boost 2, IMPERIAL GUARD.
- [x] Étape 7 : Cas : défausse une amélioration ; sinon une carte au hasard ; piercing (Tenace défaussée, 2 dégâts passent) ; valeurs. Substitution : rouges 3/4 (valeurs).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q12.

### co015 : Strike and Phase

- [x] Étape 2 : références : `01027`-style `joueur.DiscardDeckTopCards(1, effect)` puis `Faces.DiscardAll`.
- [x] Étape 5 : mots-pièges : « a resource symbol that matches that card » = couleur imprimée commune (wild = toutes).
- [x] Étape 6 : nombres texte ↔ code : Boost 1.
- [x] Étape 7 : Cas : dessus du deck physique, défausse de la main physique (reste 2 cartes). Substitution : rouges 1/1.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q13.
- [x] **26/10/2026, arbitrage Wild** (RR « Wild Resource », fiche `mots-cles/wild-resource.md`) : un wild défaussé ne correspond qu'aux cartes wild de la main. Cas ajoutés : dessus du deck wild + main R/B/Y = rien ne part (main 3) ; wild + main [wild, physical] = seul le wild part (main 1). ROUGES vus en rétablissant l'ancien `Types` (main 0 dans les deux cas), VERTS après. ⚠ Mesurer la MAIN, pas « la carte milled est en défausse » : quand le deck se vide le moteur remélange la défausse. `Puzzle.Gain('01020')` PREND la Hellcat du deck : le cas 2 en met deux.

### co016 : Utter Contempt

- [x] Étape 2 : références : `joueur.ChooseAbilities` + `AbilityFactory.ForChoiceAbility` (`cr012`) ; `this.DealIndirectDamage(identite, n, effect)` (`nt015`).
- [x] Étape 5 : mots-pièges : « boost icons » = icônes de boost IMPRIMÉES (`printed_boost` : `CountBoostIconsInternal` rend 0 hors du deck) ; « printed resources » = nombre d'ICÔNES (`printed_resource.val`) ; `CreateEncounterDeck` : le DESSUS est le DERNIER de la liste.
- [x] Étape 6 : nombres texte ↔ code : Boost 2.
- [x] Étape 7 : Cas : 1re branche (2 + 2 icônes : 4 dégâts indirects) ; 2e branche (RR + YY : 4 menaces). Substitution : rouges 2/2.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON (elle chiffre seulement ; les compteurs et statuts sont déjà dessinés).
Carte terminée : NON (provisoire) : partie réelle humaine ; Q14.

### co017-co019 : Energy, Genius, Strength (reskins Basic)

- [x] Étape 2 : références : précédent Corsair `cr017`-`cr019`, Hellcat.
- [x] Étape 5 : mots-pièges : Ressources Basic à deux icônes, « Max 1 per deck », sans module.
- [x] Étape 6 : nombres texte ↔ code : RES `YY`, `BB`, `RR`.
- [x] Étape 7 : Aucun cas (aucune capacité) : valeurs lues sur le scan. Substitution : —
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir l'en-tête.
- [x] Étape 8 bis : NON.
Carte terminée : NON (provisoire) : partie réelle humaine ; Q15.
- [x] **26/10/2026, arbitrage reskins** (RR « A copy of a card is defined by title » + GUIDE §12 bis) : ces trois ressources ne changent que l'image de `01088` / `01089` / `01090` : ART ALTERNATIF des ressources doubles. Traitement, comme Gwenpool / Beast / Binary : collection `chod` dans `COLLECTIONS` (`ui-app/src/board/variantes.ts`) ET dans `COLLECTIONS_RESSOURCES` (`public/js/prepare/app.js`, proposée par défaut au héros « Ch'od » : `collectionDuHeros`). Les cartes restent dans `cards.json` (précédent TMNT / Gwenpool).
      « Max 1 per deck » par TITRE : `validerDeck` (`public/js/deckbuilder/regles.js`, `cleCopie` = titre|sous-titre) compte déjà `01088` + le reskin comme un même titre ; **aucun correctif nécessaire**, preuve : `tools/tests-lanceur/regles-ressources-doubles-par-titre.test.mjs` (4 verts : chaque reskin du dépôt + son officielle = « Trop d’exemplaires de « Energy » : 2/1 », deux mêmes reskins idem, un seul légal, trois titres différents sans gêne). Le moteur n'applique pas MaxPerDeck (seul le constructeur le juge).
      Collection : `ui-app/src/board/resources-art-packs-fanmade-2026-10.test.ts` (45 verts : ordre Energy/Genius/Strength, wizard aligné, images présentes ; ROUGE vu avant le câblage : 18 échecs sur 27, puis rouge à nouveau en retirant l'entrée du wizard).
      Carte terminée : NON (provisoire) : partie réelle humaine (voir la collection « Ch'od » dans la modale du héros et les trois ressources à l'écran).

---

## Questions en attente (option A = celle codée ; consigne du 25/10/2026 : posées à la fin, une par carte)

> **26/10/2026 : relues contre le Rules Reference et les scans** (`VERDICTS-REGLES-2026-10-26.md`). Les points Wild (Q5, Q8, Q10b, Q11, Q13) et les reskins (Q15) sont TRANCHÉS ET CODÉS : voir les blocs « arbitrage Wild / reskins » de co005, co008-co010, co012, co013, co015 et co017-co019. Q10a (« your deck » de Mentor) est traité à part.

- **Q1 co001a** : « a card with the requirement keyword » : A toute carte jouée dont le Requirement imprimé est > 0 (événements ET améliorations) ; B seulement les événements.
- **Q2 co001b** : « search your deck and discard pile » : A deck et défausse (précédent Roz), la défausse en coût est payée même si Cr'reee est introuvable ; B deck seulement.
- **Q3 co002** : ATQ 1* / THW 1* : A valeurs imprimées 1 avec l'étoile du moteur (dégâts conséquents) ; rien d'autre.
- **Q4 co003 / co004** : portent le trait ATTACK / THWART mais le texte n'imprime pas « (attack) » / « (thwart) » : A ce ne sont PAS des attaques / contres (aucun label : pas de Sonné/Désorienté consommé, pas de Déferlement, pas de « après que vous attaquez ») ; B les traiter comme une attaque / un contre. « Taille de main » = le stat (avec ses modificateurs), pas le nombre de cartes.
- **Q5 co005** : A une ressource wild payeuse compte pour les trois lignes (règle du wild) ; B seulement pour la couleur en laquelle le moteur la convertit (physique).
- **Q6 co006** : A seulement les attaques de l'identité de Ch'od (pas celles de ses alliés) gagnent Déferlement ; B aussi celles de ses alliés. La Réponse part quand LE HÉROS abat un sbire (attaque ou capacité).
- **Q8 co008-co010** : une ressource wild IMPRIMÉE compte : A pour les trois couleurs ; B pour aucune.
- **Q9 co011** : Cr'reee glissée sous l'obligation : A elle va à la défausse du joueur quand l'obligation quitte la partie (comportement du moteur, mesuré, récupérable par Forever Friends) ; B elle revient en jeu ou en main (non imprimé).
- **[TRANCHÉ le 26/10/2026 par l'utilisateur : le joueur qui a VAINCU Mentor, voir co012]** **Q10 co012** : « your deck » = A le deck du joueur engagé avec Mentor ; B le premier joueur. Un wild défaussé compte pour les trois couleurs différentes.
- **Q11 co013** : « matches » = A au moins une couleur imprimée en commun (un wild correspond à toutes) ; B la couleur principale seulement. « Tuck a card » : le joueur à qui la carte est révélée choisit (main vide : rien).
- **Q12 co014** : « [star] attacks gain piercing » : A permanent (pas seulement en expert) ; B expert seulement.
- **Q13 co015** : si la carte du dessus du deck n'a aucune ressource imprimée (héros, sbire…), rien n'est défaussé de la main (A) ; un wild défaussé correspond à toutes les cartes de la main ayant une ressource.
- **Q14 co016** : A « number of printed resources » = nombre d'ICÔNES (YY = 2) ; B nombre de couleurs différentes. « boost icons » = icônes de boost imprimées (étoiles exclues).
- **Q15 co017-co019** : A cartes à part (précédent Hellcat/Corsair) ; B arts alternatifs des ressources officielles.

## À vérifier en partie réelle

- Une partie complète avec Ch'od choisi dans la liste Fan-made (tuile « Ch'od »).
- La fenêtre de l'Interruption « Master of All Trades » à chaque carte à Requirement jouée.
- Cr'reee Captured : Cr'reee glissée sous l'obligation à l'écran (fixture écrite à la main, la vraie zone `obligations_area` n'est pas vue).
- Les 20 images à l'écran (Duel of Wits en paysage), et le survol de la biographie dans l'assistant.
- Les icônes de ressource : lues à l'œil, comparées au coin de `01023` / `01022` / `01025` (rouge poing = physique, bleu = mental, jaune éclair = énergie), pas découpées pixel par pixel.
- L'Action d'alter ego de l'obligation à l'écran, et l'effet de Mentor sur la main au fil des rounds.

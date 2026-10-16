# Alopex (TMNT, Inkwire) : gabarits PROCESSUS-CARTE

Preuves du 16/10/2026. Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_alopex.py` (prefixe
`[alopex]`, 87 cas, tous verts) et `tools/cas/dazed.py` (carte d'etat, 18 cas, tous verts).
Substitution : `tools/substituer_pack.py .game-src 43000 ta` (16/16 cartes avec au moins un cas
rouge sans leur module ; les cas restes verts sont tous des TEMOINS d'absence, des bases `desc`
automatiques ou des cas dont la capacite est portee par la carte VOISINE, listes carte par carte
ci-dessous). Dazed : module `status/dazed.py` remplace par un stub, 11 cas rouges / 18 (les 7
verts : temoins, pose et refus de Dazed lus dans le moteur). Gates : `verifier_appels_modules.py`
(alopex et status : OK ; calibre en injectant `DealDamageInexistant`, vu et refuse),
`DECK_NOM=alopex verifier_tous_les_decks.py` (« identite ta001b, main 6, deck 9 »), autoplay
`--deck alopex` rhino + klaw, 8 parties chacun, niveau normal / equilibre : 16 parties, 0
traceback (grep `NameError|AttributeError|TypeError|KeyError|AssertionError|RecursionError|
Traceback` : 0 sur les 16 journaux), 0 incident ; temoin `--deck leonardo`, memes reglages : 16
parties, 0 traceback (les deux decks perdent 16/16 : pas de deck d'aspect, `player_deck` vide).
Statique : `test_cards.py` 6432 ok / 0 erreur ; `verifier_api_cartes.py` : rien sur le pack ;
`audit_cartes.py` : seul signalement, `exhaust_sans_cout` sur ta009 (FAUX POSITIF : l'« exhaust this
card » est le cout de la Reponse DONNEE, ecrite dans la capacite octroyee, pas sur la carte) ;
`verifier_prefixes.py` : `ta` declare. `npx vitest run` : 3593 verts, 3 rouges HORS pack
(`bulles-arts-alternatifs.test.ts` x2 : besoin des arts alternatifs `assets/pics/*_cb.jpg`, absents de
cette copie de travail ; le troisieme etait `vocabulaire-statuts` : « etourdi » reserve a Stunned,
corrige en « hebete », verifie vert apres) ; `npx tsc --noEmit` : 0 erreur.
Decisions utilisateur : `.planning/tmnt/decisions-phase-b.md`. Questions en attente :
`.planning/tmnt/alopex-questions.md` (Q1 Prey deja en jeu, Q2 Nobody et la derniere menace, Q3 Sniff
Out Trouble sans carte a reveler).

Icones de ressource verifiees par decoupe du coin bas-gauche contre 01020 (G), 01021 (B),
01023 (R), 01025 (Y) : ta002 a ta010 portent toutes l'icone « noeuds relies » bleue de 01021 =
**B (mental)**, conformes a `cards.json` (`RES: B`). ta011 Prey n'a pas d'icone ni de cout.
Icones centrales verifiees contre les glyphes de `ChampionsIcons.ttf` : obligation ta012 =
`A` (Acceleration) x2 ; manigance annexe ta013 = `H` (Hazard) x1 ; icones « Y » du coin = Boost
(ta012 : 2, ta013 : 2, ta014 : 2, ta015 : 1).

Etape 8 bis (plateau) : `ui-app/src/board/tmnt-alopex-plateau.test.ts` (11 cas verts :
`cd ui-app && npx vitest run src/board/tmnt-alopex-plateau.test.ts`), lus sur `dessinee(...)`.
Sensibilite prouvee le 16/10/2026 en CASSANT temporairement puis restaurant (git diff vide ensuite) :
(A) `attachees` de `zones.ts` (ligne 343 mise a `[]`) -> 8 cas rouges (Prey, Dazed, Cloaked, Kama,
Kabuki) ; (B) `exhausted` de `card-model.ts` (ligne 485 mise a `false`) -> 2 rouges (identite
inclinee, Kama couchees). Aucun vrai trou d'affichage trouve : l'UI etait deja correcte. Les cas sont
ecrits par etat d'arrivee pose a la main (comme les autres heros TMNT) : ils prouvent le rendu, pas
le moteur. Pas de panorama des paires jumelles 14/15 (ta009 / ta010 :
illustration continue, a trancher par l'utilisateur). Cartes sans cas plateau (ne font que
chiffrer, defausser, piocher) : ta004, ta005, ta006, ta007 (REC), ta012, ta013, ta015.

Moteur partage touche (minimal, additif) : sixieme carte d'etat Dazed (`card_face.py`,
`card_status.py`, `status.py`, `can_status.py`, `checker.py`, `ability.py`, `symbol.py`,
`puzzle.py`/`puzzle_.py` : `Puzzle.Daze` et `Puzzle.EmptyPlayerDiscardPile`, `status/dazed.py`,
`status/cloaked.py` : condition `pas_dazed` sur les degats), compteur `hunter` (`card_face.py`),
harnais `test_capacites.py` (cle de cas `payer_jusqu_a`). UI : `effets-statuts.ts`, `etats.ts`,
`ScanCard.tsx`, `compteurs-fr.ts`, texture `assets/textures/dazed.webp`.

### ta001a : Alopex (Matagi)
- [x] Étape 2 : `ironheart/29015` Falcon (`AfterUnitAttackOrThwart`), `SetupCards.AttachTo` / `AttachTo2` (mise en jeu attachee depuis la reserve).
- [x] Étape 5 : « Forced RESPONSE », « attack AN ENEMY or thwart A SCHEME », « THAT enemy or scheme » (cible de CETTE attaque), « FIND Prey » (Q1), cible vaincue = rien. Résultat : OK, une lecture marquee `TODO-QUESTION` (Q1).
- [x] Étape 6 : CTR 1 / ATQ 2 / DEF 3 / PV 9 / HS 5 lus sur le scan et dans desc. Résultat : OK.
- [x] Étape 7 : attaque de base, contre de base, attaque d'evenement (Pounce) attachent Prey (rouges sans module 3/3) ; contre-cas : Prey deja en jeu ne bouge pas (Q1), cible vaincue, attaque d'un allie (verts sans module : absence d'effet, assume).
- [x] Étape 7 bis : limite NON.
- [x] Étape 8 : autoplay 16 parties, temoin leonardo, 0 traceback.
- [x] Étape 8 bis : OUI. Cas plateau « Prey pend a l'ennemi / a la manigance », « Prey mise de cote ».
Carte terminée : OUI

### ta001b : Alopex (alter ego)
- [x] Étape 2 : `beast/bt001b`, `sunfire/sf001b` (`BeginGameWithSetAside`), `leonardo/tl001b` (Action).
- [x] Étape 5 : « Setup: set your Prey aside » (cree la carte dans la reserve, pas le champ `set_aside` du deck), « up to 2 » (deux recherches), « exhausted », cout de defausse, Action nue. Résultat : OK.
- [x] Étape 6 : REC 3 / PV 9 / HS 6. Résultat : OK.
- [x] Étape 7 : Setup (Prey dans la reserve), 2 Kama du deck inclinees, une seule trouvable, depuis la defausse (rouges 4/5 ; le cas « Action absente en forme heros » est un contre-cas d'absence, vert sans module).
- [x] Étape 7 bis : limite NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI. Cas plateau « Kama mises en jeu inclinees » (attachees a l'identite, couchees).
Carte terminée : OUI

### ta002 : Nobody (Angel Bridges)
- [x] Étape 2 : `AfterUnitAttackEnd` / `AfterUnitThwartEnd` ("This"), fiches cloak.md et daze.md.
- [x] Étape 5 : DEUX Reponses a etoile, « WITH Prey attached », « daze THAT enemy », « cloak HER » (Nobody, pas l'identite), degats consecutifs `1*` : la Reponse part AVANT eux, la carte Cloaked les absorbe. Résultat : OK, Q2 (contre qui vide la manigance).
- [x] Étape 6 : cout 2 / PV 3 / THW 1* / ATQ 1* / RES B. Résultat : OK.
- [x] Étape 7 : daze (rouge), cloak (degat consecutif a 0 avec, 1 sans), contre-cas : sans Prey, mauvais ennemi, derniere menace (Q2). Rouges 3/6, les 3 verts sont des temoins d'absence.
- [x] Étape 7 bis : limite NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI (Dazed sur l'ennemi, Cloaked sur Nobody). Cas plateau « etats Cloaked et Dazed dessines ».
Carte terminée : OUI

### ta003 : Bold Strategy (x3)
- [x] Étape 2 : `td005` (Cloak), `dt107` / `26022` (depense jusqu'a N), `tl013` (choix d'un ennemi).
- [x] Étape 5 : « Cloak ALOPEX » inconditionnel, « You MAY spend UP TO 3 [MENTAL] », « daze AN enemy FOR EACH », un seul Dazed par ennemi. Résultat : OK.
- [x] Étape 6 : cout 1 / RES B / 3 exemplaires. Résultat : OK.
- [x] Étape 7 : 0 / 1 / 3 ressources depensees, 3 ennemis ; 3 ressources pour un seul ennemi. Rouges 4/4.
- [x] Étape 7 bis : limite NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI (Cloaked sur l'identite, Dazed sur les ennemis : cas plateau commun avec ta002).
Carte terminée : OUI

### ta004 : Pounce (x2)
- [x] Étape 2 : `im002` Repulsor Barrage, `61004` (un seul coup 1 + 2n).
- [x] Étape 5 : « 1 damage », « 2 additional FOR EACH », « THAT enemy », « (attack) ». Résultat : OK.
- [x] Étape 6 : cout 0 / RES B / 2 exemplaires ; 1 + 2n, n de 0 a 2. Résultat : OK.
- [x] Étape 7 : 0 -> 1 degat, 1 -> 3, 2 -> 5, cible unique (rouges 4/4).
- [x] Étape 7 bis : limite NON. Étape 8 : OK. Étape 8 bis : NON.
Carte terminée : OUI

### ta005 : Prowl (x3)
- [x] Étape 2 : `doctor_druid/dr005` (contre d'evenement), `nebu/22009` (remise en deck depuis la defausse), `CardFinder(has_printed_res="B")`.
- [x] Étape 5 : « printed [mental] » (la wild imprimee n'en est pas une), « shuffle 1 card » obligatoire, deux phrases. Résultat : OK.
- [x] Étape 6 : cout 2 / RES B / retire 3 menaces. Résultat : OK.
- [x] Étape 7 : une carte mentale revient (Strength/Energy restent), aucune eligible, wild exclue, deux eligibles = une remise (rouges 4/4).
- [x] Étape 7 bis : limite NON. Étape 8 : OK. Étape 8 bis : NON.
Carte terminée : OUI

### ta006 : Sniff Out Trouble (x2)
- [x] Étape 2 : `Worlds.DiscardEncounterTopCard` en boucle, `ho014` / `ss019` (`Reveal` depuis la defausse), `Faces.ReadyAll`.
- [x] Étape 5 : « minion OR SIDE SCHEME », « Reveal that card -> » (cout de la suite : Q3), « draw 2 AND ready EACH [[KAMA]] YOU CONTROL », Action nue. Résultat : OK, Q3.
- [x] Étape 6 : cout 1 / RES B / pioche 2. Résultat : OK.
- [x] Étape 7 : sbire revele + pioche + Kama redressees (deck : la 3e carte reste), manigance annexe, aucun sbire (rien pioche), amelioration non Kama inchangee. Rouges 4/4.
- [x] Étape 7 bis : limite NON. Étape 8 : OK. Étape 8 bis : NON (la carte revelee est resolue par le moteur existant).
Carte terminée : OUI

### ta007 : Mutant Shelter
- [x] Étape 2 : `lj005` Kamala's Room (meme +REC), `harry_osborn/ho013` (`FindTopmost`).
- [x] Étape 5 : « your ALTER-EGO gets +2 REC » (forme heros inchangee), « Alter-Ego Action », « TOPMOST ally ». Résultat : OK.
- [x] Étape 6 : cout 1 / RES B / +2 REC. Résultat : OK.
- [x] Étape 7 : REC 3 -> 5, temoin sans la carte, forme heros (pas de fuite), Action : l'allie le plus haut remonte (deux allies en defausse, un seul part), defausse sans allie, Action absente en forme heros. Rouges 3/6, verts = temoins.
- [x] Étape 7 bis : limite NON. Étape 8 : OK. Étape 8 bis : NON.
Carte terminée : OUI

### ta008 : Kitsune Kabuki
- [x] Étape 2 : `raphael/tr001a` / `30001a` Spider-Ham (compteur depensable comme ressource), `AfterCardLeavePlay`.
- [x] Étape 5 : « as if it were a [MENTAL] » (`Resources("B")`, pas wild), un compteur = une ressource, ressource valable dans les DEUX formes, « Hero Response » (forme heros), « After PREY leaves play ». Résultat : OK.
- [x] Étape 6 : cout 3 / RES B. Résultat : OK.
- [x] Étape 7 : 2 compteurs paient Prowl, 1 compteur ne suffit pas, forme alter-ego, Reponse apres retrait de Prey, apres defaite de la cible (rouges 4/6 ; les 2 verts : un seul compteur, Reponse absente en alter-ego = temoins d'absence).
- [x] Étape 7 bis : limite NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI (compteurs de chasseur sur la carte, carte cliquable pour payer). Cas plateau « ta008 ».
Carte terminée : OUI

### ta009 : Alopex's Kama
- [x] Étape 2 : octroi `tl011` / `tm011` (decision utilisateur du 15/10/2026 : vrai octroi), `AfterCardLeavePlay` + `SetCost`.
- [x] Étape 5 : « EACH KAMA you control gains » (y compris ta010), « exhaust THIS card AND spend a [mental] », « ready ALOPEX », Restricted automatique. Résultat : OK.
- [x] Étape 6 : cout 1 / RES B / Restricted 1. Résultat : OK.
- [x] Étape 7 : Alopex redressee, Kama inclinee, ressource depensee ; l'octroi : ta010 seule n'a rien, ta010 porte la Reponse donnee par ta009 ; sans ressource mentale : non payable. Rouges 2/7 sous le stub de ta009 (les deux cas positifs) ; les 5 verts : temoins d'absence, et cas ou la capacite est portee par ta010 (octroi d'Other Kama a ta009, temoin « ta009 seule »).
- [x] Étape 7 bis : limite NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI (Kama inclinees, cas plateau « Kama »).
Carte terminée : OUI

### ta010 : Alopex's Other Kama
- [x] Étape 2 : octroi comme ta009, `32171b` Metro P.D. / `cn006` (« damage OR threat », `SetLabel('attack', 'thwart')`).
- [x] Étape 5 : « EACH KAMA gains » (ta009 porte aussi l'Action), « (attack/thwart) », « 1 damage OR remove 1 threat », « exhaust THIS card ». Résultat : OK.
- [x] Étape 6 : cout 1 / RES B / 1 degat ou 1 menace. Résultat : OK.
- [x] Étape 7 : 1 degat, option menace, octroi a ta009, deux Kama = deux Actions (1 + 2 = 3 degats, Prey posee apres la 1re), l'attaque et le contre de l'Action profitent de Prey ; ta009 seule : rien ; forme alter-ego : rien. Rouges 6/10, verts = temoins d'absence et cas du porteur voisin.
- [x] Étape 7 bis : limite NON. Étape 8 : OK (autoplay : « Other Kama s'active, 1 degat a Rhino »). Étape 8 bis : OUI (couchees, plateau).
Carte terminée : OUI

### ta011 : Prey
- [x] Étape 2 : `62009` (+N degats a la cible attachee), `37013` (`RemoveAdditionalThreat`), `61014` (`AttachedScheme`), `21180b` (Interruption forcee « leaves play »).
- [x] Étape 5 : « ALOPEX' attacks » (l'identite, pas un allie), « ATTACHED enemy / scheme » (pas les autres), « 1 ADDITIONAL », « set ASIDE » (reserve, pas defausse). Piege paye : l'Interruption forcee se relancait a l'infini (SetAside quitte le jeu) : drapeau anti-boucle, voir RECETTES §7novemdecies. Résultat : OK.
- [x] Étape 6 : pas de cout / pas de ressource / +1 degat / +1 menace. Résultat : OK.
- [x] Étape 7 : +1 degat (base et evenement), +1 menace (base et evenement), mise de cote (cible vaincue, defaussee), cycle complet avec Matagi (rouges 7/11, verts = les 4 contre-cas d'absence).
- [x] Étape 7 bis : limite NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI (Prey pendue a l'ennemi ou a la manigance, absente quand mise de cote). Cas plateau « ta011 Prey ».
Carte terminée : OUI

### ta012 : Manipulated
- [x] Étape 2 : `harry_osborn/ho013` (obligation + `PlayerActionToDiscardThis`), `leonardo/tl013` (meme equipe).
- [x] Étape 5 : « Action » nue (forme heros ET alter-ego), « Exhaust ALOPEX AND deal 1 damage ... -> » (deux parties de cout), « EACH CHARACTER YOU CONTROL » (identite + allies), « charcter » (typo du scan) corrige. Résultat : OK.
- [x] Étape 6 : Boost 2 / Acceleration 2 / GiveTo « Alopex » dans desc ; cas `icones`. Résultat : OK.
- [x] Étape 7 : Action (cout et degats, obligation defaussee), identite deja inclinee : non payable, forme alter-ego. Rouges 2/5 : les 3 verts sont des bases `desc` automatiques (Give To, Acceleration, Boost) et un temoin.
- [x] Étape 7 bis : limite NON. Étape 8 : OK. Étape 8 bis : NON.
Carte terminée : OUI

### ta013 : You Belong To Me
- [x] Étape 2 : `WhenThisRevealed`, `Players.ForEachPlayer` (`raphael/tr014`), `DefausserUneCarteDeLaMain` (`57062`).
- [x] Étape 5 : « EACH player », « from THEIR hand » (choix du joueur), main vide = rien. Résultat : OK.
- [x] Étape 6 : StartingThreat `2*` (menace 2 a un joueur), Hazard 1, Boost 2. Résultat : OK (cas `icones`).
- [x] Étape 7 : 1 joueur (2 -> 1), 2 joueurs (mains 2 -> 1 et 6 -> 5, temoin 2 et 6), main vide. Rouges 2/5, verts = temoins et bases `desc`.
- [x] Étape 7 bis : limite NON. Étape 8 : OK. Étape 8 bis : NON.
Carte terminée : OUI

### ta014 : Kitsune
- [x] Étape 2 : `leonardo/leonardo_nemesis/tl016` (`WhenThisRevealed` + Cloak sur soi), `Faces.ExhaustAll`.
- [x] Étape 5 : « Cloak KITSUNE » (elle-meme), « exhaust YOUR identity » (l'identite du joueur a qui elle est revelee, quelle que soit la forme). Résultat : OK.
- [x] Étape 6 : MNG 2 / ATQ 2 / PV 2 / Boost 2 / Nemesis Alopex. Résultat : OK.
- [x] Étape 7 : forme heros (Cloaked + Alopex inclinee), forme alter-ego (l'alter-ego inclinee). Rouges 2/3 ; le vert est la base `desc` Boost 2.
- [x] Étape 7 bis : limite NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI (Cloaked sur le sbire). Cas plateau « Cloaked sur Alopex et sur Kitsune ».
Carte terminée : OUI

### ta015 : Curse of Nine Tales (x3)
- [x] Étape 2 : `06030` Trickster (option 1 mot pour mot), `raphael_nemesis/tr016` (`AskDiscardFaces`), `joueur.ChooseAbilities`.
- [x] Étape 5 : « Choose ONE », « YOUR deck / allies YOU control », « FOR EACH DIFFERENT card TYPE », « Discard 2 allies » (exactement deux, option absente avec un seul allie). Résultat : OK.
- [x] Étape 6 : Boost 1 (desc : traitrise defaussee apres revelation, non mesurable en jeu ; lu sur le scan), menace +1 par type. Résultat : OK.
- [x] Étape 7 : trois cartes de deux types (+2), trois evenements (+1), deck vide, option 2 (deux allies defausses), un seul allie (option 1 forcee). Rouges 4/5, le vert est le cas deck vide (absence d'effet).
- [x] Étape 7 bis : limite NON. Étape 8 : OK. Étape 8 bis : NON.
Carte terminée : OUI

### Heros : gate finale
- [x] Étapes 1 a 8 du heros (cards.json + checksum, sets_info, starter, nemesis, images via `tools/importer_images_alopex.py`, bio FR/EN dans `heros-info.js`, textes FR dans `textes-fr-fanmade.ts` + copie publique regeneree, traits `FOX`, `WITCH`).
- [x] `verifier_tous_les_decks` pour le deck alopex : vert. « Partie complete » : 16 parties d'autoplay sans traceback.
- [ ] NON PROUVE : survol de la bio dans le wizard (aucun navigateur pilote ici), partie jouee par un humain dans le navigateur, panorama 14/15, rendu reel des scans.

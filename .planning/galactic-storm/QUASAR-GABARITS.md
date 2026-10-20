# Quasar (Galactic Storm, Kajislav, lot GS-2) : gabarits PROCESSUS-CARTE, une fiche par carte

Date : 20/10/2026. Copie de travail `gs2-quasar`. Cas : `Fusion/marvel-lcg-src/tools/cas/quasar.py` (filtre
`[quasar]`). Questions : `.planning/todos/2026-10-20-gs2-questions.md` (Q-GS2-1 a 5 ; la lecture recommandee est codee).
Images relues une a une (planche de decoupes des icones de ressource : coin bas gauche de chaque carte contre les reskins
Strength 67 / Genius 66 / Energy 65 du meme deck, RES=RR/BB/YY, et contre sk010 / sk025 du meme auteur, RES=G).

Preuves communes a toutes les fiches (sorties dans le rapport final) :
- `test_cards` : 6828 ok / 0 err ; `verifier_appels_modules galactic_storm` : OK (calibre : un appel invente dans gs303
  est signale « 1 appel(s) inexistant(s) ») ; `verifier_api_cartes` : 0 fichier galactic_storm en faute ;
  `verifier_ignore_crise` : OK ; `verifier_prefixes` : OK ; `verifier_coherence_cartes` : aucune remarque gs.
- `[quasar]` : 59/59 verts (57 cas de capacite + 2 fixtures de plateau).
- Substitution (`substituer_pack.py ... gs`) : 18/18 cartes avec au moins un cas rouge sans leur module ; les cas qui
  restent verts sont des cas de DONNEES (valeurs imprimees, lues dans `desc`) ou des contre-cas d'ABSENCE, listes
  carte par carte ci-dessous.
- Autoplay : `--deck quasar --vilains rhino --parties 8` : 0 bloquee, 0 traceback (grep NameError|AttributeError|
  TypeError|KeyError|AssertionError|Traceback : 0 sur les 8 journaux) ; temoin spider_man, meme fournee : 0 bloquee,
  0 traceback. Journal lu (partie 4) : Bandes posees au Setup, No Holding Back paye Y + joker des Bandes (joker
  precise [physical] : 3 degats), Flight of Light vide Crowd Control puis 1 de plus sur le complot, Maelstrom revele
  glisse les Bandes, Entropy Ascendant entre avec son Entrave.
- Deck : `verifier_tous_les_decks` passe complete (fichier moteur partage touche) : 150/151, le 151e (hulkling) tombe
  sur un `JSONDecodeError` de cards.json pendant que le script d'insertion le reecrivait ; relance seul : OK (151/151).
- Plateau (etape 8 bis) : `ui-app/src/board/quasar-plateau.test.ts`, 8 tests verts sur deux fixtures PRODUITES PAR
  LE MOTEUR (cas `[quasar] ... plateau : fixture`, verificateur `qz_fixture_plateau`, `QUASAR_FIXTURE_DIR`).
  Vu ROUGE : fixture regeneree avec le module gs099q vide -> « les Quantum Bands glissees sont dessinees sous
  Maelstrom » echoue (1 failed / 5 passed), vert avec le module. Les autres tests de plateau mesurent le rendu
  d'etats que le moteur pose (pions, attache, statut, zone) : rien de neuf dans `zones.ts`, aucun correctif plateau.

---

### gs300a : * Quasar (heros)

- [x] Etape 2 : `sk002a` (Action pure a inclinaison en cout, `WhenInYourPlayTurn(Action).SetCostFunc(Exhaust("This"))`),
      `31009`/`an001a` (`Faces.ReadyAll`).
- [x] Etape 5 : « Action » (pas Hero Action : face heros seulement, contre-cas alter ego) ; « Exhaust Quasar → » = cout ;
      « ready Quantum Bands » = condition Bandes en jeu ET inclinees (une capacite ne s'initie pas sans effet possible).
      Resultat : conforme.
- [x] Etape 6 : PV 11, CTR 2, ATQ 2, DEF 2, main 5, GUARDIAN (desc + cas « valeurs imprimees »). Resultat : conforme.
- [x] Etape 7 : « Channel the Bands : Bandes inclinees -> ... » rouge sans module / vert avec ; contre-cas « Bandes
      deja pretes » et « absente en ALTER EGO » verts sans module (absence, assume) ; valeurs : donnees.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay commun (0 traceback).
- [x] Etape 8 bis : change ce qu'on voit ? NON (redresse une carte : la jauge d'inclinaison est deja couverte).

Carte terminee : OUI

### gs300b : * Wendell Vaughn (alter ego)

- [x] Etape 2 : `sk001b` / `as001b` (`SetupPutIntoPlay`).
- [x] Etape 5 : « Setup: Put Quantum Bands into play » : la 16e carte, fabriquee (pas dans les 15). Conforme.
- [x] Etape 6 : PV 11, REC 3, main 6, S.H.I.E.L.D (trait moteur sans point final). Conforme.
- [x] Etape 7 : « Chosen as the Protector : Setup ... » rouge sans module / vert avec (Bandes en jeu, controlees) ;
      valeurs : donnees.
- [x] Etape 7 bis : NON.
- [x] Etape 8 : autoplay commun ; deck monte (« identite gs300a, main 6, deck 34 »).
- [x] Etape 8 bis : OUI (met une carte en jeu) : fixture `quasar-bandes-revenues.json` (Bandes attachees a
      l'identite, face visible) dans `quasar-plateau.test.ts` ; le rouge n'a ete montre que sur le glissement
      (gs099q), chemin d'affichage identique (`bind_object_id`).

Carte terminee : OUI

### gs301 : * Quantum Bands

- [x] Etape 2 : `sk002a` (permanente sans cout, trait donne par nom), `41002b` / `sk013` (`CanGenerateResources` +
      `Exhaust("This")`).
- [x] Etape 5 : « Permanent » base auto ; « QUASAR gains AERIAL » = nom de la face heros (contre-cas alter ego) ;
      « Hero Resource » ; icone du texte = joker (decoupe), decision de l'utilisateur Q6 : joker au choix. Conforme.
- [x] Etape 6 : pas de cout, RES G imprime (case verte), 1 joker genere. Conforme.
- [x] Etape 7 : AERIAL en heros (rouge sans module) ; ressource paie seule Quantum Absorption (rouge sans module) ;
      contre-cas alter ego (AERIAL absent, pas de ressource) verts sans module (absence) ; Permanent : donnees.
- [x] Etape 7 bis : NON.
- [x] Etape 8 : autoplay commun (Bandes payent No Holding Back, glissees par Maelstrom).
- [x] Etape 8 bis : OUI (glissee sous Maelstrom, remise en jeu) : `quasar-plateau.test.ts`.

Carte terminee : OUI

### gs302 : * Epoch

- [x] Etape 2 : `14001a` / `04032` (`AfterUnitUseBasicPower`).
- [x] Etape 5 : « one of HER basic powers » = attaquer / contrer (`powers=["ATK","THW"]`) ; « ★ » = renvoi (Q6) ;
      etoiles creuses = degats consecutifs (Q6). Conforme.
- [x] Etape 6 : cout 4, PV 4 (pastille), CTR 1* (1 consecutif), ATQ 3*** (3 consecutifs), RES G. Cas : degats
      consecutifs mesures (1 apres contre, 3 apres attaque). Conforme.
- [x] Etape 7 : contre et attaque redressent les Bandes : 2 cas rouges sans module ; valeurs : donnees.
- [x] Etape 7 bis : NON.
- [x] Etape 8 : autoplay commun.
- [x] Etape 8 bis : NON.

Carte terminee : OUI

### gs303 : Flight of Light (x2)

- [x] Etape 2 : `sh019` (`if_this_remove_last_threat`), `08013` (2e cible dans l'operation).
- [x] Etape 5 : « the LAST threat from THAT scheme » ; « a scheme » = 2e cible libre. Conforme.
- [x] Etape 6 : cout 2, RES R (poing), 3 puis 2. Conforme.
- [x] Etape 7 : 2 cas (annexe videe : 5 -> 3 ; annexe non videe : complot inchange), 2/2 rouges sans module.
- [x] Etape 7 bis : NON.
- [x] Etape 8 : autoplay commun (lu partie 4).
- [x] Etape 8 bis : NON (menace).

Carte terminee : OUI

### gs305 : No Holding Back (x2)

- [x] Etape 2 : `47021` Multitalented (`GetPaidResources(True)`).
- [x] Etape 5 : « for each [physical] / [mental] resource you used to pay » ; joker = couleur choisie (FAQ p.22) ;
      une attaque de 3n, un contre de 2n. Conforme.
- [x] Etape 6 : cout 2, RES R, 3 et 2. Conforme.
- [x] Etape 7 : RR -> 6 degats ; BB -> 4 menaces ; joker [physical] + [mental] -> 3 et 2 : 3/3 rouges sans module.
- [x] Etape 7 bis : NON.
- [x] Etape 8 : autoplay commun (lu partie 4 : 3 degats, joker des Bandes en [physical]).
- [x] Etape 8 bis : NON.

Carte terminee : OUI

### gs307 : Righteous Fury (x2)

- [x] Etape 2 : `ag006` (`if_this_attack_defeats`).
- [x] Etape 5 : « defeats » (≠ damages) ; « ready Quasar » = l'identite. Conforme.
- [x] Etape 6 : cout 3, RES Y (eclair), 6 degats. Conforme.
- [x] Etape 7 : Rhino survit (Quasar reste incline) ; Shocker vaincu (Quasar pret) : 2/2 rouges sans module.
- [x] Etape 7 bis : NON. [x] Etape 8 : autoplay commun. [x] Etape 8 bis : NON.

Carte terminee : OUI

### gs309 : Unbreakable Guard (x2)

- [x] Etape 2 : `sj010` (`WhenUnitWouldTakeDamage(HeroInterrupt, Friend)`), `tj004` (payeurs).
- [x] Etape 5 : « a friendly character », « any amount », « prevent ALL », « THAT character », « with Quantum Bands ».
- [x] Etape 6 : cout 1, RES B (noeuds). Conforme.
- [x] Etape 7 : payee Genius -> 0 degat sans Tenace ; payee Bandes -> 0 degat + Tenace : 2/2 rouges sans module.
- [x] Etape 7 bis : NON. [x] Etape 8 : autoplay commun.
- [x] Etape 8 bis : OUI (statut Tenace) : `quasar-plateau.test.ts` (« la Tenace est dessinee sur l'allie qui la
      porte », Tenace de la fixture posee par `Puzzle.Tough` : meme carte d'etat, meme rendu).

Carte terminee : OUI

### gs311 : Quantum Energy (x2)

- [x] Etape 2 : factory `AfterYouSpendThisCard`.
- [x] Etape 5 : « After you spend THIS card » ; « Response » (deux formes) ; condition Bandes inclinees. Conforme.
- [x] Etape 6 : RES G (1 joker, case verte). Conforme.
- [x] Etape 7 : redresse les Bandes (rouge sans module) ; valeur imprimee : donnees.
- [x] Etape 7 bis : NON. [x] Etape 8 : autoplay commun. [x] Etape 8 bis : NON.

Carte terminee : OUI

### gs313 : Quantum Absorption

- [x] Etape 2 : `32047` / `34020` (fenetre de paiement), `sk001b` (soin).
- [x] Etape 5 : « DEFENSE event », « with Quantum Bands », « heal 2 from Quasar ». Conforme.
- [x] Etape 6 : cout 1, RES G, 2. Conforme.
- [x] Etape 7 : soin 5 -> 3 (rouge sans module) ; sans les Bandes, evenement ATTACK : verts sans module (absence).
- [x] Etape 7 bis : NON. [x] Etape 8 : autoplay commun. [x] Etape 8 bis : NON (PV).

Carte terminee : OUI

### gs315 : Quantum Jump

- [x] Etape 2 : `34020` (+ menace), `15012` / `hc006` (ignorance selon le paiement), `UnitIgnoreKeywordIcons`.
- [x] Etape 5 : « THWART event », « that thwart », « 2 additional », « crisis AND patrol ». Ecart moteur documente :
      ciblage offert tant que les Bandes PEUVENT payer (comme 15012), tranche a la resolution ; CORRECTIF moteur pour
      la Patrouille a la resolution.
- [x] Etape 6 : cout 2, RES G, +2. Conforme.
- [x] Etape 7 : +2 (6 -> 1), Crise (6 -> 1), Patrouille (6 -> 1) rouges sans module ; « payee avec Genius sous
      Patrouille » rouge sans module (FoL injouable) ET rouge sans le CORRECTIF moteur (6 -> 3, mesure) ; « sans les
      Bandes » et « Crise, Bandes inclinees » verts sans module (absence). 4/6.
- [x] Etape 7 bis : NON. [x] Etape 8 : autoplay commun. [x] Etape 8 bis : NON.

Carte terminee : OUI

### gs316 : Quantum Weapon

- [x] Etape 2 : `32047` / `54002` (+1 degat sur l'attaque payee), `GainPiercing` / `GainOverKill`.
- [x] Etape 5 : « that attack », « 1 additional », « piercing AND overkill ». Conforme.
- [x] Etape 6 : cout 2, RES G, +1. Conforme.
- [x] Etape 7 : 7 degats ; Sandman Tenace vaincu + 3 d'exces : 2 rouges sans module ; « sans les Bandes » vert (absence).
- [x] Etape 7 bis : NON. [x] Etape 8 : autoplay commun. [x] Etape 8 bis : NON.

Carte terminee : OUI

### gs349 : Quantum Bubble

- [x] Etape 2 : factory `AfterPlayerPlayedCard` (`paid_res_effects`), `Faces.GiveStatus`.
- [x] Etape 5 : « ally », « with Quantum Bands », « that ally » ; moment de la Reponse : Q-GS2-4 (recommande code).
- [x] Etape 6 : cout 2, RES G, numero imprime 49. Conforme.
- [x] Etape 7 : Martinex paye par les Bandes -> Tenace (rouge sans module) ; sans les Bandes (absence).
- [x] Etape 7 bis : NON. [x] Etape 8 : autoplay commun.
- [x] Etape 8 bis : OUI (statut) : `quasar-plateau.test.ts` (Tenace sur Martinex).

Carte terminee : OUI

### gs065 : Protector of the Universe (obligation)

- [x] Etape 2 : `tr013` / `vv011` (`PlayersCannotChangeForms`), `sk029` (vaincre ennemi ou manigance), `bt001a`
      (`take_no_damage`), `53029` (retrait de pion), fiche uses.md.
- [x] Etape 5 : « Uses » base auto ; « cannot flip to ALTER-EGO » ; trois declencheurs ; « from here ». Conforme.
- [x] Etape 6 : 3 pions, 1 retire, 2 icones de boost. Conforme.
- [x] Etape 7 : forme bloquee, defense sans degat, ennemi vaincu, manigance vaincue, dernier pion : 5/5 rouges.
- [x] Etape 7 bis : NON (pas de limite imprimee).
- [x] Etape 8 : autoplay commun (obligation melangee au deck rencontre).
- [x] Etape 8 bis : OUI (compteurs) : `quasar-plateau.test.ts` (3 pions duty dessines).

Carte terminee : OUI

### gs099q : * Maelstrom (sbire nemesis)

- [x] Etape 2 : `se005` / `td012` (glisser), `sk038` (`AfterCardLeavePlay`), `sk032` (sbire nemesis du meme auteur).
- [x] Etape 5 : « Tuck QUANTUM BANDS » (permanente : exception moteur) ; « leaves play » ; « the Quasar player ».
- [x] Etape 6 : MNG 1, ATQ 2, PV 5, 2 boost, numero 99 (Q-GS2-1). Conforme.
- [x] Etape 7 : revele -> Bandes glissees (rouge sans module) ; vaincu -> Bandes revenues : vert sans module car sans
      le module les Bandes ne partent jamais (la precondition change) ; avec le module, ce cas prouve le retour
      (Bandes glissees PUIS remises en jeu). Valeurs : donnees.
- [x] Etape 7 bis : NON. [x] Etape 8 : autoplay commun (lu partie 4 : glissement).
- [x] Etape 8 bis : OUI : `quasar-plateau.test.ts` (Bandes dessinees sous Maelstrom, puis de retour sur Quasar).

Carte terminee : OUI

### gs239q : Entropy Ascendant (manigance annexe nemesis)

- [x] Etape 2 : fiche hinder.md, `65011` (cout des evenements de chaque joueur), fiche requirement.md.
- [x] Etape 5 : « EACH event card », « requirement » (pas un cout en plus) ; evenement a 0 : Q-GS2-3.
- [x] Etape 6 : menace 3, Entrave 1 par joueur (4 a un joueur), 3 boost. Conforme.
- [x] Etape 7 : FoL payee RR reste en main (rouge sans module) ; YY jouee, amelioration non touchee, menace : verts
      sans module (temoins / donnees).
- [x] Etape 7 bis : NON. [x] Etape 8 : autoplay commun (lu partie 4).
- [x] Etape 8 bis : OUI (manigance en jeu) : `quasar-plateau.test.ts`.

Carte terminee : OUI

### gs237q : Avatar of Oblivion (attachement nemesis)

- [x] Etape 2 : `16131` (`highest_atk`), `01185` (meme Interruption forcee mot pour mot), `sk064` (trait donne).
- [x] Etape 5 : « the MINION with the highest ATK », « If you cannot → surge », « instead ». Conforme.
- [x] Etape 6 : +1 ATK (desc ATK+), aucune icone de boost. Conforme.
- [x] Etape 7 : attache + ELITE + ATQ +1 ; defaite remplacee ; Renfort sans sbire : 3/3 rouges sans module.
- [x] Etape 7 bis : NON. [x] Etape 8 : autoplay commun.
- [x] Etape 8 bis : OUI (attache) : `quasar-plateau.test.ts` (Avatar dessine sur son porteur ; dans la fixture,
      Shocker et Maelstrom ont ATK 2 a egalite et le moteur l'a attache a Maelstrom : egalite = choix, regle
      ordinaire ; le cas de capacite, lui, ne met que Shocker en jeu).

Carte terminee : OUI

### gs240q : Distant Manipulation (traitrise nemesis, x2)

- [x] Etape 2 : `hs052` (« Choose to either ... If you cannot, surge »).
- [x] Etape 5 : « each card with a "Resource" ability you control » : Q-GS2-2 (recommande code) ; « each resource
      card from your hand » ; option impossible non offerte. Conforme.
- [x] Etape 6 : 1 icone de boost. Conforme.
- [x] Etape 7 : incliner ; defausser ; Renfort : 3/3 rouges sans module.
- [x] Etape 7 bis : NON. [x] Etape 8 : autoplay commun. [x] Etape 8 bis : NON (inclinaison / defausse).

Carte terminee : OUI

---

## Reskins (19) : arts alternatifs, pas de cartes

Chaque scan compare a l'officielle (cout, ressource imprimee, PV, CTR/ATQ et degats consecutifs, traits, unicite,
texte) : identiques, seule l'illustration change (Starhawk et Martyr ajoutent un sous-titre au bandeau, sans effet).
16 officielles recoivent le code d'art « quasar » (`data/arts_alternatifs.json`, images `assets/pics/<id>_quasar.jpg`
615x882) : 56046, 21065, 22035, 17022, 48014, 16012, 09020, 17020, 18019, 47021, 32014, 54033, 19012, 09015, 10031,
19020. Energy / Genius / Strength forment la collection de ressources « quasar » (`variantes.ts`, `app.js`). Pas de
capacite propre, donc pas de cas de capacite : les officielles gardent leurs cas.

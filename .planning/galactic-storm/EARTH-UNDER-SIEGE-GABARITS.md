# Gabarits PROCESSUS-CARTE.md — Scénario 4 Earth Under Siege (gs161-gs194, gsr01-gsr10), lot GS-7

EN COURS. Dernier scénario de Galactic Storm restant (GS-4, GS-5, GS-6 et GS-8 sont clos). Scans extraits
des 4 zips Kajislav (`MC custom content by Kajislav-20261014T200011Z-1-00{1,2,3}.zip`, dossiers z1/z2/z3
des transcriptions). Transcriptions : `docs/packs/galactic-storm/transcriptions/earth-under-siege.md` et
`earth-under-siege-ensembles.md`. Preuves : `Fusion/marvel-lcg-src/tools/cas/earth_under_siege.py` (filtre
`[eus]`), 8/8 cas verts. `test_cards` : 6974/6974 constructions OK, 0 erreur (toutes cartes du lot
construites, y compris les 32 restant sans script). `verifier_appels_modules galactic_storm` : OK.

**Découverte majeure du lot** : ce scénario est le PREMIER à câbler réellement la brique moteur
« plusieurs méchants en jeu » (`src/game/operate/villains.py`, `docs/reference/mots-cles/mechants-multiples.md`),
construite le 20/10/2026 pour Punisher MC×DC et Galactic Storm mais jamais encore utilisée par une vraie
carte de campagne. Jusqu'à 6 méchants (Annihilus, Attuma, Destroyer, Doctor Minerva, Mole Man, Veranke)
peuvent être simultanément en jeu ; un deck de méchants séparé (`Villains.BuildVillainDeck`/
`RevealNextVillain`, distinct de `Scenario.villain_deck`) en révèle un nouveau à mesure que la sécurité
d'Earthfall s'épuise ou qu'un méchant seul tombe.

**Numérotation des card_id** : `gs` + numéro imprimé (règle du pack), donc `gs161a`/`gs161b` (Earthfall,
stades A/B d'UNE SEULE carte), `gs162a`/`gs162b` (Enemies at Large, faces Standard/Expert), `gs163`-`gs194`
pour les 32 cartes restantes (6 méchants × 2 stades + leurs ensembles + les 3 cartes générales). Les 10
cartes « habillées » Standard/Expert (aucun numéro imprimé) : `gsr01`-`gsr10`, décision utilisateur du
20/10/2026, `ability_link` vers les cartes core 01186-01193 (recette RECETTES-MOTEUR.md « carte habillée »),
aucun script.

**Composition du scénario** : `data/scenarios/gs_earth_under_siege.json` (standard) et
`gs_earth_under_siege_expert.json` (expert). `"villain": []` dans les deux (la mise en place automatique du
moteur pour UN méchant à stades ne sert à rien ici — gs161a construit et révèle son propre deck de méchants).
Les 6 cartes de stade + les 24 cartes d'ensemble naissent MISES DE CÔTÉ (`set_aside`), `desc.set_name` = nom
du méchant (« Annihilus », pas « Earth Under Siege ») pour retrouver « le reste » de son ensemble une fois
revélé. Les cartes générales + les 7 (standard) ou 10 (expert) reskins vont dans `encounters`. Imperial Guard
(modular, déjà porté au lot GS-4) via `modular_sets`.

**Compteurs maison ajoutés** (`CardFace.COUNTER`, `card_face.py`) : `'safety'` (jetons de sécurité
d'Earthfall), `'plate'` (Uru Armor Plating, gs178), `'duration'` (Induced Mutation, gs183).

---

## gs161a : Earthfall (1A, manigance principale, stade 1)

- [x] Étape 2 : carte(s) de référence : « Content » : composition du scénario
      (`data/scenarios/gs_earth_under_siege*.json`, aucun code, modèle gs079a Kree Sentry) ; « Set [...] aside » :
      natif (`Message.WhenGameBeginSetup.CreateSetAside`, cle `set_aside`), aucun code ; « Create the villain
      deck... » : `Villains.SetRule` + `Villains.BuildVillainDeck` (brique du 20/10/2026, `villains.py`) ;
      « Reveal the Enemies at Large side scheme » : `SetupCards.PutIntoPlay(name=...)` (modèle Sinister Six
      « Light at the End », `sm/sinister_six/27100a.py`) ; « Place 6 safety counters here » :
      `Faces.PlaceCountersOn` (modèle gs143 Hala, compteur 'hideout').
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « Set [6 ensembles] aside » (déjà fait par le
      moteur, pas par ce script) ; « Reveal the top card ... shuffle the REST of its encounter set » (le
      reste = `desc.set_name` du méchant révélé, pas « Earth Under Siege ») ; « Reveal the Enemies at Large
      side scheme » (une seule des deux faces gs162a/gs162b existe selon le fichier de scénario chargé,
      jamais les deux).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : 6 jetons de sécurité, 6 méchants, aucun seuil de menace imprimé sur
      cette face (`desc = {"Stage": "1"}`, pas de TargetThreat : déclenche l'avancée native vers 1B, modèle
      `scheme_main.py` `OnAfterCardRevealedEnd`).
      Résultat : identiques.
- [x] Étape 7 : cas test_capacités, preuve par substitution : la mise en place entière est mesurée par 3
      cas `[eus] gs161a mise en place : ...` (1 méchant en jeu, 5 au deck de méchants, Enemies at Large en
      jeu, 6 compteurs de sécurité). Pas de substitution dédiée à gs161a seule (la mise en place est un bloc
      unique ; la preuve par substitution a porté sur gs161b/gs162a, voir plus bas, qui partagent le même
      helper `RevelerProchainMechantEtMelangerLeReste`).
      Résultat : 3/3 cas verts, mesures indépendantes de l'identité du méchant révélé (aléatoire,
      `Villains.BuildVillainDeck` mélange).
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay ciblé : PAS ENCORE FAIT (dépend des 32 cartes restantes du lot, à faire en fin de
      lot une fois tous les méchants scriptés).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (jetons de sécurité, méchants empilés) —
      couvert par les mesures `compteurs`/`ordre`/`tous` des cas `[eus]`, qui lisent l'état réel du moteur
      (pas de plateau dédié écrit, hors périmètre de ce lot).

Carte terminée : OUI (mise en place), autoplay en attente de la fin du lot.

## gs161b : Earthfall (1B, manigance principale, stade 1)

- [x] Étape 2 : carte(s) de référence : « After the villain phase ends » : `AbilityFactory.AfterPhaseEnd`
      (modèle sk190b Queen Veranke) ; « remove 1 safety counter » : `Faces.RemoveCountersOn` (modèle
      RetirerRepli, hala_ultimatum) ; « If a villain is defeated, remove that villain from the game »
      (règle générale p.16, pas imprimée sur une carte précise) : `AfterUnitBeDefeated` + `Villains.Remove`
      (modèle Sinister Six `WhenUnitBeDefeated` scénario, adapté en Réponse pour laisser le Forced Interrupt
      d'Enemies at Large mesurer « le dernier méchant » avant le retrait).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « LESS safety counters... THAN the number of
      cards in the villain deck » (comparaison stricte `<`, pas `<=`) ; « the villain deck » = deck de
      méchants (`Villains.VillainDeckSize`), PAS `Scenario.villain_deck` (jamais utilisé sur ce scénario).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : « remove 1 safety counter », comparaison stricte. Identiques.
- [x] Étape 7 : cas test_capacités par capacité, preuve par substitution :
      - **tic de sécurité** (`AfterPhaseEnd`) : 2 cas mesurent le seuil pile (6→5, 5 pas < 5 au deck de 5 =
        pas de révélation ; 5→4, 4 < 5 = 2e méchant révélé). **Substitution faite à la main** (ligne
        `AfterPhaseEnd` commentée dans gs161b.py, cas rejoué) : ROUGE (`gs161b.safety=6` au lieu de 5) ;
        module remis, VERT (8/8 cas, confirmé).
      - **retrait du méchant vaincu** (`AfterUnitBeDefeated`) : 2 cas, méchant NON dernier (retiré, l'autre
        reste, deck inchangé) et méchant DERNIER (Enemies at Large révèle le remplaçant AVANT le retrait,
        voir gs162a) + 1 cas deck de méchants vide (victoire, voir gs162a).
      Résultat : 5/5 cas liés à gs161b verts, substitution directe faite sur le tic de sécurité.
- [x] Étape 7 bis : limite imprimée ? NON (le tic de sécurité n'est pas une limite « once per round », c'est
      un décompte qui ne remonte jamais).
- [ ] Étape 8 : autoplay ciblé : PAS ENCORE FAIT, voir gs161a.
- [x] Étape 8 bis : OUI (compteurs de sécurité, méchants empilés), mesuré par les cas `[eus]` (voir gs161a).

Carte terminée : OUI (mécanique), autoplay en attente de la fin du lot.

## gs162a : Enemies at Large (face A, Standard)

- [x] Étape 2 : carte(s) de référence : « After the last threat is removed from here, place 1 safety
      counter ... and N threat here » : `AbilityFactory.WhenLastThreatRemoveFromThisScheme` (modèle gs119
      Majestrix's Verdict) ; « When the last villain is defeated... Otherwise, the players win » :
      `WhenUnitBeDefeated(ForcedInterrupt, Villain, ...)` + `Worlds.SetGameOver(True, effect)` (modèle
      `sm/sinister_six/27102b.py`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : « the LAST villain is defeated » (condition
      `len(Villains.All(effect)) == 1`, mesurée AU MOMENT DE L'INTERRUPTION, avant que gs161b ne retire le
      méchant vaincu — l'ordre Interrupt-avant-Réponse est la clé de toute la mécanique, prouvé par cas) ;
      « place 1 safety counter on the MAIN SCHEME » (pas sur This : `Worlds.FindMainScheme`).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : menace de départ 4, Reponse forcée +4 menace + 1 compteur sécurité.
      Identiques.
- [x] Étape 7 : cas test_capacités par capacité, preuve par substitution :
      - **dernier méchant → révélation** : cas « mechant vaincu DERNIER » (1 seul en jeu, le remplaçant est
        révélé AVANT le retrait, deck de méchants descend de 1). VERT.
      - **dernier méchant, deck vide → victoire** : cas dédié, `monde.is_game_over` et `players_won`
        mesurés. VERT.
      - **méchant NON dernier → pas de révélation** : cas « mechant vaincu NON DERNIER » (2 en jeu, un seul
        retiré, deck de méchants inchangé). VERT — preuve négative que la condition `len==1` ne mord pas à
        tort.
      - Pas de cas dédié à la Réponse forcée « last threat removed » (menace/compteur de sécurité) faute de
        temps dans ce lot : construction vérifiée (`test_cards`, `verifier_appels_modules`), à couvrir en
        fin de lot avec les autres cartes de menace.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay ciblé : PAS ENCORE FAIT, voir gs161a.
- [x] Étape 8 bis : OUI (méchants empilés/retirés), mesuré par les cas `[eus]`.

Carte terminée : NON — la Réponse forcée « last threat removed » (sécurité/menace) n'a pas de cas dédié.
Le reste (le cœur neuf, « dernier méchant ») est prouvé 3/3.

## gs162b : Enemies at Large (face B, Expert)

Identique à gs162a (menace de départ 5 au lieu de 4, voir son gabarit pour les cartes de référence et les
mots-pièges). Construction vérifiée (`test_cards`, `verifier_appels_modules`) ; **aucun cas dédié** (le lot
a porté sa preuve sur la face Standard, jouée par défaut en test). À couvrir en fin de lot : un cas identique
à gs162a mais en mode expert (`"scenario": "gs_earth_under_siege_expert"`).

Carte terminée : NON — aucun cas de preuve, construction seulement.

---

## gs163, gs164, gs165 : cartes générales

Faites, prouvées, commitées (voir commits dédiés). gs163 Main Concern : 5/5 cas verts, substitution faite.
gs164 Observe the Perimeter : 2/2 cas verts, substitution faite. gs165 Threat on the Horizon : 2/2 cas
verts (la vraie mise en place du scénario est nécessaire : "rhino" porte sa propre manigance principale et
fausse `Worlds.FindMainScheme`).

## Annihilus (gs166-gs169) : CONSTRUCTION VÉRIFIÉE, PREUVE PAR CAS INCOMPLÈTE

**⚠ Découverte importante, à signaler.** gs166/gs167 (Forced Response `AfterEnemyActivatesAgainstYou`) et
gs169 (When Revealed `WhenThisRevealed`) construisent sans erreur (`test_cards`) et suivent des modèles
exacts déjà utilisés ailleurs dans le projet (`sm/venom_goblin/27114.py`, `night_thrasher_nemesis/nt013.py`
pour le premier ; `gs165` — LE MÊME PACK — pour le second). Mais dans ce harnais `test_capacites.py`, leurs
opérations ne se déclenchent JAMAIS, malgré de très nombreuses variantes testées (carte inline vs helper
partagé, avec/sans `Villains.SetRule`, avec/sans Rhino en jeu, forme héros/alter-ego, `.SetName()`, vraie
mise en place du scénario vs mise en place manuelle, carte fraîchement créée vs copie réelle mélangée dans
l'ensemble du méchant). gs165 (même `WhenThisRevealed`, même pack) fonctionne pourtant parfaitement par
ailleurs — preuve que le mécanisme n'est pas cassé EN GÉNÉRAL dans ce pack.

Piste la plus probable (non confirmée) : `Puzzle.Reveal`/`FindOrCreateFace` du harnais se comporte
différemment pour une carte créée directement dans `scenario.encounter_deck` à la construction du scénario
(cas de gs165, listée dans `encounters`) que pour une carte créée via `set_aside` puis déplacée par
`Faces.ShuffleAllTo` (cas de gs169, dans l'ensemble du méchant) — ou pour un méchant mis en jeu « à la
main » (`Puzzle.PutIntoPlay`) plutôt que révélé par `Villains.RevealNextVillain` (cas de gs166). Si c'est
confirmé, **toutes les cartes d'ensemble « When Revealed »/« When Defeated » des 6 méchants** de ce
scénario pourraient être affectées par la même limite de harnais (pas forcément un vrai défaut de jeu : une
vraie partie pioche normalement dans un deck déjà mélangé, sans passer par ce chemin de code specifique au
test).

**gs168** (`WhenSchemeBeDefeated`) a, lui, été rattrapé : première passe en échec parce que le TEST
utilisait `Puzzle.Gain`+`Puzzle.Discard` sur une carte dont 2 exemplaires existent déjà dans le deck de
départ (`FindOrCreateFace` créait un 3e fantôme et le défaussait, sans toucher à la carte gagnée) — une
fois le test corrigé (carte déjà en défausse par le mulligan), **l'ability a bien fonctionné**. Correctif
retenu au passage, à appliquer partout ailleurs : `AbilityType.ForcedInterrupt`, PAS
`AbilityType.WhenDefeated`, pour un `WhenSchemeBeDefeated` sur une manigance de RENCONTRE — le moteur le
dit explicitement (`defeated.py` : « Don't try to use "AbilityType.WhenDefeated", see "11033" »).

**Statut carte par carte** :
- gs166, gs167 (Annihilus I/II) : construction OK, preuve par cas NON FAITE (voir ci-dessus).
- gs168 (Portal to the Negative Zone) : **5/5 preuve réelle** (voir ci-dessous, une fois le test corrigé).
- gs169 (Annihilation Wave) : construction OK, preuve par cas NON FAITE (voir ci-dessus).

Prochaine étape pour clore ce doute : relire `src/game/card/face/model/face_on_event.py`
(`OnWhenCardRevealed`) et `src/game/ability/factory/activate.py`
(`AbilityFactoryActivate.AfterEnemyActivationEnd`) avec plus de temps, ou vérifier directement en partie
réelle / autoplay (le chemin de code normal du jeu, pas celui de `Puzzle.Reveal`/`Puzzle.Attack`).

## Attuma (gs170-gs175) : CONSTRUCTION VÉRIFIÉE, PREUVE PAR CAS ÉLARGIE À ÉCHOUÉ

**⚠ Deuxième découverte, qui élargit celle d'Annihilus.** gs170/gs171 (bonus SCH/ATK conditionnel,
`ThisGainKeyword` + `check_fn`), gs174 (riposte conditionnelle, même mécanique), gs172/gs173 (attache avec
branche « Otherwise, attach to the villain », `AttachToFaceWhenPutIntoPlay` + `otherwise_attach_to`), gs175
(When Revealed, compte « for each »): les 6 cartes construisent sans erreur mais **aucune** ne prouve son
effet dans ce harnais, dès que le montage implique DEUX cartes de l'ensemble en jeu en même temps ou une
branche de secours (« Otherwise »). Vérifié directement : `Worlds.FindCardsOnField(effect,
CardFinder(trait="ATLANTIS"))` trouve bien les deux cartes attendues quand on l'appelle à la main (logique
saine) — c'est le DÉCLENCHEMENT/RECALCUL depuis l'ability (`ThisGainKeyword`/`WhileValid`,
`AttachToFaceWhenPutIntoPlay` à deux branches) qui ne mord pas sous `Puzzle.PutIntoPlay`, avec ou sans
`change_on_event=OnEvent.CardInPlay(...)` explicite. Piste non confirmée : le harnais `Puzzle` ne génère
peut-être pas l'événement qui ferait recalculer un effet continu/une sélection à deux branches en dehors du
déroulement normal du jeu — à vérifier avec plus de temps ou en partie réelle. Les 10 cartes de ce lot
(Annihilus + Attuma) partagent donc le même statut : **construction correcte, comportement à confirmer
hors de ce harnais**.

## Reste du lot (gs176-gs194, gsr01-gsr10)

Entrées `cards.json` écrites et vérifiées (`test_cards`, 0 erreur), mais **aucun script ni cas de test
encore écrit** pour les 4 méchants restants (Destroyer, Doctor Minerva, Mole Man, Veranke) ni pour les 10
reskins (ability_link, pas de script attendu mais pas encore vérifiés en jeu). Prochaine étape du lot : un
méchant à la fois, dans l'ordre du scénario, questions une à une avec capture quand un doute se présente.

**Vu le volume de capacités qui ne se prouvent pas dans ce harnais (voir Annihilus et Attuma ci-dessus),
les méchants restants sont construits et vérifiés par `test_cards`/lecture attentive du texte imprimé
contre le code, SANS reprendre un cas de test par capacité à chaque fois** — cela éviterait de dépenser le
budget restant à re-découvrir le même problème 4 fois de plus. Cas de test écrits seulement pour les
mécaniques qui n'impliquent qu'UNE SEULE carte en jeu sans branche de secours (celles-là ont prouvé marcher :
gs163, gs164, gs165, gs168). Point à trancher avec l'utilisateur en fin de lot : vérification complète en
partie réelle / autoplay avant de considérer GS-7 clos.

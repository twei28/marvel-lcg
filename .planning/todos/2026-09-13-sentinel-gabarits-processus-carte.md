# Sentinel (T-Wrecks, set 173) — gabarits PROCESSUS-CARTE, 26 cartes

**Livré le 13/09/2026.** Préfixe `st`. Pack de HÉROS : identité recto verso, quatre
améliorations **recto-verso** posées au setup, 8 cartes signature (15 exemplaires),
1 obligation, 5 cartes némésis, 2 extras hors set, plus la quatrième carte d'état du
moteur. `PROCESSUS-HEROS.md` s'applique, donc `PROCESSUS-CARTE.md` 26 fois. Relevé
complet et vocabulaire dans `2026-09-12-sentinel-releve-des-cartes.md`.

**Ce pack a exigé cinq chantiers moteur.** Trois étaient prévisibles à la lecture des
cartes, les deux derniers sont sortis du harnais :

1. **`exposed`, quatrième carte d'état** (fiche `mots-cles/exposed.md`) : le moteur n'en
   connaissait que trois. `CardFace.STATUS`, `StatusCard.symbol_name`, `Symbol`,
   `Status.exposed`, `CanStatus.exposed` / `HasStatus`, `Puzzle.Expose`, et côté plateau
   `effets-statuts.ts`, `etats.ts`, `CardEffectDelta`.
2. **`Support` hérite de `CanAttach`** : `st010` Juston Seyfert est un SOUTIEN qui dit
   « Action: Attach to a side scheme ». Le moteur ne savait attacher que les `Asset2`.
3. **`Support.bind_face`** repasse la main à `CanAttach` quand la carte vit dans une zone
   d'améliorations : sans cela `GetBindFace()` levait une assertion sur Juston attaché.
4. **`DamageProperty.unpreventable`** : le mot-clé maison DESTROY inflige « 2 dégâts
   imblocables », et le moteur n'avait aucun moyen de le dire. Détail plus bas.
5. **Quatre tables d'états figées à trois entrées** : le symbole affiché à la défausse
   d'un état (`sender_unit.py`), `has_status="Any"` et `canbe_status="Any"`
   (`checker.py`), le ciblage par nom (`ability.py`), l'annotation de `on_event.py`.

## Ce qui a été mesuré, et comment

| Gate | Résultat |
|---|---|
| `tools/verifier_prefixes.py` | OK, `st` réservé, 26 cartes, aucun numéro emprunté |
| `tools/verifier_noms_modules.py .game-src sentinel` | OK, aucun nom inconnu |
| `tools/verifier_appels_modules.py .game-src <port> sentinel` | OK, tous les appels existent |
| `tools/verifier_desc_mots_cles.py sentinel` | OK, 26/26 `desc` conformes au texte |
| `tools/verifier_coherence_cartes.py` | textes fr 26/26, images 26/26, cas cités 100 % |
| `tools/verifier_traductions_fr.py` | 153 clés, 154 littéraux, 0 sans traduction |
| `tools/test_cards.py` | 5565 cartes construites, **0 erreur** |
| `tools/test_capacites.py`, batterie COMPLÈTE | **1913/1917**, 0 processus mort |
| `verifier_tous_les_decks.py` (`DECK_NOM=sentinel`) | OK, « identité st001a, main 6, deck 9 » |
| `tools/test_capacites.py` filtre `st0` | **42/42** |
| `tools/substituer_pack.py st0` | **26/26** cartes avec au moins un cas rouge sans module |
| `verifier_tous_les_decks.py` (les 136 decks) | **136/136** montent une partie |
| `tools/autoplay.py` sentinel / rhino + klaw, 16 parties | **0 traceback, 0 partie bloquée**, 3,5 et 4,1 rounds |
| `tools/autoplay.py` témoin night_thrasher, 16 parties | 0 traceback, 3,4 et 4,1 rounds — même profil |
| `ui-app` : `npx tsc --noEmit` + 1334 tests | vert |

⚠ **Un piège de nommage, qui a caché deux cas pendant une journée** : les deux cas de la
carte d'état s'appelaient « EXPOSED … », sans `st0`. Le filtre du pack ne les voyait pas,
le compte annonçait 40/40, et le cas nominal était **faux depuis le début**
(`Puzzle.Attack(x)` fait ATTAQUER x : nommer le vilain le faisait frapper le héros).
Trouvé par la batterie complète, pas par la passe filtrée. Les cas portent désormais
`st002a` dans leur nom.

Les cas rouges de la batterie complète sont **antérieurs à ce pack**, vérifié en
rejouant les six suspects **avec les correctifs moteur retirés par `git stash`** : ils
tombaient exactement pareil. Six d'entre eux (`bl015`, `sm014` ×2, `sm016`, `su019`,
`ze010`) ont été **réparés le 13/09/2026** : `remplir_les_decks_vides` donnait 25
ressources inertes à quatre héros qui n'ont jamais eu de moitié d'aspect, et ces cas
comptent précisément ce qui sort du dessus du deck. Il ne reste que les quatre du héros
mis de côté.

**Cas verts sans module, assumés** : ce sont tous des CONTRE-CAS d'absence d'effet, ou
des cas qui appartiennent à une autre face.

| Carte | Cas resté vert | Pourquoi c'est normal |
|---|---|---|
| `st001a` | témoin « plus aucun Component intact » | le cas prouve que l'interruption NE se déclenche PAS ; sans module elle ne se déclenche pas non plus |
| `st002b` | témoin « Head encore INTACTE » | ce cas mesure `st002a`, pas la face détruite |
| `st003b` | témoin « Arms encore INTACTE » | idem, il mesure `st003a` |
| `st005a` | cas de setup des quatre pièces + témoin « sans l'action » | le setup appartient aux quatre cartes ; le témoin prouve une absence |
| `st006` | témoin « sans Arms (Intact) » | absence d'effet, la carte doit rester injouable |

## Cinq défauts trouvés par le harnais, jamais par relecture

**1. La face DESTROYED agissait pendant que la face INTACT était visible.** `IsInPlay()`
accepte, par défaut, n'importe quelle face du même NOM COURT, et `ModelName.SetName`
coupe la parenthèse finale : « Arms (Intact) » et « Arms (Destroyed) » s'appellent
toutes deux « Arms ». Les trois malus de coût s'appliquaient donc en permanence, et la
moitié de la batterie tombait pour une seule raison — toutes les cartes coûtaient un cran
de plus. Corrigé par `IsThisFaceUp()` dans `VosCartesCoutentUnDePlus`. **Le même piège a
fait passer le cas `st015` au vert sans son module** (`en_jeu_trait` compte lui aussi des
faces invisibles) : d'où la vérification outillée `sentinel_pieces_detruites`.

**2. Ablative Protocol démontait le robot entier d'un seul coup.** Les 2 dégâts de la
destruction sont eux-mêmes des dégâts « que vous alliez subir » : l'interruption se
relançait, et une attaque à 2 retournait les QUATRE pièces. L'insert dit pourtant
« 2 **unpreventable** damage », et remplacer des dégâts EST une prévention. Le moteur ne
savait pas l'exprimer : les deux seules cartes officielles qui emploient le mot
(`62001a` Luke Cage, `62028` Internal Injury) se contentaient d'`ignore_tough`, qui ne
ferme qu'une porte sur trois. **`DamageProperty.unpreventable` a donc été ajouté**, honoré
par `PreventDamage` ET par `SetBeInstead`, et les deux cartes officielles ont été mises à
jour au passage.

**3. L'ordre « dégâts puis retournement » ne terminait jamais.** Avant même le correctif
ci-dessus, trois parties d'autoplay se bloquaient sur « Ablative_Protocol, cibles légales
[11, 10, 9, 8] » reposée à l'identique : les dégâts arrivaient avant le retournement,
donc la relance retrouvait la même pièce intacte. `Detruire()` retourne d'abord.

**4. « Exposed » faisait planter le moteur à chaque défausse.** `AfterStatusDiscardFrom`
tenait une table de symboles figée à trois entrées et levait un `KeyError`. Le harnais ne
l'a pas vu : le moteur attrape l'exception, écrit `crash.json` et continue. **47
tracebacks** sont sortis des journaux d'autoplay. Trois autres tables à trois états ont
été étendues au passage (`has_status="Any"` et `canbe_status="Any"` dans le filtre de
cartes, le ciblage par nom dans `ability.py`, l'annotation de `on_event.py`).

**5. Mark VII-A défaussait une amélioration PERMANENTE.** « If you cannot, discard 1
upgrade you control » : les quatre Component sont permanents, donc indéfaussables, et
`DiscardInternal` tombait sur son assertion. Quatre tracebacks de plus. Le filtre du
moteur (`checker.py:170`) est repris mot pour mot dans la carte.

⚠ **Les deux sortent de l'autoplay, pas de la batterie.** C'est la démonstration que le
grep des tracebacks de l'étape 8 n'est pas une formalité : aucun des 42 cas ne les
voyait, et tous restaient verts.

## Deux pièges de montage, pour ne pas les repayer

- **Hydra Mercenary (01101) porte GARDE** : le vilain cesse d'être une cible légale
  d'attaque tant qu'il est engagé. Le cas `st009` ne frappait qu'un seul ennemi. Sbire de
  remplacement : Shocker (01103).
- **Le complot principal `01097b` a un seuil de 7\*** : `Puzzle.SetThreat('01097b', 8)`
  l'accomplit et la partie est perdue avant le test. Plafond utile : 6.
- **`Puzzle.Attack(x)` fait ATTAQUER x**, il ne l'attaque pas. Nommer le vilain le fait
  frapper le héros.
- **Ne jamais relancer le harnais sur une plage de ports voisine de la précédente** : les
  sockets restent en TIME_WAIT et les fils meurent sur `AssertionError: ip/port`. C'est
  la cause des 49 « processus mort » de la première passe complète, pas un défaut de
  carte. Éloigner la base de ports d'au moins un millier.
- **Une carte dont le coût n'est pas payable ne revient PAS en main** : le moteur la pose
  sur la table puis la défausse. Un cas de surcoût doit donc mesurer l'ABSENCE D'EFFET,
  jamais `en_main`.

## Ce que les gates ne peuvent pas voir

- **La partie réelle dans le navigateur n'a pas été jouée par un humain.** Les cartes sont
  prouvées une à une et le deck monte une partie complète en autoplay, mais « est-ce que
  le héros est agréable » reste ouvert. Outil manquant : aucun, c'est une main humaine.
- **Le plateau téléphone** (bandes, 480×1050) n'a pas été regardé avec ce héros : les
  quatre Component sont des améliorations attachées à l'identité, cas déjà couvert par
  d'autres packs, et la carte d'état Exposé passe par le chemin générique des statuts
  (test unitaire ajouté). À confirmer à l'œil au premier essai.
- **Le taux de victoire ne dit rien** : `player_deck` est vide (9 cartes de deck), Sentinel
  s'épuise comme Night Thrasher dans les mêmes conditions. Une nuance quand même :
  Sentinel finit **éliminé 12 fois sur 16** contre 8 sur 16 pour le témoin. C'est le
  pilote, pas la carte — il accepte TOUJOURS Ablative Protocol, y compris pour remplacer
  1 dégât par 2 plus une pièce perdue. Un humain ne le fera pas.

## Gabarits, une carte par section

L'étape 8 (autoplay ciblé) est la même pour toutes les cartes du pack et n'est donc pas
recopiée vingt-six fois : voir la ligne unique du tableau de mesures.

### st001a : * Sentinel (face héros)
- [x] Étape 2 : `49006` Magnetic Bubble (seul montage qui remplace intégralement des dégâts, `SetBeInstead`), contre `08032` / `31019` qui ne PRÉVIENNENT qu'une partie.
- [x] Étape 5 : `instead` → remplacement total, pas `PreventDamage(n)` ; `a COMPONENT upgrade` → UN seul, et seulement une pièce encore INTACT (le sélecteur porte `trait="INTACT"`, ce qui borne aussi la chaîne) ; `Interrupt` nue mais imprimée sur la face héros. Résultat : conforme.
- [x] Étape 6 : 2 dégâts imblocables par destruction (mot-clé), aucun autre nombre. Résultat : conforme.
- [x] Étape 7 : nominal (1 pièce retournée, 2 dégâts subis, 5 dégâts d'origine disparus) + témoin sans pièce intacte. Rouge sans module sur le nominal. Résultat : 1/2, le témoin est un contre-cas assumé.
- [x] Étape 7 bis : pas de limite imprimée. NON.
- [x] Étape 8 bis : OUI, la carte RETOURNE une amélioration. Couvert par la vérification outillée `sentinel_pieces_detruites`, vue ROUGE avant le correctif d'ordre (quatre pièces au lieu d'une).
Carte terminée : OUI.

### st001b : * Sentinel (face alter-ego)
- [x] Étape 2 : `06001b` Odinson (recherche deck + défausse puis `GainCard`), `45014` (`CostFunc.Discard("YourHandCards")`), `dz017a` (`Faces.FlipAllTo(..., None, ...)`).
- [x] Étape 5 : `flip each` → TOUS d'un coup, aucune sélection ; `(Limit once per phase.)` → `LimitOncePerPhase` et non `PerRound` ; `Setup` → AUCUN script, `desc.Setup` porte déjà les quatre pièces, en écrire un les mettrait en jeu deux fois. Résultat : conforme.
- [x] Étape 6 : 1 carte défaussée. Résultat : conforme.
- [x] Étape 7 : recherche de Juston (main vidée d'abord), retournement de deux pièces détruites. Rouge sans module. Résultat : 3/3.
- [x] Étape 7 bis : OUI. Témoin : deck refait avec DEUX Juston, deux Actions dans la même phase, la main s'arrête à 2 cartes.
- [x] Étape 8 bis : OUI, retournement d'améliorations. Même vérification que ci-dessus.
Carte terminée : OUI.

### st002a : * Head (Intact)
- [x] Étape 2 : `nt003a` (permanente recto-verso posée par `desc.Setup`), `av009` / `09009` (action de héros à inclinaison), `dz037` (cibles multiples).
- [x] Étape 5 : `expose 2 enemies` n'est PAS « up to 2 » → `range=("Zero", 2)` ; `enemies` → `Enemy`, vilain compris ; exposer = poser la carte d'état maison. Résultat : conforme.
- [x] Étape 6 : 2 ennemis. Résultat : conforme (deux Exposé posés, pièce inclinée).
- [x] Étape 7 : cas nominal, rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI, la carte pose un STATUT. Couvert côté plateau par `effets-statuts.test.ts` (badge « Exposé ») et `etats.test.ts` (pastille E), tous deux vus rouges avant l'ajout d'`exposed` aux tables.
Carte terminée : OUI.

### st002b : * Head (Destroyed)
- [x] Étape 2 : `nt003b` (seconde face permanente), `aa018` / `39062` (surcoût de jeu), helper du pack pour le filtre par TRAIT.
- [x] Étape 5 : `THWART events` → ÉVÉNEMENTS seuls ; `Your` → le contrôleur de la pièce ; pas de `desc.Setup` sur cette face. Résultat : conforme.
- [x] Étape 6 : +1 ressource. Résultat : conforme (Clear the Area à 1 devient impayable avec une seule carte-ressource).
- [x] Étape 7 : cas nominal + jumeau positif. Rouge sans module sur le nominal. Résultat : 1/2, le jumeau mesure `st002a`.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON (aucun changement visible hors le coût affiché, déjà porté par `ui.cost`).
Carte terminée : OUI.

### st003a : * Arms (Intact)
- [x] Étape 2 : `av009` Bear Arms (action de héros étiquetée `attack` sur une amélioration), `nt003b` pour `DealDamage`.
- [x] Étape 5 : l'étiquette `(attack)` compte — sans elle, pas de riposte ni de Coriace ni d'Exposé ; `an enemy` → une seule cible ; c'est le COMPONENT qui frappe, aucune statistique du héros. Résultat : conforme.
- [x] Étape 6 : 1 dégât. Résultat : conforme.
- [x] Étape 7 : cas nominal, rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### st003b : * Arms (Destroyed)
- [x] Étape 2 : jumelle exacte de `st002b`, trait ATTACK.
- [x] Étape 5 : mêmes mots-pièges. Résultat : conforme.
- [x] Étape 6 : +1 ressource. Résultat : conforme (Press the Advantage reste sans effet).
- [x] Étape 7 : nominal + jumeau positif. Résultat : 1/2, le jumeau mesure `st003a`.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### st004a : * Torso (Intact)
- [x] Étape 2 : `03007` Steve's Apartment (`HealthUnits` + `SetTarget("YourIdentity", canbe_heal=True)`), `av009`.
- [x] Étape 5 : `heal 1 damage from Sentinel` → nom propre, mais action de HÉROS donc `YourIdentity` suffit ; `canbe_heal` indispensable, sinon l'action reste proposée à un Sentinel indemne. Résultat : conforme.
- [x] Étape 6 : 1 dégât soigné. Résultat : conforme (3 → 2).
- [x] Étape 7 : cas nominal, rouge sans module. ⚠ Les quatre pièces sont détruites AVANT la blessure puis Torso remontée : sinon Ablative Protocol intercepte les dégâts et l'action n'a plus de cible. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### st004b : * Torso (Destroyed)
- [x] Étape 2 : `39062` Growing Pains, posé sur le helper du pack (la fabrique du moteur ne regarde pas quelle face est visible).
- [x] Étape 5 : `your upgrades` → un TYPE de carte, pas un trait ; le surcoût frappe aussi les autres Component, mais aucun ne se joue depuis la main. Résultat : conforme.
- [x] Étape 6 : +1 ressource. Résultat : conforme (Targeting Protocol reste hors jeu).
- [x] Étape 7 : cas nominal, rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### st005a : * Legs (Intact)
- [x] Étape 2 : `05008` Nakia Bahadir et `54019` Man on the Wall (`Worlds.UpdateNextCardPlayCost`), `av009`.
- [x] Étape 5 : ARBITRAGE — l'auteur écrit « the next card you play » sans durée, le moteur EXIGE `"Phase"` ou `"Turn"`. On retient `"Phase"`, la durée officielle de cet effet sur les deux cartes de référence. Résultat : conforme, écart documenté.
- [x] Étape 6 : −1 au coût. Résultat : conforme (un événement à 1 part d'une main sans la moindre ressource).
- [x] Étape 7 : nominal + témoin sans l'action. Rouge sans module sur le nominal. Résultat : 1/3 (le cas de setup appartient aux quatre pièces, le témoin est un contre-cas).
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### st005b : * Legs (Destroyed)
- [x] Étape 2 : `04165` Martial Law (`hand_size=-1`), `06007` Asgard pour le signe inverse.
- [x] Étape 5 : `You` → les DEUX faces de l'identité, d'où la cible `"You"` et non un nom propre (piège inverse de nt003a). Résultat : conforme.
- [x] Étape 6 : −1 carte en main. Résultat : conforme (mesuré par `attributs: {hand_size: -1}`).
- [x] Étape 7 : cas nominal, rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### st006 : Exterminate
- [x] Étape 2 : `06005` Hammer Throw (coût additionnel qui incline une amélioration nommée + `AttackProperty`), `04044` Piercing Strike.
- [x] Étape 5 : `Arms (Intact) AND any one other` → DEUX pièces dont la première est IMPOSÉE (condition de la capacité), la seconde choisie (sélecteur de coût) ; le choix « inclinez ou détruisez » se pose pour CHACUNE ; `ranged, piercing, overkill` dans un seul `AttackProperty` ; l'exposition vient APRÈS les dégâts et n'est pas liée à la cible. Résultat : conforme.
- [x] Étape 6 : 2 ressources, 7 dégâts, 2 ennemis exposés. Résultat : conforme.
- [x] Étape 7 : nominal + témoin sans Arms. Rouge sans module sur le nominal. Résultat : 1/2.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI (statut Exposé), couvert par les tests de plateau cités en `st002a`.
Carte terminée : OUI.

### st007 : Hardwire Access
- [x] Étape 2 : `03011` Falcon: Sam Wilson (retrait de menace RÉPARTI, `repeat_rules="Threat"`), `36010` Torrential Rain.
- [x] Étape 5 : `from among schemes in play` → la menace se RÉPARTIT ; `Exposed status cards in play` → tout le plateau, alliés compris ; X se lit au moment de la sélection ; aucune mention de Crise. Résultat : conforme.
- [x] Étape 6 : 3 + X menaces. Résultat : conforme (6 → 3 sans Exposé, 6 → 1 avec deux).
- [x] Étape 7 : deux cas, X = 0 et X = 2. Rouges sans module. Résultat : 2/2.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON (menace, déjà couverte).
Carte terminée : OUI.

### st008 : Rocket Punch
- [x] Étape 2 : `06005` Hammer Throw, `04044`.
- [x] Étape 5 : `or destroy it` → « it » désigne Arms, pas une pièce au choix ; une pièce déjà inclinée reste payable par la destruction. Résultat : conforme.
- [x] Étape 6 : 5 dégâts, 2 dégâts imblocables si destruction. Résultat : conforme.
- [x] Étape 7 : nominal (inclinaison) + branche destruction sur une pièce déjà inclinée. Rouges sans module. Résultat : 2/2.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI (retournement), couvert par le second cas qui exige `en_jeu: st003b` / `hors_jeu: st003a`.
Carte terminée : OUI.

### st009 : Threat Suppression
- [x] Étape 2 : `dt005` Blast Radius (`range=("Zero", 3)`), `al012` / `ih003` (`MayChooseFace` dans une liste déjà restreinte).
- [x] Étape 5 : `of those enemies` → l'assommement ne vise que les ennemis QUI VIENNENT D'ÊTRE BLESSÉS ; `up to 2` → on demande deux fois, le joueur peut s'arrêter ; `different enemies` → le sélecteur ne rend jamais deux fois la même carte. Résultat : conforme.
- [x] Étape 6 : 1 dégât, 3 ennemis, 2 assommés. Résultat : conforme.
- [x] Étape 7 : cas nominal à deux ennemis, rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI (statut Sonné), chemin générique déjà couvert.
Carte terminée : OUI.

### st010 : * Juston Seyfert
- [x] Étape 2 : `04135` Twisted Reality / `03032` Followed (carte attachée à une manigance annexe), `09009` (action à inclinaison), `dz037` (choix entre deux branches).
- [x] Étape 5 : `side scheme` → annexe uniquement, `SchemeSide2` ; `put ... in play under your control` → il QUITTE la manigance vaincue, d'où la fenêtre « When ... be defeated » ; `Ready Sentinel or up to 2` → un choix, pas les deux, et la seconde branche accepte zéro à deux cartes. Résultat : conforme.
- [x] Étape 6 : 1 menace retirée, jusqu'à 2 pièces redressées. Résultat : conforme (3 → 2 menaces).
- [x] Étape 7 : attache + retrait de menace, puis manigance vaincue → Sentinel redressé. ⚠ C'est `pret` qui prouve, pas `en_jeu` : sans son module Juston est un soutien ordinaire et entre en jeu tout seul. Rouges sans module. Résultat : 2/2.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI, la carte CHANGE DE ZONE (elle s'attache). Correctif moteur `Support` + `CanAttach`, vu rouge par l'assertion de `GetBindFace()`.
Carte terminée : OUI.

### st011 : Propulsion Array
- [x] Étape 2 : `56007` Hunted (coût additionnel sur la capacité de jeu), `61005` Infiltration (`ShuffleAllTo`), `aa005` / `dz037` (`ChooseAbilities`).
- [x] Étape 5 : `Shuffle this card into your deck` est la PREMIÈRE instruction de l'effet, pas un coût ; chaque branche a son propre coût d'inclinaison ; les deux ne visent que des pièces INTACT. Résultat : conforme.
- [x] Étape 6 : coût imprimé 0, 1 pièce inclinée ou 2 redressées. Résultat : conforme.
- [x] Étape 7 : cas nominal (première branche), rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI, la carte QUITTE le jeu pour le deck. Mesuré par `dans_deck_joueur`.
Carte terminée : OUI.

### st012 : Reinforced Plating
- [x] Étape 2 : `56007`, `an006` / `42030` (`CostFunc.Discard("This")`), `49009` (`GiveStatus Tough`), `dz017a` (`FlipAllTo`).
- [x] Étape 5 : `Discard Reinforced Plating →` : la flèche fait de la défausse un COÛT, donc sans pièce détruite en jeu la carte NE DOIT PAS partir ; `flip 1` → une seule ; le Coriace va au JOUEUR. Résultat : conforme.
- [x] Étape 6 : 1 pièce retournée, 1 Coriace. Résultat : conforme.
- [x] Étape 7 : cas nominal, rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON (deux exemplaires au deck, aucune limite imprimée).
- [x] Étape 8 bis : OUI (retournement + statut), mesuré par `en_jeu` / `hors_jeu` / `statuts`.
Carte terminée : OUI.

### st013 : Targeting Protocol
- [x] Étape 2 : `st002a` (exposition), `dz037` / `aa005` (choix), `03011` (montant calculé à la sélection).
- [x] Étape 5 : `a scheme` → UN complot, rien à répartir, contrairement à `st007` ; `in play (to a maximum of 3)` → tout le plateau, plafonné ; sans Exposé la seconde branche retire zéro et reste proposée. Résultat : conforme.
- [x] Étape 6 : 2 ennemis, ou X menaces plafonné à 3. Résultat : conforme.
- [x] Étape 7 : cas nominal (première branche), rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI (statut Exposé), déjà couvert.
Carte terminée : OUI.

### st014 : Prime Directive
- [x] Étape 2 : `nt012` Practice (`WhenThisObligationGiveToYou` + `ChooseAbilities` à branches conditionnelles), `01170` Business Problems, `ih003` (`AskChooseFace`).
- [x] Étape 5 : `another friendly character` → vos alliés, jamais votre identité ; `(MUTANT if able)` n'est PAS un filtre de cible mais une CONTRAINTE, d'où la liste calculée ; sans allié la première branche disparaît et la menace devient le seul choix ; les deux branches défaussent la carte. Résultat : conforme.
- [x] Étape 6 : 3 dégâts ou 3 menaces, 3 icônes de boost (relevées à l'image, `desc` corrigé). Résultat : conforme.
- [x] Étape 7 : cas nominal sans allié, rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### st015 : * Mark VII-A
- [x] Étape 2 : `04080` Dense Forest (`AfterUnitAttackUnit(..., is_undefended_attack=True)`), `dz017a` (`FlipAllTo`).
- [x] Étape 5 : « FLIP », PAS « DESTROY » — l'auteur écrit « flip ... to its DESTROYED side », le mot-clé ferait subir 2 dégâts imblocables EN PLUS ; `against you` → le joueur attaqué ; `If you cannot` est un REPLI, pas un choix ; `1 upgrade you control` → n'importe laquelle SAUF une PERMANENTE, que la règle interdit de défausser (défaut trouvé en autoplay). Résultat : conforme.
- [x] Étape 6 : 5 PV, CTR 2, ATQ 2\*, 3 icônes de boost (relevées à l'image, `desc` corrigé). Résultat : conforme.
- [x] Étape 7 : attaque non défendue → DEUX pièces tombent, une par Ablative Protocol et une par la Réponse forcée. Vérification OUTILLÉE obligatoire, `en_jeu_trait` comptant des faces invisibles. Rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI (retournement), mesuré par la vérification outillée.
Carte terminée : OUI.

### st016 : Rogue Asset
- [x] Étape 2 : `04092` Super Absorbing Power (`GiveKeywordToInPlayWhenApplyThis(..., apply=...)` + `GainTraits`), `03025` Honorary Avenger.
- [x] Étape 5 : DEUX familles distinctes (Component INTACT d'une part, TECH d'autre part) ; une pièce DÉTRUITE n'est plus HACKED, ce qui est une vraie porte de sortie ; le trait vaut pour tous les joueurs. Résultat : conforme.
- [x] Étape 6 : 3 menaces de départ, 3 icônes de boost (relevées à l'image). Résultat : conforme.
- [x] Étape 7 : trait donné aux pièces intactes + témoin d'une pièce détruite qui ne le porte pas. Rouges sans module. Résultat : 2/2.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON (un trait ne se dessine pas).
Carte terminée : OUI.

### st017 : Disabled
- [x] Étape 2 : `01095` Rhino (`Search.EncounterCard`), `05029` Harvest (incliner toute une famille), `wd014` (statut + boost étoile).
- [x] Étape 5 : `If you cannot` ne se déclenche que si AUCUNE pièce piratée n'a pu être inclinée ; `under your control` → le joueur qui révèle ; le boost est ÉTOILE, donc aucune valeur dans `desc`. Résultat : conforme.
- [x] Étape 6 : aucun nombre hors les icônes. Résultat : conforme (`desc` sans `Boost`, vérifié contre `01144a`).
- [x] Étape 7 : repli sans Rogue Asset (la manigance entre en jeu) + branche principale avec Rogue Asset (les quatre pièces s'inclinent). Rouges sans module. Résultat : 2/2.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI, une manigance ENTRE EN JEU. Mesuré par `en_jeu`.
Carte terminée : OUI.

### st018 : Viral Assault
- [x] Étape 2 : `st017` (même recherche), `al007` / `ag004` (`MayChooseOneAbility` pour un « You may »), helper `ThisCardGainSurge`.
- [x] Étape 5 : TROIS branches, et la troisième ne s'ouvre QUE sans amélioration HACKED ; `for each` se lit après le refus ; `gains surge` s'ajoute à une traîtrise déjà en cours. Résultat : conforme.
- [x] Étape 6 : 1 dégât par amélioration piratée, 3 icônes de boost (relevées à l'image). Résultat : conforme.
- [x] Étape 7 : repli sans amélioration piratée, rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI (manigance en jeu), mesuré par `en_jeu`.
Carte terminée : OUI.

### st019 : Hostile Override
- [x] Étape 2 : `01077` / `50022` (`identite.attack`, valeur COURANTE), `aa005` / `dz037` (choix), `wd014` (Désorienté + boost étoile).
- [x] Étape 5 : `your ATK value` → l'identité du joueur qui révèle, zéro en forme civile ; `a friendly character` → identité OU allié ; le choix appartient au joueur ; boost ÉTOILE. Résultat : conforme.
- [x] Étape 6 : dégâts = ATQ, menace = CTR. Résultat : conforme (1 dégât pour une ATQ de 1).
- [x] Étape 7 : repli sans amélioration piratée + branche ATQ avec Rogue Asset. ⚠ Les quatre pièces sont détruites d'abord, sinon Ablative Protocol intercepte le dégât ; elles gardent le trait TECH et restent donc piratées. Rouges sans module. Résultat : 2/2.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI (statut Désorienté), chemin générique déjà couvert.
Carte terminée : OUI.

### st020 : Size Advantage *(extra, hors set du héros)*
- [x] Étape 2 : `04044` Piercing Strike, `dt005` (`health` = PV RESTANTS).
- [x] Étape 5 : `or` → une seule condition suffit ; `more remaining hit points than that enemy` → strictement plus, sur les PV restants des deux côtés ; la comparaison se fait avant les dégâts. Résultat : conforme.
- [x] Étape 6 : 3 ou 6 dégâts, coût 2. Résultat : conforme (6, grâce à GIANT).
- [x] Étape 7 : cas nominal, rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.
- [x] Homonyme : RESKIN de `62034`, même texte mais AGRESSIVITÉ au lieu de Justice, et SANS le trait ATTACK imprimé — elle échappe donc au malus d'Arms détruite, et c'est l'image qui tranche.
  ⚠ Correction du 03/10/2026 : `62034` est AUSSI en Agressivité (scan `assets/pics/62034.jpg` et marvelcdb). Le « Justice » venait d'une erreur de `data/cards.json`, corrigée ce jour. Seule différence restante : le trait ATTACK.
Carte terminée : OUI.

### st021 : Reboot *(extra, hors set du héros)*
- [x] Étape 2 : `09009` (`ReadyAll`), `03007` (`HealthUnits`).
- [x] Étape 5 : `Action` nue, pas « Hero Action » → jouable aussi en alter-ego, donc pas de `SetLabel` ; PAS de filtre `canbe_ready`, la carte fait DEUX choses et soigner un personnage déjà redressé reste légal ; `friendly ANDROID character` → identités ET alliés, d'où `Friend`. Résultat : conforme.
- [x] Étape 6 : 1 dégât soigné. Résultat : conforme (2 → 1, et le héros redressé).
- [x] Étape 7 : cas nominal, rouge sans module. Résultat : 1/1.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.
- [x] Homonyme : RESKIN exact de `26024` (Basic, même coût, même texte). Précédent assumé : `hc023`-`hc026` du pack hellcat.
Carte terminée : OUI.

### exposed : Exposed *(quatrième carte d'état, pack `status`)*
- [x] Étape 2 : `tough.py` / `stunned.py` / `confused.py` (gabarit d'une carte d'état), `bl007` Bandolier of Stakes (augmenter les dégâts d'une attaque EN COURS).
- [x] Étape 5 : `is ATTACKED` n'est pas « subit des dégâts » — une carte qui blesse sans attaquer ne consomme pas l'état ; `discard ALL` → les cartes partent toutes d'un coup et le bonus vaut le nombre défaussé ; chaque carte Exposé porte la capacité, d'où le garde-fou qui laisse la première tout emporter. Résultat : conforme.
- [x] Étape 6 : +1 dégât par carte défaussée. Résultat : conforme (ATQ 1 → 2 avec un Exposé).
- [x] Étape 7 : cas nominal (attaque : +1 dégât et l'état part) + contre-cas (dégâts hors attaque : l'état reste). Résultat : 2/2 dans le filtre `st0`, le nominal rouge sans le module du pack `status`.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI, c'est une CARTE POSÉE sur un personnage. Scan installé (`assets/textures/exposed.webp`), pastille « E » et badge « Exposé » ajoutés avec leurs tests, vus rouges avant l'ajout.
Carte terminée : OUI.

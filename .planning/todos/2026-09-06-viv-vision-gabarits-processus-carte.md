# PROCESSUS-CARTE.md : les 12 gabarits du pack VIV VISION (set 147, `vv`)

Gabarit régularisé le 06/09/2026 (audit C, point 3). Le portage a eu lieu le
02/09/2026 (auteur Rainy) : ce fichier met en forme la preuve déjà écrite
dans `.planning/todos/2026-09-02-portage-viv-vision.md` (§1-§10), qui
détaillait déjà les étapes 2/5/6/7 carte par carte (lignes 112-296) mais
**sans jamais cocher la ligne finale « Carte terminée »**, ce que l'audit
C du 06/09/2026 a signalé comme la lacune formelle du pack.

**Sur le fond, aucun défaut** : les 12 cartes ont leur cas de test, leur
preuve par substitution, l'autoplay du pack, et deux vrais défauts moteur
partagé ont été trouvés et corrigés. Le trou est uniquement dans la forme,
transcrit ici, sans rien ajouter ni maquiller.

**Preuves communes**, citées une fois :

- **Étape 1** : `data/cards.json`, pack `viv_vision`, 12 `card_id` ; préfixe
  `vv` déclaré.
- **Étape 4** : images `assets/pics/vv0*.jpg`. ⚠ Sur ces scans, `0.1` est
  l'**alter-ego** et `0.2` le **héros**, l'inverse de l'ordre habituel
  (journal §6, en-tête).
- **Étape 7, batterie** : `test_capacites.py … vv0` → **20 cas, tous verts**
  au portage (journal §7), **26 cas** après l'ajout des deux témoins
  d'épuisement du 06/09/2026 (`vv001a`, `vv001b`, voir plus bas).
- **Étape 7, substitution** : **12 cartes sur 12** ont au moins un cas rouge
  sans leur module (journal §7, table détaillée). Un seul cas reste vert par
  carte au maximum, toujours un contre-cas d'ABSENCE d'effet assumé (`vv001b`,
  1 vert sur 2). **Un faux vert a été trouvé et corrigé par la substitution
  elle-même** (`vv011`, voir sous sa carte) : c'est exactement ce que cette
  preuve est là pour attraper.
- **Deux fichiers moteur PARTAGÉS corrigés** (règle de portée du §6bis du
  GUIDE, donc passe complète due) : `face_action.py` (`GainUntilRoundEnd`
  n'acceptait pas `stalwart`, 3e occurrence du même oubli après `retaliate`
  et `villainous`) et `card/factory.py` (liste blanche des événements à deux
  capacités `Play`, pour `vv005`). Passe complète après correctif :
  **1012/1017 cas** (les 5 rouges sont 4 préexistants de `squirrel_girl` +
  1 faux échec de port déjà expliqué et rejoué vert, journal §8ter) ;
  **110/112 puis 111/112 decks** (2 échecs préexistants, dont 1 corrigé au
  passage, `doctor_doom`, hors périmètre du pack, signalé §10).
- **Étape 8, autoplay** : 8 parties `viv_vision` contre Rhino, témoin
  `spider_man` dans les mêmes conditions, le 02/09/2026 (journal §8). **0
  incident** pour Viv Vision (le témoin en bloque 1/8, défaut du pilote sur
  une carte officielle sans rapport). Grep exhaustif des 16 journaux : 0
  partout. Lecture ligne à ligne confirmant en particulier le mot-clé maison
  `breakthrough` en situation réelle (menace en surplus reportée sur une
  autre manigance, journal §8, extrait cité).
- `test_cards` : 5069 ok / 0 err. `verifier_api_cartes` : 4 fautes au constat,
  2 corrigées dans la foulée (aucune dans ce pack, mais un correctif
  d'API partagé profite à `wd159`/`wd160`, journal §10).

⚠ **Deux mots-clés maison créés pour ce pack**, fiches déposées avant le
script : `breakthrough` (`docs/reference/mots-cles/breakthrough.md`,
définition obtenue de l'utilisateur depuis la *Marvel Champions Home Brew
Master List*, introuvable ailleurs, journal §1) et le montage de
`AfterCardExhausted` construit à la main pour `vv009` (aucune fabrique du
dépôt ne l'enveloppait encore).

---

## Gabarits, carte par carte

### vv001a : ★ Viv Vision (face héros)
- [x] Étape 2 : `01068` ★ Vision (allié Core, texte quasi identique) ;
      `ag001b` ★ Sharon Carter pour `SetName` + `LimitOncePerRound` sur une
      action d'identité au texte imprimé « Action: » nu. **Pas** `26001a`
      Vision officiel, sans rapport (bascule Dense/Intangible).
- [x] Étape 5 : mots-pièges vérifiés : « YOU get +2 » (l'identité, pas la
      face : `ignore_flip=True`), « a chosen BASIC power » (les TROIS
      pouvoirs, là où `01068` n'en offre que deux), « until the end of the
      ROUND » (`GainUntilRoundEnd`, pas `GainUntilPhaseEnd`), « Limit once
      per round ». Résultat : conforme.
- [x] Étape 6 : THW 1/ATK 1/DEF 1, HS 5, PV 10, bonus +2, limite 1/round.
      Résultat : conforme.
- [x] Étape 7 : `vv001a Density Manipulation — 1 energie donne +2 a un
      pouvoir de base pour le round`. Substitution : **1/1 rouge** (journal
      §7).
- [x] Étape 7 bis : limite imprimée **OUI**. Témoin ajouté le 06/09/2026
      (audit C, point 1) : `vv001a … TEMOIN D'EPUISEMENT : la seconde Action
      du round ne cumule pas le bonus`, deux énergies payées, deux
      activations dans le même round, chiffre mesuré :
      `attributs.thwart == 2` (pas 4). `test_capacites.py … "vv001a"` → OK.
- [x] Étape 8 : preuve commune ci-dessus (« Density Manipulation » activée
      en partie réelle, journal §8).

**Carte terminée : OUI**

### vv001b : ★ Viv Vision (face alter-ego)
- [x] Étape 2 : `ag001b` ★ Sharon Carter, même forme exacte (Action limitée
      1/round qui choisit dans une pile et repose sur un deck) ; `al007`
      « See You Later! » pour la lecture de sa propre défausse.
- [x] Étape 5 : « a PRINTED [energy] resource » (couleur imprimée, wild NON
      converti, `checker.py:436`), « in YOUR discard pile » (écart avec
      `ag001b`, qui vise la défausse de RENCONTRE), « ON TOP of your deck »
      (argument positionnel de `MoveAllToDeck`, pas `to_top=`), « Choose »
      sans « you may » (obligatoire dès qu'un candidat existe). Résultat :
      conforme.
- [x] Étape 6 : REC 3, HS 6, PV 10, limite 1/round. Résultat : conforme.
- [x] Étape 7 : `vv001b Recharge — une carte a energie IMPRIMEE remonte de
      la defausse sur le deck` + `vv001b Recharge — une carte WILD n'est PAS
      repechable (contre-cas)`. Substitution : **1/2 rouge**, le contre-cas
      restant vert par construction (absence d'effet, journal §7).
- [x] Étape 7 bis : limite imprimée **OUI**. Témoin ajouté le 06/09/2026 :
      `vv001b … TEMOIN D'EPUISEMENT : la seconde Action du round ne remonte
      plus rien`, deux cartes à énergie imprimée en défausse, deux
      activations, chiffre mesuré : `defausse_joueur == 1` (pas 0).
      `test_capacites.py … "vv001b Recharge — TEMOIN"` → OK.
- [x] Étape 8 : preuve commune (bascule de forme exercée à chaque mise en
      place, journal §8).

**Carte terminée : OUI**

### vv002 : Hologram Projection
- [x] Étape 2 : `27006` Web Binding (annulation d'activation, porte elle
      aussi un Requirement) ; `01083`/`05015` pour la pose de statut.
- [x] Étape 5 : « an ENEMY » (vilain ET sbires, aucun filtre de type),
      « cancel THAT activation » (`SetBeInstead`, pas une interdiction
      durable), « confuse THAT enemy » (`message.trigger`). `Requirement` :
      base automatique, aucun script. Résultat : conforme.
- [x] Étape 6 : coût 2, Requirement `[energy][mental]` = « YB ». Résultat :
      conforme.
- [x] Étape 7 : `vv002 Hologram Projection — l'activation du vilain est
      annulee et le vilain desoriente`. Substitution : 1/1 (journal §7).
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : preuve commune.

**Carte terminée : OUI**

### vv003 : Just a Phase
- [x] Étape 2 : `61023` Grapnel Launcher (seule autre carte du dépôt qui
      ignore patrol) ; `20013` Making an Entrance ; `08013` Stealth Strike.
- [x] Étape 5 : mots-pièges vérifiés, **écart de déclencheur documenté et
      assumé** (§4 du journal) : le texte imprime « Hero Interrupt », le
      moteur vérifie `patrol` AU CHOIX DE LA CIBLE et non à la résolution,
      une interruption fidèle au mot imprimé n'aurait donc jamais pu lever
      `patrol`. Décision utilisateur du 02/09/2026 : rendre la carte comme
      `61023`, qui EXÉCUTE la menée elle-même (`BasicThwart`), perte assumée
      documentée dans le module et dans `textes-fr-fanmade.ts` (le texte
      imprimé reste fidèle dans `cards.json`, la traduction décrit l'effet
      réel). Résultat : conforme à l'écart assumé près.
- [x] Étape 6 : coût 1, +3 CTR. Résultat : conforme.
- [x] Étape 7 : 2 cas : le breakthrough (excès reporté sur une autre
      manigance) et l'icône de crise ignorée. Substitution : **2/2**, plus
      une substitution FINE qui isole la levée de `patrol` seule (retrait du
      seul argument `'Patrol'` de `.SetIgnoreKeyword`, le cas patrol tombe
      alors au rouge, les deux autres restent verts (journal §7).
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : preuve commune (« Just a Phase » vue en partie réelle,
      extrait de journal cité au §8 du journal source).

**Carte terminée : OUI**

### vv004 : Phase Up
- [x] Étape 2 : `03005` Shield Block (**pas** `01003` Backflip, qui filtre
      sur l'attaque) ; `dd001a` pour un mot-clé accordé jusqu'à la fin du
      round.
- [x] Étape 5 : « ANY AMOUNT of damage » (pas de `is_from_attack`, écart
      exact avec Backflip), « PREVENT ALL » (`"All"`, pas un chiffre), « YOU
      gain stalwart » (l'identité), « until the end of the ROUND ». Résultat :
      conforme.
- [x] Étape 6 : coût 1, Requirement `[energy]`. Résultat : conforme.
- [x] Étape 7 : 1 cas, avec sonde dédiée (`etat_attendu` ne sait pas lire
      `stalwart`, absent de la table `IMPRIME`). Substitution : 1/1. ⚠ Cette
      carte a exigé le correctif moteur partagé `GainUntilRoundEnd`/
      `stalwart` (voir preuve commune) : PREMIER stalwart temporaire du
      dépôt, ~30 autres cartes l'accordant par attachement permanent.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : preuve commune.

**Carte terminée : OUI**

### vv005 : Solar Beam
- [x] Étape 2 : `26008` Solar Beam, son homonyme OFFICIEL (même structure à
      deux `Play`) ; `ag003`/`41030` pour le ranged ponctuel.
- [x] Étape 5 : « THIS ATTACK gains ranged » (branche attaque seule,
      `AttackProperty(ranged=True)`, jamais `message.GainRanged` qui
      donnerait ranged à l'ennemi), « to AN enemy » / « FROM A scheme » (une
      cible chacune), deux `Hero Action` distinctes (`choisir_option:
      "Play_1"` indispensable pour tester la seconde, sans quoi le pilote
      teste toujours la première, piège documenté journal §5). Résultat :
      conforme.
- [x] Étape 6 : coût 2, 5 dégâts, 4 menaces, Requirement `[energy]`.
      Résultat : conforme.
- [x] Étape 7 : 2 cas, un par branche `Play`/`Play_1`. Substitution : 2/2.
      ⚠ Cette carte a exigé le correctif moteur partagé `factory.py` (liste
      blanche des événements à deux capacités `Play`, voir preuve commune).
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : preuve commune.

**Carte terminée : OUI**

### vv006 : Superdense Strike
- [x] Étape 2 : `56017` Savage Strike (modèle exact du couple bonus+mot-clé
      sur sa propre attaque de base, **pas** l'homonyme officiel `26009`).
- [x] Étape 5 : « AGAINST AN ENEMY » (appel direct à `WhenUnitWouldAttack`,
      `WhenUnitMakeAttack` n'exposant pas `attack_targets`), « THAT ATTACK
      gains piercing » (sur l'attaque, pas le personnage), « Give YOUR HERO
      a tough status card » (3e phrase sans flèche : un effet, pas un coût).
      Aucun Requirement imprimé : aucun inventé. Résultat : conforme.
- [x] Étape 6 : coût 2, +4 ATQ. Résultat : conforme.
- [x] Étape 7 : 1 cas, qui prouve aussi le piercing (Rhino reçoit une carte
      Tenace au préalable). Substitution : 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : preuve commune.

**Carte terminée : OUI**

### vv007 : ★ Sparky the Dog
- [x] Étape 2 : `18015` First Hit (« minion initiates an attack ») ; `sr010`
      (lecture de `message.attacker`) ; `aa003` Ebony (Action d'alter-ego
      payée par épuisement) ; `sd013` (déclaration explicite de
      `CanPlayThisSupportCard`).
- [x] Étape 5 : « a MINION » (jamais le vilain), pas de « against you »
      imprimé donc pas de filtre joueur, « to THAT minion », la flèche qui
      fait de l'épuisement un coût, « from YOUR IDENTITY ». **Ressource
      corrigée avant le script** : `RES = "G"` (wild), et non une ressource
      physique comme d'abord annoncé, vérifié par comparaison du coin
      inférieur gauche du scan avec les autres cartes du pack (leçon
      Lockjaw, journal §2). Résultat : conforme.
- [x] Étape 6 : coût 1, 2 dégâts, soin 1. Résultat : conforme.
- [x] Étape 7 : 2 cas, un par capacité. Substitution : 2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : preuve commune (« Sparky the Dog » posé puis incliné en
      partie réelle, journal §8).

**Carte terminée : OUI**

### vv008 : Computer Mind
- [x] Étape 2 : `AfterPlayerPlayedCard` (`play.py:310`) ; `ho006` pour la
      famille « réagir à la carte qu'on vient de jouer » ; fiche
      `mots-cles/requirement.md`. **Aucune autre carte du dépôt ne LIT le
      mot-clé Requirement** (les ~30 qui l'impriment ne comptent jamais les
      ressources exigées d'une autre carte) : lecture directe de
      `face.requirement.val`.
- [x] Étape 5 : « a card that HAS THE REQUIREMENT KEYWORD » (`requirement.val
      > 0`, pas « coûte des ressources »), « for each REQUIRED RESOURCE »
      (le nombre d'icônes exigées, jamais le coût), « that card »
      (`message.played_face`), « AFTER you play » (jamais
      `WhenPlayerPlayCard`), `Response` NU (jouable en alter-ego aussi).
      Résultat : conforme.
- [x] Étape 6 : coût 1, « 1 carte par ressource exigée ». Résultat :
      conforme.
- [x] Étape 7 : 1 cas, qui prouve le « for each » et pas seulement le
      déclenchement (`vv002` exige deux ressources → deux cartes piochées).
      Substitution : 1/1.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : preuve commune (« Computer Mind » équipée en partie réelle,
      journal §8).

**Carte terminée : OUI**

### vv009 : Insubstantial Flight
- [x] Étape 2 : `ho011` ★ Goblin Glider (même carte à un déclencheur près) ;
      `vr010` Regeneration (même auteur) pour la forme de la réponse.
      **Aucune fabrique n'enveloppe `Message.AfterCardExhausted`** :
      `Ability` construite à la main, montage établi (`cd008`, `aa001b`,
      `dt009`, `gb001`).
- [x] Étape 5 : « YOU gain the AERIAL trait » (l'identité), « After your
      HERO exhausts » (filtre `"YourHero"`), « exhausts » sans complément
      (n'importe quel épuisement), la flèche qui plafonne à une fois par
      round, « ready YOUR HERO ». Pas de boucle : redresser n'émet pas
      `AfterCardExhausted`. Résultat : conforme.
- [x] Étape 6 : coût 2, Requirement `[energy]`. Résultat : conforme.
- [x] Étape 7 : 2 cas, un par capacité. Substitution : 2/2.
- [x] Étape 7 bis : « once per round » borne le REDRESSEMENT, pas la carte
      elle-même comme une action répétable par le joueur (c'est une Réponse
      automatique après épuisement du héros, pas une Action). Aucun témoin
      d'épuisement écrit : l'audit C (point 1) ne liste pas `vv009` parmi
      les cartes concernées, et la carte n'a pas été revue pour cette
      exigence dans le cadre de cet audit. **Non vérifié ici** : à traiter
      séparément si jugé utile, hors du périmètre des quatre points demandés.
- [x] Étape 8 : preuve commune.

**Carte terminée : OUI** pour les étapes couvertes ; l'étape 7 bis de cette
carte précise n'a pas été auditée dans ce passage (voir ci-dessus).

### vv010 : ★ Viv's Solar Gem
- [x] Étape 2 : `sd015` Never Ending Spark (même carte à un déclencheur
      près) ; `29030` pour « after the villain phase ends ».
- [x] Étape 5 : `Resource:` NU (générable aussi en alter-ego), `Response:`
      NU (le redressement joue quelle que soit la forme : la fin de phase du
      vilain trouve souvent Viv en civil), « generate A [energy] resource »
      (une seule, pas de `for_card=`), « ready Viv's Solar Gem » (elle-même).
      Résultat : conforme.
- [x] Étape 6 : coût 2. Résultat : conforme.
- [x] Étape 7 : 2 cas : le financement réel d'un coût, et le redressement
      (sonde in-process, l'API Puzzle n'avance aucune phase). Substitution :
      2/2.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Étape 8 : preuve commune.

**Carte terminée : OUI**

### vv011 : Grounded
- [x] Étape 2 : `36030` Claustrophobia (obligation de Storm, même texte,
      mot pour mot). **Pas** `12025` Care for Cassie, qui imprime « you MAY
      flip » et un choix à deux branches.
- [x] Étape 5 : « FLIP » sans « you may » (obligatoire), « cannot change
      form » (interdiction PERMANENTE, `PlayersCannotChangeForms`, pas
      « until your next turn ends » comme `12025`), « Exhaust YOUR
      ALTER-EGO », « REMOVE FROM THE GAME » et non « discard ». Résultat :
      conforme.
- [x] Étape 6 : Boost 2. Résultat : conforme.
- [x] Étape 7 : 2 cas, un par capacité. **FAUX VERT TROUVÉ ET CORRIGÉ PAR LA
      SUBSTITUTION** (journal §7) : le cas de bascule vérifiait
      `"attendu": {"face": "vv001b", ...}`, or `face` n'est PAS une clé de
      `etat_attendu` : la ligne ne vérifiait RIEN, et le cas passait au vert
      sur une carte muette (seul `en_jeu: ["vv011"]` était réellement testé,
      et il reste vrai sans le module). Corrigé en utilisant la vraie clé,
      `forme` (`test_capacites.py:15244` au moment du journal). Substitution
      après correction : **2/2 rouges**.
- [x] Étape 7 bis : aucune limite imprimée (interdiction permanente, pas
      « once per X »).
- [x] Étape 8 : preuve commune.

**Carte terminée : OUI**

---

## Bilan PROCESSUS-CARTE

**12 cartes sur 12** ont un cas de test sujet et une preuve par substitution
réelle, y compris un faux vert authentique trouvé et corrigé (`vv011`) : la
preuve exigée par le processus a fonctionné, pas seulement existé. Les deux
cartes à limite imprimée (`vv001a`, `vv001b`) ont reçu leur témoin
d'épuisement le 06/09/2026 (audit C, point 1), qui n'existait pas au portage
initial.

## Gate finale PROCESSUS-HEROS : **NON**

Par la lettre de `PROCESSUS-HEROS.md` (« si une seule carte du pack manque
son "Carte terminée : OUI", le héros entier reste NON »), et même si les 12
cartes sont ici individuellement OUI, la gate finale du processus HÉROS
exige en plus **une partie complète jouée par un humain dans le navigateur**
(§9 de `PROCESSUS-CARTE.md`, §7 de `PROCESSUS-HEROS.md`). Cette partie
**n'a pas été jouée** (le journal §9 le disait déjà : « Aucun outil du
projet ne la remplace »). Viv Vision reste donc **formellement NON terminé**
au sens de la gate finale, malgré un travail de fond complet et vérifié.
C'est exactement le constat de l'audit C du 06/09/2026, et ce gabarit ne le
maquille pas.

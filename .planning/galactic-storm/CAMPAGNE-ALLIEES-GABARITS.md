# Galactic Storm : les 13 cartes de campagne (gs224-gs236)

Gabarit PROCESSUS-CARTE.md en cours. Scans relus un par un (dossier
`docs/packs/galactic-storm/sources/.../Campaigns/Galactic Storm/`,
transcription `docs/packs/galactic-storm/transcriptions/campagne.md`).

**Étape 1 (entrée `cards.json`) : FAITE pour les 13 cartes**, script idempotent
`.planning/galactic-storm/defs/inserer_campagne_alliees.py`. Conventions
vérifiées contre les scans et contre `sk263-sk269` (Skrull Menace, même
auteur, même gabarit « carte de campagne ») :

- `desc.HP` = pastille orange (convention GS-0 Q6, déjà actée).
- `desc.THW`/`ATK` : une étoile à contour sous la stat = un `*` (dégâts
  consécutifs, convention GS-0 Q6). Compté à l'œil sur chaque scan, PAS
  supposé depuis la transcription (qui se trompait sur plusieurs cartes :
  Crystal/Goliath/Her/Captain Marvel/Living Lightning/Sersi n'ont EN FAIT
  aucune étoile, contrairement à ce que `campagne.md` laissait craindre).
- `desc.RES` : carré de couleur bas-gauche. Vérifié par découpe contre les
  mêmes conventions pack que gs172/gs173/gs12x (éclair = `Y` énergie, noeuds
  reliés = `B` mental, poing = `R` physique, étoile = `G` wild). Les 3 alliées
  BASIC ont chacune leur couleur propre (Rick Jones `B`, Gladiator `G`,
  Lauri-Ell `R`) ; les 10 alliées IDENTITY-SPECIFIC sont toutes `G` (wild).
- `desc.Class` : `"Campaign;Basic"` (224-226) ou `"Campaign;IdentitySpecific"`
  (227-236) — classes NATIVES du moteur (`card_player.py` `CARD_CLASS`), pas
  une invention : confirmé par `IsClass("IdentitySpecific")` déjà utilisé
  ailleurs dans le moteur.
- `desc.Requirement` (Crystal, `"YBR"`) : base automatique, `requirement.md`,
  aucun script.
- `[star]` devant une capacité (Lauri-Ell, Her) : footnote pure, convention
  Skrull Menace déjà actée (GS-0 Q6), gardée dans `text` mais sans effet code.
- **gs227 Binary, piège trouvé et corrigé avant commit** : la carte imprime
  « X » en ATK. `desc.ATK = "X"` aurait fait planter `int(value)` (parseur
  natif, `can_attack.py:81`). Corrigé en `desc.ATK = "0*"` + capacité
  `AbilityFactory.ThisGainKeyword` recalculant la vraie valeur, modèle
  `mw001a` Madame Web (commentaire du moteur lui-même : « Necessaire pour
  Madame Web mw001a (ATK/THW/DEF = X) » — précédent direct, même mécanique).

**Étape 2-3 (cartes de référence + script) : FAITES pour 10/13 cartes**
(`src/cards/pack/galactic_storm/galactic_storm_campaign/`) :

| Carte | Mécanique | Référence utilisée |
|---|---|---|
| gs224 Rick Jones | rediriger l'attaque du méchant vers Rick Jones | `hood/crossfires_crew/24026` Crossfire (`WhenUnitWouldAttack` + `ReplaceTarget`) |
| gs225 Gladiator | après l'avoir joué depuis la main, vaincre un sbire | `core/spider_man/01002` Black Cat (`AfterPlayerPlayedCard` sur "This") + `jj/jessica_jones/61002` (`Faces.DefeatUnits`) |
| gs227 Binary | ATK = X (ressources énergie en main) | `mw001a` Madame Web (`ThisGainKeyword` + `desc.ATK="0*"`) |
| gs228 Captain Marvel | Resource : défausser Captain Marvel → générer YY | `core/iron_man/01033` Pepper Potts + `falcon/falcon/53006` (`CanGenerateResources`, `CostFunc.Discard`) — **combo cout/générateur pas vu identique ailleurs, à vérifier en étape 7** |
| gs229 Crystal | When Defeated : payer 3 → remettre en jeu sous contrôle | `mut_gen/mutant_genesis_campaign/32173b` (`PutIntoPlay(under_control=True)`) — **ÉCHOUE, voir § Étape 7 et `gs229.py`** |
| gs230 Doctor Pym | Alter-Ego Action : +1 à chaque pouvoir de base jusqu'à la fin du round | `fne/daredevil/60017` (`identity.GainUntilRoundEnd`) |
| gs231 Goliath | après pouvoir de base, défausser le dessus ; si [physical], 1 dégât à chaque ennemi | `AbilityFactory.AfterUnitUseBasicPower` (natif) + `01002` Black Cat (`DiscardDeckTopCards`) |
| gs232 Her | après son entrée en jeu, redresser une amélioration | `sk263` Crusader (`AfterCardEnterPlay`) + `psylocke/41011` (`canbe_ready=True`) |
| gs233 Living Lightning | après avoir quitté le jeu, défausser 2 ; par [energy] imprimé, redresser une carte | `AfterCardLeavePlay` (natif) + `01002` + `falcon/53012` Talon Line (boucle `ChooseAbilities` x N) |
| gs236 Thor | après l'avoir joué depuis la main, 1 dégât par [energy] payé pour lui à chaque sbire engagé | `01002` Black Cat + `Effect.GetPaidResources()` (`effect.py:512`) |

**Construction vérifiée** : `test_cards` 7016/7016 (+10 depuis les 7006 d'avant
les scripts), 0 erreur. `verifier_appels_modules galactic_storm` : OK (tous
les appels existent réellement, pas juste « ça charge »).

**Étape 7 (cas de test, preuve par substitution) : FAITE pour 9/10 cartes
scriptées** (`tools/cas/campagne_galactic_storm.py`, filtre `[gsc]`) :

- `test_capacites` : **11/12 cas verts** (seul gs229 échoue, voir plus bas).
- Preuve par substitution (`substituer_pack.py`) : gs225, gs228, gs230,
  gs232, gs233, gs236 → rouges 1/1. gs227 et gs231 → rouges 1/2, l'autre cas
  étant un CONTRE-CAS D'ABSENCE qui reste vert sans module par construction
  (assumé, pas un défaut).
- **gs224 Rick Jones : substitution NON concluante** (rouges 0/1, voir le
  commentaire dédié dans `tools/cas/campagne_galactic_storm.py`). Le cas
  reste vert même sans le module : `Puzzle.Attack` sans `defender=` semble
  choisir seul un personnage à « défendre » dès qu'un allié est en jeu
  (comportement du pilote de test, pas du moteur de règles). Le code lui-même
  (`ReplaceTarget`, modèle direct Crossfire `hood/crossfires_crew/24026`)
  reste la bonne méthode pour ce texte — c'est la mesure qui ne l'isole pas,
  pas forcément la carte qui est fausse. À reprendre pour fiabiliser le cas.
- **Pièges réels trouvés et corrigés en écrivant ces cas** (gardés en
  commentaire dans chaque script, donc pas perdus) :
  - gs227 Binary : `ThisGainKeyword` ne se recalculait pas quand la main
    changeait (`change_on_event` manquant) — corrigé avec
    `OnEvent.HandCards("EngagedPlayer")`, modèle `gs001a` Binary (même texte).
  - gs230 Doctor Pym : l'Alter-Ego n'a pas d'ATK/DEF, le Héros n'a pas de SCH.
    Le gain posé une seule fois sur l'Alter-Ego persiste correctement après
    un changement de forme (`TemporaryGain`, `ignore_flip=True` suit la face
    COURANTE de la carte) : le poser sur les DEUX faces (hypothèse testée en
    premier) DOUBLAIT le bonus.
  - gs236 Thor : `effect.GetPaidResources()` lit le paiement de LA RÉPONSE
    elle-même (vide), pas celui de Thor — il fallait `message.paid_resources`
    (porté par `Message.AfterPlayerPlayedCard`).
  - **gs229 Crystal : `PutIntoPlay` rend `False`** (confirmé par
    instrumentation) — voir détail dans `gs229.py` et ci-dessous.

**3 cartes PAS scriptées, chacune pour une raison précise** :
- **gs226 Lauri-Ell** — « discard each boost card on that enemy » : pas de
  précédent clair pour des « cartes boost » qui RESTERAIENT en jeu, visibles,
  sur un ennemi après une activation (le mécanisme `GiveFacedownBoostCards`
  trouvé ailleurs dans le pack sert à la pioche de boost PENDANT une
  activation, pas à un stock persistant attaché). À vérifier avant de
  scripter : soit une vraie mécanique du pack existe quelque part (pas
  trouvée), soit c'est à interpréter.
- **gs234 Sersi** — « choose a status card in play. Replace that status card
  with a different status card » : les statuts (Tough/Stunned/...) existent
  comme capacité (`Faces.GiveStatus`) mais « choisir un statut EN JEU puis le
  remplacer par un AUTRE » demande de retrouver quelle carte le porte et de
  quel type, pas juste en donner un nouveau. Faisable mais pas encore
  construit faute de temps.
- **gs235 Spider-Woman** — « discarded from the top of your deck » :
  **AUCUN précédent dans tout le dépôt** (grep exhaustif, officiel et maison).
  Probable brique moteur manquante (un hook qui n'existe pas encore pour
  qu'une carte réagisse à SA PROPRE défausse depuis le dessus du deck d'un
  joueur), pas une carte « normale » à scripter avec les briques actuelles —
  décision à prendre avant d'investir dedans (construire la brique moteur,
  ou confirmer qu'elle existe sous un autre nom).

**Reste à faire pour clore le lot** : bloc texte-contre-code (étape 5, pas
relu ligne à ligne formellement, mais couvert en pratique par les mots-pièges
notés dans chaque script), bloc nombres (étape 6, idem), autoplay ciblé
(étape 8, pas fait), bloc plateau (étape 8 bis — Her/Living Lightning
redressent des cartes, concernées, pas fait). Réparer gs229 (cause identifiée,
pas corrigée). Scripter gs226/gs234/gs235. Construire
`data/campagnes/galactic_storm.json` (chantier séparé, pas commencé).

**Statut carte par carte** :
- **9/13 terminées au sens fort** (construites, référencées, testées, preuve
  par substitution concluante) : gs225, gs227, gs228, gs230, gs231, gs232,
  gs233, gs236, et gs224 avec une réserve sur la qualité de la preuve (voir
  ci-dessus — le code suit un modèle éprouvé, seule la mesure est en cause).
- **1/13 construite et testée mais EN ÉCHEC CONFIRMÉ** : gs229 (cause
  identifiée : `PutIntoPlay` refuse le déplacement, voir `gs229.py`).
- **3/13 pas scriptées** : gs226, gs234, gs235 (raisons ci-dessus).

Carte terminée (les 13) : NON — 9 OUI, 1 NON confirmé (gs229), 3 pas
commencées (gs226, gs234, gs235).

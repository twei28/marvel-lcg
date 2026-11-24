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

**Étape 2-3 (cartes de référence + script) : FAITES pour les 13 cartes**
(`src/cards/pack/galactic_storm/galactic_storm_campaign/`) :

| Carte | Mécanique | Référence utilisée |
|---|---|---|
| gs224 Rick Jones | rediriger l'attaque du méchant vers Rick Jones | `hood/crossfires_crew/24026` Crossfire (`WhenUnitWouldAttack` + `ReplaceTarget`) |
| gs225 Gladiator | après l'avoir joué depuis la main, vaincre un sbire | `core/spider_man/01002` Black Cat (`AfterPlayerPlayedCard` sur "This") + `jj/jessica_jones/61002` (`Faces.DefeatUnits`) |
| gs226 Lauri-Ell | après avoir attaqué et blessé, défausser les boosts de la cible | `fne/kingpin/60165` James Wesley (`CanBoost`/`components.boostable.GetDeck()`) + `galactic_storm` gs176 Destroyer (`AfterUnitAttackUnit`) |
| gs227 Binary | ATK = X (ressources énergie en main) | `mw001a` Madame Web (`ThisGainKeyword` + `desc.ATK="0*"`) + `galactic_storm/binary/gs001a` (`OnEvent.HandCards`) |
| gs228 Captain Marvel | Resource : défausser Captain Marvel → générer YY | `core/iron_man/01033` Pepper Potts + `falcon/falcon/53006` (`CanGenerateResources`, `CostFunc.Discard`) |
| gs229 Crystal | When Defeated : payer 3 → remettre en jeu sous contrôle | `mut_gen/mutant_genesis_campaign/32173b` (`PutIntoPlay`) + `RegisterTemp` différé sur `AfterUnitBeDefeated` (voir piège ci-dessous) |
| gs230 Doctor Pym | Alter-Ego Action : +1 à chaque pouvoir de base jusqu'à la fin du round | `fne/daredevil/60017` (`identity.GainUntilRoundEnd`) |
| gs231 Goliath | après pouvoir de base, défausser le dessus ; si [physical], 1 dégât à chaque ennemi | `AbilityFactory.AfterUnitUseBasicPower` (natif) + `01002` Black Cat (`DiscardDeckTopCards`) |
| gs232 Her | après son entrée en jeu, redresser une amélioration | `sk263` Crusader (`AfterCardEnterPlay`) + `psylocke/41011` (`canbe_ready=True`) |
| gs233 Living Lightning | après avoir quitté le jeu, défausser 2 ; par [energy] imprimé, redresser une carte | `AfterCardLeavePlay` (natif) + `01002` + `falcon/53012` Talon Line (boucle `ChooseAbilities` x N) |
| gs234 Sersi | Action : remplacer un statut en jeu par un autre | `core/she_hulk/01027` (`CostFunc.TakeDamage`) + `card_finder has_status="Any"` + `component/status.py` (`DiscardStatusCard`/`GainStatus`) |
| gs235 Spider-Woman | après avoir été défaussée du dessus de son deck, étourdir jusqu'à 2 ennemis | `next_evol/domino/40043` Jackpot! (`AfterCardDiscardInternal(..., from_where="PlayerDeckTop")`) — **précédent en réalité déjà présent dans le dépôt**, trouvé en cherchant l'API (`from_where`) plutôt que le texte imprimé |
| gs236 Thor | après l'avoir joué depuis la main, 1 dégât par [energy] payé pour lui à chaque sbire engagé | `01002` Black Cat + `message.paid_resources` (`AfterPlayerPlayedCard`) |

**Construction vérifiée** : `test_cards` 7019/7019, 0 erreur.
`verifier_appels_modules galactic_storm` : OK.

**Étape 7 (cas de test, preuve par substitution) : FAITE pour les 13 cartes,
y compris gs224 et gs226 (résolu le 21/10/2026)**
(`tools/cas/campagne_galactic_storm.py`, filtre `[gsc]`) :

- `test_capacites` : **15/15 cas verts** (13 cartes, gs227 et gs231 ont
  chacune 2 cas).
- Preuve par substitution (`substituer_pack.py`) : **13/13 cartes → rouges
  1/1** (gs227 et gs231 → rouges 1/2, l'autre cas étant un CONTRE-CAS
  D'ABSENCE qui reste vert sans module par construction, assumé).
- **gs224 Rick Jones, résolu** : la substitution restait verte non pas à
  cause de la carte, mais d'un piège dans le TEXTE du cas lui-même —
  `questions_absentes=["Peter Parker est attaqué"]` ne matchait jamais,
  car le moteur rend le prompt avec un crochet fermant collé au nom :
  `"[(01,01001b) Peter Parker] est attaqué par..."`. Corrigé en
  `questions_absentes=["Peter Parker] est attaqué"]` → rouges 1/1.
- **gs226 Lauri-Ell, résolu** : deux pièges superposés.
  1. Une commande `Puzzle.GiveFacedownBoost(cible, carte)` a été ajoutée à
     `game/puzzle/puzzle.py` (modèle `fne/kingpin/60165` James Wesley,
     `components.boostable.GiveBoostCard`) pour pouvoir enfin seeder une
     pile de boost hors activation sur un ennemi — absente jusqu'ici.
  2. Avec cette commande, le cas restait quand même vert sans module : la
     clé `hors_jeu` (`par_id`/`IsInPlay`) est TOUJOURS vraie pour une carte
     posée FACE CACHÉE dans `components.boostable.GetDeck()` — AVANT même
     toute attaque, puisque `IsInPlay()` exige `IsFaceUp()`. Remplacé par un
     vérificateur `gsc_gs226_pile_boost_videe` qui mesure directement
     `cible.components.boostable.GetDeck().GetSize()` après l'attaque.
  3. **Un vrai bug de carte a été trouvé par ce chemin** : `gs226.py` lisait
     `message.damage_targets`, un attribut qui n'existe pas sur
     `Message.AfterUnitAttackUnit` (`AttributeError` en partie réelle, à
     chaque fois que Lauri-Ell blessait un ennemi). Corrigé en
     `message.took_damage_targets` (le vrai champ, confirmé dans
     `sender_damage.py`). → rouges 1/1.
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
  - **gs229 Crystal, piège le plus coûteux (résolu)** : `WhenUnitBeDefeated`
    fire AVANT que la carte quitte réellement le jeu (`card.area` est encore
    « en jeu » à ce moment), donc `PutIntoPlay` échouait silencieusement
    (déplacement vers la zone où la carte est déjà). `AfterUnitBeDefeated`
    posée en ability standard ne se déclenche JAMAIS pour la carte
    elle-même (capacités déjà désenregistrées). Solution : depuis
    `WhenUnitBeDefeated`, différer la remise en jeu via `effect.RegisterTemp`
    sur une ability temporaire liée à `AfterUnitBeDefeated`.
  - **gs235 Spider-Woman : fausse alerte de la session précédente** — un
    premier passage avait conclu « aucun précédent dans le dépôt » en
    cherchant le TEXTE imprimé (« discarded from the top of your deck »).
    L'API existe bel et bien (`from_where="PlayerDeckTop"`,
    `AbilityFactory.AfterCardDiscardInternal`), avec un précédent direct
    (`next_evol/domino/40043`). Leçon : chercher par API/mécanique, pas
    seulement par citation du texte imprimé, avant de conclure à une brique
    manquante.

**Reste à faire pour clore le lot à 100 %** : bloc texte-contre-code (étape
5, couvert en pratique par les mots-pièges notés dans chaque script mais pas
relu formellement ligne à ligne), bloc nombres (étape 6, idem), autoplay
ciblé (étape 8, pas fait), bloc plateau (étape 8 bis — Her/Living Lightning
redressent des cartes, concernées, pas fait).

**Statut final** : **13/13 cartes construites, scriptées, testées, 13/13
preuve par substitution pleinement concluante** (gs224/gs226 résolus le
21/10/2026, voir ci-dessus). Mode campagne proprement dit (`data/campagnes/
galactic_storm.json` + `src/cards/pack/galactic_storm/campaign.py`) :
construit séparément, voir `MODE-CAMPAGNE-GABARIT.md`.

---

## 7. La logique de campagne côté moteur : le carnet, `campaign.py`, `CampaignSetup`

C'est le chapitre le plus important pour qu'une campagne **soit réellement une campagne**. Une récompense qui
est notée au carnet mais que personne ne relit à la mise en place suivante **disparaît en silence** : c'est
arrivé à deux récompenses de Sinister Motives, à huit récompenses d'autres boîtes (audit du 19/09/2026) et à
l'allié « Captive » de Mutant Genesis (les quatre captifs se retrouvaient dans la main de départ).

### 7.1 Le carnet : le format exact

* Un **dictionnaire `str → str`**. Toutes les valeurs sont des **chaînes**.
* Une **case cochée** : `"1"`. Une **case non cochée** : la clé est **absente** (jamais `"0"` : le moteur teste
  `!= ''`, et `"0"` est non vide).
* Un **nombre** : sa représentation décimale en texte (`"3"`).
* Une **liste** : les éléments séparés par `;` (`"21181;21183"`). Vide = clé absente.
* Une clé **par joueur** : `Player N <clé>` (N de 1 à 4 : `Player 1 Role`, `Player 2 Tech Upgrade`). Le moteur
  accepte aussi la forme `<clé> P<N>`. Le panneau écrit toujours la première.
* Une clé **d'état à valeurs fixes** : un texte parmi une liste (`In play`, `In the victory display`,
  `Removed from campaign`) — voir Skrull Menace.
* Une clé **« pool »** : `Campaign Pool: <Nom>` = `"1"` quand la récompense `<Nom>` est acquise (convention de
  Mad Titan's Shadow, reprise par plusieurs boîtes).

**Lecture dans le code** (module `game/operate/campaign_logs.py`, classe `CampaignLog`, déjà importée par
`from . import *`) :

| Fonction | Rend |
|---|---|
| `CampaignLog.GetStrInternal(cle, effect)` | la chaîne, `''` si absente |
| `CampaignLog.GetIntInternal(cle, effect)` | un entier, `0` si absente (lève `ValueError` si la valeur n'est pas un nombre) |
| `CampaignLog.GetListInternal(cle, effect)` | une liste (valeur coupée sur `;`), `[]` si absente |
| `CampaignLog.GetStrByPlayer(cle, player_id, effect)` | la valeur du joueur (`player_id` **de 0 à 3**) |
| `CampaignLog.GetListByPlayer(cle, player_id, effect)` | la liste du joueur |
| `CampaignLog.GetIntByPlayer(cle, player_id, effect)` | l'entier du joueur |
| `CampaignLog.GetStr` / `GetInt` / `GetList` | idem, mais **typées** pour les clés historiques de The Rise of Red Skull et Sinister Motives (les `Literal` du fichier) : à l'exécution elles acceptent toute clé, mais pour une clé neuve **utilise les variantes `…Internal`** |
| `CampaignLog.SetStr(cle, valeur, world)` | **écrit** au carnet du monde (utilisé pour débiter une dépense de mise en place, ou noter une preuve en cours de partie) |

**Écriture** : le carnet est écrit à **la fin de la partie** par le collecteur (§7.5) ; il peut aussi l'être
pendant la partie par `CampaignLog.SetStr` (Agents of S.H.I.E.L.D. note une preuve gagnée en cours de partie ;
Hunting Season débite l'expérience dépensée à la mise en place). Tout ce qui est dans le store du monde est
recopié au carnet sortant.

**Le fichier réel :**
{{FICHIER:Fusion/marvel-lcg-src/src/game/operate/campaign_logs.py}}

### 7.2 Où le carnet entre dans une partie, et à quel moment

1. L'écran de campagne lance la partie avec `campaign_log = carnet de la campagne` (§2.3, étape 4).
2. À la construction du monde (`World.__init__`), chaque entrée est copiée dans le **store du monde** (`CampaignLog.SetStr`, `game/world/world.py`).
3. À la mise en place, **étape 13 « Campaign Setup »**, le moteur émet `Message.WhenCampaignSetup`. Toutes les
   capacités de type `AbilityType.Campaign` écoutent ce message. **Une capacité ne l'écoute que si la carte qui
   la porte existe dans la partie** : d'où le branchement sur la face 1A du complot principal (§7.3).
4. **Étape 15 bis** : `Message.WhenCampaignSetupAfterMulligans`, pour ce qui doit se résoudre **après** les
   mulligans (les preuves d'Agents of S.H.I.E.L.D. cherchent une carte dans le deck et l'ajoutent à la main : avant
   la pioche, elles feraient piocher une carte de moins ; avant le mulligan, le mulligan pourrait la défausser).
5. À la fin de la partie, `Message.WhenGameOver` : le collecteur écrit le carnet **sortant** (§7.5).

Ordre complet de la mise en place (extrait de `World.Initialize`) :
{{BLOC:Fusion/marvel-lcg-src/src/game/world/world.py|# [x] 11. Put Setup Cards|# [x] 16. Resolve Character|python}}

### 7.3 Brancher le carnet : `CampaignSetup(niveau)` sur la face 1A du complot principal

**Le mécanisme.** Les capacités de campagne d'un pack ne se déclenchent que si la **face 1A du complot principal**
du scénario appelle `CampaignSetup(niveau)` dans son `GetAbilities()` et en dépose le résultat dans la liste
retournée. **Sans cet appel, `Message.WhenCampaignSetup` n'a aucun auditeur et le carnet est ignoré, en silence.**

Le `niveau` est **le numéro du scénario dans la campagne**, de 1 à N (le `numero` de la description de campagne).

**Cas simple** (le complot n'avait aucune autre capacité) — `src/cards/pack/mts/ebony_maw/21074a.py` :
{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/mts/ebony_maw/21074a.py}}

**Cas d'un complot qui a déjà ses capacités** : on **ajoute l'import** et on **préfixe** la liste retournée —
`src/cards/pack/mts/the_tower_defense/21098a.py` :
{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/mts/the_tower_defense/21098a.py}}

**Cas d'une campagne maison (Web of Deceit), où la fonction de campagne s'appelle autrement** —
`src/cards/pack/web_of_deceit/shocker/wd002a.py` :
{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/web_of_deceit/shocker/wd002a.py}}

Règles à respecter, toutes mesurées :

1. **Un appel par scénario**, sur **la face 1A** (la face `a` du **premier** complot de `schemes`). Pas sur 1B, pas
   sur un stade suivant : la 1A est la face mise en jeu au départ, et c'est là que **tous** les modèles posent
   l'appel (une capacité de campagne ne part que si la carte qui la porte existe dans la partie).
2. L'import se fait depuis **`cards.pack.<pack>.campaign`** (le module `campaign.py` du pack), même quand le
   fichier de la carte est dans un sous-dossier.
3. **Le scénario 1 n'a pas toujours besoin de l'appel.** Dans The Rise of Red Skull, le scénario 1 (`crossbones`)
   n'appelle pas `CampaignSetup` : le carnet est vide, toutes les branches de `CampaignSetup` sont gardées par
   `if level >= 2`, et il n'y a pas de collecteur à poser. **Mais** si ton `CampaignSetup` pose le **collecteur**
   (`WriteCampaignLogAtGameOver`), l'appel au niveau 1 est **obligatoire** : sans lui, le carnet sortant du
   scénario 1 n'est jamais écrit et le scénario 2 n'a rien à lire (cas de NeXt Evolution).
4. **Le niveau doit être le bon.** Un niveau faux applique les récompenses d'un autre scénario, **sans erreur**.
   `verifier-livraison-campagne.py` compare, pour chaque scénario, le niveau appelé par sa 1A au `numero` de la
   description de campagne.
5. Le même `CampaignSetup(niveau)` sert en **standard et en expert** : la branche expert se déclare à
   l'intérieur (`WhenCampaignSetupExpertOnly`, `Worlds.IsExpert`).
6. **Ne réimplémente jamais le choix d'une face selon le mode** (standard/expert) dans la mise en place : une
   carte « Standard Mode Only » / « Expert Mode Only » se retourne **toute seule** à son entrée en jeu
   (`AbilityFactory.StandardModeOnly()` / `AbilityFactory.ExpertModeOnly()`, portés par la carte). C'est une erreur de
   lecture qui a déjà coûté une demi-journée (Public Outcry de Sinister Motives).

### 7.4 Les fabriques de campagne (`AbilityFactoryCampaign`) — le fichier réel

C'est **toute** la surface moteur dédiée aux campagnes. Tu n'en utilises **que** ces fonctions pour poser une
capacité de campagne ; tout le reste est du code Python ordinaire qui appelle les opérations du §6.

{{FICHIER:Fusion/marvel-lcg-src/src/game/ability/factory/campaign.py}}

En résumé :

| Fabrique | Quand elle part |
|---|---|
| `WhenCampaignSetup(operation, conditions=[])` | étape 13, **à chaque campagne** (standard et expert) |
| `WhenCampaignSetupExpertOnly(operation, conditions=[])` | étape 13, **campagne experte seulement** |
| `WhenCampaignSetupAfterMulligans(operation, conditions=[])` | étape 15 bis, après les mulligans |
| `ExpertCampaignSetPlayersHPToTheirRemainingHP()` | expert : remet les PV de chaque joueur à `Player N Remaining hit points` |
| `PutCardIntoPlay(card_id, under_control)` | met une carte en jeu à la mise en place |
| `ShuffleCardIntoDeck(card_id, "EncounterDeck")` | mélange une carte dans le deck de rencontre |
| `ChooseCardAtRandomAndShuffleIntoEncounterDeck(card_ids)` | tire une carte au hasard parmi celles non encore au carnet |
| `ExpertCampaignEachPlayerMayDealFacedownEncounterCardYpHealHP(n)` | expert : soin contre une carte rencontre face cachée |
| `ExpertCampaignAddRandomObligationFromExpertCampaignToHealHP(obligations)` | expert : soin contre une obligation aléatoire du set expert |

La **signature d'une opération** est toujours `def action(effect: 'Effect', message: 'Message.WhenCampaignSetup')`.
Une opération peut : générer une carte (`CardFactory.GenerateCard(id, deck_ou_None, effect.world)`), la mettre en
jeu (`card.face.PutIntoPlay('FirstPlayer', effect, under_control=…)`), la mélanger
(`Faces.ShuffleAllTo([face], 'EncounterDeck' | deck_du_joueur, effect)`), l'attacher
(`face.CastTo(Upgrade).AttachTo2(identite, effect)`), infliger des dégâts, défausser le dessus d'un deck, retirer
une carte de la partie (`Faces.RemoveAllFromGame`), poser des jetons (`PlaceTokensInternal`), ou poser une
question à un joueur (`player.MayChooseOneAbility`, `AskChooseOneText`).

### 7.5 Le carnet sortant : `WriteCampaignLogAtGameOver`

**Ce que c'est.** Une capacité (`AbilityType.Campaign`, message `WhenGameOver`) que **ton `CampaignSetup`
ajoute à sa liste** (dernière ligne : `abilities.append(WriteCampaignLogAtGameOver(lambda effect, message:
CollectXXX(level, effect)))`). À la fin de **chaque** partie de campagne (victoire comme défaite), elle écrit
`.game/campaign_log_last.json` :

```json
{ "players_won": true, "scenario": "ebony_maw", "suggestions": { "Campaign Pool: Cosmo": "1", "Player 1 Remaining hit points": "7", "Player 1 Identity": "Spider-Man" } }
```

* `suggestions` = **tout ce qui est dans le store du monde** (le carnet entrant + tout ce qui y a été écrit
  pendant la partie) **moins** les clés secrètes, **plus** `Player N Remaining hit points` et `Player N Identity`
  (ajoutés automatiquement), **plus** ce que renvoie ta fonction `collect_fn`.
* `collect_fn(effect, message)` renvoie un `dict` de mises à jour : `{clé: valeur}` ajoute/remplace, `{clé: None}`
  **retire** la clé.
* **Le résultat de la partie se lit dans `message.players_won`, JAMAIS dans l'état du monde** : le message est
  émis *avant* que `world.game_over` soit posé, un collecteur qui lit le monde voit toujours « perdue ». (c'est ainsi que Fear No
  Evil ne cochait jamais l'affaire à la victoire, trouvé le 19/09/2026 par `tools/test_campagnes.py`.)
* `scenario` (l'**estampille**) : le panneau **ignore en bloc** les suggestions dont l'estampille diffère de
  l'`id` du scénario joué. Par défaut l'estampille est le `set_name` du complot principal actif, passé en
  minuscules et soulignés (`'Ebony Maw'` → `ebony_maw`). **Elle doit être égale à l'`id` du scénario dans
  `data/campagnes/<code>.json`.** Quand `set_name` ne suffit pas (`gmw` : `collector_1` pour le scénario
  `infiltrate_the_museum` ; Hunting Season : `hs_vermin`), passe-la explicitement :
  `WriteCampaignLogAtGameOver(collect, scenario_id='hs_vermin')`.
* **Où est la fonction ?** Dans `cards/pack/mts/campaign.py` (partagée par toutes les boîtes). Un autre pack
  l'importe : `from cards.pack.mts.campaign import WriteCampaignLogAtGameOver, ActiveMainSchemeStartswith`.
* Le collecteur est **facultatif**. Les boîtes **sans** collecteur (`trors`, `sm`, `web_of_deceit`) laissent le
  panneau déduire les valeurs par des **détecteurs** déclarés dans `data/campagnes/<code>.json` (§8.4) ou faire
  saisir le joueur. **Préfère un collecteur** dès que la récompense se lit dans l'état de fin de partie : c'est
  plus fidèle et testable (`FIN_DE_PARTIE=1` à la sonde).

**Exemple complet : le collecteur de Mad Titan's Shadow** (tout `campaign.py` est plus bas, §7.6) :
{{BLOC:Fusion/marvel-lcg-src/src/cards/pack/mts/campaign.py|def CollectMTS|def CampaignSetup|python}}

### 7.6 Un `campaign.py` complet, officiel : The Mad Titan's Shadow

C'est le **modèle de départ** recommandé : un collecteur, des `CampaignSetup` par niveau, des fonctions
d'application du carnet. Lis-le en entier ; les noms de ses fonctions (`InPool`, `LogSet`,
`PutIntoPlayIfPool`…) sont des briques réutilisables (importe-les depuis `cards.pack.mts.campaign`).

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/mts/campaign.py}}

### 7.7 Deux autres modèles complets : le style « niveau croissant » et une campagne maison

**The Rise of Red Skull** : pas de collecteur ; `CampaignSetup(level, campaigns=[...], campaigns_expert=[...])`
accepte des fonctions propres au scénario (utilisées par `red_skull/04128a.py`) :

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/trors/campaign.py}}

**Web of Deceit** (campagne maison, arbres de talents) : **aucun collecteur** ; les gains sont **choisis par le
joueur** dans le panneau (champs `type: "choix"`) et le moteur les **remet dans le deck de chaque joueur** à
chaque mise en place :

{{FICHIER:Fusion/marvel-lcg-src/src/cards/pack/web_of_deceit/campaign.py}}

### 7.8 La bibliothèque de motifs : ce que les douze campagnes savent déjà faire

Chaque ligne = une fonction de `campaign.py` qui **existe, est testée** (`tools/epreuves_campagnes.py`), et que tu
peux imiter. Les fichiers entiers sont dans `modeles/D-patrons-de-campaign-py/` du zip.

| Besoin | Fonction modèle | Fichier |
|---|---|---|
| Une carte entre en jeu **si** une récompense est au carnet | `PutIntoPlayIfPool` | `mts/campaign.py` |
| Une carte est mélangée au **deck de rencontre** si… | `ShuffleIntoEncounterIfPool`, `ShuffleEachExperimentalAttachmentIntoTheEncounterDeck` | `mts`, `trors` |
| **Chaque joueur** mélange une copie d'une carte dans **son** deck | `EachPlayerShufflesCopyIfPool` | `mts` |
| Une carte est **attachée** à l'identité de chaque joueur | `EachPlayerNornStoneIfPool` | `mts` |
| Une **pénalité** de mise en place (dégâts, moitié du deck défaussée) | `AvengersTowerDamagedPenalty`, `InfinityStonesCompletedPenalty` | `mts` |
| Expert : un pion Accélération contre un soin complet | `ExpertMayPlaceAccelerationToHeal` | `mts` |
| Remettre dans **le deck de chaque joueur** les cartes qu'il a gagnées (liste par joueur) | `EachPlayerAddRescuedAlliesToTheirDeck`, `ChaqueJoueurRetrouveSesTalents`, `CartesAjoutees` | `trors`, `web_of_deceit`, `hunting_season` |
| Rôle / amélioration différente selon un **rôle** choisi en jeu | `EachPlayerRoleUpgrade`, `PutRoleUpgradeIntoPlay` | `mut_gen` |
| **Alliés captifs** libérés : le joueur choisit dans quel deck (ou aucun) | `ShuffleCaptiveAlliesIntoDeck` | `mut_gen` |
| Environnements « gagnés » qui entrent en jeu au scénario suivant | `PutEarnedEnvironmentsIntoPlay` | `next_evol` |
| Mission tirée parmi plusieurs, jamais deux fois | `SetupMissionAndOverseer` | `aoa` |
| **Solde** de points/unités et **marché** | `Experience`, `PoserExperience`, `GainsDExperience` ; `EachPlayerMarketCardsIntoDeck` | `hunting_season` ; `gmw` |
| **Enquête** à secret côté serveur | `PoserLeConseil`, `PreuveEnJeu`, `NoterPreuveGagnee` | `aos` |
| **Zone** partagée entre scénarios, tableau de progression, tirage d'« Élites » | `_cartes_de_la_zone`, `AssignerLaProgression`, `_elites` | `skrull_menace` |
| Carnet **par affaire** en ordre libre, retrait de cartes du deck | `MettreLesEnvironnements`, `RetirerLesCartesRetirees` | `fne` |
| Compteur de **menace reporté** (pions retard) | `the_rise_of_the_red_skull_place_threat` | `trors/red_skull/04128a.py` |
| **PV persistants** en expert | `AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP` | moteur |

### 7.9 Règles d'écriture des clés du carnet

1. **Copie le vocabulaire du livret** pour nommer une clé (`Allies removed from the campaign`, `Hunter Mode`) :
   l'écran et les rapports s'y retrouvent.
2. **Une clé = une signification, un format.** Ne réutilise pas une clé pour deux choses.
3. **Une clé écrite doit être lue, une clé lue doit être écrite.** Dresse la table (§7.10) et vérifie-la.
4. **Les clés « par joueur »** se lisent par `…ByPlayer` ou par `f'Player {player.player_id + 1} {cle}'` (jamais
   en dur).
5. **Un identifiant de carte** noté au carnet est un `card_id` complet (`'wd113'`), pas un nom : le nom change de
   langue, pas l'identifiant.
6. **Jamais de caractère `;` dans une valeur** de liste (c'est le séparateur) ; jamais de chaîne vide : retire la
   clé.
7. **Les clés secrètes** (que le joueur ne doit jamais lire, comme la combinaison de la taupe d'Agents of
   S.H.I.E.L.D.) se gardent **côté serveur** : demande-le à Claude (`BESOINS-MOTEUR.md`).

### 7.10 La table des clés du carnet — **livrable obligatoire** (`CARNET-CLES.md`)

Tu livres, pour **chaque** clé du carnet de ta campagne, une ligne :

| Clé | Format | Par joueur ? | Écrite par (fichier : fonction) | Lue par (fichier : fonction) | Déclarée dans la description de campagne (scénario, `type`, `detection`) | Source du livret (page) |
|---|---|---|---|---|---|---|
| `Campaign Pool: Cosmo` | drapeau `"1"` | non | `mts/campaign.py : CollectMTS` (niveau 1) | `mts/campaign.py : CampaignSetup` (niveau 3, `PutIntoPlayIfPool`) | `mts.json`, scénario `ebony_maw`, `auto`, `int` | « Campaign Log », p.12 |

Une ligne sans « lue par » est une **récompense qui disparaît en silence**. Une ligne sans « déclarée dans la
description » est une clé que **le panneau ne reportera jamais** (il ne garde que les clés déclarées).

### 7.11 Pièges propres à la logique de campagne (tous payés)

* **`player.GetHero()` lève une `AssertionError` (au lieu de rendre `None`) dès que le joueur est en forme Alter
  Ego** — ce qui est l'état normal en fin de partie. Pour le nom du héros : `identity.GetHeroFace()` (avec garde).
  Cette assertion avait coupé en silence toute écriture du carnet des quatre boîtes câblées.
* **`Faces.ShuffleAllTo` ne mélange que s'il a déplacé quelque chose.** Une carte générée **directement dans**
  `player_deck` ne « bouge » pas : le mélange ne part pas et la carte reste **sur le dessus**. Génère la carte
  **hors deck** (`CardFactory.GenerateCard(id, None, world)`), puis `ShuffleAllTo`.
* **« May » / « any player »** : « Each CAPTIVE ally recorded in the campaign log **may** be shuffled into **any**
  player's deck » = le joueur **choisit** (y compris « aucun ») ; ne mélange jamais d'office dans le deck du
  joueur 1.
* **L'état « fin de partie » n'est pas posé quand le collecteur tourne** (voir §7.5) : `message.players_won`.
* **Un carnet partiellement d'un autre scénario est pire qu'un carnet vide** : c'est pourquoi l'estampille compte.
* **Un livret en retard sur le carnet officiel** : le `campaign.py` dit ce que le moteur **fait**, le carnet
  imprimé dit ce que le livret **demande** ; **seul le second fait autorité**. Lis le carnet imprimé **avant**
  d'écrire la définition (cas de Mutant Genesis : deux lignes d'alliés dans le carnet officiel, une seule
  collectée au départ).
* **Un deck qui doit contenir une carte** : si le livret fait **chercher** une carte **dans le deck** du joueur
  (« Planning Ahead »), le joueur peut avoir retiré la carte entre deux scénarios ; la récompense disparaît alors
  en silence. Déclare le champ avec `"deck": "requis"` (§8.3) : l'écran refusera un deck qui ne la contient plus.
* **La carte de récompense n'est pas écrite dans le deck enregistré** : elle vit **au carnet** et le moteur la
  **génère** à chaque mise en place (`CardFactory.GenerateCard(id, player.player_deck, world)`). C'est ce qui rend
  possible « hors limite min/max du deck ».
* **Chaque capacité de campagne doit être idempotente vis-à-vis d'une défaite** : une défaite n'écrit rien au
  carnet, le scénario se rejoue avec **le même** carnet entrant.

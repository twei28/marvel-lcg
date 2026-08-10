# Rapport d'audit des cartes — 2 août 2026

Audit automatique de cohérence **texte imprimé ↔ capacités réellement
construites** sur les 4436 cartes, puis relecture humaine de chaque suspicion
(texte complet + script + moteur, marvelcdb en arbitre).

**État : tout est corrigé, testé et déployé des deux côtés.**
Bilan du jour : 10 discordances de script + 3 erreurs de données (audit
statique), 4 bugs supplémentaires (tests de comportement, dont 2 dans le
moteur), 5 conséquences de mission manquantes, 4 cartes d'un pack en cours qui
ne se construisaient pas, et 2 corrections antérieures.
Vérifications finales : `test_cards` **3886 ok / 0 err**,
`test_capacites` **41/41 cas verts**.

Outil : `tools/audit_cartes.py <dossier_de_jeu> <port> [rapport.json]`
À lancer sur `.game-src` (voir « Leçon d'outillage » plus bas), jamais sur le
dossier du serveur en cours.

## Bilan chiffré

| Vérification | Avant | Après |
|---|---|---|
| Cartes analysées | 4436 (dont 4211 scriptées) | idem |
| Arguments de fabrique mal typés | 0 | **0** |
| Coût d'inclinaison annoncé sans `CostFunc.Exhaust` | 1 | **0** |
| Cartes à texte « à capacité » sans aucun script | 0 | **0** |
| Capacités impossibles à construire | 0 | **0** |
| Marqueur imprimé sans capacité du même type | 123 suspicions | 115 (toutes expliquées) |
| `test_cards` (construction de toutes les capacités) | 3866 ok / 0 err | **3866 ok / 0 err** |

Les 123 suspicions ont été relues **une par une**. Verdict : **113 faux
positifs légitimes et 10 vraies discordances**, plus 3 erreurs de données
découvertes en chemin. Toutes corrigées.

Le fort taux de faux positifs est normal : le moteur rend souvent une capacité
sous un autre type que celui imprimé (« Forced Interrupt » via
`WhenUnitBeDefeated`, « Response » via `AfterUnitAttackAndDefeatUnit`), ou
depuis un helper partagé du set, une carte liée (`ability_link`), l'autre face,
ou un moteur générique (`cards/pack/aoa/missions.py`). Le marqueur est aussi
souvent seulement **cité** dans le texte (« cancel its "When Revealed" ability »).

---

## Les 10 discordances corrigées

Chacune a été vue deux fois (vérificateur puis moi) avant correction. Toutes
les modifications portent un commentaire `# CORRECTIF` pour survivre à une
future resynchro avec le source officiel.

| Carte | Défaut | Correction |
|---|---|---|
| `04162b` Improved Recovery Upgrade | Le texte impose « exhaust this card → draw 1 card », le script n'avait **aucun coût** : pioche à chaque récupération sans jamais s'incliner | `.SetCostFunc(CostFunc.Exhaust("This"))` |
| `55041` The Mangog | Carte **totalement inerte** : deux fonctions au corps entièrement commenté, et son « When Defeated » jamais déclaré | Stubs retirés, `When Defeated` branché sur le helper du set (3 compteurs shatter + 1 de synergie) |
| `55003` Enchantress stade III | La Réponse Forcée « 1 charm counter » manquait (les stades I et II l'ont), et 3 menaces par héros au lieu de **4** | Helper `AfterEnchantressAttacksYouPlaceCharmCounter()` ajouté, `"3*"` → `"4*"` |
| `55022` Spellbound | « When Revealed » implémenté en `WhenSchemeBeDefeated` : l'effet partait quand les joueurs **déjouaient** la manigance | Passé en `WhenThisRevealed` |
| `56177` Venom Blast | Capacité **Boost absente**, et le palier 3 oubliait « stunned and confused + 1 compteur skill » | `WhenCardBecomeBoost` ajouté (patron de 56176) + palier 3 complété |
| `40187` Reaper | « Forced **Interrupt**: When Reaper attacks you » accroché à `AfterUnitAttackEnd` : effet **après** l'attaque, main déjà changée, identité inclinée trop tard pour l'empêcher de défendre | `WhenUnitWouldAttack` + `ForcedInterrupt` |
| `45160` Scarab | « 3 threat instead if the attack **defeated** an ally » testait les alliés **blessés** : 3 menaces dès qu'un allié était égratigné | Ajout du test `x.IsDefeated()` |
| `57068` Khonshu's Avatar | « Resolve that card's When Revealed ability » appelait `Reveal()` : révélation complète, qui résolvait **aussi le Renfort** et les mots-clés | `Faces.ResolveAbility(..., AbilityType.WhenRevealed, ...)` |
| `27009` Web-Bracelet | « **Hero** Response » typé `Response` nu : restriction de forme héros absente (124 des 134 cartes « Hero Response » utilisent `HeroResponse`) | `AbilityType.HeroResponse` |
| `41013` Cypher | « attacks **and damages** a confused enemy » sans filtre de dégâts : pioche même quand l'attaque n'inflige rien (cible Tenace, prévention) | `AfterUnitAttackAndDamageUnit` |

## Les 3 erreurs de DONNÉES corrigées

Ici le code était juste, c'est `data/cards.json` qui mentait (vérifié sur
marvelcdb). Le checksum du fichier a été recalculé et est accepté par le moteur.

| Carte | Ce qui était écrit | Texte officiel |
|---|---|---|
| `16062a` Protect the Planet | Nom **et** texte de la face 16061b (« Terrestrial Invasion ») | « Protect the Planet » / « **When Revealed**: Resolve the Badoon Ship's *Charge Up* ability. » |
| `09014` Iron Fist | « Iron **First** enters play… » + « **Response** » | « Iron Fist… » + « **Interrupt**: When Iron Fist attacks an enemy… » |
| `38031` Bonebreaker | « **Forced Interrupt**: After Bonebreaker engages you » | « **Forced Response**: After Bonebreaker engages you… » |

**Contrôle d'intégrité** : le miroir Windows n'ayant pas été touché pendant
l'opération, la comparaison des deux `cards.json` donne exactement 4401 cartes
de part et d'autre, aucun identifiant perdu ni ajouté, et **les 3 seules cartes
qui diffèrent sont ces 3 corrections**.

## Corrections appliquées avant l'audit (mêmes journée et méthode)

| Carte | Défaut | Correction |
|---|---|---|
| `90114a` Rescue « Rapid Responder » | `powers="DEF"` au lieu de `powers=["DEF"]` : la chaîne était comparée lettre par lettre, la Réponse **ne partait jamais** | `powers=["DEF"]` |
| `90121` First Responder | Se déclenchait aussi sur les dégâts au Méchant (conforme au texte, injouable en pratique) | Restreint aux personnages **amis**. **Choix de confort assumé**, à rediscuter |

---

## Cartes vérifiées

Les 123 cartes signalées par l'audit ont toutes été relues. Les **113 faux
positifs** ci-dessous sont confirmés corrects : la capacité existe bel et bien,
sous une autre forme que celle attendue par l'heuristique.

**Faux positifs, marqueur seulement CITÉ dans le texte** (la carte annule ou
référence la capacité d'une autre) : `01004`, `01078`, `02049`, `07031`,
`11022`, `14018`, `21036`, `27001a`, `27005`, `41007`, `41018`, `43038`,
`44044`, `45096`, `56016`, `63004`.

**Faux positifs, capacité rendue sous un autre type du moteur** : `01007`,
`01051`, `01052`, `01063`, `02021`, `03032`, `07035`, `07046`, `07047`,
`21095`, `21096`, `21097`, `21173`, `24043`, `25002`, `25004`, `25008`,
`27161`, `31027`, `32044`, `32076`, `32104`, `32124a`, `32124b`, `32172b`,
`33007`, `34002b`, `34020`, `35032`, `35033`, `37026`, `37027`, `37028`,
`37030`, `38018`, `39002b`, `40024`, `40047`, `42013`, `42020`, `43015`,
`45011`, `45012`, `45026`, `45043`, `45057`, `45066`, `45091`, `45105b`,
`45136`, `45145`, `47034`, `48014`, `50058`, `50108b`, `50130b`, `50170`,
`50171`, `53031`, `53035`, `54001a`, `54028`, `55029a`, `56007`, `56056`,
`56069`, `56091`, `56092`, `56093`, `56095`, `56098`, `58026`, `58033`,
`59024`, `59039`, `59041`, `60001a`, `60001b`, `62007`, `62011`, `63011`,
`64001a`.

**Faux positifs, capacité portée par un helper partagé ou un moteur générique**
(missions Âge d'Apocalypse, God of Lies, Gwenpool…) : `35014`, `45166a`,
`45167a`, `45168a`, `45169a`, `45170a`, `55034a`, `55034b`, `55027b`,
`56061`, `56094`, `56120`, `63001a`, `50184a`, `32164`.

**Cas particuliers documentés**
- `64001a` Human Torch (carte custom maison) : Interrupt volontairement rendu
  en Response, **divergence déjà commentée dans le script**.
- `02021` : type `ForcedInterrupt` là où la carte dit `Forced Response`. Le
  déclenchement reste correct (message « After ») ; seule la priorité de
  résolution diffère. Laissé tel quel.
- `NonKeywordStar` : ce n'est pas un type vide mais l'idiome maison des
  capacités marquées `[star]` (14 usages). Jamais une discordance en soi.

---

## Leçon d'outillage (important pour la suite)

L'audit a mis au jour un piège du banc de test lui-même : **`.game/` ne contient
presque que du bytecode** (4339 `.pyc` pour 8 `.py`). Tester dessus revenait à
valider une photo figée du moteur, pas les sources vivantes.

Un dossier `.game-src/` a été créé : ses dossiers de code (`cards`, `core`,
`engine`, `game`, `editor`, `main.py`) sont des **liens directs vers `src/`**,
ses données pointent sur les vrais dossiers. **C'est désormais lui qu'il faut
viser pour tout test.** Les deux suites (`test_cards.py`, `audit_cartes.py`)
donnent le même résultat sur `.game-src` et sur `.game` rafraîchi, ce qui
valide le nouveau banc.

Second enseignement : mon propre outil a d'abord crié au loup 15 fois sur des
signatures du genre `X|List[X]|None`, où passer un `X` nu est parfaitement
légal. Le détecteur ne signale désormais que les cas où **seule** une liste est
acceptée (le vrai bug de Rescue reste détecté, vérifié par test unitaire).

## Suite : tests de comportement (2 août, après-midi)

Un second niveau a été construit, `tools/test_capacites.py` : chaque cas monte
une position de jeu réelle avec l'API Puzzle, déclenche la capacité et vérifie
l'état du monde. **41 cas, tous verts**, couvrant nos packs custom (Thor Jane
Foster, Rescue, Albert, Gwenpool, Human Torch) et plusieurs corrections de
l'audit. Validé par l'épreuve inverse : bugs réintroduits, les tests échouent.

Cette batterie a trouvé **4 bugs supplémentaires, tous corrigés** :

| Où | Défaut | Correction |
|---|---|---|
| **Moteur** `can_place_counter.py` | `maximum = would_message.maximum or maximum` : la valeur **0** est fausse en Python, donc un plafond de zéro était ignoré. Hydro-Man, censé être immunisé aux compteurs flamme, en recevait, **et effaçait au passage le plafond de 3 de Human Torch** | test `is not None` |
| **Moteur** `card/factory.py` | l'événement 64009 Radiate a deux capacités « Play » ; l'assertion de dev refusait ce cas, donc **Human Torch ne se chargeait pas** hors mode RELEASE | ajouté à la liste blanche |
| `63011` Rules of the Universe | icône Aléa jamais recalculée (`change_on_event` manquant sur une manigance Permanente) | `change_on_event=OnEvent.Threat("This")` |
| `90126` Board Meeting | `identity.IsHero()` n'existe que sur `Player`, jamais sur une face : **plantage à chaque révélation** de l'obligation | `Hero.IsType(identity)` |

Les trois cas de test qui avaient été mis de côté servent maintenant de gardes
contre la réapparition de ces défauts.

## Missions de l'Âge d'Apocalypse

Leurs **conséquences de fin de mission** (portées officiellement par des faces
verso non modélisées) n'étaient pas implémentées : réussir ou rater une mission
n'avait aucun effet. Les cinq missions appliquent désormais leur vrai résultat,
et le texte des cartes l'annonce au joueur. Vérifié en partie réelle.

## ⚠️ Avertissement de synchronisation

Les deux installations **divergent** : le pack `invisible_woman` (héros custom
en cours, 65001a à 65018) n'existe que côté Windows. Un
`rsync -a --delete src/` de WSL vers Windows **cible ce pack pour suppression**
à chaque passage. Ne plus jamais employer `--delete` pour `src/` :

```bash
rsync -a --exclude='__pycache__' <source>/ <destination>/
diff -rq --exclude=__pycache__ <source> <destination>   # avant tout nettoyage
```

Le pack a été rapatrié côté WSL et les deux côtés sont désormais identiques.
Quatre de ses cartes ne se construisaient pas (API inexistantes) : corrigé.

## Ce que cet audit ne peut pas voir

Un test ne vérifie que ce que son auteur a pensé à vérifier. Cette passe attrape
les capacités absentes, mal typées, mal déclenchées ou sans coût. Elle **ne
détecte pas** un effet qui fait la mauvaise chose tout en ayant le bon type
(mauvaise cible, mauvais nombre), ni un choix de conception discutable comme
celui de First Responder. Pour ce niveau-là, il faudra des mini-scénarios de
jeu (le moteur sait déjà le faire via les puzzles).

---

## Reprise du 10 août 2026 : les 132 suspicions restantes

Le compteur était remonté de 123 à 132 avec les packs ajoutés depuis. La revue
a été refaite en entier, et elle change autant l'outil que le verdict.

**61 des 132 n'étaient pas des suspicions du tout.** Une fabrique sur deux
emballe la vraie capacité dans un `DelayAbility` :
`AfterUnitDefeatedUnit(AbilityType.Response, …)` rend un `DelayAbility` qui,
**à l'exécution seulement**, enregistre l'ability intérieure portant le
Response. Hors partie, le drapeau n'existe donc nulle part, et l'audit criait
au loup sur la moitié de son propre rapport. Le détecteur regarde désormais
aussi les `AbilityType.X` écrits dans la source et se tait quand le script
déclare le bon type. **Le compteur tombe de 132 à 71**, sans qu'aucune carte
n'ait changé. Il ne vérifie pas que la fabrique en fait quelque chose : c'est
le rôle de `tools/test_capacites.py`.

**114 des 132 avaient déjà été relues** le 2 août, à l'identifiant près. Les
**18 nouvelles**, toutes venues des packs postérieurs, ont été ouvertes une par
une : `21117`, `65001a`, `67012`, `68002`, `68012a`, `68012b`, `68016`,
`68017`, `69025`, `70003`, `71001a`, `72001a`, `73006`, `74014`, `75003`,
`75012`, `78017`, `78026`. **Dix-sept faux positifs**, dans trois familles déjà
connues : le type est déclaré mais emballé ; la capacité est rendue par une
fabrique dédiée du moteur (`ReduceCharacterTakeDamageBy`,
`IfThereAreAtLeastCounterHere`, `ThisGainKeyword`) ; ou le marqueur n'est que
CITÉ, la carte annulant le « When Revealed » d'une autre.

**Les 2 `exhaust_sans_cout` sont eux aussi des faux positifs**, vérifiés dans
le code et non plus supposés. `70003` Forces Combined s'incline dans son propre
gestionnaire, et `75012` Network of Trees dans `AppelerEcureuil`, seul point de
passage possible faute de message moteur « quand tu appellerais un écureuil ».
Aucun des deux ne peut passer par un `CostFunc.Exhaust`.

**Le seul vrai défaut trouvé n'en était pas un, et c'est la leçon.** Le script
de `72001a` Venom portait depuis le 5 août un avertissement « DEFAUT CONNU :
Hunger ne répond jamais », avec quatre pistes écartées. Hunger répond. Ce qui
manquait n'était pas dans la carte mais dans la façon de l'éprouver : Venom
frappe à 2, et contre un sbire de 3 PV son attaque de base ne tue pas, donc
rien ne se déclenche — tout en laissant au journal l'apparence d'une attaque
normale. Le cas ajouté lui donne Sharp Teeth pour monter à 3, et le journal
donne alors « was defeated by Venom » puis « Venom gains 1 ♡ ». **Un
avertissement en commentaire n'est pas une preuve ; il coûte plus cher qu'il ne
rapporte tant qu'aucun cas rouge ne l'accompagne.**

Deux pièges de l'API Puzzle découverts en écrivant ce cas, notés au §10 du
guide : `Puzzle.Damage` sur un sbire ne fait **rien**, ni par `card_id` ni par
nom et sans le moindre message ; et `Puzzle.Attack(x)` fait attaquer **x**,
donc viser le sbire le fait frapper le héros.

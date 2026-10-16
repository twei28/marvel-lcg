# Index des fiches mots-clés

Gabarit à copier pour chaque nouvelle fiche :

```markdown
# <Mot-clé>

**Texte imprimé / définition** : ...

**Mécanisme moteur** : ...

**Carte exemple** : `<card_id>` : <nom>, extrait du `.py` correspondant
(ou « lu directement depuis `desc`, aucun script requis »).

**Pièges connus** : ...

**Variantes maison** : ...
```

## Officiels

- [x] toughness.md
- [x] guard.md
- [x] quickstrike.md
- [x] retaliate.md
- [x] restricted.md
- [x] permanent.md
- [x] surge.md
- [x] villainous.md
- [x] hazard.md
- [x] crisis.md
- [x] acceleration.md
- [x] amplify.md
- [x] steady.md
- [x] stalwart.md
- [x] peril.md
- [x] incite.md
- [x] patrol.md
- [x] hinder.md
- [x] vulnerable.md
- [x] teamup.md
- [x] alliance.md
- [x] temporary.md
- [x] piercing.md
- [x] overkill.md
- [x] ranged.md
- [x] boost.md (icônes `desc.Boost` ET effet « [star] Boost », deux
      mécanismes distincts)
- [x] special.md (le `[star]` d'une capacité permanente, à ne pas confondre
      avec l'étoile d'un effet Boost)
- [x] teamwork.md (base native lue dans `desc.Teamwork`, aucun script — et
      deux règles cohabitent dans le moteur selon `v16_teamwork`)
- [x] uses.md (base native lue dans `desc.Uses`, aucun script : le moteur
      pose les pions à l'entrée en jeu ET fait sortir la carte au dernier pion
      retiré — ne PAS recoder la sortie)
- [x] setup.md (base native lue dans `desc.Setup` : la carte entre en jeu à
      la mise en place ; son texte « Setup: ... » se code par
      `AfterGameSetup`, jamais `WhenCardSetup`)
- [x] forced-action.md (type de capacité, pas un mot-clé : l'action que le
      joueur ne peut pas ignorer, `WhenInYourPlayTurn(ForcedAction)`)
- [x] victory.md (base native lue dans `desc.Victory` : la carte vaincue va
      dans la pile de victoire quel que soit le signe ; « Victory -1 » sur
      l'alliée Typhoid Mary de Fear No Evil, relu par le carnet de campagne)
- [x] requirement.md (« Requirement ([mental]) » : le paiement doit COMPORTER
      les ressources listees, elles ne s'ajoutent pas au cout)
- [x] starting.md (Fear No Evil : choix FACULTATIF de prendre la carte en main
      avant la pioche, une seule carte starting par deck)

⚠ **`Elite` n'est PAS un mot-clé** et n'a donc pas de fiche : c'est un TRAIT.
Il se déclare dans le tableau `traits` de la carte (`"traits": ["ELITE"]`),
jamais dans `desc`, et le moteur ne lui associe aucune mécanique. Confusion
la plus fréquente sur un pack vilain.

## Maison

- [x] eclair.md (pack `zeus` : une RESSOURCE maison, cinquième couleur du
      moteur `L`, ajoutée le 11/09/2026. ⚠ Distincte de l'énergie, que le set
      némésis vise, lui)
- [x] seek.md (⚠ **définition de l'auteur enfin trouvée le 08/09/2026**, dans
      l'insert de `spider_man_2099` : « défausser depuis le dessus jusqu'à
      défausser une carte du type voulu », et NON une recherche. Trois cartes
      livrées corrigées ce jour-là : `br005`, `br009`, `ar001a`)
- [x] track.md (pack `superior_spider_man` : « move 1 threat from a scheme to
      a minion in play ». ⚠ Un DEPLACEMENT, pas un retrait — et le compteur
      `threat` sur un SBIRE a du etre ajoute a l'enum `COUNTER`, cette
      menace-la n'ayant aucune existence native)
- [x] acceleration-2099.md (pack `spider_man_2099` : capacité d'identité
      **homonyme** de l'icône officielle `acceleration.md`, aucun rapport ;
      c'est aussi un MARQUEUR que six cartes du pack relisent)
- [x] drain-x.md (pack `agent_anti_venom`)
- [x] traitor.md (pack `agent_anti_venom`)
- [x] companion.md (pack `lockjaw`)
- [x] squirrel.md (pack `squirrel_girl`)
- [x] destroy.md (pack `sentinel` : detruire un Component = 2 degats
      imblocables + retournement Intact -> Detruit)
- [x] exposed.md (pack `sentinel` : carte d'etat maison, EMPILABLE, sans
      plafond, contrairement a Coriace)
- [x] investigate-x.md (pack `jessica_jones`)
- [x] setlist.md (pack `dazzler`)
- [x] registered.md (pack `iron_patriot` : un SECOND DECK de 20 sbires qu'on
      retourne contre le méchant en payant leurs ICÔNES DE BOOST.
      ⚠ C'est un TRAIT, pas un mot-clé — la fiche existe pour les quatre
      pièges moteur de la conversion sbire → allié, mesurés le 10/09/2026)
- [x] weakness.md (aspect `venomized` : des cartes de RENCONTRE qui vivent
      dans le DECK DU JOUEUR et frappent quand on les pioche EN MAIN.
      ⚠ Aucun code moteur — mesure du 09/09/2026, 2 cas calibres)
- [x] showtime.md (pack `dazzler`)
- [x] armored.md (pack `superior_iron_man`)
- [x] fragile.md (pack `okoye`, déjà défini une première fois dans le pack
      `determination` — même mécanisme, réutilisé ici)
- [x] legion.md (pack `okoye`)
- [x] plotting.md (pack `scarlet_spider`)
- [x] breakthrough.md (pack `viv_vision`, mot-clé JAMAIS défini par l'auteur :
      définition arbitrée le 02/09/2026, miroir d'`overkill` pour la menace)
- [x] summon.md (pack `yondu`, employé SIX fois et JAMAIS défini par l'auteur :
      définition arbitrée le 03/09/2026 — fouiller le deck ET la défausse —,
      sans quoi une Yaka Arrow défaussée est perdue et neuf cartes du pack
      deviennent mortes)
- [x] multiverse.md (packs `rainy`, `brawn`, `blackcat` : mot-clé employé par
      TROIS auteurs et défini par AUCUN. Définition arbitrée le 05/09/2026 —
      marqueur de deckbuilding, ZÉRO ligne de code, l'unicité fait tout le
      travail. ⚠ à ne pas confondre avec le TRAIT `MULTIVERSE` de `wd029`)
- [x] agile.md (pack `night_thrasher`, `nt003a` Battle Board face VEHICLE :
      définition DONNÉE par l'auteur entre parenthèses, aucun arbitrage — mais
      aucune primitive moteur, et un contre-cas « attaque sans carte de boost »
      obligatoire, sans quoi les deux montages possibles passent au vert)
- [x] reckless.md (aspect `determination` : 1 menace sur chaque manigance à
      l'entrée en jeu, `Reckless()` dans le `__init__.py` du pack)
- [x] alias.md (aspect `determination` : gratuit si un homonyme de
      SOUS-TITRE est contrôlé, qui est défaussé. ⚠ Inerte aujourd'hui : les
      quatre porteurs ont un `subtitle` vide dans `cards.json`)
- [x] fleeting.md (aspect `determination`, `dt087` : défaussée en fin de
      phase. ⚠ NON IMPLÉMENTÉ, malgré le commentaire du `.py` qui prétend
      le contraire ; crochet `WhenPhaseEnd` disponible)

- [x] initiative.md (Skrull Menace, `sk263` Crusader : « INITIATIVE » est un
      TRAIT imprimé, pas un mot-clé ; aucune règle n'est écrite sur la carte,
      zéro ligne de code. ⚠ À ne pas confondre avec le set officiel « The
      Initiative »)

- [x] dazed.md (scenario `baxter_stockman` : SIXIEME carte d'etat, -2 aux pouvoirs de
      base / +2 aux degats, un seul effet puis defaussee, un seul Dazed par personnage ;
      Tough d'abord, Cloaked et Dazed SIMULTANES. Verbe « daze » = poser la carte)
- [x] replicate.md (scenario `baxter_stockman` : la capacite nommee « Replicate », de type
      SPECIAL, portee par `tx004b` et resolue par le joueur)
- [x] all-purpose-counter.md (terme officiel : le type du compteur est celui de la carte qui
      le porte ; FAQ MC4DB du 29/09/2026)

- [ ] cloak.md (pack `leonardo`, TMNT : mot-clé imprimé en verbe sur tl015 et
      tl016 et JAMAIS défini — fiche créée le 15/10/2026 SANS définition ni
      mécanisme, stub `Cloak()` en attente de la réponse de l'utilisateur,
      question Q1 de `.planning/tmnt/leonardo-phase-a.md`)

- [x] cloak.md (pack `donatello`, TMNT Heroes : mot-clé employé UNE fois et
      JAMAIS défini — AUCUN arbitrage, stub inerte, question Q-TD-05)
- [x] swarm.md (pack `donatello` : trait + compteur `swarm`, mécanique dans le
      texte de `td016` / `td017`)
- [x] tuck.md (terme officiel, `td012` Donatello's Shell ; jamais documenté
      avant ce pack)

## Packs passés en revue, aucun mot-clé imprimé propre trouvé

Vérification faite avec l'heuristique `<b>([A-Z][a-zA-Z ]{2,20})</b>` sur
`desc.text`/`text` de chaque carte du pack dans
`Fusion/marvel-lcg-src/data/cards.json` (voir Task 15). Dans les 13 packs
listés ci-dessous, chaque occurrence de `<b>...</b>` trouvée est un label
de type d'aptitude standard officiel (Action, Response, Interrupt, Hero
Action, Hero Interrupt, Hero Response, Hero Resource, Alter-Ego Action,
Alter-Ego Response, Resource, Setup, Special, Boost, Forced Response,
Forced Interrupt, When Revealed, When Defeated) : aucun terme en gras
propre au pack, donc aucun mot-clé maison à cataloguer.

- **`rainy`** (Thor/Jane Foster) : aucun terme en gras hors labels
  d'aptitude standards.
- **`albert`** (Wolverine robot) : idem.
- **`gwenpool`** : la mécanique des BULLES (texte à trous résolu par
  `ResolveBlank()` dans `cards/pack/gwenpool/gwenpool/__init__.py`) n'est
  matérialisée par aucun mot en gras sur le texte imprimé des cartes ; ce
  n'est pas un mot-clé, c'est un mécanisme de remplissage de texte propre à
  ce set.
- **`human_torch`** : les compteurs `flame` (Flame On!) ne sont jamais
  nommés en gras dans le texte imprimé ; simples compteurs de carte.
- **`mister_fantastic`** : mécanique « main vidée puis rechargée », aucun
  mot en gras propre.
- **`the_thing`** : les jetons Tenace (gagnés puis dépensés via Give 'Er /
  Take That!) ne sont jamais imprimés en gras dans `desc.text` ; simples
  jetons de carte, pas un mot-clé.
- **`totally_awesome_hulk`** : identité à trois faces et compteurs `rage`
  pilotant les changements de forme, aucun terme en gras propre au pack.
- **`invisible_woman`** : identité triple face, aucun terme en gras propre.
- **`cloak_dagger`** : mécanisme `linked_identity` (deux identités pour un
  joueur), aucun terme en gras propre ; les seules balises non standards
  rencontrées (`<hr>` sur `iw016`/`iw017`, pack `invisible_woman`) sont de
  la mise en forme, pas un mot-clé.
- **`spider_man_rainy`** : compteurs `web` (toile), aucun terme en gras
  propre.
- **`venom_rainy`** : aucun terme en gras propre.
- **`moon_knight`** : identité à cinq faces + set modulaire « Age of
  Khonshu », aucun terme en gras propre.
- **`brawn`** : la zone **Réserve** (nouvelle zone de joueur ajoutée au
  moteur, documentée en détail au §9 de `GUIDE-CREATION-CONTENU.md`,
  ligne « La zone RÉSERVE ») est un mécanisme maison majeur, mais son nom
  n'apparaît **jamais en gras** sur le texte imprimé des 26 cartes du pack
  (vérifié par balayage complet des balises `<b>` de `brawn` : seuls les
  labels d'aptitude standards y figurent) ; les cartes y font seulement
  référence en texte normal (« put this card into your reserve »). Selon
  le critère de cette tâche (mot-clé = terme en gras sur carte imprimée),
  ce n'est pas un mot-clé à ficher ici, malgré son importance mécanique :
  le mécanisme reste documenté au §9 du guide, pas dans ce catalogue.
- **`speed`** (Tommy Shepherd, set 141, 30/08/2026) : les **compteurs
  explosifs** de l'insert du pack sont un mécanisme maison central, mais le
  terme n'est **jamais imprimé en gras** — balayage complet des balises `<b>`
  des 23 cartes : `Action`, `Alter-Ego Action`, `Forced Interrupt`, `Forced
  Response`, `Hero Action`, `Hero Interrupt`, `Hero Response`, `Interrupt`,
  `Resource`, `When Revealed`, la ligne « Give to the Thomas Shepherd
  player. », et **`Permanent`** (sd018), qui a déjà sa fiche. Même critère que
  la Réserve de `brawn` et que les compteurs `flame` de `human_torch` : ce sont
  des compteurs de carte, pas un mot-clé. Le mécanisme est documenté en tête de
  `src/cards/pack/speed/speed/__init__.py` et dans `docs/speed_cartes.md`.
  `Quickstrike` (sd019) est imprimé sans gras mais possède déjà sa fiche.

- **`venompool`** (Wade Wilson symbiote, set 129, 31/08/2026) : balayage
  complet des balises `<b>` des 17 cartes — `Action`, `Boost`, `Forced
  Interrupt`, `Hero Action`, `Hero Interrupt`, `Hero Response`, `Response`,
  `When Revealed`, et la ligne « Give to the Wade Wilson player. » : que des
  labels d'aptitude standards. Les six mots-clés que le pack CITE ont tous
  déjà leur fiche ou sont natifs du moteur : `drain X` (vp009, vp010 — et
  c'est l'insert de CE pack qui en a enfin donné la définition imprimée, voir
  `drain-x.md`), `Plotting` (vp015), `Quickstrike` (vp014), `surge` (vp011,
  vp016), `overkill` (vp010), `piercing` (vp004). Les compteurs
  d'**adrénaline** de Killer Thrill (vp013) ne sont jamais imprimés en gras :
  même critère que la Réserve de `brawn` et les compteurs explosifs de
  `speed`, ce sont des compteurs de carte, pas un mot-clé.

- **`angela`** (Aldrif Odinsdottir, set 133, 31/08/2026) : balayage complet
  des balises `<b>` des 16 cartes — `Boost`, `Forced Interrupt`, `Hero
  Action`, `Hero Interrupt`, `Hero Resource`, `Response`, `Setup`, `When
  Revealed` : que des labels d'aptitude standards. Les quatre mots-clés que le
  pack CITE ont tous déjà leur fiche ou sont natifs : `steady` (an006),
  `Restricted` (an009, lu dans `desc`), `surge` (an010), `overkill` (an013).
  Le décompte « each minion you defeated this round » (an004, an007) est un
  mécanisme central du pack mais n'est **jamais imprimé en gras** : même
  critère que la Réserve de `brawn` ou les compteurs d'adrénaline de
  `venompool`, ce n'est pas un mot-clé. Il est rendu par
  `PlayerStat.round_kill_counter`, ajouté au moteur pour l'occasion.

Quatre packs supplémentaires, absents du §9 du guide et inaccessibles
depuis ce worktree (existent uniquement dans un checkout non lié), ont été
vérifiés directement par l'agent contrôleur avec la même heuristique
`<b>` : conclusion transmise et reprise ici telle quelle.

- **`wolverine_x23`** : un seul helper de script par carte (ex.
  `EstTonHeros`), aucun mot-clé en gras correspondant sur le texte
  imprimé.
- **`red_guardian`** : un seul helper de script par carte (ex.
  `BouclierEnJeu`), aucun mot-clé en gras correspondant sur le texte
  imprimé.
- **`jj`** : `__init__.py` du pack entièrement vide, aucun mécanisme
  maison d'aucune sorte.
- **`luke_cage`** : `__init__.py` du pack entièrement vide, aucun
  mécanisme maison d'aucune sorte.

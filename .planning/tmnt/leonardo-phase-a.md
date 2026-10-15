# Leonardo (TMNT, Inkwire) — phase A : construction (15/10/2026)

Branche / worktree : `worktree-agent-af57d636d7018b6db`
(`/home/oem/Desktop/Marvel LCG/.claude/worktrees/agent-af57d636d7018b6db`).
Source : zip « TMNT Heroes-20261014T200300Z-1-001.zip », dossier
« TMNT Heroes/Leonardo v3/ » (24 PNG, tous lus à la vision, carte par carte).

**RIEN n'est validé.** Aucun harnais lancé, aucune partie montée, aucun script
exécuté : seules la syntaxe et l'existence des noms d'API (`Faces.X`,
`CostFunc.X`...) ont été vérifiées statiquement (outil jeté, calibré par une
erreur volontaire). Aucun gabarit PROCESSUS-CARTE n'est rempli : phase C.

## 1. card_id créés (17) — préfixe `tl`, pack `leonardo`, set 164

Préfixe `tl` vérifié libre (`tools/verifier_prefixes.py` : OK après ajout ;
calibré en renommant temporairement `tl` : la gate tombe bien).

| card_id | type | nom | exemplaires | set_name |
|---|---|---|---|---|
| tl001a | Hero | * Leonardo | 1 | Leonardo |
| tl001b | AlterEgo | * Leo | 1 | Leonardo |
| tl002 | Ally | * Splinter | 1 | Leonardo |
| tl003 | Event | Uke Nagashi | 2 | Leonardo |
| tl004 | Event | Vigilant | 2 | Leonardo |
| tl005 | Event | Stoicism | 2 | Leonardo |
| tl006 | Event | Yo Ko Giri | 2 | Leonardo |
| tl007 | Support | * Leo's Greenhouse | 1 | Leonardo |
| tl008 | Upgrade | Iaijutsu | 1 | Leonardo |
| tl009 | Upgrade | Taichō | 1 | Leonardo |
| tl010 | Upgrade | Nukitsuke | 1 | Leonardo |
| tl011 | Upgrade | * Leonardo's Katana | 1 | Leonardo |
| tl012 | Upgrade | * Leonardo's Other Katana | 1 | Leonardo |
| tl013 | Obligation | Brainwashed Betrayal | 1 | Leonardo |
| tl014 | SideScheme | Foot Patrol | 1 | Leonardo Nemesis |
| tl015 | Minion | * Karai | 1 | Leonardo Nemesis |
| tl016 | Minion | Foot Soldiers | 3 (même card_id) | Leonardo Nemesis |

Les 24 scans = 17 card_id : les doublons (Uke Nagashi 2/3, Vigilant 4/5,
Stoicism 6/7, Yo Ko Giri 8/9, Foot Soldiers 3/4/5) ne diffèrent que par le
numéro de collection du pied de carte (différence de pixels mesurée : seulement
la zone du numéro). « Other Katana flipped » = UNE seule carte (15/15) dont la
mise en page est inversée (miroir), pas une seconde face.
`insert` (« Katana Weapon Rules ») = feuille de règles, pas une carte : non
transcrite en card_id (voir Q8).

Deck de départ : `hero_deck` = 15 cartes (Splinter 1, Uke 2, Vigilant 2, Stoicism
2, Yo Ko Giri 2, Greenhouse, Iaijutsu, Taichō, Nukitsuke, Katana, Other Katana),
`obligations` = [tl013], `nemesis_set` = [tl014, tl015, tl016 x3],
`player_deck` = **[]** (aucune decklist d'auteur dans le zip).
Étape 10 de PROCESSUS-HEROS : aucune carte Hero étrangère possible (player_deck vide).

## 2. Fichiers modifiés / créés (dans le worktree)

Modifiés :
- `Fusion/marvel-lcg-src/data/cards.json` (pack `leonardo` en queue, 17 cartes,
  `custom: "Inkwire"`, checksum recalculé)
- `Fusion/marvel-lcg-src/data/sets_info.json` (`164. Custom (Leonardo)`, checksum recalculé)
- `Fusion/marvel-lcg-src/tools/prefixes_fanmade.json` (préfixe `tl`)
- `Fusion/marvel-lcg-src/public/js/prepare/heros-info.js` (bio `tl001a`)
- `Fusion/marvel-lcg-src/src/game/card/face/card_face.py` (énum TRAITS : NINJA,
  TURTLE, TEENAGER, RAT, SENSEI, KATANA, STANCE, FOOT CLAN, NYC, SKYLINE)
- `ui-app/src/board/textes-fr-fanmade.ts` (17 entrées FR ; « Cloak » laissé en anglais)
- `docs/reference/mots-cles/README.md` (ligne `cloak.md`, case non cochée)

Créés :
- `Fusion/marvel-lcg-src/deck/starter/leonardo.json`
- `Fusion/marvel-lcg-src/data/nemesis/leonardo_nemesis.json`
- `Fusion/marvel-lcg-src/src/cards/pack/leonardo/__init__.py`,
  `leonardo/leonardo/__init__.py`, `leonardo/leonardo_nemesis/__init__.py` (stub `Cloak`)
- `.../leonardo/leonardo/tl001a.py`, `tl001b.py`, `tl002.py` ... `tl013.py` (13 scripts)
- `.../leonardo/leonardo_nemesis/tl014.py`, `tl015.py`, `tl016.py`
- `docs/reference/mots-cles/cloak.md` (fiche SANS définition, mot non défini)
- ce fichier

**HORS worktree (images, non versionnées : `assets/pics/` est gitignoré)** :
- 17 JPEG `tl*.jpg` (petit côté 615, qualité 88 = même règle que
  `outils/uniformiser-scans.py`) dans
  `/home/oem/Desktop/Marvel LCG/Fusion/marvel-lcg-src/assets/pics/` ;
- originaux pleine taille (JPEG q95) dans
  `/home/oem/Desktop/Marvel LCG/sauvegardes-serveur/scans-originaux/tl*.jpg`.
  `uniformiser-scans.py` n'a PAS été lancé (il traite tout `assets/pics` et chemine
  en dur vers le checkout principal : conflit avec les 3 autres agents) ;
  équivalent écrit à part, même paramètres. Fichiers neufs, noms uniques `tl*`.

## 3. Points de fusion avec les 3 autres tortues (à connaître)

- `card_face.py` (énum TRAITS), `prefixes_fanmade.json`, `sets_info.json`,
  `cards.json`, `heros-info.js`, `textes-fr-fanmade.ts`, `mots-cles/README.md` :
  chaque agent ajoute au MÊME endroit, conflits de contexte triviaux à résoudre
  à la main (concaténer les ajouts).
- **Numéro de set 164** pris pour Leonardo ; si un autre agent a pris le même,
  `verifier_prefixes.py` (contrôle 4) le signalera : renuméroter.
- `cloak.md` : les trois autres tortues pourraient créer la même fiche si elles
  rencontrent aussi « Cloak » → fusionner.
- Traits TMNT communs probables (NINJA, TURTLE, FOOT CLAN...) : doublons dans le
  `Literal` sans conséquence (purement déclaratif).

## 4. Lectures de scan à confirmer (non bloquantes)

- Icônes de ressource : lues par la correspondance documentée dans
  `RECETTES-MOTEUR.md` §8 (poing rouge = physique `R`, nœuds bleus = mental `B`,
  éclair jaune = énergie `Y`, étoile verte = wild `G`). **Aucune carte du même pack
  n'a de `RES` connue en base** (pack inédit) : le contrôle croisé est interne au
  pack — l'icône du texte de chaque carte correspond à la couleur du coin des
  autres cartes (ex. Uke Nagashi cite le poing ; Vigilant, dont le coin est un poing
  rouge, cite les nœuds). Mapping retenu : tl002 G, tl003 Y, tl004 R, tl005 B,
  tl006 G, tl007 B, tl008 B, tl009 Y, tl010 B, tl011 R, tl012 Y. Reste à vérifier
  en partie (Q9).
- Icône « ! » en étoile de Foot Patrol = **Crisis 1** (comparée visuellement à
  01108 Crowd Control : même glyphe, même place, mêmes 2 icônes de boost).
  « 2 [personne] » = `StartingThreat "2*"`.
- Icônes rouges en forme de « Y » (boost) : Foot Patrol 2, obligation 2, Foot
  Soldiers 1 ; Karai porte seulement l'ÉTOILE (★ Boost), aucune icône chiffrée →
  pas de `desc.Boost`. (Comparé à ls012, même glyphe en bas à droite.)
- Astérisque d'allié : Splinter ATQ/CTR « 2 + icône étoile creuse » = dégâts
  consécutifs (`"2*"`), confirmé par le texte de Taichō « consequential damage
  ([consequential]) ».
- PV minions : Karai 2, Foot Soldiers 1 (pastille orange).

## 5. Questions en attente (8)

Format : carte, texte imprimé, options (la recommandée en premier).

### Q1 — Cloak (tl015 Karai x2, tl016 Foot Soldiers)
Textes : « **When Revealed**: Cloak Karai. » / « **When Defeated**: Cloak the
villain. » / « **When Revealed**: Cloak Foot Soldiers. »
Aucune définition sur les scans ni sur l'insert ; mot inconnu du moteur.
1. **(recommandée) Donner la règle imprimée par l'auteur** (livret TMNT / scénarios) ;
   en attendant le stub `Cloak()` ne fait rien : les 3 cartes entrent en jeu sans
   effet. Un seul point de code à remplir
   (`leonardo_nemesis/__init__.py`), plus la fiche `mots-cles/cloak.md`.
2. Arbitrer « Cloak = carte intouchable (ne peut être ciblée/attaquée) jusqu'à son
   activation » : change en jeu : Karai et les Soldiers deviennent des sbires
   « cachés » difficiles à tuer ; le When Defeated de Karai rend le VILAIN
   intouchable (très fort).
3. Arbitrer « Cloak = Tenace/Stalwart-like » (statut protecteur sans ciblage
   impossible) : moins radical, mais pas dans le texte.
4. Autre (précise).

### Q2 — Octroi d'aptitude par Leonardo's Katana (tl011, accessoirement tl012)
Texte : « Each [[KATANA]] upgrade you control gains: "**Hero Resource**: Exhaust
this card → generate a [wild] resource for an identity-specific card." »
1. **(recommandée) Chaque katana porte sa propre ressource** : tl011 la porte ;
   tl012 la porte SOUS CONDITION que tl011 soit en jeu sous votre contrôle.
   Identique en jeu pour les deux katanas du pack ; ne couvre pas un katana d'un
   autre pack (inexistant à ce jour). C'est le montage écrit.
2. Vrai octroi (`GiveKeywordToInPlayWhenApplyThis(..., abilities=[...])`) :
   aucune carte joueur du dépôt ne le fait (non testé, risque de plantage à la
   construction), mais fidèle au texte pour tout futur katana.
3. tl012 génère toujours sa ressource, même sans tl011 : plus fort que l'imprimé.
4. Autre (précise).

### Q3 — Yo Ko Giri (tl006) : « paid with [energy][mental][physical] resources »
Texte : « If you paid for this card with [energy][mental][physical] resources,
you may return this card to your hand. »
1. **(recommandée) Au moins une ressource de CHAQUE couleur** (`HasColor` x3) ; la
   carte coûte 3 : donc exactement une de chaque, un wild converti compte
   éventuellement pour une couleur (comportement du moteur).
2. Trois ressources imprimées non-wild de couleurs différentes : refuse le wild
   (plus strict).
3. N'importe quel paiement d'au moins une de ces trois couleurs : plus permissif.
4. Autre (précise).

### Q4 — Iaijutsu (tl008) : « If this attack defeats an enemy, draw 1 card »
Aucune fabrique « cette attaque défait » pour un événement joué depuis la main.
1. **(recommandée) Approximation par `PlayerStat.kill_counter`** : on pioche si le
   joueur a mis K.O. au moins une unité pendant la résolution de l'événement joué.
   Écart : compte aussi un K.O. causé hors attaque par cet événement.
2. Hook exact sur l'attaque de l'événement (modif moteur, plus long) : fidèle.
3. Ne pas rendre la pioche (stub) : plus faible que l'imprimé.
4. Autre (précise).

### Q5 — Brainwashed Betrayal (tl013) : portée de trois phrases
Texte : « Flip to hero form and discard an ally you control. You cannot attack
the villain. **Forced Response**: After your turn begins, deal 3 damage to an
ally. »
1. **(recommandée) Lecture littérale** : bascule en forme de héros OBLIGATOIRE ;
   défausse d'un allié DU joueur (au choix) ; « cannot attack the villain » tant
   que l'obligation est en jeu (les sbires restent attaquables) ; les 3 dégâts
   visent N'IMPORTE QUEL allié en jeu (choisi par le joueur).
2. Les 3 dégâts ne visent que les alliés du joueur (plus dur pour lui, plus
   cohérent avec « Give to the Leo player »).
3. « Cannot attack the villain » seulement jusqu'à la fin du round.
4. Autre (précise).

### Q6 — Foot Patrol (tl014) : aucun sbire FOOT CLAN trouvé
Texte : « When Defeated: Search the encounter deck and discard pile for a [[FOOT
CLAN]] minion and put it into play engaged with the first player. »
1. **(recommandée) Rien ne se passe si aucun n'est trouvé** (lecture littérale).
2. Révéler la carte du dessus du deck Rencontre à la place : ajout hors texte.
3. Autre (précise).
Note : c'est le premier joueur qui fouille (`Search.EncounterCard(..., premier)`).

### Q7 — Insert « Katana Weapon Rules » : l'afficher ?
Les 4 puces de l'insert sont rendues par les scripts (tl001b, tl011, tl012,
tl008). La feuille elle-même n'est pas une carte.
1. **(recommandée) Ne rien créer** (comme les inserts des autres packs, règles
   dans les cartes).
2. Créer une carte `Insert` (`tl017`, image de l'insert) consultable en jeu.
3. Autre (précise).

### Q8 — Icônes de ressource (confirmation rapide)
Voir §4 : mapping tl002 G, tl003 Y, tl004 R, tl005 B, tl006 G, tl007 B, tl008 B,
tl009 Y, tl010 B, tl011 R, tl012 Y, déduit de RECETTES §8 et des icônes citées
dans les textes. 1. **(recommandée) Valider en jeu** (une carte de chaque couleur
payée par une ressource de cette couleur) ; 2. m'envoyer la décklist des
ressources imprimée.

## 6. Capacités à tester (phase C), par card_id

Rappel : chaque capacité distincte = un cas `tools/test_capacites.py` + preuve par
substitution ; limite imprimée = témoin d'épuisement ; bonus continu d'identité =
contre-cas dans l'autre forme (RECETTES §3).

- **tl001a** Kenjutsu : redresse une arme WEAPON contrôlée (cible = amélioration
  inclinée, 1 cas) ; **témoin d'épuisement** « Limit once per round » (2e usage
  même round : refusé, chiffre = arme toujours inclinée) ; contre-cas : arme déjà
  prête non ciblable.
- **tl001b** Leo : coût défausse 1 carte ; 2 katanas du deck/défausse mis en jeu
  inclinés (un depuis le deck, un depuis la défausse) ; « up to 2 » (0 ou 1 trouvé) ;
  deck mélangé ; cas sans carte en main (non proposée).
- **tl002** Splinter : Response à l'entrée ; carte `Hero` de la défausse sur le
  dessus du deck ; défausse sans carte spécifique : non proposée ; ATQ/CTR 2* =
  1 dégât consécutif (attaque ET contre).
- **tl003** Uke Nagashi : +2 DEF pour CETTE attaque (mesure : dégâts subis) ; payé
  avec [physical] (`R`) → Leonardo prêt à la fin ; payé sans physique → pas prêt ;
  vérifier qu'il se déclenche à la DÉFENSE de Leonardo (pas sur un défenseur allié).
- **tl004** Vigilant : −3 menace ; payé avec [mental] → un katana redressé ; sans
  mental → aucun ; aucun katana incliné → pas de question.
- **tl005** Stoicism : Leonardo redressé ; payé [energy] → katana redressé ; sans.
- **tl006** Yo Ko Giri : 5 dégâts perçants (contre cible Tenace : status défaussé) ;
  payé énergie+mental+physique → choix de la remettre en main ; autre paiement →
  pas de choix ; refus (« Decline »).
- **tl007** Greenhouse : coût (inclinée + défausse) ; pioche 2 ; soigne 2 de
  l'identité ; non utilisable en forme de héros ; sans carte en main.
- **tl008** Iaijutsu : déclencheur « un ennemi initie une attaque » (vilain ET sbire) ;
  coût = incliner un KATANA (et PAS Iaijutsu) ; événement ATTACK à Hero Action
  de la main joué en payant son coût ; événement non-ATTACK ou sans Hero Action
  non proposé ; K.O. → pioche 1 (et cas sans K.O. : pas de pioche).
- **tl009** Taichō : Action (incliner un katana → se redresser) uniquement quand
  Taichō est inclinée ; Response (allié subit des dégâts consécutifs → Taichō
  s'incline → allié redressé) ; allié vaincu par ces dégâts : aucune erreur ; allié
  Tenace (dégâts empêchés) : pas de déclenchement.
- **tl010** Nukitsuke : s'incline → redresse un katana incliné ; aucun katana
  incliné : non proposée.
- **tl011** Katana : Hero Resource → wild pour une carte `Hero` (et PAS pour une
  carte d'aspect) ; non utilisable en alter-ego ; Restricted (2 max).
- **tl012** Other Katana : coût = incliner 2 katanas ; +1 ATQ/CTR/DEF/REC jusqu'à
  la fin du round (cible héros, allié, autre joueur) ; ressource wild SEULEMENT si
  tl011 en jeu (contre-cas : absente sans tl011).
- **tl013** Brainwashed Betrayal : bascule forcée en héros ; défausse d'un allié
  (aucun allié : rien) ; impossible d'attaquer le vilain mais possible d'attaquer un
  sbire ; Forced Response 3 dégâts à un allié après le début du tour ; Action
  d'alter-ego : coût exhaust + 2 dégâts → retirée du jeu.
- **tl014** Foot Patrol : Crisis (menace du complot principal non retirable tant qu'il
  est en jeu) ; menace de départ 2 par joueur ; When Defeated : un sbire FOOT CLAN
  du deck/défausse Rencontre mis en jeu engagé avec le PREMIER joueur (2 joueurs :
  ≠ celui qui a vaincu) ; aucun sbire : rien.
- **tl015** Karai : When Revealed et When Defeated appellent `Cloak` (STUB : cas =
  « n'explose pas ») ; ★ Boost : la carte part chez le PREMIER joueur comme carte
  Rencontre face cachée (pas à la défausse) ; pas d'icône de boost chiffrée.
- **tl016** Foot Soldiers : When Revealed appelle `Cloak` (stub) ; Boost 1.
- **Pack** : `verifier_tous_les_decks` (deck `leonardo` jouable : asserts de
  construction, notamment AlterEgoAction/HeroAction sur tl001a/tl001b et plusieurs
  capacités par carte sur tl008/tl009/tl012), autoplay ≥ 8 parties avec témoin,
  partie complète à la main, `test_cards`, `verifier_appels_modules` (calibré),
  survol du héros dans le wizard (bio `tl001a`), tooltip FR de chaque carte.

⚠ Risques de construction à surveiller dès la première partie (aucun script n'a
été exécuté) : `CostFunc.Exhaust(..., range=(2, 2))` (tl012), `conditions=` sur
`CanGenerateResources` (tl012), `SetTarget(check_fn=..., from_where=["YourHandCards"])`
combiné à un coût (tl008), `AfterAllyTakeConsequentialDamage` avec `Ally` nu (tl009),
`PlayersCannotAttackWhile("You", CardFinder(card_type=Villain))` sur une obligation
(tl013), deux `ForChoiceAbility` dans un `ChooseAbilities` dont une « Decline » (tl006).

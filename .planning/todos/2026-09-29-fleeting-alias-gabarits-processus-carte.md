# Fleeting et Alias (pack `determination`) : gabarits PROCESSUS-CARTE

Date : 29/09/2026. Origine : les fiches `docs/reference/mots-cles/fleeting.md`
et `alias.md`, écrites le même jour après l'audit des règles fan-made contre
MC4DB, ont trouvé deux défauts : Fleeting n'était implémenté nulle part, et
Alias était inerte parce que les quatre porteurs avaient un `subtitle` vide.

Le pack `determination` n'avait AUCUN cas au harnais avant ce jour (ses decks
d'aspect ont été supprimés le 05/09/2026, les cartes restent dans
`cards.json` et dans l'éditeur). Les 7 cas ajoutés portent le filtre `[dt]`.

Harnais : dossier de jeu dédié `.game-src-fa` (copie de `.game-src`, liens
symboliques), port 47100, jamais de batterie complète (d'autres agents
tournaient en même temps). `.game` non touché.

⚠ Piège vu en passant : dans la passe groupée AVANT correctif, `dt100` et
`dt107` sont sortis VERTS alors que, rejoués SEULS, ils étaient rouges
(`dt100 n'est pas en jeu ; 33019 est encore en jeu`). Un enchaînement de cas
sur le même dossier peut donc laisser un état qui fausse le suivant. Règle
tenue : tout rouge ou vert surprenant se rejoue seul avant conclusion.

## dt087 : "Get 'Em, Boom-Boom!"

- [x] Étape 2 : carte de référence : `44032` The Merc with the Mouth
      (`WhenPlayerPhaseEnd` + `DiscardThisCard`) : comparable parce que c'est
      une défausse de soi-même déclenchée par une fin de phase ; `dz005`
      Beauty and the Beast pour `WhenPhaseEnd` sur une carte déjà en jeu.
- [x] Étape 5 : texte-contre-code : « at the end of the phase » (la phase
      COURANTE, pas la fin du round : `phase_name=None`, première fin de
      phase après l'entrée en jeu) ; « must be discarded » (ForcedResponse,
      pas optionnelle) ; « when this card would be discarded from attached
      enemy » (l'Interrupt existant écoute `WhenCardWouldDiscard`, que
      `Faces.DiscardAll` émet via `DiscardInternal`, `card.py:635`) ; « each
      enemy in play » (Rhino ET le sbire mesurés).
      Résultat : `Fleeting()` ajoutée dans `determination/__init__.py`, posée
      en tête de `dt087.py` ; commentaire mensonger (« lu par le moteur dans
      le texte ») corrigé. Condition `IsInPlay()` : une carte en main ne se
      défausse pas.
- [x] Étape 6 : nombres : 1 dégât par ennemi (Interrupt existant, inchangé) ;
      coût 0 (`desc.Cost` 0, pas de mise en jeu ordinaire, voir commentaire).
- [x] Étape 7 : cas `dt087 Get 'Em, Boom-Boom! [dt] — Fleeting : defaussee a
      la fin de la phase, et son Interrupt inflige 1 degat a chaque ennemi en
      partant` (vérificateur `dt087_fleeting_fin_de_phase`, envoie
      `Message.WhenPhaseEnd(monde.phase_id, "Player", monde)` comme
      `kb_bow_fin_de_phase`). ROUGE avant : « dt087 est encore en jeu apres
      WhenPhaseEnd ». VERT après : « degats (0, 0) -> (1, 1) ».
      Témoin `— reste attachee a Rhino tant que la phase n'est pas finie`
      (`accroche_a`, dégâts 0) : vert avant et après, contre-cas assumé.
      Substitution : voir « Substitution » en bas.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay ciblé : NON FAIT. Le pack n'a plus de deck de départ
      (supprimés le 05/09/2026), donc aucun deck à donner à `autoplay.py`
      sans en inventer un (interdit, mémoire « pas de deck inventé »).
- [x] Étape 8 bis : la carte change ce qu'on VOIT (attachée puis défaussée).
      Cas plateau : NON FAIT. L'attachement d'une amélioration à un ennemi
      est déjà dessiné par le plateau pour des dizaines de cartes ; la
      défausse retire la carte de la table. Aucun nouveau motif de dessin.

Carte terminée : NON : autoplay impossible sans deck ; tout le reste est
prouvé.

## dt105 * Venompool, dt100 * Archangel, dt106 * Captain Universe, dt107 * Zenpool (Alias)

- [x] Étape 2 : carte de référence : `bl002` (Blade) et `08002`
      (`ReduceCostToPlayThis` sous condition) ; pour la défausse à l'entrée en
      jeu, `01083` Mockingbird (`AfterCardEnterPlay` Response "This").
- [x] Étape 5 : texte-contre-code : « a card with a matching subtitle »
      (`paper.subtitle`, égalité stricte, hors la carte elle-même) ; « you
      control » (`GetControlCards()` de l'initiateur) ; « discard it »
      (UN homonyme, `homonymes[:1]`) ; « play this card for free » (réduction
      égale au coût imprimé).
      Résultat : les sous-titres imprimés, lus sur les scans
      `assets/pics/dt100.jpg`, `dt105.jpg`, `dt106.jpg`, `dt107.jpg` :
      Archangel = « Warren Worthington III » ; Venompool, Captain Universe,
      Zenpool = « Wade Wilson » (Captain Universe est bien la version
      Deadpool). Renseignés dans `data/cards.json`, checksum recalculé
      (`tools/recalculer_checksums.py`, `c34c6102...` -> `8c591703...`).
      ⚠ SECOND DÉFAUT, trouvé par le harnais une fois les sous-titres en
      place : `lambda effect: effect.this.printed_cost` rendait l'objet
      `Cost`, et la fabrique multiplie (`base_val * fn(effect)`) :
      `TypeError: unsupported operand type(s) for *: 'int' and 'Cost'`,
      avalée par le moteur (visible seulement dans `/tmp/capacites_*.log`).
      Corrigé en `.val` (comme `50081`, `50082`).
- [x] Étape 6 : nombres : réduction = coût imprimé (3, 3, 4, 2 :
      `printed_cost.val`) ; un seul homonyme défaussé.
- [x] Étape 7 : quatre cas sujets `dtNNN ... [dt] — Alias : gratuit quand
      <homonyme> est controle, et <homonyme> est defausse`, main vidée puis
      la seule carte (`main_exclusive`) : elle ne peut entrer en jeu qu'à
      coût zéro. Homonymes : `dt016` Deadpool (Wade Wilson, même pack),
      `33019` Angel (Warren Worthington III, pack cyclops), `40024` Deadpool
      officiel (Wade Wilson). ROUGE avant, chacun rejoué seul : « dtNNN n'est
      pas en jeu ; <homonyme> est encore en jeu ». VERT après : 7/7.
      Témoin `dt105 — sans homonyme controle, pas de gratuite, la carte reste
      en main` : vert avant et après, contre-cas assumé.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay : NON FAIT, même raison que dt087 (pas de deck).
- [x] Étape 8 bis : rien de nouveau à dessiner (un allié entre en jeu, un
      autre part en défausse : motifs déjà couverts).

Cartes terminées : NON pour l'autoplay (pas de deck) ; tout le reste prouvé.

## Substitution (`tools/substituer_pack.py .game-src-fa 47100 dt`)

⚠ Lancé d'abord sur le PACK ENTIER (`dt`) : 142 modules, le port avance de
60 par module (`PAS_DE_PORT`), donc après 35 modules le port sort de la
plage admise et tout le reste sort « rapport illisible ». Sur un pack de
cette taille, lancer l'outil CARTE PAR CARTE (`... 47100 dt087`), ce qui a
été fait pour les cinq cartes :

| Carte | Verdict |
|---|---|
| dt087 | rouges 1/2 : le cas Fleeting tombe ; le témoin « reste attachée avant la fin de phase » reste vert, contre-cas assumé |
| dt100 | rouges 1/1 |
| dt105 | rouges 1/2 : le cas Alias tombe ; le témoin « sans homonyme, reste en main » reste vert, contre-cas assumé |
| dt106 | rouges 1/1 |
| dt107 | rouges 1/1 |

`git status` propre après la passe (stubs restaurés). Dossier de jeu
`.game-src-fa` supprimé à la fin.

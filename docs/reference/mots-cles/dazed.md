# Dazed (carte d'état maison, pack TMNT, Baxter Stockman v3)

**Texte imprimé** (scan Inkwire, `Dazed (1).png` du zip « TMNT Enemies / Baxter
Stockman v3 », avec l'insert `Dazed Rules Insert.png`) : « The next time this
character uses a basic power or activates, decrease that value by 2, then discard
this status card. The next time this character would take any amount of damage,
increase that value by 2, then discard this status card. »

Traduction retenue : « La prochaine fois que ce personnage utilise un pouvoir de
base ou s'active, diminuez cette valeur de 2, puis défaussez cette carte d'état.
La prochaine fois que ce personnage va subir des dégâts, quelle qu'en soit la
quantité, augmentez cette valeur de 2, puis défaussez cette carte d'état. »
Nom français de l'interface : **Hébété** (« Daze » = « hébétez » ; ⚠ « étourdi » est interdit par la gate `vocabulaire-statuts.test.ts`, qui le réserve à une mauvaise traduction de Stunned = Sonné).

**Ce que dit l'insert** (« Dazed Rules ») :
- un personnage ne peut porter qu'**une** carte Dazed, sauf mention contraire ;
- Steady et Stalwart n'y changent rien (on peut hébéter un personnage Steady
  ou Stalwart ; Steady ne permet pas d'en porter deux) ;
- **un seul effet, le premier qui arrive**, comme Cloaked : « If I defend with a
  Dazed status card, do I get the −2 DEF, and also increase the damage by 2? No. »
  Et « consequential damage resolves last : la carte réduit d'abord l'ATQ/CTR
  de l'allié, puis part avant les dégâts consécutifs » ;
- **Tough résout avant Cloaked, Cloaked et Dazed résolvent en même temps** ;
- « Dazed + Stunned, attaque » : le personnage tente d'attaquer et retire la
  carte Stunned à la place (Dazed reste).

**Mécanisme moteur** : l'état est une vraie carte, recette identique à
`cloaked.md` (la fiche de la carte jumelle, dont Dazed est l'envers).

| Endroit | Ce qu'il a fallu |
|---|---|
| `data/cards.json`, pack `status` | `{"card_id": "dazed", "type": "Status", "name": "Dazed"}` + checksum |
| `CardFace.STATUS` (`card_face.py`) | `"Dazed"` ajouté au `Literal` |
| `StatusCard.symbol_name` (`card_type/card_status.py`), `Symbol` (`render/symbol.py`) | `dazed` |
| `Status.dazed` (`component/status.py`) | `DAZED_FINDER` + la propriété de comptage |
| `CanStatus` (`attribute/can_status.py`) | `dazed`, `IsDazed`, `DiscardDazed`, `HasStatus("Dazed")`, `has_status="Any"`, `DiscardEachStatus`, et la limite « UNE seule » dans `GainStatus` |
| `checker.py`, `ability.py` | `has_status` reconnaît Dazed ; `SetTarget(name="Dazed")` vise une carte d'état |
| `Puzzle.Daze` (`puzzle/puzzle.py`, `puzzle_.py`) | poser l'état dans un cas de test, comme `Puzzle.Cloak` |
| `src/cards/pack/status/dazed.py` | la capacité (trois déclencheurs, un seul consommateur), modèle `cloaked.py` |
| `cloaked.py` | cède la place à Dazed sur les dégâts (voir ci-dessous) |
| UI | `etats.ts` (lettre H, « Hébété »), `effets-statuts.ts` (badge), type de `ScanCard.tsx`, scan `assets/textures/dazed.webp` |

**Lecture des mots du texte imprimé (tranchée dans `dazed.py`)** :
- « uses a basic power » = `WhenUnitUseBasicPower` (ATQ, CTR, DEF, REC), −2 par
  `message.GainValue(-2)` ; « activates » = ennemi qui s'active (attaque ou
  manigance), exclu de la première branche pour ne pas compter deux fois.
- « would take any amount of damage » = `WhenUnitWouldTakeDamage` avec au moins
  1 dégât : `message.IncreaseDamage(2)` (y compris l'excès d'un overkill : le
  personnage subit réellement ces dégâts).
- **Tough d'abord** : la capacité de dégâts ne part pas si le personnage porte
  Tough (sauf perçant : `ignore_tough`) ni si les dégâts sont déjà remplacés ; la
  carte Dazed RESTE.
- **Cloaked et Dazed en même temps** : sur des dégâts, `dazed.py` prend la main,
  fait +2 puis −2 d'un bloc et défausse LES DEUX cartes ; `cloaked.py` lui cède
  la place (condition `pas_dazed`), sinon Cloaked retirerait 2 avant que Dazed
  n'ajoute 2 et le total serait faux (1 dégât → 1 subi, pas 2). Sur un pouvoir de
  base les deux modifications s'additionnent d'elles-mêmes.

**Carte exemple** : `ta002` Nobody et `ta003` Bold Strategy posent Dazed (fiche
`daze.md`) ; le pack Baxter Stockman (autre agent) s'en sert aussi.

**Pièges connus** :
- Dazed ne s'empile pas (une par personnage) : contrairement à Cloaked.
- `Puzzle.Daze` est une BASCULE (poser/retirer) : pour tenter une seconde pose, un
  cas appelle `Faces.GiveStatus` lui-même (cas `dazed_unique`).
- Ordre des états (Tough, puis Cloaked/Dazed ensemble) : couvert par les cas
  `[dazed] Tough résout d'abord` et `[dazed] Cloaked + Dazed`.
- « Dazed + Stunned » (attaque d'ennemi, la carte Stunned part seule) : suit le
  comportement de Cloaked ; non couvert par un cas dédié.

**Variantes maison** : aucune.

**Preuves** : `tools/cas/dazed.py` (18 cas, dont 4 témoins et la preuve par
substitution du module `dazed.py`).

# Dazed (Hébété) et « daze »

**Texte imprimé / définition** : carte d'état maison du scénario Baxter Stockman
(scan Inkwire `Dazed (1).png`, encart `Dazed Rules Insert.png`, zip « TMNT
Enemies / Baxter Stockman v3 ») : « The next time this character uses a basic
power or activates, decrease that value by 2, then discard this status card.
The next time this character would take any amount of damage, increase that
value by 2, then discard this status card. » Verbe de carte : « daze X » = poser
une carte Dazed sur X. Nom français : **Hébété** (verbe « hébétez »).

**Règles de l'encart** (font loi, codées) :
- sauf mention contraire, **une seule carte Dazed par personnage** ; Steady et
  Stalwart n'y changent rien (« Can I Daze a steady/stalwart character? Yes. ») ;
- deux déclencheurs, **un seul consommateur** : le premier qui arrive (pouvoir de
  base ou activation / dégâts à subir) applique son effet puis la carte part ;
- **Tough résout avant Cloaked, et Cloaked et Dazed résolvent SIMULTANÉMENT** ;
- Dazed -2 sur un pouvoir de base ou une activation d'ennemi (minimum 0) ;
  +2 aux dégâts « quelle qu'en soit la quantité » (au moins 1) ;
- défense : -2 DEF, puis la carte part AVANT les dégâts en excès (pas de +2) ;
- allié à dégâts consécutifs : l'ATQ/CTR baisse, la carte part, les dégâts
  consécutifs (qui résolvent en dernier) ne sont donc PAS augmentés ;
- perforant : Tough part avant les dégâts, Dazed ajoute alors ses +2.

**Mécanisme moteur** : sixième carte d'état du moteur, recette identique à
Cloaked (`cloaked.md`) :

| Endroit | Ce qu'il a fallu |
|---|---|
| `data/cards.json`, pack `status` | `{"card_id": "dazed", "type": "Status", "name": "Dazed"}` + checksum |
| `CardFace.STATUS` (`card_face.py`) | `"Dazed"` |
| `StatusCard.symbol_name`, `Symbol` | `dazed` |
| `Status.dazed` (`component/status.py`) | `DAZED_FINDER` + compteur |
| `CanStatus` (`attribute/can_status.py`) | `dazed`, `IsDazed`, `CanbeDazed` (un seul), `DiscardDazed`, `HasStatus("Dazed")`, `GainStatus` refuse un second, `DiscardEachStatus` |
| `checker.py`, `ability.py` | `has_status` / `canbe_status` reconnaissent Dazed |
| `Puzzle.Daze` (`puzzle.py`, `puzzle_.py`) | poser l'état dans un cas de test |
| `src/cards/pack/status/dazed.py` | la capacité (trois déclencheurs, un seul consommateur) ; MÊME hooks que `cloaked.py` |
| UI | `effets-statuts.ts`, `mobile/etats.ts` (lettre H, « Hébété »), `ScanCard.tsx`, texture `assets/textures/dazed.webp` |

**Simultanéité avec Cloaked** : un Cloaked puis un Dazed pris l'un après l'autre
donneraient autre chose (1 dégât : Cloaked seul → 0, le Dazed ne se déclenche plus ;
pris ensemble 1 - 2 + 2 = 1 et les deux cartes partent). `cloaked.py` s'efface donc
(`pas_de_dazed`) devant un Dazed du même porteur et `dazed.py` résout le LOT : somme
des effets de tous les Cloaked du porteur et du Dazed, puis toutes ces cartes
défaussées. Tough d'abord : si le porteur a une carte Tough qui va absorber (pas de
perforant), ni Dazed ni Cloaked ne sont consommés.

**Carte exemple** : `tx016` Wrapped Up (« Daze a friendly character. If you cannot,
this card gains surge »), `tx005` Baxter Blaster, `tx015` Roadkill Rodneys.

**Pièges connus** :
- `Faces.GiveStatus(..., "Dazed", effect)` rend le NOMBRE de personnages réellement
  hébétés : c'est ce retour qui porte « If you cannot » (tx016) ; ne pas déclarer le repli
  en cible légale ;
- `Puzzle.Daze` BASCULE (pose, puis retire au second appel) comme `Puzzle.Tough` : pour
  prouver « un seul Dazed », passer par `Faces.GiveStatus` (cas `bx_deux_dazed`) ;
- la ligne `compter` de `effets-statuts.ts` liste chaque statut en dur : un statut absent
  de `compter` donne `NaN` et le badge ne part jamais (trouvé par le cas
  `effets-statuts.test.ts`, 16/10/2026) ;
- non mesuré : l'ordre exact d'un Dazed et d'un Tough quand l'attaque est PERFORANTE (le
  moteur défausse Tough avant les dégâts, `can_attack.py` ; le cas de l'encart « 1 dégât
  perforant → 3 dégâts » n'a pas de cas).

**Variantes maison** : aucune.

**Preuves** : `tools/cas/tmnt_baxter.py` (cas `[dazed]`, 21), preuve par substitution
de `dazed.py` dans le rapport `.planning/tmnt/baxter-phase-a.md`.

# Exposed (carte d'état maison, pack `sentinel`)

**Texte imprimé** (`Exposed Status.png`) : « The next time this character is
attacked, discard all Exposed status cards from it. That attack deals 1
additional damage for each Exposed status card discarded this way. »

Traduction retenue : « La prochaine fois que ce personnage est attaqué,
défaussez toutes ses cartes d'état Exposé. Cette attaque inflige 1 dégât de
plus par carte d'état Exposé défaussée ainsi. »

**Ce que c'est** : une **quatrième carte d'état**, à côté de Coriace, Sonné et
Désorienté. Le moteur n'en connaissait que trois.

**Mécanisme moteur** : l'état est une vraie carte, comme les trois autres.

| Endroit | Ce qu'il a fallu |
|---|---|
| `data/cards.json`, pack `status` | une carte `{"card_id": "exposed", "type": "Status", "name": "Exposed"}`, jumelle des trois autres |
| `CardFace.STATUS` (`src/game/card/face/card_face.py`) | `"Exposed"` ajouté au `Literal` |
| `StatusCard.symbol_name` (`card_type/card_status.py`) | l'entrée `"Exposed": Symbol.exposed` |
| `Symbol` (`src/game/render/symbol.py`) | `exposed` |
| `Status.exposed` (`card/face/component/status.py`) | la propriété de comptage, jumelle de `confused`/`stunned`/`tough` |
| `CanStatus.exposed` et `HasStatus` (`attribute/can_status.py`) | sans quoi `HasStatus("Exposed")` tombait sur `assert False`, et `has_status="Any"` ignorait le quatrième état |
| `Puzzle.Expose` (`game/puzzle/puzzle.py`) | poser l'état dans un cas de test, comme `Puzzle.Tough` |
| `src/cards/pack/status/exposed.py` | la capacité de la carte, `AbilityType.Status` sur `"AttachedCharacter"`, modèle `tough.py` |

Un état se pose par `face.GainStatus("Exposed", effect)`
(`attribute/can_status.py:67`) et se retire par `LoseState`. **Exposé
s'empile** : contrairement à Coriace, `GainStatus` ne lui oppose aucun plafond
(`tough_max`), ce qui est voulu — « 1 dégât de plus **par carte** ».

**Carte exemple** : `st002a` Head (Intact) — « Hero Action: Exhaust Head
(Intact) → expose 2 enemies. » Voir aussi `st006` Exterminate (expose 2
ennemis après ses 7 dégâts), `st013` Targeting Protocol, et les deux cartes qui
**comptent** les Exposé en jeu : `st007` Hardwire Access et `st013`.

**Pièges connus** :

- **« Est attaqué » n'est pas « subit des dégâts ».** L'état se déclenche sur
  l'attaque, pas sur la source de dégâts : une carte qui inflige des dégâts
  sans attaquer ne le consomme pas.
- **Tout part d'un coup, et les dégâts se cumulent** : deux Exposé sur la même
  cible font +2, et les deux cartes s'en vont ensemble.
- **Les Exposé du plateau se comptent partout**, pas seulement sur la cible :
  `st007` et `st013` lisent « the number of Exposed status cards **in play** ».
- **Un état posé sur un ennemi vaincu part avec lui** : le décompte peut
  changer entre le moment où le joueur choisit sa carte et celui où elle se
  résout.
- **Le plateau les dessine déjà, mais PAS gratuitement.** `Board.tsx` sépare
  bien les cartes `kind === 'status'` des améliorations, et `etats.ts` a un repli
  générique qui aurait affiché un « E ». Trois endroits devaient quand même être
  mis à jour, sans quoi le quatrième état était muet ou anglais :
  `ETATS` dans `etats.ts` (nom français « Exposé », classe propre),
  `Statut` / `STATUTS` / `libelleStatut` dans `effets-statuts.ts` (sans quoi
  **aucun badge** n'annonçait la pose ni le retrait), et le type
  `CardEffectDelta` dans `ScanCard.tsx`. Plus le scan
  (`assets/textures/exposed.webp`, à côté de `tough.webp`).
- **Le décompte « in play » se lit sur les PERSONNAGES** :
  `Worlds.GetOnFieldCharacters` puis `components.status.exposed`. Le helper
  `ExposedEnJeu` du pack `sentinel` est le seul endroit qui le fait.

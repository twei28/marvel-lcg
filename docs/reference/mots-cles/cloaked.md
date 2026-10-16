# Cloaked (carte d'état maison, pack TMNT, Shredder v3)

**Texte imprimé** (scan Inkwire, `Cloaked.png` du zip « TMNT Enemies / Shredder v3 ») :
« The next time this character uses a basic power or activates, increase that
value by 2, then discard this status card. The next time this character would
take any amount of damage, decrease that value by 2, then discard this status
card. »

Traduction retenue : « La prochaine fois que ce personnage utilise un pouvoir de
base ou s'active, augmentez cette valeur de 2, puis défaussez cette carte d'état.
La prochaine fois que ce personnage va subir des dégâts, quelle qu'en soit la
quantité, diminuez cette valeur de 2, puis défaussez cette carte d'état. »
Nom français de l'interface : **Camouflé**.

**DÉCISION DE L'UTILISATEUR (16/10/2026)** : **un SEUL effet**, le premier qui
arrive : soit +2 au prochain pouvoir de base / à la prochaine activation, soit
−2 aux prochains dégâts subis (minimum 0), puis la carte est défaussée. Une carte
Cloaked ne sert qu'une fois. (Le texte imprimé, lu à la lettre, pourrait se
comprendre « deux effets, deux défausses » : l'utilisateur a tranché.)

**Ce que c'est** : une carte d'état de plus, à côté de Coriace, Sonné, Désorienté
(et Exposé du pack `sentinel`). Elle est posée par le mot-clé « Cloak X » (fiche
`cloak.md`) : `tl015` Karai, `tl016` Foot Soldiers, `td005` Improvised Tactics.

**Mécanisme moteur** : l'état est une vraie carte, comme les autres. Recette
identique à `exposed.md` :

| Endroit | Ce qu'il a fallu |
|---|---|
| `data/cards.json`, pack `status` | une carte `{"card_id": "cloaked", "type": "Status", "name": "Cloaked"}` + checksum (`tools/recalculer_checksums.py`) |
| `CardFace.STATUS` (`card_face.py`) | `"Cloaked"` ajouté au `Literal` |
| `StatusCard.symbol_name` (`card_type/card_status.py`) | l'entrée `"Cloaked": Symbol.cloaked` |
| `Symbol` (`render/symbol.py`) | `cloaked` |
| `Status.cloaked` (`component/status.py`) | `CLOAKED_FINDER` + la propriété de comptage |
| `CanStatus` (`attribute/can_status.py`) | `cloaked`, `IsCloaked`, `DiscardCloaked`, `HasStatus("Cloaked")`, `has_status="Any"`, et `DiscardEachStatus` (« défaussez chaque carte d'état ») |
| `checker.py`, `ability.py` | `has_status` reconnaît Cloaked ; `SetTarget(name="Cloaked")` vise une carte d'état |
| `Puzzle.Cloak` (`puzzle/puzzle.py`, `puzzle_.py`) | poser l'état dans un cas de test, comme `Puzzle.Tough` |
| `src/cards/pack/status/cloaked.py` | la capacité (trois déclencheurs, un seul consommateur), `AbilityType.Status`, modèle `tough.py` |
| UI | `etats.ts` (lettre K, « Camouflé »), `effets-statuts.ts` (badge de pose/retrait), type `CardEffectDelta` de `ScanCard.tsx`, scan `assets/textures/cloaked.webp` |

**Lecture des mots du texte imprimé (tranchée dans `cloaked.py`)** :

- **« uses a basic power »** = `WhenUnitUseBasicPower` : ATQ, CTR, DEF **et REC**
  (les quatre pouvoirs de base du moteur, `ability_type.py:48`, même lecture que
  `sk011`, `tg009`, `tg016`). La DÉFENSE est donc un pouvoir de base (aucun texte
  des règles du dépôt ne l'exclut, au contraire : `tg016` et `sk011` le notent).
  Le bonus de +2 passe par `message.GainValue`, qui route lui-même vers
  `GainATKForThisAttack`, `GainDEFForThisAttack`, `GainTHWForThisThwart` ou
  `GainRECForThisRecover`.
  Observation : une défense de héros à +2 ne se voit que si l'attaque dépasse la
  DEF de base ; le cas de test mesure donc l'ATQ et le CTR (mesurables sans
  ambiguïté), le chemin DEF/REC est le même `GainValue`.
- **« activates »** = un ENNEMI qui s'active (`WhenEnemyActivateAgainstYou`, qui ne
  porte `would_act_message` que pour une vraie activation), attaque (ATQ +2) ou
  manigance (MNG +2). Un ennemi qui attaque passe aussi par `WhenUnitUseBasicPower` :
  ce branchement-là exclut les ennemis (condition `pas_ennemi`), sinon le +2 serait
  compté deux fois.
- **« would take any amount of damage »** = `WhenUnitWouldTakeDamage` avec au moins
  1 dégât (le défaut de la fabrique : zéro dégât n'est pas « une quantité »).
  −2, au minimum 0 (`PreventDamage(min(2, dégâts))`) ; la carte est défaussée
  même si l'effet a réduit moins de 2 (il a eu lieu).
- **« then discard this status card »** : `Faces.DiscardAll([this], effect)`, la
  carte elle-même (pas « une carte Cloaked »).

**Carte exemple** : `tl016` Foot Soldiers (« When Revealed: Cloak Foot Soldiers »),
`td005` Improvised Tactics (« Cloak two friendly characters »).

**Pièges connus** :

- **Un seul effet** : le premier déclencheur qui arrive défausse la carte, les
  autres ne la trouvent plus. Cas de test dans les deux sens.
- **UNE seule carte Cloaked par personnage, sauf mention contraire** (encart du scénario Shredder, 16/10/2026 :
  « Normally characters can only have one Cloaked status card on them at a time, but the Shredder can have more
  than one, depending on his villain stage »). `CanStatus.cloaked_max` = 1 + le retour de
  `Message.GettingUnitAdditionalCloaked` ; `AbilityFactory.ThisCanHaveAdditionalCloaked(N)` (Shredder I/II/III :
  N = 1/2/3, donc 2/3/4 cartes). « Cloak X » sur un X déjà au maximum ne pose rien (`GainStatus` rend False) : c'est
  le « If you cannot » de `ts020` Foot Rikugun. REMPLACE l'ancienne note « Cloaked s'empile (aucun plafond) ».
  Plusieurs cartes sur Shredder : chacune agit UNE fois (insert : 3 Cloaked + une activation = +6 ; 3 dégâts d'une
  attaque retirent 2 cartes ; 3 attaques de 1 dégât en retirent 3). Cas : `tools/cas/tmnt_shredder.py` (« encart Q&R »).
- **Coriace d'abord** (encart : « Tough status cards always resolve before cloaked status cards »). Une cible qui porte
  Coriace ET Cloaked : Coriace absorbe tout, le Cloaked RESTE ; avec une attaque PERÇANTE la Coriace part d'abord,
  puis le Cloaked prévient 2 (cas « encart Q&R » : les deux ordres de pose).
- **Le +2 d'activation se joue sur la valeur utilisée** : il est ajouté AVANT les
  cartes de boost, comme tout `GainATKForThisAttack` (même mécanisme que Retaliate
  ou une amélioration d'ennemi).
- **Les statuts Stunned / Confused / Tough** restent intacts : Cloaked ne touche
  qu'à ses propres hooks (cas Stunned/Confused/Tough/Exposé relancés verts).

**Preuves** (`tools/cas/cloaked.py`, 13 cas, tous avec témoin ou preuve par
substitution : le module retiré, les 8 cas de comportement échouent et les 5
témoins/poses passent) ; les cas des cartes qui posent Cloaked :
`tools/cas/cloaked_cartes.py` (tl015 ×2, tl016, td005).

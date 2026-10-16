# Baxter Stockman v3 (TMNT, Inkwire) : le scénario

Pack `baxter_stockman`, prefixe de card_id `tx`, set n°195 (provisoire, voir `.planning/tmnt/baxter-phase-a.md`).
Source : zip « TMNT Enemies / Baxter Stockman v3 » (Inkwire : « TMNT Villains » et « TMNT Modulars »). 19 card_id
pour 42 exemplaires numerotes, plus la carte d'etat DAZED (`dazed`, set `status`).

| card_id | Carte | Set de rencontre | Exemplaires |
|---|---|---|---|
| tx001 / tx002 / tx003 | * Baxter Stockman I / II / III (vilain) | scenario | 1 chacun |
| tx004a / tx004b | Baxter's Laboratory (manigance principale 1A / 1B, le SPECIAL « Replicate ») | scenario | 1 |
| tx005 | * Baxter Blaster (attachement) | baxters_lab | 1 |
| tx006 | Swarm Superiority (attachement) | baxters_lab | 2 |
| tx007 | Plague of M.O.U.S.E.R.S. (sbire) | baxters_lab | 4 |
| tx008 | Radical Ingenuity | baxters_lab | 3 |
| tx009 | Rapid Replication | baxters_lab | 3 |
| tx010 | Robotics Facility (manigance annexe) | baxters_lab | 3 |
| tx011 | Mad Lab (manigance annexe) | baxters_lab | 2 |
| tx012 | Flight of Flyborgs | cyber_swarm | 3 |
| tx013 | * Superfly | cyber_swarm | 1 |
| tx014 | Buzz Off | cyber_swarm | 2 |
| tx015 | Roadkill Rodneys | high_speed | 3 |
| tx016 | Wrapped Up | high_speed | 2 |
| tx017 | Auto Defense Bots | security_protocol | 4 |
| tx018 | Intruder Alert! | security_protocol | 3 |

Scenario : `data/scenarios/baxter_stockman.json` (Baxter I et II ; sets `baxters_lab`, `cyber_swarm`, `standard` ; modulaires
`high_speed` et `security_protocol`) et `baxter_stockman_expert.json` (Baxter II et III ; + `expert`).
**A la fusion : remplacer `standard` par `tmnt_standard` et `expert` par `tmnt_expert` dans les deux fichiers** (ensembles
habilles TMNT crees par un autre agent, prefixe `te`).

Mecaniques : etat DAZED (`mots-cles/dazed.md`), Special « Replicate » (`replicate.md`), compteurs nommes des essaims
(`swarm.md`, `all-purpose-counter.md`), Cloaked / Dazed simultanes (`cloaked.md`). Homonyme : `td015` « * Baxter Stockman »
est le SBIRE nemesis de Donatello ; toujours chercher par card_id.

Preuves : `.planning/tmnt/baxter-gabarits-processus-carte.md` (un gabarit par carte), `.planning/tmnt/baxter-phase-a.md`.

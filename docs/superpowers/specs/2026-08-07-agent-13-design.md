# Pack Agent 13

Spec écrite le 07/08/2026. Le pack est fourni en 23 scans, dans
`Agent 13-20260807T065416Z-1-001.zip` à la racine du projet. Auteur : Rainy,
Marvel Champions Custom Project, Cycle 2, le même que les packs `spider_man_rainy`
et `venom_rainy` déjà livrés.

Le mode d'emploi de référence reste `GUIDE-CREATION-CONTENU.md`, dont le §5
donne la checklist d'un nouveau héros. Cette spec ne le réécrit pas : elle
enregistre ce qui est propre à Agent 13.

## 1. Ce qu'on livre

Un héros jouable de bout en bout : identité à deux faces, 15 cartes signature,
set némésis de 5 cartes, obligation, deck de départ, images, biographie, textes
français, et une partie réelle jouée.

Tranche de `card_id` : **79xxx**. Vérifiée libre dans `data/cards.json` comme
dans `src/cards/pack/`, y compris contre les paquets d'une session parallèle.

## 2. Décisions prises

| Question | Décision | Pourquoi |
|---|---|---|
| Où travailler | Côté Windows, dans `Fusion/marvel-lcg-src/`, puis pousser vers la copie WSL après chaque étape | Écart assumé au §5 du guide, qui dit l'inverse. Le sens WSL vers Windows a effacé deux fois du travail le 7/8/2026, et une session parallèle écrit dans la même copie |
| Aspect du deck de départ | Agression | 8 de ses 15 cartes signature portent une ressource physique, son pouvoir de héros la réactive pour attaquer encore, et Burst Fire, Takedown et le Pistolet sont trois attaques |
| Branche git | Nouvelle branche `pack-agent-13`, partie de l'état courant | `campagne-cablage` reste intacte en attendant sa fusion |
| Suivi git | Les fichiers du pack sont ajoutés à git | `src/cards/` n'est pas suivi, et c'est ce qui a rendu invisibles douze régressions le 7/8/2026 |

## 3. Les cartes

### Identité

| id | Face | Chiffres |
|---|---|---|
| `79001a` | Agent 13, Hero | THW 2, ATK 1, DEF 2, main 5, 9 PV |
| `79001b` | Sharon Carter, AlterEgo | REC 3, main 6, 9 PV |

Traits communs : S.H.I.E.L.D. SPY.

### Signature, 9 distinctes en 15 exemplaires

| id | Nom | Ex. | Type | Coût |
|---|---|---|---|---|
| `79002` | Captain America | 1 | Ally unique, 2 THW / 2 ATK / 5 PV | 3 |
| `79003` | Burst Fire | 3 | Event | 2 |
| `79004` | Infiltrate | 3 | Event | 2 |
| `79005` | Parting Shots | 2 | Event | 1 |
| `79006` | Takedown | 2 | Event | 0 |
| `79007` | Briefing Room | 1 | Support | 2 |
| `79008` | Agent 13's Pistol | 1 | Upgrade | 2 |
| `79009` | Physical Training | 1 | Upgrade | 2 |
| `79010` | Secret Agent | 1 | Upgrade | 2 |

### Némésis, 4 distinctes en 5 exemplaires, plus l'obligation

| id | Nom | Ex. | Type |
|---|---|---|---|
| `79011` | Assassination Plot | 1 | Side Scheme |
| `79012` | Doctor Faustus | 1 | Minion, SCH 3 / ATK 1 / 3 PV |
| `79013` | Hallucination | 1 | Attachment |
| `79014` | Hypnotic Suggestion | 2 | Treachery |
| `79015` | Sleeper Agent | 1 | Obligation |

Les textes imprimés de chaque carte sont relevés dans le scratchpad de session,
fichier `agent13/releve-cartes.md`, et doivent être recopiés dans `cards.json`
depuis ce relevé, jamais de mémoire.

## 4. Les sept cartes techniques

Sept cartes ne se copient sur aucun modèle existant. Le point d'accroche du
moteur a été vérifié pour chacune AVANT d'écrire cette spec : aucune ne demande
d'ajout au moteur.

| Carte | Ce qu'elle demande | Ce qui existe |
|---|---|---|
| `79001a` Agent 13 | réagir à un pouvoir de base, se réactiver, attaquer | `AbilityFactory.AfterUnitUseBasicPower`, avec son filtre `powers=` |
| `79001b` Sharon Carter | choisir dans la défausse de rencontre, remettre sur le deck, retirer de la menace égale aux icônes | `Faces` et `MoveToTop`, puis `FacesCounter.CountTotalBoostIcons` |
| `79004` Infiltrate | regarder la carte du dessus, compter ses icônes, la défausser au choix | modèle : `src/cards/pack/scw/scarlet_witch/15004.py` |
| `79005` Parting Shots | interruption avant l'attaque d'un ennemi, puis bascule optionnelle en alter-ego | `ChangeToForm` sur l'identité, **jamais `ChangeForm` qui n'existe pas** |
| `79008` Agent 13's Pistol | défausser la carte du dessus, dégâts égaux aux icônes défaussées | `Worlds.DiscardEncounterCards` puis `CountTotalBoostIcons` |
| `79012` Doctor Faustus | intouchable sous condition, et retourner un allié contre son héros | `message.PreventDamage("All", effect)` pour l'immunité |
| `79013` Hallucination | défausser jusqu'à un sbire, le révéler, s'y attacher | `Worlds.DiscardEncounterCards` en boucle, puis `AttachTo2` |

`79014` Hypnotic Suggestion emploie `GainStatus("Confused", ...)`, et `79015`
Sleeper Agent retire une carte du jeu par `Faces.MoveAllTo(..., world.area_removed, ...)`.

**Compter les icônes de bonus est la mécanique du pack** : elle revient sur
trois cartes, l'identité alter-ego, Infiltrate et le Pistolet. C'est aussi le
défaut le plus probable et le plus silencieux : une carte qui rendrait toujours
zéro se construirait sans erreur et passerait `test_cards`.

## 5. La preuve

Les quatre outils du §8 du guide, sur le pack `agent_13` :
`test_cards.py`, `verifier_api_cartes.py`, `verifier_coherence_cartes.py`,
`test_capacites.py`.

**En plus, un cas de comportement dédié pour chacune des sept cartes du §4.**
`test_cards` prouve qu'une carte se construit, pas qu'elle fait quelque chose.
Pour les trois cartes qui comptent des icônes de bonus, le cas doit montrer une
valeur NON NULLE relevée sur une carte de rencontre connue : c'est le seul
moyen de distinguer « ça marche » de « ça rend zéro ».

Deux pièges connus du harnais, à garder en tête en écrivant les cas :
le pilote décline les `MayChooseOneAbility`, sauf avec la clé
`accepter_choix: True` ; et cette clé n'agit que pendant le déclenchement, jamais
pendant la mise en place.

Enfin, une partie complète jouée avec le héros, comme l'exige le §5.9 du guide.

## 6. Hors périmètre

Aucun scan français : le pack est fourni en anglais, et les textes français
demandés par le §5.8 du guide sont des traductions écrites à la main dans
`ui-app/src/board/textes-fr-fanmade.ts`, pas des images.

Aucun scénario, aucun set modulaire : Agent 13 est un héros, sa némésis ne se
joue que par l'obligation.

## 7. Risques

**Une carte inerte ne lève aucune erreur.** Le moteur construit sans broncher
une capacité qui ne fait rien, et `test_cards` la déclare bonne. D'où le §5.

**Doctor Faustus retourne un allié contre son héros**, ce qu'aucune carte du
dépôt ne fait. Si le montage résiste, la question se pose à l'utilisateur en
multichoix plutôt que d'être tranchée seul, comme le veut le §4.1 du guide.

**La copie WSL peut écraser `src/`.** Une session parallèle y travaille. Pousser
après chaque étape, et vérifier `git status` avant chaque reprise.

**Le moteur exécute `.game`, pas `src/`.** Reconstruire après chaque édition,
sans quoi toute mesure porte sur le code précédent.

# PRÉ-PORTAGE — Iron Man (Model 42) (Rainy)

**Statut : dossier de préparation. AUCUN fichier du moteur n'a été touché.**
Zip : `Iron Man (Model 42)-20260902T073854Z-1-001.zip`, 19 images,
**15 cartes distinctes**. Difficulté : **2/5**.

## 1. Identité du pack

| Champ | Valeur proposée |
|---|---|
| Préfixe | `im` (vérifié libre le 02/09) |
| Numéro de set | `149` |
| Libellé | `149. Custom (Iron Man Model 42)` |
| `set_name` héros | ⚠ **`Iron Man` est PRIS** (`01029a`), et `Tony Stark` est déjà porté deux fois (`01029b`, `si001b`). Voir §5 Q1. |
| `set_name` némésis | **sans objet**, pas de set némésis. Voir §5 Q2. |
| Dossier | `src/cards/pack/iron_man_model_42/...` |

## 2. Inventaire, texte imprimé relevé sur les scans

Numérotation `IRON MAN (n/15)` : 15 exemplaires, **12 cartes signature
distinctes**, plus 2 faces d'identité, 1 obligation et 1 carte alternative.

| card_id | n/15 | Nom | Type | Coût | RES | Traits | Texte imprimé |
|---|---|---|---|---|---|---|---|
| `im001a` | — | ★ Iron Man | Hero | — | — | AVENGER. | THW 2 / ATK 2 / DEF 2 / HS 5 / PV 10. *Reactor Cores* — **Action**: Spend X printed ⚡ resources → place X reactor counters here. |
| `im001b` | — | ★ Tony Stark | AlterEgo | — | — | GENIUS. | REC 3 / HS 6 / PV 10. *Inventor* — **Setup**: Discard 1 card from your hand → search your deck for a TECH upgrade and add it to your hand. **Action**: Reduce the cost of the next upgrade played this round by 1. (Limit once per round.) |
| `im002` | 1, 2 | Repulsor Barrage | Event | 2 | ⚡ | ATTACK. SUPERPOWER. | **Hero Action** *(attack)*: Deal 3 damage to an enemy. This attack gains ranged. You may remove 1 reactor counter from Iron Man to deal 3 additional damage to that enemy. If Iron Man has the AERIAL trait, you may divide damage among enemies as you choose. |
| `im003` | 3, 4 | Tactical Overview | Event | 2 | 🧠 | SUPERPOWER. THWART. | **Hero Action** *(thwart)*: Remove 3 threat from a scheme. You may remove 1 reactor counter from Iron Man to remove 3 additional threat from that scheme. If Iron Man has the AERIAL trait, you may divide threat removed from among schemes as you choose. |
| `im004` | 5, 6, 7 | Take Flight | Event | 1 | ⚡ | SUPERPOWER. | **Hero Action**: Ready Iron Man. Iron Man gains the AERIAL trait until the end of the round. If Iron Man already has AERIAL, place 1 reactor counter on Iron Man. |
| `im005` | 8 | ★ Stark Tower | Support | 3 | ⭐ | LOCATION. | **Resource**: Exhaust Stark Tower → generate a ⭐ resource for any player. |
| `im006` | 9 | ★ Tony's Workshop | Support | 1 | 💪 | LOCATION. | **Alter-Ego Action**: Exhaust Tony's Workshop → heal 1 damage from Tony Stark and place 1 reactor counter on him. |
| `im007` | 10 | Energy Shield | Upgrade | 2 | ⚡ | TECH. | Iron Man gets +1 DEF. **Hero Interrupt**: When Iron Man would take any amount of damage, remove 1 reactor counter from him → prevent up to 2 of that damage. |
| `im008` | 11 | ★ Mark IVa Repulsors | Upgrade | 1 | ⚡ | TECH. WEAPON. | **Hero Interrupt**: When Iron Man makes a basic attack, remove 1 reactor counter from him → that attack deals 2 additional damage and gains ranged. |
| `im009` | 12 | ★ Repulsor Core One | Upgrade | 2 | ⚡ | TECH. | **Hero Action**: Exhaust Repulsor Core One → place 1 reactor counter on Iron Man. **Hero Action**: Remove 1 reactor counter from Iron Man and exhaust Repulsor Core One → ready Iron Man. |
| `im010` | 13 | Rocket Boots | Upgrade | 1 | 💪 | ARMOR. TECH. | Iron Man gains the AERIAL trait. **Hero Interrupt**: When you use one of Iron Man's basic powers, exhaust Rocket Boots → Iron Man gets +1 to that power for this use. |
| `im011` | 14 | Save The Day | Upgrade | 1 | ⚡ | PREPARATION. | **Hero Interrupt**: When a treachery is revealed, discard Save The Day and remove 1 reactor counter from Iron Man → cancel all of that treachery's effects and discard it. |
| `im012` | 14b | ★ Hulkbuster Armor | Upgrade | 2 | 💪 | ARMOR. TECH. | Iron Man gets -1 hand size, +1 ATK and DEF and his basic attacks gain overkill. **Interrupt**: When Iron Man would take any amount of damage, remove this card from the game → prevent all of that damage. ⚠ **Donnée comme « alternative replacement for Save The Day »**, voir §5 Q4. |
| `im013` | 15 | Tactical Interface | Upgrade | 1 | 🧠 | TECH. | **Hero Interrupt**: When Iron Man makes a basic thwart, remove 1 reactor counter from him → that thwart removes 2 additional threat and ignores the patrol keyword. |
| `im014` | — | Technical Issues | Obligation | — | — | — | *Give to the Tony Stark player.* You may flip to alter-ego form. Choose: • Exhaust Tony Stark and Tony's Workshop → remove Technical Issues from the game. • Remove 2 reactor counters from your identity. If no reactor counters were removed this way, this card gains surge. Discard this obligation. |

> Les 15 cartes ont été lues sur les scans, une par une, le 02/09/2026.
> Icônes de ressource lues à vue : à vérifier contre une carte du même pack.

## 3. Étape 2 du PROCESSUS-CARTE, pré-remplie

Une seule économie porte tout le pack : le compteur `reactor`, posé par
`im001a`, `im004`, `im006`, `im009`, et dépensé par `im002`, `im003`, `im007`,
`im008`, `im011`, `im013`, `im014`. **10 des 15 cartes le lisent.**

| Capacité | Carte de référence | Pourquoi |
|---|---|---|
| Compteur nommé sur l'identité | `sd` (compteur `explosive`, Speed), `vp013` (compteur `adrenaline`, Venompool), `gb` (compteurs `plan`/`timer`/`necro`, Gorr) | Trois précédents maison récents, tous du même dépôt. Le compteur `reactor` s'ajoute de la même façon. |
| `im001a` « Spend X **printed** ⚡ resources » | recette §4 de `RECETTES-MOTEUR.md` : `FacesCounter.GetPrintedResources([face])`, modèles `21006`, `ho009` | Le mot **printed** est un piège : il exclut les ressources générées. Le tableau §4 signale que `res` est figé AVANT le `PayCost` (écart payé sur `ho009`). |
| `im001b` Setup « chercher une upgrade TECH et l'ajouter à la main » | `si001b` (Superior Iron Man) et `bt001b` (Beast) | Deux Setup maison déjà écrits sur la face alter-ego. |
| `im001b` « réduire le coût de la prochaine upgrade jouée ce round » | à chercher : famille réduction de coût | Voisin de la brique Blink (vague 3), mais ici sans condition de cible : plus simple. |
| `im007`, `im012` prévention de dégâts | `si` (Endo-Sym Armor), fiche `mots-cles/armored.md` **déjà écrite** | `im012` retire la carte DU JEU, pas de la partie en cours : vérifier la nuance. |
| `im011` annulation de traîtrise | `an005` Single Out (Angela) | Annulation d'un « When Revealed » déjà écrite en maison. |
| `im010`, `im004` octroi du trait AERIAL | `wd090` Wingsuit (Web of Deceit) | ⚠ Lire la leçon du 20/08 : `wd090` était **inerte**, l'octroi de trait avait été oublié. Carte témoin de ce piège précis. |
| `im013` « ignores the patrol keyword » | fiche `mots-cles/patrol.md` **déjà écrite** | — |
| `im014` « this card gains surge » | fiche `mots-cles/surge.md` **déjà écrite** | — |
| `im002`, `im003` « divide damage/threat among as you choose » | `58018` Everywhere All at Once (Wonder Man) : « Choose X schemes. Remove 2 threat from each » | Le plus proche trouvé ; la répartition libre est plus souple, à vérifier. |

## 4. Collisions de noms, vérifiées dans `data/cards.json`

| Nom | Collision | Conséquence |
|---|---|---|
| **Iron Man** | `01029a` Hero, `09039` Ally, `23002` Ally (War Machine, `Class=Hero`), `56059-61` Leader | — |
| **Tony Stark** | `01029b` AlterEgo (Iron Man), `si001b` AlterEgo (Superior Iron Man) | **Troisième** Tony Stark du jeu. |
| **Stark Tower** | `01034` Support set **Iron Man** `Class=Hero`, `56072` SideScheme | Signature d'un autre héros : `collision_note` obligatoire. |
| **Rocket Boots** | `01039` Upgrade set **Iron Man** `Class=Hero`, `56066` Attachment | Idem, et le texte diffère (`01039` donne +1 PV et coûte une ressource 🧠). |
| **Energy Shield** | `04073` Attachment, `52018` Upgrade | Pas de `Class=Hero`, risque faible. |
| **Save The Day** | `23018` Event | Pas de `Class=Hero`. |
| `set_name` **Iron Man** / **Iron Man Nemesis** | PRIS tous les deux | Voir Q1. |

Libres : Repulsor Barrage, Tactical Overview, Take Flight, Tony's Workshop,
Mark IVa Repulsors, Repulsor Core One, Hulkbuster Armor, Tactical Interface.
« Technical Issues » : **vérifié libre** le 02/09.

## 5. ⚠ Questions à poser AVANT d'écrire le premier script

**Q1 — Le `set_name`.** `Iron Man` est pris et `si` a déjà pris
`Superior Iron Man`.
- A) *(recommandé)* `Iron Man (Model 42)`, qui reprend le nom du zip et suit le
  modèle `Thor (Jane Foster)` déjà dans le dépôt.
- B) `Model 42`.
- C) Autre (précise).

**Q2 — Pas de set némésis** (1 obligation seule). Aucun des 111 decks de départ
du dépôt n'a de `nemesis_set` vide.
- A) *(recommandé)* Livrer sans set némésis.
- B) Emprunter celui de l'Iron Man officiel.
- C) Autre (précise).

**Q3 — L'aspect du deck de départ** (aucune decklist fournie).
- A) *(recommandé)* **Agressivité** : `im002` Repulsor Barrage, `im008` Mark IVa
  et `im012` Hulkbuster tapent fort, et c'est l'aspect du deck de départ de
  l'Iron Man officiel.
- B) **Protection** : `im007` Energy Shield, `im011` Save The Day et `im012`
  forment un vrai noyau défensif.
- C) **Justice** : `im003` et `im013` sont deux cartes de menée.
- D) Autre (précise).

**Q4 — `im012` Hulkbuster Armor, donnée comme « alternative replacement for
Save The Day ».** Les deux cartes portent le numéro 14/15. Le pack propose donc
un choix de deckbuilding, pas deux cartes cumulables.
- A) *(recommandé)* Créer les DEUX cartes avec deux `card_id` distincts, mettre
  `im011` Save The Day dans le deck de départ, et signaler `im012` dans la note
  du préfixe comme variante officielle du pack.
- B) Ne créer que Save The Day.
- C) Ne créer que Hulkbuster Armor.
- D) Autre (précise).

**Q5 — `im001a` « Spend X **printed** ⚡ resources ».**
Le mot « printed » exclut-il les ressources générées par `im005` Stark Tower et
par les cartes d'aspect ?
- A) *(recommandé)* Oui, littéralement : seules les cartes dont l'icône imprimée
  est ⚡ comptent. C'est ce que dit le texte, et c'est ce que la recette §4 sait
  faire (`GetPrintedResources`).
- B) Non, toute ressource ⚡ compte.
- C) Autre (précise).

## 6. Ce que ce dossier ne fait PAS

Identique aux autres dossiers de la vague 0 : aucune écriture dans les fichiers
partagés, aucun script, aucun test, aucune image, aucune bio, aucun texte FR.

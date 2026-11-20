# Infection (maison, scénario `the_hunger_core`, préfixe `hg`)

**Texte imprimé / définition** (livret officiel du scénario, page 5, relu mot à mot le 27/10/2026) :

- « Infection is a second health bar. It is tracked with a green counter next to your identity card. Each player
  starts at 0. »
- « **Infection.** When an attack from a Zombie or Metazombie enemy deals damage to your hero, place 1 Infection
  counter. »
- How you get Infection : « A bite: 1 counter for each attack from a Zombie or Metazombie that deals damage to your
  hero, however much damage it deals. If an ally defends, or if your DEF or a tough status card prevents all the
  damage, there is no Infection. » ; « Cards that add it directly: Bite, Widow's Bite, Hunger Pulse, Bloated Zombie,
  The Hunger Core (II) and (III) and any Trapped Survivor that is devoured. »
- How you remove it : « **Basic recovery:** choose between healing your REC in damage, as usual, or **removing 3
  Infection counters**. You cannot do both. » ; « Franklin Richards can remove 2 Infection counters. Cards that heal
  damage do not remove Infection. »
- Limit and death : « The limit is **7** in Standard and **6** in Expert. Changing form does not remove Infection. »
  ; « When you reach the limit, **your hero is defeated** and its zombie version enters play: if it is a Metazombie,
  at the right end of the row (unless there are already 3); if it is a *Fallen Heroes* minion, engaged with the next
  player; if your hero has no zombie version, put a Metazombie from the Horde deck into play. »
- Page 8 (Expert) : « the Infection limit drops to 6 ». Page 8 (Défaite) : « if every hero is defeated (by damage or
  by Infection) ». FAQ p. 8 : « My hero dies from Infection in a solo game. You lose: there are no heroes left. The
  zombie version only enters play if players remain, and its hit points use the starting number of players. »
- Page 6 (glossaire) : « Zombie version: The Metazombie or minion of a chosen hero. It is set aside during setup and
  only enters play if that hero dies from Infection. » Page 7, étape 3 : la liste des Metazombies (Captain America,
  Iron Man, Hulk, Spider-Man, Captain Marvel, Thor, Black Widow, Doctor Strange, Magik) ou un minion *Fallen Heroes*.

**Mécanisme moteur** (tout dans `src/cards/pack/the_hunger_core/commun.py`, branché par `ReglesDuScenario`,
porté par le Cœur, condition `coeur_en_jeu`) :

| Besoin | Brique |
|---|---|
| le compteur | `'infection'` dans `CardFace.COUNTER` ; posé sur `joueur.GetIdentity()` par `PoserInfection` ; il vit sur la CARTE (composant `Counter`), donc reste au changement de forme (même mécanisme que [[chi-counter]]) |
| morsure | `AfterUnitAttackAndDamageUnit(Scenario, ennemi ZOMBIE/METAZOMBIE, Hero, ...)` |
| limite 7 / 6 | `AbilityFactory.AfterCounterPlacedOn(Scenario, identité, 'infection', at_least=LimiteInfection)` (`Worlds.IsExpert`) ; modèle `sl072b` Creeping Corruption (seuil de compteurs -> `Faces.DefeatUnits([identité])`, qui élimine le joueur par `Identity.OnBeDefeated`) |
| version zombie | `MettreLaVersionZombieEnJeu` : Metazombie -> `_EntrerDansLaRangee` (même logique de jeton que `MettreUnMetazombieEnJeu`, max 3) ; minion Fallen Heroes -> `PutIntoPlay(joueur_suivant)` (le minion s'engage avec le joueur passé, `Minion.OnPutIntoPlay`) ; aucune -> `MettreUnMetazombieEnJeu` |
| récupération de base | `AbilityFactory.WhenUnitMakeRecovery(Scenario, alter-ego, ...)` + `ChooseAbilities` ; branche Infection = `message.SetBeInstead` (modèle `35030` Death Factor, `tg016` Chomped) puis retrait de 3 compteurs |

**Carte exemple** : aucune carte n'imprime la règle ; elle est codée dans `commun.ReglesDuScenario`. Cartes qui
posent l'Infection : hg002, hg003, hg037, hg049, hg051-hg055, hg057, hg058 ; qui la retirent : hg072 Franklin
Richards.

**Pièges connus** :
- `Puzzle.Counter` passe par `Faces.PlaceCountersOn` : il déclenche la limite comme une vraie pose. Un cas qui veut
  partir de « 6 compteurs » doit les poser AVANT d'atteindre le seuil (ou avant que le Cœur soit en jeu).
- Le joueur suivant se calcule AVANT la défaite : `Player.Eliminate` réordonne les joueurs.
- En solo, l'élimination termine la partie (`world.is_game_over`) : la version zombie n'entre pas (FAQ p. 8).
- « Its hit points use the starting number of players » : natif, l'icône par joueur lit `started_player_num`.
- La branche « retirer 3 Infection » remplace la récupération (`SetBeInstead`) : les réponses « après une
  récupération » (`AfterUnitRecovery`) ne partent pas dans cette branche (voir GABARITS, À CONFIRMER).
- Le choix n'est proposé que si l'identité porte au moins 1 compteur Infection (sinon il n'y a rien à choisir).

**Variantes maison** : aucune.

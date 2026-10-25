# The Vault (Kajislav) : gabarits PROCESSUS-CARTE, 27 card_id

Scénario `the_vault` (standard : vilains I ; expert : vilains II), préfixe `vt`, set 215. Source : zip « The Vault (Sealed) » déposé le 24/10/2026 (51 images :
16 vilains, complot principal, environnement, obligation, 17 cartes de rencontre dont 13 doublons, plateau et 8 compteurs de PV = accessoires de table, non codés).
Cas : `Fusion/marvel-lcg-src/tools/cas/the_vault.py`, `_b`, `_c`, `_d` (filtre `[vt]`). Plateau : `ui-app/src/board/the-vault-plateau.test.ts`.
Transcriptions : `docs/packs/vault/TRANSCRIPTIONS.md`. Recettes : `docs/reference/RECETTES-MOTEUR.md` §24. Fiche : `mots-cles/activation-order.md`.

## Arbitrages utilisateur du 25/10/2026 (questions posées carte montrée, scan à l'appui)

1. **The Vault (`vt018`)** : victoire ET défaite vraies en même temps (tous les vilains vaincus, aucun sous le Vault) = **VICTOIRE**.
2. **Corrupted Guardsman (`vt022`)** : « If you cannot, this card gains surge » couvre aussi l'absence d'Inspection en jeu : **sans Inspection, il gagne Surge**.
3. **Corrupted Guardsman (`vt022`)**, Boost : le sbire de sous le Vault mélangé dans le deck de rencontre est tiré **au hasard**.

## Décisions prises seules (texte sans ambiguïté ou règle du livret), à signaler

- **Inspection of the Vault** : `GiveTo` vaut `""` (donnée au joueur à qui on la révèle) ; ses deux sources la révèlent au premier joueur. `"first player"` la ferait retirer de la partie.
- **Un vilain vaincu est retiré de la partie** (livret p.1), sans rien reporter ; après le départ du dernier vilain on révèle le dessus du deck de vilains ; câblé sur `vt017b`.
- **Doublons du zip** (identiques au pixel près hors numéro) : Craven Escape 20-21, Corrupted Guardsman 22-25, Burglary 26-27, Rampage in Public 30-33, Riot in the Vault 34-36 : une carte, plusieurs exemplaires.
- **Noms de fichiers trompeurs** : « 28 backup plan » = Contingency Measures, « 30-33 enemy encounter » = Rampage in Public, « 34-36 cause a stir » = Riot in the Vault.
- **Icônes identifiées par les glyphes de `ChampionsIcons.ttf`** (jamais à vue) : Burglary = Crisis (C), Scheming from Within et Contingency Measures = Hazard (H), ressource d'Inspection = mentale (M, nœuds reliés).
- **Modulaire** : Sinister Syndicate (existant) par défaut ; mode expert = vilains (II) + ensemble `expert`.
- **Plateau de table et compteurs de PV** : accessoires de la boîte physique, non codés (le jeu a ses propres jauges).

## Gates du scénario

- [x] Étapes 1 à 8 : cartes (`cards.json`, 27 card_id, set 215), scripts (`src/cards/pack/the_vault/the_vault/`), scénarios standard et expert, ensemble de
      rencontre `the_vault`, `sets_info.json`, préfixe `vt` déclaré, images (`assets/pics/vt*.jpg`, non versionnées ; complot et manigances redressés), textes FR
      (`textes-fr-fanmade.ts` et `public/js/traduction/textes-fr-fanmade.js`), trait `TRAITOR` ajouté à l'enum.
- [x] Moteur (additif, sans effet hors de ce scénario) : `Villain.activation_order` (`desc.ActivationOrder`), `Villains.Rule(the_villain="LowestActivationOrder",
      activation_order=True)`, `Villains.ParOrdreDActivation`, `TopOfVillainDeck`, `ShuffleIntoVillainDeck`, `RevealNextVillain(reveal=True)`,
      `Enemies.ActivationVillainsParOrdre` (appelée par `World.VillainPhase` seulement si la règle est posée), `DoActivateAgainstYouInternal(villains=...)`,
      `Puzzle.SetVillainRule(..., activation_order)`, `Puzzle.RevealNextVillain(reveal)`. Fiche `mots-cles/activation-order.md`, recettes §24.
- [x] `test_cards.py` 7402 OK / 0 erreur ; `verifier_prefixes.py` OK ; `verifier_appels_modules.py the_vault` OK ; `audit_cartes.py` : 1 suspicion `vt029`
      « Boost » (faux positif : l'effet ★ passe par `WhenBoostIconsWouldBeCount`, prouvé par cas et substitution).
- [x] Cas : **83 cas `[vt]` verts** (socle 11, activation 9, vilains 39, rencontre 24) ; substitution : **27/27 cartes** avec au moins un cas rouge sans leur module ;
      les conditions de fin de partie (`VerifierFinDePartie`) calibrées ROUGE à part (3 cas tombent sans elles).
- [x] Plateau : `ui-app/src/board/the-vault-plateau.test.ts` 6/6, rendu générique suffisant.
- [x] Autoplay : 60 parties, 0 traceback.
- [x] `verifier_tous_les_decks.py` : **157/157 decks montent une partie** (fichiers partagés du moteur touchés : `enemies.py`, `world.py`, `villains.py`, `villain.py`).
- [ ] **Partie réelle jouée par un humain : NON FAITE** (lecture à l'écran de plusieurs vilains et des cartes sous The Vault, choix du vilain visé par une carte
      joueur, rythme du deck de vilains, équilibre du scénario : le pilote perd aussi contre Rhino, le taux de victoire de l'autoplay ne dit rien).
- Non couvert par un cas : un vilain qui ENTRE en jeu pendant l'étape 2 (règle « ordre supérieur au vilain qui vient d'activer », codée dans
  `ActivationVillainsParOrdre`).

### vt001 : Batroc (Villain)

```
* Batroc (I) — VILAIN, stade 1. Activation Order 1.
Forced Response: After you attack Batroc with a card you control, choose to either discard the top 3 cards of the encounter deck or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `Worlds.DiscardEncounterCards(3, effect)` (defausse du dessus du deck de rencontre).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - vt001 Batroc (I) : apres une attaque, branche A (discard the top 3 cards of the encounter deck)
      - vt001 Batroc (I) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt002 : Batroc (Villain)

```
* Batroc (II) — VILAIN, stade 2. Activation Order 1.
When Revealed: Each player discards the top 5 cards of their deck.
Forced Response: After you attack Batroc with a card you control, choose to either discard the top 3 cards of the encounter deck or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `Worlds.DiscardEncounterCards(3, effect)` (defausse du dessus du deck de rencontre).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt002 Batroc (II) : apres une attaque, branche A (discard the top 3 cards of the encounter deck)
      - vt002 Batroc (II) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      - vt002 Batroc (II) When Revealed : each player discards the top 5 cards of their deck
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt003 : Mentallo (Villain)

```
* Mentallo (I) — VILAIN, stade 1. Activation Order 2.
Forced Response: After you attack Mentallo with a card you control, choose to either exhaust your identity or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `Faces.ExhaustAll([identite], effect)`.
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - vt003 Mentallo (I) : apres une attaque, branche A (exhaust your identity)
      - vt003 Mentallo (I) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt004 : Mentallo (Villain)

```
* Mentallo (II) — VILAIN, stade 2. Activation Order 2.
When Revealed: Each player exhausts a character they control.
Forced Response: After you attack Mentallo with a card you control, choose to either exhaust your identity or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `Faces.ExhaustAll([identite], effect)`.
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt004 Mentallo (II) : apres une attaque, branche A (exhaust your identity)
      - vt004 Mentallo (II) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      - vt004 Mentallo (II) When Revealed : each player exhausts a character they control
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt005 : Grey Gargoyle (Villain)

```
* Grey Gargoyle (I) — VILAIN, stade 1. Activation Order 3.
Forced Response: After you attack Grey Gargoyle with a card you control, choose to either stun the attacker or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `Faces.GiveStatus(cibles, "Stunned", effect)` (modeles 05015 / 01083).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - vt005 Grey Gargoyle (I) : apres une attaque, branche A (stun the attacker)
      - vt005 Grey Gargoyle (I) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt006 : Grey Gargoyle (Villain)

```
* Grey Gargoyle (II) — VILAIN, stade 2. Activation Order 3.
When Revealed: Each player stuns a character they control.
Forced Response: After you attack Grey Gargoyle with a card you control, choose to either stun the attacker or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `Faces.GiveStatus(cibles, "Stunned", effect)` (modeles 05015 / 01083).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt006 Grey Gargoyle (II) : apres une attaque, branche A (stun the attacker)
      - vt006 Grey Gargoyle (II) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      - vt006 Grey Gargoyle (II) When Revealed : each player stuns a character they control
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt007 : Hydro-Man (Villain)

```
* Hydro-Man (I) — VILAIN, stade 1. Activation Order 4.
Forced Response: After you attack Hydro-Man with a card you control, choose to either deal 1 damage to each character you control or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `this.DealDamage(cibles, 1, effect)` (modele sk184, 27172).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - vt007 Hydro-Man (I) : apres une attaque, branche A (deal 1 damage to each character you control)
      - vt007 Hydro-Man (I) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt008 : Hydro-Man (Villain)

```
* Hydro-Man (II) — VILAIN, stade 2. Activation Order 4.
When Revealed: Deal 1 damage to each friendly character.
Forced Response: After you attack Hydro-Man with a card you control, choose to either deal 1 damage to each character you control or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `this.DealDamage(cibles, 1, effect)` (modele sk184, 27172).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt008 Hydro-Man (II) : apres une attaque, branche A (deal 1 damage to each character you control)
      - vt008 Hydro-Man (II) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      - vt008 Hydro-Man (II) When Revealed : deal 1 damage to each friendly character
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt009 : Mad Thinker (Villain)

```
* Mad Thinker (I) — VILAIN, stade 1. Activation Order 5.
Forced Response: After you attack Mad Thinker with a card you control, choose to either place 1 threat on each side scheme or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `this.PlaceThreatOnSchemes(manigances, 1, effect)` (modele sl004a ; `Worlds.GetAllSideSchemes`).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - vt009 Mad Thinker (I) : apres une attaque, branche A (place 1 threat on each side scheme)
      - vt009 Mad Thinker (I) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt010 : Mad Thinker (Villain)

```
* Mad Thinker (II) — VILAIN, stade 2. Activation Order 5.
When Revealed: Place 1 threat on the main scheme for each enemy in play.
Forced Response: After you attack Mad Thinker with a card you control, choose to either place 1 threat on each side scheme or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `this.PlaceThreatOnSchemes(manigances, 1, effect)` (modele sl004a ; `Worlds.GetAllSideSchemes`).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt010 Mad Thinker (II) : apres une attaque, branche A (place 1 threat on each side scheme)
      - vt010 Mad Thinker (II) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      - vt010 Mad Thinker (II) When Revealed : 1 threat on the main scheme for each enemy in play (le vilain + 2 sbires = 3)
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt011 : Nekra (Villain)

```
* Nekra (I) — VILAIN, stade 1. Activation Order 6.
Forced Response: After you attack Nekra with a card you control, choose to either give Nekra 1 facedown boost card or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `GiveFacedownBoostCardsInternal(1, effect, None)` (modele bw021 Imperius Rex).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - vt011 Nekra (I) : apres une attaque, branche A (give Nekra 1 facedown boost card)
      - vt011 Nekra (I) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt012 : Nekra (Villain)

```
* Nekra (II) — VILAIN, stade 2. Activation Order 6.
When Revealed: Give each villain 1 facedown boost card.
Forced Response: After you attack Nekra with a card you control, choose to either give Nekra 1 facedown boost card or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `GiveFacedownBoostCardsInternal(1, effect, None)` (modele bw021 Imperius Rex).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt012 Nekra (II) : apres une attaque, branche A (give Nekra 1 facedown boost card)
      - vt012 Nekra (II) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      - vt012 Nekra (II) When Revealed : give each villain 1 facedown boost card (Nekra II et un autre vilain deja en jeu)
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt013 : Vapor (Villain)

```
* Vapor (I) — VILAIN, stade 1. Activation Order 7.
Forced Response: After you attack Vapor with a card you control, choose to either confuse the attacker or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `Faces.GiveStatus(cibles, "Confused", effect)` (modeles 05015 / 01083).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - vt013 Vapor (I) : apres une attaque, branche A (confuse the attacker)
      - vt013 Vapor (I) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt014 : Vapor (Villain)

```
* Vapor (II) — VILAIN, stade 2. Activation Order 7.
When Revealed: Each player confuses a character they control.
Forced Response: After you attack Vapor with a card you control, choose to either confuse the attacker or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `Faces.GiveStatus(cibles, "Confused", effect)` (modeles 05015 / 01083).
 - When Revealed : `AbilityFactory.WhenThisRevealed(None, ...)` (modele ld002) ; l'effet est joue par CHAQUE joueur (`Worlds.GetPlayers`).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt014 Vapor (II) : apres une attaque, branche A (confuse the attacker)
      - vt014 Vapor (II) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      - vt014 Vapor (II) When Revealed : each player confuses a character they control
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt015 : Venom (Villain)

```
* Venom (I) — VILAIN, stade 1. Activation Order 8.
Forced Response: After you attack Venom with a card you control, choose to either heal 1 damage from him or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `this.HealthUnits([cible], 1, effect)` (modele 42018 Angel's Aerie).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - vt015 Venom (I) : apres une attaque, branche A (heal 1 damage from him)
      - vt015 Venom (I) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt016 : Venom (Villain)

```
* Venom (II) — VILAIN, stade 2. Activation Order 8.
Stalwart. Toughness. (natifs : desc.Stalwart et desc.Toughness, aucun module)
Forced Response: After you attack Venom with a card you control, choose to either heal 1 damage from him or place 1
  threat on the main scheme.

Cartes de reference :
 - « After you attack X ... choose to either A or B » : `ChoixApresAttaque` (helper du set) = `AfterUnitAttackUnit(ForcedResponse,
   "You", "This", ...)` (modele pu096) + `ChooseAbilities(ForChoiceAbility(A), ForChoiceAbility(B))` (modele OFFICIEL 04096b,
   gs136) ; « place 1 threat on the main scheme » : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (60148 Proxima).
 - Option A : `this.HealthUnits([cible], 1, effect)` (modele 42018 Angel's Aerie).

⚠ Mots-pieges : « you attack ... with a card you control » = l'ATTAQUANT du joueur (heros ou allie), le joueur qui a attaque choisit ;
« the attacker » = `message.attacker` (le personnage qui a attaque, pas l'identite) ; « each character you control » = personnages
du joueur qui a attaque (`GetControlCharacters`).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - vt016 Venom (II) : apres une attaque, branche A (heal 1 damage from him)
      - vt016 Venom (II) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : plusieurs vilains dessinés en même temps dans la zone des vilains. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt017a : The Vault Breakout (MainScheme)

```
The Vault Breakout (1A) — MANIGANCE PRINCIPALE, stade 1.
Contents: All villains (I) (stages (II) instead for expert mode). The Vault and Standard encounter sets. One modular
  encounter set (Sinister Syndicate).
Setup: Create the Villain deck (see insert). Put The Vault environment into play. Then, place the top 4 villain cards and
  each player's nemesis (✦) minion beneath it facedown. Set the Inspection of the Vault obligation aside, out of play.

Cartes de reference :
 - « Contents » : data/scenarios/the_vault*.json (aucun code, modele gs161a Earthfall).
 - « Create the Villain deck » : `Villains.SetRule` + `Villains.BuildVillainDeck` (brique du 20/10/2026, modele gs161a) ; la
   regle ajoutee ici (`the_villain="LowestActivationOrder"`, `activation_order=True`) rend « the villain » = le plus petit
   Activation Order (livret p.1) et distribue les activations par ordre (livret p.2, `Enemies.ActivationVillainsParOrdre`).
 - « Put The Vault environment into play » : `SetupCards.PutIntoPlay(name=..., card_type=Environment)` (modele gs161a
   Enemies at Large) ; « place ... beneath it facedown » : `CardFace.TuckCardUnderHere` (fiche mots-cles/tuck.md).
 - « Set the Inspection ... aside » : déjà de côté (cle `set_aside` du scenario) : rien a coder.

⚠ Mots-pieges : « the top 4 villain cards » = les 4 du DESSUS du deck de vilains (les 4 restants servent a la partie) ;
« each player's nemesis minion » = le sbire MARQUE nemesis du set de chaque joueur (`is_nemesis=joueur`), pas tout le set ;
un joueur sans sbire nemesis (set emprunte sans sbire marque) ne glisse rien.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (10 cas sujets) :
      - vt017a Setup (standard) : The Vault en jeu, 4 vilains SOUS le Vault, 1 vilain revele (1B), 3 dans le deck de vilains, Inspection de cote
      - vt-activation 2 vilains, 1 joueur : CHACUN active contre lui (Batroc 2 + Hydro-Man 2 = 4 degats)
      - vt-activation 2 vilains, 2 joueurs : le plus petit ordre (Batroc 1) contre le 1er joueur, l'autre (Mentallo 2) contre le 2e
      - vt-activation l'ordre n'est PAS l'ordre d'arrivee en jeu : Mentallo (2) revele AVANT Batroc (1), Batroc agit quand meme contre le 1er joueur
      - vt-activation 1 vilain, 2 joueurs : il active contre CHAQUE joueur (Batroc 2 + 2)
      - vt-activation 4 vilains, 2 joueurs (exemple du livret) : Batroc->J1, Mentallo->J2, Nekra->J1, Venom->J2 : J1 = 2+2, J2 = 1+2
      - vt-activation « the villain » d'une carte de rencontre = le plus petit Activation Order (Batroc 1 malgre Hydro-Man 4 revele avant)
      - vt-activation sbires, 3 vilains pour 2 joueurs (exemple du livret) : le sbire du 1er joueur active UNE fois, apres la 1re activation d'un vilain contre lui
      - vt-activation sbires, autant de vilains que de joueurs : le sbire du 1er joueur active apres SON vilain (J1 = Batroc 2 + sbire 1, J2 = Mentallo 1)
      - vt-activation FAQ : le vilain d'ordre 1 est etourdi, son activation est REMPLACEE par la carte d'etat ; le suivant (Mentallo 2) active contre le 2e joueur
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou déplace une carte déjà couverte par les cas plateau du Vault. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt017b : The Vault Breakout (MainScheme)

```
The Vault Breakout (1B) — MANIGANCE PRINCIPALE, stade 1. Menace de depart 1[per_hero], seuil 6[per_hero][star], escalade
  +1[per_hero].
When Revealed: Reveal the top card of the villain deck.
[star] Forced Interrupt: When this scheme would be completed, instead do each of the following:
  1. Remove all but 1[per_hero] threat from here.
  2. Reveal 1 random villain beneath The Vault.
  3. Reveal Inspection of the Vault.
(+ regle du livret p.1, non imprimee sur la carte : un vilain vaincu est retire de la partie, ses jetons, cartes d'etat et
  attachements sont defausses ; apres le depart du dernier vilain, on revele le dessus du deck de vilains.)

Cartes de reference :
 - « When this stage would be completed, ... instead » : `WhenMainSchemeStageWouldBeCompleted` + `message.SetBeInstead`
   (modele gs118b Majestrix's Verdict, sk145b) ; « remove all but N threat » : `RemoveThreatFromSchemes([this], n, effect,
   ignore_crisis=True)` (modele gs118b).
 - « Reveal 1 random villain beneath The Vault » : `RevelerAuHasardSousLeVault` (helper du set, `Card.Reveal`) ; « Reveal
   Inspection » : `SetupCards.Reveal(..., only_set_aside=True)` (Obligation donnee au premier joueur : `GiveTo` de vt019).
 - Retrait du vilain vaincu : `AfterUnitBeDefeated(ForcedResponse, Villain, ...)` + `Villains.Remove` (modele gs161b), puis
   `ApresDepartDUnMechant` (reveler le suivant, ou la victoire).

⚠ Mots-pieges : « all BUT 1 per hero » : on ne retire que l'exces, jamais sous 1[per_hero] ; le retrait du vilain vaincu est une
REPONSE, l'ordre des ecritures du livret p.1 ne change rien au resultat ; « if you cannot » absent : un tirage impossible (aucun
vilain sous le Vault) ne fait rien, et le Vault declare alors la DEFAITE (aucun vilain dessous).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (2 cas sujets) :
      - vt017b When Revealed : le dessus du deck de vilains est REVELE (1 en jeu, 1 reste au deck)
      - vt017b Interruption forcee (VRAIE mise en place) : menace accomplie -> la menace tombe a 1[per_hero], 1 vilain sous le Vault est REVELE, l'Inspection est donnee
      Preuve par substitution : **rouges 2/2** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou déplace une carte déjà couverte par les cas plateau du Vault. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt018 : The Vault (Environment)

```
* The Vault — ENVIRONNEMENT. LOCATION.
Forced Response: After a unique minion (✦) is defeated, place it beneath The Vault facedown.
If no villain is beneath The Vault, the players lose the game.
If all the villains are either beneath The Vault or defeated, the players win the game.

Cartes de reference :
 - « After a unique minion is defeated, place it beneath X facedown » : `AfterUnitBeDefeated(ForcedResponse, Minion, ...,
   conditions=[unique])` + `CardFace.TuckCardUnderHere` (fiche tuck.md ; helper `PoserSousLeVault`).
 - Les deux conditions de fin de partie (texte en gras, pas une capacite a declencheur) : `VerifierFinDePartie` (helper du
   set), appele a chaque changement d'etat qui les touche (mise en place, vilain sous le Vault, vilain vaincu, vilain
   melange dans le deck, revelation). Victoire : `Worlds.SetGameOver(True, effect)` (modele gs162a) ; defaite : `False`.

⚠ Mots-pieges : « unique minion (✦) » = `IsUnique()` (nom precede de « * ») ; « beneath » = la zone des cartes glissees du
Vault, FACE CACHEE ; victoire ET defaite vraies ensemble = VICTOIRE (arbitrage de l'utilisateur, 25/10/2026) ; « defeated »
= retire de la partie (livret p.1), donc plus en jeu et plus dans le deck de vilains.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (7 cas sujets) :
      - vt018 un SBIRE UNIQUE vaincu (Shocker) est glisse sous le Vault
      - vt018 contre-cas : un sbire NON unique vaincu (Hydra Mercenary) n'est PAS glisse sous le Vault
      - vt018 aucun vilain sous le Vault apres qu'un sbire unique y est glisse : les joueurs PERDENT
      - vt018 dernier vilain vaincu, deck de vilains vide, 1 vilain sous le Vault : les joueurs GAGNENT
      - vt018 dernier vilain vaincu et AUCUN vilain sous le Vault : victoire ET defaite vraies ensemble -> VICTOIRE (arbitrage du 25/10/2026)
      - vt018 vilain vaincu alors que le deck de vilains n'est PAS vide : le suivant est revele (livret p.1), pas de fin de partie
      - vt018 un vilain vaincu n'emporte RIEN a la suite : ses degats, attachements et jetons disparaissent avec lui
      Preuve par substitution : **rouges 2/7** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou des conditions de fin de partie portées par le helper `VerifierFinDePartie`, calibré ROUGE à part : trois cas tombent sans lui). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : l'environnement et les cartes glissées dessous (face cachée). Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt019 : Inspection of the Vault (Obligation)

```
Inspection of the Vault — OBLIGATION. « Give to the first player. »
Alter-Ego Action: Exhaust your identity and spend a [mental] resource → set this card aside, out of play.

Cartes de reference :
 - « Give to the first player » : `desc.GiveTo = ""` (modele 04163 Zola's Algorithm) : l'obligation va au joueur a qui elle est REVELEE ; ses deux
   seules sources (vt017b et vt034) la revelent toujours au PREMIER JOUEUR. `"first player"` ne marche pas : `Worlds.FindPlayerByName` le
   cherche comme un NOM de joueur, ne trouve rien et RETIRE l'obligation de la partie.
 - « Exhaust your identity and spend a [mental] resource → set this card aside » : `WhenInYourPlayTurn(AlterEgoAction, ...)`
   + `.SetCost(Cost("B"))` + `.SetCostFunc(CostFunc.Exhaust("YourIdentity"))` (modele 04163 Zola's Algorithm, qui DEFAUSSE) ;
   `Faces.SetAside([this], effect)` (modele ta011 Prey : de cote, hors jeu, et NON defaussee : Riot in the Vault et
   l'interruption de vt017b la retrouveront).

⚠ Mots-pieges : « [mental] » = `Cost("B")` (icone « noeuds relies » du scan, verifiee sur le glyphe M de ChampionsIcons.ttf) ;
« set aside » != « discard » ; « Alter-Ego Action » : utilisable seulement en forme alter-ego du joueur qui la porte ;
la carte n'a AUCUNE autre capacite : elle sert de DRAPEAU (« if Inspection is in play ») aux cartes de rencontre.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (1 cas sujets) :
      - vt019 Alter-Ego Action : epuise l'identite, depense une ressource mentale -> l'Inspection est MISE DE COTE (hors jeu, pas defaussee)
      Preuve par substitution : **rouges 1/1** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : obligation en jeu devant le premier joueur. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt020 : Craven Escape (Attachment)

```
Craven Escape — ATTACHEMENT, x2. 2 icones de boost.
Attach to the villain with the fewest remaining hit points and without another Craven Escape attached. If you cannot, this
  card gains surge.
Forced Response: After the player phase ends, shuffle attached villain into the villain deck.

Cartes de reference :
 - « Attach to the villain with the fewest remaining hit points ... If you cannot, this card gains surge » :
   `AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Villain, check_effect_fn=...), fewest_remaining_hp=True,
   if_cannot_gain_surge=True)` (modele gs163 Main Concern, qui prend « most » ; le filtre « sans autre Craven Escape » est la
   condition posee SUR LE CANDIDAT, comme son « plus d'un vilain »).
 - « After the player phase ends » : `AfterPhaseEnd(ForcedResponse, "Player", ...)` (modele gs161b, phase « Villain ») ;
   « shuffle attached villain into the villain deck » : `Villains.ShuffleIntoVillainDeck` (brique, 25/10/2026) puis
   `ApresDepartDUnMechant` (livret p.1 : apres le depart du dernier vilain, reveler le dessus du deck de vilains).

⚠ Mots-pieges : « WITHOUT ANOTHER Craven Escape attached » : le candidat n'a AUCUN autre exemplaire attache (la carte qui
se pose n'est pas encore attachee) ; « fewest REMAINING hit points » = PV restants, pas PV imprimes ; le melange emporte
les degats du vilain (la carte retourne dans le deck a PV pleins) ; l'attachement, lui, est defausse avec le reste.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (5 cas sujets) :
      - vt020 Craven Escape : s'attache au vilain qui a le MOINS de PV restants (Batroc 7-4 = 3 contre Hydro-Man 7)
      - vt020 Craven Escape : « WITHOUT another Craven Escape attached » : la 2e copie va sur l'AUTRE vilain (Batroc a deja la 1re)
      - vt020 Craven Escape : aucun vilain sans Craven Escape -> la carte gagne SURGE (le temoin est revele)
      - vt020 Craven Escape : apres la phase JOUEUR, le vilain attache est MELANGE dans le deck de vilains (degats effaces, l'autre vilain reste)
      - vt020 Craven Escape : le DERNIER vilain en jeu est melange puis aussitot revele (deck de vilains), a PV pleins
      Preuve par substitution : **rouges 5/5** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement de rencontre posé sur un vilain. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt022 : Corrupted Guardsman (Minion)

```
Corrupted Guardsman — SBIRE x4 (TRAITOR). ATK 3, SCH 1, PV 4, 1 icone de boost + ★. Incite 1.
When Revealed: If Inspection of the Vault is in play, reveal 1 random minion beneath The Vault. If you cannot, this card
  gains surge.
[star] Boost: Shuffle 1 minion beneath The Vault into the encounter deck.

Cartes de reference :
 - Incite 1 : natif (desc.Incite, fiche mots-cles/incite.md), aucun module.
 - « reveal 1 random minion beneath The Vault » : `RevelerAuHasardSousLeVault(effect, joueur, Minion)` (helper du set) ;
   « If you cannot, gains surge » : `ThisCardGainSurge` (modele gs189).
 - « [star] Boost: Shuffle 1 minion beneath ... into the encounter deck » : `WhenCardBecomeBoost("This", ...)` +
   `Faces.ShuffleAllTo([sbire], "EncounterDeck", effect)` (modele gs163 pour la forme du Boost).

⚠ Mots-pieges : « If you cannot » couvre AUSSI l'absence d'Inspection en jeu (arbitrage de l'utilisateur, 25/10/2026 : sans
Inspection, le Guardsman gagne Surge) ; « random » = tirage seme du moteur ; le sbire du Boost est tire AU HASARD aussi
(arbitrage de l'utilisateur, 25/10/2026) ; rien dessous = le Boost ne fait rien.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (4 cas sujets) :
      - vt022 Corrupted Guardsman : Inspection en jeu et un sbire sous le Vault -> il est REVELE (en jeu), pas de surge
      - vt022 Corrupted Guardsman : Inspection NON en jeu -> il gagne SURGE (arbitrage du 25/10/2026), le sbire reste sous le Vault
      - vt022 Corrupted Guardsman : Inspection en jeu mais AUCUN sbire sous le Vault -> SURGE
      - vt022 Corrupted Guardsman : Boost -> un sbire de sous le Vault est MELANGE dans le deck de rencontre
      Preuve par substitution : **rouges 4/4** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou déplace une carte déjà couverte par les cas plateau du Vault. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt026 : Burglary (SideScheme)

```
Burglary — MANIGANCE ANNEXE x2. Menace de depart 2[per_hero]. Crisis. 2 icones de boost.
When Revealed: If Inspection of the Vault is in play, place 1[per_hero] additional threat here.
When Defeated: Reveal the top card of the villain deck.

Cartes de reference :
 - Crisis : natif (desc.Crisis, fiche mots-cles/crisis.md ; icone verifiee sur le glyphe C de ChampionsIcons.ttf).
 - « place 1[per_hero] additional threat here » : `this.PlaceThreatOnSchemes([this], n, effect)` (modele 01107 Breakin' &
   Takin' pour la forme ; n = nombre de joueurs).
 - « When Defeated » : `WhenSchemeBeDefeated(WhenDefeated, "This", ...)` (modele ld011) ; « Reveal the top card of the villain
   deck » : `RevelerProchainMechant` (helper du set).

⚠ Mots-pieges : « 1[per_hero] ADDITIONAL » = 1 par joueur EN PLUS de la menace de depart ; deck de vilains vide = rien a reveler.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt026 Burglary : sans Inspection, menace de depart seule (2 pour 1 joueur)
      - vt026 Burglary : Inspection en jeu -> 1[per_hero] menace EN PLUS (2 + 1 = 3)
      - vt026 Burglary : vaincue -> le dessus du deck de vilains est REVELE
      Preuve par substitution : **rouges 2/3** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou des conditions de fin de partie portées par le helper `VerifierFinDePartie`, calibré ROUGE à part : trois cas tombent sans lui). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe à menace (Crise). Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt028 : Contingency Measures (SideScheme)

```
Contingency Measures — MANIGANCE ANNEXE. Menace de depart 2[per_hero]. 3 icones de boost.
Forced Interrupt: When a villain would be defeated, shuffle it into the villain deck instead.
While Inspection of the Vault is in play, this card gains a hazard icon.

Cartes de reference :
 - « When a villain would be defeated, ... instead » : `WhenUnitWouldBeDefeated(ForcedInterrupt, Villain, ...)` +
   `message.SetBeInstead(effect)` (modele gs162a pour la forme ; `Villains.ShuffleIntoVillainDeck`, brique du 25/10/2026) puis
   `ApresDepartDUnMechant` (livret p.1).
 - « While Inspection of the Vault is in play, this card gains a hazard icon » : `ThisGainKeywordWhileFaceIsInPlay(
   while_face_is_in_play=CardFinder(name=Inspection), hazard=1)` (modele officiel 21182 ; icone verifiee sur le glyphe H).

⚠ Mots-pieges : « would be DEFEATED ... INSTEAD » : le vilain n'est PAS vaincu (aucun « When Defeated », aucun retrait) et ses
attachements / cartes d'etat sont defausses ; « any villain », pas seulement le vilain de plus bas ordre ; le melange se fait
meme pour le DERNIER vilain en jeu (on revele alors le suivant, ou le meme).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt028 Contingency Measures : un vilain qui serait vaincu est MELANGE dans le deck de vilains (pas vaincu), l'autre reste
      - vt028 Contingency Measures : tant que l'Inspection est en jeu, la carte gagne une icone HAZARD
      - vt028 Contingency Measures : TEMOIN sans Inspection -> aucune icone Hazard
      Preuve par substitution : **rouges 2/3** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou des conditions de fin de partie portées par le helper `VerifierFinDePartie`, calibré ROUGE à part : trois cas tombent sans lui). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt029 : Scheming from Within (SideScheme)

```
Scheming from Within — MANIGANCE ANNEXE. Menace de depart 2[per_hero]. Hazard. 1 icone de boost + ★.
When Revealed: Place 1 additional threat here for each villain beneath The Vault.
[star] Boost: If Inspection of the Vault is in play, this card gets +1 boost icon for each villain beneath The Vault.

Cartes de reference :
 - Hazard : natif (desc.Hazard, fiche mots-cles/hazard.md ; icone verifiee sur le glyphe H de ChampionsIcons.ttf).
 - « place N additional threat here » : `this.PlaceThreatOnSchemes([this], n, effect)` ; n = `len(MechantsSousLeVault)`.
 - « this card gets +1 boost icon » : `AbilityFactory.WhenBoostIconsWouldBeCount` + `message.UpdateBoostIcon(n, effect)` (modele
   56150, `IncreaseBoostIconsOnEncounterCard`).

⚠ Mots-pieges : « for each villain beneath » ne compte QUE les vilains (pas les sbires) ; l'effet de boost ne vaut que tant
que l'Inspection est en jeu et que la carte est la carte de boost qu'on compte (pas quand elle est une manigance en jeu).
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt029 Scheming from Within : 1 menace EN PLUS par vilain sous le Vault (2 + 2 = 4)
      - vt029 Scheming from Within : Boost avec Inspection -> +1 icone de boost par vilain sous le Vault (1 + 2 = 3)
      - vt029 Scheming from Within : TEMOIN sans Inspection -> 1 seule icone de boost
      Preuve par substitution : **rouges 2/3** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou des conditions de fin de partie portées par le helper `VerifierFinDePartie`, calibré ROUGE à part : trois cas tombent sans lui). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : manigance annexe à menace. Cas plateau : ui-app/src/board/the-vault-plateau.test.ts (6 cas verts ; aucun correctif de plateau nécessaire, le rendu générique dessine tout). Résultat : OK.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt030 : Rampage in Public (Treachery)

```
Rampage in Public — TRAITRISE x4. 2 icones de boost.
When Revealed: If the number of villains in play is less than the number of players, this card gains surge. Reveal the top
  card of the villain deck. If you cannot, the villain with the highest activation order value activates against you.

Cartes de reference :
 - Surge conditionnel : `ThisCardGainSurge` (modele gs189) ; revelation : `RevelerProchainMechant` (helper du set) ;
   « activates against you » : `villain.DoActivate(joueur, effect)` (modele bw021 Imperius Rex : `namor.DoActivate(joueur, effect)`).
 - « the villain with the highest activation order value » : `Villains.ParOrdreDActivation(...)[-1]`.

⚠ Mots-pieges : le nombre de vilains se compte AVANT la revelation ; « If you cannot » = deck de vilains VIDE ; « highest »
= plus GRAND Activation Order (l'inverse de « the villain ») ; aucun vilain en jeu et deck vide = rien ne s'active.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt030 Rampage in Public : 1 vilain pour 1 joueur (pas moins) -> PAS de surge, le dessus du deck de vilains est revele
      - vt030 Rampage in Public : AUCUN vilain en jeu (0 < 1 joueur) -> SURGE, et le dessus du deck de vilains est revele
      - vt030 Rampage in Public : deck de vilains VIDE -> le vilain de plus GRAND Activation Order (Hydro-Man 4, ATK 2) active contre vous, pas Mentallo (2, ATK 1)
      Preuve par substitution : **rouges 3/3** sans le module. Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou déplace une carte déjà couverte par les cas plateau du Vault. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

### vt034 : Riot in the Vault (Treachery)

```
Riot in the Vault — TRAITRISE x3. 1 icone de boost. Surge.
When Revealed: If Inspection of the Vault is not in play, reveal it. Otherwise, place 1 threat on the main scheme for each
  Villain beneath The Vault.

Cartes de reference :
 - Surge : natif (desc.Surge, fiche surge.md) ; « reveal it » : `SetupCards.Reveal(..., only_set_aside=True)` (Obligation, donnee
   au premier joueur par son `GiveTo`) ; menace : `this.PlaceThreatOnSchemes("MainScheme", n, effect)` (modele 60148).

⚠ Mots-pieges : « OTHERWISE » = deux branches exclusives (l'Inspection arrive OU la menace tombe, jamais les deux) ; « Villain
beneath » ne compte que les vilains ; Inspection de cote dans la reserve : la carte la retrouve meme apres qu'un joueur l'a
mise de cote.
```

- [x] Étape 2 : cartes de référence : voir l'en-tête du script ci-dessus (lignes « Cartes de reference »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir « Mots-pieges » ci-dessus. Résultat : chaque mot du texte a sa contrepartie dans le script.
- [x] Étape 6 : nombres texte ↔ code : valeurs relues sur le scan et contrôlées par `desc` de `cards.json` (PV par joueur, ATK, SCH, ordre d'activation, boost, menaces) et les cas de valeurs imprimées. Résultat : conformes.
- [x] Étape 7 : cas test_capacites par capacité (3 cas sujets) :
      - vt034 Riot in the Vault : Inspection NON en jeu -> elle est REVELEE (donnee au 1er joueur), aucune menace
      - vt034 Riot in the Vault : Inspection DEJA en jeu -> 1 menace sur le complot par vilain sous le Vault (2)
      - vt034 Riot in the Vault : Surge (natif) -> le temoin du deck de rencontre est revele
      Preuve par substitution : **rouges 2/3** sans le module (les cas verts restants sont des contre-cas d'absence d'effet ou des conditions de fin de partie portées par le helper `VerifierFinDePartie`, calibré ROUGE à part : trois cas tombent sans lui). Résultat : OK.
- [x] Étape 7 bis : limite imprimée ? NON (aucune « Limit once per ... » sur ce pack). Résultat : sans objet.
- [x] Étape 8 : autoplay ciblé : 60 parties (spider_man : the_vault standard et « expert » du pilote (vilains I + ensemble expert) 24, the_vault_expert (vilains II) 12, rhino témoin 24 ; profils prudent / équilibré / agressif), grep tracebacks : 0 sur les 60 journaux ; 1 partie bloquée (the_vault, prudent) par le garde-fou anti-répétition du PILOTE pendant l'enchaînement des vilains, pas par le scénario. Journaux lus : vilains I et II révélés depuis le deck de vilains (When Revealed de Nekra II joué), plusieurs vilains activent contre le même joueur dans l'ordre, Réponses forcées des huit vilains choisies (« Discard the top 3 », « Exhaust your identity », « Confuse the attacker », « Heal 1 damage », « Give Nekra 1 facedown boost card »...). Résultat : aucun incident.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT (attache, glisse, compteur, statut, mise de côté, changement de zone) ? NON en propre : elle chiffre ou déplace une carte déjà couverte par les cas plateau du Vault. Résultat : sans objet.

Carte terminée : **OUI** (hors la partie réelle jouée par un humain, voir « Gates du scénario »).

# Setup

**Texte imprimé / définition** : « Setup. » Une carte de rencontre avec ce
mot-clé est mise en jeu pendant la mise en place du scénario (étape
« Set Up »), avant que le deck rencontre soit mélangé, au lieu d'attendre
d'être révélée. Ses capacités « When Revealed » ne jouent pas ; un texte
« Setup: ... » sur la carte décrit ce qu'elle fait à ce moment.

**Mécanisme moteur** : clé `desc.Setup` (`"Setup": "1"`) lue nativement.
`HasSetup` (`src/game/card/face/attribute/has_setup.py`) enregistre
`printed_setup` ; `world.py:552` ramasse toutes les faces des decks avec
`printed_setup > 0` et appelle `ProcessSetup`, qui fait `PutIntoPlay` sous
le contrôle du premier joueur. **Aucun script requis** pour la mise en jeu
elle-même. Le texte « Setup: ... » de la carte, lui, se code avec
`AbilityFactory.AfterGameSetup(op)` : il part au pas « Resolve Character
Setup Abilities », donc APRÈS la mise en place du complot principal et des
œuvres d'Art Museum Heist.

**Carte exemple** : `60112` : Disturbed Psyche (pack `fne`, set Typhoid
Mary), `desc` contient `"Setup": "1"`, et son texte « Setup: Randomly
choose which side of Typhoid Mary is face up » est codé par
`AbilityFactory.AfterGameSetup(mise_en_place)` avec
`Rand.RandomChoice([True, False], effect)` puis `vilain.card.Flip(effect)`.
`60113a` Establish Trust (complot annexe Permanent + Setup) entre en jeu par
le seul `desc`, sans une ligne de script.

**Pièges connus** :
- `AbilityFactory.WhenCardSetup` n'est JAMAIS envoyé à une carte mise en jeu
  par le mot-clé (mesuré le 18/09/2026 : le Setup de Disturbed Psyche restait
  muet). C'est `AfterGameSetup` qu'il faut.
- Sous le harnais (graine 42), `Rand.RandomChoice` est déterministe : la
  partie de test commence toujours sur Bloody Mary (`60110b`). Les cas qui
  veulent l'autre face font `Puzzle.Flip('60110b')`.
- Un vilain que le Setup retourne doit avoir ses DEUX faces déclarées dans le
  scénario (`"villain": ["60110a,60110b"]`), sinon `card.Flip` le met face
  cachée (RECETTES-MOTEUR §7quater).

**Variantes maison** : aucune recensée pour l'instant.

## Pack Cassandra Nova (Hellfire Hunt, `hf371`, `hf604a`, 01/11/2026)

- `hf371` Psychic Aegis (`Setup`, « Attach to the villain ») : `desc.Setup = "1"` + `AttachToFaceWhenPutIntoPlay(Villain)` ; la carte entre en jeu a la mise en place si son ensemble modulaire est dans le deck, attachee au vilain, et RESTE attachee quand le stade I est vaincu (cas dedie).
- `hf604a` : le Setup d'une face A de complot s'execute AVANT que le moteur avance A -> B (`World` etape 12) : un « advance to stage 2A » du Setup se code sur la face B par `AfterGameSetup` (recette §41 de RECETTES-MOTEUR).

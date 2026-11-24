# Permanent

**Texte imprimé / définition** : « Permanent. » Une carte avec ce mot-clé
ne peut pas quitter le jeu par les moyens normaux (défausse, retrait,
retour en main, etc.) tant que l'effet qui tenterait de le faire ne
provient pas du même set qu'elle. C'est un indicateur booléen (`Permanent
1`), réinitialisé à sa valeur imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Permanent` sur la carte, lue nativement
par le moteur. `HasPermanent`
(`src/game/card/face/attribute/has_permanent.py`) enregistre l'attribut
`Permanent` -> `printed_permanent` (bool). Dans `OnWhenCardLeavePlay`, si
`self.permanent` est vrai et que l'effet qui retire la carte
(`by_effect.this.paper.set_name`) appartient à un set différent de celui
de la carte, la sortie de jeu est bloquée (`return False`) ; quelques
exceptions nommées (Flight/Super Strength/Telepathy, Weather/Storm, Power
Stone, Milano) sont codées en dur dans ce fichier moteur, pas dans les
scripts de cartes. **Aucun script requis** pour le mot-clé Permanent
lui-même : c'est une des « bases automatiques » du guide, à ne pas
recoder inutilement dans le `.py` de la carte.

**Carte exemple** : `04159a` : Basic Thwart Upgrade (`desc` contient
`"Permanent": "1"`), lu directement depuis `desc` pour l'aspect
« impossible à retirer » lui-même. Un fichier `04159a.py` existe bien
(`src/cards/pack/trors/hydra_campaign/04159a.py`), mais son contenu
(`AbilityFactory.GiveKeywordToAttached("You", health=2)` et
`AbilityFactory.GiveKeywordToAttached(Hero, thwart=1)`) code la capacité
imprimée de la carte (donner +2 HP à vous et +1 THW aux héros), pas le
mot-clé Permanent. Le script ne doit pas et ne recode pas le blocage de
sortie de jeu.

**Pièges connus** : ne pas coder de garde-fou « empêcher la défausse »
dans le `.py` d'une carte Permanent : c'est géré nativement par
`HasPermanent.OnWhenCardLeavePlay`. Le cas `04159a` est un exemple concret
et vérifié où le script existant sert exclusivement à une autre capacité
imprimée que le mot-clé lui-même. Attention également aux exceptions
codées en dur par nom de set/carte dans `has_permanent.py` : elles ne sont
pas généralisables, toute nouvelle carte Permanent avec un comportement
similaire nécessiterait une modification du moteur, pas un script de
carte isolé.

**Variantes maison** : aucune recensée pour l'instant.

**Cas `tc013` Casey's Bag (pack `casey_jones`)** : amélioration Permanente SANS coût imprimé, mise en jeu par
le Setup de `tc001b`. Un `Puzzle.Discard('tc013')` (règle de débogage d'un autre set) la laisse en jeu ;
un effet du MÊME set « Casey Jones » peut la déplacer (le test du moteur compare les `set_name`).

**Cas `gs099q` Maelstrom / `gs301` Quantum Bands (Galactic Storm, 20/10/2026)** : le sbire nemesis de Quasar
(set « Quasar Nemesis ») GLISSE nommement les Quantum Bands (Permanent, set « Quasar ») sous lui. Le test de
set de `has_permanent.py` l'aurait refuse : exception ajoutee au meme endroit que « Milano » (nom de la carte
permanente + nom et set de la carte qui agit). Cas `[quasar] gs099q` (Bandes glissees puis revenues).

# Les sons du jeu : quel déclencheur, quel fichier

Relevé le 06/09/2026 dans le moteur, pour préparer un remplacement des sons
d'origine. Rien n'est à deviner ici : chaque ligne vient du code.

## Comment ça marche, en trois phrases

Le moteur décide du son, pas le client. À chaque rendu, il place un nom dans
`WorldDescriptor.sound_name` (`src/game/render/descriptor/world.py:14`), et le
plateau joue le fichier `<nom>.wav` correspondant
(`ui-app/src/board/sons.ts`). Le client ne choisit rien : **pour changer un son,
il suffit de remplacer le fichier `.wav`, sans toucher à une ligne de code.**

Les fichiers vivent dans `Fusion/marvel-lcg-src/assets/sounds/`. La liste des
noms autorisés est figée dans le moteur, `src/game/message/message.py:17`
(`SOUND_NAMES`) : **on ne peut pas en ajouter un nouveau sans modifier le
moteur**, mais on peut remplacer n'importe lequel des 21 existants.

Deux règles du plateau, dans `sons.ts` : rien ne se joue quand l'onglet n'est pas
visible, et rien ne se joue pendant qu'on attend TA décision (le rendu se répète
tant que la question est ouverte), sauf le gong de phase.

## Les 21 sons, et ce qui les déclenche

| Fichier | Déclencheur dans le jeu | Où c'est décidé |
|---|---|---|
| `phase.wav` | **Changement de phase.** Le seul qui joue même pendant qu'on te pose une question : c'est le gong qui annonce que la main change de camp. | `can_attack.py` et les envoyeurs de phase |
| `nextturn.wav` | **Passage au tour suivant**, quand le jeton de premier joueur bouge. | `sender_round.py:106` |
| `damage.wav` | **Dégâts infligés à une unité.** Héros, allié, sbire, méchant : c'est le son de l'impact. | `sender_unit.py:277` |
| `target.wav` | **Désignation d'une cible**, juste avant l'attaque : l'attaquant vise. Joue aussi quand un effet pointe plusieurs unités. | `sender_damage.py:72`, `:93`, `:326` |
| `directattack.wav` | **Attaque directe** (déclaré dans la liste du moteur ; aucun envoyeur ne l'utilise aujourd'hui dans cette version). | `SOUND_NAMES` seulement |
| `gainlp.wav` | **Points de vie regagnés.** Un héros qui se soigne, un allié soigné. | `sender_unit.py:253` |
| `destroyed.wav` | **Une carte est détruite** et part au cimetière. | `sender_card.py` |
| `banished.wav` | **Une carte est bannie ou retirée de la partie**, y compris un complot vaincu. | `sender_scheme.py:129`, `sender_card.py:824` |
| `activate.wav` | **Une capacité s'active.** Le son le plus fréquent du jeu : quatorze points d'appel. | `message.py:112` et suivants |
| `negate.wav` | **Un effet est annulé ou contré.** | `sender_card.py` |
| `reveal.wav` | **Une carte est révélée**, face cachée retournée face visible. | `sender_card.py` |
| `flip.wav` | **Une carte se retourne** : passage héros / alter ego, changement de face d'un méchant. Six points d'appel. | `sender_card.py` |
| `draw.wav` | **Pioche.** Un joueur prend une ou plusieurs cartes. | `sender_player.py:83`, `sender_card.py:821` |
| `carddrop.wav` | **Une carte est posée sur la table**, jouée depuis la main. | `sender_card.py` |
| `cardpick.wav` | **Une carte est prise en main** (déclaré ; sans envoyeur dans cette version). | `SOUND_NAMES` seulement |
| `equip.wav` | **Une amélioration ou un attachement est équipé** sur un personnage. | `sender_card.py` |
| `set.wav` | **Une carte est mise de côté ou placée dans un deck.** Quatorze points d'appel : c'est aussi le son des mises en place. | `sender_deck.py` |
| `shuffle.wav` | **Un deck est mélangé.** | `sender_deck.py` |
| `token.wav` | **Un jeton est posé sur une carte** (menace, dégâts, ressources). | `sender_card.py` |
| `addcounter.wav` | **Un compteur augmente** (pouvoir, munitions, tout compteur nommé). | `sender_token.py:25`, `:89` |
| `removecounter.wav` | **Un compteur diminue.** | `sender_token.py:47`, `:114` |

Un vingt-deuxième fichier n'est pas un effet : `musique-plateau.mp3`, la musique
de fond du plateau, réglable à part.

## Par ordre d'importance, si tu ne remplaces qu'une poignée de sons

Les cinq qu'on entend le plus, et qui donnent sa couleur au jeu :

1. **`activate.wav`** : quatorze points d'appel, c'est le son de fond de toute la partie.
2. **`phase.wav`** : le gong qui rythme la partie, et le seul qui perce pendant une question.
3. **`damage.wav`** : chaque coup encaissé ou porté.
4. **`set.wav`** : quatorze points d'appel, très présent en mise en place.
5. **`target.wav`** : à chaque attaque, juste avant les dégâts.

Ceux qui gagneraient le plus à être marquants, parce qu'ils signalent un moment
rare et important : `destroyed.wav`, `banished.wav`, `flip.wav`, `nextturn.wav`.

Deux ne servent à rien aujourd'hui et ne s'entendront pas, quoi qu'on y mette :
`directattack.wav` et `cardpick.wav`.

## Contraintes techniques pour les nouveaux fichiers

- **Format `.wav`**, comme les existants : c'est ce que le cache de `sons.ts`
  construit (`new Audio('/<nom>.wav')`). Un `.mp3` ne serait pas trouvé.
- **Même nom exact**, en minuscules, sans accent. Le nom vient du moteur.
- **Courts.** Ces sons se déclenchent en rafale : plusieurs `activate` peuvent
  s'enchaîner en une seconde pendant une phase du méchant. Au-delà d'une demi-
  seconde, ils se chevauchent et deviennent une bouillie.
- **Volume homogène entre eux.** Le plateau ne normalise rien : un fichier deux
  fois plus fort que les autres s'entendra deux fois plus fort.
- Le même fichier est rejoué depuis le début à chaque déclenchement, jamais
  superposé à lui-même.

## Où les déposer

`Fusion/marvel-lcg-src/assets/sounds/`, en écrasant l'existant. Le déploiement
serveur les emporte avec le code (ils ne sont pas dans les exclusions de
`deploiement/deployer.ps1`, contrairement aux images de cartes).

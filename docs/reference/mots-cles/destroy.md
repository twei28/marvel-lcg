# Destroy (mot-clé maison, pack `sentinel`)

**Texte imprimé / définition** (insert du pack, `Insert.jpg`) : « When you are
instructed to **destroy** a Component upgrade, take 2 unpreventable damage and
flip that Component from its **Intact** side to its **Destroyed** side. A
Component that is already on its Destroyed side cannot be destroyed. »

Traduction retenue : « Quand on vous demande de **détruire** une amélioration
Component, subissez **2 dégâts imblocables** et retournez ce Component de sa
face **Intacte** à sa face **Détruite**. Un Component déjà sur sa face Détruite
ne peut pas être détruit. »

**Mécanisme moteur** : aucune primitive. Le mot-clé est un **raccourci de
texte**, pas une règle du moteur : il se déroule en deux opérations que le
moteur connaît déjà. **L'ordre du code est l'inverse de celui du texte**, et ce
n'est pas un détail (voir le troisième piège ci-dessous).

1. **Retourner le Component**, `Faces.FlipAllTo([component], face_up=None, effect)`
   (`src/game/operate/faces.py:144`), comme la Battle Board de `night_thrasher`
   (`nt003a` / `nt003b`) et la Spider Armor d'`armored_spidey` (`as002a`).
2. **2 dégâts imblocables à l'identité**, avec
   `DamageProperty(damage=2, ignore_tough=True, unpreventable=True)` — c'est le
   héros qui subit, pas le Component.

⚠ **`DamageProperty.unpreventable` n'existait pas avant ce pack** (ajouté le
12/09/2026). Les deux seules cartes officielles qui emploient le mot
(`62001a` Luke Cage, `62028` Internal Injury) se contentaient d'`ignore_tough`,
qui ne ferme qu'**une porte sur trois** : la carte Coriace. Une prévention
chiffrée (`08032` Defensive Stance) ou un remplacement pur et simple
(`49006` Magnetic Bubble, et surtout `st001a` lui-même) passaient au travers.
Le drapeau est honoré par `Message.WhenUnitWouldTakeDamage`, dans
`PreventDamage` **et** dans `SetBeInstead`. Les deux cartes officielles ont été
mises à jour au passage.

Le pack centralise les deux opérations dans **`Detruire()`** du `__init__.py` du
set : neuf cartes emploient le mot-clé, aucune ne doit pouvoir en diverger.

**Carte exemple** : `st001a` Sentinel — « Interrupt: When you would take any
amount of damage, destroy a COMPONENT upgrade instead. » Le mot-clé est ici la
substitution elle-même : les dégâts de l'attaque sont remplacés par 2 dégâts
imblocables plus le retournement. Voir aussi `st006` Exterminate, `st007`
Hardwire Access, `st008` Rocket Punch et `st009` Threat Suppression, dont le
coût additionnel est « inclinez **ou détruisez** » un Component nommé.

**Pièges connus** :

- **« Un Component déjà Détruit ne peut pas être détruit »** : la cible légale
  est une amélioration portant les traits `COMPONENT` **et** `INTACT`. Le
  moteur ne le déduit pas : chaque appel filtre sur le trait `INTACT`.
- **Les 2 dégâts ne sont pas préventibles, et c'est vital.** Sur `st001a`,
  l'interruption remplace des dégâts par d'autres dégâts. **Mesuré le
  12/09/2026, sans le drapeau** : une attaque de sbire à 2 dégâts retournait les
  QUATRE pièces d'un coup, chaque destruction relançant l'interruption. Et dans
  une version antérieure, où les dégâts tombaient AVANT le retournement, la
  boucle ne s'arrêtait jamais — trois parties d'autoplay bloquées sur la même
  question reposée à l'identique.
- **Retourner d'abord, blesser ensuite.** L'insert énonce l'inverse, mais c'est
  le seul ordre qui termine : si les dégâts partent en premier, la pièce visée
  est encore INTACT au moment où une relance cherche une cible.
- **C'est le HÉROS qui subit les 2 dégâts**, jamais le Component : une
  amélioration n'a pas de points de vie.
- **Détruire n'est pas défausser.** Le Component reste en jeu, retourné. Une
  carte qui défausse une amélioration (`st015` Mark VII-A, second volet) fait
  autre chose.
- **Le coût additionnel « inclinez OU détruisez »** est un choix du joueur
  **dans le coût**, pas dans l'effet : le moteur doit proposer les deux, et
  « détruire » reste possible quand la carte est déjà inclinée. C'est ce qui
  permet de rejouer un événement dans le même tour, en payant de sa carrosserie.

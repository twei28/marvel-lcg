# Track (mot-clé maison, Rainy)

**Texte imprimé / définition** : l'insert du pack **Superior Spider-Man** la
donne, et sans ambiguïté :

> **New Keyword: Track.** The track keyword is a shorthand term meaning
> **"move 1 threat from a scheme to a minion in play."** A minion may have any
> number of threat on them and they do not need to be engaged with you in order
> to be tracked. While there are no innate effects of a minion having threat on
> them, some card effects may interact with threat on a minion. **When a minion
> with threat on it is defeated, all threat on that minion is returned to the
> supply.**

⚠ **C'est un DÉPLACEMENT, pas un retrait.** La menace quitte la manigance et
arrive sur le sbire : elle n'est pas détruite. C'est exactement le piège
`instead` de PROCESSUS-CARTE §5 (leçon The Spot) — coder « retirer 1 menace »
sans rien poser sur le sbire rendrait le pack entier faux, et ferait de
`track` un simple contre gratuit.

**Q/R de l'insert** : « Can I track a minion while I am engaged with a minion
that has the patrol keyword? » → **Non depuis le complot PRINCIPAL** (patrol,
ou une icône crisis en jeu, l'interdisent), **oui depuis un complot annexe**.
Le retrait passe donc par les mêmes règles que n'importe quel retrait de
menace : `RemoveThreatFromSchemes`, sans `ignore_crisis`.

**Mécanisme moteur** : aucune primitive dédiée, deux gestes enchaînés.

- Le retrait : `this.RemoveThreatFromSchemes(cibles, 1, effect)` — et il faut
  lire son RETOUR, car il peut ne rien retirer (manigance vide, patrol, crisis).
  Ne poser sur le sbire que ce qui a réellement été retiré.
- La pose : `Faces.PlaceCountersOn([sbire], n, 'threat', effect)`.
  ⚠ Le compteur `threat` a été **AJOUTÉ à l'énum `COUNTER`** le 08/09/2026
  (`card_face.py`) : la menace posée sur un SBIRE n'a aucune existence native
  dans le moteur, contrairement à celle d'une manigance.
- Le nettoyage à la mort du sbire est **gratuit** : les compteurs disparaissent
  avec la carte. Rien à coder pour la dernière phrase de la définition.

**Carte exemple** : `su010` Facial Recognition Uplink (« After a minion enters
play, track it ») ; `su008` Mechanical Arms (« When you make a basic attack
against a minion, track that minion ») ; `su002` Spiderlings (« track a minion
INSTEAD of removing threat »).

**Pièges connus** :

- ⚠ « **a minion in play** » : n'importe quel sbire, y compris celui d'un autre
  joueur, et **sans obligation d'être engagé** — l'insert le dit. Ne pas
  restreindre le sélecteur aux sbires engagés.
- ⚠ « **from a scheme** » : principal OU annexe, au choix du joueur. Ne pas
  coder « du complot principal ».
- ⚠ Sans sbire en jeu, ou sans menace sur aucune manigance, `track` ne fait
  rien. Toute carte qui l'emploie en COÛT doit donc doubler son `CostFunc`
  d'un `conditions=[...]` (RECETTES §5).
- ⚠ `su015` Goblin Protocol dit « Threat on tracked minions counts towards the
  main scheme's target threat » : c'est le seul endroit où la menace d'un
  sbire agit, et cela demande de lire les compteurs de TOUS les sbires en jeu.

**Variantes maison** : aucune. `su011` Spider-Bot offre « track a minion **or**
remove 1 threat from a scheme », deux branches distinctes — la seconde n'est
PAS un track (rien n'est posé sur un sbire).

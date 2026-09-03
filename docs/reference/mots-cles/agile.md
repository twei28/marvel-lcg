# Agile X — MOT-CLÉ MAISON

**Texte imprimé / définition** : « gains agile 1 *(reduce damage from attacks
with boost cards by 1)*. » Le personnage qui porte Agile X subit X dégâts de
moins de la part d'une attaque **accompagnée d'au moins une carte de boost**.
La parenthèse est imprimée sur la carte elle-même : la définition vient de
l'auteur, elle n'a rien été arbitrée.

**Origine** : `nt003a` Battle Board, face `VEHICLE` (pack maison
`night_thrasher`, set 153, auteur DESIGNHACKER). Premier et seul porteur
connu au 03/09/2026.

**Ce que le mot-clé vise vraiment** : les attaques d'**activation d'ennemi**.
Une attaque de vilain ou de sbire reçoit toujours des cartes de boost ; une
attaque portée par un effet de carte (une traîtrise, une capacité) n'en reçoit
aucune. Agile ne protège donc que de la phase du vilain, jamais d'un effet
ponctuel — c'est ce qui l'empêche d'être une réduction de dégâts générale.

**Mécanisme moteur** : **aucune primitive native, il faut le scripter.**
Le moteur ne conserve la liste des cartes de boost d'une attaque que dans les
messages d'APRÈS-COUP : `Message.AfterUnitAttackUnit.boost_faces`
(`sender_damage.py:510`) et `AfterEnemyActivationEnd.HasThisBoost`
(`sender_enemy.py:149`). Au moment où les dégâts tomberaient — la seule
fenêtre où l'on peut encore les réduire — les cartes de boost ont déjà été
défaussées à l'étape (d) de `can_boost.py`.

Le montage retenu inverse donc la lecture : au lieu de demander « cette
attaque avait-elle des cartes de boost ? », on s'accroche au moment où **une
carte de boost est retournée face visible pendant une attaque**, et on
enregistre à cet instant une réduction TEMPORAIRE bornée à cette attaque.

```python
AbilityFactory.WhenBoostCardTurnedFaceUp(
    AbilityType.NonKeyword,
    None,
    poser_la_reduction,
    while_attack=True,
)
```

puis, dans l'opération, un `RegisterTemp` d'un
`ReduceCharacterTakeDamageBy(<porteur>, X)` lié à l'attaque en cours
(`is_from_attack=message.would_message`), avec un garde-fou pour ne
l'enregistrer qu'une fois par attaque : une activation retourne plusieurs
cartes de boost, et sans ce garde-fou la réduction se cumulerait autant de
fois qu'il y a de cartes.

**Carte exemple** : `nt003a` Battle Board (face `VEHICLE`) — voir le
`.py` correspondant, qui porte le commentaire complet du montage.

**Pièges connus** :

- ⚠ **Ne pas le rendre par un `ReduceCharacterTakeDamageBy` permanent.** Ce
  serait une réduction de TOUS les dégâts d'attaque, boost ou pas : la carte
  deviendrait deux fois meilleure qu'imprimée, et rien dans les tests ne le
  verrait — un cas qui compte les dégâts d'une attaque de vilain passe au vert
  dans les deux montages, puisqu'une attaque de vilain a toujours du boost.
  **Le contre-cas obligatoire est une attaque SANS carte de boost** (dégâts
  infligés par un effet de carte), où la réduction ne doit PAS s'appliquer.
  ⚠ **Et le harnais ne sait pas en produire** : une activation d'ennemi reçoit
  toujours des cartes de boost. Le contre-cas réellement monté (`nt003a`,
  « agile ne touche PAS aux dégâts hors attaque ») passe donc par des dégâts
  qui ne viennent d'aucune attaque — il prouve que la réduction n'est pas
  permanente, mais il reste vert sous substitution. C'est la seule gate du
  pack `night_thrasher` restée entrouverte, et elle est signalée comme telle
  dans son journal de portage.
- ⚠ **Une carte de boost par attaque ne suffit pas à borner la réduction** :
  le message est envoyé pour CHAQUE carte retournée. Sans garde-fou, une
  activation à trois cartes de boost réduirait de 3.
- ⚠ Agile réduit les DÉGÂTS, pas les icônes de boost. Ne pas le confondre avec
  `as015` Scarlet Spider (pack `armored_spidey`), qui réduit le nombre
  d'icônes : l'un agit sur ce que l'attaque inflige, l'autre sur ce qu'elle
  vaut.
- ⚠ Comme tout mot-clé chiffré, la valeur se réinitialise à chaque reset des
  mots-clés : elle doit être donnée par une capacité continue, pas posée une
  fois pour toutes.

**Variantes maison** : aucune autre à ce jour. À relire si un futur pack
imprime « agile » sans la parenthèse explicative — la définition ci-dessus
vient de la carte de DESIGNHACKER, pas d'une règle officielle.

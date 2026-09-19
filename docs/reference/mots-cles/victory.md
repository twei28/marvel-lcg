# Victory X (dont X négatif)

**Texte imprimé / définition** : « Victory X » (RRG) : quand cette carte est
vaincue (sbire, complot annexe) ou, pour une carte joueur qui le porte, quand
elle quitte le jeu de cette façon, elle est placée dans la **pile de victoire**
au lieu de sa défausse, et compte X points dans le score final. X peut être
**négatif** : la carte va quand même dans la pile de victoire, mais elle
retire des points. Fear No Evil imprime « Victory -1 » sur l'alliée de
campagne * Typhoid Mary / * Bloody Mary (`60210a,60210b`) : la vaincre coûte
un point ET laisse une trace, le livret vérifie « Mary Defeated? » en fin de
partie en regardant la pile de victoire.

**Mécanisme moteur** : base native, lue dans `desc.Victory` (`HasVictory`,
`src/game/card/face/attribute/has_victory.py`). `OnBeDefeated` envoie la face
dans la pile de victoire (`Faces.AddToVictoryDisplay`) dès que
`printed_victory` n'est pas `None` : **le signe ne change rien au déplacement**,
`0` et `-1` y vont comme `2`. Le nombre n'est relu que par le score. Un vilain
ne s'y déplace pas tant qu'un stade suivant porte le même nom. Aucun script
requis pour le mot-clé lui-même.

**Carte exemple** : `60210a` : * Typhoid Mary (alliée de campagne, Victory -1),
lu directement depuis `desc` (`"Victory": "-1"`), aucun script requis pour
l'aller dans la pile de victoire ; c'est `CollectFNE` (`cards/pack/fne/campaign.py`)
qui relit ensuite `card.area.flags.is_victory_display` pour cocher « Mary
Defeated? ». Autre exemple : `60024` * De-escalation (Cops, Victory 0).

**Pièges connus** :
- Écrire `"Victory": "0"` n'est PAS neutre : la carte va dans la pile de
  victoire (c'est voulu pour De-escalation, dont le texte le demande).
- Une carte qui QUITTE le jeu autrement que vaincue (défaussée par un effet,
  retirée du jeu) ne passe pas par `OnBeDefeated` : elle ne va pas dans la
  pile de victoire. Pour Typhoid Mary, « defeated » est donc bien la seule
  voie qui coche « Mary Defeated? ».
- Le harnais lit la pile par `card.area.flags.is_victory_display` (clé
  `victoire` de `pileFondue` côté plateau : « Pile de victoire »).

**Variantes maison** : aucune.

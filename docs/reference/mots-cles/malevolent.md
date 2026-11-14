# Malevolent (mot-clé MAISON, Sentry / Neptune)

**Texte imprimé / définition** (carte rr016 Void) : « Malevolent. *(Each character you control and other enemies must target this card for their first attack each round.)* » Version « Card Sized » de l'insert : « villains … forcing characters … to target him for their first attack each round » ; le grand insert précise qu'un ennemi qui attaquerait une IDENTITÉ alors que le Void est en jeu attaque le Void à la place.

**Mécanisme moteur** : AUCUN attribut (mis en `desc`, il fait planter le montage). CODÉ (03/11/2026) dans le script de Void `rr016` : `WhenUnitWouldAttackUnit(NonKeyword, Unit2, Unit2, op)` + `message.ChangeTarget(void, effect)`, marqueur de round `attaquant.rr_void_ronde`.

Historique de l'analyse : AUCUN attribut moteur. Le mot n'est pas un attribut moteur : mis dans `desc`, il fait planter le montage (`KeyError: 'Malevolent'`, constaté le 03/11/2026). Il vit donc dans le TEXTE de la carte et dans son script : une restriction de ciblage « première attaque de chaque round » (marqueur de round sur le personnage, comme `rz003`), appliquée aux personnages que le joueur contrôle et aux AUTRES ennemis.

**Carte exemple** : `rr016` Void. Précédents de restriction de cible : RECETTES §6 (Ciblage) et §16.1 (un ennemi attaque un autre ennemi ou un allié).

**Pièges connus** : « first attack each round » est par PERSONNAGE et par round ; ne pas confondre avec Guard (qui s'applique à toute attaque contre le méchant) ; le Void peut ne pas être en jeu, la règle est alors muette.

**Variantes maison** : c'est lui-même la variante maison.

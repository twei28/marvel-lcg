# Stun (étourdir)

**Texte imprimé / définition** : « Stunned » : un ennemi étourdi ne peut pas attaquer ; son prochain attaque est remplacée par le retrait du statut (Rules Reference, « Stunned »). Un héros ou un allié étourdi ne peut pas attaquer non plus ; l'attaque de base RETIRE le statut au lieu d'infliger des dégâts.

**Mécanisme moteur** : statut de carte. Donner : `Faces.GiveStatus(cibles, "Stunned", effect)` ; choisir une cible légale : `.SetTarget(Enemy, canbe_stunned=True)` (modèle `rz007`, `nebu/22005`). Le retrait se fait par le moteur à l'activation ou à l'attaque de base.

**Carte exemple** : `rz007` Agent of Wakanda (`ChooseAbilities` de deux `ForChoiceAbility`, stun ou confuse).

**Pièges connus** : sans `canbe_stunned=True` le choix propose aussi des cibles déjà étourdies ; un Void (Sentry) est un ennemi ordinaire pour ce statut, rien de particulier.

**Variantes maison** : aucune.

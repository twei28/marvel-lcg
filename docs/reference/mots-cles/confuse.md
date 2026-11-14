# Confuse (embrouiller)

**Texte imprimé / définition** : « Confused » : un ennemi embrouillé qui MANIGANCE retire le statut au lieu d'ajouter de la menace ; un personnage de joueur embrouillé qui déjoue (THW) retire le statut au lieu de retirer de la menace.

**Mécanisme moteur** : statut de carte. Donner : `Faces.GiveStatus(cibles, "Confused", effect)` ; cible légale : `.SetTarget(Enemy, canbe_confused=True)` (modèle `rz007`, `nebu/22005`).

**Carte exemple** : `rz007` Agent of Wakanda.

**Pièges connus** : « stuns AND confuses each other enemy » (Sentry, Endless Power) = DEUX statuts à donner, chacun avec sa condition ; un ennemi déjà confus ne reçoit pas un second statut.

**Variantes maison** : aucune.

# Jeton « shadow counter » (TMNT Shinobi Ninjutsu, Inkwire)

**Texte imprimé / définition** : `sa007` ✦ Hamato Clan (soutien TEAM) : « *Response*: After an ally you control leaves
play, place 1 shadow counter here. *Action*: Exhaust this card and remove 1 shadow counter from here → cloak an ally you
control. » Aucune définition à part : un « shadow counter » est un compteur nommé, sans règle propre (comme `samurai`,
`amp`, `dredge`).

**Mécanisme moteur** : `'shadow'` est dans `CardFace.COUNTER` (`card_face.py`, ajouté le 17/10/2026 avec les Ninjutsu, fichier
moteur partagé, additif). Pose : `Faces.PlaceCountersOn([this], 1, 'shadow', effect)`. Retrait en coût :
`CostFunc.Counter("This", 1, 'shadow')` (cumulé avec `CostFunc.Exhaust("This")`). Pas de `Uses` : la carte entre en jeu SANS
compteur et rien ne la défausse quand elle n'en a plus. Libellé français du plateau : « ombre » (`compteurs-fr.ts`).

**Carte exemple** : `sa007` Hamato Clan.

**Pièges connus** :
- « an ally *you control* leaves play » : compter l'allié qui PART d'un autre joueur ne pose rien (`message.trigger.
  GetControlByPlayer()` est lu après la sortie : testé en partie à deux, cas `[sa] sa007`) ;
- « leaves play » = toute sortie (défaite, défausse, retour en main), un sbire qui part n'est pas un allié ;
- l'Action demande un allié sous son contrôle comme cible légale (sinon le coût n'est pas payé pour rien) ;
- un compteur par allié parti, pas de plafond imprimé.

**Variantes maison** : tout est maison.

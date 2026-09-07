# Seek (mot-clé maison, Rainy)

**Texte imprimé / définition** : « Seek a minion from the encounter deck »,
« seek an event from your deck ». Aucune fiche d'insert ne le définit dans les
zips de Rainy (Beta Ray Bill, Ares) ; le plan de portage note qu'il est défini
par l'insert de Spider-Man 2099, non porté. Lecture retenue au dépôt, depuis
`br005` Star Jump et `br011` Hammer Time (01/09/2026), confirmée pour Ares le
07/09/2026 : **chercher la carte demandée dans la zone nommée, la prendre, puis
mélanger cette zone**. C'est un « search » ordinaire, le mot ne change rien à
la règle ; il sert au thème.

**Mécanisme moteur** : aucune primitive dédiée.
- Deck rencontre : `Search.SearchForCard(effect, joueur,
  include_encounter_deck=True, card_type=Minion)` puis `PutIntoPlay(joueur,
  effect)` et `CastTo(Minion).EngagePlayer(joueur, effect)` (`br005`, `br011`).
- En COÛT (« Seek a minion ... → ») : `CostFunc.SearchForCard(Minion,
  "PutIntoPlayEngagedYou", include_encounter_deck=True)`, dont
  `effect.cost_func.Get(CostFunc.SearchForCard).searched_faces` rend le sbire
  convoqué (`56007` Hunted, `ar001a` Ares).
- Deck du joueur : `Search.PlayerCard(effect, joueur, include_player_deck=True,
  card_type=Event)` + `joueur.GainCard` (`br009` Oathbrother).

**Carte exemple** : `ar001a` * Ares (Bring the War) : le sbire convoqué est
le COÛT de l'action, lu dans `searched_faces`, puis engagé avec le joueur.

**Pièges connus** :
- Un coût `SearchForCard` est **offert** même si le deck rencontre ne contient
  aucun sbire (`CostFunc.Base.HasTargets` rend vrai dès que `Select.From("This")`
  a une cible, RECETTES §5) : doubler d'un `conditions=[...]` qui vérifie la
  présence d'un sbire, sinon la carte est jouée pour rien.
- Sans `include_encounter_discard_pile`, la défausse n'est PAS fouillée : le
  texte de Rainy dit « from the encounter deck », on s'y tient.

**Variantes maison** : « Find a Beta Ray Bill card » (`br005`) est un autre
verbe pour la même chose côté deck joueur.

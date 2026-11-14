# Hidden Clause (capacité maison des complots de Mephisto)

**Texte imprimé / définition** : sur les trois complots principaux de Mephisto (1B Battle for the Soul, 2B Fiendish Investment, 3B Hellbound Obsession) : « **Forced Response** : At the end of your turn, resolve the "Hidden Clause" ability for each BARGAIN attachment you control. **Hidden Clause — Special** : Put N<par joueur> card(s) from the top of your deck facedown into Damnation », avec N = 1, 2, 3 selon le stade (1B, 2B, 3B). Il se déclenche donc à la fin du tour de chaque joueur, une fois par attachement BARGAIN qu'il contrôle, et peut aussi être « résolu » par des cartes de rencontre (Alter the Deal, Dark Compulsions, Meager Request, Soul Gambling…). Le nombre de cartes se lit sur le stade courant du complot principal, multiplié par le nombre de joueurs.

**Mécanisme moteur** : à implémenter. Le « Special » du complot est une capacité nommée que les cartes de rencontre appellent ; elle doit s'adresser à un joueur précis (le deck du joueur qui résout) et envoyer les cartes en Damnation (`damnation.md`).

**Carte exemple** : aucune scriptée à ce jour (pack mp non créé).

**Pièges connus** : c'est un « Special » nommé, pas un déclencheur de message du moteur ; plusieurs cartes le résolvent en dehors de la fin de tour. Le N<par joueur> se calcule par rapport au nombre de joueurs de la partie, pas au nombre de joueurs qui contrôlent un Bargain.

**Variantes maison** : tout le mécanisme est maison.

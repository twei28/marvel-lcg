# Shielded by the Horde (maison, scénario `the_hunger_core`, préfixe `hg`)

**Texte imprimé** (livret officiel du scénario, page 4) : « Shielded by the Horde. While any Metazombie is in
play, The Hunger Core cannot be targeted by player cards or abilities, cannot be dealt damage and cannot be
stunned or confused. When no Metazombie is left, the Core has the active token and is **exposed**: it can now be
targeted, dealt damage, stunned and confused. »

**Mécanisme moteur** : réutilise la brique commune du 20/10/2026, `AbilityFactory.CannotBeAffectedByPlayerCards`
(fiche [[immunite-cartes-joueur]]), avec `while_fn=lambda face: NbMetazombiesEnJeu(effect) > 0` (condition relue à
chaque question, pas figée à l'entrée en jeu). Posée sur chacune des trois faces `hg001`/`hg002`/`hg003`.

**Carte exemple** : `hg001`/`hg002`/`hg003` : * The Hunger Core, les trois stades (texte identique hors PV).

**Pièges connus** :

- **La brique ne bloque QUE les cartes joueur**, pas les cartes de rencontre (`PlayerCardImmunity.IsPlayerCardEffect`
  vérifie que la source est une face `PlayerCard`). Le texte dit « cannot be dealt damage » sans restriction, ce qui
  suggérerait un blocage total — mais aucune autre carte du pack ne tente de blesser le Cœur par un canal RENCONTRE
  que [[rupture-x]] (qui, lui, doit justement passer). Dans ce pool de cartes fermé, la portée plus étroite de la
  brique commune et la portée plus large du texte imprimé ne se distinguent jamais en pratique : décision retenue
  pour rester sur la brique existante plutôt que d'en écrire une plus large pour rien. À revoir si un futur ajout au
  pack cible le Cœur par une carte de rencontre autre que Rupture.
- **« Cannot be stunned or confused »** passe par le même crochet `GainStatus` que la brique couvre déjà (sixième
  accroche de `immunity.py`) : aucun code supplémentaire.
- **« Exposed » n'est pas la carte d'état maison du pack `sentinel`** (fiche [[exposed]]) : ici c'est un simple état
  de fait (« no Metazombie in play »), pas un composant physique. Ne pas confondre les deux fiches.
- La bascule « exposed » donne aussi le jeton actif au Cœur : voir `commun.PasserLeJeton`/`JetonApresDefaite`, pas un
  mécanisme séparé.

**Variantes maison** : aucune à ce jour.

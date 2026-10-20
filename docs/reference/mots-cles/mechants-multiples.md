# Plusieurs méchants en jeu : « le méchant », le méchant actif, le deck de méchants

**Texte imprimé / définition** :
- Punisher MC×DC 2026, p180 *Justice or Punishment?* (5B) : « Punisher is the active villain. Encounter cards
  referring to or affecting "the villain" refer only to Punisher. Players may defend any attack, even ones targeting
  enemies. »
- Galactic Storm 1.2 p.16 (Earth Under Siege, « Multiple Villains ») : deck de méchants (un méchant de chaque set mis
  de côté, mélangés face cachée) ; un méchant vaincu est retiré de la partie, ses jetons, états et attachements sont
  défaussés au lieu de passer au suivant ; un méchant révélé se place le plus à DROITE ; « Encounter cards that refer
  to "the villain" only refer to the leftmost villain. Player cards that refer to "the villain" only refer to the
  villain chosen by the player who controls that player card. If a minion takes any amount of excess damage from an
  attack with the overkill keyword, the attacking player must choose which villain that excess damage is dealt to.
  Encounter and player cards attached to a villain that refer to "the villain" only refer to the attached villain. »
- FAQ Rules Reference 1.8 p.62 (Sinister Six) : « The villain with the active counter takes the overkill damage. »

**Mécanisme moteur** : brique commune du 20/10/2026, `src/game/operate/villains.py` (`Villains`, aussi
`Worlds.Villains`). Le scénario pose `Villains.SetRule(effect, Villains.Rule(the_villain="Active"|"Leftmost",
player_cards="TheVillain"|"PlayerChooses"))` ; `Scenario.GetVillain` la lit (après le crochet `GettingVillain` du
scénario, avant l'ordre d'avant). Sans règle, rien ne change. API : `TheVillain`, `All`, `Leftmost`, `Rightmost`,
`Active`, `SetActive`, `Remove`, `BuildVillainDeck`, `RevealNextVillain`, `VillainDeckSize`. Recette :
`RECETTES-MOTEUR.md` §16.3.

**Carte exemple** : aucune carte de campagne portée. Modèles existants pour le compteur actif : Sinister Six
(`sm/sinister_six/27100a.py`, crochet `GetVillain`), Wrecking Crew (`twc/07001a.py`), Four Horsemen
(`aoa/four_horsemen/45085a.py`) ; pour le choix du joueur : Bebop & Rocksteady (`bebop_rocksteady/tk006a.py`).
Cas : `tools/cas/briques_communes.py`, filtre `[briques][mechants]` (7 cas).

**Pièges connus** :
- `Worlds.FindVillain` est appelé par ~250 scripts : ils suivent la règle sans changement, c'est le but. Un
  `SetTarget(Villain)` rend TOUS les méchants (« a villain »), pas « le méchant ».
- `player_cards="PlayerChooses"` pose sa question au moment où le moteur lit « le méchant », une fois par effet ;
  une carte joueur qui lirait `FindVillain` dans une CONDITION la ferait poser pendant une vérification (aucune
  connue à ce jour, voir les questions).
- Le compteur actif disparaît avec le méchant retiré : en règle `Active`, « le méchant » retombe sur le plus à gauche
  tant qu'aucun autre n'est désigné.
- Le deck de méchants n'est PAS `Scenario.villain_deck` (qui porte les stades) ; il est créé à la demande.

**Variantes maison** : aucune.

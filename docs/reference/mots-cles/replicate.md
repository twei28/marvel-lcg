# Replicate (le Special « Réplication » de Baxter's Laboratory)

**Texte imprimé / définition** : sur `tx004b` (Baxter's Laboratory, 1B) : « *Replicate*
— **Special**: Place 1 all-purpose counter on each SWARM minion engaged with you. If
there are no SWARM minions engaged with you, deal yourself a facedown encounter
card. » « Replicate » est le NOM de la capacité ; « Special » est son TYPE (voir
`special.md`, cas 2 : la capacité nommée qu'une AUTRE carte vient résoudre). Les
cartes disent « resolve the "Special" on the Baxter's Laboratory scheme ».

**Qui la résout** : tx001, tx002, tx003 (« each player resolves » au début de la phase du
Méchant), tx011 Mad Lab (« the first player must resolve »), tx008 Radical Ingenuity (au
choix), tx009 Rapid Replication (après la révélation du sbire). Toujours **le joueur** :
« engaged with YOU » et « deal YOURSELF » visent celui qui résout.

**Mécanisme moteur** : `AbilityFactory.WhenResolveSpecialAbility("This", op)` sur
`tx004b` ; les appelants passent par `ResoudreLeSpecial(effect, joueur)`
(`baxter_stockman/__init__.py`), qui cherche le complot `tx004b` en jeu et appelle
`face.ResolveSpecialAbility(joueur, effect)` ; dans l'opération le résolvant est
`message.GetToPlayer()`. Sans le complot en jeu, rien ne se passe.

**« all-purpose counter »** : la FAQ officielle (MC4DB, 29/09/2026, déjà notée dans
`gmw/16034`) dit que la carte qui porte le compteur en définit le type. Chaque sbire SWARM
a SON compteur nommé : swarm (tx007, tx012, td016, td017), ooze (tx013 Superfly), cable
(tx015 Roadkill Rodneys), shield (tx017 Auto Defense Bots). Le moteur sait faire
(`'all-purpose'` → `ConvertAllPurpose`) tant que la carte porte déjà un compteur ; la table
`COMPTEUR_DU_SBIRE` donne le nom par card_id pour qu'un Rodneys sans câble regagne un CÂBLE
et non un compteur générique sans effet.

**Carte exemple** : `tx004b` ; cas `[baxter] tx004b Replicate ...`.

**Pièges connus** :
- les sbires non-SWARM engagés ne comptent pas (une carte face cachée est distribuée) ;
- un SWARM engagé avec l'AUTRE joueur n'est pas touché par le Special de ce joueur ;
- la carte est distribuée face cachée pendant l'interruption de début de phase : elle est
  révélée par l'étape normale de la phase du Méchant, pas tout de suite ;
- `Players.ForEachPlayer` parcourt les joueurs dans l'ordre du tour, premier joueur d'abord.

**Variantes maison** : aucune autre que ce scénario.

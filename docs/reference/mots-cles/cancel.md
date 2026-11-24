# Cancel (annuler les effets d'une carte)

**Texte imprimé / définition** : « cancel all of its effects » : les effets de la carte ne se résolvent pas (Rules Reference, « Cancel »). Pour une carte rencontre révélée, la carte est ensuite défaussée ; ses effets de révélation, sa menace et son surge n'ont pas lieu (« cancel all of its effects and discard it »).

**Mécanisme moteur** : message `WhenPlayerRevealCard` (Interruption, avant la résolution) ; `message.CancelAllEffectsAndDiscardIt(effect)` (modèles `bkw/08008` Grappling Hook, `rainy/90106`, `iron_man_model_42/im011`). Fabrique : `AbilityFactory.WhenPlayerRevealCard(HeroInterrupt, "You", <type de carte ou None>, "All", op)` ; « discard this card → » en coût : `CostFunc.Discard("This")`.

**Carte exemple** : `rr007` Molecularkinesis (Sentry, 03/11/2026) ; `08008` Grappling Hook.

**Pièges connus** : le coût « discard this card » est payé AVANT l'annulation ; un type de carte à `None` accepte toute carte rencontre (sbire, manigance annexe, traîtrise...) ; l'annulation d'une traîtrise annule aussi son surge.

**Variantes maison** : aucune.

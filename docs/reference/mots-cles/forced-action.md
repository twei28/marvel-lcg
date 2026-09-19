# Forced Action

**Texte imprimé / définition** : « Forced Action: <coût> → <effet>. » Ce
n'est pas un mot-clé au sens des règles mais un TYPE de capacité (comme
Hero Action ou Forced Response) : une action que le joueur DOIT effectuer
pendant sa phase de joueur tant qu'elle est possible ; la phase ne peut pas
se terminer avant. Le joueur choisit seulement le moment.

**Mécanisme moteur** : `AbilityType.ForcedAction` (`ability_type.py:56`,
« the player phase cannot end until all possible forced actions among all
players have been performed »). Se code avec
`AbilityFactory.WhenInYourPlayTurn(AbilityType.ForcedAction, op)` et les
coûts en `SetCostFunc` (`CostFunc.Exhaust("This")`, `CostFunc.Counter(...)`).
Tant que le coût est payable, l'action reste proposée et la fin de phase est
bloquée ; quand il ne l'est plus (carte inclinée, pions épuisés), l'action
disparaît et la phase peut finir.

**Carte exemple** : `ls016` : Hypnotic Suggestion (pack `lady_sif`),
`WhenInYourPlayTurn(AbilityType.ForcedAction, hypnotic_suggestion)
.SetCostFunc(CostFunc.Exhaust("This"))`. Dans `fne`, les trois obligations
de Purple Man (`60105` « Fight. », `60106` « Protect. », `60107` « Serve. »)
passent par `ObligationCommandee` (purple_man/__init__.py) : même
fabrique, avec `CostFunc.Exhaust("This")` ET `CostFunc.Counter("This", 1,
'command')`.

**Pièges connus** :
- Deux `SetCostFunc` s'additionnent : incliner ET retirer un pion, jamais
  l'un des deux (piège `wd005`).
- Sous le harnais, on déclenche par `Puzzle.Action(id, 'ForcedAction')`
  (modèles `ls017`, `tg011`) avec une main sans carte jouable
  (`main_exclusive: ["01088"]`), sinon le pilote joue d'abord ses cartes et
  fausse la mesure (RECETTES-MOTEUR §7ter).
- Une Forced Action sur une carte à `Uses (N ... counters)` s'éteint avec le
  dernier pion : la sortie de la carte est native (voir `uses.md`), ne pas la
  recoder.

**Variantes maison** : aucune recensée pour l'instant.

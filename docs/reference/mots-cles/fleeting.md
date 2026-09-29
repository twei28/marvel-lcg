# Fleeting (mot-clé maison, aspect Determination)

**Texte imprimé / définition** : « Fleeting. *(This card must be discarded
from play at the end of the phase.)* » (`dt087` "Get 'Em, Boom-Boom!", seul
porteur du dépôt).

Définition MC4DB (règle `fanmade`, 29/09/2026) : « After the phase ends,
discard this card. » Même sens.

**Mécanisme moteur** : aucun crochet natif, le moteur ne lit aucun mot-clé
dans le texte. Aptitude écrite UNE fois, `Fleeting()` dans
`src/cards/pack/determination/__init__.py` (depuis le 29/09/2026 ; avant
cela le mot-clé n'était implémenté nulle part et `dt087` restait attachée
jusqu'à la défaite de l'ennemi) :

- `AbilityFactory.WhenPhaseEnd(AbilityType.ForcedResponse, None,
  DiscardThisCard, conditions=[en_jeu])` : `phase_name=None` = la PREMIÈRE
  fin de phase qui suit l'entrée en jeu, quelle que soit la phase ; la
  condition `IsInPlay()` évite de défausser une carte encore en main.
- La défausse passe par `Faces.DiscardAll`, donc par la fenêtre
  `WhenCardWouldDiscard` (`card.py:635`) : l'Interrupt de départ de `dt087`
  part bien au moment où Fleeting la défausse.

Modèle : `44032` The Merc with the Mouth (`WhenPlayerPhaseEnd` +
`DiscardThisCard`). Preuve : cas `dt087 ... [dt] — Fleeting` de
`tools/test_capacites.py` (vérificateur `dt087_fleeting_fin_de_phase`, qui
envoie lui-même `Message.WhenPhaseEnd`, l'API Puzzle n'avançant aucune
phase), vu rouge puis vert ; gabarit dans
`.planning/todos/2026-09-29-fleeting-alias-gabarits-processus-carte.md`.

**Carte exemple** : `dt087` "Get 'Em, Boom-Boom!" : `Fleeting()` +
`AfterUnitTookDamage` (Hero Response, s'attache à un ennemi) +
`WhenCardWouldDiscard` (1 dégât à chaque ennemi).

**Pièges connus** :
- « At the end of the phase » : la phase où la carte est ENTRÉE en jeu
  (elle arrive en phase vilain, après des dégâts subis), pas la fin du round.
  Un montage sur `AfterRoundEnd` serait faux.
- La carte n'a pas de mise en jeu ordinaire (pas de `CanPlayThisUpgradeCard`,
  voir son commentaire) : l'aptitude Fleeting ne doit pas en ajouter une.

**Variantes maison** : aucune ; mot-clé absent du jeu officiel.

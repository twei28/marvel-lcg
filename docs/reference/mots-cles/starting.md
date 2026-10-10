# Starting

**Texte imprimé / définition** : livret Fear No Evil (`assets/docs/mc60_fear_no_evil_rulebook.pdf`, p.3) :
« A card with starting may be added to its owner's starting hand during setup. Each deck cannot include more than one
card with starting. Before drawing their starting hand during player setup, each player with a starting card in their
deck may search their deck for that card and add it as the first card of their starting hand. That card does count
against their hand size and can be discarded for the mulligan. »

**Mécanisme moteur** : aucun support natif, chaque carte le code elle-même par `WhenGameBeginSetup`, qui pose un CHOIX
facultatif (`player.MayChooseOneAbility`, option « Add this card to your starting hand » ou Annuler) puis
`Faces.AddToHand`. La pioche de la main de départ vient après et complète jusqu'à la taille de main : la carte compte
donc dans la main.

**Carte exemple** : `60038` : Innate Reflexes (`src/cards/pack/fne/60038.py`) ; même code pour `61034`, `61036`,
`61037` (Innate Aggression, Perception, Inspiration).

**Pièges connus** :
- Le « may » : jusqu'au 09/10/2026 les quatre cartes s'ajoutaient d'office, sans question (signalement Yarro n°70).
- Le moteur nomme l'option avec des soulignés (`Add_this_card_to_your_starting_hand`) dans `/get_ask` ; le plateau
  la traduit par `vocabulaire-moteur.ts` (« Ajouter cette carte à ta main de départ »).
- « Une seule carte starting par deck » (une CARTE : deux exemplaires d'un titre sont aussi refusés) est contrôlé par
  `validerDeck` (`public/js/deckbuilder/regles.js`), qui reconnaît le mot-clé au début du texte anglais
  (`/(^|\n)\s*Starting\b/`). Test : `tools/tests-lanceur/regles-starting.test.mjs`.
- Preuve à l'écran : `ui-check/tests/starting-mise-en-place.spec.ts` (FR/EN, Ajouter/Annuler, 1920 et 360 px).

**Variantes maison** : aucune.

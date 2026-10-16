# Dredge (compteur de dragage, pack `venus`, TMNT Heroes)

**Texte imprimé / définition** : « Place 1 dredge counter on Venus for each
[[ELEMENT]] upgrade you control (to a maximum of 6) » (`tv001a`) ; « Remove X dredge
counters from Venus → ... » (`tv003`) ; « Remove 2 dredge counters from Venus → ... »
(`tv010`, `tv012`, `tv013`) ; « You may remove 2 dredge counters from Venus to ... »
(`tv004`, `tv006`, `tv007`) ; « Remove 1 dredge counter from Bonnie → ... » (`tv001b`,
`tv011`). Ce n'est PAS un mot-clé avec une règle propre : un COMPTEUR maison, jamais
défini par l'auteur au-delà de ses usages (aucun insert dans le zip, `Venus v3/`).

**Mécanisme moteur** : compteur `dredge` ajouté à l'énum `COUNTER` de
`src/game/card/face/card_face.py`, posé sur la carte d'IDENTITÉ : Venus et Bonnie sont les
deux faces d'une même carte et partagent le même stock (modèle `rage` de Raphael, pack
`raphael`). Helpers : `src/cards/pack/venus/venus/__init__.py` (`PlacerDragage`, `Dragage`,
`PeutRetirerDragage`, `ProposerRetraitDragage`). Retrait en COÛT par
`CostFunc.Counter("YourIdentity", n, 'dredge')` ; « you MAY remove ... to » = un choix
`MayChooseOneAbility` dont la branche porte le coût (modèle `01165` Eviction Notice).

**Carte exemple** : `tv001a` * Venus (pose, plafond 6), `tv004` Brain Burn (retrait
facultatif), `tv003` Arc Nova (X choisi).

**Pièges connus** :
- « (to a maximum of 6) » : lecture provisoire = plafond du STOCK de l'identité
  (`maximum=6` de `PlaceCountersOn`), question Q1 de `.planning/tmnt/venus-questions.md` ;
- « Venus » / « Bonnie » désignent l'IDENTITÉ, dans les deux formes (décision du
  15/10/2026 pour « Raphael » en civil) : `tv011` Dragon Scale se paie donc aussi en forme
  Bonnie ;
- « Remove X » avec X = 0 légal (`tv003`) : `CostFunc.Counter` refuse un retrait de 0,
  le retrait est donc fait à la main, après `DeclareNumber(0, compteurs)` ;
- une ressource à coût de compteur (`tv011`) EXIGE `conditions=[...]` : sans elle la
  ressource est offerte sans compteur et le moteur annule toute la carte en cours de
  paiement (RECETTES §4) ;
- le choix « Cancel » d'un `MayChooseOneAbility` est une option nommée « Cancel », pas
  un bouton Passer (`choisir_option: ["Cancel"]` dans les cas).

**Variantes maison** : aucune.

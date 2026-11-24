# Bargain (trait maison, scénario Mephisto, Neptune)

**Texte imprimé / définition** : trait « BARGAIN. » des attachements de rencontre du scénario Mephisto (09 Endless Greed à 15 Unquenchable Envy, Black-Hearted, Lilin Remaking, et les 4 attachements de Corruptive Offers). Tous portent Peril et le même *When Revealed* : « You may attach this card to your identity. If you do not, discard this card and the villain (Mephisto) activates against you. » Un attachement accepté donne un pouvoir à l'identité et porte un *Response* : « After your turn begins, discard this card → Mephisto activates against you. Apply this card's boost icons for this activation as if it were a boost card. » Un joueur qui contrôle un Bargain déclenche aussi le « Hidden Clause » du complot principal (voir `hidden-clause.md`) et empêche Mephisto d'agir contre lui (il se soigne à la place).

**Mécanisme moteur** : trait déclaré dans `TRAITS` (`card_face.py`, ajouté le 09/11/2026). Aucune règle du moteur n'y est attachée : tout vit dans les scripts des cartes. À implémenter : le choix à la révélation (attacher à l'identité ou défausser + activation), l'application des icônes de boost de la carte lors de l'activation forcée (`boost.md`), le comptage « each BARGAIN attachment in play / you control » (sélecteur par trait).

**Carte exemple** : aucune scriptée à ce jour (pack mp non créé).

**Pièges connus** : l'image d'ensemble `Corruptive Offers.png` montre un ancien texte (trait Condition, « Choose: », Action pour défausser) ; on suit les PNG individuels, conformes à l'encart de règles. « Peril » sur ces cartes : voir `peril.md`.

**Variantes maison** : tout le mécanisme est maison.

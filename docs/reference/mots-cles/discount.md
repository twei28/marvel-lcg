# Discount X (<trait>)

**Texte imprimé / définition** : « [star] Discount 1 ([[MARTIAL ARTIST]]). » Mot-clé officiel du coffret
Fear No Evil (60023 Know Your Enemy, 60027 Move in Shadow) repris par les aspects TMNT (Inkwire) :
réduit de X le coût pour jouer la carte si vous contrôlez une carte qui a le trait indiqué (plusieurs traits
séparés par « or » = l'un d'eux suffit). L'étoile du coût (« 3★ ») n'est qu'un rappel (Star Icon).

**Mécanisme moteur** : helper `DiscountAbility(X, [traits])` de `src/cards/pack/fne/__init__.py`
(`AbilityFactory.ReduceCostToPlayThis(X, conditions=[contrôle d'une carte au trait])`). Une carte hors du pack
`fne` l'importe par `from cards.pack.fne import DiscountAbility`. `desc.Cost` garde l'étoile (`"3*"`).

**Carte exemple** : `60023` Know Your Enemy ; aspect TMNT : `ua030` Nerve Strike (Aggression).

**Pièges connus** : la condition lit TOUTES les cartes en jeu contrôlées par le joueur (identité, alliés,
améliorations), pas seulement l'identité. Le coût réduit ne descend pas sous 0 (moteur).

**Variantes maison** : aucune.

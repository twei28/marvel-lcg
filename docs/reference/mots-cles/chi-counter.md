# Compteur « chi » (Iron Fist officiel MC64EN, et deux usages plus anciens)

**Texte imprimé / définition** : un compteur nommé, sans règle propre. Sur le héros officiel
**Iron Fist** (Hero Pack MC64EN, novembre 2026), il est posé sur la carte d'identité par la face
héros 64001a (« *Martial Arts Master* — **Response** : After you play a card, place 1 chi counter
here. **Forced Response** : After the player phase ends, remove all but 4 chi counters from here and
heal 1 damage for each chi counter removed this way ») puis dépensé par les cartes signature
(« remove N chi counters from Iron Fist / from your identity → … »). Embody the Dragon (64009) en
reçoit sur elle-même (« Move 1 chi counter from Iron Fist to this card ») et en tire sa riposte.

Deux usages plus anciens, indépendants : `21012` Power Man (Victor Alvarez, « enters play with
2 chi counters ») et `sh010` Martial Skill (TMNT Shinobi, `Uses (2 chi counters)`).

**Mécanisme moteur** : `'chi'` figure dans `CardFace.COUNTER` (`card_face.py`) depuis l'origine du
dépôt ; le plateau l'affiche (`compteurs-fr.ts` : « chi »). Les compteurs vivent dans le composant
`Counter` de la **carte** (`component/counter.py`), pas de la face : Iron Fist et Danny Rand
partagent donc le même stock, qui **reste au retournement** (décision utilisateur n°5 du
19/10/2026, Rules Reference : un personnage garde ses jetons en changeant de forme).

- poser : `Faces.PlaceCountersOn([identite], 1, 'chi', effect)` ;
- dépenser EN COÛT (flèche) : `CostFunc.Counter("YourIdentity", n, 'chi')`, doublé d'une
  `conditions=[AuMoinsChi(n)]` (helper du set `iron_fist/iron_fist/__init__.py`) pour que la
  capacité ne soit pas offerte quand le coût est impayable ;
- dépenser un nombre CHOISI (Dragon Punch, « up to 5 ») : `joueur.DeclareNumber(0, min(5, n))`
  puis `Faces.RemoveCountersOn` (modèle `venus/tv003` Arc Nova) ;
- valeur dynamique d'un mot-clé : `GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You",
  retaliate=1, get_new_value=..., change_on_event=OnEvent.Counter("This", 'chi'))` (64009).

**Carte exemple** : `64001a` Iron Fist (pose), `64006` Lei Kung (coût double incliner + 1 chi),
`64009` Embody the Dragon (déplacement + riposte X).

**Pièges connus** :
- « here » sur la face héros = la carte d'identité : le stock se lit sur `joueur.GetIdentity()`,
  quelle que soit la forme (clé de cas `compteurs_identite`) ;
- la Forced Response de fin de phase n'existe que face héros visible : en Danny Rand, le stock
  peut dépasser 4 et y rester ;
- un `CostFunc.Counter` SANS condition est offert même impayable (RECETTES §5) ;
- `Power Man` (21012) et `Martial Skill` (sh010) partagent le NOM du compteur : un chi posé sur
  eux n'est pas sur l'identité et ne paie rien chez Iron Fist (les capacités lisent l'identité).

**Variantes maison** : aucune.

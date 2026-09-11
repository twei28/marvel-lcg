# Villainous

**Texte imprimé / définition** : « Villainous. *(When this minion activates,
give it a boost card.)* » Un sbire Villainous reçoit une carte de boost à
chacune de ses activations, exactement comme le vilain. Cela n'a **aucun
rapport avec les règles d'engagement**. C'est un compteur (`Villainous 1`,
`Villainous 2`, ...), réinitialisé à sa valeur imprimée à chaque reset des
mots-clés.

**Mécanisme moteur** : clé `desc.Villainous` sur la carte, lue nativement par
le moteur. `HasVillainous`
(`src/game/card/face/attribute/has_villainous.py`) enregistre l'attribut
`Villainous` -> `printed_villainous`, restaure la valeur à chaque
`OnResetKeywords` via `GainVillainous`, et hérite de `CanBoost` pour surcharger
`GetBoostCardNum()`, qui retourne 1 si `IsVillainous()` et 0 sinon. Ce
`GetBoostCardNum()` est consulté à chaque activation : par `can_attack.py`
(appel à `GiveFacedownBoostCardsInternal(GetBoostCardNum(...) +
additional_boost_card, ...)`) pour une attaque, et par `can_scheme.py` pour un
plan. C'est la même surcharge que celle de `Villain.GetBoostCardNum()`
(`src/game/card/face/base/villain.py`), qui renvoie 1 sans condition : un sbire
Villainous se comporte donc, pour le boost, comme le vilain. **Aucun script
requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `11041` : * Deathunt 9000 (`desc` contient `"Villainous":
"1"`, plus `"Toughness": "1"`), lu directement depuis `desc`, aucun script
requis pour le mot-clé. Le fichier `11041.py` existe et code la capacité
imprimée `[star] Boost` (« Give this enemy a tough status card and another
boost card », via `AbilityFactory.WhenCardBecomeBoost`), pas le mot-clé
Villainous.

**Pièges connus** :
- Villainous ne modifie **pas** les règles d'engagement. C'est une source de
  carte de boost à l'activation, rien d'autre.
- Ne pas confondre avec `desc.Boost` (`HasBoostIcon`,
  `src/game/card/face/attribute/has_boost_icon.py`, attribut
  `printed_boost`) : cette clé-là compte les icônes de boost imprimées sur la
  carte quand ELLE sert de boost à quelqu'un d'autre. `11041` n'a d'ailleurs
  aucune clé `Boost`, contrairement à `01101` ou `16119`.
- Mot-clé de sbire uniquement.
- Si une future carte cumule Villainous avec une capacité imprimée distincte
  (c'est le cas de `11041`), vérifier via `find` si un script existe : le script
  devra porter uniquement cette capacité annexe, jamais le mot-clé Villainous
  lui-même.

**Variantes maison** : aucune recensée pour l'instant.


## Variante : un HÉROS qui gagne Villainous (dd001a Doctor Doom, hc010 Outer Demons)

Depuis le 01/09/2026, `Hero` hérite de `HasVillainous` : un héros villainous
reçoit une carte boost à chaque **attaque de base** (`can_attack.py:264`),
ses icônes s'ajoutent à l'ATQ, et `ResolveBoostCards` envoie les messages
`WhenBoostCardTurnedFaceUp` (une carte peut donc y réagir : hc010 annule
l'effet Boost et soigne 1). Deux façons de l'accorder :

- temporaire : `hero.GainUntilRoundEnd(effect, villainous=1)` (dd001a) ;
- continu, par une amélioration : `*GiveKeywordToAttached(CardFinder(name=…),
  villainous=1)` (hc010, paramètre ajouté le 11/09/2026 à `asset.py` et
  `asset_helper.py`).

⚠ **Attaque seulement.** Le contre de base ne distribue pas de boost
(`can_thwart.py` n'a pas l'équivalent). Écart assumé sur les deux packs, noté
dans leurs gabarits. Les effets [star] Boost des cartes de rencontre ne se
déclenchent que sur une activation d'ENNEMI : pour un héros, seule l'icône
compte.

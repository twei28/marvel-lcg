# Alliance

**Texte imprimé / définition** : « Alliance. *(The players can pay this card's
costs as a group.)* » Les joueurs peuvent financer le coût de la carte
collectivement, chacun depuis sa propre main. Le mot-clé ne fait que cela : il
ouvre le paiement, il ne dit rien de l'effet, qui reste celui du texte imprimé
en dessous.

**Mécanisme moteur** : clé `desc.Alliance` sur la carte, lue nativement par le
moteur, exactement comme Toughness, Guard, Patrol ou Retaliate. `HasAlliance`
(`src/game/card/face/attribute/has_alliance.py`) enregistre l'attribut
`Alliance` -> `alliance` en **booléen** ; il est mêlé au type `Event`
(`src/game/card/face/card_type/event.py` : `class Event(HasTeamUp, HasAlliance,
ClassCard, FinalType)`), donc réservé aux événements. Le drapeau est consulté à
deux endroits :

- `src/game/ability/factory/resources.py` (deux occurrences, dans les contrôles
  de paiement) : `if Event.IsType(message.paying_for_effect.this): if
  message.paying_for_effect.this.alliance: return True` ;
- `src/game/event/manager.py` : sur un `Message.WhenPlayerPayingResources`, le
  joueur à contrôler devient `message.to_player` quand l'événement payé porte
  `alliance`.

**Aucun script requis** pour le mot-clé lui-même : c'est une des « bases
automatiques » du guide.

**Carte exemple** : `25036` : Cosmic Alliance, pack `valk` (`desc` contient
`"Alliance": "1"`), lu directement depuis `desc`. Un fichier `25036.py` existe
bien, mais il ne code que la **Hero Action** imprimée (« Choose an AVENGER
character and a GUARDIAN character → ready each of those characters », via
`AbilityFactory.WhenInYourPlayTurn` + `Faces.ReadyAll`), jamais le mot-clé.
Même schéma pour `26035` (Joining Forces, pack `vision`) et `40053` (Team
Investigation, pack `next_evol`, dont le `.py` ne porte que le
`RemoveThreatFromSchemes`).

Le catalogue compte **16 cartes** avec `desc.Alliance` (23032, 23034, 25033,
25036, 26035, 40053, 42031, 44046, 47028, 47029, 48031, 48032, 53019, dt061,
dt115, wd136). Seules quatre d'entre elles impriment le rappel entre
parenthèses (`25036`, `26035`, `40053`, `42031`) ; sur les autres, « Alliance. »
est écrit seul, sans rappel, comme le note le commentaire en tête de
`dt061.py`. Le comportement moteur est identique dans les deux cas.

**Pièges connus** :
- Alliance ne s'applique qu'au **financement des coûts**, jamais aux autres
  mécaniques (dégâts, menace, etc.). L'autre joueur peut contribuer à payer,
  mais le propriétaire de la carte reste maître de l'effet.
- Le drapeau est **booléen et réservé aux événements** (`Event` hérite de
  `HasAlliance`). Le poser sur un autre type de carte n'aurait aucun effet.
- **Ne pas confondre avec Coordinated Effort (`58032`, pack `wonder_man`)** :
  cette carte ne porte PAS le mot-clé Alliance imprimé, et son `desc` n'a pas
  de clé `Alliance`. Son texte est « Attach to an encounter card in play. Max 1
  per encounter card. While paying costs on attached card, any player may help
  pay those costs. » C'est un mécanisme distinct, proche dans l'esprit
  (« laisser un autre joueur aider à payer ») mais géré par le crochet
  `CheckAnyPlayerMayHelpPay()` de
  `src/game/ability/factory/resources.py`, un **CORRECTIF maison** (voir §9 du
  guide) qui teste la présence d'un attachement nommé « Coordinated Effort ».
  Ce crochet est appelé en `or` juste après le test natif `.alliance`, ce qui
  explique la ressemblance de comportement sans qu'il s'agisse du même
  mot-clé. Le script `58032.py` ne code d'ailleurs que la restriction
  d'attachement (`CanPlayThisUpgradeCard(CardFinder(card_type=EncounterCard))`).
- Si une future carte cumule Alliance avec une capacité imprimée distincte
  (c'est le cas des trois cartes ci-dessus), vérifier via `find` si un script
  existe : le script devra porter uniquement cette capacité annexe, jamais le
  mot-clé Alliance lui-même.

**Variante `sk280` Princess Anelle (15/10/2026)** : « Alliance. » est imprimé sur un SOUTIEN de campagne (Skrull Menace),
alors que `HasAlliance` est réservé aux événements. Aucun script de mot-clé : la capacité de JEU du soutien est marquée
`ability.cout_en_groupe = True` (même marque que `sk189a` « You are a Skrull! »), que `CheckAnyPlayerMayHelpPay`
(`resources.py`) lit pour ouvrir le paiement à tous les joueurs ; la carte `sk201` Mistrust and Paranoia le ferme
(`PaiementEnGroupeInterdit`), comme pour le mot-clé natif. Cas `sk280 ... ALLIANCE (2 joueurs)`.

**Variantes maison** : **Forces Combined** (`cd003`, pack `cloak_dagger`) est le
second usager du crochet `CheckAnyPlayerMayHelpPay`, et pas du mot-clé Alliance
(son `desc` ne contient que `Class` et `Permanent`). Son texte imprimé est
« Interrupt: When you would spend resources on a card or ability, exhaust
Forces Combined → you may spend resources from both of your hands for that card
or ability. » Le crochet parcourt les cartes contrôlées et renvoie vrai dès
qu'une carte nommée « Forces Combined » est en jeu et **prête** ; l'inclinaison
elle-même est portée par la capacité de `cd003.py`, pas par le contrôle. C'est
un écart documenté au §9 du guide, cohérent avec la mécanique des deux
identités liées Cloak & Dagger (`linked_identity`).

**Note historique** : le brief du plan mentionnait la card_id `70003` pour
Forces Combined, mais cet identifiant est périmé (ancien schéma de
numérotation). La carte réelle utilise l'identifiant `cd003` du pack
`cloak_dagger`.

# Boost (icônes) et Boost ★ (effet)

**Texte imprimé / définition** : deux choses distinctes, que la même fiche
couvre parce qu'elles se lisent au même endroit sur la carte.
1. Les **icônes de boost**, en bas à droite d'une carte de rencontre : chaque
   icône ajoute 1 à l'attaque ou à la manigance du vilain quand la carte est
   retournée comme carte de boost.
2. L'**effet Boost ★**, une ligne « [star] **Boost** : … » sous un trait
   horizontal, qui se résout quand la carte est retournée comme carte de boost.

**Mécanisme moteur** :
- **Icônes = base automatique.** Clé `desc.Boost`, en CHAÎNE :
  `"Boost": "2"`. Enregistrée par
  `src/game/card/face/attribute/has_boost_icon.py` (`RegisterAttribute("Boost",
  "printed_boost")`), comptée à la révélation par `CountBoostIconsInternal`.
  Portée par `EncounterNonVillainCard` (traîtrise, complot annexe, attachement,
  environnement) et par `Enemy` (vilain, sbire). `"Boost": "0"` est légitime.
- **Effet ★ = script obligatoire.** Aucune clé `desc`. Deux endroits :
  - dans `data/cards.json`, uniquement le TEXTE imprimé, dans le champ racine
    `text`, séparé du reste par `\n<hr />\n` puis
    `[star] <b>Boost</b>: <effet>` ;
  - dans le module, une capacité
    `AbilityFactory.WhenCardBecomeBoost("This", operation)`
    (`src/game/ability/factory/boost.py`, type `AbilityType.Boost`).
- Le moteur ne lit PAS le texte : `has_boost_icon.py` calcule `boost_star` en
  cherchant une capacité de type `AbilityType.Boost`. Écrire la ligne
  « [star] Boost » sans écrire l'`Ability` ne crée aucune étoile.

**Carte exemple** : `01099` (Charge, pack `core`) pour les icônes seules
(`{"Boost": "2", "ATK+": "3"}`, aucun script). `an013` (* Hel-Wolf, pack
`angela`) pour le gabarit complet : `desc.Boost = "2"`, une capacité étoilée
permanente ET un `WhenCardBecomeBoost`.

**Pièges connus** :
- L'attaque en cours, pendant un effet de boost, se lit
  `message.would_atk_message` — à récupérer avec `getattr(..., None)`, elle
  n'existe pas si le boost sert une manigance.
- Ne pas confondre le `[star]` d'un effet Boost (sous le trait) et le `[star]`
  d'une capacité permanente (au-dessus) : le second est un
  `AbilityType.NonKeywordStar`, voir [[special]].
- Les icônes de boost d'un SBIRE comptent quand ce sbire est retourné comme
  carte de boost, pas quand il est en jeu.
- **Tester « une carte de boost supplémentaire »** : les cartes de boost sont
  défaussées en fin d'activation, l'état final n'en garde rien. Clé de
  harnais `boosts_sur: [[card_id, n]]` (ajoutée le 20/10/2026, Nyx `ze013`,
  Total Eclipse `ze016`), avec un deck Rencontre réduit à une carte à boost
  connu (Shocker `01103`) pour que les dégâts soient déterministes. Détail :
  `RECETTES-MOTEUR.md` §7.

**Variantes maison** : `gb010` (Necro-Raven, pack `gorr`) : le ★ Boost met le
sbire en jeu engagé avec le joueur au lieu de l'envoyer à la défausse, et se
cumule avec la Réponse Obligatoire d'entrée en jeu de la carte.

# Plotting

**Texte imprimé / définition** : « Plotting. (After this minion engages your
identity, it schemes.) »

**Mécanisme moteur** : pas un compteur `desc` (contrairement à
Quickstrike/Incite/Surge) : déclenché par `AbilityFactory.AfterMinionEngagePlayer`
(`src/game/ability/factory/minion.py`) ciblant `"This"` contre `"You"`, qui
appelle `this.CastTo(Minion).BasicSchemes(effect)` — une action SCH de base
contre le complot principal, sans cible explicite à fournir (symétrique de
`BasicAttacks`, voir `can_scheme.py:166`).

**Carte exemple** : `ok021` (`* Malice`, pack `okoye`) porte le même
mécanisme (« Malice schemes » après un déclencheur différent), sans le
nommer par un mot-clé — `this.CastTo(Minion).BasicSchemes(effect)` dans
`src/cards/pack/okoye/okoye_nemesis/ok021.py`.

**Pièges connus** : le trigger est `AfterMinionEngagePlayer`, pas
`AfterMinionEngageYou`/attaque — bien vérifier qu'il se déclenche à
l'engagement, pas à l'activation suivante du sbire.

**Variantes maison** : `ss019` (`* Bella Donna`, pack `scarlet_spider`,
CptScorp) est la première carte à nommer ce mécanisme « Plotting » avec
texte de rappel entre parenthèses, façon mot-clé officiel. `vp015` (`* Guzz`,
pack `venompool`, même auteur) le reprend à l'identique, à un mot près dans
le rappel : « After this minion engages **you**, it schemes » au lieu de
« engages **your identity** ». Même mécanisme, même déclencheur
`AfterMinionEngagePlayer` : la différence est rédactionnelle, pas mécanique.

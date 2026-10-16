# Daze

**Texte imprimé / définition** : le mot est imprimé en verbe, sans rappel entre
parenthèses :
- `ta002` * Nobody : « [star] **Response**: After Nobody attacks an enemy with
  Prey attached, daze that enemy. » ;
- `ta003` Bold Strategy : « **Hero Action**: Cloak Alopex. You may spend up to 3
  [mental] resources to daze an enemy for each [mental] resource spent this way. »

**Définition (insert « Dazed Rules », zip « TMNT Enemies / Baxter Stockman v3 »,
Inkwire)** : « When you are instructed to "Daze" a character, you must place a
Dazed status card on that character. » « Daze X » = **poser une carte d'état
Dazed sur X**. Même construction que « Cloak X » (fiche `cloak.md`).

**Mécanisme moteur** : `Faces.GiveStatus([cible], "Dazed", effect)`
(= `cible.GainStatus("Dazed", effect)`). La règle vit sur la carte d'état :
fiche `dazed.md`. `GainStatus` refuse une seconde carte Dazed sur un personnage
qui en porte déjà une (insert : « a character can only have one Dazed status
card »), sans lever d'erreur : `Faces.GiveStatus` rend alors 0.

**Carte exemple** : `ta003` Bold Strategy (« daze an enemy for each [mental]
resource spent » : un ennemi choisi par ressource, parmi ceux qui ne sont pas
déjà Dazed), `ta002` Nobody (« daze that enemy »).

**Pièges connus** :
- « Daze » n'est PAS « stun » ni « confuse » : c'est une cinquième famille de
  carte d'état, avec ses deux déclencheurs (voir `dazed.md`).
- Stalwart et Steady n'empêchent pas de poser Dazed (insert : « Can I Daze a
  steady/stalwart character? Yes »).
- « for each resource spent » : un ennemi PAR ressource ; deux ressources sur le
  même ennemi n'y posent qu'une carte (le moteur ne propose donc que les ennemis
  non Dazed).
- `ta002` : si l'attaque de Nobody vainc l'ennemi (donc sa Prey part), il n'y a
  plus d'ennemi à étourdir : rien ne se passe.

**Variantes maison** : aucune.

**Preuves** : `tools/cas/dazed.py` (cartes d'état) et `tools/cas/tmnt_alopex.py`
(cas `ta002` et `ta003`).

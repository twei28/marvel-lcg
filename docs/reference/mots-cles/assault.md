# Assault

**Texte imprimé / définition** : « Assault. » Mot-clé officiel (Next Evolution, `40087` Territorial Control,
`40189` Mutant Insurrection ; rappel imprimé : « Basic thwarts against this scheme use ATK instead of THW »).
Livret Galactic Storm 1.2 p.3 : « when a character makes a basic thwart on a scheme with the assault keyword,
that character uses its ATK instead of its THW. If that character is an ally, it takes the consequential damage
listed under its ATK instead of its THW after the thwart. »

**Mécanisme moteur** : clé `desc.Assault` (`"Assault": "1"`), lue nativement par
`src/game/card/face/attribute/has_assault.py` (`HasAssault`, porté par toute manigance `Scheme2`) : une capacité
de règle `WhenUnitThwartScheme(.., which_card_be_thwart="This", is_basic_thwart=True)` ajoute `ATQ - CTR` au
contre de base en cours. `GiveKeywordToAttached(assault=..)` / `face_gain.py` savent aussi l'accorder.
**Aucun script requis.**

**Carte exemple** : `40087` Territorial Control (lu directement depuis `desc`) ; `gs119` Imprisoned on Chandilar
(Galactic Storm, scénario Majestrix's Verdict), cas `[mv] gs119 Assault` : le contre de base de Spider-Man
(CTR 1, ATQ 2) retire 2 menaces.

**Pièges connus** :
- seul le contre DE BASE est concerné : une carte « remove N threat » n'est pas touchée ;
- la phrase du livret sur les dégâts CONSÉCUTIFS d'un allié (ceux de l'ATQ au lieu de ceux du CTR) n'est pas
  visible dans `has_assault.py`, qui ne règle que la valeur : non mesurée au 20/10/2026, à vérifier en partie
  réelle avec un allié aux dégâts consécutifs différents (Ch'od `gs122` : CTR 1★, ATQ 3★★).

**Variantes maison** : aucune ; `dodgy.md` (TMNT) en est un cousin facultatif.

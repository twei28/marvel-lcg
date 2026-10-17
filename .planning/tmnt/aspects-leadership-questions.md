# Aspect TMNT Leadership (`ul`) : questions ouvertes pour l'utilisateur

16/10/2026, agent Leadership. Une question par carte, multichoix, option recommandée en premier.
Scans : `scratchpad/zip-aspect/TMNT Aspect/Leadership/<fichier>` (zip « TMNT Aspect », Inkwire).
Chaque carte concernée est CONSTRUITE et TESTÉE selon l'option recommandée, mais reste « Carte terminée :
NON » dans `aspects-leadership-gabarits.md` tant que la réponse n'est pas donnée.

Déjà tranché (16/10/2026) : Q-R1 (bandeau « ✦ <titre d'origine> » → `unique_also`, appliqué à ul017,
ul019, ul020, ul021, ul037, ul046) ; Rampage avec deck court (jouable).

---

## Q-UL-1 — `ul001` Alopex (allié) contre l'identité Alopex (`ta001a/b`)
Scan : `Leadership/Alopex.png`. L'allié s'appelle « ✦ Alopex », comme le héros Alopex du pack `alopex`.
Règle d'unicité : deux cartes uniques de même titre ne peuvent pas être en jeu ensemble ; avec Alopex
comme identité, l'allié Alopex n'est donc jamais jouable.
- **A (recommandé)** : règle d'unicité normale (ce qui est codé) : le joueur Alopex ne peut pas jouer
  l'allié ; les autres héros, si.
- B : exception maison : l'allié et l'héroïne coexistent (il faudrait une clé « titre de règles » distincte).
- C : interdire l'allié dans le deck d'Alopex au deck-builder (en plus de A).
- Autre (précise).

## Q-UL-2 — `ul029` Splinter (allié Leadership) contre `tl002` Splinter (allié du kit de Leonardo)
Scan : `Leadership/Splinter.png`. Deux alliés uniques « ✦ Splinter » aux textes différents.
- **A (recommandé)** : même titre = même personnage : jamais les deux en jeu en même temps (codé,
  `CanCoexistWith`). Un joueur Leonardo peut avoir les deux dans son deck mais n'en pose qu'un.
- B : ce sont deux personnages distincts pour les règles : ils coexistent.
- C : A, et le deck-builder interdit de mettre les deux dans le même deck.
- Autre (précise).

## Q-UL-3 — `ul039` Venus « Bonnie » (allié) contre l'identité Venus (`tv001a`)
Scan : `Leadership/Venus.png`. Même problème que Q-UL-1.
- **A (recommandé)** : unicité normale (codé) : le joueur Venus ne peut pas poser l'alliée.
- B : exception : elles coexistent.
- Autre (précise).

## Q-UL-4 — `ul019` Old Hob : trait « MUTANIMALS » (pluriel)
Scan : `Leadership/Old Hob.png` (coquille connue de la consigne). Toutes les autres cartes impriment
MUTANIMAL ; `ul028` Splinter Dojo Training dit « Attach to a NINJA or MUTANIMAL ally ».
- **A (recommandé)** : coquille : Old Hob a le trait MUTANIMAL (Splinter Dojo Training s'y attache).
- B : suivre le scan à la lettre : MUTANIMALS, et Splinter Dojo Training ne s'y attache PAS (codé en attendant).
- Autre (précise).

## Q-UL-5 — `ul033` Take a Stand sans le trait TACTIC
Scan : `Leadership/Take a Stand.png`. L'officielle `62015` porte TACTIC ; le scan n'imprime aucun trait.
Effet en jeu : les cartes qui comptent ou cherchent des TACTIC ne la voient pas.
- **A (recommandé)** : oubli de l'auteur : ajouter TACTIC (comme l'officielle).
- B : suivre le scan : aucun trait (codé en attendant).
- Autre (précise).

## Q-UL-6 — `ul031` Suit Up : « attached to AN ally » au lieu de « to THAT ally »
Scan : `Leadership/Suit Up.png`. Officielle `45017` : « an upgrade that can be attached to that ally ».
- **A (recommandé)** : coquille : comme l'officielle, l'amélioration doit pouvoir s'attacher à l'allié
  trouvé (codé en attendant).
- B : lecture littérale : n'importe quelle amélioration attachable à un allié, même un autre que celui
  trouvé (recherche plus large).
- Autre (précise).

## Q-UL-7 — `ul038` « Unified Stike » : « Hero Response: When … »
Scan : `Leadership/Unified Strike.png` (coquille connue). L'officielle `58020` est une « Hero Interrupt:
When … » ; une Réponse arriverait APRÈS l'usage, où « add … for this use » ne veut plus rien dire.
Le titre imprimé est aussi « Stike ».
- **A (recommandé)** : Interruption de héros, comme l'officielle (codé) ; titre corrigé en « Unified Strike ».
- B : Interruption de héros, titre laissé « Unified Stike » (tel qu'imprimé ; actuellement dans cards.json).
- C : une vraie Réponse (le bonus ne s'appliquerait à rien : carte inutile).
- Autre (précise).

## Q-UL-8 — `ul044` "You Got This!" : ressource physique au lieu d'énergie
Scan : `Leadership/You Got This.png` (coquille connue). Officielle `49019` : [energy]. Scan : poing rouge
([physical], comparé à `ul012` Inspired = `01074` RES R).
- **A (recommandé)** : suivre le scan : [physical] (codé : `RES R`) — c'est la carte de l'auteur.
- B : coquille : [energy] comme l'officielle.
- Autre (précise).

---

### Cosmétiques (non bloquantes, aucune incidence de règle : les cartes sont terminées)
- `ul025` Shōgun : le texte imprime « After **Shugun** enters play ». Une seule carte peut se désigner
  ainsi ; le moteur vise la carte elle-même. Le texte affiché garde « Shugun » : corriger ? (A : garder
  tel qu'imprimé ; B : corriger en « Shōgun »).
- `ul041` Mushroom : « **Musroom** does not count against your ally limit ». Même traitement.
- `ul031` Suit Up : citation « TIme to get back at it. » (majuscule parasite), gardée telle quelle.

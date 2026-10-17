# Take control / allié CONTROLLED (« treat it as a CONTROLLED ally with a blank text box »)

**Texte imprimé / définition** : `phoenix/34009` Mind Control : « Attach to a non-ELITE minion. Take control of attached minion and treat it as a
CONTROLLED ally with a blank text box. Its THW is equal to its printed SCH and it takes 1 consequential damage after it thwarts or attacks. »
Même mécanique : `rogue/38011` Karma (2), `bp/51036` Redemption (1), et `tmnt_shinobi_kuji_kiri/sj006` Enthrall (3, « blank textbox »).

**Mécanisme moteur** : `AbilityFactory.TakeControlOfAttachedMinion("<gabarit>")` (`game/ability/factory/treat.py`) appelle `Faces.TreatAsAlly` :
le sbire est ÉCHANGÉ contre une face d'allié créée depuis un GABARIT de `cards.json` (type Ally, trait CONTROLLED, `Class: Encounter`), qui reprend
nom, ATQ imprimée, SCH imprimée (devenue THW) et PV du sbire. L'allié n'a que les capacités du gabarit (texte vide). Quand l'amélioration quitte le jeu,
la face du sbire est restaurée.

**Le nombre de dégâts consécutifs est une DONNÉE du gabarit** : une étoile par dégât dans `ATK` et `THW` (`phoenix_controlled_ally` « 0* », `karma_controlled_ally`
« 0** », `enthrall_controlled_ally` « 0*** »). Un autre nombre = un autre gabarit, aucun code.

**Carte exemple** : `sj006` Enthrall (pack `tmnt_shinobi_kuji_kiri`) ; cas `[sj] sj006` (allié contrôlé, texte vide + témoin, attaque puis contre : 3 dégâts consécutifs, retour en sbire).

**Pièges connus** :
- `Puzzle.Attack('<nom du sbire>')` retrouve l'allié par son NOM (le `card_id` de la face active est celui du gabarit) ; `par_id('<id du sbire>')` le retrouve par `printed_faces`.
- `Puzzle.SetThreat(...)` placé en `mise_en_place` est avalé par les interruptions de la main de départ (Great Responsibility remplace la pose) : le mettre en `declencher`, après `main_exclusive`.
- Un sbire ELITE n'est pas une cible légale (`NonEliteMinion`) ; Sandman `01102` est ELITE (témoin).

**Variantes maison** : Enthrall (3 dégâts consécutifs).

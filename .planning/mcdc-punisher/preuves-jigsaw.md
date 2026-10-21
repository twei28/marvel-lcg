# Preuves PROCESSUS-CARTE : Jigsaw (pu056a, pu056b, pu057a, pu057b)

Une seule capacité commune (`jigsaw_commun.py`), quatre faces. Le scan a été envoyé à l'utilisateur ; aucune ambiguïté de règle.

### pu056a / pu056b / pu057a / pu057b : Jigsaw

- [x] Étape 2 : cartes de référence : `sm/sinister_six/27099.py` (déclencheur), `angela/angela_nemesis/an015.py` (lecture de la défausse de rencontre), `sm/sinister_six/27100a.py` (`PutIntoPlay`, `PlaceThreatOnSchemes`).
- [x] Étape 5 : texte-contre-code. Mots-pièges : « attaque » seul (PAS « attaque et blesse » : corrigé), « le dessus » (seul le dessus compte), « mettre en jeu » (ne déclenche pas « When Revealed »), « vous » (le joueur attaqué).
      Résultat : conforme. ⚠ La carte Boost de l'attaque est défaussée AVANT la Réponse forcée : c'est elle qui est « le dessus ». À confirmer par l'utilisateur si une autre lecture est voulue.
- [x] Étape 6 : nombres : 1 menace (pu056a/b, pu057a), 2 menaces (pu057b). Résultat : conforme (cas 3).
- [x] Étape 7 : `tools/cas/jigsaw.py`, 3 cas `[jig]` : sbire en dessus → en jeu, pas de menace ; traitrise en dessus (sbire dessous) → 1 menace, aucun sbire ; pu057b → 2 menaces.
      Témoin rouge par substitution (condition sbire forcée à faux, menace forcée à 1) : 2 cas sur 3 rouges, le 3e (témoin 1 menace) reste vert comme prévu. Restauré, 3/3 verts.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay 8 parties Jigsaw (normal) contre 8 parties Hammerhead témoin, Spider-Man : 0 incident des deux côtés, 0% de victoire des deux côtés (deck de départ seul, sans amélioration), rounds 4,0 contre 4,2. Journal détaillé non relu ligne à ligne.
- [x] Étape 8 bis : la carte change ce qu'on voit ? NON (un sbire entre en jeu et de la menace monte : zones et jauges déjà couvertes).

Autres corrections de la passe : les 5 scénarios expert Jigsaw n'avaient pas l'ensemble de rencontre « expert » (le complot n'était alors pas posé ; corrigé, script de construction aussi).

Carte terminée : OUI pour le script. Restent hors de cette preuve : les 4 doutes de `jigsaw-doutes.md` (stades, étoile `N**`, tuiles d'accueil, scan tourné).

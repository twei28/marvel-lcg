# Partie au hasard : la roue

Proposition d'un joueur, relayée le 08/10/2026 : le bouton « Aléatoire » ne
tire le méchant que dans l'extension de l'onglet ouvert ; il faut un vrai
hasard, sur toutes les boîtes, et une roue qu'on voit tourner.

## Décisions (questions une à une, 08/10/2026)

1. **Lancement** : une nouvelle tuile « Partie au hasard » sur l'accueil.
   On y choisit le nombre de joueurs.
2. **Plusieurs joueurs** : un bandeau de héros PAR joueur, qui tournent en
   même temps et s'arrêtent l'un après l'autre ; jamais deux fois le même
   héros. Puis le bandeau du scénario.
3. **Contenu** : officiels par défaut ; UNE case « inclure les fan-made »
   pour les héros ET les scénarios.
4. **Une case de la roue = un scénario** jouable seul (pas un méchant).
5. **Modulaires** : ceux recommandés par le scénario, modifiables ensuite
   (avec le bouton Aléatoire habituel des modulaires).
6. **Forme** : bandeau de portraits façon machine à sous, qui défile,
   ralentit et s'arrête sous un repère.
7. **Relance** : un bouton « Relancer » sous chaque bandeau, qui ne fait
   retourner que lui.
8. **En ligne** : tous les joueurs du salon voient les bandeaux tourner et
   s'arrêter sur les mêmes résultats au même moment. Chacun relance SON
   héros ; seul l'hôte relance le scénario. Tout le monde voit les relances.
9. **Son** : un clic à chaque portrait qui passe, de plus en plus lent,
   environ 4 s ; PAS de réplique à l'arrêt.
10. **Ensuite** : le parcours habituel (deck, modulaires, difficulté), héros
    et scénario déjà posés.
11. **Bouton « Aléatoire » de l'étape Scénario** : tire désormais dans
    TOUTES les boîtes (même règle de fan-made), et bascule sur l'onglet du
    scénario tiré.

## Avancement (08/10/2026, non commité, non déployé)

Fichiers : `public/js/prepare/roue.js` (tirage pur + bandeau, partagé),
`public/css/prepare/roue.css` (lue par prepare.html ET salon.html),
`app.js` (tuile, `ouvrirRoue`, bouton Aléatoire), `catalog.js`
(`tousLesScenarios`), `sons.js` (`jouerClicRoue`), `dico-en.js`,
`salon/app.js` + `salon.html` (la roue vue de l'invité), moteur
`server_get.py` (`/set_roue`, `/get_roue`) et `server_new_game.py` (roue
effacée au lancement).

- [x] 1. Tuile « Partie au hasard » sur l'accueil, nombre de héros 1 à 4.
- [x] 2. Un bandeau par héros, ensemble, arrêts l'un après l'autre
  (2,6 s + 0,4 s par bandeau), puis le scénario ; jamais deux fois le même.
- [x] 3. Une case « Inclure les fan-made » (héros ET scénarios, retenue dans
  `mc_roue_fanmade`) ; la cocher relance tout. Officiel = `homebrew` faux
  (extension sans « Custom », catalog.js).
- [x] 4. Une case = un scénario jouable seul : ni défis (Weekly Challenges,
  onglet Défis), ni `_expert`, ni `_competitive`. Les leaders de Civil War
  restent (ils se jouent en coop).
- [x] 5. Modulaires recommandés posés par `selectScenario`, modifiables.
- [x] 6. Bandeau machine à sous sous un repère doré.
- [x] 7. « Relancer » par bandeau, qui ne fait tourner que lui (jamais sur
  le héros d'un autre siège).
- [x] 8. En ligne : l'hôte tire et publie, l'invité lit `/get_roue` (1 s
  quand une roue est ouverte, 2 s sinon) et anime ; il ne relance que son
  héros, puis passe au choix du deck de ce héros. L'hôte voit les relances.
  « Retour » ferme la roue chez tout le monde ; `/new` l'efface.
- [x] 9. Clic = `survol.wav` à 30 % du volume des effets, un toutes les 45 ms
  au plus ; pas de réplique. Mouvement réduit / sobre : posé sans défiler.
- [x] 10. « Continuer » : héros posés (en ligne, seul celui de l'hôte, les
  invités choisissent leur deck au salon), scénario posé, étape Decks.
- [x] 11. Bouton Aléatoire de l'étape Scénario : toutes les boîtes, même case
  fan-made, bascule sur l'onglet tiré (Legacy : le verrou décide ; Bataille :
  inchangé).

Vérifié : `ui-check/tests/roue-hasard.spec.ts` (4 cas purs) et
`roue-hasard-ecran.spec.ts` (solo, 3 joueurs + relance, Aléatoire, mouvement
réduit) verts sur pc, tablette, mobile ; `tools/test_salon.py` 27/27 dont
9 cas de roue ; en ligne à deux (hôte + invité, moteur d'essai avec mots de
passe de siège) : mêmes résultats des deux côtés, relance de l'invité vue
par l'hôte, fermeture propagée.
Non vu : une vraie table en ligne avec 3 ou 4 invités ; l'écart de temps
entre l'hôte et l'invité (jusqu'à 1 à 2 s, le temps du sondage).

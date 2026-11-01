# Page « Difficulté et sets modulaires » (30/10/2026)

Étape 4 de la préparation de partie, entre « Méchant » et « Final ». Elle remplace le bloc « Menace /
Sets modulaires » qui se trouvait sous la grille des scénarios (on ne le voyait pas).

## Où est quoi

| Quoi | Où |
|---|---|
| DOM de la page | `Fusion/marvel-lcg-src/public/js/prepare/page-difficulte.js` |
| Logique pure (testée) | `…/prepare/difficulte-logique.js`, test : `node --test tools/tests-lanceur/difficulte-logique.test.mjs` |
| Styles | `public/css/prepare/page-difficulte.css` (biseau et dégradé seulement sous `html[data-epure]`) |
| Branchement dans le wizard | `app.js` : `STEPS`, `stepComplete` (cas 3 et 4), `stepView`, `stepDifficulte`, `rendreNiveau` |
| Propositions VillainTheory | `…/prepare/villaintheory.js` (**généré**) par `tools/importer_villaintheory.py` |
| Noms français des sets | `…/prepare/noms-sets-fr.js` (**généré**) par `tools/generer_noms_sets_fr.py` |
| Rapports de couverture | `docs/rapports/VILLAINTHEORY-IMPORT.md`, `docs/rapports/NOMS-SETS-FR.md` |
| Tests e2e | `ui-check/tests/page-difficulte.spec.ts` (PC et téléphone) |

## Ce que fait la page

- **Colonne gauche** : sets de la partie en trois groupes (obligatoires, recommandés, ajoutés par le joueur),
  difficulté estimée, bouton « Sets proposés par VillainTheory ».
- **Colonne droite** : niveau (Standard I/II/III, Expert, Skirmish, Héroïque, Intense Combatants le cas échéant),
  puis tous les sets **modulaires** rangés par boîte (titre de la boîte en français via `titres-extensions.js`),
  avec recherche et cases à cocher.
- **Bandeau du bas** : les propositions du méchant. Un set absent du jeu **grise** la proposition et dit lequel.
- **Téléphone** : trois onglets (Sets de la partie / Niveau / Propositions), un panneau à la fois.
- L'état reste `state.difficulty` : le lanceur (`launcher.js`) et le moteur ne changent pas. Toute coche passe
  `modularConfig` à `custom` ; « Recommandés » et « Aléatoire » le remettent.

## Pièges

1. **Le mode Bataille garde sa seconde table sous la grille des scénarios** : `stepComplete(2)` l'exige pour
   continuer. `rendreMenace()` ne dessine plus que ce bloc ; le niveau est dans `rendreNiveau()`.
2. **Plafond de sets** : `validation.js` refusait plus de `max(4, recommandés)` sets. Les propositions VillainTheory
   en prennent jusqu'à 7 (les règles l'autorisent, 1.7) : le plafond est `nombreMaxDeSets` (8 au moins).
3. **Boîte d'un set** : lue à l'exécution dans `catalog.extensions()` (`sets_info.json`). Un set sans boîte va
   dans « Autres » (les extensions fan-made et les sets orphelins).
4. **Difficulté estimée** : on ne calcule rien. C'est la note de la proposition quand la sélection est
   exactement la sienne, +0 pour le recommandé, sinon « — ». Le niveau n'y entre pas : la note de l'auteur ne le
   dit pas.
5. **Noms français des sets** : le jeu n'a aucune table. `tools/generer_noms_sets_fr.py` n'en déduit que
   quelques-uns des textes FR des cartes de scénario (« recommandé : Alerte à la Bombe »), uniquement quand le
   nombre de noms égale le nombre de sets du fichier. Les autres s'affichent en anglais. Pour en ajouter : voir
   le rapport `NOMS-SETS-FR.md`, puis compléter le générateur (ne pas éditer le `.js` à la main).
6. **Noms des combinaisons** : laissés en anglais, ce sont des noms d'auteur.

## Refaire l'import

```bash
cd Fusion/marvel-lcg-src
python3 tools/importer_villaintheory.py CHEMIN/Every_Villains_Best_Modular_Sets.mht   # propositions + rapport
python3 tools/generer_noms_sets_fr.py                                                  # noms FR + rapport
node --test tools/tests-lanceur/difficulte-logique.test.mjs                            # les identifiants existent
```

Le `.mht` : ouvrir le Google Doc dans Chrome, Enregistrer sous… « Page Web, fichier unique ». Le script lit les
tableaux (nom, sets, difficulté, notes, packs) et les titres (boîte en `h1`, méchant en `h3`).
Règles : combinaison gardée si le méchant existe dans le jeu (`ALIAS` pour les titres qui diffèrent du nom du
scénario) ; sets génériques (« Any MojoMania set ») écartés ; set absent du jeu = proposition grisée.

# Corrections de la phase du méchant « Sur la table » — 18 octobre 2026

Les problèmes de l’audit du 17 octobre ont été corrigés dans les sources de l’interface et la version locale compilée du jeu.

## Déroulement obtenu

Les cartes partent du paquet et s’affichent en grand au centre. Les boosts entrent successivement et restent lisibles ensemble ; aucune minuterie ne les range pendant la lecture. Le clic lance leur départ. L’étape suivante attend la fin réelle des trajets.

Une rencontre déjà présente dans le monde du moteur reste masquée sur la table pendant sa lecture et son trajet. Sa place demeure mesurable. Une nouvelle clé de journal pour la même carte ne crée plus une deuxième présentation ni un départ spontané.

La lecture utilise les scans en grande taille, sans compteurs ni jauges du monde courant. Les cartes horizontales conservent leur orientation et leur ratio. La mise à l’échelle du départ part des dimensions réellement rendues ; les mesures de destination excluent les copies de lecture et suivent les déplacements de la table pendant le vol.

Le grand jeton du résultat attend que les cartes aient quitté le centre. Les halos de la table passent derrière les cartes de lecture. Pendant un vol de jeton, les cartes et effets de l’étape suivante attendent également ; son point de départ reste mesurable même lorsque le texte est temporairement masqué.

Le parcours de Klaw a révélé une autre cause des boosts sautés : la défense du sbire suivant pouvait effacer le résultat de l’attaque précédente. Cette question attend maintenant la validation de ce résultat. Une étape déjà validée ne relance pas la lecture de ses cartes pendant l’attente du moteur.

Espace fonctionne aussi lorsque le bouton d’une carte a gardé le focus. Un deuxième clic pendant un départ ne saute aucune étape. Une navigation qui annule une lecture annule également sa continuation différée.

## Vérifications

- **247 tests unitaires ciblés passent**, dans sept fichiers : déroulement, lecture et départ des rencontres, placements, calage de la table, flèches et animations générales.
- TypeScript et compilation de production réussis ; sortie de compilation conforme.
- Contrôles de livraison des boîtes de défense et de questions réussis : 14 tailles de liste sur quatre fenêtres, puis sept types de question sur quatre fenêtres.
- **Deux parcours complets en partie réelle passent**, sur un moteur de test séparé : Rhino / Peter Parker et Klaw / Spider-Man, seed 4321, à 1280 × 720, animations actives.
- Le parcours de Klaw exige effectivement une attaque avec deux boosts. Les assertions vérifient le masquage des exemplaires de la table, la lecture qui reste stable sans clic, l’absence de grand jeton devant les cartes, le départ au clic, le maintien de l’explication pendant ce départ, les doubles clics et l’arrivée au bilan.
- **Les quatre tests du mode sur état enregistré passent également**. Ils ont été actualisés : sélecteurs de l’interface actuelle, animations actives et distinction entre jeton au repos et jeton en vol.

La vérification en partie réelle porte sur ces deux scénarios sur PC. Le mouvement réduit, la navigation interrompue et le déplacement d’une destination sont couverts par les tests unitaires. Le multijoueur et le mobile n’ont pas fait l’objet d’un parcours réel supplémentaire pour ce correctif.

## Captures de la version corrigée

- [Deux boosts de Klaw, dont une carte horizontale, au centre](verification-2026-10-18/klaw/lecture-1.png).
- [Rencontre de Klaw lisible au centre](verification-2026-10-18/klaw/lecture-2.png).
- [Première lecture de Rhino](verification-2026-10-18/rhino/lecture-1.png).
- [Dernière lecture de Rhino](verification-2026-10-18/rhino/lecture-6.png).

Les nouveaux contrôles en partie réelle sont dans `ui-check/tests/phase-sur-table-lecture.spec.ts`. Ils nécessitent un serveur de test explicitement désigné par `UI_CHECK_BASE` et refusent le port habituel 2345.

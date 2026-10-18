# Reprise après audit de la phase « Sur la table » — 18 octobre 2026

## Comportement corrigé

- Le terme affiché reste **Boost**. Les corrections déjà présentes dans le dépôt sur ce terme et sur l’inclinaison des cadres ont été conservées.
- Un clic pendant l’entrée des cartes est ignoré : il faut un nouveau clic une fois les cartes au centre. Un clic prématuré ne supprime plus la lecture.
- Les dégâts et leurs effets visuels ne sont pas annoncés pendant l’entrée, la lecture et le départ des boosts. Une attaque résolue conserve ensuite un temps de lecture de son résultat avant le clic qui lance les dégâts.
- Les boosts déjà connus avant une interruption de dégâts sont lus **avant** de demander si le joueur veut utiliser une carte comme Barrière énergétique. Ils ne sont pas présentés une seconde fois lors de la résolution.
- Une annonce enrichie de nouveaux boosts ne conserve pas la validation donnée à l’annonce initiale sans boosts. La lecture reste rattachée au round raconté, même lorsque le moteur passe déjà au round suivant.
- La table et le déroulement partagent le verrou des questions futures. Les rencontres gardent leur face selon le récit lorsque les mains sont actualisées pour une décision ; figer les compteurs sur un état précédent ne recache plus un boost déjà lu.
- Le remplacement d’une image de carte pendant son retournement, par exemple lors du chargement du scan français, ne coupe plus ses minuteries et ne laisse plus la carte de chant.
- Les améliorations proposées dans une décision sur table disposent de boutons nommés dans le bandeau. Elles restent sélectionnables même entre plusieurs cartes attachées. Le survol et le focus ouvrent leur aperçu ; le choix ne dépend plus d’une tranche de carte à viser dans la pile.
- Les cadres dorés, rouges et verts utilisent l’angle de l’image. La vérification navigateur mesure aussi leur silhouette autour d’une carte inclinée.

## Vérification

Les tests ciblés couvrent le cycle des cartes, la séparation lecture/résultat/dégâts, une interruption après lecture des boosts, la stabilité des faces, les cadres, les choix d’améliorations, la conservation du rythme et les retournements interrompus par un changement de scan.

Les parcours navigateur utilisent un moteur séparé sur le port 2493, sans modifier la partie habituelle. Les parties réelles sont contrôlées sur PC à 1280 × 720, animations actives, seed 4321 : Rhino/Peter Parker, Klaw/Spider-Man, puis Klaw/Spider-Man avec trois améliorations en jeu dont Barrière énergétique.

Le pilote observe les changements de face des boosts, l’absence d’effets de dégâts pendant la lecture, les PV avant et après le départ, les clics précoces et l’arrivée au bilan. Le troisième parcours exige que les boosts aient été lus avant de sélectionner Barrière énergétique et que l’aperçu de cette amélioration soit visible.

Le multijoueur et le mobile ne font pas l’objet de parcours réels dans cette reprise.

## Résultats finaux

- **302 tests unitaires ciblés réussis**, dans dix fichiers.
- **Trois parcours réels réussis**, jusqu’au bilan, dont Klaw avec deux boosts puis sélection effective de Barrière énergétique avec son aperçu visible.
- **Cinq tests navigateur sur état enregistré réussis**, dont le contrôle de l’angle et des dimensions du cadre incliné.
- TypeScript, compilation de production et vérification des dix fichiers de sortie réussis.
- Contrôles des boîtes de défense (14 tailles × 4 fenêtres) et de questions (7 types × 4 fenêtres) réussis ; leurs sept cas de génération réussis également.
- Version compilée copiée dans `Fusion/marvel-lcg-src/public/app/`. Aucun changement de règles du moteur ; aucune publication distante.

## Captures

- [Deux boosts de Klaw au centre, sans résultat de dégâts prématuré](verification-audit-2026-10-18/boosts-klaw.png).
- [Table après le départ des boosts](verification-audit-2026-10-18/apres-boosts-klaw.png).
- [Barrière énergétique sélectionnable par son nom avec aperçu](verification-audit-2026-10-18/amelioration.png).
- [Dernière rencontre du parcours Rhino](verification-audit-2026-10-18/rencontre-rhino.png).

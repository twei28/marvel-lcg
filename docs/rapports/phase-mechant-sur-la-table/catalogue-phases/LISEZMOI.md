# Catalogue visuel de la phase du méchant « Sur la table »

Produit le 18 octobre 2026. Ouvrir `index.html` (une seule page, 106 captures en JPEG base64, filtre PC / tablette / mobile, sommaire par section, remarques d'ergonomie et section « Non réalisé »). Les captures sources en PNG sont dans `captures/`, nommées `<section>-<état>-<écran>.png`.

## Comment les captures ont été produites

- Moteur de test sur des ports 2493, 2495, 2496 et 2494 (jamais le port 2345). Build d'interface déjà servi (`Fusion/marvel-lcg-src/public/app/`), non reconstruit.
- Pilotage par Playwright (Chromium sans tête) : `outils/lib.mjs` (création de partie par `/new?data=…`, commandes `Puzzle.*` par `/sandbox_command`, boucle qui joue la phase et capture chaque état distinct du bandeau), `outils/run.mjs` (lance un parcours), `outils/parcours.mjs` (les états montés), `outils/multi.mjs` et `outils/multi2.mjs` (deux fenêtres, une politique à la fois), `outils/mesures.mjs` (mesure des rectangles : chevauchements, cibles tactiles, bouton « Fin du tour » recouvert, résultat dans `outils/mesures.json`), `outils/sonde-*.mjs` (sondes ponctuelles : défaite, Bebop, Rapide, étiquettes).
- Réglages navigateur posés avant chaque partie : `mc_phase_presentation=bis`, `marvel-board-mode-phase-mechant=sur-table`, `marvel-langue-choisie=1`, `marvel-langue=fr`, `mc_aide_bulle_table=vue`, affichage Épuré (valeur par défaut). Animations actives, sauf la capture « animations réduites ».
- Les parties sont en mode bac à sable (nécessaire pour poser les états). Le bandeau « Bac à sable » est masqué par une règle CSS injectée (`.bandeau-triche{display:none}`) parce qu'il recouvre la question ; tout le reste est tel quel.
- Les chemins absolus de `OUT` et du dépôt sont ceux de la session de production : à adapter pour rejouer. `outils/build.py` reconstruit `index.html` et `captures/` depuis `manifeste.py` (légendes, remarques) et `gabarit.html`.
- Les captures PNG viennent du dossier de travail ; l'index les reconvertit en JPEG (largeur maximale 1280 px, qualité 62 pour tenir sous 12 Mo).

## États montés (parcours dans `outils/parcours.mjs`)

Klaw / Spider-Man : base, défense choisie + Salto Arrière en main (`klaw-defend`), 1 / 2 / 3 alliés (`klaw-allie1`, `klaw-allies2`, `klaw-allies3`), 4 alliés (fenêtre « ALLY LIMIT »), allié presque mort, alter-ego, héros vaincu, méchant sonné / désorienté, statuts Tenace, trois boosts, boosts ★ / Amplification / Crise / traîtrise + attachement, changement de stade, manigance qui avance, défaite, trois manigances annexes, Barrière énergétique, héros incliné, allié sonné + désorienté.
Rhino / Spider-Man : 1, 3 et 6 sbires, sbires qui manigancent (alter-ego), Surcharge, Perforante, Rapide (Assassin Badoon, Vautour), onze types de cartes révélées (sbire, attachement, annexe Crise et Accélération, traîtrise, Assaut, obligation, environnement, Renfort, deux Renforts, Se Liguer en alter-ego et en héros).
Autres : Ultron, Baxter Stockman, Shredder, Bebop & Rocksteady, Crossbones.
Multijoueur : Klaw, Spider-Man + She-Hulk, politiques `concerne`, `quiconque` (jusqu'au bilan) et `tous` (bloque, voir ci-dessous).
Variantes : animations réduites, 1050×480, 1180×820, 390×844, 844×390 (pointeur tactile émulé).

## À savoir

- Le robot décide des choix par des textes de boutons ; chaque capture indique le déclencheur exact.
- Le deck de rencontre est monté avec `Puzzle.EmptyEncounterDeck()` puis `Puzzle.CreateEncounterDeck(...)` (la dernière carte donnée est la plus haute dans le script `run.mjs`, qui renverse la liste : dans `parcours.mjs` on écrit les cartes dans l'ordre où elles sortent).
- La politique multijoueur « Tout le monde valide » se bloque après la dernière attaque du sbire (seeds 4321 et 777 reproduits, test supplémentaire avec Espace et clic forcé) : le moteur reste sur `AfterCardsMovedToRevealingArea_Text` alors que les deux écrans affichent « Prêt · 2 / 2 ».
- Tablette et mobile sont des émulations de taille et de pointeur dans un navigateur de bureau, pas des mesures sur appareil.

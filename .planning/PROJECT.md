# Marvel LCG — Refonte Design / UI / UX

## What This Is

Jeu numérique non officiel Marvel Champions LCG (usage strictement personnel, accord de l'auteur), moteur Python 3.10 complet et fidèle, frontend web vanilla servi en local (http://127.0.0.1:2345). Ce projet est la refonte complète du design, de l'UI et de l'UX de l'application : menus, préparation de partie, galerie de cartes, gestion de decks, replay ET l'interface du plateau en cours de partie.

## Core Value

Une interface digne du contenu : belle, claire et fluide sur PC, tablette et mobile, sans jamais toucher aux règles du moteur.

## Requirements

### Validated

<!-- Inféré du codebase existant (.planning/codebase/) — acquis à préserver. -->

- ✓ Moteur de règles complet et testé (3766 cartes ok / 0 échec, GEN 4331/0) — existant
- ✓ Serveur web local Python qui sert le frontend et les données (endpoints /list_scenarios, /list_starter_deck, /read_file, images par card_id) — existant
- ✓ Écran de préparation fonctionnel (scene.html : wizard 4 étapes, galerie de héros dynamique, formulaires campaign log préremplis) — existant
- ✓ Runtime de partie fonctionnel (public/js/marvel/ : plateau, asks, interactions) — existant
- ✓ Galerie de cartes, gestion de decks, replay fonctionnels (cards.html, deck.html, replay.html) — existant
- ✓ Modules JS réutilisables (card_statistics.js, card_info.js, card_preview.js, set_info.js) — existant

### Active

<!-- Hypothèses jusqu'à validation. Affinées après la phase de recherche. -->

- [ ] Recherche : état de l'art des interfaces de jeux de cartes digitaux (MTG Arena, Marvel Snap, LotR LCG digital, Arkham...) → 2-3 directions visuelles proposées
- [ ] Décision techno frontend éclairée par la recherche (moderniser le vanilla vs reconstruire en React+TS+Vite)
- [ ] Design system unifié (couleurs, typo, composants, iconographie) appliqué à toute l'app
- [ ] Refonte des menus et de la navigation
- [ ] Refonte de la préparation de partie (base : plan wizard 6 étapes Mode → Héros → Decks → Scénario → Difficulté → Récapitulatif de Fusion/PREPARE-UI-PLAN.md)
- [ ] Refonte de la galerie de cartes et de la gestion de decks
- [ ] Refonte de l'interface en partie (plateau, lisibilité des cartes, clarté des asks/interactions)
- [ ] Responsive + tactile : PC, tablette, mobile

### Out of Scope

- Modification des règles du moteur — contrainte absolue du projet, le moteur est fidèle et validé
- Multijoueur en ligne / réseau en v1 — souhaité pour PLUS TARD (v2+) : ne rien construire qui le bloque (l'architecture client/serveur HTTP+WS s'y prête), mais rien de réseau dans cette refonte
- Nouveau contenu de jeu (cartes, scénarios) — tout le contenu officiel est déjà intégré, projet séparé
- Refonte du backend Python (hors endpoints strictement nécessaires à l'UI) — le serveur fonctionne, risque inutile

## Context

- Codebase mappé dans `.planning/codebase/` (7 documents). Points saillants : `public/scene.html` monolithique (~2000 lignes HTML+CSS+JS inline), vieux style partagé `public/css/menu/style.css`, surcouche récente `wizard.css`, runtime de partie dans `public/js/marvel/`.
- Un plan de refonte de la préparation existe déjà : `Fusion/PREPARE-UI-PLAN.md` (wizard 6 étapes, contrainte « garder l'écran actuel fonctionnel tant que la nouvelle version ne l'est pas »).
- Le codebase vivant est `~/marvel-work/fusion/marvel-lcg-src` (WSL) ; `Fusion/marvel-lcg-src/` est une extraction périmée ; le livrable est re-zippé vers `Fusion/marvel-lcg-src-fusion.zip` après chaque changement.
- Politique moteur : source reconstruit du bytecode, fidélité stricte, divergences volontaires marquées `CORRECTIF`. Les données `data/*.json` sont checksummées (recalcul obligatoire à toute édition).
- Tests hors repo : `~/marvel-work/tools/` (test_cards 3766/0, test_generate_cards 4331/0, test_autoplay bot in-process). RELEASE=1 obligatoire.
- Douleur exprimée : « tout à la fois » — le look, l'ergonomie des flux ET la lisibilité en partie méritent le même niveau de soin que le moteur.

## Constraints

- **Moteur**: interdiction de modifier les règles du jeu — le moteur est validé carte par carte, la refonte est purement présentation/interaction
- **Compatibilité**: les écrans actuels restent fonctionnels tant que leur remplaçant n'est pas prêt — le jeu doit rester jouable pendant toute la refonte
- **Supports**: PC, tablette et mobile — responsive et interactions tactiles à prévoir dès la conception
- **Environnement**: app servie en local par le serveur Python embarqué — pas de CDN, tout doit être self-contained dans `public/` (ou un build statique copié dedans)
- **Livraison**: chaque étape livrée = re-zip vers `Fusion/` + relance du serveur + tests de non-régression (autoplay 0 traceback)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Périmètre = toute l'app, plateau inclus | La douleur est globale, pas localisée | — Pending |
| Stack = React 19 + TS 6 + Vite 8, build multi-pages dans public/app/, migration page par page | Recherche : coexistence gratuite (serveur route par extension), CSS existant sans valeur mobile, js/prepare réinvente React à la main | — Pending |
| Direction visuelle = squelette clair « instrument de jeu » + personnalité comic KAPOW + thème sombre en option tokens | Recommandation recherche : réversible par tokens, lisibilité d'abord (échec documenté Gwent sur le tout-sombre) | — Pending |
| Plateau découpé en 3 sous-phases de risque croissant (restylage → layout responsive → interactions asks), jamais en dernier ni en bloc | Runtime = sources perdues, protocole non documenté ; bascule ?ui=old permanente | — Pending |
| Cible PC + tablette + mobile | L'utilisateur veut jouer partout | — Pending |
| Moteur de règles intouchable | Acquis validé (3766/0), tout le risque serait en pure perte | ✓ Good |

---
*Last updated: 2026-07-28 after initialization*

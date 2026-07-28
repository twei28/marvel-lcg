# REQUIREMENTS — Refonte Design / UI / UX Marvel LCG

Scopé le 2026-07-28 avec l'utilisateur, à partir de `.planning/research/FEATURES.md`.

## v1 Requirements

### Fondations (FOUND)

- [x] **FOUND-01**: Filet de sécurité en place avant toute modification visuelle : captures Playwright de référence des 6 écrans actuels, fixtures `get_world` extraites des runs autoplay, bascule `?ui=old` disponible pendant toute la migration
- [ ] **FOUND-02**: Design system tokenisé (couleurs, typo, espacement, iconographie) : squelette clair « instrument de jeu », personnalité comic (halftone/KAPOW dosée), thème sombre commutable prévu par les tokens
- [ ] **FOUND-03**: Stack nouvelle UI opérationnelle : React 19 + TypeScript 6 + Vite 8, build multi-pages statique dans `public/app/`, servi par le serveur Python existant sans modification backend, pages anciennes et nouvelles coexistent
- [ ] **FOUND-04**: Composant Carte à double représentation : tuile lisible (nom, coût, stats, icônes, statuts, art recadré) + lecteur HTML du texte réel de la carte + scan complet à l'inspection — réutilisé par toutes les surfaces

### Coquille et navigation (SHELL)

- [ ] **SHELL-01**: L'utilisateur arrive sur un hub d'accueil avec une action primaire évidente (Reprendre / Nouvelle partie)
- [ ] **SHELL-02**: L'utilisateur navigue via une navigation persistante à libellés texte (latérale desktop, basse mobile)
- [ ] **SHELL-03**: L'utilisateur peut revenir en arrière de façon fiable et non destructive depuis tout écran

### Préparation de partie (PREP)

- [ ] **PREP-01**: L'utilisateur configure sa partie via un wizard à étapes (Mode → Héros → Decks → Scénario → Difficulté → Récapitulatif) avec stepper visible et navigation arrière
- [ ] **PREP-02**: L'utilisateur voit un récapitulatif persistant de ses choix pendant tout le wizard
- [ ] **PREP-03**: Quand le lancement est bloqué, l'utilisateur voit la raison exacte du blocage sur le bouton final
- [ ] **PREP-04**: L'utilisateur choisit son héros dans une galerie visuelle (art, aspect) et son deck parmi deck de départ / deck perso / import MarvelCDB
- [ ] **PREP-05**: L'utilisateur peut relancer sa dernière configuration en un geste et reprendre une sauvegarde depuis l'accueil
- [ ] **PREP-06**: Chaque champ des formulaires de campaign log a une aide contextuelle expliquant quoi remplir

### Plateau en partie (BOARD)

- [ ] **BOARD-01**: Chaque carte du plateau est une tuile lisible (FOUND-04) ; l'utilisateur inspecte le scan complet sans modale par survol (desktop), appui long (tactile) ou clavier, sans occlusion de la carte concernée
- [ ] **BOARD-02**: Les zones du plateau (vilain, schémas, rencontre, et par joueur : identité, alliés, améliorations, main, decks, ressources) sont délimitées et étiquetées
- [ ] **BOARD-03**: Les compteurs (dégâts, menace, statuts, ressources) sont lisibles directement sur les tuiles, en fort contraste
- [ ] **BOARD-04**: Un indicateur permanent montre la phase, le tour et l'action attendue
- [ ] **BOARD-05**: Les demandes du moteur (asks) s'affichent dans une barre fixe avec intitulé, options et annuler/passer — jamais de modale surgissante
- [ ] **BOARD-06**: Seules les actions irréversibles demandent confirmation
- [ ] **BOARD-07**: La main s'affiche en rangée avec dépliage au survol/focus et distinction visuelle des cartes jouables
- [ ] **BOARD-08**: Les animations informent (origine/destination, cible des dégâts), sont réglables en vitesse et interruptibles
- [ ] **BOARD-09**: L'utilisateur consulte un journal de partie répondant à « que vient-il de se passer ? »
- [ ] **BOARD-10**: L'annulation (undo) est accessible visiblement depuis le plateau
- [ ] **BOARD-11**: En solo multi-héros, l'aire du joueur actif s'affiche en grand, les autres en bandeaux repliés avec compteurs clés
- [ ] **BOARD-12**: L'utilisateur obtient une vue d'ensemble du plateau par dézoom sémantique (pas un pan/zoom optique)
- [ ] **BOARD-13**: Les mots-clés (Retaliate, Guard, Confused...) montrent un rappel de règle au survol/appui

### Mobile et tablette (MOB)

- [ ] **MOB-01**: Toutes les interactions fonctionnent au tactile : cibles ≥ 44 px, équivalent appui long pour chaque survol, zones sûres respectées, actions principales au pouce
- [ ] **MOB-02**: Sur petit écran, l'utilisateur navigue entre les zones du plateau (onglets/carrousel/focus) au lieu de subir un plateau compressé
- [ ] **MOB-03**: La partie se joue en paysage (invitation à tourner, pas de blocage) ; les menus fonctionnent en portrait

### Accessibilité (ACC)

- [ ] **ACC-01**: Aucune information portée par la seule couleur (aspects rouge/jaune/bleu/vert : toujours couleur + icône + libellé)
- [ ] **ACC-02**: Les contrastes du texte de règles et des compteurs sont vérifiés (tokens de contraste)
- [ ] **ACC-03**: `prefers-reduced-motion` est respecté (branché sur le réglage de vitesse d'animation)

## v2 Requirements (différés)

### v1.x (après validation du plateau)

- **GAL**: Refonte galerie de cartes + deck builder (recherche instantanée, facettes, grille/liste, détail lisible, stats de deck, validation de légalité, import/export visibles)
- **SHELL**: Écran de réglages centralisé ; états de chargement squelettes
- **BOARD**: Surlignage des cibles valides (dépend de l'exposition des cibles par le descripteur) ; recherche dans les zones du plateau
- **ACC**: Taille de texte réglable ; navigation clavier complète
- **MISC**: Écran de fin de partie riche ; presets de configuration nommés ; raccourcis clavier

### v2+

- Multijoueur en ligne (souhait explicite de l'utilisateur pour plus tard — l'architecture client/serveur HTTP+WS existante s'y prête, ne rien construire qui le bloque)
- Prévisualisation d'impact chiffrée (doit venir du moteur, jamais du client)
- Timeline de replay navigable ; journal cliquable
- Suivi de campagne visuel (4 formats de log)
- PWA, sons, haptique ; deuxième thème visuel complet

## Out of Scope

- Modification des règles du moteur Python — acquis validé (3766/0), la refonte est purement présentation/interaction
- Réécriture du runtime plateau (`public/js/marvel/`, sources perdues) sans filet : toute évolution passe par extraction d'un protocole typé et bascule progressive avec `?ui=old`
- Pan/zoom libre sur le plateau — anti-pattern documenté (MTG Arena), remplacé par tuiles lisibles + navigation par zone
- Phase « responsive » tardive — le responsive est dans la definition of done de chaque écran, pas une phase finale
- Patterns de monétisation/shop, animations décoratives bloquantes — anti-features documentées

## Traceability

| Requirement | Phase | Statut |
|-------------|-------|--------|
| FOUND-01 | Phase 1 | Complete |
| FOUND-02 | Phase 2 | Pending |
| FOUND-03 | Phase 2 | Pending |
| FOUND-04 | Phase 3 | Pending |
| SHELL-01 | Phase 3 | Pending |
| SHELL-02 | Phase 3 | Pending |
| SHELL-03 | Phase 3 | Pending |
| PREP-01 | Phase 4 | Pending |
| PREP-02 | Phase 4 | Pending |
| PREP-03 | Phase 4 | Pending |
| PREP-04 | Phase 4 | Pending |
| PREP-05 | Phase 4 | Pending |
| PREP-06 | Phase 4 | Pending |
| BOARD-01 | Phase 5 | Pending |
| BOARD-02 | Phase 5 | Pending |
| BOARD-03 | Phase 5 | Pending |
| BOARD-04 | Phase 5 | Pending |
| BOARD-05 | Phase 7 | Pending |
| BOARD-06 | Phase 7 | Pending |
| BOARD-07 | Phase 7 | Pending |
| BOARD-08 | Phase 7 | Pending |
| BOARD-09 | Phase 7 | Pending |
| BOARD-10 | Phase 7 | Pending |
| BOARD-11 | Phase 6 | Pending |
| BOARD-12 | Phase 6 | Pending |
| BOARD-13 | Phase 5 | Pending |
| MOB-01 | Phase 6 | Pending |
| MOB-02 | Phase 6 | Pending |
| MOB-03 | Phase 6 | Pending |
| ACC-01 | Phase 2 | Pending |
| ACC-02 | Phase 2 | Pending |
| ACC-03 | Phase 7 | Pending |

**Couverture : 32 / 32 requirements v1 mappés** — aucun orphelin, aucun doublon.

Note : la Phase 1 étend FOUND-01 d'un test automatisé du contrat de lancement (`/new?data=` → plateau), gelé avant toute refonte de la préparation.

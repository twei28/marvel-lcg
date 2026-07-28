# État du projet

## Référence projet

Voir : .planning/PROJECT.md (mis à jour le 2026-07-28)

**Valeur centrale :** Une interface digne du contenu : belle, claire et fluide sur PC, tablette et mobile, sans jamais toucher aux règles du moteur.
**Focus actuel :** Phase 1 — Filet de sécurité et boucle de dev (bloquante)

## Position actuelle

Phase : 1 sur 7 (Filet de sécurité et boucle de dev)
Plan : aucun (phase non planifiée)
Statut : Ready to plan
Dernière activité : 2026-07-28 — Roadmap créée (7 phases, 32/32 requirements mappés)

Progression : [░░░░░░░░░░] 0%

## Métriques

**Vélocité :**
- Plans terminés : 0
- Durée moyenne : —
- Temps d'exécution total : —

**Par phase :**

| Phase | Plans | Total | Moy./plan |
|-------|-------|-------|-----------|
| - | - | - | - |

**Tendance récente :** pas encore de données

*Mis à jour après chaque plan terminé*

## Contexte accumulé

### Décisions

Journal complet dans PROJECT.md (Key Decisions). Décisions structurantes pour le travail en cours :

- [Roadmap] Stack = React 19 + TS 6 + Vite 8, build multi-pages dans `public/app/`, migration page par page (étranglement par nom de fichier HTML, zéro modification backend).
- [Roadmap] Plateau découpé en 3 phases de risque croissant (5 restylage → 6 layout/tactile → 7 interactions), jamais en bloc, jamais en dernier.
- [Roadmap] Galerie de cartes, deck builder et replay différés en v1.x — les écrans actuels restent en service.
- [Roadmap] Le responsive est dans la definition of done de chaque écran ; seul le plateau a une phase de layout dédiée (changement de modèle, pas d'ajustement CSS).
- [Roadmap] Direction visuelle : squelette clair « instrument de jeu », personnalité comic dosée, thème sombre en option par tokens.

### Todos en attente

Aucun.

### Blocages / points de vigilance

- **Intouchabilité étendue** : `public/js/marvel/` (7318 lignes de TS compilé, sources perdues) a le même statut que le moteur. Le nouveau code doit être une fonction pure de `get_world`, écrit à côté. À acter dans PROJECT.md en Phase 1.
- **Séquence CSS obligatoire** en Phase 2 : captures de référence → purge des `!important` de `wizard.css` (67 sur 165) → `@layer` → tokens. Inverser aggrave la cascade.
- **Routage serveur par extension** en liste blanche stricte : tout asset de build hors liste échoue silencieusement (200 OK, contenu vide).
- **Recherche approfondie à prévoir** avant planification : Phase 4 (contrat `/new?data=` et campaign logs des 4 formats), Phase 6 (table de zones par palier, géométrie 4 joueurs mobile), Phase 7 (vocabulaire `select_rule` / `ability_type` / `event_name`).
- **Livraison** : chaque étape livrée = re-zip vers `Fusion/` + relance serveur + non-régression (autoplay 0 traceback). Codebase vivant = `~/marvel-work/fusion/marvel-lcg-src`.

## Continuité de session

Dernière session : 2026-07-28
Arrêté à : ROADMAP.md et STATE.md créés, traçabilité REQUIREMENTS.md mise à jour
Fichier de reprise : aucun

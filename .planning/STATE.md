# État du projet

## Référence projet

Voir : .planning/PROJECT.md (mis à jour le 2026-07-28)

**Valeur centrale :** Une interface digne du contenu : belle, claire et fluide sur PC, tablette et mobile, sans jamais toucher aux règles du moteur.
**Focus actuel :** Phase 1 — Filet de sécurité et boucle de dev (bloquante)

## Position actuelle

Phase : 1 sur 7 (Filet de sécurité et boucle de dev)
Plan : 1 sur 6 dans la phase courante
Statut : En cours
Dernière activité : 2026-07-28 — 01-01-PLAN.md terminé (harnais de captures opérationnel, 18 références figées)

Progression phase 1 : [██░░░░░░░░] 17% (1/6 plans)
Progression projet : [█░░░░░░░░░] ~3% (plans des phases 2 à 7 non encore découpés)

## Métriques

**Vélocité :**
- Plans terminés : 1
- Durée moyenne : 12 min
- Temps d'exécution total : 12 min

**Par phase :**

| Phase | Plans | Total | Moy./plan |
|-------|-------|-------|-----------|
| 1 — Filet de sécurité | 1/6 | 12 min | 12 min |

**Tendance récente :** 01-01 exécuté en 12 min, 3 tâches, 3 déviations auto-corrigées

*Mis à jour après chaque plan terminé*

## Contexte accumulé

### Décisions

Journal complet dans PROJECT.md (Key Decisions). Décisions structurantes pour le travail en cours :

- [Roadmap] Stack = React 19 + TS 6 + Vite 8, build multi-pages dans `public/app/`, migration page par page (étranglement par nom de fichier HTML, zéro modification backend).
- [Roadmap] Plateau découpé en 3 phases de risque croissant (5 restylage → 6 layout/tactile → 7 interactions), jamais en bloc, jamais en dernier.
- [Roadmap] Galerie de cartes, deck builder et replay différés en v1.x — les écrans actuels restent en service.
- [Roadmap] Le responsive est dans la definition of done de chaque écran ; seul le plateau a une phase de layout dédiée (changement de modèle, pas d'ajustement CSS).
- [Roadmap] Direction visuelle : squelette clair « instrument de jeu », personnalité comic dosée, thème sombre en option par tokens.
- [01-01] Marqueurs de page vérifiés contre le HTML réellement servi, jamais contre la doc : `#mode` (scene.html) est masqué par le wizard, remplacé par `#w-stepper` ; `body` remplacé par de vrais sélecteurs.
- [01-01] Garde-fou anti `clean_cache.html` par le titre de page (`Version Mismatch`), indépendant du marqueur de chaque écran.
- [01-01] `prepare.html` inclus comme 6e écran surveillé (`preparation-nouvelle`).
- [01-01] Les scripts npm des plans 01-02 à 01-05 sont déjà déclarés dans `ui-check/package.json` pour éviter que plusieurs plans se disputent ce fichier.

### Todos en attente

Aucun.

### Blocages / points de vigilance

- ✓ **Intouchabilité étendue actée** dans PROJECT.md (Constraints + Key Decisions) : `public/js/marvel/` jamais lu ni modifié, le nouveau code est une fonction pure de `get_world`.
- **Le serveur doit tourner sous `launcher_fast.py`** pour tous les plans suivants : les fixtures (01-03) et la bascule `?ui=old` (01-04) ajoutent des fichiers dans `public/`, invisibles sous `launcher.py`. Relance = coupure de la partie en cours. Piège connu : le port 2345 reste en TIME_WAIT quelques dizaines de secondes après un arrêt, attendre avant de relancer.
- **Montée de version de Playwright = re-validation des 18 références** (le Chromium embarqué change le rendu). Version épinglée `1.62.0` sans `^`.
- **Référence de l'écran Replays quasi vide** tant qu'aucun replay n'est enregistré : à régénérer le jour où il y en aura.
- **Séquence CSS obligatoire** en Phase 2 : captures de référence → purge des `!important` de `wizard.css` (67 sur 165) → `@layer` → tokens. Inverser aggrave la cascade.
- **Routage serveur par extension** en liste blanche stricte : tout asset de build hors liste échoue silencieusement (200 OK, contenu vide).
- **Recherche approfondie à prévoir** avant planification : Phase 4 (contrat `/new?data=` et campaign logs des 4 formats), Phase 6 (table de zones par palier, géométrie 4 joueurs mobile), Phase 7 (vocabulaire `select_rule` / `ability_type` / `event_name`).
- **Livraison** : chaque étape livrée = re-zip vers `Fusion/` + relance serveur + non-régression (autoplay 0 traceback). Codebase vivant = `~/marvel-work/fusion/marvel-lcg-src`.

## Continuité de session

Dernière session : 2026-07-28
Arrêté à : 01-01-PLAN.md terminé (voir .planning/phases/01-filet-de-securite/01-01-SUMMARY.md)
Fichier de reprise : aucun
Prochain plan : 01-02-PLAN.md — page de comparaison avant/après et validation explicite des références

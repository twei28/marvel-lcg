# L'ouverture silencieuse, et le temps d'arrêt sur la face A

Chantier du 15/09/2026. Spec :
`docs/superpowers/specs/2026-09-15-mise-en-place-silencieuse-design.md`.
Plan : `docs/superpowers/plans/2026-09-15-mise-en-place-silencieuse.md`.

## Ce qui est livré

Douze tâches, chacune relue par un relecteur neuf, puis une relecture d'ensemble
et deux vagues de correctifs. 1627 cas verts.

- **Moteur** : `confirm_main_scheme` (`world_rule.py`), par défaut à FAUX, et
  `World.ConfirmMainSchemeReveal` posée dans la SEULE branche qui retourne une
  face A (`AdvanceMainScheme`), ce qui sert la mise en place ET chaque
  changement d'étape. La trame publie le drapeau, l'écran de préparation le pose
  sur les parties NEUVES seulement.
- **Plateau** : la reconnaissance de la question, le voile d'ouverture, le
  panneau de la face A, le retournement.

## ⚠ Les trois faits qui ont décidé du montage, tous mesurés

1. `world.py:548` avance `01097a` à la mise en place, première branche de
   `AdvanceMainScheme`.
2. Un changement d'étape (`01116b` → `01117a` → `01117b`) repasse par la même
   branche : un seul crochet.
3. **Une question à UNE option avec `forced=True` n'atteint JAMAIS le client.**
   Mesure : zéro appel à `DoGetInput`. Il faut `forced=False`.

## Ce qui reste à faire, et par qui

- ⚠ **Redémarrer le serveur** : `launcher_fast.py` compile `src/` AU LANCEMENT.
  Tant qu'il n'a pas redémarré, la question ne se pose pas, et le plateau se
  comporte comme avant. Rien ne casse en attendant.
- ⚠ **Jouer une ouverture et la regarder** (tâche 12 du plan) : la table qui
  n'apparaît qu'une fois montée, la face A en grand, la main vide assumée, le
  OK, le retournement, la menace, puis le mulligan. Personne ne l'a encore vu.
- **La spec `ui-check` de bout en bout** : écartée volontairement, elle crée une
  partie neuve et détruit celle en cours. À jouer sur décision.
- **L'avenant sur les manigances ANNEXES** (demande du 15/09, en fin de spec) :
  noté, non cadré, quatre points à trancher d'abord.

## Ce qui n'est PAS prouvé, et que j'assume

- Aucun cas ne rejoue une sauvegarde antérieure pour comparer son CRC. Le
  raisonnement tient (drapeau à faux par défaut, règles inscrites dans la scène,
  `buildRules` appelé uniquement à la création), mais la garde la plus
  importante du chantier repose sur une lecture, pas sur une mesure.
- `autoplay.py` n'a aucun levier pour recevoir des règles : la mesure du
  15/09 était ponctuelle, ce n'est pas un filet de régression.
- `board.tsx` n'est monté par aucun test (fiche à part).

## Statut

**Livré, déployé et VU EN JEU le 15/09/2026.** Le panneau s'est affiché sur une
vraie partie (Kang, « Kang's Arrival » face 1A). Deux défauts s'y sont vus du
premier coup, tous deux corrigés le jour même : la carte s'affichait debout, et
le bouton ne ressemblait pas aux autres.

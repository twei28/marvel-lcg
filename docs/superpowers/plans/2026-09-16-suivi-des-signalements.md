# Suivi des signalements — plan d'exécution

> **Pour un agent :** ce plan s'exécute tâche par tâche, chaque tâche se
> termine par ses tests verts et son commit.

**But :** un rapport de bug envoyé par le titulaire d'un compte devient un
ticket : quatre états, un fil dans les deux sens, une page côté joueur, une
pastille qui prévient en partie.

**Spec :** `docs/superpowers/specs/2026-09-16-suivi-des-signalements-design.md`
— elle fait foi, ce plan ne la réinterprète pas.

**Pile :** Python 3.10 sans dépendance (`site/orchestrateur.py`, SQLite),
pages HTML écrites en chaînes, `public/js/prepare/messages.js` côté client.

## Contraintes valables pour toutes les tâches

- **Aucune dépendance nouvelle.** Le site tourne sur la bibliothèque standard.
- **Tout ce qui vient d'un joueur passe par `html.escape`** : description, nom,
  journal et désormais le texte du fil sont écrits par n'importe qui.
- **Le ticket est réservé au siège 0.** `hote` + `siege = 0` : c'est la seule
  identité sûre. Les autres rapports restent des rapports.
- **Migration à la manière de `traite_le`** : `CREATE TABLE IF NOT EXISTS` et
  `PRAGMA table_info`, jamais de reprise destructive.
- **Les tests vivent dans `site/test_parcours.py`**, lancés par
  `python3 site/test_parcours.py`, et affichent `OK` / `RATE` par cas.

---

## Tâche 1 : la base et les fonctions de données

**Fichiers :** `site/orchestrateur.py` (schéma, migration, fonctions),
`site/test_parcours.py` (cas).

**Produit :** `ETATS_RAPPORT` à quatre valeurs ; table `rapports_messages` ;
`ticket_de(numero)`, `ecrire_message(numero, auteur, texte)`,
`tickets_de(pseudo)`, `marquer_ticket_lu(numero, par)`,
`reponses_non_lues(pseudo)`.

- [ ] Écrire les cas d'abord : un rapport de siège 0 donne un ticket, un
      rapport de siège 2 n'en donne pas ; une réponse se range dans le bon
      fil ; un autre compte ne voit pas le ticket ; le compteur de non-lues
      tombe à zéro après lecture.
- [ ] Les voir ROUGES (`python3 site/test_parcours.py`).
- [ ] Écrire le schéma, la migration et les six fonctions.
- [ ] Les voir VERTS, puis commiter.

## Tâche 2 : l'écran d'administration

**Fichiers :** `site/orchestrateur.py` (`_bloc_rapport`, actions POST).

Sous chaque rapport : le fil, un champ « répondre », et le quatrième bouton
d'état (« Refuser »). Même patron que l'existant : des formulaires POST vers
`/admin`, aucun JavaScript.

- [ ] Ajouter l'action `rapport_repondre` et l'état `refuse` au traitement POST.
- [ ] Rendre le fil et le formulaire dans `_bloc_rapport`.
- [ ] Vérifier à la main sur le serveur de test, puis commiter.

## Tâche 3 : la page du joueur

**Fichiers :** `site/orchestrateur.py` (route `/signalements`, gabarit,
`_barre`), `site/test_parcours.py`.

- [ ] Cas d'abord : `/signalements` sans session redirige vers l'accueil ; avec
      session, ne montre que les tickets de ce compte.
- [ ] Les voir ROUGES.
- [ ] Écrire la route, le gabarit et l'entrée dans `_barre` (avec le compteur).
- [ ] Les voir VERTS, puis commiter.

## Tâche 4 : la notification en partie

**Fichiers :** `site/orchestrateur.py` (`/api/prives`),
`Fusion/marvel-lcg-src/public/js/prepare/messages.js`.

`/api/prives` rend en plus `tickets` (nombre de réponses non lues). **Le moteur
n'est pas touché** : `get_messages_prives` recopie ce que le site lui donne.
`messages.js` pose une SECONDE pastille, d'une autre couleur, qui ouvre
`/signalements`.

- [ ] Cas d'abord : `/api/prives` compte les réponses non lues du bon compte.
- [ ] Le voir ROUGE, écrire, le voir VERT.
- [ ] Ajouter la seconde pastille dans `messages.js` (mêmes gardes : rien ne
      s'affiche tant que rien n'attend).
- [ ] Commiter.

## Tâche 5 : la purge

**Fichiers :** `site/orchestrateur.py` (`purger_rapports_traites`),
`site/test_parcours.py`.

À 30 jours, la capture est effacée du disque et `capture` mis à NULL ; le
rapport et son fil restent.

- [ ] Cas d'abord : après purge, le fichier n'existe plus, `capture` est NULL,
      le rapport et ses messages sont toujours là.
- [ ] Le voir ROUGE, écrire, le voir VERT, commiter.

## Tâche 6 : la fiche de backlog

**Fichiers :** `.planning/todos/2026-09-15-repondre-aux-rapports-de-bug.md`.

- [ ] Statut mis à jour : ce qui est livré, ce qui ne l'est pas (aucune modale
      sur le plateau, aucun ticket sans bug, aucun courrier).
- [ ] Commiter.

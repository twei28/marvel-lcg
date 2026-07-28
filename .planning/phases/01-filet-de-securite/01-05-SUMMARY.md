---
phase: 01-filet-de-securite
plan: 05
subsystem: testing
tags: [playwright, contrat-api, golden-file, new-game-descriptor, get-world, e2e, francais]

# Dependency graph
requires:
  - phase: 01-01
    provides: "harnais Playwright, global-setup (cookie de version), script npm lancement deja declare, marqueur #app de prepare.html"
  - phase: 01-04
    provides: "bascule ?ui=new / ?ui=old : le test choisit explicitement la nouvelle preparation"
provides:
  - "`ui-check/contrat-nouvelle-partie.json` : les 8 cles du NewGameDescriptor, leur type, les regles obligatoires et la reponse attendue du moteur"
  - "`npm run lancement` : 2 tests, contrat verifie AVEC et SANS navigateur, plus la preuve que le plateau repond"
  - "La seule documentation ecrite du contrat GET /new?data= (il n'en existait aucune)"
affects: [01-06-livraison, 04-preparation, 05-plateau-restylage, 06-plateau-layout, 07-plateau-interactions]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Golden de contrat d'API : on fige les CLES et les TYPES, jamais les valeurs (un deck varie, le contrat non)"
    - "Double verification d'un contrat : avec l'interface (elle peut casser) et sans (le contrat, lui, ne bouge pas)"
    - "Preuve d'etat par le moteur (/get_world) et jamais par un selecteur du DOM du runtime intouchable"
    - "Avant de sonder un etat serveur, attendre la reponse qui l'a remis a zero : sinon on mesure l'etat precedent"
    - "Selecteurs par role et par libelle (getByRole) pour survivre a la refonte de la phase 4"

key-files:
  created:
    - ui-check/contrat-nouvelle-partie.json
    - ui-check/tests/lancement-partie.spec.ts
  modified:
    - ui-check/package.json

key-decisions:
  - "Ecran retenu : prepare.html (nouvelle preparation), celle que main.html ouvre par defaut et que la phase 4 refera"
  - "Parcours fige sur la boite de base (Solo / Spider-Man / Rhino / Standard) : ce contenu ne disparaitra jamais du jeu"
  - "Le test sans navigateur passe en PREMIER (diagnostic) et le parcours navigateur en DERNIER (etat serveur exploitable)"
  - "Attendre la reponse de /new puis exiger render_id = 0 avant de sonder : sans ca le test se felicitait de la partie precedente"
  - "Un tableau vide est compatible avec n'importe quel type de tableau du contrat (challenges est vide dans la plupart des scenarios)"

patterns-established:
  - "Un contrat gele se met a jour DANS LE MEME COMMIT que le changement qui le justifie, jamais pour faire passer un test rouge"
  - "Message d'echec en francais qui dit quoi faire, pas seulement ce qui a change"

# Metrics
duration: 14 min
completed: 2026-07-28
---

# Phase 01 Plan 05 : Contrat de lancement de partie — Summary

**Les 8 clés du `NewGameDescriptor` envoyé à `GET /new?data=` sont figées par écrit dans `contrat-nouvelle-partie.json`, et `npm run lancement` prouve en 4 secondes qu'une partie lancée depuis l'écran de préparation actuel respecte ce contrat puis atteint un plateau réellement rendu — avec la même vérification rejouée sans navigateur, pour dire si c'est l'écran ou le contrat qui a cassé.**

## Performance

- **Duration:** 14 min
- **Started:** 2026-07-28T12:12:00Z
- **Completed:** 2026-07-28T12:26:00Z
- **Tasks:** 2/2 (toutes automatiques, aucun checkpoint)
- **Files modified:** 3 (2 créés, 1 modifié)

## Accomplishments

- **Le contrat existe maintenant par écrit.** `GET /new?data=<descripteur>` était le seul point de contact entre la préparation et le moteur, et il n'était documenté nulle part : ni côté serveur (`server_new_game.py` fait un `Json.LoadsAs` opaque), ni côté client. `contrat-nouvelle-partie.json` est désormais cette documentation, et le test la fait respecter.
- **Le choix d'écran est celui qui protège vraiment.** Le test pilote `prepare.html` (la **nouvelle** préparation), pas l'ancien `scene.html`. Les deux savent lancer une partie et envoient le même descripteur, mais un test sur l'ancien écran serait resté vert pendant que la refonte de la phase 4 cassait le lancement — c'est-à-dire exactement l'accident qu'on veut empêcher. C'est aussi l'écran que `main.html` ouvre par défaut.
- **La preuve d'arrivée au plateau est honnête, et elle a failli ne pas l'être.** Le premier jet sondait `/get_world` juste après le clic : il lisait le monde de la partie **précédente** et se déclarait satisfait sans rien prouver. Mesuré et corrigé (voir déviation 1) : on attend la réponse de `/new`, on vérifie que le monde a été remis à zéro (`render_id = 0`), et seulement ensuite on sonde jusqu'à `render_id > 0` avec une phase de jeu non vide.
- **La vérification survit à la préparation en chantier.** Le second test reconstruit la charge utile depuis les données du serveur et la poste directement sur `/new`, sans navigateur. En phase 4, quand l'écran sera à moitié refait, ce test dira encore si le moteur accepte le contrat.
- **L'échec est bruyant et lisible.** Vérifié sur pièce : en ajoutant une clé et en changeant un type dans le golden, les deux tests échouent avec un message en français qui liste les clés apparues, les clés disparues, les types changés, ce que ça veut dire, et quoi faire selon que le changement est accidentel ou voulu.
- **Rejouable, et sans effet de bord sur le reste du filet.** `npm run lancement` vert deux fois de suite ; `npm run captures` toujours 18/18 ; aucun fichier du jeu touché.

## Task Commits

1. **Tâche 1 : Piloter le lancement d'une partie et capturer le contrat** — `57198d3` (feat)
2. **Tâche 2 : Prouver l'arrivée au plateau** — `039d316` (test)

## Files Created/Modified

- `ui-check/contrat-nouvelle-partie.json` (créé) — le golden. En tête, un `_lisez_moi` explique ce qu'est ce contrat, où le moteur le désérialise, pourquoi on fige les clés et jamais les valeurs, et surtout la règle : **on ne le modifie pas pour faire passer un test rouge**. Contient les 8 clés typées (`campaign_json` string, `campaign_log` object, `challenges` any[], `encounter_set_names` string[], `hero_json` string[], `rules` string[], `seed` number, `timeout` number), un commentaire par clé, `regles_attendues` (`v16_all`), les règles d'une partie standard, les règles optionnelles connues, et la réponse attendue du moteur.
- `ui-check/tests/lancement-partie.spec.ts` (créé, 291 lignes) — deux tests. La logique de comparaison (`ecartsAuContrat`, `typeCompatible`) est isolée en haut du fichier et sert aux deux.
- `ui-check/package.json` — `lancement` limité à `--project=pc`.

## Decisions Made

- **L'écran de départ est `prepare.html`, la nouvelle préparation.** Trois raisons mesurées : c'est ce que `main.html` ouvre par défaut (« Préparer une partie ») ; le parcours complet fonctionne aujourd'hui de bout en bout (vérifié : Solo → Spider-Man → deck de base → Rhino → Standard → plateau) ; et c'est l'écran que la phase 4 refera, donc le seul dont le test protège quelque chose. `scene.html` construit le même descripteur en code inline et resterait vert quoi qu'il arrive à la nouvelle préparation.
- **Le parcours est fixé sur la boîte de base** (Spider-Man, Rhino), pas sur un choix aléatoire. Le bouton « Aléatoire » de l'assistant aurait donné un test plus court mais non reproductible : un scénario tiré au sort peut être expert, multi-vilains ou lourd à mettre en place. Le contenu de la boîte de base, lui, ne disparaîtra jamais.
- **Sélecteurs par rôle et par libellé** (`getByRole('button', { name: /lancer la partie/i })`, `/^Rhino$/`, `/^Spider-Man/`), jamais par classe CSS ni par identifiant : la phase 4 réécrira le DOM, elle gardera les libellés. Les identifiants `#hero-grid` / `#scn-grid` utilisés pendant l'exploration ont été écartés du test final pour cette raison.
- **Le test sans navigateur passe en premier, le parcours navigateur en dernier.** Deux bénéfices : il coûte 20 ms et dit tout de suite si le problème est dans le contrat plutôt que dans l'écran ; et finir par le parcours navigateur laisse le serveur sur une partie **réellement mise en place** (`render_id > 0`) plutôt que sur une partie créée que personne n'a affichée. C'est ce qui rend vraie la vérification `curl get_world` prévue au plan.
- **Le golden porte deux listes de règles.** `regles_attendues` = le minimum contractuel (`v16_all`), comme demandé au plan. `regles_partie_standard` = les trois règles qu'envoie réellement une partie standard, ajoutée parce que le test sans navigateur doit poster une charge **réaliste** : n'envoyer que `v16_all` reviendrait à tester le moteur avec quelque chose que l'écran n'envoie jamais.
- **Un tableau vide est compatible avec n'importe quel `X[]` du contrat.** `challenges` est vide dans la quasi-totalité des scénarios : exiger `any[]` strictement aurait rendu le test rouge le jour où un scénario à défis apparaît, sans qu'aucun contrat n'ait bougé.
- **`?ui=new` explicite au démarrage du test.** Le contexte navigateur part d'un stockage local vide, mais poser la préférence rend l'intention lisible et immunise contre un état résiduel : ce test veut la nouvelle préparation, quoi qu'il arrive à la bascule du plan 01-04.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Le sondage du plateau pouvait valider la partie PRÉCÉDENTE**

- **Found during:** Tâche 2 (vérification de la durée anormalement courte du test : 3,1 s là où l'exploration en demandait 15)
- **Issue:** Le plan prévoyait de sonder `/get_world?p=0` immédiatement après le clic de lancement. Or `page.waitForRequest` se déclenche quand la requête **part**, pas quand le moteur a fait son travail. Si une partie tournait déjà (cas normal : le run précédent), le premier sondage lisait son `render_id > 0` et le test se déclarait satisfait **sans que la nouvelle partie ait démarré**. Un test vert qui ne prouve rien est pire que pas de test : c'est exactement le contraire d'un filet de sécurité.
- **Fix:** Trois ajouts. (a) `page.waitForResponse(/\/new\?data=/)` en plus de `waitForRequest` : le moteur appelle `self.game.NewGame(...)` **avant** de répondre, donc la réponse prouve que le changement d'état a eu lieu. (b) Assertion `render_id === 0` juste après, avec un message qui explique le piège — mesuré : `NewGame` remet bien le monde à zéro. (c) Le sondage ne commence qu'ensuite.
- **Files modified:** `ui-check/tests/lancement-partie.spec.ts`
- **Verification:** L'assertion `render_id === 0` passe à chaque exécution, y compris juste après une partie rendue à `render_id 4` : la remise à zéro est prouvée, et le `render_id > 0` qui suit ne peut plus venir que de la nouvelle partie.
- **Committed in:** `039d316` (Tâche 2)

**2. [Rule 3 - Blocage] `npm run lancement` tournait sur les 3 gabarits**

- **Found during:** Tâche 1
- **Issue:** Le script déclaré au plan 01-01 était `playwright test tests/lancement-partie.spec.ts`, sans projet : 6 tests au lieu de 2, donc **6 parties créées** à chaque exécution pour la même information. Ce test ne vérifie aucune apparence.
- **Fix:** `--project=pc` ajouté (commande unique, compatible `cmd.exe`), comme `bascule` au plan 01-04.
- **Files modified:** `ui-check/package.json`
- **Verification:** `npm run lancement` → « 2 passed », exit 0.
- **Committed in:** `57198d3` (Tâche 1)

---

**Total deviations:** 2 auto-corrigées (1 bug, 1 blocage)
**Impact on plan:** Aucune dérive de périmètre. La déviation 1 est la plus importante du plan : sans elle, le livrable aurait été un test vert qui ne prouvait rien.

## Issues Encountered

- **La phase observée à l'arrivée est `Initialize`, pas `Scenario Setup`.** Le plan citait `"Scenario Setup"` d'après une mesure antérieure. Le sondage rend la main au **premier** rendu du monde, qui arrive plus tôt dans la mise en place. L'assertion porte donc sur « une phase de jeu non vide », comme le plan le demandait, et pas sur une valeur précise — qui aurait été fragile.
- **Le test se termine en pleine mise en place.** Le contexte navigateur se ferme dès que `render_id > 0`, donc le moteur s'arrête là où il en est (`round_id 0`, phase `Initialize`). C'est suffisant pour ce qu'on prouve (le moteur a accepté le descripteur et a commencé à rendre un monde) et ça garde le test à 3 secondes. Aller jusqu'à la première phase de joueur coûterait des dizaines de secondes pour une information qui relève de l'autoplay, pas du contrat.
- **Deux héros s'appellent « Spider-Man »** dans le catalogue (Peter Parker et Miles Morales, 10 et 9 PV). Le test prend le premier ; le descripteur mesuré porte bien `01001a` (Peter Parker).
- **Les valeurs du descripteur varient d'un lancement à l'autre** (`seed: -1` côté écran, contenu du deck, sets modulaires recommandés). C'est précisément pourquoi le golden ne fige que les clés et les types : figer une valeur aurait produit un test rouge en permanence.

## User Setup Required

Aucune — pas de service externe à configurer.

## Next Phase Readiness

**Prêt pour 01-06-PLAN.md** (livraison : re-zip `Fusion/`, autoplay 0 traceback, vérification d'ensemble) :

- Les quatre outils du filet de sécurité sont en place et verts : `npm run captures` (18/18), `npm run fixtures`, `npm run bascule`, `npm run lancement`.
- Aucun fichier du jeu n'a été modifié par ce plan : le contenu à re-zipper est exactement celui laissé par 01-04.

**Points de vigilance à transmettre :**

- **`npm run lancement` détruit la partie en cours.** L'avertissement s'affiche en français au démarrage du test. Cette commande doit rester séparée de `npm run captures` (lecture seule) et ne jamais être enchaînée automatiquement à autre chose.
- **Le contrat gelé n'est pas un fichier comme les autres.** La règle est écrite en tête du golden : on ne le modifie **jamais** pour faire passer un test rouge. Un test rouge veut dire que la préparation a changé ce qu'elle envoie au moteur — soit c'est un accident à corriger, soit c'est voulu, mesuré, et le golden se met à jour **dans le même commit**.
- **La phase 4 réécrira `prepare.html` : ce test est son critère d'acceptation.** Il pilote l'écran par libellés (« Continuer », « Lancer la partie », « Rhino », « Spider-Man ») et non par sélecteurs CSS. Si la refonte change ces libellés, il faudra les mettre à jour dans le test — c'est un geste conscient, pas une régression.
- **Le contrat couvre les clés et les types, pas la sémantique.** Un `campaign_log` de campagne ou un `challenges` non vide restent conformes sans être vérifiés dans le détail : la recherche approfondie de la phase 4 (contrat `/new?data=` et campaign logs des 4 formats) reste au programme.
- **Piège à ne pas réintroduire ailleurs** : sonder un état serveur juste après avoir demandé son changement, sans attendre la réponse qui prouve le changement. Le test lisait l'état précédent et se félicitait.

---
*Phase: 01-filet-de-securite*
*Completed: 2026-07-28*

# TODO / SPEC — Rapport de bug : copier ou télécharger l'état de la partie

**Statut :** **IMPLÉMENTÉ le 2026-08-12.** Plan déroulé
(`.planning/plans/2026-08-12-rapport-de-bug.md`), tâches 1 à 6 faites, six commits
`b3d50d1` à `c8d94ce`, déployé. Reste la **tâche 7** : les quatre vérifications dans
le navigateur, et la mesure du tampon (§4.5), qui demandent un humain.
**Date de conception :** 2026-08-12
**Origine :** demande utilisateur (« un truc qui permet d'avoir une sorte de log
avec les détails importants sur les dernières cartes jouées, pour pouvoir donner
plus facilement les infos quand je pense qu'il y a un bug »)
**Rapport à la roadmap :** indépendant. Ne touche que le plateau.

---

## 1. Le problème

Quand une partie se comporte mal, il faut décrire à la main ce qui venait de se
passer. La description perd exactement ce qui sert à reproduire : quel objet a
été visé, quelle carte a été jouée, ce que le moteur proposait au moment du clic.
Le panneau « H » montre bien l'enchaînement, mais **il est écrit pour être lu par
un joueur** : il nettoie les identifiants avant d'afficher.

## 2. Ce qui existe déjà (vérifié le 12/8/2026)

- **`ui-app/src/board/HistoriquePartie.tsx`**, 495 lignes. Un tampon de
  `MAX_ENTREES = 400` entrées, tous types confondus (`phase`, `text`, `card`,
  `damage`, `heal`, `threat`, `triche`), en `sessionStorage`. Chaque entrée porte
  déjà `round`, `phase`, `renderId`, `cibleId`, `joueur` et `acteur`.
- **`ui-app/src/board/causalite.ts`** : la mémoire des causes, qui sait dire « par
  X » sur un fait. `JournalHeros.tsx` puise dans le même tampon, filtré par héros.
- **Les identifiants sont dans la source, mais ils ne SURVIVENT pas dans le
  journal.** Le moteur envoie `world.prompt` avec des références de la forme
  `[(id,card_id) Nom]`. ⚠️ **CORRIGÉ le 12/8 après mesure** : cette fiche disait
  « le rapport n'a qu'à ne pas nettoyer », et c'était faux. `sansIdentifiants()`
  n'est pas appliquée à l'affichage mais **à la création de l'entrée**, par
  `texteSignificatif()` (`HistoriquePartie.tsx:73`) : ce qui est stocké en
  `sessionStorage` est déjà propre. Les entrées `card`, `damage`, `heal` et
  `threat` gardent bien leur `cibleId`, donc leur object ID est récupérable sans
  rien changer ; mais les entrées `text` de narration perdent leurs identifiants
  définitivement. D'où le champ `brut` ajouté au journal (tâche 1 du plan).
- **La demande du moteur est un objet complet** : `Demande` dans
  `ui-app/src/board/ask.ts:50` porte `options`, `prompt_text`, `event_name`,
  `show_cancel`, `ability_type`, et chaque option ses cibles et ses moyens de
  paiement.
- **`World`** (`ui-app/src/board/world.ts:69`) porte l'état complet visible :
  `render_id`, `round_id`, `phase`, les zones, et `mode_sandbox`, qui est
  conservé dans la sauvegarde.

Autrement dit : **tout le contenu du rapport existe déjà en mémoire du plateau.**
Le chantier est un assemblage et une sortie, pas une collecte nouvelle.

## 3. Décisions prises avec l'utilisateur (12/8/2026)

| Question | Décision |
|---|---|
| Forme | **Les deux** : un bouton « Copier » qui met un résumé texte dans le presse-papier, et un bouton « Télécharger » qui sort un `.json` complet |
| Profondeur | **Réglable au moment du clic** : « 20 dernières / ce tour / toute la partie » |
| Contenu | **Les quatre** : identifiants techniques, état de la table, demande en cours, contexte technique |

### Le détail du contenu retenu

1. **Identifiants techniques** : object ID (`c49`), `card_id`, nom, zone,
   propriétaire. ⚠️ **CORRIGÉ le 12/8** : la fiche demandait « le nom anglais en
   plus du français ». C'est sans objet, le moteur n'envoie qu'UN nom et il est
   anglais (mesuré sur les 35 fixtures : `"name": "None Shall Pass"`). `TEXTES_FR`
   porte le TEXTE des cartes, jamais leur nom. Le rapport recopie `carte.name`. C'est ce qui permet de viser la bonne
   carte depuis la console. Le piège documenté vaut d'être rappelé dans le
   rapport lui-même : **une commande se vise par object ID**, par nom l'étoile
   des cartes uniques fait tout échouer en silence, et par `card_id` une carte
   absente du jeu est fabriquée dans la zone mise de côté.
2. **État de la table** : PV et menace de chaque carte en jeu, mains, défausses,
   ressources disponibles, phase et round.
3. **La demande en cours** : options proposées, cibles légales, coût à payer.
   C'est la pièce qui manque quand le symptôme est « ça ne me laisse pas cliquer ».
4. **Contexte technique** : scénario, héros, difficulté, mode
   (solo / multi / campagne / sandbox / découverte), campagne et scénario en
   cours s'il y en a, `render_id`, `round_id`, et les erreurs console récentes.

## 4. Les chantiers

### 4.1 Un module de rapport

Un module qui prend `(world, demande, historique, profondeur)` et rend deux
choses : un texte lisible et un objet complet. Testable sans navigateur, donc
couvert par vitest comme le reste de `ui-app/src/board`.

### 4.2 La version texte

Faite pour être collée dans une conversation. En-tête de contexte, puis les
entrées choisies, **avec** leurs identifiants, puis la demande en cours. Le
volume compte : elle doit rester collable pour le cas « 20 dernières ».

### 4.3 La version fichier

Un `.json` structuré, nommé avec le scénario et le round. Rien de tronqué. Objectif
déclaré : pouvoir rejouer ou au moins reconstituer la situation.

### 4.4 Le sélecteur de profondeur

Trois valeurs, dans le panneau « H », avant les deux boutons. « Ce tour » se lit
sur `round` des entrées, qui est déjà stocké.

### 4.5 Le tampon

400 entrées couvrent une partie, mais le commentaire de `MAX_ENTREES` dit que le
moteur émet une entrée de narration à chaque rendu. **À mesurer** : est-ce que
« toute la partie » tient vraiment dans le tampon sur une partie longue à quatre
joueurs, ou est-ce qu'on perd le début en silence ? Si on tronque, le rapport
doit le DIRE, sinon il se lit comme complet.

## 5. Tranché au plan (12/8/2026)

| Question | Décision |
|---|---|
| Où vivent les boutons | Dans le panneau « H » **et** derrière le raccourci `B`, pour capturer sans ouvrir le panneau. `B` était libre : seuls `E` et `U` étaient pris |
| Le rapport en multi | **Complet, avec un avertissement en tête.** Le `world` du siège contient déjà les mains adverses : on ne révèle rien de neuf, et un rapport amputé rate justement le bug |
| Capture au clic ou en continu | **Au clic seulement.** Aucun tampon d'états, aucun coût mémoire. Risque assumé : si le moteur a déjà rendu la suite, l'état de table décrit n'est plus celui du bug |
| Le tampon (§4.5) | Le rapport **DIT** qu'il est tronqué quand les 400 entrées sont pleines. La mesure « est-ce que toute la partie y tient ? » reste à faire en vraie partie |

### Le texte d'origine de cette section



- **Où vivent les deux boutons** : dans le panneau « H », ou aussi derrière un
  raccourci clavier pour capturer sans ouvrir le panneau (le bug peut disparaître
  au rendu suivant).
- **En multi, un rapport contient les mains adverses.** Le `world` envoyé au
  client les contient déjà, donc rien n'est révélé qui ne le soit, mais un
  fichier qui traîne n'est pas un `world` en mémoire. À décider : rapport limité
  à ce que le siège voit, ou rapport complet avec un avertissement.
- **Faut-il capturer au moment du clic ou en continu ?** Au clic, l'état du bug
  peut avoir déjà été remplacé par le rendu suivant.

## 6. Comment on saura que c'est fait

Sur un bug réel : un clic, un collage, et l'information suffit à nommer la carte
par son object ID et à rejouer le geste sans poser de question en retour.

**Non atteint à ce jour.** Le code est écrit, testé (43 cas vitest ajoutés,
`tsc --noEmit` et `vite build` verts) et déployé, mais aucun rapport n'a été pris
sur une vraie partie. Les quatre vérifications qui restent sont détaillées à la
tâche 7 du plan :

1. Panneau « H », « 20 dernières », **Copier**. Le texte collé doit contenir au
   moins un `c<nombre>`, le nom du scénario, et la section « DEMANDE EN COURS »
   renseignée si le moteur attend une réponse.
2. Touche `B` **panneau fermé** : « Rapport copié » s'affiche, le presse-papier change.
3. « Toute la partie », **Télécharger** : fichier `rapport-<scenario>-r<n>.json`,
   qui s'ouvre sans erreur de syntaxe.
4. Taper `b` dans un champ de saisie : le rapport **ne doit pas** partir.

Et la mesure laissée ouverte par le §4.5 : lire le compteur du bouton « H » en fin
de partie. S'il atteint 400, « toute la partie » perd le début — le rapport le dit
déjà, mais on saura si le cas se produit vraiment.

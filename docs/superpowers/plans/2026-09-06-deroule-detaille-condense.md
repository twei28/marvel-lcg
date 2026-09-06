# Le déroulé détaillé condensé : plan d'exécution

> **Pour les agents :** utiliser `superpowers:subagent-driven-development`.

**Spec :** `docs/superpowers/specs/2026-09-06-deroule-detaille-condense-design.md`

**But :** le cartouche de la phase du méchant dit une chose par étape, en cinq
temps, sans narration technique, et ne fait cliquer deux fois que là où le
joueur peut vraiment agir.

**Pile :** React 19, TypeScript strict, Vitest. Moteur Python pour la seule
donnée qui manque, si le chemin par l'interface ne suffit pas.

## Contraintes globales

- TypeScript strict, zéro `any`.
- Tout texte affiché passe par `t(...)`, traduction dans `ui-app/src/board/dico-en.ts`.
- Commentaires en français, expliquant le POURQUOI.
- Aucun em dash. Aucun `flushSync`, jamais.
- Tous les hooks de `DeroulePhase.tsx` AVANT son `return null`.
- Un `useEffect` qui dépend d'un objet du monde se relance à chaque trame :
  dépendre de la clé.
- Ne jamais modifier un composant pour faire passer un test.
- Une autre session travaille sur `Fusion/marvel-lcg-src/public/js/prepare/` :
  ne rien emporter de ce dossier.
- Vérifications après chaque tâche : `npx vitest run` et `npx tsc --noEmit`
  depuis `ui-app/`.

## Ce qui existe déjà et qu'il ne faut pas refaire

- Le fait du moteur (`FaitMechant`, `ui-app/src/board/world.ts:75`) porte déjà
  `base`, `boost`, `defense`, `inflige`, `subi`, `restant`, `round_id`,
  `phase`, `cause` et la liste des `boosts`. **Le chiffre du résultat est donc
  disponible, rien à ajouter côté moteur pour l'obtenir.**
- Le cartouche relâche déjà le moteur à chaque « Suivant » (commit `68381f9`).
- Les faits portent déjà leur round (commit `88168eb`).

## Fait établi qui commande l'ordre des tâches

`RecordFaitMechant` est appelé à la FIN d'une activation
(`can_attack.py:546`). Au moment où le joueur peut défendre, **le fait n'existe
pas encore**. Le dédoublement en deux temps (décision 7 de la spec) ne peut donc
pas venir des faits : il devra lire l'événement en cours du moteur. C'est la
tâche la plus incertaine, elle vient en dernier.

---

## Tâche 1 : cinq temps, et les temps vides barrés

**Fichiers :** `deroule-phase.ts`, `DeroulePhase.tsx`, `board.tsx`, `board.css`,
plus leurs tests.

`TempsPhase` passe de quatre à cinq positions : `menace`, `mechant`, `sbires`,
`distribution`, `revelation`.

Pour ranger un fait sous `mechant` ou `sbires`, il faut savoir si son auteur est
le vilain ou un sbire. `etapesDeroule` ne voit pas le monde. **Passer
l'information depuis `board.tsx`**, qui dispose déjà de `cartesMondeParId` avec
le `kind` de chaque carte : un argument supplémentaire, par exemple un
`Set<number>` des identifiants d'ennemis « méchant », ou une fonction de
consultation. Ne pas modifier le moteur Python pour cela : le chemin par
l'interface est plus court et marche aussi sur une sauvegarde ancienne.

Un auteur inconnu (carte déjà partie de la table) se range sous `sbires` : c'est
le cas le plus fréquent, et se tromper là coûte une pastille, pas une règle.

La chronologie affiche les cinq temps avec **quatre états** : passé (`✓`),
courant, à venir, et **vide** (grisé et barré, aucune étape produite). Un temps
est vide quand aucune étape ne le porte.

## Tâche 2 : le titre dit ce qui se passe, avec son chiffre

**Fichiers :** `deroule-textes.ts`, `deroule-phase.ts`, `DeroulePhase.tsx`,
`dico-en.ts`, plus leurs tests.

Le titre générique disparaît au profit d'une phrase concrète :

- menace : `L'Effraction ! gagne 2 menaces`, et le compteur de la carte à droite
  (`5/8`). La liste de conséquences qui doublait le titre disparaît ; s'il y a
  plusieurs manigances touchées, une étape par manigance.
- attaque : `Klaw attaque Colossus` puis, en dessous, `→ 4 dégâts`. Prendre
  `subi` (ce que la cible a réellement encaissé), pas `inflige`.
- manigance d'un ennemi : `Klaw complote contre L'Effraction !` puis
  `→ 2 menaces`.
- révélation : `Colossus révèle Bombe à retardement`.

Le compteur de la cible vient de `restant`, qui peut être absent ou nul : ne
rien afficher dans ce cas plutôt qu'un `undefined`.

Ajouter aussi le compteur d'étapes du temps courant (`1 sur 3`) quand le temps
en compte plusieurs, et rien quand il n'en compte qu'une.

## Tâche 3 : la règle se replie, et le choix se retient

**Fichiers :** `DeroulePhase.tsx`, `moteur.ts` (le réglage), `board.css`,
`dico-en.ts`, plus leurs tests.

La règle passe sous un dépliant `› la règle`. Son état est un réglage personnel
retenu dans `localStorage`, sur le modèle exact de `lireAvanceAuto` /
`ecrireAvanceAuto` (`moteur.ts`) : une clé, un lecteur, un écrivain, et un
`try/catch` autour du stockage.

Une fois déplié, il le reste sur toutes les étapes et toutes les parties jusqu'à
ce que le joueur le replie.

## Tâche 4 : la narration technique quitte le cartouche

**Fichiers :** `deroule-phase.ts`, `DeroulePhase.tsx`, `board.css`, plus leurs
tests.

Le bloc qui pousse une étape quand `e.type === 'text' && e.brut` disparaît. Avec
lui disparaissent le champ `brut` de `EtapeDeroule`, le champ `auto` (plus rien
ne le produit), le minuteur d'enchaînement automatique de `DeroulePhase.tsx` et
l'état `suspendu` qui n'existait que pour lui.

⚠ Vérifier avant de supprimer que rien d'autre ne produit `auto`. Supprimer les
tests devenus sans objet, et dire dans le rapport lesquels et pourquoi. Ce code
reste récupérable dans git si l'on change d'avis.

Rien n'est perdu pour le joueur : ces lignes restent au journal et au Log.

## Tâche 5 : le bilan de fin de phase

**Fichiers :** `deroule-phase.ts`, `deroule-textes.ts`, `DeroulePhase.tsx`,
`board.css`, `dico-en.ts`, plus leurs tests.

Une dernière étape, de temps `bilan`, ajoutée après toutes les autres :

    FIN DE LA PHASE DU MÉCHANT
    Colossus a pris 6 dégâts                     8/14 PV
    L'Effraction ! a gagné 3 menaces                6/8

                                        [ À toi de jouer ]

Les totaux se calculent depuis les faits du round et les entrées de menace, pas
depuis une comparaison de photos du monde. Le bouton porte « À toi de jouer »
au lieu de « Suivant », et c'est lui qui déclenche `onTerminer`.

En multijoueur, une ligne par héros touché.

## Tâche 6 : un héros vaincu arrête le déroulé net

**Fichiers :** `deroule-phase.ts`, `DeroulePhase.tsx`, `board.css`,
`dico-en.ts`, plus leurs tests.

Quand une étape a mis un héros à terre, elle porte une marque `☠ COLOSSUS EST
VAINCU`, le déroulé n'affiche aucune étape au-delà, et le bouton dit
« Continuer ».

La source : chercher dans les entrées du journal du round l'événement de
défaite, et le rattacher à l'étape dont il est la conséquence. Vérifier dans le
code comment une défaite se présente avant d'écrire quoi que ce soit.

## Tâche 7 : le multijoueur, dans l'ordre officiel

**Fichiers :** `deroule-phase.ts`, `deroule-textes.ts`, plus leurs tests.

Les révélations de cartes rencontre sont ordonnées **par ordre du tour, en
commençant par le premier joueur**, et toutes sont montrées à tous. Chacune
porte le nom du héros concerné et son compteur (`2 sur 3`).

Trouver dans `World` l'ordre des joueurs et le premier joueur ; ne pas le
deviner.

## Tâche 8 : deux temps quand le joueur peut agir

**La plus incertaine. Commencer par une investigation écrite, avant tout code.**

Le fait n'existe pas encore au moment où le joueur peut défendre. L'étape
« intention » doit donc venir d'ailleurs : très probablement de l'événement en
cours du moteur (`World.prompt`, `World.event_name`), c'est-à-dire de la même
source que le panneau central existant.

Questions à trancher par la lecture du code, et à écrire avant d'implémenter :

1. Comment sait-on qu'une fenêtre de réponse est ouverte, plutôt qu'une simple
   attente technique ? Regarder `etat.demande`, `demandeDoitApparaitreAuCentre`,
   et `evenementNarreImportant`.
2. Le nom de l'attaquant et de la cible sont-ils lisibles à ce moment-là ?
3. Que se passe-t-il si le joueur ne fait rien ? L'étape « intention » doit-elle
   se fondre dans l'étape « résultat » quand la fenêtre se referme sans action ?

Si l'investigation montre que le coût dépasse le gain, **le dire et s'arrêter**
plutôt que de livrer un mécanisme fragile sur le chemin critique d'une partie.

---

## Après les huit tâches

Contrôle en partie réelle, avec les yeux : une phase complète en solo, puis une
au round 4 et plus, puis une avec un héros vaincu. Les défauts les plus graves
de ce chantier ont tous été trouvés ainsi, jamais par les tests.

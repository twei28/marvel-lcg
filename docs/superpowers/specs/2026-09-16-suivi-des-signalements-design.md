# Le suivi des signalements

Cadrage du 16/09/2026, question par question. Ce document fait foi : ce qui n'y
est pas n'est pas décidé.

## La demande, dans ses mots

« Quand les gens m'envoient un bug, s'ils ont un compte, j'aimerais que quand je
corrige ou que je réponde, il y ait une petite modale qui s'ouvre pour voir ma
réponse (et donc il faudrait me permettre de mettre une réponse), voire
développer tout un truc de tickets » (15/09/2026).

Interrogé sur la taille, il a choisi **le vrai suivi de tickets** : des états,
un fil dans les deux sens, une page côté joueur, une notification.

## Ce qui existe déjà, et qu'on ne redécouvre pas

Les trois questions que la fiche de backlog disait bloquantes sont répondues,
en lisant le code plutôt qu'en les posant.

- **Le code du site est dans ce dépôt** : `site/orchestrateur.py`, base SQLite
  `site/narwhal.db`, pages HTML écrites en Python.
- **La table `rapports` existe**, avec `hote` (le compte propriétaire de la
  table), `nom` (ce que la personne a tapé), `siege`, `ecran`, `description`,
  `journal`, `capture` (sur disque, jamais en base), `etat`, `traite_le`.
- **Trois états existent déjà** : `nouveau`, `en cours`, `traite`
  (`ETATS_RAPPORT`). L'écran `/admin` les groupe et sait les changer.
- **La purge** efface un rapport classé « traité » depuis plus de 30 jours,
  capture comprise (`JOURS_RAPPORTS_TRAITES`). Motif écrit dans le code : 12
  rapports par heure et par table, capture jusqu'à 4 Mio, sauvegardes de nuit
  multipliant le tout par trente.
- **Le canal de notification est complet** : `/api/prives` côté site, relayé
  par `/get_messages_prives` côté moteur (le navigateur est sur
  `p<N>.<domaine>`, son cookie de site ne voyagerait pas), affiché par
  `public/js/prepare/messages.js` en partie comme sur la préparation.
- ⚠ **Ce relais est réservé au siège 0**, volontairement : « un invité arrivé
  par un lien de siège n'a pas à savoir qu'il a reçu un message ».

## Le point dur : qui est l'auteur d'un rapport

Une table appartient à un compte. Les autres sièges sont des invités, **même
quand la personne a un compte par ailleurs**, et le rapport de bug leur est
ouvert exprès : « ce sont justement ceux qui n'ont aucun autre moyen de le
dire ».

Le rapport porte donc `hote` (le compte de la table) et `siege`, jamais
l'identité d'un invité.

**Décision : le ticket est réservé au siège 0.** Le rapport d'un siège 0 est un
ticket dont l'auteur est `hote`, sans rien ajouter au plateau. Les autres
restent des rapports, lus et traités, sans fil ni réponse. Le formulaire de
signalement le dit honnêtement à celui qui n'est pas titulaire.

Les deux autres pistes ont été écartées : demander son pseudo à l'invité (on
peut taper celui d'un autre et lui coller un ticket), et faire passer la
réponse par l'hôte (il lirait le signalement et la capture de quelqu'un
d'autre).

## Ce qu'on construit

### 1. Les données

- `ETATS_RAPPORT` gagne `refuse`, soit quatre états. Libellés côté joueur :
  **Reçu / En cours / Corrigé / Refusé**. « Refusé » couvre « ce n'est pas un
  bug » comme « je ne le ferai pas », et oblige à écrire pourquoi.
- Table `rapports_messages` : `id`, `rapport_id`, `auteur` (`admin` ou
  `joueur`), `texte`, `quand`, `lu_le` (NULL tant que le destinataire ne l'a
  pas ouvert).
- Migration sur le modèle de `traite_le` : `CREATE TABLE IF NOT EXISTS` et un
  `PRAGMA table_info`. Aucune reprise des rapports existants : ceux de siège 0
  deviennent des tickets, les autres restent ce qu'ils sont.

### 2. Les écrans

- **`/admin`**, section Rapports : sous chaque rapport, le fil, un champ
  « répondre », les quatre boutons d'état. Même patron que l'existant, des
  formulaires POST vers `/admin`, zéro JavaScript.
- **`/signalements`**, page nouvelle, réservée à un compte connecté : ses
  rapports, leur état, la capture tant qu'elle existe, le fil, un champ pour
  répondre. Un compte n'y voit QUE ses propres tickets.
- **`_barre()`** gagne une entrée « Mes signalements » pour tout le monde, avec
  un compteur quand une réponse n'est pas lue.

### 3. La notification

`/api/prives` rend, en plus des messages, le nombre de réponses de tickets non
lues. **Le moteur n'est pas touché** : `get_messages_prives` recopie ce que le
site lui donne. Pas de redémarrage de serveur pour cette partie.

`messages.js` pose **une seconde pastille, distincte**, « Réponse à ton
signalement », d'une autre couleur, qui ouvre `/signalements`. Le joueur sait
où il va avant de cliquer, et un message privé ne se confond pas avec un suivi
de bug.

La pastille partagée a été écartée : quand les deux attendent en même temps,
l'une des deux destinations passe à la trappe.

### 4. La purge

`purger_rapports_traites` n'efface plus le rapport. À 30 jours elle supprime le
fichier capture et met `capture = NULL` ; le rapport et son fil restent
consultables. Même règle pour les rapports sans ticket, plutôt que deux
régimes à tenir : c'est l'image qui pesait, pas le texte.

## Ce qu'on ne fait pas

- Aucune modale sur le plateau. La réponse se lit sur `/signalements`, le
  plateau est le pire endroit pour relire un fil et taper une réponse.
- Aucun ticket ouvert sans bug. Le rapport est la seule porte d'entrée.
- Aucun courrier électronique. Le site n'en envoie pas, et ce chantier ne le
  lui apprend pas.
- Le tchat retiré du jeu le 12/09/2026 n'est pas réveillé : le fil d'un ticket
  vit dans sa propre table, pas dans `messages`.

## Ce qu'on teste

Dans `site/test_parcours.py`, avec le reste des tests du site.

1. Un rapport de siège 0 ouvre un ticket ; un rapport de siège 2 n'en ouvre
   pas.
2. Une réponse de l'administrateur apparaît chez son auteur, et **un autre
   compte ne la voit pas** en demandant `/signalements`.
3. Le joueur répond, sa réponse se range dans le bon fil et apparaît dans
   `/admin`.
4. La pastille compte la réponse non lue, puis s'éteint une fois le fil ouvert.
5. Les quatre états se posent et se relisent, y compris `refuse`.
6. La purge à 30 jours efface le fichier capture, met `capture` à NULL, et
   laisse le rapport et son fil en place.

## Ce qui reste ouvert

Rien sur le périmètre ci-dessus. Le seul inconnu est le volume réel : si le
suivi se remplit de tickets jamais fermés, la question de l'archivage se posera
d'elle-même, et elle n'est pas tranchée ici.

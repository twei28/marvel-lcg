> **MISE À JOUR 23/10/2026 : FAIT, l'en-tête ci-dessous est périmé** (ancien état : « « NON COMMITÉ, NON DÉPLOYÉ » »). Preuve : Commité : `efb0709b` (branche `multi-invitations`, 2 commits que HEAD ne contient pas par leur identifiant) ; mais les fichiers sont **identiques** dans HEAD (`git diff --stat HEAD multi-invitations` sur `site/orchestrateur.py`, `retour-salon.ts`, `invitations.js` : 0 ligne), arrivés par `4f40f966`. Le code est donc dans les … (tri : `docs/rapports/etat-du-backlog-2026-10-19.md` §3, n°9).

# Inviter un joueur connecté (multi en ligne avec comptes)

Statut : CODÉ ET VÉRIFIÉ À DEUX NAVIGATEURS le 13/10/2026. NON COMMITÉ, NON DÉPLOYÉ (voir « Fait » en bas).

## Demande de l'utilisateur

« Un lance une partie, et il y a une petite fenêtre qui propose les gens qui
sont en ligne. » Et : « quand quelqu'un a déjà un compte, qu'il voie exactement
le même truc pour prendre le héros et le deck que d'habitude, sauf la phase
méchant, que choisit la personne qui crée la partie ».

## Décisions (une question à la fois, 13/10/2026)

1. **Où l'invité voit l'invitation** : partout sur le site, petite fenêtre
   « Arnaud t'invite à sa partie · Rejoindre / Refuser ».
2. **Où l'hôte invite** : dans la préparation, étape « Coop en ligne ». Deux
   choix côte à côte : « Créer des liens » (comme aujourd'hui) ou « Inviter
   quelqu'un de connecté », qui liste les seuls comptes connectés avec un
   bouton Inviter.
3. **Ce que voit l'invité après Rejoindre** : SA préparation habituelle, avec
   SES decks, étapes héros et deck seulement ; le méchant et le mode choisis
   par l'hôte en lecture seule, mis à jour en direct.
4. **Suivi côté hôte** : état en direct sous chaque nom : « Invité… » →
   « A rejoint · choisit son héros » → « Spider-Man · Justice · prêt » ; ou
   « A refusé » / « Sans réponse · Relancer ». Lancer s'allume quand tous
   sont prêts.
5. **Nombre de joueurs** : l'hôte le fixe d'abord (2 à 4), comme aujourd'hui.
6. **Mélange** : siège par siège, « Inviter un connecté » ou « Copier le
   lien » ; un ami sans compte garde le lien.

## L'équipe reste ensemble après la partie (ajout du 13/10/2026)

Demande : « en fin de partie, que les joueurs qu'on a invités restent dans le
même lobby, et dès qu'on crée une partie, qu'ils aient de nouveau accès à la
sélection de personnages ».

7. **Toute fin de partie** (défaite, victoire, abandon) : les invités restent
   à la table jusqu'à ce que l'un d'eux quitte.
8. **Nouvelle partie** : dès que l'hôte en crée une, les invités retrouvent la
   sélection héros + deck, avec le héros et le deck de la partie d'avant
   PRÉ-COCHÉS (un clic sur « Je suis prêt » suffit pour rejouer pareil).
9. **Invités par lien sans compte** : même traitement, leur siège leur reste
   tant qu'ils gardent la page ouverte.

## Ce qui existe déjà (relevé du 13/10/2026)

- Présence : `site/orchestrateur.py` `toucher_presence` / `presence()`
  (en ligne < 120 s), affichée seulement dans le tchat et /admin.
- Liens de sièges : `get_liens_sieges` (server_get.py, siège 0), bouton
  « Générer les liens » dans `public/js/prepare/app.js` (~l.1416-1505).
- L'invité arrive aujourd'hui sur `salon.html` (écran à part), en anonyme :
  son compte n'est pas reconnu par le moteur (sièges = cookie
  `seat_token_<n>` posé par `/claim_seat`).
- Temps réel : polling HTTP seulement (2 s salon, 20 s messages).

## Points techniques à trancher à l'écriture

- Chaque compte a sa table `p<N>` : l'invité rejoint celle de l'hôte, mais
  ses decks vivent dans SON emplacement. Il faut les lui servir à la table
  de l'hôte.
- La fenêtre d'invitation « partout sur le site » demande un polling léger
  sur toutes les pages (s'appuyer sur `toucher_presence`).
- Les liens changent à chaque allumage de la table : l'invitation doit
  porter un lien frais, généré au clic.

## Fait (13/10/2026)

- Site (`site/orchestrateur.py`) : registre des invitations EN MÉMOIRE
  (`inviter_a_la_table`, `invitations_pour`, `repondre_invitation`,
  `invitations_de`, `connectes`, `decks_de_l_invite`), routes `/api/connectes`,
  `/api/inviter`, `/api/invitations` (vaut signe de vie), `/api/invitation_reponse`,
  `/api/invitations_envoyees`, `/api/decks_invite`. Test :
  `python3 site/test_inviter_un_connecte.py` (25 cas).
- Moteur (`server_get.py`) : relais `get_connectes`, `post_inviter`,
  `get_invitations`, `post_invitation_reponse`, `get_invitations_envoyees`
  (siège 0), `get_decks_invite` (le siège de l'invité), et le signal
  `annoncer_preparation` / `get_preparation`. Test : `tools/test_salon.py`.
- Fenêtre « X t'invite » : `public/js/prepare/invitations.js`, posée sur
  prepare, deck-builder, campagne et le plateau (ui-app/board.html).
- Hôte : étape « Coop en ligne », boutons « Créer des liens » / « Inviter
  quelqu'un de connecté », puis par siège : liste des connectés, état en
  direct, « Réinviter », « Copier le lien ».
- Invité : salon avec « Ton deck » (decks de son compte, copiés chez l'hôte
  au choix), équipe et méchant visibles en permanence.
- Équipe qui reste : l'écran de fin de l'invité dit « Retour au salon », et
  l'y ramène tout seul quand l'hôte rouvre la préparation
  (`ui-app/src/board/retour-salon.ts`) ; héros et deck d'avant pré-cochés,
  « Je suis prêt » (`public/js/salon/bascule.js`, dernier choix).
- Défaut corrigé au passage : une partie finie pendant la mise en place
  laissait la fenêtre de mise en place par-dessus l'écran de fin.

Écart assumé, à valider par l'utilisateur : l'invité garde l'écran du SALON
(mêmes étapes Héros › Decks que l'assistant, même grille), pas
`prepare.html` lui-même.

Avant déploiement : entrées « Nouveautés » fr + en (deployer-tout.sh l'exige).

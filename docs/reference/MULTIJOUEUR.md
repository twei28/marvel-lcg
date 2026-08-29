# Jouer en ligne à plusieurs — mode d'emploi

Ce dossier permet de lancer une **partie Marvel Champions en ligne**, où des amis rejoignent ta partie depuis leur navigateur, sans rien installer de leur côté.

---

## En bref — comment ça marche

Quand tu lances `JOUER-EN-MULTI.bat` :

1. Le **moteur du jeu** démarre sur ton PC (dans WSL), sur le port `2347`, avec un **mot de passe** actif.
   Le port vient de `server_addresses` dans `Fusion/marvel-lcg-src/launch.online.json` ; le lanceur
   le relit à chaque démarrage, il suffit de modifier ce fichier pour en changer.
   Il est volontairement **différent du port `2345` de la partie solo**, pour que les deux puissent
   tourner en même temps : le moteur refuse de démarrer si son port est déjà pris (et le lanceur
   multi se referme alors avec « Le moteur s'est arrete au demarrage »).
2. Un **tunnel Cloudflare** s'ouvre : il rend ton PC accessible depuis Internet via une adresse temporaire du type `https://xxxx.trycloudflare.com`.
3. La fenêtre t'affiche **un lien PERSONNEL par joueur** (il réserve son siège) et **le mot de passe d'entrée** (le message est aussi copié dans ton presse-papier, prêt à coller dans Discord/WhatsApp).
4. Chaque ami clique sur **son** lien, entre le mot de passe d'entrée, et arrive sur **le salon** : il y choisit son héros, puis son deck. Son choix apparaît chez toi au fur et à mesure, et il peut encore changer d'avis tant que tu n'as pas lancé. Son siège est **verrouillé** : personne ne peut jouer à la place d'un autre.
5. Toi (hôte), tu cliques sur **ton** lien local affiché dans la fenêtre : il réserve ton siège puis ouvre l'écran de création de partie.
6. **Ctrl+C** dans la fenêtre = fin de la partie pour tout le monde (le tunnel se ferme, le lien ne marche plus).

Rien n'est exposé en dehors de la durée de la partie : dès que tu fermes, tout se coupe.

---

## Prérequis (déjà installés)

Le lanceur a besoin de :

- **WSL** (Ubuntu) sur Windows.
- **Python 3.10** — présent dans WSL : `~/marvel-work/python/bin/python3.10`.
- **cloudflared** (le tunnel) — présent dans WSL : `~/marvel-work/tools/cloudflared`.

> ⚠️ Ces outils vivent dans **WSL** (`~/marvel-work/…`), pas dans ce dossier. Le jeu Windows de ce dossier sert de source, mais le moteur et le tunnel tournent côté WSL. Si tu réinstalles Windows/WSL, il faudra les remettre.

---

## Lancer une partie

1. Double-clique sur **`JOUER-EN-MULTI.bat`** (dans ce dossier).
2. Laisse la fenêtre noire **ouverte** pendant toute la partie.
3. Attends l'encadré « PARTIE MULTI PRÊTE », puis **copie/colle le lien + le mot de passe** à tes amis.
4. Sur **ton** PC, le jeu s'ouvre aussi : c'est toi qui **crées la partie** (choix scénario, héros, etc.).
5. Chaque joueur ouvre le lien, entre le mot de passe, prend son siège et **choisit son héros et son deck**.
6. Quand tout le monde a choisi, ton bouton **Lancer la partie** s'allume. Tes amis basculent tout seuls sur le plateau.

Pour terminer : **Ctrl+C** dans la fenêtre (ou ferme-la).

---

## Les mots de passe

- **Mot de passe d'entrée** (commun) : défini dans **`Fusion/marvel-lcg-src/launch.online.json`**, champ `"password"`. Demandé à l'arrivée sur le site.
- **Mots de passe de sièges** (un par joueur) : champ `"seat_passwords"` du même fichier (4 valeurs : Joueur 1 = toi, puis Joueurs 2-4). Ils sont intégrés aux liens personnels affichés par le lanceur : chacun ne peut agir QUE sur son siège. Une valeur vide = siège libre pour tous; liste entièrement vide = protection coupée (ancien comportement).
- Le lanceur **affiche** tout à chaque partie (et le copie dans le presse-papier), donc tu n'as rien à retenir.
- Pour changer un mot de passe : édite `launch.online.json` et relance.
- **`launch.online.json` n'est plus suivi par git** (10/8/2026). Il porte des secrets, et un
  secret commité ne se change plus : il reste dans l'historique pour toujours. Les quatre
  mots de passe de sièges y étaient en clair depuis le 6 août ; ils ont été renouvelés, et
  ceux de l'historique ne valent donc plus rien. Le dépôt n'a jamais eu de remote, rien
  n'est sorti de la machine. Le fichier `launch.online.exemple.json`, lui, reste suivi :
  même structure, aucun secret. Sur une machine neuve, le copier et remplir les deux champs.
- Les parties solo (`JOUER-SOLO.bat`) ne sont **pas concernées** : aucun mot de passe en local.

---

## Bon à savoir / limites actuelles

- **Le lien change à chaque lancement** (tunnel temporaire Cloudflare). Normal.
- **Ton PC doit rester allumé** et la fenêtre ouverte pendant toute la partie.
- **Sièges protégés** (depuis le 2/8/2026) : chaque joueur a son lien personnel et ne peut pas agir sur le siège d'un autre. Regarder la partie reste ouvert à quiconque a le mot de passe d'entrée (`…/rejoindre.html` → « Juste regarder »).
- **Coupure réseau** : le plateau se reconnecte tout seul (bandeau avec compte à rebours et bouton « Reconnect now ») ; la partie reprend où elle en était.
- **Le lancement attend tout le monde** : le bouton reste gris tant qu'un siège n'a pas choisi, et la barre du bas dit qui on attend. Le **nombre de joueurs**, c'est toi qui le fixes à l'étape 1.
- **Le réglage « premier joueur » est grisé en multi** : c'est toujours le Joueur 1 qui commence. Sinon l'ordre des joueurs tournerait et chacun se retrouverait avec le deck de son voisin.
- **Les invités ne construisent pas de deck depuis le salon** : ils choisissent parmi le deck de base, les paquets d'aspect conseillés et les decks déjà enregistrés sur le serveur. Pour un deck sur mesure, ils passent par `…/deck-builder.html` (avec le mot de passe d'entrée) : leur deck apparaîtra ensuite dans leur liste, et dans la tienne.
- **Ferme bien la fenêtre à la fin.** Tant que la fenêtre noire reste ouverte, le moteur garde son port (2345 en solo, 2347 en multi) **et le tunnel reste ouvert**. Au lancement suivant, le jeu refusera de démarrer avec `AssertionError: port=2345` : ce n'est pas un bug, c'est le moteur qui refuse de tourner en double. Pour vérifier ce qui traîne encore, depuis WSL :
  ```bash
  ss -lptn | grep -E ':2345|:2347'
  ```
  et pour tout arrêter : `pkill -f launcher_fast.py ; pkill -f cloudflared`.
  ⚠️ Cela met fin à la partie en cours : ouvre d'abord `http://127.0.0.1:2345` et sauvegarde depuis le plateau si tu veux la garder.
- **Une seule partie à la fois** par PC (un moteur = une partie).
- **Images des cartes** : `launch.online.json` cherche les images dans `./assets/pics/` puis, en secours, dans l'ancien dossier `Jeux original/assets/pics/` (chemin absolu) et enfin sur Internet (marvelcdb / cerebro). Si tu **supprimes `Jeux original`**, les images continuent de marcher via `./assets/pics/` et le web, mais tu peux nettoyer ce chemin devenu inutile dans `image_folders`.

---

## Jouer une CAMPAGNE à plusieurs (depuis le 12/8/2026)

Avant cette date, une campagne était **toujours** jouée depuis un seul navigateur :
seul celui qui l'avait lancée depuis l'écran des campagnes savait qu'il jouait une
campagne, et rien ne convoquait les autres. C'est réglé.

### Comment ça se passe

1. Tu lances `JOUER-EN-MULTI.bat` comme d'habitude, et tu envoies leurs liens à tes amis.
2. Chaque invité ouvre son lien et arrive au salon. **En campagne, il n'a rien à
   choisir** : l'équipe a été arrêtée à la création de la campagne et le livret
   interdit d'en changer. Le salon lui dit simplement « **Tu tiens <héros>** ».
3. Toi, tu vas sur `campagne.html`, tu ouvres ta campagne et tu lances le scénario.
   Tes amis basculent tout seuls sur le plateau.
4. En fin de partie, **le panneau de récompenses s'ouvre chez tout le monde**, en
   direct. Chacun remplit ses propres cases ; celles des autres sont visibles mais
   grisées, avec la mention « à remplir par P2 ».
5. Chaque invité clique « **Envoyer mes champs** ». Toi seul as « **Valider et
   continuer la campagne** », et tu vois leurs choix arriver au fur et à mesure.
6. Tu valides, tu reviens à l'écran des campagnes et tu lances le suivant : **tes
   amis suivent tout seuls**, sans rien avoir à faire.

### Qui remplit quoi

**Une case qui nomme un joueur appartient à ce joueur ; tout le reste est à
l'hôte.** Un invité ne peut ni valider, ni terminer un scénario, ni marquer la
campagne gagnée ou perdue : ce n'est pas une question de confiance, c'est la forme
même des routes du serveur qui l'en empêche.

### Le siège N tient le N-ième héros de l'équipe

Il n'y a aucun écran de répartition : le **lien du joueur 1** donne le premier
héros de l'équipe, le **lien du joueur 2** le deuxième, et ainsi de suite, dans
l'ordre où l'équipe a été composée. Mettez-vous d'accord sur qui prend quel lien
avant de commencer.

### Limites connues

- **Ceci n'a jamais été joué en vraie soirée.** Tout est testé automatiquement
  (deux navigateurs pilotés, carnet relu), mais aucun humain n'a encore mené une
  campagne à plusieurs de bout en bout. Le salon qui dit « Tu tiens <héros> » n'a
  jamais été vu à l'écran.
- **Agents of S.H.I.E.L.D. à plusieurs** : le secret de la taupe ne sort d'aucune
  route, mais on n'a pas vérifié qu'il ne se déduit pas d'un carnet partagé lu par
  quatre personnes. À jouer en connaissance de cause.
- **L'équipe ne change pas en cours de campagne.** C'est la règle du livret. Si
  quelqu'un abandonne, il n'y a rien de prévu.

Le détail technique (les deux routes, la règle des droits, les pièges) est au §19
de `docs/CAMPAGNES.md`.

---

## Pour aller plus loin

Un vrai **serveur permanent multijoueur** (lien fixe, plusieurs tables, identité par siège, secret des mains appliqué côté serveur) est spécifié dans :
`.planning/todos/2026-07-28-serveur-permanent-multijoueur.md`.

C'est un autre chantier : le mode actuel (ce `.bat`) reste la solution simple « une soirée entre potes ».

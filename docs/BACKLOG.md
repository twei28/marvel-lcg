# Backlog

Les chantiers décidés ou envisagés, pas encore faits. Une entrée par sujet : ce qu'on veut, ce qu'on a mesuré,
les options, et ce qui reste à trancher. Quand un sujet est fait, on le raye ici et on renvoie vers son commit ou
sa documentation.

---

## 1. Un jeu « installable » sans installer 2,5 Go de cartes (ajouté le 18/10/2026)

**Le besoin.** Que les joueurs installent le jeu sans attendre le téléchargement de toutes les cartes.

**Le critère de choix, donné par l'utilisateur.** La solution qui est la plus facile pour les joueurs ET la plus
facile à mettre à jour de notre côté. C'est ce critère qui tranche, pas la puissance de la technique.

**Ce qu'on a mesuré (18/10/2026, `Fusion/marvel-lcg-src/assets/`).**

| Dossier | Poids | Fichiers |
|---|---|---|
| `pics` (scans anglais) | 981 Mo | 7 876, 125 Ko en moyenne |
| `pics-fr` (scans français) | 915 Mo | |
| `pics-hd` | 225 Mo | |
| `vignettes` (images de la table) | 433 Mo | 10 871, 39 Ko en moyenne |
| sons, textures | environ 25 Mo | |

Environ 2,5 Go d'images, le reste du jeu est léger. **Une partie n'en utilise qu'une petite part** : environ
120 cartes (deck du joueur, scénario, méchant), soit environ 5 Mo de vignettes. Les grands scans ne servent
qu'au zoom.

**Ce qui existe déjà.** Une installation « application » sur téléphone (`ui-app/src/board/mobile/installation.ts`,
manifeste et `sw-plateau.js` servis par `web_server.py`). Son service worker **ne garde rien en cache** et il ne
s'active que sur téléphone.

**Les options.**

1. **Application installable + cache des cartes à la demande.** Installation de quelques dizaines de Mo. Chaque carte
   vue est gardée, et les ~120 cartes de la partie sont préchargées au lancement (quelques secondes). Mise à jour :
   uniquement côté serveur, rien à redistribuer.
2. **Alléger les images.** JPG et PNG en WebP (souvent 30 à 50 % de moins), français seulement avec l'anglais en
   secours, haute définition à la demande. De 2,5 Go à environ 1 Go, sans perte à l'usage.
3. **Paquets à télécharger** (un héros, un scénario, une extension, ~8 Mo chacun) pour jouer hors ligne. Les archives
   actuelles de `paquets-cartes/` (3 Go, par héros) ne sont pas faites pour ça.
4. **Application de bureau complète** (moteur Python + interface), images téléchargées en arrière-plan. C'est la
   seule voie pour jouer **sans internet**. Mises à jour plus lourdes : installateur, versions, signature.

**Limite à connaître.** Le moteur de règles est en Python, côté serveur : une application installable depuis le
navigateur ne peut pas jouer hors ligne. Le lancement local (`JOUER-SOLO`) a, lui, toutes les images sur le disque.

**Réponses de l'utilisateur (18/10/2026).**
- Jouer **sans connexion** : oui, c'est un besoin.
- Le cache doit servir **aussi sur PC**, pas seulement sur téléphone : oui.
- Règle de nettoyage du cache : **pas décidée** (« je ne sais pas »). Proposition par défaut, à confirmer plus tard :
  garder les cartes des decks et scénarios déjà joués, effacer d'abord les moins récemment vues au-delà d'une taille
  maximale réglable (par exemple 1 Go).

**Conséquence : la recommandation change.** Le hors-ligne est un besoin, or le moteur de règles est en Python côté
serveur : les options 1 et 2 seules (navigateur + cache) ne suffisent plus. Il faut une **application de bureau**
(option 4) qui embarque le moteur et l'interface, avec les images en téléchargement à la demande. Les options 1 et 2
y restent utiles, comme briques :
- **Allègement des images (option 2)** : à faire quoi qu'il arrive, il réduit le téléchargement de chaque joueur.
- **Cache et préchargement à la demande (option 1)** : la même logique, dans l'application de bureau, avec un dossier de
  cartes sur le disque du joueur à la place du cache du navigateur.
- **Paquets (option 3)** : « télécharger ce héros et ce scénario pour jouer hors ligne », en plus du téléchargement
  automatique des cartes de la partie.

**Pour tenir ton critère (facile pour les joueurs, facile à mettre à jour).**
- Joueur : un seul installateur léger (le moteur et l'interface, sans les cartes), puis les cartes arrivent au fil des
  parties ; un bouton « tout télécharger » est facultatif.
- Mises à jour : une mise à jour automatique de l'application au lancement, et des images adressées par leur
  **empreinte** (nom de fichier = hash), de sorte que seules les cartes nouvelles ou modifiées se retéléchargent.

**À trancher ensuite.**
- La technique d'emballage du moteur Python avec une interface web (par exemple une fenêtre qui embarque le navigateur)
  et le programme de mise à jour : à comparer sur la taille de l'installateur, la signature et les antivirus sous
  Windows, et la facilité des mises à jour.
- Garder aussi l'accès par navigateur pour ceux qui ne veulent rien installer (le jeu en ligne actuel).
- Les systèmes visés : Windows seulement, ou aussi Mac et Linux (les lanceurs `.command` et `.sh` existent déjà).

**Pistes de départ.** Mesurer le gain d'un passage en WebP sur 100 cartes ; prototyper le téléchargement à la demande
des cartes d'une partie ; étendre `sw-plateau.js` pour la version en ligne ; évaluer l'emballage du moteur.

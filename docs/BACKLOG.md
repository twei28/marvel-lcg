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

**Recommandation provisoire, au regard du critère.** Les options 1 puis 2 : rien à installer pour le joueur,
et toute mise à jour (cartes, règles, interface) se fait côté serveur, sans que personne n'ait rien à retélécharger
hors les cartes nouvelles. L'option 4 est la plus lourde à tenir à jour ; elle n'a de sens que si le hors-ligne
devient un vrai besoin.

**À trancher avant de commencer.**
- Les joueurs ont-ils besoin de jouer **sans connexion**, ou seulement de lancer vite le jeu et de ne pas retélécharger
  les cartes ? (Décide entre l'option 1 et l'option 4.)
- Le cache doit-il aussi servir sur PC, ou seulement sur téléphone comme aujourd'hui ?
- Une règle de nettoyage du cache (taille maximale, cartes les moins vues d'abord) ?

**Pistes de départ.** Étendre `sw-plateau.js` (cache d'images par version, ETag), précharger la liste de cartes de la
partie au lancement, mesurer le gain d'un passage en WebP sur 100 cartes avant de convertir le tout.

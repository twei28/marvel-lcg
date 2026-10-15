# Restaurer le projet après une perte (15/10/2026)

Trois endroits portent le projet. Aucun ne suffit seul.

| Quoi | Où | Comment le récupérer |
|---|---|---|
| Code, données, scripts de cartes, docs (10 700 fichiers) | GitHub, dépôt **privé** `twei28/marvel-lcg` | `git clone` |
| Images du jeu (pics, pics-fr, pics-hd, vignettes, sons, docs, ~2,5 Go) | Serveur, servies par le site | `https://narwhalchampions.com/admin/images` (admin) |
| Ce qui n'existait que sur le poste : `paquets-cartes/`, `medias/`, `A créer/`, `captures/`, images jamais déployées | Serveur, `/var/backups/narwhal/poste/` | `rsync` par SSH (clé `cle_narwhal`) |

À garder **hors du dépôt**, sur la clé USB : `deploiement/cle_narwhal`
(clé SSH du serveur). Sans elle, ni le déploiement ni le troisième étage ne
marchent.

## En une commande

```
export NC_SESSION=<valeur du cookie nc_session, navigateur connecté en admin>
export CLE_SSH=/chemin/vers/cle_narwhal
bash outils/restaurer.sh "Marvel LCG"
```

Le script (`outils/restaurer.sh`) clone le code, télécharge les images,
rapatrie le reste, puis compte les fichiers. Chaque étage se saute si sa
variable manque. Il n'efface rien.

Si le dépôt n'est pas encore là, récupérer le script seul :
`gh repo clone twei28/marvel-lcg` puis `bash "Marvel LCG/outils/restaurer.sh"`.
Pour GitHub : `gh auth login` (installer `gh`, ou télécharger le binaire sur
github.com/cli/cli/releases).

## Ce qui n'est PAS sauvegardé

- Les zips de Google Drive (Kajislav, Conan, TMNT…) et les vidéos/captures
  de la racine : ils se retéléchargent depuis Drive.
- `site/narwhal.db`, `site/comptes.json`, `site/rapports/` : sauvegardés la
  nuit sur le serveur (`/var/backups/narwhal/comptes-*.tar.gz`, 30 jours) et
  rapatriés dans `sauvegardes-serveur/` à chaque déploiement.
- Les branches locales `deploiement-*` et autres : seules `master` et
  `sauvegarde-cle-usb-2026-10-14` sont sur GitHub.

## Points d'attention

- `deployer-tout.sh` **efface sur le serveur les images disparues en local**.
  Après une perte du poste, restaurer les images AVANT de redéployer, sinon le
  serveur perd les siennes.
- Le serveur reste un miroir du poste, pas une sauvegarde indépendante :
  `poste/` sert à ça pour ce qui n'est pas déployé.
- Pousser régulièrement : `git push` (les identifiants passent par `gh`).

## Fichiers qui n'existaient que sur le serveur (15/10/2026)

322 fichiers (`pics-hd`, `vignettes`, `cache`, quelques `pics`/`textures`) sont
copiés dans `sauvegardes-serveur/serveur-seulement-2026-10-15/` (ignoré par
git). Ce sont probablement des restes de renommages : à trier avant de les
remettre dans `assets/`.

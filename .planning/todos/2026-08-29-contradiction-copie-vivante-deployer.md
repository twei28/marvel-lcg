# TODO — Contradiction non résolue : quelle copie alimente vraiment le dev/tests

> **Mise à jour du 07/10/2026 (audit du backlog)** : RÉSOLUE : la copie WSL a été supprimée le 31/08 ; `deployer.sh` ne la cite plus qu'en commentaire ; le bandeau de `serveur-dev.py` est traité (`d0ec2e5e`).

> ⚠ **PÉRIMÉE, relevée le 16/09/2026.** La question posée ici a été tranchée
> le 31/08/2026 : la copie WSL a été SUPPRIMÉE lors du grand rangement.
> `ui-app/deployer.sh` ne déclare plus qu'une seule installation dans `JEUX`
> (le dossier Windows), et son commentaire raconte le correctif ainsi que le
> jour où le sens inversé du rsync avait effacé des biographies de héros.
> Il reste à vérifier le point 3 de la fiche (le bandeau périmé en tête de
> `serveur-dev.py`) ; le reste n'a plus d'objet.

**Statut :** ⚠️ Ouvert, laissé volontairement en l'état sur demande explicite
(29/08/2026, session de refonte de la doc de création de contenu).
**Origine :** trouvé en corrigeant `docs/reference/GUIDE-CREATION-CONTENU.md`
§1 (correctif du 29/08 : la copie vivante est `Fusion/marvel-lcg-src`
Windows, `~/marvel-work/fusion/marvel-lcg-src` est un vestige figé au
14/08/2026).

## Le problème

Deux fichiers actifs du projet affirment l'inverse du correctif §1, avec
leur propre justification :

- `ui-app/deployer.sh` (commentaire, lignes 16-22 et 151-160) : dit
  explicitement que le brief qui déclare `Fusion/marvel-lcg-src` périmée est
  faux, et déploie/synchronise activement vers **les deux** copies,
  y compris un `rsync --delete` depuis `~/marvel-work/fusion/marvel-lcg-src`
  vers les deux copies pour `public/js` et `public/css`.
- `ui-check/scripts/serveur-dev.py` (docstring, lignes 1-29) : dit que
  `Fusion/marvel-lcg-src` (Windows) est *« un codebase de DISTRIBUTION,
  périmé »*, et que `~/marvel-work/fusion/marvel-lcg-src` est *« le codebase
  de TRAVAIL, le seul que `ui-app/deployer.sh` alimente et que les plans
  modifient »*.

## Ce qui a été vérifié factuellement le 29/08/2026 (~17h30)

- `~/marvel-work/fusion/marvel-lcg-src/data/cards.json` est réellement daté
  du **14 août 10:31**, comme l'annonce le correctif.
- Le seul processus moteur en cours (`launcher_fast.py`, PID observé au
  moment du contrôle) tourne depuis
  `/mnt/c/.../Jeu Marvel Champions/Fusion/marvel-lcg-src/.game`, donc la
  copie **Windows**, pas WSL. Il utilise l'interpréteur
  `~/marvel-work/python/bin/python3.10`, mais pas le code de
  `~/marvel-work/fusion/marvel-lcg-src`.
- Rien n'écoute sur le port 2346 au moment du contrôle.
- Les deux `launch.json` (Windows et WSL) pointent par défaut sur le port
  **2345**, pas 2346. Le port 2346 (`ui-check/playwright.config.ts`,
  `UI_CHECK_BASE`) n'est qu'un second port de secours quand 2345 est pris par
  une partie multijoueur (`ui-check/scripts/serveur-dev.py`) : rien dans sa
  config ne le lie exclusivement à la copie WSL.

Ces faits penchent vers le correctif (WSL mort), mais ne prouvent pas que
`deployer.sh`/`serveur-dev.py` n'ont plus jamais été utilisés récemment de la
façon qu'ils décrivent — seulement qu'au moment du contrôle, rien ne
confirmait leur scénario.

## Ce qui n'a PAS été touché, et pourquoi

Sur question explicite (« tu utilises encore ce workflow WSL → Windows ? »),
la réponse a été « je ne sais plus, laisse tout tel quel ». Donc :
- `docs/reference/GUIDE-CREATION-CONTENU.md` §1 reste tel qu'il est
  aujourd'hui (version correctif du 29/08).
- `ui-app/deployer.sh` n'a pas été modifié : il continue de traiter les deux
  copies comme vivantes et de faire un `rsync --delete` depuis WSL.
- `ui-check/scripts/serveur-dev.py` n'a pas été modifié.

**Danger concret si `deployer.sh` tourne pendant que le correctif §1 est
vrai** : `rsync -a --delete --exclude 'app/' "$REFERENCE/public/$dossier/" "$jeu/public/$dossier/"`
(lignes 166-172) écraserait `public/js` et `public/css` de la copie Windows
avec la version figée au 14/08 de la copie WSL, dossier par dossier, avec
suppression des fichiers absents côté source.

## Pour trancher la prochaine fois

1. Lancer `bash ui-app/deployer.sh` une fois en observant ce qu'il modifie
   réellement côté Windows (`git status` avant/après sur
   `Fusion/marvel-lcg-src/public/`), ou le lire en détail avec un `--dry-run`
   ajouté à la main sur les deux `rsync`.
2. Si la copie WSL est bien morte : retirer
   `"$HOME/marvel-work/fusion/marvel-lcg-src"` du tableau `JEUX` de
   `deployer.sh` (ligne 25) et de `REFERENCE` (ligne 160), et ajouter un
   bandeau périmé en tête de `serveur-dev.py`.
3. Si elle sert encore : nuancer le §1 du guide (peut-être : Windows = ce
   que joue l'utilisateur final, WSL = environnement de dev/tests actif) au
   lieu de la qualifier de vestige à ne jamais toucher.

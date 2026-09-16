# Les données des joueurs, écrasées par le déploiement et jamais sauvegardées

Trouvé le 16/09/2026 en répondant à une question de l'utilisateur : « les
résultats des parties des joueurs, c'est bien sur le serveur que c'est gardé,
pas dans leur cache internet ? ». Réponse : oui, et c'était pire que ça.

## Trois défauts, tous mesurés sur le serveur

### 1. Le déploiement écrasait les fichiers des joueurs

`deploiement/deployer.ps1` excluait `decks`, `campagnes`, `statistiques` et
`achievements` de son archive. **Aucun de ces quatre motifs ne correspond à un
nom réel** : les fichiers s'appellent `deck/serveur-N/`, `campagnes-serveur-N/`,
`statistics-serveur-N.json` (en anglais) et `achievements-serveur-N.json`.

Les exclusions ne s'appliquaient donc à rien, et l'archive emportait les
fichiers LOCAUX du même nom, qui s'extrayaient par-dessus ceux du serveur.

**Constat, pas déduction.** Le 16/09/2026 sur le serveur :

```
-rw-rw-rw- 1 narwhal narwhal 1466 Sep 15 21:12 games_history-serveur-4.json
-rw-rw-rw- 1 narwhal narwhal  326 Sep 15 21:12 achievements-serveur-4.json
-rw-rw-rw- 1 narwhal narwhal 2610 Sep 15 21:12 campagnes-serveur-4/L_Av_nement_de_Cr_ne_Rouge.json
```

21:12 UTC, c'est 23h12 à Bruxelles : l'heure exacte du déploiement de la
veille. Les tailles sont celles des fichiers locaux, et le contenu est celui
de parties de test du 07/08 (Ebony Maw, Steve Rogers). Les droits `rw-rw-rw-`
trahissent une origine Windows, là où les fichiers du moteur sont en
`rw-r--r--`.

⚠ **La place 4 est le compte `lightningmantis`** (dernière connexion le
08/09/2026). Son historique de parties, ses hauts faits et sa campagne portent
désormais mes données de test. **C'est irrécupérable** : voir le défaut 2.

Les autres places sont indemnes, faute de fichiers locaux à leur nom.

**Corrigé** : les exclusions visent la marque de place (`*-serveur-*` et
`*/serveur-*`), jamais un dossier commun. Prouvé sur une arborescence d'essai
reproduisant les noms sensibles : les 11 fichiers de joueur sont exclus,
`deck/custom`, `deck/starter`, `launcher-serveur.sh`, `tools/config_serveur.py`
et `data/campagnes` passent.

### 2. Rien de ce que les joueurs débloquent n'était sauvegardé

`deploiement/sauvegarde.sh` prend les decks, campagnes, replays, hauts faits,
historique et statistiques **depuis le 06/09/2026**. Mais le script INSTALLÉ
sur le serveur était resté à la version d'avant :

```
grep -c "games_history-serveur" /usr/local/bin/narwhal-sauvegarde  ->  0
```

Les archives de nuit contenaient 11 fichiers, tous sous `site/`, et zéro
fichier `serveur-`. Quatre-vingt-dix jours de parties, campagnes et hauts
faits sans le moindre filet.

**La cause est un trou de process** : `deployer.ps1` n'envoie pas les scripts
d'exploitation. Seul `installer-serveur.ps1` le fait, et il n'est lancé qu'une
fois, à l'installation. Toute amélioration apportée à `sauvegarde.sh` ou
`purge.sh` depuis reste sur le poste.

**Corrigé le jour même** : script réinstallé, sauvegarde lancée, vérifiée par
restauration. 70 fichiers au lieu de 11 (5 campagnes, 31 replays, 8 fichiers de
hauts faits, 2 fiches Legacy, 10 comptes dans la base restaurée).

### 3. Deux dépendances manquantes, découvertes en le faisant

- **`legacy-serveur-*.json` n'était dans aucune liste.** Le mode Legacy est
  arrivé le 13/09, `sauvegarde.sh` datait du 06/09. Ce que le joueur a
  débloqué (vague atteinte, jetons dépensés, date de départ) n'était pas
  sauvegardé, et ne se reconstruit PAS depuis l'historique : celui-ci dit les
  parties, pas les jetons. Ajouté, à la sauvegarde et au compteur
  `--verifier`.
- **Le binaire `sqlite3` n'est pas installé sur le serveur.** La version du
  06/09 l'appelait pour `.backup` ; elle serait morte sur
  `sqlite3: command not found` sans rien produire, et le timer ne lit pas le
  code de sortie. `install-serveur.sh` l'ajoute bien à sa liste de paquets,
  mais cette ligne est postérieure à l'installation du serveur.
  **Une dépendance ajoutée à l'installateur n'atteint jamais un serveur déjà
  installé.** Le script passe désormais par `Connection.backup` de Python, qui
  prend le même instantané cohérent et ne demande aucun paquet.

## Ce qui reste à faire

- ⚠ **Déployer le `deployer.ps1` corrigé AVANT tout autre déploiement**, sinon
  le prochain envoi réécrase la place 4. Le script vit sur le poste, il n'a pas
  besoin d'être déployé : il suffit de ne pas utiliser une vieille copie.
- Dire à `lightningmantis` que son historique a été perdu, ou le laisser
  repartir de zéro sans rien dire. Décision de l'utilisateur.
- `data/campagnes` (les DÉFINITIONS de campagne) n'était pas déployé non plus :
  `--exclude=campagnes` l'attrapait. Les 9 définitions du serveur sont figées
  au 07/09/2026. Identiques aujourd'hui, mais une correction future ne serait
  jamais partie. Motif ancré sur `Fusion/marvel-lcg-src/campagnes`.
- ~~**La question de fond, non tranchée** : faut-il que `deployer.ps1` envoie
  aussi les scripts d'exploitation ?~~ ✅ **Tranchée et faite le 16/09/2026.**

  Une étape « Scripts et configuration du serveur » compare huit fichiers à
  chaque déploiement, et la mesure du jour a justifié de les traiter en **deux
  listes** :

  - **synchronisés** (entièrement issus du dépôt) : `sauvegarde.sh`,
    `purge.sh` et les quatre units de sauvegarde et de purge. Les units passent
    `systemd-analyze verify` avant d'être posées, et `daemon-reload` ne part
    que si l'une a changé.
  - **surveillés** (ils portent des réglages du serveur) :
    `/etc/systemd/system/narwhal.service` et `/etc/caddy/Caddyfile`. Le
    déploiement affiche l'écart et **n'y touche pas**.

  ⚠ **Et c'est cette distinction qui a évité la casse.** Trois fichiers avaient
  dérivé, deux dans le bon sens :
  - le Caddyfile du serveur importe deux AUTRES sites (`karaoke.caddy`,
    `publicverse.caddy`) : l'écraser les aurait coupés ;
  - `narwhal.service` porte `Environment=INSCRIPTION_LIBRE=0`, posé à la main :
    l'écraser aurait rouvert l'inscription à n'importe qui ;
  - `purge.sh`, lui, était en retard de dix jours sur le dépôt : la purge des
    rapports de bug ne tournait pas. Il a été mis à jour, et la chaîne
    `purge.sh` → `orchestrateur.py purger-rapports` est vérifiée sur le
    serveur.

## Statut

**Les trois défauts sont corrigés le 16/09/2026**, et la sauvegarde complète
est vérifiée sur le serveur. Reste la décision sur `lightningmantis` et la
question de fond ci-dessus.

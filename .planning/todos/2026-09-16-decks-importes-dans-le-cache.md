# Les decks importés vivaient dans le cache du navigateur

**Signalé par l'utilisateur, 16/09/2026** : « je suis sur le téléphone et je ne
retrouve pas les decks que j'ai importés pour certains personnages, alors que je
les ai sur PC ». Puis, sur le fond : « c'est n'importe quoi le fait que ce soit
dans le cache ».

## Ce que c'était

`prefs.savedDecks` (`public/js/prepare/prefs.js`), c'est-à-dire le
**`localStorage`** du navigateur, sous la clé `mc_prepare_prefs_v1`. Le
commentaire du fichier l'écrivait sans détour : « Decks importés/sauvegardés
**localement** (marvelcdb, etc.) ».

Vérifié côté serveur le jour même : `deck/serveur-1/` était **vide et daté du
5 septembre**. Aucun deck importé n'était jamais monté.

⚠ **Le téléphone n'était que le symptôme visible.** Vider le cache, changer de
navigateur ou ouvrir une fenêtre privée effaçait ces decks sans un mot. C'est
une perte de données de joueur, silencieuse, qui attendait chacun.

## Ce qui existait déjà, et que personne n'avait branché

Le chemin serveur était là, **et il tournait** : l'invité qui importe un deck
depuis le salon écrit sur le serveur (`salon/app.js`, `POST /save_deck`). Seul
l'HÔTE, dans l'assistant, restait au cache.

Côté moteur, tout était en place : `POST /save_deck` écrit dans
`DECK_FOLDERS[0]`, c'est-à-dire `deck/serveur-<place>/`, le dossier propre au
compte (`tools/config_serveur.py`), et `/list_deck` + `/get_hero_json` le
relisent. `api.js` exposait même déjà `listSavedDecks` et `deck`.

## Ce qui a été livré, le 16/09/2026

`public/js/prepare/decks-serveur.js` (nouveau) :

- `sauverDeck(deck)` : `POST /save_deck`, nom de fichier stable
  (`mcdb-<nom nettoyé>`), pour que deux imports du même deck ne s'empilent pas ;
- `decksSauvegardesPourHeros(heroCardId)` : lit `/list_deck`, **ne garde que les
  chemins du dossier `serveur-<N>`** (la liste rend aussi `deck/starter/` et le
  commun `deck/custom/`, qui ne sont pas des decks du joueur), charge chacun par
  `/get_hero_json`, filtre par héros ;
- **une migration une fois pour toutes** : les decks restés dans le cache
  montent tout seuls au premier affichage, sans que le joueur ait à les
  réimporter. Le cache n'est PAS vidé derrière : une remontée à moitié réussie
  laisserait un trou invisible.

`app.js` : l'import et la liste passent par ce module. Le `localStorage` ne sert
plus que de **filet** quand le serveur ne répond pas (le deck reste à l'écran,
et l'écran le dit : « Deck gardé sur cet appareil seulement »), au lieu d'être
le seul endroit où le deck existe.

## Les preuves

`ui-check/tests/decks-sur-le-serveur.spec.ts`, 6 cas (`npm run decks-serveur`) :
l'envoi au serveur, le repli hors ligne qui ne perd rien, le filtre du dossier
du joueur, le filtre par héros, la migration du cache, et le fait qu'elle **ne
se rejoue pas** (sinon chaque ouverture renverrait toute la liste).

Vérifié par mutation : en retirant le filtre du dossier, seul le cas
« seuls les decks du dossier du joueur » rougit, les cinq autres restent verts.

## Ce qui n'est PAS fait

- **Pas de suppression** : le moteur n'expose aucune route pour effacer un deck.
  Un deck importé par erreur reste dans la liste. À cadrer.
- Les decks déjà rangés dans le cache d'un joueur ne montent qu'à sa **prochaine
  visite** sur l'écran des decks. Personne ne peut les remonter à sa place.
- Le reste de `prefs.js` (favoris, arts, variantes, dernier deck joué) reste
  volontairement par appareil : ce sont des préférences, pas des données.

## Statut

**Traité le 16/09/2026.** Non déployé au moment où cette fiche est écrite.

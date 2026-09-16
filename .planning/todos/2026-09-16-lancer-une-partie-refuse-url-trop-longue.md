# Lancer une partie était refusé quand l'URL dépassait 8190 octets

**Trouvé le 16/09/2026** en cherchant si un joueur jouait vraiment ou était
seulement connecté. Sa table répondait, il était sur l'écran des héros, et
lancer une partie ne faisait **rien du tout**.

## Ce que disait son journal

```
aiohttp.http_exceptions.LineTooLong: 400, message:
  Got more than 8190 bytes when reading: b'/new?data=%7B%22campaign_json%22...'
```

Le lancement passe par `GET /new?data=<descripteur>` : l'URL porte le
**scénario entier** et le **deck de chaque joueur**. aiohttp plafonne la ligne
de requête à 8190 octets par défaut et rend un HTTP 400, que rien ne montre au
joueur. Il voit un bouton qui ne fait rien.

⚠ **Ce n'était pas un cas extrême.** Mesuré sur le dépôt le même jour, une fois
encodé dans l'URL :

| | Taille encodée |
|---|---|
| Le plus gros deck de départ (`night_thrasher`) | **7861 octets à lui seul** |
| Le plus gros scénario | 2476 octets |
| Une table à quatre joueurs, pire cas | **~34 000 octets** |

Une partie **ordinaire à un seul joueur** franchissait donc la limite. Le
plafond de 8190 était sous la taille d'un seul deck.

## Le correctif

`src/engine/network/web_server.py` : `MAX_LIGNE_REQUETE = 128 * 1024`, passé au
runner en `max_line_size` **et** `max_field_size`. Le CORPS des requêtes garde
son plafond de 8 Mio (`client_max_size`), inchangé.

128 Kio laissent passer le pire cas mesuré avec une marge confortable, sans
rapport avec le corps des requêtes, qui est l'endroit où une limite protège
vraiment.

## La gate

`tools/test_requete_longue.py`, 5 cas : la constante existe et est généreuse,
elle est **passée au runner** (une constante déclarée et jamais utilisée aurait
l'air d'un correctif sans en être un), une requête de 34 000 octets est
**refusée sans le réglage** — c'est le défaut reproduit — et passe avec, et
100 000 octets passent encore.

Le cas « refusée sans le réglage » est ce qui fait de ce fichier une preuve et
non une formalité : il montre le défaut, puis sa disparition.

## Ce qui reste, et c'est le fond du problème

**Le descripteur n'a rien à faire dans une URL.** Il devrait partir en POST,
dans le corps, qui est déjà taillé pour (8 Mio). Relever la limite éloigne le
mur, il ne le supprime pas : une campagne à quatre joueurs avec de gros decks
maison finira par le retrouver. Le contrat `/new?data=` est repris tel quel de
l'ancien `scene.html` (l'en-tête de `launcher.js` le dit), donc le changer
demande de toucher les deux côtés. À cadrer.

⚠ **Et le joueur ne voit toujours rien quand le lancement échoue.** Le 400 part
au navigateur, l'assistant n'en fait rien. C'est ce silence qui a transformé un
défaut en énigme : la table répondait, le bouton semblait mort. À traiter avec
le silence du démarrage des tables, même famille.

## Statut

**Corrigé le 16/09/2026.** Le correctif est dans le MOTEUR : il ne prend effet
qu'à l'ouverture d'une table NEUVE, chaque table compilant son code au
lancement.

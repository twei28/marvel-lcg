# L'onglet d'une table fermée sonde dans le vide, sans rien dire

**Constaté le 16/09/2026**, sur l'écran de l'utilisateur lui-même, pendant la
vérification d'avant-déploiement (« c'est qui en ligne ? »).

## Ce qu'on a mesuré

Sa table avait été fermée à sa demande. Son onglet `p1/prepare.html` est resté
ouvert et a continué de demander `/get_choix_sieges` **toutes les deux
secondes** : plus aucun processus derrière le port, Caddy rend un **502**, et
l'écran n'en montrait rien.

Relevé dans les journaux de Caddy : **525 requêtes en quinze minutes, 100 %
en erreur**, pour un écran que son propriétaire croyait encore vivant.

## La cause, en une ligne

`sonderSalon` (`public/js/prepare/app.js`) avalait tout :

```js
} catch (e) {
    return;  // serveur momentanement injoignable : on reessaiera
}
```

⚠ Et **un 502 n'est même pas une exception** : `fetch` le rend comme une
réponse normale. C'est `res.json()` qui trébuchait ensuite sur la page
d'erreur HTML de Caddy — donc le silence venait d'un `catch` qui n'était même
pas écrit pour ce cas-là.

## Ce qui a été livré, le 16/09/2026

Décision de l'utilisateur, posée en question avant d'écrire : **bandeau +
bouton, et on arrête de marteler.**

- `public/js/prepare/table-fermee.js` (nouveau) : le bandeau, sur le modèle
  d'`annonce.js` — posé sur `document.body`, hors du cycle de rendu du wizard.
  Bilingue (`dico-en.js`). Son bouton renvoie au **domaine parent**, seul
  capable de rouvrir une place.
- `app.js` : le sondage juge `res.ok` au lieu de tout avaler, retient l'instant
  du premier échec, et deux fonctions **pures** portent les décisions —
  `tableFermee({premierEchec, maintenant})` et `cadenceSondage` qui connaît un
  troisième état.
- **Le délai est de 30 s, et c'est le point délicat** : un déploiement coupe
  les tables une dizaine de secondes. Crier « table fermée » à la première
  erreur ferait mentir le bandeau à chaque mise à jour du site, et un bandeau
  qui ment n'est plus jamais cru.
- Déclarée fermée, la table est **encore sondée, mais toutes les 30 s** : le
  site peut redémarrer, et le bandeau doit alors s'effacer tout seul. C'est un
  ralentissement (15× moins de requêtes), pas un arrêt.

## Les preuves

`ui-check/tests/sondage-salon.spec.ts`, 9 cas (`npm run sondage-salon`) : les
règles pures, **et deux cas de bout en bout** qui montent le vrai écran, lui
servent de vrais 502, et regardent ce que le joueur voit — une règle verte ne
prouve aucun affichage (leçon du 15/09 sur `board.tsx`).

Vérifiés par mutation : en remettant l'ancien `catch` muet, les deux cas de
bout en bout rougissent, les sept autres restent verts. C'est exactement la
répartition attendue.

## Ce qui n'est PAS fait

- **Le plateau** (`ui-app/`) n'a pas été regardé. Il a son propre transport
  (socket, `moteur.ts`) et une reconnexion à lui : le défaut y est peut-être
  déjà couvert, peut-être pas. À mesurer avant d'y toucher, pas à supposer.
- Le cas n'a pas été rejoué à la main dans un navigateur sur une vraie table
  fermée : la preuve est celle des tests.

## Statut

**Traité le 16/09/2026.**

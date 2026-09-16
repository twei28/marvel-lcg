# Tenir plus de joueurs : ce qui a été mesuré, et ce qui a été écarté

Question de l'utilisateur, 16/09/2026 : « si j'enlève la limite de 20 places,
je pourrai avoir combien de joueurs en même temps ? », puis « comment passer à
100 sans payer plus ? ».

## Les mesures, toutes prises le jour même

| Quoi | Valeur |
|---|---|
| Machine | CX23 : 2 vCPU, 3,8 Go, **aucun swap**, 28 Go libres sur le disque |
| Une table au repos | **221 Mo** (moteur 195 Mo + ses processus) |
| Tables simultanées tenables | **~14 au grand maximum**, 10 à 12 confortablement |
| `PLACES_MAX` | 20, mais c'est un nombre de COMPTES, pas de parties simultanées |

⚠ **La mesure des 221 Mo est prise SANS partie lancée.** C'est un plancher, pas
une moyenne : le cache d'images d'une partie en cours n'est pas compté.

## Le vrai goulot n'était pas la mémoire

Relevé sur les journaux de Caddy, 3,2 heures : **`/get_choix_sieges` pesait
5917 requêtes, soit 61 % de tout le trafic vers les tables**, à raison d'une
toutes les deux secondes et par client. Y compris en solo, y compris onglet
caché, y compris quand rien ne bouge. À cent joueurs, cinquante requêtes par
seconde, chacune réveillant un processus Python.

Et ces appels **empêchaient les tables de s'éteindre** : le faucheur juge
l'inactivité sur la date du journal du moteur, que chaque requête fait vivre.

Corrigé le jour même (sondage adaptatif : rien si l'onglet est caché, 2 s en
attente dans un salon, 15 s sinon).

## Ce qui a été écarté, et pourquoi

**Rendre le moteur multi-parties** : ÉCARTÉ par l'utilisateur le 16/09/2026.

Le chiffrage, pour mémoire :

- **204 000 lignes de cartes n'auraient PAS à bouger** : les 5590 cartes
  n'utilisent aucune globale, elles reçoivent `effect` en paramètre. Vérifié :
  zéro fichier de `src/cards` ne cite `Engine.game` ni `Engine.statistics`.
- Le cœur à reprendre : 66 000 lignes (`src/engine` + `src/game`), 64 accès
  globaux, **126 variables de configuration** dont une dizaine sont propres à
  chaque place, plus toute la couche web (un serveur = une partie aujourd'hui).
- Durée estimée : **deux à trois mois** à temps plein.
- ⚠ **Le risque n'est pas le temps, c'est la fuite entre parties.** L'isolation
  par processus donne aujourd'hui gratuitement une garantie forte : une partie
  ne peut pas en voir une autre, le système d'exploitation l'en empêche. Un
  correctif du 15/09 (« la main d'un joueur ne sort plus du moteur ») montre
  que ce genre de défaut existe même AVEC cette isolation.
- En face : ~480 €/an pour une machine à 32 Go, qui tiendrait ~145 tables.

## Ce qui reste possible, gratuitement

1. ✅ **Fait** : le sondage du salon, divisé par ~15.
2. ✅ **Fait** : `.site` exclu du déploiement, pour que le faucheur cesse d'être
   aveugle après chaque mise à jour.
3. **Du swap** (4 à 8 Go) : 28 Go libres sur le disque, et les pages d'une table
   inactive sont froides. C'est surtout un filet contre le tueur de mémoire,
   qui aujourd'hui frapperait au hasard.
4. **zram** : comprimer la mémoire plutôt que de l'écrire. Les objets Python se
   compriment bien.
5. **Baisser `INACTIVITE_MINUTES`** de 45 à 15 ou 20.
6. **Fermer une table dont plus aucun client ne tient la WebSocket**, sans
   attendre le seuil d'inactivité.
7. **Redimensionner à la demande** : Hetzner facture à l'heure et sait agrandir
   une machine existante, le temps d'une soirée chargée.

## Statut

**Cadré et mesuré le 16/09/2026.** La refonte multi-parties est ÉCARTÉE.
Les points 1 et 2 sont faits. Les points 3 à 7 restent disponibles, aucun n'est
engagé.

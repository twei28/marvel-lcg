# Backlog 22 (tenir plus de joueurs) : questions en attente, 20/10/2026

Contexte : `.planning/todos/2026-09-16-tenir-plus-de-joueurs.md`, section « Backlog 22, 20/10/2026 ».
Deux gains EXACTS sont faits (sorties identiques octet pour octet, voir la fiche). Les pistes
ci-dessous n'ont PAS été faites : soit elles changent ce que reçoit le plateau, soit leur
invalidation de cache n'est pas sûre. Une question par piste, à trancher une à la fois.

Chiffres de référence (banc `outils/banc-descripteur.py`, temps CPU, après les deux gains faits) :

| Par rendu (une trame) | Solo (Spider-Man / Rhino) | Deux héros (Iron Man + Black Panther / Rhino) |
|---|---|---|
| Construction du descripteur (`ToDescriptor.World`) | ~9 ms | ~15 ms (fin de partie) |
| Enregistrement « Revoir sa partie » (conversion en dictionnaire) | ~1 ms | ~1,7 ms |
| `/get_world`, PAR CLIENT : masque | ~1,5 ms | ~2 ms |
| `/get_world`, PAR CLIENT : JSON | ~0,7 ms | ~0,8 ms |
| `/get_world`, PAR CLIENT : gzip niveau 9 | ~3,3 ms | ~6,2 ms |

Part des piles dans la construction (solo, 1097 rendus) : paquet rencontre 28 %, paquet joueur 19 %,
défausse joueur 13 %, défausse rencontre 10 %, cartes mises de côté 6 %, tout le reste (cartes en
jeu, main, zones) 24 %.

---

## Q1. Piste 1 : ne publier que le DÉCOMPTE des piles cachées (paquet joueur, paquet rencontre)

Constat : le plateau LIT le contenu de ces piles (`ui-app/src/board.tsx:596` « Chercher dans le
paquet rencontre », `board.tsx:700` cartes regardées dans une pile, `board/zones.ts:864`,
`board/HistoriquePartie.tsx:221`, `board/rapport-bug.ts:354`). Le descripteur changerait donc, et le
plateau avec : ce n'est pas une optimisation invisible.

- **A. Ne pas le faire** (recommandé tant que Q4 n'est pas tranchée). Risque nul, gain nul.
- **B. Publier les cartes de ces piles en version allégée quand PERSONNE ne les voit**
  (`visible_for_players` vide) : identifiant d'objet, dos, zone, sans `info`, `traits`, `buffs`,
  `effects`… Le plateau dessine déjà un dos pour elles. Gain estimé : jusqu'à ~45 % de la
  construction, soit ~10 à 15 % du CPU d'une table. Risque : MOYEN — `Card.Render` a un effet de bord
  (`GetRenderInfo` recalcule `face.crc`), à conserver ; contrat du descripteur modifié pour le
  siège partagé, le spectateur et « Revoir sa partie », qui voyaient ces champs ; passage par le
  plateau obligatoire.
- **C. Décompte seul** (la piste telle qu'écrite en septembre). Gain : le même que B, un peu plus.
  Risque : ÉLEVÉ — fonctions du plateau à réécrire (recherche dans le paquet, cartes regardées,
  historique, rapport de bug), et touche à `ui-app`.

## Q2. Piste 2 : compteur de version par pile, descripteur de pile réutilisé s'il n'a pas bougé

Constat : le descripteur d'une carte change SANS qu'elle change de pile. Relevé dans `Card.Render`
(`game/card/card.py:871`) : `visible_for_players` (un effet « regarder le dessus du paquet »),
`looked_at_by`, `is_new` (statistiques), `effects` et `resources` (capacités utilisables depuis une
défausse), `traits`, `buffs`, `bonus` (effets constants), `effect_by_cards`, `is_ready`. Un compteur
incrémenté sur les seuls déplacements raterait tous ces cas : l'invalidation n'est pas sûre.

- **A. Ne pas le faire** (recommandé). Risque nul.
- **B. Le faire sur les deux piles cachées seulement, avec un « double calcul » en test** (le banc
  recalcule tout et compare à chaque rendu, comme l'empreinte d'aujourd'hui). Gain estimé : ~40 % de
  la construction, ~10 % du CPU d'une table. Risque : MOYEN — un oubli d'invalidation montre une
  carte périmée, et seul le banc le verrait.
- **C. Le faire sur toutes les piles.** Gain : jusqu'à ~75 % de la construction. Risque : ÉLEVÉ.

## Q3. Piste 3 : cache par carte

- **A. Ne pas le faire** (recommandé). L'état d'une carte dépend de trop de choses (voir Q2), et
  le rendu a un effet de bord (`face.crc`).
- **B. Le faire**, avec une clé d'invalidation à construire. Gain : le plus grand des trois.
  Risque : ÉLEVÉ.

## Q4. Compression de `/get_world` : gzip niveau 9 (aujourd'hui) contre 6 ou 1

Après les deux gains faits, la COMPRESSION est la plus grosse part du coût PAR CLIENT. Le contenu
reçu par le plateau (le JSON une fois décompressé) reste identique octet pour octet ; seuls les
octets compressés sur le fil changent. Mesure solo, par client et par trame :

| Niveau | Temps de compression | Taille moyenne |
|---|---|---|
| 9 (aujourd'hui, défaut de `gzip.compress`) | ~3,3 ms | 3,9 Ko |
| 6 | ~1,1 ms | 4,1 Ko (+5 %) |
| 1 | ~0,5 ms | non mesurée finement, plus grosse |

- **A. Garder 9.** Gain nul.
- **B. Passer à 6** (recommandé) : ~2 ms gagnées par client et par trame, soit ~30 à 40 % du coût
  par client restant. Risque : FAIBLE (+5 % de données, ~4 Ko par trame).
- **C. Passer à 1.** Un peu plus de temps gagné, des trames nettement plus lourdes.

## Q5. Mettre en cache la réponse de `/get_world` par (trame, sièges visibles)

Chaque client relit le monde à chaque trame. Deux clients qui ont les mêmes droits (spectateurs,
siège partagé : `sieges_visibles` rend `None` pour tous) recevraient la même réponse, calculée une
seule fois. Pour des joueurs à des sièges différents, le gain est nul (le masque diffère).

- **A. Ne pas le faire.**
- **B. Le faire** : clé = identité du descripteur (remplacé à chaque rendu) + sièges visibles.
  Gain : tout le coût par client, pour chaque client au-delà du premier qui partage les mêmes
  droits ; nul pour une table de joueurs distincts. Risque : FAIBLE à MOYEN — il faut d'abord
  vérifier qu'aucune valeur du descripteur n'est une référence vivante modifiée par le moteur entre
  deux rendus. Lu le 20/10 : `GetInfoTraits`, `GetBuffsText`, `BonusParSource` et le
  `GetInfoDict` de base construisent des objets neufs à chaque appel ; les surcharges de
  `GetInfoDict` des types de carte n'ont pas toutes été relues, et rien ne le garantit pour demain.

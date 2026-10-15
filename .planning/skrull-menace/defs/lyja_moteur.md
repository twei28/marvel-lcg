# Lyja : modifications du moteur partage

Chaque ligne : fichier, quoi, pourquoi, cas qui la prouve.

| Fichier | Quoi | Pourquoi | Cas |
|---|---|---|---|
| `src/game/card/face/card_face.py` (enum `COUNTER`) | + `'revelation'` (une entree, additive) | sk056 Invisible Woman pose et lit des compteurs « revelation » ; sans l'entree, `IsCounter('revelation')` refuse le nom | `[lyja] sk056 Invisible Woman` (3 cas : compteur apres attaque, +1 consecutif a la 2e attaque, compteur apres un contre) |

Deja dans la base commune (commit `d845b442`, PAS de mon fait) : trait `TREACHERY` (enum `TRAITS`), `Event.OnWhenCardRevealed`
(un evenement joueur revele depuis le deck rencontre se defausse chez son proprietaire ; prouve par `[lyja] sk039 ... When Revealed`).

Aucune autre modification de `src/game/**` ni de `src/cards/pack/__init__.py`. Tout le reste vit dans
`src/cards/pack/skrull_menace/lyja/` et `lyja_nemesis/`.

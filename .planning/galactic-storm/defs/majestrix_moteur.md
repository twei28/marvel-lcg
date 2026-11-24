# Lot GS-5 (Majestrix's Verdict) : fichiers partagés touchés, contournements moteur

## Fichiers partagés modifiés

| Fichier | Quoi | Pourquoi | Preuve |
|---|---|---|---|
| `src/game/card/face/card_face.py` | `"STARJAMMER", "SHI'AR"` ajoutés à l'énum `TRAITS` (une ligne) | traits imprimés des cartes gs114-gs137, lus par les scripts (`HasTrait("STARJAMMER")`) | tous les cas `[mv]` qui glissent, libèrent ou détournent un STARJAMMER |
| `data/cards.json` | clé `galactic_storm` (créée si absente), 27 cartes | `defs/inserer_majestrix.py` (idempotent, rejouable après fusion) | — |
| `data/sets_info.json` | entrée `144. Custom (Galactic Storm)` créée si absente, scénario et set ajoutés | idem | — |
| `src/cards/pack/galactic_storm/__init__.py` | créé (en-tête du pack) | d'autres lots GS le créent aussi : garder un seul en-tête à la fusion | — |
| `docs/reference/mots-cles/assault.md`, `README.md`, `tuck.md` | fiche Assault créée ; trois pièges du glissement ajoutés à tuck.md | règle CLAUDE.md (mot-clé rencontré) | — |

Aucun autre fichier moteur modifié. La batterie complète n'a PAS été lancée (interdite pour ce lot) : l'ajout de
deux littéraux à l'énum `TRAITS` est sans effet sur les autres packs (énum de typage, `TRAITS_LIST`).

## Contournements écrits DANS le pack (aucun fichier moteur touché), à remonter peut-être au moteur

1. **Entrée en jeu depuis une `PlaceCardArea` sans remise à zéro** (`card.py`, « Fix 39035 ») : une carte glissée
   directement depuis la réserve du scénario n'a jamais calculé ses mots-clés (ATQ 0, Riposte 0, sans Toughness).
   Pack : `face.Reset(False)` avant `PutIntoPlay` (`MettreEnJeuSousControle`). Cas : `[mv] gs122 Retaliate 2`,
   `gs124`, `gs126`, `gs137`.
2. **`Worlds.FindCardOnField` voit les cartes glissées** (sur le terrain, hors jeu). Pack : filtre `IsInPlay()`
   (`EnJeu`). Cas : `[mv] gs137 Sister's Deception : Lilandra pas en jeu`.
3. **Retourner une manigance annexe dans son « When Defeated »** : `Scheme.OnBeDefeated` (scheme.py) défausse
   ensuite la CARTE si elle est en jeu, donc la face retournée et mise en jeu repart à la défausse. Concerne aussi,
   a priori, les officielles `32172a` Enemy of My Enemy et `40190a`-`40195a` (non mesuré). Pack : retournement
   différé à `AfterSchemeBeDefeated` (gs120a). Cas : `[mv] gs120a When Defeated`.
4. **`UnitCannotBeDefeatedWhile(condition=.., change_on_event=..)`** ne relance la défaite que tant que la
   condition « ne peut pas être vaincu » est VRAIE (`defeated.py`, `new_condition`), donc jamais quand elle tombe.
   Pack : relance écrite à part (`DeathbirdInvaincue`). Cas : `[mv] gs115 cannot be defeated : Deathbird II a 0 PV
   tombe des que Lilandra et le Trone passent sous controle`.
5. **Une carte retournée garde ses pions de menace** : 2B → 2A → 2B revenait avec ses menaces. Pack : retrait de
   toutes les menaces du stade qui recommence (gs118b, `ignore_crisis=True`). Cas : `[mv] gs118b Forced Interrupt`.
6. **`message.GetDefeatingPlayer()` affirme qu'un joueur a vaincu la manigance** : lire `message.defeating_player`.

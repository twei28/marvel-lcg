# Legion

**Texte imprimé / définition** : « Legion. (2 allies with the legion keyword
count as 1 ally toward your ally limit.) »

**Mécanisme moteur** : mot-clé maison, introduit par le pack `okoye`. Aucune
primitive « N comptent comme 1 » n'existe dans le moteur : la seule brique
disponible est `Message.CheckIfAllyCountLimit` / `message.SetNotCountAlly()`,
exposée via `AbilityFactory.ThisNotCountAllyLimit` (`friend.py`), qui marque
un allié comme NE COMPTANT JAMAIS (utilisée par `aoa/missions.py` pour un
allié qui échappe totalement à la limite).

`AllyLimit.CheckLimit` (`src/game/player/limit_monitor/ally_limit.py`) envoie
un message `CheckIfAllyCountLimit` à chaque allié en jeu du joueur et somme
ceux qui ne sont pas marqués « not_count » pour obtenir `curr_ally` ; c'est ce
total qui est comparé à `ally_limit`.

Implémentation retenue (`src/cards/pack/okoye/okoye/__init__.py`, fonction
`Legion()`) : classer les alliés portant Legion par ordre de création stable
(`card.object_id`), puis marquer **un allié sur deux** (index impair) comme
« ne comptant pas ». N alliés Legion valent alors `ceil(N/2)` au lieu de N,
ce qui correspond exactement à « 2 comptent comme 1 » (2→1, 3→2, 4→2, 5→3...).

```python
def Legion() -> 'Ability':
    def est_le_second_du_couple(effect, message) -> bool:
        joueur = effect.this.GetControlByPlayer()
        if joueur is None:
            return False
        allies_legion = sorted(
            (a for a in joueur.allies.Get() if EstAllieLegion(a)),
            key=lambda a: a.card.object_id,
        )
        if effect.this not in allies_legion:
            return False
        return allies_legion.index(effect.this) % 2 == 1

    return AbilityFactory.ThisNotCountAllyLimit(conditions=[est_le_second_du_couple])[0]
```

**Carte exemple** : `ok017` (jeton Dora Milaje) et `ok018` (jeton Midnight
Angel), les deux seuls porteurs du mot-clé dans ce pack (les deux « Created
Ally » générés par Adored Ones et Angelic Warfare).

**Pièges connus** :
- Le classement se recalcule à chaque appel (stateless), à partir des alliés
  **actuellement en jeu** du joueur — pas d'état persistant à synchroniser
  quand un allié Legion est défait ou rejoué.
- Edge case connu et non bloquant : `AllyLimit.CheckLimit` envoie aussi le
  message aux `gain_faces` (alliés sur le point d'entrer en jeu, pas encore
  dans `player.allies.Get()`). Pour un tel allié, `effect.this not in
  allies_legion` renvoie `False` tant qu'il n'est pas encore effectivement en
  jeu : il compte normalement au moment précis de la vérification d'entrée,
  avant de rejoindre la paire au recalcul suivant. N'a pas d'effet observable
  différent en pratique (la limite est de toute façon revérifiée après
  l'ajout), mais à garder en tête si un cas de test semble incohérent d'un
  point de vue « avant/après » très précis.
- Ne pas confondre avec `jetons`/`compteurs` (§8 du guide) : Legion ne pose
  aucun jeton, c'est un filtre de comptage pur.

**Variantes maison** : aucune autre carte du pack `okoye` ne porte Legion
que les deux jetons ci-dessus ; toute nouvelle carte Legion future devra
utiliser `EstAllieLegion()` (même fichier) pour rester dans le même groupe de
pairage plutôt que de créer un second groupe indépendant.

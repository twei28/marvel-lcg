# Rivalité Antique ne redressait pas l'allié Thor

**Signalé par BLStark le 17/09/2026** (rapport n° 13) : « Rivalité Antique
(carte En Equipe Hercules - Thor) ne redresse pas Thor quand il est sur le
terrain avec Hercule ».

## La carte

`59026 Ancient Rivalry` : « Team-Up (Hercules and Thor). Max 1 per deck.
**Hero Action**: Search your discard pile for an identity-specific upgrade and
add it to your hand. **Ready Hercules and Thor.** »

## La cause

```python
for name in ('Hercules', 'Thor'):
    hero = Worlds.FindCardOnField(effect, name=name, card_type=Hero)
```

`card_type=Hero` : on ne cherchait qu'un **héros** nommé Thor. En solo il n'y
en a pas, et l'allié `59020 * Thor (Odinson)` restait incliné.

⚠ **Or c'est précisément lui qui rend la carte jouable.** Le mot-clé Team-Up,
documenté dans l'en-tête de `has_teamup.py` : « a card with the team-up keyword
cannot be played unless both of the named characters (**identity or ally**) are
in play ». La carte était donc autorisée grâce à l'allié Thor, puis refusait de
le redresser. Les unités qui autorisent la carte et celles qu'elle redressait ne
venaient pas de la même liste.

## Le correctif

```python
Faces.ReadyAll(this.GetTeamUpUnits(), effect)
```

`GetTeamUpUnits()` rend exactement les unités qui satisfont la Team-Up,
identité ou allié. C'est la seule liste qui ne puisse pas diverger de la
condition de jeu : ce qui autorise la carte est ce qu'elle redresse.

Carte de référence : `al023` Little Rascals, même famille Team-Up, qui redresse
déjà parmi les personnages amis sans filtrer sur le type.

## La preuve

`tools/test_capacites.py`, cas « 59026 Ancient Rivalry — redresse l'ALLIE Thor,
pas seulement un heros ». Il exige **deux** choses : que la carte parte en
défausse (donc qu'elle ait vraiment été jouée) et que `59020` soit prêt.

| | Résultat |
|---|---|
| Ancien code (`card_type=Hero`) | ÉCHEC : « 59020 est incliné alors qu'il devrait être prêt » |
| Avec `GetTeamUpUnits()` | OK : état conforme |

L'échec reproduit mot pour mot ce que BLStark décrit.

## ⚠ Deux pièges du harnais, payés ici, à retenir

Le cas a « échoué » trois fois pour des raisons **étrangères à la carte**, et
chaque fois l'échec ressemblait à un correctif qui ne marche pas :

1. **`Puzzle.PutIntoPlay('59020')` ne suffit pas** : sans `under_control=True`
   l'allié n'appartient à personne, et `GetOnFieldFriendlyCharacters` ne le voit
   pas.
2. **La partie démarre en ALTER-EGO** : une « Hero Action » n'y est pas
   jouable. Sans `Puzzle.ChangeToFace('59001b', '59001a')`, la carte restait en
   main — et le cas mesurait le vide.

⚠ Le second piège est le plus vicieux : un attendu du genre
`{"hors_jeu": ["59026"]}` **passe** quand la carte n'a jamais quitté la main.
C'est en exigeant `{"defausse": ["59026"]}` que le vide est apparu. Un cas qui
vérifie un effet doit d'abord vérifier que la carte a été JOUÉE.

Une affirmation fausse a d'ailleurs été écrite puis retirée du script en cours
de route (« `GetTeamUpUnits()` rendait une liste vide ») : elle venait de ces
faux échecs, pas d'une mesure.

## Statut

**Corrigé le 17/09/2026.** Correctif dans le MOTEUR : il ne prend effet qu'à
l'ouverture d'une table NEUVE.

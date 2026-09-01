# À FAIRE : 5 cas rouges préexistants (squirrel_girl, scarlet_spider)

**Constatés le 31/08/2026** par la batterie complète de non-régression du
portage harry_osborn (801/829, rapport `/tmp/rapport-batterie-complete.json`).
Aucun traceback dans les journaux : ce sont des écarts de COMPORTEMENT, pas
des plantages. Ils ne touchent aucun fichier du portage du jour (l'énum
TRAITS et le harnais n'ont aucun lien avec ces mécaniques) : hors périmètre,
à traiter dans leur propre séance, carte par carte selon PROCESSUS-CARTE.

Les 28 autres rouges du même bilan (pack `jj`, jessica_jones_custom) sont
EXPLIQUÉS ET CORRIGÉS le jour même : les cas pointaient `"heros":
"jessica_jones"`, orphelins depuis que ce nom désigne l'ancienne version
set 61 (renommage `jessica_jones_custom` au moment d'iron_lad, 56884f6).
Re-vérifiés 28/28 après correction.

## Les 5 cas

| Cas | Symptôme mesuré |
|---|---|
| sg009 Squirrel Girl's Costume — un sbire vaincu appelle 1 écureuil | 0 carte SQUIRREL en jeu (attendu ≥ 1) |
| sg013 Call the Squirrels — 2 écureuils entrent en jeu PRÊTS | sg002 arrive incliné |
| sg007 The Gatherer — le dépenser soigne 1 dégât | 3 dégâts restants (soin non appliqué) |
| sg006 The Forager — le dépenser fait fouiller le dessus du deck | la branche optionnelle ne part pas |
| ~~ss012 Mark of Kaine~~ | ✅ **RÉSOLU le 01/09/2026** — voir ci-dessous |

## ✅ ss012 — RÉSOLU le 01/09/2026 : le CONTRÔLE était cassé, pas la carte

`ss012_mark_of_kaine_deferlement` relit le journal de partie pour y chercher
« gains overkill ». Elle en lisait le chemin avec **un index CODÉ EN DUR** :

```python
chemin_log = f"/tmp/capacites_{prefixe}517.log"
```

Des cas insérés avant lui ont décalé `ss012` de l'index **517 à 573**. La
fonction lisait donc le journal d'un cas sans aucun rapport (aujourd'hui un
diagnostic de Superior Iron Man), n'y trouvait évidemment pas « gains
overkill », et déclarait rouge. **La carte n'a jamais eu le moindre défaut.**

La piste notée plus bas — « un changement de format de log suffirait à le
fausser » — visait juste, mais la cause était plus simple : un index qui glisse.

**Correctif** : le dictionnaire `aides` expose désormais `index`, l'index du cas
COURANT, et la fonction lit **son propre** journal. Vérifié : `[filtre] ss012`
→ **2/2**. Plus aucun index codé en dur dans le fichier.

**Leçon** : toute vérification qui relit un journal de partie doit passer par
`aides["index"]`. Un numéro figé dans le code casse silencieusement à la
première insertion de cas.

## Pistes (non vérifiées, à confirmer en séance)

- Les quatre sg touchent des CHOIX OPTIONNELS ou des arrivées en jeu : une
  évolution du pilote du harnais (qui décline les MayChooseOneAbility) ou
  des messages d'entrée en jeu a pu casser les cas OU les modules — trancher
  par preuve, pas au jugé.
- ss012 vérifie via un GREP du journal de partie : un changement de format de
  log suffirait à le fausser sans aucune régression de jeu.
- Dater la casse : `git log` sur les modules sg/ss et sur le harnais, puis
  rejouer les cas aux commits candidats (le `[filtre]` rend ça rapide).

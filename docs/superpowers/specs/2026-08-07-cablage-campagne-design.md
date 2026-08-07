# Câbler les quatre boîtes-campagne restantes

Spec écrite le 07/08/2026. Elle prolonge
[`CAMPAGNES.md`](../../../CAMPAGNES.md) et son document de conception
[`2026-08-07-mode-campagne-design.md`](2026-08-07-mode-campagne-design.md).

## 1. Le problème

Le mode campagne fonctionne sur deux boîtes, `trors` et `sm`. Quatre autres
sont inertes : `mts` (partiellement), `mut_gen`, `next_evol`, `aoa`. Leur
module `campaign.py` est écrit et complet, mais aucune carte de manigance
principale 1A n'appelle `CampaignSetup(niveau)`. Sans cet appel,
`Message.WhenCampaignSetup` n'a aucun auditeur : le carnet entrant est ignoré,
et rien ne le signale.

## 2. Ce que la lecture du code a corrigé dans CAMPAGNES.md

Trois constats mesurés avant d'écrire cette spec, qui contredisent ou
complètent le document de reprise.

**`WriteCampaignLogAtGameOver` n'existe que dans ces quatre boîtes.**
`src/cards/pack/mts/campaign.py:78` définit une capacité qui, à
`Message.WhenGameOver`, calcule le carnet SORTANT complet : elle relève le
store du monde, y ajoute les PV restants et l'identité de chaque joueur,
applique le `Collect*` de la boîte, écrit le tout dans `campaign_log_last.json`
et le dump en texte. Les quatre boîtes l'utilisent. `trors` et `sm` ne
l'utilisent pas. Aucune route HTTP ne l'expose et `PanneauRecompenses` ne le
lit pas : ce travail du moteur est aujourd'hui perdu.

**Le niveau 1 de `next_evol` doit être câblé.** CAMPAGNES.md le présente comme
n'ajoutant « que la partie commune ». Cette partie commune contient
`PutEarnedEnvironmentsIntoPlay()`, `ShuffleChosenEncounterCards()`,
`ChooseCampaignPlayerSideScheme()` et l'écriture du carnet sortant. Sans
câblage, le scénario 1 ne produit aucun carnet et toute la campagne part vide.
Même raisonnement pour `aoa` niveau 1, dont `SetupMissionAndOverseer(1)`
choisit la mission d'ouverture.

**Les dix-huit fichiers existent et rendent tous une liste littérale.**
Vérifié fichier par fichier. Le préfixage décrit au §5 s'applique partout sans
cas particulier.

## 3. Périmètre

Dans le périmètre :

1. Câbler les 18 fichiers.
2. Étendre `tools/sonde_campagne.py` à la fin de partie.
3. Vérifier les 18 scénarios des deux côtés, entrant et sortant.
4. Exposer le carnet calculé par le moteur au plateau, en source prioritaire de
   pré-remplissage, les détecteurs restant le secours.
5. Écrire `data/campagnes/mts.json`.

Hors périmètre, et à traiter séparément : `mut_gen.json`, `next_evol.json`,
`aoa.json`, le retrait de `CAMPAIGN_SCHEMAS` dans `public/js/prepare/app.js`,
le sort de `gmw`, et les quatre suites listées au §9 de CAMPAGNES.md.

## 4. Décisions prises

| Question | Décision | Pourquoi |
|---|---|---|
| Livrable | Câblage vérifié, puis `mts.json` seul | Valider le modèle de fichier de campagne sur une boîte avant d'en produire quatre |
| Source du carnet sortant | Le moteur d'abord, les détecteurs en secours | Le moteur connaît son propre état ; redériver depuis le descripteur est le chemin qui a produit le bug des armes expérimentales |
| Preuve | Sonde étendue à la fin de partie | C'est le seul moyen de prouver la moitié sortante sans jouer 18 parties au navigateur |

## 5. Le câblage

Pour un fichier sans capacité, le corps entier devient :

```python
from . import *
from cards.pack.mts.campaign import CampaignSetup

def GetAbilities() -> Sequence['Ability']:
    return [*CampaignSetup(1)]
```

Pour un fichier qui a déjà des capacités, on ajoute l'import en tête et on
préfixe la liste rendue :

```python
from cards.pack.mut_gen.campaign import CampaignSetup
# …
    return [
        *CampaignSetup(1),
        AbilityFactory.WhenCardSetup("This", stalked_by_sabretooth_1a),
    ]
```

Le niveau est le numéro du scénario dans la campagne, de 1 à 5. Le préfixage
compte : les capacités de campagne doivent être enregistrées avant celles du
scénario, comme dans les deux fichiers `mts` déjà câblés.

### Les dix-huit fichiers

Tous sous `Fusion/marvel-lcg-src/`. Module importé
`cards.pack.<code>.campaign`, sauf `aoa` où c'est
`cards.pack.aoa.campaign_setup`.

| Boîte | Niv. | Fichier |
|---|---|---|
| `mts` | 2 | `src/cards/pack/mts/the_tower_defense/21098a.py` |
| `mts` | 4 | `src/cards/pack/mts/hela/21138a.py` |
| `mts` | 5 | `src/cards/pack/mts/loki/21165a.py` |
| `mut_gen` | 1 | `src/cards/pack/mut_gen/sabretooth/32063a.py` |
| `mut_gen` | 2 | `src/cards/pack/mut_gen/project_wideawake/32087a.py` |
| `mut_gen` | 3 | `src/cards/pack/mut_gen/master_mold/32112a.py` |
| `mut_gen` | 4 | `src/cards/pack/mut_gen/mansion_attack/32125a.py` |
| `mut_gen` | 5 | `src/cards/pack/mut_gen/magneto/32141a.py` |
| `next_evol` | 1 | `src/cards/pack/next_evol/morlock_siege/40077a.py` |
| `next_evol` | 2 | `src/cards/pack/next_evol/on_the_run/40103a.py` |
| `next_evol` | 3 | `src/cards/pack/next_evol/juggernaut/40121a.py` |
| `next_evol` | 4 | `src/cards/pack/next_evol/mister_sinister/40139a.py` |
| `next_evol` | 5 | `src/cards/pack/next_evol/stryfe/40166a.py` |
| `aoa` | 1 | `src/cards/pack/aoa/unus/45062a.py` |
| `aoa` | 2 | `src/cards/pack/aoa/four_horsemen/45085a.py` |
| `aoa` | 3 | `src/cards/pack/aoa/apocalypse/45103a.py` |
| `aoa` | 4 | `src/cards/pack/aoa/dark_beast/45121a.py` |
| `aoa` | 5 | `src/cards/pack/aoa/en_sabah_nur/45147a.py` |

`mts` niveaux 1 et 3 sont déjà câblés et ne sont pas touchés.

## 6. La sonde étendue

`tools/sonde_campagne.py` monte une partie, applique un carnet, exécute des
commandes `Puzzle` et rend le descripteur de monde. Elle répond seule aux
questions de mise en place en prenant la première option légale, ce qui suffit
aux choix introduits par `CampaignSetup` (rôle, complot annexe de campagne,
dégâts de Hope Summers).

Elle s'arrête après la mise en place. On ajoute une variable d'environnement
`FIN_DE_PARTIE` : quand elle vaut `1`, la sonde émet `Message.WhenGameOver`
après la capture du descripteur, puis relit `campaign_log_last.json` et le
range sous la clé `carnet_sortant` du rapport. Le rapport gagne donc un champ,
sans en perdre aucun : les usages existants de la sonde ne changent pas.

Le fichier est écrit dans le répertoire courant du processus, soit `.game`. La
sonde le supprime avant de déclencher la fin de partie, pour ne jamais relire
le rapport d'une exécution précédente.

## 7. Le critère de vérification

Un scénario compte comme câblé quand les deux moitiés passent, mesurées par la
sonde et pas par la lecture du code.

**Moitié entrante.** Avec un carnet pré-rempli d'une récompense de ce niveau,
la carte attendue apparaît dans une zone d'un joueur ou du monde du
descripteur. C'est le critère déjà employé pour établir le tableau de
CAMPAGNES.md.

**Moitié sortante.** `carnet_sortant` est présent, et contient les clés que le
`Collect*` de la boîte est censé produire à ce niveau. Une partie perdue par la
sonde reste acceptable : `WriteCampaignLogAtGameOver` s'exécute quel que soit
le vainqueur, et c'est `players_won` qui départage.

Chaque scénario est mesuré séparément. Aucune extrapolation d'un scénario à
l'autre au sein d'une boîte : c'est précisément ce raccourci qui avait laissé
croire `mts` entièrement câblé.

Les résultats des 18 mesures sont consignés dans un tableau, dans le message de
livraison et dans CAMPAGNES.md en remplacement du tableau du §6.

## 8. Le carnet du moteur, exposé au plateau

### Côté serveur

Une septième route dans
`src/engine/device/web/server/server_campagne.py` :

```
GET /get_carnet_suggere
```

Elle rend le contenu de `campaign_log_last.json` tel quel,
`{"players_won": …, "suggestions": {…}}`, ou `{"suggestions": {}}` si le
fichier est absent. Elle suit la forme des six routes voisines : réponse JSON,
pas d'écriture, pas d'état.

### Côté plateau

Dans `ui-app/src/board/campagne/`, une fonction de chargement à côté de
`chargerCampagne` et `chargerDefinition`. `PanneauRecompenses` l'appelle au
moment où il passe en phase `pret`, et son mémo de pré-remplissage devient,
pour chaque champ de type `auto` :

1. la valeur du moteur si la clé de carnet y figure ;
2. sinon `detecter(champ, monde, joueurId)` ;
3. sinon vide.

Les champs de type `choix` ne sont pas touchés : ils restent la décision du
joueur. La correction manuelle d'une valeur reste prioritaire sur tout
pré-remplissage, comme aujourd'hui.

`trors` et `sm` ne produisent pas de carnet moteur : leur route rendra un objet
vide et le comportement retombe exactement sur les détecteurs actuels. Les 40
tests de `detecteurs.test.ts` restent verts sans modification.

### Deux limites assumées

`campaign_log_last.json` est écrasé à chaque fin de partie et n'est pas
cloisonné par joueur. En solo, la fenêtre entre la fin de partie et l'affichage
du panneau est trop courte pour que ce soit un problème. En multijoueur, deux
parties simultanées sur le même serveur se marcheraient dessus. La limite est
notée dans CAMPAGNES.md ; la corriger demanderait de cloisonner par identifiant
de partie, ce qui sort du périmètre.

### Tests

Nouveaux tests dans `detecteurs.test.ts` ou un fichier voisin, sur des formes
mesurées à la sonde : la valeur du moteur l'emporte sur le détecteur ; le
détecteur prend le relais quand la clé manque ; un carnet moteur vide ne change
rien au comportement existant.

## 9. `data/campagnes/mts.json`

Modèle : `sm.json`, qui a `victoire_commune`. Contenu :

- `cle_extension` relevé dans `data/sets_info.json`, ordre des scénarios idem ;
- clés de victoire copiées telles quelles depuis `CollectMTS` de
  `src/cards/pack/mts/campaign.py`, jamais approximées ;
- champs de type `auto` sans `detection`, puisque le moteur les fournit ;
- résumé français, enjeu et libellés écrits pour chacun des 5 scénarios ;
- pas de scans : `public/stories/mts/` n'existe pas, l'écran affiche alors le
  résumé seul, ce qui est prévu.

`CAMPAIGN_SCHEMAS` dans `public/js/prepare/app.js` sert de point de départ pour
les libellés, mais chaque champ est vérifié contre `campaign.py` et le livret.
Ce bloc contient des erreurs avérées sur `trors` et `sm`, il n'y a aucune
raison de le croire juste sur `mts`.

## 10. Risques

**Une clé de carnet fausse ne lève aucune erreur.** Le moteur lit une valeur
vide et la récompense disparaît en silence. D'où le §7 : la sonde, jamais la
lecture seule.

**Le déploiement écrase `public/`.** `ui-app/deployer.sh` rsync depuis la copie
WSL avec `--delete`. Cette spec ne touche pas `public/js`, mais toute retouche
ultérieure doit être poussée vers WSL avant déploiement.

**Un scénario peut refuser de monter.** Certains de ces scénarios n'ont jamais
été montés en mode campagne. Un plantage à la mise en place est un défaut à
part entière : il est ouvert et traité, pas contourné en retirant l'appel.

**La sonde répond au hasard éclairé.** Prendre la première option légale peut
mener à un état atypique. Si une mesure sortante est ambiguë, on rejoue avec
`PUZZLE` pour forcer un état précis plutôt que d'interpréter.

## 11. Ordre de travail

1. Étendre la sonde et prouver l'extension sur `ebony_maw`, déjà câblé, dont on
   connaît le résultat attendu.
2. Câbler `mts`, mesurer les 3 scénarios.
3. Câbler `mut_gen`, `next_evol`, `aoa`, mesurer les 15 scénarios.
4. Route `/get_carnet_suggere`, branchement et tests du panneau.
5. `mts.json`.
6. Mettre CAMPAGNES.md à jour : tableau du §6, correction sur `next_evol`
   niveau 1, la nouvelle route, la limite multijoueur.

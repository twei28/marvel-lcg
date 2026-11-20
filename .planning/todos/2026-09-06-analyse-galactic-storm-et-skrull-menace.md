# Galactic Storm et Skrull Menace : analyse avant portage

> **MISE A JOUR 20/10/2026 : CE DOCUMENT EST PERIME SUR LE POINT CENTRAL.** Le matériel de Galactic Storm (et de Skrull Menace) n'est pas « incomplet » : les quatre archives `MC custom content by Kajislav-20261014T200011Z-1-00{1..4}.zip` contiennent les 319 cartes, les cinq scénarios, les deux héros, les modulaires et le livret 1.2. Skrull Menace est porté. Voir `docs/packs/galactic-storm/INVENTAIRE.md` et `REGLES.md`. La conclusion « sans les cartes, il n'y a rien à porter » (§2 et §6) et la recommandation « ne rien porter » sont caduques ; les §1 (doublons) et §4-5 (machinerie, difficulté) restent vrais.

Relevé du 06/09/2026, **sans écrire une ligne de code**. Les deux zips traînaient
dans `A créer` en **double exemplaire** et ne figuraient dans aucune ligne du
tableau de difficulté du plan de portage.

---

## 1. Les doublons : identiques, on peut en jeter un

| Zip | Taille | md5 de l'archive |
|---|---|---|
| `Galactic Storm-20260813…` | 427 754 454 | `f350bfb2…` |
| `Galactic Storm-20260902…` | 427 751 439 | `22a129df…` |
| `Skrull Menace-20260813…` | 338 515 153 | `a9b546de…` |
| `Skrull Menace-20260902…` | 338 519 616 | `95cde36d…` |

Les md5 **des archives** diffèrent, mais la comparaison **entrée par entrée**
(noms, tailles, CRC) donne **0 différence** dans les deux paires : même contenu,
au bit près. L'écart de quelques Ko n'est que la métadonnée d'archive d'un
ré-export Google Drive.

➡ **Garder la version de septembre, supprimer celle d'août.** Aucune perte.
Cela libère ~766 Mo.

---

## 2. ⚠ CE QUE LES ZIPS NE CONTIENNENT PAS : LES CARTES

C'est le fait décisif, et il vaut pour les deux.

| | Galactic Storm | Skrull Menace |
|---|---|---|
| Cartes annoncées par le livret | **305** (109 joueur, 24 vilain, 172 rencontre) | **375** (125 joueur, 24 vilain, 226 rencontre) |
| Images de cartes dans le zip | **13** | **26** |
| Ce que sont ces images | cartes 224-236, les alliés « campagne » | cartes 263-288, les cartes « campagne » |
| Le reste du zip | livret PDF, boîtes, une page de règles | livret PDF, boîtes, 3 pages de règles, 2 marque-pages |

Les 13 et 26 images correspondent **exactement** aux plages numérotées que les
livrets appellent *campaign-specific cards*. Tout le reste — les cinq scénarios,
les vilains, les sets de rencontre, et les **deux nouveaux héros de chaque
boîte** (Binary et Quasar ; Hulkling et Lyja) — **n'est nulle part dans le zip**.

Le livret donne les **decklists** des héros (noms et quantités, GS p21, SM p18)
mais **aucun texte de carte**. On ne peut donc pas porter ces cartes : on
connaîtrait leur nom et leur aspect, pas ce qu'elles font.

⚠ Les deux livrets renvoient à un **Google Drive de l'auteur** pour le journal de
campagne (GS p5, SM p5). C'est peut-être là que vivent les cartes. **Non
vérifié** : je ne suis pas allé chercher hors du dépôt.

---

## 3. Ce que le dépôt possède déjà : presque rien

Vérifié sur les 5933 cartes de `cards.json` :

- **Galactic Storm** : Kree Sentry, Deathbird, Tanalth, Supreme Intelligence,
  Binary, Rick Jones, Lauri-Ell → **tous absents**. « Annihilus » n'existe que
  comme sbire de `lockjaw`, « Quasar » et « Gladiator » comme alliés sans
  rapport.
- **Skrull Menace** : Super-Skrull, Paibok, Kly'bn, Queen Veranke, Empress R'Kll,
  Lyja, Jazinda, Xavin, Crusader, Skymax → **tous absents**. Seul
  « Hulkling » existe (`56029a`), mais c'est le héros **officiel**, pas celui de
  cette boîte.

Aucun set de rencontre du dépôt ne correspond (« Kree Militants », « Kree
Fanatic », « Galactic Artifacts » appartiennent à d'autres produits).

---

## 4. Ce qui, en revanche, ne coûtera rien

**La machinerie de campagne existe et est éprouvée** : 9 campagnes dans
`data/campagnes/`, une doc de référence (`docs/rapports/CAMPAGNES.md`) et
**quatre outils** dédiés (`verifier_campagnes.py`, `verifier_scenes_campagne.py`,
`test_campagne_en_cours.py`, `sonde_campagne.py`).

**Aucun mot-clé nouveau.** Les deux livrets listent leurs mots-clés : hinder,
incite, patrol, permanent, piercing, ranged, setup, stalwart, steady, team-up,
temporary, victory X, villainous, plus l'icône **amplify** et le type **player
side scheme**. **Tous** ont déjà leur fiche dans `docs/reference/mots-cles/` et
sont implémentés — amplify a même été payé sur `sn012` et `sf011`, et les
manigances annexes joueur sur `bc004`.

---

## 5. Laquelle est la plus simple, laquelle la plus dure

### Skrull Menace — la plus SIMPLE des deux

- Structure de campagne **standard** : un héros choisi pour toute la campagne,
  cinq scénarios dans l'ordre. C'est exactement la forme des 9 campagnes déjà
  faites.
- **26** cartes de campagne présentes contre 13.
- Une seule nouveauté moteur : la **« Cooperation Area »**, une zone partagée
  hors jeu où reviennent les cartes de campagne entre deux scénarios. `grep`
  sur tout `src/` : **le mot n'existe pas**. À créer, mais c'est une zone, pas
  une mécanique.

### Galactic Storm — la plus DURE

- ⚠ **Le joueur change de héros en cours de campagne** : trois héros différents
  par joueur, les instructions de campagne disant quand changer (« Unlike other
  campaigns… », p5). **Aucune des 9 campagnes du dépôt ne fait ça**, et le
  modèle de campagne suppose une identité stable.
- **13** cartes de campagne seulement.
- 305 cartes contre 375, mais c'est le seul point où elle est plus légère.

---

## 6. Recommandation

**Ne rien porter pour l'instant**, et ce n'est pas une question de difficulté :
**les cartes ne sont pas là**. Porter les 13 ou 26 cartes de campagne seules
n'aurait aucun sens — ce sont des cartes `BASIC / CAMPAIGN`, injouables hors de
leur campagne, qui référencent des scénarios et des vilains inexistants.

Trois suites possibles, à trancher :

1. **Aller chercher les cartes** sur le Google Drive de l'auteur, cité dans les
   deux livrets. Si les 305 / 375 cartes y sont en images, les deux boîtes
   redeviennent portables — et Skrull Menace passe en premier.
2. **Classer les deux zips** hors de `A créer`, dans un dossier « incomplet »,
   pour ne plus les recroiser à chaque revue.
3. **Ne garder que le ménage** : supprimer les deux copies d'août (766 Mo) et
   laisser les zips de septembre où ils sont.

Dans tous les cas, le ménage du point 1 est sans risque et indépendant.

⚠ **Ce que cette analyse n'a pas fait** : lire les 24 pages de chaque livret. Je
me suis arrêté aux pages de présentation, de règles, de mode campagne et de
decklists (GS 2, 4, 5, 21 ; SM 2, 3, 5). Les pages de scénario diraient le détail
de chaque mise en place, mais elles ne changeront pas la conclusion : sans les
cartes, il n'y a rien à porter.

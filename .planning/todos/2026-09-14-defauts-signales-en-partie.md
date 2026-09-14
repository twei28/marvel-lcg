# ⛔ PRIORITÉ ABSOLUE — six défauts signalés EN PARTIE, tous à RE-VÉRIFIER EN JEU

**À lire en premier, avant tout autre sujet du backlog.**

> Consigne explicite de l'utilisateur, 14/09/2026 :
> « Même si tu dis que c'est corrigé, tu vas mettre tout ça au backlog et tu vas
> dire que c'est la priorité [...] même si tu dis que tu l'as fait, tu vas dire
> qu'il faut rechecker et rechecker **en vérifiant in game, pas par moi, mais
> par toi**. »

## ⚠ LA RÈGLE DE CETTE FICHE

**Aucune ligne marquée « corrigé » ne doit être crue.** Chacune est à reprendre
et à prouver EN JEU, dans le navigateur, par l'assistant — pas par
l'utilisateur, et pas par un test unitaire seul.

Pourquoi cette règle existe, dans ses mots : « On dirait que tu ne vérifies pas
et que tu ne vas pas jusqu'au bout des choses. Ce n'est pas vérifier de A à Z,
ce n'est pas faire un truc, tu vérifies chaque truc. »

Le fait : le défaut n°1 a été signalé **trois fois**, et corrigé trois fois sur
trois causes différentes, parce qu'à chaque fois la vérification portait sur le
MORCEAU écrit et jamais sur le DÉROULÉ complet.

---

## COMMENT VÉRIFIER EN JEU (à lire avant de toucher à quoi que ce soit)

Cette section existe pour qu'une session sans mémoire puisse tout reprendre.

**1. Un serveur de jeu séparé, qui ne casse aucune partie en cours :**

```bash
~/marvel-work/python/bin/python3.10 ui-check/scripts/serveur-dev.py --port 2348
```
Il compile (~90 s) puis démarre. `bash ui-app/deployer.sh` reconstruit le
plateau dans cette installation (il ne déploie RIEN en production).

**2. Ouvrir une phase du méchant SANS jouer de partie**, grâce aux états
capturés (`tools/autoplay.py` avec `AUTOPLAY_CAPTURE=<dossier>`) :

```
http://127.0.0.1:2348/app/board.html?phase=sur-table&etat=rhino__spider_man__phase-mechant-complet.js
http://127.0.0.1:2348/app/board.html?phase=sur-table&etat=rhino__spider_man__phase-mechant-attaques.js
```
`?phase=sur-table` est la porte de chantier : elle ouvre le mode quel que soit
l'interrupteur. Sans `?phase=`, on est en mode **Détaillé**, ce qu'il faut pour
le défaut n°4.

⚠ La page `?etat=` monte le plateau, le cartouche et le bandeau, mais **pas la
barre d'action** : ce qui s'y rattache ne s'y observe pas.

**3. Le test de bout en bout, celui qui manquait :**

```bash
cd ui-check && UI_CHECK_BASE=http://127.0.0.1:2348 WSLENV=UI_CHECK_BASE \
  npx playwright test tests/phase-sur-table.spec.ts --project=pc
```
Il parcourt une phase entière, **attend cinq secondes à chaque étape sans rien
toucher** et échoue si quoi que ce soit a bougé ; puis compte les panneaux au
centre. ⚠ Il ne couvre PAS le mode Détaillé ni la fenêtre de défense : c'est un
filet, pas une preuve complète.

**4. Regarder l'écran.** Capture d'écran Playwright, et la LIRE. Plusieurs
défauts de cette liste n'étaient visibles qu'à l'œil.

---

## 1. ⛔ « Ça continue tout seul sans que je mette Suivant » — TROIS FOIS

> « Je te l'ai dit mille fois, pourquoi est-ce que ça continue tout seul sans
> que moi je mette suivant ? Ça ne devrait pas arriver putain. »

| # | Cause | Prétendu état | À FAIRE |
|---|---|---|---|
| 1 | « Avance toute seule » GRISÉ hors Détaillé mais dont la valeur s'appliquait quand même. **Griser ne désactive pas.** | corrigé, déployé (`b201c6d4`) | **re-vérifier en jeu** |
| 2 | le mode lui-même | sans objet | — |
| 3 | **Le cartouche acquitte le moteur TOUT SEUL sur une étape d'ANNONCE** (décision 7 de la spec du 07/09 pour le mode Détaillé : « pas de clic sur *va attaquer* »), ce qui contredit sa décision : deux clics par attaque, l'annonce portant le premier « parce que c'est là aussi où on peut choisir de défendre ». | corrigé, commité `<voir plus bas>` | **re-vérifier en jeu** |

Règle extraite dans `ui-app/src/board/cartouche-a-jour.ts`, gate de onze cas.

⚠ **Ce défaut ne se voit pas** : rien ne plante, rien ne rougit, la phase défile.
Le seul contrôle valable est d'ATTENDRE sans cliquer et de regarder.

## 2. ⛔ Trois panneaux superposés au centre

> « C'est quoi cette merde qui se superpose. » / « On est quand même d'accord que
> là il y a trois trucs qui se superposent, c'est n'importe quoi. »

Capture : le sélecteur de cibles (« CIBLES HORS TABLE »), le panneau du moteur
(« CHOISIR LA CIBLE ») et le cartouche replié, tous les trois au centre.

Cause : depuis que le bouton a été centré à sa demande, tout ce qui se pose « au
centre » s'y retrouve ensemble.

**Prétendu corrigé** (le cartouche se tait). **À re-vérifier en jeu, sur une
vraie question du moteur** — la fixture n'en porte pas.

## 3. ⛔ Le jeton de menace : DEUX demandes, UNE SEULE traitée

> « J'ai envie que la menace sur le trafic clandestin **se mette quand je fais
> suivant** et qu'il ait déjà **la même forme que le triangle** là. Pourquoi tu
> me fais un rond ? »

- **La forme** : l'image du vrai jeton existait déjà
  (`components/jetons/menace.png`), utilisée par la scène du mode Détaillé.
  **Prétendu corrigé, JAMAIS VU À L'ÉCRAN.** À re-vérifier en jeu.
- **Le moment : PAS FAIT.** Le jeton part dès que l'étape s'affiche, avant tout
  clic. Il doit partir AU CLIC, comme la carte rencontre.

## 4. ⛔⛔ RÉGRESSION — en mode Détaillé, on ne sait plus quand on peut défendre

> « Et en mode détaillé il n'indique même plus quand on peut défendre etc, il
> fait cliquer sur la carte sans rien indiquer. C'est une putain de régression. »

**LE PLUS GRAVE.** C'est le mode de tous les joueurs, il marchait, et quelque
chose de la journée l'a cassé. **RIEN NE DOIT ÊTRE DÉPLOYÉ TANT QUE CE DÉFAUT
N'EST PAS COMPRIS.**

**Cause NON TROUVÉE.** Trois pistes ont été écartées PAR LECTURE, donc sans
preuve, et il faut les reprendre en jeu :
- `unCartouche` a remplacé `modePhase === 'detaille'` en huit endroits
  (commit `56b6e6e8`) : les deux valent la même chose quand le mode EST
  « detaille »… en théorie ;
- l'extraction de `cartoucheEstAJour` : formule équivalente tant que `surTable`
  est faux… en théorie ;
- le silence du cartouche devant la question : gardé par `surTable`… en théorie.

**Où chercher** : `questionEnScene` et `afficherDemandeCentrale` (board.tsx), la
prop `question` passée à `DeroulePhase`, `texteFenetreReponse()` dans la branche
repliée, et la branche `questionAuJoueur && question`.

**Comment reproduire** : une vraie partie en mode Détaillé jusqu'à une attaque
du méchant, et regarder si la fenêtre « Défendre / Passer » s'annonce.
`git bisect` sur les commits de la journée est une piste sérieuse.

## 5. ⛔ « Maîtres du Chaos révèle Maîtres du Chaos » — signalé DEUX FOIS

D'abord « L'Homme-Radioactif révèle L'Homme-Radioactif », classé « non
reproduit » à tort : une capture d'autoplay montrait `joueur_nom` correct, et
j'en avais conclu qu'il n'y avait rien. **Le défaut n'était pas dans la donnée,
il était dans l'affichage.** Leçon : une donnée juste ne prouve pas un affichage
juste.

**Cause trouvée, CORRECTION NON ÉCRITE.** Dans `DeroulePhase` :

```ts
auteurNom: enFrancais(etape.carteId, etape.auteurNom)
```

`enFrancais(id, nom)` rend `nomFr(id) ?? nom`. Sur une révélation, `carteId`
désigne **la carte révélée**, pas le héros. Le nom du héros est donc écrasé par
celui de la carte, des deux côtés de la phrase.

⚠ La ligne juste en dessous (`cibleNom`) porte DÉJÀ ce cas particulier, écrit le
09/09/2026 pour une raison jumelle (« prendre carteId ici écrivait *Klaw attaque
Klaw* »). Le même piège, à une ligne d'écart.

**À faire** : ne pas traduire l'auteur par `carteId` sur une révélation, **avec
un cas de test** — ce fichier n'en a aucun sur ce point — puis vérifier en jeu.

## 6. ⛔ Le texte marvelcdb sous la carte agrandie est en ANGLAIS

> « Je suis en FR et le texte dans le tooltip sous la carte est en
> anglais............... »

Capture : la carte Hulk agrandie, bloc « MARVELCDB » en dessous, en anglais, en
pleine partie française.

**NON EXAMINÉ.** Chercher du côté du réglage « Textes marvelcdb » et de sa
source : le proxy réseau (coupé par défaut, arrive après coup) contre le
dictionnaire local (`noms-fr.ts`, `textes-fr-complets`).

⚠ **Troisième défaut de langue de la journée**, après les 61 clés sans anglais
et les noms anglais du bilan (les deux corrigés et déployés). Trois défauts de
langue en un jour appellent **une passe de langue à part entière**, pas des
correctifs au coup par coup : il faudrait lister tout ce qui s'affiche et
vérifier chaque source dans les deux langues.

---

## État exact du dépôt

- **Déployé en production** : jusqu'à `b5c42238`.
- **Commité mais PAS déployé** : tout ce qui suit `b5c42238`.
- ⚠ **Le code des défauts 1, 2 et 3 (forme) a été écrit et commité SANS AVOIR
  ÉTÉ VU EN JEU.** C'est précisément ce que cette fiche demande de reprendre.

## Statut

**PRIORITÉ ABSOLUE**, ouverte le 14/09/2026. Six défauts.
**Rien n'est prouvé tant que ce n'est pas vérifié en jeu par l'assistant.**

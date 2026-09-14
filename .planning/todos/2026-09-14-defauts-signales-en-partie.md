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
capturés (`Fusion/marvel-lcg-src/tools/autoplay.py` avec
`AUTOPLAY_CAPTURE=<dossier>`) :

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

**5. JOUER UNE VRAIE PARTIE, sans toucher une souris.** C'est ce qui a permis
de trouver la cause du défaut n°4, et les fixtures n'y suffisaient pas (elles
ne portent aucune question du moteur). Recette, écrite pour être recopiée :

- créer la partie : `GET /new?data=<descripteur>` (le descripteur est figé dans
  `ui-check/contrat-nouvelle-partie.json`, et `lancement-partie.spec.ts` le
  construit déjà) ; **le monde ne se met en place qu'une fois un client
  connecté** : ouvrir `/app/board.html` PUIS attendre `render_id > 0` ;
- garder la main de départ (bouton « Garder cette main ») ;
- pour atteindre une ATTAQUE, il faut basculer en identité héros au tour 1
  (option `Change_Form`), sinon le méchant manigance et n'attaque jamais ;
- répondre au moteur comme le ferait un bouton :
  `POST /post?p=0` avec `{"id":<option>,"targets":[…],"resources":[]}`, ou `{}`
  pour passer. ⚠ Les options arrivent dans `options_json` (une CHAÎNE), et une
  option qui exige des cibles (`target_num_range`) fait PLANTER le moteur si on
  répond sans elles ;
- ⚠ `GET /get_ask` répond un objet MÊME QUAND IL N'Y A RIEN À DEMANDER : il est
  alors sans `event_name`. Le lire comme une question donne de faux défauts.

Tout cela est écrit et commenté dans `ui-check/tests/phase-detaille-defense.spec.ts`.

---

## 1. ⛔ « Ça continue tout seul sans que je mette Suivant » — TROIS FOIS

> « Je te l'ai dit mille fois, pourquoi est-ce que ça continue tout seul sans
> que moi je mette suivant ? Ça ne devrait pas arriver putain. »

| # | Cause | État au 14/09/2026, 20 h | Preuve |
|---|---|---|---|
| 1 | « Avance toute seule » GRISÉ hors Détaillé mais dont la valeur s'appliquait quand même. **Griser ne désactive pas.** | **vérifié EN JEU** | `phase-sur-table.spec.ts`, cas « même avec Avance toute seule ALLUMÉE, rien ne bouge » : cinq secondes d'attente, rien ne bouge. |
| 2 | le mode lui-même | sans objet | — |
| 3 | **Le cartouche acquitte le moteur TOUT SEUL sur une étape d'ANNONCE** (décision 7 de la spec du 07/09 pour le mode Détaillé : « pas de clic sur *va attaquer* »), ce qui contredit sa décision : deux clics par attaque, l'annonce portant le premier « parce que c'est là aussi où on peut choisir de défendre ». | **PAS ENCORE PROUVÉ EN JEU** | gate unitaire seulement (`cartouche-a-jour.test.ts`, 11 cas) |

Règle extraite dans `ui-app/src/board/cartouche-a-jour.ts`, gate de onze cas.

⚠ **Ce défaut ne se voit pas** : rien ne plante, rien ne rougit, la phase défile.
Le seul contrôle valable est d'ATTENDRE sans cliquer et de regarder.

### ⚠ CE QU'ON A APPRIS EN ESSAYANT DE PROUVER LA CAUSE 3 (à ne pas refaire)

- **Le filet sur état enregistré NE PEUT PAS la garder.** `?etat=` ne rejoue
  aucune trame du moteur : il n'y a rien à relâcher, donc rien à retenir.
  Mesuré en retirant la garde `!surTable` et en reconstruisant : les cas de
  `phase-sur-table.spec.ts` restent VERTS. Ils gardent l'avance auto (cause 1),
  pas l'acquittement (cause 3).
- **La fixture `…phase-mechant-complet.js` ne contient AUCUNE annonce** (menace,
  deux manigances, révélations). C'est `…phase-mechant-attaques.js` qui en porte
  une : « Rhino va attaquer Spider-Man · 3 dégâts », au 4ᵉ temps.
- **Un test en vraie partie a été écrit, essayé six fois, puis ABANDONNÉ** : il
  demande sept minutes et reste fragile. Ce qui coûte : atteindre une attaque
  exige de jouer un tour de héros en forme HÉROS, et sur la table chaque temps
  demande un clic.
- **Observé EN JEU malgré tout, sans être figé dans un test** : l'annonce
  « Rhino va attaquer Spider-Man · 2 dégâts » s'affiche, et cinq secondes plus
  tard le déroulé n'a PAS sauté au temps suivant — le cartouche s'est tu et le
  panneau du moteur (« Défendre / Passer ») a pris sa place, ce qui est le
  comportement voulu. **Ce n'est pas une preuve, c'est une observation.**
- Deux pièges du harnais, pour la prochaine fois :
  - une route interceptée (`page.route('**/get_site_admin')`) empêche le
    `waitUntil: 'networkidle'` d'`ouvrirEtMettreEnPlace` de se satisfaire, et le
    test reste bloqué cinq minutes avant sa première boucle ;
  - appeler `avancerLaPartie` PENDANT la phase du méchant le fait attendre une
    question qui ne viendra jamais : sur la table, le cartouche retient la trame
    tant que le joueur n'a pas cliqué. Le tour du héros se joue par le pilote,
    la phase du méchant par l'écran.

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

## 4. ✅ Mode Détaillé : on ne savait plus quand on peut défendre — CAUSE TROUVÉE, CORRIGÉ, VÉRIFIÉ EN JEU

> « Et en mode détaillé il n'indique même plus quand on peut défendre etc, il
> fait cliquer sur la carte sans rien indiquer. C'est une putain de régression. »

**Reproduit en jeu le 14/09/2026**, dans une vraie partie Rhino / Spider-Man
sur le serveur de chantier (port 2348), mode Détaillé, jusqu'aux attaques du
round 2. Relevé du rendu à la seconde près, à l'instant où le moteur demande
« Défendre / Passer » :

```
effets = 1   afficherDemandeCentrale = false   questionEnScene = false
cartouche : « deroule-phase est-replie », texte « tu peux défendre ou répondre »
boutons visibles : AUCUN (seule la barre d'outils du haut)
```

**La cause.** `afficherDemandeCentrale` portait la condition `effets.size === 0`
— « le panneau central cède la place à une animation en cours » — et
`questionEnScene` était bâti PAR-DESSUS lui. Or une animation d'effet dure
**1,7 s** (`useEffetsCartes`), et la seconde attaque d'une phase arrive
toujours pendant l'animation des dégâts de la première. La question n'était
alors logée NI dans le panneau central NI dans la scène : le cartouche se
repliait sur une phrase SANS BOUTON, et il ne restait que le menu d'une carte
de la table. Mot pour mot ce qui a été signalé.

⚠ **Ce n'était pas une régression de la journée** : la condition date du
07/09/2026 (`5536a7a4`, naissance de `questionEnScene`). Ce qui a changé, ce
sont les animations, qui ont rendu la fenêtre visible.

**Le correctif** : la règle est sortie de `board.tsx` et vit désormais dans
`ui-app/src/board/ou-va-la-question.ts`, avec sa gate de 12 cas. Le panneau
central cède toujours à l'animation ; la SCÈNE, elle, ne cède qu'aux autres
FAÇONS DE RÉPONDRE (un ciblage, le menu d'une carte), jamais à une animation,
parce qu'il n'y a rien derrière elle. `EvenementCentrale` se tait aussi devant
la question logée dans la scène, sans quoi la narration se poserait au centre,
par-dessus les boutons.

**La preuve** :
- `ui-app/src/board/ou-va-la-question.test.ts` — 12 cas ; vérifié ROUGE en
  remettant l'ancienne règle ;
- `ui-check/tests/phase-detaille-defense.spec.ts` (`npm run
  phase-detaille-defense`) — joue une VRAIE partie jusqu'à deux fenêtres de
  défense et surveille le cartouche toutes les 200 ms après chaque clic.
  Vérifié ROUGE avec l'ancienne règle remise et le plateau reconstruit, VERT
  avec le correctif. ⚠ Un test qui s'arrêtait à la PREMIÈRE attaque passait au
  vert à tort : c'est la seconde qui porte le défaut.
- capture d'écran relue : titre, bandeau « À TOI DE JOUER », boutons
  DÉFENDRE / PASSER, un seul panneau au centre.

**Reste à voir** (constaté sur la capture, HORS de ce défaut) : en 1920×1080,
le haut du cartouche (la chronologie MENACE / MÉCHANT / SBIRES…) déborde de
l'écran par le haut.

## 5. ⛔ « Maîtres du Chaos révèle Maîtres du Chaos » — signalé DEUX FOIS

D'abord « L'Homme-Radioactif révèle L'Homme-Radioactif », classé « non
reproduit » à tort : une capture d'autoplay montrait `joueur_nom` correct, et
j'en avais conclu qu'il n'y avait rien. **Le défaut n'était pas dans la donnée,
il était dans l'affichage.** Leçon : une donnée juste ne prouve pas un affichage
juste.

**Cause trouvée, CORRECTION ÉCRITE dans `a02101a1` mais JAMAIS VUE EN JEU** —
la ligne ci-dessous ne traduit plus l'auteur par `carteId` sur une révélation,
et un cas de test la garde. Reste à le vérifier en partie. Dans `DeroulePhase` :

```ts
auteurNom: enFrancais(etape.carteId, etape.auteurNom)
```

`enFrancais(id, nom)` rend `nomFr(id) ?? nom`. Sur une révélation, `carteId`
désigne **la carte révélée**, pas le héros. Le nom du héros est donc écrasé par
celui de la carte, des deux côtés de la phrase.

⚠ La ligne juste en dessous (`cibleNom`) porte DÉJÀ ce cas particulier, écrit le
09/09/2026 pour une raison jumelle (« prendre carteId ici écrivait *Klaw attaque
Klaw* »). Le même piège, à une ligne d'écart.

**À faire** : vérifier EN JEU qu'une révélation annonce bien « Jessica Jones
révèle Maîtres du Chaos », et non le nom de la carte des deux côtés.

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
- **Commité mais PAS déployé** : tout ce qui suit `b5c42238`, le correctif du
  défaut n°4 compris.
- ⚠ **Le code des défauts 1, 2 et 3 (forme) a été écrit et commité SANS AVOIR
  ÉTÉ VU EN JEU.** C'est précisément ce que cette fiche demande de reprendre.

## Statut

**PRIORITÉ ABSOLUE**, ouverte le 14/09/2026. Six défauts.
**Rien n'est prouvé tant que ce n'est pas vérifié en jeu par l'assistant.**

Avancement au 14/09/2026, 20 h :
- n°4 : **fait**, cause trouvée, corrigé, prouvé en jeu (rouge/vert mesurés).
- n°1 : cause 1 **vérifiée en jeu** ; cause 3 **toujours pas prouvée en jeu**
  (voir l'encadré de ce défaut : le filet sur fixture ne peut pas la garder).
- n°2, 3, 5, 6 : **à reprendre**, toujours rien de prouvé en jeu.

# Kit de création de campagne : Marvel Champions LCG (moteur `marvel-lcg`, projet « Narwhal Champions »)

> **Version du 20/10/2026.** Ce manuel est construit par `outils/construire-kit-campagne.py` à partir du dépôt
> réel : chaque fichier cité en bloc de code est la **copie exacte** du fichier du projet au moment de la
> construction. Si un exemple de ce manuel et le dépôt divergent un jour, c'est le dépôt qui a raison.

## 1. Mode d'emploi et règles absolues

### 1.1 Pour qui, pour quoi

Tu es une IA chargée de **produire les fichiers d'une campagne** pour ce jeu : les cartes, les scénarios, les
sets de rencontre, la description de la campagne, la logique de carnet, les scripts des cartes, les textes
français, la liste des images, et les preuves (cas de test) qui vont avec.

Ce que tu produis **n'est jamais intégré tel quel**. Il est donné à **Claude**, l'assistant qui a accès au dépôt
du jeu : Claude le compare, le teste en jeu, le corrige et l'intègre. Tu n'as, toi, accès à rien d'autre que ce
manuel, ses annexes et les fichiers modèles du zip. Tout ce que tu dois savoir est donc ici.

Ce manuel couvre **toute la chaîne** d'une campagne, dans cet ordre :

1. **Les cartes** (`data/cards.json`) : vilains, complots principaux et annexes, sbires, traîtrises,
   attachements, environnements, cartes de campagne, récompenses, et au besoin héros et cartes joueur.
2. **Les scénarios et les sets de rencontre** (`data/scenarios`, `data/encounter_sets`, `data/sets_info.json`).
3. **Les scripts** des cartes (`src/cards/pack/<pack>/...`), c'est-à-dire leurs capacités en Python.
4. **La logique de campagne côté moteur** (`src/cards/pack/<pack>/campaign.py`) : ce que le carnet change à la
   mise en place du scénario suivant, et ce que le jeu relève à la fin d'un scénario.
5. **La description de la campagne** (`data/campagnes/<code>.json`) : ce que l'écran des campagnes montre et ce
   que le panneau de récompenses fait reporter au carnet.
6. **Les textes français, les images, les pages du livret, les crédits, les preuves de test.**

### 1.2 Les règles absolues

Elles viennent de règles posées par l'utilisateur du projet et d'erreurs déjà payées. Les enfreindre fait
échouer l'intégration, ou pire : produit une campagne qui *a l'air* de marcher et ne marche pas.

1. **Fidélité à 100 % au texte imprimé.** Une carte fait exactement ce qu'elle dit, rien de moins, rien de plus.
   Pas d'approximation « recommandée ». Si le moteur ne sait pas faire ce que la carte dit, tu l'écris dans
   `A_FAIRE_CLAUDE` (règle 3) : le moteur s'étend, la carte ne s'édulcore pas.
2. **N'invente jamais une fonction, une clé, une chaîne de ciblage.** Tu n'utilises que ce qui figure dans ce
   manuel, dans ses annexes, dans l'index de l'API du moteur (`annexes/I-index-api-moteur.md`) ou dans les
   fichiers modèles. Une fonction inventée ne lève **presque jamais d'erreur** : la carte se construit, entre en
   jeu, et ne fait rien. C'est le défaut le plus fréquent et le plus silencieux de ce projet.
3. **Ce que tu ne sais pas faire s'écrit, il ne se devine pas.** Écris dans le script :

   ```python
   # A_FAIRE_CLAUDE: <ce qui manque, le texte imprimé visé, la carte de référence la plus proche>
   ```

   et continue le reste. Une carte à moitié écrite avec un `A_FAIRE_CLAUDE` honnête vaut mieux qu'une carte
   « complète » qui appelle une fonction inventée. **Un script qui renvoie une liste vide ne signifie pas que la
   carte n'a aucun effet** : si la carte a un texte de capacité, un `GetAbilities()` vide sans
   `A_FAIRE_CLAUDE` est une faute.
4. **Une question à la fois, en choix multiple.** Quand un texte, une icône ou une règle laisse place à plus
   d'une lecture, tu poses **une seule** question à l'utilisateur (pas un lot de dix), avec : l'option que tu
   recommandes en premier, « Autre (précise) » en dernier, et pour chaque option **ce que ça change en jeu**.
   Tu cites le fichier image de la carte concernée. Tu attends la réponse avant la question suivante. Tu ne
   tranches pas en silence. Détail et cas qui déclenchent une question : §1.3.
5. **Ne touche jamais au moteur.** Tu n'écris que des cartes, des scénarios, des campagnes, leurs scripts, leurs
   textes et leurs preuves. Si une mécanique demande une modification du moteur (un compteur nouveau, un trait
   nouveau, un message nouveau, un type de champ de carnet nouveau, un écran nouveau), tu l'écris dans
   `BESOINS-MOTEUR.md` (§12.4) : ce que c'est, pourquoi, quelle carte l'exige.
6. **N'écrase jamais un fichier partagé.** `data/cards.json`, `data/sets_info.json`,
   `ui-app/src/board/textes-fr-fanmade.ts` et `tools/prefixes_fanmade.json` contiennent le travail de tout le
   monde. Tu livres des **fragments** à fusionner (§12), jamais le fichier entier.
7. **Les valeurs de `desc` sont toujours des chaînes** (`"HP": "10"`, jamais `10`).
8. **Une icône de ressource ne se nomme jamais « à vue ».** Elle se compare à une carte du même pack dont la
   ressource est connue (§4.6). Une lecture au jugé a déjà inventé une « ressource os » (sur Lockjaw) : quatre
   cartes n'ont pas rendu ce qu'elles promettent jusqu'au 9/8/2026.
9. **Les textes de cartes sont en anglais** (c'est la langue des données du moteur). Le texte français se livre à
   part, dans un fragment dédié, avec le vocabulaire officiel (§10.3).
10. **Ne laisse aucune trace de travail dans les livrables** : pas de `print` de debug, pas de fichier
    temporaire, pas de commentaire qui raconte ton raisonnement. Les commentaires expliquent *pourquoi* une
    carte est écrite ainsi, en français, comme dans les modèles.

### 1.3 Ce qui déclenche une question à l'utilisateur

| Situation | Exemple vécu |
|---|---|
| Mot-clé maison non défini sur les cartes fournies | « drain X » qu'aucune carte n'explique |
| Texte imprimé contradictoire | « Forced **Interrupt** : **After** X schemes or attacks » : le type et le déclencheur se contredisent |
| Valeur imprimée que le format ne sait pas exprimer | une ATK « ★ » |
| Portée ambiguë d'une phrase | « Discard this obligation » : la dernière option seulement, ou les deux ? |
| Mot-clé officiel inapplicable tel quel | `TeamUp` qui suppose deux héros en jeu |
| Contenu absent du matériel fourni | aucune liste de deck fournie pour un héros |
| Effet que le moteur ne peut pas rendre fidèlement | « if this attack has ranged or piercing » sur un événement |
| Icône imprimée qu'on ne reconnaît pas | l'icône « nœuds reliés » de Lockjaw, prise pour un os pendant cinq jours |
| Règle du livret qui ne dit pas quoi faire d'un cas limite | une défaite au scénario 3 : se rejoue-t-il, ou la campagne continue-t-elle ? |

Ne posent **pas** de question : les choix purement techniques (quelle fabrique, où ranger une aide, format
d'image). Ceux-là, tu les fais, et tu les expliques dans tes doutes si tu hésites.

Les points **non tranchables** (une capacité que tu ne sais pas coder, un comportement du moteur que tu ne peux
pas vérifier) ne sont pas des questions : ils vont dans `A_FAIRE_CLAUDE` et dans `QUESTIONS.md`.

### 1.4 Ce que tu livres (résumé ; le détail est au §12)

Un dossier `livraison/` qui **reproduit l'arborescence du projet**, plus quatre fichiers de suivi :

```
livraison/
  MANIFESTE.md           la liste de TOUS les fichiers livrés, une ligne chacun : chemin, rôle, nombre de cartes
  QUESTIONS.md           les questions ouvertes (une par carte ou par règle), format du §1.3
  BESOINS-MOTEUR.md      ce que le moteur ou l'interface devra apprendre (trait, compteur, message, écran...)
  AUTO-VERIFICATION.md   ce que tu as vérifié toi-même, avec la sortie de `verifier-livraison-campagne.py`
  integration/           l'arborescence à fusionner (data/..., src/..., tools/..., textes-fr/..., images.md)
```

Avant de livrer, tu lances **`verifier-livraison-campagne.py`** (fourni dans le zip, à la racine, Python 3 sans
dépendance) sur ton dossier. Il attrape les erreurs de forme que Claude attraperait de toute façon, mais que tu
peux corriger toi-même sans attendre : clés manquantes, identifiants en double, scénario qui référence une
carte absente, script rangé dans le mauvais dossier, clé de carnet qui n'existe nulle part, vocabulaire
français interdit. **Il ne remplace pas le jeu** : un script qui passe ce contrôle peut encore ne rien faire en
partie. C'est pourquoi les règles 2 et 3 comptent plus que tout le reste.

### 1.5 Comment lire ce manuel

| Si tu dois... | Lis |
|---|---|
| comprendre ce qu'est une campagne ici et comment tout s'enchaîne | §2 |
| savoir quels fichiers produire | §3 (la liste maîtresse) |
| écrire ou vérifier une carte | §4 puis l'annexe A (kit de cartes, catalogue d'exemples réels) |
| écrire un scénario et ses sets | §5 |
| écrire le script d'une carte | §6, annexes A, B (recettes) et C (mots-clés) |
| écrire la logique de carnet | §7 |
| écrire `data/campagnes/<code>.json` | §8 |
| comprendre ce que fait l'écran | §9 |
| les images, textes français, pages du livret, crédits | §10 |
| prouver que ça marche | §11 |
| préparer la livraison | §12 |
| voir deux campagnes complètes, fichier par fichier | §13 et le dossier `modeles/` du zip |
| éviter les pièges déjà payés | §14 |

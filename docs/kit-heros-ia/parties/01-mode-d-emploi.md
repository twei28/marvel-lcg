# Kit de création de héros : Marvel Champions LCG (moteur `marvel-lcg`, projet « Narwhal Champions »)

> **Version du 20/10/2026.** Ce manuel est construit par `outils/construire-kit-heros.py` à partir du dépôt
> réel : chaque fichier cité en bloc de code est la **copie exacte** du fichier du projet au moment de la
> construction. Si un exemple de ce manuel et le dépôt divergent un jour, c'est le dépôt qui a raison.

## 1. Mode d'emploi et règles absolues

### 1.1 Pour qui, pour quoi

Tu es une IA chargée de **produire les fichiers d'un héros** pour ce jeu : ses cartes (les deux faces de l'identité,
les cartes signature, l'obligation, le set némésis, au besoin les cartes d'aspect du pack), son deck de départ,
les scripts de ses cartes (leurs capacités en Python), les textes français, sa biographie, la liste des images, et
les preuves (cas de test) qui vont avec. L'utilisateur te donne **les images des cartes du héros** : ce sont elles
qui font foi pour tout ce qui est imprimé.

Ce que tu produis **n'est jamais intégré tel quel**. Il est donné à **Claude**, l'assistant qui a accès au dépôt
du jeu : Claude le compare, le teste en jeu, le corrige et l'intègre. Tu n'as, toi, accès à rien d'autre que ce
manuel, ses annexes et les fichiers modèles du zip. Tout ce que tu dois savoir est donc ici.

Ce manuel couvre **toute la chaîne** d'un héros, dans cet ordre :

1. **Les cartes** (`data/cards.json`) : les faces `Hero` / `AlterEgo`, les cartes signature, l'obligation, les
   cartes némésis, et si le pack en a, les cartes d'aspect.
2. **Le deck de départ** (`deck/starter/<héros>.json`) et l'entrée de l'extension (`data/sets_info.json`).
3. **Les scripts** des cartes (`src/cards/pack/<pack>/…`).
4. **Les textes français, la biographie, la réplique de recrutement, les images, les crédits.**
5. **Les preuves** : cas de test de capacité, gabarits de contrôle par carte.

### 1.2 Les règles absolues

Elles viennent de règles posées par l'utilisateur du projet et d'erreurs déjà payées. Les enfreindre fait
échouer l'intégration, ou pire : produit un héros qui *a l'air* de marcher et ne marche pas.

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
4. **Une question à la fois, en choix multiple, avec l'image.** Quand un texte, une icône ou une règle laisse
   place à plus d'une lecture, tu poses **une seule** question à l'utilisateur (pas un lot de dix), avec :
   l'**image de la carte concernée** (cite son fichier), l'option que tu recommandes en premier, « Autre
   (précise) » en dernier, et pour chaque option **ce que ça change en jeu**. Tu attends la réponse avant la
   question suivante. Tu ne tranches pas en silence. Cas qui déclenchent une question : §1.3.
5. **Ne touche jamais au moteur.** Tu n'écris que des cartes, des decks, leurs scripts, leurs textes et leurs
   preuves. Si une mécanique demande une modification du moteur (un compteur nouveau, un trait nouveau, un
   message nouveau), tu l'écris dans `BESOINS-MOTEUR.md` (§9.5) : ce que c'est, pourquoi, quelle carte l'exige.
6. **N'écrase jamais un fichier partagé.** `data/cards.json`, `data/sets_info.json`,
   `ui-app/src/board/textes-fr-fanmade.ts`, `tools/prefixes_fanmade.json`, `public/js/prepare/heros-info.js`
   et `public/js/prepare/repliques-heros.js` contiennent le travail de tout le monde. Tu livres des
   **fragments** à fusionner (chapitre 9), jamais le fichier entier.
7. **Les valeurs de `desc` sont toujours des chaînes** (`"HP": "14"`, jamais `14`).
8. **Une icône de ressource ne se nomme jamais « à vue ».** Elle se compare à une carte du même pack dont la
   ressource est connue. Une lecture au jugé a déjà inventé une « ressource os » sur Lockjaw : l'icône « nœuds
   reliés » était une ressource **mentale**, et quatre cartes n'ont pas rendu ce qu'elles promettent pendant cinq
   jours. Dans le doute : question (§1.3).
9. **Les textes de cartes sont en anglais** (c'est la langue des données du moteur). Le texte français se livre à
   part, dans un fragment dédié, avec le vocabulaire officiel (chapitre 7).
10. **`player_deck` reste VIDE pour un héros maison**, sauf si **l'auteur du héros fournit une decklist** imprimée
    ou dans son dossier : on la recopie alors telle quelle. Les ~25 cartes d'aspect qu'une IA « composerait » pour
    compléter un héros sont une invention, pas du contenu de l'auteur (consigne de l'utilisateur du
    06/09/2026, appliquée à 33 decks le 12/09/2026). Ne pose plus la question de l'aspect.
11. **Jamais la carte signature d'un autre héros** dans un deck. Une carte de classe `Hero` (`desc.Class =
    "Hero"`) appartient à un seul héros. Le moteur **ne valide pas** les decks de départ : c'est à toi.
12. **Ne laisse aucune trace de travail dans les livrables** : pas de `print` de debug, pas de fichier
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
| Contenu absent du matériel fourni | aucune liste de deck fournie pour un héros maison |
| Effet que le moteur ne peut pas rendre fidèlement | « if this attack has ranged or piercing » sur un événement |
| Icône imprimée qu'on ne reconnaît pas | l'icône « nœuds reliés » de Lockjaw, prise pour un os |
| Que devient une chose au moment du retournement d'identité ? | Iron Fist : les jetons Chi restent-ils sur l'identité quand on passe en alter ego ? (réponse : oui, décision de l'utilisateur du 20/10/2026) |
| Deux lectures valides de « a scheme » / « an enemy » | The Way of Things : deux « a scheme » indépendants, ou le même ? |
| Carte du héros qui nomme une carte absente des images fournies | une capacité qui « cherche X » où X n'est pas dans le matériel : X existe-t-elle déjà dans le jeu, ou faut-il la livrer ? |

Ne posent **pas** de question : les choix purement techniques (quelle fabrique, où ranger une aide, format
d'image). Ceux-là, tu les fais, et tu les expliques dans tes doutes si tu hésites.

Les points **non tranchables** (une capacité que tu ne sais pas coder, un comportement du moteur que tu ne peux
pas vérifier) ne sont pas des questions : ils vont dans `A_FAIRE_CLAUDE` et dans `QUESTIONS.md`.

### 1.4 Ce que tu livres (résumé ; le détail est au chapitre 9)

Un dossier `livraison/` qui **reproduit l'arborescence du projet**, plus des fichiers de suivi :

```
livraison/
  MANIFESTE.md           la liste de TOUS les fichiers livrés, une ligne chacun : chemin, rôle, nombre de cartes
  QUESTIONS.md           les questions ouvertes (une par carte ou par règle), format du §9.4
  BESOINS-MOTEUR.md      ce que le moteur ou l'interface devra apprendre (trait, compteur, message, écran...)
  A_FAIRE_CLAUDE.md      tous les marqueurs A_FAIRE_CLAUDE du code, regroupés
  GABARITS.md            un gabarit de contrôle par carte à capacité
  AUTO-VERIFICATION.md   ce que tu as vérifié toi-même, avec la sortie de `verifier-livraison-heros.py`
  images.md              card_id → fichier source
  CREDITS.md             l'auteur du héros, les sources
  integration/           l'arborescence à fusionner (data/, deck/, src/, textes-fr/, public/, tools/)
```

Avant de livrer, tu lances **`verifier-livraison-heros.py`** (fourni dans le zip, à la racine, Python 3 sans
dépendance ; il charge `verifier-livraison-campagne.py` placé à côté) sur ton dossier. Il attrape les erreurs de
forme que Claude attraperait de toute façon, mais que tu peux corriger toi-même sans attendre : une face qui
manque, un deck de départ qui cite une carte absente ou la signature d'un autre héros, une obligation sans
`GiveTo`, un script rangé dans le mauvais dossier, une capacité imprimée sans script, une biographie indexée par
le nom. **Il ne remplace pas le jeu** : un script qui passe ce contrôle peut encore ne rien faire en partie.
C'est pourquoi les règles 2 et 3 comptent plus que tout le reste.

### 1.5 Comment lire ce manuel

| Si tu dois... | Lis |
|---|---|
| comprendre ce qu'est un héros ici et comment il entre en partie | chapitre 2 |
| savoir quels fichiers produire | chapitre 3 (la liste maîtresse) |
| écrire ou vérifier les cartes du héros | chapitre 4, puis l'annexe A (kit de cartes) et le chapitre 12 |
| écrire le deck de départ, le set némésis, une variante | chapitre 5 |
| écrire le script d'une carte, une face d'identité | chapitre 6, annexes A, B (recettes) et C (mots-clés) |
| textes français, images, biographie, réplique, crédits | chapitre 7 |
| prouver que ça marche | chapitre 8 |
| préparer la livraison | chapitre 9 |
| voir quatre héros complets, fichier par fichier | chapitre 10 et le dossier `modeles/` du zip |
| éviter les pièges déjà payés | chapitre 11 |
| les tableaux de référence communs aux campagnes et aux héros | chapitre 12 |

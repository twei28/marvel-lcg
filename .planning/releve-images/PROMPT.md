# Prompt à donner à une IA qui voit les images

## À lire avant de l'envoyer

**marvelcdb ne dit pas qui est dessiné sur une carte.** Ce champ n'existe nulle
part dans sa base. Le site sert ici à deux choses seulement : donner la liste
officielle des cartes, et surtout **l'URL de chaque scan**. La réponse, elle,
ne peut venir que du fait de **regarder l'image**.

Conséquence : cette tâche n'a de sens que pour une IA capable d'**ouvrir et de
voir les images**. Une IA qui ne fait que lire du texte inventera des réponses
plausibles et fausses, et un relevé faux est pire que pas de relevé : le jeu
garde son approximation quand une carte n'est pas relevée, mais il fait
confiance à une carte relevée.

Joindre les deux fichiers :

- `personnes.csv` — les 501 personnes du jeu et leur identifiant exact
- `a-relever.csv` — les 3 989 illustrations officielles, par ordre de priorité

Les cartes fan-made ne sont pas dans la liste : marvelcdb ne les connaît pas,
elles se relèvent à la main dans le jeu.

---

## Le prompt

Tu vas m'aider à construire un relevé : pour chaque carte du jeu de société
Marvel Champions LCG, **quels personnages sont visibles sur l'illustration**.

### Ce qui compte, et ce qui ne compte pas

La question porte sur **l'image seule**, pas sur le texte, pas sur le nom, pas
sur le type de la carte.

- Un allié « Spider-Man » montre Spider-Man : il compte.
- Une amélioration « Web-Shooters » qui ne montre que des lance-toiles posés sur
  une table ne montre personne, même si elle appartient au kit de Spider-Man.
- Un événement « Swinging Web Kick » qui montre Spider-Man frappant Rhino
  montre **deux** personnes : les deux comptent.
- Un personnage reconnaissable même de dos, de loin, partiellement caché ou en
  ombre compte, **à condition** de pouvoir dire qui c'est avec certitude.
- Une silhouette anonyme, un passant, un policier sans nom, un soldat de
  l'Hydra, une foule : personne. Un lieu, un objet, un véhicule : personne.
- Un personnage en photo, en affiche, à la télévision ou en statue **dans**
  l'illustration compte : il est bien dessiné sur la carte.
- Une identité civile compte comme la personne : Peter Parker, c'est
  Spider-Man ; Bruce Banner, c'est Hulk. Le fichier `personnes.csv` te donne les
  deux noms sur la même ligne, avec un seul identifiant.

### Le vocabulaire imposé

Tu ne peux répondre qu'avec les identifiants de la colonne `id` de
`personnes.csv`. Aucun autre. Si le personnage que tu vois n'y figure pas
(un second rôle qui n'est ni un héros jouable, ni un vilain, ni un sbire unique),
**ne l'indique pas** : cette carte n'a alors aucune personne à relever de ton
point de vue.

Attention aux homonymes, ils sont volontairement séparés :
`spider-man-peter-parker`, `spider-man-miles-morales`,
`spider-man-miguel-o-hara` sont trois personnes différentes qui partagent un nom
de code. Regarde le costume et le contexte. Si tu hésites entre deux d'entre
elles, **saute la carte** plutôt que de choisir au hasard.

### Où trouver les images

Le catalogue public de marvelcdb : `https://marvelcdb.com/api/public/cards/`
renvoie toutes les cartes en JSON. Le champ `code` correspond exactement à la
colonne `image` de `a-relever.csv`, et le champ `imagesrc` donne le chemin du
scan, à préfixer par `https://marvelcdb.com`. Vérifie ces deux noms de champs
sur place plutôt que de me croire sur parole : l'API peut avoir changé.

Une carte de `a-relever.csv` absente de marvelcdb : saute-la et signale-la.

### L'ordre de travail

La colonne `priorite` de `a-relever.csv` :

- `0` : 708 cartes signature. **Commence par celles-là**, ce sont les seules
  dont j'ai besoin tout de suite.
- `1` : 1 096 autres cartes de joueur.
- `2` : 2 185 cartes de rencontre.

Ne passe à la priorité suivante qu'une fois la précédente terminée.

### Le format de sortie

Un fichier JSON, un seul objet, une clé par illustration relevée :

```json
{
  "01001a": ["spider-man-peter-parker"],
  "01002":  ["spider-man-peter-parker"],
  "01007":  ["spider-man-peter-parker", "rhino"],
  "01005":  []
}
```

- La clé est la colonne `image` de `a-relever.csv`, **telle quelle**.
- La valeur est la liste des identifiants, ordre indifférent.
- **Une liste vide veut dire « j'ai regardé, il n'y a personne dessus »**, et
  c'est une réponse utile : lieu, objet, décor, foule anonyme.
- **Une carte que tu n'as pas su trancher ne doit PAS apparaître dans le
  fichier.** C'est la règle la plus importante des trois : absente veut dire
  « pas encore regardée », et le jeu retombe alors sur son approximation. Une
  liste vide sur une carte que tu n'as pas vue serait donc une affirmation
  fausse, pas une abstention.

Rends aussi, à part, la liste des cartes que tu as sautées avec la raison en
trois mots (« image introuvable », « hésitation Spider-Man », « personnage
inconnu »).

### Comment travailler

Procède par paquets de 50 cartes, et donne-moi le JSON de chaque paquet au fur
et à mesure plutôt qu'un seul fichier à la fin. Entre deux paquets, dis-moi
combien tu as relevé, combien tu as sauté, et sur quoi tu as le plus hésité.

Ne devine jamais. Sur ce relevé, une abstention ne coûte rien et une erreur
coûte cher.

---

## Quand l'IA rend un paquet

```bash
python3 outils/importer-releve-images.py paquet-01.json            # vérifie
python3 outils/importer-releve-images.py paquet-01.json --ecrire   # verse
```

L'outil **refuse le paquet entier** si une seule ligne cloche : identifiant de
personne inventé, illustration qui n'existe pas, valeur qui n'est pas une liste.
Il ne remplace jamais le fichier en bloc, il fusionne clé par clé : les paquets
s'additionnent, et ce qui a été relevé à la main dans le jeu n'est pas écrasé.

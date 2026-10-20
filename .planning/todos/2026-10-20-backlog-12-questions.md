# Backlog 12 : questions ouvertes (vérification des cartes hors irefrixs, pack Dazzler)

Ouvert le 20/10/2026. Règle absolue de `docs/reference/PROCESSUS-CARTE.md`
(« En cas de doute : DEMANDER, carte par carte ») : ces points n'ont PAS été
tranchés. Le code est laissé tel quel en attendant la réponse, et la carte
concernée est notée « Carte terminée : NON » dans
`.planning/todos/2026-10-20-backlog-12-gabarits-processus-carte.md`.

Une question par carte, à poser une à une avec le scan sous les yeux
(`Fusion/marvel-lcg-src/assets/pics/<card_id>.png`). Option recommandée en
premier, « Autre (précise) » toujours disponible en dernier.

---

## Q1. dz012 « Too Good to be True » : qui choisit les 3 cartes du Showtime! ?

Texte imprimé : « **Showtime!**: Shuffle 3 cards from your discard pile into
your deck. »

Le texte ne dit ni « choose », ni « top », ni « random ». Le code actuel prend
les **3 cartes du dessus** de la défausse (les 3 dernières défaussées), sans
rien demander. Aucune carte officielle ne porte cette phrase (vérifié dans
`data/cards.json`).

1. **Le joueur choisit les 3 cartes (recommandé).** En jeu : Dazzler remet
   dans son deck les cartes qu'elle veut revoir (ses meilleures chansons, un
   allié clé). Lecture habituelle des cartes qui désignent des cartes de SA
   défausse sans préciser lesquelles.
2. **Les 3 du dessus de la défausse (code actuel).** En jeu : ce sont toujours
   les 3 dernières cartes défaussées, souvent des ressources dépensées ce
   tour-ci ; aucune décision pour le joueur.
3. **3 cartes au hasard.** En jeu : effet imprévisible, ni choix ni contrôle.
4. Autre (préciser).

Ce que la réponse change dans le code : `dz012.py`, fonction `showtime`
(sélection des 3 cartes). Avec moins de 3 cartes en défausse, toutes partent
dans les trois lectures.

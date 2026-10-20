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

---

## Q2. dz016 « Sound Collector Suit » : quand peut-on « retirer 1 compteur sound » ?

Texte imprimé : « **Resource**: Exhaust Sound Collector Suit → generate a
[energy] resource for a [[SONG]] **or** remove 1 sound counter from a
[[SONG]] in the Setlist. »

Les deux branches sont écrites sous un type « **Resource** ». Une capacité
Resource ne se déclenche qu'au moment de payer un coût ; or la seconde branche
ne produit aucune ressource. Le code actuel en fait une **Action** séparée
(type « Action », jouable dans les deux formes, à n'importe quel moment du
tour du joueur, hors de tout paiement).

1. **Seulement pendant un paiement (recommandé, lecture littérale du type
   Resource).** En jeu : en payant n'importe quelle carte, Dazzler peut
   incliner la combinaison et, au lieu de produire l'énergie, effacer un
   compteur sound. Impossible au milieu de son tour sans rien payer.
2. **Action à tout moment du tour (code actuel).** En jeu : Dazzler
   efface un compteur quand elle veut pendant son tour, sans rien payer, puis
   peut répéter (Rehearsal) la chanson tout de suite.
3. **Seulement pendant le paiement d'une carte [[SONG]].** En jeu : comme 1,
   mais réservé au paiement d'une chanson (« for a SONG » s'appliquerait aux
   deux branches).
4. Autre (préciser).

Ce que la réponse change dans le code : `dz016.py` (la seconde capacité :
Action aujourd'hui ; branche d'une capacité de ressource sinon, ce qui
demande peut-être une extension du moteur, puisqu'une carte ne peut porter
qu'UNE `CanGenerateResources`).

---

## Q3. dz021 « Solid Sound Body » : quel « Klaw » reçoit +10 PV et la carte de boost ?

Texte imprimé : « Klaw gets +10 hit points. *(When this scheme is defeated,
Klaw loses those hit points.)* **When Defeated**: Give Klaw a facedown boost
card. »

Le complot vient du set némésis de Dazzler, dont le sbire s'appelle Klaw
(`dz020`). Mais le scénario officiel « Klaw » (boîte de base) a un VILAIN qui
s'appelle aussi Klaw. Contre ce scénario, les deux sont en jeu en même temps.
Le code actuel cherche par le nom : le bonus +10 PV s'applique à **toute**
carte « Klaw » en jeu (le vilain compris), et la carte de boost va au
**premier** Klaw trouvé (sbire ou vilain, selon l'ordre interne).

1. **Seulement le sbire Klaw du set némésis (recommandé).** En jeu : contre le
   scénario Klaw, le vilain garde ses PV normaux ; seul le sbire némésis devient
   un mur de 16 PV, et c'est lui qui reçoit la carte de boost.
2. **Tous les « Klaw » en jeu (code actuel pour les PV).** En jeu : contre le
   scénario Klaw, le vilain prend aussi +10 PV tant que le complot est en jeu,
   ce qui rallonge beaucoup la partie ; la carte de boost va à l'un des deux.
3. **Le vilain Klaw s'il est en jeu, sinon le sbire.** En jeu : le complot
   renforce le vilain du scénario Klaw, et le sbire némésis dans tous les
   autres scénarios.
4. Autre (préciser).

Hors scénario Klaw (cas le plus courant), les trois lectures donnent le même
résultat. Ce que la réponse change dans le code : `dz021.py`
(`CardFinder(name="Klaw")` et `FindCardOnField(name="Klaw")`).

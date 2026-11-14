# Backlog 12 : questions (vérification des cartes hors irefrixs, pack Dazzler)

> **CLOSES le 20/10/2026** : l'utilisateur a répondu aux cinq questions
> (relais du coordinateur). Chaque réponse est codée, avec ses cas
> `[dazzler] ... (Qn)` dans `tools/cas/dazzler.py`, rouges sans le correctif.
> Détail sous chaque question (« Réponse »).

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

**Réponse (20/10/2026) : option 1, le joueur choisit les 3 cartes** (moins de
3 : toutes partent). Codé dans `dz012.py` (trois choix successifs) ; cas
« le JOUEUR choisit les 3 cartes de la defausse (Q1) », rouge avec l'ancien
code (la carte du dessus partait).

---

## Q2. dz016 « Sound Collector Suit » : quand peut-on « retirer 1 compteur sound » ?

Texte imprimé : « **Resource**: Exhaust Sound Collector Suit → generate a
[energy] resource for a [[SONG]] **or** remove 1 sound counter from a
[[SONG]] in the Setlist. »

Les deux branches sont écrites sous un type « **Resource** ». Une capacité
Resource ne se déclenche qu'au moment de payer un coût (Rules Reference v1.8,
RESOURCE ABILITY : « A resource ability can be triggered anytime the player
who controls the ability is generating resources to pay a cost » ; et « A
resource ability that generates a resource only for a specific type of cost
cannot be triggered when paying a cost not of that type ») ; or la seconde
branche ne produit aucune ressource. Le code actuel en fait une **Action** séparée
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

**Réponse (20/10/2026) : option 1, seulement pendant un paiement.** Codé
dans `dz016.py` : la seconde branche n'est plus une Action mais une Réponse
au message de paiement `AfterCardsBeSpendAsResource` (incliner la
combinaison, effacer un compteur). **Écart assumé**, faute de pouvoir porter
deux `CanGenerateResources` ou une ressource nulle (`assert res.val > 0`) :
la fenêtre n'existe que si au moins une ressource a été dépensée, et elle
arrive juste après la dépense. Cas « PENDANT un paiement » et « HORS
paiement, pas d'Action » (Q2), rouges avec l'ancien code.

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

---

**Réponse (20/10/2026) : option 2, tous les « Klaw » en jeu** (comportement
actuel) ; la carte de boost va au premier Klaw trouvé. Aucun code changé.
Cas « contre le scenario Klaw, le vilain Klaw gagne aussi +10 PV (Q3) ».
Constat : le sbire némésis « * Klaw » ne peut PAS entrer en jeu à côté du
vilain « * Klaw » (unicité de même titre, refus du moteur) : contre ce
scénario, seul le vilain est concerné.

---

## Q4. dz031 « Tribute » : que veut dire « Tribute becomes a copy of that card » ?

Texte imprimé : « Limit 1 per deck. **Hero Action**: After you play Tribute
from your hand, choose 1 non-identity event in your collection. Tribute
becomes a copy of that card, *(except for its cost)* but keeps the [[SONG]]
trait, until it is placed in the discard pile. »

Le module actuel ne rend PAS la copie : il fabrique l'événement choisi, le met
en main et tente de le JOUER gratuitement ; Tribute part ensuite dans la
Setlist sous son propre nom. Écarts constatés au harnais le 20/10/2026 : le
pilote a choisi `01052` Chase Them Down (une **Response**), qui ne peut pas
être jouée en Action et **reste dans la main** : le joueur gagne une carte
venue de nulle part. La fabrique ne montre pas non plus les cartes proposées
(`Search.Collection` / `AskChoosePaper`, RECETTES §2). Le moteur ne sait pas
aujourd'hui changer l'identité d'une carte : la lecture fidèle demande une
extension du moteur.

Points que le texte ne tranche pas :

- quand la copie est un événement à **Interrupt/Response** (« When... »,
  « After... »), à quel moment se résout-elle, puisque Tribute est jouée
  comme Hero Action ?
- une fois copie, Tribute est-elle rangée dans la **Setlist** (elle garde
  [[SONG]]) avec le **Showtime!** de la carte copiée s'il en a un ?

1. **Copie vraie, limitée aux événements jouables tout de suite en Action /
   Hero Action (recommandé).** En jeu : le joueur choisit (en voyant les
   cartes) un événement d'action, Tribute en résout l'effet sans payer son
   coût, garde [[SONG]], entre dans la Setlist en étant toujours cette copie
   (donc avec son Showtime! si elle en a un), et redevient Tribute en
   défausse. Aucune carte n'apparaît en main. Demande une extension du moteur.
2. **Copie vraie, tout événement non-identité.** En jeu : comme 1, mais un
   événement à Interrupt/Response peut être choisi ; il faudrait alors dire
   s'il se résout aussitôt (en ignorant son déclencheur) ou s'il est perdu.
3. **Lecture actuelle corrigée a minima.** En jeu : l'événement choisi est
   résolu gratuitement s'il est jouable en Action, puis la carte fabriquée
   disparaît (retirée de la partie) ; Tribute va dans la Setlist sous son
   propre nom, sans Showtime!. Pas d'extension du moteur.
4. Autre (préciser).

Ce que la réponse change dans le code : `dz031.py` en entier, et pour 1 et 2
un mécanisme moteur de « carte qui devient la copie d'une autre » (face
temporaire portant le nom, le texte, les capacités et les traits de la carte
copiée, plus [[SONG]], jusqu'à l'entrée en défausse).

---

**Réponse (20/10/2026) : option 1, vraie copie limitée aux événements
jouables tout de suite en Action / Hero Action.** Codé sans toucher au moteur
commun : `Card.SwapCardFace` donne à Tribute la face de la carte choisie
(plus [[SONG]]) et `Card.CheckIfCanDiscard` la remet sur sa face imprimée à
l'entrée en défausse (`DevenirCopie`, `dazzler/__init__.py`) ; choix en
voyant les cartes (`AskChooseFace`, modèle Cameo 58031), les événements de
classe Hero (identité) exclus ; Live Concert range la copie dans la Setlist.
Cas (Q4) : copie résolue et rangée (rouge avec l'ancien code), Response non
proposée (rouge), retour à Tribute en défausse (vert aussi avec l'ancien
code : contre-cas). Reste non codé : « from your HAND » (Tribute jouée
depuis Lightbringr déclenche aussi la copie).

---

## Q5. dz035 « Karaoke Night » : une Hero Action à COÛT (« X → Y ») résolue depuis la Setlist

Texte imprimé : « **Action**: Exhaust Karaoke Night and choose a [[SONG]] in
the Setlist → resolve the '**Hero Action**' of that card. Discard that card. »

Une seule chanson du pack a une Hero Action avec un coût avant la flèche :
`dz026` Song of Leadership, « Exhaust an ally → heal damage from that ally
equal to the amount of [[SONG]] cards in your discard pile ». Le texte de
Karaoke Night ne dit pas si ce coût se paie. Le code actuel passe par le
chemin du moteur qui résout l'EFFET sans payer le coût : aucun allié n'est
incliné, donc « that ally » n'existe pas et rien n'est soigné (la chanson est
quand même défaussée).

1. **Le coût se paie (recommandé).** En jeu : Karaoke Night sur Song of
   Leadership demande d'incliner un allié, qui est ensuite soigné ; sans allié
   prêt, ce choix n'est pas proposé.
2. **Le coût est ignoré, l'effet s'applique à un allié choisi.** En jeu :
   le joueur choisit un allié (même incliné), qui est soigné sans être
   incliné.
3. **Comportement actuel : la chanson part sans effet.** En jeu : choisir
   Song of Leadership avec Karaoke Night ne sert qu'à la défausser.
4. Autre (préciser).

Les autres chansons (aucune flèche) ne sont pas concernées. Ce que la réponse
change dans le code : `dz035.py` (et peut-être `dz026.py`, pour lire l'allié
choisi hors paiement).

**Réponse (20/10/2026) : option 1, le coût se paie.** Codé dans `dz035.py` :
la Hero Action est résolue par `EffectInvoker.ResolveSelfInternal(...,
skip_cost=False)` ; une chanson au coût impayable n'est pas proposée (et
l'Action n'est pas offerte si aucune ne l'est). Cas (Q5) : Song of
Leadership incline puis soigne l'allié ; sans allié prêt, rien n'est proposé
(les deux rouges avec l'ancien code).

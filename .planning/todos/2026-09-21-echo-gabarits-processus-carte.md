# PROCESSUS-CARTE.md — les 4 gabarits d'ECHO touchés le 21/09/2026

Gate de `CLAUDE.md` : rien n'est terminé sans le gabarit rempli, preuve à
l'appui. Rédigés le 21/09/2026, à la suite du signalement n°17 (Yarro) et de la
conclusion de l'observation en suspens.

**Portée.** Ce ne sont pas quatre cartes neuves : ce sont les quatre cartes du
set `fne/echo` que ce chantier a modifiées. Les autres cartes du set (`60039`,
`60041`-`60047`, `60060`) n'ont pas été touchées et gardent leur statut
antérieur.

Rapport complet : `.planning/rapports/2026-09-21-echo-conclusion.md`.

> **MISE À JOUR DU 20/10/2026 (backlog 13, branche `backlog-13-reserves`).**
> Les deux manques communs sont comblés :
>
> - **Étape 8 bis : FAITE pour 60040a/b/c.** Cas moteur
>   « 60040a 60040b 60040c Photographic Reflexes — etape 8 bis : ce que le
>   moteur ENVOIE au plateau (monde + options) » (vérificateur
>   `echo_rendu_pour_le_plateau`) : il prend le descripteur du monde
>   (`ToDescriptor.World`, ce que sert `/get_world`) et celui des options
>   (`Effect.Render`, ce que sert `/get_ask`) et les écrit en fixture
>   (`ui-app/src/board/__fixtures__/echo-photographic-reflexes.json`). Le cas
>   plateau `ui-app/src/board/echo-photographic-reflexes-plateau.test.ts`
>   (6 cas) relit cette fixture et affirme : les trois variantes dessinées en
>   main, Haymaker glissé dessiné SOUS Echo (`portePar` = Echo, face cachée
>   lisible par son propriétaire), chaque variante CLIQUABLE (rôle `porteur`),
>   le clic en mode Détaillé choisit l'action de LA variante cliquée, Haymaker
>   glissé cliquable à coût 0. **Vu ROUGE** : fixture régénérée avec le module
>   `60040a` remplacé par un module vide (`substituer_pack.py`) →
>   « carte 9: expected undefined to be 'porteur' » ; fixture d'origine
>   remise → 6/6.
> - **Étape 8 : FAITE.** `autoplay.py` deck `echo` contre Rhino, 8 parties
>   (71 s), 0 partie bloquée, 5,2 rounds en moyenne ; témoin `spider_man`,
>   8 parties, 0 bloquée, 6,9 rounds. Grep `NameError|AttributeError|
>   TypeError|KeyError|AssertionError|Traceback` sur les 16 journaux : 0
>   partout. Journaux lus pour les cartes du chantier : Watch and Learn part
>   dans les 8 parties, le chemin B (« Discard_a_Photographic_Reflexes ») dans
>   5, le chemin A (action en main) dans 2. Écart de rounds avec le témoin :
>   Echo est éliminée plus tôt (6 éliminations sur 8 contre 4), pas de
>   blocage.
> - **Trouvé en lisant le journal** (graine 4, lignes 297 à 305) : le chemin A
>   est offert quand l'événement glissé n'est PAS payable ; Photographic
>   Reflexes est alors défaussée pour rien (reproduit au harnais). Le chemin B
>   refuse, lui, dans la même position. **Doute de règle, non tranché** :
>   question Q1 de `.planning/todos/2026-10-20-backlog-13-questions.md`.

**Preuves communes**, citées une fois :

- **Étape 7, cas** : `tools/test_capacites.py`, filtres `Echo — ` et
  `Photographic Reflexes — ` → **17 témoins d'Echo, 17 verts**.
- **Batterie complète** : `PARALLELES=12` sur un dossier jetable — voir le §6
  du rapport pour le détail et les rouges antérieurs.
- **Étape 1** : aucune entrée `cards.json` touchée. Les textes ont été
  **relus** contre MarvelCDB (`/card/60037a`, `/card/60040a`, `/card/60040b`) :
  identiques au mot près, y compris le `[star]` et le `Cost: -1` des trois
  variantes.
- **Étape 4, image** : inchangée, les quatre cartes avaient déjà la leur.
- **Étape 8** : **PAS FAITE.** Pas d'autoplay ciblé sur le deck d'Echo, faute
  de temps machine. Dit noir sur blanc, ici et au rapport.
  *Faite le 20/10/2026, voir la mise à jour en tête.*
- **Étape 8 bis** : **PAS FAITE** pour le chemin A. Voir le gabarit `60040a`.
  *Faite le 20/10/2026, voir la mise à jour en tête.*

---

## 60037a : * Echo (face héros)

- [x] **Étape 2 : cartes de référence**
      *Watch and Learn* (inchangée) : `su012` Contingency Plan pour la zone
      glissée. *Rafraîchissement du cache* : `aoa/magik/45030a.py`, qui remet
      `can_state.is_like_in_hand` à `None` à la main sur le dessus de son deck —
      **même piège, même remède**, et c'est la seule autre carte du dépôt qui
      l'avait déjà payé. *Réduction de coût* : `dz014` Lightbringr et `aa002`
      Scarlet Witch, qui portent **la même phrase imprimée** (« Reduce the cost
      ... by N ») et la rendent par `WhenCalculateEffectCost` + `UpdateCost`.

- [x] **Étape 5 : texte-contre-code, mots-pièges**
      - `a player` (« After **a player** plays ») : `'AnyPlayer'`, donc
        l'événement d'un autre joueur se glisse aussi. **Non testé** en
        multijoueur (voir les réserves).
      - `that event` : c'est bien `message.played_face`, la carte nommée plus
        haut, pas une autre.
      - `from that player's discard pile` : garde
        `face.card.area.flags.is_discards or face.IsInProcessingArea()`. La
        seconde branche est une concession de timing (la Response part pendant
        que l'événement est encore en résolution) ; conséquence assumée : un
        événement qui ne finit PAS en défausse (retiré du jeu, rendu en main)
        serait tout de même glissé. **Écart connu, non corrigé.**
      - `more than 3` / `all but 3` : `excess = len(placed) - 3`, choix de
        `excess` cartes exactement.
      - `If you are in hero form` : `initiator.IsInHeroForm()` —
        **c'est ici que vivait le défaut**, non pas dans la condition, mais dans
        le cache qui figeait sa réponse.
      - `Reduce the cost ... by 2` : **corrigé**, c'était une génération de deux
        wild. Voir l'étape 7.
      - `You cannot trigger ... for that event` :
        `message.from_area != GetPlacedCardArea()`.
      Résultat : **deux écarts trouvés et corrigés, un écart de timing assumé.**

- [x] **Étape 6 : nombres texte ↔ code**
      `3` cartes glissées (`len(placed) - 3`), `2` de réduction
      (`UpdateCost(-2)`). `desc` : HP 9, ATK 2, THW 2, DEF 2, HS 5 — inchangés,
      non touchés par ce chantier. Résultat : **conformes**.

- [x] **Étape 7 : cas par capacité, preuve par substitution**
      - *Watch and Learn, la mise sous Echo* : `l'evenement basique joue est
        glisse sous Echo` — rouge sans le module, vert avec.
      - *Watch and Learn, la limite de 3* : `une 4e carte glissee, on defausse
        jusqu'a 3`.
      - *Watch and Learn, la clause « cannot trigger »* : `ne re-glisse PAS
        l'evenement joue depuis sous Echo`.
      - *La permission, les trois conditions* : `forme HEROS ... est offerte`
        (+ contre-bout défausse), `forme CIVILE ... n'est PAS offerte`,
        `sans Photographic Reflexes ... n'est PAS offerte`.
      - *Le rafraîchissement du cache, les trois crochets* :
        `retour en forme HEROS` (forme, lu à chaque étape),
        `une Photographic Reflexes ARRIVE en main` (`AfterCardEnterHand`),
        `la Photographic Reflexes QUITTE la main`
        (`WhenCardWouldMoveToArea`).
        **Substitution par crochet, pas en bloc** : voir le §5 du rapport.
      - *La réduction de 2* : `chemin B : la carte glissee coute 2 de moins`,
        et surtout `la reduction de 2 NE COUVRE PAS l'exigence de couleur`
        (`28013` No Quarter), **le seul qui distingue une réduction d'une
        génération de wild**. Substitution par **l'ancienne implémentation**,
        pas par le vide.
      Résultat : **chaque capacité a son cas sujet, et chaque correctif a une
      substitution qui le vise lui.**

- [x] **Étape 7 bis : limite imprimée ?**
      **OUI**, « more than 3 tucked cards ». Témoin d'épuisement : `une 4e carte
      glissee, on defausse jusqu'a 3`, quatre événements joués dans le même
      tour, **chiffre mesuré : 3 cartes restantes**, pas une présence.

- [x] **Étape 8 : autoplay ciblé** — FAITE le 20/10/2026 (voir la mise à
      jour en tête) : 8 parties `echo` / `rhino`, témoin `spider_man`
      8 parties, 0 traceback, 0 partie bloquée ; Watch and Learn part dans
      les 8 parties.

- [x] **Étape 8 bis : la carte change-t-elle ce qu'on VOIT ?**
      **OUI** — elle glisse des cartes sous l'identité. Mais c'est du **déjà
      couvert** : `ui-check`/`plateau-de-test` a son cas de chaîne
      d'attachement depuis le 09/09 (`attachement-en-chaine.test.ts`), et la
      zone glissée d'Echo était déjà dessinée avant ce chantier — le joueur du
      signalement VOYAIT ses cartes glissées, c'est même comme ça qu'il les a
      décrites. **Ce chantier ne change rien à ce qui est dessiné pour 60037a.**

**Carte terminée : OUI**, sous la réserve de l'étape 8 (autoplay non fait) et
de l'écart de timing `IsInProcessingArea` ci-dessus, tous deux nommés.
*20/10/2026 : la réserve de l'étape 8 est levée (autoplay fait) ; reste
l'écart de timing `IsInProcessingArea`, nommé.*

---

## 60040a : Photographic Reflexes (variante [energy])

- [x] **Étape 2 : cartes de référence**
      - `an006` Angelic Ribbons et `al014` Lurking : « discard this card → » est
        un **coût**, `CostFunc.Discard("This")`, jamais l'effet.
      - `21185` System Shock et `21032` Pip the Troll : une capacité déclenchée
        **depuis la main** se monte sur `.CanWorkOnlyInHand()`.
      - `16130` Crystal Ball : « may play a card ..., reducing its resource
        cost » → `player.PlayOneCardLikeInTurn`, qui demande **laquelle** puis
        la joue en payant vraiment.
      - `al015`/`al016` : le précédent des variantes qui ne diffèrent que par
        l'icône de ressource.

- [x] **Étape 5 : texte-contre-code, mots-pièges**
      - `If you are in hero form` : porté par `AbilityType.HeroAction`
        (`GetAbilityTypeCondition` → `GetInitiator().IsHero()`).
      - `you can discard ... from your hand` : `CostFunc.Discard("This")` +
        `CanWorkOnlyInHand()`. **`discard` ≠ `play`** : la carte n'est pas
        jouée, donc aucun « after you play an event » ne part pour elle.
        Arbitrage annoncé au §3b du rapport.
      - `to play an event tucked under Echo` : `PlayOneCardLikeInTurn` sur les
        seuls `Event` de la zone glissée. S'il n'y en a aucun, la carte
        **n'offre pas l'action** (condition `il_y_a_un_evenement_glisse`) — sans
        quoi on recréait le défaut signalé sous une autre forme.
      - `as if it were in your hand` : c'est `PlayCardsLikeInTurn` qui le porte.
      - `Reduce the cost ... by 2` : **volontairement pas ici**, mais sur Echo,
        pour que les chemins A et B paient la même chose et qu'une seconde copie
        en main ne double pas la réduction.
      - `You cannot trigger ... for that event` : porté par Echo
        (`check_aspect_event`), et donc valable **sur les deux chemins**.
      - **Un mot-piège que le texte NE porte pas** : rien ne dit « once per
        round », rien ne dit « choose one ». Aucune limite n'a été inventée.
      Résultat : **conforme, avec un arbitrage nommé (la défausse est un coût).**

- [x] **Étape 6 : nombres texte ↔ code**
      `Cost: -1` = `[star]`, donc aucun coût en ressources : l'action n'en
      déclare pas. `RES: Y` pour cette variante. `2` de réduction, porté par
      Echo. Résultat : **conformes**.

- [x] **Étape 7 : cas par capacité, preuve par substitution**
      Une seule capacité, quatre cas sujets :
      `chemin A : on clique la carte EN MAIN, elle joue l'evenement glisse`,
      `forme HEROS avec un evenement glisse : l'action EST offerte`,
      `aucune carte glissee : la carte n'offre AUCUNE action`,
      `forme CIVILE : la carte n'offre AUCUNE action`.
      Substitution (module vidé, `return []`) : **3 rouges sur 6**.
      ⚠ **Les deux contre-cas d'ABSENCE restent verts sous substitution** :
      c'est assumé, pas maquillé, comme l'exige l'étape 7.3 ; c'est le cas
      positif qui les rend discriminants.
      ⚠ **Et le cas `forme CIVILE` ne discrimine pas la clause de forme** :
      voir le §5 du rapport, il passerait sans elle.

- [x] **Étape 7 bis : limite imprimée ?** **NON.** Aucune.

- [x] **Étape 8 : autoplay ciblé** — FAITE le 20/10/2026, même fournée que
      60037a ; le chemin A (action en main) part dans 2 parties sur 8.

- [x] **Étape 8 bis : la carte change-t-elle ce qu'on VOIT ?** FAITE le
      20/10/2026 : cas plateau
      `ui-app/src/board/echo-photographic-reflexes-plateau.test.ts`, sur une
      fixture produite par le moteur (cas « etape 8 bis : ce que le moteur
      ENVOIE au plateau »). Vu ROUGE avec le module `60040a` vidé (« carte 9:
      expected undefined to be 'porteur' »), vert 6/6 avec. ⚠ Il n'y a pas eu
      de correctif côté plateau : le dessin et le clic étaient déjà justes, le
      rouge prouve que le cas DISCRIMINE, pas qu'un défaut a été réparé.
      Texte d'origine de cette case, conservé :
      **OUI, ET C'EST LE POINT FAIBLE DE CE CHANTIER.** La carte devient
      cliquable en main : c'est une **action portée par une carte de la main**,
      une forme que `ui-app` n'a jamais eu à dessiner pour Echo.
      `test_capacites` prouve que le moteur l'offre (`60040a action=True`) ; il
      ne prouve **rien** sur le bouton. Ce qui manque précisément : un cas
      `plateau-de-test` qui pose une main contenant `60040a` avec une carte
      glissée sous Echo en forme héros, et affirme que l'action est rendue.
      **Vu ROUGE sans le correctif : non, le cas n'existe pas.**

**Carte terminée : NON.** Ce qui manque : l'étape 8 bis (rien ne garantit que
le geste soit visible à l'écran) et l'étape 8. Le moteur est juste et mesuré ;
l'écran ne l'est pas.

*20/10/2026, plus tard : Q1 TRANCHÉE par l'utilisateur* (« retirer le geste
quand aucun événement glissé n'est jouable ou payable après la réduction de
2 »). Correctif dans `fne/echo/__init__.py` : `il_y_a_un_evenement_glisse`
pose la question du chemin B (`FilterAvailableEffects` sur le « Play » de
chaque carte glissée) PUIS vérifie le paiement (`JeuPayableSans` : somme des
moyens listés, une entrée par carte payeuse, la Photographic Reflexes cliquée
écartée), car l'offre du moteur ne vérifie jamais le paiement. Corollaire :
la garde du 25/09 laisse une SECONDE copie payer sur le chemin A (la copie
cliquée est déjà partie en coût). Trois cas sujets, vus ROUGES avant le
correctif : « chemin A ABSENT quand l'evenement glisse n'est pas payable »
(« action OFFERTE, attendu absente »), « chemin A avec DEUX copies »
(« cartes glissees ['18020'], attendu [] »), et le témoin « chemin A PRESENT
et joue des que l'evenement glisse est payable » (vert avant et après).
Filtre `6004` : 16/16 ; filtre `Echo` : 18/18 ; fixture du plateau inchangée
(régénérée, identique) ; autoplay echo/rhino rejoué, 8 parties, 0 traceback,
plus aucune « Cancel » après une Photographic Reflexes (graine 4 réglée).
**Carte terminée : OUI** (60040a, et 60040b / 60040c par le même
constructeur).

*Texte du premier passage du 20/10, conservé :* **Carte terminée : NON**,
pour une seule raison nouvelle : le chemin A est offert
quand aucun événement glissé n'est payable, et la carte est alors défaussée
pour rien (autoplay graine 4, reproduit au harnais). C'est un doute de règle,
posé en Q1 de `.planning/todos/2026-10-20-backlog-13-questions.md` ; la carte
passera à OUI avec le cas sujet de l'option retenue. Non vu en navigateur :
la capture d'écran réelle n'a pas pu être faite (copie du client compilé dans
le dossier du jeu refusée par la permission « déploiement ») ; le cas plateau
s'arrête au calcul de ce qui est dessiné et cliquable, pas aux pixels.

---

## 60040b : Photographic Reflexes (variante [mental])

- [x] **Étape 2** : identique à `60040a`, plus `al015` (variante sans module
      propre) pour le principe « même texte, icône différente ».
- [x] **Étape 5** : **même texte au mot près que `60040a`**, vérifié sur
      MarvelCDB et dans `cards.json`. Le module appelle le constructeur commun
      `AbilitesPhotographicReflexes` : il n'y a pas de seconde lecture possible,
      donc pas de second écart possible.
- [x] **Étape 6** : `Cost: -1`, `RES: B` — **la seule différence**, et elle est
      dans `desc`, pas dans le code.
- [x] **Étape 7** : cas sujet **nominatif** :
      `60040b ... trois variantes en main : c'est CELLE qu'on clique qui part`,
      qui vérifie que `60040a` et `60040c` sont **encore en main**. C'est lui qui
      a attrapé le défaut de double défausse (§3c du rapport). Substitution :
      rouge sans le module.
- [x] **Étape 7 bis** : pas de limite imprimée.
- [x] **Étape 8 / 8 bis** : faites le 20/10/2026, comme `60040a`. Le cas
      moteur de l'étape 8 bis tombe ROUGE avec le module `60040b` vidé
      (« 60040b en main : aucune option rendue sur son objet 11 »,
      `substituer_pack.py` : rouges 2/2).

**Carte terminée : NON**, pour la même raison que `60040a` (étape 8 bis).
*20/10/2026 : Q1 tranchée et corrigée (voir `60040a`).* **Carte terminée :
OUI.**

---

## 60040c : Photographic Reflexes (variante [physical])

- [x] **Étape 2 / 5** : identiques à `60040b`.
- [x] **Étape 6** : `Cost: -1`, `RES: R`.
- [x] **Étape 7** : couverte par le cas des trois variantes, qui exige que
      `60040c` **reste en main** quand on clique `60040b` — donc la carte est
      bien chargée, distincte, et non consommée par erreur.
      ⚠ **Réserve honnête** : aucun cas ne clique `60040c` elle-même. Les trois
      modules appelant le même constructeur, le risque est celui d'un module mal
      branché, pas d'un comportement différent ; et le cas des trois variantes
      l'attraperait.
- [x] **Étape 7 bis** : pas de limite imprimée.
- [x] **Étape 8 / 8 bis** : faites le 20/10/2026, comme `60040a`. La réserve
      « aucun cas ne clique 60040c elle-même » est en partie levée : le cas
      moteur de l'étape 8 bis exige une option portée par l'objet de `60040c`
      et tombe ROUGE avec son module vidé (« 60040c en main : aucune option
      rendue sur son objet 13 », rouges 1/1).

**Carte terminée : NON**, pour la même raison.
*20/10/2026 : Q1 tranchée et corrigée (voir `60040a`).* **Carte terminée :
OUI.**

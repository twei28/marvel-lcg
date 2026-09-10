# Iron Patriot (Neptune, set 142) — gabarits PROCESSUS-CARTE, 39 faces

**Livré le 10/09/2026.** Préfixe `ip`. Pack de HÉROS complet : identité recto
verso, 16 cartes de set héros, 1 obligation, un set némésis de 5 cartes, un set
de rencontre modulaire « Molecule Man » de 6 cartes, et surtout un **second
deck de 20 sbires**, le deck REGISTERED. `PROCESSUS-HEROS.md` s'applique, donc
`PROCESSUS-CARTE.md` 39 fois.

## Ce qui a été mesuré, et comment

| Gate | Résultat | Calibrage (§9) |
|---|---|---|
| `tools/verifier_prefixes.py` | OK, 0 doublon, 39 cartes sous `ip` | — |
| `tools/verifier_appels_modules.py iron_patriot` | OK, tous les appels existent | ✅ vu ROUGE 4 fois en cours de route (`unite.DoAttack`, `AbilityFactory.AfterVillainPhaseBegin`, `UnitSchemeDivideThreatAmongEachScheme`, `this.BasicAttack` sur un `Unit2`) |
| `tools/verifier_desc_mots_cles.py iron_patriot` | OK, 40/40 | — |
| `tools/test_cards.py` | 5468 cartes construites, 0 erreur | ✅ vu ROUGE : `AbilityType.Constant` (inexistant), `*` sur une `Ability` seule, `assert selectors == []` sur les sbires |
| `tools/verifier_tous_les_decks.py` (`DECK_NOM=iron_patriot`) | OK, « identité ip001a, main 6, deck 35 » | ✅ vu ROUGE 6 fois : obligation sans `GiveTo`, `PlayerSideScheme` sans `HasPermanent`/`HasSetup`, événement à deux capacités Play, `CardFinder(trait=…)` sans `card_type`… |
| `tools/test_capacites.py` filtre `ip0` | **75/75** | ✅ chaque cas a été vu ROUGE avant son correctif ; 5 défauts réels trouvés par eux (voir ci-dessous) |
| `tools/test_capacites.py` batterie COMPLÈTE | **1724/1728** — les 4 rouges sont ceux de Squirrel Girl, connus et documentés depuis le 31/08/2026 (`.planning/todos/2026-08-31-cas-rouges-sg-ss.md`) | — |
| `tools/autoplay.py` | 16 parties (Rhino et Klaw, normal, profil équilibré), **0 traceback** sur les 16 journaux | ✅ vu ROUGE : 4 défauts réels au premier passage, corrigés (voir ci-dessous) |
| `ui-app` : `tsc` + 1214 tests | vert | ✅ `textes-fr-fanmade.test.ts` vu ROUGE sur 8 cartes (« Quand elle est révélée » au lieu de « Une fois révélée ») |
| Cas plateau `deck-registered.test.ts` | 5/5 | ✅ `sousArbre` renvoyant `[]` → 2 cas rouges |

## Ce qui a été trouvé en chemin

**Cinq défauts RÉELS, tous trouvés par les cas, aucun par relecture.**

1. **`ip002a` Registration Act se faisait défausser à chaque partie.** Elle
   imprime « This scheme does not count against the player side scheme limit »,
   et cette phrase avait d'abord été classée « règle d'éditeur, non codée ».
   Faux : le moniteur `world/limit_monitor/player_side_scheme_limit.py` compte
   les manigances de joueur EN JEU. Registration Act mangeait l'unique place, et
   `ip003` Absolute Power était défaussée dans le souffle où elle entrait
   (journal : « entered play » puis « was discarded », deux lignes). Corrigé par
   le drapeau `not_count_player_side_scheme_limit`, posé À L'ENTRÉE EN JEU (pas
   au setup : une carte `desc.Setup` n'a jamais cette fenêtre).
2. **Le « Special » payé disparaissait au moment où on le payait.**
   `Faces.TreatAsAlly` ÉCHANGE la face du sbire contre celle du gabarit
   `registered_ally`, qui n'a aucune capacité. Trois correctifs successifs, tous
   mesurés : recharger le module pour obtenir des `Ability` neuves (celles en
   place sont liées à leur papier, `card.py:316`), recopier les traits imprimés
   (sans quoi `ip021` Suppressive Fire comptait 0 personnage H.A.M.M.E.R.), et
   rallumer les bonus continus (`WhileValid` se suspend à `WhenCardEnterPlay`,
   qui est déjà passé quand on inscrit).
3. **Convertir pendant le « When Revealed » cassait la révélation**
   (`assert self.engaged_player=None`, `minion.py:41`). Fenêtre décalée sur
   `AfterCardRevealedEnd`.
4. **`ip002a` ne basculait pas sur son verso.** `FlipTo` seul ne suffit pas :
   une manigance vaincue a déjà quitté le terrain. Modèle `40190a` :
   `card.Flip` puis `face.Reveal`.
5. **`ip014` Seige levait `TypeError` en pleine résolution**, APRÈS avoir
   défaussé les alliés : `DealDamage(..., overkill=True)` n'existe pas, c'est
   `property=AttackProperty(overkill=True)`.

**Quatre défauts de plus, trouvés par l'AUTOPLAY et par lui seul.** Les cas
étaient verts quand ils sont sortis : aucun ne joue une carte du pack pendant
qu'elle est encore un SBIRE contrôlé par le scénario, et c'est là que trois
d'entre eux vivaient.

6. **`ip013` Call to Arms perdait sa moitié punitive EN SILENCE.**
   `GainUntilRoundEnd` ne transmettait pas `attack_consequential_damage` /
   `thwart_consequential_damage` à `TemporaryGain`, qui les accepte pourtant
   depuis toujours. Le `TypeError` était avalé par le moteur : le
   `Faces.ReadyAll` qui précède passait, les alliés étaient bien redressés, la
   carte avait l'air de marcher. Quatrième trou du même genre dans cette
   signature après `retaliate`, `villainous`, `stalwart` et `recover`.
7. **`ip031` Loki plantait à chaque traîtrise révélée.** La fabrique
   `AfterYouResolveTreachery` appelle `effect.GetInitiator()` dans sa condition,
   qui AFFIRME que l'initiateur est un joueur (`reveal.py:198`). Loki est
   d'abord un sbire du SCÉNARIO : 26 `AssertionError` sur 8 parties.
8. **`ip028` Taskmaster plantait à chaque recalcul de son bonus**, même cause :
   `GetControlByPlayer()` assère (`card_face.py:972`). D'où le helper
   `JoueurQuiControle`, qui rend `None` au lieu de tomber, et les cinq appels du
   pack passés dessus.
9. **`ip036` Master of Molecules levait `AttributeError` en pleine
   interruption** — `Message.WhenUnitWouldAttack` n'a pas de `GetToPlayer()`
   (la méthode y est même commentée avec un `assert False`) : le joueur visé se
   lit sur `against_player`. L'attaque partait donc SANS la moitié « selon la
   couleur défaussée », c'est-à-dire sans la carte.

**Deux pièges de plateforme, notés pour la suite du dépôt :**

- **`attacker="You"` n'existe pas.** `Condition.CheckWhichCard` connaît
  « This », « YourHero », « YouControlCharacter »… mais pas « You » seul :
  l'assertion `not isinstance(check_rule, Sequence)` tombe (une chaîne EST une
  Sequence) et la condition explose en silence. `ip001a` et `ip011` en
  souffraient.
- **Un ENNEMI ne peut pas porter de `.SetTarget()`** (`ability.py:168`). Les 14
  cartes du deck REGISTERED sont chargées comme des sbires : leurs cibles se
  demandent DANS l'opération, par `joueur.AskChooseFaces`.

**Trois faux verts démasqués et corrigés :**

- `traits_de` n'existait pas dans `etat_attendu` : les cas qui l'écrivaient
  passaient au vert sans rien mesurer. Clé ajoutée.
- `par_id` ne trouvait plus un allié converti (son `card_id` devient
  `registered_ally`) : ajout d'un repli sur `card.printed_faces`, côté harnais
  ET côté `Puzzle.FindOrCreateFace` — qui fabriquait sinon un DOUBLON détaché et
  blessait un fantôme.
- Venom porte RÉSISTANCE : le premier paquet de dégâts d'un cas était mangé par
  la carte Robuste, et le cas mesurait 0. Amorçage ajouté.

## Ce qui n'est PAS fait, et pourquoi

⚠ **« During deck building, your deck cannot include any aspect allies »**
(`ip001b`, et l'insert) n'est pas automatisé. C'est une règle d'ÉDITEUR, pas de
moteur de partie. Le deck de départ de l'auteur la respecte de lui-même : ses
trois alliés — Nick Fury, Yellow Jacket, War Machine — sont tous de classe
Basic.

⚠ **L'étiquette de la zone du deck REGISTERED reste « Deck spécial »** sur le
plateau. Elle se déduit du seul trait COMMUN à toutes les cartes du deck
(`nomDeckSpecial`, `zones.ts:427`) — « Invocation » chez Docteur Strange — et
les 20 sbires n'en ont aucun (H.A.M.M.E.R., ASSASSIN, ASGARD, SYMBIOTE…). Le
deck est bien dessiné, bien consultable, avec sa défausse à côté ; c'est son
titre qui ne dit pas son nom. Cas de garde écrit et vert :
`ui-app/src/board/deck-registered.test.ts`.

⚠⚠ **L'AUTOPLAY PERD LES 16 PARTIES AU ROUND 1, ET C'EST LA CARTE.**
`Enlistment` est une Action **sans coût et sans limite imprimée** : le pilote,
qui prend toute action gratuite, la déclenche jusqu'à 21 fois d'affilée, révèle
21 sbires qu'il ne paie pas, et se noie sous sa propre armée à la phase du
méchant. Les trois profils (prudent, équilibré, agressif) font exactement
pareil. Le scan a été relu à la loupe : **il n'y a aucune limite sur la carte**,
et l'insert le confirme — « Norman can access this deck at any time, the only
limit to bringing them in is your resources ». Le port est donc fidèle ; c'est
le pilote qui ne voit pas le piège. Conséquence à assumer : **l'autoplay ne
prouve ici que l'absence de plantage**, pas l'équilibre, et il n'exerce presque
aucune carte au-delà d'`Enlistment`.

⚠ **Aucune partie humaine dans le navigateur.** Les 46 cas et l'autoplay disent
ce que le moteur FAIT ; le plaisir de jeu et l'équilibre du marché « payer ses
icônes de boost » ne se mesurent qu'à la main.

## Matériel : deux pièges du zip, tranchés

⚠ **Le pack numérote chaque EXEMPLAIRE physique, pas chaque carte.** 53 fichiers
pour 37 cartes distinctes. Mesure par différence de pixels : les fichiers
homonymes ne diffèrent que sur le bandeau du numéro (1,8 % de la hauteur).

⚠ **Sauf `(06)` et `(6)` H.A.M.M.E.R. Helicarrier**, qui portent le même numéro
imprimé et diffèrent sur 96 % de l'image : deux VERSIONS du texte, « Action » et
« Response ». On retient l'ACTION — un « Response » sans clause « After… » n'est
pas une Réponse valide, et le fichier suit la numérotation zéro-padée du
dossier.

⚠ **La carte « Starter Deck » de l'auteur a trois écarts** avec le matériel
imprimé, tous tranchés en faveur du matériel (numérotation décalée, Total
Authority absente du texte mais présente au rang 16, « Cabal Machination's »
pour « Cabal Obligations »). Détail dans `deck/starter/iron_patriot.json`.

---

### ip001a : Iron Patriot

- [x] Étape 2 : carte(s) de référence : `06009`, `ab011`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip001a Iron Patriot — chaque allie qu'il controle gagne le trait REGISTERED
      • ip001a Authoritative Force — le sbire vaincu a l'attaque part dans le deck REGISTERED
      • ip001a Authoritative Force — TEMOIN : le SECOND sbire de la phase n'y va PAS
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? **OUI**. Témoin d'épuisement écrit et vert :
      • ip001a Authoritative Force — TEMOIN : le SECOND sbire de la phase n'y va PAS
      Résultat : le second déclenchement est bien REFUSÉ
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip001b : Norman Osborn

- [x] Étape 2 : carte(s) de référence : `09001b`, `58031`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip001b Norman Osborn — le deck REGISTERED est monte au setup : 20 sbires
      • ip001b Norman Osborn — l'Action resout le « Special » d'un allie REGISTERED
      • ip001b Norman Osborn — l'allie REGISTERED vaincu rentre dans la DEFAUSSE REGISTERED
      • ip001b Norman Osborn — le sbire NON recrute part en defausse de RENCONTRE
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? **OUI** — voir `ui-app/src/board/deck-registered.test.ts`, 5/5, calibré §9.
      Résultat : OK

**Carte terminée : OUI**

### ip002a : Registration Act

- [x] Étape 2 : carte(s) de référence : `09001b`, `ip001b`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip002a Registration Act — Enlistment revele le dessus du deck REGISTERED et le met en jeu
      • ip002a + ip020 — TEMOIN : la DEUXIEME revelation du round ne donne PLUS d'allie
      • ip002a Registration Act — vaincue, elle BASCULE sur Dark Reign (ip002b)
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? **OUI** — voir `ui-app/src/board/deck-registered.test.ts`, 5/5, calibré §9.
      Résultat : OK

**Carte terminée : OUI**

### ip002b : Dark Reign

- [x] Étape 2 : carte(s) de référence : `ip002a`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip002a Registration Act — vaincue, elle BASCULE sur Dark Reign (ip002b)
      • ip002b Dark Reign — Accept Change revele le dessus du deck REGISTERED
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? **OUI** — voir `ui-app/src/board/deck-registered.test.ts`, 5/5, calibré §9.
      Résultat : OK

**Carte terminée : OUI**

### ip003 : Absolute Power

- [x] Étape 2 : carte(s) de référence : `40006`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip003 Absolute Power — un heros ne peut PAS retirer de menace de cette manigance
      • ip003 Absolute Power — l'Action retire 1 menace en inclinant un personnage REGISTERED
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip004 : Corrupt Absolutely

- [x] Étape 2 : carte(s) de référence : `ip003`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip004 Corrupt Absolutely — un heros ne peut PAS retirer de menace non plus
      • ip004 Corrupt Absolutely — l'Action d'alter ego retire 1 menace elle aussi
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip005 : Sentry

- [x] Étape 2 : carte(s) de référence : `32017`, `45031`, `bl006`, `dd003`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip005 Sentry — le « Special » Void's Wrath donne riposte X = son ATQ (4)
      • ip005 Sentry — il defend a la place du heros SANS s'incliner
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip006 : Victoria Hand

- [x] Étape 2 : carte(s) de référence : `ag004`, `ip001b`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip006 Victoria Hand — elle regarde le dessus du deck REGISTERED et le defausse
      • ip006 Victoria Hand — deck REGISTERED VIDE, la seule option restante recycle un sbire
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip007 : H.A.M.M.E.R. Helicarrier

- [x] Étape 2 : carte(s) de référence : `03024`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip007 H.A.M.M.E.R. Helicarrier — la limite d'allies passe de 3 a 4
      • ip007 H.A.M.M.E.R. Helicarrier — l'Action redresse un allie REGISTERED
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip008 : Director of Security

- [x] Étape 2 : carte(s) de référence : `15009`, `as015`, `bt014`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip008 Director of Security — la premiere carte revelee du round perd 1 icone de boost
      • ip008 Director of Security — TEMOIN : la DEUXIEME carte du round garde ses icones
      • ip008 Director of Security — la Ressource d'alter ego produit bien une ressource
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? **OUI**. Témoin d'épuisement écrit et vert :
      • ip008 Director of Security — TEMOIN : la DEUXIEME carte du round garde ses icones
      Résultat : le second déclenchement est bien REFUSÉ
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip009 : Total Authority

- [x] Étape 2 : carte(s) de référence : `40049`, `ip001b`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip009 Total Authority — Iron Patriot gagne stable
      • ip009 Total Authority — apres un pouvoir de base, elle resout un « Special »
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip010 : Deceptive Guard

- [x] Étape 2 : carte(s) de référence : `21061`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip010 Deceptive Guard — l'interruption de heros empeche TOUS les degats d'une attaque
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip011 : Foreboding Influence

- [x] Étape 2 : carte(s) de référence : `28014`, `ip002a`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip011 Foreboding Influence — 2 cartes de la defausse REGISTERED remontent dans le deck
      • ip011 Foreboding Influence — cote HEROS, elle recrute le sbire qu'on vient d'attaquer
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip012 : Repulsor Bombard

- [x] Étape 2 : carte(s) de référence : `01080`, `vz032`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip012 Repulsor Bombard — 2 degats, plus 1 par icone de boost defaussee du deck REGISTERED
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip013 : Call to Arms

- [x] Étape 2 : carte(s) de référence : `vz015`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip013 Call to Arms — elle REDRESSE les allies REGISTERED
      • ip013 Call to Arms — les allies redresses prennent +1 degat consecutif
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip014 : Seige

- [x] Étape 2 : carte(s) de référence : `01021`, `29017`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip014 Seige — X degats = ATQ cumulee des allies REGISTERED defausses
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip015 : Exposed Insanity

- [x] Étape 2 : carte(s) de référence : `56027`, `su014`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip015 Exposed Insanity — sans allie REGISTERED, elle fait entrer Reign's End
      • ip015 Exposed Insanity — premiere branche : Norman s'incline, l'obligation quitte la partie
      • ip015 Exposed Insanity — seconde branche : elle DEFAUSSE les allies REGISTERED
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip016 : Doctor Doom

- [x] Étape 2 : carte(s) de référence : `04077`, `56027`, `dd003`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip016 Doctor Doom — revele sans Cabal Obligations en jeu, il la fait entrer
      • ip016 * Doctor Doom — Cabal Rivalry le remelange et joue une carte Iron Patriot
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip017 : Reign's End

- [x] Étape 2 : carte(s) de référence : `09029`, `ip001a`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip017 Reign's End — 2 menaces des qu'un personnage entre en jeu
      • ip017 Reign's End — 3 cartes dessous, les joueurs PERDENT
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? **OUI** — voir `ui-app/src/board/deck-registered.test.ts`, 5/5, calibré §9.
      Résultat : OK

**Carte terminée : OUI**

### ip018 : Cabal Obligations

- [x] Étape 2 : carte(s) de référence : `02048`, `40082`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip018 Cabal Obligations — l'identite attachee ne peut plus se redresser
      • ip018 Cabal Obligations — les allies REGISTERED ne peuvent plus attaquer
      • ip018 Cabal Obligations — l'Action la defausse contre X ressources
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? **OUI** — voir `ui-app/src/board/deck-registered.test.ts`, 5/5, calibré §9.
      Résultat : OK

**Carte terminée : OUI**

### ip019 : Assembled Resistance

- [x] Étape 2 : carte(s) de référence : `02029`, `ag001a`, `al014`, `ip002a`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip019 Assembled Resistance — cote ALTER EGO, elle revele le deck REGISTERED
      • ip019 Assembled Resistance — cote HEROS, un personnage ami vous attaque
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip020 : H.A.M.M.E.R. Agents

- [x] Étape 2 : carte(s) de référence : `25023`, `__init__.py`, `ip020`, `ip021`, `ip022`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip020 H.A.M.M.E.R. Agents — premiere revelee du round : elle devient allie REGISTERED
      • ip002a + ip020 — TEMOIN : la DEUXIEME revelation du round ne donne PLUS d'allie
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip021 : H.A.M.M.E.R. Commandos

- [x] Étape 2 : carte(s) de référence : `__init__.py`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip021 H.A.M.M.E.R. Commandos — Suppressive Fire frappe 1 fois par personnage H.A.M.M.E.R.
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip022 : H.A.M.M.E.R. Operatives

- [x] Étape 2 : carte(s) de référence : `ip021`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip022 H.A.M.M.E.R. Operatives — Counter Intelligence retire de la menace
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip023 : Bullseye

- [x] Étape 2 : carte(s) de référence : `04027`, `50099`, `bc006`, `dt069`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip023 * Bullseye — recrute contre ses icones de boost, il porte le trait REGISTERED
      • ip023 * Bullseye — Kill Order met le sbire K.O. si la carte defaussee porte une etoile de boost
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip024 : Daken

- [x] Étape 2 : carte(s) de référence : `04027`, `05015`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip024 * Daken — Forced Response : il se soigne d'1 au debut de la phase du mechant
      • ip024 * Daken — Emotional Pheromones etourdit jusqu'a 2 ennemis
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip025 : Ghost

- [x] Étape 2 : carte(s) de référence : `29033`, `dt104`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip025 * Ghost — Intangible Espionage retire 1 menace par icone de manigance en jeu
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip026 : Madame Masque

- [x] Étape 2 : carte(s) de référence : `01118`, `02029`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip026 * Madame Masque — False Faces fait piocher selon l'etape de la manigance principale
      • ip026 * Madame Masque — apres avoir blesse un personnage, elle le desoriente
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip027 : Moonstone

- [x] Étape 2 : carte(s) de référence : `01131`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip027 * Moonstone — Psych Evaluation soigne 2 et donne une carte Robuste
      • ip027 * Moonstone — apres avoir VAINCU un personnage, elle se blinde
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip028 : Taskmaster

- [x] Étape 2 : carte(s) de référence : `ip001b`, `ip003`, `ip004`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip028 * Taskmaster — +1 ATQ et +1 MNG par personnage REGISTERED controle
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip029 : Venom

- [x] Étape 2 : carte(s) de référence : `17020`, `43019`, `al014`, `dt018`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip029 * Venom — sous la moitie de ses PV de depart, il gagne +1 ATQ
      • ip029 * Venom — TEMOIN : a la moitie EXACTE, pas de bonus
      • ip029 * Venom — Symbiotic Devour : l'allie attaque un personnage
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip030 : Ares

- [x] Étape 2 : carte(s) de référence : `01118`, `04027`, `25023`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip030 * Ares — War Tactician ramene un evenement ATTACK en main
      • ip030 * Ares — apres avoir blesse un personnage, il l'etourdit
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip031 : Loki

- [x] Étape 2 : carte(s) de référence : `31015`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip031 * Loki — Trickster Magic sort une traitrise du deck de rencontre
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip032 : Penance

- [x] Étape 2 : carte(s) de référence : `04006`, `16121`, `ip021`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip032 * Penance — Unleashed Pain frappe autant que les degats qu'il a subis
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip033 : The Hood

- [x] Étape 2 : carte(s) de référence : `01113`, `bc006`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip033 * The Hood — Demonic Crimes defausse le dessus du deck REGISTERED
      • ip033 * The Hood — quand il attaque, il recoit 1 carte de boost en plus
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip034 : Molecule Man

- [x] Étape 2 : carte(s) de référence : `04077`, `27152`, `56027`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip034 Molecule Man — revele, il fait entrer Master of Molecules
      • ip034 * Molecule Man — aucun personnage ne peut defendre contre lui
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip035 : "You're in My World"

- [x] Étape 2 : carte(s) de référence : `07004`, `41028`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip035 \
      • ip035 \
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

### ip036 : Master of Molecules

- [x] Étape 2 : carte(s) de référence : `01099`, `01122`, `41028`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip036 * Master of Molecules — il s'attache bien a Molecule Man
      • ip036 * Master of Molecules — la carte defaussee au hasard alourdit l'attaque
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? **OUI** — voir `ui-app/src/board/deck-registered.test.ts`, 5/5, calibré §9.
      Résultat : OK

**Carte terminée : OUI**

### ip037 : Manipulate Realities

- [x] Étape 2 : carte(s) de référence : `04077`, `41028`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py iron_patriot`.
      Résultat : « les 40 cartes de iron_patriot ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • ip037 Manipulate Realities — sans Molecule Man en jeu, elle prend deferlement
      • ip037 Manipulate Realities — Molecule Man en jeu, elle vide la main d'une couleur
      Résultat : vert (batterie `ip0` : **75/75**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay : 16 parties (Rhino et Klaw, normal, profil équilibré),
      grep tracebacks sur les 16 journaux : **0**. ⚠ Les 16 parties sont perdues
      au round 1 : voir « Ce qui n'est PAS fait » — le pilote spamme `Enlistment`,
      qui n'a aucune limite imprimée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — elle ne fait que chiffrer (dégâts, menace, ressources) ou déplacer des cartes dans des zones déjà dessinées.
      Résultat : OK

**Carte terminée : OUI**

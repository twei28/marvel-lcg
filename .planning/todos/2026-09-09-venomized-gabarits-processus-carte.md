# Venomized (ekAugust, set 168) — gabarits PROCESSUS-CARTE, 37 cartes

**Livré le 09/09/2026.** Sixième aspect de deck-building (noir), préfixe `vz`.
Ce n'est pas un pack de héros : aucune identité, aucune obligation, aucun set
némésis. `PROCESSUS-HEROS.md` ne s'applique donc pas — c'est
`PROCESSUS-CARTE.md`, 37 fois.

## Ce qui a été mesuré, et comment

| Gate | Résultat | Calibrage (§9) |
|---|---|---|
| `tools/verifier_prefixes.py` | OK, 0 doublon, 37 cartes sous `vz` | — |
| `tools/verifier_appels_modules.py venomized` | OK, tous les appels existent | ✅ appel bidon injecté dans vz016 → « `this.DealDamageQuiNExistePas` n'existe pas » |
| `tools/verifier_desc_mots_cles.py venomized` | OK, 37/37 | ✅ `Uses` de vz032 faussé → écart signalé |
| `tools/test_cards.py` | 5429 cartes construites, 0 erreur | ✅ paramètre bidon dans vz013 → `TypeError` nommant le module |
| `tools/test_capacites.py` filtre `vz0` | **39/39** | ✅ modules `vz036`/`vz037` retirés → 0/2 |
| `tools/autoplay.py`, 8 parties + témoin | 0 traceback sur 16 journaux | — |
| `ui-app` : `tsc` + 1209 tests | vert | ✅ `aspect.test.ts` vu rouge avant la déclaration de l'aspect |
| Non-régression `su0` / `sm0` | 32/32 et 34/34 | — |

## Ce qui a été trouvé en chemin

- **`weakness` est un mot-clé sans une ligne de code moteur**, et c'est une
  MESURE, pas une hypothèse : une Treachery placée dans le deck du joueur se
  pioche normalement et son `AfterCardEnterHand` part. Fiche :
  `docs/reference/mots-cles/weakness.md`.
- **Piège du harnais** : toute menace posée APRÈS `Puzzle.ChangeForm` est
  perdue (sonde : 5 avant → 5, 5 après → 0). Quatre cas `vz` ont été rouges
  pour cette seule raison. Noté dans `test_capacites.py`.
- **Faux vert évité** : les deux cartes de défense étaient testées sur
  Spider-Man (DEF 3) face à Rhino niveau 1 (ATQ 2). Il ne prenait aucun dégât
  même sans la carte. Elles sont passées à Storm (DEF 1).
- **`.NoOutOfPlayLimit()`** : sans lui, une capacité « après que cette carte
  est vaincue » ne part jamais, la carte étant déjà en défausse. Les trois
  alliés vz002 / vz003 / vz005 étaient rouges pour ce seul motif.

## Matériel manquant, signalé à l'auteur

⚠ **« Symbiotic Healing Factor »** est citée par la decklist de l'insert et
marquée « custom Aspect card designed by ekAugust ». **Elle n'est pas dans le
zip** : 37 fichiers pour 37 cartes, aucune de ce nom. Elle n'a donc ni
`card_id`, ni image, ni module, et le paquet d'aspect livré compte 24 cartes de
deck au lieu des 25 annoncées.

⚠ **La règle de deck-building du set Weakness n'est pas automatisée** : le
nombre de cartes Weakness dépend du coût total des cartes Venomized du deck, ce
que le constructeur ne calcule pas. Le paquet livré en contient 2, ce que la
decklist de l'auteur demande (coût total mesuré : 30, tranche 21-40).

---

### vz001 : Agent Anti-Venom

- [x] Étape 2 : carte(s) de référence : `21055`, `br005`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz001 Agent Anti-Venom — defausse jusqu'a un allie du MEME TRAIT, qui entre en jeu
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz002 : Codex

- [x] Étape 2 : carte(s) de référence : `ab011`, `gb010`, `deck.py:106`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz002 Codex — vaincu pendant la phase du joueur, il revient si le dessus est VENOMIZED
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz003 : Mania

- [x] Étape 2 : carte(s) de référence : `vz002`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz003 Mania — vaincue pendant la phase du joueur, elle fait piocher 1 carte
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz004 : Red Goblin

- [x] Étape 2 : carte(s) de référence : `01066`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz004 Red Goblin — un sbire entre en jeu, il s'incline et lui met 1 degat
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz005 : Sleeper

- [x] Étape 2 : carte(s) de référence : `vz002`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz005 Sleeper — vaincu pendant la phase du joueur, il desoriente le vilain
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz006 : Venom

- [x] Étape 2 : carte(s) de référence : `su012`, `CardFace.TuckCardUnderHere`, `48021`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz006 Venom — un sbire tombe, une carte part FACE CACHEE sous lui
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz007 : Backed into a Corner

- [x] Étape 2 : carte(s) de référence : `16052`, `message.PreventDamage(n, effect)`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz007 Backed into a Corner — degats prevenus = DEF + ATQ de Storm (1 + 2 = 3), zero subi
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz008 : Black Webbing

- [x] Étape 2 : carte(s) de référence : `tg002`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz008 Black Webbing — CONTRE-CAS SOLO : sans autre joueur, elle ne fait RIEN
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz009 : "Can't Escape Us!"

- [x] Étape 2 : carte(s) de référence : `32008`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz009 "Can't Escape Us!" — 2 degats, puis 3 de plus en inclinant une carte SYMBIOTE
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz010 : Dive into Danger

- [x] Étape 2 : carte(s) de référence : `16003`, `29017`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz010 Dive into Danger — menace retiree = CTR + DEF du heros (1 + 3 = 4)
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz011 : Feed the Hunger

- [x] Étape 2 : carte(s) de référence : `CardFinder.NonEliteMinion`, `Faces.DefeatUnits`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz011 Feed the Hunger — le sbire est MIS K.O. et soigne ses PV imprimes
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz012 : Forceful Bonding

- [x] Étape 2 : carte(s) de référence : `14006`, `gb010`, `Identity.ChangeToForm`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz012 Forceful Bonding — X cartes defaussees, une VENOMIZED, et on passe en heros
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz013 : Inner Strength

- [x] Étape 2 : carte(s) de référence : `25018`, `29017`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz013 Inner Strength — degats = ATQ + CTR du heros (2 + 1 = 3)
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz014 : Scared of the Dark

- [x] Étape 2 : carte(s) de référence : `32008`, `selector_target_helper.py:275`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz014 Scared of the Dark — le Tough saute, et l'ennemi est etourdi
      • vz014 Scared of the Dark — TEMOIN D'EPUISEMENT : le SECOND exemplaire du round ne fait rien
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? **OUI** (« Max 1 per round »). Témoin d'épuisement écrit,
      il mesure le REFUS du second déclenchement dans le même round.
      Résultat : vert
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz015 : Stronger Together

- [x] Étape 2 : carte(s) de référence : `03015`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz015 Stronger Together — deux personnages du MEME TRAIT redresses
      • vz015 Stronger Together — TEMOIN D'EPUISEMENT : le second exemplaire du round ne redresse plus
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? **OUI** (« Max 1 per round »). Témoin d'épuisement écrit,
      il mesure le REFUS du second déclenchement dans le même round.
      Résultat : vert
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz016 : Symbiotic Drop Kick

- [x] Étape 2 : carte(s) de référence : `10014`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz016 Symbiotic Drop Kick — 4 degats, et le bonus PAYE EN [physical] SEUL
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz017 : Symbiotic For Justice!

- [x] Étape 2 : carte(s) de référence : `01060`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz017 Symbiotic For Justice! — 4 menaces retirees quand le paiement contient du [mental]
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz018 : Symbiotic Go All Out

- [x] Étape 2 : carte(s) de référence : `29017`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz018 Symbiotic Go All Out — degats = CTR + ATQ + DEF (1 + 2 + 3 = 6), heros incline
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz019 : Symbiotic Multitasking

- [x] Étape 2 : carte(s) de référence : `15013`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz019 Symbiotic Multitasking — 2 menaces retirees SANS [mental] au paiement
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz020 : Symbiotic Not Today!

- [x] Étape 2 : carte(s) de référence : `38016`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz020 Symbiotic Not Today! — +2 DEF sur Storm, zero degat, PUIS 2 menaces retirees
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz021 : Symbiotic One By One

- [x] Étape 2 : carte(s) de référence : `28014`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz021 Symbiotic One By One — le sbire tombe, et la SECONDE attaque part
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz022 : Symbiotic Perseverance

- [x] Étape 2 : carte(s) de référence : `13033`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz022 Symbiotic Perseverance — le changement de forme donne un Tough au heros
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz023 : Symbiotic Sneak Attack

- [x] Étape 2 : carte(s) de référence : `23017`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz023 Symbiotic Sneak Attack — l'allie de la MAIN entre en jeu
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz024 : In the Thick of It

- [x] Étape 2 : carte(s) de référence : `40019`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz024 In the Thick of It — la manigance-joueur se pose et se laisse contrer
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI.** Son « When Defeated » a d'abord paru intestable ; la cause
réelle était un `assert deck.GetSize() != 0` de `src/game/selector/selector_end.py`, qui
faisait tomber le moteur dès qu'une recherche sortait la dernière carte d'un deck. La carte
OFFICIELLE `40019` Lock and Load était cassée de la même façon. Assert retiré, les deux
cartes sont vertes, et le cas `40019` garde le correctif.

### vz025 : Gluttony

- [x] Étape 2 : carte(s) de référence : `21046`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz025 Gluttony — depensee comme ressource, elle redresse le heros
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz026 : Symbiote Infusion

- [x] Étape 2 : carte(s) de référence : `32018`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz026 Symbiote Infusion — depensee pour une carte SYMBIOTE, elle fait piocher
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz027 : The Power of the Bond

- [x] Étape 2 : carte(s) de référence : `01062`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz027 The Power of the Bond — DEUX exemplaires payent un cout 3, ce qui prouve le doublement
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz028 : Alchemax

- [x] Étape 2 : carte(s) de référence : `01034`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz028 Alchemax — remonte la carte d'ASPECT du dessus de la defausse en main
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz029 : Doctor Steven

- [x] Étape 2 : carte(s) de référence : `05008`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz029 Doctor Steven — la prochaine carte VENOMIZED coute 1 de moins
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz030 : Durable Physiology

- [x] Étape 2 : carte(s) de référence : `Uses`, `01080`, `ReduceCharacterTakeDamageBy`, `45131`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz030 Durable Physiology — un pion klyntar consomme, et l'attaque du sbire ne passe plus
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz031 : First Contact

- [x] Étape 2 : carte(s) de référence : `01057`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz031 First Contact — +1 ATQ, +1 CTR ET +1 DEF sur l'identite
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI.** L'icône restée « non identifiée » au premier portage est le
glyphe `H` de `ChampionsIcons.ttf`, c'est-à-dire `.icon-hazard` : la carte porte **Hazard 1**,
désormais dans son `desc`. Mesuré par la clé `icones` du harnais, vu ROUGE sans la donnée
(« icones Hazard en jeu = 0 (attendu 1) »).

### vz032 : Klyntar Tendrils

- [x] Étape 2 : carte(s) de référence : `Uses`, `01080`, `32009`, `su006`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz032 Klyntar Tendrils — la branche degats, PUIS le soin qui tombe dans tous les cas
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz033 : Symbiotic Bond

- [x] Étape 2 : carte(s) de référence : `04033`, `CostFunc.TakeDamage(1, "YourIdentity")`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz033 Symbiotic Bond — genere du [wild] contre 1 degat et une inclinaison
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz034 : Urban Camouflage

- [x] Étape 2 : carte(s) de référence : `51019`, `CostFunc.TakeDamage(1, "YourIdentity")`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz034 Urban Camouflage — l'ennemi est desoriente et la carte part a la defausse
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz035 : "You Are What You Eat"

- [x] Étape 2 : carte(s) de référence : `vr014`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz035 "You Are What You Eat" — un soin de l'identite fait piocher, la carte s'incline
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz036 : Flash Fire

- [x] Étape 2 : carte(s) de référence : `weakness`, `bk002`, `al022`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz036 Flash Fire — MESURE du mot-cle WEAKNESS : une Traitrise vit dans le deck du JOUEUR
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

### vz037 : Sensory Overload

- [x] Étape 2 : carte(s) de référence : `weakness`, `vz036`, `determination/__init__.py`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges listés carte par carte.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py venomized`.
      Résultat : « les 37 cartes de venomized ont un desc conforme à leur texte ». Gate CALIBRÉE (§9) : `Uses` de vz032 passé à `3,tactic` → « Uses vaut '3,tactic', le texte dit '3,klyntar' »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • vz037 Sensory Overload — 1 menace sur CHAQUE manigance en entrant en main
      Résultat : vert (batterie `vz0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 8 parties, deck « Spider-Man (Venomized) » (decklist de
      l'auteur), témoin `spider_man`, grep tracebacks sur les 16 journaux : **0 partout**.
      Le deck Venomized a tenu 8 parties sur 8 sans blocage, le témoin 7 sur 8.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? Couverte par la déclaration de
      l'aspect côté plateau (`catalogue.ts`, `board.css`) : sans elle `aspect.test.ts` comptait
      `Venomized` comme classe inconnue et les 35 cartes n'avaient aucun liseré. Vu ROUGE
      (« expected [ 'Venomized' ] to deeply equal [] ») puis vert.
      Résultat : OK

**Carte terminée : OUI**

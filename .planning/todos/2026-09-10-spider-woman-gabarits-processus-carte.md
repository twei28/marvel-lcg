# Spider-Woman (Kajislav, set 169) — gabarits PROCESSUS-CARTE, 29 cartes

**Livré le 10/09/2026.** Préfixe `sw`. Pack de HÉROS complet : identité recto verso,
19 cartes de set héros et d'aspect Protection, 1 obligation, et **deux sets némésis
alternatifs** livrés par l'auteur, tous deux numérotés 1/5 à 5/5. `PROCESSUS-HEROS.md`
s'applique, donc `PROCESSUS-CARTE.md` 29 fois.

Le pack entier tourne autour d'un seul stock : les compteurs `psionic web` de
l'identité. Julia Carpenter en pose 5 au montage et 3 par Action, jusqu'à 10 ;
Spider-Woman les dépense pour annuler des icônes de boost, contrer et frapper.
**Douze des 29 cartes** les lisent, les posent ou les dépensent.

## Ce qui a été mesuré, et comment

| Gate | Résultat | Calibrage (§9) |
|---|---|---|
| `tools/verifier_prefixes.py` | OK, 0 doublon, 29 cartes sous `sw` | — |
| `tools/verifier_appels_modules.py spider_woman_kajislav` | OK, tous les appels existent | ✅ vu ROUGE : `AbilityFactory.TreatAsMinion` (c'est une fonction de module, pas une méthode) |
| `tools/verifier_desc_mots_cles.py spider_woman_kajislav` | OK, 29/29 | — |
| `tools/test_cards.py` | 5497 cartes construites, **0 erreur** | — |
| `tools/verifier_tous_les_decks.py` (`DECK_NOM=spider_woman_kajislav`) | OK, « identité sw001a, main 6, deck 33 » | — |
| `tools/test_capacites.py` filtre `sw0` | **39/39** | ✅ chaque cas vu ROUGE avant son correctif ; 8 défauts réels trouvés par eux |
| `tools/test_capacites.py` batterie COMPLÈTE | **1774/1778** — les 4 rouges sont ceux de Squirrel Girl, connus depuis le 31/08/2026 | Passe exigée : trois fichiers moteur touchés |
| `tools/autoplay.py` | 32 parties (Rhino et Klaw, normal, profil équilibré), **0 traceback**, **0 partie sans verdict** | ✅ vu ROUGE : 8 `AssertionError` au premier passage, 1 défaut réel |
| `tools/autoplay.py` **témoin** `spider_man` | 32 parties, 0 traceback, **1 partie bloquée** | Le témoin dit que le 0 % de victoires vient du PILOTE, pas du pack |
| `ui-app` : `tsc` + 1217 tests | vert | ✅ `compteurs-fr.test.ts` vu ROUGE sans l'entrée « psionic web » |

## Ce qui a été trouvé en chemin

**Neuf défauts RÉELS. Aucun n'a été trouvé par relecture.** Huit par le harnais de
capacités, un par l'autoplay et par lui seul.

1. **`AbilityFactory.TreatAsMinion` n'existe pas** sous ce nom : c'est une fonction de
   module (`game/ability/factory/treat.py:3`), que le `import *` de `cards/pack` ne
   réexporte pas. Précédent déjà documenté dans `agent_anti_venom_nemesis`.
2. **`ToilesParRessourceMentale` rendait TOUJOURS zéro.** On lisait
   `effect.cost_func.Get(CostFunc.Spend).return_res` : l'objet existe, la ligne ne lève
   rien, et le compte est nul. Quatre cartes posaient donc zéro compteur en silence.
   La bonne brique est `effect.GetPaidResources()` (`effect.py:501`), celle de `bw008`.
3. **`CostFunc.TakeDamage("This", 2)` : arguments à l'envers**, c'est `(valeur, cible)`.
   Le moteur appelle `value(effect)` sur une chaîne, lève un `TypeError` et l'AVALE.
   Les deux alliés Protection concernés étaient inertes.
4. **`activate_target="You"` fait exploser une assertion.** Une chaîne EST une
   `Sequence` en Python, et `invoke_check_card` (`condition/card_type.py:247`) affirme
   le contraire. L'interruption de `sw001a` ne s'ouvrait JAMAIS. Piège déjà rencontré,
   déjà documenté, et repris quand même : `"YourHero"` est la valeur juste.
5. **`AskDiscardFaces` n'a pas de paramètre `prompt`.** `TypeError` avalé : `sw021`
   Man-Bull ne faisait rien défausser du tout.
6. **Le gabarit `minion` a ZÉRO point de vie**, et `TreatAsMinion` ne recopie que
   l'ATQ et la MNG. L'allié converti par `sw023` entrait en jeu et était vaincu dans
   le même souffle. Les PV imprimés sont désormais recopiés dans le `process`.
7. **CORRECTIF MOTEUR : un coût qui tue son payeur était déclaré IMPAYÉ.**
   `TakeDamageOnCall` (`cost_func.py:15`) portait un `if unit.IsDefeated(): return
   False` sans un mot d'explication, alors que le commentaire au-dessus ne justifie
   que les dégâts EMPÊCHÉS. `sw013` Shroud a 2 PV et son coût imprimé est « infligez-lui
   2 dégâts » : la carte était **injouable par construction**. Ligne retirée, avec sa
   justification sur place. Batterie complète repassée : **1774/1778**, aucun écart.
8. **Une condition relue APRÈS le paiement du coût.** `which_player="You"` se résout
   par le CONTRÔLEUR de la carte ; Shroud mort n'en a plus, la condition tombe et
   l'opération n'est jamais lancée. Remplacée par une condition maison sur le
   PROPRIÉTAIRE, qui survit à la défausse. Trouvé en posant une sonde `print` dans
   l'opération, faute de tout autre signal.
9. **Trouvé par l'AUTOPLAY et par lui seul.** `sw001a` posait `activate_target` sans
   `while_attack=True`. La fabrique lit les cibles dans `attacked_targets` et fait
   `assert False` quand l'activation n'est pas une attaque — or **une manigance de
   vilain tire aussi des cartes de boost**. 8 `AssertionError` sur 32 parties. Aucun
   des 39 cas ne fait manigancer le vilain, donc aucun ne pouvait le voir.

## Ce que les gates ne peuvent pas voir

- **`sw017` Tactical Retreat résiste au harnais dans sa situation normale.** Son coût
  est « inclinez votre héros », or DÉFENDRE incline déjà le héros et le pilote défend
  dès qu'on le lui propose. Le cas passe donc par `ip034` Molecule Man, contre qui
  « Character cannot defend » : aucune défense offerte, héros prêt, coût payable. C'est
  la situation réelle de la carte, celle où l'on choisit de ne pas défendre.
- **Le taux de victoire ne dit rien du pack** : 0 % pour Spider-Woman comme pour le
  témoin Spider-Man, avec une partie bloquée en plus côté témoin.

## Gabarits, une carte par section

### sw001a : * Spider-Woman

- [x] Étape 2 : carte(s) de référence : `08006` Attacrobatics et `09038` Foiled (`WhenBoostCardTurnedFaceUp`) ; `CancelAllBoostIcons` pour le modele de l'annulation, dont `CancelBoostIcons` est la version UNITAIRE ecrite pour cette carte
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw001a Psionic Webbing — une icone de boost annulee coute 1 toile et blesse l'ennemi
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : les compteurs `psionic web` s'affichent sur l'identite. Le plateau ecrivait
      « 5 psionic web » en partie francaise ; entree ajoutee dans `compteurs-fr.ts`, avec
      son cas dans `compteurs-fr.test.ts`. Vu ROUGE avant l'entree.
      Résultat : OK

**Carte terminée : OUI**

### sw001b : * Julia Carpenter

- [x] Étape 2 : carte(s) de référence : `kb001a` Kate's Bow pour la pose de compteurs par Action ; `Faces.PlaceCountersOn(..., maximum=)` pour le plafond imprime
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw001b Julia Carpenter — Setup : 5 compteurs de toile psionique
      • sw001b Proper Relaxation — l'Action pose 3 compteurs de plus (5 -> 8)
      • sw001b Proper Relaxation — TEMOIN DU PLAFOND : 9 + 3 donne 10, pas 12
      • sw001b Proper Relaxation — TEMOIN D'EPUISEMENT : la 2e Action est refusee
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? OUI — le cout d'inclinaison de « Proper Relaxation », plus le plafond de 10 compteurs.
      DEUX temoins : « TEMOIN D'EPUISEMENT » monte deux Actions dans le meme tour, la
      seconde est REFUSEE et le stock reste a 8 et non 11 ; « TEMOIN DU PLAFOND » part
      de 9, demande 3, et mesure 10.
      Résultat : OK
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : meme compteur, meme correctif (`compteurs-fr.ts`).
      Résultat : OK

**Carte terminée : OUI**

### sw002 : * Madame Web

- [x] Étape 2 : carte(s) de référence : `ThisGainKeyword(..., change_on_event=OnEvent.Counter(...))`, modele `gp011` ; `Search.PlayerCard(set_name=...)` pour « a Spider-Woman card »
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw002 Madame Web — +1 CTR tant qu'il y a au moins 4 toiles
      • sw002 Madame Web — TEMOIN : a 3 toiles, plus de bonus de CTR
      • sw002 Madame Web — When Defeated : une carte Spider-Woman du deck rentre en main
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? OUI — le seuil « at least 4 counters ». Temoin : on retire 2 compteurs des 5 du
      montage, le +1 CTR doit DISPARAITRE. C'est aussi le seul test du
      `change_on_event` : sans lui la condition ne serait lue qu'a l'entree en jeu.
      Résultat : OK
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw003 : * Rachel Carpenter

- [x] Étape 2 : carte(s) de référence : `50029` Press Conference pour l'Action d'alter ego a cout d'inclinaison
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw003 Rachel Carpenter — l'Action d'alter ego redresse Julia
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw004 : Madame Web's Powers

- [x] Étape 2 : carte(s) de référence : `GiveKeywordToInPlayWhenApplyThis("You", trait=...)` ; `CanGenerateResources` + `CostFunc.Custom` pour l'effet annexe du paiement
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw004 Madame Web's Powers — l'identite gagne le trait PSIONIC
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw005 : Swing and Kick

- [x] Étape 2 : carte(s) de référence : `bw008` (Brawn) : `effect.GetPaidResources().GetColor("B")`, la brique « provenance du paiement »
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw005 Swing and Kick — 5 degats, et 1 toile par ressource [mental] depensee
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw006 : Psi-Web Trap

- [x] Étape 2 : carte(s) de référence : `bw008` pour le paiement ; `AskChooseOneText(range(...))` faute de « demander un nombre » dans le moteur
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw006 Psi-Web Trap — X toiles depensees retirent X menaces d'une manigance
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw007 : Psionic Web Blast

- [x] Étape 2 : carte(s) de référence : `sw006`, meme brique, autre sortie
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw007 Psionic Web Blast — X toiles depensees infligent X degats
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw008 : Swinging Rescue

- [x] Étape 2 : carte(s) de référence : `Faces.AddToHand` + `joueur.DrawUp` ; `bw008` pour les toiles
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw008 Swinging Rescue — un allie de la defausse rentre en main, 2 toiles par [mental]
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw009 : Web Formation

- [x] Étape 2 : carte(s) de référence : `RemoveThreatFromSchemes("EachScheme", ...)` ; `bw008` pour les toiles
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw009 Web Formation — 2 menaces retirees de CHAQUE manigance
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw010 : Hold 'Em Tight

- [x] Étape 2 : carte(s) de référence : `mw008` (cout X, `effect.GetCostX()`) ; `bw008` pour les toiles
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw010 Hold 'Em Tight — X degats et l'ennemi blesse est etourdi
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw011 : * Arachnne Costume

- [x] Étape 2 : carte(s) de référence : `GainUntilRoundEnd` ; `AskChooseOneText` pour le choix du pouvoir de base
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw011 Arachnne Costume — 2 toiles rendues donnent +2 a un pouvoir de base
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw012 : * Century

- [x] Étape 2 : carte(s) de référence : `WhenUnitWouldTakeDamage(..., is_from_attack=True)` + `PreventDamage("All")`, modele `03005` EM Shield
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw012 Century — une attaque plus faible que ses PV restants est entierement evitee
      • sw012 Century — TEMOIN : une attaque egale a ses PV restants passe
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? OUI — le mot « LESS ». Temoin a l'EGALITE : Century blesse de 1 n'a plus que 2 PV,
      l'attaque en vaut 2, la prevention ne doit PAS jouer et l'allie tombe.
      Résultat : OK
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw013 : * Shroud

- [x] Étape 2 : carte(s) de référence : `30005` "I Don't Think So!" : `WhenPlayerRevealCard(..., "All", ...)` + `CancelAllEffectsAndDiscardIt`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw013 Shroud — il annule une carte Rencontre revelee et la defausse
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw014 : * U.S. Agent

- [x] Étape 2 : carte(s) de référence : `WhenUnitAttackYou` ; `CostFunc.TakeDamage(valeur, cible)`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw014 U.S. Agent — il encaisse 1 pour rendre 2 a l'ennemi qui vous attaque
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw015 : Blinded Sight

- [x] Étape 2 : carte(s) de référence : `GainForThisActive(attack=-2)` ; `IfThisAttackDealDamage` + `RunAt.AfterEnemyActivationEnd`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw015 Blinded Sight — -2 ATQ, et l'ennemi qui n'a rien fait est desoriente
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw016 : Misdiiirection

- [x] Étape 2 : carte(s) de référence : `AfterUnitDefendAgainstAttack(..., take_no_damage=True)` + `CostFunc.Discard("This")`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw016 Misdiiirection — defense sans degat : un AUTRE ennemi prend l'ATQ de l'attaquant
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? OUI — « Max 1 per player », base native `desc.MaxPerUnit`, verifiee par
      `verifier_desc_mots_cles`.
      Résultat : OK
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw017 : Tactical Retreat

- [x] Étape 2 : carte(s) de référence : `17006` Bad Boy : meme texte au cout pres, `PreventDamage("All")` puis `ChangeToForm(AlterEgo)`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw017 Tactical Retreat — degats entierement evites, et retour en alter ego
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw018 : * Battleworld

- [x] Étape 2 : carte(s) de référence : `Worlds.DiscardEncounterTopCard` et `joueur.DiscardDeckTopCard`, deux defaussements en chaine
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw018 Battleworld — un sbire du deck Rencontre et un allie du deck joueur entrent en jeu
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw019 : Past and Future

- [x] Étape 2 : carte(s) de référence : base native `desc.TeamUp` + `SetTarget("TeamUp")`, fiche `mots-cles/teamup.md`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw019 Past and Future — Team-Up : 2 toiles de plus une fois Madame Web en jeu
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? OUI — « Max 1 per deck », base native `desc.MaxPerDeck`.
      Résultat : OK
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw020 : Separation from the Child

- [x] Étape 2 : carte(s) de référence : `WhenThisObligationGiveToYou` + `ChooseAbilities` a deux branches
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw020 Separation from the Child — la 1re branche retire l'obligation de la partie
      • sw020 Separation from the Child — 2e branche : moins de 5 toiles, la carte gagne Renfort
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw021 : * Man-Bull

- [x] Étape 2 : carte(s) de référence : `27153` Induced Panic pour `IsClass("IdentitySpecific")` ; `04077` pour `Players.ForEachPlayer`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw021 * Man-Bull — chaque joueur defausse 1 carte specifique a une identite
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw022 : Vault Breakout

- [x] Étape 2 : carte(s) de référence : `Search.EncounterCard(include_discard_pile=False, card_type=Minion)`, qui remelange seul
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw022 Vault Breakout — chaque joueur sort un sbire du deck Rencontre
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw023 : Bad Inspiration

- [x] Étape 2 : carte(s) de référence : `27171` Manipulated Mind, MEME TEXTE a l'attachement pres ; `agent_anti_venom_nemesis` pour l'appel direct de `TreatAsMinion`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw023 Bad Inspiration — un allie de la defausse revient EN SBIRE
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : l'allie converti change de FACE, le plateau dessine un sbire portant le nom de
      l'allie (`minion.SetName`). Couvert par le cas moteur, qui lit le gabarit `minion`
      en jeu et ses PV recopies.
      Résultat : OK

**Carte terminée : OUI**

### sw024 : Violent Disturbance

- [x] Étape 2 : carte(s) de référence : `sw021`, dont elle partage `EstSpecifiqueALIdentite`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw024 Violent Disturbance — TOUTES les cartes du set heros quittent la main
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw025 : * Ms. Marvel

- [x] Étape 2 : carte(s) de référence : `AfterUnitSchemeEnd(ForcedResponse, "This", ...)` ; `50029` pour le couple Reponse forcee + fenetre
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw025 * Ms. Marvel — apres avoir manigance, elle pose 2 menaces sur l'Acte
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw026 : Superhuman Registration Act

- [x] Étape 2 : carte(s) de référence : `gp011` Rules of the Universe : L'INVERSE EXACT, mot pour mot, deja permanente et nemesis
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw026 Superhuman Registration Act — chargee de menace, elle porte une icone d'alea
      • sw026 Superhuman Registration Act — TEMOIN : sans menace, plus d'icone d'alea
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? OUI — l'icone d'alea est GAGNEE, pas imprimee. Temoin : menace ramenee a zero,
      l'icone doit s'ETEINDRE alors que la manigance, PERMANENTE, reste en jeu.
      Résultat : OK
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw027 : Fugitive

- [x] Étape 2 : carte(s) de référence : `50029` Press Conference (fenetre de phase + `PlayerActionToDiscardThis`) ; `aa017` Funeral pour `SetCost(Cost("B"))`
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw027 Fugitive — l'Acte vide, l'Action d'alter ego defausse l'obligation
      • sw027 Fugitive — TEMOIN : tant que l'Acte porte de la menace, l'Action est refusee
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? OUI — « If there is no threat on Superhuman Registration Act ». Temoin : l'Acte
      charge a 3, l'Action d'alter ego doit etre REFUSEE et Fugitive rester en jeu.
      Résultat : OK
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

### sw028 : Fighting a Friend

- [x] Étape 2 : carte(s) de référence : `50142` Psychological Manipulation (deux `WhenThisRevealed`, ATQ du heros) ; `60064` pour le choix de la cible
- [x] Étape 5 : texte-contre-code : bloc « TEXTE CONTRE CODE » du module, mots-pièges
      listés ligne par ligne.
      Résultat : OK
- [x] Étape 6 : nombres texte ↔ code : `tools/verifier_desc_mots_cles.py spider_woman_kajislav`.
      Résultat : « les 29 cartes de spider_woman_kajislav ont un desc conforme à leur texte »
- [x] Étape 7 : cas `test_capacites` par capacité :
      • sw028 Fighting a Friend — cote alter ego : 3 menaces sur l'Acte
      • sw028 Fighting a Friend — cote heros : un personnage ami prend l'ATQ du heros
      Résultat : vert (batterie `sw0` : **39/39**)
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : 32 parties (Rhino et Klaw, normal, équilibré), grep
      tracebacks sur les 32 journaux : **0**. Témoin `spider_man`, mêmes réglages :
      0 traceback et 1 partie bloquée.
      Résultat : OK
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON — ni attache, ni glisse,
      ni compteur propre, ni statut, ni mise de côté, ni changement de zone que le
      plateau dessine autrement qu'une carte ordinaire.

**Carte terminée : OUI**

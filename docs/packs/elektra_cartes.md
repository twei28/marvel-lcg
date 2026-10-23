# Elektra Natchios (Hero Pack officiel MC63, FFG, novembre 2026) : cartes d'ASPECT, gabarits PROCESSUS-CARTE

Chantier du 22-23/10/2026. Pack `elektra` (`src/cards/pack/elektra/`), `set_name` vide (cartes officielles :
ni champ `custom`, ni préfixe lettre). Numéro de card_id = numéro de collection imprimé (63015 à 63039 ; les
numéros 24-26 et 28-33 ne sont pas publiés). **Périmètre (décision de l'utilisateur) : les cartes d'aspect
seulement. PAS le héros Elektra, ni ses cartes signature.**

Sources : `.planning/elektra-officiel/` (`hoh/` = images 300 px de la page Hall of Heroes, `cc-spoil/` = captures
HD « content creator »). Chaque carte relue sur son image avant le code.

**Cas** : `tools/cas/elektra_aspects.py`, préfixe `[el_aspect]`, **44 cas, 44 verts**
(`CAS_PREFIX=ife5_ PARALLELES=4 test_capacites.py .game-src 44400 <rapport> "[el_aspect]"`). Les réimpressions
TMNT 63017-63020 gardent en plus leurs cas `[ua]` de `tools/cas/tmnt_aspect_aggression.py` (ids renommés).
Vérificateur maison `el_melange_haut` (Double-Cross).

## Réimpressions (décision : « nouvelle = source, ancienne = lien »)

| Nouveau | Carte | Ancien | Devenu |
|---|---|---|---|
| 63017 | Combo Move | `ua011` (TMNT Inkwire) | art alternatif `tmnt` |
| 63018 | Chain Reaction | `ua008` | art alternatif `tmnt` |
| 63019 | Nerve Strike | `ua030` | art alternatif `tmnt` |
| 63020 | Flow of Battle | `ua019` | art alternatif `tmnt` |
| 63027 | Dance with the Devil | `60031` (FNE, Daredevil) | `full_link` vers 63027 |

La source (63xxx) porte script, image officielle et tests ; l'ancienne carte n'existe plus que comme lien /
art alternatif. ⚠ Dans `data/cards.json` la source doit être placée **avant** son lien (le chargeur copie le
papier de la source) : le lien `60031` est à la fin de la liste `elektra`.

## Cartes

### 63015 * Shang-Chi (allié Aggression, 4 ressources)
- Étape 2 : références `ua040` Ujigami (10 compteurs, « Remove 1 counter → deal 1 damage »), `hc001a` Hellcat
  (limite deux fois par round = deux capacités identiques, chacune `.LimitOncePerRound()`).
- Étape 5 : « Action » (pas Hero Action) ; « Limit TWICE per round » (3e usage refusé, cas) ; 1 dégât de carte,
  pas une attaque.
- Étape 6 : PV 3, ATQ 2, CTR 2 (cas « valeurs imprimées »), 10 compteurs `ring`.
- Étape 7 : 4 cas. Étape 7 bis : limite imprimée OUI (témoin d'épuisement : 3e Action refusée).
- Étape 8 bis : compteur `ring` générique. Carte terminée : OUI.

### 63016 * Black Cat (allié Aggression, 3 ressources)
- Texte : « [star] Villainous. (When this character uses a basic power, give it a boost card.) ». Décision de
  l'utilisateur : l'implémenter dans le moteur. `desc.Villainous = "1"` suffit (`can_boost.py` gère déjà les
  alliés et héros Villainous) : aucune ligne de script.
- Cas : valeurs imprimées ; attaque avec carte boost Exhaustion (1 + 2 = 3 dégâts) ; témoin sans Villainous
  (Vision : 2 dégâts, aucune carte boost) ; et le cas Backstab / Black Cat (aucun ennemi n'active).
  Carte terminée : OUI.

### 63017-63020 Combo Move, Chain Reaction, Nerve Strike, Flow of Battle
Réimpressions TMNT (tableau ci-dessus), scripts déplacés par `git mv` depuis `tmnt_aspect_aggression`, textes
et cas `[ua]` inchangés (2 à 4 cas chacun, verts).

### 63021 Shuriken (amélioration Aggression, coût 2★)
- Références : `64017` Night Nurse (Uses + `CostFunc.Counter("This", 1, ...)`), `64032` (`DiscountAbility` +
  amélioration posée sur son porteur), `ua040`.
- Étape 5 : Hero Action SANS (attack) : 1 dégât de carte ; Uses (3) : au dernier compteur retiré la carte est
  défaussée (règle des Uses, cas) ; Réduction 1 si Martial Artist (cas + contre-cas Danny Rand).
- ⚠ The Power of Aggression (`01055`) DOUBLE les ressources pour une carte Aggression : le témoin « une seule
  ressource » utilise `01079` (Protection, doublé pour Protection seulement).
- Étape 7 : 5 cas. Étape 7 bis : limite imprimée NON. Carte terminée : OUI.

### 63022 * Stone (allié Basic, 3 ressources)
- Étape 5 : « EXACTLY defeats » (un excès ne déclenche rien, deux cas) ; « enemy OR side scheme » deux
  déclencheurs ; « heal 2 damage from Stone » sur lui-même.
- ⚠ Ordre du moteur : la Réponse part avant les dégâts consécutifs (Stone avec 2 dégâts, Tiger Shark achevé
  exactement : soigné 2 → 0 puis consécutifs 2 = 2). Constaté sur le cas, commun à toutes les Réponses
  « après avoir vaincu » du moteur.
- Étape 6 : PV 3, ATQ 2**, CTR 1*. Étape 7 : 6 cas. Carte terminée : OUI.

### 63023 Hunting Shadows (événement Basic, coût 0)
- Références : `18011` Angela (`Search.EncounterCardTop`), `Deck.Shuffle`, `Card.MoveToTop`.
- Étape 5 : « top 8 » ; « a card » (tout type) ; mélange du deck SANS la carte mise de côté, puis elle est
  remise au DESSUS (cas : la carte la plus profonde des 17 devient la prochaine révélée, deck inchangé à 17).
- Étape 7 : 1 cas (vérificateur `sc_dessus_rencontre`). Carte terminée : OUI.

### 63027 Dance with the Devil (amélioration Basic, Team-Up Daredevil et Elektra)
Réimpression de `60031` (lien). 2 cas : Team-Up complet (3 dégâts, carte défaussée), contre-cas sans Elektra
(non jouable). Carte terminée : OUI.

### 63034 * Double-Cross (manigance annexe de joueur Justice, coût 0, menace 2 par joueur, Victory 0)
- Références : `43021` Specialized Training (`WhenSchemeBeDefeated` + cartes Linked), `63023`.
- Étape 5 : « NOT ALREADY a copy IN THE VICTORY DISPLAY » ; les trois cartes de la zone de mise de côté ;
  « shuffle into the TOP 10 » = les 3 cartes + les 10 premières (13), ou tout le deck s'il en a moins de 10.
- Étape 7 : 4 cas (valeurs, 15 cartes → 13 mélangées, 4 cartes → 7, copie déjà en pile de victoire → rien).
  Carte terminée : OUI.

### 63035 Backstab, 63036 Misdirect, 63037 Sabotage (traîtrises Linked (Double-Cross))
- `desc.Linked = "Double-Cross"` : le moteur les fabrique dans `world.aside_deck` (fiche `linked.md`).
- ⚠ Pas de `desc.Class` : une Traîtrise n'accepte pas cet attribut dans le moteur (KeyError `Class`) ; ces
  cartes ne sont jamais dans un deck de joueur (mises de côté), l'aspect Justice n'a pas d'effet.
- Backstab : Boost « si un ENNEMI active » : la manigance d'un ennemi COMPTE (2 dégâts à Rhino, pas d'icônes) ;
  « sinon +2 icônes » = aucun ennemi n'active (attaque d'un allié Villainous, Black Cat : 1 + 2 = 3 dégâts).
  ⚠ `message.activating_enemy` peut être un allié Villainous : `Enemy.IsType` le distingue.
- Misdirect : soin de 4 d'une identité (plafonné aux dégâts) ; Boost sonne un ennemi.
- Sabotage : 3 menaces retirées du complot principal (plafonné) ; Boost désoriente un ennemi.
- Révélation : Renfort (cas : la carte suivante est révélée). 10 cas. Cartes terminées : OUI.

### 63038 * Moondragon (allié Leadership, 4 ressources)
- Références : `47012` Husk (`WhenUnitUseBasicPower`, `GainValue`), `tt014` Firebird (dégâts consécutifs « pour
  cet usage »), `58006` (`DeclareNumber`).
- Étape 5 : « from 1 to 3 » ; « +X to THAT power » ; MÊME X pour la puissance et les dégâts consécutifs.
- Limite du harnais : le pilote répond toujours le premier item de `DeclareNumber` (X = 1) ; la borne 3 reste
  dans le code (`DeclareNumber(1, 3)`) mais n'est pas forçable. 3 cas. Carte terminée : OUI.

### 63039 * Moon Knight (allié Protection, 4 ressources)
- Modèle `47012` Husk pour le format « spend up to 3 resources → if you spent at least 1 » : `Cost("3",
  up_to=True)`. ⚠ Le harnais ne paie un coût « jusqu'à » qu'avec `payer_jusqu_a` (sinon l'Interruption n'est
  pas payée ni résolue).
- Cas : [energy] prévient 2 (budget pour toute l'attaque) ; [physical] inflige 2 à l'attaquant ; [mental]
  défausse la carte boost de l'attaquant (2 dégâts contre 4 au témoin) ; 0 ressource : rien ; les trois types
  ensemble. 7 cas. Carte terminée : OUI.

## Gates

- **Substitution** (`tools/substituer_pack.py .game-src 44600 630`, pack sauvegardé puis comparé : identique) :
  **15/15** cartes scriptées rouges sans leur module. Les cas restés verts sont des témoins d'ABSENCE (coût non
  payable, contre-cas, Team-Up incomplet, un excès qui ne déclenche rien) ou des valeurs imprimées (`desc`).
  Black Cat n'a pas de script (`desc.Villainous`) : preuve par le cas « 1 + 2 = 3 dégâts » contre le témoin
  Vision (2 dégâts, aucune carte boost).
- `test_cards` : **7197 ok / 0 erreur** ; `verifier_prefixes` OK ; `verifier_appels_modules elektra` OK ;
  `verifier_api_cartes` : aucun problème dans `elektra`.
- **Autoplay** : deck Iron Fist + les 13 cartes d'Elektra, `--vilains rhino,klaw --profils prudent,agressif
  --parties 4` : 16 parties, 0 blocage, **0 traceback** (défaites rapides attendues : deck d'un héros sans
  cartes signature adaptées).
- Lanceur `node --test tools/tests-lanceur/*.test.mjs` : 323/323. vitest : seuls échecs `aspect.test.ts`
  (Class `IdentitySpecific`) et `zones-arts-alternatifs.test.ts` (03017_mcdc26), sans rapport.
- Étape 8 bis (plateau) : aucun rendu nouveau (compteurs `ring` / `shuriken` génériques).
- Textes FR provisoires dans `textes-fr-fanmade.ts` (63015, 63016, 63017-63023, 63027, 63034-63039), module public
  régénéré. Images : `assets/pics/630xx` ; 63034-63037 coupées depuis les captures HD ; plusieurs autres cartes
  viennent des images 300 px de Hall of Heroes (à remplacer par des scans HD quand ils existent).

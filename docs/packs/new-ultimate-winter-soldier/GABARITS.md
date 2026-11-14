# New Ultimate Winter Soldier (Dipsome) : gabarits PROCESSUS-CARTE, 19 card_id

Pack `new_ultimate_winter_soldier`, préfixe `uw`, set 219. Source : zip « New Ultimate Winter Soldier » déposé le 25/10/2026 (24 images :
19 cartes distinctes, dont 5 en double ; **aucun texte fourni**, tout est lu sur les scans ; auteur Dipsome, même auteur que `harry_osborn`,
Terre-6160). Le héros reprend le montage du **Wolverine officiel** (`wolv`, 35001-35012) : Healing Factor, Wolverine's Claws mises de côté
et mises en jeu au Setup, Adamantium Skeleton ; son moteur propre est « discard 1 card from your hand AT RANDOM » (fiche
`mots-cles/defausse-au-hasard.md`). Deck `deck/starter/new_ultimate_winter_soldier.json` : 15 cartes + Griffes mises de côté, `player_deck`
vide (aucune decklist fournie, décision du 06/09/2026).

Cas : `Fusion/marvel-lcg-src/tools/cas/new_ultimate_winter_soldier.py` (filtre `[uw]`). Plateau : `ui-app/src/board/new-ultimate-winter-soldier-plateau.test.ts`
(7 cas verts d'emblée).

## Arbitrages du 26/10/2026 (RR 1.8 + scans)
Questions en attente tranchées par le Rules Reference et les scans (`VERDICTS-REGLES-2026-10-26.md`, `docs/rapports/2026-10-26-arbitrages-heros-fanmade.md`). Seule **uw006** change (la répétition rejoue le coût) ; le reste est « A confirmé ».

## ⚠ DOUTES EN ATTENDANT L'UTILISATEUR (choix provisoire codé, cartes « NON (provisoire) »)

1. **uw006** : « repeat this ability » repart-il de l'EFFET (même X, aucune nouvelle défausse : retenu, comme 35008) ou de TOUTE la capacité ?
2. **uw014** : lecture du texte (« it », « the engaged player »).
3. **uw002** : « that event deals 1 additional damage (max 3) » : par attaque de l'événement (retenu, comme Cybernetic Arm) ou par événement ?
4. **uw003** : une Phoenix qui entre en jeu à la place de la défausse compte-t-elle comme « défaussée » pour les Griffes et Winter Mask ? (retenu : non)
5. **uw009** : une Response par carte tirée, même en plein paiement d'un coût (retenu : oui).
6. **uw011/uw012** : « after » rendu dans la fenêtre « when defeated » (l'amélioration attachée n'existe plus après) ; « defeated by Winter Soldier » inclut les
   attaques d'événements du héros (retenu : oui).
7. **uw015** : ATK ★ et SCH ★ sans chiffre : 0 (retenu).

## Gates du héros

- [x] PROCESSUS-HEROS étapes 1 à 8 : cartes (`cards.json`, pack `new_ultimate_winter_soldier`), scripts (`src/cards/pack/new_ultimate_winter_soldier/`), deck de départ,
      `sets_info.json` (« 219. Custom (New Ultimate Winter Soldier) »), préfixe `uw`, images (`assets/pics/uw*.jpg`, 615×882, non versionnées ; `uw014`
      en paysage 882×615), textes FR (`ui-app/src/board/textes-fr-fanmade.ts`, gates vertes), vocabulaire des boutons (`vocabulaire-moteur.ts`), biographie
      (`public/js/prepare/heros-info.js`, `uw001a`, module chargé ; **survol dans l'assistant NON vérifié**).
- [x] Légalité des decks (§10) : 0 signature étrangère dans un `player_deck` (le `player_deck` est vide).
- [x] Valeurs imprimées relues contre `cards.json` : 0 écart.
- [ ] Une partie complète jouée par un humain : NON FAITE.

### uw001a : * Winter Soldier (face HÉROS) — EARTH-6160. OPPOSITION. SOLDIER. PV 10, THW 2, ATK 2, DEF 2, main 5.

Healing Factor — Response : After the villain phase begins, heal 2 damage.

- [x] Étape 2 : carte(s) de référence : `35001a` Wolverine (même Healing Factor, cible `YourHero`, `canbe_heal`) ; `53011`/`45032` (`AfterPhaseBegin(.., "Villain", ..)`).
- [x] Étape 5 : mots-pièges : « After the VILLAIN phase begins » (35001a : la phase des joueurs) ; « Response » facultative ; forme héros seulement. Conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 10, ATK 2, THW 2, DEF 2, main 5 (`desc` + cas « valeurs imprimées »). Conforme.
- [x] Étape 7 : cas : 3 dégâts → 1 ; contre-cas ALTER EGO (3 dégâts restent) ; valeurs imprimées. Substitution : rouges 1/3 (vert sans module : le contre-cas alter ego et les valeurs imprimées, assumés).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : aucune partie humaine.

### uw001b : * Logan (face ALTER EGO) — EARTH-6160. MUTANT. SOLDIER. PV 10, REC 6, main 6.

Shuck! — Setup : Search your deck and discard pile for the Wolverine's Claws upgrade and put it into play.

- [x] Étape 2 : carte(s) de référence : `35001b` Logan officiel : `SetupPutIntoPlay([id])` + `set_aside` du deck de départ (la phrase imprimée « search your deck and discard pile » est rendue ainsi dans le jeu officiel).
- [x] Étape 5 : mots-pièges : Les Griffes sont mises de côté, jamais dans la main de départ : le texte les trouve toujours ; la mise en jeu part au pas « Resolve Character Setup Abilities » (après la pioche et les mulligans). Conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 10, REC 6, main 6. Conforme.
- [x] Étape 7 : cas : Griffes en jeu au départ, forme AlterEgo ; valeurs imprimées. Substitution : rouges 1/2 (valeurs imprimées).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : aucune partie humaine.

### uw002 : * Wolverine's Claws — PERMANENT. WEAPON. Pas de coût, [wild] imprimée.

Resource : Exhaust Wolverine's Claws → generate a [wild] resource for an ATTACK event. That event deals 1 additional damage (to a maximum of 3) for each card you discarded from your hand at random this round.

- [x] Étape 2 : carte(s) de référence : `54002` Cybernetic Arm (`CanGenerateResources(.., for_card=CardFinder2("ATTACK", Event), ex_operation=..)` + temp `WhenUnitWouldAttack` + `DealAdditionalDamage`) ; compteur `world.stat.CountRandomDiscards` (CORRECTIF moteur).
- [x] Étape 5 : mots-pièges : « AT RANDOM » (défausse choisie : rien) ; « THIS round » (reset en fin de round) ; plafond 3 ; « THAT event » : chaque attaque de l'événement reçoit le bonus ; la défausse qui PAIE l'événement compte. Conforme.
- [x] Étape 6 : nombres texte ↔ code : Aucun nombre sauf le plafond 3 et +1 par carte. Conforme.
- [x] Étape 7 : cas : payent Fury : 2+2+1=5 ; plafond (4 avant + coût) : 7 ; 2 avant + coût : 7 ; témoin défausses choisies : 5 ; reset au round suivant : 5 ; témoin non-ATTACK (Last Resort) reste en main. Substitution : rouges 5/6.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : question en attente (bonus par attaque ou par événement) + aucune partie humaine.

### uw003 : * Phoenix (Jean Grey) — allié EARTH-6160. Coût 3, PV 3, ATK 1*, THW 2*, [physical].

Hero Interrupt : When Phoenix is discarded from your hand at random, put her into play under your control.

- [x] Étape 2 : carte(s) de référence : `27087b` / `ap101` (`WhenCardWouldDiscard` sur la carte elle-même en main, `NoOutOfPlayLimit().NoGameAreaLimit()`) ; `27040` (`face.PutIntoPlay(joueur, effect)`).
- [x] Étape 5 : mots-pièges : « AT RANDOM » (marque `world.defausses_au_hasard`) ; « Hero » ; remplacée = jamais dans la défausse (pas comptée pour les Griffes ni Winter Mask) ; son coût 3 fait quand même le X de la carte qui l'a tirée. Conforme.
- [x] Étape 6 : nombres texte ↔ code : Coût 3, PV 3 ; X=3 mesuré (2+3=5). Conforme.
- [x] Étape 7 : cas : tirée par le coût de Fury : en jeu, pas défaussée, 2+3=5 ; hors coût : en jeu ; témoin défausse choisie : dans la défausse ; témoin alter ego : dans la défausse ; valeurs imprimées. Substitution : rouges 3/6 (verts sans module : les trois témoins « reste défaussée »/« pas de déclenchement », assumés).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : question en attente (une carte remplacée par Phoenix est-elle « défaussée » ?) + aucune partie humaine.

### uw004 : Deranged Burst — ATTACK, x2. Coût 2, [physical].

Hero Action (attack) : Discard 1 card from your hand at random → deal 6 damage to an enemy, this attack deals X additional damage, where X is equal to the numeral in the printed resource cost of that card. If you exhausted Wolverine's Claws to play this card, this attack gains piercing.

- [x] Étape 2 : carte(s) de référence : `35010` Lunging Strike (« if you exhausted Wolverine's Claws ... gains overkill ») ; `tj004` (`effect.context.paid_this_res_effects`) pour lire QUI a payé ; `CoutDefausseAuHasard()`.
- [x] Étape 5 : mots-pièges : « at random » ; « THAT card » (la défaussée) ; « PRINTED resource cost » (0 sans coût imprimé) ; « exhausted Claws to PLAY » (la ressource des Griffes a payé). Conforme.
- [x] Étape 6 : nombres texte ↔ code : 6 dégâts, coût 2, X = coût imprimé : 6+2=8, 6+4=10, 6+0=6. Conforme.
- [x] Étape 7 : cas : 8, 10, 0 (X=0 → 6), perforante avec Griffes (Tough traversé), témoin sans Griffes (Tough absorbe), témoin seule autre carte payée (reste en main). Substitution : rouges 5/6 (vert : le témoin « seule autre carte », assumé).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : aucune partie humaine.

### uw005 : Wild Slash — ATTACK, x2. Coût 0, [energy].

Hero Action : Discard 1 card from your hand at random → make the following attack up to X times, where X is equal to the numeral in the printed resource cost of that card : • Take 1 damage → deal 3 damage to an enemy.

- [x] Étape 2 : carte(s) de référence : `35009` Slice and Dice (« Make the following 2 attacks » : `ChooseAbilities(ForChoiceAbility(..).SetLabel('attack').SetTarget(Enemy))` + `this.AttackDamage`, aucun libellé sur l'événement) ; `35008` (`TakeDamage`, `MayChooseOneAbility`).
- [x] Étape 5 : mots-pièges : « up to X TIMES » (Cancel offert) ; chaque attaque = instance distincte ; « Hero Action » sans « (attack) » imprimé, comme Slice and Dice. Conforme.
- [x] Étape 6 : nombres texte ↔ code : 3 dégâts, 1 dégât subi, X=2 → 6 / 2 ; X=4 → 12 / 4 ; X=0 → rien. Conforme.
- [x] Étape 7 : cas : X=2, X=4, X=0, témoin Cancel. Substitution : rouges 2/4 (verts : X=0 et Cancel, assumés).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : aucune partie humaine.

### uw006 : Berserker Fury — ATTACK, x2. Coût 1, [physical].

Hero Action (attack) : Discard 1 card from your hand at random → deal 2 damage to an enemy. This attack deals X additional damage ... If this attack defeated an enemy, you may take 2 damage to repeat this ability.

- [x] Étape 2 : carte(s) de référence : `35008` Berserker Barrage (MÊME phrase de répétition : temp `AfterUnitDefeatedUnitInternal` + `MayChooseOneAbility`).
- [x] Étape 5 : mots-pièges : « repeat this ability » : **ARBITRAGE DU 26/10/2026 (FAQ RR v1.8, Across the Spider-Verse : « repeating the ability on this card includes the repeat effect itself »)** : répéter = rejouer la capacité EN ENTIER, coût compris : NOUVELLE défausse au hasard (nouveau X), main vide = répétition non proposée, et la répétition peut elle-même se répéter. Différence avec 35008 (pas de coût avant la flèche). Conforme.
- [x] Étape 6 : nombres texte ↔ code : 2 dégâts + X, 2 dégâts subis pour répéter. Conforme.
- [x] Étape 7 : cas : sans Griffes 4 ; avec Griffes 5 ; victoire + main vide → répétition IMPOSSIBLE (Rhino intact, 0 dégât subi) ; victoire + 2e carte en main (01022 X=2, 01021 X=4) → 2 dégâts subis, NOUVELLE défausse, Rhino 2 + 4 = 6 ; témoin sans victoire ; témoin répétition déclinée. Les deux cas de répétition étaient ROUGES avec l'ancien code (Rhino 4 au lieu de 0 / 6, 01021 non défaussée). Substitution : rouges 6/6.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : partie humaine non faite. Question de règle TRANCHÉE le 26/10/2026 (la répétition repaie le coût, FAQ RR v1.8). À vérifier en partie : la défausse au hasard de la répétition se fait bien après les 2 dégâts, et la répétition suivante est reproposée si elle vainc encore.

### uw007 : Last Resort — SUPERPOWER. THWART. x2. Coût 1, [mental].

Hero Action (thwart) : Discard 1 card from your hand at random → remove 1 threat from a scheme. Remove X additional threat from that scheme, ... If this removes the last threat from that scheme, draw 2 cards.

- [x] Étape 2 : carte(s) de référence : `35011` Track by Scent (`RemoveThreatFromSchemes(.., if_this_remove_last_threat=..)`).
- [x] Étape 5 : mots-pièges : UN seul complot (« THAT scheme ») : 1+X d'un coup ; « the LAST threat » = le complot tombe à 0. Conforme.
- [x] Étape 6 : nombres texte ↔ code : 1 + X menaces ; pioche 2. Conforme.
- [x] Étape 7 : cas : 6 → 3 sans pioche ; 3 → 0 : pioche 2 ; témoin 5 → 2 sans pioche. Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : aucune partie humaine.

### uw008 : Desperate Regenerate — SUPERPOWER. x2. Coût 2, [energy].

Action : Draw 2 cards. Discard 1 card from your hand at random. Choose : • Heal 3 damage from your identity. • Discard each stunned and confused status card from your identity.

- [x] Étape 2 : carte(s) de référence : `35012` Regenerative Healing (même choix) + `DiscardRandomHandCards`.
- [x] Étape 5 : mots-pièges : Ordre : piocher puis défausser (la carte piochée peut être tirée) ; la carte jouée est exclue du tirage ; pas de condition d'identité (elle pioche toujours). Conforme.
- [x] Étape 6 : nombres texte ↔ code : Pioche 2, défausse 1, soigne 3. Conforme.
- [x] Étape 7 : cas : soigne 3 (5 → 2, main 2) ; identité étourdie sans dégât ; sans dégât ni statut elle pioche et défausse. Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : aucune partie humaine.

### uw009 : * Winter Mask — amélioration EARTH-6160. ITEM. Coût 2, [mental].

Hero Response : After you discard a card from your hand at random, take 1 damage → draw 1 card.

- [x] Étape 2 : carte(s) de référence : `01027`/`35012` (`CostFunc.TakeDamage(1, "Initiator")` + `DrawUp`) ; `40043` (`AfterCardDiscardInternal`) ; marque `world.defausses_au_hasard`.
- [x] Étape 5 : mots-pièges : « YOU discard » (le propriétaire de la carte défaussée est le porteur) ; « at random » ; une Response par carte tirée ; la défausse qui paie une autre carte l'offre en plein coût (mesuré, ça passe). Conforme.
- [x] Étape 6 : nombres texte ↔ code : 1 dégât, 1 carte. Conforme.
- [x] Étape 7 : cas : hero : 1 dégât + 1 carte ; témoin défausse choisie ; témoin alter ego ; avec Fury (la défausse du coût la déclenche) ; Phoenix remplacée : rien. Substitution : rouges 2/5 (verts : les témoins « ne se déclenche pas », assumés).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : question en attente (une Response par carte tirée ; timing en plein paiement) + aucune partie humaine.

### uw010 : Adamantium Skeleton — Coût 2, [physical].

You get +4 hit points. Winter Soldier gets +1 ATK and his basic attacks gain piercing.

- [x] Étape 2 : carte(s) de référence : `35004` Adamantium Skeleton (texte identique, « Wolverine » → « Winter Soldier »).
- [x] Étape 5 : mots-pièges : « You » = identité (deux faces) ; « Winter Soldier » = face héros seulement ; piercing visé sur `"You"` (le propriétaire) et non sur le nom, qui désignerait aussi le Winter Soldier officiel. Conforme.
- [x] Étape 6 : nombres texte ↔ code : +4 PV, +1 ATQ. Conforme.
- [x] Étape 7 : cas : PV 14 / ATQ 3 ; contre-cas alter ego (+4 PV seulement) ; attaque de base perforante (3 dégâts, Tough tombe) ; témoin sans la carte (0). Substitution : rouges 3/4 (vert : le témoin sans la carte).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : aucune partie humaine.

### uw011 : Mission Objective — amélioration. Coût 2, [mental].

Hero form only. Attach to a minion. Hero Response : After the attached minion is defeated by Winter Soldier, remove 3 threat from a scheme. Winter Soldier may take 1 damage to attach this card to another minion.

- [x] Étape 2 : carte(s) de référence : `01007` Spider-Tracer (`CanPlayThisUpgradeCard(Minion)` + `SetTarget(Scheme2)`) ; `pd002` (`AttachTo2` pour déplacer).
- [x] Étape 5 : mots-pièges : ⚠ Fenêtre `WhenUnitBeDefeated` (HeroResponse), PAS `AfterUnitBeDefeated` (envoyé après la défausse des attachements : muet) ; « BY Winter Soldier » : le tueur est le héros du propriétaire ou un événement de ce joueur ; « another minion » : le sbire vaincu est exclu. Conforme.
- [x] Étape 6 : nombres texte ↔ code : 3 menaces, 1 dégât. Conforme.
- [x] Étape 7 : cas : jouée (forme héros) ; témoin alter ego (reste en main) ; vaincu par le héros : 5 → 2 ; autre sbire : rattachée + 1 dégât ; témoin mort d'autre chose (rien). Substitution : rouges 4/5 (vert : le témoin alter ego).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (cas plateau `new-ultimate-winter-soldier-plateau.test.ts`, vert d'emblée : rendu générique).

Carte terminée : NON (provisoire) : question en attente (« après » rendu avant la défausse du sbire ; événements du héros comptés comme « par Winter Soldier ») + aucune partie humaine.

### uw012 : "This is Your Enemy" — amélioration. Coût 1, [mental].

Hero form only. Attach to a minion. Hero Response : After the attached minion is defeated by Winter Soldier, Winter Soldier draws 3 cards and discards 1 card from his hand at random.

- [x] Étape 2 : carte(s) de référence : `uw011` (même déclencheur et même fenêtre) ; `01007`.
- [x] Étape 5 : mots-pièges : Piocher PUIS défausser au hasard (vraie défausse au hasard : compte pour les Griffes). Conforme.
- [x] Étape 6 : nombres texte ↔ code : 3 cartes, 1 défausse. Conforme.
- [x] Étape 7 : cas : jouée (attachée) ; vaincu par le héros : main 1 → 3 ; témoin autre cause : main 1. Substitution : rouges 2/3 (vert : le témoin « jouée » compté avec le cas d'attache).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (même cas plateau).

Carte terminée : NON (provisoire) : même question que uw011 + aucune partie humaine.

### uw013 : Live with the Burden — obligation de Logan. Boost 1.

Give to the Logan player. When Revealed : Discard 1 card from your hand at random. Take X damage, where X is equal to the numeral in the printed resource cost of that card. You may exhaust your identity to prevent 2 of that damage. Discard this card.

- [x] Étape 2 : carte(s) de référence : `42024` (`WhenThisObligationRevealed`, `GetGaveToPlayer`) ; `hc013` (défausser l'obligation explicitement).
- [x] Étape 5 : mots-pièges : Dégâts (pas indirects) ; « you MAY exhaust » (identité prête requise) ; on ne prévient jamais plus que X ; la carte se défausse dans tous les cas. Conforme.
- [x] Étape 6 : nombres texte ↔ code : Boost 1, prévention 2. Conforme.
- [x] Étape 7 : cas : coût 3 → 1 dégât + identité inclinée ; refus (Cancel) → 3 ; X=0 → 0. Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : aucune partie humaine.

### uw014 : Directorate X — complot annexe de l'ennemi juré. Menace de départ 2 par joueur.

Forced Response : After the villain phase ends, if Alonya Prostovich is in play, the engaged player discards cards from the encounter deck until a minion is discarded and reveal it. If it is not in play, the first player finds it and reveals it.

- [x] Étape 2 : carte(s) de référence : `pu114` Punisher's Armory (`Worlds.DiscardEncounterCardsUntil` + `Reveal`) ; `54037` Whiteout (`Find.FindAndReveal`) ; `AfterPhaseEnd(ForcedResponse, "Villain", ..)`.
- [x] Étape 5 : mots-pièges : TEXTE AMBIGU (« it » deux fois, « the engaged player ») : lecture provisoire, Alonya en jeu → le joueur avec qui elle est engagée défausse jusqu'à un sbire et le révèle ; Alonya absente → le premier joueur la cherche et la révèle. Conforme.
- [x] Étape 6 : nombres texte ↔ code : Menace 2 par joueur. Conforme.
- [x] Étape 7 : cas : Alonya absente : trouvée et révélée ; Alonya en jeu : sbire révélé (01103) ; valeurs imprimées. Substitution : rouges 2/3 (vert : les valeurs imprimées).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : QUESTION EN ATTENTE (lecture du texte).

### uw015 : * Alonya Prostovich — sbire némésis. EARTH-6160. DIRECTORATE X. PV 3, ATK ★, SCH ★, boost ★ seul.

[star] Forced Interrupt : When Alonya Prostovich activates, place 2 threat on each scheme instead. [star] Boost : Reveal this card.

- [x] Étape 2 : carte(s) de référence : `hc014` (`WhenEnemyWouldActivate`) ; `SetBeInstead` ; `PlaceThreatOnSchemes("EachScheme", ..)` ; `16140`/`pu114` (« Boost: Reveal this card » = `WhenCardBecomeBoost("This", RevealThisCard)`).
- [x] Étape 5 : mots-pièges : « instead » : ni attaque ni manigance ; « EACH scheme » (principal + annexes) ; ATK ★ / SCH ★ sans chiffre : 0 dans `desc`, valeur sans effet puisque l'activation est remplacée. Conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 3. ATK/SCH ★ = 0 (choix provisoire).
- [x] Étape 7 : cas : alter ego : +2 principal et +2 annexe ; forme héros : idem sans attaque ; boost : révélée ; valeurs imprimées. Substitution : rouges 3/4 (vert : valeurs imprimées).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucun attachement ni changement de zone propre).

Carte terminée : NON (provisoire) : question mineure en attente (valeur des ★ ATK/SCH) + aucune partie humaine.

### uw016 : Phoenix Specimen Brainwashing — attachement némésis. PSIONIC. Pas d'icône de boost.

Attach to your identity. [star] Forced Response : After the end of the villain phase, discard 1 card from your hand at random, place X threat on a scheme, where X is equal to the numeral in the printed resource cost of that card. Hero Action : Spend a [mental] resource → discard this card.

- [x] Étape 2 : carte(s) de référence : `tg016` Chomped (`AttachToFaceWhenPutIntoPlay("YourIdentity")`) ; `AfterPhaseEnd` ; `.SetCost(Cost("B"))`.
- [x] Étape 5 : mots-pièges : ⚠ `SetTarget(Scheme2, can_place_threat=True)` OBLIGATOIRE (sans, aucune cible, rien ne se pose, sans erreur) ; X dépend de la carte tirée : le choix du complot se fait après la défausse. Conforme.
- [x] Étape 6 : nombres texte ↔ code : X = coût imprimé. Conforme.
- [x] Étape 7 : cas : coût 3 → 3 menaces ; Energy → 0 ; Hero Action payée en mental → hors jeu. Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (cas plateau).

Carte terminée : NON (provisoire) : aucune partie humaine.

### uw017 : * X-S Sentinel I — sbire. EARTH-6160. SENTINEL. PV 8, ATK 3★, SCH 1, boost ★ + 2.

[star] X-S Sentinel I's attack gains ranged, overkill and piercing. [star] Boost : This attack gains ranged, overkill and piercing.

- [x] Étape 2 : carte(s) de référence : `ho016` Bullseye (`UnitAttackGainKeyword("This", ..)`) ; `an013` (boost, `would_atk_message` via `getattr`).
- [x] Étape 5 : mots-pièges : Seul le piercing est observable en cas (Tough traverse) ; ranged et overkill sont posés par la même fabrique. Conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 8, ATK 3, SCH 1, boost 2+★. Conforme.
- [x] Étape 7 : cas : attaque perforante (3 dégâts, Tough tombe) ; témoin Shocker (0) ; boost donné à Rhino : traverse ; valeurs imprimées. Substitution : rouges 2/4 (verts : témoin et valeurs imprimées).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (cas plateau).

Carte terminée : NON (provisoire) : ranged et overkill non mesurés (pas de riposte ni d'excès dans les cas) + aucune partie humaine.

### uw018 : * X-S Sentinel II — sbire. EARTH-6160. SENTINEL. PV 7, ATK 1★, SCH 1★, boost 3. QUICKSTRIKE. VILLAINOUS.

Quickstrike. Villainous. [star] Forced Response : After X-S Sentinel II activates, heal 3 damage from X-S Sentinel II.

- [x] Étape 2 : carte(s) de référence : Quickstrike et Villainous natifs (`desc`) ; `ap005a` (`AfterEnemyActivationEnd`).
- [x] Étape 5 : mots-pièges : « activates » (attaque OU manigance) ; un statut Sonné qui remplace l'activation n'envoie pas ce message (RECETTES §25). Conforme.
- [x] Étape 6 : nombres texte ↔ code : PV 7, ATK 1, SCH 1, boost 3. Conforme.
- [x] Étape 7 : cas : attaque immédiate à l'engagement (1 dégât) ; 4 dégâts → 1 après activation ; valeurs imprimées. Substitution : rouges 1/3 (verts : Quickstrike natif et valeurs imprimées, assumés).
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay : voir le bilan du héros ci-dessous.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (cas plateau).

Carte terminée : NON (provisoire) : aucune partie humaine.

## Bilan du héros (25/10/2026)

- **Cas** : `[uw]` **73/73 verts** (aucune exception avalée avec `MCLCG_TRACE_CRASH`). **Substitution** (`tools/substituer_pack.py .game-src <port> uw0`, carte par carte, pack restauré à l'identique) :
  19/19 cartes avec au moins un cas rouge sans leur module.
- **Statique** : `test_cards.py` 7520 modules OK (1 erreur hors pack : `roz/roz_nemesis/rz020`, pack d'une autre session) ; `verifier_api_cartes` : rien sur le pack ;
  `verifier_prefixes` OK ; `verifier_traductions_fr` OK ; `verifier_appels_modules` OK et **calibré** (un appel inventé `this.RetirerMenaceInexistante` dans `uw007` a été vu,
  puis retiré).
- **Decks** : `new_ultimate_winter_soldier` « identite uw001a, main 6, deck 9 » ; passe complète **161/161**.
- **Autoplay** : 8 parties (rhino/klaw × équilibré/agressif × 2) du héros et 8 du Wolverine officiel en témoin : 0 traceback sur les 16 journaux, 0 blocage, 0 victoire des
  deux côtés (le pilote), 6 à 7,5 rounds contre 4 à 5 pour le témoin. 747 lignes de journal montrent les événements du pack joués.
- **UI** : `textes-fr-fanmade`, `vocabulaire-*` (nouveau cas des six boutons), `new-ultimate-winter-soldier-plateau` verts.
- **Non fait** : partie humaine ; survol de la biographie dans l'assistant ; ranged et overkill de X-S Sentinel I (non observables dans les cas).

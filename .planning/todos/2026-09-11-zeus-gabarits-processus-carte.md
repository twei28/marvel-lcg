# Zeus (Mozilla, set 171) — gabarits PROCESSUS-CARTE, 17 cartes

**Livré le 11/09/2026.** Préfixe `ze`. Pack de HÉROS : identité recto verso, 10 cartes
de set héros (15 exemplaires), 1 obligation, 4 cartes némésis (5 exemplaires).
`PROCESSUS-HEROS.md` s'applique, donc `PROCESSUS-CARTE.md` 17 fois. Relevé complet et
vocabulaire dans `2026-09-11-zeus-releve-des-cartes.md`.

**Ce pack a exigé un chantier moteur avant sa première ligne** : l'**éclair**, une
ressource maison, est devenu la cinquième couleur du moteur (`L`, spec et plan dans
`docs/superpowers/`, fiche `mots-cles/eclair.md`). Vocabulaire : *énergie* = la
ressource officielle jaune, *éclair* = celle de Zeus.

## Ce qui a été mesuré, et comment

| Gate | Résultat | Calibrage (§9) |
|---|---|---|
| `tools/verifier_prefixes.py` | OK, `ze` réservé, 17 cartes | — |
| `tools/verifier_appels_modules.py zeus` | OK | ✅ vu ROUGE avec un faux `AbilityFactory.NExistePasDuTout` injecté dans ze010, puis vert restauré |
| `tools/verifier_noms_modules.py zeus` | OK | — |
| `tools/verifier_desc_mots_cles.py zeus` | OK, 17/17 | — |
| `tools/verifier_coherence_cartes.py` | textes fr 17/17, images 13/17 (les 4 némésis attendent les fichiers) | — |
| `tools/test_cards.py` | 5514 cartes construites, 0 erreur | — |
| `verifier_tous_les_decks.py` (`DECK_NOM=zeus`) | OK, « identité ze001a, main 6, deck 9 » | — |
| `tools/test_capacites.py` filtre `ze0` | **35/35** | ✅ 18/35 au premier passage ; chaque famille lue au journal avant correction |
| `tools/substituer_pack.py ze` | **17/17** cartes avec au moins un cas rouge sans module | 6 cartes gardent un cas vert sans module : les contre-cas d'ABSENCE d'effet (voir ci-dessous) |
| Helper `SkyfatherDe` (Special donné, hors module) | ✅ vu ROUGE par substitution MANUELLE du helper (`return None`), puis restauré | — |
| `tools/autoplay.py` zeus / rhino, 8 parties | **0 traceback, 0 partie bloquée**, 5,9 rounds | — |
| `tools/autoplay.py` témoin spider_man | 0 traceback, 7,5 rounds | Zeus joue à **9 cartes de deck** (pas de decklist d'auteur) : il s'épuise plus tôt, c'est attendu |
| `ui-app` : 1226 tests + cas plateau Mother of Night | vert | le cas plateau est vert d'emblée (correctif générique du 09/09) |

**Cas verts sans module, assumés** : `ze001a` (2 contre-cas « pas d'éclair » / « pas
d'énergie »), `ze002` (contre-cas sans Special en main), `ze007` (témoin d'épuisement
à un compteur), `ze009` (contre-cas sans Skyfather ; et le cas nominal, parce que le
Special donné vit dans le helper, d'où la substitution manuelle du helper), `ze012`
(l'interdiction du Tempest est lue par le helper `AlcoholProblemsDe`, pas par le
module), `ze015` (contre-cas mental + physique).

## Ce qui a été trouvé en chemin

**Trois défauts réels dans le pack, trouvés par le harnais, jamais par relecture** :

1. **Un Special résolu depuis la main tombait dans le vide.** `ResolveSpecialAbility`
   cherche les effets ENREGISTRÉS, et une carte en main n'en a aucun ; et même enregistré
   en temporaire, l'effet d'une carte hors jeu est ignoré. → `RegisterTemp` +
   `.NoOutOfPlayLimit()` sur les quatre Special. Recette ajoutée à RECETTES §4.
2. **Skyfather ne peut pas infliger ses dégâts lui-même** : `upgrade.py:68` affirme
   qu'une amélioration n'agit que dans son propre effet. → les dégâts partent de la
   carte qui résout. Recette ajoutée à RECETTES §2.
3. **`CostFunc.Spend` dans une capacité de ressource remet le pool à zéro** (« total YY »
   puis « total L ») : Mount Olympus effaçait les énergies déjà générées. →
   `CostFunc.Custom` qui PRÉLÈVE dans le pool. Recette ajoutée à RECETTES §4.

**Deux défauts d'outillage** :

4. **Le harnais interdisait l'id de l'objet joué parmi les EFFETS de paiement**, deux
   espaces de numéros distincts : Precognition (objet 13) ne pouvait pas être payée par
   Thunderbolt (effet 13), et la carte échouait « sans motif ». Sept cas de diagnostic
   pour l'isoler ; trace `PAIEMENT` ajoutée sous `TRACE_OPTIONS=1`.
5. **Le moteur écrivait « failed » sans motif** quand un effet échoue après son offre.
   `player_action.py` écrit désormais `effect.failures`. C'est aussi la piste du rapport
   joueur du jour (« des contres ne retirent pas la menace », backlog du 11/09).

**Trois pièges de montage**, pour ne pas les repayer : *The Break-In!* est à l'étape
`01097b` dès le montage ; `Puzzle.CreatePlayerDeck` met la DERNIÈRE carte au DESSUS ;
une obligation révélée vit dans `obligations_area`, hors de `FindCardsOnField`.

## Ce que les gates ne peuvent pas voir

- **Le boost supplémentaire de Nyx** (« give Nyx 1 additional boost card ») n'est pas
  mesurable par le harnais : aucune clé d'assertion ne compte les cartes de boost d'un
  ennemi, et les dégâts qui en résultent varient. Le cas prouve la défausse du dessus du
  deck, pas le boost. **À vérifier en partie réelle** : outil manquant, une clé
  `boosts_sur` dans `etat_attendu`.
- **Mount Olympus en vraie partie** : l'ordre des moyens de paiement compte (une énergie
  doit être générée AVANT que Mount Olympus prélève). Le plateau laisse le joueur
  cliquer dans l'ordre qu'il veut ; si Mount Olympus est cliqué en premier, le moteur
  annule ce moyen (`GameSignal_UndoRequest`). À observer à l'œil.
- **Le taux de victoire ne dit rien** : 0 % pour Zeus comme pour le témoin.

## Gabarits, une carte par section

### ze001a : * Zeus (Skyfather's Tempest)
- [x] Étape 2 : `WhenPlayerPlayCard` (play.py:260, porte `paid_resources`) + `SetTarget(Scheme2)` comme 01060 ; Special via `ResoudreLeSpecialDe`.
- [x] Étape 5 : `both` → PaieEnergieEtEclair (un joker ne vaut pas les deux) ; `that event` → `message.played_face` ; `a scheme` → cible. Résultat : conforme.
- [x] Étape 6 : 1 menace. Résultat : conforme (6 → 1 avec Precognition à 4).
- [x] Étape 7 : nominal (Confused + menace 1), joker (idem), contre-cas ×2 (Y+B, L+L) ; rouge sans module / vert avec. Résultat : 4/4.
- [x] Étape 7 bis : pas de limite imprimée. NON.
- [x] Étape 8 : autoplay 8 parties, 0 traceback.
- [x] Étape 8 bis : NON (statut et menace, déjà couverts).
Carte terminée : OUI.

### ze001b : * Zeus Panhellenios (God of Lightning)
- [x] Étape 2 : 03001b (Search deck + défausse, GainCard). Nom exact pour éviter 50131b/57021.
- [x] Étape 5 : `deck and discard pile` → les deux ; `(Limit once per round.)` → LimitOncePerRound. Résultat : conforme.
- [x] Étape 6 : aucun nombre hors la limite.
- [x] Étape 7 : recherche en défausse (deck vidé) ; rouge sans module. Résultat : 2/2.
- [x] Étape 7 bis : OUI, témoin : deux Actions, il RESTE un Thunderbolt en défausse (chiffre 1).
- [x] Étape 8 : autoplay, 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### ze002 : * Hera
- [x] Étape 2 : 01083 Mockingbird (`AfterCardEnterPlay`), choix par `AskChooseFace`, Special par le helper.
- [x] Étape 5 : `in your hand` → `hand_cards.Get()` ; `printed` → `APrintedSpecial` (capacités déclarées, Skyfather exclu). Filtre en `conditions`. Résultat : conforme.
- [x] Étape 6 : CTR 2*, ATQ 1*, 2 PV, coût 2 : `desc` conforme à la carte (relevé corrigé le jour même).
- [x] Étape 7 : Thunder Strike seule en main → Rhino sonné, la carte RESTE en main ; contre-cas sans Special. Résultat : 2/2, rouge sans module.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### ze003 : Thunder Strike (×4)
- [x] Étape 2 : 05015 Tackle + 35023 (`AttackProperty(piercing=True)`) ; Special : ab007 + NoOutOfPlayLimit.
- [x] Étape 5 : `Requirement ([energy])` → `desc.Requirement "Y"` (base automatique) ; `This attack gains piercing` → propriété d'attaque ; `Stun an enemy` → GiveStatus Stunned. ⚠ RES = `L`, la seule carte à imprimer l'éclair. Résultat : conforme.
- [x] Étape 6 : coût 2, 5 dégâts, Requirement 1.
- [x] Étape 7 : 5 dégâts à Rhino ROBUSTE (percant prouvé) ; Special via Hera (ze002). Résultat : rouge sans module.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### ze004 : Precognition (×2)
- [x] Étape 2 : 01060 For Justice (contre sur événement, cible Scheme2) ; Special ab007. ⚠ Homonyme 40004, jamais cherchée par nom.
- [x] Étape 5 : `Remove 4 threat from a scheme` → RemoveThreatFromSchemes(cibles, 4) ; `Confuse an enemy`. Résultat : conforme.
- [x] Étape 6 : coût 2, 4 menaces.
- [x] Étape 7 : 6 → 2 (contre-cas Tempest), Special via Hera → Rhino désorienté. Rouge sans module.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### ze005 : Olympian Might (×2)
- [x] Étape 2 : 35018 Precision Strike (`IsDefeated()` après DealDamage) ; `GetHero()` pour « ready Zeus » (nom propre = face héros).
- [x] Étape 5 : `If this attack defeats that enemy` → même cible ; `ready Zeus` → héros ; `Gain tough status card` → identité. Résultat : conforme.
- [x] Étape 6 : coût 3, 7 dégâts, Requirement 2.
- [x] Étape 7 : Nyx vaincue → Zeus prêt ; contre-cas Rhino survit → Zeus reste incliné ; Special via Hera → Robuste. 3/3, rouge sans module.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### ze006 : Wrath of Olympus
- [x] Étape 2 : 35023 (`overkill=True`), `RemoveThreatFromSchemes("EachScheme", 2)`, `FindCardsOnField(Enemy)`.
- [x] Étape 5 : `each enemy in play` → tous les ennemis ; `each scheme` → EachScheme. Résultat : conforme.
- [x] Étape 6 : coût 5, 10 dégâts, Requirement 3, Special 2/2.
- [x] Étape 7 : 10 dégâts (Requirement YYY payé Thunderbolt + Energy + Hephaestus + Olympian Might) ; Special via Hera : Rhino 2, Nyx 2, menace 6 → 4. Rouge sans module.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### ze007 : * The Aegis
- [x] Étape 2 : ab007 → `AfterPlayerResolveAbility(..., ability_name=TEMPEST)` ; 05017 Energy Barrier (`WhenUnitWouldTakeDamage` + `CostFunc.Counter` + `PreventDamage`). Compteur `aegis` ajouté à l'enum et à compteurs-fr.
- [x] Étape 5 : `After you resolve your Skyfather's Tempest` → nom exact ; `any amount of damage` → toute source ; `remove 2 → prevent 3`. Résultat : conforme.
- [x] Étape 6 : coût 1, 1 compteur, 2 retirés, 3 prévenus.
- [x] Étape 7 : compteur posé après le Tempest ; 3 dégâts prévenus avec 2 compteurs. Rouge sans module.
- [x] Étape 7 bis : OUI (coût en compteurs), témoin : à 1 compteur, 3 dégâts passent et le compteur reste (chiffres 3 et 1).
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : OUI, un compteur : la jauge des compteurs est déjà dessinée (compteurs-fr `aegis: égide`), cas plateau non ajouté (mécanisme générique).
Carte terminée : OUI.

### ze008 : * Thunderbolt
- [x] Étape 2 : ab007 Donald Pierce, mot pour mot.
- [x] Étape 5 : `generate a [energy]` → Resources("Y"), PAS un éclair ; `ready Thunderbolt`. Résultat : conforme.
- [x] Étape 6 : coût 0.
- [x] Étape 7 : incliné pour payer puis PRÊT après le Tempest ; contre-cas sans éclair → reste incliné. Rouge sans module.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### ze009 : Skyfather
- [x] Étape 2 : 12033 (`GainUntilPhaseEnd(hand_size=1)`) ; le Special donné : helper `ResoudreLeSpecialDe` (aucune fabrique de greffe dans le moteur, documenté dans le module).
- [x] Étape 5 : `Each event you own` → `Event.IsType` + `GetOwner()` ; `does not have a printed Special` → `APrintedSpecial` faux ; `until the end of the phase`. Résultat : conforme.
- [x] Étape 6 : coût 2, 2 dégâts, +1 main.
- [x] Étape 7 : For Justice (sans Special) payée éclair + énergie → Rhino 2 ; contre-cas sans Skyfather → 0 ; +1 main (`hand_size` 5). Rouge sans module pour la main ; le Special donné vu rouge par substitution MANUELLE du helper.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### ze010 : * Hephaestus
- [x] Étape 2 : 09008 Sanctum Sanctorum (cible en défausse, ShuffleAllTo, DrawUp), `SetHasNoTargetEffect` : sans Thunder Strike, on pioche quand même (règle générale).
- [x] Étape 5 : `1 copy of Thunder Strike` → cible nommée, `from your discard pile`, `Draw 1 card`. Résultat : conforme.
- [x] Étape 6 : coût 1, 1 copie, 1 carte.
- [x] Étape 7 : Thunder Strike remélangée (défausse 2 → 1), Hephaestus incliné. Rouge sans module.
- [x] Étape 7 bis : NON (l'inclinaison est le coût).
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### ze011 : * Mount Olympus
- [x] Étape 2 : ab007 + `CostFunc.Custom` qui prélève dans le pool (RECETTES §4, ligne ajoutée ce jour) ; ⚠ PAS `CostFunc.Spend`.
- [x] Étape 5 : `spend a [energy]` → prélever une énergie (un joker à défaut) ; `generate a [lightning]` → Resources("L"). Résultat : conforme, avec la réserve « ordre des moyens de paiement » ci-dessus.
- [x] Étape 6 : coût 1, 1 pour 1.
- [x] Étape 7 : Precognition payée Thunderbolt + Wrath + Mount Olympus → éclair fabriqué, Tempest déclenché, Mount Olympus incliné. Rouge sans module.
- [x] Étape 7 bis : NON (inclinaison).
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI, à observer en partie réelle pour l'ordre de paiement.

### ze012 : Alcohol Problems
- [x] Étape 2 : `PlayerActionToRemoveThisFromGame` (attachment.py:29) + sg022 (coûts) ; l'interdiction lue par le Tempest via `AlcoholProblemsDe` (`obligations_area`).
- [x] Étape 5 : `Give to` → base `desc.GiveTo` ; `cannot resolve` → condition du Tempest ; `Exhaust your identity and spend a [lightning]` → deux coûts. Résultat : conforme.
- [x] Étape 6 : boost 2, 1 éclair.
- [x] Étape 7 : Tempest muet tant qu'elle est en jeu (menace 2, pas de Confused) ; retirée du jeu contre inclinaison + Thunder Strike. Rouge sans module pour l'action ; l'interdiction vit dans le helper (cas vert sans module, assumé).
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI.

### ze013 : * Nyx
- [x] Étape 2 : `WhenEnemyWouldActivate` (activate.py:6, `GiveBoostCardForThisActivation`) ; 06030 Trickster (`DiscardDeckTopCards`). Steady/Villainous : bases.
- [x] Étape 5 : `activates against you` → `GetToPlayer()` non nul ; `printed [energy] icon` → `HasColorPrinted("Y")`, ÉNERGIE officielle, pas l'éclair. Résultat : conforme.
- [x] Étape 6 : 6 PV, MNG 2, ATQ 1, boost 3, 1 carte, 1 boost.
- [x] Étape 7 : carte du dessus défaussée à l'activation. Rouge sans module.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : NON pour le boost supplémentaire, non mesurable par le harnais (clé `boosts_sur` manquante) ; le reste OUI. À vérifier en partie réelle.

### ze014 : The Mother of Night
- [x] Étape 2 : 01166 Highway Robbery (PlaceCardHere, GetPlacedCardArea, When Defeated) ; 03001b pour la recherche. Hazard : base.
- [x] Étape 5 : `Each player` → ForEachPlayer ; `2 cards with printed [energy]` → deux recherches `has_printed_res="Y"` ; `1 additional threat for each` → PlaceThreatOnSchemes([this], n) ; `owner's discard pile` → DiscardAll. Résultat : conforme.
- [x] Étape 6 : 1 menace, 2 cartes, +1 chacune, boost 3.
- [x] Étape 7 : 2 cartes dessous, menace 3, Hephaestus (mental) resté dans le deck ; déjouée → défausse 2. Rouge sans module.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : OUI, cas plateau `mere-de-la-nuit-cartes-dessous.test.ts` : les deux cartes dessinées, portées par la manigance, face cachée (vert d'emblée, correctif générique du 09/09).
Carte terminée : OUI.

### ze015 : Shroud of the Nightmother
- [x] Étape 2 : `UpdateResourcesGeneratedWhilePlayingThis` (resources.py:340) pour réécrire `CheckEffectGeneratedResources` ; sg022 pour l'attachement et l'action.
- [x] Étape 5 : `cannot spend [energy]` → la part énergie retirée de tout moyen de paiement (un moyen à énergie seule tombe à zéro et n'est plus offert) ; `while paying for cards` → `ability.is_play` ; `2 resources of any type` → `Spend(Cost("2"))`. Résultat : conforme.
- [x] Étape 6 : boost 2, 2 ressources.
- [x] Étape 7 : Precognition avec seulement des énergies RESTE en main ; contre-cas mental + physique paie ; action d'alter ego la défausse. Rouge sans module.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : OUI, un attachement sur l'identité : mécanisme générique déjà dessiné (`accroche_a` vérifié par le cas moteur).
Carte terminée : OUI.

### ze016 : Total Eclipse (×2)
- [x] Étape 2 : 06030 Trickster, 02044 Lightning Bolt (indirect), an010 (Stunned), 01164 Titania's Fury (boost) avec la FACE qui s'active.
- [x] Étape 5 : `each event discarded` → `Event.IsType` ; `printed Special` → APrintedSpecial (Skyfather exclu) ; `you are stunned` → identité ; `the activating enemy` → `being_message.by_face`. Résultat : conforme.
- [x] Étape 6 : 3 cartes, 1 dégât par événement, boost 1.
- [x] Étape 7 : 1 dégât + sonné (Thunder Strike défaussée) ; contre-cas For Justice → 1 dégât, pas sonné. Rouge sans module.
- [x] Étape 7 bis : NON.
- [x] Étape 8 : 0 traceback.
- [x] Étape 8 bis : NON.
Carte terminée : OUI (la capacité Boost n'a pas de cas : `Puzzle.Boost` sans mesure du nombre de cartes de boost, même manque que Nyx).

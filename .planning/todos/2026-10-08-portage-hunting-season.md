# Portage HUNTING SEASON (fan-made, auteur Nugget, préfixe `hs`, pack `hunting_season`)

Source : `.planning/hunting-season/` (zip extrait le 08/10/2026 : LIRE_D_ABORD, SPECIFICATIONS,
POINTS_OUVERTS, `reference/` avec livret PDF, manifeste, 239 scans JPEG, `campaign_rules.py`).
Règles : PROCESSUS-CARTE.md par carte, questions une à une, aller au bout.

## Statut global (09/10/2026)

PORTAGE TERMINE : blocs 0 à 6 faits, textes français écrits, test d'écran du Lodge vert.
Rien n'est commité ni déployé : attendre le « déploie ». L'entrée « nouveautés » (fr + en, 2026-10-09)
est déjà écrite dans `public/js/prepare/nouveautes.js`. Au déploiement : `ui-app/deployer.sh`
(les textes FR vivent dans ui-app).

## Décisions
- 08/10/2026 : Swarmed by Rats (hs018/hs019) = **Response** (texte imprimé conservé, déclencheur « After »).
- 09/10/2026 : POINTS_OUVERTS n°8 tranché par l'utilisateur. Une défaite aux scénarios 1 à 4 fait CONTINUER la campagne (gains de défaite, visite du Lodge, scénario suivant). Seul le résultat contre Kraven décide de la fin de campagne.

## Blocs (un bloc entièrement vérifié avant le suivant)
0. Données : FAIT le 08/10/2026 (non commité, non déployé).
1. Vermin hs001-hs029 (31 entrées) + Feral Instincts hs141-145 + scénarios hs_vermin
2. Scorpion hs030-053
3. The Lizard hs054a-079 + Lizard Thralls hs146-150
4. Vulture hs080-103 + Red Vulture hs151-156
5. Kraven hs104-124 + Trap hs125-140 + Savage Six hs157-163
6. Campagne : Lodge hs164-199, récompenses hs200-205, expert hs206-221, Hunter hs222-226,
   `campaign_rules.py` (XP, marché partagé, Master Hunter, PV), écran.

## Bloc 0 : données (08/10/2026)
- `data/cards.json` : clé `hunting_season`, 239 entrées (clé `custom` retirée), checksum recalculé.
- `data/sets_info.json` : « 178. Custom (Hunting Season) » ; `tools/prefixes_fanmade.json` : `hs` déclaré.
- Copiés : 10 scénarios, 4 `encounter_sets`, `campagnes/hunting_season.json`, arbre
  `src/cards/pack/hunting_season/` (255 .py, 231 scripts VIDES `A_FAIRE_CLAUDE`).
- Images : 234 JPEG copiés dans `assets/pics/`, plus hs222 à hs226 en PNG pleine taille (1,2 à 2,4 Mo) extraits du zip de Downloads le 08/10/2026 : les 239 sont là.
- `verifier_prefixes` : aucun défaut `hs`. Les 20 défauts viennent du préfixe `rs` (Red Sonja) non
  déclaré, antérieur et hors périmètre.
- Pas encore chargé en jeu : valeurs dynamiques (HP=X, StartingThreat=X, `*`), DEF+ d'attachement,
  schéma de campagne insuffisant (POINTS_OUVERTS 3, 4, 5, 7).

## Corrections après lecture des scans (08/10/2026)
- hs109 : "per player" retiré (limite globale par round), confirmé par l utilisateur.
- hs121, hs122 : "Other characters cannot defend against this attack", confirmé.
- hs068/hs069 Boa Constricted : aucune icône de boost sur le scan, Boost 2 -> 0 (confirmé par l'utilisateur).
- hs117/hs118 : on garde « The villain », jamais le nom Kraven dans le texte (décision de l'utilisateur).
- hs092/hs093 Forcefully Elevated : aucune icône de boost sur le scan, Boost 1 -> 0 (confirmé).
- hs155/hs156 : deux icônes de boost sur le scan, Boost 1 -> 2 (confirmé).
- hs067 Ancient Reptilian Brain : l'ATK du scan est une étoile seule (valeur donnée par le texte), aucune clé numérique à ajouter ; à traiter au script du bloc Lizard.
- hs166 Black Cat : THW 1* confirmé sur le scan, rien à changer.
- hs224/hs226 : texte aligné sur le scan (« the main scheme », « 1 facedown », « Hunter Mode Only. »). À relire sur les scans hs222, hs223, hs225 pour « Hunter Mode Only. ».
- hs222/hs223/hs225 : « Hunter Mode Only. » ajouté (vu sur les scans). Les 5 cartes Hunter sont alignées.
- hs205 Lizard : texte du scan = Forced Interrupt « When Lizard attacks, the attack gains piercing » (et non un effet permanent). Corrigé.
- hs113 Hunting Rifle : « doesn't damage you » vs « take no damage » = même effet de jeu, laissé tel quel.
- hs129-134 pièges : le scan n'a pas le libellé « When Revealed » (la carte est dévoilée à la donne). On garde le libellé dans le JSON car le moteur s'en sert pour déclencher l'effet, sans effet de jeu différent.
- Passe « écarts scan vs ChatGPT » close le 08/10 : restent les étoiles de stats (hs036, hs044, hs077, Lizard) et hs141 (SCH étoilé) à traiter dans le script de chaque carte au bloc concerné, pas avant.

## Bloc 1 : Vermin hs001-029 + Feral Instincts hs141-145 (08/10/2026)
- Scripts écrits (0 erreur `test_cards` : 6039 ok, 0 err). 20 cas `[hs1]` verts dans `test_capacites.py` (hs001/002/007/015/018/020/021/024/025/026-029/141/143/144/145).
- Corrigé en route : `FindAndPutIntoPlay` n'a pas `check_face_fn` (passer `finder=CardFinder(...)`) ; le guard de hs018/019 passe par `CardFinder(check_effect_fn=...)` + `change_on_event=[OnEvent.CardType(...), OnEvent.PlayAreaCard(Minion)]` (sinon assert `len(params) == 2`).
- Autoplay : 8 parties Vermin + 8 Rhino témoin, 0 incident, 0 victoire des deux côtés (pilote). Traces `ChoiceOne` AssertionError sur le choix de hs026-029 : réponse « 0 » du pilote avalée (documentée dans autoplay.py), parties non bloquées.
- Audits : verifier_api_cartes, audit_cartes, verifier_appels_modules propres pour `hs` ; verifier_prefixes : seuls les 20 défauts `rs` connus.
- Clôture (08/10/2026) : 33 cas `[hs1]` verts. Ajoutés : hs003 (scénario EXPERT seulement : `hs_vermin` ne liste que hs001/hs002), hs004a, hs004b + Special de hs006 (avance / n'avance pas, verificateur `hs_apres_etape_1`), hs005a, hs008/hs012 (Boost), hs016 (+ témoin sans Clone), hs022, hs142 (ATK+1 et Interrupt).
- Pièges de harnais : `CreateEncounterDeck` met le DERNIER argument sur le dessus ; hs007 est déjà en jeu à la mise en place (hs004a), donc `en_jeu: hs007` est vide de sens, utiliser hs012/hs013 ; l'attaque d'un héros se pilote par `cibles` (le 2e argument d'`Attack` est un DÉFENSEUR) ; `Puzzle.Attack('01001a')` pour le héros.
- Preuve par substitution : rouges pour hs003, hs004a, hs005a, hs002 (après réécriture du cas, il était vert sans module), hs008, hs012, hs020 à hs029. hs001, hs007, hs018 : 1 rouge sur 2 (le second est le témoin, normal). hs015 : Guard imprimé en data, module vide, normal.
- Doublons strictement identiques au script d'une carte testée (diff hors commentaires) : hs009/010 = hs008, hs011/013/014 = hs012, hs017 = hs016, hs019 = hs018, hs023 = hs022. hs007 = hs008.
- Étape 8 bis : aucune carte du bloc ne glisse ni ne pose sous une autre (hs018/019/142 s'attachent à un niveau, déjà couvert) : rien de plus à dessiner.
- NON FAIT : boost supplémentaire de hs016/017 ; hs005b ; `hs_vermin` joué de bout en bout ; icônes douteuses (hs020, hs021, hs142/144/145) ; textes français.
- Bloc 1 : fonctionnel, vert. Reste en fin de portage : textes français et icônes.

## Bloc 2 : Scorpion (hs030-053)

Statut : TERMINE.

- Cas harnais `[hs2]` : 47/47 verts. `test_cards` 6039 ok, `verifier_appels_modules` OK, autoplay `hs_scorpion` normal + expert 8 parties 0 incident, audits `hs` propres.
- Doublons assumes : hs049 = hs048, hs051 = hs050, hs053 = hs052, hs041 = hs040.
- Substitution : chaque script remplace par un stub fait tomber son cas ; empreinte du pack restauree a chaque fois. Temoins assumes. hs036 ATK+1 est en data.
- hs034a : le moteur avance seul une face A sans seuil de menace (`scheme_main.py` OnAfterCardRevealedEnd). Le script etait redondant, il est vide (comme hs004a). Le cas reste vert et garde le comportement.
- Corrections de script : hs050/hs051 alter-ego (+2 SCH si etourdi), hs044 `would_atk_message.GainPiercing`, hs045 `would_atk_message.GainOverKill`.
- Piege harnais : `EmptyEncounterDeck()` seul donne `IsGameOver` apres les boosts ; toujours recreer un deck. Le deck du scenario contient deja les cartes testees : le vider.
- Moteur : support `DEF+` (`has_modify.py`, `card_face.py`), a signaler.
- Etape 8 bis : `ui-app/src/board/hunting-season-queue-scorpion.test.ts` (Queue dessinee, rang Scorpion + 1, portee par Scorpion).
- Interpretation : l'icone de boost de Tail Enhancements compte les TAIL attaches a Scorpion et a sa Queue.

Carte terminee : OUI (bloc 2).

## Bloc 3 : The Lizard (hs054-079) + Lizard Thralls (hs146-150)

Statut : TERMINE (09/10/2026), non commité, non déployé.

- Cas harnais `[hs3]` : une soixantaine, verts. `test_cards` 6039 ok / 0 err. Autoplay `hs_the_lizard` normal + expert, 16 parties, 0 erreur (0 victoire, comme le témoin Rhino).
- Audits `hs` propres (verifier_api_cartes, audit_cartes, verifier_appels_modules, verifier_prefixes : seuls les 20 défauts `rs`).
- Substitution : rouge pour presque toutes les cartes, empreinte du pack restaurée (221a8628…). Témoins assumés : hs054a 4/5, hs060 2/3, hs061 2/3, hs063 2/3.
- Bug réel trouvé par l'autoplay : hs072/hs073 appelaient `GetHero()` en alter-ego. Corrigé (`heros_pret`), cas de régression ajouté.
- Moteur : compteur `shame` dans `COUNTER` (`card_face.py`) ; `Puzzle.EndVillainPhase()` (harnais). Plateau : nom français « honte » (`compteurs-fr.ts`, test ajouté). Le compteur lui-même est dessiné par le chemin générique `c_*`.
- Assumé : hs059b reste vert sans module. `Puzzle.Flip` en harnais ne reproduit pas un retournement du Lizard quand hs059b est en jeu (le flip ne se produit pas, même sans le module) et une vraie activation ne manigance pas dans ce montage. Le script est une interrupt simple (`SetBeInstead` sur `WhenCardWouldFlip`), même mécanisme que d'autres cartes testées.
- Assumé : hs065 « ranged » sans assertion d'état ; hs067 rebond testé seulement via Hero Action ; hs069/hs071 = copies.
- Étape 8 bis : pas de nouveau glissement/dessous ; honte couverte ci-dessus.
- NON FAIT : textes français (fin de portage).

Carte terminee : OUI (bloc 3), avec les écarts assumés ci-dessus.

## Bloc 4 : Vulture hs080-103 et Red Vulture hs151-156

Etat : 30 cartes ecrites, non committe.

Preuves :
- Harnais `[hs4]` : 52/52 (cas par carte, y compris restriction d'attaque hs080/081/082 avec temoin AERIAL, hs097/098/099, hs151, boosts hs085/086, actions hs084/088/090, hs094 vaincue).
- Substitution (empreinte du pack avant/apres identique, cf8f8d50648e1da33b825d34a0e8c13b) : toutes les cartes rouges. Les « 1/2 » (hs080, hs083b, hs088, hs096, hs097-099) sont des temoins d'absence d'effet, assumes.
- `test_cards` : ok 6039, err 0. Audits : rien sur Vulture/Red Vulture.
- Autoplay `hs_vulture` normal+expert, 8 parties chacun : 0 plantage, 0 victoire (le bot n'a pas AERIAL).
- Etape 8 bis : sans objet, aucun affichage nouveau (pas de changement de plateau).

Changements moteur : `trait.py` (`SuppressTrait`, perte temporaire de trait), `face_action.py` (`lose_trait` dans `TemporaryGain`, `GainUntilTurnEnd`, `GainUntilRoundEnd`).

Bugs trouves : unicite de nom Vulture / Vulture (James Natale) (ability `IgnoreUniqueRule`), double `Advance` de hs083a, hs089 et hs101 defaussaient le complot principal via `CostFunc.Discard("HandCard")`.

Ecarts assumes :
- Restriction d'attaque par `SetBeInstead` : l'epuisement paye est perdu, un ranged gagne plus tard n'est pas vu.
- « Si cette attaque vous blesse » : PV avant/apres, soins intermediaires non vus.
- `ResetTrait` (changement de face) efface la perte de trait.
- hs096 compte tous les personnages, ennemis compris.
- Non couvert : le choix « 1 menace » de hs083b (le pilote prend le premier choix) et le boost supplementaire de hs100/101.
- Observation non expliquee : `Puzzle.PlaceThreat('hs083b', 5)` inflige 5 degats a l'identite. A reproduire avant le bloc 6.

Carte terminee : OUI (hors les deux cas non couverts ci-dessus).

## Bloc 5 : Kraven hs104-124, Pieges hs125-140, Savage Six hs157-163

Etat : TERMINE le 09/10/2026, non committe, non deploye.

Preuves :
- Harnais `[hs5]` : 53 cas (51 + 2 Capture Net), executes. Les 51 premiers 51/51, hs131/132 2/2 apres correction.
- `test_cards` : ok 6039, err 0. `verifier_appels_modules hunting_season` : OK. `audit_cartes` et `verifier_api_cartes` : rien sur hs104-163 (seul hs143, bloc suivant).
- Substitution : empreinte du pack identique avant/apres (233e25a252212764c2f15f2406d26050). Rouges : hs104, 105, 106, 107b, 110, 111, 116-120, 123, 124, 129-134, 139, 157, 158 (et 1/2 ou 2/3 assumes pour 115, 125, 159, 160, 161, 163 : temoins d'absence d'effet).
- Autoplay `hs_kraven_the_hunter` normal et expert, 8 parties chacun : 0 victoire, 1 partie bloquee (expert, graine 6 : question forcee Spider-Sense a cible unique, epuisee par le garde-fou anti-repetition du pilote, artefact du bot). Un NameError reel est apparu AVANT correction.

Bug trouve par l'autoplay et que le harnais ne voyait pas : `PorteurEstAttaquant` absent de `trap/__init__.py` (hs131, hs132 plantaient a chaque attaque du porteur). Corrige, deux cas ajoutes.

Changements moteur : `worlds.py` (noms des paquets de pieges dans `ASIDE_DECK_NAME`).

Cloture (09/10/2026) :
- Cas `[hs5]` : 74/74 verts. Ajoutes : hs109 (+ temoin d'epuisement, + boost), hs112 (interruption payee), hs113 (Tough, temoin, interruption), hs114 (arme revelee, interruption), hs121/hs122 (heros et alter-ego), hs126 (riposte du Lion), hs127/hs128 (riposte percante), hs135/hs136/hs137 (confusion, degat, paiement mental), hs138 (degats, epuisement), hs162 (restriction, boost). Les cas mise en place et 108 portent maintenant hs107a et hs108a hs108b dans leur nom. Retires : 4 cas faibles verts sans module (hs112, hs126, hs135, hs138).
- Substitution : rouge pour chaque carte ci-dessus (hs113 2/3, le vert est le temoin « Kraven blesse normalement »). Empreinte du pack restauree (b58d31c5ef0e46381938a8d1c522a344).
- Bugs corriges : hs113 `Cost("11")` (onze ressources, interruption impayable) devient `Cost("2")` ; hs162 boost epuisait seulement en forme heros, le texte dit « your identity ».
- Harnais (moteur du bac a sable) : `Puzzle.FindOrCreateFace` fouille aussi les decks supplementaires du scenario. Avant, `Remove`/`Reveal` d'un piege fabriquaient un doublon hors du paquet. Consequence : le cas hs117 « avec un piege attache » attend 14 pieges (la Bear Trap revelee sort vraiment du paquet). Non-regression : cas Attack on Mount Athena, Across the Mojoverse, Infinity Gauntlet, Hercules (16) verts.
- Piege harnais : en alter-ego, Peter Parker produit une ressource mentale, les cas « sans ressource mentale » se jouent en forme heros. Le pilote accepte toujours une interruption optionnelle : la riposte de hs112 seule (interruption refusee) n'est pas testable, assumee.
- `test_cards` 6039 ok, 0 err.
- Autoplay, partie bloquee (expert, graine 6) relue : deux Big Game Hunter de suite, la question Spider-Sense (identite de Spider-Man) revient une 3e fois et le garde-fou anti-repetition du pilote la refuse. Artefact du pilote, pas un defaut du pack.
- Etape 8 bis : `ui-app/src/board/hunting-season-pieges-kraven.test.ts` (Bear Trap dessinee attachee au heros, paquets de pieges dans les decks supplementaires sans carte ecartee ni face devoilee). 3/3 verts. Les pieges distribues apparaissent comme « Deck supplementaire N » et non aupres du joueur : limite d'affichage assumee (information cachee de toute facon).
- Reste assume : limites hs105/hs106 (ciblage), surcharge de hs159, « les autres personnages ne peuvent pas defendre » de hs121 (un seul joueur sans allie), crochet `RemelangeDefaussePiege` (bloc 6), textes francais.

Carte terminee : OUI (bloc 5), avec les ecarts assumes ci-dessus.

## Bloc 6 : campagne (Lodge hs164-199, récompenses hs200-205, expert hs206-221, Hunter hs222-226)

Statut : TERMINE (09/10/2026), non commité, non déployé.

- Scripts : 63 cartes écrites (aucun `A_FAIRE_CLAUDE` restant). Copies vérifiées identiques (32) : hs170/171=hs169, 173/174=172, 176/177=175, 179/180=178, 182/183=181, 186/187=185, 189/190=188, 192/193=191, 195/196=194, 198/199=197, sets experts 2 à 4 = set 1.
- `campaign.py` réécrit (ports de `campaign_rules.py`) : XP par puce du livret, allié de récompense (moins d'alliés PREDATOR possédés, Master Hunter aux égalités), pénalité « 1 carte de héros » notée puis choisie à la mise en place suivante, drapeaux Kraven, Gibbon, PV experts plafonnés, 2 XP pour une carte de départ de plus, XP contre soins, carte aléatoire de SON set expert (obligatoire à 0 PV), environnement du mode Hunter. `CampaignSetup(1)` ajouté à hs004a.
- Moteur : compteur `rat` (`card_face.py`) ; `DrawUp("Max")` ne remplace plus une carte de RENCONTRE piochée dans le deck du joueur (élargit le fix 04163, livret p.11). Master Trapper : interrupt câblé dans `RemelangeDefaussePiege`.
- Écran : `defaite_continue` (contexte.ts, PanneauRecompenses.tsx) = décision POINTS_OUVERTS n°8 ; Marché générique (`cartes`, `motif_cout`, `verrous`, `ouvert_apres_premier`, `unite`) devenu le Lodge ; `options_campagne` (Mode Hunter, Master Hunter). Textes en ajoutés (dico-en.js, dico-en.ts).
- Gates : `test_campagnes` 137/137 (19 épreuves `hunting_season`, dont témoins) ; `verifier_campagnes` OK ; cas `[hs6]` 41/41 ; `test_cards` 6039/0 ; vitest campagne 136/136 (3 nouveaux, `PanneauRecompenses.defaite-continue.test.tsx`).
- Substitution : toutes les cartes à cas tombent au rouge, empreinte restaurée (673e236d…). Verts sans module = témoins (hs175, hs208, hs222).
- NON FAIT : autoplay non pertinent (aucune carte du bloc dans les decks de démo).
- Assumé : le choix de la carte de héros retirée et de l'allié de récompense est proposé par le moteur, corrigeable au panneau ; hs181 Fresh Tracks via `RegisterTemp` sur AfterUnitThwartEnd.

Carte terminee : OUI (bloc 6), avec les écarts assumés ci-dessus.

## Clôture (09/10/2026)

- `campagne-lodge.spec.ts` lancé sur un moteur d'essai (port 2330, cache séparé, supprimé ensuite) : 3/3, deux fois.
  Corrigé dans le test : le verrou des réglages se lit sur le bouton Master Hunter (le mode Hunter n'existe qu'en
  expert, la 2e épreuve est standard), et la 3e épreuve attend que l'écran soit redessiné avant de cliquer « Le Lodge ».
- Textes français : 239 entrées `hs` dans `ui-app/src/board/textes-fr-fanmade.ts` (153 textes distincts, recopiés sur
  chaque exemplaire). Balises, jetons, traits `[[...]]` et sauts de ligne identiques à l'anglais (vérifié par script).
  Gate `textes-fr-fanmade.test.ts` et `vocabulaire-statuts.test.ts` vertes.
- `verifier_traductions_fr.py` : vert après correction d'une clé orpheline antérieure (« A facedown card would be revealed »,
  texte moteur changé le 04/10 sans sa clé).
- À reprendre hors portage : la mise en place affiche « Hs Feral Instincts » (`titreSet` met en forme l'identifiant du set,
  `public/js/campagne/app.js`) au lieu du nom du set (« Feral Instincts »).


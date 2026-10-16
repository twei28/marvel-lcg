# Leonardo (TMNT, Inkwire) : gabarits PROCESSUS-CARTE

Preuves du 16/10/2026. Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_leonardo.py`
(prefixe `[leonardo]`, 76 cas, tous verts). Substitution :
`tools/substituer_pack.py .game-src 42000 tl` (rouge sans module pour les 17
cartes ; les cas restes verts sont des TEMOINS d'absence ou des bases `desc`
automatiques, assumes ci-dessous). Autoplay : `tools/autoplay.py --deck leonardo`,
8 parties (rhino + klaw, normal, equilibre), 0 traceback. Decisions utilisateur :
`.planning/tmnt/decisions-phase-b.md`.

Icones de ressource verifiees par decoupe contre 01020 (G), 01021 (B), 01023 (R),
01025 (Y) : tl002 G, tl003 Y, tl004 R, tl005 B, tl006 G, tl007 B, tl008 B,
tl009 Y, tl010 B, tl011 R, tl012 Y : TOUTES conformes a `cards.json`.

Etape 8 bis (plateau) : `ui-app/src/board/tmnt-leonardo-plateau.test.ts`, 21 cas verts
(`cd ui-app && npx vitest run src/board/tmnt-leonardo-plateau.test.ts`). Cas lus sur
`dessinee(...)` de `plateau-de-test.ts`. Sensibilite prouvee en CASSANT temporairement puis
restaurant 4 lignes de rendu : (A) `peutPayer` de `interaction.ts` -> 4 cas rouges (katanas non
cliquables) ; (B) `attachees` de `zones.ts` -> 10 rouges (katanas, Cloaked) ; (C) `exhausted` de
`card-model.ts` -> 2 rouges (katanas / serre non couchees) ; (D) zones `retirees` et
`dealt_encounter_cards` de `zones.ts` -> 2 rouges. Aucun vrai trou d'affichage trouve : l'UI
etait deja correcte. Pas de panorama des paires jumelles 14/15 (travail ulterieur). Cartes sans
cas plateau (ne font que redresser/chiffrer) : tl001a, tl003, tl004, tl005, tl008, tl009, tl010.

Moteur partage touche (minimal, additif) : `environment.py`, `environment_helper.py`,
`environment_helper2.py` (parametre `abilities_en_continu`, octroi a toute carte
visee en jeu), `resources.py` (la depense liee a `CanGenerateResources` ignore
`DiscardPay`), `face_effect.py` (`RegisterGiven` enregistre en local la depense de
ressource donnee).

### tl001a : Leonardo (Kenjutsu)
- [x] Étape 2 : `04001a` Hawkeye (Action de heros redressant une amelioration).
- [x] Étape 5 : « you control » (`YouControlCards`), « WEAPON upgrade », « once per round ». Résultat : OK.
- [x] Étape 6 : ATQ 2 / CTR 2 / DEF 2 / PV 12 / HS 5 lus dans desc. Résultat : OK.
- [x] Étape 7 : cas Kenjutsu redresse tl011 (rouge sans module) ; contre-cas arme prete ; arme d'un autre joueur / non WEAPON.
- [x] Étape 7 bis : limite OUI, temoin d'epuisement : deux katanas inclinees, 2e Action refusee, tl012 reste inclinee.
- [x] Étape 8 : autoplay 8 parties, 0 traceback.
- [x] Étape 8 bis : NON (aucun changement de rendu propre).
Carte terminée : OUI

### tl001b : Leo (alter ego)
- [x] Étape 2 : `ls005`/`40059` (recherche deck + defausse, mise en jeu).
- [x] Étape 5 : « up to 2 » (deux recherches `may`), « exhausted », cout de defausse. Résultat : OK.
- [x] Étape 6 : REC 3 / PV 12 / HS 6. Résultat : OK.
- [x] Étape 7 : 2 katanas (deck + defausse) inclinees ; une seule ; aucune ; temoin main vide.
- [x] Étape 7 bis : NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI. Cas `tmnt-leonardo-plateau.test.ts` « tl001b Leo » (2 katanas attachees a l'identite, couchees, absentes de la pile du deck), vus rouges en cassant `attachees` (B) et `exhausted` (C).
Carte terminée : OUI

### tl002 : Splinter
- [x] Étape 2 : `25009`/`51009` (carte specifique en defausse vers le deck).
- [x] Étape 5 : « on TOP », « identity-specific ». Étape 6 : cout 3, PV 3, ATQ/CTR 2*.
- [x] Étape 7 : Response (tl003 monte sur le dessus, rouge sans module) ; temoin : Energy (Basic) refusee comme cible ; ATQ/CTR 2* = 1 degat consecutif (base `desc`, vert sans module, assume).
- [x] Étapes 7 bis, 8 : NON / OK.
- [x] Étape 8 bis : OUI (carte remontee dans le deck). Cas `tmnt-leonardo-plateau.test.ts` « tl002 Splinter » : pile du deck representee par la carte du dessus (dos, 2 cartes), plus de tl003 dans la defausse. Sensibilite : voir l'en-tete.
Carte terminée : OUI

### tl003 : Uke Nagashi
- [x] Étape 2 : `sg016`, `ls006`. Étape 5 : « when LEONARDO defends » (`YourHero`), « for that attack », « paid with physical ».
- [x] Étape 7 : +2 DEF (1 degat -> 0) et Leonardo redresse si physique ; sans physique reste incline ; base : sans Uke 1 degat ; allie defenseur : non jouee.
- [x] 7 bis NON ; 8 OK ; 8 bis NON.
Carte terminée : OUI

### tl004 : Vigilant
- [x] Étape 2 : `ls001a`, `ls004`. Étape 5 : « a scheme », « paid with mental ».
- [x] Étape 7 : -3 menace (physique) sans redressement ; mental : katana redressee ; mental sans katana inclinee : aucune question. Rouge sans module 3/3.
- [x] 7 bis NON ; 8 OK ; 8 bis NON.
Carte terminée : OUI

### tl005 : Stoicism
- [x] Étape 2 : `ls005`, `tl004`. Étape 5 : « ready LEONARDO », « paid with energy ».
- [x] Étape 7 : mental : Leonardo seul ; energie : Leonardo + katana. Rouge 2/2.
- [x] 7 bis NON ; 8 OK ; 8 bis NON.
Carte terminée : OUI

### tl006 : Yo Ko Giri
- [x] Étape 2 : `ls003` (piercing), `62004` (retour en main). Étape 5 : « piercing » inconditionnel, « you MAY return », une de chaque couleur (decision utilisateur).
- [x] Étape 7 : 5 degats percants sur Rhino Tenace ; E+M+P : retour en main ; Decline ; E+M seulement : aucune question. Rouge 4/4.
- [x] 7 bis NON ; 8 OK ; 8 bis OUI : cas « tl006 Yo Ko Giri » (retour en main : l'evenement est dessine dans la zone `main`).
Carte terminée : OUI

### tl007 : Leo's Greenhouse
- [x] Étape 2 : `ls007`. Étape 5 : deux parties de cout (inclinaison + defausse), « draw 2 AND heal 2 ».
- [x] Étape 7 : degats 3 -> 1, main 2 -> 3, incline ; temoins forme heros / main vide / deja incline.
- [x] 7 bis NON ; 8 OK ; 8 bis OUI : cas « tl007 Leo's Greenhouse » (serre couchee via `exhausted`, vu rouge en C ; cartes piochees dans la main).
Carte terminée : OUI

### tl008 : Iaijutsu
- [x] Étape 2 : `42013`, `vr009`, `27018`. Étape 5 : « enemy initiates », cout = une KATANA (pas Iaijutsu, l'insert), « ATTACK event with Hero Action », « paying its cost ».
- [x] Étape 7 : crochet EXACT (decision utilisateur) : `AfterUnitDefeatedUnit` filtre sur `by_effect.this` = l'evenement joue. Sbire vaincu : pioche 1 ; vilain non vaincu : aucune pioche ; temoins katana inclinee, evenement non-ATTACK. Aucune modification du moteur pour ce crochet.
- [x] 7 bis NON ; 8 OK ; 8 bis NON.
Carte terminée : OUI

### tl009 : Taicho
- [x] Étape 2 : `drax/19012`, `ho009`. Étape 5 : « ready THIS card », « consequential », allie vaincu : Reponse non proposee (condition `trigger.IsInPlay()`).
- [x] Étape 7 : Hero Action ; temoins prete / aucune katana prete ; Reponse (Splinter redressee) ; temoin Taicho inclinee ; allie vaincu ; allie Tenace.
- [x] 7 bis NON ; 8 OK ; 8 bis NON.
Carte terminée : OUI

### tl010 : Nukitsuke
- [x] Étape 2 : `ho009`. Étape 5 : « a KATANA you control », `canbe_ready`.
- [x] Étape 7 : redresse tl011 et s'incline ; temoins aucune katana inclinee / deja inclinee.
- [x] 7 bis NON ; 8 OK ; 8 bis NON.
Carte terminée : OUI

### tl011 : Leonardo's Katana (octroi)
- [x] Étape 2 : `michelangelo/tm011`, `rogue/38019`. Étape 5 : « each KATANA you control gains », Hero Resource, identity-specific.
- [x] Étape 7 : vrai octroi (decision) : les DEUX katanas paient Nukitsuke ; une seule katana ; l'octroi disparait quand tl011 quitte ; tl012 seule : 0 ; 1 ressource chacune, effets distincts (risque `Ability.Initialize` leve : meme instance chez deux porteurs fonctionne) ; katana d'un autre joueur : 0 ; alter ego : refuse ; carte d'aspect : refusee.
- [x] Étape 8 bis : OUI. Cas `tmnt-leonardo-plateau.test.ts` « tl011 / tl012 : la ressource octroyee aux katanas dans le paiement » (5 cas, `useInteraction` : les deux katanas sont dessinees ET deviennent des sources de paiement cliquables `role: 'ressource'`, un clic remplit un cran du cout, les deux ensemble paient 2, temoin : katana sans ressource octroyee non proposee). ROUGE en cassant `peutPayer` (A) : 4 cas rouges. Cote moteur, lu : `Card.get_resources` (card.py) liste tous les effets payants de `GetEffects`, qui inclut les `given_effects` de `RegisterGiven`. Pas de partie humaine.
Carte terminée : OUI

### tl012 : Leonardo's Other Katana
- [x] Étape 2 : `ls004`, `32045`. Étape 5 : « each of their basic powers » (ATQ/CTR/DEF ; REC n'existe pas en forme heros, non mesurable), « exhaust 2 KATANA » (2 pretes), « until the end of the round ».
- [x] Étape 7 : +1 sur Leonardo ; +1 ATQ/CTR sur Splinter ; disparait a la fin du round ; temoins une katana prete / tl012 seule. Ressource : voir tl011.
- [x] Étape 8 bis : OUI, memes cas que tl011 (la katana tl012 est l'une des deux sources cliquables).
Carte terminée : NON : l'UI est prouvee, il ne reste que « each of their basic powers » : +1 REC non mesure (aucune face heros n'a de REC), decision d'interpretation a trancher.

### tl013 : Brainwashed Betrayal
- [x] Étape 2 : `ls005`, `ls012`, `11049`, `45080`. Étape 5 : lecture litterale (decisions) : flip obligatoire, un allie defausse au choix, « cannot attack the villain » (sbires attaquables), 3 degats a n'importe quel allie.
- [x] Étape 7 : flip + defausse (1 allie, 2 allies au choix, 0 allie) ; attaque : Shocker prend 2, Rhino 0 (temoin sans obligation : Rhino 2) ; Forced Response sur l'allie d'un AUTRE joueur / sur Splinter vaincue ; Action d'alter ego : retiree du jeu (`area_removed`), 2 degats, Leo incline. Rouge 7/8.
- [x] 7 bis NON ; 8 OK ; 8 bis OUI : cas « tl013 » (identite dessinee en face heros `tl001a`, obligation dessinee, allie defausse sur la pile, carte retiree du jeu dans `annexes`, vu rouge en D).
Carte terminée : OUI

### tl014 : Foot Patrol
- [x] Étape 2 : `40059`, `sm/27129`. Étape 5 : « AND discard pile », FOOT CLAN ET Minion, premier joueur, rien si aucun (decision).
- [x] Étape 7 : menace 2 par joueur (solo 2, duo 4, base `desc`) ; Crisis (principal 6 inchange, temoin 4) ; When Defeated : deck, defausse, aucun, et 2 joueurs (engage avec le premier joueur et non le vainqueur). Rouge 3/8 (reste : bases `desc` et temoins).
- [x] 7 bis NON ; 8 OK ; 8 bis OUI : cas « tl014 Foot Patrol » (sbire mis en jeu dessine dans `terrain-combat`).
Carte terminée : OUI

### tl015 : Karai
- [x] Réserve de perimetre : Cloak/Cloaked = autre agent (`cloaked_cartes.py`). Ici : When Revealed (Karai Cloaked), When Defeated (vilain Cloaked), ★ Boost (carte distribuee au premier joueur, pas a la defausse) : verts, rouges 5/5 sans module.
- [x] Étape 8 bis : OUI. Cas `tmnt-leonardo-plateau.test.ts` « tl015 Karai, tl016 Foot Soldiers : le statut Cloaked » : carte `cloaked` (`StatusCard`) dessinee SOUS Karai, sous le vilain apres sa defaite, boost : Karai donnee face cachee (dos seul). Vus rouges en cassant `attachees` (B) et `dealt_encounter_cards` (D). Cas moteur relances le 16/10/2026 : `test_capacites.py .game-src 43000 /tmp/r.json "[leonardo]"` : 76/76 verts, dont les 3 cas Cloaked de tl015/tl016. Pas de partie humaine (reste commun).
Carte terminée : OUI

### tl016 : Foot Soldiers
- [x] When Revealed (Cloaked sur la carte), Boost 1 (3 degats). Rouge 2/3 (Boost = base `desc`).
- [x] Étape 8 bis : OUI, cas « tl016 » du bloc Cloaked ci-dessus (carte `cloaked` dessinee sur le sbire). Cas moteur 76/76 verts.
Carte terminée : OUI

Reste commun (aucun outil) : une partie jouee par un humain dans le navigateur ;
`verifier_tous_les_decks.py` (125 decks) non relance, remplace par l'autoplay du
deck leonardo (deck complet monte 8 fois sans traceback).

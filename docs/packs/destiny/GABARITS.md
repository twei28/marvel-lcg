# Destiny (Irene Adler, Merlin) : gabarits PROCESSUS-CARTE, 02/11/2026

Pack `destiny` (prefixe `dy`, set 246, auteur Merlin). Scripts : `src/cards/pack/destiny/{destiny,destiny_nemesis}/` (17 cartes). Cas : `tools/cas/destiny.py` (49). Deck : `deck/starter/destiny.json` (`player_deck` VIDE : aucun Extras). Textes FR : `ui-app/src/board/textes-fr-fanmade.ts` (seul fichier de traduction touche). Biographie : `heros-info.js` (`dy001a`). Plateau : `ui-app/src/board/destiny-plateau.test.ts`.

## Source et decisions

- Texte canonique = ANGLAIS (scans beta EN 1.0, 750x1075, mis a 615 de petit cote dans `assets/pics/dy0*.jpg`, dossier non versionne) + precisions du FR Release 1.2 (plus recent) : Glimpse « Discard it at the end of the round » (absent de l'EN), Setup d'Irene = amelioration PSIONIC, **Mystique : « redressez votre identite »** (l'EN disait « ready it »), `Incite` de So, What's the Plan? (desc corrige en `Incite 1`).
- Icones : Y rouge = boost, carte+ = Incite, etoile rouge = ★ Boost. Ressources verifiees contre le pack : poing R, etoile G, noeuds B, eclair Y. `2*` = degats consecutifs (comme Drax `mt002`).
- Glimpse (Permanent + Setup, sans cout) entre en jeu a la mise en place ; un nom d'objet `SideScheme` n'existe pas dans le moteur (`dy015` : `effect.this` nu).
- Hero deck = les 16 numeros « n/16 » ; obligation dy013 ; nemesis dy014 + dy015 + dy016 x3.
- Particularite de test : le heros DEFEND l'attaque (DEF = X) ; Astral Projection n'est jouable que s'il y a de la menace ; `EmptyPlayerDeck` retire des cartes de la partie (voir le commentaire de `tools/cas/destiny.py`).

### dy001a

- [x] Etape 2 : carte(s) de reference : `mw001a` (X dynamique), `sw001a`/`08006` (interruption sur carte de boost), `sn014` (etoile + icones).
- [x] Etape 5 : mots-pieges : `while_attack` non pose (toute activation) ; « then discard ONE of them » : choix du joueur entre la retournee (icones + effet ★ annules) et la nouvelle (defaussee face cachee) ; limite par phase ; X lu a chaque changement de la zone glissee. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : PV 9, main 5, ATQ/CTR/DEF = X (0 en desc). Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (7) : Mister Sinister (2 icones de boost) sous Glimpse : ATQ, CTR et DEF valent 2 ; Destiny's Warning (UNE etoile Boost, 0 icone) sous Glimpse : X vaut 1 (l'etoile compte) ; TEMOIN : rien sous Glimpse, ATQ, CTR et DEF valent 0 ; on defausse la carte RETOURNEE : ses icones sont annulees, la nouvelle (2 icones) joue : Rhino frappe pour 2 + 2 = 4 ; on defausse la NOUVELLE carte (encore face cachee) : la carte retournee joue seule : Rhino frappe pour 2 + 1 = 3 ; TEMOIN : en ALTER-EGO la capacite de la face heros n'existe pas : une seule carte de boost, Rhino frappe pour 2 + 1 = 3 et le deck garde Shocker ; LIMITE une fois par phase : au 2e Rhino de la phase, rien n'est offert (carte de boost 2 icones : 2 + 2 ; total 4 + 4 = 8, et non 7). Substitution : **rouges 5/7** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d'epuisement : voir le cas LIMITE ci-dessus, chiffre mesure au second emploi.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : « Then discard one of them » = choix du joueur entre la carte retournee et la nouvelle face cachee (confirme par l'utilisateur le 02/11/2026) ; partie humaine non jouee, 24 parties autoplay menees au bout.

### dy001b

- [x] Etape 2 : carte(s) de reference : `01040b` (Setup + recherche), `27030b` (reponse au retour de forme).
- [x] Etape 5 : mots-pieges : « PSIONIC upgrade » : une amelioration ; « change TO this form » : retour en alter-ego. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : REC 3, main 6, PV 9. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (3) : une amelioration PSIONIC du deck est ajoutee a la main de depart ; apres le retour en alter-ego, une carte PSIONIC de la defausse est melangee dans le deck ; TEMOIN : une carte NON PSIONIC de la defausse (Energy) n'est pas offerte, elle y reste. Substitution : **rouges 2/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy002

- [x] Etape 2 : carte(s) de reference : `40004` (LookAtDeck), `sn014`/`su012` (glisser sous une carte), `bw016` (fin de round).
- [x] Etape 5 : mots-pieges : 3 cartes regardees, une glissee (zone de boost seule lisible), les deux autres melangees dans le deck Rencontre, defaussee en fin de round (FR 1.2) ; Permanent+Setup natifs. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : aucun cout imprime. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (5) : Glimpse of the Future est en jeu des la mise en place (Permanent + Setup) ; Precognition : une des 3 cartes du dessus est glissee sous la carte, les deux autres restent dans le deck Rencontre, Glimpse est inclinee ; « top 3 » : la 4e carte du deck n'est pas regardee, elle reste dans le deck (la carte glissee est l'une des 3 premieres) ; la carte glissee est defaussee (defausse RENCONTRE) a la fin du round ; TEMOIN : tant que le round n'est pas fini, la carte reste glissee. Substitution : **rouges 4/5** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? OUI : cas plateau `destiny-plateau.test.ts` (carte glissee sous Glimpse dessinee, derriere elle, face cachee) ; pas vu ROUGE (le correctif `enUnites` existe deja).

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy003

- [x] Etape 2 : carte(s) de reference : `48001a` (Cost("1") + limite par phase), `17007` (cout d'inclinaison).
- [x] Etape 5 : mots-pieges : « ready YOUR IDENTITY » (FR 1.2) ; limite une fois par phase. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 3, PV 3, THW 2*, ATQ 2*, 1 soin. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (2) : Action : une ressource depensee, l'identite gagne 1 PV et est REDRESSEE, Mystique inclinee ; LIMITE une fois par phase : Mystique redressee, la 2e Action est refusee (1 seul soin : 3 - 1 = 2 degats, et non 1). Substitution : **rouges 2/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d'epuisement : voir le cas LIMITE ci-dessus, chiffre mesure au second emploi.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy004

- [x] Etape 2 : carte(s) de reference : `08007` / `46004` (`CanGenerateResources(.., for_card=CardFinder2)`).
- [x] Etape 5 : mots-pieges : « Resource » (pas Hero Resource) ; ne paie qu'une carte PSIONIC. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 1, 1 [wild]. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (2) : genere [wild] pour une carte PSIONIC : elle paie Unmask (cout 1, PSIONIC), Mental Awareness s'incline ; TEMOIN : elle NE paie PAS une carte non PSIONIC (Unconditional Love reste en main, Mental Awareness reste prete). Substitution : **rouges 1/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy005

- [x] Etape 2 : carte(s) de reference : `26022` (depense variable), `01060` (retrait de menace).
- [x] Etape 5 : mots-pieges : 3 ressources [mental] au plus ; une manigance DIFFERENTE par ressource ; X par manigance. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 1, 3 ressources, X. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (3) : 2 ressources mentales, X = 2 : DEUX manigances DIFFERENTES perdent 2 menaces chacune ; Clairvoyance inclinee ; UNE seule ressource depensee : UNE seule manigance est visee (l'autre garde sa menace) ; TEMOIN : rien sous Glimpse (X = 0), aucune menace retiree. Substitution : **rouges 3/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy006

- [x] Etape 2 : carte(s) de reference : `26022`, `01054` (degats directs).
- [x] Etape 5 : mots-pieges : idem sur les ennemis ; degats directs (pas une attaque). Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 1, 3 ressources, X. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (3) : 2 ressources mentales, X = 2 : DEUX ennemis DIFFERENTS (Rhino, Hydra Mercenary) recoivent 2 degats chacun ; Unmask inclinee ; UNE seule ressource depensee : UN seul ennemi est vise ; TEMOIN : rien sous Glimpse (X = 0), aucun degat. Substitution : **rouges 3/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy007

- [x] Etape 2 : carte(s) de reference : `mw004` (`WhenUnitWouldTakeDamage(HeroInterrupt)` + `PreventDamage`).
- [x] Etape 5 : mots-pieges : « prevent X OF that damage » ; offerte seulement si X >= 1 ; le heros defend d'abord (DEF = X). Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 0, 1 ressource [mental], X. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (3) : X = 2 : Sandman (ATQ 3) frappe, la DEF 2 laisse 1 degat, Be Careful (X = 2) le previent : 0 degat et Be Careful s'incline ; X = 1 (une etoile) : DEF 1 laisse 2 degats, Be Careful en previent 1 : l'identite subit 1 ; TEMOIN : rien sous Glimpse (X = 0), la capacite n'est pas offerte : 3 degats, Be Careful reste prete. Substitution : **rouges 2/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy008

- [x] Etape 2 : carte(s) de reference : `21036` Cosmic Ward (clone).
- [x] Etape 5 : mots-pieges : Interruption forcee : annule Une fois revelee, defausse la traitrise puis Prescience. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 1. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (2) : a la revelation d'une traitrise, ses effets Une fois revelee sont annules (Rhino ne recoit pas de carte Tenace), elle est defaussee, puis Prescience aussi ; TEMOIN : sans Prescience la traitrise s'applique (Rhino devient Tenace). Substitution : **rouges 1/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy009

- [x] Etape 2 : carte(s) de reference : `01060` For Justice!.
- [x] Etape 5 : mots-pieges : 3 + X menaces retirees d'une manigance. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 2, 3 + X. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (2) : X = 2 : 3 + 2 = 5 menaces retirees du complot principal (6 -> 1) ; TEMOIN : rien sous Glimpse : 3 menaces seulement (6 -> 3). Substitution : **rouges 2/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy010

- [x] Etape 2 : carte(s) de reference : `01054` Uppercut.
- [x] Etape 5 : mots-pieges : 4 + X degats a un ennemi (pas une attaque). Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 2, 4 + X. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (2) : X = 2 : 4 + 2 = 6 degats a Rhino ; TEMOIN : rien sous Glimpse : 4 degats seulement. Substitution : **rouges 2/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy011

- [x] Etape 2 : carte(s) de reference : `01040b` (recherche), `Faces.ReadyAll`.
- [x] Etape 5 : mots-pieges : Mystique/Raven = toute carte en jeu nommee Mystique ou Raven Darkholme (allie dy003 ou identite du heros Mystique) ; deck ET defausse ; QUESTION OUVERTE. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : cout 1. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (3) : Mystique en jeu : Mystique ET l'identite de Destiny sont redressees ; Mystique absente, dans le DECK : elle est ajoutee a la main ; Mystique absente, dans la DEFAUSSE : elle est ajoutee a la main. Substitution : **rouges 3/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : « Mystique/Raven Darkholme » = toute carte en jeu portant l'un de ces deux noms, alliee dy003 ou futur heros Mystique (confirme par l'utilisateur le 02/11/2026).

### dy012

- [x] Etape 2 : carte(s) de reference : `mt006` / `tm007` (`AfterYouSpendThisCard`), `27030b`.
- [x] Etape 5 : mots-pieges : 1 carte propre a l'identite de SA defausse, melangee dans le deck ; le choix se fait dans l'operation (un `SetTarget(card_class=..)` sur cette Reponse rend la carte impayable). Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : 2 ressources [mental], 1 carte. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (2) : apres depense, une carte propre a l'identite (Mental Awareness) de la defausse est melangee dans le deck ; TEMOIN : une carte de BASE (Energy) de la defausse n'est pas offerte, elle y reste (deck vide). Substitution : **rouges 1/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy013

- [x] Etape 2 : carte(s) de reference : `mt011` Psychic Tremor, `01165` / `03026`.
- [x] Etape 5 : mots-pieges : « Discard this obligation » appartient a la seconde branche ; sans amelioration SKILL la branche reste offerte et la carte gagne surge. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : boost 2. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (3) : branche 1 : en alter-ego, Irene Adler s'incline et l'obligation est retiree de la partie ; branche 2 : une amelioration SKILL (Unmask) est defaussee, puis l'obligation est defaussee ; branche 2 SANS amelioration SKILL : rien n'est defausse et la carte gagne SURGE (la carte rencontre suivante, Hydra Mercenary, est distribuee). Substitution : **rouges 3/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy014

- [x] Etape 2 : carte(s) de reference : `49007` / `60113b` (`EnemyCannotActivate` conditionnel), `sn014` (`DoActivate`).
- [x] Etape 5 : mots-pieges : tant que Warning est en jeu il ne s'active pas ; Une fois revele : si un AUTRE Sinister est en jeu, defausse celle-ci puis il active contre vous en ignorant l'interdiction (drapeau `dy_forcer`). Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : PV 5, ATQ 3, SCH 3, boost 2, Incite 2. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (2) : tant que Destiny's Warning est en jeu, il ne s'active PAS (0 degat) ; TEMOIN : sans Destiny's Warning il s'active (ATQ 3 : 3 degats). Substitution : **rouges 1/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy015

- [x] Etape 2 : carte(s) de reference : `02027` Goblin Nation (★ Boost : mise en jeu).
- [x] Etape 5 : mots-pieges : 1[per_hero] menace du complot principal ; ★ Boost = mise en jeu sans Une fois revelee ; Incite 2 natif ; en forme heros, dy001a peut annuler l'effet ★ (voir cas). Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : menace 3*, boost 0, Incite 2. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (2) : a la revelation : Incite 2 pose 2 menaces PUIS Une fois revelee en retire 1 par joueur (1 + 2 - 1 = 2) ; ★ Boost : retournee comme carte de boost d'une manigance de Rhino, elle entre en jeu. Substitution : **rouges 2/2** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

### dy016

- [x] Etape 2 : carte(s) de reference : `rl015` (`ThisCardGainSurge`), `dy015`/`dy014`.
- [x] Etape 5 : mots-pieges : trois branches exclusives : retirer de Warning / Sinister active contre vous / surge. Resultat : texte et code alignes ligne a ligne.
- [x] Etape 6 : nombres : boost 2, Incite 1, 1 menace par joueur. Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas (3) : Destiny's Warning en jeu : 1 menace par joueur retiree de la manigance annexe (4 -> 3) ; pas de Warning, Mister Sinister en jeu : il s'active contre vous (ATQ 3 : 3 degats) ; ni Warning ni Sinister : la carte gagne SURGE (la carte suivante, Hydra Mercenary, est distribuee). Substitution : **rouges 3/3** (les verts restants sont des TEMOINS d'absence d'effet ou des bases natives).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : 8 parties (rhino, normal, equilibre), temoin Spider-Man : 8 parties ; grep tracebacks : 0 sur les 16 journaux.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on voit ? NON.

Carte terminee : OUI : sous reserve de la gate de heros (partie humaine complete non jouee).

## Verifications du pack

- `test_capacites` `dy0` : 49/49 ; `substituer_pack` : 17/17 cartes (empreinte du dossier identique apres).
- `verifier_appels_modules destiny` OK ; `verifier_api_cartes` 9148 fichiers, 0 en faute ; `test_cards` 8120 OK / 0 erreur ; `audit_cartes` 0 module en erreur (seul signalement : dy008 « When Revealed » cite dans le texte, faux positif identique a Cosmic Ward) ; `verifier_prefixes` OK ; `verifier_tous_les_decks` (deck destiny) : identite dy001a, main 7, deck 8.
- Autoplay : 8 parties, 0 victoire (deck sans aspect), 5,0 rounds ; temoin Spider-Man 0 victoire, 6,9 rounds ; 0 exception. Le pilote joue Path of Violence, Mental Awareness, Mystique, Be Careful, Unmask, Clairvoyance, Prescience, Astral Projection ; Seizure, Sinister, Warning, So What's the Plan? sont apparus.

## Manques

1. Aucune partie humaine complete ; voile FR et traductions gerees ailleurs (seul `textes-fr-fanmade` ecrit).
2. Questions de lecture en attente : dy001a (« discard one of them »), dy011 (Mystique/Raven).
3. Images non versionnees (`assets/pics/` ignore par git).

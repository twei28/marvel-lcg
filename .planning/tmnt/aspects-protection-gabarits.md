# Aspect TMNT Protection (up001-up043) : gabarits PROCESSUS-CARTE

16/10/2026, branche `aspects-up`. Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_aspect_protection.py`
(filtre `[up] `). Questions : `.planning/tmnt/aspects-protection-questions.md`. Transcriptions des scans :
relues sur chaque PNG (`zip-aspect/TMNT Aspect/Protection/`).

**Substitution, tout l'aspect d'un coup** (`scratchpad/up/substitution.sh`) : les 24 `ability_link` retires
ET les 18 modules `up*.py` mis de cote, filtre `[up] ` relance, puis tout restaure et relance. Les chiffres
« rouge sans / vert avec » de chaque carte viennent de ces deux passes.

**Autoplay** (etape 8) : voir la section en fin de fichier (decks `deck-up-A` nouvelles/modifiees et
`deck-up-B` reskins, Black Panther contre Rhino, temoin Black Panther de depart).

### up001 : Ace Duck (bandeau Brother Voodoo) (IDENTIQUE 09012)

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"09012"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « search the top 5 » (5), « an EVENT card », « Shuffle your deck » ; traits du scan AERIAL DUCK DIMENSION X (pas AVENGER MYSTIC) ; bandeau ✦ Brother Voodoo -> `unique_also` (Q-R1)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 3, PV 3, ATK 1* (1 etoile), THW 2** (2 etoiles), RES B (icone noeuds = 09012 RES B), 5 cartes
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up001 ...` : 4/4 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up001 Ace Duck : Reponse a l'entree en jeu, l'evenement des 5 du dessus va en main
      - OK / sans : OK : up001 TEMOIN 09012 (officielle) : Ace Duck : Reponse a l'entree en jeu, l'evenement des 5 du dessus va en main
      - OK / sans : OK : up001 unicite : Brother Voodoo (09012) en jeu -> up001 n'est PAS jouable (bandeau « Brother Voodoo »)
      - OK / sans : OK : up001 unicite : TEMOIN, sans Brother Voodoo en jeu, up001 est jouable
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 3 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up002 : Armored Vest (IDENTIQUE 01081)

> **Converti en art alternatif de 01081 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up002` n'existe plus dans `cards.json` (image `01081_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `01081` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"01081"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « any player's control », « Max 1 per player » (`MaxPerUnit` recopie dans desc), « your HERO »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES B, +1 DEF, MaxPerUnit 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up002 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up002 Armored Vest : +1 DEF au heros
      - OK / sans : OK : up002 TEMOIN 01081 (officielle) : Armored Vest : +1 DEF au heros
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 5 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up003 : Army of One (IDENTIQUE 60048)

> **Converti en art alternatif de 60048 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up003` n'existe plus dans `cards.json` (image `60048_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `60048` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"60048"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « for EACH ally you control » (cout +1 par allie), « Ready your HERO »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1* (desc `1*`), +1 par allie, RES Y
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up003 ...` : 4/4 verts avec module/lien ; substitution : 1/2 cas sujets ROUGES sans. 
      - OK / sans : KO : up003 Army of One : redresse le heros
      - OK / sans : OK : up003 TEMOIN 60048 (officielle) : Army of One : redresse le heros
      - OK / sans : OK : up003 Army of One : 2 allies controles -> cout 3, injouable avec 2 ressources  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
      - OK / sans : OK : up003 TEMOIN 60048 (officielle) : Army of One : 2 allies controles -> cout 3, injouable avec 2 ressources
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties, 0 traceback ; carte JAMAIS jouee par le pilote (couverte par ses cas seulement) (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up004 : Autodefenestration (MODIFIEE de 01003 Backflip)

- [x] Etape 2 : carte(s) de reference : `01003` Backflip (prevention totale d'une attaque) ; `ua015` Demolish (`CostFunc.Rampage`) ; `21061` (HeroInterrupt + cout) ; fiche rampage.md lue AVANT
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Hero Interrupt » (pas Interrupt : cas alter-ego), « you would take ... damage FROM AN ATTACK » (cas hors attaque), « prevent ALL », Rampage = cout (identite Tenace = impaye)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 0* (desc `0*`), Rampage 2 (`CostFunc.Rampage(2)`), RES R
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up004 ...` : 4/4 verts avec module/lien ; substitution : 1/4 cas sujets ROUGES sans. 
      - OK / sans : KO : up004 Autodefenestration : Rampage 2 paye (2 degats, 2 cartes) puis l'attaque de Rhino entierement prevenue
      - OK / sans : OK : up004 Autodefenestration : identite Tenace -> cout Rampage NON paye, la carte reste en main  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
      - OK / sans : OK : up004 Autodefenestration : degats HORS attaque (Puzzle.Damage 3) -> non jouable, 3 degats  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
      - OK / sans : OK : up004 Autodefenestration : forme ALTER-EGO -> Hero Interrupt indisponible (2 degats de Rhino)  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 5 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI.

### up005 : Change of Fortune (IDENTIQUE 48014)

> **Converti en art alternatif de 48014 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up005` n'existe plus dans `cards.json` (image `48014_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `48014` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"48014"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « during the VILLAIN phase » (contre-cas phase joueur), « exhaust this card -> draw 2 »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES B, 2 cartes, MaxPerUnit 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up005 ...` : 4/4 verts avec module/lien ; substitution : 1/2 cas sujets ROUGES sans. 
      - OK / sans : KO : up005 Change of Fortune : sbire vaincu par le heros en phase du vilain -> incline, pioche 2
      - OK / sans : OK : up005 TEMOIN 48014 (officielle) : Change of Fortune : sbire vaincu par le heros en phase du vilain -> incline, pioche 2
      - OK / sans : OK : up005 Change of Fortune : meme defaite en phase des JOUEURS -> rien  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
      - OK / sans : OK : up005 TEMOIN 48014 (officielle) : Change of Fortune : meme defaite en phase des JOUEURS -> rien
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 1 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up006 : "Come Get Me, Bub!" (IDENTIQUE 48016)

> **Converti en art alternatif de 48016 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up006` n'existe plus dans `cards.json` (image `48016_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `48016` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"48016"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « until you discard a MINION », « engaged with YOU », « heal 3 AND tough »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 0, RES B, soin 3
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up006 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up006 "Come Get Me, Bub!" : sbire defausse du deck rencontre mis en jeu engage, soin 3 + Tenace
      - OK / sans : OK : up006 TEMOIN 48016 (officielle) : "Come Get Me, Bub!" : sbire defausse du deck rencontre mis en jeu engage, soin 3 + Tenace
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 1 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up007 : Cyber Ninja (Donnie) (NOUVELLE)

- [x] Etape 2 : carte(s) de reference : `09012` (Reponse a l'entree) ; `ar010`/`53001b` (cout « discard from your hand ») ; `td005` (cloak = statut Cloaked) ; fiches cloak.md/cloaked.md lues AVANT
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « discard AN UPGRADE from YOUR HAND » (cout, contre-cas sans amelioration), « draw 1 AND cloak CYBER NINJA » (la carte elle-meme)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 2, PV 2, ATK 1*, THW 1*, RES B, 1 carte piochee
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up007 ...` : 2/2 verts avec module/lien ; substitution : 1/2 cas sujets ROUGES sans. 
      - OK / sans : KO : up007 Cyber Ninja : Reponse, une amelioration defaussee de la main -> pioche 1 et Camoufle
      - OK / sans : OK : up007 Cyber Ninja : sans amelioration en main, cout impayable -> ni pioche ni Camoufle  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 3 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? OUI : pose une carte d'etat Camoufle (deja dessinee par le pack TMNT, `etats.ts` lettre K ; aucun nouveau rendu). Cas plateau : `ui-app/src/board/tmnt-protection-plateau.test.ts` (7/7 verts d'emblee : aucun correctif necessaire, le rendu generique existait deja ; temoin d'absence id 999).

Carte terminee : OUI.

### up008 : Defensive Conditioning (IDENTIQUE 56046)

> **Converti en art alternatif de 56046 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up008` n'existe plus dans `cards.json` (image `56046_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `56046` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"56046"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « YOU get +3 hit points AND your HERO gets +1 DEF »
      Resultat : conforme (le cas mesure +1 DEF ; +3 PV porte par le meme module officiel).
- [x] Etape 6 : nombres texte <-> code : cout 2, RES R, +3 PV, +1 DEF, MaxPerUnit 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up008 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up008 Defensive Conditioning : +1 DEF au heros
      - OK / sans : OK : up008 TEMOIN 56046 (officielle) : Defensive Conditioning : +1 DEF au heros
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties, 0 traceback ; carte JAMAIS jouee par le pilote (couverte par ses cas seulement) (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up009 : Demoralize (NOUVELLE)

- [x] Etape 2 : carte(s) de reference : `10015` Toe to Toe (« Choose an enemy. It attacks you ») ; `56048` Taunt (TACTIC, sans libelle d'attaque) ; Confused = `Faces.GiveStatus`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « an enemy » (vilain OU sbire : deux cas), « It attacks YOU », « Confuse THAT enemy » (le meme), pas de libelle (attack)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 0, RES B
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up009 ...` : 2/2 verts avec module/lien ; substitution : 2/2 cas sujets ROUGES sans. 
      - OK / sans : KO : up009 Demoralize : Rhino attaque le heros (incline : 2 degats) puis est Desoriente
      - OK / sans : KO : up009 Demoralize : un SBIRE choisi (Hydra Mercenary) attaque puis est Desoriente ; Rhino intact
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties, 0 traceback ; carte JAMAIS jouee par le pilote (couverte par ses cas seulement) (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI.

### up010 : Electrostatic Armor (IDENTIQUE 10031)

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"10031"' src/game src/engine` : rien (ou commentaire seul) (seul un commentaire cite 10031 dans condition.py)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « After you DEFEND », « the attacking character » ; le scan dit bien « Play under » (cards.json de 10031 a la coquille « Player »)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES Y, 1 degat, MaxPerUnit 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up010 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up010 Electrostatic Armor : apres une defense, 1 degat a l'attaquant
      - OK / sans : OK : up010 TEMOIN 10031 (officielle) : Electrostatic Armor : apres une defense, 1 degat a l'attaquant
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 5 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up011 : Energy Barrier (IDENTIQUE 05017)

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"05017"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ANY amount of damage » (pas seulement d'attaque), « remove 1 counter -> prevent 1 AND deal 1 to AN enemy », Uses recopie dans desc
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 2, RES Y, Uses 3 reflection, 1/1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up011 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up011 Energy Barrier : previent 1, 1 degat a un ennemi, 1 compteur retire
      - OK / sans : OK : up011 TEMOIN 05017 (officielle) : Energy Barrier : previent 1, 1 degat a un ennemi, 1 compteur retire
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 2 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up012 : Get Their Attention (IDENTIQUE 60049)

> **Converti en art alternatif de 60049 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up012` n'existe plus dans `cards.json` (image `60049_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `60049` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"60049"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « When an enemy INITIATES an attack », « remove 3 threat from A scheme »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 2, RES B, 3 menaces
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up012 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up012 Get Their Attention : quand un ennemi attaque, 3 menaces retirees
      - OK / sans : OK : up012 TEMOIN 60049 (officielle) : Get Their Attention : quand un ennemi attaque, 3 menaces retirees
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 2 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up013 : Groo the Wanderer (MODIFIEE de 20016 Star-Lord)

- [x] Etape 2 : carte(s) de reference : `20016` Star-Lord (Reponse forcee copiee) ; `10012` Sentry (meme effet) ; riposte de `16120` Badoon Sentry pour mesurer l'ABSENCE de ranged
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « deal YOURSELF 1 FACEDOWN encounter card » (distribuee, pas revelee), « under your control », AUCUNE ligne ranged (difference avec 20016, cas dedie + temoin 20016)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 2, PV 4, ATK 3* (1), THW 2** (2), RES R (poing), 1 carte
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up013 ...` : 3/3 verts avec module/lien ; substitution : 1/2 cas sujets ROUGES sans. 
      - OK / sans : KO : up013 Groo the Wanderer : en jeu -> 1 carte rencontre face cachee distribuee au joueur
      - OK / sans : OK : up013 Groo the Wanderer : AUCUN ranged -> la Riposte 1 de Badoon Sentry le touche (1 consecutif + 1 = 2)  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
      - OK / sans : OK : up013 TEMOIN 20016 Star-Lord : attaque ranged -> pas de riposte (1 consecutif seulement)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 4 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI.

### up014 : Grotto (bandeau Iron Fist) (IDENTIQUE au compteur pres (09014) : script propre)

- [x] Etape 2 : carte(s) de reference : `09014` Iron Fist, copie ligne a ligne ; le module officiel ecrit `'mystic'` en dur -> pas d'ability_link
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « 2 BRUTE counters », « When Grotto ATTACKS an enemy », « stun THAT enemy AND deal 1 » ; bandeau ✦ Iron Fist -> unique_also
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 4, PV 3, ATK 2*, THW 1*, RES R, 2 compteurs, 1 degat
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up014 ...` : 4/4 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up014 Grotto : entre en jeu avec 2 compteurs brute ; son attaque sonne Rhino et lui inflige 1 + 2
      - OK / sans : OK : up014 TEMOIN 09014 Iron Fist : meme montage, compteurs mystic
      - OK / sans : OK : up014 unicite : Iron Fist (09014) en jeu -> up014 n'est PAS jouable (bandeau « Iron Fist »)
      - OK / sans : OK : up014 unicite : TEMOIN, sans Iron Fist en jeu, up014 est jouable
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 2 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (compteur `brute` ajoute a CardFace.COUNTER + compteurs-fr).

### up015 : Helpful Bystander (NOUVELLE)

- [x] Etape 2 : carte(s) de reference : `40079` Morlock (« it attacks X instead » = ReplaceTarget) ; `an002` Sera (+1 taille de main depuis un allie) ; overkill.md (`GainOverKill`) ; vulnerable.md (desc)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Your HERO gets +1 hand size », « When an enemy attacks YOU » (Forced), « INSTEAD » (cible remplacee), « THIS attack gains overkill » (exces a l'identite), Vulnerable / Max 1 per deck dans desc, THW/ATK « – » = cles absentes (modele 01050)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, PV 1, RES R, +1 HS, MaxPerDeck 1, Vulnerable 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up015 ...` : 2/2 verts avec module/lien ; substitution : 2/2 cas sujets ROUGES sans. 
      - OK / sans : KO : up015 Helpful Bystander : Rhino attaque le joueur -> attaque le Bystander a la place, deferlement 1 sur l'identite
      - OK / sans : KO : up015 Helpful Bystander : votre heros gagne +1 taille de main
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 1 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI.

### up016 : Herman (NOUVELLE)

- [x] Etape 2 : carte(s) de reference : `12011` Ant-Man (surpaiement a l'entree, `message.overpaid`, plafond) ; `62001a`/`32001a` (`ThisCanHaveAdditionalTough`) ; toughness.md lue
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « up to 3 tough » (1 + 2 supplementaires), « ADDITIONAL ... (to a max of 2) for EACH resource you overpaid », Interrupt « When Herman enters play »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 2, PV 1, ATK 2** , THW 1**, RES R, max 3 Tenace, +2 max
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up016 ...` : 3/3 verts avec module/lien ; substitution : 2/3 cas sujets ROUGES sans. 
      - OK / sans : KO : up016 Herman : surpaye de 2 (4 ressources pour un cout de 2) -> 3 cartes Tenace
      - OK / sans : OK : up016 Herman : paye juste (cout 2) -> 1 seule Tenace (Toughness)  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
      - OK / sans : KO : up016 Herman : surpaye de 4 (6 ressources) -> plafond, 3 Tenace et pas 5
- [x] Etape 7 bis : limite imprimee ? OUI (« to a max of 2 ») : temoin, surpaiement de 4 -> 3 Tenace et pas 5 (cas « surpaye de 4 »).
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 3 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? OUI : plusieurs cartes Tenace sur un allie (rendu existant, Luke Cage/Colossus portent deja plusieurs Tenace). Cas plateau : `ui-app/src/board/tmnt-protection-plateau.test.ts` (7/7 verts d'emblee : aucun correctif necessaire, le rendu generique existait deja ; temoin d'absence id 999).

Carte terminee : OUI.

### up017 : Honor Blade (Leo, bandeau Patriot) (IDENTIQUE 56041)

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"56041"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « After YOU engage a minion », « give HONOR BLADE » (la carte) ; traits TURTLE WARRIOR ; bandeau ✦ Patriot -> unique_also
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 3, PV 3, ATK 2*, THW 1*, RES Y
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up017 ...` : 4/4 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up017 Honor Blade : apres que vous engagez un sbire, Tenace
      - OK / sans : OK : up017 TEMOIN 56041 (officielle) : Honor Blade : apres que vous engagez un sbire, Tenace
      - OK / sans : OK : up017 unicite : Patriot (56041) en jeu -> up017 n'est PAS jouable (bandeau « Patriot »)
      - OK / sans : OK : up017 unicite : TEMOIN, sans Patriot en jeu, up017 est jouable
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 2 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up018 : "I Can Do This All Day" (IDENTIQUE 56047 (coquille « Hero Action »))

> **Converti en art alternatif de 56047 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up018` n'existe plus dans `cards.json` (image `56047_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `56047` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"56047"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Hero ACTION (defense): When... » imprime : coquille probable (Q-UP2) ; « declare your HERO », « WITHOUT exhausting »
      Resultat : conforme a 56047 ; Q-UP2 ouverte.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES B
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up018 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up018 "I Can Do This All Day" : heros incline declare defenseur sans s'incliner (0 degat)
      - OK / sans : OK : up018 TEMOIN 56047 (officielle) : "I Can Do This All Day" : heros incline declare defenseur sans s'incliner (0 degat)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 6 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

**Mise à jour du 17/10/2026 (Réponse du 17/10/2026)** : **Hero Interrupt confirmé** (coquille « Hero Action » du scan) ; texte affiché corrigé
en « Hero Interrupt » (cards.json) / « Interruption de héros » (FR) ; code inchangé (lien 56047).
Carte terminee : OUI.

### up019 : In Harm's Way (IDENTIQUE 60050)

> **Converti en art alternatif de 60050 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up019` n'existe plus dans `cards.json` (image `60050_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `60050` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"60050"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « X = your DEF » (DEF du heros), « an enemy AND a scheme », cout +1 par allie
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 3*, RES R, X = DEF (3)
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up019 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up019 In Harm's Way : X = DEF 3 degats a Rhino et 3 menaces retirees
      - OK / sans : OK : up019 TEMOIN 60050 (officielle) : In Harm's Way : X = DEF 3 degats a Rhino et 3 menaces retirees
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 1 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up020 : Innate Reflexes (IDENTIQUE 60038)

> **Converti en art alternatif de 60038 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up020` n'existe plus dans `cards.json` (image `60038_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `60038` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"60038"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Starting » (capacite du module 60038, `WhenGameBeginSetup`), « your HERO gets +1 DEF » ; pas d'icone de ressource (desc sans RES, comme 60038)
      Resultat : conforme (le cas mesure +1 DEF ; Starting vient du meme module officiel, non mesure ici).
- [x] Etape 6 : nombres texte <-> code : cout 1, +1 DEF
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up020 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up020 Innate Reflexes : +1 DEF au heros
      - OK / sans : OK : up020 TEMOIN 60038 (officielle) : Innate Reflexes : +1 DEF au heros
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 8 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up021 : Jotaro (MODIFIEE de 26014 Protector)

- [x] Etape 2 : carte(s) de reference : `26014` Protector (ReduceDamage + Cost + LimitOncePerRound) ; `32011` Nightcrawler (`who_deal_damage=Enemy`) ; toughness.md
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « When AN ENEMY would deal any amount of damage » (source ennemie, cible quelconque), « spend a [physical] » (contre-cas sans R), « reduce BY 1 », « Limit once per round »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 3 (scan ; la table TSV disait 2), PV 2, ATK 2*, THW 1*, RES R, Toughness 1, -1, cout R
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up021 ...` : 5/5 verts avec module/lien ; substitution : 1/3 cas sujets ROUGES sans. 
      - OK / sans : KO : up021 Jotaro : Rhino frapperait le heros de 2 -> [physical] depense, 1 seul degat
      - OK / sans : OK : up021 Jotaro : sans ressource [physical] (Genius BB), pas de reduction : 2 degats  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
      - OK / sans : KO : up021 Jotaro : TEMOIN D'EPUISEMENT, deux attaques dans le round -> une seule reduction (6 - 1 = 5)
      - OK / sans : OK : up021 Jotaro : ligne de base SANS Jotaro, deux attaques de Rhino -> 6 degats
      - OK / sans : OK : up021 Jotaro : Tenacite (Toughness) -> entre en jeu avec une carte Tenace  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
- [x] Etape 7 bis : limite imprimee ? OUI : temoin d'epuisement « deux attaques dans le round -> une seule reduction (6 - 1 = 5) » avec sa ligne de base mesuree (6).
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 4 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI.

### up022 : Lindsey Baker (bandeau The Night Nurse) (IDENTIQUE au compteur pres (09019) : script propre)

- [x] Etape 2 : carte(s) de reference : `09019` The Night Nurse, copie ligne a ligne ; module officiel `'medical'` en dur -> pas d'ability_link
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Exhaust AND remove 1 healing counter » (deux couts), « a HERO », « heal 1 AND discard 1 status card from IT » ; bandeau ✦ The Night Nurse -> unique_also
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES B, Uses 3 healing, 1/1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up022 ...` : 4/4 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up022 Lindsey Baker : Action -> soigne 1 et defausse le Sonne du heros, 1 compteur healing retire
      - OK / sans : OK : up022 TEMOIN 09019 The Night Nurse : meme montage (compteurs medical)
      - OK / sans : OK : up022 unicite : The Night Nurse (09019) en jeu -> up022 n'est PAS jouable (bandeau « The Night Nurse »)
      - OK / sans : OK : up022 unicite : TEMOIN, sans The Night Nurse en jeu, up022 est jouable
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 2 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (compteur `healing` ajoute a CardFace.COUNTER : `desc.Uses` l'exigeait).

### up023 : Lookout (NOUVELLE)

- [x] Etape 2 : carte(s) de reference : `nt005` Kickflip (`ReduceCostToPlayThis(1, conditions=...)`) ; `ua015` (« you control a NYC support ») ; `13017` Lie in Wait (Hero Response apres engagement, defausse en cout) ; cloak.md
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « if you control a NYC SUPPORT » (contre-cas sans soutien), « After a minion engages YOU », « discard Lookout -> » (cout), « cloak your HERO AND draw 1 »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 2 (-1), RES B, 1 carte
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up023 ...` : 3/3 verts avec module/lien ; substitution : 2/3 cas sujets ROUGES sans. 
      - OK / sans : KO : up023 Lookout : un sbire vous engage -> Lookout defausse, heros Camoufle, 1 carte piochee
      - OK / sans : KO : up023 Lookout : soutien NYC controle (Shell Cycle tr008) -> cout 1, jouable avec une seule ressource
      - OK / sans : OK : up023 Lookout : SANS soutien NYC -> cout 2, injouable avec une seule ressource  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties, 0 traceback ; carte JAMAIS jouee par le pilote (couverte par ses cas seulement) (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? OUI : Camoufle sur le heros (rendu existant). Cas plateau : `ui-app/src/board/tmnt-protection-plateau.test.ts` (7/7 verts d'emblee : aucun correctif necessaire, le rendu generique existait deja ; temoin d'absence id 999).

Carte terminee : OUI.

### up024 : Nobody (Angel Bridge) (NOUVELLE)

- [x] Etape 2 : carte(s) de reference : `56041` Patriot (Tough sur soi) ; `td005` (Cloaked) ; `tl005`/`tl006` (choix entre options)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a tough OR cloaked » (une seule, deux cas), « on THEM » (Nobody) ; homonyme unique de `ta002` (Q-UP3)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 3, PV 3, ATK 2*, THW 2**, RES B
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up024 ...` : 2/2 verts avec module/lien ; substitution : 2/2 cas sujets ROUGES sans. 
      - OK / sans : KO : up024 Nobody : Reponse -> option Tenace
      - OK / sans : KO : up024 Nobody : Reponse -> option Camoufle
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 2 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? OUI : Tenace ou Camoufle (rendu existant). Cas plateau : `ui-app/src/board/tmnt-protection-plateau.test.ts` (7/7 verts d'emblee : aucun correctif necessaire, le rendu generique existait deja ; temoin d'absence id 999).

Carte terminee : NON : en attente de Q-UP3 (unicite partagee avec ta002 ; codee selon la regle normale).

### up025 : Powerful Punch (IDENTIQUE 32014)

> **Converti en art alternatif de 32014 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up025` n'existe plus dans `cards.json` (image `32014_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `32014` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"32014"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « When an enemy INITIATES an attack », « 4 damage to THAT enemy »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 2, RES R, 4 degats
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up025 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up025 Powerful Punch : quand Rhino attaque, 4 degats a Rhino
      - OK / sans : OK : up025 TEMOIN 32014 (officielle) : Powerful Punch : quand Rhino attaque, 4 degats a Rhino
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 5 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up026 : Primal Provisions (NOUVELLE)

- [x] Etape 2 : carte(s) de reference : `ua015` (Rampage) ; `tr006`/`19030` (`MaxOnePerPhase`) ; fiche rampage.md lue AVANT
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Max 1 per PHASE », Rampage = cout (2 degats + 2 cartes) avant la pioche, « Hero Action »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 0*, Rampage 2, 2 cartes, RES Y
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up026 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up026 Primal Provisions : Rampage 2 paye puis 2 cartes piochees
      - OK / sans : KO : up026 Primal Provisions : TEMOIN D'EPUISEMENT « Max 1 per phase » : la 2e copie reste en main
- [x] Etape 7 bis : limite imprimee ? OUI (Max 1 per phase) : temoin, deux copies dans la meme phase -> la 2e reste en main, un seul Rampage paye.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 5 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI.

### up027 : Protection Training (MODIFIEE de 32013)

- [x] Etape 2 : carte(s) de reference : `32013` Protective Training ; `CardFinder(traits=[...])` = OU (finder.py)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « NINJA OR MUTANIMAL ally » (deux branches + contre-cas Jessica Jones), « Max 1 TRAINING upgrade per ally » (moteur, ability.py), « +3 hit points »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES B, +3 PV
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up027 ...` : 3/3 verts avec module/lien ; substitution : 3/3 cas sujets ROUGES sans. 
      - OK / sans : KO : up027 Protection Training : s'attache a un allie NINJA (Honor Blade? non : Wonder Turtle) -> +3 PV
      - OK / sans : KO : up027 Protection Training : allie MUTANIMAL seul (Seymour Gutz up034) -> jouable, +3 PV
      - OK / sans : KO : up027 Protection Training : seul allie X-MEN/autre (Jessica Jones 01059) -> injouable
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties, 0 traceback ; carte JAMAIS jouee par le pilote (couverte par ses cas seulement) (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? OUI : amelioration attachee a un allie (rendu d'attachement de racine existant). Cas plateau : `ui-app/src/board/tmnt-protection-plateau.test.ts` (7/7 verts d'emblee : aucun correctif necessaire, le rendu generique existait deja ; temoin d'absence id 999).

Carte terminee : OUI.

### up028 : Rabid Infection (NOUVELLE)

- [x] Etape 2 : carte(s) de reference : `43012` Puncture Wound (« enemy that X attacked this turn », `this_turn_made_attack`) ; `sk093` (`apply=` + Gain<MotCle>) ; `stunned.py` (« When attached enemy activates ») ; vulnerable.md
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a MINION that YOUR HERO attacked THIS TURN » (contre-cas non attaque), « non-ELITE » (contre-cas Killmonger), « gains vulnerable » (Sonne -> defausse ; « is or becomes » code a la main), « When attached minion ACTIVATES », « AN enemy »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 0, RES R, 1 degat
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up028 ...` : 4/4 verts avec module/lien ; substitution : 4/4 cas sujets ROUGES sans. 
      - OK / sans : KO : up028 Rabid Infection : sbire attaque par le heros -> attachee, vulnerable : Sonne = defausse
      - OK / sans : KO : up028 Rabid Infection : sbire NON attaque ce tour -> injouable
      - OK / sans : KO : up028 Rabid Infection : sbire ELITE (Killmonger 01157) -> pas vulnerable, survit au Sonne
      - OK / sans : KO : up028 Rabid Infection : le sbire s'active (attaque) -> 1 degat a un ennemi (Rhino)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties, 0 traceback ; carte JAMAIS jouee par le pilote (couverte par ses cas seulement) (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? OUI : amelioration attachee a un SBIRE (rendu existant des attachements d'ennemi). Cas plateau : `ui-app/src/board/tmnt-protection-plateau.test.ts` (7/7 verts d'emblee : aucun correctif necessaire, le rendu generique existait deja ; temoin d'absence id 999).

Carte terminee : OUI.

### up029 : Ready for a Fight (IDENTIQUE 52019)

> **Converti en art alternatif de 52019 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up029` n'existe plus dans `cards.json` (image `52019_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `52019` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"52019"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : coquille « Intterupt » sur le scan (lecture sans ambiguite : Interrupt, comme 52019), Requirement recopie dans desc, « change to hero form », « attacks you INSTEAD »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES R, Requirement R, MaxPerUnit 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up029 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up029 Ready for a Fight : Rhino allait manigancer -> forme heros, Rhino attaque a la place
      - OK / sans : OK : up029 TEMOIN 52019 (officielle) : Ready for a Fight : Rhino allait manigancer -> forme heros, Rhino attaque a la place
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 1 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up030 : Redirection Mastery (NOUVELLE, défense exacte)

- [x] Etape 2 : carte(s) de reference : (a remplir apres Q-UP1) : `38014` Judoka Skill / `10031` (Reponse apres defense)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « exactly defend » : lecture incertaine -> Q-UP1
      Resultat : EN ATTENTE (Q-UP1).
- [x] Etape 6 : nombres texte <-> code : cout 2, RES R, MaxPerUnit 1
      Resultat : conforme.
- [ ] Etape 7 : AUCUN cas (voir « Carte terminee »).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties, 0 traceback ; carte JAMAIS jouee par le pilote (couverte par ses cas seulement) (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

**Réponse du 17/10/2026, lecture choisie « DÉFENSE EXACTE »** : après que votre héros défend contre une attaque, la Réponse ne part que si la
valeur de l'attaque (boosts compris) est EXACTEMENT égale à votre DEF pour cette attaque (coup paré pile, 0 dégât) ; l'attaquant
subit alors des dégâts égaux à votre DEF.

- [x] Étape 2 : `09020` Unflappable (« Play under any player's control » = `CanPlayThisUpgradeCard("Players")`, Response après
      défense) ; `62015` Take a Stand (`AfterUnitDefendEnd(HeroResponse, "YourHero", ...)`) ; `40165` Stryfe
      (`attacker.TakeDamage(this, value, effect)`). Mot-clé : aucun (SKILL = trait).
- [x] Étape 5 : « exactly defend » (égalité stricte attaque == DEF, sans plafond), « YOUR DEF FOR THAT ATTACK » (DEF retenue pour
      ce coup), « the attacker » (de CETTE attaque, encore en jeu), « Hero Response » (défenseur = votre HÉROS), Max 1 per player.
      Résultat : conforme.
- [x] Étape 6 : coût 2, RES R, MaxPerUnit 1, dégâts = DEF. Résultat : conforme.
- [x] **EXTENSION MOTEUR** : `Message.AfterUnitDefendEnd` porte `damage_before_defense` (valeur de l'attaque avant le retrait
      de la DEF) et `defense_value` (DEF retenue), renseignés par `can_attack.py` ; `dealt_damage` est plafonné à 0 et ne distingue
      pas parade pile / attaque inférieure à la DEF. Paramètres facultatifs : les autres lecteurs du message ne changent pas.
- [x] Étape 7 : 5 cas `[up] up030 ...` (Spider-Man DEF 3) : attaque = DEF (Melter ATQ 3) -> Melter subit 3, héros 0 ; attaque >
      DEF (Titania) -> rien, héros 3 ; attaque < DEF (Rhino ATQ 2) -> rien ; BOOSTS comptent (Rhino 2 + boost 1 = 3) -> Rhino
      subit 3 ; TÉMOIN sans la carte -> rien. 5/5 verts. **Substitution** (module retiré) : les 2 cas « part » ROUGES, les 3 cas
      d'absence verts (assumé).
- [x] Étape 7 bis : « Max 1 per player » = donnée (`MaxPerUnit`) : NON.
- [x] Étape 8 : autoplay du 17/10 (section en fin de fichier de Basic).
- [x] Étape 8 bis : NON (dégâts : jauge déjà dessinée).

Carte terminée : OUI.

### up031 : Road Rage (Raph) (MODIFIEE de 01066 Hawkeye)

- [x] Etape 2 : carte(s) de reference : `01066` Hawkeye (copie, 3 compteurs « fuel » au lieu de 4 « arrow »)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « 3 FUEL counters », « After A minion enters play », « remove 1 -> deal 2 to THAT minion »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 3, PV 3, ATK 2*, THW 1*, RES B (scan), 3 compteurs, 2 degats
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up031 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up031 Road Rage : entre avec 3 compteurs fuel ; un sbire entre -> 2 degats, 2 compteurs restent
      - OK / sans : OK : up031 TEMOIN 01066 Hawkeye : meme montage, 4 compteurs arrow -> 3
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 2 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (compteur `fuel` ajoute).

### up032 : Ronin (IDENTIQUE 60053)

> **Converti en art alternatif de 60053 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up032` n'existe plus dans `cards.json` (image `60053_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `60053` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"60053"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « While you do NOT control any allies », « +1 DEF AND retaliate 1 » ; unique ✦
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES B, +1 DEF, riposte 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up032 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up032 Ronin : sans allie, +1 DEF et riposte 1
      - OK / sans : OK : up032 TEMOIN 60053 (officielle) : Ronin : sans allie, +1 DEF et riposte 1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties, 0 traceback ; carte JAMAIS jouee par le pilote (couverte par ses cas seulement) (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up033 : Senkon (NOUVELLE)

- [x] Etape 2 : carte(s) de reference : `54018` Bambino (restricted gagne sur une identite, copie exacte) ; `38014` Judoka Skill (-ATK pour l'attaque defendue) ; restricted.md
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Attach to a FRIENDLY character », « While attached to an IDENTITY -> restricted » (deux cas), « ATTACHED character defends against an ENEMY attack », « exhaust Senkon -> -1 ATK for THAT attack »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES R, -1 ATQ, restricted 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up033 ...` : 3/3 verts avec module/lien ; substitution : 2/3 cas sujets ROUGES sans. 
      - OK / sans : KO : up033 Senkon : attache a Jessica Jones qui defend contre Rhino -> Rhino -1 ATQ (1 degat au lieu de 2)
      - OK / sans : OK : up033 Senkon : attache a un ALLIE -> pas restricted  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
      - OK / sans : KO : up033 Senkon : attache a l'IDENTITE -> restricted
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 5 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? OUI : amelioration attachee a un allie ou a l'identite (rendu existant). Cas plateau : `ui-app/src/board/tmnt-protection-plateau.test.ts` (7/7 verts d'emblee : aucun correctif necessaire, le rendu generique existait deja ; temoin d'absence id 999).

Carte terminee : OUI.

### up034 : Seymour Gutz (bandeau Rogue) (IDENTIQUE 48012)

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"48012"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ANOTHER friendly character », « printed THW and ATK », « Limit once per round » (porte par le module officiel) ; coquille « Seymor » dans le texte (sans effet) ; bandeau ✦ Rogue -> unique_also
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 4, PV 3, ATK 2*, THW 2*, RES R
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up034 ...` : 4/4 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up034 Seymour Gutz : 1 degat a Jessica Jones -> + ATQ 2 et CTR 1 imprimes jusqu'a la fin du round
      - OK / sans : OK : up034 TEMOIN 48012 (officielle) : Seymour Gutz : 1 degat a Jessica Jones -> + ATQ 2 et CTR 1 imprimes jusqu'a la fin du round
      - OK / sans : OK : up034 unicite : Rogue (48012) en jeu -> up034 n'est PAS jouable (bandeau « Rogue »)
      - OK / sans : OK : up034 unicite : TEMOIN, sans Rogue en jeu, up034 est jouable
- [x] Etape 7 bis : limite imprimee ? OUI (once per round) : portee par le module 48012 inchange ; pas de temoin d'epuisement propre (identique a l'officielle, non mesure).
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 1 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up035 : Shield Spell (IDENTIQUE 21061)

> **Converti en art alternatif de 21061 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up035` n'existe plus dans `cards.json` (image `21061_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `21061` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"21061"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Play only if your identity has the MYSTIC trait » (cas sur Doctor Strange), « discard THAT MANY cards », « Max 1 per deck » (desc)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 0, RES Y, MaxPerDeck 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up035 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up035 Shield Spell : identite MYSTIC (Doctor Strange), attaque de Rhino entierement prevenue, 2 cartes du deck defaussees
      - OK / sans : OK : up035 TEMOIN 21061 (officielle) : Shield Spell : identite MYSTIC (Doctor Strange), attaque de Rhino entierement prevenue, 2 cartes du deck defaussees
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties, 0 traceback ; carte JAMAIS jouee par le pilote (couverte par ses cas seulement) (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up036 : Stand Alone (IDENTIQUE 60054)

> **Converti en art alternatif de 60054 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up036` n'existe plus dans `cards.json` (image `60054_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `60054` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"60054"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « if you do NOT control any allies », « exhaust Stand Alone -> ready your hero »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES Y, MaxPerUnit 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up036 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up036 Stand Alone : sans allie, l'attaque de Rhino redresse le heros
      - OK / sans : OK : up036 TEMOIN 60054 (officielle) : Stand Alone : sans allie, l'attaque de Rhino redresse le heros
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 2 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up037 : Taunt (IDENTIQUE 56048)

> **Converti en art alternatif de 56048 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up037` n'existe plus dans `cards.json` (image `56048_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `56048` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"56048"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « The VILLAIN attacks you », « Other characters cannot defend », « Draw 3 »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES R, 3 cartes
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up037 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up037 Taunt : Rhino attaque, puis 3 cartes piochees
      - OK / sans : OK : up037 TEMOIN 56048 (officielle) : Taunt : Rhino attaque, puis 3 cartes piochees
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties, 0 traceback ; carte JAMAIS jouee par le pilote (couverte par ses cas seulement) (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up038 : The Best Offense... (IDENTIQUE 60052)

> **Converti en art alternatif de 60052 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up038` n'existe plus dans `cards.json` (image `60052_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `60052` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"60052"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Temporary » (desc), « +1 DEF », « DEF in place of THW AND ATK »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES B, +1 DEF
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up038 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up038 The Best Offense... : l'attaque de base utilise la DEF (3 + 1 = 4)
      - OK / sans : OK : up038 TEMOIN 60052 (officielle) : The Best Offense... : l'attaque de base utilise la DEF (3 + 1 = 4)
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 4 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up039 : Tonfa (NOUVELLE)

- [x] Etape 2 : carte(s) de reference : EXTENSION MOTEUR `Message.WhenCalculatingAttackDamage` ; `42004` Aerial Agility (retaliate pour l'attaque) ; `38014` ; restricted.md / retaliate.md
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « When CALCULATING DAMAGE during an attack against YOU » (fenetre ajoutee au moteur), « exhaust -> » (cout), « EITHER +1 DEF OR retaliate 1 » (deux cas + ligne de base), Restricted (desc)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES R, +1 DEF, riposte 1, Restricted 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up039 ...` : 3/3 verts avec module/lien ; substitution : 2/2 cas sujets ROUGES sans. 
      - OK / sans : KO : up039 Tonfa : attaque non defendue de Rhino -> option riposte 1 : Rhino subit 1
      - OK / sans : KO : up039 Tonfa : Titania (ATQ 6) attaque, le heros defend (DEF 3) -> option +1 DEF : 2 degats au lieu de 3
      - OK / sans : OK : up039 Tonfa : ligne de base SANS Tonfa, Titania contre DEF 3 -> 3 degats
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 4 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (extension moteur).

### up040 : Unflappable (IDENTIQUE 09020)

> **Converti en art alternatif de 09020 le 17/10/2026** : seule l'image différait de l'officielle, la carte `up040` n'existe plus dans `cards.json` (image `09020_tmnt.jpg`, `data/arts_alternatifs.json`). Les cas du reskin sont supprimés, le TÉMOIN sur `09020` est conservé. Ce qui suit est l'historique.

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"09020"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « After you defend AND take no damage », « exhaust -> draw 1 »
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 1, RES B, 1 carte, MaxPerUnit 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up040 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up040 Unflappable : defense sans degat -> incline, pioche 1
      - OK / sans : OK : up040 TEMOIN 09020 (officielle) : Unflappable : defense sans degat -> incline, pioche 1
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 3 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up041 : Usagi Yojimbo (NOUVELLE)

- [x] Etape 2 : carte(s) de reference : `53011` Draw Their Fire (`not_need_to_exhaust`) ; RR v1.8 « Defending » ; retaliate.md / toughness.md (desc)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « does not exhaust TO DEFEND » (pret apres defense ; incline = peut defendre, RR ; ne deborde pas sur un autre allie), Retaliate 2, Toughness
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 3, PV 3, ATK 2*, THW 1*, RES Y, Retaliate 2, Toughness 1
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up041 ...` : 5/5 verts avec module/lien ; substitution : 2/3 cas sujets ROUGES sans. 
      - OK / sans : KO : up041 Usagi Yojimbo : defend sans s'incliner (reste pret), Tenace consomme, Riposte 2 sur Rhino
      - OK / sans : KO : up041 Usagi Yojimbo : INCLINE, il peut quand meme defendre (RR v1.8, « Defending »)
      - OK / sans : OK : up041 Usagi Yojimbo : la capacite ne deborde PAS sur un autre allie (Jessica Jones defend et s'incline)  <- contre-cas d'ABSENCE ou donnee de desc : reste vert sous substitution (assume, PROCESSUS-CARTE §7.3)
      - OK / sans : OK : up041 TEMOIN moteur 53011 Draw Their Fire : Falcon defend sans s'incliner (correctif cost_func.Exhaust)
      - OK / sans : OK : up041 TEMOIN : un allie ordinaire (Jessica Jones) s'incline pour defendre
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 5 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (correctif moteur cost_func.Exhaust, temoin 53011 vert).

### up042 : What Doesn't Kill Me (IDENTIQUE 27016)

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"27016"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Requirement (physical) » (desc), « Heal 2 from your hero -> ready » (cout soin)
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 2, RES R, soin 2
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up042 ...` : 2/2 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up042 What Doesn't Kill Me : soigne 2 et redresse le heros
      - OK / sans : OK : up042 TEMOIN 27016 (officielle) : What Doesn't Kill Me : soigne 2 et redresse le heros
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 4 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

### up043 : Wonder Turtle (Mikey, bandeau White Widow) (IDENTIQUE 54032)

- [x] Etape 2 : carte(s) de reference : reskin IDENTIQUE par `ability_link` (RECETTES §11) ; module de l'officielle relu : aucun nom ni card_id en dur ; `grep -rn '"54032"' src/game src/engine` : rien (ou commentaire seul)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « After you resolve the ability of a PREPARATION card you control », « equal to that card's PRINTED resource cost » ; bandeau ✦ White Widow -> unique_also
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : cout 4, PV 3, ATK 1*, THW 2*, RES B
      Resultat : conforme.
- [x] Etape 7 : cas `[up] up043 ...` : 4/4 verts avec module/lien ; substitution : 1/1 cas sujets ROUGES sans. 
      - OK / sans : KO : up043 Wonder Turtle : apres Defensive Stance (cout 2) resolue, soigne 2
      - OK / sans : OK : up043 TEMOIN 54032 (officielle) : Wonder Turtle : apres Defensive Stance (cout 2) resolue, soigne 2
      - OK / sans : OK : up043 unicite : White Widow (54032) en jeu -> up043 n'est PAS jouable (bandeau « White Widow »)
      - OK / sans : OK : up043 unicite : TEMOIN, sans White Widow en jeu, up043 est jouable
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : 16 parties (decks A/B) + 8 temoin Black Panther, 0 traceback ; carte jouee 4 fois (section Autoplay).
- [x] Etape 8 bis : change ce qu'on VOIT ? NON (chiffres, jauges deja dessinees).

Carte terminee : OUI (reskin : capacite de l'officielle prouvee par le temoin et la substitution ; Q-R2 deck-builder en attente).

## Autoplay (étape 8), 16/10/2026

`tools/autoplay.py`, Rhino normal, profil équilibré, 8 parties par deck, ports 35200+ :

| Deck | Contenu | Fins | Bloquées | Tracebacks (NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback) |
|---|---|---|---|---|
| `deck-up-A` (Black Panther) | nouvelles + modifiées : up004 ×2, up007, up009, up013-up016, up021-up024, up026-up028, up031, up033, up039, up041 | 4 schéma complété, 4 joueur éliminé | 0/8 | 0 sur 8 journaux |
| `deck-up-B` (Black Panther) | 23 reskins (tous sauf up035 MYSTIC) | 7 schéma, 1 éliminé | 0/8 | 0 sur 8 journaux |
| témoin `black_panther` (départ) | — | 7 schéma | 1/8 | 0 sur 8 journaux |

Cartes JOUÉES (« s'apprête à jouer », 16 journaux) : up001 3, up002 5, up004 5, up005 1, up006 1, up007 3,
up010 5, up011 2, up012 2, up013 4, up014 2, up015 1, up016 3, up017 2, up018 6, up019 1, up020 8, up021 4,
up022 2, up024 2, up025 5, up026 5, up029 1, up031 2, up033 5, up034 1, up036 2, up038 4, up039 4, up040 3,
up041 5, up042 4, up043 4. Jamais jouées par le pilote : up003, up008, up009, up023, up027, up028, up032,
up037 (couvertes par leurs cas seulement) ; up030 sans script (Q-UP1) ; up035 hors deck (identité MYSTIC).

Lecture du journal (extraits) : up004 Autodefenestration paie Rampage 2 (« inflige 2 dégâts à Black Panther »,
deux cartes du deck défaussées) puis « 2 dégâts de cette attaque évités » ; up039 Tonfa s'incline pendant le
calcul des dégâts de Rhino (« Tonfa s'active ») et Black Panther riposte 1 ; up033 Senkon s'incline quand Black
Panther défend.

## Régression des extensions moteur

Filtres relancés après `cost_func.Exhaust` et `WhenCalculatingAttackDamage` : `[rampage]` 6/6, `[reskin]` 11/11,
`[cloaked]` 13/13, `[dazed]` 48/48, `Overkill [regle]` 5/5, `[RR1.8]` 9/9, `[raphael]` 97/97, `[michelangelo]`
92/92, `[leonardo]` 77/77, `Retaliate` 9/9, `Riposte` 22/22, `defens` 46/46, `Defend` 3/3. Témoin officiel de
la mécanique « ne s'incline pas pour défendre » : `[up] up041 TEMOIN moteur 53011 Draw Their Fire` vert.
`tools/test_cards.py` : 6599 ok, 0 erreur. `tools/verifier_appels_modules.py ... tmnt_aspect_protection` : OK,
calibré (§9) : un module piège `upzz.py` appelant `Faces.AppelQuiNExistePas` a bien été signalé, puis retiré.
Plateau (étape 8 bis) : `ui-app/src/board/tmnt-protection-plateau.test.ts` 7/7.

## Ce qui n'est PAS prouvé

- Partie réelle dans le navigateur par un humain : non faite (aucun outil ne la remplace). En particulier :
  l'affichage du choix « +1 DEF / Riposte 1 » de Tonfa, le choix Tenace/Camouflé de Nobody, et l'absence
  d'annonce du coût Rampage avant paiement (même remarque que ua015).
- up003, up008, up009, up023, up027, up028, up032, up037 n'ont jamais été jouées par le pilote d'autoplay.
- up020 « Starting » et up034 « Limit once per round » : portés par les modules officiels (60038, 48012)
  inchangés, pas de cas propre sur le reskin.
- Batterie complète non lancée (consigne : l'orchestrateur la lance après fusion).

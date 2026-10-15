# Super-Skrull (scenario 2 de Skrull Menace, Kajislav) et Kree-Skrull War — gabarits PROCESSUS-CARTE

Pack `skrull_menace`, card_id sk117-sk140 : scenario Super-Skrull (sk117-sk135 : 3 mechants, 2 complots principaux a 2 faces, 4 pouvoirs
SUPERPOWER, 10 cartes de rencontre) et set modulaire Kree-Skrull War (sk136-sk140). 26 entrees cards.json (19 + 5 card_id, faces a/b comprises).
Fiches generees le 15/10/2026 a partir des resultats REELS (rapport test_capacites, sorties de substituer_pack.py, en-tetes des modules).

Rappels communs a toutes les cartes :
- **Etape 6 (nombres)** : stats, PV (14/16/19 par joueur), menaces (depart / objectif / escalade), boosts et icones relus sur les SCANS de l'auteur
  contre `data/cards.json` ; corrections de lecture par rapport a la transcription : Lord Kl'rt porte l'icone d'AMPLIFICATION (croix + avion), pas une
  « icone de heros » ; Rock Mimicry : badge ATK a etoile seule sans valeur (decision utilisateur du 15/10).
- **Icones de ressource de Mt'nox / Hypnotic Gaze** : verifiees contre des cartes du MEME PACK (PROCESSUS-CARTE etape 3), pas a vue : poing = `sk049`
  The Thing (RES R), eclair = `sk044` Lazerfist (Y), noeuds = `sk043` New York Bookstore (B), etoile = `sk045` Ministerial Tiara (G).
- **Etape 7 (tests)** : 73 cas `[super_skrull]` dans `tools/cas/super_skrull.py` (tous verts), plus les 72 cas `[sk-e]` du scenario 1 et les cas Hulkling non
  touches. Montage : `RAZ` (retire le pouvoir attache a la mise en place par la graine du harnais), `NEUTRE` (deck rencontre sans icone de boost).
- **Substitution** (`substituer_pack.py`, empreinte du pack identique avant/apres : 76425945ac38aeb3fded3740f5bf6bff) : CHAQUE module a au moins un cas qui
  tombe au rouge sans lui. Les cas qui restent verts sans module sont, un a un : des TEMOINS ou CONTRE-CAS d'absence d'effet (assumes), les cas de
  donnees natives (PV par joueur, Permanent, heritage des attachements entre stades). Un premier passage a aussi trouve deux cas VIDES (stades II et III,
  expert : le montage laissait deja 2 pouvoirs, sk125 attache par la graine) et un cas de surge qui ne mesurait rien (le harnais ne pose pas
  `v18_surge`) : corriges, voir « Bugs trouves » ci-dessous.
- **Etape 8 (autoplay)** : 16 parties spider_man et 16 parties hulkling_kajislav (8 normal + 8 expert chacune) : 0 traceback dans les 32 journaux,
  32/32 parties terminees (21 eliminations, 10 complots acheves, 1 victoire en expert). Les 19 cartes du scenario et les 5 du modulaire apparaissent
  dans les journaux (Reponse obligatoire du mechant a chaque phase, remelange du paquet SUPERPOWER, Earth Involvement). Le bot n'est pas un juge
  d'equilibrage : il prouve que le scenario se joue sans erreur.
- **Outils statiques** : `verifier_appels_modules skrull_menace` OK (calibre : un appel inexistant ajoute a sk129 est bien signale, puis retire) ;
  `verifier_api_cartes` : aucune faute dans `super_skrull/` ni `kree_skrull_war/` ; `verifier_noms_modules`, `verifier_desc_mots_cles`,
  `verifier_cartes_en_jeu` : rien sur ces sets.
- **Etape 8 bis (plateau)** : `ui-app/src/board/super-skrull-plateau.test.ts` (5 cas, etat CAPTURE sur le moteur le 15/10/2026 par la sonde), vu ROUGE
  (3/5) sur un etat casse (pouvoir sans `bind_object_id`, compteurs perdus), puis VERT. Limite connue : le paquet SUPERPOWER n'a pas de zone dessinee
  (comme le paquet PLANET du scenario 1) ; les pouvoirs revelés, eux, se dessinent sur le mechant.
- **Moteur partage touche** : une ligne dans `Worlds.ASIDE_DECK_NAME` (`"SuperpowerDeck"`), voir `defs/super_skrull_moteur.md`.
- **Bugs trouves par les tests** : (1) `Puzzle.PutIntoPlay` sur une carte du paquet SUPERPOWER ne declenche pas son attache (le chemin reel, `Reveal`,
  marche) : les cas utilisent `Reveal` ; (2) les cartes defaussees du dessus d'un deck sont FACE CACHEE et `discard_pile.Get()` ne les enumere pas : cle
  `defausse_ids` (GetAll) dans le verificateur ; (3) un deck joueur d'une carte, vide apres defausse, remelange aussitot la defausse (regle du moteur) :
  les cas de Mt'nox / Hypnotic Gaze gardent des cartes de remplissage ; (4) Skrull Soldier (sk114) place lui-meme 2 menaces sur chaque annexe : le
  contre-cas « autre set » d'Earth Involvement utilise une traitrise sans effet.
- **Questions ouvertes** : `defs/super_skrull_questions.md` (10 points, dont le sort d'un pouvoir defausse, le wild de Hypnotic Gaze, le cout d'Invisibility
  paye apres l'inclinaison de l'attaquant).
- **Jeu reel** : jamais joue par un humain dans le navigateur ; ce qui manque pour le dire noir sur blanc : la zone d'affichage du paquet SUPERPOWER et le
  cout « avant declaration » d'Invisibility (le moteur n'a pas de cout additionnel par cible), qui ne se jugent qu'en partie reelle.


### sk117 : Super-Skrull

- [x] Etape 2 : carte(s) de reference : `04079b`, `hs107a` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk117.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « AFTER resolving step TWO ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "14*", "ATK": "2", "SCH": "1", "Stage": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk117 Super-Skrull I — Reponse obligatoire apres l'etape 2 : tout revient au paquet, UNE carte revelee » VERT; « sk117 Super-Skrull I — vaincu : le stade II herite des pouvoirs attaches (les attachements restent au mechant) » VERT; « sk117 Super-Skrull I — a DEUX joueurs : 28 PV (14 par joueur), Earth Involvement a 2 menaces, 2 joueurs dans la partie » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ; reste(nt) vert(s) sans module : sk117 Super-Skrull I — vaincu : le stade II herite des pouvoirs attaches (les attachements | sk117 Super-Skrull I — a DEUX joueurs : 28 PV (14 par joueur), Earth Involvement a 2 menac (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (le mechant porte de VRAIS PV (14 par joueur, pas de INF) et les pouvoirs qui lui sont attaches). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk118 : Super-Skrull

- [x] Etape 2 : carte(s) de reference : `04079b`, `hs107a` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk118.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « AFTER resolving step TWO ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "16*", "ATK": "2", "SCH": "1", "Stage": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Setup EXPERT : on commence au stade II (sk118), un pouvoir attache, paquet de 3 » VERT; « sk118 Super-Skrull II — Reponse obligatoire : DEUX cartes revelees (stade II) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme mechant au stade II). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk119 : Super-Skrull

- [x] Etape 2 : carte(s) de reference : `04079b`, `hs107a` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk119.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « AFTER resolving step TWO ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "19*", "ATK": "2", "SCH": "2", "Stage": "3"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk119 Super-Skrull III — stade III (expert) : deux cartes, et la defausse du paquet revient au paquet » VERT; « sk119 Super-Skrull III — PV 19 par joueur, SCH 2 (les trois stades ont leurs chiffres) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ; reste(nt) vert(s) sans module : sk119 Super-Skrull III — PV 19 par joueur, SCH 2 (les trois stades ont leurs chiffres) (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (meme mechant au stade III). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk120a : Searching for the Heir

- [x] Etape 2 : carte(s) de reference : `hs107a` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk120a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk120a Setup : paquet SUPERPOWER cree, sk120b revele, UN pouvoir attache au Super-Skrull » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (mise en place : cree le paquet SUPERPOWER (limite connue : cette pile n'a pas de zone dessinee, comme le paquet PLANET du scenario 1 ; les pouvoirs revelés, eux, sont dessines)). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk120b : Searching for the Heir

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk120b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Reveal ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "1", "TargetThreat": "6*", "EscalationThreat": "1*", "StartingThreat": "0"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk120a Setup : paquet SUPERPOWER cree, sk120b revele, UN pouvoir attache au Super-Skrull » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (revele un pouvoir : il s'attache et se dessine sur le mechant). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk121a : Heir to the Throne

- [x] Etape 2 : carte(s) de reference : `04077` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk121a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH player ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk121a Heir to the Throne 2A — Lord Kl'rt absent : il est cherche et attache au Super-Skrull » VERT; « sk121a Heir to the Throne 2A — Lord Kl'rt deja en jeu : une carte rencontre face cachee a chaque joueur » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attache Lord Kl'rt au mechant). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk121b : Heir to the Throne

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk121b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Reveal ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Stage": "2", "TargetThreat": "12*", "EscalationThreat": "2*", "StartingThreat": "2*"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk121b Heir to the Throne 2B — revelee : un pouvoir de plus est revele » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (revele un pouvoir : il s'attache et se dessine sur le mechant). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk122 : Flexibility

- [x] Etape 2 : carte(s) de reference : `gb014`, `01099`, `16133` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk122.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Super-Skrull GAINS stalwart ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"SCH+": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk122 Flexibility — +1 SCH et le Super-Skrull gagne stalwart (il ne peut plus etre etourdi) » VERT; « sk122 Flexibility — TEMOIN sans pouvoir : le Super-Skrull est bien etourdi, SCH imprime » VERT; « sk122 Flexibility — ses attaques gagnent Distance : la Riposte de l'allie defenseur est ignoree » VERT; « sk122 Flexibility — TEMOIN Riposte : sans Distance, le Super-Skrull encaisse la Riposte (1 degat) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ; reste(nt) vert(s) sans module : sk122 Flexibility — TEMOIN sans pouvoir : le Super-Skrull est bien etourdi, SCH imprime | sk122 Flexibility — TEMOIN Riposte : sans Distance, le Super-Skrull encaisse la Riposte (1 (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement au mechant). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk123 : Invisibility

- [x] Etape 2 : carte(s) de reference : `58027`, `50173` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk123.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ATTACK Super-Skrull ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"SCH+": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk123 Invisibility — +1 SCH » VERT; « sk123 Invisibility — attaquer le Super-Skrull coute 1 ressource : l'attaque part, une carte est depensee » VERT; « sk123 Invisibility — main vide : le cout ne peut pas etre paye, l'attaque est annulee » VERT; « sk123 Invisibility — TEMOIN sans pouvoir : l'attaque ne coute rien (2 degats, main intacte) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/4 ; reste(nt) vert(s) sans module : sk123 Invisibility — TEMOIN sans pouvoir : l'attaque ne coute rien (2 degats, main intacte (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement au mechant). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk124 : Pyrokinesis

- [x] Etape 2 : carte(s) de reference : `27176`, `vv003`, `ho016`, `50107b` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk124.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « FRIENDLY character ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"ATK+": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk124 Pyrokinesis — +1 ATK (le Super-Skrull passe de 2 a 3) » VERT; « sk124 Pyrokinesis — un personnage ami contre le complot principal : il prend 1 degat » VERT; « sk124 Pyrokinesis — CONTRE-CAS complot ANNEXE contre : aucun degat » VERT; « sk124 Pyrokinesis — ses attaques gagnent Perforant : la carte Tough du heros est defaussee ET il subit les degats » VERT; « sk124 Pyrokinesis — TEMOIN Tough : sans Perforant, la carte Tough absorbe l'attaque (0 degat) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/5 ; reste(nt) vert(s) sans module : sk124 Pyrokinesis — CONTRE-CAS complot ANNEXE contre : aucun degat | sk124 Pyrokinesis — TEMOIN Tough : sans Perforant, la carte Tough absorbe l'attaque (0 deg (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement au mechant). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk125 : Rock Mimicry

- [x] Etape 2 : carte(s) de reference : `60079`, `50107b` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk125.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « When Super-Skrull ATTACKS ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk125 Rock Mimicry — le Super-Skrull attaque avec UNE carte boost de plus (2 icones au lieu de 1) » VERT; « sk125 Rock Mimicry — TEMOIN : sans le pouvoir, une seule carte boost (3 degats) » VERT; « sk125 Rock Mimicry — ses attaques gagnent Dechainement : l'exces sur un allie vaincu va a l'identite » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ; reste(nt) vert(s) sans module : sk125 Rock Mimicry — TEMOIN : sans le pouvoir, une seule carte boost (3 degats) (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement au mechant). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk126 : Invisible Forcefield

- [x] Etape 2 : carte(s) de reference : `drive`, `60117`, `60167` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk126.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ENEMY »; « highest PRINTED hit points ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « sk126 Invisible Forcefield — revelee : s'attache a l'ennemi aux PV imprimes les plus eleves (le mechant) » VERT; « sk126 Invisible Forcefield — la 2e copie saute le mechant (deja protege) et va sur l'ennemi suivant » VERT; « sk126 Invisible Forcefield — aucun ennemi libre : elle gagne surge (la carte suivante est revelee) » VERT; « sk126 Invisible Forcefield — les degats vont sur la carte : le Super-Skrull ne perd rien, 2 jetons de degat ici » VERT; « sk126 Invisible Forcefield — a 5 degats ici ou plus : la carte est defaussee (3 puis 2 degats) » VERT; « sk126 Invisible Forcefield — TEMOIN : sans la carte, le Super-Skrull encaisse les 2 degats » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/6 ; reste(nt) vert(s) sans module : sk126 Invisible Forcefield — TEMOIN : sans la carte, le Super-Skrull encaisse les 2 degats (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement a un ennemi, avec des compteurs de degats visibles). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk127 : Lord Kl'rt

- [x] Etape 2 : carte(s) de reference : `gb014`, `sk115`, `16054` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk127.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Amplify": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk127 Lord Kl'rt — revele : s'attache au Super-Skrull ; porte l'icone d'amplification » VERT; « sk127 Lord Kl'rt — Action de heros : le cout revele un pouvoir, l'effet defausse Lord Kl'rt » VERT; « sk127 Lord Kl'rt — Boost : « Reveal this card » : revele pendant l'activation du mechant, il s'attache » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement au mechant avec icone d'amplification). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk128 : Mt'nox

- [x] Etape 2 : carte(s) de reference : `04145`, `sk114` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk128.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « UNDEFENDED »; « against YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "2", "ATK": "2*", "Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk128 Mt'nox — attaque non defendue, carte physique (Strength) : le mechant recoit Tough » VERT; « sk128 Mt'nox — attaque non defendue, carte energie (Energy) : le joueur est etourdi » VERT; « sk128 Mt'nox — attaque non defendue, carte mentale (Genius) : le joueur est desoriente » VERT; « sk128 Mt'nox — attaque non defendue, carte wild (Power of Justice) : TOUT (Tough, etourdi, desoriente) » VERT; « sk128 Mt'nox — CONTRE-CAS attaque DEFENDUE par un allie : rien n'est defausse, aucun statut » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/5 ; reste(nt) vert(s) sans module : sk128 Mt'nox — CONTRE-CAS attaque DEFENDUE par un allie : rien n'est defausse, aucun statu (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk129 : Praxagora

- [x] Etape 2 : carte(s) de reference : `50107b` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk129.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « attacks gain overkill ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "5", "SCH": "1", "ATK": "3*", "Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk129 Praxagora — ses attaques gagnent Dechainement : l'exces (2) sur Black Cat vaincue va a l'identite » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk130 : R'kin

- [x] Etape 2 : carte(s) de reference : `sk102`, `01182` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk130.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « WHEN DEFEATED ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "2", "SCH": "2", "ATK": "1", "Boost": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk130 R'kin — vaincu : on defausse jusqu'a un attachement, qui est revele (ici un Invisible Forcefield) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk131 : Galactic Council Membership

- [x] Etape 2 : carte(s) de reference : `27176`, `ho015` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk131.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a PLAYER attacks ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "3*"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk131 Galactic Council Membership — un joueur attaque le Super-Skrull : 1 menace sur le complot principal » VERT; « sk131 Galactic Council Membership — CONTRE-CAS : l'attaque vise un sbire, pas le Super-Skrull : aucune menace » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ; reste(nt) vert(s) sans module : sk131 Galactic Council Membership — CONTRE-CAS : l'attaque vise un sbire, pas le Super-Skr (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (complot annexe ordinaire (menace chiffree)).

Carte terminée : OUI

### sk132 : Skrull Warlords

- [x] Etape 2 : carte(s) de reference : `27189a`, `04079b` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk132.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ANY player's control ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2*", "Boost": "3"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk132 Skrull Warlords — un allie entre en jeu sous le controle du joueur : le mechant recoit une carte boost face cachee » VERT; « sk132 Skrull Warlords — TEMOIN : une carte de RENCONTRE qui entre en jeu ne donne aucune carte boost » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ; reste(nt) vert(s) sans module : sk132 Skrull Warlords — TEMOIN : une carte de RENCONTRE qui entre en jeu ne donne aucune c (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (complot annexe ordinaire, la carte boost donnee est face cachee dans la pile du mechant).

Carte terminée : OUI

### sk133 : Hypnotic Gaze

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk133.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « YOUR deck »; « FOR EACH resource ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk133 Hypnotic Gaze — 2 icones physiques defaussees : un personnage est etourdi par ressource (heros et allie) » VERT; « sk133 Hypnotic Gaze — 2 icones mentales defaussees : un personnage est desoriente par ressource » VERT; « sk133 Hypnotic Gaze — CONTRE-CAS energie + wild : aucune ressource physique ni mentale, aucun effet » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk134 : Power Multiplying

- [x] Etape 2 : carte(s) de reference : `sk106`, `sk120b` (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk134.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « If YOU CANNOT ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk134 Power Multiplying — revelee : un pouvoir de plus est revele (pas de surge) » VERT; « sk134 Power Multiplying — paquet SUPERPOWER vide : « If you cannot, this card gains surge » » VERT; « sk134 Power Multiplying — Boost : +1 icone par pouvoir attache (2 pouvoirs : ATK 2 + 2 icones = 4 degats) » VERT; « sk134 Power Multiplying — Boost TEMOIN sans pouvoir attache : aucune icone (ATK 2 = 2 degats) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/4 ; reste(nt) vert(s) sans module : sk134 Power Multiplying — Boost TEMOIN sans pouvoir attache : aucune icone (ATK 2 = 2 dega (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk135 : Villain's Versatility

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/super_skrull/sk135.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « sk135 Villain's Versatility — Pyrokinesis attache : 3 degats indirects au joueur » VERT; « sk135 Villain's Versatility — Rock Mimicry attache : le Super-Skrull recoit une carte Tough » VERT; « sk135 Villain's Versatility — Flexibility attache : le joueur defausse 1 carte de sa main » VERT; « sk135 Villain's Versatility — Invisibility attache : 2 menaces sur le complot principal » VERT; « sk135 Villain's Versatility — deux pouvoirs (Pyrokinesis + Invisibility) : les deux lignes s'appliquent » VERT; « sk135 Villain's Versatility — CONTRE-CAS aucun pouvoir attache : la carte ne fait rien » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/6 ; reste(nt) vert(s) sans module : sk135 Villain's Versatility — CONTRE-CAS aucun pouvoir attache : la carte ne fait rien (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk136 : Bel-Dann

- [x] Etape 2 : carte(s) de reference : `sk112`, `27141`, `04077` (detail et justification en tete de `src/cards/pack/skrull_menace/kree_skrull_war/sk136.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « put him INTO PLAY »; « reveal ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "1", "ATK": "3", "Boost": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk136 Bel-Dann — revele : Raksor est cherche dans le deck et mis en jeu engage avec le joueur » VERT; « sk136 Bel-Dann — Raksor est cherche aussi dans la DEFAUSSE rencontre » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (met un sbire en jeu engage avec le joueur). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk137 : Raksor

- [x] Etape 2 : carte(s) de reference : `sk136` (detail et justification en tete de `src/cards/pack/skrull_menace/kree_skrull_war/sk137.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucun mot-piege dans un texte de mots-cles.
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "2", "ATK": "2", "Boost": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk137 Raksor — revele : Bel-Dann est cherche et mis en jeu engage avec le joueur » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (met un sbire en jeu engage avec le joueur). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk138 : Earth Involvement

- [x] Etape 2 : carte(s) de reference : `60113a`, `40109`, `jj001b`, `27190` (detail et justification en tete de `src/cards/pack/skrull_menace/kree_skrull_war/sk138.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « AT LEAST 1 threat HERE ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "1*", "Permanent": "1", "Setup": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk138 Earth Involvement — Permanent + Setup : en jeu des la mise en place, menace 1 par joueur, crise tant qu'il y a de la menace » VERT; « sk138 Earth Involvement — menace contree jusqu'a 0 : elle RESTE en jeu (Permanent) et perd la crise » VERT; « sk138 Earth Involvement — Reponse obligatoire : une carte du set Kree-Skrull War revelee : +2 menaces ici » VERT; « sk138 Earth Involvement — CONTRE-CAS une carte d'un AUTRE set (Super-Skrull) revelee : pas de menace » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ; reste(nt) vert(s) sans module : sk138 Earth Involvement — menace contree jusqu'a 0 : elle RESTE en jeu (Permanent) et perd | sk138 Earth Involvement — CONTRE-CAS une carte d'un AUTRE set (Super-Skrull) revelee : pas (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot annexe Permanent + Setup, icone de crise conditionnelle (descripteur capture : crisis 1, permanent 1)). Cas plateau : `ui-app/src/board/super-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (3/5), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk139 : Imperial Kree Army

- [x] Etape 2 : carte(s) de reference : `sk106`, `46028`, `sk114` (detail et justification en tete de `src/cards/pack/skrull_menace/kree_skrull_war/sk139.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the top card »; « each boost icon (Y) ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk139 Imperial Kree Army — revelee : defausse le dessus (1 icone Y) : 1 degat a chaque personnage controle » VERT; « sk139 Imperial Kree Army — 2 icones Y defaussees : 2 degats a chaque personnage (pas 2 repartis) » VERT; « sk139 Imperial Kree Army — CONTRE-CAS dessus sans icone Y : aucun degat » VERT; « sk139 Imperial Kree Army — Boost : +2 menaces sur Earth Involvement (sans etre « revelee ») » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/4 ; reste(nt) vert(s) sans module : sk139 Imperial Kree Army — CONTRE-CAS dessus sans icone Y : aucun degat (temoin / contre-cas d'absence / donnee native : assume).
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

### sk140 : Skrull Imperial Fleet

- [x] Etape 2 : carte(s) de reference : `sk139`, `ho015`, `sk114`, `sk106` (detail et justification en tete de `src/cards/pack/skrull_menace/kree_skrull_war/sk140.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH scheme in play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module et contre le SCAN).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk140 Skrull Imperial Fleet — revelee : 1 menace par icone Y defaussee sur CHAQUE complot (principal et annexes) » VERT; « sk140 Skrull Imperial Fleet — Boost : +2 menaces sur Earth Involvement » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON (aucun « once per round » sur ces cartes).
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement).

Carte terminée : OUI

# Sets modulaires restants (Shaper of Worlds, Elites, Standard / Expert Skrull) — gabarits PROCESSUS-CARTE

Pack `skrull_menace`, card_id sk228-sk262 : **Shaper of Worlds** (sk228 sbire, sk229 complot annexe, sk230a-d quatre fragments),
les **cinq ensembles d'Elites** (Crusader sk231-235, Jazinda sk236-240, Skymax sk241-244, War Skrull sk245-249, Xavin sk250-253) et les
alternatives **Standard Skrull** (sk254-259) / **Expert Skrull** (sk260-262). 38 card_id ; sk246, sk247 et sk254 reutilisent le code de
sk098 / sk113 par `ability_link` (aucun script propre). Fiches generees a partir des resultats REELS (rapport test_capacites,
sorties de substituer_pack.py, en-tetes des modules) par `.planning/skrull-menace/defs/generer_gabarits_modulaires.py`.

Rappels communs a toutes les cartes :
- **Etape 6 (nombres)** : stats, PV (« par joueur » = `*`), menaces, boosts et icones relus sur les SCANS de l'auteur (1500x2150, tous vus un par un)
  contre `data/cards.json`. Lectures corrigees par rapport a la transcription (voir `defs/modulaires_questions.md`) : sk234 et sk248 portent une
  icone HAZARD, sk229 et sk239 ACCELERATION, sk252 AMPLIFY ; sk243 et sk249 n'en portent aucune ; sk262 est le numero imprime « 162 » (coquille).
- **Mise en place des sets (chemin reel)** : un scenario d'ESSAI `sk_essai_modulaires` (Rhino + les six modulaires de ce bloc, `modular_sets`) prouve que
  chaque set entre dans le deck rencontre (30 cartes) et que le sbire de Shaper et ses 4 fragments sont MIS DE COTE ; `sk_essai_skrull_standard` et
  `sk_essai_skrull_expert` prouvent que Standard Skrull (7 cartes) et Expert Skrull (3) REMPLACENT Standard et Expert (aucune carte officielle dans le deck).
  Ces scenarios ne sont pas declares dans `sets_info.json` : invisibles de l'ecran de choix.
- **Etape 7 (tests)** : cas `[modulaires]` dans `tools/cas/modulaires.py` (charge par `tools/test_capacites.py`), **117/117 verts**. Pieges payes :
  - `Puzzle.Discard` ne voit pas la main : pour « discards an ally from their hand » on vide la main (`Puzzle.EmptyHand`) ;
  - `FindOrCreateFace` prend la PREMIERE copie du deck rencontre : une carte a deux exemplaires (sk242, sk249, sk251) se mesure apres `EmptyEncounterDeck` ;
  - defausser tout le deck rencontre l'epuise : la defausse est remelangee et un pion Acceleration pose (cas « jusqu'a » : toujours une carte au fond) ;
  - la main de depart de Spider-Man contient Great Responsibility (`01061`), qui remplace toute menace par des degats : `Puzzle.EmptyHand()` avant `SetThreat` ;
  - une carte de boost / de surge consomme le dessus du deck : sk261 donne d'abord la carte de boost, puis le surge revele la carte SUIVANTE ;
  - un « Retaliate » (Volstagg `21193`) et une carte Robuste mesurent Distance et Perçant de l'arme sk237 ; Black Cat (2 PV) mesure Deferlement.
- **Substitution (`substituer_pack.py`, cinq passes sk22/sk23/sk24/sk25/sk26, empreinte md5 du pack identique avant/apres)** : chaque module est vide a tour de role, les cas filtres
  sur son card_id doivent tomber. Les cas « vert sans module » de chaque fiche sont TOUS des temoins d'ABSENCE d'effet (nom « TEMOIN », « sans l'attachement »), des mesures de
  comportement NATIF (Surge de sk240 et sk261, Hazard de sk248 : cles `desc`) ou le repli « aucune cible » que le moteur applique de lui-meme (sk250 sans traitrise, sk260 sans
  sbire nemesis) : assumes comme le prevoit l'etape 7. sk246, sk247 et sk254 sans module propre : preuve PAR LIEN (module cible vide : sk098 pour sk246 / sk254, sk113 pour sk247 ; tous les cas rouges).
- **Etape 8 (autoplay)** : 16 parties `equilibre` spider_man contre `sk_essai_modulaires` (les 6 sets), 8 contre `sk_essai_skrull_standard`, 8 contre `sk_essai_skrull_expert`, 8 contre Rhino comme
  TEMOIN. Grep exhaustif `NameError|AttributeError|TypeError|KeyError|AssertionError|Traceback` et `<E>` sur les 32 journaux des sets du bloc : **0** (les seules lignes `<E>` de la fournee sont celles du TEMOIN Rhino :
  l'Action de heros de l'amelioration OFFICIELLE `01093` Tenacity, artefact connu du pilote, deja releve au lot Paibok). Les 38 card_id du bloc ont ete jouees au moins une fois (comptage
  dans les journaux). 0 victoire : le profil `equilibre` ne bat pas non plus Rhino (temoin 0/8), ce n'est pas un signal d'equilibrage ; 0 partie « bloquee » apres correctif.
  - **Defaut trouve PAR l'autoplay et corrige** : la premiere fournee (8 parties) avait une partie « bloquee » (graine 2) : l'Action de heros de `sk237` declarait une cible OBLIGATOIRE ; sans ressource [physical]
    le pilote la rejouait sans fin (`Hero_Action ... WhenPlayerInTurn failed`). Le choix de la cible est maintenant fait DANS l'effet et l'action n'est pas offerte sans autre ennemi ; 0 bloquee ensuite
    (cas `sk237 ... aucun AUTRE ennemi`). Aucun cas de la batterie ne le voyait.
- **Outils statiques** : `verifier_appels_modules skrull_menace` OK ; `verifier_api_cartes` sans faute dans skrull_menace (les deux outils ont ete calibres : une erreur plantee, `Worlds.NexistePas`, est bien relevee) ;
  `verifier_tous_les_decks` : 141/141 decks montent une partie.
- **Plateau (etape 8 bis)** : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (6 tests, etat CAPTURE sur le moteur par `sonde_campagne`), vu ROUGE sur un etat casse puis VERT ; `tsc --noEmit` propre.
- **Moteur partage** : aucune modification (`defs/modulaires_moteur.md`).
- **Limites connues et questions** : `defs/modulaires_questions.md` (icones, ordre de Replaced Archenemy, Surprising Alliance remplacement, Xavin et les evenements TREACHERY de Lyja, mise de cote de Shaper, interface Standard / Expert Skrull...).
- **Ce qu'aucun outil ne voit** : une vraie partie jouee par un humain dans le navigateur (agrement des ensembles, equilibrage du bot), non faite.



### sk228 : Shaper of Worlds

- [x] Etape 2 : carte(s) de reference : `24045`, `bk002`, `vz036`, `sk139` (detail et justification en tete de `src/cards/pack/skrull_menace/shaper_of_worlds/sk228.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a PLAYER attacks ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "INF", "SCH": "2", "ATK": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk228 Reponse forcee : un joueur attaque Shaper of Worlds -> la carte est melangee dans SON deck » VERT; « sk228 Reponse forcee, TEMOIN : attaquer un AUTRE sbire ne melange pas Shaper (il reste en jeu) » VERT; « sk228 Interruption forcee : Shaper entre en MAIN (pioche) -> 4 cartes du deck rencontre defaussees, Shaper en jeu, main vide » VERT; « sk228 Interruption forcee, TEMOIN : une carte ordinaire piochee ne declenche rien (rien n'est defausse du deck rencontre) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (sbire aux PV infinis (pastille INF) ; melange dans le deck du joueur apres une attaque). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk229 : Cosmic Cube Creation

- [x] Etape 2 : carte(s) de reference : `60038`, `sk100`, `sk136` (detail et justification en tete de `src/cards/pack/skrull_menace/shaper_of_worlds/sk229.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « SET-ASIDE ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2", "Hinder": "4*", "Victory": "2", "Acceleration": "1", "Boost": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk229 mise en place : le sbire Shaper of Worlds et les 4 fragments sont MIS DE COTE (insert du set) » VERT; « sk229 Cosmic Cube Creation revelee : le Shaper MIS DE COTE entre en jeu engage ; menace 2 + Hinder 4 ; icone Acceleration » VERT; « sk229 Quand vaincu : le joueur choisit un fragment MIS DE COTE et le melange dans son deck » VERT; « sk229 Quand vaincu a DEUX joueurs : CHAQUE joueur choisit son propre fragment (un fragment pris n'est plus offert au suivant) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/4.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (mise de cote du sbire et des 4 fragments a la mise en place (pile annexe face cachee), Shaper mis en jeu a la revelation, fragments melanges dans les decks). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk230a : Cosmic Cube Fragment

- [x] Etape 2 : ressource sans texte de regle (texte d'ambiance seulement) : aucune capacite scriptee.
- [x] Etape 5 : sans objet (aucun mot a verifier).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"RES": "YYY"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk230a Cosmic Cube Fragment (YYY) : une ressource qui vaut TROIS energies (paie Crisis Interdiction, cout 2) » VERT.
      Substitution : sans objet (aucun module) ; la mesure porte sur les icones de ressource du `desc` (cas `sk230a`/`sk230d`), verte sans module PAR NATURE (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attend face cachee dans la pile annexe (mise de cote), puis passe dans un deck joueur). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk230b : Cosmic Cube Fragment

- [x] Etape 2 : ressource sans texte de regle (texte d'ambiance seulement) : aucune capacite scriptee.
- [x] Etape 5 : sans objet (aucun mot a verifier).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"RES": "BBB"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk230b Cosmic Cube Fragment (BBB) : trois icones MENTALES (paie le cout [mental][mental] de Distracted, qui se defausse) » VERT.
      Substitution : sans objet (aucun module) ; la mesure porte sur les icones de ressource du `desc` (cas `sk230a`/`sk230d`), verte sans module PAR NATURE (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attend face cachee dans la pile annexe (mise de cote), puis passe dans un deck joueur). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk230c : Cosmic Cube Fragment

- [x] Etape 2 : ressource sans texte de regle (texte d'ambiance seulement) : aucune capacite scriptee.
- [x] Etape 5 : sans objet (aucun mot a verifier).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"RES": "RRR"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk230c Cosmic Cube Fragment (RRR) : trois icones PHYSIQUES (paie le cout [physical] de Skrull Energy Gun, qui change d'ennemi) » VERT.
      Substitution : sans objet (aucun module) ; la mesure porte sur les icones de ressource du `desc` (cas `sk230a`/`sk230d`), verte sans module PAR NATURE (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attend face cachee dans la pile annexe (mise de cote), puis passe dans un deck joueur). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk230d : Cosmic Cube Fragment

- [x] Etape 2 : ressource sans texte de regle (texte d'ambiance seulement) : aucune capacite scriptee.
- [x] Etape 5 : sans objet (aucun mot a verifier).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"RES": "RBY"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk230d Cosmic Cube Fragment (RBY) : trois icones de TROIS couleurs (paie Swinging Web Kick, cout 3 : 8 degats a Rhino) » VERT.
      Substitution : sans objet (aucun module) ; la mesure porte sur les icones de ressource du `desc` (cas `sk230a`/`sk230d`), verte sans module PAR NATURE (assume).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attend face cachee dans la pile annexe (mise de cote), puis passe dans un deck joueur). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk231 : Crusader

- [x] Etape 2 : carte(s) de reference : `sk139`, `sk167`, `30037`, `hs007` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_crusader/sk231.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH character YOU control ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4*", "SCH": "2", "ATK": "2", "Victory": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk231 Crusader revele a DEUX joueurs : seuls les personnages du joueur a qui il est revele subissent le degat » VERT; « sk231 Crusader revele : 1 degat a CHAQUE personnage qu'on controle (identite et allie), aucune carte de boost si personne ne tombe » VERT; « sk231 Crusader revele : un allie VAINCU par ce degat -> 1 carte de boost face cachee au mechant » VERT; « sk231 Crusader revele : DEUX allies vaincus -> 2 cartes de boost » VERT; « sk231 Boost : la carte retournee en boost entre en jeu ENGAGEE avec le joueur » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 5/5.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (degats aux personnages et cartes de boost face cachee du mechant : jauges et pile de boost deja couvertes).

Carte terminée : OUI

### sk232 : Enemy Adaptation

- [x] Etape 2 : carte(s) de reference : `ip034`, `27152`, `sk146` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_crusader/sk232.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « SKRULL minion »; « the villain ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"SCH+": "1", "ATK+": "1", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk232 Enemy Adaptation revelee avec un sbire SKRULL en jeu : elle s'attache a lui (+1 MNG, +1 ATQ) » VERT; « sk232 Enemy Adaptation : SANS sbire SKRULL (un sbire non-Skrull est en jeu), elle s'attache au MECHANT » VERT; « sk232 Enemy Adaptation : « You cannot defend against attached enemy's attacks » -> le heros ne peut pas defendre » VERT; « sk232 Enemy Adaptation, TEMOIN : sans l'attachement le heros DEFEND et ne subit rien (Skrull Commander 2 ATQ contre DEF 3) » VERT; « sk232 Action de heros : donne 1 carte de boost au mechant -> la carte est defaussee » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement porte par un sbire SKRULL ou par le mechant). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk233 : Freedom Ring

- [x] Etape 2 : carte(s) de reference : `sk137`, `sk142`, `sk136`, `sk161`, `30037` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_crusader/sk233.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « If CRUSADER is not in play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk233 Freedom Ring revelee avec Crusader en jeu : elle s'attache a lui, qui devient VILLAINOUS » VERT; « sk233 Freedom Ring, Crusader ABSENT : defausse jusqu'a un sbire, le met en jeu engage et s'y attache (Villainous) » VERT; « sk233 Freedom Ring, Crusader absent et AUCUN sbire dans le deck : 1 carte de boost face cachee au mechant » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement porte par Crusader ou par un sbire amene en jeu). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk234 : Spy Training

- [x] Etape 2 : carte(s) de reference : `ls015`, `sk167` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_crusader/sk234.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « an ally YOU control ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "3*", "Hazard": "1", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk234 Spy Training revelee : un allie qu'on controle est VAINCU et le mechant recoit 1 carte de boost ; menace 3, Hazard » VERT; « sk234 Spy Training revelee SANS allie : la carte de boost est donnee quand meme (lecture : effets independants) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (defait un allie (zone deja couverte) et donne une carte de boost).

Carte terminée : OUI

### sk235 : Rivals to the End

- [x] Etape 2 : carte(s) de reference : voir en-tete (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_crusader/sk235.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Choose a MINION ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk235 Rivals to the End : le sbire choisi attaque le heros DEUX fois de suite (Skrull Commander ATQ 2 x 2 = 4 degats) » VERT; « sk235 Rivals to the End en ALTER-EGO : aucune attaque -> 1 carte de boost par personnage qu'on controle (identite + allie = 2) » VERT; « sk235 Rivals to the End, aucun sbire en jeu (heros) : aucune attaque -> 1 carte de boost (identite seule) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (attaques de sbire et cartes de boost : aucun nouvel element dessine).

Carte terminée : OUI

### sk236 : Jazinda

- [x] Etape 2 : carte(s) de reference : `sk168`, `hs222`, `hs007` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_jazinda/sk236.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « THE VILLAIN »; « +1 SCH ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "5*", "SCH": "3", "ATK": "1", "Victory": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk236 Jazinda en jeu : le MECHANT gagne +1 MNG » VERT; « sk236 Jazinda, TEMOIN : sans elle le mechant garde son MNG imprime » VERT; « sk236 Boost : la carte retournee en boost entre en jeu ENGAGEE avec le joueur » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (bonus de MNG du mechant : chiffre seulement).

Carte terminée : OUI

### sk237 : Skrull Energy Gun

- [x] Etape 2 : carte(s) de reference : `27152`, `ls015`, `sk086` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_jazinda/sk237.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « WHILE attached to a SKRULL enemy ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"ATK+": "1", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 11/11 cas verts : « sk237 Skrull Energy Gun revelee avec un sbire SKRULL en jeu : elle s'attache a lui (+1 ATQ) » VERT; « sk237 Skrull Energy Gun : les attaques de l'hote SKRULL gagnent OVERKILL (Black Cat, 2 PV, defend contre ATQ 3 : l'exces 1 passe au heros) » VERT; « sk237 Skrull Energy Gun, TEMOIN : sans l'arme, ATQ 2 contre Black Cat (2 PV) : pas d'exces, le heros est intact » VERT; « sk237 Skrull Energy Gun : PIERCING -> l'attaque ignore la carte Robuste de Volstagg et lui inflige ses 3 degats » VERT; « sk237 Skrull Energy Gun, TEMOIN : sans l'arme, la carte Robuste de Volstagg absorbe l'attaque (0 degat) » VERT; « sk237 Skrull Energy Gun : RANGED -> la Riposte de Volstagg est ignoree (le sbire ne perd aucun PV) » VERT; « sk237 Skrull Energy Gun, TEMOIN : sans l'arme, la Riposte de Volstagg blesse Skrull Commander (1 degat) » VERT; « sk237 Skrull Energy Gun sur un ennemi NON SKRULL (le mechant Rhino) : ni overkill ni piercing ni ranged, seulement +1 ATQ » VERT; « sk237 Action de heros : depenser une ressource [physical] -> la carte passe a un AUTRE ennemi (le mechant) » VERT; « sk237 Action de heros SANS choisir la cible (le pilote prend la premiere) : l'hote n'est JAMAIS une cible offerte » VERT; « sk237 Action de heros, aucun AUTRE ennemi (la carte est sur le mechant, seul ennemi) : l'action n'est PAS offerte » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 6/11 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement porte par un sbire SKRULL, deplace sur un autre ennemi (meme mecanisme que sk232)). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk238 : Sy-Torak Gem

- [x] Etape 2 : carte(s) de reference : `sk146`, `sk086` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_jazinda/sk238.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « attached CHARACTER »; « +3 hit points ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"ATK+": "1", "Boost": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk238 Sy-Torak Gem revelee avec Jazinda en jeu : elle s'attache a elle (+1 ATQ, +3 PV) » VERT; « sk238 Sy-Torak Gem, Jazinda ABSENTE : elle s'attache au MECHANT (Rhino 14 -> 17 PV) » VERT; « sk238 Action de heros : carte de boost au mechant ET une ressource [energy] -> la carte est defaussee » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement porte par Jazinda ou par le mechant, +3 PV (meme mecanisme que sk232)). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk239 : Stealing for the Empire

- [x] Etape 2 : carte(s) de reference : `sk144b`, `sk139`, `sk106` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_jazinda/sk239.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « until an ATTACHMENT is discarded ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "3", "Acceleration": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk239 Stealing for the Empire revelee : defausse jusqu'a un attachement, le revele, menace sur le complot PRINCIPAL = ses icones (Sy-Torak Gem : 3) » VERT; « sk239 Stealing for the Empire : attachement a 2 icones (Charge) -> 2 menaces sur le complot principal » VERT; « sk239 Stealing for the Empire, aucun attachement dans le deck : pas de menace sur le complot principal » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (defausse jusqu'a un attachement puis le revele : l'attachement suit la regle commune, menace sur le complot principal).

Carte terminée : OUI

### sk240 : Skrull of Royal Blood

- [x] Etape 2 : carte(s) de reference : `sk157`, `sk106` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_jazinda/sk240.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the HIGHEST number ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Surge": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk240 Skrull of Royal Blood : les cartes de la defausse rencontre au MAXIMUM d'icones de boost (2 : Charge et Ivory Horn) retournent dans le deck » VERT; « sk240 Skrull of Royal Blood : surge natif -> la carte du dessus du deck est revelee aussi » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (la defausse rencontre revient dans le deck : zones non dessinees).

Carte terminée : OUI

### sk241 : Skymax

- [x] Etape 2 : carte(s) de reference : `sk157`, `hs007` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_skymax/sk241.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ALL minions ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "5*", "SCH": "2", "ATK": "3", "Victory": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk241 Skymax revele : TOUS les sbires de la defausse rencontre retournent dans le deck (la traitrise reste) » VERT; « sk241 Skymax revele, TEMOIN : une defausse sans sbire ne bouge pas » VERT; « sk241 Boost : la carte retournee en boost entre en jeu ENGAGEE avec le joueur » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (la defausse rencontre revient dans le deck : zones non dessinees).

Carte terminée : OUI

### sk242 : Changing Appearance

- [x] Etape 2 : carte(s) de reference : `ip034`, `27152`, `sk099`, `40146` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_skymax/sk242.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « attached ENEMY »; « cannot be ATTACKED ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"SCH+": "2", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « sk242 Changing Appearance revelee avec un sbire SKRULL : elle s'attache a lui (+2 MNG) » VERT; « sk242 Changing Appearance : l'ennemi attache NE PEUT PAS ETRE ATTAQUE (le heros frappe Rhino a la place, Skrull Commander est intact) » VERT; « sk242 Changing Appearance, TEMOIN : sans l'attachement le heros attaque Skrull Commander (2 degats) » VERT; « sk242 Interruption forcee : l'ennemi attache qui allait attaquer COMPLOTE a la place (MNG 2 + 2 = 4 menaces), puis la carte est defaussee » VERT; « sk242 Interruption forcee, TEMOIN : sans l'attachement le meme sbire ATTAQUE (2 degats au heros, aucune menace) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement porte par un sbire SKRULL ou par le mechant (meme mecanisme que sk232)). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk243 : Surprising Alliance

- [x] Etape 2 : carte(s) de reference : `sw023`, `27171`, `sk141` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_skymax/sk243.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a player discards an ALLY FROM THEIR HAND ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2*", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk243 Surprising Alliance : un allie DEFAUSSE de la main entre en jeu engage comme SBIRE (SCH = THW imprime 1), il ne va pas a la defausse » VERT; « sk243 Surprising Alliance, TEMOIN : sans le complot l'allie defausse va a la defausse du joueur » VERT; « sk243 Surprising Alliance, TEMOIN : un evenement defausse de la main (Backflip) va a la defausse normalement » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (l'allie defausse devient un SBIRE engage (face echangee, image de l'allie conservee : meme mecanisme qu'Impostor, deja couvert par skrull-empire-plateau.test.ts)). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (test du lot 1 : etat capture sur le moteur, meme face echangee et meme attachement), VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk244 : Shape Alteration

- [x] Etape 2 : carte(s) de reference : `sk128`, `01188`, `24045` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_skymax/sk244.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH SKRULL ENEMY »; « stunned AND confused ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 4/4 cas verts : « sk244 Shape Alteration : retire Sonne et Desoriente des ennemis SKRULL et leur donne Robuste ; un ennemi non-Skrull est intact » VERT; « sk244 Shape Alteration : aucun ennemi SKRULL en jeu -> SURGE (la carte du dessus est revelee) » VERT; « sk244 Shape Alteration, TEMOIN : avec un ennemi SKRULL en jeu, PAS de surge (le deck n'est pas touche) » VERT; « sk244 Boost : un ennemi SKRULL (au choix du joueur) recoit une carte Robuste » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (cartes d'etat Robuste posees / Sonne et Desoriente retires sur les ennemis SKRULL (statuts deja couverts)). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk245 : War Skrull

- [x] Etape 2 : carte(s) de reference : `sk150`, `sk114`, `hs007` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_war_skrull/sk245.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ATTACKS YOU ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "5*", "SCH": "2", "ATK": "2*", "Victory": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk245 Reponse forcee : War Skrull attaque le joueur -> les 2 cartes du dessus de SON deck sont defaussees (3 -> 1) » VERT; « sk245 Reponse forcee, TEMOIN : l'attaque d'un AUTRE sbire ne defausse rien (le deck garde ses 3 cartes) » VERT; « sk245 Boost : la carte retournee en boost entre en jeu ENGAGEE avec le joueur » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (cartes defaussees du deck du joueur : pile non dessinee).

Carte terminée : OUI

### sk246 : Impostor

- [x] Etape 2 : meme texte que `sk098` : `ability_link: sk098` dans cards.json, AUCUN script propre (modele identique, voir son module).
- [x] Etape 5 : texte-contre-code : le texte imprime est mot pour mot celui de la carte liee (relu sur le scan) ; seul le « for this attack » de sk247 differe de « for this activation » de sk113 (le Boost n'a de sens que pendant une attaque : meme effet).
      Resultat : conforme.
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk246 Impostor (War Skrull) revele : un allie devient un sbire SKRULL engage (meme code que sk098, `ability_link`) » VERT; « sk246 Impostor (War Skrull) revele SANS allie : le mechant complote (menace sur le complot principal) » VERT.
      Substitution par LIEN (module `sk098` vide, empreinte identique apres) : 2/2 cas tombent au rouge.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement porte par l'allie devenu sbire (meme mecanisme qu'Impostor, deja couvert par skrull-empire-plateau.test.ts)). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (test du lot 1 : etat capture sur le moteur, meme face echangee et meme attachement), VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk247 : Skrull Commander

- [x] Etape 2 : meme texte que `sk113` : `ability_link: sk113` dans cards.json, AUCUN script propre (modele identique, voir son module).
- [x] Etape 5 : texte-contre-code : le texte imprime est mot pour mot celui de la carte liee (relu sur le scan) ; seul le « for this attack » de sk247 differe de « for this activation » de sk113 (le Boost n'a de sens que pendant une attaque : meme effet).
      Resultat : conforme.
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "5", "SCH": "2", "ATK": "2", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk247 Skrull Commander (War Skrull) : les AUTRES sbires SKRULL gagnent +1 ATQ (meme code que sk113, `ability_link`) » VERT; « sk247 Skrull Commander (War Skrull) Boost : si l'activation est une attaque, +2 icones (1 + 2 = 3 icones : Rhino ATQ 2 + 3 = 5 degats) » VERT.
      Substitution par LIEN (module `sk113` vide, empreinte identique apres) : 2/2 cas tombent au rouge.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (bonus d'ATQ : chiffre seulement).

Carte terminée : OUI

### sk248 : Skrull Geneticist

- [x] Etape 2 : carte(s) de reference : `ar012`, `16118`, `sk105` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_war_skrull/sk248.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « YOURSELF »; « FACEDOWN ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "3", "SCH": "3", "ATK": "0", "Hazard": "1", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk248 Skrull Geneticist Boost : le joueur se distribue 1 carte rencontre face cachee » VERT; « sk248 Skrull Geneticist en jeu : icone HAZARD (1 carte rencontre de plus a la phase du mechant) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (carte rencontre distribuee face cachee : deja couvert).

Carte terminée : OUI

### sk249 : Cloning Program

- [x] Etape 2 : carte(s) de reference : `sk033`, `sk154` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_war_skrull/sk249.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH SKRULL MINION »; « ADDITIONAL time ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "4", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 6/6 cas verts : « sk249 Cloning Program : chaque sbire SKRULL active UNE FOIS DE PLUS a l'etape 2 de la phase du mechant (Rhino 2 + Commander 2 + 2 = 6) » VERT; « sk249 Cloning Program, TEMOIN : sans le complot la meme phase fait 4 degats (Rhino 2 + Commander 2) » VERT; « sk249 Cloning Program, DEUX exemplaires : deux activations de plus (2 + 2 + 2 + 2 = 8) » VERT; « sk249 Cloning Program : une attaque HORS de l'etape 2 (Puzzle.Attack) n'est pas doublee (2 degats) » VERT; « sk249 Cloning Program : la menace ne peut PAS etre retiree tant qu'AUCUN sbire SKRULL n'est en jeu (4 menaces restent) » VERT; « sk249 Cloning Program, TEMOIN : avec un sbire SKRULL en jeu la meme contre retire 1 menace (4 -> 3) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/6 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (activations supplementaires : aucun nouvel element dessine).

Carte terminée : OUI

### sk250 : Xavin

- [x] Etape 2 : carte(s) de reference : `sk144b`, `hs007` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_xavin/sk250.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « until a TREACHERY is discarded ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "5*", "SCH": "2", "ATK": "3", "Victory": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk250 Xavin revele : defausse jusqu'a une TRAITRISE (un sbire est defausse au passage) et la revele (Advance : le mechant complote) » VERT; « sk250 Xavin revele : AUCUNE traitrise dans le deck -> tout le deck est defausse, rien n'est revele (pas de menace) » VERT; « sk250 Boost : la carte retournee en boost entre en jeu ENGAGEE avec le joueur » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (revele une traitrise : aucun nouvel element dessine).

Carte terminée : OUI

### sk251 : Invisible Forcefield

- [x] Etape 2 : carte(s) de reference : `sk086`, `39031` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_xavin/sk251.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « highest PRINTED hit points ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 7/7 cas verts : « sk251 Invisible Forcefield revele : elle s'attache a l'ennemi aux PV imprimes les plus eleves (Rhino 14 > Skrull Commander 5) » VERT; « sk251 Invisible Forcefield : un SECOND exemplaire ne s'attache pas au meme ennemi, il va au suivant (Skrull Commander) » VERT; « sk251 Invisible Forcefield : aucun ennemi eligible (le mechant en porte deja une, aucun sbire) -> SURGE » VERT; « sk251 Interruption forcee : les degats infliges a l'ennemi attache vont SUR la carte (Rhino intact, 2 jetons de degat) » VERT; « sk251 Interruption forcee, TEMOIN : sans la carte l'attaque blesse Rhino (2 degats) » VERT; « sk251 Seuil : 3 degats deja poses + 2 = 5 -> la carte est DEFAUSSEE, Rhino toujours intact » VERT; « sk251 Seuil, TEMOIN : 2 degats deja poses + 2 = 4 -> la carte RESTE en jeu avec 4 jetons » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 6/7 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement porte par l'ennemi, avec le compteur de degats detournes (c_damage : meme mecanisme que sk126 de Super-Skrull)). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk252 : Super-Skrull Training Program

- [x] Etape 2 : carte(s) de reference : `sk128` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_xavin/sk252.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH SKRULL ENEMY »; « a TOUGH status card ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "2*", "Amplify": "1", "Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk252 Super-Skrull Training Program revele : chaque ennemi SKRULL recoit une carte Robuste (le mechant non-Skrull non) ; icone Amplify » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (cartes d'etat Robuste posees sur les ennemis SKRULL (statut deja couvert)). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk253 : Going Nova

- [x] Etape 2 : carte(s) de reference : `sk163`, `jj020` (detail et justification en tete de `src/cards/pack/skrull_menace/skrull_elite_xavin/sk253.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « INDIRECT ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk253 Going Nova revelee : 2 degats indirects (1 joueur) -> l'identite les subit » VERT; « sk253 Going Nova revelee a DEUX joueurs : 4 degats indirects repartis entre tous les personnages (4 sur les deux identites) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (degats indirects : jauges seulement).

Carte terminée : OUI

### sk254 : Impostor

- [x] Etape 2 : meme texte que `sk098` : `ability_link: sk098` dans cards.json, AUCUN script propre (modele identique, voir son module).
- [x] Etape 5 : texte-contre-code : le texte imprime est mot pour mot celui de la carte liee (relu sur le scan) ; seul le « for this attack » de sk247 differe de « for this activation » de sk113 (le Boost n'a de sens que pendant une attaque : meme effet).
      Resultat : conforme.
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk254 Impostor (Standard Skrull) revele : un allie devient un sbire SKRULL engage (meme code que sk098, `ability_link`) » VERT; « sk254 Impostor (Standard Skrull) SANS allie : le mechant complote » VERT.
      Substitution par LIEN (module `sk098` vide, empreinte identique apres) : 2/2 cas tombent au rouge.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement porte par l'allie devenu sbire (meme mecanisme qu'Impostor, deja couvert par skrull-empire-plateau.test.ts)). Cas plateau : `ui-app/src/board/skrull-empire-plateau.test.ts` (test du lot 1 : etat capture sur le moteur, meme face echangee et meme attachement), VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk255 : Cursed by the Past

- [x] Etape 2 : carte(s) de reference : `01190` (detail et justification en tete de `src/cards/pack/skrull_menace/standard_skrull/sk255.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « YOUR nemesis minion / side scheme »; « is in play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk255 Cursed by the Past (rien en jeu) : le Vautour (sbire nemesis) et Highway Robbery (complot nemesis) sont reveles, le RESTE du set va dans le deck rencontre » VERT; « sk255 Cursed by the Past (Vautour et complot DEJA en jeu) : le Vautour active contre soi, le complot recoit sa menace de depart (3 + 3 = 6) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (revele les cartes du set nemesis : cartes standard du moteur (sbire, complot annexe)).

Carte terminée : OUI

### sk256 : Experiment Subject

- [x] Etape 2 : carte(s) de reference : `01188`, `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/standard_skrull/sk256.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « an UPGRADE you control ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk256 Experiment Subject : une amelioration qu'on controle est defaussee, le mechant ne complote pas » VERT; « sk256 Experiment Subject SANS amelioration : le mechant complote (menace 1) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (defausse d'une amelioration : zone deja couverte).

Carte terminée : OUI

### sk257 : Forge Ahead

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/standard_skrull/sk257.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « each minion ENGAGED WITH YOU »; « SCHEMES ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk257 Forge Ahead : chaque sbire engage avec soi complote (Skrull Commander MNG 2) et le mechant NE complote PAS » VERT; « sk257 Forge Ahead SANS sbire engage : le mechant complote (menace 1) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (manigances : menace seulement).

Carte terminée : OUI

### sk258 : Mobilization

- [x] Etape 2 : carte(s) de reference : `01189`, `01187`, `sk112`, `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/standard_skrull/sk258.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH minion IN PLAY ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk258 Mobilization (alter-ego) : chaque sbire en jeu s'engage avec LE JOUEUR, puis le mechant complote » VERT; « sk258 Mobilization (heros) : le mechant ET chaque sbire engage attaquent (Rhino 2 + Skrull Commander 2 = 4 degats) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (engagement des sbires : zones d'engagement deja couvertes).

Carte terminée : OUI

### sk259 : Stick to the Plan

- [x] Etape 2 : carte(s) de reference : `01187`, `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/standard_skrull/sk259.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the HERO »; « hero ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk259 Stick to the Plan : le mechant attaque le heros qui a le plus de PV RESTANTS (Captain Marvel 12 contre Spider-Man 10) » VERT; « sk259 Stick to the Plan : PV RESTANTS (pas PV max) : Captain Marvel a 3 degats (9 restants) -> Spider-Man (10) est attaque » VERT; « sk259 Stick to the Plan, joueur en ALTER-EGO : aucun heros -> aucune attaque, le mechant complote » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (attaque du mechant : jauges seulement).

Carte terminée : OUI

### sk260 : Replaced Archenemy

- [x] Etape 2 : carte(s) de reference : `sk098` (detail et justification en tete de `src/cards/pack/skrull_menace/expert_skrull/sk260.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « YOUR nemesis minion »; « Then, it activates ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"SCH+": "1", "Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « sk260 Replaced Archenemy (nemesis hors jeu) : le Vautour est trouve, la carte s'y attache, il est revele ; il gagne SKRULL et +1 MNG » VERT; « sk260 Replaced Archenemy (Vautour DEJA en jeu) : elle s'y attache puis il active contre soi (alter-ego : il complote, MNG 1 + 1 = 2) » VERT; « sk260 Replaced Archenemy : aucun sbire nemesis trouvable (retire de la partie) -> la carte est defaussee » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement porte par le sbire nemesis (meme mecanisme que sk232), qui gagne le trait SKRULL). Cas plateau : `ui-app/src/board/modulaires-skrull-plateau.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse, puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk261 : Focused Attention

- [x] Etape 2 : carte(s) de reference : `sk167`, `30037` (detail et justification en tete de `src/cards/pack/skrull_menace/expert_skrull/sk261.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the VILLAIN »; « FACEDOWN ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Surge": "1", "Boost": "3"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « sk261 Focused Attention : le mechant recoit 1 carte de boost face cachee ; surge natif (la carte du dessus est revelee) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (carte de boost face cachee du mechant : deja couvert).

Carte terminée : OUI

### sk262 : Tricky Assault

- [x] Etape 2 : carte(s) de reference : `01187`, `sk100` (detail et justification en tete de `src/cards/pack/skrull_menace/expert_skrull/sk262.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « FLIP to hero form ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2"} ; relu sur le scan 1500x2150. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « sk262 Tricky Assault : le joueur passe en forme HEROS, le mechant l'attaque ; attaque NON defendue -> le mechant complote en plus » VERT; « sk262 Tricky Assault, attaque DEFENDUE (Spider-Man DEF 3) : aucun degat et le mechant ne complote pas » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun.
- [x] Etape 8 bis : change ce qu'on voit ? NON (changement de forme du joueur et attaque : zones deja couvertes).

Carte terminée : OUI


---
**Bilan : 38/38 cartes terminees.**

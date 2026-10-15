# Hulkling (Kajislav) — gabarits PROCESSUS-CARTE

Pack `skrull_menace`, 31 card_id. Commandes et sorties : voir la fin du fichier.
Rappels communs a toutes les cartes :
- **Etape 6 (nombres)** : couts, stats, PV, boosts et icones de ressource relus sur les SCANS (planches du 15/10/2026, et recadrage des icones de ressource compare a armored_spidey, meme gabarit) contre `data/cards.json` et les chiffres du script : conformes pour les 31.
- **Etape 8 (autoplay)** : 8 parties `hulkling_kajislav` contre Rhino + 8 du temoin `spider_man`, profil equilibre. Aucune partie bloquee (8/8 finies des deux cotes), grep NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback : **0 dans les 16 journaux**. Journal lu sur l'origine (pioche apres depense KREE, retournement), Talos (degats consecutifs renvoyes) et Ancestors.
- **Outils statiques** : `test_cards` 6070 ok / 0 err ; `verifier_appels_modules skrull_menace` OK et `verifier_api_cartes` sans faute sur le pack, les deux CALIBRES le 15/10/2026 par un module piege (3 fautes plantees, toutes vues) ; `verifier_coherence_cartes` 31/31 couvertes ; `verifier_prefixes` sans defaut sur `sk`.
- **Etape 8 bis (plateau)** : `ui-app/src/board/skrull-menace-hulkling.test.ts`, 7 cas batis sur un descripteur CAPTURE (sonde_campagne sur `.game-src`, 15/10/2026), vus ROUGES sur un etat casse puis VERTS. Node 22.20.0 installe dans ~/.local le 15/10/2026 pour cela.

### sk001a : Hulkling

- [x] Etape 2 : carte(s) de reference : `22001b` * Nebula (detail et justification en tete de `sk001a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « KREE **or** SKRULL »; « **from your hand** »; « if you **share that** trait »; « Limit once per **round** ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "13", "ATK": "2", "THW": "1", "DEF": "2", "HS": "5"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « Descendant of Both Races — carte SKRULL jouee en forme Skrull : pioche 1 » VERT; « Descendant — CONTRE-CAS : carte SKRULL jouee en forme KREE, aucune pioche » VERT; « Descendant — TEMOIN D'EPUISEMENT : deux cartes SKRULL le meme round, une seule pioche » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3. Cas restant VERT sans module (absence d'effet, assume) : « Descendant — CONTRE-CAS : carte SKRULL jouee en forme KREE, aucune pioche ».
- [x] Etape 7 bis : limite imprimee ? OUI (once per round) : cas « sk001a Descendant — TEMOIN D'EPUISEMENT », deux sk008 le meme round, main mesuree a 1 (2 sans limite) : VERT
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk001b : Teddy Altman

- [x] Etape 2 : carte(s) de reference : `as001b` * Peter Parker (Earth-31198), `26007` Density Control (detail et justification en tete de `sk001b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « After you change **origin** form »; « heal 1 damage from **Teddy Altman** »; « Skrull Origin side **faceup** ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "13", "REC": "4", "HS": "6"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « Setup — Skrull Origin arrive en jeu, face Skrull » VERT; « Kree/Skrull Hybrid — retourner l'origine en civil soigne 1 » VERT; « Hybrid — CONTRE-CAS : passer en heros n'est PAS changer d'origine, aucun soin » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3. Cas restant VERT sans module (absence d'effet, assume) : « Hybrid — CONTRE-CAS : passer en heros n'est PAS changer d'origine, aucun soin ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (met en jeu l'upgrade d'origine). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk002a : Skrull Origin

- [x] Etape 2 : carte(s) de reference : `17008` Jet Boots / `01017` Cosmic Flight, `65001a` * Wave (detail et justification en tete de `sk002a.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **Hulkling** gains »; « Origin form »; « **Action** »; « spend a card **with the KREE trait** »; « exhaust this card → »; « Permanent. ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Permanent": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « Skrull Origin — Hulkling a SKRULL et pas KREE » VERT; « Skrull Origin — CONTRE-CAS civil : Teddy Altman n'a ni SKRULL ni KREE » VERT; « Skrull Origin — l'Action retourne sur Kree Origin : Hulkling passe KREE » VERT; « Skrull Origin — depenser une carte KREE de la main fait piocher 1 » VERT; « Skrull Origin — CONTRE-CAS : la ressource d'Excelsior (KREE) en jeu ne fait PAS piocher » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/5. Cas restant VERT sans module (absence d'effet, assume) : « Skrull Origin — CONTRE-CAS civil : Teddy Altman n'a ni SKRULL ni KREE »; « Skrull Origin — CONTRE-CAS : la ressource d'Excelsior (KREE) en jeu ne fait PAS piocher ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (retourne l'upgrade). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk002b : Kree Origin

- [x] Etape 2 : carte(s) de reference : `17008` Jet Boots / `01017` Cosmic Flight, `65001a` * Wave (detail et justification en tete de `sk002b.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **Hulkling** gains »; « Origin form »; « **Action** »; « spend a card **with the SKRULL trait** »; « exhaust this card → »; « Permanent. ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Permanent": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Kree Origin — Hulkling a KREE ; depenser une carte SKRULL fait piocher 1 » VERT; « Kree Origin — Hulkling a KREE et pas SKRULL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (retourne l'upgrade). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk003 : Wiccan

- [x] Etape 2 : carte(s) de reference : `cn002` * Belit (pack conan, MEME auteur Kajislav) (detail et justification en tete de `sk003.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « While **you** have »; « 2* / 1* ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "HP": "3", "THW": "2*", "ATK": "1*", "RES": "B"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « Wiccan — forme Skrull : +1 THW, pas d'ATK en plus » VERT; « Wiccan — l'origine retournee en Kree : le bonus passe a l'ATK » VERT; « Wiccan — CONTRE-CAS civil : aucun bonus » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3. Cas restant VERT sans module (absence d'effet, assume) : « Wiccan — CONTRE-CAS civil : aucun bonus ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk004 : Kree Durability

- [x] Etape 2 : carte(s) de reference : `13033` Perseverance (detail et justification en tete de `sk004.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « After you change **form** »; « **Hero** Response »; « ready Hulkling **and** give him a tough ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "R"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Kree Durability — apres passage en heros : Hulkling redresse et Tough » VERT; « Kree Durability — aussi apres un changement d'ORIGINE (livret p. 4) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (statut Tenace). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk005 : Kree Ferocity

- [x] Etape 2 : carte(s) de reference : `56017` Savage Strike / `ah011` Kinetic Stomp, `10003` Hulk Smash / `32007` Made of Rage, `32008` Steel Fist (detail et justification en tete de `sk005.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **basic** attack »; « +6 ATK »; « You **may** take 2 **indirect** damage → ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "R"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Kree Ferocity — attaque de base +6, 2 indirects acceptes : 8 a Rhino » VERT; « Kree Ferocity — CONTRE-CAS : 2 indirects refuses, aucun degat a Hulkling, 8 quand meme » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk006 : Shift and Strike

- [x] Etape 2 : carte(s) de reference : `13014` Surprise Attack (detail et justification en tete de `sk006.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « After you change **form** »; « If you have SKRULL... If you have KREE... »; « confuse / stun **that** enemy »; « (attack) ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "R"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Shift and Strike — passer en heros (origine Skrull) : 4 degats et Rhino desoriente » VERT; « Shift and Strike — origine retournee en Kree : Rhino etourdi, pas desoriente » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (statuts Sonne/Desoriente). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk007 : Skrull Infiltration

- [x] Etape 2 : carte(s) de reference : `rs008` Savage She-Devil (pack red_sonja), `90119` Search and Rescue, `32008` Steel Fist (detail et justification en tete de `sk007.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « You **may** take 2 **indirect** damage → »; « a scheme »; « (thwart) ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "B"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « Skrull Infiltration — 4 menaces retirees du complot principal » VERT; « Skrull Infiltration — sous Crise, payer 2 indirects : le complot perd 4 menaces » VERT; « Skrull Infiltration — CONTRE-CAS sous Crise, refuser de payer : rien ne bouge » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3. Cas restant VERT sans module (absence d'effet, assume) : « Skrull Infiltration — CONTRE-CAS sous Crise, refuser de payer : rien ne bouge ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk008 : Skrull Regeneration

- [x] Etape 2 : carte(s) de reference : `yd006` Twirlin' and Whirlin' / `14006` Speed Cyclone (detail et justification en tete de `sk008.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **for each** resource you **overpaid** »; « Ready Hulkling »; « **Hero** Action ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "Y"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Skrull Regeneration — redresse Hulkling et soigne 2 par ressource surpayee » VERT; « Skrull Regeneration — CONTRE-CAS sans surpaiement : redresse, aucun soin » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk009 : Alliance

- [x] Etape 2 : carte(s) de reference : `18010` * Gamora's Sword (detail et justification en tete de `sk009.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « from your hand »; « **the main** scheme »; « an enemy ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "RES": "Y"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Alliance — jouer une carte KREE de la main : 1 degat a un ennemi » VERT; « Alliance — jouer une carte SKRULL de la main : 1 menace en moins sur le principal » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk010 : Ancestors

- [x] Etape 2 : carte(s) de reference : `22034` Defensive Training, `im004` Take Flight (detail et justification en tete de `sk010.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « individual counters »; « in your hand **or in play** »; « the KREE **or** SKRULL trait »; « until the end of the **round** »; « Action ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "G", "Uses": "2,individual"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « Ancestors — donner KREE a Hulkling (Skrull) : il a les DEUX traits » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (compteurs individual + trait). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk011 : Changeling

- [x] Etape 2 : carte(s) de reference : `47018` * Synch (detail et justification en tete de `sk011.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **Hulkling** gains »; « a basic power »; « exhaust Changeling → ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "R"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « Changeling — Hulkling AERIAL ; une contre de base gagne +1 » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk012 : Emperor Dorrek-Vell

- [x] Etape 2 : carte(s) de reference : `as012` Night Vision (pack armored_spidey, meme auteur) (detail et justification en tete de `sk012.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « While **you** have »; « **each ally you control** ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "B"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Emperor Dorrek-Vell — origine Skrull : chaque allie +1 THW » VERT; « Dorrek-Vell — origine retournee Kree : le bonus passe a l'ATK » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk013 : Excelsior

- [x] Etape 2 : carte(s) de reference : `41002b` Psi-Katana (detail et justification en tete de `sk013.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Restricted »; « **While Excelsior is ready** »; « **Hulkling's** basic attacks »; « **Resource** ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "RES": "Y", "Restricted": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « Excelsior — pret : l'attaque de base de Hulkling est percante (Tough ignore) » VERT; « Excelsior — CONTRE-CAS incline : plus de percant, le Tough absorbe » VERT; « Excelsior — Resource : s'incline pour payer une carte » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3. Cas restant VERT sans module (absence d'effet, assume) : « Excelsior — CONTRE-CAS incline : plus de percant, le Tough absorbe ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk014 : Nega Rings

- [x] Etape 2 : carte(s) de reference : `40037b` * Neena Thurman (detail et justification en tete de `sk014.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **swap** »; « a card **of your choice** in your discard pile »; « spend a [energy] resource »; « **Hero** Action ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "Y"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « Nega Rings — echanger une carte de la main avec une de la defausse » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (echange une carte main <-> defausse). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk015 : Lauri-Ell

- [x] Etape 2 : carte(s) de reference : `27080` Lashing Out (via `AfterVenomTakesAttackDamageRemoveEqualThreat`,
#    sm/venom/__init__.py) (detail et justification en tete de `sk015.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **from an attack** »; « any amount »; « give **her** ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "4", "HP": "3", "THW": "0*", "ATK": "3*", "RES": "R"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Lauri-Ell — blessee par une attaque : elle recoit un Tough » VERT; « Lauri-Ell — CONTRE-CAS : degats hors attaque (Puzzle.Damage), pas de Tough » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2. Cas restant VERT sans module (absence d'effet, assume) : « Lauri-Ell — CONTRE-CAS : degats hors attaque (Puzzle.Damage), pas de Tough ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (statut Tenace). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk016 : Mur-G'nn

- [x] Etape 2 : carte(s) de reference : `09004` Magic Blast / `01050` * Hulk, `22012` * Wraith (detail et justification en tete de `sk016.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « printed resource **has** »; « Ready a card **you control** »; « **an identity** »; « Action ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "HP": "2", "THW": "2*", "ATK": "2*", "RES": "B"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « Mur-G'nn — carte [physical] defaussee : redresse une carte que tu controles » VERT; « Mur-G'nn — carte [mental] defaussee : soigne 3 » VERT; « Mur-G'nn — CONTRE-CAS carte WILD defaussee : aucun effet (decision du 15/10) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (statut Tenace possible). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk019 : Provoked!

- [x] Etape 2 : carte(s) de reference : `09020` Unflappable (detail et justification en tete de `sk019.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « After **you** defend »; « take **at least 1** damage »; « **Hero** Response »; « ready **your hero** ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "0", "RES": "R"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Provoked! — defendre et encaisser au moins 1 : le heros se redresse » VERT; « Provoked! — CONTRE-CAS : defendre sans degat (Rhino ATK 2 = DEF 2), carte gardee » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2. Cas restant VERT sans module (absence d'effet, assume) : « Provoked! — CONTRE-CAS : defendre sans degat (Rhino ATK 2 = DEF 2), carte gardee ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk021 : Deflect the Blow

- [x] Etape 2 : carte(s) de reference : `50042` * EM Shield (detail et justification en tete de `sk021.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **Hero** Interrupt »; « discard ... **and** exhaust your hero »; « When **you** would take »; « all of that damage »; « (defense) ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "R"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « Deflect the Blow — attaque non defendue, heros pret : tout est previent, heros incline » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (se defausse). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk023 : Talos

- [x] Etape 2 : carte(s) de reference : `dt043` * The Thing, `53024` Wingman (detail et justification en tete de `sk023.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **consequential** damage »; « **another** character **you control** »; « deal **that** damage »; « Interrupt ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "3", "HP": "3", "THW": "1*", "ATK": "3**", "RES": "R"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « Talos — ses degats consecutifs vont a un autre personnage (l'identite) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk024 : Drunk in Love

- [x] Etape 2 : carte(s) de reference : `32008` Steel Fist pour `Faces.GiveStatus(cibles, "Confused", effect)`,
#    et `SetTarget(..., canbe_status=[...])` qui ne retient que les cibles
#    capables de recevoir le statut.
#  - `47012` / `ab012` pour `HealthUnits(...)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) (detail et justification en tete de `sk024.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Confuse your identity **→** »; « heal 4 damage from **it** »; « Action ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "B"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « Drunk in Love — desoriente l'identite puis la soigne de 4 » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (statut Desoriente). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk025 : Strength in Otherness

- [x] Etape 2 : carte(s) de reference : `22022` Daughters of Thanos / `12020` Swarm Tactics (detail et justification en tete de `sk025.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **for each** different card type »; « **the main** scheme »; « Team-Up (Hulkling **and** Wiccan) »; « Max 1 per deck ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "G", "TeamUp": "Hulkling;Wiccan", "MaxPerDeck": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 1/1 cas verts : « Strength in Otherness — 3 types en defausse : 3 menaces et 3 degats » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk029 : Glorious Flight

- [x] Etape 2 : carte(s) de reference : `47018` * Synch, `52001a` * Silk (detail et justification en tete de `sk029.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Play only if **you** have AERIAL »; « an **enemy** or a **side scheme** »; « **you** defeat »; « discard Glorious Flight → »; « **Hero** Response ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "1", "RES": "Y"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Glorious Flight — vaincre un ennemi : defausser la carte, le heros se redresse » VERT; « Glorious Flight — CONTRE-CAS : injouable sans le trait AERIAL » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (se defausse). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk030 : Pride

- [x] Etape 2 : carte(s) de reference : `09004` Magic Blast / `01050` Hulk, `26007` Density Control (detail et justification en tete de `sk030.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **identity-specific** card »; « add **it** to your hand »; « Max 1 per player »; « Action ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Cost": "2", "RES": "G", "MaxPerUnit": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Pride — carte signature au-dessus du deck : elle va en main » VERT; « Pride — CONTRE-CAS carte non signature : elle reste defaussee » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (defausse -> main). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk031 : Interracial Hatred

- [x] Etape 2 : carte(s) de reference : `40160` Manufactured Drama (detail et justification en tete de `sk031.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « KREE **and** SKRULL »; « you control »; « Exhaust **Teddy Altman** → »; « **discard** this obligation ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1", "GiveTo": "Teddy Altman"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « Interracial Hatred — en jeu, Hulkling (Skrull) ne peut pas se redresser » VERT; « Interracial Hatred — CONTRE-CAS : Teddy Altman (HYBRID) se redresse » VERT; « Interracial Hatred — Action d'alter-ego : incliner Teddy defausse l'obligation » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3. Cas restant VERT sans module (absence d'effet, assume) : « Interracial Hatred — CONTRE-CAS : Teddy Altman (HYBRID) se redresse ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (obligation en jeu). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk032 : Empress R'Klll

- [x] Etape 2 : carte(s) de reference : `39014b` * Spiral, `41002b` Psi-Katana / `13008` (detail et justification en tete de `sk032.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « each player **in hero form** »; « Villainous ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"HP": "4", "SCH": "2", "ATK": "1*", "Boost": "2", "Villainous": "1", "Nemesis": "Teddy Altman"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Empress R'Klll — revelee en forme heros : attaque percante (Tough ignore) » VERT; « Empress R'Klll — CONTRE-CAS revelee en civil : aucune attaque » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 1/2. Cas restant VERT sans module (absence d'effet, assume) : « Empress R'Klll — CONTRE-CAS revelee en civil : aucune attaque ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (sbire en jeu). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk033 : DNA Masking

- [x] Etape 2 : carte(s) de reference : `60131` (fne, The Getaway), `31030` Grand Larceny (detail et justification en tete de `sk033.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « **Minions** cannot take damage »; « while there are **no** minions in play ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"StartingThreat": "3*", "Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « DNA Masking — les sbires ne peuvent pas subir de degats » VERT; « DNA Masking — sans sbire en jeu, sa menace ne baisse pas » VERT; « DNA Masking — AVEC un sbire en jeu, la menace baisse » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/3. Cas restant VERT sans module (absence d'effet, assume) : « DNA Masking — AVEC un sbire en jeu, la menace baisse ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (complot annexe en jeu). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk034 : Inhibited

- [x] Etape 2 : carte(s) de reference : `21158` Frozen, `36030` Claustrophobia, `56029b` Teddy Altman (officiel) (detail et justification en tete de `sk034.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « change **form** »; « share **a** TRAIT »; « Action »; « Spend [physical][physical] »; « Attach to **your** identity ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 5/5 cas verts : « Inhibited — attachee : l'origine ne peut plus etre retournee » VERT; « Inhibited — attachee : passer en civil est refuse aussi » VERT; « Inhibited — Action : payer [physical][physical] la defausse » VERT; « Inhibited — une carte qui partage un trait (Alliance, SKRULL) ne peut pas etre jouee » VERT; « Inhibited — CONTRE-CAS : une carte sans trait commun (Drunk in Love) se joue » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 4/5. Cas restant VERT sans module (absence d'effet, assume) : « Inhibited — CONTRE-CAS : une carte sans trait commun (Drunk in Love) se joue ».
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? OUI (attachement sur l'identite). Cas plateau : `ui-app/src/board/skrull-menace-hulkling.test.ts` (etat CAPTURE sur le moteur), vu ROUGE sur un etat casse (6/7 rouges, le 7e non casse), puis VERT.
      Resultat : conforme.

Carte terminée : OUI

### sk035 : Assailed by Their Own

- [x] Etape 2 : carte(s) de reference : `36030` Claustrophobia / `39014b` (detail et justification en tete de `sk035.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a character **in play** »; « Take X damage »; « Choose »; « **Otherwise** ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "2"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 3/3 cas verts : « Assailed by Their Own — revelee en civil : l'identite s'incline » VERT; « Assailed — revelee en heros avec Wiccan (AVENGER) en jeu : degats = ATK de Wiccan » VERT; « Assailed — revelee en heros SANS candidat : l'identite s'incline (otherwise) » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

### sk036 : Swapping Roles

- [x] Etape 2 : carte(s) de reference : `mf016` / `27080` Lashing Out (detail et justification en tete de `sk036.py`).
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « each card **you control** »; « shares **a** TRAIT with your identity ».
      Resultat : conforme (texte imprime relu phrase par phrase contre le module).
- [x] Etape 6 : nombres texte ↔ desc ↔ code : {"Boost": "1"} ; relu sur le scan. Resultat : conforme.
- [x] Etape 7 : 2/2 cas verts : « Swapping Roles — revelee : identite ET cartes partageant un trait s'inclinent » VERT; « Swapping Roles — Boost : les cartes partageant un trait s'inclinent, PAS l'identite » VERT.
      Substitution (`substituer_pack.py`, empreinte du pack identique avant/apres) : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir rappel commun (0 traceback, 0 partie bloquee).
- [x] Etape 8 bis : change ce qu'on voit ? NON (chiffres seulement : degats, menace, pioche, ressources, bonus de stats).

Carte terminée : OUI

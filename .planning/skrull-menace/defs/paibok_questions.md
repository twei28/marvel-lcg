# Paibok (sk141-160) et New Revengers (sk161-169) — questions ouvertes pour l'utilisateur

Format : card_id, phrase imprimee, lectures possibles, lecture RETENUE (implementee), chemin de l'image.
Images : `~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav/Scenario Packs/Paibok (Skrull Menace Expansion Content)/`
(`<dossier>` ci-dessous) et `Modular Sets/New Revengers (Skrull Menace Expansion Content)/` (`<NR>`).

## 1. sk146 Captain Paibok — l'icone du milieu de la boite de texte
- Phrase : aucune ; une icone noire (croix evidee sur une carte penchee, RIEN dessous) est imprimee entre « Attach to Paibok. »
  et « Hero Action ». La transcription l'appelait « icone de heros ».
- Lectures : (a) icone HAZARD (une carte a jouer penchee portant une croix, sans rien dessous : forme exacte de l'icone de
  `sk100` Emperor's Throne, voir `docs/reference/mots-cles/hazard.md`) ; (b) simple decor.
- RETENU : (a), `desc.Hazard = "1"` sur sk146. Effet : tant que Captain Paibok est en jeu, la phase du mechant distribue une
  carte rencontre de plus (Aleas). Verifie par un cas (`icones: Hazard 1`).
- Image : `<dossier>/Encounter cards/06 captain Paibok.png`. A confirmer par l'utilisateur (si c'est du decor, supprimer la
  cle `Hazard` de la carte dans `defs/paibok_cards.py` et relancer `defs/inserer_paibok.py`).

## 2. sk147 Distracted / sk153 Trapped in Ice — « When you thwart / attack » et les EVENEMENTS
- Phrases : « Forced Interrupt: When you thwart, reduce the amount of threat that thwart removes by 1. » /
  « Forced Interrupt: When you attack, reduce the amount of damage that attacks deals by 1. » (« attacks deals » : coquille imprimee, laissee.)
- Lectures : (a) seulement le pouvoir de BASE du heros (contrer / attaquer) ; (b) aussi les evenements « (thwart) » / « (attack) ».
- RETENU : (b), via la fenetre moteur `WhenUnitWouldThwart` / `WhenUnitWouldAttack` du heros (identite attachee). MESURE : les deux
  evenements testes passent bien par ces messages (Swinging Web Kick 8 -> 7 degats ; Crisis Interdiction 2 -> 1 menace), cas de la batterie.
  Un evenement qui retirerait de la menace / infligerait des degats SANS passer par ces messages ne serait pas reduit (non rencontre).
- Image : `<dossier>/Encounter cards/07 distracted.png`, `15 trapped in ice.png`.

## 3. sk146 Captain Paibok — « Hero Action: Resolve ... → discard this card »
- Lectures : (a) le « → » separe COUT (resoudre les Boost) et EFFET (defausser) ; (b) tout est l'effet.
- RETENU : (a) (comme tout « Hero Action: X → Y » du jeu). Consequence : resoudre les Boost est paye MEME si la defausse est
  empechee ; ici Captain Paibok n'est pas un POWER SKRULL, rien ne l'empeche. Les Boost se resolvent dans l'ordre choisi par le
  joueur qui agit (`ChooseOrder`, pas de question s'il n'y en a qu'un), Captain Paibok lui-meme compris (il soigne 2 a Paibok).
- Image : `<dossier>/Encounter cards/06 captain Paibok.png`.

## 4. sk155 General Kalamari — « The player who defeated General Kalamari »
- Cas non prevu : Kalamari vaincu sans joueur responsable (degats d'un effet, Riposte d'un autre ennemi...).
- RETENU : repli sur le PREMIER joueur. Image : `<dossier>/Encounter cards/18 general Kalamari.png`.

## 5. sk157 Settling Scores — « each boost card 1 additional time »
- Lectures : (a) tout Boost de toute carte de boost retournee, quelle que soit l'activation (vilain, sbire) ; (b) seulement celles du set Paibok.
- RETENU : (a) (le texte dit « each boost card », sans restriction de set ; le texte des autres cartes dit « of the Paibok set »
  quand il le veut). Le Boost est rejoue avec le message d'origine (il voit l'attaque ou la manigance en cours) ; un Boost annule n'est pas rejoue.
- Image : `<dossier>/Encounter cards/20 settling scores.png`.

## 6. sk145b — la boucle du complot « Mastering Superpowers »
- Constat de lecture (pas un doute) : 2B ne s'accomplit jamais (« remove all threat from here instead »), il n'y a pas de stade 3 :
  les joueurs gagnent en vainquant Paibok (stade II, ou III en expert) ou perdent par les quatre POWER SKRULL. Chaque tour de
  complot ajoute un jeton de maitrise et revele un POWER SKRULL (course entre defausser et maitriser).
- Image : `<dossier>/Setup cards/05 mastering supoerpowers IIB.png`.

## 7. sk163 Asti the All-Seeing — « Assign 2 indirect damage among players »
- Lecture retenue : le PREMIER joueur repartit les degats indirects entre les personnages de tous les joueurs (meme montage que
  `gmw 16085b` Museum Ship). Image : `<NR>/03 asti.png`.

## 8. Icones relues sur les scans (pas de doute, pour memoire)
- sk156 Galactic Ambassador et sk168 The Revenge Time : icone ACCELERATION (croix + pointe + barre) ; decision utilisateur du 15/10/2026 pour sk156.
- sk150 Ice Control : badge ATQ a etoile seule = « voir le texte » (decision utilisateur) : seul le +1 MNG est chiffre dans `desc`.
- Etoile rouge de boost = pas d'icone chiffree ; « Y » rose = 1 icone de boost (sk146 : etoile + 2 Y -> Boost 2).
- Icones de ressource des couts de defausse verifiees contre `sk044` (Lazerfist, [energy] = eclair) et `sk057` (Mister Fantastic, [mental] = noeuds)
  du MEME auteur : Distracted BB, Hypnotized YY, Trapped in Ice RR, Electricity Projection BR, Metallic Skin YB, Shapeshifting YR.

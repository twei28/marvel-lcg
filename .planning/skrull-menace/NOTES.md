# Skrull Menace (Kajislav) — notes d'intégration

Sources extraites (hors dépôt) : `~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav/`
Livret : `Campaigns/Skrull Menace (Released)/rulebook/rulebook 1.5.pdf` (24 p., images sans texte).
Cartes = PNG seulement : le texte de chaque carte reste à transcrire.

## Volume (images de cartes, hors couvertures/inserts)
- Cartes de campagne (n° 263-288) : 34 (alliés 7, side schemes joueur 7, supports 6, upgrades 6, ressource, etc.)
- Héros : Hulkling 37, Lyja 35
- Scénarios : Skrull Empire 50, Super-Skrull 29, Paibok 30, Skrull Pantheon 27, Secret Invasion 83
- Modular sets : ~83 (Army of Skrulls 8, Skrull Society 9, Dard'van Sect 8, New Revengers 10, Kree-Skrull War 6,
  Shaper of Worlds 6, 5 Skrull Elite x6, Standard/Expert Skrull 10)
- Total ≈ 410 images

## Moteur : état (vérifié par lecture du code)
- OUI : side schemes joueur + limite, victory display partagée, hinder/incite/patrol/steady/stalwart/teamup/temporary/
  villainous/piercing/ranged/amplify.
- PARTIEL : formes supplémentaires (liste en dur dans src/game/player/form/form.py) ; Shift/Strike inexistants
  (scripts par carte) ; helper « défausse le dessus du deck pour placer en victory display » à écrire.
- NON : « Cooperation Area ». Modèle le plus proche : hunting_season/campaign.py + gmw (clés du carnet + WhenCampaignSetup).

## Livret — campagne
- 5 scénarios dans l'ordre (tous à gagner). Identité fixe pour toute la campagne ; deck libre entre scénarios.
- Règle : quand un sbire/side scheme est vaincu, le joueur peut défausser le dessus de son deck pour le placer en
  victory display. Chaque carte du display coche UNE seule exigence du tableau Cooperation Progress.
- Cartes de campagne : n'entrent dans un deck que via la Cooperation Area ; rendues à la zone après chaque partie ;
  hors limite min/max du deck ; toutes aspects. Chaque joueur peut mélanger 1 carte de chaque type (allié, side scheme
  joueur, ressource, support, upgrade) de la zone dans son deck à la mise en place (scénarios 2-5).
- Skrull Elite (Crusader, Jazinda, Skymax, War Skrull, Xavin) : un tiré au hasard par scénario (1 à 4) ; si le sbire
  est en victory display -> set + sbire retirés de la campagne, + allié du même nom + side scheme joueur de l'aspect
  de l'allié ajoutés à la Cooperation Area ; sinon l'ensemble est remélangé dans le deck rencontre au scénario suivant.
- Suivi d'états entre scénarios : Shaper of Worlds (en jeu / mis de côté / autre zone) ; Cosmic Cube Creation
  (en jeu / victory display / autre zone / retiré) ; chaque Elite (inclus / victory display / autre zone).
  Si Cosmic Cube Creation en victory display : TOUTES les copies de Cosmic Cube Fragment vont dans la Cooperation Area.
- Expert : PV restants conservés par identité (plafonnés aux PV de base) ; soin par jeton d'accélération sur le
  complot principal ; un joueur éliminé revient au scénario suivant ; méchants (III) à la place des (I).
- Alt sets : Standard Skrull / Expert Skrull peuvent remplacer Standard / Expert.
- Victoire finale : Veranke vaincue au scénario 5.

## Livret — scénarios
1. Skrull Empire : méchants Dorrek I/II, Dorrek VII I/II, R'Klll I/II, S'Byll I/II (4 paquets méchant, un par stade,
   pile alternée) ; PV portés par l'environnement Skrull Empire ; paquet Planète de 9 environnements ; trahisons
   Overthrow mises de côté. Deck rencontre : Skrull Empire, Army of Skrulls, Skrull Society, Standard.
2. Super-Skrull : Super-Skrull I/II ; paquet Superpowers (4 attachements) ; Kree-Skrull War (side scheme Earth
   Involvement : permanent + setup). Ajoute Super-Skrull ally + Searching for Powers.
3. Paibok : Paibok I/II ; attachements Power Skrull (4), compteurs de maîtrise ; New Revengers. Ajoute Paibok ally +
   Skrull Military Training.
4. Skrull Pantheon : Kly'bn / Sl'gur't (carte double face, PV partagés), compteurs de foi ; Dard'van Sect, Skrull Society.
5. Secret Invasion : Veranke (double face Camouflaged/Revealed) ; paquet Impostor de 20 cartes double face ; Army of Skrulls.

## Livret — héros
- Hulkling / Protection : formes Skrull Origin / Kree Origin (hors limite 1 changement par tour), Shift, Strike, Changeling.
- Lyja / Agression : treacheries à infiltrer, Skrull Spy, Boost.
- Listes de decks : p.18 du livret.

## Plan (étapes)
1. [fait] Lecture du livret. 2. Transcription des cartes. 3. Hulkling + Lyja. 4. Skrull Empire. 5. Scénarios 2-5 + modular.
6. campagne : data/campagnes/skrull_menace.json + Cooperation Area + états + expert.
Chaque carte : docs/reference/PROCESSUS-CARTE.md ; héros : PROCESSUS-HEROS.md.

## Conventions de lecture validees par l'utilisateur (15/10/2026)
- Icones : Crisis = ! dans une explosion ; Acceleration = croix sur forme a pointe + barre ; Hazard = croix sur carte penchee nue ; Amplify = croix + avion (voir docs/reference/mots-cles/).
- Side scheme de joueur : coin haut droit (carte a l'endroit) = cout ; boite noire bas gauche = menace de depart.
- Complot principal face B : ovale haut gauche = objectif ; case bas droite : +N (haut) = escalade, nombre du bas = depart.
- Badge orange des allies de campagne = points de vie.
- Badge ATK/stat a etoile seule, ou etoile en exposant = renvoi aux effets etoile du texte, sans valeur chiffree.
- Skrull Empire : les mechants n'ont pas de PV ; l'environnement Skrull Empire (14/18/22 par joueur) les porte.

## Etat au 15/10/2026 (fin de journee)
- Hulkling : FAIT et commite (0c0d05cf). Testable en local (LANCEUR-LINUX.sh).
- Scenario 1 Skrull Empire (sk070-116) : scripts, donnees, textes FR, tests (72 cas [sk-e]), plateau, gabarits ecrits ; EN ATTENTE du commit (batterie complete relancee apres l'ajout de pv_sur_environnement dans villain.py).
- Decisions utilisateur : PV de l'environnement = vrai cadran ; **PAS de deploiement avant la fin des 5 scenarios ET de la campagne** (deployer.sh interdit d'ici la).
- Tout est fait (15-16/10/2026) : Lyja, scenarios 2-5, modulaires, 26 cartes de campagne, mode campagne (voir CAMPAGNE-MODE.md).
- Piege decouvert : un meme nom unique d'un stade a l'autre (« * Emperor Dorrek I ») -> retirer l'ancien AVANT de reveler le nouveau (FinDeStade).
- Dette hors perimetre : 4 cas Squirrel Girl rouges (sg006/007/009/013), anterieurs a Skrull Menace.

## Decisions utilisateur du 15/10/2026 (audit de l'inventaire, voir INVENTAIRE.md)
- Hors campagne IGNORE pour l'instant : heros Super-Skrull (Beta), heros Wiccan (1.1), cartes Veranke de Earth Under Siege.
- Etoile rouge a droite du numero de set des cartes 02-09 de Lyja = icone de boost ★ (l'effet « ★ Boost » s'applique quand la carte est retournee comme carte de boost ; elle compte comme ★ pour Ministerial Tiara et Hit the Weak Spot).
- Lectures faites par moi, non contestees : Galactic Ambassador = Acceleration ; Punish the Defector = Hazard ; Y rouge = icone de boost ordinaire ; Bel-Dann « alternative » = meme carte ; Pantheon = UNE carte double face a PV partages (la transcription disait deux mechants, c'est corrige).

## Decisions utilisateur du 15/10/2026 (suite : questions de Lyja)
- sk066 Paibok : « when a TREACHERY card would be discarded » = TOUTE defausse de traitrise, a la lettre (y compris un evenement TREACHERY de Lyja defausse de la main).
- sk040 Feign Loyalty : « attachment » = TOUTE carte attachee (attachements de rencontre ET ameliorations du joueur) ; implemente (lyja/__init__.py, cas dedie).

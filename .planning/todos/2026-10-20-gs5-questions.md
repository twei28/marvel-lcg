# Galactic Storm, lot GS-5 (scénario 2 « Majestrix's Verdict », gs114-gs137) : questions pour l'utilisateur (20/10/2026)

Une question par carte ou par point, recommandation en premier, ce que chaque option change en jeu. La lecture
recommandée est celle qui est codée aujourd'hui ; rien d'autre n'a été tranché en silence. Scans : copies réduites
dans `Fusion/marvel-lcg-src/assets/pics/<card_id>.png` (dépôt principal), originaux dans
`sauvegardes-serveur/scans-originaux/<card_id>.png`.

## Décisions déjà prises (GS-0, 20/10/2026), appliquées dans ce lot : closes

- **Q4 « Forces Response »** : coquille, traitée comme « Forced Response ». Aucune carte de ce scénario ne la porte.
- **Q5 nom imprimé** : le nom imprimé fait foi (aucun écart nom de fichier / nom imprimé dans ce scénario).
- **Q6 conventions** : « ★ » devant Forced interrupt / Forced Response / Boost et en exposant d'une statistique =
  renvoi au texte (Deathbird I-III, 1B, 2B, Javelin, Korvus, Corsair, Hepzibah) ; étoiles blanches à contour sous
  CTR/ATQ d'un allié = dégâts consécutifs (une `*` par étoile : Ch'od et Korvus « ATK 3** ») ; pastille orange à
  chiffre = points de vie (alliés et sbires). Appliqué tel quel.
- **Q7 livret 1.2 partout** : règles « Chandilar Prison » et FAQ du scénario 2 lues dans le livret 1.2 et l'insert.
- **Q9 Imperial Guard** : retrait des cartes non-traîtrises après victoire aux scénarios 1 et 2 seulement. Le
  scénario 2 EST concerné, mais c'est une instruction de CAMPAGNE (lot GS-9) : rien à coder ici, noté pour GS-9.
- **Q10** : rien inventé là où le livret est vide ; les points ouverts sont ci-dessous.

## Q1. Ensemble modulaire du scénario joué seul (Imperial Guard pas encore porté)

Le livret et 1A demandent « One modular encounter set (Imperial Guard) ». Imperial Guard appartient au lot GS-4,
pas encore porté : sans module, le scénario ne se lance pas hors campagne.
1. **(Recommandé) Kree Militants (officiel, thème guerre Kree-Shi'ar) en attendant, remplacé par Imperial Guard
   dès que GS-4 est fusionné** (une ligne `MODULAIRE` dans `.planning/galactic-storm/defs/inserer_majestrix.py`).
   Change en jeu : 4 à 6 cartes Kree au lieu des 9 cartes tirées de la Garde impériale ; la difficulté reste proche.
2. Aucun modulaire : paquet rencontre plus court (Majestrix's Verdict + Standard), scénario plus facile.
3. Un autre modulaire officiel (préciser lequel).
4. Autre (préciser).

## Q2. gs136 Exemplar Punishment : « place 2 threat on it »

Texte : « For each STARJAMMER ally tucked under Imprisoned on Chandilar choose to either take 1 indirect damage or
place 1 threat on the main scheme. If there is no ally tucked under Imprisoned on Chandilar, place 2 threat on it. »
Scan : `gs136.png`.
1. **(Recommandé) « it » = Imprisoned on Chandilar** (nom le plus proche dans la phrase). Change en jeu : sans
   prisonnier, la prison remonte de 2 et la libération suivante est plus lente.
2. « it » = la manigance principale (suite logique de la première phrase). Change en jeu : sans prisonnier, la
   manigance principale avance de 2, ce qui rapproche l'exécution suivante (2A).
3. Autre (préciser).

## Q3. gs119 Imprisoned on Chandilar : « place 6 threat here » quand plus personne n'est glissé

Texte : « When the last threat is removed from here, the players as a group choose a STARJAMMER ally tucked under
here, put that ally into play under any player's control and place 6 threat here. » En solo il reste toujours au
moins deux STARJAMMER en prison (limite de 3 alliés, Lilandra hors compte) ; à plusieurs joueurs, la prison peut
se vider. Scan : `gs119.png`.
1. **(Recommandé) Les 6 menaces reviennent même sans allié à libérer** (la manigance, Permanente, ne peut pas
   rester à 0). Change en jeu : la prison reste une manigance « vivante » qui accumule la menace des cartes.
2. Rien ne se passe s'il n'y a plus d'allié glissé : la prison reste à 0 (et chaque nouvelle menace posée dessus
   peut être retirée pour rien). Change en jeu : plus aucune pression de la prison une fois vidée.
3. Autre (préciser).

## Q4. gs127 / gs128 / gs129 : qui peut payer la Réponse « spend a [x] resource → attach this card to Lilandra » ?

Texte (trois attachements) : « Response: After Lilandra attacks Deathbird, spend a [energy|mental|physical]
resource → attach this card to Lilandra. » Aucun « you » dans la phrase ; la question ne se pose qu'à plusieurs.
1. **(Recommandé) N'importe quel joueur** (carte de rencontre, comme `32173b` Rescue Captives). Change en jeu : un
   coéquipier peut payer la ressource pour le joueur qui contrôle Lilandra.
2. Seulement le joueur qui contrôle Lilandra. Change en jeu : il doit avoir la ressource lui-même.
3. Autre (préciser).

## Points tranchés par nécessité (pas des questions, à relire)

- **gs118b, boucle 2B → 2A → 2B** : « flip this card and reveal it instead » ; 2A finit par « Advance to stage 2B ».
  Le moteur gardait les menaces d'une carte retournée : 2B revenait avec ses 5 menaces et était « accomplie » de
  nouveau à la première menace, boucle sans fin. Codé : le stade 2B qui recommence repart de sa menace de départ
  (0), comme tout stade qui commence.
- **Lilandra et le Trône** : la face soutien `gs120b` n'existe que via la défaite de la face manigance `gs120a`.
- **Starjammers basiques** (`Class: Campaign;Basic`) : ils n'apparaissent pas dans l'éditeur de deck hors campagne
  (cartes recrutées en campagne, comme Magneto `32172b`). Lilandra : `Class: Encounter`.

## Réponses de l'utilisateur (20/10/2026)

Principe : suivre les règles du jeu à 100 %, sauf si la carte ou la campagne dit le contraire.
- Q1 (modulaire du scénario seul) : « On attend de tout finir ». Aucun choix définitif maintenant : le module provisoire Kree Militants reste codé pour pouvoir lancer le scénario, et sera remplacé par Imperial Guard quand ce set (GS-4) sera porté (une ligne `MODULAIRE` dans `inserer_majestrix.py`).
- Q2 (gs136, « place 2 threat on it ») : « it » = Imprisoned on Chandilar (lecture codée).
- Q3 (gs119, les 6 menaces sans allié à libérer) : décidée par la règle (« faire ce qu'on peut » ; la manigance Permanente ne peut pas rester à 0) : les 6 menaces reviennent même sans allié (lecture codée).
- Q4 (gs127/128/129, qui paie la Réponse) : décidée par précédent officiel (`32173b` Rescue Captives, carte de rencontre sans « you ») : n'importe quel joueur (lecture codée).

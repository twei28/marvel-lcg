# Galactic Storm, lot GS-2 (heros Quasar) : questions pour l'utilisateur (20/10/2026)

Une question par carte, recommandation en premier, ce que chaque option change en jeu. Rien n'est tranche :
la lecture RECOMMANDEE est celle qui est codee en attendant la reponse (le dire suffit a la garder).
Contexte : `docs/packs/galactic-storm/transcriptions/quasar.md`, gabarits `.planning/galactic-storm/QUASAR-GABARITS.md`.

## Decisions deja prises (GS-0, 20/10/2026), appliquees dans ce lot : CLOSES

- Q1 numerotation : `gs` + (300 + n) du pied « QUASAR (n/16) », Quantum Bubble `gs349`, nemesis en collision avec
  Binary suffixees `q` (gs237q, gs239q, gs240q). Appliquee. Precisions techniques, sans effet en jeu : identite
  `gs300a`/`gs300b` (aucun n/16 imprime sur l'identite) ; une copie prend le PREMIER n/16 (Flight of Light 3/16 et
  4/16 -> `gs303` x2, decision c).
- Q2 porter toutes les images : fait (18 card_id, 19 reskins).
- Q3 un card_id par carte avec le nombre d'exemplaires : fait (deck de heros : 15 cartes, 10 card_id).
- Q4 « Forces Response » : sans objet pour Quasar (aucune carte du lot ne porte la coquille).
- Q5 nom imprime > nom de fichier : applique (« quantum enegry.png » = Quantum Energy).
- Q6 conventions : « ★ » devant une capacite = renvoi au texte (Epoch) ; etoiles creuses sous THW/ATK = degats
  consecutifs (Epoch 1* / 3***) ; pastille orange = PV (Epoch 4, Maelstrom 5). QUANTUM BANDS genere un JOKER
  [wild] au choix de celui qui paie : code ainsi (`Resources("G")`, couleur precisee par `AskSpecifyResources`
  quand une carte la lit, ex. No Holding Back ; conforme a la FAQ p.22).
- Q7 livret 1.2 partout : applique (FAQ p.22 de Quasar suivie, voir gs305 / gs315).
- Q10 ne rien inventer la ou le livret est vide : aucune FAQ manquante ne touche Quasar.

## Q-GS2-1. gs099q Maelstrom : son numero imprime 99 est AUSSI celui de Hobgoblin (Imperial Guard)

Image : `MC custom content by Kajislav/Hero Packs/Quasar (Galactic Storm expansion content)/Encounter cards/44 Maelstrom nemesis.png`
(pied « Kajislav 99 ») ; Hobgoblin : `Modular Sets/Imperial Guard/09 hobgoblin.png` (INVENTAIRE n° 270).
La regle « gs + numero imprime » donne `gs099` aux deux.
1. **(Recommande) Maelstrom = `gs099q`** (suffixe q comme les trois autres nemesis de Quasar en collision),
   Hobgoblin garde `gs099`. Change en jeu : rien ; c'est ce qui est code.
2. Maelstrom = `gs099`, Hobgoblin suffixe (`gs099i`) : il faudra renommer ici avant la fusion.
3. Autre (precisez).

## Q-GS2-2. gs240q Distant Manipulation : « each card with a "Resource" ability you control »

Image : `.../Encounter cards/47 distant manipulation.png`.
1. **(Recommande) Toute carte EN JEU que vous controlez portant une capacite Resource, y compris « Hero Resource » et
   « Alter-Ego Resource », identite comprise.** Change en jeu : Quantum Bands (Hero Resource) s'incline ; une
   identite a capacite Ressource (Peter Parker 01001b, « Scientist — Resource ») s'incline aussi. C'est ce qui
   est code (le moteur classe Hero/Alter-Ego Resource comme des Resource).
2. Seulement les capacites marquees exactement « Resource » (pas Hero/Alter-Ego Resource) : les Bandes de Quasar
   echappent a la carte, ce qui semble contraire a son intention (la nemesis de Quasar).
3. Sans l'identite : seuls les allies / ameliorations / soutiens s'inclinent.
4. Autre (precisez).

## Q-GS2-3. gs239q Entropy Ascendant : « Each event card gains requirement ([energy]) » sur un evenement a 0

Image : `.../Encounter cards/45 Entropy Ascendant.png` (carte pivotee).
Exigence = « en payant cette carte, depensez les ressources indiquees » (pas un cout en plus : un evenement a 2 coute
toujours 2, dont une [energy]).
1. **(Recommande) Un evenement a 0 doit quand meme depenser une [energy]** (il coute alors 1). C'est ce qui est code.
   Change en jeu : les evenements gratuits deviennent payants tant que la manigance est en jeu.
2. Un evenement a 0 reste gratuit (l'exigence ne porte que sur une carte qu'on paie).
3. Autre (precisez).

## Q-GS2-4. gs349 Quantum Bubble : « After you pay for an ally with Quantum Bands, give that ally a tough status card »

Image : `.../Hero cards/14 Quantum Bubble.png`.
Une carte d'etat ne se pose que sur un personnage en jeu ; « apres avoir paye », l'allie n'est pas encore en jeu.
1. **(Recommande) La Reponse se resout des que l'allie paye est entre en jeu** (fenetre « apres avoir joue »).
   C'est ce qui est code. Change en jeu : rien de visible, sauf si l'entree en jeu est annulee (pas de Tenace).
2. Autre (precisez).

## Q-GS2-5. Arts alternatifs de Quasar : affiches PAR DEFAUT pour le joueur Quasar ?

Les 19 « Starter deck's reskins » sont branches en arts alternatifs (code « quasar », 16 cartes + la collection de
ressources « Quasar » pour Energy / Genius / Strength).
1. **(Recommande) Oui pour les 16 cartes** (serie « quasar » de `data/arts_alternatifs.json`, meme mecanisme que la
   serie TMNT pour un heros TMNT) ; les ressources restent « Standard » sauf choix du joueur (la collection par
   defaut n'existe que pour TMNT dans le code). C'est ce qui est fait. Change : un joueur Quasar voit les dessins de
   Kajislav sans rien regler ; il peut revenir a l'officielle carte par carte.
2. Jamais par defaut (comme MCDC26) : retirer la serie, garder seulement le choix carte par carte.
3. Par defaut aussi pour les ressources (code a ajouter dans `collectionPourJoueur`).

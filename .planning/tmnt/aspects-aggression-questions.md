# Aspect TMNT Aggression (`ua`) : questions ouvertes

16/10/2026. Scans : `scratchpad/zip-aspect/TMNT Aspect/Aggression/<fichier>.png`. Une question par carte ;
option recommandée en premier. La carte concernée reste NON terminée tant que la réponse n'est pas rendue
(une lecture est codée en attendant : celle recommandée).

## Q-UA1 — ua019 Flow of Battle : que veut dire « Prerequisite (MARTIAL ARTIST) » ?

Scan : `Aggression/Flow of Battle.png`. Imprimé sans texte de rappel ; une seule officielle du dépôt le porte
(`61029` Defend Our City, « Prerequisite ([[Defender]]) »), et son script ne code rien pour ce mot.

1. **(recommandé, codé)** La carte ne peut être JOUÉE que si votre identité a le trait MARTIAL ARTIST
   (comme « Play only if your identity has the X trait »). En jeu : Spider-Man ne peut pas la poser ;
   Daredevil, si.
2. Contrainte de CONSTRUCTION de deck seulement : un deck dont le héros n'est pas MARTIAL ARTIST ne peut pas
   l'inclure, mais en partie rien ne l'empêche (le moteur ne contrôle pas ; le deck-builder ne l'exprime pas
   aujourd'hui).
3. Les deux (deck ET jeu).
4. Autre (précise).

## Q-UA2 — ua037 Slash : « After Slash enters play, take 3 damage » : qui subit les 3 dégâts ?

Scan : `Aggression/Slash.png` (Allié 2, PV 5, ATK 3, THW 0).

1. **(recommandé, codé)** VOUS : votre identité subit 3 dégâts (convention des cartes joueur : « take X
   damage » sans sujet = le joueur, comme Blood Rage ou Rampage). Slash reste à 5 PV.
2. Slash lui-même : il entre en jeu et descend à 2 PV (« take » au sens « Slash takes »).
3. Autre (précise).

## Q-UA3 — ua033 Pete : « After YOU deal damage to an enemy » : quelles sources comptent ?

Scan : `Aggression/Pete.png` (Soutien, Uses 3 pistol).

1. **(recommandé, codé)** Les dégâts infligés par votre IDENTITÉ (attaque de base, capacités du héros) —
   précédent moteur de l'officielle `16032` Schadenfreude (« each time you deal any amount of damage to an
   enemy », fabrique `AfterYouDealDamage` = source « YourIdentity »). Un événement d'attaque joué (Clobber)
   ou un allié ne déclenche PAS Pete.
2. Identité ET cartes que vous jouez/contrôlez hors alliés (événements, améliorations, soutiens) : Clobber
   déclenche Pete, un allié non.
3. Tout ce que vous contrôlez, alliés compris.
4. Autre (précise).

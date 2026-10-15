# Secret Invasion (sk189-227) — questions de regles pour l'utilisateur

Pour chaque point : la phrase, les lectures possibles, **celle retenue** (implementee), le chemin de l'image. Aucune question n'a ete posee
pendant le travail (consigne du brief) ; chaque lecture est facile a changer (un seul endroit, indique).
Images : `~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav/Scenario Packs/Secret Invasion (Skrull Menace Expansion Content)/`.

## Q1 — « After your turn ends » du complot 1B (sk192b) et 2B (sk193b) : pour QUEL joueur ?
- Phrase : « Forced Response: After your turn ends, if there are less than 2[per_hero] suspicion counters on "Who Do You Trust?", put a
  CAMOUFLAGED ally at random from the IMPOSTOR deck into play under your control. » (2B : un sbire REVEALED « engaged with you »).
- Lectures : (a) **a la fin du tour de CHAQUE joueur**, l'allie (ou le sbire) va a CE joueur ; (b) une fois par round, au premier joueur ;
  (c) a la fin du tour du premier joueur seulement.
- **Retenue : (a).** Une carte de rencontre dit « your turn » comme les Responses des attachements (`AfterPlayerTurnEnd`, modele gb022).
  Code : `secret_invasion/sk192b.py`, `sk193b.py`. Images : `setup cards/04 The Infiltration Has Begun IB.png`, `05 the skrull invasion IIB.png`.

## Q2 — Manigance de l'allie CAMOUFLAGED en phase du mechant (insert p. 16, `insert.png`)
- Phrase : « if the player's identity is in alter-ego form during the villain phase, the CAMOUFLAGED ally schemes at the same time as minions
  after the villain's activation. The CAMOUFLAGED ally takes consequential damage after it schemes but it does not exhaust. »
- Points ouverts : (1) « at the same time as minions » : l'allie maniganche **juste apres l'activation du mechant contre ce joueur** (avant
  les sbires) ; le moteur n'a pas de boucle d'activation extensible, la lecture « le joueur choisit l'ordre parmi les sbires et l'allie » n'est pas
  rendue ; (2) l'allie ne recoit **aucune carte de boost** (ce n'est pas un ennemi, la regle n'en parle pas) ; (3) valeur = SCH de la carte, degat
  consequentiel = 1 (une pastille sous le SCH, identique sur les 20 cartes) ; (4) la manigance n'est pas une « activation » d'ennemi : les
  capacites « when an enemy schemes » ne la voient pas.
- **Retenue :** comme ci-dessus. Code : `secret_invasion/__init__.py` (`AllieImpostor`, `ManigancerAllie`).

## Q3 — Le badge orange des cartes Impostor est-il un cout ou des PV ?
- Aucune carte Impostor ne s'achete (elles sortent d'un paquet) et le badge est identique sur les deux faces. NOTES.md : « badge orange des
  allies de campagne = points de vie ». **Retenu : PV** (`HP` dans le desc : 2 a 4 selon la carte).

## Q4 — Le SCH de l'allie Impostor
- La classe Ally du moteur n'a pas de statistique SCH (cle `desc` refusee). Le SCH imprime etant le meme sur les deux faces (20 cartes
  verifiees), il est **lu sur la face sbire** (`SchAllie`). Les pastilles du SCH valent toutes 1 ; celles de l'ATQ (1 ou 2) sont codees dans
  la cle `ATK` du desc (« 2** » = 2 degats consequentiels).

## Q5 — « Flip Queen Veranke » alors que Veranke est CAMOUFLAGED (sk203 Camouflage, boost)
- Boost : « Flip Queen Veranke, after this activation ends ». **Retenu :** n'a d'effet que si la face visible est Queen Veranke (la carte la
  renvoie sur Spider-Woman) ; elle ne retourne JAMAIS Spider-Woman vers Queen Veranke. Meme lecture pour le « When Revealed (Queen Veranke) ».
  Autre lecture : « flip » = basculer la carte quelle que soit la face. Code : `sk203.py`. Image : `encounter cards/16 camouflaged.png`.

## Q6 — Mistrust and Paranoia (sk201)
- « Players cannot attack minions engaged with other players or defend against them. » **Retenu :** « players » = tout personnage qu'un
  joueur controle (heros ET allies, y compris les allies Impostor) ; le sbire d'un AUTRE joueur ne peut ni etre attaque ni etre defendu
  contre. « Cannot pay any card's or ability's costs as a group » : ferme le mot-cle Alliance (evenements), Coordinated Effort et le paiement
  en groupe de « You are a Skrull! » ; **Forces Combined (cd003) n'est pas touche** (c'est UN joueur qui paie avec ses deux mains).
  Code : `sk201.py`, `resources.py` (modification de moteur, voir `secret_invasion_moteur.md`).

## Q7 — « You are a Skrull! » : « Exhaust a hero »
- **Retenu :** quand le paiement en groupe est ouvert, N'IMPORTE QUEL heros (de n'importe quel joueur) peut etre incline, et les 1[per_hero]
  ressources viennent de toutes les mains ; sous Mistrust and Paranoia, seulement le heros du joueur qui agit, et ses propres ressources.
  Autre lecture : « a hero » = celui du joueur qui agit, seul le paiement des ressources etant en groupe.

## Q8 — « Who Do You Trust? » : « an equal amount »
- **Retenu :** Interruptions forcees AVANT l'evenement : la quantite de jetons est celle de la menace qui va etre posee ; pour la menace
  retiree, elle est bornee par la menace reellement presente ; on ne peut pas retirer plus de jetons qu'il n'y en a. Autre lecture :
  Reponses forcees, apres, avec la quantite effectivement placee/retiree.

## Q9 — Faute d'impression « Hagar » sur le sbire Ch'Gra (sk223b, carte n° 42)
- Le texte imprime dit « Heal all damage from Hagar and put him into play engaged with you » alors que le sbire s'appelle Ch'Gra (copie de la
  carte 43). **Retenu :** la carte se soigne elle-meme (aucun autre « Hagar » n'existe sur la carte) ; le texte anglais est garde TEL QU'IMPRIME,
  le texte francais dit « Hagar » aussi. Image : `impostor deck cards/42 spider-man impostor minion.png`.

## Q10 — « would leave play, flip him instead » : quels departs ?
- **Retenu :** TOUT depart (defaite, defausse, retour en main, retrait du jeu, exces de la limite d'allies). Un allie vaincu (PV a 0) se
  retourne donc avec tous ses PV (le « When Revealed » du sbire soigne tout). Le garde `en_retournement` evite la recursion.

## Q11 — Super-Skrull Enhancement sans sbire SKRULL : « choose a CAMOUFLAGED ally »
- **Retenu :** le joueur qui revele choisit parmi les allies CAMOUFLAGED de TOUS les joueurs ; l'allie est retourne D'ABORD (ses
  attachements partent) puis l'amelioration s'attache au sbire. « Otherwise » (aucun allie) : Renfort.

## Q12 — Escalade du complot 1B : « [star] Place 1 additional threat here for each SKRULL enemy... »
- **Retenu :** l'etoile du badge d'escalade renvoie a ce texte : la menace supplementaire s'ajoute A L'ESCALADE de la phase du complot principal
  (`WhenCalcThisSchemeEscalation`). Autre lecture : effet permanent separe (hors escalade). 2B : « +X », X = 2 x ennemis SKRULL, meme mecanisme.

## Q13 — Traits CAMOUFLAGED / REVEALED / IMPOSTOR en francais
- Laisses en anglais dans les textes (convention du brief : traits en anglais). Si l'utilisateur veut « CAMOUFLÉ / RÉVÉLÉ », c'est un
  ajout dans `tools/traits_fr_maison.json` et `ui-app/src/board/traits-fr.ts`.

## Q14 — Badges a etoile (renvoi au texte)
- Spider-Woman (3 stades) : ATQ a etoile ; Ssrov (sk219b) : SCH ET ATQ a etoile ; M'lanz, H'kurrek, Korya, Hagar : ATQ a etoile. Aucune valeur
  chiffree en plus (convention validee du 15/10/2026) : la ligne « [star] ... » du texte porte l'effet.

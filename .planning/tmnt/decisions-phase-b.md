# Décisions de l'utilisateur, phase B (TMNT)

Une ligne par réponse. Source : conversation du 15/10/2026.

- **Cloak (tl015, tl016, td005, + Michelangelo si concerné)** : « Cloak X » = poser la carte de statut « Cloaked » sur X.
  Définition trouvée dans le zip des ennemis : `TMNT Enemies /Shredder v3/Cloaked.png` (+1 : « prochaine attaque/menace/activation : +2 »,
  + 2 : « prochains dégâts : −2 », chaque phrase suivie de « défaussez cette carte de statut »).
  Lecture retenue : **un seul effet, le premier qui arrive**, puis la carte est défaussée.
- **Cartes jumelles (14/15)** : voir mémoire `tmnt-cartes-jumelles-panorama`.
- **Katana (tl011, tl012)** : **vrai octroi d'aptitude** (la 14 donne « Hero Resource » à tout katana en jeu). Risque de construction à tester en phase C.
- **Yo Ko Giri (tl006)** : retour en main si payée avec **au moins une ressource de chaque couleur** (énergie, mental, physique).
- **Iaijutsu (tl008)** : **crochet exact sur l'attaque** (modif moteur, partagée : à faire en phase C avec précaution, tests du moteur à relancer).
- **Brainwashed Betrayal (tl013)** : **lecture littérale** (bascule héros obligatoire + défausse d'un de ses alliés ; ne peut pas attaquer le vilain tant que l'obligation est en jeu, sbires attaquables ; 3 dégâts à n'importe quel allié, au choix).
- **Foot Patrol (tl014)** : si aucun sbire FOOT CLAN trouvé, **rien ne se passe**.
- **Inserts (règles d'arme, Sai, etc.)** : **ne rien créer**, les règles vivent dans les scripts (vaut pour les 4 tortues).
- **Leonardo Q8 (icônes de ressource)** : pas posée à l'utilisateur ; je les vérifie moi-même par découpe contre des cartes officielles en phase C.
- **Donatello td005 Improvised Tactics** : « Cloak two friendly characters » = poser le statut Cloaked (voir Cloak ci-dessus), plus de question.
- **Bō Tobu (td003)** : nom **« Bō Tobu » avec macron**, un seul card_id, image du 2/15.
- **Donatello's Shell (td012)** : **fidélité 100 %** exigée : « jouer, dépenser OU DÉFAUSSER comme si en main » doit être rendu en entier (étendre le moteur : coût « défausser de la main » doit accepter la carte glissée). Règle générale : pas d'approximation (voir mémoire fidelite-cartes-100-pour-cent).
- **Essaims td016/td017 (PV ★)** : par la même règle, PV = nombre de compteurs swarm, **suivis dynamiquement** (pas de mort « à la main »).
- **Extermination! (td014)** : nom corrigé (le scan dit « Extermination! », l'agent avait écrit « Exterminate! »). Traits **pluriels MOUSERS / FLYBORGS** conservés.
- **Michelangelo, I'm Here to Help (tm009/tm001b)** : au Setup, **fouille du deck** (la carte reste dans les 15, 12/15).
- **Michelangelo, tm009 pioche 3** : plus de question, l'insert tranche : forme héros obligatoire + « only the Michelangelo player » = propriétaire.
- **Michelangelo, Nunchuck (tm011/tm012)** : plus de question, l'insert dit « either NUNCHUCK (or both) » : vrai octroi à tous les Nunchuck, comme Leonardo/Katana.
- **Majime (tm006)** : X = **dégâts réellement subis** (le script écrit par l'agent utilise le nombre déclaré : À CORRIGER).
- **Booyakasha (tm001a)** : annexe vidée = **vaincue** ; **Crise bloque** le déplacement depuis la manigance principale (le script écrit ne bloque pas : À CORRIGER, vérifier `MoveThreat` du moteur).
- **Impulsive (tm004)** : **jouable sans WEAPON** (seul le coût doit être payable).
- **Sewer Problems (tm014)** : icône centrale = **Crise 1** (même glyphe que 01108 Crowd Control, vérifié par découpe).
- **Michelangelo « Hero Spin »** : une seule face héros, rien de plus (tm001a).
- **Rage de Raphael (tr002, tr010, etc.)** : plafond de 3 **seulement où il est imprimé** (Yaban Hito, Sai) ; Casey Jones et Gekido sans plafond (`PLAFOND_PARTOUT = False`, état actuel du code).
- **« Raphael » en forme civile (tr002, tr007, tr010)** : les effets visent **l'identité** (soin, dégâts, rage sur la carte d'identité même en alter-ego). Le code actuel fait l'inverse : À CORRIGER.
- **Encart Sai (tr011, tr012)** : **l'encart fait loi** : chaque usage d'une Sai = action d'attaque + 1 rage (max 3).
- **Out of Control (tr013)** : « vous » = **l'identité seulement** (alliés peuvent contrer/défendre).
- **Mutagen Bomb (tr014)** : icône = **Amplify 1** (même glyphe que 16054 Vendetta, vérifié par découpe) ; `desc.Amplify = "1"` ajouté dans cards.json, checksum recalculé.
- **Disarm (tr003)** : « attachment » = **attachements de rencontre seulement** (type Attachment), pas les améliorations posées sur un ennemi.
- **Td002 Metalhead** : pas de question, fidélité 100 % : l'interruption doit être offerte depuis la main et la Carapace ; à prouver en phase C, sinon passer par `SetPlay` + coût 0.
- **Rage de Raphael, plafond de 3 PARTOUT (16/10/2026, remplace la decision du 15/10)** : Raphael est limite a 3 compteurs de rage maximum, quelle que soit la source (Casey Jones et Gekido compris). `PLAFOND_PARTOUT = True`.

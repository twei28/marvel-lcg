# Skrull Pantheon (scénario 4 de Skrull Menace, Kajislav) et Dard'van Sect — gabarits PROCESSUS-CARTE

Pack `skrull_menace`, card_id sk170-sk183 (scénario Skrull Pantheon : méchant double face Kly'bn / Sl'gur't par stade, complots
principaux 1A/1B et 2A/2B, environnement double face Stronghold / Destroyed, attachements Blessed by, Nogor, complots annexes,
traîtrises) et sk184-sk188 (set modulaire Dard'van Sect : deux sbires, complot annexe, deux traîtrises). Fiches générées à partir des
résultats RÉELS (rapport test_capacites, sorties de substituer_pack.py, en-têtes des modules) par
`.planning/skrull-menace/defs/generer_gabarits_pantheon.py`.

Rappels communs à toutes les cartes :
- **Numérotation** relue sur les 25 scans (pied de carte) : 170A/B, 171A/B, 172A/B (Kly'bn / Sl'gur't I, II, III), 173A/B (Protect the Pantheon),
  174A/B (Slaying the False Gods), 175A/B (Skrull Pantheon), 176-183 (rencontre), 184-188 (Dard'van Sect). Chaque face d'une carte double
  face a son card_id (`sk170a` = face Kly'bn, `sk170b` = face Sl'gur't ; `sk175a` Stronghold, `sk175b` Destroyed).
- **Règles du scénario** (insert p.14, lu par le coordinateur) : une SEULE carte double face par stade (PV partagés, le stade suivant arrive du
  même côté), jetons de foi (compteur maison `faith`), « Flip the villain » = défausse des attachements, cartes d'état, cartes de boost et autres
  éléments associés SAUF jetons de foi et dégâts, puis « When Revealed » de la face d'arrivée. Aucune carte de campagne n'est portée.
- **Étape 6 (nombres)** : stats, PV (15/18/20 par joueur, étoile = « par joueur »), menaces (9*/6*/+1* puis 12*/0/+1*), icônes de boost (Y = 1, ★ = pas d'icône
  chiffrée), SCH/ATK, relus sur les SCANS (1500x2150, tous vus un par un) contre `data/cards.json` : conformes. Lectures corrigées par rapport à
  la transcription : l'icône noire « boîte avec un plus » de sk186 est l'icône **HAZARD** (méthode du glyphe `H` de ChampionsIcons.ttf, rendu à côté
  du scan) ; Nogor : SCH/ATK/PV portent une ★ (renvoi au texte) et gardent leurs chiffres imprimés 1/1/4 ; Dard'van Priest : ATK ★ = `0*`.
  Voir `defs/pantheon_questions.md`.
- **Étape 7 (tests)** : 98 cas `[pantheon]` dans `tools/cas/pantheon.py` (chargé par `tools/test_capacites.py`), **98/98 verts**. Chaque mesure part d'un
  plateau connu : deck rencontre vidé (`EmptyEncounterDeck`) puis monté par `CreateEncounterDeck`, main fixée par `main_exclusive`, forme héros
  (`ChangeForm('01001b')`) quand on mesure une phase du méchant, deux joueurs par `heros2`. Pièges payés pendant les tests (détail :
  `defs/pantheon_moteur.md`) :
  - un deck de test rempli de cartes UNIQUES (Sandman) bouclait à l'infini (règle d'unicité + remélange + Renfort) : cartes de remplissage non uniques et inertes (`sk107`) ;
  - un deck qui s'épuise remélange sa défausse : cartes de remplissage SOUS les cartes mesurées ;
  - en alter ego le méchant manigance et atteint vite le seuil 9 du complot 1B (stade 1 accompli en pleine mesure) : mesurer une phase du méchant en forme héros ;
  - `carte_du_surge` exige UN SEUL exemplaire de la carte semée ; `passer_sur_option="Defense"` ne doit PAS figurer dans un cas dont la capacité remplace l'attaque (la question n'est jamais posée : c'est une preuve de plus que l'attaque est annulée).
- **Substitution (`substituer_pack.py`, deux passes sk17 / sk18, puis sk170a et sk174b rejouées après renommage de leurs cas ; empreinte md5 du pack identique avant/après, aucun stub restant)** :
  chaque module est vidé à tour de rôle, les cas filtrés sur son card_id doivent tomber. Les cas « vert sans module » de chaque fiche sont TOUS des
  témoins d'ABSENCE d'effet (« TEMOIN », « sans … », « NON offerte ») ou des mesures de comportement NATIF du moteur sans module : PV par stade lus dans `desc` (sk170a), Hinder (sk179) et menace de départ
  `2*` (sk180) lus dans `desc`, victoire quand le dernier stade du méchant est vaincu (sk171a, sk171b, sk172a), « si ce stade est achevé, les joueurs
  perdent » du complot 2B (texte en gras lu par le moteur, sk174b), environnement qui reste de côté tant que le stade 1 dure (sk175a) : assumés comme le prévoit l'étape 7.
- **Étape 8 (autoplay)** : 40 parties `equilibre`, graines 1-8 : spider_man contre `sk_skrull_pantheon` (8) et `sk_skrull_pantheon_expert` (8), hulkling_kajislav contre les deux (16),
  plus 8 parties spider_man contre Rhino comme TÉMOIN. Grep exhaustif `NameError|AttributeError|TypeError|KeyError|AssertionError|Traceback|<F>` sur les 32 journaux
  du scénario (copiés dès la fin de chaque fournée, `/tmp` étant nettoyé par d'autres sessions) : **0**. Journaux lus : retournements du méchant (44 + 56),
  jetons de foi (236 + 261 poses), environnement mis en jeu (18 + 42), stade 2 du complot, Nogor, Strengthen the Faith, Prayer (Kly'bn déplace bien les traîtrises défaussées vers la défausse sans les distribuer),
  Fanatic, Priest, Collective Prayers, Sectarian Practices, Blessed by : chaque carte a été jouée en partie. 0 victoire sur 32 (profil `equilibre`, 4-5 rounds avant l'élimination ou
  l'accomplissement de 2B : le témoin Rhino fait 0/8 aussi, ce n'est pas un signal d'équilibrage) ; 0 partie bloquée sur le scénario ; le témoin en a 2
  (artefact du pilote sur `01093` Tenacity, carte officielle, sans rapport).
- **Étape 8 bis (plateau)** : `ui-app/src/board/pantheon-plateau.test.ts` (12 cas, états CAPTURÉS sur le moteur par `tools/sonde_campagne.py` : jetons de foi, face Kly'bn puis Sl'gur't
  de la même carte, carte Tenace, carte de boost portée par le méchant, Blessed attaché au sbire, environnement Stronghold / Destroyed), vu ROUGE sur un état cassé (clé de compteur fausse, attachement détaché : plusieurs cas rouges),
  puis VERT ; `tsc --noEmit` propre. `compteurs-fr.test.ts` : `faith` → « foi ».
- **Outils statiques** : `verifier_appels_modules skrull_menace` OK (calibré : un appel inexistant glissé dans sk188 est bien vu) ; `verifier_api_cartes` sans faute dans skrull_menace (calibré de même).
- **Moteur partagé** : uniquement un compteur (`'faith'`) et un trait (`"GOD"`) déclarés dans `card_face.py` + traduction du trait et du compteur (`defs/pantheon_moteur.md`).
- **Limites connues et questions** : `defs/pantheon_questions.md` (icône Hazard de sk186, distribution « dans l'ordre des joueurs », jetons de foi conservés d'un stade à l'autre, « Advance to stage 2B »
  qui saute la face A, Action de l'environnement non offerte sans jeton, choix du Priest / de Sectarian Practices, retournement en pleine activation). À noter : l'Action de héros de l'environnement
  Stronghold est PROPOSÉE même sans deux ressources de même type en main (le moteur ne teste la couleur qu'au paiement, comme `40090`), mais le paiement mixte est refusé (cas dédié).
- **Ce qu'aucun outil ne voit** : une vraie partie jouée par un humain dans le navigateur (agrément du scénario, équilibrage du bot : profil `equilibre`), non faite ; l'équilibrage des deux
  chemins du stade 1 (Stronghold / Destroyed) en particulier ne se juge qu'à la main.

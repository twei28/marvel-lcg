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



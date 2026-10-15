# Mode campagne « Skrull Menace » — regle par regle

Livret : `Campaigns/Skrull Menace (Released)/rulebook/rulebook 1.5.pdf`, 24 pages-images, relues une a une (rendues a 110 dpi, puis lues
a l'oeil ; les pages 22-24 aussi en PNG d'origine). Les pages citees sont celles du livret imprime. Le resume de `NOTES.md` a ete
verifie : un seul ecart (les fragments, voir Q5 dans `defs/campagne_mode_questions.md`), le reste est confirme.

Fichiers : `src/cards/pack/skrull_menace/campaign.py` (moteur), `data/campagnes/skrull_menace.json` (definition), `tools/test_campagne_chaine.py` +
`tools/cas/campagne_mode.py` (cas), `ui-check/tests/campagne-skrull-menace.spec.ts` (interface), `defs/campagne_mode_{moteur,questions}.md`,
`defs/campagne_mode_fr.txt`.

## Comment ca tourne

- Le carnet entrant (`campaign_log`) arrive dans le store du monde ; `CampaignSetup(n)` (porte par la manigance principale 1A du scenario n,
  type `Campaign`, hors jeu) lit le carnet a l'etape 13 de la mise en place (`Message.WhenCampaignSetup`).
- A la fin de la partie (`WhenGameOver`), `Releve` ecrit le carnet sortant ; le panneau de recompenses de la partie le propose, et ne reporte
  QUE les cles declarees dans le fichier de campagne (d'ou 11 champs declares, tous verifies par `tools/verifier_campagnes.py`).
- Une defaite n'ecrit rien : on rejoue sans penalite (p.5).

### Les cles du carnet

| Cle | Valeur | Ou dans le livret imprime |
|---|---|---|
| `Cooperation Area` | ids des cartes de campagne disponibles, `;` (ordre de la planche) | « Cooperation Area », p.22 |
| `Cooperation Progress` | `Carte: exigence;...` une par case cochee | tableau p.24 |
| `Shaper of Worlds Game Area` | `In play` / `Set aside, out of play` / `In another game area` | p.22 |
| `Cosmic Cube Creation Game Area` | `In play` / `In the victory display` / `In another game area` / `Removed from campaign` | p.22 |
| `Skrull Elite: Crusader` ... `Xavin` (5 cles) | vide (jamais tiree) / `In the victory display` / `In another game area` / `Removed from campaign` | p.23 |
| `Eliminated Players` (expert) | numeros de siege elimines pendant la partie | p.6 |
| `Player N Remaining hit points` (expert) | PV restants plafonnes aux PV de base | p.22 |
| `Alternative Standard Set`, `Alternative Expert Set` | `1` = remplacer par le set Skrull (reglages de la campagne) | p.4 |
| `Player N Identity` | nom de la face heros (ecrite par le moteur commun) | p.22 |

## Les regles

| # | Regle | Page | Implementation | Cas qui la prouve | Limites |
|---|---|---|---|---|---|
| 1 | Cinq scenarios dans l'ordre (Skrull Empire, Super-Skrull, Paibok, Skrull Pantheon, Secret Invasion), tous a gagner | 5 | `skrull_menace.json` : `scenarios[]` (ids = fichiers `data/scenarios/sk_*.json`, pas de `_expert` dans l'id : l'ecran prend la variante experte tout seul), le 5e `final` | spec Playwright (la boite est proposee, 5 scenarios, ordre de parution) ; chaine `CAMPAGNE ENTIERE` joue les cinq a la suite | rien |
| 2 | Identite fixe, deck libre entre les scenarios | 5 | generique (ecran de campagne : equipe figee a la creation, « Modifier les decks » repasse par la preparation et verifie l'identite) ; le moteur ecrit `Player N Identity` | non specifique (existant) | rien d'ajoute |
| 3 | Quand un joueur vainc un sbire ou une manigance annexe, il peut defausser le dessus de son deck pour la placer dans la pile de victoire | 6, carte rappel | `RegleDeCooperation` : deux capacites `Campaign` (`WhenUnitBeDefeated` sur les sbires, `WhenSchemeBeDefeated` sur les manigances annexes de tout genre), un `MayChooseOneAbility` ; rien si pas de joueur vainqueur, deck vide, `Victory X` (y va deja), sbire REVEALED (FAQ p.21) | 7 chaines `cooperation —` (acceptee, refusee, sans joueur, Victory X, manigance annexe, deck vide, REVEALED) + 32 parties du bot en mode campagne (`Mister Fantastic défaussée` puis le complot en pile de victoire) | Q9 |
| 4 | Tableau « Cooperation Progress » : chaque carte de la pile coche UNE exigence ; ligne complete = carte de campagne gagnee | 6, 24, FAQ 21 | `PROGRESSION` (13 lignes, 34 cases, relu au zoom), `ExigenceRemplie`, `AssignerLaProgression` (jumelage carte/exigence : le plus de lignes completes, puis le plus de cases) ; `Releve` | chaine pure (29 exigences distinctes, un cas qui la remplit + un qui ne la remplit pas ; une carte = une case ; deux Spy pour deux lignes ; le progres se garde) ; `CAMPAGNE ENTIERE` (3 scenarios cochent le tableau) | Q1 : la carte qui coche une case est choisie par le jeu |
| 5 | Les cartes de campagne n'entrent dans un deck que par la zone, sont rendues apres chaque partie, hors limite min/max | 5 | cartes generees a la mise en place APRES la composition du deck (`CardFactory.GenerateCard(id, player_deck)`), jamais ecrites au deck enregistre ; la zone du carnet ne perd jamais une carte | `zone de cooperation — scenario 2` (`carnet_verifier` : la zone est rendue intacte, plus les ajouts) | Q10 : le constructeur de decks doit encore cacher sk263-sk288 |
| 6 | Scenarios 2 a 5 : chaque joueur peut melanger UNE carte de chaque type (allie, manigance annexe de joueur, ressource, soutien, amelioration) de la zone a son deck | 10, 12, 15, 17 | `_cartes_de_la_zone` : `AskChooseOneText` par type et par joueur (avec « Cancel »), la carte prise n'est plus proposee au suivant | 5 chaines `zone de cooperation —` : une de chaque type, le choix du joueur, tout refuser, deux joueurs (unicite), scenario 1 (rien n'est propose) | questions en texte seul, pas en vignettes |
| 7 | Victoire des scenarios 2 et 3 : Super-Skrull + Searching for Powers ; Paibok + Skrull Military Training | 11, 13 | `AJOUTS_DE_SCENARIO` | `Shaper « Set aside » + Cube « In the victory display »` (`Cooperation Area = sk267;sk274`), `Elites — scenario 3` (sk265, sk275), `CAMPAGNE ENTIERE` | scenarios 1, 4, 5 : rien d'autre que les Elites |
| 8 | Shaper of Worlds : en jeu (engage avec le premier joueur) / de cote / remelange au deck rencontre | 7, 9, 10, 12, 15, 17 | `_shaper_et_cube` ; `sk229.py` ne remet plus le set de cote en mode campagne | 4 chaines `Shaper ...` + scenario 1 sans carnet | un Shaper jamais note est de cote |
| 9 | Cosmic Cube Creation : melange au scenario 1 ; en jeu / en pile de victoire (retire) / ailleurs (remelange) ; UN fragment par joueur de cote ; pile de victoire : les QUATRE fragments dans la zone | 7, 9, 10, 21 | `_shaper_et_cube`, ligne `Cosmic Cube Fragment` du tableau, `Releve` | `Shaper « In play »`, `... « In another game area »`, `... « In the victory display »`, `Cube « Removed »`, `CAMPAGNE ENTIERE` (S2 : Cube en pile de victoire, S3 : retire, aucun fragment) | Q5 |
| 10 | Skrull Elite : UNE au hasard aux scenarios 1 a 4 (« one other »), la restante au 5 ; sbire en pile de victoire : l'ensemble et le sbire quittent la campagne, l'allie du meme nom et la manigance annexe de joueur de son aspect rejoignent la zone ; sinon l'ensemble revient au scenario suivant | 7, 9, 10, 12, 15, 17 | `ELITES` (sbire, ensemble, allie, aspect, manigance), `_elites` (mise en place), `Releve` (etat et ajouts) | `Elites — scenario 3 / 4 / 5`, `mise en place 1` (une seule Elite, solo et deux joueurs), `CAMPAGNE ENTIERE` (cinq Elites distinctes en cinq scenarios) | Q2, Q3, Q4 ; les allies/manigances sont CREES a la mise en place par id (sk263-sk273) |
| 11 | Campagne experte : PV restants gardes, plafonnes aux PV de base, soin par un pion Acceleration, un joueur elimine revient, mechants (III) a la place des (I) | 6, 10, 12, 15, 17 | `_campagne_experte` ; `Releve` (PV plafonnes, `Eliminated Players`) ; les mechants (III) et le set Expert sont dans `data/scenarios/sk_*_expert.json` | `expert — 2 scenarios`, `... REFUSE le soin`, `... TEMOIN campagne standard`, `... PLAFONNES`, `... ELIMINE ... revient`, `... REFUSE le pion` | Q6, Q7 |
| 12 | Sets Standard Skrull / Expert Skrull a la place de Standard / Expert | 4 | reglages de campagne (`options_campagne`, cles `Alternative ... Set`) ; `_sets_alternatifs` retire les cartes du set remplace du deck rencontre et melange celles du set Skrull | 3 chaines `sets alternatifs` (remplace, les deux en expert, temoin a 0) | la liste « Mise en place » de l'ecran ne montre pas le remplacement |
| 13 | Victoire finale : Veranke vaincue au scenario 5 | 17 | `final: true` (le panneau dit « La campagne est gagnée ») ; `Releve` du niveau 5 ne note que les PV | `CAMPAGNE ENTIERE` (5e etape), spec Playwright du panneau pour le scenario 2 | aucun enregistrement au 5, le livret n'en demande aucun |
| 14 | Une defaite ne coute rien | 5 | `Releve` rend `{}` quand `players_won` est faux ; le panneau n'ecrit rien | le harnais (`fin: "Lose"` : carnet intact) | l'Elite est redessinee au nouvel essai (Q3) |

## Interface et ce qui a ete decide (15-16/10/2026)

- **Les cartes sk263-sk288 et la carte « Cooperation Progress Reminder » (sk289a/b)** : portees, fusionnees, 111 cas `[campagne_cartes]`
  verts. Absentes du constructeur de decks et de l'import (`SETS_RESERVES_A_LA_CAMPAGNE`, `public/js/deckbuilder/regles.js`).
- **Ecran « Coopération »** (`vueCooperation`, bloc `cooperation` de `skrull_menace.json`) : la zone en cinq colonnes (presentes en couleur,
  les autres en gris), le tableau de la p.24 (13 lignes, 34 cases, ligne complete = « gagnée »), le journal par scenario.
- **Journal par scenario** (Q13) : `campagne.historique[<scenario>]`, ecrit par le panneau de recompenses a chaque scenario gagne ; la colonne
  « Maintenant » est le carnet. Rien ne le relit pour jouer.
- **Choix des cartes de la zone AVANT la partie**, sur vignettes (`vueChoixDeLaZone`, bouton « Cartes de la zone » aux scenarios 2 a 5) :
  cle `Player N Cooperation Deck` lue par `_cartes_de_la_zone` (une carte inconnue, hors zone, deja prise ou 2e du meme type est ignoree ;
  `none` = rien). Rien de choisi : les questions de la mise en place comme avant. 4 chaines + mutation (3 rouges sur 4 sans la lecture).
- **Tableau « Cooperation Progress » en cases dans le panneau de fin de partie** (champ `cases`) : le jeu propose l'assignation, le joueur
  corrige case par case (Q1).
- **L'Elite du scenario, tiree et montree avant le lancement** (`elitesDuScenario`) : l'ecran fait le tirage du livret une fois, le garde
  (`Next Skrull Elite` = « <scenario>:<nom> ») et le moteur le lit ; une annonce d'un autre scenario ou d'une Elite deja tiree est ignoree.
  4 chaines + mutation (1 rouge sur 2 sans la lecture ; la 2e coincide avec le tirage a graine fixe).
- **Questions du jeu en francais** : cooperation, zone, campagne experte (`vocabulaire-moteur.ts`).
- **Partie reelle dans le navigateur** (`ui-check/tests/campagne-skrull-ecran-reel.spec.ts`) : cartes choisies a l'ecran dans le deck et
  en main, texte lisible (captures relues), question de cooperation affichee en francais, reponse qui defausse le dessus du deck.

## Ce qui n'est PAS fait (decisions, pas oublis)

- **Un bouton a cote de la carte vaincue** pour la cooperation : la question standard (« Défausser le dessus de ton deck pour placer ... ») est
  deja posee a l'ecran, en francais, avec « Annuler ».
- **La mise en pile de victoire par la console de debug** : un coup donne par la console n'enchaine pas la suite de la regle (artefact de
  l'outil, pas de la carte) ; la mise en pile est prouvee par les 7 chaines `cooperation —`.

## Comment rejouer les preuves

```bash
# depuis la racine de la copie, apres `bash outils/preparer-worktree.sh`
cd Fusion/marvel-lcg-src && export RELEASE=1 PARALLELES=2
"/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python" tools/test_campagne_chaine.py "$PWD/.game-src" 31000 /tmp/chaines.json          # 32 chaines, ~2 min
AUTOPLAY_REGLES=mode_campaign AUTOPLAY_CARNET='{"Cosmic Cube Creation Game Area":"In play"}' \
  "/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python" tools/autoplay.py "$PWD/.game-src" --deck lyja --vilains sk_super_skrull --parties 6 --paralleles 2
"/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python" tools/verifier_campagnes.py
# interface : serveur sur un port a soi (copie de .game-src + main.py), puis
UI_CHECK_BASE=http://127.0.0.1:31900 npx playwright test tests/campagne-skrull-menace.spec.ts --project=pc   # dans ui-check
```

## Resultats (16/10/2026)

- 36 chaines `[campagne_mode]` : 36/36 (dont la campagne entiere de 5 scenarios, les cas experte avec joueur elimine, la regle de cooperation).
- Preuve par mutation : 9 mutations d'une ligne du module (REVEALED, defausse du dessus, retrait de l'Elite en pile de victoire,
  Shaper « In play », unicite des cartes de la zone, ajouts du scenario 2, `*CampaignSetup(2)` de sk120a, joueur qui refuse le pion,
  plafond des PV) : toutes tuees par au moins une chaine.
- Bot (`autoplay.py`, mode campagne, carnets differents par scenario, standard et expert) : 32 parties, 0 plantage, la regle de
  cooperation vue a l'oeuvre dans le journal.
- `tools/verifier_campagnes.py` : 11 cles declarees, toutes trouvees. `verifier_appels_modules` : OK. `verifier_api_cartes` : aucune faute dans skrull_menace.
- Blocs existants apres les modifications des 1A et de sk229 : `[modulaires]` 117/117, `[sk-e]` 67/67, `[super_skrull]` 73/73,
  `[paibok]` 113/113, `[pantheon]` 98/98, `[secret_invasion]` 225/225.
- Playwright (`campagne-skrull-menace.spec.ts`) : 3/3 (boite proposee et ordonnee, ecran de campagne avec sets, reglages et livret, scenario 2
  gagne en vrai et zone / Shaper / Cube reportes par le vrai panneau).

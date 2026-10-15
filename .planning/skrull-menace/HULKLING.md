# Hulkling (Kajislav, Skrull Menace) : plan de portage

Source des textes : `transcriptions/hulkling.md` (doutes tranchés avec l'utilisateur, marqués VERIFIE).
Processus : `docs/reference/PROCESSUS-HEROS.md` + `PROCESSUS-CARTE.md` pour CHAQUE carte.

## Choix techniques (sans effet de règle, documentés ici)

| Point | Choix | Pourquoi |
|---|---|---|
| Pack `cards.json` | `skrull_menace` | préfixe `sk` déjà réservé (set 143, `tools/prefixes_fanmade.json`) |
| Extension | `143. Custom (Skrull Menace)` | « Custom » => rangé seul dans le filtre Fan-made (`isHomebrew`, catalog.js) |
| `card_id` | `sk` + numéro IMPRIMÉ sur 3 chiffres (+ a/b) | une seule numérotation pour tout le coffret (1 à ~375), lisible contre les scans |
| `set_name` | `Hulkling (Kajislav)` / `Hulkling (Kajislav) Nemesis` | un Hulkling OFFICIEL existe (cw `56029a`, set « Hulkling ») ; précédent : `Spider-Woman (Kajislav)`. Un set partagé ferait perdre le crédit auteur (`_auteurParSet`) |
| Scripts | `src/cards/pack/skrull_menace/hulkling_kajislav/` (+ `_nemesis`) | chemin dérivé du set_name (`FileManager.CleanName`) |
| `custom` | `"Kajislav"` sur chaque carte | affiche « Hulkling (Kajislav) » dans la grille (auteur.js) |
| Deck | `deck/starter/hulkling_kajislav.json`, `player_deck` REMPLI | decklist fournie par l'auteur (Extras/48) => recopiée telle quelle (PROCESSUS-HEROS étape 3) |
| Forme d'origine | script de la carte appelle `identity.ChangeAdditionalFrom(...)` | envoie déjà `WhenUnitWouldChangeForm` / `AfterUnitChangeForm` (identity.py:144) : les « After you change form » partent, et Inhibited peut annuler. AUCUNE retouche de `form.py` |
| Trait `HYBRID` | à ajouter à l'énum `TRAITS` | seul trait absent pour Hulkling ; fichier PARTAGÉ => passe des 107 decks |

## Cartes (numéro imprimé => card_id)

| card_id | Carte | Type | Notes |
|---|---|---|---|
| sk001a | Hulkling | Hero | Response, limite 1/round |
| sk001b | Teddy Altman | AlterEgo | Setup (origine Skrull) + Response après changement d'origine |
| sk002a / sk002b | Skrull Origin / Kree Origin | Upgrade permanent 2 faces | modèle : as002a/b Spider Armor |
| sk003 | Wiccan (William Kaplan) | Ally | +1 ATK si KREE, +1 THW si SKRULL |
| sk004 x2 | Kree Durability | Event | |
| sk005 x2 | Kree Ferocity | Event | |
| sk006 | Shift and Strike | Event | |
| sk007 x2 | Skrull Infiltration | Event | ignore patrol + crisis |
| sk008 | Skrull Regeneration | Event | surpaiement |
| sk009 | Alliance | Support | |
| sk010 | Ancestors | Support | Uses 2 |
| sk011 | Changeling | Upgrade | |
| sk012 | Emperor Dorrek-Vell | Upgrade | |
| sk013 | Excelsior | Upgrade | Restricted, Resource |
| sk014 | Nega Rings | Upgrade | |
| sk015 | Lauri-Ell | Ally Protection | |
| sk016 | Mur-G'nn | Ally Protection | |
| sk019 | Provoked! | Event Protection | |
| sk021 | Deflect the Blow | Upgrade Protection | |
| sk023 | Talos | Ally Basic | |
| sk024 | Drunk in Love | Event Basic | |
| sk025 | Strength in Otherness | Event Basic | Team-Up, Max 1 per deck |
| sk029 | Glorious Flight | Upgrade Basic | |
| sk030 | Pride | Upgrade Basic | Max 1 per player |
| sk031 | Interracial Hatred | Obligation | |
| sk032 | Empress R'Klll | Minion (némésis) | |
| sk033 | DNA Masking | SideScheme (némésis) | |
| sk034 | Inhibited | Attachment (némésis) | |
| sk035 | Assailed by Their Own | Treachery (némésis) | |
| sk036 | Swapping Roles | Treachery (némésis) | |

Numéros 17, 18, 20, 22, 26, 27, 28 = cartes OFFICIELLES du deck :
Counter-Punch `01077` x3, Not Today! `38016` x3, The Night Nurse `09019`, Hard to Ignore `16017` x2,
Energy `01088`, Genius `01089`, Strength `01090`.

## Décisions de l'utilisateur (15/10/2026, une question par carte)

| Carte | Question | Décision |
|---|---|---|
| (pack) | Comment présenter un second Hulkling ? | Pas de question à poser : tout héros d'une extension « Custom » va dans le filtre Fan-made, nom suivi de l'auteur (`custom`). |
| sk002a/b Origines | « spend a card » = ? | Seule une carte DÉFAUSSÉE DE LA MAIN compte ; la capacité Resource d'Excelsior en jeu ne « dépense » rien. |
| sk010 Ancestors | « in your hand or in play » | N'importe quelle carte en jeu (lecture littérale), plus ta main. |
| sk016 Mur-G'nn | Effet d'une ressource WILD défaussée ? | Aucun effet. |
| sk025 Strength in Otherness | « for each different card type » porte sur quoi ? | Sur les DEUX : X menaces et X dégâts. |
| sk031 Interracial Hatred | « KREE and SKRULL » | Les cartes KREE ou SKRULL (l'une ou l'autre). |

Sans question (lecture unique, ou choix technique documenté dans l'en-tête du module) : « Uses (2 individual counters) » = nom de compteur ; Deflect the Blow ne sert que sur une attaque NON défendue (défendre incline le héros) ; Skrull Infiltration demande à payer 2 indirects seulement quand une Patrouille/Crise bloque réellement le complot principal visé.

## Gabarits PROCESSUS-CARTE

`HULKLING-GABARITS.md` : 14 cartes OUI, 17 NON — il ne leur manque QUE l'étape 8 bis
(cas plateau vitest), impossible tant que Node n'est pas installé sur le Linux.

## État au 15/10/2026

Fait : données (31 card_id), scripts, deck de départ (decklist de l'auteur), extension 143,
images (assets/pics, originaux dans sauvegardes-serveur/scans-originaux), biographie
(heros-info.js), texte français (ui-app/src/board/textes-fr-fanmade.ts), 70 cas
test_capacites verts, substitution 31/31, autoplay 8+8 sans erreur.

Reste : Node (cas plateau + `ui-app/deployer.sh`, sans quoi le texte FR n'apparaît pas en
jeu), passe des 107 decks (fichier partagé `card_face.py` touché), une partie humaine.

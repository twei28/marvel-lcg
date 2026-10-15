# Brief commun — agents en parallele sur le coffret Skrull Menace (Kajislav)

Tu travailles dans une COPIE ISOLEE du depot (git worktree). Mission : porter un bloc du
coffret dans le moteur, carte par carte, selon les processus du projet. Les textes pour
l'utilisateur sont en FRANCAIS ; commentaires de code en francais, comme le reste du depot.

## Lire d'abord (dans ta copie)
1. `CLAUDE.md` ; `docs/reference/PROCESSUS-CARTE.md` (obligatoire pour CHAQUE carte, jusqu'au
   gabarit « Carte terminee : OUI ») ; `docs/reference/PROCESSUS-HEROS.md` si heros ;
   `docs/reference/GUIDE-CREATION-CONTENU.md` §1 ; `docs/reference/RECETTES-MOTEUR.md` ;
   la fiche `docs/reference/mots-cles/<mot>.md` de chaque mot-cle rencontre (README du dossier si absente).
2. `.planning/skrull-menace/NOTES.md` (conventions VALIDEES par l'utilisateur : icones, etoiles,
   numerotation, decisions), `INVENTAIRE.md`, tes transcriptions dans `transcriptions/`.
3. Modele a imiter : le scenario 1 deja fait, `Fusion/marvel-lcg-src/src/cards/pack/skrull_menace/skrull_empire/`
   (+ `skrull_society/`, `army_of_skrulls/`), ses definitions `.planning/skrull-menace/defs/skrull_empire_cards.py`,
   ses cas `[sk-e]` dans `Fusion/marvel-lcg-src/tools/test_capacites.py`, ses gabarits `SKRULL-EMPIRE-GABARITS.md`,
   `data/scenarios/sk_skrull_empire*.json`, `data/encounter_sets/sk_*.json`. Hulkling : `hulkling_kajislav/`.
4. Les cartes (images 1500x2150) : `~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav/`
   (sous-dossiers Hero Packs / Scenario Packs / Modular Sets / Campaigns). Regarde-les (outil Read sur
   l'image) pour verifier chiffres et icones : la transcription peut se tromper. Convention d'icones
   validee : Crisis = « ! » dans une explosion ; Acceleration = croix + pointe + barre ; Hazard = croix sur
   carte penchee ; Amplify = croix + avion ; Y rouge = icone de boost ordinaire ; etoile ★ = renvoi au texte.

## Environnement
- Python du depot : `PY="/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python"` ; Node : `export PATH="$HOME/.local/bin:$PATH"`.
- Avant tout test : `bash outils/preparer-worktree.sh` (a la racine de TA copie). Les harnais se lancent sur
  `"$PWD/.game-src"` (chemin ABSOLU), depuis `Fusion/marvel-lcg-src`. JAMAIS deux harnais a la fois dans ta copie.
  Ports : utilise UNIQUEMENT ta plage (voir ta mission), < 32768. `PARALLELES=2` maximum.
- Outils (voir leur en-tete) : `tools/test_capacites.py <game_dir> <port> <rapport.json> [filtre]`,
  `tools/substituer_pack.py <game_dir> <port> <prefixe>` (preuve par substitution : sauvegarde le pack et son md5
  AVANT, verifie l'empreinte APRES ; relance seul un cas « vert sans module » avant de conclure : faux positifs
  frequents sous charge), `tools/verifier_appels_modules.py <gd> <port> skrull_menace`, `tools/verifier_api_cartes.py`,
  `tools/recalculer_checksums.py` (apres tout changement de data/cards.json ou sets_info.json),
  `tools/autoplay.py --deck X --vilains <scenario> --parties 8 --port P --paralleles 2` (le bot n'attaque pas
  un mechant a PV infinis : 0 victoire n'est pas un signal ; cherche tracebacks et parties bloquees).
- Sonde d'etat : voir `Fusion/marvel-lcg-src/tools/sonde_campagne.py` (Puzzle.* en direct, descripteur du plateau).

## Regles de partage (IMPORTANT : d'autres agents travaillent en meme temps)
- NE MODIFIE PAS `tools/test_capacites.py`. Tes cas vont dans `Fusion/marvel-lcg-src/tools/cas/<bloc>.py`
  (`CAS = [...]`, et `VERIFICATIONS = r'''...'''` si tu as besoin de fonctions de verification). Prefixe les noms
  de cas par `[<bloc>]` pour pouvoir filtrer.
- NE MODIFIE PAS `ui-app/src/board/textes-fr-fanmade.ts` ni `data/translate_fr.json`. Tes textes francais vont dans
  `.planning/skrull-menace/defs/<bloc>_fr.txt` (memes lignes que `defs/lyja_fr.txt` : commentaire + `'sk###': "…",`),
  UNE entree par card_id, y compris copies. Je les fusionne.
- Cartes : definitions dans `.planning/skrull-menace/defs/<bloc>_cards.py` (liste `CARDS`, format de
  `defs/lyja_cards.py`) et un script IDEMPOTENT `defs/inserer_<bloc>.py` qui les (re)insere dans
  `data/cards.json` (cle `skrull_menace`, remplace par card_id, JSON indent=1 ensure_ascii=False) puis met a jour
  `data/sets_info.json` (`143. Custom (Skrull Menace)`) et recalcule les checksums. Je rejouerai ce script apres fusion.
  Scenarios : `data/scenarios/sk_<nom>.json` (+ `_expert.json`), sets rencontre `data/encounter_sets/sk_<nom>.json`.
- Moteur PARTAGE (`src/game/**`, `src/cards/pack/__init__.py`, enums de traits dans `card_face.py`) : ne le touche
  que si INDISPENSABLE, de facon ADDITIVE et minimale (un trait manquant = une ligne). Chaque modification est
  consignee dans `defs/<bloc>_moteur.md` (fichier, quoi, pourquoi, cas qui la prouve). Une modification de moteur
  exige de relancer toute ta batterie. Ne reformate rien.
- Images : les scans ne sont PAS versionnes. Ecris-les dans le depot PRINCIPAL, chemins absolus :
  `/home/oem/Desktop/Marvel LCG/Fusion/marvel-lcg-src/assets/pics/<card_id>.png` (petit cote ramene a 615 px,
  LANCZOS ; carte paysage : rotation 90 degres anti-horaire `im.rotate(90, expand=True)` avant) et l'original dans
  `/home/oem/Desktop/Marvel LCG/sauvegardes-serveur/scans-originaux/<card_id>.png`. Copies d'une carte : une seule image
  par card_id. Recette : voir le bloc Lyja dans l'historique git (`git log -p` du commit d845b442 ne contient pas les
  images ; la regle ci-dessus suffit).
- Ne deploie JAMAIS (`deployer.sh` interdit : decision de l'utilisateur). Ne touche pas au jeu qui tourne sur le port 2345.

## Vocabulaire francais (textes de cartes) — a respecter, un test le verifiera
Source : Guide de reference FR (`Fusion/marvel-lcg-src/assets/docs/mc01_guide_de_reference_fr.pdf`, `pdftotext` disponible)
+ textes officiels `ui-app/src/board/textes-fr-complets.ts` (cherche TOUJOURS comment une phrase equivalente est rendue
sur une carte officielle avant d'ecrire la tienne). Acquis : « est censé(e) » (jamais « devrait ») ; « n'importe quelle
quantité de dégâts » ; « jeton » pour un compteur de carte, « pion Accélération » ; « stade » (« achevé ») ; « Une fois
révélée » (manigance/traîtrise), « Une fois vaincu » (personnage), « Une fois déjouée » (MANIGANCE) ; « champ de boost »,
« icône d'étoile » ; « perd le texte imprimé dans sa boîte de texte » ; « choisissez : soit vous inclinez…, soit vous… » ;
« attribuez-vous 1 carte Rencontre face cachée » ; « Interruption forcée », « Réponse forcée », « Action de héros »,
« Réponse de héros », « Action d'alter ego » ; Sonné / Désorienté / carte d'état Tenace ; Ténacité ; Solide ; Robuste ;
Renfort (surge) ; Déferlement (overkill) ; Perçant ; Vilenie ; Incitation X ; Entrave X ; Distance (ranged) ;
« 1 max par deck », « En Équipe (A et B) » ; stats ATQ, CTR, DEF, REC, MNG ; noms propres et traits `[[TRAIT]]` en anglais.

## Pieges deja payes (ne les repaie pas)
- Dans `desc`, `*` apres un nombre : ATK/THW d'un allie = degats consequentiels ; HP/StartingThreat = « par joueur » ;
  SCH avec `*` = MULTIPLIE par le nombre de joueurs (donc SCH plein : "2", jamais "2*").
- `Puzzle.CreateEncounterDeck(a, b, c)` : la DERNIERE carte creee est sur le dessus. `Puzzle.Remove` pour vider ce qui est
  aleatoire (planetes...) ; `main_exclusive` pour fixer la main ; une carte en deux copies : `EmptyEncounterDeck()` avant
  de viser une copie.
- Un cas « vert sans module » en substitution sous charge est souvent un faux positif : relance-le seul. Un cas qui
  verifie une ABSENCE d'effet reste vert sans module : assume-le dans le gabarit.
- Dans un cas, un effet visible (degats, menace) peut venir d'une AUTRE carte de la main de depart (Great Responsibility
  01061 transforme la menace en degats) : fixe la main (`main_exclusive`).
- Un meme nom unique de carte d'un stade a l'autre : retirer l'ancienne avant de reveler la nouvelle.
- Les fabriques d'abilites ont des limites (ex. `ThisGainKeywordWhileFaceIsInPlay` refuse un Environnement ;
  `get_new_value` rend une grandeur POSITIVE). Quand ca ne marche pas, SONDE l'etat reel (sonde_campagne) au lieu de deviner.
- Ne laisse aucun `print` de debug ni fichier temporaire dans le depot.

## Ambiguites de regles : NE DEVINE PAS EN SILENCE
Tu ne peux pas interroger l'utilisateur. Pour toute vraie ambiguite (texte de carte qui admet deux lectures, symbole
douteux, cas non prevu par le livret), choisis la lecture la plus raisonnable, implemente-la, et consigne dans
`.planning/skrull-menace/defs/<bloc>_questions.md` : card_id, la phrase, les lectures possibles, celle retenue, le chemin de
l'image. Je poserai ces questions a l'utilisateur et tu (ou moi) corrigerons.

## Livrables et fin
- Scripts `src/cards/pack/skrull_menace/<dossier_du_set>/<card_id>.py` (dossier = `FileManager.CleanName(set_name)` ;
  verifie-le), `__init__.py` avec helpers, cartes dans cards.json, images, decks/scenarios/sets, cas, gabarits
  `.planning/skrull-menace/<BLOC>-GABARITS.md` (un gabarit PROCESSUS-CARTE par carte, avec les preuves REELLES : sorties
  de substitution, cas verts, autoplay ; « Carte terminee : OUI » seulement si tout est tenu), et les fichiers `defs/…`.
- Passe finale : `verifier_appels_modules`, `verifier_api_cartes` (aucune faute dans skrull_menace), TOUS tes cas verts,
  substitution de tout ton pack, autoplay (8 parties par scenario/deck, 0 traceback), `tools/verifier_tous_les_decks.py`
  si tu as touche un fichier partage ou ajoute un deck. Commit sur la branche de ta copie (plusieurs commits propres,
  messages en francais), avec en fin de message :
  `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` et `Claude-Session: https://claude.ai/code/session_01Fr5EHa4uWZF6muMMGeLMU3`.
- Rapport final COURT (< 25 lignes) : ce qui est fait, resultats chiffres, fichiers partages touches, questions ouvertes
  (renvoie a `defs/<bloc>_questions.md`), ce qui reste.

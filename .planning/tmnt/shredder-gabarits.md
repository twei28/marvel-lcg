# Shredder v3 (`ts`) et TMNT Standard-Expert (`te`) : gabarits PROCESSUS-CARTE, 16/10/2026

Preuves communes à toutes les cartes (16/10/2026, copie `tmnt-shredder`, scans relus un à un) :

- **Cas** : `Fusion/marvel-lcg-src/tools/cas/tmnt_shredder.py` (préfixe `[shredder]`, 114 cas, tous verts) et
  `tools/cas/tmnt_standard_expert.py` (préfixe `[tmnt-se]`, 28 cas), lancés par
  `tools/test_capacites.py .game-src <port> rapport "[shredder]"` / `"[tmnt-se]"` (CAS_PREFIX propre, ports 37100+,
  jamais deux harnais sur le même dossier). Résultat final (16/10/2026, après tous les correctifs) : `[shredder]` 114/114 ; `[tmnt-se]` 21/28 dans ce worktree (les 7 cas `[dazed]` exigent la carte d'état Dazed du pack Baxter : 7/7 verts en copie d'intégration).
- **Substitution** (`tools/substituer_pack.py .game-src 38000 ts`, puis `... 39000 te`) : chaque module remplacé par
  un stub tombe au ROUGE sur au moins un cas sujet : `ts` 29/29 cartes, `te` 8/8 modules (empreinte md5 des modules
  identique avant/après : aucun stub oublié). Les cas qui restent verts sans module sont des TÉMOINS D'ABSENCE (« sans X,
  rien ne se passe »), des mesures de données natives de `desc` (Guard, Patrol, Toughness, Quickstrike, Steady,
  Retaliate, Hinder, Incite, Hazard, Crisis, ATK+ / SCH+ : lues par le moteur, aucun module) ou des cas portés par une
  autre carte dont le nom cite l'id. Bilan rouges/cas : ts001 3/4, ts002 5/5, ts003 4/4, ts004a 2/2, ts004b 2/3,
  ts005a 2/3, ts005b 2/3, ts006 5/7, ts007 4/6, ts008 2/3, ts010 4/4, ts012 1/3, ts013 3/3, ts015 2/4, ts017 3/3,
  ts020 2/3, ts022 4/4, ts101 3/3, ts102 3/4, ts103 3/5, ts104 3/4, ts201 3/4, ts202 2/3, ts203 2/4, ts204 2/2,
  ts205 3/5, ts206 1/1, ts301 2/2, ts303 1/1 ; te101 2/3, te102 2/2, te004 2/2, te005 2/2, te006 2/2.
  `te001`, `te002`, `te103` (carte d'état **Dazed**, livrée par le pack Baxter Stockman) : substitution rejouée dans une
  copie d'INTÉGRATION (ce dépôt + les fichiers moteur de Dazed du worktree `tmnt-baxter`, non commités à cette date) :
  1/1 rouge chacune. **Les 7 cas `[dazed]` ne sont verts qu'avec Dazed ; dans ce worktree seul ils échouent.**
  Habillages `te021-te027`, `te121-te123` (`ability_link`, aucun module) : les 8 modules du CORE `01186-01193` ont été
  stubbés ensemble, les 8 cas « habillage » sont tombés au rouge (8/8), modules restaurés (md5 identique).
- **Cas de l'encart du scénario** (« Shredder Insert ») : 9 cas `[shredder] encart Q&R` (3 Cloaked + activation = +6 ; 3
  dégâts / 3 Cloaked ; 3 × 1 dégât ; Tough avant Cloaked dans les deux ordres ; Tough + Cloaked + piercing ; Étourdi +
  Cloaked ; Steady ne change pas le plafond). Ils ont trouvé UN défaut moteur réel (Cloaked consommé avant Tough si posé
  avant), corrigé dans `status/cloaked.py`.
- **Autoplay** : joué dans la copie d'INTÉGRATION décrite plus haut (Dazed présent : `te001`, `te002`, `te103` y sont tirées sans erreur) (`tools/autoplay.py`, héros témoin Spider-Man, profil équilibre, 8 parties par ligne, `--paralleles 3`) :
  scénario `shredder` (Chunin + Foot Goon Squad), `shredder_expert`, et quatre variantes temporaires (non commitées) avec
  UN SEUL modulaire (Chunin seul, Foot Goon Squad seul, normal et expert) ; solo : 6 × 8 = 48 parties terminées, 0
  plantage, `grep -c "NameError|AttributeError|TypeError|KeyError|AssertionError|Traceback"` = 0 sur les 48 journaux ;
  à DEUX joueurs (`--deck2 black_widow`, option ajoutée) : 6 × 8 = 48 parties, 0 erreur de script, mais 3 parties sur
  8 bloquées sur la même question du pilote (`Ask(id=8)` visant Natasha Romanoff) dans CHAQUE variante ; **le témoin
  Rhino à deux joueurs bloque 8 parties sur 8** : le blocage est une limite du pilote à deux joueurs, pas du scénario.
  Taux de victoire 0 % partout, y compris le témoin Rhino en solo (0 sur 8, 6,9 rounds contre 3,8 pour Shredder) : le
  pilote ne gagne jamais avec ce deck, taux non comparable ; Shredder tient 3,8 rounds en normal, 2,8 en expert. Un
  premier passage (avant le correctif) avait trouvé 7 plantages sur 32 parties à un modulaire : TOUS `te006` Skulk
  (`AssertionError face != last_face` : le détournement du boost « deal this card to the first player » restait actif
  et renvoyait la traîtrise dans les cartes distribuées après sa révélation). Corrigé (usage unique) dans les deux
  helpers, cas `te006 Skulk Boost : donnée puis RÉVÉLÉE` (rouge sans correctif, vert avec) et `ts101 Boost puis
  révélation`. Le même motif existe dans `tl015` (Leonardo) : sans conséquence pour un sbire qui entre en jeu, mais
  une traîtrise le déclencherait ; à reprendre dans ce pack.
- **Gates** : `test_cards.py` : 6452 modules, 0 erreur (au moment des 30 + 17 cartes) ;
  `verifier_appels_modules.py shredder tmnt_standard_expert` : OK, et **calibré** (un `Worlds.PasUneMethode` écrit
  exprès est détecté, fichier retiré) ; `verifier_tous_les_decks.py` (fichiers moteur partagés touchés : passe
  complète) : **145/145 decks montent une partie** ; régression des cartes qui posent Cloaked : `[cloaked` 17/17,
  `tl015` 6/6, `tl016` 3/3, `td005` 5/5 verts après le plafond d'une carte Cloaked et l'ordre Tough/Cloaked.
  PAS relancée : la batterie complète de `test_capacites.py` (~2 h, 4 500 cas).
- **Icônes vérifiées par découpe contre des cartes officielles** (coin bas droit, même résolution) : icône de boost
  rouge (forme en Y) de `ts008` (étoile + 1) = `01101` Hydra Mercenary (1) ; étoile de boost de `ts008` = `04027`
  Crossfire ; `ts301` (2 icônes) = `02022` (étoile + 2). Icône centrale de `ts020` Foot Rikugun = **HAZARD** (même
  glyphe que `01107` ; différente de l'Accélération `01109` « + sur maison » et de l'Amplify `16054` « + sur avion ») ;
  icône de `ts022`, `ts206`, `ts305` = **CRISIS** (glyphe `01125`/`14025`). Icône de menace par joueur (silhouette) lue
  sur `ts004b`, `ts005b`, `ts020`, `ts022`, `ts206` (« 1[per_hero] », « 2[per_hero] »…), menace fixe de `ts305` (3, sans
  silhouette) vs Hinder 1[per_hero] imprimé en texte.
- **Étape 8 bis (plateau)** : `ui-app/src/board/shredder-plateau.test.ts` (4 cas). Sensibilité prouvée : dans `zones.ts`,
  `attacheesPar.get(id)` rendu `.slice(0, 1)` → 3 cas ROUGES (Cloaked multiples, attachements, Kira no Ken), ligne
  restaurée, 4/4 verts. Le point nouveau est « plusieurs cartes Cloaked sur un même personnage » (jusqu'à 4 sur Shredder III) :
  chaque carte d'état doit être dessinée. Pas de correctif d'affichage nécessaire (l'UI dessinait déjà tout). Ce que le
  test NE prouve PAS : un rendu pixel à l'écran (jamais regardé).
- Moteur partagé touché (additif, documenté) : voir le rapport final et `docs/reference/RECETTES-MOTEUR.md` §10.
- Questions ouvertes : `.planning/tmnt/shredder-questions.md` (Q1-Q9) ; `te201` Intense Combatants : scriptée le 16/10/2026
  (carte d'état Intensified), « Carte terminée : OUI ».

### te001 : No Quarter (Treachery, set TMNT Standard)

- [x] Étape 2 : référence(s) : `01188` Caught Off Guard (`player.DiscardControlCards( effect, upgrade=True, support=True)`, rendu None si rien de defausse) ; `hs042` (`message.AfterThisActivation`). « Daze » : voir `Daze` (carte d'etat livree par le pack Baxter Stockman).
- [x] Étape 5 : mots-pièges : « discard an upgrade OR support YOU CONTROL » (pas un allie) ; « If NO cards were discarded » = le retour de la defausse est None ; « daze YOUR identity ».
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : aucune valeur imprimee en `desc`.
- [x] Étape 7 : 3 cas sujet(s) : te001 [dazed] No Quarter : sans amelioration ni soutien, l'identite est hebetee (Dazed) ; te001 [dazed] No Quarter, avec une amelioration : elle est defaussee et l'identite n'est PAS hebetee ; te001 [dazed] No Quarter Boost : apres l'activation, l'identite est hebetee. Substitution : rouges 1/1.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : NON : cas écrits et verts en copie d'intégration (Dazed du pack Baxter), rouges sans module (1/1) ; dans CE worktree la carte d'état Dazed n'existe pas, donc non prouvée ici. A re-lancer après fusion.

### te002 : Outmatched (Treachery, set TMNT Standard)

- [x] Étape 2 : référence(s) : `te001` (le boost) ; Incite 2 lu dans `desc` (`qsv 14025`, `sk101`).
- [x] Étape 5 : mots-pièges : voir l'en-tete du script
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Incite 2.
- [x] Étape 7 : 2 cas sujet(s) : te002 [dazed] Outmatched Boost : apres l'activation, l'identite est hebetee ; te002 [dazed] Outmatched : l'identite est hebetee. Substitution : rouges 1/1.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : NON : même raison que te001 (7 cas `[dazed]`).

### te004 : Pursued by Shadows (Treachery, set TMNT Standard)

- [x] Étape 2 : référence(s) : `hood 24031` Seek and Destroy / `mts 21188` (la recherche `Search.EncounterCard(include_discard_pile=True, include_set_aside=True, is_nemesis=player)`), `01190` Shadow of the Past (`Reveal(..., if_entered_play=)` + `ThisCardGainSurge`).
- [x] Étape 5 : mots-pièges : « YOUR nemesis minion » (`is_nemesis=player`, jamais celui d'un autre joueur) ; « Cloak your nemesis minion » : meme s'il etait DEJA en jeu ; « did not enter play THIS WAY » : seule la revelation de cette carte compte.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 2.
- [x] Étape 7 : 2 cas sujet(s) : te004 Pursued by Shadows : le sbire nemesis est cherche, revele et CAMOUFLE (pas de Renfort) ; te004 Pursued by Shadows : nemesis DEJA en jeu -> il est camoufle et la carte gagne Renfort. Substitution : rouges 2/2.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### te005 : Shadow of the Past (Treachery, set TMNT Standard)

- [x] Étape 2 : référence(s) : Shadow of the Past (TMNT Standard 5/7) — TRAITRISE. 2 icones de boost. Texte IDENTIQUE au core 01190 : le script est celui de `01190` (`cards/pack/core/standard/01190.py`), recopie ici parce que la carte vit dans un autre pack et n'a pas d'`ability_link` (le texte imprime est le meme, mot pour mot :
- [x] Étape 5 : mots-pièges : voir l'en-tete du script
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 2.
- [x] Étape 7 : 2 cas sujet(s) : te005 Shadow of the Past : sbire ET complot annexe nemesis reveles, le reste du set melange au deck ; te005 Shadow of the Past, sans sbire nemesis : la carte gagne Renfort. Substitution : rouges 2/2.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### te006 : Skulk (Treachery, set TMNT Standard)

- [x] Étape 2 : référence(s) : `gob 02044` / `mts 21151` (`player.GetIdentity() .TakeIndirectDamage(this, n, effect)`) ; `tl015` (boost : `FaceCacheeAuPremierJoueur`).
- [x] Étape 5 : mots-pièges : « TAKE 2 indirect damage » (le joueur qui revele) ; « cloak THE VILLAIN » ; le boost n'a RIEN d'autre : la carte est donnee, pas defaussee.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : aucune valeur imprimee en `desc`.
- [x] Étape 7 : 3 cas sujet(s) : te006 Skulk : 2 degats indirects au joueur ET le vilain est camoufle ; te006 Skulk Boost : la carte est donnee face cachee au premier joueur ; te006 Skulk Boost : donnee puis REVELEE dans le meme round -> elle est defaussee UNE fois (plus de boucle). Substitution : rouges 2/2.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### te021 : Advance (Treachery, set TMNT Standard Reskin)

- [x] Étape 2 : référence(s) : `ability_link` vers le core : AUCUN module propre (voir ci-dessous)
- [x] Étape 5 : mots-pièges : memes mots que le core (texte verifie sur le scan)
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : aucune valeur imprimee en `desc`.
- [x] Étape 7 : 1 cas sujet(s) : te021 Advance (habillage de 01186) : le vilain manigance (1 menace de plus sur 1B). Substitution : voir la section communs (habillage par ability_link).
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### te023 : Assault (Treachery, set TMNT Standard Reskin)

- [x] Étape 2 : référence(s) : `ability_link` vers le core : AUCUN module propre (voir ci-dessous)
- [x] Étape 5 : mots-pièges : memes mots que le core (texte verifie sur le scan)
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : aucune valeur imprimee en `desc`.
- [x] Étape 7 : 2 cas sujet(s) : te023 Assault (habillage de 01187), forme heros : le vilain attaque ; te023 Assault, alter-ego : la carte gagne Renfort. Substitution : voir la section communs (habillage par ability_link).
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### te025 : Caught Off Guard (Treachery, set TMNT Standard Reskin)

- [x] Étape 2 : référence(s) : `ability_link` vers le core : AUCUN module propre (voir ci-dessous)
- [x] Étape 5 : mots-pièges : memes mots que le core (texte verifie sur le scan)
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 1.
- [x] Étape 7 : 1 cas sujet(s) : te025 Caught Off Guard (habillage de 01188) : une amelioration controlee est defaussee. Substitution : voir la section communs (habillage par ability_link).
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### te026 : Gang-Up (Treachery, set TMNT Standard Reskin)

- [x] Étape 2 : référence(s) : `ability_link` vers le core : AUCUN module propre (voir ci-dessous)
- [x] Étape 5 : mots-pièges : memes mots que le core (texte verifie sur le scan)
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 1.
- [x] Étape 7 : 1 cas sujet(s) : te026 Gang-Up (habillage de 01189), forme heros : le vilain ET chaque sbire engage attaquent (2 + 1 = 3). Substitution : voir la section communs (habillage par ability_link).
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### te027 : Shadow of the Past (Treachery, set TMNT Standard Reskin)

- [x] Étape 2 : référence(s) : `ability_link` vers le core : AUCUN module propre (voir ci-dessous)
- [x] Étape 5 : mots-pièges : memes mots que le core (texte verifie sur le scan)
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 2.
- [x] Étape 7 : 1 cas sujet(s) : te027 Shadow of the Past (habillage de 01190) : sbire ET complot annexe nemesis. Substitution : voir la section communs (habillage par ability_link).
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### te101 : Annihilation (Treachery, set TMNT Expert)

- [x] Étape 2 : référence(s) : `hood 24054` Total Annihilation (MEME mecanique : `villain.DoAttackYou(player, effect, property=AttackProperty(overkill=True))` et `WhenCardBecomeBoost(..., during_attack=True, attacker=Villain)` + `GainOverKill`).
- [x] Étape 5 : mots-pièges : « the VILLAIN » (pas un sbire : `attacker=Villain`) ; « THAT attack » : l'attaque de cette carte.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 2.
- [x] Étape 7 : 3 cas sujet(s) : te101 Annihilation : le vilain attaque et l'attaque gagne OVERKILL (Maria Hill HP 2, 1 degat : excedent sur le ; te101 Annihilation Boost : si le vilain attaque, l'attaque gagne OVERKILL (3 contre Maria Hill HP 2) ; te101 Annihilation Boost, TEMOIN : un boost sans overkill (Foot Soldiers) : pas d'excedent. Substitution : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### te102 : Haunted by the Past (Treachery, set TMNT Expert)

- [x] Étape 2 : référence(s) : `hood 24031` Seek and Destroy (la recherche + `PutIntoPlay`), `core expert 01191` Exhaustion (`Faces.ExhaustAll([identity])`), `ThisCardGainSurge`.
- [x] Étape 5 : mots-pièges : « put it into play engaged with YOU » ; « did not enter play THIS WAY » ; les DEUX consequences (epuiser ET surge) quand il n'entre pas.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 2.
- [x] Étape 7 : 2 cas sujet(s) : te102 Haunted by the Past : le sbire nemesis est cherche et mis en jeu engage avec le joueur ; te102 Haunted by the Past, sans sbire nemesis : identite epuisee ET Renfort. Substitution : rouges 2/2.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### te103 : Sinister Plan (Treachery, set TMNT Expert)

- [x] Étape 2 : référence(s) : `te004` (recherche + `if_entered_play`), `te001` (`Daze`).
- [x] Étape 5 : mots-pièges : « YOUR nemesis SIDE SCHEME » (type SchemeSide2, `is_nemesis`) ; on dazes TOUJOURS ; le surge seulement si le complot annexe n'est pas entre.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 3.
- [x] Étape 7 : 2 cas sujet(s) : te103 [dazed] Sinister Plan : complot annexe nemesis revele ET identite hebetee ; te103 [dazed] Sinister Plan, sans complot annexe nemesis : identite hebetee ET Renfort. Substitution : rouges 1/1.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : NON : même raison que te001 (carte d'état Dazed).

### te121 : Exhaustion (Treachery, set TMNT Expert Reskin)

- [x] Étape 2 : référence(s) : `ability_link` vers le core : AUCUN module propre (voir ci-dessous)
- [x] Étape 5 : mots-pièges : memes mots que le core (texte verifie sur le scan)
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 2, Surge 1.
- [x] Étape 7 : 1 cas sujet(s) : te121 Exhaustion (habillage de 01191) : identite epuisee + Renfort. Substitution : voir la section communs (habillage par ability_link).
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### te122 : Masterplan (Treachery, set TMNT Expert Reskin)

- [x] Étape 2 : référence(s) : `ability_link` vers le core : AUCUN module propre (voir ci-dessous)
- [x] Étape 5 : mots-pièges : memes mots que le core (texte verifie sur le scan)
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 2.
- [x] Étape 7 : 1 cas sujet(s) : te122 Masterplan (habillage de 01192) : 4 menaces sur chaque complot annexe. Substitution : voir la section communs (habillage par ability_link).
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### te123 : Under Fire (Treachery, set TMNT Expert Reskin)

- [x] Étape 2 : référence(s) : `ability_link` vers le core : AUCUN module propre (voir ci-dessous)
- [x] Étape 5 : mots-pièges : memes mots que le core (texte verifie sur le scan)
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 3, Surge 1.
- [x] Étape 7 : 1 cas sujet(s) : te123 Under Fire (habillage de 01193) : Renfort + revele la carte du dessus du deck. Substitution : voir la section communs (habillage par ability_link).
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### te201 : Intense Combatants (Environment, set TMNT Intense)

Scriptée le 16/10/2026 (`src/cards/pack/tmnt_standard_expert/tmnt_intense/te201.py`), après réception de la carte
d'état INTENSIFIED (réponse Q2). Moteur : 7e carte d'état, fiche `docs/reference/mots-cles/intensified.md`.

- [x] Étape 2 : référence(s) : 56175 Contaminant Immunity / ah006 Gamma Barrier (Interrupt « would be stunned » →
      `SetBeInstead` sur la pose, puis autre effet) ; fenêtre DÉDIÉE `WhenStatusWouldCardPlaceOnAgain` ouverte avant
      les plafonds (un second Sonné est refusé par `CanbeStunned` avant `WhenStatusWouldCardPlaceOn`). Permanent / Setup :
      `desc`, aucun code. Intensified : `tough.py` (gabarit d'état) + paibok `__init__.py` (`WhenCardWouldDiscard` +
      `SetBeInstead`).
- [x] Étape 5 : mots-pièges : « a character » (tout personnage, ami ou ennemi : `CardFinder()`) ; « already has 1 copy
      of THAT status card » (même nom, ≥ 1, testé avant les plafonds) ; « instead » (la pose N'A PAS lieu, une
      Intensified la remplace) ; **Forced** Interrupt (`AbilityType.ForcedInterrupt`, avant la pose). Intensified : « would
      discard » (remplacement), « instead » (la carte d'origine RESTE), « cannot be given ... no status cards ».
      Résultat : conforme ; la seconde Intensified n'ouvre pas la fenêtre (sinon boucle).
- [x] Étape 6 : nombres : Permanent 1, Setup 1 (`desc`) ; « 1 copy » = `HasStatus` (≥ 1). Résultat : conforme.
- [x] Étape 7 : `tools/cas/intensified.py` : 8 cas `[te201]` (second Sonné → Intensified ; témoin sans te201 ; premier
      Sonné normal ; second Exposé → Intensified ; témoin Exposé ×2 ; seconde Intensified s'empile sans boucle ; seconde
      Coriace du héros → Intensified ; chaîne complète Sonné ×2 → deux attaques annulées) + 16 cas `[intensified]`.
      Substitution : `te201.py` retiré → 4 cas te201 ROUGES (les 4 autres sont des témoins / absences, assumés) ;
      `intensified.py` retiré → 8 cas de remplacement + chaîne te201 ROUGES ; `CanbeIntensified` neutralisé → « ne
      peut PAS être donnée » ROUGE ; garde `vidage` retirée → « défaussez chaque carte d'état » ROUGE. Remis : 24/24 VERTS.
- [x] Étape 7 bis : limite imprimée NON.
- [x] Étape 8 : autoplay Shredder spider_man, 4 parties (voir rapport) : 0 traceback. ⚠ te201 n'est dans AUCUN ensemble
      ni scénario (environnement optionnel) : l'autoplay ne l'exerce pas, il ne prouve que la non-régression du moteur
      des états. Batterie complète : 5233/5243, les 10 échecs sont antérieurs (9 connus + `[jennika] tj005` deux
      Moonlighting, rouge aussi avec le `can_status.py` d'origine : plafond Cloaked = 1 du pack shredder).
- [x] Étape 8 bis : OUI (pose une carte d'état). Cas plateau `ui-app/src/board/tmnt-intensified-plateau.test.ts`
      (3 cas) ; sensibilité : `zones.ts` `attacheesPar.get(id)` rendu `.slice(0, 1)` → 2 cas ROUGES, restauré → 3/3.
Carte terminée : OUI (reste non prouvé : une partie réelle avec te201 en jeu, faute d'ensemble qui la contienne ;
lectures à confirmer listées dans intensified.md).

### ts001 : * Shredder (Villain, set Shredder)

- [x] Étape 2 : référence(s) : - `sk189b` (Queen Veranke I) : `AbilityFactory.AfterPhaseEnd(ForcedResponse, "Villain", op)` pour « After the villain phase ends » ; - `ThisCanHaveAdditionalCloaked(N)` (game/ability/factory/status.py), jumelle de `ThisCanHaveAdditionalTough` (colossus 32001a) : le maximum de cartes Cloaked est 1 + N (encart du scenario : « the Shredder can have more than one, depending on his villain stage »).
- [x] Étape 5 : mots-pièges : « up to 2 » = maximum, pas « toujours 2 » ; « give Shredder a cloaked status card » = UNE carte (le stade III en donne DEUX) ; « after the VILLAIN phase ends » (pas la phase des joueurs).
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 12*, ATK 2, SCH 1, Stage I.
- [x] Étape 7 : 4 cas sujet(s) : ts001 plafond : Shredder I porte AU PLUS 2 cartes Cloaked (la 3e est refusee) ; ts001 TEMOIN : un personnage ordinaire (le heros) ne porte qu'UNE carte Cloaked ; ts001 Forced Response : apres la phase du mechant, Shredder recoit UN Cloaked ; ts001 Forced Response au maximum : Shredder I a deja 2 Cloaked, la 3e n'est pas posee. Substitution : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (attache ou carte d'état Cloaked visible) : cas plateau `ui-app/src/board/shredder-plateau.test.ts`.
Carte terminée : OUI

### ts002 : * Shredder (Villain, set Shredder)

- [x] Étape 2 : référence(s) : `01095` (Rhino II : « Search the encounter deck and discard pile for X and reveal it », `Search.EncounterCard(include_discard_pile= True, ...)` puis `Reveal`) et `ts001` pour le reste. Bladed Armor est cherchee par card_id (`ts006`), jamais par le nom.
- [x] Étape 5 : mots-pièges : voir l'en-tete du script
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 14*, ATK 2, SCH 2, Stage II.
- [x] Étape 7 : 5 cas sujet(s) : ts002 plafond : Shredder II porte AU PLUS 3 cartes Cloaked ; ts002 Forced Response : apres la phase du mechant, Shredder II recoit UN Cloaked (pas deux) ; ts002 When Revealed (mise en place expert) : Bladed Armor est cherchee et s'attache a Shredder II ; ts002 When Revealed (passage au stade II, mode normal) : Bladed Armor vient du deck et s'attache ; ts002 When Revealed : Bladed Armor est AUSSI cherchee dans la DEFAUSSE de rencontre. Substitution : rouges 5/5.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (attache ou carte d'état Cloaked visible) : cas plateau `ui-app/src/board/shredder-plateau.test.ts`.
Carte terminée : OUI

### ts003 : * Shredder (Villain, set Shredder)

- [x] Étape 2 : référence(s) : `ts002` (la recherche) et `ts001` (le Response, avec DEUX cartes ici : « 2 cloaked status cards » = deux poses, chacune refusee si Shredder est deja au maximum).
- [x] Étape 5 : mots-pièges : voir l'en-tete du script
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 16*, ATK 3, SCH 2, Stage III.
- [x] Étape 7 : 4 cas sujet(s) : ts003 plafond : Shredder III porte AU PLUS 4 cartes Cloaked ; ts003 Forced Response : apres la phase du mechant, Shredder III recoit DEUX Cloaked ; ts003 Forced Response (un seul emplacement libre) : Shredder III a 3 Cloaked, il n'en recoit qu'UN ; ts003 When Revealed : Kuro Kabuto est cherche et s'attache a Shredder III. Substitution : rouges 4/4.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (attache ou carte d'état Cloaked visible) : cas plateau `ui-app/src/board/shredder-plateau.test.ts`.
Carte terminée : OUI

### ts004a : Clan of Shadows (MainScheme, set Shredder)

- [x] Étape 2 : référence(s) : `sp001a` (Heightened Threat : `WhenCardSetup("This", op)` sur une face A, puis `Find.FindAndReveal` pour « searches ... and reveals it »), `fne 60161a` (« Each player ... » a la mise en place), `Players.ForEachPlayer` (kang's wrath 11013b) pour « each player ».
- [x] Étape 5 : mots-pièges : « EACH player » (pas seulement le premier) ; « searches the encounter deck » SEULEMENT (pas la defausse : a la mise en place elle est vide de toute facon) ; « FOOT CLAN minion » = type sbire ET trait.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Stage 1A.
- [x] Étape 7 : 2 cas sujet(s) : ts004a Setup (solo) : le joueur cherche un sbire FOOT CLAN et le revele, engage avec lui ; ts004a Setup (2 joueurs) : CHAQUE joueur cherche et revele un sbire FOOT CLAN. Substitution : rouges 2/2.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### ts004b : Clan of Shadows (MainScheme, set Shredder)

- [x] Étape 2 : référence(s) : `sk179` (Shapeless Wastes : `AfterUnitBeDefeated( ForcedResponse, CardFinder(card_type=...), op)`), `01095` pour un When Revealed de complot ; `Cloak` du pack (fiche cloak.md).
- [x] Étape 5 : mots-pièges : « AFTER a FOOT CLAN minion IS DEFEATED » (Reponse forcee, apres) ; tout sbire FOOT CLAN, du deck OU modulaire, nemesis compris ; « on THIS scheme » (ce complot, pas « the main scheme » d'ailleurs) ; « Cloak Shredder » = le vilain Shredder, retrouve par card_id.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : StartingThreat 1*, TargetThreat 6*, EscalationThreat 1*, Stage 1B.
- [x] Étape 7 : 3 cas sujet(s) : ts004b When Revealed : Shredder recoit un Cloaked a la mise en place ; ts004b Forced Response : un sbire FOOT CLAN vaincu -> 1 menace sur 1B ; ts004b Forced Response, TEMOIN : un sbire SANS le trait FOOT CLAN vaincu -> aucune menace. Substitution : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### ts005a : Shredder's Wrath (MainScheme, set Shredder)

- [x] Étape 2 : référence(s) : `Players.ForEachPlayer` (11013b, ordre des joueurs), `Worlds.DiscardEncounterCards(n, effect)` (15004 / ho014 : « discard N cards from the top of the encounter deck ») et `Deck.FindTopmost` (56108 : « the topmost X in the encounter discard pile »).
- [x] Étape 5 : mots-pièges : « EACH player » discards 4 PUIS revele (par joueur, pas 4 x N d'abord) ; « topmost » = le plus recent sur la defausse ; si aucun sbire FOOT CLAN, rien ne se passe ; chaque joueur revele a SON propre compte.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Stage 2A.
- [x] Étape 7 : 3 cas sujet(s) : ts005a When Revealed (solo) : defausse 4 cartes du deck puis revele le sbire FOOT CLAN le plus haut de la defa ; ts005a When Revealed (2 joueurs) : CHAQUE joueur defausse 4 puis revele un sbire FOOT CLAN ; ts005a When Revealed, TEMOIN : aucun sbire FOOT CLAN dans la defausse -> rien n'est revele. Substitution : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### ts005b : Shredder's Wrath (MainScheme, set Shredder)

- [x] Étape 2 : référence(s) : `Faces.GiveStatus(Worlds.GetOnFieldEnemies(effect), ...)` (aoa 45092 pour GiveStatus Tough) ; `AfterUnitSchemeEnd` (bkw 08012) pour « after X schemes ». « If this scheme is completed, the players lose » : lu par le moteur sur le complot principal (aucun script, comme 01097b).
- [x] Étape 5 : mots-pièges : « EACH enemy » = vilain ET sbires (Worlds.GetOnFieldEnemies) ; « after SHREDDER schemes » : seulement quand Shredder manigance, pas un sbire.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : StartingThreat 2*, TargetThreat 10*, EscalationThreat 1*, Stage 2B.
- [x] Étape 7 : 3 cas sujet(s) : ts005b When Revealed : chaque ennemi (le vilain ET les sbires) recoit une carte Coriace ; ts005b Forced Response : apres que Shredder manigance -> UN Cloaked sur Shredder ; ts005b Forced Response, TEMOIN : un SBIRE qui manigance ne donne pas de Cloaked a Shredder. Substitution : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### ts006 : Bladed Armor (Attachment, set Shredder)

- [x] Étape 2 : référence(s) : - `01100` Enhanced Ivory Horn : `AttachToFaceWhenPutIntoPlay` + `PlayerActionToDiscardThis(HeroAction)` (« Spend ... -> discard this card ») ; - `gmw 16097` Weapon Mastery : `*GiveKeywordToAttached(CardFinder, retaliate=1)` ; - `bl009` Daywalker : `CostFunc.TakeDamage(1, "YourIdentity")` pour « take 1 damage -> » ; `gmw` Element Gun / `sm 27130` : `Cost("1")` = « spend 1 resource of any type ».
- [x] Étape 5 : mots-pièges : « IF there are NO cloaked status cards on Shredder » = condition pour OFFRIR l'action (Shredder porte 0 Cloaked) ; « take 1 damage » et « spend 1 resource » sont deux COUTS (avant le « -> ») ; « Shredder » retrouve par card_id (`IDS_SHREDDER`).  TODO-QUESTION (.planning/tmnt/shredder-questions.md, Q1) : « take 1 damage » sans sujet. Lecture retenue : l'IDENTITE du joueur qui paie prend 1 degat.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 3, ATK+ 1.
- [x] Étape 7 : 7 cas sujet(s) : ts006 Retaliate 1 : le heros qui attaque Shredder subit 1 degat ; ts006 Retaliate, TEMOIN : sans Bladed Armor, le heros n'encaisse aucune riposte ; ts006 ATQ +1 : Shredder frappe a 3 (ATQ 2 + 1) ; ts006 ATQ +1, TEMOIN : sans Bladed Armor Shredder frappe a 2 ; ts006 Action de heros OFFERTE quand Shredder n'a AUCUN Cloaked ; ts006 Action de heros NON OFFERTE tant que Shredder porte un Cloaked ; ts006 Action de heros : 1 degat a l'identite + 1 ressource -> Bladed Armor est defaussee. Substitution : rouges 5/7 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (attache ou carte d'état Cloaked visible) : cas plateau `ui-app/src/board/shredder-plateau.test.ts`.
Carte terminée : OUI

### ts007 : * Kuro Kabuto (Attachment, set Shredder)

- [x] Étape 2 : référence(s) : - `01100` / `ts006` : `AttachToFaceWhenPutIntoPlay`, `PlayerActionToDiscardThis` ; - `gmw nebula/__init__` : « boost : attach this card to the villain » = `message.AfterThisActivation(effect, op)` puis `this.AttachTo2(villain, effect)` (une carte de boost est rangee APRES sa resolution : attacher tout de suite serait ecrase) ; - `ra026` / `mf003` : `CostFunc.Discard("YourHandCards", range=(2, 2))` pour « discard 2 ca
- [x] Étape 5 : mots-pièges : « Shredder gains STEADY » (Steady, pas Stalwart) ; « after the VILLAIN phase ends » ; le boost attache, il ne se contente pas de reveler.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : SCH+ 1.
- [x] Étape 7 : 6 cas sujet(s) : ts007 Steady : Shredder gagne steady ; ts007 Steady, TEMOIN : Shredder I n'est pas steady de lui-meme ; ts007 Forced Response : apres la phase du mechant, Kuro Kabuto cloake Shredder EN PLUS de la Reponse du vilain ; ts007 Forced Response, TEMOIN : sans Kuro Kabuto, la phase du mechant ne donne qu'UN Cloaked ; ts007 Action de heros : defausser 2 cartes de la main -> Kuro Kabuto est defaussee ; ts007 Boost : apres l'activation, Kuro Kabuto s'attache a Shredder. Substitution : rouges 4/6 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (attache ou carte d'état Cloaked visible) : cas plateau `ui-app/src/board/shredder-plateau.test.ts`.
Carte terminée : OUI

### ts008 : Elite Guard (Minion, set Shredder)

- [x] Étape 2 : référence(s) : `01101` Hydra Mercenary (Guard, lu dans `desc`) ; Patrol idem (fiche patrol.md) ; `ts004b` pour « Cloak Shredder » ; `fne 60149` (boost « give ... a tough status card » : `Faces.GiveStatus([...], "Tough")`).
- [x] Étape 5 : mots-pièges : « Cloak SHREDDER » (le vilain, pas la garde) ; boost : « Give SHREDDER a tough » (pas « the activating enemy »).
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 3, ATK 2, SCH 1, Boost 1, Guard 1, Patrol 1.
- [x] Étape 7 : 3 cas sujet(s) : ts008 Guard + Patrol (desc) : la garde porte les deux mots-cles ; ts008 When Revealed : Shredder recoit un Cloaked ; ts008 Boost : Shredder recoit une carte Coriace. Substitution : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### ts010 : Foot Ninja (Minion, set Shredder)

- [x] Étape 2 : référence(s) : - `hood 24015` Griffin : « when defeated, shuffle into the encounter deck » = `WhenUnitBeDefeated` + `Faces.ShuffleAllTo([this], deck, effect)` (la defaite A LIEU : elle compte, contrairement a un « would be defeated ... instead » comme `an014`) ; - `hs042` / `aoa four_horsemen` : `message.AfterThisActivation(effect, op)` pour « after this activation resolves ».
- [x] Étape 5 : mots-pièges : « When Foot Ninja IS defeated » (pas « would ... instead ») : le sbire est vaincu PUIS melange ; « cloak THE VILLAIN » (le vilain, pas Shredder par nom) ; « THEM » = le sbire lui-meme.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 1, ATK 1, SCH 1, Boost 1.
- [x] Étape 7 : 4 cas sujet(s) : ts010 When Revealed : Foot Ninja se cloake lui-meme ; ts010 Forced Interrupt : vaincu, Foot Ninja est melange dans le deck de rencontre ; ts010 Forced Interrupt : la defaite COMPTE (1B recoit sa menace : le sbire est bien vaincu) ; ts010 Boost : apres l'activation, le vilain recoit un Cloaked. Substitution : rouges 4/4.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### ts012 : * Mongo (Minion, set Shredder)

- [x] Étape 2 : référence(s) : `01101` (Guard dans `desc`), `01099`/fiche retaliate.md (Retaliate dans `desc`) ; `core klaw 01123` Sonic Boom (boost « exhaust your hero » : `player.IsHero()` puis action sur `player.GetHero()`) ; `Faces.GiveStatus` pour Stunned.
- [x] Étape 5 : mots-pièges : « YOUR HERO » : le HEROS du joueur qui subit le boost ; en forme alter-ego il n'a pas de heros en jeu : rien ne se passe (meme lecture que Sonic Boom). Mongo n'a ni « When Revealed » ni autre capacite.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 4, ATK 2, SCH 0, Boost 1, Guard 1, Retaliate 1.
- [x] Étape 7 : 3 cas sujet(s) : ts012 Boost (forme heros) : le heros est etourdi ; ts012 Boost (forme alter-ego) : pas de heros en jeu, rien n'est etourdi ; ts012 Guard + Retaliate 1 (desc). Substitution : rouges 1/3 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### ts013 : Cloak of Shadows (Treachery, set Shredder)

- [x] Étape 2 : référence(s) : `Faces.GiveStatus(Worlds.GetOnFieldEnemies(effect), ...)` (`ts005b`) ; `cw 56108` Arrest Order (`Worlds.GetEncounterDiscardPile(effect) .FindTopmost(CardFinder2(trait, Minion))`) ; `hs042` (`AfterThisActivation`).
- [x] Étape 5 : mots-pièges : « EACH enemy » = vilain + TOUS les sbires en jeu ; « IF YOU are not engaged with a minion » : le joueur qui revele, lu APRES avoir pose les Cloaked ; « topmost » ; le boost cloake SHREDDER (pas « the villain »).
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : aucune valeur imprimee en `desc`.
- [x] Étape 7 : 3 cas sujet(s) : ts013 When Revealed : chaque ennemi est cloake (Shredder ET le sbire engage), pas de revelation si engage ; ts013 When Revealed : non engage -> revele le sbire FOOT CLAN le plus haut de la defausse ; ts013 Boost : apres l'activation, Shredder recoit un Cloaked. Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### ts015 : Disarming Assault (Treachery, set Shredder)

- [x] Étape 2 : référence(s) : `aoa four_horsemen` (`DoActivate(..., do_not_give_boost= True)` ; ici `DoAttackYou(property=AttackProperty(do_not_give_boost=True))`, l'attaque seule) ; `if_characters_damaged_by_this` (do_attack) pour « deals damage to YOU » ; `Caught Off Guard 01188` (`player.DiscardControlCards`).
- [x] Étape 5 : mots-pièges : « attacks YOU » (l'identite du joueur) ; « deals damage to YOU » : l'IDENTITE doit etre blessee (un allie qui encaisse ne compte pas) ; « a WEAPON you control » (trait WEAPON, jamais le trait KATANA seul) ; « if you cannot » absent : sans arme, rien ne se passe.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 1.
- [x] Étape 7 : 4 cas sujet(s) : ts015 When Revealed : Shredder attaque SANS boost, et l'arme du joueur est defaussee s'il y a degats ; ts015 When Revealed, TEMOIN : l'attaque ne fait AUCUN degat (Coriace) -> l'arme est gardee ; ts015 Boost : une arme du joueur est defaussee ; ts015 Boost, TEMOIN : un allie sans le trait WEAPON n'est PAS defausse. Substitution : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### ts017 : Shred (Treachery, set Shredder)

- [x] Étape 2 : référence(s) : `01187` Assault (le couple `WhenThisRevealed("Hero")` / `("Alter-Ego")`), `ts015` (attaque sans boost), `ts013` (boost « after this activation resolves, cloak Shredder »).
- [x] Étape 5 : mots-pièges : deux When Revealed DISTINCTS selon la forme (sans « surge » en alter-ego : il pose seulement la carte) ; « place a cloaked status card ON Shredder » = `Cloak`.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 2.
- [x] Étape 7 : 3 cas sujet(s) : ts017 When Revealed (alter-ego) : Shredder recoit un Cloaked, sans attaque ; ts017 When Revealed (heros) : Shredder attaque SANS boost, aucun Cloaked pose ; ts017 Boost : apres l'activation, Shredder recoit un Cloaked. Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### ts020 : Foot Rikugun (SideScheme, set Shredder)

- [x] Étape 2 : référence(s) : `hs222` (`AfterCardEnterPlay(ForcedResponse, CardFinder( trait=..., card_type=Minion), op)`, `message.trigger` = le sbire) ; RECETTES §2 « give X a tough status card. If you cannot » (lire le RETOUR, ne pas conditionner la cible).
- [x] Étape 5 : mots-pièges : « If YOU CANNOT » = Cloaked refuse (le sbire est DEJA Cloaked : un seul par personnage) ; « it » = le sbire qui entre ; une copie par exemplaire en jeu.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 2, Hazard 1, StartingThreat 2*.
- [x] Étape 7 : 3 cas sujet(s) : ts020 Forced Response : un sbire FOOT CLAN qui entre en jeu est cloake ; ts020 Forced Response (DEUX Rikugun) : le 2e ne peut pas cloaker, il donne une carte Coriace ; ts020 Forced Response, TEMOIN : un sbire SANS le trait FOOT CLAN n'est pas cloake. Substitution : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### ts022 : Throne of the Jōnin (SideScheme, set Shredder)

- [x] Étape 2 : référence(s) : `01095` (Search.EncounterCard puis Reveal) ; `mts 21188` (le joueur qui revele cherche) ; `PlaceThreatOnSchemes([this], "2*", effect)` (`ts004b` pour poser de la menace sur CE complot).
- [x] Étape 5 : mots-pièges : « a FOOT CLAN ATTACHMENT » (type Attachment ET trait : Bladed Armor, Kuro Kabuto, Kira no Ken en font partie) ; « If you CANNOT » = aucune trouvee ; le surplus de menace est « 2 par joueur » en PLUS de la menace de depart.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 2, Crisis 1, StartingThreat 1*.
- [x] Étape 7 : 4 cas sujet(s) : ts022 When Revealed : cherche un attachement FOOT CLAN dans le deck et le revele (Bladed Armor) ; ts022 When Revealed : cherche AUSSI dans la defausse ; ts022 If you cannot : aucun attachement FOOT CLAN -> 2[per_hero] menaces en plus (1 + 2 = 3, solo) ; ts022 If you cannot (2 joueurs) : 2 par joueur = 4 en plus de la menace de depart (2) = 6. Substitution : rouges 4/4.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### ts101 : * Karai (Minion, set Chunin)

- [x] Étape 2 : référence(s) : `tl015` * Karai (nemesis de Leonardo) : MEME texte, MEME montage (`WhenThisRevealed`, `WhenUnitBeDefeated(WhenDefeated, "This")`, detournement du rangement du boost).
- [x] Étape 5 : mots-pièges : « Cloak KARAI » (elle-meme) vs « Cloak THE VILLAIN » (When Defeated) ; « to the FIRST player » (pas celui qui revele).
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 2, ATK 1, SCH 1.
- [x] Étape 7 : 4 cas sujet(s) : ts101 When Revealed : Karai se cloake elle-meme ; ts101 When Defeated : le VILAIN recoit un Cloaked ; ts101 Boost : Karai est donnee face cachee au PREMIER joueur ; ts101 Boost puis revelation : Karai donnee, revelee dans le meme round, entre en jeu cloakee (pas de boucle). Substitution : rouges 3/3.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (attache ou carte d'état Cloaked visible) : cas plateau `ui-app/src/board/shredder-plateau.test.ts`.
Carte terminée : OUI

### ts102 : * Ocho (Minion, set Chunin)

- [x] Étape 2 : référence(s) : `web_of_deceit wd110` Tiger (`UnitAttackGainKeyword("This", piercing=True)`) ; `01095` (Search.EncounterCard + Reveal) ; Guard lu dans `desc`.
- [x] Étape 5 : mots-pièges : « Karai » cherchee par card_id (`IDS_KARAI`) ; « reveal HER » : si Karai n'est pas trouvee, rien ; le boost ne cherche pas dans l'ensemble des cartes du jeu mais dans le deck ET la defausse de rencontre.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 4, ATK 2*, SCH 2, Boost 1, Guard 1.
- [x] Étape 7 : 4 cas sujet(s) : ts102 Guard (desc) + attaques PERCANTES : Ocho blesse un heros Coriace et lui retire sa carte Coriace ; ts102 TEMOIN : un sbire sans piercing (Hydra, ATQ 1) est absorbe par la carte Coriace ; ts102 Boost : cherche Karai dans le deck et la revele ; ts102 Boost : Karai-NEMESIS de Leonardo (tl015) est AUSSI Karai : trouvee par son card_id. Substitution : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### ts103 : * Kira no Ken (Attachment, set Chunin)

- [x] Étape 2 : référence(s) : `01100` (`AttachToFaceWhenPutIntoPlay`) avec son `if_cannot_operation` (« if you cannot attach ... ») pour la branche « Karai n'est pas en jeu » ; `ts102` (la recherche de Karai) ; `UnitAttackGainKeyword` pour « attacks gain piercing ».
- [x] Étape 5 : mots-pièges : « Karai » = ts101 OU tl015 (meme personnage, `IDS_KARAI`) ; « Then, attach this card to HER » : apres la revelation ; si Karai reste introuvable, la carte n'a nulle part ou s'attacher et est defaussee.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 2, ATK+ 1*.
- [x] Étape 7 : 5 cas sujet(s) : ts103 Karai en jeu : Kira no Ken s'attache a elle ; ts103 Karai absente : elle est cherchee dans le deck, revelee, puis Kira no Ken s'attache a elle ; ts103 Karai introuvable : Kira no Ken est defaussee ; ts103 ATQ +1 et attaques PERCANTES : Karai ATQ 1 +1 perce la Coriace du heros (2 degats) ; ts103 TEMOIN : Karai SANS Kira no Ken (ATQ 1) est absorbee par la Coriace. Substitution : rouges 3/5 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (attache ou carte d'état Cloaked visible) : cas plateau `ui-app/src/board/shredder-plateau.test.ts`.
Carte terminée : OUI

### ts104 : Doroppuin (Treachery, set Chunin)

- [x] Étape 2 : référence(s) : `cw 56108` (`GetEncounterDiscardPile().FindTopmost`), `01188` (`ThisCardGainSurge` pour « otherwise, this gains surge ») ; `wd110` Tiger pour « if this activation is an attack, it gains piercing ».
- [x] Étape 5 : mots-pièges : « the topmost MINION » (n'importe quel sbire, pas seulement FOOT CLAN) ; « Otherwise » = la defausse n'a aucun sbire ; boost : seulement si l'activation EST une attaque (`during_attack=True`).
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 1.
- [x] Étape 7 : 4 cas sujet(s) : ts104 When Revealed : revele le sbire le plus haut de la defausse (n'importe quel sbire) ; ts104 Otherwise : defausse sans sbire -> la carte gagne surge (la carte suivante est revelee) ; ts104 Boost (attaque) : l'attaque gagne PIERCING -> Coriace retiree, degats subis ; ts104 Boost, TEMOIN : sans piercing (boost Elite Guard), la Coriace absorbe tout. Substitution : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### ts201 : * Bebop (Minion, set Foot Goon Squad)

- [x] Étape 2 : référence(s) : `wd110` Tiger (`UnitAttackGainKeyword("This", piercing= True)` + boost piercing) ; `tl015` (detournement du rangement du boost vers les cartes distribuees : `FaceCacheeAuPremierJoueur`) ; Toughness lu dans `desc`.
- [x] Étape 5 : mots-pièges : « Otherwise » = l'activation n'est PAS une attaque (une manigance) ; « to the FIRST player » ; `Toughness` : carte robuste a l'entree.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 4, ATK 2*, SCH 0, Toughness 1.
- [x] Étape 7 : 4 cas sujet(s) : ts201 Bebop : Toughness (desc) et attaques PERCANTES (Coriace du heros percee) ; ts201 Boost (attaque) : l'attaque de Shredder gagne piercing ; ts201 Boost (manigance, alter-ego) : Bebop est donne face cachee au premier joueur ; ts201 Boost (attaque), TEMOIN : en attaque Bebop n'est PAS distribue. Substitution : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (attache ou carte d'état Cloaked visible) : cas plateau `ui-app/src/board/shredder-plateau.test.ts`.
Carte terminée : OUI

### ts202 : * Bludgeon (Minion, set Foot Goon Squad)

- [x] Étape 2 : référence(s) : `gob 02038` Scorpion / `mts 21086` Supergiant (`AfterUnitAttackAndDamageUnit(ForcedResponse, "This", "Character", op, target_in_play=True)`) ; `core klaw 01123` Sonic Boom (boost « exhaust your hero » : `player.IsHero()` puis `Faces.ExhaustAll`).
- [x] Étape 5 : mots-pièges : « attacks AND DAMAGES » (pas une attaque absorbee par Toughness) ; « that character » = le blesse (identite ou allie) ; « your HERO » (rien en alter-ego).
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 3, ATK 2, SCH 2, Boost 1, Quickstrike 1.
- [x] Étape 7 : 3 cas sujet(s) : ts202 Bludgeon : apres avoir attaque ET blesse un personnage, il l'epuise ; ts202 Bludgeon, TEMOIN : attaque absorbee par la Coriace -> le heros n'est PAS epuise ; ts202 Boost : le heros est epuise. Substitution : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### ts203 : * Hun (Minion, set Foot Goon Squad)

- [x] Étape 2 : référence(s) : `gob 02038` Scorpion (le Response) ; `thor 06029` Frost Giant (boost « if this attack deals damage to a character, stun that character » ; ici `IfUnitTakeDamageFromThisAttack`, voir le commentaire dans le script).
- [x] Étape 5 : mots-pièges : « IF THIS ACTIVATION deals damage » : une manigance n'en inflige pas (le boost ne fait alors rien) ; « a character » (identite ou allie, pas seulement vous) ; Toughness lu dans `desc`.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 3, ATK 2, SCH 1, Boost 1, Toughness 1.
- [x] Étape 7 : 4 cas sujet(s) : ts203 Hun : apres avoir attaque ET blesse un personnage, il l'etourdit ; ts203 Hun, TEMOIN : attaque absorbee par la Coriace -> pas d'etourdissement ; ts203 Boost : si l'activation (attaque) fait des degats, le personnage est etourdi ; ts203 Boost, TEMOIN : l'attaque ne fait aucun degat (Coriace) -> pas d'etourdissement. Substitution : rouges 2/4 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### ts204 : * Koya (Minion, set Foot Goon Squad)

- [x] Étape 2 : référence(s) : `aoa four_horsemen` (`this.HealthUnits([villain], 2, effect)`), `hs160` / `ts004b` (`PlaceThreatOnSchemes("MainScheme", 1, effect)`) ; Incite et Quickstrike lus dans `desc`.
- [x] Étape 5 : mots-pièges : « heal 2 damage FROM THE VILLAIN » (pas d'elle-meme) ; « place 1 threat ON THE MAIN SCHEME » ; les deux effets du boost, dans cet ordre.
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 2, ATK 1, SCH 2, Incite 1, Quickstrike 1.
- [x] Étape 7 : 2 cas sujet(s) : ts204 Koya : When Revealed, soigne 2 degats du vilain (+ Incite 1 : 1 menace sur le complot principal) ; ts204 Boost : 1 menace sur le complot principal ET 2 degats soignes du vilain. Substitution : rouges 2/2.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### ts205 : * Rocksteady (Minion, set Foot Goon Squad)

- [x] Étape 2 : référence(s) : `ts201` (meme montage, overkill au lieu de piercing) ; `fne 60149` Rhino (`UnitAttackGainKeyword("This", overkill=True)`) ; Steady et Quickstrike lus dans `desc`.
- [x] Étape 5 : mots-pièges : voir l'en-tete du script
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 4, ATK 2*, SCH 0, Boost 1, Steady 1, Quickstrike 1.
- [x] Étape 7 : 5 cas sujet(s) : ts205 Rocksteady : attaque a overkill -> l'excedent frappe le heros (Maria Hill HP 2 - 1 degat, ATQ 2 : 1 en t ; ts205 TEMOIN : Mongo (ATQ 2, sans overkill) tue Maria Hill sans excedent sur le heros ; ts205 Boost (attaque) : l'attaque de Shredder gagne overkill (ATQ 2 + 1 icone = 3 contre Maria Hill HP 2) ; ts205 Boost (attaque), TEMOIN : meme position avec un boost sans overkill (Foot Soldiers) : pas d'exces ; ts205 Boost (manigance) : Rocksteady est donne face cachee au premier joueur. Substitution : rouges 3/5 ⚠ un cas reste vert sans module.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (attache ou carte d'état Cloaked visible) : cas plateau `ui-app/src/board/shredder-plateau.test.ts`.
Carte terminée : OUI

### ts206 : Send Out the Goons (SideScheme, set Foot Goon Squad)

- [x] Étape 2 : référence(s) : `hood 24018` Brothers Grimm (`Worlds.DiscardEncounterCardsUntil( effect, card_type=..., trait=...)` puis `face.Reveal(player, effect)`).
- [x] Étape 5 : mots-pièges : « discard until a BRUTE MINION IS DISCARDED » (type sbire ET trait) ; « reveal THAT minion » ; sans BRUTE dans le deck, tout le deck est defausse (borne : le moteur melange la defausse une fois, `DiscardUntil`).
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 3, Crisis 1, StartingThreat 1*.
- [x] Étape 7 : 1 cas sujet(s) : ts206 When Revealed : defausse le deck jusqu'a un sbire BRUTE, qu'elle revele. Substitution : rouges 1/1.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

### ts301 : Foot Assassin (Minion, set Shadow of the Foot)

- [x] Étape 2 : référence(s) : `ts010` (« Cloak <lui-meme> » au When Revealed) ; `AfterUnitAttackEnd` (RECETTES §1 : « After you attack an enemy », ici avec « This » comme attaquant) pour « after Foot Assassin attacks » ; Quickstrike dans `desc`.
- [x] Étape 5 : mots-pièges : « AFTER Foot Assassin attacks » (Reponse forcee, apres CHAQUE attaque, meme sans degats) ; « cloak THEM » = elle-meme ; un seul Cloaked a la fois (plafond).
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 1, ATK 1, SCH 1, Boost 2, Quickstrike 1.
- [x] Étape 7 : 2 cas sujet(s) : ts301 When Revealed : Foot Assassin se cloake elle-meme ; ts301 Forced Response : apres avoir attaque, Foot Assassin se cloake. Substitution : rouges 2/2.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### ts303 : Foot Soldiers (Minion, set Shadow of the Foot)

- [x] Étape 2 : référence(s) : `tl016` Foot Soldiers (nemesis de Leonardo : MEME texte, `Cloak(effect, this)`) ; `ts010`.
- [x] Étape 5 : mots-pièges : voir l'en-tete du script
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : HP 1, ATK 1, SCH 1, Boost 1.
- [x] Étape 7 : 1 cas sujet(s) : ts303 When Revealed : Foot Soldiers se cloake lui-meme. Substitution : rouges 1/1.
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : OUI (pose un statut / une carte face cachée) : couvert par les cas génériques du plateau (`effets-statuts`, `tmnt-leonardo-plateau`, `shredder-plateau`) ; aucun rendu propre à la carte.
Carte terminée : OUI

### ts305 : Foothold (SideScheme, set Shadow of the Foot)

- [x] Étape 2 : référence(s) : `ability_link` vers le core : AUCUN module propre (voir ci-dessous)
- [x] Étape 5 : mots-pièges : memes mots que le core (texte verifie sur le scan)
- [x] Étape 6 : nombres lus sur le scan = `cards.json` : Boost 3, Crisis 1, StartingThreat 3, Hinder 1*, Incite 2.
- [ ] Étape 7 : 2 cas sujet(s) : ts305 Foothold : menace de depart 3 (fixe) + Hinder 1[per_hero] ; ts305 Foothold (2 joueurs) : menace 3 + Hinder 1 par joueur (2) = 5. Substitution : voir la section communs (habillage par ability_link).
- [x] Étape 7 bis : limite imprimée NON (aucune carte du pack ne porte « Limit »).
- [x] Étape 8 : autoplay, voir communs (grep tracebacks = 0).
- [x] Étape 8 bis : NON (ne change que des chiffres ou révèle une carte déjà gérée).
Carte terminée : OUI

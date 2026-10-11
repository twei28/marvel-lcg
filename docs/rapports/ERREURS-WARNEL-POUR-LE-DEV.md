# Warnel Chawpiovs : erreurs de scripts trouvées et correctifs proposés

Document destiné au développeur de Warnel Chawpiovs. Il regroupe les erreurs trouvées en relisant les scripts de cartes (`Sets/SetScripts_*.json`) face au texte imprimé, au code du moteur Godot (`src/`) et, quand c'était possible, à une seconde implémentation indépendante (le moteur Narwhal, Python).

## Comment lire ce document

- **Erreurs prouvées** : le texte imprimé, le JSON et le code du moteur ont été lus et ils se contredisent. Chaque fiche donne un correctif JSON à coller.
- **Cartes incertaines** : un doute réel mais non prouvé, à tester en jeu. Ce ne sont pas des erreurs confirmées.
- Les effets de campagne ne sont pas détaillés.

## Limites (à lire avant d'appliquer)

- Audit **statique** : aucun correctif n'a été exécuté dans Godot. Les correctifs de type renommage de clé sont sûrs. Ceux qui ajoutent ou restructurent des tâches sont à tester en jeu, surtout quand la fiche l'indique.
- Les numéros de ligne sont approximatifs. Le nom de la carte et la clé JSON sont fiables.
- Les mentions « Référence Narwhal » sont absentes ou partielles pour certains packs (core, trors, une partie de sm et winter). Ce n'est pas une confirmation.
- Pattern global : le moteur **ignore en silence** toute clé inconnue. Une faute de frappe dans une clé supprime donc l'effet ou élargit le filtre, sans message d'erreur. Voir l'annexe en fin de document, avec la liste des clés fautives.
- Suggestion : un contrôle au chargement des scripts qui signale les clés absentes des constantes `KEY_*` de `ScriptProperties.gd` détecterait toute cette famille d'erreurs.

## Packs couverts

aos, next_evol, sm, aoa, mts, mut_gen, gmw, core, trors, ironheart, spiderham, drs, psylocke, ncrawler, winter, vision, valk, cyclops, wsp, scw, wolv, stld, gambit, phoenix, ant, nebu, warm, gam, cap, msm, thor, qsv, bkw, drax, vnm, hlk, red_hulk.


---

## Audit Warnel, lot 01 : Sets/SetScripts_aos.json

Moteur lu : src/wc/ScriptingEngine/ScriptingEngine.gd, src/wc/CardTemplate.gd, src/wc/WCUtils.gd, src/core/ScriptingEngine/ScriptProperties.gd, src/core/ScriptingEngine/ScriptObject.gd, src/wc/GameData.gd.
Les numéros de ligne du JSON sont approximatifs. Le fichier contient des virgules finales (tolérées par Godot, retirées pour l'analyse).

## Erreurs prouvées

### [aos] Rapido (50099)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Rapido's attacks gain ranged and deal indirect damage. »
- **Ce que fait le script Warnel** : SetScripts_aos.json, clé "Rapido" (~l.7546) : `"attacks_gain": {"__trigger__": "self", "__tags__": "piercing"}`. L'indirect damage est bien donné par `attack_indirect_damage`, mais le mot-clé accordé est piercing et non ranged.
- **Pourquoi c'est faux** : ScriptingEngine.gd, deal_damage / receive_damage : `script.has_tag("piercing")` retire les jetons tough de la cible (l.~1092 et l.~1178). Le tag `ranged` n'est lu qu'à l'endroit de la riposte (l.~1513, `if script.has_tag("ranged")` : pas de Retaliate). Résultat : les attaques de Rapido ignorent tough (non imprimé) et déclenchent Retaliate (contraire du texte). D'autres sets utilisent bien `"__tags__": "ranged"` (SetScripts_mts.json l.1955, SetScripts_next_evol.json l.7648).
- **Correctif proposé** :
```json
"attacks_gain": {
    "__trigger__": "self",
    "__tags__": "ranged"
},
```
- **Référence Narwhal** : aos/batrocs_brigade/50099.py, `UnitAttackGainKeyword("This", ranged=True, indirect_damage=True)`.

### [aos] Rescued Captive (50091)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Action: Exhaust Rescued Captive → remove 1[per_hero] threat from the main scheme. »
- **Ce que fait le script Warnel** : clé "Rescued Captive" (~l.7708), `manual` : `{"name": "remove_threat", "amount": 1, "subject": "main_scheme"}`. Retire toujours 1 menace, quel que soit le nombre de joueurs.
- **Pourquoi c'est faux** : le suffixe `p` (par héros) n'est interprété que dans les chaînes (ScriptObject.gd l.~865 : `value_str.ends_with("p")` multiplie par `cfc.count_players()`). Un entier brut n'est pas multiplié, et remove_threat (ScriptingEngine.gd l.2931) n'applique aucun facteur par héros. D'autres cartes du même fichier écrivent bien `"1p"`.
- **Correctif proposé** :
```json
{"name": "remove_threat", "amount": "1p", "subject": "main_scheme"}
```
- **Référence Narwhal** : aos/batroc/50091.py, `RemoveThreatFromSchemes(effect.targets, "1*", effect)`.

### [aos] Eyepatch Camera (50043)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Interrupt: When any amount of threat would be placed on the main scheme, discard Eyepatch Camera → place up to 3 of that threat on your suit form upgrade instead. »
- **Ce que fait le script Warnel** : clé "Eyepatch Camera" (~l.3745), `interrupt_add_threat` avec trois options (1, 2, 3 Threat). Chacune contient constraints, prevent, mod_tokens ; aucune ne contient de `discard` de la carte (le JSON de la clé ne contient pas le mot "discard").
- **Pourquoi c'est faux** : l'étiquette `hero_interrupt` (ScriptingEngine.gd, `_tags_to_tags` l.~3942) ne fait que mapper vers `hero_form` + `interrupt_ability`, elle n'ajoute aucune défausse. Les autres cartes du fichier qui disent « discard X → » écrivent un `{"name": "discard", "subject": "self"}` explicite (cf. Prism Dust). Le joueur peut donc réutiliser indéfiniment l'Eyepatch Camera.
- **Correctif proposé** : ajouter dans chacune des trois options, juste après le `constraints` :
```json
{"name": "discard", "subject": "self", "is_cost": true}
```
- **Référence Narwhal** : aos/nick_fury/50043.py, `.SetCostFunc(CostFunc.Discard("This"))`.

### [aos] Hard Sound Bindings (50145)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Forced Interrupt: When you would attack, discard Hard Sound Bindings instead. Then, you are stunned. »
- **Ce que fait le script Warnel** : clé "Hard Sound Bindings" (~l.4574), `interrupt_attack` : `prevent` de l'attaque puis `mod_tokens stunned +1` sur `host`. Pas de défausse (le JSON de la clé ne contient pas "discard").
- **Pourquoi c'est faux** : rien dans le moteur ne défausse un attachement après un interrupt ; la carte reste attachée et empêche toute attaque future, définitivement, avec un stun à chaque tentative.
- **Correctif proposé** (le stun passe par `my_identity` pour ne pas dépendre de l'hôte après la défausse) :
```json
"interrupt_attack": {
    "trigger": "host",
    "board": [
        {"name": "prevent", "subject": "interrupted_event"},
        {"name": "discard", "subject": "self"},
        {"name": "mod_tokens", "subject": "my_identity", "modification": 1, "token_name": "stunned"}
    ]
},
```
- **Référence Narwhal** : aos/hard_sound/50145.py (`Faces.DiscardAll([this], effect)` puis `Faces.GiveStatus([identity], "Stunned", effect)`).

### [aos] Concentrated Fire (50037)
- **Gravité** : bloquante (une des deux options)
- **Certitude** : prouvée par le code
- **Texte imprimé** : « If this attack defeats an enemy, choose: • Place threat on your suit form upgrade equal to that enemy's printed SCH. • Change to Stealth suit form. »
- **Ce que fait le script Warnel** : clé "Concentrated Fire" (~l.2588), option "Change to Stealth" : `{"name": "change_form", "form_name": "Assault", "subject": "my_identity"}`.
- **Pourquoi c'est faux** : CardTemplate.gd `change_form_script_replacement` (~l.2888) cherche la carte nommée `form_name` parmi les formes disponibles en set_aside et change vers elle. "Assault" est donc la forme visée : depuis Stealth, on passe à Assault ; depuis Assault, la forme n'est pas dans set_aside et le changement échoue (return {}). Dans aucun cas on ne va vers Stealth.
- **Correctif proposé** :
```json
"Change to Stealth": [
    {"name": "change_form", "form_name": "Stealth", "subject": "my_identity"}
]
```
- **Référence Narwhal** : aos/nick_fury/50037.py, `ChangeToStealthSuitForm(initiator, effect)`.

### [aos] Covert Surveillance (50038)
- **Gravité** : bloquante (changement de forme absent) et partielle (condition manquante)
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Remove 2 threat from a scheme. If you are in Stealth suit form, you may place that threat on your suit form upgrade. Otherwise, you may change to Stealth suit form. »
- **Ce que fait le script Warnel** : clé "Covert Surveillance" (~l.2842), `thwart_happened` : option "Move Threat on suit form" sans aucune condition ; option "Change to Stealth" qui ne contient qu'un `constraints` (`!card_is_in_play Stealth`) et aucun `change_form`.
- **Pourquoi c'est faux** : la seconde option ne fait rien (un constraints en is_cost ne modifie pas la forme, cf. CardTemplate.gd `change_form_script_replacement` pour ce qui change réellement la forme). La première option est offerte même hors Stealth, alors que le texte la réserve à la forme Stealth.
- **Correctif proposé** :
```json
"thwart_happened": {
    "event_filters": {"secondary_source": "self"},
    "all": {
        "Move Threat on suit form": [
            {"name": "constraints", "is_cost": true, "constraints": [
                {"func_name": "card_is_in_play", "func_params": {"card_name": "Stealth"}}
            ]},
            {"name": "mod_tokens", "modification": "trigger_details_amount_removed", "token_name": "threat",
             "subject": "boardseek", "filter_state_seek": [{"filter_same_controller": true, "filter_properties": {"form_family": "suit"}}]}
        ],
        "Change to Stealth": [
            {"name": "constraints", "is_cost": true, "constraints": [
                {"func_name": "!card_is_in_play", "func_params": {"card_name": "Stealth"}}
            ]},
            {"name": "change_form", "form_name": "Stealth", "subject": "my_identity"}
        ]
    }
}
```
- **Référence Narwhal** : aos/nick_fury/50038.py (`initiator.form.IsInSuitForm("Stealth")` puis `ChangeToStealthSuitForm`).

### [aos] Extract Captives - 3A (50089a)
- **Gravité** : bloquante
- **Certitude** : prouvée par le texte seul (à confirmer en jeu), `remove_threat` "all" est utilisé ailleurs dans le fichier (~l.642)
- **Texte imprimé** : « If the Alert Level is on its High side, deal each player 1 facedown encounter card. Otherwise, remove all threat from Alert Level and flip it to its High side. In either case, in expert mode, place 2[per_hero] threat on Alert Level. »
- **Ce que fait le script Warnel** : clé "Extract Captives - 3A", `reveal`, branche `else` : `add_threat subject "Alert Level" amount "2p"` puis `flip_doublesided_card`. Le `post_reveal` ajoute déjà 2p en mode expert.
- **Pourquoi c'est faux** : la branche « Otherwise » ajoute 2 menaces par héros en mode normal aussi, et ne retire jamais la menace existante. Le texte demande de retirer toute la menace.
- **Correctif proposé** :
```json
"else": [
    {"name": "remove_threat", "amount": "all", "subject": "Alert Level"},
    {"name": "flip_doublesided_card", "subject": "Alert Level"}
]
```
- **Référence Narwhal** : aos/batroc/50089a.py (`Faces.RemoveTokensOn([env], "All", 'threat', effect)`).

### [aos] Holding Cell (50105a, 50106a, 50107a, 50108a : quatre entrées identiques)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Forced Interrupt: When the last lock counter is removed from here, flip this card and put Flying Inhuman into play under any player's control. » (idem Psionic, Strong, etc. selon la variante)
- **Ce que fait le script Warnel** : clés "Holding Cell #50105a/106a/107a/108a" (~l.4713 à 4965), `card_token_modified` : `"filter_count": 0, "filter_token_name": "threat"`. Les compteurs de la carte sont pourtant des jetons `lock` (self_moved_to_board : `token_name "lock"`).
- **Pourquoi c'est faux** : ScriptProperties.gd (~l.1449) compare `filter_token_name` au nom du jeton réellement modifié (`trigger_details["token_name"]`). Le jeton qui tombe à 0 est `lock`, jamais `threat` : le déclencheur ne part jamais, l'Inhumain n'est jamais libéré, la carte ne se retourne pas.
- **Correctif proposé** (les quatre entrées) :
```json
"card_token_modified": {
    "trigger": "self",
    "filter_count": 0,
    "filter_token_name": "lock",
    ...
}
```
- **Référence Narwhal** : aos/modok/__init__.py, `HoldingCell(cost)` (aos/modok/50105a.py).

### [aos] Grant Ward (50022)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Forced Response: After you reveal a treachery, you may spend a [mental] resource. If you do not, take damage equal to Grant Ward's ATK and remove Grant Ward from the game. »
- **Ce que fait le script Warnel** : clé "Grant Ward" (~l.5290), `reveal_encounter` sans aucun filtre de type.
- **Pourquoi c'est faux** : le trigger `reveal_encounter` (GameData.gd, `reveal_encounter()` et `_script_executed_from_stack`) est émis pour toute carte d'encounter révélée (minion, side scheme, environnement, trahison). Les autres cartes du jeu qui visent les trahisons ajoutent `"filter_state_trigger": [{"filter_properties": {"type_code": "treachery"}}]` (SetScripts_aos.json ~l.5372, gmw ~l.3278, mts ~l.1812). Grant Ward punit donc le joueur à chaque révélation.
- **Correctif proposé** : ajouter dans `reveal_encounter` :
```json
"filter_state_trigger": [{"filter_properties": {"type_code": "treachery"}}],
```
- **Référence Narwhal** : aos/50022.py, `AfterPlayerRevealCard(AbilityType.ForcedResponse, "You", Treachery, grant_ward)`.

### [aos] Prism Dust (50052)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Response (attack): After a minion enters play, discard Prism Dust → confuse that minion and deal 2 damage to it. »
- **Ce que fait le script Warnel** : clé "Prism Dust" (~l.7140), `response_card_moved_to_board` : `filter_properties: {"code_type": "minion"}`.
- **Pourquoi c'est faux** : `code_type` n'existe nulle part dans src ni dans les définitions de cartes (propriété standard : `type_code`). ScriptProperties.gd `check_properties` compare via `card.get_property("code_type")` qui renvoie vide : le filtre ne correspond jamais, la réponse n'est jamais offerte.
- **Correctif proposé** :
```json
"filter_state_trigger": [{"filter_properties": {"type_code": "minion"}}],
```
- **Référence Narwhal** : aos/50052.py.

### [aos] Leaping Kick (50096)
- **Gravité** : bloquante (cas "aucun allié")
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Revealed (Hero): Batroc attacks the ally with the most remaining hit points. This attack gains overkill. If there were no allies in play, Batroc attacks you. »
- **Ce que fait le script Warnel** : clé "Leaping Kick" (~l.5640), branche `else` : `{"name": "enemy_attacks", "subject": "Batroc"}`.
- **Pourquoi c'est faux** : aucune fonction `enemy_attacks` n'existe dans ScriptingEngine.gd (existent : `enemy_attacks_you` l.2153, `enemy_attacks_engaged_hero` l.2222). Le moteur appelle `call(script.script_name, script)` (ScriptingEngine.gd l.563) : l'appel échoue et Batroc n'attaque pas. C'est la seule occurrence de ce nom dans tous les Sets.
- **Correctif proposé** :
```json
"else": [
    {"name": "enemy_attacks_you", "subject": "Batroc"}
]
```
- **Référence Narwhal** : aos/batroc/50096.py.

### [aos] Justice, Like Lightning (50131a)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Each player reveals a random set-aside Thunderbolt minion. »
- **Ce que fait le script Warnel** : clé "Justice, Like Lightning" (~l.7050), `reveal` : `"subject": "tutor_and_choose"` sur les minions Thunderbolt du set_aside.
- **Pourquoi c'est faux** : WCUtils.gd (~l.719) transforme `tutor_and_choose` en `needs_selection: true, selection_count: 1` : le joueur choisit le minion. Le texte impose un tirage aléatoire (Down but Not Out, dans le même fichier, utilise `subject_index: random`).
- **Correctif proposé** :
```json
{"name": "reveal_encounter", "subject": "tutor", "subject_index": "random", "src_container": "set_aside",
 "filter_state_tutor": [{"filter_properties": {"type_code": "minion"}, "filter_properties2": {"trait_thunderbolt": 1}}]}
```
- **Référence Narwhal** : aos/thunderbolts/50131a.py (`RevealRandomSetasideThunderboltMinion`).

### [aos] Thunderbolt Backup (50131b)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu). Pas de définition dans SetDefinition_aos.json, texte lu dans cards.json de Narwhal.
- **Texte imprimé** : « Forced Interrupt: When the round ends, attach the Thunderbolt minion with the most damage here, swapping it ... Heal 1[per_hero] damage from attached minion. In expert mode, heal 1[per_hero] additional damage ... and give it a tough status card. »
- **Ce que fait le script Warnel** : clé "Thunderbolt Backup", `round_ended` se termine par `{"name": "sequence", "sequence_ability": "do_heal,"}` (virgule dans la chaîne), alors que la clé définie est `"do_heal"`.
- **Pourquoi c'est faux** : `sequence` (ScriptingEngine.gd l.3446 -> GameData.start_play_sequence) utilise la chaîne comme nom de déclencheur ; `"do_heal,"` n'existe pas, donc ni le soin ni le tough ne sont appliqués.
- **Correctif proposé** : `"sequence_ability": "do_heal"`.
- **Référence Narwhal** : aos/thunderbolts/50131b.py.

### [aos] Intelligence (50051)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « look at each encounter card dealt to each player and the top card of the encounter deck. You may swap any number of those cards. »
- **Ce que fait le script Warnel** : clé "Intelligence" (~l.4750) : `"TODO": "swap"`, et `response_card_moved_to_pile` ne fait que `view_card`.
- **Pourquoi c'est faux** : le TODO marque l'échange comme non codé ; seule la consultation existe.
- **Correctif proposé** : pas de JSON sûr sans fonction moteur d'échange de cartes encounter (aucune ne figure dans ScriptingEngine.gd). Il faut une `custom_script` GDScript (src/wc/cards/CustomScripts.gd) ou une nouvelle tâche `swap_cards` déplaçant des cartes entre `encounters_facedown` et `deck_villain`.
- **Référence Narwhal** : n/a (non vérifié).

## Totaux

- Cartes auditées : 218 (entrées de cartes de SetScripts_aos.json, hors la clé `_macros`)
- Erreurs prouvées : 14 cartes (17 entrées, car Holding Cell en compte 4)
- Cartes OK : 176 (218 moins 17 erreurs moins 25 incertaines)
- Effets de campagne non gérés (non listés) : 0 repéré dans ce fichier (le code de campagne n'a pas été recherché exhaustivement)

## Cartes incertaines (non prouvées, à tester en jeu)

- Divided Loyalties : « attack, thwart, or defend with an ally » ; le `script_alterants` ne couvre que attack et thwart. Le coût de défense passe peut-être par un autre mécanisme du moteur, non trouvé.
- Hinder sans macro `hinder` : Aerial Dogfight, Mad Science, Psionic Enhancement, Destroy Evidence, Automated Defenses. Le mot-clé est peut-être géré à partir du texte par le moteur, non vérifié.
- Authority, Blackmail, Ideology, Medical Records, Money, Security Clearance, Security Scanner, Travel, Wiretap : `{"TODO": ""}` alors que le texte imprimé décrit un effet de Setup (recherche dans la collection du joueur). Probablement un effet de campagne ou de construction de deck, donc non listé comme erreur.
- Press Conference : le filtre de retrait de jetons ne limite pas explicitement aux supports que le joueur contrôle (impact faible).
- Abduct Superhumans, A.I.M. Abductor : comportement si Abduct n'est pas en jeu.
- Parcours du Combattant : boost « après cette attaque », résolution à tester.
- M.O.D.O.K. : plusieurs Holding Cell en jeu.
- Nabbed! : tuck de l'allié défaussé.
- Dum Dum Dugan : passage de l'altération.
- Psionic Force Field, Informant : interaction avec les événements d'interruption.
- Psionic Enhancement : `draw_boost_card` avec sujet `host`.


---

## Audit Warnel, lot 02 : `Sets/SetScripts_next_evol.json` (pack Next Evolution)

Méthode : chaque clé du lot (231, `_macros` exclue) a été rapprochée du texte imprimé (cards.json / SetDefinition_next_evol.json), puis les soupçons ont été vérifiés dans le code Godot (`src/wc/...`, `src/core/...`) et recoupés avec les modules Narwhal (`Fusion/marvel-lcg-src/src/cards/pack/next_evol/...`). Seules les erreurs prouvées sont listées. Les fonctions moteur citées ont été lues.

Faits moteur utiles pour plusieurs fiches :
- `src/core/ScriptingEngine/ScriptProperties.gd`, `check_validity` (l. ~1735-1780) : dans un `filter_state_*`, chaque clé est testée par un `if ... in filter`. Une clé inconnue (faute de frappe) n'est testée par aucune branche et la carte est donc acceptée.
- `src/wc/OVUtils.gd` (filtrage `event_filters`) + `src/wc/WCUtils.gd` `is_element1_in_element2` (l. 277) : une clé de `event_filters` absente de `trigger_details` fait échouer le filtre (`if not element2.has(key): return false`).
- `src/wc/ScriptingEngine/ScriptingEngine.gd` `conditional_script` (l. 1750) : toutes les options dont la condition est vraie s'exécutent (pas seulement la première).
- `src/core/CardTemplate.gd` `move_to` (l. ~1262) + `src/core/ScriptingEngine/ScriptingEngine.gd` `move_card_to_container` (l. 642) : `dest_index` par défaut = -1, ce qui ajoute la carte en dernier enfant du Pile, donc en haut (`Pile.get_top_card()` = `get_last_card()`, `Hand.draw_card` prend `get_top_card()`).
- Aucun mélange automatique après une recherche : seul le task `shuffle_container` (ScriptingEngine.gd l. 331 / core l. 996) mélange. Les cartes du même fichier qui le font l'écrivent explicitement (Build Support, Call for Backup, Lock and Load, Professor).

---

### [next_evol] Ruckus (40115)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « <b>When Revealed</b>: Stun each character you control. »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Ruckus"`, bloc `reveal` : `filter_state_seek: [{"gilter_group": "group_friendly_my_hero"}]`. La clé est écrite `gilter_group` (faute de frappe).
- **Pourquoi c'est faux** : dans `ScriptProperties.gd` `check_validity` (l. ~1745-1780), chaque clé de filtre est testée par un `if FILTER_PROPERTIES in filter ... elif filter == FILTER_GROUP ...`. `gilter_group` ne correspond à aucune branche, donc `card_matches` reste vrai pour toutes les cartes du `boardseek`. Le task `mod_tokens` (stunned, `subject_count: all`) s'applique alors à toutes les cartes en jeu (vilain, sbires, plans, alliés des autres joueurs), pas seulement aux personnages du joueur.
- **Correctif proposé** :
```json
"reveal": {"all": [{"name": "mod_tokens", "token_name": "stunned", "modification": 1, "subject": "boardseek", "subject_count": "all", "filter_state_seek": [{"filter_group": "group_friendly_my_hero"}]}]}
```
- **Référence Narwhal** : `next_evol/nasty_boys/40115.py`

### [next_evol] Thumbelina (40182)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Reduce the amount of damage Thumbelina takes from each attack by 1 unless the attacker has the [[TINY]] trait. »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Thumbelina"`, `interrupt_receive_damage.event_filters` : `{"target": "self", "amount": ">0", "tag": ["attack"]}`. La clé est `tag` (singulier). C'est la seule occurrence de `"tag":` dans tout `Sets/*.json`, toutes les autres cartes utilisent `tags`.
- **Pourquoi c'est faux** : `WCUtils.is_element1_in_element2` (l. 284-286) renvoie `false` dès qu'une clé du filtre est absente des `trigger_details`. Les détails de l'événement `receive_damage` portent `tags`, pas `tag`. Le filtre échoue donc toujours et la réduction de 1 dégât n'est jamais appliquée. Corollaire : avec `tags: ["attack"]` le filtre ne s'appliquerait qu'aux attaques, ce que veut le texte.
- **Correctif proposé** :
```json
"interrupt_receive_damage": {
  "filter_state_trigger": [{"filter_properties": {"trait_tiny": 0}}],
  "event_filters": {"target": "self", "amount": ">0", "tags": ["attack"]},
  "board": [{"name": "prevent", "amount": 1, "subject": "interrupted_event"}]
}
```
- **Référence Narwhal** : `next_evol/extreme_measures/40182.py`

### [next_evol] Titanium Exoskeleton (40091)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « <b>Hero Action</b>: Choose to either spend 3 resources of any type or remove a confused or stunned status card from attached enemy → discard this card. »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Titanium Exoskeleton"`, `manual.board`, options `"Remove Stunned"` et `"Remove Confused"` : les deux font `{"name": "mod_tokens", "token_name": "stunned", "modification": -1, "subject": "host", "is_cost": true}`.
- **Pourquoi c'est faux** : l'option « Remove Confused » retire un jeton `stunned`, jamais `confused`. Un ennemi confus (sans stun) ne peut donc pas être libéré : `mod_tokens` en coût échoue faute de jeton `stunned`. `confused` est un nom de jeton valide (utilisé par Dizzying Deeds dans le même fichier).
- **Correctif proposé** : remplacer le `token_name` de la seconde option.
```json
"Remove Confused": [
  {"name": "constraints", "is_cost": true, "tags": ["hero_action"]},
  {"name": "mod_tokens", "token_name": "confused", "modification": -1, "subject": "host", "is_cost": true},
  {"name": "discard", "subject": "self"}
]
```
- **Référence Narwhal** : `next_evol/military_grade/40091.py`

### [next_evol] Reaper (40187)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « <b>Forced Interrupt</b>: When Reaper attacks you, if you have at least: • [mental][mental] resources in your hand, stun your identity. • [mental][mental][mental][mental] resources in your hand, exhaust your identity. »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Reaper"`, `interrupt_enemy_attack` : second `conditional_script` option avec `"func_name": "count_printed_resources>=3"` (resource_type mental) pour l'épuisement.
- **Pourquoi c'est faux** : le seuil est 3 au lieu de 4 (quatre icônes [mental] imprimées). `count_printed_resources` (`src/wc/CardTemplate.gd` l. 4282) renvoie la somme des icônes `mental` de la main et le suffixe `>=3` est comparé tel quel. L'identité est donc épuisée dès 3 ressources mentales. `conditional_script` exécutant toutes les options vraies, la structure à deux seuils cumulatifs est correcte, seul le seuil est faux. Le module Narwhal confirme `b >= 2` et `b >= 4`.
- **Correctif proposé** :
```json
{"condition": {"func_name": "count_printed_resources>=4", "func_params": {"resource_type": "mental", "subject": "tutor", "subject_count": "all", "src_container": "hand_current_hero_target"}}, "nested_tasks": [{"name": "exhaust_card", "subject": "current_hero_target"}]}
```
(remplace la seconde entrée de `options`).
- **Référence Narwhal** : `next_evol/mutant_insurrection/40187.py`

### [next_evol] Harpoon (minion, 40098)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « <b>Forced Interrupt</b>: When Harpoon attacks you or an ally you control, choose: • Take 2 indirect damage. • Harpoon gets +2 ATK for this attack and this attack gains piercing. »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Harpoon #40098"`, seconde option `"+1 Boost Card"` : `[{"name": "draw_boost_card", "subject": "self"}]`. C'est le texte du stade A du vilain (« Give Harpoon 1 additional facedown boost card »), copié pour le sbire.
- **Pourquoi c'est faux** : `draw_boost_card` ajoute une carte boost et ne donne ni +2 ATK ni piercing. Le moteur sait faire les deux : +ATK le temps de l'attaque via `add_script` avec `end_condition: enemy_activation_finished` et un `alterants` sur `attack` (même mécanisme que Vertigo #40100 dans ce fichier), et le tag `piercing` est lu par `ScriptingEngine.gd` l. 1092 et 1149 via `replacement_effect` sur `current_activation` avec `additional_tags` (voir `SetScripts_aos.json` l. 7371).
- **Correctif proposé** (le `replacement_effect` sur `current_activation` dans un `interrupt_enemy_attack` est calqué sur `SetScripts_aos.json` l. 7365-7375, à tester en jeu) :
```json
"+2 ATK and piercing": [
  {"name": "add_script", "end_condition": "enemy_activation_finished", "subject": "self",
   "script": {"alterants": {"all": [{"filter_task": "get_property", "filter_property_name": "attack", "trigger": "self", "alteration": 2}]}}},
  {"name": "replacement_effect", "subject": "current_activation", "replacements": {"additional_tags": ["piercing"]}}
]
```
- **Référence Narwhal** : `next_evol/mutant_slayers/40098.py` (`GainAttackForThisAttack(+2)` et `GainPiercing`)

### [next_evol] Impervious (40156)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Reduce the amount of damage attached villain takes from each attack by 1. <b>Hero Action</b>: Spend [physical][physical] resources → give the villain a tough status card and discard this card. »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Impervious"`. (1) `manual` : `constraints hero_action`, `exhaust_card` sur `my_hero` (coût), `pay_cost physical 2`, `discard self`. Aucun jeton `tough` n'est jamais donné. (2) `interrupt_receive_damage.event_filters` = `{"target": "host", "amount": ">0"}` sans `tags`.
- **Pourquoi c'est faux** : (1) l'action ne donne pas le statut tough au vilain (le nom de jeton `tough` existe : `CFConst.gd` l. 745, `SetScripts_core.json` « Heart-Shaped Herb »), et elle épuise le héros, coût absent du texte. (2) Sans `tags: ["attack"]` le filtre accepte tout dégât au vilain (effets de cartes, retaliate, etc.), alors que le texte limite la réduction à « each attack » (voir `Aerial Bombardment` dans ce fichier : `"tags": ["retaliate"]`). `OVUtils.gd` n'applique la logique d'attaque que si `tags` contient `attack`.
- **Correctif proposé** :
```json
"Impervious": {
  "card_moved_to_board": {"trigger": "self", "board": [{"name": "attach_to_card", "subject": "villain"}]},
  "interrupt_receive_damage": {
    "event_filters": {"target": "host", "amount": ">0", "tags": ["attack"]},
    "board": [{"name": "prevent", "amount": 1, "subject": "interrupted_event"}]
  },
  "manual": {"board": [
    {"name": "constraints", "is_cost": true, "tags": ["hero_action"]},
    {"name": "pay_cost", "cost": {"physical": 2}, "is_cost": true},
    {"name": "mod_tokens", "token_name": "tough", "modification": 1, "subject": "host"},
    {"name": "discard", "subject": "self"}
  ]}
}
```
- **Référence Narwhal** : `next_evol/super_strength/40156.py`

### [next_evol] Favored Weapon (40107)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « <b>Hero Response</b>: After your hero defends against an attack from attached enemy and takes no damage → discard this card. »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Favored Weapon"`, bloc `response` : `event_name: defense_happened`, `event_filters: {"target": "my_hero", "damage": "<1"}`, aucune contrainte sur l'attaquant.
- **Pourquoi c'est faux** : `ScriptingEngine.gd` l. 1505 émet `defense_happened` avec `signal_details = {attacker, target, damage, tags}`. Le filtre `attacker` existe (`OVUtils.gd` l. 782 et d'autres cartes, p. ex. `SetScripts_ncrawler.json` l. 1594 : `"attacker": "host", "damage": "<1"`). Ici il manque : l'arme est défaussée après n'importe quelle défense sans dégât, y compris contre un autre ennemi que celui qui porte l'arme.
- **Correctif proposé** :
```json
"response": {"event_name": "defense_happened", "event_filters": {"target": "my_hero", "attacker": "host", "damage": "<1"}, "is_optional_board": true, "board": [{"name": "constraints", "is_cost": true, "tags": ["hero_form"]}, {"name": "discard", "subject": "self"}]}
```
- **Référence Narwhal** : `next_evol/on_the_run/40107.py`

### [next_evol] Stryfe (minion, 40032)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « <b>Forced Interrupt</b>: When a player plays a [[PSIONIC]] event, cancel the effects of that event and deal 1 damage to Stryfe. »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Stryfe"`, `interrupt_play_card.filter_state_trigger: [{"filter_properties": {"type_code": "event"}}]`. Le trait PSIONIC n'est pas testé.
- **Pourquoi c'est faux** : `check_validity` ne vérifie que `type_code == event`. Tout événement joué (psionique ou non) est annulé, défaussé, et Stryfe prend 1 dégât. Le motif `{"type_code": "event"}` est copié de Grappling Hook (`SetScripts_aos.json` l. 4404), dont le texte vise tous les événements. `filter_properties` + `filter_properties2` sont combinés en ET (commentaire `ScriptProperties.gd` l. 1747), et le trait se teste par `trait_psionic` (déjà utilisé dans ce fichier).
- **Correctif proposé** :
```json
"interrupt_play_card": {
  "filter_state_trigger": [{"filter_properties": {"type_code": "event"}, "filter_properties2": {"trait_psionic": 1}}],
  "board": [{"name": "prevent", "subject": "interrupted_event"}, {"name": "discard", "subject": "trigger"}, {"name": "deal_damage", "amount": 1, "subject": "self"}]
}
```
- **Référence Narwhal** : `next_evol/cable_nemesis/40032.py`

### [next_evol] Domino (action Swap, 40037a)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « <b>Action</b>: Choose a card in your hand. Swap that card with the top card of your deck. (Limit once per round.) »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Domino"`, `manual.board["Swap Card"]` : `nop` (choix de la carte de la main, `is_cost`), puis `move_card_to_container` `subject: previous` vers `dest_container: deck`, puis `draw_cards` `amount: 1`.
- **Pourquoi c'est faux** : `dest_index` vaut -1 par défaut (`ScriptProperties.gd` l. 1297) et `move_to` ajoute alors la carte comme dernier enfant du Pile, soit le dessus (`Pile.get_top_card` = `get_last_card`). `draw_cards` pioche ensuite `hand.draw_card(deck)` = `get_top_card()` : on reprend la carte qu'on vient de poser. L'échange est un no-op, la carte du dessus d'origine n'est jamais récupérée.
- **Correctif proposé** (piocher avant de remettre ; `draw_cards` n'a pas de `subject` donc `previous` doit rester la carte choisie, à tester en jeu) :
```json
"Swap Card": [
  {"name": "constraints", "is_cost": true, "tags": ["action_ability"]},
  {"name": "mod_tokens", "is_cost": true, "modification": -1, "subject": "self", "token_name": "__swap"},
  {"name": "nop", "is_cost": true, "subject": "index", "subject_count": "all", "src_container": "hand", "needs_selection": true, "selection_count": 1, "selection_type": "equal"},
  {"name": "draw_cards", "amount": 1},
  {"name": "move_card_to_container", "subject": "previous", "dest_container": "deck"}
]
```
Si `previous` est écrasé par `draw_cards`, mémoriser la carte choisie avant (`save_variable`) ou utiliser `subject_index`. La clé `function_overrides` et `once_per_round` du bloc restent inchangées.
- **Référence Narwhal** : `next_evol/domino/40037a.py` (`Faces.SwapWithDeckTop`)

### [next_evol] Neena Thurman (40037b)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « <b>Action</b>: Choose a card in your hand. Swap that card with the top card of your discard pile. (Limit once per round.) »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Neena Thurman"`, `manual.board["Swap Card"]` : `nop` (choix), `move_card_to_container` `subject: previous` vers `discard`, puis `move_card_to_container` `subject: index`, `subject_index: top`, `src_container: discard`, `dest_container: hand`.
- **Pourquoi c'est faux** : même mécanique que Domino. La carte choisie est posée sur la défausse (en dernier = dessus), puis `subject_index: top` (`ScriptObject.gd` l. 673-676 : `all_cards.size() - 1`) désigne cette même carte, qui revient en main. L'échange ne fait rien et la carte du dessus de la défausse n'est jamais récupérée.
- **Correctif proposé** : prendre d'abord la carte du dessus, puis poser la carte choisie.
```json
"Swap Card": [
  {"name": "constraints", "is_cost": true, "tags": ["action_ability"]},
  {"name": "mod_tokens", "is_cost": true, "modification": -1, "subject": "self", "token_name": "__swap"},
  {"name": "nop", "is_cost": true, "subject": "index", "subject_count": "all", "src_container": "hand", "needs_selection": true, "selection_count": 1, "selection_type": "equal"},
  {"name": "move_card_to_container", "subject": "index", "subject_index": "top", "src_container": "discard", "dest_container": "hand", "is_cost": true},
  {"name": "move_card_to_container", "subject": "previous", "dest_container": "discard"}
]
```
(même réserve sur la persistance de `previous` après le deuxième task ; sinon enregistrer la carte choisie avec `save_variable`).
- **Référence Narwhal** : `next_evol/domino/40037b.py`

### [next_evol] "I'll Take That" (40158)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Discard the upgrade you control with the lowest cost (highest cost instead if the villain has the [[PSIONIC]] trait). If no upgrade was discarded this way, this card gains surge. »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"\"I'll Take That\""`, `reveal` : un seul `discard` avec `sort_by: function`, `sort_name: get_subject_int_printed_property`, `sort_descending: true`, `subject_count: 1`. Aucun test du trait PSIONIC.
- **Pourquoi c'est faux** : `ScriptObject.gd` l. 973-974 inverse la liste triée (ordre croissant par défaut) quand `sort_descending` est vrai. Le script défausse donc toujours l'amélioration la plus chère. Le cas par défaut du texte (la moins chère) n'est jamais atteint et le trait PSIONIC n'est pas lu.
- **Correctif proposé** (`has_trait` avec `subject: villain` est déjà employé avec `Mister Sinister` ailleurs dans le fichier ; le préfixe `!` sur `func_name` est utilisé par Back to the Future, à valider pour `has_trait`) :
```json
"reveal": {"all": [
  {"name": "conditional_script", "options": [
    {"condition": {"func_name": "has_trait", "func_params": {"subject": "villain", "trait": "psionic"}},
     "nested_tasks": [{"name": "discard", "subject": "boardseek", "subject_count": 1, "is_cost": true, "sort_by": "function", "sort_name": "get_subject_int_printed_property", "func_params": {"property": "cost"}, "sort_descending": true, "filter_state_seek": [{"filter_group": "group_upgrade_support_my_hero", "filter_properties": {"type_code": "upgrade"}}]}]},
    {"condition": {"func_name": "!has_trait", "func_params": {"subject": "villain", "trait": "psionic"}},
     "nested_tasks": [{"name": "discard", "subject": "boardseek", "subject_count": 1, "is_cost": true, "sort_by": "function", "sort_name": "get_subject_int_printed_property", "func_params": {"property": "cost"}, "filter_state_seek": [{"filter_group": "group_upgrade_support_my_hero", "filter_properties": {"type_code": "upgrade"}}]}]}
  ]},
  {"name": "surge", "is_else": true}
]}
```
Le chaînage de `surge` en `is_else` après un `conditional_script` est à tester (le `is_else` actuel suit directement le `discard`).
- **Référence Narwhal** : `next_evol/super_strength/40158.py`

### [next_evol] Back to the Future (40033)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « The Cable player cannot remove threat from schemes other than Back to the Future. Other players cannot remove threat from Back to the Future. The Cable player cannot damage enemies not engaged with them. Other players cannot damage minions engaged with the Cable player. »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Back to the Future"`, un seul bloc `interrupt_remove_threat` : prévient le retrait de menace sur Back to the Future si `event_source_hero` n'est pas Cable.
- **Pourquoi c'est faux** : la clé n'a aucun autre bloc. Il manque (1) l'interdiction pour Cable de retirer de la menace aux autres plans, (2) l'interdiction pour Cable d'infliger des dégâts aux ennemis non engagés avec lui, (3) l'interdiction pour les autres joueurs d'infliger des dégâts aux sbires engagés avec Cable. Aucun `interrupt_receive_damage`, `script_alterants` ou `is_valid_target_filters` n'est présent (contrairement à Stryfe's Grasp, même fichier, qui restreint les cibles via `script_alterants.is_valid_target_filters`).
- **Correctif proposé** : ajouter à la clé un bloc de type `script_alterants` sur le modèle de Stryfe's Grasp pour (2) et (3), et un second `interrupt_remove_threat` pour (1) (`event_source_hero` = Cable, cible différente de Back to the Future). Forme exacte des filtres de cible à valider en jeu :
```json
"interrupt_remove_threat#cable": {"event_filters": {"filter_state_event_target": [{"filter_properties": {"Name": "!Back to the Future"}}]}, "condition_board": {"func_name": "get_subject_int_property", "func_params": {"subject": "event_source_hero", "property": "shortname", "property_value": "Cable"}}, "board": [{"name": "prevent", "amount": "all", "subject": "interrupted_event"}]}
```
(le suffixe `#cable` est illustratif : la clé doit être un second nom de déclencheur valide, ou fusionner les deux cas dans un seul bloc avec deux options). Les restrictions de dégâts demandent le même mécanisme `script_alterants` que Stryfe's Grasp.
- **Référence Narwhal** : `next_evol/cable_nemesis/40033.py`

### [next_evol] Inhibitor Collar (40092)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « <b>Action</b>: Choose to either exhaust a character you control or take 3 damage → discard this card. (Any player can do this.) »
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clé `"Inhibitor Collar"`, `manual.board` : option « Exhaust Character » avec `constraints` `tags: ["action"]`, option « Take 3 Damage » avec `constraints` `tags: ["hero_action"]`.
- **Pourquoi c'est faux** : dans `ScriptingEngine.gd` `constraints` (l. 3941), `hero_action` se développe en `["hero_form", "action_ability"]` : l'option des dégâts est refusée en forme alter-ego, alors que le texte dit « Action » (valable dans les deux formes) et que l'objet est attaché à l'identité, y compris alter-ego. À l'inverse, le tag brut `"action"` ne figure pas dans `_tags_to_tags` ni dans le `match` : l'option « Exhaust » n'a aucune contrainte de timing (jouable pendant une attaque ennemie, sur la pile, etc.). Les deux options devraient utiliser `action_ability` (ou `as_action`).
- **Correctif proposé** : remplacer `"tags": ["action"]` et `"tags": ["hero_action"]` par `"tags": ["action_ability"]` dans les deux options.
- **Référence Narwhal** : `next_evol/military_grade/40092.py`

### [next_evol] Recherches sans mélange (Fantomex 40015, Nathan Summers 40001b, Superpower Training 40059, Technovirus Resurgence 40031, A Sound Thrashing 40135, Black Tom Cassidy 40132, Get Nasty 40117, Topaz 40066)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : chacune se termine par « <i>(Shuffle.)</i> » après une recherche dans un deck (Fantomex : « search your deck and discard pile for E.V.A. and put it into play. (Shuffle.) » ; Nathan Summers : « Setup: Search your deck and discard pile for a player side scheme and put it into play. (Shuffle.) » ; Superpower Training : « search their deck and discard pile for an identity-specific upgrade ... (Shuffle.) » ; les autres cherchent dans le deck de rencontre).
- **Ce que fait le script Warnel** : `SetScripts_next_evol.json`, clés `"Fantomex - Charlie Cluster-7"`, `"Nathan Summers"`, `"Superpower Training"`, `"Technovirus Resurgence"`, `"A Sound Thrashing"`, `"Black Tom Cassidy"`, `"Get Nasty"`, `"Topaz"` : un `move_card_to_board` / `reveal_encounter` / `nop` tutor depuis le deck, sans `shuffle_container`.
- **Pourquoi c'est faux** : le moteur ne mélange jamais après une recherche (`ScriptingEngine.gd` l. 223-380 : `move_card_to_board` et `move_card_to_container` ne mélangent pas, seul le task `shuffle_container` l. 331 le fait). Le deck reste dans son ordre d'origine, ce qui révèle l'information que la règle masque. Les cartes sœurs du même fichier (Build Support, Call for Backup, Lock and Load, Professor) ajoutent bien `{"name": "shuffle_container", "dest_container": "deck_my_hero"}`.
- **Correctif proposé** : ajouter à la fin de chaque liste de tâches, pour les decks joueur (Fantomex, Nathan Summers, Superpower Training, Technovirus Resurgence) :
```json
{"name": "shuffle_container", "dest_container": "deck_my_hero"}
```
et pour le deck de rencontre (A Sound Thrashing, Black Tom Cassidy, Get Nasty, Topaz) :
```json
{"name": "shuffle_container", "dest_container": "deck_villain"}
```
(le nom `deck_villain` est celui des `src_container` de ces mêmes scripts ; à tester que `shuffle_container` l'accepte pour le deck de rencontre). Pour Nathan Summers, l'ajouter dans `setup.all` après le `move_card_to_board`. Pour A Sound Thrashing, mettre le mélange en `is_else: true` après la recherche.
- **Référence Narwhal** : `next_evol/40015.py`, `next_evol/cable/40001b.py`, `next_evol/40059.py` (les modules Narwhal mélangent après recherche)

---

Cartes auditées : 231
Cartes OK : 180 (231 moins 20 de campagne, moins 21 clés en erreur prouvée, moins 10 clés incertaines ; "OK" = aucun écart trouvé après lecture, pas test en jeu)
Effets de campagne non gérés (non listés) : 20 (scripts `{"TODO": "campaign mode not supported"}` : Assemble the Team, Establish Safehouse, Gear Up, Geared Up, Lady Mastermind, Malice, Mission Prep, Mission Prepped, Overburdened, Pouches, Practice Maneuvers, Practiced Maneuvers, Prepare Defenses, Prepared Defenses, Safehouse, Safehouse Established, Scrambler, Team Assembled, Under Pressure, Vanisher)

Erreurs prouvées : 14 fiches (Ruckus, Thumbelina, Titanium Exoskeleton, Reaper, Harpoon 40098, Impervious, Favored Weapon, Stryfe 40032, Domino, Neena Thurman, "I'll Take That", Back to the Future, Inhibitor Collar, groupe des 8 recherches sans mélange)

Cartes incertaines (non prouvées, à tester en jeu) :
- Aerial Bombardment : le +1 ATK est inconditionnel, alors que le texte pourrait le lier à « while attacking a non-AERIAL character » comme l'ignorance de retaliate (lecture de la phrase ambiguë).
- Mutant Insurrection : « Each minion gains toughness » n'est codé que pour les sbires qui arrivent après (`card_moved_to_board`), pas ceux déjà en jeu, et le jeton tough reste après la défausse du plan. Le moteur n'a pas de propriété `toughness` dynamique.
- Left to Your Fate 2B : l'alterant `cost +1` n'a ni `filter_state_trigger` ni `trigger` (portée réelle de `alterants.board` sans filtre non vérifiée), peut s'appliquer au-delà des cartes joueur.
- Mutant Slayers : le décompte « for each character with one or more of the traits » peut compter deux fois une carte à deux traits (comportement de `count_cards` multi-filtres non lu).
- Hope Summers (carte joueur 40204) : pas de script dans ce fichier pour la version joueur (seulement 40130), à chercher dans les autres SetScripts.
- Faces A sans texte imprimé (Escaping with Hope 2A, Gotta Get Away 1A, Bulking Up 2A, Focusing In 2A, Left to Your Fate 2A, Mutant Massacre 2A, Sinister Ends 3A, Sinister Intent 1A/1B) : non vérifiables, la face B a été lue.
- Plasma Rifle : `max_amount: 4` sur `attack`, support par `attack` non confirmé.
- A Good Workout : un seul `attack` à 4 + ressources, alors que le texte permet de viser un autre ennemi pour les dégâts additionnels.


---

## Audit SetScripts_sm.json (lot 03)

Fichier : `Sets/SetScripts_sm.json`. Références Narwhal : les modules `src/cards/pack/sm/<id>.py` n'existent que pour quelques cartes (27047, 27191, 27018 trouvés) ; sinon "n/a".

## Erreurs prouvées

### [sm] Calling in Favors (27129)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Rhino schemes with +2 SCH. »
- **Ce que fait le script Warnel** : SetScripts_sm.json, clé "Calling in Favors", `temporary_effect.effect.alterants.all[0]` modifie `"filter_property_name":"thwart"` (+2).
- **Pourquoi c'est faux** : `enemy_schemes` lit la propriété `scheme`, pas `thwart` (propriété des héros). Le bonus n'a aucun effet.
- **Correctif proposé** :
```json
{"filter_task":"get_property","filter_property_name":"scheme","filter_state_trigger":[{"filter_properties":{"shortname":"Rhino"}}],"alteration":2}
```
- **Référence Narwhal** : n/a

### [sm] Deepest Fears (27157)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « If no identity-specific card was discarded this way, take 1 damage. »
- **Ce que fait le script Warnel** : branche `else` : `{"name":"indirect_damage","subject":"my_identity","amount":1}`.
- **Pourquoi c'est faux** : le texte dit "take 1 damage" (dégât direct), pas "indirect damage" ; les dégâts indirects ne se redirigent pas de la même façon (alliés).
- **Correctif proposé** :
```json
{"name":"deal_damage","subject":"my_identity","amount":1}
```
- **Référence Narwhal** : n/a

### [sm] Defense Mechanism (27038)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « Hero Response: After your hero uses a basic power, discard Defense Mechanism → resolve Spider-Man's "Spider Camouflage" ability. »
- **Ce que fait le script Warnel** : seulement `response_basic_attack_happened` et `response_basic_thwart_happened`.
- **Pourquoi c'est faux** : la défense est un basic power (Rules Reference) ; l'événement `basic_defense_happened` existe et n'est pas écouté.
- **Correctif proposé** : ajouter, identique aux deux autres blocs :
```json
"response_basic_defense_happened":{"trigger":"my_hero","is_optional_board":true,"board":[{"name":"constraints","is_cost":true,"tags":["hero_interrupt"]},{"name":"move_card_to_container","subject":"self","dest_container":"discard"},{"name":"sequence","sequence_ability":"spider_camouflage","subject":"my_hero"}]}
```
- **Référence Narwhal** : n/a

### [sm] Dum Dum Dugan (27047)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « For each card exhausted this way, Dum Dum Dugan gets +1 to that power for this use. »
- **Ce que fait le script Warnel** : `interrupt_thwart` : `temporary_effect` avec `"alteration":"count_previous_subjects"` sans `passthrough_alteration`, contrairement à `interrupt_attack`.
- **Pourquoi c'est faux** : `count_previous_subjects` n'est pas une alteration valide appliquée directement ; seule la forme `passthrough_alteration` + `parent_passthrough_alteration` (utilisée dans la branche attack) calcule le nombre de cartes épuisées. Le bonus de thwart est donc nul.
- **Correctif proposé** :
```json
{"name":"temporary_effect","end_condition":"thwart_happened","subject":"self","passthrough_alteration":"count_previous_subjects","effect":{"alterants":{"all":[{"filter_task":"get_property","filter_property_name":"thwart","filter_state_trigger":[{"filter_card_name":"Dum Dum Dugan"}],"alteration":"parent_passthrough_alteration"}]}}}
```
- **Référence Narwhal** : `src/cards/pack/sm/27047.py`

### [sm] Frequent Flyers (27108)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Put the set-aside Hobgoblin and Vulture into play. »
- **Ce que fait le script Warnel** : `"__subject_name__":"Vulture - 1"`.
- **Pourquoi c'est faux** : le nom de la carte est "Vulture" (`shortname` = nom sans " - stage") ; "Vulture - 1" ne correspond à aucune carte, le Vautour n'entre jamais en jeu et la branche else (défausse) se déclenche à tort.
- **Correctif proposé** :
```json
{"_conditional_move_to_play":{"__subject_name__":"Vulture","__src_container__":"set_aside"}}
```
- **Référence Narwhal** : n/a

### [sm] Guard the Bell Tower (27079)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « When Revealed: Remove each chime counter from the Bell Tower and flip it to its quiet side. »
- **Ce que fait le script Warnel** : `reveal` met seulement `chime` à 0.
- **Pourquoi c'est faux** : le "flip to its quiet side" n'est pas codé.
- **Correctif proposé** : ajouter après `mod_tokens` :
```json
{"name":"conditional_script","options":[{"condition":{"func_name":"!has_trait","func_params":{"subject":"Bell Tower","trait":"quiet"}},"nested_tasks":[{"name":"flip_doublesided_card","subject":"Bell Tower"}]}]}
```
- **Référence Narwhal** : n/a

### [sm] Ghost Kick (27002)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « After Ghost-Spider uses a basic power, deal 6 damage to an enemy. »
- **Ce que fait le script Warnel** : `event_name":["basic_attack_happened","basic_thwart_happened"]`.
- **Pourquoi c'est faux** : la défense est un basic power ; `basic_defense_happened` manque.
- **Correctif proposé** :
```json
"event_name":["basic_attack_happened","basic_thwart_happened","basic_defense_happened"]
```
- **Référence Narwhal** : n/a

### [sm] Phantom Flip (27004) et Power Within (27037)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : "uses a basic power" (les deux cartes).
- **Ce que fait le script Warnel** : seuls attack et thwart sont écoutés.
- **Pourquoi c'est faux** : DEF et REC sont des basic powers ; `basic_defense_happened` n'est pas écouté.
- **Correctif proposé** : Phantom Flip, ajouter `"basic_defense_happened"` à `event_name` ; Power Within, ajouter un bloc `response_basic_defense_happened` copie du bloc attack.
- **Référence Narwhal** : n/a

### [sm] Ionic Boots (27148)
- **Gravité** : bloquante (typo) + partielle (filtre)
- **Certitude** : prouvée par le code
- **Texte imprimé** : « attacks and damages your identity » (déclencheur), puis défausse sur action.
- **Ce que fait le script Warnel** : `manual.board` : `"des_container":"discard_villain"`. `interrupt_receive_damage` sans filtre de cible, avec `"TODO":"damage to my identity"`.
- **Pourquoi c'est faux** : `src/core/ScriptingEngine/ScriptingEngine.gd`, `move_card_to_container` (l.650-656) : `dest_container` absent donc `FAILED`. Les ressources sont dépensées pour rien. Sans filtre, un dégât d'attaque sur un allié déclenche aussi la carte.
- **Correctif proposé** :
```json
"dest_container":"discard_villain"
```
et `"event_filters":{"target":"current_hero_target","amount":">0","tags":["attack"]}` (comme Hobgoblin - 1).
- **Référence Narwhal** : n/a

### [sm] Kinetic Armor (27149), Neocarbon Scales (27150), Tracking Display (27152), Spiked Gauntlet (27151)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : action de défausse de la carte.
- **Ce que fait le script Warnel** : `manual.board` (Spiked Gauntlet : `manual.board[...].if_no_damage`) contient `"des_container"`.
- **Pourquoi c'est faux** : même typo, `FAILED` dans `move_card_to_container`.
- **Correctif proposé** : remplacer par `"dest_container":"discard_villain"`.
- **Référence Narwhal** : n/a

### [sm] Neocarbon Scales (27150), second défaut
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « damage ... from each attack »
- **Ce que fait le script Warnel** : `interrupt_receive_damage`, `event_filters {"target":"host"}`.
- **Pourquoi c'est faux** : sans `tags:["attack"]`, tous les dégâts (conséquents, indirects) sont réduits.
- **Correctif proposé** :
```json
"event_filters":{"target":"host","tags":["attack"],"amount":">0"}
```
- **Référence Narwhal** : n/a

### [sm] In Cold Blood (27029)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « You cannot play events. »
- **Ce que fait le script Warnel** : `alterants.board[0].filter_state_trigger[0]` : `filter_properties {"trait_attack":1,"comparison":"ge"}` ET `filter_properties2 {"type_code":"event"}`.
- **Pourquoi c'est faux** : l'interdiction vise tous les événements, pas seulement ceux au trait attack.
- **Correctif proposé** : retirer `filter_properties` (`trait_attack`), ne garder que `{"type_code":"event"}`.
- **Référence Narwhal** : n/a

### [sm] Remote Navigation (27141)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « the villain activates against you »
- **Ce que fait le script Warnel** : `{"name":"villain_attacks_you"}`.
- **Pourquoi c'est faux** : `villain_attacks_you` appelle `enemy_attacks_you` (activation "attack" même en alter-ego, où l'activation est un scheme).
- **Correctif proposé** :
```json
{"name":"enemy_activates_against_you","subject":"villain"}
```
(précédent : Death dans SetScripts_aoa.json)
- **Référence Narwhal** : n/a

### [sm] Sand Smash (27072)
- **Gravité** : mineure
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « Resolve ... Surging Sands ... This card gains surge. »
- **Ce que fait le script Warnel** : `reveal_alter_ego` sans surge.
- **Correctif proposé** : ajouter `{"name":"surge"}` après le `sequence`.
- **Référence Narwhal** : n/a

### [sm] Venom - 3 (27075)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Place 2 facedown boost cards on each identity. »
- **Ce que fait le script Warnel** : `draw_boost_card` sans `amount`.
- **Pourquoi c'est faux** : `draw_boost_card` vaut 1 par défaut.
- **Correctif proposé** : `"amount":2`.
- **Référence Narwhal** : n/a

### [sm] Bell Tower (27077a)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « at least 3[per_hero] chime counters »
- **Ce que fait le script Warnel** : `card_token_modified` avec `"filter_count":3` fixe.
- **Pourquoi c'est faux** : le seuil doit être 3 par joueur.
- **Correctif proposé** : retirer `filter_count` et `comparison`, ajouter `"condition_board":{"func_name":"count_tokens>=3p","func_params":{"subject":"self","token_name":"chime"}}` en gardant `filter_token_name` et le flip (précédent : Pursued by the Past, SetScripts_aoa.json).
- **Référence Narwhal** : n/a

### [sm] Arm Cannon (27147)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : bonus aux attaques du vilain attaché.
- **Ce que fait le script Warnel** : macro `attacks_gain` avec `"__trigger__":"self"`.
- **Pourquoi c'est faux** : dans SP.gd, "self" désigne l'attachement (owner_card), alors que l'attaquant est le vilain hôte.
- **Correctif proposé** : `"__trigger__":"host"` (comme Razor Claws).
- **Référence Narwhal** : n/a

### [sm] Advanced Glider (27136)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à valider en jeu)
- **Texte imprimé** : « activates against you again »
- **Ce que fait le script Warnel** : `enemy_attack_happened` + `i_attack`.
- **Pourquoi c'est faux** : une activation peut être un scheme (alter-ego) ; `enemy_scheme_happened` manque et `i_attack` force une attaque.
- **Correctif proposé** : `"event_name":["enemy_attack_happened","enemy_scheme_happened"]` et remplacer `i_attack` par `enemy_activates` avec `target_identity` (`my_identity`, précédents dans SetScripts_mut_gen.json).
- **Référence Narwhal** : n/a

### [sm] Symbiote Suit (27191)
- **Gravité** : mineure
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « +1 to each of its basic powers »
- **Ce que fait le script Warnel** : alterants sur health, attack, thwart, defense, hand_size ; pas `recover`.
- **Correctif proposé** :
```json
{"filter_task":"get_property","filter_property_name":"recover","alteration":1,"filter_same_controller":true,"filter_state_trigger":[{"filter_group":"group_identities"}]}
```
- **Référence Narwhal** : `src/cards/pack/sm/27191.py`

### [sm] Loose Ends (27135)
- **Gravité** : mineure
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « During that reveal, if you change to alter-ego form, discard 1 random card from your hand »
- **Ce que fait le script Warnel** : `"TODO":"discard 1 if change form"`, effet imprimé non codé. Pas de correctif vérifié (l'événement `identity_changed_form` existe).
- **Référence Narwhal** : n/a

### [sm] Across the Spider-Verse (27018)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « choose a player. That player may spend 3 resources of any type to repeat this ability »
- **Ce que fait le script Warnel** : `"TODO":"dual player"`, partie non codée. Pas de correctif vérifié.
- **Référence Narwhal** : `src/cards/pack/sm/27018.py`

## Bilan

Cartes auditées : 207
Cartes OK : 140
Effets de campagne non gérés (non listés) : 25

Erreurs prouvées : 24 cartes (Kinetic Armor, Neocarbon Scales, Tracking Display, Spiked Gauntlet, Ionic Boots comptées individuellement ; Phantom Flip et Power Within séparément).

## Cartes incertaines (non prouvées, à tester en jeu)

- High Fashion : défausse limitée à upgrades, supports et alliés, texte à confirmer.
- Induced Panic : `faction_code hero` utilisé pour "identity-specific".
- Kraven the Hunter : le minion n'a pas de choix explicite.
- Take One for the Team : propriété guard sur l'hôte ne correspond pas clairement à "cannot attack".
- Taunting Presence : alterant `cannot_remove_threat` sur Light at the End absent du texte de cards.json.
- Web of Life and Destiny : pas de filtre type ally.
- Sky-Destroyer : pas de restriction "you play".
- Venom - 3 : "this turn" contre `once_per_round`.
- Phantom Flip : `group_scheme` inexistant, filtre probablement ignoré.
- Masterful Mirage : pas de filtre amount ni de source "you".
- Return the Favor : task `attack` contre "deal 5 damage".
- Sand Storm : filtre `group_friendly` inclut les alliés alors que le texte dit "among players".
- Symbiotic Monstrosity : boost sans condition attack.
- Webbed Up : sémantique du déclencheur.
- Worried Father : attache à l'identité au lieu de George.
- Bait and Switch : absente de cards.json 'sm', texte inconnu.
- Light at the End : règle "cannot win unless they escape" non vue.
- Manipulated Mind : "does not take consequential damage" non vu.


---

## Audit Warnel : Sets/SetScripts_aoa.json (lot 04)

Dépôt lu : warnel-chawpiovs-research (lecture seule). Texte imprimé : SetDefinition_aoa.json / cards.json. Narwhal sert de second avis.

### [aoa] Apocalypse - 3 (face 45186b) (45186b)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Forced Response: After Apocalypse changes to this form, place 3 threat on each scheme in play. »
- **Ce que fait le script Warnel** : `"add_threat","amount":2` (SetScripts_aoa.json, clé « Apocalypse - 3 #45186b », event card_changed_form). Il place 2 menaces au lieu de 3.
- **Pourquoi c'est faux** : valeur littérale 2 contre 3 imprimé. Aucune autre tâche ne compense (add_threat est exécuté tel quel par ScriptingEngine.gd, aucun bonus ajouté).
- **Correctif proposé** :
```json
"card_changed_form": {
	"trigger": "self",
	"board": [
		{
			"name": "add_threat",
			"amount": 3,
			"subject": "boardseek",
			"subject_count": "all",
			"filter_state_seek": [
				{ "filter_group": "group_schemes" }
			]
		}
	]
}
```
- **Référence Narwhal** : n/a

### [aoa] Apocalypse - 3 (face 45186c) (45186c)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Stalwart. Forced Response: After Apocalypse changes to this form, heal 3 damage from him. »
- **Ce que fait le script Warnel** : `{"name":"heal","amount":2,"subject":"self"}` (clé « Apocalypse - 3 #45186c », card_changed_form). Soigne 2 au lieu de 3.
- **Pourquoi c'est faux** : valeur littérale 2 contre 3 imprimé ; la tâche heal (ScriptingEngine.gd, heal) soigne exactement `amount`.
- **Correctif proposé** :
```json
"card_changed_form": {
	"trigger": "self",
	"board": [
		{ "name": "heal", "amount": 3, "subject": "self" }
	]
}
```
- **Référence Narwhal** : n/a

### [aoa] Evil Alliance (45078)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Revealed: Each nemesis minion in play activates against you. If no minions activated this way, place 3 pursuit counters on Pursued by the Past. »
- **Ce que fait le script Warnel** : `"enemy_attacks_you"` sur chaque sbire nemesis (clé « Evil Alliance », reveal).
- **Pourquoi c'est faux** : enemy_attacks_you (src/wc/ScriptingEngine/ScriptingEngine.gd, enemy_attacks_you) force toujours une attaque. Un sbire qui « s'active contre » un joueur en alter-ego doit comploter (enemy_activates_against_you : attaque si héros, complot si alter-ego). Le même moteur utilise déjà enemy_activates_against_you pour Wolf Among Sheep.
- **Correctif proposé** :
```json
"reveal": {
	"all": [
		{
			"name": "enemy_activates_against_you",
			"subject": "boardseek",
			"subject_count": "all",
			"filter_state_seek": [
				{
					"filter_properties": { "is_nemesis": true },
					"filter_properties2": { "type_code": "minion" }
				}
			],
			"is_cost": true
		},
		{
			"is_else": true,
			"name": "mod_tokens",
			"modification": 3,
			"subject": "Pursued by the Past",
			"token_name": "pursuit"
		}
	]
}
```
(La clé « boost » reste inchangée.)
- **Référence Narwhal** : n/a

### [aoa] Genetic Experiments (45066)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Attached minion gets +2 hit points. Forced Interrupt: When attached minion is defeated, place 2 threat on Gene Pool. »
- **Ce que fait le script Warnel** : clés présentes : card_moved_to_board, alterants (+2 PV), boost. Aucun déclencheur de mort du sbire (clé « Genetic Experiments »).
- **Pourquoi c'est faux** : l'effet imprimé « place 2 threat on Gene Pool » n'est codé nulle part dans la clé. Même motif que No Longer Worthy (interrupt_card_dies, trigger host).
- **Correctif proposé** : ajouter dans la clé :
```json
"interrupt_card_dies": {
	"trigger": "host",
	"board": [
		{ "name": "add_threat", "amount": 2, "subject": "Gene Pool" }
	]
}
```
- **Référence Narwhal** : n/a

### [aoa] Full-Body Charge (45045)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Deal 8 damage to an enemy. If your hero's remaining hit points are less than half your hero's starting hit points, this attack gains overkill. »
- **Ce que fait le script Warnel** : `save_variable my_life = get_subject_int_property(subject:"self", property:"health")` (clé « Full-Body Charge », manual).
- **Pourquoi c'est faux** : « self » est la carte événement elle-même (script.owner), qui n'a pas de PV de héros. La comparaison `get_remaining_damage<my_life` (PV restants du héros × 2 < my_life) compare donc à une valeur fausse. Il faut lire les PV de départ du héros.
- **Correctif proposé** :
```json
"manual": {
	"hand": [
		{ "name": "constraints", "is_cost": true, "tags": ["hero_action"] },
		{
			"name": "save_variable",
			"var_name": "my_life",
			"is_cost": true,
			"var_type": "int",
			"value": {
				"func_name": "get_subject_int_property",
				"func_params": { "subject": "my_identity", "property": "health" }
			}
		},
		{
			"name": "attack",
			"amount": 8,
			"subject": "an_enemy",
			"tags": {
				"if": {
					"func_name": "get_remaining_damage<my_life",
					"func_params": { "subject": "my_identity", "multiplier": 2 }
				},
				"then": ["overkill"],
				"else": []
			}
		}
	]
}
```
- **Référence Narwhal** : src/cards/pack/aoa/45045.py

### [aoa] No Longer Worthy (45105b)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Attach to Apocalypse and heal 5[per_hero] hit points from him. »
- **Ce que fait le script Warnel** : `{"name":"heal","amount":5,"subject":"Apocalypse"}` (clé « No Longer Worthy », card_moved_to_board). Soigne 5 quel que soit le nombre de joueurs.
- **Pourquoi c'est faux** : le [per_hero] est retiré du texte du mot-clé ; le moteur n'applique "Np" (N × joueurs) que si on l'écrit dans le script (ScriptObject.gd, retrieve_integer_property). À 2 joueurs, le soin devrait être 10.
- **Correctif proposé** :
```json
{ "name": "heal", "amount": "5p", "subject": "Apocalypse" }
```
(à la place de la tâche heal, le reste de la clé inchangé.)
- **Référence Narwhal** : src/cards/pack/aoa/apocalypse/45105b.py

### [aoa] Land Out of Time (45131)
- **Gravité** : partielle
- **Certitude** : prouvée par le code (le correctif est à confirmer en jeu : portée de « previous » après un sequence)
- **Texte imprimé** : « If the Savage Land is in play, resolve its Special ability and take 1 indirect damage for each resource icon on the discarded cards. Otherwise, find The Savage Land and reveal it. »
- **Ce que fait le script Warnel** : `sequence special` sur The Savage Land en coût, puis else reveal (clé « Land Out of Time »). Aucune tâche indirect_damage.
- **Pourquoi c'est faux** : la partie « take 1 indirect damage for each resource icon » est absente de la clé.
- **Correctif proposé** :
```json
"reveal": {
	"all": [
		{
			"name": "conditional_script",
			"options": [
				{
					"condition": {
						"func_name": "card_is_in_play",
						"func_params": { "subject": "The Savage Land" }
					},
					"nested_tasks": [
						{
							"name": "sequence",
							"sequence_ability": "special",
							"trigger_identity": "my_identity",
							"subject": "The Savage Land"
						},
						{
							"name": "indirect_damage",
							"subject": "my_identity",
							"amount": {
								"func_name": "count_printed_resources",
								"func_params": { "subject": "previous" }
							}
						}
					]
				}
			],
			"else": [
				{
					"name": "reveal_encounter",
					"subject": "find",
					"filter_state_tutor": [
						{ "filter_properties": { "shortname": "The Savage Land" } }
					]
				}
			]
		}
	]
}
```
- **Référence Narwhal** : src/cards/pack/aoa/savage_land/45131.py

### [aoa] Super-Charged (45006)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Interrupt: When you make a basic attack, discard Super-Charged → you get +2 ATK for this attack for each charge counter here (to a maximum of +8 ATK). »
- **Ce que fait le script Warnel** : l'interrupt « interrupt_attack_started » contient constraints, save_variable, add_script, sans aucune tâche discard (clé « Super-Charged »). La carte reste en jeu avec ses compteurs et peut resservir à chaque attaque.
- **Pourquoi c'est faux** : le coût « discard Super-Charged » est absent. Narwhal le code (CostFunc.Discard("This")). La valeur est déjà sauvegardée dans my_increase avant, donc défausser ensuite est sûr (même schéma que les événements qui ajoutent un script puis vont à la défausse).
- **Correctif proposé** : ajouter une dernière tâche dans le board de « interrupt_attack_started » (après add_script) :
```json
{ "name": "discard", "subject": "self" }
```
Bloc complet du board :
```json
[
	{ "name": "constraints", "is_cost": true, "tags": ["hero_interrupt"] },
	{
		"name": "save_variable",
		"var_name": "my_increase",
		"var_type": "int",
		"value": {
			"func_name": "count_tokens",
			"func_params": { "token_name": "charge", "subject": "self", "multiplier": 2, "max": 8 }
		}
	},
	{
		"name": "add_script",
		"end_condition": "basic_attack_happened",
		"subject": "self",
		"script": {
			"alterants": {
				"all": [
					{
						"filter_task": "get_property",
						"filter_property_name": "attack",
						"trigger": "my_hero",
						"alteration": "my_increase"
					}
				]
			}
		}
	},
	{ "name": "discard", "subject": "self" }
]
```
- **Référence Narwhal** : src/cards/pack/aoa/bishop/45006.py

---

Cartes auditées : 207
Cartes OK : 170
Erreurs prouvées : 7 cartes (8 faces/entrées : Apocalypse 3b, Apocalypse 3c, Evil Alliance, Genetic Experiments, Full-Body Charge, No Longer Worthy, Land Out of Time, Super-Charged)
Effets de campagne non gérés (non listés) : 18
Cartes incertaines (non prouvées, à tester en jeu) :
- Limbo (45032) : ordre « déplacer la carte choisie sous la pioche » puis « piocher » ; le texte dit « swap » avec le dessus de la pioche, ordre de résolution non prouvé.
- Pursued by the Past #45075a : `enemy_activates_against_you` sans subject, la résolution du sujet vide (propriétaire de l'environnement ou sbire nemesis) n'a pas été tranchée dans le code.
- Earthquake, Manta, Oracle : cibles ou déclencheurs douteux, non vérifiés dans le code.
- Giant Growth, Plugged In, Source of Power : « le joueur qui a vaincu » ; le sujet event_source_hero n'est pas certain dans ce contexte.
- Gene Pool : interrupt_card_dies alors que le texte dit Forced Response (« after an ally is defeated »), effet probablement identique en pratique.
- Witchfire : « Otherwise » du texte ambigu (pas d'allié vaincu), le script suppose is_else sur ally_died.
- Stepping Disc : filtre faction_code hero au lieu des cartes du set Magik, sans effet pratique prouvé.


---

## Audit Warnel, lot 05 : Sets/SetScripts_mts.json

Principe du contrôle : chaque erreur ci-dessous est établie par la lecture du moteur (CFInt.gd, StackScript.gd, ScriptingEngine.gd, ScriptObject.gd, OVUtils.gd) et par le texte imprimé.

Rappel de la sémantique utilisée (src/wc/ScriptingEngine/Scripts/StackScript.gd, `execute_*`, et src/core/ScriptingEngine/ScriptingEngine.gd, `execute`) : quand tous les coûts (`is_cost`) peuvent être payés, seules les tâches NON `is_else` s'exécutent ; quand un coût ne peut pas être payé, seules les tâches `is_else` s'exécutent. Une tâche `is_else` ne se déclenche donc jamais si le script n'a aucun coût.

### [mts] Avengers Tower (21100a, face environnement)

- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Forced Response: After damage is placed here, if there is at least 9[per_hero] damage here, remove all of it. Then flip Avengers Tower over. »
- **Ce que fait le script Warnel** : `Sets/SetScripts_mts.json`, clé `"Avengers Tower #21100a"`, bloc `card_damaged`, condition `"comparison": "ge", "comparison_value": 9` : seuil littéral de 9 dégâts quel que soit le nombre de joueurs.
- **Pourquoi c'est faux** : `src/wc/OVUtils.gd` (comparaison, ~l.349-359) et `src/core/ScriptingEngine/ScriptObject.gd` `retrieve_integer_property` (~l.865-866) ne multiplient par le nombre de joueurs (`cfc.count_players()`) que pour une valeur de la forme `"Np"`. Un entier est pris tel quel. À 2, 3 ou 4 joueurs, la tour se retourne trop tôt (9 au lieu de 18, 27, 36).
- **Correctif proposé** : remplacer `9` par `"9p"` dans la condition.
```json
"card_damaged": {
  "event_filters": { "target": "self" },
  "board": [
    {
      "name": "conditional_script",
      "options": [
        {
          "condition": {
            "if": {
              "func_name": "count_tokens",
              "func_params": { "token_name": "damage", "subject": "self" },
              "comparison": "ge",
              "comparison_value": "9p"
            },
            "then": 1,
            "else": 0
          },
          "nested_tasks": [
            { "name": "heal", "subject": "self", "amount": 100 },
            { "name": "flip_doublesided_card", "subject": "self" }
          ]
        }
      ]
    }
  ]
}
```
- **Référence Narwhal** : `src/cards/pack/mts/the_tower_defense/21100a.py` (`at_least="9*"`, 9 par héros).

### [mts] Avengers Tower (21100b, face stronghold)

- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Forced Response: After damage is placed here, if there is at least 9[per player] damage here, the players lose the game. »
- **Ce que fait le script Warnel** : `Sets/SetScripts_mts.json`, clé `"Avengers Tower #21100b"`, bloc `card_damaged`, `"comparison_value": 9` (littéral) puis `defeat`.
- **Pourquoi c'est faux** : même mécanisme que ci-dessus (OVUtils.gd, ScriptObject.gd `retrieve_integer_property`) : sans suffixe `p`, la défaite survient dès 9 dégâts, même à plusieurs joueurs.
- **Correctif proposé** :
```json
"card_damaged": {
  "event_filters": { "target": "self" },
  "board": [
    {
      "name": "conditional_script",
      "options": [
        {
          "condition": {
            "if": {
              "func_name": "count_tokens",
              "func_params": { "token_name": "damage", "subject": "self" },
              "comparison": "ge",
              "comparison_value": "9p"
            },
            "then": 1,
            "else": 0
          },
          "nested_tasks": [ { "name": "defeat" } ]
        }
      ]
    }
  ]
}
```
- **Référence Narwhal** : `src/cards/pack/mts/the_tower_defense/21100b.py` (`at_least="9*"`).

### [mts] Cosmic Inquisition (21070)

- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu) pour l'incite ; prouvée par le code pour l'absence de mélange
- **Texte imprimé** : « Incite 2. When Revealed: If the Universal Church of Truth side scheme is in play, discard the top 10 cards of your deck. Otherwise, search the encounter deck, discard pile, and set-aside area for Universal Church of Truth and reveal it. Shuffle the encounter deck. »
- **Ce que fait le script Warnel** : `Sets/SetScripts_mts.json`, clé `"Cosmic Inquisition"`, bloc `reveal` seul : tutor + reveal de Universal Church of Truth (`is_cost`), sinon défausse de 10 cartes (`is_else`). Aucune clé `incite`, aucun `shuffle_container`.
- **Pourquoi c'est faux** : `incite` n'est pas un mot-clé auto-généré (`src/wc/CFConst.gd` AUTO_KEYWORDS ne produit un script automatique que pour `setup` et `toughness`, voir `SetScripts_All.gd`) ; il faut la clé `incite` qui active la macro de `Sets/_macros.json`, comme pour `"Barrel Roll"` dans `SetScripts_gmw.json` l.689 ou `"A.I.M. Interference ([energy])"` dans `SetScripts_aos.json`. Sans elle, les 2 menaces ne sont jamais ajoutées. De plus, `move_card_to_container` ne mélange pas (ScriptingEngine.gd, `move_card_to_container` ; le mélange exige `shuffle_container`, voir le motif de `SetScripts_bkw.json` l.26), donc le deck d'encounter n'est pas mélangé après la recherche.
- **Correctif proposé** (la tâche de mélange est hors `is_else`, donc exécutée seulement quand la recherche a réussi, ce qui correspond au « Otherwise ») :
```json
"Cosmic Inquisition": {
  "incite": { "__amount__": 2 },
  "reveal": {
    "all": [
      {
        "is_cost": true,
        "name": "deal_encounter",
        "immediate_reveal": true,
        "subject": "tutor",
        "src_container": ["deck_villain", "discard_villain", "set_aside"],
        "filter_state_tutor": [ { "filter_properties": { "Name": "Universal Church of Truth" } } ]
      },
      { "name": "shuffle_container", "dest_container": "deck_villain" },
      {
        "name": "move_card_to_container",
        "subject": "tutor",
        "up_to": true,
        "subject_count": 10,
        "src_container": "deck",
        "dest_container": "discard",
        "is_else": true
      }
    ]
  }
}
```
- **Référence Narwhal** : `src/cards/pack/mts/adam_warlock_nemesis/21070.py` (incite 2 puis la branche conditionnelle).

### [mts] Hall of Nastrond (21141 sur marvelcdb)

- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Defeated: The first player detaches Odin from the main scheme and takes control of him. Deal each player 1 facedown encounter card. »
- **Ce que fait le script Warnel** : `Sets/SetScripts_mts.json`, clé `"Hall of Nastrond"`, bloc `card_defeated` : `detach` d'Odin (`is_cost`), `move_card_to_board` d'Odin, puis `deal_encounter` marqué `"is_else": true`.
- **Pourquoi c'est faux** : le `deal_encounter` est en `is_else`, donc il ne s'exécute que si le détachement d'Odin échoue (StackScript.gd, branche `RunType.ELSE`). Dans le cas normal (Odin présent), aucun joueur ne reçoit sa carte d'encounter face cachée, alors que le texte l'exige dans tous les cas.
- **Correctif proposé** : une copie de la distribution en tâche normale (cas Odin détaché) et l'originale en `is_else` (cas Odin absent) :
```json
"card_defeated": {
  "trigger": "self",
  "all": [
    {
      "name": "detach",
      "subject": "boardseek",
      "is_cost": true,
      "filter_state_seek": [ { "filter_properties": { "shortname": "Odin" } } ]
    },
    { "name": "move_card_to_board", "grid_name": "allies_first_player", "subject": "previous" },
    {
      "name": "deal_encounter",
      "subject": "boardseek",
      "filter_state_seek": [ { "filter_group": "group_identities" } ]
    },
    {
      "name": "deal_encounter",
      "is_else": true,
      "subject": "boardseek",
      "filter_state_seek": [ { "filter_group": "group_identities" } ]
    }
  ]
}
```
- **Référence Narwhal** : `src/cards/pack/mts/hela/21142.py` (Odin mis en jeu, puis `ForEachPlayer` : 1 carte d'encounter à chacun).

### [mts] Gnipahellir (21140)

- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Defeated: The first player reveals Gjallerbru and Skurg, and puts them into play. Deal each other player 1 facedown encounter card. »
- **Ce que fait le script Warnel** : `Sets/SetScripts_mts.json`, clé `"Gnipahellir"`, bloc `card_defeated` avec `for_each_player` : `move_card_to_board` (tutor Gjallerbru ou Skurge dans `set_aside`, sans `is_cost`), puis `deal_encounter` en `is_else`.
- **Pourquoi c'est faux** : sans tâche `is_cost`, les coûts sont toujours considérés payables, donc la branche `RunType.ELSE` n'est jamais atteinte (StackScript.gd, `if sceng.can_all_costs_be_paid`). Les autres joueurs ne reçoivent jamais leur carte d'encounter. La carte sœur `"Gjallerbru"` (même fichier) utilise le bon motif : `is_cost: true` sur le `move_card_to_board` du tutor, pour que le passage des joueurs suivants, qui ne trouvent plus rien dans `set_aside`, bascule en `is_else`.
- **Correctif proposé** :
```json
"card_defeated": {
  "trigger": "self",
  "all": {
    "_rules": { "for_each_player": true, "forced": true },
    "Next Disaster": [
      {
        "name": "move_card_to_board",
        "subject": "tutor",
        "subject_count": "all",
        "src_container": "set_aside",
        "is_cost": true,
        "filter_state_tutor": [
          { "filter_properties": { "Name": "Gjallerbru" } },
          { "filter_properties": { "Name": "Skurge" } }
        ]
      },
      { "name": "deal_encounter", "subject": "my_hero", "is_else": true }
    ]
  }
}
```
- **Référence Narwhal** : `src/cards/pack/mts/hela/21140.py`.

### [mts] Kaluu (21014)

- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Response: After Kaluu enters play, search the top 5 cards of your deck for an event → add that event to your hand. Shuffle your deck. »
- **Ce que fait le script Warnel** : `Sets/SetScripts_mts.json`, clé `"Kaluu"`, bloc `self_moved_to_board` : un seul `move_card_to_container` du deck vers la main, aucun mélange.
- **Pourquoi c'est faux** : `move_card_to_container` ne mélange pas automatiquement (ScriptingEngine.gd) ; le mélange demande `shuffle_container` avec `dest_container` (motif de `SetScripts_bkw.json` l.26). Le deck reste dans l'ordre, ce qui donne un avantage au joueur (il connaît le haut du deck après les 5 cartes cherchées).
- **Correctif proposé** : ajouter une seconde tâche à la fin de `self_moved_to_board.board` :
```json
{ "name": "shuffle_container", "dest_container": "deck" }
```
- **Référence Narwhal** : `src/cards/pack/mts/21014.py` (`Search.PlayerDeckTop` 5 cartes, puis `GainCard`).

---

Cartes auditées : 202
Cartes OK : 182 (hors 6 erreurs prouvées et 14 effets de campagne ; dont 6 cartes incertaines)
Effets de campagne non gérés (non listés) : 14

Cartes incertaines (non prouvées, à tester en jeu) :
- White Tiger / Ava Ayala (21013) : `get_subject_int_property` (src/wc/CardTemplate.gd ~l.3756) ne lit ni `min` ni `max`, donc `"min": 1` du script est sans effet : un méchant sans numéro d'étape pigerait 0 carte au lieu de 1, et aucun plafond à 3. Impact réel dépend de l'existence de tels méchants.
- The Titan's Throne (21124) : le texte marvelcdb dit « When Revealed », le script et Narwhal le traitent comme « When Defeated » ; probablement une coquille de la base marvelcdb, à vérifier sur le scan.
- Avengers Tower support (21020) : l'augmentation de limite d'alliés +1 est inconditionnelle, alors que le texte l'exige seulement si chacun de vos alliés a le trait Avenger ; la condition n'est peut-être gérée qu'ailleurs.
- Thanos - 3 (21113) : le script cherche Thanos's Armor alors que le texte marvelcdb mentionne Helmet ; la base marvelcdb est probablement fautive, script plausible.
- Direct Assault : défausse codée seulement dans `interrupt_card_dies` ; à tester si le cas hors mort est possible.
- Formes de Spectrum (Gamma Blast, Photon Speed, Pulsar Shield, Energy Duplication) : dépendance à `card_is_in_play`/forme énergie, à tester en jeu.


---

## Lot 06 : Sets/SetScripts_mut_gen.json (Mutant Genesis)

Texte imprimé de référence : Sets/SetDefinition_mut_gen.json. Règles : Rules Reference v18 (entrée « THEN »).

### [mut_gen] Juggernaut (32026)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « ... that attack gains overkill and piercing » (boost)
- **Ce que fait le script Warnel** : Sets/SetScripts_mut_gen.json, clé "Juggernaut" (l.1992), `boost.all[0].replacements.additional_tags` = ["overkill","piercing","ranged"]
- **Pourquoi c'est faux** : le tag "ranged" n'est pas sur la carte. Dans src/wc/ScriptingEngine/ScriptingEngine.gd, la tâche d'attaque (autour de l.1513, émission de attack_happened) saute le retaliate de la cible quand le tag "ranged" est présent, et l'attaque compte comme ayant le mot-clé attaque à distance. Une attaque de Juggernaut déclenche donc à tort aucun retaliate.
- **Correctif proposé** :
```json
"Juggernaut": {
	"boost": {
		"all": [
			{
				"name": "replacement_effect",
				"subject": "current_activation",
				"replacements": {
					"additional_tags": ["overkill", "piercing"]
				}
			}
		]
	}
}
```
- **Référence Narwhal** : src/cards/pack/mut_gen/colossus_nemesis/32026.py (GainOverKill + GainPiercing seulement)

### [mut_gen] Rampaging Juggernaut (32027)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « Place 2 threat here for each tough status card discarded » (When Revealed)
- **Ce que fait le script Warnel** : clé "Rampaging Juggernaut" (l.4522), `reveal.all[0]` : add_threat avec `amount` = count_tokens tough, sans multiplicateur.
- **Pourquoi c'est faux** : le script place 1 menace par jeton tough au lieu de 2. Le moteur supporte `multiplier` sur les `func_name` (src/wc/OVUtils.gd, ~l.378-388 : `(result + plus) * multiplier / divider`), et le même fichier l'utilise déjà (l.713, l.2532).
- **Correctif proposé** :
```json
"Rampaging Juggernaut": {
	"reveal": {
		"all": [
			{
				"name": "add_threat",
				"subject": "self",
				"amount": {
					"func_name": "count_tokens",
					"func_params": {
						"token_name": "tough",
						"subject": "boardseek",
						"subject_count": "all",
						"multiplier": 2,
						"filter_state_seek": [ { "filter_group": "group_friendly" } ]
					}
				}
			},
			{
				"name": "mod_tokens",
				"token_name": "tough",
				"modification": 0,
				"set_to_mod": true,
				"subject": "boardseek",
				"subject_count": "all",
				"filter_state_seek": [ { "filter_group": "group_friendly" } ]
			}
		]
	}
}
```
- **Référence Narwhal** : src/cards/pack/mut_gen/colossus_nemesis/32027.py (`2 * value`)

### [mut_gen] Energy Barrier (32103)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Attach to a Sentinel minion without Energy Barrier attached and give it a tough status card. Otherwise, this card gains surge. »
- **Ce que fait le script Warnel** : clé "Energy Barrier" (l.1103), `self_moved_to_board.board[0].filter_state_seek` = `type_code: minion` + `filter_max_per_host: 1`, aucune restriction de trait.
- **Pourquoi c'est faux** : la carte peut se fixer sur n'importe quel serviteur (Brotherhood, etc.), le trait Sentinel n'est jamais testé. `filter_max_per_host` (src/wc/SP.gd, `check_max_per_host`, l.348) ne teste que l'absence d'une autre copie, pas le trait. Stun Beam, qui a la même formulation, filtre bien `trait_sentinel`.
- **Correctif proposé** :
```json
"filter_state_seek": [
	{
		"filter_properties": { "type_code": "minion" },
		"filter_properties2": { "trait_sentinel": 1, "comparison": "ge" },
		"filter_max_per_host": 1
	}
]
```
(à remplacer dans `self_moved_to_board.board[0]`; filter_properties et filter_properties2 sont combinés en ET, voir commentaire SP.gd ~l.630)
- **Référence Narwhal** : n/a (non lu en détail)

### [mut_gen] Stun Beam (32116)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Attach to a Sentinel minion without Stun Beam attached. Otherwise, this card gains surge. »
- **Ce que fait le script Warnel** : clé "Stun Beam" (l.5948), filtre `type_code: minion` + `trait_sentinel` mais pas de `filter_max_per_host`.
- **Pourquoi c'est faux** : rien n'empêche une seconde copie sur le même serviteur (la seule vérification « une par hôte » est `check_max_per_host` dans src/wc/SP.gd l.348, et elle n'est pas demandée). Les deux copies empilent « stun if damage ».
- **Correctif proposé** :
```json
"filter_state_seek": [
	{
		"filter_properties": { "type_code": "minion" },
		"filter_properties2": { "trait_sentinel": 1, "comparison": "ge" },
		"filter_max_per_host": 1
	}
]
```
(à remplacer dans `self_moved_to_board.board[0]`)
- **Référence Narwhal** : n/a

### [mut_gen] Sentinel stade III (32086), clé "Sentinel - 3"
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « ... Deal each other player a facedown encounter card. »
- **Ce que fait le script Warnel** : clé "Sentinel - 3" (l.5078), `sentinel_encounters.all._rules` = `{"for_each_player": true, "forced": true}`. La clé "Sentinel - 2" (même texte) porte en plus `"exclude_first_player": true`.
- **Pourquoi c'est faux** : le premier joueur reçoit aussi une carte facedown. `exclude_first_player` est le seul mécanisme d'exclusion du premier joueur (src/wc/CardTemplate.gd ~l.1916, boucle for_each_player). Le texte de 32085 (II) et 32086 (III) est identique sur ce point.
- **Correctif proposé** :
```json
"sentinel_encounters": {
	"all": {
		"_rules": {
			"for_each_player": true,
			"exclude_first_player": true,
			"forced": true
		},
		"Deal Encounter": [
			{
				"name": "deal_encounter",
				"subject": "my_identity",
				"src_container": ["deck_villain", "discard_villain"]
			}
		]
	}
}
```
- **Référence Narwhal** : src/cards/pack/mut_gen/sentinels/ (module du villain stade III), non relu

### [mut_gen] Sabretooth I, II, III (32060, 32061, 32062), clés "Sabretooth - 1/2/3"
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Forced Response: After Sabretooth activates against you, discard the top card of the encounter deck. Heal damage from Sabretooth equal to the number of boost icons discarded this way. »
- **Ce que fait le script Warnel** : clés l.4719, l.4743, l.4767 (scripts strictement identiques) : seul `enemy_attack_happened` avec `trigger: self`.
- **Pourquoi c'est faux** : « activates against you » couvre l'attaque (héros) et la machination (alter-ego). Le moteur émet deux signaux distincts, `enemy_attack_happened` et `enemy_scheme_happened` (src/wc/ScriptingEngine/ScriptingBus.gd l.79 et l.81 ; GameData.gd l.300). Quand Sabretooth manigance contre un joueur en alter-ego, rien ne se déclenche. Les autres lots gèrent ce cas en écoutant les deux événements (ex. Sets/SetScripts_aoa.json l.50-55 et l.742-747, `event_name` = [enemy_attack_happened, enemy_scheme_happened]).
- **Correctif proposé** : à appliquer aux trois clés
```json
"Sabretooth - 1": {
	"enemy_attack_happened": {
		"trigger": "self",
		"board": [
			{ "name": "discard", "subject": "index", "subject_index": "top", "src_container": "deck_villain", "is_cost": true },
			{ "name": "heal", "subject": "self", "amount": { "func_name": "count_boost_icons", "func_params": { "subject": "previous" } } }
		]
	},
	"enemy_scheme_happened": {
		"trigger": "self",
		"board": [
			{ "name": "discard", "subject": "index", "subject_index": "top", "src_container": "deck_villain", "is_cost": true },
			{ "name": "heal", "subject": "self", "amount": { "func_name": "count_boost_icons", "func_params": { "subject": "previous" } } }
		]
	}
}
```
(la clé `enemy_scheme_happened` comme clé de script est déjà utilisée dans Sets/SetScripts_ant.json l.993)
- **Référence Narwhal** : src/cards/pack/mut_gen/sabretooth/ (non relu)

### [mut_gen] Permanently Phased (32055)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Give to the Kitty Pryde player. »
- **Ce que fait le script Warnel** : clé "Permanently Phased" (l.3775), `give_obligation.__to__` = "Kitty Pride" (faute de frappe, le nom est « Kitty Pryde »).
- **Pourquoi c'est faux** : la macro `give_obligation` (Sets/_macros.json l.171) appelle `change_controller_hero` avec `target_identity` = ce nom ; la tâche (src/wc/ScriptingEngine/ScriptingEngine.gd, l.3784-3806) fait `find_card_by_name(target_identity)`, et si rien n'est trouvé `new_controller_id` reste à 0 et la tâche retourne FAILED. L'obligation n'est donc jamais donnée au joueur Kitty Pryde. L'identité s'appelle bien « Kitty Pryde » (clé "Kitty Pryde" l.2009 du même fichier, carte 32030b).
- **Correctif proposé** :
```json
"give_obligation": {
	"__to__": "Kitty Pryde"
}
```
- **Référence Narwhal** : src/cards/pack/mut_gen/shadowcat/32055.py (cible le joueur Shadowcat)

### [mut_gen] Insert Virus Program (32120)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « When Defeated: Deal 2 damage to each Sentinel enemy. »
- **Ce que fait le script Warnel** : clé "Insert Virus Program" (l.1819), `card_defeated.all[0].filter_state_seek` : `trait_sentinel` + `filter_properties2.type_code = minion` + `filter_same_controller: true`.
- **Pourquoi c'est faux** : le filtre `type_code: minion` exclut les villains Sentinel (Sentinel 32084-86 et Master Mold 32109-11 portent le trait Sentinel et sont des ennemis). Le texte vise tout ennemi Sentinel. `group_enemies` (src/wc/CFConst.gd l.353-364) couvre minion et villain.
- **Correctif proposé** :
```json
"filter_state_seek": [
	{
		"filter_properties": { "trait_sentinel": 1, "comparison": "ge" },
		"filter_group": "group_enemies",
		"filter_same_controller": true
	}
]
```
(à remplacer dans `card_defeated.all[0]`; `filter_same_controller` est conservé tel quel, voir l'incertitude plus bas)
- **Référence Narwhal** : src/cards/pack/mut_gen/sentinels/32120.py (tous les ennemis de trait SENTINEL)

---

Cartes auditées : 213
Cartes OK : 199 (aucune erreur prouvée ; hors les 11 erreurs et 3 incertaines)
Effets de campagne non gérés (non listés) : 25

Cartes incertaines (non prouvées, à tester en jeu)
- Magneto - Erik Lehnsherr (32172b) : `first_player_changed` déplace l'allié vers la grille `upgrade_support_first_player` (copiée de gmw) alors que les alliés d'autres cartes utilisent `allies_first_player` ; je n'ai pas trouvé la définition des grilles dans src, impact non prouvé.
- Defensive Energy (32018) : « draw 1 card when you spend this card to play a Defense event » est codé par un `nop` filtré sur le trigger dans le bloc `resource` ; le comportement exact (pioche, wild) dépend du flux de paiement, à tester en jeu.
- Phased Strike (32038) : « you may discard AN attachment » codé avec `subject_count` "all" + sélection optionnelle sans `selection_count` explicite ; nombre de cartes sélectionnables non vérifié dans le code.
- Insert Virus Program : `filter_same_controller` compare le contrôleur-héros de l'ennemi à celui de la machination, effet sur les ennemis engagés avec un autre héros non vérifié.

Points vérifiés et jugés corrects : limites `12p`, `6p`, `5p` (le texte imprimé de 32144b, 32063b, 32087b contient bien l'icône [per_hero]) ; Magnetic Missile (aucun dégât sans sbire Sentinel, conforme à la règle « THEN » du Rules Reference v18 : la partie après « then » ne se résout pas si la première échoue) ; Brotherhood Beatdown (`conditional_script` exécute toutes les options vraies, ScriptingEngine.gd l.1772-1781).


---

## Lot 07 : Sets/SetScripts_gmw.json (Guardians of the Galaxy / Rocket Raccoon & Groot, campagne Collector)

Moteur lu : /mnt/c/tmp/warnel-chawpiovs-research (src/wc/...). Textes imprimés : cards.json (clé gmw).

### [gmw] Macro milano_remove_threat (Blockade 16066, Bombardment, Cannonade, Interception Imminent 1B, Oppressive Armada, Pincer Maneuver, Spatial Positioning, Terrestrial Invasion 1B, The Great Escape 3B)
**Gravité** : mineure
**Certitude** : prouvée par le code
**Texte imprimé** : « <b>First Player Action:</b> Exhaust the Milano → remove 3 threat from this scheme. »
**Ce que fait le script Warnel** : la macro `milano_remove_threat` (SetScripts_gmw.json l.23, utilisée l.922, l.937 et dans les autres side schemes) pose `"tags": ["action_ability"]` sans `first_player`. Le même fichier utilise pourtant le tag `first_player` sur Kree Command Ship (« First Player Interrupt »).
**Pourquoi c'est faux** : ScriptingEngine.gd, `constraints`, cas `"first_player"` (~l.4002) : c'est ce tag qui force `select_current_playing_hero(first_player_id)` et refuse si le premier joueur n'est pas jouable. Sans lui, n'importe quel héros actif peut lancer l'action, ce qui viole « First Player Action ».
**Correctif proposé** :
```json
"milano_remove_threat": {
  "manual": {
    "board": [
      {"name": "constraints", "is_cost": true, "tags": ["action_ability", "first_player"]},
      {"name": "exhaust_card", "subject": "Milano", "is_cost": true},
      {"name": "remove_threat", "subject": "self", "amount": 3}
    ]
  }
}
```
**Référence Narwhal** : brotherhood_of_badoon/16061b.py et ship_command (action réservée au premier joueur).

### [gmw] Protect the Planet 2B (16062b)
**Gravité** : mineure
**Certitude** : prouvée par le code
**Texte imprimé** : « <b>First Player Action:</b> Exhaust the Milano → choose to either remove 3 threat from this scheme or deal 3 damage to a minion. »
**Ce que fait le script Warnel** : clé "Protect the Planet - 2B" (l.4418), les deux options du `manual` ont `"tags": ["action_ability"]` seul.
**Pourquoi c'est faux** : même cause que la macro (constraints, tag `first_player` absent).
**Correctif proposé** : dans les deux options de `manual.board`, remplacer la contrainte par
```json
{"name": "constraints", "is_cost": true, "tags": ["action_ability", "first_player"]}
```
**Référence Narwhal** : brotherhood_of_badoon/16062b.py

### [gmw] Rogue Vessel (16143)
**Gravité** : partielle
**Certitude** : prouvée par le code
**Texte imprimé** : « <b>First Player Action:</b> Exhaust the Milano and spend 2 resources of any type → discard this card. »
**Ce que fait le script Warnel** : clé "Rogue Vessel" (l.4806), `manual.board` : constraints `action_ability` seul, puis `pay_cost` `{"unc":2}`.
**Pourquoi c'est faux** : sans `first_player` (ScriptingEngine.gd, `constraints`, ~l.4002), le héros actif quelconque paie les 2 ressources, alors que la règle impose le premier joueur (il paie et il agit).
**Correctif proposé** :
```json
"manual": {"board": [
  {"name": "constraints", "is_cost": true, "tags": ["action_ability", "first_player"]},
  {"name": "exhaust_card", "subject": "Milano", "is_cost": true},
  {"name": "pay_cost", "cost": {"unc": 2}, "is_cost": true},
  {"name": "discard", "subject": "self"}
]}
```
**Référence Narwhal** : ship_command/16143.py

### [gmw] Nebula's Ship (16093)
**Gravité** : partielle
**Certitude** : prouvée par le code
**Texte imprimé** : « <b>First Player Action:</b> Exhaust the Milano and spend up to 2 resources of any type → remove 1 evasion counter from here for each resource spent this way. »
**Ce que fait le script Warnel** : clé "Nebula's Ship" (l.3951), options "Shoot the Thrusters! (1)" et "(2)" : aucune `constraints` du tout (ni `action_ability`, ni `first_player`).
**Pourquoi c'est faux** : sans `action_ability` (ScriptingEngine.gd, `constraints`, ~l.3990) l'action est possible hors du tour de jeu des joueurs, en interruption, et sans `first_player` elle est payable par n'importe quel héros.
**Correctif proposé** : ajouter en tête de chaque option
```json
{"name": "constraints", "is_cost": true, "tags": ["action_ability", "first_player"]}
```
**Référence Narwhal** : nebula/16093.py

### [gmw] Stay Awhile (16078)
**Gravité** : bloquante en partie à 2 joueurs ou plus, sans effet en solo
**Certitude** : prouvée par le code
**Texte imprimé** : « When Revealed (Alter-Ego): Choose to either spend [physical][physical] resources or put the top card of your deck faceup into The Collection. When Revealed (Hero): Collector attacks you with +1 ATK. If you take any amount of damage from that attack, put the top card of your deck faceup into The Collection. »
**Ce que fait le script Warnel** : clé "Stay Awhile" (l.5384). Branche alter-ego, option "Collection" : `move_card_to_container` avec `"src_container":"deck"` et `"for_each_player":true`. Branche héros, `post_activity_trigger` : `"src_container":"deck_current_hero_target"` et `"for_each_player":true`.
**Pourquoi c'est faux** : CardTemplate.gd (~l.2729-2745) duplique la tâche une fois par héros avec `for_each_player` et remplace le mot exact `deck` par `deckN`. Dans l'option alter-ego, tous les joueurs mettent donc le dessus de leur paquet dans la Collection alors que seul le joueur révélé choisit (« your deck »). Dans la branche héros, la tâche est dupliquée N fois sur le même `deck_current_hero_target` : N cartes du paquet de la cible au lieu d'une. Le script `reveal` ne tourne qu'une fois, pour le héros ciblé (CardTemplate.gd ~l.1799).
**Correctif proposé** :
```json
"Collection": [{"name": "move_card_to_container", "subject": "index", "subject_index": "top", "src_container": "deck_current_hero_target", "dest_container": "the_collection"}]
```
et dans `post_activity_trigger`, retirer `"for_each_player": true`.
**Référence Narwhal** : collector_1/16078.py (carte du joueur concerné seulement).

### [gmw] Museum Ship (16085b)
**Gravité** : partielle
**Certitude** : prouvée par le code
**Texte imprimé** : « Forced Interrupt: When the villain phase begins, choose one: Exhaust the Milano → assign 2[per_hero] indirect damage among players. / Assign 3[per_hero] indirect damage among players. »
**Ce que fait le script Warnel** : clé "Museum Ship" (l.3676) : `"amount": 2` et `"amount": 3` constants.
**Pourquoi c'est faux** : CardTemplate.gd `indirect_damage_replacement` (~l.2962) recopie `amount` tel quel dans `selection_count` (`indirect_damage_script_definition`, ScriptingEngine.gd l.4292), sans multiplication par le nombre de héros. CFControlExtended.gd (~l.485) ne fait que retirer `[per_hero]` des mots-clés. La suffixe « p » (ScriptObject.gd ~l.865, `Np` x `count_players`) existe, utilisée par SetScripts_aos.json (`"2p"`). `selection_count` accepte déjà des chaînes dynamiques (Full Auto, `my_boost_count`).
**Correctif proposé** :
```json
"board": {"_rules": {"forced": true},
  "Exhaust Milano": [{"name": "exhaust_card", "subject": "Milano", "is_cost": true}, {"name": "indirect_damage", "all_players": true, "amount": "2p"}],
  "3 Damage": [{"name": "indirect_damage", "all_players": true, "amount": "3p"}]}
```
**Référence Narwhal** : collector_2/16085b.py (`2 * player_num`, `3 * player_num`).

### [gmw] Collector A1 et B1 (16080a, 16081a)
**Gravité** : partielle
**Certitude** : prouvée par le code
**Texte imprimé** : « Forced Interrupt: When Collector would be defeated, remove 3[per_hero] threat from the main scheme and flip this card instead. »
**Ce que fait le script Warnel** : clés "Collector - A1" (l.1261) et "Collector - B1" (l.1340), `interrupt.card_dies.board` : `{"name":"remove_threat","amount":3,"subject":"main_scheme"}`.
**Pourquoi c'est faux** : montant constant, aucune mise à l'échelle par héros (voir Museum Ship : CFControlExtended.gd ~l.485 et ScriptObject.gd ~l.865). À 2 joueurs il faut retirer 6.
**Correctif proposé** : `{"name":"remove_threat","amount":"3p","subject":"main_scheme"}` (dans les deux clés).
**Référence Narwhal** : collector_2/16080a.py (`"3*"`).

### [gmw] Collector III (16072)
**Gravité** : partielle
**Certitude** : prouvée par le texte seul (à confirmer en jeu), l'absence de la tâche est dans le JSON
**Texte imprimé** : « Forced Interrupt: When a card would be placed into a discard pile from play, put it faceup into The Collection instead, then place 1 threat on the main scheme. »
**Ce que fait le script Warnel** : clé "Collector - 3" (l.1225), `interrupt_card_moved_to_pile` : un seul `move_card_to_container` vers `the_collection`. Aucune menace n'est posée.
**Pourquoi c'est faux** : la partie « then place 1 threat on the main scheme » est absente (la menace n'est posée qu'au `reveal`).
**Correctif proposé** :
```json
"interrupt_card_moved_to_pile": {"event_filters": {"destination": "discard_any", "source": "board"}, "board": [
  {"name": "move_card_to_container", "dest_container": "the_collection", "subject": "trigger"},
  {"name": "add_threat", "subject": "main_scheme", "amount": 1}
]}
```
**Référence Narwhal** : collector_1/__init__.py `PutCardIntoTheCollectionInsteadDiscard(True)` (menace 1 par carte).

### [gmw] Drang III, déclencheur (16060)
**Gravité** : partielle
**Certitude** : prouvée par le code
**Texte imprimé** : « Forced Response: After Drang activates, resolve the Badoon Ship's "Charge Up" ability. » (Drang I et II : « After Drang schemes »)
**Ce que fait le script Warnel** : clé "Drang - 3" (l.2025) reprend `response_enemy_scheme_happened` de Drang I et II.
**Pourquoi c'est faux** : GameData.gd (~l.300) émet `enemy_scheme_happened` et `enemy_attack_happened` séparément. Drang III en forme héros attaque, donc sans charge. Le même fichier gère les deux cas pour Badoon Engineer (« engages you or activates against you »).
**Correctif proposé** : ajouter à côté de la clé existante
```json
"response_enemy_attack_happened": {"trigger": "self", "board": [{"name": "sequence", "sequence_ability": "charge_up", "subject": "Badoon Ship"}]}
```
**Référence Narwhal** : brotherhood_of_badoon/16060.py `ResolveBadoonShipChargeUpabilityAfterThisActive()`.

### [gmw] Drang III, défausse par héros (16060)
**Gravité** : partielle
**Certitude** : prouvée par le code
**Texte imprimé** : « When Revealed: Discard the top 4[per_hero] cards of the encounter deck. Each time a minion is discarded this way, put it into play engaged with the player who is engaged with the fewest minions. »
**Ce que fait le script Warnel** : clé "Drang - 3", `reveal.all` : 4 appels fixes à `drang_minion_discard`.
**Pourquoi c'est faux** : 4 cartes quel que soit le nombre de joueurs (aucun [per_hero] automatique, CFControlExtended.gd ~l.485). `for_each_player` au niveau de la tâche (CardTemplate.gd ~l.2729) multiplie par le nombre de héros.
**Correctif proposé** : ajouter `"for_each_player": true` à chacune des 4 tâches
```json
{"name": "sequence", "sequence_ability": "drang_minion_discard", "subject": "self", "for_each_player": true}
```
**Référence Narwhal** : brotherhood_of_badoon/16060.py (`"4*"`).

### [gmw] Crisis on Halfworld (16053)
**Gravité** : bloquante pour l'effet « Give to the Rocket Raccoon player »
**Certitude** : prouvée par le code
**Texte imprimé** : « Give to the Rocket Raccoon player. »
**Ce que fait le script Warnel** : l.1486, `"give_obligation": {"__to__": "Rocket Rackoon"}` (faute de frappe).
**Pourquoi c'est faux** : la macro (_macros.json l.177) appelle `change_controller_hero` avec le nom ; ScriptingEngine.gd l.3784 fait `find_card_by_name(target_identity)`, ne trouve rien, `new_controller_id` reste 0 et la tâche renvoie FAILED. Aucune autre occurrence de « Rackoon » dans le dépôt.
**Correctif proposé** : `"give_obligation": {"__to__": "Rocket Raccoon"}`
**Référence Narwhal** : rocket_raccoon/16053.py

---

Cartes auditées : 192
Cartes OK : 168
Effets de campagne non gérés (non listés) : 33

Cartes incertaines (non prouvées, à tester en jeu)
- Badoon Grunt (16118) : `count_engaged_minions==0` évalué après `card_moved_to_board` compte peut-être le Grunt lui-même.
- The Poison (16125) : `step_started` PLAYER_TURN sans filtre sur le tour du porteur (« When your turn begins »).
- Beyonder's Blazer : `pay_cost` avec `type_constraint: different`, comportement non lu.
- Nebula II et III : `once_per_round_per_player` combiné à un jeton joueur, non vérifié.
- Booster Boots, Groot allié (16047), Rocket allié (16019) : « Play only if your identity has the [[guardian]] trait » ; Narwhal l'impose, Warnel le déduit du texte (CFControlExtended.gd ~l.704), à confirmer en jeu.


---

## Audit Warnel lot 08 : Sets/SetScripts_core.json

### [core] Business Problems (marvelcdb 01170)
- **Gravité** : partielle (condition manquante)
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Choose one: Discard a random card from your hand; or exhaust each upgrade you control. »
- **Ce que fait le script Warnel** : Sets/SetScripts_core.json, clé « Business Problems », option « Exhaust upgrades » :
```json
{"name":"exhaust_card","subject":"boardseek","subject_count":"all","filter_state_seek":[{"filter_group":"group_upgrade_support_my_hero"},{"filter_properties":{"type_code":"upgrade"}}]}
```
  Le tableau `filter_state_seek` est en OU : un élément suffit.
- **Pourquoi c'est faux** : `src/core/Utils/CardFilter.gd` et `ScriptProperties.gd` (check_validity) évaluent les éléments d'un tableau en OU et les clés d'un même dict en ET. Le second élément `type_code: upgrade` correspond donc à TOUTE amélioration en jeu, y compris celles des autres joueurs ou du vilain. Le texte ne vise que les améliorations contrôlées par le joueur.
- **Correctif proposé** : fusionner en un seul dict (ET) :
```json
{"name":"exhaust_card","subject":"boardseek","subject_count":"all","filter_state_seek":[{"filter_group":"group_upgrade_support_my_hero","filter_properties":{"type_code":"upgrade"}}]}
```
  (ou ne garder que `{"filter_group":"group_upgrade_support_my_hero"}` si ce groupe contient aussi les supports, à vérifier dans `CFConst.TYPES_TO_GROUPS`).
- **Référence Narwhal** : Fusion/marvel-lcg-src/src/cards/pack/core/ (module de Business Problems), filtre sur les améliorations du contrôleur.

### [core] Legions of Hydra (marvelcdb 01180)
- **Gravité** : bloquante (compte faux)
- **Certitude** : prouvée par le code
- **Texte imprimé** : traduction du texte de la manigance : ajoute de la menace selon le nombre d'ennemis HYDRA en jeu.
- **Ce que fait le script Warnel** :
```json
{"name":"add_threat","amount":"per_boardseek","subject":"self","per_boardseek":{"subject":"boardseek","subject_count":"all","filter_state_seek":[{"filter_properties":{"comparison":"gt","trait_hydra":0}},{"filter_group":"group_enemies"}]}}
```
- **Pourquoi c'est faux** : `perMessage.gd` et `ScriptObject.gd` (_boardseek_subjects) comptent les sujets trouvés. Les deux éléments du tableau étant en OU, le compte inclut tout ennemi (group_enemies) OU toute carte avec le trait Hydra, donc plus que les ennemis Hydra.
- **Correctif proposé** :
```json
"filter_state_seek":[{"filter_group":"group_enemies","filter_properties":{"comparison":"gt","trait_hydra":0}}]
```
- **Référence Narwhal** : Fusion/marvel-lcg-src/src/cards/pack/core/01180.py (comptage des ennemis Hydra).

## Pied de rapport
- Cartes auditées : 189
- Erreurs prouvées : 2
- Cartes OK : 180 (hors incertaines)
- Effets de campagne non gérés (non listés) : 0

Cartes incertaines (non prouvées, à tester en jeu) :
- Energy Daggers (01046) : double dégât possible sur le vilain si `group_enemies{id}` l'inclut ; le vilain est contrôleur 0, probablement exclu, à tester.
- Helicarrier : pas de choix de joueur, altération de coût sans filtre de joueur (AlterantEngine non lu en entier).
- Avengers Mansion, Helicarrier : « Max 1 per player » absent du script, gestion MaxPerUnit non vérifiée.
- Cosmic Flight : `hero_interrupt` peut manquer, non prouvé.
- Hulk : `count_printed_resources` et ressource wild non vérifiés.
- Klaw 3 et Rhino 3 : toughness non vérifiée.
- Immortal Klaw (01127) : non confronté au module Narwhal.


---

## Audit Warnel lot 09 : Sets/SetScripts_trors.json (The Rise of Red Skull, 165 clés)

Moteur lu : `src/wc/ScriptingEngine/ScriptingEngine.gd`, `src/core/ScriptingEngine/*`, `src/wc/CFConst.gd`, `Sets/_macros.json`.

### [trors] Cornered Staff (04071)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Revealed: Discard 1[per_hero] cards from the top of the encounter deck. Place 1 additional threat here for each boost icon discarded this way. »
- **Ce que fait le script Warnel** : `Sets/SetScripts_trors.json`, clé `Cornered Staff`. `discard_and_count` enregistre `save_variable` avec `"var_name": "my_boost_count"`, mais `do_threat` lit `"amount": "my_boost_icons"`.
- **Pourquoi c'est faux** : `ScriptObject.get_property` (`src/core/ScriptingEngine/ScriptObject.gd`, ~l.108-140) ne remplace une chaîne que si elle est une clé de `owner.script_variables`. `my_boost_icons` n'est écrite nulle part (`save_variable`, `ScriptingEngine.gd` l.831, n'écrit que `my_boost_count`). Les autres sets utilisent bien `my_boost_count` (`SetScripts_scw.json`, `SetScripts_stld.json`). La chaîne reste brute, donc la menace supplémentaire n'est jamais posée correctement.
- **Correctif proposé** :
```json
"Cornered Staff": {
	"reveal": {
		"all": [
			{"name": "sequence", "sequence_ability": "discard_and_count", "subject": "self", "count": "count_players"},
			{"name": "sequence", "sequence_ability": "do_threat", "subject": "self"}
		]
	},
	"discard_and_count": {
		"_silent": true,
		"all": [
			{"name": "discard", "subject": "index", "subject_index": "top", "src_container": "deck_villain", "is_cost": true},
			{"name": "save_variable", "var_name": "my_boost_count", "var_type": "int", "mode": "add", "value": {"func_name": "count_boost_icons", "func_params": {"subject": "previous"}}, "_comments": "remembering the card for damage"}
		]
	},
	"do_threat": {
		"_silent": true,
		"all": [
			{"name": "add_threat", "amount": "my_boost_count", "subject": "self"}
		]
	}
}
```
- **Référence Narwhal** : n/a (non consulté)

### [trors] Crossbones' Assault (04070)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Defeated: Crossbones activates against the player who defeated this scheme. »
- **Ce que fait le script Warnel** : clé `Crossbones' Assault` : `{"interrupt":{"event_name":"card_dies","board":[{"name":"villain_attacks_you"}],"trigger":"self"}}`
- **Pourquoi c'est faux** : le texte dit « activates » (attaque en forme héros, complot en alter-ego). `villain_attacks_you` (`ScriptingEngine.gd` l.2376) appelle `enemy_attacks_you` (l.2153) qui crée toujours une activation `"attack"`. Si le joueur est en alter-ego, Crossbones attaque au lieu de comploter. `enemy_activates_against_you` (l.2172) existe précisément pour ce cas (elle teste `is_hero_form()`), et est utilisée par `SetScripts_aoa.json` (Apocalypse, Death, Famine).
- **Correctif proposé** :
```json
"Crossbones' Assault": {
	"interrupt": {
		"event_name": "card_dies",
		"board": [{"name": "enemy_activates_against_you", "subject": "villain"}],
		"trigger": "self"
	}
}
```
- **Référence Narwhal** : n/a

### [trors] Super Absorbing Power (04092)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « [star] Boost: Reveal this card. »
- **Ce que fait le script Warnel** : clé `Super Absorbing Power` : seule la section `alterants` existe, aucune section `boost`.
- **Pourquoi c'est faux** : sans bloc `boost`, rien ne se passe quand la carte est retournée comme boost. Les autres side schemes à « Boost: Reveal this card » ont `"boost":{"all":[{"name":"reveal_encounters","subject":"self"}]}` (même fichier : `Ball and Chain` ; `SetScripts_mts.json` : `Universal Church of Truth`).
- **Correctif proposé** : ajouter à la clé, à côté de `alterants` (inchangé) :
```json
"boost": {
	"all": [
		{"name": "reveal_encounters", "subject": "self"}
	]
}
```
- **Référence Narwhal** : n/a

### [trors] Hydra Flame-Soldier (04145)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Forced Response: After Hydra Flame-Soldier makes an undefended attack against you, discard a support you control. »
- **Ce que fait le script Warnel** : clé `Hydra Flame-Soldier`, bloc `enemy_attack_happened` : `"src_container": "upgrade_support"`, `"subject":"index"`, sans filtre de type.
- **Pourquoi c'est faux** : la zone `upgrade_support` contient les upgrades ET les supports (`src/wc/CFConst.gd` l.453-454 : `"upgrade"` et `"support"` mènent à `upgrade_support`). Le joueur peut donc défausser une upgrade. Le bloc `boost` de la même carte filtre correctement `"type_code":"support"`. Le correctif reprend exactement la forme du bloc `boost` (zone `_current_hero_target`).
- **Correctif proposé** (clé complète) :
```json
"Hydra Flame-Soldier": {
	"enemy_attack_happened": {
		"trigger": "self",
		"board": [
			{
				"name": "move_card_to_container",
				"dest_container": "discard_current_hero_target",
				"src_container": "upgrade_support_current_hero_target",
				"is_cost": true,
				"subject": "boardseek",
				"subject_count": "all",
				"filter_state_seek": [
					{"filter_group": "group_upgrade_support_current_hero_target", "filter_properties": {"type_code": "support"}}
				],
				"selection_count": {
					"if": {"func_name": "current_activation_status", "func_params": {"undefended": true}},
					"then": 1,
					"else": 0
				},
				"selection_type": "equal",
				"needs_selection": true
			}
		]
	},
	"boost": {
		"all": [
			{
				"name": "move_card_to_container",
				"dest_container": "discard_current_hero_target",
				"src_container": "upgrade_support_current_hero_target",
				"is_cost": true,
				"subject": "boardseek",
				"subject_count": "all",
				"filter_state_seek": [
					{"filter_group": "group_upgrade_support_current_hero_target", "filter_properties": {"type_code": "support"}}
				],
				"selection_count": {
					"if": {"func_name": "current_activation_status", "func_params": {"undefended": true}},
					"then": 1,
					"else": 0
				},
				"selection_type": "equal",
				"needs_selection": true
			}
		]
	}
}
```
(Le bloc `boost` ci-dessus est recopié à l'identique de l'existant, à vérifier en le comparant au fichier avant collage.)
- **Référence Narwhal** : n/a

### [trors] Clint Barton (04001b)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Weapon of Choice : Action : Spend 1 resource of any type → search your deck and discard pile for Hawkeye's Bow and add it to your hand. Shuffle your deck. (Limit once per phase). »
- **Ce que fait le script Warnel** : clé `Clint Barton` : `move_card_to_container` (tutor `deck`+`discard` vers `hand`), aucune tâche de mélange.
- **Pourquoi c'est faux** : le moteur ne mélange jamais après une recherche. `move_card_to_container` ne l'appelle pas ; seules `shuffle_container` (`ScriptingEngine.gd` l.331) et `shuffle_card_into_container` (l.372) mélangent, et les autres cartes du fichier les appellent explicitement (Hydra Prison, Zola, Jessica Drew's Apartment). Le deck reste dans l'ordre d'origine, ce qui est un avantage indu.
- **Correctif proposé** (ajouter la dernière tâche) :
```json
"Clint Barton": {
	"once_per_round": {"__name__": "_weapon_of_choice"},
	"manual": {
		"board": {
			"Weapon of Choice": [
				{"name": "constraints", "is_cost": true, "tags": ["action_ability"]},
				{"name": "mod_tokens", "subject": "self", "modification": -1, "token_name": "_weapon_of_choice", "is_cost": true},
				{"name": "pay_cost", "cost": {"unc": 1}, "is_cost": true},
				{"name": "move_card_to_container", "subject": "tutor", "src_container": ["deck", "discard"], "dest_container": "hand", "filter_state_tutor": [{"filter_properties": {"Name": "Hawkeye's Bow"}}]},
				{"name": "shuffle_container", "dest_container": "deck"}
			]
		}
	}
}
```
- **Référence Narwhal** : n/a

### [trors] Prison Camps (04141)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Defeated: The player who defeated this scheme searches their deck and discard pile for an ally, puts it into play, and shuffles their deck. »
- **Ce que fait le script Warnel** : clé `Prison Camps` : `move_card_to_board` (tutor `deck`+`discard`, allié), pas de mélange.
- **Pourquoi c'est faux** : même raison que Clint Barton (aucun mélange automatique, voir `ScriptingEngine.gd` l.331 et l.372).
- **Correctif proposé** :
```json
"Prison Camps": {
	"card_defeated": {
		"trigger": "self",
		"all": [
			{"name": "move_card_to_board", "src_container": ["deck", "discard"], "subject": "tutor", "subject_count": "all", "selection_count": 1, "selection_type": "equal", "needs_selection": true, "filter_state_tutor": [{"filter_properties": {"type_code": "ally"}}]},
			{"name": "shuffle_container", "dest_container": "deck"}
		]
	}
}
```
- **Référence Narwhal** : n/a

### [trors] Crossbones - 2 (04059, stade 2)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Revealed: Search the encounter deck and discard pile for Crossbone's Machine Gun and attach it to Crossbones. Shuffle the encounter deck. »
- **Ce que fait le script Warnel** : clé `Crossbones - 2`, bloc `reveal` : `move_card_to_board` (tutor `deck_villain`+`discard_villain`), pas de mélange.
- **Pourquoi c'est faux** : aucun mélange automatique du deck rencontre (même raison que ci-dessus). Le format de la tâche de mélange pour le deck rencontre est déjà utilisé dans ce fichier (`Hydra Patrol` : `shuffle_container` avec `dest_container: deck_villain`).
- **Correctif proposé** (clé complète, `interrupt` inchangé) :
```json
"Crossbones - 2": {
	"interrupt": {
		"event_name": "pre_receive_damage",
		"trigger": "self",
		"event_filters": {"tags": ["attack"]},
		"condition_board": {"func_name": "count_attachments", "func_params": {"subject": "self", "filter_state_attachment": [{"filter_properties": {"comparison": "gt", "trait_weapon": 0}}]}},
		"board": [{"name": "replacement_effect", "subject": "interrupted_event", "replacements": {"additional_tags": ["piercing"]}}]
	},
	"reveal": {
		"all": [
			{"name": "move_card_to_board", "subject": "tutor", "src_container": ["deck_villain", "discard_villain"], "filter_state_tutor": [{"filter_properties": {"Name": "Crossbones' Machine Gun"}}]},
			{"name": "shuffle_container", "dest_container": "deck_villain"}
		]
	}
}
```
- **Référence Narwhal** : n/a

### [trors] Absorbing Man - 2 (04077, stade 2)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Revealed: If Super Absorbing Power is in play, deal 1 encounter card to each player. Otherwise, search the encounter deck and discard pile for Super Absorbing Power and reveal it. Shuffle the encounter deck if it was searched this way. »
- **Ce que fait le script Warnel** : clé `Absorbing Man - 2`, bloc `reveal` : `deal_encounter` en `is_cost` (tutor), puis `deal_encounter` en `is_else`. Aucun mélange.
- **Pourquoi c'est faux** : aucun mélange automatique. Le mélange ne doit avoir lieu que si la recherche a abouti. Dans le moteur (`src/core/CFInt.gd` l.13-19 ; `src/core/ScriptingEngine/ScriptingEngine.gd` l.322-329), le passage NORMAL exécute toutes les tâches sauf les `is_else`, et le passage ELSE n'exécute que les `is_else`. Une tâche de mélange placée entre le coût et le `is_else` ne tourne donc que si la carte a été trouvée.
- **Correctif proposé** (clé complète) :
```json
"Absorbing Man - 2": {
	"alterants": {
		"board": [{
			"filter_task": "get_property",
			"filter_property_name": "trait_*",
			"trigger": "self",
			"per_boardseek": {"subject": "boardseek", "subject_count": "all", "filter_has_requested_property": true, "filter_state_seek": [{"filter_properties": {"type_code": "environment"}}]},
			"alteration": "per_boardseek"
		}]
	},
	"reveal": {
		"all": [
			{"is_cost": true, "name": "deal_encounter", "immediate_reveal": true, "subject": "tutor", "src_container": ["deck_villain", "discard_villain"], "filter_state_tutor": [{"filter_properties": {"Name": "Super Absorbing Power"}}]},
			{"name": "shuffle_container", "dest_container": "deck_villain"},
			{"is_else": true, "name": "deal_encounter", "subject": "boardseek", "filter_state_seek": [{"filter_group": "group_identities"}]}
		]
	}
}
```
- **Référence Narwhal** : n/a

---

Cartes auditées : 165
Cartes OK : 135
Effets de campagne non gérés (non listés) : 16

Cartes incertaines (non prouvées, à tester en jeu) :
- Marked for Death : le texte dit « faceup », le script pose avec le tag `facedown` ; `return_attachments_to` filtre sur ce même tag, donc cohérent, probable différence d'affichage seulement.
- Earth's Mightiest Heroes : pas d'exclusion de « another » entre la cible épuisée et la cible prête ; effet net nul si la même carte est choisie, sans gain.
- Avengers Tower (cap 03024) : pas de carte trors correspondante, `_comments` TODO dans le script ; texte non vérifié ici.
- Hail Hydra! (cap 03030) : pas de carte trors, texte non vérifié.
- Hydra Bomber (core 01110) : pas de carte trors, texte non vérifié.
- Hydra Soldier (core 01182) : pas de carte trors, texte non vérifié.


---

## Audit Warnel, lot 10 : ironheart, spiderham, drs, psylocke, ncrawler

Méthode : pour chaque entrée, texte imprimé (SetDefinition_<pack>.json, ou cards.json de Narwhal pour drs) comparé au JSON, puis lecture du moteur Warnel (`src/wc/...`, `src/core/ScriptingEngine/...`). Narwhal sert de second avis uniquement.

Rappels de moteur utilisés plusieurs fois :
- Une clé inconnue dans un filtre `filter_state_*` est ignorée sans erreur (`src/core/ScriptingEngine/ScriptProperties.gd`, évaluation des filtres d'état), donc le filtre devient permissif.
- Pour les déclencheurs, seule la clé `event_filters` (pluriel) est lue (`src/wc/OVUtils.gd`, `filter_trigger`, lignes ~615 et ~664).
- Une condition sans suffixe de comparaison (`count_...` seul) passe dès que le résultat est non nul (`OVUtils.gd`, `func_name_run`).
- `constraints` ignore silencieusement un tag inconnu (`src/wc/ScriptingEngine/ScriptingEngine.gd`, `_tags_to_tags` et `constraints()`).

---

### [ironheart] Zzzax (29037)
- **Gravité** : partielle
- **Certitude** : prouvée par le code (deux défauts)
- **Texte imprimé** : « [star] Zzzax gets +X ATK and +X hit points, where X is equal to the total number of [energy] resources on cards the engaged player controls. [star] Boost: If you have at least [energy] [energy] resources in your hand, put Zzzax into play engaged with you. »
- **Ce que fait le script Warnel** : `Sets/SetScripts_ironheart.json`, clé `Zzzax`.
  1. `boost.condition_all` = `{"func_name":"count_printed_resources", ... "src_container":"hand_current_hero_target"}` sans comparaison : la condition est vraie dès 1 énergie en main.
  2. `alterants` (attack et health) : `"filter_state_seek":[{"filer_group":"play_area_my_hero"}]`. `filer_group` est une faute de frappe.
- **Pourquoi c'est faux** :
  1. `OVUtils.gd` `func_name_run` : sans suffixe, le résultat entier est traité comme booléen, donc seuil effectif 1 au lieu de 2.
  2. `ScriptProperties.gd` ne connaît pas `filer_group` et l'ignore : le `boardseek` n'est plus restreint, X compte les énergies imprimées de toutes les cartes en jeu (tous joueurs, villain, encounter) et non celles du joueur engagé. Le même filtre écrit correctement et avec le bon groupe existe dans `SetScripts_mts.json` (`play_area_current_hero_target`) et `SetScripts_psylocke.json` (Chimera).
- **Correctif proposé** :
```json
"Zzzax": {
  "alterants": {"board": [
    {"filter_task": "get_property", "filter_property_name": "attack", "trigger": "self",
     "alteration": {"func_name": "count_printed_resources", "func_params": {"resource_type": "energy", "subject": "boardseek", "subject_count": "all", "filter_state_seek": [{"filter_group": "play_area_current_hero_target"}]}}},
    {"filter_task": "get_property", "filter_property_name": "health", "trigger": "self",
     "alteration": {"func_name": "count_printed_resources", "func_params": {"resource_type": "energy", "subject": "boardseek", "subject_count": "all", "filter_state_seek": [{"filter_group": "play_area_current_hero_target"}]}}}
  ]},
  "boost": {
    "condition_all": {"func_name": "count_printed_resources>=2", "func_params": {"resource_type": "energy", "subject": "index", "subject_count": "all", "src_container": "hand_current_hero_target"}},
    "all": [{"name": "move_card_to_board", "subject": "self"}]
  }
}
```
- **Référence Narwhal** : `src/cards/pack/ironheart/zzzax/29037.py` (compte les énergies du joueur engagé, boost exige au moins 2).

### [ironheart] Helicarrier (29026)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « Action: Exhaust Helicarrier → choose a player. Reduce the resource cost of the next card that player plays this phase by 1. »
- **Ce que fait le script Warnel** : `SetScripts_ironheart.json`, clé `Helicarrier` : `manual.board` exhaust + `mod_tokens _helicarrier = 1`, `alterants` sur `cost` (`per_token_self`) sans aucun `filter_state_trigger`, remise à 0 du jeton sur `card_played` avec `trigger: another` (n'importe quel joueur).
- **Pourquoi c'est faux** : aucune étape « choose a player ». L'alterant `cost` sans filtre s'applique à toute carte de tout joueur (`CFScriptUtils.get_altered_value`), et le jeton est consommé par la première carte jouée par n'importe qui. En multijoueur, la réduction va au premier joueur qui joue, pas au joueur choisi.
- **Correctif proposé** : ajouter une sélection de joueur comme coût (même motif que Kurt's Chapel dans `SetScripts_ncrawler.json`), stocker le héros choisi et restreindre l'alterant et la remise à zéro à ce joueur. JSON indicatif pour la première étape, le reste est à valider en jeu :
```json
{"name": "nop", "subject": "boardseek", "subject_count": "all", "needs_selection": true, "selection_count": 1, "selection_type": "equal", "is_cost": true, "filter_state_seek": [{"filter_group": "group_identities"}]}
```
- **Référence Narwhal** : n/a (29026 absent).

### [ironheart] R&D Facility (29020)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « That character gets +1 THW and +1 ATK until the end of the phase. »
- **Ce que fait le script Warnel** : `SetScripts_ironheart.json`, clé `R&D Facility`, `manual.board[...add_script].end_condition = "round_ended"`.
- **Pourquoi c'est faux** : le bonus dure jusqu'à la fin du round, donc il reste actif pendant la phase du méchant (défense) alors que le texte l'arrête à la fin de la phase. `phase_ended` est la valeur utilisée par 28 autres scripts du dépôt.
- **Correctif proposé** :
```json
{"name": "add_script", "subject": "previous", "end_condition": "phase_ended", "script": {"alterants": {"all": [
  {"filter_task": "get_property", "filter_property_name": "attack", "trigger": "self", "alteration": 1},
  {"filter_task": "get_property", "filter_property_name": "thwart", "trigger": "self", "alteration": 1}]}}}
```
- **Référence Narwhal** : `src/cards/pack/ironheart/29020.py` (`GainUntilPhaseEnd`).

### [ironheart] Brawn (29004)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Resource: Generate a [mental] resource. (Limit once per phase.) »
- **Ce que fait le script Warnel** : `SetScripts_ironheart.json`, clé `Brawn - Amadeus Cho` : `"once_per_round":{"__name__":"__resource"}`.
- **Pourquoi c'est faux** : `_macros.json` `once_per_round` ne remet le jeton qu'à `round_ended`, alors que la limite est par phase (`once_per_phase` remet à `phase_ended`).
- **Correctif proposé** :
```json
"once_per_phase": {"__name__": "__resource"}
```
(à la place de `once_per_round`, le reste de la clé inchangé)
- **Référence Narwhal** : `src/cards/pack/ironheart/ironheart/29004.py` (`LimitOncePerPhase`).

### [spiderham] "Feast on This!" (30028)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Revealed: Take 2 damage. You are confused. If you already confused, this card gains surge. »
- **Ce que fait le script Warnel** : `SetScripts_spiderham.json`, clé `"Feast on This!"` : `conditional_script` avec `"func_name":"is_stunned"` ; si vrai, surge ; sinon (`else`) confuse.
- **Pourquoi c'est faux** : la condition teste l'étourdissement au lieu de la confusion (`CardTemplate.gd` a deux fonctions distinctes, `is_confused` et `is_stunned`, l.3560-3566). Un héros déjà confus ne déclenche pas le surge ; un héros étourdi déclenche le surge sans être confus.
- **Correctif proposé** :
```json
"conditional_script": {"name": "conditional_script", "options": [{"condition": {"func_name": "is_confused", "func_params": {"subject": "my_identity"}}, "nested_tasks": [{"name": "surge"}]}], "else": [{"name": "mod_tokens", "modification": 1, "token_name": "confused", "subject": "my_identity"}]}
```
(seul `is_stunned` devient `is_confused` dans la clé existante)
- **Référence Narwhal** : `src/cards/pack/spiderham/spider_ham_nemesis/30028.py` (`IsConfused` puis surge sinon confuse).

### [spiderham] Huge Wooden Hammer (30010)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Interrupt: When Spider-Ham makes a basic attack, exhaust Huge Wooden Hammer and remove 1 toon counter from Spider-Ham → Spider-Ham gets +2 ATK for that attack. That attack gains overkill. »
- **Ce que fait le script Warnel** : `SetScripts_spiderham.json`, clé `Huge Wooden Hammer`, `interrupt_attack_started` avec `"event_filter":{"tags":["basic power"]}` (singulier).
- **Pourquoi c'est faux** : `OVUtils.gd` `filter_trigger` ne lit que `event_filters`. Le filtre est donc ignoré : l'interruption est proposée à chaque attaque de Spider-Ham (événements compris). Le coût (épuiser, retirer un toon) est payé pour une attaque non basique, et le `add_script` n'est retiré qu'à `basic_attack_happened`, donc +2 ATK et overkill peuvent rester en attente jusqu'à la prochaine attaque basique.
- **Correctif proposé** :
```json
"interrupt_attack_started": {"trigger": "Spider-Ham", "event_filters": {"tags": ["basic power"]}, ...reste inchangé }
```
- **Référence Narwhal** : `src/cards/pack/spiderham/spider_ham/30010.py`.

### [spiderham] The Green Gobbler (30026)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Forced Response: After The Green Gobbler engages you, discard all counters from each card you control. »
- **Ce que fait le script Warnel** : `SetScripts_spiderham.json`, clé `The Green Gobbler` : `remove_all_counters` avec `filter_state_seek:[{"filter_group":"group_friendly_my_hero"},{"filter_group":"upgrade_support_my_hero"}]`.
- **Pourquoi c'est faux** : les groupes de cartes s'appellent `group_upgrade_support<id>` (`CFConst.gd` `TYPES_TO_GROUPS`). `upgrade_support_my_hero` n'est pas un groupe de cartes (c'est un nom de grille, utilisé comme `source_grid` ailleurs), donc les améliorations et soutiens ne sont jamais vidés de leurs jetons. Les 9 autres usages dans le dépôt écrivent `group_upgrade_support_my_hero`.
- **Correctif proposé** :
```json
"filter_state_seek": [{"filter_group": "group_friendly_my_hero"}, {"filter_group": "group_upgrade_support_my_hero"}]
```
- **Référence Narwhal** : `src/cards/pack/spiderham/spider_ham_nemesis/30026.py`.

### [spiderham] Followed (30018)
- **Gravité** : mineure
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « Interrupt: When attached scheme is defeated, deal 4 damage to an enemy. »
- **Ce que fait le script Warnel** : `SetScripts_spiderham.json`, clé `Followed` : `"response":{"event_name":"card_dies","trigger":"host", ...}`.
- **Pourquoi c'est faux** : le texte est un Interrupt. Le motif utilisé par le dépôt pour les attachements qui réagissent à la mort de leur hôte est `interrupt_card_dies` + `trigger: host` (par exemple `SetScripts_cyclops.json` l.930). `response` + `card_dies` se déclenche après `die()` (`CardTemplate.gd`), quand l'hôte a déjà quitté le jeu et que ses attachements sont défaussés ; la carte risque de ne jamais se déclencher ou de le faire hors fenêtre.
- **Correctif proposé** :
```json
"interrupt_card_dies": {"trigger": "host", "all": [{"name": "deal_damage", "amount": 4, "subject": "target", "filter_state_subject": [{"filter_group": "group_enemies"}]}]}
```
- **Référence Narwhal** : n/a (30018 absent).

### [spiderham] Web of Life and Destiny (30023)
- **Gravité** : mineure
- **Certitude** : prouvée par le texte seul
- **Texte imprimé** : « Response: After a [[Web-Warrior]] ally leaves play, choose a player → that player draws 1 card. »
- **Ce que fait le script Warnel** : `SetScripts_spiderham.json`, clé `Web of Life and Destiny`, `card_leaves_play.filter_state_trigger = [{"filter_properties":{"trait_web-warrior":1,"comparison":"ge"}}]`.
- **Pourquoi c'est faux** : pas de filtre `type_code: ally`. N'importe quelle carte Web-Warrior (un héros Spider-Ham ou une amélioration/soutien portant le trait) qui quitte le jeu déclenche la pioche. La carte jumelle Warrior of the Great Web du même pack filtre bien sur `ally`.
- **Correctif proposé** :
```json
"filter_state_trigger": [{"filter_properties": {"trait_web-warrior": 1, "comparison": "ge"}, "filter_properties2": {"type_code": "ally"}}]
```
- **Référence Narwhal** : n/a (30023 absent).

### [drs] Astral Projection (09003)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Action (thwart): Choose a scheme → remove 3 threat from that scheme and look at the top card of the encounter deck. For each boost icon on that card, remove 1 additional threat from the chosen scheme. »
- **Ce que fait le script Warnel** : `SetScripts_drs.json`, clé `Astral Projection` : `thwart` avec `"filter_state_subject":[{"filter_groups":"group_schemes"}]`.
- **Pourquoi c'est faux** : `filter_groups` (pluriel) n'existe pas (aucune occurrence dans `src`, une seule dans tout `Sets/`). Le filtre est ignoré, la cible n'est plus limitée aux machinations. Images of Ikonn du même pack écrit correctement `filter_group`.
- **Correctif proposé** :
```json
{"name": "thwart", "subject": "target", "filter_state_subject": [{"filter_group": "group_schemes"}], "amount": {"func_name": "count_boost_icons", "func_params": {"subject": "previous"}}, "plus_amount": 3}
```
- **Référence Narwhal** : `src/cards/pack/drs/doctor_strange/09003.py` (cible `Scheme2`).

### [psylocke] Soaring Hearts (41020)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Action: Search your discard pile for an identity-specific event and add it to your hand. Ready Angel and Psylocke. »
- **Ce que fait le script Warnel** : `SetScripts_psylocke.json`, clé `Soaring Hearts`, `constraints` avec `"tags":["hero_ego_action"]`.
- **Pourquoi c'est faux** : `hero_ego_action` n'est pas dans `_tags_to_tags` (`ScriptingEngine.gd` ~l.3940) ni dans les cas de `constraints()`. Il n'est utilisé nulle part ailleurs. Aucune contrainte de forme héros ni de phase d'action n'est appliquée : la carte peut être jouée en forme alter-ego et hors fenêtre d'action. Les autres cartes d'équipe (Cyclops) utilisent `hero_action`.
- **Correctif proposé** :
```json
{"name": "constraints", "is_cost": true, "tags": ["hero_action"], "team_up": ["Angel", "Psylocke"]}
```
- **Référence Narwhal** : `src/cards/pack/psylocke/41020.py` (`AbilityType.HeroAction`).

### [psylocke] Directed Force (41019)
- **Gravité** : mineure
- **Certitude** : prouvée par le code (le fichier le reconnaît lui-même par `"TODO":"max 1 per attack"`)
- **Texte imprimé** : « ... that attack deals 2 additional damage. (Max 1 per attack.) »
- **Ce que fait le script Warnel** : `SetScripts_psylocke.json`, clé `Directed Force` : `interrupt_receive_damage` filtré sur `has_attack_keyword`, aucun test de limite.
- **Pourquoi c'est faux** : deux exemplaires peuvent s'empiler sur la même attaque (+4).
- **Correctif proposé** : marquer l'attaque lors de la première utilisation (par exemple `replacement_effect` avec `additional_tags:["directed_force"]` sur `interrupted_event`) et refuser le jeu si le tag est déjà présent. Je n'ai pas vérifié que le moteur sait exclure un tag dans `event_filters`, donc pas de JSON complet fourni.
- **Référence Narwhal** : `src/cards/pack/psylocke/41019.py` (`LimitOncePerEvent()`).

### [psylocke] Flurry of Blades (41004), Mental Detection (41005), Psionic Redirect (41006), Telepathic Suggestion (41007)
- **Gravité** : mineure (visible seulement si plusieurs joueurs ont des Psi-Knife / Psi-Katana en jeu)
- **Certitude** : prouvée par le code
- **Texte imprimé** : par exemple Mental Detection : « For each Psi-Knife you control, remove 2 additional threat ... For each Psi-Katana you control, draw 1 card. » (même formulation « you control » sur les quatre)
- **Ce que fait le script Warnel** : `SetScripts_psylocke.json`, les quatre clés comptent les cartes avec `"filter_state_seek":[{"filer_same_controller":true,"filter_properties":{"Name":"Psi-Knife"}}]` (ou `Psi-Katana`).
- **Pourquoi c'est faux** : `filer_same_controller` est une faute de frappe, la clé est ignorée (`ScriptProperties.gd`). Le comptage inclut les cartes de tous les joueurs. Le « you control » du texte n'est plus respecté.
- **Correctif proposé** : remplacer `filer_same_controller` par `filter_same_controller` dans les 4 scripts (8 occurrences dans le fichier, 2 par carte).
```json
"filter_state_seek": [{"filter_same_controller": true, "filter_properties": {"Name": "Psi-Knife"}}]
```
- **Référence Narwhal** : `src/cards/pack/psylocke/psylocke/41004.py`, `41005.py`, `41006.py`, `41007.py`.

### [ncrawler] Azazel's Sword (48029)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Attach to Azazel. Otherwise, attach to the villain. »
- **Ce que fait le script Warnel** : `SetScripts_ncrawler.json`, clé `Azazel's Sword`, `card_moved_to_board` : `{"name":"attach_to_card","subject":"Crossfire","is_cost":true}` puis, en `is_else`, attache au `villain`.
- **Pourquoi c'est faux** : la cible nommée est `Crossfire` (un autre méchant, présent dans `SetScripts_trors.json`) et non `Azazel`. Azazel n'est donc jamais choisi : l'épée va toujours au méchant (ou à Crossfire s'il est en jeu).
- **Correctif proposé** :
```json
{"name": "attach_to_card", "subject": "Azazel", "is_cost": true}
```
- **Référence Narwhal** : `src/cards/pack/ncrawler/nightcrawler_nemesis/48029.py` (`CardFinder(name="Azazel")`, repli `Villain`).

### [ncrawler] Prehensile Tail (48005)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « You can control 1 additional upgrade that has the restricted keyword. »
- **Ce que fait le script Warnel** : `SetScripts_ncrawler.json`, clé `Prehensile Tail` : alterant `restricted_limit` sur `my_identity` avec `"alteration": -1` et le commentaire « hack to make it count as 2 restricted » (copié de Kurt's Cutlasses).
- **Pourquoi c'est faux** : `GameData.gd` `check_restricted_limit` déclenche la règle quand le nombre de cartes restreintes dépasse `restricted_limit` (2 par défaut, `CFConst.gd`). -1 ramène la limite à 1, c'est l'inverse. Les cartes équivalentes (`SetScripts_vnm.json`, Flash Thompson) utilisent `+1`.
- **Correctif proposé** :
```json
"alterants": {"board": [{"filter_task": "get_property", "filter_property_name": "restricted_limit", "trigger": "my_identity", "alteration": 1}]}
```
- **Référence Narwhal** : `src/cards/pack/ncrawler/nightcrawler/48005.py` (`control_additional_restricted`).

### [ncrawler] Combine Forces (48031)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Action: Exhaust an [[X-Force]] character and an [[X-Men]] character → defeat a non-[[Elite]] minion. »
- **Ce que fait le script Warnel** : `SetScripts_ncrawler.json`, clé `Combine Forces` : `manual.hand` sans aucune tâche `constraints` avec `hero_action`.
- **Pourquoi c'est faux** : `SetScripts_All.gd` n'ajoute que `as_action` (qui équivaut à `action_ability`) pour un événement, pas `hero_form` (`ScriptingEngine.gd` `_tags_to_tags`). La carte peut donc être jouée en forme alter-ego. Gunboat Diplomacy, la carte sœur, a bien le `constraints`.
- **Correctif proposé** : ajouter en tête de `manual.hand` :
```json
{"name": "constraints", "is_cost": true, "tags": ["hero_action"]}
```
- **Référence Narwhal** : `src/cards/pack/ncrawler/48031.py` (`HeroAction`).

### [ncrawler] Executioner (48036)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Revealed: Executioner attacks the friendly character with the fewest remaining hit points. If this attack defeats an ally, remove that ally from the game. »
- **Ce que fait le script Warnel** : `SetScripts_ncrawler.json`, clé `Executioner` : `card_defeated` avec `event_filters:{"source":"self","tags":["executioner"]}` puis `move_card_to_container` du `trigger` vers `removed_from_game`, sans filtre de type.
- **Pourquoi c'est faux** : `group_friendly` contient les héros et alter-egos (`CFConst.gd` `TYPES_TO_GROUPS`), et `CardTemplate.die` émet `card_defeated` pour eux aussi. Si l'identité du joueur est la cible la plus fragile et que l'attaque la bat, elle est retirée de la partie, ce que le texte réserve aux alliés.
- **Correctif proposé** :
```json
"card_defeated": {"event_filters": {"source": "self", "tags": ["executioner"]}, "filter_state_trigger": [{"filter_properties": {"type_code": "ally"}}], "all": [{"name": "move_card_to_container", "subject": "trigger", "dest_container": "removed_from_game"}]}
```
- **Référence Narwhal** : `src/cards/pack/ncrawler/crazy_gang/48036.py` (`if Ally.IsType(face)`).

---

## Totaux

Cartes auditées : 190 (ironheart 43, spiderham 39, drs 37, psylocke 35, ncrawler 36 ; l'entrée `_macros` n'est pas une carte)

Cartes avec erreur prouvée : 20 (17 blocs ci-dessus, dont un bloc commun à 4 cartes)

Cartes OK : 158 (190 moins 20 erreurs prouvées moins 12 incertaines)

Effets de campagne non gérés (non listés) : 0 constaté dans ce lot, les packs héros ne contiennent pas de mode campagne.

Cartes incertaines (non prouvées, à tester en jeu) :
- [ironheart] Zzzap! (29040) : « dealt 1 or fewer damage » est approché par le nombre d'énergies en main (<=1), les dégâts indirects peuvent être répartis sur des alliés.
- [ironheart] Ironheart V3 (29003a) : tag `action_ability` alors que le texte est « Hero Action », sans effet probable sur une face héros.
- [ironheart] Bombshell : répartition équitable des dégâts, non démontrée.
- [drs] Counterspell (09030) : la carte contrôlée par le méchant, `filter_same_controller` évalué sur quel joueur ? Non vérifié.
- [drs] Physical Toll (09027) : même doute sur `filter_same_controller` dans l'alterant de coût.
- [drs] The Night Nurse (09019) : le retrait du statut est un coût, impossible de soigner un héros sans statut alors que le texte n'exige pas qu'il en ait un.
- [drs] Iron Fist (09014) : déclencheur `interrupt_pre_receive_damage` avec `trigger: self`, pas clair qu'il couvre « When Iron Fist attacks an enemy ».
- [drs] Astral Projection : l'ordre regarder la carte puis choisir la machination n'est pas celui du texte (point secondaire, non prouvé).
- [psylocke] Psionic Illusion (41028) : un [wild] imprimé compte-t-il comme le type nommé ? Règle non cherchée dans le Rules Reference.
- [psylocke] IPAC (41022) : « deal 1 facedown encounter card → draws 2 » : le script pioche avant de distribuer la carte, ordre coût puis effet inversé, effet réel non démontré.
- [psylocke] Domino (41031) : tâches `is_cost` mêlées à `move_card_to_container subject previous`, risque de remettre la carte piochée au lieu de la carte choisie.
- [ncrawler] Queen of Hearts (48034) : « (Shuffle.) » absent du script, mais le moteur mélange peut-être automatiquement après `deal_encounter` d'un tutor.


---

## Audit Warnel, lot 11

Fichiers audités : `Sets/SetScripts_winter.json`, `vision`, `valk`, `cyclops`, `wsp`, `scw`, `wolv` (232 entrées).
Moteur lu : `src/core/ScriptingEngine/ScriptObject.gd`, `ScriptProperties.gd`, `src/core/CFControl.gd`, `src/wc/OVUtils.gd`, `src/wc/CardTemplate.gd`, `src/wc/ScriptingEngine/ScriptingEngine.gd`, `src/core/BoardTemplate.gd`.
Textes imprimés : `Sets/SetDefinition_<pack>.json` de Warnel. Rappel de sémantique utilisée : `filter_state_<x>` est une liste de blocs en OU, et chaque bloc est un ET (`ScriptProperties.check_validity`, l.1726). La comparaison de chaîne `eq` est sensible à la casse (`CFUtils.compare_strings`, l.311).

---

### [vision] Joining Forces (26035)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Action: As a group, the players put a total of 1 [[Avenger]] ally and 1 [[Guardian]] ally into play from their hand(s). »
- **Ce que fait le script Warnel** : `SetScripts_vision.json`, clé `Joining Forces`, `manual.hand[2]` : `"src_container": "hand_any"`. Le premier `move_card_to_board` utilise `"any_hand"`.
- **Pourquoi c'est faux** : `hand_any` n'existe pas. `CardTemplate.gd` (~l.2757-2790, remplacement des zones) crée `any_hand` (liste des mains de tous les joueurs) et `hand_my_hero`, `hand_first_player`, `hand_active_player` (`OVUtils.gd` l.712). Aucun remplacement ne produit `hand_any`. La chaîne reste telle quelle, `CFControl.get_all_cards_from_containers` (l.323) ne trouve ni `NMAP["hand_any"]` ni grille de ce nom (`BoardTemplate.get_grid`, l.95), donc la liste de cartes est vide. L'allié Guardian n'est jamais proposé : seule la moitié de l'effet est jouée. Le nom `hand_any` n'apparaît dans aucun autre script du dépôt (seule occurrence : cette clé).
- **Correctif proposé** :
```json
"Joining Forces": {
  "manual": {
    "hand": [
      {"name": "constraints", "is_cost": true, "tags": ["hero_action"]},
      {"name": "move_card_to_board", "subject": "tutor", "subject_count": "all", "needs_selection": true, "selection_count": 1, "selection_type": "max", "selection_optional": true, "src_container": "any_hand", "filter_state_tutor": [{"filter_properties": {"type_code": "ally"}, "filter_properties2": {"trait_avenger": 1}}]},
      {"name": "move_card_to_board", "subject": "tutor", "subject_count": "all", "needs_selection": true, "selection_count": 1, "selection_type": "max", "selection_optional": true, "src_container": "any_hand", "filter_state_tutor": [{"filter_properties": {"type_code": "ally"}, "filter_properties2": {"trait_guardian": 1}}]}
    ]
  }
}
```
- **Référence Narwhal** : `src/cards/pack/vision/26035.py`

---

### [valk] Leadership Training (25034)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Alter-ego Action: Exhaust this card and remove 1 training counter from it → choose a leadership (blue) event in you discard pile and shuffle it into your deck. »
- **Ce que fait le script Warnel** : `SetScripts_valk.json`, clé `Leadership Training`, `manual.board[3]` : `"filter_state_tutor": [{"filter_properties": {"faction_code": "Leadership"}}]`.
- **Pourquoi c'est faux** : (1) les définitions de cartes stockent `faction_code` en minuscules (`SetDefinition_valk.json` : `"leadership"`, `"aggression"`, `"basic"`, et tous les autres scripts écrivent `"aggression"`, `"leadership"`, `"justice"` en minuscules) et `check_properties` compare avec `CFUtils.compare_strings`, strictement sensible à la casse. `"Leadership"` ne correspond donc à aucune carte : l'action ne trouve jamais de cible. (2) Il n'y a aucun filtre `type_code: event`, alors que le texte limite à un événement : une fois la casse corrigée, n'importe quelle carte Leadership de la défausse (allié, soutien) serait proposée.
- **Correctif proposé** :
```json
"filter_state_tutor": [{"filter_properties": {"faction_code": "leadership"}, "filter_properties2": {"type_code": "event"}}]
```
(remplacer ce seul tableau dans `manual.board[3]` ; le reste de la clé est inchangé.)
- **Référence Narwhal** : `src/cards/pack/valk/25034.py` (`SetTarget(Event, card_class="Leadership", from_where=["YourDiscardPile"])`)

---

### [valk] Hall of Heroes (25016)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Alter-Ego Action: Exhaust Hall of Heroes and remove 3 glory counters from it → draw 3 cards. »
- **Ce que fait le script Warnel** : `SetScripts_valk.json`, clé `Hall of Heroes`, `manual.board` : `constraints`, `mod_tokens glory -3 (is_cost)`, `draw_cards 3`. Pas d'`exhaust_card`.
- **Pourquoi c'est faux** : le coût « exhaust » est imprimé mais absent. Le moteur ne l'ajoute pas pour un `manual` de support (les ajouts de `SetScripts_All.get_scripts` concernent coût de jeu, traits d'attaque/défense et « max per »). Résultat : la carte reste redressée et peut être réutilisée dès qu'elle a 3 jetons, plusieurs fois par tour. Comparer avec `Logan's Cabin` (`SetScripts_wolv.json`) qui code bien `exhaust_card` en coût.
- **Correctif proposé** :
```json
"manual": {
  "board": [
    {"name": "constraints", "is_cost": true, "tags": ["alter_ego_action"]},
    {"name": "exhaust_card", "is_cost": true, "subject": "self"},
    {"name": "mod_tokens", "subject": "self", "modification": -3, "token_name": "glory", "is_cost": true},
    {"name": "draw_cards", "amount": 3}
  ]
}
```
- **Référence Narwhal** : n/a (module non présent dans `pack/valk`)

---

### [valk] Valhalla (25004)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « Response: After Valkyrie attacks and defeats the enemy that has Death-Glow attached, exhaust Valhalla → draw 1 card and heal 1 damage from Valkyrie. »
- **Ce que fait le script Warnel** : `SetScripts_valk.json`, clé `Valhalla`, `interrupt_card_dies.board[2]` : `{"name": "heal", "amount": 2, "subject": "Valkyrie"}`.
- **Pourquoi c'est faux** : le script soigne 2, le texte imprimé dit 1. Le moteur applique `amount` tel quel (`ScriptingEngine.heal`).
- **Correctif proposé** :
```json
{"name": "heal", "amount": 1, "subject": "Valkyrie"}
```
- **Référence Narwhal** : n/a (module non présent dans `pack/valk`)

---

### [vision] Side Step (26019)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Interrupt (defense): When you would take any amount of damage, prevent 3 of that damage. If you paid for this card using [energy] resource, deal 1 damage to that enemy. »
- **Ce que fait le script Warnel** : `SetScripts_vision.json`, clé `Side Step`, `card_played.all[0]` : `{"name": "deal_damage", "amount": 1, "subject": "target", "needs_subject": true, "filter_state_subject": [{"filter_group": "group_enemies"}]}`.
- **Pourquoi c'est faux** : « that enemy » est l'ennemi qui attaque. `subject: "target"` + `needs_subject` fait choisir au joueur n'importe quel ennemi en jeu. Le moteur connaît le sujet qui convient : `current_activation_enemy` (`SP.gd` l.26, `OVUtils.gd` l.204), déjà utilisé dans ce même fichier (`Flow Like Water`, ligne 367).
- **Correctif proposé** :
```json
{"name": "deal_damage", "amount": 1, "subject": "current_activation_enemy"}
```
- **Référence Narwhal** : n/a (module non présent dans `pack/vision`)

---

### [valk] Cosmic Alliance (25036)
Fichier `SetScripts_valk.json`, clé `Cosmic Alliance`.
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Action: Choose an [[avenger]] character and a [[guardian]] character → ready each of those characters. »
- **Ce que fait le script Warnel** : deux `ready_card` avec `"subject": "boardseek"` et `filter_state_seek` (`group_friendly` + `trait_avenger` / `trait_guardian`), sans `needs_selection` ni `subject_count`.
- **Pourquoi c'est faux** : `ScriptObject._local_find_subjects` (l.475) ne demande un choix au joueur que si `needs_selection` est vrai (défaut faux, `ScriptProperties.get_default` l.1278). `_boardseek_subjects` (l.544) prend alors simplement le premier personnage correspondant dans l'ordre des noeuds (`subject_count` défaut 1, l.1305). Le joueur ne choisit donc pas, alors que le texte dit « Choose ».
- **Correctif proposé** :
```json
"Cosmic Alliance": {
  "manual": {
    "hand": [
      {"name": "constraints", "is_cost": true, "tags": ["hero_action"]},
      {"name": "ready_card", "subject": "boardseek", "subject_count": "all", "needs_selection": true, "selection_count": 1, "selection_type": "equal", "filter_state_seek": [{"filter_group": "group_friendly", "filter_properties": {"trait_avenger": 1}}]},
      {"name": "ready_card", "subject": "boardseek", "subject_count": "all", "needs_selection": true, "selection_count": 1, "selection_type": "equal", "filter_state_seek": [{"filter_group": "group_friendly", "filter_properties": {"trait_guardian": 1}}]}
    ]
  }
}
```
- **Référence Narwhal** : `src/cards/pack/valk/25036.py`

---

### [valk] Problem Solvers (25033)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hero Action (thwart): Exhaust an [[avenger]] character and a [[guardian]] character → remove X threat from each scheme, where X is equal to the combined THW of those characters. »
- **Ce que fait le script Warnel** : `SetScripts_valk.json`, clé `Problem Solvers`, deux `exhaust_card` (`is_cost`) avec `subject: "boardseek"` sans `needs_selection`.
- **Pourquoi c'est faux** : même mécanisme que Cosmic Alliance : le moteur choisit automatiquement le premier Avenger et le premier Guardian du plateau, le joueur ne choisit pas (et ne peut pas choisir celui dont la valeur de THW est la meilleure, ce qui change X).
- **Correctif proposé** : ajouter `"subject_count": "all", "needs_selection": true, "selection_count": 1, "selection_type": "equal"` aux deux tâches `exhaust_card`, comme dans le bloc de Cosmic Alliance ci-dessus (le reste de la clé est inchangé).
```json
{"name": "exhaust_card", "is_cost": true, "subject": "boardseek", "subject_count": "all", "needs_selection": true, "selection_count": 1, "selection_type": "equal", "filter_state_seek": [{"filter_group": "group_friendly", "filter_properties": {"trait_avenger": 1}}]}
```
(et la même tâche avec `"trait_guardian": 1`.)
- **Référence Narwhal** : `src/cards/pack/valk/25033.py`

---

### [valk] Powerful Enchantments (25030)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Hinder 1[per_hero]. Players cannot discard attachments that are attached to friendly characters. »
- **Ce que fait le script Warnel** : `SetScripts_valk.json`, clé `Powerful Enchantments` : `{"TODO": "", "hinder": {"__amount__": 1, "__each_player__": true}}`.
- **Pourquoi c'est faux** : la clé `TODO` laisse l'effet imprimé non codé. Aucune propriété `cannot_discard` n'existe dans le moteur (recherche dans `src/` : aucune occurrence, ni de `Powerful Enchantments`). Les attachements aux personnages alliés peuvent donc être défaussés librement.
- **Correctif proposé** : il faut une propriété moteur. Esquisse : ajouter `cannot_discard` à `CardConfig.PROPERTIES_NUMBERS`, la refuser dans la fonction de défausse d'attachement (`ScriptingEngine.discard` / action manuelle de défausse), puis dans le JSON :
```json
"Powerful Enchantments": {
  "hinder": {"__amount__": 1, "__each_player__": true},
  "alterants": {
    "board": [
      {"filter_task": "get_property", "filter_property_name": "cannot_discard",
       "filter_state_trigger": [{"filter_properties": {"type_code": "attachment"}, "filter_group": "group_friendly_attachments"}],
       "alteration": 1}
    ]
  }
}
```
Ce JSON est indicatif : `group_friendly_attachments` est à créer ou remplacer par le groupe qui existe dans votre `CFConst`. Sans le correctif GDScript, seule la suppression de `TODO` est sûre.
- **Référence Narwhal** : n/a

---

### [vision] Ultron Unleashed (26030)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Revealed: Search the encounter deck, discard pile, and set-aside area for Ultron Drones and put it into play. Shuffle the encounter deck. Each player puts the top card of their deck into play facedown, engaged with them as a [[Drone]] minion. »
- **Ce que fait le script Warnel** : `SetScripts_vision.json`, clé `Ultron Unleashed`, `reveal.all` : `deal_encounter` puis la macro `ultron_drone`. Pas de `shuffle_container`.
- **Pourquoi c'est faux** : `deal_encounter` (`ScriptingEngine.gd` l.3287) ne mélange pas, et seul `shuffle_container` (l.331) mélange le paquet. Les autres scripts qui ont le même texte le codent explicitement (`SetScripts_aos.json` l.1135, `SetScripts_aoa.json` l.1274).
- **Correctif proposé** : insérer entre les deux tâches
```json
{"name": "shuffle_container", "dest_container": "deck_villain"}
```
- **Référence Narwhal** : n/a

---

### [valk] Enchantress (25029)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Revealed: Search the encounter deck, discard pile, and set-aside area for a copy of Seduced and attach it to your identity. (Shuffle.) »
- **Ce que fait le script Warnel** : `SetScripts_valk.json`, clé `Enchantress`, `reveal.all` : un seul `move_card_to_board` (tutor `Seduced`, `grid_name: enemies_my_hero`). Pas de `shuffle_container`.
- **Pourquoi c'est faux** : même cause que Ultron Unleashed : aucune des tâches de pioche/déplacement ne mélange (`ScriptingEngine.gd`, seules l.331-374). (Le rattachement à l'identité est assuré par `Seduced.self_moved_to_board`, il n'y a donc pas d'erreur de ce côté.)
- **Correctif proposé** : ajouter à la suite
```json
{"name": "shuffle_container", "dest_container": "deck_villain"}
```
- **Référence Narwhal** : n/a

---

### [cyclops] Genetic Manipulation (33029)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « When Defeated: Search the encounter deck and discard pile for Gene Therapy and reveal it. (Shuffle.) »
- **Ce que fait le script Warnel** : `SetScripts_cyclops.json`, clé `Genetic Manipulation`, `card_defeated.all` : un seul `deal_encounter`. Pas de `shuffle_container`.
- **Pourquoi c'est faux** : même cause (aucun mélange automatique dans `deal_encounter`).
- **Correctif proposé** : ajouter dans `card_defeated.all`
```json
{"name": "shuffle_container", "dest_container": "deck_villain"}
```
- **Référence Narwhal** : n/a

---

## Pied de rapport

Cartes auditées : 232
Cartes OK : 212 (232 moins 11 erreurs prouvées moins 9 incertaines)
Erreurs prouvées : 11 (Joining Forces, Leadership Training, Hall of Heroes, Valhalla, Side Step, Cosmic Alliance, Problem Solvers, Powerful Enchantments, Ultron Unleashed, Enchantress, Genetic Manipulation)
Effets de campagne non gérés (non listés) : 0 relevé dans ce lot (pas de comptage systématique, aucun repéré)

Pack `wolv` (35 cartes) : aucune erreur prouvée. Pistes écartées après lecture du moteur : `filter_state_seek` utilisé avec `subject: "target"` (Giant Help, Wasp Sting) fonctionne, car `ScriptObject.gd` l.367 et `OVUtils.gd` l.31 recopient `filter_state_subject` dans `filter_state_seek`; Wasp #13001a `card_dies` avec deux blocs dans `filter_state_trigger` est correct (les blocs sont en OU, `check_validity` l.1726).

### Cartes incertaines (non prouvées, à tester en jeu)
- [vision] Ultron Drones (26031) : « Forced Response: After a facedown Drone minion is defeated, place that card in its owner's discard pile » absent du script (alterants seuls); non prouvé qu'aucun code générique ne gère la destination.
- [valk] The Best Defense… (25020) : « Hero Interrupt » codé en `response` sur `enemy_attack_damage`; non prouvé que l'alterant arrive trop tard.
- [wsp] Wasp #13001a : « (or an event you play) » ; le filtre `event_filters.source: "self"` pourrait exclure les événements, source réelle de l'événement non vérifiée.
- [cyclops] Full Blast (33008) : `tags: ["!basic power"]` accepte toute attaque non basique, tags réels d'Optic Blast non vérifiés.
- [cyclops] Field Commander (33004) : clé `filter_same_controler` mal orthographiée (ignorée ?) et pas de limite à « attached to a minion »; effet réel non testé.
- [vision] Solar Beam (26008) : double trait Attack et Thwart, risque de blocage par les contraintes automatiques si Vision est Intangible; non testé.
- [winter] Firepower (54014) : une attaque unique à 3 par arme épuisée au lieu d'une attaque par arme; ciblage non vérifié.
- [winter] Man on the Wall (54019) : portée de la réduction de coût (tous les joueurs, toutes les cartes) non vérifiée.
- [wolv] Wolverine's Claws (35002) : `subject: "self"` dans `additional_scripts` (dégâts égaux au coût imprimé de l'événement joué) non vérifié.


---

## Audit Warnel lot 12 : stld, gambit, phoenix, ant, nebu, warm, gam, cap, msm

Fichiers : Sets/SetScripts_{stld,gambit,phoenix,ant,nebu,warm,gam,cap,msm}.json. Textes imprimés : SetDefinition_<pack>.json (cap et warm : API marvelcdb).

### [stld] Banishment (17024)
- **Gravité** : bloquante
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Discard an Element Gun from play. If you cannot, place 3 threat on the main scheme. Discard this obligation. »
- **Ce que fait le script Warnel** : SetScripts_stld.json, clé `Banishment`, sections `Flip then Discard` et `Discard` : le `conditional_script` donne `"nested_scripts": [ {discard Element Gun} ]` dans l'option.
- **Pourquoi c'est faux** : `ScriptingEngine.conditional_script` (src/wc/ScriptingEngine/ScriptingEngine.gd l.1750) lit `script.get_sub_property("nested_tasks", option, {})`. La clé `nested_scripts` n'existe nulle part dans src (grep vide) : le sous-script est `{}`. Quand un Element Gun est en jeu, la condition est vraie, rien n'est défaussé, et le `else` (3 menaces) n'est pas joué non plus. L'Element Gun n'est donc jamais défaussé.
- **Correctif proposé** : renommer `nested_scripts` en `nested_tasks` dans les deux occurrences.
```json
{ "name": "conditional_script", "options": [ { "condition": { "func_name": "card_is_in_play", "func_params": { "card_name": "Element Gun" } }, "nested_tasks": [ { "name": "discard", "subject": "boardseek", "filter_state_seek": [ { "filter_properties": { "Name": "Element Gun" } } ] } ] } ], "else": [ { "name": "add_threat", "amount": 3, "subject": "main_scheme" } ] }
```
- **Référence Narwhal** : n/a (non consulté pour cette carte)

### [stld] Blaze of Glory (17015)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « Each [[guardian]] character gets +2 THW and +2 ATK this phase. »
- **Ce que fait le script Warnel** : SetScripts_stld.json, `Blaze of Glory`.manual.hand, `temporary_effect.effect.alterants.all` : deux alterants identiques, tous deux `"filter_property_name": "attack"`, `"alteration": 2`.
- **Pourquoi c'est faux** : aucun alterant `thwart`. Les guardians reçoivent +4 ATK et 0 THW. La propriété `thwart` est celle utilisée par les autres cartes (ex. Morale Boost, msm).
- **Correctif proposé** : remplacer la 2e entrée par `thwart`.
```json
{ "filter_task": "get_property", "filter_property_name": "thwart", "filter_state_trigger": [ { "filter_group": "group_characters", "filter_properties": { "trait_guardian": 1, "comparison": "ge" } } ], "alteration": 2 }
```
- **Référence Narwhal** : n/a

### [stld] Yondu (17013)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Yondu's attacks gain ranged. »
- **Ce que fait le script Warnel** : `Yondu` : `{ "attacks_gain": { "__trigger__": "self", "__tags__": "piercing" } }`.
- **Pourquoi c'est faux** : la macro `attacks_gain` (Sets/_macros.json) ajoute le tag fourni aux attaques. `piercing` ignore le Toughness/Tough, `ranged` ignore le Retaliate : ce sont deux tags distincts (CFConst.gd l.768 et l.770, ScriptingEngine.gd l.1149). Les autres cartes "gain ranged" utilisent `"__tags__": "ranged"`.
- **Correctif proposé** :
```json
{ "attacks_gain": { "__trigger__": "self", "__tags__": "ranged" } }
```
- **Référence Narwhal** : n/a

### [gambit] Acolyte Frenzy (37035)
- **Gravité** : bloquante
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « Each [[ACOLYTE]] minion engaged with you activates against you. If you are not engaged with an [[ACOLYTE]] minion, this card gains surge. »
- **Ce que fait le script Warnel** : SetScripts_gambit.json, `reveal.all[0]` : `"filter_state_seek": [ { "filter_properties": { "trait_assassin": 1 }, "filter_properties2": { "type_code": "minion" }, "filter_same_controller": true } ]`.
- **Pourquoi c'est faux** : le filtre cherche le trait `assassin` au lieu de `acolyte`. Les sbires Acolyte n'activent jamais, et si un sbire Assassin est engagé il active à tort. Le surge se déclenche donc à tort.
- **Correctif proposé** : `"filter_properties": { "trait_acolyte": 1 }` (même forme que le reste du filtre).
- **Référence Narwhal** : n/a

### [msm] Sneak By (05004)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « Hero Action (thwart): Remove 3 threat from a scheme. »
- **Ce que fait le script Warnel** : SetScripts_msm.json, `Sneak By`.manual.hand : `{ "name": "thwart", "amount": 4, ... }`.
- **Pourquoi c'est faux** : 4 menaces retirées au lieu de 3.
- **Correctif proposé** : `"amount": 3`.
- **Référence Narwhal** : n/a

### [msm] Harvest (05029)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « Exhaust each [[Persona]] support in play. For each support exhaust this way, the villain heals 1 damage. If no [[Persona]] support was exhausted this way, this card gains surge. »
- **Ce que fait le script Warnel** : `Harvest`.reveal.all : `exhaust_card` (boardseek, trait_persona, non épuisés) puis `{ "name": "surge", "is_else": true }`.
- **Pourquoi c'est faux** : aucune tâche de soin. Le vilain ne guérit jamais 1 dégât par support épuisé.
- **Correctif proposé** : ajouter une tâche `heal` sur le vilain, avec le motif déjà utilisé ailleurs (`"subject": "villain"` dans Preemptive Strike, `"amount": "count_previous_subjects"` dans Strength In Numbers). Position par rapport au `surge` `is_else` à valider en jeu.
```json
{ "name": "heal", "subject": "villain", "amount": "count_previous_subjects" }
```
- **Référence Narwhal** : n/a

### [warm] As One! (23032)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « ... deal X damage to an enemy, where X is the combined ATK of those characters. This attack gains overkill. »
- **Ce que fait le script Warnel** : SetScripts_warm.json, `As One!`.manual.hand, tâche `attack` : `amount` = somme des `attack` de `all_previous`, `subject: target`, aucun `tags`.
- **Pourquoi c'est faux** : l'overkill est lu dans les tags de l'attaque (ScriptingEngine.gd l.1148 : `"overkill" in tags`). Sans tag, l'attaque n'a pas overkill. Full Auto (même pack) met bien `"tags": ["overkill"]`.
- **Correctif proposé** : ajouter `"tags": ["overkill"]` à la tâche `attack`.
- **Référence Narwhal** : n/a

### [warm] Upgraded Chassis (23004)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « War Machine gains the [[aerial]] trait. »
- **Ce que fait le script Warnel** : `alterants.board[0]` : `"filter_property_name": "trait_aerial", "filter_state_trigger": [ { "filter_card_name": "War Machine" } ], "alteration": 1`.
- **Pourquoi c'est faux** : `filter_card_name` n'est lu que comme clé de script de premier niveau (ScriptProperties.gd l.1479). Dans un `filter_state_trigger`, `check_validity` (ScriptProperties.gd l.1726, SP.gd l.464) ignore les clés inconnues : le dictionnaire est vide et accepte toute carte. Toutes les cartes gagnent le trait aerial, pas seulement War Machine.
- **Correctif proposé** (même motif que Captain America's Shield, cap) :
```json
{ "filter_task": "get_property", "filter_property_name": "trait_aerial", "filter_state_trigger": [ { "filter_properties": { "Name": "War Machine" } } ], "alteration": 1 }
```
- **Référence Narwhal** : n/a

### [nebu] Defensive Training (22034) et [warm] Vigilante Training (23033)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « ... choose a Protection (green) event in your discard pile and shuffle it into your deck. » (Vigilante Training : « a justice (yellow) event »)
- **Ce que fait le script Warnel** : `shuffle_card_into_container` avec `"filter_state_tutor": [ { "filter_properties": { "faction_code": "protection" } } ]` (Vigilante : `"justice"`).
- **Pourquoi c'est faux** : aucun filtre `type_code: event`. N'importe quelle carte Protection (allié, amélioration, soutien) de la défausse est proposée.
- **Correctif proposé** :
```json
"filter_state_tutor": [ { "filter_properties": { "faction_code": "protection" }, "filter_properties2": { "type_code": "event" } } ]
```
  (idem avec `"justice"` pour Vigilante Training)
- **Référence Narwhal** : nebu/22034.py

### [ant] Wrist Gauntlets (12010), option "Confuse"
- **Gravité** : bloquante
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « Hero Action: If you are in [[Tiny]] hero form, exhaust Wrist Gauntlets and spend [energy][energy] resources → confuse an enemy. »
- **Ce que fait le script Warnel** : SetScripts_ant.json, `Wrist Gauntlets`.manual.board["Confuse"] : `"constraints": [ { "func_name": "identity_has_trait", "func_params": { "trait": "giant" } } ]`, puis `mod_tokens` avec `"token_name": "stunned"`.
- **Pourquoi c'est faux** : deux erreurs. (1) La contrainte exige la forme Giant, comme l'option "Stun" : elle ne peut pas être jouée en forme Tiny, la seule où le texte l'autorise. (2) Le jeton posé est `stunned` au lieu de `confused`.
- **Correctif proposé** :
```json
"Confuse": [ { "name": "constraints", "is_cost": true, "tags": [ "hero_action" ], "constraints": [ { "func_name": "identity_has_trait", "func_params": { "trait": "tiny" } } ] }, { "name": "exhaust_card", "is_cost": true, "subject": "self" }, { "name": "pay_cost", "cost": { "energy": 2 }, "is_cost": true }, { "name": "mod_tokens", "token_name": "confused", "modification": 1, "subject": "target", "needs_subject": true, "filter_state_subject": [ { "filter_group": "group_enemies" } ] } ]
```
- **Référence Narwhal** : n/a

### [ant] Ant-Man allié (12011)
- **Gravité** : mineure
- **Certitude** : prouvée par le code
- **Texte imprimé** : « ... place 1 pym counter on him (to a maximum of 4) for each resource you overpaid ... »
- **Ce que fait le script Warnel** : `self_moved_to_board.board[0]` : `mod_tokens` pym, `modification: { func_name: get_overpaid_amount }`, `"max_modification": 4`.
- **Pourquoi c'est faux** : la clé `max_modification` n'est lue nulle part dans src : le plafond de 4 n'est pas appliqué.
- **Correctif proposé** : implémenter le plafond dans `mod_tokens` (côté moteur), ou borner la valeur de `get_overpaid_amount`. Je n'ai pas de correctif JSON vérifié.
- **Référence Narwhal** : n/a

### [nebu] Gamora, sbire némésis (22028)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « [star] Forced Response: After Gamora attacks and damages you, choose and discard an upgrade you control. »
- **Ce que fait le script Warnel** : SetScripts_nebu.json, `Gamora #22028` : seulement `self_moved_to_board` (défausse de l'allié Gamora). Aucune autre clé.
- **Pourquoi c'est faux** : la Forced Response d'attaque n'est pas scriptée.
- **Correctif proposé** : ajouter un déclencheur sur dégâts d'attaque infligés au héros qui défausse une amélioration choisie. Je n'ai pas de JSON vérifié pour l'événement de déclenchement.
- **Référence Narwhal** : nebu/nebula_nemesis/22028.py

### [phoenix] Mutant Peacekeepers (34018)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « Exhaust your hero and any number of [[X-MEN]] allies → remove X threat ... where X is the total THW of those characters. »
- **Ce que fait le script Warnel** : 2e `exhaust_card` : `"selection_needed": true, "selection_optional": true, "selection_type": "min", "selection_count": 1, "subject": "boardseek", "subject_count": "all"`.
- **Pourquoi c'est faux** : `selection_needed` n'existe pas (la clé est `needs_selection`, KEY_NEEDS_SELECTION). Sans elle, `boardseek` choisit automatiquement les premiers alliés au lieu de laisser le joueur choisir. Le total de THW en dépend.
- **Correctif proposé** : remplacer `selection_needed` par `needs_selection`.
```json
{ "name": "exhaust_card", "subject": "boardseek", "subject_count": "all", "needs_selection": true, "selection_optional": true, "selection_type": "min", "selection_count": 1, "filter_state_seek": [ { "filter_group": "group_allies_my_hero", "filter_properties": { "trait_x-men": 1, "comparison": "ge" }, "filter_is_exhausted": false } ] }
```
- **Référence Narwhal** : phoenix/34018.py

### [phoenix] Psychic Misdirection (34033)
- **Gravité** : partielle
- **Certitude** : prouvée par le code
- **Texte imprimé** : « choose a different enemy → damage from that attack is dealt to the chosen enemy instead of you. »
- **Ce que fait le script Warnel** : `nop` avec `needs_selection` : `"filter_state_seek": [ { "filer_group": "group_enemies" } ]`.
- **Pourquoi c'est faux** : `filer_group` est une faute de frappe. La clé est ignorée, le filtre est vide et toute carte du plateau est choisissable (allié, héros, plan...), pas seulement un ennemi.
- **Correctif proposé** :
```json
"filter_state_seek": [ { "filter_group": "group_enemies" } ]
```
- **Référence Narwhal** : n/a

### [phoenix] Cerebro (34022)
- **Gravité** : partielle
- **Certitude** : prouvée par le texte seul (à confirmer en jeu)
- **Texte imprimé** : « search the top 5 cards of your deck for an [[X-MEN]] ally (search your whole deck instead if you control a [[PSIONIC]] character) »
- **Ce que fait le script Warnel** : `move_card_to_container` avec `"subject_count": 5` fixe.
- **Pourquoi c'est faux** : la variante PSIONIC (tout le deck) n'est pas gérée.
- **Correctif proposé** : brancher via `conditional_script` (options/`nested_tasks`, `else`) : `subject_count: "all"` si on contrôle un personnage Psionic, sinon 5. Non vérifié en jeu.
- **Référence Narwhal** : phoenix/34022.py

---
Cartes auditées : 290 (stld 32, gambit 33, phoenix 34, ant 32, nebu 33, warm 33, gam 30, cap 32, msm 31)
Cartes OK : 264 (290 moins 16 en erreur et 10 incertaines)
Effets de campagne non gérés (non listés) : 0 relevé
Erreurs prouvées : 16 (Banishment, Blaze of Glory, Yondu, Acolyte Frenzy, Sneak By, Harvest, As One!, Upgraded Chassis, Defensive Training, Vigilante Training, Wrist Gauntlets, Ant-Man allié, Gamora 22028, Mutant Peacekeepers, Psychic Misdirection, Cerebro)

Cartes incertaines (non prouvées, à tester en jeu)
- [stld] Cosmo (17020) : texte/JSON divergent, sémantique moteur non vérifiée.
- [stld] Peter Quill, Smooth Talker : le déplacement vers le deck puis `draw_cards` peut redonner la même carte (échange non garanti), dépend de l'index par défaut.
- [nebu] Giant Strength : écart possible, non prouvé.
- [gambit] The Assassins Guild : filtres `filter_state_event_source` (type ally) et `filter_state_actual_source` dans `event_filters` d'apparence contradictoire.
- [gambit] War Room : clé `ais_cost` (faute de frappe, exhaust non marqué coût), mais `exhaustme` renvoie OK sur une carte déjà épuisée (CardTemplate.gd l.2378), effet réel non prouvé.
- [cap] Captain America's Helmet : `heal` avec `set_to_mod: true, amount: 1` pour "set hit point dial to 1", sémantique non vérifiée.
- [cap] Baron Zemo : l'alterant `cannot_thwart` ne semble pas conditionné à l'engagement.
- [cap] Quincarrier (warm) et Honorary Avenger : "Play only if your identity has the Avenger trait" absent du JSON, peut être géré hors script.
- [warm] Iron Man : "Shuffle your deck" absent du JSON, mélange peut être implicite.
- [gam] Gamora 18001a : limites "once per phase" remises à zéro sur `round_ended` (écart de timing marginal).


---

## Lot 13 : thor, qsv, bkw, drax, vnm, hlk, red_hulk_by_merlin

Références moteur (clone Warnel, `src/`) :
- `src/core/ScriptingEngine/ScriptProperties.gd` : `get_default` (needs_selection=false, subject_index=0 donc bas du paquet, src_container=null) et `check_validity` (clés de filtre inconnues ignorées).
- `src/core/ScriptingEngine/ScriptObject.gd` `_index_seek_subjects` : "top" doit être demandé explicitement ; container nul donne [].
- `src/wc/ScriptingEngine/ScriptingEngine.gd` `constraints()` et `_tags_to_tags` : le tag `"action"` n'est reconnu nulle part (grep `src/` vide).
- `src/wc/OVUtils.gd` : "host" vaut null pour un minion non attaché ; `matches_filters(_filters:Dictionary...)` rejette un Array.

## thor

### [thor] Loki (06028)
- Gravité : bloquante
- Certitude : prouvée par le code
- Texte imprimé : "Interrupt: When Loki would be defeated, discard the top card of the encounter deck. If that card is a treachery, heal all damage from Loki instead."
- Ce que fait le script Warnel : `{"name":"discard","subject":"index","src_countainer":"deck_villain"}` puis `{"name":"heal","subject":"host","amount":100}`.
- Pourquoi c'est faux : `src_countainer` est une faute de frappe, donc `src_container` reste null et `ScriptObject._index_seek_subjects` renvoie [] (aucune carte défaussée, la condition ne se déclenche jamais). Même corrigé, `subject_index` absent vaut 0 (bas du paquet) au lieu du dessus. De plus "host" = `owner.current_host_card` (OVUtils.get_subjects), null pour un minion : le soin ne cible personne ; il faut "self".
- Correctif proposé :
```json
{"interrupt": {"event_name": "card_dies", "trigger": "self", "board": [{"name": "discard", "subject": "index", "subject_index": "top", "subject_count": 1, "src_container": "deck_villain"}, {"name": "conditional_script", "options": [{"condition": {"func_name": "get_subject_int_property", "func_params": {"subject": "previous", "property": "type_code", "property_value": "treachery"}}, "nested_tasks": [{"name": "prevent", "subject": "interrupted_event"}, {"name": "heal", "subject": "self", "amount": 100}]}]}]}}
```
- Référence Narwhal : n/a (pas de module 06028.py)

### [thor] Odin's Anger (06026)
- Gravité : partielle
- Certitude : prouvée par le code
- Texte imprimé : "Discard Mjolnir from your hand or from play. You are stunned."
- Ce que fait le script Warnel : deux fois `{"name":"discard","subject":"tutor","src_container":"hand","filter_state_tutor":[{"filter_propoerties":{"Name":"Mjolnir"}}]}`.
- Pourquoi c'est faux : `filter_propoerties` n'est pas une clé connue ; `SP.check_validity` l'ignore, le filtre est vide et accepte toute carte. Le tutor défausse donc la première carte de la main (n'importe laquelle) au lieu de Mjolnir.
- Correctif proposé : remplacer les deux occurrences par `"filter_state_tutor":[{"filter_properties":{"Name":"Mjolnir"}}]` (reste du bloc inchangé).
- Référence Narwhal : n/a (pas de module 06026.py)

### [thor] Odinson (06001b)
- Gravité : mineure
- Certitude : prouvée par le texte seul
- Texte imprimé : "Worthy — Action: Search your deck and discard pile for the Mjolnir upgrade and add it to your hand. Shuffle your deck."
- Ce que fait le script Warnel : `move_card_to_container` (tutor, src ["deck","discard"]) sans mélange ensuite.
- Pourquoi c'est faux : `move_card_to_container` ne mélange pas (src/core/ScriptingEngine.gd et src/wc/ScriptingEngine.gd) ; il faut un `shuffle_container` explicite comme dans les autres cartes de recherche (ex. Agent Coulson dans bkw).
- Correctif proposé : ajouter à la fin du tableau "Worthy" `{"name":"shuffle_container","dest_container":"deck"}`.
- Référence Narwhal : n/a (06001b.py existe mais non pertinent au script)

### [thor] Hall of Heroes (06017)
- Gravité : partielle
- Certitude : prouvée par le texte seul
- Texte imprimé : "Alter-Ego Action: Exhaust Hall of Heroes and remove 3 glory counters from it → draw 3 cards."
- Ce que fait le script Warnel : la tâche "manual" ne contient pas d'`exhaust_card`.
- Pourquoi c'est faux : l'épuisement est un coût imprimé ; sans lui la capacité est réutilisable à l'infini tant qu'il y a 3 glory. Le module Narwhal 06017.py a bien `CostFunc.Exhaust("This")`.
- Correctif proposé :
```json
"manual": {"board": [{"name": "constraints", "is_cost": true, "tags": ["alter_ego_action"]}, {"name": "exhaust_card", "subject": "self", "is_cost": true}, {"name": "mod_tokens", "subject": "self", "modification": -3, "token_name": "glory", "is_cost": true}, {"name": "draw_cards", "amount": 3}]}
```
- Référence Narwhal : thor/06017.py

### [thor] Teamwork (06032)
- Gravité : bloquante
- Certitude : prouvée par le code
- Texte imprimé : "Hero Interrupt When you use your basic thwart power (THW) or basic attack power (ATK), exhaust an ally you control → add that ally's matching power..."
- Ce que fait le script Warnel : `interrupt_attack` et `interrupt_thwart` avec `"event_filters": ["basic_power"]`.
- Pourquoi c'est faux : `matches_filters` attend un Dictionary (OVUtils.gd), un Array est invalide ; et le tag moteur est "basic power" (avec espace), pas "basic_power". Le filtre ne fonctionne pas. Version correcte : `SetScripts_cyclops.json` clé "Teamwork".
- Correctif proposé : dans les deux blocs, `"event_filters": {"tags": ["basic power"]}`.
- Référence Narwhal : thor/06032.py

## qsv

### [qsv] Speed Cyclone (14006)
- Gravité : bloquante
- Certitude : prouvée par le code
- Texte imprimé : "Hero Action: Stun X Enemies."
- Ce que fait le script Warnel : `mod_tokens` stunned sur `boardseek` `subject_count:"all"` avec `"need_selection": true`.
- Pourquoi c'est faux : `need_selection` n'existe pas (la clé est `needs_selection`, ScriptProperties.gd) ; elle est ignorée, la valeur par défaut est false, donc TOUS les ennemis sont étourdis sans choix ni limite X.
- Correctif proposé :
```json
{"manual": {"hand": [{"name": "constraints", "is_cost": true, "tags": ["hero_action"]}, {"name": "mod_tokens", "token_name": "stunned", "modification": 1, "subject": "boardseek", "subject_count": "all", "needs_selection": true, "selection_count": {"func_name": "count_paid_resources"}, "filter_state_seek": [{"filter_group": "group_enemies"}]}]}}
```
- Référence Narwhal : n/a (pas de module 14006.py)

### [qsv] Maximum Velocity (14005)
- Gravité : partielle
- Certitude : prouvée par le code
- Texte imprimé : "Max 1 per phase."
- Ce que fait le script Warnel : clé racine `"TODO": "max 1 per phase"` sans effet.
- Pourquoi c'est faux : la limite n'est jamais vérifiée ; `constraints()` (wc/ScriptingEngine.gd) gère `max_per_phase` dans la tâche de contraintes.
- Correctif proposé : `{"name":"constraints","is_cost":true,"tags":["hero_action"],"max_per_phase":1}` (supprimer la clé "TODO").
- Référence Narwhal : n/a (pas de module 14005.py)

### [qsv] United We Stand (14031)
- Gravité : partielle
- Certitude : prouvée par le texte seul
- Texte imprimé : "Play only if your identity has the [[Avenger]] trait."
- Ce que fait le script Warnel : la contrainte ne teste que le tag hero_action.
- Pourquoi c'est faux : restriction absente (Narwhal : `SetPlay(only_if_your_identity_has_trait="AVENGER")`).
- Correctif proposé : `{"name":"constraints","is_cost":true,"tags":["hero_action"],"constraints":[{"func_name":"identity_has_trait","func_params":{"trait":"avenger"}}]}` (format de SetScripts_core.json l.3123).
- Référence Narwhal : qsv/14031.py

### [qsv] Multiple Man - Jamie Madrox (14012)
- Gravité : mineure
- Certitude : prouvée par le texte seul
- Texte imprimé : "Shuffle your deck if it was searched this way."
- Ce que fait le script Warnel : `move_card_to_board` tutor depuis ["hand","deck"] sans mélange.
- Pourquoi c'est faux : aucun mélange implicite dans le moteur ; le deck est cherché mais pas mélangé.
- Correctif proposé : ajouter après le move `{"name":"shuffle_container","dest_container":"deck"}`.
- Référence Narwhal : qsv/14012.py

### [qsv] Pietro Maximoff (14001b)
- Gravité : partielle
- Certitude : prouvée par le code
- Texte imprimé : "Superpowered Siblings — Action: Discard 2 cards from your hand → draw 2 cards..."
- Ce que fait le script Warnel : `"tags":["action"]`.
- Pourquoi c'est faux : "action" n'est reconnu nulle part dans `_tags_to_tags`/`constraints()` : aucun contrôle de timing d'action (utilisable hors de l'étape d'action).
- Correctif proposé : `"tags":["action_ability"]`.
- Référence Narwhal : n/a

### [qsv] Warlock (14013)
- Gravité : partielle
- Certitude : prouvée par le code
- Texte imprimé : "Action: Spend a [mental] resource → heal up to 2 damage from Warlock."
- Ce que fait le script Warnel : `"tags":["action"]` (même cause).
- Correctif proposé : `"tags":["action_ability"]`.
- Référence Narwhal : qsv/14013.py (AbilityType.Action)

## bkw

### [bkw] Covert Ops (08003)
- Gravité : partielle
- Certitude : prouvée par le code
- Texte imprimé : "Action (thwart): Remove 4 threat from a scheme. Confuse the villain."
- Ce que fait le script Warnel : `"tags":["action"]` (tag inopérant).
- Correctif proposé : `"tags":["action_ability"]`.
- Référence Narwhal : n/a

### [bkw] Quincarrier (08023)
- Gravité : partielle
- Certitude : prouvée par le texte seul
- Texte imprimé : "Play only if your identity has the [[Avenger]] trait."
- Ce que fait le script Warnel : seulement `resource` ; aucun bloc "manual"/"hand" de restriction.
- Pourquoi c'est faux : restriction absente, la carte se joue avec n'importe quelle identité (Narwhal : `SetPlay(only_if_your_identity_has_trait="AVENGER")`).
- Correctif proposé : ajouter `"manual": {"hand": [{"name":"constraints","is_cost":true,"constraints":[{"func_name":"identity_has_trait","func_params":{"trait":"avenger"}}]}]}`.
- Référence Narwhal : bkw/08023.py

### [bkw] Defensive Stance (08032)
- Gravité : partielle
- Certitude : prouvée par le texte seul
- Texte imprimé : "Hero Interrupt: When you would take any amount of damage, discard Defensive Stance → prevent 3 of that damage."
- Ce que fait le script Warnel : `"event_filters":{"target":"my_hero","tags":["attack"]}`.
- Pourquoi c'est faux : le texte vise tout dommage (traîtrises, conséquences), le script ne réagit qu'aux dommages d'attaque. Narwhal : `WhenUnitWouldTakeDamage` sans restriction.
- Correctif proposé : `"event_filters":{"target":"my_hero","amount":">0"}`.
- Référence Narwhal : bkw/08032.py

## drax

### [drax] "Think Fast!" (19031)
- Gravité : partielle
- Certitude : prouvée par le texte seul
- Texte imprimé : "Play only if your identity has the [[guardian]] trait."
- Ce que fait le script Warnel : contrainte hero_action seule.
- Correctif proposé : `{"name":"constraints","is_cost":true,"tags":["hero_action"],"constraints":[{"func_name":"identity_has_trait","func_params":{"trait":"guardian"}}]}`.
- Référence Narwhal : drax/19031.py (`only_if_your_identity_has_trait="GUARDIAN"`)

### [drax] Gamora (19020)
- Gravité : partielle
- Certitude : prouvée par le texte seul
- Texte imprimé : "Play only if your identity has the [[guardian]] trait."
- Ce que fait le script Warnel : pas de bloc "manual"/"hand" de restriction.
- Correctif proposé : ajouter `"manual":{"hand":[{"name":"constraints","is_cost":true,"constraints":[{"func_name":"identity_has_trait","func_params":{"trait":"guardian"}}]}]}`.
- Référence Narwhal : drax/19020.py

### [drax] Mantis (19002)
- Gravité : bloquante
- Certitude : prouvée par le code
- Texte imprimé : "Action: Exhaust Mantis and deal 1 damage to her → heal 3 damage from an identity."
- Ce que fait le script Warnel : `heal` avec `"need_selection": true`.
- Pourquoi c'est faux : `need_selection` inexistant (ScriptProperties.gd), ignoré, donc le soin de 3 s'applique à toutes les identités (`subject_count:"all"`) au lieu d'une seule.
- Correctif proposé : `"needs_selection": true` à la place.
- Référence Narwhal : n/a

### [drax] Deflection (19015)
- Gravité : mineure
- Certitude : prouvée par le texte seul
- Texte imprimé : "prevent up to 5 of that damage. Discard cards from the top of your deck equal to the amount prevented this way."
- Ce que fait le script Warnel : `event_prevented` avec `"amount_prevented": ">1"`.
- Pourquoi c'est faux : `amount_prevented` existe (ScriptingEngine.gd l.1997) ; avec ">1" aucune carte n'est défaussée quand 1 dommage est empêché. Narwhal : `DiscardDeckTopCards(value)` sans seuil.
- Correctif proposé : `"event_filters":{"amount_prevented":">0"}`.
- Référence Narwhal : drax/19015.py

### [drax] Leading Blow (19017)
- Gravité : bloquante
- Certitude : prouvée par le code
- Texte imprimé : "discard the top card of the encounter deck → reduce your hero's ATK ... by the number of printed boost icons on that card."
- Ce que fait le script Warnel : `{"name":"discard","subject":"index","subject_count":1,"is_cost":1,"src_container":"deck_villain"}`.
- Pourquoi c'est faux : `subject_index` absent vaut 0 (bas du paquet, `get_default`) ; "top" doit être explicite (cf. SetScripts_core.json l.3920 et 3941). La carte défaussée est celle du dessous, les icônes de renfort sont donc fausses. Narwhal : `Discard("EncounterDeckTop")`.
- Correctif proposé : ajouter `"subject_index":"top"` à cette tâche.
- Référence Narwhal : drax/19017.py

## vnm

### [vnm] "Welcome Aboard" (20027)
- Gravité : bloquante
- Certitude : prouvée par le texte seul
- Texte imprimé : "Play only if your identity has the [[guardian]] trait. Max 1 per round. Hero Action: Reduce the resource cost of the next ally played this phase by 2."
- Ce que fait le script Warnel : `"alteration": -1` ; aucune restriction guardian ; aucune limite par round.
- Pourquoi c'est faux : réduction de 1 au lieu de 2 ; deux restrictions imprimées absentes (Narwhal : -2, `only_if_your_identity_has_trait="GUARDIAN"`, `MaxOnePerRound()`).
- Correctif proposé : `"alteration": -2` et `{"name":"constraints","is_cost":true,"tags":["hero_action"],"max_per_round":1,"constraints":[{"func_name":"identity_has_trait","func_params":{"trait":"guardian"}}]}`.
- Référence Narwhal : vnm/20027.py

### [vnm] Shake it Off (20028)
- Gravité : partielle
- Certitude : prouvée par le texte seul
- Texte imprimé : "After a [[guardian]] character takes any amount of damage from an attack, give that character a tough status card."
- Ce que fait le script Warnel : `card_damaged` sans filtre d'attaque.
- Pourquoi c'est faux : se déclenche pour tout dommage (traîtrise, conséquence...). Narwhal : `is_from_attack=True`. Précédent Warnel : Counterattack (bkw) filtre `"tags":["attack"]`.
- Correctif proposé : ajouter `"event_filters":{"tags":["attack"]}` au bloc `card_damaged`.
- Référence Narwhal : vnm/20028.py

## hlk

### [hlk] Inspiring Presence (10030)
- Gravité : partielle
- Certitude : prouvée par le texte seul
- Texte imprimé : "Play only if your identity has the [[Avenger]] trait."
- Correctif proposé : `{"name":"constraints","is_cost":true,"tags":["hero_action"],"constraints":[{"func_name":"identity_has_trait","func_params":{"trait":"avenger"}}]}`.
- Référence Narwhal : hlk/10030.py

### [hlk] Beat Cop (10029)
- Gravité : partielle
- Certitude : prouvée par le code
- Texte imprimé : "Action: Exhaust Beat Cop → move 1 threat from a scheme to here. // Action: Exhaust and discard Beat Cop → deal 1 damage to a minion for each threat here."
- Ce que fait le script Warnel : `"tags":["action"]` dans les deux capacités (tag inopérant).
- Correctif proposé : `"tags":["action_ability"]` dans les deux.
- Référence Narwhal : hlk/10029.py

### [hlk] Bruce Banner (10001b)
- Gravité : partielle
- Certitude : prouvée par le code
- Texte imprimé : "Experimental Research — Action: Draw 1 card. Choose and discard 1 card from your hand. (Limit once per round.)"
- Ce que fait le script Warnel : `"tags":["action"]` (tag inopérant).
- Correctif proposé : `"tags":["action_ability"]`.
- Référence Narwhal : n/a

---
Cartes auditées : 198
Cartes OK : 162
Effets de campagne non gérés (non listés) : 0

Cartes incertaines (non prouvées, non comptées comme erreurs) :
- [qsv] Side Step (14015) : "deal 1 damage to that enemy" ; le script cible un ennemi au choix (`subject:"target"`) et non l'attaquant. Probable, correctif non vérifié.
- [drax] Challenge Accepted (19028) : `filter_state_attacker` et `damage:">=4"` à la racine non confirmés dans le moteur.
- [vnm] Plasma Pistol (20022) : retrait du jeton charge sans `is_cost`.
- [vnm] Venom's Pistol (20010) : event_name `remove_threat` pour le thwart de base non confirmé.
- [red] Overheating (70802) : `up_to:true` au lieu d'un nombre exact de cartes défaussées.
- [red] Battle of the Hulks (70820) : mot-clé [amplify] non géré.
- [bkw] Espionage (08033) : signal `interrupt_surge` non retrouvé littéralement dans `src/`.
- [qsv] Under Surveillance : "Max 1 per scheme" absent.
- [qsv/thor] Get Over Here! (dégâts d'attaque), Hercules (groupe + is_inverted), Lightning Strike (coût X via pay_cost).
- [bkw] Target Acquired (08024) : `interrupt_boost` pour une réponse.


---

## Annexe : clés mal orthographiées (détection automatique)

Méthode : toutes les clés en snake_case des 37 fichiers `SetScripts_*.json` ont été comparées à l'ensemble des chaînes entre guillemets présentes dans `src/` et `scripts/`. Les clés rares (1 à 4 occurrences) absentes du moteur ont été relues une à une. Les clés ci-dessous ne sont lues nulle part : le moteur les ignore en silence et l'effet correspondant n'a pas lieu.

| Carte | Fichier | Clé fautive | Clé correcte |
|---|---|---|---|
| Ionic Boots, Kinetic Armor, Neocarbon Scales, Spiked Gauntlet, Tracking Display, Upgrading Adaptoids - 1A | `SetScripts_sm.json` | `des_container` | `dest_container` |
| Holding Cell (3 occurrences) | `SetScripts_aos.json` | `des_container` | `dest_container` |
| War Room | `SetScripts_gambit.json` | `ais_cost` | `is_cost` |
| Field Commander | `SetScripts_cyclops.json` | `filter_same_controler` | `filter_same_controller` |
| Zemo's Manipulations - 1B | `SetScripts_aos.json` | `filtr_state_seek` | `filter_state_seek` |
| C.I.T.T. | `SetScripts_stld.json` | `ineeds_subject` | `needs_subject` |
| Locked and Loaded | `SetScripts_vnm.json` | `selectiontyp` | `selection_type` |
| Mental Paralysis | `SetScripts_phoenix.json` | `subjec` | `subject` |
| Mutant Peacekeepers | `SetScripts_phoenix.json` | `selection_needed` | `needs_selection` |
| Release the Hounds, Mantis, Speed Cyclone | `SetScripts_aoa.json`, `SetScripts_drax.json` | `need_selection` | `needs_selection` |
| Superpower Feedback | `SetScripts_next_evol.json` | `filter_events` | `event_filters` |
| Ruckus | `SetScripts_next_evol.json` | `gilter_group` | `filter_group` |
| Zzzax, Psychic Misdirection, Iron Heart (x2) | `SetScripts_ironheart.json`, `SetScripts_phoenix.json` | `filer_group` | `filter_group` |
| Flurry of Blades, Mental Detection, Psionic Redirect, Telepathic Suggestion | `SetScripts_psylocke.json` | `filer_same_controller` | `filter_same_controller` |
| Loki | `SetScripts_thor.json` | `src_countainer` | `src_container` |
| Odin's Anger | `SetScripts_thor.json` | `filter_propoerties` | `filter_properties` |
| Astral Projection | `SetScripts_drs.json` | `filter_groups` | `filter_group` |
| Permanently Phased | `SetScripts_mut_gen.json` | valeur `"Kitty Pride"` | `"Kitty Pryde"` |
| Crisis on Halfworld | `SetScripts_gmw.json` | valeur `"Rocket Rackoon"` | `"Rocket Raccoon"` |
| Banishment | `SetScripts_stld.json` | `nested_scripts` | `nested_tasks` |
| Thunderbolt Backup | `SetScripts_aos.json` | valeur `"do_heal,"` | `"do_heal"` |

Remarque : `SetScripts_aos.json` (ligne 7644) et `SetScripts_core.json` (ligne 824) contiennent des virgules finales dans le JSON. Elles sont refusées par un parseur strict ; le moteur Godot les tolère visiblement, mais elles sont à nettoyer.

Les clés restantes absentes du moteur sont des noms de macros, de fonctions ou de variables définis par les auteurs (par exemple `ultron_drone`, `do_advance`, `trait_*`) et ne sont pas des fautes.

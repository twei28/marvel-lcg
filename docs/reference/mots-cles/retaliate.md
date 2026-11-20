# Retaliate

**Texte imprimé / définition** : « Retaliate 1. *(After this character is
attacked, deal 1 damage to the attacking character.)* » Après qu'un personnage
Retaliate a été attaqué, l'attaquant subit un nombre de dégâts égal à la valeur
de Retaliate. C'est un compteur (`Retaliate 1`, `Retaliate 2`, ...),
réinitialisé à sa valeur imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Retaliate` sur la carte, lue nativement
par le moteur. `HasRetaliate`
(`src/game/card/face/attribute/can_retaliate.py`) enregistre l'attribut
`Retaliate` -> `printed_retaliate`, restaure la valeur à chaque
`OnResetKeywords` via `GainRetaliate`, et fournit
`ResolveRetaliate(atk_message)` qui applique les dégâts en retour en
s'appuyant sur la classe `Retaliate(GameRule)` de
`src/game/effect/rule.py` comme justification de l'effet. Trois conditions y
sont vérifiées avant le `attacker.TakeDamage(...)` : l'attaquant existe et
n'est pas vaincu, l'attaque n'est pas à distance (`atk_message.IsRanged()`) et
le défenseur n'est pas vaincu, et l'attaque n'ignore pas le mot-clé
(`atk_message.IsIgnoreRetaliate()`). Sinon un `Message.AfterIgnoreKeywordOnCard`
est émis à la place. L'appel vient de `can_attack.py` et de
`src/game/effect/effect_invoke.py`. **Aucun script requis** pour ce mot-clé.

**Carte exemple** : `01040a` : * Black Panther (`desc` contient
`"Retaliate": "1"`), lu directement depuis `desc`, aucun script requis.
Aucun fichier `01040a.py` trouvé dans `src/cards/pack` : cette face de
carte n'a pas de capacité imprimée distincte nécessitant un script.

**Pièges connus** : trois cas où Retaliate ne se déclenche pas, tous lisibles
dans `ResolveRetaliate` : attaque **à distance** (`IsRanged()`), défenseur ou
attaquant **déjà vaincu** au moment de la résolution, et attaque qui **ignore
Retaliate** (`IsIgnoreRetaliate()`). Aucun rapport en revanche avec Quickstrike :
ce mot-clé n'est pas une règle d'ordre de résolution des dégâts, c'est une
attaque déclenchée quand un sbire s'engage avec un héros (voir sa fiche), et il
n'a aucune interaction particulière avec Retaliate. Si une future carte
cumule Retaliate avec une capacité imprimée annexe (déclencheur sur les
dégâts infligés, par exemple), vérifier via `find` si un script existe
pour cette carte : le script devra porter uniquement cette capacité
annexe, jamais le mot-clé Retaliate lui-même. La carte `03009` (Captain
America's Shield) illustre ce piège concret ailleurs dans le catalogue :
elle a un script (`AbilityFactory.GiveKeywordToAttached`), mais ce script
code sa capacité d'ATTACHEMENT (donner Defense 1 et Retaliate 1 à
Captain America), pas le mot-clé Retaliate en tant que tel.

**Retaliate X à valeur dynamique** (officiel, `64009` Embody the Dragon, Iron
Fist MC64EN : « Iron Fist gains retaliate X, where X is equal to the number of chi
counters on this card ») : `GiveKeywordToInPlayWhenApplyThis(Hero,
control_by="You", retaliate=1, get_new_value=<compteurs de la carte>,
change_on_event=OnEvent.Counter("This", 'chi'))`. La valeur est relue à chaque
pose/retrait de compteur ; « Iron Fist » est le NOM de la face héros, donc pas de
riposte pour l'alter ego (contre-cas `[iron_fist] 64009`).

**Variantes maison** : aucune recensée pour l'instant.


**Rules Reference 1.8 (22/07/2026)** : Retaliate devient « Forced Response : After this character is attacked, deal X damage to the attacker », résolu avec les autres réponses forcées « after attacks / after is attacked », dans l'ordre choisi (le bullet 1.7 « 1. after takes damage 2. Retaliate X 3. after attacked » est supprimé). Moteur : règle `v18_retaliate` (posée par `v18_all`). Sous cette règle, `EventManager.RegisterPlayRule` pose UNE réponse forcée de règle pour toute la partie (`CanRetaliate.AbiliteRiposte()`, sur `AfterUnitAttackUnit`, pour toute cible attaquée qui a Retaliate), et les deux appels directs (`can_attack.py`, `effect_invoke.py`) sont sautés ; « attaquant vaincu » se relit sur l'état du monde après la fenêtre. Pas une capacité par carte : un premier essai l'ajoutait dans `CardFactory.CreateFace` et cassait les faces créées sans carte (`TreatAsMinion` : mw026 Veranke, av014, av015, sw023). Sans la règle (sauvegardes d'avant), rien n'est ajouté : les identifiants d'effets, donc le rejeu, restent identiques. Cas : `[RR1.8] wx009 riposte` (Radioactive Man à 1 PV : sa réponse forcée fait défausser avant la riposte, et le témoin 1.7).

## Pièges vus au portage de Raza Longknife (26/10/2026)

- **Retaliate CONDITIONNELLE donnée par une amélioration** (« while your identity has sustained 5 or more damage, you gain Retaliate 1 », `rl008`) : `*GiveKeywordToAttached("You", get_new_value=fn, retaliate=1, ex_change_on_event=OnEvent.Health("YourIdentity"))`, `fn` rend 0 ou 1 selon `attach.sustained`. Modèle `brawn/bw016`. Sans `ex_change_on_event` la valeur ne suit pas les dégâts.
- Cas : `[rl] rl008` (5 dégâts : Rhino qui attaque subit 1 ; 4 dégâts : 0). Le héros défend de lui-même sous le harnais (ATQ 2 - DEF 2 = 0 dégât) mais la riposte part quand même.

- **Retaliate donnée PAR une attaque (`rl008`, vérifié le 26/10/2026)** : la parenthèse imprimée « (Retaliate will trigger for attacks that cause Raza to gain Retaliate) » est exacte avec le moteur (RR 1.8 : Réponse forcée APRÈS l'attaque). Cas : Raza à 4 dégâts ET ÉPUISÉ (`Puzzle.Exhaust('rl001a')`) : l'attaque non défendue de Rhino le porte à 6, Rhino subit 1 ; témoin 2 + 2 = 4 : rien. ⚠ Un héros en forme héros DÉFEND tout seul (le pilote) : l'attaque est réduite à 0 et ne teste pas la parenthèse (l'ancien contre-cas « à 4 dégâts » ne la testait donc pas).

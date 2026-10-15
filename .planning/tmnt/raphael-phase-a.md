# Raphael (TMNT Heroes v3, Inkwire) : PHASE A (construction), rien n'est validé

Worktree : `.claude/worktrees/agent-a1ef6da137c87ed6b`, branche `worktree-agent-a1ef6da137c87ed6b`.
Source : zip « TMNT Heroes-20261014T200300Z-1-001.zip », dossier `TMNT Heroes/Raphael v3/` (24 PNG).
Préfixe `tr` (libre dans `cards.json`, vérifié ; `verifier_prefixes.py` vert après ajout). Pack `raphael`, set 164.

**Aucun harnais lancé** (ni `test_capacites`, ni `autoplay`, ni `verifier_tous_les_decks`, ni `test_cards`,
ni `verifier_appels_modules` : ce dernier écrit `launch.json` et charge le moteur, et la machine n'a pas
python3.10). Seules vérifications faites : JSON valide + checksum recalculé et calibré sur HEAD, `py_compile` des
18 modules, `verifier_prefixes.py` (statique), et une vérification maison des noms de méthodes appelées (voir
« Limites »). **Rien n'a été exécuté en jeu.**

## 1. card_id créés (18)

| card_id | Nom | Type | Set |
|---|---|---|---|
| tr001a | * Raphael | Hero | Raphael |
| tr001b | * Raph | AlterEgo | Raphael |
| tr002 | * Casey Jones | Ally | Raphael |
| tr003 | Disarm (x2 dans le deck) | Event | Raphael |
| tr004 | Headbutt (x2) | Event | Raphael |
| tr005 | Savage Assault | Event | Raphael |
| tr006 | Unbridled Fury (x2) | Event | Raphael |
| tr007 | Seething Rage (x2) | Resource | Raphael |
| tr008 | * Shell Cycle | Support | Raphael |
| tr009 | * Raph's Punching Bag | Support | Raphael |
| tr010 | Gekido | Upgrade | Raphael |
| tr011 | * Raphael's Sai | Upgrade (Restricted) | Raphael |
| tr012 | * Raphael's Other Sai | Upgrade (Restricted) | Raphael |
| tr013 | Out of Control (obligation, GiveTo « Raph ») | Obligation | Raphael |
| tr014 | Mutagen Bomb | SideScheme | Raphael Nemesis |
| tr015 | * Old Hob | Minion | Raphael Nemesis |
| tr016 | Insurrection (x2 dans le set) | Treachery | Raphael Nemesis |
| tr017 | Prepare to Rally | Treachery | Raphael Nemesis |

Deck : 15 cartes = tr002, tr003 x2, tr004 x2, tr005, tr006 x2, tr007 x2, tr008, tr009, tr010, tr011, tr012.
`nemesis_set` = tr014, tr015, tr016, tr016, tr017. `player_deck` VIDE (règle PROCESSUS-HEROS étape 3).
Les 5 doublons du zip (Disarm n°3, Headbutt n°5, Unbridled Fury n°8, Seething Rage n°10, Insurrection n°4) sont des
copies (comparaison d'image) : un seul card_id chacune. L'encart « Raphael Insert.png » n'est pas une carte.
`custom` = « Inkwire » (nom lu au pied de chaque scan : « TMNT Heroes By: Inkwire »).

Icônes de ressource : **comparées par découpe** du coin bas-gauche : poing de `tr003` = poing de `01003` (RES R),
étoile de `tr002` = étoile de `01043d` (RES G). Toutes les cartes de deck sauf Casey Jones sont `RES R`.

## 2. Fichiers modifiés / créés (dans `Fusion/marvel-lcg-src/` sauf mention)

- `data/cards.json` (pack `raphael` en queue, checksum recalculé), `data/sets_info.json` (« 164. Custom (Raphael) »).
- `data/nemesis/raphael_nemesis.json`, `deck/starter/raphael.json` (nouveaux).
- `src/cards/pack/raphael/__init__.py`, `raphael/__init__.py` (helpers + capacités des Sai), `raphael/tr001a.py` à
  `tr013.py` (14 modules), `raphael_nemesis/__init__.py`, `raphael_nemesis/tr014.py`, `tr016.py`, `tr017.py`.
  `tr015` Old Hob n'a pas de script (Toughness, Quickstrike, Nemesis : bases automatiques de `desc`).
- `tools/prefixes_fanmade.json` (préfixe `tr`), `tools/importer_images_raphael.py` (recette des images, nouveau).
- `public/js/prepare/heros-info.js` (entrée `tr001a`), `../../ui-app/src/board/textes-fr-fanmade.ts` (18 entrées,
  rien n'apparaît tant que `ui-app/deployer.sh` n'a pas tourné).
- Images : 18 JPG 615x882 / 882x615 dans `Fusion/marvel-lcg-src/assets/pics/` (**gitignoré**), et la **même série
  commitée** dans `.planning/tmnt/raphael-pics/` pour que l'intégrateur la recopie dans le vrai `assets/pics/`.
- **Aucun fichier moteur partagé touché** (`card_face.py` : les compteurs `rage` et `timer` y existaient déjà).

À l'intégration avec Leonardo / Donatello / Michelangelo : conflits attendus et triviaux sur `cards.json` (fin de
fichier + `checksum`), `sets_info.json` (le numéro « 164 » sera pris par chacun : renuméroter ; relancer
`verifier_prefixes.py`), `prefixes_fanmade.json`, `heros-info.js`, `textes-fr-fanmade.ts`. **Recalculer les deux
checksums après fusion** (formule : sha256 de `json.dumps(obj sans "checksum", sort_keys=True)`).

## 3. Décisions de modélisation (pas des questions, mais à connaître)

- **Compteur de rage = ressource [physical]** : montage de `30001a` Spider-Ham (`CanGenerateResources(HeroResource,
  Resources("R"))` + `CostFunc.Counter`). Les compteurs vivent sur la CARTE d'identité (partagés par les deux faces).
- **Les deux Sai « font gagner » une capacité à chaque Sai que vous contrôlez** : le moteur n'a aucun « gains » pour des
  cartes joueur. Chaque Sai (`tr011`, `tr012`) porte donc LES DEUX capacités (attaque, pioche), chacune conditionnée à
  la présence de la carte qui la donne (`SaiEnJeu`). Effet observable : deux Sai en jeu = deux Actions d'attaque et deux
  Réponses de pioche, une par carte (comme l'encart le dit). Les dégâts d'attaque sont infligés par `hero.DealDamage`
  pour que Raphael soit l'auteur de la mise K.O. (Réponse de `tr012`).
- Tous les « choisir » se résolvent par `ChooseAbilities` : le pilote du harnais prend la 1re branche (phase C : clés
  `preferer_option` / `cibles`).

## 4. Questions en attente (6)

### Q1. `tr002` Casey Jones, `tr010` Gekido, `tr011`/`tr012` : le plafond de 3 rage vaut-il partout ?
Texte imprimé : « place 1 rage counter on him **(to a maximum of 3)** » sur `tr001a` et `tr007` ; **rien** sur `tr002`
(« Place 1 rage counter on Raphael ») ni `tr010` (« Place 1 rage counter on Raphael »). L'encart des Sai dit « (to a
maximum of 3) ».
- A (recommandée) : plafond de 3 partout, c'est une propriété de la rage sur Raphael ; les trois mentions imprimées
  sont un rappel. Garde « retirez 2 rage » (`tr013`) et la dépense comme ressource dans une échelle prévisible.
- B (code actuel, lecture littérale) : plafond seulement où il est imprimé. Casey et Gekido peuvent dépasser 3 : plus de
  ressources [physical] à dépenser, plus de cartes avec le Sac de frappe (`tr009`).
- C : autre.
Bascule : `PLAFOND_PARTOUT = True` dans `raphael/raphael/__init__.py`.

### Q2. « Raphael » en forme civile (`tr002`, `tr007`, aussi soin de `tr010`)
Casey Jones et Seething Rage peuvent se jouer/dépenser en forme alter-ego (« Response », pas « Hero Response »), mais
« Raphael » est le nom de la face héros (l'alter-ego s'appelle « Raph »).
- A (recommandée) : « Raphael » = face héros seulement ; en civil, ni dégâts à Raphael, ni soin, ni rage (les sbires
  engagés prennent quand même 1 dégât avec Casey). Code actuel.
- B : en civil, la rage se pose quand même sur l'identité (le compteur est sur la carte) et le soin/dégât visent l'identité.
  Change : Casey/Seething Rage alimentent le Sac de frappe (`tr009`, Action d'alter-ego) sans passer par la forme héros.
- C : autre.

### Q3. Encart « Sai Weapon Rules » : fait-il loi ? (`tr011`, aussi `tr012`)
L'encart dit : « Each time you use the Sai to deal 1 damage to yourself and 1 damage to an enemy, it is an **attack**
action. Make sure to place **1 rage counter** on Raphael when you use this ability (to a maximum of 3). » La carte
`tr011` imprime seulement « Hero Action (attack): Exhaust this card and take 1 damage → deal 1 damage to an enemy ».
Les 1 dégât pris en coût ne sont pas « from an attack » : Yaban Hito ne part pas, d'où la rage posée à la main.
- A (recommandée, code actuel) : l'encart fait loi : attaque + 1 rage (max 3) à chaque usage d'une Sai.
- B : seulement le texte de la carte : pas de rage posée par la Sai (Raphael ne gagne de la rage qu'en subissant des
  attaques, par Casey, Gekido, Seething Rage).
- C : autre.

### Q4. `tr013` Out of Control : portée de « You cannot change forms, thwart, or defend »
Texte : « You cannot change forms, thwart, or defend. » Et la Hero Action de sortie dit « flip to alter-ego form ».
- A (recommandée, code actuel) : « You » = l'identité seulement (les alliés peuvent contrer et défendre) ; l'Action de
  sortie de la carte elle-même peut retourner en civil (exception déjà prévue par le moteur). Interdiction continue
  tant que la carte est en jeu.
- B : « You » vise aussi les alliés du joueur (plus dur : plus aucun contre ni défense ; mais l'encart ne le dit pas).
- C : autre.
Note de jeu : la sortie coûte 2 rage ; sans 2 compteurs l'Action n'est pas offerte, et Raphael ne peut plus défendre.
Le texte n'a aucune autre sortie (voulu ? sans doute).

### Q5. `tr014` Mutagen Bomb : icône imprimée sous le texte (croix + forme d'avion)
Icône découpée et comparée aux témoins : ce n'est ni le Hazard de `hd022` (carte penchée + croix, rien dessous) ni
l'Acceleration de `hd026` / `ag011` (croix + pointe + **barre épaisse** dessous). Aucune clé posée dans `desc` (rien
d'inventé). Menace de départ « 2 + silhouette » = `StartingThreat "2*"` (lu, pas ambigu).
- A (recommandée) : Hazard 1 : ressemble le plus au Hazard (croix, pas de barre), et le texte de la carte fait
  piocher des cartes rencontre. +1 carte rencontre en phase du vilain tant que la carte est en jeu.
- B : Acceleration 1 : +1 menace sur le complot principal par round tant que la carte est en jeu.
- C : aucune icône (simple décor du gabarit) : la carte ne fait que son Réponse forcée.
- D : autre (icône maison à définir).
Pour A ou B : ajouter `"Hazard": "1"` ou `"Acceleration": "1"` à `desc` de `tr014` dans `cards.json` (+ checksum).

### Q6. `tr003` Disarm : « an attachment with the text "Hero Action" or "Hero Response" from an enemy »
- A (recommandée, code actuel) : seuls les ATTACHEMENTS de rencontre (type Attachment) attachés à un ennemi, via
  `GetAttachedAttachments`. Lecture littérale du mot « attachment ».
- B : aussi les AMÉLIORATIONS joueur attachées à un ennemi (type Upgrade, ex. Burning de Sunfire), comme le fait
  `sf003`/`sf005` dans le pack Sunfire (qui emploie le même mot « attachment »).
- C : autre.

## 5. Capacités à tester en phase C (par card_id)

Rappels harnais (RECETTES §7) : le pilote prend le MINIMUM d'un « up to » et la 1re branche d'un choix ; Moxie
(`12016`) fausse les mesures d'attribut ; ne jamais retirer une assertion qui échoue ; chaque capacité = un cas sujet
(`tr0xx` dans le nom) + preuve par substitution ; **un contre-cas dans l'AUTRE forme** pour tout bonus d'identité.

- **tr001a** : (1) dépense d'un compteur de rage comme ressource [physical] pour payer une carte (le compteur baisse de
  1) ; (2) Yaban Hito : une attaque qui blesse pose 1 rage, plafond 3 (4e attaque : toujours 3) ; (3) contre-cas : des
  dégâts qui ne viennent PAS d'une attaque (Casey, Sai) ne posent rien ; (4) 0 dégât (Tough) : pas de rage.
- **tr001b** : Action : défausser 1 carte de la main (coût) puis chercher deck + défausse jusqu'à 2 Sai, mises en jeu
  inclinées (forcer `cibles` à 2) ; cas avec 1 seule Sai trouvable ; deck mélangé ; contre-cas en forme héros (Action absente).
- **tr002** : arrivée en jeu : 1 dégât à Raphael ET à chaque sbire engagé avec CE joueur (pas aux sbires engagés ailleurs,
  si 2 héros), +1 rage ; en civil (Q2) ; pas de Yaban Hito ; ATQ/CTR 2* = 1 dégât consécutif (mesurer).
- **tr003** : Requirement R ; retire 4 menaces ; option Sai : refuser (rien défaussé) / accepter (Sai + attachement
  défaussés) ; sans Sai ou sans attachement éligible : pas d'offre ; attachement SANS « Hero Action/Response » refusé (Q6).
- **tr004** : Requirement RR ; 4 dégâts + étourdir (1re branche) ET désorienter (clé `preferer_option`) ; ennemi vaincu
  par les 4 dégâts : pas de statut, pas de plantage.
- **tr005** : Requirement RRR ; 10 dégâts répartis (forcer `cibles` sur 10 sélections : 10 sur un seul ennemi, puis 5+5) ;
  total mesuré à 10 ; attention `repeat_rules="Health"` : au total de PV < 10, tout n'est pas distribuable.
- **tr006** : +2 ATQ jusqu'à la fin du round (mesurer l'ATQ du héros) ; pioche seulement si payé avec une ressource
  [physical] (cas payé en [mental] : pas de pioche ; cas payé avec un compteur de rage : à confirmer) ; limite
  « Max 1 per phase » : **témoin d'épuisement** (2e exemplaire dans la même phase refusé ; vérifier si la limite vaut
  par carte ou pour les deux exemplaires) et réarmement à la phase suivante.
- **tr007** : Réponse à la dépense : soigne 2 (mesurer les PV) + 1 rage plafonnée à 3 ; en civil (Q2).
- **tr008** : coût inclinaison + 2 ressources ; redresse le héros ; +1 CTR jusqu'à la fin du round **seulement si** payé
  avec 2 [physical] (contre-cas payé en [mental]/[energy]) ; A VERIFIER que `GetPaidResources` est renseigné pour un coût
  d'ABILITÉ ; dépense par compteurs de rage.
- **tr009** : +2 REC en forme alter-ego (contre-cas : en forme héros, REC du héros inchangé, pas de fuite) ; Action
  d'alter-ego : inclinaison + retrait de tous les compteurs de rage (les compteurs gagnés en forme héros PERSISTENT
  après le retournement ?) ; pioche = nombre RÉEL retiré (0, 1, 3 compteurs) ; Action non offerte à 0 compteur.
- **tr010** : inclinaison ; choix rage (1re branche) / soin (`preferer_option`) ; rage non plafonnée (Q1) ; soin à 0 dégât.
- **tr011** : Restricted (2 Restricted max : les deux Sai coexistent, un 3e objet Restricted est refusé) ; Action
  d'attaque : coût inclinaison + 1 dégât à l'identité, 1 dégât à un ennemi, 1 rage plafonnée à 3 (Q3) ; la Sai est
  « Hero Action » (absente en civil) ; la capacité « gagnée » n'existe sur `tr012` que si `tr011` est en jeu (contre-cas).
- **tr012** : Réponse « après que Raphael met K.O. un ennemi » : inclinaison + pioche ; vaut pour vilain ET sbire ;
  attaque de base ET d'événement ET dégât de Sai ; une Sai OU les deux pour un même ennemi (2 pioches) ; ne répond pas
  si inclinée (entrée épuisée via `tr001b`) ; ne répond pas si c'est un allié qui vainc (contre-cas) ; la capacité
  n'existe sur `tr011` que si `tr012` est en jeu.
- **tr013** : à la réception : forme héros + identité inclinée (partir d'abord en civil ET en héros) ; ne peut ni changer de
  forme (le changement volontaire est bloqué), ni contrer, ni défendre (les alliés oui, Q4) ; Hero Action : coût 2 rage
  (non offerte à 0 ou 1) puis alter-ego ET obligation défaussée (le retournement par la carte elle-même n'est PAS bloqué) ;
  `GiveTo "Raph"` résolu sur le bon joueur ; **partie d'obligation complète** (qui l'a donnée, réveil du pilote).
- **tr014** : après l'étape 1 de la phase du vilain : 1er passage = 1 compteur `timer` seulement ; 2e passage = défausse
  de la carte + 1 carte rencontre face cachée à CHAQUE joueur (cas 2 joueurs) ; menace de départ 2 par joueur ; icône (Q5).
- **tr015** : Toughness (carte Robuste à l'entrée), Quickstrike (attaque à l'engagement, pas en civil), Nemesis
  « Raphael » (entre avec le set), 4 PV, ATQ 2, SCH 2, 2 icônes de boost. Aucun script : seulement des mesures.
- **tr016** : Une fois révélée : défausse d'un allié (le joueur choisit) ; sans allié : défausse d'1 carte de la main (choisie)
  ET jamais les deux ; sans allié ni main : rien ; Boost étoile : défausse d'un allié REDRESSÉ seulement (un allié incliné
  ne compte pas) ; sans allié redressé : rien. `Boost 0` + capacité étoile (sans l'Ability, aucune étoile).
- **tr017** : Une fois révélée et Boost : le joueur choisit 1 carte à défausser ; main vide : rien.
- **Pack entier** : montage du deck sans erreur de construction (pas de capacités `Play` doubles, la gate
  `verifier_tous_les_decks` est la SEULE à l'attraper) ; `verifier_appels_modules.py` calibré puis lancé ; autoplay
  d'au moins 8 parties contre un témoin + grep des tracebacks ; une partie complète jouée à la main.

## 6. Limites de cette phase A (honnêteté)

- Rien n'a été exécuté : ni module chargé par le moteur, ni partie. Les appels d'API viennent de cartes modèles lues
  (Spider-Ham `30001a`, Sunfire, Break Through, Cybernetic Arm, etc.) et chaque nom de méthode appelé a été retrouvé
  dans `src/` par recherche de `def`, mais **la signature et le type du porteur n'ont pas été vérifiés** : ma
  vérification maison n'attrape pas un nom existant mal placé (calibrage : une erreur volontaire de type « méthode
  d'une autre classe » n'a PAS été vue ; ce filet est donc faible). `verifier_appels_modules.py` reste à lancer.
- Points d'API non prouvés : `Search.SearchForCards(range=(0, 2))` (« up to 2 »), `effect.GetPaidResources()` pour un
  coût d'ABILITÉ et pour des ressources générées par compteurs, `joueur.GetControlUpgrade()` (inclut-il les Sai
  attachées à l'identité ?), `CostFunc.Counter("YourIdentity", ...)` / `UnitCannotThwartTarget("YourIdentity")` depuis une
  obligation, `hero.DealDamage` répété sur une liste avec doublons (`tr005`), `GetEngagedPlayer()` (`tr002`),
  `MaxOnePerPhase` entre deux exemplaires.
- Lectures de scan à confirmer en jeu : PV de Casey Jones = 2 et d'Old Hob = 4 (cercle orange), CTR/ATQ 2* de Casey
  (étoile creuse = 1 dégât consécutif), traits lus tels qu'imprimés (aucun trait inventé pour Old Hob), nom
  « Old Hobb » avec deux b dans l'italique de `tr014` mais « Old Hob » sur la carte (conservé tel quel).
- Biographie ajoutée (`heros-info.js`) mais **la preuve par survol du héros dans le wizard n'a pas été faite**
  (aucun navigateur lancé) ; texte FR ajouté mais non déployé (`ui-app/deployer.sh` non lancé).
- Pas de `PROCESSUS-CARTE.md` rempli (gabarits de la phase C), donc aucune carte n'est « terminée ».

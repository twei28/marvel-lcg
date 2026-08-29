# TODO / SPEC — La campagne « Web of Deceit »

**Statut :** 🚧 **EN COURS.** Le scénario **#1 (Shocker) est dans le jeu et se
gagne** : 38 cartes, leurs images, leurs sets de rencontre, ses deux
difficultés, et les modules qui font tourner sa boucle (voir §13). Les quatre
autres scénarios, les modulaires restants et les spécialisations ne sont pas
commencés.
**Inventorié et lu le 2026-08-13.** Les 438 cartes du Drive sont
localisées, téléchargées et lisibles ; le livret est lu ; les 5 scénarios sont
définis ; le croisement avec l'existant est fait ; le scénario #1 est transcrit.
**Rien n'est encore dans le jeu.** Voir §7 à §11.
⚠️ **Ce n'est PAS qu'un travail de contenu** : le livret ajoute un système de
**spécialisations** (arbres de talents entre scénarios) que le moteur ne sait
pas faire. Voir §9.
**Origine :** demande utilisateur (dossier Google Drive partagé)
**Prérequis :** `2026-08-12-nommage-contenu-fanmade.md` (le préfixe `wd`)
**Source :** https://drive.google.com/drive/folders/1K0Q-41Aqy6tgPDMp0K6pYRKdv66IWCIN

---

## 1. Ce que contient le dossier (relevé le 12/8/2026)

**Nom : « Web of Deceit ».** Un rulebook et six sous-dossiers :

```
web-of-deceit-rulebook.pdf   8,6 Mo
Campaign - Rewards/
Campaign Setup Cards/
Heroes/
Modulars/
Other/
Scenarios/
```

C'est la structure exacte d'une campagne : récompenses, cartes de mise en place,
héros, sets modulaires, scénarios. ⚠️ **Le contenu de chaque sous-dossier n'a PAS
été inventorié** : la lecture s'est arrêtée à la liste. Premier geste du plan :
descendre dedans et compter.

Recoupement : une extension « Web of Deceit » circule sur le Workshop Steam avec
Alligator Loki, Beta Ray Bill, Doctor Octopus, Scarlet Spider/Kaine, The Lizard,
et des packs héros (Madame Web, Misty Knight, Mockingbird, Silver Sable,
Spider-Woman…). **À vérifier** : ce Drive est-il la même chose, une part, ou autre
chose ? Plusieurs de ces héros sont **déjà dans le jeu** (Madame Web = set 107,
Albert = 100). Le risque de doublon est réel et se mesure avant de coder.

## 2. Ce qui joue en notre faveur

**Le mode campagne n'a plus de dette connue** (12/8/2026, `docs/rapports/CAMPAGNES.md`).
Les huit boîtes sont jouées, les carnets se remplissent seuls, et depuis
aujourd'hui une campagne se joue à plusieurs. **Ajouter une neuvième campagne est
un travail de CONTENU, pas de moteur** — au contraire de l'aspect Determination.

Ce qui existe et se réutilise tel quel :

- `data/campagnes/<code>.json` : la définition (scénarios, champs de victoire,
  pages du livret). Modèle : `trors.json`, le mieux garni.
- `cards/pack/<code>/campaign.py` : les crochets `CampaignSetup(level)` posés sur
  le main scheme 1a. Modèle : `trors/campaign.py`.
- Le panneau de récompenses, les détecteurs, l'écriture automatique du carnet, la
  règle de défaite, la reprise : **rien à écrire**, tout se déclare en JSON.
- `tools/verifier_campagnes.py` refuse une clé de carnet que le moteur ne connaît
  pas, une `detection` inexistante, un `deck: "requis"` sans `parJoueur`.

## 3. Le nommage

Préfixe **`wd`**, selon `2026-08-12-nommage-contenu-fanmade.md` : `wd001`…
Un code de campagne `web_of_deceit` pour `data/campagnes/`.

⚠️ **Si des héros du Drive existent déjà dans le jeu**, ne PAS les redoubler : le
mécanisme `full_link` (`{"card_id": "wd051", "full_link": "32014"}`) pointe vers
une carte identique existante, sans module ni image. Il a servi pour Echo.

## 4. Les chantiers

1. **Inventorier le Drive**, sous-dossier par sous-dossier, et **lire le rulebook**
   (8,6 Mo). C'est lui qui donne l'enchaînement des scénarios, les règles de
   campagne et le contenu du carnet. Sans cette lecture, rien ne peut être conçu.
2. **Croiser avec l'existant** : quels héros, vilains et modulaires sont déjà là ?
3. **La définition de campagne** : `data/campagnes/web_of_deceit.json`, sur le
   modèle de `trors.json`.
4. **Le campaign log** : les champs de victoire, `auto` autant que possible. La
   règle acquise le 11/8 vaut ici : **aucun champ `auto` sans source**, et ce qui
   reste à saisir doit être une vraie décision du livret.
5. **Les scénarios** : `data/scenarios/*.json` + les modules de cartes.
6. **Les images** : redimensionner à l'import (voir la dette du 12/8).
7. **Les crochets** : `cards/pack/wd/campaign.py`.
8. **Les tests** : `verifier_campagnes.py`, `test_cards`, `test_generate_cards`,
   puis une vraie partie par scénario — c'est ce qui a trouvé les vrais bugs sur
   les huit boîtes précédentes.

## 5. À trancher

- **Le périmètre.** La campagne seule, ou aussi les packs héros qui l'accompagnent ?
  Ce sont deux chantiers de taille très différente.
- **Les droits.** Le site source dit ne pas détenir les droits sur le contenu
  qu'il compile. Usage strictement personnel, comme le reste du projet.
- **La campagne à plusieurs.** Elle marche depuis aujourd'hui, mais n'a jamais été
  jouée par un humain. Éprouver ça sur une campagne connue avant d'en ajouter une
  neuve serait plus sage.

## 6. Comment on saura que c'est fait

La campagne apparaît dans l'écran des campagnes, ses scénarios s'enchaînent, le
carnet se remplit tout seul entre deux scénarios, et une partie est menée de bout
en bout sur au moins le premier et le dernier scénario.

---

## 7. L'INVENTAIRE (13/08/2026) — 438 cartes, et où elles sont

Le Drive n'est pas listable par l'API : elle n'énumère pas les enfants d'un
dossier qu'on n'a que **reçu**. La page publique, elle, porte chaque entrée
avec son identifiant. `tools/importer_web_of_deceit.py` est la recette :
`--inventaire` descend l'arbre, `--telecharger` écrit chaque carte en JPEG
1000 px (assez pour LIRE son texte, et pour en tirer ensuite le 600x840 du jeu).

⚠️ **Le dossier mélange de vrais sous-dossiers et des RACCOURCIS** vers d'autres
dossiers du même auteur : quatre des cinq scénarios et tous les héros maison
sont des raccourcis. Un raccourci s'ouvre comme un dossier.

```
Campaign - Rewards/   50   les 5 spécialisations, 10 cartes chacune
Campaign Setup Cards/  9   Vote for Fisk (x2), The Great Web, 2 gobelins experts,
                           + le modulaire Bodyguard (4)
Modulars/             43   City Sewers 8, Crime Wave 6, Kraven 5,
                           Power Drain II 6, Standard III 17
Scenarios/           147   Shocker 20, Electro 25+6, The Lizard 27 (+City Sewers),
                           Vulture 29 (+Underling 14), Kingpin 26
Heroes/              148   Scarlet Spider, Superior Spider-Man, Venom (+Venomized),
                           Spider-Man 2099 — tous des RACCOURCIS, hors périmètre
Other/                     livret en PNG, planches d'impression, boîtes
```

**Le cœur de la campagne = ~230 cartes** (scénarios + modulaires + récompenses
+ mise en place), les 148 cartes de héros maison étant un autre chantier.

## 8. LES CINQ SCÉNARIOS, relevés dans le livret

| # | Scénario | Deck vilain | Complots principaux | Sets de rencontre |
|---|----------|-------------|--------------------|-------------------|
| 1 | Shocker | Shocker (A) — (B) en expert | Shock Party, Look Who Finally Showed, The Gang's All Here | Shocker, **City in Chaos**, Power Drain II, Crime Wave, Standard III |
| 2 | Electro | Electro (I)+(II) — (II)+(III) en expert | Power Outage, Power Surge | Electro, Power Drain II, **A.I.M. Science**, Standard III |
| 3 | The Lizard | The Lizard (A) | Chasing Down The Lizard, The Cure | The Lizard, City Sewers, **Down to Earth**, Standard III |
| 4 | Vulture | Vulture (I)+(II) — (II)+(III) | Surveillance Airship | Vulture, **A.I.M. Abduction**, Standard III |
| 5 | Kingpin | Kingpin (I)+(II) — (II)+(III) | Shadow of the Kingpin | Kingpin, Crime Wave, Standard III |

**Règles communes à tous les scénarios** (livret p.3) : le modulaire Bodyguard
est dans CHAQUE rencontre, son attachement est distribué face cachée au premier
joueur à la mise en place, et l'environnement « Vote for Fisk » entre en jeu.
En expert à plusieurs joueurs, « Vote for Fisk » passe sur sa face experte et
un gobelin expert (Green Goblin ou Hobgoblin) est mélangé au deck rencontre.

## 9. CE QUE LE LIVRET CHANGE — la fiche se trompait sur l'ampleur

**Le §2 disait « un travail de CONTENU, pas de moteur ». C'est faux**, et c'est
mesuré à la lecture :

* **Les spécialisations** (livret p.2 et p.4). Chaque joueur choisit en début de
  campagne un **arbre de talents** parmi cinq (Multiverse, Radioactive,
  Spider-Sense, Symbiosis, Web-Spinner), reçoit son palier 0 à la mise en place
  du scénario #1, puis **un palier de plus après chaque scénario gagné**.
  Certains paliers offrent un choix limité. Les cartes gagnées restent pour
  toute la campagne, **doivent** figurer dans le deck, et ne comptent pas dans
  la taille minimale. C'est un mécanisme que le mode campagne actuel ne connaît
  pas : le carnet sait poser des cartes IMPOSÉES, pas dérouler un arbre.
* **Quatre mots-clés neufs** : Negate X (piocher X si une partie de la carte a
  été annulée), Fragile (les attaques contre ce personnage gagnent transpercement),
  Legion (deux alliés Legion comptent pour un), Seek X (défausser du dessus de
  son deck jusqu'à défausser X).
* **Le Bodyguard** : un attachement qui va chercher le sbire le plus costaud du
  deck rencontre et le met en jeu. Le vaincre défausse l'attachement mais
  **remélange le sbire** dans le deck.

## 10. LE CROISEMENT AVEC L'EXISTANT — quatre modulaires sont déjà là

Vérifié dans `data/encounter_sets/` :

* **déjà dans le jeu** : `city_in_chaos`, `down_to_earth`, `aim_science`,
  `aim_abduction`, `power_drain`, et **`standard_iii`** ;
* **le « Standard III » du Drive est une RÉIMPRESSION** de celui d'Age of
  Apocalypse (mêmes textes, même « Pursued by the Past », art re-illustré) :
  vérifié carte par carte. Les 10 fichiers `pbtp-*` ne sont que l'art alternatif
  de `45075a/b` pour chaque vilain. **Rien à créer.**
* **à créer** : les 5 sets de vilain, `crime_wave`, `city_sewers`,
  `power_drain_ii`, `underling`, `kraven_the_hunter`, `bodyguard`, les 5 arbres
  de talents et les cartes de mise en place.

⚠️ **`Power Drain II` n'est pas `power_drain`** : c'est une variante fan-made du
set officiel, à créer à part.

## 11. LE SCÉNARIO #1 EST TRANSCRIT (16 cartes)

Relevé image par image (planches de 4 cartes, seule taille où le texte d'encart
reste lisible) :

| n° | Carte | Type | Ce qu'elle fait |
|----|-------|------|-----------------|
| 1A | Shocker | Vilain, 10 PV, 1 SCH / 1 ATK, CRIMINAL | Steady. When Defeated : retirer 5 menaces d'une manigance secondaire, retourner cette carte. |
| 1B | Shocker (expert) | Vilain, 20 PV, 2/2, + MASTERS OF EVIL | Retaliate 1. When Defeated : 1 dégât à chaque héros, retirer 10 menaces d'une secondaire, retourner. |
| 2A/2B | Shock Party | Complot 1A/1B | Setup : chercher The Long Night et la révéler ; retirer du jeu chaque obligation du deck rencontre. When Revealed : chercher Vibro-Shock Gauntlets et la révéler. |
| 3A/3B | Look Who Finally Showed | Complot 2A/2B | When Revealed : mettre Rhino en jeu engagé avec le premier joueur, révéler Grand Larceny. Forced Response : après que Shocker ou Rhino est vaincu, retirer 1 menace d'ici. |
| 4A/4B | The Gang's All Here | Complot 3A/3B | When Revealed : chaque joueur sans sbire unique en cherche un et le révèle. Vibro-Shock Gauntlets gagne permanent. Stade accompli = défaite. |
| 5 | Vibro-Shock Gauntlets | Attachement, TECH. WEAPON | Attaché à Shocker, +1 ATK. Forced Response : défausser une carte. Hero Action : payer 2 pour retirer un statut de Shocker et défausser. |
| 6 | Sandman | Sbire 5 PV, 2 SCH / 2 ATK | Toughness. Forced Response : défausser les 6 cartes du dessus du deck rencontre. |
| 7 | Scorpion | Sbire 5 PV, 2/3, ELITE | Forced Response (héros) : à l'engagement, étourdit. |
| 8 | Vulture | Sbire 4 PV, 1/3, AERIAL | Quickstrike. Forced Response : défausse 1 carte au hasard sauf si l'identité est AERIAL. |
| 9 | Feedback | Traîtrise | Étourdit l'identité ET Shocker, défausse la main, repioche. |
| 10 | Ionic Boots | Attachement, TECH. WEAPON | +★ ATK. 2 menaces sur le complot quand Shocker blesse. Hero Action : payer 3 pour défausser. |
| 11 | Grand Larceny | Manigance secondaire, 5 menaces | La menace ne peut pas être retirée de The Long Night. Hero Response : après qu'un CRIMINAL est vaincu, retirer 5 menaces d'ici. |
| 12 | The Getaway | Traîtrise | Au choix : soigner 3 et Shocker complote, ou faire revenir les Gauntlets. |
| 13 | The Check Cleared | Traîtrise | Surge. Menace sur The Long Night égale à la somme des SCH des CRIMINAL en jeu. |
| 14/15 | Get Shocked! | Traîtrise ×2 | Étourdit, 1 dégât à chaque héros. |
| 16 | The Long Night | Manigance secondaire, 10 menaces | Permanent. Hinder 15. **Les joueurs ne peuvent pas gagner tant qu'elle est là** ; retirer sa dernière menace = victoire. |

⚠️ **Le livret est en retard sur les cartes** : sa page 15 montre un Shocker
avec « Forced Interrupt : quand Shocker serait vaincu, remettre ses PV à 10 »,
que la carte du dossier ne porte plus (elle dit « When Defeated : retourner
cette carte »). **Les fichiers du Drive font foi**, pas les captures du livret.

## 12. LE PLAN, dans l'ordre

1. ~~Inventorier le Drive et lire le livret.~~ **FAIT** (§7 à §9).
2. ~~Croiser avec l'existant.~~ **FAIT** (§10).
3. **Trancher le périmètre** (§5) : la campagne seule (~230 cartes) — les héros
   maison sont un chantier séparé, et trois d'entre eux (Venom, Spider-Man 2099,
   Superior) demandent en plus un aspect maison (« Venomized »).
4. **Décider du sort des spécialisations** (§9) : c'est le seul vrai chantier
   MOTEUR. Trois voies, à mesurer avant de choisir : les câbler comme un vrai
   arbre (le plus fidèle), les traiter comme des cartes imposées de carnet (le
   moins cher, et le carnet sait déjà le faire), ou livrer la campagne sans
   elles d'abord (écart assumé et écrit).
5. Le scénario **#1 Shocker** de bout en bout : 16 cartes, données, images,
   modules, puis une vraie partie. C'est lui qui donnera la vitesse réelle.
6. Les scénarios #2 à #5, puis les modulaires, puis les récompenses.

**Ce qui est déjà prêt pour la suite** : les 460 images sont téléchargées dans
`medias/web-of-deceit-source/` (dossier ignoré par git, comme `assets/pics/`),
`tools/importer_web_of_deceit.py` sait les reprendre en une commande, et la
méthode de transcription est éprouvée : **une planche de 4 cartes par lecture**,
au-delà le texte d'encart n'est plus sûr.

---

## 13. LE SCÉNARIO #1 EST DANS LE JEU (14/08/2026)

**Boîte 120, préfixe `wd`** déclaré au registre. 38 faces (34 cartes physiques,
les 4 recto-verso comptant double) : le set Shocker (16), Crime Wave (6),
Power Drain II (6), Bodyguard (4) et les cartes de mise en place de la campagne
(Vote for Fisk standard et expert, The Great Web, les deux gobelins experts).

Ce qui n'a PAS été créé, et c'est voulu : `city_in_chaos` et `standard_iii`
existaient déjà (§10), le scénario les référence tels quels. **Rhino, que le
complot 2A va chercher, est la carte officielle de City in Chaos.**

### La boucle du scénario, et pourquoi elle demandait des modules

Shocker **n'est jamais vaincu pour de bon** : le vaincre retire de la menace
d'une manigance secondaire et le RETOURNE (face A ↔ face B). La seule façon de
gagner est de vider **The Long Night**. Sans module, le moteur terminait la
partie sur la défaite de Shocker : le bot « gagnait » en 3 rounds sans avoir
joué le scénario.

Mesuré après les modules, dans le journal d'une vraie partie :

```
"WhenUnitWouldBeDefeated" est remplacé par [Shocker (B)]
[Shocker] would deal 1 damage to [Spider-Man]
[The Long Night] perd 10 pion(s) « threat »
[Shocker (A)] is entering play
```

C'est exactement le texte de la carte, et la victoire tombe désormais par
`Players Won` depuis The Long Night, pas par la mort du vilain.

### Deux pièges payés

* **`GiveKeywordToInPlayWhenApplyThis` rend une LISTE d'abilités**, pas une.
  Sans l'étoile de dépaquetage, la carte se construit avec une liste dans sa
  liste et le moteur plante au chargement du scénario
  (`'list' object has no attribute 'paper'`).
* **`ThreatCannotBeRemovedFromWhile` ne prend pas de nom de carte** : son
  paramètre `from_card_name` est commenté dans la fabrique. Le filtre par nom
  passe par une condition.

### Ce que la mesure dit

* `verifier_prefixes` : 4930 cartes, 22 préfixes, aucun doublon.
* `verifier_cartes_en_jeu` : **les 38 cartes portent ce que leur texte annonce**
  (2 écarts corrigés : une valeur `SCH` sur un environnement, que le moteur ne
  connaît pas).
* `test_cards` : **4371 ok / 0 erreur** (+19 modules, +1 corrigé en route).
* `verifier_appels_modules` : OK sur `web_of_deceit`.
* `autoplay` : 3 parties, **2 victoires par The Long Night**, 1 bloquée.

⚠️ **La partie bloquée est un vrai point ouvert** : la question « Remove threat
from » posée quand Shocker se retourne revient à l'identique sans que le plateau
bouge (le garde-fou anti-boucle d'`autoplay` l'a nommée). À reprendre avant de
déclarer le scénario jouable par un humain.

### Ce qui reste, dans l'ordre

1. La question bloquante ci-dessus.
2. Les modules des cartes restantes du lot (Crime Wave, Power Drain II,
   Bodyguard, mise en place) : **écrits pour le set Shocker uniquement**.
3. Les scénarios #2 à #5 : ~110 cartes, la méthode est rodée (planche de 4
   cartes, une lecture par planche ; données ; images ; modules ; autoplay).
4. Les 5 arbres de talents (50 cartes) et la définition de campagne, une fois la
   voie tranchée (§12, point 4).

---

## 14. LE LOT 1 EST COMPLET (14/08/2026)

### La boucle de Shocker tournait à l'infini, et pourquoi

Le blocage relevé au §13 n'était pas la question posée : c'était **un
retournement sans fin**. Mesuré dans le journal, A → B → A → B sans reprendre
la main.

**Les points de vie sont portés par la CARTE, pas par la face**
(`CardFace.components` rend `self.card.components`). Une carte retournée à 0 PV
arrive donc sur sa nouvelle face **déjà vaincue**, et le moteur redéclenche la
défaite pendant le retournement, avant même que la ligne suivante ne s'exécute.

On rend donc ses PV à la face AVANT de retourner, puis on remet la nouvelle face
à son propre maximum. Entre les deux, la carte n'est jamais à zéro.

⚠️ **Ce bug rendait le scénario FAUX dans l'autre sens** : à 0 PV, le moindre
dégât redéclenchait la défaite, chaque coup retirait 5 ou 10 menaces de The Long
Night, et le bot gagnait en 3 rounds. Corrigé, il perd — ce qui est le
comportement attendu d'un scénario où le vilain ne meurt jamais.

### Six cartes n'avaient pas besoin d'un module

Relevé en comparant les textes AVANT d'écrire : **Power Drain II est le set
officiel Power Drain** (02041-02045) avec une carte de plus, et **Crime Pays**
et **Honor Among Thieves** existent déjà (Sinister Syndicate, Space Pirates).
Six `ability_link` plutôt que six modules, et la fidélité est celle du moteur
officiel.

Restaient à écrire : l'Electromagnetic Pulse généralisée (le set a DEUX Electro,
la carte officielle n'en nommait qu'un), la seconde Electro, les quatre cartes
du Bodyguard et les cinq cartes de mise en place.

### Le piège qui se répète : les fabriques qui rendent une LISTE

`GiveKeywordToInPlayWhenApplyThis` **et** `GiveKeywordToAttached` rendent une
liste d'abilités. Sans dépaquetage, la carte se construit avec une liste dans sa
liste et le moteur plante à la génération.

⚠️ **`test_cards` ne le voit pas** : il appelle `GetAbilities()` sans poser le
résultat sur une carte. Seule une vraie partie l'attrape. C'est la deuxième fois
dans ce lot.

### Trois écarts assumés, écrits

* **Multiverse Recruit** cherche « votre COLLECTION » : le moteur ne sait ouvrir
  que ce qui est dans la partie. On prend le sbire de némésis mis de côté.
* **« gains Victory 0 »** n'est pas rendu : Victory est un attribut de données,
  pas un mot-clé qui se donne en jeu.
* **The Great Web** lève la règle d'unicité pour une FAMILLE de cartes
  (WEB-WARRIOR ou « Spider » dans le titre) : `UniqueRuleNotApplyTo` ne sait
  viser qu'une carte, d'où une abilité écrite à la main sur le même message.

### Mesure

`test_cards` **4382 ok / 0 erreur**, `verifier_appels_modules` OK,
`verifier_cartes_en_jeu` « les 38 cartes portent ce que leur texte annonce »,
et **8 parties menées sans un seul incident** (normal et expert), toutes perdues
par les héros — le scénario est dur, et il doit l'être.

## 15. LA VOIE DES SPÉCIALISATIONS EST TRANCHÉE (14/08/2026)

Des trois voies du §12, c'est **le carnet de campagne** qui est retenu.

**Pourquoi** : le mode campagne sait déjà poser des **cartes imposées** dans le
deck d'un joueur entre deux scénarios (`deck: "requis"`, `parJoueur`), et c'est
exactement ce qu'est un palier d'arbre de talents — « ces cartes restent avec le
joueur pour le reste de la campagne et **doivent** figurer dans son deck »
(livret p.2). Le carnet sait aussi offrir un CHOIX entre plusieurs cartes, ce
que demandent les paliers à options.

**Ce que cette voie ne rend pas, et il faut le savoir** : l'arbre ne s'affichera
pas comme un arbre. Le joueur verra, entre deux scénarios, la liste des cartes
que son palier lui donne. La progression est fidèle, sa mise en scène ne l'est
pas.

**Ce qui reste à faire pour les livrer** : transcrire les 50 cartes (5 arbres ×
10), les entrer comme cartes joueur du pack `wd`, et écrire
`data/campagnes/web_of_deceit.json` sur le modèle de `trors.json`, avec un champ
de carnet par joueur et par palier.

---

## 16. LE SCÉNARIO #2 EST DANS LE JEU (14/08/2026)

**21 faces neuves, `wd035` à `wd053`.** Le set Electro n'est pas de Ripper3 :
c'est celui de **DesignHacker** (« ELECTRO (2.0) », 24 cartes), que la campagne
reprend en **remplaçant le deck de complots et les deux A.I.M. Scientist**
(livret p.17). Les quatre complots `Power Outage` / `Power Surge` et les deux
savants de remplacement viennent du dossier `Scenarios/Electro (Web of Deceit)/`.

**Ce qui n'a PAS été créé, et c'est voulu** : le complot autonome
« Energized! » (4/24), que le mode campagne remplace, et les deux A.I.M.
Scientist du set autonome (9/24 et 10/24), remplacés eux aussi. `A.I.M. Science`
et `Standard III` existaient déjà.

### Ce que le scénario fait, et pourquoi il tient debout

* **Electricity Clones** lève la règle d'unicité pour Electro. C'est la carte qui
  tient tout : le vilain, les deux sbires Electro du set et les deux de
  Power Drain II portent le même nom. Sans elle, un seul tiendrait la table.
* **Grounded** empêche le vilain d'être vaincu tant que le coût cumulé des
  améliorations et des soutiens en jeu est inférieur à 10 par joueur. Mesuré
  dans une vraie partie : `"WhenUnitWouldBeDefeated" est remplacé par [Grounded]`,
  et le vilain reste à 0 PV round après round. Le scénario demande de s'équiper
  avant de pouvoir frapper, exactement comme le livret l'annonce.
* **L'accélération gouverne la partie** : Power Outage soigne le vilain d'un
  point par jeton et par icône, Accelerated Plans pose 2 menaces par jeton et
  icône, Dark Matter Conversion 1 de plus. Une seule mesure, écrite une fois
  (`JetonsEtIconesDAcceleration`).

### Un écart de forme, écrit

**Power Surge (2B) porte une icône d'accélération imprimée**, et le moteur ne
sait pas la lire sur un complot PRINCIPAL : `Acceleration` est un attribut de
manigance secondaire, de sbire ou d'environnement, et `MainScheme` n'hérite pas
de `HasAccelerationIcon` — la carte refusait de se générer (`KeyError`).

Le stade pose donc **un jeton d'accélération sur lui-même à sa révélation**.
L'effet est le même au pion près : l'escalade du complot principal additionne
les jetons et les icônes (`scheme_main.py`), et le « for each acceleration token
and icon in play » des trois autres cartes le compte aussi. Mesuré dans le
journal : `[Power Surge] reçoit 1 pion(s) « acceleration_token »`.

### Deux écarts du LOT 1, corrigés au passage (commit à part)

* **Neuf images entraient dans le jeu couchées** : Ripper3 exporte tout en
  1000x1433, complots et manigances compris, qui sont des cartes PAYSAGE
  stockées debout. Une table `PAYSAGE` les redresse.
* **« Look Who Finally Showed » démarrait à 7 menaces par joueur** pour un seuil
  de 6 : le stade 2 arrivait déjà accompli à plusieurs joueurs. La carte dit 1.

### Mesure

`verifier_prefixes` 4951 cartes / 22 préfixes / 0 doublon ;
`verifier_cartes_en_jeu` « les 59 cartes portent ce que leur texte annonce » ;
`verifier_appels_modules` OK ; `test_cards` **4403 ok / 0 erreur** ;
`sonde_capacites` : les 21 faces portent leurs capacités ;
`autoplay` **8 parties Electro (normal et expert) sans un seul incident**,
toutes perdues — le stade 2 est atteint et accompli, la boucle tourne.

⚠️ **UN POINT OUVERT, qui n'est PAS du scénario #2** : `autoplay` bloque une
partie de Shocker expert sur une question `When_Defeated` de **Power Drain
(`wd020`, lié à la carte officielle `02041`)** — « chaque joueur défausse 1
ressource par icône de boost ». Vérifié en remettant la donnée d'avant le
correctif : **le blocage préexiste**, il ne vient pas du lot 2.

---

## 17. LE SCÉNARIO #3 EST DANS LE JEU (14/08/2026)

**23 faces neuves, `wd054` à `wd073`** : le set The Lizard (18 faces) et le
modulaire fan-made **City Sewers** (5 cartes), que ce scénario impose avec
`down_to_earth`, déjà dans le jeu.

### La boucle, et ce qu'elle a demandé au moteur

The Lizard n'est **jamais vaincu** non plus, mais autrement que Shocker : le
vaincre le retourne en **Curt Connors**, qui se bat contre son propre cerveau.
Deux compteurs neufs portent tout le scénario, déclarés dans `CardFace.COUNTER`
avec les autres compteurs fan-made :

* **`formula`**, sur The Lizard : +1 ATK à chaque ennemi REPTILIAN par compteur.
  La mise en place en pose 1, 2 en expert ; The Cure (2A) en ajoute un.
* **`sanity`**, sur **Lizard Brain** : vaincre The Lizard en pose 1 par joueur.
  Chaque activation de Connors en retire un — il **retire** de la menace au lieu
  d'en poser, et **ne frappe pas**. Le dernier compteur retiré rend The Lizard.

Mesuré dans le journal d'une vraie partie, dans l'ordre :

```
"WhenUnitWouldBeDefeated" est remplacé par [The Lizard]
[Lizard Brain] reçoit 1 compteur(s) « sanity »
[Curt Connors] was flipped
"WhenUnitWouldAttack" est remplacé par [Curt Connors]
[Lizard Brain] perd 1 compteur(s) « sanity »
[The Lizard] was flipped
```

**Le trait REPTILIAN** a rejoint la liste des traits du moteur, avec
`A.I.M. SCIENTIST` et `MULTIVERSE` que les lots précédents utilisaient déjà sans
les déclarer.

### Negate X, le premier des quatre mots-clés neufs

« After this card is revealed or turned faceup during an enemy activation, if
any of its effects are canceled, the revealing player draws X cards. »

Le moteur **annonce déjà** l'annulation d'une carte rencontre : `CancelEffects`
et `CancelAllEffectsInternal` envoient `WhenEffectBeCancel`, et le présentateur
l'affiche même sous le nom « negate ». Il n'existe pas de fabrique pour ce
message : l'abilité se construit à la main, une fois, dans
`city_sewers/__init__.py`.

⚠️ **Écart écrit** : le texte restreint le mot-clé à une annulation survenue
PENDANT une activation d'ennemi. Le moteur ne rapporte pas ce contexte dans le
message, la carte pioche donc quelle que soit la fenêtre d'annulation.

### Deux autres écarts, écrits

* **Curt Connors a « HIT POINTS ∞ »**. Les PV sont portés par la CARTE, pas par
  la face (leçon du lot 1) : les deux faces déclarent donc les mêmes 12 par
  joueur, et c'est une abilité « ne peut pas être vaincu » qui rend le sens
  jouable de l'infini.
* **Son ATK est une étoile**, pas un nombre : la donnée porte 0, et le
  `Forced Interrupt` remplace de toute façon l'attaque entière.

### Ce que la mesure dit

`verifier_prefixes` OK ; `verifier_cartes_en_jeu` « les 82 cartes portent ce que
leur texte annonce » ; `verifier_appels_modules` OK ; `test_cards` **4426 ok /
0 erreur** ; `sonde_capacites` : les 23 faces portent leurs capacités ;
`autoplay` **24 parties** sur les trois scénarios, normal et expert.

### ⚠️ CE QUE CE LOT A TROUVÉ SUR LES PRÉCÉDENTS

**`autoplay` écrit une traceback dans le journal de la partie et CONTINUE** : le
compteur d'incidents ne la voit pas, et le rapport annonce « 0 incident ». Les
huit parties du lot 1 en portaient **une chacune**. La vérification vraie, c'est
`grep NameError|AttributeError|TypeError` dans les journaux.

Cinq appels plantaient ainsi en silence (commit à part) : `GameRule` importé
nulle part — **le mode expert de Shocker était faux, sa face B arrivait à 10 PV
au lieu de 20** — , `Faces.AttachAllTo` et `CardFinder(card_id=)` qui n'existent
pas — **« Vote for Fisk » n'entrait dans AUCUN scénario de la campagne** — , et
`AttachTo2` appelé sur une carte joueur qui n'est pas un `Asset2`.

**Mesure après correction : ZÉRO traceback sur 24 parties.**

### Ce qui reste

1. Les scénarios **#4 Vulture** (set Vulture + modulaire Underling) et
   **#5 Kingpin** (set Kingpin + modulaire Kraven the Hunter).
2. Les 50 cartes des 5 arbres de talents et `data/campagnes/web_of_deceit.json`.
3. Le point ouvert de Power Drain (`wd020`), qui bloque une partie de Shocker
   expert et **préexiste** aux lots 2 et 3.

---

## 18. LE SCÉNARIO #4 EST DANS LE JEU (14/08/2026)

**18 faces neuves, `wd074` à `wd090`.** Le scénario n'a **qu'un seul complot
principal** (Surveillance Pigeons) et trois stades de vilain, deux joués.

⚠️ Le §8 de cette fiche annonçait « Surveillance **Airship** » : c'est une
erreur de relevé, la carte du Drive dit **Surveillance Pigeons**. Et la face 1A
porte « KINGPIN (4/24) » en pied de carte, une coquille de l'auteur que le
verso corrige.

### Quatre réimpressions, quatre modules en moins

Relevé en comparant les textes AVANT d'écrire, comme au lot 1 :

| carte | officielle | ce qui est identique |
|-------|-----------|---------------------|
| The Vulture's Plans | `01169` | texte et boost au mot près |
| Highway Robbery | `01166` | texte, boost, accélération, menace |
| Aerial Dogfight | `50159` | tout, jusqu'à `Hinder 2[per_hero]` |
| Sweeping Swoop | `01168` | le **boost** seulement |

Sweeping Swoop est le cas limite : son boost est celui de la carte officielle,
mais son « When Revealed » déferle TOUJOURS là où l'officielle ne déferle que si
Vulture est en jeu. Pas de lien possible, mais la même fabrique
(`BoostIfThisActivationDealsDamage`) fait le travail.

### Les pigeons sont un BOUCLIER, pas une menace

Le compteur `pigeon` vit sur le complot **principal**. Tant qu'il y en a trois,
la prochaine tentative de retirer de la menace en retire **trois pigeons à la
place** : le réseau de surveillance encaisse. Chaque Aerial Advantage détruit,
chaque Aviator Goggles posé, chaque harnais rendu en ajoute.

Mesuré dans le journal : `[Surveillance Pigeons] reçoit 1 compteur(s) « pigeon »
([Aerial Advantage])`.

**La mise en place distribue une carte JOUEUR**, le Wingsuit V2, une par joueur,
et met les deux Aerial Advantage en jeu sur le vilain. Mesuré :
`[Peter Parker] equipped [Wingsuit V2]`, puis `[Vulture] equipped [Aerial
Advantage]` deux fois.

### Un écart, écrit

**« Vulture cannot be attacked ... unless the attack has ranged »** : `ranged`
est une propriété de l'ATTAQUE, pas d'une carte, et la fenêtre qui décide si
Vulture peut être ciblé (`CheckIfUnitCanBeAttackBy`) est **antérieure à la
déclaration de l'attaque** — la portée n'y existe pas encore. Seul le trait
AERIAL est donc vérifié, sur l'attaquant comme sur la carte qui porte l'attaque.
C'est la voie que le scénario met en avant : le Wingsuit distribué à la mise en
place donne justement ce trait.

### Ce que ce lot a trouvé sur les précédents

* **`"Attached"` n'est pas un littéral que le moteur connaît** — la liste dit
  `AttachedMinion`, `AttachedVillain`, `AttachedIdentity`... Une chaîne inconnue
  est traitée comme une SÉQUENCE de caractères et lève une assertion. Le
  Bodyguard (`wd026`) plantait donc à chaque fois que son sbire était vaincu.
* **`AfterYouResolveTreachery` exige un joueur comme initiateur**, et
  l'initiateur d'un complot principal est le VILAIN : Power Surge (`wd039b`)
  levait une assertion à chaque traîtrise d'Electro résolue. L'abilité est
  reconstruite à la main, sans le filtre « you ».

### Mesure

`verifier_prefixes` OK ; `verifier_cartes_en_jeu` « les 100 cartes portent ce que
leur texte annonce » ; `verifier_appels_modules` OK ; `test_cards` **4440 ok /
0 erreur** ; `sonde_capacites` : les 18 faces portent leurs capacités ;
`autoplay` **24 parties sur les quatre scénarios**, normal et expert,
**zéro traceback**.

⚠️ **Le modulaire `Underling` (14 cartes) n'est PAS livré** : il est dans le
dossier du scénario Vulture mais le livret ne l'impose à aucune rencontre. À
créer avec le lot Kingpin, ou séparément.

---

## 19. LE SCÉNARIO #5 EST DANS LE JEU (14/08/2026) — LES CINQ SONT LÀ

**17 faces neuves, `wd091` à `wd106`.** Un seul complot principal, trois stades
de vilain dont deux joués. **Le trait `CORRUPT`** rejoint la liste du moteur.

### Ce que le scénario fait

* **Tout le set nourrit « Pursued by the Past »**, la carte de Standard III, en
  compteurs `pursuit` : la mise en place en pose 1 par joueur, le complot 1 par
  round, Long Live the King 1, Lady Bullseye 2 en mourant. Typhoid Mary et le
  boost de King's Gambit s'en servent comme d'une jauge.
* **Le costume encaisse à la place de Kingpin.** Ce n'est pas une unité : les
  dégâts détournés sont des COMPTEURS posés dessus, et Fisk Tower les lui retire
  un par un. Mesuré : `"WhenUnitWouldTakeDamage" est remplacé par [Kingpin's
  Suit]`, puis `[Kingpin's Suit] reçoit 1 compteur(s) « damage »`.
* **Fisk Tower charge les manigances corrompues** à la valeur du stade du
  vilain. Mesuré en expert : `[Corrupt] reçoit 2 pion(s) « threat » ([Fisk
  Tower])`.

### L'écart le plus gros de toute la campagne, écrit

**« Put the top card of your deck into play facedown as a CORRUPT side
scheme. »** Le jeu physique retourne LA carte du dessus du deck du joueur et
s'en sert comme manigance : la carte est à la fois le coût et l'obstacle.

Le moteur ne sait pas faire d'une carte joueur une manigance de rencontre.
`TreatAsMinion` échange bien une face contre une autre, mais il est écrit pour
les alliés et les héros, et la manigance qui en sortirait ne saurait ni entrer
dans la bonne zone ni revenir à son propriétaire.

**On paie donc le coût ET on pose l'obstacle, en deux gestes** : la carte du
dessus du deck part à la défausse, et un exemplaire de `wd106` — le patron
« Corrupt », mis de côté à la mise en place, huit exemplaires — entre en jeu à sa
place. Le joueur perd la même carte, la table porte la même manigance, et sa
menace de départ vient de Fisk Tower comme le veut le texte. **Seule l'identité
de la carte posée change, et elle était face cachée de toute façon.**

`wd106` n'existe pas dans le jeu physique et emprunte l'art de Devil's Reign.

### Deux autres écarts

* **FBI Investigation est une obligation SANS héros.** Le moteur exige un champ
  `GiveTo` (`assert self.printed_give_to != None`) : la donnée porte une chaîne
  vide, ce que le moteur lit comme « au joueur qui la révèle » — exactement ce
  que veut une obligation venue du deck rencontre.
* **`GiveKeywordToAttached` ne nomme ni `acceleration_icon` ni `crisis`**, deux
  mots-clés que `CardFace.Gain` sait pourtant donner. Controlling the Narrative
  passe par `apply`, la porte que la fabrique laisse ouverte.

### Mesure

`verifier_prefixes` OK ; `verifier_cartes_en_jeu` « les 117 cartes portent ce que
leur texte annonce » ; `verifier_appels_modules` OK ; `test_cards` **4456 ok /
0 erreur** ; `sonde_capacites` : les 17 faces portent leurs capacités ;
`autoplay` 8 parties Kingpin, **zéro traceback**.

⚠️ **DEUX POINTS OUVERTS, tous deux du PILOTE et non du contenu** :

1. `autoplay` boucle sur une **action de héros qui échoue** : il la rechoisit
   sans fin au lieu de se désister. Mesuré sur **Tenacity (`01093`), une carte
   officielle**, autant que sur le Hero Action de Kingpin's Cane. Le pilote de
   `test_capacites` sait décliner au bout de trois répétitions ; celui
   d'`autoplay` ne le sait pas.
2. Le blocage de **Power Drain** (`wd020`) sur Shocker expert, relevé au §17 et
   vérifié comme **préexistant**.

### Ce qui reste, dans l'ordre

1. Les modulaires **`Underling`** (14 cartes, dossier Vulture) et **`Kraven the
   Hunter`** (5 cartes), qu'aucun scénario n'impose mais qui font partie du
   dossier de campagne.
2. Une passe d'**icônes** sur les lots 1 à 3 : plusieurs cartes portent une
   icône (accélération, crise, danger) que la donnée ne déclare pas.
3. Les **50 cartes des 5 arbres de talents** et
   `data/campagnes/web_of_deceit.json`.

---

## 20. LA PASSE DE FINITION SUR LES CINQ VILAINS (14/08/2026)

**122 cartes dans le pack.** Cette passe reprend les cinq lots livrés et ferme
ce qui restait ouvert **côté contenu**.

### Le modulaire Kraven the Hunter est là (5 cartes, `wd107`–`wd111`)

Aucun scénario ne l'impose — le livret recommande Crime Wave pour Kingpin — mais
il fait partie du dossier de campagne. Prey for Mercy verrouille sa propre
menace tant que Kraven tient la table, le Tiger perce, et Pit Trap coûte un
redressement. Deux traits neufs déclarés au moteur : `TRAP!` et `UNDERLING`.

### ⚠️ « Underling » N'EST PAS un modulaire — le §7 se trompait

Le dossier `Scenarios/Vulture/Underling/` (14 cartes) n'est pas un set de
rencontre : c'est une **variante entière du set Vulture**, numérotée
« VULTURE (1/14) » à « (14/14) », où le vilain porte le trait **UNDERLING** et
un texte différent — *retaliate 2 pendant la phase du joueur au lieu de ne pas
pouvoir être attaqué*, et une mise en place qui cherche un environnement
« Skies Over New York » absent du set principal.

C'est **une deuxième façon de jouer Vulture**, pas un modulaire à ajouter à une
rencontre. **Non livrée**, et c'est un choix : la livrer voudrait dire un
sixième scénario, pas cinq cartes de plus.

### Quatre icônes que la donnée ne déclarait pas

Relevé image par image sur les manigances et les sbires des lots 1 à 3 :

| carte | ce qui manquait |
|-------|-----------------|
| `wd011` Grand Larceny | icône de **crise** |
| `wd044` A.I.M. Scientist | icône d'**accélération** (comme l'officielle `50083`) |
| `wd048` Accelerated Plans | **deux** icônes d'accélération, tout le sel de la carte |
| `wd066` Scaly Setback | `Boost` 3 alors que la carte en porte **2** (deux flèches et une étoile) |

### Un dernier appel qui plantait en partie

`HasPermanent` expose `permanent`, pas `is_permanent` : Controlling the
Narrative (`wd098`) plantait au moment de choisir la manigance à attacher.
Trouvé par une partie qui faisait tourner Kraven, pas par `test_cards`.

### Mesure finale, sur les cinq scénarios

`verifier_prefixes` OK ; `verifier_cartes_en_jeu` « les 122 cartes portent ce que
leur texte annonce » ; `verifier_appels_modules` OK ; `test_cards` **4461 ok /
0 erreur** ; `sonde_capacites` : toutes les faces portent leurs capacités ;
`autoplay` **36 parties** (Shocker, Electro, The Lizard, Vulture, Kingpin, plus
une rencontre montée avec Kraven), normal et expert, **ZÉRO traceback**.

### ⚠️ Ce qui reste ouvert, et qui ne vient pas du contenu

**Quatre parties sur 36 se bloquent, toutes de la même façon** : le pilote
d'`autoplay` repose la même question et le plateau ne bouge pas. Trois causes
identifiées, dont **deux ne sont pas de ce pack** :

* **Tenacity (`01093`)**, carte joueur OFFICIELLE : « Hero Action: Spend a
  [physical] resource and discard this card → ready your hero ». Le pilote la
  choisit quand elle ne peut pas se résoudre et la rechoisit sans fin.
* **Power Drain (`wd020`)**, lié à l'officielle `02041` : blocage **vérifié
  comme préexistant** en remettant la donnée d'avant le lot 2.
* **Kingpin's Cane (`wd100`)**, même famille : un Hero Action à coût que le
  pilote propose sans pouvoir le payer.

Le garde-fou `MAX_REPETITIONS` d'`autoplay` est fait pour une option refusée puis
reproposée ; il ne sait pas se désister quand **l'unique** option d'une question
échoue. **C'est l'outil qu'il faudrait reprendre, pas les cartes** — et le faire
sans mandat sur un outil éprouvé aurait été un refacto opportuniste.

### Ce qui reste à faire sur la campagne

1. Les **50 cartes des 5 arbres de talents** (`Campaign - Rewards/`) et
   `data/campagnes/web_of_deceit.json` sur le modèle de `trors.json` — la voie
   est tranchée depuis le §15 : le carnet de campagne.
2. La variante **Underling** de Vulture, si on la veut (§ ci-dessus).
3. Le désistement du pilote d'`autoplay`.

---

## 21. LES ARBRES DE TALENTS ET LE CARNET (14/08/2026) — LA CAMPAGNE EST COMPLÈTE

**172 cartes dans le pack `wd`**, `wd001` à `wd161`.

### Les 50 cartes des cinq arbres (`wd112`–`wd161`)

Cinq voies de dix cartes, dans l'ordre exact des paliers du livret :

| palier | quand | combien | cartes |
|--------|-------|---------|--------|
| 0 | avant le scénario 1 | 1 sur 1 | `wd112`, `wd122`, `wd132`, `wd142`, `wd152` |
| 1 | après le scénario 1 | 1 sur 2 | les deux suivantes de l'arbre |
| 2 | après le scénario 2 | 1 sur 3 | |
| 3 | après le scénario 3 | 1 sur 3 | |
| 4 | après le scénario 4 | 1 sur 1 | la dixième |

**Six d'entre elles sont doubles** : elles portent l'aspect d'un des cinq
classiques en plus de l'étiquette Campagne (« This card is both a Web of Deceit
Campaign Reward card and an Aggression card »). Elles sont déclarées
`Campaign;Aggression`, `Campaign;Justice`, `Campaign;Protection`,
`Campaign;Leadership` et `Campaign;'Pool`, sur le modèle des `Hero;Aggression`
officiels.

Deux compteurs de plus au moteur : **`bot`** (Spider-Bots) rejoint `formula`,
`sanity` et `pigeon`.

### Le carnet — `data/campagnes/web_of_deceit.json`

Écrit sur le modèle de `trors.json`, avec un `campaign.py` qui rend au deck de
chaque joueur les paliers déjà gagnés à chaque mise en place de campagne. Les
cinq complots 1A l'appellent.

`verifier_campagnes` : **« web_of_deceit — 6 clés déclarées, OK »**, et « toutes
les clés déclarées existent dans le moteur ». C'est l'outil qui attrape le piège
documenté au §5 de `docs/rapports/CAMPAGNES.md` : une clé mal orthographiée ne lève rien
du tout, la récompense ne s'applique pas, et on ne s'en aperçoit qu'après cinq
scénarios joués pour rien.

### Deux écarts, écrits

* **Les cinq arbres sont proposés ensemble.** Le carnet ne retient pas quel arbre
  le joueur a choisi : à chaque palier il voit les 5, 10 ou 15 options de tous
  les arbres et prend celle du sien. C'est la conséquence assumée de la voie
  tranchée au §15 — l'arbre ne s'affichera pas comme un arbre.
* **Le palier 0 est demandé APRÈS le scénario 1.** Le carnet ne note les gains
  qu'après une rencontre, alors que sur table le palier 0 se prend avant la
  première partie. L'aide de l'entrée le dit en toutes lettres et invite à le
  prendre dès la première partie.

### ⚠️ CE QUI RESTE, ET C'EST ÉCRIT

**Les 50 cartes de talents n'ont PAS de modules.** Elles sont dans les données,
elles ont leurs images, elles se génèrent (`verifier_cartes_en_jeu` : « les 172
cartes portent ce que leur texte annonce ») et le carnet les distribue — mais
leurs capacités ne sont pas câblées. Une carte sans module se construit très
bien et reste **inerte** : c'est exactement ce que `sonde_capacites.py` sait
mesurer, et ce que sa doc appelle « un module mal placé ne provoque AUCUNE
erreur ».

C'est le prochain chantier, et le plus gros de ce qui reste : 50 modules.
Plusieurs seront courts (un `Response` qui soigne, une ressource qui se dépense),
mais certains demandent du moteur — Earth-001 change la construction de deck,
Get it Off! compte les cartes de la pile de victoire, Master Weaver glisse des
cartes rencontre sous les alliés.

### Mesure

`verifier_prefixes` OK ; `verifier_cartes_en_jeu` « les 172 cartes portent ce que
leur texte annonce » ; `verifier_appels_modules` OK ; `verifier_campagnes` OK ;
`test_cards` **4461 ok / 0 erreur** ; `autoplay` **30 parties** sur les cinq
scénarios, normal et expert, **zéro traceback**.

---

## 22. LES 50 MODULES DE TALENTS (14/08/2026) — LA CAMPAGNE EST FINIE

**Les 50 cartes des cinq arbres portent maintenant leurs capacités.** Le pack
`web_of_deceit` est complet : 172 cartes, toutes générables, toutes câblées sauf
les quatre écarts écrits ci-dessous.

### La vérification qui compte : un deck qui les contient toutes

`test_cards` ne prouve rien sur une carte joueur — il appelle `GetAbilities()`
sans jouer. Un **deck de test** (`deck/custom/spider_man_talents.json`, dans le
dossier de travail seulement) ajoute les 50 cartes au deck de départ de
Spider-Man ; le bot les pioche, les joue, et c'est là que les défauts tombent.

**Six appels plausibles mais faux, tous invisibles à `test_cards` :**

| appel écrit | ce qui existe vraiment |
|-------------|------------------------|
| `WhenCardWouldReveal` + `CancelWhenRevealedEffect` | la fenêtre est `WhenPlayerRevealCard`, avec `"WhenRevealed"` et `from_encounter=True` |
| `Worlds.GetVictoryDisplayCards` | `Worlds.VictoryDisplay(effect).Get()` |
| `AlterEgo.ChangeForm` | `ChangeToForm(Hero, effect)` |
| `Deck2.GetTopCard` | `GetTop()` |
| `CardFace.CountPrintedRes` | `printed_resource`, un compteur par couleur |
| `ReduceCostToPlayThis(fn(effect, ui))` | la fonction ne reçoit que l'effet |

### ⚠️ ET DEUX DE PLUS SUR LE LOT 1, ENCORE

**`Faces.HealAll` n'existe pas.** The Getaway (`wd012`) et le Bodyguard
(`wd028`) l'appelaient : le choix « soigner le vilain » ne soignait rien depuis
le premier jour. C'est `this.HealthUnits([...], n, effect)`.

⚠️ **`verifier_appels_modules` ne l'a PAS vu**, alors que c'est exactement ce
qu'il cherche. Sa doc annonce qu'il vérifie les attributs des noms connus
(`Faces`, `Worlds`) — sur ce cas il a laissé passer. **Seule la partie l'a
attrapé, pour la troisième fois de cette campagne.**

### Quatre cartes n'ont PAS de module, et c'est écrit

* **`wd116` Earth-001** : « You may include WEB-WARRIOR allies from any aspect
  during deckbuilding » est une règle de CONSTRUCTION DE DECK, appliquée avant la
  partie. Le moteur construit les decks depuis `deck/`, hors de portée d'une
  carte. Elle reste jouable : permanente, elle entre à la mise en place et dit au
  joueur qu'il avait le droit de mélanger les aspects.
* **`wd128`, `wd129` Radioactive Power** et **`wd156` The Power of Web** : des
  ressources nues. Leurs icônes sont dans la donnée, il n'y a rien à brancher.

Et un écart sur une cinquième : **`wd140` See the Future** ne rend que la pioche.
« Until the end of the round, play with the top card of the encounter deck
faceup » demande une fenêtre temporaire que `PlayWithTopCardOfDeckFaceup` ne sait
pas ouvrir — elle est écrite pour une carte qui reste en jeu.

### Mesure

`test_cards` **4511 ok / 0 erreur** ; `verifier_cartes_en_jeu` « les 172 cartes
portent ce que leur texte annonce » ; `verifier_appels_modules` OK ;
`verifier_prefixes` OK ; `verifier_campagnes` OK ; **16 parties avec les 50
cartes dans le deck** (Rhino, Klaw, Shocker, Kingpin) : **les 50 sont passées en
jeu, ZÉRO traceback**.

### Ce qui reste sur la campagne

1. La variante **Underling** de Vulture (14 cartes) : une deuxième façon de jouer
   Vulture, donc un sixième scénario — pas cinq cartes à ajouter.
2. Le **désistement du pilote d'`autoplay`**, qui masque les vrais défauts (§20).
3. **Jouer une partie dans un navigateur** : tout ci-dessus est mesuré par le
   moteur, personne n'a encore vu la campagne à l'écran.

---

## 23. UNDERLING, ET LE PILOTE QUI SAIT SE DÉSISTER (14/08/2026)

### Le pilote d'`autoplay` abandonne enfin une option qui échoue

Le garde-fou rendait « bloquee » dès la première répétition sans progrès : il
n'avait aucun moyen de **passer à autre chose**. Deux ajouts (commit à part) :

* **le désistement** — l'option qui vient d'échouer est écartée et la question
  reposée ; le verdict ne tombe qu'après les avoir toutes épuisées ;
* **la montée de cibles** — une plage `[1, 3]` ne veut pas dire « 1 suffit » :
  Power Drain (`02041`) exige autant de cartes que d'icônes de boost défaussées,
  un nombre que la question n'annonce pas.

**Mesure : de 3 parties bloquées sur 30 à 1 sur 21**, la dernière étant
**Tenacity (`01093`), une carte joueur OFFICIELLE** que le moteur propose alors
que le héros est déjà prêt. Aucune régression sur les scénarios officiels.

### Underling : 4 cartes neuves, pas 14 (`wd162`–`wd165`)

La lecture carte par carte tranche : **dix des quatorze sont celles du set
Vulture déjà livré**, au mot près — Feather Daggers, Vulturion ×2, The Vulture's
Plans, Sweeping Swoop, Falling ×2, Aerial Advantage, Aerial Dogfight, Highway
Robbery. Le set de rencontre `underling` les réutilise telles quelles.

**Seules quatre sont neuves** : les trois stades d'un Vulture qui porte le trait
`UNDERLING` et **RIPOSTE** au lieu d'être intouchable (2, puis 3 au stade III,
sauf si l'attaquant est AERIAL), et l'environnement **Skies Above New York**, qui
donne le trait AERIAL à un personnage ami — c'est lui qui rend le vilain jouable
au sol.

⚠️ La carte du vilain écrit « Skies **Over** New York », l'environnement s'appelle
« Skies **Above** New York ». Coquille de l'auteur, tranchée en faveur du nom de
la carte cherchée.

Un scénario `wd_vulture_underling` (et sa variante experte) le rend jouable avec
le complot de Surveillance Pigeons.

### ⚠️ CE QUI N'EST PAS VÉRIFIÉ, ET IL FAUT LE SAVOIR

**Les 8 parties d'`autoplay` sur ce scénario se bloquent toutes**, sur le Hero
Action de Skies Above New York. La cause n'est pas la carte : **le pilote ne sait
pas payer un coût en ressources porté par une carte de RENCONTRE**. Son
`payer()` lit le champ `target_payment` de la question, que le moteur ne
renseigne pas pour une action offerte par une carte que le joueur ne contrôle
pas — il envoie donc une réponse sans ressource, l'action échoue, et la question
revient.

Le même schéma existe depuis le lot 1 sur Ionic Boots (`wd010`) et Kingpin's Cane
(`wd100`) : il n'avait jamais bloqué **par chance**, le bot ne choisissant pas
toujours ces actions.

**Ce qui EST vérifié** : `test_cards` 4515 ok / 0 erreur, les 176 cartes portent
ce que leur texte annonce, `verifier_appels_modules` OK, `verifier_prefixes` OK,
et les quatre faces portent leurs capacités. **Ce qui ne l'est pas** : une partie
complète de ce scénario. C'est le pilote qu'il faudrait reprendre — le payeur,
cette fois, pas le garde-fou.

### Ce qui reste sur la campagne

**Jouer dans un navigateur.** Tout est mesuré par le moteur ; personne n'a encore
vu la campagne à l'écran. C'est aussi le point resté ouvert de Civil War.

### `verifier_scenes_campagne.py` — ce qu'aucun autre outil ne disait

Un outil neuf ferme le dernier trou de vérification. `test_cards` construit les
capacités d'une carte, `autoplay` joue une partie, `verifier_campagnes` compare
les clés du carnet aux littéraux du `campaign.py`. **Aucun ne vérifie qu'une
SCÈNE se crée** — c'est pourtant la première chose que fait le moteur quand un
joueur choisit un scénario dans le navigateur. Un `encounter_sets` mal nommé, un
`set_aside` qui pointe une carte absente, une face B de complot manquante : rien
ne lève d'erreur ailleurs, et le joueur voit un écran vide.

Il vérifie en plus que chaque option d'arbre citée par le carnet existe dans
`cards.json` : une option fantôme ne s'affiche simplement jamais.

**Mesure : les 12 scènes de la campagne se créent** (les cinq scénarios, leurs
variantes expertes, et les deux d'Underling), et **les 50 options du carnet
pointent toutes une carte qui existe**.

⚠️ Deux pièges payés en l'écrivant, et écrits dans son en-tête : le moteur garde
des fils vivants après `Initialize` (d'où `os._exit` plutôt qu'un `SystemExit`
qui ne rendrait jamais la main), et **`os._exit` ne vide pas les tampons** — sans
le `flush`, l'outil sortait en silence et son rapport se perdait.

---

## 24. CE QU'IL RESTE À FAIRE, ET PAR QUI (14/08/2026)

### 🧑 CE QU'UN HUMAIN DOIT FAIRE — rien de tout cela n'est automatisable

1. **Jouer la campagne dans un navigateur.** Tout ce qui est écrit dans cette
   fiche est mesuré par le MOTEUR : `test_cards` construit les capacités,
   `autoplay` mène des parties sans navigateur, `verifier_scenes_campagne`
   prouve que les scènes se créent. **Personne n'a encore vu une seule carte à
   l'écran.** À regarder en priorité :
   * les **images** des 176 cartes (une carte couchée ou floue ne se voit que
     là ; trois lots en ont déjà porté) ;
   * le **carnet entre deux scénarios** : le choix de palier s'affiche-t-il, et
     les 5 / 10 / 15 options sont-elles lisibles côte à côte ?
   * la **mise en place** : « Vote for Fisk », le Wingsuit distribué, les deux
     Aerial Advantage sur le vilain, Fisk Tower.

   ⚠️ Relancer le serveur d'abord : le moteur charge sa base AU DÉMARRAGE.

2. **Trancher les écarts assumés**, si l'un gêne à l'usage. Ils sont tous écrits
   avec leur raison :
   * les **cinq arbres proposés ensemble** au lieu de celui qu'on a choisi (§21) ;
   * le **palier 0 demandé après le scénario 1** au lieu d'avant (§21) ;
   * les manigances **CORROMPUES** de Kingpin : la carte du dessus du deck part
     à la défausse et un patron entre en jeu à sa place (§19) ;
   * **Negate X** qui pioche quelle que soit la fenêtre d'annulation (§17) ;
   * **Vulture** attaquable par une carte AERIAL mais pas par une attaque à
     distance (§18) ;
   * **Earth-001** et les trois autres cartes sans module (§22).

3. **Décider du sort de la boîte 120.** Le pack mélange aujourd'hui la campagne
   (176 cartes) et rien d'autre. Si les héros maison du Drive (Scarlet Spider,
   Superior Spider-Man, Venom, Spider-Man 2099 — 148 cartes et un aspect
   « Venomized ») doivent entrer un jour, c'est un choix de périmètre, pas une
   tâche.

### 🤖 CE QUE JE PEUX ENCORE FAIRE — dans l'ordre d'utilité

1. **Le payeur du pilote d'`autoplay`.** Il ne sait pas honorer un coût en
   ressources porté par une carte de RENCONTRE : ~~c'est ce qui bloque les 8
   parties du scénario Underling, et~~ ce qui dort depuis le lot 1 sur Ionic Boots
   (`wd010`) et Kingpin's Cane (`wd100`).
   ⚠️ **CORRIGÉ LE 20/08/2026 : le payeur n'était PAS la cause du blocage
   Underling.** La cause était `wd165`, voir §29. Le chantier du payeur reste
   ouvert, mais il ne débloque plus rien.
2. ~~**Élargir la couverture d'`autoplay`** à d'autres héros que Spider-Man.~~
   **FAIT** : 10 parties avec **Black Panther** sur les cinq scénarios, **zéro
   incident, zéro traceback**. Les 72 parties de la campagne ne reposent donc
   plus sur un seul deck. Reste utile un jour : un héros **AERIAL** (Falcon)
   éprouverait la clause de Vulture pour de bon, et un héros **GENIUS** l'action
   d'alter-ego de The Cure.
3. **Le blocage de Tenacity** (`01093`) : le moteur propose l'action alors que le
   héros est déjà prêt. C'est une carte OFFICIELLE — donc soit son module, soit
   le moteur. À instruire avant de toucher quoi que ce soit.

---

## 25. LES TROIS POINTS OUVERTS N'EN FAISAIENT QU'UN (14/08/2026)

Instruits ensemble, les trois derniers points se sont révélés **une seule
cause** : le pilote d'`autoplay` abandonnait la mauvaise chose.

### Ce que la mesure a montré

Une action de tour se joue en **deux temps** : le menu (« Hero Action »,
« Play ») puis le ciblage (« Select 2 cards to swap »). **C'est le ciblage qui
boucle, mais c'est le MENU qu'il faut abandonner** — désister le ciblage ne fait
que reproposer la même action au tour suivant. Le désistement du §23 gardait la
dernière option choisie, c'est-à-dire le ciblage ; il garde maintenant les
**trois derniers choix** et les écarte tous.

**Mesure, avec Falcon (héros AERIAL, jamais essayé jusque-là) :**

| | avant | après |
|---|---|---|
| Falcon vs Vulture / The Lizard, 6 parties | **7 bloquées** | **0** |

⚠️ Et le blocage n'était pas de notre contenu : **Battlefield Awareness
(`53010`)**, carte joueur OFFICIELLE de Falcon, avec sa question « Select 2 cards
to swap ». Comme Tenacity, comme Power Drain : **le pilote, pas les cartes.**

### Ce que la sonde a établi sur Underling, et qui ferme une fausse piste

Le §23 accusait le **payeur** du pilote. C'est FAUX, et une sonde qui capture la
question telle que le moteur la pose le montre :

```
Hero_Action_1 … "target_payment": {"0": {"cost": "Y", "payment": [{"10": "Y"}, {"11": "Y"}]}}
```

Le champ **est** renseigné, et `payer()` sait le lire. La piste suivante est
ailleurs : **l'empreinte de progrès du détecteur de boucle ne voit pas un TRAIT
accordé**. Skies Above New York donne AERIAL à un personnage — ni les PV, ni la
menace, ni la taille de main, ni le round ne bougent. Le détecteur conclut à une
boucle alors que l'action a peut-être réussi.

**À reprendre par là**, et pas par le payeur : ajouter les traits accordés (ou un
compteur d'effets résolus) à l'empreinte de `progres`.

### État des blocages, mesuré sur 15 parties

| scénario | bloquées | cause |
|---|---|---|
| Rhino, Klaw, Shocker | 0 | — |
| Kingpin | 1 / 3 | **Tenacity (`01093`)**, carte officielle |
| Vulture (Underling) | 3 / 3 | l'empreinte de progrès, ci-dessus |


### L'empreinte de progrès voit maintenant les traits — et ce n'était pas la cause

La piste du §25 était juste sur le fond : l'empreinte ne photographiait que les
PV, la menace, la main et le round. Une action peut **réussir** sans toucher
aucun des quatre — « un personnage ami gagne le trait AERIAL » n'en bouge pas un.
Elle photographie désormais aussi **les traits des personnages amis**, la
**taille de la défausse** et le **nombre de cartes en jeu**.

**Mesure : aucune régression** (Falcon, 6 parties, 0 bloquée), **mais Underling
bloque toujours 3 fois sur 3.** Ce n'était donc pas la cause.

### ⚠️ CE QUE LE JOURNAL DIT VRAIMENT, ET QUI CHANGE LA PISTE

Dans la partie bloquée, **une carte OFFICIELLE échoue au même moment** :

```
<E> (16) [(13,01005) Swinging Web Kick] (Hero Action,Play,attack) [01005] WhenPlayerInTurn failed
<E> (67) [(51,wd165) Skies Above New York] (Hero Action) [wd165] WhenPlayerInTurn failed
```

**Swinging Web Kick** est une carte du deck de départ de Spider-Man. Deux actions
sans rapport échouent coup sur coup, au round 1 : ce n'est pas la carte de la
campagne, c'est **l'état du joueur** à ce moment-là (héros épuisé, ou une
restriction posée par le scénario) qui rend toute action impossible.

**La prochaine piste est là** : instrumenter ce que le moteur refuse — pourquoi
`WhenPlayerInTurn` échoue alors que l'option est offerte — plutôt que de
soupçonner encore une carte. Trois hypothèses ont été éliminées par la mesure :
le payeur (§25), l'empreinte de progrès (ici), et le désistement (§25, qui a bien
réglé les 7 blocages de Falcon).

---

## 26. LA RIPOSTE DU VULTURE SOUS-FIFRE ÉTAIT INVERSÉE (14/08/2026)

La carte dit :

> **AERIAL. UNDERLING.**
> **Setup**: Find the Skies Over New York environment and reveal it.
> **Vulture gains retaliate 2 during the player phase unless the attacker or
> attack has the AERIAL trait.** *(retaliate 3 au stade III)*

Elle riposte **sauf** contre les aériens : voler est ce qui protège.

**Le premier jet faisait exactement l'inverse.** Il lisait « une carte AERIAL
est-elle en jeu ? » et donnait la riposte quand il y en avait une :

```python
def pas_aerien(effect):
    return not Worlds.FindCardOnField(effect, CardFinder(trait="AERIAL", card_type=Friend))
return AbilityFactory.ThisGainKeyword(lambda effect, ui: 0 if pas_aerien(effect) else 1, retaliate=valeur)
```

Deux erreurs empilées : **le sens** (riposte quand il faudrait ne pas riposter) et
**la portée** (une carte AERIAL quelconque en jeu, là où le texte parle de
**l'attaquant**).

⚠️ **Ce n'est pas le mot-clé `Retaliate`, et ça ne pouvait pas l'être** : la
riposte dépend de QUI FRAPPE, un renseignement que le moteur ne connaît qu'au
moment de l'attaque. Un mot-clé constant ne sait pas l'exprimer. C'est désormais
une réponse à l'attaque (`AfterUnitBeAttacked`) qui vérifie le trait de
l'attaquant **et** de la carte qui porte l'attaque, et qui ne mord que pendant la
phase du joueur.

**Aucun outil n'aurait trouvé ça** : la carte se génère, ses appels existent, son
texte correspond à la donnée, et une partie ne dit pas qu'une riposte s'est
déclenchée au mauvais moment. **C'est une lecture du texte contre le code qui l'a
sortie** — la même méthode qui avait donné les six réimpressions du lot 4.

### La revue des 21 cartes « pareilles » — un second défaut, même famille

La riposte inversée appelait une question : **combien d'autres cartes du pack ont
une clause conditionnelle mal rendue ?** Les 176 cartes ont été passées au crible
sur les mots qui trahissent une condition (`unless`, `otherwise`, `without`,
`while`, `instead of`, `If you cannot`) : **21 cartes**, relues une à une contre
leur module.

**Dix-neuf sont justes.** `wd008` (Vulture de Shocker : ne défausse pas si
l'identité est AERIAL), `wd041` (Grounded), `wd059`, `wd061`, `wd074`–`wd076`
(le « cannot be attacked unless AERIAL » du scénario #4, dans le bon sens),
`wd098`, `wd107`, `wd114`, `wd150`…

**Une était fausse : `wd027` « He's Mine! »** — et c'est **le même défaut de
portée** que la riposte.

> **When Revealed**: If the **Bodyguard ATTACHMENT** is not in play, discard each
> non-ELITE minion engaged with you… Otherwise, this card gains surge.

Le module cherchait `name="Bodyguard"` **sans filtrer le type**. Or **deux cartes
de ce pack portent ce nom** : l'attachement `wd026` et le sbire `wd028`. Quand le
SBIRE était en jeu, la traîtrise croyait l'attachement présent et **déferlait au
lieu d'agir** — elle ne balayait pas les sbires et ne cherchait pas
l'attachement.

Le pire : la ligne SUIVANTE du même module filtre bien
(`ChercherEtReveler(..., card_type=Attachment)`). L'incohérence était visible à
l'œil, invisible à tous les outils.

`Kingpin's Suit` a reçu le même filtre par précaution — un seul porteur
aujourd'hui, mais le pack a déjà prouvé qu'il aime les homonymes (« Electro » en
compte cinq, « Vulture » trois).

### Mesure après les deux corrections

**20 parties sur les cinq scénarios, normal et expert : ZÉRO bloquée, ZÉRO
traceback.** C'est la première fois que la campagne entière passe sans un seul
incident.

---

## 27. LA REVUE DES 50 CARTES DE TALENTS — TROIS DÉFAUTS DE PLUS (14/08/2026)

Même méthode que le §26, appliquée aux `wd112`–`wd161` : les textes passés au
crible sur les mots qui portent une condition ou une portée, puis relus contre
leur module. En prime, une comparaison automatique des **nombres** du texte et de
ceux du code (les cinq écarts relevés étaient tous des valeurs de `desc` —
compteurs d'utilisation, Victory — donc justes).

**Quarante-sept sur cinquante sont justes.** Trois ne l'étaient pas, et **aucune
n'aurait été trouvée par un outil** : les trois se génèrent, leurs appels
existent, leur texte correspond à la donnée.

### `wd121` Master Weaver — portée trop ÉTROITE

> **Each** WEB-WARRIOR ally gets +1 hit point for each boost icon tucked under them.

Le premier jet avait mis `control_by="You"`. **La différence est dans le texte** :
Web-Warriors (`wd117`) écrit « each of **your** WEB-WARRIOR allies », Master
Weaver écrit « **each** WEB-WARRIOR ally ». Le Tisserand tisse pour toute la
table, pas seulement pour son porteur.

### `wd133` Spider-Sense — portée trop LARGE

> **Hero Interrupt**: When the villain initiates an attack **against you**, draw 1 card.

`WhenUnitMakeAttack` ne porte pas la clause « contre vous » ; la carte sonnait
aussi quand le vilain frappait un autre joueur. Sans effet en solo, **faux dès
qu'on est deux**. C'est `WhenUnitWouldAttack(..., against_player="You")`.

### `wd145` Flee the Scene — condition trop RESTRICTIVE

> **Response**: After your hero thwarts and **removes threat** from a scheme…

Le premier jet appelait `AfterUnitThwartAndRemoveLastThreat` : la carte ne se
déclenchait qu'en **achevant** une manigance, là où le texte se contente d'un
pion retiré. C'est `AfterUnitThwartScheme(..., remove_threat=True)`.

### Ce que ces trois-là disent de la méthode

Les deux défauts du §26 étaient des portées trop larges ; ceux-ci ajoutent une
portée trop étroite et une condition trop stricte. **Le point commun n'est pas le
sens de l'erreur, c'est la source** : à chaque fois, un mot du texte anglais —
`your`, `against you`, `the last` — que le module n'a pas rendu.

**Mesure** : `test_cards` 4515 ok / 0 erreur, `verifier_appels_modules` OK, les
trois cartes portent leurs capacités, et **9 parties avec les 50 talents dans le
deck** (Rhino, Shocker, Kingpin) — zéro incident, zéro traceback.

---

## 28. LA REVUE TEXTE-CONTRE-CODE : CE QUI EST FAIT, CE QUI RESTE

> ✅ **CLOS LE 20/08/2026.** Les 126 cartes annoncées ci-dessous ont été
> passées au crible avec la liste de mots élargie. Résultats au **§29**.

Cinq défauts trouvés en deux passes (§26, §27), **tous invisibles aux outils** :
les cartes se génèrent, leurs appels existent, leur texte correspond à la donnée.
Assez pour en faire une **méthode**, et pour dire précisément où elle s'est
arrêtée.

### Les cinq défauts, et leur source commune

| carte | le mot du texte | ce que le module faisait |
|-------|-----------------|--------------------------|
| `wd162`–`wd164` Vulture sous-fifre | « **unless** the attacker … AERIAL » | ripostait **quand** il fallait ne pas riposter |
| `wd027` "He's Mine!" | « the Bodyguard **ATTACHMENT** » | confondait avec le **sbire** du même nom |
| `wd121` Master Weaver | « **each** WEB-WARRIOR ally » | limité à **ses** alliés (`control_by="You"`) |
| `wd133` Spider-Sense | « an attack **against you** » | sonnait pour **tous** les joueurs |
| `wd145` Flee the Scene | « removes **threat** » | exigeait le **dernier** pion |

**La source est toujours la même** : un mot du texte anglais — `unless`,
`ATTACHMENT`, `each`, `against you`, `the last` — que le module n'a pas rendu.
Le sens de l'erreur, lui, varie : deux portées trop larges, une trop étroite, une
condition inversée, une trop stricte. **Ne pas chercher un motif dans le sens,
chercher le mot.**

### ⚠️ CE QUI RESTE À PASSER AU CRIBLE — 126 cartes

Les deux passes ont couvert :

* **§26** : les cartes du pack ENTIER portant un mot de condition
  (`unless`, `otherwise`, `without`, `while`, `instead of`, `If you cannot`) —
  **21 cartes**, modulaires compris ;
* **§27** : les **50 cartes de talents**, avec en plus une comparaison
  automatique des NOMBRES du texte et du code.

**Ce qui n'a PAS été fait** : la même revue, avec la liste de mots ÉLARGIE
(`another`, `each`, `for each`, `equal to`, `against you`, `your`) et la
comparaison des nombres, sur les **126 cartes hors talents** — les cinq sets de
vilain, les modulaires (Crime Wave, Power Drain II, Bodyguard, City Sewers,
Kraven, Underling) et la mise en place. Le compte exact :

* **80** portent une clause ou une portée à vérifier ;
* **46** n'en portent pas et peuvent être survolées.

⚠️ Le §26 n'en avait vu que 21 : sa liste de mots ne contenait ni `each`, ni
`for each`, ni `against you`, ni `your` — c'est-à-dire **précisément les mots qui
ont livré les trois défauts du §27**. La revue des modulaires est donc à refaire
avec la liste complète, pas seulement à compléter.

### La méthode, pour qui reprend

1. Extraire le texte de la carte depuis `cards.json` (pas depuis l'image : c'est
   la donnée que le moteur lit).
2. Relire le module **à côté**, mot à mot, en cherchant : le **sens** de la
   condition, la **portée** (`your` / `each` / `another` / `you control`), le
   **timing** (`when` / `after` / `instead`), et le **type** visé quand un nom est
   partagé (« Electro » est porté par cinq cartes de ce pack, « Vulture » par
   trois, « Bodyguard » par deux).
3. Comparer les nombres du texte à ceux du code — en sachant que les valeurs de
   `desc` (Uses, Victory, Boost) n'apparaissent pas dans le module.

---

## 29. LA REVUE DES 126 CARTES HORS TALENTS EST FAITE (20/08/2026)

Le §28 la demandait **à refaire, pas à compléter**. C'est ce qui a été fait :
les 126 cartes relues avec la liste de mots élargie, plus trois filets
automatiques. **Huit écarts, sept corrigés, un écrit.** Quatre commits sur
`master`, de `e02f021` à `8bec94a`.

### Le crible, et ce qu'il a couvert

Liste de mots complète : `unless`, `otherwise`, `without`, `while`, `instead of`,
`If you cannot`, plus les six qui manquaient au §26 — `another`, `each`,
`for each`, `equal to`, `against you`, `your` — et `you control`, `only`,
`up to`, `may`, `cannot`, `choose`, `per`. **94 des 126 cartes** en portent au
moins un ; les 32 autres sont des cartes à mots-clés purs, dont la valeur vit
dans le `desc`.

Chaque carte relue contre son module, plus trois passes automatiques :

1. **Les NOMBRES du texte contre ceux du code**, commentaires exclus. Trois
   signalements, dont deux faux positifs (les gobelins experts, dont le « 2 »
   vit dans le helper partagé `GobelinExpert()`). Le troisième était réel et
   c'est `wd077b`.
2. **Le DÉCLENCHEUR contre la fenêtre annoncée** : un texte qui dit
   `Response: After …` rendu par une fabrique qui n'a pas de fenêtre, et
   `attacks` rendu par la variante `AndDamage` (ou l'inverse). Deux réels
   (`wd089`, `wd006`), un faux positif (`wd058`, dont la clause dit bien
   « deals damage »).
3. **Les NOMS PARTAGÉS sans filtre de type**, le piège de « He's Mine! ». Trois
   signalements, deux volontaires et documentés (`wd040`, `wd043`, où « Electro »
   doit couvrir le vilain ET les sbires), un mineur (`wd003a`).

### Les huit écarts

| carte | le mot du texte | ce que le module faisait |
|-------|-----------------|--------------------------|
| `wd090` Wingsuit V2 | « Hero Action: … gains the AERIAL trait » | **aucun module**, capacité inerte |
| `wd165` Skies Above New York | « an AERIAL card **you control** » | le coût pouvait épuiser **le vilain** |
| `wd089` Aviator Goggles | « **Response**: After you attack and damage » | action de tour libre, sans déclencheur |
| `wd005` Vibro-Shock Gauntlets | « **and remove** a stunned or confused status card » | la moitié du coût absente |
| `wd028` Bodyguard (sbire) | « **If you cannot** » | testait « pas de vilain », cas impossible |
| `wd006` Sandman | « **attacks** or engages you » | exigeait des dégâts |
| `wd056b` The Cure | « once per round **per player** » | limite globale |
| `wd077b` Surveillance Pigeons | second Interrupt | absent, **écart écrit** |

**`wd090` était le plus grave**, et c'est le seul de toute la campagne à n'avoir
eu *aucun* module. `NePeutEtreAttaqueQueParLesAeriens` n'accepte que le trait
AERIAL, et le commentaire du helper dit lui-même « le Wingsuit distribué à la
mise en place donne justement ce trait ». Sans module, aucun héros non-AERIAL ne
pouvait frapper Vulture.

### ✅ LE BLOCAGE UNDERLING, ET POURQUOI LES TROIS HYPOTHÈSES ÉTAIENT À CÔTÉ

Le §25 avait éliminé par la mesure le payeur du pilote, l'empreinte de progrès et
le désistement. La piste retenue — instrumenter l'état du joueur, puisque
Swinging Web Kick (`01005`) échouait au même moment — n'était pas la bonne non
plus. **Le journal d'autoplay écrivait la réponse en clair** :

```
<E> (67) [(51,wd165) Skies Above New York] (Hero Action) [wd165] WhenPlayerInTurn failed
```

L'action donne AERIAL à un personnage amical. Dès que l'allié meurt et que le
héros a été servi une fois, la **seule cible légale l'a déjà** : l'action ne
change rien, le moteur la repropose, le pilote la reprend, la partie tourne en
rond. C'est exactement le défaut contre lequel `a_une_carte_aerienne` protégeait
déjà — l'auteur avait gardé le **coût**, pas la **cible**.

Mesure à graines identiques : **3 parties bloquées sur 3 avant, 0 sur 6 après**,
et Underling gagne même une partie en expert.

### ⚠️ LA LEÇON, ET ELLE PROLONGE CELLE DU 14/08

**Deux des huit écarts n'étaient pas trouvables à la lecture** : la portée du coût
de `wd165` et la cause du blocage. Les deux sont sortis du journal d'autoplay
**lu ligne à ligne**, et il n'y avait **aucune traceback** dedans. Le grep des
tracebacks reste nécessaire, il n'est pas suffisant : il faut aussi lire ce que la
partie a réellement fait. `[[Vulture]] exhausted ([Wingsuit V2])` est une ligne
parfaitement normale à l'œil d'un outil, et c'est un cadeau au joueur.

### `wd077b` : la clause non rendue, et ce qu'elle coûterait

> « Interrupt: When you would discard a random card from your hand, you may place
> 2 pigeon counters here instead. »

Le moteur n'a **aucune fenêtre sur une défausse aléatoire** :
`DiscardRandomHandCards` (player_action.py) tire les cartes puis appelle
`Faces.DiscardAll`, qui n'émet qu'un `WhenCardWouldDiscard` par carte, identique
à celui d'une défausse **choisie**. S'y accrocher ferait esquiver aussi les
défausses volontaires — un coût de carte, la limite de main — bien plus large que
le texte.

Le rendre demande un message moteur neuf, sur le modèle de
`WhenPlayerWouldBeDealtEncounterCard` (sender_player.py:364) : une classe
`CanBeInstead`, une fabrique dans `factory/player.py`, et l'appel dans
`DiscardRandomHandCards`. **C'est le moteur partagé, que 4516 cartes
traversent** : décision à prendre, pas tâche à faire.

Conséquence en jeu, puisqu'elle n'est pas nulle : le scénario est plus dur que son
texte. Web of Deceit défausse au hasard souvent (`wd008`, `wd078`, `wd081`,
`wd068`), et le joueur n'a pas la soupape que la carte lui promet.

### Les huit approximations relevées et NON corrigées

Aucune n'est un bug franc ; toutes sont écrites ici pour qu'on n'ait pas à les
retrouver.

* **`wd001b` et `wd014`** — « Deal 1 damage to **each hero** » est rendu par
  `Players.ForEachPlayer` + `GetIdentity()`, qui frappe aussi les joueurs en
  alter-ego. Le moteur sait distinguer (`player.IsHero()`), et `wd079` le fait
  déjà pour « Stun your hero ». Deux occurrences, même cause.
* **`wd037`** — « discard an **equal number** of cards » est lu comme le nombre
  d'icônes de boost de la traîtrise trouvée. L'autre lecture, plus naturelle en
  anglais, est le nombre de cartes défaussées. À trancher.
* **`wd105`** — « After **a card you control** defeats a side scheme » est rendu
  par `"YouControlCharacter"` : un événement qui déjoue ne compte pas.
* **`wd003a`** — cherche `name="Rhino"` sans `card_type=Minion`, alors que le
  texte dit « the Rhino **minion** ». Sans risque réel (un vilain n'est pas dans
  le deck rencontre), mais c'est le motif exact de « He's Mine! ».
* **`wd026`** — « shuffle it into the encounter deck **from the encounter discard
  pile** » est rendu par un Forced Interrupt qui mélange le sbire depuis le jeu,
  avant sa défaite.
* **`wd029`** — « (Limit once per minion per campaign.) » n'est pas appliqué.
* **`wd022`** — le texte dit « **that** minion », le module met en jeu chaque
  Electro défaussé parmi les 7. Le set en compte deux.
* **`wd025`** — « +1 hit point for each [energy] **resource** attached » compte
  les CARTES portant un [energy] imprimé, pas les icônes.

### Mesures

`test_cards` **4516 ok / 0 erreur** (4515 avant, le +1 est `wd090`) ;
`verifier_appels_modules` OK ; `verifier_cartes_en_jeu` « les 176 cartes portent
ce que leur texte annonce » ; `verifier_prefixes` OK ; `verifier_campagnes` OK ;
`verifier_scenes_campagne` **12 scènes, 50 options** ; `sonde_capacites` : les
sept cartes touchées portent leurs capacités ; **36 parties d'autoplay** sur les
six scénarios, normal et expert, **0 traceback au grep**.

Une seule partie bloquée sur 36, et c'est **Tenacity (`01093`)**, carte joueur
OFFICIELLE et point ouvert déjà connu — hors de ce pack.

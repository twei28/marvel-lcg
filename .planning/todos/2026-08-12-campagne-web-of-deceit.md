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

**Le mode campagne n'a plus de dette connue** (12/8/2026, `docs/CAMPAGNES.md`).
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

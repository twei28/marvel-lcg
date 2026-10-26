# Hellfire Hunt (Dipsome) : dossier de préparation du portage (26/10/2026)

Lecture seule : aucun fichier du jeu n'a été touché. Source : `Hellfire Hunt Campaign-20261025T195712Z-1-001.zip` (294 fichiers, extrait dans le scratchpad).
Complète `2026-10-26-audit-campagnes-fanmade.md` §2, qui n'avait lu que l'intro, les mots-clés, le carnet et White Queen.

## 0. Ce qui a été lu, et ce qui ne l'a pas été

**Lu à l'écran** : les 24 pages du livret (`ruleBookPages/file_compressed.pdf`, une image de 5000 × 5000 par page, **sans texte extractible** : `pdftotext` renvoie 24 caractères) ; les cartes de tous les dossiers (planches de 4 cartes) pour les 5 scénarios, la carte de campagne, les alliés recrutés, la side scheme « Potential Ally », les cartes d'aspect de campagne et les deux héros. Pour chaque scénario : mise en place, victoire, mécaniques propres, vilain à ses 2 ou 3 stades.

**NON lu** : les neuf modules (65 cartes) : leurs planches ont été générées mais **leurs images ne se sont pas affichées** pendant la lecture ; le tableau du §4 ne repose donc que sur le livret (quels scénarios les utilisent) et sur ce que d'autres cartes en disent (ex. White Queen cite le trait ILLUSION, Shaw les sbires ELITE HELLFIRE). **Tout ce qui est écrit sur le contenu des modules est une déduction, à vérifier carte par carte au portage.** Il en va de même des 15 cartes d'aspect de campagne et des 16 alliés (§2.3 et §6) : comptées, **pas lues**. Les ~234 cartes de rencontre et les 24 cartes de vilain ne sont pas transcrites : c'est le travail de `PROCESSUS-CARTE.md` carte par carte, pas d'une lecture de préparation.

**Illisible ou absent** :
- **FAQ (p. 22) : deux questions sur trois sont des réponses de l'auteur** (White Queen, Black King, Cassandra Nova) ; **Torn et la FAQ des deux héros (p. 23) sont « Still thinking »** : pas de réponse.
- **Le texte français de la campagne n'existe pas** : tout est en anglais.
- Les pages 9, 11, 13, 15, 17 sont des **illustrations de l'auteur** (dessins) ; 19 est une planche de bande dessinée ; 1 est la couverture ; 21 les crédits. Il n'y a **aucun texte de règle** dans ces pages.
- Pas de decklist de campagne autre que les deux decks de départ (p. 20, lue) : voir §6.
- Le carnet imprimé (p. 24, « Campaign Log ») est une image : champs lus, pas de fichier réutilisable.

## 1. Surprises (à lire d'abord)

1. **La campagne doit être gagnée dans l'ordre 1 → 5, avec la MÊME identité** (p. 5). Défaite : on recommence le scénario sans pénalité. Aucun embranchement. C'est ce que fait déjà le mode campagne du jeu.
2. **Le carnet a très peu de champs** : l'identité de chaque joueur ; la liste des **alliés « Recruited »** gagnés (jusqu'à 16) ; deux cases « défait » (Emma Frost's Redemption, Cryptic Threatening Message) ; **en expert, les PV restants** de chaque identité. Rien d'autre (pas de monnaie, pas d'enquête). La complexité est dans la MISE EN PLACE, pas dans le carnet.
3. **Le vilain de Torn n'est pas Sebastian Shaw ni un sbire** : c'est **Emma Frost, un vilain à deux faces (A et B) avec PV infinis sur la face retournée** (voir §3 Torn). Elle ne se bat pas vraiment : on retire de la menace et on la retourne.
4. **Cassandra Nova (scénario 5) change la règle de défaite en expert** : si les joueurs perdent, ils **perdent la CAMPAGNE** (« Cassandra Nova eliminates all mutants »). Le jeu a déjà un précédent (aoa) : voir §5.
5. **Les cartes de campagne ne comptent pas dans la taille du deck** et « ne peuvent être incluses dans aucun deck sauf si la campagne les ajoute » (p. 5). Il faut donc une règle de deck-building propre aux cartes « Basic / Campaign » (cartes n° 263 à 288).
6. **Le livret cite « Skrull Menace »** : ses cartes d'alliés recrutés et le lieu « Xavier's Institute » sont repris de cette campagne, **déjà dans le jeu** (`data/campagnes/skrull_menace.json`). Le moteur sait donc déjà ce qu'est une zone de coopération.
7. **L'audit précédent annonçait « 3 extensions moteur » ; il en faut davantage** : voir §7 (formes du vilain, deux decks annexes, PV persistants, mais aussi : vilain à PV infinis, Hellfire deck avec défausse propre, environnements « jour / nuit », compteurs « Cassandra Controls », « Absorb »).

## 2. La campagne (règles communes)

### 2.1 Enchaînement
Cinq scénarios, **dans l'ordre**, mêmes identités (on peut changer d'aspect et de deck entre deux). Défaite = on rejoue sans pénalité. Victoire du scénario 5 = victoire de campagne (le scénario 5 n'a pas de « suite »).

### 2.2 Carnet de campagne (pages 18-19 de l'audit ; p. 24 du livret, « Campaign Log »)
| Champ | Quand | Détail |
|---|---|---|
| Identité de chaque joueur (×4) | Setup du n°1 | non modifiable pendant la campagne |
| PV restants de chaque joueur (×4) | **expert seulement**, victoire de chaque scénario | si > PV de base, on note les PV de base |
| **Recruited Allies** par scénario (cases 1 à 4, 16 cartes) | victoire de chaque scénario | nom de chaque allié ajouté ; « gagne le trait Recruited après le scénario 2 » |
| **Emma Frost's Redemption : Defeated** (case) | victoire des n°2 et 3 | la side scheme a-t-elle été défaite ? |
| **Cryptic Threatening Message : Defeated** (case) | victoire du n°3 | idem |

### 2.3 Cartes de campagne (dossier `Campaign Card/`)
| Dossier | Cartes | Contenu |
|---|---|---|
| `Campaign/` | **8** (1 à 7 + `xav`) | **Xavier's Institute** (environnement, `xav`) ; les side schemes de campagne (Cerebro Insights 180, Emma Frost's Redemption 181, Cryptic Threatening Message 182, Psychic Minefield 183, Rally the Survivors 184, Tactical Help 185, Enemy of Enemy 186) |
| `allies/` | **16** | alliés **Recruited** (n° 200 à 215 : Armor, Sage, Dust, Mercury, Emma Frost 212, Glob, etc.) |
| `ally side scheme/` | **12** | side schemes **Potential Ally** (n° 188 à 199) : en gagner une recrute l'allié correspondant |
| Cartes d'aspect de campagne | **15** | `Hero/Aspect Cards`, n° 013 à 027 (Basic / Campaign, 263-288) |

Total « cartes de campagne » : 8 + 16 + 12 + 15 = **51**.

### 2.4 Mécaniques de campagne (nouveautés)
1. **Xavier's Institute** (environnement) : « Forced Response : après qu'un allié **Recruited** est défaussé, mettez-le dans la défausse **Recruited Mutants** à la place. Action : défaussez une carte de la main → piochez une carte du deck **Recruited Mutants** (max une fois par phase et par joueur). »
2. **Potential Ally deck** : 12 side schemes « Potential Ally » mélangés à part ; au setup de chaque scénario, on en mélange **1 par joueur** dans le deck de rencontre ; en gagner une (la **défaire**) **invite l'allié** (« When Defeated : le joueur cherche l'allié dans la zone mise de côté, le met en jeu sous son contrôle »). À la victoire : on retire de la campagne celles qui sont dans la zone de victoire et on remélange le reste.
3. **Recruited Mutants deck** : paquet vide au début, posé **à côté de Xavier's Institute** (scénarios 1 à 4) ou **à côté de la side scheme Rally the Survivors** (scénario 5). On y mélange les alliés **Recruited** gagnés ; se vide, se remélange avec sa défausse.
4. **PV persistants en expert** : voir §1.

## 3. Les cinq scénarios

Notation : « (I/II/III) » = stades du vilain ; (III) remplace (I) en **expert** pour les scénarios 1 à 5 (même schéma partout : on retire le stade I et on ajoute le III).

### Scénario 1 : White Queen (Emma Frost) : 32 cartes
**Vilain** : White Queen **deux faces (A = PSIONIC, B = DIAMOND)**, 2 stades + stade 3A en expert (`WQ A1/B1` 12 PV, `A2/B2` 15 PV, A3 expert).
- A1 : SCH 2, ATK 1★. « Forced Response : après qu'elle t'attaque, défaussez la carte du dessus du deck de rencontre ; si elle a le trait **ILLUSION**, révélez-la. **Flip White Queen.** »
- B1 (DIAMOND) : SCH 1★, ATK 2. « Forced Response : après qu'elle machine, flip. Forced Interrupt : quand elle subit des dégâts d'une attaque, défaussez la carte du dessus ; **réduisez les dégâts du nombre d'icônes de boost défaussées**. »
- Stades 2 : A2 ATK 2★ / B2 ATK 3, **Steady, Retaliate 1** (B2).
**Règle clé (livret p. 8)** : « Changer de forme n'est PAS vaincre le vilain : **on ne remet pas ses PV à zéro et on ne défausse pas ses attachements**. Quand un stade est vaincu, **le stade suivant est révélé dans la MÊME forme que celle qu'elle vient de vaincre**. » En stade 3A : « **incite 1** à chaque retour en forme PSIONIC. »
**Mise en place** : complots Infiltrating the Mansion → Locating the Cerebro → Hellfire Ascendant. Deck de rencontre : White Queen + Perfection + Hellfire Conclave + **Psionic Delusion** + Standard (CORRIGÉ le 26/10 : le livret p. 8 et le complot 1A citent Psionic Delusion, pas Mind Control ; Hellfire Conclave et Psionic Delusion sont les deux modulaires retirables). Setup de campagne : enregistrer l'identité ; mélanger les 12 Potential Ally, en mélanger 1 par joueur dans le deck de rencontre ; mettre de côté les 16 alliés Recruited ; révéler Cerebro Insights (180) ; mettre Xavier's Institute (187) en jeu et créer le deck Recruited Mutants (vide).
**FAQ de l'auteur** : si White Queen machine en DIAMOND et que ça avance le complot principal, « When Completed » la retourne en PSIONIC, elle ne se retourne **pas** une deuxième fois ; cas rare avec la carte de boost Crystalline Adaptation : boost → PSIONIC, menace posée, « When Completed » → DIAMOND, réponse au machinage → PSIONIC.
**Victoire (campagne)** : retirer les Potential Ally de la zone de victoire de la campagne ; remélanger celles du deck de rencontre et de la défausse dans le deck Potential Ally ; mélanger chaque allié Recruited en jeu dans le deck Recruited Mutants ; les noter au carnet. Expert : noter les PV restants.

### Scénario 2 : Black King (Sebastian Shaw) : 30 cartes
**Vilain** : Sebastian Shaw (I) 13 PV, (II) 15 PV, **(III) 17 PV en expert** ; SCH 2 → 3, ATK 0★ → 1★. **« Absorb » : après qu'il subit des dégâts d'une attaque, placez sur lui autant de compteurs d'énergie que de dégâts ; quand il attaque, retirez jusqu'à 3 compteurs, +1 ATK par compteur retiré.** (III) : +1 compteur supplémentaire.
**Complots** : *Jailbreak at the Hellfire Club* (1A/1B : menace inamovible ; « Forced Interrupt : quand Shaw machinerait contre toi, tu reçois 1 carte de rencontre face cachée à la place ») → *Operation Hellfire Ascendant* (2A/2B : 13 menace ; **Hero Action : épuiser un allié CAPTIVE → retirer 2 compteurs d'énergie à Shaw**, une fois par round et par joueur).
**Mise en place** : retirer tous les sbires nommés Sebastian Shaw ; **mettre de côté chaque allié CAPTIVE** ; révéler la side scheme *Captured by Hellfire!* (n°6 : « place 1 par joueur d'alliés captifs face cachée sous cette carte ; **When Defeated** : le joueur qui la défait prend au hasard une carte sous elle et l'ajoute à sa main ; s'il en reste, place 5 menace ici ; sinon, avance au complot 2A et ajoute la carte à la zone de victoire »). **Attacher « Black King » à Sebastian Shaw** (attachement : titre, **Permanent**, « King's Tactic »).
**Le Black King** : *« Forced Interrupt : quand l'Absorb de Shaw se déclenche alors qu'il porte des compteurs d'énergie, retirez tous les compteurs et placez autant de menace sur le complot principal »* ; face B : « And What is Theirs… Is Mine » : Shaw gagne **stalwart tant qu'il a plus de 5 compteurs d'énergie** ; *Max 1/joueur/round*. **FAQ** : « Max 1 » = la première occurrence uniquement ; les compteurs suivants restent sur Shaw ; la limite ne compte pas la face Black King avant le retournement.
**Campagne** : on doit « mélanger chaque CAPTIVE et RECRUITED des decks et défausses de joueurs dans le deck Recruited Mutants » ; **les captifs libérés deviennent « Recruited »** pour le reste de la campagne ; noter « Emma Frost's Redemption » si elle a été défaite.
**Alliés CAPTIVE** (cartes 8 à 13 du dossier) : *Dust*, *Mercury*, etc. : « *Interrupt* : quand Dust attaque, **résolvez l'attaque contre le vilain et chaque sbire engagé avec vous** » ; *Mercury* : Toughness.

### Scénario 3 : Black Queen (Selene) : 26 cartes
**Vilain** : Selene (I) 12 PV, (II) 14 PV, **(III) 17 PV en expert** ; ATK 1 → 2 → 3, **Toughness (II, III), Steady (III)**. « Forced Response : après qu'elle attaque, **soignez-la d'autant de dégâts non excédentaires que le joueur défenseur en a subis** (vol de vie). »
**Complots** : *Throne of the Hellfire Club* → *The Power of the Darkhold* → *Ascending to Godhood*.
**Mise en place** : **mettre « Under the Moonlight » en jeu** (environnement), mettre le module Darkhold de côté, **mélanger *Darkhold Dwarf* (mis de côté) dans le deck de rencontre**. Campagne : mélanger 1 Potential Ally par joueur ; Xavier's Institute + deck Recruited Mutants (alliés notés) ; **si « Emma Frost's Redemption » n'est pas cochée, la révéler ; sinon mélanger Emma Frost (212) dans le deck Recruited Mutants et révéler « Cryptic Threatening Message » (182)**.
**Mécanique propre : « Time Environment »** : **deux environnements « Under the Moonlight » (nuit) et « Beneath the Sun » (jour)** : « chaque action que tu fais **avance le temps** » : le joueur choisit d'opérer de jour (bonus mais ennemi plus faible) ou de nuit (ennemi plus fort, sans les bénéfices du soleil). Le livret n'en donne pas la règle chiffrée sur la page : elle est sur les deux cartes d'environnement (à transcrire carte par carte).
**Victoire** : mêmes étapes ; noter si Emma Frost's Redemption **et** Cryptic Threatening Message ont été défaites.

### Scénario 4 : Torn (Emma Frost, piégée) : 19 cartes
**Vilain** : **Emma Frost, 4 faces : A1/B1 (7 et 8 PV) face « active » ; A2/B2 face « retournée » à PV « ∞ »**. A1 : « ★ Forced Response : après qu'elle active, défaussez 1 carte du deck de rencontre ; **si PSIONIC, placez 1 menace sur chaque complot** » ; **« Forced Interrupt : quand Emma serait vaincue, retirez 5 menace de chaque complot en jeu et retournez cette carte à la place »**. A2 (retournée) : « Forced Interrupt : quand elle activerait, défaussez 2 cartes du deck de rencontre à la place ; Forced Response : après la fin de la phase du vilain, **retournez cette carte puis remettez ses PV à ses PV imprimés** ». B1/B2 : variantes (expert) : face cachée au lieu de défausse.
**Complot** : *The Hellfire Club's Revenge* (1 seul). **Setup du complot : « créer le Hellfire deck »** : chercher dans le deck de rencontre **chaque sbire ELITE HELLFIRE** et les mélanger dans **un deck à part avec sa propre défausse** (« When an ELITE, HELLFIRE minion is defeated or otherwise discarded, place it in the Hellfire discard pile ; if the Hellfire deck is empty, shuffle the Hellfire discard pile into it ; no penalty »).
**Deck de rencontre** : Torn, Perfection, Sebastian Shaw, Negasonic Teenage Warhead, Immensity + Standard ; les trois derniers modules peuvent être remplacés par **trois autres combinaisons de modules** contenant chacun un sbire ELITE HELLFIRE (Hellfire Conclave, Sebastian Shaw, Negasonic Teenage Warhead, Immensity).
**Side schemes de scénario** (cartes 3 à 5) : *Nova's Psychic Puppetry* (FRAGMENT, Hinder 12 ; « Forced Interrupt : quand la dernière menace est retirée, **Emma Frost s'échappe du contrôle de Cassandra Nova, les joueurs GAGNENT la partie** » ; « Forced Response : après qu'un sbire **ELITE HELLFIRE** est vaincu, retirez 5 menace d'une autre side scheme »), *Psychic Bulwark* (Victory 1, chaque sbire gagne guard et patrol), *Uncover The Truth* et *Protect Students* (obligations).
**Victoire du scénario** : voir le complot ; campagne : mêmes étapes.

### Scénario 5 : Cassandra Nova : 24 cartes
**Vilain** : Cassandra Nova (I) 15 PV, **(II) 18 PV**, **(III) 20 PV en expert** ; MUMMUDRAI. PSIONIC. ; **« Forced Response : après qu'elle active contre vous, placez 1 compteur « Cassandra Controls » sur votre identité »** ; (II) : **Steady** ; **When Revealed : 1 compteur sur chaque identité** ; (III) : **Stalwart**, + **1 jeton d'accélération par joueur sur le complot** au dévoilement.
**Complots** : *Diplomatic Sabotage* (1A : « retirez le sbire Cassandra Nova ; **mettre en jeu l'environnement Cassandra Domination** ; en expert, avance directement à 2A ») → *Silent Takeover* → *Mutant Extermination* (3B : « si vous avez des compteurs « Cassandra Controls » sur votre identité, vous devez **mettre 3 menace ici ou défausser 1 carte de la main** ; **Hero Action** : défaussez 7 cartes du deck de rencontre → retirez 1 compteur « Cassandra Controls » (1 fois par round par joueur) ; « When completed : les joueurs perdent la partie »).
**Cassandra Domination** (environnement, n°7) : « **Forced Response** : après qu'un compteur « Cassandra Controls » est placé sur votre identité, **s'il y en a au moins 3, retirez-en 3 → vous choisissez : 2 menace sur chaque complot, OU étourdir et désorienter votre identité, OU 3 dégâts indirects à un autre personnage ami** ». **FAQ** : si une seule autre cible a moins de 3 PV, l'option « dégâts » disparaît ; si déjà étourdi ou désorienté, l'option « étourdir/désorienter » disparaît ; il ne reste alors que la menace.
**Mise en place de campagne** : mélanger *Tactical Help* (185) et *Enemy of Enemy* (186) dans le deck de rencontre ; **révéler *Rally the Survivors* (184)** ; **retirer Xavier's Institute du jeu** ; créer le deck Recruited Mutants **à côté de *Rally the Survivors*** ; si Emma Frost's Redemption n'est pas cochée, mélanger Emma Frost (212) dedans. **Expert : « Si les joueurs perdent ce scénario, Cassandra Nova élimine tous les mutants et les joueurs perdent la campagne. »**
**Victoire** : **« Cassandra Nova est vaincue : les joueurs gagnent la campagne ! »**

## 4. Les neuf modules (comptes et usage ; CONTENU NON LU, voir §0)

| Module | Cartes | Utilisé dans | À retenir |
|---|---|---|---|
| **Perfection** | 8 | 1, 4 | non lu ; probablement le module des cartes ILLUSION (White Queen cite ce trait) : déduction |
| **Hellfire Conclave** | 8 | 1, 2, 3 | non lu ; cité par le livret comme module « ELITE HELLFIRE » (Torn) et retirable / ajoutable |
| **Mind Control** | 6 | 5 (et non 1 : correction du 26/10) | non lu ; retirable / ajoutable selon le livret |
| **Sebastian Shaw** | 8 | 2, 4 | non lu ; cité comme module ELITE HELLFIRE (Torn) |
| **Darkhold** | 6 | 3 | non lu ; le livret (complot 3A) parle de « Darkhold Dwarf » mis de côté puis mélangé au deck de rencontre |
| **Immensity** | 8 | 4, 5 | non lu ; cité comme module ELITE HELLFIRE (Torn) |
| **Negasonic Teenage Warhead** | 8 | 4 | non lu ; cité comme module ELITE HELLFIRE (Torn) |
| **Psionic Delusion** | 5 | **1** (livret p. 8, complot 1A : modulaire retirable) | à lire carte par carte (portage White Queen) |
| **Mutant Extinction Agenda** | 8 | 5 | non lu ; retirable / ajoutable selon le livret |

Total modules : **65 cartes**.

## 5. Ce que le moteur sait déjà faire (vérifié dans le dépôt)

| Besoin | État |
|---|---|
| Campagne linéaire avec carnet, mêmes identités | **Oui** : 15 campagnes déjà dans `data/campagnes/*.json` (modèle le plus proche : `skrull_menace.json`, déjà « zone de coopération » et `expert.pv_persistants`) |
| **PV persistants en expert** | **Oui** : `expert: { pv_persistants: true }` + détecteur `pv_restants` (`ui-app/src/board/campagne/detecteurs.ts`, `preremplissage.ts`) ; éprouvé en jeu : **non** (le rapport CAMPAGNES.md §1315 le dit) |
| Mots-clés Guard, Hinder, Incite, Patrol, Permanent, Piercing, Ranged, Setup, Stalwart, Steady, Team-Up, Temporary, Victory, Villainous, Armored, Amplify | **Oui** (fiches dans `docs/reference/mots-cles/`) |
| **Plusieurs vilains / vilain actif** | **Oui** : brique `Villains` (`src/game/operate/villains.py`), fiche `mechants-multiples.md` |
| **Retourner une carte / changer de forme sans reset** | Partiel : `Card.Flip` et `CardFace.FlipTo` existent ; le **vilain qui garde ses PV et ses attachements en changeant de face** n'a pas de précédent exact (les faces de vilain existantes sont des **stades** qui remettent les PV) |
| **Deck annexe par joueur** | Partiel : `player.additional_deck` / `additional_discard_pile` (précédent : Iron Patriot, fiche `piste-lead.md`) ; **un deck annexe PARTAGÉ (Recruited Mutants, Potential Ally, Hellfire deck) n'existe pas** |
| Perte de campagne en expert si défaite du dernier scénario | Précédent : **`aoa`** (« la seule victoire qui peut perdre la campagne ») : `docs/rapports/CAMPAGNES.md` |
| Compteurs nommés sur identité (« Cassandra Controls ») | **Oui** (compteurs libres, fiche `all-purpose-counter.md`) |
| Environnement qui se retourne (jour / nuit) | Partiel : à vérifier ; `environment.py` existe ; pas de précédent « jour/nuit » |

## 6. Les deux héros et leurs cartes

**Déjà portés dans le jeu** : `sunspot_hellfire` (préfixe `so`, 17 cartes, 54 cas) et `rachel_summers` (préfixe `rm`, 17 cartes, 59 cas). Les deux ont `player_deck` **vide** : « le dossier du zip n'imprime aucune decklist ». **Ce n'est plus vrai : le livret imprime les decklists p. 20 (« Starter Decks »).**

### Decklists imprimées p. 20 (à saisir dans `deck/starter/*.json`)
**Marvel Girl / Leadership** : Marvel Girl : Psyloche, Askani's Prophecies, Black Hole ×2, Psionic Blasts ×2, Telekinetic Counterblast ×2, Temporal Reversal, Clan Askani, Psionic Shield, Temporal Retrieval ×2, Telekinetic Axe, Telekinetic Sword ; Leadership : Boom Boom, Captain Britain, PAC-RAT II, Divided We Fall ×3, First Command ×3 ; Basic : White Phoenix, Jump-Start ×3, X-Gene ×2, X-Mansion, Mutant Education, Psionic Soulmates, From The Ashes ×2, Energy, Genius, Strength ; Némésis : Hound Program, Ahab, Hound Clothes ×3 ; Obligation : Memory From The Future.
**Sunspot / Aggression** : Sunspot : Cannonball, Blasting Strike ×2, Blessing of the Sun ×2, Radiant Disruption ×2, Soak Up The Sun ×2, Solar Flare, Solar Surge ×2, Da Costa International, Leader Of A.I.M., Solar Soar ; Aggression : Cable, Domino, Forge, Warpath, Battle Fury ×2, Combat Training ×2, Finishing Blow ×3 ; Basic : Caliban, Cecilia Reyes, Adrenaline Rush ×3, For What's Right ×3, X-Force Strike ×3, Energy, Genius, Strength ; Némésis : Superhuman Mutants Murdering, Donald Pierce, Cybernetic Assault ×2, Mutant Kidnapping ; Obligation : M-Pox Sickness.

### Cartes d'aspect (dossier `Hero/Aspect Cards/`, 15 cartes n° 013 à 027)
À **croiser avec la decklist ci-dessus** : ces 15 cartes ne sont **pas** dans le jeu (aucun « hellfire » dans `sets_info.json` hors Sunspot et Rachel). **Non lues** (images non affichées) : je suppose, sans l'avoir vérifié, qu'elles correspondent à des noms de la decklist (Cable, Domino, Forge, Warpath, Boom Boom, Captain Britain, PAC-RAT II, Caliban, Cecilia Reyes…). **Ce qui est sûr** : la decklist imprimée nomme des cartes d'aspect et Basic que le jeu n'a pas pour ces deux héros ; **le nombre exact et lesquelles sont des cartes officielles déjà dans le jeu sont à relever** (comparer chaque nom à `cards.json`).

**Ce qui est déjà fait côté héros** : le portage des deux héros est fait (identités, Setup, obligation, 15 cartes de héros chacun). **Ce qui manque pour que les decks de départ soient jouables** : leurs cartes d'aspect, de campagne et Basic (nombre exact à relever, voir ci-dessus).

## 7. Extensions de moteur nécessaires (avec carte modèle et plan)

| # | Extension | Carte modèle la plus proche | Plan |
|---|---|---|---|
| **E1** | **Vilain à deux faces qui change de forme sans reset des PV ni des attachements** (White Queen PSIONIC ⇄ DIAMOND ; « incite 1 » à chaque retour en PSIONIC ; stade suivant révélé **dans la même forme**) | Skrull à deux faces (`sk219a/sk208a`, `FlipThis`), Sinister Six `27100a` (crochet `GetVillain`) | ajouter une API `Villain.ChangeForm(effect, to)` qui échange la face visible **sans** appeler `SetStage` ; mémoriser la forme courante pour `RevealNextStage` ; cas : forme conservée à la défaite d'un stade, PV conservés, attachements conservés |
| **E2** | **Deck Recruited Mutants** (partagé, démarre vide, placé à côté de Xavier's Institute / Rally the Survivors ; défausse propre ; remélange automatique) | `player.additional_deck` (Iron Patriot) ; `deck_aside.py` | créer un deck nommé de **table** (pas de joueur) avec défausse ; commandes `Draw`, `Shuffle`, `Discard` ; remplacement de la défausse d'un allié RECRUITED par la défausse Recruited (« instead ») |
| **E3** | **Deck Potential Ally** (12 side schemes à part ; 1 par joueur mélangé au deck de rencontre) + « When Defeated : chercher l'allié dans la zone mise de côté et le mettre en jeu » | Setup de campagne `skrull_menace` (zone de coopération) ; `Search.EncounterCard` | zone « mise de côté » nommée dans le carnet ; mélange au setup selon le nombre de joueurs |
| **E4** | **PV persistants en expert** (noter, restaurer par jeton d'accélération) | `expert.pv_persistants` de `skrull_menace` et détecteur `pv_restants` | **déjà là** : à éprouver en jeu (jamais fait) ; ajouter le jeton d'accélération « restaurer » comme choix de setup |
| **E5** | **Hellfire deck** (Torn) : sbires ELITE HELLFIRE regroupés dans un deck à part avec défausse propre, remélange sans pénalité | `Villains.BuildVillainDeck` (deck de méchants à la demande) | réutiliser E2 (deck de table + défausse) ; capacité : « si un sbire ELITE HELLFIRE est vaincu ou défaussé, le mettre dans la défausse Hellfire » |
| **E6** | **Vilain à « PV ∞ » sur la face retournée** (Emma Frost A2/B2, Torn) : défaite impossible tant qu'elle est retournée ; se retourne après la phase du vilain avec remise à ses PV imprimés | Vilains « immortels » existants (Hydra God pas encore) ; `Stalwart`/`Permanent` | PV infinis = drapeau « indestructible » sur la face ; la remise à zéro au retournement |
| **E7** | **Environnements « jour / nuit »** (Black Queen : « Under the Moonlight » / « Beneath the Sun », qui s'échangent à chaque action) | `environment.py` ; `Faces.FlipAllTo` | transcrire les deux cartes, puis coder l'échange ; **à lire sur les cartes** (règle non détaillée dans le livret) |
| **E8** | **Compteurs « Cassandra Controls »** et leur environnement « Cassandra Domination » (déclenche un choix à 3 compteurs) ; **« Absorb »** de Shaw (compteurs d'énergie sur le vilain) | `all-purpose-counter.md` | compteurs nommés ; réponses forcées ; choix à trois branches avec **exclusions dynamiques** (FAQ : retirer l'option « dégâts » s'il n'y a pas de cible valide, l'option « étourdir » si déjà étourdi) |
| **E9** | **Défaite de campagne en expert** (scénario 5 perdu = campagne perdue) | `aoa` : « la seule victoire qui peut perdre la campagne » | champ de campagne `defaite_campagne_expert` sur le dernier scénario |
| **E10** | **Règle de deck-building des cartes de campagne** (cartes 263-288 : exclues du deck sauf ajout par la campagne ; ne comptent pas dans la taille du deck) | règles de deck propres au héros (GUIDE §14.1) | drapeau `Campaign` sur les cartes + `regles.js` |
| **E11** | **Side scheme « Fragment » avec « Hinder 12 » et victoire immédiate** quand la dernière menace est retirée (Torn) | `Hinder` (fiche) ; `Victory` | Forced Interrupt « les joueurs gagnent la partie » : précédent à chercher (`WinGame`) |

**Mots-clés absents du moteur** : aucun inédit parmi ceux du **livret** (p. 3, tous ont une fiche) ; ceux des cartes de modules n'ont pas été vérifiés. Nouveaux traits (CAPTIVE, RECRUITED, ILLUSION, DIAMOND, PSIONIC, FRAGMENT, HELLFIRE, ELITE) : simples traits.

## 8. Ordre de travail recommandé et estimation

**Cartes à porter via `PROCESSUS-CARTE.md`** (une par une) : **~300** :

| Bloc | Cartes |
|---|---|
| Scénario 1 White Queen (cartes de scénario + Perfection, Hellfire Conclave, Psionic Delusion partagés) | 32 + 8 + 8 + 5 |
| Scénario 2 Black King | 30 (dont **Shaw I/II/III, Black King, 2 complots à 2 faces, captifs**) |
| Scénario 3 Black Queen | 26 + Darkhold 6 |
| Scénario 4 Torn | 19 + Sebastian Shaw 8 + Negasonic 8 + Immensity 8 |
| Scénario 5 Cassandra Nova | 24 + Mutant Extinction Agenda 8 |
| Cartes de campagne | 8 + 16 alliés + 12 side schemes Potential Ally + 15 aspects |
| Psionic Delusion (modulaire non utilisé par un scénario du livret) | 5 |
| Decklists des héros (manquent) | ~15 aspects + cartes Basic de campagne (nombre exact à relever) |

**Ordre** :
1. **Fondations de campagne** : E2, E3 (decks de table), E10 (règle de deck), 16 alliés Recruited, Xavier's Institute, 12 Potential Ally, 15 aspects, **decklists des deux héros** (elles débloquent les parties d'essai).
2. **Scénario 1 White Queen** : E1 (forme du vilain), puis cartes ; **c'est la brique la plus risquée** : à faire en premier pour valider E1 et le cycle Recruited.
3. **Scénario 2 Black King** : E8 « Absorb », captifs ; réutilise E2.
4. **Scénario 5 Cassandra Nova** : E8 « Cassandra Controls », E9 (perte de campagne), environnement sans Xavier's Institute (Rally the Survivors).
5. **Scénario 3 Black Queen** : E7 (jour / nuit), à lire sur les cartes.
6. **Scénario 4 Torn** : E5, E6, E11 : **le plus atypique**, en dernier.
Raison : on commence par ce qui sert à tous les scénarios, puis par le scénario qui valide la mécanique la plus risquée (E1), puis du plus simple au plus atypique.

## 9. Questions réelles

Aucune des suivantes n'est tranchée par les règles ni par le livret :
1. **Black Queen (E7)** : la règle de « avancer le temps à chaque action » n'est pas dans le livret (seulement dans la description « chaque action avance le temps ») : elle est sur les deux cartes d'environnement. À transcrire carte par carte, **et si le texte ne suffit pas, question à l'utilisateur avec les images**.
2. **FAQ de Torn et des deux héros : « Still thinking »** : aucune réponse de l'auteur. Les doutes se trancheront par les règles et les cartes, comme décidé le 26/10/2026.
3. **Decklists** : faut-il compléter les deux decks de départ avec les cartes des §6 qui manquent (≈ 15 aspects plus des cartes Basic) **maintenant** (c'est nécessaire pour jouer la campagne) ou seulement quand on portera les scénarios ? **Recommandé : maintenant, car sans elles les héros n'ont pas de deck jouable.**
4. **Un seul vrai doute de règle repéré** : l'**ordre de révélation des stades en expert** pour White Queen : le livret dit « Retirez White Queen (1A) et ajoutez White Queen (3A) » : **les stades A1 et A3 sont-ils sur la même carte ou sur deux cartes distinctes ?** (le zip ne contient que 4 faces `1a/1b/2a/2b` et `3a/3b` : `3a`/`3b` existent donc bien). À confirmer en les lisant à l'écran lors du portage ; rien à demander à l'utilisateur avant.

## 10. Ce qu'il faut savoir avant de commencer

- **Aucun texte français** : il faudra écrire les ~300 textes (`ui-app/src/board/textes-fr-fanmade.ts`) et faire vérifier les voiles ; c'est un chantier aussi gros que le portage lui-même.
- **Le carnet** (`data/campagnes/hellfire_hunt.json`) : s'inspirer de `skrull_menace.json` (même auteur de la zone de coopération). Champs à créer : identité, PV restants (expert), alliés Recruited (liste de 16 cartes), 2 cases « défaite ».
- **Les 12 + 16 cartes d'alliés et de side schemes sont des doublons de Skrull Menace pour la forme** (mêmes mécaniques) : copier les modèles existants.
- **Les neuf modules sont réutilisables** ailleurs : bien les ranger en `modules` (précédent : `hunting_season`).

# Iron Fist : cartes d'aspect (22/10/2026), plan

Sources : `aspect-hoh/` (18 images 300 px de la page Hall of Heroes, n°12 à 18 = cartes d'aspect) et `cc-spoil/` (12 scans HD
« content creator », 1400x2000). Décisions de l'utilisateur : (1) les NOUVELLES cartes (64xxx, image officielle de la page) sont la
SOURCE (script, image, tests) ; les anciennes cartes de même texte deviennent des LIENS vers elles (réimpressions `full_link`, ou
art alternatif TMNT pour les 4 cartes TMNT via `tools/convertir_reskins_art_seul.py`) ; (2) les 12 cartes vraiment nouvelles sont
scriptées et testées une à une (PROCESSUS-CARTE) ; (3) ensuite : cartes d'aspect d'Elektra Natchios (MC63), sans le héros.

## 7 réimpressions (nouvelle = source, ancienne = lien)
| Nouvelle | Carte | Ancienne | Lien |
|---|---|---|---|
| 64013 | Helpful Bystander | up015 (TMNT Inkwire) | art alternatif TMNT |
| 64015 | Defiance | 26018 | full_link |
| 64016 | Demoralize | up009 (TMNT Inkwire) | art alternatif TMNT (citation différente) |
| 64017 | The Night Nurse | 09019 | full_link |
| 64018 | Redirection Mastery | up030 (TMNT Inkwire) | art alternatif TMNT |
| 64020 | Tonfa | up039 (TMNT Inkwire) | art alternatif TMNT |
| 64024 | Power Man and Iron Fist | 62023 | full_link |

## 10 cartes nouvelles
64014 Iron Fist (Lin Lie) ally Protection · 64019 No Time to Bleed (Protection, amélioration) · 64021 Colleen Wing (Basic, allié) ·
64022 Luke Cage (Basic, allié) · 64023 Punch, Reverse Punch (Basic) · 64025 Thunder Dojo (Basic, lieu) ·
64030 Death by a Thousand Cuts (Aggression) · 64031 Zen-Like Calm (Leadership) · 64032 Sensei (Leadership) · 64033 The Defenders (Basic, ressource).

Correspondance image : 12=Helpful Bystander, 13=No Time to Bleed, 14=Demoralize, 15=Redirection Mastery, 16=Tonfa, 17=Luke Cage, 18=Power Man ;
HD : 10-16=Iron Fist Lin Lie, 11-8=Defiance, 11-21=Night Nurse, 11-38=Colleen Wing, 12-15=Punch Reverse Punch, 12-32=Thunder Dojo,
12-55=Death by a Thousand Cuts, 13-27=Zen-Like Calm, 13-51=Sensei, 20-36=The Defenders (9-46 Embody et 9-54 Keep 'Em Coming : déjà faites).
Non publiées : numéros 26-29 et au-delà de 33.

## Données relevées (scans HD, 22/10/2026)
Ressources : R = poing rouge (physique), B = icône bleue « nœuds reliés » (mental), Y = éclair jaune (énergie).
| id | carte | type / classe | coût | RES | stats | traits | texte imprimé |
|---|---|---|---|---|---|---|---|
| 64014 | ✦ Iron Fist (Lin Lie) | Ally / Protection | 4 | R | PV 3, THW 1, ATK 2★ | AGENT OF ATLAS, MARTIAL ARTIST | ★ Response: After Iron Fist (this ally) attacks an enemy who has been attacked by a hero this phase, stun that enemy. If Iron Fist defeated that enemy, he takes −2 consequential damage (✪) from this attack. |
| 64019 | No Time to Bleed | Upgrade / Protection | 2★ | B | | CONDITION | ★ Discount 1 (Martial Artist or Soldier). Temporary. Max 1 per player. Response: After you play a card (including this one), heal 1 damage from your identity. |
| 64021 | ✦ Colleen Wing | Ally / Basic | 3 | R | PV 3, THW 1, ATK 2★ | HERO FOR HIRE, MARTIAL ARTIST | ★ Colleen Wing takes −1 consequential damage (✪) after she attacks an enemy who has been attacked by another Martial Artist character this phase. « Even I'd admit, she is probably the best samurai sword fighter outside of Japan. » —Razor Fist |
| 64022 | ✦ Luke Cage | Ally / Basic | 4 | R | PV 3, THW 1, ATK 2 | DEFENDER, HERO FOR HIRE | Toughness. If your hero shares a TRAIT with Luke Cage, your hero gets +1 DEF. « They don't call ol' Luke Cage 'Power Man' for nothin'! » |
| 64023 | Punch, Reverse Punch | Event / Basic | 1★ | R | | ATTACK | ★ Discount 1 (Martial Artist). Hero Action (attack): Deal 1 damage to an enemy. Deal 1 damage to an enemy. « It never hurts to practice even the basic forms. » —Shang-Chi |
| 64025 | ✦ Thunder Dojo | Support / Basic | 1 | Y | | LOCATION | Prerequisite (Defender or Martial Artist). Alter-Ego Action: Exhaust this card → shuffle up to 2 ATTACK events from your discard pile into your deck. Any player may trigger this ability. « I love giving back to the community. » —Danny Rand |
| 64030 | Death by a Thousand Cuts | Upgrade / Aggression | 2★ | R | | SKILL | ★ Discount 1 (Martial Artist or Soldier). Temporary. Max 1 per player. Response (attack): After you play a card (including this one), deal 1 damage to an enemy. |
| 64031 | Zen-Like Calm | Event / Leadership | 0 | Y | | TACTIC | Action: Heal 1 damage from a Martial Artist character. Then, if that character has no sustained damage, heal 1 damage from another character. « Matt, adjust your posture. Let your body relax. Bring your attention to your breath. » —Iron Fist |
| 64032 | Sensei | Upgrade / Leadership | 2★ | R | | TITLE | ★ Discount 2 (Martial Artist). Max 1 per player. Each Martial Artist ally you control takes −2 consequential damage (✪) after they exactly defeat an enemy or side scheme. |
| 64033 | The Defenders | Resource / Basic | – | – | | – | This card generates a [physical] resource for each Defender character you control (to a maximum of 4) and can be spent for another player whose identity has the Defender trait. |

Moteur : « enemy attacked by a hero / by another Martial Artist this phase » (64014, 64021) n'a pas de suivi par PHASE : `world.stat.this_turn_made_attack`
est remis à zéro à chaque tour de joueur. À ajouter : `this_phase_made_attack` (RecordAttack, reset OnPhaseEnd).

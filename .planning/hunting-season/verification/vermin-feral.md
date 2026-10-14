# Vérification vermin-feral (hs001-hs029, hs141-hs145)

Scans lus un par un. 36 fiches : 35 CONFORME, 0 ÉCART, 1 DOUTE (hs141, mineur).

Constats généraux valables pour tout le groupe :
- Toutes les cartes sont recto simple, sauf hs004a/b et hs005a/b (faces A/B de schémas principaux). Le pied de carte donne « VERMIN (n/29) » et « FERAL INSTINCTS (n/5) », cohérents avec les card_id.
- Icône de boost : sur ces scans, l'icône de boost est un petit glyphe rouge en forme de « Y » (deux branches + pied) en bas à droite ou à gauche. Nombre de Y = valeur Boost du JSON, sur toutes les cartes (0 sur les rats, 1 sur clones/Swarmed/treacheries, 2 sur hs020, hs021, hs142). Une étoile rouge dans le coin (rats, clones, hs143) signale l'effet « ★ Boost », pas une icône de boost.
- Les stats SCH/ATK des trois Vermin portent une petite étoile dans le coin de l'éclat (0*, 1*, 1*, 2*), absente du JSON (« 0 », « 1 », « 2 »). Aucun effet de jeu : l'étoile renvoie au texte de la carte.
- Le texte scanné contient la coquille « additonal » sur hs015/016/017 ; le JSON la corrige en « additional ». Sans effet.

| card_id | verdict | résumé |
|---|---|---|
| hs001 | CONFORME | Vermin I, PV 12 par joueur, SCH 0 ATK 1, MUTATE RAT, texte identique |
| hs002 | CONFORME | Vermin II, PV 14 par joueur, SCH 1 ATK 1, 2 cartes défaussées, « first RAT » |
| hs003 | CONFORME | Vermin III, PV 20 par joueur, SCH 1 ATK 2, « each RAT », Special d'Even More Rats |
| hs004a | CONFORME | Main scheme 1A, Contents et Setup identiques (Regular Rats engagé avec chaque joueur) |
| hs004b | CONFORME | 1B, cible 6 par joueur, +1 par joueur (étoile) et 1 par joueur, Forced Response identique |
| hs005a | CONFORME | 2A, When Revealed Bringer of Plague, avance en 2B |
| hs005b | CONFORME | 2B, cible 8 par joueur, +1 par joueur et 1 par joueur, texte et phrase de défaite identiques |
| hs006 | CONFORME | Environnement Even More Rats, texte et Special identiques |
| hs007 | CONFORME | Regular Rats, SCH 0 ATK 1, PV X (cercle), Surge, Boost 0, ★ Boost identique |
| hs008 | CONFORME | idem hs007 |
| hs009 | CONFORME | idem hs007 |
| hs010 | CONFORME | idem hs007 |
| hs011 | CONFORME | Feral Rats, SCH 0 ATK 1, PV X, Surge. Quickstrike., ★ Boost identique |
| hs012 | CONFORME | idem hs011 |
| hs013 | CONFORME | idem hs011 |
| hs014 | CONFORME | idem hs011 |
| hs015 | CONFORME | Vermin Clone, PV 4, SCH 1 ATK 2, Guard, Boost 1, MUTATE RAT, texte identique (coquille « additonal » corrigée) |
| hs016 | CONFORME | idem hs015 |
| hs017 | CONFORME | idem hs015 |
| hs018 | CONFORME | Swarmed by Rats, CONDITION, Boost 1, texte et Interrupt identiques |
| hs019 | CONFORME | idem hs018 |
| hs020 | CONFORME | Side scheme, menace 2 par joueur, icône crise (« ! » dans éclat) = Crisis 1, Boost 2, texte identique |
| hs021 | CONFORME | Side scheme, menace 3 fixe, icône Hazard (croix « + » sur tuile), Boost 2, texte identique |
| hs022 | CONFORME | A Mischief of Rats, Boost 1, texte identique |
| hs023 | CONFORME | idem hs022 |
| hs024 | CONFORME | Rabid Assault, Boost 1, deux When Revealed (Alter-Ego / Hero) identiques |
| hs025 | CONFORME | idem hs024 |
| hs026 | CONFORME | A Thousand Bites, Boost 1, texte identique |
| hs027 | CONFORME | idem hs026 |
| hs028 | CONFORME | idem hs026 |
| hs029 | CONFORME | idem hs026 |
| hs141 | DOUTE | Feral Instincts : SCH porte une étoile (pas de valeur) absente du JSON |
| hs142 | CONFORME | Primal Strength, ATK +X, Boost 2, SKILL, texte identique ; icône « physical » plausible (voir note) |
| hs143 | CONFORME | Unleashed Beast, Boost 1, When Revealed + ★ Boost identiques |
| hs144 | CONFORME | Cornered Animal, Boost 1, texte identique ; icône « energy » plausible (voir note) |
| hs145 | CONFORME | idem hs144 |

## Détail des DOUTE

### hs141 Feral Instincts
- Scan : à gauche, sous le titre vertical, deux blasons de stat : un SCH bleu contenant une ÉTOILE blanche à la place d'un chiffre, et un ATK rouge « +2 ». Boost : un Y. Texte : « Attach to the villain. ★ Forced Interrupt: When the villain would scheme against you, it attacks you instead. This attack gains overkill. Do not give the villain a boost card for this activation. Then, Discard Feral Instincts. »
- JSON : desc {"ATK+": "2", "Boost": "1"}, aucune clé SCH. Texte identique (seule différence : « Then, discard » en minuscule dans le JSON, sans effet).
- Différence : le blason SCH à étoile n'est pas transcrit.
- Effet sur le jeu : aucun, car l'étoile sans nombre ne donne pas de bonus SCH et le texte ne l'explicite pas. Seul l'affichage du blason SCH étoilé sur la carte est perdu. À trancher si on veut le reproduire (modificateur SCH nul, ou rien).

## Notes sur les icônes (jamais certaines)
- hs142 : deux petits glyphes noirs en forme de poing fermé dans « spend ⟨⟩⟨⟩ resources ». Forme cohérente avec l'icône Physical (poing), mais monochrome et minuscule : icône douteuse, correspond à [physical][physical] du JSON.
- hs144/hs145 : un glyphe noir en éclair incliné dans « spend a ⟨⟩ resource ». Forme cohérente avec Energy (éclair), monochrome : icône douteuse, correspond à [energy] du JSON.
- hs021 : icône d'une croix « + » sur une tuile à coin coupé au centre du cadre de texte, lue comme Hazard (le JSON dit Hazard 1) : forme à confirmer contre le jeu d'icônes officiel.
- hs020 : icône « ! » dans un éclat, lue comme Crisis (JSON Crisis 1), même réserve.

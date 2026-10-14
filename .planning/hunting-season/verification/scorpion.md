# Vérification groupe « scorpion » (hs030 à hs053)

Scans lus un par un contre cards.json (clé hunting_season). Scorpion (1/24) à (24/24) : toutes les fiches du scénario sont présentes (hs033/hs034 sont des recto-verso, clés hs033a/b et hs034a/b). Les doubles (hs040/041, 042/043, 048/049, 050/051, 052/053) sont identiques entre eux, seul le numéro de collection change.

## Récapitulatif

| card_id | verdict | résumé |
|---|---|---|
| hs030 | CONFORME | Scorpion I, HP 15 par joueur, SCH 1, ATK 2, CRIMINAL, Forced Interrupt (1/24) |
| hs031 | CONFORME | Scorpion II, HP 16 par joueur, SCH 2, ATK 2, non étourdissable (2/24) |
| hs032 | CONFORME | Scorpion III, HP 18 par joueur, SCH 2, ATK 3, When Revealed Tail Laser (3/24) |
| hs033a | CONFORME | Thirst for Revenge 1A, Contents + Setup identiques (4/24) |
| hs033b | CONFORME | 1B : départ 1/joueur, cible 6/joueur, escalade +1/joueur, When Completed (4/24) |
| hs034a | CONFORME | Vengeful Pursuit 2A, When Revealed avance en 2B (5/24) |
| hs034b | CONFORME | 2B : départ 0, cible 3/joueur, escalade +1/joueur, Forced Interrupt identique (5/24) |
| hs035 | CONFORME | J. Jonah Jameson, PERSONA, Permanent, Interrupt, Forced Interrupt « 3 + 1 par joueur » (6/24) |
| hs036 | ÉCART | Scorpion's Tail : « that character » devient « the character » dans le JSON (7/24) |
| hs037 | CONFORME | Tail Armor, boost 2, ARMOR TAIL TECH, texte identique (8/24) |
| hs038 | CONFORME | Honed Stinger, boost 1 + étoile, texte identique (9/24) |
| hs039 | CONFORME | Tail Laser, boost 1 + étoile, texte identique (10/24) |
| hs040 | CONFORME | Coiled Up, THW/ATK/DEF -1, texte identique (11/24) |
| hs041 | CONFORME | Coiled Up, copie de hs040 (12/24) |
| hs042 | CONFORME | Human Fly, HP 2, SCH 0, ATK 2, boost 0 + étoile (13/24) |
| hs043 | CONFORME | Human Fly, copie de hs042 (14/24) |
| hs044 | DOUTE | Grizzly : le scan met une petite étoile sur l'ATK 3, absente de la fiche (15/24) |
| hs045 | CONFORME | Hippo, HP 6, SCH 1, ATK 3, Toughness, boost 1 + étoile (16/24) |
| hs046 | CONFORME | Luring Out Prey, départ 2, icône Crisis, boost 1 (17/24) |
| hs047 | CONFORME | A Mess of Things, départ 2, icône Hazard, boost 3 (18/24) |
| hs048 | CONFORME | Tail Enhancements, boost 0 + étoile (19/24) |
| hs049 | CONFORME | Tail Enhancements, copie de hs048 (20/24) |
| hs050 | CONFORME | Stinger Stab, boost 1 (21/24) |
| hs051 | CONFORME | Stinger Stab, copie de hs050 (22/24) |
| hs052 | CONFORME | Restraining Pincers, boost 0 + étoile, icônes « poing » (23/24) |
| hs053 | CONFORME | Restraining Pincers, copie de hs052 (24/24) |

Bilan : 24 CONFORME, 1 ÉCART, 1 DOUTE (sur 26 fiches).

## Détail des écarts et doutes

### hs036 Scorpion's Tail : ÉCART (texte)
- Scan : « Forced Response: After Scorpion attacks and damages a character, that character is stunned. If **that** character is already stunned, deal 1 damage to that character. »
- JSON : « ... that character is stunned. If **the** character is already stunned, deal 1 damage to that character. »
- Différence : « that » remplacé par « the ». Sens identique.
- Effet jeu : aucun (même personnage visé). Correction purement textuelle, à aligner pour fidélité.
- Remarque annexe : le scan imprime « +1* ATK » (petite étoile sur la valeur) ; le JSON a `ATK+: "1"` sans astérisque. Voir hs044 pour la même question. Le reste (Interrupt, 10 par joueur, 8 par joueur, TECH. WEAPON.) est conforme.

### hs044 Grizzly : DOUTE (étoile sur l'ATK)
- Scan : ATK affiché « 3 » avec une petite étoile blanche en exposant (même marque que le « +1* » de hs036). SCH 1 sans étoile, HP 6, boost 1 + icône étoile. Texte : « Forced Interrupt: When Grizzly attacks, the attack gains piercing. » (étoile devant) et « Boost: This attack gains piercing. » (étoile devant).
- JSON : `ATK: "3"` sans astérisque ; texte identique au scan.
- Différence : l'astérisque de valeur (stat modifiée par le texte de la carte) n'est pas transcrit. Hippo (hs045), qui n'a pas d'étoile sur l'ATK, est bien transcrit sans.
- Effet jeu : aucun si le moteur ignore l'astérisque (le texte porte déjà l'effet piercing). À trancher selon la convention du projet pour `ATK`/`ATK+` avec étoile (mettre "3*" et "1*" ?).

## Notes de lecture
- hs047 : l'icône du bas du cadre (carte penchée + croix, rien dessous) correspond à l'icône Hazard officielle de 01107 (Breakin' & Takin'), donc JSON `Hazard: 1` correct. hs046 : icône « ! » dans une étoile déchiquetée, correspond à Crisis.
- hs052/hs053 : « spend [icône][icône] » imprimé avec deux glyphes monochromes noirs en forme de poing, compatibles avec l'icône Physical. Aucune couleur visible pour confirmer (icône à forme de poing, lecture raisonnable mais non colorée).
- Boost : hs037 deux icônes (2), hs038/039 une icône + étoile (1), hs042/043/048/049/052/053 étoile seule (0), hs046 une icône (1), hs047 trois icônes (3), hs050/051 une icône (1), hs044/045 une icône + étoile (1). Tout concorde avec le JSON.
- Étoiles ★ sur les capacités : conformes sur hs030/031/032 (Forced Interrupt), hs036 (Forced Response), hs044, et sur les Boost étoilés. Aucune étoile sur Interrupt de hs037/038/039/040 : cohérent avec le JSON.

# Vérification lizard (hs054a à hs079, hs146 à hs150)

Total : 37 fiches. Conformes 32, écarts 3, doutes 2.

Remarque globale (non comptée en écart) : sur les scans, plusieurs statistiques portent une étoile (ex. SCH 2*, ATK 0*, hs054a). Le JSON stocke la valeur sans étoile ("2", "0"). Les PV « par joueur » sont notés "14*" dans le JSON, ce qui correspond à l'icône par joueur du scan. Sans effet si le moteur applique le texte de règle, à noter si l'étoile de stat doit être rendue.

| card_id | verdict | résumé |
|---|---|---|
| hs054a | CONFORME | Curtis I : SCH 2*, ATK 0*, PV 14 par joueur, texte identique, 1/26 |
| hs054b | CONFORME | Lizard I : SCH 0*, ATK 2, PV 14 par joueur, texte identique |
| hs055a | CONFORME | Curtis II : SCH 3*, ATK 0*, PV 16, texte identique |
| hs055b | CONFORME | Lizard II : SCH 1*, ATK 2, PV 16, texte identique |
| hs056a | CONFORME | Curtis III : SCH 3*, ATK 0*, PV 20, « place 2 shame counter » identique |
| hs056b | CONFORME | Lizard III : SCH 2*, ATK 2, PV 20, discard 2 par joueur, identique |
| hs057a | CONFORME | Complot 1A, texte identique (4/26) |
| hs057b | CONFORME | 1B : cible 4 par joueur, départ 0, escalade +1 par joueur, texte identique |
| hs058a | CONFORME | Complot 2A, texte identique |
| hs058b | CONFORME | 2B : cible 10 par joueur, départ X, escalade +X, texte identique |
| hs059a | CONFORME | Complot 3A, texte identique |
| hs059b | CONFORME | 3B : cible 6 par joueur, départ 0, escalade +1 par joueur, texte identique |
| hs060 | CONFORME | Environnement Reptilian Rage, texte identique (7/26) |
| hs061 | CONFORME | SCH +1, boost 1, texte et trait identiques (8/26) |
| hs062 | CONFORME | Identique à hs061 (9/26) |
| hs063 | CONFORME | Komodo Claws, boost 1, icône éclair, texte identique (10/26) |
| hs064 | CONFORME | Identique à hs063 (11/26) |
| hs065 | DOUTE | Lizard Tail : texte et ATK+1* OK, icône de ressource de l'Action Héros à confirmer ([mental] ?) |
| hs066 | DOUTE | Alligator Jaws : texte et ATK+1* OK, icône de ressource de l'Action Héros à confirmer ([physical] ?) |
| hs067 | ÉCART | Ancient Reptilian Brain : le scan porte un modificateur ATK étoile, absent du JSON |
| hs068 | ÉCART | Boa Constricted : le scan n'a AUCUNE icône de boost, le JSON dit Boost 2 |
| hs069 | ÉCART | Identique à hs068 |
| hs070 | CONFORME | Iguana Whip, boost 1 + étoile, texte identique |
| hs071 | CONFORME | Identique à hs070 |
| hs072 | CONFORME | Triggered Transformation, boost 0 + étoile, texte identique |
| hs073 | CONFORME | Identique à hs072 |
| hs074 | CONFORME | Shed Skin, boost 1 + étoile, texte identique |
| hs075 | CONFORME | Identique à hs074 |
| hs076 | CONFORME | Iguana : PV 7, SCH 0*, ATK 0*, boost 2, Elite/Reptile, texte identique |
| hs077 | CONFORME | Chameleon : PV 4, SCH*/ATK*, boost 1, Criminal/Reptile, texte identique |
| hs078 | CONFORME | Reptile Research : départ 2, icône Hazard (identique à hs021), boost 2, texte identique |
| hs079 | CONFORME | Identique à hs078 |
| hs146 | CONFORME | Wake Your Inner Lizard : départ 3, boost 3, texte identique (1/5) |
| hs147 | CONFORME | Lizard Thrall : PV 4, SCH 1*, ATK 2*, boost 1, Civilian/Reptile, texte identique (2/5) |
| hs148 | CONFORME | Lizard Thrall : PV 4, SCH 1*, ATK 2*, boost 1, Civilian/Reptile, texte identique (3/5) |
| hs149 | CONFORME | Lizard Thrall : PV 4, SCH 1*, ATK 2*, boost 1, Civilian/Reptile, texte identique (4/5) |
| hs150 | CONFORME | Lizard Thrall : PV 4, SCH 1*, ATK 2*, boost 1, Civilian/Reptile, texte identique (5/5) |

## Détails des écarts et doutes

### hs067 Ancient Reptilian Brain : ÉCART
- Scan : bloc ATK en bas à gauche avec une ÉTOILE seule (sans nombre), comme modificateur ATK de l'attachement.
- JSON : desc = {"Boost": "2"}, aucune clé ATK+.
- Texte de règle identique mot pour mot, seul le modificateur de stat manque.
- Effet : l'attachement n'a pas de modificateur ATK étoile enregistré. La règle d'attaque (« dégâts égaux à l'ATK du personnage attaqué ») est déjà dans le texte, mais l'icône/valeur d'étoile n'est pas rendue ni portée.

### hs068 et hs069 Boa Constricted : ÉCART
- Scan : coin bas droit de la carte vide, aucune icône de boost. Texte et trait Condition conformes.
- JSON : desc = {"Boost": "2"}.
- Effet : lorsque la carte est retournée comme boost, le moteur ajouterait +2 à l'attaque/complot alors que la vraie carte n'a aucun boost (0). Les deux exemplaires sont concernés. À corriger en Boost 0 (ou absence de clé).

### hs065 Lizard Tail : DOUTE (icône)
- Scan : l'Action Héros « Spend a [icône] resource » montre une icône noire de forme évoquant un nœud de petits cercles reliés (cerveau/pensée). Je ne la nomme pas avec certitude.
- JSON : [mental].
- Effet : si ce n'est pas mental, le coût de ressource de l'Action Héros est erroné.

### hs066 Alligator Jaws : DOUTE (icône)
- Scan : l'icône de ressource est un petit poing/ovale noir arrondi. Compatible avec physical, non certifié.
- JSON : [physical].
- Effet : même risque sur le coût de l'Action Héros.

### hs063 et hs064 : icône éclair (energy) conforme à la forme, jugée sûre.

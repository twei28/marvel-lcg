# Vérification groupe lodge (hs164 à hs199, The Lodge, 36 cartes)

Scans lus un à un. Collection : 1/36 à 36/36, dans l'ordre hs164 à hs199, une face (pas de recto-verso). Doublons (3 exemplaires) lus séparément, identiques entre eux.

## Remarques globales

- **Icône de ressource (toutes les cartes)** : DOUTE. Le scan montre dans le coin bas gauche un onglet vert foncé avec une étoile à 5 branches en contour (vert clair). Ce n'est pas une icône de ressource physique/énergie/mentale, et je ne peux pas affirmer qu'elle représente « wild » : le JSON dit RES=G (wild pour la fiche). Aucune autre icône de ressource n'est imprimée sur les cartes. À trancher par l'auteur (ou par rapport aux autres cartes campagne déjà portées).
- **Classe** : aucune classe/aspect affichée, les cartes sont « Campaign - The Lodge (n/36) » sur fond gris, cohérent avec Class=Campaign;Basic.
- **Étoiles des alliés** : sur le scan, chaque stat peut avoir (a) un ★ en exposant à côté du chiffre (renvoi au texte) et (b) une icône d'étoile en contour sous la stat (dégât consécutif). Le JSON écrit « n* » : lu comme présence de l'icône sous la stat, c'est conforme pour hs164, 165, 167, 168. Les ★ en exposant (hs164 ATK, hs166 THW) ne sont pas dans desc, mais le ★ est bien dans le texte de la carte.
- Icônes de texte vues : hs166 [mental] = trois points reliés (compatible mental), hs175-177 [physical] = poing.
- Textes d'ambiance non comparés (consigne).

## Tableau récapitulatif

| card_id | verdict | résumé |
|---|---|---|
| hs164 | CONFORME | Allié coût 2, THW 2, ATK 3★, PV 2, texte identique (1/36) |
| hs165 | CONFORME | Allié coût 3, THW 1, ATK 2, PV 5, texte identique (2/36) |
| hs166 | ÉCART | THW 1★ sans icône de dégât consécutif, ATK 1 avec icône : JSON met « 1* » aux deux |
| hs167 | CONFORME | Allié coût 2, THW 2, ATK 2, PV 3, texte identique (4/36) |
| hs168 | CONFORME | Gibbon coût 2, THW 1, ATK 1, PV 3, Experience Cost 1, texte identique (5/36) |
| hs169 | CONFORME | Evade : événement coût 0, Experience Cost 2, texte identique |
| hs170 | CONFORME | Evade : événement coût 0, Experience Cost 2, texte identique |
| hs171 | CONFORME | Evade : événement coût 0, Experience Cost 2, texte identique |
| hs172 | CONFORME | Taunt : événement coût 0, Experience Cost 1, texte identique |
| hs173 | CONFORME | Taunt : événement coût 0, Experience Cost 1, texte identique |
| hs174 | CONFORME | Taunt : événement coût 0, Experience Cost 1, texte identique |
| hs175 | CONFORME | Steadfast : événement coût 0, Experience Cost 3, icône [physical] = poing, sans trait, texte identique |
| hs176 | CONFORME | Steadfast : événement coût 0, Experience Cost 3, icône [physical] = poing, sans trait, texte identique |
| hs177 | CONFORME | Steadfast : événement coût 0, Experience Cost 3, icône [physical] = poing, sans trait, texte identique |
| hs178 | CONFORME | Finish Them Off : événement coût 0, Experience Cost 2, texte identique |
| hs179 | CONFORME | Finish Them Off : événement coût 0, Experience Cost 2, texte identique |
| hs180 | CONFORME | Finish Them Off : événement coût 0, Experience Cost 2, texte identique |
| hs181 | ÉCART | Fresh Tracks : scan « If this thwart removes », JSON « If that thwart removes » |
| hs182 | ÉCART | Fresh Tracks : scan « If this thwart removes », JSON « If that thwart removes » |
| hs183 | ÉCART | Fresh Tracks : scan « If this thwart removes », JSON « If that thwart removes » |
| hs184 | CONFORME | Savage Land soutien coût 2, texte identique (21/36) |
| hs185 | CONFORME | Hunting Rifle amélioration coût 2, Restricted, 3 munitions, texte identique |
| hs186 | CONFORME | Hunting Rifle amélioration coût 2, Restricted, 3 munitions, texte identique |
| hs187 | CONFORME | Hunting Rifle amélioration coût 2, Restricted, 3 munitions, texte identique |
| hs188 | CONFORME | Hatchet amélioration coût 0, Restricted, texte identique |
| hs189 | CONFORME | Hatchet amélioration coût 0, Restricted, texte identique |
| hs190 | CONFORME | Hatchet amélioration coût 0, Restricted, texte identique |
| hs191 | CONFORME | Hunterbot amélioration coût 1, Max 1 par joueur, texte identique |
| hs192 | CONFORME | Hunterbot amélioration coût 1, Max 1 par joueur, texte identique |
| hs193 | CONFORME | Hunterbot amélioration coût 1, Max 1 par joueur, texte identique |
| hs194 | CONFORME | Trap amélioration coût 0, texte identique |
| hs195 | CONFORME | Trap amélioration coût 0, texte identique |
| hs196 | CONFORME | Trap amélioration coût 0, texte identique |
| hs197 | CONFORME | In Hiding amélioration coût 0, texte identique |
| hs198 | CONFORME | In Hiding amélioration coût 0, texte identique |
| hs199 | CONFORME | In Hiding amélioration coût 0, texte identique |

## Détail des écarts

### hs166 Black Cat : ÉCART (dégât consécutif de THW)
- Scan : THW « 1 » avec ★ en exposant, AUCUNE icône d'étoile sous THW ; ATK « 1 » sans ★ en exposant, avec UNE icône d'étoile en contour dessous. Coût 4, PV 3.
- JSON : THW "1*", ATK "1*".
- Différence : THW n'a pas d'icône de dégât consécutif sur le scan (seul le ★ de renvoi au texte), alors que le JSON le marque comme les autres alliés. Si "*" = icône, THW devrait être "1" et ATK "1*".
- Effet sur le jeu : Black Cat subirait 1 dégât consécutif à chaque thwart alors que la carte n'en inflige aucun. Texte de règle identique au scan (Forced Response, top card, [mental], add to hand).

### hs181, hs182, hs183 Fresh Tracks : ÉCART (texte)
- Scan : « Interrupt: When you thwart, increase the amount of threat that thwart removes by 2. If **this** thwart removes the last threat from a scheme, deal 1 damage to an enemy and draw 1 card. »
- JSON : « ... If **that** thwart removes the last threat ... »
- Différence : « this thwart » devient « that thwart ». Sens identique en pratique.
- Effet sur le jeu : aucun, mais texte non fidèle au scan.

### hs164 Rocket Raccoon (note, CONFORME) 
ATK « 3 » porte un ★ en exposant et THW « 2 » n'en porte pas ; JSON "2*"/"3*" correct si "*" = icône sous la stat (présente aux deux).

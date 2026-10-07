# Mode manuel 100 % identique à OCTGN, et rangement des cartes posées (07/10/2026)

**Statut : EN COURS.** Demande de l'utilisateur : « Je veux qu'en manuel ce soit 100 % identique. Par contre, il faut trouver un moyen d'aussi pouvoir déplacer les cartes après qu'elles soient posées pour changer l'ordre, que ce soit les alliés, les sbires, les manigances ou les améliorations, et pouvoir aussi choisir que ce soit à gauche ou à droite. »

Référence : `definition.xml` et `actions.py` du dépôt Ouroboros009/OCTGN-Marvel-Champions (voir la mémoire raccourcis-octgn-source). Audit du 07/10 : l'aide du manuel est fidèle au code ; écarts listés ci-dessous.

## Décidé (questions une à une)

- Portée : TOUT. Écarts existants + ciblage + surlignage + multi-sélection + le reste.
- ↑ ↓ sur allié et sbire : comme OCTGN, ↑ = +1 dégât, ↓ = −1 dégât (aujourd'hui ↑ soigne). Héros et méchant : ↑ = +1 PV (inchangé, déjà comme OCTGN).
- Réordonner en manuel : glisser SIMPLE dans la même rangée (lâchée entre deux cartes de sa rangée, elle s'y range ; ailleurs, déplacement comme aujourd'hui). Alt + glisser marche aussi.
- Amélioration glissée sans Alt tout près de son personnage : change de côté ou de rang et reste attachée ; plus loin, déplacement comme aujourd'hui.

## Lots

1. Écarts existants : carte boost FACE CACHÉE à côté du méchant (`villainBoost`) ; ↑↓ allié/sbire = dégâts ; Suppr refuse une carte Permanent et envoie une carte « Victoire X » à la pile de victoire.
2. Rangement en manuel au glisser simple (rangées et améliorations, côté compris).
3. Ciblage : Maj+clic cibler / décibler, Échap décible tout, Maj+glisser d'une carte vers une autre = flèche.
4. Surlignage de couleur au pavé numérique (1 bleu, 2 orange, 3 vert, 4 violet, 5 rouge, 6 noir, 7 blanc, 0 retire).
5. Multi-sélection : Ctrl+clic, rectangle de sélection sur une zone vide ; les gestes s'appliquent à la sélection.
6. Le reste : Ctrl+I (fiche de la carte), Ctrl+A (méchant actif), Ctrl+H (charger un héros), F8 (prendre le contrôle des cartes communes), sauvegarde / chargement d'un état de table.

Chaque lot : tests, vérification au navigateur, aide du manuel mise à jour, commit. Rien n'est déployé sans « déploie ».

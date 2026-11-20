# Hellfire Hunt, scénario 1 « White Queen » : doutes de règle

Les n°1 (hf104b, fin de stade) et n°2 (RECETTES-MOTEUR, « uses a basic power or an enemy activates ») sont cités par les commentaires du code ; leur texte complet n'a pas été rédigé dans ce fichier (voir l'en-tête de `hf104b.py` et la ligne correspondante de `docs/reference/RECETTES-MOTEUR.md`).

## 3. hf304 Illusory Defender : « Attacks against you cannot be defended by allies or other identities » (scan `assets/pics/hf304.jpg`) : RÉSOLU (02/11/2026), plus de question

- Ancien doute : le message de défense ne disait pas QUI était attaqué ; la restriction valait pour toute attaque. À plusieurs joueurs, cela empêchait un allié de défendre un AUTRE joueur, ce que le texte (« against YOU ») n'impose pas.
- Résolu par le moteur, sans lecture ambiguë : le message porte maintenant la cible de l'attaque (`attacked_targets`, ajout additif). Lecture retenue, littérale : la restriction ne s'applique que si l'attaque vise l'identité du porteur ; alors seuls les alliés (tous, y compris les siens) et les AUTRES identités ne peuvent pas défendre ; l'identité du porteur le peut.
- Effet en jeu : solo, rien ne change pour les alliés (toujours exclus) ; à 2 joueurs, les attaques contre l'autre joueur restent défendables par tous ; le porteur peut défendre avec son propre héros (avant correctif il ne le pouvait pas).
- Reste un seul point subjectif, à ne poser à l'utilisateur que s'il le veut : « other identities » est lu comme « identités autres que celle du porteur » (le porteur reste libre de défendre). Recommandation : garder cette lecture (c'est la seule qui ne rend pas la carte punitive pour son propre porteur).

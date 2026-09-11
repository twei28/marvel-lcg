# Modale : prévenir quand un paiement rendra le coup sans effet

**Décidé avec l'utilisateur le 11/09/2026**, en questions une à une. À faire
**après** le déploiement du verrou Crise (sa décision).

## Le cas, en une phrase

`15012` Crisis Averted ne perce la Crise **que si elle a été payée avec une
ressource mentale**. Or le jeu demande la cible AVANT le paiement : au moment
d'autoriser le complot principal comme cible, il ne peut pas savoir. Son
ignorance est donc déclarée sans condition (voir `mots-cles/crisis.md`), et le
joueur peut encore la jouer « dans le vide » en payant sans mental.

C'est le **seul** cas du dépôt aujourd'hui.

## Ce qui a été décidé

| Question | Réponse |
|---|---|
| Quand prévenir | **Au moment de payer**, quand le joueur valide ses ressources |
| Sous quelle forme | **Une modale à confirmer**, Continuer / Annuler |
| Sur quoi se fonder | **Le moteur calcule** si le coup fera vraiment effet. Aucune carte nommée nulle part, ni dans le plateau ni dans une liste |
| Langues | FR et EN, comme tout le reste |

## Le montage retenu

⚠ Précision donnée à l'utilisateur : « le jeu calcule » et « la carte
déclare » se rejoignent techniquement. Pour calculer, le moteur doit savoir ce
que la carte exige. La chaîne est donc :

1. La carte déclare sa condition **une fois**, sur sa capacité (aujourd'hui
   `15012` déclare une ignorance inconditionnelle ; il faudra distinguer
   « PEUT ignorer », lu au ciblage, de « ignore vraiment », lu à la
   résolution, sans quoi le ciblage refuserait la cible).
2. Le moteur évalue la condition avec les ressources réellement choisies et
   renvoie au plateau un **avertissement déjà rédigé**.
3. Le plateau affiche la modale. Il ne connaît **aucune** règle de jeu ni
   aucun `card_id`.
4. Une **gate** refuse toute future carte conditionnelle qui oublierait sa
   déclaration, sur le modèle de `tools/verifier_ignore_crise.py`.

## Ce qu'il faut regarder en premier

- `effect_checker.py:245` : `SpendResource` rend le paiement, puis
  `IsMatchCost`. C'est là que le paiement devient connu, mais **après** que le
  joueur a envoyé sa réponse : la modale doit donc vivre côté plateau, avec
  une information fournie à l'avance par le moteur.
- `EffectDescriptor.Payment` (`render/descriptor/effect.py`) : la structure
  envoyée au plateau. C'est elle qui porterait le champ d'avertissement.
- `Ability.SetIgnoreKeyword` (`ability.py:468`) accepte déjà une `condition` :
  c'est le point d'accroche de la déclaration.

## Portée

Le mécanisme est pensé général (« ce coup ne produira aucun effet »), mais une
seule carte l'exerce aujourd'hui. Ne pas élargir aux autres coups sans effet
(soigner un personnage intact, attaquer pour 0) sans une demande explicite :
le risque de fausses alertes sur des coups volontaires est réel.

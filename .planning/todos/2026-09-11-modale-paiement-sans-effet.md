# Modale : prévenir quand un paiement rendra le coup sans effet — ✅ FAIT

**Livré le 11/09/2026 au soir.** Le détail est en bas de fiche (« FAIT LE
11/09/2026 »), avec le moteur, la gate, le harnais et le plateau. Vérifié le
14/09/2026 : `paid_with` dans `ability.py`, `coupSansEffet` dans `ask.ts`,
`tools/verifier_ignore_crise.py` en place, `paiement-sans-effet.test.ts`
11 cas verts.

⚠ **LEÇON, DEUXIÈME FOIS.** Le 13/09 j'avais reproposé la « modale du héros »
comme à faire alors qu'elle était close, pour avoir lu le haut de sa fiche et
pas le bas. Le 14/09 j'ai refait exactement la même chose ici : la phrase
ci-dessous disait « à faire après le déploiement du verrou Crise », le
déploiement avait eu lieu, et le travail aussi. **Une fiche se lit en entier,
et son titre porte le statut.** D'où le « ✅ FAIT » dans le titre.

**Décidé avec l'utilisateur le 11/09/2026**, en questions une à une. Était à
faire après le déploiement du verrou Crise (sa décision) ; ce déploiement a eu
lieu, et la suite aussi.

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

## ✅ FAIT LE 11/09/2026 (soir)

**Moteur.** `Ability.SetIgnoreKeyword('Crisis', paid_with="B")` remplace la
lambda écrite à la main : même condition (rien de payé, ou une mentale, joker
compris), et la couleur est gardée dans `AbilityIgnore.paid_with`. Au rendu
(`Effect.Render`, `get_warning`), si la cible est un complot principal sous
Crise et que la capacité ne l'ignore qu'à cette condition, le descripteur
porte `target_payment[*].warning = {"keyword": "Crisis", "paid_with": "B"}`.
Sans Crise, rien. Seule `15012` est concernée aujourd'hui.

**Gate.** `tools/verifier_ignore_crise.py` refuse désormais une ignorance
conditionnelle de la Crise écrite avec `condition=` (seule la forme
`paid_with` renseigne le rendu). Calibrée : remettre la lambda dans `15012`
la fait rougir.

**Harnais.** Le pilote note les `warning` vus (`etat["avertissements"]`,
exposé aux vérificateurs par `aides["etat"]`) ; vérificateur
`avertissement_crise` ; trois cas « MODALE » : sous Crise l'avertissement est
là et le coup payé en mental retire 6 ; sans Crise, aucun avertissement ;
témoin fort : payée sans mentale sous Crise, la carte ne retire rien.

**Plateau.** `ask.ts` : type `Avertissement`, lecture du champ `warning`,
`coupSansEffet(paiement, ressources)` (compare les lettres, joker accepté).
`interaction.ts` : `valider` demande confirmation via `useConfirmation`
(`ConfirmationJeu`, ton danger, Continuer / Annuler) quand le paiement choisi
n'a pas la couleur ; la validation courte est désactivée dans ce cas.
Textes FR + EN (`textesCoupSansEffet`, `dico-en.ts`). Tests :
`paiement-sans-effet.test.ts` (9 cas, dont le hook avec `window.confirm`
espionné).

**Non fait, et c'est voulu** : aucune généralisation aux autres coups sans
effet (soigner un personnage intact, attaquer pour 0), comme décidé plus
haut.

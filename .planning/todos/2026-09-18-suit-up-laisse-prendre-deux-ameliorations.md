# Suit Up laissait prendre deux améliorations, puis mangeait la carte

**Signalé en jeu le 18/09/2026** (partie Laura Kinney contre Crossbones,
rapport `rapport-the-infinity-stone-r2.txt`) : « je joue la carte En Costume,
et il me présente d'abord une première modale où je vois bien Acolyte, puis
quand je reclique sur Jouer il ne me propose plus Acolyte » ; puis « en plus il
me laisse prendre deux améliorations au lieu d'un allié et une amélioration, et
quand je choisis deux améliorations il considère que c'est un misplay donc il
ne fait rien du tout et il défausse En Costume ».

## La carte

`45017 Suit Up` (Age of Apocalypse, Commandement) : « **Alter-Ego Action**:
Search your deck and discard pile for **an ally and an upgrade that can be
attached to that ally**. Add them to your hand. *(Shuffle.)* »

## Ce qui n'était pas un défaut

**Acolyte** (`45015` Sidekick) : « Attach to an **identity-specific** ally you
control ». Dans cette partie, le deck ne contenait que Marrow, Maria Hill,
Yondu et Triage : aucun allié signature, l'allié signature de Laura Kinney
(Honey Badger) était déjà **en jeu**, donc hors de la recherche. Sidekick
n'était attachable à aucun allié trouvable : l'écarter était juste. La
première modale, elle, n'est pas une liste de choix : c'est le « regarde » de
toutes les cartes fouillées (`Faces.LookAt`). L'utilisateur l'a diagnostiqué
lui-même.

## La cause du vrai défaut

L'ancien script posait **une seule question à deux cibles** :

```python
.SetTarget(faces,
    finder=CardFinder(card_type=Upgrade|Ally, check_effect_fn=can_attach_to_ally),
    select_rule="DifferentType",
    range=(2, 2), by_search=True,
    check_again_fn=has_one_ally_and_one_attachable_upgrade)
```

Trois défauts dans cette seule ligne :

1. **`select_rule="DifferentType"` n'est appliqué nulle part.**
   `SelectorRule.AfterSelectTargets` (`src/game/selector/selector_rule.py`)
   vérifie le NOMBRE de cibles, les coûts combinés et la règle
   `VillainAndMinions...`, mais jamais `DifferentType` ni `DifferentCards`.
   `EffectChecker` ne s'en sert que pour compter combien de types EXISTENT
   parmi les cibles légales, pas pour contraindre la sélection. Le plateau,
   lui, lit `select_rule` dans `ask.ts` et ne s'en sert nulle part. Résultat :
   deux améliorations étaient un choix accepté.
2. **Le couple n'était refusé qu'après coup**, par `check_again_fn` : l'effet
   échouait, et l'événement partait à la défausse sans rien faire. Le joueur
   perdait sa carte pour un choix que le jeu lui avait proposé.
3. **Les améliorations offertes étaient celles attachables à n'importe quel
   allié du deck**, pas à l'allié retenu.

## Le correctif

Deux recherches successives, comme le texte les énonce :

```python
allie = Search.PlayerCard(..., not_move=True,
    finder=CardFinder(card_type=Ally, check_effect_fn=allie_equipable))
amelioration = Search.PlayerCard(...,
    finder=CardFinder(card_type=Upgrade, canbe_attach_to=allie))
initiator.GainCard([allie, amelioration], effect)
```

`CardFinder(canbe_attach_to=<allié>)` appelle `Upgrade.CanAttachTo`
(`card_type/upgrade.py:83`), qui relit le sélecteur de la capacité « Play » de
l'amélioration : c'est la VRAIE règle d'attache, pas une approximation. Patron
déjà éprouvé par le pack `patriot` (`pt002` Hawkingbird,
`AmeliorationAttachableA`), et c'est aussi ce que faisait le brouillon
`45017_.py` resté dans le pack en amont (fichier mort : son nom ne correspond à
aucun `card_id`, le moteur ne le charge pas).

`allie_equipable` écarte en plus les alliés **sans aucune amélioration
attachable** : sinon le joueur choisit un allié, la seconde recherche ne
propose rien, et la carte est de nouveau perdue pour rien. « for an ally AND an
upgrade » : les deux ou aucun.

`not_move=True` sur la première recherche : le deck ne doit être mélangé
qu'une fois, par la seconde (« (Shuffle.) »).

## Gabarit PROCESSUS-CARTE

### 45017 : Suit Up

- [x] Étape 2 : cartes de référence : `pt002` Hawkingbird (pack patriot,
      `CardFinder(canbe_attach_to=<allié>)` + `GainCard`), brouillon amont
      `45017_.py` (deux `Search.PlayerCard`), `45015` Sidekick pour la règle
      d'attache la plus étroite du jeu.
- [x] Étape 5 : texte-contre-code, mots-pièges : « an ally **and** an upgrade »
      (les deux ou aucun, d'où le filtre sur les alliés) ; « that can be
      attached to **that** ally » (le filtre porte sur l'allié RETENU, pas sur
      un allié quelconque) ; « your deck **and** discard pile » (les deux
      zones) ; « (Shuffle.) » (un seul mélange, donc `not_move=True` sur la
      première recherche) ; « Alter-Ego Action » (aucune forme à changer : la
      partie commence en alter-ego).
      Résultat : conforme.
- [x] Étape 6 : nombres texte ↔ code : coût 2, ressource R, classe
      Commandement, `MaxPerDeck` absent : lus nativement dans `desc`, aucun
      nombre recodé.
- [x] Étape 7 : cas `test_capacites` + preuve par substitution :
      capacité unique (Alter-Ego Action) :
      `45017 Suit Up [aoa] — un allie ET une amelioration attachable a CET allie arrivent en main ; l'amelioration d'identite est ecartee`,
      `45017 Suit Up [aoa] — contre-cas : aucune amelioration attachable a un allie, rien n'entre en main`,
      `45017 Suit Up [aoa] — Sidekick (45015, « identity-specific ally ») n'est prise qu'avec l'allie signature : Black Cat, pas Maria Hill`.
      Générateur : `.planning/todos/generateurs-fne/gen_cas_45017.py`.
      Substitution : `substituer_pack.py .game-src-a 41600 45017` → **rouges
      3/3**, module intact après coup (md5 identique).
      Résultat : 3/3 verts.
- [x] Étape 7 bis : limite imprimée ? NON.
- [x] Étape 8 : autoplay ciblé : 8 parties `bishop` (deck de départ qui
      contient 45017) contre Rhino, profil équilibré : 0 traceback sur les 8
      journaux, 0 V / 8 D, aucune partie bloquée.
      ⚠ **Le pilote n'a JAMAIS joué Suit Up** (0 activation sur 8 parties : il
      reste en forme héros et dépense la carte comme ressource). L'autoplay
      prouve donc l'absence de plantage, pas le comportement de la carte :
      celui-ci n'est tenu que par les trois cas du harnais.
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON au sens du
      plateau : elle n'attache rien, ne pose ni compteur ni statut, et les deux
      modales (« cartes regardées », « cibles hors table ») sont le sélecteur
      GÉNÉRIQUE du moteur. Ce que le correctif change, c'est la LISTE que le
      moteur y envoie, mesurée par les cas ci-dessus.

Carte terminée : **OUI**.

## La même règle, sur l'autre carte qui la porte

`01042 Ancestral Knowledge` (« Choose up to 3 **different** cards in your
discard pile ») porte `select_rule="DifferentCards"`, la même règle que
personne n'appliquait : rien n'empêchait de choisir trois exemplaires de la
même carte, contre la FAQ citée dans son propre script.

**Option A retenue et faite** : le plateau applique désormais `select_rule` À
LA DÉSIGNATION (`ui-app/src/board/regles-selection.ts`, branché dans
`interaction.ts` pour les cibles de la table ET pour le sélecteur hors table) :
une cible qui casserait la règle n'est plus cliquable. 6 tests unitaires
(`regles-selection.test.ts`), suite complète du plateau 1676/1676, `tsc` propre.

Refuser au moment de VALIDER (option B, côté moteur) reste non fait : ce serait
correct mais ferait perdre la carte, c'est-à-dire exactement le défaut qu'on
vient de corriger. À reprendre seulement si un client autre que ce plateau
compose un choix illégal.

⚠ Le plateau ne connaît que ce que le moteur lui envoie : `card_id` et
`card_type`. « Cartes différentes » y est donc lu comme « identifiants
différents », ce qui est vrai pour le dépôt (deux exemplaires partagent leur
`card_id`), mais ne saurait pas distinguer deux réimpressions de titre
identique sous des identifiants différents.

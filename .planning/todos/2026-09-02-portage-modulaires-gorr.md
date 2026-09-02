# Portage des deux SETS MODULAIRES de Gorr — journal de validation

Sets **145. Intergalactic Hazards** (préfixe `ih`, 6 cartes physiques,
4 card_id) et **146. Necroverse** (préfixe `nv`, 8 cartes, 6 card_id). Auteur
**BLUEHG**, comme le pack Gorr. Zips fournis par l'utilisateur le 02/09/2026,
portés dans la foulée.

Les doublons (Bounty Hunter, Turned Around, Shadow Serpent, Dark Apotheosis)
sont pixel-identiques, vérifié par comparaison de la zone de texte.

---

## 0. Pourquoi ces deux sets comptent pour Gorr

Le pack Gorr les cite tous les deux dans le texte de Deicide 1A :

- **Necroverse** est mis de côté au Setup (gb004a) et remélangé dans le deck
  de rencontre à l'étape 3A (gb006a). Sans lui, **ces deux moitiés de cartes
  ne faisaient rien** : le cas du Setup restait vert sous substitution, faute
  d'effet mesurable. Il est désormais **rouge sans son module** (1/1), et un
  cas neuf prouve que les 8 cartes reviennent bien au stade 3.
- **Intergalactic Hazards** est le modulaire *recommandé* par le même texte.
  Il remplace Légions de Hel dans `data/scenarios/gorr.json` et
  `gorr_expert.json`.

Les deux scénarios déclarent donc maintenant
`encounter_sets: ["gorr", "necroverse", "standard"]` et
`modular_sets: ["intergalactic_hazards"]`.

---

## 1. Contenu

### Intergalactic Hazards — tout tourne autour du statut DÉSORIENTÉ

| id | carte | ce qu'elle fait |
|---|---|---|
| ih001 | Bounty Hunter ×2 | Sbire CRIMINAL, Patrouille. ★ +2 ATQ **si le héros est désorienté** |
| ih002 | Solar Flare | Désorienté → 3 dégâts indirects ; sinon, **devient** désorienté. ★ Boost : se révèle |
| ih003 | Turned Around ×2 | Désoriente, **puis** un sbire engagé attaque |
| ih004 | Asteroid Belt | Environnement, `Uses (2 par joueur, compteurs asteroid)`, 2 dégâts indirects à chacun en fin de phase des joueurs |

### Necroverse — le renfort qui arrive au stade 3

| id | carte | ce qu'elle fait |
|---|---|---|
| nv001 | Shadow Serpent ×2 | Sbire 6 PV, MNG 2 / ATQ 3. ★ attaques avec **overkill**. ★ Boost : 1 carte de rencontre face cachée |
| nv002 | Annihilablade | Attachement sur le vilain, +1 ATQ. ★ un allié vaincu par le vilain est **retiré du jeu** |
| nv003 | Dark Apotheosis ×2 | Attachement +1 ATQ / +1 MNG sur **l'ennemi le plus solide** |
| nv004 | Manifest Will | Remélange les **sbires** de la défausse, en révèle un |
| nv005 | The Ingenuity of Hatred | Idem pour les **attachements** |
| nv006 | The Planet Cleaver | Complot annexe, Hinder 2 par joueur, **icône Hasard** tant qu'il est en jeu |

---

## 2. Arbitrages et pièges

- **`nv002` s'attache « to the villain »**, pas à Gorr : ces sets sont
  modulaires, ils peuvent accompagner n'importe quel scénario.
  `CardFinder(card_type=Villain)`, jamais un nom.
- **`nv003` « the enemy with the most hit points REMAINING »** : les PV
  restants, pas imprimés — un vilain blessé peut céder la place à un sbire
  frais. Fonction de sélection `max(ennemis, key=health)`.
- **`nv006` « 1 carte de rencontre face cachée de plus par joueur »** EST la
  définition de l'icône **Hasard**. Mais `desc.Hazard` s'applique quand la
  carte QUI LA PORTE est révélée, alors que le texte est une Interruption
  Obligatoire qui dure tant que le complot est sur la table : elle est donc
  donnée par `ThisGainKeyword(hazard=1)`.
- **`ih004`** : `Uses (2 asteroid counters)` est une base automatique. Le
  moteur pose les compteurs à l'entrée en jeu **et défausse la carte quand le
  dernier part** : c'est ainsi que l'environnement se retire, rien à coder.
  Nouveau compteur `'asteroid'` ajouté au `Literal CardFace.COUNTER`.
- **`ih003` : l'ordre compte.** « You are confused. **Then**, choose an
  engaged minion » — le statut d'abord, l'attaque ensuite. Le cas le prouve :
  Bounty Hunter frappe à 1+2 parce que le héros vient d'être désorienté.

---

## 3. Deux vrais défauts trouvés par les tests

1. **`RegisterTemp` sans `unregister_after_exec`** (gb018 et ih002, les deux
   ★ Boost qui se révèlent) : l'argument est un mot-clé **sans valeur par
   défaut** (`face_effect.py:98`). Le `TypeError` était avalé par le moteur,
   et **le ★ Boost ne faisait rien**. Trouvé par l'autoplay.
2. **Révéler ne suffit pas.** Une fois l'argument corrigé, la carte entrait
   bien en jeu… puis le moteur poursuivait son rangement et la défaussait
   aussitôt. Il faut **remplacer** la défausse : `WhenCardWouldDiscard` porte
   `CanBeInstead`, donc `message.SetBeInstead(effect)` avant de révéler.
   Trouvé par les deux cas de test écrits juste après le premier bug.

Leçon : un ★ Boost qui met une carte en jeu a besoin de son propre cas. Sans
lui, les deux pannes seraient passées inaperçues — la carte se serait
contentée d'être défaussée, ce qui est exactement ce qu'elle fait sans
capacité.

## 4. Un faux vert démasqué par la substitution

**`nv001`** vérifiait que l'allié tombait sous l'attaque du serpent — ce qui
arrive de toute façon (ATQ 3 contre 3 PV). Le cas blesse maintenant l'allié
d'abord (il ne lui reste qu'1 PV) et mesure **l'excès qui passe sur le
héros** : 2 dégâts avec overkill, 0 sans.

---

## 5. Batteries

- `test_capacites` : **`ih00` 8/8**, **`nv00` 6/6**, et **`gb0` 32/32** (les
  30 cas de Gorr, plus le cas du remélange Necroverse et le cas du ★ Boost).
- Substitution : `ih` **4/4 cartes** rouges, `nv` **6/6**. Un seul cas reste
  vert, assumé : « Asteroid Belt entre en jeu avec 2 compteurs » est une base
  automatique (`desc.Uses`), aucun module ne la porte.
- `test_cards` : **5057 ok / 0 err**.
- Autoplay 8 parties contre `gorr`, les deux modulaires en jeu : **0 erreur**,
  les 10 cartes vues en partie réelle.
- Batterie complète du harnais : **993/997**, les 4 rouges préexistants de
  Squirrel Girl, **0 régression**.
- `tools/audit_cartes.py` : **0 discordance** sur les deux sets.

---

## 6. Reste à faire

- **Une partie jouée à la main.**
- Le stade 3 n'est jamais atteint en autoplay (les parties durent 6 tours) :
  le renfort Necroverse n'entre donc jamais dans le deck en jeu réel. Ce sont
  les cas de test qui le prouvent, par le vilain III en expert.

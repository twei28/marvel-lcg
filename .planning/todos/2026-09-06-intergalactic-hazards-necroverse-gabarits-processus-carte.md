# PROCESSUS-CARTE.md : les 10 gabarits des sets modulaires de Gorr

**145. Intergalactic Hazards** (préfixe `ih`, 4 `card_id`, 6 cartes
physiques) et **146. Necroverse** (préfixe `nv`, 6 `card_id`, 8 cartes
physiques). Gabarit régularisé le 06/09/2026 (audit C, point 3), sans
travail nouveau : mise en forme de la preuve déjà écrite le 02/09/2026 dans
`.planning/todos/2026-09-02-portage-modulaires-gorr.md` et dans l'en-tête de
chaque module `src/cards/pack/gorr/{intergalactic_hazards,necroverse}/*.py`.

Ces deux sets accompagnent le pack VILAIN Gorr (voir
`2026-09-06-gorr-gabarits-processus-carte.md`) : mêmes conventions (pas de
deck de départ, pas de textes français, `PROCESSUS-HEROS.md` non applicable).

**Preuves communes**, citées une fois :

- **Étape 1** : `data/cards.json`, sets `intergalactic_hazards` (4 card_id) et
  `necroverse` (6 card_id) ; préfixes `ih`/`nv` déclarés. ⚠ Le champ `cartes`
  de `tools/prefixes_fanmade.json` compte des **exemplaires physiques** pour
  ces deux entrées (6 et 8) et non des `card_id` (4 et 6), à la différence de
  la plupart des autres packs, écart documenté dans le texte libre de la
  note elle-même (constat de l'audit C, gravité basse, non corrigé ici : hors
  du périmètre des quatre points demandés).
- **Étape 4** : images dans `assets/pics/`.
- **Étape 7, batterie** : `test_capacites.py … ih0` → **8/8** ; `… nv0` →
  **6/6** ; `… gb0` → **32/32** une fois les deux sets déclarés dans les
  scénarios de Gorr (journal §5).
- **Étape 7, substitution** : `ih` **4/4 cartes** rouges, `nv` **6/6 cartes**
  rouges. Un seul cas reste vert dans tout le lot, assumé : « Asteroid Belt
  (`ih004`) entre en jeu avec 2 compteurs » est une base automatique
  (`desc.Uses`), aucun module ne la porte (journal §5).
- **Étape 8, autoplay** : 8 parties contre `gorr`, les deux modulaires
  déclarés dans le scénario, le 02/09/2026 : **0 erreur**, les 10 cartes
  vues en partie réelle (journal §5).
- `test_cards` : 5057 ok / 0 err. `tools/audit_cartes.py` : 0 discordance sur
  les deux sets.

⚠ **Ce que ces blocs ne peuvent pas voir** : aucune partie n'a été jouée par
un humain dans le navigateur (journal §6). Écrit ici noir sur blanc.

---

## Intergalactic Hazards (`ih`)

### ih001 : Bounty Hunter (×2, 1 card_id)
- [x] Étape 2 : sbire CRIMINAL, Patrouille, ★ +2 ATQ si le héros est
      désorienté (en-tête `ih001.py`).
- [x] Étape 5 : « if the hero is confused » lu sur le statut réel, pas sur un
      texte de carte. Résultat : conforme.
- [x] Étape 6 : ATQ de base 1, bonus +2. Résultat : conforme.
- [x] Étape 7 : `ih001 … +2 ATQ quand le heros est desoriente` +
      `ih001 … sans desorientation, l'ATQ reste a 1 (contre-cas)`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### ih002 : Solar Flare
- [x] Étape 2 : traitrise, branche « déjà désorienté » vs « devient
      désorienté », ★ Boost qui se révèle.
- [x] Étape 5 : ordre des deux branches vérifié (« if confused … otherwise »).
      Résultat : conforme.
- [x] Étape 6 : 3 dégâts indirects. Résultat : conforme.
- [x] Étape 7 : `ih002 … deja desoriente, 3 degats indirects` +
      `ih002 … sinon, le heros devient desoriente` +
      `ih002 … [star] Boost : la carte se revele au lieu d'etre defaussee`.
      ⚠ Vrai défaut trouvé et corrigé, partagé avec `gb018` : `RegisterTemp`
      sans `unregister_after_exec` avalait un `TypeError` (le ★ Boost ne
      faisait rien), puis la carte révélée était aussitôt redéfaussée sans
      `message.SetBeInstead(effect)` sur `WhenCardWouldDiscard` (journal §3).
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### ih003 : Turned Around (×2, 1 card_id)
- [x] Étape 2 : désoriente PUIS un sbire engagé attaque.
- [x] Étape 5 : ordre imprimé vérifié : « You are confused. **Then**, choose
      an engaged minion » : le statut d'abord, l'attaque ensuite. Le cas le
      prouve (Bounty Hunter frappe à 1+2 parce que le héros vient d'être
      désorienté, journal §2). Résultat : conforme.
- [x] Étape 6 : aucun nombre propre à la carte au-delà du statut. Résultat :
      conforme.
- [x] Étape 7 : `ih003 … desoriente, puis le sbire engage attaque`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### ih004 : Asteroid Belt
- [x] Étape 2 : environnement, `Uses` (2 compteurs `asteroid` par joueur,
      compteur ajouté au `Literal CardFace.COUNTER`), action qui retire X
      compteurs, X = le meilleur pouvoir de base du héros.
- [x] Étape 5 : « **2 asteroid counters** » est une base automatique
      (`desc.Uses`), rien à coder pour l'entrée en jeu ni pour la sortie
      (le moteur défausse la carte quand le dernier compteur part). X lu sur
      l'identité plutôt qu'écrit en dur (dépend du héros choisi). Résultat :
      conforme.
- [x] Étape 6 : 2 compteurs par joueur, 2 dégâts indirects en fin de phase.
      Résultat : conforme.
- [x] Étape 7 : `ih004 … entre en jeu avec 2 compteurs asteroid par joueur`
      (reste **vert sous substitution, assumé**, base automatique, aucun
      module ne la porte, voir preuve commune) +
      `ih004 … l'action retire X compteurs, X = le meilleur pouvoir`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

---

## Necroverse (`nv`)

### nv001 : Shadow Serpent (×2, 1 card_id)
- [x] Étape 2 : sbire 6 PV, MNG 2/ATQ 3, ★ attaques avec overkill, ★ Boost
      carte de rencontre face cachée.
- [x] Étape 5 : « attacks gain **overkill** » vérifié. Résultat : conforme.
- [x] Étape 6 : ATQ 3, 6 PV. Résultat : conforme.
- [x] Étape 7 : `nv001 … ses attaques gagnent overkill`. ⚠ Faux vert corrigé
      au portage : le cas d'origine vérifiait que l'allié tombait sous
      l'attaque (ATQ 3 contre 3 PV, ce qui arrive de toute façon SANS
      overkill) ; corrigé pour blesser l'allié d'abord (1 PV restant) et
      mesurer l'excès qui passe sur le héros : 2 dégâts avec overkill, 0 sans
      (journal §4).
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### nv002 : Annihilablade
- [x] Étape 2 : attachement sur le VILAIN (pas Gorr nommément : ce set est
      modulaire), +1 ATQ, ★ un allié vaincu par le vilain est retiré du jeu.
- [x] Étape 5 : « to the villain » → `CardFinder(card_type=Villain)`, jamais
      un nom propre. Résultat : conforme.
- [x] Étape 6 : +1 ATQ. Résultat : conforme.
- [x] Étape 7 : `nv002 … l'allie vaincu par le vilain est RETIRE du jeu`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### nv003 : Dark Apotheosis (×2, 1 card_id)
- [x] Étape 2 : attachement +1 ATQ/+1 MNG sur l'ennemi le plus solide.
- [x] Étape 5 : « the enemy with the most hit points **REMAINING** » : les PV
      restants, pas imprimés (`max(ennemis, key=health)`, un vilain blessé
      peut céder la place à un sbire frais). Résultat : conforme.
- [x] Étape 6 : +1/+1. Résultat : conforme.
- [x] Étape 7 : `nv003 … s'attache a l'ennemi le plus solide`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### nv004 : Manifest Will
- [x] Étape 2 : remélange les sbires de la défausse, en révèle un.
- [x] Étape 5 : filtre par TYPE (Minion), pas par trait. Résultat : conforme.
- [x] Étape 6 : aucun nombre propre. Résultat : conforme.
- [x] Étape 7 : `nv004 … remelange les sbires de la defausse et en revele
      un`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### nv005 : The Ingenuity of Hatred
- [x] Étape 2 : jumelle de `nv004`, mais sur les attachements.
- [x] Étape 5 : filtre par TYPE (Attachment). Résultat : conforme.
- [x] Étape 6 : aucun nombre propre. Résultat : conforme.
- [x] Étape 7 : `nv005 … meme chose pour les attachements`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### nv006 : The Planet Cleaver
- [x] Étape 2 : complot annexe, Hinder 2 par joueur, icône Hasard tant qu'il
      est en jeu.
- [x] Étape 5 : « 1 carte de rencontre face cachée de plus par joueur » EST
      la définition de l'icône Hasard, mais `desc.Hazard` ne s'applique qu'à
      la révélation de la carte QUI LE PORTE ; ici c'est une Interruption
      Obligatoire permanente tant que le complot est en jeu, donc donnée par
      `ThisGainKeyword(hazard=1)` plutôt que la base automatique. Résultat :
      conforme, écart de montage documenté et sans conséquence observable
      (même effet final).
- [x] Étape 6 : Hinder 2. Résultat : conforme.
- [x] Étape 7 : `nv006 … Hinder 2 par joueur et icone Hasard`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

---

## Bilan

**10 cartes sur 10** ont un cas de test sujet, une preuve par substitution
(sauf `ih004`, contre-cas d'absence assumé pour sa seule partie « base
automatique »), et la preuve commune d'autoplay au niveau du set. Aucune
limite « once per X » dans ces deux sets : l'étape 7 bis ne s'applique à
aucune carte.

Reste dû, non caché : aucune partie n'a été jouée par un humain dans le
navigateur avec ces deux sets actifs.

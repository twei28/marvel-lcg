# Crisis

**Texte imprimé / définition** : « Crisis. » Un schéma annexe avec ce mot-clé force une réponse immédiate du joueur : il doit être vaincu avant que le threat puisse être retiré du schéma principal. Le compteur `Crisis` (`1`, `2`, ...) fixe le nombre de charges de crise.

**Mécanisme moteur** : clé `desc.Crisis` sur la carte, lue nativement par le moteur. `CanCrisis` (`src/game/card/face/attribute/has_crisis.py`) enregistre l'attribut `Crisis` -> `printed_crisis`, restaure la valeur à chaque `OnResetKeywords` via `GainCrisis`. Quand un schéma Crisis entre en jeu, `SetCrisisEffectedBy()` marque le complot principal comme affecté (`scheme.card.ui.SetEffectedBy(diff, GameRule(self))`). Le blocage réel se joue dans `CardFace.RemoveThreatFromSchemes` (`src/game/card/face/card_face.py`) : sa signature porte un paramètre `ignore_crisis` que le moteur enregistre via une règle temporaire (`AbilityFactory.UnitIgnoreKeywordIcons(..., crisis=True)`) quand une carte veut explicitement passer outre. C'est donc un vrai contrôle côté moteur, intégré à la fonction de retrait de menace elle-même, pas une simple restriction d'affichage. **Aucun script requis** pour ce mot-clé lui-même : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01108` : Crowd Control (`desc` contient `"Crisis": "1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier `01108.py` trouvé dans `src/cards/pack` : cette carte ne porte que le mot-clé Crisis, sans capacité imprimée annexe.

**Pièges connus** : Crisis bloque le retrait de menace sur le complot principal au niveau de `RemoveThreatFromSchemes` lui-même, pas via une règle de perte de PV. Une carte qui veut explicitement l'ignorer doit passer `ignore_crisis=True` à cet appel. Ne pas confondre avec Peril, qui agit de manière similaire mais sur un autre déclencheur. Si une future carte cumule Crisis avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Crisis lui-même.

## ⚠ MISE À JOUR DU 11/09/2026 : la Crise verrouille désormais la CIBLE

La description ci-dessus était exacte mais **incomplète**, et cette lacune a
coûté une partie à un joueur. Jusqu'à cette date, la Crise ne bloquait qu'**à
la résolution** : le complot principal restait proposé comme cible d'un
contre, le joueur y jouait sa carte, et `RemoveThreatInternal` rendait 0. La
carte partait en défausse sans rien faire, sans un mot. Le joueur a annulé et
rejoué le même coup trois fois avant de signaler le problème.

Or ses deux sœurs verrouillent **au ciblage** :

| Mot-clé | Où il verrouille |
|---|---|
| Garde | `Villain.CanBeAttackBy` (`base/villain.py`) |
| Patrouille | `MainScheme.CanBeThwartBy` (`card_type/scheme_main.py`) |
| **Crise** | **`MainScheme.CanBeThwartBy`, depuis le 11/09/2026** |

Le complot principal n'est donc plus offert à un contre tant qu'une icône de
crise est en jeu. La condition est **identique** à celle de la résolution
(`Worlds.GetCrisisFaces(...)` et `IsIgnoreKeyword('Crisis', ...)`), sans
`IsPlayerInitiator()` : une divergence entre ce que le moteur propose et ce
qu'il résout serait pire que le trou d'origine.

### Conséquence pour une carte qui ignore la Crise

`ignore_crisis=True` passé à `RemoveThreatFromSchemes` n'agit qu'à la
résolution, donc **trop tard pour le ciblage**. Une carte qui est un
**contre** (`SetLabel('thwart')`) doit en plus le **déclarer** sur sa
capacité :

```python
.SetIgnoreKeyword('Crisis')
```

C'est ce que lit `IsIgnoreKeyword` au moment du calcul des cibles légales.
Les cartes qui retirent de la menace par une **Action** (et non un contre) ne
sont pas concernées : elles ne passent pas par `CanBeThwartBy`.

⚠ **Gate dédiée** : `tools/verifier_ignore_crise.py` échoue si un contre
ignore la Crise sans la déclarer. Calibrée en retirant la ligne de `90119`.

### Les deux cartes alignées ce jour-là

- **`90119` Search and Rescue** (pack `rescue_rainy`) : le seul vrai contre du
  dépôt à ignorer la Crise. Les six autres cartes à `ignore_crisis=True` sont
  des Actions.
- **`15012` Crisis Averted** (pack `scw`) : le cas limite. Elle n'ignore la
  Crise **que si elle a été payée avec une ressource mentale**, or le paiement
  vient APRÈS le ciblage (`effect_checker` : `check_target` puis `check_pay`).
  Son ignorance est donc déclarée avec **`paid_with="B"`** (voir ci-dessous) :
  vraie tant que rien n'est payé (la carte reste ciblable), tranchée à la
  résolution selon les ressources réellement dépensées. Payée sans mental
  sous une Crise, elle ne retire donc rien : c'est le texte de la carte, et
  le plateau **demande confirmation** avant d'envoyer un tel paiement.
  ⚠ Cette carte avait été **ratée par un grep** sur `ignore_crisis=True` :
  elle passe par une variable locale. C'est la gate qui l'a trouvée.
- **`hc006` On the Prowl** (pack `hellcat`) : même famille, variante « using
  **only** [mental] » : `paid_with="B", only=True` (`OnlyHasColor`), sur
  `'Crisis'` et `'Patrol'`. ⚠ La première gate ne la voyait pas
  (`ignore_crisis=mental`, une variable) ; corrigée le 11/09/2026 au soir.

### L'ignorance qui dépend du paiement : `paid_with` (11/09/2026 au soir)

```python
.SetIgnoreKeyword('Crisis', paid_with="B")              # au moins une mentale (15012)
.SetIgnoreKeyword('Crisis', 'Patrol', paid_with="B", only=True)  # rien d'autre (hc006)
```

`Ability.SetIgnoreKeyword` construit la condition (rien de payé, ou la
couleur ; joker compris) **et** la garde dans `AbilityIgnore.paid_with` /
`paid_only`. Au rendu d'une option (`Effect.Render`, `get_warning`), si la
cible est un complot principal verrouillé par ce mot-clé, le descripteur
porte `target_payment[*].warning = {"keyword", "paid_with", "mode"}`. Le
plateau (`ask.ts`, `coupSansEffet`) compare les lettres du paiement choisi et
ouvre une **confirmation** (`ConfirmationJeu`, Continuer / Annuler, FR et EN)
si aucune ne convient ; il ne connaît ni la carte ni la règle. Décision
utilisateur du 11/09/2026 : prévenir au moment de payer, par une modale, le
moteur calcule.

⚠ **Ne jamais écrire cette condition à la main** (`condition=lambda effect:
effect.GetPaidResources()...`) : la règle serait la même, mais le rendu ne
saurait rien, et le joueur perdrait sa carte sans un mot. La gate
`verifier_ignore_crise.py` refuse cette forme dès que la lambda lit le
paiement (`br002`, dont la condition ne lit pas le paiement, reste libre).
Harnais : trois cas « MODALE » (15012 sous Crise, témoin sans Crise, témoin
fort payé sans mental) plus un cas hc006 en mode `only`.

### Côté plateau

Le complot principal porte une pastille rouge « Crise » tant qu'une manigance
annexe à Crise est en jeu, et l'aperçu au survol nomme la manigance
responsable (`zones.ts`, `avecCrise` ; `ScanCard`, `pastille-crise`).

**Variantes maison** : aucune recensée pour l'instant.

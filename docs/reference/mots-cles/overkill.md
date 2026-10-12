# Overkill

**Texte imprimé / définition** : « Overkill. *(Excess damage from this attack
is dealt to the villain / to the enemy's side.)* » Les dégâts excédentaires
d'une attaque qui abat sa cible sont reportés : sur le vilain si c'est un
joueur qui attaque un sbire, sur l'identité du joueur si c'est un ennemi qui
abat un allié.

**Mécanisme moteur** : propriété booléenne `overkill` de la dataclass des
propriétés d'attaque (`src/game/card/face/attribute/can_attack.py`). Elle se
donne de deux façons :
- statiquement, via les paramètres `overkill=True` des fabriques d'attaque
  (`AbilityFactory.DoAttack` et parents, `src/game/ability/factory/do_attack.py`) ;
- dynamiquement, en cours d'attaque, via `message.GainOverKill(effect)` sur le
  message d'attaque (`src/game/message/sender/sender_damage.py` et
  `sender.py`) — c'est le chemin des textes « this attack gains overkill ».
Le report des dégâts est calculé dans la résolution des dégâts d'attaque
(`include_overkill` dans `src/game/ability/factory/damage.py`).

**Carte exemple** : `an013` (* Hel-Wolf) : « [star] Boost: This attack gains
overkill » rendu par `attaque.GainOverKill(effect)` dans le handler
`WhenCardBecomeBoost`, sur le modèle de `01099` (attaché à Rhino). Côté
joueur : `01053` Relentless Assault (« this attack gains overkill » selon le
paiement).

**Pièges connus** :
- Overkill ne s'applique qu'aux dégâts D'ATTAQUE : un effet « deal X damage »
  hors attaque ne reporte jamais rien.
- Sur un texte de boost, l'attaque visée est `message.would_atk_message` du
  message `WhenCardBecomeBoost` : la récupérer avec `getattr(..., None)` car
  la carte peut être révélée hors attaque (plan du vilain).

- **Aucune question à poser** (RR 1.8 p.31, signalement du 12/10/2026). L'excédent
  va au méchant (sbire vaincu) ou à l'identité du contrôleur (allié vaincu), sans
  rien demander. Le moteur posait pourtant « Simultaneous Overkill » à chaque
  excédent : l'ordre de traitement entre la cible vaincue et la cible de
  l'excédent (`can_health.py`, `TakeDamageWithOverkillTarget`). Corrigé : cet ordre
  n'est demandé que si les DEUX sont vaincues par le même coup.
- **Plusieurs méchants en jeu** : l'excédent va au méchant ACTIF (compteur
  `active`). FAQ RR 1.8 p.62 (Sinister Six) : « The villain with the active counter
  takes the overkill damage ». Étendu à TOUS les scénarios à plusieurs méchants,
  Wrecking Crew compris : **décision de l'utilisateur du 12/10/2026 pour Wrecking
  Crew, sans ruling officiel**. Le moteur le faisait déjà (`Worlds.FindVillain` →
  `Scenario.GetVillain`, qui renvoie le méchant `IsActive()` en premier).
- Cas : « Overkill [regle] » dans `tools/test_capacites.py` (un méchant, deux
  défaites simultanées, Sinister Six, Wrecking Crew, ennemi sur un allié).

**Variantes maison** : `ho016` (* Bullseye, pack `harry_osborn`) : « [star]
Bullseye's attack gains piercing and overkill » — capacité étoile (Expert),
pas un boost.

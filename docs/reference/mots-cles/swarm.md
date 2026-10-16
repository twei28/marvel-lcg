# Swarm

**Texte imprimé / définition** : `SWARM` est un TRAIT (ligne de traits
« MOUSERS. SWARM. » et « AERIAL. FLYBORGS. SWARM. ») et la capacité imprimée
tient en trois phrases, identiques sur `td016` et `td017` : « Enters play with
N swarm counters on them. [star] This minion's SCH, ATK, and hit points are
equal to the number of swarm counters here. Forced Interrupt: When this minion
takes any amount of damage, remove that many swarm counters from here
instead. » Ce n'est donc PAS un mot-clé à effet propre : la mécanique vit dans
le texte de chaque carte, le trait ne sert qu'à les regrouper.

**Mécanisme moteur** : compteur `swarm` ajouté à l'énum `COUNTER` de
`src/game/card/face/card_face.py` ; tout est dans `CapacitesEssaim(n)`
(`src/cards/pack/donatello/donatello_nemesis/__init__.py`), partagé par td016 et
td017 : entrée en jeu avec N compteurs (`ThisEnterPlayWithCounters`) ; SCH, ATQ
**et PV** égaux au nombre de compteurs par `ThisGainKeyword(fn, attack=1,
scheme=1, health=1, change_on_event=OnEvent.Counter("This", "swarm"))` (modèles
`27067` Sand Clone pour ATQ/SCH, `gorr/gb009` et `sk178` pour les PV) ;
dégâts remplacés par un retrait de compteurs par `WhenUnitWouldTakeDamage(
ForcedInterrupt, "This", op)` + `message.SetBeInstead(effect)`.

**PV dynamiques, aucune mort à la main** (décision utilisateur du 15/10/2026,
réalisée le 16/10/2026) : `desc.HP = "0"`, les PV viennent des compteurs. Quand le
dernier compteur part, PV = compteurs = 0 et `CanHealth.LimitHealth` vainc le
sbire comme pour une santé épuisée. Le module ne contient aucun appel de défaite.

**Carte exemple** : `td016` Plague of M.O.U.S.E.R.s et `td017` Flight of
Flyborgs (`src/cards/pack/donatello/donatello_nemesis/`).

**Pièges connus** :
- les dégâts sont REMPLACÉS : un coup de 10 sur 2 compteurs ne reporte aucun
  excédent (Overkill) sur le méchant ; mesuré, cas `td017 ... 10 degats d'un coup` ;
- la mort passe par `LimitHealth` (tueur `None`) : pas de message
  « AfterUnitDefeatedUnit », donc les réponses « after you defeat » d'un héros ne
  partent pas sur un essaim (limite du moteur, non mesurée sur une carte réelle) ;
- le disque orange du coin du scan est les PV, pas le boost (vérifié contre
  `01167` Vulture) : PV « ★ » ici ; le boost est la marque rouge du coin inférieur
  droit.

**Variantes maison** : aucune autre que ces deux cartes.

## Scénario Baxter Stockman (16/10/2026) : le même mécanisme, trois variantes de compteur

`tx007` Plague of M.O.U.S.E.R.S. (2 swarm) et `tx012` Flight of Flyborgs (4 swarm) reprennent mot pour mot td016 / td017 :
elles appellent `CapacitesEssaim(n)` (importé du pack donatello). Trois sbires du même trait SWARM ont leur compteur NOMMÉ :
`tx013` Superfly (ooze : SCH et ATQ égales aux compteurs, PV imprimés 5, pas de « retirez plutôt »), `tx015` Roadkill
Rodneys (cable : +1 ATQ par compteur, Réponse forcée qui les retire tous), `tx017` Auto Defense Bots (shield : défaite
évitée tant qu'il en reste). La manigance `tx004b` leur pose un « all-purpose counter » du bon type : fiches
`replicate.md` et `all-purpose-counter.md`. Compteurs `cable`, `shield`, `ooze` ajoutés à l'énum `COUNTER`.

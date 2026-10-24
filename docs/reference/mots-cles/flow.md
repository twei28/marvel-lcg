# Flow — MOT-CLÉ MAISON (Shang-Chi, DesignHacker, `ch`)

**Texte imprimé / définition** (carte `ch002` State of Flow) :

> « **Keyword - Flow**: Look at the top card here. If a printed resource on that card matches the resource required by the
> "Flow" ability, you may also resolve its effects. »

Chaque événement ATTACK de Shang-Chi imprime, après son Hero Action, une ligne « **Flow** : [ressource] → effet ». Le « top card
here » est le dessus de la pile de State of Flow : la DERNIÈRE attaque jouée (« After you play an ATTACK event, place it faceup on
top here »). Chi Mastery (`ch001a`) : « After you resolve a "Flow" ability, ready Shang-Chi. »

**Arbitrages utilisateur (24/10/2026, scans à l'appui)** :
- **Correspondance STRICTE** : un wild ne vaut que wild, un poing que poing, une énergie que énergie. La carte du dessus peut
  imprimer DEUX icônes (Throat Punch 1/15 = poing + mental) : UNE seule suffit.
- **Les impressions « copy » du zip ne sont PAS des doublons** : même dessin, icône(s) de ressource du coin différente(s). Flow lit
  cette icône : 12 événements = 6 titres × 2 impressions = 12 `card_id` distincts (`ch003`-`ch014`).
- **Special Delivery** : « play the next ATTACK event from your hand at no cost » = COÛT DIFFÉRÉ (le prochain ATTACK que le joueur
  joue ce tour coûte 0), pas un jeu immédiat.
- **Meditate** (`ch001b`) : « shuffle a card from State of Flow » = UNE carte AU CHOIX de la pile.

**Mécanisme moteur** : aucune primitive officielle, un helper de set + UN message ajouté.

- pile : `State of Flow` est mis de côté (`BeginGameWithSetAside(["ch002"])` sur `ch001b`) et entre en jeu au Setup
  (`WhenCardSetup`, modèle Storm `36001b`) ; les attaques jouées sont posées FACE VISIBLE dessous par
  `hote.PlaceCardHere([face], True, effect)` (Forced Response `AfterPlayerPlayedCard`, l'événement a déjà été défaussé par
  `Event.OnAfterPlay` : on le retire de la défausse). La pile se lit par `hote.GetPlacedCardArea().Get()`, le DESSUS est le DERNIER ;
- remélange : `AbilityFactory.AfterDeckRunOut(ForcedResponse, deck_du_joueur, op)` → `Faces.ShuffleAllTo(pile, player_deck)` ;
  le moteur remélange ensuite la défausse avec sa pénalité habituelle (règle `try_shuffle_deck`) ;
- lecture : `AccepterFlow(effect, joueur, 'R'|'B'|'Y'|'G')` (set `shang_chi/shang_chi/__init__.py`) lit
  `dessus.printed_resource_internal.HasColorPrinted(res)` (jamais `printed_resource`, qui passe par un message de comptage, ni
  `HasColor`, qui convertit le wild), puis propose « Resolve the Flow ability » par `MayChooseOneAbility` (option « Cancel ») ;
- déclencheur : `FlowResolu(joueur, carte)` envoie `Message.AfterPlayerResolveFlow` (`sender_player.py`), que
  `AbilityFactory.AfterPlayerResolveFlow` (`factory/setup.py`) écoute — modèle `AfterPlayerResolveMulligans` (Beast).

**Carte exemple** : `ch009` Dragon Strike (le Flow est résolu AVANT les dégâts : il modifie l'attaque,
`AttackProperty(piercing=True, ranged=True, overkill=True)`) ; `ch007` Special Delivery (Flow APRÈS les dégâts : « if this attack
defeats an enemy », puis `Worlds.UpdateNextCardPlayCost(..., update_to=True, in_this="Turn")`).

**Pièges connus** :
- le dessus de la pile est lu AU MOMENT du Flow : l'événement en cours n'est posé sur la pile qu'APRÈS (Forced Response), il ne
  peut donc jamais activer son propre Flow ;
- `ChooseAbilities(..., forced=False)` ne propose PAS de « Cancel » dans le harnais : employer `MayChooseOneAbility`
  (`choisir_option="Cancel"` pour refuser) ;
- `Puzzle.PlaceUnder('<attaque>', 'ch002', face_up=True)` garnit la pile, la DERNIÈRE posée est le dessus ;
- Hydra Mercenary (`01101`) a GUARD : avec lui engagé le vilain n'est pas ciblable — choisir Shocker `01103` pour les cas ;
- Sandman (`01102`) entre en jeu avec Tough, Vulture (`01167`) attaque à l'engagement : éviter pour mesurer des dégâts ;
- `AttackProperty` n'a pas `indirect_damage` : `this.DealIndirectDamage(identite, n, effect)` (Downtown Attack).

**Variantes maison** : aucune autre carte ne l'emploie.

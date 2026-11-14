# Active hero / Inactive hero (heros a PV partages, maison, The Warriors Three)

**Texte imprime / definition** : « Active hero. To change to alter-ego, flip The Warriors Three. » (faces HEROS wt001a/c/d) et
« Inactive hero. Permanent. Setup. » (soutiens PERSONA wt003-wt005). Les Warriors Three ont PLUSIEURS heros qui partagent les points de
vie ; « change your active hero » retourne le heros actif sur sa face inactive et un autre heros inactif sur sa face active. On ne change
de heros actif QUE si une carte le permet (carte-titre wt002, Leap into Action wt015). Les activations du mechant et les effets de carte
traitent TOUJOURS le heros actif comme l'identite et les heros inactifs comme des soutiens.

**Mecanisme moteur** (conception du pack, 26/10/2026) :
- UNE identite a QUATRE faces (`"hero": ["wt001a,wt001b,wt001c,wt001d"]` : Fandral, alter ego, Hogun, Volstagg, comme les formes de Wasp
  `hp001a-c` et de Conan `cn001a-e`). « Changer de heros actif » est donc un CHANGEMENT DE FORME : les PV (de l'identite) sont partages.
- Les trois heros INACTIFS sont des SOUTIENS PERSONA (`desc.Setup`, `Permanent`) du `hero_deck`, mis en jeu au Setup. Celui du heros ACTIF
  reste en jeu mais n'en est pas un (`soutiens_persona`, `inactif(nom)` dans `warriors_three/__init__.py`).
- La carte-titre wt002 (Permanent, Setup) porte « Hero Action: exhaust this card → change your active hero » et la synchronisation des etats :
  `WhenUnitWouldChangeForm` memorise le heros actif AVANT (`noter_le_heros_avant`), `AfterUnitChangeForm` echange l'etat PRET/EPUISE
  de l'identite avec celui du soutien du heros qui s'efface / s'active (`synchroniser_formes`) : « Heroes remain ready or exhausted when they
  flip » (donc plusieurs activations de heros par tour).
- **CORRECTIF `player_setup.py`** : une face HEROS qui imprime « Active hero. » ne propose PAS le « Change To <autre heros> » libre ; seul le retour
  a l'alter ego reste libre (une fois par tour) et l'alter ego propose les trois heros. Lecture du texte imprime, comme « You can only change
  form by card abilities » (Wasp).

**Carte exemple** : `wt002` (carte-titre), `wt015` Leap into Action (`changer_de_heros`), `wt003-wt005` (soutiens), `wt007-wt009` (armes :
« After <heros> becomes the active hero » = `AfterUnitChangeForm(HeroResponse, "You", ..., conditions=[message.trigger.IsName(...)])`).

**Pieges connus** :
- `Puzzle.ChangeForm(card)` ne designe PAS une face : il fait basculer l'identite vers « l'autre forme » (alter ego → derniere face heros,
  heros → alter ego). Pour un changement de heros avec messages, passer par la capacite du pack (`Puzzle.Action('wt002', 'HeroAction', 0)`).
- `AskChooseOneText` du choix de heros est TRIE par nom (Fandral, Hogun, Volstagg) : le pilote du harnais prend le premier.
- **Cartes d'etat (arbitrage du 26/10/2026, notice de l'auteur)** : chaque heros garde les siennes. Quand un heros devient inactif, ses cartes d'etat
  passent dans la zone d'etat de SON SOUTIEN (`soutien.components.status.deck`) et reviennent sur l'identite quand il redevient actif ; celles de
  la carte-titre (presentes quand le heros devient actif) restent sur l'identite pour tous (`synchroniser_cartes_d_etat`, `warriors_three/__init__.py`).
  « Give Volstagg a tough status card » avec Volstagg inactif la pose sur son soutien (`donner_etat_a_un_heros`).
- Le soutien du heros ACTIF n'est pas un soutien (notice, face A) : `soutiens_persona` l'exclut pour Rally! et Fated Clash. ECART : un effet GENERIQUE
  « un soutien » d'une autre extension le voit encore (la carte reste en jeu).
- `state.is_ready` s'ecrit directement (`card.state.is_ready`) : aucun message `AfterCardReady/Exhausted` n'est envoye par l'echange.

**Variantes maison** : seule la famille « Warriors Three » (pack `wt`).

# Insensible aux cartes joueur (CIBLÉ / TARGETED, HIDDEN)

**Texte imprimé / définition** :
- Punisher MC×DC 2026, p183 *In the Crosshairs* (attachement, trait *Targeted*) : « Attached character gets +5👤 hit
  points, gains the TARGETED trait, and cannot be affected by player cards. »
- Galactic Storm 1.2 p.14, trait HIDDEN (Hala Ultimatum) : « players cannot affect the villain with player cards.
  That includes attacking the villain with either heroes or allies, dealing damage to the villain through overkill
  when a minion is defeated with excess damage, placing a status card on the villain, and attaching upgrades or
  other player cards to the villain. Players also cannot discard tough status cards from the villain by performing
  an attack with piercing or by any player card ability that would discard a tough status card from the villain.
  If a card ability has multiple targets and one of them is the villain, players may only play that card or initiate
  that ability if there is at least one other valid target for the effect. If a card or ability has only one target
  and that target is the villain, that card cannot be played and the ability cannot be initiated. »
- « Carte joueur » au sens du Rules Reference 1.8 p.33 : allié, événement, identité, manigance de joueur, ressource,
  soutien, amélioration. L'identité en est une : l'attaque de base du héros est refusée elle aussi.

**Mécanisme moteur** : brique commune du 20/10/2026, `src/game/operate/immunity.py` (`PlayerCardImmunity`). Une
protection (source, porteur) est inscrite sur le monde quand la source entre en jeu, par la fabrique
`AbilityFactory.CannotBeAffectedByPlayerCards(which, while_fn=None)` (`ability_factory.py`) ; elle vaut tant que la
source est en jeu sur cette face. Sept accroches, toutes commentées « BRIQUE 2 » : cibles légales (`selector.py`),
dégâts dont l'excès d'overkill (`can_health.py` `TakeDamageNoDeath`), poser un état (`GainStatus`), défausser un
état dont le Robuste par perforant (`LoseState`), bonus/mots-clés (`face_gain.py`), attacher une carte joueur
(`asset.py`, `can_attach.py`), compteurs (`faces.py` `PlaceCountersOn`). Recette : `RECETTES-MOTEUR.md` §16.2.

**Carte exemple** : aucune carte portée à ce jour. Montage prévu :
- p183 : `AbilityFactory.CannotBeAffectedByPlayerCards("AttachedCharacter")` dans `GetAbilities()` de l'attachement ;
- Hala : `AbilityFactory.CannotBeAffectedByPlayerCards("This", while_fn=lambda face: face.HasTrait("HIDDEN"))` sur
  chaque face de stade.
Cas : `tools/cas/briques_communes.py`, filtre `[briques][immunite]` (14 cas).

**Pièges connus** :
- La DÉFENSE de base du héros reste permise : elle désigne l'attaquant comme cible (`SetTarget("Attacker")`) sans
  l'affecter ; elle est reconnue à son `func_names` « DEF ».
- Tout ce qui vient d'une carte RENCONTRE passe : Rachel Cole-Alves (p195) attaque le CIBLÉ, Bullet Spray (p203)
  le blesse, Flash-Bang (p207) l'étourdit. Seule la source de l'effet compte (`effect.this`), pas le joueur qui le
  résout.
- `HIDDEN` et `TARGETED` ne sont pas encore dans l'énum `TRAITS` (`card_face.py`) : les ajouter avec les données.
- La moitié « attaque » de HIDDEN (« whenever a player would be attacked by the villain, that player is dealt a
  facedown encounter card ») et la face DISCOVERED ne font PAS partie de cette brique (second temps, lot GS-6).
- Une source mise en jeu sans passer par l'entrée en jeu (pose brute) ne protège rien : la fabrique écoute
  `AfterCardEnterPlay`.

**Variantes maison** : les écureuils de Squirrel Girl (`sg002`-`sg007`) ont une immunité voisine (« Cannot be affected
by player card abilities other than abilities on Squirrel Girl cards »), écrite avant cette brique par les
accroches `refuse_target_fn` / `refuse_gain_fn` posées sur la face (`squirrel_girl/__init__.py`). Les deux coexistent.

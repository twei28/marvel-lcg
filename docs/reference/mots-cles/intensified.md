# Intensified (Intensifié) et « intensify »

**Texte imprimé / définition** : carte d'état maison TMNT (Inkwire), fournie par
l'utilisateur le 16/10/2026 (capture Discord du serveur Bebop & Rocksteady,
`.planning/tmnt/intensified-capture.webp`, réponse à la question Q2 de
`.planning/tmnt/shredder-questions.md`) : « The next time this character would
discard a status card, discard this status card instead. This card cannot be given
to a character that has no status cards. » Verbe de carte : « intensify X » = donner
une carte Intensified à X. Nom français : **Intensifié** (verbe « intensifiez »).

Traduction retenue : « La prochaine fois que ce personnage devrait défausser une
carte d'état, défaussez cette carte d'état à la place. Cette carte ne peut pas être
donnée à un personnage qui n'a aucune carte d'état. »

**Mécanisme moteur** : septième carte d'état, recette de `dazed.md` / `cloaked.md` :

| Endroit | Ce qu'il a fallu |
|---|---|
| `data/cards.json`, pack `status` | `{"card_id": "intensified", "type": "Status", "name": "Intensified"}` + checksum |
| `CardFace.STATUS` (`card_face.py`) | `"Intensified"` |
| `StatusCard.symbol_name`, `Symbol` | `intensified` |
| `Status` (`component/status.py`) | `INTENSIFIED_FINDER`, `intensified`, compteur `vidage` + contexte `SansRemplacement()` |
| `CanStatus` (`attribute/can_status.py`) | `intensified`, `IsIntensified`, `CanbeIntensified` (au moins une carte d'état), `DiscardIntensified`, `HasStatus("Intensified")`, `DiscardEachStatus` (vidage, l'emporte aussi), fenêtre te201 dans `GainStatus` |
| `checker.py`, `ability.py` | `has_status` / `canbe_status` / `SetTarget(name="Intensified")` |
| `Puzzle.Intensify(card, n)`, `Puzzle.AddStatus(card, nom, n)` | poser l'état (sans bascule) dans un cas de test |
| `src/cards/pack/status/intensified.py` | le remplacement de défausse |
| UI | `effets-statuts.ts` (badge), `mobile/etats.ts` (lettre I, « Intensifié », classe `est-intensifie`), `ScanCard.tsx`, texture `assets/textures/intensified.webp` (recadrée de la capture) |

**Le remplacement** : `intensified.py` écoute `WhenCardWouldDiscard` (message diffusé,
`CanBeInstead`) pour toute AUTRE carte d'état du MÊME porteur, et fait
`SetBeInstead` + défausse d'elle-même. Un seul crochet couvre tous les chemins de
défausse d'un état (`LoseState` de Sonné / Désorienté / Coriace / Exposé,
`Faces.DiscardAll([carte])` de Camouflé / Hébété, perforant, cartes de joueur qui
retirent un état) : modèle `skrull_menace/paibok/__init__.py`.

**Lecture codée (À CONFIRMER, voir « Questions »)** :

- l'EFFET de la carte d'origine a lieu, seule sa DÉFAUSSE est remplacée : Sonné annule
  quand même l'attaque, Désorienté la manigance, Coriace prévient les dégâts, Exposé
  ajoute ses dégâts, Camouflé ses +2, Hébété ses −2 ; la carte d'origine reste et
  resservira (c'est l'intérêt de te201) ;
- une défausse de PLUSIEURS cartes d'un coup (« discard all Exposed », lot Hébété +
  Camouflé, Sonné ×2 d'un Steady) : chaque Intensified remplace UNE carte (« a status
  card »), les autres partent. Deux Exposé + une Intensified : +2 dégâts, un Exposé reste ;
- **pas de plafond** : rien d'imprimé, plusieurs Intensified s'empilent (te201 en pose une
  à chaque doublon) ; chacune remplace une défausse ;
- « a character that has no status cards » : `GetStatusSize() == 0` ; une Intensified
  posée compte elle-même comme carte d'état (une 2e Intensified est donc toujours légale).

**Exclusions** (ne sont pas « ce personnage défausse une carte d'état ») :

- la défausse d'une autre Intensified (sinon deux Intensified se remplacent en boucle) ;
- le VIDAGE de la zone d'état : le porteur quitte le jeu / se réinitialise
  (`Status.OnDiscard`, `OnParentReset`) ou « défaussez chaque carte d'état »
  (`DiscardEachStatus`) : tout part, Intensified comprise ;
- les purges de RÈGLE : Coriace au-delà de `tough_max` (`card.py`,
  `factory/status.py`), gain de Stalwart (`has_stalwart.py` : sans cette garde,
  `stunned.py` trouverait un Sonné sur un Stalwart et son `assert` tomberait).

**Carte exemple** : `te201` Intense Combatants (environnement optionnel, TMNT Intense) :
« When a status card would be placed on a character, if that character already has 1 copy
of that status card on them, intensify them instead. » Fenêtre dédiée
`Message.WhenStatusWouldCardPlaceOnAgain`, envoyée par `GainStatus` AVANT les plafonds
(un second Sonné est sinon refusé par `CanbeStunned` en silence), fabrique
`AbilityFactory.WhenUnitWouldBeStatusAgain`. Distincte de `WhenStatusWouldCardPlaceOn`
pour que 56175 / ah006 ne voient pas une pose que le plafond aurait refusée.

**Pièges connus** :

- Intensified elle-même n'ouvre jamais la fenêtre te201 (sinon la 2e Intensified boucle) ;
- `Puzzle.Stun` / `Tough` / `Cloak` / `Daze` BASCULENT : le second appel passe par une
  défausse, qu'une Intensified remplacerait. Pour un doublon, `Puzzle.AddStatus` ;
- le perforant défausse Coriace avant les dégâts : avec une Intensified, c'est elle qui part
  et Coriace RESTE (les dégâts perforants passent quand même : `ignore_tough`) ;
- non mesuré : un sbire vaincu qui porte Sonné + Intensified (le vidage est codé, aucun cas
  ne le mesure ; l'autoplay ne pose jamais d'Intensified, te201 n'étant dans aucun ensemble).

**Variantes maison** : aucune.

**Preuves** : `tools/cas/intensified.py` (16 cas `[intensified]`, 8 cas `[te201]`). Preuves
par substitution : `intensified.py` retiré → les 8 cas de remplacement + la chaîne te201
ROUGES ; `CanbeIntensified` sans condition → « ne peut PAS être donnée » ROUGE ; garde
`vidage` retirée → cas « défaussez chaque carte d'état » ROUGE ; `te201.py` retiré → 4 cas
te201 ROUGES. Contre-cas d'absence assumés verts sous substitution (témoins, pose, « pas de
boucle »).

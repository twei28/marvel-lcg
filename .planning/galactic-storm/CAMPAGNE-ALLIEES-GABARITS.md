# Galactic Storm : les 13 cartes de campagne (gs224-gs236)

Gabarit PROCESSUS-CARTE.md en cours. Scans relus un par un (dossier
`docs/packs/galactic-storm/sources/.../Campaigns/Galactic Storm/`,
transcription `docs/packs/galactic-storm/transcriptions/campagne.md`).

**Étape 1 (entrée `cards.json`) : FAITE pour les 13 cartes**, script idempotent
`.planning/galactic-storm/defs/inserer_campagne_alliees.py`. Conventions
vérifiées contre les scans et contre `sk263-sk269` (Skrull Menace, même
auteur, même gabarit « carte de campagne ») :

- `desc.HP` = pastille orange (convention GS-0 Q6, déjà actée).
- `desc.THW`/`ATK` : une étoile à contour sous la stat = un `*` (dégâts
  consécutifs, convention GS-0 Q6). Compté à l'œil sur chaque scan, PAS
  supposé depuis la transcription (qui se trompait sur plusieurs cartes :
  Crystal/Goliath/Her/Captain Marvel/Living Lightning/Sersi n'ont EN FAIT
  aucune étoile, contrairement à ce que `campagne.md` laissait craindre).
- `desc.RES` : carré de couleur bas-gauche. Vérifié par découpe contre les
  mêmes conventions pack que gs172/gs173/gs12x (éclair = `Y` énergie, noeuds
  reliés = `B` mental, poing = `R` physique, étoile = `G` wild). Les 3 alliées
  BASIC ont chacune leur couleur propre (Rick Jones `B`, Gladiator `G`,
  Lauri-Ell `R`) ; les 10 alliées IDENTITY-SPECIFIC sont toutes `G` (wild).
- `desc.Class` : `"Campaign;Basic"` (224-226) ou `"Campaign;IdentitySpecific"`
  (227-236) — classes NATIVES du moteur (`card_player.py` `CARD_CLASS`), pas
  une invention : confirmé par `IsClass("IdentitySpecific")` déjà utilisé
  ailleurs dans le moteur.
- `desc.Requirement` (Crystal, `"YBR"`) : base automatique, `requirement.md`,
  aucun script.
- `[star]` devant une capacité (Lauri-Ell, Her) : footnote pure, convention
  Skrull Menace déjà actée (GS-0 Q6), gardée dans `text` mais sans effet code.
- **gs227 Binary, piège trouvé et corrigé avant commit** : la carte imprime
  « X » en ATK. `desc.ATK = "X"` aurait fait planter `int(value)` (parseur
  natif, `can_attack.py:81`). Corrigé en `desc.ATK = "0*"` + capacité
  `AbilityFactory.ThisGainKeyword` recalculant la vraie valeur, modèle
  `mw001a` Madame Web (commentaire du moteur lui-même : « Necessaire pour
  Madame Web mw001a (ATK/THW/DEF = X) » — précédent direct, même mécanique).

**Étape 2 (cartes de référence) : repérées pour 12/13 cartes**, pas encore
codées :

| Carte | Mécanique | Référence trouvée |
|---|---|---|
| gs224 Rick Jones | rediriger l'attaque du méchant vers Rick Jones | `hood/crossfires_crew/24026` Crossfire (`WhenUnitWouldAttack` + `message.ReplaceTarget(...)`) |
| gs225 Gladiator | après l'avoir joué depuis la main, vaincre un sbire | à préciser (trigger « play from hand » + `DefeatFace`) |
| gs226 Lauri-Ell | après avoir attaqué et blessé, défausser les boosts de la cible | à préciser (`AfterUnitAttackUnit` + dégâts > 0 + boosts sur la cible) |
| gs227 Binary | ATK = X (ressources énergie en main) | `mw001a` Madame Web (voir ci-dessus) |
| gs228 Captain Marvel | Resource : défausser Captain Marvel → générer YY | `core/iron_man/01033` Pepper Potts + `falcon/falcon/53006` (CanGenerateResources, CostFunc.Discard) |
| gs229 Crystal | When Defeated : payer 3 → remettre en jeu sous contrôle | à préciser |
| gs230 Doctor Pym | Alter-Ego Action : +1 à chaque pouvoir de base jusqu'à la fin du round | à préciser |
| gs231 Goliath | après pouvoir de base, défausser le dessus ; si [physical], 1 dégât à chaque ennemi | à préciser |
| gs232 Her | après son entrée en jeu, redresser une amélioration | à préciser |
| gs233 Living Lightning | après avoir quitté le jeu, défausser 2 ; par [energy] imprimé, redresser une carte | à préciser |
| gs234 Sersi | Action : s'épuiser + 1 dégât à elle-même + [mental] → remplacer un statut en jeu | à préciser |
| gs235 Spider-Woman | après avoir été défaussée DU DESSUS DE SON PROPRE DECK, étourdir jusqu'à 2 ennemis | **AUCUN précédent dans tout le dépôt** (grep exhaustif : rien sur « discarded from your deck » / « discarded from the top of your deck » dans aucun pack, officiel ou maison). Probable brique moteur manquante, pas une carte "normale" — à trancher avant de scripter. |
| gs236 Thor | après l'avoir joué depuis la main, 1 dégât par [energy] payé pour lui à chaque sbire engagé | à préciser (ressources de paiement : `GetPaidResources`/`paid_this_resources`, vu dans `card_player.py: SetPaidResources`) |

**Reste à faire avant de clore ce lot** : écrire `GetAbilities()` des 13
scripts (Étape 3), bloc texte-contre-code (Étape 5), bloc nombres (Étape 6),
cas de test par capacité avec preuve par substitution (Étape 7, y compris
témoin d'épuisement si besoin), autoplay ciblé (Étape 8), bloc plateau si la
carte change ce qu'on voit (Étape 8 bis — Her/Living Lightning/Sersi
attachent ou redressent des cartes, donc concernées).

Carte terminée (les 13) : NON — seule l'étape 1 (données) est faite et
vérifiée ; aucun script n'existe encore, `gs224`-`gs236` tombent donc en
« no_ga » (pas de capacité construite) dans `test_cards` (7006 ok / 0 err,
inchangé).

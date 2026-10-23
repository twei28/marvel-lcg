> **MISE À JOUR 23/10/2026 : FAIT, l'en-tête ci-dessous est périmé** (ancien état : « « RIEN CORRIGÉ », puis « Non déployé » »). Preuve : branche `luke-cage-correctifs` ancêtre de HEAD ; `2026-10-10-taches-en-pause.md` : déployé le 10/10 à 16h37 (« Luke Cage (9 cartes) ») ; réserves mineures : Sidewinder en multijoueur réel, ★ d'Augmented Jaws, doutes 62029 et 62014 (tri : `docs/rapports/etat-du-backlog-2026-10-19.md` §3, n°12).

# Luke Cage officiel (62xxx) : audit du 10/10/2026, RIEN CORRIGÉ (demande : vérifier d'abord)

Rapports d'Aghenatak du 10/10 (n°73, 74, 75, état « nouveau » sur le serveur) : les trois sont de VRAIS bugs,
pas des erreurs de jeu. Journaux et captures copiés dans le scratchpad de la session (perdus ensuite) ; les
relire dans `narwhal.db`, table `rapports`.

Règle de référence : Rules Reference v1.8, entrée Damage, ordre de résolution : 1. « would be DEALT » ;
2. cartes Tenace ; 3. « would TAKE ». Article FFG « Unbreakable » (11/06/2026) : le Bracelet sert à « conserver
ses Tenaces contre les sbires à faible ATQ » ; « les bracelets ne peuvent pas réduire le dégât imblocable de la
capacité de héros de Luke » ; Jessica Jones peut monter à 5 CTR.

## Prouvés par les journaux des rapports
- n°73 Power Man (62011) ne se déclenche jamais : `AfterStatusDiscardFrom(..., "This", "Tough")` = Tenace
  défaussé DE POWER MAN, et aptitude locale. Fogwell's Gym (`None` + DEFENDER) se déclenche bien, lui.
- n°74 Metal Bracer (62010) : accroché à `WhenUnitWouldTakeDamage` (étape 3), donc APRÈS le Tenace. Une attaque
  à 1 coûte un Tenace au lieu d'être réduite à 0. En plus, le moteur propose le Bracelet sur le dégât imblocable
  de Luke : il s'incline pour rien (le dégât passe).
- n°75 Jessica Jones (62002) : 4 Tenaces, CTR 1 au lieu de 5. `WhileValid(OnEvent.CardInPlay(Ally), ...)` ne
  recalcule qu'à l'entrée/sortie d'un allié, jamais quand un Tenace arrive ou part (`OnEvent.Status` existe).
- Même défaut, non signalé : Misty Knight (62013), bonus +2/+2 lié au Tenace sur `CardInPlay`.

## Trouvés à la lecture (agent d'audit, vérifiés dans le code ; non rejoués en partie)
- Cruisin' for a Bruisin' (62009) : pas de `CanPlayThisUpgradeCard(Minion)` → cible par défaut = TON identité ;
  le +2 ne vaut que pour les attaques de base.
- Take a Stand (62015) : `GainUntilPhaseEnd` tombe au premier `WhenPhaseEnd`, celui de la phase du méchant où
  l'on défend : le bonus ne sert jamais en phase des joueurs.
- Augmented Jaws (62031) : « +1★ ATK » imprimé (scan `assets/pics/62031.jpg`, marvelcdb) absent de
  `data/cards.json` ; et « Cottonmouth, sinon le méchant » codé en OU (peut aller au méchant malgré Cottonmouth).
- Probables : Black Belt (62037) cible `"Character"` non reconnue ; Sidewinder (62033) donné à l'initiateur du
  sbire et non au joueur qui attaque (multijoueur, risque d'assert).

## Couverture
Aucun cas pour 62003-62007, 62009-62011, 62013, 62015, 62018, 62019, 62023, 62028-62033, 62035-62037. Tous les
écarts tombent sur des cartes sans cas.

## ✅ CORRIGÉ le 10/10/2026 (branche `luke-cage-correctifs`, commit 4abf053d) : gabarits PROCESSUS-CARTE

Moteur : `WhenFaceWouldDealDamage.ReduceDamage` (réduction à l'étape « would be dealt »), paramètre `end_phase` de
`TemporaryGain`/`GainUntilPhaseEnd` (défaut None : aucune carte existante ne change). `data/cards.json` : `ATK+` de
62031, somme de contrôle recalculée (`tools/recalculer_checksums.py`).

| Carte | Réf. (étape 2) | Cas (étape 7) | Rouge avant / substitution |
|---|---|---|---|
| 62011 Power Man | 32006 Organic Steel | Tenace de Luke → pioche ; contre-cas Tenace d'un allié | oui / oui (contre-cas vert, absence) |
| 62010 Metal Bracer | `WhenDamageWouldBeDealtTo` (39028, 40106) | attaque à 1 réduite à 0, Tenace gardé ; pas sur l'imblocable | oui / oui (2e : absence) |
| 62002 Jessica Jones | 29030 Lucia von Bardas (écoute Status) | +2 après coup ; plafond +4 ; baisse à la perte | oui / oui |
| 62013 Misty Knight | 29030 | perte du Tenace → 0 ; témoin d'entrée +2/+2 | oui / oui (témoin) |
| 62009 Cruisin' | ar008 Reeling | sur un sbire + engage (2 joueurs) ; +2 base ; +2 événement | oui (sauf base, déjà bon) / oui |
| 62015 Take a Stand | 51024 + `end_phase` | survit à la fin de phase du méchant ; tombe en fin de phase joueurs | oui / oui |
| 62031 Augmented Jaws | 51040 Energy Truncheon, 01100 | sur Rhino +1 ATQ ; sur Cottonmouth s'il est là | oui / oui |
| 62037 Black Belt | 34007, 31029 | sur Iron Fist ; sur Luke ; contre-cas jamais sur Rhino | contre-cas rouge / oui |
| 62033 Sidewinder | 24046 Speed Demon | Boost sur le dessus du deck → distribué à l'attaquant ; contre-cas sans Boost | oui (assert avalée) / oui |

Étape 7 bis : aucune limite imprimée sur ces cartes. Étape 8 : autoplay 8 parties luke_cage + 8 spider_man (rhino),
0 NameError/AttributeError/TypeError/KeyError/AssertionError ; Cruisin' posé sur Hydra Mercenary et Asp, Power Man
déclenché, Bracelet utilisé 7 fois. Étape 8 bis : `ui-app/src/board/amelioration-sur-sbire.test.ts` (amélioration du
joueur sur un sbire engagé), VERT D'EMBLÉE : le plateau savait déjà la dessiner, le défaut était moteur ; jamais vu
rouge, témoin « carte absente » ajouté.
Non fait : multijoueur réel pour Sidewinder (le cas est en solo) ; capacité ★ d'Augmented Jaws (défausse de chaque
Tenace) sans cas ; 62029 Cottonmouth, 62014 Valkyrie : doutes mineurs de l'audit, non tranchés.
Carte terminée : OUI pour les 9, sous ces réserves. Non déployé.

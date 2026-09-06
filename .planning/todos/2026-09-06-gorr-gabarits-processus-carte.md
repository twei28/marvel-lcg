# PROCESSUS-CARTE.md : les 26 gabarits du pack VILAIN GORR (set 136, `gb`)

Gabarit régularisé le 06/09/2026 (audit C, point 3). Le portage réel a eu
lieu le 02/09/2026 (auteur BLUEHG) : ce fichier n'invente aucun travail, il
met en forme la preuve déjà écrite dans
`.planning/todos/2026-09-02-portage-gorr.md` (journal de synthèse, §0-§5) et
dans l'en-tête de chaque module `src/cards/pack/gorr/gorr_the_god_butcher/gbXXX.py`
(« CARTES DE RÉFÉRENCE », « TEXTE CONTRE CODE »), qui portent les étapes 2 et
5 carte par carte. **Aucune case cochée ici sans preuve déjà écrite ailleurs
et citée.**

Gorr est un pack **VILAIN** (Scenario Pack) : pas de deck de départ, pas de
textes français (convention documentée dans le journal §4, ni The Spot ni
Web of Deceit n'en ont), et `PROCESSUS-HEROS.md` ne s'applique pas
littéralement (il vise les packs héros). Le gabarit carte par carte de
`PROCESSUS-CARTE.md` s'applique en revanche intégralement.

**Preuves communes**, citées une fois :

- **Étape 1** : `data/cards.json`, pack `gorr`, 26 `card_id` ; `sets_info.json`
  « 136. Custom (Gorr the God Butcher) » ; préfixe `gb` déclaré dans
  `tools/prefixes_fanmade.json`, aucun doublon ni préfixe non déclaré.
- **Étape 4** : 26 images dans `assets/pics/`.
- **Étape 7, batterie** : `tools/test_capacites.py … gb0` → **30/30** au
  portage initial, **32/32** après les deux sets modulaires (journal §4).
- **Étape 7, substitution** : `tools/substituer_pack.py` → **25/26 cartes**
  rouges à l'origine ; la 26e (`gb004a`, Setup) est passée rouge (**1/1**) une
  fois le set modulaire Necroverse porté le même jour (journal
  `2026-09-02-portage-modulaires-gorr.md` §0 : « il est désormais rouge sans
  son module »). **26/26 cartes ont donc, à ce jour, au moins un cas qui tombe
  au rouge sans leur module.** Le détail carte par carte des cas verts
  restants (contre-cas d'absence, assumés) est cité sous chaque carte
  concernée ; le journal source ne détaille pas les autres au-delà de
  l'agrégat 25/26 → 26/26.
- **Étape 8, autoplay** : 8 parties `spider_man` contre `gorr`, 8 parties
  témoin `rhino`, le 02/09/2026 (journal §3). **Grep exhaustif des 8 journaux :
  0** (`NameError|AttributeError|TypeError|KeyError|AssertionError`). 18 des
  22 cartes alors scriptées vues en jeu réel (les 4 restantes le sont par
  construction de scénario : `gb003`/`gb006`/`gb008`/`gb022` n'apparaissent
  qu'au stade III ou avec 3 Necro-Raven en jeu, jamais atteints en 9 tours de
  bot). Après le portage des modulaires, 8 parties supplémentaires avec les
  deux sets actifs, **0 erreur**, 10 cartes vues (journal modulaires §5).
- `test_cards` : 5047 ok / 0 err (portage initial), 5057 après modulaires.
- Batterie complète du harnais : 993/997, les 4 rouges étant les 4 rouges
  préexistants de `squirrel_girl`, 0 régression.
- `tools/audit_cartes.py` : 0 discordance sur les trois packs (gorr + 2 sets
  modulaires).

⚠ **Ce que ces blocs ne peuvent pas voir** : aucune partie n'a été jouée par
un humain dans le navigateur (journal §5). Écrit ici noir sur blanc, comme
l'exige `PROCESSUS-CARTE.md`.

---

## Gabarits, carte par carte

Sauf mention contraire : étape 2 (carte de référence) et étape 5 (mots-pièges
texte-contre-code) sont documentées dans l'en-tête du module `gbXXX.py`
lui-même (bloc « CARTES DE RÉFÉRENCE » / « TEXTE CONTRE CODE »), relu et jugé
conforme dans le journal §2. Étape 6 (nombres) : conforme, aucun écart trouvé
par le journal. Étape 8 : preuve commune ci-dessus, sauf mention contraire.

### gb001, gb002, gb003 : * Gorr the God Butcher (formes I/II/III)
- [x] Étape 7 : `gb001 … un deck de joueur epuise le fait s'activer`,
      `gb002 … a la revelation, 1 carte rencontre par joueur`,
      `gb003 … a la revelation, le complot saute en 3A`.
- [x] Étape 7 bis : aucune limite imprimée sur les trois formes.

**Cartes terminées : OUI** (gb001, gb002, gb003). ⚠ gb003 n'est jamais vu en
autoplay normal (vilain III, expert seulement) : preuve par le cas et la
substitution uniquement, pas par une partie.

### gb004a : Deicide (1A)
- [x] Étape 7 : `gb004a Deicide 1A — le Setup met de cote le Gestalt et
      l'environnement`.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Substitution : **1/1 rouge** depuis le portage du set Necroverse (voir
      preuve commune) : le cas était vert avant (rien à mesurer tant que
      Necroverse n'existait pas), corrigé le jour même, jamais laissé tel
      quel.

**Carte terminée : OUI**

### gb004b : Deicide (1B)
- [x] Étape 7 : `gb004b … au stade II, l'etape 1 pose le 3e compteur plan et
      fait avancer` + `gb004b … au stade I, aucun compteur plan (contre-cas)`.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Substitution : le contre-cas (stade I) reste vert par construction,
      absence d'effet assumée (journal §2, « contre-cas d'ABSENCE d'effet »).

**Carte terminée : OUI**

### gb005a, gb005b : Make Ready the Bomb (2A/2B)
- [x] Étape 7 : `gb005a … pose la Godbomb et glisse Heroes' Labor dans chaque
      deck`, `gb005b … l'etape 1 de la phase du vilain pose 1 timer par
      joueur`.
- [x] Étape 7 bis : aucune limite imprimée.

**Cartes terminées : OUI**

### gb006a, gb006b : Welcome to Darkness (3A/3B)
- [x] Étape 7 : `gb006a … retourne la Godbomb et vide ses timers`,
      `gb006a … sans Godbomb posee, l'environnement sort de la reserve`,
      `gb006a … le set Necroverse revient dans le deck de rencontre`,
      `gb006b … un deck epuise pose 4 compteurs necro`.
- [x] Étape 7 bis : aucune limite imprimée.

**Cartes terminées : OUI**

### gb007a : Godbomb (environnement)
- [x] Étape 7 : `gb007a … au 12e timer par joueur, les joueurs perdent`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb007b : All-Black Necroverse (environnement)
- [x] Étape 7 : `gb007b … a 6 necro par joueur, les NECROVERSE gagnent +1
      ATQ` + `gb007b … a 5 necro, l'ATQ ne bouge pas (contre-cas du palier)`.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Substitution : le contre-cas (palier 5) reste vert par construction,
      assumé (journal §2).

**Carte terminée : OUI**

### gb008 : * Necro-Raven Gestalt
- [x] Étape 7 : `gb008 … vaincu, il part en reserve au lieu de la defausse`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**. ⚠ Jamais vue en autoplay (il faut 3 Necro-Raven en
jeu simultanément, jamais atteint en 9 tours) : preuve par le cas et la
substitution uniquement.

### gb009 : Black Berserker
- [x] Étape 7 : `gb009 … +1 PV par attachement NECROVERSE en jeu`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb010 : Necro-Raven
- [x] Étape 7 : `gb010 … trois copies en jeu invoquent le Gestalt`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb011 : Blighted Chains
- [x] Étape 7 : `gb011 … l'attaque de base coute une carte au hasard`. ⚠ Vrai
      défaut trouvé et corrigé au portage : `desc.Retaliate` sur un
      Attachment faisait planter la création de la carte, corrigé par
      `GiveKeywordToAttached(retaliate=1)` (journal §2, défaut #1).
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb012 : Mind-Hewn Blade
- [x] Étape 7 : `gb012 … quand Gorr attaque, 2 cartes du deck sautent`. ⚠ Vrai
      défaut trouvé et corrigé : `message.GetToPlayer()` n'existe pas sur
      `WhenUnitWouldAttack`, corrigé en `GetAgainstPlayer()` (journal §2,
      défaut #2, la carte ne faisait rien, en silence, avant correction).
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb013 : Umbral Wings
- [x] Étape 7 : `gb013 … les degats subis par Gorr sont reduits de 1`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb014 : Vicious Tendrils
- [x] Étape 7 : `gb014 … Gorr gagne riposte 1 et +1 ATQ`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb015 : Anti-Dogma
- [x] Étape 7 : `gb015 … Gorr manigance, puis 2 menaces ou 2 cartes`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb016 : Brutal Cunning
- [x] Étape 7 : `gb016 … la fouille sort un attachement NECROVERSE et le
      revele`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb017 : Gleeful Savagery
- [x] Étape 7 : `gb017 … en alter-ego, 1 degat indirect et surge`. ⚠ Faux
      vert corrigé au portage : le dégât indirect seul ne prouvait rien (il
      vient de l'activation du vilain, pas de la carte) ; le cas vérifie
      maintenant le surge (journal §2).
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb018 : Forgotten Gods
- [x] Étape 7 : `gb018 … a la fin de la phase du vilain, 1 degat indirect a
      chacun` + `gb018 … [star] Boost : la carte se revele au lieu d'etre
      defaussee`. ⚠ Vrai défaut trouvé et corrigé (partagé avec `ih002`) :
      `RegisterTemp` sans `unregister_after_exec` (mot-clé sans défaut) faisait
      avaler un `TypeError` par le moteur, le ★ Boost ne faisait rien ; puis
      un second défaut (la carte révélée était aussitôt redéfaussée) a exigé
      `message.SetBeInstead(effect)` sur `WhenCardWouldDiscard` (journal
      modulaires §3).
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb019 : Nihilistic Vision
- [x] Étape 7 : `gb019 … tous les NECROVERSE gagnent +1 ATQ`.
- [x] Étape 7 bis : aucune limite imprimée.

**Carte terminée : OUI**

### gb020 : You Are My God
- [x] Étape 2 : `AfterUnitAttackEnd(ForcedResponse, CardFinder(name=...))` +
      `DoActivate(..., do_not_give_boost=True)` (en-tête `gb020.py`).
- [x] Étape 5 : mots-pièges vérifiés dans le module : « ATTACKS » (toute
      attaque, pas seulement l'activation de phase), « HE ATTACKS AGAIN »
      (même joueur cible), « NO BOOST CARDS » (seconde attaque seulement),
      « ONCE PER PLAYER PER PHASE » (borné au joueur, pas global, piège
      `wd056b` documenté dans le module). Résultat : conforme.
- [x] Étape 6 : ATQ 2, seuil 2, 2 icônes de boost. Résultat : conforme.
- [x] Étape 7 : `gb020 … apres son attaque, Gorr attaque une seconde fois`,
      vérificateur dédié `gorr_deux_attaques`. **CORRECTIF DU 06/09/2026
      (audit C, point 2)** : la version livrée le 02/09/2026 ne vérifiait que
      `subis >= 4`, ce qui prouvait que l'effet PART mais pas que la limite
      MORD (un moteur laissant Gorr attaquer une 3e fois serait passé quand
      même). Corrigé pour vérifier une égalité stricte à chaque étape
      (`== 4` puis `== 6`, jamais `>=`).
- [x] **Étape 7 bis : limite imprimée OUI, et elle MORD DESORMAIS.**
      **CORRIGÉ le 07/09/2026 (audit C, point 2, suite, commit `ea980b97`).**
      Le témoin (`gorr_deux_attaques`) était **ROUGE** :
      `test_capacites.py … "gb020 You Are My God"` → « 10 degat(s) subis
      apres la 1ere activation (attendu EXACTEMENT 4) », identité à **-1/10
      PV** après UNE SEULE activation du vilain (5 attaques de 2, pas 2).
      Cause identifiée par lecture de code : la condition maison de
      `gb020.py` (`effect.world.stat.IsOncePerPhasePerPlayer(...)`, imposée
      par l'incompatibilité de `.LimitOncePerPhasePerPlayer()` avec
      `AfterUnitAttackEnd`, voir en-tête du module) ne faisait que LIRE le
      registre : elle n'appelait jamais `world.stat.RecordEffectWithPlayer(...)`
      pour l'alimenter, et le moteur ne le fait pas non plus pour elle
      (`SetHasSpellInPhase`, `effect/effect.py:172`, ne s'applique qu'aux
      `TriggerNonePlayerMessage`, exactement ce que `gb020` a dû écarter).
      La Réponse Forcée s'auto-redéclenchait donc sans fin, en test comme en
      partie réelle. **Corrigé dans le pack** (pas dans le moteur) : `il_frappe_encore`
      appelle désormais `effect.world.stat.RecordEffectWithPlayer(effect, joueur)`
      AVANT de déclencher la seconde attaque. Témoin passé au **VERT**
      (`6 degats au total (4 puis +2)`), et repassé au **ROUGE**, message
      identique à l'origine, en retirant temporairement cet appel
      (contre-preuve). Batterie complète du pack (filtre `gb0`) : **32/32**.
      Détail complet dans `.superpowers/audit-2026-09-06/C-gb020-report.md`.

**Carte terminée : OUI.** Le témoin d'épuisement prouve désormais que la
limite imprimée mord : Gorr attaque exactement deux fois par activation,
une seule fois par joueur et par phase, jamais plus.

### gb021 : Heroes' Labor
- [x] Étape 7 : `gb021 … revelee, elle pose 1 timer sur la Godbomb` +
      `gb021 … sans Godbomb, c'est un compteur necro qui part`.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Particularité : carte à DOS DE CARTE JOUEUR (journal §0), fabriquée
      dans `player.player_deck`, modèle Panicked Refugees (45178).

**Carte terminée : OUI**

### gb022 : Stalking Berserker
- [x] Étape 7 : `gb022 … a la fin de ton tour, 2 cartes et 1 necro`.
- [x] Étape 7 bis : aucune limite imprimée.
- [x] Particularité : carte à DOS DE CARTE JOUEUR (journal §0), même montage
      que gb021.

**Carte terminée : OUI**. ⚠ Jamais vue en autoplay (stade III, jamais
atteint) : preuve par le cas et la substitution uniquement.

---

## Bilan

**26 cartes sur 26 sont terminées** (cas de test sujet, preuve par
substitution ou contre-cas d'absence assumé, preuve commune d'autoplay au
niveau du pack). `gb020` était restée NON : son témoin d'épuisement, corrigé
le 06/09/2026 pour prouver une égalité et non un plancher, avait révélé que
sa limite imprimée (« Limit once per player per phase ») était **inerte**.
**Corrigé le 07/09/2026** (voir sa propre section ci-dessus et
`.superpowers/audit-2026-09-06/C-gb020-report.md`) : la carte appelle
maintenant `world.stat.RecordEffectWithPlayer` elle-même, et la limite mord.

Reste dû, écrit noir sur blanc et non caché : **aucune partie n'a été jouée
par un humain dans le navigateur**, pour Gorr ni pour ses deux sets
modulaires (voir les gabarits séparés). C'est le seul juge de « la carte
est-elle agréable et fait-elle ce qu'elle promet », et aucun outil du projet
ne le remplace.

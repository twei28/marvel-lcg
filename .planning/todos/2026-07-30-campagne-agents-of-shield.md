# TODO / SPEC — Campagne Agents of S.H.I.E.L.D. (mode Campagne moteur)

**Statut :** ✅ **LIVRÉ le 11/08/2026.** Ce document décrivait deux bloqueurs « durs »
qui ont tous les deux sauté. Il est conservé comme spec de référence des règles, et
parce que la façon dont les bloqueurs sont tombés vaut d'être lue.
**Date de conception :** 2026-07-30 — **statut corrigé le 12/08/2026**
**Origine :** demande « on fait aos » pendant le chantier du mode Campagne de l'écran « Préparer une partie ».
**Rapport aux campagnes livrées :** **les HUIT boîtes fonctionnent** (`trors`, `sm`,
`mts`, `mut_gen`, `next_evol`, `aoa`, `gmw`, `aos`), chacune avec son carnet et au
moins un scénario joué de bout en bout par un test. Seul Civil War reste dehors, et ce
n'est pas une campagne : voir `2026-07-30-mode-bataille-civil-war.md`.

---

## 0. Ce qui a fait tomber les deux bloqueurs (ajouté le 12/08/2026)

**Bloqueur 1, la table des 27 combinaisons : elle n'était pas perdue, elle était déjà
dans le code.** `CalcMole` (moteur, pack aos) la portait depuis le début. Elle a été
transcrite indépendamment depuis le carnet officiel, et les deux lectures concordent
exactement — c'est ce qui a permis de s'y fier. Elle vit maintenant en double, dans le
moteur et dans `data/campagnes/aos.json` pour l'écran, et
`tools/verifier_grille_aos.py` compare les deux en lisant le module Python en AST : si
l'une dérive, il refuse et nomme la combinaison fautive.

**Bloqueur 1 bis, le texte des 9 cartes Evidence :** il n'a pas été nécessaire. Les
preuves ne sont jamais fabriquées comme cartes tant que le joueur n'a pas le droit de
les voir, et leur seul rôle est d'être comparées à la combinaison de la taupe.

**Bloqueur 2, « impossible à tester » : c'était vrai, et ça ne l'est plus.**
`ui-check/scripts/serveur-dev.py` n'est plus un serveur statique : il démarre un VRAI
moteur sur le port 2346, depuis le codebase de travail, sans toucher à la partie du
2345. Tout le harnais de test des campagnes en dépend.

**Le crash du §2 est corrigé :** l'`assert Worlds.IsCampaign(effect) == False` de
`50167a.py` a été remplacé par un retour anticipé, avec le commentaire qui explique
pourquoi (en campagne, les membres du Conseil viennent du scénario précédent). `aos`
est dans les boîtes-campagnes de l'écran, et son scénario 5 se joue.

**Ce qui a été livré au-delà de cette spec :** la grille de déduction à l'écran,
l'accusation avec l'accusé qui DÉCOULE de la combinaison (correctif de règle, p.19),
la reprise du scénario 5 après une défaite en standard, le soin de campagne experte, et
le report des compteurs secrets. Détail complet au §8 bis de `docs/CAMPAGNES.md`.

**Ce qui reste ouvert sur aos :** rien de connu. Le deck de rencontre part toujours au
navigateur avec ses identifiants, comme pour toutes les boîtes (§17 de
`docs/CAMPAGNES.md`).

---

## 1. Pourquoi ce n'est pas livré (2 bloqueurs durs)

1. **Données manquantes / non récupérables :**
   - La **table des 27 combinaisons** de preuves (Means × Motive × Opportunity → quel membre du Conseil est le traître). Elle est imprimée en icônes sur le *Campaign Log* PDF officiel, **illisible** sur les scans trouvés. C'est de la donnée, pas de la logique — indispensable pour résoudre l'accusation correctement.
   - Le **texte complet de 8 des 9 cartes Evidence** (50185-50193). Seul Wiretap (50186) a été retrouvé. Chacune a une capacité « Setup » qui se ré-applique à chaque scénario suivant.
2. **Impossible à tester :** lancer une 2e instance du **vrai moteur** échoue — `device/manager/web/manager.py` fait `assert ip/port` et entre en conflit avec l'instance en ligne (port 2345, `launch.online.json`) qu'on ne doit pas perturber. Le port 2346 est un serveur **statique** (`ui-check/scripts/serveur-dev.py`) qui sert le front mais **n'exécute pas** la logique Python. Donc aucun moyen de valider du code moteur AoS sans (a) le mot de passe de l'online, ou (b) l'autorisation d'arrêter l'online un moment.

**Règle de sécurité retenue :** ne pas livrer de code moteur non testé qui pourrait planter des parties. D'où le revert.

---

## 2. Le crash à connaître ~~(à connaître)~~ — CORRIGÉ le 11/08/2026, voir §0

`src/cards/pack/aos/baron_zemo/50167a.py` (scénario 5, mise en place) contient :
```python
assert Worlds.IsCampaign(effect) == False
PreparingTheEvidence(effect)
```
→ **Baron Zemo plante en mode campagne.** La campagne AoS a été **délibérément laissée non finie** dans la reconstruction (le code campagne n'existe pas dans le bytecode d'origine). **Ne PAS rajouter `aos` à `CAMPAIGN_CODES`** (dans `public/js/prepare/app.js`) tant que le scénario 5 n'est pas géré en mode campagne.

---

## 3. Ce que la vraie campagne exige (règles officielles, vérifiées)

Sources : rulebook MC50 (FFG) + Campaign Log PDF officiel + marvelcdb `set/aos`.

C'est une **enquête à état persistant** sur 5 scénarios joués dans l'ordre (Black Widow → Batroc → M.O.D.O.K. → Thunderbolts → Baron Zemo), à gagner tous dans l'ordre. Il n'y a **pas** de récompenses « ajouter une amélioration au deck » classiques ; le report est de l'**état de jeu**.

### 3.1 État persistant à suivre dans le journal
- **Grille de marqueurs secrets** : 3 membres du Conseil (Chief Medical / Surveillance / Tactical Officer, cartes 50181-50183) × après scénarios 1/2/3/4. Reporté au setup du scénario suivant. À 4 secrets (3 en expert) le membre **flippe définitivement** côté vilain.
- **Preuves obtenues** (déduction) : à chaque fin de scénario, si ≥1 membre à 0 secret → gagner 1 carte Evidence de l'enveloppe S.H.I.E.L.D., révéler son icône, barrer les combinaisons contenant cette icône.
- **Reports par scénario :**
  - S1 victoire → nb (sbires + complots secondaires) en jeu → **menace sur Alert Level au setup S2**.
  - S2 victoire → nb Rescued Captive (50091) → **retirer X verrous du Holding Cell au setup S3**.
  - S3 victoire → environnements Adaptoïde en jeu (50109-50112) → **mis en jeu au setup S5**.
  - S4 victoire → Thunderbolts minions survivants → **mélangés au deck rencontre S5, sauf Jolt (50133)**.
- **Expert :** PV restants par joueur (report + option de soin à un coût au setup).

### 3.2 Enveloppes (mécanique cœur, infra DÉJÀ présente en code)
- Décks nommés `A.I.M.Envelope` et `S.H.I.E.L.D.Envelope` (via `Worlds.ScenarioDeck`).
- Helpers existants dans `src/cards/pack/aos/baron_zemo/__init__.py` : `ShieldEnvelopeHasCards`, `GainCardsFromShieldEnvelope`, `PreparingTheEvidence` (tirage aléatoire du traître en standalone), `CalcMole` (les 3 cartes A.I.M. → officier traître).
- 9 cartes Evidence, 3 par catégorie :
  - Means : 50185 Medical Records, 50186 Wiretap, 50187 Security Scanner
  - Motive : 50188 Money, 50189 Blackmail, 50190 Ideology
  - Opportunity : 50191 Security Clearance, 50192 Travel, 50193 Authority
- Le dossier A.I.M. = exactement 1 carte de chaque catégorie (le traître). `CalcMole` mappe les 27 combos → 3 officiers (9 chacun).
- `50168a.py` (The Accusation) : le joueur choisit means/motive/opportunity + accuse un officier ; `50168b.py` vérifie via `CalcMole`.

---

## 4. Plan d'implémentation (quand déblocable)

1. **Récupérer les données** (bloqueur 1) : transcrire la table des 27 combinaisons depuis un scan HD du Campaign Log ; récupérer les 8 textes de cartes Evidence sur marvelcdb (50185-50193).
2. **Obtenir un environnement de test** (bloqueur 2) : mot de passe online, ou fenêtre pour lancer le moteur en local.
3. **Écrire `src/cards/pack/aos/campaign.py`** (sur le modèle de `mts/campaign.py` + `aoa/campaign_setup.py`) : helpers `InPool`/`LogSet` réutilisables, `CampaignSetup(level)` par scénario.
4. **Câbler les 5 scénarios** (fichiers `*a.py` des vilains) pour appeler `CampaignSetup(level)` : placement des marqueurs secrets depuis le journal, reports S1→S2 / S2→S3 / S3→S5 / S4→S5, résolution des capacités Setup des Evidence gagnées.
5. **Corriger `baron_zemo/50167a.py`** : remplacer l'`assert IsCampaign==False` par une branche campagne qui reconstitue les enveloppes depuis le journal (le dossier A.I.M. désigné) ; fallback `PreparingTheEvidence` si journal incomplet. (Une ébauche de `PreparingTheEvidenceCampaign` a été écrite puis annulée — repartir de zéro proprement.)
6. **Étendre le journal frontend** (`CAMPAIGN_SCHEMAS.aos` dans `app.js`) : grille de marqueurs secrets (3 membres × int), reports par scénario (sbires, captifs, adaptoïdes cochés, Thunderbolts survivants), dossier A.I.M. (3 cardpick Means/Motive/Opportunity, cartes 50185-50193), PV restants (expert). Puis rajouter `aos` à `CAMPAIGN_CODES`.
7. **Tester** un enchaînement complet dans le vrai moteur (pas le serveur statique).

**Ampleur estimée :** gros, multi-séances. C'est la campagne la plus lourde des huit (état persistant + déduction + 5 scénarios câblés + expert).

---

## 5. Rappels techniques utiles
- Moteur = source **WSL** `~/marvel-work/fusion/marvel-lcg-src/src/` (la copie Windows est périmée). Recompilation `.pyc` incrémentale par `launcher_fast.py` au démarrage.
- Le journal de campagne frontend part dans le descripteur `campaign_log` (dict clé→valeur) via `launcher.js` ; le moteur le lit au setup (`world.py` seed le store, `CampaignLog.Get*`). Le moteur **ne ré-exporte pas** le journal → tout est saisi à la main par le joueur (comme le carnet physique).

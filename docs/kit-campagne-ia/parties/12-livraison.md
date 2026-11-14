---

## 12. Ce que tu livres, exactement, et dans quel ordre travailler

### 12.1 L'ordre de travail recommandé

Pour une grosse campagne, **livre scénario par scénario** (un message, ou un lot de fichiers, par scénario) plutôt
que tout d'un coup : la relecture de Claude est plus fiable et une erreur de méthode se corrige au premier lot.

| Phase | Tu fais | Tu produis |
|---|---|---|
| **0. Lecture** | Lire le livret de campagne **en entier** (règles de campagne, carnet imprimé, encarts SETUP / VICTORY / DEFEAT de chaque scénario) et les cartes fournies. Le **carnet imprimé** fait autorité sur le code : lis-le **avant** d'écrire une définition. | notes de travail (pas de livrable) |
| **1. Cadrage** | Choisir le **code** de la campagne, le **nom du pack**, proposer **deux préfixes** libres (question à choix multiple). Lister **tous** les contenus déjà présents dans le jeu (Standard, Expert, sets modulaires officiels réutilisés, héros officiels cités). | `QUESTIONS.md` (premières questions), `MANIFESTE.md` (squelette) |
| **2. Cartes** | Transcrire **chaque carte** (une planche de 4 cartes par lecture : au-delà le texte d'encart n'est plus sûr), numéroter sans trou, remplir `desc`. | `integration/data/cards.<pack>.fragment.json`, `images.md` |
| **3. Scénarios et sets** | Écrire les fichiers de scénario (standard **et** expert), les sets de rencontre, l'entrée `sets_info`. | `integration/data/scenarios/*`, `…/encounter_sets/*`, `…/sets_info.<pack>.fragment.json` |
| **4. Description + carnet** | Écrire `data/campagnes/<code>.json` et la **table des clés** (`CARNET-CLES.md`). | `integration/data/campagnes/<code>.json`, `CARNET-CLES.md` |
| **5. Scripts** | Les scripts de cartes, **scénario par scénario**, avec leur gabarit. | `integration/src/cards/pack/<pack>/…`, `GABARITS.md` |
| **6. Logique de campagne** | `campaign.py` + l'appel `*CampaignSetup(n)` sur chaque face 1A. | `integration/src/cards/pack/<pack>/campaign.py` |
| **7. Textes et métadonnées** | Textes français, biographies, préfixe, crédits, pages du livret. | `integration/textes-fr/…`, `…/mechants-info.fragment.js`, `…/prefixes.<pack>.fragment.json`, `CREDITS.md`, `livret-pages.md` |
| **8. Preuves** | Les cas de test de capacité et les épreuves de boucle. | `integration/tools/cas/<bloc>.py`, `integration/tools/epreuves.<code>.fragment.py` |
| **9. Auto-vérification** | Lancer `verifier-livraison-campagne.py` ; relire chaque checklist ; compter les `A_FAIRE_CLAUDE`. | `AUTO-VERIFICATION.md`, `A_FAIRE_CLAUDE.md`, `BESOINS-MOTEUR.md`, `QUESTIONS.md` à jour |

### 12.2 L'arborescence de la livraison

Elle **reproduit celle du projet** (chemins relatifs à la racine du moteur), pour que Claude fusionne sans deviner.
Voici la livraison d'une campagne imaginaire `ma_campagne` (pack `ma_campagne`, préfixe `mc`, code `ma_campagne`) :

```
livraison/
├── MANIFESTE.md                    la liste de TOUS les fichiers livrés (§12.3)
├── QUESTIONS.md                    les questions ouvertes (§12.4)
├── BESOINS-MOTEUR.md               ce que le moteur / l'interface devra apprendre (§12.5)
├── A_FAIRE_CLAUDE.md               tous les marqueurs A_FAIRE_CLAUDE regroupés (§12.6)
├── CARNET-CLES.md                  la table des clés du carnet (§7.10)
├── GABARITS.md                     un gabarit PROCESSUS-CARTE par carte à capacité (§6.8)
├── AUTO-VERIFICATION.md            ce que tu as vérifié, avec la sortie du vérificateur (§12.7)
├── CREDITS.md                      (§10.8)
├── images.md                       card_id → fichier source (§10.1)
├── livret-pages.md                 quelle page du PDF joue quel rôle (§10.6)
└── integration/
    ├── data/
    │   ├── cards.ma_campagne.fragment.json            {"ma_campagne": [ ...cartes... ]}
    │   ├── sets_info.ma_campagne.fragment.json         {"N. Custom (Ma campagne)": {...}}
    │   ├── campagnes/ma_campagne.json
    │   ├── scenarios/mc_scenario_1.json    mc_scenario_1_expert.json    ...
    │   └── encounter_sets/mc_set_a.json    mc_set_b.json                ...
    ├── src/cards/pack/ma_campagne/
    │   ├── __init__.py                                  helpers partagés du pack
    │   ├── campaign.py                                  §7
    │   └── <set_nettoyé>/__init__.py   <card_id>.py     ... un dossier par set
    ├── textes-fr/ma_campagne.fragment.txt              lignes pour textes-fr-fanmade.ts
    ├── public/js/prepare/mechants-info.fragment.js     biographies des vilains
    └── tools/
        ├── prefixes.ma_campagne.fragment.json           entrée de prefixes_fanmade.json
        ├── cas/ma_campagne.py                           cas de test de capacité
        └── epreuves.ma_campagne.fragment.py             EPREUVES += [ ... ]
```

**Règles de forme** :

* **Encodage UTF-8, fins de ligne `\n`**, JSON indenté de 4 espaces, `ensure_ascii=False`.
* **Un fichier par face de carte à capacité** ; **jamais** deux cartes dans un même script.
* Aucun fichier **hors** de cette arborescence ; aucun fichier temporaire.
* **Les fragments contiennent *seulement* ta part** : jamais une copie, même partielle, d'un fichier partagé qui
  contiendrait les cartes des autres.
* **Aucune modification d'un fichier existant du projet** : tout nouveau fichier ; tout ce qui doit changer dans
  un fichier existant (moteur, interface, liste blanche de traits ou compteurs) va dans `BESOINS-MOTEUR.md`.

### 12.3 `MANIFESTE.md`

Une ligne par fichier livré :

```
| Chemin (dans integration/)                         | Rôle                                  | Cartes / entrées | Statut |
|----------------------------------------------------|---------------------------------------|------------------|--------|
| data/cards.ma_campagne.fragment.json               | cartes du pack                        | 176 faces        | complet |
| src/cards/pack/ma_campagne/shocker/mc002a.py       | Setup du complot 1A + CampaignSetup   | 1                | A_FAIRE_CLAUDE ×1 |
```

**Statut** : `complet` · `partiel (A_FAIRE_CLAUDE ×n)` · `brouillon`. À la fin du manifeste : les totaux (cartes,
faces, scénarios, sets, scripts, cas de test, épreuves, `A_FAIRE_CLAUDE`).

### 12.4 `QUESTIONS.md` — une question par entrée, format fixe

```
### Q<n> — <card_id ou règle> : <le doute en une phrase>

Image / source : <fichier de la carte, page du livret>
Texte imprimé : « … »

Lectures possibles :
  A. (recommandée) <lecture> — en jeu : <ce que ça change>
  B. <lecture> — en jeu : <ce que ça change>
  C. Autre (précise)

Lecture retenue en attendant : A  (repérée par `# QUESTION <n> :` dans <fichier>)
```

Une **seule** question à la fois est posée à l'utilisateur (règle 4, §1.2) ; ce fichier les **range** pour Claude.

### 12.5 `BESOINS-MOTEUR.md` — format fixe

```
### B<n> — <titre court>

Livret : page <p>, « … »
Ce que le jeu fait déjà de plus proche : <fichier : fonction, ou « rien »>
Ce qui manque : <comportement attendu, décrit ; pas de code>
Dépend : <card_id(s), clé(s) de carnet, champ(s) de description>
En attendant : <A_FAIRE_CLAUDE posé dans <fichier>, ou lecture retenue>
```

Y vont **aussi** : les **traits nouveaux** (`trait nouveau : X, porté par mc012`), les **compteurs nouveaux**
(`compteur nouveau : knucklehead, desc.Uses de mc044`), les **chaînes d'interface nouvelles** avec leur traduction
anglaise, les cartes réservées à la campagne (`SETS_RESERVES_A_LA_CAMPAGNE`), les écrans inédits.

### 12.6 `A_FAIRE_CLAUDE.md`

Tous les marqueurs `# A_FAIRE_CLAUDE:` du code, regroupés : `fichier : ligne : texte imprimé visé : ce qui manque :
carte de référence la plus proche`. **Un marqueur dans le code qui n'est pas dans cette liste est une faute.**

### 12.7 `AUTO-VERIFICATION.md`

```
## Vérificateur de livraison
$ python3 verifier-livraison-campagne.py livraison/
<la sortie complète, collée>

## Relectures faites (cochées seulement si faites)
- [x] §4.10 checklist de carte : toutes les cartes
- [x] §5.7 checklist de scénario : chaque scénario
- [x] §8.8 checklist de description de campagne
- [x] §7.10 table des clés : chaque clé écrite ET lue

## Ce qui n'a PAS été vérifié (à exécuter par Claude)
- cas de test de capacité : écrits, non exécutés
- épreuves de boucle : écrites, non exécutées
- aucune partie jouée
```

### 12.8 Ce que tu ne fais jamais (rappel)

Pas d'images ni de scans ; pas de checksum ; pas de commit ni de déploiement ; pas de modification du moteur ;
pas de deck de départ inventé pour un héros ; pas de « vert » non exécuté ; pas de chiffre de test non mesuré ;
**pas de décision de règle en silence**.

### 12.9 Exemple de livraison réelle : Hunting Season (Nugget)

Une campagne maison a déjà été livrée par ce même procédé (auteur : Nugget ; intégrée par Claude). Son dossier de
livraison est dans `modeles/C-livraison-exemple-hunting-season/` : `LIRE_D_ABORD.md` (état réel), `PROMPT_POUR_CLAUDE.md`
(instruction de reprise), `SPECIFICATIONS.md` (règles spéciales), `POINTS_OUVERTS.md` (décisions à prendre),
`VERIFICATION.json` (contrôles statiques effectués), `integration/` (données et scripts, **brouillons partiels**,
chaque `A_FAIRE_CLAUDE` honnête), `reference/` (carnet : `campaign_log_contract.json`, `campaign_rules.py`).

Ce qui a bien fonctionné dans cette livraison : un **inventaire carte par carte** (239 entrées pour 226 cartes
physiques, l'écart expliqué) ; des **fragments** à fusionner sans écraser ; une **décision d'utilisateur par point
ouvert**, jamais en silence (« Swarmed by Rats » : la carte imprime *Interrupt* mais décrit un déclencheur *After* →
question, pas de correction silencieuse) ; un calculateur pur des règles de campagne séparé du moteur.

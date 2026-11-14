
---

## 8. Prouver que ça marche : les gates, les cas de test, le deck montable

⚠ Une gate qui répond « OK » ne prouve rien tant qu'on ne l'a pas vue **échouer** (`PROCESSUS-CARTE.md`, §9). Les
contrôles de ta livraison (`verifier-livraison-heros.py`) ont été calibrés ainsi : 45 casses volontaires dans des
livraisons réelles, 45 détectées (`outils/test_verifier_livraison_heros.py`). Mais ils lisent des fichiers ; ils ne
**jouent** pas.

### 8.1 Les six niveaux de preuve d'un héros

| # | Niveau | Qui | Ce que ça prouve |
|---|---|---|---|
| 1 | `verifier-livraison-heros.py` | **toi**, avant de livrer | la **forme** : faces, deck, obligation, némésis, scripts présents et bien rangés, textes, biographie |
| 2 | les gates statiques du dépôt (`test_cards.py`, `verifier_prefixes.py`, `verifier_api_cartes.py`, `verifier_appels_modules.py`) | Claude | chaque carte **se construit** ; aucun appel à une fonction inexistante ; préfixe déclaré |
| 3 | **cas de test de capacité** (`tools/cas/<héros>.py`, `test_capacites.py`) | toi (tu les écris), Claude (il les joue) | la capacité **fait ce que la carte dit** dans une position réelle |
| 4 | **preuve par substitution** (`tools/substituer_pack.py`) | Claude | le cas est **rouge sans le module** de la carte et vert avec : il mesure bien la carte |
| 5 | **`verifier_tous_les_decks.py`** : le deck du héros se **monte** | Claude | la gate qui attrape les asserts de construction du deck complet (§8.5) |
| 6 | autoplay ciblé + une **partie complète** avec le héros | Claude, puis l'utilisateur | aucun traceback sur 8 parties ; le héros se joue de bout en bout |

Tu ne peux pas exécuter les niveaux 2 à 6. Tu écris ce qu'il faut pour que Claude les exécute, et tu **le dis**
dans `AUTO-VERIFICATION.md` : « cas écrits, non exécutés ». **Jamais « OK » pour ce que tu n'as pas joué.**

### 8.2 Écrire les cas de test : `tools/cas/<héros>.py`

Le fichier est **découvert automatiquement** (`glob` de `tools/cas/*.py`). Il expose `CAS = [...]` et, si besoin,
`VERIFICATIONS = r'''...'''` (du code Python de vérification). Les noms de cas sont préfixés (`[iron_fist]`) pour
pouvoir les filtrer. **Un cas = un processus** : monte une position, déclenche, mesure l'état du monde.

* Le **`card_id` de la carte apparaît dans le NOM du cas** (c'est le « sujet » que `substituer_pack.py` filtre).
* **Un cas par capacité distincte** (chaque bloc Action / Response / Interrupt / Forced… séparé sur le texte).
* **Un cas va jusqu'au bout de ce que la carte annonce** : si elle fait deux choses, il mesure les deux. Ne
  retire jamais une assertion parce qu'elle échoue.
* **Toute limite imprimée** (« once per round ») exige un **témoin d'épuisement** : deux déclenchements dans le
  même round, un chiffre mesuré au second.
* Un **contre-cas dans l'autre forme** (la Réponse de la face héros ne se déclenche pas en alter ego) est la
  moitié du travail pour une identité.
* Le héros de test d'un héros dont le deck est vide est complété par le harnais (`remplir_les_decks_vides`) ; une
  carte précise en main se donne par `main_exclusive`.

Le **fichier de cas réel d'un héros officiel** (Iron Fist, 57 cas) — début du fichier, conventions de montage et
quatre cas de l'identité :

{{EXTRAIT:Fusion/marvel-lcg-src/tools/cas/iron_fist.py|1|63|python}}

Et la fonction de vérification propre au héros (les clés d'`attendu` qu'il ajoute) :

{{BLOC:Fusion/marvel-lcg-src/tools/cas/iron_fist.py|VERIFICATIONS = r'''|def if_fin_de_round|python}}

### 8.2 bis Les clés d'un cas et les clés d'`attendu` (extrait du manuel de campagne, §11.2)

{{SECTION:docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md|**Les clés d'un cas|### 11.3 Niveau 4|2}}

Le code du vérificateur générique `etat_attendu` et la liste **complète** de ses clés sont dans le zip :
`commun/outils/test_capacites.extraits.py`. Une clé inconnue fait **échouer** le cas quand il utilise directement `"verifier": "etat_attendu"` (elle était
ignorée en silence jusqu'au 11/09/2026 ; un vérificateur maison qui appelle `etat_attendu` lit ses propres clés) : n'invente pas de clé, ajoute un `VERIFICATIONS` propre au héros comme
`if_etat` d'Iron Fist.

### 8.3 Tout ce que le montage d'un cas peut utiliser : l'API `Puzzle`

Les chaînes de `mise_en_place` et de `declencher` sont des appels à cette API (`src/game/puzzle/puzzle.py`,
générée à la construction du kit — **n'en utilise aucune autre**) :

{{PUZZLE:}}

### 8.4 La moitié d'aspect de TEST (`tools/decks-de-test.fragment.json`, facultatif)

Un héros maison à `player_deck` vide a, pour le harnais **seulement**, une moitié d'aspect de test : sans elle, la
main de départ n'est faite que de cartes signature et le pilote déclenche leurs interruptions au milieu de la
mise en place. Le harnais complète lui-même un deck vide (`remplir_les_decks_vides`) avec cette moitié ; depuis le 13/09/2026
un deck absent de ce fichier reste vide (le repli « 25 ressources » a été retiré). **Tu n'as pas à la composer** : si un de tes cas a besoin d'une carte
précise en main, il la donne par `main_exclusive`.

### 8.5 La gate qui rend un héros jouable : `verifier_tous_les_decks.py`

> ### ⚠ POURQUOI C'EST UNE GATE (leçon `ls005`, 3/9/2026)
>
> Le constructeur de cartes (`factory.py`) pose des **asserts de construction** qu'aucun autre outil ne déclenche :
> un événement à deux capacités `Play` (un « Choose one », ou une Action civile + une Action héros sur la même
> carte) doit être **déclaré dans une liste blanche**, sinon la partie plante **au setup**. `test_cards` ne monte
> pas de partie ; `test_capacites` et `substituer_pack` ne montent que les positions écrites à la main. **Seul
> `verifier_tous_les_decks` l'attrape.** Mesuré : le deck `lady_sif` était **injouable depuis son portage de la
> veille**, ses gabarits cochés, ses 22 cas verts et ses 18 cartes prouvées par substitution.

Ce que ça veut dire pour toi : **toute carte qui a deux capacités `Play` sur le même événement** se signale dans
`BESOINS-MOTEUR.md` (« événement à deux capacités Play : liste blanche à compléter »), parce que c'est la seule
chose que tu ne peux pas régler seul.

### 8.6 Le chemin outillé de Claude, avec les durées vues

{{SECTION:docs/reference/RECETTES-MOTEUR.md|## 9. Le chemin outillé|### 7duovicies|2}}

### 8.7 Ce que Claude exécute, dans l'ordre, sur ta livraison

1. `verifier-livraison-heros.py` (le même que le tien) et la **comparaison** avec le dépôt si le héros est déjà
   intégré (`outils/comparer-livraison-heros-au-depot.py`) : *identique / différent / manquant / en trop*.
2. Fusion des fragments (cartes, `sets_info`, textes français, biographie, réplique, préfixe) ; recalcul des
   checksums ; images posées ; bulles de statistiques et palette générées.
3. Les gates statiques (niveau 2), puis les cas (niveau 3) et la substitution (niveau 4).
4. `DECK_NOM=<héros> verifier_tous_les_decks.py` avec un héros témoin (niveau 5).
5. Autoplay ciblé, 8 parties minimum contre le même vilain qu'un héros témoin, avec grep exhaustif des
   tracebacks (niveau 6), puis le rendu du plateau (« étape 8 bis » : ce que la carte *dessine* — compteur sur
   l'identité, carte attachée, statut).
6. Une partie complète jouée avec le héros.

Aucune carte n'est « terminée » tant qu'il reste une capacité sans cas sujet et sans preuve par substitution, ni une
limite imprimée sans témoin d'épuisement. **Si une seule carte du pack manque son « Carte terminée : OUI », le
héros entier reste NON.**

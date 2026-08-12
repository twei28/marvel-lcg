# TODO / SPEC — Un nommage de cartes qui ne nous bloquera pas

**Statut :** ✅ **TERMINÉ le 2026-08-12.** Les 19 packs fan-made sont passés à un
préfixe de deux lettres (`917ef6a`), le registre et le vérificateur sont en place
(`0cc46ac`), et les trois doublons de numéro de set sont corrigés. Reste seulement
la vérification à la main des points 2 à 5 du §4 (deck-builder, export/import,
galerie), que seuls les tests automatisés couvrent aujourd'hui.
**Origine :** demande utilisateur, à l'occasion de deux ajouts de contenu
(« il faudrait utiliser un système de nommage de carte qui ne pourra pas nous
bloquer plus tard »)
**Prérequis de :** `2026-08-12-aspect-determination.md` et
`2026-08-12-campagne-web-of-deceit.md`

---

## 1. Le problème n'est pas à venir : il est déjà là

Mesuré dans les données le 12/8/2026, pas supposé.

**Les sets officiels vont jusqu'à 60** (`60. Fear No Evil`). **Les préfixes de
`card_id` 61 à 79 sont déjà occupés par du contenu fan-made** :

| Préfixe | Occupé par | Cartes |
|---|---|---|
| 61 | Custom (Rainy) | 20 |
| 62 à 74 | divers packs custom | ~230 |
| 75 | Squirrel Girl | 23 |
| 77 | Brawn | 26 |
| 78, 79 | custom | 47 |

**Le prochain set que FFG publiera portera le numéro 61, et 61 est pris.** Ce
n'est pas un risque théorique : c'est la prochaine sortie.

**Et trois numéros de set sont DÉJÀ en double** dans `data/sets_info.json` :

```
108 -> Custom (Cloak & Dagger)  ET  Custom (Spider-Man Rainy)
109 -> Custom (Venom Rainy)     ET  Custom (Moon Knight)
110 -> Custom (Jessica Jones)   ET  Custom (Lockjaw)
```

Aucun `card_id` n'est en double aujourd'hui (vérifié sur les 4729 cartes), donc
rien n'est cassé. Mais la place est prise sans registre, et deux ajouts arrivent.

## 2. Ce que le moteur exige vraiment (mesuré)

**Une seule contrainte dure, et elle est étroite.** `src/game/operate/referential.py:14`
fait `set_id = face.paper.card_id[:2]`, et s'en sert lignes 30-33 **uniquement**
pour départager Magneto et Venom, deux cas où plusieurs sets partagent un
`set_name`. Ailleurs, l'indexation passe par `CardsDB.sets_cards[set_name]`,
jamais par le préfixe.

**Le `card_id` n'est JAMAIS converti en entier** (vérifié : aucun `int(card_id)`
dans `src/`). Et des `card_id` non numériques existent déjà et fonctionnent :
`minion`, `wild`, `rule_a`, `rule_b`, et les 25 défis `2401_the_ground_is_lava`…

**Conclusion : rien n'oblige à un préfixe numérique.**

## 3. La proposition

**Un préfixe de DEUX LETTRES par source fan-made**, jamais un nombre.

```
dh001, dh002…   DesignHacker (aspect Determination)
wd001, wd002…   Web of Deceit (campagne)
```

Pourquoi cela tient :

- **Aucune collision possible avec l'officiel**, jamais : FFG numérote, nous
  lettrons. Les deux espaces ne se rencontrent pas, quelle que soit la croissance
  du jeu.
- **Compatible avec `card_id[:2]`** : le découpage rend `dh`, un identifiant de
  set valide et distinct.
- **Lisible dans un rapport de bug et une commande de console** : `c49` désigne
  l'objet, `dh014` désigne la carte, et on sait d'où elle vient sans chercher.
- **Extensible** : 676 sources possibles, et le jour où une source dépasse 999
  cartes, `dh1001` reste non ambigu.

### Ce qui reste à trancher au plan

- ~~**Faut-il renuméroter l'existant ?**~~ **FAIT le 12/8** sur décision de
  l'utilisateur, sans attendre. Les préfixes 61-79 devaient bouger le jour
  où FFG les atteindrait. Renuméroter touche `cards.json`, les modules
  `src/cards/pack/**`, les images `assets/pics/`, les decks et les scénarios.
  Recommandation : **ne pas y toucher maintenant**, mais figer la règle pour tout
  ajout futur et ouvrir une fiche de migration à part.
- **Où vit le registre ?** Un fichier `data/prefixes_fanmade.json` (préfixe →
  source, date, nombre de cartes) qu'un vérificateur lit. Sans registre écrit, la
  règle sera oubliée exactement comme les trois doublons de `sets_info.json`.
- **Le vérificateur.** Un `tools/verifier_prefixes.py` qui refuse : un préfixe non
  déclaré, un `card_id` en double, un numéro de set en double. À brancher au même
  rituel que `verifier_campagnes.py`.

## 4. À mesurer avant d'implémenter

Un `card_id` alphabétique traverse-t-il **toute** la chaîne ? Les points à
éprouver, chacun sur une carte témoin :

1. `CardFactory.GenerateCard` (`tools/test_generate_cards.py`) ;
2. le chemin d'image (`pic_id` → `assets/pics/<id>.jpg`) et le repli marvelcdb,
   qui attend des identifiants officiels ;
3. le deck-builder et `deck/custom/*.json` ;
4. l'export/import de deck, et `data/marvelcdb/` ;
5. le tri des cartes dans la galerie.

## 5. Comment on saura que c'est fait

Une carte témoin `zz001` traverse la génération, s'affiche avec son image, entre
dans un deck, se joue en partie, et `verifier_prefixes.py` refuse un doublon
introduit exprès.


---

## Journal de migration (12/08/2026, `c04042f`)

367 bases renommées, 390 modules Python, 396 images, ~4050 remplacements.
`ron` (90) laissé de côté : contenu officiel mal numéroté.

### Les quatre pièges, tous mesurés avant de casser quoi que ce soit

1. **Le remplacement au motif était un piège mortel.** Les identifiants de deck de
   `data/marvelcdb/` tombent dans la même plage numérique : **8517 des 12800
   occurrences étaient des faux positifs**, et 66 des 68 fichiers de l'index en
   contenaient. Le même motif aurait écrit `INT_INF = iw535` dans
   `core/lib/math.py` et cassé le moteur. **Toujours passer par la liste exacte
   des `card_id` déclarés**, jamais par une plage.
2. **Trois `card_id` étaient déjà alphabétiques** (`aav_traitor_minion`,
   `mweb_veranke_minion`, `tah_hellbender_ally`). Couper les deux premiers
   caractères les corrompait en `avv_…`. Laissés tels quels.
3. **`max_id` était un NOMBRE JSON sur le homebrew, une CHAÎNE sur l'officiel.**
   Le renommage produisait du JSON invalide : le moteur ne démarrait plus, et le
   crash handler masquait la cause (lire AU-DESSUS de « During handling of the
   above exception »). Requoté, ce qui aligne le homebrew sur la forme officielle.
   Les checksums ont été recalculés **avec le moteur** (`Types.DictChecksum`).
4. **`.gitignore` ignore `assets/pics/`, mais 16 images y étaient suivies.** Elles
   apparaissaient supprimées sans ajout correspondant. Réajoutées en forcé : 16
   images suivies avant, 16 après.

### Ce que la migration a révélé dans le plateau

`codeMarvelcdb()` mélangeait deux questions : « est-ce un code de carte ? » et
« cette carte a-t-elle une page marvelcdb ? ». Tant que le fan-made empruntait des
numéros officiels, les deux se confondaient. Dès le renommage, **l'aperçu français
des cartes fan-made a cessé de s'afficher** — alors que le commentaire du composant
dit que ce texte est « le seul français que le joueur verra » sur ces cartes.
Séparé en `codeCarteConnu()` / `codeMarvelcdb()`.

C'est exactement le point que le §4 de cette fiche demandait de mesurer. Il a été
trouvé par un test existant, pas par la relecture.

### Ce qui reste à faire

- ~~Le **registre** et le **vérificateur**~~ **FAITS** (`0cc46ac`).
  `tools/prefixes_fanmade.json` déclare les 19 préfixes et dit pourquoi des
  lettres ; `tools/verifier_prefixes.py` refuse quatre silences (card_id en
  double, préfixe non déclaré, fan-made qui emprunte un numéro, numéro de set en
  double). **Les quatre ont été mis en défaut exprès** et refusent bien.
- ~~Les **trois numéros de set en double**~~ **CORRIGÉS** : Spider-Man Rainy, Moon
  Knight et Lockjaw prennent 115, 116, 117. Le numéro sert de rang de tri à la
  galerie, donc deux sets au même rang s'ordonnaient au hasard. Le lien
  fonctionnel passe par le champ `name`, rien d'autre ne bouge. Il fallait les
  corriger avant d'écrire le vérificateur : un vérificateur qui naît rouge
  n'apprend qu'à ignorer le rouge.
- Les points 2 à 5 du §4 (deck-builder, export/import, galerie, repli marvelcdb)
  n'ont pas été éprouvés un par un ; seuls les tests automatisés et la génération
  de cartes les couvrent indirectement.

# Alignement de cinq mots-clés fan-made sur le glossaire MC4DB (29/09/2026)

Source : `https://mc4db.merlindumesnil.net/api/public/rules?locale=en`, entrées
`type == "fanmade"`. Règle de priorité fixée par l'utilisateur : **texte
imprimé sur la carte > glossaire MC4DB > notre fiche**.

Harnais : `.game-src`, port 41000, `PARALLELES=1`, cas filtrés. « Rouge » =
le cas rejoué avec le script d'AVANT (`git show HEAD:…` remis en place le temps
du cas, puis le nouveau restauré et vérifié identique).

| Mot-clé | Décision | Scripts | Fiche |
|---|---|---|---|
| Multiverse | MC4DB (remplacement) | aucun (deckbuilding) | réécrite |
| Breakthrough | MC4DB (excès → principale) | `vv003.py` | mise à jour |
| Armored X | MC4DB (attaque seulement) | `si016.py` | mise à jour |
| Drain X | MC4DB pour `agent_anti_venom` ; insert imprimé conservé pour `venompool` | `agent_anti_venom/__init__.py` | mise à jour |
| Agile X | **texte imprimé conservé** (contredit MC4DB) | aucun | divergence notée |
| Summon | MC4DB (partout hors jeu) | `yondu/__init__.py`, `yondu_nemesis/__init__.py` | mise à jour |

Montage des decks après retrait de la version Multiverse
(`DECK_NOM=… tools/verifier_tous_les_decks.py .game-src 41200`) :
`thor_jane_foster` « identite ra001a, main 6, deck 9 » OK, `black_cat`
« identite bc001a, main 6, deck 9 » OK, `brawn` (inchangé, n'emportait déjà
pas bw003) OK. Éditeur : `node outils/verifier-regles-deck.mjs`, 13/13 dont
4 cas Multiverse.

---

### vv003 : Just a Phase (breakthrough)

- [x] Étape 2 : carte(s) de référence : inchangées (61023, 20013) ; `09031`
      pour `Worlds.FindMainScheme` / `GetMainSchemes`.
- [x] Étape 5 : texte-contre-code : « This thwart gains breakthrough » :
      la carte ne définit pas le mot ; MC4DB : « removed from the main
      scheme ». Le `ChooseAbilities` est retiré, l'excès part sur
      `Worlds.GetMainSchemes(effect)[0]` ; menée visant la principale : excès
      perdu. Résultat : conforme MC4DB.
- [x] Étape 6 : nombres : +3 THW inchangé, excès = voulu − retiré inchangé.
- [x] Étape 7 : cas « la menee en exces passe sur la manigance PRINCIPALE »
      (réécrit : `cibles` sans second choix) vert ; cas « avec DEUX annexes,
      l'exces va a la principale, pas a l'autre annexe » : **rouge avec
      l'ancien script** (il envoyait l'excès sur 01109 via le choix), vert
      avec le nouveau. Les deux autres cas de la carte (crise, patrol)
      toujours verts (4/4).
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay ciblé : non rejoué (aucun changement de
      déclencheur, seule la cible du report change).
- [x] Étape 8 bis : ce qu'on voit (menace sur la principale) : couvert par
      les cas moteur ; pas de rendu spécifique.

Carte terminée : OUI (autoplay non rejoué, assumé).

### si016 : Tony Stark A.I. (Armored 2)

- [x] Étape 2 : `01098` Armored Rhino Suit (`is_from_attack=True`).
- [x] Étape 5 : « Armored 2 » nu ; MC4DB : « damage from an attack ».
      `WhenUnitWouldTakeDamage(..., is_from_attack=True)`. Résultat :
      conforme.
- [x] Étape 6 : X = 2 inchangé.
- [x] Étape 7 : cas « une ATTAQUE de base du heros (ATQ 1) ne le blesse
      pas » (0 subi ; 1 sans module) vert ; cas « des degats HORS attaque
      passent en entier » (3 subis) : **rouge avec l'ancien script** (1
      subi), vert avec le nouveau, témoin d'absence d'effet (reste vert sous
      substitution, assumé). Ancien cas « previent 2 degats a CHAQUE
      instance » supprimé avec son vérificateur `si016_armored_repete`.
      3/3 sur la carte.
- [x] Étape 7 bis : NON.
- [ ] Étape 8 : autoplay non rejoué.
- [x] Étape 8 bis : NON.

Carte terminée : OUI (autoplay non rejoué, assumé).

### av009 : Bear Arms et av007 : Unlikely Allies (Drain X, helper commun)

- [x] Étape 2 : helper `Drain()` du set ; `venompool/__init__.py` pour
      l'autre définition (conservée).
- [x] Étape 5 : les deux cartes n'impriment pas de définition ; MC4DB : « if
      the target took that damage, heal X ». « A subi » lu sur les points de
      vie / la défaite de la cible, PAS sur le retour de `DealDamage` (compte
      les dégâts infligés avant prévention : rendait 1 face à un Tough, cas
      rouge une première fois pour cette raison). Résultat : conforme.
- [x] Étape 6 : X = 1 (av009), 2 (av007) inchangés.
- [x] Étape 7 : cas « drain 1 sur un vilain TOUGH : la carte de statut
      absorbe, AUCUN soin » : **rouge avec l'ancien helper** (identité
      soignée à 2), vert avec le nouveau. Sous substitution du module, ce cas
      reste vert (sans drain : 0 dégât, 3 blessures : témoin d'absence,
      assumé) ; c'est le cas « Hero Action (attaque) : drain 1 sur le vilain »
      qui prouve le module. av009 3/3, av007 2/2 (la branche drain d'av007
      n'a pas de cas dédié : même helper).
- [x] Étape 7 bis : NON.
- [ ] Étape 8 : autoplay non rejoué.
- [x] Étape 8 bis : NON.

Cartes terminées : OUI (autoplay non rejoué, assumé).

### yd001b, yd004, yd012, yd013 (Convoquer) et yd015, yd017, yd018 (ConvoquerRencontre) : summon

- [x] Étape 2 : `an001b`, `ok001b`, `ls005` (recherche joueur), `ag013`
      (recherche rencontre).
- [x] Étape 5 : aucune carte ne définit « summon » ; MC4DB : « anywhere in
      or out of play ». `Search.SearchForCards` avec deck, défausse, main,
      mise de côté, retiré de la partie ; le terrain reste exclu (les cartes
      disent elles-mêmes « if … is not in play »). Une carte déjà en main
      n'est pas re-gagnée. Résultat : conforme.
- [x] Étape 6 : rien de chiffré.
- [x] Étape 7 : cas « la Tahlei convoquee depuis la zone RETIREE DE LA
      PARTIE » et « Sav'rkk RETIRE DE LA PARTIE : summon le ramene quand
      meme » : **rouges avec les anciens helpers**, verts avec les nouveaux.
      Les cas deck / défausse / témoin d'épuisement / Sav'rkk déjà en jeu
      restent verts (yd001b 4/4, yd017 3/3). La mise de côté et la main ne
      sont pas testées (aucune zone Puzzle « mise de côté » ; « déjà en
      main » est un non-événement) : options posées, non prouvées.
- [x] Étape 7 bis : yd001b « Limit once per round » : témoin existant,
      toujours vert.
- [ ] Étape 8 : autoplay non rejoué.
- [x] Étape 8 bis : NON.

Cartes terminées : OUI pour deck / défausse / retiré ; NON prouvé pour la
mise de côté et la main.

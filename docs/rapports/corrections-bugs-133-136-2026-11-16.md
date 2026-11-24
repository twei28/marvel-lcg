# Corrections des rapports de bug 133 à 136 + formulaire public (16/11/2026)

Gabarits de `docs/reference/PROCESSUS-CARTE.md`, un par carte touchée. Rien n'est commité ni déployé à la
date de ce fichier.

## Bug 133 : Excessive Force sur un vilain à plusieurs stades

**Cause (moteur).** Un vilain à plusieurs stades qui perd son dernier PV est VAINCU, puis le stade suivant reprend la
même carte, MÊME NOM, PV remis à fond. `IsDefeated()` relu après les dégâts voyait le stade 2 en pleine forme ;
`IsInPlay()` se contente du nom. **Correctif :** `src/game/card/face/base/villain.py` marque la face du stade vaincu
(`stade_vaincu`, posé dans `OnBeDefeated`) et `IsDefeated()` la lit. Couvre toutes les cartes qui relisent
`cible.IsDefeated()` après leurs dégâts.

### dt083 : Excessive Force
- [x] Étape 2 : référence `35018` Precision Strike (« si cette attaque vainc… ») : même lecture `IsDefeated()`.
- [x] Étape 5 : mots-pièges `defeated`/`damaged` ; « si cet ennemi est vaincu par cette attaque, piochez X » : lu sur l'état
      de la cible après `DealDamage`. Résultat : correct une fois `IsDefeated()` juste.
- [x] Étape 6 : X = ressources payées (2 avec 01088) ; +2 cartes si Tenace retiré. Résultat : conforme au texte.
- [x] Étape 7 : `[stade_vaincu] dt083 … stade 1 achevé (2 PV restants) -> pioche X = 2` ROUGE sans le correctif
      (`main = 0 carte(s)`), VERT avec ; contre-cas « Rhino à 3 PV, 2 dégâts -> aucune pioche » vert dans les deux états.
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : autoplay ciblé non lancé (correctif moteur déterministe, couvert par les cas ci-dessus).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? NON (elle pioche).

Carte terminée : OUI (cas moteur). Reste : partie réelle par un humain.

### 35018 Precision Strike et ch007 Special Delivery (même famille)
- `35018` : `[stade_vaincu] 35018 … soigne 2 degats du heros` ROUGE sans / VERT avec ; contre-cas vert.
- `ch007` testait `not cible.IsInPlay()` (reste vrai sur un vilain qui avance) : corrigé en `cible.IsDefeated() or not
  cible.IsInPlay()`. Cas `[ch] ch007 … ACHEVE le STADE 1 de Rhino` ROUGE sans (`ch011 n'est pas pose sous ch002`) / VERT avec.
- `63018`, `ze005`, `sa006` (autres lecteurs de `IsDefeated()` après dégâts) : verts après le correctif moteur.

Nouveaux cas : `tools/cas/stade_vaincu.py` (4) et 1 dans `tools/cas/shang_chi_b.py`.

## Bug 134 : jeton « son » invisible sur la Setlist de Dazzler

Trois causes : (1) la Setlist est une zone hors jeu, `GetRenderInfo` n'émettait rien, compteurs compris ;
(2) le jeton, posé au coin bas gauche, était sous la carte voisine (les attachées s'étalent vers la droite, seule leur
moitié droite se voit) ; (3) aucun nom français des cartes Dazzler dans `NOMS_FR_FANMADE`.

### dz012 : « Too Good to be True » / dz001a : Rehearsal
- [x] Étape 2 : référence `44009` Armed to the Teeth (même zone `PlaceCardArea`).
- [x] Étape 5 : « place 1 sound counter on a SONG in the Setlist » : le compteur est sur la chanson (déjà vrai) ; seul
      l'ENVOI au plateau manquait. Résultat : conforme.
- [x] Étape 6 : 1 jeton par répétition, une chanson sans jeton à la fois. Résultat : conforme.
- [x] Étape 7 : `[dazzler] dz001a Rehearsal : le jeton sound … EMIS au plateau` ROUGE sans le correctif
      (`info['c_sound'] = None`), VERT avec (`dz012 emet c_sound=1`).
- [x] Étape 7 bis : limite imprimée ? OUI (Rehearsal : une fois par phase) : témoin déjà couvert par le pack (127 cas).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? OUI (compteur).
      Cas plateau : `ui-app/src/board/dazzler-setlist-lightbringr.test.ts` (vert ; le front dessinait déjà tout compteur
      émis, c'est le moteur qui manquait : le ROUGE est le cas moteur ci-dessus).
      **Preuve écran (affichage Normal, FR et EN) :** `captures/dazzler_jeton/` (avant : pas de jeton ; après :
      « 1 SON ») et `captures/dazzler_jeton-en/` (« 1 SOUND »). Spec : `ui-check/tests/dazzler-setlist-jeton.spec.ts`.
      CSS : `board.css`, jetons à droite sur les cartes attachées (`.est-attachee:not(.est-a-gauche)`).
- [x] Noms français (19 cartes, relevés sur les 24 scans) : `noms-fr-fanmade.ts` + test `noms-cartes-fr.test.ts`.
- [x] Même trou sur Blade (signalement : « pareil sur Blade ») : 18 scans posés mais seuls `bl002` à `bl008` avaient un nom.
      Ajout de `bl010`, `bl011`, `bl012`, `bl015`, `bl016`, `bl017` (relevés sur les scans) ; `bl013`/`bl014` identiques à l'anglais.

Carte terminée : OUI. Reste : partie réelle par un humain.

## Bug 135 : « 2 fois alter ego » (téléphone)
Pastille de la face en jeu recopiée sur l'autre face. Déjà corrigé par `ef57bd47` (carrousel, `portrait.css:628`) ;
le serveur n'avait pas ce code. Réglé par le prochain déploiement.
**Vu à l'écran le 16/11/2026** (format téléphone s24, Spider-Man, affichage Normal) : face en jeu = pastille « ALTER EGO », autre
face = aucune pastille (présente dans le DOM, `visibility: hidden`). Captures `captures/autre_face/`, spec
`ui-check/tests/autre-face-telephone.spec.ts`.

## Bug 136 : carte illisible en défense (téléphone)
`DemandeCentrale.tsx` : au téléphone, l'appui sur la vignette ouvre `CarteOuverte` (zoom) sans choisir ; le choix part du
bouton d'action du zoom. Repère « ⤢ » (`board.css`). Tests `DemandeCentrale.test.tsx` : 2 ROUGES sans / VERTS avec.
Preuve écran téléphone : `captures/vignette_zoom/` (spec `ui-check/tests/vignette-telephone-zoom.spec.ts`, projet `s24`).

## Textes encore en anglais (audit du 16/11/2026, demande : « pour tous les héros »)
Relevé : 4 parties jouées par le pilote (Spider-Man, Dazzler, Blade, Captain Marvel), ~250 lignes de journal distinctes, puis
une partie Dazzler lue À L'ÉCRAN (FR, affichage Normal) : `captures/dazzler_textes/textes.txt`, spec
`ui-check/tests/dazzler-textes-anglais.spec.ts`.
- Noms de cartes fan-made dans le journal et les titres de fenêtre (`cartes-journal.ts`, `DemandeCentrale.tsx`) ;
  nom des jetons (« sound » -> « son », « first_player_token » -> « premier joueur », `HistoriquePartie.tsx`, `compteurs-fr.ts`).
- Nouveau `ui-app/src/board/narration-fr.ts` : étapes de mise en place, noms de phase, noms de piles (« Dazzler's PlayerDeck<39> » ->
  « deck de Dazzler »), statuts et mots-clés bruts, noms d'événements du moteur, types d'effet entre parenthèses.
  `vocabulaire-moteur.ts` : « Scenario Setup », « Init Finished ». Tests : `narration-fr.test.ts`, `historique-brut.test.ts`,
  `cartes-journal.test.ts`, `etat-partie.test.ts`.
- ⚠ Limite : la traduction se fait dans le PLATEAU, sur le texte du moteur. Le fichier « Log » téléchargé et le texte joint à un
  rapport de bug restent en anglais.

## Rapports 131 et 132 (anciens)
- 132 (Stand Alone) : commit `200436c2` (14/11, 18:59), `60054` proposée seulement si le héros est déjà incliné. Cas `60054` 2/2 verts.
- 131 (Capturé par Hydra, carte face visible) : commit `8943109c` (14/11, 18:59), captif posé face cachée + règle `tirage_manuel`.
  Cas `[capture_hydra]` 1/1 et `[tirage_manuel]` 4/4 verts.
- Ces deux commits sont sur la branche locale ; le serveur (code du 14/11 11:46) ne les a pas. À passer en « Traité » APRÈS déploiement.

## Formulaire public de rapport de bug
`/signaler-un-bug` (site, sans compte ni table) : frein par adresse, pot de miel, capture réduite dans le navigateur,
FR/EN. Lien sous les pages de connexion et d'inscription. Test : `site/test_bug_public.py` (28 vérifications).

## Vérifications
- Moteur, passes SEULES sur la machine : `[dazzler]` 127/127 ; `[ch]` 87/87 ; `[su` 73/73 ; `[stade_vaincu]` 4/4 ;
  `[briques]` 28/28 (deux fois) ; `[dt` 14/14 (deux fois) ; `Retaliate` 30/30 ; `63018`, `ze005`, `sa006`, `dt075` verts.
- ⚠ Constat honnête : lancées pendant que la suite UI et un navigateur tournaient, certaines passes ont donné des échecs
  (4 cas Dazzler, 4 cas « riposte ») qui passent tous rejoués seuls ; une passe isolée a aussi montré `dt087` et un cas
  `[briques][mechants]` rouges une fois, verts aux 3 rejeux suivants. Cause non identifiée pour cette dernière, jamais
  reproduite.
- UI : vitest 485 fichiers / 5033 tests verts ; `tsc --noEmit` propre.

## Ce qui n'est PAS fait (à dire clairement)
- **Moon Knight** : 20 scans FR posés (`fr_mk*`), aucun nom dans `noms-fr-fanmade.ts`. Décision de l'utilisateur (16/11) : inutile de les combler.
- **Étape 8 (autoplay ciblé)** : non lancée pour `dt083`, `35018`, `ch007`, `dz012`.
- **Rapports 131 et 132** : corrigés dans le code (voir plus haut), toujours « Nouveau » dans l'admin : à classer après déploiement.
- Audit de la famille `IsInPlay()` après dégâts : fait par grep (une seule autre carte concernée, `ch007`) ; pas de preuve exhaustive.
- Partie réelle par un humain : Excessive Force sur Rhino, jeton Setlist, zoom téléphone.

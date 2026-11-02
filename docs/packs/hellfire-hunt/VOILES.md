# Voiles FR de Hellfire Hunt : relevé complet (§1 à §5 : composant d'AVANT ; §6 : état après les corrections du 02/11/2026)

Rendu : `ui-app/outils/export-voile/rendre-voile.mjs` (banc Vite + Chromium) sur les 228 cartes `hfNNN` de `data/cards.json`, scans orientés comme le plateau (complots couchés). Version du voile `13a07d37a9e2` : 186 cartes rendues, 0 erreur, 42 sans texte FR. Toutes les cartes rendues ont été ouvertes avec Read (planches de 3 portraits ou 2 complots). Rendus : `/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/6c912ee0-c9ba-469c-a5ba-e4fc4b30f45a/scratchpad/voiles/cache/hfNNN.jpg` ; planches étiquetées : `.../voiles/lab/P00-P44.jpg` (portraits), `L00-L26.jpg` (complots). Les captures plateau `captures/cassandra-nova-voiles/` (cassandra-nova, cassandra-domination, wild-sentinel, mutant-extinction) ont aussi été vues : voile correct en jeu. Les défauts relèvent du composant (`effacer-texte.ts`, `TraductionPosee.tsx`, autre session) sauf mention DONNÉE.

Limite : rendus du banc `harnais.tsx` (même composant que le site), pas un vrai plateau, sauf les 4 captures ci-dessus.

## 1. Cartes sans aucun texte FR (le scan reste en anglais) : DONNÉE
hf101a, hf101b, hf102a, hf102b, hf103a, hf103b, hf104a, hf104b, hf105a, hf105b, hf106a, hf106b, hf107, hf110, hf111, hf112, hf114, hf115, hf116, hf117, hf118, hf120, hf122, hf124, hf125 (White Queen) ; hf301-hf308, hf311, hf312, hf313, hf317, hf318, hf321, hf322, hf324, hf325 (modules Perfection / Conclave / Delusion). Aucune entrée dans `textes-fr-fanmade.ts`, `textes-fr.ts` ni `textes-fr-complets.ts`. **RÉSOLU le 02/11** : les 42 textes sont écrits (bloc `hellfire_hunt_white_queen` de `textes-fr-fanmade.ts`), relevé des voiles au §5.

## 2. Noms catalogue différents du scan : DONNÉE
- hf509 : scan « PSIONIC PARAGON », catalogue « Psychic Paragon ».
- hf364 : le scan imprime « HELLFIRE CONJURATIOION » (faute du scan), catalogue « Hellfire Conjuration ».
- hf338 : le scan imprime « SEBASIAN SHAW (8/8) » (faute du scan).

## 3. Défauts de voile (composant)
Fragments anglais résiduels (zone de traits ou de bandeau mal effacée) :
- hf342, hf343 : « USIO SIONI » au-dessus de la ligne de traits.
- hf413, hf414, hf415, hf416, hf417 : « SIONI KIL » au-dessus des traits.
- hf418 : « ONDI IO » au-dessus de « CONDITION. ».
- hf332-hf335 : « PE POWE » au-dessus de « SUPER-POUVOIR. » ; hf336, hf337 : un « d » résiduel à droite de la 3e ligne.
- hf404b : « 2A » fantôme et « it. » en bas à gauche. hf406a : bande de fragments anglais illisibles au-dessus du flavor.
- hf604b, hf605b, hf606b : fragments anglais (« a », « nd », « imit », « → ») au bas du cadre, à gauche du badge.
- hf222, hf223 : un « u » résiduel ; la barre de séparation du Boost traverse le texte.
- hf509 : « PSIONIC. » reste au-dessus de « PSIONIQUE. ».
- hf212-hf215 (Ebon Knight) : la ligne anglaise « Guard. Patrol. Quickstrike. » n'est pas effacée, le français est posé dessous (doublon).
- hf419 Dark Temptation : « When Revealed: Selene attacks you. » reste affiché en anglais au-dessus du texte français.

Mise en page :
- hf007 Jump-Start : le texte français démarre au-dessus du cadre, sur l'illustration (« Attachez-la à un » et « SUPER-POUVOIR. » chevauchent l'image).
- hf041 Cerebro Insights et hf045 Rally the Survivors : le texte démarre à gauche du panneau, sur l'illustration (premières lettres coupées) ; hf043 : même débord léger.
- hf030, hf033, hf034, hf036, hf038 : la dernière ligne (« …contrôle. ») passe sous le badge de menace (première lettre coupée). hf031 : l'icône « ! » chevauche « contrôle. ». hf041/hf043 : dernière ligne contre le badge.
- hf381 : « jeu. » touche le bas du cadre ; hf224/hf225 : « Shaw. » touche le cadre ; hf401-hf403 : le flavor frôle la barre du bas.
- hf355, hf356 Jumpstart : le texte frôle le badge « +2 SCH ».

Traces fantômes sans gravité (dans l'illustration) : hf204a « w. », hf205b « wa », hf404a « e », hf405a « et », hf503a « p. », hf604a « o », hf503b une virgule.

## 4. Cartes vues sans défaut notable
- Fondations : hf001-hf006, hf008-hf012, hf013-hf028 (hf015/hf018/hf019 en corps plus gros, lisible), hf032, hf035, hf037, hf039, hf040, hf042, hf044, hf046, hf047, hf048.
- Black King : hf201-hf203, hf204a/b, hf205a/b, hf206, hf207a/b, hf208-hf211, hf216-hf221, hf226, hf227.
- Modules : hf331, hf338, hf361-hf366, hf371-hf376, hf382-hf388, hf381, hf388.
- Black Queen : hf401-hf403, hf404a, hf405a/b, hf406b, hf407a/b (« Under the Moonlight » / « Beneath the Sun » restent en anglais dans le corps : nom de carte, voulu), hf408-hf412, hf420, hf421, hf422.
- Torn : hf341, hf344-hf348, hf351-hf358, hf501a, hf501b, hf502a, hf502b, hf503a/b, hf504a/b, hf505-hf508, hf510.
- Cassandra Nova : hf601, hf602, hf603, hf604a, hf605a, hf606a, hf607-hf619, hf620, hf621.

Aucune section « reste à regarder » : toutes les cartes rendues ont été vues.

## 5. White Queen (hf101-hf125) et modules Perfection / Conclave / Delusion : voiles du 02/11
Textes posés dans `textes-fr-fanmade.ts` (bloc `hellfire_hunt_white_queen`), JS public régénéré. Rendu : `rendre-voile.mjs`, version du voile `13a07d37a9e2`, 42 cartes rendues, 0 erreur, les 42 images vues (planches `.../scratchpad/wq/VP00-VP10.jpg`, `VL00-VL04.jpg`, rendus `.../scratchpad/wq/cache/hfNNN.jpg`). Texte saisi comparé au scan : identique au catalogue pour les 42 cartes. Composant non modifié.

Défauts (composant, sauf mention) :
- Doublon anglais non effacé, français posé dessous : hf114, hf115, hf116, hf117 (Phantom Warrior : « Guard. Steady. Toughness. » reste au-dessus de « Garde. Solide. Ténacité. ») ; hf313 Hellfire Pawn (« Guard. Patrol. Surge. »). Même défaut que Ebon Knight hf212-215 : cartes dont la seule ligne de mots-clés est suivie du Boost.
- Débord du texte hors du cadre : hf122 Psionic Fortification (« COMPÉTENCE. Une fois révélée : si » remonte sur l'illustration, texte trop long pour la zone) ; hf304 Illusory Defender (dernière ligne « d'illusion. » rognée sous le cadre, texte trop long).
- hf317 The Hellfire Conclave : « HELLFIRE » de la dernière ligne mordu par le badge « 9 » ; un « 1 » anglais résiduel sous « Incitation 1. » ; la ligne d'ambiance démarre à cheval sur le bord gauche du cadre.
- Icônes de boost en bas à droite délavées (grises au lieu de rouges) : hf111, hf120, hf304.
- Fragments anglais fantômes : hf104a un « a » sous « et White Queen (A2) » ; hf105a « army » sous le texte d'ambiance (et un « : » orphelin en début de ligne, effet de retour à la ligne) ; hf106b une trace « .com » au-dessus de « Si ce stade est achevé » ; petites taches blanches sur le bord droit du cadre (hf101a/b, hf102a/b, hf103a/b, hf301, hf302, hf303, hf304, hf306, hf313, hf114-117, hf124, hf318).
- hf125 : la ligne d'ambiance chevauche le bord gauche du panneau (premières lettres collées au cadre).
- DONNÉE (traits-fr.ts) : les traits DIAMOND, HELLFIRE et ILLUSION restent affichés tels quels sur la ligne de traits (« DIAMOND. HELLFIRE. », « ILLUSION. PSIONIQUE. ») : PSIONIC, ELITE et SKILL sont traduits, pas ces trois-là. À trancher (laisser en anglais comme pour les autres noms propres, ou « DIAMANT »).
- Sans défaut notable : hf101a, hf102a, hf103a (hors tache), hf107, hf110, hf112, hf118, hf301, hf302, hf303, hf305, hf306, hf307, hf308, hf311, hf312, hf321, hf322, hf324, hf325, hf104b, hf105b, hf106a, hf318, hf124.

## 6. Corrections du composant de voile (02/11/2026) : état final carte par carte

Composant corrigé : `ui-app/src/board/effacer-texte.ts`, `TraductionPosee.tsx`, `zones-corrections.ts` (hf122 seulement). Version du voile `5ad855362c82`. Rendus avant/après des 228 cartes hf par `rendre-voile.mjs` (planches de comparaison lues une à une dans la session), plus 63 cartes de non-régression choisies (gabarits et rapports de voile : sq015, bg014, bg001a/c, hz001b, bm016/017, bm001a, rm001a/b, rm014, co001a, uw001b/010/015, sv004/015, sz001a/004/005/009/011/013, so014, sy004/006/024/025/029/037/038/046, sl*, wt018/019, tk001a/010, vt001/020, officielles 01001a, 02020, 04010, 22011, 27010, 40016...) et 404 autres cartes tirées au hasard (170 fan-made et 260 officielles traduites ; 186 changées, toutes petites sauf des re-mises en page du texte, vues sur un échantillon d'une quarantaine).

Règles générales ajoutées (chacune a ses tests unitaires, écrits avant et vus rouges, sauf mention) :
1. Un filet noir fin plein largeur (séparateur du Boost) n'est plus pris pour le bord haut du cadre : les lignes de mots-clés / traits au-dessus de lui sont effacées (doublon anglais « Guard. Patrol. »).
2. Les lettres en GRAS (ligne de traits « ILLUSION. PSIONIC. ») ne sont plus écartées par le test « du clair autour » (elles remplissent leur boîte et celles de leurs voisines).
3. Une grande tache haute qui touche un côté de la région (liseré argenté / noir du cadre) n'est plus effacée comme « lettre collée » au bout d'une ligne (taches blanches sur le bord droit).
4. Une tache franchement colorée (icône de boost rouge) n'est plus effacée (icônes délavées).
5. Un morceau de cadre haut comme trois lettres n'entre plus dans les « lettres » (il tirait le bord gauche du texte contre le cadre).
6. Dernière lettre d'une ligne coupée par le bord droit de la région (encre noire seulement) effacée (« u » de hf222, « d » de hf336).
7. Séparateur du Boost qui touche un bord de la région, avec du texte des deux côtés : effacé (le français dessine le sien).
8. Mots collés en deux taches (« PSIONIC. »), derniers mots d'un paragraphe alignés à la marge gauche (« 2A. », « it. »), et mot collé non écarté par une tache lointaine à la même hauteur (« army »).
9. Cadre penché reconnu sans liste (au moins 8 lignes sur une droite à 0,9 % de la carte près, une ligne aberrante tolérée) : le français suit le départ des lignes (hf041 : premières lettres des 3 premières lignes perdues sous le bord).
10. hf122 : correction de zone manuelle (`ZONES_CORRECTIONS`, y0 0,575) : la détection prenait l'illustration pour le haut du cadre. Pas de règle générale (tentative de filtre « éclats du dessin » abandonnée : elle faisait régresser sq015 et aa018).

Corrigé (vu après) : hf114-hf117, hf313, hf212-hf215 (doublon) ; hf122 ; hf304 (dernière ligne entière) ; hf111, hf120, hf304 (icônes de boost rouges) ; hf104a, hf105a, hf106b (fantômes) ; taches blanches du bord droit (hf101a/b, hf102a/b, hf103a/b, hf114-117, hf124...) ; hf342, hf343, hf413-hf417, hf418, hf419 (anglais restant effacé), hf332-hf335 ; hf336, hf337 (« d ») ; hf404b (« 2A » ; « it. » ne laisse qu'un point) ; hf509 (« PSIONIC. ») ; hf222, hf223 (séparateur et « u ») ; hf007 (texte entièrement dans le cadre) ; hf041, hf043 (début des lignes) ; hf125 (ligne d'ambiance dans le cadre) ; hf317 (« 1 » fantôme, début des lignes) ; hf042, hf044, hf046, hf047 (départ des lignes décalé du bord).

Reste (impossible à corriger proprement sans changer la mise en page autour des badges, tentative `bordGaucheLibre` abandonnée : elle déplaçait le texte de 211 cartes) :
- hf317 : « HELLFIRE » de la dernière ligne mordu par le badge « 9 ». hf030, hf033, hf034, hf036, hf038 : dernière ligne contre le badge de menace (première lettre coupée sur hf030 et hf038). hf031 : l'icône « ! » chevauche « contrôle. ». hf381 : « jeu. » touche le bas du cadre.
- hf045 : le « V » / « a » de début de ligne touche le bord (l'anglais y touche aussi). hf604b, hf605b, hf606b : fragments « a », « nd », « imit », « → » contre le badge (sur le dessin, hors colonne). hf406a : fragments gris au-dessus du flavor (fond dégradé gris). hf606b : un « d, » isolé. hf222, hf223, hf337 : un point ou deux au bord droit.
- Traits : DIAMOND n'existe sur aucune carte officielle (laissé tel quel). ILLUSION : le français officiel le garde (« ILLUSION. », scans 16074, 27089 : déjà dans `traits_fr_maison.json`). HELLFIRE : les scans français officiels 49038 et 32058 impriment « DAMNÉS. ». Proposition NON appliquée (`traits-fr.ts` est généré par `tools/generer_traits_fr.py` + `traits_fr_maison.json`, dans la copie du moteur) : ajouter `"HELLFIRE": "DAMNÉS"` à `traits_fr_maison.json` et régénérer ; à confirmer par l'utilisateur (pluriel imprimé même sur un sbire seul).

Régressions : aucune vue sur les 63 + 404 cartes. Effets de bord visibles : le français est un peu plus gros sur certaines cartes (pd001a, hf212-215, hf419) parce que l'interligne mesuré change quand une ligne fantôme n'est plus comptée ; il tient dans le cadre. Les 2 tests rouges de la suite complète (`site-langue.test.ts`, `cartouche-phase.css.test.ts`) le sont aussi sans mes changements.

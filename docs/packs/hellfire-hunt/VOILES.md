# Voiles FR de Hellfire Hunt : relevé complet (composant de voile NON modifié)

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

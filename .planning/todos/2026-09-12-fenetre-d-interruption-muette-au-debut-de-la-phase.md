# En mode Détaillé, une fenêtre d'interruption ouverte AVANT la première étape de la phase du méchant n'a aucun bouton : le joueur est bloqué

**Trouvé le 12/09/2026** en montant la partie d'observation « un sbire entre
en jeu en pleine phase » (Spider-Man en forme héros contre Ultron, serveur
local, script Playwright jetable, non conservé).

## Ce qui se passe

Fin du tour du héros. La phase du méchant commence par le point 1 (menace
sur le complot principal). Spider-Man tient *De Grandes Responsabilités*
(Interrupt : « quand de la menace va être placée… »). Le moteur ouvre donc
une fenêtre : `event=WhenSchemeWouldPlaceThreat`, `show_cancel=true`,
`options=[Play#27]`, prompt « Le Crimson Cowl s'apprête à recevoir 1 menace ».

À l'écran (capture `2026-09-12-fenetre-d-interruption-muette-capture.png`, à côté de cette fiche) : bandeau « ROUND 1 · Phase
du méchant · Menace · À TOI DE JOUER », la table, et **rien pour répondre** :
pas de cartouche, pas de panneau central, bouton « Fin du tour » désactivé
(« possible quand le moteur te rend la main »), Échap sans effet. Le moteur
attend sans limite (`timeout: 0`).

## La cause, lue dans le code

`board.tsx` : `questionEnScene = modePhase === 'detaille' && phaseMechantEnCours
&& afficherDemandeCentrale && demande` → vrai. La question est donc retirée
du panneau central (`!questionEnScene` sur `<DemandeCentrale>`) et passée à
`DeroulePhase` par sa prop `question`.

`DeroulePhase.tsx` : `if (!etape || termine || partieFinie) return null` vient
AVANT la branche `est-question`. Or aucune étape n'existe encore : le fait
`menace` n'est enregistré qu'APRÈS le placement, et la fenêtre s'ouvre
avant. Le cartouche rend `null`, la question n'a plus d'écran.

Même mécanique pour toute interruption « would… » qui précède le premier
fait de la phase : *Great Responsibility*, *Emergency* (Interrupt quand le
méchant manigance… en phase 2 le point 1 a déjà créé une étape, donc a
priori seul le point 1 est exposé), et tout Interrupt sur « la menace va être
placée ».

## Ce qu'il faudrait

Rendre la branche `est-question` même sans étape (chronologie vide, la carte
scène absente), ou, sans étape, laisser la question au panneau central
(`questionEnScene` exigeant au moins une étape connue). La seconde est la
plus sûre : elle ne touche pas au cartouche.

**Décision utilisateur du 12/09/2026 : corriger, et faire aussi l'étape
d'entrée du sbire.**

## ✅ CORRIGÉ LE 12/09/2026

`DeroulePhase.tsx` : sans étape, si le moteur pose une question au joueur
local (`questionAuJoueur && question`), le cartouche rend la branche
`est-question` (bandeau « À toi de jouer » + la question, sans chronologie
ni scène) au lieu de `null`. Test `deroule-integration.test.tsx`, « montre la
question du moteur même avant la première étape de la phase » (faux serveur
avec une trame sans fait et une fenêtre `WhenSchemeWouldPlaceThreat`).

## Suite du 12/09/2026 : « pour un nouveau joueur c'est pas du tout user-friendly »

Retour de l'utilisateur sur Miss Hulk : « I Object! » de Jennifer Walters
s'ouvre avant la menace, rien ne l'indique, il fallait cliquer la carte. Le
blocage ci-dessus en était la cause en prod ; et une fois la question
affichée, elle ne disait ni ce que fait la capacité, ni ne montrait la carte.

**Décision** (question une à une) : afficher le texte de la capacité, même
en anglais. **Livré** : `estFenetreDeReaction` (show_cancel + Interrupt /
Response, ou événement When/After hors tour) ; le titre du moteur sans sa
parenthèse technique ; la phrase « Jennifer Walters peut réagir » (« Tu peux
réagir » à plusieurs porteurs) ; la vignette de la carte porteuse toujours
affichée ; sous le bouton, le texte de la capacité (`texte-capacite.ts` :
français de `TEXTES_FR` / fan-made quand il existe, sinon l'anglais de
cards.json par `Catalogue.texte`, paragraphe retrouvé par le nom de l'option
puis par le type). Vu en jeu, capture : la carte, « I Object! — Interrupt:
When threat would be placed on a scheme, prevent 1 of that threat », Passer.

## Retour du 12/09/2026 : « c'est moche, les tailles ne sont pas bonnes, et pourquoi de l'anglais en FR »

Capture : la jauge « 15 / 15 » de la vignette recouvrait le bouton, « Passer »
s'étirait à la hauteur de la colonne vignette + texte, le titre citait
« Underground Distribution » et le texte de la capacité était en anglais.

**Livré** :
- mise en page : les boutons s'alignent par le bas (`.dc-boutons`), la
  vignette réserve la place de sa jauge (`--jauge-debord`), le texte des
  capacités passe dans un bloc sous la rangée des boutons (`.dc-capacites`) ;
- les cartes citées par le moteur (« [(48,01097b) The Break-In!] ») sont
  nommées en français (`sansIdentifiantsEnFrancais`, noms-fr.ts) ;
- le texte de la capacité en **français officiel** pour toutes les cartes :
  nouveau `tools/generer_textes_fr_complets.py` (fr.marvelcdb.com, filtre de
  sincérité contre l'anglais, 3 387 cartes) → `textes-fr-complets.ts`
  (720 Ko), chargé par import dynamique à la première fenêtre de réaction,
  anglais de cards.json en attendant ; `extraireCapacite` retrouve le
  paragraphe français depuis le type anglais du moteur (Interrupt →
  Interruption, Forced Response → Réponse forcée…) ;
- le bouton porte le nom français de la capacité quand le texte le donne
  (« "Objection !" — » → bouton « Objection ! »).

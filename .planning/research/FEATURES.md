# Feature Research

**Domain:** UI/UX d'un client de jeu de cartes numérique coopératif (LCG solo/coop, PC + tablette + mobile)
**Researched:** 2026-07-28
**Confidence:** MEDIUM-HIGH

> Périmètre : les « features » de ce document sont des **capacités d'interface et des patterns de design**, pas des règles de jeu. Le moteur est intouchable (contrainte projet). Tout ce qui suit doit se construire au-dessus des descripteurs JSON déjà produits par `src/game/render/to_descriptor.py`.

---

## Synthèse en 10 lignes

1. Le problème central d'un LCG numérique n'est pas le look, c'est la **densité d'information** : afficher beaucoup de texte de règles sur peu de surface, sans zoom ni panoramique.
2. Les trois écoles de représentation de carte sont identifiées et documentées : Hearthstone (carte digitale native + tooltips), Legends of Runeterra (minimalisme, art plein cadre, gabarits par catégorie), MTG Arena (fidélité au carton, au prix de l'UX numérique).
3. Le projet a des **scans de cartes réelles** comme seule source d'art. Il hérite donc du problème MTG Arena. La sortie est la **double représentation** : tuile lisible sur le plateau, scan complet à l'inspection.
4. Zones explicitement délimitées et étiquetées : c'est le facteur numéro un de lisibilité d'un plateau à nombreuses zones.
5. Un moteur qui automatise tout impose deux surfaces critiques souvent négligées : la **barre de demande (ask)** et le **journal de partie**. Sans elles, le joueur ne comprend pas ce qui vient de se passer.
6. Le « dark premium art-forward » est la mode du genre, et c'est aussi là que Gwent s'est cassé les dents sur la lisibilité du plateau.
7. Marvel Snap donne la référence d'art direction Marvel : la hiérarchie visuelle sert les cartes, halftone en hommage, éléments interactifs poussés vers le bas de l'écran.
8. Les adaptations mobiles ratées partagent un symptôme : tout compresser au lieu de **naviguer entre les zones**.
9. Les animations sont un piège classique : informatives et interruptibles, ou elles deviennent la première plainte des joueurs.
10. Aucun client officiel Marvel Champions numérique n'existe pour servir d'étalon (vérifié, voir Sources). Les concurrents de fait sont MarvelCDB, DragnCards et Tabletop Simulator.

---

## Feature Landscape

### Table Stakes (Users Expect These)

Sans ces éléments, l'interface est perçue comme cassée ou datée. C'est exactement le registre de la douleur exprimée par l'utilisateur.

#### A. Coquille applicative et navigation

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Hub d'accueil avec action primaire unique et évidente (« Reprendre » ou « Nouvelle partie ») | Tous les clients modernes ouvrent sur une action, pas sur un sommaire | LOW | La critique récurrente de LotR ACG porte sur un menu à grands boutons où la navigation ne suit pas la direction attendue |
| Navigation persistante avec **libellés texte**, pas seulement des icônes | Les icônes non universelles ne sont identifiables qu'après clic (défaut documenté de Marvel Snap) | LOW | Barre latérale sur desktop, barre basse sur mobile |
| Écran de réglages centralisé (vitesse d'animation, taille de texte, thème, son, langue) | Standard de genre depuis 2020 | MEDIUM | Doit persister côté client, pas côté moteur |
| États de chargement explicites (squelettes, jamais d'écran vide) | Le backend fait du long-polling : les temps d'attente sont visibles | LOW | Une requête HTTP = une action de jeu dans l'architecture actuelle |
| Retour arrière fiable et non destructif partout | Attente web de base | LOW | Nécessite un routage propre, aujourd'hui inexistant (pages HTML séparées) |

#### B. Préparation de partie

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Wizard à étapes avec stepper visible, position courante et navigation arrière | Le plan `PREPARE-UI-PLAN.md` le prévoit déjà en 6 étapes | MEDIUM | Remplace l'écran monolithique de 2251 lignes |
| Récapitulatif persistant des choix (panneau latéral ou barre) | L'utilisateur doit voir sa configuration sans revenir en arrière | MEDIUM | Dépend d'un store d'état centralisé |
| Validation en ligne avec raison de blocage explicite sur le bouton final | « Lancer » grisé sans explication est le classement numéro un des frustrations de setup | MEDIUM | Les formulaires de campaign log actuels ont une intégration incomplète (voir CONCERNS.md) |
| Galerie de héros visuelle (art, aspect, difficulté) plutôt qu'une liste déroulante | Standard depuis Hearthstone ; déjà partiellement présent | LOW | La galerie dynamique existe, il manque la mise en forme |
| Sélection de deck : deck de départ, deck perso, import MarvelCDB | Attente du public LCG, déjà supporté par le moteur | MEDIUM | L'import MarvelCDB est un acquis à mettre en valeur, pas à cacher |
| Mémorisation de la dernière configuration + relance en un geste | Le joueur solo relance souvent la même config | LOW | Très fort ratio valeur/coût |
| Reprise de partie sauvegardée depuis l'accueil | Le moteur sait sauvegarder/charger | LOW | Aujourd'hui peu ou pas exposé |
| Aide contextuelle sur les champs de campaign log | Champs opaques identifiés comme lacune (« no guidance ») dans CONCERNS.md | MEDIUM | Texte d'aide par champ, pas une doc externe |

#### C. Galerie de cartes et deck builder

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Recherche instantanée sur nom et texte, sans rechargement | MarvelCDB est la référence du public visé (« fast, powerful and exhaustive ») | MEDIUM | Index côté client sur `cards.json` (2,3 Mo) |
| Filtres à facettes : aspect, type, coût, traits, set/pack, icônes de ressource, joueur/rencontre | Exactement les axes de tri exposés par MarvelCDB | MEDIUM | Les facettes doivent être combinables et effaçables d'un geste |
| Bascule vue grille (scans) / vue liste dense | MarvelCDB offre Checklist, Spoiler, Full Cards, Scans, Simple List | MEDIUM | La liste dense est indispensable sur mobile et pour le deckbuilding rapide |
| Panneau de détail carte avec texte de règles **lisible** (texte réel, pas seulement le scan) | Le scan seul est illisible en dessous d'un seuil ; défaut cité pour LotR ACG (« text difficult to read without squinting ») | MEDIUM | Les données texte existent dans `cards.json` : à afficher en typographie native |
| Ajout/retrait au clic avec stepper de quantité et limite de copies visible | Attente de tout deck editor | LOW | Feedback immédiat obligatoire |
| Statistiques de deck en direct : total, courbe de coût, répartition aspect/type | Moxfield/MTG Arena ont fixé le standard, y compris l'affichage de la courbe en haut d'écran | MEDIUM | `card_statistics.js` existe déjà comme base |
| Validation de légalité en direct avec message clair | Sinon la partie échoue au lancement | MEDIUM | Doit refléter les règles du moteur, sans les réimplémenter (voir anti-features) |
| Import / export MarvelCDB conservés et rendus visibles | Acquis fonctionnel du client actuel | LOW | Ne pas régresser |

#### D. Plateau en partie (surface la plus critique)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Double représentation de carte** : tuile lisible sur le plateau, scan complet à l'inspection | Le zoom/panoramique sur un plateau de cartes est unanimement décrit comme une expérience ratée ; la tuile doit porter nom, coût, stats, icônes, statut, art recadré | HIGH | **Le composant le plus important de tout le projet.** Dépendance de la galerie, du deck builder et du plateau |
| Inspection non modale et instantanée : survol (desktop), appui long (tactile), raccourci clavier | Reproche explicite fait à LotR ACG : « you must click it » au lieu de survoler | MEDIUM | Doit être annulable, ne jamais bloquer, ne jamais masquer la carte concernée |
| Zones explicitement délimitées **et étiquetées** : vilain, schéma principal, schémas secondaires, deck/défausse de rencontre, et par joueur identité, alliés, améliorations/soutiens, main, deck/défausse, ressources | La définition claire des zones de jeu est identifiée comme condition de base d'un plateau lisible | HIGH | Un plateau coop à 4 héros a 20+ zones : c'est le vrai défi de mise en page |
| Indicateur de phase/tour permanent + rappel de l'action attendue | DragnCards en fait un élément de premier plan (Phase/Step Tracker + phase helper text) ; Marvel Snap est critiqué pour un indicateur de tour trop subtil | MEDIUM | Doit répondre à « c'est à qui, on est où, qu'est-ce qu'on attend de moi » |
| **Barre de demande (ask)** explicite : intitulé de la demande, options, annuler/passer | Le moteur pilote tout par des demandes ; c'est le point de contact principal du joueur | HIGH | Remplace les prompts actuels jugés confus. Un emplacement fixe, jamais une modale surgissante aléatoire |
| Surlignage des cibles valides et grisage des cibles invalides | Attente de genre ; évite le clic à l'aveugle | MEDIUM-HIGH | **Dépendance backend** : le descripteur doit exposer les cibles légales. Sinon le client devrait deviner, ce qui est interdit |
| Compteurs lisibles directement sur les cartes : dégâts, menace, épuisement, statuts (tough/stunned/confused), ressources, compteurs génériques | Sans cela le joueur inspecte en boucle | MEDIUM | Puces à fort contraste posées sur la tuile, jamais du texte fin dans l'art |
| Journal de partie consultable | Quand le moteur résout automatiquement des chaînes d'effets, le journal est la seule réponse à « que s'est-il passé » ; DragnCards en fait une zone permanente | MEDIUM | Il existe un flux d'événements côté moteur : la matière première est là |
| Annuler (undo) accessible depuis le plateau | Le moteur gère l'undo (`game_over.py`) ; en solo c'est une attente forte | MEDIUM | Doit être visible, pas caché dans un menu |
| Main en rangée superposée avec dépliage au survol/focus, cartes jouables distinguées | La main est le point d'interaction le plus fréquent | MEDIUM | Voir note sur l'éventail dans les anti-features |
| Aucune occlusion des cartes concernées par les surcouches | Plainte documentée sur MTG Arena : la pile masque les cartes en dessous et bloque les interactions | MEDIUM | Règle de conception : les panneaux se poussent, ils ne se superposent pas aux zones actives |
| Animations informatives : origine et destination des cartes, cible des dégâts, source du déclenchement | Slay the Spire est cité en exemple : les traînées de cartes tirées/défaussées aident à comprendre le flux | MEDIUM-HIGH | Une animation qui ne dit rien est du bruit |
| Réglage de vitesse d'animation + interruption possible | Plaintes massives et anciennes sur Hearthstone ; considéré comme option d'accessibilité | LOW | Slay the Spire autorise à jouer plus vite que les animations : c'est le comportement cible |
| Confirmation des actions irréversibles uniquement | Confirmer tout tue le rythme | LOW | Coupler avec undo plutôt que multiplier les confirmations |

#### E. Mobile et tablette

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Cibles tactiles généreuses (44 px minimum) et zéro dépendance au survol | Base tactile | MEDIUM | Chaque affordance de survol doit avoir un équivalent appui/appui long |
| Éléments interactifs regroupés dans la moitié basse de l'écran | Choix explicite de Marvel Snap sur l'ergonomie du pouce | LOW-MEDIUM | Sur téléphone, main + boutons d'action en bas |
| **Navigation entre zones** sur petit écran plutôt que compression de tout le plateau | Le symptôme des adaptations ratées est de tout écraser | HIGH | Onglets de zones, carrousel d'aires de joueur, ou vue d'ensemble + focus |
| Paysage privilégié en partie, portrait supporté au moins dans les menus | Un plateau de cartes est intrinsèquement paysage | MEDIUM | Prévoir un message d'invitation à tourner l'appareil, pas un blocage brutal |
| Prise en compte des zones sûres (encoche, barres système) | Base mobile 2026 | LOW | `env(safe-area-inset-*)` |
| Bouton d'action principale toujours atteignable au pouce, jamais sous un doigt qui tient l'appareil | Marvel Snap est critiqué pour des boutons Fin de tour / Abandon mal placés que l'on clique par erreur | LOW | Ne pas coller les actions destructrices aux actions fréquentes |

#### F. Accessibilité (table stakes en 2026)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| L'information n'est jamais portée par la seule couleur | Les aspects Marvel Champions sont codés rouge/jaune/bleu/vert : le couple rouge/vert est le cas de deutéranopie le plus courant | LOW | Toujours coupler couleur + icône + libellé |
| Taille de texte réglable | Un LCG est un jeu de texte dense | MEDIUM | Impose une mise en page fluide, à décider dès le design system |
| Respect de `prefers-reduced-motion` | Standard web | LOW | Se branche sur le réglage de vitesse d'animation |
| Contrastes vérifiés sur le texte de règles et les compteurs | Le reproche « lire en plissant les yeux » est le pire retour possible | LOW | Tokens de contraste dans le design system |
| Navigation clavier utilisable sur desktop | Attendue par les joueurs PC réguliers | MEDIUM | Voir raccourcis en différenciateur |

---

### Differentiators (Competitive Advantage)

Ce qui ferait de ce client le meilleur client Marvel Champions existant, officiel ou non.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Tuiles adaptatives** : la taille des cartes du plateau s'ajuste à l'encombrement de la zone, avec dépliage au survol/focus | Résout structurellement le plateau surchargé, là où MTG Arena souffre encore | HIGH | Dépend du composant carte à double représentation |
| **Vue d'ensemble** du plateau (dézoom sémantique, pas un zoom optique) | Répond à « où en est la partie » en un geste, indispensable en coop multi-héros | MEDIUM | À ne pas confondre avec un pan/zoom libre (anti-feature) |
| **Journal riche et cliquable** : chaque entrée renvoie à la carte, filtrable, avec « rejouer le dernier événement » | Transforme l'automatisation du moteur d'opacité en pédagogie. Aucun concurrent communautaire ne le fait bien | HIGH | Dépend d'un flux d'événements exploitable dans le descripteur |
| **Rappels de règles sur les mots-clés** (tooltips sur Vengeance, Guard, Retaliate, Confused...) | Bénéfice numérique pur, école Hearthstone. Élimine les allers-retours vers le PDF | MEDIUM | Nécessite une table mot-clé → texte, à produire une fois |
| **Prévisualisation d'impact** : effet chiffré d'une action avant validation | Le différenciateur le plus fort possible pour un LCG solo | HIGH | **Doit venir du moteur**, jamais d'un calcul dupliqué côté client |
| Coût payable calculé et ressources disponibles affichées en permanence | Supprime le comptage mental, source d'erreurs et de lenteur | MEDIUM | Le moteur connaît déjà les coûts payables (il propose les actions) |
| Recherche et filtres **dans les zones du plateau** (défausses, deck de rencontre, mis de côté) avec le même moteur que la galerie | Réutilisation élégante d'un composant, valeur immédiate | MEDIUM | Dépend du moteur de recherche de la galerie |
| **Suivi de campagne visuel** : progression, log lisible et éditable avec libellés explicites | La tenue de campagne manuelle est identifiée comme la lacune la plus pénible du client actuel | HIGH | Forte valeur : 4 formats de campagne concernés (MTS, MG, NeXt, AoA) |
| **Replay avec timeline navigable** | Le système de replay existe mais reste brut ; une timeline en fait un outil d'apprentissage | HIGH | Acquis technique sous-exploité |
| Écran de fin de partie riche (récapitulatif, statistiques, faits marquants) | Le moment de récompense émotionnelle, aujourd'hui inexistant | MEDIUM | `report.html` et le module statistiques existent |
| Gestion élégante du **solo multi-héros** (2 à 4 aires jouées par une personne) | Cas d'usage dominant du public solo, très mal traité partout | HIGH | Aire active en grand, autres aires en bandeaux repliés avec compteurs clés |
| Raccourcis clavier + palette de commandes sur desktop | DragnCards a validé l'appétit du public LCG pour les raccourcis (touche TAB pour la liste) | MEDIUM | Doit être découvrable, sinon inutile |
| Design system documenté avec thèmes commutables | Rend le choix de direction visuelle réversible et peu coûteux | MEDIUM | Voir section Directions visuelles |
| Sons discrets et retour haptique tactile | Renforce la compréhension sans allonger les animations | LOW-MEDIUM | Des sons existent déjà dans `assets/sounds/` |
| Installation en PWA / plein écran | Rend le client local « vrai app » sur tablette | LOW-MEDIUM | Contrainte : tout doit rester self-contained dans `public/` |
| Presets de configuration nommés (« ma partie test », « campagne en cours ») | Réduit la friction de relance à néant | LOW | Extension naturelle de la mémorisation de config |

---

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Boutique, monnaie, lootbox, saison, battle pass, « quêtes journalières » | Ce sont les patterns visuels que le joueur a l'habitude de voir dans Marvel Snap / Hearthstone, donc ils semblent « professionnels » | Aucun sens pour un client local personnel ; occupent l'espace de navigation le plus précieux (Marvel Snap est critiqué pour un menu d'accueil « super packed » avec une section actualités redondante) | Consacrer la navigation au jeu, à la collection et aux campagnes |
| Plateau 3D, caméra libre, pan et zoom obligatoires pour tout voir | Semble résoudre le manque de place | Zoomer et se déplacer sur un plateau de cartes est explicitement identifié comme une expérience désastreuse ; détruit la lecture en un coup d'œil | Zones fixes, tuiles adaptatives, dézoom sémantique, navigation par zone sur mobile |
| Plateau très sombre avec art plein cadre partout | C'est la mode « premium » du genre | Cas d'école Gwent Homecoming : lisibilité du plateau dégradée, joueurs décrivant une sensation de « grande forêt ». Les zones deviennent indistinguables | Hiérarchie de luminosité entre zones, en-têtes de zone étiquetés, art contenu dans les cartes |
| Afficher uniquement les scans de cartes, à toutes les tailles | Fidélité au carton, familiarité | C'est le piège assumé de MTG Arena : fidélité physique au prix de l'UX numérique. Avec des scans MarvelCDB, le texte est illisible en dessous d'un certain seuil | Double représentation : tuile native sur le plateau, scan à l'inspection |
| Éventail de cartes très incliné en main | Imite le carton et Hearthstone | La rotation dégrade la lisibilité du texte, complique les cibles tactiles et gâche la place sur petit écran | Rangée superposée, léger décalage, dépliage au survol/focus. Réserver l'inclinaison au desktop grand écran, purement décorative |
| Drag and drop comme **seul** moyen de jouer une carte | C'est le geste « naturel » du carton | Précision insuffisante au doigt, pénible sur trackpad, inaccessible au clavier | Appui pour sélectionner puis appui sur la cible, avec le drag comme raccourci optionnel |
| Flèches de ciblage permanentes entre toutes les cartes liées | Rend les liens explicites | Une couche de flèches est décrite comme invasive et inélégante ; sur un plateau coop à 20+ zones cela devient un plat de spaghettis | Flèche temporaire pendant le geste de ciblage, puis surlignage source/cible et rattachement visuel des améliorations à leur porteur |
| Cinématiques d'activation de vilain, longues animations non interruptibles | « Ça fait AAA » | Première plainte historique des joueurs de jeux de cartes numériques ; insupportable dès la deuxième partie | Feedback court, informatif, interruptible, avec réglage de vitesse et possibilité de jouer par-dessus l'animation |
| Réimplémenter des règles côté client pour prédire ou valider | Nécessaire en apparence pour la prévisualisation d'impact et la validation de deck | Viole la contrainte absolue du projet et crée deux sources de vérité qui divergeront silencieusement | Faire exposer l'information par le moteur via le descripteur ou un endpoint de lecture. Si le moteur ne le sait pas, la feature est reportée, pas devinée |
| Disposition du plateau entièrement personnalisable (glisser-déposer des zones) | Séduit les power users | Coût énorme, dette de mise en page, casse le responsive, valeur faible en solo | Deux ou trois présélections de disposition (compacte, confort, mobile) |
| Tutoriel scripté complet du jeu | Semble indispensable pour un jeu complexe | Coût de production immense, obsolète à chaque évolution, et le public cible connaît déjà les règles | Aide contextuelle, tooltips de mots-clés, texte d'aide de phase |
| Automatisation des décisions du joueur (« jouer pour moi », suggestions de coup optimal) | Le bot d'autoplay existe déjà dans les outils de test | Change la nature du jeu, et la moindre suggestion fausse détruit la confiance | Réserver le bot aux tests ; côté joueur, se limiter à mettre en avant les actions légales |
| Chat, comptes, classements, multi en ligne | Réflexe « jeu numérique » | Hors périmètre déclaré du projet | Rien. Le multi local existant reste tel quel |
| Modales bloquantes empilées pour chaque demande | Solution la plus rapide à coder | Fait perdre le contexte du plateau, ce qui est exactement le défaut à corriger | Barre de demande à emplacement fixe, plateau toujours visible et lisible |

---

## Feature Dependencies

```
[Design System : tokens, typo, couleurs, icônes, espacement]
    ├──requires──> [Décision techno frontend]   (voir STACK.md)
    └──enables───> TOUT le reste

[Composant Carte à double représentation]
    ├──requires──> [Design System]
    ├──requires──> [Accès au texte de règles de cards.json, pas seulement au scan]
    └──enables───> [Plateau] [Galerie] [Deck builder] [Inspection] [Journal cliquable]

[Couche d'adaptation des descripteurs (state adapter)]
    ├──requires──> [Descripteurs existants to_descriptor.py]
    └──enables───> [Plateau] [Barre de demande] [Journal] [Animations informatives]

[Système de zones du plateau]
    ├──requires──> [Composant Carte] + [State adapter]
    ├──enables───> [Tuiles adaptatives] ──enables──> [Vue d'ensemble]
    └──enables───> [Navigation par zone mobile]

[Barre de demande (ask)]
    ├──requires──> [State adapter]
    └──enables───> [Surlignage des cibles valides]
                        └──requires──> [Cibles légales exposées par le descripteur]  ⚠ dépendance backend

[Flux d'événements exploitable]
    ├──enables───> [Journal de partie] ──enables──> [Journal cliquable] ──enables──> [Timeline de replay]
    └──enables───> [Animations informatives]

[Moteur de recherche / filtres]
    ├──requires──> [Index de cards.json côté client]
    └──enables───> [Galerie] [Deck builder] [Recherche dans les zones du plateau]

[Store d'état de setup]
    └──enables───> [Wizard] ──enables──> [Récapitulatif persistant] [Presets] [Validation en ligne]

[Réglage de vitesse d'animation] ──enhances──> [Animations informatives]
[Prévisualisation d'impact] ──requires──> [Données de prévision fournies par le moteur]  ⚠ dépendance backend
[Undo exposé dans l'UI] ──reduces──> [besoin de dialogues de confirmation]

[Éventail incliné en main] ──conflicts──> [Lisibilité tactile et petit écran]
[Plateau sombre art plein cadre] ──conflicts──> [Reconnaissance des zones]
[Pan/zoom libre] ──conflicts──> [Lecture en un coup d'œil]
```

### Dependency Notes

- **Tout dépend du design system.** Sans tokens partagés, la refonte reproduit le problème actuel : un vieux CSS partagé plus des surcouches successives (`style.css` + `wizard.css`).
- **Le composant Carte est le goulot d'étranglement.** Il est utilisé par toutes les surfaces. Le concevoir mal coûte trois refontes. Le concevoir bien rend la galerie et le deck builder presque gratuits.
- **Deux dépendances backend sont à valider tôt** : les cibles légales et les données de prévisualisation. Elles tombent dans le périmètre autorisé (« endpoints strictement nécessaires à l'UI »), mais si le descripteur ne les porte pas, il faut soit un ajout minimal côté rendu, soit renoncer à la feature. Ne jamais compenser par du calcul de règles côté client.
- **Le journal conditionne la timeline de replay.** Construire le journal d'abord donne la timeline à moindre coût ensuite.
- **La navigation par zone mobile dépend du système de zones**, pas de media queries ajoutées après coup. C'est une décision d'architecture de mise en page, à prendre au début.
- **Le surlignage des actions légales rend la barre de demande beaucoup plus lisible**, et réciproquement. Les livrer ensemble.

---

## MVP Definition

### Launch With (v1) : « le jeu est beau et lisible »

- [ ] Design system (tokens couleur/typo/espacement, icônes, composants de base) : prérequis de tout le reste
- [ ] Coquille de navigation + hub d'accueil avec action primaire et libellés texte : donne immédiatement l'impression d'une app moderne
- [ ] Composant Carte à double représentation (tuile lisible + scan à l'inspection) : cœur du problème de lisibilité
- [ ] Inspection au survol / appui long / clavier, non modale, sans occlusion : le geste le plus fréquent en partie
- [ ] Système de zones du plateau, délimitées et étiquetées : facteur numéro un de lisibilité
- [ ] Indicateur de phase/tour permanent + rappel de l'action attendue : répond à « où en est-on »
- [ ] Barre de demande (ask) à emplacement fixe, avec annuler/passer : point de contact principal avec le moteur
- [ ] Compteurs lisibles sur les cartes (dégâts, menace, épuisement, statuts) : évite l'inspection en boucle
- [ ] Wizard de préparation avec stepper, récapitulatif persistant et validation en ligne : la douleur explicitement citée
- [ ] Responsive PC / tablette / mobile avec navigation par zone sur petit écran : cible déclarée du projet
- [ ] Base d'accessibilité : jamais la couleur seule, contrastes vérifiés, `prefers-reduced-motion`
- [ ] Réglage de vitesse d'animation avec animations interruptibles : évite d'introduire le pire défaut du genre

### Add After Validation (v1.x)

- [ ] Refonte galerie + deck builder (recherche instantanée, facettes, vue liste/grille, stats de deck) : déclencheur = le plateau est stable et joué
- [ ] Journal de partie consultable : déclencheur = premiers retours « je n'ai pas compris ce qui s'est passé »
- [ ] Surlignage des cibles valides : déclencheur = confirmation que le descripteur porte l'information
- [ ] Undo exposé dans l'UI du plateau : déclencheur = flux de jeu validé
- [ ] Tooltips de mots-clés : déclencheur = table mot-clé → texte constituée
- [ ] Tuiles adaptatives et vue d'ensemble : déclencheur = observation de plateaux réellement surchargés
- [ ] Raccourcis clavier desktop : déclencheur = usage régulier sur PC
- [ ] Écran de fin de partie riche
- [ ] Presets de configuration

### Future Consideration (v2+)

- [ ] Prévisualisation d'impact chiffrée : reporter car dépend d'informations que le moteur n'expose peut-être pas ; à ne jamais bricoler côté client
- [ ] Timeline de replay navigable : reporter car dépend du journal et d'un flux d'événements propre
- [ ] Suivi de campagne visuel et log éditable : reporter car les 4 formats de campagne ont des logiques différentes, gros travail de modélisation
- [ ] Journal cliquable avec renvoi vers les cartes : reporter, extension du journal simple
- [ ] Recherche/filtres dans les zones du plateau : reporter, dépend du moteur de recherche de la galerie
- [ ] Installation PWA, sons et haptique : reporter, polish
- [ ] Deuxième thème visuel complet : reporter, mais garder le design system prêt à l'accueillir

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Design system (tokens + composants) | HIGH | MEDIUM | P1 |
| Composant Carte à double représentation | HIGH | HIGH | P1 |
| Système de zones délimitées et étiquetées | HIGH | HIGH | P1 |
| Barre de demande (ask) à emplacement fixe | HIGH | MEDIUM | P1 |
| Inspection non modale (survol / appui long) | HIGH | MEDIUM | P1 |
| Indicateur de phase/tour + action attendue | HIGH | LOW | P1 |
| Compteurs lisibles sur les cartes | HIGH | MEDIUM | P1 |
| Wizard de préparation + récapitulatif + validation | HIGH | MEDIUM | P1 |
| Responsive + navigation par zone mobile | HIGH | HIGH | P1 |
| Réglage/interruption des animations | MEDIUM | LOW | P1 |
| Base d'accessibilité (couleur, contraste, motion) | MEDIUM | LOW | P1 |
| Recherche instantanée + filtres à facettes | HIGH | MEDIUM | P2 |
| Statistiques de deck en direct | MEDIUM | MEDIUM | P2 |
| Journal de partie consultable | HIGH | MEDIUM | P2 |
| Surlignage des cibles valides | HIGH | MEDIUM | P2 |
| Undo exposé dans l'UI | MEDIUM | LOW | P2 |
| Tooltips de mots-clés | MEDIUM | MEDIUM | P2 |
| Tuiles adaptatives + vue d'ensemble | HIGH | HIGH | P2 |
| Solo multi-héros (aires repliables) | HIGH | HIGH | P2 |
| Raccourcis clavier / palette de commandes | LOW | MEDIUM | P3 |
| Écran de fin de partie riche | MEDIUM | MEDIUM | P3 |
| Presets de configuration | MEDIUM | LOW | P3 |
| Prévisualisation d'impact | HIGH | HIGH | P3 |
| Timeline de replay | MEDIUM | HIGH | P3 |
| Suivi de campagne visuel | MEDIUM | HIGH | P3 |
| PWA, sons, haptique | LOW | LOW | P3 |

---

## Competitor Feature Analysis

| Feature | Marvel Snap | MTG Arena | Legends of Runeterra | DragnCards / MarvelCDB / TTS | Our Approach |
|---------|-------------|-----------|----------------------|------------------------------|--------------|
| Représentation de carte sur le plateau | Carte native, art plein cadre, texte minimal | Scan quasi fidèle au carton, illisible quand le plateau se remplit | Gabarits par catégorie, minimalisme, art plein cadre | TTS et DragnCards : scan brut, zoom obligatoire | Tuile native lisible + scan complet à l'inspection |
| Inspection de carte | Appui pour agrandir | Survol, mais occlusion fréquente par la pile | Survol/appui fluide | DragnCards : icône « œil » pour parcourir les piles | Survol, appui long, raccourci clavier, sans occlusion |
| Délimitation des zones | 3 lieux, très peu de zones | Champ de bataille indifférencié, se sature | Rangées et bancs explicites | TTS : tapis image, aucune structure logicielle | Zones nommées, hiérarchie de luminosité, en-têtes |
| Indicateur de phase | Indicateur de tour jugé trop subtil | Barre de phases discrète | Jeton d'attaque très visible | DragnCards : Phase/Step Tracker de premier plan + texte d'aide | Bandeau de phase permanent avec action attendue |
| Ciblage | Simplifié à l'extrême (peu de ciblage) | Flèches et prompts, ergonomie critiquée | Ciblage clair, feedback fort | Aucun (résolution manuelle, non automatisée) | Cibles valides surlignées, geste appui-appui, drag optionnel |
| Journal / historique | Minimal | Journal peu accessible | Historique correct | DragnCards : journal permanent, central au produit | Journal permanent, puis cliquable |
| Deck builder | Simple, collection visuelle | Filtres complets, courbe en haut d'écran | Filtres soignés | MarvelCDB : recherche syntaxique puissante, gestion de collection, tri par nom/pack/classe/type/coût, 5 modes d'affichage | Facettes de MarvelCDB + stats en direct + vue liste dense |
| Mobile | Référence du genre, éléments interactifs en bas | Portage tardif, dense | Multiplateforme dès la conception, système visuel pensé pour l'échelle | MarvelCDB : pages retravaillées pour le mobile ; TTS : inutilisable | Navigation par zone, paysage privilégié, portée du pouce |
| Animation | Impactante, courte | Longue, parfois bloquante | Soignée | Aucune | Informative, courte, interruptible, réglable |
| Direction visuelle | « Piano glass » sombre + hologrammes de lumière + halftone en hommage aux comics | Fidélité au carton, chrome discret | Toile, or et verre, braises ; puis virage vers un UI plat plus simple | Utilitaire, aucun parti pris | Voir section suivante |
| Monétisation dans l'UI | Boutique en première position de la navigation | Boutique proéminente | Boutique proéminente | Aucune | Aucune (anti-feature assumée) |

---

## Directions Visuelles Proposées

Trois directions cohérentes et exclusives sur le **squelette**, avec dans chaque cas les couches qui peuvent être empruntées aux autres. Le point commun obligatoire : les cartes sont déjà des illustrations riches et bavardes. L'interface doit donc être le cadre, jamais un concurrent visuel. C'est la leçon la plus solide de la recherche, formulée par la direction artistique de Marvel Snap : les cartes ont la priorité dans la hiérarchie visuelle et l'UI est là pour les mettre en valeur.

### Direction A : « Comic Panel » (planche de comics, énergie KAPOW)

**Principe** : la mise en page est une planche de comics. Les zones sont des cases (panels) séparées par des gouttières blanches. Encrage épais, halftone Ben-Day discret en texture de fond, onomatopées et éclats de vitesse réservés au feedback d'action, palette de primaires saturés dérivée des aspects.

**Pour**
- Identité Marvel immédiate, aucune confusion avec un autre client. C'est la direction la plus « à soi ».
- **La métaphore des cases sert directement la fonction** : les gouttières résolvent gratuitement le problème numéro un identifié par la recherche, la délimitation des zones. C'est le seul des trois axes où l'esthétique fait le travail de l'ergonomie.
- Le halftone est un choix validé industriellement sur cette IP : Marvel Snap l'a retenu comme hommage aux origines comics de Marvel, avec la question « à quoi ressembleraient les comics du futur ».
- Peu coûteux à produire sans artiste : bordures, gouttières, trames et transformations se font en CSS. Pas de dépendance à des assets 3D ou à des textures achetées.
- Le feedback d'action (éclat sur les dégâts, lignes de vitesse sur l'attaque) devient informatif **et** joyeux, ce qui coche la case « animations qui informent ».

**Contre**
- Risque majeur de bruit visuel : chaque carte est déjà une illustration de comics. Empiler un décor de comics autour peut produire une bouillie.
- Le halftone à petite taille génère du moiré sur écran non-Retina et du scintillement au défilement. C'est un vrai piège technique.
- Les typographies « comics » sont hostiles au texte de règles dense. À proscrire pour le corps de texte.
- Les primaires saturés compliquent le respect des contrastes et l'accessibilité.
- Peut vieillir vite ou paraître bon marché si la main est lourde.

**Garde-fous si retenue** : langage comics limité au chrome et au feedback transitoire, jamais derrière du texte ; trame halftone à taille fixe en pixels et opacité très faible ; corps de texte en linéale neutre, le lettrage comics réservé aux titres et aux onomatopées ; gouttières claires comme structure porteuse.

### Direction B : « Dark premium art-forward »

**Principe** : surfaces quasi noires, panneaux de verre et de lumière, accents dorés ou couleur d'identité du héros, art en pleine largeur, ambiance cinématographique.

**Pour**
- Fait chanter les scans de cartes, qui deviennent la seule source de couleur.
- C'est le standard de fait du genre en 2025-2026 : « piano glass » sombre et boutons-hologrammes chez Marvel Snap, système toile/or et verre/braises chez Legends of Runeterra. Le joueur reconnaît le registre « jeu de cartes premium ».
- Cohérent avec le principe « les cartes d'abord » : l'UI disparaît.
- Confortable en session du soir, flatteur sur écran OLED.
- Chemin le plus court vers un rendu « cher ».

**Contre**
- **Le risque documenté est exactement celui du projet.** Gwent Homecoming a poussé le plateau sombre et l'art omniprésent, et les joueurs ont décrit une lisibilité dégradée avec une sensation de « grande forêt ». Un LCG coop a beaucoup plus de zones que Gwent : le risque est supérieur, pas inférieur.
- Vingt zones sombres se ressemblent toutes. La reconnaissance de zone, qui est le besoin numéro un, devient le point faible.
- Le contraste entre un chrome très sombre et des scans clairs fatigue à la longue.
- Mauvais en usage tablette de jour, alors que la tablette est une cible déclarée.
- Risque de paraître « un jeu de cartes sombre de plus ».

**Garde-fous si retenue** : différencier les zones par paliers de luminosité et par en-têtes étiquetés, pas par des ornements ; tokens de contraste stricts et vérifiés sur les compteurs ; prévoir un thème clair pour le jour et le mobile dès le premier jour, ce qui revient de fait à construire aussi la direction C.

### Direction C : « Instrument de jeu » (clair, moderne, typographique)

**Principe** : surfaces claires ou neutres, hiérarchie typographique forte, panneaux plats, couleurs d'aspect utilisées comme signal fonctionnel et non comme décor, espacement généreux. L'interface se comporte comme un bon outil, et les cartes fournissent tout le spectacle.

**Pour**
- **Meilleur rapport lisibilité/effort** pour un plateau coop à nombreuses zones, ce qui est précisément le problème le plus dur du projet.
- Legends of Runeterra a elle-même fait évoluer son client vers une approche plus plate et plus simple, en visant la clarté et le passage à l'échelle multiplateforme sur une UI très dense en information. Le mouvement historique du genre va dans ce sens.
- Contraste maximal entre l'UI sobre et les scans riches : les cartes ressortent sans effort.
- Le meilleur sur mobile et en usage diurne sur tablette.
- Le moins cher à construire et à maintenir, le plus facile à rendre accessible, celui qui vieillit le mieux.

**Contre**
- Le moins spectaculaire au premier coup d'œil. Risque de ressembler à MarvelCDB ou à un tableur plutôt qu'à un jeu, alors que l'utilisateur veut « une interface digne du contenu ».
- Aucune récompense émotionnelle intrinsèque : la victoire ne se ressent pas si rien n'est ajouté.
- Exige une vraie maîtrise de la typographie et de l'espacement pour ne pas paraître générique. Le « clean » raté est plus punitif que le « sombre » raté.

**Garde-fous si retenue** : investir l'énergie dans le mouvement et les moments (impact, victoire, révélation d'encounter) plutôt que dans les surfaces ; utiliser la couleur d'identité du héros comme accent de son aire de jeu ; soigner les micro-détails d'ombre et de rayon pour éviter l'effet maquette.

### Recommandation

**Squelette C, personnalité A, thème B en option.** Concrètement : structure et lisibilité de l'« instrument de jeu », énergie comics dans le feedback transitoire et les moments forts, thème sombre proposé en préférence utilisateur plutôt qu'en direction fondatrice.

Raisons :
1. La douleur exprimée est la lisibilité autant que le look. C se paie en clarté, A et B se paient en clarté.
2. La seule direction dont l'esthétique **aide** l'ergonomie est A, mais uniquement par sa structure en cases et ses gouttières claires, qui sont compatibles avec C. On peut prendre le bénéfice sans prendre le bruit.
3. B a un échec documenté sur exactement ce risque (Gwent), sur un jeu qui a moins de zones que Marvel Champions.
4. Un design system correctement tokenisé rend ce choix réversible. Décider « C avec accents A » n'interdit pas de livrer un thème B plus tard, à condition que la structure ne dépende jamais de l'obscurité pour exister.

**Décision à prendre tôt malgré tout** : le sens des tokens de surface (clair par défaut ou sombre par défaut) conditionne la manière d'écrire les composants. À trancher dans la première phase, pas plus tard.

---

## Confidence & Gaps

**HIGH confidence**
- Le problème central est la densité d'information et la lisibilité du texte à petite taille, et les trois écoles de représentation de carte (Hearthstone / LoR / MTG Arena) sont un cadre d'analyse solide.
- Direction artistique de Marvel Snap (hiérarchie au service des cartes, piano glass, hologrammes, halftone, éléments interactifs en bas de l'écran) : décrite par la designer elle-même.
- Système visuel de Legends of Runeterra (matières hiérarchisées, anatomie de carte réutilisable, virage vers un UI plat, contrainte multiplateforme) : décrit par un designer de l'équipe.
- Aucun client officiel Marvel Champions numérique identifié. Twin Sails Interactive, ex-Asmodee Digital, est devenu indépendant en avril 2025 et aucune annonce Marvel Champions n'a été trouvée.

**MEDIUM confidence**
- Critiques d'ergonomie de LotR Adventure Card Game (survol impossible, tri de cartes en deckbuilding, texte difficile à lire, menu principal désorientant) : plusieurs recensions convergentes, sources secondaires.
- Défauts d'ergonomie de Marvel Snap (icônes de navigation non libellées, timer invisible, placement des boutons Fin de tour/Abandon, indicateur de tour trop subtil) : étude de cas UX indépendante, non confirmée par l'éditeur.
- Occlusion de la pile dans MTG Arena : retours utilisateurs sur le portail officiel de feedback, donc réels mais non arbitrés.
- Fonctionnement de DragnCards (Phase/Step Tracker, journal permanent, hotkeys via TAB, parcours des piles, automatisations non appliquées) : documentation communautaire d'un plugin d'un autre jeu, à confirmer sur le plugin Marvel Champions.

**LOW confidence / à valider**
- Échec de lisibilité de Gwent Homecoming : plaintes de forum, pas de post-mortem officiel. Le signal reste utile comme mise en garde, il ne constitue pas une preuve.
- Détail exact des options d'accessibilité natives de Hearthstone et Legends of Runeterra : non confirmé. Hearthstone semble surtout servi par un mod communautaire, ce qui suggère une accessibilité native faible.

**Gaps assumés**
- **Aucune référence solide trouvée sur la présentation d'un plateau coopératif à 4 aires de joueur sur téléphone.** C'est un problème apparemment non résolu par l'industrie. La navigation par zone est une proposition raisonnée, pas un pattern validé. À prototyper tôt et à tester en vrai.
- La talk GDC 2023 de Second Dinner et l'analyse ArtStation d'Andrew Hutcheson sur l'UI de Marvel Snap n'ont pas pu être consultées directement (vidéo, et 403 sur ArtStation). Le contenu retenu vient de sources secondaires concordantes.
- La syntaxe de recherche complète de MarvelCDB n'a pas pu être extraite champ par champ. Les axes de tri et modes d'affichage sont confirmés, la grammaire de requête exacte reste à relever sur le site.
- Ce que le descripteur du moteur expose réellement (cibles légales, prévisualisation) n'a pas été vérifié dans le code lors de cette recherche. C'est le point de blocage potentiel de deux features à forte valeur, à instruire en priorité.

---

## Sources

**Direction artistique et systèmes visuels (HIGH)**
- [Marvel Snap, portfolio de la designer UI (Tiffany Smart)](https://www.tiffanysmart.com/work/marvel-snap) : hiérarchie au service des cartes, piano glass, hologrammes, halftone, ergonomie du pouce
- [Legends of Runeterra, étude de cas UX/UI (Ryan O'Donoghue)](https://www.ryanodon.com/case-studies/legends-of-runeterra) : matières hiérarchisées, anatomie de carte réutilisable, tokens vers Unity, contrainte multiplateforme
- [Legends of Runeterra UX/UI (ArtStation, Rufio Jones)](https://www.artstation.com/artwork/XnmR6w) : évolution du client, virage UI plat

**Analyse d'UI de jeux de cartes (MEDIUM-HIGH)**
- [The Card Games UI Design of Fairtravel Battle, GDKeys](https://gdkeys.com/the-card-games-ui-design-of-fairtravel-battle/) : densité d'information, échec du zoom/panoramique, coins joueur, délimitation des zones, trois écoles de carte (Hearthstone / LoR / MTG Arena)
- [Marvel Snap, étude de cas UI/UX (Design Bootcamp)](https://medium.com/design-bootcamp/marvels-snap-ui-ux-case-study-9f727d8f3875) : icônes non libellées, accueil surchargé, timer invisible, placement des boutons, indicateur de tour
- [Marvel Snap, wireframe de gameplay (Carol Michelon)](https://medium.com/@hello_54095/marvel-snap-gameplay-wireframe-ed76251eebc5)
- [Flash Thoughts: Slay the Spire's UI, Cloudfall Studios](https://www.cloudfallstudios.com/blog/2018/2/20/flash-thoughts-slay-the-spires-ui) : traînées de cartes informatives, zone de lancement, jouer plus vite que les animations
- [SNAPPY U.I., Andrew Hutcheson (ArtStation, inaccessible 403)](https://www.artstation.com/artwork/GemNDd)

**Critiques et échecs documentés (MEDIUM à LOW)**
- [LotR Adventure Card Game, recension Nintendo Life](https://www.nintendolife.com/reviews/switch-eshop/lord_of_the_rings_adventure_card_game) : survol impossible, tri de cartes en deckbuilding
- [LotR Adventure Card Game, recension Board Game Quest](https://www.boardgamequest.com/the-lord-of-the-rings-adventure-card-game-digital-review/) : UI inconsistante, texte difficile à lire
- [LotR Adventure Card Game, recension TheGamer](https://www.thegamer.com/the-lord-of-the-rings-adventure-card-game-review-you-shall-pass/) : menu principal désorientant
- [MTG Arena, feedback officiel : la pile masque les cartes en dessous](https://feedback.wizards.com/forums/918667-mtg-arena-bugs-product-suggestions/suggestions/40528594-stack-cards-blocking-view-of-cards-beneath-them-on)
- [Gwent Homecoming, retours de forum CD Projekt Red](https://forums.cdprojektred.com/index.php?threads/not-only-good-changes-in-gwent-homecoming.10987511/) : lisibilité du plateau, « grande forêt » (LOW)
- [Hearthstone, plainte historique sur la durée des animations (HearthPwn)](https://www.hearthpwn.com/forums/hearthstone-general/general-discussion/253808-animation-time-speed-it-up-a-lot)

**Outils communautaires LCG (MEDIUM)**
- [MarvelCDB](https://marvelcdb.com/) et [page À propos](https://marvelcdb.com/about) : positionnement « fast, powerful and exhaustive », gestion de collection, filtrage
- [MarvelCDB, recherche de cartes](https://marvelcdb.com/search) : axes de tri (nom, pack, classe, type, coût) et modes d'affichage
- [The Champion's Guide to MarvelCDB](https://alteregochronicle.wixsite.com/alter-ego-chronicle/post/the-champion-s-guide-to-marvelcdb) : syntaxe de filtrage, usages réels
- [DragnCards](https://dragncards.com/) et [tutoriel DragnCards (WARS TCG)](https://warstcg.org/dragncards-tutorial/) : Phase/Step Tracker, journal, hotkeys TAB, parcours des piles, automatisations non appliquées
- [Fil BGG : DragnCards pour LotR LCG](https://boardgamegeek.com/thread/2692585/dragncards-a-new-online-site-to-play-lotr-lcg)
- [Marvel Champions: Digital Edition sur itch.io](https://irefrixs.itch.io/marvel-lcg) : le client amont du projet, serveur web local, dépendance au sélecteur CSS `:has()`
- [Marvel Champions Digital (kitze.io)](https://www.kitze.io/projects/marvel-champions-digital) : projet concurrent, approche tablette d'abord et interactions tactiles

**Absence de client officiel (MEDIUM, claim négatif)**
- [Twin Sails Interactive devient indépendant d'Asmodee (avril 2025)](https://twin-sails.com/en/twin-sails-interactive-moves-forward-as-an-independent-entity-from-asmodee/) : aucune mention de Marvel Champions dans les annonces trouvées
- [Fil BGG : application iOS/Android Marvel Champions](https://boardgamegeek.com/thread/3296681/ios-and-android-marvel-champions-app) : demandes de la communauté, pas d'annonce officielle

**Références de style et outillage de design**
- [Game UI Database (Edd Coates)](https://www.gameuidatabase.com/) : 55 000+ captures, 1 300+ jeux, recherche par type d'écran, patterns, éléments de HUD, filtres daltonisme intégrés. Outil recommandé pour instruire la direction visuelle
- [Interface In Game](https://interfaceingame.com/) : captures et vidéos d'UI, dont [Legends of Runeterra Mobile](https://interfaceingame.com/games/legends-of-runeterra-mobile/) et [Slay the Spire](https://interfaceingame.com/games/slay-the-spire/)
- [Retro Comic Book Art: Using Ben Day Dots in Web Design](https://www.elegantthemes.com/blog/design/retro-comic-book-art-using-ben-day-dots-in-web-design) : histoire et mise en œuvre du halftone Ben-Day
- [Legends of Runeterra, rapport d'accessibilité (Family Gaming Database)](https://www.familygamingdatabase.com/accessibility/Legends+of+Runeterra)
- [Hearthstone Access](https://hearthstoneaccess.github.io/) : mod d'accessibilité communautaire, signal d'une accessibilité native faible

**Contexte interne**
- `.planning/PROJECT.md` : périmètre, contraintes, douleur exprimée
- `.planning/codebase/CONCERNS.md` : `scene.html` monolithique 2251 lignes, hacks CSS du wizard, formulaires de campaign log sans guidage
- `.planning/codebase/ARCHITECTURE.md` : rendu piloté par descripteurs JSON, une requête HTTP par action de jeu
- `Fusion/PREPARE-UI-PLAN.md` : plan de wizard en 6 étapes déjà défini

---
*Feature research for: UI/UX de client de jeu de cartes numérique coopératif (Marvel Champions LCG)*
*Researched: 2026-07-28*

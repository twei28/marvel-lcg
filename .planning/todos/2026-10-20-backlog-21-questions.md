# Backlog 21 (mode navigateur « Play ») : questions restantes après l'essai multi-navigateurs du 20/10/2026

**Statut : EN ATTENTE DE DÉCISION.** Essai joué avec Playwright sur la construction locale (`navigateur/construire.py`, serveur `navigateur/serveur-local.py`), parcours `navigateur/essais/navigateurs.mjs` : page, moteur, assistant solo (Spider-Man contre Rhino), mulligan, un tour, phase du méchant, retour au round 2. Rien publié, rien déployé.

## Ce qui a été corrigé en route (petit, clair)
- `serveur-local.py` ne servait pas les sons (`/survol.wav`, `/voix-*.mp3` : 404 en rafale). Le Caddyfile de production les sert : seul le serveur d'essai manquait. Corrigé.
- `construire.py` : le plateau enregistre `/sw-plateau.js` à la racine, absent de `dist` (404 « bad HTTP response code » en console, constaté en émulation mobile). Le service worker minimal (ne garde rien en cache) est maintenant copié à la racine.
- `navigateur.html` : trois phrases FR au tutoiement (avertissement téléphone, message de nouvelle version, navigateur incompatible) reformulées sans tutoiement.

## Questions

### Q1. WebKit (Safari) : le processus de rendu plante quand on ouvre la fiche du héros dans l'assistant
Constat : avec le WebKit de Playwright (build WPE, Linux, 26.5), la page se charge, le moteur démarre et l'accueil s'affiche, puis le processus web se termine (`SIGABRT`, « Target crashed ») dès qu'on choisit un héros dans l'assistant (ouverture de la fenêtre du deck). Reproductible à chaque essai. Les pages d'accueil, `cards.html`, `credits.html` restent 40 s sans plantage. La cause n'est pas isolée (moteur Python/mémoire, rendu 3D de la fiche, ou défaut propre au build WPE de test). La machine d'essai était de plus très chargée (charge 50 à 77 sur 8 cœurs, swap plein), ce qui ne permet pas d'exclure la mémoire.
Recommandation : ne pas annoncer Safari/iOS comme pris en charge. Faire un essai sur un vrai Safari (Mac ou iPhone) avant toute ouverture publique ; en attendant, garder l'avertissement « expérimental » et le bouton vers les tables du serveur pour les appareils Apple.
Question : disposez-vous d'un Mac ou d'un iPhone pour un essai réel, ou Safari est-il hors périmètre pour Play ?

### Q2. Firefox : démarrage nettement plus lent que Chromium
Constat (machine chargée, valeurs indicatives) : moteur prêt en 40 à 120 s sous Firefox contre 8 à 15 s sous Chromium et WebKit ; Firefox émet aussi un avertissement console répété (« WebAssembly exception handling 'try' instruction is deprecated », Pyodide 0.27.8). Le parcours complet aboutit (round 2) sans erreur.
Recommandation : mesurer sur une machine au repos avant de conclure ; si l'écart persiste, passer à une version de Pyodide récente (exceptions WebAssembly modernes) lors de la prochaine reconstruction du moteur, avec relance du contrôle d'équivalence. Une barre de progression par étape (déjà présente) suffit en attendant.
Question : accepter ce temps de démarrage sous Firefox, ou lancer la montée de version de Pyodide ?

### Q3. Mobile (390×844)
Constat : la page se charge, l'avertissement « expérimental » s'affiche, l'accueil mobile (bouton JOUER), l'assistant mobile (fiche héros, CHOISIR) et le plateau fonctionnent sous Chromium émulé ; le parcours jusqu'au round 2 aboutit. Ce que l'émulation ne dit pas : mémoire réelle (le moteur demande environ 300 Mo), chaleur, fermeture de l'onglet par le système, saisie tactile fine (le plateau mobile est lui-même en « mis de côté », item 24 et 25 du rapport d'état).
Recommandation : essai sur un vrai téléphone Android puis iPhone avant d'ouvrir ; garder l'avertissement.
Question : un téléphone de test est-il disponible ?

### Q4. Ouverture publique (DÉCISION, non traitée ici)
`play.narwhalchampions.com` est joignable mais sans lien depuis le site. Rendre l'adresse accessible depuis le site (lien, bouton, mention) est une décision de produit. Non touché.
Recommandation : attendre les réponses Q1 à Q3 (au moins Safari et téléphone), puis ouvrir d'abord avec la mention « bêta » sur la page.

### Q5. Brancher `publier.py` sur `deployer.ps1` (DÉPLOIEMENT, non traité ici)
Aujourd'hui `navigateur/publier.py --oui` et `deployer.ps1 -Code` sont deux commandes distinctes ; les deux déploiements ne sont pas liés. Non touché (aucun déploiement dans ce lot).
Recommandation : garder deux commandes tant que Play n'est pas ouvert au public ; les chaîner seulement après la décision Q4, pour qu'un redéploiement du jeu ne laisse pas Play sur un plateau périmé (le plateau construit est partagé).

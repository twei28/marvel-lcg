# Phase 1 : Filet de sécurité et boucle de dev - Context

**Gathered:** 2026-07-28
**Status:** Ready for planning

<domain>
## Phase Boundary

Outillage de non-régression, posé AVANT toute refonte visuelle :
1. Une commande unique capture les écrans actuels (5 écrans × 3 gabarits PC/tablette/mobile) et signale toute différence visuelle à la relance.
2. 20 à 40 fixtures `get_world` issues de l'autoplay, rejouables hors partie (afficher un état de plateau sans lancer une vraie partie).
3. Bascule `?ui=old` : sur toute page en cours de migration, retour à l'ancienne version, jeu jouable de bout en bout.
4. Test automatisé : une partie se lance depuis l'écran de préparation actuel et atteint le plateau (contrat `/new?data=` gelé).

Contrainte transverse à acter dans PROJECT.md : l'intouchabilité du moteur s'étend au runtime `public/js/marvel/` (7318 lignes de TS compilé, sources perdues). Le nouveau code est une fonction pure de `get_world`, écrit à côté.

</domain>

<decisions>
## Implementation Decisions

### Validation des changements visuels voulus
- **L'utilisateur valide sur photos** : à chaque changement d'apparence intentionnel, Claude présente les images avant/après et l'utilisateur approuve ou refuse AVANT de figer la nouvelle référence.
- Le workflow de mise à jour des captures de référence doit donc inclure une étape d'approbation utilisateur explicite (pas de mise à jour silencieuse des baselines).

### Présentation des comparaisons avant/après
- **Page de comparaison dans le navigateur** : images côte à côte (avant / après), écran par écran. C'est le format de validation préféré de l'utilisateur.
- L'outil de capture doit donc produire (ou permettre de produire) une page HTML de comparaison consultable localement.

### Bascule `?ui=old`
- Modalités laissées à la discrétion de Claude (lien visible vs paramètre d'URL, mémorisation, portée). L'utilisateur a répondu « tu décides ».
- Critère directeur : le plus sûr et le plus simple pour un utilisateur non technique ; montrer le résultat une fois en place.

### Claude's Discretion
L'utilisateur n'est pas à l'aise avec les sujets techniques et délègue explicitement tout le reste, notamment :
- Choix de l'outil de capture/diff visuel, seuils de tolérance, gestion des faux positifs.
- Sélection des 20-40 fixtures `get_world` (moments de partie couverts : début, mi-partie, asks, multi-héros, side schemes…), nommage, procédure de régénération.
- Mécanique exacte de la bascule `?ui=old` (voir ci-dessus).
- Forme des rapports de test automatisés (console, verbosité, granularité).
- Déclenchement de la boucle de vérification (manuel vs avant chaque livraison).

</decisions>

<specifics>
## Specific Ideas

L'utilisateur se décrit comme « pas doué en IT » : toute interaction qui lui est destinée (validation avant/après, bouton de retour à l'ancienne UI, messages d'erreur des outils) doit être compréhensible sans vocabulaire technique. Les échanges avec lui se font en français, courts et concrets.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 01-filet-de-securite*
*Context gathered: 2026-07-28*

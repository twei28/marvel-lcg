// legacy.js — les RÈGLES du mode Legacy, et rien d'autre.
//
// On commence avec la seule boîte de base et ses cinq héros ; on ouvre la suite
// en jouant. Spec complète : `.planning/todos/2026-09-13-mode-legacy.md`.
//
// ⚠ AUCUNE ENTRÉE-SORTIE ICI. Ce fichier ne lit ni le réseau, ni le stockage,
// ni le catalogue : on lui passe tout, il répond. C'est ce qui le rend
// testable sans monter une partie, et c'est là que vivent les seules décisions
// qui comptent. Le branchement (catalogue, historique, fiche du compte) est
// ailleurs.
//
// Les mots :
//   palier      une vague, avec ses scénarios et ses héros. Douze en tout, du
//               Set de base (vague 0) à Fear No Evil (vague 11).
//   fiche       ce que le mode retient d'un compte, et qui ne se déduit pas de
//               l'historique : la date de départ et les jetons dépensés.
//   jeton       une monnaie. Une première victoire avec un héros OFFICIEL en
//               donne un ; s'achète un héros fan-made.
"use strict";

/** Le Set de base, toujours ouvert : c'est le point de départ, pas une marche. */
export const VAGUE_DEPART = 0;

/** Compare deux noms de scénario sans se laisser arrêter par la casse, les
 *  espaces ou les accents.
 *
 *  ⚠ L'HISTORIQUE NE GARDE QUE LE NOM AFFICHÉ d'un scénario (« Rhino »), pas
 *  son identifiant de fichier. C'est donc par le nom qu'on recolle les deux,
 *  et un nom se compare mal tel quel. */
export function cleNom(nom) {
    return String(nom || "")
        .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
        .toLowerCase().replace(/\s+/g, " ").trim();
}

/** Ce que les parties gagnées ont apporté.
 *
 *  `depuis` (instant UNIX) fait table rase de tout ce qui précède : c'est le
 *  chemin « repartir de zéro », choisi une fois à l'activation du mode.
 *
 *  ⚠ UNE VICTOIRE À PLUSIEURS COCHE TOUS LES HÉROS DE LA TABLE, et le vilain.
 *  Fidèle au jeu de plateau, où l'équipe gagne ensemble, et ça récompense de
 *  jouer à plusieurs.
 */
export function victoires(historique, depuis = 0) {
    const scenarios = new Set();
    const heros = new Set();
    // Le héros dont la PREMIÈRE victoire était en expert. Sert aux jetons.
    const premiereEnExpert = new Set();
    for (const partie of historique || []) {
        if (!partie || !partie.won) continue;
        if (depuis && Number(partie.time || 0) < depuis) continue;
        const cle = cleNom(partie.scenario);
        if (cle) scenarios.add(cle);
        for (const h of partie.heroes || []) {
            const id = String(h && h.card_id || "");
            if (!id) continue;
            // ⚠ ON NE REGARDE L'EXPERT QUE SUR LA PREMIÈRE VICTOIRE DE CE
            // HÉROS. Le jeton se gagne une fois ; son bonus se décide au même
            // moment, sans quoi il suffirait de rejouer un héros déjà validé
            // en expert pour battre monnaie sans fin.
            if (!heros.has(id)) {
                heros.add(id);
                if (partie.expert) premiereEnExpert.add(id);
            }
        }
    }
    return { scenarios, heros, premiereEnExpert };
}

/** Les jetons gagnés, dépensés et restants.
 *
 *  Un jeton par héros OFFICIEL dont on a gagné une partie, et un de plus si
 *  cette première victoire était en expert. Les héros fan-made n'en donnent
 *  pas : ce sont eux qu'on achète.
 */
export function jetons(gagnees, herosOfficiels, depenses = []) {
    const officiels = new Set(herosOfficiels || []);
    let total = 0;
    for (const id of gagnees.heros) {
        if (!officiels.has(id)) continue;
        total += 1;
        if (gagnees.premiereEnExpert.has(id)) total += 1;
    }
    const depenseUniques = new Set(depenses || []);
    return { gagnes: total, depenses: depenseUniques.size,
             restants: Math.max(0, total - depenseUniques.size) };
}

/** Un palier est franchi quand TOUS ses vilains sont battus. Les héros n'y
 *  font rien : ils rapportent les jetons.
 *
 *  ⚠ RÈGLE CHANGÉE LE 16/09/2026, ET VOICI POURQUOI. Il fallait auparavant
 *  avoir gagné avec tous les héros de la vague EN PLUS d'avoir battu tous ses
 *  vilains. Un joueur avait descendu les trois vilains du Set de base sans
 *  rien voir s'ouvrir : il lui manquait deux héros sur cinq, et il a cru à un
 *  défaut. Décision : « il faut simplement battre tous les méchants pour
 *  débloquer la prochaine vague ». Les héros restent payés en jetons
 *  (`jetons`), donc varier son équipe garde un intérêt, sans être exigé.
 *
 *  ⚠ LA MARCHE EST PROPORTIONNELLE À LA BOÎTE, jamais au catalogue entier :
 *  on ne demande que les scénarios DE CETTE VAGUE.
 *
 *  ⚠ UNE LISTE VIDE NE BLOQUE RIEN, et cela vaut désormais dans les deux
 *  sens : une vague sans vilain (Fear No Evil, deux héros et aucun scénario)
 *  s'ouvre et se franchit d'un coup. C'est la règle appliquée sans exception,
 *  pas un oubli.
 *
 *  ⚠ `herosRestants` EST TOUJOURS RENDU, et il sert encore : l'écran s'en
 *  sert pour dire combien de jetons attendent dans cette boîte. Ce qu'il ne
 *  fait plus, c'est fermer la route.
 */
export function palierFranchi(palier, gagnees) {
    const vilainsRestants = (palier.scenarios || [])
        .filter((s) => !gagnees.scenarios.has(cleNom(s.nom)));
    const herosRestants = (palier.heros || [])
        .filter((h) => !gagnees.heros.has(h.id));
    return { franchi: vilainsRestants.length === 0,
             vilainsRestants, herosRestants };
}

/** L'état complet du parcours.
 *
 *  Les paliers s'ouvrent DANS L'ORDRE : le premier non franchi arrête la
 *  progression, même si le suivant l'est par accident (quelqu'un qui avait
 *  déjà joué la boîte 7 avant d'activer le mode). Sans cette barrière, le mode
 *  n'aurait plus de parcours du tout.
 */
export function parcours(paliers, historique, fiche = {}) {
    const gagnees = victoires(historique, Number(fiche.depuis || 0));
    const officiels = [];
    for (const palier of paliers || []) {
        for (const h of palier.heros || []) officiels.push(h.id);
    }
    const etapes = [];
    let ouvert = true;                 // le Set de base l'est toujours
    let vagueOuverte = VAGUE_DEPART;
    for (const palier of paliers || []) {
        const bilan = palierFranchi(palier, gagnees);
        etapes.push({ vague: palier.vague, nom: palier.nom, ouvert,
                      franchi: ouvert && bilan.franchi,
                      vilainsRestants: bilan.vilainsRestants,
                      herosRestants: bilan.herosRestants });
        if (ouvert && bilan.franchi) {
            vagueOuverte = palier.vague;
        } else {
            ouvert = false;            // tout ce qui suit reste ferme
        }
    }
    // La vague ouverte est celle qui SUIT le dernier palier franchi.
    const derniereOuverte = etapes.filter((e) => e.ouvert).pop();
    return {
        etapes,
        vagueOuverte: derniereOuverte ? derniereOuverte.vague : VAGUE_DEPART,
        jetons: jetons(gagnees, officiels, fiche.jetonsDepenses),
        gagnees,
    };
}

/** Ce qu'il reste à faire pour ouvrir la suite, en une phrase.
 *
 *  ⚠ ON NOMME CE QUI MANQUE, ON NE COMPTE PAS. « Gagne avec Thor » se lit et
 *  s'exécute ; « il reste 3 héros » oblige à chercher lesquels. Au-delà de
 *  trois noms, on bascule sur le compte, faute de place.
 */
export function condition(etape, t = (x) => x) {
    if (!etape || etape.franchi) return "";
    const noms = (liste, champ) => liste.map((x) => x[champ] || x.id).filter(Boolean);
    // ⚠ LES HÉROS NE SONT PLUS CITÉS ICI (16/09/2026). Ils ne ferment plus
    // rien : les nommer dans la condition ferait croire à une exigence. Ce
    // qu'ils rapportent se dit ailleurs, sur sa propre ligne (`aJetons`).
    const vilains = noms(etape.vilainsRestants || [], "nom");
    if (!vilains.length) return "";
    return vilains.length <= 3
        ? `${t("bats")} ${vilains.join(", ")}`
        : `${t("bats")} ${vilains.length} ${t("méchants")}`;
}

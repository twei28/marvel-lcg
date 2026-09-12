// variantes.js — les VARIANTES d'un héros, réunies en un seul endroit.
//
// Idée de l'utilisateur du 11/09/2026 : une seule tuile par héros dans le
// roster, et au clic une modale qui propose ce que CE héros a de particulier :
//   - une autre VERSION du deck de héros (Hellcat avec Iron Man ou Miss Hulk
//     en allié signature ; Superior Spider-Man avec Peter Parker ou Elliot
//     Tolliver en alter ego, chacun avec son obligation) ;
//   - une autre IDENTITÉ dans le même deck (The Thing Avenger / Guardian :
//     `metadata.hero_alts`, mécanisme existant) ;
//   - un ART alternatif de la carte de héros (purement visuel) ;
//   - la collection d'ARTS des ressources doubles.
//
// COMMENT UNE VERSION EST DÉCLARÉE. Une version est un deck de départ à part
// entière (`deck/starter/<id>.json`), ce que le moteur, le harnais et la gate
// de montage savent déjà consommer tel quel. Le fichier porte
// `metadata.variante_de: "<id du deck de base>"` et un libellé
// `metadata.variante_nom` ; le deck de base porte lui aussi son
// `variante_nom` pour nommer sa propre version. Le catalogue REPLIE les
// versions sous leur base (`regrouperVariantes`) : une tuile, pas deux.
//
// Ce module est PUR (aucun accès au DOM, aucun import) pour être testé par
// `node --test tools/tests-lanceur/variantes.test.mjs`.
"use strict";

/** Libellé par défaut d'une version qui n'en déclare pas. */
export const VERSION_DE_BASE = "Version de base";

/**
 * Replie les decks « variante de X » sous le héros X.
 *
 * `heroes` : la liste du catalogue, un élément par deck de départ, chacun avec
 * `id` (nom du fichier) et `deck` (son JSON). Renvoie une NOUVELLE liste sans
 * les variantes, où chaque base porte `versions` : la base d'abord, puis ses
 * variantes dans l'ordre du catalogue. Une variante dont la base est absente
 * (retirée, `indisponible`) garde sa tuile : mieux vaut un héros de trop qu'un
 * héros disparu.
 */
export function regrouperVariantes(heroes) {
    const parId = new Map();
    for (const h of heroes) parId.set(h.id, h);
    const repliees = new Set();
    for (const h of heroes) {
        const base = baseDe(h, parId);
        if (!base) continue;
        if (!base.versions) base.versions = [versionDe(base)];
        base.versions.push(versionDe(h));
        repliees.add(h.id);
    }
    return heroes.filter((h) => !repliees.has(h.id));
}

function baseDe(h, parId) {
    const cible = h.deck && h.deck.metadata && h.deck.metadata.variante_de;
    if (!cible || cible === h.id) return null;
    return parId.get(String(cible)) || null;
}

function versionDe(h) {
    const meta = (h.deck && h.deck.metadata) || {};
    return { id: h.id, nom: meta.variante_nom || VERSION_DE_BASE, deck: h.deck };
}

/** Les versions d'un héros : au moins la sienne. */
export function versionsDe(hero) {
    if (hero && hero.versions && hero.versions.length) return hero.versions;
    return hero ? [versionDe(hero)] : [];
}

/** Le deck de la version demandée, ou le deck de base si elle n'existe pas
 *  (mémoire périmée : une version supprimée ne doit jamais casser le clic). */
export function deckDeLaVersion(hero, versionId) {
    const v = versionsDe(hero).find((x) => x.id === versionId);
    return v ? v.deck : (hero && hero.deck) || null;
}

/**
 * Ce héros a-t-il quelque chose à proposer ? Sinon la modale ne s'ouvre pas
 * (décision utilisateur : jamais de modale vide).
 *
 * `contexte` : `arts` (liste des arts alternatifs de la carte de héros).
 * Les ressources n'en font plus partie : leur art alternatif se choisit à
 * l'étape des decks (décision utilisateur du 12/09/2026).
 */
export function optionsDuHeros(hero, contexte) {
    const ctx = contexte || {};
    const versions = versionsDe(hero);
    const identites = (hero && hero.variants) || [];
    const arts = ctx.arts || [];
    const options = {
        versions: versions.length > 1 ? versions : [],
        identites: identites.length > 1 ? identites : [],
        arts: arts.length ? arts : [],
        ressources: false,
    };
    // Les ressources ne sont PLUS une option du heros (12/09/2026) : leur art
    // se choisit a l'etape des decks, bouton « Ressources : art alternatif ».
    const autreChose = options.versions.length > 0 || options.identites.length > 0 || options.arts.length > 0;
    options.aucune = !autreChose;
    return options;
}

/** Clé d'une identité alternative : le couple de faces, pas la seule face
 *  héros (Superior Spider-Man garde su001a et change d'alter ego). */
export function cleIdentite(identite) {
    if (!identite) return "";
    const hero = identite.hero && identite.hero[0];
    return hero ? String(hero) : String(identite.heroCardId || "");
}

/**
 * La carte qui ILLUSTRE une version du deck de héros : celle que cette
 * version a et que les autres n'ont pas (l'allié signature de Hellcat,
 * l'alter ego de Superior Spider-Man). À défaut, la carte de héros.
 *
 * ⚠ Comparée à TOUTES les autres versions, pas seulement au deck de base :
 * la version de base n'a rien de plus que le deck de base (c'est le même),
 * et sa vignette retombait sur la carte de héros là où celle de la variante
 * montrait bien son alliée (Hellcat : Iron Man affiché en Hellcat, Miss Hulk
 * bien affichée, releve de l'utilisateur du 12/09/2026).
 */
export function apercuVersion(hero, version) {
    const cartes = (d) => [
        ...((d && d.hero) || []).flatMap((x) => String(x).split(",")),
        ...((d && d.hero_deck) || []), ...((d && d.obligations) || []),
    ];
    const autres = versionsDe(hero).filter((v) => v !== version && v.id !== version.id);
    const socle = new Set(autres.flatMap((v) => cartes(v.deck)));
    const propre = autres.length ? cartes(version.deck).find((id) => !socle.has(id)) : undefined;
    const heros = (version.deck && version.deck.hero && version.deck.hero[0]) || (hero && hero.heroCardId) || "";
    return propre || String(heros).split(",")[0];
}


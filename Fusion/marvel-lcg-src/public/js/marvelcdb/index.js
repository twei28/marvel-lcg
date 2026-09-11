// index.js — accès à l'index local des decks MarvelCDB.
//
// Les fichiers sont produits par tools/marvelcdb_index.py et servis par la
// route existante /read_file, qui rend n'importe quel JSON du dossier de jeu.
// Aucune route serveur n'a été ajoutée.
"use strict";

const _cache = new Map();
let _popularite = null;

/** Le classement de popularite, commun a tous les heros.
 *
 *  ⚠ IL VIENT DES PAGES DU SITE, PAS DE L'API. Celle-ci ne porte AUCUN champ
 *  de popularite : ni `by_date`, ni la route par deck (verifie champ par champ
 *  le 11/09/2026), et `popular`/`hot`/`search` y repondent 404. Seul le site
 *  classe les decks, d'ou `tools/marvelcdb_popularite.py` qui en releve
 *  l'ORDRE.
 *
 *  ⚠ UN RANG, PAS UN NOMBRE DE VOTES. La page ne montre pas le compte : rien
 *  ne dit si le premier devance le second d'une voix ou de cent. On peut
 *  trier, on ne peut pas afficher un score.
 *
 *  Absent ou illisible, le tri par popularite n'est simplement pas propose :
 *  l'ecran reste utilisable quand le releve n'a jamais tourne. */
async function chargerPopularite(fetcher) {
    if (_popularite) return _popularite;
    _popularite = fetcher("/read_file?data/marvelcdb/_popularite.json")
        .then((r) => (r.ok ? r.json() : null))
        .then((p) => (p && p.rangs && typeof p.rangs === "object" ? p.rangs : {}))
        .catch(() => ({}));
    return _popularite;
}

/** Index d'un héros. Un héros sans index rend un paquet VIDE, pas une erreur :
 *  l'écran doit rester utilisable quand l'indexeur n'a jamais tourné. */
export async function chargerHeros(heroCode, recuperer) {
    const code = String(heroCode || "").split(",")[0];
    if (!code) return paquetVide(code);
    if (_cache.has(code)) return _cache.get(code);
    const fetcher = recuperer || ((url) => fetch(url));
    const promesse = Promise.all([
        fetcher("/read_file?data/marvelcdb/" + encodeURIComponent(code) + ".json")
            .then((r) => (r.ok ? r.json() : paquetVide(code)))
            .then((p) => (p && Array.isArray(p.decks) ? p : paquetVide(code)))
            .catch(() => paquetVide(code)),
        chargerPopularite(fetcher),
    ]).then(([paquet, rangs]) => {
        // Le rang est POSE SUR CHAQUE DECK plutot que passe a part : `filtrer`
        // reste une fonction pure sur une liste, sans second argument a
        // trimballer jusqu'a l'ecran.
        for (const deck of paquet.decks) {
            const rang = rangs[String(deck.id)];
            if (rang) deck.rang = rang;
        }
        return paquet;
    });
    _cache.set(code, promesse);
    return promesse;
}

function paquetVide(code) {
    return { hero_code: code, hero_name: "", deck_starter: "", decks: [] };
}

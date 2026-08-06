// index.js — accès à l'index local des decks MarvelCDB.
//
// Les fichiers sont produits par tools/marvelcdb_index.py et servis par la
// route existante /read_file, qui rend n'importe quel JSON du dossier de jeu.
// Aucune route serveur n'a été ajoutée.
"use strict";

const _cache = new Map();

/** Index d'un héros. Un héros sans index rend un paquet VIDE, pas une erreur :
 *  l'écran doit rester utilisable quand l'indexeur n'a jamais tourné. */
export async function chargerHeros(heroCode, recuperer) {
    const code = String(heroCode || "").split(",")[0];
    if (!code) return paquetVide(code);
    if (_cache.has(code)) return _cache.get(code);
    const fetcher = recuperer || ((url) => fetch(url));
    const promesse = fetcher("/read_file?data/marvelcdb/" + encodeURIComponent(code) + ".json")
        .then((r) => (r.ok ? r.json() : paquetVide(code)))
        .then((p) => (p && Array.isArray(p.decks) ? p : paquetVide(code)))
        .catch(() => paquetVide(code));
    _cache.set(code, promesse);
    return promesse;
}

function paquetVide(code) {
    return { hero_code: code, hero_name: "", deck_starter: "", decks: [] };
}

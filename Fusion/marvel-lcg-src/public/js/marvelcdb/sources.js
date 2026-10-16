// Les sites dont on sait importer un deck a partir d'un lien (16/10/2026).
//
// MarvelCDB et MC4DB (la base de Merlin, mc4db.merlindumesnil.net) parlent la
// MEME API : `/api/public/decklist/<id>.json` et `/api/public/deck/<id>.json`,
// avec `hero_code` et `slots`. Une seule conversion sert donc aux deux
// (conversion.js). Les NUMEROTATIONS, elles, sont distinctes : le deck 1 de
// MarvelCDB n'est pas le deck 1 de MC4DB. Un lien ne se lit donc que sur SON
// site ; seul un numero nu (sans lien) est tente sur MarvelCDB, puis sur MC4DB
// quand MarvelCDB ne repond pas (panne), jamais quand il repond « introuvable ».
// Les decks prives (`/deck/`) sont refuses par MC4DB (403) : normal.

export const SITES = [
    { cle: "marvelcdb", nom: "MarvelCDB", base: "https://marvelcdb.com", reconnait: /marvelcdb\.com/i },
    { cle: "mc4db", nom: "MC4DB", base: "https://mc4db.merlindumesnil.net", reconnait: /mc4db|merlindumesnil/i },
];

/** Ce qu'on lit dans la saisie : le numero, le site si c'est un lien, la forme (liste publiee ou deck). */
export function lireLien(saisie) {
    const s = String(saisie || "").trim();
    const site = SITES.find((x) => x.reconnait.test(s)) || null;
    const avecChemin = s.match(/(?:decklist|deck)\/(?:view\/)?(\d+)/);
    const nu = s.match(/(\d{3,})/);
    return { id: avecChemin ? avecChemin[1] : (nu ? nu[1] : ""), site, decklist: /decklist/.test(s) };
}

/** Rend { data, site } ou null. `chercher` est injectable pour les tests. */
export async function chargerDeck(saisie, chercher = (u) => fetch(u)) {
    const { id, site, decklist } = lireLien(saisie);
    if (!id) return null;
    const sites = site ? [site] : [SITES[0], SITES[1]];
    for (const [rang, s] of sites.entries()) {
        const formes = [`decklist/${id}.json`, `deck/${id}.json`];
        // Deux numerotations par site : l'ordre suit le type de lien colle.
        if (site && !decklist && /\/deck\//.test(String(saisie))) formes.reverse();
        if (!site && !decklist && /deck/.test(String(saisie))) formes.reverse();
        let repondu = false;
        for (const f of formes) {
            try {
                const r = await chercher(`${s.base}/api/public/${f}`);
                if (r.ok) return { data: await r.json(), site: s };
                if (r.status < 500) repondu = true;
            } catch (e) { /* panne : on essaie la suite */ }
        }
        // Numero nu : on ne passe au site suivant QUE si celui-ci n'a pas repondu.
        if (!site && repondu) break;
    }
    return null;
}

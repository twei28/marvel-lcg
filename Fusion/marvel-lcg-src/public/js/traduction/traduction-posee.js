// GÉNÉRÉ par ui-app/outils/generer-traduction-public.mjs depuis ui-app/src/board/traduction-posee.ts — NE PAS ÉDITER.
// La traduction POSÉE sur la carte : la zone de texte claire du scan anglais est
// recouverte d'un cache de sa couleur, et le français s'écrit dessus.
//
// La zone n'est pas une table par type : elle est LUE sur le scan (packs
// officiels et fan-made n'ont pas tous la même mise en page). Partie pure,
// testée par traduction-posee.test.ts ; le composant vit dans TraductionPosee.tsx.
import { TRAITS_FR } from './traits-fr.js';
function estClair(r, g, b) {
    const min = Math.min(r, g, b);
    return min > 170 && Math.max(r, g, b) - min < 45;
}
/** La plus longue suite d'indices consécutifs dont la valeur atteint le seuil. */
function plusLongueSuite(valeurs, seuil, debut = 0) {
    let meilleur = null;
    let courant = -1;
    for (let i = debut; i < valeurs.length; i += 1) {
        if (valeurs[i] >= seuil) {
            if (courant < 0)
                courant = i;
            if (!meilleur || i - courant > meilleur[1] - meilleur[0])
                meilleur = [courant, i];
        }
        else {
            courant = -1;
        }
    }
    return meilleur;
}
/** Dilatation (max) ou érosion (min) carrée de rayon r ; hors image = vide. */
function morpho(source, largeur, hauteur, r, dilater) {
    const sortie = new Uint8Array(source.length);
    for (let y = 0; y < hauteur; y += 1) {
        for (let x = 0; x < largeur; x += 1) {
            let v = dilater ? 0 : 1;
            for (let dy = -r; dy <= r && (dilater ? v === 0 : v === 1); dy += 1) {
                for (let dx = -r; dx <= r; dx += 1) {
                    const yy = y + dy;
                    const xx = x + dx;
                    const dedans = yy >= 0 && yy < hauteur && xx >= 0 && xx < largeur ? source[yy * largeur + xx] : 0;
                    if (dilater && dedans) {
                        v = 1;
                        break;
                    }
                    if (!dilater && !dedans) {
                        v = 0;
                        break;
                    }
                }
            }
            sortie[y * largeur + x] = v;
        }
    }
    return sortie;
}
/**
 * Cherche la zone de texte d'une carte PORTRAIT dans ses pixels RGBA (300 x 420
 * conseillé : les badges y gardent un anneau net).
 *
 * 1. Une bande de lignes majoritairement claires sous le premier tiers, bornée
 *    par ses colonnes claires : le cœur de la zone.
 * 2. Un remplissage depuis ce cœur, sur le fond (clair ou gris moyen neutre),
 *    par des passages d'au moins 3 x 3 pixels : il contourne les lettres mais
 *    ne passe pas la jonction floue d'un badge.
 * 3. Une fermeture de 2 pixels comble les lettres.
 * 4. Ligne par ligne, les morceaux de zone sont réunis tant que le trou qui les
 *    sépare n'est que du texte ; un aplat coloré, l'intérieur clair d'un badge
 *    ou un trait sombre vertical (son anneau) le coupe.
 * 5. Les bords sont lissés (médiane sur 9 lignes).
 *
 * Null quand rien de net n'apparaît : le texte reste alors dans l'encadré.
 */
export function detecterZoneTexte(pixels, largeur, hauteur) {
    const n = largeur * hauteur;
    const L = new Uint8Array(n);
    const F0 = new Uint8Array(n);
    const neutreFort = new Uint8Array(n);
    for (let k = 0; k < n; k += 1) {
        const r = pixels[k * 4];
        const g = pixels[k * 4 + 1];
        const b = pixels[k * 4 + 2];
        const min = Math.min(r, g, b);
        const ecart = Math.max(r, g, b) - min;
        L[k] = estClair(r, g, b) ? 1 : 0;
        F0[k] = L[k] || (ecart < 28 && min >= 110) ? 1 : 0;
        neutreFort[k] = ecart < 40 ? 1 : 0;
    }
    const lignes = [];
    for (let y = 0; y < hauteur; y += 1) {
        let c = 0;
        for (let x = 0; x < largeur; x += 1)
            c += L[y * largeur + x];
        lignes.push(c / largeur);
    }
    const bande = plusLongueSuite(lignes, 0.42, Math.floor(hauteur * 0.3));
    if (!bande || bande[1] - bande[0] + 1 < hauteur * 0.12)
        return null;
    const colonnes = [];
    for (let x = 0; x < largeur; x += 1) {
        let c = 0;
        for (let y = bande[0]; y <= bande[1]; y += 1)
            c += L[y * largeur + x];
        colonnes.push(c / (bande[1] - bande[0] + 1));
    }
    const etendue = plusLongueSuite(colonnes, 0.5);
    if (!etendue || etendue[1] - etendue[0] + 1 < largeur * 0.4)
        return null;
    const [cx0, cx1] = etendue;
    const ya = Math.max(Math.floor(hauteur * 0.25), bande[0] - Math.floor(hauteur * 0.2));
    const yb = Math.min(hauteur - 1, bande[1] + Math.floor(hauteur * 0.15));
    const xa = Math.max(0, cx0 - 2);
    const xb = Math.min(largeur - 1, cx1 + 2);
    // 2. Remplissage par des passages épais.
    const F = morpho(F0, largeur, hauteur, 1, false);
    const M = new Uint8Array(n);
    const pile = [];
    for (let y = bande[0]; y <= bande[1]; y += 1) {
        for (let x = cx0; x <= cx1; x += 1) {
            const k = y * largeur + x;
            if (F[k] && colonnes[x] >= 0.5) {
                M[k] = 1;
                pile.push(k);
            }
        }
    }
    while (pile.length) {
        const k = pile.pop();
        const x = k % largeur;
        const y = (k - x) / largeur;
        const voisins = [
            [x + 1, y],
            [x - 1, y],
            [x, y + 1],
            [x, y - 1],
        ];
        for (const [nx, ny] of voisins) {
            if (nx < xa || nx > xb || ny < ya || ny > yb)
                continue;
            const kk = ny * largeur + nx;
            if (!M[kk] && F[kk]) {
                M[kk] = 1;
                pile.push(kk);
            }
        }
    }
    // 3. Fermeture : les lettres.
    const C = morpho(morpho(M, largeur, hauteur, 2, true), largeur, hauteur, 2, false);
    // 4. Obstacles : intérieur clair épais hors zone, aplat coloré, trait vertical sombre.
    const horsZone = new Uint8Array(n);
    for (let k = 0; k < n; k += 1)
        horsZone[k] = F0[k] && !M[k] ? 1 : 0;
    const interieur = morpho(horsZone, largeur, hauteur, 2, false);
    const vertical = new Int32Array(n);
    for (let x = 0; x < largeur; x += 1) {
        let y = 0;
        while (y < hauteur) {
            if (F0[y * largeur + x]) {
                y += 1;
                continue;
            }
            const d = y;
            while (y < hauteur && !F0[y * largeur + x])
                y += 1;
            for (let yy = d; yy < y; yy += 1)
                vertical[yy * largeur + x] = y - d;
        }
    }
    const colore = Math.max(3, Math.round(largeur * 0.013));
    const traitVertical = Math.round(hauteur * 0.06);
    const obstacle = (y, a, b) => {
        let suite = 0;
        for (let x = a; x <= b; x += 1) {
            const k = y * largeur + x;
            if (interieur[k] || vertical[k] >= traitVertical)
                return true;
            suite = neutreFort[k] ? 0 : suite + 1;
            if (suite >= colore)
                return true;
        }
        return false;
    };
    const brut = [];
    for (let y = 0; y < hauteur; y += 1) {
        const morceaux = [];
        let debut = -1;
        for (let x = 0; x <= largeur; x += 1) {
            const v = x < largeur && C[y * largeur + x];
            if (v && debut < 0)
                debut = x;
            if (!v && debut >= 0) {
                morceaux.push([debut, x - 1]);
                debut = -1;
            }
        }
        const fusion = [];
        for (const m of morceaux) {
            const dernier = fusion[fusion.length - 1];
            if (dernier && !obstacle(y, dernier[1] + 1, m[0] - 1))
                dernier[1] = m[1];
            else
                fusion.push([m[0], m[1]]);
        }
        brut.push(fusion.length ? fusion.reduce((a, b) => (b[1] - b[0] > a[1] - a[0] ? b : a)) : null);
    }
    const largeurs = brut.filter((r) => r !== null).map(([g, d]) => d - g).sort((a, b) => a - b);
    if (!largeurs.length)
        return null;
    const typique = largeurs[Math.floor(largeurs.length / 2)];
    const retenues = [];
    brut.forEach((r, y) => {
        if (r && r[1] - r[0] >= typique * 0.5)
            retenues.push(y);
    });
    if (!retenues.length)
        return null;
    const y0 = retenues[0];
    const y1 = retenues[retenues.length - 1];
    // 5. Lissage des bords.
    const bordsPx = [];
    for (let y = y0; y <= y1; y += 1) {
        const fenetre = [];
        for (let j = Math.max(y0, y - 4); j <= Math.min(y1, y + 4); j += 1) {
            const r = brut[j];
            if (r)
                fenetre.push(r);
        }
        if (!fenetre.length) {
            bordsPx.push(bordsPx[bordsPx.length - 1] ?? [cx0, cx1]);
            continue;
        }
        const gauches = fenetre.map((r) => r[0]).sort((a, b) => a - b);
        const droites = fenetre.map((r) => r[1]).sort((a, b) => a - b);
        bordsPx.push([gauches[Math.floor(gauches.length / 2)], droites[Math.floor(droites.length / 2)]]);
    }
    const somme = [0, 0, 0];
    let compte = 0;
    bordsPx.forEach(([g, d], i) => {
        const y = y0 + i;
        for (let x = g; x <= d; x += 1) {
            const k = y * largeur + x;
            if (!L[k])
                continue;
            somme[0] += pixels[k * 4];
            somme[1] += pixels[k * 4 + 1];
            somme[2] += pixels[k * 4 + 2];
            compte += 1;
        }
    });
    if (!compte)
        return null;
    const x0 = Math.min(...bordsPx.map((b) => b[0]));
    const x1 = Math.max(...bordsPx.map((b) => b[1]));
    return {
        x0: x0 / largeur,
        y0: y0 / hauteur,
        x1: (x1 + 1) / largeur,
        y1: (y1 + 1) / hauteur,
        fond: [0, 1, 2].map((k) => Math.round(somme[k] / compte)),
        bords: bordsPx.map(([g, d]) => [g / largeur, (d + 1) / largeur]),
    };
}
/** Glyphes de la police ChampionsIcons (relevés sur public/fonts/ChampionsIcons.ttf). */
const GLYPHES = {
    physical: 'P',
    mental: 'M',
    energy: 'E',
    wild: 'W',
    star: 'S',
    unique: 'U',
    per_hero: 'G',
    per_player: 'G',
    boost: 'B',
    crisis: 'C',
    acceleration: 'A',
    hazard: 'H',
    amplify: 'D',
};
/**
 * Le texte d'une traduction (balises <b>/<i>, jetons « [energy] », traits
 * « [[AÉRIEN]] », sauts de ligne) en HTML prêt à poser. Seules les balises de
 * mise en forme survivent ; un jeton inconnu reste écrit en toutes lettres.
 */
export function texteEnHtml(texte) {
    return texte
        .replace(/<(?!\/?(b|i|em|strong|br)\b)[^>]*>/g, '')
        .replace(/\[\[([^\]]+)\]\]/g, (_, trait) => `<span class="tp-trait">${TRAITS_FR[trait.toUpperCase()] ?? trait}</span>`)
        .replace(/\[([a-z_]+)\]/g, (tout, cle) => GLYPHES[cle] ? `<span class="tp-icone tp-icone-${cle}">${GLYPHES[cle]}</span>` : tout)
        .replace(/\n/g, '<br />');
}
/**
 * La forme du cache en CSS : un `clip-path: polygon(...)` qui suit les bords de
 * chaque ligne, et les encoches du HAUT, que le texte doit contourner (deux
 * flottants les réservent). Pourcentages relatifs au rectangle du cache.
 */
export function formeDuCache(zone) {
    const largeur = zone.x1 - zone.x0;
    const n = zone.bords.length;
    const versX = (x) => Math.round(((x - zone.x0) / largeur) * 1000) / 10;
    const versY = (i) => Math.round((i / n) * 1000) / 10;
    const points = [];
    const ajouter = (x, y) => {
        const point = `${x}% ${y}%`;
        if (points[points.length - 1] !== point)
            points.push(point);
    };
    zone.bords.forEach(([g], i) => {
        ajouter(versX(g), versY(i));
        ajouter(versX(g), versY(i + 1));
    });
    for (let i = n - 1; i >= 0; i -= 1) {
        ajouter(versX(zone.bords[i][1]), versY(i + 1));
        ajouter(versX(zone.bords[i][1]), versY(i));
    }
    const mediane = (valeurs) => [...valeurs].sort((a, b) => a - b)[Math.floor(valeurs.length / 2)];
    const tolerance = 0.02;
    const encoche = (cote) => {
        const reference = mediane(zone.bords.map((b) => b[cote]));
        let lignes = 0;
        let pire = reference;
        for (const bord of zone.bords) {
            const rentre = cote === 1 ? bord[1] < reference - tolerance : bord[0] > reference + tolerance;
            if (!rentre)
                break;
            lignes += 1;
            pire = cote === 1 ? Math.min(pire, bord[1]) : Math.max(pire, bord[0]);
        }
        if (lignes === 0)
            return null;
        return { hauteur: versY(lignes), largeur: Math.round((Math.abs(reference - pire) / largeur) * 1000) / 10 };
    };
    return { clipPath: `polygon(${points.join(', ')})`, gauche: encoche(0), droite: encoche(1) };
}
/** Les traits imprimés (« AERIAL », « Dark Elf ») en français quand on les connaît : « AÉRIEN. DARK ELF. » */
export function ligneDeTraits(traits, traduction) {
    return traits
        .map((trait) => trait.trim().replace(/\.$/, ''))
        .filter(Boolean)
        .map((trait) => `${traduction[trait.toUpperCase()] ?? trait.toUpperCase()}.`)
        .join(' ');
}

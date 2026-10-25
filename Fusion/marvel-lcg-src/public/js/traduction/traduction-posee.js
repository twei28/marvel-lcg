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
/** Les bords d'une rangée AJOUTÉE : la médiane des bords des `n` rangées voisines, qu'un badge ou une ombre ne peut pas creuser d'une seule rangée. */
function bordsMedians(voisines) {
    const g = voisines.map((b) => b[0]).sort((a, b) => a - b);
    const d = voisines.map((b) => b[1]).sort((a, b) => a - b);
    return [g[Math.floor(g.length / 2)], d[Math.floor(d.length / 2)]];
}
/**
 * Prolonge le bas de la zone sous un TRAIT DE SÉPARATION (la ligne « Boost » est souvent écrite sous un filet) : le
 * remplissage ne le franchit pas, et la dernière ligne anglaise restait visible sous le voile (audit du 25/10/2026,
 * une trentaine de cartes). On descend tant que des rangées claires portent de l'encre ÉTALÉE (du texte, pas un
 * pictogramme), en acceptant un filet de quelques pixels entre deux ; la bordure épaisse du cadre arrête la descente.
 * Rend la dernière rangée de texte trouvée (+ 2 px), ou `y1` si rien n'y est écrit.
 */
function prolongerVersLeBas(pixels, clair, largeur, hauteur, x0, x1, y1) {
    // Le milieu de la zone seulement : un badge (ATQ, icône) ou une bordure de coin ne doit pas faire passer la rangée pour « sombre ».
    const marge = Math.round((x1 - x0) * 0.2);
    const a = x0 + marge;
    const b = x1 - marge;
    const total = b - a + 1;
    if (total < 20)
        return y1;
    const limite = Math.min(hauteur - 1, y1 + Math.round(hauteur * 0.2));
    const lignes = [];
    let filet = 0;
    // La dernière rangée qui porte de l'encre DANS la zone : le grand blanc du bas du cadre ne compte pas comme « proche du texte ».
    let dernierTexte = y1;
    for (let y = y1; y > y1 - 80 && y >= 0; y -= 1) {
        let encre = 0;
        for (let x = a; x <= b; x += 1) {
            const k = y * largeur + x;
            if (!clair[k] && 0.299 * pixels[k * 4] + 0.587 * pixels[k * 4 + 1] + 0.114 * pixels[k * 4 + 2] < 125)
                encre += 1;
        }
        if (encre / total >= 0.02) {
            dernierTexte = y;
            break;
        }
    }
    for (let y = y1 + 1; y <= limite; y += 1) {
        let claires = 0;
        let encre = 0;
        let premiere = -1;
        let derniere = -1;
        let paquets = 0;
        let avant = false;
        for (let x = a; x <= b; x += 1) {
            const k = y * largeur + x;
            const sombre = !clair[k] && 0.299 * pixels[k * 4] + 0.587 * pixels[k * 4 + 1] + 0.114 * pixels[k * 4 + 2] < 125;
            if (clair[k])
                claires += 1;
            if (sombre) {
                encre += 1;
                if (premiere < 0)
                    premiere = x;
                derniere = x;
                if (!avant)
                    paquets += 1;
            }
            avant = sombre;
        }
        // Une bande noire à lettres blanches (le bandeau du bas : « DONATELLO NEMESIS ») a assez de pixels clairs pour passer pour du texte : le noir dominant la trahit.
        const estClaire = claires / total >= 0.3 && encre / total <= 0.5;
        if (!estClaire) {
            filet += 1;
            if (filet > 2)
                break;
            lignes.push({ y, claire: false, encre, paquets, texte: false });
            continue;
        }
        filet = 0;
        const part = encre / total;
        const texte = part >= 0.02 && part <= 0.5 && (derniere - premiere) / total >= 0.3 && paquets >= 5;
        lignes.push({ y, claire: true, encre, paquets, texte });
        // Un grand blanc, puis du « texte » : c'est le bandeau du bas, pas la suite du cadre.
        if (texte)
            dernierTexte = y;
        else if (y - dernierTexte > 28)
            break;
    }
    const textes = lignes.filter((l) => l.texte);
    if (textes.length < 3)
        return y1;
    // Jusqu'au bout du texte : les hampes et les jambages portent moins d'encre que le corps des lettres, et une DERNIÈRE LIGNE COURTE
    // (« first player. », « Shredder. ») n'a ni l'étendue ni les paquets d'une ligne pleine. Un pictogramme plein (beaucoup d'encre d'un coup) ne compte pas.
    let fin = textes[textes.length - 1].y;
    let vides = 0;
    for (const l of lignes.filter((r) => r.y > fin)) {
        if (!l.claire)
            break;
        if (l.paquets >= 1 && l.encre / total >= 0.015 && l.encre / total <= 0.2) {
            fin = l.y;
            vides = 0;
        }
        else {
            vides += 1;
            if (vides > 12)
                break;
        }
    }
    return Math.min(limite, fin + 3);
}
/**
 * Prolonge le HAUT de la zone sur la ligne de TRAITS imprimée (« TECH. WEAPON. ») : sur un cadre à décor, elle est écrite sur
 * un bandeau teinté qui n'est pas du « clair » de la zone, la détection commence sous elle, et l'anglais restait visible
 * au-dessus du voile, au-dessus des traits français réécrits (audit du 25/10/2026). On monte à travers des rangées
 * claires ou portant du texte, mais SEULEMENT si la montée butte sur une frontière (bordure sombre, barre du titre,
 * illustration) avant la limite : sans frontière, on est dans l'illustration et on ne touche à rien.
 */
export function prolongerVersLeHaut(pixels, clair, largeur, hauteur, x0, x1, y0) {
    const marge = Math.round((x1 - x0) * 0.2);
    const a = x0 + marge;
    const b = x1 - marge;
    const total = b - a + 1;
    if (total < 20)
        return y0;
    const limite = Math.max(0, y0 - Math.round(hauteur * 0.06));
    let haut = y0;
    let vides = 0;
    let frontiere = false;
    for (let y = y0 - 1; y >= limite; y -= 1) {
        let lumineuses = 0;
        let encre = 0;
        for (let x = a; x <= b; x += 1) {
            const k = y * largeur + x;
            const lum = 0.299 * pixels[k * 4] + 0.587 * pixels[k * 4 + 1] + 0.114 * pixels[k * 4 + 2];
            if (clair[k] || lum > 150)
                lumineuses += 1;
            if (lum < 125)
                encre += 1;
        }
        if (lumineuses / total < 0.45 || encre / total > 0.6) {
            frontiere = true;
            break;
        }
        if (encre / total >= 0.01) {
            haut = y;
            vides = 0;
        }
        else {
            vides += 1;
            if (vides > 8) {
                frontiere = true;
                break;
            }
        }
    }
    if (!frontiere || haut >= y0)
        return y0;
    // Un rang de marge au-dessus du texte, sauf si la frontière le touche : elle reste visible.
    return Math.max(limite, haut - 1);
}
/**
 * Prolonge une zone DÉJÀ détectée (manigance paysage) vers le haut et vers le bas, comme la détection portrait le fait
 * d'elle-même : la citation en italique au-dessus du texte et la ligne « Boost » sous le filet restaient en anglais.
 * Les lignes de `bords` ajoutées prolongent la première et la dernière.
 */
export function prolongerLaZone(zone, pixels, largeur, hauteur) {
    const clair = new Uint8Array(largeur * hauteur);
    for (let k = 0; k < clair.length; k += 1) {
        const r = pixels[k * 4];
        const g = pixels[k * 4 + 1];
        const b = pixels[k * 4 + 2];
        const proche = Math.abs(r - zone.fond[0]) + Math.abs(g - zone.fond[1]) + Math.abs(b - zone.fond[2]) <= ECART_FOND;
        clair[k] = proche || estClair(r, g, b) ? 1 : 0;
    }
    const x0 = Math.round(zone.x0 * largeur);
    const x1 = Math.round(zone.x1 * largeur) - 1;
    const y0 = Math.round(zone.y0 * hauteur);
    const y1 = Math.round(zone.y1 * hauteur) - 1;
    const yBas = prolongerVersLeBas(pixels, clair, largeur, hauteur, x0, x1, y1);
    const yHaut = prolongerVersLeHaut(pixels, clair, largeur, hauteur, x0, x1, y0);
    if (yBas === y1 && yHaut === y0)
        return zone;
    const n = zone.bords.length;
    const parLigne = n / Math.max(1, y1 - y0 + 1);
    const ajoutBas = Math.round((yBas - y1) * parLigne);
    const ajoutHaut = Math.round((y0 - yHaut) * parLigne);
    const bords = zone.bords.slice();
    const bordsBas = bordsMedians(zone.bords.slice(-20));
    const bordsHaut = bordsMedians(zone.bords.slice(0, 20));
    for (let i = 0; i < ajoutBas; i += 1)
        bords.push(bordsBas);
    for (let i = 0; i < ajoutHaut; i += 1)
        bords.unshift(bordsHaut);
    return { ...zone, y0: yHaut / hauteur, y1: (yBas + 1) / hauteur, bords };
}
/** Écart toléré, somme des trois canaux, entre un pixel et le fond donné. */
const ECART_FOND = 66;
export function detecterZoneTexte(pixels, largeur, hauteur, options = {}) {
    const { debutBande = 0.3, plafond = 0.25, fond, relache = false } = options;
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
        L[k] = (fond ? Math.abs(r - fond[0]) + Math.abs(g - fond[1]) + Math.abs(b - fond[2]) <= ECART_FOND : estClair(r, g, b)) ? 1 : 0;
        F0[k] = L[k] || (ecart < 28 && min >= 110) ? 1 : 0;
        // Un fond coloré n'est pas un aplat qui coupe la zone : il EST la zone.
        neutreFort[k] = ecart < 40 || (fond !== undefined && L[k]) ? 1 : 0;
    }
    const lignes = [];
    for (let y = 0; y < hauteur; y += 1) {
        let c = 0;
        for (let x = 0; x < largeur; x += 1)
            c += L[y * largeur + x];
        lignes.push(c / largeur);
    }
    const bande = plusLongueSuite(lignes, relache ? 0.3 : 0.42, Math.floor(hauteur * debutBande));
    if (!bande || bande[1] - bande[0] + 1 < hauteur * (relache ? 0.06 : 0.12))
        return null;
    const colonnes = [];
    for (let x = 0; x < largeur; x += 1) {
        let c = 0;
        for (let y = bande[0]; y <= bande[1]; y += 1)
            c += L[y * largeur + x];
        colonnes.push(c / (bande[1] - bande[0] + 1));
    }
    const etendue = plusLongueSuite(colonnes, relache ? 0.4 : 0.5);
    if (!etendue || etendue[1] - etendue[0] + 1 < largeur * (relache ? 0.3 : 0.4))
        return null;
    const [cx0, cx1] = etendue;
    const ya = Math.max(Math.floor(hauteur * plafond), bande[0] - Math.floor(hauteur * 0.2));
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
    const yBas = prolongerVersLeBas(pixels, L, largeur, hauteur, x0, x1, y1);
    const bordsBas = bordsMedians(bordsPx.slice(-20));
    for (let y = y1 + 1; y <= yBas; y += 1)
        bordsPx.push(bordsBas);
    const yHaut = prolongerVersLeHaut(pixels, L, largeur, hauteur, x0, x1, y0);
    const bordsHaut = bordsMedians(bordsPx.slice(0, 20));
    for (let y = y0 - 1; y >= yHaut; y -= 1)
        bordsPx.unshift(bordsHaut);
    return {
        x0: x0 / largeur,
        y0: yHaut / hauteur,
        x1: (x1 + 1) / largeur,
        y1: (yBas + 1) / hauteur,
        fond: [0, 1, 2].map((k) => Math.round(somme[k] / compte)),
        bords: bordsPx.map(([g, d]) => [g / largeur, (d + 1) / largeur]),
    };
}
/**
 * La zone, de l'IMAGE vers le CADRE de la carte.
 *
 * Le scan est posé dans le cadre en `object-fit: cover` (ScanCard.css) : quand son rapport hauteur/largeur n'est pas celui
 * du cadre (176/127), il est agrandi puis ROGNÉ, de moitié en haut et en bas (ou à gauche et à droite). Les fractions
 * lues sur l'image entière n'étaient plus celles du cadre : au bas d'un scan de 615 x 882, le voile tombait 6 px trop
 * haut et laissait dépasser la dernière ligne anglaise (audit du 25/10/2026, la cause de la plupart des cas « anglais
 * sous le voile »).
 */
export function zoneDansLeCadre(zone, image, cadre) {
    if (!(image.largeur > 0 && image.hauteur > 0 && cadre.largeur > 0 && cadre.hauteur > 0))
        return zone;
    const echelle = Math.max(cadre.largeur / image.largeur, cadre.hauteur / image.hauteur);
    const dessinee = { largeur: image.largeur * echelle, hauteur: image.hauteur * echelle };
    if (Math.abs(dessinee.largeur - cadre.largeur) < 0.5 && Math.abs(dessinee.hauteur - cadre.hauteur) < 0.5)
        return zone;
    const dx = (cadre.largeur - dessinee.largeur) / 2;
    const dy = (cadre.hauteur - dessinee.hauteur) / 2;
    const fx = (v) => Math.min(1, Math.max(0, (v * dessinee.largeur + dx) / cadre.largeur));
    const fy = (v) => Math.min(1, Math.max(0, (v * dessinee.hauteur + dy) / cadre.hauteur));
    return {
        ...zone,
        x0: fx(zone.x0),
        x1: fx(zone.x1),
        y0: fy(zone.y0),
        y1: fy(zone.y1),
        bords: zone.bords.map(([g, d]) => [fx(g), fx(d)]),
    };
}
/**
 * La couleur du fond de la zone de texte, lue dans un rectangle (fractions de
 * la carte) : médiane des pixels clairs, ou null s'ils sont trop rares pour
 * être un fond plutôt qu'un détail de l'illustration.
 */
export function couleurDuFond(pixels, largeur, hauteur, [fx0, fy0, fx1, fy1]) {
    const canaux = [[], [], []];
    let total = 0;
    for (let y = Math.floor(fy0 * hauteur); y < Math.floor(fy1 * hauteur); y += 1) {
        for (let x = Math.floor(fx0 * largeur); x < Math.floor(fx1 * largeur); x += 1) {
            const k = (y * largeur + x) * 4;
            total += 1;
            if (Math.min(pixels[k], pixels[k + 1], pixels[k + 2]) < 150)
                continue;
            canaux[0].push(pixels[k]);
            canaux[1].push(pixels[k + 1]);
            canaux[2].push(pixels[k + 2]);
        }
    }
    if (!total || canaux[0].length < total * 0.45)
        return null;
    return canaux.map((c) => c.sort((a, b) => a - b)[Math.floor(c.length / 2)]);
}
/**
 * La zone de texte d'une carte dont le cadre n'est PAS gris clair (Skrulls verts, cadres teintés de crème ou de bleu) : la
 * détection ordinaire n'y trouve rien et le texte anglais restait en clair (audit du 25/10/2026, une cinquantaine de
 * cartes). On lit la couleur du fond dans la bande où ces cadres écrivent, puis on relance la détection sur CETTE couleur.
 */
export function detecterZoneSurFondTeinte(pixels, largeur, hauteur) {
    const sondes = [
        [0.35, 0.66, 0.65, 0.74],
        [0.3, 0.72, 0.7, 0.8],
        [0.35, 0.6, 0.65, 0.68],
        [0.35, 0.78, 0.65, 0.86],
    ];
    for (const sonde of sondes) {
        const fond = couleurDuFond(pixels, largeur, hauteur, sonde);
        if (!fond)
            continue;
        const zone = detecterZoneTexte(pixels, largeur, hauteur, { fond }) ?? detecterZoneTexte(pixels, largeur, hauteur, { fond, relache: true });
        if (zone)
            return zone;
    }
    return detecterZoneTexte(pixels, largeur, hauteur, { relache: true });
}
/** Boîtes englobantes des taches sombres connexes d'un masque : [x0, y0, x1, y1, pixels]. */
function taches(masque, largeur, hauteur) {
    const vu = new Uint8Array(masque.length);
    const sortie = [];
    const pile = [];
    for (let depart = 0; depart < masque.length; depart += 1) {
        if (!masque[depart] || vu[depart])
            continue;
        vu[depart] = 1;
        pile.push(depart);
        let [x0, y0, x1, y1, n] = [largeur, hauteur, 0, 0, 0];
        while (pile.length) {
            const k = pile.pop();
            const x = k % largeur;
            const y = (k - x) / largeur;
            n += 1;
            x0 = Math.min(x0, x);
            x1 = Math.max(x1, x);
            y0 = Math.min(y0, y);
            y1 = Math.max(y1, y);
            const voisins = [x + 1 < largeur ? k + 1 : -1, x > 0 ? k - 1 : -1, y + 1 < hauteur ? k + largeur : -1, y > 0 ? k - largeur : -1];
            for (const v of voisins) {
                if (v >= 0 && masque[v] && !vu[v]) {
                    vu[v] = 1;
                    pile.push(v);
                }
            }
        }
        sortie.push([x0, y0, x1, y1, n]);
    }
    return sortie;
}
/**
 * La zone de texte d'une carte PAYSAGE (manigances), dans ses pixels redressés
 * (420 x 300 conseillé).
 *
 * Officielles comme fan-made, les manigances suivent le gabarit FFG : la boîte
 * d'une manigance principale est à gauche, celle d'une annexe à droite. On lit
 * la couleur de son fond au cœur de la boîte (vert, crème, gris : pas toujours
 * clair et neutre), puis on pousse chaque bord tant qu'au moins un quart de la
 * ligne ou de la colonne est de ce fond : le texte, même dense, n'arrête pas
 * l'expansion, le cadre sombre et l'illustration si. Le remplissage pixel par
 * pixel du portrait échoue ici : un texte serré y bouche tous les passages.
 *
 * Les taches sombres plus hautes qu'une ligne de texte sont des badges ou des
 * icônes : contre un bord (menace, +1 par joueur), elles creusent une encoche ;
 * au milieu (boost, crise), elles restent visibles si plus rien n'est écrit
 * dessous, sinon la boîte entière est couverte pour que la traduction soit
 * complète.
 */
export function detecterZoneTextePaysage(pixels, largeur, hauteur, cote = 'gauche') {
    const sondes = { gauche: [0.06, 0.38, 0.44, 0.78], droite: [0.54, 0.38, 0.92, 0.78] };
    const ordre = cote === 'gauche' ? ['gauche', 'droite'] : ['droite', 'gauche'];
    for (const essai of ordre) {
        const fond = couleurDuFond(pixels, largeur, hauteur, [...sondes[essai]]);
        if (!fond)
            continue;
        const F = new Uint8Array(largeur * hauteur);
        for (let k = 0; k < F.length; k += 1) {
            const ecart = Math.abs(pixels[k * 4] - fond[0]) + Math.abs(pixels[k * 4 + 1] - fond[1]) + Math.abs(pixels[k * 4 + 2] - fond[2]);
            F[k] = ecart <= ECART_FOND ? 1 : 0;
        }
        const partLigne = (y, a, b) => {
            let c = 0;
            for (let x = a; x < b; x += 1)
                c += F[y * largeur + x];
            return c / (b - a);
        };
        const partColonne = (x, a, b) => {
            let c = 0;
            for (let y = a; y <= b; y += 1)
                c += F[y * largeur + x];
            return c / (b - a + 1);
        };
        const [sx0, sy0, sx1, sy1] = sondes[essai];
        // Chaque bord avance jusqu'au cadre. Le cadre, un onglet (« MAIN SCHEME ») ou
        // un bandeau (nom du set) sont des SUITES sombres continues ; le texte, même
        // serré, n'en fait jamais de longues. Il faut aussi rester sur du clair :
        // le fond, ou le liseré dégradé que certains gabarits fan-made mettent au
        // bord de la boîte, et sur lequel le texte déborde.
        const estSombre = (x, y) => {
            const k = (y * largeur + x) * 4;
            return pixels[k] + pixels[k + 1] + pixels[k + 2] < 330;
        };
        const estClairOuFond = (x, y) => {
            const k = (y * largeur + x) * 4;
            return F[y * largeur + x] === 1 || Math.min(pixels[k], pixels[k + 1], pixels[k + 2]) >= 150;
        };
        const ligneDansBoite = (y, a, b) => {
            if (y < 0 || y >= hauteur)
                return false;
            let suite = 0;
            let clairs = 0;
            const limite = 0.18 * (b - a + 1);
            for (let x = a; x <= b; x += 1) {
                suite = estSombre(x, y) ? suite + 1 : 0;
                if (suite >= limite)
                    return false;
                if (estClairOuFond(x, y))
                    clairs += 1;
            }
            return clairs / (b - a + 1) >= 0.3;
        };
        const colonneDansBoite = (x, a, b) => {
            if (x < 0 || x >= largeur)
                return false;
            let suite = 0;
            let clairs = 0;
            // Le cadre court sur presque toute la hauteur ; un badge (« +1 »), lui,
            // n'en couvre qu'un tiers et doit seulement creuser une encoche.
            const limite = 0.6 * (b - a + 1);
            for (let y = a; y <= b; y += 1) {
                suite = estSombre(x, y) ? suite + 1 : 0;
                if (suite >= limite)
                    return false;
                if (estClairOuFond(x, y))
                    clairs += 1;
            }
            return clairs / (b - a + 1) >= 0.3;
        };
        let haut = Math.floor(sy0 * hauteur);
        let bas = Math.floor(sy1 * hauteur);
        let gauche = Math.floor(sx0 * largeur);
        let droite = Math.floor(sx1 * largeur);
        // Du clair qui n'est pas le fond (liseré, mais aussi une illustration
        // claire) n'est accepté que tout près du dernier fond vu : 3 % au plus.
        const marge = Math.round(Math.max(largeur, hauteur) * 0.03);
        const avancer = (depart, pas, borne, dedans, fondIci) => {
            let bord = depart;
            let dernierFond = depart;
            for (let i = depart + pas; pas > 0 ? i <= borne : i >= borne; i += pas) {
                if (!dedans(i) || Math.abs(i - dernierFond) > marge)
                    break;
                bord = i;
                if (fondIci(i))
                    dernierFond = i;
            }
            return bord;
        };
        const etendreCotes = () => {
            gauche = avancer(gauche, -1, 0, (x) => colonneDansBoite(x, haut, bas), (x) => partColonne(x, haut, bas) >= 0.1);
            droite = avancer(droite, 1, largeur - 1, (x) => colonneDansBoite(x, haut, bas), (x) => partColonne(x, haut, bas) >= 0.1);
        };
        etendreCotes();
        haut = avancer(haut, -1, Math.floor(hauteur * 0.12), (y) => ligneDansBoite(y, gauche, droite), (y) => partLigne(y, gauche, droite + 1) >= 0.1);
        bas = avancer(bas, 1, hauteur - 1, (y) => ligneDansBoite(y, gauche, droite), (y) => partLigne(y, gauche, droite + 1) >= 0.1);
        etendreCotes();
        if (droite - gauche < largeur * 0.3 || bas - haut < hauteur * 0.3)
            continue;
        const bords = [];
        for (let y = haut; y <= bas; y += 1)
            bords.push([gauche, droite]);
        const lb = droite - gauche + 1;
        const masqueSombre = new Uint8Array(lb * (bas - haut + 1));
        // Trois pixels de bord laissés de côté : un liseré sombre collé à une
        // icône en ferait une seule tache trop large pour être reconnue.
        for (let y = haut + 3; y <= bas - 3; y += 1) {
            for (let x = gauche + 3; x <= droite - 3; x += 1) {
                const k = (y * largeur + x) * 4;
                masqueSombre[(y - haut) * lb + (x - gauche)] = pixels[k] + pixels[k + 1] + pixels[k + 2] < 330 ? 1 : 0;
            }
        }
        let coupe = bas;
        for (const [tx0, ty0, tx1, ty1, n] of taches(masqueSombre, lb, bas - haut + 1)) {
            const h = ty1 - ty0;
            const l = tx1 - tx0;
            if (h < hauteur * 0.06 || l < largeur * 0.03 || l > largeur * 0.16 || h > hauteur * 0.3 || n < 0.25 * h * l)
                continue;
            const [ax0, ay0, ax1, ay1] = [tx0 + gauche, ty0 + haut, tx1 + gauche, ty1 + haut];
            if (ax1 >= droite - largeur * 0.02) {
                for (let y = Math.max(haut, ay0 - 3); y <= bas; y += 1)
                    bords[y - haut][1] = Math.min(bords[y - haut][1], ax0 - 3);
            }
            else if (ax0 <= gauche + largeur * 0.02) {
                for (let y = Math.max(haut, ay0 - 3); y <= bas; y += 1)
                    bords[y - haut][0] = Math.max(bords[y - haut][0], ax1 + 3);
            }
            else if (ay0 > haut + 0.35 * (bas - haut)) {
                // Plus rien d'écrit sous l'icône (aucune ligne avec des lettres) : on la
                // laisse visible. Sinon la boîte entière est couverte.
                let texteDessous = false;
                for (let y = ay1 + 2; y <= bas - Math.round(hauteur * 0.04) && !texteDessous; y += 1) {
                    let sombres = 0;
                    for (let x = gauche + 3; x <= droite - 3; x += 1)
                        sombres += masqueSombre[(y - haut) * lb + (x - gauche)];
                    if (sombres / lb >= 0.04)
                        texteDessous = true;
                }
                if (!texteDessous)
                    coupe = Math.min(coupe, ay0 - 4);
            }
        }
        const fin = coupe - haut + 1;
        const bordsRetenus = bords.slice(0, fin);
        return {
            x0: gauche / largeur,
            y0: haut / hauteur,
            x1: (droite + 1) / largeur,
            y1: (coupe + 1) / hauteur,
            fond,
            bords: bordsRetenus.map(([g, d]) => [g / largeur, (d + 1) / largeur]),
        };
    }
    return null;
}
/** Les icônes de manigance imprimées, dans l'ordre où le scan les aligne. Boost n'en fait pas partie : il est hors de la boîte de texte. */
const ICONES_MANIGANCE = [
    ['Acceleration', 'acceleration'],
    ['Crisis', 'crisis'],
    ['Hazard', 'hazard'],
    ['Amplify', 'amplify'],
];
/** Les icônes d'une carte d'après son `desc` : un champ absent, vide ou « 0 » ne s'imprime pas. */
export function iconesImprimees(desc) {
    if (!desc)
        return [];
    return ICONES_MANIGANCE.filter(([champ]) => {
        const valeur = String(desc[champ] ?? '').trim();
        return valeur !== '' && valeur !== '0';
    }).map(([, jeton]) => jeton);
}
/** Glyphes de la police ChampionsIcons (relevés sur public/fonts/ChampionsIcons.ttf). */
export const GLYPHES = {
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
 * Le texte POSÉ sur la carte, mis en page comme le texte imprimé (25/10/2026, demande de l'utilisateur : « respecte la
 * typo, la taille et l'emplacement ») : un paragraphe par ligne du texte, espacés comme sur la carte ; une ligne
 * entièrement en italique (citation, avec son attribution « —Nom » éventuelle) en plus petit ; une ligne entre
 * `<center>…</center>` centrée (« Ordre d'activation N » des méchants de The Vault, comme « Activation Order N »).
 * L'encadré sous la carte (Board.tsx) garde `texteEnHtml`.
 */
export function texteEnParagraphes(texte) {
    return texte
        .split('\n')
        .map((ligne) => {
        const brute = ligne.trim();
        const centre = /^<center>([\s\S]*)<\/center>$/.exec(brute);
        const contenu = centre ? centre[1] : brute;
        const citation = /^<i>[\s\S]*<\/i>(\s*[—–-][^<]*)?$/.test(contenu) && !/<\/i>[\s\S]*<i>/.test(contenu);
        const classes = ['tp-par', centre ? 'tp-centre' : '', citation ? 'tp-citation' : ''].filter(Boolean).join(' ');
        return `<div class="${classes}">${texteEnHtml(contenu)}</div>`;
    })
        .join('');
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
/**
 * Marge ajoutée au cache d'une carte PAYSAGE : son texte déborde parfois un peu
 * de la boîte, sur l'illustration (côté opposé au cadre) et vers le bas
 * (constaté sur hs004a, Rats and More Rats 1A, 09/10/2026). Avec les pixels de
 * la carte (largeur x hauteur, RGBA), une ligne ne s'élargit pas quand la bande
 * ajoutée contient du blanc franc : c'est un badge (« +1 par joueur » de hs004b).
 */
export function elargirPaysage(zone, cote, image) {
    const [avantX, apresX, bas] = cote === 'gauche' ? [0.006, 0.012, 0.012] : [0.012, 0.006, 0.012];
    const x0 = Math.max(0, zone.x0 - avantX);
    const x1 = Math.min(1, zone.x1 + apresX);
    const y1 = Math.min(1, zone.y1 + bas);
    const n = zone.bords.length;
    const blancDans = (i, a, b) => {
        if (!image)
            return false;
        const y = Math.floor((zone.y0 + ((zone.y1 - zone.y0) * (i + 0.5)) / n) * image.hauteur);
        let blancs = 0;
        for (let x = Math.floor(a * image.largeur); x < Math.ceil(b * image.largeur); x += 1) {
            const k = (y * image.largeur + x) * 4;
            if (Math.min(image.pixels[k], image.pixels[k + 1], image.pixels[k + 2]) > 230)
                blancs += 1;
        }
        return blancs >= 2;
    };
    // Une ligne creusée autour d'un badge (encoche) garde son bord : seules les
    // lignes à pleine largeur s'élargissent, et pas sur un badge blanc.
    const bords = zone.bords.map(([g, d], i) => {
        const gauche = g <= zone.x0 + 0.005 && !blancDans(i, Math.max(0, g - avantX), g) ? Math.max(0, g - avantX) : g;
        const droite = d >= zone.x1 - 0.005 && !blancDans(i, d, Math.min(1, d + apresX)) ? Math.min(1, d + apresX) : d;
        return [gauche, droite];
    });
    // La marge du bas prolonge la dernière ligne, au prorata de la hauteur ajoutée.
    const ajout = Math.round((n * bas) / Math.max(1e-6, zone.y1 - zone.y0));
    const derniere = bords[bords.length - 1];
    for (let i = 0; i < ajout && derniere; i += 1)
        bords.push([derniere[0], derniere[1]]);
    return { ...zone, x0, x1, y1, bords };
}

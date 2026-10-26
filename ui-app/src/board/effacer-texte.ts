// effacer-texte.ts — efface les LETTRES du texte imprimé d'un scan, en gardant tout le reste de l'image (25/10/2026).
//
// Le voile français posait une boîte d'une seule couleur sur la zone de texte : elle ne ressemblait jamais au vrai cadre
// (rayons, dégradés, liserés, illustration qui mord dessus) et chaque bord mal mesuré se voyait. On n'efface plus que
// l'encre des lettres anglaises, remplacée par le fond qui l'entoure :
//  1. le fond sans lettres = une FERMETURE (maximum puis minimum glissants) plus large qu'un trait de lettre : le sombre
//     fin disparaît, les dégradés et les grandes formes restent ;
//  2. l'encre = ce qui est nettement plus sombre que ce fond ; on n'en garde que les PETITES taches (taille d'une lettre).
//     Les grandes (illustration qui mord sur le cadre, liserés, filet du Boost) ne sont pas touchées ;
//  3. le halo anti-crénelé des lettres rejoint le masque (hystérésis), puis le masque est rempli par diffusion depuis
//     ses voisins, ce qui garde le grain du fond.
// Fond sombre (texte clair) : tout est inversé (ouverture, encre plus claire que le fond).

export type OptionsEffacement = {
  /** Dimensions de la CARTE entière, en pixels du tampon : les seuils sont relatifs à la carte, pas à la zone. */
  largeurCarte: number
  hauteurCarte: number
  /** Texte clair sur fond sombre. */
  sombre?: boolean
  /** Bande du bas (fraction de la HAUTEUR DE LA CARTE) laissée intacte : les icônes de manigance ou de conséquence
      imprimées sous le texte y restent telles quelles, au lieu d'être à moitié effacées puis redessinées. */
  reserveBas?: number
  /** Bandes du haut et du bas (pixels de la région) ajoutées autour de la zone détectée : une tache qui y tient tout
      entière n'appartient pas au texte (ligne du type « RESOURCE » au-dessus du cadre, bandeau du bas) et reste. */
  margeHaut?: number
  margeBas?: number
  /** Idem à gauche et à droite (pointillés et liserés du cadre). */
  margeCote?: number
}

/** Maximum (ou minimum) glissant d'un canal, ligne par ligne puis colonne par colonne. */
function filtreGlissant(source: Float32Array, largeur: number, hauteur: number, rayon: number, maximum: boolean): Float32Array {
  const temporaire = new Float32Array(source.length)
  const sortie = new Float32Array(source.length)
  const passe = (entree: Float32Array, resultat: Float32Array, pas: number, longueur: number, lignes: number, saut: number) => {
    for (let k = 0; k < lignes; k += 1) {
      const base = k * saut
      for (let t = 0; t < longueur; t += 1) {
        const debut = t - rayon < 0 ? 0 : t - rayon
        const fin = t + rayon >= longueur ? longueur - 1 : t + rayon
        let v = entree[base + debut * pas]
        for (let u = debut + 1; u <= fin; u += 1) {
          const w = entree[base + u * pas]
          if (maximum ? w > v : w < v) v = w
        }
        resultat[base + t * pas] = v
      }
    }
  }
  passe(source, temporaire, 1, largeur, hauteur, largeur)
  passe(temporaire, sortie, largeur, hauteur, largeur, 1)
  return sortie
}

/** Le masque grossi d'un pixel (voisinage 3×3), restreint à `permis` s'il est donné. */
function dilater(masque: Uint8Array, largeur: number, hauteur: number, permis?: Uint8Array): Uint8Array {
  const sortie = new Uint8Array(masque)
  for (let y = 0; y < hauteur; y += 1) {
    for (let x = 0; x < largeur; x += 1) {
      const i = y * largeur + x
      if (masque[i] || (permis && !permis[i])) continue
      let voisin = false
      for (let dy = -1; dy <= 1 && !voisin; dy += 1) {
        for (let dx = -1; dx <= 1; dx += 1) {
          const ny = y + dy
          const nx = x + dx
          if (ny >= 0 && ny < hauteur && nx >= 0 && nx < largeur && masque[ny * largeur + nx]) {
            voisin = true
            break
          }
        }
      }
      if (voisin) sortie[i] = 1
    }
  }
  return sortie
}

/** Le rectangle occupé par le texte effacé, en fractions de la région : le français se pose au même endroit. */
export type CadreDuTexte = {
  x0: number
  y0: number
  x1: number
  y1: number
  /** Jusqu'où le fond du texte se prolonge sous la dernière ligne (avant un bandeau, une icône, le bas du cadre). */
  bas: number
  /** Nombre de lignes du texte effacé : une seule ligne courte ne dit rien de la largeur de la colonne. */
  lignes: number
  /** Interligne de l'anglais imprimé (médiane de l'écart entre deux lignes), en fraction de la HAUTEUR DE LA CARTE ; 0 si inconnu. */
  interligne: number
  /** Bord droit du fond libre, par bandes horizontales égales de la région (BANDES_DROITE, fractions de sa largeur) : là
      où une illustration entre dans le cadre de texte. Le français s'y arrête, comme l'anglais. */
  droite: number[]
  /** Où COMMENCENT les lignes de l'anglais, par les mêmes bandes (fractions de la largeur de la région) : un cadre qui penche
      (le bord noir à gauche s'écarte vers le bas) fait commencer les lignes du haut plus à droite. Le français les suit, sans
      quoi ses premières lettres se perdent sur le bord noir. Jamais en deçà de `x0`. */
  gauche: number[]
  /** Bandes (fractions de la hauteur de la région) des icônes imprimées entre deux paragraphes, et la part des lignes
      de texte qui les précèdent. */
  entre: { y0: number; y1: number; avant: number }[]
}

/**
 * Efface les lettres d'une région RGBA (modifiée sur place). Les pixels hors lettres restent identiques au scan : une
 * région un peu trop grande ne se voit donc pas. Rend le rectangle des lettres effacées (null : aucune).
 */
export function effacerTexte(rgba: Uint8ClampedArray, largeur: number, hauteur: number, options: OptionsEffacement): CadreDuTexte | null {
  const n = largeur * hauteur
  if (n === 0) return null
  const sombre = options.sombre === true
  const rayon = Math.max(3, Math.round(options.largeurCarte * 0.013))
  const canaux = [0, 1, 2].map((c) => {
    const canal = new Float32Array(n)
    for (let i = 0; i < n; i += 1) canal[i] = rgba[i * 4 + c]
    // Fermeture (texte sombre) ou ouverture (texte clair).
    return filtreGlissant(filtreGlissant(canal, largeur, hauteur, rayon, !sombre), largeur, hauteur, rayon, sombre)
  })
  const ecart = new Float32Array(n)
  for (let i = 0; i < n; i += 1) {
    const lumiere = (rgba[i * 4] + rgba[i * 4 + 1] + rgba[i * 4 + 2]) / 3
    const fond = (canaux[0][i] + canaux[1][i] + canaux[2][i]) / 3
    ecart[i] = sombre ? lumiere - fond : fond - lumiere
  }
  const encre = new Uint8Array(n)
  for (let i = 0; i < n; i += 1) encre[i] = ecart[i] > 45 ? 1 : 0
  // Aplats sombres : ce qui reste sombre APRÈS la fermeture est plus large qu'un trait de lettre (intérieur d'une icône,
  // illustration, bandeau). Une tache d'encre qui en touche un en fait partie : elle n'est jamais une lettre.
  const aplat = new Uint8Array(n)
  if (!sombre) for (let i = 0; i < n; i += 1) aplat[i] = (canaux[0][i] + canaux[1][i] + canaux[2][i]) / 3 < 110 ? 1 : 0
  const presAplat = dilater(dilater(aplat, largeur, hauteur), largeur, hauteur)
  const toucheUnAplat = (pixels: readonly number[]) => pixels.some((i) => presAplat[i])

  // Taches d'encre : seules les petites (une lettre, un signe) sont du texte.
  const hauteurMax = options.hauteurCarte * 0.06
  const largeurMax = options.largeurCarte * 0.25
  // Un filet (séparateur du Boost) est fin et long : le français redessine le sien à sa place (<hr />).
  const epaisseurFilet = options.hauteurCarte * 0.006
  // Lettres retenues pour situer le texte (pas les points de trame ni les éclats du cadre : trop petits).
  const hauteurMin = options.hauteurCarte * 0.008
  const lettres: Lettre[] = []
  const candidates: { pixels: number[]; xMin: number; xMax: number; yMin: number; yMax: number; collee: boolean; bande: boolean }[] = []
  // Taches trop grandes pour une lettre : souvent l'illustration, parfois une lettre collée à un trait du dessin.
  const rejetees: { pixels: number[]; xMin: number; xMax: number; yMin: number; yMax: number }[] = []
  const texte = new Uint8Array(n)
  const vu = new Uint8Array(n)
  const pile: number[] = []
  const tache: number[] = []
  type Tache = { pixels: number[]; xMin: number; xMax: number; yMin: number; yMax: number }
  const taches: Tache[] = []
  const limiteBas = options.reserveBas ? hauteur - Math.round(options.reserveBas * options.hauteurCarte) : hauteur
  for (let depart = 0; depart < n; depart += 1) {
    if (!encre[depart] || vu[depart]) continue
    vu[depart] = 1
    pile.push(depart)
    tache.length = 0
    let xMin = largeur
    let xMax = -1
    let yMin = hauteur
    let yMax = -1
    while (pile.length) {
      const i = pile.pop()!
      tache.push(i)
      const x = i % largeur
      const y = (i - x) / largeur
      if (x < xMin) xMin = x
      if (x > xMax) xMax = x
      if (y < yMin) yMin = y
      if (y > yMax) yMax = y
      for (let dy = -1; dy <= 1; dy += 1) {
        for (let dx = -1; dx <= 1; dx += 1) {
          const ny = y + dy
          const nx = x + dx
          if (ny < 0 || ny >= hauteur || nx < 0 || nx >= largeur) continue
          const j = ny * largeur + nx
          if (encre[j] && !vu[j]) {
            vu[j] = 1
            pile.push(j)
          }
        }
      }
    }
    taches.push({ pixels: tache.slice(), xMin, xMax, yMin, yMax })
  }
  // Les icônes imprimées sous le texte (bande du bas) sont plus hautes qu'une lettre ; leurs morceaux plus petits (le
  // trait sous la croix d'une conséquence...) sont à la même place. On les laisse toutes.
  // Une icône (accélération, crise, conséquence...) est plus haute qu'une lettre, accent et jambage compris : on la garde
  // partout ; dans la bande du bas annoncée par l'appelant, même une icône un peu plus petite.
  // Une icône est seule sur sa ligne ; une lettre haute (« p », « l » d'un mot, avec son jambage) a des voisines à la
  // même hauteur, à moins de deux hauteurs de lettre.
  const dansUnMot = (t: Tache) => {
    const h = t.yMax - t.yMin + 1
    let voisines = 0
    for (const v of taches) {
      if (v === t || v.yMax - v.yMin + 1 > h * 1.2 || v.yMax - v.yMin + 1 < h * 0.3) continue
      // Une lettre est faite de traits fins ; les morceaux d'une icône (la croix, la carte) sont pleins.
      if (v.pixels.length > 0.5 * (v.xMax - v.xMin + 1) * (v.yMax - v.yMin + 1)) continue
      const commun = Math.min(v.yMax, t.yMax) - Math.max(v.yMin, t.yMin)
      const ecart = Math.max(v.xMin - t.xMax, t.xMin - v.xMax)
      // Même ligne : bas aligné (ligne de base), haut aligné, ou haut à mi-hauteur (« p » à jambage à côté d'un « a »).
      if (commun > (v.yMax - v.yMin) * 0.5 && ecart < h * 1.5 && (Math.abs(v.yMax - t.yMax) <= Math.max(2, h * 0.12) || Math.abs(v.yMin - t.yMin) <= Math.max(2, h * 0.12) || Math.abs(v.yMin - (t.yMin + t.yMax) / 2) <= Math.max(2, h * 0.2))) voisines += 1
      if (voisines >= 2) return true
    }
    return false
  }
  const icones = taches.filter(
    (t) =>
      t.yMax - t.yMin > options.hauteurCarte * (t.yMax >= limiteBas ? 0.026 : 0.034) &&
      // Hors de la bande du bas, une icône est pleine ; un mot imprimé de biais (lettres collées : « HELMET. »), non.
      (t.yMax >= limiteBas || t.pixels.length >= 0.4 * (t.xMax - t.xMin + 1) * (t.yMax - t.yMin + 1) || toucheUnAplat(t.pixels)) &&
      t.yMax - t.yMin < options.hauteurCarte * 0.08 &&
      t.xMax - t.xMin < options.largeurCarte * 0.15 &&
      // Une icône est trapue ; un liseré ou un trait du cadre est fin et long.
      t.xMax - t.xMin + 1 >= 0.45 * (t.yMax - t.yMin + 1) &&
      t.xMin > 0 &&
      t.xMax < largeur - 1 &&
      t.yMax < hauteur - 1 &&
      !dansUnMot(t)
  )
  // Une icône pleine n'est vue que par morceaux (son intérieur noir, plus large qu'un trait, n'est pas de l'« encre ») :
  // tout ce qui tient dans sa zone, élargie d'une hauteur sur les côtés et de 0,7 hauteur dessous (le texte est au-dessus), en fait
  // partie et n'est jamais effacé.
  const zonesIcones = icones.map((i) => {
    const demi = (i.yMax - i.yMin) / 2
    const pres = options.largeurCarte * 0.015
    return { x0: i.xMin - 2 * demi, x1: i.xMax + 2 * demi, y0: i.yMin - pres, y1: i.yMax + Math.max(pres, 1.4 * demi) }
  })
  const dansUneIcone = (t: Tache) => zonesIcones.some((z) => t.xMin >= z.x0 && t.xMax <= z.x1 && t.yMin >= z.y0 && t.yMax <= z.y1)
  // Le bord HAUT du cadre de texte, quand la zone le déborde : une rangée presque entièrement sombre dans le haut de
  // la région. Ce qui est au-dessus (ligne du type « RESOURCE », titre) n'est pas le texte de la carte.
  const sombreRangee = rangeesSombres(rgba, largeur, hauteur)
  let hautDuCadre = -1
  for (let y = 0; y < hauteur * 0.35; y += 1) if (sombreRangee[y]) hautDuCadre = y
  for (const t of taches) {
    const { xMin, xMax, yMin, yMax } = t
    if (yMax < hautDuCadre) continue
    // Une tache coupée par le bord de la région est un morceau d'illustration ou de cadre, pas une lettre (la région
    // déborde un peu de la zone de texte) : on n'y touche pas.
    const auBord = xMin === 0 || yMin === 0 || xMax === largeur - 1 || yMax === hauteur - 1
    const icone = dansUneIcone(t)
    // Touche un aplat sombre (morceau d'icône, ou lettre collée à un trait) : jamais compté pour FORMER une ligne ; effacé
    // seulement s'il tombe dans une ligne formée par d'autres lettres.
    const collee = toucheUnAplat(t.pixels)
    if (yMax < (options.margeHaut ?? 0) || yMin >= hauteur - (options.margeBas ?? 0)) continue
    // Les bandes de côté (liserés, pointillés du cadre) ne sont jamais du texte... sauf la dernière lettre d'une ligne qui y
    // déborde : elle est retenue à part (`bande`) et n'est effacée que si elle est au bout d'une ligne reconnue (26/10/2026).
    const bande = xMax < (options.margeCote ?? 0) || xMin >= largeur - (options.margeCote ?? 0)
    if (bande && (collee || yMax - yMin < hauteurMin)) continue
    // Au-dessus et au-dessous d'une lettre (une hauteur de lettre), le fond clair domine. Les creux sombres entre les
    // lettres blanches d'un bandeau (« RESOURCE ») ont le bandeau sombre autour : ce n'est pas du texte.
    {
      const marge = yMax - yMin + 1
      const partClaire = (ya: number, yb: number, xa: number, xb: number) => {
        let clairs = 0
        let tous = 0
        for (let y = Math.max(0, ya); y <= Math.min(hauteur - 1, yb); y += 1) {
          for (let x = Math.max(0, xa); x <= Math.min(largeur - 1, xb); x += 1) {
            const i = (y * largeur + x) * 4
            const l = (rgba[i] + rgba[i + 1] + rgba[i + 2]) / 3
            if (sombre ? l < 110 : l > 150) clairs += 1
            tous += 1
          }
        }
        return tous ? clairs / tous : 1
      }
      // Au-dessus ET au-dessous, séparément (26/10/2026) : une lettre de la première ou de la dernière ligne, collée au bord
      // sombre du cadre (le trait d'un « l », d'un « I »), n'a du sombre que d'un côté ; un creux de bandeau en a des deux.
      const ecartVertical = Math.max(2, marge)
      const enHaut = partClaire(yMin - ecartVertical, yMin - 1, xMin, xMax)
      const enBas = partClaire(yMax + 1, yMax + ecartVertical, xMin, xMax)
      if (enHaut < 0.45 && enBas < 0.45) continue
      // De part et d'autre aussi : un morceau de bandeau noir (avec ses lettres blanches en creux) n'a que du sombre à côté.
      // La marge latérale ne descend pas sous une hauteur de lettre : celle d'un tiret « — » (2 px de haut, 26 de large) le
      // ferait passer pour un morceau de bandeau, et le tiret anglais restait sous le français.
      const plat = yMax - yMin <= epaisseurFilet && xMax - xMin > options.largeurCarte * 0.3
      const margeLaterale = Math.max(marge, Math.round(options.hauteurCarte * 0.012))
      if (!plat && partClaire(yMin, yMax, xMin - margeLaterale, xMax + margeLaterale) < 0.2) continue
    }
    // Un mot imprimé de biais (« HELMET. », lettres collées) forme une seule tache, plus haute qu'une lettre mais creuse.
    const motDeBiais = yMax - yMin < options.hauteurCarte * 0.075 && t.pixels.length < 0.35 * (xMax - xMin + 1) * (yMax - yMin + 1)
    const lettre = !auBord && !icone && (yMax - yMin < hauteurMax || motDeBiais) && xMax - xMin < largeurMax
    const filet = !auBord && !icone && yMax - yMin <= epaisseurFilet && xMax - xMin > options.largeurCarte * 0.3 && xMax - xMin < largeur * 0.95
    if (!lettre && !filet) {
      if (!icone) rejetees.push(t)
      continue
    }
    // Filet et mot imprimé de biais (une seule tache, hors de toute ligne) : effacés tels quels.
    if (filet || (motDeBiais && yMax - yMin >= hauteurMax)) for (const i of t.pixels) texte[i] = 1
    else candidates.push({ ...t, collee, bande })
    if (lettre && !collee && !bande && yMax - yMin >= hauteurMin) lettres.push({ x0: xMin, x1: xMax + 1, y0: yMin, y1: yMax + 1 })
  }
  // Une lettre n'est effacée que dans une LIGNE de texte (au moins trois lettres côte à côte) : les lettres d'un titre
  // imprimé à la verticale, une par rangée, restent.
  // Le texte s'arrête au-dessus des icônes.
  const cadre = cadreDesLettres(lettres, options.largeurCarte, options.hauteurCarte)
  // Couleur du fond du texte (médiane, lettres comprises : elles sont minoritaires), puis « cette zone est-elle sur ce fond ? »
  // d'après le fond sans lettres (fermeture) autour d'elle.
  const reference = [0, 1, 2].map((c) => {
    const v: number[] = []
    if (cadre) for (let y = Math.round(cadre.y0); y < cadre.y1; y += 3) for (let x = Math.round(cadre.x0); x < cadre.x1; x += 3) v.push(canaux[c][y * largeur + x])
    v.sort((a, b) => a - b)
    return v.length ? v[Math.floor(v.length / 2)] : 255
  })
  const surLeFond = (x0: number, y0: number, x1: number, y1: number, tolerance = 60): boolean => {
    let somme = 0
    let n = 0
    const pad = Math.round(options.hauteurCarte * 0.01)
    for (let y = Math.max(0, y0 - pad); y <= Math.min(hauteur - 1, y1 + pad); y += 1) {
      for (let x = Math.max(0, x0 - pad); x <= Math.min(largeur - 1, x1 + pad); x += 1) {
        const i = y * largeur + x
        somme += Math.abs(canaux[0][i] - reference[0]) + Math.abs(canaux[1][i] - reference[1]) + Math.abs(canaux[2][i] - reference[2])
        n += 1
      }
    }
    return n === 0 || somme / n < tolerance
  }
  // ... et jamais à gauche de la colonne du texte (un titre vertical collé au cadre n'en fait pas partie).
  const boites = [...boitesDesLignes(lettres, options.hauteurCarte), ...boitesDesMotsCollés(lettres, cadre, options.hauteurCarte)]
  const fins = finsDesLignes(lettres, options.hauteurCarte)
  const marge = options.hauteurCarte * 0.012
  for (const t of candidates) {
    if (cadre && t.xMax < cadre.x0 - marge) continue
    // Une petite marque (guillemet fermant, point) juste après la dernière lettre d'une ligne est de cette ligne (26/10/2026).
    const boutDeLigne = fins.some(
      (f) => t.xMin >= f.x0 && t.xMax <= f.x1 && t.yMin >= f.y0 && t.yMax <= f.y1 && t.xMax - t.xMin <= f.h * 0.9 && t.yMax - t.yMin <= f.h * 1.1
    )
    // À droite de la colonne du texte, seulement sur le fond du texte (pas sur une illustration colorée qui entre dans le
    // cadre : ses traits fins passeraient pour des lettres). Le bout d'une ligne tolère un fond plus sombre : près du bord
    // droit, les rayons du cadre assombrissent le fond autour du guillemet fermant.
    if (cadre && t.xMin > cadre.x1 + marge && !surLeFond(t.xMin, t.yMin, t.xMax, t.yMax) && !(boutDeLigne && surLeFond(t.xMin, t.yMin, t.xMax, t.yMax, 120))) continue
    // Une tache collée à un aplat (doigt, trait d'illustration) hors de la colonne du texte reste.
    if (t.collee && cadre && (t.xMin < cadre.x0 || t.xMax > cadre.x1)) continue
    // Une tache de la bande de côté n'est effacée que juste après la fin d'une ligne reconnue, ou juste avant son début.
    const dansUneLigne = t.bande
      ? boutDeLigne || boites.some((b) => t.xMin >= b.x0 && t.xMax <= b.x1 && t.yMin >= b.y0 && t.yMax <= b.y1)
      : boutDeLigne || boites.some((b) => t.xMin >= b.x0 && t.xMax <= b.x1 && t.yMin >= b.y0 && t.yMax <= b.y1)
    if (dansUneLigne) for (const i of t.pixels) texte[i] = 1
  }
  effacerLettresCollees(lettres, rejetees, encre, texte, largeur, options.hauteurCarte, options.margeCote ?? 0, surLeFond)

  // Hystérésis : le halo plus pâle des lettres rejoint le masque ; puis une marge d'un pixel.
  const faible = new Uint8Array(n)
  for (let i = 0; i < n; i += 1) faible[i] = ecart[i] > 10 ? 1 : 0
  let masque: Uint8Array = texte
  for (let k = 0; k < 3; k += 1) masque = dilater(masque, largeur, hauteur, faible)
  masque = dilater(masque, largeur, hauteur)
  // Le halo des lettres voisines ne mord jamais sur une icône.
  for (const z of zonesIcones) {
    for (let y = Math.max(0, Math.floor(z.y0)); y <= Math.min(hauteur - 1, Math.ceil(z.y1)); y += 1) {
      for (let x = Math.max(0, Math.floor(z.x0)); x <= Math.min(largeur - 1, Math.ceil(z.x1)); x += 1) {
        const i = y * largeur + x
        if (masque[i] && !texte[i]) masque[i] = 0
      }
    }
  }

  // Remplissage : départ au fond de la fermeture, puis diffusion depuis les voisins.
  const indices: number[] = []
  for (let i = 0; i < n; i += 1) if (masque[i]) indices.push(i)
  const valeurs = [0, 1, 2].map((c) => {
    const canal = new Float32Array(n)
    for (let i = 0; i < n; i += 1) canal[i] = masque[i] ? canaux[c][i] : rgba[i * 4 + c]
    return canal
  })
  for (let tour = 0; tour < 25; tour += 1) {
    for (const canal of valeurs) {
      for (const i of indices) {
        const x = i % largeur
        const haut = i >= largeur ? canal[i - largeur] : canal[i]
        const bas = i + largeur < n ? canal[i + largeur] : canal[i]
        const gauche = x > 0 ? canal[i - 1] : canal[i]
        const droite = x < largeur - 1 ? canal[i + 1] : canal[i]
        canal[i] = (haut + bas + gauche + droite) / 4
      }
    }
  }
  for (const i of indices) {
    rgba[i * 4] = valeurs[0][i]
    rgba[i * 4 + 1] = valeurs[1][i]
    rgba[i * 4 + 2] = valeurs[2][i]
  }
  if (!cadre) return null
  // Le français peut descendre jusqu'au bord bas du cadre (première rangée sombre sous le texte anglais)...
  let basDuCadre = hauteur
  for (let y = Math.ceil(cadre.y1); y < hauteur; y += 1) {
    if (sombreRangee[y]) {
      basDuCadre = y
      break
    }
  }
  // ... et s'arrête au-dessus des icônes imprimées SOUS lui.
  const dessous = icones.filter((i) => i.yMin >= cadre.y1 - 2)
  const hautIcones = dessous.length ? Math.min(...dessous.map((i) => i.yMin)) : hauteur
  return {
    x0: cadre.x0 / largeur,
    y0: cadre.y0 / hauteur,
    x1: cadre.x1 / largeur,
    y1: cadre.y1 / hauteur,
    bas: Math.min(basDuCadre, hautIcones) / hauteur,
    lignes: cadre.lignes,
    interligne: cadre.interligne / options.hauteurCarte,
    droite: bordDroitLibre(rgba, largeur, hauteur, cadre, options.hauteurCarte),
    gauche: bordGaucheDesLignes(lettres, cadre.x0, largeur, hauteur, options.hauteurCarte),
    // Icônes imprimées AU MILIEU du texte (entre la capacité et la citation) : le français saute leur hauteur.
    entre: zonesIcones
      .map((z) => {
        // L'icône entière : tous les morceaux dans sa zone (la croix, la carte...).
        const morceaux = taches.filter((t) => t.xMin >= z.x0 && t.xMax <= z.x1 && t.yMin >= z.y0 && t.yMax <= z.y1)
        return { y0: Math.min(...morceaux.map((t) => t.yMin)), y1: Math.max(...morceaux.map((t) => t.yMax)) }
      })
      .filter((i) => i.y0 > cadre.y0 && i.y1 < cadre.y1)
      .map((i) => ({
        y0: (i.y0 - 3) / hauteur,
        y1: (i.y1 + 3) / hauteur,
        // Part des lignes anglaises imprimées AU-DESSUS de l'icône : le français place la bande à la frontière de
        // paragraphes la plus proche de cette part.
        avant: cadre.basDesLignes.filter((y) => y <= i.y0).length / Math.max(1, cadre.basDesLignes.length),
      }))
      // Deux icônes côte à côte (ou deux morceaux d'une même icône) : une seule bande.
      .sort((a, b) => a.y0 - b.y0)
      .reduce<{ y0: number; y1: number; avant: number }[]>((bandes, b) => {
        const derniere = bandes[bandes.length - 1]
        if (derniere && b.y0 <= derniere.y1) derniere.y1 = Math.max(derniere.y1, b.y1)
        else bandes.push({ ...b })
        return bandes
      }, []),
  }
}

/**
 * Une lettre imprimée sur un dessin touche parfois un de ses traits : elle forme avec lui une grande tache, gardée comme
 * illustration. Au bout de chaque ligne de texte (sur la hauteur de la ligne, jusqu'à trois lettres après la dernière
 * lettre reconnue, et avant la première), l'encre de ces grandes taches est effacée elle aussi : le trait du dessin y
 * perd quelques pixels, recomblés par le remplissage, mais il ne reste plus un bout de mot anglais.
 */
function effacerLettresCollees(
  lettres: readonly Lettre[],
  rejetees: readonly { pixels: number[]; xMin: number; xMax: number; yMin: number; yMax: number }[],
  encre: Uint8Array,
  texte: Uint8Array,
  largeur: number,
  hauteurCarte: number,
  cote: number,
  surLeFond: (x0: number, y0: number, x1: number, y1: number, tolerance?: number) => boolean
): void {
  if (!rejetees.length || !lettres.length) return
  const lignes: Lettre[][] = []
  for (const l of [...lettres].sort((a, b) => a.y0 + a.y1 - b.y0 - b.y1)) {
    const milieu = (l.y0 + l.y1) / 2
    const ligne = lignes.find((g) => Math.abs((g[0].y0 + g[0].y1) / 2 - milieu) <= hauteurCarte * 0.008)
    if (ligne) ligne.push(l)
    else lignes.push([l])
  }
  const bouts: { x0: number; x1: number; y0: number; y1: number }[] = []
  for (const ligne of lignes) {
    if (ligne.length < 3) continue
    const y0 = Math.min(...ligne.map((l) => l.y0))
    const y1 = Math.max(...ligne.map((l) => l.y1))
    const portee = (y1 - y0) * 3
    const debut = Math.min(...ligne.map((l) => l.x0))
    const fin = Math.max(...ligne.map((l) => l.x1))
    // Jamais dans les bandes de côté (liserés, pointillés du cadre) ; avant la ligne, une hauteur de lettre seulement.
    // Seulement là où le fond est celui du texte : un bout de ligne qui donne sur une illustration colorée (une main)
    // n'y efface rien.
    const candidats = [
      { x0: fin, x1: Math.min(fin + portee, largeur - 1 - cote), y0, y1 },
      { x0: Math.max(debut - (y1 - y0), cote), x1: debut, y0, y1 },
    ]
    for (const b of candidats) if (b.x1 > b.x0 && surLeFond(b.x0, b.y0, b.x1, b.y1, 90)) bouts.push(b)
  }
  for (const t of rejetees) {
    if (!bouts.some((b) => t.xMax >= b.x0 && t.xMin <= b.x1 && t.yMax >= b.y0 && t.yMin <= b.y1)) continue
    for (const i of t.pixels) {
      if (!encre[i]) continue
      const x = i % largeur
      const y = (i - x) / largeur
      if (bouts.some((b) => x >= b.x0 && x <= b.x1 && y >= b.y0 && y <= b.y1)) texte[i] = 1
    }
  }
}

/**
 * Une ligne d'un seul mot en italique n'a parfois que une ou deux taches (les lettres collées) : elle n'atteint pas les trois
 * lettres d'une ligne et restait en anglais (« bestowed. » sous une citation). On la reconnaît si elle est large (au moins quatre
 * hauteurs de lettre en tout) ET dans le voisinage du bloc de texte déjà reconnu (à moins de trois hauteurs de lettre au-dessus ou
 * au-dessous, et dans ses colonnes) : une tache isolée plus loin, ou sur le dessin, n'est pas du texte.
 */
export function boitesDesMotsCollés(
  lettres: readonly Lettre[],
  cadre: Lettre | null,
  hauteurCarte: number
): Lettre[] {
  if (!cadre) return []
  const lignes: Lettre[][] = []
  for (const l of [...lettres].sort((a, b) => a.y0 + a.y1 - b.y0 - b.y1)) {
    const milieu = (l.y0 + l.y1) / 2
    const ligne = lignes.find((g) => Math.abs((g[0].y0 + g[0].y1) / 2 - milieu) <= hauteurCarte * 0.008)
    if (ligne) ligne.push(l)
    else lignes.push([l])
  }
  const boites: Lettre[] = []
  for (const ligne of lignes) {
    if (ligne.length >= 3) continue
    const x0 = Math.min(...ligne.map((l) => l.x0))
    const x1 = Math.max(...ligne.map((l) => l.x1))
    const y0 = Math.min(...ligne.map((l) => l.y0))
    const y1 = Math.max(...ligne.map((l) => l.y1))
    const h = y1 - y0
    if (x1 - x0 < 4 * h) continue
    if (ligne.length === 2 && Math.max(ligne[0].x0, ligne[1].x0) - Math.min(ligne[0].x1, ligne[1].x1) > 1.5 * h) continue
    if (x0 < cadre.x0 - h || x1 > cadre.x1 + h || y0 < cadre.y0 - 3 * h || y1 > cadre.y1 + 3 * h) continue
    boites.push({ x0: x0 - h, x1: x1 + h, y0: y0 - h * 0.6, y1: y1 + h * 0.6 })
  }
  return boites
}

/** Pour chaque ligne de texte (au moins trois lettres à la même hauteur), la place juste après sa dernière lettre : une et demie
    hauteurs de lettre, sur la hauteur de la ligne (plus un tiers). `h` : hauteur de la ligne. */
export function finsDesLignes(lettres: readonly Lettre[], hauteurCarte: number): { x0: number; x1: number; y0: number; y1: number; h: number }[] {
  const lignes: Lettre[][] = []
  for (const l of [...lettres].sort((a, b) => a.y0 + a.y1 - b.y0 - b.y1)) {
    const milieu = (l.y0 + l.y1) / 2
    const ligne = lignes.find((g) => Math.abs((g[0].y0 + g[0].y1) / 2 - milieu) <= hauteurCarte * 0.008)
    if (ligne) ligne.push(l)
    else lignes.push([l])
  }
  return lignes
    .filter((ligne) => ligne.length >= 3)
    .map((ligne) => {
      const y0 = Math.min(...ligne.map((l) => l.y0))
      const y1 = Math.max(...ligne.map((l) => l.y1))
      const h = y1 - y0
      const fin = Math.max(...ligne.map((l) => l.x1))
      return { x0: fin, x1: fin + 1.5 * h, y0: y0 - h / 3, y1: y1 + h / 3, h }
    })
}

/** Les rectangles des lignes de texte (au moins trois lettres à la même hauteur, sans trou de plus de quatre hauteurs de
    lettre), élargis d'une demi-hauteur de ligne en haut et en bas (accents, cédilles) et d'une hauteur sur les côtés. */
export function boitesDesLignes(lettres: readonly Lettre[], hauteurCarte: number): Lettre[] {
  const lignes: Lettre[][] = []
  for (const l of [...lettres].sort((a, b) => a.y0 + a.y1 - b.y0 - b.y1)) {
    const milieu = (l.y0 + l.y1) / 2
    const ligne = lignes.find((g) => Math.abs((g[0].y0 + g[0].y1) / 2 - milieu) <= hauteurCarte * 0.008)
    if (ligne) ligne.push(l)
    else lignes.push([l])
  }
  const boites: Lettre[] = []
  for (const ligne of lignes) {
    const parX = [...ligne].sort((a, b) => a.x0 - b.x0)
    const h = Math.max(...ligne.map((l) => l.y1 - l.y0))
    // Morceaux de lettres voisines (écart < quatre hauteurs : l'espace entre deux mots en italique est large).
    let morceau: Lettre[] = []
    const fermer = () => {
      if (morceau.length >= 3) {
        boites.push({
          x0: morceau[0].x0 - h,
          x1: Math.max(...morceau.map((l) => l.x1)) + h,
          y0: Math.min(...morceau.map((l) => l.y0)) - h * 0.6,
          y1: Math.max(...morceau.map((l) => l.y1)) + h * 0.6,
        })
      }
      morceau = []
    }
    for (const l of parX) {
      if (morceau.length && l.x0 - Math.max(...morceau.map((m) => m.x1)) > h * 4) fermer()
      morceau.push(l)
    }
    fermer()
  }
  return boites
}

/** Pour chaque rangée de la région : est-elle presque entièrement sombre (bord du cadre de texte, bandeau) ? */
function rangeesSombres(rgba: Uint8ClampedArray, largeur: number, hauteur: number): Uint8Array {
  const sortie = new Uint8Array(hauteur)
  const xa = Math.round(largeur * 0.1)
  const xb = Math.round(largeur * 0.9)
  for (let y = 0; y < hauteur; y += 1) {
    let sombres = 0
    for (let x = xa; x < xb; x += 1) {
      const i = (y * largeur + x) * 4
      if (rgba[i] + rgba[i + 1] + rgba[i + 2] < 300) sombres += 1
    }
    sortie[y] = sombres > (xb - xa) * 0.6 ? 1 : 0
  }
  return sortie
}

type Lettre = { x0: number; x1: number; y0: number; y1: number }

/**
 * Le rectangle du texte, en pixels de la région, tiré des lettres regroupées en LIGNES : dans une ligne, on part de la
 * lettre du milieu et on avance de proche en proche (un écart de plus d'un mot rompt la chaîne). Un éclat du liseré ou
 * de l'illustration à la même hauteur qu'une ligne reste donc hors de la ligne. Seules les lignes d'au moins trois
 * lettres comptent.
 */
export function cadreDesLettres(lettres: readonly Lettre[], largeurCarte: number, hauteurCarte: number): (Lettre & { lignes: number; interligne: number; basDesLignes: number[] }) | null {
  const triees = [...lettres].sort((a, b) => (a.y0 + a.y1) / 2 - (b.y0 + b.y1) / 2)
  const lignes: Lettre[][] = []
  for (const l of triees) {
    const milieu = (l.y0 + l.y1) / 2
    const ligne = lignes.find((g) => {
      const m = g.reduce((t, x) => t + (x.y0 + x.y1) / 2, 0) / g.length
      return Math.abs(m - milieu) <= hauteurCarte * 0.008
    })
    if (ligne) ligne.push(l)
    else lignes.push([l])
  }
  let cadre: Lettre | null = null
  let retenues = 0
  const hautsDeLigne: number[] = []
  for (const ligne of lignes) {
    if (ligne.length < 3) continue
    const parX = [...ligne].sort((a, b) => a.x0 - b.x0)
    // Un espace entre deux mots vaut environ une hauteur de lettre ; un éclat du cadre est bien plus loin.
    const hauteurs = ligne.map((l) => l.y1 - l.y0).sort((a, b) => a - b)
    const ecartMax = Math.max(largeurCarte * 0.025, hauteurs[Math.floor(hauteurs.length / 2)] * 1.3)
    const centre = Math.floor(parX.length / 2)
    let debut = centre
    let fin = centre
    let droite = parX[centre].x1
    while (fin + 1 < parX.length && parX[fin + 1].x0 - droite <= ecartMax) {
      fin += 1
      droite = Math.max(droite, parX[fin].x1)
    }
    while (debut > 0 && parX[debut].x0 - parX[debut - 1].x1 <= ecartMax) debut -= 1
    if (fin - debut + 1 < 3) continue
    const morceau = parX.slice(debut, fin + 1)
    const boite = {
      x0: morceau[0].x0,
      x1: Math.max(...morceau.map((l) => l.x1)),
      y0: Math.min(...morceau.map((l) => l.y0)),
      y1: Math.max(...morceau.map((l) => l.y1)),
    }
    retenues += 1
    hautsDeLigne.push(boite.y1)
    cadre = cadre
      ? { x0: Math.min(cadre.x0, boite.x0), x1: Math.max(cadre.x1, boite.x1), y0: Math.min(cadre.y0, boite.y0), y1: Math.max(cadre.y1, boite.y1) }
      : boite
  }
  hautsDeLigne.sort((a, b) => a - b)
  const ecarts = hautsDeLigne.slice(1).map((v, i) => v - hautsDeLigne[i]).filter((e) => e > 0).sort((a, b) => a - b)
  const interligne = ecarts.length ? ecarts[Math.floor(ecarts.length / 2)] : 0
  return cadre ? { ...cadre, lignes: retenues, interligne, basDesLignes: hautsDeLigne } : null
}

export const BANDES_DROITE = 60

/**
 * Où doit commencer le français, bande par bande, quand le bord gauche du cadre PENCHE : les départs des lignes d'anglais suivent
 * alors une droite (le bord noir s'écarte vers le bas). On ajuste cette droite sur le milieu et le départ de chaque ligne de la
 * colonne du texte, puis on la décale pour qu'aucune ligne ne commence à sa gauche (le bord lui-même). Ce n'est une pente que si
 * elle descend d'au moins 1,5 % de la largeur sur le texte, avec au moins quatre lignes, et si les départs restent à moins de 1,2 %
 * de la droite : un retrait de première ligne, une ligne en gras ou la ligne des traits (centrée) ne sont PAS une pente, et le
 * résultat est alors le même bord partout (`x0`), donc aucun décalage. Les lignes qui commencent bien plus à droite que la colonne
 * n'en font pas partie.
 */
function bordGaucheDesLignes(lettres: readonly Lettre[], x0: number, largeur: number, hauteur: number, hauteurCarte: number): number[] {
  const plat = () => Array.from({ length: BANDES_DROITE }, () => x0 / largeur)
  const groupes: Lettre[][] = []
  for (const l of [...lettres].sort((a, b) => a.y0 + a.y1 - b.y0 - b.y1)) {
    const milieu = (l.y0 + l.y1) / 2
    const groupe = groupes.find((g) => Math.abs((g[0].y0 + g[0].y1) / 2 - milieu) <= hauteurCarte * 0.008)
    if (groupe) groupe.push(l)
    else groupes.push([l])
  }
  const lignes = groupes
    .filter((g) => g.length >= 3)
    .map((g) => ({ milieu: (Math.min(...g.map((l) => l.y0)) + Math.max(...g.map((l) => l.y1))) / 2, debut: Math.min(...g.map((l) => l.x0)) }))
    .filter((l) => l.debut - x0 <= largeur * 0.08)
  if (lignes.length < 4) return plat()
  const n = lignes.length
  const moyY = lignes.reduce((t, l) => t + l.milieu, 0) / n
  const moyX = lignes.reduce((t, l) => t + l.debut, 0) / n
  const variance = lignes.reduce((t, l) => t + (l.milieu - moyY) ** 2, 0)
  if (variance === 0) return plat()
  const pente = lignes.reduce((t, l) => t + (l.milieu - moyY) * (l.debut - moyX), 0) / variance
  const ordonnee = moyX - pente * moyY
  const residus = lignes.map((l) => l.debut - (ordonnee + pente * l.milieu))
  const decalage = Math.min(...residus) // la droite passe par la ligne la plus à gauche : aucune ligne ne commence en deçà
  const haut = Math.min(...lignes.map((l) => l.milieu))
  const bas = Math.max(...lignes.map((l) => l.milieu))
  const chute = Math.abs(pente) * (bas - haut)
  if (chute < largeur * 0.015 || Math.max(...residus.map((r) => Math.abs(r - decalage))) > largeur * 0.012 + Math.abs(decalage) * 0) return plat()
  const sortie: number[] = []
  for (let b = 0; b < BANDES_DROITE; b += 1) {
    const centre = Math.min(bas, Math.max(haut, ((b + 0.5) * hauteur) / BANDES_DROITE))
    sortie.push(Math.max(x0, ordonnee + decalage + pente * centre) / largeur)
  }
  return sortie
}

/**
 * Sur la région NETTOYÉE (lettres effacées), bande par bande : depuis le milieu du texte vers la droite, la première
 * fenêtre de colonnes nettement différente du fond du texte (une main, un menton, le dessin pâle d'un cadre). Les rayons
 * et la trame du cadre, fins et épars, ne l'arrêtent pas.
 */
function bordDroitLibre(
  rgba: Uint8ClampedArray,
  largeur: number,
  hauteur: number,
  cadre: { x0: number; y0: number; x1: number; y1: number },
  hauteurCarte: number
): number[] {
  const echantillons: number[][] = [[], [], []]
  for (let y = Math.round(cadre.y0); y < cadre.y1; y += 3) {
    for (let x = Math.round(cadre.x0); x < (cadre.x0 + cadre.x1) / 2; x += 3) {
      const i = (y * largeur + x) * 4
      for (let c = 0; c < 3; c += 1) echantillons[c].push(rgba[i + c])
    }
  }
  const ref = echantillons.map((v) => (v.length ? v.sort((a, b) => a - b)[Math.floor(v.length / 2)] : 255))
  const autre = (i: number) => Math.abs(rgba[i] - ref[0]) + Math.abs(rgba[i + 1] - ref[1]) + Math.abs(rgba[i + 2] - ref[2]) > 90
  const fenetre = Math.max(6, Math.round(hauteurCarte * 0.015))
  const debut = Math.round((cadre.x0 + cadre.x1) / 2)
  const sortie: number[] = []
  for (let b = 0; b < BANDES_DROITE; b += 1) {
    const ya = Math.floor((b * hauteur) / BANDES_DROITE)
    const yb = Math.max(ya + 1, Math.floor(((b + 1) * hauteur) / BANDES_DROITE))
    let limite = largeur
    let somme = 0
    const densite: number[] = []
    for (let x = debut; x < largeur; x += 1) {
      let n = 0
      for (let y = ya; y < yb; y += 1) if (autre((y * largeur + x) * 4)) n += 1
      densite.push(n / (yb - ya))
      somme += densite[densite.length - 1]
      if (densite.length > fenetre) somme -= densite[densite.length - 1 - fenetre]
      if (densite.length >= fenetre && somme / fenetre > 0.25) {
        limite = x - fenetre + 1
        break
      }
    }
    // Seule une illustration qui entre PAR LA DROITE compte : de la limite au bord, la bande reste surtout « autre ». Un
    // dessin venu de la gauche (un menton qui s'arrête au milieu) ne rétrécit pas la colonne.
    if (limite < largeur) {
      let autres = 0
      for (let x = limite; x < largeur; x += 1) {
        let n = 0
        for (let y = ya; y < yb; y += 1) if (autre((y * largeur + x) * 4)) n += 1
        if (n / (yb - ya) > 0.15) autres += 1
      }
      if (autres < (largeur - limite) * 0.6) limite = largeur
    }
    sortie.push(limite / largeur)
  }
  return sortie
}

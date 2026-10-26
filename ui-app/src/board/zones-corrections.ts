// Corrections À LA MAIN de la zone de texte détectée sur un scan (TraductionPosee) : seuls les bords donnés remplacent ceux
// de la détection, qui garde le reste (fond, gauche/droite). Mesurées sur l'image servie (assets/pics) : première et
// dernière ligne de l'intérieur clair du cadre de texte, autour de la zone détectée.
//
// The Vault (Kajislav, 25/10/2026) : le cadre de texte de ce gabarit est INCLINÉ ; la détection prend la première ligne
// entièrement claire, sous la pente, et laissait dépasser au-dessus du voile le haut de « Activation Order N » (méchants),
// des traits (TRAITOR, LOCATION) et, sous le voile, la fin de la citation de Craven Escape.
import type { ZoneTexte } from './traduction-posee'

export type CorrectionZone = Partial<Pick<ZoneTexte, 'x0' | 'y0' | 'x1' | 'y1'>>

const MECHANT_VAULT: CorrectionZone = { y0: 0.582, y1: 0.932 }

export const ZONES_CORRECTIONS: Readonly<Record<string, CorrectionZone>> = {
  ...Object.fromEntries(Array.from({ length: 16 }, (_, i) => [`vt${String(i + 1).padStart(3, '0')}`, MECHANT_VAULT])),
  vt018: { y0: 0.579, y1: 0.932 },
  // Smasher (26/10/2026) : la dernière ligne de la citation touchait le liseré du bas du cadre.
  sz001a: { y1: 0.912 },
  sz001b: { y1: 0.912 },
  sz002: { y1: 0.912 },
  vt019: { y0: 0.584, y1: 0.921 },
  vt020: { y0: 0.502, y1: 0.925 },
  vt022: { y0: 0.583, y1: 0.932 },
  vt030: { y0: 0.573, y1: 0.932 },
  vt034: { y0: 0.573, y1: 0.932 },
  // Warriors Three (26/10/2026). wt019 Gleipnir : la détection s'arrêtait avant la dernière ligne de la citation (italique,
  // 0.90 à 0.925), qui restait en anglais sous le voile. wt018 (manigance annexe couchée) : la zone détectée mordait sur le
  // bandeau « WARRIORS THREE NEMESIS » et le chiffre de menace en bas, et sur le liseré du cadre à gauche.
  wt019: { y1: 0.916 },
  wt018: { x0: 0.476, x1: 0.962, y0: 0.25, y1: 0.852 },
  // Wasp (Hank Pym) : l'étiquette « RESOURCE » de Pym Particles dépassait coupée en deux au-dessus du voile.
  hp006: { y0: 0.7 },
  // Batman : le voile commençait sous la première ligne de Smoke Cloud (anglais visible au-dessus), était trop étroit sur Detective Work,
  // et laissait dépasser le flavor anglais de Split Decision (manigance annexe paysage).
  bm019: { y0: 0.575 },
  bm020: { x0: 0.03, y0: 0.575, x1: 0.955, y1: 0.915 },
  bm014: { y0: 0.2 },
  // Batgirl, Return of the Mask (manigance annexe couchée) : la zone détectée commençait sous le haut de la première ligne du flavor
  // (italique, 0.244 à 0.276) : le haut de ses lettres restait en anglais au-dessus du français.
  bg014: { y0: 0.238 },
  // Hepzibah, Heavy Machine Gun : le titre vertical long entre dans la zone et le français se posait en minuscule (taille lue sur la bande
  // du titre) : le bord gauche passe à droite de la bande.
  hz006: { x0: 0.135 },
  // Kill Order (annexe paysage) : le voile rayait le bas du cartouche « HEPZIBAH NEMESIS (2/5) ».
  hz013: { y1: 0.875 },
  // Le trait imprimé en gras (« SKILL. », « CONDITION. SYMBIOTE. ») est trop épais pour l'effacement : il restait en morceaux (« ONDI ION MBIO »).
  // Le voile commence sous lui : le trait anglais reste lisible tel quel, et le français suit.
  sq012: { y0: 0.645 },
  rl016: { y0: 0.52 },
  // Rachel Summers : Hound Program (annexe paysage), le voile mordait l'ornement du haut et rayait « MARVEL GIRL NEMESIS (1/5) » en bas.
  rm014: { y1: 0.9 },
}

/**
 * Cartes dont le bord gauche du cadre de texte PENCHE (le bord noir s'écarte vers le bas) : le français suit le départ des lignes
 * anglaises, bande par bande (`gauche` de effacerTexte), au lieu de commencer tout à gauche, sur le bord noir. Relevées à la main :
 * une citation en retrait ou une ligne en gras ressemblent à une pente, et la détection seule mettait le français en escalier sur
 * des cartes ordinaires (Ch'od, 26/10/2026).
 */
export const CADRES_PENCHES: ReadonlySet<string> = new Set(['sq015'])

/**
 * Zones relevées À LA MAIN, pour les cartes dont le cadre de texte n'est pas du gris clair et que la détection ne trouve pas, ou
 * trouve de travers (audit du 25/10/2026) : cadres teintés, sombres, ou chargés. Elles REMPLACENT la détection.
 * Fractions de l'IMAGE (comme la détection) ; `coin` : le haut de la zone, sur la hauteur donnée, s'arrête à `x1` (un badge mord dessus).
 */
export type ZoneManuelle = {
  x0: number
  y0: number
  x1: number
  y1: number
  fond: [number, number, number]
  coin?: { hauteur: number; x1: number }
  /** Une illustration mord sur le cadre : jusqu'à `jusqua` (fraction de la HAUTEUR de la zone), le bord gauche ou droit est celui donné. Premier palier atteint. */
  paliers?: { jusqua: number; x0?: number; x1?: number }[]
}

export const ZONES_MANUELLES: Readonly<Record<string, ZoneManuelle>> = {
  // Batman, Energy : la détection prenait un aplat gris hors du cadre (l'étiquette RESOURCE disparaissait sous le voile).
  bm023: { x0: 0.05, y0: 0.7, x1: 0.945, y1: 0.915, fond: [248, 248, 248] },
  ah007: { x0: 0.06, y0: 0.67, x1: 0.92, y1: 0.905, fond: [254, 254, 236] },
  ah012b: { x0: 0.05, y0: 0.575, x1: 0.93, y1: 0.885, fond: [254, 254, 238] },
  cd015: { x0: 0.045, y0: 0.56, x1: 0.935, y1: 0.88, fond: [52, 52, 52] },
  hs035: { x0: 0.04, y0: 0.62, x1: 0.95, y1: 0.925, fond: [250, 247, 237] },
  ma015: { x0: 0.05, y0: 0.645, x1: 0.95, y1: 0.89, fond: [233, 236, 239] },
  ma016: { x0: 0.05, y0: 0.645, x1: 0.95, y1: 0.89, fond: [233, 236, 239] },
  pu013: { x0: 0.05, y0: 0.575, x1: 0.94, y1: 0.895, fond: [251, 246, 245], coin: { hauteur: 0.17, x1: 0.77 } },
  pu090a: { x0: 0.06, y0: 0.465, x1: 0.93, y1: 0.905, fond: [253, 252, 252] },
  sk146: { x0: 0.175, y0: 0.49, x1: 0.945, y1: 0.915, fond: [226, 246, 233] },
  sk150: { x0: 0.165, y0: 0.495, x1: 0.955, y1: 0.915, fond: [226, 246, 233] },
  sk196: { x0: 0.18, y0: 0.5, x1: 0.95, y1: 0.915, fond: [224, 239, 225] },
  sk198: { x0: 0.18, y0: 0.5, x1: 0.95, y1: 0.915, fond: [224, 239, 225] },
  tk106: { x0: 0.03, y0: 0.60, x1: 0.97, y1: 0.915, fond: [237, 237, 238] },
  sr017: { x0: 0.03, y0: 0.57, x1: 0.95, y1: 0.9, fond: [241, 247, 233] },
  bt009: { x0: 0.05, y0: 0.7, x1: 0.95, y1: 0.905, fond: [252, 253, 254] },
  dd007: { x0: 0.04, y0: 0.695, x1: 0.955, y1: 0.91, fond: [253, 253, 253] },
  wd128: { x0: 0.04, y0: 0.69, x1: 0.955, y1: 0.91, fond: [244, 244, 244] },
  wd129: { x0: 0.04, y0: 0.69, x1: 0.955, y1: 0.91, fond: [244, 244, 244] },
  wd156: { x0: 0.04, y0: 0.69, x1: 0.955, y1: 0.91, fond: [242, 243, 243] },
  // Illustration qui mord sur le cadre (audit du 25/10/2026, planche de l'utilisateur) : le menton de Rhino sur tk010, une main sur
  // tk001a/tk002a, le badge « 2 » de Ms. Lion, le bouclier de Nendo, le bâton d'Onmitsu (cadre rétréci sur toute la hauteur : le décor ne gère que l'encoche du haut).
  tk010: { x0: 0.035, y0: 0.47, x1: 0.845, y1: 0.915, fond: [254, 253, 248], paliers: [{ jusqua: 0.2, x0: 0.44 }] },
  tk001a: { x0: 0.04, y0: 0.575, x1: 0.88, y1: 0.915, fond: [254, 253, 248], paliers: [{ jusqua: 0.66, x1: 0.745 }] },
  tk002a: { x0: 0.04, y0: 0.575, x1: 0.88, y1: 0.915, fond: [254, 253, 248], paliers: [{ jusqua: 0.66, x1: 0.745 }] },
  sk170b: { x0: 0.03, y0: 0.575, x1: 0.955, y1: 0.925, fond: [238, 249, 231] },
  sk171b: { x0: 0.03, y0: 0.575, x1: 0.955, y1: 0.925, fond: [238, 249, 231] },
  sk172b: { x0: 0.04, y0: 0.575, x1: 0.955, y1: 0.925, fond: [238, 249, 231] },
  sk203: { x0: 0.04, y0: 0.575, x1: 0.965, y1: 0.925, fond: [233, 249, 234] },
  cd008: { x0: 0.14, y0: 0.585, x1: 0.945, y1: 0.905, fond: [248, 253, 255] },
  gs010: { x0: 0.115, y0: 0.585, x1: 0.965, y1: 0.905, fond: [255, 255, 255] },
  jj022: { x0: 0.045, y0: 0.585, x1: 0.955, y1: 0.915, fond: [254, 254, 254] },
  lj025: { x0: 0.04, y0: 0.585, x1: 0.955, y1: 0.925, fond: [254, 254, 254], paliers: [{ jusqua: 0.16, x1: 0.74 }] },
  pu104: { x0: 0.03, y0: 0.555, x1: 0.965, y1: 0.895, fond: [253, 252, 252] },
  sc001: { x0: 0.035, y0: 0.585, x1: 0.7, y1: 0.915, fond: [254, 254, 254] },
  se010: { x0: 0.04, y0: 0.585, x1: 0.7, y1: 0.915, fond: [251, 251, 252] },
  // Cadres plus hauts que la détection ne le voyait (un trait, une citation ou un titre d'environnement restait en anglais au-dessus du voile),
  // cadres pris pour une illustration (an010), titre rogné (sv010).
  sv010: { x0: 0.075, y0: 0.705, x1: 0.95, y1: 0.915, fond: [255, 255, 255] },
  // Smasher, Sunspot, Silver Surfer, She-Hulk « Why Not » (26/10/2026) : cadres relevés sur le scan. La détection débordait sur le bandeau
  // du bas ou sur les pictogrammes (so014, sz013), sur le titre d'une manigance couchée (sz012), s'arrêtait trop haut (sv015 : « bestowed »
  // restait en anglais) ou prenait le haut du dessin pour du cadre (sv007, sv011, sz003, sz006). Les cartes de She-Hulk imprimées avec des
  // bandes adhésives manuscrites (wn001a, wn001b, wn002, wn003, wn004, wn006, wn009, wn010) passent en voile uni (VOILE_UNI).
  so014: { x0: 0.045, y0: 0.58, x1: 0.955, y1: 0.915, fond: [252, 253, 248], coin: { hauteur: 0.06, x1: 0.77 } },
  sz012: { x0: 0.47, y0: 0.275, x1: 0.94, y1: 0.83, fond: [246, 250, 249] },
  sz013: { x0: 0.035, y0: 0.595, x1: 0.95, y1: 0.915, fond: [246, 250, 249] },
  sz003: { x0: 0.045, y0: 0.585, x1: 0.955, y1: 0.915, fond: [245, 245, 244] },
  sz006: { x0: 0.09, y0: 0.585, x1: 0.955, y1: 0.915, fond: [245, 245, 245] },
  sv007: { x0: 0.04, y0: 0.595, x1: 0.955, y1: 0.915, fond: [250, 251, 252] },
  sv011: { x0: 0.05, y0: 0.58, x1: 0.95, y1: 0.915, fond: [251, 252, 252] },
  sv015: { x0: 0.2, y0: 0.495, x1: 0.955, y1: 0.915, fond: [239, 239, 239] },
  wn002: { x0: 0.045, y0: 0.575, x1: 0.955, y1: 0.905, fond: [243, 247, 249] },
  wn003: { x0: 0.045, y0: 0.575, x1: 0.955, y1: 0.905, fond: [243, 246, 248] },
  wn010: { x0: 0.06, y0: 0.6, x1: 0.955, y1: 0.885, fond: [247, 247, 247] },
  wn001a: { x0: 0.045, y0: 0.615, x1: 0.955, y1: 0.915, fond: [237, 241, 244] },
  wn001b: { x0: 0.045, y0: 0.615, x1: 0.955, y1: 0.915, fond: [237, 241, 244] },
  wn004: { x0: 0.04, y0: 0.595, x1: 0.96, y1: 0.915, fond: [241, 244, 246] },
  wn006: { x0: 0.04, y0: 0.595, x1: 0.96, y1: 0.915, fond: [241, 244, 246] },
  wn009: { x0: 0.05, y0: 0.575, x1: 0.945, y1: 0.875, fond: [245, 245, 245] },
  an010: { x0: 0.03, y0: 0.575, x1: 0.965, y1: 0.92, fond: [255, 255, 255] },
  pu015: { x0: 0.1, y0: 0.575, x1: 0.88, y1: 0.895, fond: [251, 247, 246], coin: { hauteur: 0.16, x1: 0.72 } },
  pu140: { x0: 0.105, y0: 0.18, x1: 0.93, y1: 0.925, fond: [251, 246, 243] },
  pu144: { x0: 0.105, y0: 0.18, x1: 0.93, y1: 0.925, fond: [251, 246, 243] },
  pu142: { x0: 0.105, y0: 0.18, x1: 0.93, y1: 0.925, fond: [251, 246, 243] },
  pu147: { x0: 0.1, y0: 0.19, x1: 0.93, y1: 0.91, fond: [251, 246, 243] },
  wc021: { x0: 0.04, y0: 0.57, x1: 0.96, y1: 0.915, fond: [255, 254, 249] },
  wc022: { x0: 0.04, y0: 0.57, x1: 0.96, y1: 0.915, fond: [255, 254, 249] },
  60020: { x0: 0.04, y0: 0.59, x1: 0.945, y1: 0.915, fond: [253, 251, 238], coin: { hauteur: 0.18, x1: 0.75 } },
  sn001b: { x0: 0.035, y0: 0.635, x1: 0.955, y1: 0.915, fond: [250, 250, 250] },
  // Manigance annexe paysage : le flavor anglais dépassait au-dessus du voile.
  // Power Surge 2B : la main d'Electro entre dans le cadre de texte, juste après les lignes ; la zone s'arrête avant elle.
  wd039b: { x0: 0.022, y0: 0.19, x1: 0.53, y1: 0.91, fond: [226, 246, 250] },
  hs021: { x0: 0.455, y0: 0.215, x1: 0.975, y1: 0.65, fond: [241, 234, 226] },
  // Roz, Ch'od, US Agent, Winter Soldier (26/10/2026). co002 : la citation en glyphes extraterrestres (dessinée) reste au scan, la zone s'arrête au-dessus ;
  // uw015 : le badge de coût mord sur le haut du cadre et un « X. » de la ligne de traits restait.
  co002: { x0: 0.05, y0: 0.595, x1: 0.935, y1: 0.84, fond: [251, 251, 251], coin: { hauteur: 0.16, x1: 0.755 } },
  uw015: { x0: 0.03, y0: 0.575, x1: 0.95, y1: 0.912, fond: [239, 239, 241] },
  // rz019 (Minotaur) : les pastilles SCH / ATK mordent sur le cadre à gauche dès la moitié de sa hauteur : zone rétrécie à gauche (le texte anglais commence à 0,19).
  rz019: { x0: 0.185, y0: 0.5, x1: 0.945, y1: 0.93, fond: [238, 238, 246] },
  // co005 : la ligne de traits anglaise (« SKILL. ») résiste à l'effacement, quelle que soit la zone : voile uni (VOILE_UNI) sur le cadre entier.
  co005: { x0: 0.045, y0: 0.598, x1: 0.945, y1: 0.915, fond: [240, 240, 240] },
  // sy042 (Kalyx, Starjammers Aspects) : « play, » et « play. » (début des lignes 2 et 3 du premier paragraphe) restaient en anglais sous le
  // français, quelle que soit la zone : zone relevée + voile uni (VOILE_UNI).
  sy042: { x0: 0.045, y0: 0.595, x1: 0.955, y1: 0.915, fond: [249, 254, 247] },
}

/**
 * Cartes où l'effacement des lettres échoue (texte clair sur cadre sombre à reflets, tableau imprimé dans le cadre) : on y
 * garde le voile UNI d'avant, qui couvre tout le cadre.
 */
export const VOILE_UNI: ReadonlySet<string> = new Set(['cd015', 'pu142', 'co005', 'rz001a', 'bm019', 'wn001a', 'wn001b', 'wn002', 'wn003', 'wn004', 'wn006', 'wn009', 'wn010', 'sy042'])

function zoneManuelle(m: ZoneManuelle): ZoneTexte {
  const lignes = 100
  const bords = Array.from({ length: lignes }, (_, i): [number, number] => {
    const palier = m.paliers?.find((p) => i / lignes < p.jusqua)
    return [palier?.x0 ?? m.x0, palier?.x1 ?? (m.coin && i / lignes < m.coin.hauteur ? m.coin.x1 : m.x1)]
  })
  return { x0: m.x0, y0: m.y0, x1: m.x1, y1: m.y1, fond: m.fond, bords }
}

/** La zone détectée, corrigée si une correction existe pour ce code d'image (forme rectangulaire : la pente est absorbée). */
export function corrigerZone(code: string, zone: ZoneTexte | null): ZoneTexte | null {
  const manuelle = ZONES_MANUELLES[code]
  if (manuelle) return zoneManuelle(manuelle)
  const correction = ZONES_CORRECTIONS[code]
  if (!zone || !correction) return zone
  const corrigee = { ...zone, ...correction }
  return { ...corrigee, bords: [[corrigee.x0, corrigee.x1]] }
}

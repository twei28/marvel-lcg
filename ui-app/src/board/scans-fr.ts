// scans-fr.ts — scans de cartes en francais.
//
// Le pack d'images OCTGN FR est extrait par tools/importer_scans_fr.py sous
// assets/pics-fr, avec un prefixe « fr_ » dans le NOM DU FICHIER. C'est ce
// prefixe, et non une route ni un en-tete, qui distingue les deux collections :
// le serveur sert les deux dossiers sans rien savoir des langues, et les caches
// (serveur comme navigateur) ne peuvent pas les confondre, y compris en
// multijoueur avec deux joueurs regles differemment.
//
// Ce module est le SEUL endroit ou la regle est ecrite. scanUrl() l'appelle.
import { CODES_SCAN_FR } from './scans-fr-liste'
import { dosPicId, estDosGenerique } from './dos-cartes'
import { resoudreLangue } from './langue-resolution'

export const CLE_SCANS_FR = 'marvel-board-scans-fr'
export const PREFIXE_FR = 'fr_'

/** Sans reglage : actif quand le jeu est en FRANCAIS (la langue se resout par langue-resolution.ts : choix dans le jeu > cookie du
    site > navigateur > francais, 26/10/2026) ; en anglais, des cartes francaises sous une interface anglaise se liraient comme un
    bug. Un reglage explicite (« on » / « off », pose par la bascule de langue ou le menu Options) gagne toujours. */
export function scansFrActifs(): boolean {
  let reglage: string | null = null
  try {
    reglage = window.localStorage.getItem(CLE_SCANS_FR)
  } catch {
    /* stockage bloque : on suit la langue */
  }
  if (reglage === 'off') return false
  if (reglage === 'on') return true
  let stockage = ''
  try {
    stockage = window.localStorage.getItem('marvel-langue') || ''
  } catch {
    /* idem */
  }
  let cookie = ''
  try {
    cookie = document.cookie
  } catch {
    /* cookies bloques */
  }
  return resoudreLangue({ stockage, cookie, navigateur: typeof navigator === 'undefined' ? null : navigator }) === 'fr'
}

/** Les scans francais deposes a la main dans assets/pics-fr, hors archive
    OCTGN : les trois cartes d'etat (12/09/2026, `fr_tough.webp`...). La liste
    generee ne les connait pas, elle ne lit que les codes des archives. */
export const SCANS_FR_MAISON: ReadonlySet<string> = new Set(['tough', 'stunned', 'confused'])

/** Les cartes fan-made livrees avec un scan francais de leur auteur (Destiny de Merlin, FR Release 1.2 ; Beast de Proust, 02/11/2026) : `fr_dy*.jpg`
    est depose a la main dans assets/pics-fr. La liste generee ne les connait pas ; sans ce jeu, le voile FR se poserait sur l'image. */
export const SCANS_FR_FANMADE: ReadonlySet<string> = new Set([
  'dy001a', 'dy001b', 'dy002', 'dy003', 'dy004', 'dy005', 'dy006', 'dy007', 'dy008',
  'dy009', 'dy010', 'dy011', 'dy012', 'dy013', 'dy014', 'dy015', 'dy016',
  // Beast de Proust (scans FR seuls, ni EN ni dos, 02/11/2026) : `fr_bs*.jpg` deposes a la main dans assets/pics-fr.
  'bs001a', 'bs001b', 'bs002', 'bs003', 'bs004', 'bs005', 'bs006', 'bs007', 'bs008',
  'bs009', 'bs010', 'bs011', 'bs012', 'bs013', 'bs014', 'bs015', 'bs016', 'bs017',
  // Mystique de Merlin (Release FR 1.1.1, 02/11/2026) : `fr_my*.jpg` deposes a la main dans assets/pics-fr (les 23 faces).
  'my001a', 'my001b', 'my002', 'my003a', 'my003b', 'my004a', 'my004b', 'my005a', 'my005b', 'my006', 'my007', 'my008',
  'my009', 'my010', 'my011', 'my012', 'my013', 'my014', 'my015', 'my016', 'my017', 'my018', 'my019',
  // Blade de Rainy (04/11/2026, scans remplaces le 08/11/2026 par une version sans filigrane) : `fr_bl*.jpg`
  // depose a la main dans assets/pics-fr, les 17 cartes du pack.
  'bl001a', 'bl001b', 'bl002', 'bl003', 'bl004', 'bl005', 'bl006', 'bl007', 'bl008', 'bl009', 'bl010', 'bl011',
  'bl012', 'bl013', 'bl014', 'bl015', 'bl016', 'bl017',
  // Dazzler de Lord Havok (08/11/2026) : `fr_dz*.jpg` depose a la main dans assets/pics-fr. Couvre l'identite, les
  // 15 cartes du deck signature, Concert en Direct (ses deux faces), l'obligation et le set nemesis (Klaw) —
  // SAUF dz018 et dz024-dz038 (cartes bonus sans scan FR dans le depot de l'auteur : elles gardent le voile).
  'dz001a', 'dz001b', 'dz002', 'dz003', 'dz004', 'dz005', 'dz006', 'dz007', 'dz008', 'dz009', 'dz010',
  'dz011', 'dz012', 'dz013', 'dz014', 'dz015', 'dz016', 'dz017a', 'dz017b', 'dz019', 'dz020', 'dz021',
  'dz022', 'dz023',
  // Moon Knight de DesignHacker (09/11/2026) : `fr_mk*.jpg` depose a la main dans assets/pics-fr. Couvre les 5 faces d'identite,
  // les 10 cartes du deck signature, l'obligation et le set nemesis (Bushman) : les 20 cartes du depot de l'auteur.
  // Les cartes bonus mk017-mk024 n'ont pas de scan FR : elles gardent le voile.
  'mk001a', 'mk001b', 'mk001c', 'mk001d', 'mk001e', 'mk002', 'mk003', 'mk004', 'mk005', 'mk006', 'mk007', 'mk008',
  'mk009', 'mk010', 'mk011', 'mk012', 'mk013', 'mk014', 'mk015', 'mk016',
  // La ville ne dort jamais (campagne MC×DC 2026, Punisher) : scans FR de l'equipe (zip du 13/11/2026), `fr_pu*.jpg` poses par
  // .planning/mcdc-punisher/poser-scans-fr.py. 155 cartes, cartes de campagne (pu140-pu151) et de defi (pu279-pu282) comprises ; les seconds
  // exemplaires partagent le scan de l'original. The City (pu005) et Never Sleeps (pu006) ont leurs illustrations recollees
  // (panorama-city-fr.py). SANS scan FR (voile garde) : pu146 (allie Punisher, l'image 6138 n'est pas associee), Hawkeye pu283 et Resistance pu284b/pu285b.
  'pu001a', 'pu001b', 'pu002a', 'pu002b', 'pu003a', 'pu003b', 'pu004', 'pu005', 'pu006', 'pu007', 'pu008', 'pu009',
  'pu010', 'pu011', 'pu012', 'pu013', 'pu014', 'pu015', 'pu016', 'pu017', 'pu018', 'pu020', 'pu021', 'pu022',
  'pu023', 'pu024', 'pu025', 'pu026', 'pu027', 'pu028', 'pu030', 'pu031', 'pu032', 'pu033', 'pu034', 'pu035',
  'pu036', 'pu037', 'pu038', 'pu039', 'pu040', 'pu041', 'pu042', 'pu043', 'pu044', 'pu045', 'pu046', 'pu047',
  'pu048a', 'pu048b', 'pu049a', 'pu049b', 'pu050a', 'pu050b', 'pu051a', 'pu051b', 'pu052a', 'pu052b', 'pu053a', 'pu053b',
  'pu054a', 'pu054b', 'pu055a', 'pu055b', 'pu056a', 'pu056b', 'pu057a', 'pu057b', 'pu058', 'pu059', 'pu060', 'pu063',
  'pu064', 'pu065', 'pu066', 'pu068', 'pu070', 'pu071a', 'pu071b', 'pu072a', 'pu072b', 'pu073', 'pu074', 'pu075',
  'pu076', 'pu077', 'pu078', 'pu079', 'pu080', 'pu082', 'pu084', 'pu086a', 'pu086b', 'pu087a', 'pu087b', 'pu088a',
  'pu088b', 'pu089a', 'pu089b', 'pu090a', 'pu090b', 'pu091a', 'pu091b', 'pu092', 'pu093', 'pu094', 'pu095', 'pu096',
  'pu097', 'pu098', 'pu099', 'pu100', 'pu102', 'pu104', 'pu105', 'pu106a', 'pu106b', 'pu107', 'pu108', 'pu109',
  'pu110', 'pu111', 'pu113', 'pu114', 'pu115', 'pu116', 'pu117', 'pu118', 'pu119', 'pu120', 'pu121', 'pu123',
  'pu125', 'pu126', 'pu127', 'pu128', 'pu129', 'pu130', 'pu131', 'pu139', 'pu140', 'pu141', 'pu142', 'pu143',
  'pu144', 'pu145', 'pu147', 'pu148', 'pu149a', 'pu149b', 'pu151', 'pu279', 'pu280', 'pu281', 'pu282',
])

/** Les cartes dont le SEUL scan est francais (aucun scan anglais n'existe : Beast de Proust, `bs*`) : en anglais on voile le scan francais et
    on pose le texte anglais dessus (textes-en-scan-fr.ts), l'inverse de la traduction habituelle. Leur `assets/pics/<id>.jpg` est ce meme scan. */
export const SCANS_FR_SEULS: ReadonlySet<string> = new Set([
  'bs001a', 'bs001b', 'bs002', 'bs003', 'bs004', 'bs005', 'bs006', 'bs007', 'bs008',
  'bs009', 'bs010', 'bs011', 'bs012', 'bs013', 'bs014', 'bs015', 'bs016', 'bs017',
  // Mystique : le texte du scan EN beta 4.2 est PERIME par la Release FR 1.1.1 (le FR prime) pour ces faces, ou n'existe pas (my019) : on montre le scan FR voile par l'anglais.
  'my005a', 'my005b', 'my007', 'my012', 'my013', 'my018', 'my019',
])

/** Les cartes fan-made dont le scan est DEJA imprime en francais par son auteur (pack Superior Iron Man de Merlin, `si001a`...`si017`,
    audit des voiles du 25/10/2026) : poser une traduction dessus ferait doublon avec l'image. Aucun fichier `fr_` n'existe pour elles. */
export function scanDejaFrancais(code: string): boolean {
  return /^si\d{3}[ab]?$/.test(code)
}

/** La liste generee fait foi : elle ne contient que des fichiers reellement
    extraits, donc jamais un art alternatif ni un dos generique. */
export function aScanFr(picId: string): boolean {
  return CODES_SCAN_FR.has(picId) || SCANS_FR_MAISON.has(picId) || SCANS_FR_FANMADE.has(picId)
}

/** L'url d'un scan a montrer dans un petit JETON (rond, fantome de glisser). Les scans francais OFFICIELS portent un filigrane en losange
    qui se voit dans un petit rond : on retire leur prefixe `fr_` pour montrer l'illustration anglaise. Les scans francais FAN-MADE
    (SCANS_FR_FANMADE) n'ont pas de filigrane et sont le seul visage francais de la carte : on les garde (08/11/2026). */
export function urlDeJeton(url: string): string {
  return url.replace(/(\/(?:scan|vignette)\/)fr_([^/.?]+)/, (tout, voie: string, id: string) =>
    SCANS_FR_FANMADE.has(id) ? tout : voie + id
  )
}

/** Nom de fichier a demander au serveur pour cette carte. */
export function picIdFr(picId: string): string {
  // Les dos génériques suivent le choix « Dos de cartes » (dos-cartes.ts).
  if (estDosGenerique(picId)) return dosPicId(picId)
  if (!scansFrActifs()) return picId
  return aScanFr(picId) ? PREFIXE_FR + picId : picId
}

/** Aligne les scans sur la langue de l'interface. Appele par la bascule 🌐
    (langue.ts) : passer en anglais sans changer les images laissait le plateau
    en francais, ce qui se lisait comme un bug.

    L'option « Scans en francais » du menu Options reste maitresse APRES coup :
    un joueur qui veut l'interface en anglais et les scans en francais n'a qu'a
    la rallumer, seule la bascule de langue realigne. */
export function alignerScansSurLangue(langue: 'fr' | 'en'): void {
  try {
    window.localStorage.setItem(CLE_SCANS_FR, langue === 'fr' ? 'on' : 'off')
  } catch {
    /* preference non critique : la bascule de langue reste utile */
  }
}

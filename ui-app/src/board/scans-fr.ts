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

export const CLE_SCANS_FR = 'marvel-board-scans-fr'
export const PREFIXE_FR = 'fr_'

/** Actif par DEFAUT : le jeu est joue en francais. Seul « off » coupe. */
export function scansFrActifs(): boolean {
  try {
    return window.localStorage.getItem(CLE_SCANS_FR) !== 'off'
  } catch {
    return true
  }
}

/** Les scans francais deposes a la main dans assets/pics-fr, hors archive
    OCTGN : les trois cartes d'etat (12/09/2026, `fr_tough.webp`...). La liste
    generee ne les connait pas, elle ne lit que les codes des archives. */
export const SCANS_FR_MAISON: ReadonlySet<string> = new Set(['tough', 'stunned', 'confused'])

/** La liste generee fait foi : elle ne contient que des fichiers reellement
    extraits, donc jamais un art alternatif ni un dos generique. */
export function aScanFr(picId: string): boolean {
  return CODES_SCAN_FR.has(picId) || SCANS_FR_MAISON.has(picId)
}

/** Nom de fichier a demander au serveur pour cette carte. */
export function picIdFr(picId: string): string {
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

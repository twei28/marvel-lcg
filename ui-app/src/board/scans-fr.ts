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

/** La liste generee fait foi : elle ne contient que des fichiers reellement
    extraits, donc jamais un art alternatif ni un dos generique. */
export function aScanFr(picId: string): boolean {
  return CODES_SCAN_FR.has(picId)
}

/** Nom de fichier a demander au serveur pour cette carte. */
export function picIdFr(picId: string): string {
  if (!scansFrActifs()) return picId
  return aScanFr(picId) ? PREFIXE_FR + picId : picId
}

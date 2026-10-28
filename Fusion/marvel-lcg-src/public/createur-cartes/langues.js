// Les deux langues du createur (FR / EN) : valeurs par defaut des lignes de texte, traits, libelles de type.
// `donnees/traits-fr.json` vient de `ui-app/src/board/traits-fr.ts` (traits anglais en majuscules -> traits francais officiels).
export { LIBELLES } from './carte.js'

export const TEXTES = {
  en: { ligneEnsemble: (main, pv) => `hand size ${main} / hit points ${pv}`, createur: 'Marvel Champions custom content by: ' },
  fr: { ligneEnsemble: (main, pv) => `taille de main ${main} / points de vie ${pv}`, createur: 'Contenu personnalisé Marvel Champions par : ' },
}

let traitsFr = null

/** Charge la table des traits (une fois). */
export async function chargerTraits(dossier = 'donnees/') {
  traitsFr ??= await (await fetch(dossier + 'traits-fr.json')).json()
  return traitsFr
}

/**
 * « Hero. Avenger. » -> « Héros. Vengeur. » : chaque trait (separes par des points) passe par la table ; un trait inconnu reste tel quel.
 * Sens inverse (francais -> anglais) avec `vers: 'en'`.
 */
export function traduireTraits(traits, vers = 'fr', table = traitsFr) {
  if (!traits || !table) return traits ?? ''
  const inverse = vers === 'en' ? Object.fromEntries(Object.entries(table).map(([en, fr]) => [fr, en])) : null
  return traits
    .split('.')
    .map((t) => t.trim())
    .filter(Boolean)
    .map((t) => {
      const cle = t.toUpperCase()
      const r = inverse ? inverse[cle] : table[cle]
      return r ? (t === cle ? r : r.charAt(0) + r.slice(1).toLowerCase()) : t
    })
    .join('. ') + '.'
}

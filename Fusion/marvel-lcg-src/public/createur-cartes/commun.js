// Ce que les modules de la page se partagent : petits utilitaires DOM et l'etat courant (rempli par app.js au demarrage).
export const $ = (s, r = document) => r.querySelector(s)

export const el = (tag, attrs = {}, ...enfants) => {
  const e = document.createElement(tag)
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') e.className = v
    else if (k.startsWith('on')) e.addEventListener(k.slice(2), v)
    else if (v === true) e.setAttribute(k, '')
    else if (v !== false && v != null) e.setAttribute(k, v)
  }
  for (const c of enfants.flat()) if (c != null) e.append(c.nodeType ? c : document.createTextNode(c))
  return e
}

/** L'etat courant : app.js y branche ses fonctions (carte courante, changement, types...). */
export const S = {
  carte: () => null, // la carte courante
  projet: () => ({ cartes: [] }),
  types: {},
  changement: () => {}, // a appeler apres toute modification (rendu + sauvegarde + historique)
  reconstruire: () => {}, // reconstruit le formulaire
  message: () => {},
  imageDe: async () => null,
  rendre: async () => null,
  choisir: () => {},
}

export const nouvelId = () => Math.random().toString(36).slice(2, 10)
export const blobVersDataUrl = (blob) => new Promise((ok) => { const r = new FileReader(); r.onload = () => ok(r.result); r.readAsDataURL(blob) })
export const dataUrlVersBlob = async (url) => (await fetch(url)).blob()

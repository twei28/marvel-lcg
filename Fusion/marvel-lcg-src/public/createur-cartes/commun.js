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

/**
 * Un petit bouton pipette (EyeDropper natif du navigateur) qui pose la couleur choisie dans
 * `inputCouleur` et declenche son evenement « input ». Invisible si le navigateur ne connait
 * pas l'API (Firefox, Safari a ce jour) : pas de bouton casse.
 */
export function pipette(inputCouleur) {
  if (!('EyeDropper' in window)) return null
  return el('button', {
    class: 'btn petit btn-pipette', type: 'button', title: 'Choisir une couleur n’importe où à l’écran',
    onclick: async () => {
      try {
        const r = await new EyeDropper().open()
        inputCouleur.value = r.sRGBHex
        inputCouleur.dispatchEvent(new Event('input', { bubbles: true }))
      } catch { /* annule par l'utilisateur (Echap) : rien a faire */ }
    },
  }, '🖋️')
}

export const nouvelId = () => Math.random().toString(36).slice(2, 10)
export const blobVersDataUrl = (blob) => new Promise((ok) => { const r = new FileReader(); r.onload = () => ok(r.result); r.readAsDataURL(blob) })
export const dataUrlVersBlob = async (url) => (await fetch(url)).blob()

/** Une fenetre de dialogue : titre, contenu (un element), boutons [{ texte, principal, action }]. Rend la fenetre. */
export function dialogue(titre, contenu, boutons = [{ texte: 'Fermer' }]) {
  const d = el('dialog', { class: 'dlg' })
  const rang = el('div', { class: 'rang', style: 'justify-content:flex-end;margin-top:8px' })
  for (const b of boutons) {
    rang.append(el('button', { class: 'btn' + (b.principal ? ' principal' : ''), type: 'button', onclick: async () => { if (!b.action || (await b.action(d)) !== false) d.close() } }, b.texte))
  }
  d.append(el('div', { class: 'panneau', style: 'min-width:min(560px,92vw);max-height:80vh;overflow:auto' }, el('h2', {}, titre), contenu, rang))
  document.body.append(d)
  d.addEventListener('close', () => d.remove())
  d.showModal()
  return d
}

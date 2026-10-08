// LE CADRE DU JOUEUR (08/10/2026) : le spectateur et la relecture dessinent le
// plateau DANS UN CADRE (iframe) à la taille de l'écran du joueur, avec SES
// réglages, mis à l'échelle dans l'écran de celui qui regarde. Décisions de
// l'utilisateur : « sa taille, mise à l'échelle » et « ses réglages, sauf la
// langue ».
//
// Pourquoi un cadre et pas un simple `transform` : le plateau lit
// `innerWidth`, ses media queries et `vh`/`vw`, et pose des fenêtres dans
// `document.body` (createPortal). Dans un cadre de W×H, tout cela vaut
// exactement ce que le joueur avait.
//
// ⚠ CE MODULE EST IMPORTÉ EN PREMIER par board.tsx : dans le cadre, il remplace
// `localStorage` AVANT qu'un autre module ne le lise. Le cadre lit et écrit
// une COPIE en mémoire (réglages de celui qui regarde, recouverts par ceux du
// joueur) : rien de ce que la relecture fait ne touche aux vrais réglages.

/** Ce plateau est-il dessiné dans le cadre d'un spectateur ou d'une relecture ? */
export function estCadre(): boolean {
  return new URLSearchParams(window.location.search).has('cadre')
}

/**
 * Les réglages qui voyagent avec le joueur. Tout ce qui commence par ces
 * préfixes, SAUF la langue (et ce qui en dépend : scans et textes français) et
 * ce qui n'est pas un réglage (historique, rapport en attente, hauts faits).
 */
const PREFIXES = ['marvel-board-', 'mc_', 'mode-plateau', 'marvel-ordre-cartes']
const EXCLUES = new Set([
  'marvel-langue',
  'marvel-board-scans-fr',
  'marvel-board-marvelcdb',
  'marvel-historique-partie',
  'marvel-rapport-en-attente',
  'marvel-board-succes',
])

export function estUnReglage(cle: string): boolean {
  return !EXCLUES.has(cle) && PREFIXES.some((p) => cle.startsWith(p))
}

/** Les réglages du joueur, tels qu'il les a (publiés en genre « regl »). */
export function reglagesDuJoueur(stockage: Storage = window.localStorage): Record<string, string> {
  const reglages: Record<string, string> = {}
  try {
    for (let i = 0; i < stockage.length; i++) {
      const cle = stockage.key(i)
      if (cle === null || !estUnReglage(cle)) continue
      const valeur = stockage.getItem(cle)
      if (valeur !== null && valeur.length <= 2000) reglages[cle] = valeur
    }
  } catch {
    // Stockage refusé : rien à publier.
  }
  return reglages
}

/** Un `Storage` en mémoire, qui ne touche à rien de durable. */
export class StockageMemoire implements Storage {
  private valeurs = new Map<string, string>()
  constructor(depart: Record<string, string> = {}) {
    for (const [cle, valeur] of Object.entries(depart)) this.valeurs.set(cle, valeur)
  }
  get length(): number {
    return this.valeurs.size
  }
  clear(): void {
    this.valeurs.clear()
  }
  getItem(cle: string): string | null {
    return this.valeurs.get(cle) ?? null
  }
  key(index: number): string | null {
    return [...this.valeurs.keys()][index] ?? null
  }
  removeItem(cle: string): void {
    this.valeurs.delete(cle)
  }
  setItem(cle: string, valeur: string): void {
    this.valeurs.set(cle, String(valeur))
  }
  [nom: string]: unknown
}

/** Copie de travail du cadre : les réglages de celui qui regarde, puis ceux du joueur. */
export function recouvrir(stockage: Storage, reglagesJoueur: Record<string, string>): void {
  for (let i = stockage.length - 1; i >= 0; i--) {
    const cle = stockage.key(i)
    if (cle !== null && estUnReglage(cle) && !(cle in reglagesJoueur)) stockage.removeItem(cle)
  }
  for (const [cle, valeur] of Object.entries(reglagesJoueur)) {
    if (estUnReglage(cle)) stockage.setItem(cle, valeur)
  }
}

let copie: StockageMemoire | undefined

/** Le stockage du cadre (undefined hors cadre). */
export function stockageDuCadre(): StockageMemoire | undefined {
  return copie
}

if (typeof window !== 'undefined' && estCadre()) {
  const depart: Record<string, string> = {}
  try {
    const vrai = window.localStorage
    for (let i = 0; i < vrai.length; i++) {
      const cle = vrai.key(i)
      if (cle !== null) depart[cle] = vrai.getItem(cle) ?? ''
    }
  } catch {
    // Pas de stockage : la copie part vide.
  }
  copie = new StockageMemoire(depart)
  try {
    Object.defineProperty(window, 'localStorage', { configurable: true, value: copie })
  } catch {
    // Navigateur qui refuse : le cadre lira les réglages de celui qui regarde.
  }
}

/**
 * Le cadre rend à celui qui regarde son clavier et l'approche du bas de
 * l'écran : sans cela, une fois le cadre cliqué, Espace et les flèches
 * n'atteindraient plus la barre de lecture, et la barre cachée ne reviendrait
 * plus (la souris au-dessus du cadre ne bouge que DANS le cadre).
 */
if (typeof window !== 'undefined' && estCadre() && window.parent !== window) {
  window.addEventListener(
    'keydown',
    (e) => {
      try {
        window.parent.dispatchEvent(
          new KeyboardEvent('keydown', {
            key: e.key,
            code: e.code,
            shiftKey: e.shiftKey,
            ctrlKey: e.ctrlKey,
            altKey: e.altKey,
            metaKey: e.metaKey,
            bubbles: true,
            cancelable: true,
          })
        )
      } catch {
        // Parent d'une autre origine : rien à relayer.
      }
    },
    true
  )
  window.addEventListener(
    'mousemove',
    (e) => {
      try {
        const cadre = window.frameElement
        if (!cadre) return
        const r = cadre.getBoundingClientRect()
        const k = window.innerHeight > 0 ? r.height / window.innerHeight : 1
        window.parent.dispatchEvent(
          new MouseEvent('mousemove', { clientX: r.left + e.clientX * k, clientY: r.top + e.clientY * k })
        )
      } catch {
        // Idem.
      }
    },
    true
  )
}

export const CLASSE_SURVOL = 'survol-joueur'

/**
 * LE SURVOL DU JOUEUR (`:hover`). Sa main remonte quand sa souris la survole,
 * un bouton s'éclaire : c'est du CSS, que la souris de celui qui regarde ne
 * peut pas reproduire. Chaque règle `:hover` des feuilles du plateau est donc
 * recopiée avec `.survol-joueur` à la place, et cette classe est posée sous le
 * curseur du joueur (CoucheCurseurs.tsx). Les règles imbriquées (@media,
 * @supports, @layer) gardent leur enveloppe.
 */
export function recopierSurvols(doc: Document = document): string {
  const recopier = (regles: CSSRuleList): string => {
    let sortie = ''
    for (const regle of Array.from(regles)) {
      if (regle instanceof CSSStyleRule) {
        if (regle.selectorText.includes(':hover')) {
          const selecteur = regle.selectorText.replace(/:hover/g, `.${CLASSE_SURVOL}`)
          sortie += `${selecteur} { ${regle.style.cssText} }\n`
        }
      } else if (regle instanceof CSSMediaRule) {
        const dedans = recopier(regle.cssRules)
        if (dedans) sortie += `@media ${regle.conditionText} {\n${dedans}}\n`
      } else if (regle instanceof CSSSupportsRule) {
        const dedans = recopier(regle.cssRules)
        if (dedans) sortie += `@supports ${regle.conditionText} {\n${dedans}}\n`
      } else if (typeof CSSLayerBlockRule !== 'undefined' && regle instanceof CSSLayerBlockRule) {
        const dedans = recopier(regle.cssRules)
        if (dedans) sortie += `@layer ${regle.name} {\n${dedans}}\n`
      }
    }
    return sortie
  }
  let texte = ''
  for (const feuille of Array.from(doc.styleSheets)) {
    try {
      texte += recopier(feuille.cssRules)
    } catch {
      // Feuille d'une autre origine (police) : rien à recopier.
    }
  }
  return texte
}

/** Pose une fois, dans le cadre, la feuille des survols recopiés. */
export function poserSurvolsDuJoueur(doc: Document = document) {
  if (doc.getElementById('survols-du-joueur')) return
  const style = doc.createElement('style')
  style.id = 'survols-du-joueur'
  style.textContent = recopierSurvols(doc)
  doc.head.appendChild(style)
}

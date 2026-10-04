// Charge les matchers DOM (toBeInTheDocument, toHaveClass...) pour tous les tests.
import '@testing-library/jest-dom/vitest'

// jsdom n'implemente pas window.matchMedia. useModeMobile s'en sert pour savoir
// si l'ecran est etroit ou le pointeur grossier : sans ce bouchon, tout rendu de
// composant appelant le hook leverait une TypeError. Un test qui a besoin de
// piloter la valeur pose son propre bouchon avec vi.stubGlobal.
if (typeof window !== 'undefined' && !window.matchMedia) {
  window.matchMedia = ((media: string) => ({
    media,
    matches: false,
    onchange: null,
    addEventListener: () => {},
    removeEventListener: () => {},
    addListener: () => {},
    removeListener: () => {},
    dispatchEvent: () => false,
  })) as typeof window.matchMedia
}

// jsdom n'implemente pas window.confirm (il journalise "not implemented" et
// rend undefined, donc un appel non bouchonne est deja lu comme "refuse" par
// le code, mais bruite chaque test qui l'atteint). Un bouchon qui refuse
// explicitement donne le meme resultat SANS le bruit -- utile depuis l'ajout
// du paiement/de la fin de tour automatiques (24/09/2026), qui retombent sur
// `window.confirm` via `useConfirmation()` hors `FournisseurConfirmation`
// (interaction.ts, board.tsx) des qu'une seule carte peut encore payer, meme
// dans des tests qui ne testent pas cette fonctionnalite. Un test qui pilote
// vraiment la reponse pose son propre `vi.stubGlobal('confirm', ...)`, qui
// prend le pas le temps du test et se retire proprement ensuite
// (`vi.unstubAllGlobals()` restaure CE bouchon-ci, jamais `undefined`).
//
// ⚠ PAS DE GARDE `!window.confirm` : jsdom DEFINIT deja la methode (c'est son
// CORPS qui journalise et rend undefined), donc une garde sur sa seule
// presence ne la remplacerait jamais.
if (typeof window !== 'undefined') {
  window.confirm = () => false
}

// Node 25 expose un localStorage NATIF global dont clear() est absent, et vitest
// ne le remplace pas par celui de jsdom (localStorage n'est pas dans sa liste de
// globales figee). Mesure : node -e "typeof globalThis.localStorage.clear" donne
// undefined. On pose donc un stockage memoire complet.
// Object.defineProperty et NON vi.stubGlobal : un stub serait efface par le
// vi.unstubAllGlobals() d'un test, et il faudrait le reposer apres chaque test.
if (typeof window !== 'undefined' && typeof window.localStorage?.clear !== 'function') {
  const donnees = new Map<string, string>()
  const memoire: Storage = {
    get length() {
      return donnees.size
    },
    key: (index: number) => Array.from(donnees.keys())[index] ?? null,
    getItem: (cle: string) => donnees.get(cle) ?? null,
    setItem: (cle: string, valeur: string) => {
      donnees.set(cle, String(valeur))
    },
    removeItem: (cle: string) => {
      donnees.delete(cle)
    },
    clear: () => {
      donnees.clear()
    },
  }
  Object.defineProperty(window, 'localStorage', { value: memoire, configurable: true })
}

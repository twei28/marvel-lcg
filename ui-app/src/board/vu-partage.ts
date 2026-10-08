// CE QUE LE JOUEUR VOIT, partagé avec le spectateur et la relecture.
//
// Demande du 08/10/2026 : « voir 100 % de ce que le joueur a vu quand il
// jouait ». Le monde du moteur ne dit pas tout : la carte cochée dans une
// fenêtre de paiement, la carte agrandie, la pile ouverte, les réglages (le
// volume des sons compris), la taille de l'écran, les messages, les menus,
// le glisser, les défilements. Le plateau du joueur les publie ici, un GENRE par information
// (POST /set_vu, `server_get.set_vu`), le moteur les relaie au spectateur en
// direct (GET /get_vus) et les enregistre (ligne « v » du .marvelreplay).
//
// ⚠ LE SPECTATEUR NE PUBLIE RIEN, comme pour les curseurs : il resterait
// sinon visible du joueur. Et une relecture ne publie rien non plus.
import { useEffect, useState } from 'react'
import { estSpectateur } from './moteur'
import { lecteurActif } from './relecture/lecteur'

export type GenreVu =
  | 'sel'
  | 'loupe'
  | 'pile'
  | 'regl'
  | 'ecran'
  | 'msg'
  | 'menu'
  | 'manu'
  | 'glis'
  | 'defil'

const derniers = new Map<string, string>()
const enAttente = new Map<string, { siege: number; g: GenreVu; v: unknown; minuteur: number }>()

function envoyer(siege: number, g: GenreVu, v: unknown) {
  const texte = JSON.stringify(v ?? null)
  const cle = `${siege}|${g}`
  if (derniers.get(cle) === texte) return
  derniers.set(cle, texte)
  void fetch('/set_vu', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ p: siege, g, v: v ?? null }),
  }).catch(() => undefined)
}

/** Publie ce que le joueur voit. Une valeur identique à la précédente ne part pas. */
export function publierVu(siege: number, g: GenreVu, v: unknown) {
  if (estSpectateur()) return
  const cle = `${siege}|${g}`
  const attente = enAttente.get(cle)
  if (attente) {
    window.clearTimeout(attente.minuteur)
    enAttente.delete(cle)
  }
  envoyer(siege, g, v)
}

/**
 * Même chose pour ce qui change à chaque image (glisser, défilement) : une
 * publication au plus toutes les `ms`, la DERNIÈRE valeur toujours envoyée.
 */
export function publierVuLimite(siege: number, g: GenreVu, v: unknown, ms = 120) {
  if (estSpectateur()) return
  const cle = `${siege}|${g}`
  const attente = enAttente.get(cle)
  if (attente) {
    attente.v = v
    return
  }
  envoyer(siege, g, v)
  const entree = {
    siege,
    g,
    v,
    minuteur: window.setTimeout(() => {
      enAttente.delete(cle)
      envoyer(entree.siege, entree.g, entree.v)
    }, ms),
  }
  enAttente.set(cle, entree)
}

/** Pour les tests : oublie ce qui a déjà été publié. */
export function oublierVusPublies() {
  derniers.clear()
  for (const attente of enAttente.values()) window.clearTimeout(attente.minuteur)
  enAttente.clear()
}

// --- Côté spectateur en direct : une seule lecture partagée par tous les genres.
type Instantane = Record<string, Record<string, unknown>>
let instantane: Instantane = {}
let texteInstantane = '{}'
const abonnes = new Set<() => void>()
let minuteurDirect: number | undefined

function lireDirect() {
  fetch('/get_vus', { cache: 'no-store' })
    .then((r) => (r.ok ? r.text() : '{}'))
    .then((texte) => {
      if (texte === texteInstantane) return
      texteInstantane = texte
      instantane = JSON.parse(texte) as Instantane
      for (const abonne of abonnes) abonne()
    })
    .catch(() => undefined)
}

function abonnerDirect(rappel: () => void): () => void {
  abonnes.add(rappel)
  if (minuteurDirect === undefined) {
    lireDirect()
    minuteurDirect = window.setInterval(lireDirect, 300)
  }
  return () => {
    abonnes.delete(rappel)
    if (abonnes.size === 0 && minuteurDirect !== undefined) {
      window.clearInterval(minuteurDirect)
      minuteurDirect = undefined
    }
  }
}

/**
 * Ce que le siège `siege` voit, pour un genre : `undefined` hors spectateur
 * (le plateau du joueur se sert de son propre état), ou tant que rien n'a été
 * publié. En relecture, la valeur au temps de la lecture ; en direct, la
 * dernière publiée.
 */
export function useVuDuJoueur<T>(g: GenreVu, siege: number | undefined): T | undefined {
  const [valeur, setValeur] = useState<{ texte: string; v: T | undefined }>({ texte: 'undefined', v: undefined })
  useEffect(() => {
    if (!estSpectateur() || siege === undefined) {
      setValeur({ texte: 'undefined', v: undefined })
      return
    }
    const poser = (v: unknown) => {
      const texte = v === undefined ? 'undefined' : JSON.stringify(v)
      setValeur((avant) => (avant.texte === texte ? avant : { texte, v: v as T | undefined }))
    }
    const lecteur = lecteurActif()
    if (lecteur) {
      // Réglages et écran valent dès le début : publiés un instant après le
      // premier rendu, ils s'appliquent aussi à la toute première image.
      const desLeDebut = g === 'regl' || g === 'ecran'
      const lire = () =>
        poser(lecteur.vuA(lecteur.tempsCourant(), siege, g) ?? (desLeDebut ? lecteur.premierVu(siege, g) : undefined))
      lire()
      const minuteur = window.setInterval(lire, 100)
      return () => window.clearInterval(minuteur)
    }
    const lire = () => poser(instantane[String(siege)]?.[g])
    lire()
    return abonnerDirect(lire)
  }, [g, siege])
  return valeur.v
}

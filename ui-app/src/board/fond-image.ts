// fond-image.ts — l'image de fond de la table, importée par le joueur (11/11/2026).
//
// Demande de l'utilisateur : pouvoir mettre une image à soi en fond de table. Le site n'en fournit
// AUCUNE : seul ce que le joueur importe est affiché. L'image reste sur CET appareil (navigateur),
// réduite à 1920 px et recompressée en JPEG, pour tenir dans le stockage local.
//
// Les couleurs du héros et du méchant (halos en coin, board/halo-heros.ts) sont MASQUÉES avec une
// image, sauf si le joueur coche « Garder les couleurs du héros et du méchant » (11/11/2026). Gardées,
// les bandes restent aux mêmes coins, posées par-dessus l'image.

export const CLE_FOND_IMAGE = 'mc_fond_image_v1'
export const CLE_FOND_COULEURS = 'mc_fond_image_couleurs_v1'
/** Événement émis quand l'image ou le choix des couleurs change : le plateau recalcule ses halos. */
export const EVENEMENT_FOND_IMAGE = 'fond-image-change'

/** Plus grand côté gardé à l'import. */
const COTE_MAX = 1920
/** Taille maximale de l'image stockée, en caractères (le stockage local en tient environ 5 Mo). */
const TAILLE_MAX = 2_000_000

export type ResultatImport = 'ok' | 'illisible' | 'trop-gros' | 'stockage'

export function lireFondImage(): string | undefined {
  try {
    return window.localStorage.getItem(CLE_FOND_IMAGE) ?? undefined
  } catch {
    return undefined
  }
}

export function lireGarderCouleurs(): boolean {
  try {
    return window.localStorage.getItem(CLE_FOND_COULEURS) === '1'
  } catch {
    return false
  }
}

/** Le fond de la table quand on garde les couleurs : l'image sert de couche de base, sous les bandes. */
export function baseDuFondImage(): string | undefined {
  return document.documentElement.dataset.fondImage && document.documentElement.dataset.fondCouleurs
    ? 'var(--fond-image)'
    : undefined
}

function prevenir(): void {
  window.dispatchEvent(new CustomEvent(EVENEMENT_FOND_IMAGE))
}

/**
 * Pose (ou retire, avec `undefined`) l'image de fond de la table sur la page. Le choix « garder les
 * couleurs » est relu ici : il ne vaut que s'il y a une image.
 */
export function appliquerFondImage(url: string | undefined): void {
  const racine = document.documentElement
  if (!url) {
    racine.style.removeProperty('--fond-image')
    delete racine.dataset.fondImage
    delete racine.dataset.fondCouleurs
    return
  }
  racine.style.setProperty('--fond-image', `url("${url}") center / cover no-repeat`)
  racine.dataset.fondImage = 'oui'
  if (lireGarderCouleurs()) racine.dataset.fondCouleurs = 'oui'
  else delete racine.dataset.fondCouleurs
}

export function ecrireGarderCouleurs(garder: boolean): void {
  try {
    if (garder) window.localStorage.setItem(CLE_FOND_COULEURS, '1')
    else window.localStorage.removeItem(CLE_FOND_COULEURS)
  } catch {
    /* stockage refusé : le choix vaut pour la session */
  }
  appliquerFondImage(lireFondImage())
  prevenir()
}

/** Réduit l'image importée et la range. Le résultat dit ce qui s'est passé. */
export async function importerFondImage(fichier: File): Promise<ResultatImport> {
  let source: ImageBitmap
  try {
    source = await createImageBitmap(fichier)
  } catch {
    return 'illisible'
  }
  const echelle = Math.min(1, COTE_MAX / Math.max(source.width, source.height))
  const toile = document.createElement('canvas')
  toile.width = Math.round(source.width * echelle)
  toile.height = Math.round(source.height * echelle)
  const contexte = toile.getContext('2d')
  if (!contexte) return 'illisible'
  contexte.drawImage(source, 0, 0, toile.width, toile.height)
  source.close()

  let url = toile.toDataURL('image/jpeg', 0.85)
  if (url.length > TAILLE_MAX) url = toile.toDataURL('image/jpeg', 0.7)
  if (url.length > TAILLE_MAX) return 'trop-gros'

  try {
    window.localStorage.setItem(CLE_FOND_IMAGE, url)
  } catch {
    return 'stockage'
  }
  appliquerFondImage(url)
  prevenir()
  return 'ok'
}

export function retirerFondImage(): void {
  try {
    window.localStorage.removeItem(CLE_FOND_IMAGE)
  } catch {
    /* stockage refusé : rien à retirer */
  }
  appliquerFondImage(undefined)
  prevenir()
}

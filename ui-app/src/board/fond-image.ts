// fond-image.ts — l'image de fond de la table, importée par le joueur (11/11/2026).
//
// Demande de l'utilisateur : pouvoir mettre une image à soi en fond de table. Le site n'en fournit
// AUCUNE : seul ce que le joueur importe est affiché. L'image reste sur CET appareil (navigateur),
// réduite à 1920 px et recompressée en JPEG, pour tenir dans le stockage local.
//
// La teinte (teinte.ts) reste là quand il n'y a pas d'image : le fond d'image passe par-dessus,
// et le retirer rend la couleur choisie.

export const CLE_FOND_IMAGE = 'mc_fond_image_v1'

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

/** Pose (ou retire, avec `undefined`) l'image de fond de la table sur la page. */
export function appliquerFondImage(url: string | undefined): void {
  const racine = document.documentElement
  if (!url) {
    racine.style.removeProperty('--fond-image')
    delete racine.dataset.fondImage
    return
  }
  racine.style.setProperty('--fond-image', `url("${url}")`)
  racine.dataset.fondImage = 'oui'
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
  return 'ok'
}

export function retirerFondImage(): void {
  try {
    window.localStorage.removeItem(CLE_FOND_IMAGE)
  } catch {
    /* stockage refusé : rien à retirer */
  }
  appliquerFondImage(undefined)
}

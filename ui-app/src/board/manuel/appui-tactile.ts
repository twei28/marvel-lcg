// appui-tactile.ts — au doigt, le même geste sert à deux choses (lot 4,
// question 11 du 06/10/2026) : glisser la carte, ou la tenir pour ouvrir le
// menu du clic droit. iPad n'envoie pas de `contextmenu` à l'appui long :
// c'est donc une minuterie qui décide, et un déplacement qui l'annule.
//
// Fonction PURE : le branchement (écoutes du document) vit dans CoucheTriche.tsx.
import { APPUI_LONG_MS } from '../mobile/useAppuiLong'
import { SEUIL_GLISSER } from '../glisser/useGlisser'

export type AppuiEnCours = { x: number; y: number; debut: number }

/** `glisser` : le doigt a bougé, le glisser prend la main. `menu` : tenu assez longtemps. */
export function issueAppui(
  appui: AppuiEnCours,
  maintenant: number,
  x: number,
  y: number
): 'glisser' | 'menu' | 'attente' {
  if (Math.hypot(x - appui.x, y - appui.y) >= SEUIL_GLISSER) return 'glisser'
  if (maintenant - appui.debut >= APPUI_LONG_MS) return 'menu'
  return 'attente'
}

/** La souris a déjà son clic droit : seuls le doigt et le stylet comptent. */
export const appuiCompte = (pointerType: string): boolean => pointerType === 'touch' || pointerType === 'pen'

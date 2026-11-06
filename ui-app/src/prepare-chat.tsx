// Le tchat, injecte en IFRAME dans l'ecran de preparation (`prepare.html`,
// JS classique, voir Fusion/marvel-lcg-src/public/prepare.html).
//
// ⚠ PAS DE TRANSPORT « SITE DIRECT » ICI. `prepare.html` n'est PAS servi par
// le site (orchestrateur.py) : `/entrer` redirige deja le navigateur vers le
// moteur PERSONNEL du joueur (p<N>.<domaine>, voir `_entrer_dans_partie`),
// qui sert prepare.html EXACTEMENT comme il sert board.html (meme serveur
// Python, server_html.py + server_get.py). Le `transportMoteur()` de tchat.ts
// (deja ecrit pour board.tsx) fonctionne donc ici tel quel, par defaut : une
// requete relative `fetch('/get_salon_joueurs')` depuis cette page tombe sur
// le meme moteur. Voir le commentaire equivalent dans messages.js, qui relaie
// deja par ce chemin pour la meme raison (le cookie du site ne traverse pas
// vers p<N>.<domaine>).
//
// ⚠ PAS DE TABLE ENCORE (`tableId` absent) : en preparation, avant d'etre
// assis, l'onglet Table de VoletTchat reste simplement cache (comportement
// deja prevu par le composant quand `tableId` n'est pas fourni).
import { useEffect, useState } from 'react'
import { createRoot, type Root } from 'react-dom/client'
import { VoletTchat } from './board/VoletTchat'
import './board/VoletTchat.css'

// L'iframe hote (prepare.html) reste TOUJOURS en plein viewport (sinon le
// CSS de VoletTchat.css, ancre aux bords du viewport, se positionnerait par
// rapport a une iframe minuscule au lieu de la vraie page). Le document
// parent bascule seulement `pointer-events` sur l'iframe selon la position
// du curseur, en comparant au rectangle qu'on lui transmet ici. Comme
// l'iframe occupe exactement le meme viewport que la vraie page, les
// coordonnees mesurees ici (`getBoundingClientRect`) sont deja celles de la
// vraie page : on mesure l'union des elements reellement interactifs
// (`.volet-tchat-languette`, `.volet-tchat`) et on previent le parent a
// chaque changement.
// ⚠ L'IMPASSE CORRIGEE ICI (06/11/2026, bug remonte par l'utilisateur : « je
// reste coince dans le chat, je ne peux plus cliquer sur rien »). Le parent
// ne bascule `pointer-events` a 'none' que sur SON PROPRE `mousemove` — or
// l'iframe couvre tout le viewport : des que `pointer-events:auto` est pose,
// TOUT mouvement de souris, meme loin du widget visible, est capture par le
// DOCUMENT DE CETTE IFRAME (les evenements ne traversent jamais une frontiere
// d'iframe). Le `mousemove` du parent ne reçoit donc plus RIEN, et ne peut
// plus jamais repasser l'iframe a 'none' : blocage definitif tant que la
// page n'est pas rechargee. On ferme la boucle ici : CETTE page ecoute aussi
// son propre `mousemove`, et des que le curseur sort du rectangle du widget
// (meme encore « dans » l'iframe), elle previent le parent directement.
const MARGE_PX = 4

function useSignalerEmprise() {
  useEffect(() => {
    if (window.parent === window) return
    let dernier = ''
    let rectCourant: { left: number; top: number; width: number; height: number } | null = null
    const mesurer = () => {
      const elements = document.querySelectorAll('.volet-tchat-languette, .volet-tchat')
      let rect: { left: number; top: number; right: number; bottom: number } | undefined
      elements.forEach((el) => {
        const r = el.getBoundingClientRect()
        if (r.width === 0 && r.height === 0) return
        rect = rect
          ? {
              left: Math.min(rect.left, r.left),
              top: Math.min(rect.top, r.top),
              right: Math.max(rect.right, r.right),
              bottom: Math.max(rect.bottom, r.bottom),
            }
          : { left: r.left, top: r.top, right: r.right, bottom: r.bottom }
      })
      const donnees = rect
        ? {
            left: Math.max(0, Math.floor(rect.left - MARGE_PX)),
            top: Math.max(0, Math.floor(rect.top - MARGE_PX)),
            width: Math.ceil(rect.right - rect.left + MARGE_PX * 2),
            height: Math.ceil(rect.bottom - rect.top + MARGE_PX * 2),
          }
        : { left: 0, top: 0, width: 0, height: 0 }
      rectCourant = donnees.width > 0 && donnees.height > 0 ? donnees : null
      const serialise = JSON.stringify(donnees)
      if (serialise === dernier) return
      dernier = serialise
      window.parent.postMessage({ type: 'marvel-tchat-rect', rect: donnees }, window.location.origin)
    }
    mesurer()
    // Taille/position des elements suivis (deplacement, resize de la fenetre
    // detachee) : ResizeObserver seul ne voit pas un deplacement sans
    // changement de taille, d'ou le `resize`/`scroll` en plus ci-dessous.
    const observateurTaille = new ResizeObserver(mesurer)
    const reobserver = () => {
      observateurTaille.disconnect()
      document.querySelectorAll('.volet-tchat-languette, .volet-tchat').forEach((el) => observateurTaille.observe(el))
      mesurer()
    }
    reobserver()
    // Apparition/disparition du panneau (`.volet-tchat` monte seulement si
    // `ouvert`) : il faut reobserver a chaque fois qu'il entre/sort du DOM.
    const observateurMutation = new MutationObserver(reobserver)
    observateurMutation.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'class'] })
    window.addEventListener('resize', mesurer)
    window.addEventListener('scroll', mesurer, true)

    const dansLeRectangle = (x: number, y: number) => {
      if (!rectCourant) return false
      return (
        x >= rectCourant.left && x <= rectCourant.left + rectCourant.width &&
        y >= rectCourant.top && y <= rectCourant.top + rectCourant.height
      )
    }
    const surPosition = (x: number, y: number) => {
      if (!dansLeRectangle(x, y)) {
        window.parent.postMessage({ type: 'marvel-tchat-hors-widget' }, window.location.origin)
      }
    }
    const surSouris = (e: MouseEvent) => surPosition(e.clientX, e.clientY)
    const surToucher = (e: TouchEvent) => {
      const point = e.touches[0]
      if (point) surPosition(point.clientX, point.clientY)
    }
    document.addEventListener('mousemove', surSouris, { passive: true })
    document.addEventListener('touchstart', surToucher, { passive: true })

    return () => {
      observateurTaille.disconnect()
      observateurMutation.disconnect()
      window.removeEventListener('resize', mesurer)
      window.removeEventListener('scroll', mesurer, true)
      document.removeEventListener('mousemove', surSouris)
      document.removeEventListener('touchstart', surToucher)
    }
  }, [])
}

function PageTchatPreparation() {
  const [ouvert, setOuvert] = useState(false)
  useSignalerEmprise()
  return <VoletTchat ouvert={ouvert} ouvrir={() => setOuvert(true)} fermer={() => setOuvert(false)} />
}

declare global {
  interface Window {
    racineTchatPreparation?: Root
  }
}

if (!import.meta.env.VITEST) {
  const cible = document.getElementById('tchat-racine')
  if (!cible) throw new Error('Element #tchat-racine not found in prepare-chat.html')
  window.racineTchatPreparation ??= createRoot(cible)
  window.racineTchatPreparation.render(<PageTchatPreparation />)
}

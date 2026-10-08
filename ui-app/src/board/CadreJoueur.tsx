// Le cadre du joueur, côté celui qui regarde : un iframe à la taille de l'écran
// du joueur (genre « ecran » de vu-partage.ts), mis à l'échelle et centré dans
// la place disponible. Voir cadre-joueur.ts pour l'intérieur du cadre.
import { useEffect, useState } from 'react'
import { t } from './langue'
import { useVuDuJoueur } from './vu-partage'

export type EcranJoueur = { w: number; h: number }

/** La place du cadre : sa taille, son échelle et son décalage. */
export function placerCadre(dispo: EcranJoueur, ecran: EcranJoueur | undefined, haut = 0) {
  const w = ecran && ecran.w > 0 ? ecran.w : dispo.w
  const h = ecran && ecran.h > 0 ? ecran.h : dispo.h - haut
  const echelle = Math.min(dispo.w / w, (dispo.h - haut) / h)
  return {
    w,
    h,
    echelle,
    gauche: (dispo.w - w * echelle) / 2,
    haut: haut + (dispo.h - haut - h * echelle) / 2,
  }
}

function useFenetre(): EcranJoueur {
  const [fenetre, setFenetre] = useState<EcranJoueur>({ w: window.innerWidth, h: window.innerHeight })
  useEffect(() => {
    const suivre = () => setFenetre({ w: window.innerWidth, h: window.innerHeight })
    window.addEventListener('resize', suivre)
    return () => window.removeEventListener('resize', suivre)
  }, [])
  return fenetre
}

export function CadreJoueur({ src, siege, haut = 0 }: { src: string; siege: number; haut?: number }) {
  const ecran = useVuDuJoueur<EcranJoueur>('ecran', siege)
  const place = placerCadre(useFenetre(), ecran, haut)
  return (
    <div className="cadre-joueur-fond">
      <iframe
        className="cadre-joueur"
        src={src}
        title={t('Écran du joueur')}
        style={{
          width: place.w,
          height: place.h,
          transform: `translate(${place.gauche}px, ${place.haut}px) scale(${place.echelle})`,
        }}
      />
    </div>
  )
}

/**
 * Ouvre, dans le cadre, la fenêtre des Réglages DU JOUEUR, en lecture seule
 * (décidé le 08/10/2026) : la barre du jeu est masquée pour celui qui regarde,
 * donc rien d'autre ne les montre. Le cadre écoute ce message (board.tsx).
 */
export function BoutonReglagesDuJoueur({ className }: { className?: string }) {
  return (
    <button
      type="button"
      className={className}
      title={t('Voir les réglages du joueur')}
      onClick={() =>
        document
          .querySelector<HTMLIFrameElement>('iframe.cadre-joueur')
          ?.contentWindow?.postMessage({ type: 'reglages-du-joueur' }, window.location.origin)
      }
    >
      ⚙ {t('Réglages')}
    </button>
  )
}

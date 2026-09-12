// La main du joueur, en FEUILLE au bas de l'ecran (spec du 12/09/2026) :
// cachee derriere l'encoche de droite, elle sort d'un tap ou d'un swipe, et
// toute seule quand une question du moteur porte sur une carte en main. Elle
// se referme d'un tap sur le voile, d'un swipe vers la droite, du Retour
// Android (`.main-feuille-voile` est dans FERMABLES).
//
// La rangee elle-meme est celle du 11/09 : cartes a taille lisible, qui
// defilent horizontalement. TAP = lire la carte en grand, APPUI LONG = jouer.
//
// ⚠ ScanCard est rendu EN DIRECT : ses pastilles (cout, PV) restent sur la
// carte, c'est le choix de la spec du 12/09 (« une pastille par valeur »).
import { useRef, type ReactElement } from 'react'
import { ScanCard } from '../../components/ScanCard'
import { t } from '../langue'
import type { UniteAffichee } from '../zones'
import { useAppuiLong } from './useAppuiLong'

export const SEUIL_FERMETURE = 40

/**
 * Une carte de la main, avec son geste. `useAppuiLong` tient un minuteur par
 * appel : il ne peut donc pas etre invoque depuis la boucle `.map` du parent
 * (nombre de crochets variable d'un rendu a l'autre) — d'ou ce composant,
 * un par carte, qui l'appelle une seule fois.
 */
function CarteMainPortrait({
  unite,
  onOuvrir,
  onJouer,
}: {
  unite: UniteAffichee
  onOuvrir: (unite: UniteAffichee) => void
  onJouer?: (unite: UniteAffichee) => void
}): ReactElement {
  const appui = useAppuiLong(onJouer ? () => onJouer(unite) : undefined)
  return (
    <span className="main-portrait-carte" data-tactile="carte-main" {...appui.gestes}>
      <ScanCard
        {...unite.carte}
        highlight={false}
        onSelect={() => {
          // Le maintien vient de jouer la carte : le clic qui suit le
          // relachement du doigt ne doit pas AUSSI l'ouvrir.
          if (appui.vientDeDeclencher()) return
          onOuvrir(unite)
        }}
      />
    </span>
  )
}

export function MainPortrait({
  unites,
  ouverte,
  onFermer,
  onOuvrir,
  onJouer,
}: {
  unites: UniteAffichee[]
  ouverte: boolean
  onFermer: () => void
  onOuvrir: (unite: UniteAffichee) => void
  /** Appui long : jouer la carte directement, sans passer par la lecture. */
  onJouer?: (unite: UniteAffichee) => void
}): ReactElement | null {
  const depart = useRef<number | undefined>(undefined)
  if (!ouverte) return null
  return (
    <>
      <div className="main-feuille-voile" onPointerDown={onFermer} />
      <section
        className="main-feuille"
        role="dialog"
        aria-label={t('Ta main')}
        onPointerDown={(evenement) => {
          depart.current = evenement.clientX
        }}
        onPointerMove={(evenement) => {
          if (depart.current === undefined) return
          if (evenement.clientX - depart.current >= SEUIL_FERMETURE) {
            depart.current = undefined
            onFermer()
          }
        }}
        onPointerUp={() => {
          depart.current = undefined
        }}
        onPointerCancel={() => {
          depart.current = undefined
        }}
      >
        <span className="main-feuille-poignee" aria-hidden="true" />
        {unites.length === 0 ? (
          <p className="portrait-vide main-portrait-vide">{t('Ta main est vide')}</p>
        ) : (
          <div className="main-portrait defile">
            {unites.map((unite) => (
              <CarteMainPortrait key={unite.cle} unite={unite} onOuvrir={onOuvrir} onJouer={onJouer} />
            ))}
          </div>
        )}
        <div className="main-feuille-pied">
          <span className="main-portrait-compte">
            <b>{unites.length}</b> {t('en main')}
          </span>
          <button type="button" className="main-feuille-fermer" onClick={onFermer}>
            {t('Fermer')}
          </button>
        </div>
      </section>
    </>
  )
}

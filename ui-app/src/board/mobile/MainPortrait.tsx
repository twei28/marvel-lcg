// La main du joueur, en FEUILLE au bas de l'ecran (spec du 12/09/2026) :
// cachee derriere l'encoche de droite, elle sort d'un tap ou d'un swipe, et
// toute seule quand une question du moteur porte sur une carte en main. Elle
// se referme d'un tap sur le voile, d'un swipe vers la droite, du Retour
// Android (`.main-feuille-voile` est dans FERMABLES).
//
// La rangee elle-meme est celle du 11/09 : cartes a taille lisible, qui
// defilent horizontalement.
//
// LE GESTE (zone 3 de la refonte, 10/10/2026, « jouer une carte : toucher,
// puis bouton Jouer ») :
//   TOUCHER une carte jouable -> elle se leve, « Jouer » apparait en bas ;
//   TOUCHER une carte non jouable -> elle s'ouvre en grand, pour la lire ;
//   TOUCHER LONG -> elle se JOUE si elle est jouable, sinon elle s'ouvre en
//   grand. Meme regle que sur les bandes (decision du 10/10/2026) : toucher
//   = lire, appui long = agir. Le bandeau « Annuler » rattrape un doigt
//   qui s'attarde.
//
// ⚠ ScanCard est rendu EN DIRECT : ses pastilles (cout, PV) restent sur la
// carte, c'est le choix de la spec du 12/09 (« une pastille par valeur »).
import { useEffect, useRef, useState, type ReactElement } from 'react'
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
export function CarteMainPortrait({
  unite,
  choisie,
  onChoisir,
  onOuvrir,
  onAgir,
  paiement = false,
}: {
  unite: UniteAffichee
  choisie: boolean
  /** Absent : la carte ne se choisit pas (pas jouable maintenant). */
  onChoisir?: (unite: UniteAffichee) => void
  onOuvrir: (unite: UniteAffichee) => void
  /** L'appui long : joue la carte. Absent (pas jouable) : il la lit. */
  onAgir?: (unite: UniteAffichee) => void
  /** Le moteur demande de PAYER : un toucher sur une carte qui peut payer la choisit tout de suite (24/10/2026). */
  paiement?: boolean
}): ReactElement {
  const appui = useAppuiLong(() => (onAgir ? onAgir(unite) : onOuvrir(unite)))
  return (
    <span
      className={`main-portrait-carte${choisie ? ' est-choisie' : ''}`}
      data-tactile="carte-main"
      {...appui.gestes}
    >
      <ScanCard
        {...unite.carte}
        highlight={false}
        onSelect={() => {
          // Le maintien vient de jouer ou d'ouvrir la carte : le clic qui
          // suit le relachement du doigt ne doit pas AUSSI la choisir.
          if (appui.vientDeDeclencher()) return
          // Une CIBLE de la question en cours (défausse de fin de tour, carte
          // à choisir en main) se coche d'un toucher, sans passer par sa fiche.
          const cible = unite.carte.state === 'targetable' || unite.carte.state === 'selected'
          const paie = paiement && (unite.carte.state === 'playable' || unite.carte.state === 'selected')
          if ((cible || paie) && unite.carte.onSelect) unite.carte.onSelect()
          else if (onChoisir) onChoisir(unite)
          else onOuvrir(unite)
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
  jouable,
}: {
  unites: UniteAffichee[]
  ouverte: boolean
  onFermer: () => void
  onOuvrir: (unite: UniteAffichee) => void
  /** Le bouton « Jouer » de la carte choisie. */
  onJouer?: (unite: UniteAffichee) => void
  /** Cette carte se joue-t-elle maintenant ? Oui : un toucher la choisit. */
  jouable?: (unite: UniteAffichee) => boolean
}): ReactElement | null {
  const depart = useRef<number | undefined>(undefined)
  const [cleChoisie, setCleChoisie] = useState<string | undefined>()
  // La carte choisie n'existe que tant qu'elle est en main ET jouable : jouee,
  // defaussee ou devenue injouable, le bouton disparait avec elle.
  const choisie = cleChoisie === undefined ? undefined : unites.find((u) => u.cle === cleChoisie)
  const choisieValide = choisie && onJouer && (jouable?.(choisie) ?? false) ? choisie : undefined
  useEffect(() => {
    if (!ouverte) setCleChoisie(undefined)
  }, [ouverte])
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
              <CarteMainPortrait
                key={unite.cle}
                unite={unite}
                choisie={choisieValide?.cle === unite.cle}
                onChoisir={
                  onJouer && jouable?.(unite)
                    ? (u) => setCleChoisie((avant) => (avant === u.cle ? undefined : u.cle))
                    : undefined
                }
                onOuvrir={onOuvrir}
                onAgir={
                  onJouer && jouable?.(unite)
                    ? (u) => {
                        setCleChoisie(undefined)
                        onJouer(u)
                      }
                    : undefined
                }
              />
            ))}
          </div>
        )}
        <div className="main-feuille-pied">
          {choisieValide ? (
            <button type="button" className="main-feuille-lire" onClick={() => onOuvrir(choisieValide)}>
              {t('Lire')}
            </button>
          ) : (
            <span className="main-portrait-compte">
              <b>{unites.length}</b> {t('en main')}
            </span>
          )}
          <span className="main-feuille-boutons">
            <button type="button" className="main-feuille-fermer" onClick={onFermer}>
              {t('Fermer')}
            </button>
            {choisieValide ? (
              <button
                type="button"
                className="main-feuille-jouer"
                data-tactile="jouer"
                onClick={() => {
                  setCleChoisie(undefined)
                  onJouer?.(choisieValide)
                }}
              >
                {t('Jouer')}
              </button>
            ) : null}
          </span>
        </div>
      </section>
    </>
  )
}

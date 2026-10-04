/**
 * Le journal de la partie en VOLET, tire depuis le bord droit de l'ecran.
 *
 * Demande de l'utilisateur, 03/10/2026, apres un retour de joueur sur le trop
 * plein de fenetres : « un log, avec une petite languette quelque part sur
 * l'ecran qu'on puisse tirer pour voir et remettre, en bas a droite, la ou il
 * y a les manigances ». Le volet passe PAR-DESSUS les manigances (choix de
 * l'utilisateur) et remplace la fenetre centree « Partie » : meme contenu
 * (Historique, Log, Journal du heros), recu en enfant.
 *
 * La languette se clique OU se tire : vers la gauche elle ouvre, vers la droite
 * elle referme. Un geste trop court compte pour un clic.
 */
import { useEffect, useRef } from 'react'
import { t } from './langue'
import './VoletJournal.css'

/** En dessous de ce deplacement horizontal, le geste est un simple clic. */
export const SEUIL_GESTE_PX = 24

export function VoletJournal({
  ouvert,
  ouvrir,
  fermer,
  children,
}: {
  ouvert: boolean
  ouvrir: () => void
  fermer: () => void
  children: React.ReactNode
}) {
  useEffect(() => {
    if (!ouvert) return
    const surTouche = (e: KeyboardEvent) => {
      if (e.key === 'Escape') fermer()
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [ouvert, fermer])

  const debutGeste = useRef<number | undefined>(undefined)
  // Le clic qui suit un geste ne doit pas annuler ce que le geste a fait.
  const clicAIgnorer = useRef(false)

  return (
    <>
      <button
        type="button"
        className={`volet-journal-languette${ouvert ? ' est-ouvert' : ''}`}
        aria-expanded={ouvert}
        aria-controls="volet-journal"
        title={ouvert ? t('Refermer le journal de la partie') : t('Ouvrir le journal de la partie')}
        onPointerDown={(e) => {
          debutGeste.current = e.clientX
        }}
        onPointerUp={(e) => {
          const debut = debutGeste.current
          debutGeste.current = undefined
          if (debut === undefined) return
          const dx = e.clientX - debut
          if (dx <= -SEUIL_GESTE_PX) {
            clicAIgnorer.current = true
            ouvrir()
          } else if (dx >= SEUIL_GESTE_PX) {
            clicAIgnorer.current = true
            fermer()
          }
        }}
        onClick={() => {
          if (clicAIgnorer.current) {
            clicAIgnorer.current = false
            return
          }
          if (ouvert) fermer()
          else ouvrir()
        }}
      >
        <span className="volet-journal-languette-texte">{t('Journal')}</span>
      </button>
      {ouvert ? (
        <aside id="volet-journal" className="volet-journal" role="dialog" aria-label={t('Partie')}>
          <header className="volet-journal-tete">
            <h2>{t('Partie')}</h2>
            <button type="button" className="reglages-fermer" onClick={fermer} title={t('Fermer')}>
              ×
            </button>
          </header>
          <div className="volet-journal-contenu modale-partie-contenu">{children}</div>
        </aside>
      ) : null}
    </>
  )
}

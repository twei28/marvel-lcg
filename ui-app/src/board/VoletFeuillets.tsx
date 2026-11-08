/**
 * L'onglet « FEUILLETS », tire depuis le bord droit comme l'Aide et le Journal : le feuillet de regles des heros en jeu
 * (Dazzler pour l'instant). Le parent ne le monte que s'il y a au moins un feuillet (`feuilletsDeLaPartie`).
 */
import { useEffect, useState } from 'react'
import { t } from './langue'
import type { Feuillet } from './feuillets'
import './VoletFeuillets.css'

function ImageFeuillet({ feuillet }: { feuillet: Feuillet }) {
  const [src, setSrc] = useState<string | null>(null)
  const [agrandi, setAgrandi] = useState(false)
  useEffect(() => {
    let actif = true
    void feuillet.charger().then((url) => actif && setSrc(url))
    return () => {
      actif = false
    }
  }, [feuillet])
  if (!src) return <p className="feuillet-attente">{t('Chargement…')}</p>
  return (
    <>
      <button type="button" className="feuillet-image" onClick={() => setAgrandi(true)} title={t('Agrandir')}>
        <img src={src} alt={`${t('Feuillet')} ${feuillet.titre}`} />
      </button>
      {agrandi ? (
        <div className="feuillet-zoom" role="dialog" aria-label={`${t('Feuillet')} ${feuillet.titre}`} onClick={() => setAgrandi(false)}>
          <img src={src} alt={`${t('Feuillet')} ${feuillet.titre}`} />
        </div>
      ) : null}
    </>
  )
}

export function VoletFeuillets({
  feuillets,
  ouvert,
  ouvrir,
  fermer,
}: {
  feuillets: readonly Feuillet[]
  ouvert: boolean
  ouvrir: () => void
  fermer: () => void
}) {
  useEffect(() => {
    if (!ouvert) return
    const surTouche = (e: KeyboardEvent) => {
      if (e.key === 'Escape') fermer()
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [ouvert, fermer])
  if (feuillets.length === 0) return null
  return (
    <>
      <button
        type="button"
        className={`volet-feuillets-languette${ouvert ? ' est-ouvert' : ''}`}
        aria-expanded={ouvert}
        aria-controls="volet-feuillets"
        title={ouvert ? t('Refermer les feuillets') : t('Ouvrir les feuillets')}
        onClick={ouvert ? fermer : ouvrir}
      >
        <span>{t('Feuillets')}</span>
      </button>
      {ouvert ? (
        <aside id="volet-feuillets" className="volet-feuillets" role="dialog" aria-label={t('Feuillets')}>
          <header className="volet-feuillets-tete">
            <h2>{t('Feuillets')}</h2>
            <button type="button" className="reglages-fermer" onClick={fermer} title={t('Fermer')}>
              ×
            </button>
          </header>
          <div className="volet-feuillets-corps">
            {feuillets.map((f) => (
              <section key={f.prefixe}>
                {feuillets.length > 1 ? <h3>{f.titre}</h3> : null}
                <ImageFeuillet feuillet={f} />
              </section>
            ))}
          </div>
        </aside>
      ) : null}
    </>
  )
}

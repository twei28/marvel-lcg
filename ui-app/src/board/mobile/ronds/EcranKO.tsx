// « K.O. ! » plein ecran rouge quand TON heros tombe a 0 PV (decision Q65, 24/10/2026). Le heros est elimine de la partie
// (il ne repasse PAS en alter ego) : en solo la defaite suit, en equipe tu regardes la suite. Un toucher sur « Continuer » le ferme.
import { useEffect, useState, type ReactElement } from 'react'
import { t } from '../../langue'

export function EcranKO({ elimine, nom }: { elimine: boolean; nom: string | undefined }): ReactElement | null {
  const [ferme, setFerme] = useState(false)
  // Un heros qui revient dans la partie (nouvelle partie, annulation) rearme l'ecran.
  useEffect(() => {
    if (!elimine) setFerme(false)
  }, [elimine])
  if (!elimine || ferme) return null
  return (
    <div className="ecran-ko" role="alertdialog" aria-label={t('K.O. !')}>
      <b>{t('K.O. !')}</b>
      {nom ? <span className="ecran-ko-nom">{nom}</span> : null}
      <span className="ecran-ko-texte">{t('Ton héros est éliminé de la partie.')}</span>
      <button type="button" className="ecran-ko-continuer" onClick={() => setFerme(true)}>
        {t('Continuer')}
      </button>
    </div>
  )
}

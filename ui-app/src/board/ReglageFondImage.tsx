// ReglageFondImage.tsx — « Image de fond de la table » dans les Réglages (11/11/2026).
//
// Le joueur importe sa propre image ; le site n'en fournit aucune. Importer remplace l'image
// précédente, « Retirer » rend la couleur de la table. Voir board/fond-image.ts.
import { useState } from 'react'
import type { ChangeEvent } from 'react'
import { t } from './langue'
import { importerFondImage, lireFondImage, retirerFondImage, type ResultatImport } from './fond-image'

const MESSAGES: Record<Exclude<ResultatImport, 'ok'>, string> = {
  illisible: "Ce fichier n'est pas une image lisible.",
  'trop-gros': "L'image reste trop lourde même réduite : prends-en une plus petite.",
  stockage: "Le navigateur refuse de garder l'image (stockage plein).",
}

export function ReglageFondImage() {
  const [presente, setPresente] = useState(() => !!lireFondImage())
  const [message, setMessage] = useState<string>()

  async function choisir(evenement: ChangeEvent<HTMLInputElement>) {
    const fichier = evenement.target.files?.[0]
    evenement.target.value = ''
    if (!fichier) return
    const resultat = await importerFondImage(fichier)
    if (resultat === 'ok') {
      setPresente(true)
      setMessage(undefined)
    } else {
      setMessage(t(MESSAGES[resultat]))
    }
  }

  return (
    <div className="reglage-fond-image">
      <span className="reglage-teinte-titre">{t('Image de fond de la table')}</span>
      <div className="reglage-fond-image-actions">
        <label className="reglage-fond-image-bouton">
          {t('Importer une image…')}
          <input type="file" accept="image/*" hidden onChange={choisir} />
        </label>
        {presente ? (
          <button
            type="button"
            className="reglage-fond-image-bouton"
            onClick={() => {
              retirerFondImage()
              setPresente(false)
              setMessage(undefined)
            }}
          >
            {t('Retirer')}
          </button>
        ) : null}
      </div>
      {message ? <p className="reglage-fond-image-erreur" role="alert">{message}</p> : null}
    </div>
  )
}

// LA FACE A DE LA MANIGANCE, EN GRAND, AVANT QU'ELLE SE RETOURNE.
//
// Demande de l'utilisateur, 15/09/2026 : « on doit voir la face A de la
// premiere manigance, puis on fait ok, puis elle se place sur la face B ».
// Le moteur ATTEND vraiment cette reponse (World.ConfirmMainSchemeReveal) :
// c'est le seul mouvement de toute l'ouverture, tout le reste a ete rendu
// silencieux expres (voir manigance-face-a.ts).

import { useState } from 'react'
import { scanUrl } from './card-model'
import { t } from './langue'
import { nomAffiche } from './noms-cartes-fr'
import type { WorldCard } from './world'

export function PanneauManigance({
  carte,
  onValider,
}: {
  carte: WorldCard
  onValider: () => void
}) {
  // ⚠ UN SEUL ENVOI. Le moteur n'attend qu'une reponse ; une seconde partirait
  // dans le vide, ou pire, repondrait a la question suivante. `envoye` porte
  // aussi bien la garde du double clic que le declenchement du retournement :
  // les deux se decident au meme instant.
  const [envoye, setEnvoye] = useState(false)

  return (
    <div
      className={`panneau-manigance${envoye ? ' est-retournee' : ''}`}
      role="dialog"
      aria-modal="true"
    >
      <img className="panneau-manigance-carte" src={scanUrl(carte.pic_id)} alt={nomAffiche(carte)} />
      <button
        type="button"
        className="panneau-manigance-ok"
        disabled={envoye}
        onClick={() => {
          if (envoye) return
          setEnvoye(true)
          onValider()
        }}
      >
        {t('Retourner la manigance')}
      </button>
    </div>
  )
}

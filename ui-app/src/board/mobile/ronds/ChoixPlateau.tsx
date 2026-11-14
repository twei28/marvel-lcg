// LE CHOIX DU PLATEAU, a chaque debut de partie sur telephone (demande du 24/10/2026) : les ronds sont un essai, le
// joueur choisit entre les cartes en bandes (le plateau d'origine) et les ronds. La question se repose a chaque partie
// TANT QUE le joueur n'a pas coche « garder ce choix » (precision du 24/10/2026) ; ensuite elle ne revient plus, et le
// choix se change dans les Reglages (« Plateau », « Demander a chaque partie »). Le dernier choix est pre-selectionne.
//
// « Une nouvelle partie » = le round 1 du plateau, pas encore repondu dans cet onglet. Le marqueur vit dans
// sessionStorage et tombe des que la partie passe au round 2 : recharger la page en plein round 1 ne repose pas la
// question, la partie suivante la repose.
import { useEffect, useState, type ReactElement } from 'react'
import { createPortal } from 'react-dom'
import { t } from '../../langue'
import { ecrireReglageTelephone, plateauDejaChoisi, useReglagesTelephone, type PlateauTelephone } from '../reglages-telephone'
import './ronds.css'

export const CLE_CHOIX_PLATEAU = 'marvel-tel-plateau-choisi'

function lire(): boolean {
  try {
    return window.sessionStorage.getItem(CLE_CHOIX_PLATEAU) === '1'
  } catch {
    return false
  }
}

function ecrire(fait: boolean): void {
  try {
    if (fait) window.sessionStorage.setItem(CLE_CHOIX_PLATEAU, '1')
    else window.sessionStorage.removeItem(CLE_CHOIX_PLATEAU)
  } catch {
    // Stockage indisponible : la question se reposera au prochain chargement.
  }
}

/** Faut-il poser la question ? Vrai au round 1 d'une partie vivante, tant qu'on n'a pas repondu. */
export function useChoixPlateau(
  roundId: number | undefined,
  enVueDEtat: boolean
): { demander: boolean; repondre: (choix: PlateauTelephone, garder?: boolean) => void } {
  const { plateauMemorise } = useReglagesTelephone()
  const [fait, setFait] = useState(lire)
  useEffect(() => {
    if (roundId !== undefined && roundId > 1 && lire()) {
      ecrire(false)
      setFait(false)
    }
  }, [roundId])
  const demander = !enVueDEtat && !plateauMemorise && roundId !== undefined && roundId <= 1 && !fait
  return {
    demander,
    repondre: (choix, garder = false) => {
      ecrireReglageTelephone('plateau', choix)
      if (garder) ecrireReglageTelephone('plateauMemorise', true)
      ecrire(true)
      setFait(true)
    },
  }
}

export function ChoixPlateau({ repondre }: { repondre: (choix: PlateauTelephone, garder?: boolean) => void }): ReactElement {
  const { plateau } = useReglagesTelephone()
  // Les ronds d'abord, et presélectionnés tant que le joueur n'a rien choisi : plus adaptés au téléphone (26/10/2026).
  const ronds = plateau === 'ronds' || !plateauDejaChoisi()
  const [garder, setGarder] = useState(false)
  return createPortal(
    <div className="choix-plateau-voile" role="dialog" aria-modal="true" aria-label={t('Quel plateau ?')}>
      <div className="choix-plateau">
        <h2>{t('Quel plateau ?')}</h2>
        <p>{t('Choisis comment afficher la table pour cette partie. Tu pourras changer dans les réglages.')}</p>
        <div className="choix-plateau-boutons">
          <button type="button" className={ronds ? 'est-propose' : ''} onClick={() => repondre('ronds', garder)}>
            <b>{t('Ronds')} <small>{t('conseillé')}</small></b>
            <span>{t('Plus adapté au téléphone : chaque carte en rond, tout tient sur l’écran')}</span>
          </button>
          <button type="button" className={!ronds ? 'est-propose' : ''} onClick={() => repondre('cartes', garder)}>
            <b>{t('Cartes')}</b>
            <span>{t('Les cartes en bandes, comme avant')}</span>
          </button>
        </div>
        <label className="choix-plateau-garder">
          <input type="checkbox" checked={garder} onChange={(evenement) => setGarder(evenement.target.checked)} />
          <span>{t('Garder ce choix pour les prochaines parties')}</span>
        </label>
      </div>
    </div>,
    document.body
  )
}

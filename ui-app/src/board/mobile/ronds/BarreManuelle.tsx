// MODE MANUEL au doigt (decision Q52, 24/10/2026) : on touche un rond pour le CHOISIR, une barre d'outils en bas agit dessus
// (PV, menace, jeton, epuiser, defausser). « Lire » ouvre la feuille de la carte. Memes ordres que le menu du clic droit du PC
// (`triche.ts`), memes mots ; la table se met a jour par l'etat du moteur, comme apres n'importe quel geste.
import type { ReactElement } from 'react'
import type { ScanCardProps } from '../../../components/ScanCard'
import { t } from '../../langue'
import * as triche from '../../triche'

const PERSONNAGES = new Set(['hero', 'alter-ego', 'ally', 'minion', 'villain'])
const COMPLOTS = new Set(['main-scheme', 'side-scheme'])

export function BarreManuelle({
  carte,
  onLire,
  onFermer,
}: {
  carte: ScanCardProps | undefined
  onLire: () => void
  onFermer: () => void
}): ReactElement | null {
  if (!carte) return null
  const id = Number(carte.id)
  const personnage = PERSONNAGES.has(carte.kind)
  const complot = COMPLOTS.has(carte.kind)
  const compteur = (carte.counters ?? [])[0]
  const agir = (action: () => Promise<boolean>) => () => void action()
  return (
    <div className="barre-manuelle" role="toolbar" aria-label={t('Outils du mode manuel')}>
      <span className="barre-manuelle-nom">{carte.name}</span>
      <div className="barre-manuelle-boutons">
        {personnage ? (
          <>
            <button type="button" onClick={agir(() => triche.blesser(id, 1))}>
              {t('PV')} −1
            </button>
            <button type="button" onClick={agir(() => triche.soigner(id, 1))}>
              {t('PV')} +1
            </button>
          </>
        ) : null}
        {complot ? (
          <>
            <button type="button" onClick={agir(() => triche.poserMenace(id, -1))}>
              {t('Menace')} −1
            </button>
            <button type="button" onClick={agir(() => triche.poserMenace(id, 1))}>
              {t('Menace')} +1
            </button>
          </>
        ) : null}
        <button type="button" onClick={agir(() => triche.poserCompteur(id, 'counter', (compteur?.value ?? 0) + 1))}>
          {t('Jeton')} +1
        </button>
        {!complot ? (
          <button type="button" onClick={agir(() => (carte.exhausted ? triche.redresser(id) : triche.incliner(id)))}>
            {carte.exhausted ? t('Redresser') : t('Incliner')}
          </button>
        ) : null}
        <button type="button" onClick={agir(() => triche.defausser(id))}>
          {t('Défausser')}
        </button>
        <button type="button" onClick={onLire}>
          {t('Lire')}
        </button>
        <button type="button" onClick={onFermer} aria-label={t('Fermer')}>
          ×
        </button>
      </div>
    </div>
  )
}

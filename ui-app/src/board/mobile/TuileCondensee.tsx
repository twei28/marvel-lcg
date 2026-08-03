// Une entite du plateau, reduite a ce qu'il faut pour DECIDER : sa vignette, son
// nom, et les seuls chiffres qui comptent. Le texte de regles et le scan complet
// arrivent au tap, dans le menu d'actions.
//
// Une tuile est un <button> : c'est ce qui la rend atteignable au doigt ET au
// clavier sans code supplementaire, et ce qui lui donne un role accessible.

import { t } from '../langue'
import type { ScanCardProps } from '../../components/ScanCard'
import type { Taille } from './condensation'
import './mobile.css'

export type TuileCondenseeProps = {
  carte: ScanCardProps
  taille: Taille
  onOuvrir: () => void
}

export function TuileCondensee({ carte, taille, onOuvrir }: TuileCondenseeProps) {
  // Une carte face cachee ne divulgue NI son nom NI ses compteurs : ce serait
  // donner au joueur une information que le moteur lui refuse.
  const cachee = carte.facedown === true && carte.peeking !== true
  const nom = cachee ? t('Carte face cachée') : carte.name

  return (
    <button
      type="button"
      className={`tuile ${taille === 'plancher' ? 'tuile-plancher' : 'tuile-confort'}`}
      onClick={onOuvrir}
      data-tactile="tuile"
      // Etat pose par l'interaction en cours (jouable, ciblable, choisie...).
      // Sans lui, aucune carte n'etait signalee comme agissante sur mobile.
      data-etat={carte.state}
    >
      <span className="tuile-vignette" aria-hidden="true">
        {!cachee && carte.imageUrl ? <img src={carte.imageUrl} alt="" loading="lazy" /> : null}
      </span>
      <span className="tuile-texte">
        <span className="tuile-nom">
          {nom}
          {carte.estActif && !cachee ? (
            <span className="tuile-actif">{t('Actif')}</span>
          ) : null}
        </span>
        {cachee ? null : (
          <span className="tuile-compteurs">
            {carte.allyHp ? <span className="tuile-pv">{carte.allyHp}</span> : null}
            {carte.schemeThreat ? (
              <span className="tuile-menace">{carte.schemeThreat}</span>
            ) : null}
            {carte.pileCount ? <span className="tuile-pile">{carte.pileCount}</span> : null}
            {(carte.counters ?? []).map((compteur) => (
              <span className="tuile-compteur" key={compteur.label}>
                {compteur.label} {compteur.value}
              </span>
            ))}
            {carte.effectDelta ? (
              <span className={`tuile-delta tuile-delta-${carte.effectDelta.kind}`}>
                {carte.effectDelta.value > 0 ? `+${carte.effectDelta.value}` : carte.effectDelta.value}
              </span>
            ) : null}
          </span>
        )}
      </span>
    </button>
  )
}

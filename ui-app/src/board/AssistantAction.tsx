import type { Demande } from './ask'
import { classeTonaliteAction } from './action-style'
import { nomLisible } from './BarreAction'
import type { Interaction } from './interaction'
import { t } from './langue'
import type { WorldCard } from './world'

type AssistantActionProps = {
  demande?: Demande
  interaction: Interaction
  aNous: boolean
  connecte: boolean
  cartesParId: Map<number, WorldCard>
  affichage?: 'simple' | 'detailed'
}

function nomCarte(id: number, cartesParId: Map<number, WorldCard>): string {
  return cartesParId.get(id)?.name ?? `${t('Carte')} ${id}`
}

function nomsCibles(cibles: number[], cartesParId: Map<number, WorldCard>): string {
  const comptes = new Map<number, number>()
  for (const cible of cibles) comptes.set(cible, (comptes.get(cible) ?? 0) + 1)
  return [...comptes.entries()]
    .map(([id, nombre]) => `${nomCarte(id, cartesParId)}${nombre > 1 ? ` x${nombre}` : ''}`)
    .join(', ')
}

function resume(interaction: Interaction, cartesParId: Map<number, WorldCard>): string {
  const option = interaction.option
  if (!option) return ''
  const morceaux = [nomLisible(option)]
  if (interaction.cibles.length > 0) {
    morceaux.push(nomsCibles(interaction.cibles, cartesParId))
  }
  if (interaction.coutAffiche) morceaux.push(`${t('coût')} ${interaction.coutAffiche}`)
  return morceaux.join(' -> ')
}

function etapeDirecte(interaction: Interaction): string {
  const option = interaction.option
  if (!option) return ''
  const etape =
    interaction.assistant.etape === 'target'
      ? t('choisir la cible')
      : interaction.assistant.etape === 'payment'
        ? t('payer le coût')
        : t('confirmer')
  return `${nomLisible(option)} -> ${etape}`
}

function indicationSimple(interaction: Interaction): string {
  const assistant = interaction.assistant
  const etape = assistant.etape
  if (etape === 'target') {
    // Le mode simple n'affiche pas `detail` : sans le compteur ici, une action
    // repartie sur plusieurs attributions (43006) passe pour une cible unique.
    if (assistant.cibleMaximum > 1) {
      return `${t('Choisis les cibles')} ${assistant.cibleNombre}/${assistant.cibleMaximum}`
    }
    return t('Choisis la cible')
  }
  if (etape === 'payment') return interaction.coutAffiche ? `${t('Paie')} ${interaction.coutAffiche}` : t('Paie le coût')
  return ''
}

function classeType(type: string | undefined): string {
  const t = (type ?? '').toLowerCase()
  return ['r', 'b', 'y', 'g'].includes(t) ? `est-${t}` : ''
}

export function AssistantAction({
  demande,
  interaction,
  aNous,
  connecte,
  cartesParId,
  affichage = 'detailed',
}: AssistantActionProps) {
  if (!connecte || !aNous || !demande || !interaction.option) return null

  const assistant = interaction.assistant
  const action = resume(interaction, cartesParId)
  const titre = etapeDirecte(interaction)
  const montrerResume = interaction.cibles.length > 0 || interaction.coutAffiche !== ''
  const nomAction = nomLisible(interaction.option)

  if (affichage === 'simple') {
    const indication = indicationSimple(interaction)
    return (
      <aside
        className={`assistant-action mode-simple etape-${assistant.etape} ${classeTonaliteAction(nomAction)}`}
        aria-live="polite"
      >
        <span className="assistant-simple-action">{nomAction}</span>
        {indication ? <span className="assistant-simple-indication">{indication}</span> : null}
        {assistant.indice ? <span className="assistant-indice">{assistant.indice}</span> : null}
        {montrerResume && action ? <span className="assistant-simple-resume">{action}</span> : null}
        <div className="assistant-boutons">
          <button type="button" className="assistant-annuler" onClick={interaction.annuler}>
            {t('Annuler')}
          </button>
          {interaction.prete ? (
            <button type="button" className="assistant-confirmer" onClick={interaction.valider}>
              {t('Confirmer')}
            </button>
          ) : null}
        </div>
      </aside>
    )
  }

  return (
    <aside className={`assistant-action etape-${assistant.etape}`} aria-live="polite">
      <span className="assistant-eyebrow">{nomLisible(interaction.option)}</span>
      <strong>{titre || assistant.titre}</strong>
      {assistant.detail ? <span className="assistant-detail">{assistant.detail}</span> : null}
      {assistant.indice ? <span className="assistant-indice">{assistant.indice}</span> : null}

      {assistant.etape === 'payment' && assistant.coutSlots.length > 0 ? (
        <div className="assistant-cout" aria-label={t('Coût à payer')}>
          {assistant.coutSlots.map((slot) => (
            <span
              className={`assistant-slot${slot.rempli ? ' est-rempli' : ''} ${classeType(slot.type)}`}
              key={slot.index}
            >
              {slot.label ?? ''}
            </span>
          ))}
          {assistant.coutRegles.length > 0 ? (
            <span className="assistant-regles">{assistant.coutRegles.join(' - ')}</span>
          ) : null}
        </div>
      ) : null}

      {montrerResume && action ? (
        <span className="assistant-resume">{action}</span>
      ) : null}

      {/* Confirmer / annuler ICI, au centre de l'ecran : plus besoin d'aller
          chercher le bouton en bas a droite a chaque action. */}
      <div className="assistant-boutons">
        <button type="button" className="assistant-annuler" onClick={interaction.annuler}>
          {t('Annuler')}
        </button>
        <button
          type="button"
          className="assistant-confirmer"
          disabled={!interaction.prete}
          onClick={interaction.valider}
        >
          {t('Confirmer')}
        </button>
      </div>
    </aside>
  )
}

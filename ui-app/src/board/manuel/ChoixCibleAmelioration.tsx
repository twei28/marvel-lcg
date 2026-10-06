// ChoixCibleAmelioration.tsx — sur quelle carte attacher une amélioration
// lâchée sur la table (question 3 du 06/10/2026 : « propose sur qui on veut
// l'attacher, si c'est possible de l'attacher sur quelque chose d'autre »).
//
// Une seule cible possible (l'identité) : `poser-en-jeu.ts` attache sans
// fenêtre. Plusieurs : cette fenêtre, sur le patron de « On en est où ? »
// (`InterrupteurFacon.tsx`), mêmes classes, aucune apparence nouvelle.
// Fermer sans choisir n'envoie rien.
import { useEffect } from 'react'
import { t } from '../langue'
import type { CibleAmelioration } from './poser-en-jeu'

export type ChoixCible = { sourceId: number; nom: string; cibles: CibleAmelioration[] }

export function ChoixCibleAmelioration({
  choix,
  onChoisir,
  onFermer,
}: {
  choix: ChoixCible
  onChoisir: (cible: CibleAmelioration) => void
  onFermer: () => void
}) {
  useEffect(() => {
    const surEchap = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') onFermer()
    }
    document.addEventListener('keydown', surEchap)
    return () => document.removeEventListener('keydown', surEchap)
  }, [onFermer])

  const titre = `${t('Attacher')} ${choix.nom}`
  return (
    <div className="pile-triche-voile" onPointerDown={onFermer}>
      <section
        className="pile-triche choix-reprise"
        role="dialog"
        aria-label={titre}
        onPointerDown={(evenement) => evenement.stopPropagation()}
      >
        <header className="pile-triche-entete">
          <h2>{titre}</h2>
          <button type="button" onClick={onFermer}>
            {t('Annuler')}
          </button>
        </header>
        <p className="choix-reprise-aide">{t('Sur quelle carte ?')}</p>
        <ul className="choix-reprise-liste">
          {choix.cibles.map((cible) => (
            <li key={cible.id}>
              <button type="button" onClick={() => onChoisir(cible)}>
                <strong>{cible.nom}</strong>
              </button>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}

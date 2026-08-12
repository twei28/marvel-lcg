// Les deux sorties du rapport de bug : le presse-papier et un fichier.
//
// La capture se fait AU CLIC (décision du 12/8/2026) : le rapport lit le monde
// et la demande du moment. Le journal, lui, couvre déjà le passé. Aucun tampon
// d'états n'est gardé, donc aucun coût mémoire.
//
// Le message rendu par le crochet sert au panneau ET au raccourci clavier :
// capturer sans ouvrir le panneau doit quand même se voir, sinon on ne sait pas
// si le geste a pris.
import { useCallback, useEffect, useRef, useState } from 'react'
import { CLE_TUTORIEL } from './CoucheCoach'
import { lireContexte } from './campagne/contexte'
import { erreursRecentes } from './erreurs-console'
import { t } from './langue'
import type { Demande } from './ask'
import type { EntreeHistorique } from './HistoriquePartie'
import {
  construireRapport,
  nomFichierRapport,
  rapportEnTexte,
  type PorteeRapport,
  type RapportBug as Rapport,
} from './rapport-bug'
import type { World } from './world'

export type OutilsRapport = {
  copier: (portee: PorteeRapport) => Promise<void>
  telecharger: (portee: PorteeRapport) => void
  /** Confirmation transitoire, ou null. Affichée aussi hors du panneau. */
  message: string | null
}

const DUREE_MESSAGE = 4000

function enModeDecouverte(): boolean {
  try {
    return window.localStorage.getItem(CLE_TUTORIEL) !== null
  } catch {
    return false
  }
}

function contexteCampagne(): { id: string; scenario: string } | undefined {
  const contexte = lireContexte()
  return contexte ? { id: contexte.id, scenario: contexte.scenario } : undefined
}

export function useRapportBug(
  monde: World | undefined,
  demande: Demande | undefined,
  entrees: EntreeHistorique[],
  siege?: number
): OutilsRapport {
  const [message, setMessage] = useState<string | null>(null)
  const minuterie = useRef<number | undefined>(undefined)

  // Le message s'efface tout seul. Sans ce nettoyage, un démontage pendant les
  // quatre secondes laisserait la minuterie appeler setMessage dans le vide.
  useEffect(() => () => window.clearTimeout(minuterie.current), [])

  const annoncer = useCallback((texte: string) => {
    setMessage(texte)
    window.clearTimeout(minuterie.current)
    minuterie.current = window.setTimeout(() => setMessage(null), DUREE_MESSAGE)
  }, [])

  const construire = useCallback(
    (portee: PorteeRapport): Rapport | null => {
      if (!monde) return null
      return construireRapport(monde, demande, entrees, portee, {
        horodatage: new Date().toISOString(),
        siege,
        campagne: contexteCampagne(),
        decouverte: enModeDecouverte(),
        erreurs: erreursRecentes(),
        url: window.location.href,
      })
    },
    [monde, demande, entrees, siege]
  )

  // Rend une promesse : sans elle, un test ne peut pas attendre la fin de
  // l'écriture, et l'appelant clavier n'a aucun moyen de savoir que c'est fini.
  const copier = useCallback(
    async (portee: PorteeRapport) => {
      const rapport = construire(portee)
      if (!rapport) return
      // Le presse-papier peut être refusé (page non sécurisée, permission
      // retirée). Un échec silencieux ferait croire à une copie réussie et
      // ferait coller le presse-papier PRÉCÉDENT.
      try {
        await navigator.clipboard.writeText(rapportEnTexte(rapport))
        annoncer(t('Rapport copié'))
      } catch {
        annoncer(t('Copie refusée par le navigateur'))
      }
    },
    [construire, annoncer]
  )

  const telecharger = useCallback(
    (portee: PorteeRapport) => {
      const rapport = construire(portee)
      if (!rapport) return
      const contenu = new Blob([JSON.stringify(rapport, null, 1)], { type: 'application/json' })
      const url = URL.createObjectURL(contenu)
      const lien = document.createElement('a')
      lien.href = url
      lien.download = nomFichierRapport(rapport)
      lien.click()
      URL.revokeObjectURL(url)
      annoncer(t('Rapport téléchargé'))
    },
    [construire, annoncer]
  )

  return { copier, telecharger, message }
}

const PORTEES: Array<{ valeur: PorteeRapport; libelle: string }> = [
  { valeur: 'recent', libelle: '20 dernières' },
  { valeur: 'tour', libelle: 'Ce tour' },
  { valeur: 'partie', libelle: 'Toute la partie' },
]

export function BoutonsRapportBug({ outils }: { outils: OutilsRapport }) {
  const [portee, setPortee] = useState<PorteeRapport>('recent')

  return (
    <div className="hp-rapport">
      <label className="hp-rapport-portee">
        {t('Profondeur')}
        <select value={portee} onChange={(e) => setPortee(e.target.value as PorteeRapport)}>
          {PORTEES.map(({ valeur, libelle }) => (
            <option key={valeur} value={valeur}>
              {t(libelle)}
            </option>
          ))}
        </select>
      </label>
      <button
        type="button"
        onClick={() => void outils.copier(portee)}
        title={t('Copier un rapport de bug')}
      >
        {t('Copier')}
      </button>
      <button
        type="button"
        onClick={() => outils.telecharger(portee)}
        title={t('Télécharger le rapport complet')}
      >
        {t('Télécharger')}
      </button>
    </div>
  )
}

/** Confirmation transitoire, visible même quand le panneau est fermé. */
export function MessageRapport({ message }: { message: string | null }) {
  if (!message) return null
  return (
    <span className="hp-rapport-message" role="status" aria-live="polite">
      {message}
    </span>
  )
}

// Les deux pièces propres à la « Phase dynamique » (16/10/2026, voir
// cartouche-dynamique.css) : la LIGNE DE QUESTION, en clair, au-dessus des choix, et
// l'HISTORIQUE compact des événements déjà confirmés.
//
// Ni l'une ni l'autre ne décide ni ne calcule rien : la question vient du moteur (le
// texte qu'il envoie, ou la carte qui l'a posée), l'historique relit les étapes déjà
// passées du cartouche. Aucune commande n'est envoyée d'ici.

import { useMemo, useRef, useState } from 'react'
import { titreDepuisSource } from './DemandeCentrale'
import type { EtapeDeroule } from './deroule-phase'
import { titreEtape } from './deroule-textes'
import { etapeEnLangue } from './etape-en-langue'
import { t } from './langue'
import type { QuestionDuMoteur } from './sous-cadre'

/**
 * La phrase de la décision. Une défense se dit « Qui défend contre cette attaque ? »
 * (les défenseurs possibles sont les boutons juste dessous) ; toute autre question
 * garde le texte du moteur, ou la carte qui la pose.
 */
export function phraseQuestion(q: QuestionDuMoteur, defense: boolean): string {
  if (defense) return t('Qui défend contre cette attaque ?')
  return titreDepuisSource(q.demande, q.demande.options, q.cartesParId)
}

export function QuestionDynamique({ q, defense }: { q: QuestionDuMoteur | undefined; defense: boolean }) {
  if (!q) return null
  return (
    <p className="dyn-question" role="status">
      {phraseQuestion(q, defense)}
    </p>
  )
}

/** Les événements déjà confirmés, les plus récents d'abord. Rien de ce qui est annoncé ou en cours. */
export function evenementsConfirmes(etapes: readonly EtapeDeroule[], index: number): EtapeDeroule[] {
  return etapes
    .slice(0, Math.max(0, index))
    .filter((e) => e.etat !== 'annonce')
    .reverse()
}

/** Une ligne d'historique en clair : les étapes sans rédaction propre ne montrent jamais leur nom interne. */
export function phraseHistorique(e: EtapeDeroule, stade?: number): string {
  switch (e.titre) {
    case 'stade-revele':
      // « Klaw passe au stade 2 » (19/10/2026) : jamais la cle interne « stade-revele ».
      return e.cibleNom
        ? stade !== undefined && stade > 0
          ? t('%1 passe au stade %2').replace('%1', e.cibleNom).replace('%2', String(stade))
          : t('%1 passe au stade suivant').replace('%1', e.cibleNom)
        : t('Le méchant passe au stade suivant')
    case 'paquet-vide':
      return t('Paquet rencontre vide')
    case 'etoile-differe':
      return e.auteurNom ? t('Effet ★ de %1').replace('%1', e.auteurNom) : t('Effet ★')
    case 'riposte':
      return e.auteurNom ? t('Riposte de %1').replace('%1', e.auteurNom) : t('Riposte')
    case 'elimination':
      return e.cibleNom ? t('%1 est éliminé').replace('%1', e.cibleNom) : t('Un héros est éliminé')
    default:
      return titreEtape(e)
  }
}

export function HistoriqueDynamique({
  etapes,
  index,
  nomFr,
}: {
  etapes: readonly EtapeDeroule[]
  index: number
  /** Les noms français des cartes (l'étape ne porte que les noms du moteur, en anglais). */
  nomFr?: (id: number) => string | undefined
}) {
  const [ouvert, setOuvert] = useState(false)
  const faits = evenementsConfirmes(etapes, index)
  if (faits.length === 0) return null
  const montres = ouvert ? faits : faits.slice(0, 3)
  return (
    <div className="dyn-historique">
      <div className="dyn-historique-tete">
        <span>{t('Historique')}</span>
        {faits.length > 3 ? (
          <button type="button" className="dyn-historique-bascule" aria-expanded={ouvert} onClick={() => setOuvert((o) => !o)}>
            {ouvert ? t('Réduire') : `${t('Tout voir')} (${faits.length})`}
          </button>
        ) : null}
      </div>
      <ol className={ouvert ? 'dyn-historique-liste est-ouverte' : 'dyn-historique-liste'}>
        {montres.map((e) => (
          <li key={e.cle}>{phraseHistorique(etapeEnLangue(e, nomFr))}</li>
        ))}
      </ol>
    </div>
  )
}

/**
 * UNE COMMANDE UNE SEULE FOIS PAR DÉCISION (exigence du 16/10/2026) : un double clic
 * sur « Défendre avec X » ne doit pas envoyer deux réponses. Chaque commande
 * TERMINALE (choisir une option, valider, annuler) refuse d'être redite à l'identique
 * pendant `DELAI_COMMANDE_MS`, tant que la même décision est à l'écran. Rien d'autre
 * n'est filtré : choisir une AUTRE option, ou cliquer plusieurs cibles, reste libre.
 *
 * ⚠ C'est un filtre d'interface, pas une règle : la validité d'une commande reste au
 * moteur. Il ne retient rien, ne retarde rien, et ne désactive aucun bouton qui
 * pourrait rester sans réponse.
 */
export const DELAI_COMMANDE_MS = 1200

export function cleDeDecision(q: QuestionDuMoteur): string {
  return `${q.demande.event_name}|${q.demande.prompt_text}|${q.demande.options.map((o) => o.id).join(',')}`
}

export function useCommandeUneFois(q: QuestionDuMoteur | undefined, actif: boolean): QuestionDuMoteur | undefined {
  const derniere = useRef<{ cle: string; quand: number } | undefined>(undefined)
  return useMemo(() => {
    if (!q || !actif) return q
    const decision = cleDeDecision(q)
    const ouvrir = (commande: string): boolean => {
      const cle = `${decision}#${commande}`
      const maintenant = Date.now()
      const d = derniere.current
      if (d && d.cle === cle && maintenant - d.quand < DELAI_COMMANDE_MS) return false
      derniere.current = { cle, quand: maintenant }
      return true
    }
    return {
      ...q,
      choisirOption: (option, cibles) => {
        if (ouvrir(`option:${option.id}`)) q.choisirOption(option, cibles)
      },
      interaction: {
        ...q.interaction,
        choisirOption: (option, cibles, parGeste) => {
          if (ouvrir(`option:${option.id}`)) q.interaction.choisirOption(option, cibles, parGeste)
        },
        valider: () => {
          if (ouvrir('valider')) q.interaction.valider()
        },
        annuler: () => {
          if (ouvrir('annuler')) q.interaction.annuler()
        },
      },
    }
  }, [q, actif])
}

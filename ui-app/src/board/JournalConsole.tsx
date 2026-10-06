/**
 * Le journal de la CONSOLE : compact, une ligne par fait, les outils rangés
 * dans un menu « ⋯ » (choix de l'utilisateur, 03/10/2026 : « beaucoup trop de
 * détail et beaucoup trop haut »). Le journal du héros y reste accessible.
 */
import { useEffect, useRef, useState, type ReactNode } from 'react'
import { t } from './langue'
import { avecIcones } from './icones-ressources'
import { BoutonsRapportBug, type OutilsRapport } from './RapportBug'
import type { EntreeHistorique } from './HistoriquePartie'
import { lignesCompactes } from './journal-compact'
import { TexteAvecCartes } from './NomsDeCartes'
import './JournalConsole.css'

export function JournalConsole({
  entrees,
  effacer,
  rapport,
  telechargerLog,
  journalHeros,
  revuePhase,
  onRevoirPhase,
}: {
  entrees: EntreeHistorique[]
  effacer: () => void
  rapport?: OutilsRapport
  telechargerLog: () => void
  journalHeros: ReactNode
  /**
   * « Revoir la phase du méchant » (03/10/2026) : la derniere phase finie, en
   * lecture seule (RevuePhase). Absente tant qu'il n'y en a pas.
   */
  revuePhase?: ReactNode
  /**
   * Scene PC (D38, refonte du 04/10/2026) : le bouton rouvre la phase dans le
   * cartouche du bas, en relecture, et le journal reste le journal. Prend le
   * pas sur `revuePhase`.
   */
  onRevoirPhase?: () => void
}) {
  const [vue, setVue] = useState<'historique' | 'heros' | 'phase'>('historique')
  const [menu, setMenu] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!menu) return
    const fermer = (evenement: PointerEvent) => {
      if (evenement.target instanceof Node && ref.current?.contains(evenement.target)) return
      setMenu(false)
    }
    document.addEventListener('pointerdown', fermer)
    return () => document.removeEventListener('pointerdown', fermer)
  }, [menu])

  const lignes = lignesCompactes(entrees)

  return (
    <section className="journal-console" aria-label={t('Journal de la partie')}>
      <header className="jc-tete" ref={ref}>
        <strong>
          {vue === 'historique' ? t('Journal') : vue === 'phase' ? t('Phase du méchant') : t('Journal du héros')}
        </strong>
        {revuePhase || onRevoirPhase ? (
          <button
            type="button"
            className="jc-revue-bouton"
            onClick={() => {
              if (onRevoirPhase) {
                onRevoirPhase()
                return
              }
              setVue(vue === 'phase' ? 'historique' : 'phase')
            }}
          >
            {vue === 'phase' ? t('Retour au journal') : t('Revoir la phase du méchant')}
          </button>
        ) : null}
        <button
          type="button"
          className="jc-menu-bouton"
          aria-haspopup="menu"
          aria-expanded={menu}
          title={t('Outils du journal')}
          onClick={() => setMenu((m) => !m)}
        >
          ⋯
        </button>
        {menu ? (
          <div className="jc-menu" role="menu">
            <button
              type="button"
              role="menuitem"
              onClick={() => {
                setVue(vue === 'historique' ? 'heros' : 'historique')
                setMenu(false)
              }}
            >
              {vue === 'historique' ? t('Journal du héros') : t('Journal de la partie')}
            </button>
            <button
              type="button"
              role="menuitem"
              onClick={() => {
                telechargerLog()
                setMenu(false)
              }}
            >
              {t('Log de la partie')}
            </button>
            {rapport ? <BoutonsRapportBug outils={rapport} /> : null}
            <button
              type="button"
              role="menuitem"
              disabled={entrees.length === 0}
              onClick={() => {
                effacer()
                setMenu(false)
              }}
            >
              {t('Effacer')}
            </button>
          </div>
        ) : null}
      </header>
      {vue === 'phase' && revuePhase ? (
        revuePhase
      ) : vue === 'heros' ? (
        journalHeros
      ) : lignes.length === 0 ? (
        <p className="jc-vide">{t('Aucune entrée pour le moment')}</p>
      ) : (
        <ol className="jc-lignes">
          {lignes.map((ligne) =>
            ligne.genre === 'round' ? (
              <li key={ligne.cle} className="jc-round">
                {t('Round')} {ligne.round}
              </li>
            ) : ligne.genre === 'phase' ? (
              <li key={ligne.cle} className={`jc-phase phase-${ligne.famille}`}>
                {ligne.famille === 'mechant' ? t('Phase du méchant') : t('Phase des joueurs')}
              </li>
            ) : (
              <li
                key={ligne.cle}
                className={`jc-fait type-${ligne.type}${ligne.famille ? ` phase-${ligne.famille}` : ''}`}
                title={ligne.detail}
              >
                <TexteAvecCartes texte={ligne.texte} cartes={ligne.cartes} />
                {ligne.detail ? <span className="jc-detail"> · {avecIcones(ligne.detail)}</span> : null}
              </li>
            )
          )}
        </ol>
      )}
    </section>
  )
}

// Le bandeau colle en haut du portrait : ou on en est, qui doit agir, le
// menu « … » et le bouton d'action principal (spec du 12/09/2026 : la barre
// du bas n'existe plus, tout le chrome tient ici).
//
// Le menu « … » ouvre une feuille basse qui contient `menu` : c'est le
// `.board-actions` du plateau PC, rendu tel quel (Annuler, Sauver,
// Historique, Options, Salon, Journal, Musique, Langue, Quitter) et mis en
// colonne par portrait.css. On ne reecrit pas ces boutons : leurs classes
// (`.bh-options`, `.bh-history`...) sont celles que le Retour Android et le
// filet Playwright connaissent.
//
// Contrairement au brief d'origine, ce composant ne calcule PAS lui-meme qui
// agit : libelleQuiAgit() a besoin de { aNous, connecte, demande }, qui ne
// sont pas dans BoardProps. Le plateau PC calcule deja ce libelle ; on le lui
// fait simplement passer.
import { useState, type ReactElement, type ReactNode } from 'react'
import { libellePhase, libelleRound } from '../etat-partie'
import { t } from '../langue'
import type { World } from '../world'
import { installer, useInstallable } from './installation'

export type ActionPrincipale = { libelle: string; suggere?: boolean; agir: () => void }

export function BandeauPortrait({
  monde,
  quiAgit,
  menu,
  actionPrincipale,
}: {
  monde: World | undefined
  quiAgit?: string
  menu?: ReactNode
  actionPrincipale?: ActionPrincipale
}): ReactElement {
  const [menuOuvert, setMenuOuvert] = useState(false)
  const installable = useInstallable()
  return (
    <header className="portrait-bandeau">
      <div className="portrait-bandeau-etat" role="status">
        <strong>{libelleRound(monde) || t('Mise en place')}</strong>
        <span>{libellePhase(monde)}</span>
        {quiAgit ? <em>{quiAgit}</em> : null}
      </div>
      {menu ? (
        <button
          type="button"
          className={`portrait-menu-bouton${menuOuvert ? ' est-actif' : ''}`}
          data-tactile="menu"
          aria-expanded={menuOuvert}
          aria-label={t('Menu')}
          onClick={() => setMenuOuvert((ouvert) => !ouvert)}
        >
          {/* Ouvert, il devient la croix qui referme tout : les feuilles
              (Options, Historique...) s'ouvrent PAR-DESSUS le menu et ne
              laissent libre que le haut de l'ecran, ou vit ce bouton. */}
          {menuOuvert ? '×' : '…'}
        </button>
      ) : null}
      {actionPrincipale ? (
        <button
          type="button"
          className={`portrait-action${actionPrincipale.suggere ? ' est-suggere' : ''}`}
          data-tactile="action"
          onClick={actionPrincipale.agir}
        >
          {actionPrincipale.libelle}
          {actionPrincipale.suggere ? ' ✓' : ''}
        </button>
      ) : null}
      {menu && menuOuvert ? (
        <>
          <div className="portrait-menu-voile" onPointerDown={() => setMenuOuvert(false)} />
          <nav className="portrait-menu" aria-label={t('Menu')}>
            <span className="portrait-menu-poignee" aria-hidden="true" />
            {menu}
            {/* Discret, au fond du menu, et seulement quand le navigateur
                accepte d'installer (zone 3, installation.ts). */}
            {installable ? (
              <button
                type="button"
                className="portrait-installer"
                onClick={() => {
                  setMenuOuvert(false)
                  void installer()
                }}
              >
                <span aria-hidden="true">⤓</span> {t('Installer l’application')}
              </button>
            ) : null}
          </nav>
        </>
      ) : null}
    </header>
  )
}

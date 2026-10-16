// « Sur la table », sans modale (16/10/2026, demande de l'utilisateur) : « tout s'active
// sur la table et on clique tout sur la table, sans avoir une modale en plus ».
//
// Deux pièces, et rien d'autre :
//  - la CARTE QUI AGIT porte un halo doré et se clique pour passer à la suite ;
//  - une ligne fine en haut de la table dit ce qui se passe, en une phrase.
// Aucune boîte ne flotte au milieu du plateau.
//
// Tout est dans le repère du cadre du plateau (voir `mesures-plateau.ts`), comme le trait
// et les cartes sorties du paquet : ce composant se rend par le même portail.
import { useEffect, useState, type ReactNode } from 'react'
import { boiteDeCarte, cadreDuPlateau, type Boite } from './mesures-plateau'
import { t } from './langue'

/** Le rectangle de la carte, remesuré tant qu'elle bouge (vol, mise à l'échelle). */
export function useBoiteDeCarte(carteId: number | undefined, cle: string): Boite | undefined {
  const [boite, setBoite] = useState<Boite | undefined>(undefined)
  useEffect(() => {
    const mesurer = () => {
      const cadre = cadreDuPlateau()
      const b = cadre ? boiteDeCarte(carteId, cadre) : undefined
      setBoite((avant) =>
        avant && b && avant.x === b.x && avant.y === b.y && avant.w === b.w && avant.h === b.h ? avant : b
      )
    }
    mesurer()
    const minuteur = window.setInterval(mesurer, 120)
    window.addEventListener('resize', mesurer)
    return () => {
      window.clearInterval(minuteur)
      window.removeEventListener('resize', mesurer)
    }
  }, [carteId, cle])
  return boite
}

export type TableSansModaleProps = {
  /** La carte qui agit ; à défaut, celle qui subit (la menace n'a pas d'auteur). */
  acteurId: number | undefined
  /** La carte qui subit : un anneau rouge discret, pour comprendre qui reçoit. */
  cibleId: number | undefined
  /** Change à chaque étape : relance la mesure. */
  cle: string
  /** Ce qui se passe, noms survolables. */
  phrase: ReactNode
  /** Le nombre qui compte (« 2 dégâts »). */
  nombre?: string
  /** Faux pour l'étape d'un autre joueur ou en spectateur : rien à cliquer. */
  peutAgir: boolean
  avancer: () => void
  reculer?: () => void
  /** Ce qu'on attend, quand la suite n'est pas à nous (« La suite arrive… »). */
  mention?: string
  /** Texte accessible du clic sur la carte. */
  libelleAction: string
}

export function TableSansModale({
  acteurId,
  cibleId,
  cle,
  phrase,
  nombre,
  peutAgir,
  avancer,
  reculer,
  mention,
  libelleAction,
}: TableSansModaleProps) {
  const boiteActeur = useBoiteDeCarte(acteurId ?? cibleId, cle)
  const boiteCible = useBoiteDeCarte(acteurId !== undefined ? cibleId : undefined, cle)
  // Une étape sans carte à cliquer (« Aucun sbire engagé », menace sans manigance visible) :
  // la ligne du haut porte alors son propre bouton. On laisse 300 ms à la mesure.
  const [laisseMesurer, setLaisseMesurer] = useState(true)
  useEffect(() => {
    setLaisseMesurer(true)
    const minuteur = window.setTimeout(() => setLaisseMesurer(false), 300)
    return () => window.clearTimeout(minuteur)
  }, [cle])
  const sansCarte = !boiteActeur && (acteurId === undefined && cibleId === undefined ? true : !laisseMesurer)
  return (
    <>
      <div className="tsm-bandeau" role="status" aria-live="polite">
        {reculer ? (
          <button type="button" className="tsm-retour" onClick={reculer} aria-label={t('Précédent')} title={t('Précédent')}>
            ‹
          </button>
        ) : null}
        <span className="tsm-phrase">{phrase}</span>
        {nombre ? <b className="tsm-nombre">{nombre}</b> : null}
        {peutAgir && sansCarte ? (
          <button type="button" className="tsm-bouton" onClick={avancer} aria-label={libelleAction}>
            {t('Continuer')}
          </button>
        ) : (
          <span className="tsm-consigne">
            {peutAgir ? t('Clique la carte dorée pour continuer') : (mention ?? t('La suite arrive…'))}
          </span>
        )}
      </div>
      {boiteCible ? <span className="tsm-cible" style={boiteStyle(boiteCible)} aria-hidden="true" /> : null}
      {boiteActeur ? (
        <button
          type="button"
          className={`tsm-acteur${peutAgir ? '' : ' est-inactif'}`}
          style={boiteStyle(boiteActeur)}
          onClick={peutAgir ? avancer : undefined}
          disabled={!peutAgir}
          aria-label={libelleAction}
          title={libelleAction}
        />
      ) : null}
    </>
  )
}

function boiteStyle(b: Boite) {
  return { left: `${b.x}px`, top: `${b.y}px`, width: `${b.w}px`, height: `${b.h}px` }
}

export type ChoixSurTable = {
  id: number
  /** Le libellé court de l'étiquette (« Défendre avec Spider-Man »). */
  nom: string
  /** La carte qui porte ce choix : elle s'allume et se clique. Sans carte, le choix va dans la ligne du haut. */
  carteId?: number
  indisponible?: string
  choisir: () => void
  survoler?: (actif: boolean) => void
}

/**
 * La QUESTION du moteur, sans fenêtre : les cartes qui peuvent répondre s'allument en vert,
 * une étiquette collée dessous dit ce que le clic fait ; les choix sans carte
 * (« Ne pas défendre ») sont des boutons de la ligne du haut.
 */
export function QuestionSurTable({
  phrase,
  choix,
  refus,
}: {
  phrase: ReactNode
  choix: ChoixSurTable[]
  refus?: { libelle: string; agir: () => void; survoler?: (actif: boolean) => void }
}) {
  const surCarte = choix.filter((c) => c.carteId !== undefined)
  const enLigne = choix.filter((c) => c.carteId === undefined)
  return (
    <>
      <div className="tsm-bandeau est-question" role="group" aria-label={t('Ta décision')}>
        <span className="tsm-phrase">{phrase}</span>
        {enLigne.map((c) => (
          <button
            key={c.id}
            type="button"
            className="tsm-bouton"
            disabled={!!c.indisponible}
            title={c.indisponible}
            onClick={c.choisir}
          >
            {c.nom}
          </button>
        ))}
        {refus ? (
          <button
            type="button"
            className="tsm-bouton est-refus"
            onClick={refus.agir}
            onMouseEnter={() => refus.survoler?.(true)}
            onMouseLeave={() => refus.survoler?.(false)}
          >
            {refus.libelle}
          </button>
        ) : null}
      </div>
      {surCarte.map((c) => (
        <PuceSurCarte key={c.id} choix={c} />
      ))}
    </>
  )
}

function PuceSurCarte({ choix }: { choix: ChoixSurTable }) {
  const boite = useBoiteDeCarte(choix.carteId, String(choix.id))
  if (!boite) return null
  const bloque = !!choix.indisponible
  return (
    <>
      <button
        type="button"
        className={`tsm-utilisable${bloque ? ' est-inactif' : ''}`}
        style={boiteStyle(boite)}
        disabled={bloque}
        aria-label={choix.nom}
        title={choix.indisponible ?? choix.nom}
        onClick={choix.choisir}
        onMouseEnter={() => choix.survoler?.(true)}
        onMouseLeave={() => choix.survoler?.(false)}
      />
      <button
        type="button"
        className={`tsm-etiquette${bloque ? ' est-inactif' : ''}`}
        style={{ left: `${boite.x + boite.w / 2}px`, top: `${boite.y + boite.h + 6}px` }}
        disabled={bloque}
        onClick={choix.choisir}
      >
        {choix.nom}
      </button>
    </>
  )
}

/** Le bilan de fin de phase, sans fenêtre : une ligne fine, une pastille par fait, un bouton. */
export function BilanSurTable({
  titre,
  lignes,
  vide,
  peutAgir,
  avancer,
  reculer,
  mention,
}: {
  titre: string
  lignes: Array<{ cle: string; texte: string; compteur?: string }>
  vide?: string
  peutAgir: boolean
  avancer: () => void
  reculer?: () => void
  mention?: string
}) {
  return (
    <div className="tsm-bandeau est-bilan" role="status" aria-live="polite">
      {reculer ? (
        <button type="button" className="tsm-retour" onClick={reculer} aria-label={t('Précédent')} title={t('Précédent')}>
          ‹
        </button>
      ) : null}
      <b className="tsm-titre">{titre}</b>
      {lignes.length === 0 ? (
        <span className="tsm-phrase">{vide}</span>
      ) : (
        <span className="tsm-pastilles">
          {lignes.map((ligne) => (
            <span key={ligne.cle} className="tsm-pastille">
              {ligne.texte}
              {ligne.compteur ? <small> {ligne.compteur}</small> : null}
            </span>
          ))}
        </span>
      )}
      {peutAgir ? (
        <button type="button" className="tsm-bouton" onClick={avancer}>
          {t('Terminer la phase')}
        </button>
      ) : (
        <span className="tsm-consigne">{mention ?? t('La suite arrive…')}</span>
      )}
    </div>
  )
}

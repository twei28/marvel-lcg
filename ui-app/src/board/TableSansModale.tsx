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
/**
 * Le rectangle de l'IMAGE de la carte, pas de son bloc entier : le bloc compte aussi la pastille
 * de type au-dessus et la barre de PV dessous, et les cadres lumineux débordaient (« pas du tout
 * bien centrés », 16/10/2026).
 */
function boiteDeLImage(
  id: number | undefined,
  cadre: { element: HTMLElement; origine: DOMRect }
): Boite | undefined {
  if (id === undefined) return undefined
  // Une carte rencontre RÉVÉLÉE est montrée en grand à côté du paquet, et sa copie face cachée reste
  // sur la table : le halo va sur celle qu'on lit (« qu'on comprenne bien quelle est la carte de
  // rencontre », 16/10/2026).
  const el =
    cadre.element.querySelector<HTMLElement>(`.rencontre-sortie.est-revelee .scan-card[data-card-id="${id}"] .scan-frame`) ??
    cadre.element.querySelector<HTMLElement>(`.scan-card[data-card-id="${id}"] .scan-frame`)
  if (!el) return boiteDeCarte(id, cadre)
  const r = el.getBoundingClientRect()
  if (r.width === 0 || r.height === 0) return boiteDeCarte(id, cadre)
  return { x: r.left - cadre.origine.left, y: r.top - cadre.origine.top, w: r.width, h: r.height }
}

export function useBoiteDeCarte(carteId: number | undefined, cle: string): Boite | undefined {
  const [boite, setBoite] = useState<Boite | undefined>(undefined)
  useEffect(() => {
    const mesurer = () => {
      const cadre = cadreDuPlateau()
      const b = cadre ? boiteDeLImage(carteId, cadre) : undefined
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
  /** Avant la phrase, en rouge : d'où vient cette carte (« Renfort de Pris par Surprise »). */
  surtitre?: string
  /** Après la phrase : ce qui va suivre (« Renfort : une autre carte va être révélée »). */
  suite?: string
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
  surtitre,
  suite,
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
      <span className="tsm-depart" aria-hidden="true" />
      <div className="tsm-bandeau" role="status" aria-live="polite">
        {reculer ? (
          <button type="button" className="tsm-retour" onClick={reculer} aria-label={t('Précédent')} title={t('Précédent')}>
            ‹
          </button>
        ) : null}
        {surtitre ? <span className="tsm-surtitre">{surtitre}</span> : null}
        <span className="tsm-phrase">{phrase}</span>
        {nombre ? <b className="tsm-nombre">{nombre}</b> : null}
        {suite ? <span className="tsm-suite">{suite}</span> : null}
        {peutAgir && sansCarte ? (
          <button type="button" className="tsm-bouton" onClick={avancer} aria-label={libelleAction}>
            {t('Continuer')}
          </button>
        ) : (
          <span className="tsm-consigne">
            {peutAgir ? t('Clique la carte dorée, ou Espace') : (mention ?? t('La suite arrive…'))}
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
  // Une carte qu'on ne trouve pas sur la table (hors du cadre, disparue) ne doit JAMAIS rendre son
  // choix injouable : il passe alors dans la ligne du haut, comme un choix sans carte.
  const [absentes, setAbsentes] = useState<ReadonlySet<number>>(new Set())
  const signaler = (id: number, absente: boolean) =>
    setAbsentes((avant) => {
      if (avant.has(id) === absente) return avant
      const suivant = new Set(avant)
      if (absente) suivant.add(id)
      else suivant.delete(id)
      return suivant
    })
  // UN SEUL CHOIX POSSIBLE (16/10/2026) : on n'est pas obligé de cliquer, Espace le prend. S'il y
  // en a plusieurs, rien ne se choisit au clavier : on clique la carte voulue.
  const possibles = choix.filter((c) => !c.indisponible)
  const uniqueId = possibles.length + (refus ? 1 : 0) === 1 ? (refus ? 'refus' : possibles[0]!.id) : undefined
  const surCarte = choix.filter((c) => c.carteId !== undefined && !absentes.has(c.id))
  const enLigne = choix.filter((c) => c.carteId === undefined || absentes.has(c.id))
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
            data-choix-unique={uniqueId === c.id ? '' : undefined}
          >
            {c.nom}
            {uniqueId === c.id ? <kbd className="tsm-touche">{t('Espace')}</kbd> : null}
          </button>
        ))}
        {refus ? (
          <button
            type="button"
            className="tsm-bouton est-refus"
            onClick={refus.agir}
            onMouseEnter={() => refus.survoler?.(true)}
            onMouseLeave={() => refus.survoler?.(false)}
            data-choix-unique={uniqueId === 'refus' ? '' : undefined}
          >
            {refus.libelle}
            {uniqueId === 'refus' ? <kbd className="tsm-touche">{t('Espace')}</kbd> : null}
          </button>
        ) : null}
      </div>
      {/* Les cartes pas encore mesurées : on les surveille pour pouvoir les rabattre en ligne. */}
      {choix
        .filter((c) => c.carteId !== undefined && absentes.has(c.id))
        .map((c) => (
          <VeilleCarte key={`veille-${c.id}`} choix={c} signaler={signaler} />
        ))}
      {surCarte.map((c) => (
        <PuceSurCarte key={c.id} choix={c} signaler={signaler} unique={uniqueId === c.id} />
      ))}
    </>
  )
}

/** Surveille une carte rabattue en ligne : si elle reparaît sur la table, elle reprend sa place. */
function VeilleCarte({ choix, signaler }: { choix: ChoixSurTable; signaler: (id: number, absente: boolean) => void }) {
  const boite = useBoiteDeCarte(choix.carteId, String(choix.id))
  useEffect(() => {
    if (boite) signaler(choix.id, false)
  }, [boite, choix.id, signaler])
  return null
}

function PuceSurCarte({
  choix,
  signaler,
  unique,
}: {
  choix: ChoixSurTable
  signaler: (id: number, absente: boolean) => void
  unique: boolean
}) {
  const boite = useBoiteDeCarte(choix.carteId, String(choix.id))
  // 600 ms de mesure avant de rabattre le choix en ligne : la carte peut encore voler.
  useEffect(() => {
    if (boite) return
    const minuteur = window.setTimeout(() => signaler(choix.id, true), 600)
    return () => window.clearTimeout(minuteur)
  }, [boite, choix.id, signaler])
  if (!boite) return null
  const hauteurTable = cadreDuPlateau()?.boite.h ?? Number.POSITIVE_INFINITY
  const enBas = boite.y + boite.h + 44 > hauteurTable
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
        style={
          // Une carte de la MAIN touche le bas de la table : l'étiquette passe au-dessus.
          enBas
            ? { left: `${boite.x + boite.w / 2}px`, top: `${boite.y - 6}px`, transform: 'translate(-50%, -100%)' }
            : { left: `${boite.x + boite.w / 2}px`, top: `${boite.y + boite.h + 6}px` }
        }
        disabled={bloque}
        onClick={choix.choisir}
        data-choix-unique={unique ? '' : undefined}
      >
        {choix.nom}
        {unique ? <kbd className="tsm-touche">{t('Espace')}</kbd> : null}
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
  bouton,
  defaite,
}: {
  titre: string
  lignes: Array<{ cle: string; texte: string; compteur?: string }>
  vide?: string
  peutAgir: boolean
  avancer: () => void
  reculer?: () => void
  mention?: string
  /** Le libellé du bouton (« Terminer la phase » par défaut). */
  bouton?: string
  /** Une ligne de défaite : le bandeau passe au rouge. */
  defaite?: boolean
}) {
  return (
    <div className={`tsm-bandeau est-bilan${defaite ? ' est-defaite' : ''}`} role="status" aria-live="polite">
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
          {bouton ?? t('Terminer la phase')}
        </button>
      ) : (
        <span className="tsm-consigne">{mention ?? t('La suite arrive…')}</span>
      )}
    </div>
  )
}

export type CibleSurTable = {
  id: number
  choisie: boolean
  /** Rang dans une sélection ordonnée (1, 2…) : le gros numéro posé sur la carte. */
  ordre?: number
  fois?: number
  /** Ce que fait le clic, écrit sous la carte : une PILE à ouvrir (« Chercher dans le deck »). */
  etiquette?: string
  agir: () => void
}

/**
 * Le CIBLAGE d'une action, sans fenêtre (16/10/2026) : les cartes qu'on peut viser brillent en vert,
 * un clic les choisit, et quand la sélection est ordonnée un gros numéro (1, 2…) se pose sur chacune.
 * La ligne du haut dit ce qu'on choisit, compte (n/max), et porte « Valider » et « Annuler ».
 */
export function CiblageSurTable({
  titre,
  choisies,
  maximum,
  cibles,
  prete,
  raison,
  valider,
  annuler,
}: {
  titre: string
  choisies: number
  maximum: number
  cibles: CibleSurTable[]
  prete: boolean
  raison: string
  valider: () => void
  annuler?: () => void
}) {
  return (
    <>
      <div className="tsm-bandeau est-question" role="group" aria-label={t('Ta décision')}>
        <span className="tsm-phrase">
          <b>{titre}</b>
          {maximum > 0 ? <span className="tsm-compte"> {choisies}/{maximum}</span> : null}
        </span>
        <button
          type="button"
          className="tsm-bouton"
          disabled={!prete}
          title={prete ? undefined : raison}
          onClick={valider}
          data-choix-unique={prete ? '' : undefined}
        >
          {t('Valider')}
          {prete ? <kbd className="tsm-touche">{t('Espace')}</kbd> : null}
        </button>
        {annuler ? (
          <button type="button" className="tsm-bouton est-refus" onClick={annuler}>
            {t('Annuler')}
          </button>
        ) : null}
      </div>
      {cibles.map((c) => (
        <CarteCiblable key={c.id} cible={c} />
      ))}
    </>
  )
}

function CarteCiblable({ cible }: { cible: CibleSurTable }) {
  const boite = useBoiteDeCarte(cible.id, 'cible')
  if (!boite) return null
  return (
    <>
      <button
        type="button"
        className={`tsm-utilisable${cible.choisie ? ' est-choisie' : ''}`}
        style={boiteStyle(boite)}
        onClick={cible.agir}
        aria-pressed={cible.choisie}
        aria-label={cible.etiquette}
      />
      {cible.etiquette ? (
        <button
          type="button"
          className="tsm-etiquette"
          style={
            boite.y + boite.h + 44 > (cadreDuPlateau()?.boite.h ?? Number.POSITIVE_INFINITY)
              ? { left: `${boite.x + boite.w / 2}px`, top: `${boite.y - 6}px`, transform: 'translate(-50%, -100%)' }
              : { left: `${boite.x + boite.w / 2}px`, top: `${boite.y + boite.h + 6}px` }
          }
          onClick={cible.agir}
        >
          {cible.etiquette}
        </button>
      ) : null}
      {cible.ordre !== undefined || (cible.fois ?? 0) > 1 ? (
        <span
          className="tsm-numero"
          style={{ left: `${boite.x + boite.w / 2}px`, top: `${boite.y + boite.h / 2}px` }}
          aria-hidden="true"
        >
          {cible.ordre ?? `×${cible.fois}`}
        </span>
      ) : null}
    </>
  )
}

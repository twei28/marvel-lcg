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
import { useEffect, useState, type CSSProperties, type ReactNode } from 'react'
import { boiteDeCarte, cadreDuPlateau, redresserBoite, type Boite } from './mesures-plateau'
import { t } from './langue'
import type { PiedMulti } from './CartouchePhase'
import type { PhaseLecture } from './CoucheRencontreSurTable'

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
  // Une carte rencontre RÉVÉLÉE est montrée en grand au centre, et sa copie face cachée reste
  // sur la table : le halo va sur celle qu'on lit (« qu'on comprenne bien quelle est la carte de
  // rencontre », 16/10/2026).
  const el =
    cadre.element.querySelector<HTMLElement>(`.rencontre-sortie.est-revelee .scan-card[data-card-id="${id}"] .scan-frame`) ??
    cadre.element.querySelector<HTMLElement>(`.scan-card[data-card-id="${id}"] .scan-frame`)
  if (!el) return boiteDeCarte(id, cadre)
  const r = el.getBoundingClientRect()
  if (r.width === 0 || r.height === 0) return boiteDeCarte(id, cadre)
  const bloc = el.closest<HTMLElement>('.scan-card')?.getBoundingClientRect()
  const englobante: Boite = {
    x: r.left - cadre.origine.left,
    y: r.top - cadre.origine.top,
    w: r.width,
    h: r.height,
    // Le bloc de la carte compte la barre de PV sous l'image : l'etiquette « Defendre avec X » se pose
    // SOUS elle au lieu de la cacher (19/10/2026).
    bas: Math.max(r.bottom, bloc ? bloc.bottom : 0) - cadre.origine.top,
  }
  // UNE CARTE INCLINEE (epuisee : 8 degres) : le cadre doré s'incline avec elle au lieu de rester droit autour
  // de sa boite englobante (18/10/2026). L'angle se lit sur la carte et ses parents, sa taille de mise en page
  // (offsetWidth/Height) ne change pas avec la rotation.
  const angle = angleDeLElement(el, cadre.element)
  return angle ? { ...redresserBoite(englobante, el.offsetWidth, el.offsetHeight, angle), bas: englobante.bas } : englobante
}

/** L'angle total (degres) de l'element et de ses parents jusqu'au cadre, lu sur leurs transformations. */
function angleDeLElement(el: HTMLElement, racine: HTMLElement): number {
  let total = 0
  for (let e: HTMLElement | null = el; e && e !== racine; e = e.parentElement) {
    const transform = getComputedStyle(e).transform
    if (!transform || transform === 'none') continue
    try {
      const m = new DOMMatrixReadOnly(transform)
      total += (Math.atan2(m.b, m.a) * 180) / Math.PI
    } catch {
      /* transformation illisible : on la laisse droite */
    }
  }
  return Math.abs(total) < 0.05 ? 0 : total
}

export function useBoiteDeCarte(carteId: number | undefined, cle: string): Boite | undefined {
  const [boite, setBoite] = useState<Boite | undefined>(undefined)
  useEffect(() => {
    if (carteId === undefined) { setBoite(undefined); return }
    const mesurer = () => {
      const cadre = cadreDuPlateau()
      const b = cadre ? boiteDeLImage(carteId, cadre) : undefined
      setBoite((avant) =>
        avant && b && avant.x === b.x && avant.y === b.y && avant.w === b.w && avant.h === b.h && avant.angle === b.angle && avant.bas === b.bas ? avant : b
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
  calcul?: string
  lecture?: PhaseLecture
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
  calcul,
  lecture,
  peutAgir,
  avancer,
  reculer,
  mention,
  libelleAction,
  surtitre,
  suite,
}: TableSansModaleProps) {
  // La carte au centre se lit sans rechercher un halo derrière elle. Aucun
  // intervalle de mesure ni rendu des halos pendant ses déplacements.
  const boiteActeur = useBoiteDeCarte(lecture ? undefined : acteurId ?? cibleId, cle)
  const boiteCible = useBoiteDeCarte(!lecture && acteurId !== undefined ? cibleId : undefined, cle)
  const enTrajet = lecture === 'entree' || lecture === 'depart'
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
        {calcul ? <span className="tsm-calcul">{calcul}</span> : null}
        {suite ? <span className="tsm-suite">{suite}</span> : null}
        {peutAgir && (sansCarte || lecture) ? (
          <button type="button" className="tsm-bouton" onClick={avancer} aria-label={libelleAction} disabled={enTrajet}>
            {t('Continuer')}
            {lecture === 'lecture' ? <kbd className="tsm-touche">{t('Espace')}</kbd> : null}
          </button>
        ) : (
          <span className="tsm-consigne">
            {peutAgir ? t('Clique la carte dorée, ou Espace') : (mention ?? t('La suite arrive…'))}
          </span>
        )}
        {enTrajet ? <span className="tsm-attente">{lecture === 'entree' ? t('Les cartes arrivent…') : t('Les cartes se placent…')}</span> : null}
      </div>
      {!lecture && boiteCible ? <span className="tsm-cible" style={boiteStyle(boiteCible)} aria-hidden="true" /> : null}
      {!lecture && boiteActeur ? (
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

/**
 * L'etiquette d'une carte a EXACTEMENT la largeur de la carte (19/10/2026) : jamais plus large, donc plus de
 * chevauchement entre voisines. Le nom se coupe sur deux lignes puis par des points de suspension (le nom entier
 * reste dans l'infobulle et dans le libelle accessible) ; la police suit la largeur. Posee SOUS la barre de PV
 * (`bas`), ou AU-DESSUS de la carte quand elle touche le bas de la table.
 */
function styleEtiquette(b: Boite, auDessus: boolean): CSSProperties {
  const base: CSSProperties = {
    left: `${b.x}px`,
    width: `${b.w}px`,
    fontSize: `${Math.max(10, Math.min(16, b.w / 6.4))}px`,
  }
  return auDessus
    ? { ...base, top: `${b.y - 4}px`, transform: 'translateY(-100%)' }
    : { ...base, top: `${Math.max(b.y + b.h, b.bas ?? 0) + 3}px` }
}

/** « Défendre avec Spider-Man » : le verbe en petit sur une ligne, le nom dessous (deux lignes au plus, puis « … »). */
function TexteEtiquette({ nom }: { nom: string }) {
  const verbe = `${t('Défendre avec')} `
  if (!nom.startsWith(verbe) || nom.length === verbe.length) return <span className="tsm-etiquette-texte">{nom}</span>
  return (
    <>
      <span className="tsm-etiquette-verbe">{verbe.trim()}</span>
      <span className="tsm-etiquette-texte">{nom.slice(verbe.length)}</span>
    </>
  )
}

function boiteStyle(b: Boite) {
  return {
    left: `${b.x}px`,
    top: `${b.y}px`,
    width: `${b.w}px`,
    height: `${b.h}px`,
    ...(b.angle ? { transform: `rotate(${b.angle}deg)` } : {}),
  }
}

export type ChoixSurTable = {
  id: number
  /** Le libellé court de l'étiquette (« Défendre avec Spider-Man »). */
  nom: string
  /** La carte qui porte ce choix : elle s'allume et se clique. Sans carte, le choix va dans la ligne du haut. */
  carteId?: number
  /** Une amélioration dans une pile se choisit aussi par son nom, sans viser une tranche. */
  enLigne?: boolean
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
  const [soulignee, setSoulignee] = useState<number>()
  const signatureChoix = choix.map((c) => `${c.id}:${c.carteId}`).join(',')
  useEffect(() => { setSoulignee(undefined) }, [signatureChoix])
  const survoler = (c: ChoixSurTable, actif: boolean) => {
    setSoulignee(actif ? c.carteId : undefined)
    c.survoler?.(actif)
  }
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
  const surCarte = choix.filter((c) => !c.enLigne && c.carteId !== undefined && !absentes.has(c.id))
  const enLigne = choix.filter((c) => c.enLigne || c.carteId === undefined || absentes.has(c.id))
  return (
    <>
      {soulignee !== undefined ? <style>{`
        .plateau-cadre .scan-card[data-card-id="${soulignee}"]:not(.carte-apercu *) .scan-frame {
          box-shadow: 0 0 0 3px #4fd17b, 0 0 18px rgba(79, 209, 123, .7) !important;
        }
        .plateau-cadre .est-attachee:has(.scan-card[data-card-id="${soulignee}"]),
        .plateau-cadre .plateau-unite:has(.scan-card[data-card-id="${soulignee}"]) { z-index: 110 !important; }
      `}</style> : null}
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
            onMouseEnter={() => survoler(c, true)}
            onMouseLeave={() => survoler(c, false)}
            onFocus={() => survoler(c, true)}
            onBlur={() => survoler(c, false)}
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
        .filter((c) => !c.enLigne && c.carteId !== undefined && absentes.has(c.id))
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
        style={styleEtiquette(boite, enBas)}
        disabled={bloque}
        title={choix.nom}
        onClick={choix.choisir}
        data-choix-unique={unique ? '' : undefined}
      >
        <TexteEtiquette nom={choix.nom} />
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
          style={styleEtiquette(boite, boite.y + boite.h + 44 > (cadreDuPlateau()?.boite.h ?? Number.POSITIVE_INFINITY))}
          title={cible.etiquette}
          onClick={cible.agir}
        >
          <TexteEtiquette nom={cible.etiquette} />
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

/** Commandes communes aux étapes et au bilan, indépendantes des cartes du joueur visé. */
export function CommandesMultiSurTable({ multi, enTrajet }: { multi?: PiedMulti; enTrajet: boolean }) {
  if (!multi) return null
  return <div className="tsm-multi" role="group" aria-label={t('Qui fait avancer la phase du méchant ?')}>
    {multi.genre === 'choix-hote' ? <>
      <span>{t('Qui fait avancer la phase du méchant ?')}</span>
      {([['concerne', 'Le joueur concerné'], ['tous', 'Tout le monde valide'], ['quiconque', 'N’importe qui']] as const).map(([valeur, nom]) =>
        <button key={valeur} type="button" className="tsm-bouton" data-politique={valeur} onClick={() => multi.choisir(valeur)}>{t(nom)}</button>)}
    </> : multi.genre === 'pret' ? <>
      {multi.pastilles.map((p) => <span key={p.nom} title={p.nom} style={{ color: p.couleur }}>{p.pret ? '●' : '○'} {p.nom}</span>)}
      <button type="button" className="tsm-bouton" data-pret="" disabled={multi.pret || enTrajet} onClick={multi.marquer}>{t('Prêt')} · {multi.pastilles.filter((p) => p.pret).length} / {multi.pastilles.length}</button>
    </> : <span>{multi.genre === 'regarde' ? `${multi.nom} — ${t('La suite arrive…')}` : t('Qui fait avancer la phase du méchant ?')}</span>}
  </div>
}

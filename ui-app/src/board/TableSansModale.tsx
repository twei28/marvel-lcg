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
import { useCallback, useEffect, useLayoutEffect, useRef, useState, type CSSProperties, type HTMLAttributes, type KeyboardEvent as ClavierReact, type PointerEvent as PointeurReact, type ReactNode } from 'react'
import { boiteDeCarte, cadreDuPlateau, redresserBoite, type Boite } from './mesures-plateau'
import { t } from './langue'
import { ScanCard, type ScanCardProps } from '../components/ScanCard'
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
  const blocEl = el.closest<HTMLElement>('.scan-card')
  const bloc = blocEl?.getBoundingClientRect()
  // Une carte inclinee tourne aussi sa barre de PV : on prend le point le plus bas de tout ce que le bloc contient.
  const basContenu = blocEl ? Math.max(0, ...Array.from(blocEl.querySelectorAll('*')).map((e) => e.getBoundingClientRect().bottom)) : 0
  const englobante: Boite = {
    x: r.left - cadre.origine.left,
    y: r.top - cadre.origine.top,
    w: r.width,
    h: r.height,
    // Le bloc de la carte compte la barre de PV sous l'image : l'etiquette « Defendre avec X » se pose
    // SOUS elle au lieu de la cacher (19/10/2026).
    bas: Math.max(r.bottom, bloc ? bloc.bottom : 0, basContenu) - cadre.origine.top,
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


// ---------------------------------------------------------------------------------------------------------------
// LE BANDEAU DEPLACABLE (19/10/2026). La ligne du haut peut cacher une carte qu'on veut lire : une POIGNEE visible
// (souris et doigt) la glisse ailleurs ; elle reste ENTIEREMENT dans l'ecran (dans la table, jamais sur la barre
// du haut), sa place est retenue (localStorage) d'une etape a l'autre, un double-clic sur la poignee ou le petit
// bouton de remise la ramene a sa place d'origine. Le fond du bandeau laisse passer les clics (la carte doree
// dessous reste cliquable) ; seuls ses boutons, sa poignee et les noms survolables les captent.
// ---------------------------------------------------------------------------------------------------------------
const CLE_PLACE_BANDEAU = 'marvel-tsm-bandeau-place'
type Decalage = { dx: number; dy: number }
const REPOS: Decalage = { dx: 0, dy: 0 }

function placeRetenue(): Decalage {
  try {
    const brut = JSON.parse(window.localStorage.getItem(CLE_PLACE_BANDEAU) ?? 'null') as Partial<Decalage> | null
    if (brut && Number.isFinite(brut.dx) && Number.isFinite(brut.dy)) return { dx: Number(brut.dx), dy: Number(brut.dy) }
  } catch {
    /* stockage refuse ou valeur abimee : la place d'origine */
  }
  return REPOS
}

function retenirPlace(d: Decalage) {
  try {
    if (d.dx === 0 && d.dy === 0) window.localStorage.removeItem(CLE_PLACE_BANDEAU)
    else window.localStorage.setItem(CLE_PLACE_BANDEAU, JSON.stringify(d))
  } catch {
    /* stockage refuse : la place vaut pour cet affichage */
  }
}

const SEUIL_GLISSER = 4
const PAS_CLAVIER = 16

export function BandeauDeplacable({
  className,
  children,
  ...reste
}: { className: string; children: ReactNode } & Omit<HTMLAttributes<HTMLDivElement>, 'className' | 'children'>) {
  const ref = useRef<HTMLDivElement>(null)
  const [decalage, setDecalage] = useState<Decalage>(placeRetenue)
  /** Le decalage reellement pose (apres cadrage), en px de la mise en page du bandeau. */
  const pose = useRef<Decalage>(REPOS)
  const geste = useRef<{ x: number; y: number; base: Decalage } | null>(null)

  /** Ramene `voulu` pour que le bandeau reste entier dans la table ET dans l'ecran. */
  const cadrer = useCallback((voulu: Decalage): Decalage => {
    const el = ref.current
    if (!el || el.offsetWidth === 0) return voulu
    const r = el.getBoundingClientRect()
    const echelle = r.width / el.offsetWidth || 1
    const parent = (el.offsetParent as HTMLElement | null)?.getBoundingClientRect()
    const gauche = Math.max(0, parent?.left ?? 0)
    const haut = Math.max(0, parent?.top ?? 0)
    const droite = Math.min(window.innerWidth, parent?.right ?? window.innerWidth)
    const bas = Math.min(window.innerHeight, parent?.bottom ?? window.innerHeight)
    // Position sans decalage, en px d'ecran.
    const nl = r.left - pose.current.dx * echelle
    const nr = r.right - pose.current.dx * echelle
    const nt = r.top - pose.current.dy * echelle
    const nb = r.bottom - pose.current.dy * echelle
    const dx = Math.max(gauche - nl, Math.min(voulu.dx * echelle, droite - nr)) / echelle
    const dy = Math.max(haut - nt, Math.min(voulu.dy * echelle, bas - nb)) / echelle
    return { dx: Math.round(dx * 10) / 10, dy: Math.round(dy * 10) / 10 }
  }, [])

  const appliquer = useCallback(() => {
    const el = ref.current
    if (!el) return
    const net = cadrer(decalage)
    pose.current = net
    el.style.translate = net.dx === 0 && net.dy === 0 ? '' : `${net.dx}px ${net.dy}px`
    el.dataset.deplace = net.dx === 0 && net.dy === 0 ? 'non' : 'oui'
  }, [cadrer, decalage])

  // A chaque rendu (le contenu change d'une etape a l'autre), puis quand la taille de la ligne ou de la fenetre change.
  useLayoutEffect(appliquer)
  useEffect(() => {
    const el = ref.current
    if (!el) return
    const veille = typeof ResizeObserver === 'undefined' ? undefined : new ResizeObserver(appliquer)
    veille?.observe(el)
    window.addEventListener('resize', appliquer)
    return () => {
      veille?.disconnect()
      window.removeEventListener('resize', appliquer)
    }
  }, [appliquer])

  const remettre = () => {
    setDecalage(REPOS)
    retenirPlace(REPOS)
  }
  const poser = (d: Decalage) => {
    const net = cadrer(d)
    setDecalage(net)
    return net
  }

  const onPointerDown = (e: PointeurReact<HTMLButtonElement>) => {
    if (e.pointerType === 'mouse' && e.button !== 0) return
    geste.current = { x: e.clientX, y: e.clientY, base: pose.current }
    try { e.currentTarget.setPointerCapture(e.pointerId) } catch { /* sans capture : on suit quand meme */ }
  }
  const onPointerMove = (e: PointeurReact<HTMLButtonElement>) => {
    const g = geste.current
    if (!g) return
    const el = ref.current
    const echelle = el && el.offsetWidth ? el.getBoundingClientRect().width / el.offsetWidth : 1
    const dx = e.clientX - g.x
    const dy = e.clientY - g.y
    if (Math.hypot(dx, dy) < SEUIL_GLISSER) return
    poser({ dx: g.base.dx + dx / echelle, dy: g.base.dy + dy / echelle })
  }
  const fin = (e: PointeurReact<HTMLButtonElement>) => {
    if (!geste.current) return
    geste.current = null
    try { e.currentTarget.releasePointerCapture(e.pointerId) } catch { /* deja rendue */ }
    retenirPlace(pose.current)
  }
  const onKeyDown = (e: ClavierReact<HTMLButtonElement>) => {
    if (e.key === 'Escape' || e.key === 'Home') { e.preventDefault(); remettre(); return }
    const pas: Record<string, Decalage> = {
      ArrowLeft: { dx: -PAS_CLAVIER, dy: 0 }, ArrowRight: { dx: PAS_CLAVIER, dy: 0 },
      ArrowUp: { dx: 0, dy: -PAS_CLAVIER }, ArrowDown: { dx: 0, dy: PAS_CLAVIER },
    }
    const p = pas[e.key]
    if (!p) return
    e.preventDefault()
    e.stopPropagation()
    retenirPlace(poser({ dx: pose.current.dx + p.dx, dy: pose.current.dy + p.dy }))
  }
  const deplace = decalage.dx !== 0 || decalage.dy !== 0

  return (
    <div ref={ref} className={className} {...reste}>
      <button
        type="button"
        className="tsm-poignee"
        aria-label={t('Déplacer la ligne (double-clic : la remettre en place)')}
        title={t('Glisse pour déplacer la ligne ; double-clic pour la remettre en place')}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={fin}
        onPointerCancel={fin}
        onDoubleClick={remettre}
        onKeyDown={onKeyDown}
      />
      {children}
      {deplace ? (
        <button type="button" className="tsm-remise" aria-label={t('Remettre la ligne en place')} title={t('Remettre la ligne en place')} onClick={remettre} />
      ) : null}
    </div>
  )
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
  /** Les règles cachées qui jouent (une ligne discrète, T11). */
  regles?: string[]
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
  regles,
}: TableSansModaleProps) {
  // La carte au centre se lit sans rechercher un halo derrière elle. Aucun
  // intervalle de mesure ni rendu des halos pendant ses déplacements.
  const boiteActeur = useBoiteDeCarte(lecture ? undefined : acteurId ?? cibleId, cle)
  const boiteCible = useBoiteDeCarte(!lecture && acteurId !== undefined ? cibleId : undefined, cle)
  const enTrajet = lecture === 'entree' || lecture === 'depart'
  return (
    <>
      <span className="tsm-depart" aria-hidden="true" />
      <BandeauDeplacable className="tsm-bandeau" role="status" aria-live="polite">
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
        {/* « Continuer (Espace) » est TOUJOURS la, a chaque etape (19/10/2026) : plus de phrase « Clique la carte doree, ou Espace ».
            La carte doree reste cliquable. */}
        {peutAgir ? (
          <button type="button" className="tsm-bouton" onClick={avancer} aria-label={libelleAction} disabled={enTrajet}>
            {t('Continuer')}
            <kbd className="tsm-touche">{t('Espace')}</kbd>
          </button>
        ) : (
          <span className="tsm-consigne">{mention ?? t('La suite arrive…')}</span>
        )}
        {regles && regles.length > 0 ? (
          <span className="tsm-regles">
            {regles.map((ligne) => (
              <span key={ligne}>{ligne}</span>
            ))}
          </span>
        ) : null}
        {enTrajet ? <span className="tsm-attente">{lecture === 'entree' ? t('Les cartes arrivent…') : t('Les cartes se placent…')}</span> : null}
      </BandeauDeplacable>
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
  /** La carte elle-même : l'amélioration à cliquer s'étale en VRAIE carte à côté de son porteur (éventail). */
  carte?: ScanCardProps
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
  // Les ameliorations a cliquer (interruption, reponse) s'etalent en eventail a cote de leur porteur (PC).
  const enEventail = choix.filter((c) => c.enLigne && c.carte && c.carteId !== undefined && !absentes.has(c.id))
  const surCarte = choix.filter((c) => !c.enLigne && c.carteId !== undefined && !absentes.has(c.id))
  // Le bouton nomme (« Barriere energetique — Interruption ») reste dans le bandeau, quoi qu'il arrive aux cartes.
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
      <BandeauDeplacable className="tsm-bandeau est-question" role="group" aria-label={t('Ta décision')}>
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
      </BandeauDeplacable>
      {/* Les cartes pas encore mesurées : on les surveille pour pouvoir les rabattre en ligne. */}
      {choix
        .filter((c) => !c.enLigne && c.carteId !== undefined && absentes.has(c.id))
        .map((c) => (
          <VeilleCarte key={`veille-${c.id}`} choix={c} signaler={signaler} />
        ))}
      {surCarte.map((c) => (
        <PuceSurCarte key={c.id} choix={c} signaler={signaler} unique={uniqueId === c.id} />
      ))}
      {enEventail.length > 0 ? <EventailAmeliorations choix={enEventail} survoler={survoler} signaler={signaler} unique={uniqueId} /> : null}
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

// ---------------------------------------------------------------------------------------------------------------
// T14 (19/10/2026) : L'EVENTAIL DES AMELIORATIONS A CLIQUER (interruption, reponse). Empilees sous leur porteur et a
// moitie cachees, elles se choisissaient mal. Au moment du CHOIX elles s'etalent en rangee de VRAIES cartes a cote du
// porteur, entierement visibles, assez grandes pour le doigt, avec leur nom ; elles se rangent des que le choix est
// fait (le composant disparait avec la question). Le bouton nomme du bandeau reste. Le choix ne depend plus d'une
// tranche de carte visible dans la pile.
// ---------------------------------------------------------------------------------------------------------------
type Rect = { x: number; y: number; w: number; h: number }
const ECART_EVENTAIL = 8
const HAUTEUR_LIBELLE = 38

function croise(a: Rect, b: Rect, marge = 0): boolean {
  return a.x < b.x + b.w + marge && a.x + a.w + marge > b.x && a.y < b.y + b.h + marge && a.y + a.h + marge > b.y
}

/** Ou poser la rangee : a droite de la pile, sinon a gauche, au-dessus, en dessous ; jamais sur le bandeau ni hors du cadre. */
export function placerEventail(
  pile: Rect,
  total: { w: number; h: number },
  cadre: { w: number; h: number },
  interdits: Rect[],
  /** Les autres cartes de la table : on cherche d'abord une place qui n'en recouvre aucune. */
  souples: Rect[] = []
): Rect {
  const marge = 6
  const dansLeCadre = (r: Rect) => r.x >= marge && r.y >= marge && r.x + r.w <= cadre.w - marge && r.y + r.h <= cadre.h - marge
  const calage = (n: number, max: number, taille: number) => Math.max(marge, Math.min(n, max - taille - marge))
  const yAligne = calage(pile.y, cadre.h, total.h)
  const xAligne = calage(pile.x, cadre.w, total.w)
  const candidats: Rect[] = [
    { x: pile.x + pile.w + ECART_EVENTAIL, y: yAligne, w: total.w, h: total.h },
    { x: pile.x - ECART_EVENTAIL - total.w, y: yAligne, w: total.w, h: total.h },
    { x: xAligne, y: pile.y - ECART_EVENTAIL - total.h, w: total.w, h: total.h },
    { x: xAligne, y: pile.y + pile.h + ECART_EVENTAIL, w: total.w, h: total.h },
  ]
  const sansInterdit = (r: Rect) => dansLeCadre(r) && !interdits.some((i) => croise(r, i, 4)) && !croise(r, pile)
  const libre = candidats.find((r) => sansInterdit(r) && !souples.some((c) => croise(r, c)))
  if (libre) return libre
  // Une rangee decalee le long de la pile peut trouver un trou entre les cartes : on essaie des decalages.
  const decales: Rect[] = []
  for (const dy of [0, -total.h - ECART_EVENTAIL, pile.h + ECART_EVENTAIL, -(total.h / 2)]) {
    for (let x = marge; x + total.w <= cadre.w - marge; x += 24) decales.push({ x, y: calage(pile.y + dy, cadre.h, total.h), w: total.w, h: total.h })
  }
  const proche = decales
    .filter((r) => sansInterdit(r) && !souples.some((c) => croise(r, c)))
    .sort((a, b) => Math.hypot(a.x - pile.x - pile.w, a.y - pile.y) - Math.hypot(b.x - pile.x - pile.w, b.y - pile.y))[0]
  if (proche) return proche
  const sansBandeau = candidats.find(sansInterdit)
  if (sansBandeau) return sansBandeau
  // Rien de libre : le meilleur compromis, dans le cadre, qui ne recouvre pas le porteur.
  const reste = candidats.find((r) => dansLeCadre(r) && !croise(r, pile)) ?? candidats.find((r) => dansLeCadre(r))
  return reste ?? { x: calage(candidats[0]!.x, cadre.w, total.w), y: yAligne, w: total.w, h: total.h }
}

function EventailAmeliorations({
  choix,
  survoler,
  signaler,
  unique,
}: {
  choix: ChoixSurTable[]
  survoler: (c: ChoixSurTable, actif: boolean) => void
  signaler: (id: number, absente: boolean) => void
  unique: string | number | undefined
}) {
  const [place, setPlace] = useState<{ x: number; y: number; carte: number } | undefined>()
  const ids = choix.map((c) => c.carteId!).join(',')
  useEffect(() => {
    const mesurer = () => {
      const cadre = cadreDuPlateau()
      if (!cadre) { setPlace(undefined); return }
      // La pile : tout ce que l'unite du porteur dessine (porteur + ameliorations empilees).
      const premiere = cadre.element.querySelector<HTMLElement>(`.scan-card[data-card-id="${choix[0]!.carteId}"]`)
      const unite = premiere?.closest<HTMLElement>('.plateau-unite')
      if (!unite) { setPlace(undefined); return }
      let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity
      for (const f of unite.querySelectorAll<HTMLElement>('.scan-frame')) {
        if (f.closest('.est-statut')) continue
        const r = f.getBoundingClientRect()
        if (r.width === 0) continue
        x0 = Math.min(x0, r.left); y0 = Math.min(y0, r.top); x1 = Math.max(x1, r.right); y1 = Math.max(y1, r.bottom)
      }
      if (!Number.isFinite(x0)) { setPlace(undefined); return }
      const basBloc = Math.max(y1, ...Array.from(unite.querySelectorAll('.scan-card')).map((e) => e.getBoundingClientRect().bottom))
      const pile: Rect = { x: x0 - cadre.origine.left, y: y0 - cadre.origine.top, w: x1 - x0, h: basBloc - y0 }
      // La largeur d'une carte : lisible et assez large pour le doigt, mais la rangee doit tenir dans la table.
      const n = choix.length
      const largeurMax = Math.floor((cadre.boite.w - 12 - ECART_EVENTAIL * (n - 1)) / n)
      const w = Math.max(64, Math.min(112, largeurMax))
      const total = { w: n * w + ECART_EVENTAIL * (n - 1), h: Math.round((w * 176) / 127) + HAUTEUR_LIBELLE }
      const interdits: Rect[] = []
      const bandeau = document.querySelector<HTMLElement>('.tsm-bandeau.est-question')?.getBoundingClientRect()
      if (bandeau) interdits.push({ x: bandeau.left - cadre.origine.left, y: bandeau.top - cadre.origine.top, w: bandeau.width, h: bandeau.height })
      // L'apercu au survol s'ouvre a DROITE de la fenetre (souris seulement) : la rangee reste a gauche de sa place.
      if (window.matchMedia?.('(hover: hover)').matches) {
        const largeurApercu = Math.min(380, cadre.boite.w * 0.3)
        interdits.push({ x: cadre.boite.w - largeurApercu, y: 0, w: largeurApercu, h: cadre.boite.h })
      }
      const souples: Rect[] = []
      for (const f of cadre.element.querySelectorAll<HTMLElement>('.scan-card .scan-frame')) {
        if (unite.contains(f) || f.closest('.tsm-eventail, .carte-apercu, .rencontre-sur-table, .deroule-phase, .est-statut')) continue
        const r = f.getBoundingClientRect()
        if (r.width === 0 || r.height === 0) continue
        souples.push({ x: r.left - cadre.origine.left, y: r.top - cadre.origine.top, w: r.width, h: r.height + 20 })
      }
      const r = placerEventail(pile, total, { w: cadre.boite.w, h: cadre.boite.h }, interdits, souples)
      setPlace((avant) => (avant && avant.x === r.x && avant.y === r.y && avant.carte === w ? avant : { x: r.x, y: r.y, carte: w }))
    }
    mesurer()
    const minuteur = window.setInterval(mesurer, 150)
    window.addEventListener('resize', mesurer)
    return () => { window.clearInterval(minuteur); window.removeEventListener('resize', mesurer) }
    // eslint-disable-next-line react-hooks/exhaustive-deps -- la rangee suit les cartes, pas l'identite des objets de choix
  }, [ids])
  // Pas de place mesurable au bout de 600 ms : les choix restent dans le bandeau (ils y sont deja).
  useEffect(() => {
    if (place) return
    const minuteur = window.setTimeout(() => choix.forEach((c) => signaler(c.id, true)), 600)
    return () => window.clearTimeout(minuteur)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [place, ids])
  if (!place) return null
  return (
    <div
      className="tsm-eventail"
      role="group"
      aria-label={t('Améliorations à jouer')}
      style={{ left: `${place.x}px`, top: `${place.y}px`, '--eventail-w': `${place.carte}px` } as CSSProperties}
    >
      {choix.map((c, i) => {
        const bloque = !!c.indisponible
        const [nomCarte, capacite] = c.nom.split(' — ')
        return (
          <button
            key={c.id}
            type="button"
            className={`tsm-eventail-carte${bloque ? ' est-inactif' : ''}`}
            style={{ '--rang': i } as CSSProperties}
            disabled={bloque}
            aria-label={c.nom}
            title={c.indisponible ?? c.nom}
            onClick={c.choisir}
            onMouseEnter={() => survoler(c, true)}
            onMouseLeave={() => survoler(c, false)}
            onFocus={() => survoler(c, true)}
            onBlur={() => survoler(c, false)}
            data-eventail=""
            data-choix-unique={unique === c.id ? '' : undefined}
          >
            <span className="tsm-eventail-image" aria-hidden="true">
              <ScanCard {...c.carte!} id={`eventail-${c.carte!.id}`} onSelect={undefined} highlight={false} state="ready" exhausted={false} />
            </span>
            <span className="tsm-eventail-nom">
              <b>{nomCarte}</b>
              {capacite ? <i>{capacite}</i> : null}
            </span>
            {unique === c.id ? <kbd className="tsm-touche">{t('Espace')}</kbd> : null}
          </button>
        )
      })}
    </div>
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
    <BandeauDeplacable className={`tsm-bandeau est-bilan${defaite ? ' est-defaite' : ''}`} role="status" aria-live="polite">
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
    </BandeauDeplacable>
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
  ordreDeLaTable,
}: {
  titre: string
  choisies: number
  maximum: number
  cibles: CibleSurTable[]
  prete: boolean
  raison: string
  valider: () => void
  annuler?: () => void
  /**
   * Une selection ORDONNEE dont l'ordre de la table est un bon defaut (ordre d'activation des sbires) : un bouton
   * « Garder l'ordre de la table » choisit les cartes restantes dans l'ordre de la rangee et valide, en UN clic
   * (Espace) au lieu d'un clic par sbire (19/10/2026). Les cliquer une a une reste possible.
   */
  ordreDeLaTable?: boolean
}) {
  // Les clics sur les cartes s'ajoutent dans l'etat du jeu ; la validation attend que cet etat soit a jour.
  const [validerQuandPrete, setValiderQuandPrete] = useState(false)
  useEffect(() => {
    if (!validerQuandPrete || !prete) return
    setValiderQuandPrete(false)
    valider()
  }, [validerQuandPrete, prete, valider])
  const restantes = cibles.filter((c) => !c.choisie && c.etiquette === undefined)
  const garderLOrdre = () => {
    if (restantes.length === 0) {
      if (prete) valider()
      return
    }
    // L'ORDRE DE LA TABLE = la rangee lue de gauche a droite (puis de haut en bas) : le moteur, lui, liste les sbires
    // du plus recemment engage au plus ancien, soit de DROITE a GAUCHE a l'ecran (mesure du 19/10/2026).
    const cadre = cadreDuPlateau()
    const place = (c: CibleSurTable) => {
      const b = cadre ? boiteDeCarte(c.id, cadre) : undefined
      return b ? { x: b.x, y: Math.round(b.y / 60) } : { x: Number.POSITIVE_INFINITY, y: 0 }
    }
    const rangee = [...restantes].sort((a, b) => place(a).y - place(b).y || place(a).x - place(b).x)
    for (const c of rangee) c.agir()
    setValiderQuandPrete(true)
  }
  return (
    <>
      <BandeauDeplacable className="tsm-bandeau est-question" role="group" aria-label={t('Ta décision')}>
        <span className="tsm-phrase">
          <b>{titre}</b>
          {maximum > 0 ? <span className="tsm-compte"> {choisies}/{maximum}</span> : null}
        </span>
        {ordreDeLaTable && !prete ? (
          <button type="button" className="tsm-bouton" onClick={garderLOrdre} data-choix-unique="" data-ordre-table="">
            {choisies > 0 ? t('Finir dans l’ordre de la table') : t('Garder l’ordre de la table')}
            <kbd className="tsm-touche">{t('Espace')}</kbd>
          </button>
        ) : null}
        <button
          type="button"
          className={`tsm-bouton${ordreDeLaTable && !prete ? ' est-refus' : ''}`}
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
        {ordreDeLaTable && !prete ? <span className="tsm-consigne">{t('ou clique les cartes une à une, dans l’ordre voulu')}</span> : null}
      </BandeauDeplacable>
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

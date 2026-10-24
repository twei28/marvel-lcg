// UN ROND : une carte de la table dessinee comme un rond (decisions du 24/10/2026).
//
// - le cadre : l'illustration de la carte, rognee en rond ; l'anneau dit les PV (vert), la menace (orange)
//   ou les degats d'un sbire (rouge) ; la pastille donne la valeur ;
// - dessous : le nom, puis l'attaque et la menace (valeurs du moteur, deja modifiees par les cartes en jeu) ;
// - dessus : les etats en etiquettes (initiales colorees des qu'il y en a plus de deux), les jetons par type,
//   les ameliorations attachees en petits ronds poses a moitie sous la carte hote ;
// - une carte epuisee est grisee.
//
// Le geste : un toucher agit quand le moteur demande de CHOISIR cette carte (cible, ressource), sinon il ouvre
// la feuille de la carte ; l'appui long ouvre l'apercu (meme composant `CarteOuverte` pour l'instant).
import { useEffect, useRef, useState, type MouseEvent as ReactMouseEvent, type ReactElement } from 'react'
import type { CardEffectDelta, ScanCardProps } from '../../../components/ScanCard'
import { versVignette } from '../../../components/ScanCard'
import { avecInteraction } from '../../Board'
import type { EtatInteractif } from '../../interaction'
import { t } from '../../langue'
import type { GroupeDePile, UniteAffichee } from '../../zones'
import { useAppuiLong } from '../useAppuiLong'
import { SEUIL_INITIALES, etatsDe } from './etats-ronds'
import { useEtatGlisse } from './glisser-ronds'
import type { CleZone } from './repartir-ronds'

export type DecorRonds = {
  interactifs: Map<number, EtatInteractif>
  effets: Map<number, CardEffectDelta>
  heroActifId?: number
  ouvrirPile: (titre: string, cartes: ScanCardProps[], groupes?: GroupeDePile[]) => void
  ouvrirCarte: (carte: ScanCardProps, attachees?: ScanCardProps[]) => void
  /** Appui long : l'apercu tenu au doigt, sans boutons (Q51). */
  apercuTenu?: (carte: ScanCardProps, attachees?: ScanCardProps[]) => void
  agir: (carte: ScanCardProps) => void
  /** Mode manuel au doigt (Q52) : un toucher CHOISIT le rond, la barre d'outils agit dessus. */
  manuel?: { choisieId: number | undefined; choisir: (carte: ScanCardProps) => void }
}

/**
 * Les JETONS (ronds) montrent l'illustration ANGLAISE : les scans francais portent un filigrane en losange qui se voit dans
 * un petit rond (demande du 24/10/2026). La feuille de la carte, elle, garde le scan francais. Le serveur rend toujours
 * quelque chose pour une vignette anglaise (repli sur la francaise quand il n'y en a pas).
 */
export function urlDuJeton(url: string): string {
  return versVignette(url.replace(/(\/(?:scan|vignette)\/)fr_/, '$1'))
}

const ETIQUETTE_STAT: Record<string, string> = { ATK: 'ATQ', THW: 'CTR', DEF: 'DÉF', REC: 'REC', SCH: 'MNG' }
const STATS_PAR_TYPE: Partial<Record<ScanCardProps['kind'], string[]>> = {
  villain: ['ATK', 'SCH'],
  minion: ['ATK', 'SCH'],
  ally: ['ATK', 'THW'],
  hero: ['ATK', 'THW', 'DEF'],
  'alter-ego': ['REC'],
}

/** Les cartes qui s'epuisent en servant : prete = anneau dore, utilisee = grisee. */
const KINDS_QUI_S_EPUISENT = new Set(['support', 'upgrade', 'ally', 'hero', 'alter-ego'])

/** Les roles pour lesquels un toucher CHOISIT la carte au lieu de l'ouvrir. */
const ROLES_QUI_CHOISISSENT = new Set(['cible', 'ressource'])

export type ApparenceRond = {
  /** « 3/4 » ou « 1/7 » : la pastille. Vide = pas de pastille. */
  texte?: string
  /** 0 -> 1 : la part d'anneau peinte. */
  part: number
  couleur: string
}

const VERT = '#3d9b57'
const ROUGE = '#c4453c'
const ORANGE = '#d9822b'
const GRIS = '#6a7280'
const VIOLET = '#8a6bd1'

/** Ce que l'anneau et la pastille disent d'une carte. Pure : testee. */
export function apparenceDe(carte: ScanCardProps): ApparenceRond {
  const jauge = carte.jauge
  const texte = jauge?.texte ?? carte.allyHp ?? carte.schemeThreat
  if (carte.kind === 'environment') return { texte, part: 1, couleur: VIOLET }
  if (jauge?.genre === 'menace' || carte.schemeThreat !== undefined) {
    // Manigance annexe d'un JOUEUR : anneau vert (le vert n'est plus l'anneau « carte prete », devenu dore), pour la
    // distinguer d'un coup d'oeil des manigances du mechant (24/10/2026).
    const duJoueur = carte.kind === 'side-scheme' && carte.camp === 'player'
    return { texte, part: jauge?.remplissage ?? 1, couleur: duJoueur ? VERT : ORANGE }
  }
  if (jauge || carte.allyHp !== undefined) {
    // Le mechant a l'anneau vert comme un heros (ses PV) ; seuls ses sbires sont rouges.
    return { texte, part: jauge?.remplissage ?? 1, couleur: carte.camp === 'encounter' && carte.kind !== 'villain' ? ROUGE : VERT }
  }
  return { texte, part: 1, couleur: carte.camp === 'encounter' ? ROUGE : GRIS }
}

/** L'illustration : la carte est rognee sur son dessin (les manigances se posent en paysage, leur dessin est a droite). */
function positionDe(carte: ScanCardProps): { taille: string; position: string } {
  // Manigance principale : texte a gauche, dessin a droite ; manigance annexe : l'inverse (coteDuTexte).
  if (carte.kind === 'main-scheme') return { taille: '230% auto', position: '88% 55%' }
  if (carte.kind === 'side-scheme') return { taille: '230% auto', position: '12% 55%' }
  if (carte.kind === 'hero' || carte.kind === 'alter-ego') return { taille: '175% auto', position: '44% 22%' }
  if (carte.kind === 'villain') return { taille: '200% auto', position: '38% 20%' }
  return { taille: '190% auto', position: '48% 24%' }
}

export function Rond({
  unite,
  zone,
  decor,
  vaincu = false,
}: {
  unite: UniteAffichee
  zone: CleZone
  decor: DecorRonds
  /** Le rond d'une carte qui vient de partir : grise, « VAINCU », sans geste. */
  vaincu?: boolean
}): ReactElement {
  const carte = avecInteraction(unite.carte, decor.interactifs, decor.effets)
  const role = decor.interactifs.get(Number(unite.carte.id))?.role
  const choisit = role !== undefined && ROLES_QUI_CHOISISSENT.has(role)
  const attachees = unite.attachees.map((a) => avecInteraction(a, decor.interactifs, decor.effets))
  const apercu = () => decor.ouvrirCarte(carte, attachees.filter((a) => a.kind !== 'status'))
  const appui = useAppuiLong(() => (decor.apercuTenu ?? decor.ouvrirCarte)(carte, attachees.filter((a) => a.kind !== 'status')))
  const apparence = apparenceDe(carte)
  const { taille, position } = positionDe(carte)
  const paysageTourne = carte.isLandscape === true && carte.scanIsPortrait === true && !carte.facedown
  const etats = etatsDe(attachees)
  const ameliorations = attachees.filter((a) => a.kind !== 'status')
  const initiales = etats.length > SEUIL_INITIALES
  const statsVoulues = STATS_PAR_TYPE[carte.kind] ?? []
  const stats = (carte.statsComplets ?? []).filter((s) => statsVoulues.includes(s.label))
  const cible = carte.targetPulse === true || carte.state === 'targetable' || role === 'cible'
  const { etat: etatGlisse, glissable, clicAvale } = useEtatGlisse(Number(unite.carte.id))
  const surToucher = (evenement: ReactMouseEvent<HTMLButtonElement>) => {
    evenement.stopPropagation()
    // Le clic qui suit un glisser ne doit pas ouvrir la feuille.
    if (clicAvale()) return
    if (appui.vientDeDeclencher()) return
    if (decor.manuel) return decor.manuel.choisir(carte)
    if (choisit || (role === 'cible' && carte.onSelect)) decor.agir(carte)
    else apercu()
  }
  // Le retournement (changement de forme, nouveau stade du mechant) : quand la carte d'un meme rond change d'illustration.
  const imageAvant = useRef(carte.imageUrl)
  const [retourne, setRetourne] = useState(false)
  useEffect(() => {
    if (imageAvant.current === carte.imageUrl) return
    imageAvant.current = carte.imageUrl
    setRetourne(true)
    const fin = window.setTimeout(() => setRetourne(false), 600)
    return () => window.clearTimeout(fin)
  }, [carte.imageUrl])
  // Un changement de PV ou de menace s'ecrit un instant au-dessus du rond (« -3 », « +2 »).
  const delta = carte.effectDelta
  // Riposte N (Q60) : une etiquette permanente sur le sbire, avec sa valeur (« Retaliate 1 » en anglais).
  const motRiposte = (carte.keywords ?? []).find((mot) => /^(retaliate|riposte)\b/i.test(mot.nom.trim()))
  const valeurRiposte = motRiposte ? /(\d+)/.exec(motRiposte.nom)?.[1] : undefined
  const gardien = (carte.keywords ?? []).some((mot) => /^(guard|garde)$/i.test(mot.nom.trim()))
  const estRessource = role === 'ressource'
  const classes = [
    'rond',
    retourne ? 'se-retourne' : '',
    vaincu ? 'rond-vaincu' : '',
    estRessource ? 'est-ressource' : '',
    `rond-${zone}`,
    carte.exhausted ? 'est-epuise' : '',
    !carte.exhausted && !carte.facedown && KINDS_QUI_S_EPUISENT.has(carte.kind) ? 'est-prete' : '',
    cible ? 'est-cible' : '',
    decor.manuel?.choisieId === Number(unite.carte.id) ? 'est-choisi-manuel' : '',
    carte.state === 'selected' ? 'est-choisi' : '',
    carte.crise ? 'est-bloquee' : '',
    glissable ? 'est-glissable' : '',
    etatGlisse === 'cible' ? 'est-cible-glisse' : '',
    etatGlisse === 'assombri' ? 'est-assombri' : '',
    etatGlisse === 'source' ? 'est-source-glisse' : '',
    carte.facedown ? 'est-cachee' : '',
  ]
    .filter(Boolean)
    .join(' ')
  const rayon = 46
  const circonference = 2 * Math.PI * rayon
  return (
    <div
      className={classes}
      data-tactile="carte"
      data-card-id={unite.carte.id}
      data-kind={carte.kind}
      style={{ ['--nb-amelio' as string]: ameliorations.length }}
    >
      <button
        type="button"
        className="rond-bouton"
        aria-label={`${carte.name}${apparence.texte ? `, ${apparence.texte}` : ''}`}
        onClick={surToucher}
        disabled={vaincu}
        {...appui.gestes}
      >
        {paysageTourne ? (
          // Une manigance se pose en paysage mais son scan est servi en portrait : on le tourne d'un quart de tour
          // (comme ScanCard) puis on cadre son dessin, a droite de la carte.
          <span className={`rond-art rond-art-tourne${carte.kind === 'side-scheme' ? ' est-dessin-gauche' : ''}`}>
            <img src={urlDuJeton(carte.imageUrl)} alt="" draggable={false} loading="lazy" />
          </span>
        ) : (
          <span
            className="rond-art"
            style={{
              backgroundImage: carte.facedown ? undefined : `url(${urlDuJeton(carte.imageUrl)})`,
              backgroundSize: taille,
              backgroundPosition: position,
            }}
          />
        )}
        <svg className="rond-anneau" viewBox="0 0 100 100" aria-hidden="true">
          <circle cx="50" cy="50" r={rayon} className="rond-fond-anneau" />
          <circle
            cx="50"
            cy="50"
            r={rayon}
            className="rond-part-anneau"
            style={{ stroke: apparence.couleur }}
            strokeDasharray={`${Math.max(0, Math.min(1, apparence.part)) * circonference} ${circonference}`}
            transform="rotate(-90 50 50)"
          />
        </svg>
        {apparence.texte ? (
          <em className="rond-pastille" style={{ background: apparence.couleur }}>
            {apparence.texte}
          </em>
        ) : null}
        {carte.orderNumber !== undefined ? <b className="rond-ordre">{carte.orderNumber}</b> : null}
      </button>
      {etats.length > 0 ? (
        <span className="rond-etats">
          {etats.map((etat) => (
            <i key={etat.cle} style={{ background: etat.fond, color: etat.encre }} title={etat.texte}>
              {initiales ? etat.initiales : etat.texte}
            </i>
          ))}
        </span>
      ) : null}
      {carte.counters && carte.counters.length > 0 ? (
        <span className="rond-jetons">
          {carte.counters.map((jeton) => (
            <i key={jeton.cle ?? jeton.label}>
              {jeton.label} {jeton.value}
            </i>
          ))}
        </span>
      ) : null}
      {ameliorations.length > 0 ? (
        <span className="rond-attachees" aria-hidden="true">
          {ameliorations.map((amelioration, i) => (
            <span
              key={amelioration.id}
              className="rond-mini"
              title={amelioration.name}
              style={{ ['--rang' as string]: i, backgroundImage: `url(${urlDuJeton(amelioration.imageUrl)})` }}
            />
          ))}
        </span>
      ) : null}
      {vaincu ? <span className="rond-vaincu-etiquette">{t('VAINCU')}</span> : null}
      <span className="rond-nom">{carte.name}</span>
      {stats.length > 0 ? (
        <span className="rond-stats">
          {stats.map((stat) => (
            <span
              key={stat.label}
              className={`stat-${stat.label}${stat.base !== undefined && stat.value > stat.base ? ' est-augmentee' : ''}${stat.base !== undefined && stat.value < stat.base ? ' est-reduite' : ''}`}
            >
              {t(ETIQUETTE_STAT[stat.label] ?? stat.label)} {stat.value}
            </span>
          ))}
        </span>
      ) : null}
      {delta && delta.kind !== 'status' && delta.kind !== 'token' ? (
        <span
          key={`${delta.kind}-${delta.value}-${carte.id}`}
          className={`rond-delta rond-delta-${delta.kind}`}
          aria-hidden="true"
        >
          {delta.kind === 'damage' ? `-${Math.abs(delta.value)}` : `+${Math.abs(delta.value)}`}
        </span>
      ) : null}
      {estRessource ? <span className="rond-etiquette rond-etiquette-ressource">+1</span> : null}
      {motRiposte ? (
        <span className="rond-etiquette rond-etiquette-riposte">
          {t('Riposte')}
          {valeurRiposte ? ` ${valeurRiposte}` : ''}
        </span>
      ) : null}
      {gardien ? <span className="rond-etiquette rond-etiquette-garde">🛡 {t('Garde')}</span> : carte.crise ? <span className="rond-etiquette">⚠ {t('Crise')}</span> : null}
    </div>
  )
}

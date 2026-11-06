/**
 * Le tchat, en VOLET tire depuis le bord — meme pattern que VoletJournal.tsx
 * (languette qui se clique ou se tire, Escape referme), enrichi d'onglets
 * (Général / Table / un par conversation privée) et d'un mode détaché en
 * fenêtre flottante redimensionnable.
 *
 * Reconstruction du 06/11/2026, après le retrait du 12/09/2026 (commit
 * bb0c8051) : trois fils désormais, le fil de table ouvert aux spectateurs,
 * jamais au journal de partie (qui reste un volet à part, VoletJournal).
 *
 * ⚠ LE FIL DE TABLE N'APPARAÎT JAMAIS EN RELECTURE (`?relecture`) : il n'a pas
 * survécu à la partie qui l'a vu naître (voir `effacer_messages_table`, côté
 * serveur). Un spectateur EN DIRECT (`?spectateur`), lui, le voit et peut y
 * écrire.
 */
import { useEffect, useMemo, useRef, useState } from 'react'
import { t } from './langue'
import {
  DRAPEAUX_LANGUES,
  drapeauxDuMessage,
  ecrireLanguesChoisies,
  heureLocale,
  lireLanguesChoisies,
  listerConnectes,
  transportMoteur,
  type MessageTchat,
  type TransportTchat,
} from './tchat'
import { useGlisserPanneau, styleAvecDecalage } from './placement/useGlisserPanneau'
import { useFenetreFlottante, styleAvecTaille } from './useFenetreFlottante'
import './VoletTchat.css'

/** En dessous de ce deplacement horizontal, le geste est un simple clic (voir VoletJournal.tsx). */
export const SEUIL_GESTE_PX = 24

/** Rien de plus a l'ecran que ce qu'un fil peut utilement montrer. */
const MAX_MESSAGES = 80
const PERIODE_OUVERT_MS = 4000
const PERIODE_FERME_MS = 20000

type CleFil = 'general' | 'table' | `mp:${string}`

function enRelecture(): boolean {
  return new URLSearchParams(window.location.search).has('relecture')
}

type EtatFil = {
  messages: MessageTchat[]
  curseur: number
  nonLus: number
  idsConnus: Set<number>
  moi?: string
}

function filVide(): EtatFil {
  return { messages: [], curseur: 0, nonLus: 0, idsConnus: new Set() }
}

export function VoletTchat({
  ouvert,
  ouvrir,
  fermer,
  tableId,
  spectateur = false,
  transport,
}: {
  ouvert: boolean
  ouvrir: () => void
  fermer: () => void
  /** Absent hors partie (préparation sans table encore créée). */
  tableId?: string
  spectateur?: boolean
  transport?: TransportTchat
}) {
  const reseau = useMemo(() => transport ?? transportMoteur(), [transport])
  const tableVisible = Boolean(tableId) && !enRelecture()

  const [onglet, setOnglet] = useState<CleFil>('general')
  const [fils, setFils] = useState<Record<CleFil, EtatFil>>(() => ({ general: filVide(), table: filVide() }))
  const [brouillon, setBrouillon] = useState('')
  const [muet, setMuet] = useState(false)
  const futActif = useRef(false)
  const [detache, setDetache] = useState(false)
  const filRef = useRef<HTMLDivElement | null>(null)
  // Conversations privees connues (fil general seulement, voir `/tchat/vue`) :
  // alimente la liste des onglets MP meme avant d'avoir clique sur qui que ce soit.
  const [privesConnus, setPrivesConnus] = useState<Record<string, number>>({})
  // Bouton « Creer une table » (chantier du 06/11/2026) : mode selection de
  // pseudos presents, avant de rediriger vers l'ecran de creation existant.
  const [creationTable, setCreationTable] = useState(false)
  const [invitesChoisis, setInvitesChoisis] = useState<Set<string>>(new Set())
  const [connectesDisponibles, setConnectesDisponibles] = useState<string[]>([])

  // Drapeaux de langues parlees (chantier du 06/11/2026) : reglage dans le
  // tchat lui-meme, garde dans CE navigateur (le profil du compte, s'il y en
  // a un, n'est synchronise que via le transport « site direct », pas encore
  // branche depuis le plateau).
  const [langues, setLangues] = useState<string[]>(() => lireLanguesChoisies().split(',').filter(Boolean))
  const [menuLanguesOuvert, setMenuLanguesOuvert] = useState(false)
  const languesDejaPreremplies = useRef(langues.length > 0)

  const basculerLangue = (code: string) => {
    setLangues((precedent) => {
      const suivant = precedent.includes(code) ? precedent.filter((c) => c !== code) : [...precedent, code]
      ecrireLanguesChoisies(suivant.join(','))
      return suivant
    })
  }

  const { decalage, gestes: gestesDeplacer } = useGlisserPanneau('tchat', 'marvel-tchat-position')
  const { taille, poignee: poigneeTaille } = useFenetreFlottante(
    'marvel-tchat-taille',
    { largeur: 360, hauteur: 460 },
    { largeur: 280, hauteur: 280 },
    { largeur: 720, hauteur: 820 }
  )

  const debutGeste = useRef<number | undefined>(undefined)
  const clicAIgnorer = useRef(false)

  useEffect(() => {
    if (!ouvert) return
    const surTouche = (e: KeyboardEvent) => {
      if (e.key === 'Escape') fermer()
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [ouvert, fermer])

  // Polling adaptatif : le fil affiché au premier plan a la cadence rapide,
  // les autres fils connus tournent en arrière-plan pour leur pastille.
  useEffect(() => {
    if (!ouvert || muet) return
    let vivant = true
    const sonder = async (fil: CleFil) => {
      const [filReseau, avec] = fil === 'general' ? (['general', ''] as const) : fil === 'table' ? (['table', ''] as const) : (['prive', fil.slice(3)] as const)
      const curseur = fils[fil]?.curseur ?? 0
      const vue = await reseau.lire(filReseau, curseur, avec)
      if (!vivant) return
      if (!vue.actif) {
        if (fil === onglet) {
          if (!futActif.current) setMuet(true)
        }
        return
      }
      futActif.current = true
      if (fil === 'general' && vue.prives) {
        setPrivesConnus(vue.prives)
      }
      if (fil === 'general' && !languesDejaPreremplies.current && vue.mesLangues) {
        languesDejaPreremplies.current = true
        const choix = vue.mesLangues.split(',').filter(Boolean)
        setLangues(choix)
        ecrireLanguesChoisies(choix.join(','))
      }
      if (vue.messages.length === 0) return
      setFils((precedent) => {
        const etat = precedent[fil] ?? filVide()
        const inedits = vue.messages.filter((m) => !etat.idsConnus.has(m.id))
        if (inedits.length === 0) return precedent
        const idsConnus = new Set(etat.idsConnus)
        for (const m of inedits) idsConnus.add(m.id)
        const messages = [...etat.messages, ...inedits].slice(-MAX_MESSAGES)
        const nonLus = fil === onglet ? 0 : etat.nonLus + inedits.filter((m) => m.pseudo !== etat.moi).length
        return { ...precedent, [fil]: { messages, curseur: vue.dernier, nonLus, idsConnus, moi: vue.pseudo ?? etat.moi } }
      })
    }
    const filsASonder: CleFil[] = ['general', ...(tableVisible ? (['table'] as const) : [])]
    // Premier sondage immediat de tout ce qu'on connait (badges compris),
    // puis l'onglet affiche repasse toutes les 4 s, les autres toutes les 20 s.
    for (const fil of filsASonder) sonder(fil)
    const minuteur = window.setInterval(() => {
      sonder(onglet)
    }, PERIODE_OUVERT_MS)
    const minuteurFond = window.setInterval(() => {
      for (const fil of filsASonder) if (fil !== onglet) sonder(fil)
    }, PERIODE_FERME_MS)
    return () => {
      vivant = false
      window.clearInterval(minuteur)
      window.clearInterval(minuteurFond)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ouvert, muet, onglet, tableVisible, reseau])

  // Pastille totale (languette repliée) : somme des non-lus de tous les fils connus.
  const nonLusTotal = Object.values(fils).reduce((total, f) => total + f.nonLus, 0)

  useEffect(() => {
    // L'onglet affiché est considéré lu dès qu'on le regarde.
    setFils((precedent) => {
      const etat = precedent[onglet]
      if (!etat || etat.nonLus === 0) return precedent
      return { ...precedent, [onglet]: { ...etat, nonLus: 0 } }
    })
  }, [onglet, ouvert])

  useEffect(() => {
    if (!filRef.current) return
    filRef.current.scrollTop = filRef.current.scrollHeight
  }, [fils, onglet])

  const envoyer = async () => {
    const texte = brouillon.trim()
    if (!texte) return
    setBrouillon('')
    const [filReseau, avec] = onglet === 'general' ? (['general', ''] as const) : onglet === 'table' ? (['table', ''] as const) : (['prive', onglet.slice(3)] as const)
    const ok = await reseau.dire(filReseau, texte, avec, langues.join(','))
    if (!ok) setBrouillon(texte)
  }

  const etatOnglet = fils[onglet] ?? filVide()

  const ouvrirMp = (pseudo: string) => {
    const cle: CleFil = `mp:${pseudo}`
    setFils((precedent) => (precedent[cle] ? precedent : { ...precedent, [cle]: filVide() }))
    setOnglet(cle)
  }

  const basculerInvite = (pseudo: string) => {
    setInvitesChoisis((precedent) => {
      const suivant = new Set(precedent)
      if (suivant.has(pseudo)) suivant.delete(pseudo)
      else suivant.add(pseudo)
      return suivant
    })
  }

  const surClicPseudo = (pseudo: string) => {
    if (pseudo === etatOnglet.moi) return
    if (creationTable) basculerInvite(pseudo)
    else ouvrirMp(pseudo)
  }

  const ouvrirCreationTable = () => {
    setCreationTable(true)
    setInvitesChoisis(new Set())
    void listerConnectes().then(setConnectesDisponibles)
  }

  const validerCreationTable = () => {
    if (invitesChoisis.size === 0) return
    const liste = [...invitesChoisis].map((p) => encodeURIComponent(p)).join(',')
    window.location.href = `/prepare.html?inviter=${liste}`
  }

  const styleDetache = detache ? styleAvecTaille(styleAvecDecalage({ position: 'fixed' }, decalage), taille) : undefined

  return (
    <>
      <button
        type="button"
        className={`volet-tchat-languette${ouvert ? ' est-ouvert' : ''}`}
        aria-expanded={ouvert}
        aria-controls="volet-tchat"
        title={ouvert ? t('Refermer le tchat') : t('Ouvrir le tchat')}
        onPointerDown={(e) => {
          debutGeste.current = e.clientX
        }}
        onPointerUp={(e) => {
          const debut = debutGeste.current
          debutGeste.current = undefined
          if (debut === undefined) return
          const dx = e.clientX - debut
          if (dx <= -SEUIL_GESTE_PX) {
            clicAIgnorer.current = true
            ouvrir()
          } else if (dx >= SEUIL_GESTE_PX) {
            clicAIgnorer.current = true
            fermer()
          }
        }}
        onClick={() => {
          if (clicAIgnorer.current) {
            clicAIgnorer.current = false
            return
          }
          if (ouvert) fermer()
          else ouvrir()
        }}
      >
        <span className="volet-tchat-languette-texte">{t('Tchat')}</span>
        {!ouvert && nonLusTotal > 0 ? <span className="volet-tchat-pastille">{nonLusTotal}</span> : null}
      </button>
      {ouvert ? (
        <aside
          id="volet-tchat"
          className={`volet-tchat${detache ? ' est-detache' : ''}`}
          role="dialog"
          aria-label={t('Tchat')}
          style={styleDetache}
        >
          <header className="volet-tchat-tete" {...(detache ? gestesDeplacer : {})}>
            <h2>{t('Tchat')}</h2>
            <button
              type="button"
              className="volet-tchat-detacher"
              onClick={() => setDetache((d) => !d)}
              title={detache ? t('Rattacher le tchat') : t('Détacher le tchat dans sa propre fenêtre')}
            >
              {detache ? '⧉' : '⤢'}
            </button>
            <button type="button" className="reglages-fermer" onClick={fermer} title={t('Fermer')}>
              ×
            </button>
          </header>
          <div className="volet-onglets volet-tchat-onglets">
            <button type="button" className={onglet === 'general' ? 'est-actif' : ''} onClick={() => setOnglet('general')}>
              {t('Général')}
              {fils.general?.nonLus ? <em>{fils.general.nonLus}</em> : null}
            </button>
            {tableVisible ? (
              <button type="button" className={onglet === 'table' ? 'est-actif' : ''} onClick={() => setOnglet('table')}>
                {t('Table')}
                {fils.table?.nonLus ? <em>{fils.table.nonLus}</em> : null}
              </button>
            ) : null}
            {[...new Set([...Object.keys(fils).filter((cle) => cle.startsWith('mp:')), ...Object.keys(privesConnus).map((p) => `mp:${p}`)])].map(
              (cle) => (
                <button type="button" key={cle} className={onglet === cle ? 'est-actif' : ''} onClick={() => ouvrirMp(cle.slice(3))}>
                  {cle.slice(3)}
                  {fils[cle as CleFil]?.nonLus ? <em>{fils[cle as CleFil].nonLus}</em> : null}
                </button>
              )
            )}
          </div>
          <div className="volet-tchat-contenu">
            {onglet === 'general' ? (
              <div className="volet-tchat-creer-table">
                {creationTable ? (
                  <>
                    <p className="volet-tchat-creer-table-aide">{t('Choisis les personnes à inviter (clique sur un pseudo).')}</p>
                    {connectesDisponibles.length > 0 ? (
                      <div className="volet-tchat-connectes">
                        {connectesDisponibles
                          .filter((p) => p !== etatOnglet.moi)
                          .map((p) => (
                            <button
                              type="button"
                              key={p}
                              className={invitesChoisis.has(p) ? 'est-choisi' : ''}
                              onClick={() => basculerInvite(p)}
                            >
                              {p}
                            </button>
                          ))}
                      </div>
                    ) : null}
                    <div className="volet-tchat-creer-table-actions">
                      <button type="button" onClick={() => setCreationTable(false)}>
                        {t('Annuler')}
                      </button>
                      <button type="button" disabled={invitesChoisis.size === 0} onClick={validerCreationTable}>
                        {t('Valider')} {invitesChoisis.size > 0 ? `(${invitesChoisis.size})` : ''}
                      </button>
                    </div>
                  </>
                ) : (
                  <button type="button" className="volet-tchat-creer-table-bouton" onClick={ouvrirCreationTable}>
                    {t('Créer une table')}
                  </button>
                )}
              </div>
            ) : null}
            {muet ? (
              <p className="volet-tchat-muet">
                {t('Pas de tchat ici.')}{' '}
                <button type="button" onClick={() => setMuet(false)}>
                  {t('Réessayer')}
                </button>
              </p>
            ) : (
              <>
                <div className="volet-tchat-fil" ref={filRef}>
                  {etatOnglet.messages.map((m) => (
                    <p key={m.id} className={`volet-tchat-message${m.pseudo === etatOnglet.moi ? ' est-moi' : ''}`}>
                      <button
                        type="button"
                        className="volet-tchat-pseudo"
                        disabled={m.pseudo === etatOnglet.moi}
                        onClick={() => surClicPseudo(m.pseudo)}
                      >
                        {m.pseudo}
                      </button>{' '}
                      {drapeauxDuMessage(m) ? <span className="volet-tchat-drapeaux">{drapeauxDuMessage(m)}</span> : null}{' '}
                      <span className="volet-tchat-heure">{heureLocale(m)}</span>
                      <br />
                      {m.texte}
                    </p>
                  ))}
                </div>
                <form
                  className="volet-tchat-saisie"
                  onSubmit={(e) => {
                    e.preventDefault()
                    void envoyer()
                  }}
                >
                  <div className="volet-tchat-langues">
                    <button
                      type="button"
                      className="volet-tchat-langues-bouton"
                      onClick={() => setMenuLanguesOuvert((o) => !o)}
                      title={t('Langues parlées')}
                    >
                      {langues.length > 0 ? langues.map((c) => DRAPEAUX_LANGUES[c]).join('') : '🏳️'}
                    </button>
                    {menuLanguesOuvert ? (
                      <div className="volet-tchat-langues-menu">
                        {Object.entries(DRAPEAUX_LANGUES).map(([code, drapeau]) => (
                          <label key={code}>
                            <input type="checkbox" checked={langues.includes(code)} onChange={() => basculerLangue(code)} />
                            {drapeau} {code}
                          </label>
                        ))}
                      </div>
                    ) : null}
                  </div>
                  <input
                    type="text"
                    value={brouillon}
                    onChange={(e) => setBrouillon(e.target.value)}
                    placeholder={t('Écrire un message…')}
                    maxLength={500}
                  />
                  <button type="submit">{t('Envoyer')}</button>
                </form>
              </>
            )}
          </div>
          {detache ? <div className="volet-tchat-poignee-taille" {...poigneeTaille} /> : null}
        </aside>
      ) : null}
    </>
  )
}

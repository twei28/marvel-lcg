// Un texte du journal dont les noms de cartes identifiees sont soulignes : au
// survol (PC) ou au toucher (tablette), l'image de la carte s'affiche en grand,
// avec le meme apercu que la table (decisions du 06/10/2026, idee de Yarro).
//
// Sans fournisseur (`CartesDuJournal`) ou sans carte identifiee, le texte
// s'affiche tel quel : rien n'est souligne qu'on ne sache pas montrer.
import { createContext, Fragment, useContext, useEffect, useRef, useState, type PointerEvent } from 'react'
import type { ScanCardProps } from '../components/ScanCard'
import { CarteApercu } from './Board'
import { decouperNoms, type RefCarte } from './cartes-journal'
import { avecIcones } from './icones-ressources'
import './NomsDeCartes.css'

export type AccesCartesJournal = {
  /** Vrai si la carte est connue du monde : sans elle, le nom reste du texte. */
  existe: (id: number) => boolean
  voir: (id: number, faceVisible: boolean) => ScanCardProps | undefined
  /** Classe de l'apercu, pour passer devant le panneau qui raconte. */
  classe?: string
  /** Panneaux que l'apercu ne doit pas recouvrir (voir usePlacement). */
  borneDroite?: readonly string[]
}

export const CartesDuJournal = createContext<AccesCartesJournal | undefined>(undefined)

function NomCarte({ id, nom, acces }: { id: number; nom: string; acces: AccesCartesJournal }) {
  const [carte, setCarte] = useState<ScanCardProps>()
  const pointeur = useRef<string>('mouse')
  const ici = useRef<HTMLSpanElement>(null)

  useEffect(() => {
    if (!carte || pointeur.current === 'mouse') return
    const fermer = (evenement: globalThis.PointerEvent) => {
      if (evenement.target instanceof Node && ici.current?.contains(evenement.target)) return
      setCarte(undefined)
    }
    document.addEventListener('pointerdown', fermer)
    return () => document.removeEventListener('pointerdown', fermer)
  }, [carte])

  const montrer = () => setCarte(acces.voir(id, true))
  return (
    <span
      ref={ici}
      className="nom-carte-journal"
      onPointerDown={(evenement: PointerEvent) => {
        pointeur.current = evenement.pointerType
      }}
      onPointerEnter={(evenement: PointerEvent) => {
        if (evenement.pointerType === 'mouse') montrer()
      }}
      onPointerLeave={(evenement: PointerEvent) => {
        if (evenement.pointerType === 'mouse') setCarte(undefined)
      }}
      onClick={(evenement) => {
        if (pointeur.current === 'mouse') return
        evenement.stopPropagation()
        if (carte) setCarte(undefined)
        else montrer()
      }}
    >
      {nom}
      {carte ? <CarteApercu carte={carte} classe={acces.classe} borneDroite={acces.borneDroite} /> : null}
    </span>
  )
}

export function TexteAvecCartes({ texte, cartes }: { texte: string; cartes: readonly RefCarte[] }) {
  const acces = useContext(CartesDuJournal)
  if (!acces || cartes.length === 0) return <>{avecIcones(texte)}</>
  const connues = cartes.filter((ref) => acces.existe(ref.id))
  return (
    <>
      {decouperNoms(texte, connues).map((morceau, rang) =>
        typeof morceau === 'string' ? (
          <Fragment key={rang}>{avecIcones(morceau)}</Fragment>
        ) : (
          <NomCarte key={rang} id={morceau.id} nom={morceau.nom} acces={acces} />
        )
      )}
    </>
  )
}

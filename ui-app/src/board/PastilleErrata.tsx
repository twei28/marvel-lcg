// La pastille « Errata » posée en bas d'une carte agrandie dont le texte officiel a été corrigé (Rules Reference 1.8,
// Annexe V : errata-rrg.ts). Au survol (ou au focus clavier), une bulle dit ce qui a changé et d'où ça vient.
//
// ⚠ DANS L'APERÇU AU SURVOL, la souris ne peut PAS atteindre la pastille (le panneau laisse passer la souris, sinon il
// se re-survolerait lui-même) : la même information s'écrit alors sous la carte, en clair (`NoteErrata`).
import { langueActuelle } from './langue'
import type { ErratumRrg } from './errata-rrg'
import './errata.css'

function libelles(erratum: ErratumRrg) {
  const en = langueActuelle() === 'en'
  return {
    en,
    source: `Rules Reference ${erratum.source === '1.8' ? '1.8' : '1.7'}`,
    resume: en ? erratum.resumeEn : erratum.resumeFr,
    titre: en ? 'Official errata: the printed text was corrected' : 'Errata officiel : le texte imprimé a été corrigé',
  }
}

/** `cote` : carte couchée (manigance), côté de sa boîte de texte : la pastille s'y range, au-dessus du bandeau du bas. */
export function PastilleErrata({ erratum, cote }: { erratum: ErratumRrg; cote?: 'gauche' | 'droite' }) {
  const l = libelles(erratum)
  return (
    <span className={`pastille-errata${cote ? ` pastille-errata-${cote}` : ''}`} tabIndex={0} role="note" aria-label={`Errata, ${l.source} : ${l.resume}`}>
      <span className="pastille-errata-mot">Errata</span>
      <span className="pastille-errata-bulle" role="tooltip">
        <b>{l.titre}</b>
        <span className="pastille-errata-resume">{l.resume}</span>
        <span className="pastille-errata-source">{l.source}</span>
      </span>
    </span>
  )
}

/** La même information, lisible sans souris, sous une carte agrandie (aperçu au survol). */
export function NoteErrata({ erratum }: { erratum: ErratumRrg }) {
  const l = libelles(erratum)
  return (
    <div className="note-errata" role="note">
      <span className="note-errata-mot">Errata</span>
      <span className="note-errata-texte">
        {l.resume} <span className="note-errata-source">({l.source})</span>
      </span>
    </div>
  )
}

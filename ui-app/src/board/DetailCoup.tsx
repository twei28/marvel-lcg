// LE DETAIL D'UN COUP en lecture seule, et la liste des coups d'un onglet.
//
// Partage par la relecture d'un onglet passe (DeroulePhase) et la revue de la
// phase finie (RevuePhase, volet du journal) : decisions du 03/10/2026. Les
// phrases sont celles du cartouche (deroule-textes.ts) ; l'etape recue est deja
// mise en langue par l'appelant quand il le peut.

import type { EtapeDeroule } from './deroule-phase'
import type { RefCarte } from './cartes-journal'
import { TexteAvecCartes } from './NomsDeCartes'
import {
  compteurLigneBilan,
  detailEtape,
  lignesEtoileBoost,
  resultatEtape,
  surtitreEtape,
  texteActivationAnnulee,
  texteBilanVide,
  texteCauseActivation,
  texteConsequence,
  texteDefaite,
  texteEffet,
  texteLigneBilan,
  texteSuiteRenfort,
  titreEtape,
} from './deroule-textes'

/**
 * Sur ces etapes, `carteId` est la carte NOMMEE par `cibleNom` (la carte
 * revelee, le nouveau stade, la carte qui entre) et `auteurNom` un autre nom
 * (le heros qui revele, l'ancien stade) : voir deroule-phase.ts.
 */
const CARTE_NOMMEE_PAR_LA_CIBLE = new Set(['revelation', 'stade', 'entree'])

/** Les cartes que l'etape designe par leur identifiant, chacune avec SON nom. */
export function cartesDeEtape(etape: EtapeDeroule): RefCarte[] {
  const refs: RefCarte[] = []
  if (CARTE_NOMMEE_PAR_LA_CIBLE.has(etape.titre)) {
    if (etape.carteId !== undefined && etape.cibleNom) refs.push({ id: etape.carteId, nom: etape.cibleNom })
    return refs
  }
  if (etape.carteId !== undefined && etape.auteurNom) refs.push({ id: etape.carteId, nom: etape.auteurNom })
  if (etape.cibleId !== undefined && etape.cibleNom) refs.push({ id: etape.cibleId, nom: etape.cibleNom })
  return refs
}

export function DetailCoup({ etape }: { etape: EtapeDeroule }) {
  const resultat = detailEtape(etape)
  const cartes = cartesDeEtape(etape)
  const annulee = texteActivationAnnulee(etape)
  const cause = texteCauseActivation(etape)
  const suite = texteSuiteRenfort(etape)
  return (
    <>
      {surtitreEtape(etape) ? <p className="deroule-surtitre">{surtitreEtape(etape)}</p> : null}
      <div className="deroule-entete">
        <p className="deroule-titre">
          <TexteAvecCartes texte={titreEtape(etape)} cartes={cartes} />
        </p>
      </div>
      {resultat ? (
        <p className="deroule-resultat">
          <TexteAvecCartes texte={resultat} cartes={cartes} />
        </p>
      ) : null}
      {lignesEtoileBoost(etape).map((ligne) => (
        <p key={ligne} className="deroule-etoile">{ligne}</p>
      ))}
      {annulee ? <p className="deroule-annulee">{annulee}</p> : null}
      {cause ? <p className="deroule-cause">{cause}</p> : null}
      {etape.effets && etape.effets.length > 0 ? (
        <ul className="deroule-effets">
          {etape.effets.map((effet, rang) => (
            <li key={rang}>{texteEffet(effet)}</li>
          ))}
        </ul>
      ) : null}
      {etape.consequences && etape.consequences.length > 0 ? (
        <ul className="deroule-effets deroule-consequences">
          {etape.consequences.map((consequence) => (
            <li key={consequence.cle}>{texteConsequence(consequence)}</li>
          ))}
        </ul>
      ) : null}
      {suite ? <p className="deroule-suite-renfort">{suite}</p> : null}
      {etape.defaite ? (
        <p className="deroule-defaite">
          <span aria-hidden="true">☠</span> {texteDefaite(etape)}
        </p>
      ) : null}
      {etape.bilan ? (
        <ul className="deroule-bilan">
          {etape.bilan.length === 0 ? (
            <li className="deroule-bilan-rien">{texteBilanVide()}</li>
          ) : (
            etape.bilan.map((ligne) => (
              <li key={ligne.cle}>
                <span className="deroule-bilan-fait">{texteLigneBilan(ligne)}</span>
                {compteurLigneBilan(ligne) ? (
                  <span className="deroule-bilan-compteur">{compteurLigneBilan(ligne)}</span>
                ) : null}
              </li>
            ))
          )}
        </ul>
      ) : null}
    </>
  )
}

/** Les coups d'un onglet, un bouton chacun : un clic en donne le detail. */
export function ListeDesCoups({ coups, choisir }: { coups: EtapeDeroule[]; choisir: (cle: string) => void }) {
  return (
    <ul className="deroule-relecture-liste">
      {coups.map((coup) => {
        const chiffre = resultatEtape(coup)
        return (
          <li key={coup.cle}>
            <button type="button" onClick={() => choisir(coup.cle)}>
              {titreEtape(coup)}
              {chiffre ? <span className="deroule-relecture-chiffre"> {chiffre}</span> : null}
            </button>
          </li>
        )
      })}
    </ul>
  )
}

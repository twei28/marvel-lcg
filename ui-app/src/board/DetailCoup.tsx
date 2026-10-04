// LE DETAIL D'UN COUP en lecture seule, et la liste des coups d'un onglet.
//
// Partage par la relecture d'un onglet passe (DeroulePhase) et la revue de la
// phase finie (RevuePhase, volet du journal) : decisions du 03/10/2026. Les
// phrases sont celles du cartouche (deroule-textes.ts) ; l'etape recue est deja
// mise en langue par l'appelant quand il le peut.

import type { EtapeDeroule } from './deroule-phase'
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

export function DetailCoup({ etape }: { etape: EtapeDeroule }) {
  const resultat = detailEtape(etape)
  const annulee = texteActivationAnnulee(etape)
  const cause = texteCauseActivation(etape)
  const suite = texteSuiteRenfort(etape)
  return (
    <>
      {surtitreEtape(etape) ? <p className="deroule-surtitre">{surtitreEtape(etape)}</p> : null}
      <div className="deroule-entete">
        <p className="deroule-titre">{titreEtape(etape)}</p>
      </div>
      {resultat ? <p className="deroule-resultat">{resultat}</p> : null}
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

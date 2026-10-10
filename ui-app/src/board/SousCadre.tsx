// LE SOUS-CADRE DU CARTOUCHE DU BAS (lot 4 de la refonte du 04/10/2026, scene
// PC, mode « Étape par étape »). Decisions D4, D5, D6, D31, D32, D37.
//
// Pendant la phase du mechant, une reponse, un ciblage, un paiement ou une
// confirmation se jouent ICI, par-dessus la rangee grisee de l'etape : plus
// aucun panneau hors du cartouche (DemandeCentrale, CiblesScene et
// AssistantAction restent pour la table et le telephone). La defense et le
// choix d'une carte revelee, eux, se jouent dans la rangee meme
// (CartouchePhase).
//
// Ce composant ne RETIENT rien (piege 26) et ne parle jamais au moteur en
// direct (piege 27). Il traduit chaque clic :
//  - vignette d'option → `q.choisirOption(option)` (pulse des cibles, survol
//    remis a zero, puis `interaction.choisirOption`) ;
//  - cible ou carte de la main → son `agir` (`interaction.cartes`, ou la cible
//    hors table) ;
//  - « Confirmer », « Jouer X » → `interaction.valider()` ;
//  - le refus (« Aucune réponse », « Annuler ») → `interaction.annuler()`.
// La vue (`vueSousCadre`, sous-cadre.ts) ne porte que des donnees.
//
// Convention du clavier (D37, clavier-cartouche.ts) : chaque choix porte
// `data-choix="n"` (1 a 9) et affiche « (n) », le refus porte `data-refus`.

import type { ReactNode } from 'react'
import type { ScanCardProps } from '../components/ScanCard'
import { ScanCardTraduite } from './traduction-carte'
import type { Option } from './ask'
import { avecIcones, coutEnIcones, marquerRessources, ressourcesEnMots } from './icones-ressources'
import { t } from './langue'
import { raisonDite } from './phrase-etat'
import type { CibleVue, QuestionDuMoteur, VignetteOption, VueSousCadre } from './sous-cadre'

/**
 * Une carte du cartouche : NUE, comme dans la scene d'avant. Rien de ce que le
 * monde COURANT dit d'elle (compteurs, PV, jetons) : la table peut etre en
 * avance sur le recit, et c'est la rangee qui donne les chiffres de l'etape.
 */
export function CarteNue({ scan }: { scan: ScanCardProps }) {
  return (
    <ScanCardTraduite
      {...scan}
      state={undefined}
      exhausted={false}
      counters={undefined}
      schemeThreat={undefined}
      allyHp={undefined}
      stats={undefined}
      labelType={undefined}
      camp={undefined}
      jauge={undefined}
      jetonMenace={undefined}
      jetonDegats={undefined}
      masquerType
    />
  )
}

/** Le chiffre du clavier (D37) : de 1 a 9 ; au-dela, aucun raccourci. */
function chiffreClavier(n: number): string | undefined {
  return n >= 1 && n <= 9 ? String(n) : undefined
}

/** L'option du moteur qu'une vignette porte : celles de l'interaction, puis la demande. */
export function optionDe(q: QuestionDuMoteur, optionId: number): Option | undefined {
  return (
    q.interaction.options.find((option) => option.id === optionId) ??
    q.demande.options.find((option) => option.id === optionId)
  )
}

/**
 * UNE OPTION DU MOTEUR, EN VIGNETTE CLIQUABLE : la carte qui la porte (ou
 * qu'elle nomme), son numero, son nom, et dessous son texte (D32). Une option
 * indisponible garde sa place et son numero, ne se joue pas, et dit pourquoi.
 */
export function BoutonOption({ vignette, choisir }: { vignette: VignetteOption; choisir: () => void }) {
  const classes = ['deroule-vignette', 'est-choix']
  if (!vignette.scan) classes.push('est-texte')
  if (vignette.indisponible) classes.push('est-indisponible')
  return (
    <button
      type="button"
      className={classes.join(' ')}
      data-choix={chiffreClavier(vignette.chiffre)}
      data-option-id={vignette.optionId}
      aria-label={ressourcesEnMots(vignette.nom)}
      aria-disabled={vignette.indisponible ? true : undefined}
      title={vignette.indisponible ?? vignette.sousTexte}
      onClick={() => {
        if (!vignette.indisponible) choisir()
      }}
    >
      {/* Le numero se pose sur le coin de la CARTE, pas du bouton : la
          legende, plus large que la carte, decalait le badge a cote d'elle. */}
      {vignette.scan ? (
        <span className="deroule-vignette-carte">
          <CarteNue scan={vignette.scan} />
          <span className="deroule-chiffre" aria-hidden="true">
            ({vignette.chiffre})
          </span>
        </span>
      ) : (
        <span className="deroule-chiffre" aria-hidden="true">
          ({vignette.chiffre})
        </span>
      )}
      <span className={vignette.scan ? 'deroule-legende' : 'deroule-choix-nom'}>
        {avecIcones(marquerRessources(vignette.nom))}
      </span>
      {vignette.indisponible ? (
        <span className="deroule-raison">{vignette.indisponible}</span>
      ) : vignette.sousTexte ? (
        <span className="deroule-sous-texte">{vignette.sousTexte}</span>
      ) : null}
    </button>
  )
}

/** Une cible, une carte de la main qui paie, ou un sbire a ordonner. */
function BoutonCarte({ cible, rang, agir }: { cible: CibleVue; rang: number; agir: () => void }) {
  const classes = ['deroule-vignette', 'est-choix']
  if (cible.choisie) classes.push('est-choisie')
  if (cible.pulse) classes.push('est-pulse')
  return (
    <button
      type="button"
      className={classes.join(' ')}
      data-choix={chiffreClavier(rang)}
      data-carte-id={cible.carteId}
      aria-label={cible.nom}
      aria-pressed={cible.choisie}
      onClick={agir}
    >
      <span className="deroule-vignette-carte">
        {cible.scan ? <CarteNue scan={cible.scan} /> : <span className="deroule-vignette-nom">{cible.nom}</span>}
        <span className="deroule-chiffre" aria-hidden="true">
          ({rang})
        </span>
        {cible.ordre !== undefined ? <span className="deroule-ordre">{cible.ordre}</span> : null}
        {cible.fois !== undefined && cible.fois > 1 ? <span className="deroule-fois">×{cible.fois}</span> : null}
      </span>
      {cible.scan ? <span className="deroule-legende">{cible.nom}</span> : null}
    </button>
  )
}

/**
 * Ce que le sous-cadre porte. La defense et ce qui se joue pendant elle
 * restent dans la rangee (D7, D8) : CartouchePhase ne les lui confie jamais.
 */
export type VueDuSousCadre = Exclude<VueSousCadre, { genre: 'defense' | 'pendant-defense' }>

export type SousCadreProps = {
  /** La question en donnees (`vueSousCadre`). */
  vue: VueDuSousCadre
  /** Les gestionnaires : le sous-cadre n'en a pas d'autres. */
  q: QuestionDuMoteur
}

export function SousCadre({ vue, q }: SousCadreProps) {
  const i = q.interaction
  const choisirOption = (optionId: number) => {
    const option = optionDe(q, optionId)
    if (option) q.choisirOption(option)
  }
  const agirSur = (cible: CibleVue) => {
    if (cible.horsTable) {
      i.ciblesHorsTable.find((hors) => hors.props.id === String(cible.carteId))?.agir()
      return
    }
    const etat = i.cartes.get(cible.carteId)
    if (etat?.agir) {
      etat.agir()
      return
    }
    // L'ORDRE DES SBIRES pas encore engage : le premier clic l'engage, en
    // commencant par ce sbire-la.
    if (vue.genre === 'ordre' && !i.option) {
      const ordre = i.options[0] ?? q.demande.options[0]
      if (ordre) q.choisirOption(ordre, [cible.carteId])
    }
  }

  let titre: string
  let compte: string | undefined
  let phrase: string | undefined
  let cartes: ReactNode[] = []
  let refus: string | undefined
  let valider: { libelle: string; prete: boolean } | undefined
  let cout: ReactNode

  switch (vue.genre) {
    case 'reponses':
      titre = vue.titre
      cartes = vue.choix.map((choix) => (
        <BoutonOption key={choix.optionId} vignette={choix} choisir={() => choisirOption(choix.optionId)} />
      ))
      refus = vue.refus
      break
    case 'choix-carte':
      titre = vue.intitule
      cartes = vue.choix.map((choix) => (
        <BoutonOption key={choix.optionId} vignette={choix} choisir={() => choisirOption(choix.optionId)} />
      ))
      refus = vue.refus
      break
    case 'cibles':
      titre = vue.titre
      compte = `${vue.choisies} / ${vue.maximum}${vue.minimum !== vue.maximum ? ` (${t('min')} ${vue.minimum})` : ''}`
      phrase = vue.prete || !vue.raison ? undefined : raisonDite(vue.raison)
      cartes = vue.cibles.map((cible, rang) => (
        <BoutonCarte key={`${cible.horsTable ? 'h' : 't'}${cible.carteId}`} cible={cible} rang={rang + 1} agir={() => agirSur(cible)} />
      ))
      refus = t('Annuler')
      valider = { libelle: t('Confirmer'), prete: vue.prete }
      break
    case 'ordre':
      titre = vue.titre
      cartes = vue.cibles.map((cible, rang) => (
        <BoutonCarte key={cible.carteId} cible={cible} rang={rang + 1} agir={() => agirSur(cible)} />
      ))
      // Question FORCEE : aucun refus. « Confirmer » des que l'ordre est complet.
      valider = { libelle: t('Confirmer'), prete: vue.prete }
      break
    case 'paiement':
      titre = vue.titre
      phrase = vue.phraseEtat || undefined
      cout =
        vue.coutSlots.length > 0 ? (
          <span className="deroule-cout" aria-label={t('Coût à payer')}>
            {vue.coutSlots.map((slot) => (
              <span key={slot.index} className={slot.rempli ? 'deroule-cout-pastille est-rempli' : 'deroule-cout-pastille'}>
                {slot.rempli && slot.type ? avecIcones(coutEnIcones(slot.type)) : ''}
              </span>
            ))}
          </span>
        ) : undefined
      cartes = vue.cartesMain.map((carte, rang) => (
        <BoutonCarte key={carte.carteId} cible={carte} rang={rang + 1} agir={() => agirSur(carte)} />
      ))
      refus = t('Annuler')
      valider = { libelle: vue.libelleJouer, prete: vue.prete }
      break
    case 'confirmer':
      titre = vue.titre
      phrase = vue.prete || !vue.raison ? undefined : raisonDite(vue.raison)
      refus = t('Annuler')
      valider = { libelle: t('Confirmer'), prete: vue.prete }
      break
  }

  return (
    <div className={`deroule-sous-cadre est-${vue.genre}`} role="group" aria-label={titre}>
      <div className="deroule-sous-cadre-tete">
        <strong className="deroule-sous-cadre-titre">{titre}</strong>
        {compte ? <small className="deroule-sous-cadre-compte">{compte}</small> : null}
        {vue.genre === 'paiement' && vue.consigne ? <small className="deroule-sous-cadre-compte">{vue.consigne}</small> : null}
        {cout}
        {phrase ? <small className="deroule-sous-cadre-phrase">{phrase}</small> : null}
      </div>
      {cartes.length > 0 ? <div className="deroule-sous-cadre-cartes">{cartes}</div> : null}
      <div className="deroule-boutons deroule-sous-cadre-boutons">
        {refus ? (
          <button type="button" className="bh-bouton" data-refus="" onClick={i.annuler}>
            {refus}
          </button>
        ) : null}
        {valider ? (
          <button type="button" className="bh-bouton deroule-valider" disabled={!valider.prete} onClick={i.valider}>
            {valider.libelle}
          </button>
        ) : null}
      </div>
    </div>
  )
}

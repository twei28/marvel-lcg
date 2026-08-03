// Une bande de la vue d'etat : un titre, des tuiles condensees, et une pastille
// « +N » quand le budget ne suffit pas. La pastille ouvre la bande en focus :
// c'est la seule facon d'atteindre ce qui est replie, elle n'est jamais decorative.
//
// Quand la fenetre n'a pas la hauteur de tenir six bandes avec leurs tuiles,
// PlateauMobile rend BandeResume a la place : la meme bande reduite a une seule
// ligne touchable (voir degradation.ts). Le titre reste le meme bouton, donc la
// ligne de resume ouvre la bande en focus exactement comme le titre plein.

import type { ReactNode } from 'react'
import { t } from '../langue'
import type { ScanCardProps } from '../../components/ScanCard'
import type { BandeAffichee } from './bandes'
import { condenser, type BudgetBande } from './condensation'
import { chiffresResume } from './degradation'
import { TuileCondensee } from './TuileCondensee'
import './mobile.css'

export type BandeMobileProps = {
  bande: BandeAffichee
  budget: BudgetBande
  /** Nombre de cibles legales dans cette bande pendant un ciblage. 0 = aucune pastille. */
  cibles?: number
  onOuvrirBande: () => void
  onOuvrirCarte: (carte: ScanCardProps) => void
}

/**
 * Le titre d'une bande. C'est un bouton dans les deux modes d'affichage : il
 * ouvre la bande en focus, et c'est la cible tactile de 44 px garantie par
 * .bande-titre dans mobile.css.
 */
export function TitreBande({
  titre,
  cibles,
  onOuvrirBande,
  enfants,
}: {
  titre: string
  cibles?: number
  onOuvrirBande: () => void
  enfants?: ReactNode
}) {
  return (
    <button
      type="button"
      className="bande-titre"
      onClick={onOuvrirBande}
      data-tactile="titre-bande"
    >
      <span className="bande-titre-nom">{titre}</span>
      {cibles ? (
        <span className="bande-cibles" aria-label={`${cibles} ${t('cibles ici')}`}>
          {cibles}
        </span>
      ) : null}
      {enfants}
    </button>
  )
}

export function BandeMobile({
  bande,
  budget,
  cibles,
  onOuvrirBande,
  onOuvrirCarte,
}: BandeMobileProps) {
  const unites = bande.emplacements.flatMap((emplacement) => emplacement.groupes.flat())
  const { tuiles, restantes, taille } = condenser(unites, budget)

  return (
    <section className="bande" aria-label={bande.titre}>
      <TitreBande titre={bande.titre} cibles={cibles} onOuvrirBande={onOuvrirBande} />
      <div className="bande-tuiles">
        {tuiles.map((unite) => (
          <TuileCondensee
            key={unite.cle}
            carte={unite.carte}
            taille={taille}
            onOuvrir={() => onOuvrirCarte(unite.carte)}
          />
        ))}
        {restantes > 0 ? (
          <button
            type="button"
            className="bande-surplus"
            onClick={onOuvrirBande}
            data-tactile="surplus"
            aria-label={`+${restantes} ${t('autres')}`}
          >
            +{restantes}
          </button>
        ) : null}
      </div>
    </section>
  )
}

export type BandeResumeProps = {
  bande: BandeAffichee
  cibles?: number
  onOuvrirBande: () => void
}

/**
 * La bande degradee : une seule ligne, son titre, son nombre de cartes et ses
 * chiffres cles. Elle ne montre AUCUNE tuile, donc elle ne peut rien couper ;
 * un appui ouvre la bande en focus, qui devient l'unique route vers son
 * contenu. C'est pour cela que la ligne entiere est le bouton .bande-titre.
 */
export function BandeResume({ bande, cibles, onOuvrirBande }: BandeResumeProps) {
  const unites = bande.emplacements.flatMap((emplacement) => emplacement.groupes.flat())
  const chiffres = chiffresResume(unites)

  return (
    <section className="bande bande-reduite" aria-label={bande.titre}>
      <TitreBande
        titre={bande.titre}
        cibles={cibles}
        onOuvrirBande={onOuvrirBande}
        enfants={
          <>
            <span className="bande-resume-nombre" aria-label={`${unites.length} ${t('cartes')}`}>
              {unites.length}
            </span>
            {chiffres.map((chiffre, index) => (
              <span className="bande-resume-chiffre" key={`${index}-${chiffre}`}>
                {chiffre}
              </span>
            ))}
          </>
        }
      />
    </section>
  )
}

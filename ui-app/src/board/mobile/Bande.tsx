// Une BANDE du plateau portrait : un titre, puis un rail de cartes qui defile
// horizontalement du doigt (spec du 12/09/2026). La carte epinglee reste au
// bord gauche pendant le defilement (mechant, manigance principale, identite).
//
// Chaque carte passe par `Unite`, le composant du plateau PC : attachements
// glisses sous la porteuse, statuts, piles, stades, pastilles de PV et de
// menace. On ne redessine pas une seconde fois ce qu'il sait deja faire.
//
// Le geste : TAP = ouvrir la carte en grand, APPUI LONG = agir. Le tap est
// intercepte a la capture, avant le bouton de ScanCard : sur telephone, le
// clic d'une carte ne doit jamais declencher l'action du moteur par
// surprise. Le bouton des stades (loupe) garde son clic.
import type { ReactElement, ReactNode, MouseEvent as ReactMouseEvent } from 'react'
import { kindLabel, type CardEffectDelta, type ScanCardProps } from '../../components/ScanCard'
import { t } from '../langue'
import { Unite, avecInteraction } from '../Board'
import type { EtatInteractif } from '../interaction'
import type { GroupeDePile, UniteAffichee } from '../zones'
import { useAppuiLong } from './useAppuiLong'

export type CleBande = 'vilain' | 'manigances' | 'engages' | 'heros'

type Decor = {
  interactifs: Map<number, EtatInteractif>
  effets: Map<number, CardEffectDelta>
  heroActifId?: number
  ouvrirPile: (titre: string, cartes: ScanCardProps[], groupes?: GroupeDePile[]) => void
  /** Tap : lire la carte en grand. Recoit la carte DECOREE (etat, onSelect). */
  ouvrirCarte: (carte: ScanCardProps) => void
  /** Appui long : agir avec la carte porteuse. Recoit la carte decoree. */
  agir: (carte: ScanCardProps) => void
}

function CarteBande({
  unite,
  epinglee,
  titreZone,
  decor,
}: {
  unite: UniteAffichee
  epinglee: boolean
  titreZone: string
  decor: Decor
}): ReactElement {
  const porteur = avecInteraction(unite.carte, decor.interactifs, decor.effets)
  const appui = useAppuiLong(() => decor.agir(porteur))

  const surTap = (evenement: ReactMouseEvent<HTMLDivElement>) => {
    const cible = evenement.target as HTMLElement
    if (cible.closest('.stages-bouton')) return
    const scan = cible.closest<HTMLElement>('.scan-card')
    if (!scan) return
    evenement.stopPropagation()
    evenement.preventDefault()
    // Le maintien vient d'agir : le clic qui suit le relachement du doigt ne
    // doit pas AUSSI ouvrir la carte.
    if (appui.vientDeDeclencher()) return
    const id = scan.dataset.cardId
    const carte = [unite.carte, ...unite.attachees].find((c) => String(c.id) === id) ?? unite.carte
    decor.ouvrirCarte(avecInteraction(carte, decor.interactifs, decor.effets))
  }

  return (
    <div
      className={`bande-carte${epinglee ? ' est-epinglee' : ''}`}
      data-tactile="carte"
      data-card-id={unite.carte.id}
      onClickCapture={surTap}
      {...appui.gestes}
    >
      <Unite
        unite={unite}
        interactifs={decor.interactifs}
        effets={decor.effets}
        ouvrirPile={decor.ouvrirPile}
        bloquerActionsPassives={false}
        heroActifId={decor.heroActifId}
        titreZone={titreZone}
      />
    </div>
  )
}

export function Bande({
  cle,
  titre,
  epinglee,
  unites,
  texteVide,
  onglets,
  decor,
}: {
  cle: CleBande
  titre: string
  epinglee?: UniteAffichee
  unites: UniteAffichee[]
  /** Ce que dit la bande quand elle est vide : elle garde sa hauteur. */
  texteVide: string
  /** Les onglets du multijoueur, sur la bande du heros seulement. */
  onglets?: ReactNode
  decor: Decor
}): ReactElement {
  const vide = !epinglee && unites.length === 0
  // La pastille de type est tue quand la bande la repete deja (« Mechant »
  // dans Mechant, « Heros » dans Ton heros : pastilleRedondante, zones.ts).
  // Dans Manigances, « Manigance principale » et « Manigance annexe » sont
  // tout aussi redondantes, et a trois cartes par ecran elles se marchaient
  // dessus (releve sur le S24, 12/09/2026) : la zone se declare du nom du
  // type lui-meme, ce qui la rend muette.
  const titreZoneDe = (unite: UniteAffichee): string =>
    cle === 'manigances' ? (unite.carte.labelType ?? t(kindLabel[unite.carte.kind])) : titre
  return (
    <section className={`bande bande-${cle}${vide ? ' est-vide' : ''}`} aria-label={titre}>
      <header className="bande-entete">
        <h2 className="bande-titre">{titre}</h2>
        {onglets}
      </header>
      {vide ? (
        <p className="bande-vide">{texteVide}</p>
      ) : (
        <div className="bande-rail">
          {epinglee ? <CarteBande unite={epinglee} epinglee titreZone={titreZoneDe(epinglee)} decor={decor} /> : null}
          {unites.map((unite) => (
            <CarteBande key={unite.cle} unite={unite} epinglee={false} titreZone={titreZoneDe(unite)} decor={decor} />
          ))}
        </div>
      )}
    </section>
  )
}

// La bande Heros : contrairement aux cinq autres bandes, un seul joueur y est
// deplie a la fois (spec S7). Seul terrain-soutien se decoupe par proprietaire
// (les aires de tous les joueurs y sont aplaties par zones.ts) ; les autres
// emplacements de la bande (deck special, piles, nemesis, annexes) n'existent
// que pour le siege regarde et restent toujours affiches sous le joueur
// deplie, quel qu'il soit.

import { useState } from 'react'
import { t } from '../langue'
import type { ScanCardProps } from '../../components/ScanCard'
import type { UniteAffichee } from '../zones'
import type { BandeAffichee } from './bandes'
import { condenser, type BudgetBande } from './condensation'
import { TitreBande } from './BandeMobile'
import { MESURES_PAR_DEFAUT } from './degradation'
import { groupesParJoueur, ordreDAffichage } from './joueurs'
import { TuileCondensee } from './TuileCondensee'
import './mobile.css'

/**
 * Hauteur reelle d'un bandeau replie, en pixels CSS. Vaut le min-height de
 * .bandeau-joueur dans mobile.css (44px) : box-sizing: border-box y absorbe
 * deja le padding vertical (6px * 2) et la bordure (1px * 2), ils ne
 * s'ajoutent donc pas par-dessus ces 44px.
 */
const HAUTEUR_BANDEAU_REPLIE = 44

/**
 * Ce que les bandeaux joueurs replies prennent EN PLUS des tuiles, dans la
 * meme bande. PlateauMobile s'en sert pour relever d'autant le plancher de la
 * bande Heros : sans cela, le partage au prorata pouvait lui laisser moins que
 * les 64 px de la pastille « +N » et la couper (le bug des 4 joueurs).
 *
 * `ecart` est le row-gap MESURE de .bande : chaque bandeau empile en ajoute un.
 */
export function hauteurBandeauxReplies(autresJoueurs: number, ecart: number): number {
  return autresJoueurs * (HAUTEUR_BANDEAU_REPLIE + ecart)
}

export type BandeHerosProps = {
  bande: BandeAffichee
  /**
   * Hauteur pour la bande, bandeaux replies COMPRIS : ils sont retires ici,
   * pour que ce composant reste juste meme si son appelant ne les connait pas.
   */
  budget: BudgetBande
  /** Siege regarde : c'est le joueur deplie par defaut. */
  playerId: number
  /** Nombre de cibles legales dans cette bande pendant un ciblage. */
  cibles?: number
  /**
   * row-gap MESURE de .bande. Il doit etre celui qu'a utilise l'appelant pour
   * calculer le plancher de cette bande, sinon les deux calculs divergent.
   */
  ecartGrille?: number
  onOuvrirBande: () => void
  onOuvrirCarte: (carte: ScanCardProps) => void
}

/**
 * La carte d'identite d'un joueur : la premiere unite de ses groupes dont le
 * type est hero ou alter-ego. Absente si aucune ne correspond (bandeau replie
 * de secours, voir plus bas). Exportee : ZoneFocus etiquette ses sections de
 * joueur avec exactement la meme regle, plutot que de la redecrire.
 */
export function carteIdentite(groupes: UniteAffichee[][]): ScanCardProps | undefined {
  for (const groupe of groupes) {
    for (const unite of groupe) {
      if (unite.carte.kind === 'hero' || unite.carte.kind === 'alter-ego') return unite.carte
    }
  }
  return undefined
}

export function BandeHeros({
  bande,
  budget,
  playerId,
  cibles,
  ecartGrille = MESURES_PAR_DEFAUT.ecart,
  onOuvrirBande,
  onOuvrirCarte,
}: BandeHerosProps) {
  // Le siege regarde (playerId) change au passage de tour en solo multi-heros
  // et via le selecteur de vue, mais ce composant n'est JAMAIS remonte (sa cle
  // est stable) : un useState(playerId) ne relirait son argument qu'au
  // montage, et la bande melangerait le terrain-soutien de l'ancien joueur aux
  // piles du nouveau. On memorise donc le choix explicite AVEC le siege depuis
  // lequel il a ete fait : il gagne tant que le siege ne bouge pas, et il est
  // caduc des que le siege change (spec S7 : le passage de tour deplie
  // automatiquement le heros actif).
  const [choix, setChoix] = useState({ siege: playerId, joueur: playerId })
  if (choix.siege !== playerId) {
    // Mise a jour EN COURS DE RENDU (motif documente par React pour ajuster un
    // etat quand une prop change) : React relance le rendu avant de peindre,
    // donc aucune image intermediaire ne montre l'ancien joueur. Un useEffect
    // ferait clignoter la bande une image, et surtout melangerait deux joueurs
    // le temps de cette image.
    setChoix({ siege: playerId, joueur: playerId })
  }
  const joueurDeplie = choix.siege === playerId ? choix.joueur : playerId

  const soutien = bande.emplacements.find((emplacement) => emplacement.cle === 'terrain-soutien')
  const groupesParProprietaire = soutien
    ? groupesParJoueur(soutien)
    : new Map<number, UniteAffichee[][]>()
  const joueurs = [...groupesParProprietaire.keys()]
  const ordre = ordreDAffichage(joueurs, joueurDeplie)
  const autresJoueurs = ordre.filter((joueur) => joueur !== joueurDeplie)

  const unitesTerrainSoutien = (groupesParProprietaire.get(joueurDeplie) ?? []).flat()
  const unitesAutresEmplacements = bande.emplacements
    .filter((emplacement) => emplacement.cle !== 'terrain-soutien')
    .flatMap((emplacement) => emplacement.groupes.flat())
  const unites = [...unitesTerrainSoutien, ...unitesAutresEmplacements]

  // Chaque bandeau replie occupe une vraie place dans la grille de .bande, en
  // plus des tuiles : sans cette soustraction, condenser() croit disposer de
  // toute la hauteur du budget et le surplus reel deborde silencieusement
  // sous l'overflow: hidden de .pm-bandes, au lieu d'etre replie dans le +N.
  // PlateauMobile a deja ajoute cette meme reserve au plancher de la bande :
  // ce qui reste ici est donc toujours au moins la hauteur d'une pastille.
  const hauteurReserveeBandeaux = hauteurBandeauxReplies(autresJoueurs.length, ecartGrille)
  const budgetTuiles = {
    largeur: budget.largeur,
    hauteur: Math.max(0, budget.hauteur - hauteurReserveeBandeaux),
  }

  const { tuiles, restantes, taille } = condenser(unites, budgetTuiles)

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
      {autresJoueurs.map((joueur) => {
        const identite = carteIdentite(groupesParProprietaire.get(joueur) ?? [])
        const nom = identite?.name ?? `${t('Joueur')} ${joueur}`
        return (
          <button
            key={joueur}
            type="button"
            className="bandeau-joueur"
            data-tactile="joueur-replie"
            onClick={() => setChoix({ siege: playerId, joueur })}
          >
            <span className="bandeau-joueur-nom">{nom}</span>
            {identite?.allyHp ? <span className="bandeau-joueur-pv">{identite.allyHp}</span> : null}
            {(identite?.counters ?? []).map((compteur) => (
              <span className="bandeau-joueur-compteur" key={compteur.label}>
                {compteur.label} {compteur.value}
              </span>
            ))}
          </button>
        )
      })}
    </section>
  )
}

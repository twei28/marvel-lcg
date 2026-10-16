// Les cartes qui SORTENT du deck rencontre, sur la table.
//
// Deux des trois gestes que l'utilisateur a demandés le 14/09/2026 d'après la
// phase du méchant de play.marvelsimulator.com :
//
//   « les cartes boost sortent vraiment du paquet pour se mettre à côté, pour
//     ensuite voir à combien ; idem pour la carte d'activation, elle sort du
//     paquet et elle s'affiche, et ça j'aime vraiment bien »
//
// ⚠ CE COMPOSANT NE DÉCIDE NI OÙ NI QUAND. Où : `places-rencontre.ts`, pur et
// testé. Quand : `boostsMontres`, le compteur que `DeroulePhase` tient déjà
// pour la scène centrale, et qui avance d'un boost toutes les 1,5 s SANS clic
// (« tout l'élan en une étape », choix de l'utilisateur parmi trois).
//
// ⚠ ET IL NE LIT PAS LA TABLE. Les cartes boost sont déjà parties à la défausse
// au moment où l'étape s'affiche, et la carte révélée est encore face cachée
// dans le monde de la trame retenue. Les deux viennent de `carteScene`, qui les
// sort de l'index du monde et les retourne pour nous.

import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import type { ScanCardProps } from '../components/ScanCard'
import { ScanCardTraduite } from './traduction-carte'
import type { EtapeDeroule } from './deroule-phase'
import { sceneDe } from './deroule-scene'
import { t } from './langue'
import {
  boiteDeCarte,
  boiteDuDeckRencontre,
  cadreDuPlateau,
  destinationDeLaCarte,
} from './mesures-plateau'
import { placeDeLaRevelee, placesDesBoosts, type Boite } from './places-rencontre'

/**
 * Le temps que met une carte rencontre a rejoindre sa place.
 *
 * ⚠ DEUX SECONDES, choix de l'utilisateur parmi trois : « un vrai trajet, pas
 * un saut ». C'est long pour une animation ; c'est voulu, on doit pouvoir
 * suivre la carte des yeux jusqu'a sa destination.
 */
export const DUREE_VOL_MS = 2000

export function CoucheRencontreSurTable({
  etape,
  boostsMontres,
  carteScene,
  dosRencontre,
  actif,
}: {
  etape: EtapeDeroule | undefined
  boostsMontres: number
  carteScene?: (id: number, faceVisible: boolean) => ScanCardProps | undefined
  dosRencontre?: ScanCardProps
  actif: boolean
}) {
  const [ancre, setAncre] = useState<
    { deck: Boite; cadre: Boite; attaquant: Boite | undefined } | undefined
  >(undefined)
  // Une seconde mesure au repos : au premier rendu de l'étape, les cartes de la
  // table peuvent encore être en vol.
  const [seconde, setSeconde] = useState(0)
  const cle = etape?.cle
  const auteurId = etape?.carteId

  /**
   * LA CARTE QUI S'EN VA, une fois lue.
   *
   * Demande de l'utilisateur, 14/09/2026 : « on voit la carte et on doit la
   * voir aller de là vers l'endroit où elle va se poser ». Et sur le moment :
   * « au clic : on lit, puis elle part » — elle ne s'efface pas toute seule.
   *
   * ⚠ ELLE SURVIT A SON ETAPE. Au clic, l'étape change et la carte quitterait
   * l'écran instantanément : on garde donc ICI ce qu'on montrait juste avant,
   * le temps du vol. Deux secondes, sa décision : « un vrai trajet, pas un
   * saut ».
   */
  const [sortie, setSortie] = useState<
    { props: ScanCardProps; de: Boite; vers: Boite; cle: string } | undefined
  >(undefined)
  type CarteMontree = { id: number; props: ScanCardProps; place: Boite; cle: string }
  /**
   * ⚠ DEUX MEMOIRES, ET C'EST LA CLE. `courant` est ecrit PENDANT le rendu ;
   * `precedent` n'est mis a jour que dans l'effet, APRES. Une seule memoire ne
   * pouvait pas marcher : React rend la nouvelle etape AVANT de lancer les
   * effets, si bien que la memoire portait deja la carte du pas suivant quand
   * l'effet cherchait celle du pas d'avant. Deux revelations de suite ne
   * faisaient alors voler personne. Mesure a l'ecran.
   */
  const courant = useRef<CarteMontree | undefined>(undefined)
  const precedent = useRef<CarteMontree | undefined>(undefined)

  useLayoutEffect(() => {
    if (!actif) {
      setAncre(undefined)
      return
    }
    const mesurer = () => {
      const c = cadreDuPlateau()
      if (!c) return
      const deck = boiteDuDeckRencontre(c)
      if (!deck) return
      // ⚠ L'ATTAQUANT, PAS LE PAQUET, pour poser les boosts. Il peut manquer
      // (carte detruite pendant la phase) : on retombe alors sur le paquet
      // plutot que d'inventer une position.
      setAncre({ deck, cadre: c.boite, attaquant: boiteDeCarte(auteurId, c) })
    }
    mesurer()
    window.addEventListener('resize', mesurer)
    return () => window.removeEventListener('resize', mesurer)
  }, [actif, cle, auteurId, seconde])

  useEffect(() => {
    if (!actif) return
    setSeconde(0)
    const minuteur = window.setTimeout(() => setSeconde(1), 260)
    return () => window.clearTimeout(minuteur)
  }, [actif, cle])

  // L'ETAPE A CHANGE : la carte qu'on montrait part vers sa place.
  useEffect(() => {
    const avant = precedent.current
    precedent.current = courant.current
    if (!avant || avant.cle === cle) return
    const c = cadreDuPlateau()
    const vers = c ? destinationDeLaCarte(avant.id, c) : undefined
    // Sans destination mesurable, pas de vol : la carte s'efface, plutôt que
    // de partir vers un point inventé.
    if (!vers) return
    setSortie({ props: avant.props, de: avant.place, vers, cle: avant.cle })
    const minuteur = window.setTimeout(() => setSortie(undefined), DUREE_VOL_MS + 120)
    return () => window.clearTimeout(minuteur)
  }, [cle])

  // LES BOOSTS, COORDONNÉS (16/10/2026) : « la première sort du paquet et se met au milieu ; la
  // deuxième sort du paquet et se met à côté de l'autre ; puis chacune va à côté du méchant ».
  // Chaque boost passe par trois états : `sortie` (au paquet), `centre` (lu, au milieu, en
  // grand), `range` (à sa place, à côté de l'attaquant). Tous rejoignent leur place ensemble,
  // une fois le dernier retourné et lu.
  const [etatsBoost, setEtatsBoost] = useState<Record<string, 'centre' | 'range'>>({})
  const totalBoosts = etape?.boosts.length ?? 0
  const boostsVus = etape ? Math.min(boostsMontres, totalBoosts) : 0
  useEffect(() => {
    setEtatsBoost({})
  }, [cle])
  // Un nouveau boost sorti : au rendu suivant, il part du paquet vers le milieu.
  useEffect(() => {
    if (!actif || boostsVus === 0) return
    const image = window.requestAnimationFrame(() =>
      setEtatsBoost((avant) => {
        const suivant: Record<string, 'centre' | 'range'> = { ...avant }
        for (let i = 0; i < boostsVus; i++) if (suivant[`b${i}`] === undefined) suivant[`b${i}`] = 'centre'
        return suivant
      })
    )
    return () => window.cancelAnimationFrame(image)
  }, [actif, boostsVus, cle])
  // Tous retournés : on laisse le temps de lire, puis ils rejoignent le méchant ensemble.
  useEffect(() => {
    if (!actif || totalBoosts === 0 || boostsVus < totalBoosts) return
    const minuteur = window.setTimeout(
      () =>
        setEtatsBoost((avant) => {
          const suivant: Record<string, 'centre' | 'range'> = {}
          for (const k of Object.keys(avant)) suivant[k] = 'range'
          return suivant
        }),
      1700
    )
    return () => window.clearTimeout(minuteur)
  }, [actif, boostsVus, totalBoosts, cle])

  if (!actif || !etape || !ancre) return null

  const scene = sceneDe(etape)
  // Aucune carte revelee sur cette etape : la memoire du rendu se vide, sinon
  // une carte d'une etape ancienne repartirait en vol deux etapes plus tard.
  courant.current = undefined
  const boosts = scene.cartes.filter((c) => c.role === 'boost').slice(0, boostsMontres)
  const revelee = scene.cartes.find((c) => c.role === 'revelee')

  // ⚠ LE TOTAL VIENT DES APPORTS, PAS DU MONTANT DE L'ÉTAPE. `montant` est ce
  // que la cible a ENCAISSÉ, défense déduite ; ici on annonce ce que l'élan
  // AJOUTE, ce qui est la question que se pose le joueur en regardant sortir
  // les cartes : « à combien ça monte ».
  const apport = etape.boosts
    .slice(0, boostsMontres)
    .reduce((somme, boost) => somme + (boost.apport ?? 0), 0)

  const carteNue = (props: ScanCardProps, garderType = false) => (
    // Rien de ce que le monde COURANT dit de la carte : la table peut être en
    // avance sur le récit. Même choix que la scène centrale.
    <ScanCardTraduite
      {...props}
      state={undefined}
      exhausted={false}
      counters={undefined}
      schemeThreat={undefined}
      allyHp={undefined}
      stats={undefined}
      labelType={garderType ? props.labelType : undefined}
      // 16/10/2026 : pas de petite pastille de type au-dessus des cartes montrées en grand.
      masquerType
      camp={undefined}
    />
  )

  const places = placesDesBoosts(ancre.attaquant ?? ancre.deck, ancre.cadre, boosts.length)

  return (
    <div className="rencontre-sur-table" aria-hidden="true">
      {boosts.map((carte, i) => {
        const props = carte.role === 'dos' ? dosRencontre : carteScene?.(carte.id, true)
        const place = places[i]
        if (!props || !place) return null
        // La grande taille de lecture, et la place de CE boost parmi tous ceux de l'étape,
        // alignés au milieu de la table (le total est connu d'avance : le premier ne bouge pas
        // quand le deuxième arrive).
        const echelle = Math.max(
          1.4,
          Math.min(
            3.2,
            (ancre.cadre.h * 0.42) / (place.h || 1),
            ((ancre.cadre.w * 0.8 - 16 * (totalBoosts - 1)) / Math.max(1, totalBoosts)) / (place.w || 1)
          )
        )
        const largeurLue = place.w * echelle
        const groupe = totalBoosts * largeurLue + (totalBoosts - 1) * 16
        const centreX = ancre.cadre.x + ancre.cadre.w / 2 - groupe / 2 + largeurLue / 2 + i * (largeurLue + 16)
        const centreY = ancre.cadre.y + ancre.cadre.h / 2
        const etat = etatsBoost[`b${i}`]
        const transform =
          etat === 'range'
            ? 'none'
            : etat === 'centre'
              ? `translate(${centreX - (place.x + place.w / 2)}px, ${centreY - (place.y + place.h / 2)}px) scale(${echelle})`
              : `translate(${ancre.deck.x - place.x}px, ${ancre.deck.y - place.y}px) scale(0.92)`
        return (
          <div
            key={`boost-${carte.role === 'dos' ? i : carte.id}`}
            className={`rencontre-sortie est-boost${i === boosts.length - 1 ? ' est-zoom' : ''}`}
            style={{
              left: `${place.x}px`,
              top: `${place.y}px`,
              // ⚠ `--card-w`, PAS `width` (voir `ScanCard.css`).
              '--card-w': `${place.w}px`,
              transform,
              opacity: etat === undefined ? 0 : 1,
              // Au centre, les boosts passent devant les cartes de la table ; rangés, ils redescendent.
              zIndex: etat === 'centre' ? 5 : 2,
              animation: 'none',
              transition: 'transform 900ms cubic-bezier(0.25, 0.7, 0.3, 1), opacity 240ms ease-out',
            } as React.CSSProperties}
          >
            {carteNue(props)}
          </div>
        )
      })}

      {/* Le total de l'élan, sous les cartes sorties. Il n'apparaît qu'à partir
          de deux boosts : sur un seul, la carte dit déjà tout. */}
      {boosts.length > 1 ? (
        <div
          className="rencontre-total"
          style={{
            left: `${places[0].x}px`,
            top: `${places[0].y + places[0].h + 6}px`,
            width: `${places[places.length - 1].x + places[0].w - places[0].x}px`,
          }}
        >
          {t('Élan')} +{apport}
        </div>
      ) : null}

      {/* LA CARTE QUI S'EN VA. Elle n'existe plus dans l'etape courante : c'est
          `sortie` qui la garde, le temps du trajet. */}
      {sortie ? (
        <div
          key={`sortie-${sortie.cle}`}
          className="rencontre-sortie est-depart"
          style={{
            left: `${sortie.vers.x}px`,
            top: `${sortie.vers.y}px`,
            '--card-w': `${sortie.vers.w}px`,
            // D'ou elle vient : le decalage de sa place LUE vers sa place
            // FINALE. Le meme principe que la sortie du paquet, a l'envers.
            '--depart-x': `${sortie.de.x - sortie.vers.x}px`,
            '--depart-y': `${sortie.de.y - sortie.vers.y}px`,
            '--depart-echelle': `${sortie.de.w / sortie.vers.w}`,
          } as React.CSSProperties}
        >
          {carteNue(sortie.props)}
        </div>
      ) : null}

      {revelee && revelee.role !== 'dos'
        ? (() => {
            const props = carteScene?.(revelee.id, true)
            if (!props) return null
            const place = placeDeLaRevelee(ancre.deck, ancre.cadre)
            // On retient ce qu'on montre : au prochain changement d'etape,
            // c'est cette carte-la qui partira vers sa place.
            courant.current = { id: revelee.id, props, place, cle: cle ?? '' }
            return (
              <div
                className="rencontre-sortie est-revelee"
                style={{
                  left: `${place.x}px`,
                  top: `${place.y}px`,
                  // Voir le commentaire des boosts : c'est `--card-w` qui
                  // dimensionne une ScanCard, jamais `width`.
                  '--card-w': `${place.w}px`,
                  '--depart-x': `${ancre.deck.x - place.x}px`,
                  '--depart-y': `${ancre.deck.y - place.y}px`,
                } as React.CSSProperties}
              >
                {carteNue(props, true)}
              </div>
            )
          })()
        : null}
    </div>
  )
}

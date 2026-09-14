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

import { useEffect, useLayoutEffect, useState } from 'react'
import { ScanCard, type ScanCardProps } from '../components/ScanCard'
import type { EtapeDeroule } from './deroule-phase'
import { sceneDe } from './deroule-scene'
import { t } from './langue'
import { boiteDuDeckRencontre, cadreDuPlateau } from './mesures-plateau'
import { placeDeLaRevelee, placesDesBoosts, type Boite } from './places-rencontre'

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
  const [ancre, setAncre] = useState<{ deck: Boite; cadre: Boite } | undefined>(undefined)
  // Une seconde mesure au repos : au premier rendu de l'étape, les cartes de la
  // table peuvent encore être en vol.
  const [seconde, setSeconde] = useState(0)
  const cle = etape?.cle

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
      setAncre({ deck, cadre: c.boite })
    }
    mesurer()
    window.addEventListener('resize', mesurer)
    return () => window.removeEventListener('resize', mesurer)
  }, [actif, cle, seconde])

  useEffect(() => {
    if (!actif) return
    setSeconde(0)
    const minuteur = window.setTimeout(() => setSeconde(1), 260)
    return () => window.clearTimeout(minuteur)
  }, [actif, cle])

  if (!actif || !etape || !ancre) return null

  const scene = sceneDe(etape)
  const boosts = scene.cartes.filter((c) => c.role === 'boost').slice(0, boostsMontres)
  const revelee = scene.cartes.find((c) => c.role === 'revelee')

  // ⚠ LE TOTAL VIENT DES APPORTS, PAS DU MONTANT DE L'ÉTAPE. `montant` est ce
  // que la cible a ENCAISSÉ, défense déduite ; ici on annonce ce que l'élan
  // AJOUTE, ce qui est la question que se pose le joueur en regardant sortir
  // les cartes : « à combien ça monte ».
  const apport = etape.boosts
    .slice(0, boostsMontres)
    .reduce((somme, boost) => somme + (boost.apport ?? 0), 0)

  const carteNue = (props: ScanCardProps) => (
    // Rien de ce que le monde COURANT dit de la carte : la table peut être en
    // avance sur le récit. Même choix que la scène centrale.
    <ScanCard
      {...props}
      state={undefined}
      exhausted={false}
      counters={undefined}
      schemeThreat={undefined}
      allyHp={undefined}
      stats={undefined}
      labelType={undefined}
      camp={undefined}
    />
  )

  const places = placesDesBoosts(ancre.deck, ancre.cadre, boosts.length)

  return (
    <div className="rencontre-sur-table" aria-hidden="true">
      {boosts.map((carte, i) => {
        const props = carte.role === 'dos' ? dosRencontre : carteScene?.(carte.id, true)
        const place = places[i]
        if (!props || !place) return null
        return (
          <div
            key={`boost-${carte.role === 'dos' ? i : carte.id}`}
            className="rencontre-sortie est-boost"
            style={{
              left: `${place.x}px`,
              top: `${place.y}px`,
              width: `${place.w}px`,
              height: `${place.h}px`,
              // D'où elle vient : le décalage de départ de l'animation, en
              // pixels, du paquet vers sa place. C'est CE décalage qui fait
              // « sortir du paquet » plutôt qu'« apparaître à côté ».
              '--depart-x': `${ancre.deck.x - place.x}px`,
              '--depart-y': `${ancre.deck.y - place.y}px`,
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

      {revelee && revelee.role !== 'dos'
        ? (() => {
            const props = carteScene?.(revelee.id, true)
            if (!props) return null
            const place = placeDeLaRevelee(ancre.deck, ancre.cadre)
            return (
              <div
                className="rencontre-sortie est-revelee"
                style={{
                  left: `${place.x}px`,
                  top: `${place.y}px`,
                  width: `${place.w}px`,
                  height: `${place.h}px`,
                  '--depart-x': `${ancre.deck.x - place.x}px`,
                  '--depart-y': `${ancre.deck.y - place.y}px`,
                } as React.CSSProperties}
              >
                {carteNue(props)}
              </div>
            )
          })()
        : null}
    </div>
  )
}

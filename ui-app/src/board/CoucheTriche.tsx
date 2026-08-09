// CoucheTriche.tsx — tout le mode Bac à sable, en une seule couche.
//
// Le plateau n'a que deux lignes à ajouter : appeler `useTriche(world)` et
// rendre `<CoucheTriche>`. Le clic droit est capté au niveau du DOCUMENT et
// résolu par `data-card-id`, que chaque carte porte déjà — aucune modification
// des composants de carte, aucun accessoire à faire descendre à travers le
// plateau.
//
// Ce regroupement est délibéré : le mode doit pouvoir être remanié ou retiré
// sans laisser de traces éparpillées dans un plateau de 2000 lignes.

import { useCallback, useEffect, useMemo, useState } from 'react'
import { scanUrl } from './card-model'
import { t } from './langue'
import { MenuTriche, type CibleTriche } from './MenuTriche'
import * as triche from './triche'
import type { World, WorldCard } from './world'

/** Une pile ouverte à la consultation. */
export type PileTriche = {
  titre: string
  cartes: WorldCard[]
  /** Pile du joueur : la carte part en main. Sinon : elle entre en jeu. */
  duJoueur: boolean
}

type MenuOuvert = { cible: CibleTriche; x: number; y: number }

/** Les types de cartes qui se mesurent en menace plutôt qu'en points de vie. */
const MANIGANCES = new Set(['MainScheme', 'SideScheme', 'Scheme'])
/** Ce qui ne s'incline pas et n'a pas d'état : inutile de proposer ces entrées. */
const SANS_ETAT = new Set(['Event', 'Treachery', 'Obligation', 'Resource'])

/** Parcourt le monde et indexe chaque carte par son identifiant d'objet. */
function indexer(world: World | undefined): Map<number, WorldCard> {
  const index = new Map<number, WorldCard>()
  if (!world) return index
  const parcourir = (valeur: unknown) => {
    if (Array.isArray(valeur)) {
      for (const element of valeur) parcourir(element)
      return
    }
    if (typeof valeur !== 'object' || valeur === null) return
    const objet = valeur as Record<string, unknown>
    if (typeof objet.id === 'number' && typeof objet.card_type === 'string') {
      index.set(objet.id, objet as unknown as WorldCard)
    }
    for (const enfant of Object.values(objet)) parcourir(enfant)
  }
  parcourir(world)
  return index
}

/**
 * Les quatre piles consultables, repérées par la carte qui les REPRÉSENTE à
 * l'écran — c'est-à-dire leur dessus. Un clic droit sur ce dessus doit ouvrir
 * la pile, pas le menu de la carte : sans cette distinction, on ne pourrait
 * jamais atteindre le contenu d'un deck.
 */
function pilesParDessus(
  world: World | undefined,
  joueurId: number
): Map<number, PileTriche> {
  const piles = new Map<number, PileTriche>()
  if (!world) return piles
  const joueur = world.players?.[joueurId]

  const ajouter = (cartes: WorldCard[] | undefined, titre: string, duJoueur: boolean) => {
    if (!cartes || cartes.length === 0) return
    const dessus = cartes.at(-1)
    if (dessus) piles.set(dessus.id, { titre, cartes, duJoueur })
  }

  ajouter(joueur?.player_deck, t('Deck du héros'), true)
  ajouter(joueur?.player_discard_pile, t('Pile de défausse'), true)
  ajouter(world.encounter_deck, t('Deck Rencontre'), false)
  ajouter(world.encounter_discard_pile, t('Défausse Rencontre'), false)
  return piles
}

export function useTriche(
  world: World | undefined,
  joueurId: number,
  /** Verse l'intervention dans le journal de partie. */
  ajouterAuJournal?: (libelle: string) => void
) {
  const actif = world?.mode_sandbox === true
  const [menu, setMenu] = useState<MenuOuvert | undefined>(undefined)
  const [pile, setPile] = useState<PileTriche | undefined>(undefined)
  const [interventions, setInterventions] = useState<string[]>([])

  const index = useMemo(() => (actif ? indexer(world) : new Map()), [actif, world])
  const piles = useMemo(
    () => (actif ? pilesParDessus(world, joueurId) : new Map()),
    [actif, world, joueurId]
  )

  const noter = useCallback(
    (libelle: string) => {
      setInterventions((liste) => [...liste, libelle])
      ajouterAuJournal?.(libelle)
    },
    [ajouterAuJournal]
  )

  // L'écoute vit au niveau du document : les cartes portent déjà
  // `data-card-id`, il suffit de remonter depuis la cible du clic.
  useEffect(() => {
    if (!actif) return
    const surClicDroit = (evenement: MouseEvent) => {
      const cible = evenement.target as HTMLElement | null
      const noeud = cible?.closest?.('[data-card-id]') as HTMLElement | null
      if (!noeud) return
      const id = Number(noeud.getAttribute('data-card-id'))
      if (!Number.isFinite(id)) return

      evenement.preventDefault()

      const pileVisee = piles.get(id)
      if (pileVisee) {
        setPile(pileVisee)
        return
      }

      const carte = index.get(id)
      if (!carte) return
      setMenu({
        cible: {
          id,
          nom: carte.name || `${t('Carte')} ${id}`,
          estManigance: MANIGANCES.has(carte.card_type),
          estPersonnage: !SANS_ETAT.has(carte.card_type),
        },
        x: evenement.clientX,
        y: evenement.clientY,
      })
    }
    document.addEventListener('contextmenu', surClicDroit)
    return () => document.removeEventListener('contextmenu', surClicDroit)
  }, [actif, index, piles])

  return { actif, interventions, couche: { menu, pile, setMenu, setPile, noter } }
}

export type CoucheTricheProps = {
  actif: boolean
  couche: ReturnType<typeof useTriche>['couche']
}

export function CoucheTriche({ actif, couche }: CoucheTricheProps) {
  const { menu, pile, setMenu, setPile, noter } = couche
  if (!actif) return null

  const agirSurCarte = async (carte: WorldCard, mode: 'defaut' | 'reveler') => {
    if (!pile) return
    const reussi = pile.duJoueur
      ? await triche.envoyerEnMain(carte.id)
      : mode === 'reveler'
        ? await triche.reveler(carte.id)
        : await triche.mettreEnJeu(carte.id)
    const quoi = pile.duJoueur
      ? t('Ajoutée à la main')
      : mode === 'reveler'
        ? t('Révélée')
        : t('Mise en jeu')
    noter(`${quoi} — ${carte.name}${reussi ? '' : ` (${t('refusé')})`}`)
    setPile(undefined)
  }

  return (
    <>
      {/* Le bandeau : on ne doit JAMAIS se demander si une partie était truquée. */}
      <div className="bandeau-triche" role="status">
        <span className="bandeau-triche-marque">{t('Bac à sable')}</span>
        <span className="bandeau-triche-aide">
          {t('Clic droit sur une carte ou une pile')}
        </span>
      </div>

      {menu ? (
        <MenuTriche
          cible={menu.cible}
          x={menu.x}
          y={menu.y}
          onFermer={() => setMenu(undefined)}
          onIntervention={noter}
        />
      ) : null}

      {pile ? (
        <div className="pile-triche-voile" onPointerDown={() => setPile(undefined)}>
          <section
            className="pile-triche"
            role="dialog"
            aria-label={pile.titre}
            onPointerDown={(evenement) => evenement.stopPropagation()}
          >
            <header className="pile-triche-entete">
              <h2>
                {pile.titre} <small>({pile.cartes.length})</small>
              </h2>
              <span className="pile-triche-aide">
                {pile.duJoueur
                  ? t('Choisis une carte pour l’ajouter à ta main')
                  : t('Choisis une carte pour la mettre en jeu')}
              </span>
              <button type="button" onClick={() => setPile(undefined)}>{t('Fermer')}</button>
            </header>

            <div className="pile-triche-cartes">
              {pile.cartes.length === 0 ? (
                <p className="pile-triche-vide">{t('Cette pile est vide')}</p>
              ) : (
                pile.cartes.map((carte, rang) => (
                  <span className="pile-triche-carte" key={`${carte.id}-${rang}`}>
                    <img src={scanUrl(carte.pic_id)} alt={carte.name} loading="lazy" />
                    <span className="pile-triche-actions">
                      <button type="button" onClick={() => void agirSurCarte(carte, 'defaut')}>
                        {pile.duJoueur ? t('En main') : t('Mettre en jeu')}
                      </button>
                      {/* « Révéler » : la carte suit le cheminement normal
                          d'une carte Rencontre au lieu d'être posée
                          directement. C'est l'échappatoire prévue quand le
                          placement automatique ne convient pas. */}
                      {!pile.duJoueur ? (
                        <button type="button" onClick={() => void agirSurCarte(carte, 'reveler')}>
                          {t('Révéler')}
                        </button>
                      ) : null}
                    </span>
                  </span>
                ))
              )}
            </div>
          </section>
        </div>
      ) : null}
    </>
  )
}

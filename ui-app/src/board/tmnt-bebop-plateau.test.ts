// Bebop & Rocksteady (TMNT, `tk`) : ce que le plateau DESSINE.
// PROCESSUS-CARTE étape 8 bis, pour les cartes qui changent ce qu'on VOIT :
//  - tk001a/tk001b, tk003a/tk003b : un vilain qui se RETOURNE (ALERT <-> K.O.) garde
//    son rang et ses attachements ;
//  - tk007a/tk007b, tk008a/tk008b : le Temper (attachement permanent à deux faces) porte
//    des jetons « knucklehead » (affichés « andouille ») et se retourne ROWDY <-> ENRAGED ;
//  - tk006a/tk006b : l'environnement Destructive Dunderheads se RETOURNE en attachement
//    Gone Berserk et CHANGE DE ZONE (de l'environnement au vilain restant) ;
//  - tk101 + tk106-tk109 : cartes « Linked » mises en jeu depuis la zone de côté.
//
// L'état d'arrivée est posé à la main, sur le modèle de `paibok-plateau.test.ts` ; il
// reprend la forme publiée par le moteur (identifiants d'objet, `bind_object_id`, clés
// `c_<compteur>` de `info`) relevée sur `scenario bebop_rocksteady` le 16/10/2026 par les
// cas de `tools/cas/tmnt_bebop.py` (états de fin de cas : tk006a vaincu, tk007b, tk005a).
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World, WorldCard } from './world'

const HEROS = 1
const BEBOP = 84
const ROCKSTEADY = 85
const HOG = 87
const RHINO = 88
const DUNDERHEADS = 86
const COMPLOT = 48
const WTTJ = 89

const bebop = (face: 'tk001a' | 'tk001b' = 'tk001a'): WorldCard =>
  carteSurTable(BEBOP, face, 'EncounterVillain', 'Bebop', { info: { max_health: 15, health: 15 } })
const rocksteady = (face: 'tk003a' | 'tk003b' = 'tk003a'): WorldCard =>
  carteSurTable(ROCKSTEADY, face, 'EncounterVillain', 'Rocksteady', { info: { max_health: 17, health: 17 } })
const hog = (face: 'tk007a' | 'tk007b' = 'tk007a', jetons = 0): WorldCard =>
  carteSurTable(HOG, face, 'Attachment', face === 'tk007a' ? 'Hog Wild' : 'Headfirst', {
    bind_object_id: BEBOP,
    info: jetons ? { c_knucklehead: jetons } : {},
  })
const rhino = (face: 'tk008a' | 'tk008b' = 'tk008a', jetons = 0): WorldCard =>
  carteSurTable(RHINO, face, 'Attachment', face === 'tk008a' ? 'Rhino Rage' : 'Headstrong', {
    bind_object_id: ROCKSTEADY,
    info: jetons ? { c_knucklehead: jetons } : {},
  })

const mondeDeDepart = (surcharge: Partial<World> = {}): World =>
  tableAvec(
    siege({ area_hero: [carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man')] }),
    {
      area_villain: [bebop(), hog(), rocksteady(), rhino()],
      area_environment: [carteSurTable(DUNDERHEADS, 'tk006a', 'Environment', 'Destructive Dunderheads')],
      area_schemes_main: [carteSurTable(COMPLOT, 'tk005b', 'MainScheme', 'Demolition Crew')],
      area_schemes_side: [carteSurTable(WTTJ, 'tk101', 'SideScheme', 'Welcome to the Jungle')],
      ...surcharge,
    } as Partial<World>
  )

const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })
const scan = (carte: WorldCard) => toScanCard(carte, contexte())

describe('tk001a / tk003a : les deux vilains et leur Temper', () => {
  // tk005a : « Put ... Hog Wild attachment, and Rhino Rage attachment into play ».
  it('dessine Bebop ET Rocksteady, chacun porteur de son Temper', () => {
    for (const id of [BEBOP, ROCKSTEADY]) expect(dessinee(mondeDeDepart(), id)).toBeDefined()
    expect(dessinee(mondeDeDepart(), HOG)?.portePar).toBe(BEBOP)
    expect(dessinee(mondeDeDepart(), RHINO)?.portePar).toBe(ROCKSTEADY)
  })

  it('un Temper ne passe pas sur le mauvais vilain (témoin)', () => {
    expect(dessinee(mondeDeDepart(), HOG)?.portePar).not.toBe(ROCKSTEADY)
    expect(dessinee(mondeDeDepart(), RHINO)?.portePar).not.toBe(BEBOP)
  })
})

describe('tk007a / tk007b : jetons knucklehead et retournement du Temper', () => {
  it('Hog Wild montre ses jetons, en français « andouille »', () => {
    const jetons = scan(hog('tk007a', 2)).counters?.find((c) => c.cle === 'knucklehead')
    expect(jetons?.value).toBe(2)
  })

  it('Hog Wild sans jeton ne dessine aucun compteur', () => {
    expect(scan(hog('tk007a', 0)).counters?.find((c) => c.cle === 'knucklehead')).toBeUndefined()
  })

  // « flip this card to its ENRAGED side » : la face dessinée est Headfirst, au même rang, jetons gardés.
  it('Headfirst (face ENRAGED) est dessiné à la place de Hog Wild, accroché à Bebop, avec ses 3 jetons', () => {
    const monde = mondeDeDepart({
      area_villain: [bebop(), hog('tk007b', 3), rocksteady(), rhino()],
    } as Partial<World>)
    const vue = dessinee(monde, HOG)
    expect(vue?.codeCarte).toBe('tk007b')
    expect(vue?.portePar).toBe(BEBOP)
    expect(vue?.compteurs['knucklehead']).toBe(3)
  })

  it('le nom français du compteur est « andouille »', () => {
    const etiquette = scan(hog('tk007a', 1)).counters?.find((c) => c.cle === 'knucklehead')?.label
    expect(etiquette?.toLowerCase()).toContain('andouille')
  })
})

describe('tk001b / tk003b : vilains K.O.', () => {
  // « flip Bebop and Rocksteady to their K.O. sides » : la face K.O. remplace la face ALERT.
  it('dessine la face K.O. des deux vilains et garde leur Temper (ROWDY)', () => {
    const monde = mondeDeDepart({
      area_villain: [bebop('tk001b'), hog('tk007a', 3), rocksteady('tk003b'), rhino('tk008a', 3)],
    } as Partial<World>)
    expect(dessinee(monde, BEBOP)?.codeCarte).toBe('tk001b')
    expect(dessinee(monde, ROCKSTEADY)?.codeCarte).toBe('tk003b')
    expect(dessinee(monde, HOG)?.portePar).toBe(BEBOP)
    expect(dessinee(monde, RHINO)?.portePar).toBe(ROCKSTEADY)
  })

  it('témoin : en ALERT, la face dessinée est celle de départ', () => {
    expect(dessinee(mondeDeDepart(), BEBOP)?.codeCarte).toBe('tk001a')
  })
})

describe('tk006a / tk006b : Destructive Dunderheads se retourne en Gone Berserk et change de zone', () => {
  // Bebop vaincu : lui et son Temper sont mis de côté, l'environnement se retourne et
  // s'accroche à Rocksteady (état relevé en fin du cas « Bebop vaincu » du harnais).
  const apres = () =>
    tableAvec(
      siege({ area_hero: [carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man')] }),
      {
        area_villain: [
          rocksteady(),
          rhino(),
          carteSurTable(DUNDERHEADS, 'tk006b', 'Attachment', 'Gone Berserk!', { bind_object_id: ROCKSTEADY }),
        ],
        area_environment: [],
        area_schemes_main: [carteSurTable(COMPLOT, 'tk005b', 'MainScheme', 'Demolition Crew')],
      } as Partial<World>
    )

  it('Gone Berserk est dessiné, accroché à Rocksteady, et plus dans la zone Environnement', () => {
    const vue = dessinee(apres(), DUNDERHEADS)
    expect(vue).toBeDefined()
    expect(vue?.portePar).toBe(ROCKSTEADY)
    expect(vue?.codeCarte).toBe('tk006b')
    expect(vue?.zone).not.toBe('terrain-environnement')
  })

  it('Bebop et son Temper ne sont plus dessinés (mis de côté)', () => {
    expect(dessinee(apres(), BEBOP)).toBeUndefined()
    expect(dessinee(apres(), HOG)).toBeUndefined()
  })

  it('témoin : avant, Destructive Dunderheads est dans la zone Environnement', () => {
    const vue = dessinee(mondeDeDepart(), DUNDERHEADS)
    expect(vue).toBeDefined()
    expect(vue?.portePar).toBe(0)
  })

  it('aucune carte dessinée en double (Rocksteady est dessiné une seule fois)', () => {
    const vues = cartesDessinees(apres()).filter((c) => c.id === ROCKSTEADY)
    expect(vues).toHaveLength(1)
  })
})

describe('tk101 + tk106-tk109 : cartes Linked mises en jeu', () => {
  // « Each player may choose 1 set-aside NYC card and put it into play » : Eastman Theater
  // arrive dans la zone des soutiens, Power Play dans celle des manigances de joueur.
  it('Eastman Theater (soutien) est dessiné dans la zone des soutiens du joueur', () => {
    const monde = tableAvec(
      siege({
        area_hero: [carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man')],
        supports: [carteSurTable(120, 'tk107', 'Support', 'Eastman Theater')],
      })
    )
    expect(dessinee(monde, 120)?.zone).toBe('terrain-soutien')
  })

  it('une carte de côté (Channel 6 News) n est PAS dessinée sur la table', () => {
    const monde = tableAvec(
      siege({
        area_hero: [carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man')],
        set_aside_deck: [carteSurTable(121, 'tk106', 'Support', 'Channel 6 News', { is_face_up: false, visible_for_players: [] })],
      })
    )
    expect(dessinee(monde, 121)?.zone).not.toBe('terrain-soutien')
  })
})

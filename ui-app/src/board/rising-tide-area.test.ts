// La Rising Tide area (pack Wave) dessine-t-elle vraiment ce que le moteur y
// place ?
//
// Étape 8 bis de `docs/reference/PROCESSUS-CARTE.md` : `tools/test_capacites.py`
// a déjà prouvé que le moteur pose bien les cartes dans `player.rising_tide`
// (16/16 cas verts, pack Wave, 22/09/2026), mais un moteur vert ne prouve rien
// sur le rendu — leçon de Contingency Plan (`attachement-en-chaine.test.ts`) :
// une zone jamais dessinée à l'écran reste injouable même quand le moteur est
// juste. Ce fichier est la moitié manquante pour la Rising Tide area, jamais
// vérifiée avant ce cas.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import { toScanCard } from './card-model'
import { catalogueVide } from './catalogue'

const IDENTITE = 1
const FACE_VISIBLE = 10
const FACE_CACHEE = 11

const monde = () =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(IDENTITE, '65001b', 'AlterEgo', 'Pearl Pangan')],
      rising_tide: [
        carteSurTable(FACE_VISIBLE, '65003', 'Event', 'Crashing Wave', {
          is_face_up: true,
        }),
        // ⚠ La Rising Tide area N'EST PAS « comme en main » (contrairement à
        // la Réserve du pack brawn) : l'insert du pack le dit explicitement,
        // « an area, rather than a deck ». Une carte face cachée qui s'y
        // trouve n'est donc PAS automatiquement visible à son propriétaire
        // (`Card.IsVisible`, moteur) : `visible_for_players: []` reproduit
        // fidèlement ce que le serveur envoie réellement (recherche moteur,
        // journal de portage du 22/09/2026, § « Point OUVERT »).
        carteSurTable(FACE_CACHEE, '65005', 'Event', 'Instinctive Flow', {
          is_face_up: false,
          visible_for_players: [],
        }),
      ],
    })
  )

describe('Rising Tide area (pack Wave)', () => {
  it('dessine une carte posée dans player.rising_tide', () => {
    // C'est la SEULE assertion qui aurait attrapé le défaut de Contingency
    // Plan : une carte absente de `cartesDessinees` n'est nulle part à
    // l'écran, quel que soit le reste.
    expect(dessinee(monde(), FACE_VISIBLE)).toBeDefined()
  })

  it('la dessine dans l emplacement rising-tide, pas ailleurs', () => {
    expect(dessinee(monde(), FACE_VISIBLE)?.zone).toBe('rising-tide')
  })

  it('une carte face visible montre sa vraie face, ni peeking ni facedown', () => {
    const carte = dessinee(monde(), FACE_VISIBLE)
    expect(carte?.codeCarte).toBe('65003')
    expect(carte?.peeking).toBe(false)
    expect(carte?.facedown).toBe(false)
  })

  it('une carte face cachée ET invisible pour ce siège ne montre que le dos (jamais peeking)', () => {
    // Différence de fond avec la Réserve (`bw002` etc.) : celle-ci porte
    // `dansLaMain: true` et ses cartes face cachée s'affichent `peeking`
    // (encadré en pointillés, visibles au propriétaire). La Rising Tide area
    // n'a PAS cette permission : une carte face cachée y reste un dos de
    // carte générique pour son propre propriétaire, exactement ce que
    // l'insert du pack exige.
    const carte = dessinee(monde(), FACE_CACHEE)
    expect(carte).toBeDefined()
    expect(carte?.facedown).toBe(true)
    expect(carte?.peeking).toBe(false)
    expect(carte?.codeCarte).toBeUndefined()
  })

  it('les deux cartes de la zone sont bien dessinées ensemble, sans en perdre une', () => {
    const vues = cartesDessinees(monde()).filter((c) => c.zone === 'rising-tide')
    expect(vues.map((c) => c.id).sort()).toEqual([FACE_CACHEE, FACE_VISIBLE].sort())
  })

  // ⚠ PLANTAGE VU EN PRODUCTION LE 24/09/2026, en boucle continue dès l'entrée
  // en jeu de Wave (Pearl Pangan) : `Cache.LoadImage` (moteur) recevait un
  // `card_id` vide et faisait planter la route d'images à chaque tentative du
  // client. Racine cliente trouvée dans `toScanCard` (`card-model.ts`) :
  // `down_card_ids[0] ?? 'no_image'` laisse passer une CHAINE VIDE (`??` ne
  // rattrape que `null`/`undefined`, pas `''`), et `scanUrl('')` construit
  // `/scan/` — exactement la requête qui faisait tomber le serveur. `??` est
  // remplacé par `||` dans le correctif ; ce cas le prouve directement, sans
  // dépendre de la façon dont `down_card_ids[0]` finit par valoir `''` côté
  // moteur (raison exacte non retrouvée malgré une partie Wave réelle rejouée
  // en local).
  it('une carte cachée avec down_card_ids[0] vide retombe sur le dos générique, jamais sur /scan/ tout court', () => {
    const carte = carteSurTable(FACE_CACHEE, '65005', 'Event', 'Instinctive Flow', {
      is_face_up: false,
      visible_for_players: [],
      down_card_ids: [''],
    })
    const rendu = toScanCard(carte, { playerId: 0, actives: new Set(), catalogue: catalogueVide })
    expect(rendu.imageUrl).not.toBe('/scan/')
    expect(rendu.imageUrl).toBe('/scan/no_image')
  })
})

// Lyja (Kajislav, pack skrull_menace) : ce que le plateau DESSINE.
// PROCESSUS-CARTE étape 8 bis, pour les deux cartes du pack qui changent ce
// qu'on voit : sk066 Paibok (une traîtrise défaussée est ATTACHÉE FACE CACHÉE à
// lui) et sk056 Invisible Woman (un jeton « revelation » posé sur la cible de
// son pouvoir de base).
//
// Les formes ne sont pas inventées : elles reprennent un descripteur CAPTURÉ le
// 15/10/2026 (`tools/sonde_campagne.py` pointée sur `.game-src`, scénario rhino,
// deck lyja), après ces commandes Puzzle : PutIntoPlay sk066, EmptyEncounterDeck,
// CreateEncounterDeck 01103/01112, Discard 01112, PutIntoPlay sk056 (sous
// contrôle), Attack sk056. Relevé :
//
//   world.area_villain       : id=49 01094 EncounterVillain {max_health:14, health:13, c_revelation:1}
//   joueur.allies            : id=39 sk056 Ally (Invisible Woman) {max_health:2, health:2}
//   joueur.engaged_enemies   : id=3  sk066 Minion (Paibok)
//                              id=83 01112 (False Alarm, traîtrise) is_face_up:false bind=3
import { describe, expect, it } from 'vitest'
import { construirePlateau } from './zones'
import { catalogueVide } from './catalogue'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'
import type { World } from './world'

const RHINO = 49
const INVISIBLE_WOMAN = 39
const PAIBOK = 3
const TRAITRISE_SOUS_PAIBOK = 83

const monde = (surcharges: { traitriseAttachee?: boolean } = {}): World =>
  tableAvec(
    siege({
      allies: [carteSurTable(INVISIBLE_WOMAN, 'sk056', 'Ally', 'Invisible Woman', { info: { max_health: 2, health: 2 } })],
      engaged_enemies: [
        carteSurTable(PAIBOK, 'sk066', 'Minion', 'Paibok', { info: { max_health: 4, health: 4 } }),
        carteSurTable(TRAITRISE_SOUS_PAIBOK, '01112', 'Treachery', 'False Alarm', {
          is_face_up: false,
          bind_object_id: surcharges.traitriseAttachee === false ? 0 : PAIBOK,
          down_card_ids: ['encounter'],
        }),
      ],
    }),
    {
      area_villain: [
        carteSurTable(RHINO, '01094', 'EncounterVillain', 'Rhino', {
          info: { max_health: 14, health: 13, c_revelation: 1 },
        }),
      ],
    } as Partial<World>
  )

function compteursDe(world: World, id: number) {
  const plateau = construirePlateau(world, { playerId: 0, catalogue: catalogueVide })
  for (const e of plateau.emplacements)
    for (const g of e.groupes) for (const u of g) if (Number(u.carte.id) === id) return u.carte.counters ?? []
  throw new Error(`carte ${id} absente du plateau`)
}

describe('Lyja (Kajislav) : ce que ses cartes dessinent', () => {
  // sk066 Paibok : « attach it facedown to Paibok instead ». La traîtrise
  // doit être DESSINÉE (toBeDefined : l'assertion qui aurait attrapé
  // Contingency Plan), portée par Paibok et face cachée.
  it('la traîtrise attachée à Paibok est dessinée, portée par lui, face cachée', () => {
    const carte = dessinee(monde(), TRAITRISE_SOUS_PAIBOK)
    expect(carte).toBeDefined()
    expect(carte?.portePar).toBe(PAIBOK)
    expect(carte?.peeking || carte?.facedown).toBe(true)
  })

  // Témoin : sans lui, un plateau qui dessinerait TOUT en racine passerait le
  // premier cas. La traîtrise attachée ne doit pas apparaître comme sbire séparé.
  it("TEMOIN : la traîtrise attachée n'est pas une racine séparée, Paibok l'est", () => {
    const racines = cartesDessinees(monde()).filter((c) => c.portePar === 0).map((c) => c.id)
    expect(racines).not.toContain(TRAITRISE_SOUS_PAIBOK)
    expect(racines).toContain(PAIBOK)
  })

  // sk056 Invisible Woman : le jeton « revelation » posé sur Rhino se voit.
  it('Rhino montre son jeton revelation', () => {
    expect(compteursDe(monde(), RHINO)).toContainEqual(expect.objectContaining({ cle: 'revelation', value: 1 }))
  })

  it('Invisible Woman, elle, est dessinée dans la zone des alliés', () => {
    expect(dessinee(monde(), INVISIBLE_WOMAN)).toBeDefined()
  })

  // Contre-cas : détachée (état cassé), la traîtrise redevient une racine et le
  // premier cas tombe : c'est ce qui prouve que le test mesure bien le lien.
  it("ETAT CASSE : sans lien bind, la traîtrise n'est plus portée par Paibok", () => {
    expect(dessinee(monde({ traitriseAttachee: false }), TRAITRISE_SOUS_PAIBOK)?.portePar).not.toBe(PAIBOK)
  })
})

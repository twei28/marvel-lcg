// Photographic Reflexes (60040a/b/c, pack fne, Echo) : ce que la table DESSINE
// et ce qu'elle rend CLIQUABLE. Étape 8 bis de PROCESSUS-CARTE.md, réserve du
// 21/09/2026 levée le 20/10/2026 (backlog 13).
//
// La carte crée deux gestes que le joueur doit TROUVER à l'écran :
//   - chemin A : une action portée par une carte de la MAIN (« discard
//     Photographic Reflexes from your hand to play an event tucked under
//     Echo ») ;
//   - chemin B : l'événement glissé sous Echo devient jouable, à 2 de moins.
// `test_capacites` prouvait que le moteur offre les deux ; rien ne prouvait
// que le plateau les montre.
//
// ⚠ LA FIXTURE N'EST PAS ÉCRITE À LA MAIN. Elle sort du moteur, par le cas
// « 60040a 60040b 60040c Photographic Reflexes — etape 8 bis » de
// `tools/test_capacites.py` (vérificateur `echo_rendu_pour_le_plateau`) lancé
// avec ECHO_FIXTURE_DIR : le monde est celui de `ToDescriptor.World` (ce que
// sert `/get_world`, réduit au siège 0 sans ses decks), les options celles de
// `Effect.Render` (ce que sert `/get_ask`). Position : Echo en forme héros,
// Haymaker (01087) joué puis glissé sous elle par Watch and Learn, les trois
// variantes en main. Pour la régénérer : relancer ce cas avec
// ECHO_FIXTURE_DIR=<dossier>, puis recopier le JSON ici.
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { act, renderHook } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { lireDemande, type Demande } from './ask'
import { catalogueVide } from './catalogue'
import { useInteraction } from './interaction'
import { cartesDessinees, dessinee } from './plateau-de-test'
import type { World } from './world'
import { construirePlateau } from './zones'

const ici = dirname(fileURLToPath(import.meta.url))
const fixture = JSON.parse(
  readFileSync(join(ici, '__fixtures__/echo-photographic-reflexes.json'), 'utf8')
) as { monde: World; options: Array<Record<string, unknown>>; identite: number }

const monde = fixture.monde
const ECHO = fixture.identite
type CarteBrute = { id: number; card_id: string }
const carteDe = (zone: 'hand_cards' | 'area_hero', cardId: string): number => {
  const cartes = (monde.players[0] as unknown as Record<string, CarteBrute[]>)[zone]
  const trouvee = cartes.find((c) => c.card_id === cardId)
  if (!trouvee) throw new Error(`${cardId} absent de ${zone} dans la fixture`)
  return trouvee.id
}
const REFLEXES = ['60040a', '60040b', '60040c'].map((c) => carteDe('hand_cards', c))
const HAYMAKER = carteDe('area_hero', '01087')

function demande(options = fixture.options): Demande {
  return lireDemande({
    options_json: JSON.stringify(options),
    prompt_text: '',
    event_name: 'echo-8-bis',
    show_cancel: true,
    ability_type: '',
  })!
}

function interaction(d: Demande, mode: 'simple' | 'detailed' = 'simple') {
  const { idsAffiches } = construirePlateau(monde, { playerId: 0, catalogue: catalogueVide })
  return renderHook(() => useInteraction(monde, d, vi.fn(), idsAffiches, 0, catalogueVide, mode))
}

describe('Photographic Reflexes : ce que le joueur voit', () => {
  it('dessine les trois variantes dans la main', () => {
    for (const id of REFLEXES) expect(dessinee(monde, id), `carte ${id}`).toBeDefined()
  })

  it('dessine Haymaker glissé SOUS Echo, posé face cachée mais lisible par son propriétaire', () => {
    const carte = dessinee(monde, HAYMAKER)
    expect(carte).toBeDefined()
    expect(carte?.portePar).toBe(ECHO)
    expect(carte?.peeking).toBe(true)
    expect(carte?.facedown).toBe(false)
  })

  it('chemin A : chaque variante en main est CLIQUABLE, porteuse de son action', () => {
    const { result } = interaction(demande())
    for (const id of REFLEXES) {
      const etat = result.current.cartes.get(id)
      expect(etat?.role, `carte ${id}`).toBe('porteur')
      expect(etat?.agir, `carte ${id}`).toBeTypeOf('function')
    }
  })

  it('chemin A, mode Détaillé : un clic sur la carte de la main choisit SON action, pas celle d une autre variante', () => {
    const { result } = interaction(demande(), 'detailed')
    const deuxieme = REFLEXES[1]
    act(() => result.current.cartes.get(deuxieme)!.agir!())
    expect(result.current.option?.bind_id).toBe(deuxieme)
    expect(result.current.option?.name).toBe('Hero_Action')
  })

  it('chemin B : Haymaker glissé est CLIQUABLE sous Echo, à coût réduit à 0', () => {
    const { result } = interaction(demande())
    const etat = result.current.cartes.get(HAYMAKER)
    expect(etat?.role).toBe('porteur')
    expect(etat?.agir).toBeTypeOf('function')
    const jouer = demande().options.find((o) => o.bind_id === HAYMAKER)
    expect(jouer?.target_payment[0]?.cost).toBe('0')
  })

  // Témoin : le moteur n'offre PAS l'action (module de 60040a absent, forme
  // civile). Sans lui, une table qui rendrait toute carte de la main cliquable
  // passerait les cas ci-dessus.
  it('témoin : sans option du moteur, aucune variante n est cliquable', () => {
    const sansReflexes = fixture.options.filter((o) => !REFLEXES.includes(Number(o.bind_id)))
    const { result } = interaction(demande(sansReflexes))
    for (const id of REFLEXES) expect(result.current.cartes.get(id)?.agir, `carte ${id}`).toBeUndefined()
    // Et le monde reste dessiné à l'identique : c'est bien le CLIC qui disparaît.
    expect(cartesDessinees(monde).length).toBeGreaterThan(REFLEXES.length)
  })
})

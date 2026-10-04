// Le texte d'une capacite proposee par le moteur (voir texte-capacite.ts).
import { describe, expect, it } from 'vitest'
import { extraireCapacite, nettoyerTexteCarte } from './texte-capacite'

const JENNIFER =
  '"I Object!" — <b>Interrupt</b>: When threat would be placed on a scheme, prevent 1 of that threat. (Limit once per round.)'
const SPIDER_MAN = 'Spider-Sense — <b>Interrupt</b>: When the villain initiates an attack against you, draw 1 card.'
const ULTRON =
  '[star] <b>Forced Response</b>: After Ultron attacks you, choose to either place 1 threat on the main scheme or put the top card of your deck into play facedown, engaged with you as a [[Drone]] minion.'
const DEUX_CAPACITES =
  '<b>Action</b>: Exhaust Beat Cop &#8594; move 1 threat from a scheme to here.\n<b>Action</b>: Exhaust and discard Beat Cop &#8594; deal 1 damage to a minion for each threat here.'
const HERO_ET_INTERRUPT =
  'Legal Practice — <b>Alter-Ego Action</b>: Exhaust She-Hulk → remove 2 threat.\n"I Object!" — <b>Interrupt</b>: When threat would be placed on a scheme, prevent 1 of that threat.'

describe('nettoyerTexteCarte', () => {
  it('retire les balises, garde les fleches, les traits et l’etoile', () => {
    expect(nettoyerTexteCarte(ULTRON)).toBe(
      '★ Forced Response: After Ultron attacks you, choose to either place 1 threat on the main scheme or put the top card of your deck into play facedown, engaged with you as a Drone minion.'
    )
    expect(nettoyerTexteCarte(DEUX_CAPACITES.split('\n')[0]!)).toBe('Action: Exhaust Beat Cop → move 1 threat from a scheme to here.')
  })
})

describe('nettoyerTexteCarte, jetons de ressource', () => {
  it('garde les jetons de ressource (a un crochet) pour qu’ils deviennent des icones', () => {
    expect(nettoyerTexteCarte('<b>Spend</b> [[energy]][[mental]][[physical]] or exhaust a [[Drone]]')).toBe(
      'Spend [energy][mental][physical] or exhaust a Drone'
    )
    expect(nettoyerTexteCarte('ressources : [energy] [mental]')).toBe('ressources : [energy] [mental]')
  })
})

describe('extraireCapacite', () => {
  it('rend tout le texte quand la carte n’a qu’une capacite', () => {
    expect(extraireCapacite(JENNIFER, '"I_Object!"', 'Interrupt')).toBe(
      '"I Object!" — Interrupt: When threat would be placed on a scheme, prevent 1 of that threat. (Limit once per round.)'
    )
    expect(extraireCapacite(SPIDER_MAN, 'Spider-Sense', 'Interrupt')).toContain('draw 1 card')
  })

  it('retrouve la capacite par le nom de l’option du moteur, soulignes et guillemets compris', () => {
    expect(extraireCapacite(HERO_ET_INTERRUPT, '"I_Object!"', 'Interrupt')).toBe(
      '"I Object!" — Interrupt: When threat would be placed on a scheme, prevent 1 of that threat.'
    )
    expect(extraireCapacite(HERO_ET_INTERRUPT, 'Legal_Practice', 'Alter-Ego Action')).toContain('remove 2 threat')
  })

  it('a defaut de nom, prend le paragraphe du type de la demande', () => {
    expect(extraireCapacite(HERO_ET_INTERRUPT, 'Interrupt', 'Interrupt')).toContain('prevent 1 of that threat')
  })

  it('sans rien pour trancher, rend tout : mieux vaut trop que rien', () => {
    expect(extraireCapacite(DEUX_CAPACITES, 'Play', 'Normal')).toContain('move 1 threat')
    expect(extraireCapacite(DEUX_CAPACITES, 'Play', 'Normal')).toContain('deal 1 damage')
  })

  it('retrouve le paragraphe FRANCAIS depuis le type anglais du moteur', () => {
    const jenniferFr =
      '"<i>Objection !</i>" — <b>Interruption</b> : quand de la menace est censée être placée sur une manigance, prévenez 1 de ces menaces. (Limite d\'une fois par round.)\n<b>Action d\'alter-ego</b> : piochez 1 carte.'
    expect(extraireCapacite(jenniferFr, '"I_Object!"', 'Interrupt')).toBe(
      '"Objection !" — Interruption : quand de la menace est censée être placée sur une manigance, prévenez 1 de ces menaces. (Limite d\'une fois par round.)'
    )
    expect(extraireCapacite(jenniferFr, 'Alter-Ego_Action', 'Alter-Ego Action')).toBe("Action d'alter-ego : piochez 1 carte.")
    const ultronFr =
      '<b>Réponse forcée</b> : après qu\'Ultron vous a attaqué, choisissez.\n<b>Action de héros</b> : autre chose.'
    expect(extraireCapacite(ultronFr, 'Forced_Response', 'Forced Response')).toContain('après qu')
    expect(extraireCapacite(ultronFr, 'Hero_Action', 'Hero Action')).toBe('Action de héros : autre chose.')
  })

  it('rien sans texte', () => {
    expect(extraireCapacite(undefined, 'Interrupt', 'Interrupt')).toBeUndefined()
    expect(extraireCapacite('   ', 'Interrupt', 'Interrupt')).toBeUndefined()
  })
})

// Le cas signalé en jeu : « RESOLVE MULLIGANS » affiché en plein milieu d'une
// interface française. Ces tests verrouillent la traduction ET sa limite — un
// nom de capacité imprimé sur la carte doit rester en anglais.
import { afterEach, describe, expect, it } from 'vitest'
import { tonaliteAction } from './action-style'
import { traduireMoteur } from './vocabulaire-moteur'

const enFrancais = () => window.localStorage.setItem('marvel-langue', 'fr')
const enAnglais = () => window.localStorage.setItem('marvel-langue', 'en')

afterEach(() => window.localStorage.clear())

describe('traduireMoteur', () => {
  it('traduit le libellé signalé en jeu', () => {
    enFrancais()
    expect(traduireMoteur('Resolve Mulligans')).toBe('Résoudre les mulligans')
  })

  it('traduit le choix facultatif d un script (signalement Yarro n43, Ben Urich)', () => {
    enFrancais()
    expect(traduireMoteur('Discard one')).toBe('En défausser une')
    expect(traduireMoteur('Cancel')).toBe('Annuler')
    enAnglais()
    expect(traduireMoteur('Discard one')).toBe('Discard one')
  })

  it('traduit le choix de Robbie Robertson 60156 (meme defaut que Ben Urich)', () => {
    enFrancais()
    expect(traduireMoteur('Discard it and deal another')).toBe('La défausser et en distribuer une autre')
  })

  it('traduit le choix du mot-clé Starting (signalement Yarro n°70)', () => {
    enFrancais()
    expect(traduireMoteur('Add this card to your starting hand')).toBe('Ajouter cette carte à ta main de départ')
  })

  it('traduit les choix de la campagne Skrull Menace (cooperation, zone, campagne experte)', () => {
    enFrancais()
    expect(traduireMoteur('Discard the top card of your deck to place Skrull Warrior in the victory display')).toBe(
      'Défausser le dessus de ton deck pour placer Skrull Warrior dans la pile de victoire'
    )
    expect(traduireMoteur('Cooperation Area: add a card (PlayerSideScheme)')).toBe(
      'Zone de coopération : ajouter une carte (manigance annexe de joueur)'
    )
    expect(traduireMoteur('Place 1 acceleration token on the main scheme to heal to full')).toContain('te soigner complètement')
    enAnglais()
    expect(traduireMoteur('Discard the top card of your deck to place Skrull Warrior in the victory display')).toBe(
      'Discard the top card of your deck to place Skrull Warrior in the victory display'
    )
  })

  it('traduit les choix de Venus (compteurs de dragage)', () => {
    enFrancais()
    expect(traduireMoteur('Remove 2 dredge counters to draw 3 cards')).toBe('Retirer 2 compteurs de dragage pour piocher 3 cartes')
    expect(traduireMoteur('Remove 2 dredge counters to confuse and stun an enemy')).toContain('désorienter et sonner')
    enAnglais()
    expect(traduireMoteur('Remove 2 dredge counters to draw 3 cards')).toBe('Remove 2 dredge counters to draw 3 cards')
  })

  it('traduit les deux branches de l obligation de Jennika (tj012)', () => {
    enFrancais()
    expect(traduireMoteur('Place 3 threat on the main scheme. Discard this obligation')).toBe(
      'Placer 3 menaces sur la manigance principale. Défausser cette obligation'
    )
    expect(traduireMoteur('Exhaust Jenny → remove Personality Adjustment from the game')).toBe(
      'Incliner Jenny → retirer Personality Adjustment de la partie'
    )
    enAnglais()
    expect(traduireMoteur('Place 3 threat on the main scheme. Discard this obligation')).toBe(
      'Place 3 threat on the main scheme. Discard this obligation'
    )
  })

  it('traduit les pouvoirs de base', () => {
    enFrancais()
    expect(traduireMoteur('Attack')).toBe('Attaquer')
    expect(traduireMoteur('Thwart')).toBe('Contrer')
    expect(traduireMoteur('Defense')).toBe('Défendre')
    expect(traduireMoteur('Recover')).toBe('Récupérer')
    expect(traduireMoteur('Change Form')).toBe('Changer de forme')
  })

  it('reprend le vocabulaire officiel des mots-clés', () => {
    enFrancais()
    expect(traduireMoteur('Quickstrike')).toBe('Coup Rapide')
    expect(traduireMoteur('Retaliate')).toBe('Riposte')
    expect(traduireMoteur('Surge')).toBe('Renfort')
    expect(traduireMoteur('Toughness')).toBe('Ténacité')
  })

  it('laisse intact un nom de capacité écrit sur la carte', () => {
    enFrancais()
    // Le scan affiché est anglais : traduire le bouton casserait le lien.
    expect(traduireMoteur('The Power of the Mind')).toBe('The Power of the Mind')
  })

  it("ne touche à rien quand l'interface est en anglais", () => {
    enAnglais()
    expect(traduireMoteur('Resolve Mulligans')).toBe('Resolve Mulligans')
    expect(traduireMoteur('Attack')).toBe('Attack')
  })

  it('traduit la capacité dupliquée en la numérotant pour un humain', () => {
    enFrancais()
    // Le moteur écrit `Attack_1` pour la SECONDE occurrence (effect.py) ;
    // `nomLisible` l'a déjà transformée en « Attack 1 ».
    expect(traduireMoteur('Attack 1')).toBe('Attaquer (2)')
  })

  it('ne numérote pas ce qu’il ne connaît pas', () => {
    enFrancais()
    expect(traduireMoteur('Mystic Blast 1')).toBe('Mystic Blast 1')
  })
})

describe('traduireMoteur : les choix imprimés par les scripts de cartes (D4, 05/10/2026)', () => {
  it('traduit les choix les plus fréquents, nombre compris', () => {
    enFrancais()
    expect(traduireMoteur('Take 2 damage')).toBe('Subir 2 dégâts')
    expect(traduireMoteur('Take 1 damage')).toBe('Subir 1 dégât')
    expect(traduireMoteur('Take 2 indirect damage')).toBe('Subir 2 dégâts indirects')
    expect(traduireMoteur('Place 1 threat on the main scheme')).toBe('Placer 1 menace sur la manigance principale')
    expect(traduireMoteur('Place 2 threat here')).toBe('Placer 2 menaces ici')
    expect(traduireMoteur('Draw 1 card')).toBe('Piocher 1 carte')
    expect(traduireMoteur('Draw 2 cards')).toBe('Piocher 2 cartes')
    expect(traduireMoteur('Deal 3 damage to an enemy')).toBe('Infliger 3 dégâts à un ennemi')
    expect(traduireMoteur('Remove 2 threat from a scheme')).toBe('Retirer 2 menaces d’une manigance')
    expect(traduireMoteur('Stun an enemy')).toBe('Rendre un ennemi sonné')
    expect(traduireMoteur('Confuse an enemy')).toBe('Rendre un ennemi désorienté')
  })

  it('laisse en anglais un choix inconnu (le texte de la carte reste le repère)', () => {
    enFrancais()
    expect(traduireMoteur('Take damage equal to Juggernaut\'s ATK')).toBe('Take damage equal to Juggernaut\'s ATK')
  })

  it('traduit les deux choix de Proxima Midnight (21092)', () => {
    enFrancais()
    expect(traduireMoteur('deal 1 damage to Avengers Tower')).toBe('Infliger 1 dégât à la tour des Avengers')
    expect(traduireMoteur('Deal 2 damage to your identity')).toBe('Infliger 2 dégâts à ton identité')
    expect(traduireMoteur('Proxima Midnight gets +2 ATK for this attack')).toBe(
      'Proxima Midnight gagne +2 ATQ pour cette attaque'
    )
  })

  it("ne touche à rien en anglais", () => {
    enAnglais()
    expect(traduireMoteur('Take 2 damage')).toBe('Take 2 damage')
  })
})

describe('tonaliteAction — les couleurs survivent à la traduction', () => {
  it('reconnaît les libellés français', () => {
    expect(tonaliteAction('Attaquer')).toBe('attack')
    expect(tonaliteAction('Contrer')).toBe('thwart')
    expect(tonaliteAction('Récupérer')).toBe('recover')
    expect(tonaliteAction('Défendre')).toBe('defense')
    expect(tonaliteAction('Changer de forme')).toBe('change')
    expect(tonaliteAction('Jouer')).toBe('play')
    expect(tonaliteAction('Réponse forcée')).toBe('ability')
  })

  it('reconnaît toujours les libellés anglais', () => {
    expect(tonaliteAction('Attack')).toBe('attack')
    expect(tonaliteAction('Thwart')).toBe('thwart')
    expect(tonaliteAction('Recover')).toBe('recover')
    expect(tonaliteAction('Defense')).toBe('defense')
    expect(tonaliteAction('Change Form')).toBe('change')
    expect(tonaliteAction('play')).toBe('play')
    expect(tonaliteAction('Forced Response')).toBe('ability')
  })

  it('retombe sur la tonalité neutre pour un nom de carte', () => {
    expect(tonaliteAction('Mystic Blast')).toBe('general')
  })
})

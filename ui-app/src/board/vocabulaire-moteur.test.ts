// Le cas signalé en jeu : « RESOLVE MULLIGANS » affiché en plein milieu d'une
// interface française. Ces tests verrouillent la traduction ET sa limite — un
// nom de capacité imprimé sur la carte doit rester en anglais.
import { afterEach, describe, expect, it } from 'vitest'
import { tonaliteAction } from './action-style'
import { sansIndexDeCapacite, traduireMoteur } from './vocabulaire-moteur'

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

  it('traduit les choix de Bebop & Rocksteady (ordre des deux activations, vilain visé)', () => {
    enFrancais()
    expect(traduireMoteur('Choose which villain activates first against Spider-Man')).toBe(
      'Choisis le méchant qui s’active d’abord contre Spider-Man'
    )
    expect(traduireMoteur('Choose Bebop or Rocksteady')).toBe('Choisis Bebop ou Rocksteady')
    enAnglais()
    expect(traduireMoteur('Choose which villain activates first against Spider-Man')).toBe(
      'Choose which villain activates first against Spider-Man'
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

  it('ne numérote jamais une capacité dupliquée (demande du 22/10/2026 : plus de « Action 1 / Action 2 »)', () => {
    enFrancais()
    // Le moteur écrit `Attack_1` pour la SECONDE occurrence (effect.py) ; l'index interne n'a aucun sens
    // pour un joueur. Les actions d'une même carte se distinguent par leur paragraphe (`nomActionParlant`).
    expect(traduireMoteur('Attack 1')).toBe('Attaquer')
    expect(sansIndexDeCapacite('Hero Action 1')).toBe('Hero Action')
    expect(sansIndexDeCapacite('Action 2')).toBe('Action')
    expect(sansIndexDeCapacite('Spend 1 resource')).toBe('Spend 1 resource')
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

describe('Build Support (rapport BL-Stark du 23/10/2026)', () => {
  it('le choix de recherche d un soutien est en francais', () => {
    expect(traduireMoteur('Search their deck and discard pile for a support with a cost of 3 or less and put it into play')).toBe(
      'Chercher un soutien de coût 3 ou moins dans ton deck ou ta défausse et le mettre en jeu'
    )
  })
})

describe('changer vers une forme nommee', () => {
  it('Ant-Man : le trait distinctif devient « forme Géant / Minuscule » ; un nom de forme reste tel quel', () => {
    expect(traduireMoteur('Change To GIANT')).toBe('Passer en forme Géant')
    expect(traduireMoteur('Change To TINY')).toBe('Passer en forme Minuscule')
    expect(traduireMoteur('Change To Spider-Man')).toBe('Passer en Spider-Man')
  })
})

describe('New Ultimate Winter Soldier (uw, 25/10/2026) : les choix des cartes de defausse au hasard', () => {
  it('traduit les boutons de Wild Slash, Berserker Fury, Mission Objective, Live with the Burden, Desperate Regenerate, Phoenix Specimen', () => {
    enFrancais()
    expect(traduireMoteur('Take 1 damage → deal 3 damage to an enemy')).toBe('Subir 1 dégât → infliger 3 dégâts à un ennemi')
    expect(traduireMoteur('Take 2 damage → repeat this ability')).toBe('Subir 2 dégâts → répéter cette capacité')
    expect(traduireMoteur('Take 1 damage → attach this card to another minion')).toBe('Subir 1 dégât → attacher cette carte à un autre sbire')
    expect(traduireMoteur('Exhaust your identity → prevent 2 of that damage')).toBe('Incliner ton identité → prévenir 2 de ces dégâts')
    expect(traduireMoteur('Discard each stunned and confused status card from your identity')).toBe(
      'Défausser chaque carte d’état Sonné et Désorienté de ton identité'
    )
    expect(traduireMoteur('Place 3 threat on a scheme')).toBe('Placer 3 menaces sur une manigance')
    enAnglais()
    expect(traduireMoteur('Place 3 threat on a scheme')).toBe('Place 3 threat on a scheme')
  })
})

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

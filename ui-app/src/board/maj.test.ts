// La règle de détection d'une nouvelle version, éprouvée sur les deux formes
// d'empreinte réellement servies par le jeu.
import { describe, expect, it } from 'vitest'
import { doitProposerRechargement, empreinteDe, PERIODE_MAJ_MS } from './maj'

describe('empreinteDe', () => {
  it('lit le nom haché du plateau', () => {
    const html = '<script type="module" crossorigin src="/app/assets/board-BLVkgumq.js"></script>'
    expect(empreinteDe(html)).toBe('board-BLVkgumq.js')
  })

  it('lit la chaîne de requête de l’assistant', () => {
    const html = '<script type="module" src="/public/js/prepare/app.js?v=d36dcac3"></script>'
    expect(empreinteDe(html)).toBe('d36dcac3')
  })

  it('rend une chaîne vide quand il n’y a rien à lire', () => {
    expect(empreinteDe('<html><body>Introuvable</body></html>')).toBe('')
    expect(empreinteDe('')).toBe('')
  })
})

describe('doitProposerRechargement', () => {
  it('propose quand l’empreinte servie a changé', () => {
    expect(doitProposerRechargement('board-AAAA.js', 'board-BBBB.js')).toBe(true)
  })

  it('ne propose rien quand c’est la même', () => {
    expect(doitProposerRechargement('board-AAAA.js', 'board-AAAA.js')).toBe(false)
  })

  // ⚠ LE CAS QUI COMPTE LE PLUS. Une empreinte vide veut dire qu'on n'a pas su
  // lire : page d'erreur, réseau de travers, page qui a changé de forme.
  // Proposer un rechargement là-dessus ferait tourner le joueur en rond.
  it('⚠ ne propose RIEN quand on ne sait pas', () => {
    expect(doitProposerRechargement('', 'board-BBBB.js')).toBe(false)
    expect(doitProposerRechargement('board-AAAA.js', '')).toBe(false)
    expect(doitProposerRechargement('', '')).toBe(false)
  })
})

it('la vérification est espacée : un déploiement n’est pas une urgence', () => {
  expect(PERIODE_MAJ_MS).toBeGreaterThanOrEqual(60_000)
})

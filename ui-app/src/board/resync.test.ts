// Le filet de resynchronisation : quand renvoyer l'accusé de la trame courante.
// On teste la décision pure `doitRenvoyerAccuse`, cœur du filet (voir le bug
// du mulligan jamais proposé en coop, moteur.ts / DELAI_FILET_RESYNC_MS).
import { describe, it, expect } from 'vitest'
import { doitRenvoyerAccuse } from './moteur'

const base = {
  connecte: true,
  aDemande: false,
  gameOver: false,
  multijoueur: false,
  playerId: 0,
  siegesNonAcquittes: [0] as number[] | undefined,
}

describe('doitRenvoyerAccuse — le filet de resync', () => {
  it('renvoie quand le serveur dit qu’un siège est en retard (hot-seat)', () => {
    expect(doitRenvoyerAccuse({ ...base, multijoueur: false, siegesNonAcquittes: [1] })).toBe(true)
  })

  it('ne renvoie rien si personne n’est en retard', () => {
    expect(doitRenvoyerAccuse({ ...base, siegesNonAcquittes: [] })).toBe(false)
  })

  it('ne renvoie rien tant que le moteur ne publie pas la liste (undefined)', () => {
    expect(doitRenvoyerAccuse({ ...base, siegesNonAcquittes: undefined })).toBe(false)
  })

  it('ne renvoie rien si le client est déconnecté (la reconnexion s’en charge)', () => {
    expect(doitRenvoyerAccuse({ ...base, connecte: false })).toBe(false)
  })

  it('ne renvoie rien si le moteur nous pose une question : c’est au joueur d’agir', () => {
    expect(doitRenvoyerAccuse({ ...base, aDemande: true })).toBe(false)
  })

  it('ne renvoie rien une fois la partie finie', () => {
    expect(doitRenvoyerAccuse({ ...base, gameOver: true })).toBe(false)
  })

  describe('en multijoueur, seul NOTRE siège compte', () => {
    it('renvoie si notre siège est dans la liste', () => {
      expect(doitRenvoyerAccuse({ ...base, multijoueur: true, playerId: 1, siegesNonAcquittes: [1] })).toBe(true)
    })

    it('ne renvoie rien si c’est un AUTRE siège qui est en retard', () => {
      // C'est à ce siège-là de renvoyer le sien ; renvoyer le nôtre, déjà
      // accusé, ne débloquerait rien et ferait du bruit.
      expect(doitRenvoyerAccuse({ ...base, multijoueur: true, playerId: 0, siegesNonAcquittes: [1] })).toBe(false)
    })
  })
})

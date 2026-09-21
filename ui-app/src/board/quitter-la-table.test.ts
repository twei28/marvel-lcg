// « Quitter la partie » ferme la table, et le plateau doit le dire avant.
//
// ⚠ POURQUOI CE MODULE EXISTE. Le bouton ne faisait que naviguer vers
// `/prepare.html` : le moteur gardait son monde chargé, l'emplacement restait
// pris, et le salon des invités — qui bascule dès que la table porte UNE
// partie — expédiait les arrivants sur l'ANCIENNE avant même qu'ils aient
// choisi leur héros. Deux soirées perdues les 19 et 20/09/2026.
//
// ⚠ ET LE DANGER EST LA PAGE MORTE. Une seconde après la fermeture, le moteur
// n'existe plus : toute adresse qu'il servirait (`/prepare.html`, `/`) serait
// morte avec lui. Le seul atterrissage valable est celui que le SITE donne.
//
// ⚠ TROIS ISSUES, JAMAIS DEUX. Les écraser en « c'est fermé / ce n'est pas
// fermé » fait dire au plateau quelque chose de faux : le site révoque et
// lance l'extinction AVANT de répondre, donc son silence ne veut pas dire
// qu'il n'a rien fait. C'est ce que mesurent les cas « inconnue ».
import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  PLAFOND_LECTURE_SITE_MS,
  fermerLaTable,
  laTablePeutAvoirEteFermee,
  lienAccueil,
  lireLeSite,
  natureDuDepart,
} from './quitter-la-table'

const SITE = 'https://exemple.test'
const CONNU = { connu: true, url: SITE }
const LOCAL = { connu: true, url: '' }
const INCONNU = { connu: false, url: '' }

afterEach(() => {
  vi.unstubAllGlobals()
  vi.useRealTimers()
})

/**
 * Une réponse HTTP minimale, comme `fetch` la rend.
 *
 * ⚠ LE STATUT EST OBLIGATOIRE dès qu'on sort du 200 : `ok` seul ne distingue
 * pas un 403 du moteur (« ce siège n'est pas celui de l'hôte ») d'un 502 de
 * Caddy (« ce moteur est mort »), et ces deux-là ne racontent pas du tout la
 * même histoire au joueur.
 */
function reponse(corps: unknown, statut = 200): Response {
  return {
    ok: statut >= 200 && statut < 300,
    status: statut,
    json: async () => corps,
  } as Response
}

/** Se placer sur une adresse donnée, le temps d'un cas. */
function surLAdresse(href: string) {
  const url = new URL(href)
  vi.stubGlobal('location', {
    protocol: url.protocol,
    hostname: url.hostname,
    port: url.port,
    href,
  } as Location)
}

describe('ce qu’on annonce avant de fermer', () => {
  it('l’hôte d’une table du site : la fermeture, en toutes lettres', () => {
    expect(natureDuDepart({ siege: 0, spectateur: false, site: CONNU })).toBe('fermeture')
  })

  it('⚠ un INVITÉ ne ferme pas la table de l’hôte', () => {
    // Le moteur le refuserait de toute façon (403), mais c'est ici que se
    // décide ce qu'on lui ANNONCE : lui promettre la fermeture serait un
    // mensonge, et lui annoncer les autres déconnectés, une frayeur.
    expect(natureDuDepart({ siege: 1, spectateur: false, site: CONNU })).toBe('simple')
  })

  it('un spectateur ne ferme rien non plus', () => {
    expect(natureDuDepart({ siege: 0, spectateur: true, site: CONNU })).toBe('simple')
  })

  it('sans site derrière, il n’y a aucune table à rendre', () => {
    // Partie locale (JOUER-SOLO.bat) : personne ne tient d'emplacement, et
    // `/prepare.html` reste vivant puisque le moteur ne s'éteint pas.
    expect(natureDuDepart({ siege: 0, spectateur: false, site: LOCAL })).toBe('simple')
  })

  it('⚠ site INCONNU n’est pas « pas de site » : on le dit au joueur', () => {
    // LE CAS QUI RÉTABLISSAIT LE DÉFAUT EN SILENCE. Un hoquet réseau sur la
    // lecture de l'adresse faisait passer l'hôte pour un joueur local : il
    // voyait l'ancienne fenêtre, partait, et la table restait debout avec
    // l'ancienne partie dedans — c'est-à-dire le défaut d'origine, rétabli
    // sans que personne ne puisse le savoir.
    expect(natureDuDepart({ siege: 0, spectateur: false, site: INCONNU })).toBe('incertain')
  })

  it('mais un invité reste un invité, même adresse inconnue', () => {
    expect(natureDuDepart({ siege: 1, spectateur: false, site: INCONNU })).toBe('simple')
  })
})

describe('l’adresse du site, lue une fois', () => {
  it('se lit auprès du moteur, qui seul la connaît', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => reponse({ url: SITE })))
    expect(await lireLeSite()).toEqual({ connu: true, url: SITE })
    expect(fetch).toHaveBeenCalledWith('/get_site_url', expect.anything())
  })

  it('« aucun site » est une réponse, pas un échec', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => reponse({ url: '' })))
    expect(await lireLeSite()).toEqual({ connu: true, url: '' })
  })

  it('⚠ un échec laisse l’adresse INCONNUE, jamais « aucun site »', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('coupé') }))
    expect(await lireLeSite()).toEqual({ connu: false, url: '' })
  })

  it('une réponse en erreur laisse l’adresse inconnue elle aussi', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => reponse({}, 500)))
    expect(await lireLeSite()).toEqual({ connu: false, url: '' })
  })

  it('⚠ est PLAFONNÉE : un moteur qui traîne ne suspend rien', async () => {
    // Sans plafond, la lecture reste pendue et le bouton paraît mort — au
    // moment précis où ça rame, c'est-à-dire quand on clique « Menu ».
    let abandon: AbortSignal | undefined
    vi.stubGlobal('fetch', vi.fn((_cible: string, options: RequestInit) => {
      abandon = options.signal ?? undefined
      return new Promise<Response>((_resoudre, rejeter) => {
        abandon?.addEventListener('abort', () => rejeter(new Error('abandon')))
      })
    }))
    const lecture = lireLeSite(20)
    expect(await lecture).toEqual({ connu: false, url: '' })
    expect(abandon?.aborted).toBe(true)
  })

  it('le plafond par défaut est court : il est dans le chemin d’un clic', () => {
    expect(PLAFOND_LECTURE_SITE_MS).toBeLessThanOrEqual(3000)
  })
})

describe('fermer la table', () => {
  it('le demande au moteur, en POST', async () => {
    vi.stubGlobal('fetch', vi.fn(async () =>
      reponse({ issue: 'fermee', url: SITE + '/arret' })))
    const depart = await fermerLaTable()
    expect(fetch).toHaveBeenCalledWith('/quitter_la_table', expect.objectContaining({
      method: 'POST',
    }))
    expect(depart).toEqual({ issue: 'fermee', url: SITE + '/arret' })
  })

  it('⚠ ne déclare RIEN fermé sans adresse où atterrir', async () => {
    // La gate, et elle n'est pas théorique : annoncer la fermeture sans lieu
    // où renvoyer le joueur le laisserait sur une page du moteur qu'on vient
    // de tuer. Pas d'adresse, pas de fermeture — mais pas de démenti non
    // plus : l'issue devient inconnue.
    vi.stubGlobal('fetch', vi.fn(async () => reponse({ issue: 'fermee', url: '' })))
    expect(await fermerLaTable()).toEqual({ issue: 'inconnue', url: '' })
  })

  it('« il n’y avait rien à fermer » se distingue de tout le reste', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => reponse({ issue: 'sans-site', url: '' })))
    expect(await fermerLaTable()).toEqual({ issue: 'sans-site', url: '' })
  })

  it('un 403 se dit comme un refus : le moteur a répondu, rien n’a bougé', async () => {
    // La SEULE issue où l'on peut affirmer que rien n'a bougé : le moteur est
    // vivant, il a examiné la demande et l'a rejetée avant d'appeler personne.
    vi.stubGlobal('fetch', vi.fn(async () => reponse({ error: 'not the host' }, 403)))
    expect(await fermerLaTable()).toEqual({ issue: 'refusee', url: '' })
  })

  it('⚠ un 502 n’est PAS un refus : c’est un moteur qui n’est plus là', async () => {
    // LE MENSONGE QUI AVAIT RECULÉ D'UN CRAN SANS DISPARAÎTRE. Le plateau
    // parle au moteur à travers Caddy : un moteur mort, ou en train de
    // s'éteindre, rend 502. Le compter comme un refus affichait « Rien n'a été
    // touché » et proposait de « rester sur la partie » à l'hôte d'une table
    // qui venait de disparaître — et le chemin y menait tout seul : issue
    // inconnue, « Rester ici », la table finit de s'éteindre, on reclique.
    vi.stubGlobal('fetch', vi.fn(async () => reponse({}, 502)))
    expect(await fermerLaTable()).toEqual({ issue: 'inconnue', url: '' })
  })

  it('un 401 non plus : un cookie périmé ne prouve rien sur la table', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => reponse({}, 401)))
    expect(await fermerLaTable()).toEqual({ issue: 'inconnue', url: '' })
  })

  it('⚠ un moteur injoignable laisse l’issue INCONNUE, pas « rien n’a bougé »', async () => {
    // LE MENSONGE À NE PAS DIRE. `/api/eteindre` révoque le mot de passe et
    // lance l'extinction AVANT de répondre : il n'existe aucun chemin
    // d'abandon côté site. Un silence ne prouve donc pas que la table est
    // encore là — c'est même le contraire qui est probable.
    vi.stubGlobal('fetch', vi.fn(async () => { throw new Error('coupé') }))
    expect(await fermerLaTable()).toEqual({ issue: 'inconnue', url: '' })
  })

  it('et l’adresse du site voyage avec l’issue inconnue', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => reponse({ issue: 'inconnue', url: SITE })))
    expect(await fermerLaTable()).toEqual({ issue: 'inconnue', url: SITE })
  })
})

describe('la phrase « l’hôte a peut-être fermé la table »', () => {
  // ⚠ ELLE N'A PAS TOUJOURS UN SENS, et le bandeau de reconnexion, qui ne
  // reçoit qu'un état de socket, ne peut pas le deviner tout seul.
  it('a un sens pour un invité d’une table du site', () => {
    expect(laTablePeutAvoirEteFermee({ siege: 1, spectateur: false, site: CONNU })).toBe(true)
  })

  it('et pour un spectateur, qui n’a fermé personne', () => {
    expect(laTablePeutAvoirEteFermee({ siege: 0, spectateur: true, site: CONNU })).toBe(true)
  })

  it('⚠ mais PAS pour l’hôte : c’est lui qui l’aurait fermée', () => {
    expect(laTablePeutAvoirEteFermee({ siege: 0, spectateur: false, site: CONNU })).toBe(false)
  })

  it('⚠ ni en partie locale : il n’y a ni hôte ni table', () => {
    // JOUER-SOLO.bat, sur 127.0.0.1 : la phrase parlerait de gens qui
    // n'existent pas.
    expect(laTablePeutAvoirEteFermee({ siege: 0, spectateur: false, site: LOCAL })).toBe(false)
    expect(laTablePeutAvoirEteFermee({ siege: 1, spectateur: false, site: LOCAL })).toBe(false)
  })

  it('ni tant qu’on ignore d’où vient la table', () => {
    expect(laTablePeutAvoirEteFermee({ siege: 1, spectateur: false, site: INCONNU })).toBe(false)
  })
})

describe('l’accueil déduit de l’adresse courante', () => {
  it('retire le sous-domaine de la table', () => {
    surLAdresse('https://p3.narwhalchampions.com/app/board.html?p=1')
    expect(lienAccueil()).toBe('https://narwhalchampions.com/')
  })

  it('⚠ ne découpe PAS une adresse IP', () => {
    // `127.0.0.1` donnait `http://0.0.1/`. Le défaut est ancien, mais il
    // n'apparaissait qu'après une demi-minute de coupure ; il est désormais
    // offert plus tôt, et sert de dernier recours au départ volontaire.
    surLAdresse('http://127.0.0.1:2345/app/board.html')
    expect(lienAccueil()).toBe('http://127.0.0.1:2345/')
  })

  it('⚠ et ne perd pas le port', () => {
    surLAdresse('http://localhost:2345/app/board.html')
    expect(lienAccueil()).toBe('http://localhost:2345/')
  })

  it('un domaine sans sous-domaine reste lui-même', () => {
    surLAdresse('https://narwhalchampions.com/app/board.html')
    expect(lienAccueil()).toBe('https://narwhalchampions.com/')
  })
})

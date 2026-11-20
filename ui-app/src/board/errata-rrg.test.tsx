// Les ERRATA officiels (Rules Reference 1.8, Annexe V) posés sur les cartes : la table est complète, chaque carte existe dans
// cards.json, les textes EN et FR sont renseignés et cohérents avec la base, la pastille s'affiche, et rien ne s'affiche hors
// agrandissement (les petites cartes de la table n'importent pas l'errata).
import { readdirSync, readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { renderToStaticMarkup } from 'react-dom/server'
import { describe, expect, it } from 'vitest'
import { CODES_ERRATA, erratumDeCarte, texteErratum } from './errata-rrg'
import { NoteErrata, PastilleErrata } from './PastilleErrata'
import { TEXTES_FR_COMPLETS } from './textes-fr-complets'
import { TraductionSurCarte } from './traduction-carte'

type Fiche = { card_id?: string; text?: string; full_link?: string; ability_link?: string }
const CARDS = JSON.parse(readFileSync(resolve(__dirname, '../../../Fusion/marvel-lcg-src/data/cards.json'), 'utf8')) as Record<string, unknown>
const FICHES = new Map<string, Fiche>()
;(function parcourir(o: unknown): void {
  if (Array.isArray(o)) return o.forEach(parcourir)
  if (o && typeof o === 'object') {
    const fiche = o as Fiche
    if (typeof fiche.card_id === 'string' && !FICHES.has(fiche.card_id)) FICHES.set(fiche.card_id, fiche)
    Object.values(o).forEach(parcourir)
  }
})(CARDS)

const reel = (code: string): Fiche | undefined => {
  const f = FICHES.get(code)
  const lien = f?.full_link ?? f?.ability_link
  return lien ? FICHES.get(lien) : f
}
const net = (t: string | undefined) =>
  (t ?? '')
    .replace(/\\\//g, '/')
    .replace(/&#8594;/g, '→')
    .replace(/\r/g, '')
    .replace(/ /g, ' ')
    .replace(/\s+/g, ' ')
    .trim()

/** Errata qui ne touchent NI le texte NI les traits (titre, icône, classification) : pastille seule, sans voile. */
const PASTILLE_SEULE = ['01184', '16024', '48037', '49023', '50153', '56073']

describe('table des errata RRG', () => {
  it('porte les 87 cartes de l\'Annexe V (hors les 6 corrections du livret)', () => {
    expect(CODES_ERRATA.length).toBe(87)
    expect(new Set(CODES_ERRATA).size).toBe(87)
  })

  it('chaque carte existe dans cards.json', () => {
    const absentes = CODES_ERRATA.filter((c) => !FICHES.has(c))
    expect(absentes).toEqual([])
  })

  it('chaque errata a sa source, son résumé EN et FR, et ses deux textes ou aucun', () => {
    for (const code of CODES_ERRATA) {
      const e = erratumDeCarte(code)
      expect(e, code).toBeDefined()
      if (!e) continue
      expect(['1.7', '1.8'], code).toContain(e.source)
      expect(e.resumeEn.length, `${code} résumé EN`).toBeGreaterThan(5)
      expect(e.resumeFr.length, `${code} résumé FR`).toBeGreaterThan(5)
      expect(texteErratum(e, 'en') === undefined, `${code} EN/FR cohérents`).toBe(texteErratum(e, 'fr') === undefined)
    }
  })

  it('seuls les errata de titre, d\'icône et de classification n\'ont pas de texte posé', () => {
    const sans = CODES_ERRATA.filter((c) => {
      const e = erratumDeCarte(c)
      return e && texteErratum(e, 'en') === undefined
    })
    expect(sans.sort()).toEqual(PASTILLE_SEULE)
  })

  it('le texte anglais posé est celui de cards.json (le texte de la base est à jour)', () => {
    const ecarts: string[] = []
    for (const code of CODES_ERRATA) {
      const e = erratumDeCarte(code)
      const en = e && texteErratum(e, 'en')
      if (!en) continue
      const base = net(reel(code)?.text)
      if (net(en) !== base) ecarts.push(`${code}\n  errata : ${net(en)}\n  base   : ${base}`)
    }
    expect(ecarts).toEqual([])
  })

  it('le texte français posé est celui des textes français de base', () => {
    const ecarts: string[] = []
    for (const code of CODES_ERRATA) {
      const e = erratumDeCarte(code)
      const fr = e && texteErratum(e, 'fr')
      const base = TEXTES_FR_COMPLETS[code]
      if (!fr || !base) continue
      if (net(fr) !== net(base)) ecarts.push(code)
    }
    expect(ecarts).toEqual([])
  })

  it('Suit Up : « attachée à un allié » (errata de la 1.7)', () => {
    const e = erratumDeCarte('45017')!
    expect(texteErratum(e, 'en')).toContain('attached to an ally')
    expect(texteErratum(e, 'en')).not.toContain('that ally')
    expect(texteErratum(e, 'fr')).toContain('attachée à un allié')
    expect(e.source).toBe('1.7')
  })

  it('les cartes réimprimées partagent l\'errata de la carte réelle', () => {
    expect(erratumDeCarte('22020')).toBe(erratumDeCarte('17020'))
    expect(erratumDeCarte('04147')).toBe(erratumDeCarte('04057'))
  })

  it('une carte sans errata n\'a rien', () => {
    expect(erratumDeCarte('01001a')).toBeUndefined()
    expect(erratumDeCarte(undefined)).toBeUndefined()
    expect(erratumDeCarte('ca001a')).toBeUndefined()
  })
})

describe('pastille et surcouche', () => {
  it('la pastille dit « Errata », ce qui a changé et la version', () => {
    const html = renderToStaticMarkup(<PastilleErrata erratum={erratumDeCarte('45017')!} />)
    expect(html).toContain('Errata')
    expect(html).toContain('role="note"')
    expect(html).toMatch(/Rules Reference 1\.7/)
    expect(html).toMatch(/an ally|un allié/)
  })

  it('la note sous l\'aperçu écrit la même information sans souris', () => {
    const html = renderToStaticMarkup(<NoteErrata erratum={erratumDeCarte('45017')!} />)
    expect(html).toContain('Errata')
    expect(html).toMatch(/an ally|un allié/)
  })

  it('la carte agrandie d\'un errata porte la pastille ; une carte sans errata, rien', () => {
    const avec = renderToStaticMarkup(<TraductionSurCarte codeCarte="45017" imageUrl="/scan/45017" />)
    expect(avec).toContain('pastille-errata')
    const sans = renderToStaticMarkup(<TraductionSurCarte codeCarte="01001a" imageUrl="/scan/01001a" />)
    expect(sans).not.toContain('pastille-errata')
  })

  it('un errata sans texte (titre, icône) ne donne que la pastille', () => {
    const html = renderToStaticMarkup(<TraductionSurCarte codeCarte="01184" imageUrl="/scan/01184" />)
    expect(html).toContain('pastille-errata')
    expect(html).not.toContain('traduction-posee')
  })

  it('une carte face cachée n\'affiche pas l\'errata', () => {
    const html = renderToStaticMarkup(<TraductionSurCarte codeCarte="45017" imageUrl="/scan/45017" facedown />)
    expect(html).not.toContain('pastille-errata')
  })
})

describe('l\'errata ne s\'affiche qu\'à l\'agrandissement', () => {
  it('seuls l\'aperçu agrandi, la surcouche partagée et la pastille importent l\'errata', () => {
    const racine = resolve(__dirname, '..')
    const fichiers: string[] = []
    const lister = (dossier: string) => {
      for (const nom of readdirSync(dossier, { withFileTypes: true })) {
        const chemin = resolve(dossier, nom.name)
        if (nom.isDirectory()) lister(chemin)
        else if (/\.tsx?$/.test(nom.name) && !/\.test\./.test(nom.name)) fichiers.push(chemin)
      }
    }
    lister(racine)
    const importeurs = fichiers
      .filter((f) => /from '\.\/errata-rrg'|from '\.\/PastilleErrata'|PastilleErrata/.test(readFileSync(f, 'utf8')))
      .map((f) => f.replace(racine + '/', ''))
      .sort()
    expect(importeurs).toEqual(['board/Board.tsx', 'board/PastilleErrata.tsx', 'board/traduction-carte.tsx'])
  })
})

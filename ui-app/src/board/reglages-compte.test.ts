// Les reglages du plateau gardes sur le compte : la liste des cles est la meme
// que celle du serveur, et le rapprochement suit le contrat « le compte fait
// foi, le navigateur verse ce que le compte n'a pas ».
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, expect, it } from 'vitest'
import { StockageMemoire } from './cadre-joueur'
import { changementsDepuis, lireReglages, rapprocher, reglageValide, REGLAGES_DU_COMPTE } from './reglages-compte'

const ici = dirname(fileURLToPath(import.meta.url))
const serveur = readFileSync(
  join(ici, '../../../Fusion/marvel-lcg-src/src/engine/device/web/server/server_get.py'),
  'utf8',
)

describe('reglages du compte', () => {
  it('a exactement les cles que le serveur accepte', () => {
    const bloc = serveur.match(/REGLAGES_CLES = frozenset\(\(([\s\S]*?)\)\)/)?.[1] ?? ''
    const cles = [...bloc.matchAll(/'([^']+)'/g)].map((m) => m[1])
    expect(cles.length).toBeGreaterThan(40)
    expect([...REGLAGES_DU_COMPTE].sort()).toEqual(cles.sort())
    expect(new Set(REGLAGES_DU_COMPTE).size).toBe(REGLAGES_DU_COMPTE.length)
  })

  it('laisse hors du compte la langue, la vue admin et ce qui est deja synchronise', () => {
    for (const cle of ['marvel-langue', 'mc_vue_joueur', 'mc_affichage_v1', 'mc_teinte_v1', 'mc_table_v1', 'mc_hero_art_v1', 'mc_fond_image_v1']) {
      expect(REGLAGES_DU_COMPTE).not.toContain(cle)
    }
  })

  it('ne garde que des textes courts sans caractere de controle', () => {
    expect(reglageValide('gauche')).toBe(true)
    expect(reglageValide('{"he":"Mon héros"}')).toBe(true)
    expect(reglageValide('x'.repeat(2001))).toBe(false)
    expect(reglageValide('a\nb')).toBe(false)
    expect(reglageValide(null)).toBe(false)
    expect(reglageValide(3)).toBe(false)
  })

  it('lit les seules cles de la liste', () => {
    const stockage = new StockageMemoire()
    stockage.setItem('mc_ameliorations_cote', 'gauche')
    stockage.setItem('marvel-langue', 'en')
    stockage.setItem('mc_piles_inversees', 'x'.repeat(2001))
    expect(lireReglages(stockage)).toEqual({ mc_ameliorations_cote: 'gauche' })
  })

  it('le compte fait foi, le navigateur verse ce que le compte n a pas', () => {
    const { versNavigateur, versCompte } = rapprocher(
      { mc_ameliorations_cote: 'droite', 'marvel-board-sons': '0', affichage: 'sobre', mc_apercu_zoom: 3 },
      { mc_ameliorations_cote: 'gauche', 'marvel-board-sons': '0', 'marvel-board-musique': '1', mc_apercu_zoom: '2' },
    )
    // Valeur differente : le compte gagne. Valeur egale : rien a ecrire.
    expect(versNavigateur).toEqual({ mc_ameliorations_cote: 'droite' })
    // Absente du compte (ou invalide) : le reglage d'avant est recupere.
    expect(versCompte).toEqual({ 'marvel-board-musique': '1', mc_apercu_zoom: '2' })
  })

  it('premiere visite apres la mise a jour : tout le navigateur part vers le compte', () => {
    const navigateur = { 'marvel-board-sons': '0', mc_noms_zones_v1: '{"he":"Moi"}' }
    expect(rapprocher({}, navigateur)).toEqual({ versNavigateur: {}, versCompte: navigateur })
  })

  it('ne renvoie que ce qui a change, null pour un reglage efface', () => {
    expect(
      changementsDepuis(
        { 'marvel-board-sons': '0', 'marvel-board-musique': '1', mc_apercu_zoom: '2' },
        { 'marvel-board-sons': '1', mc_apercu_zoom: '2', mc_phase_bis: '1' },
      ),
    ).toEqual({ 'marvel-board-sons': '1', 'marvel-board-musique': null, mc_phase_bis: '1' })
  })
})

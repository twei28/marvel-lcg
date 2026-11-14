import { describe, expect, it } from 'vitest'
import { avecBandes } from './TraductionPosee'

describe('avecBandes', () => {
  const html = '<div class="tp-par">Entrave 1.</div><div class="tp-par">Interruption forcée : un long paragraphe de capacité.</div><div class="tp-par tp-citation">« Citation »</div>'
  it("pose le bloc de l'icône à la frontière de paragraphes la plus proche de la part d'anglais au-dessus d'elle", () => {
    const sortie = avecBandes(html, [{ avant: 0.8 }])
    expect(sortie.indexOf('tp-bande')).toBeGreaterThan(sortie.indexOf('long paragraphe'))
    expect(sortie.indexOf('tp-bande')).toBeLessThan(sortie.indexOf('Citation'))
  })
  it('sans icône, rien ne change', () => {
    expect(avecBandes(html, [])).toBe(html)
  })
})

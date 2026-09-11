// La chaine de causalite doit tenir dans LES DEUX langues.
//
// Le moteur traduit sa narration quand data/translate_fr.json est charge
// (TransText). Les motifs n'existaient qu'en anglais, et l'en-tete du module
// l'assumait : « si elle venait a etre traduite, les motifs cesseraient de
// matcher ». C'est arrive le 11/09/2026, en reparant les cles de traduction :
// « Spider-Man est attaque par Klaw » ne donnait plus aucun auteur.

import { describe, expect, it } from 'vitest'
import { creerMemoireCauses, lireCause, noterCause } from './causalite'

const noter = (texte: string) => {
  const memoire = creerMemoireCauses()
  noterCause(memoire, texte, 10)
  return memoire
}

describe('causalite, narration anglaise', () => {
  it('lit « is being attacked by »', () => {
    expect(lireCause(noter('Spider-Man is being attacked by Klaw'), 'degats', 'Spider-Man', 10))
      .toMatchObject({ source: 'Klaw' })
  })

  it('lit « would deal ... damage to » avec sa carte responsable', () => {
    expect(lireCause(noter('Quasar would deal 2 damage to Evil Gwenpool (Quasar)'), 'degats', 'Evil Gwenpool', 10))
      .toMatchObject({ source: 'Quasar', via: 'Quasar' })
  })

  it('lit « would place ⚠ »', () => {
    expect(lireCause(noter('Underground Distribution would place 2⚠ (Place Threat)'), 'menace', 'Underground Distribution', 10))
      .toMatchObject({ via: 'Place Threat' })
  })
})

describe('causalite, narration francaise', () => {
  it('lit « est attaqué par »', () => {
    expect(lireCause(noter('Spider-Man est attaqué par Klaw'), 'degats', 'Spider-Man', 10))
      .toMatchObject({ source: 'Klaw' })
  })

  it('lit « s’apprête à infliger », apostrophe courbe ou droite', () => {
    expect(lireCause(noter('Quasar s’apprête à infliger 2 dégât(s) à Evil Gwenpool'), 'degats', 'Evil Gwenpool', 10))
      .toMatchObject({ source: 'Quasar' })
    expect(lireCause(noter("Quasar s'apprête à infliger 2 dégât(s) à Evil Gwenpool"), 'degats', 'Evil Gwenpool', 10))
      .toMatchObject({ source: 'Quasar' })
  })

  it('lit « va subir ... de » et garde la carte responsable', () => {
    expect(lireCause(noter('Evil Gwenpool va subir 2 dégât(s) de Quasar (Quasar)'), 'degats', 'Evil Gwenpool', 10))
      .toMatchObject({ source: 'Quasar', via: 'Quasar' })
  })

  it('lit « s’apprête à recevoir ⚠ »', () => {
    expect(lireCause(noter('Trafic Clandestin s’apprête à recevoir 2⚠ (Phase Menace)'), 'menace', 'Trafic Clandestin', 10))
      .toMatchObject({ via: 'Phase Menace' })
  })

  it('lit « va contrer »', () => {
    expect(lireCause(noter('Spider-Man va contrer Trafic Clandestin (+1)'), 'menace', 'Trafic Clandestin', 10))
      .toMatchObject({ source: 'Spider-Man' })
  })

  it('ignore « va contrer » sans complement, comme son motif anglais', () => {
    // « {unit} will thwart » (sans manigance) existe aussi cote moteur et est
    // traduit depuis le 11/09/2026. Les deux motifs exigent un nom apres le
    // verbe : sans lui, aucune cause n'est notee, donc aucun faux auteur.
    expect(lireCause(noter('Spider-Man va contrer'), 'menace', 'Spider-Man', 10)).toBeUndefined()
    expect(lireCause(noter('Spider-Man will thwart'), 'menace', 'Spider-Man', 10)).toBeUndefined()
  })

  it('ne confond pas « dégât(s) » avec la carte responsable entre parentheses', () => {
    const cause = lireCause(noter('Evil Gwenpool va subir 2 dégât(s) de Quasar'), 'degats', 'Evil Gwenpool', 10)
    expect(cause).toMatchObject({ source: 'Quasar' })
    expect(cause?.via).toBeUndefined()
  })
})

// Les trois questions que le moteur pose a la mise en place de MojoMania (cards/pack/mojo/campaign.py) arrivent en anglais ;
// le plateau les rend en francais officiel. Le nom de la carte reste celui du scan.
import { describe, expect, it } from 'vitest'
import { traduireMoteur } from './vocabulaire-moteur'

describe('traduireMoteur : campagne MojoMania', () => {
  it('traduit les deux options de Longshot', () => {
    expect(traduireMoteur('Reveal Longshot')).toBe('Révéler Longshot')
    expect(traduireMoteur('Shuffle Longshot into the encounter deck')).toBe('Mélanger Longshot dans le deck de rencontre')
  })

  it('traduit la remise en jeu de la carte gardee, en gardant son nom', () => {
    expect(traduireMoteur('Put Stark Tower into play under your control')).toBe('Mettre Stark Tower en jeu sous ton contrôle')
  })
})

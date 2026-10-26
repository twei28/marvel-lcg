import { act, fireEvent, render, renderHook, screen } from '@testing-library/react'
import { beforeEach, describe, expect, it } from 'vitest'
import {
  CLES_TELEPHONE,
  DEFAUTS_TELEPHONE,
  ecrireColonnesZone,
  ecrireReglageTelephone,
  plateauDejaChoisi,
  lireReglagesTelephone,
  useReglagesTelephone,
} from './reglages-telephone'
import { ContenuOnglet, type ProprietesReglages } from '../FenetreReglages'
import { PlateauMobile } from './PlateauMobile'
import type { BoardProps } from '../Board'

beforeEach(() => {
  window.localStorage.clear()
  document.documentElement.removeAttribute('data-taille-texte')
})

describe('les reglages du telephone (zone 3)', () => {
  it('ont des defauts sages : texte normal, vibrations oui, verrou non', () => {
    expect(lireReglagesTelephone()).toEqual(DEFAUTS_TELEPHONE)
  })

  it('se relisent apres ecriture, et une valeur inconnue retombe au defaut', () => {
    ecrireReglageTelephone('tailleTexte', 'tres-grand')
    ecrireReglageTelephone('vibrations', false)
    ecrireReglageTelephone('verrouPortrait', true)
    expect(lireReglagesTelephone()).toEqual({ plateau: 'cartes', plateauMemorise: false, aideDebut: true, visitePiles: true, colonnesZones: { manigances: 3, allies: 3, sbires: 3, enJeu: 4 }, tailleTexte: 'tres-grand', vibrations: false, verrouPortrait: true })
    window.localStorage.setItem(CLES_TELEPHONE.tailleTexte, 'enorme')
    expect(lireReglagesTelephone().tailleTexte).toBe('normal')
  })

  it('le plateau (cartes ou ronds) se relit, et une valeur inconnue retombe sur les cartes', () => {
    ecrireReglageTelephone('plateau', 'ronds')
    expect(lireReglagesTelephone().plateau).toBe('ronds')
    window.localStorage.setItem(CLES_TELEPHONE.plateau, 'triangles')
    expect(lireReglagesTelephone().plateau).toBe('cartes')
    expect(plateauDejaChoisi()).toBe(false)
    ecrireReglageTelephone('plateau', 'cartes')
    expect(plateauDejaChoisi()).toBe(true)
  })

  it('les colonnes des zones (26/10/2026) : Manigances 3, Allies 3, Sbires 3, Cartes en jeu 4 par defaut, et se relisent apres ecriture', () => {
    expect(lireReglagesTelephone().colonnesZones).toEqual({ manigances: 3, allies: 3, sbires: 3, enJeu: 4 })
    ecrireColonnesZone('allies', 2)
    ecrireColonnesZone('enJeu', 0)
    expect(lireReglagesTelephone().colonnesZones).toEqual({ manigances: 3, allies: 2, sbires: 3, enJeu: 0 })
  })

  it('une valeur de colonnes inconnue (5, texte, vide) retombe au defaut de la zone', () => {
    window.localStorage.setItem(CLES_TELEPHONE.colonnesZones, 'x,9,-1,')
    expect(lireReglagesTelephone().colonnesZones).toEqual({ manigances: 3, allies: 3, sbires: 3, enJeu: 4 })
    window.localStorage.setItem(CLES_TELEPHONE.colonnesZones, '1,2')
    expect(lireReglagesTelephone().colonnesZones).toEqual({ manigances: 1, allies: 2, sbires: 3, enJeu: 4 })
  })

  it('le crochet suit un changement fait ailleurs, sans rechargement', () => {
    const { result } = renderHook(() => useReglagesTelephone())
    act(() => ecrireReglageTelephone('tailleTexte', 'grand'))
    expect(result.current.tailleTexte).toBe('grand')
  })
})

const props = {} as unknown as ProprietesReglages

describe('les colonnes des zones dans la fenetre des reglages', () => {
  it('sur telephone : un choix 1 / 2 / 3 / 4 / Auto par zone (Manigances, Alliés, Sbires, Cartes en jeu), qui s\'enregistre', () => {
    render(<ContenuOnglet onglet="apparence" p={{ ...props, affichage: 'normal', telephone: true }} />)
    for (const zone of ['Manigances', 'Alliés', 'Sbires', 'Cartes en jeu']) {
      const groupe = screen.getByRole('group', { name: `Colonnes : ${zone}` })
      expect(Array.from(groupe.querySelectorAll('button')).map((b) => b.textContent)).toEqual(['1', '2', '3', '4', 'Auto'])
    }
    fireEvent.click(screen.getByRole('group', { name: 'Colonnes : Sbires' }).querySelectorAll('button')[1]!)
    fireEvent.click(screen.getByRole('group', { name: 'Colonnes : Cartes en jeu' }).querySelectorAll('button')[4]!)
    expect(lireReglagesTelephone().colonnesZones).toEqual({ manigances: 3, allies: 3, sbires: 2, enJeu: 0 })
  })

  it('pas sur ordinateur : le choix des colonnes ne concerne que le plateau du telephone', () => {
    render(<ContenuOnglet onglet="apparence" p={{ ...props, affichage: 'normal', telephone: false }} />)
    expect(screen.queryByRole('group', { name: 'Colonnes : Sbires' })).toBeNull()
  })
})

describe('dans la fenetre des reglages', () => {
  it('sur telephone : taille du texte (3 niveaux) et verrou portrait en Apparence, vibrations en Son', () => {
    const { unmount } = render(<ContenuOnglet onglet="apparence" p={{ ...props, affichage: 'normal', telephone: true }} />)
    const groupe = screen.getByRole('group', { name: 'Taille du texte' })
    expect(groupe.querySelectorAll('button')).toHaveLength(3)
    fireEvent.click(screen.getByRole('button', { name: 'Très grande' }))
    expect(lireReglagesTelephone().tailleTexte).toBe('tres-grand')
    fireEvent.click(screen.getByRole('switch', { name: /Verrou portrait/ }))
    expect(lireReglagesTelephone().verrouPortrait).toBe(true)
    unmount()
    render(<ContenuOnglet onglet="son" p={{ ...props, sons: true, telephone: true }} />)
    fireEvent.click(screen.getByRole('switch', { name: /Vibrations/ }))
    expect(lireReglagesTelephone().vibrations).toBe(false)
  })

  it('sur PC : aucune de ces lignes', () => {
    render(<ContenuOnglet onglet="apparence" p={{ ...props, affichage: 'normal' }} />)
    expect(screen.queryByRole('group', { name: 'Taille du texte' })).toBeNull()
    expect(screen.queryByRole('switch', { name: /Verrou portrait/ })).toBeNull()
  })
})

describe('la taille du texte sur le plateau', () => {
  const plateau = {
    world: { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] },
    playerId: 0,
    plateau: { emplacements: [], nombreDeCartes: 0, idsAffiches: new Set(), representantsDePile: new Map(), nombreIgnore: 0 },
  } as unknown as BoardProps

  it('se pose sur <html>, suit le reglage, et part avec le plateau', () => {
    ecrireReglageTelephone('tailleTexte', 'grand')
    const { unmount } = render(<PlateauMobile {...plateau} />)
    expect(document.documentElement).toHaveAttribute('data-taille-texte', 'grand')
    act(() => ecrireReglageTelephone('tailleTexte', 'normal'))
    expect(document.documentElement).not.toHaveAttribute('data-taille-texte')
    act(() => ecrireReglageTelephone('tailleTexte', 'tres-grand'))
    unmount()
    expect(document.documentElement).not.toHaveAttribute('data-taille-texte')
  })
})

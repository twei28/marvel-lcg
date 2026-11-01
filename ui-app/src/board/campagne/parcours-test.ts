// Pour les tests du panneau de récompenses : avancer dans le parcours de fin de scénario
// (Victoire → Bilan → Carnet → Suite) en cliquant « Continuer ».
import { fireEvent, screen, waitFor } from '@testing-library/react'
import { expect } from 'vitest'

const pageCourante = () => document.querySelector('.parcours-fin')?.getAttribute('data-page')

export async function continuerVers(page: 'bilan' | 'carnet' | 'suite') {
  fireEvent.click(await screen.findByRole('button', { name: 'Continuer' }))
  await waitFor(() => expect(pageCourante()).toBe(page))
}

export async function auBilan() {
  await continuerVers('bilan')
}

export async function auCarnet() {
  await auBilan()
  await continuerVers('carnet')
}

export async function alaSuite() {
  await auCarnet()
  await continuerVers('suite')
}

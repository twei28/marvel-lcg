// LA TABLE PERSONNALISABLE, l'enregistrement (decision du 04/10/2026) : une
// disposition par nombre de joueurs (solo, 2, 3, 4), dans le navigateur et sur
// le compte, qui fait foi quand il existe (meme contrat que la teinte et
// l'affichage). Cles du compte `table-1` a `table-4`, bornees cote serveur
// (`_table_valide`, server_get.py) ; le texte est celui de `ecrireTable`.

import { useEffect, useState } from 'react'
import { DISPOSITION_ORIGINE, cleTable, ecrireTable, lireTable, type Disposition } from './disposition'

export const CLE_TABLE = 'mc_table_v1'
/** Evenement de la page : une disposition vient de changer. */
export const EVENEMENT_TABLE = 'mc-table-change'

function lireTout(): Record<string, string> {
  try {
    const brut = JSON.parse(window.localStorage.getItem(CLE_TABLE) ?? '{}')
    return brut && typeof brut === 'object' && !Array.isArray(brut) ? (brut as Record<string, string>) : {}
  } catch {
    return {}
  }
}

function ecrireTout(tables: Record<string, string>): void {
  try {
    window.localStorage.setItem(CLE_TABLE, JSON.stringify(tables))
  } catch {
    /* stockage indisponible : le choix ne survivra pas au rechargement */
  }
  window.dispatchEvent(new Event(EVENEMENT_TABLE))
}

/** La disposition de ce nombre de joueurs ; l'origine sans choix, ou si le choix ne tient pas. */
export function dispositionPour(nombreDeJoueurs: number): Disposition {
  return lireTable(lireTout()[cleTable(nombreDeJoueurs)]) ?? DISPOSITION_ORIGINE
}

/** Range le choix (`undefined` = disposition d'origine), et le dit au compte. */
export function enregistrerDisposition(nombreDeJoueurs: number, d: Disposition | undefined, versLeCompte = true): void {
  const cle = cleTable(nombreDeJoueurs)
  const tables = lireTout()
  if (d) tables[cle] = ecrireTable(d)
  else delete tables[cle]
  ecrireTout(tables)
  if (!versLeCompte) return
  try {
    void fetch('/save_preferences', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ changements: { [cle]: d ? ecrireTable(d) : null } }),
    }).catch(() => {})
  } catch {
    /* hors ligne : le navigateur garde le choix */
  }
}

/** Les tables VALIDES du compte, ou `undefined` quand le navigateur reste la reference. */
export function tablesDuCompte(reponse: {
  compte?: boolean
  existe?: boolean
  preferences?: Record<string, unknown>
} | null | undefined): Record<string, string> | undefined {
  if (!reponse || !reponse.compte || !reponse.existe) return undefined
  const tables: Record<string, string> = {}
  for (const [cle, valeur] of Object.entries(reponse.preferences ?? {})) {
    if (/^table-[1-4]$/.test(cle) && typeof valeur === 'string' && lireTable(valeur)) tables[cle] = valeur
  }
  return tables
}

/** Le compte fait foi : le navigateur prend exactement ses tables. */
export function synchroniserTables(tables: Record<string, string>): void {
  ecrireTout({ ...tables })
}

/** Interroge le compte au chargement du plateau. */
export async function chercherTablesDuCompte(): Promise<Record<string, string> | undefined> {
  try {
    const reponse = await fetch('/get_preferences', { cache: 'no-store' })
    if (!reponse.ok) return undefined
    return tablesDuCompte(await reponse.json())
  } catch {
    return undefined
  }
}

/**
 * La disposition de la table pour ce nombre de joueurs, tenue a jour : un
 * choix fait ailleurs (un autre onglet, l'editeur) et le compte au chargement.
 */
export function useDispositionTable(nombreDeJoueurs: number): Disposition {
  const [, redessiner] = useState(0)
  useEffect(() => {
    const suivre = () => redessiner((n) => n + 1)
    window.addEventListener(EVENEMENT_TABLE, suivre)
    window.addEventListener('storage', suivre)
    return () => {
      window.removeEventListener(EVENEMENT_TABLE, suivre)
      window.removeEventListener('storage', suivre)
    }
  }, [])
  useEffect(() => {
    let vivant = true
    void chercherTablesDuCompte().then((tables) => {
      if (vivant && tables !== undefined) synchroniserTables(tables)
    })
    return () => {
      vivant = false
    }
  }, [])
  return dispositionPour(nombreDeJoueurs)
}

// L'assemblee de Kingsfall multi-tables, TENUE A JOUR. Le rendu du monde ne se refait que quand CETTE table joue : un autre groupe qui rejoint, verse des
// jetons ou finit sa partie n'y changerait rien avant le prochain coup. Tant que la partie appartient a une assemblee, on relit donc l'etat commun
// (`/get_assemblee`) toutes les quelques secondes, et on le prefere au dernier rendu.
import { useEffect, useState } from 'react'
import { assembleeDuMonde } from './assemblee-etat'
import { chargerAssemblee } from './sources'
import type { AssembleeExport, World } from './world'

export const PERIODE_ASSEMBLEE_MS = 4000

export function useAssembleeEnDirect(monde: World | undefined, playerId: number): AssembleeExport | undefined {
  const duMonde = assembleeDuMonde(monde)
  const code = duMonde?.code
  const [direct, setDirect] = useState<AssembleeExport | undefined>(undefined)
  useEffect(() => {
    if (!code) {
      setDirect(undefined)
      return
    }
    let vivant = true
    const lire = () => {
      chargerAssemblee(playerId)
        .then((etat) => {
          const lu = assembleeDuMonde({ assemblee: etat } as unknown as World)
          if (vivant && lu && lu.code === code) setDirect(lu)
        })
        .catch(() => {
          /* le serveur ne repond pas un instant : on garde le dernier etat connu */
        })
    }
    lire()
    const minuteur = window.setInterval(lire, PERIODE_ASSEMBLEE_MS)
    return () => {
      vivant = false
      window.clearInterval(minuteur)
    }
  }, [code, playerId])
  return direct && direct.code === code ? direct : duMonde
}

// Le calcul d'effacer-texte.ts (≈ 0,2 s par carte sur un ordinateur, davantage sur un téléphone) tourne ici, hors du
// fil de l'interface : un plateau qui affiche plusieurs cartes traduites ne se fige plus pendant qu'on nettoie les scans.
import { effacerTexte, type OptionsEffacement } from './effacer-texte'

type Demande = { id: number; donnees: Uint8ClampedArray; largeur: number; hauteur: number; options: OptionsEffacement }

self.onmessage = (evenement: MessageEvent<Demande>) => {
  const { id, donnees, largeur, hauteur, options } = evenement.data
  let cadre = null
  try {
    cadre = effacerTexte(donnees, largeur, hauteur, options)
  } catch {
    cadre = null
  }
  ;(self as unknown as Worker).postMessage({ id, donnees, cadre }, [donnees.buffer])
}

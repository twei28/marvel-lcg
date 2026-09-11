// Le plateau en PORTRAIT : une colonne, un seul ecran, aucun defilement.
//
// Spec : docs/superpowers/specs/2026-09-11-plateau-portrait-telephone-design.md
//
// Releve mesure sur play.marvelsimulator.com : leur page ne defile pas
// (scrollHeight == innerHeight), et cela ne tient que parce que la table n'est
// PAS faite de cartes jouables. Le vilain, le complot et les allies sont la
// vraie carte en petit, avec leurs chiffres en gros A COTE. Seule la main est
// en cartes qu'on lit a vue.
//
// Il accepte exactement les BoardProps du plateau PC, comme PlateauPaysage :
// c'est ce qui permet a board.tsx de choisir sans rien adapter.
import type { BoardProps } from '../Board'
import './portrait.css'

export function PlateauPortrait(_props: BoardProps) {
  return <main className="plateau-portrait" />
}

// Vitrine du composant carte : six cartes representatives, dans une table
// factice, pour juger l'apparence sans lancer de partie.
//
// Elle ne contient plus de composant : ScanCard est le composant du plateau, la
// vitrine n'en est qu'un client. Les scans sont importes en dur ICI, et
// seulement ici : le vrai plateau construit ses URL depuis l'id de carte.
import { createRoot, type Root } from 'react-dom/client'
import { ScanCard, type ScanCardProps } from './components/ScanCard'
import '../styles/tokens.css'
import './vitrine.css'
import grootScan from '../../Fusion/marvel-lcg-src/assets/pics/16001a.jpg'
import ronanScan from '../../Fusion/marvel-lcg-src/assets/pics/90001.jpg'
import ronanSchemeScan from '../../Fusion/marvel-lcg-src/assets/pics/90002.jpg'
import accusedScan from '../../Fusion/marvel-lcg-src/assets/pics/90003.jpg'
import hammerScan from '../../Fusion/marvel-lcg-src/assets/pics/90004.jpg'
import daredevilScan from '../../Fusion/marvel-lcg-src/assets/pics/60039.jpg'

const cards: ScanCardProps[] = [
  {
    id: 'groot',
    name: 'Groot',
    kind: 'hero',
    state: 'selected',
    imageUrl: grootScan,
    allyHp: '7/14',
    // Bande a mi-hauteur : alerte douce, la carte respire lentement.
    jauge: { remplissage: 0.5, genre: 'pv', alarme: true },
  },
  {
    id: 'daredevil',
    name: 'Daredevil',
    kind: 'ally',
    state: 'exhausted',
    imageUrl: daredevilScan,
    allyHp: '1/3',
    // Un tiers de PV : alerte forte, bande rouge.
    jauge: { remplissage: 0.3333, genre: 'pv', alarme: true },
  },
  {
    id: 'ronan',
    name: 'Ronan the Accuser',
    kind: 'minion',
    state: 'targetable',
    imageUrl: ronanScan,
    allyHp: '4/6',
    // Un ennemi n'a pas droit a l'alarme : bande coloree, mais aucune pulsation.
    jauge: { remplissage: 0.6667, genre: 'pv', alarme: false },
  },
  {
    id: 'judge-jury-executioner',
    name: 'Judge, Jury, Executioner',
    kind: 'side-scheme',
    state: 'ready',
    imageUrl: ronanSchemeScan,
    isLandscape: true,
    schemeThreat: '3',
    // Complot du mechant a menace haute : bande presque pleine et alerte forte.
    jauge: { remplissage: 0.9, genre: 'menace', alarme: true },
  },
  {
    id: 'the-accused',
    name: 'The Accused',
    kind: 'attachment',
    state: 'playable',
    imageUrl: accusedScan,
  },
  {
    id: 'bring-the-hammer-down',
    name: 'Bring the Hammer Down',
    kind: 'treachery',
    state: 'disabled',
    imageUrl: hammerScan,
  },
]

function Vitrine() {
  return (
    <main className="showcase">
      <section className="tabletop" aria-label="Enhanced scan prototype">
        <header className="hud">
          <div>
            <span className="eyebrow">Board prototype</span>
            <h1>Enhanced scan</h1>
          </div>
          <div className="turn-summary">
            <span>Player Phase</span>
            <strong>Groot must choose a target</strong>
          </div>
        </header>

        <div className="board-surface">
          <div className="board-row encounter-row">
            {cards.slice(2, 4).map((card) => (
              <ScanCard {...card} key={card.id} />
            ))}
          </div>
          <div className="board-row player-row">
            {cards.slice(0, 2).map((card) => (
              <ScanCard {...card} key={card.id} />
            ))}
          </div>
          <div className="hand-row">
            {cards.slice(4).map((card) => (
              <ScanCard {...card} key={card.id} />
            ))}
          </div>
        </div>

        <footer className="ask-bar">
          <div>
            <span className="eyebrow">Expected action</span>
            <strong>Choose a target for the attack</strong>
          </div>
          <div className="ask-actions">
            <button type="button">Cancel</button>
            <button type="button" className="primary">
              Confirm
            </button>
          </div>
        </footer>
      </section>
    </main>
  )
}

// Meme garde que board.tsx : depuis que la vitrine partage ScanCard avec le
// plateau, retoucher le composant declenche une mise a jour a chaud qui peut
// reexecuter ce module sans recharger la page. Un second createRoot sur le meme
// noeud vide la page au lieu de montrer la retouche.
declare global {
  interface Window {
    racineVitrine?: Root
  }
}

const cible = document.getElementById('vitrine')
if (!cible) throw new Error('Element #vitrine not found in vitrine.html')
window.racineVitrine ??= createRoot(cible)
window.racineVitrine.render(<Vitrine />)

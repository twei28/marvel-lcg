// Hepzibah (Starjammers, `hz001a`-`hz015`) : ce que le plateau DESSINE une fois les cartes résolues.
//
// `Fusion/marvel-lcg-src/tools/cas/hepzibah.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le joueur REGARDE
// (PROCESSUS-CARTE.md, étape 8 bis). Les cartes du pack qui changent ce qu'on VOIT :
//   - hz005 Energy Blaster (3 compteurs « charge ») et hz006 Heavy Machine Gun (2 compteurs « ammo ») : améliorations posées
//     sur Hepzibah, dont les compteurs doivent se lire à l'écran ;
//   - hz010 Armed to the Teeth : son Special pose un compteur polyvalent (« all-purpose ») sur une arme ;
//   - hz015 Shi'ar Infantry : deux copies en jeu (révélée + l'autre mise en jeu par son « When Revealed ») ;
//   - hz013 Kill Order : manigance annexe, menace posée.
// Aucun correctif de plateau : le rendu générique suffisait (modèle `alien-vs-predator-plateau.test.ts`, compteurs `info.c_*`).
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const BLASTER = 2
const MITRAILLEUSE = 3
const COMBINAISON = 4
const SBIRE_A = 80
const SBIRE_B = 81
const KILL_ORDER = 82

const heros = () => carte(IDENTITE, 'hz001a', 'Hero', 'Hepzibah')
const valeurs = (id: number, monde: ReturnType<typeof tableAvec>) => Object.values(dessinee(monde, id)?.compteurs ?? {})

describe('hz005 / hz006 : les armes à compteurs posées sur Hepzibah', () => {
  const monde = (blasterInfo: Record<string, number>) =>
    tableAvec(
      siege({
        area_hero: [
          heros(),
          carte(COMBINAISON, 'hz004', 'Upgrade', "Hepzibah's Spacesuit", { bind_object_id: IDENTITE }),
          carte(BLASTER, 'hz005', 'Upgrade', 'Energy Blaster', { bind_object_id: IDENTITE, info: blasterInfo }),
          carte(MITRAILLEUSE, 'hz006', 'Upgrade', 'Heavy Machine Gun', { bind_object_id: IDENTITE, info: { c_ammo: 1 } }),
        ],
      })
    )

  it('Energy Blaster est dessinée derrière Hepzibah, avec ses 2 compteurs de charge restants', () => {
    const m = monde({ c_charge: 2 })
    expect(dessinee(m, BLASTER)).toBeDefined()
    expect(dessinee(m, BLASTER)?.portePar).toBe(IDENTITE)
    expect(valeurs(BLASTER, m)).toContain(2)
  })

  it("Heavy Machine Gun montre son dernier compteur de munitions, et la combinaison est dessinée aussi", () => {
    const m = monde({ c_charge: 2 })
    expect(dessinee(m, MITRAILLEUSE)?.portePar).toBe(IDENTITE)
    expect(valeurs(MITRAILLEUSE, m)).toContain(1)
    expect(dessinee(m, COMBINAISON)).toBeDefined()
  })

  it('le compteur polyvalent posé par le Special d’Armed to the Teeth s’ajoute aux compteurs de charge', () => {
    const m = monde({ c_charge: 2, 'c_all-purpose': 1 })
    const compteurs = valeurs(BLASTER, m)
    expect(compteurs).toContain(2)
    expect(compteurs).toContain(1)
    expect(compteurs.length).toBe(2)
  })
})

describe('hz015 Shi’ar Infantry et hz013 Kill Order', () => {
  const monde = () =>
    tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(SBIRE_A, 'hz015', 'Minion', "Shi'ar Infantry"),
        carte(SBIRE_B, 'hz015', 'Minion', "Shi'ar Infantry"),
      ],
      area_schemes_side: [carte(KILL_ORDER, 'hz013', 'SideScheme', 'Kill Order')],
    })

  it('les deux copies de Shi’ar Infantry (révélée + mise en jeu) sont dessinées', () => {
    expect(dessinee(monde(), SBIRE_A)).toBeDefined()
    expect(dessinee(monde(), SBIRE_B)).toBeDefined()
  })

  it('Kill Order est dessinée dans la zone des manigances annexes', () => {
    expect(dessinee(monde(), KILL_ORDER)).toBeDefined()
  })
})

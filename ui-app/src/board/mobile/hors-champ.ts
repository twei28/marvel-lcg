// Combien de cartes d'une rangee sont hors du champ visible ?
//
// Une rangee qui deborde defile, et un voile au bord droit porte ce compte :
// c'est le seul signal qui dit qu'il y a une suite. Le calcul est ici, pur,
// pour etre teste ; la lecture du DOM est une enveloppe de trois lignes.
//
// Une carte compte comme hors champ quand PLUS DE LA MOITIE de sa largeur est
// cachee, a droite comme a gauche : une carte coupee d'un bord reste lisible
// et se voit, inutile de l'annoncer.

export type Boite1D = { gauche: number; largeur: number }

export function nombreHorsChamp(boites: Boite1D[], defilement: number, largeurVisible: number): number {
  const bordDroit = defilement + largeurVisible
  let compte = 0
  for (const { gauche, largeur } of boites) {
    const moitie = largeur / 2
    const cacheADroite = gauche + largeur - bordDroit
    const cacheAGauche = defilement - gauche
    if (cacheADroite > moitie || cacheAGauche > moitie) compte += 1
  }
  return compte
}

export function mesurerHorsChamp(conteneur: HTMLElement, selecteur = '.carte-posee'): number {
  const boites: Boite1D[] = []
  for (const enfant of conteneur.querySelectorAll<HTMLElement>(selecteur)) {
    boites.push({ gauche: enfant.offsetLeft, largeur: enfant.offsetWidth })
  }
  return nombreHorsChamp(boites, conteneur.scrollLeft, conteneur.clientWidth)
}

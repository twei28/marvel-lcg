// Les phrases du deroule : ecrites par nous, pas la narration du moteur.
//
// « Ultron frappe Shuri » se lit ; « [(50,01113) Klaw] would deal 2 damage »
// se dechiffre. Et tout passe par le dictionnaire : le plateau est bilingue,
// rattraper les traductions apres coup coute plus cher que de les poser tout
// de suite.
import { describe, expect, it } from 'vitest'
import {
  compteurEtape,
  compteurLigneBilan,
  regleEtape,
  resultatEtape,
  texteBilanVide,
  texteDefaite,
  texteLigneBilan,
  titreEtape,
} from './deroule-textes'
import type { EtapeDeroule, LigneBilan } from './deroule-phase'

const etape = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule => ({
  cle: 'k',
  temps: 'sbires',
  titre: 'attaque',
  regle: 'regle:activations',
  carteId: 50,
  cibleId: 12,
  auteurNom: 'Ultron',
  cibleNom: 'Shuri',
  boosts: [],
  consequences: [],
  ...extra,
})

const menace = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule =>
  etape({
    temps: 'menace',
    titre: 'menace',
    regle: 'regle:menace',
    carteId: undefined,
    cibleId: undefined,
    auteurNom: undefined,
    cibleNom: undefined,
    ...extra,
  })

describe('phrases du deroule', () => {
  it('nomme l attaquant et sa cible', () => {
    expect(titreEtape(etape())).toBe('Ultron attaque Shuri')
  })

  it('dit la manigance autrement que l attaque', () => {
    expect(titreEtape(etape({ titre: 'manigance' }))).toBe('Ultron complote contre Shuri')
  })

  it('nomme la manigance et son gain de menace', () => {
    // Le titre generique « Menace sur la manigance principale » disait moins
    // que la ligne qui le suivait : une seule phrase concrete le remplace.
    expect(
      titreEtape(menace({ cibleNom: 'L’Effraction !', montant: 2 }))
    ).toBe('L’Effraction ! gagne 2 menaces')
  })

  it('accorde la menace au singulier', () => {
    expect(titreEtape(menace({ cibleNom: 'L’Effraction !', montant: 1 })))
      .toBe('L’Effraction ! gagne 1 menace')
  })

  it('se replie sur le titre generique quand l entree ne dit ni nom ni montant', () => {
    // Une phrase vague vaut mieux qu'une phrase fausse : « gagne undefined
    // menaces » serait pire que l'ancien titre.
    expect(titreEtape(menace())).toBe('Menace sur la manigance principale')
    expect(titreEtape(menace({ cibleNom: 'L’Effraction !' })))
      .toBe('Menace sur la manigance principale')
  })

  it('rappelle la regle du point 1', () => {
    expect(regleEtape(etape({ regle: 'regle:menace' })))
      .toBe('Point 1 : chaque joueur ajoute 1 menace à la manigance principale.')
  })

  it('rappelle la regle des activations', () => {
    expect(regleEtape(etape())).toBe('Point 2 : chaque ennemi s\'active contre le héros engagé avec lui.')
  })

  it('laisse passer un titre deja redige', () => {
    // Une carte revelee arrive avec son titre venu du journal : on ne le
    // reecrit pas.
    expect(titreEtape(etape({ temps: 'revelation', titre: 'Icy Grip révélée' })))
      .toBe('Icy Grip révélée')
  })

  it('rappelle la regle des cartes revelees', () => {
    expect(regleEtape(etape({ regle: 'regle:revelation' })))
      .toBe('Point 4 : chaque joueur révèle sa carte rencontre et en applique l\'effet.')
  })

  it('ne dit rien d une regle inconnue plutot que d inventer', () => {
    expect(regleEtape(etape({ regle: 'regle:inexistante' }))).toBe('')
  })

  it('dit les degats reellement subis, sous le titre', () => {
    expect(titreEtape(etape({ auteurNom: 'Klaw', cibleNom: 'Colossus', montant: 4 })))
      .toBe('Klaw attaque Colossus')
    expect(resultatEtape(etape({ montant: 4 }))).toBe('→ 4 dégâts')
  })

  it('accorde le degat au singulier', () => {
    expect(resultatEtape(etape({ montant: 1 }))).toBe('→ 1 dégât')
  })

  it('compte en menaces quand l ennemi complote', () => {
    expect(resultatEtape(etape({ titre: 'manigance', montant: 2 }))).toBe('→ 2 menaces')
    expect(resultatEtape(etape({ titre: 'manigance', montant: 1 }))).toBe('→ 1 menace')
  })

  it('ne dit aucun resultat sans montant', () => {
    expect(resultatEtape(etape())).toBe('')
  })

  it('ne repete pas le chiffre de la menace, deja dans son titre', () => {
    expect(resultatEtape(menace({ cibleNom: 'L’Effraction !', montant: 2 }))).toBe('')
  })

  it('affiche le compteur de la cible, seuil compris', () => {
    expect(compteurEtape(etape({ restant: 5, plafond: 8 }))).toBe('5/8')
  })

  it('affiche le compteur seul quand la cible n a pas de seuil', () => {
    // Les PV d'un heros n'ont pas de plafond publie par le moteur.
    expect(compteurEtape(etape({ restant: 7 }))).toBe('7')
  })

  it('n invente aucun compteur quand le fait n en porte pas', () => {
    // Une cible sans compteur : rien vaut mieux qu'un « undefined » ou un
    // « 0/0 » affiche au joueur.
    const sansRestant = etape({ montant: 4 })
    expect(compteurEtape(sansRestant)).toBe('')
    const textes = [titreEtape(sansRestant), resultatEtape(sansRestant), compteurEtape(sansRestant)]
    for (const texte of textes) {
      expect(texte).not.toMatch(/undefined|NaN/)
    }
  })

  it('laisse tomber un seuil nul plutot que d afficher 0/0', () => {
    expect(compteurEtape(etape({ restant: 0, plafond: 0 }))).toBe('0')
  })

  it('nomme d apres le fait, pas d apres une recherche externe', () => {
    // Une carte morte pendant la phase n'est plus dans l'index du monde au
    // moment ou l'etape s'affiche : le titre doit rester juste puisqu'il lit
    // le nom porte par l'etape elle-meme, jamais une resolution a l'affichage.
    expect(titreEtape(etape({ auteurNom: 'Klaw', cibleNom: 'Drone détruit' })))
      .toBe('Klaw attaque Drone détruit')
  })
})

describe('les phrases du bilan', () => {
  const ligne = (extra: Partial<LigneBilan> = {}): LigneBilan => ({
    cle: 'degats:Colossus',
    genre: 'degats',
    cibleNom: 'Colossus',
    total: 6,
    ...extra,
  })

  it('dit ce que la cible a pris, en un total', () => {
    expect(texteLigneBilan(ligne())).toBe('Colossus a pris 6 dégâts')
  })

  it('accorde le degat au singulier', () => {
    expect(texteLigneBilan(ligne({ total: 1 }))).toBe('Colossus a pris 1 dégât')
  })

  it('dit la menace autrement que les degats', () => {
    expect(
      texteLigneBilan(ligne({ genre: 'menaces', cibleNom: 'L’Effraction !', total: 3 }))
    ).toBe('L’Effraction ! a gagné 3 menaces')
    expect(
      texteLigneBilan(ligne({ genre: 'menaces', cibleNom: 'L’Effraction !', total: 1 }))
    ).toBe('L’Effraction ! a gagné 1 menace')
  })

  it('affiche le compteur de la cible, seuil compris', () => {
    expect(compteurLigneBilan(ligne({ restant: 6, plafond: 8 }))).toBe('6/8')
  })

  it('affiche les points de vie seuls : le moteur n en publie pas le maximum', () => {
    expect(compteurLigneBilan(ligne({ restant: 8 }))).toBe('8')
  })

  it('n invente aucun compteur quand la ligne n en porte pas', () => {
    const sansCompteur = ligne()
    expect(compteurLigneBilan(sansCompteur)).toBe('')
    expect(texteLigneBilan(sansCompteur)).not.toMatch(/undefined|NaN/)
  })

  it('titre l etape de bilan par la fin de la phase, pas par un coup', () => {
    const etapeBilan: EtapeDeroule = {
      cle: 'bilan',
      temps: 'bilan',
      titre: 'bilan',
      regle: '',
      boosts: [],
      consequences: [],
      bilan: [],
    }
    expect(titreEtape(etapeBilan)).toBe('Fin de la phase du méchant')
    // Pas de regle a rappeler : le bilan n'est pas un point de la carte de
    // reference.
    expect(regleEtape(etapeBilan)).toBe('')
    // Ni chiffre ni compteur au-dessus des lignes : tout est dans les lignes.
    expect(resultatEtape(etapeBilan)).toBe('')
    expect(compteurEtape(etapeBilan)).toBe('')
  })

  it('dit qu il ne s est rien passe plutot que de rester vide', () => {
    expect(texteBilanVide()).toBe('Aucun dégât, aucune menace.')
  })

  it('annonce la chute du heros, en le nommant', () => {
    expect(texteDefaite(etape({ defaite: true, cibleNom: 'Colossus' }))).toBe(
      'Colossus est vaincu'
    )
  })

  it('ne dit rien sur une etape ordinaire', () => {
    // Le cas negatif : sans la marque, pas un mot. Une phrase de defaite
    // glissee sous un coup ordinaire ferait douter le joueur de tout le reste
    // du cartouche.
    expect(texteDefaite(etape())).toBe('')
  })

  it('se tait plutot que de nommer un heros qu il ne connait pas', () => {
    expect(texteDefaite(etape({ defaite: true, cibleNom: undefined }))).toBe('')
  })
})

// Les phrases du deroule : ecrites par nous, pas la narration du moteur.
//
// « Ultron frappe Shuri » se lit ; « [(50,01113) Klaw] would deal 2 damage »
// se dechiffre. Et tout passe par le dictionnaire : le plateau est bilingue,
// rattraper les traductions apres coup coute plus cher que de les poser tout
// de suite.
import { describe, expect, it } from 'vitest'
import {
  libelleDeStatut,
  texteCauseActivation,
  compteurEtape,
  compteurLigneBilan,
  detailEtape,
  evolutionEtape,
  texteEffet,
  regleEtape,
  resultatEtape,
  texteActivationAnnulee,
  texteAttente,
  texteBilanVide,
  texteDefaite,
  texteFenetreReponse,
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

  it('dit qu un sbire entre en jeu, ou un sbire anonyme a defaut de nom', () => {
    expect(titreEtape(etape({ titre: 'entree', cibleNom: 'Drone', auteurNom: undefined }))).toBe('Drone entre en jeu')
    expect(titreEtape(etape({ titre: 'entree', cibleNom: undefined, auteurNom: undefined }))).toBe('Un sbire entre en jeu')
  })

  it('dit la manigance autrement que l attaque', () => {
    expect(titreEtape(etape({ titre: 'manigance' }))).toBe('Ultron manigance sur Shuri')
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

  it('laisse passer un titre libre, non repertorie', () => {
    // Repli general de titreEtape pour toute cle absente de REDIGES. Ce n'est
    // PAS ainsi qu'une carte revelee se construit reellement (voir
    // deroule-phase.ts, cle 'revelation', juste en dessous) : ce test verifie
    // seulement le filet de securite.
    expect(titreEtape(etape({ temps: 'revelation', titre: 'Icy Grip révélée' })))
      .toBe('Icy Grip révélée')
  })

  it('nomme le heros qui revele sa carte', () => {
    expect(
      titreEtape(
        etape({ temps: 'revelation', titre: 'revelation', auteurNom: 'Colossus', cibleNom: 'Bombe à retardement' })
      )
    ).toBe('Colossus révèle Bombe à retardement')
  })

  it('se replie sur l ancienne formule sans heros connu', () => {
    // Joueur introuvable, ou l'appelant n'a pas fourni les noms : une carte
    // revelee anonyme vaut mieux qu'un « undefined révèle ».
    expect(
      titreEtape(etape({ temps: 'revelation', titre: 'revelation', auteurNom: undefined, cibleNom: 'Bombe à retardement' }))
    ).toBe('Bombe à retardement révélée')
  })

  // Le temps DISTRIBUTION n'avait jamais d'etape avant la tache A2 : rien ne
  // le renseignait. Sa carte est FACE CACHEE, d'ou un titre qui ne nomme que
  // le heros qui la recoit.
  it('nomme le heros qui recoit sa carte rencontre, sans nommer la carte', () => {
    expect(
      titreEtape(etape({ temps: 'distribution', titre: 'distribution', auteurNom: 'Colossus' }))
    ).toBe('Colossus reçoit sa carte rencontre')
  })

  it('se replie sur une formule impersonnelle sans heros connu', () => {
    expect(
      titreEtape(etape({ temps: 'distribution', titre: 'distribution', auteurNom: undefined }))
    ).toBe('Carte rencontre distribuée')
  })

  // Le mode Heroique en distribue plusieurs par joueur : une seule etape,
  // qui dit combien. « Colossus recoit sa carte rencontre » deux fois de suite
  // aurait dit deux fois la meme chose.
  it('compte les cartes quand un joueur en recoit plusieurs', () => {
    expect(
      titreEtape(
        etape({ temps: 'distribution', titre: 'distribution', auteurNom: 'Colossus', montant: 2 })
      )
    ).toBe('Colossus reçoit 2 cartes rencontre')
  })

  it('compte les cartes meme sans heros connu', () => {
    expect(
      titreEtape(
        etape({ temps: 'distribution', titre: 'distribution', auteurNom: undefined, montant: 3 })
      )
    ).toBe('3 cartes rencontre distribuées')
  })

  it('rappelle la regle de la distribution', () => {
    expect(regleEtape(etape({ regle: 'regle:distribution' })))
      .toBe('Point 3 : chaque joueur reçoit une carte rencontre, face cachée.')
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

  it('affiche les points de vie sur leur maximum quand il est connu', () => {
    // Le maximum ne vient pas des faits du moteur mais du monde (board.tsx) :
    // quand il l'a fourni, le bilan dit « 8/14 » au lieu de « 8 ».
    expect(compteurLigneBilan(ligne({ restant: 8, plafond: 14 }))).toBe('8/14')
  })

  it('affiche les points de vie seuls quand le maximum est inconnu', () => {
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

// ---------------------------------------------------------------------- A3 --
describe("les deux temps d'une activation", () => {
  const annonce = (extra: Partial<EtapeDeroule> = {}): EtapeDeroule =>
    etape({ etat: 'annonce', valeurAnnoncee: 4, auteurNom: 'Klaw', cibleNom: 'Colossus', ...extra })

  it("dit l'intention au futur proche, jamais au passe", () => {
    expect(titreEtape(annonce())).toBe('Klaw va attaquer Colossus')
    expect(titreEtape(annonce({ titre: 'manigance', cibleNom: 'L’Effraction !' }))).toBe(
      'Klaw va manigancer sur L’Effraction !'
    )
  })

  it("montre la valeur imprimee, dite pour ce qu'elle est", () => {
    expect(resultatEtape(annonce())).toBe('→ 4 dégâts annoncés')
    expect(resultatEtape(annonce({ valeurAnnoncee: 1 }))).toBe('→ 1 dégât annoncé')
    expect(resultatEtape(annonce({ titre: 'manigance', valeurAnnoncee: 2 }))).toBe(
      '→ 2 menaces annoncées'
    )
  })

  // L'annonce ne doit JAMAIS parler comme une resolution : sans cela, le
  // joueur lirait « → 4 dégâts » sur un coup qui n'a pas encore eu lieu, et il
  // n'apprendrait rien de plus quand il aurait lieu.
  it("ne montre aucun compteur de cible sur une annonce", () => {
    expect(compteurEtape(annonce())).toBe('')
  })

  it("dit que l'activation annulee n'a pas lieu, et garde son titre d'annonce", () => {
    const annulee = annonce({ etat: 'annule' })
    expect(titreEtape(annulee)).toBe('Klaw va attaquer Colossus')
    expect(texteActivationAnnulee(annulee)).toBe("L'attaque n'a pas lieu.")
    expect(texteActivationAnnulee(annonce({ etat: 'annule', titre: 'manigance' }))).toBe(
      "La manigance n'a pas lieu."
    )
    // Plus rien a attendre : la valeur annoncee ne s'affiche plus.
    expect(resultatEtape(annulee)).toBe('')
  })

  it('ne dit rien sur une etape qui n est pas annulee', () => {
    expect(texteActivationAnnulee(etape({ etat: 'resolu', montant: 4 }))).toBe('')
    expect(texteActivationAnnulee(annonce())).toBe('')
  })

  it('a une phrase pour la fenetre de reponse', () => {
    expect(texteFenetreReponse()).toBe('tu peux défendre ou répondre')
  })

  // La resolution, elle, ne change pas d'un mot : c'est ce que le joueur lit
  // depuis toujours, et l'annonce ne doit rien lui prendre.
  it('laisse la resolution intacte', () => {
    const resolue = etape({ etat: 'resolu', montant: 4, restant: 8 })
    expect(titreEtape(resolue)).toBe('Ultron attaque Shuri')
    expect(resultatEtape(resolue)).toBe('→ 4 dégâts')
    expect(compteurEtape(resolue)).toBe('8')
  })

  // ATTENTE : de qui parle-t-on ? « La suite arrive… » parlait du moteur, quoi
  // qu'il arrive, y compris quand la table entiere attendait un coequipier
  // (constat F5).
  it('dit qu on attend le moteur quand on n attend personne d autre', () => {
    expect(texteAttente({})).toBe('La suite arrive…')
    expect(texteAttente({ autreJoueur: false, nom: 'Spider-Man' })).toBe('La suite arrive…')
  })

  it('nomme le joueur que la table attend', () => {
    expect(texteAttente({ autreJoueur: true, nom: 'Spider-Man' })).toBe(
      'En attente de Spider-Man'
    )
  })

  // Le moteur ne publie pas quel client est en retard (voir attente-table.ts) :
  // sans nom, on le dit sans en inventer un.
  it('reste vague quand le nom du joueur en retard n est pas connu', () => {
    expect(texteAttente({ autreJoueur: true })).toBe("En attente d'un autre joueur")
  })
})

// --- Le detail du coup et l'evolution du compteur ---------------------------
// Livraison B de la spec du 7 septembre 2026 : la scene dit d'ou vient le
// chiffre (« 1 imprime + 2 (Photographic Reflexes) = 3 menaces ») et ce
// qu'il a change (« 2 → 5 / 12 »).
describe('le detail du coup', () => {
  it('additionne l imprime et les boosts, en menaces', () => {
    expect(
      detailEtape(
        etape({
          titre: 'manigance',
          etat: 'resolu',
          base: 1,
          montant: 3,
          boosts: [{ cle: 'b', nom: 'Photographic Reflexes', cibleId: 9, apport: 2 }],
        })
      )
    ).toBe('1 imprimé + 2 (Photographic Reflexes) = 3 menaces')
  })

  it('additionne plusieurs boosts, en degats', () => {
    expect(
      detailEtape(
        etape({
          etat: 'resolu',
          base: 2,
          montant: 4,
          boosts: [
            { cle: 'a', nom: 'Whip', cibleId: 9, apport: 1 },
            { cle: 'b', nom: 'Sword', cibleId: 10, apport: 1 },
          ],
        })
      )
    ).toBe('2 imprimé + 1 (Whip) + 1 (Sword) = 4 dégâts')
  })

  it('dit ce que la defense a bloque et ce qui a ete subi', () => {
    expect(
      detailEtape(
        etape({
          etat: 'resolu',
          base: 2,
          defense: 1,
          montant: 2,
          boosts: [{ cle: 'a', nom: 'Whip', cibleId: 9, apport: 1 }],
        })
      )
    ).toBe('2 imprimé + 1 (Whip) = 3 dégâts · 1 bloqué par la défense · 2 subis')
  })

  it('accorde le subi au singulier', () => {
    expect(detailEtape(etape({ etat: 'resolu', base: 2, defense: 1, montant: 1 })))
      .toBe('2 imprimé = 2 dégâts · 1 bloqué par la défense · 1 subi')
  })

  it('se replie sur le resultat simple sans imprime connu', () => {
    // Fait degrade (moteur ancien) : pas de `base`, on dit ce qu'on sait.
    expect(detailEtape(etape({ etat: 'resolu', montant: 4 }))).toBe('→ 4 dégâts')
  })

  it('se replie sur le resultat simple sans boost ni defense', () => {
    // « 2 imprime = 2 degats » n'apprendrait rien.
    expect(detailEtape(etape({ etat: 'resolu', base: 2, montant: 2 }))).toBe('→ 2 dégâts')
  })

  it('dit l annonce comme avant', () => {
    expect(detailEtape(etape({ etat: 'annonce', valeurAnnoncee: 3 }))).toBe('→ 3 dégâts annoncés')
  })

  it('ne dit rien sur une menace, dont le titre porte deja le chiffre', () => {
    expect(detailEtape(menace({ montant: 2, restant: 7, plafond: 12 }))).toBe('')
  })
})

describe('l evolution du compteur', () => {
  it('menace : avant, apres, sur le seuil', () => {
    expect(evolutionEtape(menace({ montant: 2, restant: 7, plafond: 12 }))).toBe('5 → 7 / 12')
  })

  it('manigance : la menace monte', () => {
    expect(evolutionEtape(etape({ titre: 'manigance', montant: 3, restant: 5, plafond: 12 })))
      .toBe('2 → 5 / 12')
  })

  it('attaque : les PV descendent, avec le nom de la cible', () => {
    expect(evolutionEtape(etape({ montant: 4, restant: 8 }), 12)).toBe('Shuri 12 → 8 / 12 PV')
  })

  it('attaque sans maximum connu : les PV seuls', () => {
    expect(evolutionEtape(etape({ montant: 4, restant: 8 }))).toBe('Shuri 12 → 8 PV')
  })

  it('attaque avec maximum : sur le maximum', () => {
    expect(evolutionEtape(etape({ montant: 4, restant: 8 }), 14)).toBe('Shuri 12 → 8 / 14 PV')
  })

  it('rien sans restant', () => {
    expect(evolutionEtape(etape({ montant: 4 }))).toBe('')
  })

  it('le compteur seul sans montant', () => {
    expect(evolutionEtape(etape({ restant: 5, plafond: 8 }))).toBe('5/8')
  })

  it('ne descend jamais sous zero', () => {
    // Un coup de 6 sur 4 PV : la cible avait 4, pas 6. Le maximum plafonne
    // l'avant reconstitue.
    expect(evolutionEtape(etape({ montant: 6, restant: 0 }), 4)).toBe('Shuri 4 → 0 / 4 PV')
  })
})

// --- Ce que la carte revelee a fait ------------------------------------------
describe('les effets d une revelation', () => {
  it('dit la menace posee sur une manigance', () => {
    expect(
      texteEffet({ genre: 'menace', cible: "Patrouille d'Hydra", cible_id: 3, montant: 2, restant: 5 })
    ).toBe("→ Patrouille d'Hydra gagne 2 menaces (5)")
  })

  it('dit les degats subis et le restant', () => {
    expect(texteEffet({ genre: 'degats', cible: 'Scott Lang', cible_id: 9, montant: 1, restant: 10 }))
      .toBe('→ Scott Lang subit 1 dégât (10 PV)')
  })

  it('dit la carte entree en jeu, avec son type', () => {
    expect(texteEffet({ genre: 'entree', carte: 'Hydra Mercenary', carte_id: 4, type: 'sbire' }))
      .toBe('→ Hydra Mercenary entre en jeu (sbire)')
    expect(texteEffet({ genre: 'entree', carte: 'Breakin & Takin', carte_id: 5, type: 'manigance' }))
      .toBe('→ Breakin & Takin entre en jeu (manigance)')
  })

  it('ne dit pas de restant quand le moteur ne le donne pas', () => {
    expect(texteEffet({ genre: 'menace', cible: 'X', cible_id: 3, montant: 1 })).toBe('→ X gagne 1 menace')
  })
})

describe('la cause d une activation', () => {
  // Le moteur ne remplit `cause` que pour une activation qui ne vient PAS de
  // la regle du jeu : le vilain qu'une carte revelee fait frapper une seconde
  // fois. C'est la reponse a « on dirait qu'il m'attaque deux fois sans
  // raison », signale en jeu.
  it('nomme la carte qui a declenche le coup', () => {
    expect(texteCauseActivation(etape({ cause: 'Assaut' }))).toBe('déclenché par Assaut')
  })

  it('se tait quand le coup vient de la regle du jeu', () => {
    expect(texteCauseActivation(etape())).toBe('')
    expect(texteCauseActivation(etape({ cause: '' }))).toBe('')
  })
})

describe('les cartes de statut dans le cartouche', () => {
  // Signale en jeu : « quand des cartes de statut sont donnees au mechant, aux
  // sbires ou aux joueurs, cela ne se voit pas ». Le moteur les publie
  // desormais comme des faits de la phase (sender_unit.py).
  it('nomme le porteur et la carte de statut', () => {
    expect(titreEtape(etape({ titre: 'statut', cibleNom: 'Klaw', statut: 'Stunned' }))).toBe(
      'Klaw gagne Sonné'
    )
    expect(titreEtape(etape({ titre: 'statut', cibleNom: 'Colossus', statut: 'Tough' }))).toBe(
      'Colossus gagne Robuste'
    )
  })

  it('traduit le nom que le moteur envoie, quelle que soit sa casse', () => {
    expect(libelleDeStatut('Confused')).toBe('Désorienté')
    expect(libelleDeStatut('confused')).toBe('Désorienté')
  })

  it('rend tel quel un statut qu il ne connait pas, plutot que rien', () => {
    expect(libelleDeStatut('Petrified')).toBe('Petrified')
    expect(libelleDeStatut(undefined)).toBe('')
  })

  it('se replie sur une formule impersonnelle sans porteur connu', () => {
    expect(titreEtape(etape({ titre: 'statut', cibleNom: undefined, statut: 'Stunned' }))).toBe(
      'Une carte de statut est posée : Sonné'
    )
  })

  it('le bilan compte les statuts, et distingue lesquels', () => {
    expect(
      texteLigneBilan({ cle: 'k', genre: 'statuts', statut: 'Stunned', cibleNom: 'Klaw', total: 1 })
    ).toBe('Klaw gagne Sonné')
    expect(
      texteLigneBilan({ cle: 'k', genre: 'statuts', statut: 'Tough', cibleNom: 'Klaw', total: 2 })
    ).toBe('Klaw gagne Robuste x2')
  })
})

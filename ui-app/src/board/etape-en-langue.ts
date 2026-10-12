// L'ETAPE TELLE QU'ON LA LIT : les noms en francais quand le plateau les
// connait (`nomFr`, par identifiant). Sortie de DeroulePhase le 04/10/2026 pour
// servir aussi a la revue de la phase (RevuePhase, volet du journal).
//
// `etape` reste la source pour ce qui se cherche par nom anglais (les PV
// maximum, indexes par le nom du monde).

import type { EtapeDeroule } from './deroule-phase'

export function etapeEnLangue(etape: EtapeDeroule, nomFr?: (id: number) => string | undefined): EtapeDeroule {
  const enFrancais = (id: number | undefined, nom: string | undefined) =>
    (id !== undefined ? nomFr?.(id) : undefined) || nom
  return {
    ...etape,
    // ⚠ SUR UNE REVELATION, L'AUTEUR N'EST PAS `carteId`. `carteId` designe la
    // carte REVELEE ; l'auteur, lui, est le HEROS qui la revele, et il n'a pas
    // d'identifiant dans l'etape. Traduire l'auteur par `carteId` remplacait
    // donc le nom du heros par celui de la carte, et le cartouche annoncait
    // « Maitres du Chaos revele Maitres du Chaos ».
    //
    // Signale DEUX FOIS par l'utilisateur (14/09/2026), et introuvable dans les
    // faits du moteur : une capture d'autoplay montre bien
    // `joueur_nom = 'Jessica Jones'`. Le defaut n'etait pas dans la donnee mais
    // ICI, dans la traduction. La ligne voisine (`cibleNom`) portait deja le
    // meme cas particulier, pour la meme raison, depuis le 09/09/2026.
    auteurNom: enFrancais(
      etape.titre === 'revelation' ? undefined : etape.carteId,
      etape.auteurNom
    ),
    // Sur une vraie revelation, la « cible » est la carte revelee elle-meme
    // (carteId). Mais une ATTAQUE rangee sous Revelation (le vilain qu'une
    // carte fait frapper une seconde fois) a une vraie cible : prendre
    // carteId ici ecrivait « Klaw attaque Klaw ». On decide par le TITRE, pas
    // par le temps. Signale et teste le 09/09/2026.
    cibleNom: enFrancais(etape.titre === 'revelation' ? etape.carteId : etape.cibleId, etape.cibleNom),
    boosts: etape.boosts.map((boost) => ({ ...boost, nom: enFrancais(boost.cibleId, boost.nom) ?? boost.nom })),
    effets: etape.effets?.map((effet) =>
      effet.genre === 'entree'
        ? { ...effet, carte: enFrancais(effet.carte_id, effet.carte) ?? effet.carte }
        : { ...effet, cible: enFrancais(effet.cible_id, effet.cible) ?? effet.cible }
    ),
    // ⚠ LE BILAN AUSSI, ET IL A ETE OUBLIE JUSQU'AU 15/09/2026. Mesure en
    // partie francaise : « The Break-In! a gagne 1 menace » sous un cartouche
    // qui ecrivait « L'EFFRACTION ! » deux lignes plus haut. Le bilan est
    // construit sur les etapes BRUTES (`avecBilan`), il ne passait donc par
    // aucune traduction.
    bilan: etape.bilan?.map((ligne) => ({
      ...ligne,
      cibleNom: enFrancais(ligne.cibleId, ligne.cibleNom) ?? ligne.cibleNom,
    })),
    consequences: etape.consequences?.map((consequence) => etapeEnLangue(consequence, nomFr)),
    annuleePar: enFrancais(etape.annuleeParId, etape.annuleePar),
    renfortDe: enFrancais(etape.renfortDeId, etape.renfortDe),
  }
}

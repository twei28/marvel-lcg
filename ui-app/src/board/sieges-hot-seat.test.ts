// Rattraper les sieges quand on s'est connecte TROP TOT.
//
// Ce qui a ete signale en jeu : « la partie se lance mais la main n'arrive
// qu'apres trente secondes », en jouant SEUL avec plusieurs heros.
//
// La mecanique : une partie a plusieurs heros sur un seul ecran passe par
// `hot_seat`, qui demande au moteur TOUS les sieges d'un coup. Mais le moteur
// les tire de `controller_manager.total_players`, qui vaut ZERO tant que la
// partie n'est pas montee (engine/controller/manager.py). Le site, lui, redirige
// vers le plateau des que le port repond — donc AVANT. Le client ouvrait ainsi
// son socket sur une liste de sieges vide, et n'en tenait aucun.
//
// En local le defaut ne se voit pas : on ouvre le navigateur a la main, bien
// apres le demarrage, et le compte est deja bon.
//
// Et la panne est SILENCIEUSE : le moteur n'envoie ses trames qu'aux clients
// d'un siege. Sans siege, on ne recoit rien du tout — pas d'erreur, pas de
// fermeture, juste un socket ouvert et muet. Le signal a guetter est donc
// l'absence de trame, pas son contenu.
//
// La reponse : passe un court delai sans la moindre trame, on rouvre le socket
// pour reclamer les sieges — une fois, pas en boucle.
import { describe, expect, it } from 'vitest'
import { doitRattraperLesSieges } from './sieges-hot-seat'

const cas = (extra: Partial<Parameters<typeof doitRattraperLesSieges>[0]>) =>
  doitRattraperLesSieges({
    multijoueur: false,
    trameRecue: false,
    dejaRattrape: false,
    ...extra,
  })

describe('rattrapage des sieges', () => {
  it('rouvre quand le socket est reste muet', () => {
    expect(cas({})).toBe(true)
  })

  it('ne touche a rien des qu une trame est arrivee', () => {
    // Cas normal : la partie etait deja montee, les sieges sont tenus.
    expect(cas({ trameRecue: true })).toBe(false)
  })

  it('ne rouvre pas une seconde fois', () => {
    // Sinon c'est une boucle de reconnexion, et la partie ne demarre jamais.
    expect(cas({ dejaRattrape: true })).toBe(false)
  })

  it('ne touche JAMAIS a une partie repartie sur plusieurs machines', () => {
    // La, chacun tient son siege et `hot_seat` est justement interdit : rouvrir
    // ne rapporterait rien et ferait clignoter la connexion de tout le monde.
    expect(cas({ multijoueur: true })).toBe(false)
  })

  it('ne rouvre pas non plus un multijoueur reste muet', () => {
    // Un moteur lent ou un reseau capricieux : la reconnexion ordinaire du
    // socket s'en charge deja, avec son repli progressif.
    expect(cas({ multijoueur: true, trameRecue: false })).toBe(false)
  })
})

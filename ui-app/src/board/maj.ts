import { useEffect, useState } from 'react'

// « Une mise à jour du jeu est arrivée. » — détecter qu'on tourne sur du vieux code.
//
// ⚠ POURQUOI CE FICHIER EXISTE, ET C'EST UNE REMARQUE DE L'UTILISATEUR.
// Après un déploiement, un onglet resté ouvert garde le JavaScript qu'il a
// chargé, indéfiniment. Les empreintes anti-cache (`?v=…`) ne servent qu'au
// PROCHAIN chargement de la page : elles ne réveillent personne.
//
// Constaté le 16/09/2026 en production : un onglet interrogeait encore le
// serveur toutes les deux secondes, des heures après le déploiement du
// correctif qui espace ces appels. Ma réponse avait été « pense à recharger ta
// page », et l'utilisateur a répondu ce qu'il fallait : « je n'ai pas pensé à
// ça, les autres joueurs ne vont pas y penser ».
//
// ⚠ AUCUN CHANGEMENT CÔTÉ SERVEUR, et c'est délibéré. La page relit SON PROPRE
// HTML et compare l'empreinte de son script principal à celle qu'elle a
// chargée. Le déploiement recalcule cette empreinte depuis le contenu
// (`ui-app/deployer.sh`) : elle change si et seulement si le code a changé.

/** Toutes les minutes.
 *
 *  ⚠ ETAIT A CINQ MINUTES, RACCOURCI LE 25/09/2026 (demande de l'utilisateur,
 *  cas vecu). Un deploiement pendant une session de developpement OU l'un
 *  joue et l'autre code en meme temps n'a rien d'exceptionnel : l'ecart de
 *  cinq minutes a laisse le bandeau muet le temps d'un round entier, avec le
 *  deck du heros introuvable a l'ecran (correctif deja livre, simplement pas
 *  encore vu par cet onglet). Une minute reste un ecart raisonnable devant
 *  un `fetch` unique et tres leger. */
export const PERIODE_MAJ_MS = 60_000

/** L'empreinte du script principal citée par un HTML, ou '' si introuvable.
 *
 *  Le plateau est servi par `board.html`, qui référence un fichier au nom
 *  haché (`/app/assets/board-BLVkgumq.js`) : c'est le nom ENTIER qui fait
 *  l'empreinte, il change à chaque construction. L'assistant, lui, utilise une
 *  chaîne de requête (`app.js?v=d36dcac3`). Les deux formes sont acceptées ici,
 *  pour que la même règle serve des deux côtés.
 */
export function empreinteDe(html: string): string {
  const hache = html.match(/\/app\/assets\/(board-[A-Za-z0-9_-]+\.js)/)
  if (hache) return hache[1]
  const requete = html.match(/app\.js\?v=([A-Za-z0-9.]+)/)
  if (requete) return requete[1]
  return ''
}

/** Faut-il proposer de recharger ?
 *
 *  ⚠ ON NE PROPOSE RIEN QUAND ON NE SAIT PAS. Une empreinte vide veut dire que
 *  la page a changé de forme, que le réseau a répondu de travers, ou qu'on lit
 *  une page d'erreur. Proposer un rechargement là-dessus ferait tourner le
 *  joueur en rond sans rien corriger.
 */
export function doitProposerRechargement(chargee: string, servie: string): boolean {
  if (!chargee || !servie) return false
  return chargee !== servie
}

/** L'empreinte de la page ACTUELLEMENT chargée, lue dans ses propres balises.
 *
 *  On lit le DOM plutôt qu'une constante injectée à la construction : la page
 *  dit elle-même quel script elle a chargé, et cette vérité-là ne peut pas
 *  diverger du fichier réellement servi. */
export function empreinteChargee(document: Document): string {
  const balises = Array.from(document.querySelectorAll('script[src]'))
  for (const balise of balises) {
    const empreinte = empreinteDe(balise.getAttribute('src') || '')
    if (empreinte) return empreinte
  }
  return ''
}

/** Relit la page servie et dit si elle annonce un autre script.
 *
 *  ⚠ `cache: 'no-store'` : sans cela le navigateur nous rendrait la copie qu'il
 *  a déjà, c'est-à-dire exactement celle qu'on cherche à dépasser.
 *  ⚠ Et on n'ajoute PAS de paramètre anti-cache à l'URL : la page doit être
 *  demandée telle que le joueur la demanderait.
 */
export async function versionServieDiffere(
  chargee: string,
  url = window.location.pathname,
  recuperer: typeof fetch = fetch,
): Promise<boolean> {
  if (!chargee) return false
  try {
    const reponse = await recuperer(url, { cache: 'no-store' })
    if (!reponse.ok) return false
    return doitProposerRechargement(chargee, empreinteDe(await reponse.text()))
  } catch {
    // Réseau coupé, serveur qui redémarre : on se tait. Ce n'est pas le moment
    // de réclamer un rechargement.
    return false
  }
}


/** Vrai dès qu'une version plus récente est servie.
 *
 *  ⚠ ON VERIFIE AUSSI AU RETOUR SUR L'ONGLET. Quelqu'un qui revient après deux
 *  heures ne doit pas attendre cinq minutes de plus pour l'apprendre, et c'est
 *  le moment où il va justement se remettre à jouer.
 *
 *  ⚠ ET ON NE REDEMANDE PLUS RIEN une fois la réponse connue : le bandeau est
 *  posé, le joueur décide. Continuer à interroger n'apprendrait rien.
 */
export function useMiseAJour(periode = PERIODE_MAJ_MS): boolean {
  const [aChange, setAChange] = useState(false)
  useEffect(() => {
    if (aChange) return
    const chargee = empreinteChargee(document)
    if (!chargee) return
    let vivant = true
    const verifier = async () => {
      if (!vivant || document.hidden) return
      if (await versionServieDiffere(chargee)) {
        if (vivant) setAChange(true)
      }
    }
    const minuteur = window.setInterval(verifier, periode)
    document.addEventListener('visibilitychange', verifier)
    void verifier()
    return () => {
      vivant = false
      window.clearInterval(minuteur)
      document.removeEventListener('visibilitychange', verifier)
    }
  }, [aChange, periode])
  return aChange
}

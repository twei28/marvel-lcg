// Vérifie l'armement du coach du mode Découverte.
//
// Le module visé est pur et sans import : Node peut l'exécuter tel quel, sans
// navigateur ni serveur. Même esprit que outils/verifier-salon-etat.mjs.
//
// Ce que ces cas protègent : le coach ne doit JAMAIS déborder sur une partie
// normale. Il a débordé une fois, parce que la clé de stockage n'était jamais
// effacée — un tutoriel abandonné en cours de route la laissait sur le nom
// d'une leçon, et toutes les parties suivantes la relisaient.
//
// Usage : node outils/verifier-tutoriel-etat.mjs

import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const chemin = resolve('Fusion/marvel-lcg-src/public/js/prepare/tutoriel-etat.js')
const { CLE_TUTORIEL, PREMIERE_LECON, appliquerTutoriel } =
  await import(pathToFileURL(chemin).href)

let echecs = 0
const verifier = (nom, obtenu, attendu) => {
  const ok = JSON.stringify(obtenu) === JSON.stringify(attendu)
  if (!ok) echecs += 1
  console.log(`${ok ? 'OK   ' : 'ECHEC'} ${nom}`)
  if (!ok) {
    console.log(`      obtenu  ${JSON.stringify(obtenu)}`)
    console.log(`      attendu ${JSON.stringify(attendu)}`)
  }
}

/** localStorage de test : un simple dictionnaire. */
function stockage(depart = {}) {
  const donnees = { ...depart }
  return {
    donnees,
    getItem: (k) => (k in donnees ? donnees[k] : null),
    setItem: (k, v) => { donnees[k] = String(v) },
    removeItem: (k) => { delete donnees[k] },
  }
}

const lire = (s) => s.getItem(CLE_TUTORIEL)

// Le mode Découverte arme le coach sur la première leçon.
{
  const s = stockage()
  appliquerTutoriel(s, { id: 'decouverte' })
  verifier('mode Découverte : le coach est armé', lire(s), PREMIERE_LECON)
}

// Un mode normal n'arme rien sur un stockage vierge.
{
  const s = stockage()
  appliquerTutoriel(s, { id: 'solo' })
  verifier('mode normal : rien n’est armé', lire(s), null)
}

// LE CAS DU BUG : un tutoriel abandonné en cours de route (la clé vaut le nom
// d'une leçon), puis une partie normale. La clé doit être effacée.
{
  const s = stockage({ [CLE_TUTORIEL]: 'jouer-une-carte' })
  appliquerTutoriel(s, { id: 'solo' })
  verifier('tutoriel abandonné puis partie normale : le coach est désarmé', lire(s), null)
}

// Même chose au retour à la préparation (mode inconnu) : c'est ce que fait
// app.js au chargement, et c'est ce qui couvre puzzles, reprises et salon.
{
  const s = stockage({ [CLE_TUTORIEL]: 'attaquer' })
  appliquerTutoriel(s, null)
  verifier('retour au wizard : le coach est désarmé', lire(s), null)
}

// Un tutoriel terminé ('fini') est effacé comme le reste : la valeur 'fini' ne
// sert qu'à taire le coach pendant la partie en cours.
{
  const s = stockage({ [CLE_TUTORIEL]: 'fini' })
  appliquerTutoriel(s, { id: 'solo' })
  verifier('tutoriel terminé puis partie normale : la clé est nettoyée', lire(s), null)
}

// Relancer le mode Découverte repart de la première leçon, même si une partie
// précédente s'était arrêtée plus loin.
{
  const s = stockage({ [CLE_TUTORIEL]: 'fin-du-tour' })
  appliquerTutoriel(s, { id: 'decouverte' })
  verifier('relancer le mode Découverte repart de la première leçon',
    lire(s), PREMIERE_LECON)
}

// Un stockage indisponible (navigation privée stricte) ne casse pas le
// lancement : la fonction avale l'erreur.
{
  const casse = {
    getItem: () => { throw new Error('stockage indisponible') },
    setItem: () => { throw new Error('stockage indisponible') },
    removeItem: () => { throw new Error('stockage indisponible') },
  }
  let leve = false
  try { appliquerTutoriel(casse, { id: 'decouverte' }) } catch { leve = true }
  verifier('stockage indisponible : le lancement n’échoue pas', leve, false)
}

console.log(echecs === 0 ? '\nTOUT PASSE' : `\n${echecs} ECHEC(S)`)
process.exit(echecs === 0 ? 0 : 1)

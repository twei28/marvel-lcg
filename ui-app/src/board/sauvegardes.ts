// Où cette table range ses trois emplacements de sauvegarde.
//
// ⚠ LE DOSSIER VIENT DU MOTEUR, ET JAMAIS DU CLIENT (correctif du 13/09/2026).
// Le plateau écrivait « ../replays/save_1.json » en dur : le dossier COMMUN, le
// même pour tout le monde. Sur un serveur à vingt places, les trois
// emplacements étaient donc PARTAGÉS entre tous les comptes — chacun écrasait
// la sauvegarde du voisin, et chargeait des parties qu'il n'avait jamais
// jouées. Signalé par un joueur, puis confirmé en production :
// `replays/save_1..3.json` existaient à la racine pendant que les dossiers
// `replays/serveur-N/` de chacun restaient vides.
//
// La configuration disait pourtant la vérité depuis toujours (`replay_folders`,
// séparé par place dans `tools/config_serveur.py`) : c'est le client qui
// inventait un chemin au lieu de la lire.
//
// Module À PART, et non deux fonctions dans board.tsx : importer board.tsx
// monte l'application entière, ce qui rend ces deux lignes intestables.

/** Le dossier de sauvegardes de CETTE table, demandé au moteur.
 *
 *  Le repli sur `../replays/` ne sert qu'à une partie locale, où il n'y a qu'un
 *  joueur et donc personne à écraser. */
export async function dossierSauvegardes(): Promise<string> {
  try {
    const reponse = await fetch('/get_dossier_sauvegardes', { cache: 'no-store' })
    if (!reponse.ok) return '../replays/'
    const brut = (await reponse.json()) as { dossier?: string }
    const dossier = String(brut?.dossier ?? '').trim()
    if (!dossier) return '../replays/'
    return dossier.endsWith('/') ? dossier : dossier + '/'
  } catch {
    return '../replays/'
  }
}

/** Le chemin d'un des trois emplacements, dans le dossier de CETTE table. */
export async function cheminEmplacement(slot: number): Promise<string> {
  return `${await dossierSauvegardes()}save_${slot}.json`
}

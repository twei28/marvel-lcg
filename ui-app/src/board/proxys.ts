/** Cartes dont l'image N'EST PAS un scan : un PROXY maison (moteur du createur de cartes), fait d'apres le texte de la carte en attendant
    le scan officiel. Demande du 14/11/2026 : le dire sous la carte agrandie. Retirer l'id d'ici le jour ou le vrai scan est pose.
    - 63028 Conditioned by the Hand (obligation d'Elektra) : texte lu par un joueur, aucun scan officiel publie. */
const PROXYS: ReadonlySet<string> = new Set(['63028'])

/** Vrai si l'image REELLEMENT affichee (`/scan/<id>`, `/vignette/<id>`, avec ou sans `fr_`) est un proxy. */
export function estUnProxy(url: string | undefined): boolean {
  const id = url?.match(/\/(?:fr_)?([a-z0-9]+)(?:[.?]|$)/i)?.[1]
  return !!id && PROXYS.has(id.toLowerCase())
}

/**
 * L'onglet « ASSEMBLEE » (Kingsfall multi-tables, « La ville ne dort jamais »), tire depuis le bord droit comme le Journal, l'Aide et la Ville.
 *
 * Il dit ce que les autres tables font : le code a donner aux autres groupes, la barre de Longue vie vers son seuil (2 par joueur + 2 par groupe, tous
 * groupes confondus), les degats et la menace du Roi, l'etat de chaque groupe, et le verdict quand toutes les parties sont finies. Les donnees viennent du
 * stockage commun des assemblees, relu a chaque rendu (`ToDescriptor.Assemblee`).
 */
import { useEffect, useRef, useState } from 'react'
import { t } from './langue'
import { avancementLongueVie, ETAT_DU_GROUPE, groupesEnCours, nomDuGroupe, verdictDeLAssemblee } from './assemblee-etat'
import type { AssembleeExport } from './world'
import './VoletAssemblee.css'

const LIBELLE_ETAT = {
  en_cours: 'En cours',
  victoire: 'A vaincu le Caïd',
  defaite: 'Défaite',
  abandon: 'Table fermée (défaite)',
} as const

export function VoletAssemblee({
  assemblee,
  ouvert,
  ouvrir,
  fermer,
}: {
  assemblee: AssembleeExport
  ouvert: boolean
  ouvrir: () => void
  fermer: () => void
}) {
  const [copie, setCopie] = useState(false)
  const verdict = verdictDeLAssemblee(assemblee)
  // Le verdict s'ouvre tout seul UNE fois : c'est la nouvelle que les joueurs attendent a la fin de leur partie.
  const verdictDejaMontre = useRef(false)
  useEffect(() => {
    if (verdict !== 'en_attente' && !verdictDejaMontre.current) {
      verdictDejaMontre.current = true
      ouvrir()
    }
  }, [verdict, ouvrir])
  useEffect(() => {
    if (!ouvert) return
    const surTouche = (e: KeyboardEvent) => {
      if (e.key === 'Escape') fermer()
    }
    document.addEventListener('keydown', surTouche)
    return () => document.removeEventListener('keydown', surTouche)
  }, [ouvert, fermer])

  const copier = async () => {
    try {
      await navigator.clipboard.writeText(assemblee.code)
      setCopie(true)
      window.setTimeout(() => setCopie(false), 1500)
    } catch {
      /* le code reste affiche : on peut le recopier a la main */
    }
  }
  const part = Math.round(avancementLongueVie(assemblee) * 100)
  const enCours = groupesEnCours(assemblee)

  return (
    <>
      <button
        type="button"
        className={`volet-assemblee-languette${ouvert ? ' est-ouvert' : ''}${verdict !== 'en_attente' ? ` est-${verdict}` : ''}`}
        aria-expanded={ouvert}
        aria-controls="volet-assemblee"
        aria-label={ouvert ? t('Refermer l’assemblée') : t('Ouvrir l’assemblée')}
        title={ouvert ? t('Refermer l’assemblée') : t('Ouvrir l’assemblée')}
        onClick={() => (ouvert ? fermer() : ouvrir())}
      >
        <span className="volet-assemblee-languette-texte">{t('Assemblée')}</span>
        <span className="assemblee-mini" aria-hidden="true">
          <i style={{ height: `${Math.max(4, part * 0.34)}px` }} />
        </span>
      </button>
      {ouvert ? (
        <aside id="volet-assemblee" className="volet-assemblee" role="dialog" aria-label={t('Assemblée')}>
          <header className="volet-assemblee-tete">
            <h2>{t('Assemblée')}</h2>
            <button type="button" className="reglages-fermer" onClick={fermer} title={t('Fermer')}>
              ×
            </button>
          </header>
          <div className="assemblee-corps">
            {verdict !== 'en_attente' ? (
              <p className={`assemblee-verdict est-${verdict}`} role="status">
                {verdict === 'gagnee' ? t('L’assemblée gagne !') : t('L’assemblée perd.')}
              </p>
            ) : (
              <p className="assemblee-attente">
                {enCours > 1 ? `${enCours} ${t('groupes jouent encore.')}` : enCours === 1 ? t('Un groupe joue encore.') : ''}
              </p>
            )}

            <section className="assemblee-bloc">
              <h3>{t('Code de l’assemblée')}</h3>
              <div className="assemblee-code">
                <code>{assemblee.code}</code>
                <button type="button" onClick={copier}>
                  {copie ? t('Copié') : t('Copier')}
                </button>
              </div>
              <p className="assemblee-petit">
                {t('Donnez ce code aux autres groupes : ils le saisissent en lançant leur partie.')}
              </p>
            </section>

            <section className="assemblee-bloc">
              <h3>{t('Longue vie')}</h3>
              <div
                className="assemblee-barre"
                role="progressbar"
                aria-valuemin={0}
                aria-valuemax={assemblee.seuil}
                aria-valuenow={assemblee.total_jetons}
              >
                <i style={{ width: `${part}%` }} />
              </div>
              <p className="assemblee-petit">
                {assemblee.retournee
                  ? t('Retournée : « À bas ». Chaque groupe a remis son Soutien des Citoyens.')
                  : `${assemblee.total_jetons} / ${assemblee.seuil} ${t('jetons (2 par joueur + 2 par groupe)')}`}
              </p>
            </section>

            <section className="assemblee-bloc">
              <h3>{t('Le Roi')}</h3>
              <div className="assemblee-roi">
                <span className="est-degats">
                  <b>{assemblee.degats}</b> {t('dégâts')}
                </span>
                <span className="est-menace">
                  <b>{assemblee.menace}</b> {t('menace')}
                </span>
              </div>
              <p className="assemblee-petit">{t('À la fin de toutes les parties, les dégâts égaux ou supérieurs à la menace font gagner l’assemblée.')}</p>
            </section>

            <section className="assemblee-bloc">
              <h3>{t('Groupes')}</h3>
              <ul className="assemblee-groupes">
                {assemblee.groupes.map((g) => (
                  <li key={g.tab} className={`est-${ETAT_DU_GROUPE[g.etat]}${g.tab === assemblee.table ? ' est-ici' : ''}`}>
                    <span className="assemblee-groupe-nom">
                      {nomDuGroupe(g)}
                      {g.tab === assemblee.table ? <em> · {t('cette table')}</em> : null}
                      {g.tab === assemblee.organisateur ? <em> · {t('organisatrice')}</em> : null}
                    </span>
                    <span className="assemblee-groupe-etat">{t(LIBELLE_ETAT[ETAT_DU_GROUPE[g.etat]])}</span>
                    {g.recus > 0 ? <span className="assemblee-groupe-recus">+{g.recus}</span> : null}
                  </li>
                ))}
              </ul>
            </section>
          </div>
        </aside>
      ) : null}
    </>
  )
}

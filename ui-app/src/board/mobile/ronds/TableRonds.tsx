// La TABLE en ronds : trois rangees de deux zones (voir repartir-ronds.ts), a la place des quatre bandes de cartes.
// Elle ne porte aucune logique de jeu : les ronds appellent `ouvrirCarte` / `agir` comme les bandes (PlateauPortrait).
//
// Disposition en GRILLES par zone (27/10/2026, maquette dispo-ronds.html) : chaque zone a sa grille (2x2, 1x1 ou 3x2),
// des ronds de taille fixe, et une pagination par colonne (fleches ◂ ▸) quand elle deborde sa grille. Une zone vide est
// masquee ; une rangee dont les deux zones sont vides disparait ; sinon la zone pleine occupe la rangee seule.
import { useEffect, useMemo, useRef, useState, type ReactElement, type ReactNode } from 'react'
import { t } from '../../langue'
import type { BandesPortrait } from '../bandes-portrait'
import { disposerZone } from './disposition-ronds'
import { Rond, type DecorRonds } from './Rond'
import { repartirEnRonds, type CleZone, type GroupeRond, type RangeeRonds, type TitresRonds, type UniteRond, type ZoneRonds } from './repartir-ronds'
import './ronds.css'

/** Les ronds qui viennent de quitter une zone de combat (sbire vaincu, allie vaincu) : fantomes grises « VAINCU » un instant (Q44). */
function useVaincus(zone: ZoneRonds): UniteRond[] {
  const avant = useRef<UniteRond[]>(zone.unites)
  const [fantomes, setFantomes] = useState<UniteRond[]>([])
  useEffect(() => {
    const encore = new Set(zone.unites.map((u) => u.cle))
    const partis = avant.current.filter((u) => !encore.has(u.cle))
    avant.current = zone.unites
    if (partis.length === 0 || (zone.cle !== 'sbires' && zone.cle !== 'allies')) return
    setFantomes((f) => [...f, ...partis])
    const fin = window.setTimeout(() => setFantomes((f) => f.filter((x) => !partis.includes(x))), 1100)
    return () => window.clearTimeout(fin)
  }, [zone.unites, zone.cle])
  return fantomes
}

type RondAffiche = { unite: UniteRond; vaincu: boolean }

function Zone({
  zone,
  vaincus,
  decor,
  onglets,
  page,
  setPage,
}: {
  zone: ZoneRonds
  vaincus: UniteRond[]
  decor: DecorRonds
  onglets?: ReactNode
  page: number
  setPage: (f: (p: number) => number) => void
}): ReactElement {
  // Les fantomes « vaincu » suivent les ronds ordinaires, a la fin de la zone.
  const items: RondAffiche[] = [
    ...zone.unites.map((unite) => ({ unite, vaincu: false })),
    ...vaincus.map((unite) => ({ unite, vaincu: true })),
  ]
  const dispo = disposerZone(zone.cle, items, page)
  // Les fleches defilent d'une colonne a la fois ; la pagination est bornee par `disposerZone`.
  const fleches = dispo.fleches ? (
    <span className="ronds-fleches">
      <button type="button" aria-label={t('Colonnes précédentes')} disabled={!dispo.peutReculer} onClick={() => setPage((p) => p - 1)}>
        ◂
      </button>
      <button type="button" aria-label={t('Colonnes suivantes')} disabled={!dispo.peutAvancer} onClick={() => setPage((p) => p + 1)}>
        ▸
      </button>
    </span>
  ) : null
  return (
    <section className={`ronds-zone ronds-zone-${zone.cle}`} data-zone={zone.cle} data-colonnes={dispo.colonnes.length} aria-label={zone.titre}>
      <h2 className="ronds-titre">
        {zone.titre}
        {fleches}
        {onglets}
      </h2>
      <div className="ronds-colonnes">
        {dispo.colonnes.map((colonne, c) => (
          <div className="ronds-colonne" key={dispo.page + c}>
            {colonne.map(({ unite, vaincu }) => (
              <Rond key={vaincu ? `vaincu-${unite.cle}` : unite.cle} unite={unite} zone={zone.cle} decor={decor} vaincu={vaincu} />
            ))}
          </div>
        ))}
      </div>
    </section>
  )
}

/**
 * Une rangee : ses deux zones cote a cote, un fin separateur entre elles. Une zone vide (aucun rond ET aucun fantome
 * « vaincu ») est masquee ; si les deux le sont, la rangee entiere disparait ; sinon la zone pleine l'occupe seule.
 */
function RangeeZones({
  rangee,
  decor,
  onglets,
  pageDe,
  bougerPage,
}: {
  rangee: RangeeRonds
  decor: DecorRonds
  onglets?: ReactNode
  pageDe: (cle: CleZone) => number
  bougerPage: (cle: CleZone) => (f: (p: number) => number) => void
}): ReactElement | null {
  const gVaincus = useVaincus(rangee.gauche)
  const dVaincus = useVaincus(rangee.droite)
  const gVide = rangee.gauche.unites.length === 0 && gVaincus.length === 0
  const dVide = rangee.droite.unites.length === 0 && dVaincus.length === 0
  if (gVide && dVide) return null
  return (
    <div className={`ronds-rangee ${rangee.cle}`}>
      {!gVide && (
        <Zone zone={rangee.gauche} vaincus={gVaincus} decor={decor} onglets={onglets} page={pageDe(rangee.gauche.cle)} setPage={bougerPage(rangee.gauche.cle)} />
      )}
      {!gVide && !dVide && <span className="ronds-separateur" aria-hidden="true" />}
      {!dVide && <Zone zone={rangee.droite} vaincus={dVaincus} decor={decor} page={pageDe(rangee.droite.cle)} setPage={bougerPage(rangee.droite.cle)} />}
    </div>
  )
}

export function TableRonds({
  bandes,
  decor,
  onglets,
}: {
  bandes: BandesPortrait
  decor: DecorRonds
  /** Les onglets du multijoueur, dans l'en-tete de la zone du heros. */
  onglets?: ReactNode
}): ReactElement {
  const titres: TitresRonds = {
    vilain: t('Méchant'),
    manigances: t('Manigances'),
    allies: t('Alliés'),
    sbires: t('Sbires'),
    heros: t('Héros'),
    enJeu: t('Cartes en jeu'),
  }
  const libelles = { ville: t('La ville'), environnements: t('Environnements') }
  const rangees = useMemo(() => repartirEnRonds(bandes, titres, libelles), [bandes]) // eslint-disable-line react-hooks/exhaustive-deps
  // Le toucher d'un rond de groupe : « La ville » ouvre l'onglet Ville (le meme geste que sa languette), « Environnements »
  // etale ses cartes dans la visionneuse de pile.
  const decorGroupes: DecorRonds = {
    ...decor,
    ouvrirGroupe:
      decor.ouvrirGroupe ??
      ((groupe: GroupeRond) => {
        if (groupe.genre === 'ville') (document.querySelector('.volet-ville-languette') as HTMLElement | null)?.click()
        else decor.ouvrirPile(groupe.titre, groupe.cartes)
      }),
  }
  // La page (defilement en colonnes) de chaque zone. Independante par zone ; `disposerZone` la borne au rendu.
  const [pages, setPages] = useState<Partial<Record<CleZone, number>>>({})
  const pageDe = (cle: CleZone) => pages[cle] ?? 0
  const bougerPage = (cle: CleZone) => (f: (p: number) => number) => setPages((etat) => ({ ...etat, [cle]: Math.max(0, f(etat[cle] ?? 0)) }))
  return (
    <div className="table-ronds">
      {rangees.map((rangee) => (
        <RangeeZones key={rangee.cle} rangee={rangee} decor={decorGroupes} onglets={rangee.cle === 'rangee-heros' ? onglets : undefined} pageDe={pageDe} bougerPage={bougerPage} />
      ))}
    </div>
  )
}

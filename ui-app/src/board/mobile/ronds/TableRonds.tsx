// La TABLE en ronds : trois rangees de deux zones (voir repartir-ronds.ts), a la place des quatre bandes de cartes.
// Elle ne porte aucune logique de jeu : les ronds appellent `ouvrirCarte` / `agir` comme les bandes (PlateauPortrait).
import { useEffect, useLayoutEffect, useMemo, useRef, useState, type CSSProperties, type ReactElement, type ReactNode } from 'react'
import { t } from '../../langue'
import type { BandesPortrait } from '../bandes-portrait'
import { useReglagesTelephone } from '../reglages-telephone'
import { calculerDisposition, D_AVEC_STATS, D_MIN, type Comptes, type Disposition, type ZoneDisposee } from './disposition-ronds'
import { Rond, type DecorRonds } from './Rond'
import { repartirEnRonds, type GroupeRond, type TitresRonds, type UniteRond, type ZoneRonds } from './repartir-ronds'
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

function Zone({ zone, decor, onglets, disposee }: { zone: ZoneRonds; decor: DecorRonds; onglets?: ReactNode; disposee?: ZoneDisposee }): ReactElement {
  const vaincus = useVaincus(zone)
  // Disposition adaptative (26/10/2026) : largeur, nombre de colonnes et largeur de colonne viennent de `calculerDisposition`.
  const style: CSSProperties | undefined = disposee
    ? ({
        width: `${disposee.largeur}px`,
        ['--cols' as string]: Math.max(1, disposee.colonnes),
        ['--col-w' as string]: `${disposee.largeurColonne}px`,
      } as CSSProperties)
    : undefined
  return (
    <section
      className={`ronds-zone ronds-zone-${zone.cle}${zone.unites.length === 0 && vaincus.length === 0 ? ' est-vide' : ''}`}
      data-zone={zone.cle}
      data-colonnes={disposee ? disposee.colonnes : undefined}
      style={style}
      aria-label={zone.titre}
    >
      <h2 className="ronds-titre">
        {zone.titre}
        {onglets}
      </h2>
      <div className="ronds-liste">
        {zone.unites.map((unite) => (
          <Rond key={unite.cle} unite={unite} zone={zone.cle} decor={decor} />
        ))}
        {vaincus.map((unite) => (
          <Rond key={`vaincu-${unite.cle}`} unite={unite} zone={zone.cle} decor={decor} vaincu />
        ))}
      </div>
    </section>
  )
}

/** Les comptes de ronds par zone, et le plus grand nombre d'ameliorations decalees sur le cote d'un rond (elles elargissent sa colonne). */
function comptesDes(rangees: ReturnType<typeof repartirEnRonds>): Comptes {
  const entree = (zone: ZoneRonds) => ({
    n: zone.unites.length,
    amelios: zone.unites.reduce((max, u) => Math.max(max, u.attachees.filter((a) => a.kind !== 'status').length), 0),
  })
  const [vilain, allies, heros] = rangees
  return {
    vilain: entree(vilain!.gauche),
    manigances: entree(vilain!.droite),
    allies: entree(allies!.gauche),
    sbires: entree(allies!.droite),
    heros: entree(heros!.gauche),
    enJeu: entree(heros!.droite),
  }
}

/**
 * Mesure le conteneur de la table (`.portrait-table`, la zone qui defile) et rend la disposition adaptative : le diametre des ronds, les
 * colonnes et la largeur de chaque zone. `null` tant qu'on ne mesure rien (jsdom, premier rendu) : le CSS d'origine s'applique alors.
 * Le calcul de hauteur de `calculerDisposition` est une ESTIMATION : apres chaque rendu, si le contenu depasse encore le conteneur, on
 * retire un pixel au diametre (jusqu'a 44 px) ; l'ecran defile alors verticalement, jamais horizontalement.
 */
function useDispositionRonds(racine: React.RefObject<HTMLDivElement | null>, comptes: Comptes): { disposition: Disposition; d: number } | null {
  const { colonnesZones } = useReglagesTelephone()
  const [taille, setTaille] = useState<{ largeur: number; hauteur: number } | null>(null)
  const [reduit, setReduit] = useState<{ cle: string; n: number }>({ cle: '', n: 0 })

  useLayoutEffect(() => {
    const conteneur = racine.current?.parentElement
    if (!conteneur) return
    const mesurer = () => {
      const largeur = conteneur.clientWidth
      const hauteur = conteneur.clientHeight
      setTaille((avant) => (largeur > 0 && (avant?.largeur !== largeur || avant?.hauteur !== hauteur) ? { largeur, hauteur } : largeur > 0 ? avant : null))
    }
    mesurer()
    if (typeof ResizeObserver === 'undefined') return
    const observateur = new ResizeObserver(mesurer)
    observateur.observe(conteneur)
    return () => observateur.disconnect()
  }, [racine])

  const disposition = useMemo(
    () => (taille ? calculerDisposition({ largeur: taille.largeur, hauteur: taille.hauteur, comptes, colonnes: colonnesZones }) : null),
    [taille, comptes, colonnesZones],
  )
  // Le retrait appartient a UNE disposition : quand les comptes, les colonnes ou la taille changent, on repart de l'estimation.
  const cleDeCalcul = disposition ? `${disposition.d}|${JSON.stringify(comptes)}|${JSON.stringify(colonnesZones)}|${taille?.largeur}x${taille?.hauteur}` : ''
  const retrait = reduit.cle === cleDeCalcul ? reduit.n : 0

  const d = disposition ? Math.max(D_MIN, disposition.d - retrait) : 0
  // Affinage par la mesure reelle : tant que ca depasse en hauteur, un pixel de moins.
  useLayoutEffect(() => {
    const conteneur = racine.current?.parentElement
    if (!disposition || !conteneur || d <= D_MIN) return
    if (conteneur.scrollHeight > conteneur.clientHeight + 1) setReduit((r) => ({ cle: cleDeCalcul, n: (r.cle === cleDeCalcul ? r.n : 0) + 1 }))
  }, [disposition, d, racine, cleDeCalcul])

  return disposition ? { disposition, d } : null
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
  const racine = useRef<HTMLDivElement>(null)
  const comptes = useMemo(() => comptesDes(rangees), [rangees])
  const adaptee = useDispositionRonds(racine, comptes)
  const styleTable = adaptee ? ({ ['--d' as string]: `${adaptee.d}px` } as CSSProperties) : undefined
  const classeTable = `table-ronds${adaptee ? ' est-adaptative' : ''}${adaptee && adaptee.d < D_AVEC_STATS ? ' ronds-petits' : ''}`
  return (
    <div ref={racine} className={classeTable} style={styleTable}>
      {rangees.map((rangee, i) => (
        // La largeur des deux zones suit leur nombre de ronds (24/10/2026) : trois ronds de chaque cote = moitie-moitie,
        // au lieu d'une colonne unique pour les manigances.
        <div
          key={rangee.cle}
          className={`ronds-rangee ${rangee.cle}`}
          style={{ ['--n-g' as string]: Math.max(1, rangee.gauche.unites.length), ['--n-d' as string]: Math.max(1, rangee.droite.unites.length) }}
        >
          <Zone zone={rangee.gauche} decor={decorGroupes} onglets={rangee.cle === 'rangee-heros' ? onglets : undefined} disposee={adaptee?.disposition.rangees[i]?.gauche} />
          <span className="ronds-separateur" aria-hidden="true" />
          <Zone zone={rangee.droite} decor={decorGroupes} disposee={adaptee?.disposition.rangees[i]?.droite} />
        </div>
      ))}
    </div>
  )
}

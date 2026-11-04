// La traduction française d'une carte affichée en scan anglais, et sa pose sur
// la carte : partagées par l'aperçu (Board.tsx) et les affichages en grand au
// centre (révélations, mise en place, scène de la phase du méchant).
import { useEffect, useState, type ReactNode } from 'react'
import { codeCarteConnu } from './marvelcdb'
import { aScanFr, SCANS_FR_SEULS, scanDejaFrancais, scansFrActifs } from './scans-fr'
import { TEXTES_EN_SCAN_FR } from './textes-en-scan-fr'
import { TEXTES_FR } from './textes-fr'
import { TEXTES_FR_FANMADE } from './textes-fr-fanmade'
import { TraductionPosee, type CotePaysage } from './TraductionPosee'
import { erratumDeCarte, texteErratum, type ErratumRrg } from './errata-rrg'
import { PastilleErrata } from './PastilleErrata'
import { ScanCard, type ScanCardProps } from '../components/ScanCard'

/** Texte officiel FR de la carte, de trois sources qui ne se marchent pas dessus.
 *
 *  1. Le dictionnaire HORS LIGNE des cartes officielles, mais seulement pour
 *     celles qui n'ont pas de scan francais : la ou le scan est en francais, le
 *     texte ferait doublon avec l'image.
 *  2. Le dictionnaire des packs FAN-MADE, traduit a la main. Ces cartes
 *     n'auront JAMAIS de scan francais ni de page marvelcdb : ce texte est le
 *     seul francais que le joueur verra dessus, et c'est pour elles que ce bloc
 *     compte le plus.
 *  3. A defaut, le comportement historique : marvelcdb par reseau, sur option,
 *     coupee par defaut. */
/** Le texte français à montrer pour une carte affichée en scan anglais, ou rien. */
export function useTraductionFr(codeCarte?: string, artAlternatif = false): string | undefined {
  // Deux codes, deux rôles. `code` sert de CLÉ aux dictionnaires français et
  // accepte le fan-made ; `codeCdb` désigne une page marvelcdb, que seules les
  // cartes officielles possèdent. Les confondre revenait à n'afficher aucun
  // texte français sur le contenu fan-made.
  const code = codeCarteConnu(codeCarte)
  // Un ART ALTERNATIF est un scan anglais, meme sur une carte qui a son scan
  // francais : il faut alors le texte francais de TOUTES les cartes
  // (textes-fr-complets.ts, 700 Ko), charge une fois a la demande.
  // L'inverse : scan FRANCAIS seul, interface en anglais -> le texte anglais se pose sur le scan voile (TraductionPosee, langue 'en').
  if (code !== undefined && !artAlternatif && SCANS_FR_SEULS.has(code) && !scansFrActifs()) return TEXTES_EN_SCAN_FR[code]
  const scanAnglais = code !== undefined && scansFrActifs() && (artAlternatif || (!aScanFr(code) && !scanDejaFrancais(code)))
  const [textesComplets, setTextesComplets] = useState<Readonly<Record<string, string | undefined>>>()
  useEffect(() => {
    if (!scanAnglais || !artAlternatif || textesComplets) return
    let vivant = true
    import('./textes-fr-complets')
      .then((module) => {
        if (vivant) setTextesComplets(module.TEXTES_FR_COMPLETS)
      })
      .catch(() => undefined)
    return () => {
      vivant = false
    }
  }, [scanAnglais, artAlternatif, textesComplets])
  const repli =
    code && scanAnglais
      ? (TEXTES_FR[code] ?? TEXTES_FR_FANMADE[code] ?? textesComplets?.[code])
      : undefined
  return repli
}


/**
 * Le texte à poser sur une carte agrandie, et sa langue : l'ERRATA officiel s'il y en a un (dans la langue des scans actifs,
 * posé sur n'importe quel scan : l'ancien texte imprimé est sous le voile), sinon la traduction. `langue` absente = le
 * comportement historique de TraductionPosee. Un errata sans texte (titre, icône, classification) ne donne que la pastille.
 */
export function useTexteSurCarte(
  codeCarte?: string,
  artAlternatif = false
): { texte: string; langue?: 'fr' | 'en'; erratum?: ErratumRrg } | undefined {
  const traduction = useTraductionFr(codeCarte, artAlternatif)
  const erratum = erratumDeCarte(codeCarte)
  const langue: 'fr' | 'en' = scansFrActifs() ? 'fr' : 'en'
  const texteErrata = erratum ? texteErratum(erratum, langue) : undefined
  if (erratum && texteErrata) return { texte: texteErrata, langue, erratum }
  return traduction ? { texte: traduction } : undefined
}

/** Côté de la boîte de texte d'une carte paysage, selon son type. */
export function coteDuTexte(type: string | undefined): CotePaysage | undefined {
  if (type === 'MainScheme') return 'gauche'
  // La manigance annexe de JOUEUR est imprimée comme celle des méchants : boîte de texte à droite (audit du 25/10/2026 : sans cela,
  // ses 21 cartes fan-made gardaient leur anglais).
  if (type === 'SideScheme' || type === 'PlayerSideScheme') return 'droite'
  return undefined
}

/**
 * La traduction posée sur une carte affichée en grand, ou rien : même
 * condition que l'aperçu (français, scan anglais, traduction connue).
 * `paysage` : la carte est montrée couchée.
 */
export function useSurcoucheTraduction(carte: {
  codeCarte?: string
  artAlternatif?: boolean
  imageUrl?: string
  traits?: readonly string[]
  type?: string
  paysage?: boolean
  facedown?: boolean
}): ReactNode | undefined {
  const codeCarte = carte.facedown ? undefined : carte.codeCarte
  const surcouche = useTexteSurCarte(codeCarte, carte.artAlternatif)
  const erratum = erratumDeCarte(codeCarte)
  const cote = carte.paysage ? coteDuTexte(carte.type) : undefined
  const voile =
    surcouche && carte.imageUrl && !(carte.paysage && !cote) ? (
      <TraductionPosee url={carte.imageUrl} texte={surcouche.texte} traits={carte.traits} paysage={cote} langue={surcouche.langue} />
    ) : undefined
  if (!voile && !erratum) return undefined
  return (
    <>
      {voile}
      {erratum ? <PastilleErrata erratum={erratum} cote={cote} /> : null}
    </>
  )
}

/** Le type de carte du moteur ramené à celui qui place la boîte de texte paysage. */
export function typeDeBoite(cardType: string | undefined): string | undefined {
  if (cardType === 'MainScheme') return 'MainScheme'
  if (cardType && /SideScheme$/.test(cardType)) return 'SideScheme'
  return cardType
}

/** La même chose en composant, pour un cadre qui n'est pas une ScanCard. */
export function TraductionSurCarte(props: Parameters<typeof useSurcoucheTraduction>[0]) {
  return <>{useSurcoucheTraduction(props)}</>
}

/** Une ScanCard qui porte sa traduction posée (affichages en grand hors aperçu). */
export function ScanCardTraduite(props: ScanCardProps) {
  const surcouche = useSurcoucheTraduction({
    codeCarte: props.codeCarte,
    artAlternatif: props.artAlternatif,
    imageUrl: props.imageUrl,
    traits: props.traits,
    paysage: props.isLandscape,
    type: props.kind === 'main-scheme' ? 'MainScheme' : props.kind === 'side-scheme' ? 'SideScheme' : undefined,
    facedown: props.facedown,
  })
  return <ScanCard {...props} surcouche={props.surcouche ?? surcouche} />
}

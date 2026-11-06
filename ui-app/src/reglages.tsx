// reglages.tsx — le panneau Reglages du plateau (FenetreReglages), monte
// SEUL, hors de toute partie : demande de l'utilisateur, 06/11/2026, que la
// tuile « Options » de l'accueil ouvre « exactement la meme chose » qu'en
// jeu, pas une resucee (voir l'ancien `demanderLAffichage`, app.js).
//
// Chargee dans une iframe par l'accueil (vanilla JS, autre bundle) :
// isoler le document evite tout risque de collision avec board.css (10 000+
// lignes, classes non scopees). Les reglages eux-memes lisent/ecrivent les
// MEMES cles localStorage que le plateau (modules partages, voir chaque
// import ci-dessous) : un bascule ici vaut pour la prochaine partie, et vice
// versa.
//
// `FenetreReglages` est rendue en continu (`ouvert` ne vaut jamais false) :
// cette page ENTIERE est le panneau. `fermer` previent le parent par
// `postMessage`, qui retire l'iframe de sa propre modale.
import { useCallback, useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import '../styles/tokens.css'
import '../styles/palette.css'
import '../styles/affichage-sobre.css'
import '../styles/affichage-epure.css'
import '../styles/teinte.css'
import './board/board.css'
import { FenetreReglages } from './board/FenetreReglages'
import {
  appliquerAffichage,
  chercherAffichageDuCompte,
  CLE_AFFICHAGE,
  ecrireAffichage,
  lireAffichage,
  retenirEpurePermis,
  type Affichage,
} from './board/affichage'
import { appliquerTeinte, chercherTeinteDuCompte, ecrireTeinte, envoyerTeinteAuCompte, lireTeinteDuNavigateur, type Teinte } from './board/teinte'
import { essaisOuverts } from './board/essais'
import { CLE_ANIMATIONS, CLE_MODE_ACTIONS, CLE_REVELATION, CLE_SONS, lireAnimations, lireModeActions, lireRevelation, lireSons } from './board/reglages-divers'
import { CLE_MUSIQUE, lireMusiqueActive } from './board/musique'
import { CLE_SCANS_FR, scansFrActifs } from './board/scans-fr'
import { CLE_DOS_CARTES, lireDosCartes, type DosCartes } from './board/dos-cartes'
import { CLE_TEXTES_CDB, lireTextesCdb } from './board/marvelcdb'
import { basculerLangue } from './board/langue'
import {
  ecrireFinTourAuto,
  ecrireModePhaseMechant,
  ecrireReponseAmbiance,
  ecrireSauvegardeAuto,
  libelleModePhase,
  lireFinTourAuto,
  lireModePhaseMechant,
  lireReponseAmbiance,
  lireSauvegardeAuto,
  type ModeActions,
  type ModePhaseMechant,
  type ReponseAmbiance,
} from './board/moteur'
import { texteTempsParDecision } from './board/deroule-textes'
import {
  CLE_AUTO_CIBLE,
  CLE_VALIDATION_COURTE,
  ecrirePaiementAuto,
  lireAutoCible,
  lirePaiementAuto,
  lireValidationCourte,
} from './board/interaction'
import { CLE_METEO, lireMeteoActive, type ApercuMeteo } from './board/CoucheMeteo'
import { CLE_DESIGN_ESSAI, lireDesignEssai } from './board/design-essai'
import { CLE_CURSEURS, lireCurseursActifs } from './board/CoucheCurseurs'
import { useModeMobile } from './board/mobile/useModeMobile'
import { useEstTelephone } from './board/mobile/telephone'
import { useEstTablette } from './board/tablette/tablette'

/** Prevenu le parent (l'accueil) que le panneau doit se fermer. */
function fermer(): void {
  window.parent.postMessage({ marvelReglages: 'fermer' }, '*')
}

function PanneauReglagesAutonome() {
  const [affichage, setAffichage] = useState<Affichage>(lireAffichage)
  useEffect(() => {
    appliquerAffichage(affichage)
  }, [affichage])
  useEffect(() => {
    let vivant = true
    void essaisOuverts().then((ouverts) => {
      retenirEpurePermis(ouverts)
      if (vivant) setAffichage(lireAffichage())
    })
    void chercherAffichageDuCompte().then((duCompte) => {
      if (!vivant || duCompte === undefined) return
      try {
        window.localStorage.setItem(CLE_AFFICHAGE, duCompte)
      } catch {
        /* stockage indisponible */
      }
      setAffichage(duCompte)
    })
    return () => {
      vivant = false
    }
  }, [])
  const changerAffichage = useCallback((choisi: Affichage) => {
    ecrireAffichage(choisi)
    setAffichage(choisi)
  }, [])

  const [teinte, setTeinte] = useState<Teinte | undefined>(lireTeinteDuNavigateur)
  useEffect(() => {
    appliquerTeinte(teinte)
  }, [teinte])
  useEffect(() => {
    let vivant = true
    void chercherTeinteDuCompte().then((duCompte) => {
      if (!vivant || duCompte === undefined) return
      ecrireTeinte(duCompte ?? undefined, false)
      setTeinte(duCompte ?? undefined)
    })
    return () => {
      vivant = false
    }
  }, [])
  const retenirTeinte = useCallback((choisie: Teinte | undefined) => {
    ecrireTeinte(choisie, false)
    setTeinte(choisie)
    window.setTimeout(() => envoyerTeinteAuCompte(choisie), 600)
  }, [])
  const changerTeinte = useCallback((choisie: Teinte) => retenirTeinte(choisie), [retenirTeinte])
  const reinitialiserTeinte = useCallback(() => retenirTeinte(undefined), [retenirTeinte])

  const [animations, setAnimations] = useState(lireAnimations)
  const basculerAnimations = useCallback(() => {
    setAnimations((a) => {
      const nouveau = !a
      try {
        window.localStorage.setItem(CLE_ANIMATIONS, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [sons, setSons] = useState(lireSons)
  const basculerSons = useCallback(() => {
    setSons((s) => {
      const nouveau = !s
      try {
        window.localStorage.setItem(CLE_SONS, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [musique, setMusique] = useState(lireMusiqueActive)
  const basculerMusique = useCallback(() => {
    setMusique((m) => {
      const nouveau = !m
      try {
        window.localStorage.setItem(CLE_MUSIQUE, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [scansFr, setScansFr] = useState(scansFrActifs)
  const basculerScansFr = useCallback(() => {
    setScansFr((s) => {
      const nouveau = !s
      try {
        window.localStorage.setItem(CLE_SCANS_FR, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [dosCartes, setDosCartes] = useState<DosCartes>(lireDosCartes)
  const changerDosCartes = useCallback((choix: DosCartes) => {
    try {
      window.localStorage.setItem(CLE_DOS_CARTES, choix)
    } catch {
      /* preference non critique */
    }
    setDosCartes(choix)
  }, [])

  const [textesCdb, setTextesCdb] = useState(lireTextesCdb)
  const basculerTextesCdb = useCallback(() => {
    setTextesCdb((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_TEXTES_CDB, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [modePhase, setModePhase] = useState<ModePhaseMechant>(lireModePhaseMechant)
  const changerModePhase = useCallback((mode: ModePhaseMechant) => {
    setModePhase(mode)
    ecrireModePhaseMechant(mode)
  }, [])

  const [validationCourte, setValidationCourte] = useState(lireValidationCourte)
  const basculerValidationCourte = useCallback(() => {
    setValidationCourte((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_VALIDATION_COURTE, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [autoCible, setAutoCible] = useState(lireAutoCible)
  const basculerAutoCible = useCallback(() => {
    setAutoCible((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_AUTO_CIBLE, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [finTourAutoChoix, setFinTourAutoChoix] = useState(lireFinTourAuto)
  const basculerFinTourAuto = useCallback(() => {
    setFinTourAutoChoix((c) => {
      const nouveau = c === 'on' ? 'off' : 'on'
      ecrireFinTourAuto(nouveau)
      return nouveau
    })
  }, [])

  // Paiement automatique : pas de partie, donc rien a payer ici -- expose
  // quand meme le reglage (demande de l'utilisateur, « exactement la meme
  // chose »), avec la meme cle que le plateau (CLE_PAIEMENT_AUTO).
  const [paiementAutoChoix, setPaiementAutoChoix] = useState(lirePaiementAuto)
  const basculerPaiementAuto = useCallback(() => {
    setPaiementAutoChoix((c) => {
      const nouveau = c === 'on' ? 'off' : 'on'
      ecrirePaiementAuto(nouveau)
      return nouveau
    })
  }, [])

  const [sauvegardeAuto, setSauvegardeAuto] = useState(lireSauvegardeAuto)
  const basculerSauvegardeAuto = useCallback(() => {
    setSauvegardeAuto((v) => {
      const nouveau = !v
      ecrireSauvegardeAuto(nouveau)
      return nouveau
    })
  }, [])

  const [revelation, setRevelation] = useState(lireRevelation)
  const cyclerRevelation = useCallback(() => {
    setRevelation((r) => {
      const suivant = r === 'off' ? 'court' : r === 'court' ? 'long' : 'off'
      try {
        window.localStorage.setItem(CLE_REVELATION, suivant)
      } catch {
        /* preference non critique */
      }
      return suivant
    })
  }, [])

  const [meteo, setMeteo] = useState(lireMeteoActive)
  const basculerMeteo = useCallback(() => {
    setMeteo((m) => {
      const nouveau = !m
      try {
        window.localStorage.setItem(CLE_METEO, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])
  const [apercuMeteo, setApercuMeteo] = useState<ApercuMeteo>(undefined)

  const [reponseAmbiance, setReponseAmbiance] = useState<ReponseAmbiance>(lireReponseAmbiance)
  const cyclerReponseAmbiance = useCallback(() => {
    setReponseAmbiance((r) => {
      const suivant: ReponseAmbiance = r === 'demander' ? 'toujours' : r === 'toujours' ? 'jamais' : 'demander'
      ecrireReponseAmbiance(suivant)
      return suivant
    })
  }, [])

  const [designEssai, setDesignEssai] = useState(() => {
    try {
      return lireDesignEssai(window.location.search, window.localStorage)
    } catch {
      return false
    }
  })
  const basculerDesignEssai = useCallback(() => {
    setDesignEssai((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_DESIGN_ESSAI, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const [modeActions, setModeActions] = useState<ModeActions>(() => lireModeActions())
  const changerModeActions = useCallback((mode: ModeActions) => {
    setModeActions(mode)
    try {
      window.localStorage.setItem(CLE_MODE_ACTIONS, mode)
    } catch {
      /* preference non critique */
    }
  }, [])

  const [curseurs, setCurseurs] = useState(lireCurseursActifs)
  const basculerCurseurs = useCallback(() => {
    setCurseurs((v) => {
      const nouveau = !v
      try {
        window.localStorage.setItem(CLE_CURSEURS, nouveau ? 'on' : 'off')
      } catch {
        /* preference non critique */
      }
      return nouveau
    })
  }, [])

  const { reglage: reglageMode, surAppareilMobile, changer: changerReglageMode } = useModeMobile()
  const cyclerReglageMode = useCallback(() => {
    changerReglageMode(reglageMode === 'pc' ? 'auto' : 'pc')
  }, [reglageMode, changerReglageMode])

  const telephone = useEstTelephone()
  const tablette = useEstTablette()

  return (
    <FenetreReglages
      ouvert
      fermer={fermer}
      affichage={affichage}
      changerAffichage={changerAffichage}
      teinte={teinte}
      changerTeinte={changerTeinte}
      reinitialiserTeinte={reinitialiserTeinte}
      animations={animations}
      basculerAnimations={basculerAnimations}
      sons={sons}
      basculerSons={basculerSons}
      musique={musique}
      basculerMusique={basculerMusique}
      scansFr={scansFr}
      basculerScansFr={basculerScansFr}
      dosCartes={dosCartes}
      changerDosCartes={changerDosCartes}
      textesCdb={textesCdb}
      basculerTextesCdb={basculerTextesCdb}
      basculerLangue={basculerLangue}
      modePhase={modePhase}
      changerModePhase={changerModePhase}
      libelleModePhase={libelleModePhase}
      // Pas de partie en cours : aucune limite de temps a afficher.
      tempsParDecision={0}
      texteTempsParDecision={texteTempsParDecision}
      validationCourte={validationCourte}
      basculerValidationCourte={basculerValidationCourte}
      autoCible={autoCible}
      basculerAutoCible={basculerAutoCible}
      finTourAuto={finTourAutoChoix === 'on'}
      basculerFinTourAuto={basculerFinTourAuto}
      paiementAuto={paiementAutoChoix === 'on'}
      basculerPaiementAuto={basculerPaiementAuto}
      sauvegardeAuto={sauvegardeAuto}
      basculerSauvegardeAuto={basculerSauvegardeAuto}
      revelation={revelation}
      cyclerRevelation={cyclerRevelation}
      meteo={meteo}
      basculerMeteo={basculerMeteo}
      apercuMeteo={apercuMeteo}
      reglerApercuMeteo={setApercuMeteo}
      reponseAmbiance={reponseAmbiance}
      cyclerReponseAmbiance={cyclerReponseAmbiance}
      designEssai={designEssai}
      basculerDesignEssai={basculerDesignEssai}
      modeActions={modeActions}
      changerModeActions={changerModeActions}
      curseurs={curseurs}
      basculerCurseurs={basculerCurseurs}
      montrerDisposition={surAppareilMobile}
      reglageMode={reglageMode}
      cyclerReglageMode={cyclerReglageMode}
      telephone={telephone}
      tablette={tablette}
    />
  )
}

// Echap ferme aussi depuis le document de l'iframe (FenetreReglages l'ecoute
// deja elle-meme ; ce doublon n'est pas necessaire -- gardé minimal ici).
const racine = document.getElementById('reglages')
if (racine) createRoot(racine).render(<PanneauReglagesAutonome />)

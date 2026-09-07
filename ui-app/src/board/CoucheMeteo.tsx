// CoucheMeteo — la météo du plateau.
//
// Un effet HTML autonome (public/effects/weather/) est superposé en iframe
// plein écran. À l'origine il ne servait qu'aux Soutiens météo de Storm ;
// il lit désormais aussi les cartes d'Environnement, qui vivent ailleurs.
//
// ON NE LIT QUE CE QUI EST EN JEU, par zones nommées. Le code d'origine
// parcourait tout l'objet joueur, main et decks compris : or Storm joue avec
// un DECK météo (`additional_deck`) qui contient ses trois autres cartes. Il
// ne s'en sortait que parce que `supports` précède `additional_deck` dans
// l'ordre des clés du descripteur, ce qui est un accident, pas une garantie.
//
// L'aperçu (sélecteur des réglages) prime sur les cartes tant qu'il est actif :
// c'est un outil de conception, il doit pouvoir montrer un effet sans partie.
import { useMemo } from 'react'
import type { World, WorldCard } from './world'
import { t } from './langue'
import type { ReponseAmbiance } from './moteur'

/** Les effets qu'on sait afficher, pour le sélecteur d'aperçu. */
export const EFFETS_METEO = [
  'rain', 'storm', 'snow', 'fog', 'stars', 'embers',
  'dust', 'neon', 'jungle',
  'noir', 'horror', 'cyber', 'sitcom', 'sepia', 'sandstorm',
] as const
export type EffetMeteo = (typeof EFFETS_METEO)[number]

/** Le nom affiché de chaque effet. Une table, et non une suite de ternaires :
 *  le sélecteur en compte six et en comptera davantage. */
export const LIBELLE_EFFET: Record<EffetMeteo, string> = {
  rain: 'Pluie',
  storm: 'Orage',
  snow: 'Neige',
  fog: 'Brume',
  stars: 'Étoiles',
  embers: 'Braises',
  dust: 'Poussière',
  neon: 'Néons',
  jungle: 'Jungle',
  noir: 'Noir et blanc',
  horror: 'Horreur',
  cyber: 'Cyber',
  sitcom: 'Sitcom',
  sepia: 'Sépia',
  sandstorm: 'Tempête de sable',
}

/**
 * L'apercu est une LISTE d'effets, parce qu'on doit pouvoir en essayer
 * plusieurs a la fois depuis que les ambiances se superposent en jeu.
 *
 * Trois etats, et ils ne disent pas la meme chose :
 *   undefined -> Auto, ce sont les cartes qui decident, c'est le mode normal ;
 *   []        -> Aucun, le vide impose meme si une carte declencherait
 *                quelque chose ;
 *   [ ... ]   -> exactement ces effets, empiles dans cet ordre.
 *
 * Sans la distinction entre les deux premiers, « Aucun » signifiait en
 * realite « Auto » et il n'existait aucun moyen de couper temporairement
 * l'ambiance sans toucher au reglage lui-meme.
 */
export type ApercuMeteo = readonly string[] | undefined

export function libelleApercu(apercu: ApercuMeteo): string {
  if (apercu === undefined) return 'Auto'
  if (apercu.length === 0) return 'Aucun'
  if (apercu.length === 1) return LIBELLE_EFFET[apercu[0] as EffetMeteo] ?? apercu[0]
  return `${apercu.length} effets`
}

/** L'ambiance appartient au SCÉNARIO et aux modules, jamais aux cartes que le
 *  joueur monte dans son deck. Un lieu joué par un héros est sa base, une
 *  carte de sa main : il n'a pas à repeindre la table pour tout le monde.
 *  Seize Soutiens de héros ont été câblés le 8/8/2026 puis retirés pour cette
 *  raison ; un cas de test refuse désormais toute carte de deck de joueur.
 *
 *  La seule exception est le deck météo de Storm, et elle se justifie : son
 *  sujet EST la météo, changer le temps est sa capacité, et c'est pour ces
 *  trois cartes que la couche a été écrite.
 *
 *  La table est typée sur les effets connus : une faute de frappe ici
 *  demanderait un fichier HTML inexistant, et l'écran resterait vide. */
export const METEO_PAR_CARTE: Record<string, EffetMeteo> = {
  // Storm — deck météo. 36002 Clear Skies n'a volontairement aucun visuel.
  '36003': 'rain', // Hurricane
  '36004': 'storm', // Thunderstorm
  '36005': 'snow', // Blizzard
  // Environnements
  '04081': 'snow', // Snowy Hillside, Absorbing Man
  '29039': 'storm', // Air Static, Zzzax
  '50131a': 'storm', // Justice, Like Lightning, Thunderbolts
  // Lieux clos, souterrains ou boises
  '04080': 'fog', // Dense Forest, Tourist Trap
  '16085a': 'fog', // Library Labyrinth, Galaxy's Most Wanted
  '24060': 'fog', // Back-Alley Enclave, The Hood
  '24061': 'fog', // Secret Lair, The Hood
  '24062': 'fog', // Sewer Tunnels, The Hood
  '27077a': 'fog', // Bell Tower silencieux, Sinister Motives
  '27077b': 'fog', // Bell Tower qui sonne, Sinister Motives
  // Vaisseaux et espace
  '16063': 'stars', // Badoon Ship
  '16085b': 'stars', // Museum Ship
  '16093': 'stars', // Nebula's Ship
  '16108': 'stars', // Kree Command Ship
  '16143': 'stars', // Rogue Vessel
  '45139': 'stars', // Blue Area of the Moon, Age of Apocalypse
  // Feu
  '21076': 'embers', // Fireball, The Mad Titan's Shadow
  '90128': 'embers', // Burning Building, Rainy
  // Pierre, metal et gravats
  '04082': 'dust', // Rocky Outcrop, Tourist Trap
  '04083': 'dust', // Abandoned Facility, Tourist Trap
  '21079': 'dust', // Rubblestorm, The Mad Titan's Shadow
  // La tour des Avengers a deux faces. Seule l'ENDOMMAGEE prend la poussiere :
  // intacte (21100a, STRONGHOLD), elle n'a aucune raison d'en avoir.
  '21100b': 'dust', // Avengers Tower endommagee, The Mad Titan's Shadow
  // La rue la nuit
  '24063': 'neon', // Warehouse District, The Hood
  '27065': 'sandstorm', // City Streets : la rue de Sandman, dans son scenario
  '31037': 'neon', // Surge in Crime, SP//dr
  // Vegetation
  '45127': 'jungle', // The Savage Land, Age of Apocalypse
  '45133': 'jungle', // Genosha, Age of Apocalypse
  // --- Mojoverse -----------------------------------------------------------
  // Chaque decor est une parodie de genre televise. Le genre ne se devine pas
  // au titre mais aux figurants qui l'accompagnent dans le paquet : Dragnet et
  // Law & Order d'un cote, Dragon et Troll de l'autre, Vampire et Loup-garou,
  // des PROGRAMMES nommes Magneto 2.6, un Gunslinger.
  '39035': 'noir', // Dial M for Mojo : le polar rendu en noir et blanc
  '39041': 'embers', // A Game of Mojo's, fantasy : le souffle du Dragon
  '39047': 'horror', // The Mojo Files, vampires et loups-garous
  '39053': 'cyber', // Mojo Runner, ennemis PROGRAMME
  '39060': 'sitcom', // Mojo in the Middle, comedie familiale
  '39066': 'sepia', // Wild Wild Mojo, western

  // Sans ambiance, par choix : les trois Manhattan infestes (27117b, 27118b,
  // 27119b) et Skies Over New York (27116b). Leurs effets ont ete ecrits puis
  // retires, ils ne rendaient pas ce qu'ils devaient rendre.
  //
  // Sans ambiance egalement : la Roue des genres (39026a/b) et les faces de
  // foule (39003a/b, 39004a/b) restent muettes a dessein, car elles sont en
  // jeu EN MEME TEMPS que le decor et lui disputeraient l'affichage puisque
  // la couche ne montre qu'un effet.
}

/** Les zones où une carte est réellement EN JEU, et elles seules. */
const ZONES_JOUEUR = ['supports', 'environment_area'] as const
const ZONES_MONDE = ['area_environment'] as const

/**
 * La cle de stockage garde son nom d'origine. Le reglage s'appelle desormais
 * « Ambiance » a l'ecran, la couche ne faisant plus seulement de la meteo,
 * mais la renommer ici remettrait l'interrupteur a zero chez qui l'avait
 * coupe. Les noms de code suivent la meme logique : CoucheMeteo, meteoDuMonde
 * et les autres restent tels quels, un renommage massif n'apportant rien.
 */
export const CLE_METEO = 'marvel-board-meteo'

export function lireMeteoActive(): boolean {
  try {
    return window.localStorage.getItem(CLE_METEO) !== 'off'
  } catch {
    return true
  }
}

/**
 * Etat suivant de « Ambiance » et de son apercu apres un clic sur
 * l'interrupteur general (voir `basculerMeteo` dans board.tsx). Couper
 * « Ambiance » remet TOUJOURS l'apercu sur Auto (undefined) : sinon un
 * apercu fige un jour pour essayer un effet continuerait de le forcer a
 * l'ecran malgre l'interrupteur general coupe, sans que rien ne le signale
 * (voir `effetsAffiches` ci-dessus, ou l'apercu prime sur `active`).
 * Rallumer, a l'inverse, ne touche jamais a l'apercu : ce n'est pas a
 * l'interrupteur general de decider quel effet montrer.
 */
export function basculerAmbiance(meteoActuelle: boolean): {
  meteo: boolean
  reinitialiserApercu: boolean
} {
  const meteo = !meteoActuelle
  return { meteo, reinitialiserApercu: !meteo }
}

function cartesDe(source: unknown, zones: readonly string[]): WorldCard[] {
  if (typeof source !== 'object' || source === null) return []
  const sortie: WorldCard[] = []
  for (const zone of zones) {
    const valeur = (source as Record<string, unknown>)[zone]
    // Certaines zones sont des listes de listes (decks multiples) : on aplatit.
    if (Array.isArray(valeur)) sortie.push(...(valeur.flat() as WorldCard[]))
  }
  return sortie
}

/**
 * Les cartes EN JEU, dans l'ordre de PEINTURE : le décor du scénario d'abord,
 * donc en dessous, puis les cartes des joueurs par-dessus, siège par siège.
 *
 * Sortie en un seul endroit parce que deux lectures s'en servent, `meteosDuMonde`
 * et `premiereCarteAmbiance` : elles doivent voir exactement les mêmes zones,
 * sans quoi la modale nommerait une carte dont l'ambiance ne s'allume pas, ou
 * l'inverse.
 */
function cartesEnJeu(world: World | undefined): WorldCard[] {
  if (!world) return []
  const enJeu: WorldCard[] = [...cartesDe(world, ZONES_MONDE)]
  for (const joueur of world.players ?? []) enJeu.push(...cartesDe(joueur, ZONES_JOUEUR))
  return enJeu
}

/**
 * TOUTES les ambiances dictées par les cartes en jeu, sans doublon.
 *
 * Elles se superposent au lieu de se disputer l'affichage. Le choix n'est pas
 * gratuit : mesuré le 8/8/2026, empiler trois effets ne coûte pas une image
 * par seconde. Ce qui coûtait, c'était le `filter: blur()` de cinq d'entre
 * eux, remplacé depuis par un masque.
 *
 * L'ordre est l'ordre de PEINTURE, celui de `cartesEnJeu`.
 */
export function meteosDuMonde(world: World | undefined): string[] {
  const sortie: string[] = []
  for (const carte of cartesEnJeu(world)) {
    const effet = carte && typeof carte.card_id === 'string' ? METEO_PAR_CARTE[carte.card_id] : undefined
    if (effet && !sortie.includes(effet)) sortie.push(effet)
  }
  return sortie
}

/** La CAUSE d'une ambiance : la carte qui l'allume, et ce qu'elle allume. */
export type CarteAmbiance = {
  /** L'identifiant de la carte, tel qu'il figure dans METEO_PAR_CARTE. */
  cardId: string
  /** Le nom affichable de la carte, celui que le moteur donne. */
  nom: string
  effet: EffetMeteo
}

/**
 * La première carte en jeu qui allume une ambiance, ou `undefined`.
 *
 * `meteosDuMonde` rend des effets, jamais leur cause : « noir » ne dit rien à
 * personne. Pour expliquer au joueur ce qui vient de repeindre sa table, il
 * faut pouvoir écrire « Dial M for Mojo ».
 *
 * « Première » au sens de l'ordre de peinture : le décor du scénario passe
 * avant la carte d'un joueur, et c'est bien lui la cause visible.
 */
export function premiereCarteAmbiance(world: World | undefined): CarteAmbiance | undefined {
  for (const carte of cartesEnJeu(world)) {
    if (!carte || typeof carte.card_id !== 'string') continue
    const effet = METEO_PAR_CARTE[carte.card_id]
    // Le nom peut manquer d'une vieille sauvegarde : l'identifiant vaut mieux
    // qu'une phrase trouée.
    if (effet) return { cardId: carte.card_id, nom: carte.name || carte.card_id, effet }
  }
  return undefined
}

/** L'ambiance DOMINANTE, celle peinte en premier. */
export function meteoDuMonde(world: World | undefined): string {
  return meteosDuMonde(world)[0] ?? ''
}

/** Les effets qui EFFACENT la couleur du plateau. Sous eux, la couleur du
 *  cadre d'une carte ne dit plus son aspect, et le plateau doit la redonner
 *  autrement. Seul le noir et blanc en fait partie : le sepia teinte mais
 *  laisse les teintes distinctes les unes des autres. */
export const EFFETS_DELAVANTS: readonly string[] = ['noir']

/** Les effets réellement affichés, aperçu et interrupteur compris. */
export function effetsAffiches(
  world: World | undefined,
  active: boolean,
  apercu?: ApercuMeteo
): string[] {
  if (apercu !== undefined) return [...apercu]
  return active ? meteosDuMonde(world) : []
}

export function CoucheMeteo({
  world,
  active,
  apercu,
}: {
  world: World | undefined
  active: boolean
  /** Force ces effets, quelles que soient les cartes. Voir ApercuMeteo. */
  apercu?: ApercuMeteo
}) {
  const duJeu = useMemo(() => meteosDuMonde(world), [world])
  // L'apercu est une demande EXPLICITE : il passe outre l'interrupteur. Sans
  // ca, choisir un apercu alors que l'ambiance est coupee n'affiche rien et
  // l'outil parait casse. L'interrupteur ne commande que l'ambiance du jeu.
  const meteos = apercu !== undefined ? apercu : active ? duJeu : []
  if (meteos.length === 0) return null
  return (
    <>
      {meteos.map((meteo) => (
        <iframe
          key={meteo}
          className={`couche-meteo couche-meteo--${meteo}`}
          src={`/effects/weather/${meteo}.html`}
          title=""
          aria-hidden="true"
          tabIndex={-1}
        />
      ))}
    </>
  )
}

/**
 * Les lignes du panneau Options qui dependent de l'apercu d'ambiance
 * (« Aperçu d’ambiance » et ses pastilles, « Demande d’ambiance ») : extraites
 * de PanneauOptions (board.tsx) pour vivre a cote du reste du domaine ambiance
 * et pouvoir etre testees seules : board.tsx se monte lui-meme sur #plateau
 * des son import et ne peut pas etre importe tel quel dans un test.
 *
 * Grisees et inertes tant que « Ambiance » (meteo) est coupee : un apercu ou
 * une reponse figes n'ont plus de sens quand l'ambiance elle-meme est coupee
 * (voir `basculerAmbiance` ci-dessus, qui remet deja l'apercu sur Auto au
 * moment de la coupure ; cette ligne grisee dit au joueur pourquoi les
 * pastilles ne repondent plus).
 */
export function ReglagesApercuAmbiance({
  meteo,
  apercuMeteo,
  reglerApercuMeteo,
  reponseAmbiance,
  cyclerReponseAmbiance,
}: {
  meteo: boolean
  apercuMeteo: ApercuMeteo
  reglerApercuMeteo: (valeur: ApercuMeteo) => void
  reponseAmbiance: ReponseAmbiance
  cyclerReponseAmbiance: () => void
}) {
  return (
    <>
      {/* L'apercu n'est pas un interrupteur mais un ETABLI : les ambiances se
          superposant en jeu, il faut pouvoir en essayer plusieurs a la fois.
          D'ou des pastilles a cocher plutot qu'un cycle, qui n'aurait jamais
          montre qu'un effet. */}
      <div className={`ligne-option est-etabli${meteo ? '' : ' est-desactive'}`}>
        <span className="ligne-option-libelle">{t('Aperçu d’ambiance')}</span>
        <span className="ligne-option-etat" aria-hidden="true">
          {meteo ? t(libelleApercu(apercuMeteo)) : t('Ambiance coupée')}
        </span>
      </div>
      <div
        className={`apercu-pastilles${meteo ? '' : ' est-desactive'}`}
        role="group"
        aria-label={t('Aperçu d’ambiance')}
        title={
          meteo
            ? t('Force ces effets à l écran pour les voir, sans partie ni carte')
            : t('Ambiance coupée')
        }
      >
        <button
          type="button"
          className={`pastille${apercuMeteo === undefined ? ' est-actif' : ''}`}
          onClick={() => reglerApercuMeteo(undefined)}
          disabled={!meteo}
        >
          {t('Auto')}
        </button>
        <button
          type="button"
          className={`pastille${apercuMeteo?.length === 0 ? ' est-actif' : ''}`}
          onClick={() => reglerApercuMeteo([])}
          disabled={!meteo}
        >
          {t('Aucun')}
        </button>
        {EFFETS_METEO.map((effet) => {
          const choisi = apercuMeteo?.includes(effet) ?? false
          return (
            <button
              key={effet}
              type="button"
              className={`pastille${choisi ? ' est-actif' : ''}`}
              aria-pressed={choisi}
              disabled={!meteo}
              onClick={() =>
                reglerApercuMeteo(
                  choisi ? (apercuMeteo ?? []).filter((e) => e !== effet) : [...(apercuMeteo ?? []), effet]
                )
              }
            >
              {t(LIBELLE_EFFET[effet])}
            </button>
          )
        })}
      </div>
      {/* Le garde-fou de la modale d'ambiance : sans cette ligne, une case
          « ne plus me montrer ca » cochee par erreur serait definitive. Un
          cycle plutot qu'un simple bouton « redemander », parce que les trois
          etats sont utiles a qui sait ce qu'il veut. Grisee et inerte tant
          que « Ambiance » est coupee : demander si on garde une ambiance n'a
          pas de sens quand l'ambiance elle-meme est coupee. */}
      <button
        type="button"
        className={`ligne-option${meteo ? '' : ' est-desactive'}`}
        onClick={cyclerReponseAmbiance}
        disabled={!meteo}
        title={
          meteo
            ? t('Quand une carte allume une ambiance : poser la question, la garder sans demander, ou la couper sans demander')
            : t('Ambiance coupée')
        }
      >
        <span className="ligne-option-libelle">{t('Demande d’ambiance')}</span>
        <span className="ligne-option-etat" aria-hidden="true">
          {meteo
            ? reponseAmbiance === 'demander'
              ? t('Demander')
              : reponseAmbiance === 'toujours'
                ? t('Toujours')
                : t('Jamais')
            : t('Ambiance coupée')}
        </span>
      </button>
    </>
  )
}

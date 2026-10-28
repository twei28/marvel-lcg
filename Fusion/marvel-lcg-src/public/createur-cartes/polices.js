// Les polices du gabarit. Les noms de famille sont ceux des mesures (`types.json` -> `style.fontFamily`) : on les declare
// tels quels, avec les memes graisses, pour que le canvas choisisse la meme face que la carte de reference.
//
// ChampionsIcons : les icones du jeu sont des LETTRES de cette police (voir ICONES).

const FACES = [
  ['TextbookNewExtraBold', 'TextbookNewW08-ExtraBold.ttf', {}],
  ['ancbi', 'AvenirNextCondensed-BoldItalic.ttf', {}],
  ['AvenirNextCondMed', 'Avenir Next Condensed Medium.ttf', { weight: '400' }],
  ['ElektraMed', 'ElektraMedProMod-BoldItalic-mod.ttf', { weight: 'bold', style: 'italic' }],
  ['Exo2Mod', 'Exo2Mod-Bold.ttf', { weight: 'bold' }],
  ['AvenirNext', 'AvenirNextLTPro-It.otf', { style: 'italic' }],
  ['AvenirNext', 'AvenirNextLTPro-Bold.otf', { weight: 'bold' }],
  ['HorribleJefe', 'Horrible-Jefe.ttf', {}],
  ['AvenirNext', 'AvenirNextLTPro-BoldItalic.otf', { weight: 'bold', style: 'italic' }],
  ['AvenirNext', 'AvenirNextLTPro-Regular.otf', { weight: 'normal' }],
  ['AvenirNext', 'AvenirNextLTPro-Demi.otf', { weight: '500' }],
  ['ChampionsIcons', 'ChampionsIcons.ttf', {}],
  ['KomikaTitle', 'KomikaTitle.ttf', {}],
  ['KomikaText', 'KOMTXT_.ttf', {}],
  ['KomikaText', 'KOMTXTI.ttf', { style: 'italic' }],
  ['FigginsExtraBold', 'figgins-extrabold.otf', {}],
  ['FuturaMedCond', 'FUTURAMC.TTF', {}],
  ['FuturaExtraBold', 'Futura Extra Bold.otf', {}],
]

/** Les icones : nom -> lettre de ChampionsIcons. Les noms entre crochets [energy] viennent des textes du jeu. */
export const ICONES = {
  acceleration: 'a', boost: 'b', crisis: 'c', crise: 'c', consequential: 'd', energy: 'e', energie: 'e', amplify: 'f', per_hero: 'g',
  per_player: 'g', per_group: 't', hazard: 'h', danger: 'h', artist: 'i', mental: 'm', infinity: 'n', physical: 'p', physique: 'p',
  star: 's', boost_star: 's', unique: 'u', wild: 'w', joker: 'w',
}

let chargees = null

/** Charge toutes les polices une fois (promesse partagee). */
export function chargerPolices(dossier = 'polices/') {
  if (!chargees) {
    chargees = Promise.all(
      FACES.map(async ([famille, fichier, d]) => {
        try {
          const face = new FontFace(famille, `url("${dossier + encodeURI(fichier)}")`, { weight: d.weight, style: d.style })
          await face.load()
          document.fonts.add(face)
        } catch (e) {
          console.warn('police introuvable :', fichier, e)
        }
      })
    ).then(() => document.fonts.ready)
  }
  return chargees
}

// errata-rrg.ts — les ERRATA OFFICIELS (Marvel Champions Rules Reference 1.8, Annexe V) posés sur les cartes.
//
// Le scan d'une carte officielle garde l'ANCIEN texte imprimé, même quand `cards.json` est corrigé : le plateau pose donc
// le texte à jour par-dessus (voile, comme la traduction : TraductionPosee) et une pastille « Errata » en bas de la carte
// agrandie. Source des 87 entrées : A créer/errata-rrg/AUDIT-ERRATA.md (81 cartes ; les 6 corrections du livret de règles
// ne portent sur aucune carte).
//
//  - `en` / `fr` : le texte COMPLET corrigé de la zone de texte (même mise en forme que `cards.json`), `null` quand
//    l'errata ne touche ni le texte ni les traits (titre, icône, classification) : pastille seule, sans voile ;
//  - `resumeEn` / `resumeFr` : ce qui a changé, dit dans la bulle de la pastille ;
//  - `source` : la première version du Rules Reference qui porte l'errata ('1.7' = déjà là en 1.7, '1.8' = nouveau ou
//    modifié en 1.8). La bulle cite la version.
//
// ⚠ ÉDITÉ À LA MAIN. Un nouvel errata s'ajoute ici (texte EN complet, texte FR complet, résumé EN et FR), puis
// `errata-rrg.test.ts` vérifie que la carte existe dans cards.json et que les deux textes sont renseignés.
import { codeCarteConnu } from './marvelcdb'

export type ErratumRrg = {
  source: '1.7' | '1.8'
  en: string | null
  fr: string | null
  resumeEn: string
  resumeFr: string
}

const ERRATA: Readonly<Record<string, ErratumRrg>> = {
  '01026': {
    source: '1.7',
    en: "<b>Alter-Ego Action</b>: Exhaust Superhuman Law Division and spend a [mental] resource → remove 2 threat from a scheme.",
    fr: "<b>Action d'alter ego</b> : inclinez le département Judiciaire des Surhumains et dépensez une ressource [mental] → retirez 2 menaces d'une manigance.",
    resumeEn: "Removed “(thwart)” label.",
    resumeFr: "Retrait de l'étiquette « (contre) ».",
  },
  '01029a': {
    source: '1.8',
    en: "You get +1 hand size for each [[Tech]] upgrade you control (to a maximum of +6 hand size).",
    fr: "Votre taille de main augmente de +1 pour chaque amélioration [[TECH]] que vous contrôlez (jusqu'à +6 de taille de main maximum).",
    resumeEn: "Changed “(to a maximum hand size of 7)” to “(to a maximum of +6 hand size)”.",
    resumeFr: "« maximum de 7 » remplacé par « +6 de taille de main maximum ».",
  },
  '01183': {
    source: '1.7',
    en: "<b>When Revealed</b>: If M.O.D.O.K. is not in play, search the encounter deck and discard pile for M.O.D.O.K. and put him into play engaged with you, then shuffle the encounter deck.",
    fr: "<b>Une fois révélée</b> : si MODOK n'est pas en jeu, cherchez-le dans le deck rencontre ou la pile de défausse Rencontre et mettez-le en jeu engagé avec vous. Ensuite, mélangez le deck Rencontre.",
    resumeEn: "Added periods to “M.O.D.O.K.”",
    resumeFr: "Points ajoutés à « M.O.D.O.K. » (écriture anglaise).",
  },
  '01184': {
    source: '1.7',
    en: null,
    fr: null,
    resumeEn: "Added periods to card title.",
    resumeFr: "Titre : points ajoutés à « M.O.D.O.K. ».",
  },
  '03025': {
    source: '1.7',
    en: "Play only if your identity has the [[Avenger]] trait.\nAttach to a friendly character. Max 1 per character.\nAttached character gets +1 hit point and gains the [[Avenger]] trait.",
    fr: "Jouez cette carte uniquement si votre identité a le trait [[Avenger]].\nAttachez cette carte à un personnage ami.\n1 max par personnage.\nLe personnage attaché gagne +1 point de vie et le trait [[Avenger]].",
    resumeEn: "Added “Max 1 per character.”",
    resumeFr: "ajouté : « 1 max par personnage. »",
  },
  '03030': {
    source: '1.7',
    en: "<b>When Revealed</b>: Each [[Hydra]] minion engaged with a hero attacks that hero. Each player who was not attacked this way searches the encounter deck and discard pile for a [[Hydra]] minion and puts it into play engaged with them. Shuffle the encounter deck if it was searched.",
    fr: "<b>Une fois révélée</b> : chaque sbire [[Hydra]] engagé avec un héros attaque ce héros. Chaque joueur qui n'a pas été attaqué par cet effet cherche un sbire [[Hydra]] dans le deck de Rencontre et le met en jeu engagé avec lui. Mélangez le deck Rencontre s'il a été consulté.",
    resumeEn: "Changed the shuffle ability to only occur if the encounter deck is searched.",
    resumeFr: "Le deck Rencontre n'est mélangé que s'il a été consulté.",
  },
  '03032': {
    source: '1.7',
    en: "Attach to a side scheme. Max 1 per scheme.\n<b>Interrupt</b>: When attached scheme is defeated, deal 4 damage to an enemy.",
    fr: "Attachez cette carte à une manigance annexe.\n1 max par manigance.\n<b>Interruption</b> : quand la manigance attachée est déjouée, infligez 4 dégâts à un ennemi.",
    resumeEn: "Changed “Response” to “Interrupt”.",
    resumeFr: "« Réponse » devient « Interruption ».",
  },
  '04021': {
    source: '1.7',
    en: "If each of your allies has the [[Avenger]] trait, increase your ally limit by 1.\n<b>Action:</b> Exhaust Avengers Tower → reduce the cost of the next [[Avenger]] ally played this phase by 1.",
    fr: "Si chacun de vos alliés a le trait [[Avenger]], augmentez de 1 votre limite d'alliés.\n<b>Action</b> : inclinez la Tour des Avengers → réduisez de 1 le coût du prochain allié [[Avenger]] joué à cette phase.",
    resumeEn: "Should have the Avenger trait.",
    resumeFr: "La carte doit avoir le trait Avenger.",
  },
  '04028': {
    source: '1.8',
    en: "<b>When Revealed:</b> The Clint Barton player searches their hand, deck, discard pile, and play area for Mockingbird and tucks her faceup beneath this card. When this scheme is defeated, return the tucked Mockingbird to her owner's hand.",
    fr: "<b>Une fois révélée</b> : le joueur de Clint Barton cherche Mockingbird dans sa main, son deck, sa pile de défausse ou zone de jeu et la glisse, face visible, sous cette carte. Quand cette manigance est déjouée, renvoyez la Mockingbird glissée dans la main de son propriétaire.",
    resumeEn: "Changed “places” to “tucks” and “stage” to “scheme”. Added “the tucked”.",
    resumeFr: "« place » devient « glisse », « stade » devient « manigance », ajout de « glissée ».",
  },
  '04057': {
    source: '1.7',
    en: "<b>When Revealed</b>: Each [[Hydra]] minion engaged with a hero attacks that hero. Each player who was not attacked this way searches the encounter deck and discard pile for a [[Hydra]] minion and puts it into play engaged with them. Shuffle the encounter deck if it was searched.",
    fr: "<b>Une fois révélée</b> : chaque sbire [[HYDRA]] engagé avec un héros attaque ce héros. Chaque joueur qui n'a pas été attaqué par cet effet cherche un sbire [[HYDRA]] dans le deck Rencontre ou la pile de défausse Rencontre et le met en jeu engagé avec lui. Mélangez le deck Rencontre s'il a été consulté.",
    resumeEn: "Changed the shuffle ability to only occur if the encounter deck is searched.",
    resumeFr: "Le deck Rencontre n'est mélangé que s'il a été consulté.",
  },
  '04061a': {
    source: '1.7',
    en: "<b>Contents:</b> Crossbones (I) and Crossbones (II). Crossbones, Experimental Weapons, and Standard Encounter sets. Three modular sets <i>(Hydra Assault, Weapon Master, and Legions of Hydra)</i>.\n<b>Setup:</b> Create the Experimental Weapons deck and set it next to the main scheme deck. (See rulebook page 5.)",
    fr: "<b>Contenu</b> : Crossbones (I) et Crossbones (II). Les sets de rencontre Crossbones, Armes Expérimentales et Standard. Trois sets de rencontre modulaires <i>(Offensive d'Hydra, Maîtrise des Armes et Légions d'Hydra)</i>.\n<b>Mise en place</b> : Constituez le deck Armes Expérimentales et placez-le à côté du deck Manigance Principale. (Voir livret de règles, page 5.)",
    resumeEn: "Changed “Hydra Patrol” to “Hydra Assault”.",
    resumeFr: "« Hydra Patrol » devient « Hydra Assault » (texte anglais).",
  },
  '04128a': {
    source: '1.7',
    en: "<b>Contents:</b> Red Skull (I) and Red Skull (II). Red Skull and Standard encounter sets. Two modular encounter sets <i>(Hydra Assault and Hydra Patrol).</i>\n<b>Setup:</b> Put the Red House into play. Shuffle every other encounter side scheme into the side-scheme deck and set it next to the encounter deck (see insert).\nSet The Sleeper aside, out of play.",
    fr: "<b>Contenu</b> : Crâne Rouge (I) et Crâne Rouge (II). Les sets de Rencontre Crâne Rouge et Standard. Deux sets de rencontre modulaires <i>(Offensive d'Hydra et Patrouille d'Hydra).</i>\n<b>Mise en place</b> : mettez en jeu la Maison Rouge. Mélangez chaque autre manigance annexe de rencontre dans le deck Manigance Annexe et placez-le à côté du deck Rencontre <i>(voir livret de règles)</i>. Mettez de côté Le Dormeur, hors jeu.",
    resumeEn: "Added “encounter” before “side scheme”.",
    resumeFr: "Ajout de « de rencontre » après « manigance annexe ».",
  },
  '04135': {
    source: '1.7',
    en: "Incite 1.\nAttach to a side scheme.\n<b>Forced Interrupt:</b> When attached side scheme is defeated, deal the first player an encounter card.",
    fr: "Incitation 1.\nAttachez cette carte à une manigance annexe.\n<b>Interruption forcée</b> : quand la manigance attachée est déjouée, attribuez une carte Rencontre au premier joueur.",
    resumeEn: "Changed “Forced Response” to “Forced Interrupt”.",
    resumeFr: "« Réponse forcée » devient « Interruption forcée ».",
  },
  '04136': {
    source: '1.7',
    en: "<b>When Revealed:</b> For each side scheme in play, choose and exhaust a character you control.\n<hr />\n[star] <b>Boost</b>: Exhaust a character you control.",
    fr: "<b>Une fois révélée</b> : pour chaque manigance annexe en jeu, choisissez un personnage que vous contrôlez et inclinez-le.\n\n[star] <b>Boost</b>: inclinez un personnage que vous contrôlez.",
    resumeEn: "Revised wording to function as intended with updated “for each” rules.",
    resumeFr: "Formulation revue pour fonctionner avec la règle actuelle de « pour chaque ».",
  },
  '06006': {
    source: '1.7',
    en: "<b>Hero Action</b>: Spend X [energy] resources → deal X damage to the villain and each minion engaged with you. This damage ignores tough status cards if you have the [[Aerial]] trait.",
    fr: "<b>Action de héros</b> : dépensez X ressources [energy] → infligez X dégâts au méchant et à chaque sbire engagé avec vous. Ces dégâts ignorent les cartes d'état Tenace si vous avez le trait [[AÉRIEN]].",
    resumeEn: "Changed “attack” to “damage”.",
    resumeFr: "« Cette attaque » devient « Ces dégâts » : ce n'est pas une attaque.",
  },
  '06028': {
    source: '1.7',
    en: "<b>Forced Interrupt</b>: When Loki would be defeated, discard the top card of the encounter deck. If that card is a treachery, heal all damage from Loki instead.\n<i>(Thor's nemesis minion.)</i>",
    fr: "<b>Interruption forcée</b> : quand Loki est censé être vaincu, défaussez la carte du dessus du deck Rencontre. Si cette carte est une traîtrise, soignez tous les dégâts de Loki à la place.\n<i>(Sbire Némésis de Thor.)</i>",
    resumeEn: "Changed “Interrupt” to “Forced Interrupt”.",
    resumeFr: "« Interruption » devient « Interruption forcée ».",
  },
  '07014': {
    source: '1.7',
    en: "<b>When Revealed</b>: The active villain heals 3 hit points. Give that villain a tough status card.\n<hr />\n[star] <b>Boost</b>: Move the active counter to the villain with the least threat on his side scheme. That villain schemes.",
    fr: "<b>Une fois révélée</b> : le méchant actif se soigne de 3 dégâts. Donnez-lui une carte d'état Tenace.\n\n[star] <b>Boost</b>: déplacez le jeton Actif vers le méchant dont la manigance annexe a le moins de menaces. Ce dernier manigance.",
    resumeEn: "Changed “gains” to “heals”.",
    resumeFr: "« gagne » remplacé par « se soigne » (texte anglais).",
  },
  '08001a': {
    source: '1.7',
    en: "\"Widowmaker\" — <b>Response</b>: After you resolve the ability of a [[Preparation]] card you control, deal 1 damage to an enemy.",
    fr: "\"Faiseuse de veuves\" — <b>Réponse</b> : après avoir résolu la capacité d'une carte [[Préparation]] que vous contrôlez, infligez 1 dégât à un ennemi.",
    resumeEn: "Changed “trigger” to “resolve”.",
    resumeFr: "« déclencher » devient « résoudre ».",
  },
  '08009': {
    source: '1.8',
    en: "Black Widow gets +1 DEF.\n<b>Hero Response</b>: After you resolve the ability of a [[Preparation]] card you control, exhaust Synth-Suit → ready Black Widow.",
    fr: "Black Widow gagne +1 DEF.\n<b>Réponse de héros</b> : après avoir résolu la capacité d'une carte [[Préparation]] que vous contrôlez, inclinez le Costume Synthétique → redressez Black Widow.",
    resumeEn: "Changed “trigger” to “resolve”.",
    resumeFr: "« déclencher » devient « résoudre ».",
  },
  '09014': {
    source: '1.7',
    en: "Iron Fist enters play with 2 mystic counters on him.\n<b>Interrupt</b>: When Iron Fist attacks an enemy, remove 1 mystic counter from him → stun that enemy and deal 1 damage to it.",
    fr: "Iron Fist entre en jeu avec 2 jetons Mystique sur lui.\n<b>Interruption</b> : quand Iron Fist attaque un ennemi, retirez-lui 1 jeton Mystique → sonnez cet ennemi et infligez-lui 1 dégât.",
    resumeEn: "Changed “Response” to “Interrupt”.",
    resumeFr: "« Réponse » devient « Interruption ».",
  },
  '09021': {
    source: '1.7',
    en: "<b>Interrupt</b>: When a hero would take any amount of damage, reduce that amount by 1.",
    fr: "<b>Interruption</b> : quand un héros est censé subir n'importe quelle quantité de dégâts, diminuez de 1 cette quantité.",
    resumeEn: "Removed “(defense)” and the Defense trait.",
    resumeFr: "Retrait de « (défense) » et du trait Défense.",
  },
  '10025': {
    source: '1.7',
    en: "<b><i>Give to the Bruce Banner player.</i></b>\nChange form <i>(flip your identity)</i>.\n• If you are Bruce Banner, discard 2 cards from your hand. Discard this obligation.\n• If you are Hulk, exhaust your hero. Discard this obligation.",
    fr: "<b><i>Donnez cette carte au joueur de Bruce Banner.</i></b>\nChangez de forme <i>(retournez votre identité)</i>.\n• Si vous êtes Bruce Banner, défaussez 2 cartes de votre main. Défaussez cette obligation.\n• Si vous êtes Hulk, inclinez votre héros. Défaussez cette obligation.",
    resumeEn: "Removed “Then:”.",
    resumeFr: "Retrait de « Ensuite : ».",
  },
  '13028': {
    source: '1.7',
    en: "Guard.\n<b>Forced Interrupt</b>: When Beetle is defeated, the defeating player chooses to either spend a [physical] resource or shuffle Beetle into the encounter deck.\n<i>(Wasp's nemesis minion.)</i>",
    fr: "Garde.\n<b>Interruption forcée</b> : quand Le Scarabée est vaincu, le joueur qui l'a vaincu choisit : soit il dépense une ressource [physical], soit il mélange Le Scarabée dans le deck Rencontre.\n<i>(Sbire Némésis de La Guêpe.)</i>",
    resumeEn: "Specified which player should resolve the ability.",
    resumeFr: "Précision : c'est le joueur qui a vaincu Le Scarabée qui résout la capacité.",
  },
  '16123': {
    source: '1.7',
    en: "Attach to your identity.\nAttached character gets -1 THW, -1 ATK, and -1 DEF.\n<b>Hero Action:</b> Take 1 damage and spend [mental][mental] resources &#8594; discard this card. Any player can do this.",
    fr: "Attachez cette carte à votre identité.\nLe personnage attaché perd -1 CTR, -1 ATQ et -1 DEF.\n<b>Action de héros</b> : subissez 1 dégât et dépensez les ressources suivantes : [mental][mental] → défaussez cette carte. N'importe quel joueur peut le faire.",
    resumeEn: "Changed reminder text to rules text.",
    resumeFr: "Le rappel entre parenthèses devient une règle.",
  },
  '16125': {
    source: '1.7',
    en: "Attach to your identity.\n<b>Forced Interrupt:</b> When your turn begins, place 1 poison counter here, the take 1 damage for each poison counter here.\n<b>Hero Action:</b> Spend 3 resources of different types &#8594; discard this card. Any player can do this.",
    fr: "Attachez cette carte à votre identité.\n<b>Interruption forcée</b> : quand votre tour commence, placez 1 jeton Poison sur cette carte. Ensuite, subissez 1 dégât pour chaque jeton Poison sur cette carte.\n<b>Action de héros</b> : dépensez 3 ressources de différents types → défaussez cette carte. N'importe quel joueur peut le faire.",
    resumeEn: "Changed reminder text to rules text.",
    resumeFr: "Le rappel entre parenthèses devient une règle.",
  },
  '17020': {
    source: '1.7',
    en: "<b>Interrupt</b>: When Cosmo attacks or thwarts, name a card type, then discard the top card of a player deck or the encounter deck. If that card is of the named type, Cosmo does not take consequential damage for this use.",
    fr: "<b>Interruption</b> : quand Cosmo attaque ou contre, nommez un type de carte, ensuite, défaussez la carte du dessus d'un deck de joueur ou du deck Rencontre. Si cette carte est du type nommé, Cosmo ne subit pas de dégâts consécutifs pour cette utilisation.",
    resumeEn: "Changed “a deck” to “a player deck or the encounter deck”. Removed reminder text.",
    resumeFr: "« un deck » devient « un deck de joueur ou le deck Rencontre » ; retrait du rappel.",
  },
  '21116': {
    source: '1.7',
    en: "Hinder 1[per_hero]. Victory 1.\nThanos cannot take damage from player cards.<b> When Defeated:</b> Each player may spend up to 3 [physical] resources from their hand. Deal 2 damage to Thanos for each [physical] resource spent this way. This damage ignores the tough status card.",
    fr: "Entrave 1[per_hero]. Victoire 1.\nThanos ne peut pas subir de dégâts de la part des cartes de joueur.\n<b>Une fois déjouée</b> : chaque joueur peut dépenser jusqu'à 3 ressources [physical] de sa main. Infligez 2 dégâts à Thanos pour chaque ressource [physical] ainsi dépensée. Ces dégâts ignorent la carte d'état Tenace.",
    resumeEn: "Added “from player cards”.",
    resumeFr: "Ajout de « de la part des cartes de joueur ».",
  },
  '21129': {
    source: '1.7',
    en: "Permanent. Setup.\nAttach to the villain.\n[star] <b>Forced Response</b>: After attached villain activates against you, resolve the <b> Special </b> ability of each [[infinity stone]] in play. Otherwise, put the top card of the [[infinity stone]] deck into play.",
    fr: "Permanent. Mise en Place.\nAttachez cette carte au méchant.\n[star] <b>Réponse forcée</b> : après que le méchant attaché s'est activé contre vous, résolvez la capacité \"<b>Spécial</b>\" de chaque [[PIERRE D'INFINITÉ]] en jeu. Sinon, mettez en jeu la carte du dessus du deck [[PIERRE D'INFINITÉ]].",
    resumeEn: "Added “Attach to the villain” and “against you”.",
    resumeFr: "Ajout de « Attachez cette carte au méchant » et de « contre vous ».",
  },
  '21178': {
    source: '1.7',
    en: "Treat attached ally as an [[Enthralled]] minion with a blank text box. Attached minion's SCH is equal to its printed THW and it does not take consequential damage.\n<b>When Revealed</b>: Attach to the ally with the highest cost without Beguiled attached. Attached ally engages its controller. Otherwise, this card gains surge.",
    fr: "L'allié attaché est considéré comme un sbire [[ENVOUTÉ]] ayant une boîte de texte vide. La MNG du sbire attaché est égale à son CTR imprimé et il ne subit pas de dégâts consécutifs.\n<b>Une fois révélée</b> : attachez cette carte à l'allié ayant le coût le plus élevé et qui n'a pas déjà une carte Ensorcelé attachée. L'allié attaché engage son contrôleur. Sinon, cette carte gagne Renfort.",
    resumeEn: "Should have the Condition trait.",
    resumeFr: "La carte doit avoir le trait Condition.",
  },
  '22011': {
    source: '1.7',
    en: "<b>Response:</b> After you play Eros from your hand, for each [mental] resource you used to pay for him, choose a minion and confuse it.",
    fr: "<b>Réponse</b> : après avoir joué Eros de votre main, pour chaque ressource [mental] que vous avez utilisée pour le payer, choisissez un sbire et désorientez-le.",
    resumeEn: "Revised wording to function as intended with updated “for each” rules.",
    resumeFr: "Formulation revue pour fonctionner avec la règle actuelle de « pour chaque ».",
  },
  '22031': {
    source: '1.7',
    en: "<b>When Revealed:</b> Gamora attacks you. If the Gamora hero or ally is in play, she attacks you (resolve her ATK against you without exhausting her). If no attack was made this way, this card gains surge.",
    fr: "<b>Une fois révélée</b> : Gamora vous attaque. Si la carte Allié ou Héros Gamora est en jeu, elle vous attaque (résolvez son ATQ contre vous sans l'incliner). Si aucune attaque n'est effectuée par cet effet, cette carte gagne Renfort.",
    resumeEn: "Changed reminder text to rules text to function with the updated rules on referential abilities.",
    resumeFr: "Le rappel entre parenthèses devient une règle.",
  },
  '23001b': {
    source: '1.7',
    en: "<b>Action</b>: Choose a War Machine card in your discard pile and shuffle it into your deck. (Limit once per phase.)\n<b>Forced Response</b>: After you change to this form, discard each ammo counter from your identity.",
    fr: "<b>Action</b> : choisissez dans votre pile de défausse une carte du set de War Machine et mélangez-la dans votre deck. (Limite d'une fois par phase.)\n<b>Réponse forcée</b> : après être passé sous cette forme, défaussez chaque jeton Munition de votre identité.",
    resumeEn: "Added “(Limit once per phase.)”",
    resumeFr: "Ajout de « (Limite d'une fois par phase.) ».",
  },
  '25007': {
    source: '1.7',
    en: "You get +4 hit points and gain the [[aerial]] trait.",
    fr: "Vous gagnez +4 points de vie et le trait [[AÉRIEN]].",
    resumeEn: "Changed “Valkyrie” to “You”.",
    resumeFr: "« Valkyrie » devient « Vous ».",
  },
  '25011': {
    source: '1.7',
    en: "<b>Hero Interrupt</b> <i>(defense)</i>: When the enemy with Death-Glow attached attacks, declare Valkyrie the defender without exhausting her. She gets +2 DEF for this attack.",
    fr: "<b>Interruption de héros</b> <i>(défense)</i> : quand l'ennemi auquel l'Aura de la Mort est attachée attaque, déclarez Valkyrie comme défenseur sans l'incliner. Elle gagne +2 DEF pour cette attaque.",
    resumeEn: "Added “(defense)”.",
    resumeFr: "Ajout de « (défense) » et du trait Défense.",
  },
  '25031': {
    source: '1.7',
    en: "Treat attached ally as an [[Enthralled]] minion with a blank text box. Attached minion's SCH is equal to its printed THW and it does not take consequential damage.\n<b>When Revealed</b>: Attach to the ally with the highest cost without Beguiled attached. Attached ally engages its controller. Otherwise, this card gains surge.",
    fr: "L'allié attaché est considéré comme un sbire [[ENVOUTÉ]] ayant une boîte de texte vide. La MNG du sbire attaché est égale à son CTR imprimé et il ne subit pas de dégâts consécutifs.\n<b>Une fois révélée</b> : attachez cette carte à l'allié ayant le coût le plus élevé qui n'a pas déjà une carte Ensorcelé attachée. L'allié attaché engage son contrôleur. Sinon, cette carte gagne Renfort.",
    resumeEn: "Should have the Condition trait.",
    resumeFr: "La carte doit avoir le trait Condition.",
  },
  '26022': {
    source: '1.7',
    en: "<b>Interrupt:</b> When Machine Man attacks or thwarts, spend up to 3 resources of any type &#8594; Machine Man gets +1 THW and +1 ATK for this use for each resource spent this way.",
    fr: "<b>Interruption</b> : quand Machine Man attaque ou contre, dépensez jusqu'à 3 ressources de n'importe quel type → pour cette utilisation, Machine Man gagne +1 CTR et +1 ATQ pour chaque ressource ainsi dépensée.",
    resumeEn: "Added “for this use”.",
    resumeFr: "Ajout de « pour cette utilisation ».",
  },
  '27025': {
    source: '1.7',
    en: "<b>Give to the Gwen Stacy player.</b>\nSearch your deck, hand, discard pile, and play area for George Stacy and attach him facedown to this card.\n<b>Alter-Ego Action</b>: Exhaust Gwen Stacy and remove this obligation from the game → add George Stacy to your hand.",
    fr: "<b>Donnez cette carte au joueur de Gwen Stacy.</b>\nCherchez George Stacy dans votre deck, main, pile de défausse ou zone de jeu et attachez-le face cachée à cette carte.\n<b>Action d'alter ego</b> : inclinez Gwen Stacy et retirez cette obligation de la partie → ajoutez George Stacy à votre main.",
    resumeEn: "Attaches George Stacy to itself instead of setting him aside and attaching to him.",
    resumeFr: "George Stacy est attaché face cachée à cette obligation.",
  },
  '27073': {
    source: '1.7',
    en: "Toughness. (This character enters play with a tough status card.)\n<i>Vengeance</i> — <b>Forced Response</b>: After you or an ally you control attacks and damages Venom, place 1 facedown boost card on your identity.",
    fr: "Ténacité. <i>(Ce personnage entre en jeu avec une carte d'état Tenace.)</i>\n<i>Vengeance</i> — <b>Réponse forcée</b> : après que vous ou un allié que vous contrôlez a attaqué et blessé Venom, placez 1 carte de boost face cachée sur votre identité.",
    resumeEn: "Changed “you attack and damage Venom with a card you control” to “you or an ally you control attacks and damages Venom”.",
    resumeFr: "« vous attaquez et blessez Venom avec une carte que vous contrôlez » devient « vous ou un allié que vous contrôlez attaquez et blessez Venom ».",
  },
  '27074': {
    source: '1.7',
    en: "Toughness. Steady.\n<b>When Revealed</b>: Search the encounter deck and discard pile for the Tooth and Nail side scheme and put it into play. <i>(Shuffle.)</i>\n<i>Vengeance</i> — <b>Forced Response</b>: After you or an ally you control attacks and damages Venom, place 1 facedown boost card on your identity.",
    fr: "Ténacité. Solide.\n<b>Une fois révélée</b> : cherchez la manigance annexe Crocs et Griffes dans le deck Rencontre ou la pile de défausse du deck Rencontre et mettez-la en jeu. <i>(Mélangez le deck Rencontre.)</i>\n<i>Vengeance</i> — <b>Réponse forcée</b> : après que vous ou un allié que vous contrôlez a attaqué et blessé Venom, placez 1 carte de boost face cachée sur votre identité.",
    resumeEn: "Changed “you attack and damage Venom with a card you control” to “you or an ally you control attacks and damages Venom”.",
    resumeFr: "« vous attaquez et blessez Venom avec une carte que vous contrôlez » devient « vous ou un allié que vous contrôlez attaquez et blessez Venom ».",
  },
  '27075': {
    source: '1.7',
    en: "Retaliate 1. Steady. Toughness.\n<b>When Revealed</b>: Place 2 facedown boost cards on each identity.\n<i>Retribution</i> — <b>Forced Response</b>: After you or an ally you control attacks and damages Venom, place 1 facedown boost card on your identity (2 facedown boost cards instead if this is the first attack this turn).",
    fr: "Riposte 1. Ténacité. Solide.\n<b>Une fois révélée</b> : placez 2 cartes de boost sur votre identité.\n<i>Représailles</i> — <b>Réponse forcée</b> : après que vous ou un allié que vous contrôlez a attaqué et blessé Venom, placez 1 carte de boost face cachée sur votre identité. (2 à la place s'il s'agit de la première attaque de ce tour.)",
    resumeEn: "Changed “you attack and damage Venom with a card you control” to “you or an ally you control attacks and damages Venom”.",
    resumeFr: "« vous attaquez et blessez Venom avec une carte que vous contrôlez » devient « vous ou un allié que vous contrôlez attaquez et blessez Venom ».",
  },
  '27171': {
    source: '1.7',
    en: "Treat attached ally as a minion with a blank text box (except for [[traits]]). Attach minion's SCH is equal to its printed THW and it does not take consequential damage.\n<b>When Revealed</b>: Attach to the ally you control with the lowest cost. Attached ally engages its controller. Otherwise, this card gains surge.",
    fr: "L'allié attaché perd le texte imprimé dans sa boîte de texte <i>(sauf les [[TRAITS]])</i> et est considéré comme un sbire. La MNG du sbire attaché est égale à son CTR imprimé et il ne subit pas de dégâts consécutifs.\n<b>Une fois révélée</b> : attachez cette carte à l'allié que vous contrôlez ayant le coût le moins élevé. L'allié attaché engage son contrôleur. Sinon, cette carte gagne Renfort.",
    resumeEn: "Added “Attached ally engages its controller.”",
    resumeFr: "Ajout de « L'allié attaché engage son contrôleur ».",
  },
  '28002': {
    source: '1.7',
    en: "<b>Hero Response</b>: After you play an event, exhaust Ms. Marvel and deal 1 damage to her → return that event to your hand from your discard pile.",
    fr: "<b>Réponse de héros</b> : après avoir joué un événement, inclinez Miss Marvel et infligez-lui 1 dégât → renvoyez cet événement de votre pile de défausse dans votre main.",
    resumeEn: "Added “from your discard pile”.",
    resumeFr: "Ajout de « de votre pile de défausse ».",
  },
  '29025': {
    source: '1.7',
    en: "Max 1 per deck.\nPlay only if your identity has the [[Champion]] trait.\n<b>Hero Action</b>: Remove ‘Go for Champions!’ from the game &#8594; each [[champion]] character in play cannot take damage until the end of the round.",
    fr: "1 max par deck.\nJouez cette carte uniquement si votre identité a le trait [[CHAMPION]].\n<b>Action de héros</b> : retirez cette carte de la partie → jusqu'à la fin du round, aucun personnage [[CHAMPION]] en jeu ne peut subir de dégâts.",
    resumeEn: "Added “Remove ‘Go for Champions!’ from the game →”.",
    resumeFr: "Ajout de « Retirez cette carte de la partie → ».",
  },
  '31001b': {
    source: '1.7',
    en: "Permanent. This card's printed text box cannot be treated as if it were blank.\n<i>Return to Base</i> — <b>Forced Interrupt</b>: When you flip to this side, flip SP//dr to Peni Parker. Detach Peni Parker from here, moving all counters on this card and cards attached to this card to her.",
    fr: "Permanent. Cette carte ne peut pas perdre le texte imprimé dans sa boîte de texte.\n<i>Retour à la Base</i> — <b>Interruption forcée</b> : quand vous retournez cette carte sur cette face, retournez SP//dr sur sa face Peni Parker. Détachez Peni Parker de cette carte, en déplaçant sur elle tous les jetons de cette carte et toutes les cartes attachées à cette carte.",
    resumeEn: "Counters and attachments now move to Peni Parker, instead of the reverse.",
    resumeFr: "Les jetons et les attachements vont maintenant vers Peni Parker, et non l'inverse.",
  },
  '31027': {
    source: '1.7',
    en: "<b>Forced Response</b>: After the engaged player generates any number of resources, deal an equal amount of damage to that player’s hero.\n<i>(SP//dr's nemesis minion.)</i>",
    fr: "<b>Réponse forcée</b> : après que le joueur engagé a généré n'importe quel nombre de ressources, infligez une quantité équivalente de dégâts au héros de ce joueur.\n<i>(Sbire Némésis de SP//dr.)</i>",
    resumeEn: "Changed “engaged hero” to “engaged player” and “that hero” to “that player’s hero”.",
    resumeFr: "« héros engagé » devient « joueur engagé », « ce héros » devient « le héros de ce joueur ».",
  },
  '32008': {
    source: '1.7',
    en: "<b>Hero Action</b> <i>(attack)</i>: Deal 5 damage to an enemy. You may discard a tough status card from your hero to stun and confuse that enemy.",
    fr: "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Vous pouvez défausser une carte d'état Tenace de votre héros pour sonner et désorienter cet ennemi.",
    resumeEn: "Replaced cost arrow with “to”.",
    resumeFr: "La flèche de coût est remplacée par « pour ».",
  },
  '32010': {
    source: '1.7',
    en: "<b>Alter-Ego Interrupt</b>: When the villain would activate, change to hero form.",
    fr: "<b>Interruption d'alter ego</b> : quand le méchant est censé s'activer, passez en forme de héros.",
    resumeEn: "Added “would”.",
    resumeFr: "Ajout de « est censé ».",
  },
  '32088a': {
    source: '1.7',
    en: "<b>When Defeated</b>: The first player searches the encounter deck and discard pile for a [[Sentinel]] minion and reveals it. Flip this card and put Jubilee into play, discarding any other ally version of Jubilee from play.",
    fr: "<b>Une fois déjouée</b> : le premier joueur cherche un sbire [[SENTINELLE]] dans le deck Rencontre ou la pile de défausse Rencontre et le révèle. Retournez cette carte et mettez en jeu Jubilé, en défaussant toute autre version alliée de Jubilé qui serait en jeu.",
    resumeEn: "Added “ally”.",
    resumeFr: "Ajout de « alliée ».",
  },
  '32141b': {
    source: '1.7',
    en: "<b>Forced Response</b>: After you place a magnet counter on this scheme, if there are at least 3 magnet counters here, remove 3 of them and discard cards from the encounter deck until a [[Magnetic]] card is discarded. Reveal that card.",
    fr: "<b>Réponse forcée</b> : après avoir placé un jeton Aimant sur cette manigance, s'il y a au moins 3 jetons Aimant dessus, retirez 3 de ces jetons et défaussez des cartes du deck Rencontre jusqu'à ce qu'une carte [[MAGNÉTIQUE]] soit défaussée. Révélez cette carte.",
    resumeEn: "Magnet counters are now removed before the Magnetic card is revealed.",
    resumeFr: "Les 3 jetons Aimant sont maintenant retirés avant la révélation de la carte Magnétique.",
  },
  '32143b': {
    source: '1.7',
    en: "<b>Forced Response</b>: After you place a magnet counter on this scheme, if there are at least 3 magnet counters here, remove 3 of them and discard cards from the encounter deck until a [[Magnetic]] card is discarded. Reveal that card.",
    fr: "<b>Réponse forcée</b> : après avoir placé un jeton Aimant sur cette manigance, s'il y a au moins 3 jetons Aimant dessus, retirez 3 de ces jetons et défaussez des cartes du deck Rencontre jusqu'à ce qu'une carte [[MAGNÉTIQUE]] soit défaussée. Révélez cette carte.\n<b>Si ce stade est achevé, les joueurs perdent la partie.</b>",
    resumeEn: "Magnet counters are now removed before the Magnetic card is revealed.",
    resumeFr: "Les 3 jetons Aimant sont maintenant retirés avant la révélation de la carte Magnétique.",
  },
  '35001b': {
    source: '1.7',
    en: "<i>Snikt!</i> - <b>Setup</b>: Put Wolverine’s Claws into play.",
    fr: "<i>Tching !</i> — <b>Mise en place</b> : mettez en jeu les Griffes de Wolverine.",
    resumeEn: "Text rewritten: “Setup: Put Wolverine’s Claws into play.”",
    resumeFr: "Texte réécrit : « Mise en place : mettez en jeu les Griffes de Wolverine. »",
  },
  '35008': {
    source: '1.7',
    en: "<b>Hero Action</b> <i>(attack)</i>: Deal 4 damage to an enemy. If this attack defeats an enemy, you may take 2 damage to repeat this ability.",
    fr: "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Si un ennemi est vaincu par cette attaque, vous pouvez subir 2 dégâts pour répéter cette capacité.",
    resumeEn: "Replaced cost arrow with “to”.",
    resumeFr: "La flèche de coût est remplacée par « pour ».",
  },
  '36030': {
    source: '1.7',
    en: "<b><i>Give to the Ororo Munroe player.</i></b>\nFlip to alter-ego form. You cannot change to hero form.\n<b>Alter-Ego Action:</b> Exhaust Ororo Munroe &#8594; remove Claustrophobia from the game.",
    fr: "<b><i>Donnez cette carte au joueur d'Ororo Munroe.</i></b>\nPassez sous forme d'alter ego.\nVous ne pouvez pas passer sous forme de héros.\n<b>Action d'alter ego</b> : inclinez Ororo Munroe → retirez Claustrophobie de la partie.",
    resumeEn: "Changed “change forms” to “change to hero form”.",
    resumeFr: "« changer de forme » devient « passer sous forme de héros ».",
  },
  '36038': {
    source: '1.7',
    en: "Treat attached ally as a [[Controlled]] minion with a blank text box. Attached minion's SCH is equal to its printed THW and it does not take consequential damage.\n<b>When Revealed</b>: Attach to the ally with the lowest THW without Possessed attached. Attached ally engages its controller. If you cannot, this card gains surge.",
    fr: "Considérez l'allié attaché comme un sbire [[CONTRÔLÉ]] dont la boîte de texte est vide. Sa MNG est égale à son CTR imprimé et il ne subit pas de dégâts consécutifs.\n<b>Une fois révélée</b> : attachez cette carte à l'allié ayant le CTR le plus faible qui n'a pas d'exemplaire de Possédé attaché. L'allié attaché engage son contrôleur. Si vous ne pouvez pas, cette carte gagne Renfort.",
    resumeEn: "Added “Attached ally engages its controller.”",
    resumeFr: "Ajout de « L'allié attaché engage son contrôleur ».",
  },
  '37034': {
    source: '1.7',
    en: "Attach to a minion. Otherwise, Psionic Shield gains surge.\n<b>Forced Interrupt</b>: When attached minion would leave play, instead heal all damage from that minion. Then, discard this attachment.",
    fr: "Attachez cette carte à un sbire. Sinon, Bouclier Psionique gagne Renfort.\n<b>Interruption forcée</b> : quand le sbire attaché est censé quitter le jeu, soignez tous les dégâts de ce sbire à la place. Ensuite, défaussez cet attachement.",
    resumeEn: "Removed “and put it back into play”.",
    resumeFr: "Retrait de « et mettez-le de nouveau en jeu ».",
  },
  '38001a': {
    source: '1.7',
    en: "<i>Skin Contact</i> − <b>Action</b>: Find Touched and attach it to another character. You gain each of the attached character's [[TRAITS]] until the end of the round. (Limit once per round.)\n<b>Forced Response</b>: After the player phase begins, find Touched and set it aside.",
    fr: "<i>Contact Cutané</i> — <b>Action</b> : trouvez Touché et attachez-le à un autre personnage. Vous gagnez tous les [[TRAITS]] du personnage attaché jusqu'à la fin du round. (Limite d'une fois par round.)\n<b>Réponse forcée</b> : après le début de la phase des Joueurs, trouvez et mettez de côté Touché.",
    resumeEn: "Changed “Attach Touched...” to “Find Touched and attach it...”.",
    resumeFr: "« Attachez Touché… » devient « Trouvez Touché et attachez-le… ».",
  },
  '38001b': {
    source: '1.7',
    en: "<b>Setup</b>: Find your Touched upgrade and set it aside.\n<i>Withdrawn</i> − <b>Forced Response</b>: After you change to this form, find Touched and set it aside.",
    fr: "<b>Mise en place</b> : trouvez votre amélioration Touché et mettez-la de côté.\n<i>Retrait</i> — <b>Réponse forcée</b> : après être passé sous cette forme, trouvez Touché et mettez-le de côté.",
    resumeEn: "Now specifies to “find” Touched and set it aside.",
    resumeFr: "Précision : on « trouve » Touché avant de le mettre de côté.",
  },
  '38007': {
    source: '1.7',
    en: "<b>Hero Action</b>: Find Touched and attach it to a character other than Rogue and deal 2 damage to that character → heal 2 damage from Rogue and ready her. You gain each of the attached character's [[TRAITS]] until the end of the round.",
    fr: "<b>Action de héros</b> : trouvez Touché et attachez-le à un personnage autre que Malicia et infligez 2 dégâts à ce personnage → soignez Malicia de 2 dégâts et redressez-la. Vous gagnez tous les [[TRAITS]] du personnage attaché jusqu'à la fin du round.",
    resumeEn: "Changed “Attach Touched...” to “Find Touched and attach it...”.",
    resumeFr: "« Attachez Touché… » devient « Trouvez Touché et attachez-le… ».",
  },
  '38026': {
    source: '1.7',
    en: "<b>When Defeated</b>: The defeating player searches the encounter deck and discard pile for a copy of the Misled treachery and shuffles it into their deck.",
    fr: "<b>Une fois déjouée</b> : le joueur qui l'a vaincu cherche un exemplaire de la traîtrise Induite en Erreur dans le deck Rencontre ou la pile de défausse Rencontre, et le mélange dans son deck.",
    resumeEn: "Specified who should resolve the ability.",
    resumeFr: "Précision : c'est le joueur qui a vaincu le sbire qui résout la capacité.",
  },
  '38031': {
    source: '1.7',
    en: "Teamwork ([[REAVER]]). Toughness.\n<b>Forced Response</b>: After Bonebreaker engages you, take 1 indirect damage for each [[REAVER]] minion engaged with you.",
    fr: "Collaboration ([[REAVER]]). Ténacité.\n<b>Réponse forcée</b> : après que Bonebreaker vous a engagé, subissez 1 dégât indirect pour chaque sbire [[REAVER]] engagé avec vous.",
    resumeEn: "Changed “Forced Interrupt” to “Forced Response”.",
    resumeFr: "« Interruption forcée » devient « Réponse forcée ».",
  },
  '39016': {
    source: '1.7',
    en: "Permanent.\n<b>Forced Response</b>: After the last threat is removed from here, the player who removed that threat reveals the top card of the show deck and places 3[per_hero] threat here.\n<b>Hero Action</b>: Take 2 damage &#8594; remove 3 threat from here.",
    fr: "Permanent.\n<b>Réponse forcée</b> : après que la dernière menace a été retirée de cette manigance, le joueur qui l'a retirée révèle la carte du dessus du deck Spectacle et place 3[per_hero] menaces sur À La Recherche de Spirale.\n<b>Action de héros</b> : subissez 2 dégâts → retirez 3 menaces de cette manigance.",
    resumeEn: "Added cost arrow.",
    resumeFr: "Ajout de la flèche de coût.",
  },
  '39045': {
    source: '1.7',
    en: "Surge.\n<b>When Defeated</b>: In player order, each player may search their deck for a card and play that card, ignoring its resource cost. <i>(Shuffle.)</i>\n[star] <b>Boost</b>: Put this card into play.",
    fr: "Renfort.\n<b>Une fois vaincu</b> : dans l'ordre des joueurs, chaque joueur peut chercher une carte dans son deck et la jouer sans tenir compte de son coût en ressources. <i>(Mélangez.)</i>\n\n[star] <b>Boost</b>: mettez cette carte en jeu.",
    resumeEn: "Replaced “for free” with “ignoring its resource cost”.",
    resumeFr: "« gratuitement » devient « sans tenir compte de son coût en ressources ».",
  },
  '40092': {
    source: '1.7',
    en: "Attach to your identity.\nTreat your identity's printed text box as if it were blank <i>(except for traits)</i>.\n<b>Action</b>: Choose to either exhaust a character you control or take 3 damage → discard this card. Any player can do this.",
    fr: "Attachez cette carte à votre identité.\nVotre identité perd le texte imprimé dans sa boîte de texte <i>(sauf les [[TRAITS]])</i>.\n<b>Action</b> : choisissez : soit vous inclinez un personnage que vous contrôlez, soit vous subissez 3 dégâts → défaussez cette carte. N'importe quel joueur peut utiliser cette capacité.",
    resumeEn: "Changed reminder text to rules text.",
    resumeFr: "Le rappel entre parenthèses devient une règle.",
  },
  '43036': {
    source: '1.7',
    en: "Linked (Specialized Training).\nYour identity gets +4 hit points.\n<b>Response</b>: After your identity takes damage from an enemy attack, exhaust this card &#8594; draw 1 card.",
    fr: "Liée (Entraînement Spécialisé).\nVotre identité gagne +4 points de vie.\n<b>Réponse de héros</b> : après que votre héros a subi des dégâts d'une attaque ennemie, inclinez cette amélioration → piochez 1 carte.",
    resumeEn: "Changed “hero” to “identity”.",
    resumeFr: "« héros » devient « identité ».",
  },
  '44041': {
    source: '1.7',
    en: "Treat attached ally as a [['POOL]] minion with a blank text box. Attached minion's SCH is equal to its printed THW and it does not take consequential damage.\n<b>When Revealed</b>: Attach to the ally with the highest cost without 'Pool-ized attached. Attached ally engages its controller. Otherwise, this card gains surge.",
    fr: "L'allié attaché est considéré comme un sbire [['POOL]] ayant une boîte de texte vide. La MNG du sbire attaché est égale à son CTR imprimé et il ne subit pas de dégâts consécutifs.\n<b>Une fois révélée</b> : attachez cette carte à l'allié ayant le coût le plus élevé et qui n'a pas déjà une 'Poolisation attachée. L'allié attaché engage son contrôleur. Sinon, cette carte gagne Renfort.",
    resumeEn: "Added “Attached ally engages its controller.”",
    resumeFr: "Ajout de « L'allié attaché engage son contrôleur ».",
  },
  '45017': {
    source: '1.7',
    en: "<b>Alter-Ego Action</b>: Search your deck and discard pile for an ally and an upgrade that can be attached to an ally. Add them to your hand. <i>(Shuffle.)</i>",
    fr: "<b>Action d'alter ego</b> : cherchez dans votre deck et pile de défausse un allié et une amélioration pouvant être attachée à un allié. Ajoutez-les à votre main. <i>(Mélangez.)</i>",
    resumeEn: "Changed “can be attached to that ally” to “can be attached to an ally”.",
    resumeFr: "« attachée à cet allié » devient « attachée à un allié ».",
  },
  '45171a': {
    source: '1.7',
    en: "Mission Team cannot be discarded and the first player gains control of it.\n<b>Action</b>: Exhaust Mission Team → choose:\n• Reduce the cost of the next ally played to the mission this phase by 2.\n• Make a mission attempt.",
    fr: "Équipe de Mission ne peut pas être défaussée et le premier joueur en gagne le contrôle.\n<b>Action</b> : inclinez Équipe de Mission → choisissez :\n- Réduisez de 2 le coût du prochain allié joué dans la zone de mission pendant cette phase.\n- Effectuez une tentative de mission.",
    resumeEn: "Added “this phase” to the first bullet.",
    resumeFr: "Ajout de « pendant cette phase » dans la première puce.",
  },
  '48012': {
    source: '1.7',
    en: "<b>Action</b>: Deal 1 damage to another friendly character → until the end of the round, Rogue gains each of that character's [[Traits]] and adds that character's base THW and ATK to her matching powers. (Limit once per round.)",
    fr: "<b>Action</b> : infligez 1 dégât à un autre personnage ami → jusqu'à la fin du round, Malicia gagne tous les [[TRAITS]] de ce personnage et ajoute la CTR et l'ATQ de base de ce personnage à ses pouvoirs correspondants. (Limite d'une fois par round.)",
    resumeEn: "Changed “printed” to “base”.",
    resumeFr: "« imprimés » devient « de base ».",
  },
  '48037': {
    source: '1.7',
    en: null,
    fr: null,
    resumeEn: "Removed the star icon from this card’s boost field.",
    resumeFr: "L'icône ★ est retirée du champ Boost.",
  },
  '49010': {
    source: '1.7',
    en: "<b>Hero Action</b>: Discard a minion with Wrapped in Metal attached. Then, deal 5 damage to an enemy and stun it.",
    fr: "<b>Action de héros</b> : défaussez un sbire auquel est attaché Enveloppé de Métal. Puis, infligez 5 dégâts à un ennemi et sonnez-le.",
    resumeEn: "Changed cost arrow to “Then”.",
    resumeFr: "La flèche de coût devient « Puis ».",
  },
  '49023': {
    source: '1.7',
    en: null,
    fr: null,
    resumeEn: "Classification should be “Basic” instead of “Protection”.",
    resumeFr: "Classification : Basic (et non Protection).",
  },
  '49028': {
    source: '1.7',
    en: "Steady. Toughness. Villainous.\n[star] <b>Forced Response</b>: After Exodus attacks you, discard cards from the top of your deck equal to his total ATK for that attack.\n<i>(Magneto's nemesis minion.)</i>",
    fr: "Solide. Ténacité. Vilenie.\n[star] <b>Réponse forcée</b> : après qu'Exodus vous a attaqué, défaussez un nombre de cartes du dessus de votre deck égal à son total d'ATQ pour cette attaque.\n(<i>Sbire Némésis de Magnéto.</i>)",
    resumeEn: "Added “for that attack”.",
    resumeFr: "Ajout de « pour cette attaque ».",
  },
  '50153': {
    source: '1.7',
    en: null,
    fr: null,
    resumeEn: "The “SCH” modifier should be a “THW” modifier.",
    resumeFr: "Le modificateur « MNG » devient un modificateur « CTR ».",
  },
  '50156': {
    source: '1.7',
    en: "Villainous. Victory 1.\n[star] Each character without the [[Aerial]] trait cannot defend against MACH-IV's attacks.",
    fr: "Vilenie. Victoire 1.\n[star] Chaque personnage sans le trait [[Aérien]] ne peut pas se défendre contre les attaques de MACH‑IV.",
    resumeEn: "Changed “make basic defenses” to “defend”.",
    resumeFr: "« effectuer de défense de base » devient « se défendre ».",
  },
  '52008': {
    source: '1.7',
    en: "<b>Interrupt</b>: When you reveal a card from the same encounter set as a card tucked under your identity, exhaust Eidetic Memory → swap those cards. Reveal the card that had been tucked under your identity instead.",
    fr: "<b>Interruption</b> : quand vous révélez une carte appartenant au même set de rencontre qu'une carte intercalée sous votre identité, inclinez Mémoire Eidétique → échangez ces cartes. Révélez la carte qui était intercalée sous votre identité à la place.",
    resumeEn: "Changed “Silk” to “your identity”.",
    resumeFr: "« Silk » devient « votre identité ».",
  },
  '54033': {
    source: '1.7',
    en: "Play only if your identity has the [[S.H.I.E.L.D.]] trait.\nAttach to a friendly character. Max 1 per character.\nAttached character gets +1 hit point and gains the [[S.H.I.E.L.D.]] trait.",
    fr: "Jouez cette carte uniquement si votre identité a le trait [[S.H.I.E.L.D.]]\nAttachez cette carte à un personnage ami.\n1 max par personnage.\nLe personnage attaché gagne +1 point de vie et le trait [[S.H.I.E.L.D.]]",
    resumeEn: "Added “Max 1 per character.”",
    resumeFr: "Ajout de « 1 max par personnage ».",
  },
  '56019': {
    source: '1.8',
    en: "Play only if you have the [[Avenger]] trait.\n<b>Response</b>: After Yellowjacket enters play, search the top 5 cards of your deck for an upgrade and add it to your hand.",
    fr: "Jouez cette carte uniquement si vous avez le trait [[Avenger]].\n<b>Réponse</b> : après que Le Frelon est entré en jeu, cherchez une amélioration parmi les 5 cartes de votre deck et ajoutez-la à votre main.",
    resumeEn: "Changed “Yellow Jacket” to “Yellowjacket”.",
    resumeFr: "Titre : « Yellowjacket » (et non « Yellow Jacket »).",
  },
  '56073': {
    source: '1.8',
    en: null,
    fr: null,
    resumeEn: "Title should read “Yellowjacket”.",
    resumeFr: "Titre : « Yellowjacket ».",
  },
  '56098': {
    source: '1.8',
    en: "Permanent.\n<b>Forced Response</b>: After a leader, hero, or ally attacks Captain Marvel, place 1 energy counter here. Then, if there are at least 4 energy counters here, remove all of them and Captain Marvel attacks that character. This attack gains overkill.",
    fr: "Permanent.\n<b>Réponse forcée</b> : après qu'un leader, un héros ou un allié a attaqué Captain Marvel, placez 1 jeton Énergie ici. Ensuite, s'il y a au moins 4 jetons Énergie sur cette carte, retirez-les tous et Captain Marvel attaque ce personnage. Cette attaque gagne Déferlement.",
    resumeEn: "Changed “→” to “and”.",
    resumeFr: "La flèche de coût devient « et ».",
  },
  '57065': {
    source: '1.8',
    en: "Retaliate 2. Toughness.\n<b>When Revealed</b>: Resolve the \"<b>When Revealed</b>\" ability of the topmost treachery in the encounter discard pile. <i>(Limit once per phase.)</i>",
    fr: "Riposte 2. Ténacité.\n<b>Une fois révélée</b> : résolvez la capacité « <b>Une fois révélée</b> » de la traîtrise la plus proche du dessus de la pile de défausse Rencontre. (Une fois par phase max.)",
    resumeEn: "Added “(Limit once per phase.)”",
    resumeFr: "Ajout de « (Une fois par phase max.) ».",
  },
  '57076': {
    source: '1.8',
    en: "<b>Action</b>: Choose an attachment on the enemy leader with the text \"<b>Hero Action</b>\" or \"<b>Hero Response</b>\" and discard it.",
    fr: "<b>Action</b> : choisissez un attachement sur le leader ennemi ayant le texte « <b>Réponse de héros</b> » ou « <b>Action de héros</b> » et défaussez-le.",
    resumeEn: "Changed “Hero Interrupt” to “Hero Action.”",
    resumeFr: "« Interruption de héros » devient « Action ».",
  },
  '58002': {
    source: '1.8',
    en: "Permanent. Max 3 cards tucked here.\n<b>Response</b>: After you play an event with a printed [energy] resource, tuck that event from your discard pile under this card. Then, heal 1 damage from your identity.",
    fr: "Permanent. 3 cartes max. intercalées dessous.\n<b>Réponse</b> : après avoir joué un événement ayant une ressource [energy] imprimée, intercalez-le sous cette carte depuis votre pile de défausse. Puis, soignez 1 dégât de votre identité.",
    resumeEn: "Changed cost arrow to “Then”.",
    resumeFr: "La flèche de coût devient « Puis ».",
  },
}

/** Une même carte imprimée sous plusieurs codes (réimpressions, copies) : le code renvoie à l'entrée de la carte réelle. */
const RENVOIS: Readonly<Record<string, string>> = {
  '03024': '04021',
  '04147': '04057',
  '16024': '49023',
  '22020': '17020',
  '32142b': '32141b',
}

export const CODES_ERRATA: readonly string[] = [...Object.keys(ERRATA), ...Object.keys(RENVOIS)]

/** L'errata d'une carte (par son code de carte), ou rien. */
export function erratumDeCarte(codeCarte: string | undefined): ErratumRrg | undefined {
  const code = codeCarteConnu(codeCarte)
  if (code === undefined) return undefined
  return ERRATA[code] ?? ERRATA[RENVOIS[code] ?? '']
}

/** Le texte à poser sur la carte dans cette langue, ou rien (errata sans texte : pastille seule). */
export function texteErratum(erratum: ErratumRrg, langue: 'fr' | 'en'): string | undefined {
  return (langue === 'fr' ? erratum.fr : erratum.en) ?? undefined
}

export const SOURCE_ERRATA = 'Rules Reference'

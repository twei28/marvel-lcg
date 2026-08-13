// cartes-fr.js — le texte francais des cartes de l'aspect Determination.
//
// POURQUOI CE FICHIER EXISTE, ET POURQUOI IL EST SEPARE DES DONNEES
//
// La traduction d'une carte passe normalement par son IMAGE : le jeu demande
// assets/pics-fr/fr_<code>.jpg et retombe seul sur l'anglais quand elle manque
// (engine/file/cache.py). Determination est du contenu fan-made : il n'existe
// aucun scan francais, et il n'y en aura pas.
//
// Le texte, lui, EST affiche : la galerie le rend tel quel (galerie/app.js) et
// l'editeur de deck cherche dedans. Le traduire a donc une valeur immediate.
//
// MAIS PAS DANS data/cards.json. Deux endroits LISENT le texte anglais pour
// DECIDER, et une traduction en place les casserait :
//   * src/cards/pack/determination/dt133.py compte les personnages « Fragile. » ;
//   * src/game/card/face/card_type/scheme_main.py cherche « the players lose
//     the game » pour reconnaitre une manigance perdante.
// Le texte anglais reste donc la source, et le francais vit ici.
//
// TERMINOLOGIE : celle du jeu, pas une invention. overkill = Deferlement,
// piercing = Percant, ranged = A Distance (data/translate_fr.json) ; scheme =
// manigance, minion = sbire, villain = mechant, thwart = contrer, exhaust =
// incliner, ready = redresser, stunned = sonne, confused = desoriente, tough =
// coriace (dico du plateau).
//
// Les balises (<b>, <i>) et les jetons ([star], [per_hero], [boost]...) sont
// conserves a l'identique : un outil le verifie, parce qu'une balise perdue
// casse l'affichage sans rien dire.
"use strict";

import { langueActuelle } from "/public/js/prepare/langue.js";

const CARTES_FR = {
    "dt001": {
        "name": "* Cable",
        "text": "Téméraire. <i>(Après l'entrée en jeu de ce personnage, placez 1 menace sur chaque manigance.)</i>\n[star] <b>Interruption</b> : Quand Cable attaque, défaussez autant de cartes que vous voulez de votre main → Cable gagne +1 ATQ pour cette attaque par carte défaussée ainsi."
    },
    "dt002": {
        "name": "* Moon Knight",
        "text": "<b>Réponse forcée</b> : Après l'entrée en jeu de Moon Knight, défaussez une carte de votre main. Si la ressource imprimée de cette carte comprend :\n[energy] - Piochez une carte.\n[mental] - Désorientez un ennemi.\n[physical] - Sonnez un ennemi.\n[wild] - Choisissez 2 des effets ci-dessus."
    },
    "dt003": {
        "name": "* Venom",
        "text": "<b>Réponse forcée</b> : Après l'entrée en jeu de Venom, placez 2 menaces sur la manigance principale."
    },
    "dt004": {
        "name": "* Wolverine",
        "text": "[star] <b>Réponse forcée</b> : Après que Wolverine a contré, soignez-lui 2 dégâts."
    },
    "dt005": {
        "name": "Rayon de souffle",
        "text": "<b>Action de héros</b> <i>(attaque)</i> : Infligez jusqu'à 5 dégâts à votre héros et choisissez jusqu'à 3 ennemis → infligez X dégâts à chaque ennemi choisi, où X est le nombre de dégâts que votre héros a subis ainsi."
    },
    "dt006": {
        "name": "Bouclier humain",
        "text": "<b>Interruption de héros</b> <i>(défense)</i> : Quand un personnage allié s'apprête à subir des dégâts d'une attaque, prévenez jusqu'à 3 de ces dégâts. Ensuite, si vous avez subi des dégâts de cette attaque, redressez votre héros."
    },
    "dt007": {
        "name": "La Force de la Détermination",
        "text": "Max 2 par deck.\nDoublez le nombre de ressources générées par cette carte quand vous payez une carte Détermination <i>(violette)</i>."
    },
    "dt008": {
        "name": "Escouade de mercenaires",
        "text": "Usages (3 pions tactique).\n<b>Action</b> : Inclinez l'Escouade de mercenaires et retirez-lui 1 pion tactique → infligez 1 dégât à un ennemi et retirez 1 menace de la manigance principale."
    },
    "dt009": {
        "name": "Complexe du sauveur",
        "text": "<b>Interruption de héros</b> : Quand un allié que vous contrôlez s'apprête à subir des dégâts conséquents, inclinez le Complexe du sauveur → infligez ces dégâts à votre héros à la place."
    },
    "dt010": {
        "name": "Gilet de combat héroïque",
        "text": "Jouable sous le contrôle de n'importe quel joueur. Max 1 par joueur.\n<b>Action de héros</b> : Subissez 1 dégât → votre héros gagne +1 CTR, +1 ATQ ou +1 DEF jusqu'à la fin du round. <i>(Limite d'une fois par round.)</i>"
    },
    "dt011": {
        "name": "Je peux faire ça toute la journée",
        "text": "Max 1 par joueur.\n<b>Interruption</b> : Quand votre héros s'apprête à être vaincu, placez 1 [per_hero] menace sur la manigance principale et réglez votre cadran de points de vie sur 1 à la place. Ensuite, retirez cette carte de la partie."
    },
    "dt012": {
        "name": "Disparu en un éclair",
        "text": "Jouable seulement si les points de vie restants de votre héros sont inférieurs à la moitié de ses points de vie de départ.\n<b>Action de héros</b> : Désorientez un ennemi. Ensuite, changez de forme."
    },
    "dt013": {
        "name": "Reconnaissance",
        "text": "<b>Action de héros</b> : Dépensez une ressource de n'importe quel type ou inclinez un personnage allié que vous contrôlez → regardez jusqu'à 3 cartes Rencontre face cachée. Si un sbire est vu ainsi, mettez-le en jeu engagé avec vous, et piochez 2 cartes. <i>(Limite d'une fois par round.)</i>"
    },
    "dt014": {
        "name": "Contre-attaque",
        "text": "Max 1 par joueur.\n<b>Réponse de héros</b> : Après qu'une attaque avec Déferlement a vaincu un allié que vous contrôlez et vous a blessé, défaussez Contre-attaque → infligez X dégâts à un ennemi, où X est le total de l'ATQ de cet allié et de votre héros."
    },
    "dt015": {
        "name": "Préparation n°2",
        "text": "Max 1 par joueur.\n<b>Action de héros</b> : Infligez 2 dégâts à votre héros et défaussez Préparation n°2 → redressez votre héros et infligez 1 dégât à chaque sbire engagé avec vous."
    },
    "dt016": {
        "name": "* Deadpool",
        "text": "<b>Réponse forcée</b> : Après l'entrée en jeu de Deadpool, distribuez-vous 1 carte Rencontre."
    },
    "dt017": {
        "name": "Masochisme",
        "text": "<b>Réponse de héros</b> : Après avoir subi plus de 3 dégâts, piochez X cartes, où X est le nombre de dégâts subis au-delà de 3."
    },
    "dt018": {
        "name": "Sentir la douleur",
        "text": "Tant que les points de vie restants de votre héros sont inférieurs à la moitié de ses points de vie maximum, votre héros gagne Riposte 1."
    },
    "dt019": {
        "name": "Galvaniser",
        "text": "Jouable seulement si les points de vie maximum de votre héros sont de 12 ou plus.\n<b>Action de héros</b> : Inclinez Galvaniser et subissez 3 dégâts → redressez votre héros ou piochez 1 carte."
    },
    "dt020": {
        "name": "Tenir bon",
        "text": "Max 1 par joueur.\n<b>Action de héros</b> : Inclinez Tenir bon et subissez 2 dégâts → si vous avez moins de la moitié de vos points de vie maximum restants, vous gagnez +2 en taille de main jusqu'à la fin de la phase."
    },
    "dt021": {
        "name": "Spontanéité",
        "text": "Jouable sous le contrôle de n'importe quel joueur. Max 1 par joueur.\n<b>Ressource</b> : Inclinez Spontanéité et subissez 1 dégât → générez une ressource [wild] pour un événement Détermination <i>(violet)</i>."
    },
    "dt022": {
        "name": "* Cloak",
        "text": "Vous pouvez jouer les cartes attachées à Cloak comme si elles étaient dans votre main.\n<b>Action de héros</b> : Inclinez Cloak → choisissez un allié ou une amélioration dans votre main et attachez-la-lui face cachée."
    },
    "dt023": {
        "name": "* Dagger",
        "text": "Fragile. <i>(Les attaques contre ce personnage gagnent Déferlement.)</i>\nTant que Dagger est attachée à l'allié Cloak, réduisez de 2 le coût pour la jouer."
    },
    "dt024": {
        "name": "* Elektra",
        "text": "Fragile. <i>(Les attaques contre ce personnage gagnent Déferlement.)</i>\nLes attaques d'Elektra gagnent Perçant et À Distance."
    },
    "dt025": {
        "name": "* Shang-Chi",
        "text": "Fragile. <i>(Les attaques contre ce personnage gagnent Déferlement.)</i>\n<b>Réponse</b> : Après que Shang-Chi a retiré la dernière menace d'une manigance ou vaincu un sbire, redressez-le."
    },
    "dt026": {
        "name": "* Le Punisher",
        "text": "Fragile. <i>(Les attaques contre ce personnage gagnent Déferlement.)</i>\nLes attaques du Punisher gagnent Perçant et À Distance."
    },
    "dt027": {
        "name": "Coup bas",
        "text": "<b>Action de héros</b> <i>(attaque)</i> : Infligez 2 dégâts à un ennemi (4 dégâts à la place si cet ennemi est sonné ou désorienté). Cette attaque gagne Perçant."
    },
    "dt028": {
        "name": "Renvoyer l'ascenseur",
        "text": "<b>Action de héros</b> <i>(attaque/contre)</i> : Subissez jusqu'à 3 dégâts → infligez X dégâts répartis entre les ennemis comme vous le souhaitez, puis retirez X menaces réparties entre les manigances en jeu comme vous le souhaitez, où X est le nombre de dégâts que vous avez subis ainsi."
    },
    "dt029": {
        "name": "Une épine dans le pied",
        "text": "<b>Action de héros</b> <i>(contre)</i> : Retirez 2 menaces d'une manigance. Ensuite, vous pouvez subir jusqu'à 5 dégâts et retirer 1 menace d'une manigance par point de dégât subi ainsi, réparties entre les manigances comme vous le souhaitez."
    },
    "dt030": {
        "name": "Injection d'adrénaline",
        "text": "Usages (2 pions adrénaline).\n<b>Action</b> : Inclinez l'Injection d'adrénaline et retirez-lui 1 pion adrénaline → choisissez un allié. La prochaine attaque de cet allié inflige 2 dégâts supplémentaires et il subit 1 dégât conséquent supplémentaire."
    },
    "dt031": {
        "name": "Agir d'instinct",
        "text": "<b>Réponse de héros</b> : Après être passé en forme héros, donnez une carte d'état à un personnage."
    },
    "dt032": {
        "name": "Rire jaune",
        "text": "Jouable seulement si les points de vie restants de votre héros sont inférieurs à la moitié de ses points de vie de départ.\n<b>Action de héros</b> <i>(attaque)</i> : Subissez 1 dégât et infligez 6 dégâts au méchant. Ensuite, changez de forme."
    },
    "dt033": {
        "name": "Subsistance",
        "text": "Jouable seulement si votre identité a le trait AVENGER.\n<b>Action de héros</b> : Soignez 1 dégât à votre identité. Soignez-lui X dégâts supplémentaires, où X est égal au numéro de stade du méchant."
    },
    "dt034": {
        "name": "Téléportation improvisée",
        "text": "<b>Action de héros</b> : Donnez 1 carte de boost face cachée au méchant → changez de forme, puis redressez votre identité."
    },
    "dt035": {
        "name": "* Gladiator",
        "text": "Tant que vos points de vie restants sont inférieurs ou égaux à 5, réduisez de 2 tous les dégâts conséquents subis par Gladiator."
    },
    "dt036": {
        "name": "* Quasar",
        "text": "<b>Réponse</b> : Après l'entrée en jeu de Quasar, infligez 2 dégâts à chaque ennemi engagé avec vous."
    },
    "dt037": {
        "name": "* Star-Lord",
        "text": "[star] <b>Réponse</b> : Après que Star-Lord a contré, infligez 1 dégât à un ennemi."
    },
    "dt038": {
        "name": "Détonation",
        "text": "<b>Action de héros</b> <i>(attaque)</i> : Défaussez une amélioration que vous contrôlez portant des pions, puis infligez X dégâts au méchant et à chaque sbire engagé avec vous, où X est le nombre de pions défaussés ainsi."
    },
    "dt039": {
        "name": "Entrée et sortie",
        "text": "<b>Action de héros</b> <i>(contre)</i> : Retirez 2 menaces d'une manigance. Si c'est la première carte que vous jouez ce round, vous pouvez subir 1 dégât pour renvoyer cette carte dans votre main."
    },
    "dt040": {
        "name": "Coup en traître",
        "text": "<b>Action de héros</b> <i>(attaque)</i> : Infligez 2 dégâts à un ennemi. Si c'est la première carte que vous jouez ce round, vous pouvez subir 1 dégât pour renvoyer cette carte dans votre main."
    },
    "dt041": {
        "name": "Munitions illégales",
        "text": "Restreint. Cette carte ne peut pas être en jeu tant que vous contrôlez un allié.\nVos attaques de base gagnent Déferlement.\n<b>Réponse</b> : Après avoir attaqué un sbire et infligé 2 dégâts excédentaires ou plus avec Déferlement, sonnez le méchant."
    },
    "dt042": {
        "name": "I.C.E.R.",
        "text": "Restreint. Usages (3 pions charge).\n<b>Action de héros</b> : Inclinez l'I.C.E.R. et retirez-lui 1 pion charge → infligez 1 dégât à un sbire et sonnez-le."
    },
    "dt043": {
        "name": "* La Chose",
        "text": "Ténacité.\n<b>Interruption forcée</b> : Quand votre héros s'apprête à subir des dégâts, infligez ces dégâts à La Chose à la place."
    },
    "dt044": {
        "name": "Pansement de fortune",
        "text": "<b>Action de héros</b> : Distribuez-vous 1 carte Rencontre face cachée, puis soignez 6 dégâts à votre identité."
    },
    "dt045": {
        "name": "Envol",
        "text": "Jouable seulement si votre identité a le trait AERIAL.\n<b>Action de héros</b> : Placez 2 menaces sur la manigance principale → sonnez et désorientez le méchant."
    },
    "dt046": {
        "name": "Faire rempart",
        "text": "<b>Interruption de héros</b> <i>(défense)</i> : Quand un personnage allié s'apprête à subir des dégâts, distribuez-vous une carte Rencontre face cachée → prévenez jusqu'à 5 de ces dégâts."
    },
    "dt047": {
        "name": "S'attarder un peu trop",
        "text": "<b>Action de héros</b> <i>(contre)</i> : Distribuez-vous 1 carte Rencontre face cachée, puis choisissez :\n• Retirez 5 menaces d'une manigance.\n• Retirez 2 menaces de chaque manigance en jeu."
    },
    "dt048": {
        "name": "Payer les pots cassés",
        "text": "<b>Action de héros</b> : Donnez au méchant une ou plusieurs cartes Rencontre face cachée de votre zone de joueur comme cartes de boost face cachée. Ensuite, le méchant vous attaque. Cette attaque gagne Déferlement et Perçant."
    },
    "dt049": {
        "name": "Tenter le diable",
        "text": "<b>Interruption de héros</b> <i>(attaque/défense/contre)</i> : Quand un ennemi s'active contre vous, distribuez-vous une carte Rencontre face cachée → annulez cette activation. Si une attaque a été annulée ainsi, infligez 3 dégâts à cet ennemi. Si une manigance a été annulée ainsi, retirez 2 menaces de la manigance principale."
    },
    "dt050": {
        "name": "Avide de souffrance",
        "text": "Jouable seulement si les points de vie restants de votre héros sont inférieurs à la moitié de ses points de vie de départ.\n<b>Action de héros</b> <i>(attaque)</i> : Subissez 2 dégâts. Ensuite, infligez 8 dégâts au méchant."
    },
    "dt051": {
        "name": "Dernier recours",
        "text": "<b>Interruption de héros</b> : Quand un personnage GUARDIAN que vous contrôlez s'apprête à subir des dégâts, placez 2 menaces sur la manigance principale et défaussez Dernier recours → prévenez 6 de ces dégâts."
    },
    "dt052": {
        "name": "* Blade",
        "text": "<b>Réponse</b> : Après que Blade a vaincu un sbire sans infliger de dégâts excédentaires, soignez-lui 2 dégâts."
    },
    "dt053": {
        "name": "* Ghost Rider",
        "text": "[star] <b>Interruption de héros</b> : Quand Ghost Rider attaque, infligez jusqu'à 3 dégâts à votre héros. Ghost Rider gagne +1 ATQ pour cette attaque par dégât subi ainsi par votre héros."
    },
    "dt054": {
        "name": "* Morbius",
        "text": "<b>Réponse forcée</b> : Après l'entrée en jeu de Morbius, infligez 2 dégâts à votre identité."
    },
    "dt055": {
        "name": "Magie noire",
        "text": "Jouable seulement si votre identité a le trait MYSTIC. Max 1 par deck.\n<b>Action de héros</b> <i>(attaque)</i> : Mélangez votre deck. Choisissez un ennemi et retirez de la partie jusqu'à 3 cartes du dessus de votre deck → drainez 2 à cet ennemi par carte retirée ainsi."
    },
    "dt056": {
        "name": "* Oblivion",
        "text": "<b>Action</b> : Mélangez cette carte dans le deck Rencontre (sans la regarder).\n<b>Quand révélée</b> : Le joueur qui a joué cette carte choisit de défausser une carte de sa main ou d'infliger 5 dégâts à chaque allié qu'il contrôle, au méchant et à chaque sbire engagé avec lui. Retirez cette carte de la partie."
    },
    "dt057": {
        "name": "Deux fois la Détermination",
        "text": "Max 1 par deck.\n<b>Réponse de héros</b> : Après avoir dépensé cette carte, renvoyez-la dans votre main. <i>(Limite d'une fois par round.)</i>"
    },
    "dt058": {
        "name": "Héros à louer",
        "text": "Jouable sous le contrôle de n'importe quel joueur. Max 1 carte TEAM par joueur.\nSi chacun de vos alliés a le trait HERO FOR HIRE, cette carte gagne : « <b>Réponse</b> : Après qu'un allié que vous contrôlez a vaincu un ennemi, piochez 1 carte. »"
    },
    "dt059": {
        "name": "Entraînement Arme X",
        "text": "Max 1 par joueur.\nLes alliés que vous contrôlez à qui il reste 1 point de vie gagnent +2 ATQ et subissent 2 dégâts conséquents supplémentaires."
    },
    "dt060": {
        "name": "Entraînement aux explosifs",
        "text": "Jouable seulement si votre identité a le trait GUARDIAN. Max 1 par joueur.\n<b>Réponse</b> : Après avoir défaussé une amélioration que vous contrôlez, inclinez l'Entraînement aux explosifs → infligez 2 dégâts à un ennemi."
    },
    "dt061": {
        "name": "Embuscade spatiale",
        "text": "Alliance.\n<b>Action de héros</b> <i>(attaque)</i> : Inclinez un personnage AVENGER et un personnage GUARDIAN et infligez 1 dégât à chacun d'eux → infligez un total de 6 dégâts répartis entre les ennemis comme vous le souhaitez. Si aucun de ces personnages alliés n'a été vaincu ainsi, redressez-les."
    },
    "dt062": {
        "name": "« C'est tout ce que t'as ? »",
        "text": "Max 1 par round.\n<b>Action de héros</b> : Cherchez un attachement dans le deck Rencontre. Révélez cet attachement → piochez 3 cartes. <i>(Mélangez le deck Rencontre.)</i>"
    },
    "dt063": {
        "name": "* La Torche humaine",
        "text": "<b>Réponse forcée</b> : Après le début de votre tour, infligez 1 dégât au méchant, à chaque sbire engagé avec vous, à votre héros et à chaque autre allié que vous contrôlez."
    },
    "dt064": {
        "name": "Entraînement à la résistance",
        "text": "Max 2 par deck. Usages (2 pions entraînement).\n<b>Action d'alter-ego</b> : Inclinez cette carte et retirez-lui 1 pion entraînement → choisissez un événement Détermination <i>(violet)</i> dans votre pile de défausse et mélangez-le dans votre deck."
    },
    "dt065": {
        "name": "* Colleen Wing",
        "text": "Fragile.\nColleen Wing gagne +1 CTR tant que Misty Knight est en jeu, et +1 ATQ quand elle attaque des ennemis portant l'amélioration Prime."
    },
    "dt066": {
        "name": "* Misty Knight",
        "text": "<b>Action</b> : Inclinez Misty Knight et infligez-lui 1 dégât → choisissez l'un des effets suivants :\n• Cherchez un exemplaire de l'amélioration Prime dans votre deck et votre pile de défausse et ajoutez-le à votre main.\n• Réduisez de 1 le coût en ressources de la prochaine amélioration Prime que vous jouez ce tour-ci."
    },
    "dt067": {
        "name": "Prime",
        "text": "Attachez à un sbire ayant le trait BRUTE, CRIMINAL ou MERCENARY, ou à un ennemi unique (✦). Max 1 par ennemi.\n<b>Réponse</b> : Après que l'ennemi attaché a été attaqué et vaincu, le propriétaire de cette carte pioche 2 cartes. Si l'attaquant a le trait HERO FOR HIRE, soignez-lui 1 dégât."
    },
    "dt068": {
        "name": "Pistolet double",
        "text": "Attachez à un allié. Max 1 par allié. Usages (1 pion munition et 1 pion charge).\n<b>Action</b> : Inclinez le Pistolet double et choisissez l'un des effets suivants :\n• Retirez-lui 1 pion munition → la prochaine attaque de l'allié attaché gagne Perçant.\n• Retirez-lui 1 pion charge → la prochaine attaque de l'allié attaché gagne Déferlement."
    },
    "dt069": {
        "name": "Motivé",
        "text": "Attachez à un allié. Max 1 par allié.\n<b>Interruption</b> : Quand l'allié attaché attaque un ennemi, il gagne +X ATQ pour cette attaque, où X est le nombre de cartes attachées à cet ennemi."
    },
    "dt070": {
        "name": "Dépôt de munitions",
        "text": "Entre en jeu avec 2 pions munition et 2 pions charge. Max 1 par joueur.\n<b>Action</b> : Inclinez le Dépôt de munitions → déplacez 1 pion munition ou 1 pion charge de cette carte vers une autre amélioration que vous contrôlez."
    },
    "dt071": {
        "name": "Se déchaîner",
        "text": "Exigence ([wild][physical]). Max 2 par deck.\n<b>Action de héros</b> <i>(attaque)</i> : Subissez 2 dégâts → piochez 3 cartes et infligez X dégâts à un ennemi, où X est le total des coûts en ressources imprimés de ces cartes."
    },
    "dt072": {
        "name": "* Red Dagger",
        "text": "<b>Action de héros</b> : Placez 1 pion accélération sur Red Dagger. <i>(Limite d'une fois par phase.)</i>\n<b>Interruption</b> : Quand Red Dagger attaque, résolvez cette attaque X fois, où X est le nombre de pions accélération en jeu."
    },
    "dt073": {
        "name": "* Starling",
        "text": "Fragile.\n<b>Réponse de héros</b> : Après que Starling a subi 5 dégâts ou plus d'une attaque, votre héros gagne +1 ATQ jusqu'à la fin de la partie."
    },
    "dt074": {
        "name": "En coulisses",
        "text": "Max 2 par deck.\n<b>Interruption de héros</b> : Quand le méchant attaque, si votre identité a le trait AERIAL, donnez au méchant 1 carte de boost supplémentaire pour cette activation et défaussez cette carte → mettez en jeu l'allié le plus haut de votre pile de défausse. Déclarez-le défenseur pour cette attaque. Ensuite, désorientez le méchant."
    },
    "dt075": {
        "name": "Pitreries multiverselles",
        "text": "Mise en place. Max 1 par deck.\n<b>Interruption forcée</b> : Quand la partie commence, choisissez 3 cartes d'aspect non-Détermination différentes de votre collection et mettez-les de côté.\n<b>Action</b> : Inclinez cette carte et distribuez-vous une carte Rencontre face cachée → cherchez 1 de ces cartes mises de côté et ajoutez-la à votre main."
    },
    "dt076": {
        "name": "* Gorilla-Man",
        "text": "Gorilla-Man ignore le texte « Max 1 par allié » des améliorations."
    },
    "dt077": {
        "name": "* Hit-Monkey",
        "text": "<b>Interruption</b> : Quand Hit-Monkey s'apprête à subir des dégâts conséquents, regardez la carte du dessus du deck Rencontre → prévenez 1 de ces dégâts par icône de boost ([boost]) et par étoile ([star]) vue ainsi."
    },
    "dt078": {
        "name": "Équipement encombrant",
        "text": "Jouable seulement si votre héros a une taille de main imprimée de 4 ou moins. Max 1 par deck.\nVotre héros gagne +2 en taille de main.\n<b>Interruption forcée</b> : Quand la phase du méchant commence, choisissez de défausser cette carte ou de placer 1 pion accélération dessus."
    },
    "dt079": {
        "name": "Matériel emprunté",
        "text": "Attachez à un allié. Max 1 par deck.\nL'allié attaché gagne +1 point de vie par amélioration qui lui est attachée (jusqu'à un maximum de +4 points de vie).\n<b>Réponse forcée</b> : Après l'entrée en jeu de Matériel emprunté, attachez-lui un allié de votre pile de défausse face cachée → l'allié attaché gagne les TRAITS de cet allié face cachée."
    },
    "dt080": {
        "name": "* Masacre",
        "text": "<b>Réponse de héros</b> : Après l'entrée en jeu de Masacre, cherchez un exemplaire du soutien Escouade de mercenaires dans votre deck et votre pile de défausse et mettez-le en jeu.\n<b>Action de héros</b> : Infligez 1 dégât à Masacre → placez 1 pion tactique sur chaque Escouade de mercenaires que vous contrôlez. <i>(Limite d'une fois par round.)</i>"
    },
    "dt081": {
        "name": "Entraînement au sabre",
        "text": "Attachez à un allié X-MEN. Max 1 amélioration TRAINING par allié.\n<b>Réponse</b> : Après que l'allié attaché a effectué une attaque qui retire une carte d'état coriace d'un ennemi, sonnez cet ennemi."
    },
    "dt082": {
        "name": "Choix difficile",
        "text": "<b>Action de héros</b> : Subissez 2 dégâts → donnez une carte d'état coriace à un personnage. Si une carte d'état coriace a été donnée à un ennemi ainsi, soignez 4 dégâts à votre héros."
    },
    "dt083": {
        "name": "Force excessive",
        "text": "<b>Action de héros</b> <i>(attaque)</i> : Infligez X dégâts à un ennemi. Cette attaque gagne Perçant. Si cet ennemi est vaincu ainsi, piochez X cartes. Si une carte d'état coriace a été retirée ainsi, piochez 2 cartes."
    },
    "dt084": {
        "name": "À l'improviste",
        "text": "Exigence ([wild]).\n<b>Action de héros</b> : Cherchez un exemplaire de Spontanéité dans votre deck, votre main et votre pile de défausse et mettez-le en jeu. Si vous en contrôlez déjà un, infligez plutôt 1 dégât à un personnage, puis placez une carte d'état sur lui."
    },
    "dt085": {
        "name": "* ForgetMeNot",
        "text": "ForgetMeNot ne compte pas dans votre limite d'alliés.\n<b>Réponse</b> : Après avoir subi des dégâts d'une carte Détermination <i>(violette)</i>, infligez 1 dégât à ForgetMeNot → soignez 2 dégâts à votre identité."
    },
    "dt086": {
        "name": "Désarmé avec agressivité",
        "text": "Jouable sous le contrôle de n'importe quel joueur. Max 1 par joueur.\nTant que les points de vie restants de votre héros sont inférieurs à la moitié de ses points de vie de départ, votre héros gagne +2 ATQ et -1 en taille de main."
    },
    "dt087": {
        "name": "« Vas-y, Boum-Boum ! »",
        "text": "<b>Réponse de héros</b> : Après avoir subi des dégâts, attachez cette carte à un ennemi.\nÉphémère. <i>(Cette carte doit être défaussée à la fin de la phase.)</i>\n<b>Interruption</b> : Quand cette carte s'apprête à être défaussée, infligez 1 dégât à chaque ennemi en jeu."
    },
    "dt088": {
        "name": "Fausse sécurité",
        "text": "Attachez à un sbire et donnez-lui une carte d'état coriace.\n<b>Réponse forcée</b> : Après qu'une carte d'état coriace a été retirée du sbire attaché, défaussez Fausse sécurité → redressez un personnage allié."
    },
    "dt089": {
        "name": "Concaténer",
        "text": "Attachez à un ennemi.\n<b>Interruption de héros</b> <i>(attaque)</i> : Quand vous attaquez l'ennemi attaché, défaussez chaque amélioration TACTIC attachée à cet ennemi → infligez-lui 2 dégâts par carte défaussée ainsi et cette attaque gagne Déferlement."
    },
    "dt090": {
        "name": "Contrôle psychique des foules",
        "text": "Jouable seulement si votre identité a le trait PSIONIC.\n<b>Action de héros</b> : Inclinez votre identité → choisissez l'un des effets suivants :\n• Désorientez chaque sbire engagé avec vous.\n• Infligez 2 dégâts à chaque ennemi désorienté."
    },
    "dt091": {
        "name": "Énergie déterminée",
        "text": "Max 2 par deck.\n<b>Interruption de héros</b> : Quand vous dépensez cette carte pour jouer une carte TACTIC, donnez une carte d'état coriace à un allié et à un sbire."
    },
    "dt092": {
        "name": "* X-23",
        "text": "Téméraire. <i>(Après l'entrée en jeu de ce personnage, placez 1 menace sur chaque manigance.)</i>\n[star] <b>Réponse forcée</b> : Après que X-23 a contré, soignez-lui 2 dégâts."
    },
    "dt093": {
        "name": "Paratonnerre",
        "text": "Attachez à un sbire. Max 1 par sbire.\n<b>Interruption forcée</b> : Quand une carte du set Rencontre standard est révélée, défaussez le Paratonnerre → infligez 6 dégâts au sbire attaché. Les dégâts excédentaires sont infligés au personnage portant le plus de cartes attachées."
    },
    "dt094": {
        "name": "Talent de diversion",
        "text": "Usages (3 pions diversion). Max 1 par joueur.\n<b>Interruption</b> : Quand vous subissez des dégâts d'une attaque, retirez 1 pion diversion de cette carte → subissez 1 dégât supplémentaire et piochez 1 carte."
    },
    "dt095": {
        "name": "Sur les rotules",
        "text": "Jouable seulement si votre identité a le trait X-MEN.\n<b>Action de héros</b> <i>(attaque/contre)</i> : Défaussez chaque allié X-MEN que vous contrôlez → retirez X menaces réparties entre les manigances et infligez X dégâts répartis entre les ennemis, où X est le total des points de vie restants de ces alliés."
    },
    "dt096": {
        "name": "* Péril pourpre",
        "text": "Victoire 0. Seul le propriétaire de cette carte peut en retirer de la menace.\n<b>Réponse de héros</b> : Après que cette carte a été placée dans la zone de victoire, défaussez X cartes du dessus de votre deck et ajoutez à votre main chaque carte Détermination défaussée ainsi (jusqu'à un maximum de 5), où X est le nombre de cartes dans la zone de victoire."
    },
    "dt097": {
        "name": "Glissement temporel",
        "text": "<b>Réponse de héros</b> : Après qu'une carte que vous contrôlez a été vaincue, choisissez l'un des effets suivants :\n• Placez-la dans la zone de victoire et piochez 1 carte."
    },
    "dt098": {
        "name": "* Bedlam",
        "text": "Victoire 0.\n<b>Ressource de héros</b> : Vainquez Bedlam → générez des ressources [physical][mental][energy]."
    },
    "dt099": {
        "name": "* Marrow",
        "text": "Téméraire.\n[star] <b>Interruption</b> : Quand Marrow attaque, défaussez la carte du dessus de votre deck. Si une ressource [energy] ou [physical] a été défaussée ainsi, cette attaque gagne Perçant et À Distance."
    },
    "dt100": {
        "name": "* Archangel",
        "text": "Alias. <i>(Si vous contrôlez une carte au sous-titre identique, défaussez-la et jouez cette carte gratuitement.)</i>\nTéméraire. Riposte 2.\n<b>Réponse</b> : Après qu'un personnage AERIAL a utilisé un pouvoir de base, inclinez Archangel et infligez-lui 1 dégât → redressez ce personnage."
    },
    "dt101": {
        "name": "* Darkhawk",
        "text": "[star] Entre en jeu avec un pion configuration sur son ATQ. Darkhawk gagne +2 au pouvoir portant un pion.\n<b>Action</b> : Inclinez Darkhawk → déplacez le pion configuration sur son autre pouvoir de base."
    },
    "dt102": {
        "name": "* Un jeu dangereux",
        "text": "Vous ne pouvez pas déplacer plus de 4 menaces vers cette carte par tour.\n<b>Action de héros</b> : Subissez jusqu'à 4 dégâts → déplacez ce nombre de menaces d'une autre manigance vers cette carte.\n<b>Réponse forcée</b> : Après que de la menace a été placée ici, s'il y a au moins 16 [per_hero] menaces ici, infligez 16 [per_hero] dégâts au méchant et retirez cette carte de la partie."
    },
    "dt103": {
        "name": "En pleine ligne de mire",
        "text": "<b>Action de héros</b> <i>(attaque)</i> : Infligez un total de 5 dégâts répartis entre les personnages comme vous le souhaitez. Ensuite, chaque joueur pioche 1 carte par personnage AERIAL sous son contrôle blessé ainsi."
    },
    "dt104": {
        "name": "Détourner l'attention",
        "text": "Jouable seulement s'il y a une manigance annexe dans la zone de victoire.\n<b>Action de héros</b> : Déplacez jusqu'à 6 menaces d'une manigance vers les autres manigances en jeu, réparties aussi équitablement que possible."
    },
    "dt105": {
        "name": "* Venompool",
        "text": "Alias. Venompool gagne +1 ATQ par carte Rencontre face cachée devant vous (jusqu'à un maximum de +3 ATQ).\n<b>Réponse forcée</b> : Après l'entrée en jeu de Venompool, choisissez de placer 2 menaces sur la manigance principale ou de vous distribuer une carte Rencontre face cachée."
    },
    "dt106": {
        "name": "* Captain Universe",
        "text": "Alias.\n<b>Interruption</b> : Quand Captain Universe s'apprête à subir des dégâts conséquents, réduisez ce montant de X, où X est le nombre de cartes Rencontre face cachée devant vous."
    },
    "dt107": {
        "name": "* Zenpool",
        "text": "Alias.\n<b>Interruption</b> : Quand Zenpool entre en jeu, dépensez autant de ressources que vous voulez. Défaussez 1 carte Rencontre face cachée devant vous par ressource dépensée ainsi."
    },
    "dt108": {
        "name": "Défier l'avenir",
        "text": "<b>Action de héros</b> : Regardez la carte du dessus du deck Rencontre et chaque carte Rencontre face cachée devant vous. Vous pouvez défausser autant de ces cartes que vous voulez. Distribuez-vous 1 carte Rencontre face cachée par carte défaussée ainsi."
    },
    "dt109": {
        "name": "Déphasage",
        "text": "<b>Action de héros</b> : Choisissez un personnage allié dans n'importe quelle zone de jeu <i>(y compris la zone de mission)</i>, le deck ou la main d'un joueur → jusqu'à ce que ce personnage soit retourné ou entre dans une pile de défausse, traitez-le comme s'il avait une ressource [wild] imprimée supplémentaire et une boîte de texte vierge <i>(sauf les TRAITS)</i>."
    },
    "dt110": {
        "name": "Bulle temporelle",
        "text": "<b>Action de héros</b> : Choisissez de défausser X cartes de votre main et de subir X dégâts, ou de vous distribuer X cartes Rencontre face cachée → redressez X cartes que vous contrôlez."
    },
    "dt111": {
        "name": "* Morph",
        "text": "<b>Interruption forcée</b> : Quand la boîte de texte de Morph s'apprête à être traitée comme vierge, Morph gagne +2 CTR et +2 ATQ jusqu'à ce qu'il quitte le jeu."
    },
    "dt112": {
        "name": "* Spiral",
        "text": "[star] Spiral gagne +1 ATQ par carte face cachée devant vous. Elle ne peut pas dépasser 6 ATQ.\n<b>Réponse forcée</b> : Après l'entrée en jeu de Spiral, distribuez-vous 2 cartes Rencontre face cachée."
    },
    "dt113": {
        "name": "* Tabula Rasa",
        "text": "Attachez à un personnage allié ayant une boîte de texte vierge <i>(sauf les TRAITS)</i>.\n<b>Ressource de héros</b> : Inclinez le personnage attaché → générez ses ressources imprimées pour un événement."
    },
    "dt114": {
        "name": "* Blink",
        "text": "<b>Action</b> : Inclinez Blink et infligez 1 dégât à elle et à votre identité → choisissez de redresser une carte LOCATION ou de changer de forme."
    },
    "dt115": {
        "name": "Quoi qu'il en coûte",
        "text": "Alliance.\n<b>Action de héros</b> <i>(attaque/contre)</i> : Infligez jusqu'à 3 dégâts à un personnage X-MEN et jusqu'à 3 dégâts à un personnage X-FORCE → retirez X menaces réparties entre les manigances en jeu et infligez X dégâts répartis entre les ennemis en jeu, où X est le total des dégâts subis ainsi."
    },
    "dt116": {
        "name": "* Agent Koenig",
        "text": "Fragile.\n[star] L'Agent Koenig entre en jeu avec 1 pion LMD sur lui. Tant qu'il porte 1 pion ou plus, il gagne +1 ATQ.\n<b>Interruption</b> : Quand l'Agent Koenig s'apprête à être vaincu, retirez-lui 1 pion LMD → retirez-lui tous ses dégâts à la place."
    },
    "dt117": {
        "name": "* Le Béhémoth",
        "text": "Usages (2 pions déploiement).\n<b>Action</b> : Inclinez Le Béhémoth, retirez-lui 1 pion déploiement et défaussez un allié que vous contrôlez → cherchez un allié S.H.I.E.L.D. dans votre collection ou votre deck et mettez-le en jeu."
    },
    "dt118": {
        "name": "* Le Pic",
        "text": "<b>Réponse</b> : Après avoir retiré un pion polyvalent d'une carte que vous contrôlez, placez-le ici (jusqu'à un maximum de 6 pions ici).\n<b>Action</b> : Défaussez Le Pic et 1 carte de votre main → infligez 1 dégât au méchant et retirez 1 menace d'une manigance par pion défaussé ainsi."
    },
    "dt119": {
        "name": "Support technique",
        "text": "Usages (2 pions stimulant).\n<b>Réponse</b> : Après avoir retiré un pion polyvalent d'une carte que vous contrôlez, inclinez le Support technique et retirez-lui un pion stimulant → redressez un personnage S.H.I.E.L.D. ou un soutien PERSONA."
    },
    "dt120": {
        "name": "Technologie bricolée",
        "text": "<b>Interruption</b> : Quand une carte de boost est retournée face visible, défaussez Technologie bricolée et la carte du dessus de votre deck → si le coût imprimé de cette carte est supérieur à X, où X est le nombre d'icônes ([star] et [boost]) sur la carte de boost, placez un total de X pions polyvalents sur des cartes que vous contrôlez. Ensuite, défaussez la carte de boost."
    },
    "dt121": {
        "name": "Explosion radioactive",
        "text": "Vous gagnez -1 point de vie.\n<b>Réponse de héros</b> : Après avoir changé de forme, défaussez Explosion radioactive → résolvez la capacité « <b>Spécial</b> » de cette carte.\n<b>Spécial</b> : Infligez à un ennemi des dégâts égaux à votre ATQ. Si 3 dégâts ou plus ont été infligés ainsi, sonnez cet ennemi."
    },
    "dt122": {
        "name": "* Spiders-Man",
        "text": "Usages (5 pions araignée). Fragile.\n[star] Spiders-Man ne peut pas quitter le jeu tant qu'il porte 1 pion araignée ou plus.\n<b>Interruption forcée</b> : Quand Spiders-Man utilise un pouvoir de base, retirez-lui 1 pion araignée ou plus → infligez 1 dégât à un ennemi par pion retiré ainsi."
    },
    "dt123": {
        "name": "* Ralph",
        "text": "<b>Interruption de héros</b> : Quand votre héros attaque un ennemi, attachez Ralph à cet ennemi et regardez 2 cartes parmi le dessus du deck Rencontre et les cartes Rencontre distribuées aux joueurs → cette attaque gagne Perçant et inflige X dégâts supplémentaires à la fois à cet ennemi et à Ralph, où X est le nombre d'icônes de boost ([boost]) vues ainsi."
    },
    "dt124": {
        "name": "Cible désignée",
        "text": "Jouable seulement si votre identité a le trait SOLDIER. Attachez à un sbire. Max 1 par sbire.\nLes attaques contre le sbire attaché gagnent À Distance et infligent 1 dégât supplémentaire par carte attachée à ce sbire."
    },
    "dt125": {
        "name": "* Night Thrasher",
        "text": "Night Thrasher entre en jeu incliné.\nRiposte 2.\n<b>Réponse</b> : Après avoir retourné une carte que vous contrôlez, redressez Night Thrasher."
    },
    "dt126": {
        "name": "* Rage",
        "text": "Rage entre en jeu incliné.\n[star] Rage gagne +X ATQ, où X est égal au numéro de stade du méchant."
    },
    "dt127": {
        "name": "Souffler ensemble",
        "text": "Max 1 par round.\n<b>Action de héros</b> : Soignez 2 dégâts à chaque ennemi blessé → redressez un personnage allié par ennemi soigné ainsi."
    },
    "dt128": {
        "name": "* Réseau MRVL",
        "text": "Usages (3 pions rediffusion).\n<b>Réponse</b> : Après qu'un ennemi a subi des dégâts pendant la phase du méchant, retirez 1 pion rediffusion d'ici → redressez un personnage que vous contrôlez."
    },
    "dt129": {
        "name": "Conditionnement déterminé",
        "text": "Jouable sous le contrôle de n'importe quel joueur. Max 1 par joueur.\nVous gagnez +3 points de vie, et votre héros gagne -1 DEF et Riposte 1."
    },
    "dt130": {
        "name": "Détonation programmée",
        "text": "Attachez à un ennemi. Max 1 par ennemi.\n<b>Interruption forcée (Héros)</b> <i>(attaque)</i> : Quand la phase du méchant se termine, passez en forme alter-ego et retirez Détonation programmée de la partie → infligez 6 dégâts à l'ennemi attaché. Cette attaque gagne À Distance et Déferlement."
    },
    "dt131": {
        "name": "* Speedball",
        "text": "Speedball entre en jeu incliné.\n<b>Réponse</b> : Après avoir redressé Speedball, placez 1 pion balle sur lui (jusqu'à un maximum de 2). Réduisez de 1 par pion balle sur lui le montant des dégâts que Speedball subit des attaques ennemies."
    },
    "dt132": {
        "name": "Énergie enragée",
        "text": "Doublez le nombre de ressources générées par cette carte tant que les points de vie restants de votre héros sont inférieurs à la moitié de ses points de vie de départ."
    },
    "dt133": {
        "name": "* Orka",
        "text": "Augmentez de 1 le coût pour jouer cette carte si vous ne contrôlez aucun personnage HERO FOR HIRE.\n[star] Orka gagne +1 ATQ par personnage ayant le mot-clé fragile que vous contrôlez ou avec lequel vous êtes engagé."
    },
    "dt134": {
        "name": "* Paladin",
        "text": "Perfide.\n[star] <b>Interruption forcée</b> : Quand Paladin attaque un ennemi portant 1 amélioration Détermination <i>(violette)</i> ou plus, donnez-lui 1 carte de boost supplémentaire pour cette attaque."
    },
    "dt135": {
        "name": "* Tarantula",
        "text": "Fragile. Tarantula gagne une icône [boost] par jeton de dégât sur elle.\n<b>Réponse forcée</b> : Après que Tarantula a contré une manigance annexe ou attaqué un sbire sans le vaincre exactement, elle subit 1 dégât conséquent supplémentaire."
    },
    "dt136": {
        "name": "Exploiter les entraves",
        "text": "[star] Remise 1 (MARTIAL ARTIST).\n<b>Action de héros</b> <i>(attaque)</i> : Infligez 2 dégâts à un ennemi. Infligez-lui 1 dégât supplémentaire par carte qui lui est attachée. Si cette attaque vainc exactement cet ennemi, soignez 2 dégâts à votre identité."
    },
    "dt137": {
        "name": "Action calculée",
        "text": "<b>Action de héros</b> <i>(attaque/contre)</i> : Infligez X dégâts à un ennemi et retirez Y menaces d'une manigance, où le total de X + Y est égal à 6. Si une carte a été vaincue exactement ainsi, redressez votre héros. Sinon, subissez 1 dégât."
    },
    "dt138": {
        "name": "Évalué pour ses faiblesses",
        "text": "Attachez à un sbire.\nLe sbire attaché gagne fragile.\n<b>Interruption</b> : Quand vous vous apprêtez à infliger des dégâts au sbire attaché, choisissez d'augmenter ou de diminuer ce montant de 1."
    },
    "dt139": {
        "name": "Déconcerté",
        "text": "[star] Si les points de vie qu'il vous reste sont inférieurs à la moitié de vos points de vie maximum, réduisez de 1 le coût de cette carte.\nAttachez à un allié ou à un sbire non-ELITE.\nTraitez la boîte de texte imprimée du personnage attaché comme vierge <i>(sauf les TRAITS)</i>."
    },
    "dt140": {
        "name": "Voie de la Miséricorde",
        "text": "Jouable sous le contrôle de n'importe quel joueur. Max 1 carte ETHOS par joueur.\n<b>Réponse de héros</b> : Après avoir attaqué un sbire, s'il lui reste exactement 1 point de vie, piochez 1 carte. Ensuite, si vous êtes le seul joueur de cette partie, défaussez ce sbire."
    },
    "dt141": {
        "name": "Voie de la Pénitence",
        "text": "Jouable sous le contrôle de n'importe quel joueur. Max 1 carte ETHOS par joueur.\n<b>Réponse de héros</b> : Après avoir attaqué un sbire, si cette attaque a infligé des dégâts excédentaires, subissez ce montant de dégâts → choisissez un joueur qui pioche 1 carte par dégât subi ainsi. <i>(Limite d'une fois par joueur et par sbire.)</i>"
    },
    "dt142": {
        "name": "Voie de la Tempérance",
        "text": "Jouable sous le contrôle de n'importe quel joueur. Max 1 carte ETHOS par joueur.\n<b>Réponse de héros</b> : Après avoir attaqué un sbire, si cette attaque a vaincu exactement ce sbire, chaque joueur peut défausser 1 carte de sa main et piocher 1 carte."
    }
};

/** La carte, traduite si l'interface est en francais ET si on a sa traduction.
 *  Sinon la carte d'origine, telle quelle. */
export function carteFr(carte) {
    if (!carte || langueActuelle() !== "fr") return carte;
    const fr = CARTES_FR[carte.card_id || carte.id];
    if (!fr) return carte;
    return { ...carte, name: fr.name, text: fr.text };
}

/** Le nom francais, ou le nom d'origine. Rend une CHAINE : a utiliser quand la
 *  carte est une instance de classe (cards.get()), que `carteFr` copierait a
 *  plat en lui faisant perdre ses methodes. */
export function nomFr(carte) {
    if (!carte || langueActuelle() !== "fr") return carte ? carte.name : "";
    const fr = CARTES_FR[carte.card_id || carte.id];
    return fr ? fr.name : carte.name;
}

/** Le texte francais, ou le texte d'origine. Meme precaution que `nomFr`. */
export function texteFr(carte) {
    if (!carte || langueActuelle() !== "fr") return carte ? carte.text : "";
    const fr = CARTES_FR[carte.card_id || carte.id];
    return fr ? fr.text : carte.text;
}

export { CARTES_FR };

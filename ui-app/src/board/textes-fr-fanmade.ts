// textes-fr-fanmade.ts — texte francais des cartes des packs fan-made.
//
// ECRIT A LA MAIN, ne pas confondre avec textes-fr.ts qui est GENERE depuis
// marvelcdb : ces cartes n'existent que dans ce projet, aucune source en ligne
// ne les connait et aucun scan francais n'existera jamais pour elles. C'est
// donc le seul francais que le joueur verra sur ces cartes.
//
// Conventions suivies, alignees sur la traduction officielle FFG/Asmodee :
//  - les mots-cles suivent mots-cles.ts (Renfort, Deferlement, Robuste...) ;
//  - les statistiques s'ecrivent ATQ, CTR, DEF, REC, MNG ;
//  - les NOMS PROPRES restent en anglais (cartes, personnages, traits [[...]]),
//    parce que le joueur a la carte anglaise sous les yeux et doit s'y
//    retrouver ;
//  - les jetons de jeu ([mental], [star], [per_hero]...) sont recopies tels
//    quels : ce sont des icones, pas du texte.
//
// Une carte absente d'ici n'affiche rien, ce qui est le comportement normal.
export const TEXTES_FR_FANMADE: Readonly<Record<string, string | undefined>> = {
  // rainy — Thor (Hero)
  '61001a': "Digne — <b>Action</b> : cherchez l'amélioration Mjolnir dans votre deck et votre pile de défausse, et ajoutez-la à votre main. Mélangez votre deck. (Limite d'une fois par round.)",
  // rainy — Jane Foster (AlterEgo)
  '61001b': "Survivante — Jane Foster gagne +1 en taille de main tant que son obligation Chimiothérapie est mise de côté ou retirée de la partie.\nMédecin — <b>Action</b> : soignez 1 dégât d'un autre personnage allié. (Limite d'une fois par round.)",
  // rainy — Odinson (Ally)
  '61002': "Multivers.\n[star] <b>Réponse</b> : après qu'Odinson a attaqué, choisissez un joueur. Infligez 1 dégât à chaque sbire engagé avec ce joueur.",
  // rainy — Roz Solomon (Ally)
  '61003': "[star] <b>Interruption</b> : quand Roz Solomon contre, inclinez Congress of Worlds ou une carte [[S.H.I.E.L.D]] que vous contrôlez → elle gagne +2 CTR pour cette utilisation.",
  // rainy — Hammer Swing (Event)
  '61004': "<b>Action de héros</b> <i>(attaque)</i> : inclinez Mjolnir et dépensez 1 ressource de n'importe quel type → infligez 4 dégâts à un ennemi.\n<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, inclinez Mjolnir → prévenez tous ces dégâts.",
  // rainy — Lightning Strike (Event)
  '61005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 6 dégâts à un ennemi et 1 dégât à chaque ennemi engagé avec vous. Si vous avez payé cette carte en n'utilisant que des ressources [energy], sonnez un ennemi.",
  // rainy — Stand Fast (Event)
  '61006': "<b>Action de héros</b> : redressez Thor et Mjolnir. Si vous avez payé cette carte en n'utilisant que des ressources [energy], donnez une carte d'état Tenace à Thor.",
  // rainy — Mjolnir (Upgrade)
  '61007': "Restreint.\nThor gagne +1 ATQ et le trait [[AERIAL]].\n<b>Action de héros</b> <i>(attaque)</i> : défaussez Mjolnir → infligez 2 dégâts à un ennemi. Cette attaque gagne à distance.",
  // rainy — Unyielding (Upgrade)
  '61008': "<b>Réponse de héros</b> <i>(contre)</i> : après avoir été attaqué sans subir de dégâts, inclinez Unyielding → retirez 2 menaces d'une manigance. Vous pouvez dépenser 1 ressource de n'importe quel type pour redresser votre héros.",
  // rainy — Congress of Worlds (Support)
  '61009': "<b>Action d'identité civile</b> : inclinez Congress of Worlds et dépensez 1 ressource de n'importe quel type → retirez 2 menaces de la manigance principale ou 3 menaces d'une manigance annexe.",
  // rainy — Medical Clinic (Support)
  '61010': "Jane Foster gagne +2 REC.\n<b>Action d'identité civile</b> : inclinez Medical Clinic et dépensez 1 ressource → soignez 3 dégâts d'une identité.",
  // rainy — Scrying Pool (Support)
  '61011': "<b>Action de héros</b> : inclinez Scrying Pool → regardez la carte du dessus d'un deck. Vous pouvez défausser cette carte. Si une traîtrise a été regardée de cette façon, retirez 1 menace d'une manigance. Si un événement a été regardé de cette façon depuis un deck de joueur, ce joueur pioche 1 carte.",
  // rainy — Goddess of Thunder (Upgrade)
  '61012': "<b>Ressource de héros</b> : inclinez Goddess of Thunder → générez une ressource [energy], ou [energy][energy] à la place pour une carte Thor.",
  // rainy — Mighty (Upgrade)
  '61013': "Vous gagnez +2 points de vie.\nThor gagne +1 DEF et riposte 1.",
  // rainy — Chemotherapy (Obligation)
  '61026': "Donnez-la au joueur Jane Foster.\nPassez en forme d'identité civile. Choisissez :\n- Inclinez Jane Foster et Medical Clinic → retirez Chimiothérapie de la partie.\n- Choisissez soit de défausser 2 cartes, soit de subir 2 dégâts. Défaussez cette obligation.",
  // rainy — War of the Realms (SideScheme)
  '61027': "<b>Une fois révélée</b> : chaque joueur subit 1 dégât indirect par personnage qu'il contrôle.",
  // rainy — Malekith (Minion)
  '61028': "[star] <b>Réponse Obligatoire</b> : après que Malekith s'est activé, chaque joueur subit 1 dégât indirect.",
  // rainy — War Witches (Minion)
  '61029': "[star] <b>Interruption Obligatoire</b> : quand War Witches devraient attaquer, elles manigancent à la place.\n<b>Réponse Obligatoire</b> : après que de la menace a été placée sur la manigance principale, le joueur engagé subit 1 dégât indirect.",
  // rainy — Execute (Treachery)
  '61030': "<b>Une fois révélée</b> : mettez K.O. l'allié en jeu ayant le plus de points de vie restants. Si aucun allié n'a été mis K.O. de cette façon, cette carte gagne renfort.",
  // rainy — Hostile Takeover (Treachery)
  '61031': "<b>Une fois révélée</b> : choisissez soit de défausser le soutien que vous contrôlez ayant le coût le plus élevé, soit de subir un nombre de dégâts égal à son coût (ces dégâts ignorent les cartes d'état Tenace). Si aucun soutien n'a été défaussé et qu'aucun dégât n'a été subi de cette façon, cette carte gagne renfort.",
  // albert — Albert (Hero)
  '62001a': "<i>Protocole d'initialisation</i> — <b>Spéciale</b> : piochez 1 carte. Après avoir joué cette carte ce round, redressez Albert.\n<b>Action</b> : résolvez la capacité \"<i>Protocole d'initialisation</i>\" d'Albert. (Limite d'une fois par round.)",
  // albert — Albert (AlterEgo)
  '62001b': "<i>Développement poussé</i> — <b>Mise en place</b> : cherchez une amélioration [[Enhancement]] dans votre deck et votre pile de défausse, et mettez-la en jeu.",
  // albert — Elsie-Dee (Ally)
  '62002': "<b>Interruption</b> : quand Elsie-Dee devrait être mise K.O. en subissant des dégâts en excès, répartissez X dégâts entre les ennemis en jeu, où X est égal à l'excédent.",
  // albert — Guard Protocol (Event)
  '62003': "<b>Action de héros</b> : jusqu'à la fin du round, Albert gagne riposte 1 tant qu'il est en forme de héros. Donnez une carte d'état Tenace à Albert. S'il en a déjà une, résolvez la capacité \"<i>Protocole d'initialisation</i>\" d'Albert.",
  // albert — Lethal Directive (Event)
  '62004': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Si cet ennemi est mis K.O. par cette attaque, résolvez la capacité \"<i>Protocole d'initialisation</i>\" d'Albert.",
  // albert — Sabotage Sequence (Event)
  '62005': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Si ce contre retire la dernière menace de cette manigance, résolvez la capacité \"<i>Protocole d'initialisation</i>\" d'Albert.",
  // albert — System Relaunch (Event)
  '62006': "<b>Action d'identité civile</b> : soignez un nombre de dégâts d'Albert égal à votre REC et passez en forme de héros → résolvez la capacité \"<i>Protocole d'initialisation</i>\" d'Albert.",
  // albert — Donald Pierce (Support)
  '62007': "<b>Ressource</b> : inclinez Donald Pierce → générez une ressource [wild].\n<b>Réponse</b> : après avoir résolu la capacité \"<i>Protocole d'initialisation</i>\" d'Albert, redressez cette carte.",
  // albert — Adamantium Claws (Upgrade)
  '62008': "Tant qu'il est en forme de héros, Albert gagne +1 ATQ et ses attaques de base gagnent perçant.",
  // albert — Genius-Level Intellect (Upgrade)
  '62009': "Vous gagnez le trait [[Genius]].\nTant qu'il est en forme de héros, Albert gagne +1 CTR.",
  // albert — Kevlar Shell (Upgrade)
  '62010': "Tant qu'il est en forme de héros, Albert gagne +1 DEF et riposte 1.",
  // albert — Counterpart Elimination (Obligation)
  '62011': "Donnez-la au joueur Albert.\nVous ne pouvez pas résoudre la capacité \"<i>Protocole d'initialisation</i>\" d'Albert.\n<b>Une fois révélée</b> : trouvez un sbire [[Wolverine]] et révélez-le.\n<b>Réponse</b> : après qu'un sbire [[Wolverine]] a été mis K.O., défaussez cette carte.",
  // albert — Wolverine (Minion)
  '62012': "<b>Réponse Obligatoire</b> : après que vous avez attaqué Wolverine, soignez 1 dégât de ce dernier.\n<i>(Sbire nemesis d'Albert.)</i>\n[star] <b>Boost</b> : mettez ce sbire en jeu, engagé avec le joueur Albert.",
  // albert — Crack in the Multiverse (SideScheme)
  '62013': "Entrave 2[per_hero].\n<b>Réponse Obligatoire</b> : après la fin de la phase des joueurs, le premier joueur trouve un sbire [[Wolverine]] et le révèle.",
  // albert — Patch (Minion)
  '62014': "Riposte 1.\n<b>Une fois révélée</b> : infligez 1 dégât à chaque joueur.",
  // albert — Weapon X (Minion)
  '62015': "Coup Rapide.\n<b>Une fois révélée</b> : défaussez 1 carte au hasard de votre main.",
  // albert — Zombie Wolvie (Minion)
  '62016': "<b>Quand vaincu</b> : mélangez Zombie Wolvie dans le deck rencontre.",
  // gwenpool — Gwenpool (Hero)
  '63001a': "<i>Conscience du support</i> — <b>Interruption</b> : quand vous résolvez une capacité d'une carte Gwenpool, remplacez \"____\" par une phrase issue d'une bulle de dialogue. (Utilisez les bulles d'une carte que vous jouez, d'une carte que vous dépensez, ou d'une carte en jeu.) (Limite de chaque bulle une fois par phase.)\n<i>Bulle de dialogue : « Piochez 1 carte. »</i>",
  // gwenpool — Gwendolyn Poole (AlterEgo)
  '63001b': "<i>« Je ne serai pas une figurante »</i> — <b>Action</b> : trouvez une carte Gwenpool et ajoutez-la à votre main. (Limite d'une fois par phase.)",
  // gwenpool — "Here I Come!" (Event)
  '63002': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Cette attaque gagne déferlement. Si cette attaque met un ennemi K.O., ____.\n<i>Bulle de dialogue : « Infligez 2 dégâts au méchant. »</i>",
  // gwenpool — "It Can't End Like This!" (Event)
  '63003': "<b>Action de héros</b> <i>(attaque/contre)</i> : infligez 1 dégât au méchant et retirez 1 menace de la manigance principale. Si le méchant a manigancé au round précédent, ____.\n<i>Bulle de dialogue : « Désorientez le méchant. »</i>",
  // gwenpool — Fun Background Noise (Event)
  '63004': "<b>Interruption de héros</b> : quand une carte de traîtrise est révélée depuis le deck rencontre, annulez ses effets \"<b>Une fois révélée</b>\" et défaussez-la. Puis, ____.\n<i>Bulle de dialogue : « Donnez une carte d'état Tenace à Gwenpool. »</i>",
  // gwenpool — "Sorry, Gotta Run!" (Event)
  '63005': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance. Ce contre ignore le mot-clé patrouille et les icônes de crise. Si ce contre déjoue une manigance, ____.\n<i>Bulle de dialogue : « Retirez 2 menaces de la manigance principale. »</i>",
  // gwenpool — Endless Storylines (Resource)
  '63006': "<b>Réponse de héros</b> : après avoir dépensé cette carte, ____ et ____.\n<i>Bulles de dialogue : « Retirez 1 menace d'une manigance. » / « Soignez 1 dégât de Gwenpool. » / « Infligez 1 dégât à un ennemi. »</i>",
  // gwenpool — Gwen's Room (Support)
  '63007': "Vous gagnez +1 REC.\n<b>Action d'identité civile</b> : inclinez Gwen's Room → soignez 1 dégât de Gwendolyn Poole. Puis, trouvez Unbelievable Gwenpool et ajoutez-la à votre main.\n<i>Bulle de dialogue : « Soignez 1 dégât de Gwenpool. »</i>",
  // gwenpool — Comicbook Panels (Upgrade)
  '63008': "<b>Ressource de héros</b> : inclinez Comicbook Panels → générez une ressource [wild] et ____.\n<b>Action de héros</b> : inclinez Comicbook Panels et Unbelievable Gwenpool → ____ et ____.\n<i>Bulle de dialogue : « Regardez la carte du dessus de n'importe quel deck. »</i>",
  // gwenpool — Unbelievable Gwenpool (Upgrade)
  '63009': "<b>Action d'identité civile</b> : inclinez Unbelievable Gwenpool → cherchez une carte Gwenpool dans votre deck et attachez-la ici face visible (maximum 1). <i>(Mélangez.)</i> Vous pouvez utiliser les bulles de dialogue de la carte attachée.\n<b>Action de héros</b> : piochez 2 cartes et ____. Défaussez Unbelievable Gwenpool.\n<i>Bulle de dialogue : « Redressez Gwenpool. »</i>",
  // gwenpool — THE END (Obligation)
  '63010': "Donnez-la au joueur Gwendolyn Poole.\nVous ne pouvez pas utiliser les bulles de dialogue des cartes Gwenpool.\n<b>Action d'identité civile</b> : inclinez Gwendolyn Poole et défaussez Unbelievable Gwenpool → retirez THE END de la partie.",
  // gwenpool — Rules of the Universe (SideScheme)
  '63011': "Permanent.\nTant qu'il n'y a pas de menace ici, cette manigance perd l'icône [hazard].\n<b>Interruption Obligatoire</b> : quand vous résolvez une capacité d'une carte Gwenpool, remplacez \"____\" par la phrase de la bulle de dialogue d'Evil Gwenpool.",
  // gwenpool — Evil Gwenpool (Minion)
  '63012': "Solide. Vilenie.\n<b>Quand vaincue</b> : mélangez Evil Gwenpool dans le deck rencontre.\n<i>(Sbire nemesis de Gwenpool.)</i>\n[star] <b>Boost</b> : mettez Evil Gwenpool en jeu, engagée avec vous.\n<i>Bulle de dialogue : « Gwenpool subit 1 dégât. »</i>",
  // gwenpool — Break Reality (Treachery)
  '63013': "Incitation 1.\n<b>Une fois révélée</b> : cherchez Evil Gwenpool dans le deck rencontre et révélez-la. <i>(Mélangez.)</i> Si Unbelievable Gwenpool est en jeu, elle gagne coup rapide. Si Evil Gwenpool était déjà en jeu, ajoutez 2[per_hero] menaces sur Rules of the Universe.",
  // gwenpool — "Future Me Scares Me" (Treachery)
  '63014': "Incitation 0 (incitation 1 à la place, s'il s'agit d'une partie multijoueur).\nIncitation 1 (incitation 2 à la place, s'il s'agit d'une partie en mode expert).\n<b>Une fois révélée</b> : si Evil Gwenpool est en jeu, ajoutez 2 menaces sur Rules of the Universe et mélangez cette carte dans le deck rencontre.",
  // human_torch — Human Torch (Hero)
  '64001a': "<i>Flamme à volonté !</i> — <b>Interruption</b> : quand vous placez un compteur de flamme sur un ennemi, infligez 1 dégât à cet ennemi. Un ennemi ne peut pas avoir plus de 3 compteurs de flamme sur lui.",
  // human_torch — Johnny Storm (AlterEgo)
  '64001b': "<i>Ignition</i> — <b>Action</b> : inclinez Johnny Storm → cherchez une carte [[FIRE]] parmi les 4 cartes du dessus de votre deck et ajoutez-la à votre main. Si aucune carte n'a été ajoutée à votre main de cette façon, redressez Johnny Storm. (Limite d'une fois par round.)",
  // human_torch — The Thing (Ally)
  '64002': "Ténacité.\n<b>Réponse</b> : après que The Thing s'est défendu, redressez-le. (Limite d'une fois par phase.)",
  // human_torch — Johnny's Workshop (Support)
  '64003': "<b>Réponse</b> : après être passé à Johnny Storm, piochez 1 carte.\n<b>Réponse</b> : après être passé à Human Torch, redressez une carte [[FIRE]].",
  // human_torch — Unstable Uniform (Upgrade)
  '64004': "Human Torch gagne +1 DEF.\n<b>Réponse de héros</b> : après avoir subi des dégâts d'une attaque, placez un compteur de flamme sur l'attaquant.",
  // human_torch — Internal Combustion (Upgrade)
  '64005': "<b>Action de héros</b> : retirez 3 compteurs de flamme d'un ennemi et défaussez Internal Combustion → piochez 3 cartes.",
  // human_torch — Spark (Upgrade)
  '64006': "<b>Ressource de héros</b> : inclinez Spark → générez une ressource [energy] pour une carte [[FIRE]].\n<b>Action de héros</b> : inclinez Spark → placez un compteur de flamme sur un ennemi.",
  // human_torch — Fly-By (Event)
  '64007': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance, puis retirez 1 menace d'une manigance par compteur de flamme sur le méchant.",
  // human_torch — Blaze and Daze (Event)
  '64008': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Puis, s'il a 3 compteurs de flamme sur lui, retirez tous ces compteurs et sonnez cet ennemi.",
  // human_torch — Radiate (Event)
  '64009': "Choisissez l'un ou l'autre :\n<b>Action de héros</b> <i>(attaque)</i> : placez 2 compteurs de flamme sur X ennemis.\n<b>Action</b> : retirez tous les compteurs de flamme de X ennemis → changez de forme, puis soignez 1 dégât par compteur de flamme retiré de cette façon (maximum 5).",
  // human_torch — Nova Flame (Event)
  '64010': "<b>Action de héros</b> <i>(attaque)</i> : inclinez Human Torch → placez jusqu'à 3 compteurs de flamme sur un ennemi, puis infligez 7 dégâts à cet ennemi. Cette attaque gagne déferlement.",
  // human_torch — Flame Off (Obligation)
  '64011': "Donnez-la au joueur Johnny Storm.\nPassez en forme d'identité civile et retirez tous les compteurs de flamme des ennemis en jeu. Puis :\n- Si jusqu'à 3 compteurs ont été retirés de cette façon, défaussez cette obligation.\n- Si 4 compteurs de flamme ou plus ont été retirés de cette façon, retirez Flame Off de la partie.",
  // human_torch — Hydro-Man (Minion)
  '64012': "Aucun compteur de flamme ne peut être placé sur Hydro-Man.\n[star] <b>Boost</b> : mettez Hydro-Man en jeu, engagé avec vous.",
  // human_torch — Dam It (SideScheme)
  '64013': "Hydro-Man est apparu et a éteint toutes les flammes !\n<b>Une fois révélée</b> : retirez tous les compteurs de flamme des ennemis en jeu. Puis, placez 1 menace supplémentaire ici par compteur de flamme retiré de cette façon.",
  // human_torch — Tidal Surge (Treachery)
  '64014': "Renfort.\n<b>Une fois révélée</b> : si Hydro-Man est en jeu, chaque joueur doit choisir soit d'incliner son identité, soit de subir 3 dégâts indirects.",
  // mister_fantastic — Mister Fantastic (Hero)
  '65001a': "<i>Flexibilité</i> — <b>Réponse</b> : après avoir dépensé une carte [[SUPERPOWER]] comme ressource ou l'avoir défaussée de votre main sans la jouer, renvoyez-la dans votre main. (Limite d'une fois par phase.)",
  // mister_fantastic — Reed Richards (AlterEgo)
  '65001b': "<i>Grands esprits</i> — <b>Ressource</b> : inclinez Reed Richards → générez une ressource [mental] ([mental][mental] à la place si Sue Storm est en jeu). Si vous avez payé une carte [[TECH]] avec les ressources de cette capacité, redressez Reed Richards. (Limite d'une fois par round.)",
  // mister_fantastic — Invisible Woman (Ally)
  '65002': "<b>Réponse</b> : après qu'Invisible Woman est entrée en jeu, redressez votre identité.",
  // mister_fantastic — H.E.R.B.I.E. (Support)
  '65003': "<b>Action</b> : inclinez H.E.R.B.I.E. → défaussez X cartes de votre main, puis piochez X cartes.\n<b>Action</b> : inclinez puis défaussez H.E.R.B.I.E. → piochez X cartes, puis défaussez X cartes de votre main.",
  // mister_fantastic — Baxter Building (Support)
  '65004': "<b>Action d'identité civile</b> : inclinez Baxter Building → soignez 2 dégâts d'une identité.\n<b>Action de héros</b> : inclinez Baxter Building → cherchez une carte Mister Fantastic parmi les 4 cartes du dessus de votre deck, puis ajoutez-la à votre main (les 8 premières à la place si votre héros a 10 points de vie restants ou plus).",
  // mister_fantastic — Fantasticar (Support)
  '65005': "Mister Fantastic gagne +1 en taille de main.\n<b>Action de héros</b> : inclinez Fantasticar → choisissez un joueur en forme de héros. Réduisez de 1 le coût de la prochaine carte d'événement que ce joueur joue durant cette phase.",
  // mister_fantastic — Unstable Uniform (Upgrade)
  '65006': "Mister Fantastic gagne +1 DEF.\n<b>Réponse de héros</b> : après vous être défendu contre une attaque, renvoyez dans votre main la carte Mister Fantastic la plus profonde de votre pile de défausse.",
  // mister_fantastic — Fantasti-Flare (Upgrade)
  '65007': "Utilisations (4 compteurs de flare).\n<b>Action</b> : inclinez Fantasti-Flare et retirez-lui un compteur de flare → choisissez un joueur. Réduisez de 1 le coût du prochain allié que ce joueur joue durant cette phase.",
  // mister_fantastic — Neutralizer (Upgrade)
  '65008': "Jouez-la sous le contrôle de n'importe quel joueur. Restreint. Utilisations (2 compteurs de charge).\n<b>Interruption de héros</b> : quand vous faites une attaque de base, inclinez Neutralizer et retirez-lui un compteur de charge → vous gagnez +3 ATQ pour cette attaque. Cette attaque gagne déferlement.",
  // mister_fantastic — Stretched Thin (Event)
  '65009': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance. Puis, s'il ne vous reste aucune carte en main, retirez 1 menace de chaque manigance en jeu.",
  // mister_fantastic — Big Reach (Event)
  '65010': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts au méchant. Puis, infligez X dégâts à un ennemi, où X est le nombre de cartes qu'il vous reste en main.",
  // mister_fantastic — Slippery (Event)
  '65011': "<b>Interruption</b> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, prévenez 2 de ces dégâts et piochez 2 cartes.",
  // mister_fantastic — Mental Gymnastics (Event)
  '65012': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 + X dégâts à un ennemi. Puis, s'il ne vous reste aucune carte en main, désorientez cet ennemi.",
  // mister_fantastic — Ben's Cure (Obligation)
  '65013': "Donnez-la au joueur Reed Richards.\nVous pouvez passer en forme d'identité civile. Choisissez :\n- Inclinez Reed Richards et défaussez une carte ayant une ressource [mental] imprimée → retirez Ben's Cure de la partie.\n- Subissez 1 dégât et placez 1 menace sur la manigance principale → défaussez cette obligation.",
  // mister_fantastic — Wizard (Minion)
  '65014': "Chaque héros subit -1 CTR.",
  // mister_fantastic — Hubris (SideScheme)
  '65015': "Wizard a un plan machiavélique en tête.\n<b>Une fois révélée</b> : placez X menaces supplémentaires ici, où X est le CTR cumulé de tous les héros.",
  // mister_fantastic — Projection (Attachment)
  '65016': "Incitation 1. Renfort.\nAttachez-la à votre carte d'identité.\n[star] <b>Boost</b> : attachez-la à votre carte d'identité.",
  // mister_fantastic — Execution (Treachery)
  '65017': "<b>Une fois révélée</b> : défaussez chaque attachement Projection en jeu. Pour chaque attachement défaussé de cette façon, chaque joueur doit choisir soit de défausser 2 cartes de sa main, soit de subir 2 dégâts indirects. Si aucun attachement Projection n'a été défaussé de cette façon, remélangez Execution dans le deck rencontre et cette carte gagne renfort.",
  // invisible_woman — Invisible Woman (Hero)
  '66001a': "<i>Bouh !</i> — <b>Réponse Obligatoire</b> : après avoir attaqué un ennemi, passez à votre autre forme de héros.",
  // invisible_woman — Sue Storm (AlterEgo)
  '66001b': "<i>Grands esprits</i> — <b>Ressource</b> : inclinez Sue Storm → générez une ressource [mental] ([mental][mental] à la place si Reed Richards est en jeu). Si vous avez payé une carte [[TECH]] avec les ressources de cette capacité, redressez Sue Storm. (Limite d'une fois par round.)",
  // invisible_woman — Invisible Woman (Hero)
  '66001c': "<i>Barrière invisible</i> — <b>Interruption</b> : quand un ennemi ayant 2 ATQ ou plus initie une attaque contre vous, infligez 1 dégât à cet ennemi.",
  // invisible_woman — Mister Fantastic (Ally)
  '66002': "<b>Réponse</b> : après que Mister Fantastic est entré en jeu, retirez 1 menace de chaque manigance ou ajoutez la carte du dessus de votre pile de défausse à votre main.",
  // invisible_woman — Central City Estate (Support)
  '66003': "Vous gagnez +1 REC.\n<b>Action d'identité civile</b> : inclinez Central City Estate → redressez Sue Storm.",
  // invisible_woman — Unstable Uniform (Upgrade)
  '66004': "Invisible Woman gagne +1 DEF.\n<b>Réponse de héros</b> : après être passé en forme de héros [[INVISIBLE]], vous gagnez +1 CTR jusqu'à la fin de ce tour.\n<b>Réponse de héros</b> : après être passé en forme de héros [[PSIONIC]], vous gagnez +1 ATQ jusqu'à la fin de ce tour.",
  // invisible_woman — Flying Disk (Upgrade)
  '66005': "Si vous êtes en forme de héros [[PSIONIC]], vous gagnez le trait [[AERIAL]] et vos attaques gagnent à distance.\n<b>Action de héros</b> : défaussez Flying Disk → infligez 4 dégâts à un ennemi.",
  // invisible_woman — Vanishing Act (Upgrade)
  '66006': "<b>Action de héros</b> : si vous êtes en forme de héros [[INVISIBLE]], inclinez Vanishing Act et dépensez des ressources [mental][energy] → désorientez un ennemi.",
  // invisible_woman — Force Shields (Upgrade)
  '66007': "<b>Action de héros</b> : si vous êtes en forme de héros [[PSIONIC]], inclinez Force Shields et défaussez X cartes ayant une ressource [physical] imprimée → donnez une carte d'état Tenace à X personnages alliés.",
  // invisible_woman — Incognito (Event)
  '66008': "Jouez-la uniquement si vous êtes en forme de héros [[INVISIBLE]].\n<b>Action de héros</b> : regardez les 4 cartes du dessus du deck rencontre. Pour chaque icône étoile vue de cette façon, piochez 1 carte.",
  // invisible_woman — Infiltrate (Event)
  '66009': "Jouez-la uniquement si vous êtes en forme de héros [[INVISIBLE]].\n<b>Action de héros</b> <i>(contre)</i> : retirez jusqu'à 4 menaces d'une manigance ou jusqu'à 2 menaces de chaque manigance.",
  // invisible_woman — Forceful (Event)
  '66010': "Jouez-la uniquement si vous êtes en forme de héros [[PSIONIC]].\n<b>Action de héros</b> <i>(attaque)</i> : défaussez autant de cartes d'état Tenace que vous le souhaitez des personnages que vous contrôlez → infligez 3 dégâts au méchant par carte d'état Tenace défaussée de cette façon.",
  // invisible_woman — Psionic Fields (Event)
  '66011': "Jouez-la uniquement si vous êtes en forme de héros [[PSIONIC]].\n<b>Action de héros</b> <i>(attaque)</i> : choisissez 2 des options suivantes (vous pouvez choisir deux fois la même) :\n• Infligez 4 dégâts à un ennemi.\n• Sonnez un ennemi.",
  // invisible_woman — Spectral Shift (Event)
  '66012': "<b>Action</b> : changez de forme. Puis, si vous êtes passé :\nen forme de héros [[INVISIBLE]] - Piochez 2 cartes.\nen forme de héros [[PSIONIC]] - Piochez 1 carte.",
  // invisible_woman — Family Time (Obligation)
  '66013': "<b><i>Donnez-la au joueur Sue Storm.</i></b>\nVous pouvez passer en forme d'identité civile. Choisissez :\n• Inclinez Sue Storm → retirez Family Time de la partie.\n• Défaussez une carte de votre main → défaussez cette obligation.",
  // invisible_woman — Psycho-Man (Minion)
  '66014': "<b>Réponse Obligatoire</b> : après que Psycho-Man s'est activé, défaussez 4 cartes du deck rencontre. Si des cartes Nemesis d'Invisible Woman ont été défaussées de cette façon, révélez-les à la place.",
  // invisible_woman — Emotional Masterplan (SideScheme)
  '66015': "Les héros ne peuvent pas changer de forme.\n<b>Action</b> : défaussez 2 cartes de votre main → considérez que la zone de texte imprimée de cette carte est vierge jusqu'à la fin de votre tour.",
  // invisible_woman — Microversal Maneuvers (Attachment)
  '66016': "Attachez-la à Psycho-Man. Si vous ne pouvez pas, cette carte gagne renfort.\n<b>Réponse Obligatoire</b> : après que Psycho-Man a manigancé contre vous, subissez 1 dégât indirect.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // invisible_woman — Titanic Terror (Attachment)
  '66017': "Attachez-la à Psycho-Man. Si vous ne pouvez pas, cette carte gagne renfort.\n<b>Réponse Obligatoire</b> : après que Psycho-Man a attaqué, placez 1 menace sur la manigance principale.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // invisible_woman — End of the Line (Treachery)
  '66018': "<b>Une fois révélée</b> : défaussez les 8 cartes du dessus du deck rencontre. Si Microversal Maneuvers ou Titanic Terror sont défaussées de cette façon, révélez-les.",
  // the_thing — The Thing (Hero)
  '67001a': "<i>Vas-y !</i> — <b>Action</b> : défaussez une carte d'état Tenace de The Thing.\n<i>Prends ça !</i> — <b>Réponse</b> : après avoir défaussé une carte d'état Tenace de The Thing, vos attaques infligent 1 dégât supplémentaire jusqu'à la fin de la phase.",
  // the_thing — Ben Grimm (AlterEgo)
  '67001b': "<i>L'adorable Chose aux yeux bleus</i> — <b>Réponse</b> : après que Ben Grimm a soigné 4 dégâts ou plus, donnez-lui une carte d'état Tenace.",
  // the_thing — The Thing (Hero)
  '67001c': "<i>Vas-y !</i> — <b>Action</b> : défaussez une carte d'état Tenace de The Thing.\n<i>Prends ça !</i> — <b>Réponse</b> : après avoir défaussé une carte d'état Tenace de The Thing, vos attaques infligent 1 dégât supplémentaire jusqu'à la fin de la phase.",
  // the_thing — Ben Grimm (AlterEgo)
  '67001d': "<i>L'adorable Chose aux yeux bleus</i> — <b>Réponse</b> : après que Ben Grimm a soigné 4 dégâts ou plus, donnez-lui une carte d'état Tenace.",
  // the_thing — Human Torch (Ally)
  '67002': "<b>Réponse</b> : après que Human Torch est entré en jeu, choisissez l'un ou l'autre :\n- Infligez 1 dégât à The Thing, puis donnez-lui une carte d'état Tenace.\n- Infligez 3 dégâts au méchant.",
  // the_thing — Alicia Masters (Support)
  '67003': "<b>Action d'identité civile</b> : inclinez Alicia Masters → piochez 2 cartes.",
  // the_thing — Yancy Street Gang (Support)
  '67004': "<b>Action</b> : inclinez Yancy Street Gang → infligez 1 dégât à un personnage. Ces dégâts gagnent perçant. Si une carte d'état Tenace a été défaussée de cette façon, redressez Yancy Street Gang.",
  // the_thing — Unstable Uniform (Upgrade)
  '67005': "The Thing gagne +1 DEF.\n<b>Réponse de héros</b> : après vous être défendu contre une attaque, piochez une carte.",
  // the_thing — Rock 'Em (Event)
  '67006': "<b>Action de héros</b> <i>(contre)</i> : retirez 4 menaces d'une manigance. Si cela retire la dernière menace de cette manigance, donnez une carte d'état Tenace à The Thing ou désorientez le méchant.",
  // the_thing — True Grit (Upgrade)
  '67007': "<b>Action de héros</b> : infligez 2 dégâts à The Thing → redressez votre héros et défaussez-lui une carte d'état. (Maximum une fois par round.)",
  // the_thing — Toughen Up (Event)
  '67008': "<b>Réponse</b> : après avoir subi des dégâts, quel qu'en soit le nombre, donnez une carte d'état Tenace à votre identité.",
  // the_thing — Sock 'Em (Event)
  '67009': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Si cet ennemi est mis K.O. par cette attaque, donnez une carte d'état Tenace à The Thing ou piochez une carte.",
  // the_thing — It's Clobberin' Time! (Event)
  '67010': "<b>Action de héros</b> : faites les 2 attaques suivantes :\n- Infligez 4 dégâts à un ennemi.\n- Infligez 4 dégâts à un ennemi.",
  // the_thing — Annual Shedding (Obligation)
  '67011': "Donnez-la au joueur Ben Grimm.\nPassez en forme d'identité civile. Choisissez l'un ou l'autre :\n- Défaussez une carte d'état Tenace de Ben Grimm → défaussez cette obligation.\n- Sonnez ou désorientez Ben Grimm → défaussez cette obligation.",
  // the_thing — Puppet Master (Minion)
  '67012': "Puppet Master ne peut pas être attaqué tant que Hulk est en jeu.\n<b>Réponse Obligatoire</b> : après que Puppet Master a été révélé, cherchez Hulk dans le deck rencontre et révélez-le.\n<i>(Sbire nemesis de The Thing.)</i>",
  // the_thing — Pulling The Strings (SideScheme)
  '67013': "Le beau-père malgré lui de Ben Grimm a pris le contrôle de l'Incroyable Hulk !\nLe sbire en jeu ayant le MNG le plus faible gagne +1 ATQ et +1 MNG.",
  // the_thing — Hulk (Minion)
  '67014': "Garde.\n[star] Les attaques de Hulk gagnent perçant et déferlement.",
  // the_thing — Friendly Fire (Treachery)
  '67015': "<b>Une fois révélée</b> : vous subissez X dégâts, où X est l'ATQ du personnage allié ayant l'ATQ la plus élevée. Si votre identité est le seul personnage allié en jeu, cette carte gagne renfort.",
  // totally_awesome_hulk — Totally Awesome Hulk (Hero)
  '68001a': "<i>Perte de contrôle</i> — Vous ne pouvez passer en forme de héros [[BRUTE]] qu'en résolvant les effets du soutien \"The Trunk\".\n<i>Hyper-esprit</i> — Considérez toutes les ressources que vous générez comme des ressources [wild].",
  // totally_awesome_hulk — Amadeus Cho (AlterEgo)
  '68001b': "<i>Rétro-ingénierie</i> — <b>Action</b> : défaussez une carte spécifique à votre héros de votre main → piochez X cartes, où X est le coût imprimé de la carte défaussée de cette façon. (Limite d'une fois par round.)",
  // totally_awesome_hulk — Uncontrollable Hulk (Hero)
  '68001c': "<i>Incontrôlable</i> — Vous ne pouvez ni prendre ni quitter cette forme sans résoudre les effets du soutien \"The Trunk\".\n<b>Interruption</b> : quand vous attaquez, cette attaque inflige 2 dégâts supplémentaires.",
  // totally_awesome_hulk — Hercules (Ally)
  '68002': "<b>Réponse</b> : après qu'Hercules a mis un sbire K.O., redressez-le.",
  // totally_awesome_hulk — Maddy Cho (Support)
  '68003': "Totally Awesome Hulk gagne +1 en taille de main.\n<b>Action de héros</b> : inclinez Maddy Cho → ajoutez ou retirez 1 compteur de rage sur \"The Trunk\".",
  // totally_awesome_hulk — Kegger (Upgrade)
  '68004': "<b>Ressource</b> : mélangez Kegger dans votre deck → générez une ressource [wild].\n<b>Action</b> : mélangez Kegger et une carte de votre main dans votre deck → redressez votre identité.",
  // totally_awesome_hulk — Motivation (Upgrade)
  '68005': "Votre héros gagne +1 DEF.\n<b>Réponse de héros</b> : après que votre héros s'est défendu, subissez 2 dégâts → redressez votre héros.",
  // totally_awesome_hulk — Gamma Barrier (Upgrade)
  '68006': "Votre héros gagne riposte 1.\n<b>Interruption</b> : quand vous devriez être sonné, défaussez cette carte → prévenez ce sonnage et sonnez le méchant à la place.",
  // totally_awesome_hulk — The Power of Forgiveness (Resource)
  '68007': "<b>Réponse</b> : après avoir résolu les effets de la carte payée avec The Power of Forgiveness, retirez tous les compteurs de \"The Trunk\" et soignez 2 points de vie d'un autre personnage allié.",
  // totally_awesome_hulk — Calculated Strike (Event)
  '68008': "<b>Action de héros</b> <i>(attaque/contre)</i> : retirez 2 menaces d'une manigance, puis infligez 3 dégâts au méchant. Si vous avez payé cette carte en n'utilisant que des ressources [wild], retirez 2 menaces supplémentaires.",
  // totally_awesome_hulk — Wild Lunge (Event)
  '68009': "Vous ne pouvez dépenser que des ressources [wild] pour payer cette carte.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi.",
  // totally_awesome_hulk — Irradiated Swipe (Event)
  '68010': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Si vous avez payé cette carte en n'utilisant que des ressources [wild], piochez 2 cartes.",
  // totally_awesome_hulk — Kinetic Stomp (Event)
  '68011': "<b>Interruption de héros</b> : quand vous faites une attaque de base, vous gagnez +6 ATQ pour cette attaque. Si cette attaque inflige 10 dégâts ou plus, redressez votre héros.",
  // totally_awesome_hulk — "The Trunk" (Support)
  '68012a': "<b>Réponse Obligatoire</b> : après que Totally Awesome Hulk a subi des dégâts, quel qu'en soit le nombre, ajoutez un compteur de rage ici.\n<b>Interruption Obligatoire</b> : quand il y a 4 compteurs de rage ici, retournez cette carte et passez en forme d'Uncontrollable Hulk.",
  // totally_awesome_hulk — "The Trunk" (Support)
  '68012b': "<b>Réponse Obligatoire</b> : après qu'Uncontrollable Hulk a attaqué, retirez un compteur de rage de cette carte.\n<b>Interruption Obligatoire</b> : quand il n'y a plus de compteur de rage ici, retournez cette carte et passez en forme d'Amadeus Cho.",
  // totally_awesome_hulk — Get Under Control (Obligation)
  '68013': "<b><i>Donnez-la au joueur Amadeus Cho.</i></b>\nVous ne pouvez pas mettre d'alliés en jeu.\n<b>Action d'identité civile</b> : considérez que la zone de texte imprimée de \"The Trunk\" est vierge, puis retirez \"The Trunk\" de la partie → retirez cette obligation de la partie.",
  // totally_awesome_hulk — Lady Hellbender (Minion)
  '68014': "<b>Action de héros</b> : dépensez un nombre de ressources [wild] égal aux points de vie restants de Lady Hellbender → considérez Lady Hellbender comme une alliée que vous contrôlez, avec du CTR au lieu du MNG.\n<i>(Sbire nemesis de Totally Awesome Hulk.)</i>",
  // totally_awesome_hulk — For The Queen! (SideScheme)
  '68015': "Tant que Lady Hellbender est en jeu, les sbires [[MONSTER]] gagnent vilenie.",
  // totally_awesome_hulk — Fin Fang Foom (Minion)
  '68016': "<b>Une fois révélée</b> : Fin Fang Foom gagne +2 points de vie par joueur.\n<b>Interruption Obligatoire</b> : quand il reste à Fin Fang Foom 2 points de vie par joueur ou moins, ses attaques gagnent déferlement.",
  // totally_awesome_hulk — Krackalakassian (Minion)
  '68017': "<b>Une fois révélée</b> : Krackalakassian gagne +2 points de vie par joueur.\n<b>Interruption Obligatoire</b> : quand Krackalakassian attaque, subissez 2 dégâts indirects.",
  // totally_awesome_hulk — Threat Assessment (Treachery)
  '68018': "<b>Une fois révélée</b> : infligez 3 dégâts à l'identité ayant le plus de points de vie restants.",
  // madame_web — Madame Web (Hero)
  '69001a': "<i>Un lien avec les alliés</i> — Madame Web gagne les <b>traits</b> de chaque allié que vous contrôlez.\nX est égal au nombre d'alliés que vous contrôlez (maximum 3).",
  // madame_web — Cassandra Webb (AlterEgo)
  '69001b': "<i>Arachnophilie</i> — Vous pouvez inclure dans votre deck des alliés ayant le trait <b>WEB-WARRIOR</b> ou dont le titre contient \"Spider\", quel que soit leur aspect.\n<b>Mise en place</b> : cherchez l'amélioration Life-Support System dans votre deck et votre pile de défausse, et mettez-la en jeu.",
  // madame_web — Spider-Woman (Ally)
  '69002': "Spider-Woman entre en jeu avec 2 compteurs de toile psionique.\n<b>Réponse</b> : après qu'une manigance annexe est entrée en jeu, retirez 1 compteur de toile psionique de Spider-Woman → retirez 2 menaces de cette manigance annexe.",
  // madame_web — Webb's Apartment (Support)
  '69003': "<b>Action d'identité civile</b> : inclinez Webb's Apartment → soignez 1 dégât d'un personnage que vous contrôlez.",
  // madame_web — Clairvoyance (Upgrade)
  '69004': "<b>Interruption de héros</b> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, inclinez Clairvoyance → prévenez 1 de ces dégâts.",
  // madame_web — Astral Form (Upgrade)
  '69005': "<b>Action de héros</b> <i>(contre)</i> : inclinez Astral Form et dépensez une ressource [mental] → retirez X menaces réparties entre les manigances en jeu, où X est le nombre d'alliés que vous contrôlez.",
  // madame_web — Weaving a Web (Upgrade)
  '69006': "<b>Ressource</b> : inclinez Weaving a Web → générez une ressource [wild] pour un allié.",
  // madame_web — Life-Support System (Upgrade)
  '69007': "Vous gagnez +3 points de vie.\nCassandra Webb gagne +1 REC.\n<b>Interruption</b> : quand vous devriez être mis K.O. en défaussant cette carte, réglez plutôt votre cadran de points de vie sur 1.",
  // madame_web — Webb's Team Strikes! (Event)
  '69008': "<b>Action de héros</b> <i>(attaque)</i> : inclinez jusqu'à X alliés que vous contrôlez → infligez 3 dégâts au méchant par allié incliné de cette façon.",
  // madame_web — Foresight (Event)
  '69009': "<b>Interruption de héros</b> : quand vous révélez une carte rencontre, inclinez Madame Web → annulez les effets de cette carte et défaussez-la.",
  // madame_web — Gathering of Five (Event)
  '69010': "<b>Action</b> : défaussez la carte du dessus de votre deck. Si la ressource imprimée de cette carte est :\n[physical] - Infligez 3 dégâts à votre identité.\n[energy] - Madame Web gagne +2 ATQ jusqu'à la fin de la phase.\n[mental] - Retirez 2 menaces d'une manigance.\n[wild] - Soignez tous les dégâts de votre identité.",
  // madame_web — Web of Fate (Resource)
  '69011': "<b>Réponse</b> : après avoir dépensé cette carte, regardez les 5 cartes du dessus de votre deck. Ajoutez-en 1 à votre main et remettez les autres dans le même ordre.",
  // madame_web — Neurological Deterioration (Obligation)
  '69012': "Vous ne pouvez pas redresser votre identité.\n<b>Action d'identité civile</b> : dépensez des ressources [energy] [mental] [physical] → retirez Neurological Deterioration de la partie.",
  // madame_web — Spider-Woman (Minion)
  '69013': "<b>Une fois révélée</b> : choisissez soit de subir 2 dégâts indirects, soit d'incliner votre identité.\n<i>(Sbire nemesis de Madame Web.)</i>",
  // madame_web — Spider-Women Hunt (SideScheme)
  '69014': "En prenant le nom de \"Spider-Woman\", Witter a orchestré des attaques contre les autres femmes ayant porté ce nom avant elle, et absorbé leurs pouvoirs.\n<b>Une fois révélée</b> : placez 2 menaces supplémentaires ici par personnage en jeu dont le titre contient \"Spider\".",
  // madame_web — Power Absorption (Treachery)
  '69015': "<b>Une fois révélée</b> : défaussez un allié que vous contrôlez. Si aucun allié n'a été défaussé de cette façon, passez en forme d'identité civile et inclinez votre identité.",
  // madame_web — Hypnosis (Treachery)
  '69016': "Renfort.\n<b>Une fois révélée</b> : sonnez et désorientez un personnage que vous contrôlez.",
  // madame_web — Ana Kraven (Minion)
  '69017': "[star] <b>Réponse Obligatoire</b> : après qu'Ana Kraven vous a attaqué, placez 1 menace sur la manigance annexe The Grim Hunt. Si The Grim Hunt n'est pas en jeu, placez 1 menace sur la manigance principale.\n<i>(Sbire nemesis de Madame Web.)</i>",
  // madame_web — The Grim Hunt (SideScheme)
  '69018': "Quand Sasha Kraven envoya sa fille Ana enlever la médium connue sous le nom de Madame Web, ce fut le début d'une chasse à tous ceux qui portent la marque de l'araignée.\n<b>Une fois révélée</b> : mettez Kraven the Hunter de côté, hors jeu.\nThe Grim Hunt gagne 1 menace par joueur à la fin de chaque phase du méchant. Si cette manigance est accomplie (5 menaces par joueur), mettez en jeu Kraven the Hunter mis de côté, engagé avec le premier joueur.",
  // madame_web — Kraven the Hunter (Minion)
  '69019': "Riposte 1. Vilenie.\n<b>Quand vaincu</b> : mettez Kraven the Hunter de côté, hors jeu.",
  // madame_web — One Spyder Down (Treachery)
  '69020': "<b>Une fois révélée</b> : défaussez un allié que vous contrôlez. Si vous ne pouvez pas, cette carte gagne renfort.",
  // madame_web — Hunting Spyders (Treachery)
  '69021': "<b>Une fois révélée</b> : infligez 3 dégâts à un allié que vous contrôlez. Si vous ne pouvez pas, infligez 3 dégâts à votre identité.",
  // madame_web — Scarlet Spider (Ally)
  '69022': "<b>Réponse de héros</b> : après que Scarlet Spider est entré en jeu, redressez votre héros.",
  // madame_web — Spider-Woman (Ally)
  '69023': "Spider-Woman gagne +1 ATQ si vous avez payé cette carte en n'utilisant que des ressources [physical].",
  // madame_web — Spider-Woman (Ally)
  '69024': "<b>Interruption de héros</b> : quand le méchant initie une attaque contre vous, piochez 1 carte.",
  // madame_web — Spider-Woman (Ally)
  '69025': "<b>Interruption Obligatoire</b> : quand Spider-Woman arrive dans votre main, payez son coût imprimé → mettez Spider-Woman en jeu sous votre contrôle. Si vous ne pouvez pas, défaussez Spider-Woman.",
  // madame_web — Spider-Woman (Ally)
  '69026': "<b>Interruption Obligatoire</b> : quand Spider-Woman devrait être mise K.O., soignez plutôt tous ses dégâts et engagez-la comme un sbire. Considérez Spider-Woman comme un sbire à la zone de texte vierge <i>(à l'exception de ses <b>traits</b>)</i>. Son MNG est égal à son CTR imprimé et elle ne subit pas de dégâts consécutifs.",
  // madame_web — Order of the Web (Support)
  '69027': "Jouez-la sous le contrôle de n'importe quel joueur. Maximum 1 carte <b>TEAM</b> par joueur.\n<b>Action</b> : inclinez Order of the Web → choisissez dans votre pile de défausse un allié dont le titre contient \"Spider\" et mélangez-le dans votre deck.",
  // madame_web — Advice (Event)
  '69028': "<b>Action</b> : choisissez un allié et défaussez la carte du dessus du deck rencontre. Cet allié gagne +X ATQ durant cette phase, où X est le nombre d'icônes de boost ([boost]) défaussées de cette façon.",
  // madame_web — Female Power (Event)
  '69029': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi par personnage que vous contrôlez dont le titre contient \"Girl\", \"Lady\", \"Madame\", \"Ms.\", \"She\" ou \"Woman\".",
  // cloak_dagger — Cloak (Hero)
  '70001a': "Riposte 1.\n[star] <i>Duo protecteur</i> — Cloak gagne +2 DEF tant que Dagger est en jeu.",
  // cloak_dagger — Tyrone Johnson (AlterEgo)
  '70001b': "Pendant la construction du deck, voir l'encart.\n<i>Éclaircissement</i> — Tandy Bowen et Tyrone Johnson gagnent robuste tant que Tandy Bowen est en jeu.",
  // cloak_dagger — Dagger (Hero)
  '70002a': "[star] <i>Duo destructeur</i> — Dagger gagne +2 ATQ tant que Cloak est en jeu.\n[star] <i>Barrage lumineux</i> — Les dégâts que Dagger inflige avec son pouvoir d'attaque de base <i>(ATQ)</i> peuvent être répartis entre les ennemis comme vous le souhaitez.",
  // cloak_dagger — Tandy Bowen (AlterEgo)
  '70002b': "Pendant la construction du deck, voir l'encart.\n[star] <i>Harmonie</i> — Tandy Bowen et Tyrone Johnson gagnent +2 REC tant que Tyrone Johnson est en jeu.",
  // cloak_dagger — Forces Combined (Upgrade)
  '70003': "Immuable. Permanent. Mise en place.\n<b>Interruption</b> : quand vous devriez dépenser des ressources pour une carte ou une capacité, inclinez Forces Combined → vous pouvez dépenser des ressources de vos deux mains pour cette carte ou cette capacité.",
  // cloak_dagger — Lightforce Cleansing (Event)
  '70004': "<b>Action de héros</b> : soignez 3 dégâts d'un personnage allié. Si 2 dégâts ou plus ont été soignés de Cloak de cette façon, piochez 1 carte dans le deck de chacune de vos identités.",
  // cloak_dagger — Lightforce Daggers (Event)
  '70005': "<b>Action de héros</b> <i>(attaque)</i> : infligez un total de 3 dégâts répartis entre les ennemis comme vous le souhaitez et sonnez le méchant. Puis, si Cloak est en jeu, désorientez un ennemi.",
  // cloak_dagger — Pure Lightforce (Resource)
  '70006': "<b>Réponse de héros</b> : après avoir dépensé cette carte pour une carte [[LIGHTFORCE]], infligez 1 dégât au méchant par ressource payée en trop pour le coût de cette carte [[LIGHTFORCE]].",
  // cloak_dagger — Lightforce Absorption (Upgrade)
  '70007': "<b>Réponse</b> : après avoir joué une carte [[LIGHTFORCE]], inclinez Lightforce Absorption → mélangez une carte [[LIGHTFORCE]] de la pile de défausse de Dagger dans le deck de Dagger.",
  // cloak_dagger — Living Light (Upgrade)
  '70008': "Cette carte ne peut pas être inclinée tant que le joueur Cloak & Dagger n'a pas infligé 5 dégâts ou plus au méchant durant cette phase.\n<b>Action de héros</b> : inclinez Living Light → redressez Dagger.",
  // cloak_dagger — Dark Teleportation (Event)
  '70009': "<b>Action de héros</b> : redressez un personnage allié. Puis, si Dagger a été redressée de cette façon, retirez 2 menaces d'une manigance.",
  // cloak_dagger — Darkforce Channel (Event)
  '70010': "<b>Action de héros</b> <i>(attaque)</i> : choisissez jusqu'à 3 ennemis différents. Infligez 1 dégât à chacun d'eux et soignez 1 dégât de Cloak par ennemi blessé de cette façon. Désorientez le méchant. Puis, si Dagger est en jeu, sonnez un ennemi.",
  // cloak_dagger — Raw Darkforce (Resource)
  '70011': "<b>Réponse de héros</b> : après avoir dépensé cette carte pour une carte [[DARKFORCE]], retirez 1 menace de la manigance principale par ressource payée en trop pour le coût de cette carte [[DARKFORCE]].",
  // cloak_dagger — Dark Intangibility (Upgrade)
  '70012': "<b>Réponse</b> : après que Cloak a fait une défense de base, inclinez Dark Intangibility → redressez Cloak, et il gagne riposte 1 jusqu'à la fin de la phase.",
  // cloak_dagger — Darkforce Absorption (Upgrade)
  '70013': "<b>Réponse</b> : après avoir joué une carte [[DARKFORCE]], inclinez Darkforce Absorption → mélangez une carte [[DARKFORCE]] de la pile de défausse de Cloak dans le deck de Cloak.",
  // cloak_dagger — Lovers Quarrel (Obligation)
  '70014': "<b><i>Donnez-la au joueur Cloak & Dagger.</i></b>\nPassez les deux identités en forme d'identité civile, puis choisissez l'un ou l'autre :\n• Inclinez Tandy Bowen et Tyrone Johnson → retirez Lovers Quarrel de la partie.\n• Tyrone Johnson ne peut ni changer de forme, ni jouer de cartes, ni utiliser de pouvoirs de base au round suivant → défaussez cette obligation.",
  // cloak_dagger — Mister Negative (Minion)
  '70015': "<b>Réponse Obligatoire</b> : après que Mister Negative a attaqué votre héros, passez-le en forme d'identité civile.",
  // cloak_dagger — Bigger Fish (SideScheme)
  '70016': "<b>Interruption Obligatoire</b> : quand le méchant ou Mister Negative devraient attaquer, ils manigancent à la place.",
  // cloak_dagger — Inner Demon (Minion)
  '70017': "Garde. Ténacité.",
  // cloak_dagger — Opposites Attack (Treachery)
  '70018': "<b>Une fois révélée</b> : passez chaque héros en forme d'identité civile. Puis, placez 1 menace sur la manigance principale par héros retourné de cette façon.",
  // spider_man_rainy — Spider-Man (Hero)
  '71001a': "Comme des mouches — <b>Interruption</b> : quand un sbire s'engage avec vous, entoilez-le. (Limite de deux fois par round.)\n<b>Réponse</b> : après qu'un ennemi entoilé a été mis K.O., retirez 1 menace d'une manigance.",
  // spider_man_rainy — Peter Parker (AlterEgo)
  '71001b': "La sagesse d'oncle Ben — <b>Action</b> : défaussez 1 carte de votre main → cherchez une ressource Great Power ou Great Responsibility dans votre deck et votre pile de défausse, et ajoutez-la à votre main. Mélangez votre deck. (Limite de deux fois par round.)",
  // spider_man_rainy — Spider-Man (Ally)
  '71002': "[star] <b>Interruption</b> : quand cet allié utilise un pouvoir de base, entoilez un ennemi (maximum 3 compteurs de toile par ennemi).",
  // spider_man_rainy — Thwip! (Event)
  '71003': "<b>Action de héros</b> : redressez votre héros et entoilez un ennemi (maximum 3 compteurs de toile par ennemi).",
  // spider_man_rainy — Web Barrage (Event)
  '71004': "<b>Action de héros</b> : faites l'attaque suivante contre X ennemis.\n<i>(attaque)</i> : entoilez un ennemi et infligez-lui 2 dégâts. Cette attaque gagne à distance.",
  // spider_man_rainy — Web Strike (Event)
  '71005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 6 dégâts à un ennemi. Si cet ennemi est entoilé, infligez 2 dégâts supplémentaires. Cette attaque gagne déferlement.",
  // spider_man_rainy — Webbed Up (Event)
  '71006': "<b>Action de héros</b> : choisissez un ennemi et entoilez-le jusqu'à 3 fois.\n<b>Interruption de héros</b> <i>(défense)</i> : quand une identité devrait subir des dégâts d'une attaque, prévenez tous ces dégâts.",
  // spider_man_rainy — Great Power (Resource)
  '71007': "<b>Réponse de héros</b> <i>(attaque)</i> : après avoir dépensé cette carte, infligez 2 dégâts à un ennemi.",
  // spider_man_rainy — Great Responsibility (Resource)
  '71008': "<b>Réponse de héros</b> <i>(contre)</i> : après avoir dépensé cette carte, retirez 2 menaces d'une manigance.",
  // spider_man_rainy — J. Jonah Jameson (Support)
  '71009': "<b>Action d'identité civile</b> : inclinez J. Jonah Jameson → piochez 1 carte. Si cette carte comportait une image de Spider-Man, piochez une autre carte.",
  // spider_man_rainy — Spider-Sense (Upgrade)
  '71010': "<b>Interruption de héros</b> : quand le méchant ou un sbire ayant vilenie initie une attaque contre vous, piochez 1 carte.\n<b>Interruption de héros</b> : quand une carte de boost est retournée face visible pendant une attaque contre vous, défaussez 1 carte de votre main → annulez la capacité de boost de cette carte.",
  // spider_man_rainy — Web-Shooters (Upgrade)
  '71011': "Votre héros gagne le trait [[AERIAL]].\n<b>Ressource de héros</b> : inclinez Web-Shooters → générez une ressource [wild] pour une carte WEB.\n<b>Action de héros</b> : inclinez Web-Shooters → entoilez un ennemi.",
  // spider_man_rainy — Impact Webbing (Upgrade)
  '71012': "Permanent. Mise en place.\n<b>Interruption Obligatoire</b> : quand un ennemi entoilé s'active, retirez tous les compteurs de toile de cet ennemi → cet ennemi subit -1 MNG et -1 ATQ par compteur de toile retiré de cette façon, pour cette activation.",
  // spider_man_rainy — Bad Publicity (Obligation)
  '71013': "Donnez-la au joueur Peter Parker.\nUtilisations (3 compteurs de menace).\n<b>Réponse de héros</b> : après avoir mis un ennemi K.O. ou déjoué une manigance, retirez 1 compteur de menace d'ici.",
  // spider_man_rainy — For My Next Trick... (SideScheme)
  '71014': "<i>Mysterio a l'air de préparer un mauvais coup !</i>\nUtilisations (2 compteurs d'illusion).\n<b>Réponse Obligatoire</b> : après le début de la phase du méchant, retirez 1 compteur d'illusion d'ici.\n<b>Interruption Obligatoire</b> : quand cette carte devrait quitter le jeu sans avoir été déjouée, attribuez à chaque joueur une carte rencontre face cachée.",
  // spider_man_rainy — Mysterio (Minion)
  '71015': "Entre en jeu avec 2 compteurs d'illusion.\n<b>Interruption Obligatoire</b> : quand Mysterio devrait subir des dégâts, retirez plutôt un compteur d'illusion d'ici.\n[star] <b>Réponse Obligatoire</b> : après que Mysterio s'est activé contre vous et a infligé des dégâts ou placé de la menace, attribuez-vous une carte rencontre face cachée.",
  // spider_man_rainy — Jump Scare (Treachery)
  '71016': "<b>Une fois révélée</b> : attribuez-vous une carte rencontre face cachée. Subissez 1 dégât par carte rencontre face cachée devant vous.\n[star] <b>Boost</b> : attribuez-vous une carte rencontre face cachée.",
  // spider_man_rainy — Smoke and Mirrors (Treachery)
  '71017': "Renfort.\n<b>Une fois révélée</b> : donnez à Mysterio une carte d'état Tenace et une carte de boost face cachée. Si vous ne pouvez pas, donnez-les au méchant.\n[star] <b>Boost</b> : vous êtes désorienté.",
  // venom_rainy — Venom (Hero)
  '72001a': "Faim — <b>Réponse</b> : après avoir mis un ennemi K.O., soignez 1 dégât de Venom.\nLien symbiotique — <b>Ressource</b> : subissez 1 dégât → générez une ressource [wild]. (Limite d'une fois par phase.)",
  // venom_rainy — Eddie Brock (AlterEgo)
  '72001b': "Journaliste d'investigation — <b>Réponse</b> : après que de la menace a été placée sur la manigance principale, retirez 2 menaces d'une manigance. (Limite d'une fois par round.)",
  // venom_rainy — Bulletproof (Event)
  '72002': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts d'une attaque, quel qu'en soit le nombre, prévenez 2 de ces dégâts et piochez 1 carte. Puis, vous pouvez mélanger cette carte dans votre deck.",
  // venom_rainy — Just A Snack (Event)
  '72003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 1 dégât à un ennemi (2 dégâts à la place si vous avez payé cette carte avec une ressource [physical]). Soignez 2 dégâts de Venom.",
  // venom_rainy — Self-Sacrifice (Event)
  '72004': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Vous pouvez subir 2 dégâts pour retirer 3 menaces supplémentaires de cette manigance.",
  // venom_rainy — Symbiotic Fury (Event)
  '72005': "<b>Réponse de héros</b> : après avoir subi des dégâts, subissez 1 dégât supplémentaire → redressez votre héros. Puis, si vous avez subi 6 dégâts ou plus au total, infligez 2 dégâts à un ennemi.",
  // venom_rainy — Tendril Explosion (Event)
  '72006': "<b>Action de héros</b> : infligez X dégâts à chaque ennemi.",
  // venom_rainy — Venomous Bite (Event)
  '72007': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Puis, sonnez cet ennemi. Si aucun ennemi n'a été sonné de cette façon, soignez 2 dégâts de Venom.",
  // venom_rainy — Camouflage (Upgrade)
  '72008': "<b>Interruption de héros</b> <i>(attaque)</i> : quand un ennemi devrait initier une attaque, défaussez Camouflage → infligez 4 dégâts à cet ennemi et désorientez-le. Si aucun ennemi n'a été désorienté de cette façon, retirez 2 menaces d'une manigance.",
  // venom_rainy — Lethal Protector (Upgrade)
  '72009': "Venom gagne +1 DEF.\n<b>Interruption de héros</b> <i>(attaque/défense)</i> : quand un ennemi initie une attaque, inclinez Lethal Protector → infligez 2 dégâts à cet ennemi. Si un ennemi a été mis K.O. de cette façon, redressez Lethal Protector.",
  // venom_rainy — Regeneration (Upgrade)
  '72010': "Vous gagnez +2 points de vie.\n<b>Réponse d'identité civile</b> : après avoir utilisé votre REC, inclinez Regeneration → redressez Eddie Brock.",
  // venom_rainy — Sharp Teeth (Upgrade)
  '72011': "Venom gagne +1 ATQ.\nLes attaques de base de Venom gagnent déferlement et perçant.",
  // venom_rainy — We Hunger (Obligation)
  '72012': "Donnez-la au joueur Eddie Brock.\nPassez en forme de héros. Choisissez :\n- Subissez 3 dégâts → défaussez cette obligation.\n- Placez 3 menaces sur la manigance principale → soignez 1 dégât de Venom et défaussez cette obligation.",
  // venom_rainy — Paint The Town Red (SideScheme)
  '72013': "<i>Carnage a lâché sur la ville une horde déchaînée de symbiotes violents ! Arrêtez-les avant que la ville ne sombre dans le chaos absolu !</i>\nEntrave 2[per_hero].",
  // venom_rainy — Carnage (Minion)
  '72014': "Coup Rapide. Riposte 1.\n<b>Réponse Obligatoire</b> : après avoir soigné des dégâts, subissez 1 dégât.\n<i>(Sbire nemesis de Venom.)</i>",
  // venom_rainy — Symbiote Rioter (Minion)
  '72015': "Garde. Patrouille.\n<b>Réponse Obligatoire</b> : après avoir attaqué un autre ennemi, subissez 1 dégât.",
  // jessica_jones — Jessica Jones (Hero)
  '73001a': "Enquête musclée — <b>Réponse</b> <i>(attaque)</i> : après avoir déjoué une manigance annexe, infligez à un ennemi un nombre de dégâts égal à votre ATQ.",
  // jessica_jones — Jessica Jones (AlterEgo)
  '73001b': "<b>Mise en place</b> : mélangez le set On the Job dans le deck rencontre.\nÇa paie les factures — <b>Réponse</b> : après qu'une manigance annexe a été révélée, piochez 2 cartes. <i>(Limite d'une fois par phase.)</i>",
  // jessica_jones — Luke Cage (Ally)
  '73002': "Ténacité. <i>(Ce personnage entre en jeu avec une carte d'état Tenace.)</i>\nTant qu'il y a une manigance annexe en jeu, réduisez de 1 les dégâts subis par Luke Cage.",
  // jessica_jones — Breakthrough (Event)
  '73003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Infligez-lui 1 dégât supplémentaire par manigance annexe en jeu.",
  // jessica_jones — Crack the Case (Event)
  '73004': "Jouez-la uniquement s'il y a une manigance annexe en jeu.\n<b>Action</b> <i>(contre)</i> : retirez 2 menaces d'une manigance. Si une manigance annexe est déjouée de cette façon, redressez Jessica Jones.",
  // jessica_jones — Hit the Streets (Event)
  '73005': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Retirez-en 1 supplémentaire par manigance annexe en jeu.",
  // jessica_jones — Out in the Open (Event)
  '73006': "<b>Interruption</b> : quand une carte de traîtrise est révélée depuis le deck rencontre, annulez ses effets \"<b>Une fois révélée</b>\". Défaussez les cartes du dessus du deck rencontre jusqu'à défausser une manigance annexe. Révélez cette manigance annexe.",
  // jessica_jones — The Truth Hurts (Event)
  '73007': "Jouez-la uniquement s'il y a une manigance annexe en jeu.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Si vous avez déjoué une manigance annexe ce round, désorientez cet ennemi.",
  // jessica_jones — Alias Investigations (Support)
  '73008': "<b>Action</b> : inclinez Alias Investigations → défaussez les cartes du dessus du deck rencontre jusqu'à défausser une manigance annexe. Révélez cette manigance annexe.",
  // jessica_jones — Jessica's Camera (Upgrade)
  '73009': "<b>Réponse</b> : après avoir déjoué une manigance annexe, inclinez Jessica's Camera → placez 1 compteur de preuve ici. Tant que Jessica's Camera a au moins :\n(1) Jessica Jones gagne +1 DEF.\n(2) Jessica Jones gagne +1 CTR.\n(3) Jessica Jones gagne +1 ATQ.",
  // jessica_jones — Jessica's Jacket (Upgrade)
  '73010': "Vous gagnez +2 points de vie.\n<b>Interruption</b> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, inclinez Jessica's Jacket → prévenez 1 de ces dégâts et retirez 1 menace d'une manigance.",
  // jessica_jones — Private Investigator (Upgrade)
  '73011': "<b>Action d'identité civile</b> : inclinez Private Investigator → déplacez 1 menace d'une manigance vers cette carte.\n<b>Action de héros</b> : retirez toute la menace d'ici → infligez 1 dégât à un sbire par menace retirée de cette façon.",
  // jessica_jones — Always a Bigger Conspiracy (SideScheme)
  '73012': "<i>« Il y a toujours deux histoires derrière une histoire. » — Jessica Jones</i>\nQuand Jessica Jones contre une manigance annexe, elle peut utiliser son ATQ au lieu de son CTR.\n<b>Quand déjouée</b> : défaussez les cartes du dessus du deck rencontre jusqu'à défausser une manigance annexe. Révélez cette manigance annexe.",
  // jessica_jones — Chase Down a Lead (SideScheme)
  '73013': "Investigation 2. <i>(Une fois révélée, déplacez 2 menaces de la manigance principale vers cette carte.)</i>\n<b>Quand déjouée</b> : le joueur Jessica Jones cherche une carte spécifique à son héros parmi les 5 cartes du dessus de son deck et l'ajoute à sa main. <i>(Mélangez.)</i>",
  // jessica_jones — Hang Back and Watch (SideScheme)
  '73014': "Investigation 2[per_hero]. <i>(Une fois révélée, déplacez 2[per_hero] menaces de la manigance principale vers cette carte.)</i>\n<b>Quand déjouée</b> : soignez 2 dégâts de Jessica Jones.",
  // jessica_jones — Pore Over the Evidence (SideScheme)
  '73015': "Investigation 1[per_hero]. <i>(Une fois révélée, déplacez 1[per_hero] menace de la manigance principale vers cette carte.)</i>\n<b>Quand déjouée</b> : réduisez de 2 le coût de la prochaine carte que le joueur Jessica Jones joue durant cette phase.",
  // jessica_jones — Sneak Into the Crime Scene (SideScheme)
  '73016': "Investigation 2. <i>(Une fois révélée, déplacez 2 menaces de la manigance principale vers cette carte.)</i>\n<b>Quand déjouée</b> : donnez une carte d'état Tenace à Jessica Jones.",
  // jessica_jones — Stable Home Life (Obligation)
  '73017': "<i>Donnez-la au joueur Jessica Jones.</i>\nVous pouvez passer en forme d'identité civile. Choisissez :\n- Inclinez votre identité civile → retirez Stable Home Life de la partie.\n- Défaussez du jeu une manigance annexe On the Job. Si vous ne pouvez pas, cette carte gagne renfort. Défaussez cette obligation.",
  // jessica_jones — "Look At Me!" (SideScheme)
  '73018': "Purple Man ne peut pas subir de dégâts.\n<b>Réponse Obligatoire</b> : après qu'une manigance annexe a été déjouée, placez X menaces sur la manigance principale, où X est égal au nombre de manigances annexes en jeu.\n<hr /> [star] <b>Boost</b> : après la fin de cette activation, révélez cette carte.",
  // jessica_jones — Purple Man (Minion)
  '73019': "[star] <b>Interruption Obligatoire</b> : quand Purple Man devrait attaquer, placez plutôt 2 menaces sur chaque manigance annexe. S'il n'y a aucune manigance annexe en jeu, révélez la carte du dessus du deck rencontre.\n<i>(Son ATQ imprimée est une [star] : sa valeur est définie par sa capacité, le 0 affiché ne sert jamais.)</i>\n<hr /> [star] <b>Boost</b> : vous êtes désorienté.\n<i>(Sbire nemesis de Jessica Jones.)</i>",
  // jessica_jones — "I've Got Everyone" (Treachery)
  '73020': "<b>Une fois révélée</b> : répartissez X dégâts indirects entre les joueurs <i>(comme vous le souhaitez)</i>, où X est égal au nombre de manigances annexes en jeu. Désorientez chaque personnage blessé de cette façon. S'il n'y a aucune manigance annexe en jeu, cette carte gagne renfort.",
  // jessica_jones — The Purple Children (Treachery)
  '73021': "Incitation 1 <i>(incitation 2 à la place si Purple Man est en jeu)</i>.\n<b>Une fois révélée</b> : placez 2 menaces sur chaque manigance annexe en jeu. S'il n'y a aucune manigance annexe en jeu, vous êtes désorienté.",
  // jessica_jones — Power Couple (Event)
  '73022': "Team-Up (Jessica Jones et Luke Cage). Maximum 1 par deck.\n<b>Action de héros</b> : donnez une carte d'état Tenace à Jessica Jones et à Luke Cage. Puis, piochez autant de cartes qu'il y a de cartes d'état Tenace parmi les personnages alliés.",
  // agent_anti_venom — Agent Anti-Venom (Hero)
  '74001a': "[star] <i>Dix sur dix !</i> — Tant qu'il reste exactement 10 points de vie à Agent Anti-Venom, il gagne +1 CTR, +1 ATQ, +1 DEF, et ses attaques gagnent perçant.",
  // agent_anti_venom — Flash Thompson (AlterEgo)
  '74001b': "<i>Petit scout</i> — <b>Réponse</b> : après être passé à cette forme, soignez 2 dégâts de n'importe quel personnage.",
  // agent_anti_venom — Spider-Man (Ally)
  '74002': "<b>Interruption</b> : quand un sbire non-[[ELITE]] devrait attaquer ou manigancer, dépensez une ressource [mental] → annulez cette activation.",
  // agent_anti_venom — Dig Deep (Event)
  '74003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. S'il reste exactement 10 points de vie à Agent Anti-Venom, retirez 1 menace d'une manigance et sonnez cet ennemi.",
  // agent_anti_venom — Extricate (Event)
  '74004': "<b>Action de héros</b> <i>(contre)</i> : retirez 4 menaces d'une manigance. S'il reste exactement 10 points de vie à Agent Anti-Venom, piochez 1 carte ou désorientez un ennemi.",
  // agent_anti_venom — "I've Got This!" (Event)
  '74005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts au méchant <i>(7 dégâts à la place si cette attaque a à distance ou perçant)</i>.",
  // agent_anti_venom — Anti-Venom Goo (Resource)
  '74006': "<b>Interruption de héros</b> : quand vous dépensez cette carte pour jouer un événement, réduisez de 1 le coût de cet événement. Puis, soignez 1 dégât d'un personnage allié par ressource payée en trop pour le coût de cet événement avec cette carte.",
  // agent_anti_venom — Unlikely Allies (Support)
  '74007': "<b>Action de héros</b> : inclinez cette carte et défaussez une carte de votre main. Si la zone de ressource imprimée de cette carte comporte :\n[physical] - Drainez 2 d'un ennemi.\n[mental] - Retirez 2 menaces d'une manigance.\n[energy] - Piochez 2 cartes.\n[wild] - Choisissez 2 des options ci-dessus.",
  // agent_anti_venom — Anti-Maniac Booster (Upgrade)
  '74008': "Agent Anti-Venom gagne riposte 1.\n<b>Réponse</b> : après qu'Agent Anti-Venom a subi des dégâts d'une attaque, inclinez Anti-Maniac Booster → soignez 1 dégât d'Agent Anti-Venom.",
  // agent_anti_venom — Bear Arms (Upgrade)
  '74009': "<b>Action de héros</b> : inclinez Bear Arms → la prochaine attaque d'Agent Anti-Venom gagne à distance.\n<b>Action de héros</b> <i>(attaque)</i> : inclinez Bear Arms → drainez 1 du méchant.",
  // agent_anti_venom — Heroic Will (Upgrade)
  '74010': "<b>Action d'identité civile</b> : inclinez Heroic Will → changez de forme.\n<b>Action de héros</b> : inclinez Heroic Will → redressez Agent Anti-Venom.",
  // agent_anti_venom — One Man Army (Upgrade)
  '74011': "<b>Interruption</b> : quand Agent Anti-Venom utilise un pouvoir de base, s'il n'y a aucun allié sous votre contrôle, piochez 1 carte et soignez 1 dégât d'Agent Anti-Venom. <i>(Limite d'une fois par round.)</i>",
  // agent_anti_venom — Spread Too Thin (Obligation)
  '74012': "<i>Donnez-la au joueur Flash Thompson.</i>\nVous pouvez passer en forme d'identité civile. Choisissez :\n- Infligez 3 dégâts à votre identité → retirez Spread Too Thin de la partie.\n- Retirez de la partie une amélioration que vous contrôlez. Défaussez cette obligation.",
  // agent_anti_venom — Maniac (Minion)
  '74013': "<b>Réponse Obligatoire</b> : après que Maniac a attaqué un allié que vous contrôlez, infligez X dégâts à votre héros, où X est l'ATQ imprimée de cet allié.\n<i>(Sbire nemesis d'Agent Anti-Venom.)</i>",
  // agent_anti_venom — The Made Men (SideScheme)
  '74014': "<b>Interruption Obligatoire</b> : après que Maniac a manigancé ou attaqué, l'allié ayant l'ATQ imprimée la plus élevée sous le contrôle de chaque joueur gagne traître <i>(considérez cet allié comme un sbire engagé avec son propriétaire. Il a 1 MNG, une zone de texte imprimée vierge, et ne subit pas de dégâts consécutifs.)</i>",
  // agent_anti_venom — Infected Scorpion (Minion)
  '74015': "Coup Rapide.\n<b>Interruption Obligatoire</b> : quand Infected Scorpion attaque un allié, prévenez tous les dégâts infligés à cet allié. Cet allié gagne traître <i>(considérez cet allié comme un sbire engagé avec son propriétaire. Il a 1 MNG, une zone de texte imprimée vierge, et ne subit pas de dégâts consécutifs.)</i>",
  // agent_anti_venom — Infected (Attachment)
  '74016': "Attachez-la au sbire ayant le plus de points de vie imprimés. S'il n'y a aucun sbire en jeu, cette carte gagne renfort.\nLes attaques du sbire attaché gagnent déferlement.",
  // squirrel_girl — Squirrel Girl (Hero)
  '75001a': "<i>Armée imbattable</i> — <b>Réponse de héros</b> : après avoir dépensé un Écureuil, infligez 1 dégât à un ennemi ou retirez 1 menace d'une manigance. (Limite d'une fois par phase.)\n<i>Aide d'Écureuil</i> — <b>Ressource</b> : défaussez un allié [[SQUIRREL]] que vous contrôlez → générez 1 ressource [wild]. Ne la dépensez que pour payer une carte Squirrel Girl. (Limite d'1 Écureuil par carte jouée.)",
  // squirrel_girl — Doreen Green (AlterEgo)
  '75001b': "Doreen Green commence la partie avec un deck d'Écureuils. <i>(Mettez les 6 alliés [[SQUIRREL]] de côté, mélangés. Quand un effet appelle un Écureuil, révélez la carte du dessus du deck d'Écureuils et mettez-la en jeu inclinée, sous votre contrôle. Si le deck d'Écureuils est vide, mélangez la pile de défausse des Écureuils pour en former un nouveau.)</i>\n<i>Langage des écureuils</i> — <b>Action d'identité civile</b> : inclinez Doreen Green → appelez 1 Écureuil. (Limite d'une fois par round.)\n<i>Aide d'Écureuil</i> — <b>Ressource</b> : défaussez un allié [[SQUIRREL]] que vous contrôlez → générez 1 ressource [wild]. Ne la dépensez que pour payer une carte Squirrel Girl. (Limite d'1 Écureuil par carte jouée.)",
  // squirrel_girl — Tippy-Toe (Ally)
  '75002': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>\n<b>Réponse</b> : après que Tippy-Toe est entrée en jeu, regardez les 2 cartes du dessus du deck d'Écureuils. Remettez-les dans l'ordre de votre choix.",
  // squirrel_girl — Monkey Joe (Ally)
  '75003': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>\n<b>Réponse</b> : après que Monkey Joe a mis un sbire K.O., appelez 1 Écureuil.",
  // squirrel_girl — The Lookout (Ally)
  '75004': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>",
  // squirrel_girl — The Bruiser (Ally)
  '75005': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>\n<b>Interruption</b> : quand un autre allié [[SQUIRREL]] que vous contrôlez devrait subir des dégâts consécutifs, inclinez The Bruiser → infligez plutôt 1 de ces dégâts à The Bruiser.",
  // squirrel_girl — The Forager (Ally)
  '75006': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>\n<b>Réponse</b> : après avoir dépensé The Forager, regardez les 2 cartes du dessus de votre deck. Défaussez-en 1, ou remettez-les dans l'ordre de votre choix.",
  // squirrel_girl — The Gatherer (Ally)
  '75007': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>\n<b>Réponse</b> : après avoir dépensé The Gatherer, soignez 1 dégât de Squirrel Girl.",
  // squirrel_girl — Nancy Whitehead (Ally)
  '75008': "<b>Réponse</b> : après que Nancy Whitehead est entrée en jeu, appelez 1 Écureuil.",
  // squirrel_girl — Squirrel Girl's Costume (Upgrade)
  '75009': "Squirrel Girl gagne +1 ATQ.\n<b>Réponse de héros</b> : après qu'un sbire a été mis K.O., appelez 1 Écureuil. (Limite d'une fois par round.)",
  // squirrel_girl — Prehensile Tail (Upgrade)
  '75010': "<b>Ressource</b> : inclinez Prehensile Tail → générez 1 ressource [wild]. Ne la dépensez que pour payer une carte Squirrel Girl.",
  // squirrel_girl — Central Park (Support)
  '75011': "<b>Action</b> : inclinez Central Park → si vous contrôlez moins de 3 alliés [[SQUIRREL]], appelez 1 Écureuil.",
  // squirrel_girl — Network of Trees (Support)
  '75012': "<b>Interruption</b> : quand vous devriez appeler un Écureuil, inclinez Network of Trees → regardez les 2 cartes du dessus du deck d'Écureuils. Appelez-en 1 et placez l'autre sous le deck d'Écureuils.",
  // squirrel_girl — Call the Squirrels (Event)
  '75013': "<b>Action</b> : appelez 2 Écureuils. Les Écureuils appelés de cette façon entrent en jeu redressés.",
  // squirrel_girl — Squirrel Swarm (Event)
  '75014': "<b>Action de héros <i>(attaque)</i></b> : infligez 3 dégâts à un ennemi. Si vous avez dépensé un Écureuil pour jouer cette carte, infligez-lui 3 dégâts supplémentaires.",
  // squirrel_girl — Recon Team (Event)
  '75015': "<b>Action de héros <i>(contre)</i></b> : retirez 3 menaces d'une manigance. Si vous avez dépensé un Écureuil pour jouer cette carte, retirez 1 menace d'une autre manigance.",
  // squirrel_girl — Unbeatable! (Event)
  '75016': "<b>Interruption de héros <i>(défense)</i></b> : quand Squirrel Girl se défend contre une attaque, elle gagne +2 DEF pour cette attaque. Si vous avez dépensé un Écureuil pour jouer cette carte, elle gagne +3 DEF à la place. Si cette attaque n'inflige aucun dégât à Squirrel Girl, redressez-la.",
  // squirrel_girl — Nuts! (Resource)
  '75017': "<b>Réponse</b> : après avoir dépensé cette carte pour payer une carte Squirrel Girl, appelez 1 Écureuil.",
  // squirrel_girl — Surprise Exam (Obligation)
  '75018': "<b><i>Donnez-la au joueur Doreen Green.</i></b>\nVous pouvez passer en forme d'identité civile. Choisissez :\n• Inclinez Doreen Green et défaussez de votre main une carte ayant une ressource [mental] imprimée → retirez Surprise Exam de la partie.\n• Défaussez 1 allié [[SQUIRREL]] que vous contrôlez. Si vous ne pouvez pas, défaussez 1 carte au hasard de votre main. Défaussez cette obligation.",
  // squirrel_girl — Ratatoskr (Minion)
  '75019': "<b>Interruption Obligatoire</b> : quand Ratatoskr s'active contre vous, défaussez 1 allié [[SQUIRREL]] que vous contrôlez. Si vous ne pouvez pas, Ratatoskr reçoit 1 carte de boost supplémentaire pour cette activation.",
  // squirrel_girl — Discord in the Branches (SideScheme)
  '75020': "<i>(Icône de crise : tant que cette manigance est en jeu, les joueurs ne peuvent pas réduire la valeur de manigance du méchant.)</i>\nTant que cette manigance est en jeu, les capacités imprimées des alliés [[SQUIRREL]] sont considérées comme vierges. Leur CTR, leur ATQ et leurs points de vie ne sont pas affectés.\n<b>Réponse Obligatoire</b> : après qu'un allié [[SQUIRREL]] est entré en jeu, placez 1 menace ici. (Limite d'une fois par round.)",
  // squirrel_girl — Poisoned Rumors (Treachery)
  '75021': "<b>Une fois révélée</b> : défaussez 2 alliés [[SQUIRREL]] que vous contrôlez. Si vous ne pouvez pas, placez 2 menaces sur Discord in the Branches. Si cette manigance n'est pas en jeu, placez plutôt ces menaces sur la manigance principale.\n[star] <b>Boost</b> : après la fin de cette activation, inclinez 1 allié [[SQUIRREL]] que vous contrôlez.",
  // squirrel_girl — Ratatoskr's Whispers (Attachment)
  '75022': "Attachez-la à votre carte d'identité.\nVous ne pouvez pas dépenser d'alliés [[SQUIRREL]].\n<b>Action d'identité civile</b> : inclinez Doreen Green et défaussez de votre main une carte ayant une ressource [mental] imprimée → défaussez Ratatoskr's Whispers.\n[star] <b>Boost</b> : défaussez 1 allié [[SQUIRREL]] que vous contrôlez. Si vous ne pouvez pas, cette activation gagne +1 ATQ et +1 MNG.",
}

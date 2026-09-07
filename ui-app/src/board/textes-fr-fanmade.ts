// textes-fr-fanmade.ts — texte francais des cartes sans scan francais.
//
// ECRIT A LA MAIN, ne pas confondre avec textes-fr.ts qui est GENERE depuis
// marvelcdb : ces cartes n'ont aucune source en ligne et n'auront jamais de
// scan francais. C'est donc le seul francais que le joueur verra dessus.
//
// PIEGE : le catalogue du jeu tient en DEUX fichiers, data/cards.json ET
// data/cards_custom.json. Rescue, Hulk (Rainy) et Stan Lee ne vivent que dans
// le second : ne lire que le premier les laisse muettes, sans que rien ne le
// signale. Classer les packs par tranche de code (« 61 a 75 ») est faux pour la
// meme raison : il y en a en 76xxx, 78xxx et 90xxx.
//
// Conventions, alignees sur la traduction officielle FFG/Asmodee :
//  - mots-cles de mots-cles.ts (Renfort, Deferlement, Robuste, Coup Rapide) ;
//  - statistiques ATQ, CTR, DEF, REC, MNG ;
//  - aspects Agressivite, Justice, Leadership, Protection ;
//  - NOMS PROPRES et traits [[...]] laisses en anglais : le joueur a la carte
//    anglaise sous les yeux et doit s'y retrouver ;
//  - jetons de jeu ([mental], [star], [per_hero]...) recopies tels quels.
//
// Ne sont PAS ici les cartes de defi (« challenges ») : leur identifiant n'a pas
// le format d'un code de carte, le plateau ne les affiche donc jamais.
export const TEXTES_FR_FANMADE: Readonly<Record<string, string | undefined>> = {
  // vision — Intangible (Upgrade)
  '26002a': "Forme de masse. Permanent.\nVision ne peut ni attaquer ni se défendre.\nRéduisez de 2 les dégâts que Vision subit de chaque attaque.",
  // vision — Dense (Upgrade)
  '26002b': "Forme de masse. Permanent.",
  // aos — A.I.M. Interference ([mental]) (Treachery)
  '50184b': "Incitation 1.\n<b>Une fois révélée</b> : placez 1 compteur de secret sur chaque carte [[Board Member]]. Vous pouvez dépenser X ressources [mental] pour empêcher X de ces compteurs d'être placés.\n<hr />\n[star] <b>Boost</b> : résolvez la capacité \"<b>Une fois révélée</b>\" de cette carte.",
  // aos — A.I.M. Interference ([physical]) (Treachery)
  '50184c': "Incitation 1.\n<b>Une fois révélée</b> : placez 1 compteur de secret sur chaque carte [[Board Member]]. Vous pouvez dépenser X ressources [physical] pour empêcher X de ces compteurs d'être placés.\n<hr />\n[star] <b>Boost</b> : résolvez la capacité \"<b>Une fois révélée</b>\" de cette carte.",
  // fne — Daredevil (Hero)
  '60001a': "<i>Sens surhumains</i> — <b>Action</b> : jouez la carte du dessus du deck [[Sense]] comme si elle était dans votre main <i>(en payant son coût)</i>.",
  // fne — Matt Murdock (AlterEgo)
  '60001b': "Matt Murdock commence la partie avec un deck [[Sense]]. <i>(Voir le livret de règles p. 26.)</i>\n<b>Interruption forcée</b> : quand une amélioration [[Sense]] devrait quitter le jeu, placez-la plutôt sous le deck [[Sense]].",
  // fne — Acute Tactility (Upgrade)
  '60002': "Attachez-la à un ennemi ou à une manigance.\n<b>Interruption</b> : quand vous mettez K.O. l'ennemi attaché ou retirez la dernière menace de la manigance attachée, défaussez cette carte → redressez votre identité.",
  // fne — Enhanced Olfaction (Upgrade)
  '60003': "Attachez-la à un ennemi ou à une manigance.\n<b>Interruption</b> : quand vous mettez K.O. l'ennemi attaché ou retirez la dernière menace de la manigance attachée, défaussez cette carte → réduisez de 2 le coût de la prochaine carte que vous jouez durant cette phase.",
  // fne — Heightened Hearing (Upgrade)
  '60004': "Attachez-la à un ennemi.\n<b>Interruption de héros</b> <i>(défense)</i> : quand l'ennemi attaché attaque, défaussez cette carte → cet ennemi subit -3 ATQ pour cette attaque. <i>(Vous devenez la cible de cette attaque.)</i>",
  // fne — Radar Sense (Upgrade)
  '60005': "Attachez-la à un ennemi.\n<b>Réponse</b> <i>(attaque)</i> : après avoir attaqué l'ennemi attaché, défaussez cette carte → infligez 3 dégâts à cet ennemi.",
  // fne — Superior Taste (Upgrade)
  '60006': "Attachez-la à une manigance.\n<b>Réponse</b> <i>(contre)</i> : après avoir contré la manigance attachée, défaussez cette carte → retirez 2 menaces de cette manigance.",
  // fne — Elektra (Ally)
  '60007': "[star] <b>Interruption forcée (Héros)</b> : quand Elektra devrait subir des dégâts consécutifs, Daredevil les subit à sa place.",
  // fne — Cross-Examination (Event)
  '60008': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Pour chaque amélioration attachée à cet ennemi, vous pouvez lui infliger 1 dégât supplémentaire.",
  // fne — Deposition (Event)
  '60009': "<b>Action d'alter ego</b> <i>(contre)</i> : vous pouvez choisir n'importe quelle amélioration du deck [[Sense]] et la jouer en ignorant son coût en ressources. <i>(Ne mélangez pas.)</i> Retirez 2 menaces d'une manigance.",
  // fne — Living Lie Detector (Event)
  '60010': "<b>Action</b> <i>(contre)</i> : retirez 2 menaces d'une manigance. Pour chaque amélioration attachée à cette manigance, vous pouvez en retirer 1 menace supplémentaire.",
  // fne — Raising Hell (Event)
  '60011': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à chaque ennemi par amélioration attachée à cet ennemi (3 dégâts à la place si Daredevil a le trait [[Aerial]]).",
  // fne — Focus the Senses (PlayerSideScheme)
  '60012': "La menace de cette manigance ne peut être retirée que par Daredevil ou Matt Murdock.\n<b>Une fois déjouée</b> : vous pouvez déplacer autant d'améliorations [[Sense]] en jeu que vous le souhaitez vers d'autres cartes auxquelles elles peuvent s'attacher. Choisissez autant d'améliorations du deck [[Sense]] que vous le souhaitez et mettez-les en jeu. <i>(Ne mélangez pas.)</i>",
  // fne — Foggy Nelson (Support)
  '60013': "<b>Action d'alter ego</b> : inclinez Foggy Nelson → retirez 2 menaces d'une manigance.",
  // fne — Karen Page (Support)
  '60014': "<b>Action</b> : inclinez Karen Page → mélangez 1 carte Daredevil de votre pile de défausse dans votre deck. Si vous êtes sous forme d'alter ego, piochez 1 carte.",
  // fne — Nelson and Murdock (Support)
  '60015': "<b>Réponse</b> : après qu'un personnage ou un soutien [[Attorney]] a déjoué une manigance annexe, désorientez un ennemi.",
  // fne — Sister Maggie (Support)
  '60016': "Matt Murdock gagne +3 REC.\n<b>Réponse</b> : après avoir récupéré, défaussez une carte d'état de votre identité.",
  // fne — Daredevil's Billy Club (Upgrade)
  '60017': "Restreint. Daredevil gagne +1 ATQ.\n<b>Action de héros</b> : renvoyez cette carte dans votre main <i>(depuis le jeu)</i> → choisissez :\n• Infligez 1 dégât à un ennemi.\n• Daredevil gagne le trait [[Aerial]] jusqu'à la fin du round.",
  // fne — The Man Without Fear (Upgrade)
  '60018': "<b>Action de héros</b> : inclinez cette carte et infligez 1 dégât à Daredevil → choisissez :\n• Choisissez n'importe quelle amélioration du deck [[Sense]] et jouez-la en ignorant son coût en ressources. <i>(Ne mélangez pas.)</i>\n• Redressez Daredevil.",
  // fne — Blindspot (Ally)
  '60019': "[star] <b>Réponse</b> : après que Blindspot a contré, désorientez un ennemi ayant une amélioration attachée.",
  // fne — Cloak (Ally)
  '60020': "<b>Action</b> : inclinez Cloak et dépensez des ressources [energy] [energy] → trouvez Dagger et mettez-la en jeu.",
  // fne — Dagger (Ally)
  '60021': "Cloak perd chaque icône [acceleration].\n[star] Si Cloak est en jeu, Dagger subit -1 dégât consécutif après avoir utilisé un pouvoir de base.",
  // fne — Ghost Rider (Ally)
  '60022': "[star] <b>Interruption</b> : quand Ghost Rider attaque un ennemi, dépensez une ressource [energy] (des ressources [energy] [energy] à la place si cet ennemi est le méchant) → désorientez cet ennemi.",
  // fne — Know Your Enemy (Event)
  '60023': "[star] Réduction 1 ([[Martial Artist]]).\n<b>Action de héros</b> <i>(contre)</i> : retirez 1 menace d'une manigance. Retirez 1 menace d'une manigance.",
  // fne — De-escalation (PlayerSideScheme)
  '60024': "Victoire 0.\n<b>Une fois déjouée</b> : retirez un jeton d'accélération du jeu.",
  // fne — Legal Trouble (Upgrade)
  '60026': "[star] Réduction 1 ([[Attorney]] ou [[Police]]).\nAttachez-la à un sbire. 1 max par sbire.\nLe sbire attaché subit -2 MNG.",
  // fne — Move in Shadow (Upgrade)
  '60027': "[star] Réduction 1 ([[Martial Artist]] ou [[Spy]]).\nTemporaire. 1 max par joueur.\n<b>Réponse</b> <i>(contre)</i> : après avoir joué une carte <i>(y compris celle-ci)</i>, retirez 1 menace d'une manigance.",
  // fne — Stealth Training (Upgrade)
  '60028': "Jouez-la sous le contrôle de n'importe quel joueur. 1 max par joueur.\n<b>Réponse</b> : après avoir contré et déjoué exactement une manigance annexe, inclinez Stealth Training → sonnez un ennemi.",
  // fne — Stick (Support)
  '60029': "<b>Interruption</b> : quand un personnage allié [[Martial Artist]] utilise un pouvoir de base, choisissez :\n• Inclinez Stick → ce personnage gagne +1 à ce pouvoir de base pour cette utilisation.\n• Ce personnage subit -1 à ce pouvoir de base pour cette utilisation. Redressez Stick.",
  // fne — Contingency Planning (Upgrade)
  '60030': "1 max par joueur.\nVous pouvez jouer l'amélioration glissée sous cette carte comme si elle était dans votre main.\n<b>Action</b> : choisissez 1 amélioration de votre main pouvant s'attacher à un sbire ou à une manigance annexe. Glissez cette amélioration sous cette carte (maximum 1).",
  // fne — Dance with the Devil (Upgrade)
  '60031': "En Équipe (Daredevil et Elektra). 1 max par deck.\nAttachez-la à un ennemi.\n<b>Action de héros</b> <i>(attaque)</i> : défaussez cette carte → infligez 3 dégâts à l'ennemi attaché.",
  // fne — Sensory Overload (Obligation)
  '60032': "<b><i>Donnez-la au joueur Matt Murdock.</i></b>\n<b>Réponse forcée</b> : après qu'une amélioration [[Sense]] est entrée en jeu, subissez 1 dégât.\n<b>Réponse d'alter ego</b> : après avoir récupéré, défaussez cette carte.",
  // fne — Bullseye (Minion)
  '60033': "<b>Une fois révélée</b> : choisissez :\n• Défaussez un soutien [[Persona]] que vous contrôlez.\n• Bullseye vous attaque <i>(même sous forme d'alter ego)</i>.",
  // fne — Deadliest Man Alive (SideScheme)
  '60034': "<b>Interruption forcée</b> : quand Bullseye attaque, donnez-lui une carte de boost face cachée.",
  // fne — Stolen Sai (Attachment)
  '60035': "Attachez-la à l'ennemi ayant l'ATQ la plus élevée.\n[star] Les attaques du personnage attaché gagnent perçant.\n<b>Action de héros</b> : dépensez des ressources [physical] [physical] → choisissez soit d'attacher cette carte à Elektra, soit de la défausser.\n<hr />\n[star] <b>Boost</b> : si cette activation est une attaque, elle gagne perçant.",
  // fne — Eye on the Target (Treachery)
  '60036': "<b>Une fois révélée</b> : choisissez :\n• Retirez de la partie un allié ou un soutien [[Persona]] que vous contrôlez.\n• Bullseye vous attaque <i>(même sous forme d'alter ego)</i>. S'il n'est pas en jeu, trouvez-le et révélez-le.",
  // fne — Echo (Hero)
  '60037a': "<i>Observer et apprendre</i> — <b>Réponse</b> : après qu'un joueur a joué un événement d'aspect ou de base, glissez cet événement sous cette carte depuis la pile de défausse de ce joueur. Puis, s'il y a plus de 3 cartes glissées ici, défaussez-les toutes sauf 3.",
  // fne — Maya Lopez (AlterEgo)
  '60037b': "<i>C'est en forgeant qu'on devient forgeron</i> — <b>Interruption</b> : quand vous passez sous forme de héros, cherchez un événement d'aspect ou de base dans votre deck et ajoutez-le à votre main. <i>(Mélangez.)</i>",
  // fne — Innate Reflexes (Upgrade)
  '60038': "Mise en place.\nVotre héros gagne +1 DEF.",
  // fne — Daredevil (Ally)
  '60039': "[star] <b>Réponse</b> : après que Daredevil a utilisé un pouvoir de base, réduisez de 1 le coût du prochain événement que vous jouez ce round.",
  // fne — Photographic Reflexes (Event)
  '60040a': "[star] Si vous êtes sous forme de héros, vous pouvez défausser Photographic Reflexes de votre main pour jouer un événement glissé sous Echo comme s'il était dans votre main. Réduisez de 2 le coût pour jouer cet événement. Vous ne pouvez pas déclencher la capacité <i>\"Observer et apprendre\"</i> d'Echo pour cet événement.",
  // fne — Photographic Reflexes (Event)
  '60040b': "[star] Si vous êtes sous forme de héros, vous pouvez défausser Photographic Reflexes de votre main pour jouer un événement glissé sous Echo comme s'il était dans votre main. Réduisez de 2 le coût pour jouer cet événement. Vous ne pouvez pas déclencher la capacité <i>\"Observer et apprendre\"</i> d'Echo pour cet événement.",
  // fne — Photographic Reflexes (Event)
  '60040c': "[star] Si vous êtes sous forme de héros, vous pouvez défausser Photographic Reflexes de votre main pour jouer un événement glissé sous Echo comme s'il était dans votre main. Réduisez de 2 le coût pour jouer cet événement. Vous ne pouvez pas déclencher la capacité <i>\"Observer et apprendre\"</i> d'Echo pour cet événement.",
  // fne — Study the Tape (Event)
  '60041': "<b>Action</b> : cherchez dans la pile de défausse de n'importe quel joueur 1 événement d'aspect, 1 événement de base ou 1 exemplaire de Photographic Reflexes, et ajoutez cette carte à votre main.",
  // fne — The Rez (Support)
  '60042': "<b>Action d'alter ego</b> : inclinez The Rez → soignez X dégâts de Maya Lopez, où X est le coût le plus élevé parmi les cartes glissées sous elle.",
  // fne — American Sign Language (Upgrade)
  '60043': "<b>Ressource de héros</b> : inclinez cette carte → générez une ressource [wild] pour un événement joué par n'importe quel joueur.",
  // fne — Choreography (Upgrade)
  '60044': "<b>Action</b> : inclinez cette carte → mélangez 1 événement d'aspect ou de base de votre pile de défausse dans votre deck. Si vous êtes sous forme d'alter ego, piochez 1 carte.",
  // fne — Echo's Katana (Upgrade)
  '60045': "Restreint.\n<b>Réponse de héros</b> <i>(attaque)</i> : après avoir joué un événement, inclinez Echo's Katana → infligez à un ennemi un nombre de dégâts égal au coût imprimé de cet événement. Cette attaque gagne perçant.",
  // fne — Improvisation (Upgrade)
  '60046': "<b>Réponse de héros</b> : après avoir joué un événement, s'il a les traits suivants :\n• [[Attack]] — soignez 1 dégât d'Echo.\n• [[Defense]] — retirez 1 menace d'une manigance.\n• [[Thwart]] — infligez 1 dégât à un ennemi.",
  // fne — Muscle Memory (Upgrade)
  '60047': "<b>Action de héros</b> : inclinez cette carte → ajoutez à votre main un événement glissé sous Echo.",
  // fne — Army of One (Event)
  '60048': "[star] Augmentez de 1 le coût pour jouer cette carte par allié que vous contrôlez.\n<b>Action de héros</b> : redressez votre héros.",
  // fne — Get Their Attention (Event)
  '60049': "<b>Interruption de héros</b> <i>(défense/contre)</i> : quand un ennemi initie une attaque, retirez 3 menaces d'une manigance.",
  // fne — In Harm's Way (Event)
  '60050': "[star] Augmentez de 1 le coût pour jouer cette carte par allié que vous contrôlez.\n<b>Action de héros</b> <i>(attaque/contre)</i> : infligez X dégâts à un ennemi et retirez X menaces d'une manigance, où X est votre DEF.",
  // fne — The Best Offense... (Upgrade)
  '60052': "Temporaire.\nVotre héros gagne +1 DEF.\nUtilisez votre DEF à la place de votre CTR et de votre ATQ. <i>(Ignorez tout modificateur de votre CTR et de votre ATQ.)</i>",
  // fne — Ronin (Upgrade)
  '60053': "Tant que vous ne contrôlez aucun allié, votre héros gagne +1 DEF et riposte 1.",
  // fne — Stand Alone (Upgrade)
  '60054': "1 max par joueur.\n<b>Interruption de héros</b> : quand un ennemi vous attaque <i>(avant qu'un défenseur ne soit déclaré)</i>, si vous ne contrôlez aucun allié, inclinez Stand Alone → redressez votre héros.",
  // fne — See No Evil, Hear No Evil (Event)
  '60055': "En Équipe (Daredevil et Echo). 1 max par deck.\n<b>Action de héros</b> <i>(attaque/contre)</i> : choisissez 2 des options suivantes (vous pouvez choisir deux fois la même) :\n• Infligez 3 dégâts à un ennemi.\n• Retirez 3 menaces d'une manigance.",
  // fne — Raised by the Kingpin (Obligation)
  '60060': "<b><i>Donnez-la au joueur Maya Lopez.</i></b>\nVous ne pouvez pas infliger de dégâts à Kingpin.\n<b>Une fois révélée</b> : trouvez Kingpin et mettez-le en jeu, engagé avec vous.\n<b>Réponse</b> : après avoir contré, placez cette menace ici. S'il y a 4 menaces ou plus ici, retirez cette carte de la partie.",
  // fne — Kingpin (Minion)
  '60061': "[star] <b>Interruption forcée</b> : quand Kingpin devrait attaquer le joueur Maya Lopez, il manigance à la place.\n<i>(Sbire nemesis d'Echo.)</i>",
  // fne — Master Manipulator (SideScheme)
  '60062': "Kingpin ne peut pas subir de dégâts.\n<b>Une fois révélée</b> : trouvez Kingpin et mettez-le en jeu, engagé avec vous.\n<hr />\n[star] <b>Boost</b> : si Kingpin est en jeu, révélez cette manigance.",
  // fne — Kingpin's Henchman (Minion)
  '60063': "Garde.\nKingpin ne peut pas subir de dégâts.",
  // fne — Pawn of the Kingpin (Treachery)
  '60064': "<b>Une fois révélée (alter ego)</b> : si Kingpin est en jeu, il manigance. Sinon, cette carte gagne renfort.\n<b>Une fois révélée (héros)</b> : infligez à un héros un nombre de dégâts égal à l'ATQ de votre héros.",
  // rainy — Thor (Hero)
  'ra001a': "Digne — <b>Action</b> : cherchez l'amélioration Mjolnir dans votre deck et votre pile de défausse, et ajoutez-la à votre main. Mélangez votre deck. (Limite d'une fois par round.)",
  // rainy — Jane Foster (AlterEgo)
  'ra001b': "Survivante — Jane Foster gagne +1 en taille de main tant que son obligation Chimiothérapie est mise de côté ou retirée de la partie.\nMédecin — <b>Action</b> : soignez 1 dégât d'un autre personnage allié. (Limite d'une fois par round.)",
  // rainy — Odinson (Ally)
  'ra002': "Multivers.\n[star] <b>Réponse</b> : après qu'Odinson a attaqué, choisissez un joueur. Infligez 1 dégât à chaque sbire engagé avec ce joueur.",
  // rainy — Roz Solomon (Ally)
  'ra003': "[star] <b>Interruption</b> : quand Roz Solomon contre, inclinez Congress of Worlds ou une carte [[S.H.I.E.L.D]] que vous contrôlez → elle gagne +2 CTR pour cette utilisation.",
  // rainy — Hammer Swing (Event)
  'ra004': "<b>Action de héros</b> <i>(attaque)</i> : inclinez Mjolnir et dépensez 1 ressource de n'importe quel type → infligez 4 dégâts à un ennemi.\n<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, inclinez Mjolnir → prévenez tous ces dégâts.",
  // rainy — Lightning Strike (Event)
  'ra005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 6 dégâts à un ennemi et 1 dégât à chaque ennemi engagé avec vous. Si vous avez payé cette carte en n'utilisant que des ressources [energy], sonnez un ennemi.",
  // rainy — Stand Fast (Event)
  'ra006': "<b>Action de héros</b> : redressez Thor et Mjolnir. Si vous avez payé cette carte en n'utilisant que des ressources [energy], donnez une carte d'état Tenace à Thor.",
  // rainy — Mjolnir (Upgrade)
  'ra007': "Restreint.\nThor gagne +1 ATQ et le trait [[AERIAL]].\n<b>Action de héros</b> <i>(attaque)</i> : défaussez Mjolnir → infligez 2 dégâts à un ennemi. Cette attaque gagne à distance.",
  // rainy — Unyielding (Upgrade)
  'ra008': "<b>Réponse de héros</b> <i>(contre)</i> : après avoir été attaqué sans subir de dégâts, inclinez Unyielding → retirez 2 menaces d'une manigance. Vous pouvez dépenser 1 ressource de n'importe quel type pour redresser votre héros.",
  // rainy — Congress of Worlds (Support)
  'ra009': "<b>Action d'alter ego</b> : inclinez Congress of Worlds et dépensez 1 ressource de n'importe quel type → retirez 2 menaces de la manigance principale ou 3 menaces d'une manigance annexe.",
  // rainy — Medical Clinic (Support)
  'ra010': "Jane Foster gagne +2 REC.\n<b>Action d'alter ego</b> : inclinez Medical Clinic et dépensez 1 ressource → soignez 3 dégâts d'une identité.",
  // rainy — Scrying Pool (Support)
  'ra011': "<b>Action de héros</b> : inclinez Scrying Pool → regardez la carte du dessus d'un deck. Vous pouvez défausser cette carte. Si une traîtrise a été regardée de cette façon, retirez 1 menace d'une manigance. Si un événement a été regardé de cette façon depuis un deck de joueur, ce joueur pioche 1 carte.",
  // rainy — Goddess of Thunder (Upgrade)
  'ra012': "<b>Ressource de héros</b> : inclinez Goddess of Thunder → générez une ressource [energy], ou [energy][energy] à la place pour une carte Thor.",
  // rainy — Mighty (Upgrade)
  'ra013': "Vous gagnez +2 points de vie.\nThor gagne +1 DEF et riposte 1.",
  // rainy — Chemotherapy (Obligation)
  'ra026': "Donnez-la au joueur Jane Foster.\nPassez sous forme d'alter ego. Choisissez :\n- Inclinez Jane Foster et Medical Clinic → retirez Chimiothérapie de la partie.\n- Choisissez soit de défausser 2 cartes, soit de subir 2 dégâts. Défaussez cette obligation.",
  // rainy — War of the Realms (SideScheme)
  'ra027': "<b>Une fois révélée</b> : chaque joueur subit 1 dégât indirect par personnage qu'il contrôle.",
  // rainy — Malekith (Minion)
  'ra028': "[star] <b>Réponse forcée</b> : après que Malekith s'est activé, chaque joueur subit 1 dégât indirect.",
  // rainy — War Witches (Minion)
  'ra029': "[star] <b>Interruption forcée</b> : quand War Witches devraient attaquer, elles manigancent à la place.\n<b>Réponse forcée</b> : après que de la menace a été placée sur la manigance principale, le joueur engagé subit 1 dégât indirect.",
  // rainy — Execute (Treachery)
  'ra030': "<b>Une fois révélée</b> : mettez K.O. l'allié en jeu ayant le plus de points de vie restants. Si aucun allié n'a été mis K.O. de cette façon, cette carte gagne renfort.",
  // rainy — Hostile Takeover (Treachery)
  'ra031': "<b>Une fois révélée</b> : choisissez soit de défausser le soutien que vous contrôlez ayant le coût le plus élevé, soit de subir un nombre de dégâts égal à son coût (ces dégâts ignorent les cartes d'état Tenace). Si aucun soutien n'a été défaussé et qu'aucun dégât n'a été subi de cette façon, cette carte gagne renfort.",
  // albert — Albert (Hero)
  'ab001a': "<i>Protocole d'initialisation</i> — <b>Spéciale</b> : piochez 1 carte. Après avoir joué cette carte ce round, redressez Albert.\n<b>Action</b> : résolvez la capacité \"<i>Protocole d'initialisation</i>\" d'Albert. (Limite d'une fois par round.)",
  // albert — Albert (AlterEgo)
  'ab001b': "<i>Développement poussé</i> — <b>Mise en place</b> : cherchez une amélioration [[Enhancement]] dans votre deck et votre pile de défausse, et mettez-la en jeu.",
  // albert — Elsie-Dee (Ally)
  'ab002': "<b>Interruption</b> : quand Elsie-Dee devrait être mise K.O. en subissant des dégâts en excès, répartissez X dégâts entre les ennemis en jeu, où X est égal à l'excédent.",
  // albert — Guard Protocol (Event)
  'ab003': "<b>Action de héros</b> : jusqu'à la fin du round, Albert gagne riposte 1 tant qu'il est sous forme de héros. Donnez une carte d'état Tenace à Albert. S'il en a déjà une, résolvez la capacité \"<i>Protocole d'initialisation</i>\" d'Albert.",
  // albert — Lethal Directive (Event)
  'ab004': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Si cet ennemi est mis K.O. par cette attaque, résolvez la capacité \"<i>Protocole d'initialisation</i>\" d'Albert.",
  // albert — Sabotage Sequence (Event)
  'ab005': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Si ce contre retire la dernière menace de cette manigance, résolvez la capacité \"<i>Protocole d'initialisation</i>\" d'Albert.",
  // albert — System Relaunch (Event)
  'ab006': "<b>Action d'alter ego</b> : soignez un nombre de dégâts d'Albert égal à votre REC et passez sous forme de héros → résolvez la capacité \"<i>Protocole d'initialisation</i>\" d'Albert.",
  // albert — Donald Pierce (Support)
  'ab007': "<b>Ressource</b> : inclinez Donald Pierce → générez une ressource [wild].\n<b>Réponse</b> : après avoir résolu la capacité \"<i>Protocole d'initialisation</i>\" d'Albert, redressez cette carte.",
  // albert — Adamantium Claws (Upgrade)
  'ab008': "Tant qu'il est sous forme de héros, Albert gagne +1 ATQ et ses attaques de base gagnent perçant.",
  // albert — Genius-Level Intellect (Upgrade)
  'ab009': "Vous gagnez le trait [[Genius]].\nTant qu'il est sous forme de héros, Albert gagne +1 CTR.",
  // albert — Kevlar Shell (Upgrade)
  'ab010': "Tant qu'il est sous forme de héros, Albert gagne +1 DEF et riposte 1.",
  // albert — Counterpart Elimination (Obligation)
  'ab011': "Donnez-la au joueur Albert.\nVous ne pouvez pas résoudre la capacité \"<i>Protocole d'initialisation</i>\" d'Albert.\n<b>Une fois révélée</b> : trouvez un sbire [[Wolverine]] et révélez-le.\n<b>Réponse</b> : après qu'un sbire [[Wolverine]] a été mis K.O., défaussez cette carte.",
  // albert — Wolverine (Minion)
  'ab012': "<b>Réponse forcée</b> : après que vous avez attaqué Wolverine, soignez 1 dégât de ce dernier.\n<i>(Sbire nemesis d'Albert.)</i>\n[star] <b>Boost</b> : mettez ce sbire en jeu, engagé avec le joueur Albert.",
  // albert — Crack in the Multiverse (SideScheme)
  'ab013': "Entrave 2[per_hero].\n<b>Réponse forcée</b> : après la fin de la phase des joueurs, le premier joueur trouve un sbire [[Wolverine]] et le révèle.",
  // albert — Patch (Minion)
  'ab014': "Riposte 1.\n<b>Une fois révélée</b> : infligez 1 dégât à chaque joueur.",
  // albert — Weapon X (Minion)
  'ab015': "Coup Rapide.\n<b>Une fois révélée</b> : défaussez 1 carte au hasard de votre main.",
  // albert — Zombie Wolvie (Minion)
  'ab016': "<b>Une fois vaincu</b> : mélangez Zombie Wolvie dans le deck rencontre.",
  // gwenpool — Gwenpool (Hero)
  'gp001a': "<i>Conscience du support</i> — <b>Interruption</b> : quand vous résolvez une capacité d'une carte Gwenpool, remplacez \"____\" par une phrase issue d'une bulle de dialogue. (Utilisez les bulles d'une carte que vous jouez, d'une carte que vous dépensez, ou d'une carte en jeu.) (Limite de chaque bulle une fois par phase.)\n<i>Bulle de dialogue : « Piochez 1 carte. »</i>",
  // gwenpool — Gwendolyn Poole (AlterEgo)
  'gp001b': "<i>« Je ne serai pas une figurante »</i> — <b>Action</b> : trouvez une carte Gwenpool et ajoutez-la à votre main. (Limite d'une fois par phase.)",
  // gwenpool — "Here I Come!" (Event)
  'gp002': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Cette attaque gagne déferlement. Si cette attaque met un ennemi K.O., ____.\n<i>Bulle de dialogue : « Infligez 2 dégâts au méchant. »</i>",
  // gwenpool — "It Can't End Like This!" (Event)
  'gp003': "<b>Action de héros</b> <i>(attaque/contre)</i> : infligez 1 dégât au méchant et retirez 1 menace de la manigance principale. Si le méchant a manigancé au round précédent, ____.\n<i>Bulle de dialogue : « Désorientez le méchant. »</i>",
  // gwenpool — Fun Background Noise (Event)
  'gp004': "<b>Interruption de héros</b> : quand une carte de traîtrise est révélée depuis le deck rencontre, annulez ses effets \"<b>Une fois révélée</b>\" et défaussez-la. Puis, ____.\n<i>Bulle de dialogue : « Donnez une carte d'état Tenace à Gwenpool. »</i>",
  // gwenpool — "Sorry, Gotta Run!" (Event)
  'gp005': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance. Ce contre ignore le mot-clé patrouille et les icônes de crise. Si ce contre déjoue une manigance, ____.\n<i>Bulle de dialogue : « Retirez 2 menaces de la manigance principale. »</i>",
  // gwenpool — Endless Storylines (Resource)
  'gp006': "<b>Réponse de héros</b> : après avoir dépensé cette carte, ____ et ____.\n<i>Bulles de dialogue : « Retirez 1 menace d'une manigance. » / « Soignez 1 dégât de Gwenpool. » / « Infligez 1 dégât à un ennemi. »</i>",
  // gwenpool — Gwen's Room (Support)
  'gp007': "Vous gagnez +1 REC.\n<b>Action d'alter ego</b> : inclinez Gwen's Room → soignez 1 dégât de Gwendolyn Poole. Puis, trouvez Unbelievable Gwenpool et ajoutez-la à votre main.\n<i>Bulle de dialogue : « Soignez 1 dégât de Gwenpool. »</i>",
  // gwenpool — Comicbook Panels (Upgrade)
  'gp008': "<b>Ressource de héros</b> : inclinez Comicbook Panels → générez une ressource [wild] et ____.\n<b>Action de héros</b> : inclinez Comicbook Panels et Unbelievable Gwenpool → ____ et ____.\n<i>Bulle de dialogue : « Regardez la carte du dessus de n'importe quel deck. »</i>",
  // gwenpool — Unbelievable Gwenpool (Upgrade)
  'gp009': "<b>Action d'alter ego</b> : inclinez Unbelievable Gwenpool → cherchez une carte Gwenpool dans votre deck et attachez-la ici face visible (maximum 1). <i>(Mélangez.)</i> Vous pouvez utiliser les bulles de dialogue de la carte attachée.\n<b>Action de héros</b> : piochez 2 cartes et ____. Défaussez Unbelievable Gwenpool.\n<i>Bulle de dialogue : « Redressez Gwenpool. »</i>",
  // gwenpool — THE END (Obligation)
  'gp010': "Donnez-la au joueur Gwendolyn Poole.\nVous ne pouvez pas utiliser les bulles de dialogue des cartes Gwenpool.\n<b>Action d'alter ego</b> : inclinez Gwendolyn Poole et défaussez Unbelievable Gwenpool → retirez THE END de la partie.",
  // gwenpool — Rules of the Universe (SideScheme)
  'gp011': "Permanent.\nTant qu'il n'y a pas de menace ici, cette manigance perd l'icône [hazard].\n<b>Interruption forcée</b> : quand vous résolvez une capacité d'une carte Gwenpool, remplacez \"____\" par la phrase de la bulle de dialogue d'Evil Gwenpool.",
  // gwenpool — Evil Gwenpool (Minion)
  'gp012': "Solide. Vilenie.\n<b>Une fois vaincue</b> : mélangez Evil Gwenpool dans le deck rencontre.\n<i>(Sbire nemesis de Gwenpool.)</i>\n[star] <b>Boost</b> : mettez Evil Gwenpool en jeu, engagée avec vous.\n<i>Bulle de dialogue : « Gwenpool subit 1 dégât. »</i>",
  // gwenpool — Break Reality (Treachery)
  'gp013': "Incitation 1.\n<b>Une fois révélée</b> : cherchez Evil Gwenpool dans le deck rencontre et révélez-la. <i>(Mélangez.)</i> Si Unbelievable Gwenpool est en jeu, elle gagne coup rapide. Si Evil Gwenpool était déjà en jeu, ajoutez 2[per_hero] menaces sur Rules of the Universe.",
  // gwenpool — "Future Me Scares Me" (Treachery)
  'gp014': "Incitation 0 (incitation 1 à la place, s'il s'agit d'une partie multijoueur).\nIncitation 1 (incitation 2 à la place, s'il s'agit d'une partie en mode expert).\n<b>Une fois révélée</b> : si Evil Gwenpool est en jeu, ajoutez 2 menaces sur Rules of the Universe et mélangez cette carte dans le deck rencontre.",
  // human_torch — Human Torch (Hero)
  'ht001a': "<i>Flamme à volonté !</i> — <b>Interruption</b> : quand vous placez un compteur de flamme sur un ennemi, infligez 1 dégât à cet ennemi. Un ennemi ne peut pas avoir plus de 3 compteurs de flamme sur lui.",
  // human_torch — Johnny Storm (AlterEgo)
  'ht001b': "<i>Ignition</i> — <b>Action</b> : inclinez Johnny Storm → cherchez une carte [[FIRE]] parmi les 4 cartes du dessus de votre deck et ajoutez-la à votre main. Si aucune carte n'a été ajoutée à votre main de cette façon, redressez Johnny Storm. (Limite d'une fois par round.)",
  // human_torch — The Thing (Ally)
  'ht002': "Ténacité.\n<b>Réponse</b> : après que The Thing s'est défendu, redressez-le. (Limite d'une fois par phase.)",
  // human_torch — Johnny's Workshop (Support)
  'ht003': "<b>Réponse</b> : après être passé à Johnny Storm, piochez 1 carte.\n<b>Réponse</b> : après être passé à Human Torch, redressez une carte [[FIRE]].",
  // human_torch — Unstable Uniform (Upgrade)
  'ht004': "Human Torch gagne +1 DEF.\n<b>Réponse de héros</b> : après avoir subi des dégâts d'une attaque, placez un compteur de flamme sur l'attaquant.",
  // human_torch — Internal Combustion (Upgrade)
  'ht005': "<b>Action de héros</b> : retirez 3 compteurs de flamme d'un ennemi et défaussez Internal Combustion → piochez 3 cartes.",
  // human_torch — Spark (Upgrade)
  'ht006': "<b>Ressource de héros</b> : inclinez Spark → générez une ressource [energy] pour une carte [[FIRE]].\n<b>Action de héros</b> : inclinez Spark → placez un compteur de flamme sur un ennemi.",
  // human_torch — Fly-By (Event)
  'ht007': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance, puis retirez 1 menace d'une manigance par compteur de flamme sur le méchant.",
  // human_torch — Blaze and Daze (Event)
  'ht008': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Puis, s'il a 3 compteurs de flamme sur lui, retirez tous ces compteurs et sonnez cet ennemi.",
  // human_torch — Radiate (Event)
  'ht009': "Choisissez l'un ou l'autre :\n<b>Action de héros</b> <i>(attaque)</i> : placez 2 compteurs de flamme sur X ennemis.\n<b>Action</b> : retirez tous les compteurs de flamme de X ennemis → changez de forme, puis soignez 1 dégât par compteur de flamme retiré de cette façon (maximum 5).",
  // human_torch — Nova Flame (Event)
  'ht010': "<b>Action de héros</b> <i>(attaque)</i> : inclinez Human Torch → placez jusqu'à 3 compteurs de flamme sur un ennemi, puis infligez 7 dégâts à cet ennemi. Cette attaque gagne déferlement.",
  // human_torch — Flame Off (Obligation)
  'ht011': "Donnez-la au joueur Johnny Storm.\nPassez sous forme d'alter ego et retirez tous les compteurs de flamme des ennemis en jeu. Puis :\n- Si jusqu'à 3 compteurs ont été retirés de cette façon, défaussez cette obligation.\n- Si 4 compteurs de flamme ou plus ont été retirés de cette façon, retirez Flame Off de la partie.",
  // human_torch — Hydro-Man (Minion)
  'ht012': "Aucun compteur de flamme ne peut être placé sur Hydro-Man.\n[star] <b>Boost</b> : mettez Hydro-Man en jeu, engagé avec vous.",
  // human_torch — Dam It (SideScheme)
  'ht013': "Hydro-Man est apparu et a éteint toutes les flammes !\n<b>Une fois révélée</b> : retirez tous les compteurs de flamme des ennemis en jeu. Puis, placez 1 menace supplémentaire ici par compteur de flamme retiré de cette façon.",
  // human_torch — Tidal Renfort (Treachery)
  'ht014': "Renfort.\n<b>Une fois révélée</b> : si Hydro-Man est en jeu, chaque joueur doit choisir soit d'incliner son identité, soit de subir 3 dégâts indirects.",
  // mister_fantastic — Mister Fantastic (Hero)
  'mf001a': "<i>Flexibilité</i> — <b>Réponse</b> : après avoir dépensé une carte [[SUPERPOWER]] comme ressource ou l'avoir défaussée de votre main sans la jouer, renvoyez-la dans votre main. (Limite d'une fois par phase.)",
  // mister_fantastic — Reed Richards (AlterEgo)
  'mf001b': "<i>Grands esprits</i> — <b>Ressource</b> : inclinez Reed Richards → générez une ressource [mental] ([mental][mental] à la place si Sue Storm est en jeu). Si vous avez payé une carte [[TECH]] avec les ressources de cette capacité, redressez Reed Richards. (Limite d'une fois par round.)",
  // mister_fantastic — Invisible Woman (Ally)
  'mf002': "<b>Réponse</b> : après qu'Invisible Woman est entrée en jeu, redressez votre identité.",
  // mister_fantastic — H.E.R.B.I.E. (Support)
  'mf003': "<b>Action</b> : inclinez H.E.R.B.I.E. → défaussez X cartes de votre main, puis piochez X cartes.\n<b>Action</b> : inclinez puis défaussez H.E.R.B.I.E. → piochez X cartes, puis défaussez X cartes de votre main.",
  // mister_fantastic — Baxter Building (Support)
  'mf004': "<b>Action d'alter ego</b> : inclinez Baxter Building → soignez 2 dégâts d'une identité.\n<b>Action de héros</b> : inclinez Baxter Building → cherchez une carte Mister Fantastic parmi les 4 cartes du dessus de votre deck, puis ajoutez-la à votre main (les 8 premières à la place si votre héros a 10 points de vie restants ou plus).",
  // mister_fantastic — Fantasticar (Support)
  'mf005': "Mister Fantastic gagne +1 en taille de main.\n<b>Action de héros</b> : inclinez Fantasticar → choisissez un joueur sous forme de héros. Réduisez de 1 le coût de la prochaine carte d'événement que ce joueur joue durant cette phase.",
  // mister_fantastic — Unstable Uniform (Upgrade)
  'mf006': "Mister Fantastic gagne +1 DEF.\n<b>Réponse de héros</b> : après vous être défendu contre une attaque, renvoyez dans votre main la carte Mister Fantastic la plus profonde de votre pile de défausse.",
  // mister_fantastic — Fantasti-Flare (Upgrade)
  'mf007': "Utilisations (4 compteurs de flare).\n<b>Action</b> : inclinez Fantasti-Flare et retirez-lui un compteur de flare → choisissez un joueur. Réduisez de 1 le coût du prochain allié que ce joueur joue durant cette phase.",
  // mister_fantastic — Neutralizer (Upgrade)
  'mf008': "Jouez-la sous le contrôle de n'importe quel joueur. Restreint. Utilisations (2 compteurs de charge).\n<b>Interruption de héros</b> : quand vous faites une attaque de base, inclinez Neutralizer et retirez-lui un compteur de charge → vous gagnez +3 ATQ pour cette attaque. Cette attaque gagne déferlement.",
  // mister_fantastic — Stretched Thin (Event)
  'mf009': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance. Puis, s'il ne vous reste aucune carte en main, retirez 1 menace de chaque manigance en jeu.",
  // mister_fantastic — Big Reach (Event)
  'mf010': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts au méchant. Puis, infligez X dégâts à un ennemi, où X est le nombre de cartes qu'il vous reste en main.",
  // mister_fantastic — Slippery (Event)
  'mf011': "<b>Interruption</b> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, prévenez 2 de ces dégâts et piochez 2 cartes.",
  // mister_fantastic — Mental Gymnastics (Event)
  'mf012': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 + X dégâts à un ennemi. Puis, s'il ne vous reste aucune carte en main, désorientez cet ennemi.",
  // mister_fantastic — Ben's Cure (Obligation)
  'mf013': "Donnez-la au joueur Reed Richards.\nVous pouvez passer sous forme d'alter ego. Choisissez :\n- Inclinez Reed Richards et défaussez une carte ayant une ressource [mental] imprimée → retirez Ben's Cure de la partie.\n- Subissez 1 dégât et placez 1 menace sur la manigance principale → défaussez cette obligation.",
  // mister_fantastic — Wizard (Minion)
  'mf014': "Chaque héros subit -1 CTR.",
  // mister_fantastic — Hubris (SideScheme)
  'mf015': "Wizard a un plan machiavélique en tête.\n<b>Une fois révélée</b> : placez X menaces supplémentaires ici, où X est le CTR cumulé de tous les héros.",
  // mister_fantastic — Projection (Attachment)
  'mf016': "Incitation 1. Renfort.\nAttachez-la à votre carte d'identité.\n[star] <b>Boost</b> : attachez-la à votre carte d'identité.",
  // mister_fantastic — Execution (Treachery)
  'mf017': "<b>Une fois révélée</b> : défaussez chaque attachement Projection en jeu. Pour chaque attachement défaussé de cette façon, chaque joueur doit choisir soit de défausser 2 cartes de sa main, soit de subir 2 dégâts indirects. Si aucun attachement Projection n'a été défaussé de cette façon, remélangez Execution dans le deck rencontre et cette carte gagne renfort.",
  // invisible_woman — Invisible Woman (Hero)
  'iw001a': "<i>Bouh !</i> — <b>Réponse forcée</b> : après avoir attaqué un ennemi, passez à votre autre forme de héros.",
  // invisible_woman — Sue Storm (AlterEgo)
  'iw001b': "<i>Grands esprits</i> — <b>Ressource</b> : inclinez Sue Storm → générez une ressource [mental] ([mental][mental] à la place si Reed Richards est en jeu). Si vous avez payé une carte [[TECH]] avec les ressources de cette capacité, redressez Sue Storm. (Limite d'une fois par round.)",
  // invisible_woman — Invisible Woman (Hero)
  'iw001c': "<i>Barrière invisible</i> — <b>Interruption</b> : quand un ennemi ayant 2 ATQ ou plus initie une attaque contre vous, infligez 1 dégât à cet ennemi.",
  // invisible_woman — Mister Fantastic (Ally)
  'iw002': "<b>Réponse</b> : après que Mister Fantastic est entré en jeu, retirez 1 menace de chaque manigance ou ajoutez la carte du dessus de votre pile de défausse à votre main.",
  // invisible_woman — Central City Estate (Support)
  'iw003': "Vous gagnez +1 REC.\n<b>Action d'alter ego</b> : inclinez Central City Estate → redressez Sue Storm.",
  // invisible_woman — Unstable Uniform (Upgrade)
  'iw004': "Invisible Woman gagne +1 DEF.\n<b>Réponse de héros</b> : après être passé sous forme de héros [[INVISIBLE]], vous gagnez +1 CTR jusqu'à la fin de ce tour.\n<b>Réponse de héros</b> : après être passé sous forme de héros [[PSIONIC]], vous gagnez +1 ATQ jusqu'à la fin de ce tour.",
  // invisible_woman — Flying Disk (Upgrade)
  'iw005': "Si vous êtes sous forme de héros [[PSIONIC]], vous gagnez le trait [[AERIAL]] et vos attaques gagnent à distance.\n<b>Action de héros</b> : défaussez Flying Disk → infligez 4 dégâts à un ennemi.",
  // invisible_woman — Vanishing Act (Upgrade)
  'iw006': "<b>Action de héros</b> : si vous êtes sous forme de héros [[INVISIBLE]], inclinez Vanishing Act et dépensez des ressources [mental][energy] → désorientez un ennemi.",
  // invisible_woman — Force Shields (Upgrade)
  'iw007': "<b>Action de héros</b> : si vous êtes sous forme de héros [[PSIONIC]], inclinez Force Shields et défaussez X cartes ayant une ressource [physical] imprimée → donnez une carte d'état Tenace à X personnages alliés.",
  // invisible_woman — Incognito (Event)
  'iw008': "Jouez-la uniquement si vous êtes sous forme de héros [[INVISIBLE]].\n<b>Action de héros</b> : regardez les 4 cartes du dessus du deck rencontre. Pour chaque icône étoile vue de cette façon, piochez 1 carte.",
  // invisible_woman — Infiltrate (Event)
  'iw009': "Jouez-la uniquement si vous êtes sous forme de héros [[INVISIBLE]].\n<b>Action de héros</b> <i>(contre)</i> : retirez jusqu'à 4 menaces d'une manigance ou jusqu'à 2 menaces de chaque manigance.",
  // invisible_woman — Forceful (Event)
  'iw010': "Jouez-la uniquement si vous êtes sous forme de héros [[PSIONIC]].\n<b>Action de héros</b> <i>(attaque)</i> : défaussez autant de cartes d'état Tenace que vous le souhaitez des personnages que vous contrôlez → infligez 3 dégâts au méchant par carte d'état Tenace défaussée de cette façon.",
  // invisible_woman — Psionic Fields (Event)
  'iw011': "Jouez-la uniquement si vous êtes sous forme de héros [[PSIONIC]].\n<b>Action de héros</b> <i>(attaque)</i> : choisissez 2 des options suivantes (vous pouvez choisir deux fois la même) :\n• Infligez 4 dégâts à un ennemi.\n• Sonnez un ennemi.",
  // invisible_woman — Spectral Shift (Event)
  'iw012': "<b>Action</b> : changez de forme. Puis, si vous êtes passé :\nsous forme de héros [[INVISIBLE]] - Piochez 2 cartes.\nsous forme de héros [[PSIONIC]] - Piochez 1 carte.",
  // invisible_woman — Family Time (Obligation)
  'iw013': "<b><i>Donnez-la au joueur Sue Storm.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Sue Storm → retirez Family Time de la partie.\n• Défaussez une carte de votre main → défaussez cette obligation.",
  // invisible_woman — Psycho-Man (Minion)
  'iw014': "<b>Réponse forcée</b> : après que Psycho-Man s'est activé, défaussez 4 cartes du deck rencontre. Si des cartes Nemesis d'Invisible Woman ont été défaussées de cette façon, révélez-les à la place.",
  // invisible_woman — Emotional Masterplan (SideScheme)
  'iw015': "Les héros ne peuvent pas changer de forme.\n<b>Action</b> : défaussez 2 cartes de votre main → considérez que la zone de texte imprimée de cette carte est vierge jusqu'à la fin de votre tour.",
  // invisible_woman — Microversal Maneuvers (Attachment)
  'iw016': "Attachez-la à Psycho-Man. Si vous ne pouvez pas, cette carte gagne renfort.\n<b>Réponse forcée</b> : après que Psycho-Man a manigancé contre vous, subissez 1 dégât indirect.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // invisible_woman — Titanic Terror (Attachment)
  'iw017': "Attachez-la à Psycho-Man. Si vous ne pouvez pas, cette carte gagne renfort.\n<b>Réponse forcée</b> : après que Psycho-Man a attaqué, placez 1 menace sur la manigance principale.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // invisible_woman — End of the Line (Treachery)
  'iw018': "<b>Une fois révélée</b> : défaussez les 8 cartes du dessus du deck rencontre. Si Microversal Maneuvers ou Titanic Terror sont défaussées de cette façon, révélez-les.",
  // the_thing — The Thing (Hero)
  'th001a': "<i>Vas-y !</i> — <b>Action</b> : défaussez une carte d'état Tenace de The Thing.\n<i>Prends ça !</i> — <b>Réponse</b> : après avoir défaussé une carte d'état Tenace de The Thing, vos attaques infligent 1 dégât supplémentaire jusqu'à la fin de la phase.",
  // the_thing — Ben Grimm (AlterEgo)
  'th001b': "<i>L'adorable Chose aux yeux bleus</i> — <b>Réponse</b> : après que Ben Grimm a soigné 4 dégâts ou plus, donnez-lui une carte d'état Tenace.",
  // the_thing — The Thing (Hero)
  'th001c': "<i>Vas-y !</i> — <b>Action</b> : défaussez une carte d'état Tenace de The Thing.\n<i>Prends ça !</i> — <b>Réponse</b> : après avoir défaussé une carte d'état Tenace de The Thing, vos attaques infligent 1 dégât supplémentaire jusqu'à la fin de la phase.",
  // the_thing — Ben Grimm (AlterEgo)
  'th001d': "<i>L'adorable Chose aux yeux bleus</i> — <b>Réponse</b> : après que Ben Grimm a soigné 4 dégâts ou plus, donnez-lui une carte d'état Tenace.",
  // the_thing — Human Torch (Ally)
  'th002': "<b>Réponse</b> : après que Human Torch est entré en jeu, choisissez l'un ou l'autre :\n- Infligez 1 dégât à The Thing, puis donnez-lui une carte d'état Tenace.\n- Infligez 3 dégâts au méchant.",
  // the_thing — Alicia Masters (Support)
  'th003': "<b>Action d'alter ego</b> : inclinez Alicia Masters → piochez 2 cartes.",
  // the_thing — Yancy Street Gang (Support)
  'th004': "<b>Action</b> : inclinez Yancy Street Gang → infligez 1 dégât à un personnage. Ces dégâts gagnent perçant. Si une carte d'état Tenace a été défaussée de cette façon, redressez Yancy Street Gang.",
  // the_thing — Unstable Uniform (Upgrade)
  'th005': "The Thing gagne +1 DEF.\n<b>Réponse de héros</b> : après vous être défendu contre une attaque, piochez une carte.",
  // the_thing — Rock 'Em (Event)
  'th006': "<b>Action de héros</b> <i>(contre)</i> : retirez 4 menaces d'une manigance. Si cela retire la dernière menace de cette manigance, donnez une carte d'état Tenace à The Thing ou désorientez le méchant.",
  // the_thing — True Grit (Upgrade)
  'th007': "<b>Action de héros</b> : infligez 2 dégâts à The Thing → redressez votre héros et défaussez-lui une carte d'état. (Maximum une fois par round.)",
  // the_thing — Toughen Up (Event)
  'th008': "<b>Réponse</b> : après avoir subi des dégâts, quel qu'en soit le nombre, donnez une carte d'état Tenace à votre identité.",
  // the_thing — Sock 'Em (Event)
  'th009': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Si cet ennemi est mis K.O. par cette attaque, donnez une carte d'état Tenace à The Thing ou piochez une carte.",
  // the_thing — It's Clobberin' Time! (Event)
  'th010': "<b>Action de héros</b> : faites les 2 attaques suivantes :\n- Infligez 4 dégâts à un ennemi.\n- Infligez 4 dégâts à un ennemi.",
  // the_thing — Annual Shedding (Obligation)
  'th011': "Donnez-la au joueur Ben Grimm.\nPassez sous forme d'alter ego. Choisissez l'un ou l'autre :\n- Défaussez une carte d'état Tenace de Ben Grimm → défaussez cette obligation.\n- Sonnez ou désorientez Ben Grimm → défaussez cette obligation.",
  // the_thing — Puppet Master (Minion)
  'th012': "Puppet Master ne peut pas être attaqué tant que Hulk est en jeu.\n<b>Réponse forcée</b> : après que Puppet Master a été révélé, cherchez Hulk dans le deck rencontre et révélez-le.\n<i>(Sbire nemesis de The Thing.)</i>",
  // the_thing — Pulling The Strings (SideScheme)
  'th013': "Le beau-père malgré lui de Ben Grimm a pris le contrôle de l'Incroyable Hulk !\nLe sbire en jeu ayant le MNG le plus faible gagne +1 ATQ et +1 MNG.",
  // the_thing — Hulk (Minion)
  'th014': "Garde.\n[star] Les attaques de Hulk gagnent perçant et déferlement.",
  // the_thing — Friendly Fire (Treachery)
  'th015': "<b>Une fois révélée</b> : vous subissez X dégâts, où X est l'ATQ du personnage allié ayant l'ATQ la plus élevée. Si votre identité est le seul personnage allié en jeu, cette carte gagne renfort.",
  // totally_awesome_hulk — Totally Awesome Hulk (Hero)
  'ah001a': "<i>Perte de contrôle</i> — Vous ne pouvez passer sous forme de héros [[BRUTE]] qu'en résolvant les effets du soutien \"The Trunk\".\n<i>Hyper-esprit</i> — Considérez toutes les ressources que vous générez comme des ressources [wild].",
  // totally_awesome_hulk — Amadeus Cho (AlterEgo)
  'ah001b': "<i>Rétro-ingénierie</i> — <b>Action</b> : défaussez une carte spécifique à votre héros de votre main → piochez X cartes, où X est le coût imprimé de la carte défaussée de cette façon. (Limite d'une fois par round.)",
  // totally_awesome_hulk — Uncontrollable Hulk (Hero)
  'ah001c': "<i>Incontrôlable</i> — Vous ne pouvez ni prendre ni quitter cette forme sans résoudre les effets du soutien \"The Trunk\".\n<b>Interruption</b> : quand vous attaquez, cette attaque inflige 2 dégâts supplémentaires.",
  // totally_awesome_hulk — Hercules (Ally)
  'ah002': "<b>Réponse</b> : après qu'Hercules a mis un sbire K.O., redressez-le.",
  // totally_awesome_hulk — Maddy Cho (Support)
  'ah003': "Totally Awesome Hulk gagne +1 en taille de main.\n<b>Action de héros</b> : inclinez Maddy Cho → ajoutez ou retirez 1 compteur de rage sur \"The Trunk\".",
  // totally_awesome_hulk — Kegger (Upgrade)
  'ah004': "<b>Ressource</b> : mélangez Kegger dans votre deck → générez une ressource [wild].\n<b>Action</b> : mélangez Kegger et une carte de votre main dans votre deck → redressez votre identité.",
  // totally_awesome_hulk — Motivation (Upgrade)
  'ah005': "Votre héros gagne +1 DEF.\n<b>Réponse de héros</b> : après que votre héros s'est défendu, subissez 2 dégâts → redressez votre héros.",
  // totally_awesome_hulk — Gamma Barrier (Upgrade)
  'ah006': "Votre héros gagne riposte 1.\n<b>Interruption</b> : quand vous devriez être sonné, défaussez cette carte → prévenez ce sonnage et sonnez le méchant à la place.",
  // totally_awesome_hulk — The Power of Forgiveness (Resource)
  'ah007': "<b>Réponse</b> : après avoir résolu les effets de la carte payée avec The Power of Forgiveness, retirez tous les compteurs de \"The Trunk\" et soignez 2 points de vie d'un autre personnage allié.",
  // totally_awesome_hulk — Calculated Strike (Event)
  'ah008': "<b>Action de héros</b> <i>(attaque/contre)</i> : retirez 2 menaces d'une manigance, puis infligez 3 dégâts au méchant. Si vous avez payé cette carte en n'utilisant que des ressources [wild], retirez 2 menaces supplémentaires.",
  // totally_awesome_hulk — Wild Lunge (Event)
  'ah009': "Vous ne pouvez dépenser que des ressources [wild] pour payer cette carte.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi.",
  // totally_awesome_hulk — Irradiated Swipe (Event)
  'ah010': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Si vous avez payé cette carte en n'utilisant que des ressources [wild], piochez 2 cartes.",
  // totally_awesome_hulk — Kinetic Stomp (Event)
  'ah011': "<b>Interruption de héros</b> : quand vous faites une attaque de base, vous gagnez +6 ATQ pour cette attaque. Si cette attaque inflige 10 dégâts ou plus, redressez votre héros.",
  // totally_awesome_hulk — "The Trunk" (Support)
  'ah012a': "<b>Réponse forcée</b> : après que Totally Awesome Hulk a subi des dégâts, quel qu'en soit le nombre, ajoutez un compteur de rage ici.\n<b>Interruption forcée</b> : quand il y a 4 compteurs de rage ici, retournez cette carte et passez en forme d'Uncontrollable Hulk.",
  // totally_awesome_hulk — "The Trunk" (Support)
  'ah012b': "<b>Réponse forcée</b> : après qu'Uncontrollable Hulk a attaqué, retirez un compteur de rage de cette carte.\n<b>Interruption forcée</b> : quand il n'y a plus de compteur de rage ici, retournez cette carte et passez en forme d'Amadeus Cho.",
  // totally_awesome_hulk — Get Under Control (Obligation)
  'ah013': "<b><i>Donnez-la au joueur Amadeus Cho.</i></b>\nVous ne pouvez pas mettre d'alliés en jeu.\n<b>Action d'alter ego</b> : considérez que la zone de texte imprimée de \"The Trunk\" est vierge, puis retirez \"The Trunk\" de la partie → retirez cette obligation de la partie.",
  // totally_awesome_hulk — Lady Hellbender (Minion)
  'ah014': "<b>Action de héros</b> : dépensez un nombre de ressources [wild] égal aux points de vie restants de Lady Hellbender → considérez Lady Hellbender comme une alliée que vous contrôlez, avec du CTR au lieu du MNG.\n<i>(Sbire nemesis de Totally Awesome Hulk.)</i>",
  // totally_awesome_hulk — For The Queen! (SideScheme)
  'ah015': "Tant que Lady Hellbender est en jeu, les sbires [[MONSTER]] gagnent vilenie.",
  // totally_awesome_hulk — Fin Fang Foom (Minion)
  'ah016': "<b>Une fois révélée</b> : Fin Fang Foom gagne +2 points de vie par joueur.\n<b>Interruption forcée</b> : quand il reste à Fin Fang Foom 2 points de vie par joueur ou moins, ses attaques gagnent déferlement.",
  // totally_awesome_hulk — Krackalakassian (Minion)
  'ah017': "<b>Une fois révélée</b> : Krackalakassian gagne +2 points de vie par joueur.\n<b>Interruption forcée</b> : quand Krackalakassian attaque, subissez 2 dégâts indirects.",
  // totally_awesome_hulk — Threat Assessment (Treachery)
  'ah018': "<b>Une fois révélée</b> : infligez 3 dégâts à l'identité ayant le plus de points de vie restants.",
  // madame_web — Madame Web (Hero)
  'mw001a': "<i>Un lien avec les alliés</i> — Madame Web gagne les <b>traits</b> de chaque allié que vous contrôlez.\nX est égal au nombre d'alliés que vous contrôlez (maximum 3).",
  // madame_web — Cassandra Webb (AlterEgo)
  'mw001b': "<i>Arachnophilie</i> — Vous pouvez inclure dans votre deck des alliés ayant le trait <b>WEB-WARRIOR</b> ou dont le titre contient \"Spider\", quel que soit leur aspect.\n<b>Mise en place</b> : cherchez l'amélioration Life-Support System dans votre deck et votre pile de défausse, et mettez-la en jeu.",
  // madame_web — Spider-Woman (Ally)
  'mw002': "Spider-Woman entre en jeu avec 2 compteurs de toile psionique.\n<b>Réponse</b> : après qu'une manigance annexe est entrée en jeu, retirez 1 compteur de toile psionique de Spider-Woman → retirez 2 menaces de cette manigance annexe.",
  // madame_web — Webb's Apartment (Support)
  'mw003': "<b>Action d'alter ego</b> : inclinez Webb's Apartment → soignez 1 dégât d'un personnage que vous contrôlez.",
  // madame_web — Clairvoyance (Upgrade)
  'mw004': "<b>Interruption de héros</b> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, inclinez Clairvoyance → prévenez 1 de ces dégâts.",
  // madame_web — Astral Form (Upgrade)
  'mw005': "<b>Action de héros</b> <i>(contre)</i> : inclinez Astral Form et dépensez une ressource [mental] → retirez X menaces réparties entre les manigances en jeu, où X est le nombre d'alliés que vous contrôlez.",
  // madame_web — Weaving a Web (Upgrade)
  'mw006': "<b>Ressource</b> : inclinez Weaving a Web → générez une ressource [wild] pour un allié.",
  // madame_web — Life-Support System (Upgrade)
  'mw007': "Vous gagnez +3 points de vie.\nCassandra Webb gagne +1 REC.\n<b>Interruption</b> : quand vous devriez être mis K.O. en défaussant cette carte, réglez plutôt votre cadran de points de vie sur 1.",
  // madame_web — Webb's Team Strikes! (Event)
  'mw008': "<b>Action de héros</b> <i>(attaque)</i> : inclinez jusqu'à X alliés que vous contrôlez → infligez 3 dégâts au méchant par allié incliné de cette façon.",
  // madame_web — Foresight (Event)
  'mw009': "<b>Interruption de héros</b> : quand vous révélez une carte rencontre, inclinez Madame Web → annulez les effets de cette carte et défaussez-la.",
  // madame_web — Gathering of Five (Event)
  'mw010': "<b>Action</b> : défaussez la carte du dessus de votre deck. Si la ressource imprimée de cette carte est :\n[physical] - Infligez 3 dégâts à votre identité.\n[energy] - Madame Web gagne +2 ATQ jusqu'à la fin de la phase.\n[mental] - Retirez 2 menaces d'une manigance.\n[wild] - Soignez tous les dégâts de votre identité.",
  // madame_web — Web of Fate (Resource)
  'mw011': "<b>Réponse</b> : après avoir dépensé cette carte, regardez les 5 cartes du dessus de votre deck. Ajoutez-en 1 à votre main et remettez les autres dans le même ordre.",
  // madame_web — Neurological Deterioration (Obligation)
  'mw012': "Vous ne pouvez pas redresser votre identité.\n<b>Action d'alter ego</b> : dépensez des ressources [energy] [mental] [physical] → retirez Neurological Deterioration de la partie.",
  // madame_web — Spider-Woman (Minion)
  'mw013': "<b>Une fois révélée</b> : choisissez soit de subir 2 dégâts indirects, soit d'incliner votre identité.\n<i>(Sbire nemesis de Madame Web.)</i>",
  // madame_web — Spider-Women Hunt (SideScheme)
  'mw014': "En prenant le nom de \"Spider-Woman\", Witter a orchestré des attaques contre les autres femmes ayant porté ce nom avant elle, et absorbé leurs pouvoirs.\n<b>Une fois révélée</b> : placez 2 menaces supplémentaires ici par personnage en jeu dont le titre contient \"Spider\".",
  // madame_web — Power Absorption (Treachery)
  'mw015': "<b>Une fois révélée</b> : défaussez un allié que vous contrôlez. Si aucun allié n'a été défaussé de cette façon, passez sous forme d'alter ego et inclinez votre identité.",
  // madame_web — Hypnosis (Treachery)
  'mw016': "Renfort.\n<b>Une fois révélée</b> : sonnez et désorientez un personnage que vous contrôlez.",
  // madame_web — Ana Kraven (Minion)
  'mw017': "[star] <b>Réponse forcée</b> : après qu'Ana Kraven vous a attaqué, placez 1 menace sur la manigance annexe The Grim Hunt. Si The Grim Hunt n'est pas en jeu, placez 1 menace sur la manigance principale.\n<i>(Sbire nemesis de Madame Web.)</i>",
  // madame_web — The Grim Hunt (SideScheme)
  'mw018': "Quand Sasha Kraven envoya sa fille Ana enlever la médium connue sous le nom de Madame Web, ce fut le début d'une chasse à tous ceux qui portent la marque de l'araignée.\n<b>Une fois révélée</b> : mettez Kraven the Hunter de côté, hors jeu.\nThe Grim Hunt gagne 1 menace par joueur à la fin de chaque phase du méchant. Si cette manigance est accomplie (5 menaces par joueur), mettez en jeu Kraven the Hunter mis de côté, engagé avec le premier joueur.",
  // madame_web — Kraven the Hunter (Minion)
  'mw019': "Riposte 1. Vilenie.\n<b>Une fois vaincu</b> : mettez Kraven the Hunter de côté, hors jeu.",
  // madame_web — One Spyder Down (Treachery)
  'mw020': "<b>Une fois révélée</b> : défaussez un allié que vous contrôlez. Si vous ne pouvez pas, cette carte gagne renfort.",
  // madame_web — Hunting Spyders (Treachery)
  'mw021': "<b>Une fois révélée</b> : infligez 3 dégâts à un allié que vous contrôlez. Si vous ne pouvez pas, infligez 3 dégâts à votre identité.",
  // madame_web — Scarlet Spider (Ally)
  'mw022': "<b>Réponse de héros</b> : après que Scarlet Spider est entré en jeu, redressez votre héros.",
  // madame_web — Spider-Woman (Ally)
  'mw023': "Spider-Woman gagne +1 ATQ si vous avez payé cette carte en n'utilisant que des ressources [physical].",
  // madame_web — Spider-Woman (Ally)
  'mw024': "<b>Interruption de héros</b> : quand le méchant initie une attaque contre vous, piochez 1 carte.",
  // madame_web — Spider-Woman (Ally)
  'mw025': "<b>Interruption forcée</b> : quand Spider-Woman arrive dans votre main, payez son coût imprimé → mettez Spider-Woman en jeu sous votre contrôle. Si vous ne pouvez pas, défaussez Spider-Woman.",
  // madame_web — Spider-Woman (Ally)
  'mw026': "<b>Interruption forcée</b> : quand Spider-Woman devrait être mise K.O., soignez plutôt tous ses dégâts et engagez-la comme un sbire. Considérez Spider-Woman comme un sbire à la zone de texte vierge <i>(à l'exception de ses <b>traits</b>)</i>. Son MNG est égal à son CTR imprimé et elle ne subit pas de dégâts consécutifs.",
  // madame_web — Order of the Web (Support)
  'mw027': "Jouez-la sous le contrôle de n'importe quel joueur. Maximum 1 carte <b>TEAM</b> par joueur.\n<b>Action</b> : inclinez Order of the Web → choisissez dans votre pile de défausse un allié dont le titre contient \"Spider\" et mélangez-le dans votre deck.",
  // madame_web — Advice (Event)
  'mw028': "<b>Action</b> : choisissez un allié et défaussez la carte du dessus du deck rencontre. Cet allié gagne +X ATQ durant cette phase, où X est le nombre d'icônes de boost ([boost]) défaussées de cette façon.",
  // madame_web — Female Power (Event)
  'mw029': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi par personnage que vous contrôlez dont le titre contient \"Girl\", \"Lady\", \"Madame\", \"Ms.\", \"She\" ou \"Woman\".",
  // cloak_dagger — Cloak (Hero)
  'cd001a': "Riposte 1.\n[star] <i>Duo protecteur</i> — Cloak gagne +2 DEF tant que Dagger est en jeu.",
  // cloak_dagger — Tyrone Johnson (AlterEgo)
  'cd001b': "Pendant la construction du deck, voir l'encart.\n<i>Éclaircissement</i> — Tandy Bowen et Tyrone Johnson gagnent robuste tant que Tandy Bowen est en jeu.",
  // cloak_dagger — Dagger (Hero)
  'cd002a': "[star] <i>Duo destructeur</i> — Dagger gagne +2 ATQ tant que Cloak est en jeu.\n[star] <i>Barrage lumineux</i> — Les dégâts que Dagger inflige avec son pouvoir d'attaque de base <i>(ATQ)</i> peuvent être répartis entre les ennemis comme vous le souhaitez.",
  // cloak_dagger — Tandy Bowen (AlterEgo)
  'cd002b': "Pendant la construction du deck, voir l'encart.\n[star] <i>Harmonie</i> — Tandy Bowen et Tyrone Johnson gagnent +2 REC tant que Tyrone Johnson est en jeu.",
  // cloak_dagger — Forces Combined (Upgrade)
  'cd003': "Immuable. Permanent. Mise en place.\n<b>Interruption</b> : quand vous devriez dépenser des ressources pour une carte ou une capacité, inclinez Forces Combined → vous pouvez dépenser des ressources de vos deux mains pour cette carte ou cette capacité.",
  // cloak_dagger — Lightforce Cleansing (Event)
  'cd004': "<b>Action de héros</b> : soignez 3 dégâts d'un personnage allié. Si 2 dégâts ou plus ont été soignés de Cloak de cette façon, piochez 1 carte dans le deck de chacune de vos identités.",
  // cloak_dagger — Lightforce Daggers (Event)
  'cd005': "<b>Action de héros</b> <i>(attaque)</i> : infligez un total de 3 dégâts répartis entre les ennemis comme vous le souhaitez et sonnez le méchant. Puis, si Cloak est en jeu, désorientez un ennemi.",
  // cloak_dagger — Pure Lightforce (Resource)
  'cd006': "<b>Réponse de héros</b> : après avoir dépensé cette carte pour une carte [[LIGHTFORCE]], infligez 1 dégât au méchant par ressource payée en trop pour le coût de cette carte [[LIGHTFORCE]].",
  // cloak_dagger — Lightforce Absorption (Upgrade)
  'cd007': "<b>Réponse</b> : après avoir joué une carte [[LIGHTFORCE]], inclinez Lightforce Absorption → mélangez une carte [[LIGHTFORCE]] de la pile de défausse de Dagger dans le deck de Dagger.",
  // cloak_dagger — Living Light (Upgrade)
  'cd008': "Cette carte ne peut pas être inclinée tant que le joueur Cloak & Dagger n'a pas infligé 5 dégâts ou plus au méchant durant cette phase.\n<b>Action de héros</b> : inclinez Living Light → redressez Dagger.",
  // cloak_dagger — Dark Teleportation (Event)
  'cd009': "<b>Action de héros</b> : redressez un personnage allié. Puis, si Dagger a été redressée de cette façon, retirez 2 menaces d'une manigance.",
  // cloak_dagger — Darkforce Channel (Event)
  'cd010': "<b>Action de héros</b> <i>(attaque)</i> : choisissez jusqu'à 3 ennemis différents. Infligez 1 dégât à chacun d'eux et soignez 1 dégât de Cloak par ennemi blessé de cette façon. Désorientez le méchant. Puis, si Dagger est en jeu, sonnez un ennemi.",
  // cloak_dagger — Raw Darkforce (Resource)
  'cd011': "<b>Réponse de héros</b> : après avoir dépensé cette carte pour une carte [[DARKFORCE]], retirez 1 menace de la manigance principale par ressource payée en trop pour le coût de cette carte [[DARKFORCE]].",
  // cloak_dagger — Dark Intangibility (Upgrade)
  'cd012': "<b>Réponse</b> : après que Cloak a fait une défense de base, inclinez Dark Intangibility → redressez Cloak, et il gagne riposte 1 jusqu'à la fin de la phase.",
  // cloak_dagger — Darkforce Absorption (Upgrade)
  'cd013': "<b>Réponse</b> : après avoir joué une carte [[DARKFORCE]], inclinez Darkforce Absorption → mélangez une carte [[DARKFORCE]] de la pile de défausse de Cloak dans le deck de Cloak.",
  // cloak_dagger — Lovers Quarrel (Obligation)
  'cd014': "<b><i>Donnez-la au joueur Cloak & Dagger.</i></b>\nPassez les deux identités sous forme d'alter ego, puis choisissez l'un ou l'autre :\n• Inclinez Tandy Bowen et Tyrone Johnson → retirez Lovers Quarrel de la partie.\n• Tyrone Johnson ne peut ni changer de forme, ni jouer de cartes, ni utiliser de pouvoirs de base au round suivant → défaussez cette obligation.",
  // cloak_dagger — Mister Negative (Minion)
  'cd015': "<b>Réponse forcée</b> : après que Mister Negative a attaqué votre héros, passez-le sous forme d'alter ego.",
  // cloak_dagger — Bigger Fish (SideScheme)
  'cd016': "<b>Interruption forcée</b> : quand le méchant ou Mister Negative devraient attaquer, ils manigancent à la place.",
  // cloak_dagger — Inner Demon (Minion)
  'cd017': "Garde. Ténacité.",
  // cloak_dagger — Opposites Attack (Treachery)
  'cd018': "<b>Une fois révélée</b> : passez chaque héros sous forme d'alter ego. Puis, placez 1 menace sur la manigance principale par héros retourné de cette façon.",
  // spider_man_rainy — Spider-Man (Hero)
  'sr001a': "Comme des mouches — <b>Interruption</b> : quand un sbire s'engage avec vous, entoilez-le. (Limite de deux fois par round.)\n<b>Réponse</b> : après qu'un ennemi entoilé a été mis K.O., retirez 1 menace d'une manigance.",
  // spider_man_rainy — Peter Parker (AlterEgo)
  'sr001b': "La sagesse d'oncle Ben — <b>Action</b> : défaussez 1 carte de votre main → cherchez une ressource Great Power ou Great Responsibility dans votre deck et votre pile de défausse, et ajoutez-la à votre main. Mélangez votre deck. (Limite de deux fois par round.)",
  // spider_man_rainy — Spider-Man (Ally)
  'sr002': "[star] <b>Interruption</b> : quand cet allié utilise un pouvoir de base, entoilez un ennemi (maximum 3 compteurs de toile par ennemi).",
  // spider_man_rainy — Thwip! (Event)
  'sr003': "<b>Action de héros</b> : redressez votre héros et entoilez un ennemi (maximum 3 compteurs de toile par ennemi).",
  // spider_man_rainy — Web Barrage (Event)
  'sr004': "<b>Action de héros</b> : faites l'attaque suivante contre X ennemis.\n<i>(attaque)</i> : entoilez un ennemi et infligez-lui 2 dégâts. Cette attaque gagne à distance.",
  // spider_man_rainy — Web Strike (Event)
  'sr005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 6 dégâts à un ennemi. Si cet ennemi est entoilé, infligez 2 dégâts supplémentaires. Cette attaque gagne déferlement.",
  // spider_man_rainy — Webbed Up (Event)
  'sr006': "<b>Action de héros</b> : choisissez un ennemi et entoilez-le jusqu'à 3 fois.\n<b>Interruption de héros</b> <i>(défense)</i> : quand une identité devrait subir des dégâts d'une attaque, prévenez tous ces dégâts.",
  // spider_man_rainy — Great Power (Resource)
  'sr007': "<b>Réponse de héros</b> <i>(attaque)</i> : après avoir dépensé cette carte, infligez 2 dégâts à un ennemi.",
  // spider_man_rainy — Great Responsibility (Resource)
  'sr008': "<b>Réponse de héros</b> <i>(contre)</i> : après avoir dépensé cette carte, retirez 2 menaces d'une manigance.",
  // spider_man_rainy — J. Jonah Jameson (Support)
  'sr009': "<b>Action d'alter ego</b> : inclinez J. Jonah Jameson → piochez 1 carte. Si cette carte comportait une image de Spider-Man, piochez une autre carte.",
  // spider_man_rainy — Spider-Sense (Upgrade)
  'sr010': "<b>Interruption de héros</b> : quand le méchant ou un sbire ayant vilenie initie une attaque contre vous, piochez 1 carte.\n<b>Interruption de héros</b> : quand une carte de boost est retournée face visible pendant une attaque contre vous, défaussez 1 carte de votre main → annulez la capacité de boost de cette carte.",
  // spider_man_rainy — Web-Shooters (Upgrade)
  'sr011': "Votre héros gagne le trait [[AERIAL]].\n<b>Ressource de héros</b> : inclinez Web-Shooters → générez une ressource [wild] pour une carte WEB.\n<b>Action de héros</b> : inclinez Web-Shooters → entoilez un ennemi.",
  // spider_man_rainy — Impact Webbing (Upgrade)
  'sr012': "Permanent. Mise en place.\n<b>Interruption forcée</b> : quand un ennemi entoilé s'active, retirez tous les compteurs de toile de cet ennemi → cet ennemi subit -1 MNG et -1 ATQ par compteur de toile retiré de cette façon, pour cette activation.",
  // spider_man_rainy — Bad Publicity (Obligation)
  'sr013': "Donnez-la au joueur Peter Parker.\nUtilisations (3 compteurs de menace).\n<b>Réponse de héros</b> : après avoir mis un ennemi K.O. ou déjoué une manigance, retirez 1 compteur de menace d'ici.",
  // spider_man_rainy — For My Next Trick... (SideScheme)
  'sr014': "<i>Mysterio a l'air de préparer un mauvais coup !</i>\nUtilisations (2 compteurs d'illusion).\n<b>Réponse forcée</b> : après le début de la phase du méchant, retirez 1 compteur d'illusion d'ici.\n<b>Interruption forcée</b> : quand cette carte devrait quitter le jeu sans avoir été déjouée, attribuez à chaque joueur une carte rencontre face cachée.",
  // spider_man_rainy — Mysterio (Minion)
  'sr015': "Entre en jeu avec 2 compteurs d'illusion.\n<b>Interruption forcée</b> : quand Mysterio devrait subir des dégâts, retirez plutôt un compteur d'illusion d'ici.\n[star] <b>Réponse forcée</b> : après que Mysterio s'est activé contre vous et a infligé des dégâts ou placé de la menace, attribuez-vous une carte rencontre face cachée.",
  // spider_man_rainy — Jump Scare (Treachery)
  'sr016': "<b>Une fois révélée</b> : attribuez-vous une carte rencontre face cachée. Subissez 1 dégât par carte rencontre face cachée devant vous.\n[star] <b>Boost</b> : attribuez-vous une carte rencontre face cachée.",
  // spider_man_rainy — Smoke and Mirrors (Treachery)
  'sr017': "Renfort.\n<b>Une fois révélée</b> : donnez à Mysterio une carte d'état Tenace et une carte de boost face cachée. Si vous ne pouvez pas, donnez-les au méchant.\n[star] <b>Boost</b> : vous êtes désorienté.",
  // venom_rainy — Venom (Hero)
  'vr001a': "Faim — <b>Réponse</b> : après avoir mis un ennemi K.O., soignez 1 dégât de Venom.\nLien symbiotique — <b>Ressource</b> : subissez 1 dégât → générez une ressource [wild]. (Limite d'une fois par phase.)",
  // venom_rainy — Eddie Brock (AlterEgo)
  'vr001b': "Journaliste d'investigation — <b>Réponse</b> : après que de la menace a été placée sur la manigance principale, retirez 2 menaces d'une manigance. (Limite d'une fois par round.)",
  // venom_rainy — Bulletproof (Event)
  'vr002': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts d'une attaque, quel qu'en soit le nombre, prévenez 2 de ces dégâts et piochez 1 carte. Puis, vous pouvez mélanger cette carte dans votre deck.",
  // venom_rainy — Just A Snack (Event)
  'vr003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 1 dégât à un ennemi (2 dégâts à la place si vous avez payé cette carte avec une ressource [physical]). Soignez 2 dégâts de Venom.",
  // venom_rainy — Self-Sacrifice (Event)
  'vr004': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Vous pouvez subir 2 dégâts pour retirer 3 menaces supplémentaires de cette manigance.",
  // venom_rainy — Symbiotic Fury (Event)
  'vr005': "<b>Réponse de héros</b> : après avoir subi des dégâts, subissez 1 dégât supplémentaire → redressez votre héros. Puis, si vous avez subi 6 dégâts ou plus au total, infligez 2 dégâts à un ennemi.",
  // venom_rainy — Tendril Explosion (Event)
  'vr006': "<b>Action de héros</b> : infligez X dégâts à chaque ennemi.",
  // venom_rainy — Venomous Bite (Event)
  'vr007': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Puis, sonnez cet ennemi. Si aucun ennemi n'a été sonné de cette façon, soignez 2 dégâts de Venom.",
  // venom_rainy — Camouflage (Upgrade)
  'vr008': "<b>Interruption de héros</b> <i>(attaque)</i> : quand un ennemi devrait initier une attaque, défaussez Camouflage → infligez 4 dégâts à cet ennemi et désorientez-le. Si aucun ennemi n'a été désorienté de cette façon, retirez 2 menaces d'une manigance.",
  // venom_rainy — Lethal Protector (Upgrade)
  'vr009': "Venom gagne +1 DEF.\n<b>Interruption de héros</b> <i>(attaque/défense)</i> : quand un ennemi initie une attaque, inclinez Lethal Protector → infligez 2 dégâts à cet ennemi. Si un ennemi a été mis K.O. de cette façon, redressez Lethal Protector.",
  // venom_rainy — Regeneration (Upgrade)
  'vr010': "Vous gagnez +2 points de vie.\n<b>Réponse d'alter ego</b> : après avoir utilisé votre REC, inclinez Regeneration → redressez Eddie Brock.",
  // venom_rainy — Sharp Teeth (Upgrade)
  'vr011': "Venom gagne +1 ATQ.\nLes attaques de base de Venom gagnent déferlement et perçant.",
  // venom_rainy — We Hunger (Obligation)
  'vr012': "Donnez-la au joueur Eddie Brock.\nPassez sous forme de héros. Choisissez :\n- Subissez 3 dégâts → défaussez cette obligation.\n- Placez 3 menaces sur la manigance principale → soignez 1 dégât de Venom et défaussez cette obligation.",
  // venom_rainy — Paint The Town Red (SideScheme)
  'vr013': "<i>Carnage a lâché sur la ville une horde déchaînée de symbiotes violents ! Arrêtez-les avant que la ville ne sombre dans le chaos absolu !</i>\nEntrave 2[per_hero].",
  // venom_rainy — Carnage (Minion)
  'vr014': "Coup Rapide. Riposte 1.\n<b>Réponse forcée</b> : après avoir soigné des dégâts, subissez 1 dégât.\n<i>(Sbire nemesis de Venom.)</i>",
  // venom_rainy — Symbiote Rioter (Minion)
  'vr015': "Garde. Patrouille.\n<b>Réponse forcée</b> : après avoir attaqué un autre ennemi, subissez 1 dégât.",
  // jessica_jones — Jessica Jones (Hero)
  'jj001a': "Enquête musclée — <b>Réponse</b> <i>(attaque)</i> : après avoir déjoué une manigance annexe, infligez à un ennemi un nombre de dégâts égal à votre ATQ.",
  // jessica_jones — Jessica Jones (AlterEgo)
  'jj001b': "<b>Mise en place</b> : mélangez le set On the Job dans le deck rencontre.\nÇa paie les factures — <b>Réponse</b> : après qu'une manigance annexe a été révélée, piochez 2 cartes. <i>(Limite d'une fois par phase.)</i>",
  // jessica_jones — Luke Cage (Ally)
  'jj002': "Ténacité. <i>(Ce personnage entre en jeu avec une carte d'état Tenace.)</i>\nTant qu'il y a une manigance annexe en jeu, réduisez de 1 les dégâts subis par Luke Cage.",
  // jessica_jones — Breakthrough (Event)
  'jj003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Infligez-lui 1 dégât supplémentaire par manigance annexe en jeu.",
  // jessica_jones — Crack the Case (Event)
  'jj004': "Jouez-la uniquement s'il y a une manigance annexe en jeu.\n<b>Action</b> <i>(contre)</i> : retirez 2 menaces d'une manigance. Si une manigance annexe est déjouée de cette façon, redressez Jessica Jones.",
  // jessica_jones — Hit the Streets (Event)
  'jj005': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Retirez-en 1 supplémentaire par manigance annexe en jeu.",
  // jessica_jones — Out in the Open (Event)
  'jj006': "<b>Interruption</b> : quand une carte de traîtrise est révélée depuis le deck rencontre, annulez ses effets \"<b>Une fois révélée</b>\". Défaussez les cartes du dessus du deck rencontre jusqu'à défausser une manigance annexe. Révélez cette manigance annexe.",
  // jessica_jones — The Truth Hurts (Event)
  'jj007': "Jouez-la uniquement s'il y a une manigance annexe en jeu.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Si vous avez déjoué une manigance annexe ce round, désorientez cet ennemi.",
  // jessica_jones — Alias Investigations (Support)
  'jj008': "<b>Action</b> : inclinez Alias Investigations → défaussez les cartes du dessus du deck rencontre jusqu'à défausser une manigance annexe. Révélez cette manigance annexe.",
  // jessica_jones — Jessica's Camera (Upgrade)
  'jj009': "<b>Réponse</b> : après avoir déjoué une manigance annexe, inclinez Jessica's Camera → placez 1 compteur de preuve ici. Tant que Jessica's Camera a au moins :\n(1) Jessica Jones gagne +1 DEF.\n(2) Jessica Jones gagne +1 CTR.\n(3) Jessica Jones gagne +1 ATQ.",
  // jessica_jones — Jessica's Jacket (Upgrade)
  'jj010': "Vous gagnez +2 points de vie.\n<b>Interruption</b> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, inclinez Jessica's Jacket → prévenez 1 de ces dégâts et retirez 1 menace d'une manigance.",
  // jessica_jones — Private Investigator (Upgrade)
  'jj011': "<b>Action d'alter ego</b> : inclinez Private Investigator → déplacez 1 menace d'une manigance vers cette carte.\n<b>Action de héros</b> : retirez toute la menace d'ici → infligez 1 dégât à un sbire par menace retirée de cette façon.",
  // jessica_jones — Always a Bigger Conspiracy (SideScheme)
  'jj012': "<i>« Il y a toujours deux histoires derrière une histoire. » — Jessica Jones</i>\nQuand Jessica Jones contre une manigance annexe, elle peut utiliser son ATQ au lieu de son CTR.\n<b>Une fois déjouée</b> : défaussez les cartes du dessus du deck rencontre jusqu'à défausser une manigance annexe. Révélez cette manigance annexe.",
  // jessica_jones — Chase Down a Lead (SideScheme)
  'jj013': "Investigation 2. <i>(Une fois révélée, déplacez 2 menaces de la manigance principale vers cette carte.)</i>\n<b>Une fois déjouée</b> : le joueur Jessica Jones cherche une carte spécifique à son héros parmi les 5 cartes du dessus de son deck et l'ajoute à sa main. <i>(Mélangez.)</i>",
  // jessica_jones — Hang Back and Watch (SideScheme)
  'jj014': "Investigation 2[per_hero]. <i>(Une fois révélée, déplacez 2[per_hero] menaces de la manigance principale vers cette carte.)</i>\n<b>Une fois déjouée</b> : soignez 2 dégâts de Jessica Jones.",
  // jessica_jones — Pore Over the Evidence (SideScheme)
  'jj015': "Investigation 1[per_hero]. <i>(Une fois révélée, déplacez 1[per_hero] menace de la manigance principale vers cette carte.)</i>\n<b>Une fois déjouée</b> : réduisez de 2 le coût de la prochaine carte que le joueur Jessica Jones joue durant cette phase.",
  // jessica_jones — Sneak Into the Crime Scene (SideScheme)
  'jj016': "Investigation 2. <i>(Une fois révélée, déplacez 2 menaces de la manigance principale vers cette carte.)</i>\n<b>Une fois déjouée</b> : donnez une carte d'état Tenace à Jessica Jones.",
  // jessica_jones — Stable Home Life (Obligation)
  'jj017': "<i>Donnez-la au joueur Jessica Jones.</i>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n- Inclinez votre alter ego → retirez Stable Home Life de la partie.\n- Défaussez du jeu une manigance annexe On the Job. Si vous ne pouvez pas, cette carte gagne renfort. Défaussez cette obligation.",
  // jessica_jones — "Look At Me!" (SideScheme)
  'jj018': "Purple Man ne peut pas subir de dégâts.\n<b>Réponse forcée</b> : après qu'une manigance annexe a été déjouée, placez X menaces sur la manigance principale, où X est égal au nombre de manigances annexes en jeu.\n<hr /> [star] <b>Boost</b> : après la fin de cette activation, révélez cette carte.",
  // jessica_jones — Purple Man (Minion)
  'jj019': "[star] <b>Interruption forcée</b> : quand Purple Man devrait attaquer, placez plutôt 2 menaces sur chaque manigance annexe. S'il n'y a aucune manigance annexe en jeu, révélez la carte du dessus du deck rencontre.\n<i>(Son ATQ imprimée est une [star] : sa valeur est définie par sa capacité, le 0 affiché ne sert jamais.)</i>\n<hr /> [star] <b>Boost</b> : vous êtes désorienté.\n<i>(Sbire nemesis de Jessica Jones.)</i>",
  // jessica_jones — "I've Got Everyone" (Treachery)
  'jj020': "<b>Une fois révélée</b> : répartissez X dégâts indirects entre les joueurs <i>(comme vous le souhaitez)</i>, où X est égal au nombre de manigances annexes en jeu. Désorientez chaque personnage blessé de cette façon. S'il n'y a aucune manigance annexe en jeu, cette carte gagne renfort.",
  // jessica_jones — The Purple Children (Treachery)
  'jj021': "Incitation 1 <i>(incitation 2 à la place si Purple Man est en jeu)</i>.\n<b>Une fois révélée</b> : placez 2 menaces sur chaque manigance annexe en jeu. S'il n'y a aucune manigance annexe en jeu, vous êtes désorienté.",
  // jessica_jones — Power Couple (Event)
  'jj022': "En Équipe (Jessica Jones et Luke Cage). 1 max par deck.\n<b>Action de héros</b> : donnez une carte d'état Tenace à Jessica Jones et à Luke Cage. Puis, piochez autant de cartes qu'il y a de cartes d'état Tenace parmi les personnages alliés.",
  // agent_anti_venom — Agent Anti-Venom (Hero)
  'av001a': "[star] <i>Dix sur dix !</i> — Tant qu'il reste exactement 10 points de vie à Agent Anti-Venom, il gagne +1 CTR, +1 ATQ, +1 DEF, et ses attaques gagnent perçant.",
  // agent_anti_venom — Flash Thompson (AlterEgo)
  'av001b': "<i>Petit scout</i> — <b>Réponse</b> : après être passé à cette forme, soignez 2 dégâts de n'importe quel personnage.",
  // agent_anti_venom — Spider-Man (Ally)
  'av002': "<b>Interruption</b> : quand un sbire non-[[ELITE]] devrait attaquer ou manigancer, dépensez une ressource [mental] → annulez cette activation.",
  // agent_anti_venom — Dig Deep (Event)
  'av003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. S'il reste exactement 10 points de vie à Agent Anti-Venom, retirez 1 menace d'une manigance et sonnez cet ennemi.",
  // agent_anti_venom — Extricate (Event)
  'av004': "<b>Action de héros</b> <i>(contre)</i> : retirez 4 menaces d'une manigance. S'il reste exactement 10 points de vie à Agent Anti-Venom, piochez 1 carte ou désorientez un ennemi.",
  // agent_anti_venom — "I've Got This!" (Event)
  'av005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts au méchant <i>(7 dégâts à la place si cette attaque a à distance ou perçant)</i>.",
  // agent_anti_venom — Anti-Venom Goo (Resource)
  'av006': "<b>Interruption de héros</b> : quand vous dépensez cette carte pour jouer un événement, réduisez de 1 le coût de cet événement. Puis, soignez 1 dégât d'un personnage allié par ressource payée en trop pour le coût de cet événement avec cette carte.",
  // agent_anti_venom — Unlikely Allies (Support)
  'av007': "<b>Action de héros</b> : inclinez cette carte et défaussez une carte de votre main. Si la zone de ressource imprimée de cette carte comporte :\n[physical] - Drainez 2 d'un ennemi.\n[mental] - Retirez 2 menaces d'une manigance.\n[energy] - Piochez 2 cartes.\n[wild] - Choisissez 2 des options ci-dessus.",
  // agent_anti_venom — Anti-Maniac Booster (Upgrade)
  'av008': "Agent Anti-Venom gagne riposte 1.\n<b>Réponse</b> : après qu'Agent Anti-Venom a subi des dégâts d'une attaque, inclinez Anti-Maniac Booster → soignez 1 dégât d'Agent Anti-Venom.",
  // agent_anti_venom — Bear Arms (Upgrade)
  'av009': "<b>Action de héros</b> : inclinez Bear Arms → la prochaine attaque d'Agent Anti-Venom gagne à distance.\n<b>Action de héros</b> <i>(attaque)</i> : inclinez Bear Arms → drainez 1 du méchant.",
  // agent_anti_venom — Heroic Will (Upgrade)
  'av010': "<b>Action d'alter ego</b> : inclinez Heroic Will → changez de forme.\n<b>Action de héros</b> : inclinez Heroic Will → redressez Agent Anti-Venom.",
  // agent_anti_venom — One Man Army (Upgrade)
  'av011': "<b>Interruption</b> : quand Agent Anti-Venom utilise un pouvoir de base, s'il n'y a aucun allié sous votre contrôle, piochez 1 carte et soignez 1 dégât d'Agent Anti-Venom. <i>(Limite d'une fois par round.)</i>",
  // agent_anti_venom — Spread Too Thin (Obligation)
  'av012': "<i>Donnez-la au joueur Flash Thompson.</i>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n- Infligez 3 dégâts à votre identité → retirez Spread Too Thin de la partie.\n- Retirez de la partie une amélioration que vous contrôlez. Défaussez cette obligation.",
  // agent_anti_venom — Maniac (Minion)
  'av013': "<b>Réponse forcée</b> : après que Maniac a attaqué un allié que vous contrôlez, infligez X dégâts à votre héros, où X est l'ATQ imprimée de cet allié.\n<i>(Sbire nemesis d'Agent Anti-Venom.)</i>",
  // agent_anti_venom — The Made Men (SideScheme)
  'av014': "<b>Interruption forcée</b> : après que Maniac a manigancé ou attaqué, l'allié ayant l'ATQ imprimée la plus élevée sous le contrôle de chaque joueur gagne traître <i>(considérez cet allié comme un sbire engagé avec son propriétaire. Il a 1 MNG, une zone de texte imprimée vierge, et ne subit pas de dégâts consécutifs.)</i>",
  // agent_anti_venom — Infected Scorpion (Minion)
  'av015': "Coup Rapide.\n<b>Interruption forcée</b> : quand Infected Scorpion attaque un allié, prévenez tous les dégâts infligés à cet allié. Cet allié gagne traître <i>(considérez cet allié comme un sbire engagé avec son propriétaire. Il a 1 MNG, une zone de texte imprimée vierge, et ne subit pas de dégâts consécutifs.)</i>",
  // agent_anti_venom — Infected (Attachment)
  'av016': "Attachez-la au sbire ayant le plus de points de vie imprimés. S'il n'y a aucun sbire en jeu, cette carte gagne renfort.\nLes attaques du sbire attaché gagnent déferlement.",
  // squirrel_girl — Squirrel Girl (Hero)
  'sg001a': "<i>Armée imbattable</i> — <b>Réponse de héros</b> : après avoir dépensé un Écureuil, infligez 1 dégât à un ennemi ou retirez 1 menace d'une manigance. (Limite d'une fois par phase.)\n<i>Aide d'Écureuil</i> — <b>Ressource</b> : défaussez un allié [[SQUIRREL]] que vous contrôlez → générez 1 ressource [wild]. Ne la dépensez que pour payer une carte Squirrel Girl. (Limite d'1 Écureuil par carte jouée.)",
  // squirrel_girl — Doreen Green (AlterEgo)
  'sg001b': "Doreen Green commence la partie avec un deck d'Écureuils. <i>(Mettez les 6 alliés [[SQUIRREL]] de côté, mélangés. Quand un effet appelle un Écureuil, révélez la carte du dessus du deck d'Écureuils et mettez-la en jeu inclinée, sous votre contrôle. Si le deck d'Écureuils est vide, mélangez la pile de défausse des Écureuils pour en former un nouveau.)</i>\n<i>Langage des écureuils</i> — <b>Action d'alter ego</b> : inclinez Doreen Green → appelez 1 Écureuil. (Limite d'une fois par round.)\n<i>Aide d'Écureuil</i> — <b>Ressource</b> : défaussez un allié [[SQUIRREL]] que vous contrôlez → générez 1 ressource [wild]. Ne la dépensez que pour payer une carte Squirrel Girl. (Limite d'1 Écureuil par carte jouée.)",
  // squirrel_girl — Tippy-Toe (Ally)
  'sg002': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>\n<b>Réponse</b> : après que Tippy-Toe est entrée en jeu, regardez les 2 cartes du dessus du deck d'Écureuils. Remettez-les dans l'ordre de votre choix.",
  // squirrel_girl — Monkey Joe (Ally)
  'sg003': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>\n<b>Réponse</b> : après que Monkey Joe a mis un sbire K.O., appelez 1 Écureuil.",
  // squirrel_girl — The Lookout (Ally)
  'sg004': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>",
  // squirrel_girl — The Bruiser (Ally)
  'sg005': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>\n<b>Interruption</b> : quand un autre allié [[SQUIRREL]] que vous contrôlez devrait subir des dégâts consécutifs, inclinez The Bruiser → infligez plutôt 1 de ces dégâts à The Bruiser.",
  // squirrel_girl — The Forager (Ally)
  'sg006': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>\n<b>Réponse</b> : après avoir dépensé The Forager, regardez les 2 cartes du dessus de votre deck. Défaussez-en 1, ou remettez-les dans l'ordre de votre choix.",
  // squirrel_girl — The Gatherer (Ally)
  'sg007': "<i>Écureuil. (Ne compte pas dans votre limite d'alliés. Ne peut pas se défendre. Ne peut pas recevoir d'améliorations. Ne peut être ni choisi ni renforcé par des cartes joueur autres que Squirrel Girl. Quand il quitte le jeu, mettez-le dans la pile de défausse des Écureuils. Peut être dépensé pour l'Aide d'Écureuil.)</i>\n<b>Réponse</b> : après avoir dépensé The Gatherer, soignez 1 dégât de Squirrel Girl.",
  // squirrel_girl — Nancy Whitehead (Ally)
  'sg008': "<b>Réponse</b> : après que Nancy Whitehead est entrée en jeu, appelez 1 Écureuil.",
  // squirrel_girl — Squirrel Girl's Costume (Upgrade)
  'sg009': "Squirrel Girl gagne +1 ATQ.\n<b>Réponse de héros</b> : après qu'un sbire a été mis K.O., appelez 1 Écureuil. (Limite d'une fois par round.)",
  // squirrel_girl — Prehensile Tail (Upgrade)
  'sg010': "<b>Ressource</b> : inclinez Prehensile Tail → générez 1 ressource [wild]. Ne la dépensez que pour payer une carte Squirrel Girl.",
  // squirrel_girl — Central Park (Support)
  'sg011': "<b>Action</b> : inclinez Central Park → si vous contrôlez moins de 3 alliés [[SQUIRREL]], appelez 1 Écureuil.",
  // squirrel_girl — Network of Trees (Support)
  'sg012': "<b>Interruption</b> : quand vous devriez appeler un Écureuil, inclinez Network of Trees → regardez les 2 cartes du dessus du deck d'Écureuils. Appelez-en 1 et placez l'autre sous le deck d'Écureuils.",
  // squirrel_girl — Call the Squirrels (Event)
  'sg013': "<b>Action</b> : appelez 2 Écureuils. Les Écureuils appelés de cette façon entrent en jeu redressés.",
  // squirrel_girl — Squirrel Swarm (Event)
  'sg014': "<b>Action de héros <i>(attaque)</i></b> : infligez 3 dégâts à un ennemi. Si vous avez dépensé un Écureuil pour jouer cette carte, infligez-lui 3 dégâts supplémentaires.",
  // squirrel_girl — Recon Team (Event)
  'sg015': "<b>Action de héros <i>(contre)</i></b> : retirez 3 menaces d'une manigance. Si vous avez dépensé un Écureuil pour jouer cette carte, retirez 1 menace d'une autre manigance.",
  // squirrel_girl — Unbeatable! (Event)
  'sg016': "<b>Interruption de héros <i>(défense)</i></b> : quand Squirrel Girl se défend contre une attaque, elle gagne +2 DEF pour cette attaque. Si vous avez dépensé un Écureuil pour jouer cette carte, elle gagne +3 DEF à la place. Si cette attaque n'inflige aucun dégât à Squirrel Girl, redressez-la.",
  // squirrel_girl — Nuts! (Resource)
  'sg017': "<b>Réponse</b> : après avoir dépensé cette carte pour payer une carte Squirrel Girl, appelez 1 Écureuil.",
  // squirrel_girl — Surprise Exam (Obligation)
  'sg018': "<b><i>Donnez-la au joueur Doreen Green.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Doreen Green et défaussez de votre main une carte ayant une ressource [mental] imprimée → retirez Surprise Exam de la partie.\n• Défaussez 1 allié [[SQUIRREL]] que vous contrôlez. Si vous ne pouvez pas, défaussez 1 carte au hasard de votre main. Défaussez cette obligation.",
  // squirrel_girl — Ratatoskr (Minion)
  'sg019': "<b>Interruption forcée</b> : quand Ratatoskr s'active contre vous, défaussez 1 allié [[SQUIRREL]] que vous contrôlez. Si vous ne pouvez pas, Ratatoskr reçoit 1 carte de boost supplémentaire pour cette activation.",
  // squirrel_girl — Discord in the Branches (SideScheme)
  'sg020': "<i>(Icône de crise : tant que cette manigance est en jeu, les joueurs ne peuvent pas réduire la valeur de manigance du méchant.)</i>\nTant que cette manigance est en jeu, les capacités imprimées des alliés [[SQUIRREL]] sont considérées comme vierges. Leur CTR, leur ATQ et leurs points de vie ne sont pas affectés.\n<b>Réponse forcée</b> : après qu'un allié [[SQUIRREL]] est entré en jeu, placez 1 menace ici. (Limite d'une fois par round.)",
  // squirrel_girl — Poisoned Rumors (Treachery)
  'sg021': "<b>Une fois révélée</b> : défaussez 2 alliés [[SQUIRREL]] que vous contrôlez. Si vous ne pouvez pas, placez 2 menaces sur Discord in the Branches. Si cette manigance n'est pas en jeu, placez plutôt ces menaces sur la manigance principale.\n[star] <b>Boost</b> : après la fin de cette activation, inclinez 1 allié [[SQUIRREL]] que vous contrôlez.",
  // squirrel_girl — Ratatoskr's Whispers (Attachment)
  'sg022': "Attachez-la à votre carte d'identité.\nVous ne pouvez pas dépenser d'alliés [[SQUIRREL]].\n<b>Action d'alter ego</b> : inclinez Doreen Green et défaussez de votre main une carte ayant une ressource [mental] imprimée → défaussez Ratatoskr's Whispers.\n[star] <b>Boost</b> : défaussez 1 allié [[SQUIRREL]] que vous contrôlez. Si vous ne pouvez pas, cette activation gagne +1 ATQ et +1 MNG.",
  // moon_knight — Moon Knight (Hero)
  'mk001a': "<i>La meilleure défense, c'est l'attaque</i> — Réduisez de 1 le coût des cartes Agressivité <i>(rouges)</i> que vous jouez.",
  // moon_knight — Marc Spector (AlterEgo)
  'mk001b': "Mise en place. Marc Spector commence la partie avec une pile d'IDENTITÉS. <i>(Voir l'encart.)</i>\n<i>Coups bas</i> — Utilisez tous les aspects au lieu d'un seul pendant la construction du deck. Vous ne pouvez pas inclure de cartes au coût imprimé de 3 ou plus, et devez inclure au moins 4 cartes de chaque aspect.",
  // moon_knight — Mr. Knight (Hero)
  'mk001c': "<i>La meilleure attaque, c'est la défense</i> — Réduisez de 1 le coût des cartes Protection <i>(vertes)</i> que vous jouez.",
  // moon_knight — Steven Grant (AlterEgo)
  'mk001d': "<i>PDG</i> — Réduisez de 1 le coût des cartes Leadership <i>(bleues)</i> que vous jouez.",
  // moon_knight — Jake Lockley (AlterEgo)
  'mk001e': "<i>Juste parce que</i> — Réduisez de 1 le coût des cartes Justice <i>(jaunes)</i> que vous jouez.",
  // moon_knight — Echo (Ally)
  'mk002': "[star] Echo a un CTR et une ATQ égaux au CTR et à l'ATQ de votre héros actif. Si vous êtes sous forme d'alter ego, Echo ne peut ni attaquer ni contrer.",
  // moon_knight — Khonshu (Support)
  'mk003': "<b>Action</b> : inclinez Khonshu → passez à la forme Moon Knight.\n<b>Réponse</b> : après avoir changé de forme, inclinez Khonshu → piochez une carte.",
  // moon_knight — Frenchie (Support)
  'mk004': "<b>Interruption</b> : quand de la menace devrait être placée sur la manigance principale, quelle qu'en soit la quantité, défaussez Frenchie → prévenez toute cette menace.",
  // moon_knight — Different Folks (Upgrade)
  'mk005': "Après avoir changé de forme, placez un compteur de folie ici.\n<b>Action de héros</b> : retirez 6 compteurs de folie de Different Folks → sonnez un ennemi.",
  // moon_knight — Different Strokes (Upgrade)
  'mk006': "<b>Interruption</b> : quand vous jouez une carte d'aspect, placez un compteur de folie ici. <i>(Limite d'une fois par round pour chaque aspect.)</i>\n<b>Action</b> : retirez 3 compteurs de folie de Different Strokes → redressez votre identité ou changez de forme.\n<b>Interruption forcée</b> : quand la phase des joueurs se termine, retirez tous les compteurs de folie de Different Strokes.",
  // moon_knight — Deck and Cover (Event)
  'mk007': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Si cet ennemi est mis K.O., changez de forme.\n<i>(Cette carte est à la fois une carte Moon Knight et une carte Agressivité.)</i>",
  // moon_knight — Fight or Foil (Event)
  'mk008': "Choisissez l'une ou l'autre :\n• <b>Action</b> <i>(attaque)</i> : passez à la forme Moon Knight → infligez 2 dégâts à un ennemi.\n• <b>Action</b> <i>(contre)</i> : passez à la forme Mr. Knight → retirez 2 menaces d'une manigance.\n<i>(Cette carte est à la fois une carte Moon Knight et une carte Justice.)</i>",
  // moon_knight — Gear Up (Event)
  'mk009': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous vous défendez contre une attaque, vous gagnez +2 DEF et riposte 2 jusqu'à la fin du round. Après la résolution de cette attaque, changez de forme.\n<i>(Cette carte est à la fois une carte Moon Knight et une carte Protection.)</i>",
  // moon_knight — Where'd He Go? (Event)
  'mk010': "Choisissez l'une ou l'autre :\n• <b>Action</b> : passez sous forme de héros → désorientez un ennemi.\n• <b>Action</b> : passez sous forme d'alter ego → sonnez un ennemi.\n<i>(Cette carte est à la fois une carte Moon Knight et une carte Leadership.)</i>",
  // moon_knight — Versatility (Event)
  'mk011': "Considérez cette carte comme appartenant à l'aspect de votre choix.\n<b>Action de héros</b> : si l'aspect de la carte du dessus de votre pile de défausse est :\n• Agressivité - Infligez 4 dégâts à un ennemi.\n• Justice - Retirez 3 menaces d'une manigance.\n• Leadership - Désorientez un ennemi.\n• Protection - Sonnez un ennemi.",
  // moon_knight — Seek Help (Obligation)
  'mk012': "<b><i>Donnez-la au joueur Marc Spector.</i></b>\nVous pouvez passer à Marc Spector. Choisissez :\n• Inclinez Marc Spector → retirez Seek Help de la partie.\n• Subissez 2 dégâts indirects → défaussez cette obligation.",
  // moon_knight — Bushman (Minion)
  'mk013': "<b>Interruption forcée</b> : quand Bushman devrait être mis K.O., s'il n'y a aucun compteur de folie ici, soignez plutôt tous ses dégâts et placez un compteur de folie sur lui.\n[star] Bushman gagne +2 ATQ s'il y a un compteur de folie ici.",
  // moon_knight — Mano a Mano (SideScheme)
  'mk014': "Moon Knight et Mr. Knight subissent -1 ATQ.",
  // moon_knight — Cull the Weak (Treachery)
  'mk015': "<b>Une fois révélée</b> : défaussez l'allié que vous contrôlez ayant le moins de points de vie restants. Si vous ne pouvez pas, subissez 2 dégâts à la place.",
  // moon_knight — Bushman's Knife (Attachment)
  'mk016': "Attachez-la à Bushman si possible. Sinon, attachez-la au sbire ayant le plus de points de vie restants.\n[star] Les attaques du personnage attaché gagnent perçant.\n<b>Action de héros</b> : dépensez une ressource [physical] → défaussez cette carte.",
  // moon_knight — Doctor Strange (Minion)
  'mk017': "Victoire 1. Vilenie.\n<b>Réponse forcée</b> : après que Doctor Strange a blessé votre héros, défaussez 1 carte au hasard de votre main.\n<b>Une fois vaincu</b> : le joueur qui a mis Doctor Strange K.O. met The Eye of Agamotto en jeu sous son contrôle.",
  // moon_knight — Ghost Rider (Minion)
  'mk018': "Victoire 1. Vilenie.\n[star] Les attaques de Ghost Rider gagnent perçant et déferlement.\n<b>Une fois vaincu</b> : le joueur qui met Ghost Rider K.O. met The Hell Charger en jeu sous son contrôle.",
  // moon_knight — Iron Fist (Minion)
  'mk019': "Victoire 1. Vilenie.\n<b>Réponse forcée</b> : après qu'Iron Fist a blessé un personnage que vous contrôlez, sonnez ce personnage.\n<b>Une fois vaincu</b> : le joueur qui a mis Iron Fist K.O. met The Iron Fist en jeu sous son contrôle.",
  // moon_knight — Thor (Minion)
  'mk020': "Victoire 1. Vilenie.\n<b>Réponse forcée</b> : après que Thor a blessé un personnage que vous contrôlez, attribuez-vous 1 carte rencontre.\n<b>Une fois vaincu</b> : le joueur qui a mis Thor K.O. met Mjolnir en jeu sous son contrôle.",
  // moon_knight — Mjolnir (Upgrade)
  'mk021': "Lié (Thor).\nVotre héros gagne +1 ATQ et le trait [[AERIAL]].\n<b>Réponse forcée</b> : après vous être engagé avec un sbire, inclinez Mjolnir et retirez-lui 1 compteur d'attaque → piochez 2 cartes.",
  // moon_knight — The Eye of Agamotto (Upgrade)
  'mk022': "Lié (Doctor Strange).\n<b>Ressource</b> : inclinez The Eye of Agamotto et retirez-lui 1 compteur mystique → générez 2 ressources [wild].",
  // moon_knight — The Hell Charger (Upgrade)
  'mk023': "Lié (Ghost Rider).\n<b>Action de héros</b> : inclinez The Hell Charger et retirez-lui 1 compteur de charge → votre prochaine attaque de cette phase gagne +2 ATQ, perçant et déferlement.",
  // moon_knight — The Iron Fist (Upgrade)
  'mk024': "Lié (Iron Fist).\n<b>Interruption de héros</b> : quand vous attaquez un ennemi, inclinez The Iron Fist et retirez-lui 1 compteur mystique → sonnez cet ennemi et infligez-lui 1 dégât supplémentaire.",
  // brawn — Brawn (Hero)
  'bw001a': "<i>The Complete Package</i> — tant que Brawn est incliné, il gagne : « <b>Ressource</b> : générez une ressource [mental]. <i>(Limite d'une fois par phase.)</i> »",
  // brawn — Amadeus Cho (AlterEgo)
  'bw001b': "Amadeus Cho commence la partie avec une réserve. <i>(Votre réserve est une zone hors-jeu qui contient au maximum 3 cartes. Vous pouvez jouer une carte de votre réserve en payant son coût, ou défausser une carte de votre réserve pour générer ses ressources. Les ressources générées depuis votre main ne peuvent pas payer une carte de votre réserve, et celles générées depuis votre réserve ne peuvent pas payer une carte de votre main.)</i>\n<i>Mastermind Excello</i> — <b>Action</b> : regardez les 2 cartes du dessus de votre deck. Placez l'une d'elles dans votre réserve et l'autre sur le dessus ou le dessous de votre deck. <i>(Limite d'une fois par round.)</i>",
  // brawn — Silk (Ally)
  'bw002': "<b>Action</b> : renvoyez Silk dans votre réserve → sonnez un sbire et infligez-lui 2 dégâts.\n<b>Réponse</b> : après avoir joué Silk depuis votre main, cherchez une traîtrise dans le deck rencontre et défaussez-la.",
  // brawn — Ironheart (Ally, alternative a Silk)
  'bw003': "Multivers.\n[star] <b>Interruption</b> : quand Ironheart utilise un pouvoir de base, le joueur Amadeus Cho place la carte du dessus de son deck dans sa réserve.",
  // brawn — Calculated Defense (Event)
  'bw004': "<b>Interruption de héros</b> : quand Brawn se défend contre une attaque, redressez Brawn et piochez 1 carte <i>(2 cartes à la place si Brawn ne s'est pas redressé de cette façon)</i>. Si vous avez joué cette carte depuis votre main en utilisant une ressource [mental], placez cette carte dans votre réserve.",
  // brawn — Calculated Defense (Event)
  'bw005': "<b>Interruption de héros</b> : quand Brawn se défend contre une attaque, redressez Brawn et piochez 1 carte <i>(2 cartes à la place si Brawn ne s'est pas redressé de cette façon)</i>. Si vous avez joué cette carte depuis votre main en utilisant une ressource [mental], placez cette carte dans votre réserve.",
  // brawn — Gamma Strike (Event)
  'bw006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 7 dégâts à un ennemi. Si vous avez payé cette carte uniquement avec des ressources [physical], cette attaque inflige 3 dégâts supplémentaires et gagne déferlement. Si vous avez payé cette carte uniquement avec des ressources [mental] et que vous l'avez jouée depuis votre main, placez-la dans votre réserve.",
  // brawn — Gamma Strike (Event)
  'bw007': "<b>Action de héros</b> <i>(attaque)</i> : infligez 7 dégâts à un ennemi. Si vous avez payé cette carte uniquement avec des ressources [physical], cette attaque inflige 3 dégâts supplémentaires et gagne déferlement. Si vous avez payé cette carte uniquement avec des ressources [mental] et que vous l'avez jouée depuis votre main, placez-la dans votre réserve.",
  // brawn — Heavy Lifting (Event)
  'bw008': "<b>Action de héros</b> <i>(contre)</i> : pour chaque ressource [physical] utilisée pour payer cette carte, votre héros gagne +1 ATQ jusqu'à la fin du round. Retirez d'une manigance un nombre de menaces égal à votre ATQ.",
  // brawn — Heavy Lifting (Event)
  'bw009': "<b>Action de héros</b> <i>(contre)</i> : pour chaque ressource [physical] utilisée pour payer cette carte, votre héros gagne +1 ATQ jusqu'à la fin du round. Retirez d'une manigance un nombre de menaces égal à votre ATQ.",
  // brawn — Shockwave (Event)
  'bw010': "<b>Action de héros</b> : défaussez les X cartes du dessus de votre deck <i>(maximum 5)</i>. Pour chaque ressource [physical] défaussée de cette façon, infligez 2 dégâts à chaque ennemi. Pour chaque ressource [mental] défaussée de cette façon, retirez 2 menaces de chaque manigance.",
  // brawn — Shockwave (Event)
  'bw011': "<b>Action de héros</b> : défaussez les X cartes du dessus de votre deck <i>(maximum 5)</i>. Pour chaque ressource [physical] défaussée de cette façon, infligez 2 dégâts à chaque ennemi. Pour chaque ressource [mental] défaussée de cette façon, retirez 2 menaces de chaque manigance.",
  // brawn — Cho's Lab (Support)
  'bw012': "<b>Réponse de héros</b> : après avoir changé de forme, inclinez Cho's Lab → placez la carte du dessous de votre deck dans votre réserve.\n<b>Action d'alter ego</b> : inclinez Cho's Lab → mélangez une carte Brawn de votre pile de défausse dans votre deck.",
  // brawn — Brawn's Suit (Upgrade)
  'bw013': "Vous gagnez +2 points de vie.\n<b>Réponse de héros</b> : après avoir joué une carte depuis votre réserve, infligez 1 dégât à un ennemi.",
  // brawn — Forward-Thinking (Upgrade)
  'bw014': "<b>Réponse</b> : après avoir joué une carte depuis votre réserve, redressez votre identité.",
  // brawn — Hulk Out (Upgrade)
  'bw015': "Utilisations <i>(2 compteurs de rage)</i>.\nPour chaque compteur de rage ici, Brawn gagne +1 ATQ et +1 DEF, et gagne riposte 1.\n<b>Interruption forcée</b> : quand le round se termine, retirez 1 compteur de rage d'ici.",
  // brawn — Hulk Out (Upgrade)
  'bw016': "Utilisations <i>(2 compteurs de rage)</i>.\nPour chaque compteur de rage ici, Brawn gagne +1 ATQ et +1 DEF, et gagne riposte 1.\n<b>Interruption forcée</b> : quand le round se termine, retirez 1 compteur de rage d'ici.",
  // brawn — Totally Awesome (Upgrade)
  'bw017': "<b>Réponse de héros</b> : après avoir joué une carte depuis votre réserve, retirez 1 menace d'une manigance.",
  // brawn — Analysis Paralysis (Obligation)
  'bw018': "<b><i>Donnez-la au joueur Amadeus Cho.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Amadeus Cho → retirez Analysis Paralysis de la partie.\n• Vous êtes sonné et désorienté. Si vous étiez déjà sonné et désorienté, cette carte gagne renfort. Défaussez cette obligation.",
  // brawn — Rising Tide (SideScheme)
  'bw019': "<i>Outré par le mépris des habitants de la surface pour l'océan, Namor invoque un raz-de-marée colossal pour balayer l'œuvre des hommes.</i>\nEntrave 2[per_hero].\n<b>Une fois révélée</b> : placez 1 jeton d'accélération ici.\n<b>Interruption forcée</b> : quand la phase du Méchant commence, placez 1 jeton d'accélération ici.",
  // brawn — Namor (Minion)
  'bw020': "Patrouille. Ténacité.\n[star] Namor gagne +X ATQ et +X MNG, où X est égal au nombre de jetons d'accélération en jeu.\n<b>Interruption forcée</b> : quand Namor manigance, placez cette menace sur Rising Tide à la place.",
  // brawn — Imperius Rex! (Treachery)
  'bw021': "<b>Une fois révélée</b> : Namor s'active contre vous. S'il n'est pas en jeu, cherchez Namor, mettez-le en jeu engagé avec vous et donnez-lui 1 carte de boost face cachée.\n<hr />\n[star] <b>Boost</b> : attribuez-vous cette carte comme carte Rencontre face cachée.",
  // brawn — Tidal Renfort (Treachery)
  'bw022': "Renfort.\n<b>Une fois révélée</b> : placez 1 jeton d'accélération sur Rising Tide. Si Namor est en jeu, donnez-lui une carte d'état Tenace.\n<hr />\n[star] <b>Boost</b> : donnez à l'ennemi qui s'active 1 carte de boost supplémentaire.",
  // brawn — Tidal Renfort (Treachery)
  'bw023': "Renfort.\n<b>Une fois révélée</b> : placez 1 jeton d'accélération sur Rising Tide. Si Namor est en jeu, donnez-lui une carte d'état Tenace.\n<hr />\n[star] <b>Boost</b> : donnez à l'ennemi qui s'active 1 carte de boost supplémentaire.",
  // brawn — Strong as Silk (Event, Team-Up)
  'bw024': "En Équipe (Brawn et Silk). 1 max par deck.\n<b>Action de héros</b> : Brawn et Silk gagnent +1 ATQ jusqu'à la fin du round. Brawn et Silk peuvent chacun effectuer une attaque de base sans s'incliner.",
  // brawn — Brains and Brawn (Event, Team-Up)
  'bw025': "En Équipe (Brawn et Ironheart). 1 max par deck.\n<b>Action de héros</b> : pour chaque ressource imprimée dans votre main et votre réserve, si c'est une :\n[physical] - infligez 1 dégât à un ennemi.\n[mental] - retirez 1 menace d'une manigance.",
  // lockjaw — Lockjaw (Hero)
  'lj001a': "<i>Rapporte !</i> — <b>Action</b> : inclinez Lockjaw et dépensez une ressource [mental] → choisissez une carte qui n'est pas une ressource dans la pile de défausse de n'importe quel joueur et ajoutez-la à la main de son propriétaire. <i>(Limite d'une fois par round.)</i>",
  // lockjaw — Lockjaw (AlterEgo)
  'lj001b': "<b>Mise en place</b> : cherchez Tuning Fork dans votre deck, votre main et votre pile de défausse, et mettez-la en jeu.\n<i>Réconfort</i> — <b>Réponse</b> : après être passé à cette forme, redressez un personnage allié.",
  // lockjaw — Black Bolt (Ally)
  'lj002': "[star] <b>Interruption forcée</b> : quand Black Bolt attaque, défaussez X cartes du deck de chaque joueur et du deck rencontre. X est égal à l'ATQ de Black Bolt.",
  // lockjaw — Tuning Fork (Upgrade)
  'lj003': "Vous pouvez jouer des soutiens [[LOCATION]] depuis votre pile de défausse pendant votre tour <i>(en payant leur coût en ressources)</i>.\n<b>Ressource</b> : inclinez Tuning Fork → générez une ressource [wild].",
  // lockjaw — Jaw Lock (Upgrade)
  'lj004': "Attachez-la à un ennemi. Forme de héros uniquement.\n<b>Réponse</b> : après avoir joué un événement [[TELEPORT]], infligez 1 dégât à l'ennemi attaché.\n<b>Interruption</b> : quand l'ennemi attaché devrait s'activer, défaussez plutôt Jaw Lock.",
  // lockjaw — Kamala's Room (Support)
  'lj005': "Votre alter ego gagne +1 REC.\n<b>Action d'alter ego</b> : inclinez Kamala's Room → regardez les 3 cartes du dessus de votre deck. Ajoutez-en 1 à votre main et défaussez les autres.",
  // lockjaw — New Attilan (Support)
  'lj006': "<b>Action d'alter ego</b> : inclinez New Attilan → défaussez les cartes du dessus de votre deck jusqu'à défausser une carte Lockjaw. Puis, ajoutez cette carte à votre main.",
  // lockjaw — Doc Jaw's Lab (Support)
  'lj007': "<b>Action d'alter ego</b> : inclinez Doc Jaw's Lab → redressez Tuning Fork.",
  // lockjaw — Teleport To Safety (Event)
  'lj008': "<b>Interruption</b> : quand une identité devrait subir des dégâts d'une attaque, quel qu'en soit le nombre, changez la forme de cette identité → prévenez tous ces dégâts.",
  // lockjaw — Fast Travel (Event)
  'lj009': "<b>Action</b> : choisissez un joueur. Ce joueur change de forme. Si vous avez payé cette carte avec une ressource [mental], vous pouvez changer de forme.",
  // lockjaw — Zooming Around (Event)
  'lj010': "<b>Action de héros</b> : choisissez un joueur. Infligez 1 dégât à chaque ennemi engagé avec ce joueur. Retirez 1 menace de chaque manigance. Si vous avez payé cette carte avec une ressource [mental], vous pouvez changer de forme.",
  // lockjaw — Ruff Ambush (Event)
  'lj011': "<b>Réponse de héros</b> <i>(attaque)</i> : après être passé sous forme de héros, infligez 5 dégâts à un ennemi <i>(7 dégâts à la place si vous avez payé cette carte avec une ressource [mental])</i>.",
  // lockjaw — Psionic Tracking (Event)
  'lj012': "<b>Action d'alter ego</b> : choisissez un joueur. Cherchez n'importe quelle carte dans le deck de ce joueur et défaussez-la.",
  // lockjaw — Canine Urges (Obligation)
  'lj013': "<b><i>Donnez-la au joueur Lockjaw.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Lockjaw et Tuning Fork → retirez Canine Urges de la partie.\n• Défaussez tous les événements [[TELEPORT]] de votre main. Si aucun événement n'a été défaussé de cette façon, cette carte gagne renfort. Défaussez cette obligation.",
  // lockjaw — Dognapped! (SideScheme)
  'lj014': "<b>Réponse forcée</b> : après qu'un événement [[TELEPORT]] a été joué, placez 1 menace ici.",
  // lockjaw — Annihilus (Minion)
  'lj015': "<b>Interruption forcée</b> : quand Annihilus devrait être mis K.O., mélangez-le plutôt dans le deck rencontre.\n[star] <b>Boost</b> : après la fin de cette activation, mélangez cette carte dans le deck rencontre.",
  // lockjaw — Dog Catcher (Minion)
  'lj016': "Renfort.\n[star] <b>Interruption forcée</b> : quand Dog Catcher devrait manigancer, il attaque à la place.",
  // lockjaw — Provoked (Attachment)
  'lj017': "Attachez-la à votre carte d'identité.\nLe personnage attaché ne peut pas passer sous forme d'alter ego.\n[star] <b>Réponse</b> : après que le personnage attaché a attaqué, placez 1 compteur de calme ici.\n<b>Interruption forcée</b> : quand il y a 3 compteurs de calme ou plus ici, défaussez cette carte.",
  // lockjaw — Zabu (Ally)
  'lj018': "Compagnon. <i>(Cet allié ne compte pas dans la limite d'alliés et ne peut pas servir à se défendre contre les attaques.)</i>\n[star] Les attaques de Zabu gagnent perçant.",
  // lockjaw — Throg (Ally)
  'lj019': "Compagnon. <i>(Cet allié ne compte pas dans la limite d'alliés et ne peut pas servir à se défendre contre les attaques.)</i>\n<b>Action</b> : dépensez une ressource [energy] et inclinez Throg → retirez 1 menace de chaque manigance. Infligez 1 dégât à Throg.",
  // lockjaw — Redwing (Ally)
  'lj020': "Compagnon. <i>(Cet allié ne compte pas dans la limite d'alliés et ne peut pas servir à se défendre contre les attaques.)</i>\n<b>Action de héros</b> : inclinez Redwing et infligez-lui 1 dégât → regardez la carte du dessus du deck rencontre.",
  // lockjaw — Hairball (Ally)
  'lj021': "Compagnon. <i>(Cet allié ne compte pas dans la limite d'alliés et ne peut pas servir à se défendre contre les attaques.)</i>\n<b>Interruption</b> : quand un personnage allié devrait subir des dégâts d'une attaque, quel qu'en soit le nombre, inclinez Hairball → prévenez 1 de ces dégâts.",
  // lockjaw — Lockheed (Ally)
  'lj022': "Compagnon. <i>(Cet allié ne compte pas dans la limite d'alliés et ne peut pas servir à se défendre contre les attaques.)</i>\n[star] Les attaques de Lockheed gagnent à distance.",
  // lockjaw — Protect The Pack (Event)
  'lj023': "<b>Interruption de héros</b> : quand un personnage allié devrait subir des dégâts, quel qu'en soit le nombre <i>(y compris des dégâts consécutifs)</i>, subissez ces dégâts à sa place.",
  // lockjaw — Wet Slobbering Kiss (Event)
  'lj024': "<b>Action</b> : choisissez l'une ou l'autre :\n• Soignez 3 dégâts d'un personnage allié qui n'est pas votre identité.\n• Infligez 3 dégâts à un ennemi.",
  // lockjaw — Ms. Lion (Ally)
  'lj025': "Compagnon. <i>(Cet allié ne compte pas dans la limite d'alliés et ne peut pas servir à se défendre contre les attaques.)</i>",
  // lockjaw — Ms. Marvel (Ally)
  'lj026': "[star] <b>Interruption</b> : quand Ms. Marvel contre, elle gagne +1 CTR et subit +1 dégât consécutif pour ce contre.\n[star] <b>Interruption</b> : quand Ms. Marvel attaque, elle gagne +1 ATQ et subit +1 dégât consécutif pour cette attaque.",
  // lockjaw — Animals Unleashed (Event)
  'lj027': "1 max par deck.\n<b>Action de héros</b> : chaque joueur peut chercher un allié [[PET AVENGER]] dans son deck, sa main et sa pile de défausse, et le mettre en jeu. Chaque [[PET AVENGER]] gagne +1 ATQ jusqu'à la fin du round.",
  // lockjaw — Companionship (Event)
  'lj028': "<b>Action</b> : inclinez un [[PET AVENGER]] que vous contrôlez → choisissez un joueur. Ce joueur pioche 2 cartes.",
  // lockjaw — Inhuman's Best Friend (Event)
  'lj029': "Team-Up <i>(Lockjaw et Ms. Marvel)</i>. 1 max par deck.\n<b>Action d'alter ego</b> : redressez jusqu'à 4 soutiens que vous contrôlez.",
  // lockjaw — Central Park (Support)
  'lj030': "<b>Action d'alter ego</b> : inclinez Central Park → soignez 1 dégât d'un [[PET AVENGER]] ou d'un [[GOOD BOY]].",
  // stanlee — Stan Lee (Hero)
  '90101a': "Stan Lee possède les zones de texte de chaque héros utilisé avec la capacité <i>Marvelous</i>.",
  // stanlee — Stan Lee (AlterEgo)
  '90101b': "Stan Lee possède les zones de texte de chaque alter ego utilisée avec la capacité <i>Marvelous</i>.\n<i>Marvelous</i> — Pendant la construction du deck, votre deck doit inclure 15 cartes spécifiques à un héros, prises parmi les autres sets de héros de votre collection.",
  // rainy — Hulk (Hero)
  '90102a': "Colère — <b>Réponse</b> : après que Hulk a subi des dégâts, infligez 1 dégât à un ennemi.",
  // rainy — Bruce Banner (AlterEgo)
  '90102b': "Sortez le gros bras — <b>Interruption</b> : quand un ennemi devrait manigancer, dépensez une ressource [physical] → passez sous forme de héros. Cet ennemi vous attaque à la place.",
  // rainy — Black Widow (Ally)
  '90103': "[star] <b>Réponse</b> : après que Black Widow a contré, retirez 1 menace d'une autre manigance.\n<b>Action de héros</b> : inclinez Black Widow → passez sous forme d'alter ego.",
  // rainy — Brilliant Mind (Event)
  '90104': "<b>Action d'alter ego</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Si vous avez payé cette carte en n'utilisant que des ressources [mental], choisissez soit de retirer 2 menaces supplémentaires de cette manigance, soit de désorienter un ennemi.",
  // rainy — Hulk Smash (Event)
  '90105': "<b>Action de héros</b> : faites les attaques suivantes contre la même cible :\n• <i>(attaque)</i> : infligez 3 dégâts.\n• <i>(attaque)</i> : infligez 3 dégâts.\n• <i>(attaque)</i> : infligez 3 dégâts.",
  // rainy — Interception (Event)
  '90106': "<b>Interruption de héros</b> : quand une traîtrise est révélée, subissez 2 dégâts → annulez tous ses effets et défaussez-la. Si vous avez payé cette carte en trop avec une ressource [energy] ou [physical], retirez 2 menaces d'une manigance.",
  // rainy — Reckless Charge (Event)
  '90107': "<b>Action de héros</b> <i>(attaque)</i> : infligez 1 dégât à Hulk → infligez 3 dégâts à un ennemi. Si vous avez payé cette carte avec une ressource [physical], cette attaque gagne déferlement.",
  // rainy — Natural Genius (Resource)
  '90108': "Ne dépensez cette carte qu'sous forme d'alter ego.",
  // rainy — Unnatural Strength (Resource)
  '90109': "Ne dépensez cette carte qu'sous forme de héros.",
  // rainy — The Other Guy (Support)
  '90110': "<b>Réponse d'alter ego</b> <i>(contre)</i> : après avoir changé de forme, retirez 1 menace d'une manigance. <i>(Limite d'une fois par phase.)</i>\n<b>Réponse de héros</b> <i>(attaque)</i> : après avoir changé de forme, infligez 1 dégât à un ennemi. <i>(Limite d'une fois par phase.)</i>",
  // rainy — Intimidating Roar (Upgrade)
  '90111': "<b>Réponse de héros</b> <i>(contre)</i> : après que Hulk a subi des dégâts d'une attaque, inclinez Intimidating Roar → retirez 1 menace d'une manigance (2 menaces à la place si vous avez subi 3 dégâts ou plus).",
  // rainy — Limitless Endurance (Upgrade)
  '90112': "Vous gagnez +3 points de vie et Bruce Banner gagne +1 REC.\n<b>Action de héros</b> : inclinez Limitless Endurance → soignez 1 dégât de Hulk.",
  // rainy — Limitless Strength (Upgrade)
  '90113': "Hulk gagne +1 ATQ.\n<b>Ressource de héros</b> : inclinez Limitless Strength → générez une ressource [physical].",
  // rainy — Rescue (Hero)
  '90114a': "Intervention rapide — [star] <b>Réponse</b> : après avoir utilisé votre DEF de base, faites un contre ou une attaque de base sans incliner Rescue.",
  // rainy — Pepper Potts (AlterEgo)
  '90114b': "Cadre dirigeante — <b>Action</b> : chaque joueur peut défausser 1 carte de sa main pour chercher une amélioration [[TECH]] dans son deck et l'ajouter à sa main. <i>(Limite d'une fois par round.)</i>",
  // rainy — Iron Man (Ally)
  '90115': "[star] <b>Interruption</b> : quand Iron Man utilise un pouvoir de base, dépensez 1 ressource de n'importe quel type → Iron Man gagne +2 à ce pouvoir de base pour cette utilisation.",
  // rainy — Magnetic Restraints (Event)
  '90116': "<b>Action de héros</b> : choisissez l'un ou l'autre :\n• Sonnez un ennemi.\n• Choisissez un attachement dont le texte contient \"Action de héros\" ou \"Réponse de héros\" et défaussez-le.",
  // rainy — Repulsor Blasts (Event)
  '90117': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Cette attaque gagne à distance. Dépensez X ressources [energy] (maximum 3) → répétez cette attaque X fois contre les cibles de votre choix.",
  // rainy — Responsive (Event)
  '90118': "<b>Réponse de héros</b> : après avoir utilisé un pouvoir de base, redressez Rescue. Vous gagnez +1 à un pouvoir de base de votre choix <i>(CTR, ATQ ou DEF)</i> jusqu'à la fin du round.",
  // rainy — Search and Rescue (Event)
  '90119': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. S'il y a une icône de crise en jeu, retirez 2 menaces supplémentaires de cette manigance et ce contre ignore l'icône de crise.",
  // rainy — Stark Resilient (Support)
  '90120': "<b>Ressource</b> : inclinez Stark Resilient → générez une ressource [wild] pour n'importe quel joueur.",
  // rainy — First Responder (Upgrade)
  '90121': "Utilisations (3 compteurs médicaux).\n<b>Réponse de héros</b> : après qu'un autre personnage a subi des dégâts, inclinez cette carte et retirez-lui 1 compteur médical → soignez 1 dégât de ce personnage (2 dégâts à la place s'il s'agit d'une identité).",
  // rainy — Magnetic Deflector (Upgrade)
  '90122': "<b>Interruption de héros</b> <i>(défense)</i> : quand un ennemi initie une attaque, défaussez la carte du dessus de votre deck → cet ennemi subit -1 ATQ pour cette attaque. <i>(Limite de deux fois par round.)</i>",
  // rainy — Model V Chassis (Upgrade)
  '90123': "Vous gagnez +3 points de vie.\n<b>Réponse de héros</b> : après vous être défendu sans subir de dégâts, inclinez Model V Chassis et dépensez 1 ressource de n'importe quel type → donnez une carte d'état Tenace à Rescue.",
  // rainy — Model V Helmet (Upgrade)
  '90124': "Rescue gagne +1 CTR et ignore le mot-clé patrouille.\n<b>Réponse de héros</b> <i>(contre)</i> : après qu'une manigance annexe est entrée en jeu, inclinez Model V Helmet → retirez 1 menace de cette manigance (2 menaces à la place s'il y a une icône de crise en jeu).",
  // rainy — Repulsor Gauntlets (Upgrade)
  '90125': "Rescue gagne +1 ATQ.\n<b>Interruption de héros</b> : quand Rescue fait une attaque de base, inclinez Repulsor Gauntlets → cette attaque gagne à distance.",
  // rainy — Board Meeting (Obligation)
  '90126': "<b><i>Donnez-la au joueur Pepper Potts.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Pepper Potts → retirez Board Meeting de la partie.\n• Défaussez 1 amélioration [[TECH]] que vous contrôlez. Si aucune amélioration n'a été défaussée de cette façon, cette carte gagne renfort. Défaussez cette obligation.",
  // rainy — Helicopter Crash (SideScheme)
  '90127': "Un hélicoptère de presse s'est écrasé dans une zone très peuplée et des civils sont en danger ! Évacuez-les avant que l'appareil n'explose et que d'autres vies ne soient perdues.",
  // rainy — Burning Building (Environment)
  '90128': "<b>Réponse forcée</b> : après le début de la phase du méchant, infligez 1 dégât indirect à chaque joueur.\n<b>Action de héros</b> : inclinez votre héros et dépensez une ressource [physical] → défaussez Burning Building.",
  // rainy — Wounded Civilians (Obligation)
  '90129': "Utilisations (1 [per_player] compteurs de civil).\n<b>Interruption</b> : quand un joueur devrait soigner des dégâts d'un personnage, retirez plutôt 1 compteur de civil d'ici.",
  // rainy — Catastrophic Collision (Treachery)
  '90130': "Péril.\n<b>Une fois révélée</b> : choisissez l'une des options suivantes :\n• Infligez 2 [per_player] dégâts indirects aux joueurs. Ces dégâts gagnent perçant.\n• Attribuez à chaque joueur 1 carte rencontre face cachée.\n• Chaque joueur défausse de sa main la carte au coût le plus élevé.",
  // rainy — Innocent Bystander (Attachment)
  '90131': "Attachez-la à votre identité.\nVous subissez -1 en taille de main.\n<b>Action de héros</b> : inclinez votre héros → défaussez cette carte et retirez 1 menace d'une manigance.\n[star] <b>Boost</b> : placez 2 menaces sur la manigance principale.",
  // rainy — Agent 13 (Hero)
  'ag001a': "<i>Hand-to-Hand Specialist</i> — <b>Réponse</b> : après qu'Agent 13 utilise un pouvoir de base, redressez Agent 13 et faites une attaque de base contre un ennemi. <i>(Limite d'une fois par round.)</i>",
  // rainy — Sharon Carter (AlterEgo)
  'ag001b': "<i>Super Spy</i> — <b>Action</b> : choisissez une carte de la pile de défausse rencontre et placez-la sur le dessus du deck rencontre. Puis, retirez d'une manigance un nombre de menaces égal au nombre d'icônes de boost sur cette carte. <i>(Limite d'une fois par round.)</i>",
  // rainy — Captain America (Steve Rogers) (Ally)
  'ag002': "Riposte 1.\n<b>Interruption</b> : quand Captain America se défend contre une attaque et devrait subir des dégâts, réduisez ces dégâts de 2 (jusqu'à un minimum de 1).",
  // rainy — Burst Fire (Event)
  'ag003': "<b>Action de héros</b> : faites les 2 attaques suivantes :\n- Infligez 2 dégâts à un ennemi. Cette attaque gagne à distance.\n- Infligez 2 dégâts à un ennemi. Cette attaque gagne à distance.",
  // rainy — Infiltrate (Event)
  'ag004': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Regardez la carte du dessus du deck rencontre et retirez 1 menace supplémentaire par icône de boost sur cette carte. Puis, vous pouvez défausser cette carte de rencontre.",
  // rainy — Parting Shots (Event)
  'ag005': "<b>Interruption de héros</b> <i>(attaque)</i> : quand un ennemi devrait initier une attaque contre vous, infligez 2 dégâts à cet ennemi. Cette attaque gagne à distance. Vous pouvez passer sous forme d'alter ego → cet ennemi manigance à la place.",
  // rainy — Takedown (Event)
  'ag006': "<b>Réponse de héros</b> <i>(attaque)</i> : après avoir attaqué un ennemi, infligez 2 dégâts à un ennemi. Si cet ennemi est mis K.O. par cette attaque, piochez 1 carte.",
  // rainy — Briefing Room (Support)
  'ag007': "<b>Réponse de héros</b> : après qu'un sbire ou une manigance annexe est révélé, inclinez Briefing Room → chaque joueur sous forme de héros pioche 1 carte.",
  // rainy — Agent 13's Pistol (Upgrade)
  'ag008': "Restreint.\n<b>Réponse de héros</b> : après qu'Agent 13 attaque, inclinez Agent 13's Pistol et défaussez la carte du dessus du deck rencontre → infligez 1 dégât à un ennemi par icône de boost défaussée de cette façon.",
  // rainy — Physical Training (Upgrade)
  'ag009': "Vous gagnez +2 points de vie.\nAgent 13 gagne +1 ATQ.",
  // rainy — Secret Agent (Upgrade)
  'ag010': "<b>Ressource de héros</b> : inclinez Secret Agent → générez une ressource [wild].",
  // rainy — Assassination Plot (SideScheme)
  'ag011': "<b>Une fois révélée</b> : défaussez l'allié que vous contrôlez ayant le plus de points de vie restants. Si vous ne pouvez pas, placez 2 menaces sur cette manigance.",
  // rainy — Doctor Faustus (Minion)
  'ag012': "Doctor Faustus ne peut pas subir de dégâts tant que vous êtes engagé avec un autre sbire.\n[star] <b>Interruption forcée</b> : quand Doctor Faustus devrait vous attaquer alors que vous contrôlez un allié, cet allié vous inflige des dégâts égaux à son ATQ à la place.",
  // rainy — Hallucination (Attachment)
  'ag013': "<b>Une fois révélée</b> : défaussez des cartes du deck rencontre jusqu'à défausser un sbire. Révélez ce sbire et attachez cette carte à lui. Si vous ne pouvez pas, cette carte gagne renfort.\n<b>Interruption forcée</b> : quand le sbire attaché devrait subir des dégâts, quel qu'en soit le nombre, défaussez-le et placez 3 menaces sur la manigance principale.",
  // rainy — Hypnotic Suggestion (Treachery)
  'ag014': "<b>Une fois révélée (alter ego)</b> : vous êtes désorienté. Cette carte gagne renfort.\n<b>Une fois révélée (héros)</b> : désorientez votre héros et placez sur la manigance principale un nombre de menaces égal à votre CTR.",
  // rainy — Sleeper Agent (Obligation)
  'ag015': "<b><i>Donnez-la au joueur Sharon Carter.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n- Retirez l'allié Captain America de la partie → retirez Sleeper Agent de la partie.\n- Défaussez 1 carte de votre main et placez 2 menaces sur la manigance principale. Défaussez cette obligation.",

  // okoye — Okoye (Hero)
  'ok001a': "<i>L'Art de la guerre</i> — <b>Réponse</b> : après avoir effectué une attaque de base ou un contre de base, les alliés [[DORA MILAJE]] que vous contrôlez subissent 1 dégât consécutif de moins lorsqu'ils effectuent le même pouvoir de base jusqu'à la fin de la phase. <i>(Limite d'une fois par round.)</i>",
  // okoye — Okoye (AlterEgo)
  'ok001b': "<i>Meneuse de l'avant-garde</i> — <b>Mise en place</b> : cherchez une carte [[REINFORCEMENTS]] dans votre deck et votre pile de défausse, et ajoutez-la à votre main. <i>(Mélangez.)</i>\n<i>Rassemblement des forces</i> — <b>Action</b> : mélangez une carte [[REINFORCEMENTS]] de votre pile de défausse dans votre deck. <i>(Limite d'une fois par round.)</i>",
  // okoye — Aneka (Ally)
  'ok002': "<b>Réponse</b> : après qu'Aneka est entrée en jeu, tous les autres alliés [[DORA MILAJE]] que vous contrôlez gagnent +1 ATQ jusqu'à la fin de la phase.",
  // okoye — Ayo (Ally)
  'ok003': "<b>Réponse</b> : après qu'Ayo est entrée en jeu, tous les autres alliés [[DORA MILAJE]] que vous contrôlez gagnent +1 CTR jusqu'à la fin de la phase.",
  // okoye — Adored Ones (Event) x2
  'ok004': "<b>Action de héros</b> : choisissez une option :\n• Créez 2 alliés Dora Milaje et mettez-les en jeu.\n• Cherchez Aneka ou Ayo dans votre deck et votre pile de défausse, et mettez-la en jeu.",
  'ok005': "<b>Action de héros</b> : choisissez une option :\n• Créez 2 alliés Dora Milaje et mettez-les en jeu.\n• Cherchez Aneka ou Ayo dans votre deck et votre pile de défausse, et mettez-la en jeu.",
  // okoye — Angelic Warfare (Event) x2
  'ok006': "<b>Action de héros</b> : créez 2 alliés Midnight Angel et mettez-les en jeu.\n<b>Action de héros</b> : redressez Okoye et donnez à jusqu'à 3 alliés une carte d'état Tenace.",
  'ok007': "<b>Action de héros</b> : créez 2 alliés Midnight Angel et mettez-les en jeu.\n<b>Action de héros</b> : redressez Okoye et donnez à jusqu'à 3 alliés une carte d'état Tenace.",
  // okoye — Spear Thrust (Event) x2
  'ok008': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Vous pouvez incliner jusqu'à 3 personnages [[DORA MILAJE]] que vous contrôlez pour infliger un total de X dégâts répartis entre des ennemis comme vous le souhaitez, X étant le nombre d'alliés inclinés dans le cadre de cet effet.",
  'ok009': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Vous pouvez incliner jusqu'à 3 personnages [[DORA MILAJE]] que vous contrôlez pour infliger un total de X dégâts répartis entre des ennemis comme vous le souhaitez, X étant le nombre d'alliés inclinés dans le cadre de cet effet.",
  // okoye — Close Ranks (Support)
  'ok010': "<b>Réponse</b> : après qu'un allié [[DORA MILAJE]] que vous contrôlez a été mis K.O., placez 1 compteur de phalange ici <i>(jusqu'à un maximum de 3)</i>.\n<b>Ressource</b> : inclinez Close Ranks et retirez n'importe quel nombre de compteurs de phalange ici → générez autant de ressources [physical].",
  // okoye — Upanga (Support)
  'ok011': "Chaque allié [[DORA MILAJE]] que vous contrôlez gagne +1 point de vie.\n<b>Action d'alter ego</b> : inclinez Upanga → mélangez 1 carte [[ARMOR]], [[TECH]] ou [[WEAPON]] de votre pile de défausse dans votre deck.",
  // okoye — Midnight Angel Armor (Upgrade) x2
  'ok012': "Attachez-la à un personnage [[DORA MILAJE]] allié. 1 max par personnage.\nLe personnage attaché gagne +2 points de vie, gagne le trait [[AERIAL]], et perd le mot-clé fragile.",
  'ok013': "Attachez-la à un personnage [[DORA MILAJE]] allié. 1 max par personnage.\nLe personnage attaché gagne +2 points de vie, gagne le trait [[AERIAL]], et perd le mot-clé fragile.",
  // okoye — Royal Protector (Upgrade)
  'ok014': "Votre limite d'alliés augmente de 1. Okoye gagne +1 CTR sous forme de héros.\n<b>Réponse de héros</b> : après qu'un allié [[WAKANDA]] a été mis K.O., inclinez Royal Protector → redressez Okoye.",
  // okoye — Vibranium Spear (Upgrade) x2
  'ok015': "Attachez-la à un personnage [[WAKANDA]] allié.\nRestreint. 1 max par personnage.\nLe personnage attaché gagne +1 ATQ (+2 ATQ à la place si attaché à un allié) et ses attaques de base gagnent perçant.",
  'ok016': "Attachez-la à un personnage [[WAKANDA]] allié.\nRestreint. 1 max par personnage.\nLe personnage attaché gagne +1 ATQ (+2 ATQ à la place si attaché à un allié) et ses attaques de base gagnent perçant.",
  // okoye — Dora Milaje (jeton Created Ally)
  'ok017': "Fragile. <i>(Les attaques contre ce personnage gagnent déferlement.)</i>\nLégion. <i>(2 alliés ayant le mot-clé légion comptent comme 1 allié pour votre limite d'alliés.)</i>",
  // okoye — Midnight Angel (jeton Created Ally)
  'ok018': "Fragile. <i>(Les attaques contre ce personnage gagnent déferlement.)</i>\nLégion. <i>(2 alliés ayant le mot-clé légion comptent comme 1 allié pour votre limite d'alliés.)</i>",
  // okoye — Funeral Rites (Obligation)
  'ok019': "<b><i>Donnez-la au joueur Okoye.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez votre alter ego et tous les alliés [[DORA MILAJE]] que vous contrôlez → retirez Funeral Rites de la partie.\n• Inclinez 3 alliés [[DORA MILAJE]] que vous contrôlez. Si aucun allié n'a été incliné de cette façon, cette carte gagne renfort. Défaussez cette obligation.",
  // okoye — Malevolent Mimic (SideScheme, nemesis)
  'ok020': "<i>Nakia a détourné une arme secrète wakandaise — un mimique. Elle l'a empoisonnée pour semer le chaos parmi les civils innocents !</i>\n<b>Réponse forcée</b> : après qu'un allié a été mis K.O., placez 2 menaces ici.",
  // okoye — Malice (Minion, nemesis)
  'ok021': "Solide.\n<b>Réponse forcée</b> : après qu'un allié a été mis K.O., Malice manigance.\n<i>(Sbire némésis d'Okoye.)</i>",
  // okoye — Mimic-27 (Minion, nemesis)
  'ok022': "X est égal à votre ATQ (X est égal à 0 à la place si vous êtes sous forme d'alter ego).\n<b>Interruption forcée</b> : quand Mimic-27 attaque, vous devez choisir un allié pour défendre contre son attaque, si possible.\n<b>Réponse forcée</b> : après que Mimic-27 a attaqué et mis K.O. un personnage, elle attaque à nouveau. <i>(Limite d'une fois par round.)</i>",
  // okoye — War Drumming (Treachery, nemesis) x2
  'ok023': "<b>Une fois révélée (alter ego)</b> : cette carte gagne renfort.\n<b>Une fois révélée (héros)</b> : choisissez un sbire en jeu. Ce sbire vous attaque. Si l'ATQ de l'ennemi attaquant est de 2 ou moins, il gagne vilenie pour cette attaque. Si son ATQ est de 3 ou plus, il gagne déferlement pour cette attaque. S'il n'y a aucun sbire en jeu, cette carte gagne renfort.",
  'ok024': "<b>Une fois révélée (alter ego)</b> : cette carte gagne renfort.\n<b>Une fois révélée (héros)</b> : choisissez un sbire en jeu. Ce sbire vous attaque. Si l'ATQ de l'ennemi attaquant est de 2 ou moins, il gagne vilenie pour cette attaque. Si son ATQ est de 3 ou plus, il gagne déferlement pour cette attaque. S'il n'y a aucun sbire en jeu, cette carte gagne renfort.",

  // iron_lad — Iron Lad (Hero)
  'il001a': "<i>Destin</i> — <b>Action</b> : nommez un type de ressource et regardez les 4 cartes du dessus de votre deck. Ajoutez jusqu'à 2 cartes portant le type de ressource choisi à votre main et défaussez les autres. <i>(Limite d'une fois par round.)</i>",
  // iron_lad — Iron Lad (AlterEgo, Nathaniel Richards)
  'il001b': "<i>Génie inventif</i> — <b>Action</b> : réduisez le coût en ressources de la prochaine carte [[TECH]] jouée cette phase de 2. <i>(Limite d'une fois par round.)</i>",
  // iron_lad — Stature (Ally)
  'il002': "<b>Réponse</b> : après que Stature est entrée en jeu, soignez 1 dégât de votre identité. Vous pouvez défausser jusqu'à 3 cartes de votre deck pour soigner 1 dégât supplémentaire par carte défaussée.",
  // iron_lad — Energy Overflow (Event)
  'il003': "<b>Action de héros</b> : défaussez une carte [[TECH]] que vous contrôlez → infligez 6 dégâts à X ennemis en jeu, X étant égal au coût en ressources imprimé de la carte défaussée. Ces dégâts ignorent les cartes d'état Tenace.",
  // iron_lad — Ion Blast (Event) x3
  'il004': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Vous pouvez défausser 5 cartes de votre deck pour infliger 6 dégâts à la place.",
  'il005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Vous pouvez défausser 5 cartes de votre deck pour infliger 6 dégâts à la place.",
  'il006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Vous pouvez défausser 5 cartes de votre deck pour infliger 6 dégâts à la place.",
  // iron_lad — Seeking Solutions (Event) x2
  'il007': "<b>Action d'alter ego</b> : mélangez 2 cartes de votre défausse dans votre deck. Piochez 1 carte par carte [[TECH]] mélangée dans votre deck de cette façon.",
  'il008': "<b>Action d'alter ego</b> : mélangez 2 cartes de votre défausse dans votre deck. Piochez 1 carte par carte [[TECH]] mélangée dans votre deck de cette façon.",
  // iron_lad — Vision AI (Support)
  'il009': "<b>Action d'alter ego</b> : inclinez Vision AI → mélangez la carte du dessus de votre défausse dans votre deck. Retournez la carte du dessous de votre défausse dans votre main.",
  // iron_lad — Hack (Upgrade)
  'il010': "<b>Interruption</b> <i>(contre)</i> : quand une menace serait placée sur un plan, défaussez Hack → retirez ce montant de ce plan à la place. De plus, vous pouvez défausser 5 cartes de votre deck pour retirer le même montant d'un plan différent.",
  // iron_lad — Ion Amplifiers (Upgrade) x2
  'il011': "Utilisations <i>(X compteurs d'ion, X étant égal au nombre de cartes [[TECH]] que vous contrôlez.)</i>\n<b>Ressource de héros</b> : inclinez Ion Amplifiers et retirez 1 compteur d'ion → générez une ressource [wild].",
  'il012': "Utilisations <i>(X compteurs d'ion, X étant égal au nombre de cartes [[TECH]] que vous contrôlez.)</i>\n<b>Ressource de héros</b> : inclinez Ion Amplifiers et retirez 1 compteur d'ion → générez une ressource [wild].",
  // iron_lad — Iron Lad's Boots (Upgrade)
  'il013': "Iron Lad gagne le trait [[AERIAL]].\n<b>Réponse de héros</b> : après avoir joué un événement, inclinez Iron Lad's Boots → retournez la carte du dessous de votre défausse dans votre main.",
  // iron_lad — Iron Lad's Helmet (Upgrade)
  'il014': "<b>Réponse de héros</b> : après qu'Iron Lad a utilisé un pouvoir de base, inclinez Iron Lad's Helmet → retournez la carte du dessous de votre défausse dans votre main.",
  // iron_lad — Iron Lad's Suit (Upgrade)
  'il015': "Vous gagnez +3 points de vie.\n<b>Action de héros</b> : inclinez Iron Lad's Suit → redressez Iron Lad.",
  // iron_lad — Neurokinetic Interface (Upgrade)
  'il016': "<b>Réponse de héros</b> : après avoir révélé une carte de rencontre, inclinez Neurokinetic Interface → si cette carte était :\n• Une traîtrise ou un sbire, infligez 2 dégâts à un ennemi.\n• Un plan secondaire ou une pièce jointe, retirez 2 menaces d'un plan.",
  // iron_lad — Shadow of the Future (Obligation)
  'il017': "<b><i>Donnez-la au joueur Nathaniel Richards.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Retirez les 3 cartes du dessus de votre deck de la partie → retirez Shadow of the Future de la partie.\n• Défaussez 1 carte [[TECH]] que vous contrôlez. Défaussez 3 cartes de votre deck. Défaussez cette obligation.",
  // iron_lad — Early Start (SideScheme, nemesis)
  'il018': "<b>Une fois révélée</b> : inclinez chaque amélioration Iron Lad en jeu.\nTant que ce plan est en jeu, les améliorations Iron Lad ne peuvent pas être redressées.",
  // iron_lad — Kang the Conqueror (Minion, nemesis)
  'il019': "Robustesse. Vilenie.\n<b>Une fois révélée</b> : placez l'amélioration Iron Lad au coût le plus élevé en jeu sous Kang the Conqueror.\n<b>Une fois vaincu</b> : renvoyez l'amélioration placée ici dans la main de son propriétaire. Mettez Kang the Conqueror de côté.",
  // iron_lad — Taking Responsability (Obligation, nemesis)
  'il020': "<b>Réponse forcée</b> : après que vous avez attaqué ou contré, défaussez la carte du dessus de votre deck.\n<b>Action</b> : retirez la carte du dessus de votre deck de la partie → défaussez cette obligation.",
  // iron_lad — Pay the Price (Treachery, nemesis) x2
  'il021': "<b>Une fois révélée</b> : défaussez 8 cartes de votre deck. Si moins de 8 cartes ont été défaussées de cette façon, cette carte gagne renfort.",
  'il022': "<b>Une fois révélée</b> : défaussez 8 cartes de votre deck. Si moins de 8 cartes ont été défaussées de cette façon, cette carte gagne renfort.",
  // iron_lad — Sudden Plan Change (Event, Basic, Team-Up)
  'il023': "En Équipe (Stature et Iron Lad). 1 max par deck.\n<b>Action de héros</b> : changez vers l'autre forme. Vous gagnez +1 taille de main jusqu'à la fin de la phase.",

  // superior_iron_man — Superior Iron Man (Hero)
  'si001a': "<i>« Quoi les autres ? »</i> — <b>Ressource</b> : infligez 1 dégât à un personnage ami → générez une ressource [wild]. <i>(Limite d'une fois par phase.)</i>",
  // superior_iron_man — Tony Stark (AlterEgo)
  'si001b': "<b>Mise en place</b> : trouvez l'Armure Endo-Sym et mettez-la en jeu.\n<i>O.P.A.</i> — <b>Action</b> <i>(contre)</i> : dépensez X ressources [mental] (minimum 1) → retirez 1 + X menace d'une manigance. <i>(Limite d'une fois par phase.)</i>",
  // superior_iron_man — Endo-Sym Armor (Upgrade)
  'si002': "Permanent. Mise en place.\n<b>Action de héros</b> <i>(attaque)</i> : dépensez X ressources [physical] (minimum 1) → infligez 2 + X dégâts à un ennemi. <i>(Limite d'une fois par phase.)</i>\n<b>Interruption de héros</b> <i>(défense)</i> : quand vous êtes censé subir n'importe quelle quantité de dégâts, dépensez X ressources [energy] (minimum 1) → prévenez 1 + X de ces dégâts. <i>(Limite d'une fois par phase.)</i>",
  // superior_iron_man — Teen Abomination (Jammy) (Ally)
  'si003': "Teen Abomination entre en jeu avec 4 jetons Rage sur lui.\n<b>Réponse forcée</b> : après que Teen Abomination a fait une attaque de base, retirez-lui 1 jeton Rage.\n[star] Teen Abomination gagne +1 ATQ pour chaque jeton Rage sur lui.",
  // superior_iron_man — Daniel Hall (Support)
  'si004': "Utilisation (3 jetons Flouze).\n<b>Ressource</b> : retirez 1 jeton Flouze de Daniel Hall et inclinez-le → générez une ressource [wild].\n<b>Interruption forcée</b> : quand vous êtes censé retirer le dernier jeton Flouze de Daniel Hall, choisissez une carte de votre main et défaussez-la.",
  // superior_iron_man — Claire Mooney (Support)
  'si005': "Utilisation (3 jetons Flouze).\n<b>Ressource</b> : retirez 1 jeton Flouze de Claire Mooney et inclinez-la → générez une ressource [wild].\n<b>Interruption forcée</b> : quand vous êtes censé retirer le dernier jeton Flouze de Claire Mooney, choisissez une carte de votre main et défaussez-la.",
  // superior_iron_man — Mason Thomas (Support)
  'si006': "Utilisation (3 jetons Flouze).\n<b>Ressource</b> : retirez 1 jeton Flouze de Mason Thomas et inclinez-le → générez une ressource [wild].\n<b>Interruption forcée</b> : quand vous êtes censé retirer le dernier jeton Flouze de Mason Thomas, choisissez une carte de votre main et défaussez-la.",
  // superior_iron_man — Pepper Potts (Support)
  'si007': "<b>Action</b> : inclinez Pepper Potts → retirez 1 menace d'une manigance en ignorant son icône de crise.",
  // superior_iron_man — Stark Island (Support)
  'si008': "<b>Action d'alter ego</b> : inclinez Stark Island → recherchez dans votre deck et dans votre pile de défausse un soutien [[Individual]] et mettez-le en jeu sous votre contrôle en payant son coût. Mélangez votre deck.",
  // superior_iron_man — Iron Sight (Support)
  'si009': "Utilisation (2 [per_hero] jetons Observation).\n<b>Interruption</b> : quand une carte de boost est retournée face visible lors d'une activation, retirez 1 jeton Observation d'Iron Sight et inclinez-la → annulez les icônes de boost de cette carte.",
  // superior_iron_man — Endo-Sym Spare (Upgrade)
  'si010': "<b>Action d'alter ego</b> : inclinez Réserve Endo-Sym → recherchez dans votre pile de défausse une carte ressource Matière Endo-Sym et mélangez-la dans votre deck.",
  // superior_iron_man — Spectacular Blast (Event)
  'si011': "<b>Action de héros</b> <i>(attaque/contre)</i> : infligez 3 dégâts à un ennemi. Retirez 2 menaces d'une manigance.",
  // superior_iron_man — Spectacular Save (Event)
  'si012': "<b>Interruption de héros</b> <i>(contre/défense)</i> : quand un personnage ami est censé subir n'importe quelle quantité de dégâts, prévenez 3 de ces dégâts. Retirez 1 menace d'une manigance.",
  // superior_iron_man — Endo-Sym Matter (Resource)
  'si013': "Doublez le nombre de ressources générées par cette carte lorsque vous payez pour les cartes spécifiques à votre identité (y compris pour le coût des capacités sur ces cartes).",
  // superior_iron_man — Alone (Obligation)
  'si014': "<b><i>Donnez-la au joueur Tony Stark.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Tony Stark → retirez Alone de la partie.\n• Dépensez 3 ressources de n'importe quel type. Si vous ne le pouvez pas, cette carte gagne renfort. Défaussez cette obligation.",
  // superior_iron_man — Massive Attack (SideScheme)
  'si015': "Entrave 2.\n<b>Une fois révélée</b> : infligez 1 dégât au joueur Tony Stark.\n[star] <b>Boost</b> : mettez Massive Attack en jeu.",
  // superior_iron_man — Tony Stark A.I. (Minion)
  'si016': "Armure 2. Garde. Patrouille.\n<b>Une fois révélée</b> : infligez 1 dégât au joueur Tony Stark.\n[star] Infligez 1 dégât au joueur Tony Stark.",
  // superior_iron_man — Get My Body Back (Treachery)
  'si017': "<b>Une fois révélée</b> : infligez 1 dégât au joueur Tony Stark, puis infligez-lui 1 dégât supplémentaire.",
  // scarlet_spider — Scarlet Spider (Hero)
  'ss001a': "<i>Interrogatoire extrême</i> — <b>Réponse</b> : après que vous avez infligé un excès de dégâts à un sbire, remélangez-le dans le deck de rencontre. Puis, retirez d'un plan une menace égale au montant de dégâts en excès infligés. <i>(Maximum 3 menaces par sbire.)</i>",
  // scarlet_spider — Kaine Parker (AlterEgo)
  'ss001b': "<i>Lien arachnéen</i> — <b>Action</b> : défaussez 1 carte de votre main → cherchez dans votre défausse 1 exemplaire de Spider-pathy et ajoutez-le à votre main. <i>(Limite d'une fois par round.)</i>",
  // scarlet_spider — Grim Resolve (Event) x2
  'ss002': "<b>Action</b> : choisissez un pouvoir de base, vous gagnez +1 à ce pouvoir jusqu'à la fin du round pour chaque ressource différente dépensée sur cette carte. Puis, redressez votre identité.",
  'ss003': "<b>Action</b> : choisissez un pouvoir de base, vous gagnez +1 à ce pouvoir jusqu'à la fin du round pour chaque ressource différente dépensée sur cette carte. Puis, redressez votre identité.",
  // scarlet_spider — Precise Force (Event) x3
  'ss004': "<b>Action de héros</b> <i>(attaque)</i> : infligez jusqu'à 3 dégâts à un ennemi.",
  'ss005': "<b>Action de héros</b> <i>(attaque)</i> : infligez jusqu'à 3 dégâts à un ennemi.",
  'ss006': "<b>Action de héros</b> <i>(attaque)</i> : infligez jusqu'à 3 dégâts à un ennemi.",
  // scarlet_spider — Spider-pathy (Event) x2
  'ss007': "<b>Action</b> : cherchez dans le deck de rencontre le sbire le plus proche du dessus et mettez-le en jeu, engagé avec vous. Piochez 1 carte.",
  'ss008': "<b>Action</b> : cherchez dans le deck de rencontre le sbire le plus proche du dessus et mettez-le en jeu, engagé avec vous. Piochez 1 carte.",
  // scarlet_spider — Unrestrained (Event) x2
  'ss009': "<b>Action de héros</b> <i>(attaque)</i> : infligez 7 dégâts à un ennemi. Si le vilain subit un déferlement de dégâts de cette attaque, sonnez et désorientez le vilain.",
  'ss010': "<b>Action de héros</b> <i>(attaque)</i> : infligez 7 dégâts à un ennemi. Si le vilain subit un déferlement de dégâts de cette attaque, sonnez et désorientez le vilain.",
  // scarlet_spider — Four Seasons' Room (Support)
  'ss011': "<b>Action d'alter ego</b> : inclinez Four Seasons' Room → piochez 1 carte <i>(2 à la place si vous donnez une carte boost face cachée au vilain)</i>.",
  // scarlet_spider — Mark of Kaine (Upgrade) x3
  'ss012': "Attachez-la à un sbire. Les attaques contre ce sbire gagnent déferlement.\n<b>Interruption de héros</b> : quand Scarlet Spider inflige un excès de dégâts à ce sbire, augmentez ce montant de 2.",
  'ss013': "Attachez-la à un sbire. Les attaques contre ce sbire gagnent déferlement.\n<b>Interruption de héros</b> : quand Scarlet Spider inflige un excès de dégâts à ce sbire, augmentez ce montant de 2.",
  'ss014': "Attachez-la à un sbire. Les attaques contre ce sbire gagnent déferlement.\n<b>Interruption de héros</b> : quand Scarlet Spider inflige un excès de dégâts à ce sbire, augmentez ce montant de 2.",
  // scarlet_spider — Spider Stealth Suit (Upgrade)
  'ss015': "Vous gagnez +1 point de vie.\n<b>Interruption de héros</b> : quand vous jouez un événement [[ATTAQUE]] ou [[CONTRE]], augmentez de 1 le dégât infligé ou la menace retirée par cet événement.",
  // scarlet_spider — Stings of Kaine (Upgrade)
  'ss016': "Scarlet Spider gagne +1 ATQ.\n<b>Interruption de héros</b> : quand vous attaquez, inclinez Stings of Kaine → cette attaque gagne perçant et déferlement.",
  // scarlet_spider — Murderer's Guilt (Obligation)
  'ss017': "<b><i>Donnez-la au joueur Kaine Parker.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Kaine Parker et subissez 2 dégâts → retirez Murderer's Guilt de la partie.\n• Subissez 1 dégât par événement dans votre main. Si moins de 3 dégâts ont été subis de cette façon, cette carte gagne renfort. Défaussez cette obligation.",
  // scarlet_spider — Assassins Guild (SideScheme, nemesis)
  'ss018': "<i>Kaine avait autrefois accepté des contrats d'assassinat sur le territoire de la Guilde des Assassins. Elle veut sa part !</i>\nChaque ennemi [[ASSASSIN]] gagne +1 ATQ.",
  // scarlet_spider — Bella Donna (Minion, nemesis)
  'ss019': "Machination. <i>(Après que ce sbire s'est engagé avec votre identité, il manigance.)</i>\n<b>Interruption forcée</b> : quand Bella Donna est mise K.O., cherchez dans le deck de rencontre un autre sbire [[ASSASSIN]] et révélez-le.\n<i>(Sbire némésis de Scarlet Spider.)</i>",
  // scarlet_spider — Harvester (Minion, nemesis)
  'ss020': "Coup rapide.\nLes attaques de Harvester gagnent perçant.\n<b>Réponse forcée</b> : après que Harvester a attaqué et blessé un personnage, infligez 1 dégât à ce personnage.",
  // scarlet_spider — Undead Hand Ninja (Minion, nemesis)
  'ss021': "Incitation 1.\n<b>Interruption forcée</b> : quand ce sbire serait mis K.O., remélangez-le dans le deck de rencontre à la place.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // scarlet_spider — Forced Contract (Treachery, nemesis)
  'ss022': "Renfort.\n<b>Une fois révélée</b> : l'allié ayant l'ATQ la plus élevée subit des dégâts égaux à l'ATQ de Scarlet Spider. S'il n'y a aucun allié en jeu, vous subissez 2 dégâts.\n<hr />\n[star] <b>Boost</b> : chaque personnage ami subit 1 dégât.",

  // howard_the_duck — Howard the Duck (Hero)
  'hd001a': "<i>Détective privé</i> — <b>Interruption</b> : quand une menace devrait être placée sur une manigance, empêchez 1 de cette menace. <i>(Limite d'une fois par round.)</i>\n<b>Réponse</b> : après qu'une manigance annexe est entrée en jeu, redressez Howard the Duck. <i>(Limite d'une fois par round.)</i>",
  // howard_the_duck — Howard Duckson (AlterEgo)
  'hd001b': "<i>Raisonnement can-artésien</i> — <b>Action</b> : regardez les 3 cartes du dessus du deck de rencontre. Placez-en 1 sous le deck et remettez les autres dans l'ordre de votre choix. <i>(Limite d'une fois par round.)</i>",
  // howard_the_duck — Man-Thing (Ally)
  'hd002': "Ténacité.\nRéduisez de 1 le coût pour jouer Man-Thing pour chaque manigance annexe Howard the Duck dans la zone de victoire.",
  // howard_the_duck — Mallard Magic (Event) x2
  'hd003': "<b>Action de héros</b> : choisissez :\n• Sonnez un ennemi et infligez-lui 5 dégâts.\n• Désorientez un ennemi et retirez 4 menaces d'une manigance.",
  'hd004': "<b>Action de héros</b> : choisissez :\n• Sonnez un ennemi et infligez-lui 5 dégâts.\n• Désorientez un ennemi et retirez 4 menaces d'une manigance.",
  // howard_the_duck — Quack Attack (Event) x2
  'hd005': "<b>Interruption de héros</b> <i>(attaque/défense)</i> : quand vous devriez subir des dégâts, quel qu'en soit le montant, empêchez 2 de ces dégâts. Infligez 1 dégât à un ennemi pour chaque manigance annexe dans la zone de victoire.",
  'hd006': "<b>Interruption de héros</b> <i>(attaque/défense)</i> : quand vous devriez subir des dégâts, quel qu'en soit le montant, empêchez 2 de ces dégâts. Infligez 1 dégât à un ennemi pour chaque manigance annexe dans la zone de victoire.",
  // howard_the_duck — Fowl Play (Event) x2
  'hd007': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Si vous déjouez ainsi une manigance annexe, vous pouvez redresser votre héros ou retirer 1 menace d'une manigance pour chaque manigance annexe dans la zone de victoire.",
  'hd008': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Si vous déjouez ainsi une manigance annexe, vous pouvez redresser votre héros ou retirer 1 menace d'une manigance pour chaque manigance annexe dans la zone de victoire.",
  // howard_the_duck — Quack and Burn (Event)
  'hd009': "<b>Action de héros</b> <i>(attaque/contre)</i> : cherchez Man-Thing et ajoutez-le à votre main. Infligez à un ennemi des dégâts égaux à l'ATQ de Man-Thing et retirez d'une manigance une menace égale au CTR de Howard the Duck.",
  // howard_the_duck — Trapped (PlayerSideScheme)
  'hd010': "Victoire 0.\nTant que Trapped est dans la zone de victoire, Howard the Duck gagne +1 ATQ.\n<b>Une fois déjouée</b> : chaque joueur peut chercher un allié dans son deck et sa pile de défausse, et l'ajouter à sa main. Le joueur qui a déjoué cette manigance peut mettre cet allié en jeu.",
  // howard_the_duck — In a World (PlayerSideScheme)
  'hd011': "Victoire 0.\nTant que In a World est dans la zone de victoire, Howard the Duck gagne +1 DEF.\n<b>Une fois déjouée</b> : donnez une carte d'état Tenace à chaque joueur. Le joueur qui a déjoué cette manigance peut soigner 2 dégâts de son identité.",
  // howard_the_duck — He Never Made (PlayerSideScheme)
  'hd012': "Victoire 0.\nTant que He Never Made est dans la zone de victoire, Howard the Duck gagne +1 CTR.\n<b>Une fois déjouée</b> : chaque joueur peut mélanger jusqu'à 3 cartes de sa pile de défausse dans son deck. Le joueur qui a déjoué cette manigance peut à la place ajouter 1 de ces cartes à sa main.",
  // howard_the_duck — Beverly Switzler (Support)
  'hd013': "<b>Action d'alter ego</b> : inclinez Beverly Switzler → remettez dans votre main la carte Howard the Duck la plus basse de votre pile de défausse. Soignez 1 dégât de votre identité.",
  // howard_the_duck — Ducktective Agency (Support)
  'hd014': "<b>Ressource</b> : inclinez Ducktective Agency → générez 1 ressource [mental] pour un événement.\n<b>Réponse de héros</b> : après que vous avez retiré la dernière menace d'une manigance, redressez Ducktective Agency.",
  // howard_the_duck — Duckpool Suit (Upgrade)
  'hd015': "Vous gagnez +3 points de vie.\nHoward the Duck gagne +1 ATQ.\n<b>Réponse de héros</b> : après que vous avez déjoué une manigance annexe, inclinez Duckpool Suit → infligez 1 dégât à un ennemi.",
  // howard_the_duck — Iron Suit (Upgrade)
  'hd016': "<b>Action</b> : inclinez Iron Suit → déplacez 1 menace d'une manigance vers cette carte.\n<b>Action de héros</b> : inclinez Iron Suit et retirez X menaces de cette carte → infligez X dégâts à un sbire ou retirez X menaces d'une manigance.",
  // howard_the_duck — Nexus of all Realities (Upgrade)
  'hd017': "Mise en place. Permanent.\n<b>Interruption</b> : quand un personnage entre en jeu, choisissez la zone de jeu dans laquelle il est joué.\n<b>Interruption</b> : quand un allié que vous contrôlez quitte le jeu, cherchez une carte événement dans votre deck et ajoutez-la à votre main.",
  // howard_the_duck — Energy / Genius / Strength (Resource, re-skins de 01088/01089/01090)
  'hd018': "1 max par deck.",
  'hd019': "1 max par deck.",
  'hd020': "1 max par deck.",
  // howard_the_duck — Waddle it Be? (Obligation)
  'hd021': "<b><i>Donnez-la au joueur Howard Duckson.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Howard Duckson → retirez Waddle it Be? de la partie.\n• Retirez de la zone de victoire toutes les manigances annexes Howard the Duck et mélangez-les dans votre deck. Si aucune manigance n'a été retirée de cette façon, cette carte gagne renfort. Défaussez cette obligation.",
  // howard_the_duck — Duck and Cover! (SideScheme, nemesis)
  'hd022': "<i>Quack-tastrophe ! Howard the Duck s'est encore mis dans un pétrin qui le dépasse. C'est aux héros de le sauver d'un groupe de chasseurs de primes interdimensionnels.</i>\n<b>Une fois révélée</b> : chaque joueur doit défausser de sa main les cartes ayant une ressource [mental] imprimée. Placez 1 menace supplémentaire ici pour chaque carte défaussée de cette façon.",
  // howard_the_duck — Collector (Minion, nemesis)
  'hd023': "Vilenie. <i>(Quand ce sbire s'active, donnez-lui une carte boost.)</i>\n<b>Une fois révélé</b> : défaussez un allié ou un soutien que vous contrôlez. Si vous ne pouvez pas, mettez en jeu la manigance la plus proche du dessus du deck de rencontre.\n<i>(Sbire némésis de Howard the Duck.)</i>",
  // howard_the_duck — Hellcow (Minion, nemesis alternatif)
  'hd024': "Coup Rapide.\n<b>Interruption forcée</b> : quand la phase du méchant commence, soignez 1 dégât de Hellcow.\n<b>Interruption</b> : quand Hellcow devrait être mise K.O., remélangez-la dans le deck de rencontre à la place.",
  // howard_the_duck — Duck, Duck, Doom! (SideScheme, nemesis)
  'hd025': "<i>Doctor Bong a tendu un piège pour capturer Howard the Duck.</i>\n<b>Une fois révélée</b> : placez un allié que vous contrôlez sous cette carte. Si vous ne pouvez pas, désorientez votre identité.\n<b>Une fois déjouée</b> : rendez l'allié placé sous cette carte à la main de son propriétaire.",
  // howard_the_duck — A Fowl Plot (SideScheme, nemesis)
  'hd026': "<i>Le Collectionneur compte ajouter Howard the Duck à sa collection d'objets rares et uniques.</i>\n<b>Une fois révélée</b> : défaussez une amélioration que vous contrôlez. Si aucune carte n'a été défaussée de cette façon, placez 1 menace sur la manigance principale et subissez 1 dégât.\n<i>(Manigance annexe némésis de Howard the Duck.)</i>",
  // howard_the_duck — Duck Hunt (Treachery, nemesis)
  'hd027': "<b>Une fois révélée (alter ego)</b> : le méchant manigance. S'il y a des manigances annexes en jeu, répartissez et placez plutôt parmi elles la menace de cette activation.\n<b>Une fois révélée (héros)</b> : donnez une carte d'état Tenace au méchant. Si vous ne pouvez pas, soignez plutôt 3 dégâts de celui-ci.",
  // wiccan — Wiccan (Hero)
  'wc001a': "<i>Clairvoyance</i> — durant la phase des joueurs, jouez avec la carte du dessus du deck de rencontre face visible.\n<b>Interruption forcée</b> : au début de la phase du méchant, défaussez la carte du dessus du deck de rencontre.",
  // wiccan — Billy Kaplan (AlterEgo)
  'wc001b': "<i>Clairvoyance</i> — durant la phase des joueurs, jouez avec la carte du dessus du deck de rencontre face visible.\n<b>Action</b> : regardez les 2 cartes du dessus du deck de rencontre, vous pouvez en défausser une. <i>(Limite d'une fois par round.)</i>",
  // wiccan — Hulkling (Ally)
  'wc002': "<b>Interruption</b> : quand Hulkling attaque, il gagne +1 ATQ pour chaque icône de boost sur la carte du dessus du deck de rencontre. Puis, défaussez cette carte.",
  // wiccan — Impenetrable Barrier (Event, x2)
  'wc003': "<b>Action de héros</b> : donnez une carte d'état Tenace à votre héros. Donnez une carte d'état Tenace à un maximum de X personnages amis, où X est égal au nombre d'icônes de boost sur la carte du dessus du deck de rencontre.",
  'wc004': "<b>Action de héros</b> : donnez une carte d'état Tenace à votre héros. Donnez une carte d'état Tenace à un maximum de X personnages amis, où X est égal au nombre d'icônes de boost sur la carte du dessus du deck de rencontre.",
  // wiccan — Magic Bolt (Event, x3)
  'wc005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Puis, si la carte du dessus du deck de rencontre a :\n• 0 ou 1 icône de boost → piochez 1 carte.\n• 2 icônes de boost ou plus → infligez 3 dégâts à un ennemi. Cette attaque gagne à distance.",
  'wc006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Puis, si la carte du dessus du deck de rencontre a :\n• 0 ou 1 icône de boost → piochez 1 carte.\n• 2 icônes de boost ou plus → infligez 3 dégâts à un ennemi. Cette attaque gagne à distance.",
  'wc007': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Puis, si la carte du dessus du deck de rencontre a :\n• 0 ou 1 icône de boost → piochez 1 carte.\n• 2 icônes de boost ou plus → infligez 3 dégâts à un ennemi. Cette attaque gagne à distance.",
  // wiccan — Magic Manipulation (Event)
  'wc008': "<b>Action d'alter ego</b> : remélangez 1 carte de votre pile de défausse dans votre deck pour chaque icône de boost sur la carte du dessus du deck de rencontre. Puis, piochez 1 carte.",
  // wiccan — Magic Portal (Event, x2)
  'wc009': "<b>Action de héros</b> <i>(contre)</i> : retirez 5 menaces d'une manigance. Puis, si la carte du dessus du deck de rencontre a :\n• 0 ou 1 icône de boost → piochez 1 carte.\n• 2 icônes de boost ou plus → retirez 2 menaces de chaque manigance en jeu.",
  'wc010': "<b>Action de héros</b> <i>(contre)</i> : retirez 5 menaces d'une manigance. Puis, si la carte du dessus du deck de rencontre a :\n• 0 ou 1 icône de boost → piochez 1 carte.\n• 2 icônes de boost ou plus → retirez 2 menaces de chaque manigance en jeu.",
  // wiccan — Teleport (Event, x2)
  'wc011': "<b>Action</b> : choisissez un joueur → redressez l'identité de ce joueur. Ce joueur peut changer de forme. Si la carte du dessus du deck de rencontre a 2 icônes de boost ou plus, ce joueur gagne +1 à un pouvoir de base de son choix jusqu'à la fin du round.",
  'wc012': "<b>Action</b> : choisissez un joueur → redressez l'identité de ce joueur. Ce joueur peut changer de forme. Si la carte du dessus du deck de rencontre a 2 icônes de boost ou plus, ce joueur gagne +1 à un pouvoir de base de son choix jusqu'à la fin du round.",
  // wiccan — Transmutation (Event)
  'wc013': "<b>Action</b> : cherchez une carte dans le deck de rencontre. Puis, mélangez le deck de rencontre et placez cette carte sur son dessus. Piochez 1 carte.",
  // wiccan — Warping Reality (Event)
  'wc014': "<b>Action</b> : réduisez de 1+X le coût de la prochaine carte jouée durant ce round, où X est le nombre d'icônes de boost sur la carte du dessus du deck de rencontre.",
  // wiccan — Mother's Protection (Support)
  'wc015': "<b>Interruption</b> : quand votre identité devrait subir des dégâts, remélangez Mother's Protection dans votre deck → empêchez 3 de ces dégâts.",
  // wiccan — Wiccan's Cloak (Upgrade)
  'wc016': "<b>Réponse</b> : après avoir joué un événement [[SPELL]] qui compte le nombre d'icônes de boost sur une carte de rencontre, inclinez Wiccan's Cloak et défaussez la carte du dessus du deck de rencontre → résolvez à nouveau cet événement.",
  // wiccan — Royal Couple (Event, Basic)
  'wc017': "En Équipe (Hulkling et Wiccan). 1 max par deck.\n<b>Action de héros</b> : choisissez une carte dans la pile de défausse de rencontre et placez-la sur le dessus du deck de rencontre. Redressez votre héros.",
  // wiccan — Avoiding the Demiurge (Obligation)
  'wc018': "<b><i>Donnez-la au joueur Billy Kaplan.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez votre identité → retirez Avoiding the Demiurge de la partie.\n• Les icônes de boost ne peuvent plus être comptées pour les effets des cartes Wiccan jusqu'à la fin de la prochaine phase des joueurs. Défaussez cette obligation.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // wiccan — New Vessel (SideScheme, nemesis)
  'wc019a': "<i>Moridun a infecté Wiccan et se trouve désormais dans son esprit. L'emprise du sorcier maléfique sur Wiccan ne cesse de grandir.</i>\nSeul le joueur Billy Kaplan peut retirer de la menace de cette manigance.\n<b>Une fois déjouée</b> : retirez 2 menaces de la manigance principale. Puis, mettez de côté New Vessel et Moridun.\n<b>Une fois accomplie</b> : mettez Moridun de côté et retournez cette carte. <i>(8 menaces.)</i>",
  // wiccan — The Demiurge (Environment, verso de wc019a)
  'wc019b': "Permanent.\n<b>Réponse forcée</b> : après qu'un deck de joueur se retrouve à court de cartes, placez 1 menace sur la manigance principale.",
  // wiccan — Moridun (Attachment, nemesis)
  'wc020': "Attachez-la à l'identité du joueur Billy Kaplan.\n<b>Une fois révélée</b> : révélez votre manigance annexe New Vessel mise de côté.\n<b>Interruption forcée</b> : quand Wiccan devrait infliger des dégâts à un ennemi ou retirer de la menace d'une manigance, placez 1 menace sur la manigance annexe New Vessel.\n<i>(Sbire némésis de Wiccan.)</i>",
  // wiccan — Inescapable Horror (Treachery, nemesis, x2)
  'wc021': "<b>Une fois révélée</b> : infligez 1 dégât à chaque personnage ami. Si Moridun est en jeu, vous êtes sonné.\n<hr />\n[star] <b>Boost</b> : infligez 1 dégât à chaque personnage ami que vous contrôlez.",
  'wc022': "<b>Une fois révélée</b> : infligez 1 dégât à chaque personnage ami. Si Moridun est en jeu, vous êtes sonné.\n<hr />\n[star] <b>Boost</b> : infligez 1 dégât à chaque personnage ami que vous contrôlez.",
  // wiccan — Master Magus Returns (Treachery, nemesis)
  'wc023': "<b>Une fois révélée</b> : si l'environnement The Demiurge n'est pas en jeu, révélez l'attachement Moridun mis de côté, puis retirez Master Magus Returns de la partie. Si Moridun n'a pas été révélé de cette façon, vous êtes désorienté.\n<hr />\n[star] <b>Boost</b> : vous êtes désorienté.",
  // speed — Speed (Hero) [set 141, CptScorp]
  'sd001a': "<i>Hyperkinetic Fuel</i> — <b>Interruption</b> : quand vous payez un événement uniquement avec des ressources [energy], placez un compteur explosif sur un ennemi ou une manigance. <i>(Voir l'encart.)</i>",
  // speed — Thomas Shepherd (AlterEgo)
  'sd001b': "<i>Accelerated Perception</i> — <b>Action</b> : remélangez 1 événement de votre pile de défausse dans votre deck. Puis, piochez 1 carte. <i>(Limite d'une fois par round.)</i>",
  // speed — Quicksilver (Ally)
  'sd002': "<b>Interruption</b> : quand Quicksilver attaque ou contre un ennemi ou une manigance portant un compteur explosif, il ne subit aucun dégât consécutif pour cette utilisation.",
  // speed — Blasting Velocity (Event, x2)
  'sd003': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Effectuez une attaque de base contre un ennemi portant un compteur explosif, sans vous incliner.",
  'sd004': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Effectuez une attaque de base contre un ennemi portant un compteur explosif, sans vous incliner.",
  // speed — "I'm Out" (Event)
  'sd005': "<b>Interruption de héros</b> : quand vous révélez une carte de rencontre, annulez les effets de cette carte et défaussez-la. Si vous deviez résoudre la capacité <i>\"Hyperkinetic Fuel\"</i> de Speed en jouant cet événement, remélangez plutôt 1 événement de votre pile de défausse dans votre deck et piochez 1 carte.",
  // speed — Kinetic Flurry (Event, x2)
  'sd006': "Vous ne pouvez dépenser que des ressources [energy] pour payer cette carte. Choisissez un ennemi et effectuez X fois l'attaque suivante :\n<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à cet ennemi (3 dégâts à la place si cet ennemi porte un compteur explosif).",
  'sd007': "Vous ne pouvez dépenser que des ressources [energy] pour payer cette carte. Choisissez un ennemi et effectuez X fois l'attaque suivante :\n<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à cet ennemi (3 dégâts à la place si cet ennemi porte un compteur explosif).",
  // speed — Swift Strikes (Event, x3)
  'sd008': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Effectuez un contre de base contre une manigance portant un compteur explosif, sans vous incliner.",
  'sd009': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Effectuez un contre de base contre une manigance portant un compteur explosif, sans vous incliner.",
  'sd010': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Effectuez un contre de base contre une manigance portant un compteur explosif, sans vous incliner.",
  // speed — Top Speed (Resource, x2)
  'sd011': "<b>Interruption</b> : quand vous dépensez cette carte, vous pouvez générer une ressource [energy] supplémentaire ([energy][energy] à la place s'il y a un compteur explosif en jeu). Si vous le faites, vous ne pouvez plus jouer de cartes pour le reste du tour.",
  'sd012': "<b>Interruption</b> : quand vous dépensez cette carte, vous pouvez générer une ressource [energy] supplémentaire ([energy][energy] à la place s'il y a un compteur explosif en jeu). Si vous le faites, vous ne pouvez plus jouer de cartes pour le reste du tour.",
  // speed — Mother's Protection (Support)
  'sd013': "<b>Interruption</b> : quand votre identité devrait subir des dégâts, remélangez Mother's Protection dans votre deck → empêchez 3 de ces dégâts.",
  // speed — Explosive Touch (Upgrade)
  'sd014': "<b>Réponse de héros</b> : après avoir attaqué ou contré, avec un pouvoir de base, un ennemi ou une manigance portant un compteur explosif, inclinez Explosive Touch → redressez Speed.",
  // speed — Never Ending Spark (Upgrade)
  'sd015': "<b>Réponse de héros</b> : après qu'un compteur explosif est placé sur un ennemi ou une manigance, redressez cette carte.\n<b>Ressource</b> : inclinez Never Ending Spark → générez une ressource [energy].",
  // speed — Quick Adaptation (Upgrade)
  'sd016': "<b>Interruption de héros</b> : quand vous attaquez ou contrez, avec un pouvoir de base, un ennemi ou une manigance portant un compteur explosif, vous gagnez +1 ATQ et +1 CTR pour cette utilisation.",
  // speed — No Outrunning This (Obligation)
  'sd017': "<b><i>Donnez-la au joueur Thomas Shepherd.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Thomas Shepherd → retirez No Outrunning This de la partie.\n• Vous ne pouvez pas résoudre l'<b>Interruption</b> <i>Hyperkinetic Fuel</i> de Speed jusqu'à la fin du prochain round. Défaussez cette obligation.",
  // speed — The Real Question (SideScheme, nemesis)
  'sd018': "<i>\"Les super-héros, c'est bien ?\"</i>\n<b>Une fois révélée</b> : défaussez des cartes du dessus du deck de rencontre jusqu'à ce qu'un attachement soit défaussé. Révélez cet attachement.\nTant que cette manigance est en jeu, les attachements gagnent <b><i>Permanent</i></b>.",
  // speed — Coat of Arms (Minion, nemesis)
  'sd019': "Coup Rapide.\n[star] Quand Coat of Arms attaque, si elle inflige des dégâts, infligez 1 dégât supplémentaire à chaque personnage que vous contrôlez.\n<i>(Sbire némésis de Speed.)</i>",
  // speed — Inspirational Art (Attachment, nemesis)
  'sd020': "Attachez-la au vilain.\n<b>Interruption forcée</b> : quand une carte de boost est retournée face visible durant une activation du vilain, chaque carte de boost gagne +1 icône de boost ([boost]).\n<b>Action de héros</b> : dépensez des ressources [energy][physical] → défaussez cette carte.",
  // speed — Magic Chains (Attachment, nemesis)
  'sd021': "Attachez-la à Coat of Arms, si possible. Sinon, attachez-la au vilain.\n<b>Réponse forcée</b> : après que l'ennemi attaché attaque, si l'attaque inflige des dégâts, sonnez votre héros → défaussez cette carte.",
  // speed — Conflicted Feelings (Obligation, nemesis)
  'sd022': "<b><i>Donnez-la au joueur Thomas Shepherd.</i></b>\nTant que cette obligation est en jeu, Coat of Arms ne peut pas subir de dégâts.\n<b>Action d'alter ego</b> : dépensez des ressources [energy][mental] → défaussez cette carte.",
  // patriot — Patriot (Hero)
  'pt001a': "<i>Will to Protect</i> — <b>Interruption</b> : quand un allié que vous contrôlez devrait subir des dégâts consécutifs, déplacez ces dégâts sur Patriot. <i>(Limite d'une fois par round.)</i>",
  // patriot — Elijah Bradley (AlterEgo)
  'pt001b': "<i>Leader</i> — Pendant la construction du deck, vous pouvez inclure des alliés [[YOUNG AVENGER]] de n'importe quel aspect.\n<b>Action</b> : inclinez Elijah Bradley → cherchez le Patriot's Shield dans votre deck et votre pile de défausse, et ajoutez-le à votre main. Mélangez votre deck.",
  // patriot — Hawkingbird (Ally)
  'pt002': "Les alliés que vous contrôlez gagnent +1 point de vie.\n<b>Réponse</b> : après l'entrée en jeu de Hawkingbird, vous pouvez chercher dans votre deck et votre pile de défausse une amélioration pouvant être attachée à un allié, et l'ajouter à votre main.",
  // patriot — Aided Defense (Event, x2)
  'pt003': "<b>Interruption de héros</b> <i>(défense)</i> : quand votre héros se défend contre une attaque, inclinez un allié que vous contrôlez → vous gagnez +1 DEF par point de vie restant sur l'allié incliné. Si vous ne subissez aucun dégât de cette attaque, redressez l'allié incliné.",
  'pt004': "<b>Interruption de héros</b> <i>(défense)</i> : quand votre héros se défend contre une attaque, inclinez un allié que vous contrôlez → vous gagnez +1 DEF par point de vie restant sur l'allié incliné. Si vous ne subissez aucun dégât de cette attaque, redressez l'allié incliné.",
  // patriot — Covered Fire (Event, x2)
  'pt005': "<b>Interruption de héros</b> <i>(défense)</i> : quand votre héros se défend contre une attaque, choisissez un allié que vous contrôlez → infligez à un ennemi un nombre de dégâts égal à l'ATQ de cet allié, ou retirez d'une manigance un nombre de menaces égal au CTR de cet allié.",
  'pt006': "<b>Interruption de héros</b> <i>(défense)</i> : quand votre héros se défend contre une attaque, choisissez un allié que vous contrôlez → infligez à un ennemi un nombre de dégâts égal à l'ATQ de cet allié, ou retirez d'une manigance un nombre de menaces égal au CTR de cet allié.",
  // patriot — Isaiah Bradley (Support)
  'pt007': "Vous gagnez +1 REC.\n<b>Action d'alter ego</b> : inclinez Isaiah Bradley → soignez 2 dégâts sur Elijah Bradley.",
  // patriot — Commandeer (Upgrade)
  'pt008': "<b>Action de héros</b> : inclinez et défaussez Commandeer, choisissez un allié → déplacez 1 attachement d'un ennemi vers cet allié jusqu'à la fin du round. Considérez que la zone de texte de cet attachement est vierge, et que son MNG est un CTR.",
  // patriot — Commander's Orders (Upgrade)
  'pt009': "<b>Interruption de héros</b> : quand un allié que vous contrôlez devrait s'activer, inclinez Commander's Orders → échangez ses valeurs d'ATQ et de CTR pour cette activation.",
  // patriot — Follow My Lead (Upgrade)
  'pt010': "<b>Ressource</b> : inclinez Follow My Lead → générez une ressource [wild] pour un allié ou pour une amélioration pouvant être attachée à un allié.",
  // patriot — On Your Feet (Upgrade)
  'pt011': "<b>Action de héros</b> : inclinez On Your Feet → choisissez : redressez un allié, ou soignez 1 dégât sur un allié.",
  // patriot — Patriot's Shield (Upgrade)
  'pt012': "Vous gagnez +1 DEF.\n<b>Interruption de héros</b> : quand vous devriez subir des dégâts d'une attaque, vous pouvez déplacer 1 de ces dégâts ici. Quand Patriot's Shield atteint 3 dégâts, défaussez-la.",
  // patriot — Revenge (Upgrade)
  'pt013': "Attachez-la à un allié. 1 max par allié.\n<b>Interruption</b> : quand Patriot subit des dégâts d'une attaque, quel qu'en soit le nombre, défaussez Revenge → l'allié attaché gagne +2 ATQ jusqu'à la fin du prochain round.",
  // patriot — The Chosen Leader (Upgrade)
  'pt014': "<b>Réponse</b> : après qu'un allié que vous contrôlez est mis K.O. par des dégâts consécutifs, cherchez un allié dans votre deck et ajoutez-le à votre main.\n<b>Réponse forcée</b> : quand un allié que vous contrôlez est utilisé pour se défendre, infligez 1 dégât à votre identité.",
  // patriot — Throwing Stars (Upgrade)
  'pt015': "Attachez-la à un allié. 1 max par allié.\n<b>Interruption</b> <i>(attaque)</i> : quand l'allié attaché attaque, défaussez Throwing Stars → infligez 3 dégâts répartis comme vous le souhaitez. Cette attaque gagne <b><i>Perçant</i></b> et <b><i>Distance</i></b>.",
  // patriot — Working Together (Upgrade)
  'pt016': "Attachez-la à un allié. 1 max par allié.\n<b>Interruption</b> : quand l'allié attaché devrait contrer, choisissez un autre personnage ami et défaussez Working Together → ajoutez la valeur de CTR de ce personnage ami au contre de cet allié.",
  // patriot — MGH Addiction (Obligation)
  'pt017': "<b><i>Donnez-la au joueur Elijah Bradley.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Défaussez la carte de soutien Isaiah Bradley → retirez MGH Addiction de la partie.\n• Inclinez tous les alliés sous votre contrôle. Si aucun allié n'a été incliné de cette façon, cette carte gagne <b><i>Déferlement</i></b>. Défaussez cette obligation.",
  // patriot — Mr. Hyde's Lab (SideScheme, nemesis)
  'pt018': "<i>\"Vous faites juste du lèche-vitrine... ou vous voulez entrer ?\" – Mr. Hyde</i>\n<b>Une fois K.O.</b> : Mr. Hyde vous attaque. Si aucune attaque n'a eu lieu de cette façon, cherchez Mr. Hyde dans le deck de rencontre et la pile de défausse de rencontre, et mettez-le en jeu.",
  // patriot — Mr. Hyde (Minion, nemesis)
  'pt019': "Robuste.\n<b>Une fois révélée</b> : cherchez l'attachement MGH Drug dans le deck de rencontre, la pile de défausse de rencontre et les cartes mises de côté, et attachez-le à Mr. Hyde.\n<i>(Sbire némésis de Patriot.)</i>",
  // patriot — MGH Drug (Attachment, nemesis)
  'pt020': "Attachez-la à Mr. Hyde, si possible. Sinon, attachez-la au vilain.\n[star] Les attaques de l'ennemi attaché gagnent <b><i>Surpuissance</i></b>.\n<b>Action de héros</b> : dépensez des ressources [mental][energy] → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // patriot — Bulldozing Charge (Treachery, nemesis, x2)
  'pt021': "<b>Une fois révélée</b> : Mr. Hyde vous attaque. Si aucune attaque n'a eu lieu de cette façon, infligez 1 dégât à chaque personnage ami.\n<hr />\n[star] <b>Boost</b> : si cette carte est résolue durant une attaque, cette attaque gagne <b><i>Surpuissance</i></b>.",
  'pt022': "<b>Une fois révélée</b> : Mr. Hyde vous attaque. Si aucune attaque n'a eu lieu de cette façon, infligez 1 dégât à chaque personnage ami.\n<hr />\n[star] <b>Boost</b> : si cette carte est résolue durant une attaque, cette attaque gagne <b><i>Surpuissance</i></b>.",

  // ---------------------------------------------------------------- ms_america
  // Pack fan-made « jakxin », set 137. America Chavez, la Starling.
  // ma026 a ma029 sont des re-skins `full_link` (12030, 01088, 01089, 01090) :
  // le client herite du texte de la carte liee, rien a ecrire pour elles.
  // ms_america — Ms. America (Hero)
  'ma001a': "<i>Star-Gaze</i> — <b>Réponse</b> : après avoir joué une carte [[SUPERPOWER]], si la ressource IMPRIMÉE de cette carte était :\n• [physical] – infligez 1 dégât à un ennemi.\n• [energy] – soignez 1 dégât sur Ms. America.\n• [mental] – retirez 1 menace d'une manigance.\n• [wild] – redressez Ms. America.",
  // ms_america — America Chavez (AlterEgo)
  'ma001b': "Vous pouvez inclure dans votre deck des améliorations qui modifient vos pouvoirs de base, de n'importe quel aspect.\n<i>Thinking With Portals</i> — <b>Action</b> : défaussez une carte de votre main → cherchez une carte dans votre pile de défausse et mélangez-la dans votre deck. <i>(Limite d'une fois par round.)</i>",
  // ms_america — Alloy (Ally)
  'ma002': "<b><i>Robuste</i></b>.\n<b>Réponse de héros</b> : après avoir résolu « Star-Gaze », Alloy gagne +1 ATQ jusqu'à la fin du tour.",
  // ms_america — Hawkeye / Kate Bishop (Ally)
  'ma003': "[star] L'attaque de Hawkeye gagne <b><i>Perçant</i></b> et <b><i>Distance</i></b>.\n<b>Interruption</b> : quand Hawkeye devrait être mise K.O. par des dégâts consécutifs, si vous avez résolu « Star-Gaze » ce tour-ci, mélangez-la dans votre deck à la place.",
  // ms_america — Santana Family (Support)
  'ma004': "Les événements attachés à Santana Family peuvent être joués comme s'ils étaient dans votre main.\n<b>Action d'alter ego</b> : inclinez Santana Family → cherchez un événement dans votre pile de défausse et attachez-le face cachée à cette carte <i>(maximum 2)</i>.",
  // ms_america — Star Light (Upgrade)
  'ma005': "<b>Ressource de héros</b> : inclinez Star Light → générez une ressource [wild]. Vous pouvez remplacer la ressource imprimée de la carte jouée par une ressource [wild].",
  // ms_america — Star Flight (Upgrade)
  'ma006': "Ms. America gagne +1 CTR et le trait [[AERIAL]].\n<b>Interruption de héros</b> : quand vous jouez une carte Événement, inclinez Star Flight → cet événement gagne le trait [[SUPERPOWER]].",
  // ms_america — Hyper-Cosmic Awareness (Upgrade)
  'ma007': "<b>Réponse de héros</b> : après avoir joué une carte [[SUPERPOWER]], placez 1 compteur star sur cette carte.\n<b>Interruption de héros</b> : quand une carte Rencontre est révélée, inclinez cette carte et retirez-en 4 compteurs star → annulez tous ses effets et défaussez-la.",
  // ms_america — Energy Infusion (Resource)
  'ma008': "<b>Réponse de héros</b> : après avoir dépensé cette carte pour payer une carte [[SUPERPOWER]], résolvez « Star-Gaze » une fois de plus, sur la même ressource imprimée que la carte jouée.",
  // ms_america — America's Anger (Event, x2)
  'ma009': "<b>Action de héros</b> : choisissez CTR ou ATQ et redressez votre identité → doublez tous les modificateurs appliqués au pouvoir choisi lors de sa prochaine utilisation ce tour-ci.",
  'ma010': "<b>Action de héros</b> : choisissez CTR ou ATQ et redressez votre identité → doublez tous les modificateurs appliqués au pouvoir choisi lors de sa prochaine utilisation ce tour-ci.",
  // ms_america — Bulletproof Chica (Event, x2)
  'ma011': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, prévenez tous ces dégâts. Donnez une carte de statut Robuste à votre identité.",
  'ma012': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, prévenez tous ces dégâts. Donnez une carte de statut Robuste à votre identité.",
  // ms_america — Star Portal (Event, x2)
  'ma013': "<b>Action de héros</b> : cherchez un allié dans la pile de défausse de n'importe quel joueur et mettez-le incliné dans la zone de jeu de n'importe quel joueur → retirez d'une manigance un nombre de menaces égal au CTR de cet allié et infligez à un ennemi un nombre de dégâts égal à son ATQ.",
  'ma014': "<b>Action de héros</b> : cherchez un allié dans la pile de défausse de n'importe quel joueur et mettez-le incliné dans la zone de jeu de n'importe quel joueur → retirez d'une manigance un nombre de menaces égal au CTR de cet allié et infligez à un ennemi un nombre de dégâts égal à son ATQ.",
  // ms_america — Break Through (Event, x2)
  'ma015': "<b>Action de héros</b> <i>(attaque/contre)</i> : infligez 4 dégâts à un ennemi. Retirez 3 menaces d'une manigance. Si cela met K.O. un ennemi ou une manigance, étourdissez ou désorientez un ennemi.",
  'ma016': "<b>Action de héros</b> <i>(attaque/contre)</i> : infligez 4 dégâts à un ennemi. Retirez 3 menaces d'une manigance. Si cela met K.O. un ennemi ou une manigance, étourdissez ou désorientez un ennemi.",
  // ms_america — Edges Syndrome (Obligation)
  'ma017': "<b><i>Donnez-la au joueur America Chavez.</i></b>\nVotre identité subit -1 à chacun de ses pouvoirs de base.\n<b>Action</b> : subissez 2 dégâts → défaussez cette carte.\n<b>Action</b> : subissez 4 dégâts → retirez cette carte de la partie.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // ms_america — Catalina Chavez (Minion, nemesis)
  'ma018': "<b><i>Coup Rapide</i></b>.\n[star] Catalina Chavez gagne chaque modificateur de caractéristique présent dans votre zone de jeu (le CTR étant remplacé par le MNG).\n<i>(Sbire némésis de Ms. America.)</i>",
  // ms_america — Search for the Cure (SideScheme, nemesis)
  'ma019': "<b>Une fois révélée</b> : chaque joueur cherche un allié dans sa pile de défausse et l'attache à cette carte. La menace de départ de cette carte est égale au coût en ressources cumulé des cartes attachées. Pour chaque joueur qui n'a attaché aucun allié, cette carte reçoit 2[per_hero] menaces de départ supplémentaires.",
  // ms_america — Star Lightning (Treachery, nemesis, x2)
  'ma020': "<b>Une fois révélée</b> : Catalina Chavez vous attaque. Si cette attaque inflige des dégâts, votre identité est étourdie. Si aucune attaque n'a eu lieu de cette façon, cette carte gagne <b><i>Déferlement</i></b>.",
  'ma021': "<b>Une fois révélée</b> : Catalina Chavez vous attaque. Si cette attaque inflige des dégâts, votre identité est étourdie. Si aucune attaque n'a eu lieu de cette façon, cette carte gagne <b><i>Déferlement</i></b>.",
  // ms_america — Gwenpool (Ally, Agressivite)
  'ma022': "[star] Gwenpool gagne +1 ATQ par amélioration spécifique à une identité que vous contrôlez <i>(maximum +2 ATQ)</i>.",
  // ms_america — Marvel Boy (Ally, Basic)
  'ma023': "<b>Interruption</b> : quand Marvel Boy est mis K.O. par des dégâts consécutifs, redressez une amélioration que vous contrôlez.",
  // ms_america — Noh-Varr's Ship (Support, Basic)
  'ma024': "Jouable uniquement si votre identité a le trait [[YOUNG AVENGER]].\n<b>Ressource</b> : inclinez Noh-Varr's Ship → générez une ressource [wild].",
  // ms_america — Power Stomp (Event, Agressivite)
  'ma025': "Jouable uniquement si votre héros a au moins 3 ATQ.\n<b>Action de héros</b> <i>(attaque)</i> : infligez X dégâts au vilain et à chaque sbire engagé avec vous, X étant égal à votre ATQ.",

  // ---------------------------------------------------------------- venompool
  // Pack fan-made « CptScorp », Cycle 2, set 129. Wade Wilson porte le
  // symbiote Klyntar. Le mot-cle maison « drain X » est DEFINI par l'insert du
  // pack : infliger X degats a l'ennemi, puis soigner X degats sur votre
  // identite (voir docs/reference/mots-cles/drain-x.md).
  // venompool — Venompool (Hero)
  'vp001a': "<i>Fear Factor</i> — <b>Réponse</b> <i>(contrer)</i> : après que Venompool a mis un ennemi K.O., retirez 1 menace d'une manigance. <i>(Limite 1 [per_hero] par phase.)</i>",
  // venompool — Wade Wilson (AlterEgo)
  'vp001b': "[star] Wade Wilson ne peut utiliser sa REC que lorsqu'il a 3 points de vie ou moins.\n<i>Unexpected Bond</i> — <b>Action</b> : inclinez Wade Wilson → cherchez l'amélioration Klyntar Suit dans votre deck et votre pile de défausse et ajoutez-la à votre main. Mélangez votre deck.",
  // venompool — Black Cat (Ally, signature)
  'vp002': "[star] Le contre de base de Black Cat ignore les icônes de crise ([crisis]).",
  // venompool — Talk About Armed Assault (Event, x3)
  'vp003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts répartis entre les ennemis comme vous le souhaitez <i>(6 dégâts à la place si l'amélioration True Form est en jeu)</i>.",
  // venompool — Tasty Meal (Event, x2)
  'vp004': "<b>Action de héros</b> <i>(attaque/contrer)</i> : infligez 2 dégâts à un ennemi. Retirez 1 menace d'une manigance. Venompool gagne +1 CTR, +1 ATQ et +1 DEF jusqu'à la fin de la manche. Si True Form est en jeu, cette attaque gagne <b><i>Perçant</i></b>.",
  // venompool — Thwip! (Event, x2)
  'vp005': "<b>Action de héros</b> <i>(contrer)</i> : étourdissez le vilain. Si le vilain est déjà étourdi, retirez 3 menace d'une manigance à la place.",
  // venompool — Whack-a-Rabbit (Event, x3)
  'vp006': "Vous pouvez déclencher l'« <b>Action de héros</b> » ci-dessous une fois de plus par sbire engagé avec vous. <i>(Chaque ennemi ne peut être ciblé qu'une seule fois.)</i>\n<b>Action de héros</b> <i>(attaque)</i> : subissez 1 dégât → infligez 2 dégâts à un ennemi.",
  // venompool — Eat Them All! (Upgrade)
  'vp007': "<b>Réponse de héros</b> : après que Venompool a attaqué, soignez 1 dégât sur lui. <i>(Limite une fois par phase.)</i>",
  // venompool — Foresight (Upgrade)
  'vp008': "<b>Action de héros</b> : subissez 2 dégâts et inclinez Foresight → redressez Venompool.",
  // venompool — Klyntar Suit (Upgrade)
  'vp009': "Vous gagnez +3 points de vie.\n<b>Réponse de héros</b> <i>(attaque)</i> : après avoir subi des dégâts d'une attaque ennemie, inclinez Klyntar Suit → drainez 1 à l'ennemi attaquant. <i>(Voir l'insert : infligez 1 dégât à cet ennemi, puis soignez 1 dégât sur votre identité.)</i>",
  // venompool — True Form (Upgrade)
  'vp010': "Défaussez cette carte du jeu si vous ne contrôlez pas Klyntar Suit.\n<b>Interruption de héros</b> : quand Venompool fait une attaque de base contre un ennemi, inclinez True Form → cette attaque gagne <b><i>Surpuissance</i></b>. Drainez 1 à cet ennemi.",
  // venompool — One Too Many Voices (Obligation)
  'vp011': "<b><i>Donnez cette carte au joueur de Wade Wilson.</i></b>\nVous devez passer en forme alter ego. Choisissez :\n• Inclinez Wade Wilson → retirez One Too Many Voices de la partie.\n• Défaussez Klyntar Suit. Si Klyntar Suit n'a pas été défaussée de cette façon, cette carte gagne <b><i>Déferlement</i></b>. Défaussez cette obligation.",
  // venompool — Shocking Entrance (SideScheme, nemesis)
  'vp012': "<b>Une fois révélée</b> : infligez 3 dégâts indirects au premier joueur.\n<i>(Icône de danger : distribuez +1 carte de rencontre durant la phase du vilain.)</i>\n<hr />\n[star] <b>Boost</b> : infligez 1 dégât indirect au premier joueur.",
  // venompool — Killer Thrill (Minion, nemesis)
  'vp013': "[star] Killer Thrill gagne +1 ATQ par compteur d'adrénaline sur elle.\n<b>Interruption forcée</b> : quand la phase du joueur se termine, placez 1 compteur d'adrénaline sur Killer Thrill. Puis, s'il y a 2 compteurs d'adrénaline ou plus sur elle, retirez-les tous et elle s'active.\n<i>(Sbire nemesis de Venompool.)</i>",
  // venompool — Coldwar (Minion, nemesis)
  'vp014': "<b><i>Coup Rapide</i></b>. <i>(Après que ce sbire s'est engagé avec votre héros, il vous attaque.)</i>\n[star] Tant que Killer Thrill est en jeu, Coldwar gagne +1 ATQ.\n<hr />\n[star] <b>Boost</b> : après cette activation, distribuez-vous cette carte comme carte de rencontre face cachée.",
  // venompool — Guzz (Minion, nemesis)
  'vp015': "<b><i>Plotting</i></b>. <i>(Après que ce sbire s'est engagé avec vous, il manigance.)</i>\n[star] Tant que Killer Thrill est en jeu, Guzz gagne +1 MNG.\n<hr />\n[star] <b>Boost</b> : après cette activation, distribuez-vous cette carte comme carte de rencontre face cachée.",
  // venompool — Psyche Warp (Treachery, nemesis)
  'vp016': "<b>Une fois révélée</b> : vous subissez X dégâts, X étant égal à l'ATQ de l'allié ayant la plus haute ATQ IMPRIMÉE parmi vos alliés. Défaussez cet allié. Si aucun dégât n'a été subi de cette façon, cette carte gagne <b><i>Déferlement</i></b>.",

  // ------------------------------------------------------------------- angela
  // Pack fan-made « Juri Krasko », set 133. Aldrif Odinsdottir, fille d'Odin
  // elevee dans le Heven. Tout son kit paie quand un SBIRE tombe.
  // angela — Angela (Hero)
  'an001a': "<i>Frenzy</i> — <b>Réponse</b> : après avoir mis un sbire K.O., redressez Angela. <i>(Limite une fois par manche.)</i>",
  // angela — Aldrif Odinsdottir (AlterEgo)
  'an001b': "<b>Mise en place</b> : cherchez une carte [[WEAPON]] dans votre deck et votre pile de défausse et ajoutez-la à votre main. Mélangez votre deck.\n[star] <i>Of Heven and Hel</i> — Aldrif Odinsdottir gagne +1 REC par carte [[WEAPON]] que vous contrôlez.",
  // angela — Sera (Ally, signature)
  'an002': "Angela gagne +1 en taille de main.",
  // angela — Heven's Fury (Event, x3)
  'an003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 7 dégâts à un ennemi. Vous pouvez incliner une carte [[WEAPON]] que vous contrôlez. Si vous le faites, répartissez plutôt les dégâts entre les ennemis en jeu.",
  // angela — Murderous Glare (Event, x3)
  'an004': "<b>Réponse</b> <i>(contrer)</i> : après qu'Angela a attaqué et mis un ennemi K.O., retirez 2 menaces d'une manigance. Retirez 1 menace supplémentaire de CETTE manigance par sbire que vous avez mis K.O. durant cette manche.",
  // angela — Single Out (Event, x3)
  'an005': "<b>Interruption de héros</b> : quand une carte de traîtrise est révélée depuis le deck de rencontre, annulez ses effets « <b>Une fois révélée</b> ». Cherchez un sbire dans le deck de rencontre et mettez-le en jeu engagé avec n'importe quel joueur.",
  // angela — Angelic Ribbons (Upgrade)
  'an006': "Angela gagne <b><i>Ferme</i></b>.\n<b>Interruption de héros</b> : quand un ennemi s'active, défaussez cette carte → cet ennemi gagne -X ATQ et -X MNG pour cette activation, X étant l'ATQ d'Angela.",
  // angela — Asgard's Assassin (Upgrade, x2)
  'an007': "<b>Ressource de héros</b> : inclinez Asgard's Assassin → générez une ressource [physical] <i>(si vous avez mis un sbire K.O. durant cette manche, générez plutôt [wild])</i>.",
  // angela — Siri's Dress (Upgrade)
  'an008': "Vous gagnez +4 points de vie.\nAngela gagne le trait [[AERIAL]].",
  // angela — Xiphos, Sword of the Stars (Upgrade)
  'an009': "<b><i>Limité</i></b>.\nAngela gagne +1 ATQ.\n<b>Réponse</b> : après qu'Angela a mis un sbire K.O., piochez une carte. <i>(Limite une fois par manche.)</i>",
  // angela — Banished from Asgard (Obligation)
  'an010': "<b><i>Donnez cette carte au joueur d'Aldrif Odinsdottir.</i></b>\nVous pouvez passer en forme alter ego. Choisissez :\n• Inclinez Aldrif Odinsdottir → retirez Banished from Asgard de la partie.\n• Défaussez 1 carte [[ASGARD]] que vous contrôlez. Vous êtes étourdi. Si aucune carte n'a été défaussée de cette façon, cette carte gagne <b><i>Déferlement</i></b>. Défaussez cette obligation.",
  // angela — Hel's Retribution (SideScheme, nemesis)
  'an011': "<b>Une fois révélée</b> : le joueur actif défausse de son deck autant de cartes qu'il y a de cartes [[ASGARD]] en jeu.\n<i>(Icône de danger : distribuez +1 carte de rencontre durant la phase du vilain.)</i>",
  // angela — Hela (Minion, nemesis)
  'an012': "Tant qu'il y a d'autres sbires en jeu, Hela ne peut pas subir de dégâts.\n<b>Interruption forcée</b> : quand vous mettez un sbire K.O., défaussez une carte de votre main.\n<i>(Sbire nemesis d'Angela.)</i>",
  // angela — Hel-Wolf (Minion, nemesis)
  'an013': "[star] Le joueur engagé doit se défendre contre les attaques de Hel-Wolf avec un allié qu'il contrôle, s'il le peut.\n<hr />\n[star] <b>Boost</b> : cette attaque gagne <b><i>Surpuissance</i></b>.",
  // angela — Disir (Minion, nemesis)
  'an014': "<b>Interruption forcée</b> : quand Disir devrait être mise K.O., mélangez-la plutôt dans le deck de rencontre.\n<hr />\n[star] <b>Boost</b> : après la fin de cette activation, mélangez cette carte dans le deck de rencontre.",
  // angela — Back from Hel (Treachery, nemesis)
  'an015': "<b>Une fois révélée</b> : cherchez le sbire le plus au fond de la pile de défausse de rencontre et révélez-le.\n<hr />\n[star] <b>Boost</b> : si vous êtes engagé avec un sbire, cette attaque gagne 1 icône de boost supplémentaire ([boost]).",

  // harry_osborn — Green Goblin (Hero)
  'ho001a': "<b>Réponse</b> : après que vous avez attaqué un ennemi, retirez 1 carte de statut de CET ennemi → infligez 2 dégâts à un ennemi et retirez 2 menaces d'une manigance.",
  // harry_osborn — Harry Osborn (AlterEgo)
  'ho001b': "Vous pouvez inclure dans votre deck le nombre maximal d'exemplaires de 3 améliorations [[TECH]] d'aspects autres que l'aspect choisi.",
  // harry_osborn — Spider-Man, Peter Parker (Ally, signature)
  'ho002': "<b>Réponse</b> : après que Spider-Man est entré en jeu, placez un total de 2 cartes de statut étourdi sur jusqu'à 2 ennemis.",
  // harry_osborn — Repulsor Blast (Event, x2)
  'ho003': "<b>Action de héros</b> <i>(attaque)</i> : étourdissez un ennemi. Infligez 4 dégâts à CET ennemi.",
  // harry_osborn — Pumpkin Bomb (Event, x2)
  'ho004': "<b>Action de héros</b> <i>(attaque)</i> : choisissez un joueur. Infligez X dégâts au Méchant et à chaque sbire engagé avec ce joueur. Pour chaque ennemi mis K.O. de cette façon, désorientez un ennemi.",
  // harry_osborn — Gwen Stacy Osborn (Support, signature)
  'ho005': "Harry Osborn gagne +1 REC.\n<b>Action d'alter ego</b> : inclinez Harry Osborn et Gwen Stacy Osborn → désorientez un ennemi.",
  // harry_osborn — Norman Osborn (Support, signature)
  'ho006': "<b>Interruption de héros</b> : quand vous jouez un événement [[ATTACK]], inclinez Norman Osborn → cet événement inflige 1 dégât supplémentaire.",
  // harry_osborn — Otto Octavius (Support, signature)
  'ho007': "<b>Action d'alter ego</b> : inclinez Otto Octavius → choisissez un joueur. Ce joueur cherche une amélioration [[TECH]] dans son deck et l'ajoute à sa main. (Mélangez.)",
  // harry_osborn — Goblin Armor (Upgrade, signature)
  'ho008': "Vous gagnez +3 points de vie.\n<b>Action de héros</b> <i>(contre)</i> : inclinez Goblin Armor → retirez 1 menace d'une manigance (2 menaces à la place si vous avez le trait [[AERIAL]]).",
  // harry_osborn — Goblin Helmet (Upgrade, signature)
  'ho009': "<b>Action de héros</b> : inclinez Goblin Helmet → redressez une amélioration [[TECH]] que vous contrôlez.\n<b>Ressource de héros</b> : inclinez Goblin Helmet et 1 amélioration [[TECH]] que vous contrôlez → générez la ressource imprimée sur cette amélioration.",
  // harry_osborn — Powered Gauntlets (Upgrade, x2)
  'ho010': "<b>Action de héros</b> <i>(attaque)</i> : inclinez Powered Gauntlets → infligez 1 dégât à un ennemi. Si vous avez le trait [[AERIAL]], vous pouvez dépenser une ressource de n'importe quel type pour désorienter CET ennemi.",
  // harry_osborn — Goblin Glider (Upgrade, signature)
  'ho011': "Green Goblin gagne +1 ATQ et le trait [[AERIAL]].\n<b>Action de héros</b> : inclinez Goblin Glider → redressez Green Goblin.",
  // harry_osborn — "That Had to Hurt" (Upgrade, x2)
  'ho012': "Temporaire. Forme héros seulement. Attachez à un ennemi. 1 max par ennemi.\nLe personnage attaché perd le mot-clé Robuste ou Solide.\n<b>Réponse</b> : après que le personnage attaché a reçu une carte de statut, infligez-lui 1 dégât.",
  // harry_osborn — Risky Business (Obligation)
  'ho013': "<b><i>Donnez au joueur Harry Osborn.</i></b>\nVous êtes étourdi.\n<b>Action d'alter ego</b> : inclinez Harry Osborn → défaussez cette carte. Renvoyez dans votre main l'amélioration [[TECH]] la plus au-dessus de votre pile de défausse.",
  // harry_osborn — Ruler of Manhattan (SideScheme nemesis)
  'ho014': "<b>Une fois révélée</b> : défaussez les cartes du dessus du deck de rencontre jusqu'à défausser une manigance annexe. Révélez cette manigance annexe. Retirez d'ici autant de menaces que le nombre d'icônes de boost ([boost]) sur cette carte.\n<i>(Icône de danger : distribuez +1 carte de rencontre durant la phase du vilain.)</i>\n<i>(Manigance annexe némésis de Green Goblin.)</i>",
  // harry_osborn — Kingpin (Minion nemesis)
  'ho015': "[star] Kingpin gagne +1 MNG et +1 ATQ pour chaque manigance annexe en jeu.\n<i>(Sbire némésis de Green Goblin.)</i>\n<hr />\n[star] <b>Boost</b> : placez 2 menaces sur chaque manigance annexe.",
  // harry_osborn — Bullseye (Minion nemesis, x2)
  'ho016': "Robuste. Vilenie.\n[star] L'attaque de Bullseye gagne <b><i>Perçant</i></b> et <b><i>Déferlement</i></b>.",
  // harry_osborn — Refrain From Argument (SideScheme nemesis)
  'ho017': "Entrave 1[per_hero].\n<i>(Icône de crise : la menace ne peut pas être retirée de la manigance principale.)</i>\n<hr />\n[star] <b>Boost</b> : révélez cette carte s'il n'y a aucune manigance annexe en jeu.",

  // agatha_harkness — Agatha Harkness (Hero)
  'aa001a': "<i>Power Absorption</i> — <b>Réponse</b> : après qu'Agatha Harkness a subi des dégâts d'une attaque, défaussez autant de cartes du dessus de votre deck. Ajoutez à votre main 1 carte [[SPELL]] défaussée de cette façon. <i>(Limite une fois par phase.)</i>",
  // agatha_harkness — Agatha Harkness (AlterEgo)
  'aa001b': "<b>Mise en place</b> : mettez Ghost Agatha de côté. Cherchez la manigance-joueur Agatha All Along et ajoutez-la à votre main.\n<i>Ghost Form</i> — <b>Réponse forcée</b> : après que vous avez été éliminé de la partie, mettez en jeu le soutien Ghost Agatha mis de côté.",
  // agatha_harkness — Scarlet Witch (Ally, signature)
  'aa002': "Vous pouvez jouer l'événement attaché à Scarlet Witch comme s'il était dans votre main, en réduisant son coût de 1.\n<b>Réponse</b> : après que Scarlet Witch est entrée en jeu, choisissez un événement [[SPELL]] dans votre pile de défausse et attachez-le à elle face cachée.",
  // agatha_harkness — Ebony (Support, signature)
  'aa003': "Tant que vous êtes sous forme d'alter ego, Agatha Harkness gagne +1 REC.\n<b>Action d'alter ego</b> : inclinez Ebony → regardez les 2 cartes du dessus de votre deck. Ajoutez-en 1 à votre main.",
  // agatha_harkness — Wake Thy Power (Event, x2)
  'aa004': "<b>Action de héros</b> : défaussez les 2 cartes du dessus de votre deck. Pour chaque icône de ressource défaussée de cette façon :\n• [energy] – retirez 2 menaces d'une manigance.\n• [mental] – piochez 1 carte.\n• [physical] – soignez 2 dégâts de votre héros.\n• [wild] – choisissez 1 des options ci-dessus.",
  // agatha_harkness — Witchcraft (Event, x3)
  'aa005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 1 dégât à un ennemi. Défaussez les 3 cartes du dessus du deck de rencontre. Pour chaque icône de boost défaussée de cette façon, infligez 1 dégât supplémentaire à CET ennemi. Pour chaque carte défaussée de cette façon sans icône de boost, étourdissez ou désorientez un ennemi.",
  // agatha_harkness — Soul Harvest (Event, x2)
  'aa006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Soignez 2 dégâts d'Agatha Harkness. Défaussez la carte du dessus de votre deck. Si ses ressources imprimées comportent :\n• [wild] ou [physical] — étourdissez CET ennemi.\n• [mental] ou [energy] — désorientez CET ennemi.",
  // agatha_harkness — Occult Knowledge (Resource, signature)
  'aa007': "<b>Réponse</b> : après que cette carte a été défaussée du dessus de votre deck, ajoutez-la à votre main.",
  // agatha_harkness — Agatha All Along (PlayerSideScheme, signature)
  'aa008': "Victoire 0.\n<b>Réponse</b> : après qu'Agatha Harkness a subi des dégâts d'une attaque, retirez autant de menaces d'ici.\nTant qu'Agatha All Along est au tableau des victoires, Agatha Harkness gagne +1 à chacun de ses pouvoirs de base et +3 points de vie.",
  // agatha_harkness — The Witches' Road (Support, signature)
  'aa009': "<b>Réponse</b> : après qu'un alter ego [[MYSTIC]] est passé sous forme de héros, inclinez The Witches' Road → réduisez de 1 le coût en ressources de la prochaine carte [[SPELL]] que ce héros joue cette phase. Mélangez 2 cartes de la défausse de ce héros dans son deck.",
  // agatha_harkness — Mirror Image (Upgrade, signature)
  'aa010': "Tant que vous êtes sous forme de héros, Agatha Harkness gagne +1 CTR.\n<b>Interruption</b> : quand vous devriez subir des dégâts qui vous mettraient K.O., défaussez plutôt cette carte.",
  // agatha_harkness — Runic Magician (Upgrade, signature)
  'aa011': "<b>Ressource</b> : inclinez Runic Magician → générez une ressource [wild] pour une carte [[SPELL]] ou [[MYSTIC]].\n<b>Interruption de héros</b> : quand vous résolvez la capacité « Power Absorption » d'Agatha Harkness, ignorez l'exigence du trait [[SPELL]].",
  // agatha_harkness — Regained Youth (Upgrade, signature)
  'aa012': "Vous gagnez +4 points de vie.\n<b>Réponse</b> : après que votre deck s'est vidé, soignez 2 dégâts de votre identité.",
  // agatha_harkness — Ghost Agatha (Support persona, mise de côté)
  'aa013': "Permanente. Le premier joueur contrôle Ghost Agatha.\n<b>Action</b> : inclinez Ghost Agatha → regardez les 3 cartes du dessus de votre deck. Piochez-en 1, défaussez-en 1 et remettez-en 1 sur le dessus de votre deck.",
  // agatha_harkness — Chaotic Forces (Obligation)
  'aa014': "<b><i>Donnez-la au joueur Agatha Harkness.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Cherchez Agatha All Along au tableau des victoires et mettez-la en jeu → retirez Chaotic Forces de la partie.\n• Défaussez cette carte et la carte du dessus du deck de rencontre. Pour chaque icône de boost défaussée de cette façon, subissez 1 dégât indirect.",
  // agatha_harkness — Burned at the Stake (SideScheme nemesis)
  'aa015': "Death gagne <b><i>Robuste</i></b>.\n<i>(Icône de danger : distribuez +1 carte de rencontre durant la phase du vilain.)</i>",
  // agatha_harkness — Death (Minion nemesis)
  'aa016': "[star] Death ne peut pas être vaincue.\n<b><i>Vulnérable</i></b>. <i>(Défaussez ce personnage s'il est étourdi ou désorienté.)</i>\n<i>(Sbire némésis d'Agatha Harkness.)</i>",
  // agatha_harkness — Funeral (Obligation du set nemesis)
  'aa017': "Votre héros gagne -1 CTR.\n<b>Action d'alter ego</b> : dépensez une ressource [energy] → défaussez cette carte.",
  // agatha_harkness — Death's Embrace (Attachment nemesis, x2)
  'aa018': "Attachez-la à votre identité.\nChaque carte que vous jouez coûte 1 ressource supplémentaire.\n<b>Action de héros</b> : inclinez votre héros ou dépensez [mental][energy][physical] → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : si cette activation est une manigance, attachez cette carte au premier joueur.",
  // agatha_harkness — Wiccan (Ally Justice, carte bonus)
  'aa019': "<b>Réponse</b> : après que Wiccan a contré, défaussez la carte du dessus du deck de rencontre. Pour chaque icône de boost défaussée de cette façon, infligez 1 dégât à un ennemi.",
  // agatha_harkness — Pixie (Ally Leadership, carte bonus)
  'aa020': "<b>Réponse</b> : après avoir joué Pixie depuis votre main, ajoutez un allié [[X-MEN]] de votre pile de défausse à votre main.",
  // agatha_harkness — Coven of Chaos (Event Leadership, carte bonus)
  'aa021': "Jouable seulement si votre identité a le trait [[MYSTIC]].\n<b>Action d'alter ego</b> : mettez en jeu un allié [[MYSTIC]] de la pile de défausse de n'importe quel joueur, sous le contrôle de son propriétaire.",
  // beast — Beast (Hero)
  'bt001a': "<i>Thick Skinned</i> — <b>Réponse</b> : quand vous subissez 0 dégât en vous défendant, cherchez n'importe quelle carte dans votre deck ou votre pile de défausse et ajoutez-la à votre main.",
  // beast — Dr Hank McCoy (AlterEgo)
  'bt001b': "<i>Scientific Discovery</i> — <b>Réponse forcée</b> : après que vous êtes passé sous cette forme, mélangez 1 carte de découverte au hasard dans votre deck.\n<b>Mise en place</b> : toutes les cartes que vous écartez de votre main au mulligan pendant la mise en place sont remélangées dans votre deck.",
  // beast — Wonder Man (Ally, signature)
  'bt002': "<b>Une fois vaincu</b> : infligez 2 dégâts à un ennemi.",
  // beast — Phoenix (Ally, signature)
  'bt003': "<b>Une fois vaincue</b> : infligez 2 dégâts à un ennemi.",
  // beast — Experimental Warfare (Event, signature)
  'bt004': "<b>Interruption</b> <i>(défense)</i> : inclinez toutes les cartes d'amélioration en jeu, Beast gagne +1 DEF par amélioration inclinée quand il se défend contre cette attaque. Si l'attaque a infligé « 0 » dégât, infligez 3 dégâts au personnage attaquant et redressez votre identité.",
  // beast — Fighting With Friends (Event, x2)
  'bt005': "<b>Réponse de héros</b> : redressez votre héros. Si vous avez payé cette carte avec une ressource [mental] → redressez un allié.",
  // beast — In The Heat Of Battle (Event, signature)
  'bt006': "<b>Action</b> <i>(contrer)</i> : retirez 4 menaces d'une manigance. Si cet événement a retiré toutes les menaces d'une manigance → mélangez 1 carte de découverte dans votre main.",
  // beast — Multi-Tasking ([mental]) (Event, signature)
  'bt007a': "<b>Action de héros</b> <i>(contrer)</i> <i>(attaque)</i> : infligez 1 dégât à tous les personnages ennemis et retirez 1 menace de toutes les manigances. Si c'était la première carte que vous avez jouée ce tour-ci → répétez cette action de héros.",
  // beast — Multi-Tasking ([physical]) (Event, signature)
  'bt007b': "<b>Action de héros</b> <i>(contrer)</i> <i>(attaque)</i> : infligez 1 dégât à tous les personnages ennemis et retirez 1 menace de toutes les manigances. Si c'était la première carte que vous avez jouée ce tour-ci → répétez cette action de héros.",
  // beast — Primal Rage (Event, x2)
  'bt008': "<b>Interruption de héros</b> : quand vous effectuez une attaque de base, défaussez une carte de votre main → vous gagnez +5 ATQ pour cette attaque.",
  // beast — Alien Materials (Resource double [energy][mental], x2)
  'bt009': "",
  // beast — Beast's Lab (Support, signature)
  'bt010': "<b>Action de héros</b> : inclinez Beast's Lab → choisissez un joueur. Ce joueur cherche une amélioration dans son deck et sa pile de défausse et l'ajoute à sa main.",
  // beast — Hank's Kimono (Support, signature)
  'bt011': "<b>Action d'alter ego</b> : inclinez Hank's Kimono → cherchez une carte ressource dans votre pile de défausse et placez-la sur le dessus de votre deck.",
  // beast — Civilian Disguise (Support, signature)
  'bt012': "<i>(Entre en jeu avec 3 compteurs de déguisement.)</i>\n<b>Réponse</b> : après vous être défendu contre une attaque, retirez 1 compteur de déguisement → piochez 1 carte.",
  // beast — Hunter Gear (Upgrade, signature)
  'bt013': "Beast gagne +1 DEF.\n<b>Action</b> : inclinez Hunter Gear → générez une ressource [physical] si vous n'avez aucune carte marquée d'une ressource [physical] dans votre main.",
  // beast — Peter Parker (Ally, découverte mise de côté)
  'bt014': "<b>Action</b> : inclinez cette carte → générez une ressource [wild].",
  // beast — Space Hand Grenade (Upgrade, découverte mise de côté)
  'bt015': "Attachez-la à un sbire.\n<b>Interruption forcée</b> : quand ce sbire devrait attaquer, annulez cette attaque et infligez 4 dégâts à ce sbire.",
  // beast — Ambush (Event, découverte mise de côté)
  'bt016': "<b>Interruption forcée</b> <i>(attaque/défense)</i> : quand le vilain devrait vous attaquer, inclinez une carte de soutien en jeu → annulez cette attaque.",
  // beast — Automated Life-Support (Upgrade, découverte mise de côté)
  'bt017': "Attachez-la à un allié. 1 max par allié.\n<b>Interruption forcée</b> : quand l'allié devrait être vaincu, soignez 1 dégât et donnez-lui une carte de statut Robuste.",
  // beast — Mecha-Beast (Upgrade, découverte mise de côté)
  'bt018': "Attachez-la à Beast.\nBeast gagne +1 CTR et +2 points de vie.",
  // beast — Unfinished Projects (Obligation)
  'bt019': "<b><i>Donnez-la au joueur Hank McCoy.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Défaussez 2 cartes d'amélioration/soutien en jeu → retirez Mutation Degeneration de la partie.\n• Inclinez votre identité et subissez 2 dégâts. Défaussez cette obligation.",
  // beast — Lizard-Fied Mutants (Minion nemesis, x2)
  'bt020': "<b><i>Garde</i></b>. <b><i>Patrouille</i></b>. <i>(Tant que ce sbire est engagé avec vous, vous ne pouvez pas attaquer le vilain, et vous ne pouvez pas contrer la manigance principale.)</i>\n<i>(Sbire némésis de Beast.)</i>",
  // beast — Dark Transformation (Treachery nemesis)
  'bt021': "<b>Une fois révélée</b> : défaussez les 5 cartes du dessus de votre deck. Vous subissez 1 dégât pour chaque carte spécifique au héros défaussée de cette façon.",
  // beast — Dark Beast (Minion nemesis)
  'bt022': "<b><i>Robuste</i></b>. <i>(Ce personnage ne peut être ni étourdi ni désorienté.)</i>\n<b>Une fois révélé</b> : tous les alliés sont désorientés.\n<i>(Sbire némésis de Beast.)</i>",
  // beast — Mutant Science Program (SideScheme nemesis)
  'bt023': "<i>« Beast enlève des mutants et pratique sur eux des tests dangereux. »</i>\n<b>Une fois révélée</b> : placez 1 compteur de test sur cette manigance annexe pour chaque allié dans votre pile de défausse. S'il n'y a aucun allié dans votre pile de défausse, placez plutôt 2[per_hero] compteurs de test.\n<b>Réponse forcée</b> : chaque fois que vous piochez un allié dans votre main → retirez 1 compteur de test, défaussez l'allié, puis cherchez le sbire Lizard-Fied dans le deck de rencontre ou la pile de défausse et mettez-le en jeu.",
  // doctor_doom — Doctor Doom (Hero)
  'dd001a': "<i>Power Syphon</i> — <b>Réponse</b> : après que vous avez payé un événement [[SPELL]] avec une ressource [mental], placez 1 compteur de pouvoir ici (maximum 3).\n<i>Overwhelming Power</i> — <b>Action</b> : retirez 3 compteurs de pouvoir → vous gagnez <b><i>Vilain</i></b> jusqu'à la fin du round. Ignorez les effets de boost des cartes de boost qui vous sont distribuées.",
  // doctor_doom — Victor von Doom (AlterEgo)
  'dd001b': "Vous ne pouvez inclure aucun allié supplémentaire dans votre deck.\n<i>Master of Magic and Technology</i> — vous pouvez inclure jusqu'à 6 cartes [[TECH]] et/ou [[SPELL]] d'aspects autres que celui que vous avez choisi.",
  // doctor_doom — Victorious (Ally, signature)
  'dd002': "<b><i>Robuste</i></b>.\n<b>Réponse</b> : après que Victorious est entrée en jeu, cherchez un événement [[SPELL]] dans votre deck et votre pile de défausse et ajoutez-le à votre main.",
  // doctor_doom — Doombot (Ally, x2)
  'dd003': "<b><i>Exigence</i></b> ([mental]). <i>(En payant cette carte, dépensez les ressources indiquées.)</i>\n<b><i>Robuste</i></b>.\n<b>Interruption</b> : quand un ennemi vous attaque, jouez Doombot depuis votre main (en payant son coût) et déclarez-le défenseur sans l'incliner.",
  // doctor_doom — "This World Is Mine!" (Event, x3)
  'dd004': "<b>Action de héros</b> <i>(attaque)</i> : infligez 8 dégâts à un ennemi. Si vous avez payé cette carte uniquement avec des ressources [mental], cette attaque gagne <b><i>Déferlement</i></b> et <b><i>Perçage</i></b>.",
  // doctor_doom — "Doom Prevails" (Event, signature)
  'dd005': "<b>Action de héros</b> : regardez les 3 cartes du dessus du deck de rencontre. Infligez X dégâts répartis entre les ennemis en jeu, où X est le nombre d'icônes ([star] et [boost]) dans la zone de boost de ces cartes. Si vous avez payé cette carte uniquement avec des ressources [mental], retirez aussi X menaces réparties entre les manigances en jeu.",
  // doctor_doom — "Pain Is For Lesser Men!" (Event, x2)
  'dd006': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts d'une attaque, empêchez tous ces dégâts. Si vous avez payé cette carte uniquement avec des ressources [mental], étourdissez et désorientez l'ennemi.",
  // doctor_doom — Unparalleled Genius (Resource [mental]x3, x2)
  'dd007': "",
  // doctor_doom — Doomstadt (Support, signature)
  'dd008': "Les événements glissés sous Doomstadt peuvent être joués comme s'ils étaient dans votre main.\n<b>Action</b> : inclinez Doomstadt → glissez un événement [[SPELL]] de votre main sous cette carte (maximum 3).",
  // doctor_doom — Doom's Time Platform (Upgrade, signature)
  'dd009': "<b>Action de héros</b> : inclinez Doom's Time Platform → choisissez :\n• Redressez Doctor Doom.\n• Mélangez 1 événement ou 1 amélioration de votre pile de défausse dans votre deck.",
  // doctor_doom — Doom's Armor (Upgrade, signature)
  'dd010': "Doctor Doom gagne +3 points de vie et le trait [[AERIAL]].\n<b>Interruption de héros</b> : si Doctor Doom a <b><i>Vilain</i></b>, quand il utilise un pouvoir de base, inclinez Doom's Armor → distribuez-vous 1 carte de boost supplémentaire.",
  // doctor_doom — Doom's Mask (Upgrade, signature)
  'dd011': "Doctor Doom gagne <b><i>Constance</i></b>.\n<b>Ressource</b> : inclinez Doom's Mask → générez une ressource [mental] (plutôt [mental][mental] si vous payez un événement [[SPELL]]).",
  // doctor_doom — Rescue Cynthia von Doom (Obligation)
  'dd012': "<b><i>Donnez-la au joueur Victor von Doom.</i></b>\nPassez sous forme d'alter ego. Vous ne pouvez pas changer de forme.\n• <b>Action d'alter ego</b> : inclinez votre identité et défaussez une carte [[TECH]] que vous contrôlez → retirez cette carte de la partie.\n• <b>Action d'alter ego</b> : inclinez votre identité → défaussez cette carte.",
  // doctor_doom — Incomparable Ego (Obligation)
  'dd013': "<b><i>Donnez-la au joueur Victor von Doom.</i></b>\nInclinez chaque allié que vous contrôlez. Les alliés que vous contrôlez ne peuvent pas se redresser.\n<b>Action d'alter ego</b> : inclinez votre identité et défaussez une carte [mental] de votre main → défaussez cette carte.\n<i>(Icône d'accélération : placez 1 menace supplémentaire sur la manigance principale durant la phase du vilain.)</i>\n<i>(Icône de danger : distribuez +1 carte de rencontre durant la phase du vilain.)</i>\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // doctor_doom — Meddlesome Heroes! (SideScheme nemesis)
  'dd014': "<i>« Mes inventions ont sauvé des mondes, mais la meilleure chose que j'aie jamais bâtie, c'était ma famille. » — Reed Richards</i>\n<b>Une fois vaincue</b> : subissez 4 dégâts indirects ou placez 4 menaces réparties entre les manigances en jeu.\n<i>(Icône de danger : distribuez +1 carte de rencontre durant la phase du vilain.)</i>",
  // doctor_doom — Mister Fantastic (Minion nemesis)
  'dd015': "<b><i>Garde</i></b>. <b><i>Patrouille</i></b>.\nTant que Mister Fantastic est engagé avec vous, chaque fois que vous générez une ressource [mental], générez plutôt une ressource [physical].\n<b>Une fois révélé</b> : Mister Fantastic s'engage avec le joueur Doctor Doom.\n<i>(Sbire némésis de Doctor Doom.)</i>",
  // doctor_doom — Richards! (Treachery nemesis, x2)
  'dd016': "<b>Une fois révélée</b> : Mister Fantastic s'active. Si Mister Fantastic ne s'est pas activé de cette façon, cherchez-le et révélez-le.",

  // alligator_loki — Alligator Loki (Hero)
  'al001a': "L'ennemi attaché gagne -1 MNG et -1 ATQ.\n<i>Lock Jaws</i> — <b>Interruption</b> : quand Alligator Loki effectue une attaque ou une défense de base contre un ennemi, attachez Alligator Loki à cet ennemi.\n<b>Réponse forcée</b> : après que l'ennemi attaché s'est activé, détachez Alligator Loki.",
  // alligator_loki — Alligator Loki (AlterEgo)
  'al001b': "<b>Mise en place</b> : cherchez Throg et ajoutez-le à votre main.\n<i>Nap Time</i> — <b>Réponse forcée</b> : après que vous êtes passé sous cette forme, détachez Alligator Loki. Vous pouvez effectuer une récupération de base sans vous incliner.",
  // alligator_loki — Throg (Minion de joueur, signature)
  'al002': "<b><i>Patrouille</i></b>.\n<b>Interruption</b> : quand Alligator Loki attaque Throg, cette attaque gagne <b><i>Déferlement</i></b>.\n<b>Une fois vaincu</b> : retirez 3 menaces d'une manigance. Mélangez Throg dans le deck du joueur Alligator Loki.",
  // alligator_loki — Chomp! (Event, x4)
  'al003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi (6 dégâts à la place si Alligator Loki est attaché à cet ennemi). Si cette attaque vainc un ennemi, redressez Alligator Loki. Sinon, vous pouvez attacher Alligator Loki à cet ennemi.",
  'al004': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi (6 dégâts à la place si Alligator Loki est attaché à cet ennemi). Si cette attaque vainc un ennemi, redressez Alligator Loki. Sinon, vous pouvez attacher Alligator Loki à cet ennemi.",
  'al005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi (6 dégâts à la place si Alligator Loki est attaché à cet ennemi). Si cette attaque vainc un ennemi, redressez Alligator Loki. Sinon, vous pouvez attacher Alligator Loki à cet ennemi.",
  'al006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi (6 dégâts à la place si Alligator Loki est attaché à cet ennemi). Si cette attaque vainc un ennemi, redressez Alligator Loki. Sinon, vous pouvez attacher Alligator Loki à cet ennemi.",
  // alligator_loki — See You Later! (Event, x2)
  'al007': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Passez sous forme d'alter ego. Vous pouvez mélanger Throg de votre pile de défausse dans votre deck.",
  'al008': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Passez sous forme d'alter ego. Vous pouvez mélanger Throg de votre pile de défausse dans votre deck.",
  // alligator_loki — Alligator Antics (Event, signature)
  'al009': "<b>Action</b> : redressez votre identité. Cherchez le sbire Throg dans n'importe quel deck ou pile de défausse et mettez-le en jeu. Cherchez dans la zone de mise de côté, le deck de rencontre et sa pile de défausse un attachement qui peut être attaché à un sbire, et attachez-le à Throg.",
  // alligator_loki — Loki (Support persona, signature)
  'al010': "Alligator Loki gagne le trait [[MYSTIC]].\nTant que vous êtes sous forme de héros, Alligator Loki gagne +1 CTR.\n<b>Ressource d'alter ego</b> : inclinez Loki → générez une ressource [wild].",
  // alligator_loki — Butterfly Swamp (Support, signature)
  'al011': "Tant que vous êtes sous forme d'alter ego, Alligator Loki gagne +1 REC.\n<b>Action d'alter ego</b> : inclinez Butterfly Swamp → mélangez 1 carte [[PREPARATION]] de votre pile de défausse dans votre deck. Piochez 1 carte.",
  // alligator_loki — Gator Aid (Upgrade, signature)
  'al012': "<b>Interruption</b> : quand le personnage attaché utilise un pouvoir de base, inclinez Gator Aid → ce personnage gagne +1 à ce pouvoir pour cette utilisation. Après cette utilisation, vous pouvez attacher cette carte à un autre personnage ami.",
  // alligator_loki — Unbreakable Grip (Upgrade, signature)
  'al013': "Tant que vous êtes sous forme de héros, Alligator Loki gagne +1 ATQ.\n<b>Interruption de héros</b> : quand vous devriez détacher Alligator Loki d'un ennemi en jeu, inclinez plutôt Unbreakable Grip.",
  // alligator_loki — Lurking (Upgrade, x3)
  'al014': "1 max par joueur.\n<b>Réponse de héros</b> : après qu'un sbire est entré en jeu, défaussez Lurking → Alligator Loki effectue une attaque de base contre ce sbire sans s'incliner. Alligator Loki gagne +1 ATQ pour cette attaque.",
  'al015': "1 max par joueur.\n<b>Réponse de héros</b> : après qu'un sbire est entré en jeu, défaussez Lurking → Alligator Loki effectue une attaque de base contre ce sbire sans s'incliner. Alligator Loki gagne +1 ATQ pour cette attaque.",
  'al016': "1 max par joueur.\n<b>Réponse de héros</b> : après qu'un sbire est entré en jeu, défaussez Lurking → Alligator Loki effectue une attaque de base contre ce sbire sans s'incliner. Alligator Loki gagne +1 ATQ pour cette attaque.",
  // alligator_loki — Time Out (Obligation)
  'al017': "<b><i>Donnez-la au joueur Alligator Loki.</i></b>\nCherchez Frogjolnir dans la zone de mise de côté et mélangez-le dans le deck de rencontre.\nVous gagnez -2 ATQ tant que vous êtes sous forme de héros.\n<b>Action d'alter ego</b> : inclinez votre alter ego → retirez Time Out de la partie.",
  // alligator_loki — Throg and Loki (SideScheme nemesis)
  'al018': "<i>« SMAK ! SHLORP ! RAWR ! KLONK ! SPLOOSH ! »</i>\nAlligator Loki ne peut attaquer que Throg.\n<b>Une fois révélée</b> : si Throg n'est pas en jeu, cherchez-le dans le deck de rencontre et sa pile de défausse et révélez-le.\n<i>(Icône de danger : distribuez +1 carte de rencontre durant la phase du vilain.)</i>",
  // alligator_loki — Throg (Minion nemesis)
  'al019': "<b>Interruption forcée</b> : quand ce sbire devrait entrer en jeu, défaussez tout autre Throg en jeu. Placez ici, face cachée, une carte de votre main au hasard.\n<b>Une fois vaincu</b> : rendez chaque carte face cachée placée ici à la main de son propriétaire.\n<i>(Sbire némésis d'Alligator Loki.)</i>",
  // alligator_loki — Lightning Bolt (Treachery nemesis, x2)
  'al020': "<b>Une fois révélée</b> : défaussez 2 cartes du deck de rencontre. Subissez 1 dégât indirect pour chaque icône de boost défaussée de cette façon.\n<hr />\n[star] <b>Boost</b> : défaussez 3 cartes du deck de rencontre.",
  'al021': "<b>Une fois révélée</b> : défaussez 2 cartes du deck de rencontre. Subissez 1 dégât indirect pour chaque icône de boost défaussée de cette façon.\n<hr />\n[star] <b>Boost</b> : défaussez 3 cartes du deck de rencontre.",
  // alligator_loki — Frogjolnir (Attachment nemesis, mise de côté)
  'al022': "Si Throg n'est pas en jeu, trouvez-le et révélez-le. Attachez cette carte à Throg. Puis Throg s'active contre vous.\nThrog gagne le trait [[AERIAL]].\n[star] <b>Réponse forcée</b> : après que Throg vous a attaqué, subissez 1 dégât indirect.",
  // alligator_loki — Little Rascals (Event Team-Up, carte bonus)
  'al023': "En Équipe (Alligator Loki et Honey Badger/Gabby Kinney). 1 max par deck.\n<b>Action</b> : étourdissez et désorientez le vilain. Si vous ne le pouvez pas, redressez Alligator Loki ou Honey Badger.",

  // hulk_rainy — Hulk (Hero) [set 148, Rainy]
  'hk001a': "<i>Anger</i> — <b>Réponse</b> : après que Hulk a subi des dégâts, infligez 1 dégât à un ennemi.",
  // hulk_rainy — Bruce Banner (AlterEgo)
  'hk001b': "<i>Bring Out The Big Guy</i> — <b>Interruption</b> : quand un ennemi devrait manigancer, dépensez une ressource [physical] → passez sous forme de héros. Cet ennemi vous attaque à la place.",
  // hulk_rainy — Black Widow (Ally)
  'hk002': "[star] <b>Réponse</b> : après que Black Widow a contré, retirez 1 menace d'une AUTRE manigance.\n<b>Action de héros</b> : inclinez Black Widow → passez sous forme d'alter ego.",
  // hulk_rainy — Brilliant Mind (Event, x2)
  'hk003': "<b>Action d'alter ego</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Si vous avez payé cette carte uniquement avec des ressources [mental], choisissez de retirer 2 menaces supplémentaires de cette manigance OU de désorienter un ennemi.",
  // hulk_rainy — Hulk Smash (Event, x2)
  'hk004': "<b>Action de héros</b> : effectuez les attaques suivantes contre LA MÊME cible :\n• <i>(attaque)</i> : infligez 3 dégâts.\n• <i>(attaque)</i> : infligez 3 dégâts.\n• <i>(attaque)</i> : infligez 3 dégâts.",
  // hulk_rainy — Interception (Event, x2)
  'hk005': "<b>Interruption de héros</b> : quand une traîtrise est révélée, subissez 2 dégâts → annulez tous ses effets et défaussez-la. Si vous avez SURPAYÉ cette carte avec une ressource [energy] ou [physical], retirez 2 menaces d'une manigance.",
  // hulk_rainy — Reckless Charge (Event, x2)
  'hk006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 1 dégât à Hulk → infligez 3 dégâts à un ennemi. Si vous avez payé cette carte avec une ressource [physical], cette attaque gagne Déferlement.",
  // hulk_rainy — Natural Genius (Resource)
  'hk007': "Ne dépensez cette carte qu'sous forme d'alter ego.",
  // hulk_rainy — Unnatural Strength (Resource)
  'hk008': "Ne dépensez cette carte qu'sous forme de héros.",
  // hulk_rainy — The Other Guy (Support)
  'hk009': "<b>Réponse d'alter ego</b> <i>(contre)</i> : après avoir changé de forme, retirez 1 menace d'une manigance. <i>(Limite d'une fois par phase.)</i>\n<b>Réponse de héros</b> <i>(attaque)</i> : après avoir changé de forme, infligez 1 dégât à un ennemi. <i>(Limite d'une fois par phase.)</i>",
  // hulk_rainy — Intimidating Roar (Upgrade)
  'hk010': "<b>Réponse de héros</b> <i>(contre)</i> : après que Hulk a subi des dégâts D'UNE ATTAQUE, inclinez Intimidating Roar → retirez 1 menace d'une manigance (2 menaces à la place si vous avez subi 3 dégâts ou plus).",
  // hulk_rainy — Limitless Endurance (Upgrade)
  'hk011': "Vous gagnez +3 points de vie et Bruce Banner gagne +1 REC.\n<b>Action de héros</b> : inclinez Limitless Endurance → soignez 1 dégât de Hulk.",
  // hulk_rainy — Limitless Strength (Upgrade)
  'hk012': "Hulk gagne +1 ATQ.\n<b>Ressource de héros</b> : inclinez Limitless Strength → générez une ressource [physical].",
  // hulk_rainy — Inner Conflict (Obligation)
  'hk013': "<b><i>Donnez-la au joueur Bruce Banner.</i></b>\nChangez de forme (retournez votre identité). Puis :\n• Si vous êtes Bruce Banner, défaussez 1 carte AU HASARD de votre main. Défaussez cette obligation.\n• Si vous êtes Hulk, inclinez votre héros. Défaussez cette obligation.",

  // viv_vision — Viv Vision (Hero) [set 147, Rainy]
  'vv001a': "<i>Density Manipulation</i> — <b>Action</b> : dépensez une ressource [energy] → vous gagnez +2 à un pouvoir de base de votre choix jusqu'à la fin du round. <i>(Limite d'une fois par round.)</i>",
  // viv_vision — Viv Vision (AlterEgo)
  'vv001b': "<i>Recharge</i> — <b>Action</b> : choisissez dans votre pile de défausse une carte portant une ressource [energy] imprimée et placez-la sur le dessus de votre deck. <i>(Limite d'une fois par round.)</i>",
  // viv_vision — Hologram Projection (Event)
  'vv002': "<b><i>Exigence</i></b> ([energy][mental]). <i>(En payant cette carte, dépensez les ressources indiquées.)</i>\n<b>Interruption de héros</b> : quand un ennemi devrait s'activer, annulez cette activation et désorientez cet ennemi.",
  // viv_vision — Just a Phase (Event, x2)
  // ⚠ ECART ASSUME : la carte imprime « Interruption de héros », le moteur la
  // rend en « Action de héros (contre) » — le mot-cle Patrouille est verifie au
  // CHOIX DE LA CIBLE, donc avant toute fenetre d'interruption. Voir l'en-tete
  // de src/cards/pack/viv_vision/viv_vision/vv003.py. Le texte FR ci-dessous
  // decrit ce que la carte FAIT REELLEMENT en jeu, pour ne pas promettre au
  // joueur un declencheur qu'il ne verra jamais.
  'vv003': "<b>Action de héros</b> <i>(contre)</i> : inclinez votre héros → effectuez une menée de base avec +3 CTR, en ignorant le mot-clé Patrouille et l'icône de crise ([crisis]). Cette menée gagne percée.",
  'vv004': "<b><i>Exigence</i></b> ([energy]). <i>(En payant cette carte, dépensez les ressources indiquées.)</i>\n<b>Interruption</b> <i>(défense)</i> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, prévenez la totalité de ces dégâts. Vous gagnez Robuste jusqu'à la fin du round.",
  // viv_vision — Solar Beam (Event, x4)
  'vv005': "<b><i>Exigence</i></b> ([energy]). <i>(En payant cette carte, dépensez les ressources indiquées.)</i>\n<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Cette attaque gagne à distance.\n<b>Action de héros</b> <i>(contre)</i> : retirez 4 menaces d'une manigance.",
  // viv_vision — Superdense Strike (Event, x2)
  'vv006': "<b>Interruption de héros</b> : quand votre héros effectue une attaque de base contre un ennemi, il gagne +4 ATQ pour cette attaque et cette attaque gagne perçant. Donnez une carte d'état Tenace à votre héros.",
  // viv_vision — Sparky the Dog (Support)
  'vv007': "<b>Interruption de héros</b> : quand un sbire déclenche une attaque, inclinez Sparky the Dog → infligez 2 dégâts à ce sbire.\n<b>Action d'alter ego</b> : inclinez Sparky the Dog → soignez 1 dégât de votre identité.",
  // viv_vision — Computer Mind (Upgrade)
  'vv008': "<b>Réponse</b> : après avoir joué une carte portant le mot-clé Exigence, inclinez Computer Mind → piochez 1 carte par ressource exigée sur cette carte.",
  // viv_vision — Insubstantial Flight (Upgrade)
  'vv009': "<b><i>Exigence</i></b> ([energy]). <i>(En payant cette carte, dépensez les ressources indiquées.)</i>\nVous gagnez le trait [[AERIAL]].\n<b>Réponse de héros</b> : après que votre héros s'est incliné, inclinez Insubstantial Flight → redressez votre héros.",
  // viv_vision — Viv's Solar Gem (Upgrade)
  'vv010': "<b>Ressource</b> : inclinez Viv's Solar Gem → générez une ressource [energy].\n<b>Réponse</b> : après la fin de la phase du Méchant, redressez Viv's Solar Gem.",
  // viv_vision — Grounded (Obligation)
  'vv011': "<b><i>Donnez-la au joueur Viv Vision.</i></b>\nPassez sous forme d'alter ego.\nVous ne pouvez pas changer de forme.\n<b>Action d'alter ego</b> : inclinez votre alter ego → retirez Grounded de la partie.",

  // lady_sif — Lady Sif (Hero) [set 150, Rainy]
  'ls001a': "<i>Valiant Warrior</i> — <b>Réponse</b> <i>(contre)</i> : après que Lady Sif a utilisé un pouvoir de base, retirez 1 menace d'une manigance.",
  // lady_sif — Lady Sif (AlterEgo)
  'ls001b': "<i>Shieldmaiden</i> — <b>Action</b> : redressez un personnage [[ASGARD]] amical. <i>(Limite d'une fois par round.)</i>",
  // lady_sif — Thor, Odinson (Ally)
  'ls002': "[star] <b>Réponse</b> : après que Thor a attaqué, choisissez un joueur. Infligez 1 dégât à chaque sbire engagé avec ce joueur.",
  // lady_sif — Impale (Event, x2)
  'ls003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 6 dégâts à un ennemi. Choisissez de faire gagner à cette attaque SOIT Déferlement, SOIT Perçant.",
  // lady_sif — Lead The Charge (Event, x3)
  'ls004': "<b>Action de héros</b> <i>(attaque)</i> : Lady Sif effectue une attaque de base SANS s'incliner. Choisissez un AUTRE personnage amical. Ce personnage gagne +1 ATQ jusqu'à la fin du round.",
  // lady_sif — To Arms! (Event)
  'ls005': "<b>Action d'alter ego</b> : passez sous forme de héros. Vous pouvez dépenser 1 ressource pour redresser votre héros.\n<b>Action de héros</b> : cherchez une amélioration [[WEAPON]] dans votre deck ET dans votre défausse, et ajoutez-la à votre main. Mélangez votre deck.",
  // lady_sif — Valiant Defense (Event, x3)
  'ls006': "<b>Interruption de héros</b> <i>(défense)</i> : quand un ennemi attaque, effectuez une défense de base SANS incliner votre héros. Vous gagnez +1 DEF pour cette attaque (+2 DEF à la place si vous avez payé cette carte avec une ressource [energy]).",
  // lady_sif — Sif's Chambers (Support)
  'ls007': "<b>Action d'alter ego</b> : inclinez Sif's Chambers → soignez 1 dégât de Lady Sif. Soignez 1 dégât de Thor ou d'Odinson. Choisissez une carte Lady Sif dans votre défausse et mélangez-la dans votre deck.",
  // lady_sif — Sif's Steed (Support)
  'ls008': "<b>Réponse de héros</b> : après que Lady Sif s'est inclinée, inclinez Sif's Steed → redressez Lady Sif.\n<b>Action de héros</b> : inclinez Sif's Steed → redressez Lady Sif.",
  // lady_sif — Sif's Crest (Upgrade)
  'ls009': "Vous gagnez +2 points de vie.\n<b>Interruption de héros</b> : quand Lady Sif utilise un pouvoir de base, piochez 1 carte. <i>(Limite d'une fois par phase.)</i>",
  // lady_sif — Sif's Spear (Upgrade)
  'ls010': "<b><i>Restreinte.</i></b>\nLady Sif gagne +1 DEF sous forme de héros et gagne Riposte 1.",
  // lady_sif — Sif's Sword (Upgrade)
  'ls011': "<b><i>Restreinte.</i></b>\nLady Sif gagne +1 ATQ sous forme de héros. Sous forme de héros, les attaques de BASE de Lady Sif gagnent Perçant.",
  // lady_sif — Unrequited Love (Obligation)
  'ls012': "<b><i>Donnez-la au joueur Lady Sif.</i></b>\nVous pouvez passer sous forme d'alter ego.\nÉtourdissez Lady Sif. Étourdissez OU désorientez Thor. Si vous ne le pouvez pas, désorientez Lady Sif. Défaussez cette obligation.",
  // lady_sif_nemesis — Captivating Wiles (SideScheme)
  'ls013': "<i>L'Enchanteresse nous manipule pour que nous fassions son sale travail !</i>\n<b>Interruption forcée</b> : quand la phase du joueur commence, inclinez l'identité du PREMIER joueur et placez 2 menaces sur la manigance principale.\n<hr />[star] <b>Boost</b> : placez 2 menaces sur la manigance principale.",
  // lady_sif_nemesis — Enchantress (Minion)
  'ls014': "<b>Interruption forcée</b> : quand Enchantress est attaquée, déclarez le héros engagé défenseur (sans l'incliner). Si vous ne le pouvez pas, annulez cette attaque et placez 2 menaces sur la manigance principale à la place. <i>(Limite d'une fois par phase.)</i>\n<i>(Sbire némésis de Lady Sif.)</i>",
  // lady_sif_nemesis — Skurge (Minion)
  'ls015': "<b><i>Travail d'équipe</i></b> ([[ASGARD]]). <b><i>Robustesse.</i></b>\n[star] <b>Interruption forcée</b> : quand Skurge vous attaque, il attaque le personnage que VOUS contrôlez ayant le moins de points de vie restants. Cette attaque gagne Déferlement et Perçant.\n<hr />[star] <b>Boost</b> : détruisez un allié que vous contrôlez.",
  // lady_sif_nemesis — Hypnotic Suggestion (Attachment)
  'ls016': "Attachez-la à votre identité.\n<b>Action forcée</b> : inclinez cette carte → piochez 1 carte, puis jouez cette carte (en payant son coût). Si vous ne le pouvez pas, placez 2 menaces sur la manigance principale.\n<b>Action d'alter ego</b> : inclinez cette carte et dépensez une ressource [mental] → défaussez cette carte.",
  // lady_sif_nemesis — Love Concoction (Attachment)
  'ls017': "Attachez-la à votre identité.\n<b>Action forcée</b> : inclinez cette carte et donnez au méchant une carte de boost face cachée → redressez votre identité.\n<b>Action d'alter ego</b> : inclinez cette carte et donnez au méchant une carte de boost face cachée → défaussez cette carte.\n<hr />[star] <b>Boost</b> : révélez cette carte.",

  // iron_man_model_42 — Iron Man (Hero) [set 151, Rainy]
  'im001a': "<i>Reactor Cores</i> — <b>Action</b> : dépensez X ressources [energy] IMPRIMÉES → placez X pions réacteur ici.",
  // iron_man_model_42 — Tony Stark (AlterEgo)
  'im001b': "<i>Inventor</i> — <b>Mise en place</b> : défaussez 1 carte de votre main → cherchez une amélioration [[TECH]] dans votre deck et ajoutez-la à votre main.\n<b>Action</b> : réduisez de 1 le coût de la prochaine amélioration jouée ce round. <i>(Limite d'une fois par round.)</i>",
  // iron_man_model_42 — Repulsor Barrage (Event, x2)
  'im002': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Cette attaque gagne Portée. Vous pouvez retirer 1 pion réacteur d'Iron Man pour infliger 3 dégâts supplémentaires à CET ennemi. Si Iron Man a le trait [[AERIAL]], vous pouvez répartir les dégâts entre les ennemis comme vous voulez.",
  // iron_man_model_42 — Tactical Overview (Event, x2)
  'im003': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Vous pouvez retirer 1 pion réacteur d'Iron Man pour retirer 3 menaces supplémentaires de CETTE manigance. Si Iron Man a le trait [[AERIAL]], vous pouvez répartir les menaces retirées entre les manigances comme vous voulez.",
  // iron_man_model_42 — Take Flight (Event, x3)
  'im004': "<b>Action de héros</b> : redressez Iron Man. Iron Man gagne le trait [[AERIAL]] jusqu'à la fin du round. Si Iron Man a DÉJÀ [[AERIAL]], placez 1 pion réacteur sur Iron Man.",
  // iron_man_model_42 — Stark Tower (Support)
  'im005': "<b>Ressource</b> : inclinez Stark Tower → générez une ressource [wild] pour n'importe quel joueur.",
  // iron_man_model_42 — Tony's Workshop (Support)
  'im006': "<b>Action d'alter ego</b> : inclinez Tony's Workshop → soignez 1 dégât de Tony Stark et placez 1 pion réacteur sur lui.",
  // iron_man_model_42 — Energy Shield (Upgrade)
  'im007': "Iron Man gagne +1 DEF.\n<b>Interruption de héros</b> : quand Iron Man devrait subir des dégâts, quels qu'ils soient, retirez-lui 1 pion réacteur → prévenez jusqu'à 2 de ces dégâts.",
  // iron_man_model_42 — Mark IVa Repulsors (Upgrade)
  'im008': "<b>Interruption de héros</b> : quand Iron Man effectue une attaque de BASE, retirez-lui 1 pion réacteur → cette attaque inflige 2 dégâts supplémentaires et gagne Portée.",
  // iron_man_model_42 — Repulsor Core One (Upgrade)
  'im009': "<b>Action de héros</b> : inclinez Repulsor Core One → placez 1 pion réacteur sur Iron Man.\n<b>Action de héros</b> : retirez 1 pion réacteur d'Iron Man et inclinez Repulsor Core One → redressez Iron Man.",
  // iron_man_model_42 — Rocket Boots (Upgrade)
  'im010': "Iron Man gagne le trait [[AERIAL]].\n<b>Interruption de héros</b> : quand vous utilisez l'un des pouvoirs de base d'Iron Man, inclinez Rocket Boots → Iron Man gagne +1 à CE pouvoir pour cette utilisation.",
  // iron_man_model_42 — Save The Day (Upgrade)
  'im011': "<b>Interruption de héros</b> : quand une traîtrise est révélée, défaussez Save The Day et retirez 1 pion réacteur d'Iron Man → annulez tous les effets de cette traîtrise et défaussez-la.",
  // iron_man_model_42 — Hulkbuster Armor (Upgrade, variante de im011)
  'im012': "Iron Man gagne -1 carte en main, +1 ATQ et +1 DEF, et ses attaques de BASE gagnent Déferlement.\n<b>Interruption</b> : quand Iron Man devrait subir des dégâts, quels qu'ils soient, retirez cette carte de la partie → prévenez TOUS ces dégâts.",
  // iron_man_model_42 — Tactical Interface (Upgrade)
  'im013': "<b>Interruption de héros</b> : quand Iron Man effectue une menée de BASE, retirez-lui 1 pion réacteur → cette menée retire 2 menaces supplémentaires et ignore le mot-clé Patrouille.",
  // iron_man_model_42 — Technical Issues (Obligation)
  'im014': "<b><i>Donnez-la au joueur Tony Stark.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Tony Stark ET Tony's Workshop → retirez Technical Issues de la partie.\n• Retirez 2 pions réacteur de votre identité. Si AUCUN pion réacteur n'a été retiré de cette façon, cette carte gagne Déchaînement. Défaussez cette obligation.",
  // armored_spidey — Armored Spidey (Hero) [set 152, Kajislav]
  'as001a': "<i>Armor Protection</i> — <b>Interruption</b> : quand vous devriez subir des dégâts, quels qu'ils soient, provenant d'une attaque, retirez 1 pion métal de Spider Armor → prévenez jusqu'à 2 de ces dégâts.",
  // armored_spidey — Peter Parker (AlterEgo)
  'as001b': "<b>Mise en place</b> : mettez en jeu votre amélioration Spider Armor, face [[OPERATIONAL]] visible. Placez 3 pions métal dessus.\n<i>Egomaniac</i> — <b>Réponse</b> : après qu'un joueur a joué une carte sous VOTRE contrôle, piochez 1 carte <i>(limite d'une fois par round et par joueur)</i>.",
  // armored_spidey — Spider Armor, face OPERATIONAL (Upgrade permanente)
  'as002a': "Permanente.\n<b>Réponse forcée</b> : après que vous êtes passé sur cette face, placez 3 pions métal ici.\n<b>Réponse forcée</b> : après que le DERNIER pion métal a été retiré d'ici, retournez cette carte.",
  // armored_spidey — Spider Armor, face DESTROYED (Upgrade permanente)
  'as002b': "Permanente.\nArmored Spidey gagne -1 ATQ et -1 DEF.\n<b>Action d'alter ego</b> : dépensez 3 ressources de n'importe quel type → retournez cette carte.",
  // armored_spidey — Spider-Bot (Ally)
  'as003': "<b><i>Robustesse.</i></b>\n<b>Action</b> : défaussez Spider-Bot → retournez votre amélioration Spider Armor sur sa face [[OPERATIONAL]].",
  // armored_spidey — Burst It! (Event)
  'as004': "<b>Action de héros</b> : retirez TOUS les pions métal de Spider Armor → infligez 1 dégât à CHAQUE ennemi en jeu par pion métal retiré de cette façon.",
  // armored_spidey — Embrace It! (Event, x2)
  'as005': "<b>Réponse</b> : après que vous avez retiré un pion métal de Spider Armor, redressez votre identité.",
  // armored_spidey — Kick It! (Event, x2)
  'as006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Vous pouvez retirer 1 pion métal de Spider Armor pour étourdir CET ennemi.",
  // armored_spidey — Sell It! (Event)
  'as007': "<b>Action d'alter ego</b> : retirez autant de pions métal que vous voulez de Spider Armor. Piochez 2 cartes par pion métal retiré de cette façon.",
  // armored_spidey — Sense It! (Event, x2)
  'as008': "<b>Interruption de héros</b> : quand une carte de traîtrise est révélée depuis le deck de rencontre, annulez tous ses effets et défaussez-la. Vous pouvez retirer 1 pion métal de Spider Armor → infligez 1 dégât au méchant OU retirez 1 menace de la manigance principale par icône de boost défaussée de cette façon.",
  // armored_spidey — Swing It! (Event, x2)
  'as009': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Vous pouvez retirer 1 pion métal de Spider Armor pour désorienter un ennemi.",
  // armored_spidey — Gwen Stacy (Support)
  'as010': "<b>Réponse</b> : après qu'une carte de coût IMPRIMÉ 2 ou plus est entrée en jeu sous votre contrôle, redressez Gwen Stacy. <i>(Limite d'une fois par round.)</i>\n<b>Ressource</b> : inclinez Gwen Stacy → générez une ressource [wild].",
  // armored_spidey — Parker Industries (Support)
  'as011': "<b>Action d'alter ego</b> : inclinez Parker Industries → regardez les 3 premières cartes de votre deck. Ajoutez-en 1 à votre main et défaussez les autres.",
  // armored_spidey — Night Vision (Upgrade)
  'as012': "Tant que Spider Armor a le trait [[OPERATIONAL]], Armored Spidey gagne +1 CTR et ignore les mots-clés Garde et Patrouille.",
  // armored_spidey — Vibranium Enhancement (Upgrade)
  'as013': "Tant que Spider Armor a le trait [[OPERATIONAL]], Armored Spidey gagne Riposte 1 et Stoïque.\n<b>Réponse</b> : après avoir joué cette carte, si Spider Armor a le trait [[OPERATIONAL]], placez 1 pion métal dessus <i>(maximum 3)</i>.",
  // armored_spidey — Corporate Expansion (Obligation)
  'as014': "<b><i>Donnez-la au joueur Peter Parker.</i></b>\nVous ne pouvez pas jouer de cartes d'ÉVÉNEMENT tant que vous êtes sous forme de héros.\n<b>Réponse d'alter ego</b> : après qu'une carte de coût IMPRIMÉ 2 ou plus est entrée en jeu sous votre contrôle, défaussez cette obligation.",
  // armored_spidey — Scarlet Spider (Ally, Protection)
  'as015': "Scarlet Spider entre en jeu avec 3 pions sens sur lui.\n<b>Interruption</b> : quand le méchant s'active contre vous, retirez 1 pion sens de Scarlet Spider → réduisez de 1 le nombre d'icônes de boost ([boost]) de CHAQUE carte de boost pour cette activation.",
  // armored_spidey — Six-Armed Spider-Man (Ally, Protection)
  'as016': "<b>Réponse</b> : après que Six-Armed Spider-Man s'est défendu contre une attaque, défaussez les 6 premières cartes de votre deck. Infligez 1 dégât à l'ennemi attaquant par type de carte DIFFÉRENT défaussé de cette façon.",
  // armored_spidey — Defensive Briefing (Event, Protection, x2)
  'as017': "<b>Action de héros</b> : choisissez jusqu'à X héros. Chaque héros choisi gagne +3 DEF jusqu'à la fin du round.",
  // armored_spidey — Just a Ricochet (Event, Protection, x2)
  'as018': "Jouable seulement si vous contrôlez une amélioration [[ARMOR]].\n<b>Réponse de héros</b> <i>(attaque)</i> : après que votre héros a effectué une défense de base et n'a subi AUCUN dégât, infligez à un ennemi un nombre de dégâts égal à la DEF de votre héros.",
  // armored_spidey — The Daily Bugle (Support, Protection)
  'as019': "<b>Réponse</b> : après qu'un personnage ou une manigance annexe a été vaincu, inclinez The Daily Bugle → placez 1 pion article ici.\n<b>Action d'alter ego</b> : retirez TOUS les pions article d'ici → soignez 1 dégât d'un personnage que vous contrôlez par pion article retiré de cette façon.",
  // armored_spidey — Double Defense (Upgrade, Protection, x2)
  'as020': "1 max par joueur.\n<b>Interruption de héros</b> : quand un personnage AUTRE que votre identité devrait subir des dégâts, quels qu'ils soient, provenant d'une attaque, défaussez Double Defense → réduisez ce montant de la DEF de votre héros.",
  // armored_spidey — Octo Spidey (Ally, Basic)
  'as021': "[star] <b>Interruption</b> : quand Octo Spidey utilise un pouvoir de base, défaussez les 4 premières cartes de votre deck. Octo Spidey gagne +1 à CE pouvoir pour cette utilisation par type de ressource DIFFÉRENT défaussé de cette façon.",
  // armored_spidey — Spider-Verse (Support, Basic)
  'as022': "Jouable seulement si votre identité a le trait [[WEB-WARRIOR]] ou « Spider » dans son titre.\nAugmentez de 1 votre limite d'alliés.\n<b>Ressource</b> : inclinez Spider-Verse → générez une ressource [energy] pour un allié ayant le trait [[WEB-WARRIOR]] ou « Spider » dans son titre, pour n'importe quel joueur.",
  // armored_spidey_nemesis — Kingpin (Minion)
  'as023': "[star] <b>Réponse forcée</b> : après que Kingpin a manigancé, défaussez la première carte du deck de rencontre, puis placez 1 menace sur la manigance annexe « The Kingpin of Crime » par icône de boost défaussée de cette façon.\n<i>(Sbire némésis d'Armored Spidey.)</i>",
  // armored_spidey_nemesis — "The Kingpin of Crime" (SideScheme)
  'as024': "<b><i>Entrave 1.</i></b>\nTraitez la zone de texte imprimée de CHAQUE soutien NON permanent comme si elle était vierge.",
  // armored_spidey_nemesis — Underworld Impact (Treachery, x2)
  'as025': "<b>Une fois révélée</b> : choisissez de subir 1 dégât OU de placer 1 menace sur la manigance principale, par soutien que vous contrôlez. Si vous ne contrôlez AUCUN soutien, cette carte gagne Déchaînement.\n<hr />[star] <b>Boost</b> : cette carte gagne +1 icône de boost ([boost]) par soutien que vous contrôlez.",
  // armored_spidey_nemesis — Behind the Scenes (Treachery)
  'as026': "<b>Une fois révélée</b> : défaussez la première carte de votre deck. Puis défaussez de votre main CHAQUE carte du même type que la carte défaussée. Si AUCUNE carte n'a été défaussée de votre main de cette façon, cette carte gagne Déchaînement.",
  // night_thrasher — Night Thrasher (Hero) [set 153, DESIGNHACKER]
  'nt001a': "<i>Varial Heelflip</i> — <b>Réponse</b> : après avoir joué une carte [[SKILL]], retournez l'amélioration Battle Board. <i>(Limite d'une fois par phase.)</i>",
  // night_thrasher — Dwayne Taylor (AlterEgo)
  'nt001b': "<i>Tech Deck</i> — Pendant la construction de deck, vous pouvez inclure jusqu'à 4 cartes [[SKILL]] d'aspects AUTRES que le vôtre.\n<i>Manual</i> — <b>Action</b> : remélangez X cartes [[SKILL]] de votre main dans votre deck → piochez X cartes. <i>(Limite d'une fois par round.)</i>",
  // night_thrasher — Disaster (Event, x2)
  'nt002': "<b>Action de héros</b> <i>(attaque/contre)</i> : retournez l'amélioration Battle Board. PUIS, si elle a le trait :\n• [[VEHICLE]], retirez 3 menaces d'une manigance.\n• [[WEAPON]], infligez 4 dégâts à un ennemi.",
  // night_thrasher — Battle Board, face VEHICLE (Upgrade permanente)
  'nt003a': "Permanente. Mise en place.\nNight Thrasher gagne +1 CTR et Agile 1 <i>(réduit de 1 les dégâts des attaques accompagnées de cartes de boost)</i>.\n<b>Réponse</b> : après que vous êtes passé sur cette face, retirez 1 menace d'une manigance.",
  // night_thrasher — Battle Board, face WEAPON (Upgrade permanente)
  'nt003b': "Permanente.\nNight Thrasher gagne +1 ATQ et +1 DEF.\n<b>Réponse de héros</b> : après que vous êtes passé sur cette face, infligez 1 dégât à un ennemi.",
  // night_thrasher — Drop In (Event, x2)
  'nt004': "<b>Réponse de héros</b> : après être passé en forme de HÉROS, si l'amélioration Battle Board a le trait :\n• [[VEHICLE]], désorientez un ennemi.\n• [[WEAPON]], étourdissez un ennemi.",
  // night_thrasher — Kickflip (Event, x4)
  'nt005': "Si la DERNIÈRE carte que vous avez jouée ce round était un événement Night Thrasher, réduisez de 1 le coût de cette carte.\n<b>Action de héros</b> <i>(attaque)</i> : retournez l'amélioration Battle Board ET infligez 1 dégât à un ennemi. Piochez 1 carte.",
  // night_thrasher — Melon Grab (Event)
  'nt006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 8 dégâts à un ennemi. Si l'amélioration Battle Board a le trait :\n• [[VEHICLE]], les dégâts de cette attaque peuvent être répartis entre les ennemis comme vous voulez.\n• [[WEAPON]], cette attaque gagne Perçant et Déferlement.",
  // night_thrasher — Tailblock (Event, x2)
  'nt007': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts, quels qu'ils soient, si l'amélioration Battle Board a le trait :\n• [[VEHICLE]], prévenez 1 de ces dégâts et piochez 2 cartes.\n• [[WEAPON]], prévenez 3 de ces dégâts.",
  // night_thrasher — The Mancave (Support)
  'nt008': "<b>Réponse d'alter ego</b> : après avoir changé de forme, soignez 1 dégât de votre identité.\n<b>Réponse de héros</b> : après avoir changé de forme, réduisez de 1 le coût en ressources de la PROCHAINE carte [[SKILL]] que vous jouez ce tour.",
  // night_thrasher — Escrima Sticks (Upgrade)
  'nt009': "Tant que l'amélioration Battle Board a le trait [[VEHICLE]], vos attaques gagnent Perçant et Déferlement.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 6 dégâts à un ennemi. Remélangez cette carte dans votre deck.",
  // night_thrasher — Multi-Skilled (Upgrade)
  'nt010': "<b>Ressource</b> : inclinez Multi-Skilled → générez une ressource [wild] pour une carte [[SKILL]].",
  // night_thrasher — Prewind Stance (Upgrade)
  'nt011': "Night Thrasher gagne +1 DEF et Riposte 1.\n<b>Interruption de héros</b> : quand votre tour OU la phase du méchant commence, inclinez Prewind Stance → retournez l'amélioration Battle Board.",
  // night_thrasher_nemesis — Practice (Obligation)
  'nt012': "<b><i>Donnez-la au joueur Night Thrasher.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez votre identité OU défaussez 1 carte de votre main → retirez Practice de la partie.\n• Vous ne pouvez pas retourner l'amélioration Battle Board jusqu'au début de la prochaine phase du méchant. Défaussez cette obligation.",
  // night_thrasher_nemesis — Terrax the Tamer (Minion)
  'nt013': "<b>Réponse forcée</b> : après que Terrax the Tamer s'est activé, défaussez les 8 premières cartes du deck de rencontre. Si l'attachement Cosmic Ax a été défaussé de cette façon, révélez-le.\n<i>(Sbire némésis de Night Thrasher.)</i>",
  // night_thrasher_nemesis — Cemented (SideScheme)
  'nt014': "<b><i>Entrave 1[per_hero].</i></b>\nLes joueurs ne peuvent pas effectuer d'attaque de BASE avec un héros ou un allié, ni retourner d'améliorations ou d'identités.\n<b>Action</b> : chaque joueur PEUT défausser 1 carte de sa main → jusqu'à la fin de la phase, chaque joueur ayant défaussé une carte de cette façon peut traiter la zone de texte imprimée de cette carte comme si elle était vierge.",
  // night_thrasher_nemesis — Cosmic Connection (Treachery, x2)
  'nt015': "<b>Une fois révélée</b> : si l'attachement Cosmic Ax est en jeu ET que votre héros contrôle une carte [[WEAPON]], subissez 3 dégâts INDIRECTS. Si AUCUN dégât n'a été subi de cette façon, cette carte gagne Déchaînement.",
  // night_thrasher_nemesis — Cosmic Ax (Attachment)
  'nt016': "Attachez-le à Terrax the Tamer. Si vous ne le pouvez pas, défaussez les 8 premières cartes du deck de rencontre. Si Terrax the Tamer a été défaussé de cette façon, révélez-le et attachez-lui Cosmic Ax.\n<hr />[star] <b>Boost</b> : si Terrax the Tamer est en jeu, révélez cette carte.",
  // yondu — Yondu (Hero) [set 154, BLUEHG + DESIGNHACKER]
  'yd001a': "<i>D'ast Whistlin'</i> — <b>Interruption</b> : quand l'amélioration Yaka Arrow est attachée à un ennemi OU en est retirée, infligez 1 dégât à CET ennemi. Quand elle est attachée à votre identité, soignez 1 dégât de Yondu.",
  // yondu — Yondu Udonta (AlterEgo)
  'yd001b': "<i>Crew Cut</i> — <b>Action</b> : convoquez l'amélioration Tahlei et ajoutez-la à votre main. <i>(Limite d'une fois par round.)</i>\n<i>Whistlin'</i> — <b>Action</b> : inclinez Yondu Udonta → convoquez l'amélioration Yaka Arrow et ajoutez-la à votre main.\n<i>(« Convoquer » = fouiller votre deck ET votre défausse pour la carte nommée.)</i>",
  // yondu — Cheap Shot (Event)
  'yd002': "<b>Action de héros</b> <i>(attaque)</i> : étourdissez un ennemi. PUIS, si CET ennemi a l'amélioration Yaka Arrow attachée, infligez-lui 6 dégâts.",
  // yondu — Fight Dirty (Event)
  'yd003': "<b>Action de héros</b> <i>(attaque)</i> : désorientez un ennemi. PUIS, si CET ennemi a l'amélioration Yaka Arrow attachée, infligez-lui 6 dégâts.",
  // yondu — Whistle While You Work (Event, x2)
  'yd004': "<b>Action de héros</b> : attachez l'amélioration Yaka Arrow à Yondu → redressez Yondu ET l'amélioration Tahlei. Si l'amélioration Yaka Arrow n'est PAS en jeu, convoquez-la et ajoutez-la à votre main À LA PLACE.",
  // yondu — Tough Motherlover (Event)
  'yd005': "<b>Action</b> : donnez une carte de statut Tenace à votre identité. PUIS, si vous avez l'amélioration Yaka Arrow EN MAIN, piochez une carte.",
  // yondu — Twirlin' and Whirlin' (Event, x4)
  'yd006': "Vous pouvez répéter cette capacité pour chaque ressource surpayée pour cette carte.\n<b>Action de héros</b> : attachez l'amélioration Yaka Arrow à un ennemi ou à votre identité.",
  // yondu — Jackpot! (Resource)
  'yd007': "<b>Réponse</b> : après avoir dépensé cette carte, traitez la PROCHAINE carte que vous dépensez comme si elle avait le DOUBLE de ressources.",
  // yondu — Ravager Redshirts (Support)
  'yd008': "<b>Interruption de héros</b> : quand vous devriez subir des dégâts, quels qu'ils soient, d'un ennemi ayant l'amélioration Yaka Arrow attachée, inclinez Ravager Redshirts → prévenez jusqu'à 2 de ces dégâts.",
  // yondu — Invest (Upgrade)
  'yd009': "<b>Action de héros</b> : inclinez Invest et dépensez 2 ressources ou plus de votre main → si le nombre de ressources dépensées de cette façon était de :\n• 2 — attachez l'amélioration Yaka Arrow à un ennemi ou à votre identité.\n• 3 — redressez Yondu et l'amélioration Tahlei.\n• 4 ou plus — piochez 5 cartes.",
  // yondu — Ravage (Upgrade)
  'yd010': "Les sbires portant un pion blessure gagnent le mot-clé Fragile. <i>(Les attaques contre un personnage fragile gagnent Déferlement.)</i>\n<b>Réponse de héros</b> : après que l'amélioration Yaka Arrow a été attachée à un SBIRE, inclinez Ravage → placez un pion blessure sur CE sbire.",
  // yondu — Tahlei (Upgrade)
  'yd011': "<b>Action de héros</b> : inclinez Tahlei → si l'amélioration Yaka Arrow est EN JEU, attachez-la à un ennemi, à votre identité, ou ajoutez-la à votre main.",
  // yondu — Yaka Arrow (Upgrade)
  'yd012': "La Yaka Arrow ne peut être attachée à une carte que si elle est EN JEU. Tant qu'elle est attachée à Yondu, il gagne +1 CTR et +1 ATQ.\n<b>Interruption forcée</b> : quand l'ennemi auquel elle est attachée devrait être vaincu, attachez la Yaka Arrow à un ennemi, à votre identité, ou ajoutez-la à votre main.",
  // yondu — Banished (Obligation)
  'yd013': "<b><i>Donnez-la au joueur Yondu Udonta.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez votre alter ego → retirez Banished de la partie.\n• Défaussez l'amélioration Yaka Arrow ET inclinez l'amélioration Tahlei. Défaussez cette obligation.",
  // yondu_nemesis — Price on Your Head (SideScheme)
  'yd014': "<b>Réponse forcée</b> : après qu'un personnage AMICAL a été vaincu, soignez 1 dégât de Sav'rkk. Si Sav'rkk n'est PAS en jeu, soignez 1 dégât du méchant À LA PLACE.",
  // yondu_nemesis — Sav'rkk (Minion)
  'yd015': "Les améliorations ne peuvent PAS être retirées de Sav'rkk.\n<b>Une fois révélé</b> : convoquez l'attachement Sword-Gun-Arm et attachez-le à Sav'rkk.\n<i>(Sbire némésis de Yondu.)</i>",
  // yondu_nemesis — Sword-Gun-Arm (Attachment)
  'yd016': "Attachez-le à Sav'rkk. Si vous ne le pouvez pas, attachez-le au sbire ayant la plus forte ATQ. Si vous ne le pouvez pas, cette carte gagne Déchaînement.\n[star] Les attaques du personnage auquel il est attaché gagnent Déferlement.\n<b>Réponse forcée</b> : quand le personnage auquel il est attaché a 2 points de vie restants ou moins, défaussez Sword-Gun-Arm.",
  // yondu_nemesis — Hard to Kill (Treachery)
  'yd017': "<b>Une fois révélée</b> : si Sav'rkk est en jeu, il soigne 2 dégâts. SINON, convoquez Sav'rkk et révélez-le.\n<hr />[star] <b>Boost</b> : le MÉCHANT soigne 2 dégâts.",
  // yondu_nemesis — Savage Destruction (Treachery)
  'yd018': "<b>Une fois révélée</b> : si Sav'rkk est en jeu, il vous ATTAQUE. SINON, convoquez Sav'rkk et révélez-le.",
  // doctor_druid — * Doctor Druid (Hero) [set 155, Kajislav]
  'dr001a': "<i>Rituel druidique</i> — <b>Action</b> : subissez 1 dégât → jouez l'événement le plus haut de votre défausse portant une capacité « Action » ou « Action de héros » <i>(en payant son coût)</i>. <i>(Limite d'une fois par round.)</i>",
  // doctor_druid — * Anthony Druid (AlterEgo)
  'dr001b': "<i>Soins psychiatriques</i> — <b>Interruption</b> : quand un personnage amical effectue une récupération de base, il gagne +X REC, où X est égal à la REC d'Anthony Druid.",
  // doctor_druid — * Doctor Strange (Ally)
  'dr002': "Tant que cette carte est dans votre MAIN, Doctor Druid ignore le mot-clé Garde, le mot-clé Patrouille et l'icône de crise ([crisis]).\n<b>Réponse</b> : après que Doctor Strange attaque ou contre, rendez à votre main l'événement le plus haut de votre défausse.",
  // doctor_druid — * Ancient One (Support)
  'dr003': "Tant que cette carte est dans votre MAIN, vos attaques de base gagnent Déferlement, Perçant et Portée.\n<b>Action d'alter ego</b> : inclinez Ancient One → regardez les 3 premières cartes de votre deck, ajoutez chaque carte Doctor Druid à votre main et défaussez les autres.",
  // doctor_druid — Fellow Druid (Support, x2)
  'dr004': "Tant que cette carte est dans votre MAIN, vous gagnez +1 en taille de main.\n<b>Ressource</b> : inclinez Fellow Druid → générez une ressource [wild] pour une carte Doctor Druid.",
  // doctor_druid — Astral Travel (Event, x2)
  'dr005': "Tant que cette carte est dans votre MAIN, vos contres retirent 1 menace supplémentaire.\n<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance.",
  // doctor_druid — Awaken Nature (Event, x2)
  'dr006': "Tant que cette carte est dans votre MAIN, Doctor Druid gagne Représailles 1.\n<b>Action de héros</b> <i>(attaque/contre)</i> : infligez 1 dégât à chaque ennemi et retirez 1 menace de chaque manigance.",
  // doctor_druid — Elemental Control (Event, x2)
  'dr007': "Tant que cette carte est dans votre MAIN, vos attaques infligent 1 dégât supplémentaire.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi.",
  // doctor_druid — Mystical Protection (Event, x2)
  'dr008': "Tant que cette carte est dans votre MAIN, chaque personnage que vous contrôlez gagne Inébranlable.\n<b>Interruption de héros</b> : quand une carte de rencontre devrait être révélée, défaussez-la à la place. S'il n'y a aucune icône de boost ([boost]) sur cette carte, donnez une carte de statut Tenace à un personnage amical.",
  // doctor_druid — Practice of Druidry (Event, x3)
  'dr009': "Tant que cette carte est dans votre MAIN, votre identité gagne +1 à chacun de ses pouvoirs de base.\n<b>Action de héros</b> : redressez Doctor Druid.",
  // doctor_druid — Ancient Order of Druids (Obligation)
  'dr010': "<b><i>Donnez-la au joueur Anthony Druid.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Anthony Druid → retirez Ancient Order of Druids de la partie.\n• Défaussez chaque événement spécifique à l'identité de votre main. Si aucun événement n'a été défaussé de cette façon, cette carte gagne Renfort. Défaussez cette obligation.",
  // doctor_druid_nemesis — * Nekra (Minion)
  'dr011': "Nekra gagne +1 ATQ et +1 PV pour chaque pion haine sur elle.\n<b>Réponse forcée</b> : après que Nekra attaque ou subit des dégâts, placez 1 pion haine sur elle <i>(maximum 5)</i>.\n<i>(Sbire némésis de Doctor Druid.)</i>",
  // doctor_druid_nemesis — Harness Violent Emotions (SideScheme)
  'dr012': "<i>Plus les émotions de Nekra sont violentes, plus elle devient forte.</i>\n<b>Une fois révélée</b> : cherchez Nekra dans le deck ET la défausse de rencontre, et révélez-la.\n<b>Interruption forcée</b> : quand Nekra vous attaque, défaussez 1 carte spécifique à l'identité de votre main.",
  // doctor_druid_nemesis — Emotionally Overwhelmed (Attachment, x2)
  'dr013': "Attachez-la à votre identité.\n<b>Interruption forcée</b> : quand votre tour commence, défaussez un événement spécifique à l'identité de votre main.\n<b>Action d'alter ego</b> : étourdissez votre identité → défaussez cette carte.",
  // doctor_druid_nemesis — Resurrection of Nekra (Treachery)
  'dr014': "<b>Une fois révélée</b> : si Nekra est en jeu, elle s'active contre vous. SINON, cherchez Nekra dans le deck ET la défausse de rencontre, et révélez-la.",
  // blink — * Blink (Hero) [set 156, Kajislav]
  'bk001a': "<i>Manipulation des portails</i> — <b>Action</b> : rendez à votre main 1 amélioration [[PORTAL]] en jeu. <i>(Limite d'une fois par round.)</i>\n<b>Réponse</b> : après être passée sous cette forme, remélangez 1 amélioration [[PORTAL]] de votre défausse dans votre deck.",
  // blink — * Clarice Ferguson (AlterEgo)
  'bk001b': "<i>Vacances méritées</i> — <b>Réponse forcée</b> : après être passée sous cette forme, remélangez chaque amélioration [[PORTAL]] en jeu dans votre deck. Soignez 1 dégât de votre identité par amélioration ainsi remélangée.",
  // blink — * Sabretooth (Ally)
  'bk002': "<b>Réponse</b> : après que Sabretooth arrive dans votre main, s'il y a une amélioration [[PORTAL]] en jeu, mettez-le en jeu sous votre contrôle. <i>(Limite d'une fois par round.)</i>",
  // blink — Assault Redirection (Event, x2)
  'bk003': "<b>Interruption de héros</b> <i>(défense)</i> : quand un personnage devrait subir des dégâts, quels qu'ils soient, d'une attaque, prévenez la totalité de ces dégâts. Vous pouvez défausser une amélioration [[PORTAL]] attachée à un ennemi pour infliger à cet ennemi autant de dégâts que ceux prévenus de cette façon.",
  // blink — Everywhere at Once (Event, x3)
  'bk004': "<b>Action de héros</b> <i>(attaque/contre)</i> : infligez 2 dégâts à chaque ennemi portant une amélioration [[PORTAL]]. Retirez 2 menaces de chaque manigance portant une amélioration [[PORTAL]].",
  // blink — Lose Footing (Event)
  'bk005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi, plus 2 dégâts supplémentaires par amélioration [[PORTAL]] qui lui est attachée.",
  // blink — Multiple 'Porting (Event)
  'bk006': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance, plus 2 menaces supplémentaires par amélioration [[PORTAL]] qui lui est attachée.",
  // blink — * Crystal Palace (Support)
  'bk007': "<b>Réponse</b> : après qu'une amélioration [[PORTAL]] est défaussée du jeu, inclinez Crystal Palace → attachez-la ici face cachée.\n<b>Action d'alter ego</b> : inclinez Crystal Palace → ajoutez à votre main chaque amélioration [[PORTAL]] attachée ici.",
  // blink — * Blink's Quiver (Upgrade)
  'bk008': "<b>Action de héros</b> : inclinez Blink's Quiver → cherchez une amélioration [[PORTAL]] dans votre deck et ajoutez-la à votre main.\n<b>Action de héros</b> : mettez en jeu une amélioration [[PORTAL]] de votre main.",
  // blink — Portal (Upgrade, x5)
  'bk009': "Forme héros uniquement. Attachez-la à un ennemi ou à une manigance.\n<b>Interruption</b> : quand l'ennemi ou la manigance attaché(e) devient la cible d'un événement [[ATTACK]] ou [[THWART]], réduisez de 2 le coût en ressources de cet événement. Défaussez cette carte après la résolution de cet événement.",
  // blink — * Nocturne (Ally, Agressivité)
  'bk010': "<b>Réponse</b> : après que Nocturne entre en jeu, infligez 1 dégât à un sbire par amélioration que vous contrôlez.",
  // blink — Little Surprise (Event, Agressivité, x2)
  'bk011': "<b>Interruption de héros</b> <i>(attaque)</i> : quand un ennemi manigance, infligez-lui 4 dégâts.",
  // blink — * Mimic (Ally, Basic)
  'bk012': "[star] <b>Action</b> : choisissez un personnage en jeu → jusqu'à la fin du round, la CTR de Mimic est égale à la CTR imprimée de ce personnage <i>(sa SCH à la place si vous choisissez un ennemi)</i> et son ATQ est égale à l'ATQ imprimée de ce personnage.",
  // blink — * Morph (Ally, Basic)
  'bk013': "<b>Action</b> : remélangez Morph dans le deck de rencontre.\n<b>Une fois révélée</b> : défaussez Morph.",
  // blink — Proper Funeral (Event, Basic, x2)
  'bk014': "Alliance. 1 max par phase.\n<b>Réponse</b> : après qu'un allié est vaincu, retirez cet allié de la partie → piochez 3 cartes.",
  // blink — * Earth-295 (Support, Basic)
  'bk015': "<b>Action</b> : inclinez Earth-295 et dépensez 1 ressource de n'importe quel type → redressez un allié, un soutien ou une amélioration unique ([star]) en jeu.",
  // blink — * Tallus (Upgrade, Basic)
  'bk016': "<b>Action</b> : inclinez Tallus → regardez la carte du dessus de votre deck. Si c'est un événement, vous pouvez le jouer <i>(en payant son coût)</i>. Remélangez votre deck.\n<b>Réponse</b> : après qu'un soutien [[LOCATION]] entre en jeu, redressez Tallus.",
  // blink — Stranger in This Reality (Obligation)
  'bk017': "<b><i>Donnez-la au joueur Clarice Ferguson.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Clarice Ferguson → retirez Stranger in This Reality de la partie.\n• Défaussez chaque amélioration [[PORTAL]] en jeu. Si aucune amélioration [[PORTAL]] n'a été défaussée de cette façon, cette carte gagne Renfort. Défaussez cette obligation.",
  // blink_nemesis — * Timebroker (Minion)
  'bk018': "Timebroker ne peut pas subir de dégâts.\n[star] <b>Réponse forcée</b> : après l'activation de Timebroker, placez 2 menaces sur la manigance annexe Damaged Reality.\n<b>Réponse forcée</b> : après que Timebroker entre en jeu, trouvez la manigance annexe Damaged Reality et révélez-la.\n<i>(Sbire némésis de Blink.)</i>",
  // blink_nemesis — Damaged Reality (SideScheme)
  'bk019': "<i>Les Timebreakers avaient accidentellement endommagé de nombreuses réalités à travers le Multivers, puis piégé des héros pour qu'ils réparent leurs erreurs.</i>\n<b>Une fois révélée</b> : placez 1 menace supplémentaire ici par amélioration [[PORTAL]] en jeu. PUIS, défaussez l'une de ces améliorations.\n<b>Une fois vaincue</b> : défaussez Timebroker.",
  // blink_nemesis — Timebreakers (Treachery, x3)
  'bk020': "<b>Une fois révélée</b> : cherchez Timebroker dans le deck ET la défausse de rencontre, et révélez-le. <i>(Remélangez.)</i> Si Timebroker n'entre pas en jeu de cette façon, cette carte gagne Renfort.",
  // texas_twister — * Texas Twister (Hero)
  'tt001a': "<i>Contrôle du vortex</i> — [star] <b>Réponse</b> : après que vous utilisez l'un des pouvoirs de base de Texas Twister <i>(CTR, ATQ ou DEF)</i>, il gagne +1 à CE pouvoir jusqu'à la fin du round.",
  // texas_twister — * Drew Daniels (AlterEgo)
  'tt001b': "<i>Ralentissement</i> — <b>Réponse</b> : après être passé sous cette forme, remélangez jusqu'à 2 cartes [[SUPERPOWER]] de votre défausse dans votre deck.",
  // texas_twister — * Shooting Star (Ally)
  'tt002': "<b>Réponse</b> : après que Shooting Star entre en jeu, redressez Texas Twister.",
  // texas_twister — Accelerated Rotation (Event, x2)
  'tt003': "<b>Action de héros</b> : Texas Twister gagne +1 CTR, +1 ATQ et +1 DEF jusqu'à la fin du round.",
  // texas_twister — Keep Spinning (Event, x5)
  'tt004': "<b>Réponse de héros</b> : après que vous utilisez l'un des pouvoirs de base de Texas Twister <i>(CTR, ATQ ou DEF)</i>, redressez Texas Twister.",
  // texas_twister — * Pine Ridge Reservation (Support)
  'tt005': "Drew Daniels gagne +1 REC.\n<b>Action d'alter ego</b> : inclinez Pine Ridge Reservation → rendez à votre main la carte du dessus de votre défausse.",
  // texas_twister — * Agent T (Upgrade)
  'tt006': "Votre identité gagne le trait [[S.H.I.E.L.D.]].\n<b>Ressource</b> : inclinez Agent T → générez une ressource [wild].",
  // texas_twister — Cyclonic Suction (Upgrade)
  'tt007': "<b>Réponse de héros</b> : après que vous utilisez l'un des pouvoirs de base de Texas Twister <i>(CTR, ATQ ou DEF)</i>, inclinez Cyclonic Suction → piochez 1 carte.",
  // texas_twister — Spin It to the Left! (Upgrade)
  'tt008': "Texas Twister gagne +1 CTR et +1 DEF.\n<b>Interruption forcée</b> : quand une carte [[ROTATION]] entre en jeu, défaussez cette carte.\n<b>Réponse forcée</b> : après que vous faites une attaque de base, défaussez cette carte.",
  // texas_twister — Spin It to the Right! (Upgrade)
  'tt009': "Texas Twister gagne +1 ATQ et +1 DEF.\n<b>Interruption forcée</b> : quand une carte [[ROTATION]] entre en jeu, défaussez cette carte.\n<b>Réponse forcée</b> : après que vous faites un contre de base, défaussez cette carte.",
  // texas_twister — * Texas Twister's Hat (Upgrade)
  'tt010': "Texas Twister gagne <b><i>Solide</i></b>.\n<b>Action d'alter ego</b> : inclinez Texas Twister's Hat → redressez Drew Daniels.",
  // texas_twister — Whirling Debris (Upgrade)
  'tt011': "Texas Twister gagne <b><i>Riposte 1</i></b>.\n<b>Interruption de héros</b> : quand vous faites une attaque de base, inclinez Whirling Debris → les dégâts de cette attaque peuvent être répartis entre les ennemis de votre choix.",
  // texas_twister — * Armadillo (Ally, Protection)
  'tt012': "Armadillo entre en jeu avec 2 pions carapace sur lui.\n<b>Réponse</b> : après qu'un sbire entre en jeu, retirez 1 pion carapace d'Armadillo → donnez une carte de statut Robuste à Armadillo.",
  // texas_twister — * Fifty-One (Ally, Leadership)
  'tt013': "<b>Réponse</b> : après que Fifty-One est vaincu en subissant des dégâts consécutifs, choisissez un allié ; cet allié gagne +1 CTR et +1 ATQ jusqu'à la fin de la phase.",
  // texas_twister — * Firebird (Ally, Justice)
  'tt014': "[star] <b>Interruption</b> : quand Firebird contre, défaussez la carte du dessus de votre deck. Par ressource [energy] imprimée ainsi défaussée, réduisez de 1 tous les dégâts consécutifs que Firebird subit pour cet usage.",
  // texas_twister — * Living Lightning (Ally, Agressivité)
  'tt015': "[star] <b>Interruption</b> : quand Living Lightning attaque, infligez 1 dégât à chaque personnage en jeu.",
  // texas_twister — Lone Star Rangers (Event, Basic)
  'tt016': "<b>Action de héros</b> : après qu'un personnage [[RANGER]] est vaincu, redressez chaque personnage [[RANGER]] que vous contrôlez.",
  // texas_twister — * Phantom Rider (Ally, Basic)
  'tt017': "Phantom Rider subit -1 dégât consécutif ; il ignore les mots-clés Garde et Patrouille, ainsi que toute icône de crise ([crisis]) en jeu.",
  // texas_twister — * Red Wolf (Ally, Basic)
  'tt018': "<b>Réponse</b> : après qu'un allié entre en jeu sous votre contrôle, réduisez de 1 tous les dégâts consécutifs que Red Wolf subit jusqu'à la fin de la phase.",
  // texas_twister — Twist Again (Event, Basic, max 1)
  'tt019': "Équipe (Texas Twister et Shooting Star). 1 max par deck.\n<b>Action de héros</b> : après que vous utilisez l'un des pouvoirs de base de Texas Twister ou de Shooting Star, redressez-les tous les deux.",
  // texas_twister — Rodeo Extravaganza (Obligation)
  'tt020': "<b><i>Donnez-la au joueur de Drew Daniels.</i></b>\nVotre identité ne peut pas être redressée par des effets de cartes joueur.\n<b>Action d'alter ego</b> : inclinez Drew Daniels → retirez Rodeo Extravaganza de la partie.",
  // texas_twister_nemesis — * Master Pandemonium (Minion)
  'tt021': "[star] <b>Interruption forcée</b> : quand Master Pandemonium s'apprête à s'activer contre vous, choisissez de dépenser une ressource [energy] ou d'incliner votre identité.\n<i>(Sbire némésis de Texas Twister.)</i>",
  // texas_twister_nemesis — Portal to Hell (SideScheme)
  'tt022': "<i>Le corps de Master Pandemonium est un portail vers l'Enfer, d'où il peut libérer d'innombrables démons.</i>\n<b>Une fois révélée</b> : cherchez l'attachement Demonic Limbs et révélez-le.",
  // texas_twister_nemesis — Demonic Limbs (Attachment)
  'tt023': "Attachez-la à Master Pandemonium. Si vous ne pouvez pas, étourdissez un personnage que vous contrôlez et rendez confus un personnage que vous contrôlez.\nMaster Pandemonium ne peut pas subir de dégâts.\n<b>Action de héros</b> : dépensez [energy][energy] → défaussez cette carte.",
  // texas_twister_nemesis — Soul Fragmentation (Treachery, x2)
  'tt024': "<b>Une fois révélée</b> : défaussez les 3 cartes du dessus de votre deck. Si une ressource [physical] a été défaussée ainsi, vous êtes étourdi ; si une ressource [mental] a été défaussée ainsi, vous êtes confus ; si une ressource [wild] a été défaussée ainsi, inclinez votre identité.",
  // beta_ray_bill — * Beta Ray Bill (Hero)
  'br001a': "<i>Digne</i> — <b>Action</b> : cherchez Stormbreaker et ajoutez-la à votre main. Si elle quitte le jeu de cette façon, infligez 3 dégâts à un ennemi. <i>(Limite d'une fois par round.)</i>",
  // beta_ray_bill — * Beta Ray Bill (AlterEgo) — ⚠ MEME NOM que la face héros
  'br001b': "<i>Voyageur des étoiles</i> — <b>Action</b> : cherchez un exemplaire de Star Jump et ajoutez-le à votre main. <i>(Limite d'une fois par round.)</i>",
  // beta_ray_bill — Eye of the Storm (Event, x2)
  'br002': "<b>Action de héros</b> : dépensez X ressources [energy] et choisissez un joueur → retirez X menaces de chaque manigance en jeu. Ce joueur engage jusqu'à X sbires en jeu. Cette action ignore l'icône de crise si vous avez le trait [[AERIAL]] ou si vous avez utilisé Stormbreaker pour payer cette carte.",
  // beta_ray_bill — Hammer Throw (Event, x3) — ⚠ HOMONYME de 06005 (Thor)
  'br003': "<b>Action de héros</b> <i>(attaque)</i> : inclinez Stormbreaker → infligez 6 dégâts à un ennemi. Cherchez Stormbreaker et ajoutez-la à votre main. Cette attaque gagne Déferlement.",
  // beta_ray_bill — Hammer Twirl (Event, x2)
  'br004': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts d'une attaque, inclinez Stormbreaker ou dépensez 1 ressource de n'importe quel type → prévenez tous ces dégâts. Si vous avez payé cette carte avec Stormbreaker, infligez 2 dégâts à votre attaquant.",
  // beta_ray_bill — Star Jump (Event, coût X, x2)
  'br005': "<b>Action</b> : choisissez X des effets suivants :\n• Cherchez un sbire dans le deck de rencontre et mettez-le en jeu engagé avec vous → redressez Skuttlebutt.\n• Cherchez une carte Beta Ray Bill et ajoutez-la à votre main.\n• Redressez Beta Ray Bill.",
  // beta_ray_bill — Thunderstrike (Event, x2)
  'br006': "Prérequis ([energy]).\n<b>Action de héros</b> : choisissez un joueur → infligez 3 dégâts au vilain et à chaque sbire engagé avec ce joueur. Étourdissez chaque ennemi ainsi blessé.",
  // beta_ray_bill — * Skuttlebutt (Support)
  'br007': "Skuttlebutt ne se redresse pas à la fin de la phase du joueur. Tant que Skuttlebutt est prêt, vous gagnez +1 en taille de main.\n<b>Action de héros</b> : inclinez Skuttlebutt → choisissez l'un des effets suivants :\n• Infligez 2 dégâts à chaque ennemi.\n• Retirez 2 menaces de chaque manigance.",
  // beta_ray_bill — Calm Before the Storm (Upgrade)
  'br008': "Votre héros gagne +1 ATQ tant que Stormbreaker est en jeu, et +1 CTR tant qu'elle ne l'est pas.\n<b>Action de héros</b> : dépensez 1 ressource de n'importe quel type et inclinez cette carte → résolvez la capacité <i>Digne</i> de votre héros <i>(en ignorant sa limite)</i>.",
  // beta_ray_bill — Oathbrother (Upgrade)
  'br009': "<b>Réponse de héros</b> : après qu'un sbire entre en jeu, cherchez un événement dans votre deck et ajoutez-le à votre main. <i>(Limite d'une fois par phase.)</i>",
  // beta_ray_bill — * Stormbreaker (Upgrade)
  'br010': "Restreinte.\nVotre héros gagne le trait [[AERIAL]].\n<b>Ressource de héros</b> : défaussez Stormbreaker du jeu → générez [wild][wild] pour un événement.",
  // beta_ray_bill — Hammer Time (Event, Basic, max 1)
  'br011': "Alliance. Équipe (Beta Ray Bill et Thor). 1 max par deck.\n<b>Action de héros</b> <i>(attaque)</i> : cherchez un sbire dans le deck de rencontre et mettez-le en jeu engagé avec vous → infligez-lui 10 dégâts. Cette attaque gagne Déferlement.",
  // beta_ray_bill — Unworthy (Obligation)
  'br012': "<b><i>Donnez-la au joueur de Beta Ray Bill.</i></b>\nUtilisations (2 pions indignité). Victoire 0.\n<b>Une fois révélée</b> : cherchez Stormbreaker et glissez-la sous cette carte. Tant qu'elle y est, Stormbreaker ne peut pas être cherchée.\n<b>Réponse forcée</b> : après que vous vainquez un ennemi ou une manigance, retirez 1 pion indignité d'ici.",

  // ===== throg (set 159, Rainy) — 17 cartes ==============================
  // ⚠ Les deux faces ont des NOMS DIFFERENTS : « Throg » en héros,
  // « Puddlegulp » en alter ego. Contrairement à beta_ray_bill.
  // throg — * Throg (Hero)
  'tg001a': "[star] <i>Endurance de grenouille</i> — <b>Réponse</b> : après que Throg utilise un pouvoir de base, renvoyez Frogjolnir dans votre main → redressez Throg. <i>(Limite d'une fois par phase.)</i>",
  // throg — * Puddlegulp (AlterEgo)
  'tg001b': "<i>Digne</i> — <b>Action</b> : cherchez Frogjolnir et ajoutez-la à votre main. <i>(Limite d'une fois par round.)</i>",
  // throg — Airborne Amphibian (Event, x3)
  'tg002': "<b>Action de héros</b> : redressez Throg et Frogjolnir. Vous pouvez choisir un sbire engagé avec un autre joueur et l'engager pour piocher 1 carte.",
  // throg — Great Courage (Event, x2)
  'tg003': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance. Engagez n'importe quel nombre de sbires en jeu. Pour chaque sbire engagé avec vous <i>(jusqu'à un maximum de 3)</i>, retirez 2 menaces d'une manigance.",
  // throg — Hammer Throw (Event, x2) — ⚠ HOMONYME de 06005 (Thor) et br003 (Beta Ray Bill)
  'tg004': "<b>Action de héros</b> <i>(attaque)</i> : inclinez Frogjolnir et renvoyez-la dans votre main → infligez 6 dégâts à un ennemi. Cette attaque gagne Déferlement.",
  // throg — Lightning Leap (Event, x2)
  'tg005': "<b>Interruption de héros</b> : quand vous faites une attaque de base contre un sbire engagé avec un joueur, résolvez plutôt cette attaque contre le vilain et chaque sbire engagé avec ce joueur, en ignorant le mot-clé Garde.",
  // throg — Thunderous Charge (Event, x2)
  'tg006': "<b>Interruption de héros</b> : quand vous faites un contre de base contre une manigance, résolvez plutôt ce contre contre chaque manigance en jeu, en ignorant l'icône de crise ([crisis]) <i>(dans l'ordre de votre choix, bonus de CTR compris pour ce contre)</i>.",
  // throg — * Foreverglade (Support)
  'tg007': "<b>Réponse d'alter ego</b> : après que vous faites une récupération de base, inclinez Foreverglade → redressez Puddlegulp et piochez 1 carte.",
  // throg — Frog of Thunder (Upgrade)
  'tg008': "<b>Ressource de héros</b> : inclinez Frog of Thunder → générez une ressource [energy]. Si vous avez payé une carte Throg de cette façon, infligez 1 dégât à un ennemi.",
  // throg — * Frogjolnir (Upgrade) — la carte que tout le pack cite
  'tg009': "Restreinte.\nThrog gagne le trait [[AERIAL]].\n<b>Interruption de héros</b> : quand Throg utilise un pouvoir de base, inclinez Frogjolnir → Throg gagne +1 à ce pouvoir pour cette utilisation.",
  // throg — * Throg's Armor (Upgrade)
  'tg010': "Vous gagnez +2 points de vie.\n<b>Réponse de héros</b> : après que vous engagez un sbire, donnez à Throg une carte de statut Robuste. Si vous ne pouvez pas, piochez 1 carte. <i>(Limite d'une fois par phase.)</i>",
  // throg — Trouble in Central Park (Obligation) — bandeau THROG, set du héros
  'tg011': "<b><i>Donnez-la au joueur de Puddlegulp.</i></b>\nUtilisations (3 pions ennemi). Victoire 0.\n<b>Action forcée</b> : cherchez un sbire dans le deck de rencontre et mettez-le en jeu engagé avec vous → retirez 1 pion ennemi d'ici. Cet ennemi vous attaque. <i>(Limite d'une fois par round.)</i>",
  // throg — Adorable Distraction (SideScheme némésis)
  'tg012': "<i>Alligator Loki distrait tout le monde par sa bouille adorable. Que quelqu'un le caresse, qu'on puisse revenir à nos affaires !</i>\nEntrave 1[per_hero].\nAlligator Loki ne peut pas être attaqué.\n<i>(Manigance annexe némésis de Throg.)</i>",
  // throg — * Alligator Loki (Minion némésis) — ⚠ HOMONYME du HEROS al001a (set 140)
  'tg013': "<b>Réponse forcée</b> : après qu'Alligator Loki entre en jeu, cherchez Chomped et attachez-la à votre identité.\n[star] <b>Interruption forcée</b> : quand Alligator Loki manigance et place de la menace, placez autant de menace sur chaque manigance annexe.\n[star] Les attaques d'Alligator Loki gagnent Perçant.\n<i>(Sbire némésis de Throg.)</i>",
  // throg — Causing a Commotion (SideScheme némésis)
  'tg014': "<i>Alligator Loki fait un scandale et met la pagaille ! Que quelqu'un l'attrape avant qu'il n'en fasse davantage !</i>\n<b>Une fois révélée</b> : chaque joueur défausse les 3 premières cartes de son deck et place 1 menace ici pour chaque type de carte différent défaussé de cette façon.",
  // throg — "Lost" Property (SideScheme némésis)
  'tg015': "<i>Ce garnement a pris nos affaires ! Attrapez-le et récupérez-les, aussi mignon soit-il avec.</i>\n<b>Une fois révélée</b> : chaque joueur glisse sous cette carte une amélioration spécifique à son identité qu'il contrôle. Elle ne peut pas être cherchée tant qu'elle est dessous.\n<b>Une fois vaincue</b> : ajoutez chaque carte glissée dessous à la main de son propriétaire.",
  // throg — Chomped (Attachment némésis)
  'tg016': "Attachez-la à votre identité.\n<b>Interruption forcée</b> : quand le round se termine, subissez 1 dégât.\n<b>Interruption forcée</b> : quand vous utiliseriez un pouvoir de base, défaussez Chomped et subissez plutôt 1 dégât.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // spider_man_noir — * Spider-Man Noir (Hero)
  'sn001a': "[star] Spider-Man Noir gagne +X ATQ et +X CTR, X étant égal au nombre de cartes glissées sous lui.\n<i>Sens d'araignée</i> — <b>Réponse</b> : après que vous résolvez une traîtrise, glissez cette carte ici <i>(jusqu'à un maximum de 3)</i>.",
  // spider_man_noir — * Peter Parker (AlterEgo) — ⚠ HOMONYME de 01001b, sr001b, as001b et de l'allié bt014
  'sn001b': "<i>Fin limier</i> — <b>Action</b> : défaussez la carte du dessus du deck rencontre → choisissez soit de glisser cette carte ici <i>(jusqu'à un maximum de 3)</i>, soit de retirer d'une manigance un nombre de menaces égal au nombre d'icônes de boost défaussées. <i>(Limite d'une fois par round.)</i>",
  // spider_man_noir — Guns Blazing (Event, x3)
  'sn002': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi et redressez Dual Pistols. Si cette attaque vainc un sbire, glissez-le sous Spider-Man Noir depuis la pile de défausse rencontre <i>(jusqu'à un maximum de 3 cartes)</i>.",
  // spider_man_noir — Webs Within Webs (Event, x2)
  'sn003': "<b>Action de héros</b> <i>(contre)</i> : défaussez la carte du dessus du deck rencontre → retirez d'une manigance un nombre de menaces égal à 3 plus le nombre d'icônes de boost défaussées de cette façon. Glissez la carte défaussée sous votre héros <i>(jusqu'à un maximum de 3)</i>.",
  // spider_man_noir — Web Shot (Event, x2)
  'sn004': "<b>Interruption de héros</b> : quand une carte de boost est retournée face visible pendant l'activation d'un ennemi, défaussez-la à la place et glissez-la sous Spider-Man Noir <i>(jusqu'à un maximum de 3)</i>.",
  // spider_man_noir — Web Swinging (Event, x3)
  'sn005': "<b>Réponse de héros</b> : après que Spider-Man Noir utilise un pouvoir de base, défaussez une carte glissée sous Spider-Man Noir → redressez Spider-Man Noir. Défaussez la carte du dessus du deck rencontre et glissez-la sous Spider-Man Noir <i>(jusqu'à un maximum de 3)</i>.",
  // spider_man_noir — * The Black Cat Club (Support)
  'sn006': "<b>Action d'alter ego</b> : inclinez The Black Cat Club et défaussez une carte glissée sous votre identité → choisissez soit de piocher 2 cartes, soit de soigner 4 dégâts de votre identité.",
  // spider_man_noir — Dual Pistols (Upgrade)
  'sn007': "Restreinte.\n<b>Action de héros</b> <i>(attaque)</i> : inclinez Dual Pistols et défaussez une carte glissée sous votre héros → infligez 3 dégâts à un ennemi. Cette attaque gagne à distance.",
  // spider_man_noir — Enhanced Spider-Sense (Upgrade) — ⚠ HOMONYME de l'événement 01004
  'sn008': "<b>Interruption de héros</b> : quand un autre joueur révèle une traîtrise, révélez-la à sa place et piochez 1 carte.\n<b>Interruption de héros</b> : quand le vilain déclenche une attaque contre vous, piochez 1 carte.",
  // spider_man_noir — Fancy Fedora (Upgrade)
  'sn009': "<b>Action de héros</b> : inclinez cette carte et défaussez une carte glissée sous votre héros → retirez 2 menaces d'une manigance.\n<b>Réponse</b> : après que vous contrez et vainquez une manigance annexe, glissez-la sous votre identité depuis la pile de défausse rencontre <i>(jusqu'à un maximum de 3 cartes)</i>.",
  // spider_man_noir — Organic Webbing (Upgrade) — ⚠ HOMONYME de 30011 et 52009
  'sn010': "<b>Action de héros</b> : inclinez Organic Webbing et défaussez une carte glissée sous Spider-Man Noir → redressez Spider-Man Noir. Il gagne le trait [[AERIAL]] jusqu'à la fin du round.",
  // spider_man_noir — In Walks Trouble (Obligation)
  'sn011': "<b><i>Donnez-la au joueur de Peter Parker.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Peter Parker → retirez In Walks Trouble de la partie.\n• Révélez une carte au hasard glissée sous votre identité. Si vous ne pouvez pas, cette carte gagne <b><i>Déferlement</i></b>. Défaussez cette obligation.",
  // spider_man_noir — Power Struggle (SideScheme némésis)
  'sn012': "<i>Electro draine les réserves d'énergie de la ville. Il crépite d'étincelles et devient plus fort de minute en minute : arrêtez-le avant qu'il ne soit trop tard !</i>\n<b>Interruption forcée</b> : quand un personnage contre cette manigance, il subit 1 dégât.",
  // spider_man_noir — * Electro Noir (Minion némésis)
  'sn013': "Riposte 1.\n[star] <b>Interruption forcée</b> : quand Electro Noir s'active contre vous, donnez-lui comme carte de boost une carte de rencontre au hasard glissée sous votre identité. Sinon, donnez-lui une carte de boost face cachée du dessus du deck rencontre.\n<i>(Sbire némésis de Spider-Man Noir.)</i>",
  // spider_man_noir — Lightning Strikes Twice (Treachery némésis, x2)
  'sn014': "<b>Une fois révélée</b> : glissez la carte du dessus du deck rencontre sous votre identité <i>(jusqu'à un maximum de 3 cartes)</i>. Pour chaque icône ([star] et [boost]) dans la zone de boost des cartes glissées sous votre identité, subissez 1 dégât <i>(jusqu'à un maximum de 4 dégâts)</i>.\n<hr />\n[star] <b>Boost</b> : après cette activation, cet ennemi s'active de nouveau.",
  // spider_man_noir — Thunderstorm (Environment némésis) — ⚠ HOMONYME de 36004
  'sn015': "Les cartes de ce set gagnent Déferlement.\n<b>Réponse forcée</b> : après que le mot-clé Déferlement d'une carte de rencontre est résolu <i>(y compris celui de cette carte)</i>, le joueur qui le résout subit 1 dégât indirect s'il est sous forme de héros.\n<b>Action de héros</b> : dépensez des ressources [energy] [energy] → défaussez cette carte.",
  // black_cat — * Black Cat (Hero) — ⚠ HOMONYME de 01002, wd045 et vp002
  'bc001a': "S'il y a plus de 3 cartes glissées ici, défaussez-les toutes sauf 3.\n<i>Tychokinésie</i> — <b>Interruption</b> : quand les icônes ([star] et [boost]) d'une carte de rencontre devraient être comptées, comptez à la place celles d'une carte glissée ici. Puis défaussez-la.",
  // black_cat — * Felicia Hardy (AlterEgo)
  'bc001b': "S'il y a plus de 3 cartes glissées ici, défaussez-les toutes sauf 3.\n<i>Cambriolage</i> — <b>Action</b> : regardez les 2 cartes du dessus du deck rencontre et glissez-en 1 sous votre identité. <i>(Limite d'une fois par round.)</i>",
  // black_cat — * Spider-Man version SYMBIOTE (Ally, carte 1/15)
  'bc002': "[star] <b>Interruption forcée</b> : quand Spider-Man utilise un pouvoir de base, défaussez la carte du dessus du deck rencontre. Pour chaque icône de boost ([boost]) défaussée de cette façon, il gagne +1 à ce pouvoir pour cette utilisation et subit +1 dégât consécutif.",
  // black_cat — * Spider-Man version AVENGER (Ally, carte 1/15, Multiverse)
  'bc003': "Multivers. Entre en jeu avec 2 pions toile.\n<b>Interruption</b> : quand un ennemi s'active, retirez 1 pion toile d'ici et défaussez une carte glissée sous votre identité → annulez cette activation.",
  // black_cat — * Big Heist (manigance annexe JOUEUR)
  'bc004': "Seuls les personnages [[THIEF]] peuvent retirer de la menace de cette manigance.\n<b>Une fois vaincue</b> : choisissez :\n• Cherchez dans votre collection une amélioration basique ou d'aspect et jouez-la sans payer son coût en ressources.\n• Glissez sous Black Cat une amélioration attachée en jeu portant le texte \"<b>Action de héros</b>\" ou \"<b>Réponse de héros</b>\".\n• Piochez 3 cartes.",
  // black_cat — Cat Burglary (Event, x2) — ⚠ HOMONYME de la capacité de bc001b
  'bc005': "<b>Action de héros</b> <i>(contre)</i> : regardez les 3 cartes du dessus du deck rencontre et défaussez-en 1. Retirez 1 menace d'une manigance, plus 1 menace supplémentaire par icône ([star] et [boost]) dans la zone de boost de cette carte. Glissez-la sous Black Cat.",
  // black_cat — Lucky Hit (Event, x2)
  'bc006': "<b>Action de héros</b> <i>(attaque)</i> : défaussez les 2 cartes du dessus du deck rencontre et infligez 1 dégât à un ennemi par icône ([star] et [boost]) défaussée de cette façon. Glissez une de ces cartes sous Black Cat.",
  // black_cat — Misfortune (Event, x2)
  'bc007': "<b>Interruption de héros</b> : quand une carte de boost est retournée pendant l'activation d'un ennemi, glissez-la plutôt sous votre héros. Cet ennemi gagne -1 ATQ et -1 MNG pour cette activation par icône ([star] et [boost]) dans la zone de boost de cette carte.",
  // black_cat — * Black Cat's Claws (Upgrade)
  'bc008': "<b>Action de héros</b> <i>(attaque)</i> : inclinez Black Cat's Claws et défaussez la carte du dessus du deck rencontre → infligez à un ennemi autant de dégâts qu'il y a d'icônes dans la zone de boost de cette carte. Si ce nombre était 0, glissez-la sous Black Cat.",
  // black_cat — Grappling Hook (Upgrade, x2) — ⚠ HOMONYME de 08008 et 50069
  'bc009': "<b>Action de héros</b> : inclinez Grappling Hook et défaussez une carte glissée sous Black Cat → redressez Black Cat et glissez sous elle la carte du dessus du deck rencontre.",
  // black_cat — Ill Gotten Gains (Upgrade, x2)
  'bc010': "<b>Ressource</b> : inclinez cette carte → générez une ressource [wild] <i>([wild][wild] à la place pour une amélioration attachée)</i>.\n<b>Réponse</b> : après que vous défaussez du jeu une amélioration attachée portant le texte \"<b>Action de héros</b>\" ou \"<b>Réponse de héros</b>\", glissez-la sous votre identité.",
  // black_cat — Nine Lives (Upgrade, x2)
  'bc011': "<b>Interruption de héros</b> : quand Black Cat subirait des dégâts, quel qu'en soit le nombre, inclinez Nine Lives et défaussez la carte du dessus du deck rencontre → prévenez 1 de ces dégâts par icône ([star] et [boost]) dans la zone de boost de cette carte.",
  // black_cat — Luck's Ran Out (Obligation)
  'bc012': "<b><i>Donnez-la au joueur de Felicia Hardy.</i></b>\nRévélez une carte au hasard glissée sous votre identité. Si vous ne pouvez pas, cette carte gagne <b><i>Déferlement</i></b>. Défaussez cette carte.",
  // cameo_compliment — Lock It Down (Support, aspect JUSTICE)
  'cc001': "Mise en place. 1 max par deck.\n<b>Mise en place</b> : cherchez dans votre collection un soutien spécifique à une identité portant le trait [[LOCATION]] appartenant à une identité absente de cette partie. Mélangez cette carte dans votre deck. Défaussez 2 cartes de votre main et retirez cette carte de la partie.",
  // cameo_compliment — New Suit? (Support, aspect PROTECTION)
  'cc002': "Mise en place. 1 max par deck.\n<b>Mise en place</b> : cherchez dans votre collection une amélioration spécifique à une identité portant le trait [[ARMOR]] appartenant à une identité absente de cette partie. Mélangez cette carte dans votre deck. Défaussez 2 cartes de votre main et retirez cette carte de la partie.",
  // cameo_compliment — Ye Be Worthy (Support, aspect AGRESSIVITÉ)
  'cc003': "Mise en place. 1 max par deck.\n<b>Mise en place</b> : cherchez dans votre collection une amélioration NON PERMANENTE spécifique à une identité portant le trait [[WEAPON]] appartenant à une identité absente de cette partie. Mélangez cette carte dans votre deck. Défaussez 2 cartes de votre main et retirez cette carte de la partie.",
  // sunfire — * Sunfire (Hero) — ⚠ HOMONYME de l'allié 35014
  'sf001a': "[star] <i>Aura brûlante</i> — <b>Interruption</b> : quand Sunfire fait une attaque de base ou une défense de base contre un ennemi, attachez à cet ennemi un exemplaire de Burning mis de côté.",
  // sunfire — * Shiro Yoshida (AlterEgo)
  'sf001b': "Shiro Yoshida commence la partie avec 6 améliorations Burning mises de côté.\n<i>Tête brûlée</i> — <b>Action</b> : défaussez les 5 cartes du dessus de votre deck. Choisissez une carte défaussée de cette façon et ajoutez-la à votre main. <i>(Limite d'une fois par round.)</i>",
  // sunfire — Atomic Fire (Event, x2)
  'sf002': "<b>Action de héros</b> : choisissez un joueur et attachez un exemplaire de Burning mis de côté au vilain et à chaque sbire engagé avec ce joueur. Infligez 3 dégâts à chaque ennemi portant un exemplaire de Burning.",
  // sunfire — Burning Hands (Event, x3)
  'sf003': "<b><i>Exigence</i></b> ([energy]).\n<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Puis choisissez une amélioration attachée portant le texte \"<b>Action de héros</b>\" ou \"<b>Réponse de héros</b>\" et défaussez-la. Sinon, attachez un exemplaire de Burning mis de côté à un ennemi.",
  // sunfire — Hot Pursuit (Event, x4) — ⚠ HOMONYME de la manigance annexe 24058
  'sf004': "<b>Réponse de héros</b> : après que vous attachez un exemplaire de Burning à un ennemi, redressez Sunfire.",
  // sunfire — Solar Blast (Event, x3)
  'sf005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Puis choisissez une amélioration attachée portant le texte \"<b>Action de héros</b>\" ou \"<b>Réponse de héros</b>\" attachée à cet ennemi et défaussez-la. Sinon, attachez à cet ennemi un exemplaire de Burning mis de côté.",
  // sunfire — * Atomic Samurai (Upgrade)
  'sf006': "<b>Interruption</b> : quand un ennemi subirait des dégâts de la capacité déclenchée de Burning, il subit 1 dégât supplémentaire.",
  // sunfire — * Sunfire's Mask (Upgrade)
  'sf007': "Vous gagnez +2 points de vie.\n<b>Réponse de héros</b> : après qu'un ennemi portant un exemplaire de Burning est vaincu, piochez 1 carte. <i>(Limite d'une fois par phase.)</i>",
  // sunfire — Sunfire's Suit (Upgrade)
  'sf008': "Sunfire gagne +1 DEF.\n<b>Réponse de héros</b> : après que Sunfire se défend contre une attaque, inclinez Sunfire's Suit et dépensez 1 ressource de n'importe quel type → redressez Sunfire.",
  // sunfire — Burning (Upgrade, 6 exemplaires MIS DE CÔTÉ)
  'sf009': "Permanent.\n<b>Réponse forcée</b> : après la fin de la phase des joueurs, infligez 1 dégât à l'ennemi auquel cette carte est attachée. Mettez cette carte de côté.\n<b>Réponse forcée</b> : après que l'ennemi auquel cette carte est attachée quitte le jeu, mettez cette carte de côté.",
  // sunfire — Shame (Obligation)
  'sf010': "<b><i>Donnez-la au joueur de Shiro Yoshida.</i></b>\nVous avez -1 à votre taille de main. Le nombre de cartes dans votre main ne peut pas dépasser votre taille de main <i>(défaussez jusqu'à votre taille de main après avoir pioché des cartes)</i>.\n<b>Action d'alter ego</b> : inclinez Shiro Yoshida et défaussez 1 carte de votre main → retirez Shame de la partie.",
  // sunfire — Hand Ambush (SideScheme némésis)
  'sf011': "<i>La Main nous attendait en embuscade !</i>\n<b>Interruption forcée</b> : quand un ennemi entre en jeu, donnez-lui une carte de boost face cachée.\n<b>Réponse forcée</b> : après qu'un sbire [[HAND]] est vaincu, placez-le sur le dessus du deck rencontre.",
  // sunfire — * Silver Samurai (Minion némésis)
  'sf012': "Coup Rapide. Riposte 1.\n<b>Interruption forcée</b> : quand Silver Samurai entre en jeu, si elle n'est pas en jeu, cherchez Silver Samurai's Katana et attachez-la-lui.\n<i>(Sbire némésis de Sunfire.)</i>",
  // sunfire — Hand Ninja (Minion némésis)
  'sf013': "[star] Les attaques de Hand Ninja gagnent Perçant.\n<b>Réponse forcée</b> : après que Hand Ninja entre en jeu, il s'active contre vous.\n<hr />\n[star] <b>Boost</b> : mettez ce sbire en jeu, engagé avec vous.",
  // sunfire — * Silver Samurai's Katana (Attachment némésis)
  'sf014': "Attachez-la à Silver Samurai. Si vous ne pouvez pas, cherchez Silver Samurai et mettez-le en jeu engagé avec vous, cette carte attachée.\nSilver Samurai ne peut pas subir de dégâts provenant d'attaques.\n<b>Action de héros</b> : dépensez 3 ressources de n'importe quel type → défaussez cette carte.",
  // sunfire — Tachyon Whip (Attachment némésis)
  'sf015': "Attachez-la à votre héros. Sinon, cette carte gagne <b><i>Déferlement</i></b>. Vous ne pouvez pas passer sous forme d'alter ego.\n<b>Réponse forcée</b> : après que vous utilisez un pouvoir de base, subissez 2 dégâts.\n<b>Action de héros</b> : dépensez des ressources [physical][physical] → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : après cette activation, révélez cette carte.",
}

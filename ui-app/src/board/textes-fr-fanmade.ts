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
//  - etats : Sonne, Desoriente, carte d'etat Tenace (Tough), Tenacite
//    (Toughness), Robuste (Stalwart), Solide (Steady). Gate :
//    vocabulaire-statuts.test.ts ;
//  - statistiques ATQ, CTR, DEF, REC, MNG ;
//  - aspects Agressivite, Justice, Leadership, Protection ;
//  - NOMS PROPRES et traits [[...]] laisses en anglais : le joueur a la carte
//    anglaise sous les yeux et doit s'y retrouver ;
//  - jetons de jeu ([mental], [star], [per_hero]...) recopies tels quels ;
//  - cartes d'etat maison : Camouflé (Cloaked), Hébété (Dazed, verbe « hébétez »),
//    Intensifié (Intensified, verbe « intensifiez ») ;
//  - capacite nommee « Special » = « Spécial » ; « all-purpose counter » = « compteur polyvalent ».
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
  '60001a': "<i>Sens surhumains</i> — <b>Action</b> : jouez la carte du dessus du deck [[Sense]] comme si elle était dans votre main <i>(en payant son coût)</i>.\n<b>Interruption forcée</b> : quand une amélioration [[Sense]] devrait quitter le jeu, placez-la plutôt sous le deck [[Sense]].",
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
  'cd001b': "Pendant la construction du deck, voir l'encart.\n<i>Éclaircissement</i> — Tandy Bowen et Tyrone Johnson gagnent Robuste tant que Tandy Bowen est en jeu.",
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
  'il019': "Ténacité. Vilenie.\n<b>Une fois révélée</b> : placez l'amélioration Iron Lad au coût le plus élevé en jeu sous Kang the Conqueror.\n<b>Une fois vaincu</b> : renvoyez l'amélioration placée ici dans la main de son propriétaire. Mettez Kang the Conqueror de côté.",
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
  'pt019': "Ténacité.\n<b>Une fois révélée</b> : cherchez l'attachement MGH Drug dans le deck de rencontre, la pile de défausse de rencontre et les cartes mises de côté, et attachez-le à Mr. Hyde.\n<i>(Sbire némésis de Patriot.)</i>",
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
  'ma002': "<b><i>Ténacité</i></b>.\n<b>Réponse de héros</b> : après avoir résolu « Star-Gaze », Alloy gagne +1 ATQ jusqu'à la fin du tour.",
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
  'ma011': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, prévenez tous ces dégâts. Donnez une carte d'état Tenace à votre identité.",
  'ma012': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, prévenez tous ces dégâts. Donnez une carte d'état Tenace à votre identité.",
  // ms_america — Star Portal (Event, x2)
  'ma013': "<b>Action de héros</b> : cherchez un allié dans la pile de défausse de n'importe quel joueur et mettez-le incliné dans la zone de jeu de n'importe quel joueur → retirez d'une manigance un nombre de menaces égal au CTR de cet allié et infligez à un ennemi un nombre de dégâts égal à son ATQ.",
  'ma014': "<b>Action de héros</b> : cherchez un allié dans la pile de défausse de n'importe quel joueur et mettez-le incliné dans la zone de jeu de n'importe quel joueur → retirez d'une manigance un nombre de menaces égal au CTR de cet allié et infligez à un ennemi un nombre de dégâts égal à son ATQ.",
  // ms_america — Break Through (Event, x2)
  'ma015': "<b>Action de héros</b> <i>(attaque/contre)</i> : infligez 4 dégâts à un ennemi. Retirez 3 menaces d'une manigance. Si cela met K.O. un ennemi ou une manigance, sonnez ou désorientez un ennemi.",
  'ma016': "<b>Action de héros</b> <i>(attaque/contre)</i> : infligez 4 dégâts à un ennemi. Retirez 3 menaces d'une manigance. Si cela met K.O. un ennemi ou une manigance, sonnez ou désorientez un ennemi.",
  // ms_america — Edges Syndrome (Obligation)
  'ma017': "<b><i>Donnez-la au joueur America Chavez.</i></b>\nVotre identité subit -1 à chacun de ses pouvoirs de base.\n<b>Action</b> : subissez 2 dégâts → défaussez cette carte.\n<b>Action</b> : subissez 4 dégâts → retirez cette carte de la partie.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // ms_america — Catalina Chavez (Minion, nemesis)
  'ma018': "<b><i>Coup Rapide</i></b>.\n[star] Catalina Chavez gagne chaque modificateur de caractéristique présent dans votre zone de jeu (le CTR étant remplacé par le MNG).\n<i>(Sbire némésis de Ms. America.)</i>",
  // ms_america — Search for the Cure (SideScheme, nemesis)
  'ma019': "<b>Une fois révélée</b> : chaque joueur cherche un allié dans sa pile de défausse et l'attache à cette carte. La menace de départ de cette carte est égale au coût en ressources cumulé des cartes attachées. Pour chaque joueur qui n'a attaché aucun allié, cette carte reçoit 2[per_hero] menaces de départ supplémentaires.",
  // ms_america — Star Lightning (Treachery, nemesis, x2)
  'ma020': "<b>Une fois révélée</b> : Catalina Chavez vous attaque. Si cette attaque inflige des dégâts, votre identité est sonnée. Si aucune attaque n'a eu lieu de cette façon, cette carte gagne <b><i>Déferlement</i></b>.",
  'ma021': "<b>Une fois révélée</b> : Catalina Chavez vous attaque. Si cette attaque inflige des dégâts, votre identité est sonnée. Si aucune attaque n'a eu lieu de cette façon, cette carte gagne <b><i>Déferlement</i></b>.",
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
  'vp005': "<b>Action de héros</b> <i>(contrer)</i> : sonnez le vilain. Si le vilain est déjà sonné, retirez 3 menace d'une manigance à la place.",
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
  'vp011': "<b><i>Donnez cette carte au joueur de Wade Wilson.</i></b>\nVous devez passer sous forme d'alter ego. Choisissez :\n• Inclinez Wade Wilson → retirez One Too Many Voices de la partie.\n• Défaussez Klyntar Suit. Si Klyntar Suit n'a pas été défaussée de cette façon, cette carte gagne <b><i>Déferlement</i></b>. Défaussez cette obligation.",
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
  'an006': "Angela gagne <b><i>Solide</i></b>.\n<b>Interruption de héros</b> : quand un ennemi s'active, défaussez cette carte → cet ennemi gagne -X ATQ et -X MNG pour cette activation, X étant l'ATQ d'Angela.",
  // angela — Asgard's Assassin (Upgrade, x2)
  'an007': "<b>Ressource de héros</b> : inclinez Asgard's Assassin → générez une ressource [physical] <i>(si vous avez mis un sbire K.O. durant cette manche, générez plutôt [wild])</i>.",
  // angela — Siri's Dress (Upgrade)
  'an008': "Vous gagnez +4 points de vie.\nAngela gagne le trait [[AERIAL]].",
  // angela — Xiphos, Sword of the Stars (Upgrade)
  'an009': "<b><i>Limité</i></b>.\nAngela gagne +1 ATQ.\n<b>Réponse</b> : après qu'Angela a mis un sbire K.O., piochez une carte. <i>(Limite une fois par manche.)</i>",
  // angela — Banished from Asgard (Obligation)
  'an010': "<b><i>Donnez cette carte au joueur d'Aldrif Odinsdottir.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Aldrif Odinsdottir → retirez Banished from Asgard de la partie.\n• Défaussez 1 carte [[ASGARD]] que vous contrôlez. Vous êtes sonné. Si aucune carte n'a été défaussée de cette façon, cette carte gagne <b><i>Déferlement</i></b>. Défaussez cette obligation.",
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
  'ho002': "<b>Réponse</b> : après que Spider-Man est entré en jeu, placez un total de 2 cartes de statut sonné sur jusqu'à 2 ennemis.",
  // harry_osborn — Repulsor Blast (Event, x2)
  'ho003': "<b>Action de héros</b> <i>(attaque)</i> : sonnez un ennemi. Infligez 4 dégâts à CET ennemi.",
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
  'ho013': "<b><i>Donnez au joueur Harry Osborn.</i></b>\nVous êtes sonné.\n<b>Action d'alter ego</b> : inclinez Harry Osborn → défaussez cette carte. Renvoyez dans votre main l'amélioration [[TECH]] la plus au-dessus de votre pile de défausse.",
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
  'aa005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 1 dégât à un ennemi. Défaussez les 3 cartes du dessus du deck de rencontre. Pour chaque icône de boost défaussée de cette façon, infligez 1 dégât supplémentaire à CET ennemi. Pour chaque carte défaussée de cette façon sans icône de boost, sonnez ou désorientez un ennemi.",
  // agatha_harkness — Soul Harvest (Event, x2)
  'aa006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Soignez 2 dégâts d'Agatha Harkness. Défaussez la carte du dessus de votre deck. Si ses ressources imprimées comportent :\n• [wild] ou [physical] — sonnez CET ennemi.\n• [mental] ou [energy] — désorientez CET ennemi.",
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
  'aa016': "[star] Death ne peut pas être vaincue.\n<b><i>Vulnérable</i></b>. <i>(Défaussez ce personnage s'il est sonné ou désorienté.)</i>\n<i>(Sbire némésis d'Agatha Harkness.)</i>",
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
  'bt017': "Attachez-la à un allié. 1 max par allié.\n<b>Interruption forcée</b> : quand l'allié devrait être vaincu, soignez 1 dégât et donnez-lui une carte d'état Tenace.",
  // beast — Mecha-Beast (Upgrade, découverte mise de côté)
  'bt018': "Attachez-la à Beast.\nBeast gagne +1 CTR et +2 points de vie.",
  // beast — Unfinished Projects (Obligation)
  'bt019': "<b><i>Donnez-la au joueur Hank McCoy.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Défaussez 2 cartes d'amélioration/soutien en jeu → retirez Mutation Degeneration de la partie.\n• Inclinez votre identité et subissez 2 dégâts. Défaussez cette obligation.",
  // beast — Lizard-Fied Mutants (Minion nemesis, x2)
  'bt020': "<b><i>Garde</i></b>. <b><i>Patrouille</i></b>. <i>(Tant que ce sbire est engagé avec vous, vous ne pouvez pas attaquer le vilain, et vous ne pouvez pas contrer la manigance principale.)</i>\n<i>(Sbire némésis de Beast.)</i>",
  // beast — Dark Transformation (Treachery nemesis)
  'bt021': "<b>Une fois révélée</b> : défaussez les 5 cartes du dessus de votre deck. Vous subissez 1 dégât pour chaque carte spécifique au héros défaussée de cette façon.",
  // beast — Dark Beast (Minion nemesis)
  'bt022': "<b><i>Robuste</i></b>. <i>(Ce personnage ne peut être ni sonné ni désorienté.)</i>\n<b>Une fois révélé</b> : tous les alliés sont désorientés.\n<i>(Sbire némésis de Beast.)</i>",
  // beast — Mutant Science Program (SideScheme nemesis)
  'bt023': "<i>« Beast enlève des mutants et pratique sur eux des tests dangereux. »</i>\n<b>Une fois révélée</b> : placez 1 compteur de test sur cette manigance annexe pour chaque allié dans votre pile de défausse. S'il n'y a aucun allié dans votre pile de défausse, placez plutôt 2[per_hero] compteurs de test.\n<b>Réponse forcée</b> : chaque fois que vous piochez un allié dans votre main → retirez 1 compteur de test, défaussez l'allié, puis cherchez le sbire Lizard-Fied dans le deck de rencontre ou la pile de défausse et mettez-le en jeu.",
  // doctor_doom — Doctor Doom (Hero)
  'dd001a': "<i>Power Syphon</i> — <b>Réponse</b> : après que vous avez payé un événement [[SPELL]] avec une ressource [mental], placez 1 compteur de pouvoir ici (maximum 3).\n<i>Overwhelming Power</i> — <b>Action</b> : retirez 3 compteurs de pouvoir → vous gagnez <b><i>Vilain</i></b> jusqu'à la fin du round. Ignorez les effets de boost des cartes de boost qui vous sont distribuées.",
  // doctor_doom — Victor von Doom (AlterEgo)
  'dd001b': "Vous ne pouvez inclure aucun allié supplémentaire dans votre deck.\n<i>Master of Magic and Technology</i> — vous pouvez inclure jusqu'à 6 cartes [[TECH]] et/ou [[SPELL]] d'aspects autres que celui que vous avez choisi.",
  // doctor_doom — Victorious (Ally, signature)
  'dd002': "<b><i>Ténacité</i></b>.\n<b>Réponse</b> : après que Victorious est entrée en jeu, cherchez un événement [[SPELL]] dans votre deck et votre pile de défausse et ajoutez-le à votre main.",
  // doctor_doom — Doombot (Ally, x2)
  'dd003': "<b><i>Exigence</i></b> ([mental]). <i>(En payant cette carte, dépensez les ressources indiquées.)</i>\n<b><i>Ténacité</i></b>.\n<b>Interruption</b> : quand un ennemi vous attaque, jouez Doombot depuis votre main (en payant son coût) et déclarez-le défenseur sans l'incliner.",
  // doctor_doom — "This World Is Mine!" (Event, x3)
  'dd004': "<b>Action de héros</b> <i>(attaque)</i> : infligez 8 dégâts à un ennemi. Si vous avez payé cette carte uniquement avec des ressources [mental], cette attaque gagne <b><i>Déferlement</i></b> et <b><i>Perçage</i></b>.",
  // doctor_doom — "Doom Prevails" (Event, signature)
  'dd005': "<b>Action de héros</b> : regardez les 3 cartes du dessus du deck de rencontre. Infligez X dégâts répartis entre les ennemis en jeu, où X est le nombre d'icônes ([star] et [boost]) dans le champ de boost de ces cartes. Si vous avez payé cette carte uniquement avec des ressources [mental], retirez aussi X menaces réparties entre les manigances en jeu.",
  // doctor_doom — "Pain Is For Lesser Men!" (Event, x2)
  'dd006': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts d'une attaque, empêchez tous ces dégâts. Si vous avez payé cette carte uniquement avec des ressources [mental], sonnez et désorientez l'ennemi.",
  // doctor_doom — Unparalleled Genius (Resource [mental]x3, x2)
  'dd007': "",
  // doctor_doom — Doomstadt (Support, signature)
  'dd008': "Les événements glissés sous Doomstadt peuvent être joués comme s'ils étaient dans votre main.\n<b>Action</b> : inclinez Doomstadt → glissez un événement [[SPELL]] de votre main sous cette carte (maximum 3).",
  // doctor_doom — Doom's Time Platform (Upgrade, signature)
  'dd009': "<b>Action de héros</b> : inclinez Doom's Time Platform → choisissez :\n• Redressez Doctor Doom.\n• Mélangez 1 événement ou 1 amélioration de votre pile de défausse dans votre deck.",
  // doctor_doom — Doom's Armor (Upgrade, signature)
  'dd010': "Doctor Doom gagne +3 points de vie et le trait [[AERIAL]].\n<b>Interruption de héros</b> : si Doctor Doom a <b><i>Vilain</i></b>, quand il utilise un pouvoir de base, inclinez Doom's Armor → distribuez-vous 1 carte de boost supplémentaire.",
  // doctor_doom — Doom's Mask (Upgrade, signature)
  'dd011': "Doctor Doom gagne <b><i>Solide</i></b>.\n<b>Ressource</b> : inclinez Doom's Mask → générez une ressource [mental] (plutôt [mental][mental] si vous payez un événement [[SPELL]]).",
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
  'al023': "En Équipe (Alligator Loki et Honey Badger/Gabby Kinney). 1 max par deck.\n<b>Action</b> : sonnez et désorientez le vilain. Si vous ne le pouvez pas, redressez Alligator Loki ou Honey Badger.",

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
  'ls012': "<b><i>Donnez-la au joueur Lady Sif.</i></b>\nVous pouvez passer sous forme d'alter ego.\nSonnez Lady Sif. Sonnez OU désorientez Thor. Si vous ne le pouvez pas, désorientez Lady Sif. Défaussez cette obligation.",
  // lady_sif_nemesis — Captivating Wiles (SideScheme)
  'ls013': "<i>L'Enchanteresse nous manipule pour que nous fassions son sale travail !</i>\n<b>Interruption forcée</b> : quand la phase du joueur commence, inclinez l'identité du PREMIER joueur et placez 2 menaces sur la manigance principale.\n<hr />[star] <b>Boost</b> : placez 2 menaces sur la manigance principale.",
  // lady_sif_nemesis — Enchantress (Minion)
  'ls014': "<b>Interruption forcée</b> : quand Enchantress est attaquée, déclarez le héros engagé défenseur (sans l'incliner). Si vous ne le pouvez pas, annulez cette attaque et placez 2 menaces sur la manigance principale à la place. <i>(Limite d'une fois par phase.)</i>\n<i>(Sbire némésis de Lady Sif.)</i>",
  // lady_sif_nemesis — Skurge (Minion)
  'ls015': "<b><i>Travail d'équipe</i></b> ([[ASGARD]]). <b><i>Ténacité.</i></b>\n[star] <b>Interruption forcée</b> : quand Skurge vous attaque, il attaque le personnage que VOUS contrôlez ayant le moins de points de vie restants. Cette attaque gagne Déferlement et Perçant.\n<hr />[star] <b>Boost</b> : détruisez un allié que vous contrôlez.",
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
  'as003': "<b><i>Ténacité.</i></b>\n<b>Action</b> : défaussez Spider-Bot → retournez votre amélioration Spider Armor sur sa face [[OPERATIONAL]].",
  // armored_spidey — Burst It! (Event)
  'as004': "<b>Action de héros</b> : retirez TOUS les pions métal de Spider Armor → infligez 1 dégât à CHAQUE ennemi en jeu par pion métal retiré de cette façon.",
  // armored_spidey — Embrace It! (Event, x2)
  'as005': "<b>Réponse</b> : après que vous avez retiré un pion métal de Spider Armor, redressez votre identité.",
  // armored_spidey — Kick It! (Event, x2)
  'as006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Vous pouvez retirer 1 pion métal de Spider Armor pour sonner CET ennemi.",
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
  'as013': "Tant que Spider Armor a le trait [[OPERATIONAL]], Armored Spidey gagne Riposte 1 et Solide.\n<b>Réponse</b> : après avoir joué cette carte, si Spider Armor a le trait [[OPERATIONAL]], placez 1 pion métal dessus <i>(maximum 3)</i>.",
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
  'nt004': "<b>Réponse de héros</b> : après être passé sous forme de héros, si l'amélioration Battle Board a le trait :\n• [[VEHICLE]], désorientez un ennemi.\n• [[WEAPON]], sonnez un ennemi.",
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
  'yd002': "<b>Action de héros</b> <i>(attaque)</i> : sonnez un ennemi. PUIS, si CET ennemi a l'amélioration Yaka Arrow attachée, infligez-lui 6 dégâts.",
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
  'dr008': "Tant que cette carte est dans votre MAIN, chaque personnage que vous contrôlez gagne Robuste.\n<b>Interruption de héros</b> : quand une carte de rencontre devrait être révélée, défaussez-la à la place. S'il n'y a aucune icône de boost ([boost]) sur cette carte, donnez une carte de statut Tenace à un personnage amical.",
  // doctor_druid — Practice of Druidry (Event, x3)
  'dr009': "Tant que cette carte est dans votre MAIN, votre identité gagne +1 à chacun de ses pouvoirs de base.\n<b>Action de héros</b> : redressez Doctor Druid.",
  // doctor_druid — Ancient Order of Druids (Obligation)
  'dr010': "<b><i>Donnez-la au joueur Anthony Druid.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Anthony Druid → retirez Ancient Order of Druids de la partie.\n• Défaussez chaque événement spécifique à l'identité de votre main. Si aucun événement n'a été défaussé de cette façon, cette carte gagne Renfort. Défaussez cette obligation.",
  // doctor_druid_nemesis — * Nekra (Minion)
  'dr011': "Nekra gagne +1 ATQ et +1 PV pour chaque pion haine sur elle.\n<b>Réponse forcée</b> : après que Nekra attaque ou subit des dégâts, placez 1 pion haine sur elle <i>(maximum 5)</i>.\n<i>(Sbire némésis de Doctor Druid.)</i>",
  // doctor_druid_nemesis — Harness Violent Emotions (SideScheme)
  'dr012': "<i>Plus les émotions de Nekra sont violentes, plus elle devient forte.</i>\n<b>Une fois révélée</b> : cherchez Nekra dans le deck ET la défausse de rencontre, et révélez-la.\n<b>Interruption forcée</b> : quand Nekra vous attaque, défaussez 1 carte spécifique à l'identité de votre main.",
  // doctor_druid_nemesis — Emotionally Overwhelmed (Attachment, x2)
  'dr013': "Attachez-la à votre identité.\n<b>Interruption forcée</b> : quand votre tour commence, défaussez un événement spécifique à l'identité de votre main.\n<b>Action d'alter ego</b> : sonnez votre identité → défaussez cette carte.",
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
  'tt012': "Armadillo entre en jeu avec 2 pions carapace sur lui.\n<b>Réponse</b> : après qu'un sbire entre en jeu, retirez 1 pion carapace d'Armadillo → donnez une carte d'état Tenace à Armadillo.",
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
  'tt023': "Attachez-la à Master Pandemonium. Si vous ne pouvez pas, sonnez un personnage que vous contrôlez et rendez confus un personnage que vous contrôlez.\nMaster Pandemonium ne peut pas subir de dégâts.\n<b>Action de héros</b> : dépensez [energy][energy] → défaussez cette carte.",
  // texas_twister_nemesis — Soul Fragmentation (Treachery, x2)
  'tt024': "<b>Une fois révélée</b> : défaussez les 3 cartes du dessus de votre deck. Si une ressource [physical] a été défaussée ainsi, vous êtes sonné ; si une ressource [mental] a été défaussée ainsi, vous êtes confus ; si une ressource [wild] a été défaussée ainsi, inclinez votre identité.",
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
  'br006': "Prérequis ([energy]).\n<b>Action de héros</b> : choisissez un joueur → infligez 3 dégâts au vilain et à chaque sbire engagé avec ce joueur. Sonnez chaque ennemi ainsi blessé.",
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
  'tg010': "Vous gagnez +2 points de vie.\n<b>Réponse de héros</b> : après que vous engagez un sbire, donnez à Throg une carte d'état Tenace. Si vous ne pouvez pas, piochez 1 carte. <i>(Limite d'une fois par phase.)</i>",
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
  'sn014': "<b>Une fois révélée</b> : glissez la carte du dessus du deck rencontre sous votre identité <i>(jusqu'à un maximum de 3 cartes)</i>. Pour chaque icône ([star] et [boost]) dans le champ de boost des cartes glissées sous votre identité, subissez 1 dégât <i>(jusqu'à un maximum de 4 dégâts)</i>.\n<hr />\n[star] <b>Boost</b> : après cette activation, cet ennemi s'active de nouveau.",
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
  'bc005': "<b>Action de héros</b> <i>(contre)</i> : regardez les 3 cartes du dessus du deck rencontre et défaussez-en 1. Retirez 1 menace d'une manigance, plus 1 menace supplémentaire par icône ([star] et [boost]) dans le champ de boost de cette carte. Glissez-la sous Black Cat.",
  // black_cat — Lucky Hit (Event, x2)
  'bc006': "<b>Action de héros</b> <i>(attaque)</i> : défaussez les 2 cartes du dessus du deck rencontre et infligez 1 dégât à un ennemi par icône ([star] et [boost]) défaussée de cette façon. Glissez une de ces cartes sous Black Cat.",
  // black_cat — Misfortune (Event, x2)
  'bc007': "<b>Interruption de héros</b> : quand une carte de boost est retournée pendant l'activation d'un ennemi, glissez-la plutôt sous votre héros. Cet ennemi gagne -1 ATQ et -1 MNG pour cette activation par icône ([star] et [boost]) dans le champ de boost de cette carte.",
  // black_cat — * Black Cat's Claws (Upgrade)
  'bc008': "<b>Action de héros</b> <i>(attaque)</i> : inclinez Black Cat's Claws et défaussez la carte du dessus du deck rencontre → infligez à un ennemi autant de dégâts qu'il y a d'icônes dans le champ de boost de cette carte. Si ce nombre était 0, glissez-la sous Black Cat.",
  // black_cat — Grappling Hook (Upgrade, x2) — ⚠ HOMONYME de 08008 et 50069
  'bc009': "<b>Action de héros</b> : inclinez Grappling Hook et défaussez une carte glissée sous Black Cat → redressez Black Cat et glissez sous elle la carte du dessus du deck rencontre.",
  // black_cat — Ill Gotten Gains (Upgrade, x2)
  'bc010': "<b>Ressource</b> : inclinez cette carte → générez une ressource [wild] <i>([wild][wild] à la place pour une amélioration attachée)</i>.\n<b>Réponse</b> : après que vous défaussez du jeu une amélioration attachée portant le texte \"<b>Action de héros</b>\" ou \"<b>Réponse de héros</b>\", glissez-la sous votre identité.",
  // black_cat — Nine Lives (Upgrade, x2)
  'bc011': "<b>Interruption de héros</b> : quand Black Cat subirait des dégâts, quel qu'en soit le nombre, inclinez Nine Lives et défaussez la carte du dessus du deck rencontre → prévenez 1 de ces dégâts par icône ([star] et [boost]) dans le champ de boost de cette carte.",
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

  // ares — * Ares (Hero)
  'ar001a': "<i>Apporter la guerre</i> — <b>Action</b> : cherchez un sbire dans le deck rencontre et mettez-le en jeu engagé avec vous → piochez 2 cartes ou jouez un événement de votre main en ignorant son coût en ressources. <i>(Limite d'une fois par round.)</i>",
  // ares — * Ares (AlterEgo)
  'ar001b': "<i>Seigneur de la guerre</i> — Vous pouvez inclure dans votre deck jusqu'à 5 améliorations [[TACTIC]] d'aspects autres que votre aspect choisi.\n<b>Interruption</b> : quand vous changez de forme, cherchez une carte [[TACTIC]] dans votre deck et ajoutez-la à votre main.",
  // ares — Spray and Pray (Event, x2)
  'ar002': "<b>Action de héros</b> : effectuez l'attaque suivante 5 fois contre les cibles de votre choix :\n<i>(attaque)</i> : infligez 1 dégât à un ennemi.",
  // ares — To Battle! (Event, x3)
  'ar003': "<b>Action de héros</b> : choisissez deux des options suivantes :\n• Cherchez une amélioration [[TACTIC]] ou [[WEAPON]] dans votre deck et votre défausse et ajoutez-la à votre main.\n• Redressez une amélioration spécifique au héros que vous contrôlez.\n• Redressez Ares.",
  // ares — * Ares' Axe (Upgrade)
  'ar004': "Restreinte.\n<b>Interruption de héros</b> : quand Ares effectue une attaque de base contre un ennemi, inclinez la Hache d'Ares → vous gagnez +1 ATQ pour cette attaque pour chaque amélioration attachée à cet ennemi. Cette attaque gagne <b><i>Perçant</i></b>.",
  // ares — * Ares' Battle Helm (Upgrade)
  'ar005': "<b>Réponse de héros</b> : après qu'Ares attaque et vainc un ennemi, inclinez le Casque de guerre d'Ares et choisissez une manigance → retirez 1 menace de cette manigance pour chaque point de dégât excédentaire infligé à cet ennemi par cette attaque.",
  // ares — Feint (Upgrade, x3)
  'ar006': "Attachez-la à un ennemi. Max. 1 par ennemi.\n<b>Interruption de héros forcée</b> <i>(attaque/défense)</i> : quand l'ennemi auquel cette carte est attachée initie une attaque, défaussez Feinte → cet ennemi a -2 ATQ pour cette attaque. Infligez 2 dégâts à cet ennemi.",
  // ares — God of War (Upgrade)
  'ar007': "<b>Réponse de héros</b> : après qu'un sbire entre en jeu, cherchez dans votre deck une amélioration [[TACTIC]] qui peut être attachée à ce sbire et jouez-la sur ce sbire. <i>(Limite d'une fois par phase.)</i>",
  // ares — Reeling (Upgrade, x2)
  'ar008': "Attachez-la à un sbire. Max. 1 par ennemi.\nLes attaques contre le sbire auquel cette carte est attachée gagnent <b><i>Déferlement</i></b>. Augmentez de 2 le montant des dégâts excédentaires infligés à cet ennemi.",
  // ares — Sundered (Upgrade, x2)
  'ar009': "Attachez-la à un sbire. Max. 1 par ennemi.\nAugmentez de 1 le montant des dégâts que l'ennemi auquel cette carte est attachée subit de chaque attaque.",
  // ares — Ire of Athena (Obligation)
  'ar010': "<b><i>Donnez-la au joueur d'Ares.</i></b>\nAugmentez de 1 le coût de chaque carte [[TACTIC]] que vous jouez.\n<b>Action d'alter ego</b> : inclinez votre alter ego ou défaussez une carte [[TACTIC]] de votre main → défaussez cette carte.",
  // ares — Athena's Guidance (SideScheme némésis)
  'ar011': "<i>Piquée au vif par sa rivalité avec Ares, l'autre dieu de la guerre, Athéna offre sa sagesse et ses tactiques à l'ennemi.</i>\nLes sbires gagnent <b><i>Attaque éclair</i></b> et <b><i>Ténacité</i></b>.\n<hr />\n[star] <b>Boost</b> : donnez une carte de boost supplémentaire à l'ennemi qui s'active.",
  // ares — * Athena (Minion némésis)
  'ar012': "<b><i>Riposte 1. Ténacité.</i></b>\nAthéna ne peut pas avoir d'améliorations [[TACTIC]] attachées.\n<i>(Sbire némésis d'Ares.)</i>\n<hr />\n[star] <b>Boost</b> : après cette activation, distribuez-vous 1 carte rencontre face cachée.",
  // ares — * Aegis Breastplate (Attachment némésis)
  'ar013': "Attachez-la à un sbire. Sinon, attachez-la au vilain.\n<b>Interruption forcée</b> : quand l'ennemi auquel cette carte est attachée devrait subir des dégâts, quel qu'en soit le montant, placez-les ici à la place et infligez autant de dégâts à l'attaquant. S'il y a 5 dégâts ou plus ici, défaussez cette carte.",
  // ares — Lead the Charge (Treachery némésis, x2)
  'ar014': "<b>Une fois révélée</b> : chaque sbire engagé avec un joueur s'active contre lui. Chaque joueur contre qui aucun sbire ne s'est activé de cette façon cherche un sbire dans le deck rencontre et sa défausse et le met en jeu engagé avec lui. Donnez une carte de boost face cachée à chaque sbire.",

  // blade — * Blade (Hero)
  'bl001a': "[star] <i>Ruée sanguine</i> — <b>Réponse</b> : après que Blade utilise un pouvoir de base, retirez-lui 1 pion de sang → redressez Blade. <i>(Limite d'une fois par phase.)</i>",
  // blade — * Eric Brooks (AlterEgo)
  'bl001b': "<i>Tueur</i> — <b>Mise en place</b> : mélangez chaque carte de votre set némésis autre que Dracula dans le deck rencontre.\n<i>Injection de sérum</i> — <b>Action</b> : dépensez une ressource [physical] → placez 2 pions de sang sur Eric Brooks. <i>(Limite d'une fois par round.)</i>",
  // blade — Gear Up (Event, x2)
  'bl002': "Réduisez de 1 le coût pour jouer cette carte si vous êtes sous forme d'alter ego.\n<b>Action</b> : cherchez une carte [[ATTACK]], [[ITEM]], [[TACTIC]] ou [[WEAPON]] dans votre deck et votre défausse et ajoutez-la à votre main.",
  // blade — Go for the Heart (Event, x3)
  'bl003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Cette attaque gagne <b><i>Perçant</i></b>. Vous pouvez incliner une amélioration [[WEAPON]] que vous contrôlez pour sonner cet ennemi.",
  // blade — On the Hunt (Event, x2)
  'bl004': "<b>Action de héros</b> <i>(contre)</i> : cherchez un sbire dans le deck rencontre et mettez-le en jeu engagé avec vous → retirez 3 menaces d'une manigance. Si ce sbire a le trait [[VAMPIRE]], piochez 1 carte.",
  // blade — Vampire Bite (Event, x2)
  'bl005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Choisissez de soigner 2 dégâts de Blade ou de placer 1 pion de sang sur lui (faites les deux à la place si cette attaque vainc cet ennemi).",
  // blade — Vampiric Reflexes (Event, x2)
  'bl006': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts d'une attaque, quel qu'en soit le montant, empêchez tous ces dégâts. Vous pouvez incliner une amélioration [[WEAPON]] que vous contrôlez pour gagner <b><i>Riposte 1</i></b> jusqu'à la fin du round.",
  // blade — Bandolier of Stakes (Upgrade)
  'bl007': "Utilisations (3 pions pieu).\n<b>Interruption de héros</b> : quand un héros attaque, retirez 1 pion pieu d'ici → cette attaque inflige 1 dégât supplémentaire et gagne <b><i>Perçant</i></b>.",
  // blade — * Blade's Sword (Upgrade)
  'bl008': "Restreinte.\n<b>Interruption de héros</b> : quand Blade effectue une attaque avec <b><i>Perçant</i></b>, augmentez de 1 le montant des dégâts que cette attaque inflige.",
  // blade — Daywalker (Upgrade)
  'bl009': "Vous avez +3 points de vie et vos attaques Vampire Bite gagnent <b><i>Perçant</i></b>.\n<b>Interruption de héros</b> : quand vous devriez déclencher la capacité <i>Ruée sanguine</i> de Blade, subissez 2 dégâts → résolvez cette capacité sans payer son coût à la place.",
  // blade — Predatory Instincts (Upgrade)
  'bl010': "Blade a +1 DEF.\n<b>Réponse de héros</b> : après qu'un ennemi entre en jeu, inclinez Instincts de prédateur → cherchez un exemplaire de Vampire Bite dans votre deck et votre défausse et ajoutez-le à votre main.",
  // blade — The Thirst (Obligation)
  'bl011': "<b><i>Donnez-la au joueur d'Eric Brooks.</i></b>\nUtilisations (3 pions soif).\n<b>Interruption forcée</b> : quand votre tour commence, retirez 1 pion de sang de votre identité pour retirer 1 pion soif d'ici. Si vous ne pouvez pas, subissez 2 dégâts.",
  // blade — Blood Hunt (SideScheme némésis)
  'bl012': "<i>Dracula a lâché une horde de nouveaux vampires, et ils ont soif de sang.</i>\nLes sbires non-[[VAMPIRE]] gagnent le trait [[VAMPIRE]] et le texte suivant : « Les attaques avec <b><i>Perçant</i></b> infligent le double de dégâts à ce sbire. » Les sbires [[VAMPIRE]] ont +3 points de vie et gagnent <b><i>Travail d'équipe</i></b> ([[VAMPIRE]]).\n<b>Réponse</b> : après qu'un sbire [[VAMPIRE]] est vaincu, retirez 2 menaces de cette manigance.",
  // blade — * Dracula (Minion némésis)
  'bl013': "Les attaques avec <b><i>Perçant</i></b> infligent le double de dégâts à Dracula.\n[star] <b>Réponse forcée</b> : après que Dracula attaque et blesse un personnage, soignez tous les dégâts de Dracula. Si vous ne pouvez pas, donnez-lui une carte d'état Tenace.\n<i>(Sbire némésis de Blade.)</i>",
  // blade — Vampire (Minion némésis, x2)
  'bl014': "Les attaques avec <b><i>Perçant</i></b> infligent le double de dégâts au Vampire.\n[star] <b>Réponse forcée</b> : après que le Vampire attaque et blesse un personnage, soignez tous les dégâts du Vampire. Si aucun dégât n'a été soigné ainsi, donnez au Vampire une carte d'état Tenace.",
  // blade — Bandolier of Stakes (Attachment némésis)
  'bl015': "<b><i>Déferlement.</i></b> Utilisations (3 pions pieu).\n<b>Une fois révélée</b> : vous pouvez dépenser 1 ressource de n'importe quel type pour attacher cette carte à votre identité. Sinon, défaussez cette carte.\n<b>Interruption de héros</b> : quand votre héros effectue une attaque de base, retirez 1 pion pieu d'ici → votre héros a +1 ATQ pour cette attaque et cette attaque gagne <b><i>Perçant</i></b>.",
  // blade — Embraced (Attachment némésis, x2)
  'bl016': "Le sbire auquel cette carte est attachée gagne le trait [[VAMPIRE]] et a +X points de vie, X étant ses points de vie imprimés. Les attaques avec <b><i>Perçant</i></b> infligent le double de dégâts à ce sbire.\n<b>Une fois révélée</b> : cherchez un sbire non-[[VAMPIRE]] dans le deck rencontre, révélez-le et attachez-lui Étreint.",
  // blade — Turned (Attachment némésis)
  'bl017': "L'allié auquel cette carte est attachée gagne <b><i>Traître</i></b>, le trait [[VAMPIRE]] et le texte suivant : « Les attaques avec <b><i>Perçant</i></b> infligent le double de dégâts à cet ennemi. » et a +3 points de vie.\n<b>Une fois révélée</b> : attachez-la à l'allié ayant le moins de points de vie restants. Si vous ne pouvez pas, cette carte gagne <b><i>Déferlement</i></b>. Soignez tous les dégâts de cet allié.",
  // spider_man_2099 — * Spider-Man (Hero)
  'sm001a': "[star] <i>Accélération</i> — <b>Réponse</b> : après que votre héros utilise un pouvoir de base, défaussez les cartes du dessus de votre deck jusqu'à en défausser un événement. Vous pouvez jouer cet événement. Placez chaque autre carte défaussée ainsi sous votre deck, dans l'ordre où vous les avez défaussées. <i>(Limite d'une fois par phase.)</i>",
  // spider_man_2099 — * Miguel O'Hara (AlterEgo)
  'sm001b': "[star] <i>Guérison accélérée</i> — <b>Réponse</b> : après avoir effectué une récupération de base, défaussez 1 carte de votre main → redressez Miguel O'Hara. <i>(Limite d'une fois par round.)</i>",
  // spider_man_2099 — * Ghost Rider (Ally)
  'sm002': "<b>Réponse</b> : après que Ghost Rider est défaussé par votre capacité <i>Accélération</i>, infligez 1 dégât à un ennemi.\n<b>Interruption</b> : quand Ghost Rider est vaincu, placez-le sous le deck de son propriétaire.",
  // spider_man_2099 — Accelerated Decoy (Event, x2)
  'sm003': "<b>Action de héros</b> : choisissez de désorienter un ennemi ou de donner une carte d'état Tenace à votre héros. Si vous avez joué cette carte grâce à votre capacité <i>Accélération</i>, faites les deux à la place.",
  // spider_man_2099 — Rapid Strikes (Event, x2)
  'sm004': "<b>Action de héros</b> : effectuez l'attaque suivante X fois, jusqu'à un maximum de 3 (une fois de plus si vous avez joué cette carte grâce à votre capacité <i>Accélération</i>) :\n• Infligez 2 dégâts à un ennemi. Cette attaque ignore le mot-clé <b><i>Garde</i></b>.",
  // spider_man_2099 — Shock and Awe (Event, x2)
  'sm005': "<b>Action de héros</b> <i>(attaque)</i> : sonnez un ennemi et infligez-lui 2 dégâts (4 dégâts à la place si cet ennemi n'a pas été sonné ainsi). Si vous avez joué cette carte grâce à votre capacité <i>Accélération</i>, sonnez chaque sbire en jeu.",
  // spider_man_2099 — Wall Crawling (Event, x2)
  'sm006': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance (3 menaces à la place si vous avez joué cette carte grâce à votre capacité <i>Accélération</i>). Vous pouvez placer cet événement sous votre deck.",
  // spider_man_2099 — * Lyla (Support)
  'sm007': "<b>Action</b> : inclinez Lyla → choisissez un événement dans votre main (dans votre main ou votre défausse à la place si vous êtes sous forme d'alter ego) et échangez-le avec la carte du dessus de votre deck.",
  // spider_man_2099 — Accelerated Vision (Upgrade)
  'sm008': "Vous pouvez résoudre votre capacité <i>Accélération</i> une fois de plus par phase (mais toujours une seule fois par déclenchement).\nQuand vous résolvez votre capacité <i>Accélération</i>, vous pouvez continuer à défausser jusqu'à défausser un événement différent, et jouer celui-ci à la place.",
  // spider_man_2099 — Fangs and Talons (Upgrade)
  'sm009': "Votre héros gagne +1 ATQ.\n<b>Interruption de héros</b> : quand vous jouez un événement [[ATTACK]] grâce à votre capacité <i>Accélération</i>, inclinez Fangs and Talons → augmentez de 1 les dégâts infligés par cet événement, et ses attaques gagnent <b><i>Perçant</i></b>.",
  // spider_man_2099 — Hyper-Agility (Upgrade)
  'sm010': "Votre héros gagne +1 DEF.\n<b>Réponse de héros</b> : après avoir résolu la capacité <i>Accélération</i> de votre héros sans jouer d'événement, réduisez de 1 les dégâts que vous subissez des attaques jusqu'à la fin du round. <i>(Limite d'une fois par phase.)</i>",
  // spider_man_2099 — Spinnerets (Upgrade)
  'sm011': "<b>Réponse de héros</b> : après avoir résolu la capacité <i>Accélération</i> de votre héros, placez 1 pion de toile ici (jusqu'à un maximum de 2).\n<b>Ressource de héros</b> : retirez X pions de toile d'ici → générez X ressources [wild] pour un événement.",
  // spider_man_2099 — Web Cape (Upgrade)
  'sm012': "Votre héros gagne le trait [[AERIAL]].\n<b>Réponse de héros</b> : après avoir résolu la capacité <i>Accélération</i> de votre héros, inclinez Web Cape → redressez votre héros.",
  // spider_man_2099 — Future in Crisis (Obligation)
  'sm013': "<b><i>Donnez-la au joueur de Miguel O'Hara.</i></b>\n<b>Action</b> : inclinez votre identité → retirez Future in Crisis de la partie.",
  // spider_man_2099 — Containment Breach (SideScheme, némésis)
  'sm014': "<i>Electro s'est échappé de son centre de confinement, et compte se venger de ses geôliers une fois rechargé !</i>\n<b>Une fois révélée</b> : chaque joueur défausse les 4 cartes du dessus de son deck et place ici autant de menaces qu'il y avait de ressources [energy] défaussées ainsi.",
  // spider_man_2099 — * Electro (Minion, némésis)
  'sm015': "<b><i>Coup Rapide</i></b>. <b><i>Riposte</i></b> 1.\n[star] <b>Réponse forcée</b> : après qu'Electro vous attaque, défaussez les 4 cartes du dessus de votre deck. Subissez 1 dégât indirect pour chaque ressource [energy] défaussée ainsi.",
  // spider_man_2099 — Power Surge (Treachery, némésis, x2)
  'sm016': "<b>Une fois révélée</b> : défaussez les 5 cartes du dessus de votre deck. Subissez autant de dégâts indirects qu'il y avait de ressources [energy] défaussées ainsi. Si 2 dégâts ou moins ont été infligés ainsi, cette carte gagne <b><i>Déferlement</i></b>.\n[star] <b>Renfort</b> : cette carte gagne +1 icône de renfort ([boost]) pour chaque ressource [energy] dans votre main.",
  // spider_man_2099 — Charged (Attachment, némésis)
  'sm017': "<b><i>Attachez-la à votre identité.</i></b>\n<b>Réponse forcée</b> : après que vous défaussez un nombre quelconque de cartes du dessus de votre deck, subissez 1 dégât indirect.\n<b>Action de héros</b> : choisissez de subir 2 dégâts indirects ou de défausser une carte que vous contrôlez portant une ressource [energy] imprimée → défaussez cette carte.",
  // superior_spider_man — * Spider-Man (Hero)
  'su001a': "<i>Sens d'araignée</i> — <b>Interruption</b> : quand le vilain ou un sbire Machiavélique lance une attaque contre vous, piochez 1 carte.",
  // superior_spider_man — * Peter Parker (AlterEgo)
  'su001b': "<i>Maître planificateur</i> — <b>Action</b> : attachez 1 carte de votre main, face cachée, à Contingency Plan (jusqu'à un maximum de 1) → piochez 1 carte. <i>(Limite d'une fois par round.)</i>",
  // superior_spider_man — * Elliot Tolliver (AlterEgo, second au choix)
  'su001c': "<i>Maître planificateur</i> — <b>Action</b> : attachez 1 carte de votre main, face cachée, à Contingency Plan (jusqu'à un maximum de 1) → piochez 1 carte. <i>(Limite d'une fois par round.)</i>",
  // superior_spider_man — Spiderlings (Ally)
  'su002': "[star] <b>Interruption</b> : quand Spiderlings contre, pistez un sbire au lieu de retirer de la menace.\n[star] Spiderlings subit -1 dégât consécutif après avoir attaqué un sbire pisté.",
  // superior_spider_man — Agility (Event, x2)
  'su003': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous subiriez un nombre quelconque de dégâts, évitez 3 de ces dégâts (évitez-les tous à la place si vous avez le trait [[AERIAL]]).",
  // superior_spider_man — Brutal Efficiency (Event, x3)
  'su004': "<b>Action de héros</b> <i>(attaque)</i> : placez X menaces sur la manigance principale (jusqu'à un maximum de 3) → infligez 3X dégâts à un ennemi. Cette attaque gagne <b><i>Fracassant</i></b>.",
  // superior_spider_man — Webbed Up (Event, x2)
  'su005': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Sonnez un sbire (sonnez un ennemi à la place si vous avez payé cette carte avec une ressource [wild]).",
  // superior_spider_man — * Anna Maria Marconi (Support)
  'su006': "<b>Action d'alter ego</b> : inclinez Anna Maria Marconi → choisissez de soigner 3 dégâts de votre identité ou de réduire de 1 le coût de la prochaine amélioration jouée ce round.",
  // superior_spider_man — Facial Recognition Uplink (Upgrade)
  'su007': "Tant qu'un sbire pisté est en jeu, votre héros gagne +1 CTR.\n<b>Réponse de héros</b> <i>(contre)</i> : après qu'un sbire entre en jeu, pistez-le.",
  // superior_spider_man — Mastermind (Upgrade)
  'su008': "<b>Action</b> : attachez une carte de votre main, face cachée, à Contingency Plan (jusqu'à un maximum de 1).\n<b>Réponse de héros</b> : après avoir vaincu un sbire portant 2 menaces ou plus, regardez les 3 cartes du dessus du deck rencontre. Défaussez-en 1.",
  // superior_spider_man — Mechanical Arms (Upgrade)
  'su009': "<b>Interruption de héros</b> <i>(contre)</i> : quand vous effectuez une attaque de base contre un sbire, pistez ce sbire.\n<b>Réponse de héros</b> : après avoir utilisé un pouvoir de base, inclinez Mechanical Arms → redressez votre héros.",
  // superior_spider_man — Spider-Bot (Upgrade, x2)
  'su010': "Utilisations (3 pions de surveillance).\n<b>Action de héros</b> <i>(contre)</i> : inclinez Spider-Bot et retirez-en 1 pion de surveillance → pistez un sbire ou retirez 1 menace d'une manigance.",
  // superior_spider_man — Web-Shooters (Upgrade)
  'su011': "Utilisations (3 pions de toile).\nVotre héros gagne le trait [[AERIAL]].\n<b>Ressource de héros</b> : inclinez Web-Shooters et retirez-en 1 pion de toile → générez une ressource [wild].",
  // superior_spider_man — Contingency Plan (Upgrade, 16e carte)
  'su012': "Permanent. Mise en place.\nLa carte attachée ici peut être jouée comme si elle était dans votre main.\n<b>Action</b> : défaussez la carte attachée.",
  // superior_spider_man — Ghost of a Conscience (Obligation de Peter Parker)
  'su013': "<b><i>Donnez-la au joueur de Peter Parker.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Peter Parker → retirez Ghost of a Conscience de la partie.\n• Vous êtes sonné et désorienté. Si vous étiez déjà sonné et désorienté, cette carte gagne <b><i>Déferlement</i></b>. Défaussez cette obligation.",
  // superior_spider_man — Crisis of Conscience (Obligation d'Elliot Tolliver)
  'su014': "<b><i>Donnez-la au joueur d'Elliot Tolliver.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Elliot Tolliver → retirez Crisis of Conscience de la partie.\n• Vous êtes sonné et désorienté. Si vous étiez déjà sonné et désorienté, cette carte gagne <b><i>Déferlement</i></b>. Défaussez cette obligation.",
  // superior_spider_man — Goblin Protocol (SideScheme, némésis)
  'su015': "<i>Le réseau de surveillance de Spider-Man a été compromis : les criminels passent désormais inaperçus !</i>\nLa menace posée sur les sbires pistés compte dans le seuil de la manigance principale. La menace posée ici ne peut être retirée ni par les Spider-Bots ni par le pistage.",
  // superior_spider_man — * Hobgoblin (Minion, némésis)
  'su016': "Machiavélique.\n[star] <b>Réponse forcée</b> : après qu'Hobgoblin vous attaque, subissez 2 dégâts indirects.\n<i>(Sbire némésis de Spider-Man.)</i>\n<hr />\n[star] <b>Renfort</b> : subissez 2 dégâts indirects.",
  // superior_spider_man — Lunatic Laugh (Treachery, némésis)
  'su017': "<b>Une fois révélée</b> : subissez 2 dégâts indirects. Désorientez chaque personnage blessé ainsi.\n<hr />\n[star] <b>Renfort</b> : chaque joueur subit 1 dégât indirect.",
  // superior_spider_man — Goblin Glider (Attachment, némésis)
  'su018': "Attachez-la à l'ennemi ayant le plus de points de vie imprimés et ne portant pas déjà un Goblin Glider. Si vous ne pouvez pas, cette carte gagne <b><i>Déferlement</i></b>.\n<b>Action de héros</b> : dépensez [energy][energy] → défaussez cette carte.",
  // superior_spider_man — Pumpkin Bombs (Attachment, némésis)
  'su019': "Attachez-la à Hobgoblin. Sinon, attachez-la au vilain.\n[star] <b>Réponse forcée</b> : après que l'ennemi auquel elle est attachée vous attaque, défaussez Pumpkin Bombs et subissez 2 dégâts indirects.\n<b>Action de héros</b> : dépensez [physical][physical] → défaussez cette carte.",
  // ---------------------------------------------------------------------
  // venomized (ekAugust, set 168) — SIXIEME ASPECT, noir.
  // Les 8 evenements « Symbiotic » sont les jumeaux de cartes officielles :
  // leur francais reprend celui de l'originale, au titre pres.
  // ---------------------------------------------------------------------
  // venomized — Agent Anti-Venom (Ally)
  'vz001': "<b>Réponse</b> : après qu'Agent Anti-Venom entre en jeu, défaussez des cartes du dessus de votre deck jusqu'à défausser un allié partageant un [[trait]] avec lui → mettez cet allié en jeu.",
  // venomized — Codex (Ally)
  'vz002': "<b>Réponse</b> : après que Codex est vaincu pendant la phase du joueur, défaussez la carte du dessus de votre deck. Si cette carte est une carte Venomized <i>(noire)</i>, renvoyez Codex dans votre main.",
  // venomized — Mania (Ally)
  'vz003': "<b>Réponse</b> : après que Mania est vaincue pendant la phase du joueur, piochez 1 carte.",
  // venomized — Red Goblin (Ally)
  'vz004': "<b>Réponse</b> : après qu'un sbire entre en jeu, inclinez Red Goblin → infligez 1 dégât à cet ennemi.",
  // venomized — Sleeper (Ally)
  'vz005': "<b>Réponse</b> : après que Sleeper est vaincu pendant la phase du joueur, désorientez le vilain.",
  // venomized — Venom (Ally)
  'vz006': "Venom gagne +1 ATQ pour chaque carte Venomized <i>(noire)</i> glissée sous lui.\n<b>Réponse</b> : après avoir vaincu un sbire, glissez une carte de votre main sous cette carte.",
  // venomized — Backed into a Corner (Event)
  'vz007': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts, quel qu'en soit le nombre, empêchez un nombre de dégâts égal à votre DEF plus votre ATQ.",
  // venomized — Black Webbing (Event)
  'vz008': "<b>Action de héros</b> : choisissez un sbire engagé avec un autre joueur → sonnez cet ennemi et engagez-le.",
  // venomized — "Can't Escape Us!" (Event)
  'vz009': "<b>Action</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Inclinez une carte [[SYMBIOTE]] que vous contrôlez → infligez 3 dégâts supplémentaires à cet ennemi.",
  // venomized — Dive into Danger (Event)
  'vz010': "<b>Action de héros</b> <i>(contre)</i> : retirez d'une manigance un nombre de menaces égal à votre CTR plus votre DEF.",
  // venomized — Feed the Hunger (Event)
  'vz011': "<b>Action de héros</b> : mettez K.O. un sbire non-[[ELITE]] engagé avec vous → soignez sur votre identité un nombre de dégâts égal au total des points de vie de cet ennemi.",
  // venomized — Forceful Bonding (Event)
  'vz012': "<b>Action d'alter ego</b> : défaussez les X cartes du dessus de votre deck. Si l'une de ces cartes est une carte [[SYMBIOTE]] ou Venomized <i>(noire)</i>, passez sous forme de héros.",
  // venomized — Inner Strength (Event)
  'vz013': "<b>Action de héros</b> <i>(attaque)</i> : infligez à un ennemi un nombre de dégâts égal à votre ATQ plus votre CTR.",
  // venomized — Scared of the Dark (Event)
  'vz014': "1 max par round.\n<b>Action de héros</b> : retirez une carte d'état Tenace d'un ennemi → sonnez cet ennemi.",
  // venomized — Stronger Together (Event)
  'vz015': "1 max par round.\n<b>Action de héros</b> : redressez 2 personnages alliés partageant un [[trait]].",
  // venomized — Symbiotic Drop Kick (Event)
  'vz016': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Si vous avez payé cette carte en n'utilisant que des ressources [physical], sonnez cet ennemi et piochez 1 carte.",
  // venomized — Symbiotic For Justice! (Event)
  'vz017': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance (4 menaces à la place si vous avez payé cette carte en utilisant une ressource [mental]).",
  // venomized — Symbiotic Go All Out (Event)
  'vz018': "Prérequis ([energy]). <i>(Lorsque vous payez cette carte, dépensez les ressources indiquées.)</i>\n<b>Action de héros</b> <i>(attaque)</i> : inclinez votre héros → infligez à un ennemi un nombre de dégâts égal au total des valeurs de CTR, d'ATQ et de DEF de votre héros.",
  // venomized — Symbiotic Multitasking (Event)
  'vz019': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance. Si vous avez payé cette carte en utilisant une ressource [mental], retirez 2 menaces d'une autre manigance.",
  // venomized — Symbiotic Not Today! (Event)
  'vz020': "<b>Interruption de héros</b> <i>(défense)</i> : quand votre héros se défend contre une attaque, il gagne +2 DEF pour cette attaque. Si vous ne subissez aucun dégât de cette attaque, retirez 2 menaces d'une manigance.",
  // venomized — Symbiotic One By One (Event)
  'vz021': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Si cette attaque met cet ennemi K.O., infligez 2 dégâts à un ennemi.",
  // venomized — Symbiotic Perseverance (Event)
  'vz022': "<b>Réponse de héros</b> : après avoir changé de forme, donnez à votre héros une carte d'état Tenace.",
  // venomized — Symbiotic Sneak Attack (Event)
  'vz023': "<b>Action</b> : choisissez dans votre main un allié partageant un [[trait]] avec votre identité → mettez cet allié en jeu. Si cet allié est encore en jeu à la fin de la phase, défaussez-le.",
  // venomized — In the Thick of It (PlayerSideScheme)
  'vz024': "Victoire 0.\n<b>Une fois déjouée</b> : chaque joueur peut chercher dans son deck et dans sa pile de défausse une amélioration ayant le trait [[SYMBIOTE]] et la mettre en jeu. <i>(Mélangez.)</i>",
  // venomized — Gluttony (Resource)
  'vz025': "1 max par deck.\n<b>Réponse</b> : après avoir dépensé cette carte, redressez votre héros.",
  // venomized — Symbiote Infusion (Resource)
  'vz026': "2 max par deck.\n<b>Interruption de héros</b> : quand vous dépensez cette carte pour jouer une carte [[SYMBIOTE]], piochez 1 carte.",
  // venomized — The Power of the Bond (Resource)
  'vz027': "2 max par deck.\nDoublez le nombre de ressources générées par cette carte lorsque vous payez une carte Venomized <i>(noire)</i>.",
  // venomized — Alchemax (Support)
  'vz028': "<b>Action d'alter ego</b> : inclinez Alchemax → ajoutez à votre main la carte d'aspect située le plus haut dans votre pile de défausse.",
  // venomized — Doctor Steven (Support)
  'vz029': "<b>Action d'alter ego</b> : inclinez Doctor Steven → réduisez de 1 le coût de la prochaine carte Venomized <i>(noire)</i> ou [[SYMBIOTE]] jouée pendant cette phase.",
  // venomized — Durable Physiology (Upgrade)
  'vz030': "Utilisations (2 pions de klyntar).\n<b>Interruption de héros</b> : quand un sbire devrait vous attaquer, inclinez cette carte et retirez-en 1 pion de klyntar → réduisez de 1 tous les dégâts qui vous sont infligés pendant ce round.",
  // venomized — First Contact (Upgrade)
  'vz031': "Jouez-la sous le contrôle de n'importe quel joueur. 1 max par joueur.\nVotre héros gagne +1 ATQ, +1 CTR et +1 DEF.",
  // venomized — Klyntar Tendrils (Upgrade)
  'vz032': "Utilisations (3 pions de klyntar).\n<b>Action de héros</b> : inclinez cette carte et retirez-en 1 pion de klyntar → choisissez soit d'infliger 1 dégât à un ennemi, soit de retirer 1 menace d'une manigance. Puis, soignez 1 dégât de votre identité.",
  // venomized — Symbiotic Bond (Upgrade)
  'vz033': "1 max par joueur.\n<b>Ressource</b> : subissez 1 dégât et inclinez cette carte → générez une ressource [wild].",
  // venomized — Urban Camouflage (Upgrade)
  'vz034': "1 max par joueur.\n<b>Interruption de héros</b> : quand un ennemi devrait vous attaquer, subissez 1 dégât et défaussez cette carte → donnez à votre héros une carte d'état Tenace et désorientez cet ennemi.",
  // venomized — "You Are What You Eat" (Upgrade)
  'vz035': "1 max par joueur.\n<b>Réponse</b> : après avoir soigné des dégâts de votre identité, inclinez cette carte → piochez 1 carte.",
  // venomized — Flash Fire (Treachery, Venomized Weakness)
  'vz036': "Faiblesse. <i>(Elle commence la partie dans votre deck et se défausse dans votre pile de défausse.)</i>\n<b>Réponse forcée</b> : après que cette carte entre dans votre main, subissez 1 dégât indirect. <i>(Vous pouvez défausser cette carte de votre main à la fin de la phase du joueur comme n'importe quelle autre carte.)</i>",
  // venomized — Sensory Overload (Treachery, Venomized Weakness)
  'vz037': "Faiblesse. <i>(Elle commence la partie dans votre deck et se défausse dans votre pile de défausse.)</i>\n<b>Réponse forcée</b> : après que cette carte entre dans votre main, placez 1 menace sur chaque manigance. <i>(Vous pouvez défausser cette carte de votre main à la fin de la phase du joueur comme n'importe quelle autre carte.)</i>",

  // ==== IRON PATRIOT (Neptune, set 142) ====
  // iron_patriot — Iron Patriot (Hero)
  'ip001a': "Chaque allié que vous contrôlez gagne le trait [[REGISTERED]].\n<i>Force autoritaire</i> — <b>Réponse</b> : après avoir attaqué et vaincu un sbire, vous pouvez le mélanger dans le deck REGISTERED. <i>(Limite d'une fois par phase.)</i>",
  // iron_patriot — Norman Osborn (AlterEgo)
  'ip001b': "<i>Nouvel ordre mondial</i> — <b>Mise en place</b> : pendant la construction du deck, votre deck ne peut contenir aucun allié d'aspect. Norman Osborn commence la partie avec le deck REGISTERED et la manigance secondaire Registration Act en jeu. <i>(Voir l'insert.)</i>\n<b>Action</b> : inclinez Norman Osborn → résolvez la capacité « Spécial » d'1 allié [[REGISTERED]].",
  // iron_patriot — Registration Act (PlayerSideScheme)
  'ip002a': "Permanente. Mise en place.\nCette manigance ne compte pas dans la limite de manigances secondaires de joueur.\n<i>Enrôlement</i> — <b>Action</b> : révélez la carte du dessus du deck REGISTERED et mettez-la en jeu engagée avec vous. À la fin du round, vous pouvez dépenser un nombre de ressources égal au nombre d'icônes de [boost] de cette carte pour prendre le contrôle de ce sbire et le traiter comme un allié [[REGISTERED]].\nLes sbires portant le trait [[REGISTERED]] sont traités comme des alliés REGISTERED. Ils subissent 1 dégât consécutif après avoir attaqué ou contré, et leur CTR est égale à leur MNG imprimée.\n<b>Une fois vaincue</b> : retournez cette carte.",
  // iron_patriot — Dark Reign (PlayerSideScheme)
  'ip002b': "Permanente.\nCette manigance ne compte pas dans la limite de manigances secondaires de joueur.\n<i>Accepter le changement</i> — <b>Action</b> : révélez la carte du dessus du deck REGISTERED. Vous pouvez dépenser un nombre de ressources égal au nombre d'icônes de [boost] de cette carte pour prendre le contrôle de ce sbire et le traiter comme un allié [[REGISTERED]]. Sinon, il entre en jeu comme un sbire engagé avec vous.\nLes sbires portant le trait [[REGISTERED]] sont traités comme des alliés REGISTERED. Ils subissent 1 dégât consécutif après avoir attaqué ou contré, et leur CTR est égale à leur MNG imprimée.",
  // iron_patriot — Absolute Power (PlayerSideScheme)
  'ip003': "Victoire 0.\nLes menaces ne peuvent pas être retirées de cette manigance par des héros ou des alliés.\nTant qu'elle est dans la pile de victoire, chaque personnage [[REGISTERED]] gagne +1 ATQ.\n<b>Action de héros</b> : inclinez un personnage [[REGISTERED]] que vous contrôlez → retirez 1 menace d'ici. N'importe quel joueur peut déclencher cette capacité.",
  // iron_patriot — Corrupt Absolutely (PlayerSideScheme)
  'ip004': "Victoire 0.\nLes menaces ne peuvent pas être retirées de cette manigance par des héros ou des alliés.\nTant qu'elle est dans la pile de victoire, chaque personnage [[REGISTERED]] gagne +1 CTR.\n<b>Action d'alter ego</b> : inclinez un personnage [[REGISTERED]] que vous contrôlez → retirez 1 menace d'ici. N'importe quel joueur peut déclencher cette capacité.",
  // iron_patriot — Sentry (Ally)
  'ip005': "Ténacité. Vulnérable.\n<b>Interruption</b> : quand un ennemi vous attaque, vous pouvez déclarer Sentry défenseur sans l'incliner.\n<i>Courroux du Vide</i> — <b>Spécial</b> : jusqu'à la fin du round, gagnez riposte X, où X est égal à l'ATQ de Sentry.",
  // iron_patriot — Victoria Hand (Support)
  'ip006': "<b>Action</b> : inclinez cette carte → choisissez :\n• Regardez la carte du dessus du deck REGISTERED. Vous pouvez la défausser.\n• Mélangez le sbire le plus haut de la pile de défausse de rencontre dans le deck REGISTERED.",
  // iron_patriot — H.A.M.M.E.R. Helicarrier (Support)
  'ip007': "Augmentez de 1 votre limite d'alliés. <i>(Cela vous permet de contrôler plus de 3 alliés.)</i>\n<b>Action</b> : inclinez cette carte et dépensez 1 ressource de n'importe quel type → redressez un allié [[REGISTERED]].",
  // iron_patriot — Director of Security (Upgrade)
  'ip008': "Réduisez de 1 le nombre d'icônes de [boost] de la première carte révélée du deck REGISTERED à chaque round.\n<b>Ressource d'alter ego</b> : inclinez cette carte → générez une ressource [wild].",
  // iron_patriot — Total Authority (Upgrade)
  'ip009': "Vous gagnez Solide.\n<b>Action de héros</b> : après qu'Iron Patriot utilise un pouvoir de base → résolvez la capacité « Spécial » d'1 allié [[REGISTERED]] que vous contrôlez.",
  // iron_patriot — Deceptive Guard (Event)
  'ip010': "<b>Interruption d'alter ego</b> : quand un ennemi manigance → cette activation retire des menaces au lieu d'en placer.\n<b>Interruption de héros</b> <i>(défense)</i> : quand un ennemi vous attaque → empêchez tous les dégâts de cette attaque.",
  // iron_patriot — Foreboding Influence (Event)
  'ip011': "<b>Action d'alter ego</b> : mélangez 2 cartes de la pile de défausse REGISTERED dans le deck REGISTERED.\n<b>Réponse de héros</b> : après avoir attaqué un sbire, dépensez un nombre de ressources égal au nombre d'icônes de [boost] de cette carte pour prendre le contrôle de ce sbire et le traiter comme un allié [[REGISTERED]].",
  // iron_patriot — Repulsor Bombard (Event)
  'ip012': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi et défaussez la carte du dessus du deck REGISTERED. Pour chaque icône de [boost] défaussée de cette façon, infligez 1 dégât à un ennemi.",
  // iron_patriot — Call to Arms (Event)
  'ip013': "<b>Action d'alter ego</b> : choisissez autant d'alliés [[REGISTERED]] en jeu que vous le voulez. Redressez chacun de ces personnages ; ils subissent +1 dégât consécutif après avoir contré ou attaqué pendant ce round.",
  // iron_patriot — Seige (Event)
  'ip014': "<b>Action de héros</b> <i>(attaque)</i> : inclinez Iron Patriot et défaussez autant d'alliés [[REGISTERED]] en jeu que vous le voulez. Infligez X dégâts à un ennemi (15 max), où X est l'ATQ cumulée de ces personnages défaussés. Cette attaque gagne Déferlement.",
  // iron_patriot — Exposed Insanity (Obligation)
  'ip015': "<b><i>À donner au joueur de Norman Osborn.</i></b>\nVous pouvez passer en forme alter ego. Choisissez :\n• Inclinez Norman Osborn → retirez Exposed Insanity de la partie.\n• Défaussez chaque allié portant le trait [[REGISTERED]] que vous contrôlez. Si aucun allié n'a été défaussé de cette façon, trouvez la manigance secondaire Reign's End et révélez-la.",
  // iron_patriot — Doctor Doom (Minion, Nemesis)
  'ip016': "Robuste. Ténacité. Ignoble.\n<b>Une fois révélée</b> : si Cabal Obligations est en jeu, distribuez 1 carte rencontre à chaque joueur. Sinon, trouvez Cabal Obligations et révélez-la. <i>(Mélangez.)</i>\n<i>Rivalité du Cabal</i> — <b>Spécial</b> : mélangez Doctor Doom dans le deck de rencontre → jouez une carte Iron Patriot de votre deck ou de votre pile de défausse en ignorant son coût en ressources. <i>(Mélangez.)</i>",
  // iron_patriot — Reign's End (SideScheme, Nemesis)
  'ip017': "<b>Interruption forcée</b> : quand un personnage entre en jeu, placez 2 menaces ici.\n<b>Réponse forcée</b> : après qu'un allié [[REGISTERED]] est vaincu, placez cet allié face cachée sous cette manigance. S'il y a 3[per_hero] cartes sous cette manigance, les joueurs perdent la partie.",
  // iron_patriot — Cabal Obligations (Attachment, Nemesis)
  'ip018': "Attachez-la à votre identité.\nL'identité attachée ne peut pas se redresser. Les alliés [[REGISTERED]] que vous contrôlez ne peuvent ni attaquer, ni contrer, ni résoudre de capacité « Spécial ».\n<b>Action</b> : dépensez X ressources de n'importe quel type, où X vaut 1 de plus que le nombre d'alliés [[REGISTERED]] en jeu → défaussez cette carte.",
  // iron_patriot — Assembled Resistance (Treachery, Nemesis)
  'ip019': "<b>Une fois révélée (alter ego)</b> : révélez la carte du dessus du deck REGISTERED et mettez-la en jeu engagée avec vous.\n<b>Une fois révélée (héros)</b> : le personnage ami ayant le plus de points de vie restants vous attaque. Si aucune attaque n'a été faite de cette façon, cette carte gagne Renfort.",
  // iron_patriot — H.A.M.M.E.R. Agents (Minion, Registered)
  'ip020': "<b>Une fois révélée</b> : si c'est la première carte révélée du deck REGISTERED ce round, mettez cette carte sous votre contrôle comme allié [[REGISTERED]].\n<i>Renforts</i> — <b>Spécial</b> : cherchez un exemplaire de H.A.M.M.E.R. Agents dans le deck REGISTERED et mettez-le en jeu sous votre contrôle comme allié [[REGISTERED]]. Mélangez le deck REGISTERED.",
  // iron_patriot — H.A.M.M.E.R. Commandos (Minion, Registered)
  'ip021': "Gardien.\n<b>Une fois révélée</b> : si c'est la première carte révélée du deck REGISTERED ce round, mettez cette carte sous votre contrôle comme allié [[REGISTERED]].\n<i>Tir de couverture</i> — <b>Spécial</b> : inclinez cet allié → pour chaque personnage H.A.M.M.E.R. en jeu, infligez 1 dégât à un ennemi.",
  // iron_patriot — H.A.M.M.E.R. Operatives (Minion, Registered)
  'ip022': "Patrouille.\n<b>Une fois révélée</b> : si c'est la première carte révélée du deck REGISTERED ce round, mettez cette carte sous votre contrôle comme allié [[REGISTERED]].\n<i>Contre-espionnage</i> — <b>Spécial</b> : inclinez cet allié → pour chaque personnage H.A.M.M.E.R. en jeu, retirez 1 menace d'une manigance.",
  // iron_patriot — Bullseye (Minion, Registered)
  'ip023': "Attaque rapide.\n[star] Quand Bullseye fait une attaque de base contre un personnage unique <i>([unique])</i>, il gagne +1 ATQ. Les attaques de Bullseye gagnent à distance.\n<i>Ordre d'exécution</i> — <b>Spécial</b> : choisissez un sbire → défaussez la carte du dessus du deck de rencontre. Si cette carte a une icône étoile ([star]) dans la zone de [boost], mettez ce sbire K.O.",
  // iron_patriot — Daken (Minion, Registered)
  'ip024': "Renfort.\n[star] Les attaques de Daken gagnent Perçant.\n<b>Réponse forcée</b> : après le début de la phase du méchant, soignez 1 dégât de Daken.\n<i>Phéromones émotionnelles</i> — <b>Spécial</b> : choisissez de sonner ou de désorienter jusqu'à 2 ennemis.",
  // iron_patriot — Ghost (Minion, Registered)
  'ip025': "Incitation 1. Patrouille.\n[star] Répartissez les menaces de la manigance ou du contre de Ghost entre chaque manigance, aussi équitablement que possible.\n<i>Espionnage intangible</i> — <b>Spécial</b> : retirez 1 menace de chaque manigance pour chaque icône [crisis], [acceleration], [amplify] et [hazard] en jeu.",
  // iron_patriot — Madame Masque (Minion, Registered)
  'ip026': "Gardien. Solide.\n[star] <b>Réponse forcée</b> : après que Madame Masque attaque et blesse un personnage, désorientez ce personnage.\n<i>Faux visages</i> — <b>Spécial</b> : piochez X cartes (3 max), où X est égal au numéro d'étape de la manigance principale. Si la manigance principale n'a pas de numéro d'étape, piochez 1 carte.",
  // iron_patriot — Moonstone (Minion, Registered)
  'ip027': "Robuste. Ténacité.\n[star] <b>Réponse forcée</b> : après que Moonstone attaque et vainc un personnage, donnez-lui une carte d'état Tenace.\n<i>Évaluation psychologique</i> — <b>Spécial</b> : choisissez 1 autre personnage ami que vous contrôlez → soignez 2 dégâts de ce personnage et donnez-lui une carte d'état Tenace.",
  // iron_patriot — Taskmaster (Minion, Registered)
  'ip028': "Gardien.\n[star] Taskmaster gagne +1 MNG et +1 ATQ pour chaque personnage [[REGISTERED]] que vous contrôlez (3 max).\n<i>Formateur d'initiative</i> — <b>Spécial</b> : résolvez la capacité « Spécial » d'1 sbire de la pile de défausse du deck REGISTERED.",
  // iron_patriot — Venom (Minion, Registered)
  'ip029': "Riposte 1. Ténacité.\nTant que les points de vie restants de Venom sont inférieurs à la moitié de ses points de vie de départ, il gagne +1 ATQ et -1 MNG ou -1 CTR.\n<i>Dévoration symbiotique</i> — <b>Spécial</b> : cet allié attaque un personnage. Cet allié subit -1 dégât consécutif s'il vainc un personnage de cette façon.",
  // iron_patriot — Ares (Minion, Registered)
  'ip030': "Ténacité.\n[star] <b>Réponse forcée</b> : les attaques d'Ares gagnent Perçant. Après qu'Ares attaque et blesse un personnage, sonnez ce personnage.\n<i>Tacticien de guerre</i> — <b>Spécial</b> : cherchez un événement [[ATTACK]] ou [[DEFENSE]] dans votre deck et ajoutez-le à votre main. <i>(Mélangez.)</i>",
  // iron_patriot — Loki (Minion, Registered)
  'ip031': "Incitation 2. Robuste.\n<b>Réponse forcée</b> : après que vous résolvez une traîtrise, soignez 1 dégât de Loki.\n<i>Magie du farceur</i> — <b>Spécial</b> : cherchez une traîtrise dans le deck de rencontre et défaussez-la. <i>(Mélangez.)</i>",
  // iron_patriot — Penance (Minion, Registered)
  'ip032': "Riposte 2. Vulnérable.\n[star] Les attaques de Penance gagnent Déferlement.\n<i>Douleur déchaînée</i> — <b>Spécial</b> : inclinez cette carte → choisissez un joueur. Infligez X dégâts au vilain et à chaque sbire engagé avec ce joueur, où X est égal au nombre de dégâts que cet allié a subis.",
  // iron_patriot — The Hood (Minion, Registered)
  'ip033': "Solide. Renfort.\n[star] <b>Interruption forcée</b> : quand The Hood attaque, donnez-lui 1 carte de [boost] pour cette activation.\n<i>Crimes démoniaques</i> — <b>Spécial</b> : défaussez la carte du dessus du deck REGISTERED. Pour chaque icône de [boost] défaussée de cette façon, choisissez soit d'infliger 1 dégât à un ennemi, soit de retirer 1 menace d'une manigance.",
  // iron_patriot — Molecule Man (Minion, Molecule Man)
  'ip034': "Ténacité. Solide.\n[star] Aucun personnage ne peut défendre contre les attaques de Molecule Man.\n<b>Une fois révélée</b> : cherchez Master of Molecules dans le deck de rencontre et la pile de défausse, et révélez-la.",
  // iron_patriot — "You're in My World" (SideScheme, Molecule Man)
  'ip035': "Cette carte ne peut pas quitter le jeu tant que Molecule Man est en jeu.\n<b>Une fois révélée</b> : nommez un type de ressource ([energy], [mental], [physical] ou [wild]). Tant que You're in My World est en jeu, aucun joueur ne peut jouer depuis sa main de carte portant ce type de ressource imprimé.",
  // iron_patriot — Master of Molecules (Attachment, Molecule Man)
  'ip036': "Attachez-la à Molecule Man. Si vous ne pouvez pas, cette carte gagne Renfort.\n[star] <b>Interruption forcée</b> : quand Molecule Man vous attaque, défaussez 1 carte au hasard de votre main. Si la ressource imprimée de cette carte comporte :\n[energy] – cette attaque gagne Déferlement et Perçant.\n[mental] – sonnez et désorientez le personnage attaqué.\n[physical] – cette attaque inflige 2 dégâts supplémentaires.\n[wild] – défaussez 1 carte supplémentaire.",
  // iron_patriot — Manipulate Realities (Treachery, Molecule Man)
  'ip037': "<b>Une fois révélée</b> : si Molecule Man est en jeu, choisissez un type de ressource imprimé ([energy], [mental], [physical] ou [wild]) présent dans votre main. Défaussez de votre main chaque carte portant le type de ressource choisi. Sinon, cette carte gagne Renfort.",
  // iron_patriot — Registered Ally (gabarit)
  'registered_ally': "Ce sbire est traité comme un allié [[REGISTERED]]. Il subit 1 dégât consécutif après avoir attaqué ou contré, et sa CTR est égale à sa MNG imprimée.",
  // spider_woman_kajislav — * Spider-Woman (Hero)
  'sw001a': "<i>Psionic Webbing</i> — <b>Interruption</b> : quand une carte de boost d'un ennemi qui vous attaque est retournée face visible, pour chaque icône de boost ([boost]) sur cette carte, vous pouvez retirer 1 compteur de toile psionique d'ici pour annuler cette icône de boost ([boost]) et infliger 1 dégât à cet ennemi.",
  // spider_woman_kajislav — * Julia Carpenter (AlterEgo)
  'sw001b': "<b>Mise en place</b> : placez 5 compteurs de toile psionique sur votre identité.\n<i>Proper Relaxation</i> — <b>Action</b> : inclinez Julia Carpenter → placez 3 compteurs de toile psionique sur elle <i>(jusqu'à un maximum de 10)</i>.",
  // spider_woman_kajislav — * Madame Web (Ally)
  'sw002': "Madame Web gagne +1 CTR tant qu'il y a au moins 4 compteurs de toile psionique sur votre identité.\n<b>Une fois vaincue</b> : cherchez dans votre deck une carte Spider-Woman et ajoutez-la à votre main. <i>(Mélangez.)</i>",
  // spider_woman_kajislav — * Rachel Carpenter (Support)
  'sw003': "<b>Action d'alter ego</b> : inclinez Rachel Carpenter → redressez Julia Carpenter.",
  // spider_woman_kajislav — Madame Web's Powers (Upgrade)
  'sw004': "Vous gagnez le trait [[PSIONIC]].\n<b>Ressource de héros</b> : inclinez Madame Web's Powers et placez 1 compteur de toile psionique sur Spider-Woman <i>(jusqu'à un maximum de 10)</i> → générez une ressource [mental].",
  // spider_woman_kajislav — Swing and Kick (Event)
  'sw005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Placez 1 compteur de toile psionique sur Spider-Woman pour chaque ressource [mental] utilisée pour payer cette carte <i>(jusqu'à un maximum de 10)</i>.",
  // spider_woman_kajislav — Psi-Web Trap (Event)
  'sw006': "<b>Action de héros</b> <i>(contre)</i> : retirez X compteurs de toile psionique de Spider-Woman → retirez X menaces d'une manigance.",
  // spider_woman_kajislav — Psionic Web Blast (Event)
  'sw007': "<b>Action de héros</b> <i>(attaque)</i> : retirez X compteurs de toile psionique de Spider-Woman → infligez X dégâts à un ennemi.",
  // spider_woman_kajislav — Swinging Rescue (Event)
  'sw008': "<b>Action de héros</b> : choisissez un allié dans la pile de défausse de n'importe quel joueur → ajoutez cet allié à la main de son propriétaire et piochez 2 cartes. Placez 2 compteurs de toile psionique sur Spider-Woman pour chaque ressource [mental] utilisée pour payer cette carte <i>(jusqu'à un maximum de 10)</i>.",
  // spider_woman_kajislav — Web Formation (Event)
  'sw009': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces de chaque manigance. Placez 1 compteur de toile psionique sur Spider-Woman pour chaque ressource [mental] utilisée pour payer cette carte <i>(jusqu'à un maximum de 10)</i>.",
  // spider_woman_kajislav — Hold 'Em Tight (Event)
  'sw010': "<b>Action de héros</b> <i>(attaque)</i> : infligez X dégâts à un ennemi. Si cet ennemi a été blessé ainsi, sonnez-le. Placez 2 compteurs de toile psionique sur Spider-Woman pour chaque ressource [mental] utilisée pour payer cette carte <i>(jusqu'à un maximum de 10)</i>.",
  // spider_woman_kajislav — * Arachnne Costume (Upgrade)
  'sw011': "<b>Action de héros</b> : inclinez cette carte, retirez jusqu'à 2 compteurs de toile psionique de Spider-Woman et choisissez un pouvoir de base → Spider-Woman gagne +1 à ce pouvoir pour chaque compteur de toile psionique retiré ainsi, jusqu'à la fin du round.",
  // spider_woman_kajislav — * Century (Ally, Protection)
  'sw012': "<b>Interruption de héros</b> : quand Century devrait subir d'une attaque moins de dégâts qu'il ne lui reste de points de vie, empêchez tous ces dégâts.",
  // spider_woman_kajislav — * Shroud (Ally, Protection)
  'sw013': "<b>Interruption</b> : quand vous révélez une carte Rencontre, inclinez Shroud et infligez-lui 2 dégâts → annulez les effets de cette carte et défaussez-la.",
  // spider_woman_kajislav — * U.S. Agent (Ally, Protection)
  'sw014': "<b>Interruption de héros</b> : quand un ennemi lance une attaque contre vous, infligez 1 dégât à U.S. Agent → infligez 2 dégâts à l'ennemi attaquant.",
  // spider_woman_kajislav — Blinded Sight (Event, Protection)
  'sw015': "<b>Interruption de héros</b> : quand un ennemi lance une attaque, cet ennemi gagne -2 ATQ pour cette attaque. Si cette attaque n'inflige aucun dégât, désorientez l'ennemi attaquant.",
  // spider_woman_kajislav — Misdiiirection (Upgrade, Protection)
  'sw016': "1 max par joueur.\n<b>Réponse de héros</b> : après vous être défendu contre l'attaque d'un ennemi sans subir de dégât, défaussez cette carte → infligez à un autre ennemi des dégâts égaux à l'ATQ de l'ennemi attaquant.",
  // spider_woman_kajislav — Tactical Retreat (Event, Protection)
  'sw017': "<b>Interruption de héros</b> : quand vous devriez subir des dégâts d'une attaque, quel qu'en soit le nombre, inclinez votre héros → empêchez tous ces dégâts. Passez sous forme d'alter ego.",
  // spider_woman_kajislav — * Battleworld (Support, Basic)
  'sw018': "<b>Action de héros</b> : dépensez une ressource [energy] et défaussez des cartes du deck Rencontre jusqu'à ce qu'un sbire soit défaussé. Mettez ce sbire en jeu engagé avec vous → défaussez des cartes du dessus de votre deck jusqu'à ce qu'un allié soit défaussé. Mettez cet allié en jeu sous votre contrôle.",
  // spider_woman_kajislav — Past and Future (Event, Basic)
  'sw019': "En Équipe (Cassandra Webb et Julia Carpenter). 1 max par deck.\n<b>Action d'alter ego</b> : piochez jusqu'à votre taille de main imprimée. Placez 2 compteurs de toile psionique sur Julia Carpenter.",
  // spider_woman_kajislav — Separation from the Child (Obligation)
  'sw020': "<b><i>Donnez-la au joueur Julia Carpenter.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Julia Carpenter → retirez Separation from the Child de la partie.\n• Retirez tous les compteurs de toile psionique de votre identité. Si moins de 5 compteurs ont été retirés ainsi, cette carte gagne Renfort. Défaussez cette obligation.",
  // spider_woman_kajislav — * Man-Bull (Minion, Nemesis A)
  'sw021': "<b>Une fois révélée</b> : chaque joueur défausse 1 carte spécifique à une identité de sa main.\n<i>(Sbire némésis de Spider-Woman.)</i>",
  // spider_woman_kajislav — Vault Breakout (SideScheme, Nemesis A)
  'sw022': "<b>Une fois révélée</b> : chaque joueur cherche un sbire dans le deck Rencontre et le met en jeu engagé avec lui. Mélangez le deck Rencontre.",
  // spider_woman_kajislav — Bad Inspiration (Treachery, Nemesis A)
  'sw023': "<b>Une fois révélée</b> : cherchez un allié dans votre pile de défausse et mettez-le en jeu engagé avec vous. Traitez cet allié comme un sbire à la zone de texte vierge. La MNG du sbire est égale à sa CTR imprimée et il ne subit pas de dégâts consécutifs. Si aucun allié n'est entré en jeu ainsi, cette carte gagne Renfort.",
  // spider_woman_kajislav — Violent Disturbance (Treachery, Nemesis A)
  'sw024': "<b>Une fois révélée</b> : défaussez toutes les cartes spécifiques à une identité de votre main.",
  // spider_woman_kajislav — * Ms. Marvel (Minion, Nemesis B)
  'sw025': "Riposte 1. Ténacité.\n<b>Réponse forcée</b> : après que Ms. Marvel manigance, placez 2 menaces sur Superhuman Registration Act.\n<i>(Sbire némésis de Spider-Woman.)</i>",
  // spider_woman_kajislav — Superhuman Registration Act (SideScheme, Nemesis B)
  'sw026': "Permanent.\nTant qu'il y a au moins 1 menace ici, cette manigance gagne une icône [hazard].",
  // spider_woman_kajislav — Fugitive (Obligation, Nemesis B)
  'sw027': "<b>Réponse forcée</b> : après le début de la phase des joueurs, placez 1 menace sur Superhuman Registration Act.\n<b>Action d'alter ego</b> : s'il n'y a aucune menace sur Superhuman Registration Act, dépensez une ressource [mental] → défaussez Fugitive.",
  // spider_woman_kajislav — Fighting a Friend (Treachery, Nemesis B)
  'sw028': "<b>Une fois révélée (alter ego)</b> : placez 3 menaces sur Superhuman Registration Act.\n<b>Une fois révélée (héros)</b> : infligez à un personnage allié des dégâts égaux à votre ATQ.",

  // Pack fan-made « zeus » (Mozilla, set 171). ⚠ [lightning] est l'ÉCLAIR,
  // la ressource maison du pack, distincte de [energy] (11/09/2026).
  // Hellcat (jakxin, set 172), 11/09/2026. hc001a : la parenthese « evenements
  // seulement » est le tooltip demande par l'utilisateur.
  'hc001a': "<b>Réponse</b> : après avoir joué une carte portant une ressource [mental] imprimée, attachez cette carte à Hellcat (maximum 3). (Limite de deux fois par round.) <i>(Événements seulement : c'est ce que la notice de l'auteur décrit, et un allié attaché quitterait la table.)</i>\n<i>Renforcée</i> — <b>Ressource</b> : défaussez 1 carte attachée à Hellcat → générez une ressource [mental].",
  'hc001b': "<i>Potentiel mental</i> — <b>Interruption</b> : quand le méchant manigance contre vous, piochez 1 carte → si cette carte porte une ressource [mental] imprimée, réduisez de 1 la menace placée.",
  'hc002': "<b>Réponse</b> : après qu'Iron Man a utilisé un pouvoir de base, dépensez une ressource [mental] et choisissez 1 (limite d'une fois par round) :\n• Redressez votre identité.\n• Piochez 2 cartes.",
  'hc003': "Vous gagnez +3 points de vie.\n<b>Interruption de héros</b> : quand vous faites un contre de base, inclinez Cat Suit et dépensez une ressource [mental] → vous gagnez +2 CTR et ignorez le mot-clé patrouille pour ce contre.",
  'hc004': "Hellcat gagne +1 ATQ.\n<b>Interruption de héros</b> : quand vous faites une attaque de base, inclinez Hellcat's Claws et dépensez une ressource [mental] → vous gagnez +2 ATQ et perçant pour cette attaque.",
  'hc005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Si vous avez payé cette carte uniquement avec des ressources [mental], infligez 2 dégâts supplémentaires à cet ennemi, et cette attaque gagne déferlement.",
  'hc006': "<b>Action de héros</b> <i>(contre)</i> : retirez 4 menaces d'une manigance. Si vous avez payé cette carte uniquement avec des ressources [mental], retirez 2 menaces supplémentaires de cette manigance, et cette carte ignore l'icône de crise ([crisis]) et le mot-clé patrouille.",
  'hc007': "<b>Interruption de héros</b> <i>(défense)</i> : quand Hellcat défend contre une attaque → vous gagnez +2 DEF pour cette défense. Cherchez dans votre pile de défausse une carte qui ne s'appelle pas Cat-Like Reflexes et porte une ressource [mental] imprimée, et ajoutez-la à votre main.",
  'hc008': "<b>Action</b> : choisissez une option :\n• Soignez 1 dégât à un personnage allié pour chaque carte attachée à votre identité.\n• Retirez 1 menace d'une manigance pour chaque carte attachée à votre identité.",
  'hc009': "<b>Interruption de héros</b> : quand vous payez un événement ATTAQUE ou CONTRE uniquement avec des ressources [mental], cet événement inflige 1 dégât supplémentaire ou retire 1 menace supplémentaire.",
  'hc010': "Hellcat gagne scélérat.\n<b>Interruption</b> : quand une carte boost donnée à Hellcat est retournée face visible, annulez sa capacité « <b>Boost</b> ». Puis soignez 1 dégât à Hellcat.\n<b>Réponse forcée</b> : après avoir changé de forme, défaussez cette carte.",
  'hc011': "<b>Action d'alter ego</b> : inclinez Hedy Wolfe → cherchez dans votre pile de défausse une carte portant une ressource [mental] imprimée et attachez-la à votre identité.",
  'hc012': "Miss Hulk gagne +1 point de vie pour chaque ressource [mental] dépensée pour la payer.\n<b>Réponse</b> : après que Miss Hulk a attaqué et vaincu un sbire, cherchez dans votre pile de défausse un événement portant une ressource [mental] imprimée et ajoutez-le à votre main.",
  'hc013': "<b><i>Donnez cette carte au joueur de Patsy Walker.</i></b>\nPassez en forme alter ego et défaussez toutes les cartes attachées à votre identité. Infligez 1 dégât à votre identité pour chaque carte ainsi défaussée. Si au moins 2 cartes ont été défaussées de votre identité de cette façon, retirez cette carte de la partie. Sinon, défaussez-la.",
  'hc014': "Blackheart gagne +X MNC et Daimon Hellstrom gagne +X ATQ, X étant le nombre de cartes attachées à Hellcat.\n<b>Interruption forcée</b> : quand Blackheart ou Daimon Hellstrom s'active, il s'active aussi contre le joueur avec lequel l'autre est engagé.",
  'hc015': "Ténacité. Scélérat.\nBlackheart ne peut pas se trouver dans la même zone de jeu que Daimon Hellstrom.\n<b>Révélation</b> : si Daimon Hellstrom est dans votre zone de jeu, Blackheart s'engage avec le joueur suivant dans l'ordre du tour. S'il ne le peut pas, cette carte gagne déferlante.\n<i>(Sbire némésis de Hellcat.)</i>",
  'hc016': "Robuste. Scélérat.\nDaimon Hellstrom ne peut pas se trouver dans la même zone de jeu que Blackheart.\n<b>Révélation</b> : si Blackheart est dans votre zone de jeu, Daimon Hellstrom s'engage avec le joueur suivant dans l'ordre du tour. S'il ne le peut pas, cette carte gagne déferlante.\n<i>(Sbire némésis de Hellcat.)</i>",
  'hc017': "<b>Révélation</b> : défaussez une amélioration que vous contrôlez. Subissez autant de dégâts que le coût en ressources de cette carte.",
  'hc018': "Firestar entre en jeu avec 1 pion feu pour chaque ressource [mental] dépensée pour la payer.\n<b>Interruption</b> : quand Firestar attaque, retirez 1 pion feu d'elle → infligez 2 dégâts à un ennemi.",
  'hc019': "<b>Interruption</b> : quand Captain Marvel utilise un pouvoir de base, dépensez 1 ressource de n'importe quel type → cherchez dans votre pile de défausse une carte portant la ressource imprimée correspondante et mélangez-la dans votre deck.",
  'hc020': "En Équipe (Hellcat et Miss Hulk). 1 max par deck.\n<b>Action de héros</b> : redressez Hellcat et Miss Hulk. Elles gagnent +2 ATQ jusqu'à la fin de la phase.",
  'hc021': "En Équipe (Hellcat et Iron Man). 1 max par deck.\n<b>Action de héros</b> : redressez Hellcat et Iron Man. Cherchez une amélioration dans votre deck et votre pile de défausse et ajoutez-la à votre main.",
  'hc022': "En Équipe (2 parmi Black Cat, Firestar, Hellcat et Monica Rambeau). 1 max par deck.\n<b>Action de héros</b> : cherchez dans votre pile de défausse 3 cartes portant chacune une ressource imprimée différente. Ajoutez-en 1 à votre main et mélangez les autres dans votre deck.",
  'hc023': "<b>Réponse</b> <i>(contre)</i> : après que votre héros a attaqué et vaincu un ennemi, retirez 2 menaces d'une manigance.",
  'hc024': "1 max par deck.",
  'hc025': "1 max par deck.",
  'hc026': "1 max par deck.",
  'ze001a': "<i>Tempête du Père du Ciel</i> — <b>Réponse</b> : après avoir dépensé à la fois une ressource [energy] et une ressource [lightning] pour payer un événement, résolvez la capacité « <b>Spécial</b> » de cet événement et retirez 1 menace d'une manigance.",
  'ze001b': "<i>Dieu de la Foudre</i> — <b>Action</b> : cherchez l'amélioration Thunderbolt dans votre deck et votre pile de défausse et ajoutez-la à votre main. (Limite d'une fois par round.)",
  'ze002': "<b>Réponse</b> : après l'entrée en jeu de Hera, choisissez une carte de votre main portant une capacité « <b>Spécial</b> » imprimée, puis résolvez cette capacité.",
  'ze003': "Requis ([energy]).\n<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Cette attaque gagne perçant.\n<b>Spécial</b> : sonnez un ennemi.",
  'ze004': "<b>Action de héros</b> <i>(contre)</i> : retirez 4 menaces d'une manigance.\n<b>Spécial</b> : désorientez un ennemi.",
  'ze005': "Requis ([energy][energy]).\n<b>Action de héros</b> <i>(attaque)</i> : infligez 7 dégâts à un ennemi. Si cette attaque vainc cet ennemi, redressez Zeus.\n<b>Spécial</b> : gagnez une carte d'état Tenace.",
  'ze006': "Requis ([energy][energy][energy]).\n<b>Action de héros</b> <i>(attaque)</i> : infligez 10 dégâts à un ennemi. Cette attaque gagne déferlement.\n<b>Spécial</b> : infligez 2 dégâts à chaque ennemi en jeu. Retirez 2 menaces de chaque manigance.",
  'ze007': "<b>Réponse</b> : après avoir résolu votre capacité « <i>Tempête du Père du Ciel</i> », placez 1 compteur d'égide ici.\n<b>Interruption de héros</b> <i>(défense)</i> : quand vous alliez subir n'importe quelle quantité de dégâts, retirez 2 compteurs d'égide d'ici → empêchez 3 de ces dégâts.",
  'ze008': "<b>Ressource de héros</b> : inclinez Thunderbolt → générez une ressource [energy].\n<b>Réponse de héros</b> : après avoir résolu votre capacité « <i>Tempête du Père du Ciel</i> », redressez Thunderbolt.",
  'ze009': "Chaque événement que vous possédez qui n'a pas de capacité « <b>Spécial</b> » imprimée gagne : « <b>Spécial</b> : infligez 2 dégâts à un ennemi. »\n<b>Réponse</b> : après avoir résolu votre capacité « <i>Tempête du Père du Ciel</i> », gagnez +1 taille de main jusqu'à la fin de la phase.",
  'ze010': "<b>Action d'alter ego</b> : inclinez Hephaestus → mélangez 1 exemplaire de Thunder Strike de votre pile de défausse dans votre deck. Piochez 1 carte.",
  'ze011': "<b>Ressource</b> : inclinez Mount Olympus et dépensez une ressource [energy] → générez une ressource [lightning].",
  'ze012': "<b><i>Donnez-la au joueur Zeus Panhellenios.</i></b>\nZeus ne peut pas résoudre sa capacité « <i>Tempête du Père du Ciel</i> ».\n<b>Action d'alter ego</b> : inclinez votre identité et dépensez une ressource [lightning] → retirez Alcohol Problems de la partie.",
  'ze013': "Solide. Vilain.\n[star] <b>Interruption forcée</b> : quand Nyx s'active contre vous, défaussez la carte du dessus de votre deck. Si cette carte porte une icône [energy] imprimée, donnez 1 carte de boost supplémentaire à Nyx.\n<i>(Sbire némésis de Zeus.)</i>",
  'ze014': "<b>Une fois révélée</b> : chaque joueur cherche dans son deck et sa pile de défausse 2 cartes portant une icône [energy] imprimée et les place face cachée sous cette carte. Placez 1 menace supplémentaire ici pour chaque carte placée face cachée de cette façon.\n<b>Une fois déjouée</b> : renvoyez chaque carte face cachée d'ici dans la pile de défausse de son propriétaire.",
  'ze015': "Attachez-la à votre identité.\nVous ne pouvez pas dépenser de ressources [energy] pour payer des cartes.\n<b>Action d'alter ego</b> : dépensez 2 ressources de n'importe quel type → défaussez cette carte.",
  'ze016': "<b>Une fois révélée</b> : défaussez les 3 cartes du dessus de votre deck. Subissez 1 dégât indirect pour chaque événement défaussé de cette façon. Si un événement portant une capacité « <b>Spécial</b> » imprimée est défaussé de cette façon, vous êtes sonné.\n<hr />\n[star] <b>Boost</b> : donnez une carte de boost supplémentaire à l'ennemi qui s'active.",
  // ------------------------------------------------------------------ sentinel
  // Pack `sentinel` (T-Wrecks, 12/09/2026). Deux mots-cles MAISON, traduits ici
  // pour la premiere fois : **Detruisez** (2 degats imblocables puis
  // retournement de la piece, fiche docs/reference/mots-cles/destroy.md) et
  // **Expose** (quatrieme carte d'etat du moteur, fiche exposed.md). Les traits
  // du pack restent en anglais comme partout ailleurs : le joueur a la carte
  // anglaise sous les yeux.
  // sentinel — Sentinel (Hero)
  'st001a': "<i>Protocole ablatif</i> — <b>Interruption</b> : quand vous devriez subir n'importe quelle quantité de dégâts, détruisez plutôt une amélioration [[COMPONENT]]. <i>(Voir l'encart.)</i>",
  // sentinel — Sentinel (AlterEgo)
  'st001b': "<b>Action</b> : cherchez Juston Seyfert dans votre deck et votre pile de défausse et ajoutez-le à votre main. <i>(Limite d'une fois par phase.)</i>\n<b>Action</b> : défaussez 1 carte de votre main → retournez chaque amélioration [[COMPONENT]] (face [[DESTROYED]]) sur sa face [[INTACT]].\n<b>Mise en place</b> : mettez chaque amélioration [[COMPONENT]] en jeu (face [[INTACT]] visible).",
  // sentinel — Head (Intact) (Upgrade permanente, mise en place)
  'st002a': "Permanente.\n<b>Action de héros</b> : inclinez Head (Intact) → exposez 2 ennemis.",
  // sentinel — Head (Destroyed) (Upgrade permanente)
  'st002b': "Permanente.\nVos événements [[THWART]] coûtent 1 ressource de plus.",
  // sentinel — Arms (Intact) (Upgrade permanente, mise en place)
  'st003a': "Permanente.\n<b>Action de héros</b> <i>(attaque)</i> : inclinez Arms (Intact) → infligez 1 dégât à un ennemi.",
  // sentinel — Arms (Destroyed) (Upgrade permanente)
  'st003b': "Permanente.\nVos événements [[ATTACK]] coûtent 1 ressource de plus.",
  // sentinel — Torso (Intact) (Upgrade permanente, mise en place)
  'st004a': "Permanente.\n<b>Action de héros</b> : inclinez Torso (Intact) → soignez 1 dégât de Sentinel.",
  // sentinel — Torso (Destroyed) (Upgrade permanente)
  'st004b': "Permanente.\nVos améliorations coûtent 1 ressource de plus.",
  // sentinel — Legs (Intact) (Upgrade permanente, mise en place)
  'st005a': "Permanente.\n<b>Action de héros</b> : inclinez Legs (Intact) → réduisez de 1 le coût de la prochaine carte que vous jouez.",
  // sentinel — Legs (Destroyed) (Upgrade permanente)
  'st005b': "Permanente.\nVous avez -1 à votre taille de main.",
  // sentinel — Exterminate (Event, x2)
  'st006': "[star] En coût additionnel pour jouer cet événement, inclinez ou détruisez Arms (Intact) ET une autre amélioration [[COMPONENT]] (face [[INTACT]] visible).\n<b>Action de héros</b> <i>(attaque)</i> : infligez 7 dégâts à un ennemi. Cette attaque gagne À distance, Perçant et Déferlement. Exposez 2 ennemis.",
  // sentinel — Hardwire Access (Event, x3)
  'st007': "[star] En coût additionnel pour jouer cet événement, inclinez Head (Intact) ou détruisez-la.\n<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces réparties entre les manigances en jeu, plus X, X étant le nombre de cartes d'état Exposé en jeu.",
  // sentinel — Rocket Punch (Event, x3)
  'st008': "[star] En coût additionnel pour jouer cet événement, inclinez Arms (Intact) ou détruisez-la.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Cette attaque gagne Déferlement.",
  // sentinel — Threat Suppression (Event, x2)
  'st009': "[star] En coût additionnel pour jouer cet événement, inclinez Legs (Intact) ou détruisez-la.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 1 dégât à un maximum de 3 ennemis différents et sonnez un maximum de 2 de ces ennemis.",
  // sentinel — Juston Seyfert (Support unique)
  'st010': "<b>Action</b> : attachez-le à une manigance annexe.\n<b>Action de héros</b> : inclinez Juston Seyfert → retirez 1 menace de la manigance annexe attachée.\n<b>Réponse forcée</b> : après que la manigance annexe attachée est déjouée, mettez Juston Seyfert en jeu sous votre contrôle. Redressez Sentinel ou jusqu'à 2 améliorations [[COMPONENT]].",
  // sentinel — Propulsion Array (Upgrade)
  'st011': "[star] En coût additionnel pour jouer cette amélioration, inclinez Legs (Intact).\n<b>Action de héros</b> : remélangez cette carte dans votre deck. Choisissez :\n• inclinez 1 amélioration [[COMPONENT]] (face [[INTACT]] visible) → redressez Sentinel ;\n• inclinez Sentinel → redressez jusqu'à 2 améliorations [[COMPONENT]] (face [[INTACT]] visible).",
  // sentinel — Reinforced Plating (Upgrade, x2)
  'st012': "[star] En coût additionnel pour jouer cette amélioration, inclinez Torso (Intact).\n<b>Action de héros</b> : défaussez Reinforced Plating → retournez 1 amélioration [[COMPONENT]] (face [[DESTROYED]] visible) sur sa face [[INTACT]]. Gagnez une carte d'état Tenace.",
  // sentinel — Targeting Protocol (Upgrade)
  'st013': "<b>Action de héros</b> : inclinez cette carte → exposez 2 ennemis, ou retirez d'une manigance autant de menaces qu'il y a de cartes d'état Exposé en jeu <i>(maximum 3)</i>.",
  // sentinel — Prime Directive (Obligation)
  'st014': "<b><i>Donnez-la au joueur Sentinel.</i></b>\n<b>Action forcée</b> : choisissez :\n• infligez 3 dégâts à un AUTRE personnage allié ([[MUTANT]] si possible) → défaussez cette carte ;\n• placez 3 menaces sur la manigance principale → défaussez cette carte.",
  // sentinel — Mark VII-A (Minion némésis)
  'st015': "[star] <b>Réponse forcée</b> : après que Mark VII-A vous a porté une attaque non défendue, retournez une amélioration [[COMPONENT]] (face [[INTACT]] visible) sur sa face [[DESTROYED]]. Si vous ne pouvez pas, défaussez 1 amélioration que vous contrôlez.\n<i>(Sbire némésis de Sentinel.)</i>",
  // sentinel — Rogue Asset (SideScheme némésis)
  'st016': "Les améliorations [[COMPONENT]] (face [[INTACT]] visible) et les améliorations [[TECH]] gagnent le trait [[HACKED]].",
  // sentinel — Disabled (Treachery némésis)
  'st017': "<b>Une fois révélée</b> : inclinez chaque amélioration [[HACKED]] que vous contrôlez. Si vous ne pouvez pas, cherchez la manigance annexe Rogue Asset dans le deck rencontre et sa pile de défausse et mettez-la en jeu. Si Rogue Asset est déjà en jeu, votre identité est sonnée.\n<hr />\n[star] <b>Boost</b> : votre identité est sonnée.",
  // sentinel — Viral Assault (Treachery némésis)
  'st018': "<b>Une fois révélée</b> : vous pouvez défausser 1 amélioration [[HACKED]] que vous contrôlez. Sinon, subissez 1 dégât par amélioration [[HACKED]] que vous contrôlez. Si vous ne contrôlez aucune amélioration [[HACKED]], cherchez la manigance annexe Rogue Asset dans le deck rencontre et sa pile de défausse et mettez-la en jeu. Si Rogue Asset est déjà en jeu, cette carte gagne Déferlement.",
  // sentinel — Hostile Override (Treachery némésis)
  'st019': "<b>Une fois révélée</b> : si vous contrôlez au moins une amélioration [[HACKED]], infligez à un personnage allié des dégâts égaux à votre valeur d'ATQ, ou placez sur la manigance principale des menaces égales à votre valeur de CTR. Si vous ne contrôlez aucune amélioration [[HACKED]], vous êtes désorienté.\n<hr />\n[star] <b>Boost</b> : vous êtes désorienté.",
  // sentinel — Size Advantage (Event, Agressivité, hors set du héros)
  'st020': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi <i>(6 dégâts à la place si vous avez le trait [[GIANT]] ou s'il vous reste plus de points de vie qu'à cet ennemi)</i>.",
  // sentinel — Reboot (Event, Basic, hors set du héros)
  'st021': "<b>Action</b> : redressez un personnage allié [[ANDROID]] et soignez-lui 1 dégât.",
  // ---------------------------------------------------------------------- muse
  // SET MODULAIRE `muse` (Rainy, 13/09/2026), 6 cartes. Quatre d'entre elles
  // parlent d'« une carte avec l'image de votre identite dessus » : ce sont les
  // CARTES SIGNATURE (decision utilisateur, voir le relevé du pack). La
  // traduction garde la formule imprimee et ajoute la precision entre
  // parentheses, comme le ferait une FAQ.
  // muse — Art Imitates Death (SideScheme)
  'mu001': "<b>Une fois révélée</b> : défaussez les 3 cartes du dessus du deck de chaque joueur. Pour chaque carte défaussée ainsi, infligez 1 dégât à chaque personnage dont l'image était sur cette carte <i>(les cartes signature : le héros dont c'est le deck)</i>.",
  // muse — Supply Run (SideScheme)
  'mu002': "<b>Interruption forcée</b> : quand un ennemi unique ([star]) s'active, défaussez la carte du dessus du deck rencontre. Si elle porte une image de cet ennemi <i>(une carte de son set)</i>, donnez-la lui en carte de boost face cachée.",
  // muse — Muse (Minion unique)
  'mu003': "Ténacité.\n<b>Interruption forcée</b> : quand un joueur joue une carte qui porte l'image de son identité <i>(une carte signature)</i>, Muse s'active contre ce joueur.",
  // muse — Graffitied Streets (Environment)
  'mu004': "Réserve (3[per_hero] compteurs graffiti).\n<b>Interruption forcée</b> : quand vous jouez une carte qui porte l'image de votre identité <i>(une carte signature)</i>, placez 1 menace sur la manigance principale.\n<b>Action</b> : inclinez un personnage que vous contrôlez → retirez d'ici autant de compteurs graffiti que son CTR. <i>(Limite d'une fois par round par joueur.)</i>",
  // muse — Grim Inspiration (Treachery)
  'mu005': "Déferlement.\n<b>Une fois révélée</b> : chaque joueur choisit une carte signature de sa pile de défausse et la place sur le dessus de son deck. Donnez à Muse et au vilain une carte de boost face cachée.",
  // muse — Obsession (Treachery, x2)
  'mu006': "<b>Une fois révélée</b> : Muse s'active contre vous. S'il n'est pas en jeu, cherchez Muse et mettez-le en jeu engagé avec vous.\n<hr />\n[star] <b>Boost</b> : cette carte gagne +X icônes de boost ([boost]), X étant le nombre de cartes de votre main qui portent l'image de votre identité <i>(les cartes signature)</i>.",
  // ---------------------------------------------------------------------- red_sonja
  // Pack red_sonja (RyCoRan, 22/09/2026), 20 cartes.
  // red_sonja — * Red Sonja (Hero)
  'rs001a': "<i>She-Devil</i> — <b>Action</b> : inclinez une amélioration [[WEAPON]] que vous contrôlez → jouez un événement de votre main en réduisant son coût en ressources de 1.",
  // red_sonja — * Sonja of Hyrkania (AlterEgo)
  'rs001b': "Lors de la construction du deck, vous pouvez inclure jusqu'à 6 événements d'aspects autres que votre aspect choisi.\n<i>Day of the Sword</i> — <b>Action</b> : cherchez dans votre deck l'amélioration Hyrkanium Blade et ajoutez-la à votre main.",
  // red_sonja — * Conan (Ally)
  'rs002': "<b>Interruption</b> : quand vous employez l'un des pouvoirs de base de Conan, inclinez une amélioration [[WEAPON]] que vous contrôlez → Conan gagne +X à ce pouvoir pour cette utilisation, X étant le coût imprimé de cette carte.",
  // red_sonja — Savage Steel (Event) x2
  'rs003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 6 dégâts à un ennemi. Pour chaque point de dégât excédentaire infligé par cette attaque, réduisez de 1 le coût du prochain événement que vous jouez durant cette phase.",
  // red_sonja — Scarlet Huntress (Event) x2
  'rs004': "<b>Action de héros</b> <i>(contre)</i> : retirez 6 menace d'une manigance. Pour chaque point de menace excédentaire retiré par ce contre, réduisez de 1 le coût du prochain événement que vous jouez durant cette phase.",
  // red_sonja — Devil's Defiance (Event) x2
  'rs005': "<b>Interruption de héros</b> <i>(défense)</i> : quand un ennemi attaque, prévenez tous les dégâts de cette attaque. Après cette attaque, donnez à Red Sonja une carte d'état Tenace.",
  // red_sonja — Hyrkanian Fury (Event)
  'rs006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Si vous avez utilisé votre capacité « She-Devil » pour réduire le coût de cette carte, sonnez cet ennemi.",
  // red_sonja — Red Reckoning (Event)
  'rs007': "<b>Action de héros</b> <i>(contre)</i> : retirez 4 menace d'une manigance. Si vous avez utilisé votre capacité « She-Devil » pour réduire le coût de cette carte, rendez un ennemi confus.",
  // red_sonja — Savage She-Devil (Event)
  'rs008': "<b>Action de héros</b> <i>(attaque/contre)</i> : infligez 5 dégâts à un ennemi. Retirez 5 menace d'une manigance. Si vous avez utilisé votre capacité « She-Devil » pour réduire le coût de cette carte, cette action ignore les mots-clés Garde et Patrouille ainsi que toute icône de Crise en jeu.",
  // red_sonja — * Queen of Sogaria (PlayerSideScheme)
  'rs009': "Victoire 0.\nSeule Red Sonja peut retirer de la menace de cette manigance. Elle peut utiliser son ATQ, sa DEF ou son CTR de base pour cela.\nTant que Queen of Sogaria est dans la vitrine de victoire, Red Sonja gagne : « <b>Réponse</b> : après avoir incliné Hyrkanium Blade, piochez 1 carte. <i>(Limite d'une fois par round.)</i> »",
  // red_sonja — She Devil with a Sword (Resource)
  'rs010': "<b>Réponse de héros</b> : après avoir dépensé cette carte, redressez une amélioration [[WEAPON]] que vous contrôlez.",
  // red_sonja — Crimson Shadow (Upgrade)
  'rs011': "Red Sonja gagne +1 CTR.\nUtilise (2 compteurs de discrétion).\n<b>Réponse de héros</b> : après la mise en jeu d'un sbire, retirez 1 compteur de discrétion d'ici → annulez l'effet « Une fois révélée » de ce sbire.",
  // red_sonja — * Bloodmoon Battleaxe (Upgrade)
  'rs012': "Restreinte.\n<b>Réponse</b> : après avoir joué un événement, inclinez Bloodmoon Battleaxe → infligez 2 dégâts à un ennemi.",
  // red_sonja — * Hyrkanium Blade (Upgrade)
  'rs013': "Les attaques de base de Red Sonja gagnent Perçant.\n<b>Réponse</b> : après avoir vaincu une manigance secondaire ou un sbire, redressez Hyrkanium Blade. <i>(Limite d'une fois par round.)</i>",
  // red_sonja — A Warrior's Burden (Obligation)
  'rs014': "Donnez-la au joueur de Sonja of Hyrkania. Choisissez :\n• Inclinez votre identité et défaussez Hyrkanium Blade → retirez A Warrior's Burden de la partie.\n• Cherchez dans le deck rencontre et sa pile de défausse 2 sbires et révélez-les → défaussez cette carte.",
  // red_sonja_nemesis — Queen of the Frozen Wastes (SideScheme, 1/5)
  'rs015': "Les joueurs ne peuvent pas redresser d'amélioration [[WEAPON]].",
  // red_sonja_nemesis — * Ice Queen (Minion, 2/5)
  'rs016': "<b>Une fois vaincu</b> : le joueur qui l'a vaincu défausse des cartes du dessus du deck rencontre et révèle le premier sbire défaussé ainsi.\n<i>(Sbire némésis de Red Sonja.)</i>\n[star] <b>Boost</b> : mettez ce sbire en jeu engagé avec vous.",
  // red_sonja_nemesis — Yeti Warrior (Minion, 3/5)
  'rs017': "Garde. Ténacité.\n[star] Les attaques de Yeti Warrior gagnent Déferlement.",
  // red_sonja_nemesis — She-Devil Shackled! (Attachment, 4/5)
  'rs018': "Utilise (3 compteurs d'entrave).\n<b>Une fois révélée</b> : attachez-la à votre identité et inclinez chaque amélioration [[WEAPON]] que vous contrôlez.\n<b>Interruption forcée</b> : quand une amélioration [[WEAPON]] que vous contrôlez devrait se redresser, dépensez 1 ressource d'un type quelconque. Si vous le faites, retirez 1 compteur d'entrave d'ici <i>(et redressez cette amélioration)</i>. Sinon, cette amélioration ne se redresse pas.",
  // red_sonja_nemesis — Frozen Fury (Treachery, 5/5)
  'rs019': "<b>Une fois révélée</b> : pour chaque amélioration que vous contrôlez (jusqu'à un maximum de 3), choisissez :\n• Subissez 1 dégât indirect.\n• Placez 1 menace sur la manigance principale.",
  // ---------------------------------------------------------------------- conan
  // Pack conan (RyCoRan, 25/09/2026), 22 cartes (identite a cinq faces).
  // conan — * Conan the Thief (Hero)
  'cn001a': "<i>Rogue's Intuition</i> — <b>Réponse</b> : après avoir retiré 4 menaces ou plus d'une manigance au cours d'une phase, placez 1 compteur Crom sur The Cimmerian.",
  // conan — * Conan (AlterEgo)
  'cn001b': "<i>Savage Vitality</i> — <b>Mise en place</b> : mettez King Conan de côté. Mettez l'amélioration The Cimmerian en jeu, face [[TITLE]] visible.\n<b>Action</b> : dépensez 1 ressource de n'importe quel type → placez 1 compteur Crom sur The Cimmerian. <i>(Limite d'une fois par round.)</i>",
  // conan — * Conan the Barbarian (Hero)
  'cn001c': "<i>Born of Battle</i> — <b>Réponse</b> : après avoir infligé 5 dégâts ou plus à un ennemi au cours d'une phase, placez 1 compteur Crom sur The Cimmerian.",
  // conan — * King Conan (Hero)
  'cn001d': "<i>Crown of Aquilonia</i> — <b>Réponse</b> : après avoir utilisé un pouvoir de base, placez 2 compteurs Crom sur The Cimmerian.",
  // conan — * Conan (AlterEgo, côté roi)
  'cn001e': "<i>Battle-Forged</i> — <b>Réponse</b> : après être passé sous cette forme, choisissez :\n• Donnez une carte d'état Tenace à King Conan.\n• Retirez tous les compteurs Crom de The Cimmerian → soignez 1 dégât de King Conan par compteur Crom retiré ainsi.",
  // conan — * Bêlit (Ally)
  'cn002': "Tant que vous avez le trait [[THIEF]] ou [[KING]], Bêlit gagne +1 CTR.\nTant que vous avez le trait [[BARBARIAN]] ou [[KING]], Bêlit gagne +1 ATQ.\n<b>Réponse</b> : après que Bêlit est entrée en jeu, si vous avez le trait [[KING]], redressez votre identité.",
  // conan — Crush Your Enemies (Event) x2
  'cn003': "[star] Réduction 1 ([[KING]]).\n<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi (4 dégâts à la place si vous êtes King Conan).",
  // conan — Reaper's Cleave (Event) x2
  'cn004': "[star] Réduction 1 ([[KING]]).\n<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance (3 menaces à la place si vous êtes King Conan).",
  // conan — Destroyer's Defiance (Event) x2
  'cn005': "[star] Réduction 1 ([[KING]]).\n<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts, prévenez tous ces dégâts. Placez 1 compteur Crom sur The Cimmerian (2 compteurs à la place si vous êtes King Conan).",
  // conan — Hyborian Havoc (Event) x2
  'cn006': "<b>Action de héros</b> <i>(attaque/contre)</i> : infligez 5 dégâts à un ennemi ou retirez 4 menaces d'une manigance. Si vous êtes :\n• Conan the Thief, désorientez un ennemi.\n• Conan the Barbarian, sonnez un ennemi.\n• King Conan, tout ce qui précède.",
  // conan — Cimmerian Counter (Event) x2
  'cn007': "[star] Réduction 1 ([[KING]]).\n<b>Réponse de héros</b> <i>(attaque/contre)</i> : après vous être défendu contre une attaque ennemie, infligez à un ennemi des dégâts égaux à votre ATQ ou retirez d'une manigance une menace égale à votre CTR. <i>(Imprimé « Action de héros » ; jouée en Réponse, arbitrage du 25/09/2026. Jouer une carte (défense) pendant l'attaque compte comme se défendre.)</i>",
  // conan — Savage Sword (Event)
  'cn008': "[star] Réduction 1 ([[KING]]).\n<b>Action de héros</b> <i>(attaque/contre)</i> : inclinez votre héros → infligez à un ennemi des dégâts, ou retirez d'une manigance une menace, égaux au total des valeurs de CTR, ATQ et DEF de votre héros.",
  // conan — * The Scarlet Citadel (PlayerSideScheme)
  'cn009': "Victoire 0.\nTant que The Scarlet Citadel est dans la pile de victoire, si vous avez le trait :\n• [[THIEF]], vous gagnez +1 CTR et ignorez le mot-clé patrouille.\n• [[BARBARIAN]], vous gagnez +1 ATQ et ignorez le mot-clé garde.\n• [[KING]], tout ce qui précède.",
  // conan — Savage Tales (Resource)
  'cn010': "<b>Réponse de héros</b> : après avoir dépensé cette carte, placez 1 compteur Crom sur The Cimmerian (2 à la place si vous êtes King Conan).",
  // conan — * Atlantean Sword (Upgrade)
  'cn011': "Restreint.\n<b>Réponse de héros</b> <i>(attaque/contre)</i> : après avoir joué un événement, inclinez Atlantean Sword → infligez à un ennemi des dégâts, ou retirez d'une manigance une menace, égaux au coût imprimé de cet événement.",
  // conan — * The Cimmerian (Upgrade, face TITLE)
  'cn012a': "Permanent.\n<b>Réponse</b> : dès qu'il y a au moins 8 compteurs Crom ici, redressez votre identité et échangez-la avec King Conan. Retirez vos autres identités de la partie. Retournez cette carte.",
  // conan — * The Cimmerian (Upgrade, face KING)
  'cn012b': "Permanent.\n<b>Interruption de héros</b> : quand vous utilisez l'un des pouvoirs de base de King Conan, retirez X compteurs Crom d'ici et inclinez The Cimmerian → King Conan gagne +X à ce pouvoir pour cette utilisation.",
  // conan — The Coils of Doom (Obligation)
  'cn013': "<b><i>Donnez-la au joueur Conan.</i></b>\nUtilisations (3 compteurs serpent). Victoire 0.\n<b>Action de héros</b> : dépensez 1 ressource de n'importe quel type ou retirez 1 compteur Crom de The Cimmerian → retirez 1 compteur serpent d'ici.",
  // conan — Frozen Ambush (SideScheme)
  'cn014': "<b>Réponse forcée</b> : après qu'une identité a changé de forme, placez 2 menaces ici.",
  // conan — * Hrothgar (Minion)
  'cn015': "Ténacité.\n<b>Réponse</b> : après avoir effectué une attaque de base contre Hrothgar, infligez 1 dégât à Hymdul.\n<i>(Sbire némésis de Conan.)</i>\n<hr />\n[star] <b>Boost</b> : vous êtes sonné.",
  // conan — * Hymdul (Minion)
  'cn016': "Ténacité.\n<b>Réponse</b> : après avoir effectué une attaque de base contre Hymdul, infligez 1 dégât à Hrothgar.\n<i>(Sbire némésis de Conan.)</i>\n<hr />\n[star] <b>Boost</b> : vous êtes désorienté.",
  // conan — Grapple on the Glacier (Treachery) x2
  'cn017': "<b>Une fois révélée</b> : cherchez dans le deck Rencontre et sa pile de défausse un sbire [[GIANT]] et mettez-le en jeu, engagé avec vous. Sinon, subissez 4 dégâts.",
  // ---------------------------------------------------------------------- wave
  // Pack wave (Pearl Pangan, 22/09/2026), 19 cartes. Mecanique propre au
  // pack : la « zone Rising Tide », une zone de cartes face visible/cachee a
  // cote du deck (nom propre du mecanisme, laisse en anglais comme les
  // traits [[...]] -- voir la convention en tete de fichier).
  // wave — * Wave (Hero)
  // ⚠ « Storm Surge » (nom de l'ability sur la carte) traduit, contrairement
  // a la convention habituelle qui garde les noms propres en anglais : il
  // contient le mot reserve « Surge » (mot-cle Renfort), que le test de
  // vocabulaire (textes-fr-fanmade.test.ts) interdit partout, y compris dans
  // un nom propre.
  '65001a': "<i>Vague de tempête</i> — <b>Réponse</b> : après avoir défaussé des cartes de votre main pour payer un coût, placez 1 de ces cartes dans votre zone Rising Tide.",
  // wave — * Pearl Pangan (AlterEgo)
  '65001b': "Mise en place : vous commencez la partie avec une zone Rising Tide (voir l'encart).\n<i>Champion Swimmer</i> — <b>Action</b> : placez la carte du dessus de votre deck face visible dans votre zone Rising Tide. <i>(Limite d'une fois par phase.)</i>",
  // wave — * Sea Hunter (Ally)
  '65002': "<b>Réponse</b> : après que Sea Hunter attaque ou contre, retournez face cachée une carte face visible de votre zone Rising Tide et payez le coût imprimé d'un événement de votre pile de défausse → jouez cet événement comme s'il était dans votre main.",
  // wave — Crashing Wave (Event) x3
  '65003': "<b>Action de héros</b> <i>(attaque)</i> : infligez 1 dégât à un ennemi. Retournez jusqu'à 3 cartes face visible de votre zone Rising Tide face cachée → infligez 2 dégâts supplémentaires pour chaque carte ainsi retournée face cachée.",
  // wave — Marine Patrol (Event) x2
  '65004': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menace d'une manigance. Retournez jusqu'à 2 cartes de votre zone Rising Tide face cachée. Pour chaque carte ainsi retournée, choisissez (max. 1 chacun) :\n• retirez 2 menace d'une manigance.\n• piochez 1 carte.",
  // wave — Instinctive Flow (Event) x2
  '65005': "<b>Action de héros</b> : retournez jusqu'à 3 cartes face visible de votre zone Rising Tide face cachée. Pour chaque carte ainsi retournée face cachée, choisissez (max. 1 chacun) :\n• infligez 2 dégâts à un ennemi.\n• retirez 2 menace d'une manigance.\n• sonnez un ennemi.",
  // wave — Ocean's Fury (Event) x2
  '65006': "Max. 1 fois par round.\n<b>Action de héros</b> : jusqu'à la fin du round, après que Wave vainc un ennemi ou retire la dernière menace d'une manigance, piochez 1 carte et retournez une carte face cachée de votre zone Rising Tide face visible.",
  // wave — Tide Wall (Event) x2
  '65007': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts, prévenez jusqu'à 3 de ces dégâts. Pour chaque point de dégât ainsi prévenu, placez la carte du dessus de votre deck face visible dans votre zone Rising Tide.",
  // wave — * Pearl's Lolo (Support)
  '65008': "<b>Action d'alter ego</b> : retournez une carte face visible de votre zone Rising Tide face cachée → soignez 3 dégâts.",
  // wave — * Wave's Swords (Upgrade)
  '65009': "Restreinte.\n<b>Action de héros</b> : inclinez Wave's Swords et retournez une carte face visible de votre zone Rising Tide face cachée → redressez Wave.",
  // wave — * Wave's Crown (Upgrade)
  '65010': "Wave gagne +1 CTR.\nVous pouvez jouer les cartes rangées sous cette carte comme si elles étaient dans votre main.\n<b>Action</b> : inclinez Wave's Crown → rangez 1 carte face visible de votre zone Rising Tide sous cette carte (max. 2).",
  // wave_nemesis — Alontech's Greatest Achievement (SideScheme, 1/5)
  '65011': "Augmentez de 1 le coût du premier événement joué par chaque joueur à chacun de ses tours.",
  // wave_nemesis — * The Reyna Sirena (Minion, 2/5)
  '65012': "En coût additionnel pour que le joueur engagé joue un événement, ce joueur doit subir 1 dégât.\n<i>(Sbire némésis de Wave.)</i>\n[star] <b>Boost</b> : vous êtes sonné.",
  // wave_nemesis — Alontech Hybrid (Minion, 3/5)
  '65013': "Les sbires et vilains SIRENA ne peuvent pas être attaqués par le joueur avec lequel Alontech Hybrid est engagé.",
  // wave_nemesis — Alontech Seawolf (Attachment, 4/5)
  '65014': "Attachez-la à la manigance principale.\n<b>Interruption forcée</b> : quand la phase joueur commence, infligez 1 dégât à chaque joueur.\n<b>Action de héros</b> : placez 1 menace sur la manigance principale et défaussez une carte spécifique à votre identité de votre main → défaussez cette carte.",
  // wave_nemesis — Triumph Probation (Obligation, 5/5)
  '65015': "Donnez-la au joueur de Pearl Pangan. Cherchez dans votre main, votre deck, votre pile de défausse et votre zone de jeu Wave's Swords et Wave's Crown et placez-les face cachée sous cette carte. Wave perd le trait TRIUMPH DIVISION.\n<b>Action d'alter ego</b> : inclinez Pearl Pangan → ajoutez Wave's Swords et Wave's Crown à votre main et retirez Triumph Probation de la partie.",
  // wave — Energy / Genius / Strength (Resource) : meme texte que hc024 etc.
  '65017': "1 max par deck.",
  '65018': "1 max par deck.",
  '65019': "1 max par deck.",
  // hunting_season — Vermin (Villain)
  'hs001': "[star] <b>Réponse forcée</b> : après que Vermin s'est activé contre vous, défaussez la carte du dessus du deck Rencontre. Si un sbire [[RAT]] a été défaussé de cette façon, mettez-le en jeu engagé avec vous.",
  // hunting_season — Vermin (Villain)
  'hs002': "[star] <b>Réponse forcée</b> : après que Vermin s'est activé contre vous, défaussez les 2 cartes du dessus du deck Rencontre. Mettez en jeu engagé avec vous le premier sbire [[RAT]] défaussé de cette façon.",
  // hunting_season — Vermin (Villain)
  'hs003': "[star] <b>Réponse forcée</b> : après que Vermin s'est activé contre vous, défaussez les 2 cartes du dessus du deck Rencontre. Mettez en jeu engagé avec vous chaque sbire [[RAT]] défaussé de cette façon. Résolvez l'effet \"Spécial\" d'Even More Rats.",
  // hunting_season — Rats and More Rats (MainScheme)
  'hs004a': "<b>Contenu</b> : Vermin (I) et Vermin (II). <i>(Vermin (II) et Vermin (III) à la place en mode expert.)</i> Sets de rencontre Vermin et Standard. Un set de rencontre modulaire <i>(recommandé : Feral Instincts)</i>.\n<b>Mise en place</b> : mettez en jeu l'environnement Even More Rats. Mettez en jeu un sbire Regular Rats engagé avec chaque joueur. Mélangez le deck Rencontre. Passez à l'étape 1B.",
  // hunting_season — Rats and More Rats (MainScheme)
  'hs004b': "[star] <b>Réponse forcée</b> : après l'étape 1 de la phase du méchant, placez 1 menace sur chaque sbire [[RAT]]. Résolvez l'effet \"Spécial\" d'Even More Rats.",
  // hunting_season — Rats, Rats and More Rats (MainScheme)
  'hs005a': "<b>Une fois révélée</b> : cherchez Bringer of Plague dans le deck Rencontre et la pile de défausse, et révélez-la. Passez à l'étape 2B.",
  // hunting_season — Rats, Rats and More Rats (MainScheme)
  'hs005b': "[star] <b>Réponse forcée</b> : après l'étape 1 de la phase du méchant, placez 1 menace sur chaque sbire [[RAT]]. Résolvez l'effet \"Spécial\" d'Even More Rats.\n<b>Si cette manigance est complétée, les rats ont envahi la ville et les joueurs perdent la partie.</b>",
  // hunting_season — Even More Rats (Environment)
  'hs006': "La menace sur les sbires [[RAT]] ne peut pas être contrée.\n<b>Spécial</b> : si le total des menaces sur les sbires [[RAT]] et sur la manigance principale est supérieur ou égal à la valeur de menace cible de la manigance principale, l'étape en cours de la manigance principale est complétée.",
  // hunting_season — Regular Rats (Minion)
  'hs007': "Renfort.\nX est égal au nombre de sbires [[RAT]] engagés avec vous (3 au maximum).\n<hr />\n[star] <b>Boost</b> : mettez Regular Rats en jeu engagé avec vous.",
  // hunting_season — Regular Rats (Minion)
  'hs008': "Renfort.\nX est égal au nombre de sbires [[RAT]] engagés avec vous (3 au maximum).\n<hr />\n[star] <b>Boost</b> : mettez Regular Rats en jeu engagé avec vous.",
  // hunting_season — Regular Rats (Minion)
  'hs009': "Renfort.\nX est égal au nombre de sbires [[RAT]] engagés avec vous (3 au maximum).\n<hr />\n[star] <b>Boost</b> : mettez Regular Rats en jeu engagé avec vous.",
  // hunting_season — Regular Rats (Minion)
  'hs010': "Renfort.\nX est égal au nombre de sbires [[RAT]] engagés avec vous (3 au maximum).\n<hr />\n[star] <b>Boost</b> : mettez Regular Rats en jeu engagé avec vous.",
  // hunting_season — Feral Rats (Minion)
  'hs011': "Renfort. Coup Rapide.\nX est égal au nombre de sbires [[RAT]] engagés avec vous (3 au maximum).\n<hr />\n[star] <b>Boost</b> : mettez Feral Rats en jeu engagé avec vous.",
  // hunting_season — Feral Rats (Minion)
  'hs012': "Renfort. Coup Rapide.\nX est égal au nombre de sbires [[RAT]] engagés avec vous (3 au maximum).\n<hr />\n[star] <b>Boost</b> : mettez Feral Rats en jeu engagé avec vous.",
  // hunting_season — Feral Rats (Minion)
  'hs013': "Renfort. Coup Rapide.\nX est égal au nombre de sbires [[RAT]] engagés avec vous (3 au maximum).\n<hr />\n[star] <b>Boost</b> : mettez Feral Rats en jeu engagé avec vous.",
  // hunting_season — Feral Rats (Minion)
  'hs014': "Renfort. Coup Rapide.\nX est égal au nombre de sbires [[RAT]] engagés avec vous (3 au maximum).\n<hr />\n[star] <b>Boost</b> : mettez Feral Rats en jeu engagé avec vous.",
  // hunting_season — Vermin Clone (Minion)
  'hs015': "Garde.\nTant que Vermin Clone est engagé avec vous, les personnages que vous contrôlez ne peuvent pas attaquer Regular Rats et Feral Rats.\n<hr />\n[star] <b>Boost</b> : attribuez une carte de boost supplémentaire à l'ennemi qui attaque pour cette activation.",
  // hunting_season — Vermin Clone (Minion)
  'hs016': "Garde.\nTant que Vermin Clone est engagé avec vous, les personnages que vous contrôlez ne peuvent pas attaquer Regular Rats et Feral Rats.\n<hr />\n[star] <b>Boost</b> : attribuez une carte de boost supplémentaire à l'ennemi qui attaque pour cette activation.",
  // hunting_season — Vermin Clone (Minion)
  'hs017': "Garde.\nTant que Vermin Clone est engagé avec vous, les personnages que vous contrôlez ne peuvent pas attaquer Regular Rats et Feral Rats.\n<hr />\n[star] <b>Boost</b> : attribuez une carte de boost supplémentaire à l'ennemi qui attaque pour cette activation.",
  // hunting_season — Swarmed by Rats (Attachment)
  'hs018': "Attachez-la à votre identité.\nChaque sbire [[RAT]] engagé avec vous gagne garde.\n<b>Interruption</b> : après avoir vaincu un sbire [[RAT]] engagé avec vous, défaussez 2 cartes de votre main → défaussez cette carte.",
  // hunting_season — Swarmed by Rats (Attachment)
  'hs019': "Attachez-la à votre identité.\nChaque sbire [[RAT]] engagé avec vous gagne garde.\n<b>Interruption</b> : après avoir vaincu un sbire [[RAT]] engagé avec vous, défaussez 2 cartes de votre main → défaussez cette carte.",
  // hunting_season — Vermin Cloning (SideScheme)
  'hs020': "<b>Une fois révélée</b> : cherchez un exemplaire de Vermin Clone dans le deck Rencontre et la pile de défausse, et mettez-le en jeu engagé avec le premier joueur.",
  // hunting_season — Bringer of Plague (SideScheme)
  'hs021': "<b>Une fois révélée</b> : placez ici autant de menaces qu'il y en a sur les sbires [[RAT]] en jeu.",
  // hunting_season — A Mischief of Rats (Treachery)
  'hs022': "<b>Une fois révélée</b> : défaussez X cartes du deck Rencontre, X étant égal au double du niveau du méchant. Pour chaque sbire [[RAT]] défaussé de cette façon, choisissez soit de placer 2 menaces sur la manigance principale, soit de mettre ce sbire en jeu engagé avec vous.",
  // hunting_season — A Mischief of Rats (Treachery)
  'hs023': "<b>Une fois révélée</b> : défaussez X cartes du deck Rencontre, X étant égal au double du niveau du méchant. Pour chaque sbire [[RAT]] défaussé de cette façon, choisissez soit de placer 2 menaces sur la manigance principale, soit de mettre ce sbire en jeu engagé avec vous.",
  // hunting_season — Rabid Assault (Treachery)
  'hs024': "<b>Une fois révélée (alter ego)</b> : Vermin manigance. S'il n'y a aucun sbire [[RAT]] engagé avec vous, cette carte gagne renfort.\n<b>Une fois révélée (héros)</b> : Vermin vous attaque. S'il n'y a aucun sbire [[RAT]] engagé avec vous, cette carte gagne renfort.",
  // hunting_season — Rabid Assault (Treachery)
  'hs025': "<b>Une fois révélée (alter ego)</b> : Vermin manigance. S'il n'y a aucun sbire [[RAT]] engagé avec vous, cette carte gagne renfort.\n<b>Une fois révélée (héros)</b> : Vermin vous attaque. S'il n'y a aucun sbire [[RAT]] engagé avec vous, cette carte gagne renfort.",
  // hunting_season — A Thousand Bites (Treachery)
  'hs026': "<b>Une fois révélée</b> : pour chaque sbire [[RAT]] engagé avec vous, choisissez soit de placer 1 menace sur ce sbire, soit de subir 1 dégât indirect. Résolvez l'effet \"Spécial\" d'Even More Rats. S'il y a un sbire [[RAT]] ou moins engagé avec vous, cette carte gagne renfort.",
  // hunting_season — A Thousand Bites (Treachery)
  'hs027': "<b>Une fois révélée</b> : pour chaque sbire [[RAT]] engagé avec vous, choisissez soit de placer 1 menace sur ce sbire, soit de subir 1 dégât indirect. Résolvez l'effet \"Spécial\" d'Even More Rats. S'il y a un sbire [[RAT]] ou moins engagé avec vous, cette carte gagne renfort.",
  // hunting_season — A Thousand Bites (Treachery)
  'hs028': "<b>Une fois révélée</b> : pour chaque sbire [[RAT]] engagé avec vous, choisissez soit de placer 1 menace sur ce sbire, soit de subir 1 dégât indirect. Résolvez l'effet \"Spécial\" d'Even More Rats. S'il y a un sbire [[RAT]] ou moins engagé avec vous, cette carte gagne renfort.",
  // hunting_season — A Thousand Bites (Treachery)
  'hs029': "<b>Une fois révélée</b> : pour chaque sbire [[RAT]] engagé avec vous, choisissez soit de placer 1 menace sur ce sbire, soit de subir 1 dégât indirect. Résolvez l'effet \"Spécial\" d'Even More Rats. S'il y a un sbire [[RAT]] ou moins engagé avec vous, cette carte gagne renfort.",
  // hunting_season — Scorpion (Villain)
  'hs030': "[star] <b>Interruption forcée</b> : quand la phase du méchant se termine, si Scorpion's Tail n'est pas attachée à Scorpion, mettez-la en jeu et attachez-la à Scorpion.",
  // hunting_season — Scorpion (Villain)
  'hs031': "Scorpion ne peut pas être sonné.\n[star] <b>Interruption forcée</b> : quand la phase du méchant se termine, si Scorpion's Tail n'est pas attachée à Scorpion, mettez-la en jeu et attachez-la à Scorpion.",
  // hunting_season — Scorpion (Villain)
  'hs032': "Scorpion ne peut pas être sonné.\n<b>Une fois révélé</b> : cherchez Tail Laser dans le deck Rencontre et la pile de défausse, et révélez-la.\n[star] <b>Interruption forcée</b> : quand la phase du méchant se termine, si Scorpion's Tail n'est pas attachée à Scorpion, mettez-la en jeu et attachez-la à Scorpion.",
  // hunting_season — Thirst for Revenge (MainScheme)
  'hs033a': "<b>Contenu</b> : Scorpion (I) et Scorpion (II). <i>(Scorpion (II) et Scorpion (III) à la place en mode expert.)</i> Sets de rencontre Scorpion et Standard. Un set de rencontre modulaire <i>(recommandé : Feral Instincts)</i>.\n<b>Mise en place</b> : mettez en jeu le soutien J. Jonah Jameson sous le contrôle du premier joueur. Mettez en jeu l'amélioration Scorpion's Tail et attachez-la à Scorpion. Passez à l'étape 1B.",
  // hunting_season — Thirst for Revenge (MainScheme)
  'hs033b': "<b>Une fois accomplie</b> : placez 1 compteur de blessure sur le soutien J. Jonah Jameson.",
  // hunting_season — Vengeful Pursuit (MainScheme)
  'hs034a': "<b>Une fois révélée</b> : passez à l'étape 2B.",
  // hunting_season — Vengeful Pursuit (MainScheme)
  'hs034b': "<b>Interruption forcée</b> : quand cette manigance devrait être complétée, placez plutôt 1 compteur de blessure sur le soutien J. Jonah Jameson. Ensuite, retirez toutes les menaces de cette manigance ainsi que toutes les améliorations et pièces jointes qui y sont attachées.",
  // hunting_season — J. Jonah Jameson (Support)
  'hs035': "Permanent.\n<b>Interruption</b> : quand un personnage allié devrait subir n'importe quelle quantité de dégâts, placez 1 compteur de blessure ici → prévenez tous ces dégâts.\n<b>Interruption forcée</b> : quand il y a 3 + 1[per_hero] compteurs de blessure ou plus ici, les joueurs perdent la partie.",
  // hunting_season — Scorpion’s Tail (Attachment)
  'hs036': "[star] <b>Réponse forcée</b> : après que Scorpion a attaqué et infligé des dégâts à un personnage, ce personnage est sonné. S'il est déjà sonné, infligez-lui 1 dégât.\n<b>Interruption</b> : quand Scorpion devrait subir n'importe quelle quantité de dégâts, ces dégâts peuvent être placés ici à la place. Ensuite, s'il y a 10[per_hero] dégâts ou plus ici, mettez Scorpion's Tail de côté, hors jeu. Ensuite, Scorpion subit 8[per_hero] dégâts.",
  // hunting_season — Tail Armor (Attachment)
  'hs037': "Déplacez 5 dégâts de Scorpion's Tail vers Scorpion. Attachez-la à Scorpion's Tail. Si vous ne pouvez pas, cette carte gagne renfort.\n<b>Interruption forcée</b> : quand des dégâts devraient être placés sur Scorpion's Tail, placez-les ici à la place. S'il y a 8 dégâts ou plus ici, défaussez Tail Armor.",
  // hunting_season — Honed Stinger (Attachment)
  'hs038': "Déplacez 5 dégâts de Scorpion's Tail vers Scorpion. Attachez-la à Scorpion's Tail. Si vous ne pouvez pas, cette carte gagne renfort.\n<b>Interruption forcée</b> : quand Scorpion attaque, il gagne +1 ATQ pour cette attaque, et l'attaque gagne perçant.\n<hr />\n[star] <b>Boost</b> : mélangez cette carte dans le deck Rencontre.",
  // hunting_season — Tail Laser (Attachment)
  'hs039': "Déplacez 5 dégâts de Scorpion's Tail vers Scorpion. Attachez-la à Scorpion's Tail. Si vous ne pouvez pas, cette carte gagne renfort.\n<b>Interruption forcée</b> : quand Scorpion attaque, l'attaque gagne à distance et déferlement.\n<hr />\n[star] <b>Boost</b> : mélangez cette carte dans le deck Rencontre.",
  // hunting_season — Coiled Up (Attachment)
  'hs040': "Déplacez 5 dégâts de Scorpion's Tail vers Scorpion. Si Scorpion's Tail est attachée à Scorpion, attachez Coiled Up à votre identité. Si vous ne pouvez pas, cette carte gagne renfort.\n<b>Interruption forcée</b> : quand Scorpion's Tail est mise de côté, défaussez Coiled Up.",
  // hunting_season — Coiled Up (Attachment)
  'hs041': "Déplacez 5 dégâts de Scorpion's Tail vers Scorpion. Si Scorpion's Tail est attachée à Scorpion, attachez Coiled Up à votre identité. Si vous ne pouvez pas, cette carte gagne renfort.\n<b>Interruption forcée</b> : quand Scorpion's Tail est mise de côté, défaussez Coiled Up.",
  // hunting_season — Human Fly (Minion)
  'hs042': "<b>Interruption forcée</b> : quand Human Fly devrait subir n'importe quelle quantité de dégâts d'une attaque, prévenez tous ces dégâts. <i>(Limite d'une fois par round.)</i>\n<hr />\n[star] <b>Boost</b> : une fois cette activation terminée, attribuez-vous cette carte comme carte Rencontre face cachée.",
  // hunting_season — Human Fly (Minion)
  'hs043': "<b>Interruption forcée</b> : quand Human Fly devrait subir n'importe quelle quantité de dégâts d'une attaque, prévenez tous ces dégâts. <i>(Limite d'une fois par round.)</i>\n<hr />\n[star] <b>Boost</b> : une fois cette activation terminée, attribuez-vous cette carte comme carte Rencontre face cachée.",
  // hunting_season — Grizzly (Minion)
  'hs044': "[star] <b>Interruption forcée</b> : quand Grizzly attaque, l'attaque gagne perçant.\n<hr />\n[star] <b>Boost</b> : cette attaque gagne perçant.",
  // hunting_season — Hippo (Minion)
  'hs045': "Ténacité.\n<hr />\n[star] <b>Boost</b> : cette attaque gagne déferlement.",
  // hunting_season — Luring Out Prey (SideScheme)
  'hs046': "<b>Une fois révélée</b> : placez 1[per_hero] menace supplémentaire ici.",
  // hunting_season — A Mess of Things (SideScheme)
  'hs047': "<b>Une fois révélée</b> : placez ici 2 menaces supplémentaires pour chaque personnage allié sonné.",
  // hunting_season — Tail Enhancements (Treachery)
  'hs048': "<b>Une fois révélée</b> : défaussez des cartes du deck Rencontre jusqu'à défausser une pièce jointe [[TAIL]]. Révélez cette carte.\n<hr />\n[star] <b>Boost</b> : cette carte gagne +1 icône de boost ([boost]) pour chaque pièce jointe [[TAIL]] attachée à Scorpion.",
  // hunting_season — Tail Enhancements (Treachery)
  'hs049': "<b>Une fois révélée</b> : défaussez des cartes du deck Rencontre jusqu'à défausser une pièce jointe [[TAIL]]. Révélez cette carte.\n<hr />\n[star] <b>Boost</b> : cette carte gagne +1 icône de boost ([boost]) pour chaque pièce jointe [[TAIL]] attachée à Scorpion.",
  // hunting_season — Stinger Stab (Treachery)
  'hs050': "<b>Une fois révélée (alter ego)</b> : Scorpion manigance. Si vous êtes sonné, Scorpion gagne +2 MNG pour cette activation.\n<b>Une fois révélée (héros)</b> : Scorpion vous attaque. Après cette activation, si vous êtes sonné, vous êtes désorienté.",
  // hunting_season — Stinger Stab (Treachery)
  'hs051': "<b>Une fois révélée (alter ego)</b> : Scorpion manigance. Si vous êtes sonné, Scorpion gagne +2 MNG pour cette activation.\n<b>Une fois révélée (héros)</b> : Scorpion vous attaque. Après cette activation, si vous êtes sonné, vous êtes désorienté.",
  // hunting_season — Restraining Pincers (Treachery)
  'hs052': "<b>Une fois révélée</b> : choisissez soit de dépenser [physical][physical], soit de sonner votre identité. Si vous ne pouvez pas, cette carte gagne renfort.\n<hr />\n[star] <b>Boost</b> : si cette activation vous inflige des dégâts, inclinez votre héros.",
  // hunting_season — Restraining Pincers (Treachery)
  'hs053': "<b>Une fois révélée</b> : choisissez soit de dépenser [physical][physical], soit de sonner votre identité. Si vous ne pouvez pas, cette carte gagne renfort.\n<hr />\n[star] <b>Boost</b> : si cette activation vous inflige des dégâts, inclinez votre héros.",
  // hunting_season — Curtis Connors (Villain)
  'hs054a': "Curtis Connors ne peut pas subir de dégâts.\n[star] <b>Interruption forcée</b> : quand Curtis Connors devrait attaquer, placez plutôt 1 compteur de honte sur l'environnement Reptilian Rage. S'il y a 3 compteurs de honte dessus, Curtis Connors manigance.\n[star] <b>Réponse forcée</b> : après que Curtis Connors a manigancé, retournez Curtis Connors.",
  // hunting_season — Curtis Connors (Villain)
  'hs055a': "Curtis Connors ne peut pas subir de dégâts.\n[star] <b>Interruption forcée</b> : quand Curtis Connors devrait attaquer, placez plutôt 1 compteur de honte sur l'environnement Reptilian Rage. S'il y a 3 compteurs de honte dessus, Curtis Connors manigance.\n[star] <b>Réponse forcée</b> : après que Curtis Connors a manigancé, retournez Curtis Connors.",
  // hunting_season — The Lizard (Villain)
  'hs054b': "[star] <b>Réponse forcée</b> : après que The Lizard a manigancé, retournez The Lizard.\n<b>Interruption forcée</b> : quand la phase du méchant se termine, défaussez 1[per_hero] cartes du dessus du deck Rencontre. Révélez chaque pièce jointe [[REPTILE]] défaussée de cette façon.",
  // hunting_season — The Lizard (Villain)
  'hs055b': "[star] <b>Réponse forcée</b> : après que The Lizard a manigancé, retournez The Lizard.\n<b>Interruption forcée</b> : quand la phase du méchant se termine, défaussez 1[per_hero] cartes du dessus du deck Rencontre. Chaque joueur, dans l'ordre des joueurs, doit révéler la pièce jointe [[REPTILE]] la plus haute de la pile de défausse Rencontre.",
  // hunting_season — Curtis Connors (Villain)
  'hs056a': "Curtis Connors ne peut pas subir de dégâts.\n[star] <b>Interruption forcée</b> : quand Curtis Connors devrait attaquer, placez plutôt 2 compteurs de honte sur l'environnement Reptilian Rage. S'il y a 3 compteurs de honte dessus, Curtis Connors manigance.\n[star] <b>Réponse forcée</b> : après que Curtis Connors a manigancé, retournez Curtis Connors.",
  // hunting_season — The Lizard (Villain)
  'hs056b': "[star] <b>Réponse forcée</b> : après que The Lizard a manigancé, retournez The Lizard.\n<b>Interruption forcée</b> : quand la phase du méchant se termine, défaussez 2[per_hero] cartes du dessus du deck Rencontre. Chaque joueur, dans l'ordre des joueurs, doit révéler la pièce jointe [[REPTILE]] la plus haute de la pile de défausse Rencontre.",
  // hunting_season — Using the Mammal Brain (MainScheme)
  'hs057a': "<b>Contenu</b> : Curtis Connors (I) et Curtis Connors (II). <i>(Curtis Connors (II) et Curtis Connors (III) à la place en mode expert.)</i> Sets de rencontre The Lizard et Standard. Un set de rencontre modulaire <i>(recommandé : Lizard Thralls)</i>.\n<b>Mise en place</b> : mettez en jeu l'environnement Reptilian Rage. Le méchant commence sur sa face Curtis Connors. Passez à l'étape 1B.",
  // hunting_season — Using the Mammal Brain (MainScheme)
  'hs057b': "<b>Une fois accomplie</b> : placez des compteurs de honte sur l'environnement Reptilian Rage pour qu'il en ait 3. Si The Lizard n'est pas en jeu, retournez Curtis Connors.",
  // hunting_season — Reptile Brain Taking Over (MainScheme)
  'hs058a': "<b>Une fois révélée</b> : cherchez un exemplaire de Reptile Research dans le deck Rencontre et la pile de défausse, et révélez-le. Passez à l'étape 2B.",
  // hunting_season — Reptile Brain Taking Over (MainScheme)
  'hs058b': "X est le nombre de cartes [[REPTILE]] en jeu (The Lizard compris).",
  // hunting_season — No Humanity Left (MainScheme)
  'hs059a': "<b>Une fois révélée</b> : si The Lizard n'est pas en jeu, retournez Curtis Connors. Placez des compteurs de honte sur l'environnement Reptilian Rage pour qu'il en ait 3. Passez à l'étape 3B.",
  // hunting_season — No Humanity Left (MainScheme)
  'hs059b': "The Lizard ne peut pas être retourné.\nLa menace ne peut pas être retirée de cette manigance.\n<b>Si cette étape est complétée, Curtis Connors est mort et les joueurs perdent la partie.</b>",
  // hunting_season — Reptilian Rage (Environment)
  'hs060': "The Lizard gagne +1 ATQ pour chaque compteur de honte sur Reptilian Rage. (3 compteurs de honte au maximum.) Tant qu'il y a au moins 1 compteur de honte ici, les attaques de The Lizard gagnent déferlement.\n<b>Réponse forcée</b> : après que The Lizard a attaqué, retirez des compteurs de honte de Reptilian Rage :\nMéchant niveau I : retirez 2 compteurs de honte.\nMéchant niveau II : retirez 1 compteur de honte.\nMéchant niveau III : retirez 0 compteur de honte.",
  // hunting_season — Enhanced Lizard Senses (Attachment)
  'hs061': "<b>Une fois révélée</b> : Curtis Connors manigance avec +1[per_hero] MNG. Attachez cette carte à The Lizard.\n<b>Interruption</b> : quand un événement est joué, annulez ses effets et défaussez-le. Ensuite, placez Enhanced Lizard Senses sous la pile de défausse Rencontre.",
  // hunting_season — Enhanced Lizard Senses (Attachment)
  'hs062': "<b>Une fois révélée</b> : Curtis Connors manigance avec +1[per_hero] MNG. Attachez cette carte à The Lizard.\n<b>Interruption</b> : quand un événement est joué, annulez ses effets et défaussez-le. Ensuite, placez Enhanced Lizard Senses sous la pile de défausse Rencontre.",
  // hunting_season — Komodo Claws (Attachment)
  'hs063': "<b>Une fois révélée</b> : Curtis Connors manigance avec +1[per_hero] MNG. Attachez cette carte à The Lizard.\nThe Lizard gagne riposte 1.\n<b>Action de héros</b> : dépensez une ressource [energy] et subissez 1 dégât → placez Komodo Claws sous la pile de défausse Rencontre.",
  // hunting_season — Komodo Claws (Attachment)
  'hs064': "<b>Une fois révélée</b> : Curtis Connors manigance avec +1[per_hero] MNG. Attachez cette carte à The Lizard.\nThe Lizard gagne riposte 1.\n<b>Action de héros</b> : dépensez une ressource [energy] et subissez 1 dégât → placez Komodo Claws sous la pile de défausse Rencontre.",
  // hunting_season — Lizard Tail (Attachment)
  'hs065': "<b>Une fois révélée</b> : Curtis Connors manigance avec +1[per_hero] MNG. Attachez cette carte à The Lizard.\n[star] <b>Interruption forcée</b> : quand The Lizard attaque, l'attaque gagne à distance.\n<b>Action de héros</b> : dépensez une ressource [mental] et placez 1 menace sur la manigance principale → placez Lizard Tail sous la pile de défausse Rencontre.",
  // hunting_season — Alligator Jaws (Attachment)
  'hs066': "<b>Une fois révélée</b> : Curtis Connors manigance avec +1[per_hero] MNG. Attachez cette carte à The Lizard.\n[star] <b>Interruption forcée</b> : quand The Lizard attaque, l'attaque gagne perçant.\n<b>Action de héros</b> : dépensez une ressource [physical] et inclinez votre héros → placez Alligator Jaws sous la pile de défausse Rencontre.",
  // hunting_season — Ancient Reptilian Brain (Attachment)
  'hs067': "<b>Une fois révélée</b> : Curtis Connors manigance avec +1[per_hero] MNG. Attachez cette carte à The Lizard.\n[star] <b>Interruption forcée</b> : quand The Lizard attaque et inflige des dégâts à un personnage, infligez à un autre personnage allié autant de dégâts que l'ATQ du personnage attaqué.\n<b>Action de héros</b> : désorientez votre héros → placez Ancient Reptilian Brain sous la pile de défausse Rencontre.",
  // hunting_season — Boa Constricted (Attachment)
  'hs068': "Attachez-la à votre identité.\nL'identité attachée ne peut pas déclencher l'effet \"Action de héros\" des pièces jointes [[REPTILE]].\n<b>Interruption forcée</b> : quand la phase des joueurs se termine, défaussez Boa Constricted.",
  // hunting_season — Boa Constricted (Attachment)
  'hs069': "Attachez-la à votre identité.\nL'identité attachée ne peut pas déclencher l'effet \"Action de héros\" des pièces jointes [[REPTILE]].\n<b>Interruption forcée</b> : quand la phase des joueurs se termine, défaussez Boa Constricted.",
  // hunting_season — Iguana Whip (Treachery)
  'hs070': "<b>Une fois révélée (alter ego)</b> : cette carte gagne renfort.\n<b>Une fois révélée (héros)</b> : le méchant vous attaque. Placez 1 menace sur la manigance principale pour chaque pièce jointe [[REPTILE]] attachée au méchant.\n<hr />\n[star] <b>Boost</b> : si cette activation est une attaque, placez 1 menace sur la manigance principale.",
  // hunting_season — Iguana Whip (Treachery)
  'hs071': "<b>Une fois révélée (alter ego)</b> : cette carte gagne renfort.\n<b>Une fois révélée (héros)</b> : le méchant vous attaque. Placez 1 menace sur la manigance principale pour chaque pièce jointe [[REPTILE]] attachée au méchant.\n<hr />\n[star] <b>Boost</b> : si cette activation est une attaque, placez 1 menace sur la manigance principale.",
  // hunting_season — Triggered Transformation (Treachery)
  'hs072': "<b>Une fois révélée</b> : placez des compteurs de honte sur l'environnement Reptilian Rage pour qu'il en ait 3. Choisissez soit d'incliner votre héros, soit que le méchant manigance. Cette activation ignore les cartes d'état Désorienté.\n<hr />\n[star] <b>Boost</b> : placez 1 compteur de honte sur l'environnement Reptilian Rage.",
  // hunting_season — Triggered Transformation (Treachery)
  'hs073': "<b>Une fois révélée</b> : placez des compteurs de honte sur l'environnement Reptilian Rage pour qu'il en ait 3. Choisissez soit d'incliner votre héros, soit que le méchant manigance. Cette activation ignore les cartes d'état Désorienté.\n<hr />\n[star] <b>Boost</b> : placez 1 compteur de honte sur l'environnement Reptilian Rage.",
  // hunting_season — Shed Skin (Treachery)
  'hs074': "<b>Une fois révélée</b> : soignez 3 dégâts du méchant et retirez-lui chaque carte d'état. Donnez au méchant une carte d'état Tenace.\n<hr />\n[star] <b>Boost</b> : donnez au méchant une carte d'état Tenace.",
  // hunting_season — Shed Skin (Treachery)
  'hs075': "<b>Une fois révélée</b> : soignez 3 dégâts du méchant et retirez-lui chaque carte d'état. Donnez au méchant une carte d'état Tenace.\n<hr />\n[star] <b>Boost</b> : donnez au méchant une carte d'état Tenace.",
  // hunting_season — Iguana (Minion)
  'hs076': "[star] Iguana gagne +1 MNG et +1 ATQ pour chaque carte [[REPTILE]] en jeu (+4 MNG et +4 ATQ au maximum).",
  // hunting_season — The Chameleon (Minion)
  'hs077': "[star] The Chameleon a une MNG et une ATQ égales à celles du méchant.",
  // hunting_season — Reptile Research (SideScheme)
  'hs078': "<b>Une fois révélée</b> : placez 1 menace supplémentaire ici pour chaque carte [[REPTILE]] en jeu.",
  // hunting_season — Reptile Research (SideScheme)
  'hs079': "<b>Une fois révélée</b> : placez 1 menace supplémentaire ici pour chaque carte [[REPTILE]] en jeu.",
  // hunting_season — Vulture (Villain)
  'hs080': "Tant que Vulture a le trait [[AERIAL]], pour pouvoir attaquer Vulture, l'attaquant ou l'attaque doit avoir le trait [[AERIAL]], ou l'attaque doit être à distance (coût supplémentaire).",
  // hunting_season — Vulture (Villain)
  'hs081': "Tant que Vulture a le trait [[AERIAL]], pour pouvoir attaquer Vulture, l'attaquant ou l'attaque doit avoir le trait [[AERIAL]], ou l'attaque doit être à distance (coût supplémentaire).\n[star] <b>Interruption forcée</b> : quand Vulture attaque un personnage à qui il reste moins de la moitié de ses points de vie maximum, il gagne +1 ATQ pour cette attaque.",
  // hunting_season — Vulture (Villain)
  'hs082': "Tant que Vulture a le trait [[AERIAL]], pour pouvoir attaquer Vulture, l'attaquant ou l'attaque doit avoir le trait [[AERIAL]], ou l'attaque doit être à distance (coût supplémentaire).\n[star] <b>Interruption forcée</b> : quand Vulture attaque un personnage à qui il reste moins de la moitié de ses points de vie maximum, il gagne +1 ATQ pour cette attaque.",
  // hunting_season — Aerial Mayhem (MainScheme)
  'hs083a': "<b>Contenu</b> : Vulture (I) et Vulture (II). <i>(Vulture (II) et Vulture (III) à la place en mode expert.)</i> Sets de rencontre Vulture et Standard. Un set de rencontre modulaire <i>(recommandé : Red Vulture)</i>.\n<b>Mise en place</b> : cherchez l'environnement S.H.I.E.L.D. Wingsuits dans le deck Rencontre et la pile de défausse, et mettez-le en jeu. Passez à l'étape 1B.",
  // hunting_season — Aerial Mayhem (MainScheme)
  'hs083b': "<b>Réponse forcée</b> : après qu'un personnage que vous contrôlez sans le trait [[AERIAL]] a contré et retiré des menaces de cette manigance, choisissez soit d'infliger 1 dégât à ce personnage, soit de placer 1 menace sur cette manigance.\n<b>Si cette manigance est complétée, les joueurs perdent la partie.</b>",
  // hunting_season — S.H.I.E.L.D. Wingsuits (Environment)
  'hs084': "<b>Action de héros</b> : dépensez une ressource de n'importe quel type → votre héros et chaque allié que vous contrôlez gagnent le trait [[AERIAL]] jusqu'à la fin du round.",
  // hunting_season — Armadillo (Minion)
  'hs085': "[star] <b>Réponse forcée</b> : après qu'Armadillo a attaqué et infligé des dégâts à un personnage, ce personnage gagne le trait [[AERIAL]] jusqu'à la fin du round.\n<hr />\n[star] <b>Boost</b> : si cette attaque vous inflige des dégâts, vous gagnez le trait [[AERIAL]] jusqu'à la fin du round.",
  // hunting_season — White Rabbit (Minion)
  'hs086': "[star] <b>Réponse forcée</b> : après que White Rabbit vous a attaqué et infligé des dégâts, si vous n'avez pas le trait [[AERIAL]], défaussez une carte au hasard de votre main.\n<hr />\n[star] <b>Boost</b> : si cette attaque vous inflige des dégâts, défaussez une carte de votre main.",
  // hunting_season — Gibbon (Minion)
  'hs087': "Garde.\n<b>Interruption forcée</b> : quand Gibbon devrait subir n'importe quelle quantité de dégâts, prévenez 1 de ces dégâts.",
  // hunting_season — Wing Harness (Attachment)
  'hs088': "Attachez-la à Vulture.\n[star] <b>Interruption forcée</b> : quand Vulture attaque un personnage qui a le trait [[AERIAL]], il gagne +1 ATQ pour cette attaque.\n<b>Action de héros</b> : inclinez votre héros et défaussez 2 cartes de votre main → défaussez Wing Harness. Vulture perd le trait [[AERIAL]] jusqu'à la fin du tour du joueur actif.",
  // hunting_season — Metal Talons (Attachment)
  'hs089': "Attachez-la à Vulture.\nVulture gagne riposte 1.\n[star] <b>Interruption forcée</b> : quand Vulture attaque, l'attaque gagne perçant.\n<b>Réponse de héros</b> : après avoir attaqué Vulture, défaussez une carte de votre main → défaussez Metal Talons.",
  // hunting_season — Projectile Feathers (Attachment)
  'hs090': "Attachez-la à Vulture.\n<b>Interruption forcée</b> : quand Vulture vous attaque, défaussez Projectile Feathers et subissez 2 dégâts indirects (3 dégâts indirects à la place si vous avez le trait [[AERIAL]]).\n<b>Action de héros</b> : dépensez des ressources [energy][energy] → défaussez Projectile Feathers. Vulture perd le trait [[AERIAL]] jusqu'à la fin du tour du joueur actif.",
  // hunting_season — Projectile Feathers (Attachment)
  'hs091': "Attachez-la à Vulture.\n<b>Interruption forcée</b> : quand Vulture vous attaque, défaussez Projectile Feathers et subissez 2 dégâts indirects (3 dégâts indirects à la place si vous avez le trait [[AERIAL]]).\n<b>Action de héros</b> : dépensez des ressources [energy][energy] → défaussez Projectile Feathers. Vulture perd le trait [[AERIAL]] jusqu'à la fin du tour du joueur actif.",
  // hunting_season — Forcefully Elevated (Obligation)
  'hs092': "Vous gagnez le trait [[AERIAL]]. Vous ne pouvez pas passer sous forme d'alter ego.\n<b>Réponse forcée</b> : après avoir attaqué Vulture, choisissez soit de subir 2 dégâts, soit de dépenser une ressource [physical]. Défaussez Forcefully Elevated.",
  // hunting_season — Forcefully Elevated (Obligation)
  'hs093': "Vous gagnez le trait [[AERIAL]]. Vous ne pouvez pas passer sous forme d'alter ego.\n<b>Réponse forcée</b> : après avoir attaqué Vulture, choisissez soit de subir 2 dégâts, soit de dépenser une ressource [physical]. Défaussez Forcefully Elevated.",
  // hunting_season — Aerial Kidnapping (SideScheme)
  'hs094': "Renfort.\n<b>Interruption forcée</b> : quand la phase du méchant commence, placez 3 menaces sur la manigance principale et défaussez Aerial Kidnapping.\n<b>Une fois déjouée</b> : Vulture perd le trait [[AERIAL]] jusqu'à la fin du tour du joueur actif.",
  // hunting_season — Aerial Kidnapping (SideScheme)
  'hs095': "Renfort.\n<b>Interruption forcée</b> : quand la phase du méchant commence, placez 3 menaces sur la manigance principale et défaussez Aerial Kidnapping.\n<b>Une fois déjouée</b> : Vulture perd le trait [[AERIAL]] jusqu'à la fin du tour du joueur actif.",
  // hunting_season — A Feast for Vultures (SideScheme)
  'hs096': "<b>Une fois révélée</b> : placez ici 1 menace supplémentaire pour chaque personnage à qui il reste moins de la moitié de ses points de vie maximum.",
  // hunting_season — Knocked Out of the Sky (Treachery)
  'hs097': "Renfort.\n<b>Une fois révélée</b> : si vous avez le trait [[AERIAL]], vous perdez le trait [[AERIAL]] jusqu'à la fin du round. Si vous avez perdu le trait [[AERIAL]] de cette façon, subissez 2 dégâts.",
  // hunting_season — Knocked Out of the Sky (Treachery)
  'hs098': "Renfort.\n<b>Une fois révélée</b> : si vous avez le trait [[AERIAL]], vous perdez le trait [[AERIAL]] jusqu'à la fin du round. Si vous avez perdu le trait [[AERIAL]] de cette façon, subissez 2 dégâts.",
  // hunting_season — Knocked Out of the Sky (Treachery)
  'hs099': "Renfort.\n<b>Une fois révélée</b> : si vous avez le trait [[AERIAL]], vous perdez le trait [[AERIAL]] jusqu'à la fin du round. Si vous avez perdu le trait [[AERIAL]] de cette façon, subissez 2 dégâts.",
  // hunting_season — Sweeping Swoop (Treachery)
  'hs100': "<b>Une fois révélée</b> : sonnez votre identité et défaussez 1 carte de votre main. Si vous avez le trait [[AERIAL]], cette carte gagne renfort.\n<hr />\n[star] <b>Boost</b> : si le personnage qui s'active a le trait [[AERIAL]], il reçoit une carte de boost supplémentaire pour cette activation.",
  // hunting_season — Sweeping Swoop (Treachery)
  'hs101': "<b>Une fois révélée</b> : sonnez votre identité et défaussez 1 carte de votre main. Si vous avez le trait [[AERIAL]], cette carte gagne renfort.\n<hr />\n[star] <b>Boost</b> : si le personnage qui s'active a le trait [[AERIAL]], il reçoit une carte de boost supplémentaire pour cette activation.",
  // hunting_season — Ravenous Onslaught (Treachery)
  'hs102': "<b>Une fois révélée (alter ego)</b> : Vulture manigance. S'il vous reste moins de la moitié de vos points de vie maximum, cette carte gagne renfort.\n<b>Une fois révélée (héros)</b> : Vulture vous attaque. S'il vous reste moins de la moitié de vos points de vie maximum, cette carte gagne renfort.",
  // hunting_season — Ravenous Onslaught (Treachery)
  'hs103': "<b>Une fois révélée (alter ego)</b> : Vulture manigance. S'il vous reste moins de la moitié de vos points de vie maximum, cette carte gagne renfort.\n<b>Une fois révélée (héros)</b> : Vulture vous attaque. S'il vous reste moins de la moitié de vos points de vie maximum, cette carte gagne renfort.",
  // hunting_season — Kraven The Hunter (Villain)
  'hs104': "<b>Interruption forcée</b> : quand un personnage que vous contrôlez attaque Kraven The Hunter, attribuez-vous une carte [[TRAP]] du deck [[TRAP]]. Révélez chaque carte [[TRAP]] qui vous a été attribuée. (Limite d'une fois par round par joueur.)",
  // hunting_season — Kraven The Hunter (Villain)
  'hs105': "<b>Une fois révélé</b> : cherchez la pièce jointe Tooth Necklace dans le deck Rencontre et la pile de défausse, et révélez-la.\n<b>Interruption forcée</b> : quand un personnage que vous contrôlez attaque Kraven The Hunter, attribuez-vous une carte [[TRAP]] du deck [[TRAP]]. Révélez chaque carte [[TRAP]] qui vous a été attribuée. (Limite d'une fois par round par joueur.)",
  // hunting_season — Kraven The Hunter (Villain)
  'hs106': "<b>Une fois révélé</b> : chaque joueur s'attribue une carte [[TRAP]] du deck [[TRAP]].\n<b>Interruption forcée</b> : quand un personnage que vous contrôlez attaque Kraven The Hunter, attribuez-vous une carte [[TRAP]] du deck [[TRAP]]. Révélez chaque carte [[TRAP]] qui vous a été attribuée. (Limite de deux fois par round et par joueur.)",
  // hunting_season — Acquiring Targets (MainScheme)
  'hs107a': "<b>Contenu</b> : Kraven The Hunter (I) et Kraven The Hunter (II). <i>(Kraven The Hunter (II) et Kraven The Hunter (III) à la place en mode expert.)</i> Sets de rencontre Kraven The Hunter et Standard. Un set de rencontre modulaire <i>(recommandé : Savage Six)</i>.\n<b>Mise en place</b> : mélangez toutes les cartes [[TRAP]] pour former un deck [[TRAP]] séparé. Passez à l'étape 1B.",
  // hunting_season — Acquiring Targets (MainScheme)
  'hs107b': "[star] <b>Interruption forcée</b> : quand vous passez sous forme de héros, placez 2 menaces ici.\n<b>Réponse forcée</b> : après être passé sous forme d'alter ego, retirez 1 menace d'ici.",
  // hunting_season — The Great Hunt (MainScheme)
  'hs108a': "<b>Une fois révélée</b> : cherchez la manigance annexe The Calypso Serum dans le deck Rencontre et la pile de défausse, et révélez-la. Mélangez le deck Rencontre. Passez à l'étape 2B.",
  // hunting_season — The Great Hunt (MainScheme)
  'hs108b': "<b>Réponse forcée</b> : après qu'une carte [[TRAP]] a été révélée, placez 1 menace ici. (Limite d'une fois par round par joueur.)\n<b>Si cette manigance est complétée, les joueurs perdent la partie.</b>",
  // hunting_season — Last Son of Kraven (Minion)
  'hs109': "<b>Interruption forcée</b> : quand un personnage que vous contrôlez attaque Last Son of Kraven, attribuez-vous une carte [[TRAP]] du deck [[TRAP]]. (Limite d'une fois par round.)\n<hr />\n[star] <b>Boost</b> : une fois cette activation terminée, mélangez cette carte dans le deck Rencontre.",
  // hunting_season — Chameleon (Minion)
  'hs110': "Chameleon ne peut pas subir de dégâts.\n<b>Interruption forcée</b> : quand Chameleon devrait attaquer, il manigance à la place.\n<b>Interruption forcée</b> : quand un ennemi devrait être vaincu, défaussez Chameleon à la place.",
  // hunting_season — Poisoned Dagger (Attachment)
  'hs111': "Attachez-la à Kraven The Hunter.\n[star] <b>Réponse forcée</b> : après que Kraven The Hunter a attaqué et infligé des dégâts à un personnage, désorientez ce personnage.\n<b>Interruption</b> : quand vous attaquez Kraven The Hunter, défaussez une carte au hasard de votre main → défaussez cette pièce jointe.",
  // hunting_season — Kraven’s Spear (Attachment)
  'hs112': "Attachez-la à Kraven The Hunter.\nKraven The Hunter gagne riposte 1.\n<b>Interruption</b> : quand vous attaquez Kraven The Hunter, infligez 3 dégâts à votre identité → défaussez cette pièce jointe.",
  // hunting_season — Hunting Rifle (Attachment)
  'hs113': "Attachez-la à Kraven The Hunter.\n<b>Réponse forcée</b> : après que Kraven The Hunter vous a attaqué sans que vous subissiez de dégâts de cette attaque, subissez 1 dégât.\n<b>Interruption</b> : quand vous attaquez Kraven The Hunter, dépensez 2 ressources de n'importe quel type → défaussez cette pièce jointe.",
  // hunting_season — Tooth Necklace (Attachment)
  'hs114': "Attachez-la à Kraven The Hunter.\n[star] <b>Réponse forcée</b> : après que Kraven The Hunter a manigancé, cherchez une pièce jointe [[WEAPON]] dans le deck Rencontre et la pile de défausse, et révélez-la.\n<b>Interruption</b> : quand vous attaquez Kraven The Hunter, placez 2[per_hero] menaces sur la manigance principale → défaussez cette pièce jointe.",
  // hunting_season — The Calypso Serum (SideScheme)
  'hs115': "<b>Une fois révélée</b> : placez 1[per_hero] menace supplémentaire ici.\nChaque ennemi gagne +1 MNG et +1 ATQ.",
  // hunting_season — Toxic Gas (SideScheme)
  'hs116': "<b>Une fois révélée</b> : placez 1[per_hero] menace supplémentaire ici.\nChaque personnage allié subit -1 ATQ.",
  // hunting_season — Predatory Ambush (Treachery)
  'hs117': "<b>Une fois révélée</b> : Kraven The Hunter vous attaque. Si vous êtes sous forme d'alter ego, n'attribuez pas de carte de boost au méchant pour cette activation. Si une pièce jointe [[TRAP]] vous est attachée, attribuez-vous une carte [[TRAP]] du deck [[TRAP]].\n<hr />\n[star] <b>Boost</b> : attribuez-vous une carte [[TRAP]] du deck [[TRAP]].",
  // hunting_season — Predatory Ambush (Treachery)
  'hs118': "<b>Une fois révélée</b> : Kraven The Hunter vous attaque. Si vous êtes sous forme d'alter ego, n'attribuez pas de carte de boost au méchant pour cette activation. Si une pièce jointe [[TRAP]] vous est attachée, attribuez-vous une carte [[TRAP]] du deck [[TRAP]].\n<hr />\n[star] <b>Boost</b> : attribuez-vous une carte [[TRAP]] du deck [[TRAP]].",
  // hunting_season — The Hunt Begins (Treachery)
  'hs119': "<b>Une fois révélée</b> : défaussez X cartes du deck Rencontre, X étant égal au triple du niveau du méchant. Révélez la première pièce jointe [[ITEM]] ou [[WEAPON]] défaussée de cette façon. Si aucune pièce jointe n'a été révélée de cette façon, attribuez-vous une carte [[TRAP]] du deck [[TRAP]].",
  // hunting_season — The Hunt Begins (Treachery)
  'hs120': "<b>Une fois révélée</b> : défaussez X cartes du deck Rencontre, X étant égal au triple du niveau du méchant. Révélez la première pièce jointe [[ITEM]] ou [[WEAPON]] défaussée de cette façon. Si aucune pièce jointe n'a été révélée de cette façon, attribuez-vous une carte [[TRAP]] du deck [[TRAP]].",
  // hunting_season — Big Game Hunter (Treachery)
  'hs121': "<b>Une fois révélée</b> : Kraven The Hunter attaque le héros qui a le plus de points de vie imprimés. Les autres personnages ne peuvent pas défendre contre cette attaque. Si aucune attaque n'a eu lieu de cette façon, attribuez-vous une carte [[TRAP]] du deck [[TRAP]].",
  // hunting_season — Big Game Hunter (Treachery)
  'hs122': "<b>Une fois révélée</b> : Kraven The Hunter attaque le héros qui a le plus de points de vie imprimés. Les autres personnages ne peuvent pas défendre contre cette attaque. Si aucune attaque n'a eu lieu de cette façon, attribuez-vous une carte [[TRAP]] du deck [[TRAP]].",
  // hunting_season — Stalking Prey (Treachery)
  'hs123': "<b>Une fois révélée</b> : attribuez-vous une carte [[TRAP]] du deck [[TRAP]]. Placez 1 menace sur la manigance principale pour chaque carte [[TRAP]] qui vous a été attribuée.\n<hr />\n[star] <b>Boost</b> : si au moins 1 carte [[TRAP]] vous a été attribuée, placez 1 menace sur la manigance principale.",
  // hunting_season — Stalking Prey (Treachery)
  'hs124': "<b>Une fois révélée</b> : attribuez-vous une carte [[TRAP]] du deck [[TRAP]]. Placez 1 menace sur la manigance principale pour chaque carte [[TRAP]] qui vous a été attribuée.\n<hr />\n[star] <b>Boost</b> : si au moins 1 carte [[TRAP]] vous a été attribuée, placez 1 menace sur la manigance principale.",
  // hunting_season — Ferocious Lion (Minion)
  'hs125': "[star] Quand il attaque, Ferocious Lion gagne +1 ATQ si l'attaque n'est pas défendue.\n<b>Réponse forcée</b> : après qu'un personnage contrôlé par le joueur engagé a attaqué Kraven The Hunter, Ferocious Lion attaque ce joueur.",
  // hunting_season — Ferocious Lion (Minion)
  'hs126': "[star] Quand il attaque, Ferocious Lion gagne +1 ATQ si l'attaque n'est pas défendue.\n<b>Réponse forcée</b> : après qu'un personnage contrôlé par le joueur engagé a attaqué Kraven The Hunter, Ferocious Lion attaque ce joueur.",
  // hunting_season — Fierce Cheetah (Minion)
  'hs127': "Les attaques de Fierce Cheetah gagnent perçant.\n<b>Réponse forcée</b> : après qu'un personnage contrôlé par le joueur engagé a attaqué Kraven The Hunter, Fierce Cheetah attaque ce joueur.",
  // hunting_season — Fierce Cheetah (Minion)
  'hs128': "Les attaques de Fierce Cheetah gagnent perçant.\n<b>Réponse forcée</b> : après qu'un personnage contrôlé par le joueur engagé a attaqué Kraven The Hunter, Fierce Cheetah attaque ce joueur.",
  // hunting_season — Bear Trap (Attachment)
  'hs129': "<b>Une fois révélée</b> : choisissez soit d'incliner votre identité, soit d'attacher cette carte à votre identité. Si vous avez incliné votre identité, défaussez cette carte.\n<b>Interruption forcée</b> : quand la phase des joueurs se termine, subissez 1 dégât.\n<b>Action</b> : dépensez une ressource [physical] et subissez 2 dégâts → défaussez cette carte.",
  // hunting_season — Bear Trap (Attachment)
  'hs130': "<b>Une fois révélée</b> : choisissez soit d'incliner votre identité, soit d'attacher cette carte à votre identité. Si vous avez incliné votre identité, défaussez cette carte.\n<b>Interruption forcée</b> : quand la phase des joueurs se termine, subissez 1 dégât.\n<b>Action</b> : dépensez une ressource [physical] et subissez 2 dégâts → défaussez cette carte.",
  // hunting_season — Capture Net (Attachment)
  'hs131': "<b>Une fois révélée</b> : choisissez soit d'incliner votre identité, soit d'attacher cette carte à votre identité. Si vous avez incliné votre identité, défaussez cette carte.\n<b>Interruption forcée</b> : quand la phase des joueurs se termine, dépensez une ressource [physical] ou inclinez votre identité.\n<b>Interruption</b> : quand vous devriez attaquer, dépensez une ressource [physical] → défaussez plutôt Capture Net.",
  // hunting_season — Capture Net (Attachment)
  'hs132': "<b>Une fois révélée</b> : choisissez soit d'incliner votre identité, soit d'attacher cette carte à votre identité. Si vous avez incliné votre identité, défaussez cette carte.\n<b>Interruption forcée</b> : quand la phase des joueurs se termine, dépensez une ressource [physical] ou inclinez votre identité.\n<b>Interruption</b> : quand vous devriez attaquer, dépensez une ressource [physical] → défaussez plutôt Capture Net.",
  // hunting_season — Quicksand (Attachment)
  'hs133': "<b>Une fois révélée</b> : choisissez soit d'incliner votre identité, soit d'attacher cette carte à votre identité. Si vous avez incliné votre identité, défaussez cette carte.\n<b>Interruption</b> : quand vous jouez une carte événement, annulez ses effets et défaussez cet événement → défaussez Quicksand.",
  // hunting_season — Quicksand (Attachment)
  'hs134': "<b>Une fois révélée</b> : choisissez soit d'incliner votre identité, soit d'attacher cette carte à votre identité. Si vous avez incliné votre identité, défaussez cette carte.\n<b>Interruption</b> : quand vous jouez une carte événement, annulez ses effets et défaussez cet événement → défaussez Quicksand.",
  // hunting_season — Tranquilizer Darts (Treachery)
  'hs135': "<b>Une fois révélée</b> : choisissez soit de dépenser une ressource [mental], soit de désorienter votre identité. Si vous ne pouvez faire ni l'un ni l'autre, subissez 1 dégât.",
  // hunting_season — Tranquilizer Darts (Treachery)
  'hs136': "<b>Une fois révélée</b> : choisissez soit de dépenser une ressource [mental], soit de désorienter votre identité. Si vous ne pouvez faire ni l'un ni l'autre, subissez 1 dégât.",
  // hunting_season — Tranquilizer Darts (Treachery)
  'hs137': "<b>Une fois révélée</b> : choisissez soit de dépenser une ressource [mental], soit de désorienter votre identité. Si vous ne pouvez faire ni l'un ni l'autre, subissez 1 dégât.",
  // hunting_season — Swinging Boulder (Treachery)
  'hs138': "<b>Une fois révélée</b> : choisissez soit d'incliner votre identité, soit de défausser un allié que vous contrôlez, soit de défausser une amélioration que vous contrôlez, soit de subir 3 dégâts.",
  // hunting_season — Swinging Boulder (Treachery)
  'hs139': "<b>Une fois révélée</b> : choisissez soit d'incliner votre identité, soit de défausser un allié que vous contrôlez, soit de défausser une amélioration que vous contrôlez, soit de subir 3 dégâts.",
  // hunting_season — Swinging Boulder (Treachery)
  'hs140': "<b>Une fois révélée</b> : choisissez soit d'incliner votre identité, soit de défausser un allié que vous contrôlez, soit de défausser une amélioration que vous contrôlez, soit de subir 3 dégâts.",
  // hunting_season — Feral Instincts (Attachment)
  'hs141': "Attachez-la au méchant.\n[star] <b>Interruption forcée</b> : quand le méchant devrait manigancer contre vous, il vous attaque à la place. Cette attaque gagne déferlement. N'attribuez pas de carte de boost au méchant pour cette activation. Ensuite, défaussez Feral Instincts.",
  // hunting_season — Primal Strength (Attachment)
  'hs142': "Attachez-la au méchant.\nX est égal au niveau du méchant.\n<b>Interruption</b> : quand le méchant vous attaque, choisissez soit de dépenser des ressources [physical][physical], soit d'incliner votre identité → défaussez Primal Strength.",
  // hunting_season — Unleashed Beast (Treachery)
  'hs143': "<b>Une fois révélée</b> : le méchant vous attaque. Si vous êtes sous forme d'alter ego, n'attribuez pas de carte de boost au méchant pour cette activation.\n<hr />\n[star] <b>Boost</b> : cette carte gagne +1 icône de boost ([boost]) si cette activation est une attaque.",
  // hunting_season — Cornered Animal (Treachery)
  'hs144': "<b>Une fois révélée</b> : vous subissez 1 dégât. Si le méchant a subi 6[per_hero] dégâts ou plus, choisissez soit de dépenser une ressource [energy], soit de subir 2 dégâts indirects. Si le méchant a subi 12[per_hero] dégâts ou plus, choisissez soit de défausser une carte au hasard de votre main, soit de placer 2 menaces sur la manigance principale.",
  // hunting_season — Cornered Animal (Treachery)
  'hs145': "<b>Une fois révélée</b> : vous subissez 1 dégât. Si le méchant a subi 6[per_hero] dégâts ou plus, choisissez soit de dépenser une ressource [energy], soit de subir 2 dégâts indirects. Si le méchant a subi 12[per_hero] dégâts ou plus, choisissez soit de défausser une carte au hasard de votre main, soit de placer 2 menaces sur la manigance principale.",
  // hunting_season — Wake Your Inner Lizard (SideScheme)
  'hs146': "<b>Une fois révélée</b> : placez 1[per_hero] menace supplémentaire ici.\n<b>Interruption forcée</b> : quand la phase du méchant commence, cherchez un exemplaire de Lizard Thrall dans le deck Rencontre et la pile de défausse, et mettez-le en jeu engagé avec le premier joueur.",
  // hunting_season — Lizard Thrall (Minion)
  'hs147': "[star] <b>Interruption forcée</b> : quand Lizard Thrall devrait manigancer, il attaque à la place, sans déclencher son effet \"Interruption forcée\".\n[star] <b>Interruption forcée</b> : quand Lizard Thrall devrait attaquer, il manigance à la place, sans déclencher son effet \"Interruption forcée\".",
  // hunting_season — Lizard Thrall (Minion)
  'hs148': "[star] <b>Interruption forcée</b> : quand Lizard Thrall devrait manigancer, il attaque à la place, sans déclencher son effet \"Interruption forcée\".\n[star] <b>Interruption forcée</b> : quand Lizard Thrall devrait attaquer, il manigance à la place, sans déclencher son effet \"Interruption forcée\".",
  // hunting_season — Lizard Thrall (Minion)
  'hs149': "[star] <b>Interruption forcée</b> : quand Lizard Thrall devrait manigancer, il attaque à la place, sans déclencher son effet \"Interruption forcée\".\n[star] <b>Interruption forcée</b> : quand Lizard Thrall devrait attaquer, il manigance à la place, sans déclencher son effet \"Interruption forcée\".",
  // hunting_season — Lizard Thrall (Minion)
  'hs150': "[star] <b>Interruption forcée</b> : quand Lizard Thrall devrait manigancer, il attaque à la place, sans déclencher son effet \"Interruption forcée\".\n[star] <b>Interruption forcée</b> : quand Lizard Thrall devrait attaquer, il manigance à la place, sans déclencher son effet \"Interruption forcée\".",
  // hunting_season — Vulture (James Natale) (Minion)
  'hs151': "Coup Rapide. Vilenie.\n[star] <b>Réponse forcée</b> : après que Vulture (James Natale) vous a attaqué et infligé des dégâts, défaussez autant de cartes du dessus de votre deck que de dégâts subis.",
  // hunting_season — The Red Vulture (SideScheme)
  'hs152': "<b>Une fois révélée</b> : cherchez Vulture (James Natale) dans le deck Rencontre et la pile de défausse, et mettez-le en jeu engagé avec l'identité à qui il reste le moins de points de vie.",
  // hunting_season — Acid Expulsion (Treachery)
  'hs153': "<b>Une fois révélée</b> : défaussez les 5 cartes du dessus du deck Rencontre. Pour chaque icône de boost sur les cartes défaussées de cette façon, défaussez la carte du dessus de votre deck.\n<hr />\n[star] <b>Boost</b> : après cette attaque, défaussez la carte du dessus de votre deck pour chaque dégât subi lors de cette attaque.",
  // hunting_season — Acid Expulsion (Treachery)
  'hs154': "<b>Une fois révélée</b> : défaussez les 5 cartes du dessus du deck Rencontre. Pour chaque icône de boost sur les cartes défaussées de cette façon, défaussez la carte du dessus de votre deck.\n<hr />\n[star] <b>Boost</b> : après cette attaque, défaussez la carte du dessus de votre deck pour chaque dégât subi lors de cette attaque.",
  // hunting_season — Voracious Ambush (Treachery)
  'hs155': "<b>Une fois révélée (héros)</b> : Vulture (James Natale) attaque votre héros. Si Vulture (James Natale) ne vous a pas attaqué de cette façon, défaussez les 6 cartes du dessus du deck Rencontre et, si Vulture (James Natale) est dans la pile de défausse Rencontre, mettez-le en jeu engagé avec vous.",
  // hunting_season — Voracious Ambush (Treachery)
  'hs156': "<b>Une fois révélée (héros)</b> : Vulture (James Natale) attaque votre héros. Si Vulture (James Natale) ne vous a pas attaqué de cette façon, défaussez les 6 cartes du dessus du deck Rencontre et, si Vulture (James Natale) est dans la pile de défausse Rencontre, mettez-le en jeu engagé avec vous.",
  // hunting_season — The Savage Six (SideScheme)
  'hs157': "<b>Une fois révélée</b> : chaque sbire [[SAVAGE SIX]] attaque le héros avec lequel il est engagé. Si aucune attaque n'a eu lieu de cette façon, cherchez un sbire [[SAVAGE SIX]] dans le deck Rencontre et la pile de défausse, et mettez-le en jeu engagé avec le premier joueur.",
  // hunting_season — Vulture (Minion)
  'hs158': "[star] <b>Réponse forcée</b> : après que Vulture vous a attaqué, attribuez-vous une carte Rencontre. Ensuite, mélangez Vulture dans le deck Rencontre.\n<hr />\n[star] <b>Boost</b> : une fois cette activation terminée, mélangez cette carte dans le deck Rencontre.",
  // hunting_season — Rhino (Minion)
  'hs159': "[star] Les attaques de Rhino gagnent déferlement.\n<b>Interruption forcée</b> : quand la phase du méchant se termine, donnez à Rhino une carte d'état Tenace.\n<hr />\n[star] <b>Boost</b> : cette attaque gagne déferlement.",
  // hunting_season — Scorpion (Minion)
  'hs160': "[star] Scorpion gagne +1 MNG tant que l'identité avec laquelle il est engagé est sonnée.\n[star] <b>Réponse forcée</b> : après que Scorpion a attaqué et infligé des dégâts à un personnage, ce personnage est sonné.\n<hr />\n[star] <b>Boost</b> : cette carte gagne +1 icône de boost ([boost]) si vous êtes sonné.",
  // hunting_season — Tarantula (Minion)
  'hs161': "[star] Tarantula gagne +1 ATQ tant que l'identité avec laquelle il est engagé est désorientée.\n[star] <b>Réponse forcée</b> : après que Tarantula a attaqué et infligé des dégâts à un personnage, ce personnage est désorienté.\n<hr />\n[star] <b>Boost</b> : cette carte gagne +1 icône de boost ([boost]) si vous êtes désorienté.",
  // hunting_season — King Cobra (Minion)
  'hs162': "Tant que King Cobra est engagé avec vous, votre héros ne peut pas attaquer d'autres ennemis.\n<hr />\n[star] <b>Boost</b> : si cette attaque vous inflige des dégâts, inclinez votre identité.",
  // hunting_season — Stegron (Minion)
  'hs163': "[star] Stegron gagne +1 MNG pour chaque ennemi [[SAVAGE SIX]] en jeu (+4 MNG au maximum).\n<b>Réponse forcée</b> : après que Stegron est entré en jeu, il manigance.\n<hr />\n[star] <b>Boost</b> : cette carte gagne +1 icône de boost ([boost]) si au moins un sbire [[SAVAGE SIX]] est en jeu.",
  // hunting_season — Rocket Raccoon (Ally)
  'hs164': "Coût d'expérience 4.\n[star] L'attaque de base de Rocket Raccoon gagne à distance, perçant et déferlement.",
  // hunting_season — Old Man Logan (Ally)
  'hs165': "Coût d'expérience 4.\n<b>Interruption</b> : quand Old Man Logan défend contre une attaque, infligez à l'attaquant autant de dégâts que l'ATQ d'Old Man Logan.",
  // hunting_season — Black Cat (Ally)
  'hs166': "Coût d'expérience 4.\n[star] <b>Réponse forcée</b> : après que Black Cat a contré, défaussez la carte du dessus de votre deck. Si cette carte a une ressource [mental] imprimée, ajoutez-la à votre main.",
  // hunting_season — Ka-Zar (Ally)
  'hs167': "Coût d'expérience 4.\n<b>Réponse</b> : après que Ka-Zar est entré en jeu, infligez au méchant autant de dégâts que son niveau.",
  // hunting_season — Gibbon (Ally)
  'hs168': "Coût d'expérience 1.\n<b>Interruption</b> : quand Gibbon devrait subir n'importe quelle quantité de dégâts, prévenez 1 de ces dégâts. (Limite d'une fois par phase.)",
  // hunting_season — Evade (Event)
  'hs169': "Coût d'expérience 2.\n<b>Interruption</b> : quand vous devriez subir n'importe quelle quantité de dégâts d'une attaque, prévenez 3 de ces dégâts. Si vous n'avez subi aucun dégât de cette attaque, piochez 1 carte.",
  // hunting_season — Evade (Event)
  'hs170': "Coût d'expérience 2.\n<b>Interruption</b> : quand vous devriez subir n'importe quelle quantité de dégâts d'une attaque, prévenez 3 de ces dégâts. Si vous n'avez subi aucun dégât de cette attaque, piochez 1 carte.",
  // hunting_season — Evade (Event)
  'hs171': "Coût d'expérience 2.\n<b>Interruption</b> : quand vous devriez subir n'importe quelle quantité de dégâts d'une attaque, prévenez 3 de ces dégâts. Si vous n'avez subi aucun dégât de cette attaque, piochez 1 carte.",
  // hunting_season — Taunt (Event)
  'hs172': "Coût d'expérience 1.\n<b>Action de héros</b> : attribuez au méchant jusqu'à 3 cartes de boost face cachée. Piochez 1 carte pour chaque carte de boost face cachée attribuée au méchant de cette façon.",
  // hunting_season — Taunt (Event)
  'hs173': "Coût d'expérience 1.\n<b>Action de héros</b> : attribuez au méchant jusqu'à 3 cartes de boost face cachée. Piochez 1 carte pour chaque carte de boost face cachée attribuée au méchant de cette façon.",
  // hunting_season — Taunt (Event)
  'hs174': "Coût d'expérience 1.\n<b>Action de héros</b> : attribuez au méchant jusqu'à 3 cartes de boost face cachée. Piochez 1 carte pour chaque carte de boost face cachée attribuée au méchant de cette façon.",
  // hunting_season — Steadfast (Event)
  'hs175': "Coût d'expérience 3.\n<b>Interruption de héros</b> : quand vous révélez une carte Rencontre, dépensez une ressource [physical] → annulez les effets \"Une fois révélée\" de cette carte Rencontre.",
  // hunting_season — Steadfast (Event)
  'hs176': "Coût d'expérience 3.\n<b>Interruption de héros</b> : quand vous révélez une carte Rencontre, dépensez une ressource [physical] → annulez les effets \"Une fois révélée\" de cette carte Rencontre.",
  // hunting_season — Steadfast (Event)
  'hs177': "Coût d'expérience 3.\n<b>Interruption de héros</b> : quand vous révélez une carte Rencontre, dépensez une ressource [physical] → annulez les effets \"Une fois révélée\" de cette carte Rencontre.",
  // hunting_season — Finish Them Off (Event)
  'hs178': "Coût d'expérience 2.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Si cet ennemi a été vaincu de cette façon, piochez 2 cartes.",
  // hunting_season — Finish Them Off (Event)
  'hs179': "Coût d'expérience 2.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Si cet ennemi a été vaincu de cette façon, piochez 2 cartes.",
  // hunting_season — Finish Them Off (Event)
  'hs180': "Coût d'expérience 2.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Si cet ennemi a été vaincu de cette façon, piochez 2 cartes.",
  // hunting_season — Fresh Tracks (Event)
  'hs181': "Coût d'expérience 2.\n<b>Interruption</b> : quand vous contrez, augmentez de 2 la quantité de menaces retirée par ce contre. Si ce contre retire la dernière menace d'une manigance, infligez 1 dégât à un ennemi et piochez 1 carte.",
  // hunting_season — Fresh Tracks (Event)
  'hs182': "Coût d'expérience 2.\n<b>Interruption</b> : quand vous contrez, augmentez de 2 la quantité de menaces retirée par ce contre. Si ce contre retire la dernière menace d'une manigance, infligez 1 dégât à un ennemi et piochez 1 carte.",
  // hunting_season — Fresh Tracks (Event)
  'hs183': "Coût d'expérience 2.\n<b>Interruption</b> : quand vous contrez, augmentez de 2 la quantité de menaces retirée par ce contre. Si ce contre retire la dernière menace d'une manigance, infligez 1 dégât à un ennemi et piochez 1 carte.",
  // hunting_season — Savage Land (Support)
  'hs184': "Coût d'expérience 4.\n<b>Action de héros</b> : inclinez Savage Land et infligez 1 dégât à un héros ou à un allié → ce personnage gagne +1 CTR et +1 ATQ jusqu'à la fin du round.",
  // hunting_season — Hunting Rifle (Upgrade)
  'hs185': "Coût d'expérience 2.\nRestreint. Utilisations (3 jetons Munition).\n<b>Action de héros</b> <i>(attaque)</i> : inclinez Hunting Rifle et retirez-en 1 jeton Munition → infligez 2 dégâts à un ennemi. Cette attaque gagne à distance.",
  // hunting_season — Hunting Rifle (Upgrade)
  'hs186': "Coût d'expérience 2.\nRestreint. Utilisations (3 jetons Munition).\n<b>Action de héros</b> <i>(attaque)</i> : inclinez Hunting Rifle et retirez-en 1 jeton Munition → infligez 2 dégâts à un ennemi. Cette attaque gagne à distance.",
  // hunting_season — Hunting Rifle (Upgrade)
  'hs187': "Coût d'expérience 2.\nRestreint. Utilisations (3 jetons Munition).\n<b>Action de héros</b> <i>(attaque)</i> : inclinez Hunting Rifle et retirez-en 1 jeton Munition → infligez 2 dégâts à un ennemi. Cette attaque gagne à distance.",
  // hunting_season — Hatchet (Upgrade)
  'hs188': "Coût d'expérience 2.\nRestreint.\n<b>Interruption</b> : quand vous effectuez une attaque de base, inclinez Hatchet → vous gagnez +1 ATQ pour cette attaque.",
  // hunting_season — Hatchet (Upgrade)
  'hs189': "Coût d'expérience 2.\nRestreint.\n<b>Interruption</b> : quand vous effectuez une attaque de base, inclinez Hatchet → vous gagnez +1 ATQ pour cette attaque.",
  // hunting_season — Hatchet (Upgrade)
  'hs190': "Coût d'expérience 2.\nRestreint.\n<b>Interruption</b> : quand vous effectuez une attaque de base, inclinez Hatchet → vous gagnez +1 ATQ pour cette attaque.",
  // hunting_season — Hunterbot (Upgrade)
  'hs191': "Coût d'expérience 3.\n1 max par joueur.\nVotre héros gagne +1 ATQ.\n<b>Interruption forcée</b> : quand vous devriez subir n'importe quelle quantité de dégâts, placez-les ici à la place. Ensuite, s'il y a 3 dégâts ou plus ici, défaussez Hunterbot.",
  // hunting_season — Hunterbot (Upgrade)
  'hs192': "Coût d'expérience 3.\n1 max par joueur.\nVotre héros gagne +1 ATQ.\n<b>Interruption forcée</b> : quand vous devriez subir n'importe quelle quantité de dégâts, placez-les ici à la place. Ensuite, s'il y a 3 dégâts ou plus ici, défaussez Hunterbot.",
  // hunting_season — Hunterbot (Upgrade)
  'hs193': "Coût d'expérience 3.\n1 max par joueur.\nVotre héros gagne +1 ATQ.\n<b>Interruption forcée</b> : quand vous devriez subir n'importe quelle quantité de dégâts, placez-les ici à la place. Ensuite, s'il y a 3 dégâts ou plus ici, défaussez Hunterbot.",
  // hunting_season — Trap (Upgrade)
  'hs194': "Coût d'expérience 1.\n<b>Interruption</b> : quand un ennemi vous attaque, défaussez Trap → infligez 2 dégâts à cet ennemi. Si cet ennemi a été vaincu de cette façon, renvoyez Trap dans votre main.",
  // hunting_season — Trap (Upgrade)
  'hs195': "Coût d'expérience 1.\n<b>Interruption</b> : quand un ennemi vous attaque, défaussez Trap → infligez 2 dégâts à cet ennemi. Si cet ennemi a été vaincu de cette façon, renvoyez Trap dans votre main.",
  // hunting_season — Trap (Upgrade)
  'hs196': "Coût d'expérience 1.\n<b>Interruption</b> : quand un ennemi vous attaque, défaussez Trap → infligez 2 dégâts à cet ennemi. Si cet ennemi a été vaincu de cette façon, renvoyez Trap dans votre main.",
  // hunting_season — In Hiding (Upgrade)
  'hs197': "Coût d'expérience 2.\n<b>Interruption de héros</b> : quand un ennemi devrait vous attaquer, défaussez In Hiding → cet ennemi manigance à la place, sans recevoir de carte de boost pour cette activation.",
  // hunting_season — In Hiding (Upgrade)
  'hs198': "Coût d'expérience 2.\n<b>Interruption de héros</b> : quand un ennemi devrait vous attaquer, défaussez In Hiding → cet ennemi manigance à la place, sans recevoir de carte de boost pour cette activation.",
  // hunting_season — In Hiding (Upgrade)
  'hs199': "Coût d'expérience 2.\n<b>Interruption de héros</b> : quand un ennemi devrait vous attaquer, défaussez In Hiding → cet ennemi manigance à la place, sans recevoir de carte de boost pour cette activation.",
  // hunting_season — Vermin (Ally)
  'hs200': "Vermin entre en jeu avec 3 compteurs de rat.\n<b>Interruption</b> : quand Vermin attaque, retirez-lui un compteur de rat → Vermin ne subit pas de dégâts consécutifs pour cette attaque.",
  // hunting_season — Scorpion (Ally)
  'hs201': "<b>Réponse</b> : après que Scorpion a attaqué et infligé des dégâts à un ennemi, infligez 1 dégât à Scorpion → sonnez cet ennemi et infligez-lui 1 dégât.",
  // hunting_season — Lizard (Ally)
  'hs202': "Tant que vous êtes sous forme d'alter ego, Lizard gagne +3 CTR.\nTant que vous êtes sous forme de héros, Lizard gagne +3 ATQ.",
  // hunting_season — Vulture (Ally)
  'hs203': "<b>Action</b> : inclinez Vulture et infligez-lui 1 dégât → redressez un personnage allié, qui gagne le trait [[AERIAL]] jusqu'à la fin de la phase.",
  // hunting_season — Vermin (Minion)
  'hs204': "Vermin entre en jeu avec 3 compteurs de rat.\n<b>Interruption forcée</b> : quand Vermin devrait subir n'importe quelle quantité de dégâts, retirez-lui plutôt un compteur de rat.",
  // hunting_season — Lizard (Minion)
  'hs205': "Coup Rapide. Riposte 1.\n<b>Interruption forcée</b> : quand Lizard attaque, l'attaque gagne perçant.",
  // hunting_season — Son of Kraven (Minion)
  'hs206': "Coup Rapide.",
  // hunting_season — Son of Kraven (Minion)
  'hs210': "Coup Rapide.",
  // hunting_season — Son of Kraven (Minion)
  'hs214': "Coup Rapide.",
  // hunting_season — Son of Kraven (Minion)
  'hs218': "Coup Rapide.",
  // hunting_season — Captured! (Obligation)
  'hs207': "Vous ne pouvez pas changer de forme.\n<b>Action</b> : inclinez votre identité → défaussez Captured!",
  // hunting_season — Captured! (Obligation)
  'hs211': "Vous ne pouvez pas changer de forme.\n<b>Action</b> : inclinez votre identité → défaussez Captured!",
  // hunting_season — Captured! (Obligation)
  'hs215': "Vous ne pouvez pas changer de forme.\n<b>Action</b> : inclinez votre identité → défaussez Captured!",
  // hunting_season — Captured! (Obligation)
  'hs219': "Vous ne pouvez pas changer de forme.\n<b>Action</b> : inclinez votre identité → défaussez Captured!",
  // hunting_season — Hunted! (Obligation)
  'hs208': "Chaque sbire engagé avec vous gagne coup rapide.\n<b>Action d'alter ego</b> : défaussez une carte de votre main → défaussez Hunted!",
  // hunting_season — Hunted! (Obligation)
  'hs212': "Chaque sbire engagé avec vous gagne coup rapide.\n<b>Action d'alter ego</b> : défaussez une carte de votre main → défaussez Hunted!",
  // hunting_season — Hunted! (Obligation)
  'hs216': "Chaque sbire engagé avec vous gagne coup rapide.\n<b>Action d'alter ego</b> : défaussez une carte de votre main → défaussez Hunted!",
  // hunting_season — Hunted! (Obligation)
  'hs220': "Chaque sbire engagé avec vous gagne coup rapide.\n<b>Action d'alter ego</b> : défaussez une carte de votre main → défaussez Hunted!",
  // hunting_season — Poisoned! (Treachery)
  'hs209': "<b>Une fois révélée</b> : choisissez soit de dépenser une ressource [energy], soit de subir 2 dégâts.",
  // hunting_season — Poisoned! (Treachery)
  'hs213': "<b>Une fois révélée</b> : choisissez soit de dépenser une ressource [energy], soit de subir 2 dégâts.",
  // hunting_season — Poisoned! (Treachery)
  'hs217': "<b>Une fois révélée</b> : choisissez soit de dépenser une ressource [energy], soit de subir 2 dégâts.",
  // hunting_season — Poisoned! (Treachery)
  'hs221': "<b>Une fois révélée</b> : choisissez soit de dépenser une ressource [energy], soit de subir 2 dégâts.",
  // hunting_season — Rabid Rodents (Environment)
  'hs222': "<i>Mode Hunter uniquement.</i>\nVermin et Vermin Clone gagnent +1 ATQ.\n<b>Réponse forcée</b> : après qu'un sbire [[RAT]] est entré en jeu, placez 1 menace sur ce sbire.",
  // hunting_season — Sting of the Scorpion (Environment)
  'hs223': "<i>Mode Hunter uniquement.</i>\n<b>Réponse forcée</b> : après la fin de la phase du méchant, le premier joueur doit choisir soit de placer 1 compteur de blessure sur J. Jonah Jameson, soit de défausser des cartes du dessus du deck Rencontre jusqu'à défausser une pièce jointe, et de la révéler.",
  // hunting_season — Cold Blooded (Environment)
  'hs224': "<i>Mode Hunter uniquement.</i>\nLa valeur de menace cible de la manigance principale est réduite de 1[per_hero].\n<b>Réponse forcée</b> : après que Curtis Connors s'est activé contre votre héros, attribuez-vous 1 carte Rencontre face cachée.",
  // hunting_season — Aerial Excellence (Environment)
  'hs225': "<i>Mode Hunter uniquement.</i>\n<b>Réponse forcée</b> : après l'étape 1 de la phase du méchant, placez 1 menace sur la manigance principale pour chaque identité sans le trait [[AERIAL]]. Chaque identité qui a le trait [[AERIAL]] subit 2 dégâts indirects.",
  // hunting_season — Master Trapper (Environment)
  'hs226': "<i>Mode Hunter uniquement.</i>\n<b>Réponse forcée</b> : après l'étape 1 de la phase du méchant, attribuez à chaque joueur 1 carte [[TRAP]] face cachée.\n<b>Interruption forcée</b> : quand la pile de défausse [[TRAP]] est remélangée dans le deck [[TRAP]], attribuez au premier joueur 1 carte Rencontre face cachée.",
  // skrull_menace — Hulkling (Hero)
  'sk001a': "<i>Descendant des deux races</i> — <b>Réponse</b> : après avoir joué depuis votre main une carte avec le trait [[KREE]] ou [[SKRULL]], si vous partagez ce trait, piochez 1 carte. <i>(Limite d'une fois par round.)</i>",
  // skrull_menace — Teddy Altman (AlterEgo)
  'sk001b': "<i>Hybride Kree/Skrull</i> — <b>Mise en place</b> : mettez en jeu votre amélioration de forme d'origine, face Skrull Origin visible.\n<b>Réponse</b> : après avoir changé de forme d'origine, soignez 1 dégât de Teddy Altman.",
  // skrull_menace — Skrull Origin (Upgrade)
  'sk002a': "Forme d'origine. Permanent.\nHulkling gagne le trait [[SKRULL]].\n<b>Action</b> : inclinez cette carte → retournez cette carte.\n<b>Réponse</b> : après avoir dépensé une carte avec le trait [[KREE]], inclinez cette carte → piochez 1 carte.",
  // skrull_menace — Kree Origin (Upgrade)
  'sk002b': "Forme d'origine. Permanent.\nHulkling gagne le trait [[KREE]].\n<b>Action</b> : inclinez cette carte → retournez cette carte.\n<b>Réponse</b> : après avoir dépensé une carte avec le trait [[SKRULL]], inclinez cette carte → piochez 1 carte.",
  // skrull_menace — Wiccan (Ally)
  'sk003': "Tant que vous avez le trait [[KREE]], Wiccan gagne +1 ATQ.\nTant que vous avez le trait [[SKRULL]], Wiccan gagne +1 CTR.",
  // skrull_menace — Kree Durability (Event)
  'sk004': "<b>Réponse de héros</b> : après avoir changé de forme, redressez Hulkling et donnez-lui une carte d'état Tenace.",
  // skrull_menace — Kree Ferocity (Event)
  'sk005': "<b>Interruption de héros</b> : quand vous effectuez une attaque de base, vous gagnez +6 ATQ pour cette attaque. Vous pouvez subir 2 dégâts indirects → cette attaque gagne déferlement.",
  // skrull_menace — Shift and Strike (Event)
  'sk006': "<b>Réponse de héros</b> <i>(attaque)</i> : après avoir changé de forme, infligez 4 dégâts à un ennemi. Si vous avez le trait [[SKRULL]], désorientez cet ennemi. Si vous avez le trait [[KREE]], sonnez cet ennemi.",
  // skrull_menace — Skrull Infiltration (Event)
  'sk007': "<b>Action de héros</b> <i>(contre)</i> : retirez 4 menaces d'une manigance. Vous pouvez subir 2 dégâts indirects → ce contre ignore le mot-clé patrouille et l'icône de crise ([crisis]).",
  // skrull_menace — Skrull Regeneration (Event)
  'sk008': "<b>Action de héros</b> : redressez Hulkling. Soignez 2 dégâts de Hulkling pour chaque ressource surpayée pour cette carte.",
  // skrull_menace — Alliance (Support)
  'sk009': "<b>Réponse</b> : après avoir joué depuis votre main une carte avec le trait [[KREE]], infligez 1 dégât à un ennemi.\n<b>Réponse</b> : après avoir joué depuis votre main une carte avec le trait [[SKRULL]], retirez 1 menace de la manigance principale.",
  // skrull_menace — Ancestors (Support)
  'sk010': "Utilisations (2 jetons individual).\n<b>Action</b> : inclinez cette carte et retirez-en 1 jeton individual → choisissez 1 carte de votre main ou en jeu. Cette carte gagne le trait [[KREE]] ou [[SKRULL]] jusqu'à la fin du round.",
  // skrull_menace — Changeling (Upgrade)
  'sk011': "Hulkling gagne le trait [[AERIAL]].\n<b>Interruption</b> : quand vous utilisez une capacité de base, inclinez Changeling → vous gagnez +1 à cette capacité pour cette utilisation.",
  // skrull_menace — Emperor Dorrek-Vell (Upgrade)
  'sk012': "Tant que vous avez le trait [[KREE]], chaque allié que vous contrôlez gagne +1 ATQ.\nTant que vous avez le trait [[SKRULL]], chaque allié que vous contrôlez gagne +1 CTR.",
  // skrull_menace — Excelsior (Upgrade)
  'sk013': "Restreint. <i>(Maximum 2 cartes restreintes par joueur.)</i>\nTant qu'Excelsior est redressée, les attaques de base de Hulkling gagnent perçant.\n<b>Ressource</b> : inclinez Excelsior → générez une ressource [energy].",
  // skrull_menace — Nega Rings (Upgrade)
  'sk014': "<b>Action de héros</b> : inclinez Nega Rings et dépensez une ressource [energy] → choisissez une carte de votre main et échangez-la avec une carte de votre choix de votre défausse.",
  // skrull_menace — Lauri-Ell (Ally)
  'sk015': "<b>Réponse</b> : après que Lauri-Ell a subi n'importe quelle quantité de dégâts d'une attaque, donnez-lui une carte d'état Tenace.",
  // skrull_menace — Mur-G'nn (Ally)
  'sk016': "<b>Action</b> : inclinez Mur-G'nn et infligez-lui 1 dégât → défaussez la carte du dessus de votre deck. Si la ressource imprimée de cette carte a :\n[physical] - redressez une carte que vous contrôlez.\n[energy] - donnez une carte d'état Tenace à une identité.\n[mental] - soignez 3 dégâts d'un personnage.",
  // skrull_menace — Provoked! (Event)
  'sk019': "<b>Réponse de héros</b> : après vous être défendu contre une attaque et avoir subi au moins 1 dégât, redressez votre héros.",
  // skrull_menace — Deflect the Blow (Upgrade)
  'sk021': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous êtes censé subir n'importe quelle quantité de dégâts d'une attaque, défaussez Deflect the Blow et inclinez votre héros, prévenez la totalité de ces dégâts.",
  // skrull_menace — Talos (Ally)
  'sk023': "<b>Interruption</b> : quand Talos est censé subir n'importe quelle quantité de dégâts consécutifs, infligez ces dégâts à un autre personnage que vous contrôlez.",
  // skrull_menace — Drunk in Love (Event)
  'sk024': "<b>Action</b> : désorientez votre identité → soignez 4 dégâts de votre identité.",
  // skrull_menace — Strength in Otherness (Event)
  'sk025': "En Équipe (Hulkling et Wiccan). 1 max par deck.\n<b>Action de héros</b> <i>(attaque/contre)</i> : retirez 1 menace de la manigance principale et infligez 1 dégât au méchant pour chaque type de carte différent dans votre défausse.",
  // skrull_menace — Glorious Flight (Upgrade)
  'sk029': "Ne jouez cette carte que si vous avez un trait [[AERIAL]].\n<b>Réponse de héros</b> : après avoir vaincu un ennemi ou une manigance annexe, défaussez Glorious Flight → redressez votre héros.",
  // skrull_menace — Pride (Upgrade)
  'sk030': "1 max par joueur.\n<b>Action</b> : inclinez Pride → défaussez la carte du dessus de votre deck. Si c'est une carte propre à une identité, ajoutez-la à votre main.",
  // skrull_menace — Interracial Hatred (Obligation)
  'sk031': "<b><i>Donnez cette carte au joueur Teddy Altman.</i></b>\nLes cartes avec le trait [[KREE]] et [[SKRULL]] que vous contrôlez ne peuvent pas se redresser.\n<b>Action d'alter ego</b> : inclinez Teddy Altman → défaussez cette obligation.",
  // skrull_menace — Empress R'Klll (Minion)
  'sk032': "Vilenie.\n[star] Les attaques d'Empress R'Klll gagnent perçant.\n<b>Une fois révélée</b> : Empress R'Klll attaque chaque joueur sous forme de héros.\n<i>(Sbire némésis de Hulkling.)</i>",
  // skrull_menace — DNA Masking (SideScheme)
  'sk033': "Les sbires ne peuvent pas subir de dégâts.\nLes menaces ne peuvent pas être retirées de DNA Masking tant qu'il n'y a aucun sbire en jeu.",
  // skrull_menace — Inhibited (Attachment)
  'sk034': "Attachez cette carte à votre identité.\nVous ne pouvez pas changer de forme ni jouer de cartes qui partagent un [[TRAIT]] avec votre identité.\n<b>Action</b> : dépensez des ressources [physical][physical] → défaussez cette carte.",
  // skrull_menace — Assailed by Their Own (Treachery)
  'sk035': "<b>Une fois révélée (alter ego)</b> : inclinez votre identité.\n<b>Une fois révélée (héros)</b> : choisissez un personnage en jeu <i>(autre que votre identité)</i> qui partage un [[TRAIT]] avec votre héros. Subissez X dégâts, X étant égal à l'ATQ du personnage choisi. Sinon, inclinez votre identité.",
  // skrull_menace — Swapping Roles (Treachery)
  'sk036': "<b>Une fois révélée</b> : inclinez chaque carte que vous contrôlez qui partage un [[TRAIT]] avec votre identité <i>(y compris votre identité)</i>.\n[star] <b>Boost</b> : inclinez chaque carte que vous contrôlez qui partage un [[TRAIT]] avec votre identité <i>(à l'exception de votre identité)</i>.",
  // skrull_menace — Emperor Dorrek I (Villain, stade I)
  'sk070': "Riposte 1.\n[star] Les attaques d'Emperor Dorrek I gagnent Distance.",
  // skrull_menace — Emperor Dorrek I (Villain, stade II)
  'sk071': "Riposte 1.\n[star] Les attaques d'Emperor Dorrek I gagnent Distance.",
  // skrull_menace — Emperor Dorrek I (Villain, stade III)
  'sk072': "Riposte 2.\n[star] Les attaques d'Emperor Dorrek I gagnent Distance.",
  // skrull_menace — Emperor Dorrek VII (Villain, stade I)
  'sk073': "Incitation 1[per_hero].\n[star] Les attaques d'Emperor Dorrek VII gagnent Déferlement.",
  // skrull_menace — Emperor Dorrek VII (Villain, stade II)
  'sk074': "Incitation 1[per_hero].\n[star] Les attaques d'Emperor Dorrek VII gagnent Déferlement.",
  // skrull_menace — Emperor Dorrek VII (Villain, stade III)
  'sk075': "Incitation 1[per_hero].\n[star] Les attaques d'Emperor Dorrek VII gagnent Déferlement.",
  // skrull_menace — Empress R'Klll (Villain, stade I)
  'sk076': "<b>Une fois révélée</b> : Empress R'Klll attaque chaque joueur sous forme de héros.\n[star] Les attaques d'Empress R'Klll gagnent Perçant.",
  // skrull_menace — Empress R'Klll (Villain, stade II)
  'sk077': "<b>Une fois révélée</b> : Empress R'Klll attaque chaque joueur sous forme de héros.\n[star] Les attaques d'Empress R'Klll gagnent Perçant.",
  // skrull_menace — Empress R'Klll (Villain, stade III)
  'sk078': "<b>Une fois révélée</b> : Empress R'Klll attaque chaque joueur sous forme de héros.\n[star] Les attaques d'Empress R'Klll gagnent Perçant.",
  // skrull_menace — Empress S'Byll (Villain, stade I)
  'sk079': "Solide. Ténacité.",
  // skrull_menace — Empress S'Byll (Villain, stade II)
  'sk080': "Solide. Ténacité.",
  // skrull_menace — Empress S'Byll (Villain, stade III)
  'sk081': "Robuste. Ténacité.",
  // skrull_menace — Rise of the Skrull Empire 1A (MainScheme)
  'sk082a': "<b>Contenu</b> : tous les méchants (I) et (II) <i>(stades (II) et (III) en mode expert)</i>. Sets Skrull Empire, Skrull Society et Standard. Un set modulaire <i>(Army of Skrulls)</i>.\n<b>Mise en place</b> : créez le deck [[PLANET]] et le deck Méchant <i>(voir l'encart)</i>. Révélez la carte du dessus du deck Méchant. Mettez en jeu l'environnement Skrull Empire (I) <i>(stade (II) en mode expert)</i>.",
  // skrull_menace — Rise of the Skrull Empire 1B (MainScheme)
  'sk082b': "<b>Une fois révélée</b> : révélez la carte du dessus du deck [[PLANET]].",
  // skrull_menace — Andromeda Galaxy Colonization 2A (MainScheme)
  'sk083a': "<b>Une fois révélée</b> : défaussez des cartes du deck Rencontre jusqu'à défausser un sbire [[SKRULL]]. Mettez ce sbire en jeu, engagé avec le premier joueur.",
  // skrull_menace — Andromeda Galaxy Colonization 2B (MainScheme)
  'sk083b': "<b>Une fois révélée</b> : révélez la carte du dessus du deck [[PLANET]].",
  // skrull_menace — Further Empire Expansion 3A (MainScheme)
  'sk084a': "<b>Une fois révélée</b> : défaussez des cartes du deck Rencontre jusqu'à défausser un sbire [[SKRULL]]. Mettez ce sbire en jeu, engagé avec le premier joueur.",
  // skrull_menace — Further Empire Expansion 3B (MainScheme)
  'sk084b': "<b>Une fois révélée</b> : révélez la carte du dessus du deck [[PLANET]].",
  // skrull_menace — Entire Universe Domination 4A (MainScheme)
  'sk085a': "<b>Une fois révélée</b> : défaussez des cartes du deck Rencontre jusqu'à défausser un sbire [[SKRULL]]. Mettez ce sbire en jeu, engagé avec le premier joueur.",
  // skrull_menace — Entire Universe Domination 4B (MainScheme)
  'sk085b': "<b>Une fois révélée</b> : révélez la carte du dessus du deck [[PLANET]].\n<b>Si ce stade est achevé, les joueurs perdent la partie.</b>",
  // skrull_menace — Skrull Empire (I) (Environment)
  'sk086': "<i>Inciter à la rébellion</i> — <b>Action de héros</b> : choisissez : soit vous inclinez votre héros, soit vous dépensez 2 ressources de n'importe quel type → choisissez 1 environnement [[PLANET]] en jeu. Jusqu'à la fin du round, cet environnement perd le texte imprimé dans sa boîte de texte. <i>(Limite d'une fois par round par joueur.)</i>",
  // skrull_menace — Skrull Empire (II) (Environment)
  'sk087': "<b>Une fois révélée</b> : mélangez chaque carte Overthrow mise de côté dans le deck Rencontre.\n<i>Inciter à la rébellion</i> — <b>Action de héros</b> : choisissez : soit vous inclinez votre héros, soit vous dépensez 2 ressources de n'importe quel type → choisissez 1 environnement [[PLANET]] en jeu. Jusqu'à la fin du round, cet environnement perd le texte imprimé dans sa boîte de texte. <i>(Limite d'une fois par round par joueur.)</i>",
  // skrull_menace — Skrull Empire (III) (Environment)
  'sk088': "<b>Une fois révélée</b> : mélangez chaque carte Overthrow mise de côté dans le deck Rencontre.\n<i>Inciter à la rébellion</i> — <b>Action de héros</b> : choisissez : soit vous inclinez votre héros, soit vous dépensez 2 ressources de n'importe quel type → choisissez 1 environnement [[PLANET]] en jeu. Jusqu'à la fin du round, cet environnement perd le texte imprimé dans sa boîte de texte. <i>(Limite d'une fois par round par joueur.)</i>",
  // skrull_menace — Aks'Lo (Environment)
  'sk089': "Chaque sbire [[SKRULL]] gagne +2 PV.",
  // skrull_menace — Hy'lt Minor (Environment)
  'sk090': "Chaque identité gagne -1 REC.",
  // skrull_menace — Satriani (Environment)
  'sk091': "Chaque sbire [[SKRULL]] gagne Garde.",
  // skrull_menace — Skrell (Environment)
  'sk092': "Chaque sbire [[SKRULL]] gagne +1 MNG.",
  // skrull_menace — Skrullos (Environment)
  'sk093': "Chaque manigance annexe gagne l'icône de crise.",
  // skrull_menace — Tarnax II (Environment)
  'sk094': "La valeur de menace cible de la manigance principale est réduite de 1[per_hero].",
  // skrull_menace — Tarnax IV (Environment)
  'sk095': "Tant qu'une manigance annexe est en jeu, cette carte gagne l'icône d'amplification.",
  // skrull_menace — Tarnax VII (Environment)
  'sk096': "Chaque sbire [[SKRULL]] gagne +1 ATQ.",
  // skrull_menace — Zaragz'na (Environment)
  'sk097': "Chaque allié et chaque soutien entre en jeu incliné.",
  // skrull_menace — Impostor (Attachment)
  'sk098': "Considérez l'allié attaché comme un sbire [[SKRULL]] dont la boîte de texte est vide. Sa MNG est égale à son CTR imprimé et il ne subit pas de dégâts consécutifs.\n<b>Une fois révélée</b> : attachez cette carte à l'allié non-[[SKRULL]] ayant le plus de points de vie restants qui n'a pas d'exemplaire d'Impostor attaché. L'allié attaché s'engage avec son contrôleur. Sinon, le méchant manigance.",
  // skrull_menace — Intelligentsia (Minion)
  'sk099': "Chaque autre ennemi [[SKRULL]] gagne +1 MNG.\n[star] <b>Interruption forcée</b> : quand Intelligentsia est censée attaquer, elle manigance à la place.",
  // skrull_menace — Emperor's Throne (SideScheme)
  'sk100': "<b>Une fois déjouée</b> : le méchant attaque le joueur qui a déjoué cette manigance <i>(même s'il est sous forme d'alter ego)</i>. Donnez au méchant 1 carte de boost supplémentaire pour cette activation.",
  // skrull_menace — Seeking a Suitable World (SideScheme)
  'sk101': "Incitation 2.",
  // skrull_menace — A New Skrull Is Born (Treachery)
  'sk102': "<b>Une fois révélée</b> : défaussez des cartes du deck Rencontre jusqu'à défausser un sbire [[SKRULL]], et révélez-le.",
  // skrull_menace — Giving Orders (Treachery)
  'sk103': "<b>Une fois révélée</b> : chaque sbire [[SKRULL]] s'active contre le joueur avec lequel il est engagé. Si aucun sbire ne s'est activé de cette façon, cette carte gagne Renfort.",
  // skrull_menace — Long Live the Empire (Treachery)
  'sk104': "<b>Une fois révélée</b> : soignez 2 dégâts du méchant pour chaque ennemi [[SKRULL]] en jeu. Si aucun dégât n'a été soigné de cette façon, cette carte gagne Renfort.\n<hr />\n[star] <b>Boost</b> : soignez 1 dégât du méchant pour chaque ennemi [[SKRULL]] en jeu.",
  // skrull_menace — Overthrow (Treachery)
  'sk105': "<b>Une fois révélée</b> : retirez de la partie le méchant actuel et révélez la carte du dessus du deck Méchant. Ensuite, mettez Overthrow de côté, hors jeu.\n<hr />\n[star] <b>Boost</b> : attribuez-vous cette carte comme carte Rencontre face cachée.",
  // skrull_menace — Wrath of the Empire (Treachery)
  'sk106': "<b>Une fois révélée</b> : défaussez les 2 cartes du dessus du deck Rencontre pour chaque environnement [[PLANET]] en jeu. Placez 1 pion Accélération sur la manigance principale si une carte avec l'icône d'accélération a été défaussée de cette façon.\n<hr />\n[star] <b>Boost</b> : cette carte gagne +1 icône de boost pour chaque environnement [[PLANET]] en jeu.",
  // skrull_menace — Skrull Scientist (Minion)
  'sk107': "[star] <b>Boost</b> : soignez 2 dégâts du méchant, après la fin de cette activation.",
  // skrull_menace — Skrull Spy (Minion)
  'sk108': "<b>Une fois révélé</b> : défaussez 1 carte au hasard de votre main.\n[star] <b>Boost</b> : défaussez 1 carte au hasard de votre main.",
  // skrull_menace — Skrull Telepath (Minion)
  'sk109': "[star] <b>Interruption forcée</b> : quand Skrull Telepath est censé attaquer, il manigance à la place.\n[star] <b>Boost</b> : si cette activation est une manigance, révélez cette carte.",
  // skrull_menace — Skrull Warrior (Minion)
  'sk110': "Garde.\n[star] <b>Boost</b> : si cette attaque n'est pas défendue, vous êtes sonné.",
  // skrull_menace — Plotting Revenge (SideScheme)
  'sk111': "Entrave 2[per_hero].",
  // skrull_menace — Outnumbered (Treachery)
  'sk112': "<b>Une fois révélée</b> : engagez chaque sbire [[SKRULL]] en jeu. Ensuite, cherchez un sbire [[SKRULL]] dans le deck Rencontre et sa défausse, et révélez-le.\n[star] <b>Boost</b> : cette carte gagne +1 icône de boost pour chaque ennemi [[SKRULL]] en jeu <i>(jusqu'à +4)</i> pour cette activation.",
  // skrull_menace — Skrull Commander (Minion)
  'sk113': "Chaque autre sbire [[SKRULL]] gagne +1 ATQ.\n[star] <b>Boost</b> : si cette activation est une attaque, cette carte gagne +2 icônes de boost pour cette activation.",
  // skrull_menace — Skrull Soldier (Minion)
  'sk114': "<b>Une fois révélé</b> : placez 2 menaces sur chaque manigance annexe en jeu.\n[star] <b>Boost</b> : défaussez les 2 cartes du dessus de votre deck.",
  // skrull_menace — Hijacked (SideScheme)
  'sk115': "Entrave 1[per_hero].\n<b>Une fois révélée</b> : cherchez un allié dans votre deck, votre défausse et votre main, et placez-le sous cette manigance.\n<b>Une fois déjouée</b> : mettez en jeu l'allié placé sous cette manigance, sous le contrôle de son propriétaire.\n[star] <b>Boost</b> : révélez cette carte.",
  // skrull_menace — Skrull Assault (Treachery)
  'sk116': "<b>Une fois révélée</b> : chaque sbire [[SKRULL]] attaque le héros avec lequel il est engagé. Si aucune attaque n'a été effectuée de cette façon, cette carte gagne Renfort.\n[star] <b>Boost</b> : cette carte gagne +1 icône de boost pour chaque ennemi [[SKRULL]] en jeu <i>(jusqu'à +4)</i> pour cette activation.",
  // skrull_menace — Lyja (Hero)
  'sk037a': "<i>Espionne skrull</i> — <b>Action</b> : dépensez jusqu'à 1[per_hero] ressources de n'importe quel type → cherchez une carte [[TREACHERY]] dans le deck Rencontre pour chaque ressource dépensée de cette façon, mélangez le deck Rencontre et placez ces cartes sur le dessus du deck Rencontre dans l'ordre de votre choix.",
  // skrull_menace — Laura Green (AlterEgo)
  'sk037b': "<i>Jouer le jeu</i> — <b>Action</b> : cherchez une carte [[TREACHERY]] dans votre deck, mélangez votre deck et placez cette carte sur le dessus de votre deck. <i>(Limite d'une fois par round.)</i>",
  // skrull_menace — Human Torch (Ally)
  'sk038': "<b>Réponse</b> : après que Human Torch a quitté le jeu, cherchez une carte [[TREACHERY]] dans le deck Rencontre, mélangez le deck Rencontre et placez cette carte sur le dessus du deck Rencontre.",
  // skrull_menace — Faking Death (Event)
  'sk039': "<b>Action de héros</b> : mélangez cette carte dans le deck Rencontre.\n<b>Une fois révélée</b> : choisissez : soit vous sonnez un ennemi, soit vous le désorientez.\n<hr />\n[star] <b>Boost</b> : l'ennemi qui s'active gagne -2 MNG et -2 ATQ pour cette activation.",
  // skrull_menace — Feign Loyalty (Event)
  'sk040': "<b>Action de héros</b> : mélangez cette carte dans le deck Rencontre.\n<b>Une fois révélée</b> : défaussez un attachement en jeu qui a le mot-clé Utilisations ou le texte \"<b>Action de héros</b>\" ou \"<b>Réponse de héros</b>\".\n<hr />\n[star] <b>Boost</b> : piochez 2 cartes.",
  // skrull_menace — Hero Appearance (Event)
  'sk041': "<b>Action de héros</b> : mélangez cette carte dans le deck Rencontre.\n<b>Une fois révélée</b> : le joueur Lyja inflige un total de 4 dégâts répartis parmi les ennemis en jeu.\n<hr />\n[star] <b>Boost</b> : le joueur Lyja inflige 3 dégâts à un ennemi.",
  // skrull_menace — Posing as a Civilian (Event)
  'sk042': "<b>Action de héros</b> : mélangez cette carte dans le deck Rencontre.\n<b>Une fois révélée</b> : le joueur Lyja retire un total de 3 menaces parmi les manigances en jeu.\n<hr />\n[star] <b>Boost</b> : le joueur Lyja retire 2 menaces d'une manigance.",
  // skrull_menace — New York Bookstore (Support)
  'sk043': "Laura Green gagne +2 REC.\n<b>Réponse d'alter ego</b> : après avoir effectué une récupération de base, piochez 1 carte.",
  // skrull_menace — Lazerfist (Upgrade)
  'sk044': "Lyja gagne +1 ATQ.\n<b>Ressource de héros</b> : inclinez Lazerfist → générez une ressource [energy].",
  // skrull_menace — Ministerial Tiara (Upgrade)
  'sk045': "<b>Interruption</b> : quand une carte de boost est retournée face visible, si cette carte a une icône d'étoile ([star]) dans son champ de boost, inclinez cette carte → piochez 1 carte.",
  // skrull_menace — Mole (Upgrade)
  'sk046': "<b>Interruption de héros</b> : quand une carte [[TREACHERY]] est défaussée du dessus du deck Rencontre, inclinez Mole → résolvez la capacité \"<b>Une fois révélée</b>\" de cette carte.",
  // skrull_menace — Shapeshifter (Upgrade)
  'sk047': "Lyja gagne +1 CTR.\n<b>Réponse de héros</b> : après avoir joué un événement [[TREACHERY]], inclinez Shapeshifter → redressez Lyja.",
  // skrull_menace — The Thing (Ally)
  'sk049': "Ténacité.\n<b>Action</b> : défaussez une carte d'état Tenace de The Thing et choisissez jusqu'à 2 ennemis → infligez 2 dégâts à chacun d'eux.",
  // skrull_menace — Going Ballistic (Event)
  'sk052': "<b>Action de héros</b> <i>(attaque)</i> : défaussez votre main. Infligez 2 dégâts à un ennemi (jusqu'à un maximum de 6) pour chaque carte défaussée de cette façon.",
  // skrull_menace — Hit the Weak Spot (Event)
  'sk053': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un sbire pour chaque icône ([star] <i>et</i> [boost]) dans le champ de boost de ce sbire. Cette attaque gagne Perçant.",
  // skrull_menace — Invisible Woman (Ally)
  'sk056': "Invisible Woman subit +1 dégât consécutif pour chaque jeton Révélation sur la cible de son pouvoir de base.\n<b>Réponse forcée</b> : après qu'Invisible Woman a utilisé un pouvoir de base, placez 1 jeton Révélation sur la cible de ce pouvoir.",
  // skrull_menace — Mister Fantastic (Ally)
  'sk057': "<b>Ressource</b> : inclinez Mister Fantastic et infligez-lui 1 dégât → générez une ressource [mental].",
  // skrull_menace — Laser Tag (Event)
  'sk058': "En Équipe (Human Torch et Lyja). 1 max par deck.\n<b>Action de héros</b> : redressez Human Torch, Lyja et chaque amélioration [[SUPERPOWER]] que vous contrôlez.",
  // skrull_menace — Baxter Building (Support)
  'sk062': "Réduisez de 1 le coût de cette carte si vous contrôlez un personnage [[FANTASTIC FOUR]].\n<b>Ressource</b> : inclinez Baxter Building → générez une ressource [wild] pour n'importe quel joueur.",
  // skrull_menace — Fantasti-Car (Support)
  'sk063': "<b>Réponse</b> : après que Fantasti-Car est entrée en jeu, redressez une carte [[FANTASTIC FOUR]].\n<b>Action d'alter ego</b> : inclinez Fantasti-Car → choisissez un joueur. Ce joueur peut mélanger 1 carte de sa défausse dans son deck.",
  // skrull_menace — Fantastic Four Member (Upgrade)
  'sk064': "Ne jouez cette carte que si votre identité a le trait [[FANTASTIC FOUR]].\nAttachez-la à un personnage allié. 1 max par personnage.\nLe personnage attaché gagne +1 point de vie et le trait [[FANTASTIC FOUR]].",
  // skrull_menace — Untrustworthiness (Obligation)
  'sk065': "<b><i>Donnez cette carte au joueur Laura Green.</i></b>\n<b>Interruption forcée</b> : quand une capacité \"<b>Boost</b>\" ou \"<b>Une fois révélée</b>\" d'une carte [[TREACHERY]] est censée être résolue, annulez cette capacité. Ensuite, attribuez-vous 1 carte Rencontre face cachée.\n<b>Action d'alter ego</b> : inclinez Laura Green → défaussez Untrustworthiness.",
  // skrull_menace — Paibok (Minion)
  'sk066': "Ténacité.\n[star] Paibok gagne +1 MNG et +1 ATQ pour chaque carte [[TREACHERY]] attachée à lui.\n<b>Interruption forcée</b> : quand une carte [[TREACHERY]] est censée être défaussée, attachez-la face cachée à Paibok à la place.\n<i>(Sbire némésis de Lyja.)</i>",
  // skrull_menace — Punish the Defector (SideScheme)
  'sk067': "<i>Lors d'un combat entre les Quatre Fantastiques et son ancien amant Paibok, Lyja, qui éprouvait encore des sentiments pour la Torche, a de nouveau trahi Paibok pour se ranger du côté des Quatre Fantastiques.</i>\n<b>Une fois révélée</b> : cherchez une carte [[TREACHERY]] dans le deck Rencontre et défaussez-la. Mélangez le deck Rencontre.",
  // skrull_menace — "It's a Stinkin' Skrull!" (Treachery)
  'sk068': "<b>Une fois révélée</b> : cherchez une carte [[TREACHERY]] dans le deck Rencontre et défaussez-la. <i>(Mélangez.)</i> Si aucune carte [[TREACHERY]] n'a été défaussée de cette façon, cette carte gagne Renfort.",
  // skrull_menace — Truth Revealed (Treachery)
  'sk069': "<b>Une fois révélée</b> : cherchez dans votre deck toutes les cartes spécifiques à une identité, mélangez votre deck et placez ces cartes sous votre deck dans l'ordre de votre choix.",
  // skrull_menace — Super-Skrull I (Villain)
  'sk117': "<b>Réponse forcée</b> : après avoir résolu l'étape 2 de la phase du Méchant, mélangez chaque attachement [[SUPERPOWER]] en jeu dans le deck [[SUPERPOWER]] et révélez la carte du dessus du deck [[SUPERPOWER]].",
  // skrull_menace — Super-Skrull II (Villain)
  'sk118': "<b>Réponse forcée</b> : après avoir résolu l'étape 2 de la phase du Méchant, mélangez chaque attachement [[SUPERPOWER]] en jeu dans le deck [[SUPERPOWER]] et révélez les 2 cartes du dessus du deck [[SUPERPOWER]].",
  // skrull_menace — Super-Skrull III (Villain)
  'sk119': "<b>Réponse forcée</b> : après avoir résolu l'étape 2 de la phase du Méchant, mélangez chaque attachement [[SUPERPOWER]] en jeu dans le deck [[SUPERPOWER]] et révélez les 2 cartes du dessus du deck [[SUPERPOWER]].",
  // skrull_menace — Searching for the Heir 1A (MainScheme)
  'sk120a': "<b>Contenu</b> : Super-Skrull (I) et Super-Skrull (II) <i>(Super-Skrull (III) en mode expert)</i>. Les sets de rencontre Super-Skrull et Standard. Deux sets de rencontre modulaires <i>(Army of Skrulls et Kree-Skrull War)</i>.\n<b>Mise en place</b> : mélangez chaque attachement [[SUPERPOWER]] pour former le deck [[SUPERPOWER]] et placez-le à côté du deck Rencontre.",
  // skrull_menace — Searching for the Heir 1B (MainScheme)
  'sk120b': "<b>Une fois révélée</b> : révélez la carte du dessus du deck [[SUPERPOWER]].",
  // skrull_menace — Heir to the Throne 2A (MainScheme)
  'sk121a': "<b>Une fois révélée</b> : si Lord Kl'rt est en jeu, attribuez 1 carte Rencontre face cachée à chaque joueur. Sinon, cherchez Lord Kl'rt dans le deck Rencontre et la pile de défausse Rencontre et attachez-le à Super-Skrull. Mélangez le deck Rencontre.",
  // skrull_menace — Heir to the Throne 2B (MainScheme)
  'sk121b': "<b>Une fois révélée</b> : révélez la carte du dessus du deck [[SUPERPOWER]].\n<b>Si ce stade est achevé, les joueurs perdent la partie.</b>",
  // skrull_menace — Flexibility (Attachment)
  'sk122': "Attachez cette carte à Super-Skrull.\nSuper-Skrull gagne Robuste et ses attaques gagnent Distance.",
  // skrull_menace — Invisibility (Attachment)
  'sk123': "Attachez cette carte à Super-Skrull.\nEn tant que coût supplémentaire pour attaquer Super-Skrull, vous devez dépenser 1 ressource de n'importe quel type.",
  // skrull_menace — Pyrokinesis (Attachment)
  'sk124': "Attachez cette carte à Super-Skrull.\n<b>Réponse forcée</b> : après qu'un personnage ami a déjoué la manigance principale, infligez-lui 1 dégât.\n[star] Les attaques de Super-Skrull gagnent Perçant.",
  // skrull_menace — Rock Mimicry (Attachment)
  'sk125': "Attachez cette carte à Super-Skrull.\n[star] <b>Interruption forcée</b> : quand Super-Skrull attaque, donnez-lui 1 carte de boost supplémentaire pour cette activation.\n[star] Les attaques de Super-Skrull gagnent Déferlement.",
  // skrull_menace — Invisible Forcefield (Attachment)
  'sk126': "Attachez cette carte à l'ennemi avec le plus de points de vie imprimés et qui n'a pas déjà un Invisible Forcefield attaché. Si vous ne pouvez pas, cette carte gagne Renfort.\n<b>Interruption forcée</b> : quand le personnage attaché est censé subir n'importe quelle quantité de dégâts, placez-les sur cette carte à la place. Ensuite, s'il y a au moins 5 dégâts ici, défaussez cette carte.",
  // skrull_menace — Lord Kl'rt (Attachment)
  'sk127': "Attachez cette carte à Super-Skrull.\n<b>Action de héros</b> : révélez la carte du dessus du deck [[SUPERPOWER]] → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // skrull_menace — Mt'nox (Minion)
  'sk128': "[star] <b>Réponse forcée</b> : après que Mt'nox a effectué une attaque non défendue contre vous, défaussez la carte du dessus de votre deck. Si cette carte a comme ressource imprimée :\n[physical] - Donnez une carte d'état Tenace au méchant.\n[energy] - Vous êtes sonné.\n[mental] - Vous êtes désorienté.\n[wild] - Effectuez toutes les options ci-dessus.",
  // skrull_menace — Praxagora (Minion)
  'sk129': "[star] Les attaques de Praxagora gagnent Déferlement.",
  // skrull_menace — R'kin (Minion)
  'sk130': "<b>Une fois vaincu</b> : défaussez des cartes du dessus du deck Rencontre jusqu'à défausser un attachement. Révélez cette carte.",
  // skrull_menace — Galactic Council Membership (SideScheme)
  'sk131': "<b>Réponse forcée</b> : après qu'un joueur a attaqué Super-Skrull, placez 1 menace sur la manigance principale.",
  // skrull_menace — Skrull Warlords (SideScheme)
  'sk132': "<b>Réponse forcée</b> : après qu'une carte est entrée en jeu sous le contrôle d'un joueur, donnez au méchant 1 carte de boost face cachée.",
  // skrull_menace — Hypnotic Gaze (Treachery)
  'sk133': "<b>Une fois révélée</b> : défaussez les 2 cartes du dessus de votre deck. Pour chaque ressource [physical] défaussée de cette façon, sonnez un personnage que vous contrôlez ; pour chaque ressource [mental] défaussée de cette façon, désorientez un personnage que vous contrôlez.",
  // skrull_menace — Power Multiplying (Treachery)
  'sk134': "<b>Une fois révélée</b> : révélez la carte du dessus du deck [[SUPERPOWER]]. Si vous ne pouvez pas, cette carte gagne Renfort.\n<hr />\n[star] <b>Boost</b> : cette carte gagne +1 icône de boost ([boost]) pour chaque attachement [[SUPERPOWER]] attaché à Super-Skrull.",
  // skrull_menace — Villain's Versatility (Treachery)
  'sk135': "<b>Une fois révélée</b> : si Super-Skrull a l'attachement [[SUPERPOWER]] suivant d'attaché :\n• Pyrokinesis - Subissez 3 dégâts indirects.\n• Rock Mimicry - Donnez une carte d'état Tenace à Super-Skrull.\n• Flexibility - Défaussez 1 carte de votre main.\n• Invisibility - Placez 2 menaces sur la manigance principale.",
  // skrull_menace — Bel-Dann (Minion)
  'sk136': "<b>Une fois révélé</b> : cherchez Raksor dans le deck Rencontre et la pile de défausse Rencontre et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Raksor (Minion)
  'sk137': "<b>Une fois révélé</b> : cherchez Bel-Dann dans le deck Rencontre et la pile de défausse Rencontre et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Earth Involvement (SideScheme)
  'sk138': "Permanent. Mise en place.\nTant qu'il y a au moins 1 menace ici, cette carte gagne une icône de crise ([crisis]).\n<b>Réponse forcée</b> : après qu'une carte appartenant au set de rencontre Kree-Skrull War est révélée, placez 2 menaces ici.",
  // skrull_menace — Imperial Kree Army (Treachery)
  'sk139': "<b>Une fois révélée</b> : défaussez la carte du dessus du deck Rencontre. Infligez 1 dégât à chaque personnage que vous contrôlez pour chaque icône de boost ([boost]) défaussée de cette façon.\n<hr />\n[star] <b>Boost</b> : placez 2 menaces sur Earth Involvement.",
  // skrull_menace — Skrull Imperial Fleet (Treachery)
  'sk140': "<b>Une fois révélée</b> : défaussez la carte du dessus du deck Rencontre. Placez 1 menace sur chaque manigance en jeu pour chaque icône de boost ([boost]) défaussée de cette façon.\n<hr />\n[star] <b>Boost</b> : placez 2 menaces sur Earth Involvement.",
  // skrull_menace — Paibok (Villain, stade I)
  'sk141': "Ténacité.\nTant que le nombre de cartes [[POWER SKRULL]] attachées à Paibok est égal ou inférieur au nombre de jetons de maîtrise sur lui, les cartes [[POWER SKRULL]] ne peuvent pas être défaussées.",
  // skrull_menace — Paibok (Villain, stade II)
  'sk142': "Ténacité.\nTant que le nombre de cartes [[POWER SKRULL]] attachées à Paibok est égal ou inférieur au nombre de jetons de maîtrise sur lui, les cartes [[POWER SKRULL]] ne peuvent pas être défaussées.\n<b>Une fois révélé</b> : cherchez une carte [[POWER SKRULL]] dans le deck Rencontre ou la pile de défausse rencontre et révélez-la.",
  // skrull_menace — Paibok (Villain, stade III)
  'sk143': "Ténacité.\nTant que le nombre de cartes [[POWER SKRULL]] attachées à Paibok est égal ou inférieur au nombre de jetons de maîtrise sur lui, les cartes [[POWER SKRULL]] ne peuvent pas être défaussées.\n<b>Une fois révélé</b> : cherchez une carte [[POWER SKRULL]] dans le deck Rencontre ou la pile de défausse rencontre et révélez-la.",
  // skrull_menace — Power Skrull Engineering (MainScheme, 1A)
  'sk144a': "<b>Contenu</b> : Paibok (I) et Paibok (II) <i>(Paibok (II) et Paibok (III) en mode expert)</i>. Les sets de rencontre Paibok et Standard. Un set de rencontre modulaire <i>(New Revengers)</i>.\n<b>Mise en place</b> : placez 1 jeton de maîtrise sur Paibok.",
  // skrull_menace — Power Skrull Engineering (MainScheme, 1B)
  'sk144b': "<b>Une fois révélée</b> : défaussez des cartes du deck Rencontre jusqu'à ce qu'une carte [[POWER SKRULL]] soit défaussée. Révélez cette carte. Mélangez la pile de défausse rencontre dans le deck Rencontre.",
  // skrull_menace — Mastering Superpowers (MainScheme, 2A)
  'sk145a': "<b>Une fois révélée</b> : placez 1 jeton de maîtrise sur Paibok. Ensuite, si Captain Paibok est en jeu, résolvez sa capacité \"<b>Boost</b>\". Sinon, cherchez Captain Paibok dans le deck Rencontre ou la pile de défausse rencontre et attachez-le à Paibok. Mélangez le deck Rencontre.",
  // skrull_menace — Mastering Superpowers (MainScheme, 2B)
  'sk145b': "[star] <b>Interruption forcée</b> : quand ce stade est censé être achevé, placez 1 jeton de maîtrise sur Paibok et retirez-en toutes les menaces à la place. Ensuite, défaussez des cartes du deck Rencontre jusqu'à ce qu'une carte [[POWER SKRULL]] soit défaussée. Révélez cette carte.\n<b>Quand la phase des Joueurs se termine, si les 4 cartes [[POWER SKRULL]] sont attachées à Paibok, les joueurs perdent la partie.</b>",
  // skrull_menace — Captain Paibok (Attachment)
  'sk146': "Attachez cette carte à Paibok.\n<b>Action de héros</b> : résolvez la capacité \"<b>Boost</b>\" de chaque attachement en jeu qui appartient au set de rencontre Paibok → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : soignez 2 dégâts de Paibok.",
  // skrull_menace — Distracted (Attachment)
  'sk147': "Attachez cette carte à votre identité.\n<b>Interruption forcée</b> : quand vous contrez, diminuez de 1 la quantité de menaces que ce contre retire.\n<b>Action de héros</b> : dépensez les ressources suivantes : [mental][mental] → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : placez 1 menace sur la manigance principale.",
  // skrull_menace — Electricity Projection (Attachment)
  'sk148': "Attachez cette carte à Paibok.\nPaibok gagne Riposte 1.\n<b>Action de héros</b> : dépensez les ressources suivantes : [mental][physical] → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : sonnez un personnage que vous contrôlez.",
  // skrull_menace — Hypnotized (Attachment)
  'sk149': "Attachez cette carte à votre identité.\nEn tant que coût supplémentaire pour changer de forme, vous devez dépenser 1 ressource de n'importe quel type.\n<b>Action de héros</b> : dépensez les ressources suivantes : [energy][energy] → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : défaussez 1 carte de votre main.",
  // skrull_menace — Ice Control (Attachment)
  'sk150': "Attachez cette carte à Paibok.\n[star] <b>Réponse forcée</b> : après que Paibok vous a attaqué, inclinez un personnage que vous contrôlez.\n<b>Action de héros</b> : dépensez 3 ressources de n'importe quel type → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : inclinez un personnage que vous contrôlez.",
  // skrull_menace — Metallic Skin (Attachment)
  'sk151': "Attachez cette carte à Paibok.\n<b>Réponse forcée</b> : après que Paibok a subi des dégâts, donnez-lui une carte d'état Tenace.\n<b>Action de héros</b> : dépensez les ressources suivantes : [energy][mental] → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : donnez une carte d'état Tenace à Paibok.",
  // skrull_menace — Shapeshifting (Attachment)
  'sk152': "Attachez cette carte à Paibok.\nPaibok gagne Robuste et le trait [[AERIAL]].\n<b>Action de héros</b> : dépensez les ressources suivantes : [energy][physical] → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : désorientez un personnage que vous contrôlez.",
  // skrull_menace — Trapped in Ice (Attachment)
  'sk153': "Attachez cette carte à votre identité.\n<b>Interruption forcée</b> : quand vous attaquez, diminuez de 1 la quantité de dégâts que cette attaque inflige.\n<b>Action de héros</b> : dépensez les ressources suivantes : [physical][physical] → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : subissez 1 dégât.",
  // skrull_menace — Devos the Devastator (Minion)
  'sk154': "<b>Réponse forcée</b> : après qu'une carte d'état est placée sur un personnage allié, Devos the Devastator s'active contre le joueur qui contrôle ce personnage.",
  // skrull_menace — General Kalamari (Minion)
  'sk155': "<b>Une fois vaincu</b> : le joueur qui a vaincu General Kalamari résout la capacité \"<b>Boost</b>\" de chaque attachement en jeu qui appartient au set de rencontre Paibok.",
  // skrull_menace — Galactic Ambassador (SideScheme)
  'sk156': "<b>Une fois révélée</b> : placez 2 menaces supplémentaires ici pour chaque personnage allié qui a une carte d'état.",
  // skrull_menace — Settling Scores (SideScheme)
  'sk157': "Entrave 2[per_hero].\nRésolvez la capacité \"<b>Boost</b>\" de chaque carte de boost 1 fois supplémentaire.\n<b>Une fois révélée</b> : mélangez chaque carte [[POWER SKRULL]] de la pile de défausse rencontre dans le deck Rencontre.",
  // skrull_menace — Council Manipulation (Treachery)
  'sk158': "<b>Une fois révélée</b> : Paibok manigance. Si vous êtes sonné ou désorienté, cette carte gagne Renfort.",
  // skrull_menace — Getting Ruthless (Treachery)
  'sk159': "<b>Une fois révélée (alter ego)</b> : résolvez la capacité \"<b>Boost</b>\" de chaque attachement en jeu qui appartient au set de rencontre Paibok.\n<b>Une fois révélée (héros)</b> : Paibok vous attaque. Donnez-lui 1 carte de boost supplémentaire si vous êtes sonné ou désorienté.",
  // skrull_menace — Power Demonstration (Treachery)
  'sk160': "<b>Une fois révélée</b> : résolvez la capacité \"<b>Boost</b>\" de chaque attachement en jeu qui appartient au set de rencontre Paibok.",
  // skrull_menace — O.M.N.I.T.R.O.N.I.C.U.S. (Environment)
  'sk161': "Chaque sbire [[REVENGER]] gagne Vilenie.\n<b>Action de héros</b> : s'il n'y a aucun ennemi [[REVENGER]] en jeu, dépensez les ressources suivantes : [energy][energy] → défaussez cette carte.",
  // skrull_menace — Angar the Screamer (Minion)
  'sk162': "[star] Les attaques d'Angar the Screamer gagnent Distance.\n<b>Interruption forcée</b> : quand Angar the Screamer vous attaque, résolvez également son attaque contre chaque autre héros.",
  // skrull_menace — Asti the All-Seeing (Minion)
  'sk163': "<b>Interruption forcée</b> : quand Asti the All-Seeing subit n'importe quelle quantité de dégâts, placez 1 jeton d'absorption sur lui.\n<b>Une fois vaincu</b> : répartissez 2 dégâts indirects parmi les joueurs pour chaque jeton d'absorption sur Asti the All-Seeing.",
  // skrull_menace — Skar (Minion)
  'sk164': "[star] Les attaques de Skar gagnent Déferlement.\n<b>Une fois révélé</b> : inclinez un personnage que vous contrôlez.",
  // skrull_menace — The Maker (Minion)
  'sk165': "The Maker ne peut pas subir de dégâts tant qu'un autre ennemi [[REVENGER]] est en jeu.\n<b>Une fois révélé</b> : cherchez la manigance annexe The Revenge Time dans le deck Rencontre ou la pile de défausse rencontre et révélez-la.",
  // skrull_menace — Vermin (Minion)
  'sk166': "[star] Les attaques de Vermin infligent des dégâts indirects.\n<hr />\n[star] <b>Boost</b> : si cette activation est une attaque, elle inflige des dégâts indirects.",
  // skrull_menace — White Tiger (Minion)
  'sk167': "Coup Rapide. <i>(Après que ce sbire s'est engagé avec votre héros, il vous attaque.)</i>\n<b>Une fois vaincu</b> : donnez 1 carte de boost face cachée au méchant.",
  // skrull_menace — The Revenge Time (SideScheme)
  'sk168': "Le méchant gagne le trait [[REVENGER]].\n<b>Une fois révélée</b> : placez 1 menace supplémentaire ici pour chaque ennemi [[REVENGER]] en jeu.",
  // skrull_menace — Forming the Revengers (Treachery)
  'sk169': "<b>Une fois révélée</b> : défaussez des cartes du dessus du deck Rencontre jusqu'à ce qu'une carte avec le trait [[REVENGER]] soit défaussée. Révélez cette carte.",
  // skrull_menace — Spider-Woman (Veranke) (Villain, Secret Invasion)
  'sk189a': "Spider-Woman ne peut pas subir de dégâts.\n[star] <b>Réponse forcée</b> : après que Spider-Woman vous a attaqué, placez 1 jeton de soupçon sur \"Who Do You Trust?\".\n<i>You are a Skrull!</i> — <b>Action de héros</b> : inclinez un héros et dépensez 1[per_hero] ressources de n'importe quel type → retournez Spider-Woman. <i>(Les joueurs peuvent payer les coûts de cette capacité en groupe.)</i>",
  // skrull_menace — Queen Veranke (Villain, Secret Invasion)
  'sk189b': "<b>Réponse forcée</b> : après la fin de la phase du Méchant, si un joueur est sous forme d'alter ego, retournez Queen Veranke.\n<b>Une fois vaincue</b> : retirez tous les jetons de soupçon de \"Who Do You Trust?\".",
  // skrull_menace — Spider-Woman (Veranke) (Villain, Secret Invasion)
  'sk190a': "Spider-Woman ne peut pas subir de dégâts.\n[star] <b>Réponse forcée</b> : après que Spider-Woman vous a attaqué, placez 1 jeton de soupçon sur \"Who Do You Trust?\".\n<i>You are a Skrull!</i> — <b>Action de héros</b> : inclinez un héros et dépensez 1[per_hero] ressources de n'importe quel type → retournez Spider-Woman. <i>(Les joueurs peuvent payer les coûts de cette capacité en groupe.)</i>",
  // skrull_menace — Queen Veranke (Villain, Secret Invasion)
  'sk190b': "<b>Réponse forcée</b> : après la fin de la phase du Méchant, si un joueur est sous forme d'alter ego, retournez Queen Veranke.\n<b>Une fois vaincue</b> : retirez tous les jetons de soupçon de \"Who Do You Trust?\".",
  // skrull_menace — Spider-Woman (Veranke) (Villain, Secret Invasion)
  'sk191a': "Spider-Woman ne peut pas subir de dégâts.\n[star] <b>Réponse forcée</b> : après que Spider-Woman vous a attaqué, placez 1 jeton de soupçon sur \"Who Do You Trust?\".\n<i>You are a Skrull!</i> — <b>Action de héros</b> : inclinez un héros et dépensez 1[per_hero] ressources de n'importe quel type → retournez Spider-Woman. <i>(Les joueurs peuvent payer les coûts de cette capacité en groupe.)</i>",
  // skrull_menace — Queen Veranke (Villain, Secret Invasion)
  'sk191b': "<b>Réponse forcée</b> : après la fin de la phase du Méchant, si un joueur est sous forme d'alter ego, retournez Queen Veranke. Sinon, défaussez la première carte du deck Rencontre ; si c'est une traîtrise, retournez Queen Veranke.",
  // skrull_menace — The Infiltration Has Begun (MainScheme, Secret Invasion)
  'sk192a': "<b>Contenu</b> : Spider-Woman (I) et Spider-Woman (II) <i>(Spider-Woman (II) et Spider-Woman (III) en mode expert)</i>. Les sets de rencontre Secret Invasion et Standard. Un set de rencontre modulaire <i>(Army of Skrulls)</i>.\n<b>Mise en place</b> : créez le deck [[IMPOSTOR]] et placez-le à côté du deck Rencontre <i>(voir l'encart)</i>. Mettez en jeu l'environnement \"Who Do You Trust?\".",
  // skrull_menace — The Infiltration Has Begun (MainScheme, Secret Invasion)
  'sk192b': "[star] Placez 1 menace supplémentaire ici pour chaque ennemi [[SKRULL]] en jeu et chaque allié [[IMPOSTOR]] en jeu.\n<b>Réponse forcée</b> : après la fin de votre tour, s'il y a moins de 2[per_hero] jetons de soupçon sur \"Who Do You Trust?\", mettez en jeu sous votre contrôle un allié [[CAMOUFLAGED]] pris au hasard dans le deck [[IMPOSTOR]].",
  // skrull_menace — The Skrull Invasion (MainScheme, Secret Invasion)
  'sk193a': "<b>Une fois révélée</b> : si Mistrust and Paranoia est en jeu, retirez 2[per_hero] jetons de soupçon de \"Who Do You Trust?\". Sinon, cherchez Mistrust and Paranoia et révélez-le.",
  // skrull_menace — The Skrull Invasion (MainScheme, Secret Invasion)
  'sk193b': "X est égal à deux fois le nombre d'ennemis [[SKRULL]] en jeu.\n<b>Réponse forcée</b> : après la fin de votre tour, s'il y a moins de 2[per_hero] jetons de soupçon sur \"Who Do You Trust?\", mettez en jeu, engagé avec vous, un sbire [[REVEALED]] pris au hasard dans le deck [[IMPOSTOR]].\n<b>Si ce stade est achevé, les joueurs perdent la partie.</b>",
  // skrull_menace — "Who Do You Trust?" (Environment, Secret Invasion)
  'sk194': "<b>Interruption forcée</b> : quand n'importe quelle quantité de menaces est placée sur la manigance principale, retirez d'ici une quantité égale de jetons de soupçon.\n<b>Interruption forcée</b> : quand n'importe quelle quantité de menaces est retirée de la manigance principale, placez ici une quantité égale de jetons de soupçon.",
  // skrull_menace — Impostor (Attachment, Secret Invasion)
  'sk195': "Considérez l'allié attaché comme un sbire [[SKRULL]] dont la boîte de texte est vide. Sa MNG est égale à son CTR imprimé et il ne subit pas de dégâts consécutifs.\n<b>Une fois révélée</b> : attachez cette carte à l'allié non-[[SKRULL]] ayant le plus de points de vie restants qui n'a pas d'exemplaire d'Impostor attaché. L'allié attaché s'engage avec son contrôleur. Sinon, le méchant manigance.",
  // skrull_menace — Super-Skrull Enhancement (Attachment, Secret Invasion)
  'sk196': "Attachez cette carte au sbire [[SKRULL]] ayant le plus de points de vie restants qui n'a pas d'autre Super-Skrull Enhancement attaché. Si vous ne pouvez pas, choisissez un allié [[CAMOUFLAGED]], retournez-le et attachez-lui cette carte. Sinon, cette carte gagne Renfort.\nLe sbire attaché gagne 2 points de vie.\n<hr />\n[star] <b>Boost</b> : révélez cette carte, après la fin de cette activation.",
  // skrull_menace — Super-Skrull Enhancement (Attachment, Secret Invasion)
  'sk197': "Attachez cette carte au sbire [[SKRULL]] ayant le plus de points de vie restants qui n'a pas d'autre Super-Skrull Enhancement attaché. Si vous ne pouvez pas, choisissez un allié [[CAMOUFLAGED]], retournez-le et attachez-lui cette carte. Sinon, cette carte gagne Renfort.\n<hr />\n[star] <b>Boost</b> : révélez cette carte, après la fin de cette activation.",
  // skrull_menace — Super-Skrull Enhancement (Attachment, Secret Invasion)
  'sk198': "Attachez cette carte au sbire [[SKRULL]] ayant le plus de points de vie restants qui n'a pas d'autre Super-Skrull Enhancement attaché. Si vous ne pouvez pas, choisissez un allié [[CAMOUFLAGED]], retournez-le et attachez-lui cette carte. Sinon, cette carte gagne Renfort.\nLe sbire attaché gagne Riposte 1.\n<hr />\n[star] <b>Boost</b> : révélez cette carte, après la fin de cette activation.",
  // skrull_menace — Chaos on the Battlefield (SideScheme, Secret Invasion)
  'sk199': "Incitation 2.\n<b>Une fois révélée</b> : placez ici X menaces supplémentaires, X étant égal à la MNG totale de tous les personnages [[IMPOSTOR]] en jeu.",
  // skrull_menace — Fulfill the Prophecy (SideScheme, Secret Invasion)
  'sk200': "Entrave 1[per_hero].\nChaque sbire [[SKRULL]] gagne Garde et Patrouille.",
  // skrull_menace — Mistrust and Paranoia (SideScheme, Secret Invasion)
  'sk201': "Les joueurs ne peuvent pas attaquer les sbires engagés avec d'autres joueurs, ni défendre contre eux. Les joueurs ne peuvent pas payer en groupe les coûts d'une carte ou d'une capacité.\n<b>Une fois révélée</b> : placez ici 1 menace supplémentaire pour chaque personnage allié en jeu.",
  // skrull_menace — Arrival of Impostors (Treachery, Secret Invasion)
  'sk202': "<b>Une fois révélée</b> : chaque joueur met en jeu sous son contrôle un allié [[CAMOUFLAGED]] pris au hasard dans le deck [[IMPOSTOR]].\n<hr />\n[star] <b>Boost</b> : mettez en jeu sous votre contrôle un allié [[CAMOUFLAGED]] pris au hasard dans le deck [[IMPOSTOR]].",
  // skrull_menace — Camouflage (Treachery, Secret Invasion)
  'sk203': "<b>Une fois révélée</b> (Queen Veranke) : retournez Queen Veranke. Retirez 3 jetons de soupçon de \"Who Do You Trust?\".\n<b>Une fois révélée</b> (Spider-Woman) : Spider-Woman manigance.\n<hr />\n[star] <b>Boost</b> : retournez Queen Veranke, après la fin de cette activation.",
  // skrull_menace — Glory to the Skrull Empire (Treachery, Secret Invasion)
  'sk204': "<b>Une fois révélée</b> : donnez une carte d'état Tenace au méchant et à chaque sbire [[SKRULL]] engagé avec vous. Si le méchant a déjà une carte d'état Tenace, cette carte gagne Renfort.\n<hr />\n[star] <b>Boost</b> : donnez une carte d'état Tenace au méchant.",
  // skrull_menace — Infiltration Ritual (Treachery, Secret Invasion)
  'sk205': "<b>Une fois révélée</b> : mettez en jeu sous le contrôle de n'importe quel joueur un allié [[CAMOUFLAGED]] pris au hasard dans le deck [[IMPOSTOR]]. Si vous ne pouvez pas, cette carte gagne Renfort.\n<hr />\n[star] <b>Boost</b> : retirez 3 jetons de soupçon de \"Who Do You Trust?\".",
  // skrull_menace — Invasion Fleet (Treachery, Secret Invasion)
  'sk206': "<b>Une fois révélée</b> : chaque joueur met en jeu, engagé avec lui, un sbire [[REVEALED]] pris au hasard dans le deck [[IMPOSTOR]].\n<hr />\n[star] <b>Boost</b> : mettez en jeu, engagé avec vous, un sbire [[REVEALED]] pris au hasard dans le deck [[IMPOSTOR]].",
  // skrull_menace — Revelation (Treachery, Secret Invasion)
  'sk207': "<b>Une fois révélée</b> : retournez l'allié [[CAMOUFLAGED]] ayant le plus de points de vie restants. Si vous ne pouvez pas, mettez en jeu, engagé avec vous, un sbire [[REVEALED]] pris au hasard dans le deck [[IMPOSTOR]].\n<hr />\n[star] <b>Boost</b> : retournez 1 allié [[CAMOUFLAGED]] que vous contrôlez, après la fin de cette activation.",
  // skrull_menace — Captain America (Pitt'o Nili) (Ally, Secret Invasion)
  'sk208a': "<b>Interruption forcée</b> : quand Captain America est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Pitt'o Nili (Minion, Secret Invasion)
  'sk208b': "Garde. <i>(Tant que ce sbire est engagé avec vous, vous ne pouvez pas attaquer le méchant.)</i>\n<b>Une fois révélé</b> : soignez tous les dégâts de Pitt'o Nili et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Captain Marvel (Khn'nr) (Ally, Secret Invasion)
  'sk209a': "<b>Interruption forcée</b> : quand Captain Marvel est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Khn'nr (Minion, Secret Invasion)
  'sk209b': "<b>Une fois révélé</b> : soignez tous les dégâts de Khn'nr et mettez-le en jeu, engagé avec vous.\n<b>Une fois vaincu</b> : retirez tous les jetons de soupçon de \"Who Do You Trust?\".",
  // skrull_menace — Captain Marvel (M'lanz) (Ally, Secret Invasion)
  'sk210a': "<b>Interruption forcée</b> : quand Captain Marvel est censée quitter le jeu, retournez-la à la place.",
  // skrull_menace — M'lanz (Minion, Secret Invasion)
  'sk210b': "<b>Une fois révélé</b> : soignez tous les dégâts de M'lanz et mettez-la en jeu, engagée avec vous.\n[star] <b>Interruption forcée</b> : quand M'lanz vous attaque, résolvez également son attaque contre chaque autre héros.",
  // skrull_menace — Carnage (Zr'x) (Ally, Secret Invasion)
  'sk211a': "<b>Interruption forcée</b> : quand Carnage est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Zr'x (Minion, Secret Invasion)
  'sk211b': "Ténacité. <i>(Ce personnage entre en jeu avec une carte d'état Tenace.)</i>\n<b>Une fois révélé</b> : soignez tous les dégâts de Zr'x et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Daredevil (Trl'k) (Ally, Secret Invasion)
  'sk212a': "<b>Interruption forcée</b> : quand Daredevil est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Trl'k (Minion, Secret Invasion)
  'sk212b': "Tant que le joueur engagé est engagé avec un autre sbire [[SKRULL]], Trl'k ne peut pas subir de dégâts.\n<b>Une fois révélé</b> : soignez tous les dégâts de Trl'k et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Deathlok (Fry'lu) (Ally, Secret Invasion)
  'sk213a': "<b>Interruption forcée</b> : quand Deathlok est censée quitter le jeu, retournez-la à la place.",
  // skrull_menace — Fry'lu (Minion, Secret Invasion)
  'sk213b': "<b>Une fois révélé</b> : soignez tous les dégâts de Fry'lu et mettez-la en jeu, engagée avec vous.\n<b>Une fois vaincue</b> : donnez une carte Rencontre face cachée au joueur qui a vaincu Fry'lu.",
  // skrull_menace — Dum Dum Dugan (Sn'Tlo) (Ally, Secret Invasion)
  'sk214a': "<b>Interruption forcée</b> : quand Dum Dum Dugan est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Sn'Tlo (Minion, Secret Invasion)
  'sk214b': "Diminuez de 1 la quantité de dégâts que Sn'Tlo subit à chaque attaque.\n<b>Une fois révélé</b> : soignez tous les dégâts de Sn'Tlo et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Elektra (Siri) (Ally, Secret Invasion)
  'sk215a': "<b>Interruption forcée</b> : quand Elektra est censée quitter le jeu, retournez-la à la place.",
  // skrull_menace — Siri (Minion, Secret Invasion)
  'sk215b': "Patrouille. <i>(Tant que ce sbire est engagé avec vous, vous ne pouvez pas déjouer la manigance principale.)</i>\n<b>Une fois révélé</b> : soignez tous les dégâts de Siri et mettez-la en jeu, engagée avec vous.",
  // skrull_menace — Giant-Man (D'lutz) (Ally, Secret Invasion)
  'sk216a': "<b>Interruption forcée</b> : quand Giant-Man est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — D'lutz (Minion, Secret Invasion)
  'sk216b': "Riposte 1.\n<b>Une fois révélé</b> : soignez tous les dégâts de D'lutz et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Invisible Woman (De'Lila) (Ally, Secret Invasion)
  'sk217a': "<b>Interruption forcée</b> : quand Invisible Woman est censée quitter le jeu, retournez-la à la place.",
  // skrull_menace — De'Lila (Minion, Secret Invasion)
  'sk217b': "En tant que coût supplémentaire pour attaquer De'Lila, vous devez dépenser 1 ressource de n'importe quel type.\n<b>Une fois révélé</b> : soignez tous les dégâts de De'Lila et mettez-la en jeu, engagée avec vous.",
  // skrull_menace — Iron Fist (Grrix) (Ally, Secret Invasion)
  'sk218a': "<b>Interruption forcée</b> : quand Iron Fist est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Grrix (Minion, Secret Invasion)
  'sk218b': "<b>Une fois révélé</b> : soignez tous les dégâts de Grrix et mettez-le en jeu, engagé avec vous.\n<b>Une fois vaincu</b> : le méchant attaque le joueur qui a vaincu Grrix <i>(même si ce joueur est sous forme d'alter ego)</i>.",
  // skrull_menace — Iron Man (Ssrov) (Ally, Secret Invasion)
  'sk219a': "<b>Interruption forcée</b> : quand Iron Man est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Ssrov (Minion, Secret Invasion)
  'sk219b': "[star] Tant que le méchant a le trait [[REVEALED]], Ssrov gagne +1 MNG et +1 ATQ.\n<b>Une fois révélé</b> : soignez tous les dégâts de Ssrov et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Moon Knight (Hs'fld) (Ally, Secret Invasion)
  'sk220a': "<b>Interruption forcée</b> : quand Moon Knight est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Hs'fld (Minion, Secret Invasion)
  'sk220b': "<b>Une fois révélé</b> : soignez tous les dégâts de Hs'fld et mettez-le en jeu, engagé avec vous.\n<b>Une fois vaincu</b> : le joueur qui a vaincu Hs'fld met en jeu sous son contrôle un allié [[CAMOUFLAGED]] pris au hasard dans le deck [[IMPOSTOR]].",
  // skrull_menace — Nick Fury (H'kurrek) (Ally, Secret Invasion)
  'sk221a': "<b>Interruption forcée</b> : quand Nick Fury est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — H'kurrek (Minion, Secret Invasion)
  'sk221b': "[star] Les attaques de H'kurrek gagnent Déferlement, Perçant et Distance.\n<b>Une fois révélé</b> : soignez tous les dégâts de H'kurrek et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Phoenix (Korya) (Ally, Secret Invasion)
  'sk222a': "<b>Interruption forcée</b> : quand Phoenix est censée quitter le jeu, retournez-la à la place.",
  // skrull_menace — Korya (Minion, Secret Invasion)
  'sk222b': "<b>Une fois révélé</b> : soignez tous les dégâts de Korya et mettez-la en jeu, engagée avec vous.\n[star] <b>Réponse forcée</b> : après que Korya vous a attaqué, défaussez la première carte du deck de chaque joueur.",
  // skrull_menace — Spider-Man (Ch'Gra) (Ally, Secret Invasion)
  'sk223a': "<b>Interruption forcée</b> : quand Spider-Man est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Ch'Gra (Minion, Secret Invasion)
  'sk223b': "<b>Une fois révélé</b> : soignez tous les dégâts de Hagar et mettez-le en jeu, engagé avec vous.\n<b>Une fois vaincu</b> : retournez Queen Veranke.",
  // skrull_menace — Thor (Hagar) (Ally, Secret Invasion)
  'sk224a': "<b>Interruption forcée</b> : quand Thor est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Hagar (Minion, Secret Invasion)
  'sk224b': "[star] Les attaques de Hagar infligent des dégâts indirects.\n<b>Une fois révélé</b> : soignez tous les dégâts de Hagar et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Venom (Dharr) (Ally, Secret Invasion)
  'sk225a': "<b>Interruption forcée</b> : quand Venom est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Dharr (Minion, Secret Invasion)
  'sk225b': "Vilenie. <i>(Quand ce sbire s'active, donnez-lui une carte de boost.)</i>\n<b>Une fois révélé</b> : soignez tous les dégâts de Dharr et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Wolverine (V'lrym) (Ally, Secret Invasion)
  'sk226a': "<b>Interruption forcée</b> : quand Wolverine est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — V'lrym (Minion, Secret Invasion)
  'sk226b': "Coup rapide.\n<b>Une fois révélé</b> : soignez tous les dégâts de V'lrym et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Yellowjacket (Criti Noll) (Ally, Secret Invasion)
  'sk227a': "<b>Interruption forcée</b> : quand Yellowjacket est censé quitter le jeu, retournez-le à la place.",
  // skrull_menace — Criti Noll (Minion, Secret Invasion)
  'sk227b': "Incitation 3. <i>(Quand cette carte est révélée, placez 3 menaces sur la manigance principale.)</i>\n<b>Une fois révélé</b> : soignez tous les dégâts de Criti Noll et mettez-le en jeu, engagé avec vous.",
  // skrull_menace — Kly'bn (Villain, stade I)
  'sk170a': "<b>Une fois révélé</b> : placez 1 jeton de foi sur Kly'bn.\n<b>Réponse forcée</b> : après avoir résolu l'étape 1 de la phase du méchant, défaussez la carte du dessus du deck Rencontre pour chaque jeton de foi sur Kly'bn. Attribuez à chaque joueur, dans l'ordre des joueurs, chaque carte qui n'est pas une traîtrise défaussée de cette façon comme carte Rencontre face cachée.",
  // skrull_menace — Sl'gur't (Villain, stade I)
  'sk170b': "<b>Une fois révélé</b> : placez 1 jeton de foi sur Sl'gur't.\n<b>Réponse forcée</b> : après avoir résolu l'étape 1 de la phase du méchant, défaussez la carte du dessus du deck Rencontre pour chaque jeton de foi sur Sl'gur't. Attribuez à chaque joueur, dans l'ordre des joueurs, chaque carte qui est une traîtrise défaussée de cette façon comme carte Rencontre face cachée.",
  // skrull_menace — Kly'bn (Villain, stade II)
  'sk171a': "<b>Une fois révélé</b> : placez 1 jeton de foi sur Kly'bn.\n<b>Réponse forcée</b> : après avoir résolu l'étape 1 de la phase du méchant, défaussez la carte du dessus du deck Rencontre pour chaque jeton de foi sur Kly'bn. Attribuez à chaque joueur, dans l'ordre des joueurs, chaque carte qui n'est pas une traîtrise défaussée de cette façon comme carte Rencontre face cachée.",
  // skrull_menace — Sl'gur't (Villain, stade II)
  'sk171b': "<b>Une fois révélé</b> : placez 1 jeton de foi sur Sl'gur't.\n<b>Réponse forcée</b> : après avoir résolu l'étape 1 de la phase du méchant, défaussez la carte du dessus du deck Rencontre pour chaque jeton de foi sur Sl'gur't. Attribuez à chaque joueur, dans l'ordre des joueurs, chaque carte qui est une traîtrise défaussée de cette façon comme carte Rencontre face cachée.",
  // skrull_menace — Kly'bn (Villain, stade III)
  'sk172a': "<b>Une fois révélé</b> : placez 1 jeton de foi sur Kly'bn et donnez-lui une carte d'état Tenace.\n<b>Réponse forcée</b> : après avoir résolu l'étape 1 de la phase du méchant, défaussez la carte du dessus du deck Rencontre pour chaque jeton de foi sur Kly'bn. Attribuez à chaque joueur, dans l'ordre des joueurs, chaque carte qui n'est pas une traîtrise défaussée de cette façon comme carte Rencontre face cachée.",
  // skrull_menace — Sl'gur't (Villain, stade III)
  'sk172b': "<b>Une fois révélé</b> : placez 1 jeton de foi sur Sl'gur't et donnez-lui une carte d'état Tenace.\n<b>Réponse forcée</b> : après avoir résolu l'étape 1 de la phase du méchant, défaussez la carte du dessus du deck Rencontre pour chaque jeton de foi sur Sl'gur't. Attribuez à chaque joueur, dans l'ordre des joueurs, chaque carte qui est une traîtrise défaussée de cette façon comme carte Rencontre face cachée.",
  // skrull_menace — Protect the Pantheon (MainScheme, 1A)
  'sk173a': "<b>Contenu</b> : Kly'bn (I) et Kly'bn (II) <i>(Kly'bn (II) et Kly'bn (III) en mode expert)</i>. Les sets de rencontre Skrull Pantheon, Dard'van Sect et Standard. Un set de rencontre modulaire <i>(Skrull Society)</i>.\n<b>Mise en place</b> : mettez l'environnement Skrull Pantheon de côté, hors du jeu.",
  // skrull_menace — Protect the Pantheon (MainScheme, 1B)
  'sk173b': "<b>Interruption forcée</b> : quand la dernière menace est retirée de cette manigance, mettez en jeu l'environnement Skrull Pantheon mis de côté, face <b><i>DESTROYED</i></b> visible. Avancez au stade 2B.\n<b>Une fois achevé</b> : mettez en jeu l'environnement Skrull Pantheon mis de côté, face <b><i>STRONGHOLD</i></b> visible. Avancez au stade 2A.",
  // skrull_menace — Slaying the False Gods (MainScheme, 2A)
  'sk174a': "<i>Kly'bn, l'Éternel Skrull, et Sl'gur't des Noms Infinis sont présentés comme l'empereur et l'impératrice du Panthéon skrull.</i>\n<b>Une fois révélée</b> : cherchez la manigance annexe Strengthen the Faith dans le deck Rencontre ou la pile de défausse rencontre, révélez-la et placez-y 2[per_hero] menaces supplémentaires.",
  // skrull_menace — Slaying the False Gods (MainScheme, 2B)
  'sk174b': "<i>Kly'bn et Sl'gur't ont indirectement soutenu la création et l'expansion de l'Empire skrull. Ils ont conquis et asservi les panthéons des races conquises, près de 1000 panthéons. Maintenant, le duo en veut aux dieux de la Terre.</i>\n<b>Une fois révélée</b> : retournez le méchant.\n<b>Si ce stade est achevé, les joueurs perdent la partie.</b>",
  // skrull_menace — Skrull Pantheon (Environment, Stronghold)
  'sk175a': "<b>Action de héros</b> : dépensez 2 ressources du même type → retirez 1 jeton de foi du méchant.\n<i>Kly'bn et Sl'gur't se sont unis et sont montés à la divinité, devenant les chefs du Panthéon skrull.</i>",
  // skrull_menace — Skrull Pantheon (Environment, Destroyed)
  'sk175b': "<b>Action de héros</b> : dépensez 2 ressources de n'importe quel type → retirez 1 jeton de foi du méchant.\n<i>Le Panthéon skrull a été détruit avec succès et la Divinité skrull est devenue vraiment furieuse.</i>",
  // skrull_menace — Blessed by Kly'bn (Attachment)
  'sk176': "Attachez cette carte au sbire ayant la MNG la plus faible. Sinon, cette carte gagne Renfort.\nX est égal au nombre de jetons de foi sur le méchant.\n<hr />\n[star] <b>Boost</b> : si cette activation est une manigance, cette carte gagne +2 icônes de boost ([boost][boost]) pour cette activation.",
  // skrull_menace — Blessed by Sl'gur't (Attachment)
  'sk177': "Attachez cette carte au sbire ayant l'ATQ la plus faible. Sinon, cette carte gagne Renfort.\nX est égal au nombre de jetons de foi sur le méchant.\n<hr />\n[star] <b>Boost</b> : si cette activation est une attaque, cette carte gagne +2 icônes de boost ([boost][boost]) pour cette activation.",
  // skrull_menace — Nogor (Minion)
  'sk178': "[star] Nogor gagne +1 MNG, +1 ATQ et +1 point de vie pour chaque jeton de foi sur le méchant.\n<b>Une fois révélé</b> : retournez le méchant.\n<hr />\n[star] <b>Boost</b> : retournez le méchant.\n<i>\"Je suis le harnais vivant du pouvoir des dieux.\"</i>",
  // skrull_menace — Shapeless Wastes (SideScheme)
  'sk179': "<i>L'équivalent skrull de l'Enfer est connu sous le nom de Shapeless Wastes.</i>\nEntrave 2[per_hero].\n<b>Réponse forcée</b> : après qu'un allié ou un sbire est vaincu, si ce personnage a le trait [[SKRULL]], retournez le méchant. Sinon, placez 1 jeton de foi sur le méchant.",
  // skrull_menace — Strengthen the Faith (SideScheme)
  'sk180': "<i>La plupart des Skrulls vénèrent Kly'bn, l'Éternel Skrull, et Sl'gur't des Noms Infinis. Ce sont les seuls vrais dieux de l'Empire skrull.</i>\n<b>Réponse forcée</b> : après qu'un sbire [[SKRULL]] entre en jeu, placez 1 jeton de foi sur le méchant.\n<hr />\n[star] <b>Boost</b> : placez 1 jeton de foi sur le méchant.",
  // skrull_menace — Prayer to Kly'bn (Treachery)
  'sk181': "<b>Une fois révélée</b> : si Kly'bn est en jeu, il s'active contre vous. Sinon, retournez le méchant.\n<hr />\n[star] <b>Boost</b> : si Kly'bn n'est pas en jeu, retournez le méchant.\n<i>\"Car je suis Kly'bn. Je suis l'Éternel Skrull. Et je vous aime.\" —Kly'bn</i>",
  // skrull_menace — Prayer to Sl'gur't (Treachery)
  'sk182': "<b>Une fois révélée</b> : si Sl'gur't est en jeu, elle s'active contre vous. Sinon, retournez le méchant.\n<hr />\n[star] <b>Boost</b> : si Sl'gur't n'est pas en jeu, retournez le méchant.\n<i>\"Comment vous appelle-t-on ? Je vous prie, dites-le-nous...\" —Sl'gur't</i>",
  // skrull_menace — Talisman of the Skrulls (Treachery)
  'sk183': "<b>Une fois révélée</b> : cherchez Nogor dans le deck Rencontre ou la pile de défausse rencontre et révélez-le. Si Nogor n'est pas entré en jeu de cette façon, cette carte gagne Renfort.\n<i>\"Le Talisman est la représentation des dieux, et sa présence est requise pour assurer la bénédiction des dieux sur nos entreprises\" —Jazinda</i>",
  // skrull_menace — Dard'van Fanatic (Minion)
  'sk184': "<b>Une fois révélé</b> : choisissez : soit vous infligez 1 dégât à chaque personnage que vous contrôlez, soit vous placez 1 menace sur chaque manigance en jeu.\n<i>\"J'appartiens à la secte Dard'van. Certains la considèrent comme extrême.\" —Grrix</i>",
  // skrull_menace — Dard'van Priest (Minion)
  'sk185': "<b>Une fois révélé</b> : Dard'van Priest manigance.\n[star] <b>Interruption forcée</b> : quand Dard'van Priest est censé attaquer, choisissez à la place une carte en jeu qui a une capacité \"<b>Une fois révélé</b>\" et résolvez cette capacité.\n<i>\"Il vous aime.\"</i>",
  // skrull_menace — Dard'van Sect (SideScheme)
  'sk186': "<i>Une secte zélée de l'Empire skrull qui suit des prophéties annonçant que la Terre deviendra la nouvelle patrie de la race skrull.</i>\n<b>Une fois révélée</b> : donnez 1 carte de boost face cachée au méchant.",
  // skrull_menace — Collective Prayers (Treachery)
  'sk187': "<b>Une fois révélée</b> : défaussez la carte du dessus du deck Rencontre pour chaque personnage en jeu. Révélez chaque carte défaussée de cette façon qui appartient au set de rencontre Dard'van Sect.\n<i>\"...le premier nous aime tous de la même façon.\" —Grrix</i>",
  // skrull_menace — Sectarian Practices (Treachery)
  'sk188': "<b>Une fois révélée</b> : choisissez une carte en jeu qui a une capacité \"<b>Une fois révélé</b>\" et résolvez cette capacité. Si vous ne pouvez pas, cette carte gagne Renfort.\n<i>\"La confiance. Que savent les humains de la confiance ? Vous n'arrivez même pas à vous accorder sur un seul dieu.\" —Nogor</i>",
  // skrull_menace — Shaper of Worlds (Minion)
  'sk228': "<b>Réponse forcée</b> : après qu'un joueur a attaqué Shaper of Worlds, mélangez cette carte dans le deck de ce joueur.\n<b>Interruption forcée</b> : quand Shaper of Worlds entre dans votre main, défaussez les 4 cartes du dessus du deck Rencontre. Mettez Shaper of Worlds en jeu engagé avec vous.",
  // skrull_menace — Cosmic Cube Creation (SideScheme)
  'sk229': "Entrave 4[per_hero]. Victoire 2.\n<b>Une fois révélée</b> : mettez en jeu Shaper of Worlds, mis de côté, engagé avec vous.\n<b>Une fois déjouée</b> : chaque joueur choisit un exemplaire de la ressource Cosmic Cube Fragment mise de côté et le mélange dans son deck.",
  // skrull_menace — Cosmic Cube Fragment (Resource, A)
  'sk230a': "<i>Un artefact capable de modifier la réalité selon les souhaits de son utilisateur. Les Skrulls furent la première race à créer un Cube Cosmique.</i>",
  // skrull_menace — Cosmic Cube Fragment (Resource, B)
  'sk230b': "<i>Un artefact capable de modifier la réalité selon les souhaits de son utilisateur. Les Skrulls furent la première race à créer un Cube Cosmique.</i>",
  // skrull_menace — Cosmic Cube Fragment (Resource, C)
  'sk230c': "<i>Un artefact capable de modifier la réalité selon les souhaits de son utilisateur. Les Skrulls furent la première race à créer un Cube Cosmique.</i>",
  // skrull_menace — Cosmic Cube Fragment (Resource, D)
  'sk230d': "<i>Un artefact capable de modifier la réalité selon les souhaits de son utilisateur. Les Skrulls furent la première race à créer un Cube Cosmique.</i>",
  // skrull_menace — Crusader (Minion)
  'sk231': "Victoire 1.\n<b>Une fois révélé</b> : infligez 1 dégât à chaque personnage que vous contrôlez. Donnez au méchant 1 carte de boost face cachée pour chaque personnage vaincu de cette façon.\n[star] <b>Boost</b> : mettez Crusader en jeu engagé avec vous.",
  // skrull_menace — Enemy Adaptation (Attachment)
  'sk232': "Attachez cette carte à un sbire [[SKRULL]]. Si vous ne le pouvez pas, attachez-la au méchant.\nVous ne pouvez pas défendre contre les attaques de l'ennemi attaché.\n<b>Action de héros</b> : donnez au méchant 1 carte de boost face cachée → défaussez Enemy Adaptation.",
  // skrull_menace — Freedom Ring (Attachment)
  'sk233': "Attachez cette carte à Crusader. Si Crusader n'est pas en jeu, défaussez des cartes du dessus du deck Rencontre jusqu'à ce qu'un sbire soit défaussé. Mettez ce sbire en jeu engagé avec vous et attachez-lui cette carte. Si vous ne le pouvez pas, donnez au méchant 1 carte de boost face cachée.\nLe sbire attaché gagne Vilenie.",
  // skrull_menace — Spy Training (SideScheme)
  'sk234': "<i>Z'Reg, un agent skrull marqué par son camarade de formation K'rtem, fut envoyé espionner les Avengers une fois son entraînement terminé.</i>\n<b>Une fois révélée</b> : vainquez un allié que vous contrôlez et donnez au méchant 1 carte de boost face cachée.",
  // skrull_menace — Rivals to the End (Treachery)
  'sk235': "<b>Une fois révélée</b> : choisissez un sbire. Ce sbire attaque votre héros deux fois de suite. Si aucune attaque n'a été effectuée de cette façon, donnez au méchant 1 carte de boost face cachée pour chaque personnage que vous contrôlez.\n<i>« Ta stratégie est pitoyable, humain ! Tu te précipites au combat puis tu dorlotes tes faibles ! Ha ! Laisse-moi te montrer comment les Skrulls répondent à l'appel ! » —K'rtem</i>",
  // skrull_menace — Jazinda (Minion)
  'sk236': "Victoire 1.\nLe méchant gagne +1 MNG.\n[star] <b>Boost</b> : mettez Jazinda en jeu engagée avec vous.\n<i>« Se faire passer pour une humaine est amusant. Surtout quand je le fais tellement mieux que vous. »</i>",
  // skrull_menace — Skrull Energy Gun (Attachment)
  'sk237': "Attachez cette carte à un sbire [[SKRULL]]. Si vous ne le pouvez pas, attachez-la au méchant.\nTant qu'elle est attachée à un ennemi [[SKRULL]], les attaques de l'ennemi attaché gagnent Déferlement, Perçant et Distance.\n<b>Action de héros</b> : dépensez une ressource [physical] → attachez cette carte à un autre ennemi.",
  // skrull_menace — Sy-Torak Gem (Attachment)
  'sk238': "Attachez cette carte à Jazinda. Si vous ne le pouvez pas, attachez-la au méchant.\nLe personnage attaché gagne +3 points de vie.\n<b>Action de héros</b> : donnez au méchant 1 carte de boost face cachée et dépensez une ressource [energy] → défaussez Sy-Torak Gem.",
  // skrull_menace — Stealing for the Empire (SideScheme)
  'sk239': "<i>Un ancien agent de l'Empire Skrull fut envoyé récupérer un artefact sacré des Skrulls volé par les Krees.</i>\n<b>Une fois révélée</b> : défaussez des cartes du deck Rencontre jusqu'à ce qu'un attachement soit défaussé. Révélez cet attachement. Ensuite, placez sur la manigance principale un nombre de menaces égal au nombre d'icônes de boost ([boost]) de cet attachement.",
  // skrull_menace — Skrull of Royal Blood (Treachery)
  'sk240': "Renfort.\n<b>Une fois révélée</b> : mélangez dans le deck Rencontre toutes les cartes de la pile de défausse rencontre qui ont le plus grand nombre d'icônes de boost ([boost]).",
  // skrull_menace — Skymax (Minion)
  'sk241': "Victoire 1.\n<b>Une fois révélé</b> : mélangez dans le deck Rencontre tous les sbires de la pile de défausse rencontre.\n[star] <b>Boost</b> : mettez Skymax en jeu engagé avec vous.",
  // skrull_menace — Changing Appearance (Attachment)
  'sk242': "Attachez cette carte à un sbire [[SKRULL]]. Si vous ne le pouvez pas, attachez-la au méchant.\nL'ennemi attaché ne peut pas être attaqué.\n<b>Interruption forcée</b> : quand l'ennemi attaché est censé attaquer, il manigance à la place. Ensuite, défaussez cette carte.\n<i>« Tu n'es pas mauvais, mais mon peuple a inventé le changement de forme ! » —Skymax</i>",
  // skrull_menace — Surprising Alliance (SideScheme)
  'sk243': "<i>« Je suis le dernier survivant de mon monde. » —Skymax</i>\n<b>Réponse forcée</b> : quand un joueur défausse un allié de sa main, il le met en jeu engagé avec lui à la place. Considérez cet allié comme un sbire dont la boîte de texte est vide. Sa MNG est égale à son CTR imprimé et il ne subit pas de dégâts consécutifs.",
  // skrull_menace — Shape Alteration (Treachery)
  'sk244': "<b>Une fois révélée</b> : retirez chaque carte d'état Sonné et Désorienté de chaque ennemi [[SKRULL]] et donnez à chaque ennemi [[SKRULL]] une carte d'état Tenace. S'il n'y a aucun ennemi [[SKRULL]] en jeu, cette carte gagne Renfort.\n[star] <b>Boost</b> : donnez une carte d'état Tenace à 1 ennemi [[SKRULL]].",
  // skrull_menace — War Skrull (Minion)
  'sk245': "Victoire 1.\n[star] <b>Réponse forcée</b> : après que War Skrull vous a attaqué, défaussez les 2 cartes du dessus de votre deck.\n[star] <b>Boost</b> : mettez War Skrull en jeu engagé avec vous.",
  // skrull_menace — Impostor (Attachment, War Skrull)
  'sk246': "Considérez l'allié attaché comme un sbire [[SKRULL]] dont la boîte de texte est vide. Sa MNG est égale à son CTR imprimé et il ne subit pas de dégâts consécutifs.\n<b>Une fois révélée</b> : attachez cette carte à l'allié non-[[SKRULL]] ayant le plus de points de vie restants qui n'a pas d'exemplaire d'Impostor attaché. L'allié attaché s'engage avec son contrôleur. Sinon, le méchant manigance.",
  // skrull_menace — Skrull Commander (Minion, War Skrull)
  'sk247': "Chaque autre sbire [[SKRULL]] gagne +1 ATQ.\n[star] <b>Boost</b> : si cette activation est une attaque, cette carte gagne +2 icônes de boost ([boost][boost]) pour cette attaque.\n<i>« S'il était une menace sérieuse, nous saurions qui il est » —Commandant Ak'strk</i>",
  // skrull_menace — Skrull Geneticist (Minion)
  'sk248': "[star] <b>Boost</b> : distribuez-vous 1 carte Rencontre face cachée.\n<i>« Ces résultats sont fascinants »</i>",
  // skrull_menace — Cloning Program (SideScheme)
  'sk249': "<i>Les scientifiques skrulls avaient cloné des échantillons du sang de Deadpool et s'en servent pour améliorer un escadron de Super-Skrulls. Ils placent aussi Deadpool à la tête de l'entraînement de ces nouveaux Super-Skrulls.</i>\nChaque sbire [[SKRULL]] s'active 1 fois supplémentaire pendant l'étape deux de la phase du Méchant.\nLes menaces ne peuvent pas être retirées de cette manigance tant qu'il n'y a aucun sbire [[SKRULL]] en jeu.",
  // skrull_menace — Xavin (Minion)
  'sk250': "Victoire 1.\n<b>Une fois révélé</b> : défaussez des cartes du deck Rencontre jusqu'à ce qu'une traîtrise soit défaussée. Révélez cette traîtrise.\n[star] <b>Boost</b> : mettez Xavin en jeu engagé avec vous.",
  // skrull_menace — Invisible Forcefield (Attachment)
  'sk251': "Attachez cette carte à l'ennemi ayant le plus de points de vie imprimés et n'ayant pas d'autre Invisible Forcefield attaché. Si vous ne le pouvez pas, cette carte gagne Renfort.\n<b>Interruption forcée</b> : quand n'importe quelle quantité de dégâts est censée être infligée au personnage attaché, placez-la ici à la place. Ensuite, s'il y a au moins 5 dégâts ici, défaussez cette carte.",
  // skrull_menace — Super-Skrull Training Program (SideScheme)
  'sk252': "<i>« Souvenez-vous toujours : face à un adversaire supérieur, apprenez ses faiblesses. Exploitez-les. Telle est la voie des Skrulls. » —Commandant Chrell</i>\n<b>Une fois révélée</b> : donnez une carte d'état Tenace à chaque ennemi [[SKRULL]].",
  // skrull_menace — Going Nova (Treachery)
  'sk253': "<b>Une fois révélée</b> : répartissez 2[per_hero] dégâts indirects parmi les joueurs.\n<i>« Zut. J'oublie toujours à quel point vous êtes fragiles. » —Xavin</i>",
  // skrull_menace — Impostor (Attachment, Standard Skrull)
  'sk254': "Considérez l'allié attaché comme un sbire [[SKRULL]] dont la boîte de texte est vide. Sa MNG est égale à son CTR imprimé et il ne subit pas de dégâts consécutifs.\n<b>Une fois révélée</b> : attachez cette carte à l'allié non-[[SKRULL]] ayant le plus de points de vie restants qui n'a pas d'exemplaire d'Impostor attaché. L'allié attaché s'engage avec son contrôleur. Sinon, le méchant manigance.",
  // skrull_menace — Cursed by the Past (Treachery)
  'sk255': "<b>Une fois révélée</b> : si votre sbire Némésis est en jeu, il s'active contre vous. Sinon, trouvez votre sbire Némésis et révélez-le. Si votre manigance annexe Némésis est en jeu, placez dessus un nombre de menaces égal à sa menace de départ. Sinon, trouvez votre manigance annexe Némésis et révélez-la. Mélangez dans le deck Rencontre les cartes restantes de votre set Némésis mis de côté.",
  // skrull_menace — Experiment Subject (Treachery)
  'sk256': "<b>Une fois révélée</b> : défaussez une amélioration que vous contrôlez. Si aucune carte n'a été défaussée de cette façon, le méchant manigance.\n<i>« Je suis curieux de voir jusqu'où vont les limites de son extension... » —Scientifique skrull</i>",
  // skrull_menace — Forge Ahead (Treachery)
  'sk257': "<b>Une fois révélée</b> : chaque sbire engagé avec vous manigance. Si aucune manigance n'a été effectuée de cette façon, le méchant manigance.\n<i>« Nous ne parlons pas de conquête. Voyez cela plutôt comme une... occupation protectrice stratégique. » —Nogor</i>",
  // skrull_menace — Mobilization (Treachery)
  'sk258': "<b>Une fois révélée (alter ego)</b> : engagez chaque sbire en jeu. Le méchant manigance.\n<b>Une fois révélée (héros)</b> : le méchant et chaque sbire engagé avec vous vous attaquent.\n<i>« Nous sommes, par toutes les définitions, la race supérieure ! » —Dorrek VII</i>",
  // skrull_menace — Stick to the Plan (Treachery)
  'sk259': "<b>Une fois révélée</b> : le méchant attaque le héros ayant le plus de points de vie restants. Si aucune attaque n'a été effectuée de cette façon, le méchant manigance.\n<i>« Prosternez-vous et suppliez devant les Skrulls ! » —Paibok</i>",
  // skrull_menace — Replaced Archenemy (Attachment)
  'sk260': "Le sbire attaché gagne le trait [[SKRULL]].\n<b>Une fois révélée</b> : si votre sbire Némésis est en jeu, attachez-lui cette carte. Ensuite, il s'active contre vous. Sinon, trouvez votre sbire Némésis, attachez-lui cette carte et révélez-le.",
  // skrull_menace — Focused Attention (Treachery)
  'sk261': "Renfort.\n<b>Une fois révélée</b> : donnez au méchant 1 carte de boost face cachée.\n<i>« La Terre paiera pour ce qu'elle a fait à mon peuple ! » —Super-Skrull</i>",
  // skrull_menace — Tricky Assault (Treachery)
  'sk262': "<b>Une fois révélée</b> : passez sous forme de héros. Le méchant vous attaque. Si cette attaque n'est pas défendue, le méchant manigance.\n<i>« Nous sommes prêts à accepter votre reddition. » —Skrull inconnu</i>",
  // leonardo — * Leonardo (Hero)
  'tl001a': "<i>Kenjutsu</i> — <b>Action</b> : redressez une amélioration [[WEAPON]] que vous contrôlez. <i>(Limite d'une fois par round.)</i>",
  // leonardo — * Leo (AlterEgo)
  'tl001b': "<b>Action</b> : défaussez 1 carte de votre main → cherchez dans votre deck et votre défausse jusqu'à 2 améliorations [[KATANA]] et mettez-les en jeu, inclinées. <i>(Mélangez.)</i>",
  // leonardo — * Splinter (Ally)
  'tl002': "<b>Réponse</b> : après que Splinter entre en jeu, choisissez une carte spécifique à l'identité dans votre défausse et placez-la sur le dessus de votre deck.",
  // leonardo — Uke Nagashi (Event)
  'tl003': "<b>Interruption de héros</b> <i>(défense)</i> : quand Leonardo se défend contre une attaque, il gagne +2 DEF pour cette attaque. Si vous avez payé cette carte avec une ressource [physical], redressez Leonardo.",
  // leonardo — Vigilant (Event)
  'tl004': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Si vous avez payé cette carte avec une ressource [mental], redressez une amélioration [[KATANA]] que vous contrôlez.",
  // leonardo — Stoicism (Event)
  'tl005': "<b>Action de héros</b> : redressez Leonardo. Si vous avez payé cette carte avec une ressource [energy], redressez une amélioration [[KATANA]] que vous contrôlez.",
  // leonardo — Yo Ko Giri (Event)
  'tl006': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Cette attaque gagne Perçant. Si vous avez payé cette carte avec des ressources [energy][mental][physical], vous pouvez la remettre dans votre main.",
  // leonardo — * Leo's Greenhouse (Support)
  'tl007': "<b>Action d'alter ego</b> : inclinez Leo's Greenhouse et défaussez 1 carte de votre main → piochez 2 cartes et soignez 2 dégâts de votre identité.",
  // leonardo — Iaijutsu (Upgrade)
  'tl008': "<b>Interruption de héros</b> : quand un ennemi initie une attaque, inclinez une amélioration [[KATANA]] que vous contrôlez → vous pouvez jouer depuis votre main un événement [[ATTACK]] ayant une capacité « <b>Action de héros</b> » <i>(en payant son coût)</i>. Si cette attaque met K.O. un ennemi, piochez 1 carte.",
  // leonardo — Taichō (Upgrade)
  'tl009': "<b>Action de héros</b> : inclinez une amélioration [[KATANA]] que vous contrôlez → redressez cette carte.\n<b>Réponse de héros</b> : après qu'un allié subit des dégâts consécutifs ([consequential]), inclinez cette carte → redressez cet allié.",
  // leonardo — Nukitsuke (Upgrade)
  'tl010': "<b>Action de héros</b> : inclinez Nukitsuke → redressez une amélioration [[KATANA]] que vous contrôlez.",
  // leonardo — * Leonardo's Katana (Upgrade)
  'tl011': "Restreint.\nChaque amélioration [[KATANA]] que vous contrôlez gagne : « <b>Ressource de héros</b> : inclinez cette carte → générez une ressource [wild] pour une carte spécifique à l'identité. »",
  // leonardo — * Leonardo's Other Katana (Upgrade)
  'tl012': "Restreint.\n<b>Action de héros</b> : choisissez un personnage ami et inclinez 2 améliorations [[KATANA]] que vous contrôlez → ce personnage gagne +1 à chacun de ses pouvoirs de base jusqu'à la fin du round.",
  // leonardo — Brainwashed Betrayal (Obligation)
  'tl013': "<b><i>Donnez-la au joueur Leo.</i></b>\nPassez sous forme de héros et défaussez un allié que vous contrôlez. Vous ne pouvez pas attaquer le méchant.\n<b>Réponse forcée</b> : après que votre tour commence, infligez 3 dégâts à un allié.\n<b>Action d'alter ego</b> : inclinez Leo et subissez 2 dégâts → retirez Brainwashed Betrayal de la partie.",
  // leonardo — Foot Patrol (SideScheme némésis)
  'tl014': "<i>Karai est en patrouille avec le Foot Clan.</i>\n<b>Une fois déjouée</b> : cherchez dans le deck Rencontre et la défausse Rencontre un sbire [[FOOT CLAN]] et mettez-le en jeu, engagé avec le premier joueur.",
  // leonardo — * Karai (Minion némésis)
  'tl015': "<b>Une fois révélée</b> : camouflez Karai.\n<b>Une fois vaincu</b> : camouflez le méchant.\n<i>(Sbire némésis de Leonardo.)</i>\n<hr />\n[star] <b>Boost</b> : attribuez cette carte au premier joueur comme carte Rencontre face cachée.",
  // leonardo — Foot Soldiers (Minion némésis)
  'tl016': "<b>Une fois révélée</b> : camouflez Foot Soldiers.",
  // ---- bebop_rocksteady (Inkwire, TMNT Villains, prefixe tk) : ecrit par l'agent Bebop & Rocksteady, 16/10/2026
  // bebop_rocksteady — * Bebop (Villain)
  'tk001a': "<b>Interruption forcée</b> : quand la phase du méchant commence, retirez 1 jeton Andouille de l'attachement [[HOG]] ou placez 1 menace sur la manigance principale.\n<b>Réponse forcée</b> : après que Bebop subit des dégâts, résolvez la capacité « <b>Spécial</b> » de l'attachement [[HOG]].",
  // bebop_rocksteady — * Bebop (Villain)
  'tk001b': "[star] <b>Interruption forcée</b> : quand Bebop s'active, retirez plutôt 1 jeton Andouille de l'attachement [[HOG]]. S'il n'y a aucun jeton Andouille ici, retournez Bebop sur sa face [[ALERT]].\n<i>« J'ai mal à la tête ! »</i>",
  // bebop_rocksteady — * Bebop (Villain)
  'tk002a': "<b>Interruption forcée</b> : quand la phase du méchant commence, retirez 1 jeton Andouille de l'attachement [[HOG]] ou placez 2 menaces sur la manigance principale.\n<b>Réponse forcée</b> : après que Bebop subit des dégâts, résolvez la capacité « <b>Spécial</b> » de l'attachement [[HOG]].",
  // bebop_rocksteady — * Bebop (Villain)
  'tk002b': "[star] <b>Interruption forcée</b> : quand Bebop s'active, retirez plutôt 2 jetons Andouille de l'attachement [[HOG]]. S'il n'y a aucun jeton Andouille ici, retournez Bebop sur sa face [[ALERT]].\n<i>« J'ai mal à la tête ! »</i>",
  // bebop_rocksteady — * Rocksteady (Villain)
  'tk003a': "<b>Interruption forcée</b> : quand la phase du méchant commence, donnez une carte d'état Tenace à Rocksteady. Retirez 1 jeton Andouille de l'attachement [[RHINO]], ou infligez 1 dégât au premier joueur.\n<b>Réponse forcée</b> : après que Rocksteady subit des dégâts, résolvez la capacité « <b>Spécial</b> » de l'attachement [[RHINO]].",
  // bebop_rocksteady — * Rocksteady (Villain)
  'tk003b': "[star] <b>Interruption forcée</b> : quand Rocksteady s'active, retirez plutôt 1 jeton Andouille de l'attachement [[RHINO]]. S'il n'y a aucun jeton Andouille ici, retournez Rocksteady sur sa face [[ALERT]].\n<i>« Qu'est-ce qui m'a frappé ? »</i>",
  // bebop_rocksteady — * Rocksteady (Villain)
  'tk004a': "<b>Interruption forcée</b> : quand la phase du méchant commence, donnez une carte d'état Tenace à Rocksteady. Retirez 1 jeton Andouille de l'attachement [[RHINO]], ou infligez 2 dégâts au premier joueur.\n<b>Réponse forcée</b> : après que Rocksteady subit des dégâts, résolvez la capacité « <b>Spécial</b> » de l'attachement [[RHINO]].",
  // bebop_rocksteady — * Rocksteady (Villain)
  'tk004b': "[star] <b>Interruption forcée</b> : quand Rocksteady s'active, retirez plutôt 2 jetons Andouille de l'attachement [[RHINO]]. S'il n'y a aucun jeton Andouille ici, retournez Rocksteady sur sa face [[ALERT]].\n<i>« Qu'est-ce qui m'a frappé ? »</i>",
  // bebop_rocksteady — Demolition Crew (MainScheme)
  'tk005a': "<i>Bebop et Rocksteady laissent un sillage de destruction dans tout Manhattan !</i>\n<b>Contenu</b> : Bebop (A1) et Rocksteady (A1), <i>(Bebop (B1) et Rocksteady (B1) en mode expert.)</i> Ensembles Bebop & Rocksteady, Concrete Jungle et Standard. Un ensemble Rencontre modulaire <i>(Rock the Block)</i>.\n<b>Mise en place</b> : mettez en jeu l'environnement Destructive Dunderheads, la manigance annexe Welcome to the Jungle, l'attachement Hog Wild et l'attachement Rhino Rage.",
  // bebop_rocksteady — Demolition Crew (MainScheme)
  'tk005b': "<i>Alors que vous sortez des égouts, Bebop et Rocksteady vous accueillent. On dirait qu'ils vous attendaient !</i>\n[star] <b>Interruption forcée</b> : quand cette manigance est censée être achevée, retirez plutôt toute la menace d'ici. Puis, dans l'ordre des joueurs, Bebop et Rocksteady attaquent chaque joueur <i>(même sous forme d'alter ego)</i>.",
  // bebop_rocksteady — Destructive Dunderheads (Environment)
  'tk006a': "<i>Double Peine</i> — Pendant l'étape 2 de la phase du méchant, les deux méchants s'activent contre chaque joueur. Choisissez Bebop ou Rocksteady comme cible de chaque carte qui mentionne « le méchant ».\n<b>Interruption forcée</b> : quand Bebop ou Rocksteady est vaincu, mettez de côté ce méchant et son attachement [[TEMPER]]. Retournez le méchant restant sur sa face [[ALERT]], et cette carte sur sa face [[FERAL]].",
  // bebop_rocksteady — Gone Berserk! (Attachment)
  'tk006b': "Permanent. Attachez-la au méchant.\nLe méchant attaché ne peut pas être désorienté.\nLe méchant attaché gagne +12[per_hero] points de vie.",
  // bebop_rocksteady — Hog Wild (Attachment)
  'tk007a': "Permanent. Mise en place.\nAttachez-la à Bebop.\n[star] Bebop gagne +1 ATQ pour chaque jeton Andouille ici.\n<b>Spécial</b> : placez 1 jeton Andouille ici. S'il y a au moins 3 jetons Andouille ici, retournez cette carte sur sa face [[ENRAGED]].\n<i>« Ça va devenir sauvage ! »</i> —Bebop",
  // bebop_rocksteady — Headfirst (Attachment)
  'tk007b': "Permanent. Attachez-la à Bebop.\nBebop gagne [[ENRAGED]].\n<b>Spécial</b> : infligez 1 dégât à votre identité.\n<b>Interruption forcée</b> : quand Bebop est censé s'activer, si Headstrong est en jeu, retournez Bebop et Rocksteady sur leurs faces [[K.O.]] et retournez les deux attachements [[TEMPER]] sur leurs faces [[ROWDY]].",
  // bebop_rocksteady — Rhino Rage (Attachment)
  'tk008a': "Permanent. Mise en place.\nAttachez-la à Rocksteady.\n[star] Rocksteady gagne +1 ATQ pour chaque jeton Andouille ici.\n<b>Spécial</b> : placez 1 jeton Andouille ici. S'il y a au moins 3 jetons Andouille ici, retournez cette carte sur sa face [[ENRAGED]].\n<i>« Dégage de mon chemin, minus. »</i> —Rocksteady",
  // bebop_rocksteady — Headstrong (Attachment)
  'tk008b': "Permanent. Attachez-la à Rocksteady.\nRocksteady gagne [[ENRAGED]].\n<b>Spécial</b> : placez 1 menace sur la manigance principale.\n<b>Interruption forcée</b> : quand Rocksteady est censé s'activer, si Headfirst est en jeu, retournez Bebop et Rocksteady sur leurs faces [[K.O.]] et retournez les deux attachements [[TEMPER]] sur leurs faces [[ROWDY]].",
  // bebop_rocksteady — * Shutter Shades (Attachment)
  'tk009': "Attachez-la à Bebop s'il est [[ALERT]]. Sinon, cette carte gagne renfort.\nBebop gagne Solide.\n<b>Une fois révélée</b> : placez 1 jeton Andouille sur l'attachement [[HOG]].\n<b>Réponse forcée</b> : après que Bebop passe sur sa face [[K.O.]], défaussez cette carte.\n<i>« Je porte mes lunettes de soleil la nuit. »</i> —Bebop",
  // bebop_rocksteady — * Aviator Cap (Attachment)
  'tk010': "Attachez-la à Rocksteady s'il est [[ALERT]]. Sinon, cette carte gagne renfort.\nRocksteady gagne Solide.\n<b>Une fois révélée</b> : placez 1 jeton Andouille sur l'attachement [[RHINO]].\n<b>Réponse forcée</b> : après que Rocksteady passe sur sa face [[K.O.]], défaussez cette carte.",
  // bebop_rocksteady — * Roberta (Attachment)
  'tk011': "Attachez-la à Bebop s'il est [[ALERT]]. Sinon, cette carte gagne renfort.\n[star] Les attaques de Bebop gagnent perçant.\n<b>Réponse forcée</b> : après que Bebop passe sur sa face [[K.O.]], défaussez cette carte.\n<i>« C'est l'heure de la boucherie ! »</i> —Bebop",
  // bebop_rocksteady — * Juniper (Attachment)
  'tk012': "Attachez-la à Rocksteady s'il est [[ALERT]]. Sinon, cette carte gagne renfort.\n[star] Les attaques de Rocksteady gagnent déferlement.\n<b>Réponse forcée</b> : après que Rocksteady passe sur sa face [[K.O.]], défaussez cette carte.\n<i>« Je parie que je peux vous convaincre de bouger. »</i> —Rocksteady",
  // bebop_rocksteady — Bumbling Buffoons (SideScheme)
  'tk013': "Esquive. <i>(Quand un personnage déjoue cette manigance annexe, il peut utiliser sa DEF au lieu de sa CTR.)</i>\n<b>Une fois déjouée</b> : choisissez un ennemi. Cet ennemi vous attaque. Vous pouvez infliger les dégâts de cette attaque à un autre ennemi de votre choix à la place.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // bebop_rocksteady — Bumbling Buffoons (SideScheme)
  'tk014': "Esquive. <i>(Quand un personnage déjoue cette manigance annexe, il peut utiliser sa DEF au lieu de sa CTR.)</i>\n<b>Une fois déjouée</b> : choisissez un ennemi. Cet ennemi vous attaque. Vous pouvez infliger les dégâts de cette attaque à un autre ennemi de votre choix à la place.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // bebop_rocksteady — Bumbling Buffoons (SideScheme)
  'tk015': "Esquive. <i>(Quand un personnage déjoue cette manigance annexe, il peut utiliser sa DEF au lieu de sa CTR.)</i>\n<b>Une fois déjouée</b> : choisissez un ennemi. Cet ennemi vous attaque. Vous pouvez infliger les dégâts de cette attaque à un autre ennemi de votre choix à la place.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // bebop_rocksteady — Collision Course (SideScheme)
  'tk016': "<b>Une fois révélée</b> : placez 1 jeton Andouille sur chaque attachement [[TEMPER]].\n<b>Une fois déjouée</b> : sonnez chaque méchant.\n<i>« À terre ! »</i>",
  // bebop_rocksteady — Olé! (SideScheme)
  'tk018': "Entrave 1[per_hero].\n<b>Une fois déjouée</b> : infligez 2[per_hero] dégâts à chaque méchant. Sonnez chaque méchant [[ENRAGED]] blessé de cette façon.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // bebop_rocksteady — Toro! Toro! (SideScheme)
  'tk020': "Esquive. <i>(Quand un personnage déjoue cette manigance annexe, il peut utiliser sa DEF au lieu de sa CTR.)</i>\n<b>Une fois déjouée</b> : placez 2 jetons Andouille sur un attachement [[TEMPER]].",
  // bebop_rocksteady — Lay the Beatdown (Treachery)
  'tk022': "<b>Une fois révélée (alter ego)</b> : désorientez votre identité.\n<b>Une fois révélée (héros)</b> : choisissez :\n• Infligez 2 dégâts indirects à votre héros.\n• Sonnez votre héros.\n<i>« J'adore le son de ce rythme ! »</i> —Bebop",
  // bebop_rocksteady — Pummel (Treachery)
  'tk024': "<b>Une fois révélée</b> : choisissez :\n• Subissez des dégâts égaux à l'ATQ de Bebop ou de Rocksteady.\n• Défaussez l'amélioration ou le soutien de coût le plus élevé que vous contrôlez.\n<i>« Tu me sens ? »</i> —Bebop",
  // bebop_rocksteady — Trample (Treachery)
  'tk026': "<b>Une fois révélée (alter ego)</b> : défaussez 1 carte de votre main.\n<b>Une fois révélée (héros)</b> : choisissez un méchant. Ce méchant attaque le personnage ami ayant le moins de points de vie restants.\n<hr />\n[star] <b>Boost</b> : infligez 1 dégât à un allié que vous contrôlez.",
  // bebop_rocksteady — * Anchovy (Minion)
  'tk028': "Ténacité.\n<b>Interruption forcée</b> : quand Anchovy est vaincu, mélangez-le dans le deck Rencontre.\n<hr />\n[star] <b>Boost</b> : après la résolution de cette activation, attribuez cette carte au premier joueur comme carte Rencontre face cachée.",
  // bebop_rocksteady — Welcome to the Jungle (SideScheme)
  'tk101': "<i>« On ne peut plus se battre dans l'ombre ! Il est temps de porter ce combat jusqu'à eux. »</i> —Raphael\nMise en place. Victoire 0.\n<b>Une fois déjouée</b> : chaque joueur peut choisir 1 carte [[NYC]] mise de côté et la mettre en jeu.",
  // bebop_rocksteady — Road to Ruin (SideScheme)
  'tk102': "<b>Une fois révélée</b> : choisissez :\n• Défaussez un [[LOCATION]] ami.\n• Sonnez votre héros.\n<b>Une fois déjouée</b> : sonnez un ennemi.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // bebop_rocksteady — Fallen Empires (Treachery)
  'tk104': "<b>Une fois révélée</b> : choisissez :\n• Défaussez un [[LOCATION]] ami.\n• Défaussez 1 carte de votre main.\n<hr />\n[star] <b>Boost</b> : défaussez 1 carte de votre main.\n<i>« Manhattan a vraiment mal tourné. »</i> —Bebop",
  // bebop_rocksteady — * Channel 6 News (Support)
  'tk106': "Lié (Welcome to the Jungle).\n<b>Réponse</b> : après qu'une manigance annexe [[NYC]] est révélée, inclinez Channel 6 News → retirez 2 menaces d'une manigance.\n<i>« Qui sont ces nouveaux justiciers ? Restez à l'écoute ! »</i> —April O'Neil",
  // bebop_rocksteady — * Eastman Theater (Support)
  'tk107': "Lié (Welcome to the Jungle).\n<b>Réponse de héros</b> : après qu'une manigance annexe [[NYC]] est déjouée, inclinez Eastman Theater → redressez un héros ami.\n<i>« Vu de bons films dernièrement ? »</i> —Donatello",
  // bebop_rocksteady — * Powder Keg (PlayerSideScheme)
  'tk108': "Lié (Welcome to the Jungle).\nCette carte ne compte pas dans la limite de manigances annexes de joueur.\n<b>Une fois déjouée</b> : le joueur qui a déjoué cette manigance inflige 2 dégâts à chaque ennemi (4 dégâts à la place si l'ennemi est sonné ou désorienté).\n<i>« Snort ! Je suis sérieux, mec ! Tu ne sens pas le gaz, Bebop ? »</i> —Rocksteady",
  // bebop_rocksteady — * Power Play (PlayerSideScheme)
  'tk109': "Lié (Welcome to the Jungle).\nCette carte ne compte pas dans la limite de manigances annexes de joueur.\n<b>Réponse de héros</b> : après que vous retirez de la menace de cette manigance, défaussez 1 carte de votre main → retirez 2 menaces de cette manigance.\n<b>Une fois déjouée</b> : chaque joueur peut sonner et désorienter un ennemi.",
  // bebop_rocksteady — Hittin' the Town (Treachery)
  'tk201': "<b>Une fois révélée</b> : défaussez des cartes du dessus du deck du méchant jusqu'à ce qu'un attachement ou une manigance annexe soit défaussé, et révélez-le.\n<i>« Tu sais ce que c'est ? C'est ma nouvelle coupe de cheveux ! »</i> —Rocksteady",
  // bebop_rocksteady — Jägerbombs (Treachery)
  'tk203': "<b>Une fois révélée</b> : choisissez un :\n• Sonnez votre identité.\n• Désorientez votre identité.\n<i>« Jägerbombs ! Tu me sens, frérot ? »</i> —Bebop",
  // bebop_rocksteady — Get Your Swell On (SideScheme)
  'tk205': "<b>Une fois révélée</b> : soignez 1 dégât de chaque ennemi. Donnez une carte d'état Tenace à chaque ennemi.\n<i>« Tu as besoin de grogner comme ça ? »</i> —Rocksteady\n<i>« Pas maintenant, Chef, je suis dans la zone ! »</i> —Bebop",
  // donatello — * Donatello (Hero)
  'td001a': "<i>Kashikoi</i> — <b>Action</b> : dépensez des ressources [mental][mental] → piochez 2 cartes. <i>(Limite d'une fois par round.)</i>",
  // donatello — * Donnie (AlterEgo)
  'td001b': "<b>Action</b> : défaussez 1 carte de votre main → cherchez dans votre deck et votre défausse Donatello's Bo ou Donatello's Shell et mettez-la en jeu, inclinée. <i>(Mélangez.)</i>",
  // donatello — * Metalhead (Ally)
  'td002': "Ténacité.\n<b>Interruption</b> : quand Donatello se défend contre une attaque, dépensez une ressource [mental] → jouez Metalhead depuis votre main ou depuis Donatello's Shell sans payer son coût en ressources.",
  // donatello — Bō Tobu (Event, x2)
  'td003': "<b>Interruption de héros</b> <i>(défense/contre)</i> : quand vous devriez subir des dégâts d'une attaque, prévenez 3 de ces dégâts et retirez 3 menaces d'une manigance.",
  // donatello — Chūdan-Ura-Uke (Event, x2)
  'td004': "<b>Interruption de héros</b> <i>(attaque/défense)</i> : quand vous devriez subir des dégâts d'une attaque, prévenez 3 de ces dégâts et infligez 3 dégâts à l'ennemi attaquant.",
  // donatello — Improvised Tactics (Event, x2) — « Cloak » = camouflez (statut Camouflé, décision phase B)
  'td005': "<b>Action de héros</b> : inclinez une amélioration [[TECH]] que vous contrôlez → choisissez deux options <i>(vous ne pouvez pas choisir deux fois la même option)</i> :\n• Camouflez deux personnages amis.\n• Sonnez ou désorientez un ennemi.\n• Piochez 2 cartes.",
  // donatello — Singularity (Event)
  'td006': "Jouable uniquement si vous contrôlez l'amélioration Anti-Gravity Gauntlet.\n<b>Action de héros</b> <i>(attaque)</i> : infligez 10 dégâts à un ennemi. Cette attaque gagne Déferlement, Perçant et À Distance.",
  // donatello — Inspired Brilliance (Resource, x2) : aucun texte imprimé, donc aucune entrée
  // donatello — * Donnie's Lab (Support)
  'td008': "<b>Action d'alter ego</b> : inclinez Donnie's Lab → ajoutez à votre main une carte [[ANDROID]], [[ITEM]] ou [[TECH]] de votre défausse.",
  // donatello — * Anti-Gravity Gauntlet (Upgrade)
  'td009': "Donatello gagne +1 ATQ.\n<b>Interruption de héros</b> : quand vous jouez un événement [[ATTACK]], inclinez Anti-Gravity Gauntlet et défaussez 1 carte de votre main → augmentez de 3 les dégâts infligés par cet événement.",
  // donatello — * Truevision Goggles (Upgrade)
  'td010': "<b>Interruption de héros</b> : quand vous effectuez un contre de base, inclinez Truevision Goggles → vous gagnez +1 CTR pour ce contre. Vous pouvez défausser une carte d'état d'un ennemi.",
  // donatello — * Donatello's Bō (Upgrade)
  'td011': "Restreint.\n<b>Action de héros</b> : inclinez cette carte → redressez Donatello.",
  // donatello — * Donatello's Shell (Upgrade)
  'td012': "Vous pouvez jouer, dépenser ou défausser les cartes glissées ici comme si elles étaient dans votre main. <i>(1 carte glissée maximum.)</i>\n<b>Action de héros</b> : inclinez Donatello's Shell → choisissez une carte dans votre main et glissez-la ici.",
  // donatello — Broken Shell (Obligation)
  'td013': "<b><i>Donnez-la au joueur Donnie.</i></b>\nPassez sous forme d'alter ego et perdez 5 points de vie. Si cela devait vaincre votre identité, mettez plutôt votre cadran de points de vie à 1. Vous ne pouvez pas passer sous forme de héros.\n<b>Action d'alter ego</b> : dépensez des ressources [mental][mental] ou défaussez Donatello's Shell du jeu → retirez Broken Shell de la partie.",
  // donatello — Extermination! (SideScheme némésis)
  'td014': "<i>Baxter Stockman a lancé ses machines à la recherche des tortues pour les exterminer.</i>\n<b>Une fois déjouée</b> : cherchez dans le deck Rencontre et la défausse Rencontre un sbire [[MOUSERS]] ou [[FLYBORGS]] et mettez-le en jeu, engagé avec le premier joueur.",
  // donatello — * Baxter Stockman (Minion némésis)
  'td015': "Coup Rapide.\nBaxter Stockman ne peut pas subir de dégâts tant qu'il y a des [[MOUSERS]] ou des [[FLYBORGS]] en jeu.\n<b>Interruption forcée</b> : quand Baxter Stockman devrait vous attaquer, il manigance plutôt.\n<i>(Sbire némésis de Donatello.)</i>",
  // donatello — Plague of M.O.U.S.E.R.s (Minion némésis, x2)
  'td016': "Entre en jeu avec 2 compteurs d'essaim dessus.\n[star] La MNG, l'ATQ et les points de vie de ce sbire sont égaux au nombre de compteurs d'essaim qu'il porte.\n<b>Interruption forcée</b> : quand ce sbire subit des dégâts, retirez plutôt autant de compteurs d'essaim de cette carte.",
  // donatello — Flight of Flyborgs (Minion némésis)
  'td017': "Entre en jeu avec 4 compteurs d'essaim dessus.\n[star] La MNG, l'ATQ et les points de vie de ce sbire sont égaux au nombre de compteurs d'essaim qu'il porte.\n<b>Interruption forcée</b> : quand ce sbire subit des dégâts, retirez plutôt autant de compteurs d'essaim de cette carte.",
  // michelangelo — Michelangelo (Hero) [set 164, Inkwire]
  'tm001a': "<i>Booyakasha</i> — <b>Réponse</b> : après que vous avez utilisé un pouvoir de base <i>(CTR, ATQ ou DEF)</i>, déplacez jusqu'à 3 menaces d'une manigance vers une autre manigance. Vous ne pouvez pas déplacer de menace vers une manigance annexe portant 5[per_hero] menaces ou plus.",
  // michelangelo — Mikey (AlterEgo)
  'tm001b': "<b>Mise en place</b> : mettez en jeu la manigance annexe de joueur I'm Here to Help.\n<b>Action</b> : défaussez 1 carte de votre main → cherchez jusqu'à 2 améliorations [[NUNCHUCK]] dans votre deck et votre défausse et mettez-les en jeu, inclinées. <i>(Mélangez.)</i>",
  // michelangelo — Slash (Ally)
  'tm002': "Riposte 1. Ténacité.\n[star] Les attaques de Slash gagnent Perçant.",
  // michelangelo — Call for Help (Event)
  'tm003': "<b>Action de héros</b> : cherchez dans votre deck et votre défausse un allié ou la manigance annexe de joueur I'm Here to Help et ajoutez cette carte à votre main. <i>(Mélangez.)</i>",
  // michelangelo — Impulsive (Event, x2)
  'tm004': "<b>Action de héros</b> : placez 2 menaces sur la manigance principale → redressez Michelangelo et une carte [[WEAPON]] que vous contrôlez. Piochez 1 carte.",
  // michelangelo — Kaiten (Event, x2)
  'tm005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Vous pouvez incliner une amélioration [[NUNCHUCK]] que vous contrôlez pour désorienter ou sonner cet ennemi.",
  // michelangelo — Majime (Event, x2)
  'tm006': "<b>Action de héros</b> <i>(attaque/contre)</i> : subissez X dégâts <i>(jusqu'à un maximum de 3)</i> → retirez X menaces d'une manigance et infligez X dégâts à un ennemi.",
  // michelangelo — Optimism (Resource, x2)
  'tm007': "<b>Réponse</b> : après que vous avez dépensé cette carte, soignez 1 dégât de votre identité et piochez 1 carte.",
  // michelangelo — Mikey's Couch (Support)
  'tm008': "Mikey gagne +1 REC.\n<b>Action d'alter ego</b> : inclinez Mikey's Couch → choisissez jusqu'à 2 cartes dans votre défausse et mélangez-les dans votre deck.",
  // michelangelo — I'm Here to Help (PlayerSideScheme)
  'tm009': "Cette carte ne compte pas dans la limite de manigances annexes de joueur.\n<b>Réponse forcée</b> : après la fin de la phase des joueurs, retirez 1 menace de cette carte.\n<b>Interruption de héros</b> : quand cette manigance est déjouée, piochez 3 cartes <i>(seul le joueur Michelangelo peut déclencher cette capacité)</i>.",
  // michelangelo — Mikey's Skateboard (Upgrade)
  'tm010': "<b>Réponse</b> : après que vous avez changé de forme, inclinez Mikey's Skateboard → redressez votre identité.",
  // michelangelo — Michelangelo's Nunchuck (Upgrade)
  'tm011': "Restreint.\nChaque amélioration [[NUNCHUCK]] que vous contrôlez gagne : \"<b>Réponse de héros</b> : après que vous avez joué un événement, inclinez cette carte → votre héros gagne +1 à un pouvoir de base jusqu'à la fin du round.\"",
  // michelangelo — Michelangelo's Other Nunchuck (Upgrade)
  'tm012': "Restreint.\nChaque amélioration [[NUNCHUCK]] que vous contrôlez gagne : \"<b>Interruption de héros</b> : quand vous devriez subir des dégâts d'une attaque, inclinez cette carte → réduisez ces dégâts de 1 et infligez 1 dégât à l'ennemi attaquant.\"",
  // michelangelo — All Alone (Obligation)
  'tm013': "<b><i>Donnez-la au joueur Mikey.</i></b>\nPassez sous forme d'alter ego. Inclinez chaque allié et chaque soutien que vous contrôlez. Vous ne pouvez pas changer de forme.\n<b>Action d'alter ego</b> : inclinez votre identité et défaussez 1 carte de votre main → retirez All Alone de la partie.",
  // michelangelo_nemesis — Sewer Problems (SideScheme)
  'tm014': "<i>Quelque chose de terrible grandit dans les égouts.</i>\n<b>Une fois révélée</b> : chaque joueur défausse les 3 premières cartes de son deck.",
  // michelangelo_nemesis — Wyrm (Minion)
  'tm015': "Ténacité.\n<b>Une fois vaincu</b> : mélangez Wyrm dans le deck Rencontre.\n<i>(Sbire némésis de Michelangelo.)</i>",
  // michelangelo_nemesis — Smash! (Treachery, x3)
  'tm016': "<b>Une fois révélée</b> : vous subissez 2 dégâts indirects.",
  // raphael — * Raphael (Hero)
  'tr001a': "Chaque compteur de rage sur Raphael peut être dépensé comme s'il s'agissait d'une ressource [physical].\n<i>Yaban Hito</i> — <b>Réponse</b> : après que Raphael subit des dégâts d'une attaque, placez 1 compteur de rage sur lui (maximum 3).",
  // raphael — * Raph (AlterEgo)
  'tr001b': "<b>Action</b> : défaussez 1 carte de votre main → cherchez dans votre deck et votre défausse jusqu'à 2 améliorations [[SAI]] et mettez-les en jeu, inclinées. <i>(Mélangez.)</i>",
  // raphael — * Casey Jones (Ally)
  'tr002': "<b>Réponse</b> : après que Casey Jones entre en jeu, infligez 1 dégât à Raphael et à chaque sbire engagé avec vous. Placez 1 compteur de rage sur Raphael.",
  // raphael — Disarm (Event)
  'tr003': "<b><i>Exigence</i></b> ([physical]).\n<b>Action de héros</b> <i>(contre)</i> : retirez 4 menaces d'une manigance. Vous pouvez défausser une amélioration [[SAI]] que vous contrôlez pour défausser d'un ennemi un attachement portant le texte \"<b>Action de héros</b>\" ou \"<b>Réponse de héros</b>\".",
  // raphael — Headbutt (Event)
  'tr004': "<b><i>Exigence</i></b> ([physical][physical]).\n<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Sonnez ou désorientez cet ennemi.",
  // raphael — Savage Assault (Event)
  'tr005': "<b><i>Exigence</i></b> ([physical][physical][physical]).\n<b>Action de héros</b> <i>(attaque)</i> : infligez 10 dégâts répartis comme vous le souhaitez entre des ennemis.",
  // raphael — Unbridled Fury (Event)
  'tr006': "1 max par phase.\n<b>Action de héros</b> : Raphael gagne +2 ATQ jusqu'à la fin du round. Si vous avez payé cette carte avec une ressource [physical], piochez 1 carte.",
  // raphael — Seething Rage (Resource)
  'tr007': "<b>Réponse</b> : après que vous avez dépensé cette carte, soignez 2 dégâts de Raphael et placez 1 compteur de rage sur lui (maximum 3).",
  // raphael — * Shell Cycle (Support)
  'tr008': "<b>Action de héros</b> : inclinez Shell Cycle et dépensez 2 ressources de n'importe quel type → redressez votre héros. Si vous avez payé cette capacité avec des ressources [physical][physical], vous gagnez +1 CTR jusqu'à la fin du round.",
  // raphael — * Raph's Punching Bag (Support)
  'tr009': "Raph gagne +2 REC.\n<b>Action d'alter ego</b> : inclinez Raph's Punching Bag et retirez tous les compteurs de rage de votre identité → piochez 1 carte pour chaque compteur de rage retiré de cette façon.",
  // raphael — Gekido (Upgrade)
  'tr010': "<b>Action de héros</b> : inclinez Gekido → choisissez :\n• Placez 1 compteur de rage sur Raphael.\n• Soignez 1 dégât de Raphael.",
  // raphael — * Raphael's Sai (Upgrade)
  'tr011': "Restreint.\nChaque amélioration [[SAI]] que vous contrôlez gagne : \"<b>Action de héros</b> <i>(attaque)</i> : inclinez cette carte et subissez 1 dégât → infligez 1 dégât à un ennemi.\"",
  // raphael — * Raphael's Other Sai (Upgrade)
  'tr012': "Restreint.\nChaque amélioration [[SAI]] que vous contrôlez gagne : \"<b>Réponse de héros</b> : après que Raphael met K.O. un ennemi, inclinez cette carte → piochez 1 carte.\"",
  // raphael — Out of Control (Obligation)
  'tr013': "<b><i>Donnez-la au joueur Raph.</i></b>\nPassez sous forme de héros et inclinez votre identité. Vous ne pouvez pas changer de forme, contrer ni vous défendre.\n<b>Action de héros</b> : retirez 2 compteurs de rage de Raphael → passez sous forme d'alter ego et défaussez Out of Control.",
  // raphael — Mutagen Bomb (SideScheme némésis)
  'tr014': "<i>Old Hobb a transformé le mutagène en bombes.</i>\n<b>Réponse forcée</b> : après la résolution de l'étape 1 de la phase du Méchant, placez 1 compteur de minuteur ici. Ensuite, s'il y a 2 compteurs de minuteur ou plus ici, défaussez cette carte et attribuez à chaque joueur 1 carte Rencontre face cachée.",
  // raphael — * Old Hob (Minion némésis)
  'tr015': "Ténacité. Coup Rapide.\n<i>(Sbire némésis de Raphael.)</i>",
  // raphael — Insurrection (Treachery némésis)
  'tr016': "<b>Une fois révélée</b> : défaussez 1 allié que vous contrôlez. Si vous ne pouvez pas, défaussez 1 carte de votre main.\n<hr />\n[star] <b>Boost</b> : défaussez 1 allié redressé que vous contrôlez.",
  // raphael — Prepare to Rally (Treachery némésis)
  'tr017': "<b>Une fois révélée</b> : défaussez 1 carte de votre main.\n<hr />\n[star] <b>Boost</b> : défaussez 1 carte de votre main.",
  // venus — * Venus (Hero)
  'tv001a': "<b>Action</b> : placez 1 compteur de dragage sur Venus pour chaque amélioration [[ELEMENT]] que vous contrôlez (maximum 6). <i>(Limite d'une fois par round.)</i>",
  // venus — * Bonnie (AlterEgo)
  'tv001b': "<b>Mise en place</b> : défaussez des cartes du dessus de votre deck jusqu'à défausser une amélioration [[ELEMENT]]. Mettez cette carte en jeu.\n<b>Action</b> : retirez 1 compteur de dragage de Bonnie → soignez 2 dégâts d'un personnage ami. <i>(Limite d'une fois par round.)</i>",
  // venus — * Bludgeon (Ally)
  'tv002': "<b>Réponse</b> : après que Bludgeon entre en jeu, placez 1 carte de votre défausse sur le dessus de votre deck.",
  // venus — Arc Nova (Event)
  'tv003': "<b>Action de héros</b> <i>(attaque)</i> : retirez X compteurs de dragage de Venus → infligez 4 dégâts à X ennemis.",
  // venus — Brain Burn (Event)
  'tv004': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance. Vous pouvez retirer 2 compteurs de dragage de Venus pour désorienter et sonner un ennemi.",
  // venus — Eldritch Lance (Event)
  'tv005': "<b>Action de héros</b> <i>(attaque)</i> : infligez 5 dégâts à un ennemi. Cette attaque gagne Déferlement. Piochez 1 carte pour chaque ressource [wild] utilisée pour payer cette carte.",
  // venus — Quantanucleic Acid (Event)
  'tv006': "<b>Action de héros</b> : donnez à Venus une carte d'état Tenace. Vous pouvez retirer 2 compteurs de dragage de Venus pour piocher 2 cartes.",
  // venus — Resistance (Event)
  'tv007': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous devriez subir des dégâts d'une attaque, prévenez tous les dégâts de cette attaque. Vous pouvez retirer 2 compteurs de dragage de Venus pour piocher 3 cartes.",
  // venus — * Arcane Emitting Diode (Upgrade)
  'tv009': "<b>Action de héros</b> <i>(attaque)</i> : inclinez cette carte et défaussez les 2 premières cartes de votre deck → infligez 2 dégâts à un ennemi.",
  // venus — * Cosmic Requiem (Upgrade)
  'tv010': "<b>Action de héros</b> : inclinez cette carte et retirez 2 compteurs de dragage de Venus → défaussez des cartes du dessus de votre deck jusqu'à défausser un événement. Ajoutez cette carte à votre main.",
  // venus — * Dragon Scale (Upgrade)
  'tv011': "<b>Ressource</b> : inclinez cette carte et retirez 1 compteur de dragage de Venus → générez une ressource [wild].",
  // venus — * Dream Weaver (Upgrade)
  'tv012': "<b>Action de héros</b> : inclinez cette carte et retirez 2 compteurs de dragage de Venus → défaussez des cartes du dessus de votre deck jusqu'à défausser un allié ou une amélioration. Ajoutez cette carte à votre main.",
  // venus — * Reanimator Engine (Upgrade)
  'tv013': "<b>Action de héros</b> : inclinez cette carte et retirez 2 compteurs de dragage de Venus → choisissez jusqu'à 2 cartes dans votre défausse et mélangez-les dans votre deck.",
  // venus — * Turtle Shell (Upgrade)
  'tv014': "<b>Action de héros</b> : inclinez cette carte et défaussez les 2 premières cartes de votre deck → redressez Venus.",
  // venus — Faulty Creation (Obligation)
  'tv015': "<b><i>Donnez-la au joueur Bonnie.</i></b>\nVous pouvez passer sous forme d'alter ego.\n<b>Action d'alter ego</b> : inclinez Bonnie → retirez Faulty Creation de la partie.",
  // venus — Jasper Barlow's Lab (SideScheme némésis)
  'tv016': "<i>Jasper Barlow a mené des expériences sur les habitants de Mutant Town.</i>\nEntrave 2[per_hero]. Incitation 2.",
  // venus — * Jasper Barlow (Minion némésis)
  'tv017': "<b>Une fois révélée</b> : placez une carte d'état Tenace sur chaque sbire engagé avec vous.\n<i>(Sbire némésis de Venus.)</i>\n<hr />\n[star] <b>Boost</b> : attribuez cette carte au premier joueur comme carte Rencontre face cachée.",
  // venus — * Groundchuck-Dirtbag (Minion némésis)
  'tv018': "Garde. Ténacité.\n<hr />\n[star] <b>Boost</b> : attribuez cette carte au premier joueur comme carte Rencontre face cachée.",
  // venus — Salvaged Scales (Treachery némésis)
  'tv019': "<b>Une fois révélée</b> : placez 2 menaces sur la manigance principale. Si Jasper Barlow est en jeu, placez une carte d'état Tenace sur le méchant et sur chaque sbire engagé avec vous.",
  // casey_jones — * Casey Jones (Hero)
  'tc001a': "<i>Overswing</i> — <b>Ressource</b> : défaussez une amélioration [[WEAPON]] que vous contrôlez ayant le mot-clé restreint → générez [wild][wild][wild] ressources pour un événement [[ATTACK]], [[THWART]] ou [[DEFENSE]]. <i>(Limite d'une fois par phase.)</i>",
  // casey_jones — * Casey Jones (AlterEgo)
  'tc001b': "<b>Mise en place</b> : cherchez l'amélioration Casey's Bag dans votre deck et votre défausse et mettez-la en jeu. <i>(Mélangez.)</i>\n<b>Réponse</b> : après que vous avez changé pour cette forme, remettez dans votre main une amélioration [[WEAPON]] de votre pile de défausse.",
  // casey_jones — Clap Back (Event, x2)
  'tc002': "<b>Action de héros</b> <i>(contre)</i> : retirez 5 menaces d'une manigance. Si une amélioration [[WEAPON]] de Casey Jones a été défaussée pour payer cette carte, désorientez un ennemi.",
  // casey_jones — Cross Block (Event, x2)
  'tc003': "<b>Interruption de héros</b> <i>(défense)</i> : quand vous vous défendez contre une attaque, vous gagnez +3 DEF pour cette attaque. Ensuite, redressez Casey Jones et donnez-lui une carte d'état Tenace.",
  // casey_jones — Face-Off (Event, x2)
  'tc004': "<b>Action de héros</b> <i>(attaque)</i> : redressez votre héros et infligez 3 dégâts à un ennemi. Cet ennemi vous attaque.",
  // casey_jones — Grand Slam (Event, x2)
  'tc005': "<b><i>Exigence</i></b> ([wild]). <i>(En payant cette carte, dépensez les ressources indiquées.)</i>\n<b>Action de héros</b> <i>(attaque)</i> : infligez 8 dégâts à un ennemi.",
  // casey_jones — Anything Goes (Upgrade)
  'tc006': "<b>Action de héros</b> : inclinez Anything Goes → échangez une amélioration [[WEAPON]] de Casey Jones que vous contrôlez avec une amélioration [[WEAPON]] de Casey Jones glissée sous Casey's Bag.",
  // casey_jones — Baseball Bat (Upgrade)
  'tc007': "Restreint.\n<b>Interruption de héros</b> : quand vous utilisez un pouvoir de base, inclinez Baseball Bat → vous gagnez +1 à ce pouvoir pour cette utilisation.",
  // casey_jones — * Casey's Mask (Upgrade)
  'tc008': "<b>Action de héros</b> : inclinez Casey's Mask → redressez Casey Jones.",
  // casey_jones — Cricket Willow (Upgrade)
  'tc009': "Restreint.\nVotre héros gagne +1 ATQ.\n<b>Réponse de héros</b> : après que vous avez attaqué un ennemi, défaussez Cricket Willow → sonnez cet ennemi.",
  // casey_jones — Driving Iron (Upgrade)
  'tc010': "Restreint.\n<b>Action de héros</b> : inclinez Driving Iron → infligez 1 dégât à un ennemi ou retirez 1 menace d'une manigance.",
  // casey_jones — Hockey Stick (Upgrade)
  'tc011': "Restreint.\n<b>Interruption de héros</b> : quand vous effectuez une attaque ou une défense de base, inclinez Hockey Stick → vous gagnez +2 à ce pouvoir pour cette utilisation.",
  // casey_jones — Persuader (Upgrade)
  'tc012': "Restreint.\nVotre héros gagne +1 ATQ.\n<b>Interruption de héros</b> : quand vous effectuez une attaque de base, inclinez Persuader → vous gagnez +1 ATQ pour cette attaque. Cette attaque gagne perçant.",
  // casey_jones — * Casey's Bag (Upgrade)
  'tc013': "Permanent.\nVous pouvez jouer les cartes glissées ici comme si elles étaient dans votre main.\n<b>Action de héros</b> : inclinez cette carte → glissez sous cette carte l'amélioration [[WEAPON]] la plus basse de votre pile de défausse.",
  // casey_jones — Daddy Issues (Obligation)
  'tc014': "<b><i>Donnez-la au joueur Casey Jones.</i></b>\nPassez sous forme d'alter ego. Vous ne pouvez pas changer de forme.\n<b>Action</b> : inclinez Casey Jones → retirez Daddy Issues de la partie.",
  // casey_jones_nemesis — The Purple Dragons (SideScheme némésis)
  'tc015': "<i>Hun et ses Purple Dragons font la loi dans ce quartier.</i>\nIncitation 1[per_hero].",
  // casey_jones_nemesis — * Hun (Minion némésis)
  'tc016': "Ténacité.\n<b>Réponse forcée</b> : après que Hun attaque et blesse un personnage, sonnez ce personnage.\n<i>(Sbire némésis de Casey Jones.)</i>",
  // casey_jones_nemesis — Purple Dragon Goons (Minion némésis, x3)
  'tc017': "Garde. Patrouille.\n<b>Une fois révélée</b> : placez une carte d'état Tenace sur le méchant.",
  // alopex — * Alopex (Hero)
  'ta001a': "<i>Matagi</i> — <b>Réponse forcée</b> : après avoir attaqué un ennemi ou contré une manigance, trouvez Prey et attachez-la à cet ennemi ou à cette manigance.",
  // alopex — * Alopex (AlterEgo)
  'ta001b': "<b>Mise en place</b> : mettez votre amélioration Prey de côté.\n<b>Action</b> : défaussez 1 carte de votre main → cherchez dans votre deck et votre défausse jusqu'à 2 améliorations [[KAMA]] et mettez-les en jeu, inclinées. <i>(Mélangez.)</i>",
  // alopex — * Nobody (Ally)
  'ta002': "[star] <b>Réponse</b> : après que Nobody a attaqué un ennemi portant Prey, hébétez cet ennemi.\n[star] <b>Réponse</b> : après que Nobody a contré une manigance portant Prey, camouflez-la.",
  // alopex — Bold Strategy (Event)
  'ta003': "<b>Action de héros</b> : camouflez Alopex. Vous pouvez dépenser jusqu'à 3 ressources [mental] pour hébéter un ennemi pour chaque ressource [mental] dépensée de cette façon.",
  // alopex — Pounce (Event)
  'ta004': "<b>Action de héros</b> <i>(attaque)</i> : infligez 1 dégât à un ennemi. Vous pouvez dépenser jusqu'à 2 ressources [mental] pour infliger 2 dégâts supplémentaires à cet ennemi pour chaque ressource [mental] dépensée de cette façon.",
  // alopex — Prowl (Event)
  'ta005': "<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Mélangez dans votre deck 1 carte portant une ressource [mental] imprimée de votre défausse.",
  // alopex — Sniff Out Trouble (Event)
  'ta006': "<b>Action de héros</b> : défaussez des cartes du deck Rencontre jusqu'à ce que vous défaussiez un sbire ou une manigance annexe. Révélez cette carte → piochez 2 cartes et redressez chaque amélioration [[KAMA]] que vous contrôlez.",
  // alopex — * Mutant Shelter (Support)
  'ta007': "Votre alter ego gagne +2 REC.\n<b>Action d'alter ego</b> : inclinez Mutant Shelter → mélangez dans votre deck l'allié le plus haut de votre pile de défausse.",
  // alopex — * Kitsune Kabuki (Upgrade)
  'ta008': "Chaque compteur de chasseur sur cette carte peut être dépensé comme s'il s'agissait d'une ressource [mental].\n<b>Réponse de héros</b> : après que Prey quitte le jeu, placez 1 compteur de chasseur ici.",
  // alopex — * Alopex's Kama (Upgrade)
  'ta009': "Restreint.\nChaque amélioration [[KAMA]] que vous contrôlez gagne : \"<b>Réponse de héros</b> : après que Prey quitte le jeu, inclinez cette carte et dépensez une ressource [mental] → redressez Alopex.\"",
  // alopex — * Alopex's Other Kama (Upgrade)
  'ta010': "Restreint.\nChaque amélioration [[KAMA]] que vous contrôlez gagne : \"<b>Action de héros</b> <i>(attaque/contre)</i> : inclinez cette carte → infligez 1 dégât à un ennemi ou retirez 1 menace d'une manigance.\"",
  // alopex — Prey (Upgrade)
  'ta011': "Les attaques d'Alopex infligent 1 dégât supplémentaire à l'ennemi attaché.\nLes contres d'Alopex retirent 1 menace supplémentaire de la manigance attachée.\n<b>Interruption forcée</b> : quand cette carte quitte le jeu, mettez-la de côté.",
  // alopex — Manipulated (Obligation)
  'ta012': "<b><i>Donnez-la au joueur Alopex.</i></b>\n<b>Action</b> : inclinez Alopex et infligez 1 dégât à chaque personnage que vous contrôlez → défaussez Manipulated.",
  // alopex — You Belong To Me (SideScheme némésis)
  'ta013': "<i>Kitsune a planté ses griffes dans Alopex, et elle n'a aucune intention de la lâcher...</i>\n<b>Une fois révélée</b> : chaque joueur défausse 1 carte de sa main.",
  // alopex — * Kitsune (Minion némésis)
  'ta014': "<b>Une fois révélée</b> : camouflez Kitsune et inclinez votre identité.\n<i>(Sbire némésis d'Alopex.)</i>",
  // alopex — Curse of Nine Tales (Treachery némésis)
  'ta015': "<b>Une fois révélée</b> : choisissez l'un ou l'autre :\n• Défaussez les 3 cartes du dessus de votre deck et placez 1 menace sur le complot principal pour chaque type de carte différent défaussé de cette façon.\n• Défaussez 2 alliés que vous contrôlez.",
  // jennika — * Jennika (Hero)
  'tj001a': "<i>Ninja Senpai</i> — <b>Interruption</b> : quand vous jouez une carte Shinobi, Jennika gagne +1 CTR, +1 ATQ et +1 DEF jusqu'à la fin du round. <i>(Limite d'une fois par round pour chaque Shinobi.)</i>",
  // jennika — * Jenny (AlterEgo)
  'tj001b': "<b>Mise en place</b> : mettez en jeu la Voie Sōsaiken sous votre contrôle.\n<b>Action</b> : défaussez 1 carte de votre main → cherchez dans votre deck et votre défausse jusqu'à 2 améliorations [[TEKKO-KAGI]] et mettez-les en jeu, inclinées. <i>(Mélangez.)</i>",
  // jennika — Composure (Event, x3)
  'tj002': "<b>Action</b> : choisissez une carte dans votre défausse → ajoutez cette carte à votre main.",
  // jennika — Apparition (Event, x2)
  'tj003': "<b>Action</b> <i>(contre)</i> : retirez 2 menaces d'une manigance et désorientez un ennemi.\n<i>(Cette carte est à la fois une carte Jennika et une carte Kuji-Kiri.)</i>",
  // jennika — Decisive Strike (Event, x2)
  'tj004': "<b>Action de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Si vous avez payé cette carte avec un événement [[ATTACK]], sonnez cet ennemi.\n<i>(Cette carte est à la fois une carte Jennika et une carte Taijutsu.)</i>",
  // jennika — Moonlighting (Event, x2)
  'tj005': "<b>Action de héros</b> : camouflez Jennika.\n<i>(Cette carte est à la fois une carte Jennika et une carte Ninjutsu.)</i>",
  // jennika — Fearless Resolve (Upgrade, x2)
  'tj006': "Utilisations (2 compteurs de samouraï).\n<b>Action de héros</b> : inclinez Fearless Resolve et retirez-en 2 compteurs de samouraï → redressez Jennika.\n<i>(Cette carte est à la fois une carte Jennika et une carte Bushido.)</i>",
  // jennika — * Jenny's Crib (Support)
  'tj007': "<b>Action d'alter ego</b> : inclinez Jenny's Crib et défaussez 1 carte de votre main → piochez 1 carte et redressez votre identité.",
  // jennika — * Jennika's Bow (Upgrade)
  'tj008': "Restreint.\n<b>Action de héros</b> : inclinez Jennika's Bow → infligez 1 dégât à un ennemi ou retirez 1 menace d'une manigance.\n<b>Réponse de héros</b> : après que vous avez joué un événement [[ATTACK]] ou [[THWART]], redressez Jennika's Bow.",
  // jennika — * Jennika's Tekko-Kagi (Upgrade)
  'tj009': "Chaque amélioration [[TEKKO-KAGI]] que vous contrôlez gagne : « <b>Ressource de héros</b> : inclinez cette carte → générez une ressource [wild] pour une carte Shinobi. »",
  // jennika — * Jennika's Other Tekko-Kagi (Upgrade)
  'tj010': "Chaque amélioration [[TEKKO-KAGI]] que vous contrôlez gagne : « <b>Interruption de héros</b> : quand vous faites une attaque de base, inclinez cette carte et défaussez 1 carte de votre main → Jennika gagne +2 ATQ pour cette attaque. Cette attaque gagne Perçant. »",
  // jennika — Sōsaiken (Support, type imprimé PATH)
  'tj011': "Permanent.\n<b>Réponse</b> : après que vous avez joué une carte Shinobi, inclinez cette carte → piochez 1 carte.",
  // jennika — Personality Adjustment (Obligation)
  'tj012': "<b><i>Donnez-la au joueur Jenny.</i></b>\nVous pouvez passer sous forme d'alter ego. Choisissez :\n• Inclinez Jenny → retirez Personality Adjustment de la partie.\n• Placez 3 menaces sur la manigance principale. Défaussez cette obligation.",
  // jennika_nemesis — Dun Import Exports (SideScheme némésis)
  'tj013': "<i>Le dangereux mafieux Darius Dun ouvre boutique. Il a envoyé ses Street Phantoms prendre le contrôle des ports de la ville.</i>\nEntrave 1[per_hero]. Incitation 2.",
  // jennika_nemesis — * Phantasm (Minion némésis)
  'tj014': "Riposte 1. Ténacité.\n<b>Une fois vaincu</b> : camouflez chaque sbire [[PHANTOMS]] en jeu.\n<i>(Sbire némésis de Jennika.)</i>",
  // jennika_nemesis — Street Phantoms (Minion némésis, x3)
  'tj015': "Ténacité.\n<b>Une fois révélée</b> : camouflez Street Phantoms.",
  // baxter_stockman — * Baxter Stockman I (Villain)
  'tx001': "Ténacité.\n<b>Interruption forcée</b> : quand la phase du Méchant commence, chaque joueur résout la capacité « <b>Spécial</b> » de la manigance Baxter's Laboratory.\n<i>« Je vais tous leur montrer... »</i>",
  // baxter_stockman — * Baxter Stockman II (Villain)
  'tx002': "Ténacité.\n<b>Une fois révélée</b> : cherchez dans le deck Rencontre et la défausse Rencontre l'attachement Baxter Blaster et révélez-le. <i>(Mélangez.)</i>\n<b>Interruption forcée</b> : quand la phase du Méchant commence, chaque joueur résout la capacité « <b>Spécial</b> » de la manigance Baxter's Laboratory.",
  // baxter_stockman — * Baxter Stockman III (Villain)
  'tx003': "Ténacité.\nChaque sbire [[SWARM]] gagne garde.\n<b>Une fois révélée</b> : distribuez 1 carte Rencontre face cachée à chaque joueur.\n<b>Interruption forcée</b> : quand la phase du Méchant commence, chaque joueur résout la capacité « <b>Spécial</b> » de la manigance Baxter's Laboratory.",
  // baxter_stockman — Baxter's Laboratory 1A (MainScheme)
  'tx004a': "<i>Baxter Stockman s'est affairé chez Stockgen sur ses nombreux automates et ses expériences de mutagène. La récente disparition du scientifique a déclenché de folles rumeurs. Que manigançait-il ?</i>\n<b>Contenu :</b> Baxter Stockman (I) et Baxter Stockman (II). <i>(Baxter Stockman (II) et Baxter (III) en mode expert.)</i> Sets Baxter's Lab, Cyber Swarm et Standard. Deux sets de rencontre modulaires <i>(High Speed et Security Protocol)</i>.\n<b>Mise en place</b> : mettez en jeu un sbire Plague of M.O.U.S.E.R.S. engagé avec chaque joueur.",
  // baxter_stockman — Baxter's Laboratory 1B (MainScheme)
  'tx004b': "<i>Réplication</i> — <b>Spécial</b> : placez 1 compteur polyvalent sur chaque sbire [[SWARM]] engagé avec vous. S'il n'y a aucun sbire [[SWARM]] engagé avec vous, distribuez-vous 1 carte Rencontre face cachée.\n<b>Si cette manigance est achevée, les joueurs perdent la partie.</b>",
  // baxter_stockman — * Baxter Blaster (Attachment)
  'tx005': "Attachez-le à Baxter Stockman.\n[star] <b>Réponse forcée</b> : après que Baxter Stockman attaque et blesse un personnage allié, hébétez-le.\n<b>Action de héros</b> : inclinez votre héros ou dépensez 2 ressources de n'importe quel type → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : attachez Baxter Blaster à Baxter Stockman.",
  // baxter_stockman — Swarm Superiority (Attachment, x2)
  'tx006': "Attachez-la à un sbire [[SWARM]]. Si vous ne pouvez pas, cette carte gagne Renfort.\nLe sbire attaché gagne [[AERIAL]] et garde.\n<b>Une fois révélée</b> : placez 2 compteurs polyvalents sur le sbire attaché.\n<i>« Il est difficile de rivaliser avec notre nombre. »</i> —Baxter Stockman",
  // baxter_stockman — Plague of M.O.U.S.E.R.S. (Minion, x4)
  'tx007': "Entre en jeu avec 2 compteurs d'essaim dessus.\n[star] La MNG, l'ATQ et les points de vie de ce sbire sont égaux au nombre de compteurs d'essaim qu'il porte.\n<b>Interruption forcée</b> : quand ce sbire subit des dégâts, retirez plutôt autant de compteurs d'essaim de cette carte.",
  // baxter_stockman — Radical Ingenuity (Treachery, x3)
  'tx008': "<b>Une fois révélée</b> : choisissez :\n• Résolvez la capacité « <b>Spécial</b> » de Baxter's Laboratory.\n• Placez 2 menaces sur la manigance principale.\n<i>« Essssayez donc de m'arrêteeeer. »</i> —Baxter Stockman",
  // baxter_stockman — Rapid Replication (Treachery, x3)
  'tx009': "<b>Une fois révélée</b> : défaussez des cartes du dessus du deck Rencontre jusqu'à ce qu'un sbire soit défaussé. Révélez ce sbire. Ensuite, résolvez la capacité « <b>Spécial</b> » de Baxter's Laboratory.\n<i>« Allez, mes sbires ! »</i> —Baxter Stockman",
  // baxter_stockman — Robotics Facility (SideScheme, x3)
  'tx010': "<i>L'usine automatisée tourne avec précision, sans supervision humaine. Insensible au conflit qui fait rage autour de l'installation.</i>\nEntrave 1[per_hero].",
  // baxter_stockman — Mad Lab (SideScheme, x2)
  'tx011': "<i>« Ils disaient que j'étais fou. Bientôt, ils comprendront. »</i> —Baxter Stockman\n<b>Interruption forcée</b> : quand la phase du Méchant commence, le premier joueur doit résoudre la capacité « <b>Spécial</b> » de Baxter's Laboratory.",
  // baxter_stockman (Cyber Swarm) — Flight of Flyborgs (Minion, x3)
  'tx012': "Entre en jeu avec 4 compteurs d'essaim dessus.\n[star] La MNG, l'ATQ et les points de vie de ce sbire sont égaux au nombre de compteurs d'essaim qu'il porte.\n<b>Interruption forcée</b> : quand ce sbire subit des dégâts, retirez plutôt autant de compteurs d'essaim de cette carte.",
  // baxter_stockman (Cyber Swarm) — * Superfly (Minion)
  'tx013': "Entre en jeu avec 2 compteurs de mutagène dessus.\n[star] La MNG et l'ATQ de ce sbire sont égales au nombre de compteurs de mutagène qu'il porte.\n<i>« Bzz bzz. »</i>",
  // baxter_stockman (Cyber Swarm) — Buzz Off (Treachery, x2)
  'tx014': "<b>Une fois révélée</b> : choisissez :\n• Placez 3 menaces sur la manigance principale.\n• Subissez 2 dégâts.\n<i>« Bzzzzzzzzzzzzzzzzzz. »</i>",
  // baxter_stockman (High Speed) — Roadkill Rodneys (Minion, x3)
  'tx015': "Entre en jeu avec 1 compteur de câble dessus.\nCoup Rapide.\n[star] Ce sbire gagne +1 ATQ par compteur de câble qu'il porte.\n[star] <b>Réponse forcée</b> : après que ce sbire attaque et blesse un personnage, hébétez ce personnage et retirez de cette carte chaque compteur de câble.",
  // baxter_stockman (High Speed) — Wrapped Up (Treachery, x2)
  'tx016': "<b>Une fois révélée</b> : hébétez un personnage allié. Si vous ne pouvez pas, cette carte gagne Renfort.\n<i>« Appréhendez ! Appréhendez ! »</i> —Roadkill Rodney",
  // baxter_stockman (Security Protocol) — Auto Defense Bots (Minion, x4)
  'tx017': "Garde. Patrouille.\nEntre en jeu avec 1 compteur de bouclier dessus.\n<b>Interruption forcée</b> : quand ce sbire va être vaincu, soignez tous les dégâts de ce sbire et retirez plutôt 1 compteur de bouclier de cette carte.",
  // baxter_stockman (Security Protocol) — Intruder Alert! (Attachment, x3)
  'tx018': "Attachez-la à votre identité.\n[[crisis]]\n<b>Action</b> : subissez 2 dégâts ou inclinez votre identité → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : révélez cette carte.",
  // shredder — * Shredder I (Villain)
  'ts001': "Shredder peut avoir jusqu'à 2 cartes d'état Camouflé.\n<b>Réponse forcée</b> : après la fin de la phase du Méchant, donnez une carte d'état Camouflé à Shredder.\n<i>« Cette ville est à moi ! »</i>",
  // shredder — * Shredder II (Villain)
  'ts002': "Shredder peut avoir jusqu'à 3 cartes d'état Camouflé.\n<b>Une fois révélé</b> : cherchez Bladed Armor (attachement) dans le deck Rencontre et la défausse Rencontre et révélez-la. <i>(Mélangez.)</i>\n<b>Réponse forcée</b> : après la fin de la phase du Méchant, donnez une carte d'état Camouflé à Shredder.",
  // shredder — * Shredder III (Villain)
  'ts003': "Shredder peut avoir jusqu'à 4 cartes d'état Camouflé.\n<b>Une fois révélé</b> : cherchez Kuro Kabuto (attachement) dans le deck Rencontre et la défausse Rencontre et révélez-le. <i>(Mélangez.)</i>\n<b>Réponse forcée</b> : après la fin de la phase du Méchant, donnez 2 cartes d'état Camouflé à Shredder.",
  // shredder — Clan of Shadows (MainScheme 1A)
  'ts004a': '<i>Le Foot Clan contrôle les rues de la ville.</i>\n<b>Contenu</b> : Shredder (I) et Shredder (II). <i>(Shredder (II) et Shredder (III) en mode expert.)</i> Ensembles Shredder, Shadow of the Foot et Standard. Deux ensembles de rencontre modulaires <i>(Chunin et Foot Goon Squad)</i>.\n<b>Mise en place</b> : chaque joueur cherche un sbire [[FOOT CLAN]] dans le deck Rencontre et le révèle.',
  // shredder — Clan of Shadows (MainScheme 1B)
  'ts004b': "<i>L'emprise de Shredder sur la ville dure depuis trop longtemps. Vous devez démanteler son réseau criminel.</i>\n<b>Une fois révélée</b> : camouflez Shredder.\n<b>Réponse forcée</b> : après qu'un sbire [[FOOT CLAN]] a été vaincu, placez 1 menace sur cette manigance.",
  // shredder — Shredder's Wrath (MainScheme 2A)
  'ts005a': "<i>Votre ingérence dans les affaires du Foot Clan a attiré la colère de Shredder.</i>\n<b>Une fois révélée</b> : dans l'ordre des joueurs, chaque joueur défausse 4 cartes du dessus du deck Rencontre et révèle le sbire [[FOOT CLAN]] le plus haut de la défausse Rencontre.",
  // shredder — Shredder's Wrath (MainScheme 2B)
  'ts005b': "<i>Shredder vous a maintenant dans sa ligne de mire.</i>\n<b>Une fois révélée</b> : donnez une carte d'état Tenace à chaque ennemi.\n<b>Réponse forcée</b> : après que Shredder manigance, donnez une carte d'état Camouflé à Shredder.\n<b>Si cette manigance est accomplie, les joueurs perdent la partie.</b>",
  // shredder — Bladed Armor (Attachment)
  'ts006': "Attachez-la à Shredder.\nShredder gagne Riposte 1.\n<b>Action de héros</b> : s'il n'y a aucune carte d'état Camouflé sur Shredder, subissez 1 dégât et dépensez 1 ressource de n'importe quel type → défaussez cette carte.\n<i>« Hé, regardez la râpe à fromage géante. »</i> —Raphael",
  // shredder — * Kuro Kabuto (Attachment)
  'ts007': 'Attachez-le à Shredder.\nShredder gagne Solide.\n<b>Réponse forcée</b> : après la fin de la phase du Méchant, camouflez Shredder.\n<b>Action de héros</b> : défaussez 2 cartes de votre main → défaussez cette carte.\n<hr />\n[star] <b>Boost</b> : attachez Kuro Kabuto à Shredder.',
  // shredder — Elite Guard (Minion)
  'ts008': "Garde. Patrouille.\n<b>Une fois révélé</b> : camouflez Shredder.\n<hr />\n[star] <b>Boost</b> : donnez une carte d'état Tenace à Shredder.",
  // shredder — Foot Ninja (Minion)
  'ts010': '<b>Une fois révélé</b> : camouflez Foot Ninja.\n<b>Interruption forcée</b> : quand Foot Ninja est vaincu, mélangez-le dans le deck Rencontre.\n<hr />\n[star] <b>Boost</b> : après la résolution de cette activation, camouflez le Méchant.',
  // shredder — * Mongo (Minion)
  'ts012': "Garde. Riposte 1.\n<hr />\n[star] <b>Boost</b> : sonnez votre héros.\n<i>« Qui aurait cru qu'un lutteur de sumo pouvait porter un masque de kabuki ? »</i> —Michelangelo",
  // shredder — Cloak of Shadows (Treachery)
  'ts013': "<b>Une fois révélée</b> : camouflez chaque ennemi. Si vous n'êtes engagé avec aucun sbire, révélez le sbire [[FOOT CLAN]] le plus haut de la défausse Rencontre.\n<hr />\n[star] <b>Boost</b> : après la résolution de cette activation, camouflez Shredder.",
  // shredder — Disarming Assault (Treachery)
  'ts015': '<b>Une fois révélée</b> : Shredder vous attaque. Ne donnez aucune carte de boost à Shredder pour cette activation. Si cette attaque inflige des dégâts à votre identité, défaussez une [[WEAPON]] que vous contrôlez.\n<hr />\n[star] <b>Boost</b> : défaussez une [[WEAPON]] que vous contrôlez.',
  // shredder — Shred (Treachery)
  'ts017': "<b>Une fois révélée (Alter ego)</b> : placez une carte d'état Camouflé sur Shredder.\n<b>Une fois révélée (Héros)</b> : Shredder vous attaque. Ne donnez aucune carte de boost à Shredder pour cette activation.\n<hr />\n[star] <b>Boost</b> : après la résolution de cette activation, camouflez Shredder.",
  // shredder — Foot Rikugun (SideScheme)
  'ts020': "<i>Le Foot Clan entraîne ses ninjas pour en faire des assassins implacables.</i>\n<b>Réponse forcée</b> : après qu'un sbire [[FOOT CLAN]] entre en jeu, camouflez-le. Si vous ne pouvez pas, donnez-lui une carte d'état Tenace.",
  // shredder — Throne of the Jōnin (SideScheme)
  'ts022': '<i>« Ce soir, je dînerai de soupe de tortue. »</i> —Shredder\n<b>Une fois révélée</b> : cherchez un attachement [[FOOT CLAN]] dans le deck Rencontre et la défausse Rencontre et révélez-le. <i>(Mélangez.)</i> Si vous ne pouvez pas, placez 2[per_hero] menaces sur cette manigance.',
  // chunin — * Karai (Minion)
  'ts101': '<b>Une fois révélée</b> : camouflez Karai.\n<b>Une fois vaincu</b> : camouflez le Méchant.\n<hr />\n[star] <b>Boost</b> : attribuez cette carte au premier joueur comme carte Rencontre face cachée.',
  // chunin — * Ocho (Minion)
  'ts102': "Garde.\n[star] Les attaques d'Ocho gagnent Perçant.\n<hr />\n[star] <b>Boost</b> : cherchez Karai dans le deck Rencontre et la défausse Rencontre et révélez-la. <i>(Mélangez.)</i>",
  // chunin — * Kira no Ken (Attachment)
  'ts103': "Attachez-le à Karai. Si Karai n'est pas en jeu, cherchez Karai dans le deck Rencontre et la défausse Rencontre et révélez-la. Ensuite, attachez cette carte à elle.\n[star] Les attaques du sbire attaché gagnent Perçant.\n<i>« Ma lame n'a pas d'égale. »</i> —Karai",
  // chunin — Doroppuin (Treachery)
  'ts104': "<b>Une fois révélée</b> : révélez le sbire le plus haut de la défausse Rencontre. Sinon, cette carte gagne Renfort.\n<hr />\n[star] <b>Boost</b> : si cette activation est une attaque, elle gagne Perçant.\n<i>« Essayez de suivre, s'il vous plaît. »</i> —Karai",
  // foot_goon_squad — * Bebop (Minion)
  'ts201': 'Ténacité.\n[star] Les attaques de Bebop gagnent Perçant.\n<hr />\n[star] <b>Boost</b> : si cette activation est une attaque, elle gagne Perçant. Sinon, attribuez cette carte au premier joueur comme carte Rencontre face cachée.',
  // foot_goon_squad — * Bludgeon (Minion)
  'ts202': 'Coup Rapide.\n<b>Réponse forcée</b> : après que Bludgeon attaque et blesse un personnage, inclinez ce personnage.\n<hr />\n[star] <b>Boost</b> : inclinez votre héros.',
  // foot_goon_squad — * Hun (Minion)
  'ts203': 'Ténacité.\n<b>Réponse forcée</b> : après que Hun attaque et blesse un personnage, sonnez ce personnage.\n<hr />\n[star] <b>Boost</b> : si cette activation inflige des dégâts à un personnage, sonnez ce personnage.',
  // foot_goon_squad — * Koya (Minion)
  'ts204': 'Incitation 1. Coup Rapide.\n<b>Une fois révélée</b> : soignez 2 dégâts du Méchant.\n<hr />\n[star] <b>Boost</b> : placez 1 menace sur la manigance principale et soignez 2 dégâts du Méchant.',
  // foot_goon_squad — * Rocksteady (Minion)
  'ts205': 'Solide. Coup Rapide.\n[star] Les attaques de Rocksteady gagnent Déferlement.\n<hr />\n[star] <b>Boost</b> : si cette activation est une attaque, elle gagne Déferlement. Sinon, attribuez cette carte au premier joueur comme carte Rencontre face cachée.',
  // foot_goon_squad — Send Out the Goons (SideScheme)
  'ts206': "<i>Les hommes de main de Shredder sont dans les rues et rackettent les habitants.</i>\n<b>Une fois révélée</b> : défaussez des cartes du dessus du deck Rencontre jusqu'à ce qu'un sbire [[BRUTE]] soit défaussé. Révélez ce sbire.",
  // shadow_of_the_foot — Foot Assassin (Minion)
  'ts301': "Coup Rapide.\n<b>Une fois révélé</b> : camouflez Foot Assassin.\n<b>Réponse forcée</b> : après que Foot Assassin attaque, camouflez-le.\n<i>« Tu t'appelles Edward ? »</i> —Michelangelo",
  // shadow_of_the_foot — Foot Soldiers (Minion)
  'ts303': '<b>Une fois révélé</b> : camouflez Foot Soldiers.\n<i>« Méfiez-vous des ombres de New York, mes fils. Elles ont de nombreuses lames. »</i> —Splinter',
  // shadow_of_the_foot — Foothold (SideScheme)
  'ts305': '<i>Le Foot Clan a pris solidement pied.</i>\nEntrave 1[per_hero]. Incitation 2.',
  // tmnt_standard — No Quarter (Treachery)
  'te001': "<b>Une fois révélée</b> : défaussez une amélioration ou un soutien que vous contrôlez. Si aucune carte n'a été défaussée ainsi, hébétez votre identité.\n<hr />\n[star] <b>Boost</b> : après la résolution de cette activation, hébétez votre identité.",
  // tmnt_standard — Outmatched (Treachery)
  'te002': 'Incitation 2.\n<b>Une fois révélée</b> : hébétez votre identité.\n<hr />\n[star] <b>Boost</b> : après la résolution de cette activation, hébétez votre identité.',
  // tmnt_standard — Pursued by Shadows (Treachery)
  'te004': "<b>Une fois révélée</b> : cherchez votre sbire némésis dans le deck Rencontre, la défausse Rencontre et la zone mise de côté et révélez-le. <i>(Mélangez.)</i> Camouflez votre sbire némésis. Si votre sbire némésis n'est pas entré en jeu ainsi, cette carte gagne Renfort.",
  // tmnt_standard — Shadow of the Past (Treachery)
  'te005': "<b>Une fois révélée</b> : révélez votre sbire némésis mis de côté et mettez-le en jeu engagé avec vous. Révélez votre manigance annexe némésis mise de côté et mettez-la en jeu. Mélangez le reste de votre ensemble de rencontre némésis mis de côté dans le deck Rencontre. Si votre sbire némésis n'entre pas en jeu ainsi, cette carte gagne Renfort.",
  // tmnt_standard — Skulk (Treachery)
  'te006': '<b>Une fois révélée</b> : subissez 2 dégâts indirects et camouflez le Méchant.\n<hr />\n[star] <b>Boost</b> : attribuez cette carte au premier joueur comme carte Rencontre face cachée.',
  // tmnt_expert — Annihilation (Treachery)
  'te101': '<b>Une fois révélée</b> : le Méchant vous attaque. Cette attaque gagne Déferlement.\n<hr />\n[star] <b>Boost</b> : si le Méchant attaque, cette attaque gagne Déferlement.',
  // tmnt_expert — Haunted by the Past (Treachery)
  'te102': "<b>Une fois révélée</b> : cherchez votre sbire némésis dans le deck Rencontre, la défausse Rencontre et la zone mise de côté et mettez-le en jeu engagé avec vous. <i>(Mélangez.)</i> Si votre sbire némésis n'est pas entré en jeu ainsi, inclinez votre identité et cette carte gagne Renfort.",
  // tmnt_expert — Sinister Plan (Treachery)
  'te103': "<b>Une fois révélée</b> : cherchez votre manigance annexe némésis dans le deck Rencontre, la défausse Rencontre et la zone mise de côté et révélez-la. <i>(Mélangez.)</i> Hébétez votre identité. Si votre manigance annexe némésis n'est pas entrée en jeu ainsi, cette carte gagne Renfort.",
  // tmnt_aspect_aggression — Bo-Wing (Ally), reskin de 53035 Winter Soldier
  'ua006': "<b>Réponse</b> : après que Bo-Wing a attaqué et vaincu un ennemi, retirez 2 menaces d'une manigance.\n<i>« Tant que je serai en vie, tu m'auras sur le dos. »</i>",
  // tmnt_aspect_aggression — Demolish (Event) ; « Rampage » : mot-clé maison laissé en anglais, comme Cloak
  'ua015': "[star] Rampage 3. <i>(Coût additionnel pour jouer cette carte : subissez 3 dégâts et défaussez les 3 cartes du dessus de votre deck.)</i>\n<b>Action de héros</b> <i>(attaque)</i> : infligez 8 dégâts à un ennemi. Si vous contrôlez un soutien [[NYC]], cette attaque gagne Déferlement et Perçant.",
  // tmnt_intense — Intense Combatants (Environment)
  'te201': "<i>Ensembles TMNT Standard et Expert uniquement. (Environnement optionnel pour ceux qui veulent plus de rebondissements.)</i>\nPermanent. Mise en place.\n<b>Interruption forcée</b> : quand une carte d'état devrait être placée sur un personnage, si ce personnage a déjà 1 exemplaire de cette carte d'état, intensifiez ce personnage à la place.",

  // --- TMNT Aggression (ua) : ajouter les cartes uaNNN ci-dessous, dans ce bloc seulement ---
  // tmnt_aspect_aggression — Apex Predator (Event) ; « Rampage » : mot-clé maison laissé en anglais
  'ua002': "[star] Rampage 2. <i>(Coût additionnel pour jouer cette carte : subissez 2 dégâts et défaussez les 2 cartes du dessus de votre deck.)</i>\n<b>Action de héros</b> <i>(attaque)</i> : choisissez :\n• infligez 4 dégâts à un ennemi ;\n• sonnez un ennemi.",
  // tmnt_aspect_aggression — Assassin (Ally)
  'ua003': "[star] Assassin subit 1 dégât consécutif ([consequential]) de moins après avoir attaqué le Méchant ou un sbire [[ÉLITE]].\n<i>« Je fais ce qui doit être fait. »</i>",
  // tmnt_aspect_aggression — Attack Training (Upgrade), MODIFIÉE de 32043
  'ua004': "Attachez cette carte à un allié [[NINJA]] ou [[MUTANIMAL]]. 1 amélioration [[ENTRAÎNEMENT]] max par allié.\nL'allié attaché gagne +1 ATQ et +2 points de vie.\n<i>« Suivez le rythme, les gars ! »</i> —Uno",
  // tmnt_aspect_aggression — Chain Reaction (Event)
  'ua008': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Si cet ennemi est vaincu, infligez 2 dégâts à un deuxième ennemi. Si cet ennemi est vaincu, infligez 3 dégâts à un troisième ennemi.\n<i>« Encore un qui mord la poussière. »</i> —Michelangelo",
  // tmnt_aspect_aggression — Combo Move (Event)
  'ua011': "<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts répartis entre les ennemis en jeu (3 dégâts à la place si votre identité a le trait [[ARTISTE MARTIAL]]).\n<i>« Qu'est-ce que tu dis de ça ? »</i> —Donatello",
  // tmnt_aspect_aggression — Commando (Ally)
  'ua012': "<b>Réponse</b> : après que Commando est entré en jeu, défaussez un événement de votre main → sonnez un ennemi.\n<i>« Chargez les armes, les gars. »</i>",
  // tmnt_aspect_aggression — Critical Wound (Upgrade)
  'ua013': "Attachez cette carte à un sbire que votre héros a attaqué ce tour-ci. Si elle est attachée à un sbire non-[[ÉLITE]], il gagne Vulnérable.\nAugmentez de 1 la quantité de dégâts que le sbire attaché subit de chaque attaque.",
  // tmnt_aspect_aggression — Daitō (Upgrade)
  'ua014': "Attachez cette carte à un personnage allié. Tant qu'elle est attachée à une identité, cette carte gagne Restreint.\n<b>Interruption</b> : quand le personnage attaché attaque un ennemi, inclinez Daitō → cette attaque inflige 1 dégât supplémentaire et gagne Perçant.",
  // tmnt_aspect_aggression — Flow of Battle (Upgrade) ; « Prerequisite » : question Q-UA1
  'ua019': "Prérequis ([[ARTISTE MARTIAL]]).\n1 max par joueur.\n<b>Réponse de héros</b> : après que vous avez attaqué et vaincu exactement un ennemi, défaussez cette carte → piochez 3 cartes.\n<i>« Trouve la paix dans le chaos. »</i> —Leonardo",
  // tmnt_aspect_aggression — Guerilla Trap (Upgrade)
  'ua021': "Réduisez de 1 le coût pour jouer cette carte si vous contrôlez un soutien [[NYC]].\n<b>Réponse de héros</b> : après qu'un sbire vous a engagé, défaussez Guerilla Trap → hébétez ce sbire et camouflez votre héros.",
  // tmnt_aspect_aggression — Kitsune (Ally)
  'ua025': "<b>Réponse</b> : après que vous avez joué Kitsune depuis votre main, choisissez :\n• camouflez Kitsune ;\n• hébétez un ennemi.\n<i>« Non. C'est une autre Kitsune... »</i>",
  // tmnt_aspect_aggression — Leatherhead (Ally)
  'ua026': "<b>Réponse</b> : après que Leatherhead a attaqué et vaincu un sbire, soignez-lui 2 dégâts.\n<i>« Nous ne sommes pas amis. Tu n'es qu'un moyen d'arriver à mes fins. »</i>",
  // tmnt_aspect_aggression — Nerve Strike (Event)
  'ua030': "[star] Remise 1 ([[ARTISTE MARTIAL]]).\n<b>Action de héros</b> <i>(attaque)</i> : infligez 2 dégâts à un ennemi. Sonnez ou désorientez cet ennemi.\n<i>« On dirait que j'ai touché un nerf. »</i> —Nobody",
  // tmnt_aspect_aggression — Pete (Support) ; question Q-UA3
  'ua033': "Utilisations (3 compteurs pistolet).\n<b>Réponse</b> : après que vous avez infligé des dégâts à un ennemi, inclinez Pete et retirez-lui 1 compteur pistolet → infligez 1 dégât à cet ennemi.\n<i>« Salut, moi c'est Pete ! »</i>",
  // tmnt_aspect_aggression — Ray Fillet (Ally)
  'ua036': "Ray Fillet entre en jeu avec 2 compteurs munitions.\n[star] <b>Interruption</b> : quand Ray Fillet utilise un pouvoir de base, retirez-lui 1 compteur munitions → infligez 2 dégâts à un ennemi.",
  // tmnt_aspect_aggression — Slash (Ally) ; question Q-UA2
  'ua037': "<b>Réponse forcée</b> : après que Slash est entré en jeu, subissez 3 dégâts.\n<i>« Raaaarrrrr ! »</i>",
  // tmnt_aspect_aggression — Ujigami (Ally), bandeau ✦ Shang-Chi
  'ua040': "Ujigami entre en jeu avec 10 compteurs dague.\n<b>Action</b> : retirez 1 compteur dague d'ici → infligez 1 dégât à un ennemi. (Limite deux fois par round.)\n<i>« Je suis ta mort ! »</i>",
  // tmnt_aspect_aggression — Yagi & Gorogoro (Ally)
  'ua041': "[star] Les attaques de Yagi & Gorogoro gagnent Perçant.\n[star] <b>Réponse forcée</b> : après que Yagi & Gorogoro ont effectué une attaque de base, choisissez soit de défausser 2 cartes de votre main, soit de retirer Yagi & Gorogoro de la partie.",
  // tmnt_aspect_aggression — Exeen (Ally), reskin de 18011 Angela (bandeau ✦ Angela)
  'ua017': "<b>Réponse forcée</b> : après qu'Exeen est entrée en jeu sous votre contrôle, cherchez un sbire parmi les 10 cartes du dessus du deck Rencontre et mettez-le en jeu engagé avec vous. Mélangez le deck Rencontre. Si aucun sbire n'a été mis en jeu par cet effet, défaussez Exeen.",
  // tmnt_aspect_aggression — Firepower (Event), reskin de 54014
  'ua018': "<b>Action de héros</b> <i>(attaque)</i> : inclinez jusqu'à 3 améliorations [[ARME]] que vous contrôlez → pour chaque amélioration ainsi inclinée, choisissez un ennemi et infligez-lui 3 dégâts. Cette attaque gagne À Distance.",
  // tmnt_aspect_aggression — He-Dude (Ally), reskin de 56010 Two-Gun Kid (bandeau ✦ Two-Gun Kid)
  'ua022': "[star] <b>Interruption</b> : quand He-Dude effectue une attaque de base, choisissez 2 ennemis à la place de 1 et résolvez cette attaque contre chacun d'eux.\n<i>« Allez muchachos, dites-moi quand. »</i>",
  // tmnt_aspect_aggression — Rave (Ally), reskin de 16040 Bug (bandeau ✦ Bug)
  'ua035': "<b>Réponse de héros</b> : après que votre héros a effectué une attaque de base, soignez 1 dégât de Rave.\n<i>« La Nova Posse ne bat pas en retraite. On change juste de voie. »</i>",


  // --- TMNT Basic (ub) : ajouter les cartes ubNNN ci-dessous, dans ce bloc seulement ---
  // tmnt_aspect_basic — April O'Neil (Ally), reskin de 01084 Nick Fury
  'ub001': "<b>Réponse forcée</b> : après qu'April O'Neil est entrée en jeu, choisissez une option : retirez 2 menaces d'une manigance, piochez 3 cartes ou infligez 4 dégâts à un ennemi. À la fin du round, si April O'Neil est toujours en jeu, défaussez-la.",
  // tmnt_aspect_basic — Assess the Situation (Event), reskin de 12033
  'ub002': "<b>Action</b> : votre taille de main augmente de +1 jusqu'à la fin de la phase.\n<i>« Vous en pensez quoi, les gars ? C'est le moment d'entrer dans la bagarre ? »</i> —Raphael",
  // tmnt_aspect_basic — Atilla (Ally), 13019 modifiée (Réponse FORCÉE)
  'ub003': "<b>Réponse forcée</b> : après avoir joué Atilla de votre main, choisissez CTR ou ATQ. Atilla gagne +2 au pouvoir choisi jusqu'à la fin de la phase.\n<i>« Cet endroit nous appartient ! »</i>",
  // tmnt_aspect_basic — Casey Jones (Ally)
  'ub005': "<b>Réponse</b> : après que Casey Jones est entré en jeu, cherchez une amélioration [[ARME]] dans votre deck et votre pile de défausse et ajoutez-la à votre main. <i>(Mélangez.)</i>\n<i>« C'est l'heure de dégager, les gros bras. »</i>",
  // tmnt_aspect_basic — Clyde (Ally), reskin de 13018 Ironheart
  'ub006': "<b>Réponse</b> : après avoir joué Clyde de votre main, piochez 1 carte.\n<i>« On touche au marais, on goûte à la langue. »</i>",
  // tmnt_aspect_basic — Donatello (Ally)
  'ub008': "<b>Réponse</b> : après que Donatello est entré en jeu, piochez 2 cartes.\n<i>« Avant de foncer, on élabore une stratégie. »</i>",
  // tmnt_aspect_basic — Energy (Resource), reskin de 01088
  'ub011': "1 max par deck.",
  // tmnt_aspect_basic — E.P.F. R.N.D. (Support), reskin de 35022 Weapon X
  'ub012': "Jouez cette carte uniquement si votre identité a le trait [[MUTANT]].\n<b>Action d'alter ego</b> : inclinez E.P.F. R.N.D. et subissez 1 dégât → défaussez des cartes de votre deck jusqu'à ce que vous défaussiez une carte spécifique à l'identité, puis ajoutez cette carte à votre main.",
  // tmnt_aspect_basic — Fugitoid (Ally)
  'ub014': "[star] <b>Réponse</b> : après que Fugitoid a utilisé un pouvoir de base, défaussez 1 carte de votre main. Si la ressource imprimée de cette carte comporte :\n[physical] - Soignez 2 dégâts d'un personnage ami.\n[mental] - Retirez 2 menaces d'une manigance.\n[energy] - Infligez 2 dégâts à un ennemi.\n[wild] - Piochez 1 carte.",
  // tmnt_aspect_basic — Genghis (Ally), reskin de 40057 White Fox
  'ub015': "<b>Réponse</b> : après que Genghis a été défaussé du dessus de votre deck, mettez-le en jeu sous votre contrôle.\n<i>« Quand on bondit, on conquiert. »</i>",
  // tmnt_aspect_basic — Genius (Resource), reskin de 01089
  'ub016': "1 max par deck.",
  // tmnt_aspect_basic — Gofu Talisman (Upgrade), reskin de 45050 Bloodgem
  'ub017': "Jouez cette carte uniquement si vous avez le trait [[MYSTIQUE]]. 1 max par deck.\n<b>Ressource</b> : inclinez le Talisman Gofu et subissez 2 dégâts → générez une ressource [wild].",
  // tmnt_aspect_basic — Herold Lilja's Lab (Support), 34022 Cerebro modifiée
  'ub018': "Jouez cette carte uniquement si votre identité a le trait [[MUTANT]].\n<b>Action d'alter ego</b> : inclinez cette carte → cherchez un allié [[DIMENSION X]], [[NINJA]] ou [[MUTANIMAL]] dans les 5 cartes du dessus de votre deck (cherchez dans l'intégralité de votre deck si vous contrôlez un personnage [[TEMPOREL]]) et ajoutez cet allié à votre main. <i>(Mélangez.)</i>",
  // tmnt_aspect_basic — Honorable Blades (Event)
  'ub019': "En Équipe (Leonardo et Usagi Yōjimbō). 1 max par deck.\n<b>Action de héros</b> : redressez Leonardo et Usagi Yōjimbō. Camouflez Leonardo. Donnez une carte d'état Tenace à Usagi Yōjimbō.",
  // tmnt_aspect_basic — Improvised Club (Upgrade)
  'ub020': "Attachez cette carte à un allié. 1 max par allié.\n<b>Réponse</b> : après que l'allié attaché a attaqué et blessé un sbire, défaussez Improvised Club → sonnez ce sbire.\n<i>« Tu veux entrer dans mon club ? »</i> —Casey Jones",
  // tmnt_aspect_basic — Ingenuity (Upgrade), reskin de 29027
  'ub021': "Jouez cette carte uniquement si votre identité a le trait [[GÉNIE]]. 1 max par joueur.\n<b>Ressource</b> : inclinez Inventivité → générez une ressource [mental].",
  // tmnt_aspect_basic — Jennika (Ally)
  'ub022': "<b>Réponse</b> : après que Jennika est entrée en jeu, placez une carte Shinobi <i>(noire)</i> de votre pile de défausse sur le dessus de votre deck.\n<i>« Je sais me débrouiller. »</i>",
  // tmnt_aspect_basic — Katsuichi (Ally)
  'ub023': "<b>Réponse</b> : après que Katsuichi est entré en jeu, cherchez une carte spécifique à l'identité dans votre deck et ajoutez-la à votre main. <i>(Mélangez.)</i>\n<i>« Vide ton esprit, mais jamais ton cœur. »</i>",
  // tmnt_aspect_basic — The Kennel Klub (Support), 33020 Utopia modifiée
  'ub024': "Si chacun de vos alliés a le trait [[MUTANIMAL]] ou [[NINJA]], augmentez de 1 votre limite d'alliés.\n<b>Réponse</b> : après qu'un allié [[MUTANIMAL]] ou [[NINJA]] est entré en jeu, inclinez The Kennel Klub → redressez un personnage [[MUTANIMAL]] ou [[NINJA]].",
  // tmnt_aspect_basic — Leonardo (Ally)
  'ub025': "[star] <b>Réponse</b> : après que Leonardo a utilisé un pouvoir de base, redressez un autre allié [[NINJA]] que vous contrôlez.\n<i>« Suivez-moi. »</i>",
  // tmnt_aspect_basic — Martial Arts Training (Upgrade) ; « Starting » : mot-clé laissé tel quel
  'ub027': "Starting. <i>(Vous pouvez ajouter cette carte à votre main avant de piocher votre main de départ.)</i>\nVotre héros gagne le trait [[ARTISTE MARTIAL]].",
  // tmnt_aspect_basic — Mary (Ally), reskin de 01083 Mockingbird
  'ub028': "<b>Réponse</b> : après que Mary est entrée en jeu, sonnez un ennemi.\n<i>« Tu oses douter de moi ? Laisse-moi te faire la leçon à la Tudor. »</i>",
  // tmnt_aspect_basic — Michelangelo (Ally)
  'ub029': "<b>Réponse</b> : après que Michelangelo est entré en jeu, soignez 2 dégâts d'un personnage ami.\n<i>« Je couvre tes arrières. »</i>",
  // tmnt_aspect_basic — Multitalented (Event), reskin de 47021
  'ub030': "<b>Action de héros</b> <i>(attaque/contre)</i> : si vous avez payé cet événement en utilisant au moins 1 :\n[physical] - Infligez 2 dégâts à un ennemi.\n[mental] - Retirez 2 menaces d'une manigance.\n[energy] - Soignez 2 dégâts de votre identité.",
  // tmnt_aspect_basic — Mutagen (Upgrade), reskin de 38019 X-Gene
  'ub031': "Jouez cette carte uniquement si votre identité a le trait [[MUTANT]]. 1 max par joueur.\n<b>Ressource</b> : inclinez Mutagen → générez une ressource [wild] pour un événement spécifique à votre identité.",
  // tmnt_aspect_basic — Mutanimal Van (Support), 41022 IPAC modifiée
  'ub032': "Jouez cette carte uniquement si votre identité a le trait [[MUTANIMAL]].\n<b>Action de héros</b> : inclinez Mutanimal Van et attribuez 1 carte Rencontre face cachée à un joueur → ce joueur pioche 2 cartes.",
  // tmnt_aspect_basic — Ninja He-Man (Ally)
  'ub033': "Jouez cette carte uniquement si vous contrôlez une carte [[NINJA]] ou [[GUERRIER]].\nTénacité.\n<b>Réponse</b> : après que Ninja He-Man est entré en jeu, camouflez-le.",
  // tmnt_aspect_basic — Onmyōdō Saikō (Upgrade), reskin de 09026 The Sorcerer Supreme
  'ub034': "Jouez cette carte uniquement si vous avez le trait [[MYSTIQUE]].\nVotre taille de main augmente de +1 tant que vous êtes sous forme de héros.\n<i>« L'équilibre de toute chose doit être protégé des sombres agents du chaos. »</i> —Splinter",
  // tmnt_aspect_basic — Party Time (Event), reskin de 33022 Game Time
  'ub035': "<b>Action de héros</b> : choisissez un allié auquel est attachée une amélioration [[ENTRAÎNEMENT]] → redressez cet allié et soignez-le de 1 dégât.\n<i>« Bon, les gars, vous savez quelle heure il est ! »</i> —Michelangelo",
  // tmnt_aspect_basic — Party Wagon (Support), 32020 The X-Jet modifiée
  'ub036': "<b>Ressource</b> : inclinez Party Wagon → générez une ressource [wild] pour un joueur dont l'identité a le trait [[NINJA]] ou [[TORTUE]].\n<i>« Il est où, le lance-pizzas ? »</i> —Michelangelo",
  // tmnt_aspect_basic — Pepperoni (Support) ; jetons « pep » laissés tels quels
  'ub037': "Utilisations (3 jetons pep).\n<b>Réponse</b> : après que vous avez vaincu un ennemi ou retiré la dernière menace d'une manigance, inclinez Pepperoni et retirez-lui 1 jeton pep → votre taille de main augmente de +1 jusqu'à la fin de la phase.",
  // tmnt_aspect_basic — Pizza Time (Event), 37021 Mutant Education modifiée
  'ub038': "Jouez cette carte uniquement si votre identité a le trait [[MUTANT]].\n<b>Action d'alter ego</b> : choisissez dans votre pile de défausse jusqu'à 2 cartes spécifiques à l'identité et mélangez-les dans votre deck. Si Rupert's Pizzeria est en jeu, piochez 1 carte.",
  // tmnt_aspect_basic — Press and Protect (Event)
  'ub040': "En Équipe (April O'Neil et Casey Jones). 1 max par deck.\n<b>Action</b> : retirez 3 menaces d'une manigance et donnez une carte d'état Tenace à un personnage ami.",
  // tmnt_aspect_basic — Raphael (Ally)
  'ub041': "[star] Raphael gagne +1 ATQ pour chaque jeton de dégât sur lui (+2 ATQ au maximum).\n<i>« Lâche-moi un peu. »</i>",
  // tmnt_aspect_basic — Ready to Rumble (Upgrade), reskin de 21022
  'ub042': "Jouez cette carte sous le contrôle de n'importe quel joueur. 1 max par joueur.\n<b>Réponse de héros</b> : après que vous avez changé de forme, défaussez cette carte → redressez votre héros.\n<i>« Bon, c'est quoi la suite ? »</i> —Mondo Gecko",
  // tmnt_aspect_basic — Rupert's Pizzeria (Support), 32049 X-Mansion modifiée
  'ub043': "<b>Action d'alter ego</b> : inclinez Rupert's Pizzeria → soignez 1 dégât d'un personnage [[MUTANT]], [[MUTANIMAL]] ou [[NINJA]]. N'importe quel joueur dont l'alter ego a le trait [[MUTANT]] peut déclencher cette capacité.\n<i>« La meilleure part de la ville ! »</i> —Mikey",
  // tmnt_aspect_basic — Shell Phone (Upgrade), reskin de 47019 Cell Phone
  'ub044': "Utilisations (3 jetons Charge).\n<b>Action</b> : inclinez le Shell Phone, retirez-lui 1 jeton Charge et choisissez un joueur → ce joueur effectue une attaque ou un contre de base avec un personnage qu'il contrôle. Ce personnage gagne +1 CTR et +1 ATQ pour cette utilisation.",
  // tmnt_aspect_basic — Shinobi Batman (Ally)
  'ub045': "Jouez cette carte uniquement si vous contrôlez une carte [[NINJA]] ou [[JUSTICIER]].\n<b>Réponse</b> : après que Shinobi Batman a quitté le jeu, cherchez une carte [[NINJA]] ou [[JUSTICIER]] dans votre deck et ajoutez-la à votre main. <i>(Mélangez.)</i>",
  // tmnt_aspect_basic — Shuriken (Upgrade)
  'ub046': "Attachez cette carte à un personnage ami. 1 max par personnage.\n<b>Action de héros</b> : inclinez cette carte et défaussez 1 carte de votre main → infligez 1 dégât à jusqu'à 3 ennemis.",
  // tmnt_aspect_basic — Sky Wagon (Support), reskin de 01092 Helicarrier
  'ub047': "1 max par joueur.\n<b>Action</b> : inclinez le Sky Wagon → choisissez un joueur. Réduisez de 1 le coût en ressources de la prochaine carte jouée par ce joueur à cette phase.\n<i>« Un van volant ? Un dirigeable serait plus discret... »</i> —Raphael",
  // tmnt_aspect_basic — Slash (Ally), reskin de 62020 Hulk
  'ub048': "Slash gagne +1 ATQ pour chaque jeton Rage sur lui.\n<b>Réponse</b> : après que le méchant vous a attaqué, placez 1 jeton Rage sur cet allié.\n<i>« Sentez ma rage ! »</i>",
  // tmnt_aspect_basic — Snow and Shadow (Event)
  'ub049': "En Équipe (Alopex et Nobody). 1 max par deck.\n<b>Action de héros</b> : redressez Alopex et Nobody. Camouflez un personnage ami. Hébétez un ennemi.",
  // tmnt_aspect_basic — "Special Delivery!" (Event), 37031 X-Men Instruction modifiée
  'ub050': "Jouez cette carte uniquement si votre identité a le trait [[MUTANT]].\n<b>Action d'alter ego</b> : choisissez dans votre pile de défausse jusqu'à 2 alliés ayant le trait [[DIMENSION X]], [[MUTANIMAL]] ou [[NINJA]] et mélangez-les dans votre deck. Si Rupert's Pizzeria est en jeu, piochez 1 carte.",
  // tmnt_aspect_basic — Splinter Dojo (Support), 33021 Danger Room modifiée
  'ub052': "<b>Réponse d'alter ego</b> : après qu'un allié [[MUTANIMAL]] ou [[NINJA]] est entré en jeu, inclinez Splinter Dojo → cherchez une amélioration [[ENTRAÎNEMENT]] dans votre deck et votre pile de défausse et attachez-la à cet allié. N'importe quel joueur dont l'alter ego a le trait [[MUTANT]] peut déclencher cette capacité.",
  // tmnt_aspect_basic — Splinter (Support), reskin de 60029 Stick
  'ub053': "<b>Interruption</b> : quand un personnage [[ARTISTE MARTIAL]] ami utilise un pouvoir de base, choisissez :\n• Inclinez Splinter → ce personnage a +1 à ce pouvoir de base pour cette utilisation.\n• Ce personnage a -1 à ce pouvoir de base pour cette utilisation. Redressez Splinter.",
  // tmnt_aspect_basic — Strength (Resource), reskin de 01090
  'ub054': "1 max par deck.",
  // tmnt_aspect_basic — Team-Building Exercise (Support), reskin de 12024
  'ub055': "<b>Action de héros</b> : inclinez Team-Building Exercise → jouez une carte de votre main qui partage un trait avec votre héros, en réduisant de 1 son coût en ressources.\n<i>« C'est l'équipe de combat la plus redoutable du monde. »</i>",
  // tmnt_aspect_basic — The Market (Support), reskin de 41023 X-Bunker
  'ub056': "<b>Action</b> : inclinez The Market et choisissez un joueur dont l'identité a le trait [[MUTANT]] → ce joueur cherche une carte parmi les X cartes du dessus de son deck et l'ajoute à sa main, X étant le nombre de manigances annexes dans la pile de victoire. <i>(Mélangez.)</i>",
  // tmnt_aspect_basic — Turtle Lair (Support), reskin de 01091 Avengers Mansion
  'ub057': "1 max par joueur.\n<b>Action</b> : inclinez le Turtle Lair → choisissez un joueur. Ce joueur pioche 1 carte.\n<i>« Ça fait du bien d'être à la maison. »</i> —Mikey",
  // tmnt_aspect_basic — Upstate Farmhouse (Support), reskin de 20029 Crew Quarters
  'ub058': "Jouez cette carte sous le contrôle de n'importe quel joueur. 1 max par joueur.\n<b>Action d'alter ego</b> : inclinez Upstate Farmhouse → soignez 1 dégât d'un alter ego.",
  // tmnt_aspect_basic — Weapon Harness (Upgrade), 20021 Side Holster modifiée
  'ub059': "1 max par joueur. Jouez cette carte uniquement si votre identité a le trait [[NINJA]].\nVous pouvez contrôler 2 améliorations [[ARME]] supplémentaires dotées du mot-clé Restreint.",


  // --- TMNT Justice (uj) : ajouter les cartes ujNNN ci-dessous, dans ce bloc seulement ---
  // Reskins : texte de textes-fr-complets[<officielle>], nom remplace, citation ajoutee. Nouvelles : traduction.
  'uj002': "Attachez cette carte à une manigance annexe. 1 max par manigance.\n<b>Interruption</b> : quand la manigance annexe attachée est déjouée, cherchez un allié dans votre deck ou votre pile de défausse et ajoutez-le à votre main. Mélangez votre deck.",
  'uj004': "<b>Réponse</b> : après que Cowabunga est entré en jeu, défaussez une carte ressource de votre main → piochez 2 cartes et soignez 2 dégâts d'un personnage allié.\n<i>« Ça surfe, les gars ! »</i>",
  'uj005': "Attachez cette carte à un sbire que votre héros a attaqué ce tour-ci. Si elle est attachée à un sbire non-[[ÉLITE]], il gagne Vulnérable.\n<b>Interruption</b> : quand le sbire attaché quitte le jeu, retirez 2 menaces d'une manigance.",
  'uj006': "[star] Rampage 3. <i>(Coût additionnel pour jouer cette carte : subissez 3 dégâts et défaussez les 3 cartes du dessus de votre deck.)</i>\n<b>Action de héros</b> <i>(contre)</i> : retirez 3 menaces d'une manigance. Si vous contrôlez un soutien [[NYC]], redressez votre héros.",
  'uj008': "[star] <b>Réponse</b> : après que Dreadmon a subi des dégâts consécutifs ([consequential]), redressez-le.\n<b>Interruption forcée</b> : quand le round se termine, défaussez Dreadmon.\n<i>« Tu me dois une fière chandelle, mon. »</i>",
  'uj009': "[star] Rampage 2. <i>(Coût additionnel pour jouer cette carte : subissez 2 dégâts et défaussez les 2 cartes du dessus de votre deck.)</i>\n<b>Action de héros</b> <i>(attaque)</i> : infligez 1 dégât à un ennemi et désorientez-le.\n<i>« Les humains sont très faciles à embrouiller. »</i> —Alopex",
  'uj012': "Ténacité.\n<b>Interruption</b> : quand Hatamoto défend contre une attaque, retirez 1 menace d'une manigance.\n<i>« Je défendrai l'Empereur au prix de ma vie. »</i>",
  'uj016': "<b>Réponse</b> : après avoir joué Inspector Ishida de votre main, choisissez :\n• Retirez 2 menaces d'une manigance.\n• Regardez les 3 cartes du dessus du deck Rencontre et remettez-les dans l'ordre de votre choix.",
  'uj017': "[star] Réduction 1 ([[Artiste Martial]]).\n<b>Action de héros</b> <i>(contre)</i> : retirez 1 menace d'une manigance. Retirez 1 menace d'une manigance.\n<i>« Qu'est-ce qu'ils vont faire ensuite ? J'ai une intuition. »</i> —Raphael",
  'uj018': "[star] <b>Réponse</b> : après que Lita a contré, regardez la carte du dessus de votre deck. Vous pouvez défausser 1 carte de votre main pour ajouter cette carte à votre main.\n<i>« Ton temps est écoulé. »</i>",
  'uj019': "Attachez cette carte à un allié [[NINJA]] ou [[MUTANIMAL]]. 1 amélioration [[ENTRAÎNEMENT]] max par allié.\nL'allié attaché gagne +1 CTR et +2 points de vie.\n<i>« Souviens-toi de ton entraînement. »</i> —Casey Marie Jones",
  'uj020': "<b>Réponse</b> : après que Mona Lisa est entrée en jeu, choisissez un événement [[CONTRE]] dans votre pile de défausse et glissez-le ici.\n<b>Action</b> : jouez la carte glissée ici <i>(en payant son coût)</i>. Puis, défaussez Mona Lisa.",
  'uj021': "<b>Réponse</b> : après que Mondo Gecko est entré en jeu, camouflez-le.\n<i>« Salut salut les amis, laissez-moi d'abord jeter un œil. »</i>",
  'uj022': "[star] Réduction 1 ([[Artiste martial]] ou [[espion]]).\nTemporaire. 1 max par joueur.\n<b>Réponse</b> (<i>contre</i>) : après avoir joué une carte <i>(y compris celle-ci</i>), retirez 1 menace d'une manigance.",
  'uj023': "<b>Réponse</b> : après que Night-Blade est entré en jeu, cherchez une carte [[Préparation]] dans votre deck ou votre pile de défausse et ajoutez-la à votre main. Mélangez votre deck.\n<i>« Je suis la tortue qui a un plan. »</i>",
  'uj024': "1 max par round.\n<b>Action de héros</b> : cherchez une manigance annexe dans le deck Rencontre. Révélez cette manigance annexe → piochez 3 cartes <i>(Mélangez le deck Rencontre)</i>.",
  'uj026': "<b>Réponse</b> : après qu'un personnage que vous contrôlez a contré, placez 1 jeton Élan ici (jusqu'à un maximum de 8). Vous pouvez défausser Ram-Shell pour infliger 1 dégât à un ennemi pour chaque jeton Élan ici.",
  'uj027': "[star] <b>Réponse</b> : après que Sally Pride a attaqué ou contré, retirez 2 menaces d'une manigance.\n<i>« Je suis bien plus efficace avec mes poings qu'avec mes mots. »</i>",
  'uj028': "Wingnut perd chaque icône [acceleration].\n[star] Si Wingnut est en jeu, Screwloose subit -1 dégât consécutif après avoir utilisé un pouvoir de base.\n<i>« Admirez-moi cette charge utile ! »</i>",
  'uj030': "<b>Action de héros</b> <i>(attaque)</i> : infligez 4 dégâts à un ennemi. Si cet ennemi est vaincu par cette attaque, retirez 2 menaces d'une manigance.\n<i>« On ne peut pas arrêter ce qu'on ne voit pas. »</i> —Ronin",
  'uj033': "<b>Réponse</b> : après que Tomoe Ame a déjoué une manigance annexe ou vaincu un sbire, piochez 1 carte.\n<i>« Mon devoir est ma vie. Sans lui, je ne suis qu'une ombre. »</i>",
  'uj034': "Attachez cette carte à un personnage allié. Tant qu'elle est attachée à une identité, cette carte gagne Restreint. Usages (3 jetons Corde).\n<b>Réponse</b> : après que le personnage attaché a utilisé un pouvoir de base, inclinez cette carte et retirez 1 jeton Corde d'ici → retirez 2 menaces d'une manigance.",
  'uj036': "<b>Réponse</b> : après que Venus est entrée en jeu, choisissez un joueur. Ce joueur cherche une manigance annexe Joueur dans son deck et une pile de défausse et l'ajoute à sa main.\n<i>« Je façonne mon propre destin. »</i>",
  'uj037': "Réduisez de 1 le coût pour jouer cette carte si vous contrôlez un soutien [[NYC]].\n<b>Réponse de héros</b> : après qu'un sbire s'est engagé avec vous, défaussez Watch the Exits → retirez 2 menaces d'une manigance et redressez votre héros.",
  'uj038': "<b>Action</b> : inclinez Wingnut et dépensez les ressources suivantes [energy][energy] → trouvez Screwloose et mettez-le en jeu.\n[acceleration]",
  'uj039': "<b>Réponse</b> : après avoir joué Zebulon de votre main, placez 1 jeton Brûlure sur lui pour chaque carte dans votre main (jusqu'à un maximum de 4).\n<b>Action</b> : retirez 1 jeton Brûlure de Zebulon → retirez 1 menace d'une manigance.",


  // --- TMNT Leadership (ul) : ajouter les cartes ulNNN ci-dessous, dans ce bloc seulement ---
  'ul001': "Riposte 1.\n<b>Réponse</b> : après qu'Alopex est entrée en jeu, camouflez-la.\n<i>« Maintenant, place à la partie amusante. »</i>",
  'ul002': "Cette carte génère une ressource [wild] pour chaque allié que vous contrôlez (jusqu'à un maximum de 3).",
  'ul005': "<b>Réponse</b> : après que Dask est entré en jeu, regardez les 3 cartes du dessus du deck Rencontre. Pour chaque traîtrise ainsi regardée, infligez 1 dégât à un ennemi. Remettez-les dans l'ordre de votre choix.\n<i>« Viva la libertad. »</i>",
  'ul006': "Utilisations (3 jetons Blocage).\n<b>Action</b> : inclinez cette carte et retirez-en 1 jeton Blocage → donnez une carte d'état Tenace à un allié [[TURTLE]].\n<i>« Soyez prêts à tout. »</i> —Leonardo",
  'ul007': "[star] Rampage 2. <i>(Coût additionnel pour jouer cette carte : subissez 2 dégâts et défaussez les 2 cartes du dessus de votre deck.)</i>\n<b>Action de héros</b> : défaussez un allié que vous contrôlez → infligez 2 dégâts à un ennemi, retirez 2 menaces d'une manigance et piochez 2 cartes.",
  'ul008': "<b>Réponse forcée</b> : après que Gennosuke a contré ou attaqué, choisissez : soit vous défaussez 1 carte de votre main, soit vous défaussez Gennosuke.\n<i>« Je ne travaille pas gratuitement, et je ne travaille pas pour pas cher. »</i>",
  'ul009': "Exigence ([energy]). <i>(Lorsque vous payez pour cette carte, dépensez les ressources indiquées.)</i>\n<b>Action de héros</b> <i>(attaque)</i> : inclinez votre héros → infligez à un ennemi un nombre de dégâts égal à la somme des valeurs de CTR, ATQ et DEF de votre héros.",
  'ul010': "Jouez cette carte sous le contrôle de n'importe quel joueur. 1 carte [[ÉQUIPE]] max par joueur.\nChacun de vos alliés [[TURTLE]] gagne +1 point de vie. Si chacun de vos personnages a le trait [[TURTLE]], réduisez de 1 le coût en ressource des alliés [[TURTLE]] que vous jouez.",
  'ul014': "<b>Action de héros</b> : camouflez jusqu'à 2 personnages que vous contrôlez (3 personnages à la place si vous contrôlez un soutien [[NYC]]).\n<i>« Il est temps d'enquêter nous-mêmes. »</i> —Donatello",
  'ul015': "Réduisez de 1 le coût pour jouer Mission Leader si votre identité a le trait [[SOLDAT]].\n<b>Réponse de héros</b> : après qu'une manigance annexe a été déjouée, inclinez Mission Leader → chaque joueur pioche 1 carte.",
  'ul016': "Attachez cette carte à un allié. 1 max par allié.\n<b>Interruption</b> : quand le personnage attaché utilise un pouvoir de base, inclinez Naginata → il gagne +2 à ce pouvoir pour cette utilisation.\n<i>« Tu me trouves amoché ? Tu devrais voir l'autre... »</i> —Raphael",
  'ul017': "<b>Réponse</b> : après que Napoleon est entré en jeu, infligez 1 dégât à chaque ennemi.\n<i>« N'interromps jamais ton ennemi quand il est en train de commettre une erreur. »</i>",
  'ul019': "[star] <b>Réponse forcée</b> : après qu'Old Hob a attaqué, placez 1 menace sur la manigance principale.\n<i>« Cette ville respecte les crocs, les griffes et la puissance de feu. »</i>",
  'ul020': "<b>Réponse</b> : après que Rasputin est entré en jeu, chaque joueur pioche 1 carte.\n<i>« Ils me disent fou, et pourtant leur monde brûle de raison. »</i>",
  'ul021': "<b>Interruption</b> : quand Red Shell défend contre une attaque, prévenez un nombre de dégâts de cette attaque égal à l'ATQ de Red Shell.\n<i>« J'en sais plus sur le combat que tu n'en oublieras jamais. »</i>",
  'ul023': "[star] Rampage 3. <i>(Coût additionnel pour jouer cette carte : subissez 3 dégâts et défaussez les 3 cartes du dessus de votre deck.)</i>\n<b>Réponse de héros</b> : après qu'un allié a été vaincu, cherchez un allié dans votre deck et mettez-le en jeu, incliné. <i>(Mélangez.)</i>",
  'ul024': "Attachez cette carte à un sbire que votre héros a attaqué ce tour-ci. Si elle est attachée à un sbire non-[[ÉLITE]], il gagne Vulnérable.\n<b>Interruption</b> : quand le sbire attaché quitte le jeu, piochez 1 carte.\n<i>« De nouveaux jouets à mâcher ?!? »</i> —Tokka",
  'ul025': "<b>Réponse</b> : après que Shugun est entré en jeu, défaussez un allié de votre main → donnez une carte d'état Tenace à un allié.\n<i>« Suivez-moi, si vous voulez vivre. »</i>",
  'ul027': "Attachez cette carte à un allié spécifique à l'identité que vous contrôlez. 1 max par deck.\nL'allié attaché gagne +2 points de vie et devient votre \"acolyte\".\n<b>Réponse</b> : après que vous avez effectué une récupération de base, soignez 2 dégâts de l'allié attaché.",
  'ul028': "Attachez cette carte à un allié [[NINJA]] ou [[MUTANIMAL]]. 1 amélioration [[ENTRAÎNEMENT]] max par allié.\nL'allié attaché gagne +1 CTR, +1 ATQ et +1 point de vie.\n<i>« Qui a dit que tout cet entraînement ne servirait à rien ? »</i> —Michelangelo",
  'ul029': "<b>Réponse</b> : après que Splinter est entré en jeu, regardez les 5 cartes du dessus de votre deck. Ajoutez-en 1 à votre main et placez les autres sous votre deck dans l'ordre de votre choix.\n<i>« Tu dois choisir ton propre chemin, mon fils. »</i>",
  'ul030': "Réduisez de 1 le coût pour jouer cette carte si vous contrôlez un soutien [[NYC]].\n<b>Action de héros</b> : défaussez Street Vendor → soignez un total de 3 dégâts répartis parmi les personnages que vous contrôlez.\n<i>« Les meilleurs chili cheese dogs de la ville ! »</i> —Alopex",
  'ul031': "<b>Action d'alter ego</b> : cherchez dans votre deck et votre pile de défausse un allié et une amélioration pouvant être attachée à un allié. Ajoutez-les à votre main. <i>(Mélangez.)</i>\n<i>« Il est temps de s'y remettre. »</i> —Odin",
  'ul034': "<b>Interruption de héros</b> : quand vous utilisez votre pouvoir de contre de base <i>(CTR)</i> ou votre pouvoir d'attaque de base <i>(ATQ)</i>, inclinez un allié que vous contrôlez → ajoutez le pouvoir correspondant de cet allié à celui de votre héros pour cette utilisation.\n<i>« Relais des Tortues ! »</i> —Michelangelo",
  'ul035': "Jouez cette carte uniquement si votre identité a le trait [[TURTLE]].\n<b>Action de héros</b> : cherchez un allié [[TURTLE]] parmi les 5 cartes du dessus de votre deck et mettez-le en jeu. Si cet allié est toujours en jeu à la fin de la phase, ajoutez-le à votre main.",
  'ul036': "[star] <b>Réponse</b> : après que Turtle Titan a contré une manigance, soignez-lui 2 dégâts.\n<i>« Tremblez, criminels ! Turtle Titan est là ! »</i>",
  'ul037': "Ténacité.\n[star] Turtle-At-Arms gagne +2 ATQ et +2 CTR tant qu'il a une carte d'état Tenace.\n<i>« Allez, guerriers. Nous devons aider à sauver ce pays. »</i>",
  'ul039': "Vous pouvez jouer la carte attachée à Venus comme si elle était dans votre main.\n<b>Réponse</b> : après que Venus est entrée en jeu, choisissez dans votre pile de défausse une carte qui partage un [[TRAIT]] avec Venus et attachez-la-lui, face cachée.",
  'ul040': "Victoire 0.\n<b>Une fois déjouée</b> : mélangez les alliés [[WEASEL]] mis de côté dans le deck Rencontre.\n<i>« Cette caisse est apparue devant notre porte. Qu'est-ce que vous voulez qu'on en fasse ? »</i> —Rocksteady",
  'ul041': "Liée (Weasel In).\nMusroom ne compte pas dans votre limite d'alliés.\n<b>Une fois révélée</b> : soignez 2 dégâts d'un personnage ami et mettez Mushroom en jeu sous votre contrôle. Cette carte gagne Renfort. Cet effet ne peut pas être annulé.",
  'ul042': "Liée (Weasel In).\nZanna ne compte pas dans votre limite d'alliés.\n<b>Une fois révélée</b> : retirez 2 menaces d'une manigance et mettez Zanna en jeu sous votre contrôle. Cette carte gagne Renfort. Cet effet ne peut pas être annulé.",
  'ul043': "Liée (Weasel In).\nZink ne compte pas dans votre limite d'alliés.\n<b>Une fois révélée</b> : infligez 2 dégâts à un ennemi et mettez Zink en jeu sous votre contrôle. Cette carte gagne Renfort. Cet effet ne peut pas être annulé.",
  'ul044': "<b>Réponse de héros</b> : après avoir incliné votre héros pour effectuer un contre ou une attaque de base, défaussez un allié que vous contrôlez → ajoutez le pouvoir correspondant de cet allié à celui de votre héros pour cette utilisation. Redressez votre héros.",
  'ul045': "[star] <b>Réponse</b> : après que Zato-Ino a attaqué et blessé un ennemi, hébétez cet ennemi.\n<i>« Tu ferais bien de ne pas me sous-estimer. »</i>",
  'ul046': "<b>Réponse</b> : après avoir joué Zetian de votre main, piochez X cartes (jusqu'à un maximum de 3), X étant égal au numéro du stade du méchant. Si le méchant n'a pas de numéro de stade, piochez 1 carte.\n<i>« L'ordre et le chaos sont les deux faces d'une même pièce. »</i>",


  // --- TMNT Protection (up) : ajouter les cartes upNNN ci-dessous, dans ce bloc seulement ---
  // tmnt_aspect_protection — Ace Duck (Ally), reskin de 09012 Brother Voodoo
  'up001': "<b>Réponse</b> : après qu'Ace Duck est entré en jeu, cherchez une carte Événement parmi les 5 cartes du dessus de votre deck et ajoutez-la à votre main. Mélangez votre deck.\n<i>« Paniquer ? Jamais, coin-coin. »</i>",
  // tmnt_aspect_protection — Autodefenestration (Event), modifiée de 01003 Backflip ; « Rampage » laissé en anglais
  'up004': "[star] Rampage 2. <i>(Coût additionnel pour jouer cette carte : subissez 2 dégâts et défaussez les 2 cartes du dessus de votre deck.)</i>\n<b>Interruption de héros</b> <i>(défense)</i> : quand vous êtes censé subir n'importe quelle quantité de dégâts d'une attaque, prévenez tous ces dégâts.",
  // tmnt_aspect_protection — Cyber Ninja (Ally) ; « cloak » = poser une carte d'état Camouflé
  'up007': "<b>Réponse</b> : après que Cyber Ninja est entré en jeu, défaussez une amélioration de votre main → piochez 1 carte et camouflez Cyber Ninja.\n<i>« Il fut un temps où de tels sentiments troublaient mon jugement. J'ai corrigé ça... »</i>",
  // tmnt_aspect_protection — Demoralize (Event)
  'up009': "<b>Action de héros</b> : choisissez un ennemi. Il vous attaque. Désorientez cet ennemi.\n<i>« C'est l'heure de faire tomber des têtes ! »</i> —Raphael",
  // tmnt_aspect_protection — Electrostatic Armor (Upgrade), reskin de 10031
  'up010': "Jouez cette carte sous le contrôle de n'importe quel joueur.\n1 max par joueur.\n<b>Réponse</b> : après que vous avez défendu contre une attaque, infligez 1 dégât au personnage attaquant.",
  // tmnt_aspect_protection — Energy Barrier (Upgrade), reskin de 05017
  'up011': "Utilisation (3 jetons Réverbération).\n<b>Interruption</b> : quand vous êtes censé subir n'importe quelle quantité de dégâts, retirez 1 jeton Réverbération de cette carte → prévenez 1 de ces dégâts et infligez 1 dégât à un ennemi.",
  // tmnt_aspect_protection — Groo the Wanderer (Ally), modifiée de 20016 Star-Lord (sans À Distance)
  'up013': "<b>Réponse forcée</b> : après que Groo the Wanderer est entré en jeu sous votre contrôle, attribuez-vous 1 carte Rencontre face cachée.\n<i>« J'aurais deux mots à vous dire ! »</i>",
  // tmnt_aspect_protection — Grotto (Ally), texte de 09014 Iron Fist, jetons « brute »
  'up014': "Grotto entre en jeu avec 2 jetons Brute sur lui.\n<b>Interruption</b> : quand Grotto attaque un ennemi, retirez-lui 1 jeton Brute → sonnez cet ennemi et infligez-lui 1 dégât.",
  // tmnt_aspect_protection — Helpful Bystander (Ally)
  'up015': "Vulnérable. 1 max par deck.\nVotre héros gagne +1 en taille de main.\n<b>Interruption forcée</b> : quand un ennemi vous attaque, il attaque Helpful Bystander à la place. Cette attaque gagne Déferlement.",
  // tmnt_aspect_protection — Herman (Ally)
  'up016': "Ténacité. Herman peut avoir jusqu'à 3 cartes d'état Tenace.\n<b>Interruption</b> : quand Herman entre en jeu, placez sur lui une carte d'état Tenace supplémentaire (2 max) pour chaque ressource payée en trop pour son coût.",
  // tmnt_aspect_protection — Honor Blade (Ally), reskin de 56041 Patriot
  'up017': "<b>Réponse</b> : après que vous avez engagé un sbire, donnez une carte d'état Tenace à Honor Blade.\n<i>« Je suis prêt à tout. »</i>",
  // tmnt_aspect_protection — Jōtarō (Ally), modifiée de 26014 Protector
  'up021': "Ténacité.\n<b>Interruption</b> : quand un ennemi est censé infliger n'importe quelle quantité de dégâts, dépensez une ressource [physical] → diminuez de 1 cette quantité. (Limite d'une fois par round.)\n<i>« Je protégerai ce village au péril de ma vie. »</i>",
  // tmnt_aspect_protection — Lindsey Baker (Support), texte de 09019 The Night Nurse, jetons « healing »
  'up022': "Utilisations (3 jetons Guérison).\n<b>Action</b> : inclinez Lindsey Baker et retirez-lui 1 jeton Guérison → soignez 1 dégât d'un héros et défaussez 1 de ses cartes d'état.",
  // tmnt_aspect_protection — Lookout (Upgrade)
  'up023': "Réduisez de 1 le coût pour jouer cette carte si vous contrôlez un soutien [[NYC]].\n<b>Réponse de héros</b> : après qu'un sbire vous a engagé, défaussez Lookout → camouflez votre héros et piochez 1 carte.\n<i>« On ne peut pas se permettre de baisser la garde. »</i> —Raphael",
  // tmnt_aspect_protection — Nobody (Ally)
  'up024': "<b>Réponse</b> : après que Nobody est entré en jeu, placez sur lui une carte d'état Tenace ou Camouflé.\n<i>« Can they swing from a thread? Take a look overhead. Hey there, there goes Nobody. »</i>",
  // tmnt_aspect_protection — Primal Provisions (Event) ; « Rampage » laissé en anglais
  'up026': "1 max par phase.\n[star] Rampage 2. <i>(Coût additionnel pour jouer cette carte : subissez 2 dégâts et défaussez les 2 cartes du dessus de votre deck.)</i>\n<b>Action de héros</b> : piochez 2 cartes.\n<i>« On ne peut pas se reposer. Il faut continuer. »</i> —Alopex",
  // tmnt_aspect_protection — Protection Training (Upgrade), modifiée de 32013
  'up027': "Attachez cette carte à un allié [[NINJA]] ou [[MUTANIMAL]]. 1 amélioration [[ENTRAÎNEMENT]] max par allié.\nL'allié attaché gagne +3 points de vie.\n<i>« Tenez la ligne, mes frères ! »</i> —Leonardo",
  // tmnt_aspect_protection — Rabid Infection (Upgrade)
  'up028': "Attachez cette carte à un sbire que votre héros a attaqué ce tour-ci. Si elle est attachée à un sbire non-[[ÉLITE]], il gagne Vulnérable.\n<b>Interruption</b> : quand le sbire attaché s'active, infligez 1 dégât à un ennemi.",
  // tmnt_aspect_protection — Redirection Mastery (Upgrade) ; « exactly defend » : question Q-UP1
  'up030': "Jouez cette carte sous le contrôle de n'importe quel joueur. 1 max par joueur.\n<b>Réponse de héros</b> : après que vous avez « exactement » défendu une attaque, infligez à l'attaquant des dégâts égaux à votre DEF pour cette attaque.",
  // tmnt_aspect_protection — Road Rage (Ally), modifiée de 01066 Hawkeye
  'up031': "Road Rage entre en jeu avec 3 jetons Carburant sur lui.\n<b>Réponse</b> : après qu'un sbire est entré en jeu, retirez 1 jeton Carburant de Road Rage → infligez 2 dégâts à ce sbire.\n<i>« Ça faisait longtemps que je voulais te rattraper. »</i>",
  // tmnt_aspect_protection — Senkon (Upgrade)
  'up033': "Attachez cette carte à un personnage ami. Tant qu'elle est attachée à une identité, cette carte gagne Restreint.\n<b>Interruption</b> : quand le personnage attaché défend contre une attaque ennemie, inclinez Senkon → cet ennemi a –1 ATQ pour cette attaque.",
  // tmnt_aspect_protection — Seymour Gutz (Ally), reskin de 48012 Rogue
  'up034': "<b>Action</b> : infligez 1 dégât à un autre personnage ami → jusqu'à la fin du round, Seymour Gutz gagne tous les [[TRAITS]] de ce personnage et ajoute la CTR et l'ATQ imprimées de ce personnage à ses pouvoirs correspondants. (Limite d'une fois par round.)",
  // tmnt_aspect_protection — Tonfa (Upgrade)
  'up039': "Restreint.\n<b>Interruption de héros</b> : pendant le calcul des dégâts d'une attaque contre vous, inclinez cette carte → donnez à votre héros soit +1 DEF, soit Riposte 1 pour cette attaque.",
  // tmnt_aspect_protection — Usagi Yōjimbō (Ally)
  'up041': "Riposte 2. Ténacité.\nUsagi Yōjimbō ne s'incline pas pour défendre.\n<i>« Je te protégerai au péril de ma vie. »</i>",
  // tmnt_aspect_protection — What Doesn't Kill Me (Event), reskin de 27016
  'up042': "Exigence ([physical]). <i>(Lorsque vous payez pour cette carte, dépensez les ressources indiquées.)</i>\n<b>Action de héros</b> : soignez 2 dégâts de votre héros → redressez votre héros.\n<i>« Quand je sortirai d'ici, tu vas le regretter ! »</i>",
  // tmnt_aspect_protection — Wonder Turtle (Ally), reskin de 54032 White Widow
  'up043': "<b>Réponse</b> : après avoir résolu la capacité d'une carte [[Préparation]] que vous contrôlez, soignez Wonder Turtle d'un nombre de dégâts égal au coût en ressources imprimé de cette carte.\n<i>« Surprise. »</i>",


  // --- TMNT Dual-Aspect (ud) : ajouter les cartes udNNN ci-dessous, dans ce bloc seulement ---
  // tmnt_aspect_dual — Rōnin (Ally), Agressivité/Justice
  'ud001': "<b>Réponse</b> : après que Rōnin est entré en jeu, camouflez-le.\n<b>Interruption</b> : quand Rōnin est vaincu par des dégâts consécutifs ([consequential]), dépensez une ressource [wild] → piochez 3 cartes.\n<i>« Je dois venger ceux qui sont tombés. »</i>",
  // tmnt_aspect_dual — Doomsayer (Ally), Agressivité/Commandement
  'ud002': "<b>Réponse</b> : après que Doomsayer est entré en jeu, piochez X cartes (3 au maximum), où X est égal au numéro d'étape du méchant.\n<b>Interruption</b> : quand Doomsayer est vaincu par des dégâts consécutifs ([consequential]), piochez 1 carte pour chaque sbire engagé avec vous.",
  // tmnt_aspect_dual — Heavy Metal (Ally), Agressivité/Protection
  'ud003': "Heavy Metal entre en jeu avec 2 compteurs ampli sur elle.\n<b>Réponse</b> : après que Heavy Metal a subi des dégâts consécutifs ([consequential]), retirez-lui 1 compteur ampli → placez une carte d'état sur un personnage.",
  // tmnt_aspect_dual — Stealth Fighter (Ally), Justice/Commandement
  'ud004': "<b>Réponse</b> : après que Stealth Fighter est entré en jeu ou a subi des dégâts consécutifs ([consequential]), camouflez-le.\n<b>Interruption</b> : après que Stealth Fighter a été vaincu par des dégâts consécutifs ([consequential]), camouflez un personnage ami.",
  // tmnt_aspect_dual — Sōhei (Ally), Justice/Protection
  'ud005': "Ténacité.\n<b>Interruption</b> : quand Sōhei est vaincu par des dégâts consécutifs ([consequential]), votre héros gagne +2 en taille de main jusqu'à la fin du round.\n<i>« Je veillerai sur toi depuis l'autre côté. »</i>",
  // tmnt_aspect_dual — Nightwatcher (Ally), Commandement/Protection
  'ud006': "Ténacité.\n<b>Réponse</b> : après que Nightwatcher a subi des dégâts consécutifs ([consequential]), donnez-lui une carte d'état Tenace.\n<i>« Je suis le héros dont nous avons TOUS besoin ! »</i>",

  // --- TMNT Shinobi Bushido (sb) : ajouter les cartes sbNNN ci-dessous, dans ce bloc seulement ---
  // sb001 Loyalty (Upgrade, OATH)
  'sb001': "Utilisations (3 compteurs de samouraï).\nVotre héros gagne +1 DEF.\n<b>Réponse forcée</b> : après que votre héros a fait une défense de base, retirez 1 compteur de samouraï de cette carte.\n<i>« Il faudra me passer sur le corps ! »</i> —Michelangelo",
  // sb002 Rectitude (Upgrade, OATH)
  'sb002': "Utilisations (3 compteurs de samouraï).\nVotre héros gagne +1 CTR.\n<b>Réponse forcée</b> : après que votre héros a fait un contre de base, retirez 1 compteur de samouraï de cette carte.\n<i>« Nous manquons de temps ! »</i> —Donatello",
  // sb003 Courage (Upgrade, OATH)
  'sb003': "Utilisations (3 compteurs de samouraï).\nVotre héros gagne +1 ATQ.\n<b>Réponse forcée</b> : après que votre héros a fait une attaque de base, retirez 1 compteur de samouraï de cette carte.\n<i>« Je ne te crains pas. »</i> —Leonardo",
  // sb004 Glory (Upgrade, OATH)
  'sb004': "1 max par joueur.\n<b>Réponse de héros</b> : après que votre héros a déjoué une manigance annexe, défaussez cette carte → placez en tout 4 compteurs de samouraï parmi un nombre quelconque d'améliorations [[OATH]] que vous contrôlez.",
  // sb005 Gratitude (Upgrade, OATH)
  'sb005': "Utilisations (2 compteurs de samouraï).\n<b>Action</b> : inclinez cette carte et retirez-lui 1 compteur de samouraï → soignez 1 dégât de votre identité. Vous pouvez défausser 1 carte d'état de votre identité.",
  // sb006 Mercy (Upgrade, OATH), lecture provisoire (Q-B1)
  'sb006': "1 max par joueur.\n<b>Interruption de héros</b> : quand un ennemi devrait être mis K.O. par votre héros, défaussez cette carte à la place → fixez les points de vie de cet ennemi à 1. Ensuite, piochez 3 cartes.",
  // sb007 Integrity (Upgrade, OATH)
  'sb007': "<b>Réponse</b> : après que vous avez joué une amélioration [[OATH]], inclinez cette carte → placez 1 compteur de samouraï sur une amélioration [[OATH]] que vous contrôlez.\n<i>« Les actes parlent plus fort que les mots. »</i> —Odyn",
  // sb008 Self-Control (Upgrade, OATH)
  'sb008': "Utilisations (3 compteurs de samouraï).\n<b>Ressource</b> : inclinez cette carte et retirez-lui 1 compteur de samouraï → générez une ressource [wild].\n<i>« La voie de la maîtrise de soi est longue. »</i> —Michelangelo",
  // sb009 Devotion (Upgrade, OATH)
  'sb009': "Utilisations (3 compteurs de samouraï).\n<b>Action de héros</b> : inclinez cette carte et retirez-lui 1 compteur de samouraï → redressez une amélioration [[WEAPON]] que vous contrôlez.\n<i>« La maîtrise ne vient pas vite. »</i> —Ronin",
  // sb010 Tsujigiri (Event, ATTACK)
  'sb010': "<b>Action de héros</b> <i>(attaque)</i> : infligez à un ennemi un nombre de dégâts égal à votre ATQ. Si cette attaque met cet ennemi K.O., vous pouvez placer 1 compteur de samouraï sur une amélioration [[OATH]] que vous contrôlez.\n<i>« Il est temps d'essayer mes nouvelles lames. »</i> —Leonardo",
  // sb011 Vow (Event, THWART)
  'sb011': "<b>Action de héros</b> <i>(contre)</i> : retirez d'une manigance un nombre de menaces égal à la CTR de votre héros. Si cela retire la dernière menace de cette manigance, cherchez dans votre deck une amélioration [[OATH]] et ajoutez-la à votre main. <i>(Mélangez.)</i>",
  // sb012 Kensei (Event, SKILL)
  'sb012': "<b>Action de héros</b> : inclinez une amélioration [[WEAPON]] que vous contrôlez → redressez votre héros.\n<i>« Un guerrier est toujours prêt. »</i> —Raphael",
  // sb013 Santōryū Ōgi (Upgrade, SKILL), lecture provisoire (Q-B2)
  'sb013': "1 max par deck. L'amélioration attachée perd le mot-clé Restreint.\n<b>Réponse</b> : après que cette carte est entrée en jeu, cherchez dans votre deck et votre pile de défausse une amélioration [[WEAPON]]. <i>(Mélangez.)</i> Mettez cette amélioration en jeu (en payant son coût en ressources) avec cette carte attachée.",
  // sb014 Kōshō (Upgrade unique, OATH. TITLE. TRAINING.)
  'sb014': "Utilisations (2 compteurs de samouraï). Attachez-la à un allié que vous contrôlez.\n1 amélioration [[TRAINING]] max par allié.\n<b>Action de héros</b> : inclinez cette carte et retirez-lui 2 compteurs de samouraï → soignez 2 dégâts de l'allié attaché et redressez-le.",
  // sb015 Oathbreaker (Event, TACTIC)
  'sb015': "<b>Interruption de héros</b> : quand une carte rencontre est révélée depuis le deck rencontre, défaussez une amélioration [[OATH]] que vous contrôlez → annulez tous les effets de cette carte rencontre et défaussez-la.\n<i>« Je ferai ce que je dois pour les sauver tous... »</i> —Leonardo",
  // sb016 Wakizashi (Upgrade unique, NINJA. WEAPON.)
  'sb016': "Restreint.\n<b>Réponse de héros</b> : après qu'une amélioration [[OATH]] est défaussée du jeu, inclinez cette carte → piochez 1 carte.\n<i>« Je préfère le dashido traditionnel. »</i> —Moja",
  // sb017 Uno (Ally unique, NINJA. SAMURAI. TURTLE.)
  'sb017': "[star] <b>Réponse</b> : après qu'Uno a utilisé un pouvoir de base, placez 1 compteur de samouraï sur une amélioration [[OATH]] que vous contrôlez.\n<i>« Tu manques de discipline. »</i>",
  // sb018 Musha Shugyō (Manigance annexe de joueur, unique)
  'sb018': "Victoire 0.\nLes personnages autres que le propriétaire de cette carte ne peuvent pas en retirer de menace.\n<b>Une fois déjouée</b> : le propriétaire de cette carte peut chercher dans son deck et sa pile de défausse jusqu'à 2 améliorations [[OATH]] et les mettre en jeu. <i>(Mélangez.)</i>\n<i>« J'endurerai l'hiver de cette âme. »</i> —Leonardo",
  // sb019 Gusoku (Upgrade unique, ARMOR)
  'sb019': "<b>Réponse de héros</b> : après que vous avez utilisé un de vos pouvoirs de base, inclinez cette carte et retirez 1 compteur de samouraï d'une amélioration [[OATH]] que vous contrôlez → redressez votre héros.\n<i>Cette armure a vu bien des batailles.</i>",
  // sb020 Iaidō (Event, SKILL)
  'sb020': "<b>Interruption de héros</b> : quand vous utilisez un pouvoir de base, vous gagnez +2 à ce pouvoir pour cette utilisation. Vous pouvez placer 1 compteur de samouraï sur une amélioration [[OATH]] que vous contrôlez.\n<i>« Fais bien attention, je ne te le montrerai pas deux fois... »</i> —Ronin",

  // --- TMNT Shinobi Kuji-Kiri (sj) : ajouter les cartes sjNNN ci-dessous, dans ce bloc seulement ---

  // --- TMNT Shinobi Ninjutsu (sa) : ajouter les cartes saNNN ci-dessous, dans ce bloc seulement ---

  // --- TMNT Shinobi Taijutsu (sh) : ajouter les cartes shNNN ci-dessous, dans ce bloc seulement ---

  // --- TMNT Shinobi Dual (sc) : les douze cartes Dual Shinobi (17/10/2026) ---
  // sc001 Nendō (Événement, Bushido/Kuji-Kiri)
  'sc001': "<b>Action de héros</b> <i>(attaque)</i> : inclinez une amélioration [[WEAPON]] que vous contrôlez → infligez 4 dégâts à un ennemi. Hébétez cet ennemi.\n<i>« Réfléchis vite ! » —Casey Jones</i>",
  // sc002 Shugorei (Amélioration, Bushido/Kuji-Kiri)
  'sc002': "1 max par joueur.\nUtilisations (4 compteurs de samouraï).\n<b>Action</b> : inclinez cette carte et retirez-en 2 compteurs de samouraï → piochez 1 carte.\n<i>« Ce dont nous nous souvenons, nous le devenons. » —Leonardo</i>",
  // sc003 Omawari (Événement, Bushido/Ninjutsu)
  'sc003': "<b>Action de héros</b> : inclinez une amélioration [[WEAPON]] que vous contrôlez → camouflez votre héros et donnez-lui une carte d'état Tenace.\n<i>« Rien ne nous passera devant. » —Raphael</i>",
  // sc004 Kuragari (Amélioration, Bushido/Ninjutsu)
  'sc004': "Utilisations (3 compteurs de samouraï).\n<b>Action</b> : inclinez cette carte et retirez-en 3 compteurs de samouraï → camouflez et redressez votre héros.\n<i>« Chhhut... » —Casey Jones</i>",
  // sc005 Yoi-Dachi (Amélioration, Bushido/Taijutsu)
  'sc005': "1 max par joueur. Utilisations (3 compteurs de samouraï).\n<b>Réponse</b> : après que vous avez subi des dégâts d'une attaque d'ennemi, retirez 1 compteur de samouraï d'ici → hébétez cet ennemi.",
  // sc006 Migatte (Événement, Bushido/Taijutsu)
  'sc006': "<b>Interruption de héros</b> <i>(défense)</i> : quand votre héros se défend contre une attaque, il gagne +2 DEF pour cette attaque. Si vous avez payé cette carte avec une carte Shinobi, redressez votre héros.\n<i>« Il est temps de s'écarter de la tradition. » —Nightwatcher</i>",
  // sc007 Mizuki (Événement, Kuji-Kiri/Ninjutsu)
  'sc007': "<b>Action de héros</b> <i>(contre)</i> : retirez 2 menaces d'une manigance. Si cela retire la dernière menace de cette manigance, choisissez :\n• camouflez un personnage ami ;\n• remettez dans votre main un événement de votre pile de défausse.",
  // sc008 Naito Dansā (Événement, Kuji-Kiri/Ninjutsu)
  'sc008': "<b>Action de héros</b> : défaussez des cartes du dessus du deck Rencontre jusqu'à ce que vous défaussiez un attachement ou une manigance annexe. Révélez cette carte → camouflez jusqu'à 2 personnages amis. Hébétez jusqu'à 2 ennemis.\n<i>« Regardez mes mouvements. » —Michelangelo</i>",
  // sc009 Yomi (Événement, Kuji-Kiri/Taijutsu)
  'sc009': "<b>Action de héros</b> <i>(contre)</i> : choisissez 1 carte dans la pile de défausse Rencontre et placez-la sur le dessus du deck Rencontre → retirez 2 menaces d'une manigance.\n<i>« C'est comme entendre la chasse avant qu'elle ne commence. » —Donatello</i>",
  // sc010 Kusuri (Amélioration, Kuji-Kiri/Taijutsu)
  'sc010': "1 max par joueur.\n<b>Action</b> : inclinez cette carte et défaussez un événement [[ATTACK]] de votre main → soignez 2 dégâts d'un personnage ami.\n<i>« Double, double, peine et trouble... » —Donatello</i>",
  // sc011 Kenbu (Événement, Ninjutsu/Taijutsu)
  'sc011': "<b>Action de héros</b> <i>(attaque)</i> : défaussez une carte d'état Camouflé de votre héros → infligez 1 dégât à jusqu'à 3 ennemis. Hébétez chaque ennemi ayant subi des dégâts de cette façon.\n<i>« Suivant. » —Alopex</i>",
  // sc012 Hitodama (Événement, Ninjutsu/Taijutsu)
  'sc012': "<b>Réponse de héros</b> <i>(attaque)</i> : infligez 3 dégâts à un ennemi. Si vous avez payé cette carte avec un événement [[THWART]], camouflez votre héros.\n<i>« On danse ! » —Raphael</i>",

  // --- TMNT Shinobi Paths (se) : les onze Voies (socle Shinobi, 17/10/2026) ---
  // se001 Kagemusha (Path, Ninjutsu)
  'se001': "Permanent.\nVous avez -1 à votre taille de main.\nVotre héros gagne le trait [[NINJA]].\n<i>Shadow Stride</i> — <b>Action de héros</b> : inclinez cette carte → camouflez votre héros.\n<i>« Je suis les ombres. »</i>",
  // se002 Onmyōdō (Path, Kuji-Kiri)
  'se002': "Permanent.\nVous avez -1 à votre taille de main.\nVous gagnez le trait [[MYSTIC]].\n<i>Insight</i> — <b>Action de héros</b> : inclinez cette carte → regardez les 2 cartes du dessus de n'importe quel deck et remettez-les dans le même ordre.",
  // se003 Samurai (Path, Bushido)
  'se003': "Permanent.\nVous avez -1 à votre taille de main.\n<i>Way of the Warrior</i> — <b>Action de héros</b> : inclinez cette carte et retirez en tout 2 compteurs de samouraï parmi les améliorations [[OATH]] que vous contrôlez → redressez votre héros et piochez 1 carte.",
  // se004 Shihan (Path, Taijutsu)
  'se004': "Permanent.\nVous avez -1 à votre taille de main.\n<i>Recenter</i> — <b>Interruption de héros</b> : quand la phase des joueurs se termine, défaussez les 2 cartes du dessus de votre deck → remettez dans votre main 1 carte Taijutsu de votre pile de défausse.",
  // se005 The Last Rōnin (Path hybride, unique, 4 types)
  'se005': "Permanent.\nVous avez -1 à votre taille de main.\nVous pouvez jouer les cartes glissées ici comme si elles étaient dans votre main. <i>(2 cartes glissées maximum.)</i>\n<i>Kanpeki</i> — <b>Action</b> : inclinez cette carte et glissez ici 1 carte Shinobi de votre main → piochez 1 carte.",
  // se006 Yoshimitsu (Path hybride, Bushido + Kuji-Kiri)
  'se006': "Permanent.\nVous avez -1 à votre taille de main.\nVous avez +2 points de vie.\n<i>Magnificence</i> — <b>Action de héros</b> : subissez 1 dégât et inclinez cette carte → vous gagnez +1 CTR, +1 ATQ et +1 DEF jusqu'à la fin du round.",
  // se007 Yamabushi (Path hybride, Kuji-Kiri + Taijutsu)
  'se007': "Permanent.\nVous avez -1 à votre taille de main.\nVous gagnez le trait [[TEMPORAL]].\n<i>Meditate</i> — <b>Action de héros</b> : inclinez cette carte et votre héros → piochez 3 cartes. Choisissez et défaussez 1 carte de votre main.",
  // se008 Onigari (Path hybride, Kuji-Kiri + Ninjutsu)
  'se008': "Permanent.\nVous avez -1 à votre taille de main.\nVous gagnez le trait [[PSIONIC]].\n<i>Dark Visions</i> — <b>Réponse de héros</b> : après que vous avez vaincu un sbire ou une manigance annexe, inclinez cette carte → camouflez votre héros et piochez 1 carte.",
  // se009 Ashigaru (Path hybride, Bushido + Taijutsu)
  'se009': "Permanent.\nVous avez -1 à votre taille de main.\nVous gagnez le trait [[SOLDIER]].\n<i>Light of Foot</i> — <b>Ressource de héros</b> : inclinez cette carte → générez une ressource [wild]. Si vous avez payé une carte Shinobi avec cette ressource, piochez 1 carte.",
  // se010 Onmitsu (Path hybride, Ninjutsu + Taijutsu)
  'se010': "Permanent.\nVous avez -1 à votre taille de main.\n<i>Gardener</i> — <b>Réponse de héros</b> : après que vous avez joué un événement [[ATTACK]] ou [[DEFENSE]], subissez 1 dégât → hébétez un ennemi.",
  // se011 Yōjimbō (Path hybride, Bushido + Ninjutsu)
  'se011': "Permanent.\nVous avez -1 à votre taille de main.\n<i>Bodyguard</i> — <b>Interruption de héros</b> : quand un ennemi attaque, inclinez cette carte → déclarez votre héros en tant que défenseur sans l'incliner.\n<i>« Je suis à tes côtés. »</i>",

}

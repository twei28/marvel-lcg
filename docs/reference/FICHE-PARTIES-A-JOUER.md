# Fiche de parties à jouer : faire passer les cartes de « provisoire » à « terminée »

Écrite le 26/10/2026. Elle sert à une seule chose : une carte n'est « terminée » (`Carte terminée : OUI`, règle de
`docs/reference/PROCESSUS-CARTE.md`) qu'après une **vraie partie jouée par un humain**. Aucun outil du projet ne remplace ça : les tests
prouvent ce que le moteur FAIT, pas ce que le joueur VOIT et CLIQUE.

Les 15 héros et les 50 cartes d'aspect Starjammers sont **tous provisoires** aujourd'hui. Cette fiche dit, pour chacun, quelle partie monter
et quoi regarder. Les points viennent des gabarits `docs/packs/<pack>/GABARITS.md`, des verdicts du 26/10/2026 et de la liste
`docs/rapports/2026-10-26-problemes-a-corriger.md` (partie B). Quand une information manque, c'est écrit « à confirmer ».

## Avant de jouer

**Lancer le jeu**
- En local : `JOUER-SOLO.bat` (double-clic, à la racine du dossier du projet). Il existe aussi `JOUER-SOLO.command` (à confirmer pour
  Linux/Mac) et `JOUER-EN-MULTI.bat` pour jouer à deux sur la même machine.
- En ligne : le site du jeu (`narwhalchampions.com`, une table par partie). Pour tester le téléphone, jouer en ligne depuis le téléphone.
- Les nouveautés d'aujourd'hui n'apparaissent en ligne qu'après le déploiement (`! bash ui-app/deployer.sh`, à lancer par l'utilisateur).

**Choisir son héros** : à la préparation de la partie, filtre **Fan-made** de la grille des héros, puis la tuile du héros. Les cartes
d'aspect (Agressivité, Justice, Leadership, Protection) se choisissent comme d'habitude : un deck d'aspect existant ou le deckbuilder.
Les decks de départ ci-dessous ne contiennent que les cartes du héros (et sa decklist d'auteur quand elle existe).

**Vilain conseillé** : **Rhino** (le plus simple) pour presque tout. Les cas qui demandent autre chose sont dits à chaque fois.

**Signaler un bug**
- Bouton **« Signaler un bug »** (n'importe quel écran en ligne) : nom, description, capture collée en Ctrl+V. Sur le plateau, le journal de
  toute la partie part avec le rapport.
- Onglet **« Log »** du plateau : télécharge le déroulé complet de la partie. À garder si quelque chose ne marche pas : c'est le plus
  utile pour retrouver la cause.

**Comment cocher** : une case `[ ]` par carte ou par point. Quand une case est cochée, dis-moi lesquelles : je passe les cartes
concernées à « Carte terminée : OUI » dans leur gabarit.

---

## 1. Batman — deck « Batman » (Rhino)

Pack `bm`, 28 cartes, créateur ES. Batman joue avec un deck de **dissuasion** (deterrence) : des cartes qu'il mélange dans le deck de rencontre.

- [ ] **Partie complète** avec la tuile « Batman » (Fan-made), biographie au survol de la tuile.
- [ ] **Mise en place, Bruce Wayne (`bm001b`)** : la question « Choose 8 deterrence cards » s'affiche bien et on peut l'annuler.
- [ ] **Batman (`bm001a`), Hero Response** : après une attaque ou une contrariété, choisir une carte de dissuasion et la mélanger dans le deck de
  rencontre. Regarder la vue du deck de dissuasion et la défausse de dissuasion. Maximum 3 par round (la 4e doit être refusée).
- [ ] **Two-Face (`bm015`)** : une fois en jeu, chaque dissuasion mélangée lui donne +1 SCH et +1 ATK jusqu'à la fin du round (2 fois par round au maximum).
- [ ] **Split Decision (`bm014`)** : l'icône Danger (Hazard) est bien dessinée ; à la révélation d'une dissuasion, on défausse le dessus du deck de
  rencontre, et un nombre impair d'icônes de boost ajoute 2 menaces au complot principal. Rien ne doit se passer si la dissuasion est retournée
  comme carte de boost.
- [ ] **Heads I Win (`bm016`)** : à deux joueurs, à égalité de PV, le premier joueur choisit qui subit les dégâts indirects.
- [ ] **Intimidate (`bm005`)** : sur une dissuasion révélée (ou retournée en boost), annuler le surge ; la fenêtre « payer 1 ressource pour la remélanger
  dans le deck » est lisible.
- [ ] **Utility Belt (`bm012`)** : rejoue un « When Revealed » de dissuasion une fois de plus.
- [ ] **Smoke Cloud (`bm019`)** : son boost contre une **manigance** (l'effet n'est lisible qu'en boost d'une activation de manigance).
- [ ] **Contingency Plan (`bm008`)** : la défausse propose bien trois choix de pouvoir de base (THW, ATK **et DEF**), +2 au prochain usage.
- [ ] **Trillionaire (`bm001b`)** : la réduction de coût s'applique aussi à un **soutien** (par exemple The Batcave, trait LOCATION).
- [ ] **Faces « Lantern » (`bm001c`, `bm001d`)** : à confirmer comment les faire apparaître ; regarder qu'elles s'affichent.
- [ ] **Téléphone** : la vue du deck de dissuasion et le choix de la carte à mélanger restent utilisables ; voiles français des 28 cartes
  (`bm019` est en voile uni).

## 2. Wasp (Hank Pym) — deck « Wasp (Hank Pym) » (Rhino)

Pack `hp`, 20 cartes, créateur JackHKP. Trois formes : Wasp minuscule, Hank Pym (alter ego), Wasp géante. Il faut changer de forme plusieurs fois par tour.

- [ ] **Partie complète** avec la tuile « Wasp (Hank Pym) ».
- [ ] **Changer de forme** : on peut aller vers n'importe quelle AUTRE forme (alter ego, minuscule, géante) avec les cartes qui disent « change form ».
- [ ] **Infinite Avengers Mansion (`hp007`)** : poser le compteur pym sur **Hank Pym lui-même** ; lisibilité de l'invite de choix (identité, Mansion, autres cartes).
- [ ] **Bio-Synthetic Wings (`hp009`)** : les X menaces (X = changements de forme ce tour) se répartissent entre **plusieurs manigances** ;
  avec X = 0, l'action ne bloque pas la partie. À provoquer avec 2 manigances en jeu.
- [ ] **The Stinger (`hp012`)** : exactement X dégâts répartis entre les ennemis choisis ; à provoquer avec 2 ennemis en jeu.
- [ ] **Identity Crisis (`hp013`)** : le coût en deux temps (choix dégâts/menace, puis inclinaison de Hank) ; l'Action n'est pas offerte quand Hank est
  incliné ; à 5 compteurs, la carte cherche **Shadow of the Past** (`01190`) et la révèle, sinon pose 7 compteurs sur **Pursued by the Past**
  (`45075`, extension Standard III) : tester avec et sans cette extension.
- [ ] **Take Over Signal (`hp017`)** : un allié du deck devient un sbire « Hacked » engagé avec vous ; s'il n'y a aucun allié à prendre, la carte est défaussée.
- [ ] **Huge Surprise (`hp010`)** : s'attache à un ennemi, qui perd steady et stalwart ; 4 dégâts quand il est sonné ou désorienté ; la carte n'est offerte
  qu'une fois.
- [ ] **Téléphone** : choix répétés (désigner plusieurs manigances ou ennemis) faciles au doigt ; voiles des 20 cartes (`hp006` a été corrigé).

## 3. Corsair — decks « Corsair » et « Corsair (Making Amends) » (Rhino)

Pack `cr`, 20 cartes, créateurs Phenexian et Mysteltainn. Deux decks : l'obligation de départ change (Irresponsible Cad / Making Amends).

- [ ] **Partie complète** avec la tuile « Corsair », et la variante « Making Amends » à l'ouverture de sa fenêtre.
- [ ] **Pocket Universe Gems (`cr001a`)** : quand une carte de la main est défaussée pour payer, la fenêtre (réponse optionnelle) apparaît, une seule fois
  par round ; la carte est glissée sous Corsair.
- [ ] **Jouer une carte glissée sous Corsair** en cliquant dessus (le moteur l'offre, le geste de clic n'est pas prouvé).
- [ ] **Parry (`cr007`) → Riposte (`cr008`) → Remise (`cr009`)** : « la dernière carte que vous avez jouée » compte sur **toute la partie**, pas
  seulement le round : Riposte après Parry étourdit l'ennemi, Remise après Riposte redresse Corsair, Parry après Remise pioche 3 cartes.
- [ ] **Shi'ar Battle Cruiser (`cr016`)**, à **2 joueurs** : l'Alliance permet aux deux joueurs de payer ensemble les deux énergies de son Hero Action.
- [ ] **Shi'ar Bodyguard (`cr015`)** : son boost, et Slave Pits of Chandilar (`cr014`) à plusieurs joueurs (non vus).
- [ ] **Irresponsible Cad (`cr011`) / Making Amends (`cr012`)** : « Discard a card you control » ne propose que des cartes **en jeu** ; défausser Cyclops
  ou Havok retire l'obligation du jeu.
- [ ] **Téléphone** : la fenêtre de Gems, le clic sur la carte glissée.

## 4. Marvel Girl (Rachel Summers) — deck « Marvel Girl » (Rhino)

Pack `rm`, 17 cartes, créateur Dipsome.

- [ ] **Partie complète** avec la tuile « Marvel Girl » (Fan-made).
- [ ] **Chronoskimming (`rm001a`)** : au début du tour, remélanger la main et piocher une nouvelle main ; le coût de la prochaine carte baisse de 1.
- [ ] **Temporal Reversal (`rm007`)** : le tour supplémentaire s'affiche (onglet du joueur, pioche, redressement) ; **à 2 joueurs, une seule par round
  pour toute la table**.
- [ ] **Memory From The Future (`rm013`)** : le tour se termine bien à l'écran.
- [ ] **Temporal Retrieval (`rm010`)** : les cartes attachées face cachée sont lisibles par leur propriétaire seulement.
- [ ] **Hound Program (`rm014`)** : s'ajoute 1 menace à chaque début de tour de Marvel Girl en forme héros ; à 5 menaces, défaite. Image en paysage.
- [ ] **Hound Clothes (`rm016`)** : le boost (défausse 1 carte au hasard) et le -1 de taille de main.
- [ ] **Téléphone** : image de Hound Program en paysage et voile français.

## 5. Roz Solomon — deck « Roz » (Rhino)

Pack `rz`, 21 cartes, créateur jakxin. Beaucoup de cartes ont une capacité « Special » que Roz déclenche par d'autres cartes.

- [ ] **Partie complète** avec la tuile « Roz » (biographie au survol, 21 images).
- [ ] **Driven (`rz001a`)** : après un pouvoir de base, résoudre le « Special » d'une AUTRE carte Wakanda ; avec **Wakandan Stealth Tech (`rz006`)**,
  qui a deux Special, on n'en résout **qu'un seul**, au choix.
- [ ] **Les deux Thor (`rz002`, `rz003`)** : réduction de coût visible dans la main ; la Réponse est donnée à **chaque allié Thor** (y compris un Thor
  officiel) ; la limite de `rz003` est « une fois par tour » de joueur.
- [ ] **Legal Council (`rz018`)** : le choix « dépenser 1 ressource ou annuler » est lisible ; l'icône Accélération.
- [ ] **Weighed Down (`rz016`)** : 1 dégât après chaque Special résolu ; la défausse de l'obligation se range dans la défausse de rencontre ; un Special
  peut être résolu en forme alter ego.
- [ ] **Téléphone** : fenêtre de paiement de Legal Council ; voiles (Roz `rz001a` en voile uni).

## 6. The Warriors Three — decks « The Warriors Three » (Justice) et « The Warriors Three (Agression) » (Rhino)

Pack `wt`, 28 cartes, créateurs Phenexian et Mysteltainn. Un seul joueur contrôle trois héros (Fandral, Hogun, Volstagg) et change de héros actif.

- [ ] **Partie complète** avec les deux decks (variante repliée sous la tuile de base).
- [ ] **Changer de héros** : depuis un héros on ne peut aller qu'à l'alter ego ; depuis l'alter ego, aux trois héros ; avec la carte-titre et
  Leap into Action! (`wt015`), liste triée.
- [ ] **Plateau** : la carte-titre sur le héros actif, les trois soutiens « persona » (celui du héros actif est à ignorer) et leurs états incliné/prêt après un
  changement ; les cartes d'état d'un héros inactif **restent sur lui**.
- [ ] **Plusieurs activations dans un tour** (Fandral attaque, changement, Hogun attaque).
- [ ] **Mighty Endurance (`wt011`)** : un Volstagg inactif reçoit bien sa carte « tough » sur son soutien.
- [ ] **Fimbuldraugr (`wt008`)** : tant que Fandral est actif, les icônes de crise sont ignorées pour **toutes** les cartes joueur.
- [ ] **A Questing We Shall Go! (`wt016`)** : l'obligation s'attache au sbire et disparaît avec lui (à voir à l'écran, sous le sbire).
- [ ] **Fenris (`wt017`), Countdown to Ragnarok (`wt018`), Gleipnir (`wt019`), Skadihr (`wt020`)** : Fenris à PV « - » ; Skadihr devient alliée ; Gleipnir
  en jeu. Skadihr a **Quickstrike** : elle attaque dès qu'elle s'engage (forme héros).
- [ ] **Revelry in Asgard (`wt022`)** : « ce tour » = le tour du joueur (à 2 joueurs, regarder au tour de l'autre).
- [ ] **Téléphone** : Countdown (`wt018`) est en paysage ; voiles des 28 cartes.

## 7. Ch'od — deck « Ch'od » (Rhino)

Pack `co`, 20 cartes, créateurs Phenexian et Mysteltainn.

- [ ] **Partie complète** avec la tuile « Ch'od ».
- [ ] **Master of All Trades (`co001a`)** : la fenêtre de l'Interruption apparaît à chaque carte à « Requirement » jouée, une fois par phase.
- [ ] **Polymath (`co005`)** : payée avec une ressource **wild**, le jeu doit demander quel type elle représente ; payée en physique : carte « tough », en énergie :
  redresse Ch'od, en mental : pioche.
- [ ] **Cr'reee Captured (`co011`)** : Cr'reee glissée sous l'obligation, lisible à l'écran ; l'Action d'alter ego.
- [ ] **Mentor (`co012`)** : -1 de taille de main tant qu'il est engagé ; à sa défaite, on défausse 2 cartes du deck du **joueur qui l'a vaincu** (à 2 joueurs).
- [ ] **Duel of Wits (`co013`)** en paysage ; les icônes de ressource des cartes.
- [ ] **Téléphone** : fenêtre de choix du type de wild.

## 8. U.S. Agent — deck « U.S. Agent » (Rhino)

Pack `us`, 17 cartes, créateur DesignHacker.

- [ ] **Partie complète** avec la tuile « U.S. Agent » (biographie au survol).
- [ ] **Bolster (`us001a`)** : après une défense, redresse une amélioration que vous contrôlez.
- [ ] **Reckless (`us004`)** : prendre X dégâts → retirer X menaces et infliger X dégâts ; si une partie des dégâts est **prévenue**, l'effet n'a pas lieu du tout.
- [ ] **Obstinance (`us008`)** : les deux branches nommées (« Spend a mental resource » / « Spend a physical resource ») s'affichent bien.
- [ ] **U.S. Agent's Machine Gun (`us010`)** : la Réponse est reproposée **à chaque dégât de la rafale** ; « Annuler » arrête la chaîne.
- [ ] **Spear of Odin (`us016`)** : le choix de l'amélioration défaussée (fenêtre de sélection).
- [ ] **Téléphone** : la fenêtre de Machine Gun et d'Obstinance ; voiles des 17 cartes.

## 9. New Ultimate Winter Soldier — deck « New Ultimate Winter Soldier » (Rhino ou Klaw)

Pack `uw`, 19 cartes, créateur Dipsome.

- [ ] **Partie complète** avec la tuile « New Ultimate Winter Soldier » (biographie au survol).
- [ ] **Berserker Fury (`uw006`)** : défausse au hasard puis dégâts selon le coût imprimé de la carte ; la **répétition** (après un ennemi vaincu) demande
  une nouvelle défausse au hasard ; non offerte avec une main vide.
- [ ] **X-S Sentinel I (`uw017`)** : les mots-clés « ranged » et « overkill » (non observés dans les cas de test).
- [ ] **Téléphone** : voiles (`uw015` garde une ligne de traits anglaise en haut ; à signaler si gênant).

## 10. Raza Longknife — deck « Raza Longknife » (Rhino)

Pack `rl`, 21 cartes, créateurs Phenexian et Mysteltainn.

- [ ] **Partie complète** avec la tuile « Raza Longknife ».
- [ ] **Alien Augmentations (`rl001a`)** : +1 PV par amélioration TECH ou WEAPON **non attachée à une autre carte** que vous contrôlez ; regarder le PV quand on
  joue ou défausse des améliorations.
- [ ] **Raza's Cybernetic Arm (`rl008`)** : une attaque qui amène Raza à 5 dégâts ou plus déclenche Retaliate.
- [ ] **Warrior Apotheosis (`rl005`)** : le choix des sbires à engager (liste de cases à cocher).
- [ ] **Symbiote Possession (`rl014`)** : tant qu'on est engagé avec Zzzxx, on ne peut pas l'attaquer ni contrer d'autres manigances.
- [ ] **New Host (`rl016`)** : le sbire défaussé est révélé et engagé avec vous, puis New Host s'y attache ; la Réponse forcée cherche Zzzxx.
- [ ] **Shi'ar Host (`rl015`) / New Host** : leur boost (sans cas de test propre).
- [ ] **Téléphone** : voile de New Host (`rl016`).

## 11. Spider-Punisher — deck « Spider-Punisher » (Rhino)

Pack `sq`, 18 cartes, créateur T-Wrecks.

- [ ] **Partie complète** avec la tuile « Spider-Punisher ».
- [ ] **Web-Sling (`sq001a`)** : en fin de phase des joueurs, pour chaque deux améliorations redressées, 1 dégât à un ennemi ou 1 menace retirée.
- [ ] **Enhanced Combat Sense (`sq002`)** : payée avec **plusieurs** améliorations Weapon ou Tech épuisées (ressources wild).
- [ ] **Incendiary Rounds (`sq011`)** : l'autoplay a parfois bloqué dessus (cause non prouvée) : vérifier que son paiement marche en vrai.
- [ ] **The Goblin's Ultimatum (`sq015`)** jusqu'à l'obligation ; **Punisher No More (`sq013`)**.
- [ ] **AERIAL** : le trait s'affiche sur l'identité quand les conditions sont réunies (`sq005`, `sq012`).
- [ ] **Téléphone** : voile de `sq015` (première lettre au bord gauche, limite connue).

## 12. Batgirl — deck « Batgirl » (Rhino)

Pack `bg`, 24 cartes, créateur ES.

- [ ] **Partie complète** avec la tuile « Batgirl » ; le choix « Batgirl (Bat Family) » dans le sélecteur d'identité (à confirmer).
- [ ] **The Oracle (`bg001a`)** : à la résolution d'une carte du pack, changer l'icône de ressource d'un texte ; une fois par round.
- [ ] **Eidetic Memory (`bg001b`)** : remonter la carte la plus ancienne de la défausse avec le type de ressource choisi (lecture à confirmer).
- [ ] **Batarangs (`bg005`)** : payée avec une ressource **wild**, le jeu demande le type déclaré ; effet selon le type (énergie : sonne, physique : 2 dégâts, …).
- [ ] **Utility Belt (`bg012`)** : l'Action facultative « réduire le coût du prochain événement de 1 » se lit **avant** de jouer l'événement ; seulement en forme
  héros ; +1 taille de main en fin de phase si elle est prête.
- [ ] **Grapple Line (`bg011`)** : un compteur « recon » seulement si payée avec une ressource physique ; l'Action redresse un personnage et pioche si le
  compteur est là.
- [ ] **Return of the Mask (`bg014`)** : la manigance et le sbire Black Mask au début de la partie (image et voile).
- [ ] **Téléphone** : fenêtre de choix du type de wild ; voiles (`bg014`, `bg001a` : petit défaut connu).

## 13. Hepzibah — deck « Hepzibah » (Klaw ou Rhino)

Pack `hz`, 19 cartes, créateurs Phenexian et Mysteltainn. Le deck de départ n'a pas de decklist d'auteur : choisir ses cartes d'aspect.

- [ ] **Partie complète** avec la tuile « Hepzibah ».
- [ ] **Response d'Hepzibah (`hz001a`)** : après un événement, la fenêtre « Resolve the "Special" ability on a card in your hand » permet de choisir la carte.
- [ ] **Targeting Goggles (`hz003`)** : cherche un événement dans le deck ; **sans événement dans le deck, rien n'est remis sur le deck et le jeu le dit**
  (bulle d'avis, aussi sur téléphone).
- [ ] **Energy Blaster (`hz005`)** : un méchant vaincu par l'action déclenche le Special d'une carte en main.
- [ ] **Feral Rage (`hz007`)** : son Special résolu en phase du méchant donne +1 ATQ jusqu'à la fin de la phase des joueurs **suivante**.
- [ ] **Armed to the Teeth (`hz010`)** : la fenêtre « Choose one » à deux branches.
- [ ] **Vendetta (`hz011`)** : forcée en forme héros quand un sbire entre en jeu ; l'écran doit montrer la bascule.
- [ ] **The Vengeful Wing (`hz014`)** : la fenêtre « Assign N damage » (répartition des dégâts indirects).
- [ ] **Téléphone** : Kill Order (`hz013`) en paysage ; fenêtre de choix du Special.

## 14. Smasher — deck « Smasher » (Klaw ou Rhino)

Pack `sz`, 19 cartes, créateur Phenexian. Smasher joue des améliorations « Exospex » ; une seule peut être en jeu.

- [ ] **Partie complète** avec la tuile « Smasher » (alter ego au départ, bascule en héros).
- [ ] **Battle Ready (`sz001b`)** : Action d'alter ego, **une fois par tour**, cherche une Exospex dans le deck **et** la défausse (sur téléphone, la fenêtre doit
  s'ouvrir avec les deux piles).
- [ ] **Accessing (`sz004`)** : la fenêtre (amélioration puis cible) ; l'effet compte comme une **attaque**.
- [ ] **Penta-Vision (`sz005`), Hyper-Strength (`sz006`), Exo-Flight (`sz009`)** : le choix de la cible des Hero Responses jouées de la main ; Hyper-Strength :
  l'attaque a « overkill ».
- [ ] **Power Couple (`sz015`)** : le Team-Up depuis le deckbuilder (Basic, max 1 par deck) avec un vrai Cannonball en jeu.
- [ ] **Téléphone** : Entropic Subversion (`sz012`) en paysage ; fenêtre de Battle Ready.

## 15. Sunspot — deck « Sunspot (Hellfire Hunt) » (Klaw ou Rhino)

Pack `so`, 17 cartes, créateur Dipsome. Sunspot accumule des compteurs « solaire » ; à zéro, il bascule en alter ego.

- [ ] **Partie complète** avec la tuile « Sunspot », y compris le basculement forcé en alter ego quand le stock tombe à zéro.
- [ ] **Images des deux faces** : la carte héros (`so001a`) montre bien **Sunspot**, l'alter ego (`so001b`) montre Roberto Da Costa (inversion corrigée
  le 26/10/2026).
- [ ] **Solar Rechanneling (`so001a`)** : la saisie du nombre X (liste de nombres du stock) à l'écran ; aussi pour Radiant Disruption (`so005`) et
  Solar Flare (`so007`).
- [ ] **Blessings of the Sun (`so004`)** : l'ordre des deux fenêtres quand on combine avec Solar Rechanneling pendant une défense.
- [ ] **Radiant Disruption (`so005`)** : si Sunspot est AERIAL, la seconde manigance est **obligatoire** (le joueur choisit seulement laquelle).
- [ ] **Superhuman Mutants Murdering (`so013`)** : image en paysage, icône Hazard ; après chaque activation de Donald Pierce contre vous, **une** activation
  de plus (sans rebond).
- [ ] **Donald Pierce (`so014`)** : Quickstrike (il attaque à l'engagement) ; les trois boosts de némésis (3, 3 et 1 icônes) sans effet imprimé.
- [ ] **Téléphone** : saisie de X au doigt ; voile de `so014`.

---

## 16. Les 50 cartes d'aspect Starjammers (pack `sy`, créateurs Phenexian et Mysteltainn)

Elles complètent Corsair, Hepzibah, Raza, Ch'od, Rachel Summers et Smasher. Pas de deck de départ à elles : ce sont des cartes du **deckbuilder**.

- [ ] **Deckbuilder** : avec un héros Starjammer (Corsair, Hepzibah, Raza, Ch'od, Smasher, Marvel Girl), les 50 cartes sont proposées (Basic 15,
  Agressivité 9, Justice 8, Leadership 9, Protection 9) ; **Blade of the Phoenix (`sy018`) et Thorn Crew (`sy043`) ne sont PAS proposées** (cartes liées,
  mises de côté par leur carte) ; les plafonds « 1 max » / « 2 max » par deck sont respectés.
- [ ] **Alliés et Team-Up** : Corsair (`sy002`), Hepzibah (`sy003`), Ch'od (`sy001`), Raza (`sy006`) ; Life-Bonded Crewmates (`sy007`, Corsair × Hepzibah) et
  Steadfast Companions (`sy008`, Ch'od × Raza) se jouent quand les deux héros sont en jeu.
- [ ] **Corsair, allié (`sy002`)** : après l'avoir jouée depuis la main, les cartes payées se glissent dessous ; la Réponse ajoute une carte glissée à la main.
- [ ] **Freedom Fighters (`sy027`)** : quand le vilain s'active contre un joueur, épuiser un personnage STARJAMMER et un X-MEN **annule l'activation** et
  retire des menaces.
- [ ] **Far-Flung Family (`sy037`)** : cherche un allié STARJAMMER et un allié X-MEN dans les decks ; les deux entrent épuisés. À 2 joueurs, chacun cherche ce
  qui manque.
- [ ] **Kalyx (`sy042`) et Thorn Crew (`sy043`)** : Kalyx trouve Thorn Crew et le met en jeu ; ses utilisations de pouvoir de base mettent le haut du deck en
  jeu face cachée comme allié THORN (1 THW, 1 ATK, 1 PV) ; l'allié vaincu va à la défausse de son propriétaire.
- [ ] **Korvus Rook'shir (`sy017`) et Blade of the Phoenix (`sy018`)** : la lame se pose sur l'allié, +2 ATK, dégâts consécutifs s'il n'est pas PSIONIC.
- [ ] **Center Section Garden (`sy010`)** : après une récupération de base en alter ego, soigne 2 dégâts de l'identité ou d'un personnage STARJAMMER.
- [ ] **Alliance** : les cartes marquées Alliance (Freedom Fighters, Far-Flung Family) se paient à plusieurs à 2 joueurs.
- [ ] **Téléphone** : une action qui cherche dans le deck ET la défausse (par exemple avec Kalyx) ouvre la fenêtre à deux colonnes ; les 50 voiles français
  (`sy042` est en voile uni ; `sy038`, `sy024`, `sy025`, `sy029` ont de petits défauts connus).

---

## 17. À vérifier une seule fois, pour tous les héros

- [ ] **Fenêtre de choix du type de wild** (Polymath de Ch'od, Batarangs de Batgirl) : elle apparaît bien et le choix est pris en compte.
- [ ] **Collections de ressources Energy / Genius / Strength** : dans la modale des arts alternatifs, chaque héros propose sa collection ; la carte officielle et le reskin
  comptent comme la même carte pour « Max 1 par deck ».
- [ ] **Alliance à 2 joueurs** : un coût d'une carte Alliance peut être payé par les deux joueurs (Shi'ar Battle Cruiser, Freedom Fighters, Far-Flung Family).
- [ ] **Fenêtre de choix à deux colonnes (PC)** : cliquer le deck ou la défausse ouvre une seule fenêtre avec les deux, Deck à gauche et Défausse à droite ;
  choisir un allié puis une amélioration (par exemple avec Suit Up de Laura Kinney, ou Battle Ready de Smasher).
- [ ] **Téléphone, choix dans plusieurs piles** : la fenêtre s'ouvre toute seule ; la fermer sans annuler fait **clignoter l'onglet « Piles »** et affiche le bandeau
  « Choisis une carte · Rouvrir » ; « Annuler » affiche « Action annulée ».
- [ ] **Bulle d'avis « aucun résultat »** : Safe House #30 du Winter Soldier officiel (sans sbire dans le deck de rencontre : pas de pioche, avis affiché) et
  Targeting Goggles d'Hepzibah (sans événement dans le deck). Aussi sur téléphone.
- [ ] **Safe House #30 avec un sbire** : le sbire arrive engagé, une carte est piochée (le cas qui s'était mal passé en partie réelle).
- [ ] **Grille « Fan-made » et sa ligne de remerciement** : « Héros (créateur) » derrière chaque nom ; Phenexian et Mysteltainn comptés comme deux personnes.
- [ ] **Écran « Choisis ton héros »** : aller de la tuile vers le bouton « Voir ses cartes » sans que le héros affiché change en route ; cliquer le bouton ouvre ses
  cartes.
- [ ] **Page Crédits** et volet des créateurs sur l'accueil : 27 créateurs listés, avec leurs contenus.
- [ ] **Nouveautés** : les deux entrées du 26/10/2026 (15 héros, 50 cartes d'aspect) avec leurs créateurs.
- [ ] **Voiles français** : cartes à deux faces et paysage lisibles ; défauts connus à signaler seulement s'ils gênent (liste dans
  `docs/rapports/2026-10-26-problemes-a-corriger.md`, partie C).

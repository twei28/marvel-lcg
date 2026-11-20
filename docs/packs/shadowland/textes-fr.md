# Shadowland (MC65) : textes francais

Traduction du 22/10/2026 des 93 faces, **proposee et non validee en jeu**. Sources : `.planning/shadowland/traductions/fr_toutes.json` (3 traducteurs, puis harmonisation). Pas de VF officielle du pack : tout est base sur le francais officiel du corpus du jeu (`ui-app/src/board/textes-fr-complets.ts`). Destination finale : `TEXTES_FR_FANMADE` dans `ui-app/src/board/textes-fr-fanmade.ts` (une entree par `card_id` `slNNN[a|b]`, exemplaires multiples compris) ; **rien n'a ete ajoute au code**.

## Decisions de traduction

- **Tranche par l'utilisateur (22/10/2026)** : intertitres des pieges **Éviter / Désamorcer / Trébucher** (Avoid / Disarm / Trip) ; **noms de sets laisses en anglais** (Shadows in the Night, Dark Protégé, Ninja Swarm, Shadow Labyrinth, Deadly Contraptions).
- **Corpus officiel** : « Une fois révélée / vaincu / déjouée » (selon le genre, `When Defeated` d'une manigance annexe = « Une fois déjouée »), « ce stade est achevé », « phase du Méchant » (M majuscule), « dépensez les ressources suivantes : [energy] [energy] », « Liée / Lié (X) » selon le genre du type de carte, événements `[[ATTAQUE]]`, `[[CONTRE]]`, `[[DÉFENSE]]`, `[[ÉLITE]]`.
- **Termes nouveaux retenus (a valider)** : « position du méchant / du héros » (calque), « compteur de passage », « deck Piège » et « pile de défausse Piège » (trap deck / trap discard pile), « jeton Corruption » (corruption counter, comme « jeton Retard » du corpus), « déjouement de base » (basic thwart), « face A / face B » du méchant, trait `PIÈGE !` (TRAP!).
- Noms de cartes et traits non officiels (OVERPOWERING, POSSESSED, HAND...) restes en anglais.

## sl001a — A Barricade of Blades (MAIN SCHEME 1A)

> <b>Contenu</b> : les sets de rencontre Shadows in the Night, Dark Protégé et Standard. Un set de rencontre modulaire <i>(Ninja Swarm)</i>.
> <b>Mise en place</b> : mettez en jeu chaque environnement The Streets Below. Mettez de côté le set de rencontre Dark Protégé. Choisissez 1 méchant au hasard dans ce set et révélez sa face A, puis mélangez chaque carte liée à ce méchant dans le deck Rencontre.

Notes du traducteur : Noms de sets de rencontre (Shadows in the Night, Dark Protégé, Ninja Swarm) laisses en anglais comme noms propres ; le corpus officiel traduit parfois les noms de sets (ex. Le Siège des Morlocks), a trancher : propositions Ombres dans la Nuit / Protégé Obscur / Nuée de Ninjas. | « carte liée à ce méchant » = card linked to that villain (mot-cle Linked), formulation de ma part.

## sl001b — A Barricade of Blades (MAIN SCHEME 1B)

> En mode expert, le méchant gagne +1 MNG et +3[per_hero] points de vie.
> <b>Interruption forcée</b> : quand le méchant est censé être vaincu côté face A, retournez-le plutôt sur sa face B, réinitialisez ses points de vie et changez la position du méchant. Attribuez 1 carte Rencontre face cachée à chaque joueur.
> <b>Si le méchant est vaincu côté face B, les joueurs gagnent la partie.</b>

Notes du traducteur : « côté face A » : le corpus dit « face A/face B » ; « retournez-le plutôt » = « instead flip it » (le corpus utilise « à la place »). Ordre des clauses conserve.

## sl002a — Fortress Lockdown (MAIN SCHEME 2A)

> <i>Alors que les forces à l'extérieur retiennent les héros, les ninjas à l'intérieur verrouillent chaque porte et chaque fenêtre.</i>
> En mode expert, le méchant gagne +3[per_hero] points de vie.
> <b>Une fois révélée</b> : changez la position du méchant. Chaque joueur cherche un sbire dans le deck Rencontre et la pile de défausse et le révèle. <i>(Mélangez.)</i>

## sl002b — Fortress Lockdown (MAIN SCHEME 2B)

> En mode expert, le méchant gagne +1 MNG et +3[per_hero] points de vie.
> <b>Interruption forcée</b> : quand le méchant est censé être vaincu côté face A, retournez-le plutôt sur sa face B, réinitialisez ses points de vie et changez la position du méchant. Attribuez 1 carte Rencontre face cachée à chaque joueur.
> <b>Si le méchant est vaincu côté face B, les joueurs gagnent la partie.</b>
> <b>Si ce stade est achevé, les joueurs perdent la partie.</b>

## sl003a — The Streets Below (ENVIRONMENT)

> <b><i>POSITION DU MÉCHANT.</i></b>
> Si les deux positions sont identiques :
> • Chaque personnage gagne +1 ATQ.
> Si les positions sont différentes :
> • Diminuez de 1 la quantité de dégâts subis par chaque personnage lors de chaque attaque.
> • Les menaces ne peuvent pas être retirées de la manigance principale.

## sl003b — Atop the Tenshu (ENVIRONMENT)

> <b><i>POSITION DU MÉCHANT.</i></b>
> Si les deux positions sont identiques :
> • Chaque personnage gagne +1 ATQ.
> Si les positions sont différentes :
> • Diminuez de 1 la quantité de dégâts subis par chaque personnage lors de chaque attaque.
> • Les menaces ne peuvent pas être retirées de la manigance principale.

## sl004a — The Streets Below (ENVIRONMENT)

> <b><i>POSITION DU HÉROS.</i></b>
> <b>Action de premier joueur</b> : résolvez l'un des effets ci-dessous, puis retournez cette carte :
> • Placez 3 menaces sur la manigance principale et sonnez votre identité.
> • Dépensez les ressources suivantes : [physical] [physical].
> • Dépensez 1 ressource de n'importe quel type et inclinez un personnage <b><i>AERIAL</i></b> que vous contrôlez.

Notes du traducteur : Le trait <b><i>AERIAL</i></b> est recopie tel quel (balises et anglais conserves) comme dans la source.

## sl004b — Atop the Tenshu (ENVIRONMENT)

> <b><i>POSITION DU HÉROS.</i></b>
> <b>Action de premier joueur</b> : résolvez l'un des effets ci-dessous, puis retournez cette carte :
> • Infligez 3 dégâts à votre identité.
> • Dépensez les ressources suivantes : [energy] [energy].
> • Défaussez un allié ou une amélioration que vous contrôlez.

## sl005 — Black Tarantula (MINION)

> Garde.
> <b>Une fois révélé</b> : changez la position du méchant si elle n'a pas changé durant cette phase. Si la position du méchant est Atop the Tenshu, Black Tarantula vous attaque ; sinon, donnez une carte d'état Tenace au méchant et à Black Tarantula.

Notes du traducteur : « Une fois révélé » (masculin) pour un sbire, comme le corpus (ex. 03027) ; le glossaire donne « révélée » par defaut.

## sl006 — Ghost Maker (MINION)

> <b>Une fois vaincu</b> : changez la position du méchant si elle n'a pas changé durant cette phase. Si la position du méchant est Atop the Tenshu, défaussez 1 carte que vous contrôlez ; sinon, subissez 2 dégâts indirects.
> <b>[star] Boost</b>: si un allié défend contre cette attaque, révélez ce sbire.

## sl007 — Sealed Entrances (SIDE SCHEME)

> Assaut. <i>(Les contres de base contre cette manigance utilisent l'ATQ à la place de la CTR.)</i>
> <b>Une fois déjouée</b> : changez la position du méchant si elle n'a pas changé durant cette phase.

Notes du traducteur : When Defeated sur une manigance annexe rendu par « Une fois déjouée » (VF officielle pour les manigances) et non « Une fois vaincu ».

## sl008 — Strategic Positioning (SIDE SCHEME)

> <i>Sous Shadowland, la Main règne sur les rues.</i>
> Tant que la position du méchant est The Streets Below, cette manigance gagne 1 icône d'accélération ([acceleration]).
> Tant que la position du méchant est Atop the Tenshu, cette manigance gagne 1 icône d'aléa ([hazard]).

Notes du traducteur : « la Main » (Hand) traduit en prose, comme dans la VF des comics ; le trait [[Hand]] reste anglais. | Shadowland laisse en anglais (nom propre d'evenement).

## sl009 — Surround the Fortress (SIDE SCHEME)

> <b>Une fois révélée</b> : changez la position du méchant si elle n'a pas changé durant cette phase. Si la position du méchant est Atop the Tenshu, placez 1[per_hero] menace sur la manigance principale ; sinon, placez 1[per_hero] menace sur cette manigance.

Notes du traducteur : « here » rendu par « sur cette manigance ».

## sl010 — Chaos in Hell's Kitchen (TREACHERY)

> <b>Une fois révélée</b> : changez la position du méchant si elle n'a pas changé durant cette phase. Si la position du méchant est Atop the Tenshu, placez 2 menaces sur la manigance principale ; sinon, subissez 2 dégâts.
> <b>[star] Boost</b>: résolvez la capacité « <b>Une fois révélée</b> » de cette carte.

## sl011 — Moonlit Silhouette (TREACHERY)

> <b>Une fois révélée (alter ego)</b> : changez la position du méchant si elle n'a pas changé durant cette phase. Vous êtes désorienté.
> <b>Une fois révélée (héros)</b> : si la position du méchant est Atop the Tenshu, le méchant manigance ; sinon, le méchant vous attaque.

## sl012a — Archpriestess (VILLAIN A)

> [star] <b>Réponse forcée</b> : après qu'Archpriestess vous a attaqué, donnez une carte d'état Tenace à un sbire. Si aucune carte d'état Tenace n'a été placée ainsi, défaussez les 3 cartes du dessus du deck Rencontre, puis attribuez-vous 1 sbire défaussé ainsi en tant que carte Rencontre face cachée.

## sl012b — Archpriestess (VILLAIN B)

> Solide. Ténacité.
> [star] <b>Réponse forcée</b> : après qu'Archpriestess vous a attaqué, donnez une carte d'état Tenace à un sbire. Si aucune carte d'état Tenace n'a été placée ainsi, défaussez les 3 cartes du dessus du deck Rencontre, puis attribuez-vous 1 sbire défaussé ainsi en tant que carte Rencontre face cachée.

## sl013a — Daredevil (VILLAIN A)

> <b>Réponse forcée</b> : après que vous ou un allié que vous contrôlez a attaqué Daredevil, choisissez : soit vous défaussez 1 carte prise au hasard dans votre main, soit Daredevil vous attaque. (Limite d'une fois par round par joueur.)

Citation : « Hell's Kitchen est désormais sous la protection de la Main ! »

Notes du traducteur : Hell's Kitchen laisse en anglais (nom propre) ; « la Main » comme en 65008.

## sl013b — Daredevil (VILLAIN B)

> Solide. Ténacité.
> <b>Réponse forcée</b> : après que vous ou un allié que vous contrôlez a attaqué Daredevil, choisissez : soit vous défaussez 1 carte prise au hasard dans votre main, soit Daredevil vous attaque. (Limite d'une fois par round par joueur.)

## sl014a — Elektra (VILLAIN A)

> [star] <b>Interruption forcée</b> : quand Elektra vous attaque, défaussez la carte du dessus de votre deck. Si le coût imprimé de cette carte est un nombre impair, Elektra gagne +1 ATQ pour cette attaque ; sinon, cette attaque gagne Déferlement et Perçant.

Citation : « La Main me guide, et la mort me suit. »

## sl014b — Elektra (VILLAIN B)

> Solide. Ténacité.
> [star] <b>Interruption forcée</b> : quand Elektra vous attaque, défaussez la carte du dessus de votre deck. Si le coût imprimé de cette carte est un nombre impair, Elektra gagne +1 ATQ pour cette attaque ; sinon, cette attaque gagne Déferlement et Perçant.

## sl015a — Gorgon (VILLAIN A)

> [star] <b>Interruption forcée</b> : quand Gorgon vous attaque, choisissez :
> • Dépensez une ressource [physical].
> • Sonnez votre identité.
> • Subissez 2 dégâts indirects.

Citation : « J'ai connu la mort et la renaissance. Il n'y a rien que je craigne. »

## sl015b — Gorgon (VILLAIN B)

> Solide. Ténacité.
> [star] <b>Interruption forcée</b> : quand Gorgon vous attaque, choisissez :
> • Dépensez une ressource [physical].
> • Sonnez votre identité.
> • Subissez 2 dégâts indirects.

## sl016a — Lady Bullseye (VILLAIN A)

> [star] <b>Réponse forcée</b> : après que Lady Bullseye vous a attaqué, si cette attaque n'a pas été défendue, subissez 1 dégât indirect ; sinon, placez 1 menace sur la manigance principale.

Citation : « Je compte prendre mon temps avec toi. »

Notes du traducteur : Citation : tutoiement « toi » choisi (menace face a face) ; vouvoiement possible.

## sl016b — Lady Bullseye (VILLAIN B)

> Solide. Ténacité.
> [star] <b>Réponse forcée</b> : après que Lady Bullseye vous a attaqué, si cette attaque n'a pas été défendue, subissez 1 dégât indirect ; sinon, placez 1 menace sur la manigance principale.

## sl017a — White Tiger (VILLAIN A)

> [star] <b>Réponse forcée</b> : après que White Tiger vous a attaqué, elle vous attaque de nouveau avec +1 ATQ. (Limite d'une fois par round par joueur.)

Citation : « La civilisation sombrera dans le chaos et les ténèbres, et nous qui suivons la voie de la main gauche nous agenouillerons devant la Bête ! »

Notes du traducteur : Citation : « left-hand path » rendu par « voie de la main gauche » (expression consacree).

## sl017b — White Tiger (VILLAIN B)

> Solide. Ténacité.
> [star] <b>Réponse forcée</b> : après que White Tiger vous a attaqué, elle vous attaque de nouveau. (Limite d'une fois par round par joueur.)

## sl018 — Art of the Kill (ATTACHMENT)

> Lié (Elektra, Lady Bullseye ou White Tiger).
> Attachez cette carte à votre identité.
> <b>Interruption forcée</b> : quand un ennemi vous attaque, il gagne +1 ATQ pour cette attaque. Si cette attaque vainc un personnage, placez 1 menace sur la manigance principale.
> <b>Action d'alter ego</b> : dépensez les ressources suivantes : [energy] [mental] [physical] → défaussez cette carte.

Notes du traducteur : « Si cette attaque vainc un personnage » : formulation de ma part (corpus : « est vaincu par cette attaque »).

## sl019 — Krahllak's Blessing (ATTACHMENT)

> Lié (Archpriestess, Daredevil ou Gorgon).
> Attachez cette carte au méchant.
> <b>Interruption forcée</b> : quand le méchant attaché est censé subir une quantité quelconque de dégâts infligés par un personnage, diminuez cette quantité de 3. Le méchant attaché attaque ce personnage. Défaussez cette carte.

## sl020 — Archpriestess (MINION)

> Lié (Gorgon, Lady Bullseye ou White Tiger).
> Vilenie.
> <b>Une fois révélé</b> : chaque autre sbire engagé avec vous vous attaque. Si aucune attaque n'a été effectuée ainsi, défaussez les 3 cartes du dessus du deck Rencontre.

Notes du traducteur : « Une fois révélé » masculin pour un sbire.

## sl021 — Gorgon (MINION)

> Lié (Daredevil, Elektra ou Lady Bullseye).
> Garde. Vilenie.
> <b>Réponse forcée</b> : après qu'un personnage a attaqué Gorgon et lui a infligé des dégâts, sonnez ce personnage.

## sl022 — Lady Bullseye (MINION)

> Lié (Archpriestess, Gorgon ou Lady Bullseye).
> Vilenie.
> [star] <b>Interruption forcée</b> : quand Lady Bullseye vous attaque, cette attaque gagne À Distance et elle attaque l'allié ayant le coût imprimé le plus élevé que vous contrôlez, si possible.

Notes du traducteur : Linked->Lié/Liée (X, Y ou Z) : aucune occurrence officielle de la liste à 3 noms ; accord au genre de la carte, "or" -> "ou" (Lié : sbire, masculin)

## sl023 — White Tiger (MINION)

> Lié (Archpriestess, Daredevil ou Elektra).
> Vilenie.
> <b>Une fois révélée</b> : subissez 2 dégâts indirects.

Notes du traducteur : Linked->Lié/Liée (X, Y ou Z) : aucune occurrence officielle de la liste à 3 noms ; accord au genre de la carte, "or" -> "ou"

## sl024 — Rite of Offering (SIDE SCHEME)

> Liée (Archpriestess, Elektra ou White Tiger).
> <b>Une fois déjouée</b> : le joueur qui a déjoué cette manigance retire de la partie un allié qu'il contrôle. Si aucun allié n'a été retiré par cet effet, ce joueur subit 3 dégâts.

Notes du traducteur : Linked->Lié/Liée (X, Y ou Z) : aucune occurrence officielle de la liste à 3 noms ; accord au genre de la carte, "or" -> "ou" | "When Defeated" sur une manigance annexe rendu "Une fois déjouée" (usage officiel pour les manigances, ex. 04070), et "le défaiteur" -> "le joueur qui a déjoué cette manigance"

## sl025 — Shadowy Plot (SIDE SCHEME)

> Liée (Daredevil, Gorgon ou Lady Bullseye).
> <b>Une fois déjouée</b> : le joueur qui a déjoué cette manigance regarde les 3 cartes du dessus du deck Rencontre, en révèle 1 et défausse les autres.

Notes du traducteur : Linked->Lié/Liée (X, Y ou Z) : aucune occurrence officielle de la liste à 3 noms ; accord au genre de la carte, "or" -> "ou" | "When Defeated" sur une manigance annexe rendu "Une fois déjouée" (usage officiel pour les manigances, ex. 04070), et "le défaiteur" -> "le joueur qui a déjoué cette manigance"

## sl026 — Darkness Within (TREACHERY)

> Liée (Archpriestess, Gorgon ou Lady Bullseye).
> <b>Une fois révélée</b> : passez sous forme de héros. Le méchant vous attaque.
> ---
> [star] <b>Boost</b> : si cette activation est une attaque, elle gagne Déferlement.

Notes du traducteur : Linked->Lié/Liée (X, Y ou Z) : aucune occurrence officielle de la liste à 3 noms ; accord au genre de la carte, "or" -> "ou"

## sl027 — Embraced by Darkness (TREACHERY)

> Liée (Daredevil, Elektra ou White Tiger).
> <b>Une fois révélée</b> : le méchant manigance. Si 2 menaces ou moins ont été placées sur la manigance principale par cet effet, défaussez les 3 cartes du dessus du deck Rencontre.
> ---
> [star] <b>Boost</b> : si cette activation est une attaque, placez 2 menaces sur la manigance principale.

Notes du traducteur : Linked->Lié/Liée (X, Y ou Z) : aucune occurrence officielle de la liste à 3 noms ; accord au genre de la carte, "or" -> "ou"

## sl028 — Black Mountain (MINION)

> Garde.
> Tant que Black Mountain est engagé avec vous, chaque autre sbire [[NINJA]] engagé avec vous ne peut pas être attaqué.
> <b>★ Boost</b> : si un allié défend contre cette attaque, révélez ce sbire.

Notes du traducteur : doute : le Boost « reveal this minion » est rendu littéralement (révélez ce sbire) ; le sens exact est à confirmer sur le scan

## sl029 — Kirigi (MINION)

> Collaboration ([[NINJA]]).
> <b>Une fois vaincu</b> : le joueur qui a vaincu Kirigi dépense soit 2 ressources de n'importe quel type, soit mélange Kirigi dans le deck Rencontre.
> <b>★ Boost</b> : si un allié défend contre cette attaque, cette carte gagne [boost][boost] et cette attaque gagne Déferlement.

Notes du traducteur : Teamwork -> Collaboration (officiel, ex. 32159)

## sl030 — Bo Staff Ninja (MINION)

> Collaboration ([[NINJA]]). Ténacité.
> <b>Une fois vaincu</b> : le joueur qui l'a vaincu défausse les 2 cartes du dessus du deck Rencontre et révèle le premier sbire doté du mot-clé Collaboration défaussé par cet effet.

Notes du traducteur : Teamwork -> Collaboration (officiel, ex. 32159) | "keyword" -> "mot-clé" (officiel, ex. 08033)

## sl031 — Fukiya Ninja (MINION)

> Collaboration ([[NINJA]]).
> ★ Les attaques de ce sbire gagnent À Distance.
> <b>Une fois vaincu</b> : le joueur qui l'a vaincu défausse les 2 cartes du dessus du deck Rencontre et révèle le premier sbire doté du mot-clé Collaboration défaussé par cet effet.

Notes du traducteur : Teamwork -> Collaboration (officiel, ex. 32159)

## sl032 — Katana Ninja (MINION)

> Garde. Collaboration ([[NINJA]]).
> <b>Une fois vaincu</b> : le joueur qui l'a vaincu défausse les 2 cartes du dessus du deck Rencontre et révèle le premier sbire doté du mot-clé Collaboration défaussé par cet effet.

Notes du traducteur : Teamwork -> Collaboration (officiel, ex. 32159)

## sl033 — Kusarigama Ninja (MINION)

> Patrouille. Collaboration ([[NINJA]]).
> <b>Une fois vaincu</b> : le joueur qui l'a vaincu défausse les 2 cartes du dessus du deck Rencontre et révèle le premier sbire doté du mot-clé Collaboration défaussé par cet effet.

Notes du traducteur : Teamwork -> Collaboration (officiel, ex. 32159)

## sl034 — Shuriken Ninja (MINION)

> Collaboration ([[NINJA]]).
> ★ Les attaques de ce sbire gagnent Perçant.
> <b>Une fois vaincu</b> : le joueur qui l'a vaincu défausse les 2 cartes du dessus du deck Rencontre et révèle le premier sbire doté du mot-clé Collaboration défaussé par cet effet.

Notes du traducteur : Teamwork -> Collaboration (officiel, ex. 32159)

## sl035 — Dancing Shadows (SIDE SCHEME)

> Chaque sbire [[NINJA]] gagne +1 point de vie.
> Les menaces ne peuvent pas être retirées de cette manigance tant qu'au moins 1 sbire [[NINJA]] est en jeu.
> <b>★ Boost</b> : révélez cette carte.

## sl036 — Countless Numbers (TREACHERY)

> Renfort.
> <b>Une fois révélée</b> : mélangez chaque sbire [[NINJA]] de la pile de défausse Rencontre dans le deck Rencontre.
> <b>★ Boost</b> : résolvez la capacité "<b>Une fois révélée</b>" de cette carte.

## sl037 — Shifting Corridors (VILLAIN A)

> Robuste.
> <b>★ Interruption forcée</b> : quand Shifting Corridors est censé s'activer contre vous, retirez plutôt 1 compteur de passage de cette carte et révélez la carte du dessus du deck Piège.
> <b>Si le dernier compteur de passage est retiré de cette carte, les joueurs perdent la partie.</b>

Notes du traducteur : "from here" -> "de cette carte"

## sl038a — Into the Labyrinth (MAIN SCHEME 1A)

> <b>Contenu</b> : Shifting Corridors (A). Les sets de rencontre Shadow Labyrinth, Dark Protégé, Deadly Contraptions et Standard. Un set de rencontre modulaire <i>(Ninja Swarm)</i>.
> <b>Mise en place</b> : créez le deck Piège <i>(voir livret de règles, p. 12)</i>. Mettez de côté le set de rencontre Dark Protégé. Choisissez 1 méchant au hasard dans ce set, puis mélangez dans le deck Rencontre chaque carte liée à ce méchant <i>(gardez le méchant choisi de côté)</i>.

Notes du traducteur : « voir livret de règles, p. 12 » : livret = formule officielle (04128a)

## sl038b — Into the Labyrinth (MAIN SCHEME 1B)

> <b>Une fois révélée :</b> placez 10[per_hero] compteurs de passage sur Shifting Corridors (7[per_hero] à la place en mode expert).
> <b>Interruption forcée</b> : quand Shifting Corridors est censé subir des dégâts, quel qu'en soit le montant, retirez plutôt autant de menaces de cette manigance.
> <b>Interruption forcée</b> : quand la dernière menace est retirée de cette manigance, avancez au stade 2A <i>(les joueurs gagnent en avançant)</i>.

Notes du traducteur : formule de fin reprise de 16082b

## sl039a — Chamber of Vile Secrets (MAIN SCHEME 2A)

> <b>Une fois révélée</b> : faites chacune des actions suivantes :
> 1. Mettez Shifting Corridors de côté.
> 2. Trouvez le méchant Dark Protégé choisi. Défaussez-en chaque carte d'état, chaque jeton et chaque carte attachée.
> 3. Révélez la face A du méchant choisi (face B à la place en mode expert).

## sl039b — Chamber of Vile Secrets (MAIN SCHEME 2B)

> <b>Une fois révélée</b> : en mode expert, le méchant s'active contre chaque joueur.
> <b>Réponse forcée</b> : après que vous ou un allié que vous contrôlez avez contré cette manigance, révélez la carte du dessus du deck Piège. (Limite d'une fois par round par joueur.)
> <b>Si ce stade est achevé, les joueurs perdent la partie.</b>

Notes du traducteur : « thwarts » -> « a contré » (officiel, ex. 01058) ; l'accord « avez contré » avec le sujet composé « vous ou un allié » est un doute mineur (variante : « a contré »)

## sl040 — Whisper in the Dark (ATTACHMENT)

> <i>PIÈGE !</i>
> Considérez le méchant attaché comme un sbire [[ÉLITE]] avec 6 points de vie imprimés. Il gagne : "Garde. Vilenie. <b>Une fois vaincu</b> : mettez ce sbire de côté."
> <b>Une fois révélée</b> : si Shifting Corridors est en jeu, mettez en jeu le méchant choisi mis de côté, engagé avec vous, face A visible, avec cette carte attachée ; sinon, mettez cette carte de côté et le méchant manigance.

Notes du traducteur : ELITE -> ÉLITE (usage officiel, ex. 04143) alors que les autres traits restent anglais | « Treat ... as » -> « Considérez ... comme » (officiel, ex. 34009)

## sl041 — Lord Deathstrike (MINION)

> Patrouille.
> <b>Une fois révélée</b> : si Shifting Corridors est en jeu, mélangez les 2 cartes du dessus du deck Rencontre dans le deck Piège ; sinon, révélez la carte du dessus du deck Piège.
> <b>★ Boost</b> : mettez ce sbire en jeu engagé avec vous.

## sl042 — Dead End (SIDE SCHEME)

> Assaut. <i>(Les contres de base contre cette manigance utilisent l'ATQ à la place de la CTR.)</i>
> <b>Une fois révélée</b> : si Shifting Corridors est en jeu, retirez-lui 1 compteur de passage ; sinon, placez 1[per_hero] menace sur cette carte.

Notes du traducteur : rappel d'Assaut recopié de 40087

## sl043 — Hall of Hidden Doors (SIDE SCHEME)

> <b>Une fois déjouée</b> : le joueur qui a déjoué cette manigance retire 5 menaces de la manigance principale. Il défausse des cartes du deck Rencontre jusqu'à ce qu'un sbire ou une manigance annexe soit défaussé, puis le révèle.
> <b>★ Boost</b> : placez 3 menaces sur la manigance principale.

Notes du traducteur : "When Defeated" sur une manigance annexe rendu "Une fois déjouée" (usage officiel pour les manigances, ex. 04070), et "le défaiteur" -> "le joueur qui a déjoué cette manigance"

## sl044 — No Time to Think! (TREACHERY)

> Péril. <i>(Tant que vous résolvez cette carte, les autres joueurs ne peuvent pas vous aider.)</i>
> <b>Une fois révélée</b> : le méchant s'active contre vous.
> ★ <b>Boost</b> : si cette activation est une attaque, cette carte gagne [boost][boost] et cette attaque gagne Déferlement.

## sl045 — Sudden Shift (TREACHERY)

> <b>Une fois révélée</b> : mélangez la pile de défausse Piège et les 3 cartes du dessus du deck Rencontre dans le deck Piège. Révélez la carte du dessus du deck Piège.
> ★ <b>Boost</b> : mélangez la pile de défausse Piège et les 2 cartes du dessus du deck Rencontre dans le deck Piège.

## sl046 — Nervous Jitters (ATTACHMENT)

> Attachez cette carte à votre identité.
> <b>Interruption forcée</b> : quand vous choisissez l'effet "<i>Éviter</i>" ou l'effet "<i>Désamorcer</i>" sur une carte <b>PIÈGE !</b>, nommez un type de carte Rencontre, puis défaussez la carte du dessus du deck Rencontre. Si la carte ainsi défaussée n'est pas du type nommé, subissez 4 dégâts indirects et défaussez cette carte.

Notes du traducteur : "this attachment" -> "cette carte" (pas de terme officiel pour attachement)

## sl047 — Iron Monk (MINION)

> Patrouille. Ténacité.
> Tant qu'Iron Monk est engagé avec vous, vous ne pouvez pas choisir l'effet "<i>Éviter</i>" sur les cartes <b>PIÈGE !</b>.

Citation : « Votre seul chemin passe par moi. Commençons. »

## sl048 — Hall of Punishment (SIDE SCHEME)

> <b>Interruption forcée</b> : quand vous choisissez l'effet "<i>Trébucher</i>" sur une carte <b>PIÈGE !</b>, défaussez les 3 cartes du dessus de votre deck.
> ★ <b>Boost</b> : placez 1 menace sur la manigance principale pour chaque personnage que vous contrôlez.

## sl049 — Path of a Thousand Cuts (SIDE SCHEME)

> <i>Chaque pas est une épreuve d'endurance.</i>
> <b>Interruption forcée</b> : quand vous choisissez l'effet "<i>Éviter</i>" ou l'effet "<i>Trébucher</i>" sur une carte <b>PIÈGE !</b>, subissez 2 dégâts indirects.
> ★ <b>Boost</b> : infligez 1 dégât à chaque personnage que vous contrôlez.

Notes du traducteur : ligne en italique (texte d'ambiance dans le champ texte source) traduite et laissée dans texte_fr

## sl050 — Blinding Powder (TREACHERY)

> <b>Une fois révélée</b> : choisissez :
> • <i>Éviter</i> — Défaussez un événement [[CONTRE]] de votre main.
> • <i>Désamorcer</i> — Défaussez 2 cartes prises au hasard dans votre main, puis donnez une carte d'état Tenace à un personnage que vous contrôlez.
> • <i>Trébucher</i> — Infligez 2 dégâts à votre identité et désorientez-la.

Notes du traducteur : THWART (événement) -> CONTRE (usage officiel [[CONTRE]]) | « Choisissez : » avec puces conservées comme dans la source (officiel : « Choisissez : » + tirets/puces)

## sl051 — Caltrops (TREACHERY)

> <b>Une fois révélée</b> : choisissez :
> • <i>Éviter</i> — Défaussez un événement [[DÉFENSE]] de votre main.
> • <i>Désamorcer</i> — Défaussez 1 carte spécifique à votre identité de votre main, puis infligez 2 dégâts à un ennemi.
> • <i>Trébucher</i> — Infligez 2 dégâts à votre identité et sonnez-la.

Notes du traducteur : événements ATTACK/DEFENSE en gras : traduit <b>ATTAQUE</b>/<b>DÉFENSE</b> en conservant la balise (le corpus ecrit [[ATTAQUE]] ailleurs)

## sl052 — Flame Spout (TREACHERY)

> <b>Une fois révélée</b> : choisissez :
> • <i>Éviter</i> — Défaussez un allié de votre main.
> • <i>Désamorcer</i> — Défaussez un allié que vous contrôlez, puis piochez 2 cartes.
> • <i>Trébucher</i> — Infligez 3 dégâts à votre identité. Défaussez les 3 cartes du dessus de votre deck.

## sl053 — Oil Slick (TREACHERY)

> <b>Une fois révélée</b> : choisissez :
> • <i>Éviter</i> — Défaussez une amélioration de votre main.
> • <i>Désamorcer</i> — Défaussez une amélioration que vous contrôlez, puis retirez 4 menaces de la manigance principale.
> • <i>Trébucher</i> — Défaussez 1 carte de votre main. Défaussez les 8 cartes du dessus de votre deck.

## sl054 — Poison Darts (TREACHERY)

> <b>Une fois révélée</b> : choisissez :
> • <i>Éviter</i> — Dépensez les ressources suivantes : [energy] [energy].
> • <i>Désamorcer</i> — Dépensez les ressources suivantes : [mental] [mental] [physical], puis infligez 3 dégâts au méchant.
> • <i>Trébucher</i> — Infligez 3 dégâts à votre identité et inclinez-la.

## sl055 — Pressure Plate (TREACHERY)

> <b>Une fois révélée</b> : choisissez :
> • <i>Éviter</i> — Dépensez les ressources suivantes : [mental] [mental].
> • <i>Désamorcer</i> — Dépensez les ressources suivantes : [energy] [physical] [physical], puis cherchez une carte parmi les 4 cartes du dessus de votre deck et ajoutez-la à votre main. <i>(Mélangez.)</i>
> • <i>Trébucher</i> — Défaussez des cartes du dessus du deck Rencontre jusqu'à ce qu'un sbire soit défaussé, puis révélez-le.

Notes du traducteur : rappel « (Shuffle.) » rendu « (Mélangez.) » sans « votre deck » pour rester fidele ; l'officiel ecrit « (Mélangez votre deck.) » quand c'est le deck du joueur : a trancher

## sl056 — Tripwire (TREACHERY)

> <b>Une fois révélée</b> : choisissez :
> • <i>Éviter</i> — Défaussez un événement [[ATTAQUE]] de votre main.
> • <i>Désamorcer</i> — Défaussez un soutien que vous contrôlez, puis retirez 3 menaces d'une manigance.
> • <i>Trébucher</i> — Défaussez des cartes du dessus du deck Rencontre jusqu'à ce qu'une manigance annexe soit défaussée, puis révélez-la.

Notes du traducteur : événements ATTACK/DEFENSE en gras : traduit <b>ATTAQUE</b>/<b>DÉFENSE</b> en conservant la balise (le corpus ecrit [[ATTAQUE]] ailleurs)

## sl057 — Krahllak (VILLAIN)

> Solide.
> [star] <b>Interruption</b> : quand Krahllak vous attaque, vous pouvez placer 1 jeton Corruption sur votre Creeping Corruption. Si vous le faites, Krahllak gagne –3 ATQ pour cette attaque.

Citation : "Il n'y a que la Bête !"

Notes du traducteur : Creeping Corruption laisse en anglais (nom de carte)

## sl058 — Krahllak (VILLAIN)

> Solide. Ténacité.
> [star] Les attaques de Krahllak gagnent Déferlement.
> [star] <b>Interruption</b> : quand Krahllak vous attaque, vous pouvez placer 1 jeton Corruption sur votre Creeping Corruption. Si vous le faites, Krahllak gagne –3 ATQ pour cette attaque.

## sl059 — Krahllak (VILLAIN)

> Riposte 1. Solide. Ténacité.
> [star] Les attaques de Krahllak gagnent Déferlement et Perçant.
> [star] <b>Interruption</b> : quand Krahllak vous attaque, vous pouvez placer 1 jeton Corruption sur votre Creeping Corruption. Si vous le faites, Krahllak gagne –3 ATQ pour cette attaque.

## sl060a — Dark Invitation (MAIN SCHEME 1A)

> <b>Contenu</b> : Krahllak (I) et Krahllak (II). <i>(Krahllak (II) et Krahllak (III) à la place en mode expert.)</i> Les sets de rencontre Heart of Shadow, Black Flower et Standard. Un set de rencontre modulaire <i>(Ninja Swarm)</i>.
> <b>Mise en place</b> : chaque joueur met en jeu une amélioration Creeping Corruption. Mettez le reste de côté.

Notes du traducteur : noms des sets de rencontre laisses en anglais

## sl060b — Dark Invitation (MAIN SCHEME 1B)

> <b>Interruption forcée</b> : quand ce stade est censé être achevé, retirez plutôt toutes les menaces de cette manigance et chaque joueur choisit :
> • Il place 2 jetons Corruption sur sa Creeping Corruption.
> • Il subit 3 dégâts et s'attribue 1 carte Rencontre face cachée.
> <b>Réponse forcée</b> : après que Krahllak est vaincu, avancez cette manigance au stade 2A.

Notes du traducteur : les puces • sont conservees ; le sujet de « chaque joueur choisit » est repris a la 3e personne ou a l'impératif selon le source | deal themself X facedown encounter card -> « s'attribue … face cachée » (tour officiel « attribuez-vous 1 carte Rencontre face cachée »)

## sl061a — Beast Be Praised (MAIN SCHEME 2A)

> <i>Un brasier surgit dans la salle du trône, punissant ceux qui n'ont pas encore succombé à la volonté sombre de Krahllak.</i>
> <b>Une fois révélée</b> : chaque joueur dont la Creeping Corruption a le trait [[OVERPOWERING]] défausse 1 carte prise au hasard dans sa main. Chaque autre joueur défausse une carte qu'il contrôle. En mode expert, attribuez 1 carte Rencontre face cachée à chaque joueur.

Notes du traducteur : trait OVERPOWERING laisse en anglais (trait, convention du projet) ; a harmoniser avec la ligne de traits | « from play » non rendu litteralement : « défausse une carte qu'il contrôle »

## sl061b — Beast Be Praised (MAIN SCHEME 2B)

> [star] <b>Réponse forcée</b> : après avoir résolu l'étape 1 de la phase du Méchant, chaque joueur choisit :
> • Placez 1 jeton Corruption sur votre Creeping Corruption.
> • Placez 3 menaces sur cette manigance.
> <b>Si ce stade est achevé, les joueurs perdent la partie.</b>

Notes du traducteur : les puces • sont conservees ; le sujet de « chaque joueur choisit » est repris a la 3e personne ou a l'impératif selon le source

## sl062 — Dark Shroud (ATTACHMENT)

> Attachez cette carte à Krahllak.
> <b>Interruption</b> : quand vous ou un allié que vous contrôlez êtes censés infliger 4 dégâts ou plus à Krahllak avec une attaque, prévenez plutôt tous ces dégâts, placez 1 jeton Corruption sur votre Creeping Corruption et défaussez cette carte.

## sl063 — Fear Projection (ATTACHMENT)

> Attachez cette carte à Krahllak.
> Krahllak gagne Riposte 1.
> <b>Action de héros</b> : placez 2 jetons Corruption sur votre Creeping Corruption → défaussez cette carte.
> <b>Action d'alter ego</b> : dépensez les ressources suivantes : [mental] [mental] [mental] → défaussez cette carte. Retirez 1 jeton Corruption de votre Creeping Corruption.

## sl064 — Mark of the Wicked (ATTACHMENT)

> <b>Une fois révélée</b> : vous pouvez attacher cette carte à votre identité. Si vous ne le faites pas, subissez 4 dégâts, sonnez votre identité, retirez 1 jeton Corruption de votre Creeping Corruption et défaussez cette carte.
> [star] <b>Réponse forcée</b> : après que le héros attaché a effectué une attaque de base, placez 1 jeton Corruption sur votre Creeping Corruption.

## sl065 — Pull of Power (ATTACHMENT)

> <b>Une fois révélée</b> : vous pouvez attacher cette carte à votre identité. Si vous ne le faites pas, subissez 4 dégâts, désorientez votre identité, retirez 1 jeton Corruption de votre Creeping Corruption et défaussez cette carte.
> [star] <b>Réponse forcée</b> : après que le héros attaché a effectué un déjouement de base, placez 1 jeton Corruption sur votre Creeping Corruption.

## sl066 — Fist (MINION)

> Patrouille. Riposte 2.
> <b>Action de héros</b> : placez 1 jeton Corruption sur votre Creeping Corruption → infligez 4 dégâts à Fist.

Citation : Monstruosité à moitié morte ramenée à la vie par les arts mystiques de la Hand, Fist ne s'arrêtera pas avant d'avoir accompli sa mission.

Notes du traducteur : Hand laisse en anglais (nom propre / trait [[Hand]]) dans la citation

## sl067 — Hellbride (MINION)

> <b>Une fois vaincu</b> : le joueur qui l'a vaincu place 2 jetons Corruption sur sa Creeping Corruption, puis soigne 6 dégâts de son identité.
> <b>Action de héros</b> : si Hellbride a 2 points de vie restants ou moins, inclinez votre héros → défaussez Hellbride. Retirez 1 jeton Corruption de votre Creeping Corruption.

## sl068 — Retainer (MINION)

> [star] Les attaques de Retainer gagnent Déferlement.
> [star] <b>Interruption</b> : quand Retainer vous attaque, vous pouvez placer 1 jeton Corruption sur votre Creeping Corruption. Si vous le faites, Retainer gagne –3 ATQ pour cette attaque.

Citation : L'avatar de Krahllak, invoqué pour exercer sa vengeance.

## sl069 — Snakeroot Elders (MINION)

> Tant qu'il y a au moins 1 jeton Corruption sur cette carte, Snakeroot Elders gagne Garde et Patrouille.
> <b>Une fois révélée</b> : vous pouvez placer 1 jeton Corruption sur votre Creeping Corruption. Si vous ne le faites pas, placez 1 jeton Corruption sur cette carte.

Notes du traducteur : « Une fois révélée » (forme du glossaire, comme les sbires du corpus)

## sl070 — Veil of Nightmares (SIDE SCHEME)

> <i>La magie noire de Krahllak peut puiser dans les peurs les plus profondes d'une personne.</i>
> <b>Action de héros</b> : placez 1 jeton Corruption sur votre Creeping Corruption → retirez 5 menaces de cette manigance.

Notes du traducteur : l'italique d'ambiance est dans texte_fr (comme dans le source), pas de citation_fr

## sl071 — Submit or Suffer (TREACHERY)

> <b>Une fois révélée</b> : choisissez : soit vous placez 1 jeton Corruption sur votre Creeping Corruption, soit vous retirez 1 jeton Corruption de votre Creeping Corruption et Krahllak vous attaque.
> [star] <b>Boost</b> : choisissez : soit vous placez 1 jeton Corruption sur votre Creeping Corruption, soit vous sonnez votre identité.

## sl072a — Creeping Corruption (UPGRADE A)

> Permanent. Mise en place. Max 1 par joueur.
> S'il y a au moins 5 jetons Corruption sur cette carte, retirez-les tous de cette carte et retournez-la.
> <b>Action</b> : inclinez Creeping Corruption et placez 1 jeton Corruption sur cette carte → piochez 1 carte.

## sl072b — Creeping Corruption (UPGRADE B)

> Permanent. Max 1 par joueur.
> <b>S'il y a au moins 5 jetons Corruption sur cette carte, vous êtes vaincu.</b>
> <b>Action</b> : inclinez Creeping Corruption et placez 1 jeton Corruption sur cette carte → piochez 2 cartes, puis défaussez 1 carte de votre main.

## sl073 — Aka (MINION)

> Coup Rapide. Vilenie.
> [star] <b>Interruption</b> : quand Aka est censé vous attaquer, vous pouvez placer 1 jeton Corruption sur votre Creeping Corruption. Si vous le faites, annulez cette attaque.
> [star] <b>Boost</b> : choisissez : soit vous placez 1 jeton Corruption sur votre Creeping Corruption, soit vous défaussez 1 carte prise au hasard dans votre main.

## sl074 — Tongue of the Beast (MINION)

> <b>Une fois vaincu</b> : le joueur qui l'a vaincu place 2 jetons Corruption sur sa Creeping Corruption.
> [star] <b>Boost</b> : choisissez : soit vous placez 1 jeton Corruption sur votre Creeping Corruption, soit cette carte gagne [boost][boost][boost].

## sl075 — Binding Ritual (SIDE SCHEME)

> <i>"Celui que nous servons règnera en maître !"</i>
> <i>—Takashi</i>
> <b>Une fois révélée</b> : chaque joueur choisit :
> • Il place 1 jeton Corruption sur sa Creeping Corruption.
> • Il place 3 menaces sur cette manigance.

Citation : "Celui que nous servons règnera en maître !" —Takashi

Notes du traducteur : les puces • sont conservees ; le sujet de « chaque joueur choisit » est repris a la 3e personne ou a l'impératif selon le source | la citation figure aussi dans texte_fr (italique du source) et dans citation_fr

## sl076 — Roots of a Black Flower (SIDE SCHEME)

> <b>Une fois déjouée</b> : le joueur qui l'a déjouée place 2 jetons Corruption sur sa Creeping Corruption.
> [star] <b>Boost</b> : choisissez : soit vous placez 1 jeton Corruption sur votre Creeping Corruption, soit vous placez 4 menaces sur la manigance principale.

Notes du traducteur : « When Defeated » sur une manigance annexe rendu « Une fois déjouée » (usage officiel pour les manigances, ex. 21180a) au lieu de « Une fois vaincu » : a confirmer

## sl077 — Malediction (TREACHERY)

> <b>Une fois révélée (alter ego)</b> : vous pouvez placer 2 jetons Corruption sur votre Creeping Corruption. Si vous ne le faites pas, le méchant manigance avec +2 MNG.
> <b>Une fois révélée (héros)</b> : si votre Creeping Corruption a le trait <b><i>OVERPOWERING</i></b>, le méchant manigance avec +1 MNG ; sinon, le méchant vous attaque.

Notes du traducteur : trait OVERPOWERING laisse en anglais (trait, convention du projet) ; a harmoniser avec la ligne de traits | SCH rendu MNG (stat manigance officielle)

## sl078 — Invasive Thoughts (TREACHERY)

> <b>Une fois révélée</b> : placez 1 jeton Corruption sur votre Creeping Corruption. Si elle a le trait <b><i>OVERPOWERING</i></b>, placez 1 menace sur la manigance principale ; sinon, subissez 1 dégât.
> [star] <b>Boost</b> : choisissez : soit vous placez 1 jeton Corruption sur votre Creeping Corruption, soit vous subissez 4 dégâts indirects.

Notes du traducteur : trait OVERPOWERING laisse en anglais (trait, convention du projet) ; a harmoniser avec la ligne de traits

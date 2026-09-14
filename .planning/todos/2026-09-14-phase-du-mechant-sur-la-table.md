# La phase du méchant jouée SUR LA TABLE

**Demande de l'utilisateur, 14/09/2026**, après avoir vu une vidéo de
`play.marvelsimulator.com` et m'avoir envoyé cinq captures de leur phase du
méchant.

Ce qu'il a retenu, dans ses mots : « les cartes boost sortent vraiment du
paquet pour se mettre à côté, pour ensuite voir à combien ; idem pour la carte
d'activation, elle sort du paquet et elle s'affiche, et ça j'aime vraiment
bien ; j'aime bien aussi les traits qui montrent qui va être attaqué ».

Les trois gestes racontent la même chose : **on voit d'où ça vient et où ça
va**, au lieu de le lire dans un cartouche.

## ⚠ Ceci revient sur une décision prise, et l'utilisateur le sait

La spec `docs/superpowers/specs/2026-09-07-scene-phase-mechant-design.md`,
décidée avec lui après une vraie partie (Taskmaster contre Ant-Man), dit en
décision n°2 : « plus aucune carte n'est agrandie sur place dans la table,
**plus de trait**, plus de cartouche collé à la main ».

Le premier des trois défauts qui avaient motivé ce choix est le seul qui
compte encore ici : **la table est en avance sur le récit**. Le moteur envoie
un monde déjà à jour ; la scène centrale contourne le problème en portant ses
propres chiffres et en assombrissant la table.

Le point lui a été dit avant qu'il tranche. Il a choisi la table en
connaissance de cause.

## Ce qui est décidé

Cinq questions, une à la fois.

| Question | Décision |
|---|---|
| **Où tester** | **En production, mais réservé à son compte.** ⚠ RÉPONSE RÉVISÉE, voir ci-dessous. |
| **Où jouer la phase** | **Sur la table**, comme eux. La scène centrale n'est pas utilisée dans ce mode. |
| **Rythme** | **Ça se déroule seul et vite, et ça s'arrête quand le joueur peut agir.** ⚠ RÉPONSE RÉVISÉE, voir ci-dessous. |
| **Étendue du trait** | **Tout ce qui va d'une carte à une autre** : activations du méchant et des sbires, attaques et manigances, et les effets des cartes rencontre. |
| **Remplacement** | **Un troisième mode, à côté** : « Détaillé / Sur la table / Instantané ». Rien de ce qui marche n'est touché, et ne pas le choisir suffit à revenir en arrière. |

## ⚠ Où tester : réponse révisée le 14/09/2026

Premier tour : « serveur de développement seulement, rien en production ». Puis,
plus tard : « tu pourras le déployer, mais QUE pour mon compte. Tu peux le
mettre en tant que nouveau truc de base pour mon compte. Je vois trois
possibilités différentes pour la phase du méchant, mais vraiment que pour moi. »

**Décision retenue** :
- le troisième mode part en production, mais n'est proposé qu'à son compte ;
- pour lui, il devient le mode PAR DÉFAUT ;
- les autres joueurs continuent de voir deux modes, et rien ne change pour eux.

✅ **La mécanique existe déjà, elle tourne en production depuis ce matin.**
`_est_administrateur` (`server_get.py`, écrit pour le relevé des illustrations)
et la route `/get_site_admin` : le SITE ne renseigne `site_admin_url` que pour
la table de l'administrateur, et seul le siège 0 compte. Vérifié le 14/09 en
production, un non-administrateur reçoit 403.

⚠ **À ajouter** : le plateau (`ui-app/`) ne consulte pas encore cette route.
Ses deux seuls consommateurs sont dans l'assistant (`lien-admin.js`,
`releve/app.js`). Le motif est établi, il reste à le porter.

⚠ **ET ON NE CONSTRUIT PAS UNE FORTERESSE POUR UN RÉGLAGE D'AFFICHAGE.** Cette
garde est un CONFORT, pas une sécurité : quelqu'un qui forcerait son stockage
local pour s'octroyer le mode ne verrait qu'un écran en chantier, sans rien
casser ni voir quoi que ce soit de privé. À ne pas traiter comme
`save_images_cartes`, où l'écriture, elle, devait vraiment être fermée.

## ⚠ Le rythme a été demandé DEUX FOIS, et la seconde réponse annule la première

Premier tour : « un clic par étape ». Puis, dans le message suivant :
« l'idée, c'est que ce soit assez clair sans forcément que ça prenne beaucoup
de temps », et il décrit un ENTRE-DEUX entre le mode Détaillé (« très clair »)
et le mode Instantané (« ça va très vite »).

Les deux ne tiennent pas ensemble : **le mode Détaillé a DÉJÀ un clic par
étape**. Un troisième mode au même rythme n'aurait pas été un entre-deux, juste
le même temps en plus joli. La contradiction lui a été montrée, et il a tranché
pour la troisième voie.

**Décision retenue** : ça se déroule tout seul et vite, SAUF quand le joueur a
une vraie décision à prendre (défendre, une interruption, un choix de cible) ;
là ça l'attend.

✅ **Vérifié avant de l'inscrire** : `DeroulePhase.tsx` distingue déjà les deux
sortes d'attente (`questionAuJoueur`, `attendUnAutreJoueur`, `enAttente`), et
son commentaire documente même un défaut passé où elles avaient été confondues
(« La suite arrive… » s'affichait par-dessus la question). La brique tourne,
elle est à réutiliser et non à écrire.

## Ce que la première enquête a établi

✅ **L'étendue la plus large est tenable sans toucher aux 6000 cartes.**
`FaitMechant` (`WorldStat.RecordFaitMechant`, côté Python) porte déjà
`auteur`, `cible` et le nombre en clair, et il voyage avec le monde. Le trait
se déduit donc des faits déjà émis. La limite, à dire au joueur : **ne sera
relié que ce que le moteur rapporte comme fait**. Un effet qui n'en émet pas
n'aura pas de trait, et se traitera au cas par cas.

⚠ **LE RISQUE N'EST PAS « FAIRE RECULER LA TABLE », IL EST PLUS ÉTROIT.**
Pour dessiner un trait et un montant, nul besoin de rembobiner la table : les
deux cartes y sont, à leur place. Le vrai problème est **les cartes qui ont
quitté la table pendant la phase** : sur les captures de l'utilisateur, Nick
Fury est présent à l'image 4 et absent à l'image 5. Un trait vers une carte
qui n'existe plus n'a nulle part où pointer.

Trois issues possibles : la remettre le temps de l'étape, ancrer le trait sur
sa dernière position connue, ou rejouer la phase depuis une photo du monde
d'avant.

## ✅ Preuve de faisabilité, 14/09/2026 : le risque est CONFIRMÉ et borné

**Le cas existe, il est déjà rencontré, et il est déjà documenté dans le code.**
`deroule-phase.ts` (champs `auteurNom` / `cibleNom`) :

> « Une carte morte pendant la phase (ex. un minion tué par sa propre cible) a
> disparu de l'index du monde au moment où l'étape s'affiche ; y chercher son
> nom affichait "Ultron attaque #88" à la place. »

Trois conséquences, et elles changent la conception :

1. **On sait toujours QUI.** Les faits portent `auteur` et `cible` en clair,
   précisément pour cette raison. `RecapPhaseMechant` fait le même choix pour
   la même cause. Le texte d'une étape ne peut donc pas se tromper de nom.
2. **On ne sait pas toujours OÙ.** Un trait a besoin d'une position à l'écran ;
   une carte absente de l'index du monde n'en a aucune. Le contournement
   existant ne couvre que le nom.
3. **Ce n'est pas une exception rare.** Le cas a été rencontré assez souvent
   pour que DEUX composants soient écrits en conséquence. ⚠ La fréquence n'a
   PAS été mesurée : elle reste inconnue, et ce serait une erreur de la
   présenter comme faible.

⚠ **CE QUI N'A PAS MARCHÉ, ET POURQUOI C'EST NOTÉ.** Trois tentatives de
mesure par pilotage automatique d'une vraie partie (Playwright) ont échoué : la
partie ne dépassait jamais le round 1, bloquée sur « Player Turn End », et
aucune fixture existante ne porte de `faits_mechant`. **Il n'existe donc
aujourd'hui aucun moyen simple d'observer une phase du méchant réelle hors du
navigateur.** C'est un manque d'outillage à combler avant tout chantier sérieux
sur cette phase, sans quoi chaque vérification coûtera une partie jouée à la
main.

## ⚠ LE RISQUE EST LEVÉ, ET MON DIAGNOSTIC PRÉCÉDENT ÉTAIT TROP SOMBRE

La question a été posée à l'utilisateur, qui a répondu : « on montre l'attaque
AVANT qu'il parte à la défausse ; je ne comprends pas la question ». Il avait
raison, et la question était mal posée.

Ma crainte était que le plateau ne sache plus OÙ dessiner une carte déjà
partie. Vérification faite : **il le sait**. `CoucheAnimations` tient un index
`prev` des positions écran du rendu précédent, et il s'en sert DÉJÀ pour ce cas
exact — une carte absente du rendu courant vole depuis `avant.rect`, sa
dernière place réelle, jusqu'à la défausse :

```js
for (const [id, avant] of prev) {
  if (avant.zone === 'zone-main' && defausseJoueur) {
    brouillons.push({ ..., depart: avant.rect, arrivee: defausseJoueur })
  }
}
```

C'est exactement ce dont un trait a besoin : un point d'ancrage à l'écran pour
une carte qui n'est plus là. **La brique existe, il n'y a rien à inventer.**

Le bon ordre de récit est donc celui que l'utilisateur a énoncé d'instinct :
on montre le coup avec la cible ENCORE en place, puis elle part.

## Décisions restantes

Aucune. Le chantier peut commencer.

## ⚠ Prérequis : les animations

`2026-09-14-animations-molles.md`. L'utilisateur demande ici « un entre-deux
qui fasse plus jeu de cartes, où on voit vraiment les cartes bouger ». Des
cartes molles ruineraient tout l'effet : la durée de vol est FIXE (250 ms quelle
que soit la distance), donc rien ne pèse. À traiter avant ou en même temps, pas
après.

## Ce qu'on ne fait pas

- Aucune reprise de leur code ni de leurs images : ce sont des **principes
  d'affichage** qu'on reprend, pas une mise en œuvre.
- La scène centrale du mode Détaillé n'est ni retirée ni modifiée.

## Statut

Décisions prises le 14/09/2026, **non commencé**.

Preuve de faisabilité **faite** le 14/09/2026, et **le risque est levé** : le
plateau garde déjà les positions du rendu précédent et sait ancrer une carte
disparue. Aucune décision ne reste en attente.

Reste un manque d'outillage à combler : aucun moyen simple d'observer une phase
du méchant hors du navigateur (trois tentatives de pilotage automatique ont
échoué, aucune fixture ne porte de `faits_mechant`).

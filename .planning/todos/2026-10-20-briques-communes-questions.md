# Questions ouvertes : briques moteur communes Punisher MC×DC / Galactic Storm (20/10/2026)

Branche `briques-communes`. Les trois briques sont écrites et testées (`tools/cas/briques_communes.py`, préfixe
`[briques]`) ; recette `docs/reference/RECETTES-MOTEUR.md` §15. Chaque point ci-dessous laisse un **réglage** dans
le moteur : rien n'est codé en dur, la réponse se pose dans le script de la carte ou du scénario concerné. Une
question par point, option recommandée en premier.

Sources relues : Rules Reference 1.8 (`assets/docs/mc01_rules_reference_v18.pdf`) p.8-10 (Attack, Attacks Against
Allies), p.31 (Overkill), p.33 (Player Card), p.46-47 (Villain, Villain Defeat) ; livret Galactic Storm 1.2 p.4, p.9,
p.14, p.16 ; relevé Punisher `docs/packs/mcdc-2026-punisher/cartes.md` p180-p197.

---

## Q1. Un allié attaqué directement par un ennemi : les capacités « quand X vous attaque » partent-elles ?

Le **Rules Reference 1.8 p.10** (« Attacks Against Allies ») dit OUI : « Abilities that resolve while/when/after the
attacking enemy "attacks you" resolve against the attacked player. » Le **livret Galactic Storm p.4** dit NON :
« Abilities that trigger when the attacking enemy "attacks you" do **not** trigger. » Les deux textes portent le
même titre et se contredisent sur ce seul point.

Exemple en jeu : Rhino attaque directement Spider-Woman ; Spider-Man a une carte « après que le méchant vous
attaque, piochez 1 carte ».

1. **(Recommandé) Règle du livret Galactic Storm dans les scénarios Galactic Storm, Rules Reference partout
   ailleurs (Punisher compris).** Le livret de campagne est la règle spéciale de sa boîte ; il prime chez lui. En
   jeu : dans Galactic Storm, la carte de Spider-Man ne pioche pas ; dans Punisher et les scénarios officiels, elle
   pioche. Réglage : `AttackCharacter(..., ally_attack_is_against_player=False)` dans les cartes Galactic Storm.
2. **Rules Reference partout.** Le texte officiel le plus récent l'emporte. En jeu : la carte pioche aussi dans
   Galactic Storm (écart avec le livret de la campagne).
3. **Livret Galactic Storm partout.** En jeu : la carte ne pioche plus nulle part sur une attaque d'allié, y compris
   dans les scénarios officiels (écart avec le Rules Reference).
4. Autre (préciser).

État du moteur : défaut = option 2 sur toutes les cartes tant que la question n'est pas tranchée (le réglage existe).

## Q2. Kree Sentry attaque un sbire : les joueurs peuvent-ils défendre ?

Le **livret Galactic Storm p.9** (« Attacks Against Minions ») dit dans la même section : « This attack is always
considered to be **undefended**. » puis « Players **may defend** these attacks as normal by declaring a hero or an
ally as the defender. »

Exemple en jeu : Kree Sentry (ATQ 3) attaque un sbire Imperial Guard à 2 PV ; Binary, prête, pourrait s'interposer.

1. **(Recommandé) Les joueurs PEUVENT défendre ; « undefended » décrit le cas où personne ne défend (le sbire ne
   défend jamais).** C'est la seule lecture qui garde les deux phrases vraies. En jeu : la question « défendre ? »
   est posée ; si Binary défend, elle devient la cible et le sbire est épargné. Réglage :
   `AttackCharacter(..., players_may_defend=True)` sur les cartes de Kree Sentry.
2. **Personne ne peut défendre.** La première phrase l'emporte, la seconde est une reprise fautive de la p.4. En
   jeu : pas de question, le sbire encaisse toujours.
3. Autre (préciser).

État du moteur : défaut = option 2 (aucune défense) tant qu'une carte ne passe pas `players_may_defend=True`
(Punisher p180 « Players may defend any attack, even ones targeting enemies » le passera, lui, sans ambiguïté).

## Q3. Scénario 3 du Punisher : une carte JOUEUR qui parle « du méchant » vise-t-elle le Punisher ?

La carte p180 (*Justice or Punishment?* face B) dit : « Punisher is the active villain. **Encounter cards** referring
to or affecting "the villain" refer only to Punisher. » Elle ne dit rien des cartes joueur. Le méchant CIBLÉ est de
toute façon insensible aux cartes joueur (p183).

Exemple en jeu : un événement « retirez de la menace égale au CTR... du méchant » ou « infligez 3 dégâts au méchant ».

1. **(Recommandé) Le Punisher aussi.** Le CIBLÉ ne peut pas être affecté par les cartes joueur : le proposer ne
   servirait qu'à faire tomber la carte à vide. En jeu : aucune question, la carte vise le Punisher. Réglage :
   `Villains.Rule(the_villain="Active", player_cards="TheVillain")`.
2. **Le joueur choisit entre les deux méchants** (comme Galactic Storm p.16). En jeu : une question à chaque carte
   joueur qui dit « le méchant » ; le CIBLÉ n'est pas proposé tant que le Punisher est en jeu (le moteur l'écarte
   déjà), donc en pratique la même chose que l'option 1 avec une étape de plus quand le Punisher a quitté le jeu.
3. Autre (préciser).

## Q4. Earth Under Siege : quand un méchant est vaincu, que devient « le méchant » des cartes déjà en jeu ?

Livret p.16 : « If a villain is defeated, remove that villain from the game. Unlike other scenarios, all tokens,
status cards, and attachments on the just-defeated villain are discarded instead of carrying over to the next
villain. » Le moteur fait cela (`Villains.Remove`), et « le méchant » des cartes rencontre devient le nouveau
méchant le plus à gauche. Reste le cas d'un effet **en cours** qui avait déjà désigné le méchant retiré (une
attaque de joueur en deux temps, un « jusqu'à la fin de la phase »).

1. **(Recommandé) L'effet en cours s'arrête pour ce méchant (il a quitté le jeu), sans se reporter sur le
   suivant.** Règle générale « un effet sur une carte qui quitte le jeu cesse » (RR 1.8, In Play and Out of Play).
   En jeu : un « +2 ATQ au méchant jusqu'à la fin de la phase » disparaît avec lui.
2. **L'effet passe au nouveau « méchant ».** En jeu : le bonus ou le malus suit la place, comme si c'était le même
   personnage (ce que le livret refuse pour les jetons et états).
3. Autre (préciser).

---

## Second temps, noté (pas une question)

- **Méchant HIDDEN, la moitié « attaque »** (Galactic Storm p.14) : « the villain cannot attack players while it
  has the HIDDEN trait. Instead, whenever a player would be attacked by the villain, that player is dealt a facedown
  encounter card. » Puis la face DISCOVERED (retournement, attachements et états gardés, stade suivant du même côté).
  La brique livrée ne couvre que l'immunité ; cette mécanique se fera avec le scénario Hala Ultimatum (lot GS-6).
- **Trait `HIDDEN` et trait `TARGETED`** : absents de l'énum `TRAITS` (`src/game/card/face/card_face.py`) ; à
  ajouter avec les données des cartes (`HasTrait('HIDDEN')` est l'appel à passer à
  `CannotBeAffectedByPlayerCards(while_fn=...)`).
- **Défense d'une attaque visant un ennemi en multijoueur** : la capacité de défense de base est offerte aux
  personnages de TOUS les joueurs quand `players_may_defend=True` ; l'ordre dans lequel les joueurs sont consultés
  n'est vérifié qu'à un joueur (cas `[briques][attaque] players_may_defend`). À voir en partie réelle à deux.
- **`PlayerChooses` pose sa question au moment où le moteur lit « le méchant »** : comme le choix de Bebop et
  Rocksteady (`tk006a`, même montage), la question peut tomber pendant une vérification de jouabilité si une carte
  joueur lit `Worlds.FindVillain` dans une **condition**. Aucune carte connue ne le fait ; à surveiller en autoplay
  quand Earth Under Siege sera porté.

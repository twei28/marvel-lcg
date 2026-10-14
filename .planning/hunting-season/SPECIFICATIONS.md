# Spécifications d'intégration

## Inventaire et identifiants

| Ensemble | Nombre physique | IDs |
| --- | ---: | --- |
| Vermin | 29 | hs001 à hs029 |
| Scorpion | 24 | hs030 à hs053 |
| The Lizard | 26 | hs054 à hs079 |
| Vulture | 24 | hs080 à hs103 |
| Kraven The Hunter | 21 | hs104 à hs124 |
| Trap | 16 | hs125 à hs140 |
| Feral Instincts | 5 | hs141 à hs145 |
| Lizard Thralls | 5 | hs146 à hs150 |
| Red Vulture | 6 | hs151 à hs156 |
| Savage Six | 7 | hs157 à hs163 |
| The Lodge | 36 | hs164 à hs199 |
| Récompenses | 4 | hs200 à hs203 |
| Sbires de campagne | 2 | hs204 à hs205 |
| Expert Campaign Set | 16 | hs206 à hs221 |
| Hunter Mode | 5 | hs222 à hs226 |

Les IDs des complots ont a et b. Les vilains hs054, hs055 et hs056 ont aussi
a (Curtis Connors) et b (The Lizard). Une paire recto/verso représente une
seule carte physique. Les illustrations alternatives de Kraven ne sont pas
comptées comme des exemplaires supplémentaires. Les marqueurs Aerial /
Grounded ne sont pas des cartes de statut et ne font pas partie des 226.

Les copies identiques sont actuellement développées en objets complets.
reference/full_link_equivalences.json donne les équivalences si le dépôt
préfère le format réduit {card_id, full_link}. Conserver les numéros physiques.

## Scénarios

Les configurations fournies mettent le cœur de chaque scénario dans encounters,
et ses modules dans modular_sets. Ne pas ajouter un deuxième set du même cœur.
Le standard utilise les stades I et II ; l'expert utilise II et III.
Le mode expert de scénario est indépendant du mode campagne expert.

| Scénario | Module recommandé | Complots physiques |
| --- | --- | --- |
| hs_vermin | hs_feral_instincts | hs004, hs005 |
| hs_scorpion | hs_feral_instincts | hs033, hs034 |
| hs_the_lizard | hs_lizard_thralls | hs057, hs058, hs059 |
| hs_vulture | hs_red_vulture | hs083 |
| hs_kraven_the_hunter | hs_savage_six | hs107, hs108 |

Vermin : déplacer Even More Rats depuis les cartes du scénario et mettre une
copie de Regular Rats en jeu engagée avec chaque joueur. Les menaces sur les
RAT ne sont pas des menaces de complot et ne peuvent pas être contrées. Le
seuil du complot additionne ces menaces avec celles du complot actif. La santé
X des rats suit le nombre de RAT engagés avec leur joueur, au maximum 3.
Le calcul doit être dynamique, y compris après entrée/sortie d'autres rats.

Scorpion : Jameson entre sous contrôle du premier joueur, Scorpion's Tail
entre attachée à Scorpion. Les cartes restent uniques ; chercher/déplacer les
copies présentes au lieu d'en générer de nouvelles. La queue est un Attachment
selon son bandeau, malgré le mot upgrade dans le texte de mise en place. Son
damage routing est facultatif. À 10 fois le nombre de joueurs de dégâts, mettre
la queue de côté puis infliger 8 fois le nombre de joueurs à Scorpion. Les
TAIL attachments déplacent 5 dégâts depuis la queue avant de s'y attacher.
Tail Armor reçoit les dégâts à la place de la queue et part à 8 ou plus.
Jameson fait perdre à 3 + nombre de joueurs de blessures. Le deuxième complot
remplace sa complétion par une blessure, retire ses menaces ET ses attachments
et upgrades, sans faire perdre immédiatement par le seuil du complot.

Lizard : le vilain commence sur Curtis Connors. Les attachments, statuts,
boosts, dégâts et autres éléments suivent les changements de face. Le stade
suivant entre sur la même face que le stade vaincu, comme Risky Business.
Curtis Connors ne peut pas prendre de dégâts. Reptilian Rage porte au maximum
3 shame counters. Lizard gagne +1 ATK par compteur et overkill si au moins un
est présent. Le stade III ne retire aucun compteur après une attaque.
Le complot 2B a menace initiale ET escalade X, égale au nombre de cartes
REPTILE en jeu, dont Lizard. Au complot 3B, Lizard ne peut pas être retourné
et aucune menace ne peut être retirée. Les REPTILE attachments doivent rester
liés au vilain lors du changement de face. Leur dépôt au fond de la défausse
est important ; ce n'est pas une défausse ordinaire.

Vulture : tant qu'il est AERIAL, pour l'attaquer, l'attaquant ou l'attaque doit
être AERIAL, ou l'attaque doit avoir ranged. Appliquer aussi la règle aux
attaques d'événement et d'allié ; ne pas limiter aux attaques de base du héros.
S.H.I.E.L.D. Wingsuits donne AERIAL au héros et à tous ses alliés jusqu'à la fin
du round contre une ressource. Certains retraits d'AERIAL durent jusqu'à la
fin du tour ACTIF ; d'autres jusqu'à la fin du round. Les marqueurs facultatifs
ne peuvent ni déclencher ni être ciblés par des effets de cartes de statut.

## Kraven et le paquet Trap

Créer les 16 exemplaires hs125 à hs140 dans un paquet séparé avec défausse
séparée. Ils ne sont pas des cartes Rencontre pour les effets qui se réfèrent
aux cartes Rencontre. Ils ne donnent pas de boost et ne peuvent pas être
mélangés au paquet Rencontre. Les types Minion/Attachment/Treachery décrivent
leurs effets, pas leur appartenance au paquet Rencontre.

Distribuer les pièges face cachée. Les révéler seulement quand une instruction
l'exige ; la capacité de Kraven révèle tous les pièges distribués au joueur
concerné, pas seulement celui qui vient d'être distribué. Le sbire Last Son
of Kraven distribue un piège mais n'ordonne pas de le révéler.

Quand le paquet est vide, remélanger sa propre défausse sans accélération ni
pénalité Rencontre. En Hunter, Master Trapper distribue une carte Rencontre
au premier joueur quand la défausse Trap est remélangée. Si paquet et défausse
sont vides parce que tous les pièges sont en jeu ou distribués, ne rien donner.

Suivre le propriétaire et la défausse d'origine même pour les pièges mis en jeu.
Les attaques supplémentaires de Lion/Cheetah concernent le joueur engagé quand
un personnage qu'il contrôle attaque Kraven. Les limites de Kraven sont par
round ET par joueur (une aux stades I/II, deux au III). Les limites imprimées
sur le complot 2B sont également par joueur.

Chameleon : l'ennemi dont la défaite est remplacée récupère l'instance de dégâts
qui allait le vaincre, selon la FAQ du livret. Il ne récupère pas tous ses PV.
Capture Net : le coût de l'Interrupt remplace l'attaque par la défausse du filet.
Quicksand : annuler les effets de l'événement joué, le défausser puis défausser
Quicksand. Préserver les fenêtres de déclenchement et les coûts déjà payés.

## Campagne commune

Identités fixes pendant toute la campagne. Aspects et composition du deck
peuvent changer entre scénarios. Les cartes imposées de campagne restent dans
le deck et ne comptent pas dans le minimum/maximum du deck. Ceci concerne les
achats, récompenses et cartes experts ajoutées, dans tous les modes concernés.

Choisir le Master Hunter au départ. Si les joueurs ne s'accordent pas, prendre
celui qui a rencontré le plus récemment un animal sauvage non apprivoisé.
Ne pas inventer un joueur par défaut. Il décide les égalités des récompenses.

Le Lodge possède 35 copies initialement disponibles : hs164 à hs199 sauf hs168
(Gibbon). Stock commun à tous les joueurs, coût en XP par exemplaire, achats
facultatifs entre les scénarios. Une carte vendue ne reste pas achetable.
Gibbon n'est ajouté au stock qu'après victoire au scénario 4. Une copie
supplémentaire ne doit pas être générée pour chaque joueur.

Aux mises en place 2 à 5, chaque joueur peut payer 2 XP pour une carte de main
initiale supplémentaire, seulement à la mise en place. Le livret propose ce
paiement une fois ; aucune répétition arbitraire ni bonus de taille de main
permanent. Conserver un marqueur transactionnel pour ne pas le rejouer à la
reprise d'une partie ou au rechargement de l'interface.

## Gains d'expérience

Les valeurs ci-dessous s'ajoutent au solde existant. Les bonus Hunter sont
réservés aux victoires. Les critères individuels se lisent séparément pour
chaque joueur, pas pour l'ensemble du groupe.

| Scénario | Victoire | Défaite | Bonus |
| --- | ---: | ---: | --- |
| Vermin | 3 | 2 | +1 par joueur sans RAT engagé ; en victoire seulement, +1 à chacun si complot stade 1 ; +1 Hunter en victoire |
| Scorpion | 3 | 2 | +1 à chacun si queue mise de côté ; en victoire seulement, +1 si Jameson a au plus 1 blessure ; +1 Hunter en victoire |
| Lizard | 3 | 2 | +1 à chacun si complot stade 1 ou 2 ; +1 si attachments REPTILE sur Lizard strictement moins nombreux que les joueurs ; +1 Hunter en victoire |
| Vulture | 3 | 2 | +1 par joueur à au moins la moitié de ses PV maximum ; +1 à chacun si menace strictement inférieure à 7 fois les joueurs ; +1 Hunter en victoire |
| Kraven | 0 | 0 | Résultat final de campagne, aucun gain XP prescrit |

Au scénario 1 gagné, les joueurs choisissent le propriétaire de l'allié Vermin,
le Master Hunter tranche si besoin. Aux victoires 2 à 4, prendre le joueur
possédant le moins d'alliés PREDATOR, le Master Hunter tranche les égalités.
Compter les alliés possédés dans le deck de campagne, pas seulement en jeu.

Après défaite aux scénarios 2 ou 3, chaque joueur retire définitivement UNE
copie de carte spécifique à son héros, à son choix. Le choix n'est pas limité
aux cartes hs et nécessite la liste réelle de son héros. Garder ID et nombre
de copies, sans retirer toutes les copies du même titre. Au scénario 3 perdu,
noter aussi Lizard escaped ; au 1 perdu, Vermin escaped.

En préparation de Kraven : ajouter hs204 si Vermin escaped et hs205 si Lizard
escaped. Retirer hs160 si Scorpion joined you et hs158 si Vulture joined you.
Ne jamais retirer les alliés récompenses hs201/hs203 à la place des sbires.

## Campagne experte et Hunter

Restaurer les PV notés après la partie précédente. À l'enregistrement, plafonner
aux PV DE BASE de l'identité, sans intégrer un bonus maximum d'une amélioration.
Un joueur éliminé a 0 PV enregistrés ; il peut revenir en ajoutant sa pénalité
expert pour revenir à pleine santé. Les instructions de défaite 1 à 4 demandent
aussi l'enregistrement ; ne pas l'oublier avec un hook victoire uniquement.

Ordre aux mises en place 2 à 5 : offre carte initiale pour XP, reprise des PV,
soins optionnels 1 XP pour 1 dégât, puis possibilité d'ajouter une carte aléatoire
de son propre set expert pour revenir aux PV complets. La carte doit provenir
des exemplaires encore disponibles de son set numéroté. Pas de tirage dans
les sets d'autres joueurs, pas de duplication d'un exemplaire déjà imposé.

| Joueur numéroté | Son of Kraven | Captured! | Hunted! | Poisoned! |
| --- | --- | --- | --- | --- |
| 1 | hs206 | hs207 | hs208 | hs209 |
| 2 | hs210 | hs211 | hs212 | hs213 |
| 3 | hs214 | hs215 | hs216 | hs217 |
| 4 | hs218 | hs219 | hs220 | hs221 |

Ces quatre cartes ont un dos joueur mais demeurent des cartes Rencontre.
Quand elles sont PIOCHÉES depuis un deck joueur, les mettre immédiatement en
jeu dans sa zone sans piocher une carte de remplacement. Seul ce joueur peut
utiliser les capacités pour s'en débarrasser. Vérifier les règles existantes
pour un sbire ou une traîtrise pioché de cette façon, hors phase Rencontre.
Ne pas utiliser le helper générique d'obligation sans vérifier les quatre types.

Hunter implique campagne experte. Il reste indépendant du choix des stades
expert de chaque scénario. Mettre en jeu hs222, hs223, hs224, hs225 ou hs226
selon le scénario, seulement en Hunter. Aucun Setup natif n'est ajouté à ces
cartes ; l'adaptateur de campagne les place conditionnellement.

## Transcription et données

Toutes les valeurs desc sont des chaînes. Les ressources utilisent R physique,
B mental, Y énergie, G libre. Les cartes du Lodge ont RES=G. Gibbon du Lodge
a ATK=1, HP=3, contrairement au Gibbon sbire de Vulture qui a ATK=2, HP=4.
Les dégâts consécutifs d'un allié sont des étoiles dans ATK/THW ; Vermin allié
a deux dégâts consécutifs d'attaque. Une étoile imprimée de capacité/statistique
sur un ennemi n'est pas le multiplicateur par joueur. Les valeurs dynamiques
restent à raccorder : voir POINTS_OUVERTS.md.

Le livret fourni prime sur les résumés MC4DB pour les règles détaillées.
Les clefs MC4DB Scorpion joined / Vulture joined diffèrent des libellés avec
you du livret. Fournir une correspondance explicite si le carnet importe
MC4DB ; ne pas créer deux historiques indépendants ni écraser une campagne.

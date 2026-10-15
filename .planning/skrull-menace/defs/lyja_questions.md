# Lyja : questions de regles ouvertes (a poser a l'utilisateur)

Format : card_id, la phrase, les lectures possibles, la lecture RETENUE (implementee), le scan.
Dossier des scans : `~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav/Hero Packs/Lyja (Skrull Menace Expansion Content)/`.
Decisions DEJA prises par l'utilisateur (non reposees) : etoile rouge = ★ de boost ; « TREACHERY card » = type
Treachery OU trait TREACHERY ; « The Lyja player » = le proprietaire ; Hit the Weak Spot = icones IMPRIMEES du
champ de boost ; cartes joueur defaussees depuis le deck rencontre = defausse du proprietaire.

## sk039 Faking Death et sk040 Feign Loyalty : QUI CHOISIT a la revelation
- Phrase : « When Revealed: Choose to either stun or confuse an enemy » (sk039) ; « Discard an attachment with... » (sk040).
  Les trois autres evenements disent « The Lyja player ».
- Lectures : (a) le joueur a qui la carte est revelee (regle generale d'une carte rencontre) ; (b) le joueur Lyja (proprietaire).
- Retenue : (a). Solo : identique. A plusieurs, un autre joueur qui revele une Faking Death de Lyja choisit lui-meme.
- Scans : `Hero Cards/02 faking death.png`, `04 feign loyalty.png`.

## sk040 Feign Loyalty : que veut dire « attachment »
- Phrase : « Discard an attachment with the uses keyword or the text "Hero Action" or "Hero Response" from play. »
- Lectures : (a) carte de TYPE Attachment (attachement de rencontre : Enhanced Ivory Horn, Power Skrull...) ; (b) toute carte
  attachee, ameliorations joueur comprises (Lazerfist, Mole... portent des Hero Resource/Interrupt).
- Retenue : (a) (les ameliorations du joueur s'appellent « upgrades » ; la carte sert surtout contre les attachements a
  Hero Action des vilains).
- Qui choisit parmi plusieurs : meme question que ci-dessus (joueur a qui la carte est revelee).

## sk040 Feign Loyalty (Boost) : qui pioche
- Phrase : « ★ Boost: Draw 2 cards. » (pas de « The Lyja player »).
- Lectures : (a) le joueur qui subit l'activation (« you » d'un boost = le defenseur, regle du livret) ; (b) le joueur Lyja.
- Retenue : (a).

## sk041 / sk042 : « 4 damage among enemies » et « 3 threat from among schemes »
- Lecture retenue : repartition libre (un meme ennemi / une meme manigance peut etre choisi plusieurs fois, 1 point a la fois),
  PAS tout sur une seule cible comme le fait la carte officielle 32187 (« from among schemes »).
- sk042 : s'il y a moins de 3 menaces en jeu, on retire tout ce qu'il y a.
- Les degats / retraits sont faits par l'IDENTITE du joueur Lyja (pas celle du joueur qui revele).

## sk066 Paibok : PORTEE de « When a TREACHERY card would be discarded »
- Phrase : « Forced Interrupt: When a TREACHERY card would be discarded, attach it facedown to Paibok instead. »
- Lectures : (a) LITTERALE : toute traitrise defaussee, d'ou qu'elle vienne (apres revelation, defaussee du deck par une
  recherche, boost defausse, ET evenement TREACHERY de Lyja defausse de la MAIN pour payer une ressource ou par
  Going Ballistic) ; (b) seulement les traitrises de rencontre qui se resolvent et les cartes defaussees depuis le deck rencontre.
- Retenue : (a), faute de restriction imprimee. Consequence : tant que Paibok est en jeu, defausser un evenement TREACHERY de sa
  main pour payer une ressource l'attache a Paibok ; Going Ballistic defausse donc moins de cartes. A confirmer.
- Scan : `Encounter Cards/42 paibok nemesis.png`.

## sk068 « It's a Stinkin' Skrull! » : surge quand Paibok intercepte
- Phrase : « If no TREACHERY card was discarded this way, this card gains surge. »
- Si Paibok est en jeu, la traitrise trouvee est attachee a Paibok au lieu d'etre defaussee : « discarded this way » est faux.
- Retenue : la carte gagne Surge (lecture litterale ; le critere est ce que `Faces.DiscardAll` a reellement defausse).

## sk056 Invisible Woman : ordre des compteurs
- Phrase : « takes +1 consequential damage for each revelation counter on the target of her basic power » et « Forced
  Response: After ... place 1 revelation counter on the target ».
- Lecture retenue : le consecutif compte les compteurs DEJA presents AVANT ce pouvoir ; le nouveau compteur est pose apres.
  Une cible vierge ne fait rien subir a Sue ; la 2e attaque sur la meme cible lui fait subir 1.
- Les compteurs vont aussi sur une manigance (contre) ; le contre pose un compteur sur CHAQUE manigance contree.

## sk046 Mole : « discarded from the top of the encounter deck » + resolution
- Retenue : une traitrise defaussee alors qu'elle est la carte du DESSUS du deck rencontre (defausse de sommet : « discard
  the top card », Wrath of the Empire...). Une carte trouvee par recherche puis defaussee n'est PAS « du dessus ».
- « Resolve that card's When Revealed » : on resout SEULEMENT l'effet When Revealed (`Faces.ResolveAbility`), la carte est
  ensuite defaussee normalement (ni surge, ni Incitation).
- Limite connue : Mole ne declenche pas sk065 Untrustworthiness (la resolution ne passe pas par une revelation).

## sk065 Untrustworthiness : boucle possible
- « Then, deal yourself 1 facedown encounter card » : la carte distribuee, si c'est une traitrise, sera annulee a son tour
  a sa revelation et en distribuera une autre (jusqu'a une carte non TREACHERY). Retenue telle quelle (c'est le texte).
- Les evenements de Lyja revelees (type Event, trait TREACHERY) sont annulables comme les traitrises.

## sk037a Skrull Spy : « up to 1[per_hero] resources »
- Retenue : jusqu'a N ressources au TOTAL, N = nombre de heros (1 solo, 2 a deux...) ; rien depense = la recherche ne ramene
  aucune carte mais le deck rencontre est quand meme melange.

## sk064 Fantastic Four Member : « Play only if your identity has the FANTASTIC FOUR trait »
- Lyja (forme heros) a le trait FANTASTIC FOUR ; Laura Green (alter ego : SKRULL. SPY.) NON : la carte n'est donc pas jouable
  en forme alter ego (« your identity » = la face en jeu). Lecture retenue ; a confirmer si l'auteur voulait « votre heros ».

## sk045 Ministerial Tiara : ce qui compte pour « a star icon in the boost area »
- Retenue : toute carte de boost qui a un « ★ Boost: » (les evenements de Lyja, les traitrises et sbires officiels a boost
  etoile). Une icone Y ordinaire ne compte pas. Interruption proposee a la retournee, avant la resolution du ★ Boost.

## sk069 Truth Revealed : « identity-specific cards »
- Retenue : les cartes dont la classe est « Hero » (cartes signature de l'identite) du deck du joueur qui revele. Le deck
  de depart de Lyja en contient 15 (sk038-sk047). Hors deck : l'obligation et le set nemesis ne sont pas concernes.

## sk043 New York Bookstore, sk044 Lazerfist, sk047 Shapeshifter : bonus nommes
- « Laura Green gets +2 REC » (alter ego seulement), « Lyja gets +1 ATK/THW » (forme heros seulement). Aucun contre-cas dans
  l'autre forme n'est mesurable : l'alter ego n'a pas d'ATK/THW et le heros pas de REC.

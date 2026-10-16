# Bebop & Rocksteady (`tk`) : questions en attente

Aucune réponse de l'utilisateur n'a été possible pendant le portage. Pour chaque
lecture RÉELLEMENT ambiguë, le script porte la lecture la plus fidèle, marquée
`TODO-QUESTION Qn`. Format : card_id, scan, texte anglais exact, lectures
(recommandée en premier), ce que ça change en jeu. Scans : `.planning/tmnt/pics-bebop/<card_id>.jpg`.

## Q1 : `tk007b` Headfirst : « your identity »
- Scan : `.planning/tmnt/pics-bebop/tk007b.jpg`
- Texte : « **Special**: Deal 1 damage to your identity. » (résolu par la Réponse forcée du vilain : « After Bebop takes damage, resolve the "Special" ability on the HOG attachment. »)
- Lectures : (A, retenue) l'identité du joueur qui a infligé les dégâts à Bebop ; à défaut (dégâts d'une carte de rencontre, d'un effet sans joueur), le premier joueur. (B) toujours l'identité du premier joueur. (C) l'identité de chaque joueur.
- En jeu : à plusieurs joueurs, A fait payer celui qui frappe Bebop ; B fait payer toujours le même ; C multiplie les dégâts par joueur.
- Code : `JoueurResponsable` / `tk007b.py`.

## Q2 : `tk007b` Headfirst et `tk008b` Headstrong : l'activation qui déclenche le retournement
- Scans : `tk007b.jpg`, `tk008b.jpg`
- Texte : « **Forced Interrupt**: When Bebop would activate, if Headstrong is in play, flip Bebop and Rocksteady to their K.O. sides and flip both TEMPER attachments to their ROWDY sides. »
- Lectures : (A, retenue) l'activation en cours devient une activation de vilain K.O. : elle est remplacée par le retrait de 1 jeton knucklehead (2 en expert) du Temper redevenu ROWDY (et réveil s'il n'en reste plus). (B) l'activation est annulée sans retirer de jeton. (C) l'activation se déroule normalement avec les valeurs K.O. (0 ATQ / 0 SCH).
- En jeu : A coûte 1 jeton à Bebop dès ce tour-là ; B laisse 3 jetons ; C déclenche quand même les cartes de boost.
- Code : `TempersEnrages` / `ActivationKO` (`__init__.py`).

## Q3 : `tk022` Lay the Beatdown : « Deal 2 indirect damage to your hero »
- Scan : `tk022.jpg`
- Lectures : (A, retenue) 2 dégâts indirects au HÉROS seulement (propriété `is_indirect_damage`, pas de répartition). (B) dégâts indirects au sens habituel : répartis entre le héros et ses alliés au choix du joueur.
- En jeu : B permet de protéger le héros en sacrifiant un allié.
- Code : `tk022.py`.

## Q4 : `tk102` Road to Ruin : « Stun your hero » en forme d'alter ego
- Scan : `tk102.jpg`
- Texte : « **When Revealed**: Choose: • Discard a friendly LOCATION. • Stun your hero. »
- Lectures : (A, retenue) l'option « Stun your hero » n'existe qu'en forme de héros (les autres cartes du set distinguent « your identity » et « your hero »). (B) elle vise l'identité quelle que soit la forme.
- En jeu : en alter ego sans LOCATION, A ne fait RIEN, B étourdit l'alter ego.
- Code : `tk102.py` (`condition=joueur.IsHero()`).

## Q5 : `tk201` Hittin' the Town : « the villain deck »
- Scan : `tk201.jpg`
- Texte : « **When Revealed**: Discard cards from the top of the villain deck until an attachment or side scheme is discarded and reveal it. »
- Lectures : (A, retenue) « villain deck » = le DECK RENCONTRE (le scénario n'a pas de deck de vilain à défausser ; Anchovy dit « encounter deck »). (B) littéral : le deck de stades du vilain (vide ici : la carte ne ferait rien).
- Code : `tk201.py` (bornée : ne boucle pas si deck et défausse n'ont aucune cible).

## Q6 : `tk109` Power Play : la Réponse se redéclenche-t-elle sur son propre retrait ?
- Scan : `tk109.jpg`
- Texte : « **Hero Response**: After you remove threat from this scheme, discard 1 card from your hand → remove 2 threat from this scheme. »
- Lectures : (A, retenue) le retrait de 2 menaces par la Réponse est lui-même « vous retirez de la menace » : la Réponse peut se rejouer tant qu'on a des cartes à défausser. (B) une seule Réponse par contre.
- En jeu : A permet de vider la manigance en défaussant sa main ; B plafonne à 3 menaces retirées par contre.
- Code : `tk109.py` (`retire_par_vous`).

## Q7 : `tk009` / `tk010` : « When Revealed » quand la carte ne s'attache pas
- Scans : `tk009.jpg`, `tk010.jpg`
- Texte : « Attach to Bebop if he is ALERT. Otherwise, this card gains surge. ... **When Revealed**: Place 1 knucklehead counter on the HOG attachment. »
- Lectures : (A, retenue) le « When Revealed » se résout toujours (le compteur est posé même si la carte n'a pas pu s'attacher, puis Renfort). (B) sans attache, la carte est défaussée avant son « When Revealed » : pas de compteur.
- Code : `Accessoire(...)` (`__init__.py`).

## Q8 : `tk006a` Destructive Dunderheads : ordre des deux activations
- Scan : `tk006a.jpg`
- Texte : « During step two of the villain phase, both villains activate against each player. »
- Hypothèse codée : pour chaque joueur (ordre des joueurs), Bebop puis Rocksteady, puis les sbires engagés. Aucun texte ne fixe l'ordre. Alternative : le premier joueur choisit l'ordre (règle générale RR p.6 pour les activations simultanées).

## Notes de lecture (pas des questions)
- `tk101` Welcome to the Jungle : le scan imprime « take this fight to the them. » (faute de l'auteur). Le texte anglais de `cards.json` la reproduit telle quelle ; le français est corrigé.
- Les icônes (Boost, Étoile, Accélération, Aléa, Crise, Amplification) ont été vérifiées par découpe contre `01111`/`01122` (boost), `01109` (accélération), `01107` (aléa), `01108` (crise), `16054` (amplification) : voir `.planning/tmnt/bebop-phase-a.md`.

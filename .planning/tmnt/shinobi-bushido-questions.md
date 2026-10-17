# TMNT Shinobi Bushido (`sb001`-`sb020`) : questions ouvertes pour l'utilisateur (17/10/2026)

> Réponses rendues le 17/10/2026, voir shinobi-reponses.md (les mentions « NON terminée » / « provisoire » ci-dessous sont historiques : cartes levées).

Scans : `/tmp/claude-29999/-home-oem-Desktop-Marvel-LCG/2ed3e66d-9fcf-45e1-aa7f-2debf9a42af0/scratchpad/zip-shinobi/TMNT Shinobi/Bushido/`.
Une question à la fois, scan à l'appui. Les deux cartes ci-dessous sont codées sur une lecture PROVISOIRE (marquée en tête de leur script) et
restent **NON terminées**.

## Q-B1 : sb006 Mercy : où va « instead », et que veut dire « hit points to 1 » ?
- Scan : `Bushido/B6 Mercy.png`. Texte : « **Hero Interrupt**: When an enemy would be defeated by your hero, discard this card **instead** →
  set that enemy's hit points to 1. Then, draw 3 cards. » (amélioration OATH, coût 1, Max 1 par joueur).
- Le « instead » est placé après « discard this card » et avant la flèche : il devrait qualifier le remplacement de la DÉFAITE de l'ennemi.
- Options : (a) **le coût est « défausser cette carte », la défaite de l'ennemi n'a pas lieu à la place, ses points de vie RESTANTS passent à 1,
  puis on pioche 3** (recommandée, codée) ; (b) idem mais « hit points » = points de vie MAXIMUM ramenés à 1 (l'ennemi garde ses dégâts : il survit
  seulement s'il en a moins) ; (c) la défausse de Mercy est elle-même ce qui remplace la défaite et les PV passent à 1 sans coût ; (d) autre.
- Effet en jeu : (a) un coup fatal laisse l'ennemi à 1 PV et rapporte 3 cartes ; (b) rendrait la carte presque inutile sur un gros ennemi.
- Provisoire : (a). Cas : `[sb] sb006` (4 cas verts).

## Q-B2 : sb013 Santōryū Ōgi : où s'attache-t-elle, et que devient-elle si la recherche ne ramène rien ?
- Scan : `Bushido/B13 Santoryu Ogi.png`. Texte : « Max 1 per deck. **Attached upgrade** loses the restricted keyword. **Response**: After this
  card enters play, search your deck and discard pile for a WEAPON upgrade. (Shuffle.) Put that upgrade into play (paying its resource cost)
  **with this card attached**. » (amélioration SKILL, coût 0, ressource wild). Aucun « Attach to » imprimé.
- Options : (a) **jouée comme toute amélioration sans « Attach to » (sur votre identité) ; la Réponse met l'arme en jeu en payant son coût, puis
  Ōgi se DÉTACHE de l'identité et s'attache à cette arme, qui perd Restricted ; sans arme trouvée ou payable, Ōgi reste sur l'identité**
  (recommandée, codée) ; (b) Ōgi doit s'attacher d'emblée à une arme déjà en jeu (« Attach to a WEAPON upgrade you control », texte absent) et la
  Réponse en va chercher une seconde ; (c) Ōgi reste sur l'identité et « attached upgrade » désigne autre chose (précisez) ; (d) autre.
- Effet en jeu : (a) la carte sert d'accélérateur d'arme ; (b) elle devient une amélioration d'arme classique.
- ⚠ Écart moteur même en (a) : la limite « 2 cartes Restricted » est contrôlée par le moteur à l'ENTRÉE EN JEU de l'arme, avant qu'Ōgi s'y attache :
  avec déjà deux armes Restricted en jeu, l'arme ramenée force la défausse d'une autre (cas non prouvé, voir rapport). À trancher avec la lecture.
- Provisoire : (a). Cas : `[sb] sb013` (6 cas verts).

## Notes sans question (relevées, aucune décision en jeu)
- `sb016` Wakizashi : la citation imprime « the traditional **dashido** » (probable coquille de « daishō » ou « dashi » ; texte reproduit tel qu'imprimé,
  sans effet en jeu).
- `sb018` Musha Shugyō : « Characters other than the **owner** of this card cannot remove threat » : lue littéralement comme `40006` Technovirus Purge
  (« other than Cable ») : seule l'IDENTITÉ du propriétaire (et ce qu'elle joue : événements, améliorations) retire de la menace ; ses alliés ne le
  peuvent pas. Si l'auteur voulait inclure les alliés du propriétaire, c'est une ligne à changer (`pas_le_proprietaire`, `sb018.py`).
- `sb007` Integrity : elle répond aussi à sa PROPRE mise en jeu (c'est une amélioration OATH jouée) ; comportement du moteur, prouvé par cas.
- Homonyme : `sb008` Self-Control (amélioration OATH) ≠ `44026` « Self Control » (ressource de Deadpool) : cartes différentes (NOUVELLE).
- Les 20 cartes sont NOUVELLES (aucune officielle identique : seul le nom de sb008 est proche de 44026).
- Icônes de ressource vérifiées par découpe contre `jennika` (même éditeur) : poing = R, éclair = Y, noeuds = B ; l'étoile verte de Ōgi (G) et l'étoile
  noire du texte de Self-Control (wild) comparées à `jennika/tj009`.
- Musha Shugyō : coût 1 (le « 1 » est imprimé tourné de 90° en haut à droite du scan paysage), menace de départ 5 (sans étoile), ressource énergie.
- Uno : ATQ/CTR « 1★ » = 1 icône de dégâts consécutifs (`1*`) + l'étoile de rappel (modèle `ul036`) ; PV 3 (cercle orange), coût 3.

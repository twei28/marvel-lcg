# Verdicts Warriors Three (docs/packs/warriors-three/GABARITS.md, « Questions en attente »)

Sources : RR v1.8 (scratchpad/rr_v18.txt) + NOTICE DE L'AUTEUR trouvée dans le zip
(`The Warriors Three-20261025T195537Z-1-001.zip`, « Rules Insert and Precons/Warriors Three Insert Side A/B.png »,
extraits lisibles : scratchpad/wt_zip/sideA_top.jpg, sideA_bot.jpg, sideB_top.jpg, sideB_bot.jpg).
La notice n'est citée nulle part dans le gabarit : elle tranche Q1-Q5 et Q8.
Scans : Fusion/marvel-lcg-src/assets/pics/<code>.jpg

## Q1 États par héros — B : le code doit changer
Cartes : wt001a/c/d, wt002. Notice face B : « Status cards on your inactive heroes will remain on them, but wont be relevant until they become the active hero » ; « an active hero is only affected by status cards that are on them or The Warriors Three card » ; « status cards and attachments on The Warriors Three card remain on the card when it flips, but they are treated as if they were on your active hero while it is in its upgrade form ». Face A : « Heroes retain any status cards or attachments on them ».
Donc : chaque héros garde ses propres cartes d'état ; celles posées sur la carte The Warriors Three (en alter ego) suivent le héros actif. Le partage sur l'identité (A) est faux.

## Q2 wt011 Mighty Endurance, Volstagg inactif — B (ni A ni B tels qu'écrits) : le code doit changer
Texte : « Otherwise, give Volstagg a tough status card. » Notice : les états sur un héros inactif restent sur lui. Volstagg inactif reçoit donc la carte Résistance, qui ne sert que quand il redevient actif. Ni « effet perdu » (A) ni « sur l'identité » (B). Dépend de Q1.

## Q3 Soutiens des héros — B : le code doit changer
Notice face A : « flip your active hero to their inactive side, and flip another inactive hero to their active side » (une seule carte physique, deux faces) ; « will treat your inactive heroes as supports ». Le soutien du héros actif n'est donc PAS en jeu comme soutien (sa carte est la face héros). Conséquence : Rally!, Fated Clash et tout effet « a support » ne doivent pas le voir.

## Q4 État de la carte-titre — A confirmé
Notice face A : « Heroes … remain ready or exhausted when they flip » ; FAQ : la carte The Warriors Three est une seule carte qui se retourne (alter ego / amélioration). L'état passe d'une face à l'autre.

## Q5 wt006 Hildegarde — A confirmé
Texte : « all WARRIORS THREE get +1 ATK and +1 THW until the end of the phase ». Notice face B : « inactive heroes do not have basic powers to increase, but Hildegarde's ability will give them +1 ATK and +1 THW if they flip to active hero that phase ». = bonus sur le héros actif quel qu'il soit pendant la phase + alliés WARRIORS THREE.

## Q6 wt008 Fimbuldraugr — B (ni A ni B) : le code doit changer
Texte : « while he is your active hero ignore all crisis icons in play ». RR Crisis Icon : « Each crisis icon is equivalent to … "Player cards cannot remove threat from the main scheme." ». Ignorer l'icône = TOUTES les cartes joueur (alliés, autres joueurs compris) peuvent retirer de la menace de la manigance principale tant que Fandral est le héros actif. Le code actuel (`UnitIgnoreKeywordIcons(CardFinder(name="Fandral"…))`, play.py:534-542) ne lève la crise que pour les effets dont la source est Fandral (ses événements / améliorations) : un allié ou un autre joueur reste bloqué. Condition à coder : Fimbuldraugr en jeu ET Fandral héros actif, quelle que soit la source.

## Q7 wt013 Hold the Line — A confirmé
Texte : « When threat would be placed on a scheme, prevent that threat. » « that threat » = toute la menace de cette pose.

## Q8 wt014 Rally! — A confirmé (cohérent avec Q3)
Texte : « Ready all PERSONA supports you control. » Le héros actif n'est pas un soutien (notice : seuls les inactifs sont traités comme des soutiens).

## Q9 wt016 A Questing We Shall Go! — B : le code doit changer (limite moteur, pas un doute)
Texte : « Search the encounter deck for the bottom most minion. Reveal it, then attach this card to it. If you can't, this card gains surge. » Le texte impose l'attachement (RR Attachment ; quand le sbire quitte le jeu, la carte attachée est défaussée ; un effet qui défausse une pièce jointe doit pouvoir l'enlever et retirer le bonus). « bottom most » = le plus proche du dessous : A correct. Sans sbire : surge, correct.

## Q10 wt017 Fenris — A confirmé
Scan : PV imprimés « – » ; « Fenris can not take damage or be defeated ». La valeur interne n'a aucun effet.

## Q11 wt018 Countdown to Ragnarok — A confirmé
Texte : « Permanent. Threat can not be removed from this scheme. Threat can only be placed on this scheme by Fenris. » Menace de départ imprimée 0.

## Q12 wt019 Gleipnir — A confirmé, avec une précision multijoueur
Texte : « Deal yourself a facedown encounter card. Hero Action: Spend 3 resources and discard Gleipnir → discard Fenris. ★ Boost: Reveal this card. » Pas de « Give to » : RR Obligation, « the player places that obligation into their play area ». L'Action qui défausse Gleipnir implique qu'elle reste en jeu. Précision : le Boost la fait révéler par le joueur contre qui l'ennemi s'active (RR Attack : « boost abilities that refer to "you" refer to … »), pas forcément le premier joueur. Identique en solo.

## Q13 wt020 Skadihr — A confirmé
Texte : « put her under your control as a WARRIORS THREE ally. Her THW is equal to her printed SCH and she takes 2 consequential damage when she thwarts or attacks. » ATK non modifiée → 2 imprimé.

## Q14 wt021 Fated Clash — A confirmé
Hildegund and Kin (wt010) porte le trait PERSONA (cards.json) → compte. Fin du texte : « search the encounter deck and discard for Fenris and reveal him » : correct. (Avec Q3 B : le soutien du héros actif n'est pas éligible.)

## Q15 wt022 Revelry in Asgard — « ce tour » : B : le code doit changer (multijoueur seulement) ; Team-Up : A confirmé
Texte : « If a minion was defeated this turn » : turn = le tour du joueur, pas le round. Le registre de round compte aussi les sbires vaincus pendant le tour d'un AUTRE joueur. Identique en solo. Team-Up (Odinson and The Warriors Three) : fiche teamup.md / RR p.43 = personnages nommés en jeu (identité ou allié) : allié Odinson ou identité Thor en alter ego (nom Odinson) ; correct.

## Q16 wt023-wt025 — B : le code doit changer (règle de l'utilisateur du 17/10/2026)
Scans : Genius BB / Energy YY / Strength RR, « Max 1 per deck. », Basic : identiques à 01089 / 01088 / 01090 (cards.json). GUIDE-CREATION-CONTENU.md §12 bis : « si SEULE l'image change par rapport à l'officielle, c'est un art alternatif ». En carte à part, un deck pourrait aussi avoir 2 « Genius » malgré « Max 1 per deck » (limite par titre).

## Q17 Decklists imprimées — pas une question de règle ; A conservé
Réimpressions identiques en jeu (Lay Down the Law, Concussive Blow) : sans effet. Non revérifié contre les images de precon.

## Q18 wt007 — A confirmé
Scan : « Brandrheid Undrsigr ».

## Q19 Icônes de ressource — A confirmé
Planche des coins : scratchpad/icones_wt_co.jpg + scans lus un à un. wt003 Y, wt004 B, wt005 R, wt006 G (étoile verte), wt007 B, wt008 Y, wt009 R, wt010 B, wt011 R, wt012 Y, wt013 R, wt014 Y, wt015 R, wt022 Y, wt023 BB, wt024 YY, wt025 RR : tous conformes à cards.json.

DOUTE RÉEL : aucun.

# Sources des sons

Choisis par l'utilisateur le 07/10/2026 sur la page d'écoute (refonte des sons,
`docs/superpowers/specs/2026-09-15-refonte-des-sons-design.md`). Tous sous
licence **Creative Commons 0** (domaine public), vérifiée sur la page de chaque
son : utilisables sans condition ni crédit. Convertis en WAV mono 44,1 kHz
16 bits, niveau ramené entre −18 et −21 dB RMS (crête −1 dB).

Un même son sert plusieurs noms : le moteur nomme 21 déclencheurs
(`src/game/message/message.py`, `SOUND_NAMES`), le plateau joue `<nom>.wav`.

| Famille | Fichiers | Son d'origine | Auteur | Lien |
|---|---|---|---|---|
| Capacité | `activate` | Magic Strike.wav | Aleks41 | https://freesound.org/people/Aleks41/sounds/406063/ |
| Impact | `damage`, `target`, `directattack` | Blocking Arm With Hand | mmasonghi | https://freesound.org/people/mmasonghi/sounds/321810/ |
| Carte qui bouge | `draw`, `carddrop`, `set`, `equip`, `cardpick`, `shuffle` | Card Sounds.mp3 (coupé à 282 ms) | henrygillard | https://freesound.org/people/henrygillard/sounds/575387/ |
| Retournement | `flip`, `reveal` | card.mp3 | Johnny2810 | https://freesound.org/people/Johnny2810/sounds/559531/ |
| Jeton | `token`, `addcounter`, `removecounter`, `gainlp` | Coin Pickup SFX [2] | SoundDesignForYou | https://freesound.org/people/SoundDesignForYou/sounds/646672/ |
| Gong | `phase`, `nextturn` | dingDing | Glitched7777 | https://freesound.org/people/Glitched7777/sounds/723291/ |
| Survol (plateau) | `survol` | Modern UI Hover (coupé à 80 ms) | yuugfr1a | https://freesound.org/people/yuugfr1a/sounds/770203/ |
| Carte qui vole (plateau) | `vol` | Metallic Whoosh.wav | MissCellany | https://freesound.org/people/MissCellany/sounds/240640/ |

**Survol d'un héros** (écran de préparation, `SON_SURVOL_HEROS` dans
`public/js/prepare/sons.js`) : `heros-wolverine.mp3` (Wolverine d'origine),
fourni par l'utilisateur le 08/10/2026, extrait de la vidéo « Solo Echo vs
Bullseye » de la chaîne JCE TV. Pas sous licence libre : à remplacer si le
site devait s'en passer.

**Répliques des héros et des méchants** (`voix-<id>-<n>.mp3`,
08/10/2026, tables `SON_SURVOL_HEROS` et `SON_SURVOL_MECHANTS` de `sons.js`) :
voix du jeu **Marvel Rivals** (NetEase / Marvel), téléchargées depuis le wiki
fandom (`marvelrivals.fandom.com`, pages `<Nom>/Quotes`, section Abilities) :
cri d'ultime « Self » et répliques de capacités, jamais de skin, d'événement
ni de team-up. **Voix non libres**, choix de l'utilisateur. Converties en mp3
mono 96 kbit/s, ramenées à −20 dB RMS (crête ≤ −1 dB). Seulement la même
personne que dans Rivals (pas Miles Morales, X-23, Flash Thompson…). Le
Magnéto méchant reprend les fichiers du héros ; `the_hood_2` ceux de
`the_hood`. Venom méchant (Eddie Brock, vérifié dans `mechants-info.js`) :
3 répliques de capacités de Venom. Kingpin (`kingpin_fne`, `wd_kingpin`) :
3 répliques de boss (pas de capacités dans Rivals). Pas de voix pour Venom
héros (Flash Thompson), Psylocke (Rivals : Sai, pas Betsy), ni Shuri (ses
seuls dialogues durent 4,5 à 8,4 s). 124 fichiers en tout.

**Inchangés** (sons d'origine du client, choix de l'utilisateur « garder
l'actuel ») : `destroyed`, `banished`, `negate` (famille Disparition), et
`musique-plateau.mp3`.

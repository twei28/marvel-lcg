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

**Inchangés** (sons d'origine du client, choix de l'utilisateur « garder
l'actuel ») : `destroyed`, `banished`, `negate` (famille Disparition), et
`musique-plateau.mp3`.

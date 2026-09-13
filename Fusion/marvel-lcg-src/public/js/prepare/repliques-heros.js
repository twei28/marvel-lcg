// repliques-heros.js — la phrase qui claque sur la carte au recrutement.
//
// Plusieurs par héros, tirées au sort sans répéter la dernière (voir
// choisirReplique). Liste établie par l'utilisateur le 11/09/2026, gardée
// telle quelle, casse et ponctuation anglaises comprises : ce sont des
// répliques (comics et films), pas des traductions. Les onomatopées des
// pouvoirs (SNIKT, THWIP, BAMF) restent dans le style « MOT ! ».
//
// Indexé par IDENTIFIANT DE DECK (deck/starter/<id>.json), jamais par nom :
// « Spider-Man » désigne trois decks. Un héros absent d'ici retombe sur
// ONOMATOPEES (app.js), puis sur « BAM ! ». Vérifié par
// outils/verifier-repliques.mjs.
"use strict";

export const REPLIQUES = {
    /* --- officiels --- */
    spider_man: ["Your friendly neighborhood Spider-Man!", "With great power comes great responsibility.", "Come on, Spider-Man.", "I don't feel so good.", "THWIP !"],
    captain_marvel: ["Higher, further, faster!", "I'm Captain Marvel.", "I have nothing to prove to you."],
    she_hulk: ["She-Hulk smash!", "I'm sensational, and you know it.", "I'm a Hulk?!"],
    iron_man: ["I am Iron Man.", "And I am... Iron Man.", "Sometimes you've gotta run before you can walk.", "We have a Hulk."],
    black_panther: ["Wakanda Forever!", "I never freeze.", "The living are not done with you yet.", "In my culture, death is not the end."],
    captain_america: ["Avengers Assemble!", "I can do this all day.", "Before we get started, does anyone want to get out?", "I'm with you till the end of the line.", "Language!"],
    ms_marvel: ["Embiggen!", "Good is not a thing you are. It's a thing you do.", "I'm a superhero."],
    thor: ["For Asgard!", "Ultron. We would have words with thee.", "Bring me Thanos!", "You people are so petty... and tiny.", "I knew it!"],
    black_widow: ["I've got red in my ledger.", "I'm always picking up after you boys.", "Let me put you on hold.", "She's not alone."],
    doctor_strange: ["By the Hoary Hosts of Hoggoth!", "By the Vishanti!", "Dormammu, I've come to bargain.", "We're in the endgame now.", "Try me, Beyoncé."],
    hulk: ["HULK SMASH!", "Hulk is strongest one there is!", "That's my secret, Captain. I'm always angry.", "Puny god."],
    hawkeye: ["Okay... this looks bad.", "The city is flying, we're fighting an army of robots...", "If you step out that door, you are an Avenger.", "Nobody would know."],
    spider_woman: ["Spider-Woman fights back!", "I'm Spider-Woman.", "You picked the wrong spider."],
    ant_man: ["You can call me Ant.", "Does anyone have any orange slices?", "I'm gonna call him Antony.", "Why don't you pick on someone your own size?", "Do you guys just put the word quantum in front of everything?"],
    wasp: ["This is what it's like to fly. To be free.", "G.I.R.L. means Genius In action Research Labs!"],
    quicksilver: ["I'm the fastest man on Earth.", "You didn't see that coming?", "Keep up, old man!", "Too slow.", "Catch me if you can."],
    scarlet_witch: ["While I live and until I die, I am an Avenger!", "You took everything from me.", "You will.", "What mouth?", "Reality is mine to rewrite."],
    groot: ["I am Groot!", "We are Groot.", "I. Am. Groot."],
    rocket_raccoon: ["Blam! I just murdered you!", "Ain't no thing like me, except me.", "I need that guy's prosthetic leg.", "Bunch of jackasses standing in a circle.", "I'm gonna get that arm."],
    star_lord: ["We're the Guardians of the Galaxy.", "Star-Lord, man. Legendary outlaw?", "Dance-off, bro!", "I'm distracting you, you big turd blossom!", "I'm gonna make some weird shit."],
    gamora: ["The deadliest woman in the galaxy.", "I am going to die surrounded by the biggest idiots in the galaxy.", "I have lived most of my life surrounded by my enemies."],
    drax: ["Tell Mephisto Drax sent you.", "Nothing goes over my head.", "I've mastered the ability of standing so incredibly still...", "Why is Gamora?"],
    venom: ["Agent Venom, reporting for duty.", "We are Venom.", "The symbiote and I have this.", "Agent Venom. Locked and loaded."],
    spectrum: ["Let's save America by beating up everything we see.", "If you don't, I will.", "They used to call me Lieutenant Trouble."],
    adam_warlock: ["Adam Warlock, the warrior, returns!", "I am Adam."],
    nebula: ["You should have killed me.", "All I wanted was a sister!", "I wasn't always like this."],
    war_machine: ["Boom! You looking for this?", "Next time, baby.", "This is gonna be a beautiful death."],
    valkyrie: ["You might be wise to surrender.", "This is gonna be such fun!", "I think you can handle things from here.", "Valhalla can wait."],
    vision: ["I am the Vision of the Avengers.", "A thing isn't beautiful because it lasts.", "Maybe I am a monster. I don't think I'd know if I were one.", "Our very strength invites challenge.", "I was born yesterday."],
    ghost_spider: ["This mask is my badge now.", "Let's do this one last time.", "Time to hit the drums.", "THWIP !"],
    spider_man_miles_morales: ["I'm Miles Morales. And I'm Spider-Man.", "Anyone can wear the mask.", "Nah, I'mma do my own thing.", "Hey.", "THWIP !"],
    nova: ["I can. I'm NOVA!", "Nova Force, let's go!", "Helmet on. Game on.", "Human rocket incoming!"],
    ironheart: ["I swear to Thor I liked you more when you were alive.", "Let's go!", "Armor online.", "Built it myself.", "Ironheart is ready."],
    spider_ham: ["Let's rage.", "With great power comes great responsibility.", "That's all, folks... wrong universe.", "Prepare for pork-powered justice!", "THWIP !"],
    sp_dr: ["We're called SP//dr and we protect the city.", "SP//dr online.", "Peni and SP//dr, connected.", "THWIP !"],
    colossus: ["I do not give my word unless I mean to keep it.", "Four or five moments.", "For Mother Russia!"],
    shadowcat: ["Professor Xavier is a jerk!", "I am Kitty Pryde. I am an X-Man.", "Can't hit what you can't touch."],
    cyclops: ["To me, my X-Men!", "We go home. And get ready for next time.", "You're not the only one who can't control your powers."],
    phoenix: ["I am fire and life incarnate!", "Now and forever, I am Phoenix!", "You have no idea what you're dealing with."],
    wolverine: ["I'm the best there is at what I do.", "Bub.", "Go fuck yourself.", "What kind of name is Wolverine?", "SNIKT !"],
    storm: ["By the Goddess!", "Goddess be merciful.", "Do you know what happens to a toad when it's struck by lightning?"],
    gambit: ["Bang, you dead!", "Mon ami.", "The name's Gambit. Remember it."],
    rogue: ["We got us a job t'do!", "You don't know what it's like to be afraid to touch somebody.", "Sugah.", "How about I borrow that power, sugah?"],
    cable: ["Be ready for trouble, 'cause trouble is ready for you!", "There's nothing I can't kill."],
    domino: ["Someone has to blow something up.", "Luck isn't a superpower.", "I'm lucky.", "Odds are in my favor.", "Lucky me."],
    psylocke: ["The focused totality of my telepathic abilities."],
    angel: ["One last time, I need to fly!", "Time to spread my wings.", "Death from above.", "Let's fly."],
    x_23: ["I'm Laura Kinney. I'm Wolverine.", "Don't be what they made you.", "My turn.", "Claws out.", "SNIKT !"],
    deadpool: ["Chimichangas!", "Maximum effort!", "Daddy needs to express some rage.", "I'm touching myself tonight.", "Fourth wall? What fourth wall?"],
    bishop: ["You've taken your best shot! Now it's my turn!", "Now I give it back.", "The future fights back."],
    magik: ["There are no snowflakes in Hell.", "To me, my Soulsword!", "Welcome to Limbo.", "Soulsword. Now."],
    iceman: ["Iceman cometh!", "I'm Iceman. Infamous mutant.", "Stay frosty.", "Ice to meet you.", "Let's cool things down."],
    jubilee: ["Jubilee's home, safe an' sound.", "Fireworks!", "Let's make some fireworks.", "Boom. Sparkles."],
    nightcrawler: ["BAMF!", "Mein Freund.", "Auf Wiedersehen!"],
    magneto: ["I am Magneto.", "I am Magneto, mightiest of all the mutants!", "Peace was never an option.", "I've been at the mercy of men just following orders. Never again.", "Perfection."],
    maria_hill: ["We are agents of S.H.I.E.L.D. Our jurisdiction is the planet.", "I want the suspect in custody yesterday!", "Nick, the world has changed."],
    nick_fury: ["I've got my eye on you.", "There was an idea...", "Last time I trusted someone, I lost an eye.", "I'm here to talk to you about the Avenger Initiative."],
    black_panther_shuri: ["Wakanda Forever!", "You've faced the muscle of Wakanda... now face its claws!", "What are those?", "Don't scare me like that, colonizer!", "Just because something works doesn't mean it can't be improved."],
    silk: ["When I'm like this, call me Silk!", "Let's spin this up.", "Webs out.", "THWIP !"],
    falcon: ["It's time for the Falcon to fly!", "On your left.", "I do what he does, just slower.", "I'm Captain America."],
    winter_soldier: ["Who the hell is Bucky?", "I'm with you till the end of the line, pal.", "I remember all of them.", "Ready to comply."],
    tigra: ["This cat's got to hunt.", "Claws out.", "Let's hunt.", "Bad kitty."],
    hulkling: ["Didn't see that coming, did you?", "For the Young Avengers!"],
    wonder_man: ["I'm Wonder Man.", "Lights, camera, action!", "Time for the big finish.", "Hollywood meets heroics.", "This one's for the cameras."],
    hercules: ["Have at thee!", "Olympus!", "Behold the might of Hercules!", "A labor worthy of Hercules!"],
    daredevil: ["The Man Without Fear.", "I am Daredevil, and I am not afraid.", "I cannot see the light. So I will be the light.", "I'm Daredevil.", "I'm not seeking penance for what I've done. I'm asking forgiveness for what I'm about to do."],
    echo: ["I absorb an arsenal of actions.", "It's time."],
    jessica_jones: ["...Gotcha.", "I'm just trying to make a living.", "Knowing it's real means you gotta make a decision.", "Alias Investigations. Case closed.", "I'm not wearing a costume."],
    luke_cage: ["Sweet Christmas!", "I got skin like steel and muscles to match.", "I'm Luke Cage.", "You want some?"],

    /* --- homebrew --- */
    spider_man_rainy: ["Your friendly neighborhood Spider-Man!", "With great power comes great responsibility.", "Come on, Spider-Man.", "THWIP !"],
    spider_man_2099: ["I am Spider-Man 2099.", "THWIP !"],
    spider_man_noir: ["Wherever I go, the wind follows. And the wind... smells like rain.", "THWIP !"],
    spider_woman_kajislav: ["Spider-Woman fights back!", "I'm Spider-Woman.", "You picked the wrong spider."],
    stan_lee: ["Excelsior!", "Nuff said!", "Face front, true believers!"],
    sunfire: ["I burn brighter than the sun.", "You want heat? I am heat.", "Sunfire unleashed."],
    superior_iron_man: ["Why settle for Iron Man when you can have Superior Iron Man?", "Perfection is the product.", "Upgrade accepted.", "Superior means better."],
    superior_spider_man: ["I am the Superior Spider-Man!", "Observe true superiority.", "A better Spider-Man has arrived.", "THWIP !"],
    texas_twister: ["Things are getting windy.", "Texas Twister, spin it up!", "Hold onto your hat."],
    the_thing: ["It's clobberin' time!", "What a revoltin' development!"],
    thor_jane_foster: ["For Asgard!", "Whosoever holds this hammer, if they be worthy...", "The Goddess of Thunder answers.", "Mjolnir, to me."],
    throg: ["For Midgard!", "Throg, Frog of Thunder!", "By croak and thunder!", "Tiny hammer, mighty thunder."],
    totally_awesome_hulk: ["Totally awesome!", "Brains and brawn, baby.", "The awesome Hulk is here.", "Gamma genius, coming through."],
    venom_rainy: ["We are Venom.", "Lethal protector.", "Teeth out, tongues out.", "You don't want us hungry."],
    venompool: ["We are Venom. And also hilarious.", "Maximum symbiote."],
    viv_vision: ["I am Viv Vision.", "Probability favors me.", "Processing optimal outcome.", "Logic can be beautiful."],
    wiccan: ["I am Wiccan.", "Magic is in my blood.", "Reality bends for me.", "Spellcasting starts now."],
    wolverine_x23: ["I'm Laura Kinney. I'm Wolverine.", "Don't be what they made you.", "Claws out.", "My turn.", "SNIKT !"],
    yondu: ["I'm Mary Poppins, y'all!"],
    hulk_rainy: ["HULK SMASH!", "Hulk is strongest one there is!", "That's my secret, Captain. I'm always angry.", "Puny god."],
    human_torch: ["Flame on!"],
    invisible_woman: ["Force fields up."],
    iron_lad: ["The future doesn't own me.", "I make my own timeline."],
    iron_man_model_42: ["I am Iron Man.", "Let's test the new tech."],
    iron_patriot: ["Patriot armor, deployed.", "Justice wears red, white, and blue."],
    jessica_jones_custom: ["...Gotcha.", "Alias Investigations. Case closed.", "I'm just trying to make a living.", "I'm not in the hero business. Usually."],
    kate_bishop: ["Kate Bishop is the better Hawkeye.", "Some people have actually called me the world's greatest archer."],
    lockjaw: ["Woof."],
    madame_web: ["The Web of Life and Destiny binds all."],
    mister_fantastic: ["Fantastic."],
    moon_knight: ["I am Moon Knight.", "Random bullshit, go!"],
    ms_america: ["I am America.", "The multiverse has room for me."],
    night_thrasher: ["The streets fight back tonight."],
    // Les deux repliques de Sentinel sont les TEXTES D'AMBIANCE IMPRIMES du
    // pack (Size Advantage et Reboot), pas des phrases inventees.
    sentinel: ["THREAT DETECTED. THREAT INSIGNIFICANT.", "There you are. Knew I could get you back."],
    okoye: ["For Wakanda!", "I am loyal to that throne, no matter who sits upon it."],
    patriot: ["Young heroes, assemble."],
    red_guardian: ["I am Red Guardian.", "Have you ever met Captain America?"],
    rescue_rainy: ["Time to save the day."],
    scarlet_spider: ["Scarlet Spider.", "Webs, impact, repeat.", "Another spider enters the fight.", "Red suit, bad day for you.", "THWIP !"],
    speed: ["Catch me if you can.", "Too slow.", "Speed kills the silence.", "Fast enough for you?"],
    agatha_harkness: ["It was Agatha all along."],
    agent_13: ["Agent 13, in position.", "S.H.I.E.L.D. training pays off."],
    agent_anti_venom: ["The cure hurts.", "Purge the poison."],
    albert: ["SNIKT !"],
    alligator_loki: ["Hiss."],
    angela: ["I am Angela of Heven.", "Grace and slaughter.", "My blades do the talking.", "A warrior from Heven descends."],
    ares: ["War is my domain.", "I am Ares.", "Let battle decide.", "Blood and war."],
    armored_spidey: ["More spider. More armor.", "Webs with plating.", "Tech-enhanced wall-crawling.", "THWIP !"],
    beast: ["Oh my stars and garters!"],
    beta_ray_bill: ["By the hammer, Stormbreaker!"],
    black_cat: ["Bad luck, boys."],
    blade: ["The Daywalker.", "Some motherfucker's always trying to ice-skate uphill."],
    blink: ["Blink!"],
    brawn: ["Brains and brawn.", "Brawn smashing intelligently.", "Gamma power, controlled.", "Strong and smart. Annoying combo."],
    cloak_dagger: ["Light and darkness, together.", "We hunt as one.", "Into the dark. Out in the light."],
    dazzler: ["Lights, camera, Dazzler!", "Turn up the music."],
    doctor_doom: ["Doom does not beg.", "Kneel before Doom!"],
    gwenpool: ["I'm from the real world."],
    howard_the_duck: ["Trapped in a world he never made!"],
};

/**
 * Une réplique au hasard, jamais la même que la dernière quand il y a le
 * choix. `alea` est injecté (Math.random en jeu) pour rester vérifiable.
 */
export function choisirReplique(pool, derniere, alea) {
    if (!pool || pool.length === 0) return undefined;
    const candidates = pool.length > 1 ? pool.filter((r) => r !== derniere) : pool;
    return candidates[Math.floor(alea() * candidates.length)];
}

/** La classe de taille de la carte : une courte claque, une longue se lit. */
export function classeTaille(texte) {
    const n = texte.length;
    if (n <= 15) return "";
    if (n <= 30) return "ono-moyenne";
    if (n <= 60) return "ono-longue";
    return "ono-tres-longue";
}

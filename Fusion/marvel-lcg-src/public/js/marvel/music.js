import { ButtonSetting, Setting } from "./settings.js";
export class Music {
    static playBgm() {
        console.log('Play BGM');
        Music.sound_bgm.src = "./asset/marvel_s_black_widow_official_theme_epic_version.mp3";
        Music.sound_bgm.volume = 0.05;
        Music.sound_bgm.play();
    }
    static pauseBgm() {
        Music.sound_bgm.pause();
    }
    static playClickCardSound() {
        Music.doPlaySound('flip.wav');
    }
    static preloadSound(sound_name) {
        if (!Music.sound_cache[sound_name]) {
            const audio = new Audio(sound_name);
            Music.sound_cache[sound_name] = audio;
        }
    }
    static doPlaySound(sound_name) {
        if (!Setting.is_debug && document.visibilityState != 'visible') {
            return;
        }
        if (!ButtonSetting.music_on) {
            return;
        }
        console.log("Sound:", sound_name);
        Music.preloadSound(sound_name);
        const sound = Music.sound_cache[sound_name];
        sound.volume = 0.2;
        if (!sound.paused) {
            sound.pause();
            sound.currentTime = 0;
        }
        sound.play().catch((error) => {
        });
    }
}
Music.sound_bgm = document.getElementById('play-bgm');
Music.sound_cache = {};
//# sourceMappingURL=music.js.map
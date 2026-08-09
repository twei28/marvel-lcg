import { Setting } from './settings.js';
import { Notifications } from '../lib/notifications.js';
export class Notify {
    static showResponse(text) {
        Notify.create("RESPONSE", "debug", text, 2);
    }
    static showAchievement(text) {
        if (!Setting.show_achievement) {
            return;
        }
        let div = document.querySelector('#achievement-bar');
        div.classList.remove('remove');
        div.classList.add('enter');
        div.innerHTML = text;
        setTimeout(() => {
            div.classList.remove('enter');
            div.classList.add('remove');
        }, 2000);
    }
    static pause() {
        Notify.notis.pause();
    }
    static unpause() {
        Notify.notis.unpause();
    }
    static create(title = "", ex_class_name = "", description = "", duration = 4, destroyOnClick = true, clickFunction = undefined) {
        Notify.notis.create(title, ex_class_name, description, duration, destroyOnClick, clickFunction);
    }
    static showStatisticsText(text) {
        if (!Setting.is_debug && Setting.statistics_off) {
            return;
        }
        let class_name = 'statistics';
        let div_test = `<span class='${class_name}'>${text}</span>`;
        Notify.create("STATISTIC", "", div_test);
    }
    static showStatistics(card_id, text, count) {
        if (!Setting.is_debug && Setting.statistics_first && count != 1) {
            return;
        }
        if (["PutIntoPlay", "Attached", "Hero"].includes(text)) {
            text = "Enters Play";
        }
        let notify_text = `<img class='statistics-notify-img' style='--bg-image-true: url("${card_id}")'></img>  ${text} x${count}`;
        Notify.showStatisticsText(notify_text);
    }
    static showCommand(text) {
        Notify.create("COMMAND", "", text, 2);
    }
}
Notify.notis = new Notifications(document.querySelector(".notifications"));
(() => {
    const logo_code = [
        'KeyI', 'KeyR', 'KeyE', 'KeyF',
        'KeyR', 'KeyI', 'KeyX', 'KeyS',
    ];
    let logo_index = 0;
    let logo_code_string = "";
    document.addEventListener('keydown', (event) => {
        if (event.code === logo_code[logo_index]) {
            logo_index++;
            logo_code_string += event.key;
            if (logo_index === logo_code.length) {
                Notify.create("", "", `${logo_code_string.charAt(0).toUpperCase() + logo_code_string.slice(1)} (c)`);
                logo_index = 0;
                logo_code_string = "";
            }
        }
        else {
            logo_index = 0;
            logo_code_string = "";
        }
    });
})();
//# sourceMappingURL=notify.js.map
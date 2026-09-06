import { ButtonSetting, Setting } from './settings.js';
import { Game } from './game.js';
import { Effect } from './effect.js';
import { Music } from './music.js';
import { Client } from './client.js';
import { Lib } from './lib.js';
import { BtnOk } from './btn_ok.js';
import { Cards } from './cards.js';
import { Message } from './message.js';
import { centerDraggableDiv } from './draggable.js';
class ConnectionManager {
    constructor() {
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectInterval = 1000;
        this.retryTimerId = null;
        this.seconds = 0;
        this.running = false;
        this.isPaused = false;
        this.lostConnectDiv = document.getElementById('lost-connect');
        this.connectingText = document.getElementById('connecting');
        this.waitConnectText = document.getElementById('wait-connect');
        this.retryTimer = document.getElementById('retry-timer');
        this.manualConnectDiv = document.getElementById('manual-connect');
        let reconnectLink = document.getElementById('reconnect-link');
        let reconnectLink2 = document.getElementById('reconnect-link2');
        reconnectLink.addEventListener('click', (event) => {
            event.preventDefault();
            this.reconnectNow();
        });
        reconnectLink2.addEventListener('click', (event) => {
            event.preventDefault();
            this.reconnectNow();
        });
    }
    pause() {
        this.isPaused = true;
    }
    unpause() {
        this.isPaused = false;
    }
    onLostConnect() {
        this.lostConnectDiv.classList.remove('hide');
        this.startReconnect();
    }
    onConnected() {
        this.lostConnectDiv.classList.add('hide');
        this.stopReconnect();
        console.log("Reconnected successfully!");
    }
    startReconnect() {
        this.attemptReconnect();
    }
    attemptReconnect() {
        if (this.running) {
            return;
        }
        this.running = true;
        const connect = () => {
            if (this.retryTimerId) {
                clearTimeout(this.retryTimerId);
                this.retryTimerId = null;
            }
            this.reconnectAttempts++;
            this.reconnectInterval *= 2;
            this.showConnectingPrompt();
            this.running = false;
            UI.doReconnect();
        };
        if (this.reconnectAttempts == 0) {
            connect();
        }
        else if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.seconds = Math.round(this.reconnectInterval / 1000);
            this.connectingText.classList.add('hide');
            this.manualConnectDiv.classList.add('hide');
            this.retryTimer.textContent = this.seconds.toString();
            this.waitConnectText.classList.remove('hide');
            if (this.retryTimerId == null) {
                this.retryTimerId = setInterval(() => {
                    if (!this.isPaused) {
                        this.seconds -= 1;
                        if (this.seconds <= 0) {
                            connect();
                        }
                        else {
                            this.retryTimer.textContent = this.seconds.toString();
                        }
                    }
                }, 1000);
            }
        }
        else {
            this.connectingText.classList.add('hide');
            this.waitConnectText.classList.add('hide');
            this.manualConnectDiv.classList.remove('hide');
            console.log("Max reconnect attempts reached.");
        }
    }
    showConnectingPrompt() {
        this.connectingText.classList.remove('hide');
        this.waitConnectText.classList.add('hide');
    }
    stopReconnect() {
        this.reconnectAttempts = 0;
        this.reconnectInterval = 1000;
        this.running = false;
        this.lostConnectDiv.classList.add('hide');
        this.connectingText.classList.add('hide');
        this.waitConnectText.classList.add('hide');
        this.manualConnectDiv.classList.add('hide');
        this.seconds = 0;
        if (this.retryTimerId) {
            clearInterval(this.retryTimerId);
            this.retryTimerId = null;
        }
    }
    reconnectNow() {
        this.stopReconnect();
        this.onLostConnect();
    }
}
class PromptBox {
    static cleanPromptText() {
        PromptBox.prompt_box_div.classList.add("hide");
    }
    static restartPromptTextAnimation() {
        PromptBox.prompt_box_div.classList.remove("prompt-anime");
        requestAnimationFrame(() => {
            PromptBox.prompt_box_div.classList.add("prompt-anime");
        });
    }
    static setPromptGameOver() {
        PromptBox.setTempPromptText(PromptBox.game_over_text, false);
    }
    static setPromptWait() {
        Game.setGameOver(false);
    }
    static setPromptText(text) {
        if (text) {
            PromptBox.prompt_text = text;
            PromptBox.setTempPromptText(text, false);
        }
        else {
            PromptBox.resetPromptText();
        }
    }
    static setTempPromptText(text, add_on_event = true) {
        if (text) {
            const is_in_play_turn = UI.is_in_play_turn;
            if (add_on_event && is_in_play_turn) {
                add_on_event = false;
            }
            if (!add_on_event || is_in_play_turn) {
                if (text != PromptBox.prompt_text_div.innerHTML) {
                    PromptBox.prompt_text_div.innerHTML = text;
                }
            }
            else {
                PromptBox.prompt_text_div.innerHTML = PromptBox.prompt_text + "<hr/>" + text;
            }
            PromptBox.restartPromptTextAnimation();
            PromptBox.prompt_box_div.classList.remove('hide');
            if (PromptBox.prompt_box_lock.classList.contains('locked')) {
                centerDraggableDiv(PromptBox.prompt_box_div);
            }
        }
        else {
            PromptBox.resetPromptText(true);
        }
    }
    static resetPromptText(hide = false) {
        if (UI.is_in_play_turn || hide) {
            PromptBox.prompt_box_div.classList.add('hide');
        }
        else {
            PromptBox.setTempPromptText(PromptBox.prompt_text, false);
        }
    }
}
PromptBox.prompt_box_div = document.getElementById('prompt-box-container');
PromptBox.prompt_text_div = document.getElementById('prompt-text');
PromptBox.prompt_box_lock = document.getElementById('prompt-box-lock');
PromptBox.game_over_text = "<div class='game-over'>--- Game Over ---</div>";
PromptBox.prompt_text = "";
(() => {
    document.querySelector('#prompt-box-close').onclick = () => {
        PromptBox.cleanPromptText();
    };
    PromptBox.prompt_box_lock.onclick = (e) => {
        const btn = e.target;
        btn.classList.toggle('locked');
    };
})();
export class UI {
    static tempSortDeck(sort) {
        function getObjectId() {
            let object_id = null;
            function can_sort() {
                if (!UI.temp_sorted_deck_div) {
                    return false;
                }
                if (Game.game_over) {
                    return true;
                }
                if (Setting.is_debug) {
                    return true;
                }
                const classesToCheck = ['player-deck', 'additional-deck', 'encounter-deck'];
                return !classesToCheck.some(className => UI.temp_sorted_deck_div.classList.contains(className));
            }
            if (can_sort()) {
                const card_div = UI.temp_sorted_deck_div.querySelector('.card');
                if (card_div) {
                    object_id = Number(card_div.dataset.id);
                }
            }
            return object_id;
        }
        let object_id = getObjectId();
        if (object_id) {
            if (!sort) {
                let a = 1;
            }
            Cards.render.printDeckWhenHighlightTarget([object_id], sort);
        }
    }
    static async init() {
        document.querySelectorAll('.area').forEach(div => {
            div.oncontextmenu = (event) => {
                event.stopPropagation();
                event.preventDefault();
            };
        });
        document.querySelector(`#version`).innerHTML = UI.version;
        UI.hand_card_margin_bottom_div.oninput = function () {
            let element = document.querySelector('#hand-cards');
            element.style.setProperty('--margin-bottom', `${UI.hand_card_margin_bottom_div.value}vw`);
            console.log(UI.hand_card_margin_bottom_div.value);
        };
        UI.hand_card_margin_div.oninput = function () {
            let element = document.querySelector('#hand-cards');
            element.style.setProperty('--card-margin', `${UI.hand_card_margin_div.value}vw`);
            console.log(UI.hand_card_margin_div.value);
        };
        UI.hand_card_total_deg.oninput = function () {
            let element = document.querySelector('#hand-cards');
            element.style.setProperty('--total-deg', `${UI.hand_card_total_deg.value}deg`);
        };
        UI.delay_time = Number(UI.slider_div.value);
        UI.slider_div.oninput = UI.resetDelayTime;
        UI.anime_time_div.oninput = UI.updateAnimeTime;
        UI.updateAnimeTime();
        UI.hideAllTimerBar();
        UI.updateCurrentPlayer(Setting.player_id);
    }
    static setDebugMessage(category, text) {
        if (category == 'debug' || category == 'world') {
            return;
        }
        UI.debug_text = text;
        const debugText = new CustomEvent('debugText', {});
        window.dispatchEvent(debugText);
    }
    static drawLine(divA, divB, class_name = 'target', timeout = 1500) {
        const rectA = Lib.client.getOffset(divA);
        const rectB = Lib.client.getOffset(divB);
        const x1 = rectA.left + divA.offsetWidth / 2;
        const y1 = rectA.top + divA.offsetHeight / 2;
        const x2 = rectB.left + divB.offsetWidth / 2;
        const y2 = rectB.top + divB.offsetHeight / 2;
        const length = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
        const angle = Math.atan2(y2 - y1, x2 - x1);
        const angleInDegrees = angle * (180 / Math.PI);
        const arrow = document.createElement('div');
        const arrow_anime = document.createElement('div');
        arrow_anime.classList.add('target-arrow');
        arrow_anime.classList.add(class_name);
        arrow.appendChild(arrow_anime);
        arrow.classList.add('target-arrow-box');
        arrow.style.position = 'absolute';
        arrow.style.width = '0';
        arrow.style.transformOrigin = '0 0';
        arrow.style.left = `${x1}px`;
        arrow.style.top = `${y1}px`;
        arrow.style.transform = `rotate(${angleInDegrees}deg) translateZ(10px)`;
        document.body.querySelector('#scene').appendChild(arrow);
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                arrow.style.width = `${length}px`;
            });
            setTimeout(() => {
                arrow_anime.classList.add('remove');
                arrow_anime.style.width = `0`;
                setTimeout(() => {
                    arrow.remove();
                }, UI.anime_time * timeout * .5);
            }, UI.anime_time * timeout * 1);
        });
    }
    static firstGameSync() {
        UI.changeWeather('');
    }
    static focusOnPlayer(id) {
        let player_index = id;
        if (Game.forced_on_player == player_index) {
            return;
        }
        let areas = [];
        for (let j = 0; j <= 3; j++) {
            const playerElements = document.querySelectorAll(`.player-${j}`);
            playerElements.forEach(playerElement => {
                if (j === id) {
                    areas.push(playerElement);
                }
                else {
                    playerElement.classList.add('hide-player');
                }
            });
        }
        for (const area of areas) {
            area.classList.remove('hide-player');
        }
        Game.forced_on_player = player_index;
        UI.updateCurrentPlayer(player_index);
        Cards.render.printCards();
        Effect.updateHighLight();
    }
    static updateAnimeTime() {
        if (UI.hold_ctrl) {
            UI.anime_time = .01;
        }
        else {
            UI.anime_time = parseFloat(UI.anime_time_div.value);
        }
        UI.anime_move_time = UI.anime_time * 1.5;
        UI.anime_shuffle_time = UI.anime_time * 4;
        UI.anime_time_card = UI.anime_time * 4;
        document.body.style.setProperty('--anime-time', `${UI.anime_time}s`);
        document.body.style.setProperty('--anime-move-time', `${UI.anime_move_time}s`);
        document.body.style.setProperty('--anime-shuffle-time', `${UI.anime_shuffle_time}s`);
        document.body.style.setProperty('--anime-time-card', `${UI.anime_time_card}s`);
    }
    static resetDelayTime() {
        UI.delay_time = Number(UI.slider_div.value);
    }
    static getDelayTime() {
        let value = parseFloat(UI.anime_time_div.value) * 2000 + 100;
        return value;
    }
    static addDelayTime(time) {
        UI.delay_time += time;
    }
    static setPhaseText(text) {
        UI.phase_div.dataset.phase = text;
    }
    static cleanMessage() {
        const overlay = document.getElementById('message-overlay');
        overlay.style.animation = "";
        overlay.classList.remove('active');
    }
    static setTurnId(round, step) {
        UI.current_div.innerHTML = `Round ${round} Step ${step}`;
        let phase_text = "";
        if (Game.game_over) {
            phase_text = "Game Over";
        }
        else {
            phase_text = Game.world_descriptor.phase;
        }
        let waiting = false;
        if (!UI.please_wait && UI.last_phase_text == phase_text) {
            return 0;
        }
        if (UI.please_wait) {
            waiting = true;
            UI.please_wait = false;
        }
        const last_phase_text = UI.last_phase_text;
        UI.last_phase_text = phase_text;
        let text = "";
        if (round > 0 && !Game.game_over) {
            text = `${phase_text} (${round})`;
        }
        else {
            text = `${phase_text}`;
        }
        let text_div = UI.top_bar_div?.querySelector("#turn-id");
        if (text_div) {
            text_div.innerHTML = text;
        }
        if (!["Initialize",
            "Init Finished",
            "End Phase",
            "End Round",
            "Start Round",
        ].includes(phase_text)) {
            let ms = 1000;
            if (Game.game_over) {
                function extractBooleanAndCleanString(input) {
                    const regex = /\n(True|False)$/;
                    const match = input.match(regex);
                    if (match) {
                        const boolValue = match[1] === 'True';
                        const cleanedString = input.replace(regex, '');
                        return { cleanedString, boolValue };
                    }
                    return { cleanedString: input, boolValue: false };
                }
                const result = extractBooleanAndCleanString(Game.world_descriptor.prompt_last_text);
                Game.world_descriptor.prompt_last_text = result.cleanedString;
                Game.players_won = result.boolValue;
                phase_text = Game.world_descriptor.prompt_last_text.replace(/^\s*--- Game Over ---\s*(.+)$/m, "$1");
            }
            if (phase_text) {
                Message.showMessage(phase_text, ms);
            }
            return 0;
        }
        else {
            if (last_phase_text == "Game Over") {
                UI.cleanMessage();
            }
            return 0;
        }
    }
    static update() {
        if (Effect.response_json_ask?.options.length) {
            BtnOk.setDisable(false);
            BtnOk.setCancel('');
            Effect.updateHighLight();
        }
        else {
            BtnOk.setDisable(true);
        }
    }
    static selectCountClear() {
        for (const card_div of document.querySelectorAll('.card')) {
            card_div.setAttribute('select-count', "");
        }
    }
    static onLostConnect() {
        Music.pauseBgm();
        Game.is_lost_connect = true;
        UI.connection_manager.onLostConnect();
    }
    static onConnected() {
        Game.is_lost_connect = false;
        UI.connection_manager.onConnected();
    }
    static doReconnect() {
        Client.doConnect();
    }
    static hideAllTimerBar() {
        for (let i of [0, 1, 2, 3]) {
            const div = document.querySelector(`#player-${i}-btn`);
            div?.classList.remove('active');
            let bar = div?.querySelector(`.progress-bar`);
            if (bar) {
                bar.remove();
            }
        }
    }
    static updateTimerBar(remaining_time, max_timeout, round, step) {
        let pre = (remaining_time / max_timeout * 100);
        for (let i of Game.asking_players) {
            const div = document.querySelector(`#player-${i}-btn`);
            if (div) {
                div.classList.add('active');
                let bar = div.querySelector(`.progress-bar`);
                if (max_timeout != 0) {
                    if (!bar) {
                        bar = document.createElement('div');
                        bar.className = "progress-bar";
                        div.appendChild(bar);
                    }
                    ((the_bar) => {
                        the_bar.style.transitionDuration = `0s`;
                        the_bar.style.width = `${pre}%`;
                        void the_bar.offsetWidth;
                        the_bar.style.transitionDuration = `${remaining_time}s`;
                        requestAnimationFrame(() => {
                            the_bar.style.width = "0";
                        });
                    })(bar);
                }
                else {
                    if (bar) {
                        bar.remove();
                    }
                }
            }
        }
    }
    static changeWeather(weather, forced = false) {
        if (forced || UI.weather != weather) {
            if (!ButtonSetting.enable_enhance_fx) {
                UI.iframe.src = "";
            }
            else {
                UI.weather = weather;
                if (weather) {
                    UI.iframe.src = `/effects/weather/${weather}.html`;
                }
                else {
                    UI.iframe.src = "";
                }
            }
        }
    }
    static updateCurrentPlayer(player_id) {
        document.body.classList.remove('current_player_0');
        document.body.classList.remove('current_player_1');
        document.body.classList.remove('current_player_2');
        document.body.classList.remove('current_player_3');
        document.body.classList.add(`current_player_${player_id}`);
    }
}
UI.btn_end_div = document.getElementById('btn-end');
UI.btn_ok_div = document.getElementById('btn-ok');
UI.prompt = PromptBox;
UI.top_bar_div = document.getElementById('top-bar');
UI.event_name = "";
UI.is_in_play_turn = false;
UI.slider_div = document.getElementById("delay-range");
UI.delay_time = 400;
UI.last_game_id = -1;
UI.version = Lib.cookie.getString("app_version");
UI.last_phase_text = "";
UI.please_wait = false;
UI.hand_card_margin_div = document.getElementById("hand-card-margin");
UI.hand_card_total_deg = document.getElementById("hand-card-total-deg");
UI.hand_card_margin_bottom_div = document.getElementById("hand-card-margin-bottom");
UI.anime_time_div = document.getElementById("anime-time");
UI.phase_div = document.querySelector('#phase');
UI.current_div = document.querySelector("#current-round");
UI.iframe = document.getElementById("weather-background");
UI.weather = "";
UI.anime_time = 0;
UI.anime_move_time = 0;
UI.anime_shuffle_time = 0;
UI.anime_time_card = 0;
UI.error_occurred_text = "";
UI.hold_ctrl = false;
UI.hold_alt = false;
UI.hold_shift = false;
UI.temp_sorted_deck_div = null;
UI.global_first_create = true;
UI.anime_move_cards_count = 0;
UI.anime_shuffle_cards_count = 0;
UI.background_image_normal = `linear-gradient(0deg, rgba(255,255,255,0) 0%, rgba(255,255,255,1) 100%)`;
UI.background_image_super_rare = `linear-gradient(120deg, #ff0084FF 15%, #fca400FF 30%, #ffff00FF 40%, #00ff8aFF 60%, #00cfffFF 70%, #cc4cfaFF 85%)`;
UI.background_image_ultra_rare = `linear-gradient(0deg, rgba(255,255,255,0) 0%, gold 100%)`;
UI.debug_text = "";
UI.connection_manager = new ConnectionManager();
window.UI = UI;
//# sourceMappingURL=ui.js.map
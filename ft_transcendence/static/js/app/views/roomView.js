import AbstractView from "./abstractView.js";
import PongRoomManager from "../managers/PongRoomManager.js";
import { PongGame } from "/static/pong/js/PongGame.js";

export default class Room extends AbstractView {
    constructor() {
        super();
        this.setTitle("Play");
        this.pongRoomManager = new PongRoomManager();
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('Play html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading login page</p>";
        }
    }

    loadComponents() {
        this.initGame();
    }

    //Drawing Game Canvas

    initGame()
    {
        //Get canvas and context
        const canvas = document.getElementById("pongCanvas");
        const context = canvas.getContext("2d");
        
        this.pongRoomManager.createGame(context, canvas.width, canvas.height);

        this.connectSocket();
    }

    connectSocket()
    {
        //Get game data
        const gameData = document.getElementById("game-data");
        const roomId = gameData.dataset.roomId;
        const gameMode = gameData.dataset.gameMode;
        
        log.info("room_id:", roomId);
        log.info("game_mode:", gameMode);

        let socketUrl;

        if (gameMode === "tournament") {
            socketUrl = `ws://${window.location.host}/ws/pong/tournament_match/${roomId}/`;
          } else {
            socketUrl = `ws://${window.location.host}/ws/pong/${gameMode}/`;
          }

        this.pongRoomManager.connectSocket(socketUrl);
        this.pongRoomManager.loadEventHandlers();
    }



    bindUIEventHandlers() {
        console.log('Loading play event handlers...');
    }

    removeUIEventHandlers() {
        console.log('Removing play event handlers...');
    }
}
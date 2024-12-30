import AbstractHandler from "./abstractHandler.js";
import { navigateTo } from "../index.js";

export default class CreateTournamentHandler extends AbstractHandler {
    constructor() {
        super();
        this.updateUI = this.updateUI.bind(this);
    }


    async postForm(form) {
        const formData = new FormData(form);

        const submitButton = form.querySelector('button[type="submit"]:focus');
        const maxPlayers = submitButton ? submitButton.value : null;


        if (maxPlayers) {
            formData.append('max_players', maxPlayers); // Adiciona ao FormData
        } else {
            console.error("Erro: max_players não foi selecionado");
        }
    
        // Exibe todos os campos do FormData para depuração
        for (const [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }
    
    
        return fetch(form.action, {
            method: form.method,
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(response => {
                if (response.ok) {
                    console.log("Success:", response);
                    return response;
                } else {
                    console.error("Failed to submit form:", response.statusText);
                    return response;
                }
            })
            .catch(error => {
                console.error("Error:", error);
                throw error;
            }
            );
    }


    async updateUI(view, context) {
        view.bindUIEventHandlers();
        if (context.ok)
            navigateTo("/enter/tournament/");
        else
            console.log("erro: torneio nao foi criado")
    }

    getContext(_form, response) {
        return response;
    }
}
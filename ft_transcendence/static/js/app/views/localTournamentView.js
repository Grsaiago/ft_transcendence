import LocalTournamentManager from "../managers/localTournamentManager.js";
import AbstractView from "./abstractView.js";

export default class LocalTournament extends AbstractView {
    constructor() {
        super();
        this.setTitle("Local Tournament");

        this.handleStartFormSubmit = this.handleStartFormSubmit.bind(this);
        this.updateMatchesUI = this.updateMatchesUI.bind(this);
        this.playButon1Handler = this.playButon1Handler.bind(this);
        this.playButon3Handler = this.playButon3Handler.bind(this);
        this.playButon2Handler = this.playButon2Handler.bind(this);
        this.playButon4Handler = this.playButon4Handler.bind(this);
        this.playButon5Handler = this.playButon5Handler.bind(this);
        this.playButon6Handler = this.playButon6Handler.bind(this);
        this.playButon7Handler = this.playButon7Handler.bind(this);
    }

    async getHtml(url) {
        try {
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('Room html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading Room page</p>";
        }
    }

    bindUIEventHandlers() {
        console.log('Loading enter event handlers...');
        document.getElementById("tournamentForm").addEventListener("submit", this.handleStartFormSubmit);
        
        this.bindLocalTournamentManagerEvents();
        this.bindPlayButtonEventHandlers();
    }

    bindLocalTournamentManagerEvents() {
        document.addEventListener('match_status_updated', this.updateMatchesUI);
        document.addEventListener('tournamentChampion', this.handleChampion);
    }

    bindPlayButtonEventHandlers() {
        document.getElementById("btn-Match1").addEventListener("click", this.playButon1Handler)
        document.getElementById("btn-Match3").addEventListener("click", this.playButon3Handler)
        document.getElementById("btn-Match2").addEventListener("click", this.playButon2Handler)
        document.getElementById("btn-Match4").addEventListener("click", this.playButon4Handler)
        document.getElementById("btn-Match5").addEventListener("click", this.playButon5Handler)
        document.getElementById("btn-Match6").addEventListener("click", this.playButon6Handler)
        document.getElementById("btn-Match7").addEventListener("click", this.playButon7Handler)
    }

    playButon1Handler() {
        console.log("Buton 1 test handler");
        const match = this.localTournamentManager.matches.find(m => m.matchId === 'Match1');
        console.log(match['Match1-p1']);
        this.localTournamentManager.updateMatchesOnWinner('Match1', match['Match1-p1']);
    }

    playButon3Handler() {
        console.log("Buton 3 test handler");
        const match = this.localTournamentManager.matches.find(m => m.matchId === 'Match3');
        console.log(match['Match3-p1']);
        this.localTournamentManager.updateMatchesOnWinner('Match3', match['Match3-p1']);
    }

    playButon2Handler() {
        console.log("Buton 2 test handler");
        const match = this.localTournamentManager.matches.find(m => m.matchId === 'Match2');
        console.log(match['Match2-p1']);
        this.localTournamentManager.updateMatchesOnWinner('Match2', match['Match2-p1']);
    }

    playButon4Handler() {
        console.log("Buton 4 test handler");
        const match = this.localTournamentManager.matches.find(m => m.matchId === 'Match4');
        console.log(match['Match4-p1']);
        this.localTournamentManager.updateMatchesOnWinner('Match4', match['Match4-p1']);
    }

    playButon5Handler() {
        console.log("Buton 5 test handler");
        const match = this.localTournamentManager.matches.find(m => m.matchId === 'Match5');
        console.log(match['Match5-p1']);
        this.localTournamentManager.updateMatchesOnWinner('Match5', match['Match5-p1']);
    }

    playButon6Handler() {
        console.log("Buton 6 test handler");
        const match = this.localTournamentManager.matches.find(m => m.matchId === 'Match6');
        console.log(match['Match6-p1']);
        this.localTournamentManager.updateMatchesOnWinner('Match6', match['Match6-p1']);
    }

    playButon7Handler() {
        console.log("Buton 7 test handler");
        const match = this.localTournamentManager.matches.find(m => m.matchId === 'Match7');
        console.log(match['Match7-p1']);
        this.localTournamentManager.updateMatchesOnWinner('Match7', match['Match7-p1']);
    }

    handleStartFormSubmit(event) {
        event.preventDefault();

        //Form Validations
        const form = event.target;
        const inputs = form.querySelectorAll("input");
        const playersNames = Array.from(inputs).map(input => input.value.trim());
        const warnElem = document.getElementById("p-warn");

        const duplicateInputIndexes = this.getDuplicateInputIndexes(playersNames);

        if (duplicateInputIndexes.length > 0) {
            this.clearDuplicateInputs(duplicateInputIndexes, inputs);
            warnElem.innerText = "Duplicate names not allowed";
            return;
        }

        this.cleanFormsWarnsErros(inputs, warnElem);

        this.startTournament(playersNames);
    }

    startTournament(playersNames) {
        this.localTournamentManager = new LocalTournamentManager(playersNames);
        this.localTournamentManager.createMatches();
        console.log(this.localTournamentManager.matches);

        this.deactivateStartButton();
    }

    updateMatchesUI() {
        this.localTournamentManager.matches.forEach((match) => {
            const matchDiv = document.getElementById(match.matchId); // Get the match container by ID
            if (!matchDiv) {
                console.warn(`Match container with ID ${match.matchId} not found.`);
                return;
            }

            // Update player 1 and player 2 names
            const player1Div = document.getElementById(`${match.matchId}-p1`);
            const player2Div = document.getElementById(`${match.matchId}-p2`);
            const statusText = document.getElementById(`status-${match.matchId}`);
            const matchBtn = document.getElementById(`btn-${match.matchId}`);

            if (player1Div) player1Div.textContent = match[`${match.matchId}-p1`] || "TBD";
            if (player2Div) player2Div.textContent = match[`${match.matchId}-p2`] || "TBD";

            // Update match button
            // if (matchBtn) {
            //     if (match.status === "ready") {
            //         matchBtn.textContent = "Start";
            //         matchBtn.disabled = false;
            //     } else if (match.status === "finished" && match.winner) {
            //         matchBtn.textContent = `Finished! Winner: ${match.winner}`;
            //         matchBtn.disabled = true;
            //     }
            // }



            if (match.status === "ready") {
                statusText.classList.add("d-none");
                matchBtn.classList.remove("d-none");
                matchBtn.disabled = false;
            } else if (match.status === "finished" && match.winner) {
                statusText.textContent = `Winner for ${match.matchId} set to ${match.winner}`;
                statusText.classList.remove("d-none");
                matchBtn.classList.add("d-none");
                matchBtn.disabled = true;
            } else {
                statusText.textContent = "waiting for game...";
                statusText.classList.remove("d-none");
                matchBtn.classList.add("d-none");
                matchBtn.disabled = true;
            }
        });
    }

    handleChampion(event) {
        console.log("The tournament ended! The winner is: ", event.detail);
    }

    deactivateStartButton() {
        const startButton = document.getElementById("startTournament");
        const startTournamentText = document.getElementById("startTournamentText");
        
        if (startButton) {
            startButton.style.display = "none"; // Esconde o botão
            startButton.disabled = true;
        }
        if (startTournamentText) {
            startTournamentText.classList.remove("d-none"); // Exibe o texto
        }
    }

    getDuplicateInputIndexes(names) {
        const seenNames = new Map(); // Tracks first occurrence index of each name
        const duplicateIndices = [];
    
        // Check for duplicates
        names.forEach((name, index) => {
            if (seenNames.has(name)) {
                duplicateIndices.push(index); // Add duplicate occurrence to list
            } else {
                seenNames.set(name, index); // Store the first occurrence
            }
        });

        return duplicateIndices;
    }

    clearDuplicateInputs(duplicateNameIndexes, inputs) {
        if (duplicateNameIndexes.length > 0) {
            duplicateNameIndexes.forEach(index => {
                inputs[index].value = ""; // Clear the input field
                inputs[index].classList.add("is-invalid"); // Highlight cleared field
            });
            return;
        }
    }

    cleanFormsWarnsErros(inputs, warnElem) {
        warnElem.innerText = "";
        inputs.forEach(input => {
            input.classList.remove("is-invalid");
        });
    }

    removeUIEventHandlers() {
        console.log('Removing enter event handlers...');
    }
}

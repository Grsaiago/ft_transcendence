import AbstractView from "./abstractView.js";

export default class Login extends AbstractView {
    constructor() {
        super();
        this.setTitle("Login");
    }

    async getHtml() {

        const retorno = await fetch("http://www.google.com" );

        console.log(retorno);

        return retorno;
    }
}

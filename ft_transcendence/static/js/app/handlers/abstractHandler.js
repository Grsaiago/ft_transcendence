export default class AbstractHandler {
    constructor() {
        if (this.constructor === AbstractHandler) {
            throw new Error("AbstractHandler is an abstract class and cannot be instantiated directly.");
        }
    }

    async postForm(form) {
        const formData = new FormData(form);
        const data = new URLSearchParams(formData);

        return fetch(form.action, {
            method: form.method,
            body: data,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then(response => {
                if (response.ok) {
                    console.log("Success:", data);
                } else {
                    console.error("Failed to submit form:", response.statusText);
                }
            })
            .catch(error => {
                console.error("Error:", error);
            }
            );
    }

    async updateUI(_view, _context) { }

    getContext() { }
}

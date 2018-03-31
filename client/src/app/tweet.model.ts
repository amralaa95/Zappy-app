export class Tweet {
    private text: string;
    private time: string;
    constructor(text: string, time: string) {
        this.text = text;
        this.time = time;
    }
    getText() {
        return this.text;
    }
    getTime() {
        return this.time;
    }
}

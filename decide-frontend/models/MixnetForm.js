
export class Auth {
    constructor(name,url) {
        this.name = name;
        this.url = url;
    }
}

export class Pubkey {
    constructor(p,g,y) {
        this.p = p;
        this.g = g;
        this.y = y;
    }
}

export 
class MixnetForm {
    constructor() {
        this.voting = null;
        this.auths = [];
        this.pubkey = {p:null,g:null,y:null};
        this.position = null;
    }
    
}


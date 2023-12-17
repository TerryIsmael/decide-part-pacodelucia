export default
class Voting {
    constructor(id, name, desc, question, start_date, end_date, pub_key, auths, tally, postproc) {
        
            this.id = id
            this.name = name
            this.desc = desc
            this.question = question
            this.start_date = start_date
            this.end_date = end_date
            this.pub_key = pub_key
            this.auths = auths
            this.tally = tally
            this.postproc = postproc
        }
    }

class pub_key {
    constructor(p, g, y){
        this.p = p;
        this.g = g;
        this.y = y;
    }
}

class auths {
    constructor(name, url, me){
        this.name = name;
        this.url = url;
        this.me = me;
    }
}

class question {
    constructor(desc, options){
        this.desc = desc;
        this.options = options;
    }
}

class option {
    constructor(number, option) {
        this.number = number
        this.option = option
    }
}

class postproc {
    constructor(votes, number, option, postproc){
        this.votes = votes;
        this.number = number;
        this.option = option;
        this.postproc = postproc;
    }
}
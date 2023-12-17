export default 
class User {
    constructor(id, username, password, first_name, last_name, email_address) {
        this.id = id;
        this.username = username;
        this.password = password;
        this.first_name = first_name;
        this.last_name = last_name;
        this.email_address = email_address;
        this.is_active = true;
        this.is_staff = false;
        this.is_superuser = false;
    }
}
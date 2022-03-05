document.getElementById("addUserButton").addEventListener("click", function() {
    var firstName = document.getElementById("first_name").value;
    var lastName = document.getElementById("last_name").value;
    var email = document.getElementById("email").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;

    if(firstName && lastName && email && username && password) 
    {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        validationStatus = re.test(String(email).toLowerCase());

        if(validationStatus)
        {
            var body = {
                first_name: firstName,
                last_name: lastName,
                email: email,
                username: username,
                password: password,
                csrfmiddlewaretoken: csrf
            }

            var queryString = Object.keys(body).map((key) => {
                return encodeURIComponent(key) + '=' + encodeURIComponent(body[key])
            }).join('&');
            console.log(queryString);

            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/form/user/add");
            xhr.send(queryString);

            xhr.onload = function () {
                alert("ok");
            }
        }
        else alert("Почта не корректная!")
    }
    else alert("Введите все поля!")
});

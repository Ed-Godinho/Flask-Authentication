function togglePassVisibility(inputId, iconId) {
    var input = document.getElementById(inputId);
    var icon = document.getElementById(iconId);

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}


function alternarClasses() {
    var loginDiv = document.querySelector('.login');
    var signupDiv = document.querySelector('.signup');
    // Alternar as classes após um atraso de 0.5 segundos
    signupDiv.classList.toggle('inactive');
    signupDiv.classList.toggle('active');
    setTimeout(function () {
        loginDiv.classList.toggle('inactive');
        loginDiv.classList.toggle('active');
    }, 500); // 500 milissegundos = 0.5 segundos
}


const cadastro = document.getElementById('form-signup');



cadastro.addEventListener('submit', (e) => {
    e.preventDefault();

    //Dados do cadastro
    let username = document.getElementById('usuario').value;
    let email = document.getElementById('email').value;
    let senha = document.getElementById('senha1').value;
    let confirmSenha = document.getElementById('senha2').value;

    if (senha !== confirmSenha) {
        alert('Senhas não conferem');
        document.getElementById('senha1').style.border = '1px solid red';
        document.getElementById('senha2').style.border = '1px solid red';
        return;
    }

    let formData = {
        'username': username,
        'email': email,
        'senha': senha
    };

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(formData)
    };

    fetch('/cadastro', options)
        .then(response => response.json())
        .then(data => {
            if (data.success) {

                alert('Cadastro realizado com sucesso');
                alternarClasses()

            } else if (data.exists) {
                //mostra o return da API
                alert(data.message);
            } else {
                alert(data.message)
            }
        })
        .catch(error => {
            console.error("Erro na solicitação", error);
            alert('Erro na solicitação');
        });
});

//Validaciones

function validarCadena(cadena){
    return cadena.value.length > 3;
}

function validarIdentificacion(identificacion){
    return Number.isInteger(Number.parseInt(identificacion.value));
}

function validarTelefono(telefono){
    return telefono.value.match(/^(?:(?:00)?549?)?0?(?:11|[2368]\d)(?:(?=\d{0,2}15)\d{2})??\d{8}$/);
}

function validarEmail(email){
    return email.value.match(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/);
}

function validarCadenas(cadenas,spanes){
    let valido = true;
    for(i in cadenas){
        if(!validarCadena(cadenas[i])){
            valido = false;
            spanes[i].textContent = "Colocar 3 o más caracteres";
        }
    }
    return valido;
}

const form = document.querySelector('form');



form.addEventListener('submit',(event) => {
    event.preventDefault();
    const nombre = document.querySelector("#nombre");
    const apellido = document.querySelector("#apellido");
    const identificacion = document.querySelector("#identificacion");
    const telefono = document.querySelector("#telefono");
    const email = document.querySelector("#email");
    var error = false;
    if(!validarCadena(nombre)){
        let span = document.querySelector("#errorNombre");
        span.textContent = "Colocar 3 o más caracteres";
        error = true;
    }
    if(!validarCadena(apellido)){
        let span = document.querySelector("#errorApellido")
        span.textContent = "Colocar 3 o más caracteres";
        error = true;
    }
    if (!validarIdentificacion(identificacion)){
        let span = document.querySelector("#errorIdentificacion");
        span.textContent = "Colocar número entero";
        error = true;
    } 
    if(!validarTelefono(telefono)){
        let span = document.querySelector("#errorTelefono");
        span.textContent = "Colocar 10 dígitos más prefijos opcionales";
        error = true;
    }
    if(!validarEmail(email)){
        let span = document.querySelector("#errorEmail");
        span.textContent = "Colocar: usuario + @ + servidor + dominio";
        error = true;
    }
    if(!error){
        form.submit()
        window.location.replace("index.html");
        // const registro = document.querySelector(".registro");
        // registro.innerHTML = "<div><h2>Bienvenido</h2></div>";      //No entiende el evento la página index   
    }
})
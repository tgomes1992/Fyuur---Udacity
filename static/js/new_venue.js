let btn = document.querySelector(".btn")
let genres = document.querySelector("#genres").selectedOptions


function generos(){
    gen = ""
    
    for(i=0;i<genres.length;i++){
        gen+= genres[i].value + ","
    }
    return gen.slice(0,gen.length-1)
}


function envio(){
    let dados  = {
        "name"  :  document.querySelector("#name").value,
        "city" :  document.querySelector("#city").value,
        "state"  :  document.querySelector("#state").value,
        "phone" :  document.querySelector("#phone").value,
        "genres"  :  generos(),
        "facebook_link": document.querySelector("#facebook_link").value,
        "img_link": document.querySelector("#img_link").value,
        "website": document.querySelector("#website").value
    }

    $.post("/venues/create",dados,()=>{
        console.log("dados enviados")
    })
    console.log(dados)
}




botao.click(envio())




console.log("arquivo aberto");
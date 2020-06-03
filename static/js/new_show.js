let btn = document.querySelector(".btn")


function requisicao(){

    let dados = {
        "name" : document.querySelector("#name").value,
        "artist_id" : document.querySelector("#artist_id").value,
        "venue_id" : document.querySelector("#venue_id").value,
        "start_time" : document.querySelector("#start_time").value
    }
    
    $.post("/shows/create",dados,()=>{
        console.log("dados enviados")
   })


}




btn.click(requisicao())

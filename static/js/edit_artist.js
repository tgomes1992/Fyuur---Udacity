let btn  = $(".btn");
let artista = new Artist();
let options = $("option")
let genres = $("#genres").attr("data").split(",")
let form = $("form")


for (let i=0;i < genres.length;i++){
    let i2=i
    for (let j=0;j<options.length;j++){
        if (genres[i2] == options[j].value){
            options[j].setAttribute("selected","selected")

        }
    }
}




// form.submit(()=>{

//     alert("certo")
// })

btn.click(()=>{
    artista.editartist()
})


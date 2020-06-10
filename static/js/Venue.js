class Venue{ 
    constructor(){
        this.name = document.querySelector("#name");
        this.city = document.querySelector("#city");
        this.state = document.querySelector("#state");
        this.phone = document.querySelector("#phone");
        this.genres = document.querySelector("#genres").selectedOptions;
        this.facebook_link = document.querySelector("#facebook_link");
        this.image_link = document.querySelector("#img_link");
        this.website = document.querySelector("#website");
    }

    generos(){
        let genres = ""
        for (let i=0;i<this.genres.length;i++) {
            genres += this.genres[i].value+","
        }
        return genres.slice(0,genres.length-1)
    }

    criar_json(){
        let dados  = {
            "name"  :  this.name.value,
            "city" :  this.city.value,
            "state"  :  this.state.value,
            "phone" :  this.phone.value,
            "genres"  :  this.generos(),
            "facebook_link": this.facebook_link.value,
            "img_link": this.image_link.value,
            "website": this.website.value,
        }
        return dados
    }

    newvenue(){
        let dados = this.criar_json()
        $.post('/venues/create',dados,()=>{
            return console.log("dados enviados")
         })
        return console.log("done")
    }

    editvenue(){
        let id  = btn.attr("data")
        let dados = this.criar_json()
        console.log(dados)
        $.post("/venues/"+ id +"/edit",dados,()=>{
            return console.log("dados enviados")
         })
    }


    deletevenue(){
        let dados = this.criar_json()
        $.post("/artists/create",dados,()=>{
            return console.log("dados enviados")
         })
        return 0
    }

}
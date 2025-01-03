function setToday(){
    document.getElementById("end_date").valueAsDate = new Date()
    console.log('set date')
}

function closeExportWindow(){
    $('.export_layer').css('display', 'none')
}

function openExportWindow (){
    $('.export_layer').css('display', 'flex')
}

async function getExport(){
    let start_time = new Date($('#start_date').val())
    let end_time   = new Date($('#end_date').val())
    if (start_time != undefined && end_time != undefined){
        start_time = parseInt(start_time / 1000)
        end_time = parseInt(end_time / 1000)

        let res = await fetchExport(start_time, end_time)

        if (res){
            alert('Операция выполнена, загрузка сейчас начнется')
        }
        else{
            alert('Произошла ошибка, операция не выполнена')
        }
    }
    else{
        alert('Пожалуйста, укажите даты')
    }
    
}
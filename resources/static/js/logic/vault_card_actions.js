var cur_times={}

for(i=0;i<devices_data.length;i++){
    console.log(i)
    if (devices_data[i]['last_change_event']){
        cur_times[devices_data[i]['info']['id']] = devices_data[i]['last_change_event']['value']
    }
    else{
        cur_times[devices_data[i]['info']['id']]=0
    }
    
}
console.log(cur_times)

function moveVault(target, time, angle){ 
    
    $(target).css('transition-duration', `${time}ms`)
    $(target).css('transform', `rotate(-${angle}deg)`)
    
    console.log('done')
}

async function changeVaultValue(target_id, time){
    // error handling
    // fetching
    console.log('time', time)

    console.log(cur_times[target_id])
    cur_times[target_id] = cur_times[target_id] + time

    let res = await sendChangeEvent(target_id, time)

    if (res){
        if (cur_times[target_id] > FULL_TIME){
            cur_times[target_id] = FULL_TIME
        }
        if (cur_times[target_id] < 0){
            cur_times[target_id] = 0
        }
        console.log(cur_times[target_id])
    
        $(`#vault_position_loader_${target_id}`).css('display', 'block')
        $(`#vault_change_input_${target_id}`).val('');

        blockCardActions(target_id)
        
    
        moveVault(`#vault_line_${target_id}`, time, cur_times[target_id]/FULL_TIME*ANGLE_AMMOUNT)
    
        setTimeout(() => {
                                $(`#vault_position_text_${target_id}`).html(`${Math.round((cur_times[target_id]/FULL_TIME*ANGLE_AMMOUNT)*100)/100}°`)
                                $(`#vault_position_loader_${target_id}`).css('display', 'none')
                                unblockCardActions(target_id)
                                togle_apply_btn(target_id, true)
                            },     
                    Math.abs(time)
                    )
    }
    else{
        alert('Ошибка\nЗначение не было применено')
    }

    
}

function updateVaultText(){
    vault_position_text_
}

function togle_apply_btn(target_id, val){
    console.log('test test')
    if (val){
        $(`#vault_apply_btn_${target_id}`).attr('disabled','disabled');
    }
    else{
        $(`#vault_apply_btn_${target_id}`).removeAttr('disabled');
    }
}

function initSetting(){
    for (dev_id in cur_times){
        console.log(dev_id, cur_times[dev_id])
        moveVault(`#vault_line_${dev_id}`, 0, cur_times[dev_id]/FULL_TIME*ANGLE_AMMOUNT)
    }
    
}


function resetVault(target_id){
    $(`#status_icon_${target_id}`).removeClass('warn').removeClass("ok").addClass("updating");
    blockCardActions(target_id)

    fetchResetVaultGate(target_id).then(res =>{
        console.log('res', res)

        if (res){

            cur_times[target_id] = 0

            $(`#status_icon_${target_id}`).removeClass('updating').addClass("ok");

            $(`#vault_position_loader_${target_id}`).css('display', 'block')
            $(`#vault_change_input_${target_id}`).val('');
            blockCardActions(target_id)
        
            moveVault(`#vault_line_${target_id}`, FULL_TIME, cur_times[target_id]/FULL_TIME*ANGLE_AMMOUNT)
        
            setTimeout(() => {
                                    $(`#vault_position_text_${target_id}`).html(`${Math.round((cur_times[target_id]/FULL_TIME*ANGLE_AMMOUNT)*100)/100}°`)
                                    $(`#vault_position_loader_${target_id}`).css('display', 'none')
                                    unblockCardActions(target_id)
                                    togle_apply_btn(target_id, true)
                                },     
                        Math.abs(FULL_TIME)
                        )
    
        }
        else{
            $(`#status_icon_${target_id}`).removeClass('updating').addClass("warn");
            blockCardActions(target_id)
        }
    })    
}

function blockCardActions(target_id){
    $(`#vault_change_input_${target_id}`).attr('disabled','disabled');
    $(`#vault_apply_btn_${target_id}`).attr('disabled','disabled');
}

function unblockCardActions(target_id){
    $(`#vault_change_input_${target_id}`).removeAttr('disabled');
    $(`#vault_apply_btn_${target_id}`).removeAttr('disabled');
}

initSetting()

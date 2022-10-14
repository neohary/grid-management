function get_bool(bool){
    //var badgediv = document.createElement('span')
    //var badge = document.createElement('i')
    if(bool == false){
        //badgediv.classList.add('bg-danger','badge','rounded-circle','d-flex','justify-content-center')
        //badge.classList.add('fa-solid','fa-xmark','align-self-center')
        return "否"
    }else{
        //badgediv.classList.add('bg-success','rounded','badge','rounded-circle','d-flex','justify-content-center')
        //badge.classList.add('fa-solid','fa-check','align-self-center')
        return "是"
    }
    //badgediv.style.setProperty('width',"24px")
    //badgediv.style.setProperty('height',"24px")
    //badgediv.appendChild(badge)
    //return badgediv.outerHTML
}

function confirmDelete(id,index){
    var datacol = $('tr[data-index='+ index +']');
    $('.modal-title').text("确认")
    $('.modal-body').html(
        "确定要删除 "+$('.village_name',datacol).text()+" "+$('.grid_name',datacol).text() + " 第" + $('.mgridID',datacol).text()+ "户 (" + $('.population',datacol).text() + "人) 吗？"
        + "<br> 属于该户的居民信息也会一并删除。")
    var confirm = document.createElement('button')
    confirm.id = 'c-delete'
    confirm.classList.add('btn','btn-danger')
    confirm.innerText = "确定"
    confirm.setAttribute('data-bs-dismiss','modal')
    $('#c-delete').remove();
    $('.modal-footer').append(confirm);
    $('#c-delete').on('click',function(){
        var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
        //var pk = parseInt(id)
        $.ajax({
            url:'/api/houses/'+id+'/',
            type:'DELETE',
            headers:{
                "X-CSRFToken": CSRFtoken,
            },
            success:() => {
                $('#table').bootstrapTable('hideRow', {
                    index: index
                })
                $('#toast').removeClass('border-success text-success border-danger text-danger')
                    .addClass('border-success text-success')
                $('#toast .toast-body').text($('.village_name',datacol).text()+" "+$('.grid_name',datacol).text() + " 第" + $('.mgridID',datacol).text()+ "户 (" + $('.population',datacol).text() + "人) 已删除")
                $('#toast').toast('show');
            },
            error:(error) => {
                $('#toast').removeClass('border-success text-success border-danger text-danger')
                    .addClass('border-danger text-danger')
                $('#toast .toast-body').text($('.village_name',datacol).text()+" "+$('.grid_name',datacol).text() + " 第" + $('.mgridID',datacol).text()+ "户 (" + $('.population',datacol).text() + "人) 删除失败："+error.responseJSON.message)
                $('#toast').toast('show');
            }
        })
    })
}

function translateDatatypes(datatypes,id,title) {
    var result = {}
    var i_title = []
    var fields = []
    var i = 0;
    i_title.push({title:title,colspan:Object.entries(datatypes).length,align:'center'})
    Object.entries(datatypes).forEach(e => {
        fields[i] = {field:id+'-'+e[0],title:e[1][0],sortable:true,class:id+'-'+e[0]}
        i++;
    })
    result['title'] = i_title
    result['fields'] = fields

    return result
}

function translateInstances(data,t_id,obj_pk) {
    var result = []
    var i = 0;
    var temp = {}
    temp['id'] = obj_pk
    //console.log("模板: "+t_id+' '+'对象: '+obj_pk)
    Object.entries(data).forEach(e => {
        //field名 = t_id-e[0]
        //内容 = e[1]
        var field = t_id+'-'+e[0]
        if(typeof(e[1]) == "boolean"){
            if(e[1] == true){
                e[1] = "是"
                //e[1] = ['<span class="bg-success rounded badge rounded-circle d-flex justify-content-center" style="width: 24px; height: 24px;"><i class="fa-solid fa-check align-self-center"></i></span>'].join('')
            }else{
                e[1] = "否"
                //e[1] = ['<span class="bg-danger badge rounded-circle d-flex justify-content-center" style="width: 24px; height: 24px;"><i class="fa-solid fa-xmark align-self-center"></i></span>'].join('')
            }
        }
        temp[field] = e[1]
    })
    result = result.concat(temp)
    //console.log('-----------------')
    return temp
}

function iconFormatter(){
    return [
        '<i class="fa-solid fa-caret-down"></i>'
    ].join('')
}

function namelinkFormatter(id,name){
    return [
        '<a href="/resident/' + id +'">'+ name +'</a>'
    ].join('')
}
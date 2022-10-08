function get_bool(bool){
    var badgediv = document.createElement('span')
    var badge = document.createElement('i')
    if(bool == false){
        badgediv.classList.add('bg-danger','badge','rounded-circle','d-flex','justify-content-center')
        badge.classList.add('fa-solid','fa-xmark','align-self-center')
    }else{
        badgediv.classList.add('bg-success','rounded','badge','rounded-circle','d-flex','justify-content-center')
        badge.classList.add('fa-solid','fa-check','align-self-center')
    }
    badgediv.style.setProperty('width',"24px")
    badgediv.style.setProperty('height',"24px")
    badgediv.appendChild(badge)
    return badgediv.outerHTML
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
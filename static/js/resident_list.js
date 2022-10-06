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

function operaFormatter(id,index){
    return [
        '<div class="px-3">',
        '    <a href="/resident/'+id+'" class="btn btn-primary mx-lg-1 my-lg-0 my-1" role="button">',
        '        <i class="fa-solid fa-list"></i> 查看详情',
        '    </a>',
        '    <button class="btn btn-danger my-lg-0 mx-lg-1 my-1" onclick="confirmDelete('+id+','+index+')" id="delete" data-bs-toggle="modal" data-bs-target="#myModal">',
        '        <i class="fa-solid fa-trash"></i> 删除',
        '    </button>',
        '</div>'
    ].join('')
}

function nameFooter(){
    return [
        '<div class="form-name needs-validation">',
        '    <input id="form-name-input" class="form-control" aria-describedby="namehelp" required>',
        '    <div id="namehelp" class="form-text">姓名</div>',
        '    <div class="invalid-feedback">',
        '    </div>',
        '</div>',
    ].join('')
}

function sexFooter(){
    return [
        '<div class="form-sex">',
        '    <select name="form-sex-input" id="form-sex-input" class="form-select" aria-describedby="sexhelp">',
        '        <option value="m">男</option>',
        '        <option value="f">女</option>',
        '    </select>',
        '    <div id="sexhelp" class="form-text">性别</div>',
        '    <div class="invalid-feedback">',
        '    </div>',
        '</div>'
    ].join('')
}

function IDnumFooter(){
    return [
        '<div class="form-idnumber">',
        '    <input type="text" id="form-idnumber-input" maxlength="18" class="form-control" aria-describedby="idnumberhelp" required>',
        '    <div id="idnumberhelp" class="form-text">身份证号</div>',
        '    <div class="invalid-feedback">',
        '    </div>',
        '</div>'
    ].join('')
}

function phoneFooter(){
    return [
        '<div class="form-phone">',
        '    <input type="number" id="form-phone-input" maxlength="11" class="form-control" aria-describedby="phonehelp">',
        '    <div id="phonehelp" class="form-text">手机号</div>',
        '    <div class="invalid-feedback">',
        '    </div>',
        '</div>'
    ].join('')
}

function isLocalFooter(){
    return [
        '<div class="form-isLocalResident form-check">',
        '    <input type="checkbox" id="form-islocal-input" class="form-check-input" aria-describedby="islocalhelp">',
        '    <label class="form-check-label" for="form-islocal-input">',
        '        是否常住',
        '    </label>',
        '    <div class="invalid-feedback">',
        '    </div>',
        '</div>'
    ].join('')
}

function outLocationFooter(){
    return [
        '<div class="form-outlocation">',
        '    <input id="form-outlocation-input" class="form-control" aria-describedby="outlocationhelp">',
        '    <div id="outlocationhelp" class="form-text">在外地点</div>',
        '    <div class="invalid-feedback">',
        '    </div>',
        '</div>',
    ].join('')
}

function houseFooter(){
    //比较难，做一个按分级检索房屋的菜单，太难就不做了
    return [
        '<div class="form-house">',
        '    <input class="form-control" list="houselist" id="form-house-input" placeholder="输入户号搜索..." aria-describedby="househelp">',
        '    <datalist id="houselist"></datalist>',
        '    <div id="househelp" class="form-text">户</div>',
        '    <div class="invalid-feedback">',
        '    </div>',
        '</div>'
    ].join('')
}

function noteFooter(){
    //常规的文本输入，可以为空
    return [
        '<div class="form-note">',
        '    <input id="form-note-input" class="form-control" aria-describedby="notehelp">',
        '    <div id="notehelp" class="form-text">备注</div>',
        '    <div class="invalid-feedback">',
        '    </div>',
        '</div>',
    ].join('')
}

function optionFooter(){
    //一个AJAX提交表单创建信息的按钮
    return [
        '<div class="form-submit px-3">',
        '    <button onclick="event.preventDefault()" class="btn btn-primary mx-1" id="form-submit">',
        '        <i class="fa-solid fa-plus"></i> 添加',
        '    </button>',
        '</div>'
    ].join('')
}

function confirmDelete(id,index){
    var datacol = $('tr[data-index='+ index +']');
    //console.log($('.name',datacol).text())
    $('.modal-title').text("确认")
    $('.modal-body').text("确定要删除 "+$('.name',datacol).text()+"("+$('.phone',datacol).text()+")"+" 吗？")
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
            url:'/api/residents/'+id+'/',
            type:'DELETE',
            headers:{
                "X-CSRFToken": CSRFtoken,
            },
            success:() => {
                $('#table').bootstrapTable('hideRow', {
                    index:index
                })
                $('#toast').removeClass('border-success text-success border-danger text-danger')
                    .addClass('border-success text-success')
                $('#toast .toast-body').text($('.name',datacol).text()+" 已删除")
                $('#toast').toast('show');
            },
            error:(error) => {
                //console.log(error)
                $('#toast').removeClass('border-success text-success border-danger text-danger')
                    .addClass('border-danger text-danger')
                $('#toast .toast-body').text($('.name',datacol).text()+" 删除失败："+error.responseJSON.message)
                $('#toast').toast('show');
            }
        })
    });
}

var name_data,
    sex_data = 'm',
    idnumber_data,
    phone_data = null,
    islocal_data = false,
    outlocation_data = '',
    house_data,
    note_data = '',
    global_index = 0

function resetGlobalparams(){
    globalThis.name_data = undefined
    globalThis.sex_data = 'm'
    globalThis.phone_data = null
    globalThis.islocal_data = false
    globalThis.outlocation_data = ''
    globalThis.house_data = undefined
    globalThis.note_data = ''
}

function optionListener(){
    $('#form-submit').on('click',function(){
        if(globalThis.name_data != undefined){
            if(globalThis.idnumber_data != undefined){
                var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
                var f_data = {};
                f_data['name'] = globalThis.name_data
                f_data['IDnumber'] = globalThis.idnumber_data
                f_data['sex'] = globalThis.sex_data
                f_data['phone'] = globalThis.phone_data
                f_data['isLocalResident'] = globalThis.islocal_data
                f_data['outLocation'] = globalThis.outlocation_data
                f_data['note'] = globalThis.note_data
                f_data['b_house'] = globalThis.house_data
                var i = globalThis.global_index
                $.ajax({
                    url:'/api/residents/',
                    type:'POST',
                    dataType:'json',
                    data: JSON.stringify(f_data),
                    contentType: 'application/json; charset=UTF-8',
                    headers:{
                        "X-CSRFToken": CSRFtoken,
                    },
                    success:(element) => {
                        resetGlobalparams()

                        var row = []
                        row.push({
                            'id':element.id,
                            'name':element.name,
                            'sex':element.sex_display,
                            'age':element.age,
                            'phone':element.phone,
                            'isLocalResident':get_bool(element.isLocalResident),
                            'outLocation':element.outLocation,
                            'b_house':element.house_name,
                            'note':element.note,
                            'option':operaFormatter(element.id,i)
                        })
                        $('#table').bootstrapTable('append',row)
                        $('#table').bootstrapTable('scrollTo', 'bottom')
                        $('#toast').removeClass('border-success text-success border-danger text-danger')
                            .addClass('border-success text-success')
                        $('#toast .toast-body').text(element.name +" 添加成功")
                        $('#toast').toast('show');
                    },
                    error:(error) => {
                        //console.log(error)
                        $('#toast').removeClass('border-success text-success border-danger text-danger')
                            .addClass('border-danger text-danger')
                        $('#toast .toast-body').text("添加失败："+error.responseJSON.message)
                        $('#toast').toast('show');
                    }
                })
            }else{
                $('#form-idnumber-input').trigger('blur')
            }
        }else{
            $('#form-name-input').trigger('blur')
        }
    })
}

function nameFooterListener(){
    $('#form-name-input').blur(function(){
        //console.log($(this).val())
        if($(this).val() == ''){
            $('.form-name .invalid-feedback').text("姓名不能为空")
            globalThis.name_data = undefined
            $(this).removeClass('is-invalid')
                .addClass('is-invalid')
        }else{
            $(this).removeClass('is-invalid')
            globalThis.name_data = $(this).val()
        }
        
    })
    $('#form-name-input').on('input',function(){
        $(this).removeClass('is-invalid')
    })
}

function sexFooterListener(){
    $('#form-sex-input').on('change',function(){
        globalThis.sex_data = $(this).val()
    })
}

function IDnumFooterListener(){
    $('#form-idnumber-input').blur(function(){
        var num = $(this).val()
        num = num.toUpperCase()
        if(!(/(^\d{15}$)|(^\d{17}([0-9]|X)$)/.test(num))){
            $('.form-idnumber .invalid-feedback').text("身份证号有误/不能为空")
            globalThis.idnumber_data = undefined
            $(this).removeClass('is-invalid')
                .addClass('is-invalid')
        }else{
            globalThis.idnumber_data = num
            $(this).removeClass('is-invalid')
        }
    })
}

function phoneListener(){
    $('#form-phone-input').blur(function(){
        if($(this).val != ''){
            globalThis.phone_data = $(this).val()
        }else{
            globalThis.phone_data = ''
        }
    })
}

function islocalListener(){
    $('#form-islocal-input').on('click',function(){
        if($(this).is(":checked")){
            globalThis.islocal_data = true
        }else{
            globalThis.islocal_data = false
        }
    })
}

function outlocationListener(){
    $('#form-outlocation-input').blur(function(){
        if($(this).val != ''){
            globalThis.outlocation_data = $(this).val()
        }else{
            globalThis.outlocation_data = ''
        }
    })
}

function houseListener(){
    $.ajax({
        url: '/api/houses/get_by_permission/',
        type:"GET",
        dataType:"json",
        success:(data) => {
            $('#houselist').empty()
            data.houses.forEach(element => {
                var option = document.createElement('option')
                option.setAttribute('value',element.id)
                option.text = element.house_name
                $('#houselist').append(option)
            })
        }
    })
    $('#form-house-input').blur(function(){
        if($(this).val() != ''){
            var id = $(this).val()
            $.ajax({
                url:'/api/houses/'+id+'/',
                type:'GET',
                success:(response) => {
                    $('#form-house-input').removeClass('is-invalid')
                    globalThis.house_data = response.id
                },
                error:(error) => {
                    $('.form-house .invalid-feedback').text("出现错误，请核对信息或稍后再试")
                    globalThis.house_data = undefined
                    $('#form-house-input').removeClass('is-invalid')
                        .addClass('is-invalid')
                }
            })
        }
    })
}

function noteFooterListener(){
    $('#form-note-input').blur(function(){
        if($(this).val != ''){
            globalThis.note_data = $(this).val()
        }else{
            globalThis.note_data = ''
        }
    })
}

function load_Form(){
    $('tfoot > tr > th.name').html(nameFooter())
    nameFooterListener()

    $('tfoot > tr > th.sex').html(sexFooter())
    sexFooterListener()

    $('tfoot > tr > th.age').html(IDnumFooter())
    IDnumFooterListener()

    $('tfoot > tr > th.phone').html(phoneFooter())
    phoneListener()

    $('tfoot > tr > th.isLocalResident').html(isLocalFooter())
    islocalListener()

    $('tfoot > tr > th.outLocation').html(outLocationFooter())
    outlocationListener()

    $('tfoot > tr > th.note').html(noteFooter())
    noteFooterListener()

    $('tfoot > tr > th.b_house').html(houseFooter())
    houseListener()

    $('tfoot > tr > th.option').html(optionFooter())
    optionListener()
}
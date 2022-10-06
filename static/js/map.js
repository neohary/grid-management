	/*function TestControl() {
		this.defaultAnchor = BMAP_ANCHOR_BOTTOM_RIGHT;
		this.defaultOffset = new BMapGL.Size(50,100);
	}
	TestControl.prototype = new BMapGL.Control();

	TestControl.prototype.initialize = function(map){
		var div = document.createElement('div');
		div.setAttribute('role','button');
		div.classList.add('btn','btn-primary','rounded-circle','roundbtn','d-flex','justify-content-center','shadow');
		var content = document.createElement('i');
		content.classList.add('fa-solid','fa-plus','fa-lg','align-self-center');
		div.appendChild(content);
		div.onclick = function(e) {
			console.log("HELLO WORLD");
		}
		map.getContainer().appendChild(div);
		return div;
	}
	var myTestCtrl = new TestControl();
	map.addControl(myTestCtrl);*/

function draw(mode){
    drawingManager.open();
    drawingManager.setDrawingMode(mode);
}

function drawcheck(bool){
    if (bool){
        map.disableDragging();
    }
    else{
        map.enableDragging();
    }
}

function getCenter(path){
    var x = 0, y = 0;
    for(var k = 0;k<path.length;k++){
        x = x + parseFloat(path[k].lng);
        y = y + parseFloat(path[k].lat);
    }
    x = x/path.length;
    y = y/path.length;
    return new BMapGL.Point(x,y)
}

function getPathArray(path){
    var result = {};
    var i = 0;
    path.forEach(element => {
        var point = [];
        point.push(element.lng,element.lat)
        result[i] = point;
        i++;
    });
    return result
}

function toolTip(object,context){
    object.setAttribute('data-bs-toggle','tooltip');
    object.setAttribute('data-bs-placement','top');
    object.setAttribute('data-bs-html','true');
    object.setAttribute('data-bs-title',context)
}

function DrawButtonsCtrl() {
    this.defaultAnchor = BMAP_ANCHOR_BOTTOM_RIGHT;
    this.defaultOffset = new BMapGL.Size(80,100);
}
DrawButtonsCtrl.prototype = new BMapGL.Control();
DrawButtonsCtrl.prototype.initialize = function(map){
    var div = document.createElement('div');
    div.classList.add('btn-group');
    div.setAttribute('role','group');
    var btn1 = document.createElement('button')
    var btn2 = document.createElement('button')
    btn1.classList.add('btn','btn-primary','btn-lg','shadow');
    var btn1_icon = document.createElement('i');
    btn1_icon.classList.add('fa-solid','fa-vector-square','fa-xl');
    btn1.appendChild(btn1_icon);
    toolTip(btn1,"绘制矩形 <br/> 使用矩形工具选出目标区域")
    
    btn2.classList.add('btn','btn-primary','btn-lg','shadow');
    var btn2_icon = document.createElement('i');
    btn2_icon.classList.add('fa-solid','fa-draw-polygon','fa-xl');
    btn2.appendChild(btn2_icon);
    toolTip(btn2,"绘制多边形 <br/> 使用多边形工具选出目标区域")

    div.appendChild(btn1);
    div.appendChild(btn2);
    btn1.onclick = function() {
        draw(BMAP_DRAWING_RECTANGLE);
        drawcheck(true);
    }
    btn2.onclick = function(){
        draw(BMAP_DRAWING_POLYGON);
        drawcheck(true);
    }
    map.getContainer().appendChild(div);
    return div;
}

function SearchBarCtrl() {
    this.defaultAnchor = BMAP_ANCHOR_TOP_LEFT;
    this.defaultOffset = new BMapGL.Size(10,10);
}

SearchBarCtrl.prototype = new BMapGL.Control();
SearchBarCtrl.prototype.initialize = function(map){
    var div = document.createElement('div');
    var html = [
        '<div class="input-group">',
        '    <input id="search" class="form-control shadow-sm" type="text" placeholder="搜索地点">',
        '    <button id="searchbtn" class="btn btn-primary" type="button" id="button-addon1"><i class="fa-solid fa-magnifying-glass"></i></button>',
        '</div>',
        '<div id="searchResultPanel" class="form-control" style="border:1px solid #C0C0C0;width:150px;height:auto; display:none;"></div>'
    ].join('')
    div.innerHTML = html
    map.getContainer().appendChild(div);
    return div;
}

function MapTypeCtrl() {
    this.defaultAnchor = BMAP_ANCHOR_TOP_RIGHT;
    this.defaultOffset = new BMapGL.Size(20,15);
}

MapTypeCtrl.prototype = new BMapGL.Control();
MapTypeCtrl.prototype.initialize = function(map){
    var div = document.createElement('div');
    var html = [
        '<div>',
        '    <button id="switchType" onclick="switchMapType()" class="btn btn-primary btn-lg shadow-sm">',
        '        <i class="fa-solid fa-map"></i>',
        '    </button>',
        '</div>'
    ].join('')
    div.innerHTML = html
    map.getContainer().appendChild(div);
    return div;
}

var switchType = false
function switchMapType() {
    switchType = !switchType
    //console.log(switchType)
    if(switchType){
        //道路图
        map.setMapType(BMAP_NORMAL_MAP)
        $('#switchType').empty()
        $('#switchType').append(['<i class="fa-regular fa-map"></i>'].join(''))
    }else{
        //卫星图
        map.setMapType(BMAP_SATELLITE_MAP)
        $('#switchType').empty()
        $('#switchType').append(['<i class="fa-solid fa-map"></i>'].join(''))
    }
}

function searchBarListener() {
    var ac = new BMapGL.Autocomplete({
        "input":'search',
        "location":map
    })
    ac.addEventListener("onhighlight", function(e) { //鼠标放在下拉列表上的事件
        var str = "";
        var _value = e.fromitem.value;
        var value = "";
        if(e.fromitem.index > -1) {
            value = _value.province + _value.city + _value.district + _value.street + _value.business;
        }
        str = "FromItem<br />index = " + e.fromitem.index + "<br />value = " + value;
        value = "";
        if(e.toitem.index > -1) {
            _value = e.toitem.value;
            value = _value.province + _value.city + _value.district + _value.street + _value.business;
        }
        str += "<br />ToItem<br />index = " + e.toitem.index + "<br />value = " + value;
        $('#searchResultPanel').html(str)
    });
    var marker,local;
    function infowindowFormatter() {
        return [
            '<div class="p-2 c-village-form">',
            '    <div class="mb-3 needs-validation">',
            '        <label for="locname" class="form-label">名称</label>',
            '        <input type="text" class="form-control" id="locname">',
            '        <div class="invalid-feedback"></div>',
            '    </div>',
            '     <div class="mb-3 row">',
            '         <div class="col-12">',
            '             <label for="" class="form-label">坐标</label>',
            '             <input type="text" class="form-control" id="locX" readonly>',
            '             <input type="text" class="form-control" id="locY" readonly>',
            '         </div>',
            '     </div>',
            '    <div class="mb-3 d-grid">',
            '        <button class="btn btn-success" onclick="createVillage()" id="createvillage">创建村庄</button>',
            '    </div>',
            '</div>'
        ].join('')
    }
    function infowindowUpdater(){
        $('#locname').val($('#search').val())
        $('#locX').val(marker.getPosition().lng.toFixed(6))
        $('#locY').val(marker.getPosition().lat.toFixed(6))
    }
    function myFun() {
        var pp = local.getResults().getPoi(0).point; //获取第一个智能搜索的结果
        map.centerAndZoom(pp, 15);
        marker = new BMapGL.Marker(pp)
        marker.enableDragging()
        var infowindow = new BMapGL.InfoWindow(infowindowFormatter())
        marker.addEventListener('click',function(){
            this.openInfoWindow(infowindow)
            infowindowUpdater()
        })
        marker.addEventListener("dragend", function (e) {
            infowindowUpdater()
        });
        map.addOverlay(marker); //添加标注
    }
    function setPlace(text) {
        map.removeOverlay(marker);
        local = new BMapGL.LocalSearch(map, { //智能搜索
            onSearchComplete: myFun
        });
        local.search(text);
    }
    $('#searchbtn').on('click',function(){
        console.log($(this).val())
        setPlace($('#search').val())
    })
}

function createVillage(){
    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
    var P_data = {}
    if($('#locname').val() != '' && $('#locX').val() != '' && $('#locY').val() != ''){
        $('.c-village-form .needs-validation').removeClass('is-invalid')
        P_data['name'] = $('#locname').val()
        P_data['locationX'] = $('#locX').val()
        P_data['locationY'] = $('#locY').val()
        $.ajax({
            url:'/api/village/',
            type:'POST',
            dataType:'json',
            data: JSON.stringify(P_data),
            contentType: 'application/json; charset=UTF-8',
            headers:{
                "X-CSRFToken": CSRFtoken,
            },
            success:() => {
                window.location.replace("/village/create-complete");
            },
            error:(error) => {
                console.log(error)
                $('.c-village-form .invalid-feedback').text('出现错误：'+error.responseJSON)
                $('#locname').removeClass('is-invalid')
                    .addClass('is-invalid')
            }
        })
    }else{
        $('.c-village-form .invalid-feedback').text('名称/坐标不能为空')
        $('#locname').removeClass('is-invalid')
            .addClass('is-invalid')
    }
}

var styleOptions = {
    strokeColor: '#5E87DB', // 边线颜色。
    fillColor: '#5E87DB', // 填充颜色。当参数为空时，圆形将没有填充效果。
    strokeWeight: 2, // 边线的宽度，以像素为单位。
    strokeOpacity: 1, // 边线透明度，取值范围0 - 1。
    fillOpacity: 0.2 // 填充的透明度，取值范围0 - 1。
};

var loadStyleOptions = {
    //strokeColor: '#19bf24', // 边线颜色。
    //fillColor: '#10de6c', // 填充颜色。当参数为空时，圆形将没有填充效果。
    strokeWeight: 2, // 边线的宽度，以像素为单位。
    strokeOpacity: 1, // 边线透明度，取值范围0 - 1。
    fillOpacity: 0.2 // 填充的透明度，取值范围0 - 1。
};

var labelOptions = {
    borderRadius: '2px',
    background: '#FFFBCC',
    border: '1px solid #E1E1E1',
    color: '#703A04',
    fontSize: '12px',
    letterSpacing: '0',
    padding: '5px'
};

function overlay_mouseover(obj){
    obj.setStrokeColor('red');
    obj.setFillColor('#000');
};

function overlay_mouseout(obj){
    obj.setStrokeColor('#5E87DB');
    //obj.setFillColor('#5E87DB');
};
function load_overlay_mouseout(obj,color){
    obj.setStrokeColor(color);
    obj.setFillColor('#fff');
};

function overlay_formbox(obj,html,submitVerbose){
    var container = document.getElementById('formbox')
    map.centerAndZoom(getCenter(obj.getPath()),20);
    container.style.display = 'block';
    //console.log(document.getElementById('test'));
    if(document.getElementById('formdiv')){
        document.getElementById('formdiv').remove();
    }
    var formdiv = document.createElement('div');
    formdiv.appendChild(html);
    formdiv.id = 'formdiv'
    $('#formbody').append(formdiv);
    $('#submit').val(submitVerbose)
};

var labelStyle = {
    color: 'blue',
    borderRadius: '0.25rem',
    borderColor: '#ccc',
    padding: '5px',
    fontSize: '16px',
    opacity: 0.8
}

var loadLabelStyle = {
    //color: '#19bf24',
    borderRadius: '0.25rem',
    borderColor: '#ccc',
    padding: '5px',
    fontSize: '16px',
    opacity: 0.8
}
function overlay_addLabel(obj,text,offsetX,offsetY,style){
    var opts = {
        position: getCenter(obj.getPath()), // 指定文本标注所在的地理位置
        offset: new BMapGL.Size(offsetX, offsetY) // 设置文本偏移量
    };
    var label = new BMapGL.Label(text,opts)
    label.setStyle(style);
    map.addOverlay(label);
    return label;
};

function house_CreateForm(housedata){
    if(!housedata){
        $('#updatefields').hide();
        $('#editGeo').hide();
    }else{
        $('#updatefields').show();
        $('#editGeo').show();
    }
    $.get('/api/village/get_by_permission/',function(data){
        //console.log(data.villages);
        $('#village').empty();
        if(data.villages.length > 1){
            $('#village').prop('disabled',false);
            for (let i = 0; i < data.villages.length; i++) {
                var opt = document.createElement('option');
                opt.setAttribute('value',data.villages[i].id);
                opt.text = data.villages[i].name;
                if(i == 0){
                    $('#village').val(opt.value);
                };
                $('#village').append(opt);
            }
        }else if(data.villages.length == 1){
            var opt = document.createElement('option');
            opt.setAttribute('value',data.villages[0].id);
            opt.text = data.villages[0].name;
            $('#village').append(opt);
            $('#village').prop('disabled',true);
            $('#village').val(opt.value);
        };
        $('#house_mgrid_id').val('');
        if(housedata){
            $('#village').val(housedata['village'])
            $('#house_mgrid_id').val(housedata['mgridID'])
            $('#population').val(housedata['pop_count'])
            $('#holder').val(housedata['holder_name'])
        };
        $('#village').trigger('change');
    });
};

var mgrid_changeselect = ''

function house_UpdateForm(data){
    house_CreateForm(data)
    //changeSelected()
    mgrid_changeselect = data['mgrid']
}

function getResident(id){
    if(id){
        var result = $.get('/api/residents/'+id+'/',function(data){
            return data
        });
        if(result){
            return result['responseJSON']
        }
    }else{
        return ''
    }
}

function house_ClearFormData(){
    $('#village').empty();
    $('#village').val("");
    $('#mgrid').empty();
    $('#mgrid').val("");
    $('#updatefields').hide();
    $('#editGeo').hide();
    $('#delete').off();
    $('#editGeo').off();
    $('#c-delete').remove();
    $('#submit').off();
}

function getGeoPoints(geo){
    var points = []
    for (let i = 0; i < Object.keys(geo).length; i++) {
        const element = geo[i];
        var point = new BMapGL.Point(element[0],element[1])
        points.push(point)
    }
    return points
};

// 绘制多边形区域
function drawChart(points,color) {
    if (!points || points.length === 0) return;
    let ps = points.map(p => new BMapGL.Point(p.lng, p.lat));
    var colors = {
        strokeColor: color, // 边线颜色。
        //fillColor: '#10de6c', // 填充颜色。当参数为空时，圆形将没有填充效果。
    }
    var f_loadStyleOptions = Object.assign(loadStyleOptions,colors)
    let polygon = new BMapGL.Polygon(ps, f_loadStyleOptions);
    map.addOverlay(polygon); // 把图形绘制在地图上
    return polygon;
};

function abandonOverlay(polygon,label){
    map.removeOverlay(polygon);
    map.removeOverlay(label);
    document.getElementById('formbox').style.display = 'none';
    house_ClearFormData();
};

var isEditing = false;

function loadNewOverlay(data){
    var overlay = drawChart(getGeoPoints(data.geo),data.mgrid_color);
    var color = {
        color: data.mgrid_color
    }
    var f_loadLabelStyle = Object.assign(loadLabelStyle,color)
    var label = overlay_addLabel(overlay,data.short_name,-20,0,f_loadLabelStyle);

    overlay.addEventListener('mouseover',function(){
        if(!isEditing){
            overlay_mouseover(this);
        };
    })
    overlay.addEventListener('mouseout',function(){
        if(!isEditing){
            load_overlay_mouseout(this,data.mgrid_color);
        };
    })
    
    overlay.addEventListener('click',function(){
        //console.log(data)
        if(!isEditing){
            $('#title').text(data.house_name);
            house_UpdateForm(data);
            var test = document.createElement('div');
            overlay_formbox(this,test,"更新");
            $('#delete').on('click',function(){
                $('.modal-title').text("确认")
                $('.modal-body').html("确定要删除 "+data.id+" 吗？<br/> 属于该户的居民信息也会一并删除。")
                var confirm = document.createElement('button')
                confirm.id = 'c-delete'
                confirm.classList.add('btn','btn-danger')
                confirm.innerText = "确定"
                confirm.setAttribute('data-bs-dismiss','modal')
                $('#c-delete').remove();
                $('.modal-footer').append(confirm);
                $('#c-delete').on('click',function(){
                    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
                    $.ajax({
                        url:'/api/houses/'+data.id+'/',
                        type:'DELETE',
                        headers:{
                            "X-CSRFToken": CSRFtoken,
                        },
                        success:(response) => {
                            abandonOverlay(overlay,label)
                            console.log(response)
                        },
                        error:(error) => {
                            console.log(error);
                        }
                    })
                });
            });
            $('#submit').on('click',function(e){
                e.preventDefault();
                var P_data = {};
                var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
                var mgridID = $('#house_mgrid_id').val();
                P_data['village'] = $('#village').val()
                P_data['mgrid'] = $('#mgrid').val();
                if(mgridID){
                    P_data['mgridID'] = mgridID;
                }else{
                    P_data['mgridID'] = null;
                };
                //console.log(JSON.stringify(P_data))
                $.ajax({
                    url:'/api/houses/'+data.id+'/',
                    type:'PUT',
                    dataType:'json',
                    data: JSON.stringify(P_data),
                    contentType: 'application/json; charset=UTF-8',
                    headers:{
                        "X-CSRFToken": CSRFtoken,
                    },
                    success:(data) => {
                        abandonOverlay(overlay,label);
                        loadNewOverlay(data);
                    },
                    error:(error) => {
                        console.log(error);
                    }
                });
            });
            
            $('#editGeo').on('click',function(){
                if(!isEditing){
                    overlay.enableEditing();
                    isEditing = true;
                    $(this).text("完成编辑")
                }else{
                    overlay.disableEditing();
                    isEditing = false;
                    $(this).text("编辑形状")
    
                    var P_data = {};
                    var CSRFtoken = $('input[name=csrfmiddlewaretoken]').val();
                    P_data['mgrid'] = $('#mgrid').val();
                    P_data['village'] = $('#village').val()
                    P_data['geo'] = getPathArray(overlay.getPath())
                    $.ajax({
                        url:'/api/houses/'+data.id+'/',
                        type:'PUT',
                        dataType:'json',
                        data: JSON.stringify(P_data),
                        contentType: 'application/json; charset=UTF-8',
                        headers:{
                            "X-CSRFToken": CSRFtoken,
                        },
                        success:(data) => {
                            console.log("success");
                            P_data = {};
                        },
                        error:(error) => {
                            console.log(error)
                        }
                    });
                };
            });
            $('#membersManager').off()
            $('#membersManager').on('click',function(){
                //console.log(data)
                window.location.href = "/house/"+data.id;
            })
        };
    });
    return overlay;
}
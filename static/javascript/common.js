var i=0;

function copy(){
        var div = document.getElementById ("ACT_MEMBERS_NAME"+i);
        i++;
        div.setAttribute('onFocus', "");

        var whole_form = document.getElementById("sending_form");
        var new_div = document.createElement('div');
        var new_formgroup = document.createElement('div');
        var new_div_STD_INPUT1 = document.createElement('div');
        var new_div_STD_INPUT2 = document.createElement('div');
        var new_div_STD_INPUT3 = document.createElement('div');
        var new_div_STD_INPUT4 = document.createElement('div');

        var new_name = document.createElement('input');
        var new_num = document.createElement('input');
        var new_is_on = document.createElement('checkbox');
        var new_etc = document.createElement('input');
        //new_div.innerHTML = "my <b>new</b> skill - <large>DOM maniuplation!</large>";
        new_div.setAttribute('class', 'acting_members');
        new_div.setAttribute('id', 'form'+i);
        new_formgroup.setAttribute('class', 'form-group');
        new_div_STD_INPUT1.setAttribute('class', 'STD_INPUT')
        new_div_STD_INPUT2.setAttribute('class', 'STD_INPUT')
        new_div_STD_INPUT3.setAttribute('class', 'STD_INPUT')
        new_div_STD_INPUT4.setAttribute('class', 'STD_INPUT')

        new_name.setAttribute('class', 'form-control');
        new_name.setAttribute('id', 'ACT_MEMBERS_NAME'+i);
        new_name.setAttribute('name', 'MEMBERS_NAME'+i);
        new_name.setAttribute('placeholder', '이름');
        new_name.setAttribute('type', 'text');
        new_name.setAttribute('onFocus', 'copy();');
        
        new_num.setAttribute('class', 'form-control');
        new_num.setAttribute('id', 'ACT_MEMBERS_NUM'+i);
        new_num.setAttribute('name', 'MEMBERS_NUM'+i);
        new_num.setAttribute('placeholder', '학번');

        new_is_on.innerHTML="<label><input type='checkbox' name='IS_ON"+i+"'>참석 여부</label>"
        
        new_etc.setAttribute('class', 'form-control');
        new_etc.setAttribute('id', 'ACT_MEMBERS_ETC'+i);
        new_etc.setAttribute('name', 'MEMBERS_ETC'+i);
        new_etc.setAttribute('placeholder', '비고');

        //document.body.appendChild(div);
        new_div_STD_INPUT1.appendChild(new_name);
        new_div_STD_INPUT2.appendChild(new_num);
        new_div_STD_INPUT3.appendChild(new_is_on);
        new_div_STD_INPUT4.appendChild(new_etc);
        new_formgroup.appendChild(new_div_STD_INPUT1);
        new_formgroup.appendChild(new_div_STD_INPUT2);
        new_formgroup.appendChild(new_div_STD_INPUT3);
        new_formgroup.appendChild(new_div_STD_INPUT4);
        new_div.appendChild(new_formgroup);
        whole_form.appendChild(new_div);
        //document.body.appendChild(new_div);

        return;
}

function make_new_form() {
    var test = document.getElementById('acting_members');
    var test1 = test.cloneNode();
    body.appendChild(test1);
}
# -*- coding:utf-8 -*-
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import flask
import os, shutil, datetime
import random
import sys
import zipfile
from shutil import make_archive
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

UPLOAD_FOLDER = './image'
DOCX_FOLDER = './temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOCX_FOLDER'] = DOCX_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/make/', methods=['GET','POST'])
def assemble():
    if request.method=='POST':
        id_king = request.form['KING']
        id_wrt_date = request.form['WRT_DATE']
        id_club_name = request.form['CLUB_NAME']
        id_act_date = request.form['ACT_DATE']
        id_place = request.form['PLACE']
        id_act_conts = request.form['ACTIVITY_CONTENTS']
        check_type = request.form['CHECK_TYPE']
        image1 = request.files['ACT_PIC']
        image2 = request.files['TOGETHER_PIC']
        filename_img1 = image1.filename
        filename_img2 = image2.filename
        image1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_img1))
        image2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_img2))

#GET_MEMBER
        act_member=[]
        for n in range(0, 33):
            index_value_0 = request.form.getlist('MEMBERS_NAME'+str(n))
            if index_value_0:
                act_member.append(request.form['MEMBERS_NAME'+str(n)])
            else:
                act_member.append(' ')


        act_num=[]
        for n in range(0, 33):
            index_value_1 = request.form.getlist('MEMBERS_NUM'+str(n))
            if index_value_1:
                act_num.append(request.form['MEMBERS_NUM'+str(n)])
            else:
                act_num.append(' ')

        act_is_on=[]
        check_stu_num=0
        for n in range(0, 33):
            index_value_2 = request.form.getlist('IS_ON'+str(n))
            print index_value_2
            if index_value_2:
                act_is_on.append('O')
                check_stu_num=check_stu_num+1
                #act_is_on.append(request.form['IS_ON'+str(n)])
            else:
                act_is_on.append('X')
                

        act_etc=[]
        for n in range(0, 33):
            index_value_3 = request.form.getlist('MEMBERS_ETC'+str(n))
            if index_value_3:
                act_etc.append(request.form['MEMBERS_ETC'+str(n)])
            else:
                act_etc.append(' ')



#COPYING
        i=0
        today=datetime.date.today()
        folders=[['form','temp/form_']]
        while 1:
            flag=1
            for b in os.listdir('./temp'):
                if (b).find(today.strftime("%Y%m%d_"+str(i))) is not -1 :
                    i=i+1
                    flag=0
                    break
            if flag is 1:
                break
        toady_date = today.strftime("%Y%m%d_"+str(i))
        for src, dst in folders:
            shutil.copytree(src,dst+toady_date)
        
#MODIFYING
        wordFile = open('temp/form_'+toady_date+'/word/document.xml', 'r')
        print wordFile
        line = wordFile.read()

        t1 = line.replace('$KING$', id_king).replace('$WRT_DATE$', id_wrt_date).replace('$CLUB_NAME$', id_club_name)
        t2 = t1.replace('$ACT_DATE$', id_act_date).replace('$PLACE$', id_place).replace('$ACTIVITY_CONTENTS$', id_act_conts)
        
        total_num=0
        for m in range(0, 33):
            word_name = act_member[m]
            word_num = act_num[m]
            word_is_on = act_is_on[m]
            word_etc = act_etc[m]
            
            if word_name == ' ' or word_name == '':
                for n in range(m, 33):
                    t2 = t2.replace('$no'+str(n+1)+'$', ' ')
                    t2 = t2.replace('$name'+str(n+1)+'$', ' ')
                    t2 = t2.replace('$stu_num'+str(n+1)+'$', ' ')
                    t2 = t2.replace('$is_on'+str(n+1)+'$', ' ')
                    t2 = t2.replace('$etc'+str(n+1)+'$', ' ')
                break
            total_num=total_num+1
            t2 = t2.replace('$no'+str(m+1)+'$', str(m+1))
            t2 = t2.replace('$name'+str(m+1)+'$', word_name)
            t2 = t2.replace('$stu_num'+str(m+1)+'$', word_num)
            t2 = t2.replace('$is_on'+str(m+1)+'$', word_is_on)
            t2 = t2.replace('$etc'+str(m+1)+'$', word_etc)

        t2 = t2.replace('$TYPE$', str(check_type))

        wordFile.close()
        writeFile = open('temp/form_'+toady_date+'/word/document.xml', 'w')
        writeFile.write(t2)
        writeFile.close()
#PUT_IMAGE
        os.unlink('temp/form_'+toady_date+'/word/media/image1.jpeg')
        os.rename('image/'+filename_img1, 'temp/form_'+toady_date+'/word/media/image1.jpeg')
        os.unlink('temp/form_'+toady_date+'/word/media/image2.jpeg')
        os.rename('image/'+filename_img2, 'temp/form_'+toady_date+'/word/media/image2.jpeg')

#ZIP FILE
        shutil.make_archive("temp/form_"+toady_date, "zip", "temp/form_"+toady_date)
        os.rename("temp/form_"+toady_date+".zip", "temp/form_"+toady_date+".docx")
        
#RETURN
        return render_template('check.html', KING=id_king, WRT_DATE=id_wrt_date,
            CLUB_NAME=id_club_name, ACT_DATE=id_act_date, PLACE=id_place,
             ACTIVITY_CONTENTS=id_act_conts, FILE_NAME='form_'+toady_date+'.docx')


@app.route('/temp/<filename>')
def download(filename):
    return send_from_directory(app.config['DOCX_FOLDER'], filename)

if __name__ == '__main__':
    app.debug=True
    app.run()
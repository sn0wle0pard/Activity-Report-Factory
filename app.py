# -*- coding:utf-8 -*-
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import flask
import os, shutil, datetime
import random
import sys
import zipfile
import base64
from shutil import make_archive
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

UPLOAD_FOLDER = './image'
DOCX_FOLDER = './temp'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOCX_FOLDER'] = DOCX_FOLDER

def find_week(Y, M, D):
    #Y = id_act_date_Y
    Y = int(Y)
    M = int(M)
    D = int(D)
    total_day=0
    total_day = Y * 365 + Y/4 - Y/100 + Y/400

    #M = id_act_date_M-1
    M = M - 1
    while M is not 0:
        if M is 1:
            total_day += 31
        if M is 2:
            total_day += 28
        if M is 3:
            total_day += 31
        if M is 4:
            total_day += 30
        if M is 5:
            total_day += 31
        if M is 6:
            total_day += 30
        if M is 7:
            total_day += 31
        if M is 8:
            total_day += 31
        if M is 9:
            total_day += 30
        if M is 10:
            total_day += 31
        if M is 11:
            total_day += 30
        if M is 12:
            total_day += 31
        M -= 1

    #D = id_act_date_D
    total_day += D

    week_day = (total_day % 7) - 1
    if week_day is 0:
        week_day_char = "일"
    if week_day is 1:
        week_day_char = "월"
    if week_day is 2:
        week_day_char = "화"
    if week_day is 3:
        week_day_char = "수"
    if week_day is 4:
        week_day_char = "목"
    if week_day is 5:
        week_day_char = "금"
    if week_day is 6:
        week_day_char = "토"

    return week_day_char.encode('utf-8')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/make/', methods=['GET','POST'])
def assemble():
    if request.method=='POST':
        id_king = request.form['KING']
        id_wrt_date = request.form['WRT_DATE']
        id_club_name = request.form['CLUB_NAME']
        
#MAKE DATE
        id_act_date_Y = request.form['ACT_DATE_Y']
        id_act_date_M = request.form['ACT_DATE_M']
        id_act_date_D = request.form['ACT_DATE_D']
        id_act_date = id_act_date_Y + "." + id_act_date_M + "." + id_act_date_D

#FIND WEEK
#0000-1-1 IS MON(1)
        week_day_char = find_week(id_act_date_Y, id_act_date_M, id_act_date_D)

#CHECK TIME
        is_apm = request.form.get('TIME_APM')
        start_time_h = request.form.get('START_TIME_H')
        start_time_m = request.form.get('START_TIME_M')
        end_time_h = request.form.get('END_TIME_H')
        end_time_m = request.form.get('END_TIME_M')

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
        act_day = id_act_date
        i=1
        today=datetime.date.today()
        folders=[['form','temp/']]
        while 1:
            flag=1
            directory_name = id_act_date + "(" + week_day_char.decode('utf-8') + ")" + "-" + str(i)
            print directory_name
            directory_name_find = (directory_name).encode('utf-8')
            print directory_name_find
            for b in os.listdir('./temp'):
                if (b).find(directory_name_find) is not -1 :
                    i=i+1
                    flag=0
                    break
            if flag is 1:
                break
        today_date = id_act_date+str(i)
        for src, dst in folders:
            shutil.copytree(src,dst+directory_name)
        
#MODIFYING
        print week_day_char
        directory_name = id_act_date+"(" + week_day_char + ")"+"-"+str(i)
        wordFile = open('temp/'+directory_name+'/word/document.xml', 'r')
        print wordFile
        line = wordFile.read()
        write_date = id_act_date +"(" + week_day_char + ")" + " " + is_apm + " " 
        write_date += start_time_h + ":" + start_time_m + "~" + end_time_h + ":" + end_time_m

        t1 = line.replace('$KING$', id_king).replace('$WRT_DATE$', id_wrt_date).replace('$CLUB_NAME$', id_club_name)
        t2 = t1.replace('$ACT_DATE$', write_date).replace('$PLACE$', id_place).replace('$ACTIVITY_CONTENTS$', id_act_conts)
        
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
        writeFile = open('temp/'+directory_name+'/word/document.xml', 'w')
        writeFile.write(t2)
        writeFile.close()
#PUT_IMAGE
        os.unlink('temp/'+directory_name+'/word/media/image1.jpeg')
        os.rename('image/'+filename_img1, 'temp/'+directory_name+'/word/media/image1.jpeg')
        os.unlink('temp/'+directory_name+'/word/media/image2.jpeg')
        os.rename('image/'+filename_img2, 'temp/'+directory_name+'/word/media/image2.jpeg')

#RETURN
        return render_template('draw.html', PIC_NAME='../temp/'+directory_name+'/word/media/image2.jpeg', TODAY=directory_name)
        #return render_template('check.html', KING=id_king, WRT_DATE=id_wrt_date,
        #    CLUB_NAME=id_club_name, ACT_DATE=id_act_date, PLACE=id_place,
        #     ACTIVITY_CONTENTS=id_act_conts, FILE_NAME=''+directory_name+'.docx')


@app.route('/complete/', methods=['GET','POST'])
def complete():
    if request.method=='POST':
        directory_name = request.form['today_date']
        image_file = request.form['hidden_file']
        file = open("./image/image2.jpeg", 'wb')
        target_decode = image_file.split(",")[1]
        file.write(base64.b64decode(target_decode))

        file.close()
        image_name="image2.jpeg"
        os.unlink('temp/'+directory_name+'/word/media/image2.jpeg')
        os.rename('image/'+image_name, 'temp/'+directory_name+'/word/media/image2.jpeg')

    #ZIP FILE
        shutil.make_archive("temp/"+directory_name, "zip", "temp/"+directory_name)
        os.rename("temp/"+directory_name+".zip", "temp/"+directory_name+".docx")

        return render_template('complete.html', FILE_NAME=''+directory_name+'.docx')


@app.route('/temp/<date>/word/media/<filename>')
def download2(date, filename):
    IMG_FOLDER = './temp/'+date+'/word/media/'
    app.config['IMG_FOLDER'] = IMG_FOLDER
    return send_from_directory(app.config['IMG_FOLDER'], filename)


@app.route('/temp/<filename>')
def download(filename):
    return send_from_directory(app.config['DOCX_FOLDER'], filename)

if __name__ == '__main__':
    app.debug=True
    app.run()
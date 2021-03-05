# -*- coding: utf-8 -*-
import pywinauto
from pywinauto.keyboard import SendKeys
from pywinauto.controls.win32_controls import ComboBoxWrapper, ButtonWrapper, EditWrapper
from pywinauto.timings import TimeoutError
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.controls.menuwrapper import Menu
from pywinauto.application import Application, WindowSpecification
from pywinauto import Desktop
from subprocess import Popen
import time
import sys
import os
import shutil
import queue
import threading
from threading import Thread
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, wait, as_completed,ProcessPoolExecutor
import warnings
#import PyPDF2
import fitz



def createDir(mondir):

    inputdir = os.path.join(mondir, "Input")
    outputdir=os.path.join(mondir,"Output")
    bakdir=os.path.join(mondir,"Backup")
    faildir=os.path.join(mondir,"Fail")
    wipdir=os.path.join(mondir,"WIP")

    in_excel_dir=os.path.join(inputdir,"excel")
    in_word_dir=os.path.join(inputdir,"word")
    wip_excel_dir=os.path.join(wipdir,"excel")
    wip_word_dir=os.path.join(wipdir,"word")
    out_excel_dir=os.path.join(outputdir,"excel")
    out_word_dir=os.path.join(outputdir,"word")
    bak_excel_dir=os.path.join(bakdir,"excel")
    bak_word_dir=os.path.join(bakdir,"word")
    fail_excel_dir=os.path.join(faildir,"excel")
    fail_word_dir=os.path.join(faildir,"word")


    """
    if os.path.exists(mondir) == False:
        os.mkdir(mondir)
        print("폴더생성:" + mondir)
    """
    
    if os.path.exists(in_excel_dir) == False:
        os.makedirs(in_excel_dir)
        print("폴더생성:" + in_excel_dir)

    if os.path.exists(in_word_dir) == False:
        os.makedirs(in_word_dir)
        print("폴더생성:" + in_word_dir)

    if os.path.exists(wip_excel_dir) == False:
        os.makedirs(wip_excel_dir)
        print("폴더생성:" + wip_excel_dir)

    if os.path.exists(wip_word_dir) == False:
        os.makedirs(wip_word_dir)
        print("폴더생성:" + wip_word_dir)

    if os.path.exists(out_excel_dir) == False:
        os.makedirs(out_excel_dir)
        print("폴더생성:" + out_excel_dir)

    if os.path.exists(out_word_dir) == False:
        os.makedirs(out_word_dir)
        print("폴더생성:" + out_word_dir)

    if os.path.exists(bak_excel_dir) == False:
        os.makedirs(bak_excel_dir)
        print("폴더생성:" + bak_excel_dir)

    if os.path.exists(bak_word_dir) == False:
        os.makedirs(bak_word_dir)
        print("폴더생성:" + bak_word_dir)

    if os.path.exists(fail_excel_dir) == False:
        os.makedirs(fail_excel_dir)
        print("폴더생성:" + fail_excel_dir)

    if os.path.exists(fail_word_dir) == False:
        os.makedirs(fail_word_dir)
        print("폴더생성:" + fail_word_dir)



def monitoring(mondir):

    wipdir=os.path.join(mondir,"WIP")
    indir=os.path.join(mondir,"Input")
    cnt=0
    q=queue.Queue()
    for (path, dir, files) in os.walk(indir):

        if indir==path:  #자기자신 path는 제외
            continue

        for filename in files:
            
            ext = os.path.splitext(filename)[-1]
            if ext.lower() == '.pdf':

                input_full_path = os.path.join(path, filename)
                convert_type = os.path.basename(os.path.split(input_full_path)[0])
                wip_full_path = os.path.join(wipdir,convert_type,filename)

                if os.path.exists(wip_full_path) ==True:
                    os.remove(wip_full_path)

                while(True):
                    try:
                        shutil.move(input_full_path, wip_full_path)
                        if cnt==0:
                            print()
                        print("[+] Enqueue - {0}".format(input_full_path))
                        break
                    except PermissionError as e:
                        print("[!] PermissionError - 다른 프로세스가 파일을 사용 중...")
                        time.sleep(5)

                q.put((wip_full_path,convert_type))
                cnt=cnt+1





    return q


def convertingPdf(srcpath,filetype):

    result="정상"
    outputdir=os.path.join(mondir,"Output")
    bakdir=os.path.join(mondir,"Backup")
    faildir=os.path.join(mondir,"Fail")

    bak_full_path=os.path.join(bakdir,filetype,os.path.basename(srcpath))
    fail_full_path=os.path.join(faildir,filetype,os.path.basename(srcpath))

    doc = fitz.Document(srcpath)

    if os.path.exists(fail_full_path):
        os.remove(fail_full_path)
    if os.path.exists(bak_full_path):
        os.remove(bak_full_path)

    if doc.openErrCode > 0:  # 파일 open에 실패한 경우(확인필요)
        doc.close()
        shutil.move(srcpath,fail_full_path)
        shutil.copy(fail_full_path,bak_full_path)
        print("[!] Protection(Server: openErr) - {0}".format(srcpath))
        return
    else:  # 파일 open은 성공한 경우

        if doc.isEncrypted == 1:  # open 암호화 설정이 되어 있는경우, 암호화 정보(meta)를 볼 수 없음
            doc.close()
            shutil.move(srcpath, fail_full_path)
            shutil.copy(fail_full_path, bak_full_path)
            print("[!] Protection(Server: isEncrypted) - {0}".format(srcpath))
            return
        elif doc.metadata['encryption'] is not None:  # copy 등 기타 암호화 설정이 되어 있는 경우, 암호화 정보(meta)를 가져온다.
            doc.close()
            shutil.move(srcpath, fail_full_path)
            shutil.copy(fail_full_path, bak_full_path)
            print("[!] Protection(Server: copy or extract encryption) - {0}".format(srcpath))
            return

    doc.close()




    warnings.simplefilter("ignore")

    app = Application(backend='win32').start(r'C:\Program Files (x86)\ABBYY FineReader 14\FineReader.exe "{0}"'.format(srcpath),timeout=6000)


    top = app.window(title_re='‎.*- ABBYY FineReader 14')


    try:

        top.wait("visible ready", timeout=6000)

        preword= ":".join([word for word in top.class_name().split(":")[0:2]])
        ############## dlgNew 제거
        #print(top.print_control_identifiers(depth=2))
        #dlgNew = app.window(class_name_re=preword + ":.*?:10003:.*?:0:0")
        #print(dlgNew.class_name())

        ##dlgNew = top.find(class_name_re=preword + ":0:10003:.*?:0:0")
        ##dlgNew = top.child_window(class_name_re=preword + ":0:10003:.*?:0:0")
        #print(dlgNew.class_name())

        #dlgNew = top.child_window(class_name=preword+":0:10003:6:0:0")

        ##dlgNew.wait("visible ready", timeout=6000)

    except ElementNotFoundError as e:
        print("★에러시작")
        print(app.windows())
        print(top.print_control_identifiers(depth=2))
        print(e)
        print('★☆★☆★☆★☆★☆★☆★☆')
        print(srcpath)
        print(preword)
        with open(os.path.join(mondir,'temp_error_log.log'),'w') as f:
            f.write(e)
            f.write('\n'+srcpath)   #대상 파일명
            f.write('\n'+preword)   #preword
        print("★에러끝")

    #dlgNew = top.child_window(class_name="AWL:64040000:0:0:100077:0:0")


    btnSaveas=top.child_window(best_match='Toolbar다른 이름으로 저장')
    btnSaveas.wait("visible ready", timeout=6000)
    btnSaveas.click()

    try:
        dlgSaveas=app.window(title_re='문서를 다른 이름으로 저장')
        dlgSaveas.wait("visible ready", timeout=6000)
    except (TimeoutError, ElementNotFoundError) as e:
        print(e)
        print('★windows 리스트')
        #print(app.windows())

        print('★top.print_control 리스트')
        #print(top.print_control_identifiers())

        with open('temp.log','w',errors='ignore') as f:
            f.write(str(app.windows()))
        top.print_control_identifiers(2,filename='temp_cntl.log')

    #
    editFilename=dlgSaveas.child_window(best_match='Edit0')

    editFilename.wait("visible ready", timeout=20)

    editwFilename=EditWrapper(editFilename)
    cbFiletype=dlgSaveas.child_window(title="PDF 문서(*.pdf)", class_name="ComboBox")
    cbFiletype.wait("visible ready", timeout=20)


    


    cbwFiletype=ComboBoxWrapper(cbFiletype)
    ext=""
    if filetype=="word":
        cbwFiletype.select('Microsoft Word 문서(*.docx)')
        ext="docx"
    else:
        cbwFiletype.select('Microsoft Excel 워크북(*.xlsx)')
        ext = "xlsx"



    outputname="{0}.{1}".format(os.path.splitext(os.path.basename(srcpath))[0],ext)
    temp_outputname="{0}_temp.{1}".format(os.path.splitext(os.path.basename(srcpath))[0],ext)
    while(True):
        if editwFilename.window_text()==outputname or editwFilename.window_text()==os.path.splitext(outputname)[0]:
            time.sleep(1)
            break
        else:
            print("텍스트가 일치하지않음")
            time.sleep(1)
            if filetype == "word":
                cbwFiletype.select('Microsoft Word 문서(*.docx)')

            else:
                cbwFiletype.select('Microsoft Excel 워크북(*.xlsx)')


    ## 언어 설정값 확인
    try:
        cbLanguage = dlgSaveas.child_window(title="한국어 및 영어", class_name="ComboBox")
        cbLanguage.wait("visible ready", timeout=20)
    except TimeoutError as e:
        print("[!] 언어설정이 [한국어 및 영어]로 되어있지 않음")
        try:
            cbLanguage = dlgSaveas.child_window(title_re=".*어", class_name="ComboBox")
            cbLanguage.wait("visible ready", timeout=20)
        except Exception as e:
            raise Exception('언어 설정 combobox를 찾지 못함 - 2')
        cbwLanguage=ComboBoxWrapper(cbLanguage)
        cbwLanguage.select('한국어 및 영어')
    except ElementNotFoundError as e:
        raise Exception('언어 설정 combobox를 찾지 못함')


    chkAfterSaveOpen = dlgSaveas.child_window(title="저장 후 파일 열기", class_name="Button")
    chkAfterSaveOpen.wait("visible ready", timeout=20)
    chkAfterwSaveOpen = ButtonWrapper(chkAfterSaveOpen)




    while(True):

        if chkAfterwSaveOpen.get_check_state()==1: # 저장 후 파일 열기 체크 풀기
            chkAfterwSaveOpen.uncheck_by_click()
        else:
            break

    outputpath=os.path.join(outputdir,filetype,outputname)
    temp_outputpath=os.path.join(outputdir,filetype,temp_outputname)

    btnSave=dlgSaveas.child_window(title="저장(&S)", class_name="Button")
    btnSave.wait("visible ready", timeout=20)
    btnwSave=ButtonWrapper(btnSave)
    btnCancel = dlgSaveas.child_window(title="취소", class_name="Button")
    btnCancel.wait("visible ready", timeout=6000)
    btnwCancel = ButtonWrapper(btnCancel)


    while(True):
        isFileExists = os.path.exists(temp_outputpath)
        if isFileExists == True:  # 파일이 존재하면
            if os.path.exists(outputpath):  #output파일이 존재하면 temp_output삭제
                os.remove(temp_outputpath)
            else:
                shutil.move(temp_outputpath,outputpath)

            btnwCancel.click()

            try:
                dlgSaveas.wait_not("enabled visible ready", timeout=5)
            except TimeoutError as e:
                continue
            dlgSaveas.wait_not("enabled visible ready", timeout=20)
            print("파일 미생성")
            break

        else:                       #파일이 존재하지 않으면(정상)
            while(True):
                editwFilename.set_edit_text(temp_outputpath)             #파일 경로 입력
                if editwFilename.window_text()==temp_outputpath:
                    break
            btnwSave.click()

            try:
                dlgSaveas.wait_not("enabled visible ready", timeout=5)
            except TimeoutError as e:
                print("[!] time 에러발생 - 재시작")
                continue




            dlgConvert = app.window(title="변환")
            dlgConvert.wait("visible ready", timeout=20)

            btnClose = dlgConvert.child_window(title="취소(&C)", class_name="Button")
            btnClose.wait("visible ready", timeout=20)

            print("[*] Start Conversion")



            while True:
                try:

                    dlgConvert.wait_not("enabled visible ready", timeout=2)          # 2초 대기 '변환'창이 종료됨을 확인
                    ##print("wait_not으로 인한 종료 파악 성공.")
                    with open(temp_outputpath, "r+") as isOpened:                           #다이얼로그 창이 invisible인 상태에서 output파일의 읽기가능 여부 확인
                        # print("[*] End Conversion")
                        pass

                    break
                except FileNotFoundError as e:            # 파일이 아직 존재하지 않음[비정상으로 다이얼로그 창이 invisible된 상태
                    continue
                except IOError as e:  # 파일 접근에 실패하면 다시반복
                    time.sleep(1)
                    print("[!] 변환창 invisible 후, 파일 접근 재시도...")
                    pass

                except TimeoutError as e:                            #변환창이 종료되지 않았을 때,
                    try:
                        ##print("타임아웃")
                        txtMsg = dlgConvert.child_window(class_name=preword + ":3:10003:6:0:0",found_index=0)  # 오류/에러가 있는 경우
                        txtMsg.is_enabled()

                        if txtMsg is None:                               #txtMsg 존재 유무 학인, 존재하지 않으면 루틴 재시작
                            continue
                        txtMsgWinText=txtMsg.window_text()

                        txtResult = dlgConvert.child_window(best_match='Static0')  # 오류/에러가 있는 경우
                        txtResult.wait("visible ready", timeout=20)

                        if txtResult is None:                               #txtResult의 존재 유무 학인, 존재하지 않으면 루틴 재시작
                            continue

                        resultWinText = txtResult.window_text()

                        if resultWinText is not None:
                            if"경고" in resultWinText:
                                result = "경고"
                            elif "오류" in resultWinText:
                                result = "오류"
                            else:                               #정상인데 팝업타이밍이 미리뜬 경우
                                #잘못된 루틴이므로 재시작
                                continue
                            print("[!] {0}문구: {1}".format(result, txtMsgWinText))
                            break
                        else:
                            continue
                    except (ElementNotFoundError, TimeoutError, TypeError) as e:
                        continue

        if result !='오류':
            shutil.move(temp_outputpath,outputpath)

        print("[*] End Conversion")
        break

    time.sleep(2)

    app.kill()
    
    app.wait_for_process_exit(timeout=6000)
    print("[*] Kill ABBYY")


    #파일삭제

    while True:
        time.sleep(2)
        try:
            if os.path.exists(srcpath) == True:
                
                with open(srcpath, "r+") as isOpened:           #파일에 접근이 가능하면 파일 백업
                    pass

                shutil.move(srcpath, bak_full_path)
                print("[*] Close File and Move To Backup")
                
                if result=="오류":
                    shutil.copy(bak_full_path,fail_full_path)
                break
                    
        except IOError as e:                                     #파일 접근에 실패하면 다시반복
            time.sleep(1)
            print("[!] 파일 닫기 재시도...")
            pass

if __name__=="__main__":
    mondir = sys.argv[1]
    

    waiting=False
    try:
        while True:
            #print("<< 모니터링 모드 시작 >>")
            createDir(mondir)

            fileQueue=monitoring(mondir)

            if fileQueue.empty()==False:
                waiting=False
                print("\n<< 변환모드 시작 >>")
                while fileQueue.qsize()!=0:



                    srcpath,filetype=fileQueue.get()

                    print("[-] Dequeue - {0}".format(srcpath))

                    convertingPdf(srcpath,filetype)

                print("<< 변환모드 끝 >>\n")
            else:
                if waiting==False:
                    print("[∞] Waiting",end="",flush=True)
                    waiting=True
                else:
                    print(".",end="",flush=True)
                time.sleep(60)
    except Exception as e:
        print("< Pended >")
        sys.exit()


import time

import requests

from Get_Class_Activity import get_activity
from Get_Day_Course import get_course


def sign(signId, stuId, openClassId):
    qdurl = 'https://zjyapp.icve.com.cn/newmobileapi/faceteach/saveStuSign'
    qddata = {
        'signId': signId,
        'stuId': stuId,
        'classState': 2,
        'openClassId': openClassId
    }
    html = requests.post(url=qdurl, data=qddata).json()['msg']
    return html


def main(stuid):
    courses = get_course(stuid)
    if courses == 'no':
        print("你今天没有课，好好休息")
    else:
        print("Lan职教云助手提示您：\n您今天课表如下：")
        for i in range(len(courses['courseNmae'])):
            print(f'【{i + 1}】：{courses["classSection"][i]}{courses["courseNmae"][i]}')
        index = int(input("请输入你要监控的课程：")) - 1
        activities = get_activity(stuid, courses["courseId"][index], courses["openClassId"][index])
        js = 0
        # 反复监控，是否需要存在已开启的签到
        for i in range(18000):
            for i in range(len(activities)):
                activity = activities[i]
                datatype = activity['DataType']
                if datatype == '签到':
                    state = activity['Id']
                    if state == 2:
                        signId = activity['Id']
                        js += 1
                        print("您当前有一个签到，正在尝试帮你签到，请稍等！")

                        # 执行签到，为了能够失败重签，所以嵌套了一下
                        def panta():
                            msg = sign(signId, stuid, courses["openClassId"][index])
                            if msg == '签到成功':
                                print("签到成功！，我要休息半小时")
                                time.sleep(1800)
                            else:
                                print("签到失败，正在重新签到")
                                panta()

                        panta()
            if js == 0:
                print(f"系统未检测到需要签到哦！", end="当前时间：")
                print(time.strftime("%H:%M:%S", time.localtime()))
                time.sleep(30)


if __name__ == '__main__':
    stuid = ''
    main(stuid)

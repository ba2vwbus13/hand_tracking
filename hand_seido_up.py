import cv2
import numpy as np
import glob
from src.hand_tracker import HandTracker
import os

WINDOW = "Hand Tracking"
PALM_MODEL_PATH = "models/palm_detection_without_custom_op.tflite"
LANDMARK_MODEL_PATH = "models/hand_landmark.tflite"
ANCHORS_PATH = "models/anchors.csv"

POINT_COLOR = (0, 255, 0)
CONNECTION_COLOR = (255, 0, 0)
THICKNESS = 4
maisu = 0
upkei = 0
downkei = 0
stopkei = 0
onekei = 0
errorList = []

#files = glob.glob("/home/ic1/hand_tracking/HS画像/入力/陸上/1.5m/down/*")
files = glob.glob("/home/ic1/hand_tracking/HS画像/入力/水中/2m/stop/*")

for f in files:
    print('Image:{}'.format(f))
    #print(format(f))
    frame = cv2.imread(f)
    
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (5, 6), (6, 7), (7, 8),
        (9, 10), (10, 11), (11, 12),
        (13, 14), (14, 15), (15, 16),
        (17, 18), (18, 19), (19, 20),
        (0, 5), (5, 9), (9, 13), (13, 17), (0, 17)]

    detector = HandTracker(
        PALM_MODEL_PATH,
        LANDMARK_MODEL_PATH,
        ANCHORS_PATH,
        box_shift=0.2,
        box_enlarge=1.3
    )

    inf = 0
    maisu += 1 

    image = np.array(frame)
    points, _ = detector(image)
    p = [[0 for i in range(2)] for j in range(21)]
    if points is not None:
        n = 0
        #print(points)
        for point in points:
            x, y = point
            p[n][0] = x
            p[n][1] = y
            #print(n, ': x=', p[n][0], ', y=', p[n][1])
            n += 1
            cv2.circle(frame, (int(x), int(y)), THICKNESS * 2, POINT_COLOR, THICKNESS)
        for connection in connections:
            x0, y0 = points[connection[0]]
            x1, y1 = points[connection[1]]
            cv2.line(frame, (int(x0), int(y0)), (int(x1), int(y1)), CONNECTION_COLOR, THICKNESS)

        # 分類
        #右手
        if p[0][0] > p[17][0]:
            inf = 0
            print('右手')
            #if 親指の判定 and 人差し指の判定 and 中指の判定 and 薬指の判定 and 小指の判定:
            if p[2][1] > p[4][1] and p[6][0] < p[8][0] and p[10][0] < p[12][0] and p[14][0] < p[16][0] and p[18][0] < p[20][0]:
                print('浮上する')
                upkei += 1
            elif p[2][1] < p[4][1] and p[6][0] < p[8][0] and p[10][0] < p[12][0] and p[14][0] < p[16][0] and p[18][0] < p[20][0]:
                print('潜行する')
                downkei += 1
            elif p[2][1] > p[4][1] and p[6][1] > p[8][1] and p[10][1] > p[12][1] and p[14][1] > p[16][1] and p[18][1] > p[20][1]:
                print('ちょっと待って！')
                stopkei += 1
            elif p[2][0] > p[4][0] and p[6][1] > p[8][1] and p[10][1] < p[12][1] and p[14][1] < p[16][1] and p[18][1] < p[20][1]:
                print('１')
                onekei += 1
                inf = 1
            else :
                errorList.append(format(f))
            
        #左手
        elif p[0][0] < p[17][0]:
            inf = 0
            print('左手')
            if p[2][1] > p[4][1] and p[6][0] > p[8][0] and p[10][0] > p[12][0] and p[14][0] > p[16][0] and p[18][0] > p[20][0]:
                print('浮上する')
                upkei += 1
            elif p[2][1] < p[4][1] and p[6][0] > p[8][0] and p[10][0] > p[12][0] and p[14][0] > p[16][0] and p[18][0] > p[20][0]:
                print('潜行する')
                downkei += 1
            elif p[2][1] > p[4][1] and p[6][1] > p[8][1] and p[10][1] > p[12][1] and p[14][1] > p[16][1] and p[18][1] > p[20][1]:
                print('ちょっと待って！')
                stopkei += 1
            elif p[2][0] < p[4][0] and p[6][1] > p[8][1] and p[10][1] < p[12][1] and p[14][1] < p[16][1] and p[18][1] < p[20][1]:
                print('１')
                onekei += 1
                inf = 1
            else :
                errorList.append(format(f))
        else :
            print('エラー')
            errorList.append(format(f))

    else :
        errorList.append(format(f))

    """出力
    #ボタン表示
    cv2.rectangle(frame, (400, 100), (520, 150), (0, 255, 255), 4)
    cv2.rectangle(frame, (400, 100), (520, 150), (0, 0, 255), 2)
    cv2.rectangle(frame, (480, 120), (520, 150), (0, 0, 0), 2)
    """
    """
    #ボタン判定
    if inf == 1:
        #タップ
        if 400 <= p[8][0] <= 520 and 100 <= p[8][1] <= 150:
            cv2.putText(frame, 'tap', (280,150), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 255), 4)
        #ドラッグ
        if 400 <= p[8][0] <= 520 and 100 <= p[8][1] <= 150:
            cv2.putText(frame, 'Link start!', (100,200), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 255), 5)
            dx = p[8][0] - 120
            dy = p[8][1] - 50
        cv2.rectangle(frame, (0, 0), (120, 50), (0, 0, 255), 2)
        #cv2.rectangle(frame, (p[8][0]-40, p[8][1]-30), (p[8][0], p[8][1]), (0, 0, 0), 2)
    """
    
    cv2.imshow(WINDOW, frame)

    count = 0
    count = '%03d' % maisu
    name = "stop_water_out" + count + ".jpg"
    cv2.imwrite('/home/ic1/hand_tracking/HS画像/出力/水中/2m/stop/'+name, frame)
   
    key = cv2.waitKey(1)
    if key == 27:
        break

seido = stopkei / maisu * 100
print('総枚数', maisu)
print('upの表示回数', upkei)
print('downの表示回数', downkei)
print('stopの表示回数', stopkei)
print('1の表示回数', onekei)
print('精度', seido, '％')
print('ErrorList')
for s in errorList:
   print(s)
   #os.remove(s) 
cv2.destroyAllWindows()

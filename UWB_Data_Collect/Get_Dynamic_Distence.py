import requests
import time
import pandas
import threading
import queue
from openpyxl import load_workbook
from openpyxl.styles import colors, Font, Fill, NamedStyle
from openpyxl.styles import PatternFill, Border, Side, Alignment

codeStart = time.time()
Detail_Data = queue.Queue()

dis = []


undone = True
class dataIMU(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        before = {}
        max = 5
        while True:
            distance = requests.get("http://192.168.8.107/php/diagnosis.php?getrangingdiagnosis=4210000000001198&project_id=1")

            distance = distance.json()

            # distance["An0011"]["Ranging"] is string
            data = {"An0011": eval(distance["An0011"]),
                    "An0094": eval(distance["An0094"]),
                    "An0095": eval(distance["An0095"]),
                    "An0096": eval(distance["An0096"]),
                    "An0099": eval(distance["An0099"])}

            Ranging = {"An0011": data["An0011"]["Ranging"], "IMU11": data["An0011"]["IMU"],
                       "An0094": data["An0094"]["Ranging"], "IMU94": data["An0094"]["IMU"],
                       "An0095": data["An0095"]["Ranging"], "IMU95": data["An0095"]["IMU"],
                       "An0096": data["An0096"]["Ranging"], "IMU96": data["An0096"]["IMU"],
                       "An0099": data["An0099"]["Ranging"], "IMU99": data["An0099"]["IMU"]
                       }

            if before != Ranging:
                # print("Thread", self.num)
                before = Ranging
                Detail_Data.put(data)
                max -= 1
            if max <= 0:
                break


Actual_distance11 = 0
Actual_distance94 = 0
Actual_distance95 = 0
Actual_distance96 = 0
Actual_distance99 = 0

class data(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    def run(self):
        while Detail_Data.qsize() > 0 or undone:
            if Detail_Data.qsize() == 0:
                continue
            try:
                disData = Detail_Data.get()
                dis.append({"An0011_Ranging": disData["An0011"]["Ranging"],
                            "An0011_IMU": disData["An0011"]["IMU"],
                            "An0011_Actual_distance": Actual_distance11,
                            "An0094_Ranging": disData["An0094"]["Ranging"],
                            "An0094_IMU": disData["An0094"]["IMU"],
                            "An0094_Actual_distance": Actual_distance94,
                            "An0095_Ranging": disData["An0095"]["Ranging"],
                            "An0095_IMU": disData["An0095"]["IMU"],
                            "An0095_Actual_distance": Actual_distance95,
                            "An0096_Ranging": disData["An0096"]["Ranging"],
                            "An0096_IMU": disData["An0096"]["IMU"],
                            "An0096_Actual_distance": Actual_distance96,
                            "An0099_Ranging": disData["An0099"]["Ranging"],
                            "An0099_IMU": disData["An0099"]["IMU"],
                            "An0099_Actual_distance": Actual_distance99})
                print("An0011", disData["An0011"]["Ranging"], "IMU", disData["An0011"]["IMU"], "TagV", disData["An0011"]["TagVelocity"], "Actual distance" ,  Actual_distance11)
                print("An0094", disData["An0094"]["Ranging"], "IMU", disData["An0094"]["IMU"], "TagV", disData["An0094"]["TagVelocity"], "Actual distance",  Actual_distance94)
                print("An0095", disData["An0095"]["Ranging"], "IMU", disData["An0095"]["IMU"], "TagV", disData["An0095"]["TagVelocity"], "Actual distance",  Actual_distance95)
                print("An0096", disData["An0096"]["Ranging"], "IMU", disData["An0096"]["IMU"], "TagV", disData["An0096"]["TagVelocity"], "Actual distance",  Actual_distance96)
                print("An0099", disData["An0099"]["Ranging"], "IMU", disData["An0099"]["IMU"], "TagV", disData["An0099"]["TagVelocity"], "Actual distance",  Actual_distance99)
            except Exception:
                continue


        df = pandas.DataFrame(dis)
        firstrow = []
        firstrow.insert(0, {'name': '', 'age': '', 'sex': ''})
        pandas.concat([pandas.DataFrame(firstrow), df], ignore_index=True, sort=False)
        try:
            with pandas.ExcelWriter('G-print_3.xlsx', mode='a') as writer:
                df.to_excel(writer, sheet_name='100x100_An96_124', encoding="utf_8")
        except FileNotFoundError:
            df.to_excel('G-print_3.xlsx', sheet_name='440x170_An96_274', encoding="utf_8")


# class TagRealDistence(threading.Thread):
#     def __init__(self, num):
#         threading.Thread.__init__(self)
#         self.num = num
#
#     def run(self):
#         pass

# def TagRealDistence(Velocity):
#     pass
IMU = dataIMU("IMU")
Data = data("Data")



IMU.start()
Data.start()

IMU.join()
undone = False  # 要求工作已做完
Data.join()

print("Done")

codeEnd = time.time()
print(codeEnd - codeStart)
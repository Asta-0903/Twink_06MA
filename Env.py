# ___Import Statements___
from Base_Environment.B_Env import *
# from Custom_Widgets.Widgets import QCustomSlideMenu
# from Custom_Widgets.Widgets import *
# from MODULES.BASE_WIN import icon_rc

# ___Database Dictioanry___
Local_DB = \
    {
        'host': 'localhost',
        'user': 'root',
        'password': 'MSeGa@1109',
        'database': 'twink_06ma',
        'port': 3307,

    }
Cloud_DB = \
    {
        'host': '10.241.1.1',
        'user': 'AstA_V5_WAN',
        'password': 'AstA@1309',
        'database': 'twink_06ma',
        'port': 3307,
    }
# // Use """ db """ as variable for all db connections
dbase = DB_Connect(Local_DB)
dbc = dbase[0]
db = dbase[1]

# ___UI Creation___
app = Qwid.QApplication(sys.argv)
Home = uic.loadUi(fr'{ldir}\MODULES\BASE_WIN\UI-HomePage.ui')
UI_Confirm_Win = uic.loadUi(fr'{ldir}\MODULES\BASE_WIN\UI-Confirmation_Win.ui')
Rvt = uic.loadUi(fr'{ldir}\MODULES\REGISTER\UI-Revert_Win.ui')
Wge=uic.loadUi(fr'{ldir}\MODULES\WAGE CALC\Wage_Calcu.ui')
Adv = uic.loadUi(fr'{ldir}\MODULES\ADVANCE AMOUNT\Advance_amount.ui')
pwd= uic.loadUi(fr'{ldir}\MODULES\REGISTER\password.ui')
Rgtr = uic.loadUi(fr'{ldir}\MODULES\REGISTER\UI-Register.ui')
AttnPush = uic.loadUi(fr'{ldir}\MODULES\ATTENDANCE\UI-Attendance_Register.ui')
AttnView = uic.loadUi(fr'{ldir}\MODULES\ATTENDANCE\UI-Attendance_View.ui')
PnchBld = uic.loadUi(fr'{ldir}\MODULES\PUNCH_BUILD\UI-Punch_Build.ui')
PrsPnchTrck = uic.loadUi(fr'{ldir}\MODULES\PUNCH_BUILD\UI-Personal_Punch_Track.ui')

# ___Data_Fetch_Functions___
@Exception_Handle
def DB_Creation(inp,init):
    date_split=list(inp.split("-"))
    if init == True:
        for date in DateList(int(date_split[2]),int(date_split[1])):
            try:
                DB_Cmt_WOE(dbc, db, f"insert into attendance_track values ('{date}','YTC','{Cur_Date_SQL}')", True)
            except Exception as e:
                break
        try:
            TBL_Data=DB_Fetch(dbc,f"SHOW TABLES LIKE '{date_split[1]}_{date_split[2]}'",False,'LOE')
            print(TBL_Data)
            if f'{date_split[1]}_{date_split[2]}' in TBL_Data:
                return
        except:
            pass


    DB_Cmt(dbc,db,f'CREATE TABLE IF NOT EXISTS {date_split[1]}_{date_split[2]} (empcode varchar(50), primary key ('
                  f'empcode))',False)

    try:
        for i in range (1,calendar.monthrange(int(date_split[2]),int(date_split[1]))[1]+1):
            sql="alter table %s_%s add column (`%s` varchar(30))"%(date_split[1],date_split[2],str(i).zfill((2)))
            DB_Cmt_WOE(dbc, db,sql,False)
    except :
        pass

    db_data=DB_Fetch(dbc,"select emp_code from register where active_status = 'Y'",False,'LOE')
    for i in db_data:
        try:
            DB_Cmt_WOE(dbc,db,fr"insert into {date_split[1]}_{date_split[2]} (empcode) values ('{str(i)}')",False)
        except Exception as e:
            print('XXs', e)
            pass

def DateList(year, month):
    first_day = datetime(year, month, 1)

    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = next_month - timedelta(days=1)

    current_day = first_day
    while current_day <= last_day:
        yield current_day
        current_day += timedelta(days=1)

def TD_datelist(year, month):
    today = date.today()
    first_day = date(year, month, 1)

    # Calculate the last day of the specified month and year
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)

    current_day = first_day

    while current_day <= today and current_day <= last_day:
        yield current_day
        current_day += timedelta(days=1)

DB_Creation(Cur_Date_NF,True)

Active_EmpC=DB_Fetch(dbc,"select emp_code from register where active_status = 'Y'",False,'LOE')
Active_EmpList=DB_Fetch(dbc,"select employee_name from register where active_status = 'Y'",False,'LOE')

@Exception_Handle
def Attendance_Fetch(inp):
    form = list(inp.split("-"))
    print(form)
    try:
        sql="select register.team,register.employee_name, %s_%s.* from register inner join %s_%s on " \
            "register.emp_code = %s_%s.empcode where register.active_status = 'Y' order by register.emp_code" % (
                         form[0], form[1], form[0], form[1], form[0], form[1])
        db_data = DB_Fetch(dbc,sql,True,"LOL")
        print(db_data[0])
        for i in range(len(db_data)):
            db_data[i].insert(0, db_data[i][2])
            del db_data[i][3]
        db_data = [[item if item is not None else "NA" for item in inner_list]for inner_list in db_data]
    except:
        db_data=[[]]
    return db_data

Attendance_View_XLF = False
def Attendance_datasplit(data,filter,XLF):
    #print(data)
    if filter == 'Attendance':
        try:
            for part in data:
                for i in range(3,len(part)):
                    try:
                        temp=list(part[i].split("::"))
                        part[i]=temp[0]
                    except:
                        pass
        except:
            pass
    elif filter == 'OT':
        for part in data:
            for i in range(3,len(part)):
                #print(part[i])
                try:
                    temp=list(part[i].split("::"))
                    part[i]=temp[1]
                except:
                    pass

    elif filter == 'Atn+ot':
        for part in data:
            for i in range(3,len(part)):
                try:
                    temp=list(part[i].split("::"))
                    part[i]=f'{temp[0]} :: {temp[1]}'
                except:
                    pass
    dataT1=[]
    dataT2=[]
    for step in data:
        dataT1.append(step[:3])
        dataT2.append(step[3:])
    if  XLF == True:
        return data
    return [dataT1,dataT2]

def Punch_Build_Data(empcode,inp):

    inp_next = (lambda d: (d + timedelta(days=1)).strftime("%Y-%m-%d"))(datetime.strptime(inp, "%Y-%m-%d"))
    #Check_In List
    CheckIN = DB_Fetch(dbc,f"SELECT it.Timestamp FROM register r JOIN punch_logs it ON "
                     f"r.emp_code = it.Emp_Code where Timestamp between '{inp} 06:00:00' "
                     f"AND '{inp} 23:50:00' and r.emp_code='{empcode}' and Direction = 'in'",False,"LOE")

    if len(CheckIN)==0:return["NA","NA","NA","NA","A::0.0"]
    CheckIN = min(CheckIN)
    try:C_I = CheckIN.strftime("%H:%M")
    except :C_I = "NA"

    timestamps = DB_Fetch(dbc, f"SELECT it.Timestamp FROM register r JOIN punch_logs it ON "
                               f"r.emp_code = it.Emp_Code where Timestamp between '{inp} 08:00:00' "
                               f"AND '{inp_next} 08:00:00' and r.emp_code='{empcode}' and Direction = 'out'", False,
                              "LOE")


    if CheckIN.time() <=  time(10,00,0) :

        try:L_O = min([dt for dt in timestamps if time(7, 30, 0) <= dt.time() <= time(14, 30, 0)]).strftime("%H:%M")
        except:L_O= "NA"

        try:
            L_I = max([dt for dt in timestamps if time(7, 30, 0) <= dt.time() <= time(14, 45, 0)]).strftime("%H:%M")
            if L_I == L_O:L_I="NA"
        except:L_I = "NA"

        try:C_O = max([dt for dt in timestamps if time(14, 40, 0) <= dt.time() <= time(20, 0, 0)]).strftime("%H:%M")
        except:C_O= "NA"

        if L_O != "NA" and L_I != "NA" and C_O != "NA":
            FH = (datetime.strptime(L_O, "%H:%M") - datetime.strptime(C_I, "%H:%M")).total_seconds() / 3600
            LT = (datetime.strptime(L_I, "%H:%M") - datetime.strptime(L_O, "%H:%M")).total_seconds() / 3600
            SH = (datetime.strptime(C_O, "%H:%M") - datetime.strptime(L_I, "%H:%M")).total_seconds() / 3600
            NH = round((FH + SH), 0)

            if NH < 8:
                NH = "1A::" + str(NH)
            elif NH >= 8:
                NH = "1::" + str(NH - 8)
        else:
            NH = "A::0.0"


    if time(14, 50, 0) <= CheckIN.time() <= time(15, 50, 0):

        try:
            L_O = min([dt for dt in timestamps if time(19, 30, 0) <= dt.time() <= time(22, 00, 0)]).strftime("%H:%M")
        except:
            L_O = "NA"

        try:
            L_I = max([dt for dt in timestamps if time(19, 30, 0) <= dt.time() <= time(22, 00, 0)]).strftime("%H:%M")
            if L_I == L_O: L_I = "NA"
        except:
            L_I = "NA"

        try:
            C_O = max([dt for dt in timestamps if time(22, 00, 0) <= dt.time() <= time(23, 50, 0)]).strftime("%H:%M")
        except:
            C_O = "NA"

        if L_O != "NA" and L_I != "NA" and C_O != "NA":
            FH = (datetime.strptime(L_O, "%H:%M") - datetime.strptime(C_I, "%H:%M")).total_seconds() / 3600
            LT = (datetime.strptime(L_I, "%H:%M") - datetime.strptime(L_O, "%H:%M")).total_seconds() / 3600
            SH = (datetime.strptime(C_O, "%H:%M") - datetime.strptime(L_I, "%H:%M")).total_seconds() / 3600
            NH = round((FH + SH), 0)
            if NH < 8:
                NH = "2A::" + str(NH)
            elif NH >= 8:
                NH = "2::" + str(NH - 8)
        else:
            NH = "A::0.0"

    if time(22, 00, 0) <= CheckIN.time() <= time(23, 50, 0):

        try:
            L_O = min([dt for dt in timestamps if time(2, 00, 0) <= dt.time() <= time(5, 30, 0)]).strftime("%H:%M")
        except:
            L_O = "NA"

        try:
            L_I = max([dt for dt in timestamps if time(2, 00, 0) <= dt.time() <= time(5, 30, 0)]).strftime("%H:%M")
            if L_I == L_O: L_I = "NA"
        except:
            L_I = "NA"

        try:
            C_O = max([dt for dt in timestamps if time(6, 30, 0) <= dt.time() <= time(7, 30, 0)]).strftime("%H:%M")
        except:
            C_O = "NA"

        if L_O != "NA" and L_I != "NA" and C_O != "NA":
            FH = (datetime.strptime(L_O, "%H:%M") - datetime.strptime(C_I, "%H:%M")).total_seconds() / 3600
            if FH < 0 :
                FH = Time_Difference_Behind(L_O, C_I)
            LT = (datetime.strptime(L_I, "%H:%M") - datetime.strptime(L_O, "%H:%M")).total_seconds() / 3600
            SH = (datetime.strptime(C_O, "%H:%M") - datetime.strptime(L_I, "%H:%M")).total_seconds() / 3600
            NH = round((FH + SH), 0)

            if NH < 8:
                NH = "3A::" + str(NH)
            elif NH >= 8:
                NH = "3::" + str(NH - 8)
        else:
            NH = "A::0.0"


    return [C_I,L_O,L_I,C_O,NH]

def Convert_Punch_Attendance(data):

    if "NA" in data:
        return "A::0.0"

    if datetime.strptime(data[0], "%H:%M").time() <=  time(10,00,0) :
        FH = (datetime.strptime(data[1], "%H:%M") - datetime.strptime(data[0], "%H:%M")).total_seconds() / 3600
        LT = (datetime.strptime(data[2], "%H:%M") - datetime.strptime(data[1], "%H:%M")).total_seconds() / 3600
        SH = (datetime.strptime(data[3], "%H:%M") - datetime.strptime(data[2], "%H:%M")).total_seconds() / 3600
        NH = round((FH + SH), 0)
        if NH < 8:
            NH = "1A::" + str(NH)
        elif NH >= 8:
            NH = "1::" + str(NH - 8)

    if time(14, 50, 0) <= datetime.strptime(data[0], "%H:%M").time() <= time(15, 50, 0):
        print("XX")
        FH = (datetime.strptime(data[1], "%H:%M") - datetime.strptime(data[0], "%H:%M")).total_seconds() / 3600
        LT = (datetime.strptime(data[2], "%H:%M") - datetime.strptime(data[1], "%H:%M")).total_seconds() / 3600
        SH = (datetime.strptime(data[3], "%H:%M") - datetime.strptime(data[2], "%H:%M")).total_seconds() / 3600
        NH = round((FH + SH), 0)
        if NH < 8:
            NH = "2A::" + str(NH)
        elif NH >= 8:
            NH = "2::" + str(NH - 8)


    if time(22, 00, 0) <= datetime.strptime(data[0], "%H:%M").time() <= time(23, 50, 0):
        FH = (datetime.strptime(data[1], "%H:%M") - datetime.strptime(data[0], "%H:%M")).total_seconds() / 3600
        if FH < 0 :
            FH = Time_Difference_Behind(data[1], data[0])
        LT = (datetime.strptime(data[2], "%H:%M") - datetime.strptime(data[1], "%H:%M")).total_seconds() / 3600
        SH = (datetime.strptime(data[3], "%H:%M") - datetime.strptime(data[2], "%H:%M")).total_seconds() / 3600
        NH = round((FH + SH), 0)

        if NH < 8:
            NH = "3A::" + str(NH)
        elif NH >= 8:
            NH = "3::" + str(NH - 8)

    return NH

def Punch_Build_Fetch(res,date):
    try:
        data=DB_Fetch(dbc,fr"select gen_attn from punch_build where emp_code = '{res}' and gen_date='{date}'",
                      False,"LOE")
        return data[0]
    except Exception as e:print(e);return 'A::0.0'

def EmpCode_Fetch(inp):
    try:
        return DB_Fetch(dbc,f"select emp_code from register where employee_name= '{inp}'",False,"LOE")[0]
    except:
        pass

@Exception_Handle
def read_image(file_path):
        with open(file_path, 'rb') as file:
            return file.read()

Dept=['TFO','SPINNING','BLOW ROOM','SUPERVISOR','FACTORY MANAGER','CARDING','PACKING','AUTO DOFFER','CARDING FITTER',
'AUTO CONER','SIMPLEX','WATCHMAN','SWEEPING','TRAINING','SPINNING FITTER','ELECTRICIAN','CHEESE WINDING','SQC','DRIVER',
'COOKING','SPINNING MASTER','DRAWING','TFO FITTER','GENERAL MANAGER','MAINTANENCE SUPERVISOR','ACCOUNTS','ELECTRICAL HELPER',
'CHECK','AUTO CONER FITTER','ELECTRICAL SUPERVISOR','TFO TRAINER','SCAVENGER','COW MAN','COOK ASST']
Team=['Assam','PF Native','Jharkand','Odisha','CHECK','NPF Native']
Blod_grp=['A+','A-','B+','B-','O+','O-','AB+','AB-']

def AttendaceFetch_Day(inp):
    date_split=inp.split("-")
    return DB_Fetch(dbc,fr"select empcode,`{date_split[2]}` from {date_split[1]}_{date_split[0]}",False,"DIC")

def Emp_code_Gen(type):
    if type :
        db_data = DB_Fetch(dbc, "SELECT MAX(CAST(SUBSTRING(emp_code, 4) AS UNSIGNED)) +1 AS max_value FROM register "
                                "WHERE emp_code LIKE 'SIL%';", False, "LOE")[0]
        return str("SIL" + str(db_data).zfill(3))
    else:
        db_data = DB_Fetch(dbc, "SELECT MAX(CAST(SUBSTRING(emp_code, 5) AS UNSIGNED)) +1 AS max_value FROM register "
                                "WHERE emp_code LIKE 'TEMP%';", False, "LOE")[0]
        return str("TEMP" + str(db_data).zfill(3))

def resize_image(image_data, new_width, new_height):
    image = Image.open(BytesIO(image_data))
    resized_image = image.resize((new_width, new_height))
    buffered = BytesIO()
    resized_image.save(buffered, format="JPEG")  # You can change the format if needed (JPEG, PNG, etc.)
    return buffered.getvalue()

def Fetch_Employee_ID(inp):
    return DB_Fetch(dbc,f"select UID from register where employee_name ='{inp}'",False,"LOE")[0]

@Exception_Handle
def Fetch_Employee_Info(inp):
    return DB_Fetch(dbc,f"select * from register where UID = '{Fetch_Employee_ID(inp)}'",False,"LOE")




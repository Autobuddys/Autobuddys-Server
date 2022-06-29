import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
import jwt
from datetime import datetime, timedelta
from api.settings import SIMPLE_JWT
from rest_framework.permissions import IsAuthenticated, AllowAny
from elder import serializers,models,permissions
from django.db import connection 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
import calendar
from calendar import monthrange
from .apps import ElderConfig
from rest_framework.parsers  import MultiPartParser,FormParser




def query(q) :#function to execute raw sql query
    with connection.cursor() as c:
        c.execute(q)
        if q[0:6].lower()=="select":
            return dictfetchall(c) # returns result of query only if it a select query
        else :
            return "success"

def dictfetchall(cursor):#dependency for query function
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
###################################################  PDF GENERATION CODE  #######################################################
###################################################  PDF GENERATION CODE  #######################################################
###################################################  PDF GENERATION CODE  #######################################################



from fpdf import FPDF
import shutil
import os
from django.http import FileResponse



import io

def createReport(preProfile,finresult,a,b,x,tempavg,countT,countS,spo2avg,bpavg,countP,countB,bpmavg):
    # print()
    # print(finresult)
    # print()
    pdf=FPDF(format='letter', unit='mm')
    pdf.set_top_margin(20)
    
    # Add new page. Without this you cannot create the document.
    pdf.add_page()
    
    # Remember to always put one of these at least once.
    pdf.set_font('Times','',10.0) 
    
    # Effective page width, or just epw
    epw = pdf.w - 2*pdf.l_margin
    
    # Set column width to 1/4 of effective page width to distribute content 
    # evenly across table and page
    col_width = epw/5
    # PLOT_DIR = 'reports'
    # shutil.rmtree(PLOT_DIR)
    # os.mkdir(PLOT_DIR)
    pdf.image('assets/logoFinal.png', 0.02,0.01, 50,14)
    pdf.set_font('Times','B',14.0) 
    pdf.cell(epw, 0.0, 'Health Report', align='C')
    pdf.ln(12)
    pdf.set_font('Times','',10.0)
    top = pdf.y
    offset = pdf.x + 130
    pdf.multi_cell(90,0,f"Patient Name : {preProfile[0]['pname']}",0,align='L')


    pdf.y = top
    pdf.x = offset 
    pdf.multi_cell(90,0,f'Doctor Name : Dr. {preProfile[0]["dname"]}',0,align='L')

    pdf.ln(4)
    top = pdf.y
    offset = pdf.x + 130
    pdf.multi_cell(90,0,f'Phone Number (Patient) : {preProfile[0]["pphone"]}',0,align='L')


    pdf.y = top
    pdf.x = offset 
    pdf.multi_cell(90,0,f'Contact Number (Doctor) : {preProfile[0]["dphone"]}',0,align='L')

    
    pdf.ln(4)
    pdf.cell(epw, 0.0, f'Patient Age : {preProfile[0]["page"]}', align='L')
    pdf.ln(4)
    pdf.cell(epw, 0.0, f'Patient Address : {preProfile[0]["address"]}', align='L')
    pdf.ln(8)
    pdf.cell(epw, 0.0, f'Report Generated Duration : {a.date()} - {b.date()}', align='L')
    pdf.ln(4)
    pdf.cell(epw, 0.0, f'Timestamp of Report Generation : {x}',align='L')
    
    pdf.ln(7)

    if(countT!=0):
        pdf.cell(epw, 0.0, f'Temperature Average : {int(tempavg/countT)}',align='L')
    else:
        pdf.cell(epw, 0.0, f'Temperature Average : --',align='L')
    
    pdf.ln(4)
    if(countS!=0):
        pdf.cell(epw, 0.0, f'SpO2 Average : {int(spo2avg/countS)}', align='L')
    else:
        pdf.cell(epw, 0.0, f'SpO2 Average : --',align='L')
    
    
    pdf.ln(4)
    if(countP!=0):
        pdf.cell(epw, 0.0, f'Blood Pressure Average : {int(bpavg/countP)}',align='L')
    else:
        pdf.cell(epw, 0.0, f'Blood Pressure Average : --',align='L')
    
    
    pdf.ln(4)
    if(countB!=0):
        pdf.cell(epw, 0.0, f'Beats per Minute Average : {int(bpmavg/countB)}',align='L')
    else:
        pdf.cell(epw, 0.0, f'Beats per Minute Average : --',align='L')
    
    

    pdf.ln(7)
    
    

    pdf.set_fill_color(255, 94, 94)
    # Text height is the same as current font size
    th = pdf.font_size+1
    s=0
    for row in finresult:
        for datum in range(0,len(row)):
            if s<5:
                pdf.cell(col_width, th, str(row[datum]), border=1,align='C')
                s+=1
                continue
            if (datum==1 and (int(row[datum])>=34 or int(row[datum])<=30)) or (datum==2 and (int(row[datum])>=80 or int(row[datum])<=30)) or (datum==3 and (int(row[datum])>=30 or int(row[datum])<=20)) or (datum==4 and (int(row[datum])>=50 or int(row[datum])<=20)):
                pdf.cell(col_width, th, str(row[datum]), border=1,align='C',fill=True)
            else:
                pdf.cell(col_width, th, str(row[datum]), border=1,align='C')
    
        pdf.ln(th)
    
    
    pdf.ln(2*th)
    pdf.cell(epw, 0.0, '** The red fills indicate an abnormal reading!', 
    align='L')
    pdf.ln(4*th)
    # pdf.output('reports/report.pdf','F')
    # print(buf)
    return io.BytesIO(bytes(pdf.output(dest = 'S'), encoding='latin1'))
    
    # print(pdf.output(dest='S'))

    # return FileResponse(pdf.output(dest='S'),as_attachment=True,filename="Report.pdf")

def storeData(dat):
    print("haan aaye the")
    global reportdata
    reportdata=dat


class ReportDataView(APIView):
    # reportdata=bytes('','latin1')

    def get(self,req,pk,format=None):
        print(reportdata)
        response = FileResponse(reportdata)
        response.headers = {   
            'Content-Type': 'application/pdf',
            'Content-Disposition': 'attachment;filename="report.pdf"',
        }
        response.as_attachment = True
        response.filename='report.pdf'
        return response
        

    def post(self, request, format=None):
        # print("andar to aao yaar")
        x = datetime.now()
        preProfile = query(F"select * from elder_patientrelative where id='{request.data['patID']}'")
        tempavg=0
        bpmavg=0
        spo2avg=0
        bpavg=0
        countT=0
        countB=0
        countS=0
        countP=0
        
        if request.data['type']=="dates" and request.data['dur']=="total":
            a=datetime(request.data['fromY'],request.data['fromM']+1,request.data['fromD'])
            b=datetime(request.data['toY'],request.data['toM']+1,request.data['toD'])
            print(a,b)
            raw_query = f"""SELECT * FROM elder_vital WHERE patid_id={request.data['patID']} AND entered_at BETWEEN '{a}' AND '{b}' ORDER BY entered_at ASC"""
            
            
            result=query(raw_query)
            finresult=[]
            print(result)
            finresult.append(['Date','Temperature','SpO2','BPM','BP'])
            if result==[]:
                return Response("No valid data recorded for the given duration!")
            else:
                
                for i in result:
                    temp=i.copy()
                    if not i['tempval']>=34 or i['tempval']<=30:
                        tempavg+=i['tempval']
                        countT+=1
                    if not i['spo2val']>=80 or i['spo2val']<=30:
                        spo2avg+=i['spo2val']
                        countS+=1
                    if not i['bpmval']>=30 or i['bpmval']<=20:
                        bpmavg+=i['bpmval']
                        countB+=1
                    if not (i['bpval']>=50 or i['bpval']<=20):
                        bpavg+=i['bpval']
                        countP+=1
                    tp=[]
                    
                    tp=[temp['entered_at'].date(),temp['tempval'],temp['spo2val'],temp['bpmval'],temp['bpval']]
                    finresult.append(tp)
                # print(tempavg/countT,bpavg/countP,bpmavg/countB,spo2avg/countS)

                # Document title centered, 'B'old, 14 pt
                reportdata=createReport(preProfile,finresult,a,b,x,tempavg,countT,countS,spo2avg,bpavg,countP,countB,bpmavg)
                storeData(reportdata)
                return Response("done!")

        elif(request.data['dur']=="monyear"):
            # print("in monyear : ",request.data['fromM'])
            a=datetime(request.data['fromY'],request.data['fromM']+1,1)
            print("in monyear a : ",a)
            b=datetime(request.data['fromY'],request.data['fromM']+1,monthrange(request.data['fromY'],request.data['fromM']+1)[1])
            print("in monyear b : ",b)
            raw_query = f"""SELECT * FROM elder_vital
                        WHERE patid_id={request.data['patID']}
                        AND entered_at BETWEEN '{a}' AND '{b}'
                        ORDER BY entered_at ASC"""
            
            result=query(raw_query)
            finresult=[]

            finresult.append(['Date','Temperature','SpO2','BPM','BP'])
            if result==[]:
                return Response("No valid data recorded for the given duration!")
            else:
                
                for i in result:
                    temp=i.copy()
                    if not i['tempval']>=34 or i['tempval']<=30:
                        tempavg+=i['tempval']
                        countT+=1
                    if not i['spo2val']>=80 or i['spo2val']<=30:
                        spo2avg+=i['spo2val']
                        countS+=1
                    if not i['bpmval']>=30 or i['bpmval']<=20:
                        bpmavg+=i['bpmval']
                        countB+=1
                    if not (i['bpval']>=50 or i['bpval']<=20):
                        bpavg+=i['bpval']
                        countP+=1
                    tp=[]
                    
                    tp=[temp['entered_at'].date(),temp['tempval'],temp['spo2val'],temp['bpmval'],temp['bpval']]
                    finresult.append(tp)
                # print(tempavg/countT,bpavg/countP,bpmavg/countB,spo2avg/countS)

                # Document title centered, 'B'old, 14 pt
                # print(finresult)
                reportdata=createReport(preProfile,finresult,a,b,x,tempavg,countT,countS,spo2avg,bpavg,countP,countB,bpmavg)
                storeData(reportdata)
                return Response("done!")
                
        else:
            a=datetime(request.data['fromY'],1,1)
            b=datetime(request.data['fromY'],12,monthrange(request.data['fromY'],12)[1])
            raw_query = f"""SELECT * FROM elder_vital
                        WHERE patid_id={request.data['patID']}
                        AND entered_at BETWEEN '{a}' AND '{b}'
                        ORDER BY entered_at ASC"""
            
            result=query(raw_query)
            finresult=[]

            finresult.append(['Date','Temperature','SpO2','BPM','BP'])
            if result==[]:
                return Response("No valid data recorded for the given duration!")
            else:
                
                for i in result:
                    temp=i.copy()
                    if not i['tempval']>=34 or i['tempval']<=30:
                        tempavg+=i['tempval']
                        countT+=1
                    if not i['spo2val']>=80 or i['spo2val']<=30:
                        spo2avg+=i['spo2val']
                        countS+=1
                    if not i['bpmval']>=30 or i['bpmval']<=20:
                        bpmavg+=i['bpmval']
                        countB+=1
                    if not (i['bpval']>=50 or i['bpval']<=20):
                        bpavg+=i['bpval']
                        countP+=1
                    tp=[]
                    
                    tp=[temp['entered_at'].date(),temp['tempval'],temp['spo2val'],temp['bpmval'],temp['bpval']]
                    finresult.append(tp)
                # print(tempavg/countT,bpavg/countP,bpmavg/countB,spo2avg/countS)

                # Document title centered, 'B'old, 14 pt
                # print(finresult)
                reportdata=createReport(preProfile,finresult,a,b,x,tempavg,countT,countS,spo2avg,bpavg,countP,countB,bpmavg)
                storeData(reportdata)
                # with open('reports/report.pdf','r',errors="ignore") as report:
                #     return Response(
                #         report.read(),
                #         headers={'Content-Disposition': 'attachment; filename="file.pdf"'},
                #         content_type='application/pdf')
                # response = FileResponse(open('reports/report.pdf', 'rb'))
                # response.headers = {   
                #     'Content-Type': 'application/pdf',
                #     'Content-Disposition': 'attachment;filename="report.pdf"',
                # }
                # response.as_attachment = True
                # return response
                
                return Response("done!")
            

            
        # return Response("nada")


###################################################  PDF GENERATION CODE  #######################################################
###################################################  PDF GENERATION CODE  #######################################################
###################################################  PDF GENERATION CODE  #######################################################





# JUICY STUFF STARTS HERE

class UserProfileViewset(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (permissions.UpdateOwnProfile,)
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email')

class MedicalStaffViewset(viewsets.ModelViewSet):
    queryset = models.MedicalStaff.objects.all()
    serializer_class = serializers.MedicalStaffSerializer
    permission_classes = (permissions.UpdateOwnProfileMed,)
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('hospname')

class PatientRelativeViewset(viewsets.ModelViewSet):
    queryset = models.PatientRelative.objects.all()
    serializer_class = serializers.PatientRelativeSerializer
    permission_classes = (permissions.UpdateOwnProfilePat,)
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('pname','dname')

class NotificationViewset(viewsets.ModelViewSet):
    queryset = models.Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    # permission_classes = (permissions.UpdateOwnProfilePat,)
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('patid','staffid')

# class ImageViewset(viewsets.ModelViewSet):
#     queryset = models.ImageStore.objects.all()
#     serializer_class = serializers.PostImageSerializer
#     # permission_classes = (permissions.UpdateOwnProfilePat,)
#     # authentication_classes = (TokenAuthentication,)
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('patid','pname')




# def mlmodel(): yeh tera function
def mlmodel1(request):
    bpmval = float(request.data['bpmval']) / 255
    tempval = float(request.data['tempval']) / 255
    spo2val = float(request.data['spo2val']) / 255
    lin_reg_model = ElderConfig.model1
    sbp_preadict = lin_reg_model.predict([[bpmval, tempval, spo2val]])[0][0]
    sbp_preadict = 255*sbp_preadict
    bpval = sbp_preadict
    return (bpval)

    
class Vitals(APIView):
    def post(self, request,format=None):
        bpval=mlmodel1(request)
        request.data["bpval"]=bpval
        p = serializers.VitalSerializer(data=request.data)
        if p.is_valid(raise_exception=True):
            p.save()
        return Response({'message':'saved'})




class VerifyView(APIView):
    
    def post(self, request, format=None):
        token=request.headers.get('Authorization')
        
        if token:
            decoded_token = jwt.decode(token[4:],SIMPLE_JWT['SIGNING_KEY'],algorithms=SIMPLE_JWT['ALGORITHM'])
            # print(decoded_token)
            id = decoded_token['user_id']
            preProfile = query(F"select * from elder_userprofile where id='{id}';")[0]
            # print(preProfile)
            if preProfile:
                finuser = {
                    'id':preProfile['id'],
                    'name':preProfile['name'],
                    'email':preProfile['email'],
                    'phone':preProfile['phone'],
                    'is_medical':preProfile['is_medical']
                }
                return Response(json.dumps(finuser),status=200,headers={'Access-Control-Allow-Origin':'*' })
            else:
                return Response(None)
        else:
            return Response(None)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PatientListViewRelative(APIView):
    def get(self,req,pk,format=None):
        result = query(f"select id, pname from elder_patientrelative where patrel_id='{pk}'")
        if result==[]:
            return Response("")
        return Response(result)

class RelativePatientDataView(APIView):
    def post(self,req):
        result=query(f"select * from elder_patientrelative where patrel_id='{req.data['relID']}' and id='{req.data['patID']}'")
        result2=query(f"select email,name,phone from elder_userprofile where id='{req.data['relID']}'")
        res=result+result2
        if len(res)>0:return Response(res)
        return Response("gadbad jhala")

class VitalPatientDataView(APIView):
    def get(self,req,pk,format=None):
        x = datetime.now()
        start=datetime(x.year,x.month,x.day)
        
        t=0
        b=0
        s=0
        bp=0
        cout=0
        raw_query = f"""SELECT * FROM elder_vital
                        WHERE patid_id={pk}
                        AND entered_at BETWEEN '{start}' AND '{x}'"""
        result=query(raw_query)
        if result==[]:
            return Response("No readings for today!")
        else:
            for i in result:
                t+=i['tempval']
                cout+=1
                b+=i['bpmval']
                s+=i['spo2val']
                bp+=i['bpval']
                    
        return Response(json.dumps({"tempavg":int(t/cout),"bpmavg":int(b/cout),"spavg":int(s/cout),"bpavg":int(bp/cout)}))

class VitalGraphDataView(APIView):
    def get(self,req,pk,format=None):
        x = datetime.now()
        start=datetime(x.year,x.month,x.day)
        raw_query = f"""SELECT * FROM elder_vital
                        WHERE patid_id={pk}
                        AND entered_at BETWEEN '{start}' AND '{x}'"""
        result=query(raw_query)
        finarr=[]
        if result==[]:
            return Response("No readings for today!")
        else:
            return Response(result)

class ChartDataView(APIView):
    def get(self,req,pk,format=None):
        x = datetime.now()
        y=[0,1,2,3,4,5,6]
        finarr=[]
        # categories=[]

        if pk[0]=='W':
            date_str=str(str(x.year)+"-"+str(x.month)+"-"+str(x.day))
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            start_of_week = date_obj - timedelta(days=date_obj.weekday())# Monday
            end_of_week = start_of_week+timedelta(days=6)

            raw_query = f"""SELECT * FROM elder_vital
                        WHERE patid_id={pk[1:]}
                        AND entered_at BETWEEN '{start_of_week}' AND '{end_of_week}'"""
            result=query(raw_query)

            # result = query(f"select * from elder_vital where patid_id='{pk[1:]}' order by entered_at asc")
            if result==[]:
                return Response("No readings for the week!")
            else:
                finres={}
                for i in result:
                    if str(i['entered_at'].date()) in finres:
                        arr=finres[str(i['entered_at'].date())]
                        newarr=[arr[0]+i['tempval'],arr[1]+i['spo2val'],arr[2]+i['bpmval'],arr[3]+i['bpval'],arr[4]+1]
                        finres[str(i['entered_at'].date())]=newarr
                    else: finres[str(i['entered_at'].date())]=[i['tempval'],i['spo2val'],i['bpmval'],i['bpval'],1]

                    return Response(finres)

        elif pk[0]=='M':
            result = query(f"select * from elder_vital where patid_id='{pk[1:]}' order by entered_at asc")
            # raw_query = f"""SELECT * FROM elder_vital
            #             WHERE patid_id={pk[1:]}
            #             AND entered_at BETWEEN '{start_of_week}' AND '{end_of_week}'"""
            # result=query(raw_query)
            if result==[]:
                return Response("")
            else:
                finres={}
                for i in result:
                    if i['entered_at'].year==x.year and i['entered_at'].month==x.month:
                        finarr.append(i)
                if finarr==[]:return Response("No readings for the month!")
                else:
                    for i in finarr:
                        if str(i['entered_at'].date()) in finres:
                            arr=finres[str(i['entered_at'].date())]
                            newarr=[arr[0]+i['tempval'],arr[1]+i['spo2val'],arr[2]+i['bpmval'],arr[3]+i['bpval'],arr[4]+1]
                            finres[str(i['entered_at'].date())]=newarr
                        else: finres[str(i['entered_at'].date())]=[i['tempval'],i['spo2val'],i['bpmval'],i['bpval'],1]

                    return Response(finres)

        elif pk[0]=='Y':
            start_year=datetime(x.year,1,1)
            raw_query = f"""SELECT * FROM elder_vital
                        WHERE patid_id={pk[1:]}
                        AND entered_at BETWEEN '{start_year}' AND '{x}'
                        ORDER BY entered_at ASC"""
            result=query(raw_query)
            if result==[]:
                return Response("No readings for the month!")
            else:
                finres={}
                for i in result:
                    if calendar.month_name[i['entered_at'].month] in finres:
                        arr=finres[calendar.month_name[i['entered_at'].month]]
                        newarr=[arr[0]+i['tempval'],arr[1]+i['spo2val'],arr[2]+i['bpmval'],arr[3]+i['bpval'],arr[4]+1]
                        finres[calendar.month_name[i['entered_at'].month]]=newarr
                    else:
                        finres[calendar.month_name[i['entered_at'].month]]=[i['tempval'],i['spo2val'],i['bpmval'],i['bpval'],1]
                

                return Response(finres)

        return Response("nada")


from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

class EmailView(APIView):
    def post(self, req):
        # template = render_to_string('templates/email_template.html', {'name':"mansi"})
        patid=req.data['patid']
        result=query(F"select email from elder_userprofile where id=(select patrel_id from elder_patientrelative where id='{patid}');")[0]
        result2=query(F"select * from elder_medicalstaff where medstaff_id='{req.data['doctid']}';")[0]
        
        email = EmailMessage(
            f"{result2['hospname']} has requested to add you.",
            f"The request of adding has been received from .\n Hospital Name : {result2['hospname']}\n Hospital Address : {result2['address']},\n City : {result2['city']},\nState : {result2['state']},\nPincode : {result2['pincode']}\n\n If the request is genuine please login to the portal and approve the request.\nProvided link?\nWith 💖\nFrom Autobuddys.",
            settings.EMAIL_HOST_USER,
            [result['email']],
            )
        email.fail_silently = False
        email.send()
        return Response("sentt")
            
# to get the hospital details of the entered staff ID
class GetHospitalDetails(APIView):
    def get(self,req,pk,format=None):
        
        result=query(F"select * from elder_medicalstaff where medstaff_id='{pk}';")
        # print(result[0])
        if len(result)==1:return Response(result[0])

        return Response("Did not find")

# from the staff ID get the ID of the hospital
class GetHospID(APIView):
    def get(self,req,pk,format=None):
        result=query(F"select id from elder_medicalstaff where medstaff_id='{pk}';")
        if len(result)==1:return Response(result[0])

        return Response("Did not find")

# check from the notifications table whether a request has already been sent to this patient before
class CheckHospID(APIView):
    def get(self,req,pk,format=None):
        respehle=query(F"select * from elder_patientrelative where id='{pk}';")
        if len(respehle)==0:return Response("Not there")
        result=query(F"select * from elder_notification where patid_id='{pk}';")
        if len(result)==0:return Response(True)

        return Response(False)

class GetMessages(APIView):
    def get(self,req,pk,format=None):
        result=query(F"select * from elder_notification where patid_id='{pk}' and approved=False;")
        if len(result)>0:return Response(result)

        return Response("False")

# Get the notification ID from the patient's id
class GetNotificationID(APIView):
    def get(self,req,pk,format=None):
        result=query(F"select id from elder_notification where patid_id='{pk}';")
        if len(result)==1:return Response(result)

        return Response("False")

# To get the details of all the patients whom the doctor has sent requests
class GetNotifiedPatient(APIView):
    def get(self,req,pk,format=None):
        result2=[]
        appr=[]
        result=query(F"select id from elder_medicalstaff where medstaff_id='{pk}';")
        if len(result)==1:
            result1=query(F"select patid_id,approved,rejected from elder_notification where staffid_id='{result[0]['id']}' and removefromlist=false;")
            if len(result1)>=1:
                for i in range(0,len(result1)):
                    appr.append(result1[i])
                    
                    result2=result2+query(F"select * from elder_patientrelative where id='{result1[i]['patid_id']}';")
                
                    result2[i].update(patid_id=result1[i]['patid_id'])
                    result2[i].update(approved=result1[i]['approved'])
                    result2[i].update(rejected=result1[i]['rejected'])

                return Response(result2)

        return Response("False")


import face_recognition
import base64
from django.core.files.base import ContentFile
import urllib.request
from PIL import Image


class ImageViewset(APIView):
    def __init__(self):
        self.known_face_encoding = [] 
        self.known_person = []
        self.face_locations = []  
        self.face_encodings = []  
        self.face_names = []
        self.known_image = []    
        self.counter = 0
        

    def face_recog_setup_one(self,id):
        result = query(f"select * from elder_patientimage where patid={id}")
        # print(result[0]['imageFile'])
        urllib.request.urlretrieve(
        f"https://patientmedia.s3.ap-south-1.amazonaws.com/{result[0]['imageFile']}",result[0]['imageFile'][6:])
        known_image = face_recognition.load_image_file(result[0]['imageFile'][6:])
        print("known-image : ",known_image)
        # print(result[0]['imageFile'])
        try:
            # known_image = face_recognition.load_image_file(result[0]['imageFile'])
            # print("known-image : ",known_image)
           
            self.known_face_encoding.append(face_recognition.face_encodings(known_image)[0])
        except Exception as e:  
            pass
        # print(self.known_face_encoding)
        return self.known_face_encoding[0].tolist()
    
    def base64_file(self,req,name="dumb"):
        imgstr = req.data['imgstr']
        ext = req.data['type'].split('/')[-1]
        # if not name:
        #     name = _name.split(":")[-1]
        return ContentFile(base64.b64decode(imgstr), name='{}.{}'.format(name+str(req.data['patid']), ext))

    def post(self, req):
        image = models.PatientImage(imageFile=self.base64_file(req),patid=req.data['patid'])
        image.save()
        x=self.face_recog_setup_one(req.data["patid"])
        req.data["encoding"]=x
        try:
            p=serializers.PostImageSerializer(data=req.data)
            if p.is_valid(raise_exception=True):
                p.save()
        except Exception as e:
            pass
        return Response({"message":"donee yaya"})
        # print(image)
        # import io, base64
        # from PIL import Image
        # imgstr = req.data['imgstr']
        # # print(image_data)
        # # format, imgstr = image_data.split(';base64,')
        # # print("format : ", req.data['type'])
        # ext = req.data['type'].split('/')[-1]
        # data = ContentFile(base64.b64decode(imgstr))  
        # file_name = "'myphoto." + ext
        # print("file name : ",file_name)
        # img = Image.open(io.BytesIO(base64.decodebytes(bytes(req.data["imgstr"], "utf-8"))))
        # img.save('media/image.jpg')


        # try:
        #     im=serializers.PatientImageSerializer(data={"imageFile":file_name,"patid":req.data["patid"]})
            
        #     if im.is_valid(raise_exception=True):
        #         print("haan validate toh hua")
        #         im.save()
        #         x=self.face_recog_setup_one(req.data["patid"])
        #         req.data["encoding"]=x
        #         try:
        #             p=serializers.PostImageSerializer(data=req.data)
        #             if p.is_valid(raise_exception=True):
        #                 p.save()
        #         except Exception as e:
        #             pass
        #         return Response({"message":"doneeeeeeeeeeeeeeeeeeeeeee yaya"}) 
        # except Exception as e:
        #     pass
        # return Response({"message":"not done yaya"}) 

                  


# yahan pe karo change
class CompareImages(APIView):
    def post(self,req,format=None):
        print(req.data["encodings"])

        return Response("False")
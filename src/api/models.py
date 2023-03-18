from django.db import models

# Create your models here.

class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    file = models.FileField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    file_link = models.CharField(max_length=3000,default='')
    file_owner = models.CharField(max_length=3000,default='')
    
class Doctor(models.Model):
    docter_user_id = models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    studies = models.CharField(max_length=100,default='')
    specality = models.CharField(max_length=300,default='')
    hospital = models.CharField(max_length=300,default='')
    yrs_of_exp = models.IntegerField()
    qr_id = models.CharField(max_length=300,default='')
    
class PatientUser(models.Model):
    user_id = models.CharField(max_length=300, primary_key=True)
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    blood_type = models.CharField(max_length=10)
    height = models.IntegerField()
    weight = models.IntegerField()
    alegries = models.CharField(max_length=300)
    known_disease = models.CharField(max_length=300)
    #bmi overweigh underweight
    
    # some values
    blood_pressure = models.CharField(max_length=10) #last recorder
    blood_glucose = models.CharField(max_length=10) #last recorder
    last_assigned_doctor = models.CharField(max_length=300) #last assigned doctor
    no_of_appointments = models.IntegerField() #no of appointments
    
    # User Files
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    file_title = models.CharField(max_length=300)
    file_info = models.CharField(max_length=3000)
    file_hocr = models.CharField(max_length=3000)
    file_ner_dict = models.CharField(max_length=3000,default='')
    
    
    # Docter asasined to the user
    is_doc_assigned = models.BooleanField(default=False)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
class PatientUserChats(models.Model):
    user_id = models.ForeignKey(PatientUser, on_delete=models.CASCADE)
    chat_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300, default='') # from title model
    timestamp = models.DateTimeField(auto_now_add=True)
    
class PatientUserChatMessages(models.Model):
    chat_id = models.ForeignKey(PatientUserChats, on_delete=models.CASCADE)
    message_id = models.AutoField(primary_key=True)
    user_query = models.CharField(max_length=3000,default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    model_answer = models.CharField(max_length=3000,default='')
    #model_score = models.FloatField()
    alert = models.BooleanField(default=False)
    answer_severity = models.CharField(max_length=300,default='')
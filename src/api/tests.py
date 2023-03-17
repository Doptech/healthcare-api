from serializers import *

Doctor.objects.create(docter_user_id = '786283473', name = 'Vurshali Chaudhari', studies = 'MBBS', specality = 'Oconlogy', hospital = 'Shreyas Hospital Panvel', yrs_of_exp = 13, qr_id = '4322324213')

Doctor.objects.create(docter_user_id = '786283473', name = 'Vurshali Chaudhari', studies = 'MBBS', specality = 'Oconlogy', hospital = 'Shreyas Hospital Panvel', yrs_of_exp = 13, qr_id = '4322324213')
patientuser = PatientUser.objects.filter(user_id = 'R6AziGQwFvNoUTHiSmmwrHhHE7w1').first()
PatientUserChats.objects.create(user_id = patientuser,title = 'My Chat')

main_queryset = PatientUserChats.objects.filter(user_id = 'R6AziGQwFvNoUTHiSmmwrHhHE7w1').all().first()
main_queryset_2 = PatientUserChatMessages.objects.create(chat_id = main_queryset, 
                                                    user_query = "My blood pressure is normally 140/90 mm of Hg, sometimes 150/100 mm of Hg. I am taking the following medicines.",
                                                    model_answer = "YI suggest you do CBC (complete blood count), LFT (liver function test), fasting blood sugar, and fasting lipid profile. Please let me know if you are still taking Tenormin 25, Metromax 25, or both.",
                                                    model_score = 0.9,
                                                    alert = False)
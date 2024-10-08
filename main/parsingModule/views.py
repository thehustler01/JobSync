# import tempfile

# from resume_parser import resumeparse 
# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# # from pyresparser import ResumeParser
# from django.views.decorators.csrf import csrf_exempt
# # nlp = spacy.load("en_core_web_sm")

# def get_resume(request):
#     print("Request received")
#     return HttpResponse("hiiiiiiiiiiiii")
# def upload_resume(request):
    
#     if request.method == 'POST' and request.FILES['file']:
#         resume = request.FILES['file']
        
#         # Save the file temporarily
#         with tempfile.NamedTemporaryFile(delete=True, suffix='.pdf') as temp_file:
#             # Write the uploaded PDF file to the temporary file
#             for chunk in resume.chunks():
#                 temp_file.write(chunk)
#             temp_file.flush()  # Ensure the file is written
#         # file_path = os.path.join('path_to_temp_directory', resume.name)  # Specify the path where you want to temporarily save files
#         # with open(file_path, 'wb+') as destination:
#         #     for chunk in resume.chunks():
#         #         destination.write(chunk)
#             data = resumeparse.read_file(temp_file.name)
#         # os.remove(file_path)
#         return JsonResponse({'success': True, 'parsed_data': data})

#     return render(request, 'resumeParser.html')


import tempfile
from django.shortcuts import render
from django.http import HttpResponse, FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

def get_resume(request):
    print("Request received")
    return HttpResponse("hiiiiiiiiiiiii")

@csrf_exempt
def upload_resume(request):
    if request.method == 'POST' and request.FILES['resume']:
        resume = request.FILES['resume']
        
        # Save the file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            # Write the uploaded PDF file to the temporary file
            for chunk in resume.chunks():
                temp_file.write(chunk)
            temp_file.flush()  # Ensure the file is written

        # Serve the file for display in browser
        return JsonResponse({'success':True,'pdf_url': temp_file.name})

    return render(request, 'resumeParser.html')

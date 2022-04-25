from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect,render
from .models import Student, Track
from .forms import StudentForm
from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_all_student(request):
    all_st= Student.objects.all()
    st_ser = StudentSerializer(all_st, many=True)
    return Response(st_ser.data)

@api_view(['GET'])
def api_one_student(request, st_id):
    st = Student.objects.get(id = st_id)
    st_ser = StudentSerializer(st, many=False)
    return Response(st_ser.data)

@api_view(['POST'])
def api_add_student(request):
    print(request.data)
    st_ser = StudentSerializer(data = request.data)
    if st_ser.is_valid():
        st_ser.save()
        return redirect('api-all')

@api_view(['POST'])
def api_edit_student(request, st_id):
    st = Student.objects.get(id = st_id)
    st_ser = StudentSerializer(instance =st, data= request.data)
    if st_ser.is_valid():
        st_ser.save()
        return redirect('api-all')

@api_view(['DELETE'])
def api_del_student(request,st_id):
    st = Student.objects.get(id = st_id)
    st.delete()
    return Response('Student deleted')


# Create your views here.
def home(request):
    all_students = Student.objects.all()
    return render(request,'app1/home.html',{'student_list':all_students})
    
def show(request, st_id):
    st = Student.objects.get(id=st_id)
    context = {'st': st}
    return render(request, 'app1/show.html', context)
    
def del_St(request, st_id):
    st = Student.objects.get(id = st_id)
    st.delete()
    return redirect('home')

def addStudent(request):
    st_form = StudentForm()
    if request.method == 'POST':
        st_form = StudentForm(request.POST)
        if st_form.is_valid():
            st_form.save()
            return redirect('home')
    context = {'st_form' : st_form}
    return render(request, 'app1/add.html', context)

def editStudent(request,st_id):
    st = Student.objects.get(id= st_id)
    st_form = StudentForm(instance = st)
    if request.method == 'POST':
        st_form = StudentForm(request.POST, instance=st)
        if st_form.is_valid():
            st_form.save()
            return redirect('home')

    context = {'st_form' : st_form}
    return render(request, 'app1/edit.html', context)
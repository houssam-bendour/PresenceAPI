import jwt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from project.settings import SECRET_KEY
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

class AdminRegisterView(APIView):
  def post(self, request):
      serializer = UserSerializer(data=request.data)
      if serializer.is_valid():
          serializer.save()
          return Response(serializer.data)
      return({'message':'{}'.format(serializer.errors)})
    
class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, pk=None):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if user.user_type !=3 :
              if pk == None:
                data = User.objects.filter(is_deleted=False)
                serializer = UserSerializer(data, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
              else:
                  data = get_object_or_404(User,id=pk,is_deleted=False)
                  serializer = UserSerializer(data)
                  return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({'message':'utilisateur non autorisé'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST) 
    
    def put(self, request, pk):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if user.user_type ==1 :
              user_ = get_object_or_404(User,id=pk,is_deleted=False)
              serializer = UserSerializer(user_, data=request.data)
              
              if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
              else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'utilisateur non autorisé pour la modification'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if user.user_type == 1 :
              user_ = get_object_or_404(User,id=pk,is_deleted=False)
              user_.is_deleted=True
              user_.save()
              return Response({'message': 'utilisateur supprimé avec succès'}, status=status.HTTP_204_NO_CONTENT)
              
            else:
                return Response({'message':'utilisateur non autorisé pour la suppression'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST) 
    
    def post(self, request):
        user_data={}
        if request.data['user_type']=='1':
          user_data = {
            "email": request.data['email'],
            "password": request.data['password'],
            "user_type": request.data['user_type'],
            "first_name": request.data['first_name'],
            "last_name": request.data['last_name'],
            "is_superuser": True,
            "is_staff": True,
          }
        elif request.data['user_type']=='2':
           user_data = {
            "email": request.data['email'],
            "password": request.data['password'],
            "user_type": request.data['user_type'],
            "first_name": request.data['first_name'],
            "last_name": request.data['last_name'],
            "is_superuser": False,
            "is_staff": False,
            }
        else:
           user_data = {
            "email": request.data['email'],
            "password": request.data['password'],
            "user_type": request.data['user_type'],
            "first_name": request.data['first_name'],
            "last_name": request.data['last_name'],
            "rfid": request.data['rfid'],
            "CNE": request.data['CNE'],
            "is_superuser": False,
            "is_staff": False,
            }
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
          serializer.save()
          return Response(serializer.data, status=status.HTTP_200_OK)
        else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('csrftoken')
        response.data = {
            'message': 'success'
        }
        return response
    
class ModuleView(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk=None):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if pk == None:
              if user.user_type ==3 :
                  inscriptions = Inscrire.objects.filter(Q(student_id=user.id) & Q(is_deleted=False))
                  if not inscriptions:
                    return Response({'error': 'Student not inscribed'}, status=status.HTTP_404_NOT_FOUND)
                  modules = Module.objects.filter(Q(inscriptions_module__in=inscriptions) & Q(is_deleted=False))
                  serializer = ModuleSerializer(modules, many=True)
                  return Response(serializer.data, status=status.HTTP_200_OK)
              elif user.user_type ==2 :
                  modules = Module.objects.filter(Q(prof_id=user.id) & Q(is_deleted=False))
                  if not modules:
                    return Response({'error': 'prof not inscribed in this module'}, status=status.HTTP_404_NOT_FOUND)
                  serializer = ModuleSerializer(modules, many=True)
                  return Response(serializer.data, status=status.HTTP_200_OK)
              else:
                  modules = Module.objects.filter(is_deleted=False)
                  serializer = ModuleSerializer(modules, many=True)
                  return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = Module.objects.filter(Q(id=pk) & Q(is_deleted=False)).first()
                if not data:
                  return Response({'error': 'not module by this id'}, status=status.HTTP_404_NOT_FOUND)
                serializer = ModuleSerializer(data)
                return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST) 

    def post(self, request, format=None):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
          user = User.objects.filter(id=payload["user_id"]).first()
          if user.user_type ==2 :
            user_data = {
            "prof_id": user.id,
            "name": request.data['name']
            }
            serializer = ModuleSerializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          elif user.user_type ==1 :
              serializer = ModuleSerializer(data=request.data)
              if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          return Response({'message':'utilisateur non autorisé'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
          return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST) 

    def put(self, request, pk):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if user.user_type ==1 :
              module_ = get_object_or_404(Module,id=pk,is_deleted=False)
              serializer = ModuleSerializer(module_, data=request.data)
              if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
              else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif user.user_type ==2 :
              modules = Module.objects.filter(Q(id=pk) & Q(is_deleted=False) & Q(prof_id=user.id)).first()
              if not modules:
                return Response({'error': 'not module by this id'}, status=status.HTTP_404_NOT_FOUND)
              serializer = ModuleSerializer(modules, data=request.data)
              if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
              else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'utilisateur non autorisé pour la modification'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if user.user_type == 1 :
              module_ = get_object_or_404(Module,id=pk,is_deleted=False)
              module_.is_deleted=True
              module_.save()
              return Response({'message': 'module supprimé avec succès'}, status=status.HTTP_204_NO_CONTENT)
            elif user.user_type ==2 :
              modules = Module.objects.filter(Q(id=pk) & Q(is_deleted=False) & Q(prof_id=user.id)).first()
              if not modules:
                return Response({'error': 'not module by this id'}, status=status.HTTP_404_NOT_FOUND)
              modules.is_deleted=True
              modules.save()  
              return Response({'message': 'utilisateur supprimé avec succès'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message':'utilisateur non autorisé pour la suppression'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST) 
    
class PresenceList(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request,pk=None, format=None):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            print(user.user_type)
            if pk == None:
              if user.user_type ==2 :
                session = Session.objects.filter(Q(prof_id=user.id) & Q(is_deleted=False))
                if not session:
                  return Response({'error': 'not session exicted'}, status=status.HTTP_404_NOT_FOUND)
                session_ids = session.values_list('id', flat=True)
                for i in session_ids:
                  print(i)
                presences = Presence.objects.filter(Q(session_id__in=session_ids) & Q(is_deleted=False))
                serializer = PresenceSerializer(presences, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
              elif user.user_type ==3 :
                presences = Presence.objects.filter(Q(student_id=user.id) & Q(is_deleted=False))
                serializer = PresenceSerializer(presences, many=True)
                return Response(serializer.data)
              else:
                presences = Presence.objects.filter(is_deleted=False)
                serializer = PresenceSerializer(presences, many=True)
                return Response(serializer.data)
            else:
              presence = get_object_or_404(Presence,id=pk,is_deleted=False)
              serializer = PresenceSerializer(presence)
              return Response(serializer.data)
        except Exception as e:
            return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)        

class PresenceView(APIView):
    def post(self, request, pk, format=None):
        date_courante = timezone.now().strftime("%Y-%m-%d")
        timec = timezone.now().time().strftime("%H:%M:%S")
        print(date_courante)
        print(timec)
        session = Session.objects.filter(Q(date=date_courante) & Q(start_time__lte=timec) & Q(end_time__gte=timec) & Q(is_deleted=False)).first()
        if not session:
            return Response({'error': 'session not found'}, status=status.HTTP_404_NOT_FOUND)
        print(session.module_id)
        user = User.objects.filter(Q(rfid=pk) &  Q(is_deleted=False)).first()
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        insc = Inscrire.objects.filter(Q(student_id=user.id) & Q(is_deleted=False) & Q(module_id=session.module_id)).first()
        if not insc:
            return Response({'error': 'student not inscrit'}, status=status.HTTP_404_NOT_FOUND)
        exicted = Presence.objects.filter(Q(student_id=user.id) & Q(is_deleted=False) & Q(session_id=session.id)).first()
        if exicted:
            return Response({'error': 'Already present'}, status=status.HTTP_404_NOT_FOUND)
        presence_data = {
            "student_id": user.id,
            "session_id": session.id,
            "pointing": timec,
        }
        serializer = PresenceSerializer(data=presence_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SessionView(APIView):
   permission_classes=(IsAuthenticated,)
   def get(self, request,pk=None, format=None):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if pk == None:
              if user.user_type ==2 :
                sessions = Session.objects.filter(Q(prof_id=user.id) & Q(is_deleted=False))
                if not sessions:
                  return Response({'error': 'not session exected'}, status=status.HTTP_404_NOT_FOUND)
                # presences = Presence.objects.filter(Q(Session__in=session) & Q(is_deleted=False))
                serializer = SessionSerializer(sessions, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
              elif user.user_type ==3 :
                inscriptions = Inscrire.objects.filter(Q(student_id=user.id) & Q(is_deleted=False))
                if not inscriptions:
                    return Response({'error': 'Student not inscribed'}, status=status.HTTP_404_NOT_FOUND)
                module_ids = inscriptions.values_list('module_id', flat=True)
                sessions = Session.objects.filter(Q(module_id__in=module_ids) & Q(is_deleted=False))
                serializer = SessionSerializer(sessions, many=True)
                return Response(serializer.data)
              else:
                sessions = Session.objects.filter(is_deleted=False)
                serializer = SessionSerializer(sessions, many=True)
                return Response(serializer.data)
            else:
              sessions = get_object_or_404(Session,id=pk,is_deleted=False)
              serializer = SessionSerializer(sessions)
              return Response(serializer.data)
        except Exception as e:
            return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST) 

   def post(self, request, format=None):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if user.user_type==2:
              session_data = {
                          "prof_id": user.id,
                          "date": request.data['date'],
                          "start_time": request.data['start_time'],
                          "end_time": request.data['end_time'],
                          "module_id": request.data['module_id'],
                          "titre": request.data['titre'],
                          "discreption": request.data['discreption'],
                          }
              serializer = SessionSerializer(data=session_data)
              if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif user.user_type==1:
              serializer = SessionSerializer(data=request.data)
              if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=status.HTTP_201_CREATED)
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message':'utilisateur non autorisé'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)
        
   def put(self, request, pk):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if user.user_type ==1 :
              session = get_object_or_404(Session,id=pk,is_deleted=False)
              serializer = SessionSerializer(session, data=request.data)
              if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
              else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif user.user_type ==2 :
              session = Session.objects.filter(Q(id=pk) & Q(is_deleted=False) & Q(prof_id=user.id)).first()
              if not session:
                return Response({'error': 'not session by this id'}, status=status.HTTP_404_NOT_FOUND)
              serializer = SessionSerializer(session, data=request.data)
              if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
              else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'utilisateur non autorisé pour la modification'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST)

   def delete(self, request, pk):
        token = request.META.get('HTTP_AUTHORIZATION') 
        token = token.replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if user.user_type == 1 :
              session = get_object_or_404(Session,id=pk,is_deleted=False)
              session.is_deleted=True
              session.save()
              return Response({'message': 'session supprimé avec succès'}, status=status.HTTP_204_NO_CONTENT)
            elif user.user_type ==2 :
              session = Session.objects.filter(Q(id=pk) & Q(is_deleted=False) & Q(prof_id=user.id)).first()
              if not session:
                return Response({'error': 'not session by this id'}, status=status.HTTP_404_NOT_FOUND)
              session.is_deleted=True
              session.save()  
              return Response({'message': 'session supprimé avec succès'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message':'utilisateur non autorisé pour la suppression'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':'{}'.format(e)},status=status.HTTP_400_BAD_REQUEST) 
    
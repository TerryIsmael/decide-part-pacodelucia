from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_200_OK as ST_200,
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409,
        HTTP_500_INTERNAL_SERVER_ERROR as ST_500
)

from base.perms import UserIsStaff
from .models import Census

from io import BytesIO
from pandas import read_excel, DataFrame
from ldap3 import Connection, Server, ALL_ATTRIBUTES, SUBTREE
from local_settings import AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD
from .serializers import StringListSerializer, CensusSerializer

class CensusCreate(generics.ListCreateAPIView):
    # permission_classes = (UserIsStaff,)
    serializer_class = StringListSerializer

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error trying to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')

class CensusImport(generics.ListCreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            uploaded_file = request.FILES.get('file')
            content = uploaded_file.read()

            extension = uploaded_file.name.split(".")[-1]
            if extension == 'xlsx':
                df = read_excel(BytesIO(content), engine='openpyxl')
            elif extension == 'xls':
                df = read_excel(BytesIO(content))
            else:
                raise Exception("Uploaded file is not an excel file")

            for _, row in df.iloc[1:].iterrows():
                census = Census(voting_id=row['voting_id'], voter_id=row['voter_id'])
                census.save()
               
        except IntegrityError as e:
            if not 'unique constraint' in str(e).lower():
                return Response('Error trying to create census', status=ST_409)
        except Exception as e:
            return Response('Error processing Excel file', status=ST_500)
        return Response('Census created', status=ST_201)

class CensusExport(generics.RetrieveAPIView):
    def retrieve(self, request, voting_id = None, *args, **kwargs):
        try:
            if voting_id:
                censuses = Census.objects.filter(voting_id=voting_id)
            else:
                censuses = Census.objects.all()

            censuses_list = [(c.voting_id, c.voter_id) for c in censuses]

            df = DataFrame(censuses_list, columns=['voting_id', 'voter_id'])
            excel_stream = BytesIO()
            df.to_excel(excel_stream, index=False)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=output.xlsx'
            excel_stream.seek(0)
            response.write(excel_stream.read())
               
        except Exception as e:
            return Response('Error processing request', status=ST_500)
        return response

class CensusImportLDAP(generics.ListCreateAPIView):
    serializer_class = StringListSerializer

    def list(self, request, *args, **kwargs):
        try:
            server = Server(AUTH_LDAP_SERVER_URI)

            ldap_response = []
            with Connection(server, 
                            user=AUTH_LDAP_BIND_DN, 
                            password=AUTH_LDAP_BIND_PASSWORD, 
                            auto_bind=True) as conn:
                users = conn.search(search_base='dc=decide,dc=org',
                                    search_filter='(&(objectClass=inetOrgPerson)(!(cn=decidesuperuser)))',
                                    search_scope=SUBTREE,
                                    attributes=ALL_ATTRIBUTES)
                ldap_response = conn.response
            
            voters = []
            for user in ldap_response:
                voters.append(user["attributes"]["cn"][0])

        except Exception:
            return Response('Error listing LDAP all users\' cn', status=ST_500)
        return Response({"LDAP voters": voters})
    
    def create(self, request, *args, **kwargs):
        try:
            voting_id = request.data.get("voting_id")
            voters = request.data.get("voters")
            server = Server(AUTH_LDAP_SERVER_URI)

            with Connection(server, user=AUTH_LDAP_BIND_DN, password=AUTH_LDAP_BIND_PASSWORD, auto_bind=True) as conn:
                for cn in voters:
                    result = conn.search(search_base='dc=decide,dc=org',
                                        search_filter=f'(&(objectClass=inetOrgPerson)(cn={cn})(!(cn=decidesuperuser)))',
                                        search_scope=SUBTREE,
                                        attributes=ALL_ATTRIBUTES)
                    voter_id = conn.response[0]["attributes"]["uid"][0]
                    census = Census(voting_id = voting_id, voter_id = voter_id)
                    census.save()
               
        except IntegrityError as e:
            if not 'unique constraint' in str(e).lower():
                return Response('Error trying to create census', status=ST_409)
        except Exception as e:
            return Response('Error processing request', status=ST_500)
        return Response('Census created', status=ST_201)

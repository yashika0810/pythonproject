from django.contrib.auth.models import User
class LoginMemberSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields =[
        'name',
        'password',
        'email',
    ]
# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.core.mail import EmailMessage
#from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


from accounts.serializers import UserSerializer
from accounts.models import CustomUser as User

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            # Generate verification token and send email
            verification_token = self.generate_verification_token(user)
            self.send_verification_email(user.email, verification_token)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Function to generate a verification token using Django's TokenGenerator
    def generate_verification_token(self, user):
        # Generate a unique verification token for the user
        token_generator = default_token_generator
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verification_token = f"{uid}_{token}"

        return verification_token

    # Function to send the verification email using Django's EmailMessage
    def send_verification_email(self, email, verification_token):
        # Compose and send the verification email
        current_site = get_current_site(self.request)
        verification_url = reverse('verify-email')
        absolute_url = f"http://{current_site.domain}{verification_url}?token={verification_token}"
        subject = 'Verify Your Email'
        message = f'Click the following link to verify your email: {absolute_url}'
        from_email = 'settings.EMAIL_HOST_USER'
        to_email = [email]
        email = EmailMessage(subject, message, from_email, to_email)
        email.send()

class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')

        try:
            uidb64, token = token.split('_', 1)
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                # Mark the email as verified
                user.email_verified = True
                user.save()

                return Response({'message': 'Email verification successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid verification token.'}, status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response({'message': 'Invalid verification token: TypeError.'}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response({'message': 'Invalid verification token: ValueError.'}, status=status.HTTP_400_BAD_REQUEST)

        except OverflowError:
            return Response({'message': 'Invalid verification token: OverflowError.'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'message': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Validate username and password
        if not username or not password:
            return Response({'message': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate token
        token = self.generate_token(user)

        # Return token and user details
        serializer = UserSerializer(user)
        data = {
            'token': token,
            'user': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def generate_token(self, user):
        # Generate token for user
        #token_generator = default_token_generator
        #token = token_generator.make_token(user)
        token = Token.objects.create(user=user)
        return token.key

class UserProfileView(APIView):
    def get(self, request):
        # Implement logic to retrieve user profile
        pass

    def put(self, request):
        # Implement logic to update user profile
        pass

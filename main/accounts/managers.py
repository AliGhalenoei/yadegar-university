from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):

    def create_user(self , email , username , password):
        if not email:
            raise ValueError("Error Email")
        if not username:
            raise ValueError("Error username")
        
        user = self.model(email = self.normalize_email(email),username=username)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self , email , username , password):
        user = self.create_user(email , username , password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
